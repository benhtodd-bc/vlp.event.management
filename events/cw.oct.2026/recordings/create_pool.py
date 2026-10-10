#!/usr/bin/env python3
"""Sanitized flow generated from recordings/raw/create_pool.raw.py by sanitize_recording.py.

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
    vlp_ui.login(page)  # collapsed recorded login steps; credentials come from configuration
    page.get_by_role('button', name='Cloud Management').click()
    page.get_by_role('link', name='Deployment Pools').click()
    page.get_by_role('button', name='Create New').click()
    page.get_by_role('textbox', name='Name *').click()
    page.get_by_role('textbox', name='Name *').fill('VCF522-Upgrade-VCF9.1-REV1')
    page.get_by_role('textbox', name='Primary Lab Template Search').click()
    page.get_by_role('textbox', name='Primary Lab Template Search').fill('VCF522-Upgrade-VCF9.1-REV1')
    page.get_by_role('button', name='VCF522-Upgrade-VCF9.1-REV1 - [lvn3-vcd2-eduprod-r-gc]').click()
    if not vlp_ui.confirm_action("click: page.get_by_role('button', name='Create Deployment Po...')", execute):
        return
    page.get_by_role('button', name='Create Deployment Po...').click()
    if not vlp_ui.confirm_action("click: page.get_by_role('button', name='Add Lab Templates')", execute):
        return
    page.get_by_role('button', name='Add Lab Templates').click()
    page.get_by_role('dialog', name='Add Lab Templates').get_by_label('Select All').check()
    if not vlp_ui.confirm_action("click: page.get_by_role('button', name='Add', exact=True)", execute):
        return
    page.get_by_role('button', name='Add', exact=True).click()
    if not vlp_ui.confirm_action("click: page.get_by_role('button', name='Update Deployment Pool')", execute):
        return
    page.get_by_role('button', name='Update Deployment Pool').click()
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Sanitized recording: create_pool")
    ap.add_argument("--execute", action="store_true", help="Allow gated (write) clicks, with typed confirmation.")
    ap.add_argument("--headless", action="store_true")
    args = ap.parse_args()
    raise SystemExit(vlp_ui.run_flow('create_pool', run, headed=not args.headless, execute=args.execute))
