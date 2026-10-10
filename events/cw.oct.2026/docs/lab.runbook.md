# Lab runbook - class 'VCF 9.1 VKS Fast Track' (tenant `livefire`)

Citations: "AG p#" = `<project-root>/reference/vmware-lab-platform.pdf` (PDF page = printed page). "API p#" = `VLP-Admin/vlp.admin/doc/vlp.rest.api.pdf` (PDF page; 299-page guide, Labs API on p93-105). Sibling export = `VLP-Admin/vlp.admin/manage_classs/export.of.existing.labs.as.sample.csv` (4 labs, column names and example values only). Runbook step 7 in `~/.claude/skills/vlp-admin/SKILL.md`.
Definition: `classes/lab_yaml/lab.clearwater.vcf91vks.yaml` (validate: `python3 ~/.claude/skills/vlp-admin/scripts/vlp_lab.py <file> [--tolerant]`).
Flow skeleton: `~/.claude/skills/vlp-admin/scripts/flows/lab.py` (dry-run default; every selector UNVERIFIED). Tests: `scripts/test_vlp_lab.py`. Checklist: `docs/dry-run.ui.checklist.md` section 14.

Status (2026-10-08): NOT STARTED. All prerequisites exist (pool, manual, resource); the lab does not exist yet (to be confirmed by the section 6 search). SKU, name, catalog (empty), time allotted (48 h) and valid period (48 h) were decided 2026-10-08; short description, description and enabled are still undecided (section 3). Nothing here has been recorded or executed.

## 1. What a lab is, and which entry point to use

A lab is metadata + ONE deployment pool + a manual (+ resources, SaaS consoles, catalogs). The class only references the lab SKU (AG p106; SKILL.md "lab-owned objects").

| Entry point | What it creates | Use? |
|---|---|---|
| `Lab Management > Labs > Create New` (AG p106; the quick-start p61 calls the button `Create Lab`) | the LAB (metadata, pool, manual, catalog) | YES - this runbook |
| `Lab Management > Lab Builder` (AG p76-82, p119) | lab TEMPLATES (VMs, drafts, publish). Not labs. Our template `VCF522-Upgrade-VCF9.1-REV1` already exists and is in the pool | NO |
| `Class Management > Classes > Create` then `Create New Lab` (AG p45, p192) | the same Create Lab form, launched from the class wizard; the lab then shows under "Recently created labs" | NO (class is step 10, after the lab exists) |
| API `POST /api/admin/labs` (API p100: required `tenant`, `sku` without spaces, `name`; PUT p104 to update) | the lab | NO (UI path; writes via `vlp_api.py` are blocked by `ReadOnlyViolation` by design) |

"Update Content" (AG p97, p178) is the Lab Content step of the same form (reachable later from the lab row: Labs > the lab > Update). "Manual" is a field on the first tab (AG p106); the Content Engine project is only attachable once published (AG p281).

## 2. Ordered steps (AG p106-113). WRITE = persists state in livefire

Pre-checks (read-only; section 6 first): the SKU/name are not already used; pool `VCF522-Upgrade-VCF9.1-REV1`, manual `VCF91VKS_FastTrack` (published) and resource `VCF91VKS_FastTrack_PDF` appear in their list views; the catalog exists and has a group (AG p125).

