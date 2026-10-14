# 02_API — F-AGM-001 Farmer Member Management

> **Audience:** Backend developer (HTTP layer)
> **Purpose:** API contracts — CUBIC API Entity format
> **🚨 Iron Rule:** ห้ามมี business logic >5 lines ที่นี่ — ย้ายไป 03_LOGIC §3.1
> **🚨 R8:** ทุก mutation API ระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3
> **⭐ Legacy API name preservation (handover):** FN-AT-AGM-102/103/105, FN-SEQ-AGM-110/111 คงไว้เป็น Legacy Function Name ของแต่ละ endpoint — dev เดิมค้นเจอ, idempotency key ใช้ชื่อชุดนี้

---

## §2.1 API Overview

| ID | Method | Path | Summary | Legacy FN | Auth (ENC role) |
|---|---|---|---|---|---|
| F-AGM-001-API-01 | GET | /api/v1/farmer-members | List + search + filter | — | R-01, R-02 |
| F-AGM-001-API-02 | POST | /api/v1/farmer-members | Create member | **FN-SEQ-AGM-110** | R-01 |
| F-AGM-001-API-03 | GET | /api/v1/farmer-members/:id | Get detail | **FN-AT-AGM-102** | R-01, R-02 |
| F-AGM-001-API-04 | PUT | /api/v1/farmer-members/:id | Update (รวม re-submit LOCK-06) | **FN-SEQ-AGM-111** | R-01 |
| F-AGM-001-API-05 | POST | /api/v1/farmer-members/:id/verify | Verify เดี่ยว (Approve/Reject) | **FN-AT-AGM-103** | R-02 |
| F-AGM-001-API-06 | POST | /api/v1/farmer-members/bulk-verify | Verify กลุ่ม | **FN-AT-AGM-103** (batch) | R-02 |
| F-AGM-001-API-07 | DELETE | /api/v1/farmer-members/:id | Soft delete (เฉพาะ Pending) | **FN-AT-AGM-105** | R-01 |
| F-AGM-001-API-08 | POST | /api/v1/farmer-members/import | CSV import (partial success) | **FN-SEQ-AGM-110** (batch) | R-01 |
| F-AGM-001-API-09 | GET | /api/v1/farmer-members/import/template | Download CSV template | — | R-01 |
| F-AGM-001-API-10 | GET | /api/v1/farmer-members/:id/history | History timeline | — | R-01, R-02 |

> Address lookup (จังหวัด/อำเภอ/ตำบล) ใช้ M-01 master API กลางของ CUBE — ไม่ใช่ endpoint ของ feature นี้

### §2.1.1 Legacy ↔ Authoritative FN Mapping (Refactor-Wave recheck 2026-07-22) ⚠️

> Legacy binding ที่ endpoint ข้างบน (103→Verify, 110→import) **predate การ renumber ตาม authoritative scheme FN-AT/SEQ-AGM 99–114** และ mirror as-built code — **คงไว้เป็น idempotency-key format เดิม** (ห้าม break คีย์ที่รันอยู่) แต่ **dev ต้องอ้าง authoritative 99–114 scheme เมื่อ cross-reference กับ spec ใหม่**. จุด collision สำคัญ: **authoritative 103 = Search** (ไม่ใช่ Verify), **106 = Verify single**, **107 = Bulk Verify**, **110 = Create**, **114 = Upload CSV**.

