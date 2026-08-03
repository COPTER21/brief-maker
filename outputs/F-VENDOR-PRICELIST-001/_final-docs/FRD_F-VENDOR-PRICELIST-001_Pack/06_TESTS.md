# 06_TESTS — F-VENDOR-PRICELIST-001 Vendor Price List

> **Audience:** QA engineer / Developer  
> **Purpose:** acceptance bar, trace coverage and cross-module verification. Detailed human/AI steps are generated later by `ai-testcase-md-generator`.

---

## §6.1 Acceptance Criteria

### AC-01 List, filter and vendor drill-in

Given mixed records, when user searches by full vendor/product code or name and filters status, then only matching records appear; flat table shows full vendor and product codes; vendor view/drill-in contains only that Vendor UUID.

### AC-02 Create draft from list/vendor context

Given active vendor and active+purchasable product, when Maker selects master dropdown values, valid Purchase UOM, fills valid price/reason and saves draft, then one Header/v1 draft is stored. From vendor route, vendor is preselected/locked.

### AC-03 Submit new price

Given valid draft, when Maker presses `ยืนยันและส่งอนุมัติ`, then status becomes `pending_approval`, current DOA route/config/SLA are snapshotted, price is not resolvable, audit/event exists and UI shows `รออนุมัติ`.

### AC-04 Threshold behavior

Given changes below, equal to and above current threshold, when submitted, then all become pending_approval; threshold only changes normal/elevated approval path. No path applies immediately.

### AC-05 Approval and SoD

Given pending version, when a different current DOA approver approves, then it becomes active/effective per date and history is appended. Same requester attempting approve is blocked with no state change.

### AC-06 Reject and edit

Given pending version, reject without reason is blocked. With reason, UI returns to draft, rejection stays in immutable history and Maker can edit draft identity/price then resubmit.

### AC-07 New version and immutable identity

Given Active Header, editing creates a new Price Version with vendor/product/UOM/currency locked. Changing UOM/currency uses `สร้างรายการใหม่จากรายการนี้` and creates a different Header; old Active data remains unchanged.

### AC-08 Batch validation

Given multiple rows, blank rows are ignored, invalid started rows show row errors and block submit, add/remove row works, Vendor/Product are search dropdowns and UOM follows Product Master.

### AC-09 Batch success

Given all batch rows valid, when submitted once or safely retried, then each accepted row is created exactly once as pending_approval, UI returns to `#/vendor-price-list` and shows those rows as `รออนุมัติ`.

### AC-10 Import preview

Given UTF-8 CSV, when selected, then UI shows filename, counts, master/UOM checks and preview before enabling `ยืนยันนำเข้า`. Unsupported/schema-invalid file cannot commit.

### AC-11 Import commit/modes

Given valid preview token, commit reports added/updated/skipped/failed counts; new/updated rows are pending_approval. Identical stable external ID is idempotently skipped; replace-unused does not overwrite Active/used rows.

### AC-12 Compare

Given product/qty/date and valid FX, pressing `คำนวณ` returns only eligible active vendor/product/VPL candidates sorted landed THB low→high. First row is marked best. Changing inputs without calculate marks result stale and does not silently recalculate.

### AC-13 Resolve and snapshot

Given explicit vendor and a single applicable Active price, resolve returns that version/tier and complete calculation snapshot. It never chooses another vendor. PR/RFQ/PO storing the snapshot is unaffected by later VPL changes.

### AC-14 Confidential masking

Given role without pricing scope, list/detail/export/log contain no raw price/discount/freight/landed/FX/change values; visible UI uses masked representation. Permitted procurement/finance roles see values.

### AC-15 Deactivate/reactivate

Deactivate removes Header from resolve/compare but preserves detail/history. Reactivate works only after live Vendor/Product/UOM/overlap validation and then returns to Active.

### AC-16 Concurrency/idempotency

Concurrent update/approval: first valid commit wins; second receives 409. Same idempotency key/body returns same result without duplicate Header/Version/history; different body conflicts.

## §6.2 Test Inventory

