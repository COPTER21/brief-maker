# 06_TESTS — F-LOCATION-MASTER-001 Warehouse & Bin

## §6.1 Acceptance Criteria

### AC-01 Hierarchy drill
Given valid hierarchy, when API-01/API-02 or row/breadcrumb selection runs, then children/path follow Warehouse › Zone › Area › Rack › Location and never cross tenant.

### AC-02 Location flat list
Given mixed Locations, when search/type/status filters run, then only matches appear under `Location ทั้งหมด (ทุกคลัง · ข้ามชั้น)`; no match renders `ไม่พบรายการ`.

### AC-03 Create valid Location
Given Rack parent, unique code and valid fields, when user presses `ยืนยันสร้าง`, then API-14 returns 201, status active, one Location and one audit exist.

### AC-04 Direct Area guard
Given Area `allows_direct=false`, when continuing Location wizard, then no create occurs and UI shows `Area นี้ไม่อนุญาตวางตำแหน่งตรง — เพิ่ม Rack ก่อน`.

### AC-05 Status reason/audit
Given active Location, when `บล็อก` or Freeze is confirmed with reason, then status/reason/version and WORM audit update atomically; empty reason shows `กรอกเหตุผลก่อน`.

### AC-06 Bulk storage UOM
Given selected Locations with mixed `hasStock`, when user selects UOM and presses `ใช้`, then no-stock records update, stocked records skip with counts, and each update has audit.

### AC-07 Atomic bulk generation
Given a valid template, when API-17 commits, then all previewed Rack/Location records and audits exist; any invalid/duplicate/write failure leaves zero batch records.

### AC-08 Decommission
Given `hasStock=false`, decommission sets terminal status and appends audit. Given `hasStock=true`, no change occurs and UI shows `ตำแหน่งนี้ยังมีสต็อกอยู่ — ต้องย้ายสต็อกออก (stock=0) ก่อนปลดระวาง`.

### AC-09 Parent CRUD/delete
Parent creates/updates enforce required fields and sibling uniqueness; delete with child returns `BR_PARENT_HAS_CHILDREN` and preserves data.

### AC-10 Branch soft reference
Create picker lists active Branch only; a saved Branch that later becomes inactive remains resolvable; no Company cascade and no `company_id` exist.

### AC-11 Derived full
Only trusted Inventory signal sets `full`; manual attempt is rejected; clear signal restores prior operational state with audit.

### AC-12 Permission/idempotency/concurrency
Read-only users cannot mutate; permission revoked mid-flight is rejected; same request/key creates once; stale version is rejected.

## §6.2 Test Inventory

| ID | Scenario | Type | Priority |
|---|---|---|---|
| TC-HIER-01 | five-level drill/breadcrumb/path/counts | UI/API | P0 |
| TC-HIER-02 | cycle/orphan/cross-tenant rejection | Engine/DB | P0 |
| TC-LIST-01 | search/type/status/empty state | UI/API | P1 |
| TC-LOC-01 | create under Rack | UI/API/DB | P0 |
| TC-LOC-02 | direct Area allowed/blocked | UI/API | P0 |
| TC-STATUS-01 | blocked/frozen reason | UI/API/DB | P0 |
| TC-STATE-02 | derived full and restore | Integration | P0 |
| TC-UOM-01 | mixed-stock bulk UOM | Integration/DB | P0 |
| TC-BULK-01 | valid and rollback batch | Engine/API/DB | P0 |
| TC-DEL-01 | parent child delete race | API/DB | P1 |
| TC-DECOM-01 | stock guard + successful audit | Integration | P0 |
| TC-BRANCH-01 | active-only picker/inactive saved ref | Integration | P0 |
| TC-CC-01 | stale concurrent update | API | P1 |
| TC-PR-01 | permission revoked mid-flight | Security | P0 |
| TC-NF-01 | lost response retry | API | P1 |
| TC-ID-01 | double submit/idempotency | API | P0 |
| TC-TENANT-01 | RLS isolation all tables | Security/DB | P0 |
| TC-AUDIT-01 | every mutation WORM audit | DB | P0 |
| TC-DRIFT-01 | edit Location persists allowed UOM | E2E/API | P0 |
| TC-DRIFT-02 | decommission appends audit | E2E/API | P0 |
| TC-DRIFT-03 | bulk creates full planned set | E2E/API | P0 |

## §6.3 Test Data