| Authoritative FN | Purpose (authoritative) | Legacy binding ใน pack นี้ | Match |
|---|---|---|---|
| FN-AT-AGM-99 | Generate Member ID (atomic) | ใน FN-01 ผ่าน Document Numbering กลาง | behavior ✅ (ไม่อ้างชื่อ) |
| FN-AT-AGM-100 | Validate Address (cascade + postal) | FN-03 + ENG-EXT-02 | behavior ✅ |
| FN-AT-AGM-101 | Insert Member | FN-01 | behavior ✅ |
| FN-AT-AGM-102 | Load Member (read) | API-03 GET detail | ✅ ตรง |
| FN-AT-AGM-103 | **Search Members** | ❌ ผูกกับ API-05/06 Verify (legacy) | ⚠️ mis-bound — authoritative 103 = Search (=API-01) |
| FN-AT-AGM-104 | Update Member (atomic) | FN-02 | behavior ✅ |
| FN-AT-AGM-105 | Soft Delete | API-07 DELETE | ✅ ตรง |
| FN-AT-AGM-106 | **Set Verify Status (single)** | (existing ใช้ 103 แทน) | ⚠️ authoritative single-verify = 106 |
| FN-AT-AGM-107 | **Bulk Set Verify** | (existing ใช้ 103 batch แทน) | ⚠️ authoritative bulk-verify = 107 |
| FN-AT-AGM-108 | Validate CSV Row | FN-08 → FN-03 ต่อแถว | behavior ✅ |
| FN-AT-AGM-109 | Create Member from CSV Row | FN-08 → FN-01 ต่อแถว | behavior ✅ |
| FN-SEQ-AGM-110 | **Create (SEQ)** | API-02 ✅ + API-08 import ❌ | ⚠️ import ควรเป็น 114 |
| FN-SEQ-AGM-111 | Edit (SEQ) | API-04 PUT | ✅ ตรง |
| FN-SEQ-AGM-112 | Verify single (SEQ) | (flow API-05) | behavior ✅ (ไม่อ้างชื่อ) |
| FN-SEQ-AGM-113 | Bulk Verify (SEQ) | (flow API-06) | behavior ✅ (ไม่อ้างชื่อ) |
| FN-SEQ-AGM-114 | **Upload CSV (SEQ)** | ❌ existing ใช้ 110 batch | ⚠️ authoritative CSV upload = 114 |

> ทุก capability ครบ (ไม่มีฟังก์ชันหาย) — drift อยู่ที่ **legacy-name binding** เท่านั้น. อ้างอิง authoritative FN-AT-AGM-108/109 + FN-SEQ-AGM-114 สำหรับ CSV idempotency (ดู API-08 + §2.3).

---

## §2.2 Per-API Contract

### F-AGM-001-API-01: GET /api/v1/farmer-members

| Field | Value |
|---|---|
| **summary** | รายการสมาชิก + ค้นหา + กรองสถานะ (ไม่รวม is_deleted) |
| **auth** | required — R-01, R-02 |

**Request — Query params:**
- `q` (optional): คำค้น — match ชื่อ / นามสกุล / เบอร์โทร / เลขบัตร / member_id
- `verify_status` (optional): `pending_approval | approved | rejected` (ไม่ส่ง = ทั้งหมด)
- `limit` (default 20, max 100) / `offset` (default 0)
- **Headers:** `X-Tenant-Id` (required)

**Response 200:**
```json
{
  "data": [
    {
      "id": "uuid",
      "member_id": "FM-000001",
      "first_name": "สมชาย",
      "last_name": "ใจดี",
      "phone": "0812345678",
      "citizen_id_masked": "1-XXXX-XXXX-XX-1",
      "verify_status": "pending_approval",
      "selectable": true,
      "updated_at": "iso8601"
    }
  ],
  "total": 150, "limit": 20, "offset": 0
}
```
> ⭐ list ส่ง `citizen_id_masked` เท่านั้น (S02-04) — full value เฉพาะ API-03 ตาม permission
> `selectable` = true เฉพาะ pending_approval (ใช้คุม checkbox bulk)

> **Search normalization (GAP-10, authoritative TC-271):** ก่อน match — trim ช่องว่างหัว/ท้าย + ยุบช่องว่างซ้ำใน `q` · phone normalize ทั้งค่า stored และคำค้น (strip non-digit, `+66`→`0`) เพื่อให้ค้นเจอไม่ว่าจะเก็บ/พิมพ์รูปแบบใด — ดู 03_LOGIC FN-04
**Errors:** 400 ERR_INVALID_QUERY_PARAMS · 401 · 403
**Calls (Logic):** F-AGM-001-FN-04 buildMemberListQuery

---

### F-AGM-001-API-02: POST /api/v1/farmer-members  ⭐ Legacy: FN-SEQ-AGM-110

