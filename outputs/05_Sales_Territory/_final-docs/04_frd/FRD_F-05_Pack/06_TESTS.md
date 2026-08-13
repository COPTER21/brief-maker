# 06_TESTS — F-05 Sales Territory

> Audience: QA  
> This is FRD-level acceptance coverage; detailed AI-agent cases are generated later by the approved testcase skill.

---

## §6.1 Acceptance Criteria

| AC | Given / When / Then | Trace |
|---|---|---|
| AC-01 | Given authorized user and Routes, when opening `#/sales-territory`, then one page shows tabs `โครงสร้างเขต`, `ภาระงาน`, `แผนที่` and the structure list. | US-06 · API-01 · FN-01 |
| AC-02 | Given an existing Route, when clicking its row, then view drawer shows owned fields read-only and footer `ปิด`. | US-02 · API-02 · FN-02 |
| AC-03 | Given valid required input, when clicking `ยืนยันสร้าง`, then one Active Route and one audit record commit and UI shows `สร้างเขตสำเร็จ`. | US-01 · API-03 · FN-04/08 |
| AC-04 | Given duplicate/invalid/missing required, when create is submitted, then no record commits and UI preserves drawer with `กรุณากรอกข้อมูลให้ครบถ้วน` where that generic validation applies; blank province remains valid and does not increment province KPI. | BR-04/06 · EC-01/02 |
| AC-05 | Given existing Route, when mutable fields are saved through `บันทึกการแก้ไข`, then version increments, audit before/after is appended and UI shows `บันทึกการแก้ไขแล้ว`. | US-03 · API-04 · FN-05/08 |
| AC-06 | Given edit mode, when route code is inspected/changed, then field is locked and server rejects any attempted mutation. | BR-05 |
| AC-07 | Given Active Route, when modal `เก็บ Route เข้าคลัง` is confirmed with `เก็บเข้าคลัง`, then status becomes archived, no delete occurs, audit appends and toast matches `เก็บ Route {code} เข้าคลังแล้ว`. | US-04 · API-05 · FN-06/08 |
| AC-08 | Given Archived Route without conflict, when restore is invoked, then status becomes active, audit appends and toast matches `กู้คืน Route {code} แล้ว`. | US-05 · API-06 · FN-07/08 |
| AC-09 | Given search/filter has no rows, when list resolves, then exact UI is `ไม่พบ Route` / `ลองเปลี่ยนคำค้นหรือตัวกรองสถานะ` / `ล้างตัวกรอง`; reset restores HTML defaults. | US-06 |
| AC-10 | Given future workload providers do not exist, when opening `ภาระงาน`, then visibly mock/unavailable read-only content renders and no provider call blocks core Route operations. | US-07 · BR-11/16/17/20 |
| AC-11 | Given no external network, when opening `แผนที่`, then local map renders; if local asset is corrupt `[AI-DEFAULT]`, map shows contained error while structure remains usable. | US-08 · BR-07/20 |
| AC-12 | Given pointer samples inside valid province/pin and outside all four sides/four corners/side list, when moved, then inside may update matching state but outside causes zero new hover/tooltip/selection/state mutation. | BR-19 · EC-08 |
| AC-13 | Given Salesperson module is absent, when create/edit uses blank or prototype soft ref, then no FK/provider request is required and one Route holds at most one ref. | BR-02/03 · XT-01 |
| AC-14 | Given any Route, when its lifecycle/actions are inspected, then only active/archive/restore exists and there is no approval/DOA endpoint/state/UI. | BR-14 |
| AC-15 | Given overlapping province assignment in baseline, when saved, then F-05 does not enforce overlap `[AI-DEFAULT]`; OQ-09 remains visible. | BR-15 |
| AC-16 | Given two edits with same version, when both commit, then first wins and second receives 409 without lost update `[AI-DEFAULT]`. | PR-2/OQ-16 |
| AC-17 | Given permission revoked after drawer opens, when mutation is submitted, then server returns 403 and no data/audit success record commits `[AI-DEFAULT]`. | PR-3/OQ-17 |
| AC-18 | Given response loss/double-click, when same idempotency key/body retries, then only one mutation/audit occurs; different body returns 409 `[AI-DEFAULT]`. | PR-4/PR-7/OQ-FRD-02 |
| AC-19 | Given archived Route restore would conflict, when restore is submitted, then response 409 and Route remains archived `[AI-DEFAULT]`. | OQ-20 |
| AC-20 | Given 1024×768 and 1440×900, when navigating all surfaces, then no unintended nested Structure scroll, overlay clipping or inaccessible drawer action occurs. | approved regression |

