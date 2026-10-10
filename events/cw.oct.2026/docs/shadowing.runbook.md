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

Fastest check (read-only, API): from the event folder,
`python3 ~/.claude/skills/vlp-admin/scripts/check_shadow.py --templates <t1,t2,...> --ovdcs <o1,o2,...>`
(`--ovdcs` defaults to `OVDCS` in `.env`). Prints `SHADOWED` / `NOT SHADOWED` / `available to shadow` per template per target OVDC; exit 0 only if every target is shadowed.

How the data is laid out (API and UI agree; verified against the live page 2026-10-10):

- API: `GET /api/admin/CloudShadow?tenant=&cloudOrgs=` returns one row per (template, cloud org). Each `orgVdcs[]` entry has `orgVdcName`, `type` (`master` = primary, `shadows` = shadow exists, absent = no shadow), `shadowEnabled` and `available` (true = can be shadowed). Match on `orgVdcName`.
- UI (`Cloud Management > Cloud Shadow`): filter by template, then expand the chevron of each cloud org that holds target OVDCs (different orgs hold different targets). The table's **Type** column is `primary` / `shadow` / `undeployed`; the Availability icon is a dark cloud with a green dot when a shadow exists and an outlined cloud when one can be made. The Replicas value (`n/3`) is not shadow state.
- Cloud Tasks (`Cloud Management > Cloud Tasks`, UNVERIFIED path) is where to look for failed copy tasks.
- Large templates take time; do not re-click while a copy is in progress (the flow refuses to re-shadow).
- `flows/shadowing.py --browse` prints the row text per OVDC; read the Type word in it, and ignore its `existing` label.

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
