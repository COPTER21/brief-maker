# 05_RULES — F-BNK Bank Master (บัญชีธนาคาร)

> **Audience:** Backend developer + QA
> **Purpose:** Business Rules + Validation + Edge Cases + Errors + Security
> **Principle:** Declarative — อ่านแล้วเข้าใจโดยไม่ต้องดูโค้ด
> **Conflict Priority:** LOCK (OQ-BNK-01..04 + GL Contract, Strike 2026-08-11) > BRD business intent > HTML. Enforcement server-side = mirror ของ HTML `saveBank()` + `bulkValidateRow()` (Control C4).

---

## §5.1 Business Rules (BR)

### BR-01: account_no 10–12 หลัก · unique registry-wide (เทียบตัดขีด)
- **Statement:** `account_no` = 10–12 หลัก (ใส่ขีดได้) · **unique ทั้งทะเบียน โดยเทียบแบบตัดขีด** (dash-stripped digits) — ทั้งฟอร์มและไฟล์นำเข้า (รวมซ้ำกันเองในไฟล์)
- **Enforced by:** F-BNK-FN-03 + DB unique index บน `regexp_replace(account_no,'\D','','g')` · Error `ERR_ACCT_INVALID` (นอก 10–12) / `ERR_ACCT_DUPLICATE` (ซ้ำทะเบียน) / `IN_FILE_DUPLICATE` (ซ้ำในไฟล์)
- **Tag:** FIXED · **Ref:** S-05, S-08 · FN-12,19

### BR-02: IR-BNK-01 — used>0 ล็อก ธนาคาร + เลขที่บัญชี · ลบไม่ได้
- **Statement:** `used>0` → ล็อก **ธนาคาร + เลขที่บัญชี** (UI disabled + lock-tag "ล็อก — มีเอกสารผ่านแล้ว" + **logic guard** save ไม่ assign 2 field นี้) · **ลบไม่ได้** (bulk ข้าม) · field อื่น (ชื่อ/สาขา/ประเภท/พร้อมเพย์/กลุ่ม GL/ฝั่ง/★/สถานะ) แก้ได้ปกติ · `used` = count เอกสาร Receipt/PV posted · **ไม่โชว์บนจอ**
- **Enforced by:** F-BNK-FN-02 (save guard) + F-BNK-FN-07 (delete skip) · UI disabled + lock-tag
- **Tag:** FIXED · **Ref:** **OQ-BNK-03 CONFIRMED (LOCK)** · S-04,S-07 · FN-10,11,17

### BR-03: ฝั่ง ≥1 · ★ 1/ฝั่งทั้งระบบ (radio) · DEFAULT_GUARD · หลุด active → ★ หลุด
- **Statement:** เลือกฝั่ง ≥1 (`use_receive || use_pay`) · ★ default ได้ฝั่งละ 1 ตัวทั้งระบบ (radio — ตั้งใหม่ตัวเก่าหลุด) · **DEFAULT_GUARD:** ★ ต้องอยู่ฝั่งที่เปิด + status='active' · **side effect:** หลุดจาก active → `default_receive=false`+`default_pay=false` (★ ทั้ง 2 ฝั่งหลุด)
- **Enforced by:** F-BNK-FN-03 (DEFAULT_GUARD) + F-BNK-FN-08 (radio per-side) + F-BNK-FN-05 (★ drop on non-active) + 2 partial-unique index · Error `ERR_USE_IN_EMPTY` (ไม่เลือกฝั่ง) / `ERR_DEFAULT_GUARD` (★ ผิดเงื่อนไข)
- **Tag:** FIXED · **Ref:** pattern PM (VD-PDM) · S-03,S-06 · FN-07,08,09

