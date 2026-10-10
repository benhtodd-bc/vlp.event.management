# VLP admin UI dry-run checklist (read-only) - VCF 9.1 VKS Fast Track

Tenant: `livefire`. Login: https://admin.labplatform.broadcom.com/login/ (organization/tenant field = `livefire`).
Purpose: confirm what already exists before any write. Do NOT click Create, Update, Save, Publish, Sync, Drain, Refill, Set to fill up, Delete or Upload anywhere. Open pages, read, filter and search only. Do not paste credentials anywhere.

References: "AG p#" = page of `<project-root>/reference/vmware-lab-platform.pdf` (PDF page number equals printed page number). Runbook = "End-to-end class build runbook" in `~/.claude/skills/vlp-admin/SKILL.md` (steps 1-10). Prereq values come from `classes/class_yaml/class.clearwater.vks-fasttrack.yaml` (`labPrereqs`).

Menu-path notation: `A > B` is the left navigation panel. The admin guide uses the `›` form. Some entries differ from what the guide says; those are flagged "UNVERIFIED" or "GUIDE DIFFERS" and summarized at the end.

---

## 1. Tenant settings (runbook step 8)

Menu: `Portal Settings > Configuration` (AG p65, p136). Use the page search box to find each setting by name. Settings are only viewed, not changed. If the page is not visible, you may lack the Portal Settings permission; note that.

| # | Setting (exact name) | Where / AG | Look for | Result / value found |
|---|---|---|---|---|
| 1.1 | Hide Instructions panel when no manual | Configuration > Interface section (AG p65, p116, p152) | On/Off. Runbook wants ON for a manual-driven lab. NOTE: AG p111 and p177 say to turn it OFF only when using a PDF as the manual; our plan is a Content Engine manual, so ON is expected. | |
| 1.2 | Enable SaaS Consoles | Configuration > Console Interface (AG p90) | On/Off. AG p90: enabling it requires contacting VLP support. Only needed if the lab uses SaaS consoles (`saasConsoles: []`, none identified), so Off is acceptable. | |
| 1.3 | Show preferred cloud location dropdown in the classes wizard | Configuration (AG p150, p193) | On/Off. If Off the Preferred cloud location field is hidden in the class wizard. If On, list the cloud locations offered in the dropdown (see also 9). YAML has `preferredCloudLocation: ""`. | |
| 1.4 | Make time allotted for entitlement equal to class duration and hide remaining lab time | Configuration (AG p150) | On/Off. If On, entitlement length = class length and remaining/extend-time buttons are hidden. | |
| 1.5 | Enable Tracking Code for Classes | Configuration (AG p148, p192) | On/Off. If On, the class wizard shows a Tracking Code field. AG: the code cannot be changed once the class starts. Record whether an event tracking code is mandated (value, if any, to be supplied by you). | |

Feeds runbook step 8 (flip: 1.1 already ON means step 8 is done). 1.3/1.5 decide whether the preferred-location and tracking-code fields exist in the class CSV/UI.

---

## 2. Template `VCF522-Upgrade-VCF9.1-REV1` in catalog `CM3-EDUPROD-DGC` (runbook step 6 prerequisite)

Pool template changed: the pool is now built from `VCF522-Upgrade-VCF9.1-REV1`. `VCF91VKS-FastTrack-v5` is still copying (plannedTemplate, pending copy); record its status as a future item only. See `docs/deployment-pool.runbook.md` section 3.

Menu (GUIDE DIFFERS / partly UNVERIFIED): AG documents the template list as `Lab Management > Lab Builder` (Lab Templates page with cloud drop-down, AG p59, p75) and as `Lab Management > Lab Templates` (AG p119). Your note says "Cloud Management templates"; the guide has no `Cloud Management > Cloud Templates` page. Try, in order: `Lab Management > Lab Templates`, `Lab Management > Lab Builder`, then `Cloud Management > Clouds` (Cloud Catalogs tab, AG p212).

