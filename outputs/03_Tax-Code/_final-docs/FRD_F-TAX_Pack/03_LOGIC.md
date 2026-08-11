# 03_LOGIC — F-TAX ทะเบียนรหัสภาษี (Tax Code Master)

> **Audience:** BE dev (business logic layer)
> **Scope:** All non-HTTP business logic — functions, validations, guards, import/export
> **CUBIC alignment:** §3.1 Functions = scope-local · §3.2 Engines = **none** (ไม่มี logic ที่ pure+reusable+substantial ในระดับ engine — VAT/WHT calc เกิด downstream ที่ B2 line editor ไม่ใช่ที่นี่)
> **Iron Rule R8:** ทุก mutation API trace ไป ≥1 Function ใน §3.3

---

## §3.1 Functions (Scope-Local)

### F-TAX-FN-01: `createTaxCode`
- **Purpose:** สร้าง record รหัสภาษีใหม่จาก input ที่ validate แล้ว (S-01)
- **Input:** `{ code?, name_th, name_en?, category, rate, status }`
- **Output:** `TaxCode | ValidationError[]`
- **Invoked by:** F-TAX-API-02 POST /tax-codes
- **Calls:** F-TAX-FN-02 (generateAutoCode ถ้า code ว่าง), F-TAX-FN-04 (validate)
- **Side effects:** INSERT T_tax_code (`used_count`:0, `version`:1, `approver_*`:null) · audit created_by/at
- **Error cases:** ERR_VALIDATION_FAILED, ERR_CODE_DUPLICATE, BR_EXEMPT_RATE
- **Iron rule check:** ✅ no HTTP terms

### F-TAX-FN-02: `generateAutoCode`
- **Purpose:** สร้างรหัสอัตโนมัติเมื่อผู้ใช้เว้นว่าง — `VATxx`/`WHTxx`/`TAXxx` ตามประเภท ไม่ชนของเดิม (FN-02)
- **Input:** `{ category }`
- **Output:** `string` (เช่น "WHT01")
- **Logic:** base = `{vat:'VAT', wht:'WHT', exempt:'TAX'}[category]`; loop `i=1..` → `base + pad2(i)` จน unique (case-insensitive check กับ existing)
- **Invoked by:** F-TAX-FN-01, F-TAX-FN-08 (import ถ้า code ว่าง — *ปัจจุบัน import บังคับ code, ดู FN-09*)
- **Calls:** —
- **Side effects:** — (pure read ของ existing codes)
- **Iron rule check:** ✅

### F-TAX-FN-03: `updateTaxCode` ⭐ (IR-TAX-01 guard)
- **Purpose:** แก้ไข record — **บังคับ guard ตาม used_count** (S-03/S-04, BR-04, EC-07)
- **Input:** `{ id, code, name_th, name_en?, category, rate, status, expected_version }`
- **Output:** `TaxCode | GuardResult | ValidationError[]`
- **Logic:**
  1. load record; check `version === expected_version` (else ERR_STALE_DATA)
  2. **if `used_count > 0`:** persist เฉพาะ `name_th`/`name_en`/`status` — **คงค่า `code`/`rate`/`category` เดิมเสมอ** (ไม่สน payload — server guard, ไม่ใช่แค่ UI disable)
  3. **else (`used_count = 0`):** validate (FN-04) แล้ว persist ทุก field
  4. version++ · audit updated_by/at
- **Invoked by:** F-TAX-API-04 PUT /tax-codes/:id
- **Calls:** F-TAX-FN-04 (เมื่อ used=0)
- **Side effects:** UPDATE T_tax_code · audit
- **Error cases:** ERR_NOT_FOUND, ERR_STALE_DATA, ERR_CODE_DUPLICATE, ERR_VALIDATION_FAILED
- **Iron rule check:** ✅ · **enforce LOCK-IR-TAX-01**

### F-TAX-FN-04: `validateTaxCodeInput`
- **Purpose:** validation รวมศูนย์ create/edit(used=0) — ใช้ ≥2 จุด (BR-01/02/03, VR-01..03)
- **Input:** `{ id?, code(final), name_th, category, rate }`
- **Output:** `ValidationError[]` (ว่าง = ผ่าน)
- **Logic:**
  1. `name_th` ว่าง → NAME_REQUIRED ("กรุณากรอกชื่อภาษาไทย")
  2. code ซ้ำ (case-insensitive, ยกเว้น self id) → CODE_DUPLICATE ("รหัส {code} ถูกใช้แล้ว")
  3. `category==='exempt'` → **force `rate=0`** (LOCK-EXEMPT-0); else rate ต้อง 0–100 (ว่าง/NaN/<0/>100 → RATE_INVALID "กรุณากรอกอัตรา 0–100")
- **Invoked by:** F-TAX-FN-01, F-TAX-FN-03
- **Calls:** —
- **Side effects:** — (pure)
- **Iron rule check:** ✅

