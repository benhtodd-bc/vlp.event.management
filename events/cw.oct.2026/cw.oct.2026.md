---
event: Clearwater Oct 2026
location: Clearwater, Florida
event_tz: America/New_York
timezones:
  - America/New_York   # event
  - America/Los_Angeles # user
  - Europe/Sofia        # teammate
---

# Clearwater Oct 2026

Event project for the October 2026 event in Clearwater, Florida.

## Time zones

- Event: America/New_York (Eastern, EDT/EST)
- User: America/Los_Angeles (Pacific)
- Teammate in Sofia, Bulgaria: Europe/Sofia (EET/EEST)

## Sessions for this event
| Session Title | LAB template(s)/manual(s) |
|---|---|
| VCF Upgrade Fast Track | 'VC80U3-to-VCF911-Upgrade-Clearwater-Rev2'/'vSphere-to-VVF-Upgrade','VCF522-Upgrade-VCF9.1-REV1'/'VCF5.2.x-to-VCF9.1.x' |
| VCF AIRI Fast Track | 'VCF91-AIRI-FastTrack-Rev4'/'AIRI Fast Track'|
| VKS Fast Track | 'VCF91VKS-FastTrack-v5'/'VCF91VKS_FastTrack' | 

## Day 2 schedule (Wed Oct 14)

| Time | Action | Class |
|---|---|---|
| 2026-10-14 15:00 America/Los_Angeles | Bring up entitlements | VCF AIRI Fast Track - G1 |
| 2026-10-14 15:00 America/Los_Angeles | Start pre-pops | VCF Upgrade Fast Track - G2 |
| - | Not touched | VKS Fast Track |

## Lab manual Sources

- `lab.manuals/` - VCFVKS_FastTrack.(PDF + zip)
- VCF AIRI Fast Track - source is ScreenSteps Import
- VCF Upgrade Fast Track  - source is ScreenSteps Import
  



### Template Shadow Status

Verified live 2026-10-09 via `GET /api/admin/CloudShadow` (read-only API, tenant `livefire`), checked against the 8 target OVDCs. Re-checked same day; status changed for 2 of the 4 templates since the first check (see History below).

| Template | Shadow status | Detail |
|---|---|---|
| VCF91-AIRI-FastTrack-Rev4 | Not started | Still not found in any of the 3 cloud orgs' CloudShadow lists — not yet synced to those clouds' catalogs |
|    | **Confirmed — 8/8 OVDCs** | All 8 target OVDCs show `type=shadows`, `shadowEnabled=true` (lvn3-vcd2-r-ovdc8, lvn3-vcd2-r-ovdc7, lvn9-vcd1-r-ovdc3, lvn9-vcd1-r-ovdc12, lvn9-vcd2-r-ovdc6/7/8/13) |
| VC80U3-to-VCF911-Upgrade-Clearwater-Rev2 | **In progress — 8/8 OVDCs deploying** | Requested via `flows/shadowing.py --execute` 2026-10-09 (all 8 Ok clicks confirmed); CloudShadow API now reads `type=deploying` for all 8 target OVDCs — copy running, not yet complete |
| VCF91VKS-FastTrack-v5 | **In progress — 8/8 OVDCs deploying** | Template now appears in the CloudShadow lists (it didn't on the first check); all 8 OVDCs read `type=deploying`, `available=false` — shadow copy running, not yet complete |

History:

- 2026-10-09 (first check): only VCF522-Upgrade-VCF9.1-REV1 had any CloudShadow data; the other 3 templates weren't listed at all.
- 2026-10-09 (second check): VC80U3-to-VCF911-Upgrade-Clearwater-Rev2 and VCF91VKS-FastTrack-v5 now appear (catalog sync landed between checks) — VC80U3 unshadowed (0/8), VCF91VKS mid-copy. VCF91-AIRI-FastTrack-Rev4 still absent.
- 2026-10-09 (requested VC80U3): `classes/shadow_yaml/shadow.clearwater.vc80u3-upgrade.yaml` created; `flows/shadowing.py --execute` run to request shadows in all 8 OVDCs. Along the way, fixed two real bugs in the shared `flows/shadowing.py` skill script (not project-local): (1) the search-box filter and cloud-expand panel are client-side re-renders that `wait_idle()`'s networkidle check doesn't catch, so the row lookup returned "no row for template" even for templates with real data — fixed by adding a short explicit pause after each; (2) `ovdc_row()`'s `has_text=<ovdc>` locator also matches the parent cloud-level row (which nests all child OVDC rows in its DOM text), and `.first` picked that parent — meaning a write click could have hit the wrong OVDC's replica button (the exact risk flagged in `docs/shadowing.runbook.md` section 6). Fixed by using `.last` instead. Re-verified via `--browse` after each fix before running `--execute`. Confirmed via CloudShadow API: all 8 OVDCs now read `type=deploying`.

### ATE Team

Session Group `Broadcom Advanced Technical Enablement` in `cw.oct.2026.student.list.csv`. Staff, not students — excluded from all invite CSVs (checked for overlap with the VCF.Track.G1/G2 and VKS.Track rosters: none found).

| Name | Email | Role | Assignment |
|---|---|---|---|
| Alasdair Carnie | alasdair.carnie@broadcom.com | Senior Staff Solutions Architect | VCF Upgrades |
| Bal Birdy | bal.birdy@broadcom.com | Enterprise Architect | |
| Andy Beltz | andy.beltz@broadcom.com | Solutions Architect | VCF Upgrades |
| Brian Watrous | brian.watrous@broadcom.com | Advanced Technical Enablement Specialist | AIRI |
| Tim Burkard | tim.burkard@broadcom.com | Technical Trainer | AIRI |
| Dhiraj Sharma | dhiraj.sharma@broadcom.com |  | VKS Fast Track |


### EPC Resources

---
epc: [eduprod]
ovdcs:[lvn3-vcd2-eduprod-r-ovdc8,lvn3-vcd2-eduprod-r-ovdc7,lvn9-vcd1-eduprod-r-ovdc3,lvn9-vcd1-eduprod-r-ovdc12,lvn9-vcd2-eduprod-r-ovdc6,lvn9-vcd2-eduprod-r-ovdc7,lvn9-vcd2-eduprod-r-ovdc8,lvn9-vcd2-eduprod-r-ovdc13] 
source_catalog: [eduilt-xfer]
target_catalog: [CM3-EDU-PROD-DGC]
templates_to_use: [VCF91-AIRI-FastTrack-Rev4,VCF522-Upgrade-VCF9.1-REV1,VC80U3-to-VCF911-Upgrade-Clearwater-Rev2,VCF91VKS-FastTrack-v5]
---