# 05_RULES — F-TAX Tax Code (รหัสภาษี)

> **Audience:** Backend developer + QA
> **Purpose:** Business Rules + Validation + Edge Cases + Errors + Security
> **Principle:** Declarative — enforce ฝั่ง server ทั้งหมด (ไม่พึ่ง client — BRD §14.2)
> **Source:** BRD §9 (R01-R17, VR01-VR13), §8 (state machine), §4.2 (permissions), §10 (edge cases). Rule IDs ที่นี่ = `BR-TAX-NN` (map ตรง BRD Rxx).

---

## §5.1 Business Rules (BR)

| BR-TAX | ← BRD | Statement | Enforced by | Error |
|---|---|---|---|---|
| **BR-TAX-01** | R01 | รหัส unique ต่อบริษัท (case-insensitive) | UQ `(company_id, lower(code))` + FN-04 | `BR_TAX_CODE_DUPLICATE` (422) |
| **BR-TAX-02** | R02/LOCK-09 | อัตราของรหัส `used>0` แก้ไม่ได้ — เปลี่ยน = replacement + lineage | FN-03 (lock) / FN-08 | `BR_TAX_RATE_LOCKED` (422) |
| **BR-TAX-03** | R03 | WHT ต้องระบุประเภทเงินได้ก่อน activate | FN-04 (activateFull) | `BR_TAX_WHT_INCOME_REQUIRED` (422) |
| **BR-TAX-04** | R04/LOCK-03 | ทุกรหัสต้องผูก GL ตามทิศทาง/ตระกูลก่อน active | FN-04 + FN-05 + ENG-03 | `BR_TAX_GL_REQUIRED` (422) |
| **BR-TAX-05** | R05/LOCK-08 | ไม่มี hard delete — deactivate/archive + append-only audit | FN-06/07/13; ไม่มี DELETE endpoint | — |
| **BR-TAX-06** | R06/LOCK-03 | GL lookup รับเฉพาะบัญชี company ปัจจุบัน `status=active` + `posting_allowed=true` | ENG-03 gl-role-validator | `BR_TAX_GL_REQUIRED` |
| **BR-TAX-07** | R07/LOCK-12 | GL role: VAT ขาย→`VAT_SALE`, VAT ซื้อ→`VAT_PURCHASE`, **WHT→`WHT_PAYABLE` เท่านั้น** (FLAG-1 RESOLVED) | ENG-03 (`expectedRole`) | `BR_TAX_GL_REQUIRED` |
| **BR-TAX-08** | R08/LOCK-07 | picker ใช้**วันที่เอกสาร** (ไม่ใช่วันที่ระบบ) + บันทึก immutable snapshot | ENG-01 + ENG-02 | — |
| **BR-TAX-09** | R09 | pickable = `status=active AND eff_start ≤ docDate ≤ eff_end` | ENG-02 effective-date-resolver | — |
| **BR-TAX-10** | R10/LOCK-04 | VAT: STANDARD/ZERO_RATED/EXEMPT + ทิศ sale/purchase/both; zero/exempt→rate=0; auto `vat_report_category` | FN-14 + FN-04 | `ERR_VALIDATION_FAILED` |
| **BR-TAX-11** | R11/LOCK-05 | WHT: แบบ ภ.ง.ด. resolve ที่ payment/reporting (`RESOLVE_BY_PAYEE_AND_PAYMENT_CONTEXT`) — ไม่ hardcode ที่ Tax Code | field `report_mapping_rule` (const) | — |
| **BR-TAX-12** | R12/LOCK-06 | AP เสนอ WHT (แนะนำ) แต่ Payment Voucher = จุดยืนยันหัก; WHT report อ่านจาก payment result | ENG-01 `advisory` + 02_API §2.X | — |
| **BR-TAX-15** | R15/LOCK-02 | UI ทำงานใน current-company context — เปลี่ยนบริษัทในฟอร์มไม่ได้ | RLS + `X-Company-Id` (D17) | 403 (cross-company) |
| **BR-TAX-16** | R16 (CONFIGURABLE) | Preset ไทย 7 รหัสพร้อม GL พร้อมใช้วันแรก (seed) | FN-15 seedThaiPresets | — |
| **BR-TAX-17** | R17 (CONFIGURABLE) | อัตราแนะนำต่อประเภทเงินได้ WHT (1/2/3/5/10%) = "คำแนะนำ" ไม่บังคับ | `T_income_type.recommended_rate` (hint) | — (OQ-7) |

> R13 (rate 0–100) → §5.4 VR05 · R14 (effEnd ≥ effStart) → §5.4 VR11 (bound validation, ไม่ซ้ำเป็น BR).

---

## §5.2 State Machine (BRD §8)

