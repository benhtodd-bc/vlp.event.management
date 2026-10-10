# Manual project runbook - VCF91VKS_FastTrack (tenant `livefire`)

Citations: "AG p#" = `<project-root>/reference/vmware-lab-platform.pdf`. Runbook steps 2-4 in `~/.claude/skills/vlp-admin/SKILL.md`.
Definition: `classes/manual_yaml/manual.clearwater.vcf91vks.yaml` (validate: `python3 ~/.claude/skills/vlp-admin/scripts/vlp_manual.py <file>`).
Flow: `~/.claude/skills/vlp-admin/scripts/flows/manual_project.py` (dry-run default). Source recording: `recordings/manual_project.py`.

Status: DONE 2026-10-08 (project created, zip uploaded, promoted to draft, published) via manual UI, recorded live.

## Steps (AG p281-283, p286, p290)

1. `Content > Manual Projects > Add New > Start a Manual Project`: Name `VCF91VKS_FastTrack` > Create (`--step create_project`).
2. Open the project > `Upload a Manual file` > `Select File` (`lab.manuals/VKSFT91_vSphere Kubernetes Service_ Fast Track [v9.1].zip`) > Done. Creates an `imported` instance (`--step upload_zip`).
3. Instance `Dropdown Actions` > `Promote to Draft` (`--step promote_draft`).
4. Draft `Dropdown Actions` > `Publish Draft` (`--step publish`). Every language version must be published separately (AG p290).
5. Verify with `docs/dry-run.ui.checklist.md` section 12. The lab (runbook step 7) then attaches the published manual.

Flow usage (from the project root): `python3 ~/.claude/skills/vlp-admin/scripts/flows/manual_project.py [--step X] [--browse] [--execute]`. Without flags it only prints the plan and checks the zip exists. The project already exists, so a re-run skips create/upload, reports instance states, and refuses to create a duplicate.

## Undo / unpublish

The admin guide (AG p281-290) documents NO unpublish. Published manuals cannot be edited (AG p286). Documented options only:
- Delete Draft (AG p283): removes a draft; not applicable once published.
- Delete Project (AG p282): deletes the project and ALL drafts, imported and published instances. Destructive; a lab that uses the manual would lose it. Not automated by this flow.
- To change content: add a new manual (upload a corrected zip) and publish it, then re-point the lab. Whether a second published instance in the same project is allowed or supersedes the first is UNDOCUMENTED; test with the user before relying on it.
- Export (AG p283, p290) saves a draft as a ZIP for re-upload.

## Risks

- Publish is not editable afterwards (AG p286); a wrong zip means a new upload or project delete.
- Duplicate project or duplicate instance if the flow is re-run against a differently named or half-created project; the existence check relies on UNVERIFIED list search/instance-state reads.
- Language is not set by the recording; a missing or wrong language means users with another profile language may get no manual (AG p281, p290).
- Recorded sanitizer left Upload Done and Promote to Draft ungated; this flow gates them. Selectors for Dropdown Actions use `.first` and may hit the wrong instance if several exist.
- Delete Project must never be run while a lab references the manual.
