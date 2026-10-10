# Deployment pool runbook - VCF522-Upgrade-VCF9.1-REV1 (tenant `livefire`)

Citations: "AG p#" = `<project-root>/reference/vmware-lab-platform.pdf` (page = printed page). "API p#" = `vlp.rest.api.pdf` (VLP-Admin/vlp.admin/doc), page = printed page.
Pool definition: `classes/pool_yaml/pool.clearwater.vcf522-upgrade.yaml` (validate: `python3 ~/.claude/skills/vlp-admin/scripts/vlp_pool.py <file> [--tolerant]`).
Flows: create = `~/.claude/skills/vlp-admin/scripts/flows/create_pool.py`; edits = `flows/edit_pool.py`; shared helpers in `flows/pool_common.py`. See section 11 for the create-vs-update split. create_pool (dry-run default; selectors recorded 2026-10-08; pool already created, so the flow now refuses to create a duplicate). This is runbook step 6 in `~/.claude/skills/vlp-admin/SKILL.md`.

Template status: pool uses `VCF522-Upgrade-VCF9.1-REV1` (catalog `CM3-EDUPROD-DGC`). `VCF91VKS-FastTrack-v5` is still copying: recorded as `plannedTemplate (pending copy)` in `classes/class_yaml/class.clearwater.vks-fasttrack.yaml`; it needs its own pool later (or can be added to this pool only if its VM structure is identical, see 5).

## 1. Decided and open values

| Field (UI label) | Value | Status | Source |
|---|---|---|---|
| Tenant | `livefire` | known | CLAUDE.md |
| Name | `VCF522-Upgrade-VCF9.1-REV1` | decided by user | AG p100 |
| Description | (empty) | USED: none typed in the 2026-10-08 live create; UI accepted it (API lists it as required, API p69; can be set later via row Update) | |
| Primary Lab Template | `VCF522-Upgrade-VCF9.1-REV1`, catalog `CM3-EDUPROD-DGC` | known | AG p100 (single primary template) |
| OVDCs (Cloud Org VDC column) | the 8 in CLAUDE.md `OVDCS` | known list; which OVDCs actually carry the template/shadow = OPEN until pre-check 3 | AG p102 |
| Refill At | 0 | decided | AG p102 |
| Fill Up | 0 | decided | AG p102 |
| Prepops | 0 | decided | AG p102 |
| Enabled (template/pool enabled flag) | `true` (assumed default) | UNVERIFIED: recording did not touch it; confirm in section 6. AG p101 "Enabled" is a per-template checkbox; API create response returns `enabled: true` by default (API p69). Not a create-form field in AG p100. | |
| Explicitly Ready Prepops | off | only exists if Portal Settings > Configuration > Deployments > Explicitly ready prepops is on | AG p100 |
| Tenant assignment | none at pool level; the pool belongs to the tenant it is created in (AG p99 "specific to a single account or organization"); labs reference the pool (AG p106). OVDC-level Tenant Deployment/Assignment flags are staff-controlled (AG p214) | n/a | |

Zero prepops means nothing deploys until sizing is raised later. With Refill At = Fill Up = Prepops = 0 the pool is only a container: no vApp is deployed from it ahead of demand, so students' labs will deploy on demand (slow for large templates, AG p101) until prepops are raised. Raise sizing before the event (see 8).

## 2. What creation does (summary of the docs)

- A deployment pool is a collection of one or more lab templates, specific to one tenant; create it before the lab; a lab must select an existing pool (AG p99).
- Create via `Cloud Management > Deployment Pools` (AG p100): `+ Create New`, enter Name, Description, optional Explicitly Ready Prepops, choose Primary Lab Template from the List View drop-down, click `+ Create Deployment Pool`. The system creates the pool and opens the Edit Lab Templates form (AG p100). Verify the template rows, add or modify Prepops, click `Update Deployment Pool` (AG p100). `Edit VMs` (left pane) edits VM metadata (AG p100, p103-104).
- API equivalent: `POST /api/admin/deploymentPools?tenant=` with `name`, `description`, `cloudVappTemplatesForTenant: {id}` (API p68-69). The response shows `refillAt: 0`, `fillUp: 0`, `enabled: true`: creation by itself sets no prepops.
- "template - ovdc" entries: each vApp template is listed per Cloud Org VDC where it exists, displayName `<template> - <ovdc>` (API p62-66, e.g. "Lab template_4 - wdc-vcd02-vlp-QAtest2-u-ovdc1"). The Edit Lab Templates form shows Cloud Org VDC, Cloud Catalog, Refill At, Fill Up, Prepops, Available, Pools Using per row (AG p102). So Refill At/Fill Up/Prepops are per template-OVDC row and the pool aggregates them (AG p101). UNVERIFIED: whether the create-form drop-down shows one entry per OVDC (likely, from the API naming) or one per template; confirm by recording.
- Structural-identical rule: the primary template enforces identical structure (same number of VMs, OS, CPU, memory, VM names); templates later added are checked against it (AG p100, p101; API p33). "VM Equality Check" option on the Edit form (AG p101). Only one primary template can be chosen at create (AG p100).
- Validation documented: structure match when adding templates (above); cannot remove all templates, or swap all in one edit, while entitlements for labs use the pool (AG p101); a deactivated pool cannot deploy prepops (AG p102). No other create-time validation is documented (name uniqueness etc. UNVERIFIED).

