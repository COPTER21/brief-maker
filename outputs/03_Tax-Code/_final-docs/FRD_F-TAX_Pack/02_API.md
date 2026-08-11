# 02_API — F-TAX ทะเบียนรหัสภาษี (Tax Code Master)

> **Audience:** Backend developer (HTTP layer)
> **Purpose:** API contracts — HTTP layer only
> **🚨 Iron Rule:** ห้ามมี business logic >5 lines ที่นี่ — ย้ายไป 03_LOGIC §3.1
> **🚨 R8:** ทุก mutation API ระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3
> **Note:** prototype = client-side mock. contracts ด้านล่าง = production spec (soft-ref, IR-TAX-01 server guard, unique constraint).

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth |
|---|---|---|---|---|
| F-TAX-API-01 | GET | /api/v1/tax-codes | List + filter/sort/paginate | required |
| F-TAX-API-02 | POST | /api/v1/tax-codes | สร้างรหัสภาษี | required (tax_admin) |
| F-TAX-API-03 | GET | /api/v1/tax-codes/:id | รายละเอียด (view drawer) | required |
| F-TAX-API-04 | PUT | /api/v1/tax-codes/:id | แก้ไข (IR-TAX-01 guard) | required (tax_admin) |
| F-TAX-API-05 | PATCH | /api/v1/tax-codes/:id/status | เปลี่ยนสถานะ (เดี่ยว) | required (tax_admin) |
| F-TAX-API-06 | POST | /api/v1/tax-codes/bulk-status | เปลี่ยนสถานะ bulk | required (tax_admin) |
| F-TAX-API-07 | POST | /api/v1/tax-codes/bulk-delete | ลบ bulk (skip used>0) | required (tax_admin) |
| F-TAX-API-08 | POST | /api/v1/tax-codes/import | นำเข้า CSV (validate รายแถว) | required (tax_admin) |
| F-TAX-API-09 | GET | /api/v1/tax-codes/export | ส่งออก CSV (ตาม filter, BOM) | required (tax_admin) |
| F-TAX-API-10 | GET | /api/v1/tax-codes/lookup | Downstream lookup (status=active) | required |

> role `tax_admin` = placeholder; RBAC จริง deferred → OQ-TAX-06 (ปัจจุบัน mock เปิดหมด).
> **ไม่มี** endpoint ลบเดี่ยว (LOCK-BULK-DEL) · ไม่มี field/endpoint GL (LOCK-NO-GL) · ไม่มี approval endpoint (LOCK-DOA-NULL) · ไม่มี event emit (LOCK-NO-NOTIF).

---

## §2.2 Per-API Contract

### F-TAX-API-01: GET /api/v1/tax-codes

| Field | Value |
|---|---|
| method / path | GET /api/v1/tax-codes |
| summary | List with search + filter + sort + pagination |
| auth / roles | required · tax_admin |

**Request — Query params:**
- `search` (optional): match `code` / `name_th` / `name_en` / `{rate}%` (case-insensitive)
- `category` (optional): `all` | vat | wht | exempt
- `status` (optional): `all` | draft | active | inactive
- `sort` (optional): `code` | `name_th` | `rate` | `category` | `used` | `status` (default `code`)
- `dir` (optional): `asc` | `desc` (default `asc`) — **`rate` & `used` sort เชิงตัวเลข**
- `page` (optional, default 1) · `page_size` (optional, default 8)
- **Headers:** `X-Tenant-Id` (required)

**Response 200:**
```json
{
  "data": [
    { "id":"T-001","code":"VAT7","name_th":"ภาษีมูลค่าเพิ่ม 7%","name_en":"VAT 7%",
      "category":"vat","rate":7,"status":"active","used_count":214,
      "created_by":"ระบบ","created_at":"2025-01-04T00:00:00Z",
      "updated_by":"พิมพ์ใจ บัญชี","updated_at":"2026-01-10T00:00:00Z" }
  ],
  "stats": { "total":10, "active":8, "inactive":1, "draft":1 },
  "total": 10, "page": 1, "page_size": 8
}
```
**Errors:** 400 ERR_INVALID_QUERY_PARAMS · 401 ERR_NOT_AUTHENTICATED · 403 ERR_INSUFFICIENT_ROLE
**Side effects:** — (read-only)
**Calls (Logic):** F-TAX-FN-05 buildTaxCodeListQuery → 03_LOGIC §3.1

---

### F-TAX-API-02: POST /api/v1/tax-codes