- tenant A/B with identically coded hierarchy to verify isolation
- one active and one inactive Branch; Warehouse saved against each
- Area A allows direct; Area B disallows; Rack under each
- Locations across all 10 types and six statuses
- one stocked and one empty Location from Inventory provider
- duplicate/invalid template plus deterministic valid template
- actors with and without `canManage`, plus trusted integration principal

Real endpoint fixtures/tenant IDs: ไม่พบข้อมูลในบทสนทนา; use non-secret test fixtures.

## §6.4 Definition of Done

- [ ] all P0/P1 tests pass; no open P0/P1 defects
- [ ] API/logic/engine/DB integration tests pass and logic coverage ≥80% `[AI-DEFAULT]`
- [ ] tenant RLS, commit-time permission, idempotency and stale-write tests pass
- [ ] all mutations write one immutable audit; guarded failures do not partially mutate
- [ ] migration/rollback rehearsed in staging; type seeds idempotent
- [ ] `ENG-LOC-GEN` / `ENG-HIER-PATH` registration decision completed or explicitly deferred
- [ ] OQ-LOC-01/02/04/05/06/07/08 closed before affected implementation handoff
- [ ] UI E2E passes in Chromium and Firefox using workspace-local Playwright
- [ ] three HTML mock behavior gaps in `00_OVERVIEW §0.9` are covered by production tests

## §6.5 Events

No Notification event or WebSocket contract is declared for this feature: ไม่พบข้อมูลในบทสนทนา. Inventory capacity integration is API-24/contract seam, not a Notification Center event.

## §6.6 Performance Benchmarks

| Operation | Target |
|---|---|
| list/filter/tree | BRD `[AI-DEFAULT]` P95 ≤ 1.5s at expected dataset |
| guarded single mutation | BRD `[AI-DEFAULT]` P95 ≤ 2.0s excluding dependency outage |
| batch | validate against configured maximum; exact size/latency ไม่พบข้อมูลในบทสนทนา |

Run performance tests with realistic hierarchy depth fixed at five and production-like Location count; do not infer throughput from HTML mock.

## §6.7 Environment Notes

- use `.tools/python.cmd` and `.tools/playwright.cmd` per workspace policy
- mock Company/Geo/Inventory contracts deterministically; never put API key, password, token or cookie in fixtures/reports
- current prototype suite: `outputs/06_Warehouse-Bin/02_QC/e2e_warehouse.py`

## §6.8 AC → Logic/Engine Coverage

| AC | APIs | Functions/engines |
|---|---|---|
| AC-01 | 01/02/04 | FN-01/03, ENG-HIER-PATH |
| AC-02 | 03 | FN-02, ENG-HIER-PATH |
| AC-03/04 | 14 | FN-13/14/23 |
| AC-05 | 16/18 | FN-16/17/19/23 |
| AC-06 | 19 | FN-20/23 |
| AC-07 | 17 | FN-14/18/23, ENG-LOC-GEN |
| AC-08 | 20 | FN-21/23 |
| AC-09 | 05..13 | FN-04..12/23 |
| AC-10 | 05/06/22 | FN-04/05/22/23 |
| AC-11 | 24 | FN-16/25/23 |
| AC-12 | all mutations | auth/idempotency + corresponding FN |

FN-24 is covered by dependency tests for API-23; every declared function/engine has at least one test target.

## §6.9 Cross-module Test Cases

| ID | Scenario | Downstream/upstream expected |
|---|---|---|
| XT-01 | Company deactivates saved Branch | Warehouse remains readable; picker excludes Branch for new selection; no cascade |
| XT-02 | Inventory reports stock during single/bulk UOM update | stocked Location unchanged/skipped; no false success; audits only committed changes |
| XT-03 | Inventory reports stock during decommission | Location remains operational and exact stock guard text displays |
| XT-04 | Inventory changes capacity to full then clears | derived state moves to `full`, then previous state; audit records both |
| XT-05 | node decommissioned after reports reference it | historical reporting still resolves path/status; audit remains |
| XT-06 | Geo service unavailable | Geo cascade fails closed; no local Geo record is invented |

## §6.10 Microcopy-aware Expected Text

Automation must anchor visible text to `warehouse-bin.html`. Required verbatim samples: `Warehouse & Bin`, `Location ทั้งหมด (ทุกคลัง · ข้ามชั้น)`, `ยืนยันสร้าง`, `บันทึกการแก้ไข`, `ไม่พบรายการ`, `กรอกเหตุผลก่อน`, `template ไม่ถูกต้อง`, and the full stocked-decommission text in AC-08.