| TC ID | Name | Type | Maps | Priority |
|---|---|---|---|---|
| TC-UI-01 | List/search/filter/full codes | UI/E2E | AC-01 | P0 |
| TC-UI-02 | Vendor view and drill-in lock | UI/E2E | AC-01/02 | P1 |
| TC-CRT-01 | Create valid draft | API+E2E | AC-02 | P0 |
| TC-CRT-02 | Duplicate Header | negative | BR-01/EC-01 | P0 |
| TC-MST-01 | Vendor non-active at selection/submit | integration | BR-02/EC-02 | P0 |
| TC-MST-02 | Product non-purchasable/UOM invalid | integration | BR-03/06 | P0 |
| TC-SUB-01 | Submit valid draft pending | API+E2E | AC-03 | P0 |
| TC-DOA-01 | Below/equal/above threshold all pending | integration | AC-04 | P0 |
| TC-APR-01 | Different approver approves | API+E2E | AC-05 | P0 |
| TC-APR-02 | Maker self-approval blocked | security | AC-05/EC-08 | P0 |
| TC-APR-03 | Reject reason required and retained | E2E | AC-06 | P0 |
| TC-VER-01 | Active → new version, identity locked | E2E | AC-07 | P0 |
| TC-VER-02 | Clone with changed UOM/currency creates Header | E2E/API | AC-07 | P1 |
| TC-BAT-01 | Blank/invalid/add/remove rows | E2E | AC-08 | P0 |
| TC-BAT-02 | Batch success returns list pending | E2E/API | AC-09 | P0 |
| TC-BAT-03 | Commit-time master drift is atomic | integration | EC-02/PR-5 | P0 |
| TC-IMP-01 | CSV preview and confirm gating | E2E | AC-10 | P0 |
| TC-IMP-02 | unmatched master/schema/encoding | negative | EC-06 | P1 |
| TC-IMP-03 | merge/replace-unused/external ID retry | integration | AC-11 | P0 |
| TC-CMP-01 | compare explicit calculate + ascending rank | E2E/API | AC-12 | P0 |
| TC-CMP-02 | qty selects correct tier | engine/API | BR-08/15 | P0 |
| TC-CMP-03 | missing/stale FX explicit failure | integration | EC-10 | P0 |
| TC-RES-01 | explicit vendor resolve + snapshot | API | AC-13 | P0 |
| TC-RES-02 | no applicable/ambiguous price | engine/API negative | EC-14/BR-19 | P0 |
| TC-CLS-01 | unauthorized UI/API/export/log mask | security | AC-14/EC-15/16 | P0 |
| TC-STA-01 | deactivate excludes; reactivate validates | E2E/API | AC-15 | P0 |
| TC-CC-01 | concurrent draft update | API concurrency | AC-16/EC-11 | P1 |
| TC-CC-02 | concurrent approval | API concurrency | AC-16/EC-11 | P0 |
| TC-ID-01 | mutation safe retry | API | AC-16 | P0 |
| TC-A11Y-01 | keyboard/focus/Escape/search dropdown | accessibility | UI §1.7 | P1 |
| TC-PERF-01 | list/compare/resolve benchmarks | performance | §6.6 | P1 |

## §6.3 Test Data

- Two tenants and two companies; verify no cross-scope results.
- Vendors from canonical F-VENDOR fixtures: active plus each non-active lifecycle state; currencies THB/USD.
- Products from Product Master: active+purchasable with multiple buy UOM, active non-purchasable, obsolete/discontinued; VAT7/EXEMPT.
- VPL records in draft/pending/active/inactive, flat/tier, finite/open-ended validity, one pending-per-header case.
- FX: valid dated, missing and stale beyond policy.
- Roles: Maker, different normal/elevated approvers, same-person approver attempt, finance viewer, masked viewer, scoped service.
- CSV: valid UTF-8, unmatched code, duplicate external ID same/different content, invalid encoding/header, formula-like cell text.

## §6.4 Definition of Done

### Code / Data

- [ ] All P0/P1 tests pass; no P0/P1 bugs open.
- [ ] Unit coverage ≥80% for FN-04..13, FN-18/19 and ENG-01/02; branch coverage includes every error code.
- [ ] API/DB integration, RLS, unique null-site behavior, WORM trigger and migration rollback pass.
- [ ] No raw Confidential price in unauthorized payload, browser DOM, export, application log or analytics event.
- [ ] Idempotency, If-Match and concurrent approval tests pass.

### UI

- [ ] Routes/surfaces/actions and visible anchors match `vendor-price-list-v6.html`.
- [ ] Master choices are searchable dropdowns; full codes visible; locked fields explain the lock.
- [ ] Batch/import/compare flows reach documented final state.
- [ ] Keyboard, focus trap/restore, Escape chain and WCAG AA verified.

