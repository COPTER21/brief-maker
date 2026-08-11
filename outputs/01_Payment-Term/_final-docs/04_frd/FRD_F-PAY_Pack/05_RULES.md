# 05_RULES — F-PAY Payment Term (เงื่อนไขการชำระเงิน)

> **Audience:** Backend developer + QA
> **Purpose:** Business Rules + Validation (7 core) + Edge Cases + Errors + Security
> **Principle:** Declarative — อ่านแล้วเข้าใจโดยไม่ต้องดูโค้ด
> **Conflict Priority:** LOCK (LD-01..15) > BRD business intent > HTML. Enforcement server-side = mirror ของ HTML `submitTerm()` (Control C4).

---

## §5.1 Business Rules (BR)

### BR-01: Code unique + UPPERCASE
- **Statement:** `code` required, เก็บ UPPERCASE, unique/tenant
- **Enforced by:** F-PAY-FN-03 + DB UNIQUE(tenant_id, code) · Error `ERR_DUPLICATE_CODE` (409) / `ERR_CODE_REQUIRED` (422)
- **Tag:** FIXED

### BR-02: Credit net_days > 0 · Postpay ≥ 0
- **Statement:** type=credit → net_days > 0 · type=full_postpay → net_days ≥ 0 (0=ทันที)
- **Enforced by:** F-PAY-FN-03 + CHECK constraint · Error `ERR_CREDIT_DAYS_INVALID` (422)
- **Tag:** FIXED

### BR-03: Deposit % 0 < x ≤ 100
- **Statement:** type=deposit & method=percent → 0 < deposit_value ≤ 100 · manual → value ว่าง (ไม่ validate)
- **Enforced by:** F-PAY-FN-03 + CHECK · Error `ERR_DEPOSIT_PCT_INVALID` (422)
- **Tag:** FIXED

### BR-04: Installment ≥ 2 งวด + รวม 100%
- **Statement:** type=installment → count ≥ 2 **และ** SUM(pct) = 100
- **Enforced by:** F-PAY-FN-03 → **ENG-PT-01 installment-validator** · Error `ERR_INSTALLMENT_COUNT` / `ERR_INSTALLMENT_SUM` (422)
- **Tag:** FIXED · **Ref:** LD-09, LD-15 (Installment ≠ Partial)

### BR-05: Early-pay discount — discount_days > 0 และ < net_days
- **Statement:** type=credit & discount_pct > 0 → discount_days > 0 **และ** discount_days < net_days (standard 2/10 Net 30) · **1 ช่วงเท่านั้น** (AD-02)
- **Enforced by:** F-PAY-FN-03 + CHECK · Error `ERR_DISCOUNT_DAYS_INVALID` (422)
- **Tag:** FIXED (>1 tier = DYNAMIC/future, OQ-PAY-02)

### BR-06: use_in ≥ 1 · Quotation ขายเท่านั้น · **ไม่มี PR**
- **Statement:** use_in length ≥ 1, ทุกค่า ∈ 7 เอกสาร (po, ap_invoice, payment_voucher, so, quotation, ar_invoice, receipt) · Quotation = ฝั่งขาย proposal เท่านั้น · **PR ไม่อยู่ในรายการ**
- **Enforced by:** F-PAY-FN-03 + CHECK array_length ≥ 1 · Error `ERR_USE_IN_EMPTY` (422)
- **Tag:** FIXED · **Ref:** **LD-01 (LOCK) + D-08 (PM/BA — PR ถอด)**. PR ต้องไม่ปรากฏใน UI/API/DB/enum.

### BR-07: Default 1 ตัว/ประเภท + ต้อง active
- **Statement:** is_default=true → 1 ตัว/ประเภท (ตัวเก่าหลุดอัตโนมัติ) **และ** status ต้อง = active
- **Enforced by:** F-PAY-FN-08 + partial-unique index · Error `ERR_DEFAULT_NOT_ACTIVE` (422)
- **Tag:** FIXED

