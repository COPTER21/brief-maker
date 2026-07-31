# 06_TESTS — F-VENDOR ทะเบียนคู่ค้า

> **Audience:** QA, FE/BE developer  
> **Purpose:** Acceptance bar ของ FRD; test case แบบลงรายละเอียดทุก step จะสร้างต่อด้วย `ai-testcase-md-generator`

---

## §6.1 Acceptance Criteria

### AC-01: List/search/filter

**Given** authenticated user in tenant A  
**When** open `#/vendors`, search/filter/sort/page  
**Then** UI shows only matching tenant A vendors, count/pagination remain consistent  
**And** restricted values are masked by role

### AC-02: Create draft

**Given** Procurement opens `เพิ่มคู่ค้า` and enters legal name  
**When** click `บันทึกร่าง`  
**Then** API-04 returns 201, status `draft`, unique vendor code and audit event  
**And** retry with same idempotency key creates no duplicate

### AC-03: Duplicate/invalid tax ID

**Given** non-OT vendor with invalid checksum or duplicate normalized tax ID in same tenant/country  
**When** save/submit  
**Then** request is blocked with field/business error and no partial child records

### AC-04: One-time vendor without tax ID

**Given** `vendor_type=OT` and other required data valid  
**When** save and view detail  
**Then** tax ID may be null and UI shows `ยกเว้น (One-time)`  
**And** KYC/Policy approval is still required

### AC-05: Address and bank collection safety

**Given** form has multiple addresses/banks  
**When** remove any unverified bank or draft address, including first item  
**Then** selected item is removed  
**And** removing designated billing/shipping clears the role and save is blocked until explicit replacement  
**And** persisted address of active vendor is soft-disabled, not deleted

### AC-06: Submit KYC

**Given** valid vendor draft  
**When** Procurement clicks `บันทึก + ส่ง KYC` or submits existing draft  
**Then** status becomes `pending_kyc`, KYC `pending`, event/audit written once

### AC-07: KYC pass/fail normal

**Given** Compliance opens `ตรวจ KYC (Compliance)` with current version  
**When** pass with no sanctions hit  
**Then** KYC becomes `passed` and vendor remains ready for explicit approval submission  
**When** fail  
**Then** `รายละเอียดผลการตรวจ` is required, result/audit is stored, and vendor remains/returns `pending_kyc` for correction

### AC-08: Sanctions hit

**Given** checkbox `ผลการคัดกรองพบข้อมูลตรงกับรายชื่อเฝ้าระวัง` checked  
**Then** UI shows `ไม่สามารถให้ผ่าน KYC ได้`, disables `ผ่าน KYC`, and requires source+note  
**When** click `ไม่ผ่านและบล็อกคู่ค้า` with valid evidence  
**Then** KYC failed, vendor blocked, source/note/reviewer/time recorded atomically

### AC-09: Approval readiness and Policy Center

**Given** vendor KYC passed, valid contact, required verified bank and address roles  
**When** Procurement submits approval  
**Then** Vendor calls Policy Center, snapshots returned chain, sets `pending_approval`  
**And** Vendor does not calculate credit thresholds or OT auto-approve  
**Given** any prerequisite missing, **Then** request returns corresponding 422 and status is unchanged

### AC-10: Multi-step approval and SoD

**Given** pending approval with current required role  
**When** correct non-maker approves  
**Then** current step approved and next step/final activation is correct  
**And** maker, wrong role or stale concurrent request is rejected without double audit

### AC-11: Reject/resubmit

**Given** one or more approval steps exist  
**When** current approver selects `ตีกลับคู่ค้า` with reason  
**Then** vendor becomes `pending_kyc`, current round closes, remaining steps cancel  
**When** submitted again, a new Policy Center decision/round is created

### AC-12: Bank verification

