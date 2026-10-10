# Cloud shadowing runbook - VCF522-Upgrade-VCF9.1-REV1 into the 8 Clearwater OVDCs (tenant `livefire`)

Citations: "AG p#" = `<project-root>/reference/vmware-lab-platform.pdf` (printed page = PDF page). "API p#" = `vlp.rest.api.pdf` (VLP-Admin/vlp.admin/doc).
Definition: `classes/shadow_yaml/shadow.clearwater.vcf522-upgrade.yaml` (validate: `python3 ~/.claude/skills/vlp-admin/scripts/vlp_shadow.py <file>`).
Flow: `~/.claude/skills/vlp-admin/scripts/flows/shadowing.py` (dry-run default). Source recording: `recordings/shadowing.py`. Verify: `docs/dry-run.ui.checklist.md` section 15.
Pool side: `docs/deployment-pool.runbook.md` (pool rows are per template-OVDC; an OVDC without the template/shadow gives no row and no capacity). SKILL runbook step 6a.

Status 2026-10-08: DONE-pending-verification. The user performed the shadowing live in tenant `livefire` (recorded, Ok clicked 8 times). Nothing is verified in the UI yet (`verified: false`).

## 1. What was recorded

1. `Cloud Management` (button) > `Cloud Shadow` (link; the guide says "Cloud Shadows", AG p217).
2. Search box `Search...`: typed `VCF522-Upgrade-VCF9.1-REV1`.
3. Per cloud, in this order: expand the cloud-level row (`Open` arrow), click the replica value on each wanted OVDC row, press `Ok` in the prompt (the write), repeat; then `Close`.
   - Cloud row `lvn3-vcd2-eduprod-r` (catalog shown `CM3-EDU-PROD-DGC`, count `1/7`): 2 shadows.
   - Cloud row `lvn9-vcd1-eduprod-r` (`1/7`): 2 shadows.
   - Cloud row `lvn9-vcd2-eduprod-r` (`1/8`): 4 shadows.
4. Total 8 `Ok` clicks = 8 shadow requests. No options (shadow type, storage policy, catalog) were chosen; the only dialog control used was `Ok`.

The OVDC names are NOT in the recording (rows were clicked by grid row id or `.first`). Counts per cloud (2/2/4) and click order match the expected list (ovdc8, ovdc7 | ovdc3, ovdc12 | ovdc6, ovdc7, ovdc8, ovdc13), so the selection is believed correct but is inferred, not proven. Risk: the `.first` clicks (last click in lvn9-vcd1 and lvn9-vcd2) hit "the first remaining replica value on the page", which is the intended OVDC only if no other unshadowed OVDC sorts above it. Checklist section 15 must confirm exactly the 8 and no extras.

## 2. What a shadow is (docs)

- AG p217: in vCD, deploying a vApp into a storage pool other than the one holding the template first deploys a shadow copy in the new pool, then the vApp from it: a double deployment that can take long and leaves the student waiting. The administrator can pre-deploy a shadow into pools that lack a copy (AG p217-218).
- Placement (AG p216): a VDC is only a candidate if it has the template directly or as a shadow, the template is available and enabled, and storage is not over-provisioned. No shadow in an OVDC means that OVDC is not used for that template's deployments.
- Capacity: each shadow is a copy of the template in the target pool, so it consumes storage there (the guide gives no size or quota figure). Prepops are 0 in our pool, so shadows are the only capacity use for now.
- Preconditions: a cloud system credential must exist for a cloud to use shadow information (AG p215-216; credentials can be updated, AG p25). Cloud org VDC flag `Preshadow Enabled` creates shadows of templates automatically (AG p215); the tenant setting "Create cloud org VDCs and cloud OVDC catalogs with preshadow enabled" is on by default (AG p148). Whether auto-preshadow already made some of ours is UNVERIFIED (the `1/7` and `1/8` counts before our clicks suggest one existing copy per cloud).

## 3. Checking status and progress

- UI (AG p217-218): `Cloud Management > Cloud Shadows`: cloud org, availability and replica status per template; arrow next to the template for detail. `Refresh Shadow Information` runs a shadow update for the selected clouds (wording of the guide; it does not say it creates or deletes shadows).
- Read-only automation: `python3 ~/.claude/skills/vlp-admin/scripts/flows/shadowing.py --browse` (expands each cloud row, prints one line per OVDC; selectors UNVERIFIED).
- API (API p211-213, "CloudShadow API"): `GET /api/admin/CloudShadow?tenant=livefire&cloudOrgs=<display names>`. **The doc describes a schema that does not match the live response** (see KNOWN LIMITATION below) — treat the written spec (`orgVdcs`/`vAppTemplates[].shadows/shares/deploying/primary`) as aspirational, not what you'll actually get back.
- Cloud Tasks (`Cloud Management > Cloud Tasks`, UNVERIFIED path) is where to look for failed copy tasks.
- Large templates take time; do not re-click while a copy is in progress (the flow refuses to re-shadow).

