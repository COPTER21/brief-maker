# 03_LOGIC — F-PAY Payment Term (เงื่อนไขการชำระเงิน)

> **Audience:** BE dev (business logic layer)
> **Scope:** All non-HTTP business logic — functions, calculations, validations, integrations
> **CUBIC:** §3.1 Functions = scope-local (camelCase) · §3.2 Engines = CUBIC Registry (kebab-case) — **ENG-PT-01, ENG-PT-02**
> **R8:** ทุก mutation API ต้อง trace ≥1 Function/Engine ใน §3.3

---

## §3.1 Functions (Scope-Local)

### F-PAY-FN-01: `createPaymentTerm`
- **Purpose:** สร้าง payment term ใหม่จาก validated payload + จัดการ installment child + default uniqueness
- **Input:** `{ code, name, name_en?, type, trigger?, due_basis?, net_days?, discount_pct?, discount_days?, deposit_method?, deposit_value?, remaining_timing?, expense_category?, installments[]?, use_in[], is_default, status }`
- **Output:** `PaymentTerm | ValidationError[]`
- **Invoked by:** F-PAY-API-02 POST /payment-terms
- **Calls:** F-PAY-FN-03 (validate), F-PAY-FN-08 (default uniqueness), ENG-PT-01 (if type=installment)
- **Side effects:** INSERT T_payment_term (used=0, DOA fields null) · INSERT T_payment_term_installment[] · INSERT T_audit_log · **ไม่ emit event**
- **Error cases:** ERR_VALIDATION_FAILED, ERR_DUPLICATE_CODE (BR-01)
- **Iron rule check:** ✅ no HTTP terms

### F-PAY-FN-02: `updatePaymentTerm`
- **Purpose:** แก้ไข term ที่มีอยู่ **แม้ used>0** (snapshot ที่เอกสารเก่าคงเดิม — AD-01/BR-08); replace installments
- **Input:** `{ id, version, ...same as create }`
- **Output:** `PaymentTerm | ValidationError[]`
- **Invoked by:** F-PAY-API-04 PUT /payment-terms/:id
- **Calls:** F-PAY-FN-03, F-PAY-FN-08, ENG-PT-01 (if installment)
- **Side effects:** UPDATE T_payment_term (version++) · replace T_payment_term_installment · INSERT T_audit_log (before/after diff)
- **Error cases:** ERR_STALE_DATA (version mismatch), ERR_VALIDATION_FAILED, ERR_DUPLICATE_CODE
- **Iron rule check:** ✅ · **Note:** **ไม่มี** guard ล็อกการแก้เมื่อ used>0 (ตั้งใจ — ต่างจาก Tax Code, OQ-PAY-05)

### F-PAY-FN-03: `validatePaymentTerm`  ⭐ (7 core validations — mirror `submitTerm()`)
- **Purpose:** ตรวจ payload ครบทุกกฎก่อน create/edit (reuse 2 API) — server-side mirror ของ HTML `submitTerm()`
- **Input:** term payload + `existingCodes` (สำหรับ dup check) + `recordId?` (exclude self)
- **Output:** `ValidationError[]` (ว่าง = ผ่าน) — แต่ละ error: `{ field, code, message }`
- **Invoked by:** F-PAY-FN-01, F-PAY-FN-02
- **Calls:** ENG-PT-01 (installment ≥2 & sum=100%) เมื่อ type=installment
- **Validation set (ทั้ง 7 + name):**
  1. `code` required + **unique/tenant** → ERR_CODE_REQUIRED / ERR_DUPLICATE_CODE (BR-01)
  2. `name` required → ERR_NAME_REQUIRED
  3. type=credit: `net_days` > 0 → ERR_CREDIT_DAYS_INVALID (BR-02)
  4. type=deposit & method=percent: `0 < deposit_value ≤ 100` → ERR_DEPOSIT_PCT_INVALID (BR-03)
  5. type=installment: count ≥ 2 **และ** SUM(pct)=100 → ERR_INSTALLMENT_COUNT / ERR_INSTALLMENT_SUM (BR-04, via ENG-PT-01)
  6. type=credit & discount_pct>0: `discount_days > 0 และ discount_days < net_days` → ERR_DISCOUNT_DAYS_INVALID (BR-05)
  7. `use_in` length ≥ 1 (ทุกค่า ∈ 7 enum, ไม่มี 'pr') → ERR_USE_IN_EMPTY (BR-06)
  8. `is_default=true` → `status='active'` → ERR_DEFAULT_NOT_ACTIVE (BR-07)
