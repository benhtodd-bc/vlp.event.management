#!/usr/bin/env python3
"""Regenerate cw.oct.2026.tracker.html (event admin dashboard snapshot).

Run from this folder:  python3 build_tracker.py [--no-accounts]

Inputs:  cw.oct.2026.md, lab-management.tracker.md, classes/class_yaml/*.yaml, rosters/*.csv
         + READ-ONLY VLP API calls (pools, shadows, classes, whether roster accounts exist).
Output:  cw.oct.2026.tracker.html - one self-contained file; no credentials in it.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

HERE = Path(__file__).resolve().parent
SKILL = Path.home() / ".claude/skills/vlp-admin/scripts"
sys.path.insert(0, str(SKILL))
import vlp_env  # noqa: E402
from vlp_api import VlpClient, VlpApiError  # noqa: E402
from check_shadow import classify  # noqa: E402

ADMIN_BASE = "https://admin.labplatform.broadcom.com"
ADMIN_LINKS = [  # routes read from the live admin UI menu
    ("Classes", "/admin/classes"), ("Labs", "/admin/labs"), ("Lab Resources", "/admin/lab-resources"),
    ("Deployment Pools", "/admin/deployment-pools"), ("Cloud vApps", "/admin/cloud-vapps"),
    ("Cloud Tasks", "/admin/task-management/cloud-tasks"), ("Cloud Shadow", "/admin/cloud-shadow"),
    ("Clouds", "/admin/clouds"), ("Cloud oVDCs", "/admin/cloud-org-vdcs"), ("Groups", "/admin/tenant-groups"),
    ("Dashboard", "/admin/dashboard/0"),
]
STEP_RUNBOOK = {"1": None, "2": "docs/shadowing.runbook.md", "3": "docs/deployment-pool.runbook.md",
                "4": "docs/manual-project.runbook.md", "5": "docs/lab.runbook.md",
                "6": "docs/class-build.runbook.md", "7": "docs/class-build.runbook.md"}


def md_tables(text: str) -> dict[str, list[dict]]:
    """Markdown tables keyed by the nearest preceding heading."""
    out, heading, block = {}, "", []

    def flush():
        if len(block) >= 3:
            hdr = [c.strip() for c in block[0].strip().strip("|").split("|")]
            rows = [dict(zip(hdr, [c.strip() for c in r.strip().strip("|").split("|")])) for r in block[2:]]
            out.setdefault(heading, rows)
        block.clear()

    for ln in text.splitlines():
        if ln.startswith("|"):
            block.append(ln)
            continue
        flush()
        m = re.match(r"#+\s+(.*)", ln)
        if m:
            heading = m.group(1).strip()
    flush()
    return out


def status_of(cell: str) -> str:
    for sym, name in (("🚫", "blocked"), ("🔄", "progress"), ("⬜", "todo"), ("❓", "unknown")):
        if sym in cell:
            return name
    return "done" if "✅" in cell else "none"


def derive_sku(name: str) -> str:
    return re.sub(r"\s+", "-", name.strip().lower())


def utc_iso(date: str, time: str, tz: str) -> str:
    d = dt.datetime.fromisoformat(f"{date}T{time}").replace(tzinfo=ZoneInfo(tz))
    return d.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_event() -> dict:
    text = (HERE / "cw.oct.2026.md").read_text()
    fm = yaml.safe_load(text.split("---")[1])
    tables = md_tables(text)
    epc = {}
    for key in ("epc", "ovdcs", "source_catalog", "target_catalog", "templates_to_use"):
        m = re.search(rf"^{key}:\s*\[(.*)\]", text, re.M)
        epc[key] = [x.strip() for x in m.group(1).split(",")] if m else []
    day2 = []
    for r in next((v for k, v in tables.items() if k.startswith("Day 2 schedule")), []):
        m = re.match(r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) (\S+)$", r["Time"])
        day2.append({"at": utc_iso(m.group(1), m.group(2), m.group(3)) if m else None, "action": r["Action"], "class": r["Class"]})
    return {"name": fm["event"], "day2": day2, "location": fm["location"], "event_tz": fm["event_tz"],
            "timezones": [t.split("#")[0].strip() for t in fm["timezones"]],
            "sessions": tables.get("Sessions for this event", []), "team": tables.get("ATE Team", []), "epc": epc}


def load_classes() -> list[dict]:
    classes = []
    for f in sorted((HERE / "classes/class_yaml").glob("*.yaml")):
        y = yaml.safe_load(f.read_text())
        s = y["schedule"]
        roster = []
        src = (y.get("students") or {}).get("source")
        if src and (HERE / src).exists():
            with open(HERE / src, newline="") as fh:
                roster = [{"email": r["email"].strip(), "name": f'{r.get("firstName","")} {r.get("lastName","")}'.strip(),
                           "company": r.get("company", "")} for r in csv.DictReader(fh) if r.get("email")]
        classes.append({"name": y["className"], "sku": y.get("classSku") or derive_sku(y["className"]),
                        "tz": y["timezone"], "start": utc_iso(s["startDate"], s["startTime"], y["timezone"]),
                        "end": utc_iso(s["endDate"], s["endTime"], y["timezone"]), "seats": y.get("numberOfSeats"),
                        "instructors": y.get("instructors", []), "owners": y.get("owners", []),
                        "enabled": y.get("enabled"), "labs": [l.get("displayName") or l.get("sku") for l in y.get("labs", [])],
                        "labSkus": [l.get("sku") for l in y.get("labs", [])], "roster": roster})
    return classes


def vlp_snapshot(event: dict, classes: list[dict], check_accounts: bool) -> dict:
    vlp_env.load_env()
    tenant = os.environ["EVENT_TENANT"]
    templates, ovdcs = event["epc"]["templates_to_use"], event["epc"]["ovdcs"]
    snap = {"ok": False, "pools": [], "shadows": {}, "classes_found": {}, "accounts": {}}
    try:
        with VlpClient(tenant=tenant, username=os.environ["VLP_ADMIN_USERNAME"],
                       password=os.environ["VLP_ADMIN_PASSWORD"]) as c:
            for p in c.get_json("/api/admin/deploymentPools", tenant=tenant)["data"]:
                if p["name"] in templates:
                    vms = [v["displayName"] for v in p.get("deploymentPoolVms", [])]
                    snap["pools"].append({"id": p["id"], "name": p["name"], "enabled": p["enabled"],
                                          "available": p["available"], "provisioning": p["provisioning"],
                                          "ready": p["ready"], "errors": p["errorCount"] + len(p.get("errors", [])),
                                          "errorMsgs": [e.get("message", "") for e in p.get("errors", [])],
                                          "refillAt": p["refillAt"], "fillUp": p["fillUp"],
                                          "labs": [l.get("displayName") for l in p.get("labs", [])],
                                          "labSkus": [l.get("displayName") for l in p.get("labSkus", [])],
                                          "vmCount": len(vms), "hasConsoleVm": any(v.lower() == "console" for v in vms)})
            clouds = ",".join(sorted({o.rsplit("-", 1)[0] for o in ovdcs}))
            rows = c.get_json("/api/admin/CloudShadow", tenant=tenant, cloudOrgs=clouds)["data"]
            by = {(r["name"], v.get("orgVdcName")): v for r in rows for v in r.get("orgVdcs", [])}
            for t in templates:
                st = {o: classify(by.get((t, o))) for o in ovdcs}
                snap["shadows"][t] = {"shadowed": sum(s == "SHADOWED" for s in st.values()), "total": len(ovdcs),
                                      "missing": [o for o, s in st.items() if s != "SHADOWED"], "ovdcs": st}
            found = c.get_json("/api/admin/classes", tenant=tenant, search="Fast Track")
            found = found.get("data", found) if isinstance(found, dict) else found
            for x in found or []:
                snap["classes_found"][x.get("sku")] = {"id": x.get("id"), "enabled": x.get("enabled")}
            if check_accounts:
                for cl in classes:
                    for s in cl["roster"]:
                        try:
                            c.get_json(f"/api/admin/accounts/{s['email']}", tenant=tenant)
                            snap["accounts"][s["email"]] = True
                        except VlpApiError as e:
                            if e.status != 404:
                                raise
                            snap["accounts"][s["email"]] = False
        snap["ok"] = True
    except Exception as e:  # noqa: BLE001 - dashboard still builds from the files
        snap["error"] = type(e).__name__ + ": " + str(e)[:160]
    return snap


def todo_list(tracker_tables: dict, snap: dict) -> list[dict]:
    todo = []
    labs = next((v for k, v in tracker_tables.items() if k.startswith("Labs")), [])
    for row in labs:
        name = row.get("Lab (template)", "")
        for col, cell in row.items():
            m = re.match(r"(\d)\.", col)
            if m and status_of(cell) not in ("done", "none"):
                todo.append({"step": int(m.group(1)), "area": name, "what": col.split(". ", 1)[1], "detail": cell,
                             "status": status_of(cell), "runbook": STEP_RUNBOOK.get(m.group(1))})
    classes = next((v for k, v in tracker_tables.items() if k.startswith("Classes")), [])
    for row in classes:
        for col in ("6. Create Class", "7. Verify"):
            cell = row.get(col, "")
            if status_of(cell) not in ("done", "none"):
                todo.append({"step": int(col[0]), "area": row.get("Class", ""), "what": col.split(". ", 1)[1],
                             "detail": cell, "status": status_of(cell), "runbook": STEP_RUNBOOK[col[0]]})
    return sorted(todo, key=lambda t: (t["step"], t["area"]))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-accounts", action="store_true", help="skip the per-student VLP account lookups")
    a = ap.parse_args()
    event = load_event()
    classes = load_classes()
    tracker_tables = md_tables((HERE / "lab-management.tracker.md").read_text())
    snap = vlp_snapshot(event, classes, not a.no_accounts)
    data = {"generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "event": event,
            "classes": classes, "tracker": tracker_tables, "todo": todo_list(tracker_tables, snap), "snap": snap,
            "adminBase": ADMIN_BASE, "adminLinks": ADMIN_LINKS}
    html = (HERE / "tracker.template.html").read_text()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    (HERE / "cw.oct.2026.tracker.html").write_text(html.replace("__DATA__", payload))
    print(f"wrote cw.oct.2026.tracker.html  (VLP read: {'ok' if snap['ok'] else 'FAILED - ' + snap.get('error', '')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
