# 03_LOGIC — F-TAX Tax Code (รหัสภาษี)

> **Audience:** BE dev (business logic layer)
> **Scope:** Non-HTTP logic — pure functions, state transitions, validations, snapshot/pickable resolution
> **CUBIC:** §3.1 Functions = scope-local · §3.2 Engines = CUBIC Registry candidates
> **Iron Rule R8:** ทุก mutation API trace ไปที่ ≥1 Function/Engine ใน §3.3

---

## §3.1 Functions (Scope-Local) — camelCase

### F-TAX-FN-01: `buildTaxCodeListQuery`
- **Purpose:** สร้าง query สำหรับ list ตาม company + family + status filter + search (P-01).
- **Input:** `{ companyId, family, status, q, limit, offset }`
- **Output:** `{ rows: TaxCode[], total: number }`
- **Invoked by:** F-TAX-API-01
- **Calls:** —
- **Side effects:** — (read T_tax_code)
- **Error cases:** —
- **Iron rule check:** ✅ no HTTP terms

### F-TAX-FN-02: `createTaxCodeRecord`
- **Purpose:** สร้าง TaxCode record ใหม่ (draft หรือ pre-activate) พร้อม derive fields.
- **Input:** `{ companyId, actor, form, mode }` (form = fields §6.2)
- **Output:** `TaxCode | ValidationError[]`
- **Invoked by:** F-TAX-API-03
- **Calls:** F-TAX-FN-04 (validate), F-TAX-FN-14 (vat_report_category), F-TAX-FN-12 (income_category_code), F-TAX-FN-13 (audit)
- **Side effects:** INSERT T_tax_code (status=draft/active); INSERT T_tax_code_audit
- **Error cases:** BR_TAX_CODE_DUPLICATE, ERR_VALIDATION_FAILED
- **Iron rule check:** ✅ no HTTP terms

### F-TAX-FN-03: `updateTaxCodeRecord`
- **Purpose:** แก้ไข record; **enforce rate/family/vatKind/direction/code lock เมื่อ used>0** (R02/E02) — ปฏิเสธการแก้ field ที่ล็อก.
- **Input:** `{ companyId, actor, id, patch, ifMatchVersion }`
- **Output:** `TaxCode | ValidationError[]`
- **Invoked by:** F-TAX-API-04
- **Calls:** F-TAX-FN-04, F-TAX-FN-13
- **Side effects:** UPDATE T_tax_code (version++); INSERT audit
- **Error cases:** BR_TAX_RATE_LOCKED, ERR_STALE_DATA, BR_TAX_CODE_DUPLICATE
- **Iron rule check:** ✅

### F-TAX-FN-04: `validateTaxCodeForm`
- **Purpose:** Validation รวมศูนย์ (ใช้ทั้ง create/update/activate/replacement) — uniqueness (case-insensitive/company), GL role ครบตาม direction, WHT income required, effStart, effEnd≥effStart, rate 0–100. รับ flag `activateFull` (partial สำหรับ draft).
- **Input:** `{ companyId, form, activateFull: boolean }`
- **Output:** `{ ok: boolean, errors: { field: message } }`
- **Invoked by:** F-TAX-FN-02, FN-03, FN-05, FN-08 (และ API-03/04/05/08)
- **Calls:** ENG-03 gl-role-validator
- **Side effects:** — (read T_tax_code for uniqueness; read CoA for GL role)
- **Error cases:** BR_TAX_CODE_DUPLICATE, BR_TAX_GL_REQUIRED, BR_TAX_WHT_INCOME_REQUIRED, BR_TAX_EFF_START_REQUIRED, VR05/VR11 bounds
- **Iron rule check:** ✅ (returns error objects, ไม่ throw HTTP)

### F-TAX-FN-05: `activateTaxCode`
- **Purpose:** Orchestrate เปิดใช้งาน (draft/inactive → active): validate เต็ม → set status=active → snapshot-ready → audit. **บังคับ Approver (SoD) — role check ที่ API layer + re-check (E16).**
- **Input:** `{ companyId, actor, id, ifMatchVersion }`
- **Output:** `TaxCode | ValidationError[]`
- **Invoked by:** F-TAX-API-05, และผ่าน FN-02 (mode=activate), FN-08 (replacement activate)
- **Calls:** F-TAX-FN-04 (activateFull=true), ENG-03, F-TAX-FN-13
- **Side effects:** UPDATE status=active; INSERT audit ("สร้างและเปิดใช้งานรหัสภาษี"/"บันทึกการแก้ไขและเปิดใช้งาน")
- **Error cases:** BR_TAX_GL_REQUIRED, BR_TAX_WHT_INCOME_REQUIRED, ERR_STALE_DATA, ERR_INSUFFICIENT_ROLE
- **Iron rule check:** ✅