## 3. Pre-create read-only checklist (do first; no clicks that change anything)

Menu paths marked UNVERIFIED must be checked against the live UI.

1. Tenant is `livefire`. Not `eduprod` (cloud capacity only).
2. Template present in the catalog: open `Cloud Management > Clouds`, Cloud Catalogs tab (AG p212; verified path Cloud Management > Clouds in recordings/sync_clouds.py; tab name per AG, UNVERIFIED in UI) and/or `Lab Management > Lab Templates` / `Lab Builder` (AG p59, p75, p119; UNVERIFIED). Confirm `VCF522-Upgrade-VCF9.1-REV1` exists in catalog `CM3-EDUPROD-DGC`.
3. (Shadows were requested 2026-10-08 for the 8 OVDCs; see `docs/shadowing.runbook.md` and checklist section 15. Pool rows need a completed shadow in each OVDC.) Shadowed in which OVDCs: `Cloud Management > Cloud Shadows` (AG p217; UNVERIFIED path) read-only: availability/replica status per cloud org for the template. Fill the per-OVDC table in `docs/dry-run.ui.checklist.md` section 2. Do NOT click `Refresh Shadow Information` or replica ovals. Note which of the 8 OVDCs lack the template; they will not get a row.
4. OVDC flags: `Cloud Management > Cloud oVDCs` (AG p214-215): Enabled / Deployment / Assignment / Preshadow for the 8 OVDCs (read only; only staff change global flags, AG p214).
5. `VCF91VKS-FastTrack-v5` copy status: note finished/not (future item, not blocking).
6. Existing pool check: `Cloud Management > Deployment Pools` (AG p100): name `VCF522-Upgrade-VCF9.1-REV1` or any pool already containing this template must not already exist (avoids duplicates; Pools Using count AG p102). Note whether the Explicitly Ready Prepops option is shown.
7. Tenant setting `Optimized Deployment Pool Usage`: if on with one cloud, pools are hidden and labs pick a Cloud Lab Template instead (AG p106); then creating a pool by hand may be unnecessary.
8. API cross-check (read-only, optional): `python3 ~/.claude/skills/vlp-admin/scripts/vlp_preflight.py` (GET `/api/template/list`, `/api/admin/deploymentPools`).
9. Open items resolved: Description, Enabled; `vlp_pool.py <yaml>` (strict) passes.
10. Permission: account can see Cloud Management (Cloud Management button appears in the recording).

## 4. Create steps (ordered; each UI step is a write needing explicit user go-ahead)

1. Log in (tenant `livefire`). `Cloud Management > Deployment Pools` (AG p100).
2. Click `+ Create New`. [write: opens form only]
3. Name = `VCF522-Upgrade-VCF9.1-REV1`; Description = (decided value); leave Explicitly Ready Prepops off.
4. Primary Lab Template: pick `VCF522-Upgrade-VCF9.1-REV1` (catalog `CM3-EDUPROD-DGC`); if entries are per OVDC (`<template> - <ovdc>`), pick any one of the 8 OVDCs, then add the others in step 6 (UNVERIFIED behavior).
5. Click `+ Create Deployment Pool`. [WRITE: creates the pool; no prepops at 0/0/0]
6. On the Edit Lab Templates form: confirm the rows (Cloud Org VDC, Cloud Catalog); add the remaining OVDC entries with `+ Add Lab Templates` if not listed (AG p101); keep Refill At 0, Fill Up 0, Prepops 0; set Enabled as decided. Click `Update Deployment Pool` only if something changed. [WRITE]
7. Verify (section 6).
Scripted alternative: `flows/create_pool.py --execute` (typed `yes` before the create click); selectors UNVERIFIED until recorded.

## 5. Risks

