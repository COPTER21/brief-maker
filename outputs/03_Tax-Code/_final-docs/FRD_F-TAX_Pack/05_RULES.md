# 05_RULES — F-TAX ทะเบียนรหัสภาษี (Tax Code Master)

> **Audience:** Backend developer + QA
> **Purpose:** Business Rules + State Machine + Validation + Edge Cases + Errors + Security
> **Principle:** Declarative — อ่านแล้วเข้าใจโดยไม่ต้องดูโค้ด
> ทุก BR = **FIXED** (business/accounting invariant, ล็อกด้วยมติ+STD — ดู 00_OVERVIEW §0.11). ไม่มี rule ระดับ CONFIGURABLE/Engine.

---

## §5.1 Business Rules (BR)

### BR-01: รหัสห้ามซ้ำ (case-insensitive)
- **Statement:** `code` ต้องไม่ซ้ำภายใน tenant แบบไม่สนตัวพิมพ์ (vat7 == VAT7) — สร้าง/แก้/นำเข้า
- **Enforced by:** F-TAX-FN-04 (app) + **DB unique index `(tenant_id, lower(code))`** (กัน concurrent EC-A3)
- **Error:** ERR_CODE_DUPLICATE → 409 · msg "รหัส {code} ถูกใช้แล้ว" (form) / "รหัสซ้ำ (CODE_DUPLICATE)" (import)
- **Trace:** S-07, S-08 · EC-01

### BR-02: อัตรา 0–100 ทศนิยมได้
- **Statement:** `rate` ต้องเป็นตัวเลข 0 ≤ rate ≤ 100 (ทศนิยม 2 ตำแหน่ง `[AI-DEFAULT ← EC-A5]`)
- **Enforced by:** F-TAX-FN-04 + DB CHECK (rate 0–100)
- **Error:** RATE_INVALID → 400/422 · msg "กรุณากรอกอัตรา 0–100" (form) / "อัตราไม่ถูกต้อง 0–100 (RATE_INVALID)" (import)
- **Trace:** S-07, S-08 · EC-02, EC-04

### BR-03: ประเภทยกเว้นภาษี → อัตรา = 0 เสมอ  `[LOCK-EXEMPT-0]`
- **Statement:** `category='exempt'` → `rate=0` บังคับ (UI ล็อก + logic force + import validate + DB CHECK)
- **Enforced by:** UI `onTypeChange` · F-TAX-FN-04 (force 0) · F-TAX-FN-09 (import) · DB `CHECK (category<>'exempt' OR rate=0)`
- **Error:** EXEMPT_RATE (import) "ยกเว้นภาษีต้องอัตรา 0 (EXEMPT_RATE)" · BR_EXEMPT_RATE (API 422)
- **Trace:** S-02, S-08 · EC-03

### BR-04: IR-TAX-01 — `used>0` ล็อกรหัส/อัตรา/ประเภท  `[LOCK-IR-TAX-01]`
- **Statement:** record ที่ `used_count > 0` → แก้ `code`/`rate`/`category` ไม่ได้ (UI disabled + **server logic guard**) — แก้ได้เฉพาะ `name_th`/`name_en`/`status`
- **Enforced by:** UI lock-tag "ล็อก — ถูกใช้งานแล้ว" + F-TAX-FN-03 (คงค่าเดิม 3 field เสมอแม้ payload ฝืน)
- **Rationale:** เอกสารเก่าอ้างอัตราเดิมถูกต้องตลอดกาล (accounting integrity) — อยากได้อัตราใหม่ = สร้างรหัสใหม่ + ปิดตัวเก่า
- **Trace:** S-04 · EC-07 · KPI-02 (0 persist violations)

### BR-05: `used>0` ลบไม่ได้ — bulk ข้าม  `[LOCK-BULK-DEL]`
- **Statement:** ไม่มีลบเดี่ยว; ลบผ่าน bulk-delete เท่านั้น (ผ่าน confirm) — ตัว `used_count>0` ถูกข้าม พร้อมแจ้งยอด
- **Enforced by:** F-TAX-FN-07 (partition del/skip)
- **Trace:** S-06 · EC-06 · ⚠️ พึ่ง used จริง (OQ-TAX-04, EC-A7)

