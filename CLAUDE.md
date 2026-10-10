# Event Ops

Standing project for setting up and maintaining ALL of this user's VLP-based training events.
Each event is a self-contained folder under `events/<event-slug>/` — not a separate repo, and not
flat files at the project root. Check `events/<event-slug>/<event-slug>.md` first for that
event's facts (name/location, dates, timezones, OVDC capacity list, EPC resources).

## Time zones

- Rule: always state times with an explicit TZ. Look up the event TZ, user TZ, and any
  teammate TZs in the per-event `.md` file, and convert scheduling messages to all of them.

## VLP workflow
Handled via the `vlp-admin` skill (global: `~/.claude/skills/vlp-admin`, reusable across projects — not checked into this repo). Config and credentials come from an event's own `.env` (git-ignored; copy `events/.env.example` into `events/<event-slug>/.env`); never print or commit its values. Admin login uses `VLP_ADMIN_USERNAME` / `VLP_ADMIN_PASSWORD`; `INIT_STUDENT_PASSWORD` is the initial password for generated student/user CSVs.

**Run every `vlp-admin` script with cwd inside the event's folder** (`cd events/<event-slug>/` first). The scripts find their config and default file paths (`classes/...`, `lab.manuals/...`, `docs/...`) by walking up from the current directory to the nearest `.env` — since each event now owns its own `.env`, running from inside `events/<event-slug>/` is what makes every default path resolve correctly. Running from the project root will pick up the wrong (or no) `.env`.

`events/student.bulk.invite.sample.csv` is the one shared sample/template file and is NOT duplicated into each event folder, so `create_student_invites.py` needs an explicit `--template ../student.bulk.invite.sample.csv` (its own-folder default won't find it).

## Student invites
- `create_student_invites.py` builds invite CSVs from `STUDENT_LIST`; `location` defaults to `AMER` (from the sample CSV row 2), override with `--set location=<value>`.
- Duplicate emails (case-insensitive): first occurrence kept; skipped rows go to `<output stem>.duplicates.csv` (with source row numbers) next to the invite output, with an end-of-run notice. Rows with missing email go to `<output stem>.invalid.csv`. Neither file is created when empty.
- `OVDCS` (in the event's `.env`) is the comma-separated list of OVDCs (VMware Cloud Director org virtual data centers, i.e. cloud capacity) that event will use — see that event's `.md` file for its list.

## Layout

```text
<project root>/
  reference/                    # shared VLP admin-guide / REST API PDFs, not event-specific
  events/
    .env.example                  # shared template; copy to events/<event-slug>/.env
    student.bulk.invite.sample.csv  # shared template; referenced via --template ../student.bulk.invite.sample.csv
    <event-slug>/                 # e.g. cw.oct.2026 (slug encodes event + date, not just location)
      <event-slug-or-date>.md     # event facts (e.g. cw.oct.2026.md)
      .env                        # this event's credentials + config (git-ignored)
      classes/
        class_yaml/ pool_yaml/ shadow_yaml/ manual_yaml/ resource_yaml/ lab_yaml/
        class_creation/           # generated class bulk-upload CSVs
      docs/                       # this event's runbooks and checklists
      lab.manuals/                # this event's lab manual(s) (PDF + zip)
      student.invites/            # generated student invite CSVs (created on demand)
      recordings/                 # Playwright UI-flow recordings for this event
```

Filenames inside `classes/*_yaml/` still carry the event slug (e.g. `pool.clearwater.vcf522-upgrade.yaml`)
even though the folder is already event-scoped — harmless redundancy, kept to minimize churn; new
events are free to drop the prefix.

## Adding a new event

1. `mkdir events/<new-slug>` and create `events/<new-slug>/<new-slug>.md` with that event's facts.
2. Copy `events/.env.example` to `events/<new-slug>/.env` and fill it in.
3. Add `classes/*_yaml/` definitions as needed.
4. `cd events/<new-slug>/` before running any `vlp-admin` script; pass `--template ../student.bulk.invite.sample.csv` to `create_student_invites.py`.

## Rules
- Never store passwords, tokens, or other secrets in project files.

## Related project
`VSCodeWorkspaces/git.work/VLP-Admin/vlp.admin` (git repo): manage_users, manage_classs, saas.consoles, user.cleanup, create.class, doc.
