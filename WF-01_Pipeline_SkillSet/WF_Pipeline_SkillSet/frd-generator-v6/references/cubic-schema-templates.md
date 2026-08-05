# CUBIC Schema Templates — frd-generator-v6

> **Purpose:** ระบุ schema format ที่ตรงกับ CUBIC Registry สำหรับ API + Engine
> **Used by:** templates/02_api.template.md, templates/03_logic.template.md (§3.2)
> **CUBIC Principle:** API = HTTP layer · Engine = pure business logic (no HTTP)

---

## 🎯 CUBIC 3-Layer Architecture

```
┌─────────────────────────────────────────────────┐
│  Feature (F-XX)                                 │
│    ├── UI (01_UI.md)         ── React/HTML      │
│    ├── API (02_API.md)       ── HTTP routes     │
│    ├── Functions (03 §3.1)   ── scope-local     │
│    └── Engines (03 §3.2)     ── CUBIC Registry  │
└─────────────────────────────────────────────────┘

Iron Rule: UI → API → Function → Engine
           (never bypass: UI cannot call Engine direct)
```

---

## 📋 API Entity Schema (for 02_API.md)

ทุก endpoint ต้องมี Contract Block ตามนี้:

```markdown
### F-XX-API-NN: <Method> <Path>

| Field | Value |
|---|---|
| **id** | F-XX-API-NN (scope-local) |
| **method** | GET / POST / PUT / PATCH / DELETE |
| **path** | /api/v1/resource/:id |
| **summary** | [1-line purpose] |
| **auth** | required / public / api-key |
| **roles** | [admin, manager, cashier, ...] |
| **rate-limit** | default (100/min) / custom |

**Request:**
- **Path params:** `:id` (uuid)
- **Query params:** `?status=active&limit=20`
- **Headers:** `X-Tenant-Id` (required if multi-tenant)
- **Body:**
  ```json
  {
    "field": "type"
  }
  ```
- **Validation:** [field-level rules ≤ 5 lines — else ref to 05_RULES]

**Response (200/201):**
```json
{
  "id": "uuid",
  "status": "created"
}
```

**Error Responses:**
- 400: ERR_VALIDATION_FAILED
- 403: ERR_INSUFFICIENT_ROLE
- 404: ERR_NOT_FOUND
- 409: ERR_CONFLICT (idempotency)
- 500: ERR_INTERNAL

**Preconditions:** [state requirements — e.g. "order.status must be 'draft'"]
**Side effects:** [list — INSERT/UPDATE/DELETE, emit events, audit]
**Calls (Logic):** [Functions/Engines from 03_LOGIC §3.3 — anchor for R8]
```

### Iron Rules for API spec
- [ ] ไม่มี business logic >5 lines (ย้ายไป 03_LOGIC)
- [ ] ไม่มี calculation (ย้ายไป Engine)
- [ ] ไม่มี threshold/constant (ย้ายไป 05_RULES)
- [ ] มี "Calls (Logic)" field เสมอ (R8)

---

## 📋 Engine Entity Schema (for 03_LOGIC.md §3.2)

CUBIC Engine = registrable unit ใน CUBIC Registry