### BR-04: GL resolve ผ่าน Bank Posting Group · binding OPTIONAL (view เตือน)
- **Statement:** บัญชี GL เงินฝาก resolve **ผ่าน Bank Posting Group (kind=bank) เท่านั้น** (master ไม่เก็บ COA ตรง) · **binding OPTIONAL** — ไม่ผูกกลุ่ม = บันทึกได้ แต่ view เตือน "ยังไม่ผูก — GL post ไม่ได้จนกว่าจะผูกกลุ่ม" · picker เห็นเฉพาะ active (F-PG BR-06) + คงกลุ่มที่ผูกไว้เดิม (แม้ draft) กันหลุด
- **Enforced by:** F-BNK-FN-14 (picker active-only + keep-bound) · **ไม่มี** validation บล็อก (บันทึกได้) · view warning · GL post enforce ฝั่ง external GL engine
- **Tag:** FIXED · **Ref:** **OQ-BNK-02 = binding OPTIONAL + GL Contract (LOCK)** · S-02 · FN-04,24

### BR-05: Receipt/PV เลือก active + ฝั่งตรง · ★ pre-select · snapshot
- **Statement:** เอกสาร Receipt/PV เลือกได้เฉพาะบัญชี status=active **+ ฝั่งตรง** (Receipt→use_receive / PV→use_pay) · ★ ของฝั่งนั้น pre-select · snapshot ค่าตอนบันทึก
- **Enforced by:** F-BNK-FN-13b (GET /active?side=) — enforce ที่เอกสารปลายทาง (**ยังไม่ทำ**)
- **Tag:** FIXED · **Ref:** **OQ-BNK-04 CONFIRMED (LOCK)** · S-01 · BR-05

### BR-06: promptpay ว่าง / 10 / 13 หลัก
- **Statement:** `promptpay_id` = ว่าง **หรือ** 10 หลัก (เบอร์มือถือ) **หรือ** 13 หลัก (เลขภาษี) เท่านั้น
- **Enforced by:** F-BNK-FN-03 + CHECK constraint · Error `ERR_PROMPTPAY_INVALID`
- **Tag:** FIXED · **Ref:** มาตรฐานพร้อมเพย์ไทย · S-05 · FN-13

### BR-07: นำเข้า merge/append-only · ค่าไทย · default ออมทรัพย์/ทั้งสอง/ร่าง
- **Statement:** นำเข้า **merge/append-only** (ไม่มี Replace) · ค่าไทยในไฟล์ (ธนาคาร/ประเภท/ฝั่ง/สถานะ) · เว้น = ประเภทออมทรัพย์ / ฝั่งทั้งสอง / สถานะร่าง · ไฟล์ **ไม่มี** posting_group/promptpay (ผูกทีหลังในจอ) · แถวผิดถูกข้าม
- **Enforced by:** F-BNK-FN-11 (preview) + F-BNK-FN-12 (commit merge-only) · **Ref:** มติเลน · S-08 · FN-18,20
- **Tag:** FIXED

### BR-08: code unique + UPPERCASE (auto `{bank}-{seq}`)
- **Statement:** `code` unique + เก็บ UPPERCASE · เว้น = auto `{ธนาคาร}-{เลขรัน}` (เช่น KBANK-03) ไม่ชนกัน
- **Enforced by:** F-BNK-FN-03 + F-BNK-FN-09 (auto) + DB UNIQUE(tenant_id, code) · Error `ERR_CODE_DUPLICATE` ("รหัส {code} ถูกใช้แล้ว")
- **Tag:** FIXED · **Ref:** S-05,S-08 · FN-02,12

### BR-09: THB คงที่ (disabled) · ไม่มี multi-currency/SWIFT/IBAN
- **Statement:** สกุลเงิน = THB คงที่ (UI disabled) — ไม่มีตัวเลือกสกุลอื่น, ไม่มี SWIFT/IBAN, ไม่มียอดคงเหลือ/opening balance ใน master
- **Enforced by:** server enforce currency='THB' + CHECK · UI disabled (absence check) · **Ref:** OB-5 (LOCK THB-only) · S-10②③ · FN-05,40
- **Tag:** FIXED

### BR-10: BANKS 9 + ACCT_TYPES 3 = reference config seed
- **Statement:** ธนาคาร 9 ค่า + ประเภทบัญชี 3 ค่า = reference list (Config Table + seed) — ธนาคารนอกชุด (ไฟล์) → BAD_BANK · ประเภทผิด → BAD_TYPE
- **Enforced by:** F-BNK-FN-03 / FN-11 + CHECK enum · Config Table (ขยายได้ Phase 2) · Error `ERR_BAD_BANK` / `ERR_BAD_TYPE`
- **Tag:** CONFIGURABLE 🤖 (reference list อาจขยาย — ห้าม hardcode) · **Ref:** S-01,S-08 · FN-03