1. `Lab Management > Labs` (AG p106). READ.
2. Click `+Create New` (p61 calls it `Create Lab`). The Create Lab form opens on the Lab Details tab. (No write yet.)
3. Fill Lab Details (AG p106-107): Name; Unique Lab ID (= SKU); Short Description; Deployment Pool (`Add`, pick `VCF522-Upgrade-VCF9.1-REV1`); Valid Period; Time Allotted (hours); Manual (list view, `VCF91VKS_FastTrack`); Thumbnail (optional, skip); Catalog (list view, one or more).
4. Click `Create Lab`. WRITE #1 - the lab is created and a quick launch URL is generated (AG p107). From here the lab exists even if you stop; roll back per section 7.
5. Lab Configuration page (AG p107-110): General Settings Enabled / Publicly Visible / New Lab; End-User Interface End/Exit/Reset Allowed, Show Notes; Time Settings; Other Settings Prepop Enabled (derived from the pool, p109), Power Operation, Undeploy After, Concurrent Usage Limit. Accept defaults except where the table in section 3 says otherwise. Click `Next`. WRITE #2 (the guide says Next saves, p111).
6. Lab Content page (AG p110-111): Short Description / Description, Resources (list view: select `VCF91VKS_FastTrack_PDF`, then `Done`), leave Network Topology, Survey, Badges, Products, Tags, Authors, Related Labs empty unless decided. SaaS consoles: none. Click `Next`. WRITE #3.
7. VM Configuration tab (AG p111-112): leave `Use from Deployment Pool` ON (the lab then uses the pool's initial console, `console`). Do not use custom settings. Click `Update Lab` (AG p113; the quick-start p62 says `Create Lab` at this point). WRITE #4. The Labs list now shows the lab.
8. Verify per section 6 / checklist section 14. Do NOT enable it or attach it to a class until the checks pass (class = runbook step 10).

Guide discrepancies to expect: p61-62 quick start is a shorter 5-step form (SKU, name, pool, time allotted, manual) and calls the first action `Create Lab`; p106-113 is the full form. The UI is a newer Broadcom build than the 2024 guide; record real labels (section 8).

## 3. Field table (known vs to decide)

Legend: KNOWN = fixed by the project; DECIDE = user must choose (a `<placeholder>` in the YAML blocks strict mode and `--execute`); DECIDED = chosen by the user 2026-10-08; SUGGEST = my proposal, based on the sibling export.

| Field (UI label, AG page) | YAML key | State | Value / suggestion |
|---|---|---|---|
| Unique Lab ID / SKU (p106; unique in system, no spaces, API p100) | `sku` | DECIDED | `Clearwater-VCF91-VKS-FastTrack` (also set in class `labs[0].sku`) |
| Name (p106) | `name` | DECIDED | `VCF 9.1 VKS Fast Track` |
| Short Description (p106, p110) | `shortDescription` | DECIDE (placeholder, still blocks strict mode) | the loader treats it as optional and the API requires only tenant/sku/name (API p100), so an empty value would be valid; whether the Create Lab form requires it is UNVERIFIED (AG p106). Sibling labs leave it empty; SUGGEST one line, e.g. `vSphere Kubernetes Service Fast Track on VCF 9.1` |
| Description (p110) | `description` | DECIDE | sibling labs leave it empty; optional, may stay empty (set `""`) |
| Deployment Pool (p106) | `deploymentPool` | KNOWN | `VCF522-Upgrade-VCF9.1-REV1` (created 2026-10-08) |
| Initial console VM (pool Edit VMs p103; lab VM Configuration p111) | `initialConsoleVm` | KNOWN | `console` (set 2026-10-08, user-reported; still verify exactly one, checklist section 11) |
| VM Configuration (p111-112) | `vmConfiguration.useFromDeploymentPool` | KNOWN | `true` (Use from Deployment Pool) |
| Manual (p106; published Content Engine project) | `manual` | KNOWN | `VCF91VKS_FastTrack` (published 2026-10-08) |
| Resources (p110-111, p178) | `resources` | KNOWN | `VCF91VKS_FastTrack_PDF` (verified 2026-10-08). With a manual set, the PDF is a download under `More Options > Resources` (p178), not the manual |
| SaaS consoles (p97) | `saasConsoles` | KNOWN | none (`[]`); sibling `ATE-PSAirlift-iSIMSbHere` is the only export lab with consoles |
| Catalog (p107; catalogs p62, p124-125) | `catalogs` | DECIDED: empty (`[]`) | No catalog. A catalog with no group is invisible (p125); with no catalog the lab appears only under All Labs (p62). UNVERIFIED: that the Create Lab form accepts an empty Catalog field (AG p107 says 'select one or more'). The loader treats empty as valid (warning only). If the UI refuses, reuse `All Labs` or create a grouped catalog (separate WRITE) |
| Enabled (p107) | `enabled` | DECIDE | SUGGEST `true` only when the lab is verified and ready for the class; create it `false` first if the UI allows (UNVERIFIED), enable after verification. Sibling labs are `true` |
| Publicly Visible (p107) | `publicVisible` | SUGGEST | `false` (sibling labs false) |
| New Lab banner (p107) | `newItem` | SUGGEST | `false` |
| Time Allotted, hours (p106, p108) | `timeAllottedHours` | DECIDED: 2 days = 48 h | UI-facing `2d`/48 h. API `timelimit` is minutes: 2880. (Sibling: 1500 = 25 h, 2940 = 49 h) |
| Valid Period (p106, p108) | `validPeriodHours` | DECIDED: 2 days = 48 h | equal to Time Allotted (satisfies >=). API `validPeriod` is milliseconds: 172800000. UI input format UNVERIFIED (days/hours/minutes) |
| Runtime limits: End / Exit / Reset Allowed (p107) | `runtime.endAllowed/exitAllowed/resetAllowed` | SUGGEST | true / true / false (sibling VKS and Ops labs; Auto has reset true). Reset restores all VMs and loses work |
| Power Operation on exit (p109) | `runtime.powerOperation` | SUGGEST | `none` (sibling VKS/Auto/Ops); suspend/poweroff save compute but slow resume |
| Concurrent Usage Limit (p110) | `runtime.concurrentUsageLimit` | SUGGEST | `0` (no limit). DECIDE a cap if the 8 OVDCs cannot hold every seat at once (capacity: checklist section 9) |
| Undeploy After (p109) | `runtime.undeployAfter` | SUGGEST | `0` (no limit); field only shows if the Portal setting 'Show Undeploy After' is on |
| Prepop Enabled (p109) | `runtime.prepopEnabled` | KNOWN | derived from the pool; pool is Refill At/Fill Up/Prepops 0, so no prepops deploy and every start is a full deployment (slower first launch) |
| Minimum time / % steps for completion (p109) | not modelled | SUGGEST | leave 0 (sibling Ops uses 300 min minimum time) |
| Grading, callbacks, survey, badges, products, tags, authors, related labs, thumbnail, network topology (p108-111) | not modelled | SUGGEST | leave defaults/empty (sibling labs empty) |
| Class name | class YAML `className` | KNOWN | `VCF 9.1 VKS Fast Track` |

## 4. Validation the UI and API enforce

- Unique Lab ID: unique in the whole system (AG p106); no spaces (API p100). Name required (API p100). Everything else is optional in the API; the lab is saved with warnings.
- Warnings shown on the lab row / in the API `warnings` array (API p98, p102): `This lab has no initial console chosen.` (action `/lab/editVms/<id>`) and `Lab does not have a manual.` (action `/lab/editContent/<id>`). Our end state must show neither.
- AG p112: if the initial-console VM is not set to power on while other VMs are, the Lab List shows a warning. If all pool VMs power on, the vApp is started as a whole (cloud power order applies).
- Catalog groups: a catalog with no group is not visible (AG p125). A lab must be in a catalog to be listed there (AG p125).
- Only published manuals attach (AG p281, checklist section 12). A PDF-as-manual setup needs the Manual field empty and `Hide Instructions panel when no manual` off (AG p111, p177); we use a manual, so that setting is irrelevant (runbook step 8).
- Loader (`vlp_lab.py`) enforces: sku no spaces; name/pool/manual/enabled required; catalogs optional (empty = warning only, UI acceptance UNVERIFIED); hours positive and valid period >= time allotted; booleans/ints/powerOperation; status/createdOn/verified consistency; and warns (not errors) if pool/manual/resource/class SKU disagree with their sibling YAMLs.

## 5. Risks

- A lab can be created enabled by default (API example `enabled: true`, p102) before manual/pool/resources are attached; students could see a half-built lab if the catalog is public. Mitigate: catalog groups restricted, or disable until verified.
- Duplicate lab if the SKU search misses an existing row (list markup UNVERIFIED) or the flow is re-run; the SKU must be unique so VLP should reject a duplicate, but a different SKU would create a second lab.
- Pool is 0/0/0 prepops: the first start of each student lab is a full deployment (slower, capacity-heavy at class start). Not a lab-creation blocker; sizing is a pool decision (`docs/deployment-pool.runbook.md`).
- The four writes (Create Lab, Next, Next, Update Lab) are separate saves; stopping midway leaves a lab that exists with partial settings.
- Shared state: the Lab Configuration "Next" and the pool Labs list are tenant-wide; a wrong pool choice binds the lab's VM metadata to that pool's templates (AG p106).
- Time units: Time Allotted is hours in the UI but minutes in the API; Valid Period ms in the API. Double-check after creation (checklist 14).
- Quick launch URL (AG p107) works for admins to test; do not publish it. The resource `storageUrl` has a random-looking UUID prefix: treat as an identifier, not for students beyond the lab.
- Selectors in `flows/lab.py` are guesses; an untested `--execute` could click the wrong thing. Do not use `--execute` before a recording is reconciled.

## 6. Verification (read-only; also checklist section 14)

Before: Labs list search for the candidate SKU, then `FastTrack`, `VKS`, `Clearwater`; confirm no duplicate. Flow: `python3 ~/.claude/skills/vlp-admin/scripts/flows/lab.py --browse` (logs in, checks the SKU; with undecided SKU it exits 2).
After: lab listed exactly once; Unique Lab ID and Name as decided; open `Lab Configuration` (row vertical ellipsis, AG p116) to read Enabled / Publicly Visible / times; Update (Update Content) shows Manual `VCF91VKS_FastTrack` and Resources `VCF91VKS_FastTrack_PDF`; VM Configuration shows initial console `console` with `Use from Deployment Pool`; no warnings on the row; pool More details > Labs lists the lab (AG p105); quick launch URL present. API cross-check (read-only, existing preflight): `vlp_preflight.py` labs check, i.e. `GET /api/admin/labs?tenant=livefire&search=<sku>&with=manual,resources,catalogs,deploymentPool,labVms` (API p96-98) shows `deploymentPool.name`, `manual.name`, `resources`, `catalogs`, `labVms[].deploymentPoolVm.initial`, `warnings: []`, `errors: []`, `timelimit` (min) and `validPeriod` (ms). Then re-run preflight (runbook step 9). A test launch (admin quick launch) to confirm the manual and PDF resource show is a separate, user-approved action (it deploys a vApp).

## 7. Rollback / disable / undo

- Disable (preferred first move): Lab Configuration > Enabled off > Update Lab (AG p107). Reversible; keeps entitlements.
- Edit (fix a wrong value): Labs > the lab > Update / Update Content / VM Configuration > Update Lab (AG p97, p106-113). Detach a resource: Update Content > Resources, deselect > Done > Update Lab (AG p178). Change catalog membership: `Lab Management > Lab Catalogs` edit (AG p124-125).
- Delete: Labs list > row three ellipses > Delete (AG p113). Refused while an active prepop or an entitlement exists. If refused: ensure lab and prepops are active, set pool Prepops to 0 (already 0 here), enable and acknowledge all alerts, then retry. A lab already referenced by a class or with entitlements cannot be deleted; remove those first. The REST guide documents no DELETE for labs (GET/POST/PUT only, API p93-105). There is no "undo" button; deletion is permanent, so prefer disable.
- Wrong SKU after create: the Unique Lab ID is not documented as editable; the safe fix is a new lab with the right SKU, then disable/delete the wrong one.
- Deleting the lab does not delete the pool, manual project or resource (each is its own object; none of them has a documented delete here).

## 8. Recording instructions for the user (to turn the skeleton into a real flow)

Use the project recorder; WRITES are marked. Record twice if you like: first a read-only pass, then the create.
1. From the project root: `python3 ~/.claude/skills/vlp-admin/scripts/vlp_record.py lab` (logs in from `.env`, opens codegen on the admin UI; `--manual-login` if needed).
2. Click exactly, pausing 1-2 seconds per page so the recorder captures it:
   1. `Lab Management` (left menu) > `Labs`. READ
   2. Click the list search box, type the planned SKU, wait for the (empty) result. READ (this records the search selector the flow needs)
   3. Click `Create New` (or `Create Lab`, whichever the UI says). READ
   4. Click Name, type; click Unique Lab ID, type the SKU; click Short Description, type.
   5. Deployment Pool: click `Add`, pick `VCF522-Upgrade-VCF9.1-REV1`, confirm/Done.
   6. Valid Period and Time Allotted: click each field and enter the decided values (this records the input format).
   7. Manual: click the list-view icon, pick `VCF91VKS_FastTrack`, Done. Catalog: list view, pick the catalog, Done.
   8. Click `Create Lab`. WRITE #1
   9. Lab Configuration page: set Enabled / other toggles exactly as decided (click each toggle once, WRITE-ish state only saved by Next). Click `Next`. WRITE #2
   10. Lab Content page: click Resources list view, tick `VCF91VKS_FastTrack_PDF`, `Done`; leave the rest. Click `Next`. WRITE #3
   11. `Vm Configuration` tab: confirm `Use from Deployment Pool` is on (click only if it is off). Click `Update Lab`. WRITE #4
   12. Back on the Labs list: search the SKU; open the row three ellipses > `Lab Configuration`; read-only look; close without saving (do NOT click Update Lab, Delete or the Enabled toggle).
3. Stop codegen; run `python3 ~/.claude/skills/vlp-admin/scripts/sanitize_recording.py lab`; share `recordings/lab.py` (never `recordings/raw/`). Do not click Delete, Download or anything under Prepops. If the UI shows a different label than this runbook, write it down for the checklist's "Menu paths not verified against the PDF" list.
4. After the recording, reconcile selectors into `flows/lab.py` (remove the UNVERIFIED tags that were recorded, as was done for `flows/lab_resource.py`), set `status: created`, `createdOn`, `source: recorded` in the lab YAML, and tick checklist section 14.

## 9. Related

`docs/deployment-pool.runbook.md`, `docs/manual-project.runbook.md`, `docs/lab-resource.runbook.md`, class definition `classes/class_yaml/class.clearwater.vks-fasttrack.yaml` (`labs[0]`, `labDefinition`).
