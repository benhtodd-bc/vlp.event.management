#!/usr/bin/env bash
# Rebuild the tracker and publish it to the Apps Script web app. Re-deploys the SAME deployment, so the URL stays.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 build_tracker.py --site
cd site
clasp push -f
DEP=$(clasp deployments | grep -E '@[0-9]+ ' | head -1 | grep -oE 'AKfy[A-Za-z0-9_-]+')
clasp deploy -i "$DEP" --description "tracker $(date -u +%Y-%m-%dT%H:%MZ)"