### KNOWN LIMITATION (found 2026-10-10): the CloudShadow API cannot tell you per-template shadow status

The live `GET /api/admin/CloudShadow` response is shaped as a flat list of (template × cloud) rows, each
carrying its own `orgVdcs[]` with a `type` field (`master`/`shadows`/absent). **This `type` field is scoped
to the (cloud, catalog) pair, not to the individual template.** Proof: querying three templates that all sit
in catalog `CM3-EDUPROD-DGC` — `VCF522-Upgrade-VCF9.1-REV1` (really shadowed, user-confirmed in the UI),
`VCF91-AIRI-FastTrack-Rev4` (never shadowed), and `VCF522-June-2027-PWDexpiration-Rev4-Jun05` (an unrelated
template nobody ever touched) — all three returned the *identical* set of OVDCs marked `type=shadows,
shadowEnabled=true`. A template that was never shadowed reads exactly like one that was.

This directly contradicts the documented schema (API p211-213), which says each `vAppTemplates[]` entry
should carry its own `shadows`/`shares`/`deploying`/`primary` arrays of VDC URNs — a genuinely per-template
signal. The live server does not return that shape via `vlp_api.VlpClient` as tested; either the real schema
has changed since the doc was written, or that data exists under a parameter/field not yet found.

Consequence: **do not use `orgVdcs[].type == "shadows"` from this API to mark any shadow yaml
`verified: true`.** It happened twice (`VC80U3-to-VCF911-Upgrade-Clearwater-Rev2` and
`VCF91-AIRI-FastTrack-Rev4` were both wrongly marked confirmed this way on 2026-10-10) and both were
retracted. The only field that varies per-template at all is `replicasCount`/`cloudsForReplicasCount`
("ALL n/3" in the UI) — its exact meaning is still unconfirmed (it correlates with "newly added to the
catalog" rather than shadow completion; see git history on this file for the earlier, also-wrong,
"n/3 = copy progress" theory that was retracted the same day). Until a genuinely per-template signal is
found, the only trustworthy source is a human reading the expanded chevron row in the live UI for that
specific searched template, or asking VLP support / checking vCD directly. `--browse`'s DOM-scrape approach
is inherently just a slower path to the same human read-the-grid check — it is not meaningfully more
automated-trustworthy than the UI it scrapes, since no live code path has confirmed it isn't itself
exposed to the same cloud-wide aggregation this section debunks.

## 4. Running the flow (existence-checked)

```
python3 ~/.claude/skills/vlp-admin/scripts/flows/shadowing.py              # plan only, no browser
python3 ~/.claude/skills/vlp-admin/scripts/flows/shadowing.py --browse     # read-only status per OVDC
python3 ~/.claude/skills/vlp-admin/scripts/flows/shadowing.py --execute    # only OVDCs that read as missing; typed 'yes' per OVDC
```

Targets default to the shadow YAML; `--ovdcs` can switch to the OVDCS list from the project dotenv or to the pool YAML. Every target must be in the pool YAML or the flow refuses. Because the 8 were already requested, a correct `--browse` should show all `existing`; if it shows `missing` for some, either those requests failed or the status heuristic (UNVERIFIED) is wrong: look at the UI before `--execute`.

## 5. Removal / undo

NOT documented in AG p212-218, and the CloudShadow API documents GET only (API p211-213). No delete control is described on the Cloud Shadows page. Ask the user / VLP technical staff; the likely route is removing the replica in vCD directly (outside VLP). Do not remove a shadow a lab or prepop uses; wait for in-progress copies to finish before any cleanup.

## 6. Risks

- Recorded selectors were row-id based (`#clr-dg-rowNN`) and `.first`; the flow instead selects by OVDC name text (UNVERIFIED).
- Wrong OVDC shadowed (extras): consumes storage in OVDCs we do not use; undo path unknown (section 5).
- Catalog text differs: UI row `CM3-EDU-PROD-DGC` vs pool/definition `CM3-EDUPROD-DGC`. Likely a display difference or a typo in one; confirm in the UI (checklist 15).
- Storage in the target pools: check Cloud oVDCs capacity (checklist section 9) after the copies finish.
- Shadows exist only after the vCD copy completes; pool rows and labs depending on them will not deploy until then.
