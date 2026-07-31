# 06_TESTS — F-XX [Feature Name]

> **Audience:** QA engineer
> **Purpose:** Acceptance Criteria + Definition of Done + WebSocket events
> **Coverage source:** 02_API contracts + 03_LOGIC functions + 05_RULES edge cases

---

## §6.1 Acceptance Criteria (AC)

ทุก functional requirement ต้องมี AC ที่ test ได้ขัดเจน

### AC-01: List payrolls with filters
**Given** user role = manager and tenant has 5 payroll records
**When** GET /api/v1/payrolls?status=draft
**Then** response 200 with 2 records (status=draft only)
**And** response time < 500ms

### AC-02: Create payroll — happy path
**Given** valid period (unlocked) and active employee
**When** POST /api/v1/payrolls with valid body + Idempotency-Key
**Then** response 201 with new payroll record
**And** status = 'draft'
**And** gross_pay computed correctly by ENG-005
**And** audit log entry created

### AC-03: Create payroll — locked period
**Given** payroll period status = 'locked'
**When** POST /api/v1/payrolls with that period_id
**Then** response 422 with code BR_PAYROLL_PERIOD_LOCKED

### AC-04: Submit for approval
**Given** payroll in status 'draft' with all required fields
**When** POST /api/v1/payrolls/:id/submit
**Then** status = 'submitted'
**And** submitted_at = now()
**And** approver receives in-app notification

### AC-05: Approve — concurrent (EC-01)
**Given** 2 approvers click approve simultaneously
**When** Both requests reach API within 100ms
**Then** First commits successfully (200)
**And** Second receives 409 ERR_STALE_DATA

### AC-06: Idempotency (EC-02)
**Given** Idempotency-Key X with body Y, response cached
**When** Same X + Y resent within 24hr
**Then** Same response returned (no new INSERT)
**And** No duplicate audit log

[Add AC for every FR in 02_API]

---

## §6.2 Test Case Inventory

| TC ID | Name | Type | Maps to AC | Priority |
|---|---|---|---|---|
| TC-01 | List payrolls — happy | API | AC-01 | P0 |
| TC-02 | Create payroll — happy | API | AC-02 | P0 |
| TC-03 | Create — locked period | API negative | AC-03 | P1 |
| TC-04 | Submit for approval | API | AC-04 | P0 |
| TC-CC-01 | Concurrent approval | API stress | AC-05 | P1 |
| TC-ID-01 | Idempotency | API | AC-06 | P0 |
| TC-PR-01 | Permission revoked mid-flight | API | EC-03 | P2 |
| TC-NF-01 | Network failure retry | Integration | EC-04 | P2 |
| TC-PERF-01 | List 1000 records < 1s | Performance | AC-01 | P1 |
| TC-UI-01 | Page renders correctly | UI/E2E | P-01 | P1 |

---

## §6.3 Test Data Setup

### Required test data
- 3 tenants (isolated)
- 10 employees per tenant (mix of active/inactive)
- 3 payroll periods (1 open, 1 locked, 1 historical)
- 5 existing payroll records (mix of statuses)

### Roles for testing
- `qa_manager` (role: manager)
- `qa_approver` (role: approver)
- `qa_finance` (role: finance)
- `qa_employee` (role: employee, scope: own only)

---

## §6.4 Definition of Done (DoD)

ก่อน mark feature = DONE:

### Code
- [ ] All AC implemented + unit tests pass
- [ ] Integration tests pass (API + DB + Engine)
- [ ] E2E tests pass (happy path + critical edge cases)
- [ ] Code review approved
- [ ] No critical/high security findings
- [ ] Test coverage ≥ 80% on logic layer

### Documentation
- [ ] API docs published (auto from 02_API.md)
- [ ] User-facing changelog written
- [ ] FRD §07_LOCKED_DECISIONS reflects final design
- [ ] CUBIC Registry: Engines from §3.2 registered (if FULL variant)