| Field | Value |
|---|---|
| **summary** | สร้างสมาชิกใหม่ → gen member_id + สถานะ pending_approval |
| **auth** | required — R-01 |

**Request — Headers:** `X-Tenant-Id` · `Idempotency-Key` = `FN-SEQ-AGM-110:{client_ref}:{user_id}` (LOCK-03)
**Body:**
```json
{
  "first_name": "string", "last_name": "string",
  "citizen_id": "string(13)", "phone": "string(9-12)",
  "email": "string",
  "address_line": "string",
  "province_code": "string", "district_code": "string", "subdistrict_code": "string",
  "postal_code": "string|null"
}
```
**Validation (field-level ≤5 lines):** required ตาม 05_RULES VR-04 · **email required** (authoritative — LOCK-08 superseded 2026-07-22; blank → "กรุณากรอกอีเมล")
**Complex validation → FN-03 validateFarmerMemberData** (13 หลัก, unique, postal match)

**Response 201:**
```json
{ "id": "uuid", "member_id": "FM-000001", "verify_status": "pending_approval", "created_at": "iso8601", "updated_at": "iso8601" }
```
**Errors:** 400 ERR_VALIDATION_FAILED · 403 · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 BR_CITIZEN_ID_DUPLICATE · 422 BR_POSTAL_CODE_MISMATCH
**Side effects:** INSERT T_farmer_member · INSERT T_farmer_member_history (event=create) — fail = block transaction (S01-07)
**Calls (Logic):** FN-01 createFarmerMember · FN-03 validateFarmerMemberData · FN-09 recordMemberHistory

---

### F-AGM-001-API-03: GET /api/v1/farmer-members/:id  ⭐ Legacy: FN-AT-AGM-102

| Field | Value |
|---|---|
| **summary** | รายละเอียดสมาชิกเต็ม (ใช้เปิด P-02 + โหลดค่าเดิมเข้า OV-02) |
| **auth** | required — R-01, R-02 |

**Response 200:** ทุก field ตาม 04_DB §4.2 + `quota_status` (read-only จาก Quota) + `verified_by/at/note`
- `citizen_id` เต็ม เฉพาะ role ที่ผ่าน Restricted ACL — ไม่ผ่าน → masked + audit log การเข้าถึง
**Errors:** 401 · 403 · 404 ERR_NOT_FOUND (รวม soft-deleted)
**Calls (Logic):** — (single read; masking ที่ serializer ตาม D-CLASS)

---

### F-AGM-001-API-04: PUT /api/v1/farmer-members/:id  ⭐ Legacy: FN-SEQ-AGM-111

| Field | Value |
|---|---|
| **summary** | แก้ไขสมาชิก — Approved คงสถานะ (LOCK-07) · Rejected กลับ pending อัตโนมัติ (LOCK-06) |
| **auth** | required — R-01 |

**Request — Headers:** `X-Tenant-Id` · `Idempotency-Key` = `FN-SEQ-AGM-111:{id}:{user_id}`
**Body:** fields เดียวกับ API-02 + `expected_updated_at` (LOCK-03 optimistic lock)

**Response 200:**
```json
{ "id": "uuid", "member_id": "FM-000001", "verify_status": "pending_approval|approved", "resubmitted": true, "updated_at": "iso8601" }
```
> `resubmitted` = true เมื่อสถานะเดิม rejected → กลับ pending_approval (UI ใช้เลือกข้อความ toast)

**Errors:** 400 · 403 · 404 · 409 ERR_STALE_DATA (optimistic lock) · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 BR_CITIZEN_ID_DUPLICATE · 422 BR_POSTAL_CODE_MISMATCH
**Side effects:** UPDATE T_farmer_member (transaction เดียวกับ state change) · INSERT history (event=edit หรือ resubmit — verified_note เดิมเก็บใน history entry) · anomaly flag ถ้าแก้ citizen_id หลัง approved (BRD §18.5)
**Calls (Logic):** FN-02 updateFarmerMember · FN-03 validateFarmerMemberData · FN-09 recordMemberHistory