- Capacity: creating the pool with Refill At/Fill Up/Prepops = 0 consumes no prepop capacity. The Prepop feature deploys an instance of the lab ahead of demand and leaves it running, and re-queues a deployment whenever one is assigned (AG p101). "Prepops ... If you adjust this number, it will add/remove prepops" (AG p102); if available prepops drop below Refill At the system deploys until met (AG p102). So the capacity risk starts when any of these is raised above 0 on an enabled row in an enabled pool, per OVDC row. Estimate total = sum of Prepops across rows; multiply by the template's VM CPU/RAM/storage. Large templates can be hundreds of GB (AG p101).
- Aggregation/sharing: if the same template sits in several pools, editing its shared values recalculates every pool (AG p101).
- Structure mismatch when adding `VCF91VKS-FastTrack-v5` later to this pool (AG p100).
- Template/OVDC rows missing from some OVDCs (shadow not ready) mean those OVDCs provide no capacity.
- Once a lab/entitlement uses the pool, template swaps are restricted: add new then remove old in two edits (AG p101); the API remove-template call is documented as "Bug - does not work" (API p34).
- The guide is the older VMware-branded text; Broadcom UI labels may differ.

## 6. Post-create verification checklist (read-only)

- `Cloud Management > Deployment Pools` list shows the pool name (AG p101).
- `More details` (three-dot) shows Labs, VMs, Lab Templates; Refill At/Fill Up 0; Available 0; Provisioning 0; Error Count 0 (AG p105).
- Edit Lab Templates rows: template present with expected Cloud Org VDC/Catalog entries; Prepops 0 each.
- `Cloud Management > Cloud Tasks` (AG p101): no queued/failed deployment tasks for this pool (UNVERIFIED nothing is queued at 0).
- API: `GET /api/admin/deploymentPools?tenant=livefire` (API p62) shows the pool with `refillAt: 0`, `fillUp: 0`, `enabled` as decided, `cloudVappTemplatesForTenant` entries `<template> - <ovdc>`; or rerun `vlp_preflight.py`.
- Record the pool name in `labPrereqs.deploymentPool` of the class YAML.
- Optional: Download page action (CSV/Excel) exports pool/lab/template relations (AG p104).

## 7. Edit / delete / rollback

- Edit (AG p104-105): row three-dots menu: Update (name/description), Edit Lab Templates, Edit VMs, Delete, Refill At, Fill Up, Drain Prepops, Sync Prepops, Remove Lab Templates, Remove Obsolete VMs, Apply/Remove Tags, Clear Errors. API: `PUT /api/admin/deploymentPools/<id>` for name/description (API p73).
- Undo a mistaken prepop sizing: set Prepops/Refill At/Fill Up back to 0 on the Edit Lab Templates form, then `Drain Prepops` (undeploys all prepops, AG p104; API p40 `/api/pool/<id>/drain`). Draining removes deployed vApps from the cloud; confirm no student is mid-assignment.
- Delete an empty pool created by mistake: three-dots > Delete (AG p104); API `DELETE /api/admin/deploymentPools/<id>?tenant=` (API p77). Do this only while no lab references the pool (UNVERIFIED enforcement) and after draining. There is no documented undelete; recreating the pool is the recovery.
- Do not use Sync Prepops unless prepops look invalid (AG p105): it creates missing prepops.
- Rollback order: set sizing to 0, Drain Prepops, detach from any lab, Delete.

## 8. Raising sizing later (not now)

Choose per-OVDC Prepops/Refill At/Fill Up after capacity checks, edit `refillAt`/`fillUp`/`prepops`/`perOvdc` in the pool YAML for the record, then change them in Edit Lab Templates and click `Update Deployment Pool`. Docs do not state `Fill Up >= Refill At`; API examples show Refill At 5 with Fill Up 0 (API p37-41), so no such rule is enforced in `vlp_pool.py`. Do it at a quiet time and watch Cloud Tasks and OVDC capacity.

## 9. Recorded create flow (status: CREATED 2026-10-08)

Recorded live in tenant `livefire` with `vlp_record.py create_pool` (sanitized to `recordings/create_pool.py`; raw stays in gitignored `recordings/raw/`). Unlike the original plan this was a real write. Order of events:

1. Login (collapsed to `vlp_ui.login`), button `Cloud Management`, link `Deployment Pools`.
2. WRITE-GATE: button `Create New` (opens the form, no state change itself).
3. Textbox `Name *` = `VCF522-Upgrade-VCF9.1-REV1`. Description NOT typed.
4. Textbox `Primary Lab Template Search` = `VCF522-Upgrade-VCF9.1-REV1`; clicked result button `VCF522-Upgrade-VCF9.1-REV1 - [lvn3-vcd2-eduprod-r-gc]`.
5. WRITE: button `Create Deployment Po...` (pool created in VLP).
6. Button `Add Lab Templates`; dialog `Add Lab Templates` > checkbox `Select All` checked; button `Add` (exact).
7. WRITE: button `Update Deployment Pool` (commits the added rows).
8. Browser closed. No Refill At / Fill Up / Prepops cell was edited, so all values are the defaults (intended 0).