### BR-08: used>0 ลบไม่ได้ · **แก้ไขได้** (snapshot)
- **Statement:** ลบ term ที่ `used>0` ไม่ได้ (bulk ข้าม + แจ้งยอด) · **แก้ไขยังทำได้** (เอกสารเก่า snapshot ไม่กระทบ)
- **Enforced by:** F-PAY-FN-07 (delete guard) · **ไม่มี** edit lock (ตั้งใจ)
- **Tag:** FIXED · **Ref:** AD-01 / OQ-PAY-05 · Central Plan no hard delete

### BR-09: ไม่มี CSV import/export
- **Statement:** จัดการผ่านฟอร์มเท่านั้น — **ไม่มี** ปุ่ม/จอ/endpoint นำเข้า-ส่งออก CSV
- **Enforced by:** ไม่สร้าง endpoint/UI (absence check) · **Ref:** มติ 2026-08-09 (LOCK)
- **Tag:** FIXED

### BR-10: ปลายทาง active-only · Credit trigger locked=immediate
- **Statement:** เอกสารปลายทางเลือกได้เฉพาะ status=active · **Credit trigger = ทันที (locked, แก้ไม่ได้)**
- **Enforced by:** F-PAY-FN-11 (active filter) + F-PAY-FN-09 (credit trigger lock) · UI lock badge (ไม่มี dropdown ให้แก้)
- **Tag:** FIXED · **Ref:** **LD-08b (LOCK)**

### BR-11: trigger default ต่อประเภท · after_deposit เฉพาะ deposit
- **Statement:** trigger default: prepay=after_full · postpay/installment/partial/credit=immediate · deposit=after_deposit · direct=none · ตัวเลือก after_deposit โผล่เฉพาะ deposit
- **Enforced by:** F-PAY-FN-09 resolveTypeFieldSet · **Ref:** LD-02
- **Tag:** CONFIGURABLE 🤖 (ค่า default ต่อประเภทเก็บใน config seed — ยกเว้น Credit locked)

### BR-12: Direct Payment — ไม่มี trigger · ปิด po/quotation/so
- **Statement:** type=direct_payment → ไม่มี trigger, ไม่มี due_basis, ปิด use_in [po, quotation, so] (is-disabled + "ไม่รองรับ") — บันทึกตรงเข้า GL
- **Enforced by:** F-PAY-FN-09 (disabledUseIn) · **Ref:** LD-05
- **Tag:** FIXED

### BR-13: due_basis 3 ค่า (ยกเว้น Direct)
- **Statement:** due_basis ∈ {invoice_date, eom, delivery} — required ทุกประเภทยกเว้น direct_payment
- **Enforced by:** F-PAY-FN-03 + CHECK · **Tag:** CONFIGURABLE 🤖 (enum อาจขยายผ่าน config)

---

## §5.2 State Machine (3 สถานะอิสระ — ไม่มีอนุมัติ)

```
        ┌────────────────────────────────┐
        │   draft ⇄ active ⇄ inactive     │   (ทุกทิศ, Finance Admin, ทันที)
        └────────────────────────────────┘
   any (used=0) ──bulk ลบ + confirm──▶ (ลบออกจากทะเบียน)
   any (used>0) ──ลบ──▶ (ถูกข้าม — soft, no hard delete)
```

| From | To | Action | Allowed roles | Conditions |
|---|---|---|---|---|
| any | draft/active/inactive | เมนู view / bulk / form / create | Finance Admin | ทุกทิศ, ไม่มีอนุมัติ (VD-PDM-02) · ค่าปัจจุบัน disabled |
| active | — (picker) | ปลายทางเลือก | System | เฉพาะ active โผล่ใน picker (BR-10) |
| any (used=0) | (deleted) | bulk ลบ + confirm | Finance Admin | used>0 ถูกข้าม |
| any (used>0) | (skipped) | ลบ | System | no hard delete (BR-08) |

**Guard:** เปลี่ยนเป็น non-active + is_default=true → auto-unset is_default (BR-07).
> **Dead paths (ไม่อยู่ใน scope):** legacy `archived`/`doArchive`/`reactivate` มีใน HTML แต่ **ไม่ถูกเรียกจาก UI** (สถานะจริง = 3 ค่า) — dev ห้าม implement.