---

### F-AGM-001-API-05: POST /api/v1/farmer-members/:id/verify  ⭐ Legacy: FN-AT-AGM-103

| Field | Value |
|---|---|
| **summary** | Verify เดี่ยว — Approve / Reject (+เหตุผลบังคับ) |
| **auth** | required — R-02 |

**Request — Headers:** `X-Tenant-Id` · `Idempotency-Key` = `FN-AT-AGM-103:{id}:{user_id}` (คง format legacy)
**Body:**
```json
{ "verify_status": "approved|rejected", "verified_note": "string|null", "expected_updated_at": "iso8601" }
```
**Validation:** `verify_status` required · `verified_note` required เมื่อ rejected (VR-07)

**Response 200:** `{ "id", "member_id", "verify_status", "verified_by", "verified_at", "updated_at" }`
**Errors:** 400 ERR_VALIDATION_FAILED · 403 ERR_INSUFFICIENT_ROLE · 403 ERR_SOD_SELF_VERIFY (หลัง flag OQ-02) · 404 · 409 ERR_STALE_DATA · 422 BR_VERIFY_NOT_PENDING
**Side effects:** UPDATE verify fields · INSERT history (event=approve/reject)
**Calls (Logic):** FN-05 verifyFarmerMember · FN-09

---

### F-AGM-001-API-06: POST /api/v1/farmer-members/bulk-verify  ⭐ Legacy: FN-AT-AGM-103 (batch)

| Field | Value |
|---|---|
| **summary** | Verify กลุ่ม — ประมวลผลรายคน (per-record) รายงานสำเร็จ/ล้มเหลว |
| **auth** | required — R-02 |

**Request — Headers:** `X-Tenant-Id` · `Idempotency-Key` = `FN-AT-AGM-103:bulk:{user_id}:{client_ref}`
**Body:**
```json
{
  "verify_status": "approved|rejected", "verified_note": "string|null",
  "items": [ { "id": "uuid", "expected_updated_at": "iso8601" } ]
}
```
**Response 200 (partial result — ไม่ fail ทั้งชุด):**
```json
{
  "total": 10, "succeeded": 8, "failed": 2,
  "failures": [ { "id": "uuid", "member_id": "FM-000004", "error": "ERR_STALE_DATA", "message": "ถูกตรวจสอบไปแล้วโดยผู้อื่น" } ]
}
```
> EC-12: รายการที่ถูกคนอื่น verify ก่อน → ข้าม นับเป็น failed + เหตุผลใน summary — server แนะนำ batch ≤ 200 รายการ/ครั้ง (BRD §17.5)

**Errors (ทั้ง request):** 400 · 403 · 422 ERR_EMPTY_SELECTION
**Calls (Logic):** FN-06 bulkVerifyFarmerMembers → FN-05 ต่อรายการ · FN-09

---

### F-AGM-001-API-07: DELETE /api/v1/farmer-members/:id  ⭐ Legacy: FN-AT-AGM-105

| Field | Value |
|---|---|
| **summary** | Soft delete — เฉพาะ pending_approval (BR-AGM-05) |
| **auth** | required — R-01 |

**Request — Headers:** `X-Tenant-Id` · `Idempotency-Key` = `FN-AT-AGM-105:{id}:{user_id}` · Body: `{ "expected_updated_at": "iso8601" }`
**Response 200:** `{ "id", "member_id", "is_deleted": true, "deleted_at": "iso8601" }`
**Errors:** 403 · 404 · 409 ERR_STALE_DATA · 422 BR_DELETE_NOT_PENDING ("ลบได้เฉพาะรายการที่ยังไม่ได้ตรวจสอบ")
**Side effects:** UPDATE is_deleted/deleted_at/deleted_by · INSERT history (event=delete) — ไม่มี hard delete (S06-03)
**Calls (Logic):** FN-07 softDeleteFarmerMember · FN-09

---

### F-AGM-001-API-08: POST /api/v1/farmer-members/import  ⭐ Legacy: FN-SEQ-AGM-110 (batch)

