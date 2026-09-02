# 02_API — F-XX [Feature Name]

> **Audience:** Backend developer (HTTP layer)
> **Purpose:** API contracts — CUBIC API Entity format
> **🚨 Iron Rule:** ห้ามมี business logic >5 lines ที่นี่ — ย้ายไป 03_LOGIC §3.1
> **🚨 R8:** ทุก mutation API ต้องระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth |
|---|---|---|---|---|
| F-XX-API-01 | GET | /api/v1/payrolls | List payrolls | required |
| F-XX-API-02 | POST | /api/v1/payrolls | Create payroll | required (manager+) |
| F-XX-API-03 | GET | /api/v1/payrolls/:id | Get detail | required |
| F-XX-API-04 | PUT | /api/v1/payrolls/:id | Update | required (manager+) |
| F-XX-API-05 | POST | /api/v1/payrolls/:id/submit | Submit for approval | required (manager) |
| F-XX-API-06 | POST | /api/v1/payrolls/:id/approve | Approve | required (approver) |

---

## §2.2 Per-API Contract

### F-XX-API-01: GET /api/v1/payrolls

| Field | Value |
|---|---|
| **id** | F-XX-API-01 |
| **method** | GET |
| **path** | /api/v1/payrolls |
| **summary** | List payrolls with filters |
| **auth** | required |
| **roles** | manager, finance, employee (own only) |
| **rate-limit** | default (100/min) |

**Request:**
- **Query params:**
  - `status` (optional): draft | submitted | approved
  - `period_id` (optional): uuid
  - `limit` (optional, default 20, max 100)
  - `offset` (optional, default 0)
- **Headers:** `X-Tenant-Id` (required)

**Response 200:**
```json
{
  "data": [
    {
      "id": "uuid",
      "period_id": "uuid",
      "employee_id": "uuid",
      "status": "draft",
      "gross_pay": 50000,
      "net_pay": 42000,
      "created_at": "2026-05-18T10:00:00Z",
      "updated_at": "2026-05-18T10:00:00Z"
    }
  ],
  "total": 150,
  "limit": 20,
  "offset": 0
}
```

**Error Responses:**
- 400: ERR_INVALID_QUERY_PARAMS
- 401: ERR_NOT_AUTHENTICATED
- 403: ERR_INSUFFICIENT_ROLE

**Preconditions:** —
**Side effects:** — (read-only)
**Calls (Logic):** F-XX-FN-04 buildPayrollListQuery → ดู 03_LOGIC §3.1

---

### F-XX-API-02: POST /api/v1/payrolls

| Field | Value |
|---|---|
| **id** | F-XX-API-02 |
| **method** | POST |
| **path** | /api/v1/payrolls |
| **summary** | Create new payroll record |
| **auth** | required |
| **roles** | manager |
| **rate-limit** | default |

**Request:**
- **Headers:**
  - `X-Tenant-Id` (required)
  - `Idempotency-Key` (required) — PR-7 idempotency
- **Body:**
  ```json
  {
    "period_id": "uuid",
    "employee_id": "uuid",
    "base_salary": 50000,
    "deductions": [
      { "type": "social_security", "amount": 750 }
    ]
  }
  ```
- **Validation (field-level, ≤ 5 lines):**
  - `period_id`: required, uuid
  - `employee_id`: required, uuid
  - `base_salary`: required, number, > 0
  - `deductions`: optional, array
  - **Complex validation → 03_LOGIC.md F-XX-FN-03 validatePayrollData**

**Response 201:**
```json
{
  "id": "uuid",
  "status": "draft",
  "gross_pay": 50000,
  "net_pay": 42000,
  "created_at": "2026-05-18T10:00:00Z"
}
```

**Error Responses:**
- 400: ERR_VALIDATION_FAILED
- 403: ERR_INSUFFICIENT_ROLE
- 409: ERR_DUPLICATE_IDEMPOTENCY_KEY
- 422: BR_PAYROLL_PERIOD_LOCKED — ดู 05_RULES BR-PAY-01

**Preconditions:**
- Payroll period exists and not locked
- Employee exists and is active

**Side effects:**
- INSERT T_payroll
- INSERT T_audit_log
- Emit `payroll_created_event`

**Calls (Logic):**
- F-XX-FN-01 createPayrollRecord — ดู 03_LOGIC §3.1
- F-XX-FN-03 validatePayrollData — ดู 03_LOGIC §3.1
- ENG-005 payroll-calculation-engine — ดู 03_LOGIC §3.2

---

[Repeat for each remaining API]

---

## §2.3 Common Concerns

### Idempotency (PR-7)
All mutation APIs (POST/PUT/PATCH/DELETE) accept `Idempotency-Key` header:
- Server caches result for 24 hours
- Same key + same body → return cached response
- Same key + different body → 409 Conflict

### Optimistic Locking (PR-2)
PUT/PATCH endpoints require `If-Match` header with current `updated_at`:
- Match → proceed
- Mismatch → 409 ERR_STALE_DATA

### Multi-Tenant
All endpoints require `X-Tenant-Id` header:
- Auto-applied at middleware
- DB queries filtered via PostgreSQL RLS

### Audit Log
All mutation APIs auto-write to T_audit_log via middleware:
- actor (user_id)
- action (create/update/delete/...)
- resource (T_payroll:<id>)
- timestamp
- diff (before/after JSON)

---

## §2.4 API → Logic Trace (Anchor for R8)

> **Authoritative source:** `03_LOGIC.md §3.3 Trace Table`
> ที่นี่ list summary เท่านั้น

| API | Calls Functions | Calls Engines |
|---|---|---|
| F-XX-API-01 GET /payrolls | F-XX-FN-04 | — |
| F-XX-API-02 POST /payrolls | F-XX-FN-01, F-XX-FN-03 | ENG-005 |
| F-XX-API-03 GET /payrolls/:id | F-XX-FN-04 | — |
| F-XX-API-04 PUT /payrolls/:id | F-XX-FN-05 | ENG-005 |
| F-XX-API-05 POST /payrolls/:id/submit | F-XX-FN-06 | — |
| F-XX-API-06 POST /payrolls/:id/approve | F-XX-FN-07 | — |

> **R8 Check:** ทุก mutation row ต้องมี ≥ 1 entry ใน Functions/Engines column

---

## §2.X Cross-Module Contract ⭐ v6 (จาก BRD §12.1 Downstream Impact Map)

> ทุก downstream ที่มี data ไหลออกจาก feature นี้ ต้องมี contract ชัด — endpoint / event / payload

| Downstream | รูปแบบ | Contract | Trigger | Payload หลัก |
|---|---|---|---|---|
| Budget | Event | `pr.approved` | PR status → approved | { pr_id, commit_amount, budget_line } |
| PO | Endpoint (ปลายทางเรียก) | GET /prs/:id/approved-lines | on PO create | line items + qty |

- ยกเลิก/แก้กลางทาง → ระบุ compensating event (เช่น `pr.cancelled` → budget release)
- ทุกแถวต้อง trace กับ 06_TESTS §6.9 (XT-XX) อย่างน้อย 1 case
