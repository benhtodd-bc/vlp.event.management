#!/usr/bin/env python3
"""Sanitized flow generated from recordings/raw/shadowing.raw.py by sanitize_recording.py.

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
    page.get_by_role('button', name='Cloud Management').click()
    page.get_by_role('link', name='Cloud Shadow').click()
    page.get_by_role('textbox', name='Search...').click()
    page.get_by_role('textbox', name='Search...').fill('VCF522-Upgrade-VCF9.1-REV1')
    page.get_by_role('row', name='Open VCF522-Upgrade-VCF9.1-REV1 lvn3-vcd2-eduprod-r CM3-EDU-PROD-DGC 1/7 Shadow').get_by_label('Open').click()
    page.locator('#clr-dg-row56 > .datagrid-row-scrollable > .datagrid-scrolling-cells > .medium-column.truncate.quick-action-item-column > .vlp-truncate-text > .clickable').click()
    if not vlp_ui.confirm_action("click: page.get_by_role('button', name='Ok')", execute):
        return
    page.get_by_role('button', name='Ok').click()
    page.locator('#clr-dg-row55 > .datagrid-row-scrollable > .datagrid-scrolling-cells > .medium-column.truncate.quick-action-item-column > .vlp-truncate-text > .clickable').click()
    if not vlp_ui.confirm_action("click: page.get_by_role('button', name='Ok')", execute):
        return
    page.get_by_role('button', name='Ok').click()
    page.get_by_role('button', name='Close').click()
    page.get_by_role('row', name='Open VCF522-Upgrade-VCF9.1-REV1 lvn9-vcd1-eduprod-r CM3-EDU-PROD-DGC 1/7 Shadow').get_by_label('Open').click()
    page.locator('#clr-dg-row63 > .datagrid-row-scrollable > .datagrid-scrolling-cells > .medium-column.truncate.quick-action-item-column > .vlp-truncate-text > .clickable').click()
    if not vlp_ui.confirm_action("click: page.get_by_role('button', name='Ok')", execute):
        return
    page.get_by_role('button', name='Ok').click()
    page.locator('.vlp-truncate-text > .clickable').first.click()
    if not vlp_ui.confirm_action("click: page.get_by_role('button', name='Ok')", execute):
        return
    page.get_by_role('button', name='Ok').click()
    page.get_by_role('button', name='Close').click()
    page.get_by_role('row', name='Open VCF522-Upgrade-VCF9.1-REV1 lvn9-vcd2-eduprod-r CM3-EDU-PROD-DGC 1/8 Shadow').get_by_label('Open').click()
    page.locator('#clr-dg-row70 > .datagrid-row-scrollable > .datagrid-scrolling-cells > .medium-column.truncate.quick-action-item-column > .vlp-truncate-text > .clickable').click()
    if not vlp_ui.confirm_action("click: page.get_by_role('button', name='Ok')", execute):
        return
    page.get_by_role('button', name='Ok').click()
    page.locator('#clr-dg-row71 > .datagrid-row-scrollable > .datagrid-scrolling-cells > .medium-column.truncate.quick-action-item-column > .vlp-truncate-text > .clickable').click()
    if not vlp_ui.confirm_action("click: page.get_by_role('button', name='Ok')", execute):
        return
    page.get_by_role('button', name='Ok').click()
    page.locator('#clr-dg-row72 > .datagrid-row-scrollable > .datagrid-scrolling-cells > .medium-column.truncate.quick-action-item-column > .vlp-truncate-text > .clickable').click()
    if not vlp_ui.confirm_action("click: page.get_by_role('button', name='Ok')", execute):
        return
    page.get_by_role('button', name='Ok').click()
    page.locator('.vlp-truncate-text > .clickable').first.click()
    if not vlp_ui.confirm_action("click: page.get_by_role('button', name='Ok')", execute):
        return
    page.get_by_role('button', name='Ok').click()
    page.get_by_role('button', name='Close').click()
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Sanitized recording: shadowing")
    ap.add_argument("--execute", action="store_true", help="Allow gated (write) clicks, with typed confirmation.")
    ap.add_argument("--headless", action="store_true")
    args = ap.parse_args()
    raise SystemExit(vlp_ui.run_flow('shadowing', run, headed=not args.headless, execute=args.execute))