Look for (search the exact name `VCF522-Upgrade-VCF9.1-REV1`; also "VCF522" for other REVs; separately note whether `VCF91VKS-FastTrack-v5` has finished copying):

| Item | Result / value found |
|---|---|
| Template exists (exact name `VCF522-Upgrade-VCF9.1-REV1`)? | |
| Present in catalog `CM3-EDUPROD-DGC`? | |
| `VCF91VKS-FastTrack-v5` copy finished? (future; not blocking) | |
| Cloud (cloud org) and cloud catalog it lives in | |
| Other REVs present (REV2, ...)? | |
| Prepop / Refill At / Fill Up / Prepops Available (Lab Templates or Deployment Pool Edit Lab Templates form, AG p102, p119) | |
| Shadow status: `Cloud Management > Cloud Shadows` (AG p217): availability and replica status per cloud org for this template (read only; do NOT click the blue replica oval or Refresh Shadow Information) | |

Per-OVDC table (the 8 Clearwater OVDCs from `CLAUDE.md`). Source for the OVDC list: Cloud Org VDC info column on the Edit Lab Templates form (AG p102) and the Cloud Shadows page (AG p217).

| OVDC | Template present (Y/N) | Prepop count | Shadow/replica ready (Y/N) |
|---|---|---|---|
| lvn3-vcd2-eduprod-r-ovdc8 | | | |
| lvn3-vcd2-eduprod-r-ovdc7 | | | |
| lvn9-vcd1-eduprod-r-ovdc3 | | | |
| lvn9-vcd1-eduprod-r-ovdc12 | | | |
| lvn9-vcd2-eduprod-r-ovdc6 | | | |
| lvn9-vcd2-eduprod-r-ovdc7 | | | |
| lvn9-vcd2-eduprod-r-ovdc8 | | | |
| lvn9-vcd2-eduprod-r-ovdc13 | | | |

---

## 3. Deployment pool containing the template (runbook step 6)

Menu: `Cloud Management > Deployment Pools` (AG p61, p100-102). Open the list, then select a pool and view its Edit Lab Templates tab (view only; do not press Update).

| Item | Result / value found |
|---|---|
| Pool name(s) containing `VCF522-Upgrade-VCF9.1-REV1` (planned pool name `VCF522-Upgrade-VCF9.1-REV1`; planned Refill At/Fill Up/Prepops = 0) (use list filter/search) | |
| Pool enabled/active (a deactivated pool cannot deploy prepops, AG p102) | |
| Refill At (aggregate and per OVDC) | |
| Fill Up (aggregate and per OVDC) | |
| Prepops Available / "Pools Using" count | |
| Other templates in the same pool (all templates in a pool must match structure, AG p100-101) | |
| Explicitly Ready Prepops flag (only visible if the tenant setting under Deployments is on, AG p100) | |

Note: if the tenant uses "Enable Optimized Deployment Pool Usage" with one cloud, the pool is hidden and the lab uses a Cloud Lab Template field instead (AG p106). Record if you see that. Flip: pool found means runbook step 6 is done (otherwise follow `docs/deployment-pool.runbook.md`); its name goes into `labPrereqs.deploymentPool`.

---

## 4. Existing labs matching "FastTrack" (runbook step 7; answers "does the lab exist")

Menu: `Lab Management > Labs` (AG p106, p61; the guide also writes `Labs > Labs` on p177-178). Use the filter icon / search box with "FastTrack", then also "VKS" and "9.1". For each match, open the row's `Update` / `Update Content` / Lab Configuration view (read only; do not press Update Lab).

| Field | Lab #1 | Lab #2 (if any) |
|---|---|---|
| Name | | |
| Unique Lab ID / SKU (this is what the class YAML `labs[0].sku` needs) | | |
| Deployment pool attached | | |
| Manual attached | | |
| Resources attached (expect `VCF91VKS_FastTrack_PDF`) | | |
| SaaS consoles attached | | |
| Time allotted / Valid period | | |
| Enabled status | | |