### F-TAX-FN-06: `deactivateTaxCode`
- **Purpose:** active → inactive; set eff_end=today; audit. เอกสารเดิมยังใช้ snapshot (E01).
- **Input:** `{ companyId, actor, id, ifMatchVersion }`
- **Output:** `TaxCode`
- **Invoked by:** F-TAX-API-06
- **Calls:** F-TAX-FN-13
- **Side effects:** UPDATE status=inactive, eff_end=today; INSERT audit ("ปิดใช้งาน — ไม่แสดงในเอกสารใหม่")
- **Error cases:** ERR_STALE_DATA, ERR_NOT_FOUND
- **Iron rule check:** ✅

### F-TAX-FN-07: `archiveDraft`
- **Purpose:** draft → archived (เก็บร่างถาวร); no hard delete (R05).
- **Input:** `{ companyId, actor, id, ifMatchVersion }`
- **Output:** `TaxCode`
- **Invoked by:** F-TAX-API-07
- **Calls:** F-TAX-FN-13
- **Side effects:** UPDATE status=archived, eff_end=today; INSERT audit ("เก็บร่างถาวร — คงข้อมูลและประวัติไว้")
- **Error cases:** ERR_NOT_FOUND, 422 (ไม่ใช่ draft)
- **Iron rule check:** ✅

### F-TAX-FN-08: `createReplacementCode`
- **Purpose:** สร้างรหัสแทน (อัตราเปลี่ยน): gen code+"-N", set new.replaces=old, old.replaced_by=new, ปิด old.eff_end = new.eff_start − 1 วัน + lineage audit ทั้งสอง (BR-02/S-07/E12).
- **Input:** `{ companyId, actor, oldId, newForm }`
- **Output:** `{ new: TaxCode, old: TaxCode } | ValidationError[]`
- **Invoked by:** F-TAX-API-08
- **Calls:** F-TAX-FN-04, F-TAX-FN-05 (activate รหัสแทน), F-TAX-FN-13
- **Side effects:** INSERT new T_tax_code; UPDATE old (replaced_by, eff_end); INSERT audit ×2 ("สร้างรหัสแทน <code> (อัตรา N%) มีผล <date>")
- **Error cases:** 422 overlap (E12), BR_TAX_CODE_DUPLICATE
- **Iron rule check:** ✅

### F-TAX-FN-09: `resolvePickableTaxCodes`
- **Purpose:** สร้าง candidate set แล้วส่งให้ ENG-02 กรอง pickable ตาม documentDate+context; mark WHT-in-purchase `advisory` (E05/LOCK-06).
- **Input:** `{ companyId, context, documentDate, family }`
- **Output:** `PickableTaxCode[]` (+ `advisory` flag)
- **Invoked by:** F-TAX-API-09
- **Calls:** ENG-02 effective-date-resolver, ENG-01 tax-snapshot-builder (build preview snapshot)
- **Side effects:** — (read)
- **Error cases:** ERR_VALIDATION_FAILED (missing documentDate)
- **Iron rule check:** ✅

### F-TAX-FN-11: `filterGlAccounts`
- **Purpose:** GL combobox options จาก CoA — filter tax_role + company + active + posting (R06/R07). **WHT → WHT_PAYABLE เท่านั้น (LOCK-12).**
- **Input:** `{ companyId, taxRole, q }`
- **Output:** `GlOption[]`
- **Invoked by:** F-TAX-API-11
- **Calls:** ENG-03 gl-role-validator (per-row allow check)
- **Side effects:** — (read CoA)
- **Error cases:** ERR_VALIDATION_FAILED (invalid taxRole)
- **Iron rule check:** ✅

### F-TAX-FN-12: `deriveIncomeCategoryCode`
- **Purpose:** map income_type (label) → income_category_code (TRANSPORT/SERVICE/RENT/…) สำหรับ WHT report (S-05 AC2).
- **Input:** `{ incomeType }`
- **Output:** `string (code)`
- **Invoked by:** F-TAX-FN-02, FN-03 (WHT)
- **Calls:** — (read T_income_type)
- **Iron rule check:** ✅

### F-TAX-FN-13: `appendAudit`
- **Purpose:** เขียน audit row (append-only) `{ts, actor, action}`; read path `buildAuditView` (DESC, gated view_audit).
- **Input:** `{ companyId, taxCodeId, actor, action }` (write) / `{ taxCodeId }` (read)
- **Output:** `AuditEntry` / `AuditEntry[]`
- **Invoked by:** ทุก mutation FN + F-TAX-API-10 (read)
- **Calls:** —
- **Side effects:** INSERT T_tax_code_audit (write path); read path = SELECT only
- **Error cases:** —
- **Iron rule check:** ✅