---

## §5.2 State Machine (3 สถานะอิสระ — ไม่มีอนุมัติ)

```
        ┌────────────────────────────────┐
        │   draft ⇄ active ⇄ inactive     │   (ทุกทิศ, Finance Admin, ทันที)
        └────────────────────────────────┘
   any (used=0) ──bulk ลบ + confirm──▶ (ลบออกจากทะเบียน)
   any (used>0) ──ลบ──▶ (ถูกข้าม — soft, no hard delete)

   side effect: ออกจาก active (เมนู/bulk/ฟอร์ม) → default_receive=false + default_pay=false (★ หลุด)
```

| From | To | Action | Allowed roles | Conditions / Side effect |
|---|---|---|---|---|
| any | draft/active/inactive | เมนู view / bulk / form / create | Finance Admin | ทุกทิศ, ไม่มีอนุมัติ · ค่าปัจจุบัน disabled |
| active | (draft/inactive) | setStatus / bulkSetStatus / form | System | **★ ทั้ง 2 ฝั่งหลุด** (`default_*=false`) |
| active | — (picker) | ปลายทางเลือก | System | เฉพาะ active + ฝั่งตรง โผล่ใน picker (BR-05) |
| any (used=0) | (deleted) | bulk ลบ + confirm | Finance Admin | used>0 ถูกข้าม |
| any (used>0) | (skipped) | ลบ | System | no hard delete (BR-02) — ปิดบัญชี = inactive แทน |

> **ไม่มี dead path:** HTML ไม่มี archive/reactivate legacy — สถานะจริง = 3 ค่าเท่านั้น.

---

## §5.3 Permission Matrix

| Role | View/ค้นหา | Create | Edit (ธ.+เลขล็อกเมื่อ used>0) | เปลี่ยนสถานะ | ตั้ง ★ Default | นำเข้า/ส่งออก | bulk ลบ (used=0) | เลือกใช้ในเอกสาร |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Finance Master Admin** | ✅ | ✅ | ✅ | ✅ (3 ค่า) | ✅ | ✅ | ✅ | — |
| **Finance Viewer** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | — |
| **Consumer (ปลายทาง Receipt/PV)** | (ผ่าน picker) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (active + ฝั่งตรง) |

> Enforcement server-side (P3 RBAC). Viewer/Consumer เรียก mutation ตรง → **403 ERR_INSUFFICIENT_ROLE** (EC — §5.5 PM edge). Confidential field (account_no) → read access log (C6).

---

## §5.4 Field Validation Rules (mirror `saveBank()` + `bulkValidateRow()`)

### ฟอร์ม (create/edit)
| # | Field | Rule | Error code | HTTP | BR |
|---|---|---|---|---|---|
| 1 | `account_name` | required non-empty | ERR_REQUIRED | 422 | validation |
| 2 | `bank` | ∈ 9 enum | ERR_BAD_BANK | 422 | BR-10 |
| 3 | `account_no` | dash-strip 10–12 หลัก (ข้ามถ้า locked) | ERR_ACCT_INVALID | 422 | BR-01 |
| 4 | `account_no` | unique registry-wide (dash-strip, exclude self) | ERR_ACCT_DUPLICATE | 422/409 | BR-01 |
| 5 | `code` | unique case-insensitive (finalCode หลัง auto) | ERR_CODE_DUPLICATE | 422/409 | BR-08 |
| 6 | `promptpay_id` | ว่าง หรือ 10/13 หลัก | ERR_PROMPTPAY_INVALID | 422 | BR-06 |
| 7 | `use_receive/use_pay` | ≥1 = true | ERR_USE_IN_EMPTY | 422 | BR-03 |
| 8 | `default_receive/pay` | ★ ต้องฝั่งเปิด + status=active | ERR_DEFAULT_GUARD | 422 | BR-03 |

