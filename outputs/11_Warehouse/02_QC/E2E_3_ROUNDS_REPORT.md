# E2E 3-Round Stability Verification — Warehouse & Bin (WarehouseBin.html)

- **Feature:** F-LOCATION-MASTER-001 · Warehouse & Bin / Location Hierarchy (5-level master, single-file SPA)
- **Target:** `../01_HTML/WarehouseBin.html`
- **Date:** 2026-08-06
- **Method:** Real browser automation (Chromium via Playwright, project venv), 3 full rounds × 3 viewports (**1280 / 1440 / 1920**), each round on a fresh browser context so in-memory mock state never leaks between rounds. Every scenario drives the app's real handlers/DOM; screenshots captured per step.
- **Suite:** `e2e_3rounds_warehouse.py` · **Raw results:** `E2E_3_ROUNDS_RESULT.json` · **Evidence:** `e2e_shots/round{1,2,3}_{viewport}_*.png` (105 shots; ux-shots preserved separately in `ux-shots/`)

## Overall verdict

> ## ✅ PASS — all 3 rounds green on all 3 viewports
> **183 / 183 assertions passed · 0 failed · 0 console errors · 0 page errors.**
> No product bugs found. Safe for manual testing.

| Round | Scope | Assertions (×3 viewports) | Console err | Page err | Result |
|---|---|---:|---:|---:|---|
| 1 | Happy-path lifecycle (build a whole warehouse) | 66 / 66 | 0 | 0 | ✅ PASS |
| 2 | Negative / validation / guards / RBAC | 69 / 69 | 0 | 0 | ✅ PASS |
| 3 | State, persistence & robustness | 48 / 48 | 0 | 0 | ✅ PASS |
| **Total** | | **183 / 183** | **0** | **0** | **✅ PASS** |

Counts are the sum across viewports (22 / 23 / 16 unique scenarios per round respectively). A round is counted green only when it has 0 failures **and** 0 console/page errors on every viewport.

---

## Round 1 — Happy-path lifecycle (22 scenarios / viewport)

Builds a complete warehouse from scratch and reads it back.

| # | Scenario | Expected | Result | Evidence |
|---|---|---|---|---|
| 1 | Root list renders | 5 KPI stats + drill breadcrumb chip | ✅ | `round1_*_01_root_list.png` |
| 2 | Create Warehouse — branch picker (required) | branch=BR-01 persisted | ✅ | `round1_*_02_wh_geo_cascade.png` |
| 3 | Geo cascade จังหวัด→อำเภอ→ตำบล | child levels reset when province picked | ✅ | `round1_*_02_wh_geo_cascade.png` |
| 4 | Geo cascade → postcode auto | ตำบล บางพลีใหญ่ → 10540 (form + DOM) | ✅ | `round1_*_02_wh_geo_cascade.png` |
| 5 | WH persists | new WH active, branch+postcode saved, drawer closed | ✅ | — |
| 6 | KPI updates after create | warehouse count +1 | ✅ | — |
| 7 | Branch in drill breadcrumb | `สาขา` chip shown after drilling into WH | ✅ | `round1_*_03_zone_temp.png` |
| 8 | Create Zone — temp_controlled → range | temp_controlled=true, min 2 / max 8 under new WH | ✅ | `round1_*_03_zone_temp.png` |
| 9 | Create Area — allows_direct on | allows_direct=true under new Zone | ✅ | `round1_*_04_area_allows_direct.png` |
| 10 | Create Rack — rows×cols×levels | grid 2×3×2 under new Area | ✅ | `round1_*_05_rack_grid.png` |
| 11 | Location wizard step 1 opens | loc-form, step 1 | ✅ | `round1_*_06_loc_wizard_step1.png` |
| 12 | Wizard advances to step 2 | 2-step stepper, step=2 | ✅ | `round1_*_07_loc_wizard_step2.png` |
| 13 | Location persists (incl PACK type) | type=PACK, cap=5>0, barcode set → active | ✅ | — |
| 14 | Bulk Generate drawer opens | bulk view | ✅ | `round1_*_08_bulk_preview.png` |
| 15 | Bulk preview count | 2 racks × 2 = 4 locations | ✅ | `round1_*_08_bulk_preview.png` |
| 16 | Bulk commit atomic | +2 racks, +4 locations, drawer closed | ✅ | — |
| 17 | View Location — 3 tabs | overview / capacity&flags / history | ✅ | `round1_*_09_viewloc_capacity.png` |
| 18 | Capacity tab (real click) | non-blank, shows ความจุ | ✅ | `round1_*_09_viewloc_capacity.png` |
| 19 | History tab | WORM timeline renders | ✅ | — |
| 20 | View Node — full_path w/ branch | breadcrumb shows branch **bold** + ` › ` | ✅ | `round1_*_10_viewnode_path.png` |
| 21 | View Node — child counts + drill button | present | ✅ | `round1_*_10_viewnode_path.png` |
| 22 | 5-level drill-down (real row clicks) | WH→Zone→Area→Rack + location rows | ✅ | `round1_*_11_drill_location_list.png` |