```
[*] --บันทึกร่าง(Maker)--> draft
[*] --สร้าง+เปิดใช้งาน(Approver,GL ครบ)--> active
draft --เปิดใช้งาน(Approver,GL ครบ)--> active
draft --เก็บร่างถาวร(Approver)--> archived
active --ปิดใช้งาน(Approver)--> inactive
inactive --เปิดใช้งานใหม่ผ่านหน้าแก้ไข(Approver)--> active
active --สร้างรหัสแทน(อัตราใหม่)--> active(ใหม่) + ปิด eff_end เดิม
archived / inactive --> [*]
```

| From | Trigger | To | COSO Role | System | Note |
|---|---|---|---|---|---|
| (none) | saveDraft | draft | Maker | validate code+name | ไม่บังคับ GL (E04) |
| (none) | submitForm (mode=activate) | active | Approver | validate เต็ม + GL role | create+activate |
| draft | activate | active | Approver | validate เต็ม | บังคับ GL (R04) |
| draft | archiveDraft | archived | Approver | eff_end=today + audit | soft archive |
| active | deactivate | inactive | Approver | eff_end=today + audit | เอกสารเดิมใช้ได้ (E01) |
| inactive | edit→activate | active | Approver | reactivate (E13) | |
| active | replacement | active(ใหม่) + eff_end เดิม | Maker→Approver | lineage + previousDate | BR-TAX-02 (E12) |

---

## §5.3 Permission Matrix (BRD §4.2 — `tax_code.*`)

| Role | view | view_audit | create | update | activate | deactivate |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Accountant (Maker) | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Senior Acct (Checker) | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Acct/Fin Manager (Approver) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

> **SoD (S01-04):** create/update (Maker) ≠ activate/deactivate (Approver). Server re-check ที่ mutation (E16). **OQ-3:** ยืนยัน second-person approval จริง vs single-role accounting-admin (prototype demo user ถือครบ 6 สิทธิ์ — single-user sandbox). view_audit gate ที่ P-03/API-10 (E17).

---

## §5.4 Field Validation Rules (BRD §9.2 VR01-VR13 — verbatim user-facing จาก HTML)

| VR | Field/Action | เงื่อนไข | ประเภท | ข้อความ (verbatim HTML) | HTML |
|---|---|---|---|---|---|
| VR01 | code | required | Error | กรุณากรอกรหัส | L2596 |
| VR02 | code | ซ้ำใน company (case-insensitive) | Error | รหัสนี้มีอยู่แล้วในบริษัทปัจจุบัน | L2597 |
| VR03 | name | required | Error | กรุณากรอกชื่อ | — |
| VR04 | rate (activate) | required (ยกเว้น VAT zero/exempt) | Error | กรุณากรอกอัตรา | — |
| VR05 | rate | 0 ≤ rate ≤ 100 (R13) | Error | อัตราต้องอยู่ระหว่าง 0 ถึง 100 | — |
| VR06 | income_type (WHT, activate) | required | Error | WHT ต้องระบุประเภทเงินได้ | L2604 |
| VR07 | gl_sale (VAT sale/both, activate) | role VAT_SALE | Error | ต้องเลือกบัญชี GL กลุ่มภาษีขายก่อนเปิดใช้งาน | L2606 |
| VR08 | gl_purchase (VAT purchase/both, activate) | role VAT_PURCHASE | Error | ต้องเลือกบัญชี GL กลุ่มภาษีซื้อก่อนเปิดใช้งาน | L2607 |
| VR09 | gl_wht (WHT, activate) | **role WHT_PAYABLE (LOCK-12)** | Error | ต้องเลือกบัญชี GL กลุ่มภาษีหัก ณ ที่จ่ายค้างจ่ายก่อนเปิดใช้งาน | L2609 |
| VR10 | eff_start (activate) | required | Error | กรุณาระบุวันมีผลเริ่ม | — |
| VR11 | eff_end | ≥ eff_start (R14) | Error | วันสิ้นสุดต้องไม่ก่อนวันเริ่ม | L2613 |
| VR12 | activate/create/deactivate | permission | Warning (toast) | คุณไม่มีสิทธิ์บันทึกรหัสภาษี / คุณไม่มีสิทธิ์สร้างหรือเปิดใช้รหัสภาษี | L2664/2673 |
| VR13 | captureSnapshot (WHT ใน PURCHASE) | block final | Warning (toast) | WHT ในเอกสารซื้อเป็นเพียงคำแนะนำ โปรดยืนยันตอนจ่าย | L2822 |

**Cross-field:** eff_end ที่ replacement = old.eff_start ต้อง = new.eff_start − 1 (E12); zero/exempt VAT → rate forced 0 (R10).

---

## §5.5 Edge Cases (BRD §10 — confirmed ☑ + probed ☐ / Phase 2.5)

