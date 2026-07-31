# 05_RULES — F-XX [Feature Name]

> **Audience:** Backend developer + QA
> **Purpose:** Business Rules + Validation + Edge Cases + Errors + Security
> **Principle:** Declarative — อ่านแล้วเข้าใจโดยไม่ต้องดูโค้ด

---

## §5.1 Business Rules (BR)

> Source of Truth สำหรับ constants, thresholds, state machines

### BR-PAY-01: Payroll period must be unlocked
- **Statement:** ห้ามสร้าง/แก้ payroll ใน period ที่ status = 'locked'
- **Enforced by:** F-XX-API-02 precondition + F-XX-FN-01 createPayrollRecord
- **Error:** `BR_PAYROLL_PERIOD_LOCKED` → HTTP 422
- **Rationale:** Locked period = ปิดงบ ห้ามแก้ย้อนหลัง

### BR-PAY-02: Overtime calculation rate
- **Statement:** OT_RATE = 1.5x base hourly rate (default), 2.0x on holidays
- **Used by:** ENG-005 payroll-calculation-engine
- **Configurable:** YES — admin panel, audit logged
- **Effective date:** 2026-01-01

### BR-PAY-03: Maximum overtime hours
- **Statement:** `MAX_OVERTIME_HOURS_PER_MONTH = 36`
- **Enforced by:** F-XX-FN-03 validatePayrollData
- **Error:** `BR_OVERTIME_EXCEEDED` → HTTP 422
- **Rationale:** Thai labor law

### BR-PAY-04: Tax brackets (2026)
- **Statement:**
  - 0 – 150,000 THB: 0%
  - 150,001 – 300,000: 5%
  - 300,001 – 500,000: 10%
  - [...]
- **Used by:** ENG-006 tax-rule-applier
- **Configurable:** YES — finance admin, requires audit

---

## §5.2 State Machine (if has-state)

### Payroll status transitions

```
   ┌───────┐  submit   ┌──────────┐  approve   ┌──────────┐
   │ draft │──────────►│submitted │───────────►│ approved │
   └───┬───┘           └────┬─────┘            └────┬─────┘
       │                    │ reject                │ mark paid
       │ cancel             ▼                       ▼
       │              ┌──────────┐            ┌──────┐
       └─────────────►│cancelled │            │ paid │
                      └──────────┘            └──────┘
```

| From | To | Action | Allowed roles | Conditions |
|---|---|---|---|---|
| draft | submitted | submit | manager | all required fields filled |
| draft | cancelled | cancel | manager, admin | — |
| submitted | approved | approve | approver, admin | — |
| submitted | draft | reject | approver, admin | reject_reason required |
| approved | paid | mark_paid | finance | payment evidence attached |

> Transitions are enforced by F-XX-FN-06 submitOrder, F-XX-FN-07 approveOrder (see 03_LOGIC §3.1)

---

## §5.3 Permission Matrix

| Role | View | Create | Edit | Submit | Approve | Reject | Cancel | Pay |
|---|---|---|---|---|---|---|---|---|
| employee | own only | — | — | — | — | — | — | — |
| manager | all | ✅ | own only | ✅ | — | — | ✅ | — |
| approver | all | — | — | — | ✅ | ✅ | — | — |
| finance | all | — | — | — | — | — | — | ✅ |
| admin | all | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## §5.4 Field Validation Rules

### Per-field declarative rules
| Field | Rule | Error code |
|---|---|---|
| `base_salary` | required, > 0, ≤ 10,000,000 | `BR_SALARY_OUT_OF_RANGE` |
| `period_id` | required, exists in T_payroll_period | `BR_INVALID_PERIOD` |
| `employee_id` | required, employee.is_active = true | `BR_EMPLOYEE_INACTIVE` |
| `deductions[].amount` | ≥ 0 | `BR_NEGATIVE_DEDUCTION` |
| `tax_amount` | computed (not user input) | — |

### Cross-field rules
- `net_pay` MUST equal `gross_pay - tax_amount - sum(deductions)` → enforced by ENG-005
- `submitted_at` ≥ `created_at` → DB constraint
- `approved_at` ≥ `submitted_at` → DB constraint + state machine

---

## §5.5 Edge Cases (from Phase 2.5 Probing)

### EC-01: Concurrent approval (PR-1)
- **Scenario:** 2 approvers approve same payroll simultaneously
- **Resolution:** Optimistic locking via `version` column — first commits wins, second gets 409
- **Error:** `ERR_STALE_DATA`
- **Test:** TC-CC-01 in 06_TESTS