---

## §5.3 Permission Matrix

| Role | View/ค้นหา | Create | Edit (แม้ used>0) | เปลี่ยนสถานะ | ตั้ง Default | bulk ลบ (used=0) | เลือกใช้ในเอกสาร |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Finance Master Admin** | ✅ | ✅ | ✅ | ✅ (3 ค่า) | ✅ | ✅ | — |
| **Finance Viewer** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | — |
| **Consumer (ปลายทาง)** | (ผ่าน picker) | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (เฉพาะ active) |

> Enforcement server-side (P3 RBAC). Viewer/Consumer เรียก mutation ตรง → **403 ERR_INSUFFICIENT_ROLE** (EC — §5.5, PM edge).

---

## §5.4 Field Validation Rules (7 core + name — mirror `submitTerm()`)

| # | Field | Rule | Error code | HTTP | BR |
|---|---|---|---|---|---|
| 1 | `code` | required + unique/tenant (UPPERCASE) | ERR_CODE_REQUIRED / ERR_DUPLICATE_CODE | 422/409 | BR-01 |
| — | `name` | required | ERR_NAME_REQUIRED | 422 | — |
| 2 | `net_days` (credit) | > 0 | ERR_CREDIT_DAYS_INVALID | 422 | BR-02 |
| 3 | `deposit_value` (deposit %) | 0 < x ≤ 100 | ERR_DEPOSIT_PCT_INVALID | 422 | BR-03 |
| 4 | `installments` | count ≥ 2 **และ** sum = 100 | ERR_INSTALLMENT_COUNT / ERR_INSTALLMENT_SUM | 422 | BR-04 |
| 5 | `discount_days` (credit + discount) | > 0 และ < net_days | ERR_DISCOUNT_DAYS_INVALID | 422 | BR-05 |
| 6 | `use_in` | length ≥ 1 (∈ 7 enum, ไม่มี pr) | ERR_USE_IN_EMPTY | 422 | BR-06 |
| 7 | `is_default` | ถ้า true → status = active | ERR_DEFAULT_NOT_ACTIVE | 422 | BR-07 |

**Behavior:** ทุกข้อ **block save + ชี้ช่อง (is-invalid) + toast** (HTML verbatim ดู 06_TESTS §6.10). Server mirror ทุกข้อ. ข้อความ error/toast ห้ามแต่งใหม่ — ยึด HTML.
**Cross-field:** discount_days < net_days (BR-05) · installment sum = 100 (BR-04) · default⇒active (BR-07).

---

## §5.5 Edge Cases (from BRD §10 + Phase 2.5 Lane-Mode probing)

> Lane Mode: probe ที่ไม่มีคำตอบใน BRD → conservative default + tag `[AI-DEFAULT]` + OQ (ไม่ถาม user).

### EC-01: Concurrent default set (PR-1 / BRD §10.2 CA) `[AI-DEFAULT]`
- **Scenario:** 2 admin ตั้ง default ประเภทเดียวกันพร้อมกัน
- **Resolution:** Optimistic lock (`If-Match`/version) — first commit ชนะ, second → 409 `ERR_STALE_DATA`
- **Tag:** `[AI-DEFAULT]` AD-04 — ยืนยัน OQ-PAY-CC-01 · **Test:** TC-CC-01

### EC-02: Double-submit create (PR-7) `[AI-DEFAULT]`
- **Scenario:** double-click "บันทึกและสร้าง"
- **Resolution:** Idempotency-Key — request ที่ 2 คืน cached (ไม่ INSERT ซ้ำ, ไม่ dup audit)
- **Tag:** `[AI-DEFAULT]` AD-04 · **Test:** TC-ID-01

### EC-03: เปลี่ยน type ของ term ที่ used>0 (BRD §10.2 ST)
- **Scenario:** edit เปลี่ยน type/ค่า ของ term ที่ used>0
- **Resolution:** อนุญาต — เอกสารเก่า **snapshot** ไม่ retro-active (ต่างจาก Tax Code, ตั้งใจ) · กระทบเฉพาะเอกสารใหม่
- **Ref:** AD-01 / OQ-PAY-05 · **Test:** TC-EDIT-USED (AT-09)