| Field | Value |
|---|---|
| method / path | POST /api/v1/tax-codes |
| summary | สร้างรหัสภาษีใหม่ |
| auth / roles | required · tax_admin |

**Request:**
- **Headers:** `X-Tenant-Id` (required) · `Idempotency-Key` (required — กัน double-submit) `[AI-DEFAULT — PR-7]`
- **Body:**
  ```json
  { "code":"", "name_th":"ภาษีมูลค่าเพิ่ม 7%", "name_en":"VAT 7%",
    "category":"vat", "rate":7, "status":"active" }
  ```
- **Validation (field-level, ≤5 lines):** `name_th` required · `category` ∈ enum · `status` ∈ enum · `rate` present.
  - **Complex validation → 03_LOGIC F-TAX-FN-04** (auto-code, case-insensitive dup, exempt→0, rate range)

**Response 201:** record ที่สร้าง (รวม `id`, `code` ที่ final/auto, `used_count`:0, `version`:1)
**Errors:**
- 400 ERR_VALIDATION_FAILED (NAME_REQUIRED / RATE_INVALID)
- 409 ERR_CODE_DUPLICATE (BR-01 · unique constraint) · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY
- 422 BR_EXEMPT_RATE (ถ้า client ฝืนส่ง exempt+rate≠0 — server บังคับ 0)
**Preconditions:** code (หรือ auto) ไม่ซ้ำ (case-insensitive)
**Side effects:** INSERT T_tax_code · audit (created_by/at) · `approver_* = null`
**Calls (Logic):** F-TAX-FN-01 createTaxCode, F-TAX-FN-02 generateAutoCode, F-TAX-FN-04 validateTaxCodeInput

---

### F-TAX-API-03: GET /api/v1/tax-codes/:id

| Field | Value |
|---|---|
| method / path | GET /api/v1/tax-codes/:id |
| summary | รายละเอียด (overview + usage + history tabs) |
| auth | required |

**Response 200:** full record + audit fields (created/updated by+at) + `used_count`.
**Errors:** 404 ERR_NOT_FOUND
**Side effects:** — (read-only)
**Calls (Logic):** F-TAX-FN-11 getTaxCodeUsage (คืน used_count — mock; OQ-TAX-04)

---

### F-TAX-API-04: PUT /api/v1/tax-codes/:id

| Field | Value |
|---|---|
| method / path | PUT /api/v1/tax-codes/:id |
| summary | แก้ไขรหัสภาษี — **IR-TAX-01 server guard** |
| auth / roles | required · tax_admin |

**Request:**
- **Headers:** `X-Tenant-Id` · `If-Match: <version>` (optimistic lock) `[AI-DEFAULT — PR-2]`
- **Body:** เหมือน create (code/name_th/name_en/category/rate/status)

**IR-TAX-01 guard (server, F-TAX-FN-03):**
- ถ้า `used_count > 0` → **คงค่า `code`/`rate`/`category` เดิมเสมอ** (ignore ค่าใน payload แม้ client ฝืนส่ง — EC-07) · persist เฉพาะ `name_th`/`name_en`/`status`.
- ถ้า `used_count = 0` → แก้ได้ทุก field (validate เหมือน create).

**Response 200:** record หลังแก้ (+ `version` เพิ่ม)
**Errors:** 404 ERR_NOT_FOUND · 409 ERR_STALE_DATA (version mismatch) · 409 ERR_CODE_DUPLICATE · 400 ERR_VALIDATION_FAILED · 422 BR_EXEMPT_RATE
**Side effects:** UPDATE T_tax_code · audit (updated_by/at, version++)
**Calls (Logic):** F-TAX-FN-03 updateTaxCode, F-TAX-FN-04 validateTaxCodeInput (เมื่อ used=0)

---

### F-TAX-API-05: PATCH /api/v1/tax-codes/:id/status

| Field | Value |
|---|---|
| method / path | PATCH /api/v1/tax-codes/:id/status |
| summary | เปลี่ยนสถานะเดี่ยว (อิสระทุกทิศ, ไม่มี gate) |
| auth / roles | required · tax_admin |

**Body:** `{ "status": "active" }` (draft/active/inactive)
**Response 200:** record ที่อัพเดต
**Errors:** 404 ERR_NOT_FOUND · 400 ERR_INVALID_STATUS
**Rule:** LOCK-STATUS-FREE — ทุก transition allowed (ดู 05_RULES §5.2). ไม่มี approval.
**Side effects:** UPDATE status + audit
**Calls (Logic):** F-TAX-FN-06 changeTaxCodeStatus