Result: lab exists? (Y/N) ______. Flip: Y with pool + manual + resource attached and enabled means runbook steps 2-7 are done and only the class (10) remains; N means steps 2-7 are all outstanding.

---

## 5. Manual project `VCF91VKS_FastTrack` (runbook steps 2-4)

Menu: `Content > Content Engine` (AG p177, p281-282); it opens the Lab Manual Projects page. Also cross-check `Content > Manuals` list in the admin UI (AG p177; UNVERIFIED exact label, guide says "the Manuals page").

| Item | Result / value found |
|---|---|
| Project `VCF91VKS_FastTrack` exists? | |
| Instances listed (View Project): imported / draft / published, per language | |
| Published instance present? (an admin can only attach published manuals to a lab, AG p281) | |
| Shown in the admin Manuals list (sync done)? | |

Flip: exists + published means steps 2-4 done. Imported only means step 4 (promote and publish) remains. Absent means steps 2-4 outstanding (zip: `lab.manuals/VKSFT91_vSphere Kubernetes Service_ Fast Track [v9.1].zip`).

---

## 6. Lab resource `VCF91VKS_FastTrack_PDF` (runbook step 5)

Menu: `Lab Management > Lab Resources` (AG p49 writes `Lab Management > Lab Resources`; AG p177-178 writes `Labs > Lab Resources`; try both).

| Item | Result / value found |
|---|---|
| Resource `VCF91VKS_FastTrack_PDF` exists? | |
| Type/file (expect `VCF91VKS_FastTrack.pdf`) | |
| Other FastTrack resources present | |

Flip: exists means step 5 done.

---

## 7. Instructor `dhiraj.sharma@broadcom.com` (needed before step 10)

Menu: `Users & Groups > User Accounts` (AG p129); search the email. Roles: open the account's `Update > User Access` (AG p128-129) or `Users & Groups > Roles & Permissions` (AG p129) to see the role.

| Item | Result / value found |
|---|---|
| Account exists in `livefire`? | |
| Role includes Instructor? | |
| Account enabled/verified | |

Menu: `Class Management > Instructor-Lab Map` (AG p191; the guide writes `Classes › Instructor-Lab Map`, try both). Look at the InstructorLabMapping list only; do not press Create.

| Item | Result / value found |
|---|---|
| Entries for dhiraj.sharma@broadcom.com (list labs) | |
| Any entry for the FastTrack lab? (AG p191: mapping restricts the instructor to the listed labs) | |

Flip: account missing means user create (CSV) is needed before the class; role missing means a role change; no mapping for the new lab means a mapping step is needed after the lab is created (not in the current runbook).

---

## 8. Class SKU `vcf-9.1-vks-fast-track` and naming patterns (runbook step 10)

Menu: `Class Management > Classes` (AG p191; list page). Use search/filter.

| Search | Result / value found |
|---|---|
| `vcf-9.1-vks-fast-track` (SKU in use? Y/N) | |
| `VCF 9.1 VKS Fast Track` (name) | |
| "FastTrack" / "Fast Track" / "VKS" | |
| Classes already using the lab found in section 4 (names, SKUs, dates, seats) | |
| Naming pattern observed (SKU casing, separators, event/location suffix) | |

Flip: SKU in use means a different `classSku` must be chosen before generation.

---

## 9. Cloud capacity (read only; cross-check of preflight check g)

Menu: `Cloud Management > Cloud oVDCs` (AG p214; label is written "Cloud oVDCs" in the guide). Open each of the 8 OVDCs from section 2 (view only; do not toggle). Per AG p214-215 the effective state needs Enabled, and for assignment also Assignment and Tenant Assignment, and for deployment Deployment and Tenant Deployment, all True; Maintenance Mode/Tenant Maintenance Mode should be False. Use `Manage Columns` (lower-left) to show these columns.

