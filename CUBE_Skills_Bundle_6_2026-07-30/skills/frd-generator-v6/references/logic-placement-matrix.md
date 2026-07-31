# Logic Placement Decision Matrix — frd-generator-v6

> **Purpose:** ตอบคำถาม "logic ตัวนี้ควรอยู่ไฟล์ไหน" แบบ deterministic
> **Reader:** BA / Dev / Skill (v5)
> **Used by:** frd-generator-v6 Phase 1.3 (Mental Map), Phase 2 (Write), Phase 3.5 Section G (verify)

---

## 🎯 หลักการ (TL;DR)

```
ของอยู่ผิดที่ = หาไม่เจอ + dev ไม่กล้าแตะ + bug ซ้อน
```

ทุก feature มี 4 ที่หลักให้ logic อยู่:

| ไฟล์ | บทบาท | ตัวอย่าง |
|---|---|---|
| **02_API.md** | HTTP layer — รับ request, return response | path routing, status code, response shape |
| **03_LOGIC.md §3.1 Functions** | Scope-local business logic | createX, updateX, format helpers, complex validation |
| **03_LOGIC.md §3.2 Engines** | Reusable / pure / CUBIC-registered | calculation, external integration, rule applier |
| **05_RULES.md** | Declarative rules + constants | "OT_rate = 1.5x", state transition matrix |

---

## 📋 Matrix (10 patterns)

### Layer 1: HTTP-related → 02_API.md

| # | Pattern | ตัวอย่าง |
|---|---|---|
| 1 | Request parsing, body extraction | `req.body.employeeId` |
| 2 | URL routing, query string | `GET /payrolls?periodId=` |
| 3 | Response formatting (status, headers) | `return 201 + Location header` |
| 4 | Field validation < 5 lines | `if !body.email return 400` |
| 5 | Auth/role check (delegated to middleware) | `requireRole('admin')` |

**Rule:** ถ้าเอา HTTP ออกแล้วใช้ไม่ได้ → อยู่ใน 02_API

---

### Layer 2: Scope-local function → 03_LOGIC.md §3.1

| # | Pattern | ตัวอย่าง |
|---|---|---|
| 1 | **Create/Update/Delete record function** | `createPayrollRecord(input) → Record` |
| 2 | Format / transform helper | `formatThaiCurrency(num) → string` |
| 3 | Validation รวมศูนย์ (ใช้ ≥ 2 API ใน feature) | `validatePayrollPeriod(period)` |
| 4 | Workflow orchestration (กลุ่ม step) | `submitForApproval(payrollId)` calls 3 sub-steps |
| 5 | Side-effect coordinator | `notifyApprovers(payrollId)` |
| 6 | Query builder ที่ไม่ trivial | `buildDashboardQuery(filters)` |

**Rule:**
- เรียกได้โดยไม่ต้อง HTTP context (มี input/output ปกติ)
- ใช้แค่ใน feature นี้ (ไม่ reuse ข้าม feature)
- ไม่ใช่ pure calculation (มี I/O หรือ side effect)

**Naming:** camelCase verb + noun → `createPayrollRecord`, `validateBudgetLine`

---

### Layer 3: Reusable / Pure → 03_LOGIC.md §3.2 Engines

| # | Pattern | ตัวอย่าง |
|---|---|---|
| 1 | Pure calculation (math/algorithm) | `calculateNetPay(gross, deductions)` |
| 2 | Rule applier (apply rule set to input) | `applyTaxRules(income, rules) → tax` |
| 3 | External integration (3rd party) | `chargeViaOmise(amount, card)` |
| 4 | Document generator (PDF/Excel template fill) | `generatePayslipPDF(data)` |
| 5 | Reusable across 2+ features (candidate) | `validateThaiIDCard(id)` |
| 6 | Complex algorithm (sorting/matching/scheduling) | `matchInvoiceToPO(invoices, pos)` |

**Rule (Engine criteria — ≥ 2 of 3):**
1. **Pure** — input + output ชัด ไม่มี hidden state
2. **Reusable** — feature อื่นจะใช้ได้ (จริง หรือมีโอกาสสูง)
3. **Substantial** — logic > 20 lines หรือมี named algorithm

**Naming:** kebab-case noun phrase → `payroll-calculation-engine`, `thai-id-validator`

**CUBIC Registration:** Engine ใน §3.2 = candidate สำหรับ CUBIC Registry → register ตอน dev hand-off

---

### Layer 4: Declarative → 05_RULES.md

| # | Pattern | ตัวอย่าง |
|---|---|---|
| 1 | Constants / thresholds | `MAX_OVERTIME_HOURS = 36`, `MIN_AGE = 18` |
| 2 | State transition matrix | `draft → submitted (when complete)`, `submitted → approved (role=manager)` |
| 3 | Permission matrix | `role=cashier can: view, create. cannot: approve` |
| 4 | Validation rules (declarative form) | `email format = RFC5322`, `phone = TH-mobile` |
| 5 | Error code catalog | `ERR_PAYROLL_PERIOD_LOCKED, ERR_BUDGET_EXCEEDED` |