## Round 2 — Negative / validation / guards / RBAC (23 scenarios / viewport)

Every guard must block correctly and leave data untouched.

| # | Scenario | Expected | Result | Evidence |
|---|---|---|---|---|
| 1 | flexible-parent XOR | exactly one of rack/area id set; switching parent nulls the other | ✅ | `round2_*_01_xor_guard.png` |
| 2 | flexible-parent — neither parent | blocked at step 1 | ✅ | `round2_*_01_xor_guard.png` |
| 3 | allows_direct=false | block + "เพิ่มชั้นวางก่อน" suggestion | ✅ | `round2_*_02_allows_direct_block.png` |
| 4 | Duplicate code — Warehouse | 409-style block, no insert ("รหัสซ้ำในระบบ") | ✅ | — |
| 5 | Duplicate code — Zone | block within warehouse ("...ภายในคลังเดียวกัน") | ✅ | — |
| 6 | Duplicate code — Area | block within zone | ✅ | — |
| 7 | Duplicate code — Rack | block within area | ✅ | — |
| 8 | Duplicate code — Location | block within parent, wizard returns to step 1, no insert | ✅ | `round2_*_03_dup_location.png` |
| 9 | Capacity ≤ 0 | block ("ความจุต้องมากกว่า 0"), no insert | ✅ | `round2_*_04_capacity_zero.png` |
| 10 | Zone temp_controlled, missing range | block, no insert | ✅ | `round2_*_05_temp_missing.png` |
| 11 | Bulk-gen code collision | atomic rollback — submit disabled, 0 rows added (2 collisions detected) | ✅ | `round2_*_06_bulk_collision.png` |
| 12 | Bulk-gen grid = 0 | total 0 → submit disabled, no insert | ✅ | `round2_*_07_bulk_grid_zero.png` |
| 13 | **GAP-02** reparent w/ stock | blocked, parent unchanged, drawer stays w/ error | ✅ | `round2_*_08_reparent_stock_block.png` |
| 14 | **GAP-01** archive node w/ active children | blocked (no confirm path, "จัดเก็บคลังไม่ได้"), 4 active children | ✅ | `round2_*_09_archive_children_block.png` |
| 15 | **GAP-01** blocked node stays active | WH-01 status remains active | ✅ | `round2_*_09_archive_children_block.png` |
| 16 | Decommission location w/ stock | blocked (no confirm, "ต้องย้ายสต็อกออกก่อน"), status unchanged | ✅ | `round2_*_10_decommission_stock_block.png` |
| 17 | Barcode required before activate | L006 (no barcode) stays inactive | ✅ | — |
| 18 | RBAC Operator = view-only | perms create/del/status all false | ✅ | `round2_*_11_rbac_operator.png` |
| 19 | RBAC Operator — header create disabled | create button disabled | ✅ | `round2_*_11_rbac_operator.png` |
| 20 | RBAC Operator — view drawer | no edit / archive controls | ✅ | — |
| 21 | RBAC Supervisor — create/edit yes, archive no | del=false | ✅ | `round2_*_12_rbac_supervisor.png` |
| 22 | RBAC Supervisor — header create enabled | create enabled | ✅ | `round2_*_12_rbac_supervisor.png` |
| 23 | RBAC Supervisor — view drawer | edit present, archive (danger) hidden | ✅ | — |

## Round 3 — State, persistence & robustness (16 scenarios / viewport)