### BR-06: สถานะ 3 ค่าเปลี่ยนอิสระทุกทิศ ไม่มีอนุมัติ  `[LOCK-STATUS-FREE]`
- **Statement:** draft/active/inactive เปลี่ยนได้ทุกทิศทันที (view menu / bulk / form / import) — ไม่มี gate/approval; ค่าปัจจุบัน disabled ในเมนู
- **Enforced by:** F-TAX-FN-06 · ดู §5.2
- **Trace:** S-05

### BR-07: ปลายทางเลือกได้เฉพาะ "ใช้งาน"  `[LOCK-SOFT-REF]`
- **Statement:** combobox downstream (Item Master/เอกสาร) เห็นเฉพาะ `status='active'` — draft/inactive ซ่อน
- **Enforced by:** F-TAX-API-10 lookup (force active) · F-TAX-FN-05 active_only
- **Trace:** S-05 · XT-01

### BR-08: นำเข้า — ตรวจรายแถว, แถวผิดข้าม, status ว่าง=ร่าง
- **Statement:** import validate ทุกแถวอิสระ (แถวผิดข้าม ไม่ล้มไฟล์); `status` ว่าง = `draft`; `type` ใช้ชื่อไทย
- **Enforced by:** F-TAX-FN-08 + F-TAX-FN-09 (6 codes)
- **Trace:** S-08 · EC-05

### BR-09: ไม่เก็บบัญชี GL  `[LOCK-NO-GL]`
- **Statement:** ไม่มี field/endpoint เลขบัญชี GL — mapping code→GL อยู่ที่ GL Posting Setup
- **Enforced by:** absence (04_DB ไม่มี field · 02_API ไม่มี endpoint)
- **Trace:** S-10③

### BR-10: audit ผู้สร้าง/ผู้แก้ + เวลา
- **Statement:** ทุก mutation บันทึก created_by/at + updated_by/at (แสดง tab ประวัติ)
- **Enforced by:** ทุก Function mutation + audit middleware
- **Trace:** ทุก S · FN-93

---

## §5.2 State Machine  `[LOCK-STATUS-FREE]`

```
   ร่าง(draft) ⇄ ใช้งาน(active) ⇄ ไม่ใช้งาน(inactive)
        ▲__________________________________│
        (ทุกทิศทาง · ไม่มี gate · ไม่มีอนุมัติ)
```

| From | To | Action | Allowed roles | Conditions |
|---|---|---|---|---|
| any (draft/active/inactive) | any อื่น | view menu / bulk bar / form / import | tax_admin | **ไม่มีเงื่อนไข** (อิสระ) · ค่าปัจจุบัน disabled ในเมนู |

- Default: form create → `active` · import status ว่าง → `draft` (BR-08)
- **ผลปลายทาง:** เฉพาะ `active` โผล่ lookup (BR-07). เปลี่ยน active→inactive ตัวที่ used>0 = อนุญาต (สถานะอิสระ) แต่กระทบปลายทางเลือกใหม่เท่านั้น (EC-A6) — เอกสารเดิมคงค่าเดิม.
- Lifecycle STD ของอัตราใหม่: สร้างรหัสใหม่(ร่าง) → ทดสอบ → ใช้งาน → ปิดตัวเก่าเป็นไม่ใช้งาน

---

## §5.3 Permission Matrix

| Role | ดู List/รายละเอียด | สร้าง | แก้ used=0 | แก้ชื่อ/สถานะ used>0 | เปลี่ยนสถานะ (เดี่ยว/bulk) | นำเข้า/ส่งออก | ลบ bulk |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| tax_admin (บัญชี) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| consumer (Sales/สินค้า/เอกสาร) | เห็นเฉพาะ active ผ่าน lookup | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

> ⚠️ ปัจจุบัน mock user เดียวเปิดหมด — RBAC จริง deferred → **OQ-TAX-06** `[AI-DEFAULT]`.