- **Side effects:** — (pure validation, read existingCodes)
- **Iron rule check:** ✅ no HTTP terms

### F-PAY-FN-04: `buildTermListQuery`
- **Purpose:** ประกอบ query filter (search code/name/name_en + type + status) + status counts (stat 4 ใบ)
- **Input:** `{ search?, type?, status?, limit, offset, tenantId }`
- **Output:** `{ rows: PaymentTerm[], counts:{all,active,inactive,draft}, total }`
- **Invoked by:** F-PAY-API-01
- **Calls:** F-PAY-FN-10 (summary per row) · **Side effects:** — (read-only) · **Iron rule check:** ✅

### F-PAY-FN-05: `setTermStatus`
- **Purpose:** เปลี่ยนสถานะเดี่ยว (3 ค่าอิสระ, ทุกทิศ) + auto-unset is_default ถ้าเปลี่ยนเป็น non-active
- **Input:** `{ id, status, version }`
- **Output:** `PaymentTerm | Error`
- **Invoked by:** F-PAY-API-05
- **Side effects:** UPDATE status (+ is_default=false ถ้า non-active) · INSERT T_audit_log · **Iron rule check:** ✅

### F-PAY-FN-06: `bulkSetStatus`
- **Purpose:** เปลี่ยนสถานะหลายรายการเป็นค่าเดียว (bulk bar)
- **Input:** `{ ids[], status, tenantId }`
- **Output:** `{ updated:number }`
- **Invoked by:** F-PAY-API-06
- **Calls:** F-PAY-FN-05 (per id, หรือ batch UPDATE) · **Side effects:** UPDATE many + audit · **Iron rule check:** ✅

### F-PAY-FN-07: `bulkDeleteTerms`  ⭐ (guard used>0)
- **Purpose:** ลบหลายรายการ — **ข้าม** ตัวที่ `used>0` (BR-08, no hard delete Central Plan)
- **Input:** `{ ids[], tenantId }`
- **Output:** `{ deleted:number, skipped:number, skipped_ids[] }`
- **Invoked by:** F-PAY-API-07
- **Logic:** partition ids → deletable (used=0) vs skipped (used>0); DELETE deletable + CASCADE installments
- **Side effects:** DELETE (used=0) + audit · **Iron rule check:** ✅

### F-PAY-FN-08: `enforceDefaultUniqueness`  ⭐ (radio-per-type)
- **Purpose:** เมื่อ set is_default=true → unset default เดิมของ **ประเภทเดียวกัน** (1/type) + guard status=active
- **Input:** `{ termId, type, is_default, status, tenantId }`
- **Output:** `void | ERR_DEFAULT_NOT_ACTIVE`
- **Invoked by:** F-PAY-FN-01, F-PAY-FN-02 (และผลของ F-PAY-FN-05 non-active)
- **Logic:** if is_default → require status=active (BR-07); UPDATE others same type SET is_default=false (enforced เพิ่มโดย partial-unique index 04_DB)
- **Side effects:** UPDATE sibling defaults · **Iron rule check:** ✅

### F-PAY-FN-09: `resolveTypeFieldSet`  (per-type config resolver)
- **Purpose:** คืน field set + trigger default/lock ต่อประเภท (มิเรอร์ `onTypeChange` / PT_TYPES) — ใช้ทั้ง FE hint และ BE default fill + BR-11/BR-12 enforcement
- **Input:** `{ type }`
- **Output:** `{ fields[], triggerDefault, triggerLocked:boolean, noTrigger:boolean, disabledUseIn[] }`
- **Invoked by:** F-PAY-FN-01/FN-02 (default fill) · FE form
- **Logic:** credit → triggerLocked=immediate (BR-10/LD-08b) · deposit → after_deposit allowed · direct_payment → noTrigger + disabledUseIn=[po,quotation,so] (BR-12) · after_deposit เฉพาะ deposit (BR-11)
- **Side effects:** — (pure) · **Iron rule check:** ✅

### F-PAY-FN-10: `buildTermSummary`  (termSummary human-readable)
- **Purpose:** สร้างข้อความสรุปเงื่อนไข (mirror HTML `termSummary`) — ใช้ใน list + view + downstream label
- **Input:** `PaymentTerm`
- **Output:** `string` (เช่น "ครบกำหนด 30 วัน · ลด 2% ถ้าจ่ายใน 10 วัน", "3 งวด (40% / 30% / 30%)", "มัดจำ 50% · ที่เหลือ 30 วัน")
- **Invoked by:** F-PAY-API-01, F-PAY-API-03, F-PAY-API-08
- **Side effects:** — (pure) · **Iron rule check:** ✅