```markdown
### ENG-NNN: <engine-code> [NEW | EXISTING]

| Field | Value | Notes |
|---|---|---|
| **id** | (UUID — assigned at registration) | leave blank in FRD draft |
| **code** | `kebab-case-name` | unique, immutable |
| **name** | Human-readable name | for UI display |
| **category** | financial-calculation / validation / integration / generation / matcher / parser | enum |
| **version** | 1.0.0 (semver) | bump on breaking change |
| **status** | DRAFT / REGISTERED / DEPRECATED | DRAFT = ใน FRD นี้ |
| **owner** | F-XX (this feature) / shared / platform | who maintains |
| **stateless** | true / false | true = no internal state |

**Input Schema (JSON Schema):**
```json
{
  "type": "object",
  "required": ["field1", "field2"],
  "properties": {
    "field1": { "type": "string" },
    "field2": { "type": "number", "minimum": 0 }
  }
}
```

**Output Schema (JSON Schema):**
```json
{
  "type": "object",
  "properties": {
    "result": { "type": "number" },
    "breakdown": { "type": "array" }
  }
}
```

**Logic Outline:**
1. Validate input against schema
2. [Algorithm step 1]
3. [Algorithm step 2]
4. Return result

**Error cases:**
- ENG_ERR_INVALID_INPUT → input schema mismatch
- ENG_ERR_CALCULATION_FAILED → algorithm couldn't converge
- [domain-specific errors]

**Dependencies:**
- Other engines: [ENG-NNN list — explicit chain]
- External services: [none / 3rd-party API name]
- Reference data: [config/master data needed]

**Used by features:**
- F-XX (this FRD)
- F-YY (planned)
- F-ZZ (existing — already calling this engine)

**CUBIC Iron Rules check:**
- [ ] ✅ Stateless (no hidden state)
- [ ] ✅ Pure (no I/O direct — DB/HTTP/file)
- [ ] ✅ Deterministic (same input → same output)
- [ ] ✅ No HTTP terms (req/res/header/cookie/status)
- [ ] ✅ Reusable (2+ features actual or planned)
- [ ] ✅ Substantial (>20 lines OR named algorithm)

**Test cases (for QA):**
- TC-1: [normal input] → [expected output]
- TC-2: [edge input] → [expected output]
- TC-3: [error input] → [expected error code]
```

---

## 📋 Function Schema (for 03_LOGIC.md §3.1)

Functions = lightweight, scope-local — ไม่ต้อง register CUBIC

```markdown
### F-XX-FN-NN: `<functionName>`

- **Purpose:** [1-2 ประโยค]
- **Input:**
  ```
  { field1: type, field2: type }
  ```
- **Output:** `<Type | union>`
- **Invoked by:** [API ID list หรือ function อื่น]
- **Calls:** [other FN-NN list หรือ ENG-NNN list หรือ "—"]
- **Side effects:**
  - DB: INSERT T_xxx
  - Event: emit xxx_event
  - Audit log
- **Error cases:** [ERR_CODE list — ref to 05_RULES]
- **Iron rule check:** ✅ no HTTP terms
```

### Function vs Engine Decision
ดู `references/logic-placement-matrix.md` — Tie-breakers section

---

## 🔗 Cross-Schema Linkage

API → Function/Engine ผ่าน trace table ใน `03_LOGIC.md §3.3`

```
02_API.md:
  F-XX-API-02 POST /payrolls
    Calls (Logic): F-XX-FN-01, ENG-005

03_LOGIC.md §3.3:
  | API           | Functions  | Engines |
  | F-XX-API-02   | F-XX-FN-01 | ENG-005 |
```

→ Phase 3.5 Section C จะตรวจ 2 ที่นี้ตรงกัน

---

## 📚 Categories Reference (Engine)

| Category | ใช้กับ | ตัวอย่าง |
|---|---|---|
| `financial-calculation` | คำนวณเงิน ภาษี ดอกเบี้ย | payroll-calculation-engine, tax-rule-applier |
| `validation` | ตรวจ business rule ซับซ้อน | thai-id-validator, bank-account-validator |
| `integration` | call 3rd-party API | omise-payment-gateway, sms-sender |
| `generation` | สร้างเอกสาร/รหัส | invoice-pdf-generator, ref-code-generator |
| `matcher` | จับคู่ข้อมูล | invoice-po-matcher, customer-deduplicator |
| `parser` | แปลง format | csv-bank-statement-parser, ocr-result-parser |
| `scheduler` | จัดลำดับ/ตาราง | leave-conflict-scheduler |
| `aggregator` | รวบรวม/สรุป | dashboard-kpi-aggregator |

---

## 🚨 Anti-Schema Patterns

### AP-S1: Engine ที่มี HTTP terms
```
❌ WRONG:
"logic: parse req.body.amount, validate, return res.json(result)"

✅ CORRECT:
"input: { amount: number }, output: { result: number }"
```

### AP-S2: Engine ที่ไม่ stateless
```
❌ WRONG:
"logic: increment internal counter, return counter value"

✅ CORRECT:
"input: { previousCounter: number }, output: { newCounter: number }"
```

### AP-S3: Function ที่ควรเป็น Engine (ภายหลังต้อง reuse)
```
ตอนเขียน FRD เห็นว่า logic นี้ feature อื่นจะใช้แน่ → ตั้งเป็น Engine ตั้งแต่แรก
อย่ารอจน feature ที่ 2 มา refactor
```