### F-TAX-FN-14: `resolveVatReportCategory`
- **Purpose:** vat_kind → vat_report_category (standard→STANDARD, zero→ZERO_RATED, exempt→EXEMPT) feed ภ.พ.30 (R10/LOCK-04).
- **Input:** `{ vatKind }`
- **Output:** `string`
- **Invoked by:** F-TAX-FN-02, FN-03 (VAT)
- **Calls:** —
- **Iron rule check:** ✅

### F-TAX-FN-15: `seedThaiPresets`
- **Purpose:** สร้าง preset ไทย 7 รหัสพร้อม GL ตอน launch/seed (R16): VAT7, VAT0, VAT-EX, WHT1, WHT2, WHT3, WHT5.
- **Input:** `{ companyId }`
- **Output:** `TaxCode[]`
- **Invoked by:** migration/seed job (04_DB §4.4) — ไม่ใช่ runtime API (ระบุใน 07_LOCKED CD หากต้อง idempotent seed)
- **Calls:** F-TAX-FN-02 (mode=activate), F-TAX-FN-13
- **Side effects:** INSERT ×7 + audit ("สร้างและเปิดใช้งานรหัสภาษี" actor="ระบบ (Preset)")
- **Iron rule check:** ✅

---

## §3.2 Engines (Reusable / CUBIC-Registered) — kebab-case

### ENG-TAX-01: `tax-snapshot-builder` [NEW]

| Field | Value |
|---|---|
| **id** | (assigned at CUBIC registration) |
| **code** | `tax-snapshot-builder` |
| **name** | Tax Snapshot Builder |
| **category** | generation / financial-calculation |
| **version** | 1.0.0 · **status** DRAFT · **owner** F-TAX · **stateless** true |

**Input Schema:**
```json
{ "type":"object","required":["taxCode","context","documentDate"],
  "properties":{ "taxCode":{"type":"object"}, "context":{"type":"string","enum":["sale","purchase","payment"]},
  "documentDate":{"type":"string","format":"date"} } }
```
**Output Schema:**
```json
{ "type":"object","properties":{ "tax_code_id":{"type":"string"},"code":{"type":"string"},
  "rate":{"type":"number"},"family":{"type":"string"},"direction":{"type":"string"},
  "vat_report_category":{"type":["string","null"]},"income_category_code":{"type":["string","null"]},
  "context":{"type":"string"},"document_date":{"type":"string"},"advisory":{"type":"boolean"} } }
```
**Logic Outline:**
1. Validate input schema.
2. Build immutable snapshot object จาก taxCode fields ณ documentDate.
3. ถ้า family=WHT AND context=purchase → set `advisory=true` (block final; LOCK-06/E05).
4. Freeze (immutable) → return.
**Used by features:** F-TAX (this), SO/AR Invoice, PO/AP Invoice, Payment Voucher (planned — External Contract).
**Iron rule check:** ✅ Pure · ✅ Reusable (ทุก consumer doc) · ✅ Substantial (immutability + context rules) · ✅ no HTTP terms.
**CUBIC Registration:** DRAFT → register ตอน dev hand-off.

### ENG-TAX-02: `effective-date-resolver` [NEW]

| Field | Value |
|---|---|
| **code** | `effective-date-resolver` · **category** matcher/validation · **status** DRAFT · **owner** shared · **stateless** true |

**Input Schema:** `{ "candidates": TaxCode[], "documentDate":"date", "context":"sale|purchase|payment" }`
**Output Schema:** `{ "pickable": TaxCode[] }`
**Logic Outline:**
1. For each candidate: `pickable = status==='active' AND eff_start ≤ documentDate AND (eff_end == null OR documentDate ≤ eff_end)` (R09/isPickable L2219-2224).
2. Filter direction ตรง context (sale→sale/both, purchase→purchase/both, payment→WHT pay).
3. Return pickable set.
**Used by features:** F-TAX (this) + ทุก consumer picker (planned).
**Iron rule check:** ✅ Pure · ✅ Reusable · ✅ Deterministic · ✅ no HTTP terms.

### ENG-TAX-03: `gl-role-validator` [NEW]

| Field | Value |
|---|---|
| **code** | `gl-role-validator` · **category** validation · **status** DRAFT · **owner** shared · **stateless** true |