| Field | Value |
|---|---|
| **summary** | CSV import — validate header ทั้งไฟล์ก่อน → process รายแถว → partial success (LOCK-04) |
| **auth** | required — R-01 |

**Request:** multipart/form-data `file` (.csv, ≤5MB — limit อ่านจาก Import Config, ห้าม hardcode) + `batch_id` (client-gen UUID ต่อการอัปโหลด 1 ครั้ง) · Headers: `X-Tenant-Id` · `Idempotency-Key` = `FN-SEQ-AGM-110:import:{user_id}:{file_hash}` (คง format legacy)
**CSV Contract (10 คอลัมน์ — LOCK-04, ห้ามเปลี่ยน · header คอลัมน์ที่ 6 = `address` ตาม authoritative, map ภายในเป็น DB column `address_line`):**
```
first_name,last_name,citizen_id,phone,email,address,province,district,subdistrict,postal_code
```

**Batch idempotency (GAP-05, authoritative FN-AT-AGM-108/109 + FN-SEQ-AGM-114):**
- คีย์ batch = `batch_id + file_hash` — rerun เดิม (batch_id เดิม + file_hash เดิม) → **return รายงานผลเดิม** (ไม่สร้างซ้ำ)
- `batch_id` เดิม + `file_hash` **ต่าง** → **409 ERR_BATCH_CONFLICT** ("batch_id นี้ถูกใช้กับไฟล์อื่นแล้ว")
- คีย์ต่อแถว = `{fn}:{batch_id}:{row_index}:{citizen_id}` (fn = FN-AT-AGM-109 create-from-row) — กัน retry บางส่วนสร้างซ้ำ เมื่อ resume batch ที่ค้าง
**Response 200 (partial success):**
```json
{
  "total_rows": 150, "created_count": 145, "failed_count": 5,
  "errors": [ { "row": 12, "field": "citizen_id", "message": "เลขบัตรประชาชนไม่ถูกต้อง", "data": { "first_name": "…" } } ],
  "error_report_url": "/api/v1/farmer-members/import/errors/:batch_id"
}
```
**Errors (ทั้งไฟล์ — reject ก่อน process):** 400 ERR_CSV_INVALID_FILE (.csv/5MB) · 422 BR_CSV_HEADER_MISMATCH (EC-10 — บอกคอลัมน์ที่ผิด · header คาดหวัง `address`) · 422 ERR_CSV_ENCODING (EC-09 — แนะนำ save UTF-8) · 409 ERR_BATCH_CONFLICT (GAP-05 — batch_id เดิม + file_hash ต่าง)
**Side effects:** INSERT รายแถวดี + history ต่อแถว · batch log (MET-02 อ้าง FN-SEQ-AGM-110 batch)
**Calls (Logic):** FN-08 importFarmerMembersCsv → central Import Framework (ENG-EXT-01) + FN-03 ต่อแถว

---

### F-AGM-001-API-09: GET /api/v1/farmer-members/import/template

**summary:** Download แม่แบบ CSV (header 10 คอลัมน์ + 2 แถวตัวอย่าง, UTF-8 BOM) — content จาก Import Config
**Response 200:** `text/csv` filename `member-template.csv` · **Calls:** — (config read)

---

### F-AGM-001-API-10: GET /api/v1/farmer-members/:id/history

**summary:** Timeline จาก T_farmer_member_history (ใหม่→เก่า) — create/edit/approve/reject/resubmit/delete + before/after + actor
**Response 200:** `{ "data": [ { "event", "actor", "at", "note", "diff": {"before":{},"after":{}} } ] }`
- `diff` แสดงตาม classification — Restricted field ใน diff → masked ตาม role
**Errors:** 401 · 403 · 404 · **Calls:** — (read T_farmer_member_history)

---

## §2.3 Common Concerns

### Idempotency (LOCK-03)
ทุก mutation (API-02/04/05/06/07/08) ต้องส่ง `Idempotency-Key` format `{Legacy FN}:{id|ref}:{user_id}`:
- Server cache 24 ชม. — key เดิม + body เดิม → return cached response (กัน double-click EC-16)
- key เดิม + body ต่าง → 409 ERR_DUPLICATE_IDEMPOTENCY_KEY