| OVDC | Enabled | Deployment | Assignment | Tenant Deployment | Tenant Assignment | Maintenance (both) | CPU/Mem/Storage used vs threshold |
|---|---|---|---|---|---|---|---|
| lvn3-vcd2-eduprod-r-ovdc8 | | | | | | | |
| lvn3-vcd2-eduprod-r-ovdc7 | | | | | | | |
| lvn9-vcd1-eduprod-r-ovdc3 | | | | | | | |
| lvn9-vcd1-eduprod-r-ovdc12 | | | | | | | |
| lvn9-vcd2-eduprod-r-ovdc6 | | | | | | | |
| lvn9-vcd2-eduprod-r-ovdc7 | | | | | | | |
| lvn9-vcd2-eduprod-r-ovdc8 | | | | | | | |
| lvn9-vcd2-eduprod-r-ovdc13 | | | | | | | |

Also: `Cloud Management > Clouds` (AG p61, p72, p212): which cloud org each OVDC belongs to, and whether at least one Cloud Catalog is activated (AG p212). Note the cloud locations that would appear in the preferred-location dropdown (1.3).

---

## 10. Values you must supply to unblock generation

These are placeholders in `classes/class_yaml/class.clearwater.vks-fasttrack.yaml` and cannot be discovered from VLP.

| Value | YAML field | Your answer |
|---|---|---|
| Lab SKU (from section 4, or the SKU you want the new lab to have) | `labs[0].sku` | |
| Class start date and time (America/New_York, IANA only) | `schedule.startDate`, `startTime` | |
| Class end date and time (America/New_York) | `schedule.endDate`, `endTime` | |
| Seats | `numberOfSeats` | |
| Owner email(s) | `owners` | |
| Pre-provision period, format `d.hh:mm:ss` (e.g. `1.00:00:00`) | `provisioning.preProvisionPeriod` | |
| Tracking code, if 1.5 is On and one is required | not in YAML yet | |
| Preferred cloud location, if 1.3 is On | `preferredCloudLocation` | |
| Deployment pool name (from section 3) | `labPrereqs.deploymentPool` | `VCF522-Upgrade-VCF9.1-REV1` (created 2026-10-08) |
| Lab name, short/long description, catalog, enabled, time allotted, valid period (section 14; `docs/lab.runbook.md` section 3) | `classes/lab_yaml/lab.clearwater.vcf91vks.yaml` | |
| OVDC list for `.env` `OVDCS` (confirm the 8 are right after section 9) | `.env` (do not paste) | |

Per CLAUDE.md, give times with explicit zone; the other zones (Pacific, Sofia) are derived afterwards.

---

## 11. Post-create verification: pool VCF522-Upgrade-VCF9.1-REV1 (created 2026-10-08; read-only)

- [ ] Pool exists: `Cloud Management > Deployment Pools` lists `VCF522-Upgrade-VCF9.1-REV1` exactly once (no duplicate).
- [ ] Open Edit Lab Templates (view only, do not click Update): each of the 8 OVDC rows is present (Select All was used, so check there are no extra or missing rows):
  - [ ] lvn3-vcd2-eduprod-r-ovdc8
  - [ ] lvn3-vcd2-eduprod-r-ovdc7
  - [ ] lvn9-vcd1-eduprod-r-ovdc3
  - [ ] lvn9-vcd1-eduprod-r-ovdc12
  - [ ] lvn9-vcd2-eduprod-r-ovdc6
  - [ ] lvn9-vcd2-eduprod-r-ovdc7
  - [ ] lvn9-vcd2-eduprod-r-ovdc8
  - [ ] lvn9-vcd2-eduprod-r-ovdc13
- [ ] Extra rows (other OVDCs/catalogs) present? Note them: ______
- [ ] Refill At / Fill Up / Prepops are 0 on every row; Available 0, Provisioning 0, Error Count 0.
- [ ] Enabled state (per template row / pool): ______ (expected enabled; record in the pool YAML).
- [ ] Description shown: ______ (expected empty).
- [ ] Labs using the pool (More details > Labs): none.
- [ ] Cloud Tasks: nothing queued/failed for this pool.
- [ ] Edit VMs (view only, do not click Update; row three dots > Edit VMs, AG p103): VM list matches the template's VMs (includes a VM named `console`).
- [x] Initial Console is ON for the VM named `console` (user-reported done 2026-10-08, manual UI, not recorded). STILL TO VERIFY: OFF for every other VM (exactly one). Other flags noted: Visible ______ / Power On VM When Lab Starts ______.
- [ ] If the initial console VM is not set to power on while others are, a warning shows in the Lab list (AG p103); note: ______ (STILL TO VERIFY)

