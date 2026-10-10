#!/usr/bin/env python3
"""Post-login (sync clouds) portion of the recording (split from recordings/login_full.py) by sanitize_recording.py.

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
    page.get_by_role('button', name='Do Not Sell or Share My').click()
    page.get_by_role('button', name='Cloud Management').click()
    page.get_by_role('link', name='Clouds').click()
    page.get_by_role('row', name='Select Available actions lvn3-vcd1-eduprod-r lvn-cm3-vcd1.broadcom.com lvn-cm3-').get_by_label('Select').check()
    page.get_by_role('row', name='Select Available actions lvn3-vcd2-eduprod-r lvn-cm3-vcd2.broadcom.com lvn-cm3-').get_by_label('Select').check()
    page.get_by_role('row', name='Select Available actions lvn9-vcd1-eduprod-r lvn-cm9-vcd1.broadcom.com lvn-cm9-').get_by_label('Select').check()
    page.get_by_role('row', name='Select Available actions lvn9-vcd2-eduprod-r lvn-cm9-vcd2.broadcom.com lvn-cm9-').get_by_label('Select').check()
    page.get_by_role('button', name='Global Actions').click()
    if not vlp_ui.confirm_action("click: page.get_by_role('menuitem', name='Sync Cloud Org Sync Cloud Org')", execute):
        return
    page.get_by_role('menuitem', name='Sync Cloud Org Sync Cloud Org').click()
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Sanitized recording: sync_clouds")
    ap.add_argument("--execute", action="store_true", help="Allow gated (write) clicks, with typed confirmation.")
    ap.add_argument("--headless", action="store_true")
    args = ap.parse_args()
    raise SystemExit(vlp_ui.run_flow('sync_clouds', run, headed=not args.headless, execute=args.execute))