**CSV batch idempotency (API-08 — GAP-05, authoritative FN-SEQ-AGM-114):** เพิ่มระดับ batch เหนือ mutation-key ปกติ:
- batch key = `batch_id + file_hash` — rerun เดิม → return รายงานผลเดิม (ไม่สร้างซ้ำ)
- `batch_id` เดิม + `file_hash` ต่าง → 409 **ERR_BATCH_CONFLICT**
- per-row key = `{fn}:{batch_id}:{row_index}:{citizen_id}` (fn = FN-AT-AGM-109) — resume batch ที่ค้างไม่สร้างแถวซ้ำ

### Optimistic Locking (LOCK-03)
API-04/05/06/07 ต้องส่ง `expected_updated_at`:
- ตรง → proceed · ไม่ตรง → 409 ERR_STALE_DATA → UI: "ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรชและลองใหม่อีกครั้ง"

### Multi-Tenant
`X-Tenant-Id` ทุก endpoint → PostgreSQL RLS (1 tenant = 1 โรงงาน) · citizen_id unique ต่อ tenant

### Audit / Immutable Log (S01-07)
ทุก mutation เขียน T_farmer_member_history ใน transaction เดียวกัน — เขียน history fail = rollback ทั้ง transaction

---

## §2.4 API → Logic Trace (summary — authoritative ที่ 03_LOGIC §3.3)

| API | Calls Functions | Calls Engines |
|---|---|---|
| API-01 GET list | FN-04 | — |
| API-02 POST create | FN-01, FN-03, FN-09 | ENG-EXT-02 (M-01 resolve) |
| API-03 GET detail | — (serializer masking) | — |
| API-04 PUT update | FN-02, FN-03, FN-09 | ENG-EXT-02 |
| API-05 POST verify | FN-05, FN-09 | — |
| API-06 POST bulk-verify | FN-06 → FN-05, FN-09 | — |
| API-07 DELETE | FN-07, FN-09 | — |
| API-08 POST import | FN-08 → FN-03, FN-01, FN-09 | ENG-EXT-01, ENG-EXT-02 |
| API-09 GET template | — (config read) | ENG-EXT-01 |
| API-10 GET history | — (read) | — |

---

## §2.X Cross-Module Contract ⭐ (จาก BRD §12.1 Downstream Impact Map)

| Downstream | รูปแบบ | Contract | Trigger | Payload หลัก / เงื่อนไข |
|---|---|---|---|---|
| **Quota** | Endpoint (Quota เรียกเข้า) | `GET /api/v1/farmer-members/:id` + query `verify_status=approved` ใน list | ตอนผูก quota | Quota ผูกได้เฉพาะ `verify_status=approved` — invariant ระดับ module (CONTRACT.md ของ AGM batch) |
| **Quota** | Field (feature นี้อ่านกลับ) | `quota_status` ใน API-03 response | เปิด detail | read-only — feature นี้ห้ามเขียน (BR-AGM-13) |
| **สัญญา/ส่งเสริม** | Lookup สด | GET API-03 (contact + address) | อ้าง member_id | ไม่ snapshot — ใช้ค่าล่าสุดเสมอ |
| **การเงินชาวไร่** | Event | `farmer_member_citizen_id_changed_event` | แก้ citizen_id หลัง approved (LOCK-07) | { member_id, changed_by, changed_at } → Anomaly Report (BRD §18.5) ให้การเงินตรวจ |
| **รายงานทะเบียน** | Query convention | list/report ไม่รวม `is_deleted=true` | รายงานประจำงวด | soft-deleted ไม่นับ active |

- **ยกเลิก/แก้กลางทาง:** สมาชิกมี quota แล้วลบไม่ได้โดยโครงสร้าง (ลบได้เฉพาะ pending ซึ่งยังไม่มี quota — BR-AGM-05 บังคับให้เอง) → test XT-01
- ทุกแถว trace กับ 06_TESTS §6.9 (XT-01..XT-04)
