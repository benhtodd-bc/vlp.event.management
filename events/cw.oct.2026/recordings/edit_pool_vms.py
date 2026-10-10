#!/usr/bin/env python3
"""Sanitized flow generated from recordings/raw/edit_pool_vms.raw.py by sanitize_recording.py.

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
    page.goto('https://admin.labplatform.broadcom.com/admin/login')
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)
    # DROPPED: statement not allowed in sanitized flow (context/cookies/headers)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Sanitized recording: edit_pool_vms")
    ap.add_argument("--execute", action="store_true", help="Allow gated (write) clicks, with typed confirmation.")
    ap.add_argument("--headless", action="store_true")
    args = ap.parse_args()
    raise SystemExit(vlp_ui.run_flow('edit_pool_vms', run, headed=not args.headless, execute=args.execute))
