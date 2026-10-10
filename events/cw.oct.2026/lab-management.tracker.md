# Lab management tracker — Clearwater Oct 2026

Tracks each lab/class against `lab-management.checklist.md`. ✅ done, 🔄 in progress, ⬜ not started, 🚫 blocked.

## Labs (checklist steps 1-5)

| Lab (template) | 1. Copy to catalog | 2. Shadow OVDCs | 3. Create Pool | 4. Manual/Resources | 5. Create Lab |
|---|---|---|---|---|---|
| VCF522-Upgrade-VCF9.1-REV1 | ✅ | ❓ not yet re-verified live (see Shadow status below) | ✅ (initial console set) | ✅ manual attached, no resources needed | ✅ |
| VC80U3-to-VCF911-Upgrade-Clearwater-Rev2 | ✅ | ❓ not yet verified live | ✅ pool created, ⬜ initial console not set | ⬜ | ⬜ |
| VCF91VKS-FastTrack-v5 | ✅ | ❓ 2/8 OVDCs verified live (ovdc7, ovdc8); rest unchecked | ✅ pool created, ⬜ initial console not set | ✅ manual + resource (`VCF91VKS_FastTrack_PDF`) both confirmed existing; not attached to a lab yet | ⬜ |
| VCF91-AIRI-FastTrack-Rev4 | ✅ now present in CloudShadow for all 4 clouds (was absent entirely as of 2026-10-08 — the earlier "not synced" blocker is cleared) | ❓ not yet verified live | 🚫 no pool yet | 🚫 | 🚫 |

## Shadow status (detail behind step 2 above)

CloudShadow API checked 2026-10-10 — unchanged from the prior day's read. The API's per-OVDC field cannot distinguish one template's shadow state from another's (see `docs/shadowing.runbook.md` section 3), so it's not used here. Status below reflects only what's been confirmed by someone looking at the live Cloud Shadow page.

| Template | Verified in live UI | Next step |
|---|---|---|
| VCF522-Upgrade-VCF9.1-REV1 | No OVDC checked yet this way | Walk all 8 target OVDCs in the UI |
| VC80U3-to-VCF911-Upgrade-Clearwater-Rev2 | No OVDC checked yet this way | Walk all 8 target OVDCs in the UI |
| VCF91VKS-FastTrack-v5 | 2 of 8 (ovdc7, ovdc8 on lvn3-vcd2) | Walk remaining 6 OVDCs |
| VCF91-AIRI-FastTrack-Rev4 | None | Walk all 8 target OVDCs in the UI |

Target OVDCs (all 4 templates, per `cw.oct.2026.md` EPC Resources): lvn3-vcd2-eduprod-r-ovdc7/8, lvn9-vcd1-eduprod-r-ovdc3/12, lvn9-vcd2-eduprod-r-ovdc6/7/8/13.

## Classes (checklist steps 6-7)

| Class | Labs | 6. Create Class | 7. Verify |
|---|---|---|---|
| VKS Fast Track | VCF91VKS-FastTrack-v5 | ⬜ | ⬜ |
| VCF Upgrade Fast Track - G1 | VC80U3-Upgrade, VCF522-Upgrade | ⬜ | ⬜ |
| VCF Upgrade Fast Track - G2 | VC80U3-Upgrade, VCF522-Upgrade | ⬜ | ⬜ |
| VCF AIRI Fast Track - G1 | VCF91-AIRI-FastTrack-Rev4 | 🚫 no pool yet (catalog-sync blocker cleared 2026-10-10, see Labs table) | 🚫 |
| VCF AIRI Fast Track - G2 | VCF91-AIRI-FastTrack-Rev4 | 🚫 no pool yet (catalog-sync blocker cleared 2026-10-10, see Labs table) | 🚫 |