### ไฟล์นำเข้า (per row — เพิ่ม IN_FILE_DUPLICATE)
`REQUIRED` · `BAD_BANK` · `ACCT_INVALID` · `ACCT_DUPLICATE` (ซ้ำทะเบียน) · `BAD_TYPE` · `BAD_USE` (รับ/จ่าย/ทั้งสอง) · `BAD_STATUS` (ใช้งาน/ไม่ใช้งาน/ร่าง) · `CODE_DUPLICATE` · **`IN_FILE_DUPLICATE`** (รหัส/เลขบัญชีซ้ำกันเองในไฟล์)

**Behavior:** ฟอร์ม — ทุกข้อ **block save + ชี้ช่อง (has-err) + (★) toast**; ไฟล์ — แถวผิดถูกข้าม + สรุปสาเหตุ. Server mirror ทุกข้อ. ข้อความ error/toast ห้ามแต่งใหม่ — ยึด HTML (06_TESTS §6.10).
**Cross-field:** DEFAULT_GUARD (★ ⇒ ฝั่งเปิด + active) · account_no dedup dash-strip · IN_FILE_DUPLICATE นอกเหนือ ACCT_DUPLICATE ทะเบียน.

---

## §5.5 Edge Cases (from BRD §10 + Phase 2.5 Lane-Mode probing)

> Lane Mode: probe ที่ไม่มีคำตอบใน BRD → conservative default + tag `[AI-DEFAULT]` + OQ (ไม่ถาม user).

