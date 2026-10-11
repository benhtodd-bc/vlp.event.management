# Lab management tracker — Clearwater Oct 2026

Tracks each lab/class through the 7 build steps (the referenced `lab-management.checklist.md` does not exist in the repo; step order follows `docs/class-build.runbook.md`). ✅ done, 🔄 in progress, ⬜ not started, 🚫 blocked.

## Labs (checklist steps 1-5)

| Lab (template) | 1. Copy to catalog | 2. Shadow OVDCs | 3. Create Pool | 4. Manual/Resources | 5. Create Lab |
|---|---|---|---|---|---|
| VCF522-Upgrade-VCF9.1-REV1 | ✅ | ✅ 8/8 OVDCs (2026-10-10) | ✅ (initial console set) | ✅ manual attached, no resources needed | ✅ |
| VC80U3-to-VCF911-Upgrade-Clearwater-Rev2 | ✅ | ✅ 8/8 OVDCs (2026-10-10) | ✅ pool created; initial console set on the lab to `dc01-20Mar2026` | ✅ manual `vSphere-to-VVF-Upgrade` linked | ✅ `Clearwater-VC80U3-Upgrade` (disabled, no catalog) 2026-10-11 |
| VCF91VKS-FastTrack-v5 | ✅ | ✅ 8/8 OVDCs (2026-10-10) | ✅ pool created, initial console set (2026-10-11) | ✅ manual `VCF91VKS_FastTrack` + resource `VCF91VKS_FastTrack_PDF` attached | ✅ `Clearwater-VCF91-VKS-FastTrack` (disabled, no catalog) 2026-10-11 |
| VCF91-AIRI-FastTrack-Rev4 | ✅ now present in CloudShadow for all 4 clouds (was absent entirely as of 2026-10-08 — the earlier "not synced" blocker is cleared) | ✅ 8/8 OVDCs (2026-10-10) | ✅ pool created (id 45110), initial console set (2026-10-11) | ✅ manual `AIRI Fast Track` linked; no resources | ✅ `Clearwater-VCF91-AIRI-FastTrack` (disabled, no catalog) 2026-10-11 |

## Shadow status (detail behind step 2 above)

Checked 2026-10-10 with `check_shadow.py` (CloudShadow API; AIRI also confirmed by eye on the Cloud Shadow page).

| Template | Target OVDCs shadowed | Next step |
|---|---|---|
| VCF522-Upgrade-VCF9.1-REV1 | 8 of 8 | None |
| VC80U3-to-VCF911-Upgrade-Clearwater-Rev2 | 8 of 8 | None |
| VCF91VKS-FastTrack-v5 | 8 of 8 | None |
| VCF91-AIRI-FastTrack-Rev4 | 8 of 8 | None |

Target OVDCs (all 4 templates, per `cw.oct.2026.md` EPC Resources): lvn3-vcd2-eduprod-r-ovdc7/8, lvn9-vcd1-eduprod-r-ovdc3/12, lvn9-vcd2-eduprod-r-ovdc6/7/8/13.

## Classes (checklist steps 6-7)

| Class | Labs | 6. Create Class | 7. Verify |
|---|---|---|---|
| VKS Fast Track | VCF91VKS-FastTrack-v5 | ✅ created 2026-10-11, disabled (Oct 13–15); instructor Dhiraj Sharma; no students added yet | 🔄 instructors, dates, seats, labs read back; students and enable still to do |
| VCF Upgrade Fast Track - G1 | VC80U3-Upgrade, VCF522-Upgrade | ✅ created 2026-10-11, disabled (Oct 13–14); instructors Alasdair Carnie + Andy Beltz; both labs attached; no students added yet | 🔄 instructors, dates, seats, labs read back; students and enable still to do |
| VCF Upgrade Fast Track - G2 | VC80U3-Upgrade, VCF522-Upgrade | ✅ created 2026-10-11, disabled (Oct 15–16); instructors Alasdair Carnie + Andy Beltz; both labs attached; no students added yet | 🔄 instructors, dates, seats, labs read back; students and enable still to do |
| VCF AIRI Fast Track - G1 | VCF91-AIRI-FastTrack-Rev4 | ✅ created 2026-10-11, disabled (Oct 15–16); instructors Brian Watrous + Tim Burkard; no students added yet | 🔄 instructors, dates, seats, lab warning read back; students and enable still to do |
| VCF AIRI Fast Track - G2 | VCF91-AIRI-FastTrack-Rev4 | ✅ created 2026-10-11, disabled (Oct 13–14); instructors Brian Watrous + Tim Burkard; no students added yet | 🔄 instructors, dates, seats, lab warning read back; students and enable still to do |