### EC-04: นิยาม `used` (BRD §10.2 DI / OQ-PAY-07) — **OPEN**
- **Scenario:** `used` นับจากเอกสารใดบ้าง (นับ draft ของเอกสารด้วยไหม)
- **Resolution `[AI-DEFAULT]`:** นับเฉพาะเอกสารที่ **committed** (ไม่นับ draft ปลายทาง) — pending ยืนยัน **OQ-PAY-07** (blocking delete guard behavior)
- **Test:** TC-USED-DEF (verify count logic เมื่อ spec ปิด)

### EC-05: Term ถูกเปลี่ยนเป็น non-active ระหว่างสร้างเอกสารปลายทาง (BRD §10.2 DI)
- **Scenario:** ปลายทางกำลังสร้างเอกสารอ้าง term ที่เพิ่งถูกปิด
- **Resolution:** เอกสารที่ snapshot แล้วยังใช้ได้ · picker ใหม่ซ่อน (F-PAY-FN-11 active-only)
- **Test:** XT-02 (06_TESTS §6.9)

### EC-06: ลบ default term (used=0) → ประเภทนั้นไม่มี default
- **Scenario:** default ของประเภทถูกลบ
- **Resolution:** ยอมรับได้ — เอกสารใหม่ประเภทนั้นไม่มี auto-select (BRD §10.2 accepted)
- **Test:** TC-DEL-DEFAULT

### EC-07: Deposit VAT — ใบกำกับภาษี ณ จุดรับเงิน (BRD §10.2 CL / OQ-PAY-04) — **OPEN**
- **Scenario:** รับมัดจำต้องออกใบกำกับภาษี ณ จุดรับเงิน (VAT ไทย)
- **Resolution:** Hook-2 — flow บัญชี + Tax Code integration = **feature ปลายทาง (AR Receipt)** · pending **OQ-PAY-04** (blocking dev deposit GL)
- **Ref:** 03_LOGIC §3.4 Hook-2 · **Test:** XT-04

### EC-08: EOM + net_days ข้ามเดือน/ปี (BRD §10.2 CL) — **OPEN**
- **Scenario:** due_basis=eom + net_days ข้าม leap/สิ้นปี → นิยาม due date ที่ขอบเขต
- **Resolution:** คำนวณ due date เกิดที่ **downstream (AP/AR Invoice)** — F-PAY เก็บแค่ config · นิยาม boundary = OQ (downstream calc spec)
- **Test:** (downstream feature)

### EC-09: Deposit method = manual → value ว่าง (BRD §10.1 confirmed)
- **Resolution:** method=manual → deposit_value = null, **ไม่ validate** value (skip BR-03) · **Test:** AT-05b

### EC-10: Direct payment ปิด po/quotation/so ใน use_in (BRD §10.1 confirmed)
- **Resolution:** เลือก direct_payment → auto-remove po/quotation/so จาก use_in + disable checkbox ("ไม่รองรับ") · **Test:** AT-17

### EC-11: Installment days=0 หลายงวด → due date ชนกัน (BRD §10.2 CL)
- **Resolution:** ยอมรับได้ (accepted) — ไม่ block · due date เดียวกันได้

---

## §5.6 Error Catalog