### From BRD §10.1 (confirmed)
- **EC-01 (E01):** deactivate/หมดวันมีผล → หายจาก picker ใหม่ แต่เอกสารเดิมใช้ snapshot ต่อ → ENG-02 + immutable snapshot (ENG-01). Test XT-01.
- **EC-02 (E02):** แก้อัตรา used>0 → block → replacement path. FN-03 lock. Test AC-07.
- **EC-03 (E03):** ลบรหัสที่ถูกใช้ → block → soft archive/deactivate เท่านั้น (R05).
- **EC-04 (E04):** draft ยังไม่ผูก GL → บันทึกร่างได้ activate ไม่ได้. FN-04 activateFull. Test AC-04.
- **EC-05 (E05):** WHT ในเอกสารซื้อ = แนะนำ → block final snapshot; ยืนยันที่ Payment (LOCK-06). ENG-01 advisory. Test XT-03.
- **EC-06 (E06):** รหัสซ้ำ (case-insensitive) → block inline (VR02).
- **EC-07 (E07):** ภาษีต่างประเทศ → ไม่รองรับ (THB/ไทยเท่านั้น, ไม่มี selector).

### From BRD §10.2 (AI pattern-matching / probed) + Phase 2.5 defaults
- **EC-08 (E08):** GL ที่ผูกไว้ถูก deactivate/ลบใน CoA ภายหลัง → **ยังไม่ตัดสิน (block posting / warn / re-bind)** → **OQ-6** (BLOCKING). ENG-03 ตรวจ ณ activate เท่านั้น; ห้าม assume cascade.
- **EC-09 (E09):** GL ย้าย tax_role → รหัสที่อ้างยังถูกต้องไหม → verify ที่ next activate/edit; runtime re-bind = OQ-6 scope.
- **EC-10 (E10):** Income_Type ถูกถอด/เปลี่ยนชื่อ → WHT code ใช้ `income_category_code` ที่ derive แล้ว (snapshot code) — ไม่ break historical.
- **EC-11 (E11):** eff_start อนาคต → รหัส active แต่ยัง pickable ไม่ได้จนถึงวันมีผล (ENG-02 ครอบคลุม R09).
- **EC-12 (E12):** ช่วงวันมีผลของรหัสแทน overlap → FN-08 ตั้ง old.eff_end = new.eff_start − 1; backend enforce non-overlap.
- **EC-13 (E13):** reactivate inactive ที่ eff_end อดีต → ต้อง set eff_end ใหม่ผ่านหน้าแก้ไข (Approver); `[AI-DEFAULT]` = บังคับ set eff_end ≥ today ก่อน reactivate.
- **EC-14 (E14):** 2 accountants สร้างรหัสเดียวกันพร้อมกัน → UQ `(company_id, lower(code))` ระดับ DB (ไม่พึ่ง client) → คนที่ 2 ได้ `BR_TAX_CODE_DUPLICATE`.
- **EC-15 (E15 / PR-1):** แก้/deactivate รหัสเดียวกันพร้อมกัน → **optimistic lock** (`version`/`If-Match`) → 409 `ERR_STALE_DATA` `[AI-DEFAULT]` → **OQ-9**.
- **EC-16 (E16 / PR-3):** Maker (ไม่มี activate) กด submit → server อนุญาตเฉพาะ saveDraft; activate → 403 (re-check ที่ mutation, ไม่พึ่ง UI hide).
- **EC-17 (E17):** ผู้ไม่มี view_audit เรียก API-10 ตรง → 403 + log access (D9).
- **EC-18 (E18):** user ข้ามบริษัท เข้าถึงรหัสอื่น → block ฝั่ง server (RLS, D17).
- **EC-19 (E19):** หลายอัตรา VAT/WHT ในเอกสารเดียว → คำนวณ per line (downstream); contract snapshot ต้องรองรับ per-line (ENG-01 ต่อ snapshot). Test XT-04.

### Phase 2.5 Probe Defaults (Lane Mode — conservative, tagged `[AI-DEFAULT]`)
| Probe | สถานะใน BRD | Conservative default applied | Tag |
|---|---|---|---|
| PR-7 Idempotency | ไม่ระบุ | `Idempotency-Key` required ทุก mutation, TTL 24h → 409 dup | `[AI-DEFAULT]` OQ-8 |
| PR-1/PR-2 Concurrency | E15 บอกให้มี lock (ไม่ระบุ contract) | Optimistic `If-Match`/`version` → 409 ERR_STALE_DATA | `[AI-DEFAULT]` OQ-9 |
| PR-3 Permission mid-flight | E16 (server guard) | Re-check role ที่ mutation time | (BRD-grounded) |
| PR-4 Network failure | — | ครอบด้วย idempotency (retry-safe) | `[AI-DEFAULT]` OQ-8 |
| PR-6 Draft/Resume | draft status มี, ไม่ระบุ expiry | Draft persist ไม่มี auto-expiry (master data ไม่ใช่ wizard) | `[AI-DEFAULT]` OQ-10 |