### F-PAY-FN-11: `getActiveTermsForPicker`  ⭐ (downstream cross-module)
- **Purpose:** คืนเฉพาะ term status=**active** ให้เอกสารปลายทางเลือก (BR-10) + snapshot payload; filter ตาม use_in doc-type
- **Input:** `{ tenantId, useInDocType?, type? }`
- **Output:** `PickerTerm[]` (active only, มี snapshot fields + is_default)
- **Invoked by:** F-PAY-API-08 (downstream PO/SO/Invoice/PV/Receipt)
- **Logic:** WHERE status=active AND (useInDocType IS NULL OR useInDocType = ANY(use_in)); direct_payment ถูกกรองออกถ้า docType ∈ [po,quotation,so]
- **Side effects:** — (read-only, cacheable) · **Iron rule check:** ✅

---

## §3.2 Engines (Reusable / CUBIC-Registered)

### ENG-PT-01: `installment-validator` [NEW — DRAFT]

| Field | Value |
|---|---|
| **id** | (assigned at CUBIC registration) |
| **code** | `installment-validator` |
| **name** | Installment Schedule Validator & Journal Splitter |
| **category** | validation / financial-calculation |
| **status** | DRAFT (register at dev hand-off — OQ-ENG-REG) |
| **owner** | F-PAY (this) + shared (downstream AP/AR posting) |

**Input Schema:**
```json
{ "installments": [ { "seq": 1, "pct": 40, "days": 0, "due_type": "on_doc", "description": "" } ],
  "total_amount": 100000, "base_date": "2026-08-10", "due_basis": "invoice_date" }
```
**Output Schema:**
```json
{ "valid": true, "errors": [],
  "journal_split": [ { "seq":1, "amount":40000, "due_date":"2026-08-10" } ] }
```
**Logic Outline:**
1. ตรวจ count ≥ 2 → else error ERR_INSTALLMENT_COUNT ("ต้องมีอย่างน้อย 2 งวด")
2. ตรวจ SUM(pct) = 100 → else error ERR_INSTALLMENT_SUM ("สัดส่วนงวดต้องรวมเป็น 100%")
3. (downstream posting) แตก journal item ต่องวด: amount = total × pct/100 · due_date จาก due_type (on_doc / days_after_delivery(+days) / manual) + base_date/due_basis → AP/AR aging ต่องวด (BRD §12.1 Hook-1)

**Used by features:** F-PAY (validate at create/edit) · AP Invoice / AR Invoice (journal split at posting — downstream)
**Iron rule check:** ✅ Pure (no I/O, no HTTP) · ✅ Reusable (validate + downstream split) · ✅ Substantial (algorithm + boundary)
**CUBIC Registration:** DRAFT → register ตอน dev hand-off (Architect). แยก concern: validate (sync ใน F-PAY) vs split (downstream posting).

---

### ENG-PT-02: `payment-trigger-resolver` [NEW — DRAFT]

| Field | Value |
|---|---|
| **id** | (assigned at CUBIC registration) |
| **code** | `payment-trigger-resolver` |
| **name** | Warehouse/GRN/Ship Trigger Resolver (P2P/S2C) |
| **category** | integration / financial-calculation |
| **status** | DRAFT (register at dev hand-off — OQ-ENG-REG) |
| **owner** | F-PAY (this) + shared (Warehouse/GRN/Ship downstream) |

