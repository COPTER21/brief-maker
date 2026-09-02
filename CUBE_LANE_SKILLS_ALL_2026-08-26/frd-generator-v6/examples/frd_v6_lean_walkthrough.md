# Example: LEAN Variant Walkthrough — F-01 Customer Quick-Add

> **Purpose:** Concrete LEAN example — แสดงว่า 03_LOGIC mandatory แม้ feature เล็ก
> **Scenario:** Customer Quick-Add — 1 page, 1 API, 2 functions, 0 engines

---

## Input Summary

**Brief §3.4:**
- complexity: Low
- has-state: No
- has-entity: Yes (Customer)
- has-approval: No

**BRD §14.6 Screen Inventory (หยาบ):**
- 1 page (Quick-Add modal, Pattern A inside parent page)
- ERP feature: YES (Sidebar context: CRM > Customers)

**Phase 0 decision:** **LEAN** (6 files)

---

## File 1: 00_OVERVIEW.md

```markdown
# 00_OVERVIEW — F-01 Customer Quick-Add

## §0.1 Document Control
| Field | Value |
|---|---|
| Feature ID | F-01 |
| Feature Name | Customer Quick-Add |
| Variant | LEAN |
| Status | DRAFT |
| Generator | frd-generator-v6 |

## §0.3 Scope
**In Scope:**
- Add new customer via modal from any CRM page
- Validate Thai ID format
- Auto-fill Thai address from postcode

**Out of Scope:**
- Edit existing customer (use F-02)
- Bulk import (use F-03)

## §0.8 Open Questions
- OQ-01: Should we deduplicate against existing customers? (P1 backlog)
```

---

## File 2: 01_UI.md

```markdown
# 01_UI — F-01 Customer Quick-Add

## §1.1 Page Inventory
| Page ID | Name | Layout | Roles |
|---|---|---|---|
| P-01 | Quick-Add Modal | Pattern A-modal | sales, manager, admin |

## §1.2 P-01 Detail
**Pattern (จาก Phase 1.5):** B — create drawer v2 .standard 680px (v4: create ห้ามใช้ modal)

**Components:**
- Form Stack
- Input: First Name, Last Name (required)
- Input: Thai ID (with realtime validation)
- Input: Phone (TH format mask)
- Input: Postcode + auto-suggest province/district
- Action Bar: Cancel, Save

**Actions:**
| Action | Calls |
|---|---|
| Click Save | F-01-API-01 POST /customers |
| Click Cancel | Close modal |

**States:**
- Initial (empty form)
- Validating (Thai ID async check)
- Submitting (disabled save button)
- Success (show toast, close modal, refresh parent)
- Error (inline field errors + generic banner)
```

---

## File 3: 02_API.md

```markdown
# 02_API — F-01

## §2.1 API Overview
| ID | Method | Path | Auth |
|---|---|---|---|
| F-01-API-01 | POST | /api/v1/customers | required (sales+) |

## §2.2 F-01-API-01: POST /api/v1/customers

**Request:**
- Headers: X-Tenant-Id, Idempotency-Key
- Body:
  ```json
  {
    "first_name": "string",
    "last_name": "string",
    "thai_id": "string (13 digits)",
    "phone": "string",
    "postcode": "string (5 digits)"
  }
  ```
- **Validation:** field-level only — complex validation in F-01-FN-02

**Response 201:**
```json
{ "id": "uuid", "created_at": "iso8601" }
```

**Errors:**
- 400: ERR_VALIDATION_FAILED
- 409: ERR_DUPLICATE_THAI_ID (idempotency)
- 422: BR_INVALID_THAI_ID

**Side effects:**
- INSERT T_customer
- INSERT T_audit_log

**Calls (Logic):**
- F-01-FN-01 createCustomerRecord
- F-01-FN-02 validateCustomerData

## §2.4 API → Logic Trace
| API | Functions | Engines |
|---|---|---|
| F-01-API-01 | F-01-FN-01, F-01-FN-02 | — |
```

---

## File 4: 03_LOGIC.md ⭐ (THIS IS THE KEY)