| Code | HTTP | Message (i18n key) | Cause / BR |
|---|---|---|---|
| `ERR_NOT_AUTHENTICATED` | 401 | error.auth.unauth | No/invalid token |
| `ERR_INSUFFICIENT_ROLE` | 403 | error.auth.role | Viewer/Consumer เรียก mutation (§5.3) |
| `ERR_NOT_FOUND` | 404 | error.notfound | term id ไม่พบ |
| `ERR_VALIDATION_FAILED` | 400 | error.validation.failed | generic (payload malformed) |
| `ERR_CODE_REQUIRED` | 422 | pay.code.required | BR-01 ("กรุณากรอกรหัส") |
| `ERR_DUPLICATE_CODE` | 409 | pay.code.dup | BR-01 ("รหัสนี้มีอยู่แล้ว — ใช้รหัสอื่น") |
| `ERR_NAME_REQUIRED` | 422 | pay.name.required | name ว่าง |
| `ERR_CREDIT_DAYS_INVALID` | 422 | pay.credit.days | BR-02 ("จำนวนวันเครดิตต้องมากกว่า 0") |
| `ERR_DEPOSIT_PCT_INVALID` | 422 | pay.deposit.pct | BR-03 ("มัดจำแบบ % ต้องมากกว่า 0 / ไม่เกิน 100") |
| `ERR_INSTALLMENT_COUNT` | 422 | pay.inst.count | BR-04 ("ต้องมีอย่างน้อย 2 งวด") |
| `ERR_INSTALLMENT_SUM` | 422 | pay.inst.sum | BR-04 ("สัดส่วนงวดต้องรวมเป็น 100%") |
| `ERR_DISCOUNT_DAYS_INVALID` | 422 | pay.discount.days | BR-05 ("วันชำระเพื่อรับส่วนลดต้องมากกว่า 0 และน้อยกว่าวันเครดิต") |
| `ERR_USE_IN_EMPTY` | 422 | pay.usein.empty | BR-06 ("เลือกเอกสารที่ใช้อย่างน้อย 1 รายการ") |
| `ERR_DEFAULT_NOT_ACTIVE` | 422 | pay.default.active | BR-07 ("ตั้งเป็นค่า Default ได้เฉพาะเงื่อนไขสถานะ ใช้งาน") |
| `ERR_STALE_DATA` | 409 | error.concurrency.stale | EC-01 optimistic lock |
| `ERR_DUPLICATE_IDEMPOTENCY_KEY` | 409 | error.idempotency.dup | EC-02 |
| `ENG_ERR_INVALID_INPUT` | 500 | error.engine.input | ENG-PT-01/02 input mismatch |

---

## §5.7 Security Bible Application

> Domains triggered: **D2, D5, D9, D15, D17** (D7 PII = N/A). Preset **P3 Master Data** (BRD §16).

### D2: Authentication & Session
- ทุก endpoint require JWT · RBAC: Finance Admin vs Viewer vs Consumer

### D5: Financial Config
- Payment Term = config การเงินส่วนกลาง — ทุกการแก้ → audit log mandatory (ใครแก้เงื่อนไข) · ควบคุมเชิงเงิน (P4) บังคับที่**เอกสารปลายทาง** ไม่ใช่ master นี้

### D9: Audit Logging
- ทุก mutation (create/edit/status/bulk/delete) → T_audit_log (append-only, 7 ปี, immutable) · diff before/after

### D15: Admin Actions
- ทุก status transition + default change logged พร้อม actor + timestamp · **ไม่มี** approver (DOA null) → reason ไม่บังคับ

### D17: Multi-Tenant Isolation
- PostgreSQL RLS by tenant_id · API middleware validate X-Tenant-Id · cross-tenant forbidden

### D-CLASS: Data Classification
- Feature = **Internal only** (ไม่มี Confidential/Restricted/PII field ในตัว master — ดู 04_DB §4.6)

| Layer | Internal fields |
|---|---|
| API | JWT auth |
| UI | แสดงปกติ (authenticated) |
| Audit | mutation log |

**Wire points:** DOA placeholder (null) → Policy Center (future). ไม่มี Restricted Resources (ไม่มี Restricted field).

### D-domain N/A
- **D7 (PII):** ไม่มี personal data · **DOA/Approval:** N/A (master no-approval) · **NOTIF:** ไม่ emit

---

## §5.8 Compliance & Audit
| Requirement | Implementation |
|---|---|
| ควบคุมการแก้ config การเงิน | C1 RBAC + C2/C6 audit/access log (BRD §16.3) |
| Snapshot integrity | C7 — เอกสารปลายทางเก็บ snapshot ไม่ผูก FK |
| No hard delete | C5 — used>0 guard + soft archive (Central Plan) |
| Credit trigger lock | C10 — LD-08b (field-level lock) |
| Server-side validation | C4 — mirror submitTerm() (7 validations) |