---

### F-TAX-API-06: POST /api/v1/tax-codes/bulk-status

**Body:** `{ "ids":["T-004","T-010"], "status":"active" }`
**Response 200:** `{ "changed": 2 }` (ตัวที่ status ตรงอยู่แล้ว ถูกข้ามการนับ)
**Errors:** 400 ERR_INVALID_STATUS
**Side effects:** UPDATE หลายแถว + audit ต่อแถว
**Calls (Logic):** F-TAX-FN-06 changeTaxCodeStatus (loop)

---

### F-TAX-API-07: POST /api/v1/tax-codes/bulk-delete

| Field | Value |
|---|---|
| method / path | POST /api/v1/tax-codes/bulk-delete |
| summary | ลบ bulk — **`used_count>0` ถูกข้าม** (BR-05) |
| auth / roles | required · tax_admin |

**Body:** `{ "ids":["T-009","T-001"] }`
**Response 200:** `{ "deleted": 1, "skipped": 1, "skipped_ids":["T-001"] }`
**Rule:** ไม่มีลบเดี่ยว (LOCK-BULK-DEL) — endpoint นี้เท่านั้น. ทุกตัว `used_count>0` → skip (ไม่ error, รายงานยอด).
**Side effects:** DELETE เฉพาะ used_count=0 + audit
**Calls (Logic):** F-TAX-FN-07 bulkDeleteTaxCodes
> ⚠️ **OQ-TAX-04:** guard นี้พึ่ง `used_count` จริง — ตราบใดที่ยัง mock, ห้าม enable production hard-delete (EC-A7 ข้อมูลสูญหาย).

---

### F-TAX-API-08: POST /api/v1/tax-codes/import

| Field | Value |
|---|---|
| method / path | POST /api/v1/tax-codes/import |
| summary | นำเข้า CSV — validate รายแถว, แถวผิดข้าม ไม่ล้มไฟล์ |
| auth / roles | required · tax_admin |

**Request:** `multipart/form-data` (file) + `Idempotency-Key`
**Flow (2 โหมด):**
- `?mode=preview` → validate ทุกแถว, คืนผลตรวจ (ไม่ INSERT)
- `?mode=commit` → INSERT เฉพาะแถวผ่าน
**CSV columns:** `code, name_th, name_en, type(ชื่อไทย), rate, status(ว่าง=ร่าง)`
**Response 200 (preview):**
```json
{ "total":5, "ok":2, "error":3,
  "rows":[ {"code":"WHT075","status":"active","result":"ok"},
           {"code":"WHT99","result":"error","code_reason":"RATE_INVALID","message":"อัตราไม่ถูกต้อง 0–100 (RATE_INVALID)"} ] }
```
**Response 200 (commit):** `{ "imported":2, "skipped":3 }`
**Row validation → 6 error codes** (05_RULES §5.6): REQUIRED / BAD_TYPE / RATE_INVALID / EXEMPT_RATE / BAD_STATUS / CODE_DUPLICATE
**Side effects (commit):** INSERT หลายแถว (status ว่าง→draft, BR-08) + audit
**Calls (Logic):** F-TAX-FN-08 importTaxCodes, F-TAX-FN-09 validateImportRow
> ⚠️ **OQ-TAX-IMPORT-PARSE:** parser จริงต้อง validate header/encoding/คอลัมน์สลับ ก่อน validate รายแถว (mock ข้ามขั้นนี้ — EC-A1).

---

### F-TAX-API-09: GET /api/v1/tax-codes/export

**Request — Query:** เหมือน API-01 (export ตาม filter ปัจจุบัน)
**Response 200:** `text/csv; charset=utf-8` + **BOM `﻿`** (เปิด Excel ไม่เพี้ยน)
**Columns (7, verbatim):** `code, name_th, name_en, type, rate, status, used_in` — `type`/`status` = ชื่อไทย (catLabel/statusLabel); filename `taxcode_export_YYYY-MM-DD.csv`
**Side effects:** — (read-only)
**Calls (Logic):** F-TAX-FN-10 exportTaxCodesCsv

---

### F-TAX-API-10: GET /api/v1/tax-codes/lookup

| Field | Value |
|---|---|
| method / path | GET /api/v1/tax-codes/lookup |
| summary | Downstream combobox — **เฉพาะ status=active** (BR-07) |
| auth | required (ทุก consumer role) |