## §6.2 Test Inventory

| TC | Name | Type | AC | Priority |
|---|---|---|---|---|
| TC-UI-01 | one route / three tabs | UI/E2E | 01 | P0 |
| TC-UI-02 | view/create/edit drawers + exact copy | UI/E2E | 02–06 | P0 |
| TC-UI-03 | archive/restore modal and toast | UI/E2E | 07–08 | P0 |
| TC-UI-04 | search/filter/empty/reset | UI/E2E | 09 | P1 |
| TC-UI-05 | mock workload/provider absent | UI/E2E | 10 | P0 |
| TC-MAP-01 | offline asset | UI/E2E | 11 | P1 |
| TC-MAP-02 | inside/outside pointer boundary | UI/E2E | 12 | P0 |
| TC-API-01 | list/detail auth/scope | API | 01–02 | P0 |
| TC-API-02 | create validation/atomic audit | API/DB | 03–04 | P0 |
| TC-API-03 | update immutability/audit | API/DB | 05–06 | P0 |
| TC-API-04 | archive/restore lifecycle | API/DB | 07–08/19 | P0 |
| TC-XT-01 | all future providers absent | integration-negative | 10/13 | P0 |
| TC-CON-01 | stale concurrent edit | concurrency | 16 | P1 |
| TC-PERM-01 | permission revoked mid-flight | security | 17 | P1 |
| TC-IDEM-01 | network retry/double submit | resilience | 18 | P1 |
| TC-RESP-01 | 1024/1440 layout | E2E | 20 | P1 |
| TC-SEC-01 | tenant/role/PII/audit controls | security | all APIs | P0 |
| TC-PERF-01 | 10k fixture/list p95 proposal | performance | OQ-21 | P2 pending approval |

## §6.3 Test Data

- Authorized `sales_admin`, `system_admin`; denied/changed-role actor.
- Active/Archived Routes across regions; one blank province; one blank salesperson; one blank universe.
- Duplicate/invalid code samples and non-integer/negative universe.
- `R-BK-01` only in prototype/test fixture unless OQ-14 approves production seed.
- Local geo asset fixture with all 77 provinces and corrupt/missing variant.
- Do not create actual records/endpoints for the five future features.

## §6.4 Definition of Done

- All P0/P1 accepted-scope tests pass; `[AI-DEFAULT]` cases are implemented only if accepted for the release or retained behind documented OQ decision.
- Mutation API → Function trace and DB transaction/audit integrity verified.
- No hard delete, no approval, no future hard dependency.
- Security/PII/audit checks pass; no sensitive payload in operational logs.
- Approved HTML fidelity holds at 1024 and 1440; console/page errors zero for app code.
- Migrations tested with non-destructive rollback strategy.
- OQ-02/05/07/12/14/15/21 and architecture OQs resolved before relevant freeze/deploy.

## §6.5 Realtime/Notifications

N/A. No WebSocket or business notification event is declared.

## §6.6 Performance and Reliability

| Measure | Proposed target | Status |
|---|---|---|
| list/search p95 | ≤2s | `[AI-DEFAULT]` OQ-21 |
| valid mutation p95 | ≤2s | `[AI-DEFAULT]` OQ-21 |
| accepted invalid/duplicate | 0 | fixed integrity |
| hard delete | 0 | fixed integrity |
| historical snapshot mutation | 0 | fixed integrity |

## §6.7 AC → Logic Coverage

| Functions | Covered by |
|---|---|
| FN-01 | AC-01/09 |
| FN-02 | AC-02 |
| FN-03 | AC-04/06 |
| FN-04 | AC-03/18 |
| FN-05 | AC-05/06/16–18 |
| FN-06 | AC-07/16–18 |
| FN-07 | AC-08/16–19 |
| FN-08 | AC-03/05/07/08/18 |

No engine exists.

## §6.8 Rule/Edge Coverage

- BR-ST-01–20 each map in `00_OVERVIEW §0.12` and §6.1.
- EC-01–10 map to AC-04/07/08/10–13 and XT suite.
- Probe defaults map to AC-16–19 and remain visibly `[AI-DEFAULT]`.