### QA
- [ ] All P0 + P1 test cases pass
- [ ] No P0/P1 bugs open
- [ ] Performance benchmarks met
- [ ] Security checklist (D-domains) verified

### Deployment
- [ ] Migration script tested in staging
- [ ] Feature flag configured (if applicable)
- [ ] Monitoring dashboards updated
- [ ] Rollback plan documented

---

## §6.5 WebSocket Events (if applicable)

### Event: `payroll_submitted`
- **Trigger:** F-XX-API-05 submit succeeds
- **Channel:** `tenant:<tenant_id>:approvers`
- **Payload:**
  ```json
  {
    "event": "payroll_submitted",
    "payload": {
      "payroll_id": "uuid",
      "submitted_by": "uuid",
      "submitted_at": "iso8601"
    }
  }
  ```
- **Test:** Approver dashboard updates without refresh

### Event: `payroll_approved`
- **Trigger:** F-XX-API-06 approve succeeds
- **Channel:** `tenant:<tenant_id>:user:<maker_id>`
- **Test:** Maker sees update + toast notification

---

## §6.6 Performance Benchmarks

| Endpoint | P95 latency | Throughput |
|---|---|---|
| GET /payrolls (list) | < 500ms | 200 req/s |
| GET /payrolls/:id | < 200ms | 500 req/s |
| POST /payrolls | < 1000ms | 50 req/s |
| POST /payrolls/:id/approve | < 800ms | 100 req/s |

---

## §6.7 Test Environment Notes

- Use staging tenant (`tenant-test-001`)
- Mock Omise payment gateway (PR-8 compensation tests)
- Engine ENG-005 in TEST mode (no real tax calc, deterministic mock)
- DB seed script: `seed_payroll_test_data.sql`

---

## §6.8 Trace: AC → Logic Coverage

| AC | API tested | Functions tested | Engines tested |
|---|---|---|---|
| AC-01 | F-XX-API-01 | F-XX-FN-04 | — |
| AC-02 | F-XX-API-02 | F-XX-FN-01, F-XX-FN-03 | ENG-005 |
| AC-03 | F-XX-API-02 | F-XX-FN-03 (negative) | — |
| AC-04 | F-XX-API-05 | F-XX-FN-06 | — |
| AC-05 | F-XX-API-06 | F-XX-FN-07 (concurrent) | — |
| AC-06 | F-XX-API-02 | F-XX-FN-01 (idempotent) | ENG-005 |

> **Coverage check:** ทุก Function/Engine ใน 03_LOGIC §3.1, §3.2 ต้องถูก trace ที่นี่อย่างน้อย 1 AC

---

## §6.9 Cross-Module Test Cases ⭐ v6 (จาก BRD §12.1 Downstream Impact)

> ทุก downstream ที่มี data ไหล ต้องมีอย่างน้อย 1 case — โดยเฉพาะ scenario "แก้/ยกเลิกกลางทาง"

| ID | Scenario | Downstream ที่ตรวจ | Expected |
|---|---|---|---|
| XT-01 | ยกเลิก PR ที่ approved แล้ว | Budget | commitment ถูก release คืน |
| XT-02 | PR approved | PO | สร้าง PO อ้าง PR ได้ + ข้อมูลรายการตรง |

## §6.10 Microcopy-Aware Expected Text ⭐ v6

> Expected text ทุกข้อที่เป็นข้อความ UI: **มี HTML → ยึดข้อความจริงบนจอ (verbatim)** ก่อน แล้ว fallback microcopy กลาง html-generator-v6 — ห้ามแต่งคำเอง
> ตัวอย่าง: toast สร้างสำเร็จ = "สร้าง[entity]สำเร็จ" · ปุ่ม submit = "ยืนยันสร้าง" · ปุ่ม edit = "บันทึกการแก้ไข"
> · confirm ลบ = "ลบ[entity]?" + ปุ่ม "ลบ" (danger) · empty = "ยังไม่มี[entity]"
> ผลลัพธ์: testcase ที่ ai-testcase-md-generator สร้างต่อจะ match หน้าจอจริง 1:1