**Rule:**
- อ่านแล้วเข้าใจโดยไม่ต้องดูโค้ด
- เปลี่ยนได้โดยไม่ต้อง redeploy (มักไป config)
- QA ใช้ตรวจ business correctness

---

## 🧭 Decision Flowchart

```
มี logic ตัวใหม่ → ถามตามลำดับ:

Q1: "ถ้าเอา HTTP request/response context ออก ยังทำงานได้ไหม?"
    NO  → อยู่ใน 02_API (Layer 1) — STOP
    YES → ไป Q2

Q2: "เป็นแค่ค่า/กฎ ที่อ่านแล้วเข้าใจได้โดยไม่ต้องโค้ด?"
    YES → อยู่ใน 05_RULES (Layer 4) — STOP
    NO  → ไป Q3

Q3: "Pure + Reusable + Substantial (ตอบ YES ≥ 2/3)?"
    YES → อยู่ใน 03_LOGIC §3.2 Engines (Layer 3)
    NO  → อยู่ใน 03_LOGIC §3.1 Functions (Layer 2)
```

---

## 🚨 Anti-Patterns (ห้ามทำ — Phase 3.5 Section G จะจับ)

### AP-1: CRUD function แอบใน 02_API
```
❌ WRONG:
02_API.md:
  POST /payrolls
  Logic: "create new payroll record, validate fields, insert DB, return id"
       ← logic ปนใน API spec

✅ CORRECT:
02_API.md:
  POST /payrolls → calls F-XX-FN-01 createPayrollRecord
03_LOGIC.md §3.1:
  F-XX-FN-01 createPayrollRecord (full spec here)
```

### AP-2: Pure calculation แอบใน 02_API
```
❌ WRONG:
02_API.md:
  POST /payrolls
  "Calculate net pay = gross - deductions, apply tax brackets..."

✅ CORRECT:
03_LOGIC.md §3.2:
  ENG-005 payroll-calculation-engine
02_API.md:
  POST /payrolls → invokes ENG-005
```

### AP-3: Constants ลอยใน 02_API
```
❌ WRONG:
02_API.md: "validate amount ≤ 1,000,000"

✅ CORRECT:
05_RULES.md: "BR-PAY-08: MAX_PAYMENT_AMOUNT = 1,000,000 THB"
02_API.md: "validate against BR-PAY-08"
```

### AP-4: Orphan Function/Engine
```
❌ WRONG:
03_LOGIC §3.1: F-XX-FN-99 calculateBonus  (มี spec)
03_LOGIC §3.3: (ไม่มี API ตัวไหน trace ไปที่ FN-99)
              ← orphan! function ลอย ไม่มีใครเรียก

✅ CORRECT:
Either remove FN-99, or add to §3.3 trace + identify API caller
```

---

## 📐 Examples by Feature Type

### Example 1: Customer Quick-Add (LEAN)
```
02_API: POST /customers
03_LOGIC §3.1:
  - F-XX-FN-01 createCustomerRecord (insert + audit)
  - F-XX-FN-02 validateCustomerData (Thai ID format, phone)
03_LOGIC §3.2: (empty — no engines)
03_LOGIC §3.3: API-01 → FN-01, FN-02 ✅
05_RULES:
  - BR-01: Thai ID = 13 digits, checksum
  - BR-02: Phone = TH format
```

### Example 2: Order Submission with Pricing (STANDARD)
```
02_API:
  - POST /orders (create draft)
  - POST /orders/:id/submit (finalize)
03_LOGIC §3.1:
  - createOrderDraft
  - submitOrder (orchestrate: validate → price → lock → notify)
  - notifyWarehouse
03_LOGIC §3.2:
  - ENG-011 pricing-engine (apply discounts + tax)
03_LOGIC §3.3:
  - POST /orders → createOrderDraft
  - POST /orders/:id/submit → submitOrder → ENG-011
05_RULES:
  - BR-01: discount tiers
  - BR-02: state transition: draft → submitted (rules)
```

### Example 3: Payroll Cycle (FULL)
```
02_API: 8 endpoints
03_LOGIC §3.1: 12 functions (CRUD + workflow steps)
03_LOGIC §3.2: 3 engines
  - ENG-005 payroll-calculation-engine
  - ENG-006 tax-rule-applier
  - ENG-007 payslip-generator
03_LOGIC §3.3: full trace table
05_RULES: thresholds, state machine, role permissions
07_LOCKED: which engines candidate for CUBIC global registration
```

---

## ✅ Self-Test (BA / Skill ใช้ตรวจตัวเอง)

ก่อน deliver FRD Pack — ถาม:

1. มี Function/Engine ไหนที่ไม่มี API เรียก? → fix หรือ remove
2. มี API mutation ไหนไม่มี Function/Engine trace? → ขาด หรือ logic แอบใน API
3. ใน 02_API มีคำว่า "calculate", "validate complex", "create record" ไหม? → ย้ายไป 03_LOGIC
4. ใน 02_API มีตัวเลข threshold ไหม? → ย้ายไป 05_RULES
5. Engine ใน §3.2 ตอบ "Pure + Reusable + Substantial ≥ 2/3" ทุกตัวไหม? ถ้าไม่ → demote เป็น Function

ผ่านทุกข้อ = pass R8 + Logic Placement Compliance