---

## §5.4 Field Validation Rules

| VR | Field/Action | เงื่อนไข | ประเภท | ข้อความ (verbatim จาก HTML) |
|---|---|---|---|---|
| VR-01 | name_th (บันทึก) | ว่าง | Error | "กรุณากรอกชื่อภาษาไทย" |
| VR-02 | code (บันทึก) | ซ้ำ case-insensitive | Error | "รหัส {code} ถูกใช้แล้ว" |
| VR-03 | rate (บันทึก) | ว่าง / NaN / <0 / >100 | Error | "กรุณากรอกอัตรา 0–100" |
| VR-04 | category=exempt | เปลี่ยนประเภท | Trigger | set rate 0 + disable + tag "ยกเว้นภาษี = อัตรา 0" |
| VR-05 | ปุ่มบันทึก | double-submit | Prevent | loader "กำลังบันทึก…" (กันกดซ้ำ + Idempotency-Key) |
| VR-06..11 | import รายแถว | 6 กรณี | Skip row | ดู §5.6 |

---

## §5.5 Edge Cases (confirmed จาก BRD §10.1 — มีใน HTML)

| # | Scenario | Resolution | Test |
|---|---|---|---|
| EC-01 | รหัสซ้ำต่างตัวพิมพ์ (vat7 vs VAT7) | case-insensitive → บล็อก/ข้าม CODE_DUPLICATE (BR-01, DB lower(code)) | AT-11 |
| EC-02 | อัตรา=120 (import WHT99) | RATE_INVALID ข้ามแถว (BR-02) | AT-16 |
| EC-03 | ยกเว้นภาษี + อัตรา≠0 (import) | EXEMPT_RATE ข้ามแถว (BR-03) | AT-16 |
| EC-04 | อัตราทศนิยม 0.75 (WHT075) | รับได้ (numeric(5,2)) | AT-15 |
| EC-05 | import status ว่าง (VAT9) | = draft (BR-08) | AT-14 |
| EC-06 | bulk ลบผสม used>0 กับ used=0 | ลบเฉพาะ used=0, ข้าม used>0 + toast (BR-05) | AT-10 |
| EC-07 | แก้ตัว used>0 แล้วฝืน submit | server guard คงค่าเดิม 3 field (BR-04, F-TAX-FN-03) | AT-06 |
| EC-08 | นำเข้าไฟล์ที่ไม่ได้เลือก | ไม่ preview (ตรวจ file จริงก่อน) | AT-13 |

### Edge Cases (AI-pattern §10.2 — ยกเป็น OQ, ยังไม่ resolve)
| # | Edge | สถานะ |
|---|---|---|
| EC-A1 | CSV encoding ไม่ใช่ UTF-8 / คอลัมน์สลับ / header หาย | → OQ-TAX-IMPORT-PARSE (parser จริง) |
| EC-A2 | ไฟล์ import พันแถว | throttle/paginate preview (แนะนำ) |
| EC-A3 | 2 คนสร้างรหัสเดียวกันพร้อมกัน | `[AI-DEFAULT]` DB unique constraint → 409 (BR-01) · OQ-TAX-CONCURRENCY |
| EC-A5 | rate ทศนิยมยาว 0.756 | `[AI-DEFAULT]` precision 2 (numeric(5,2)) · OQ-TAX-RATE-PREC |
| EC-A7 | ลบตัวที่ปลายทางอ้างจริง แต่ used mock=0 | 🚨 ต้อง sync used จริงก่อน enable hard-delete → **OQ-TAX-04** (ข้อมูลสูญหาย) |

---

## §5.6 Error Catalog