### EC-02: Idempotency (PR-7)
- **Scenario:** User double-clicks submit
- **Resolution:** Idempotency-Key header — second request returns cached response (200, not 201)
- **Cache TTL:** 24 hours
- **Test:** TC-ID-01 in 06_TESTS

### EC-03: Permission revoked mid-edit (PR-3)
- **Scenario:** Manager edits payroll, gets demoted before save
- **Resolution:** Re-check role at mutation time (not GET time)
- **Error:** `ERR_PERMISSION_REVOKED`
- **Test:** TC-PR-01 in 06_TESTS

### EC-04: Network failure during submit (PR-4)
- **Scenario:** Request reaches server, response lost
- **Resolution:** Idempotency-Key + retry logic (3 attempts, exponential backoff)
- **Test:** TC-NF-01 in 06_TESTS

[Add more based on activated probes in Phase 2.5]

---

## §5.6 Error Catalog

| Code | HTTP | Message (i18n key) | Cause |
|---|---|---|---|
| `ERR_VALIDATION_FAILED` | 400 | error.validation.failed | Generic validation |
| `ERR_NOT_AUTHENTICATED` | 401 | error.auth.unauth | No/invalid token |
| `ERR_INSUFFICIENT_ROLE` | 403 | error.auth.role | Role mismatch |
| `ERR_NOT_FOUND` | 404 | error.notfound | Resource missing |
| `ERR_DUPLICATE_IDEMPOTENCY_KEY` | 409 | error.idempotency.dup | Same key, different body |
| `ERR_STALE_DATA` | 409 | error.concurrency.stale | Version mismatch |
| `ERR_PERMISSION_REVOKED` | 403 | error.auth.revoked | Mid-flight role change |
| `BR_PAYROLL_PERIOD_LOCKED` | 422 | br.payroll.period.locked | BR-PAY-01 |
| `BR_OVERTIME_EXCEEDED` | 422 | br.overtime.exceeded | BR-PAY-03 |
| `BR_SALARY_OUT_OF_RANGE` | 422 | br.salary.range | Field validation |
| `ENG_ERR_INVALID_INPUT` | 500 | error.engine.input | ENG-005 input mismatch |
| `ENG_ERR_CALCULATION_FAILED` | 500 | error.engine.calc | ENG-005 internal |

---

## §5.7 Security Bible Application

> Domains triggered for this feature: **D2, D5, D7, D9, D15, D17**

### D2: Authentication & Session
- All endpoints require JWT
- Token TTL: 1 hour
- Refresh token: 7 days

### D5: Financial Transactions
- All amount changes → audit log mandatory (BEFORE + AFTER)
- Approval workflow required for amount > 100,000 THB
- Reconciliation report daily

### D7: PII Protection
- `employee_id` linked to PII — encrypt at rest (column-level)
- API response: NO full PII unless requested + permitted
- Logs: NO PII (use ID references only)

### D-CLASS: Data Classification ⭐ (v5.1)

Per-field classification รายละเอียดอยู่ที่ 04_DB §4.2 + §4.6

**Enforcement summary สำหรับ feature นี้:**

| Layer | Confidential fields | Restricted fields |
|---|---|---|
| API response | `mask if no permission` | excluded จาก response ถ้าไม่ผ่าน ACL |
| UI display | แสดง `***` | hidden + audit log access |
| Export/Print | excluded column ถ้า role ไม่ผ่าน | require Restricted Resources approval |
| Audit | log view + mutation | log view + mutation + export attempts |

**Wire points:**
- Policy Center → Data Classification (master + override UI)
- Policy Center → Restricted Resources (ACL per-record)
- Policy Center → DOA (approval ถ้า downgrade classification)

### D9: Audit Logging
- All mutations → T_audit_log entry
- Retention: 7 years
- Immutable (append-only)

### D15: Admin Actions
- All status transitions logged
- Approver identity recorded
- Reason required for reject/cancel

### D17: Multi-Tenant Isolation
- PostgreSQL RLS enforced
- API middleware validates X-Tenant-Id
- Cross-tenant queries forbidden (DB-level)

---

## §5.8 Compliance & Audit Requirements

| Requirement | Implementation |
|---|---|
| Thai labor law (overtime cap) | BR-PAY-03 |
| Revenue Department reporting | Monthly export (50 ทวิ format) |
| Internal audit | T_audit_log + quarterly review |
| Data privacy (PDPA) | D7 encryption + retention policy |