Implied state: pool exists with the primary template entry plus every row the dialog listed. Which rows (and whether exactly the 8 OVDCs) is NOT in the recording: verify with `docs/dry-run.ui.checklist.md` section 11. Enabled state and any Description are unconfirmed (none typed).

`flows/create_pool.py` now uses the recorded selectors and refuses to create when the name is already in the pool list (only the gated edit-templates step is offered). To re-record, use `vlp_record.py` and `sanitize_recording.py create_pool`, then update the flow.

## 10. Unverified items

- Description field label (not recorded; none typed); Explicitly Ready Prepops field.
- Pool-list search box; opening an existing pool's Edit Lab Templates (row menu path); Refill At / Fill Up / Prepops cell selectors.
- Exact rows added by `Select All` and the resulting Enabled state.
- Whether a name collision, empty Description or a missing Enabled field is rejected (empty Description was accepted).
- `Cloud Tasks`, `Cloud Shadows`, `Cloud oVDCs` menu paths (AG pages cited; not recorded).

## 11. Create vs update split; Edit VMs / initial console

Create = Name + primary template + `Create Deployment Pool` (AG p100), done 2026-10-08 (`flows/create_pool.py`; it refuses duplicates and only notes that edits live in `edit_pool.py`). Everything after is an edit of the existing pool, driven by the `update:` section of the pool YAML and `flows/edit_pool.py`:

| Step | `--step` | What | Gate |
|---|---|---|---|
| ensure pool exists | (always, read-only) | open Deployment Pools, find the name; abort if absent | none |
| edit_templates | `templates` | Edit Lab Templates: rows and Refill At / Fill Up / Prepops (0 = untouched), AG p101-102 | typed `yes` at `Update Deployment Pool` |
| edit_vms | `vms` | Edit VMs: Initial Console VM = `update.initialConsoleVm` (`console`) | typed `yes` before toggles + save |

Run: `python3 ~/.claude/skills/vlp-admin/scripts/flows/edit_pool.py [--step templates|vms] [--browse] [--execute]`. Default prints the plan only (no browser); `--browse` logs in and reads current flags; writes need `--execute` plus a typed `yes` each.

### Edit VMs / Initial Console (what the docs say)

- STATUS: DONE (manual UI, 2026-10-08, user-reported; not recorded). Initial Console set on `console` in pool VCF522-Upgrade-VCF9.1-REV1. Still to verify: no other VM has Initial Console, and the power-on warning state (section 11 checklist). Edit VMs selectors in `flows/edit_pool.py` remain UNVERIFIED because this step was not recorded.

- Where: `Cloud Management > Deployment Pools`, row three dots > `Edit VMs` (AG p103, p104); after create also the `Edit Vms` item in the left pane (AG p100). Opens "VM Metadata"; click `>` on a VM to edit its metadata (AG p103).
- Per-VM fields: Visible, Power On VM When Lab Starts, Allow / Automatic Console Resize, Username, Password, Notes (AG p103-104). Pool-level: Use Individual VM Power On Settings (AG p103).
- Initial Console: "If activated, a lab associated with the deployment pool uses the virtual machine as its initial console" (AG p103), i.e. the VM whose console the student sees first. API: `initial` flag per VM in `manageVms` (API p34-35 Add VM; `deploymentPoolVms[].initial` in pool detail, API p66, p73-74).
- VM list: derived from the pool's templates; all templates in a pool have identical structure and VM names (AG p100; API p33). So `console` must be a VM name in the template `VCF522-Upgrade-VCF9.1-REV1`. `Remove Obsolete VMs` exists for VMs no longer in the templates (AG p105).
- Labs: a lab's VM Configuration defaults to the pool's initial console (`Use from Deployment Pool`); `Use Custom Settings` overrides it per lab (AG p111). A lab whose pool/lab has no initial console shows the warning "This lab has no initial console chosen" (API p98). If the initial console VM is not set to power on while other VMs are, a warning shows in the Lab list (AG p103, p112).
- Constraints: the guide does not state a one-per-pool rule or whether other VMs are auto-cleared; the tooling enforces a single VM (`vlp_pool.py` rejects lists) and the flow clears other flags. UNVERIFIED: effect on already-deployed prepops/entitlements (no docs; at Prepops 0 none exist for this pool yet), so verify in section 11 of the dry-run checklist.
- Undo: reopen Edit VMs, clear Initial Console on `console` (or set it on another VM) and save (AG p103); no destructive state is involved. API equivalent: `manageVms` with `initial: off` (API p34-35).
- Selectors for Edit VMs are UNVERIFIED until `recordings/edit_pool_vms` is sanitized and reconciled into `flows/edit_pool.py` (each marked UNVERIFIED in the code).
- Verify after: `docs/dry-run.ui.checklist.md` section 11 (Initial Console = `console` only).