**Query:** `q` (optional search) · `category` (optional)
**Response 200:** `[ {"code":"VAT7","name_th":"...","rate":7,"category":"vat"} ]` — **เฉพาะ active** (draft/inactive ซ่อน)
**Side effects:** — (read-only)
**Calls (Logic):** F-TAX-FN-05 buildTaxCodeListQuery (force status=active)

---

## §2.3 Common Concerns

### Idempotency (PR-7) `[AI-DEFAULT]`
Mutation POST (create/import) รับ `Idempotency-Key` — cache result 24 ชม; same key+body → cached; same key+different body → 409.

### Optimistic Locking (PR-2) `[AI-DEFAULT]`
PUT (API-04) ต้องมี `If-Match: <version>` — mismatch → 409 ERR_STALE_DATA.

### Multi-Tenant
ทุก endpoint ต้องมี `X-Tenant-Id`; DB filtered ผ่าน PostgreSQL RLS.

### Audit Log
ทุก mutation เขียน audit (actor + action + resource `tax_code:<id>` + timestamp + diff). BR-10.

### Uniqueness (concurrent) `[AI-DEFAULT — EC-A3]`
Create/import พึ่ง **DB unique index `(tenant_id, lower(code))`** — race → 409 ERR_CODE_DUPLICATE (ไม่ใช่แค่ app check).

---

## §2.4 API → Logic Trace (Anchor for R8)

> Authoritative: `03_LOGIC.md §3.3`

| API | Calls Functions | Calls Engines |
|---|---|---|
| F-TAX-API-01 GET /tax-codes | F-TAX-FN-05 | — |
| F-TAX-API-02 POST /tax-codes | F-TAX-FN-01, F-TAX-FN-02, F-TAX-FN-04 | — |
| F-TAX-API-03 GET /tax-codes/:id | F-TAX-FN-11 | — |
| F-TAX-API-04 PUT /tax-codes/:id | F-TAX-FN-03, F-TAX-FN-04 | — |
| F-TAX-API-05 PATCH /:id/status | F-TAX-FN-06 | — |
| F-TAX-API-06 POST /bulk-status | F-TAX-FN-06 | — |
| F-TAX-API-07 POST /bulk-delete | F-TAX-FN-07 | — |
| F-TAX-API-08 POST /import | F-TAX-FN-08, F-TAX-FN-09 | — |
| F-TAX-API-09 GET /export | F-TAX-FN-10 | — |
| F-TAX-API-10 GET /lookup | F-TAX-FN-05 | — |

> **R8 Check:** ทุก mutation row (API-02/04/05/06/07/08) มี ≥1 Function ✅ · ไม่มี Engine ใน feature นี้.

---

## §2.X Cross-Module Contract ⭐ (จาก BRD §12.1 Downstream Impact Map)

> ทุก downstream = **soft reference (pull model)** — ปลายทาง query lookup, เก็บแค่ `code`. Tax Code **ไม่ push event** (LOCK-NO-NOTIF).

| Downstream | รูปแบบ | Contract | Trigger | Payload หลัก |
|---|---|---|---|---|
| Item Master (กลุ่มภาษี) | Endpoint (ปลายทางเรียก) | F-TAX-API-10 GET /tax-codes/lookup | เปิด combobox กลุ่มภาษี | `[{code,name_th,rate,category}]` (active only) |
| เอกสารขาย/ซื้อ (QT/SO/INV/PR/PO) | Endpoint (ปลายทางเรียก) | F-TAX-API-10 lookup → เก็บ `code`+snapshot `rate` ในบรรทัด | เลือกภาษีในบรรทัด | rate ณ ตอนเลือก (IR-TAX-01 คุ้มครองไม่ให้ rate เดิมเปลี่ยน) |
| GL Posting Setup | Endpoint | F-TAX-API-01/10 (อ่าน code) | ตั้งค่า mapping | `code` (ทะเบียนนี้ไม่ถือเลขบัญชี — LOCK-NO-GL) |
| DOA / NOTIF | — | — | — | ไม่มี (LOCK-DOA-NULL / LOCK-NO-NOTIF) |

**"แก้/ยกเลิกกลางทาง" (compensating):**
- เปลี่ยนรหัสเป็น `inactive` → lookup หยุดคืน (เลือกใหม่ไม่ได้) แต่ **สินค้า/เอกสารเดิมคงค่า code/rate เดิม** (soft ref — ไม่มี cascade). ตรวจใน 06_TESTS XT-01/XT-02.
- ไม่มี event ต้อง release → ไม่มี compensating event (pull model).