## Paste-back summary (fill in and return)

| # | Item | Found (Y/N or value) | Notes |
|---|---|---|---|
| 1.1 | Hide Instructions panel when no manual | | |
| 1.2 | Enable SaaS Consoles | | |
| 1.3 | Show preferred cloud location dropdown (and locations offered) | | |
| 1.4 | Time allotted = class duration | | |
| 1.5 | Tracking code enabled / required value | | |
| 2 | Template `VCF522-Upgrade-VCF9.1-REV1` exists in `CM3-EDUPROD-DGC` (FastTrack-v5 copy status noted separately); catalog; OVDCs with template; shadow ready | | |
| 3 | Deployment pool name; Refill At / Fill Up; other templates | | |
| 4 | FastTrack lab exists; SKU; pool; manual; resources; consoles; enabled | | |
| 5 | Manual project `VCF91VKS_FastTrack`: exists; instances; published | | |
| 6 | Resource `VCF91VKS_FastTrack_PDF` exists | | |
| 7a | dhiraj.sharma@broadcom.com exists with Instructor role | | |
| 7b | Instructor-Lab Map entries | | |
| 8 | SKU `vcf-9.1-vks-fast-track` in use; naming pattern | | |
| 9 | OVDCs enabled for assignment and deployment (list any that are not) | | |
| 10 | Lab SKU / dates+times (ET) / seats / owners / preProvisionPeriod | | |
| - | Menu paths that did not match this checklist (give the real path) | | |

## Which findings flip which runbook steps

| Finding | Runbook effect |
|---|---|
| 1.1 already ON | Step 8 done |
| 5 published manual exists | Steps 2, 3, 4 done |
| 5 imported only | Steps 2, 3 done; step 4 (promote + publish) needed |
| 5 absent | Steps 2-4 all needed |
| 6 resource exists | Step 5 done |
| 2 template `VCF522-Upgrade-VCF9.1-REV1` missing or not in the 8 OVDCs / shadows not ready | Blocker before step 6; template must be published/synced by the template owner, not part of this runbook |
| 3 pool found containing the template | Step 6 done; record pool name in YAML |
| 3 no pool | Step 6 needed (create pool, then set Refill At / Fill Up) |
| 4 lab exists, enabled, with pool + manual + resource | Steps 2-7 effectively done; lab SKU goes into YAML; go to step 9 then 10 |
| 4 lab exists but missing manual/resource/pool | Only the missing attachment (step 7 update) needed |
| 4 no lab | Step 7 needed after 2-6 |
| 7a account missing or no Instructor role | User create/role fix needed before step 10 |
| 7b no mapping | Instructor-Lab Map entry needed after lab exists (not in current runbook) |
| 8 SKU in use | Choose a different `classSku` before step 10 |
| 9 any OVDC not enabled for assignment/deployment | Remove it from `OVDCS` or ask VLP support (only staff change the global flags, AG p214) before relying on capacity |
| 10 values supplied | Unblocks generation of the class CSV (dry run) and step 10 |

## Menu paths not verified against the PDF

- Template list "Cloud Management templates": no such page in the guide; use `Lab Management > Lab Templates` / `Lab Management > Lab Builder` (AG p59, p75, p119).
- Lab Resources: guide shows both `Lab Management > Lab Resources` (p49) and `Labs > Lab Resources` (p177-178).
- Manuals admin list: guide mentions a "Manuals page" without a path (p177).
- Instructor-Lab Map: guide writes `Classes > Instructor-Lab Map` (p191), whereas the class menu is `Class Management > Classes`.
- Where to view the tenant name/switcher and the role of an account: no explicit menu in the guide beyond `Users & Groups` (p128-129).
- Exact section names for 1.2-1.5 inside Portal Settings: 1.1 is under Interface (p65) and 1.2 under Console Interface (p90); 1.3-1.5 are listed without a section name, so use the search box.
- The guide is for the VMware-branded product (older 2024 text); the Broadcom admin UI may have renamed or moved items.

