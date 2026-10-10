#!/usr/bin/env python3
"""Sanitized flow generated from recordings/raw/lab_resource.raw.py by sanitize_recording.py.

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
    page.get_by_role('button', name='Lab Management').click()
    page.get_by_role('link', name='Lab Resources').click()
    page.get_by_role('button', name='Create New').click()
    page.get_by_role('textbox', name='Name *').click()
    page.get_by_role('textbox', name='Name *').fill('VCF91VKS_FastTrack_PDF')
    page.get_by_text('Upload a file').first.click()
    page.locator('#path_file').set_input_files('VCF91VKS_FastTrack.pdf')
    if not vlp_ui.confirm_action("click: page.get_by_role('button', name='Create Lab Resource')", execute):
        return
    page.get_by_role('button', name='Create Lab Resource').click()
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Sanitized recording: lab_resource")
    ap.add_argument("--execute", action="store_true", help="Allow gated (write) clicks, with typed confirmation.")
    ap.add_argument("--headless", action="store_true")
    args = ap.parse_args()
    raise SystemExit(vlp_ui.run_flow('lab_resource', run, headed=not args.headless, execute=args.execute))