### F-TAX-FN-05: `buildTaxCodeListQuery`
- **Purpose:** สร้าง query filter+sort+paginate สำหรับ list และ lookup (rate/used sort เชิงตัวเลข)
- **Input:** `{ search?, category?, status?, sort, dir, page, page_size, active_only? }`
- **Output:** `{ rows, stats:{total,active,inactive,draft}, total, page, page_size }`
- **Logic:** filter (category/status/search hay=code+name_th+name_en+"{rate}%") → sort (numeric สำหรับ rate/used, ไม่งั้น string lower) → slice หน้า. `active_only` (lookup) บังคับ status='active'.
- **Invoked by:** F-TAX-API-01, F-TAX-API-10 (active_only=true)
- **Calls:** —
- **Side effects:** — (read-only)
- **Iron rule check:** ✅

### F-TAX-FN-06: `changeTaxCodeStatus`
- **Purpose:** เปลี่ยนสถานะอิสระทุกทิศ ไม่มี gate (S-05, BR-06, LOCK-STATUS-FREE) — ใช้ทั้งเดี่ยว/bulk
- **Input:** `{ id, status }` (bulk = loop ids)
- **Output:** `TaxCode | { changed:number }`
- **Logic:** ถ้า status == ปัจจุบัน → no-op (ไม่นับ changed); else set status + audit. ไม่มีตรวจ transition (ทุกทิศ allowed).
- **Invoked by:** F-TAX-API-05, F-TAX-API-06
- **Calls:** —
- **Side effects:** UPDATE status + audit
- **Iron rule check:** ✅

### F-TAX-FN-07: `bulkDeleteTaxCodes`
- **Purpose:** ลบหลายตัว — **`used_count>0` ถูกข้าม** (S-06, BR-05, EC-06)
- **Input:** `{ ids[] }`
- **Output:** `{ deleted:number, skipped:number, skipped_ids[] }`
- **Logic:** partition ids → `used_count>0` = skip, else delete. DELETE เฉพาะ del set + audit. คืนยอด deleted/skipped.
- **Invoked by:** F-TAX-API-07 POST /bulk-delete
- **Calls:** —
- **Side effects:** DELETE T_tax_code (used=0 only) · audit
- **Iron rule check:** ✅ · **enforce LOCK-BULK-DEL** · ⚠️ พึ่ง used_count จริง (OQ-TAX-04)

### F-TAX-FN-08: `importTaxCodes`
- **Purpose:** orchestrate นำเข้า CSV — parse → validate รายแถว → (preview | commit) (S-08, BR-08)
- **Input:** `{ file, mode:'preview'|'commit' }`
- **Output:** `{ total, ok, error, rows[] }` (preview) | `{ imported, skipped }` (commit)
- **Logic:**
  1. parse CSV (⚠️ parser จริงต้อง validate header/encoding — OQ-TAX-IMPORT-PARSE)
  2. map `type`(ชื่อไทย)→category, `status`(ชื่อไทย)→status (ว่าง→draft, BR-08)
  3. ทุกแถวผ่าน F-TAX-FN-09 → เก็บ err/ok
  4. preview: คืนผลตรวจ (ไม่เขียน); commit: INSERT เฉพาะแถว ok (แถวผิดข้าม ไม่ล้มไฟล์)
- **Invoked by:** F-TAX-API-08 POST /import
- **Calls:** F-TAX-FN-09 (validateImportRow), F-TAX-FN-02 (ถ้าอนุญาต auto-code — ปัจจุบัน import บังคับ code)
- **Side effects (commit):** INSERT หลายแถว (used_count:0, approver_*:null) · audit
- **Iron rule check:** ✅

### F-TAX-FN-09: `validateImportRow`
- **Purpose:** ตรวจ 1 แถว import → คืน 1 ใน 6 error codes หรือ null (BR-08, EC-01..05)
- **Input:** `{ code, name_th, name_en?, type(ชื่อไทย), rate, status? }`
- **Output:** `string(errorMessage) | null`
- **Logic (ลำดับตรวจ verbatim จาก HTML `bulkValidateRow`):**
  1. code/name_th/type/rate ว่าง → **REQUIRED** "ข้อมูลบังคับไม่ครบ (REQUIRED)"
  2. type ไม่ match ชื่อไทย 3 ค่า → **BAD_TYPE** "ประเภทไม่ถูกต้อง (BAD_TYPE)"
  3. rate NaN/<0/>100 → **RATE_INVALID** "อัตราไม่ถูกต้อง 0–100 (RATE_INVALID)"
  4. type=exempt & rate≠0 → **EXEMPT_RATE** "ยกเว้นภาษีต้องอัตรา 0 (EXEMPT_RATE)"
  5. status ระบุแต่ไม่ใช่ ใช้งาน/ไม่ใช้งาน/ร่าง → **BAD_STATUS** "สถานะไม่ถูกต้อง (BAD_STATUS — ใช้ ใช้งาน/ไม่ใช้งาน/ร่าง)"
  6. code ซ้ำ (case-insensitive) → **CODE_DUPLICATE** "รหัสซ้ำ (CODE_DUPLICATE)"
