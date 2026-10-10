# Lab management tracker — Clearwater Oct 2026

Tracks each lab/class through the 7 build steps (the referenced `lab-management.checklist.md` does not exist in the repo; step order follows `docs/class-build.runbook.md`). ✅ done, 🔄 in progress, ⬜ not started, 🚫 blocked.

## Labs (checklist steps 1-5)

| Lab (template) | 1. Copy to catalog | 2. Shadow OVDCs | 3. Create Pool | 4. Manual/Resources | 5. Create Lab |
|---|---|---|---|---|---|
| VCF522-Upgrade-VCF9.1-REV1 | ✅ | ✅ 8/8 OVDCs (2026-10-10) | ✅ (initial console set) | ✅ manual attached, no resources needed | ✅ |
| VC80U3-to-VCF911-Upgrade-Clearwater-Rev2 | ✅ | ✅ 8/8 OVDCs (2026-10-10) | ✅ pool created, ⬜ initial console not set | ⬜ | ⬜ |
| VCF91VKS-FastTrack-v5 | ✅ | ✅ 8/8 OVDCs (2026-10-10) | ✅ pool created, ⬜ initial console not set | ✅ manual + resource (`VCF91VKS_FastTrack_PDF`) both confirmed existing; not attached to a lab yet | ⬜ |
| VCF91-AIRI-FastTrack-Rev4 | ✅ now present in CloudShadow for all 4 clouds (was absent entirely as of 2026-10-08 — the earlier "not synced" blocker is cleared) | ✅ 8/8 OVDCs (2026-10-10) | 🚫 no pool yet | 🚫 | 🚫 |

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
| VKS Fast Track | VCF91VKS-FastTrack-v5 | ⬜ | ⬜ |
| VCF Upgrade Fast Track - G1 | VC80U3-Upgrade, VCF522-Upgrade | ⬜ | ⬜ |
| VCF Upgrade Fast Track - G2 | VC80U3-Upgrade, VCF522-Upgrade | ⬜ | ⬜ |
| VCF AIRI Fast Track - G1 | VCF91-AIRI-FastTrack-Rev4 | 🚫 no pool yet (catalog-sync blocker cleared 2026-10-10, see Labs table) | 🚫 |
| VCF AIRI Fast Track - G2 | VCF91-AIRI-FastTrack-Rev4 | 🚫 no pool yet (catalog-sync blocker cleared 2026-10-10, see Labs table) | 🚫 |
