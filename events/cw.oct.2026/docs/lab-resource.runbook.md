# Lab resource runbook - VCF91VKS_FastTrack_PDF (tenant `livefire`)

Citations: "AG p#" = `<project-root>/reference/vmware-lab-platform.pdf`. Runbook step 5 in `~/.claude/skills/vlp-admin/SKILL.md`.
Definition: `classes/resource_yaml/resource.clearwater.vcf91vks-pdf.yaml` (validate: `python3 ~/.claude/skills/vlp-admin/scripts/vlp_resource.py <file>`).
Flow: `~/.claude/skills/vlp-admin/scripts/flows/lab_resource.py` (dry-run default). Source recording: `recordings/lab_resource.py`.

Status: VERIFIED 2026-10-08 (user-reported in the admin UI, not recorded): the resource `VCF91VKS_FastTrack_PDF` exists in tenant `livefire` and points to the stored file below. Recorded in the definition as `verified: true`, `verifiedOn: 2026-10-08`, `storageUrl`. Still open in `docs/dry-run.ui.checklist.md` section 13: exactly one row (no duplicate), file size, not yet attached to a lab (step 7, `docs/lab.runbook.md`).

Storage URL (user-reported): `https://labplatform.broadcom.com/content/api/storage/file/livefire/labResources/b8e9a393-fdd8-4425-96ca-fb286fb5c93a---VCF91VKS_FastTrack.pdf`
Handling note: the URL contains a random-looking UUID prefix (`b8e9a393-...---`). It is not a secret, but treat it as an internal identifier: keep it in the project definition and do not publish it to students beyond the lab. Students reach the file through the running lab's `More Options > Resources` menu (AG p178), not through this URL.

## Steps (AG p177-178; p49 gives the menu as `Lab Management > Lab Resources`)

1. `Lab Management > Lab Resources > Create New`.
2. Name `VCF91VKS_FastTrack_PDF`.
3. `Upload a file` > choose `lab.manuals/VCF91VKS_FastTrack.pdf` (recording used the bare name `VCF91VKS_FastTrack.pdf`, file input `#path_file`).
4. `Create Lab Resource`. The PDF is then listed on the Lab Resources page (AG p178).
5. Attaching to a lab is runbook step 7, not part of this flow: Labs > the lab > Update Content > Resources > select the resource > Done > Update Lab (AG p178).

Flow usage (from the project root): `python3 ~/.claude/skills/vlp-admin/scripts/flows/lab_resource.py [--browse] [--execute]`. Without flags it prints the plan and checks the file exists. With `--browse`/`--execute` it logs in, searches the list, and refuses to create if the name is listed. `--execute` asks for a typed `yes` twice (stage the file, then Create Lab Resource).

## Behavior when the lab has a manual

AG p177-178: using a PDF AS the manual requires `Hide Instructions panel when no manual` OFF and the lab's Manual option left empty. Our lab uses a Content Engine manual (`VCF91VKS_FastTrack`), so the PDF is only an extra resource: with several resources selected, only the first selected PDF is shown as the manual when no manual is set; otherwise the PDFs are available for download in the running lab under `More Options > Resources`. So with a manual present, expect the PDF to appear as a download, not as the manual. Note `Hide Instructions panel when no manual` (checklist 1.1) hides the whole instruction panel including the Resources menu (AG p65) when the lab has no manual; with a manual it is irrelevant. Confirm in a test run (UNVERIFIED).

## Undo / delete options

AG p177-178 documents NO delete or edit for a lab resource. Documented only:
- Detach: on the lab, Update Content > Resources, deselect the resource > Done > Update Lab (reverses step 5 of the steps above; the resource stays in the list).
- Delete/replace of the resource itself: UNDOCUMENTED in pp177-178. If the Lab Resources list offers a row action, test with the user first; a resource attached to a lab must be detached before any delete. A wrong PDF is safest handled by creating a new resource with a new name and re-pointing the lab.

## Risks

- Duplicate resource if the flow is re-run under a different name or the list read (UNVERIFIED markup) misses the existing row; the flow reads page text for the exact name.
- The recording shows no success message; creation is assumed from the click.
- Wrong file: the upload cannot be changed after create (not documented).