### API errors
| Code | HTTP | Message (i18n key) | Cause |
|---|---|---|---|
| ERR_VALIDATION_FAILED | 400 | error.validation.failed | name/rate ผิด |
| ERR_NOT_AUTHENTICATED | 401 | error.auth.unauth | no/invalid token |
| ERR_INSUFFICIENT_ROLE | 403 | error.auth.role | role mismatch (deferred OQ-TAX-06) |
| ERR_NOT_FOUND | 404 | error.notfound | record หาย |
| ERR_CODE_DUPLICATE | 409 | error.taxcode.dup | code ซ้ำ (BR-01) |
| ERR_STALE_DATA | 409 | error.concurrency.stale | version mismatch (PR-2) |
| ERR_DUPLICATE_IDEMPOTENCY_KEY | 409 | error.idempotency.dup | same key different body |
| ERR_INVALID_STATUS | 400 | error.taxcode.status | status นอก enum |
| BR_EXEMPT_RATE | 422 | br.taxcode.exempt.rate | exempt+rate≠0 (BR-03) |

### Import row error codes (6 — verbatim message จาก HTML)
| Code | Message |
|---|---|
| REQUIRED | "ข้อมูลบังคับไม่ครบ (REQUIRED)" |
| BAD_TYPE | "ประเภทไม่ถูกต้อง (BAD_TYPE)" |
| RATE_INVALID | "อัตราไม่ถูกต้อง 0–100 (RATE_INVALID)" |
| EXEMPT_RATE | "ยกเว้นภาษีต้องอัตรา 0 (EXEMPT_RATE)" |
| BAD_STATUS | "สถานะไม่ถูกต้อง (BAD_STATUS — ใช้ ใช้งาน/ไม่ใช้งาน/ร่าง)" |
| CODE_DUPLICATE | "รหัสซ้ำ (CODE_DUPLICATE)" |

---

## §5.7 Security Bible Application

> Preset **P3 — Master Data (10 controls)** `[AI-DEFAULT ← BRD §16.1]`. Domains: Access Control, Audit, Data Integrity, Input Validation. **ไม่ trigger:** PII/Encryption, Approval/SoD.

### Access Control (RBAC)
- ทุก write op ต้อง gate role tax_admin — **deferred → OQ-TAX-06** (mock เปิดหมด)
- consumer เห็นเฉพาะ lookup (active) — read-only

### Audit Trail
- ทุก mutation → audit (who/when + diff). Retention: master data เก็บถาวร.

### Data Integrity
- Unique constraint case-insensitive (C-03, กัน concurrent)
- **IR-TAX-01 guard (C-04)** — server คงค่าเดิม 3 field เมื่อ used>0 (ไม่ใช่แค่ UI disable) — KPI-02 = 0 persist violations
- exempt→0 CHECK (C-05)

### Input Validation
- server-side ด้วย ไม่ใช่แค่ UI (rate/exempt/dup); import validate รายแถว isolation (C-08 — แถวผิดไม่ล้มไฟล์)
- Export safe: BOM + escape `",\n` (C-07)

### D-CLASS: Data Classification
Per-field ที่ 04_DB §4.2/§4.6 — **ทั้งหมด Internal** (ไม่มี Confidential/Restricted/PII).
| Layer | Internal fields |
|---|---|
| API | JWT auth |
| UI | แสดงปกติ (authenticated) |
| Export | ทุก internal role |
| Audit | mutation log |

**Wire points:** ไม่มี Restricted Resources ต้อง register. DOA placeholder (approver_*) → Policy Center อนาคต (ปัจจุบัน null).

### ไม่ applicable
- Approval/SoD: **N/A** (LOCK-DOA-NULL — ไม่มี approval workflow)
- PII/Encryption: **N/A** (ไม่มี PII field)

---

## §5.8 Compliance & Audit Requirements

| Requirement | Implementation |
|---|---|
| Accounting integrity (บิลเก่าอ้างอัตราถูกตลอด) | BR-04 IR-TAX-01 guard |
| อัตราภาษีไทยมาตรฐาน (seed) | BRD §13 seed: VAT7/VAT0/NONVAT/WHT 1/2/3/5/10/15 |
| Import correctness (≥90% แถวผ่าน) | BR-08 + 6 codes (KPI-03) |
| Audit trail | BR-10 + T_tax_code audit cols |
| Data privacy (PDPA) | N/A (ไม่มี PII) |