**Input Schema:** `{ "glAccount":{...}, "expectedRole":"VAT_SALE|VAT_PURCHASE|WHT_PAYABLE", "companyId":"uuid" }`
**Output Schema:** `{ "allowed": boolean, "reason": string|null }`
**Logic Outline:**
1. `allowed = glAccount.company_id === companyId AND glAccount.status==='active' AND glAccount.posting_allowed === true AND glAccount.tax_role === expectedRole` (R06/R07/LOCK-03/LOCK-12).
2. reason = สาเหตุที่ fail (ต่างบริษัท / inactive / posting ปิด / role ผิด).
**Used by features:** F-TAX (this) + CoA-related validations (planned).
**Iron rule check:** ✅ Pure · ✅ Reusable · ✅ no HTTP terms.
> **FLAG-1/LOCK-12:** WHT ใช้ expectedRole=`WHT_PAYABLE` เท่านั้น — mirror VAT_SALE/VAT_PURCHASE (isAllowedGL L2606-2609).

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor) — MANDATORY

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| F-TAX-API-01 | GET | /tax-codes | FN-01 | — |
| F-TAX-API-02 | GET | /tax-codes/:id | — (trivial read) | — |
| F-TAX-API-03 | POST | /tax-codes | FN-02, FN-04, FN-14, FN-12, FN-13, (FN-05) | ENG-03 |
| F-TAX-API-04 | PUT | /tax-codes/:id | FN-03, FN-04, FN-13 | — |
| F-TAX-API-05 | POST | /:id/activate | FN-05, FN-04, FN-13 | ENG-03 |
| F-TAX-API-06 | POST | /:id/deactivate | FN-06, FN-13 | — |
| F-TAX-API-07 | POST | /:id/archive | FN-07, FN-13 | — |
| F-TAX-API-08 | POST | /:id/replacement | FN-08, FN-04, FN-05, FN-13 | — |
| F-TAX-API-09 | GET | /tax-codes/pickable | FN-09 | ENG-02, ENG-01 |
| F-TAX-API-10 | GET | /:id/audit | FN-13 (read) | — |
| F-TAX-API-11 | GET | /gl-accounts | FN-11 | ENG-03 |
| F-TAX-API-12 | GET | /income-types | — (reference read) | — |

### Trace Verification (Self-Check)
- [x] **Every mutation API** (03,04,05,06,07,08) มี ≥1 Function/Engine ✅
- [x] **No orphan Function** — FN-01..FN-15 ทุกตัวถูก trace (FN-15 = seed job, ระบุ Invoked-by ชัด; FN-10 ไม่มี — ไม่มี FN-10; numbering ข้าม 10 โดยตั้งใจ ดูหมายเหตุ) ✅
- [x] **No orphan Engine** — ENG-01 (API-09), ENG-02 (API-09), ENG-03 (API-03,05,11 + FN-04/11) ✅
- [x] **No hidden logic in 02_API** — create/update/validate/calculate อยู่ 03_LOGIC ✅

> **หมายเหตุ numbering:** ไม่มี F-TAX-FN-10 (จองไว้/ข้าม เพื่อคง mapping FN-09 = pickable, FN-11 = GL filter). ไม่ใช่ orphan — ไม่มี declaration ค้าง. `captureTaxSnapshot` = ENG-01 (ไม่ใช่ Function แยก).

---

## §3.4 Dependencies

### External Function/Engine called
- Chart of Accounts (CoA) read API/table — สำหรับ FN-11/ENG-03 (existing master)
- Audit Log service (ถ้า reuse — OQ-5) แทน T_tax_code_audit fallback

### External Function/Engine that calls into this feature
- Consumer docs (SO/PO/Invoice/Payment) เรียก F-TAX-API-09 + ENG-01/ENG-02 (External Contract — planned)

---

## §3.5 Open Questions / Locked Decisions Referenced
- **LD-01** (07 §7.1): Optimistic locking (version) แทน pessimistic — E15/OQ-9.
- **LD-02** (07 §7.1): Engines ENG-01/02/03 register CUBIC ที่ dev hand-off (status DRAFT).
- **LD-03** (07 §7.1): Idempotency-Key required บน mutation `[AI-DEFAULT]` — OQ-8.
- **OQ-6:** GL deactivated ใน CoA ภายหลัง (E08) → ยังไม่ตัดสิน validation behavior (ENG-03 ตรวจ ณ activate เท่านั้น; post-active CoA-change ยังไม่ spec).

---

## Audience Cheat-Sheet
| Reader | Read sections |
|---|---|
| BE dev | §3.1 + §3.2 + §3.3 |
| BE dev (HTTP) | §3.3 + relevant entries |
| QA | §3.3 + FN Side effects + ENG Input/Output |
| DBA | FN Side effects (DB ops) |
| Architect / CUBIC owner | §3.2 + §3.4 + §3.5 |