> PR-5 (bulk), PR-8 (payment compensation), PR-9 (inventory race) — **ไม่ activate** (ไม่มี bulk/payment/stock ใน feature; out of scope).

---

## §5.6 Error Catalog

| Code | HTTP | Message (i18n key) | Cause / Rule |
|---|---|---|---|
| `ERR_VALIDATION_FAILED` | 400 | error.validation.failed | field-level (VR01/03/04/05/10/11) |
| `ERR_NOT_AUTHENTICATED` | 401 | error.auth.unauth | no/invalid token |
| `ERR_INSUFFICIENT_ROLE` | 403 | error.auth.role | SoD/permission (VR12, E16/E17/E18) |
| `ERR_NOT_FOUND` | 404 | error.notfound | record missing / cross-company (E18) |
| `ERR_DUPLICATE_IDEMPOTENCY_KEY` | 409 | error.idempotency.dup | same key + different body (OQ-8) |
| `ERR_STALE_DATA` | 409 | error.concurrency.stale | version mismatch (E15/OQ-9) |
| `BR_TAX_CODE_DUPLICATE` | 422 | br.tax.code.dup | BR-TAX-01 (VR02/E06/E14) |
| `BR_TAX_RATE_LOCKED` | 422 | br.tax.rate.locked | BR-TAX-02 (E02) |
| `BR_TAX_GL_REQUIRED` | 422 | br.tax.gl.required | BR-TAX-04/06/07 (VR07-09) |
| `BR_TAX_WHT_INCOME_REQUIRED` | 422 | br.tax.wht.income | BR-TAX-03 (VR06) |
| `BR_TAX_EFF_START_REQUIRED` | 422 | br.tax.effstart | VR10 |
| `BR_TAX_EFF_RANGE` | 422 | br.tax.effrange | VR11 (effEnd < effStart) |
| `ENG_ERR_INVALID_INPUT` | 500 | error.engine.input | ENG-01/02/03 schema mismatch |

---

## §5.7 Security Bible Application

> Domains triggered: **D2, D5(-lite), D9, D15, D17**. **ไม่ trigger D7 PII** (ไม่มี PII). Security Preset = **P3 Master Data** (BRD §16.1).

### D2: Authentication & Session
- ทุก endpoint require JWT + `tax_code.*` permission. Company context ผ่าน `X-Company-Id`.

### D5: Financial (master — no payment)
- `rate`, `gl_*` เปลี่ยน → audit log mandatory (BEFORE/AFTER). ไม่มี payment/bank/MFA operation ใน feature นี้ (downstream Payment = คนละ feature).

### D9: Audit Logging
- ทุก mutation (create/update/activate/deactivate/archive/replacement) → T_tax_code_audit (append-only, 7 ปี, immutable). Audit gap → critical alert (BRD §17.4).

### D15: Admin Actions / SoD
- activate/deactivate/archive logged; Approver identity recorded. SoD create/update ≠ activate/deactivate (S01-04). แนะนำ reason/ticket ต่อ activate/deactivate (S11-02 — ปัจจุบัน HTML ไม่มี ticket field → enhancement note).

### D-CLASS: Data Classification ⭐
Per-field ที่ 04_DB §4.2/§4.6. **Enforcement summary:**

| Layer | Confidential (`gl_*`) | Restricted |
|---|---|---|
| API response | role check (accounting role) | — (ไม่มี field) |
| UI display | แสดงสำหรับ accounting role | — |
| Export/Print | ตาม role | — |
| Audit | log view + mutation | — |

**Wire points:** Policy Center → Data Classification (GL mapping override, audit). **ไม่มี Restricted → ไม่ wire Restricted Resources.** ไม่มี PII → ไม่ wire PDPA consent.

### D17: Multi-Tenant (per-company) Isolation
- PostgreSQL RLS ทุก table ตาม `company_id`; middleware validate `X-Company-Id`; cross-company query forbidden (E18).

---

## §5.8 Compliance & Audit Requirements (BRD §16)

| Requirement | Implementation |
|---|---|
| Immutable Master Data Log (SOX/ITGC S01-07) | append-only audit + no hard delete + immutable used-rate (BR-TAX-02/05) + snapshot immutable (BR-TAX-08) |
| Policy Versioning (S03-02) | replacement lineage (replaces/replaced_by) + effective date = versioning ของอัตรา |
| SoD (COSO S01-04) | Maker ≠ Approver (§5.3) |
| Standardized Audit Content (S06-03) | Who(actor)/What(action)/When(ts) ทุก event |
| Thai Revenue Code (VAT/WHT) | GL role mapping + vat_report_category + income category → ภ.พ.30/ภ.ง.ด. (downstream) |
| Data Retention (no hard delete) | R05/§4.7 |
