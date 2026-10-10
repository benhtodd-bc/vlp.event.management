#!/usr/bin/env python3
"""Sanitized flow generated from recordings/raw/manual_project.raw.py by sanitize_recording.py.

REVIEW before running: selectors come from a recording and may be brittle.
Write-like clicks are gated: dry-run stops before the first one unless --execute.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / '../.claude/skills/vlp-admin/scripts'))
import vlp_ui  # noqa: E402


def run(page, execute: bool = False) -> None:
    vlp_ui.login(page)  # recording had no login fills; log in via shared helper
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)
    page.goto('https:[REDACTED]')
    page.get_by_role('button', name='Content').click()
    page.get_by_role('link', name='Manual Projects').click()
    page.get_by_role('button', name='Add New').click()
    page.get_by_role('button', name='Start a Manual Project').click()
    page.get_by_role('textbox', name='Name').click()
    page.get_by_role('dialog', name='Start a Manual Project').locator('section').click()
    page.get_by_role('textbox', name='Name').fill('VCF91VKS_FastTrack')
    if not vlp_ui.confirm_action("click: page.get_by_role('button', name='Create', exact=True)", execute):
        return
    page.get_by_role('button', name='Create', exact=True).click()
    page.get_by_role('row', name='Available actions VCF91VKS_FastTrack 10/8/26 2:07:45 PM 10/8/26 2:07:45 PM (').get_by_label('Available actions').click()
    page.get_by_role('button', name='View Project View Project info').press('Escape')
    page.get_by_role('link', name='VCF91VKS_FastTrack').click()
    page.get_by_role('button', name='Upload a Manual file').click()
    page.get_by_role('button', name='Select File', exact=True).click()
    page.get_by_role('button', name='Select File', exact=True).set_input_files('VKSFT91_vSphere Kubernetes Service_ Fast Track [v9.1].zip')
    if not vlp_ui.confirm_action("click: page.get_by_role('button', name='Done')", execute):
        return
    page.get_by_role('button', name='Done').click()
    page.get_by_role('button', name='Dropdown Actions').click()
    if not vlp_ui.confirm_action("click: page.get_by_role('menuitem', name='Promote to Draft Promote to')", execute):
        return
    page.get_by_role('menuitem', name='Promote to Draft Promote to').click()
    page.get_by_role('button', name='Dropdown Actions').first.click()
    if not vlp_ui.confirm_action("click: page.get_by_role('menuitem', name='Publish Draft Publish Draft')", execute):
        return
    page.get_by_role('menuitem', name='Publish Draft Publish Draft').click()
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Sanitized recording: manual_project")
    ap.add_argument("--execute", action="store_true", help="Allow gated (write) clicks, with typed confirmation.")
    ap.add_argument("--headless", action="store_true")
    args = ap.parse_args()
    raise SystemExit(vlp_ui.run_flow('manual_project', run, headed=not args.headless, execute=args.execute))