**Given** Finance views unverified account  
**When** `ส่งตรวจ` then `ยืนยันผล`  
**Then** state becomes verified, identity fields read-only, audit recorded  
**When** `ปิดใช้บัญชี` with reason  
**Then** row remains historical and payment eligibility recalculates

### AC-13: Block/unblock/inactive

**Given** active vendor  
**When** authorized user blocks/deactivates with reason  
**Then** new transaction eligibility is false and historical vendor ID remains  
**When** valid blocked vendor is unblocked  
**Then** it returns active only if KYC/policy prerequisites remain valid

### AC-14: Blacklist terminal

**Given** authorized Director/Admin blacklists with reason  
**Then** status is `blacklisted`, transaction eligibility false  
**And** no UI/API transition back is available

### AC-15: Role-based masking and tenant isolation

**Given** Viewer/Procurement/Compliance/Finance/Admin roles  
**When** list/detail endpoints are read  
**Then** tax, bank, credit and KYC fields follow matrix in §5.3  
**And** each unmasked sensitive view is audited  
**And** cross-tenant ID never returns another tenant’s data

### AC-16: Tax immutability

**Given** vendor KYC passed  
**When** user attempts UI or direct API tax ID change  
**Then** UI is locked and server returns `BR_TAX_ID_IMMUTABLE`

### AC-17: Attachment security

**Given** allowed clean file and valid metadata  
**When** attach  
**Then** private metadata is created and UI lists it  
**Given** disallowed/malicious/duplicate file, **Then** no active attachment is created

### AC-18: Concurrency and retry

**Given** two users edit/approve the same version  
**When** both mutate  
**Then** first commit wins, second receives 409  
**And** retry with same Idempotency-Key returns original response without duplicate state/audit

### AC-19: Audit atomicity

**Given** audit/outbox persistence fails  
**When** any state mutation is attempted  
**Then** business mutation rolls back and error is observable  
**And** secrets/full Restricted values are absent from application logs

### AC-20: Reference and downstream failure

**Given** Policy Center unavailable  
**When** submit approval  
**Then** vendor stays prior state and no fallback chain is created  
**Given** Price List unavailable, **Then** UI/API shows explicit unavailable state, not fabricated summary

## §6.2 Test Inventory

| Test ID | Scenario | Type | Priority | Maps |
|---|---|---|---|---|
| TC-VEN-001 | list/search/filter/page | UI/API | P0 | AC-01 |
| TC-VEN-002 | create draft + idempotent replay | UI/API | P0 | AC-02 |
| TC-VEN-003 | tax format/duplicate | negative | P0 | AC-03 |
| TC-VEN-004 | OT without tax | edge | P0 | AC-04 |
| TC-VEN-005 | remove first/all bank/address | UI state | P0 | AC-05 |
| TC-VEN-006 | designated address replacement | UI/API | P0 | AC-05 |
| TC-VEN-007 | submit KYC | workflow | P0 | AC-06 |
| TC-VEN-008 | KYC normal pass/fail | permission/workflow | P0 | AC-07 |
| TC-VEN-009 | sanctions hit forced block | security/workflow | P0 | AC-08 |
| TC-VEN-010 | approval readiness failures | negative | P0 | AC-09 |
| TC-VEN-011 | Policy chain includes OT | integration | P0 | AC-09 |
| TC-VEN-012 | multi-step approval | workflow | P0 | AC-10 |
| TC-VEN-013 | SoD/wrong role/concurrent approval | security/concurrency | P0 | AC-10 |
| TC-VEN-014 | reject after partial approval + resubmit | workflow | P0 | AC-11 |
| TC-VEN-015 | bank submit/verify/deactivate | permission/workflow | P0 | AC-12 |
| TC-VEN-016 | block/unblock/deactivate | workflow | P0 | AC-13 |
| TC-VEN-017 | blacklist terminal | security/workflow | P0 | AC-14 |
| TC-VEN-018 | field masking by role | security/UI | P0 | AC-15 |
| TC-VEN-019 | tenant isolation | security/API | P0 | AC-15 |
| TC-VEN-020 | tax immutable after KYC | negative | P0 | AC-16 |
| TC-VEN-021 | attachment allowlist/scan/remove | security | P1 | AC-17 |
| TC-VEN-022 | stale aggregate update | concurrency | P0 | AC-18 |
| TC-VEN-023 | lost response/retry | resilience | P1 | AC-18 |
| TC-VEN-024 | audit/outbox failure rollback | resilience | P0 | AC-19 |
| TC-VEN-025 | Policy/Price List failure | integration | P1 | AC-20 |
| TC-VEN-026 | keyboard/focus/Esc chain | accessibility | P1 | UI §1.10 |
| TC-VEN-027 | XSS in name/reason/note/filename | security | P0 | §5.7 |
| TC-VEN-028 | large list/filter performance | performance | P1 | §6.6 |