## §6.9 Cross-Module Safeguard Cases

These verify absence/readiness; they do not assume target modules exist.

| ID | Scenario | Future module | Expected now |
|---|---|---|---|
| XT-01 | Salesperson provider absent/inactive unknown | Sales Team/Salesperson | core Route works with nullable/soft ref; no call; inactive policy OQ-03 |
| XT-02 | Customer provider absent while archive | Customer Master | archive can proceed with generic warning; no call/hard dependency |
| XT-03 | Workload metrics requested | Sales Order/Customer/Target | labelled mock/unavailable; no production metric claim |
| XT-04 | Visit hook clicked | Visit Operation | existing future warning/disabled behavior; no navigation/API call |
| XT-05 | Route updated/archived after future transaction snapshot fixture exists | all future consumers | stored snapshot values remain unchanged; archived Route excluded from new choices only after consumer contract exists |

## §6.10 Microcopy Spot Check (HTML verbatim)

| Anchor | Expected exact text |
|---|---|
| create button | `สร้างเขต` |
| validation toast | `กรุณากรอกข้อมูลให้ครบถ้วน` |
| submit state | `กำลังบันทึก…` |
| create success | `สร้างเขตสำเร็จ` |
| edit success | `บันทึกการแก้ไขแล้ว` |
| archive title/button | `เก็บ Route เข้าคลัง` / `เก็บเข้าคลัง` |
| empty state | `ไม่พบ Route` / `ลองเปลี่ยนคำค้นหรือตัวกรองสถานะ` / `ล้างตัวกรอง` |

## §6.11 Phase 3.5 Verification Report — A–M

### A. Pack Completeness — PASS

- STANDARD selection documented; 7/7 expected files present.
- `03_LOGIC.md` mandatory file present; INDEX/07 are not STANDARD files.

### B. Function/API Coverage — PASS

- Mutation API-03/04/05/06 contract blocks include auth, request, response, errors, side effects and logic calls.

### C. R8 Logic Traceability — PASS

- Every mutation traces to ≥1 function.
- FN-01–FN-08 are all traced directly or through FN-04–07; no engine/orphan.

### D. API ↔ DB — PASS

- API-01–06 read/write `T_sales_territory_route`; mutations append `T_sales_territory_audit`; idempotency uses documented platform/shared table `[AI-DEFAULT]`.

### E. UI ↔ API — PASS

- Structure list/detail/create/edit/archive/restore map to API-01–06. Workload/map/future hooks intentionally have no current provider API.

### F. Engine Iron Rules — PASS/N/A

- No engine. UI never calls Function/Engine directly.

### G. Logic Placement — PASS

- HTTP-only contract in 02; CRUD/state/audit functions in 03; constants/rules/errors in 05; no production mock calculation promoted.

### H. Security — PASS WITH OQ

- Auth, role, PII, audit, asset integrity applied. Tenant context/retention remain explicit OQs, not invented facts.

### I. Conventions — PASS

- plural versioned paths; snake_case fields; camelCase functions; UPPER_SNAKE errors; snake_case states.

### J. Data Classification — PASS

- Every §4.2 column has Classification + PII; §4.5 has classification; §4.6.1–.6 complete; highest=Confidential; D-CLASS present; Public not inferred; no Restricted field.

### K. Coverage Manifest — PASS

- Stories 9/9, rules 20/20, confirmed source edges 9/9 mapped; no empty destination.

### L. Scope Lock + Value Stream — PASS

- LOCK-01–10 imported in STANDARD overview; no contradiction.
- Future declarations cover all downstreams without claiming availability; XT-01–05 cover provider absence, archive and immutable snapshot semantics.

### M. HTML Alignment — PASS

- Page/route: 1/1, `#/sales-territory`; no invented route.
- Observed pattern spot checks: structure list (A), create/edit + view drawers (B/C), archive modal (D), shell (N), workload/map read surfaces (J-style) with HTML selectors/functions cited.
- Verbatim UI copy spot checks: 7 rows above (more than minimum 5).

### Verdict

**PASS — FRD pack mechanically complete.** Warnings are deliberate upstream `[AI-DEFAULT]`/OQ items, not undocumented drift. Dev must not convert mock/future declarations into live dependencies or unapproved business rules.