```markdown
# 03_LOGIC — F-01 Customer Quick-Add

> LEAN variant — Functions only, no Engines

## §3.1 Functions (Scope-Local)

### F-01-FN-01: createCustomerRecord
- **Purpose:** สร้าง customer record ใหม่ + audit log
- **Input:** `{ first_name, last_name, thai_id, phone, postcode, tenant_id }`
- **Output:** `Customer | ValidationError[]`
- **Invoked by:** F-01-API-01 POST /customers
- **Calls:** F-01-FN-02 (validate before insert)
- **Side effects:**
  - INSERT T_customer
  - INSERT T_audit_log (action: 'create', resource: 'customer:<id>')
- **Error cases:**
  - BR_INVALID_THAI_ID (from FN-02)
  - ERR_DUPLICATE_THAI_ID (DB unique constraint)
- **Iron rule check:** ✅ no HTTP terms

### F-01-FN-02: validateCustomerData
- **Purpose:** ตรวจ Thai ID format + checksum + phone format
- **Input:** `{ thai_id, phone, postcode }`
- **Output:** `ValidationResult` ที่มี `{ valid: boolean, errors: [] }`
- **Invoked by:** F-01-FN-01 createCustomerRecord
- **Calls:** —
- **Side effects:** — (pure)
- **Error cases:**
  - BR_INVALID_THAI_ID (format/checksum failed)
  - BR_INVALID_PHONE_FORMAT
  - BR_INVALID_POSTCODE
- **Iron rule check:** ✅ no HTTP terms, pure

## §3.2 Engines

> ไม่มี engine ใน LEAN feature นี้ — logic ทั้งหมดเป็น scope-local Functions
> ถ้าในอนาคต validateCustomerData ถูกใช้ใน 2+ features → upgrade เป็น Engine (CUBIC register)

## §3.3 API ↔ Logic Trace Table

| API | Functions | Engines |
|---|---|---|
| F-01-API-01 POST /customers | F-01-FN-01, F-01-FN-02 | — |

### Self-Check (R8)
- [x] All mutation APIs have ≥ 1 Function ✅ (F-01-API-01 has 2)
- [x] No orphan Functions (both used) ✅
- [x] No hidden logic in 02_API ✅
```

---

## File 5: 04_DB.md

```markdown
# 04_DB — F-01

## §4.2 T_customer

| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| tenant_id | uuid | NOT NULL, RLS |
| first_name | varchar(100) | NOT NULL |
| last_name | varchar(100) | NOT NULL |
| thai_id | char(13) | UNIQUE per tenant, encrypted |
| phone | varchar(20) | NOT NULL |
| postcode | char(5) | NOT NULL |
| created_at | timestamp | NOT NULL |
| created_by | uuid | NOT NULL |

**Indexes:**
- UNIQUE (tenant_id, thai_id)
- IDX (tenant_id, phone)

**RLS:** tenant_isolation policy
```

---

## File 6: 06_TESTS.md

```markdown
# 06_TESTS — F-01

## §6.1 Acceptance Criteria

### AC-01: Happy path
**Given** valid input
**When** POST /customers
**Then** 201 + new customer record + audit log

### AC-02: Invalid Thai ID
**Given** Thai ID with bad checksum
**When** POST /customers
**Then** 422 BR_INVALID_THAI_ID
**And** No DB insert

### AC-03: Duplicate Thai ID
**Given** Thai ID exists in same tenant
**When** POST /customers
**Then** 409 ERR_DUPLICATE_THAI_ID

### AC-04: Idempotency
**Given** Idempotency-Key + body X
**When** Same request resent
**Then** Same 201 response (no new INSERT)

## §6.4 Definition of Done
- [ ] AC-01 to AC-04 pass
- [ ] Code review approved
- [ ] T_customer migration tested
- [ ] Test coverage ≥ 80%
```

---

## 🎯 Key Takeaways from this LEAN Example

1. **6 files generated** — แม้ feature เล็ก
2. **03_LOGIC.md มี content จริง** — ไม่ใช่ placeholder
   - 2 Functions clearly specced (purpose, I/O, side effects)
   - Engines section explicitly states "no engines"
   - Trace table mandatory แม้มี API ตัวเดียว
3. **02_API.md = thin** — แค่ HTTP layer + reference to Logic
   - ไม่มี logic แอบ
   - Field validation อยู่ในนี้ (≤ 5 lines)
   - Complex validation ผลัก F-01-FN-02
4. **No 05_RULES.md** (LEAN skip) — rules อยู่ใน 03_LOGIC FN spec + 02_API errors
5. **No 07_LOCKED_DECISIONS** (LEAN skip) — open questions อยู่ใน 00_OVERVIEW
6. **R8 satisfied** — mutation API → 2 Functions traced

---

## 🚨 What WOULD be wrong (Anti-patterns)

### ❌ WRONG (v4-style):
```
02_API.md F-01-API-01:
  Logic: "Validate Thai ID checksum, insert customer record, log audit"
  ← business logic ปนใน API spec
```

### ✅ RIGHT (v5):
```
02_API.md F-01-API-01:
  Calls (Logic): F-01-FN-01, F-01-FN-02
  
03_LOGIC.md §3.1:
  F-01-FN-01 createCustomerRecord (full spec)
  F-01-FN-02 validateCustomerData (full spec)
```

→ BE dev อ่าน 02_API เห็น HTTP contract ชัด อ่าน 03_LOGIC เห็น business logic ชัด ไม่ปนกัน