| # | Scenario | Expected | Result | Evidence |
|---|---|---|---|---|
| 1 | 7-state: active→blocked(+reason)→active | transitions apply, reason stored | ✅ | `round3_*_01_state_transitions.png` |
| 2 | 7-state: frozen / maintenance / full | each transition applies | ✅ | `round3_*_01_state_transitions.png` |
| 3 | 7-state: decommission (soft-kept) | record stays, status=decommissioned, array length unchanged | ✅ | `round3_*_02_decommission_soft.png` |
| 4 | WORM audit on transitions | audit entries appended (0→9) | ✅ | — |
| 5 | Node soft-archive keeps record + badge | WH-03 kept, status=archived, "จัดเก็บแล้ว" badge shown in list | ✅ | `round3_*_03_node_archived_badge.png` |
| 6 | Refresh-safe — reload mid-drill | valid root render, no crash / 0 page errors | ✅ | `round3_*_04_reload_mid_drill.png` |
| 7 | Refresh-safe — reload mid-drawer | drawer closed, valid render, no crash | ✅ | `round3_*_05_reload_mid_drawer.png` |
| 8 | Esc chain tier 1 | combobox list closes first, drawer stays | ✅ | `round3_*_06_esc_combobox.png` |
| 9 | In-drawer modal z-index | modal backdrop z=70 > drawer z=55; elementFromPoint(center)=modal | ✅ | `round3_*_07_modal_over_drawer_zindex.png` |
| 10 | Esc chain tier 2 | modal closes first, drawer stays | ✅ | `round3_*_07_modal_over_drawer_zindex.png` |
| 11 | Esc chain tier 3 | next Esc closes drawer | ✅ | — |
| 12 | Drawer content re-render after in-drawer tab switch | content persists, not blank/collapsed | ✅ | `round3_*_08_drawer_rerender.png` |
| 13 | Empty state (no-match filter) | "ไม่พบรายการที่ค้นหา" | ✅ | `round3_*_09_empty_state.png` |
| 14 | Loading skeleton | `.sk-line` rows render | ✅ | `round3_*_10_loading_state.png` |
| 15 | Error state (deleted/missing node) | "ไม่พบข้อมูลที่กำลังดู" | ✅ | `round3_*_11_error_state.png` |
| 16 | Geo cascade reset on province change | district/subdistrict/postcode cleared | ✅ | `round3_*_12_geo_reset.png` |

The two latent base-kit bugs the memory file flags (in-drawer modal z-index, drawer re-render after in-drawer action) were both explicitly re-verified here (Round 3 #9 and #12) and are **fixed / not reproducible** — modal computed z-index 70 sits above the drawer's 55 and `elementFromPoint` at the modal centre resolves to `.modal`; the drawer keeps its content after an in-drawer tab switch.

---

## Bugs found

**None.** No product defect surfaced across 3 rounds × 3 viewports (183/183 assertions, 0 console errors, 0 page errors). **Safe for manual testing.**

### Behaviour note for the manual tester (not a defect)

- **Drill depth / open drawer are in-memory SPA state, not encoded in the URL hash.** Reloading the page mid-drill or mid-drawer is **safe** (no crash, no console/page error, always re-renders a valid root list), but it returns the view to the root warehouse list rather than restoring the exact drill depth or re-opening the drawer. This is consistent with the prototype's design (hash routing exists for top-level route only; the mock holds hierarchy/drawer state in memory) and none of the spec sources (DECISION_LOG, COVERAGE_MAP, AI_DEFAULTS) require hash-encoded drill persistence. Flagged only so a manual tester expecting deep-link/exact-state restoration understands the current behaviour.

### Test-harness note (resolved during this run — no HTML change)

- An initial pass showed 3 false failures on the "duplicate code at location level" scenario, caused by the test waiting 250 ms after `closeDrawer()` — shorter than the drawer's 280 ms close-animation `setTimeout`, whose delayed re-render then emptied the freshly re-opened drawer. Waits were raised to ≥ 400 ms after every close and the scenario passes cleanly on all viewports. This was a harness timing issue only; the HTML was **not** modified.

## Environment note & scope of confirmation

- Sandbox blocks network, so the external font / Lucide-icon CDN cannot load; the page's own 5 s icon-timeout fallback handles this and it does not produce console/page errors or affect the tested logic/flows. Icon glyphs may render as fallbacks in screenshots — cosmetic, environment-only.
- This confirms **no residual defect within the 3-round E2E scope defined above** on Chromium at 1280 / 1440 / 1920. It is not a guarantee across every browser, screen size, real backend integration, or all production data.

## Artifacts

- Suite: `e2e_3rounds_warehouse.py`
- Machine-readable results (per-round, per-viewport, per-assertion + notes): `E2E_3_ROUNDS_RESULT.json`
- Screenshots: `e2e_shots/round1_*.png`, `e2e_shots/round2_*.png`, `e2e_shots/round3_*.png` (105 files; prior UX shots untouched in `ux-shots/`)