### Governance / Deployment

- [ ] DOA config and SLA integrated; no local 10% constant in production logic.
- [ ] ENG-01/02 registered or implementation decision recorded by Architect.
- [ ] Monitoring for pending SLA, failed resolve, FX failures and anomalous price change enabled.
- [ ] Feature flag/rollback plan and production data migration (if any) approved.

## §6.5 Event Verification

Test submitted/approved/rejected/availability events for exact tenant, IDs, actor/time and one delivery outcome under retry. Consumers must be idempotent; event payload must not leak raw pricing unless explicitly scoped.

## §6.6 Performance Benchmarks

Targets are service SLO candidates and must be confirmed against platform baseline before release:

| Operation | Dataset | P95 target |
|---|---:|---:|
| List/filter | 100k Headers/tenant, page 20 | <500ms |
| Detail | 20 versions × 10 tiers | <300ms |
| Resolve | indexed warm path | <200ms |
| Compare | 100 eligible vendors | <800ms |
| Batch validate/commit | configured max rows | <5s async threshold; show progress if longer |

No test may hardcode batch max; read it from refs/platform config.

## §6.7 Environment Notes

- Use actual canonical Vendor/Product contracts or deterministic contract mocks built from their FRD schemas.
- Freeze DOA/FX clocks and config versions for deterministic tests.
- Validate both authorized and masked responses.
- Browser matrix for implementation release follows product policy. The current HTML is a reference prototype; exhaustive cross-browser prototype audit was explicitly cancelled and is not evidence of production readiness.

## §6.8 AC → Logic Coverage

| AC | APIs | Functions | Engines |
|---|---|---|---|
| 01 | 01,02,15 | FN-01,02,14 | — |
| 02 | 03,04 | FN-03,04,17 | ENG-01 |
| 03/04 | 05,16 | FN-05,12,15 | ENG-01 |
| 05/06 | 06 | FN-06,12 | ENG-01 |
| 07 | 07 | FN-07,04,05 | ENG-01 |
| 08/09 | 09,10 | FN-08,09,05 | ENG-01 |
| 10/11 | 11,12,17 | FN-10,11,16,08,09 | ENG-01 |
| 12 | 13 | FN-18 | ENG-02→01 |
| 13 | 14 | FN-19 | ENG-02→01 |
| 14 | all reads/exports | FN-01,02,14 | — |
| 15 | 08 | FN-13 | — |
| 16 | all mutations | FN-03,05,06,07,09,11,13,17 | ENG-01 |

Coverage: Functions 19/19 and Engines 2/2 have at least one AC/test path.

## §6.9 Cross-Module Tests

| ID | Scenario | Expected |
|---|---|---|
| XT-01 | Vendor Active → blocked/inactive after picker opened | submit/resolve/compare recheck and exclude; history remains |
| XT-02 | Product Active/purchasable → obsolete or purchasable=false | new mutation/resolve/compare blocked; historical snapshot readable |
| XT-03 | F-VENDOR API-20 summary | façade matches VPL API-15 counts and stores no duplicated price rows |
| XT-04 | DOA threshold config changes after pending submit | pending request uses auditable submit-time snapshot; no silent route rewrite |
| XT-05 | FX missing/stale | compare/resolve shows explicit failure; no fallback |
| XT-06 | PR/RFQ/PO created from resolved price, VPL changes later | transaction retains original version and calculation snapshot |
| XT-07 | Approved Contract candidate exists | source precedence selects Contract; VPL remains visible as lower-priority evidence |

## §6.10 Microcopy-Aware Expected Text

Detailed tests must use visible HTML anchors, including `สร้างรายการราคา`, `บันทึกร่าง`, `ยืนยันและส่งอนุมัติ`, `รออนุมัติ`, `ตรวจสอบและส่งอนุมัติ`, `ยืนยันนำเข้า`, `คำนวณ`, `อนุมัติราคาฉบับนี้หรือไม่?`, `ปฏิเสธราคาฉบับนี้หรือไม่?`, `ปิดใช้งานรายการราคา?`, `เปิดใช้งานรายการราคา?` and current toast text. If HTML wording changes, regenerate downstream test documents instead of hardcoding stale copy.