---

## 12. Post-create verification: manual project VCF91VKS_FastTrack (created, uploaded, published 2026-10-08; read-only)

Menu: `Content > Manual Projects` (recorded). Do not click Publish, Delete, Upload or Promote.

- [ ] Project exists once: the list shows `VCF91VKS_FastTrack` exactly once (no duplicate project).
- [ ] Open the project (View Project): exactly one instance for the uploaded zip; no leftover `imported` or `draft` instance beside the published one. Instance state: `published`. Recorded: ______
- [ ] Language of the instance: ______ (Edit details shows title/language, AG p283; the recording never set a language, so it is whatever the zip/default gave). A user's profile language selects the version at lab start (AG p281); a language with no published version is not served.
- [ ] Title/content spot check: Preview (view only) opens and shows the expected Fast Track manual (UNVERIFIED: Preview not recorded).
- [ ] Linked to no lab yet: `Lab Management > Labs` shows no lab using this manual (expected: none; the lab is runbook step 7). Also present in the admin Manuals list (sync): ______
- [ ] Created/updated timestamp is 10/8/26 around 2:07 PM (as shown in the list row).

---

## 13. Post-create verification: lab resource VCF91VKS_FastTrack_PDF (created 2026-10-08 per recording; read-only)

Menu: `Lab Management > Lab Resources` (recorded). Do not click Create Lab Resource, Delete or Upload.

- [x] Resource exists once: the list shows `VCF91VKS_FastTrack_PDF` exactly once (user-reported 2026-10-08: it exists in livefire; not recorded). STILL TO CONFIRM: exactly once (no duplicate). Found: exists
- [x] File name/size: the resource points to storage file `VCF91VKS_FastTrack.pdf` (user-reported 2026-10-08; the storage URL ends `---VCF91VKS_FastTrack.pdf`, recorded in `storageUrl` of `classes/resource_yaml/resource.clearwater.vcf91vks-pdf.yaml`). Size not confirmed: expect about 1.4 MB (1,404,319 bytes locally, `lab.manuals/VCF91VKS_FastTrack.pdf`). Found: ______ (UNVERIFIED: where the UI shows file size)
- [ ] Not attached to any lab yet: `Lab Management > Labs` shows no lab using this resource (expected: none; attaching is runbook step 7).
- [ ] Created timestamp is 10/8/26 (as shown in the list row, if shown).