## §6.3 Test Data

### Tenants and roles

- tenant A and B with similarly named vendors for isolation tests
- accounts: officer, manager, director, compliance, finance, admin, viewer
- maker and approver are different users; add one user with role revoked mid-test

### Vendor fixtures

- one record per lifecycle state
- TH vendor with valid/invalid/duplicate tax IDs
- OT without tax ID/bank
- non-OT with no bank, unverified bank, verified bank, and disabled last bank
- vendor with two addresses where billing/shipping roles are on same/different rows
- multi-step Policy chain and partially approved round
- sanctions-hit cases for OFAC, UN, EU, OTHER
- clean, duplicate, oversize, disallowed and malware-test attachments

No production PII/bank values are permitted in test data.

## §6.4 Definition of Done

### Functional

- [ ] AC-01..AC-20 pass
- [ ] all P0/P1 tests pass; no open P0/P1 defects
- [ ] state machine and permission matrix have automated coverage
- [ ] HTML behavior and implementation do not drift on route, action visibility or microcopy anchors

### Architecture/Data

- [ ] every mutation API traces to a function/engine
- [ ] migrations, constraints, RLS and indexes pass staging verification
- [ ] audit/outbox atomicity and retention controls verified
- [ ] CUBIC candidates reviewed/registered or approved as scope-local
- [ ] E-002 and E-007 contracts pass consumer tests

### Security/Quality

- [ ] tenant, RBAC, SoD, masking, encryption and sensitive-view audit verified
- [ ] attachment scanning and private access verified
- [ ] dependency/security scan has no unresolved high/critical issue
- [ ] accessibility keyboard/focus/labels meet WCAG 2.1 AA target
- [ ] observability includes correlation id, mutation failure and integration health without PII

### Documentation

- [ ] FRD Pack approved
- [ ] `html-ui-brief` generated from the same approved HTML
- [ ] AI testcase MD and QA-friendly HTML trace the final pack

## §6.5 Events

| Event | Trigger | Consumer expectation |
|---|---|---|
| `vendor_created_event` | create commit | idempotent by event id |
| `vendor_kyc_submitted_event` | pending_kyc | Compliance notification |
| `vendor_kyc_decided_event` | KYC pass/fail | Procurement notification |
| `vendor_approval_submitted_event` | chain snapshot commit | current approver notified |
| `vendor_approval_decided_event` | approve/reject | maker/next approver notified |
| `vendor_status_changed_event` | active/block/unblock/inactive/blacklist | PO/Price List/PV refresh eligibility |
| `vendor_payment_eligibility_changed_event` | verified bank changes | Payment/PV invalidate cache |

Test duplicate/out-of-order delivery: consumers use event id + vendor version and do not regress state.

## §6.6 Performance and Reliability Baseline

Final SLO ต้องยืนยันกับ platform owner; initial acceptance `[AI-DEFAULT]`:

| Operation | Initial target |
|---|---|
| vendor list/detail | p95 ≤ 500 ms at agreed staging dataset |
| local mutation excluding external screening | p95 ≤ 1 s |
| transaction eligibility | p95 ≤ 200 ms |
| concurrent approval | exactly one valid state commit |
| retry | no duplicate record/step/audit |

Policy/sanctions/storage latency is measured separately and must have timeout/circuit-breaker telemetry.

## §6.7 AC → Logic Coverage

| AC | APIs | Functions/Engines |
|---|---|---|
| AC-01/15 | API-01/03 | FN-01 |
| AC-02/03/04 | API-04 | FN-03/FN-05, ENG-02 |
| AC-05/16 | API-05 | FN-04/FN-05 |
| AC-06 | API-06 | FN-06/FN-05 |
| AC-07/08 | API-07 | FN-07 |
| AC-09/20 | API-08 | FN-08, Policy Center |
| AC-10/11 | API-09 | FN-09 |
| AC-12 | API-14/15/16 | FN-11/FN-12/FN-15, ENG-01 |
| AC-13/14 | API-10..13 | FN-10/FN-15, ENG-01 |
| AC-17 | API-17/18 | FN-13/FN-14 |
| AC-18/19 | all mutations | common middleware + relevant FN |
| AC-20 | API-20 | FN-16 |

Coverage: functions 16/16; engines 2/2.

## §6.8 Cross-Module Tests

| ID | Scenario | Downstream | Expected |
|---|---|---|---|
| XT-01 | active vendor opens `สินค้า/บริการ` | F-VENDOR-PRICE-LIST / E-002 | summary belongs to same vendor/tenant; edit unavailable in Vendor |
| XT-02 | PO selects vendor | F-PO / E-007 | only eligibility true vendor selectable; default payment term matches contract |
| XT-03 | last verified bank deactivated | Payment/PV | PO may remain eligible; payment false with reason code |
| XT-04 | active vendor becomes blocked/inactive/blacklisted | PO/PV | new transaction blocked after event/lookup; history remains |
| XT-05 | duplicate/out-of-order status events | all consumers | dedup/version prevents state regression |
| XT-06 | Price List/downstream unavailable | Vendor UI | explicit unavailable/empty contract; no fake data |

## §6.9 Microcopy-Aware Expected Text

These are verbatim anchors from approved `vendor.html`:

| Context | Expected visible text |
|---|---|
| Page | `ทะเบียนคู่ค้า` |
| Subtitle | `จัดการข้อมูลคู่ค้า เอกสาร และสถานะการใช้งานในที่เดียว` |
| Create | `เพิ่มคู่ค้า` / `เพิ่มคู่ค้าใหม่` |
| Empty | `ไม่พบคู่ค้า` |
| Payment section | `เงื่อนไขการชำระเงินเริ่มต้น` |
| Address validation | `กรุณากำหนดที่อยู่ใบกำกับ` |
| Address validation | `กรุณากำหนดที่อยู่จัดส่งหลัก` |
| Address action | `ลบที่อยู่นี้?` / `ปิดใช้ที่อยู่นี้?` |
| Bank actions | `ส่งตรวจ`, `ยืนยันผล`, `ปิดใช้บัญชี` |
| KYC title | `ตรวจ KYC (Compliance)` |
| Sanctions warning | `ไม่สามารถให้ผ่าน KYC ได้` |
| Sanctions fields | `แหล่งข้อมูลที่ตรวจพบ`, `รายละเอียดผลการตรวจ` |
| Sanctions action | `ไม่ผ่านและบล็อกคู่ค้า` |
| Pass action | `ผ่าน KYC` |
| Approval | `อนุมัติคู่ค้า — ขั้น {current}/{total}` |
| Reject | `ตีกลับคู่ค้า` |
| Offboarding | `ปิดใช้งานคู่ค้า` |

Final detailed testcase generator must re-read HTML and central microcopy source; do not copy stale strings from this table if HTML is revised.