### EC-01: IR-BNK-01 — used>0 lock + save guard (BRD §10.1 confirmed)
- **Scenario:** แก้บัญชีที่ used>0 · ฝืน DOM ลบ `disabled` แล้วเปลี่ยนธนาคาร/เลขบัญชี
- **Resolution:** UI disabled + lock-tag · logic guard (FN-02) save ไม่ assign bank/account_no → ค่าเดิมคงอยู่ (E2E R2 #9) · field อื่นแก้ได้ · ลบถูกข้าม
- **Test:** AT-08, AT-09, AT-15

### EC-02: นิยาม `used` (BRD §10.2 DI / OQ-BNK-07) — **OPEN**
- **Scenario:** `used` นับจากเอกสารใดบ้าง (นับ draft Receipt/PV ด้วยไหม)
- **Resolution `[AI-DEFAULT AD-BNK-01]`:** นับเฉพาะเอกสาร Receipt/PV ที่ **posted/committed** (ไม่นับ draft) — pending **OQ-BNK-07** (blocking delete guard + IR lock trigger จริง)
- **Test:** TC-USED-DEF (verify เมื่อ spec ปิด)

### EC-03: เปลี่ยน type/ฝั่ง ของบัญชี used>0 (BRD §10.2 ST)
- **Scenario:** edit เปลี่ยน account_type/ฝั่ง/★ ของ used>0
- **Resolution:** อนุญาต — ล็อกเฉพาะ ธนาคาร+เลขบัญชี (ไม่ล็อกทั้งใบ) · เอกสารเก่า **snapshot** ไม่ retro
- **Ref:** IR-BNK-01 · **Test:** AT-09

### EC-04: กลุ่ม GL ที่ผูกไว้ถูกเปลี่ยน draft/ลบใน F-PG หลังผูกแล้ว (BRD §10.2 DI)
- **Scenario:** record ผูก SCB (ตอนผูก active) ต่อมา F-PG เปลี่ยน SCB→draft
- **Resolution:** picker **คงกลุ่มที่ผูกไว้เดิม** (union current-bound แม้ draft, FN-14) กัน binding หลุด · resolve ตอน post ต้องตรวจว่ากลุ่มยัง valid (enforce ที่ external GL engine)
- **Test:** AT-12, XT-03

### EC-05: ปลายทางอ้างบัญชีที่เพิ่งเปลี่ยนเป็น inactive ระหว่างสร้างเอกสาร (BRD §10.2 DI)
- **Scenario:** Receipt/PV กำลังสร้าง อ้างบัญชีที่เพิ่งถูกปิด
- **Resolution:** เอกสารที่ snapshot แล้วยังใช้ได้ · picker ใหม่ซ่อน (FN-13b active-only)
- **Test:** XT-02

### EC-06: posting_group source drift (BRD §10.2 CL / OQ-BNK-06) — **OPEN**
- **Scenario:** mock list [KBANK active, SCB draft] ต่างจาก f-postgrp as-built
- **Resolution:** DEV ใช้ generic F-PG-API-01 `?kind=bank&status=active` จริง (คืน KBANK เท่านั้น) — 3 drifts §02_API §2.6 · pending **OQ-BNK-06**
- **Test:** XT-03

### EC-07: กลุ่ม bank ที่ผูกมี account_1 = NULL (BRD §10.2 CL)
- **Scenario:** ผูกกลุ่มแล้ว แต่ F-PG ยังไม่ตั้ง COA เงินฝาก (account_1=NULL)
- **Resolution:** GL post ไม่ได้แม้ผูกกลุ่ม — enforce ฝั่ง external GL engine · view เตือนล่วงหน้า (BR-04)
- **Test:** (downstream GL)

### EC-08: Concurrent ★ set (PR-1 / BRD §10.2 CA) `[AI-DEFAULT]`
- **Scenario:** 2 admin ตั้ง ★ ฝั่งเดียวกันพร้อมกัน
- **Resolution:** Optimistic lock (`If-Match`/version) — first commit ชนะ, second → 409 `ERR_STALE_DATA` · `[AI-DEFAULT AD-BNK-02]` — ยืนยัน OQ-BNK-CC-01
- **Test:** TC-CC-01

### EC-09: Double-submit create (PR-7) `[AI-DEFAULT]`
- **Scenario:** double-click "ยืนยันสร้าง"
- **Resolution:** UI = `#saveBtn is-disabled`/`pointer-events:none` synchronous (E2E R2 #8 — pointer click ที่ 2 timeout) · server = `Idempotency-Key` (production networked)
- **Tag:** `[AI-DEFAULT AD-BNK-02]` · **Test:** TC-ID-01

### EC-10: ไฟล์นำเข้า ≠ .csv (BRD §10.1 confirmed)
- **Resolution:** toast warning "โหมดสาธิตรองรับเฉพาะ .csv…" · ไม่ load · **Test:** AT-17b

### EC-11: PII/masking — เลขบัญชี (BRD §10.2 PII / OQ-BNK-08) — **OPEN**
- **Scenario:** account_no แสดงเต็มในตาราง/def-grid (mask เฉพาะ view header)
- **Resolution:** header mask (`maskAcct`) มีแล้ว · ระดับ masking ในตาราง/def-grid + access log = **OQ-BNK-08** (Security P3)
- **Test:** (Security review)

---

## §5.6 Error Catalog

| Code | HTTP | Message (verbatim/i18n) | Cause / BR |
|---|---|---|---|
| `ERR_NOT_AUTHENTICATED` | 401 | error.auth.unauth | No/invalid token |
| `ERR_INSUFFICIENT_ROLE` | 403 | error.auth.role | Viewer/Consumer เรียก mutation (§5.3) |
| `ERR_NOT_FOUND` | 404 | error.notfound | account id ไม่พบ |
| `ERR_VALIDATION_FAILED` | 400 | error.validation.failed | payload malformed |
| `ERR_REQUIRED` | 422 | "กรุณากรอกชื่อบัญชี" | account_name ว่าง |
| `ERR_BAD_BANK` | 422 | "ธนาคารไม่รู้จัก (BAD_BANK)" | BR-10 |
| `ERR_ACCT_INVALID` | 422 | "เลขบัญชี 10–12 หลัก (ใส่ขีดได้)" | BR-01 (dash-strip นอก 10–12) |
| `ERR_ACCT_DUPLICATE` | 422/409 | "เลขบัญชีนี้มีในทะเบียนแล้ว (ACCT_DUPLICATE)" | BR-01 (ซ้ำทะเบียน dash-strip) |
| `ERR_CODE_DUPLICATE` | 422/409 | "รหัส {code} ถูกใช้แล้ว" | BR-08 |
| `ERR_PROMPTPAY_INVALID` | 422 | "ต้องเป็นเบอร์ 10 หลัก หรือเลขภาษี 13 หลัก" | BR-06 |
| `ERR_USE_IN_EMPTY` | 422 | "ต้องเลือกอย่างน้อย 1 ฝั่ง" | BR-03 |
| `ERR_DEFAULT_GUARD` | 422 | "บัญชีหลักต้องอยู่ฝั่งที่เปิดใช้ และสถานะ "ใช้งาน" เท่านั้น" | BR-03 |
| `ERR_BAD_TYPE` | 422 | "ประเภทบัญชีไม่ถูกต้อง (BAD_TYPE)" | BR-10 (import) |
| `ERR_BAD_USE` | 422 | "ฝั่งใช้งานไม่ถูกต้อง (BAD_USE — รับ/จ่าย/ทั้งสอง)" | BR-07 (import) |
| `ERR_BAD_STATUS` | 422 | "สถานะไม่ถูกต้อง (BAD_STATUS — ใช้ ใช้งาน/ไม่ใช้งาน/ร่าง)" | BR-07 (import) |
| `ERR_IN_FILE_DUPLICATE` | 422 | "รหัส/เลขบัญชีซ้ำในไฟล์ (IN_FILE_DUPLICATE)" | BR-01/07 (import) |
| `ERR_STALE_DATA` | 409 | error.concurrency.stale | EC-08 optimistic lock |
| `ERR_DUPLICATE_IDEMPOTENCY_KEY` | 409 | error.idempotency.dup | EC-09 |

---

## §5.7 Security Bible Application

> Domains triggered: **D2, D5, D9, D11, D15, D17** (D7 PII overlay = account_no/promptpay). Preset **P3 Master Data** + ยกระดับ masking/access-log (BRD §16).

### D2: Authentication & Session
- ทุก endpoint require JWT · RBAC: Finance Admin vs Viewer vs Consumer

### D5: Financial Config
- Bank Master = ทะเบียนบัญชีเงินฝากส่วนกลาง — ทุกการแก้ → audit log mandatory · ควบคุมเชิงเงิน (P4) บังคับที่**เอกสารปลายทาง** (Receipt/PV/GL)

### D9: Audit Logging
- ทุก mutation (create/edit/status/bulk/import/delete) → change log (append-only, tab ประวัติ) · diff before/after

### D11: Data Masking (Sensitive)
- `account_no` mask ที่ view header (`maskAcct` → `xxx-x-xx…`) · `promptpay_id` (เลขภาษี) อ่อนไหว · read access log สำหรับ Confidential (C6/C11) · ระดับ masking ตาราง/def-grid = **OQ-BNK-08**

### D15: Admin Actions
- ทุก status transition + ★ change + bulk delete + import batch logged พร้อม actor + timestamp · **ไม่มี** approver (DOA null)

### D17: Multi-Tenant Isolation
- PostgreSQL RLS by tenant_id · API middleware validate X-Tenant-Id · cross-tenant forbidden

### D-CLASS: Data Classification
- Feature = **Confidential** (มี account_no/promptpay_id อ่อนไหว — ดู 04_DB §4.6)

| Layer | Enforcement |
|---|---|
| API | JWT auth + role re-check · read-access-log สำหรับ account_no |
| UI | account_no mask ที่ view header · Viewer read-only |
| Audit | mutation log + read access log (Confidential) |

**Wire points:** DOA placeholder (null) → Policy Center (future). ไม่มี Restricted field (ไม่ต้อง register Restricted Resources) · Confidential masking level = OQ-BNK-08.

### D-domain N/A
- **DOA/Approval:** N/A (master no-approval) · **NOTIF:** ไม่ emit

---

## §5.8 Compliance & Audit
| Requirement | Implementation |
|---|---|
| ควบคุมการแก้ทะเบียนบัญชีการเงิน | C1 RBAC + C2/C6 audit/access log |
| Snapshot integrity | C7 — Receipt/PV เก็บ snapshot ไม่ผูก FK |
| No hard delete | C5 — used>0 guard + soft (inactive = ปิดบัญชี) |
| Field-level lock (ธนาคาร+เลขบัญชี) | C8 — IR-BNK-01 (UI disabled + logic guard) |
| Data masking (sensitive) | C11 — account_no mask ที่ view header |
| Server-side validation | C4 — mirror saveBank()/bulkValidateRow() |
| Unique key enforcement | C3 — account_no (dash-strip) + code unique |