Note on `storageUrl`: it contains a random-looking UUID prefix (`b8e9a393-...---`). It is an identifier, not a secret, but treat it as an internal identifier: keep it in the project, do not publish it to students beyond the lab (students get the file only through the lab's Resources menu).

---

## 14. Pre/post-create: lab for class 'VCF 9.1 VKS Fast Track' (runbook step 7; read-only until the user records the create)

Menu: `Lab Management > Labs` (AG p106). Procedure: `docs/lab.runbook.md`. Definition: `classes/lab_yaml/lab.clearwater.vcf91vks.yaml`. Do not click Create New, Create Lab, Update Lab, Delete or the Enabled toggle during this read-only pass.

Before create:
- [ ] Lab list search for the chosen SKU (and "FastTrack", "VKS", "Clearwater") shows no existing lab for this event; if one is found, record SKU/name/pool/manual/resources: ______
- [ ] Deployment pool `VCF522-Upgrade-VCF9.1-REV1` is in the pool list (section 3/11) and has initial console `console`.
- [ ] Manual project `VCF91VKS_FastTrack` is published (section 12); it appears in the lab form's Manual list view (UNVERIFIED label).
- [ ] Resource `VCF91VKS_FastTrack_PDF` appears in Update Content > Resources list view (section 13).
- [ ] Catalog to use exists (`Lab Management > Lab Catalogs`, AG p124-125): name ______ (decision; the sibling export uses `PS Airlift-ATE`). Does it have a group set (a catalog with no group is invisible, AG p125)?
- [ ] Existing-lab naming seen in the UI (SKU / Name / Valid Period / Time Allotted columns) agrees with the suggestions in `docs/lab.runbook.md` section 3: ______

After create (verify, read-only):
- [ ] Lab listed exactly once with the chosen SKU and Name; Unique Lab ID = SKU.
- [ ] Lab Configuration: Enabled ______ (expected: as decided), Publicly Visible ______ (expected off), Prepop Enabled ______ (derived from the pool; pool is 0/0/0 so none deploy).
- [ ] Update Content: Manual = `VCF91VKS_FastTrack`; Resources = `VCF91VKS_FastTrack_PDF`; SaaS consoles none; Short Description / Description as decided.
- [ ] VM Configuration: `Use from Deployment Pool` on; initial console shows `console` (no lab-list warning "This lab has no initial console chosen", API p98).
- [ ] Lab list shows no warning/error for this lab ("Lab does not have a manual" must be absent).
- [ ] Deployment pool More details > Labs lists the new lab.
- [ ] Quick launch URL generated (AG p107): ______ (do not publish; admin test only).
- [ ] Time Allotted / Valid Period shown as decided: ______ / ______.

---

## 15. Post-shadow verification: template VCF522-Upgrade-VCF9.1-REV1 shadowed to the 8 Clearwater OVDCs (requested 2026-10-08 per recording; read-only)

Menu: `Cloud Management > Cloud Shadows` (recorded link text `Cloud Shadow`; AG p217). Procedure: `docs/shadowing.runbook.md`. Definition: `classes/shadow_yaml/shadow.clearwater.vcf522-upgrade.yaml`. Do NOT click a replica value, `Ok`, or `Refresh Shadow Information` during this pass. Read-only helper: `flows/shadowing.py --browse`.

- [ ] Search `VCF522-Upgrade-VCF9.1-REV1`: one row per cloud org. Record the catalog text (row read `CM3-EDU-PROD-DGC`; pool says `CM3-EDUPROD-DGC`: which is right? ______) and the count column (was `1/7`, `1/7`, `1/8` before the clicks; now ______).
- [ ] Per OVDC, shadow completed (open each cloud row; ready/available, not in progress or failed). Cross-check with API `GET /api/admin/CloudShadow` if available (`shadows` has the OVDC, `deploying` does not):
  - [ ] lvn3-vcd2-eduprod-r-ovdc8: ______
  - [ ] lvn3-vcd2-eduprod-r-ovdc7: ______
  - [ ] lvn9-vcd1-eduprod-r-ovdc3: ______
  - [ ] lvn9-vcd1-eduprod-r-ovdc12: ______
  - [ ] lvn9-vcd2-eduprod-r-ovdc6: ______
  - [ ] lvn9-vcd2-eduprod-r-ovdc7: ______
  - [ ] lvn9-vcd2-eduprod-r-ovdc8: ______
  - [ ] lvn9-vcd2-eduprod-r-ovdc13: ______
- [ ] No extras: any other OVDC now showing a shadow of this template beyond the 8 (the `.first` clicks were ambiguous): ______
- [ ] Matches the pool rows: `Cloud Management > Deployment Pools` > the pool > Edit Lab Templates (view only) has one `VCF522-Upgrade-VCF9.1-REV1 - <ovdc>` row per OVDC above (section 11): same 8, no more, no fewer: ______
- [ ] Cloud Tasks shows no failed shadow/copy task: ______
- [ ] Cloud oVDCs capacity after the copies (section 9): ______ (template copies consume storage).
- [ ] `Preshadow Enabled` on the 8 OVDCs: ______ (informational).
- [ ] When all ticked: set `status: confirmed`, `confirmedOn`, `verified: true`, `verifiedOn` in the shadow YAML.