- **Invoked by:** F-TAX-FN-08
- **Calls:** —
- **Side effects:** — (pure)
- **Iron rule check:** ✅

### F-TAX-FN-10: `exportTaxCodesCsv`
- **Purpose:** สร้าง CSV ตาม filter ปัจจุบัน — 7 คอลัมน์ + BOM (S-09, FN-20)
- **Input:** `{ filter (เหมือน list) }`
- **Output:** `CSV string` (นำหน้า `﻿` BOM)
- **Logic:** getFiltered → head `code,name_th,name_en,type,rate,status,used_in` → map (type=catLabel, status=statusLabel ไทย, used_in=used_count) → escape `",\n`.
- **Invoked by:** F-TAX-API-09 GET /export
- **Calls:** F-TAX-FN-05 (filter)
- **Side effects:** — (read-only)
- **Iron rule check:** ✅

### F-TAX-FN-11: `getTaxCodeUsage`
- **Purpose:** คืนจำนวนที่ถูกอ้างอิง (tab การใช้งาน) (S-11, FN-23)
- **Input:** `{ id }`
- **Output:** `{ used_count:number }`
- **Logic:** **ปัจจุบัน = อ่าน `used_count` mock**. ⚠️ ของจริง = derived count จากสินค้า(กลุ่มภาษี) + เอกสารทุกใบที่อ้าง code (OQ-TAX-04) — ห้ามเปิด hard-delete/รายงานความถูกต้องจนกว่า sync.
- **Invoked by:** F-TAX-API-03 (view detail)
- **Calls:** —
- **Side effects:** — (read-only)
- **Iron rule check:** ✅

---

## §3.2 Engines (Reusable / CUBIC-Registered)

> **ไม่มี engine ใน feature นี้** — logic ทั้งหมดเป็น scope-local Functions ใน §3.1.
> เหตุผล (Logic Placement Matrix tie-breaker): logic ที่มี = CRUD/validate/import/export/status/guard — ทุกตัวเป็น scope-local (ใช้แค่ F-TAX, ไม่ pure calc reusable). การคำนวณ VAT/WHT จริงเกิดที่ **downstream B2 line editor** ของเอกสาร (คนละ feature) ไม่ใช่ที่นี่ → ไม่มี engine candidate.

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| F-TAX-API-01 | GET | /tax-codes | F-TAX-FN-05 (list query) | — |
| F-TAX-API-02 | POST | /tax-codes | F-TAX-FN-01 (create), FN-02 (auto-code), FN-04 (validate) | — |
| F-TAX-API-03 | GET | /tax-codes/:id | F-TAX-FN-11 (usage) | — |
| F-TAX-API-04 | PUT | /tax-codes/:id | F-TAX-FN-03 (update+guard), FN-04 (validate if used=0) | — |
| F-TAX-API-05 | PATCH | /:id/status | F-TAX-FN-06 (status) | — |
| F-TAX-API-06 | POST | /bulk-status | F-TAX-FN-06 (status loop) | — |
| F-TAX-API-07 | POST | /bulk-delete | F-TAX-FN-07 (bulk delete skip used>0) | — |
| F-TAX-API-08 | POST | /import | F-TAX-FN-08 (orchestrate), FN-09 (validate row) | — |
| F-TAX-API-09 | GET | /export | F-TAX-FN-10 (csv) | — |
| F-TAX-API-10 | GET | /lookup | F-TAX-FN-05 (active_only) | — |

### Trace Verification (Self-Check)
- [x] **Every mutation API** (02/04/05/06/07/08) has ≥1 Function ✅
- [x] **No orphan Function** — FN-01..FN-11 ทุกตัวปรากฏใน trace ✅
- [x] **No orphan Engine** — ไม่มี engine ✅
- [x] **No hidden logic in 02_API** — CRUD/validate/import/guard อยู่ที่นี่ทั้งหมด ✅

---

## §3.4 Dependencies

### External Function/Engine called
- ไม่มี (feature standalone; ไม่เรียก engine/feature อื่น)

### External that calls into this feature
- Downstream (Item Master / เอกสาร / GL) เรียก **F-TAX-API-10 lookup** (pull) — ไม่เรียก Function ตรง

---

## §3.5 Open Questions / Locked Decisions Referenced

- **OQ-TAX-04:** F-TAX-FN-11 `getTaxCodeUsage` + F-TAX-FN-07 guard พึ่ง `used_count` จริง — ปัจจุบัน mock
- **OQ-TAX-RATE-PREC:** FN-04 rate precision = 2 ทศนิยม `[AI-DEFAULT]` (numeric(5,2))
- **OQ-TAX-IMPORT-PARSE:** FN-08 parser จริงต้อง validate header/encoding
- **LOCK-IR-TAX-01** → enforce ที่ FN-03 (server guard) · **LOCK-EXEMPT-0** → FN-04 · **LOCK-BULK-DEL** → FN-07 · **LOCK-STATUS-FREE** → FN-06