**Input Schema:**
```json
{ "type":"deposit", "trigger":"after_deposit", "side":"P2P|S2C",
  "deposit_paid": false, "full_paid": false, "doc_confirmed": true }
```
**Output Schema:**
```json
{ "unlock": false, "unlock_point":"after_deposit",
  "interpretation":"GRN (P2P) รอชำระมัดจำก่อน" }
```
**Logic Outline:**
1. Map trigger ต่อประเภท (LD-02): prepay→after_full · deposit→after_deposit · postpay/installment/partial/**credit(locked=immediate, LD-08b)**→immediate · direct_payment→noTrigger (skip)
2. แปลฝั่ง: P2P → Warehouse/GRN · S2C → Ship
3. คืน unlock boolean ตาม state (doc_confirmed / deposit_paid / full_paid) → downstream ปล่อยของเมื่อ unlock=true
4. Partial: ยอดจ่ายต่อรอบกำหนดที่ GRN (LD-10) — resolver คืน per-round unlock

**Used by features:** F-PAY (trigger default/lock ใน form) · Warehouse/GRN/Ship (unlock decision — downstream)
**Iron rule check:** ✅ Pure · ✅ Reusable (P2P + S2C) · ✅ Substantial (per-type/per-side matrix)
**CUBIC Registration:** DRAFT → register ตอน dev hand-off (Architect).

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| F-PAY-API-01 | GET | /payment-terms | FN-04 (query), FN-10 (summary) | — |
| F-PAY-API-02 | POST | /payment-terms | FN-01 (create), FN-03 (validate), FN-08 (default), FN-09 (type fill) | ENG-PT-01 (if installment) |
| F-PAY-API-03 | GET | /:id | FN-10 (summary) | — |
| F-PAY-API-04 | PUT | /:id | FN-02 (update), FN-03 (validate), FN-08 (default), FN-09 | ENG-PT-01 (if installment) |
| F-PAY-API-05 | PATCH | /:id/status | FN-05 (status) | — |
| F-PAY-API-06 | POST | /bulk-status | FN-06 (bulk status) | — |
| F-PAY-API-07 | POST | /bulk-delete | FN-07 (bulk delete guard) | — |
| F-PAY-API-08 | GET | /active | FN-11 (picker) | ENG-PT-02 (trigger interpretation, on-demand) |

### Trace Verification (Self-Check)
- [x] Every mutation API (02,04,05,06,07) has ≥ 1 Function ✅
- [x] No orphan Function — FN-01..11 ทุกตัวปรากฏใน trace ✅
- [x] No orphan Engine — ENG-PT-01 (API-02,04), ENG-PT-02 (API-08 + downstream) ✅
- [x] No hidden logic in 02_API — validation ทั้งหมดอยู่ FN-03; per-type ที่ FN-09 ✅

---

## §3.4 Dependencies (Cross-feature / Backend Hooks)

### External Function/Engine called
- **Tax Code master** (feature #3): deposit VAT tax-invoice ณ จุดรับเงิน — **Hook-2** (OQ-PAY-04). F-PAY เตรียมข้อมูล deposit; การออกใบกำกับภาษี + GL posting = feature ปลายทาง (AR Receipt) + Tax Code + GL Posting Setup.
- **cash-discount account** — **Hook-3** (BRD §12.1): ส่วนลดจ่ายเร็ว (discount_pct/days) → บัญชีส่วนลดรับ/จ่าย ที่ GL Posting (downstream).

### Backend Hooks (anchors — ทำที่ feature ปลายทาง, ประกาศที่นี่)
| Hook | หน้าที่ | Engine/Integration | สถานะ |
|---|---|---|---|
| Hook-1 | installment journal split → AP/AR aging ต่องวด | ENG-PT-01 (downstream posting) | FRD FULL, register |
| Hook-2 | deposit VAT tax-invoice ณ จุดรับเงิน | Tax Code + GL Posting Setup | OQ-PAY-04 (blocking dev deposit GL) |
| Hook-3 | cash-discount account | GL Posting Setup | FRD FULL |

### External Function/Engine that calls into this feature
- PO / SO / Quotation / AP / AR Invoice / Payment Voucher / Receipt → F-PAY-FN-11 (via GET /active) + ENG-PT-02 (trigger)

---

## §3.5 Open Questions / Locked Decisions Referenced
- **LD-01/07 (07_LOCKED):** ENG-PT-01 / ENG-PT-02 = DRAFT → register CUBIC ตอน dev hand-off (Architect, OQ-ENG-REG)
- **LD (07_LOCKED):** `updatePaymentTerm` **ไม่ล็อก** used>0 (ต่างจาก Tax Code) — AD-01 / OQ-PAY-05
- **AD-04:** optimistic-lock + idempotency = conservative default (Phase 2.5 probe) — OQ-PAY-CC-01
- **OQ-PAY-07:** นิยาม `used` (นับ draft ปลายทางด้วยไหม) กระทบ F-PAY-FN-07 delete guard — spec ก่อน dev

---

## Audience Cheat-Sheet
| Reader | Read sections |
|---|---|
| BE dev | §3.1 + §3.2 + §3.3 |
| QA | §3.3 + FN Side effects + ENG I/O |
| Architect / CUBIC owner | §3.2 (ENG-PT-01/02) + §3.4 + §3.5 |
| PM | §3.3 (table) |
