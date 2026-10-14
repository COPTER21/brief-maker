# 02_API — F-AGM-002 Quota Management

> **Audience:** BE dev (HTTP) · **Iron Rule:** business logic >5 lines → 03_LOGIC · **R8:** ทุก mutation ระบุ Calls(Logic)
> **⭐ Legacy API name preservation:** FN-*-AGQ-* คงไว้ต่อ endpoint (dev เดิมค้นเจอ + idempotency key)

---

## §2.1 API Overview

| ID | Method | Path | Summary | Legacy FN | Auth (ENC) |
|---|---|---|---|---|---|
| API-01 | GET | /api/v1/quotas | List + search + filter | FN-AT-AGQ-160 | R-01, R-02 |
| API-02 | POST | /api/v1/quotas/from-member | Create From-Member | **FN-SEQ-AGQ-166** | R-01 |
| API-03 | POST | /api/v1/quotas/no-member | Create No-Member | **FN-SEQ-AGQ-167** | R-01 |
| API-04 | GET | /api/v1/quotas/:id | Get detail | FN-AT-AGQ-159 / 181 | R-01, R-02 |
| API-05 | PUT | /api/v1/quotas/:id | Update (optimistic lock) | **FN-AT-AGQ-183** | R-01 |
| API-06 | GET | /api/v1/quotas/check-number | quota_number unique (exclude_id) | FN-AT-AGQ-176 | R-01 |
| API-07 | POST | /api/v1/quotas/:id/verify | Verify เดี่ยว | **FN-SEQ-AGQ-168** | R-02 |
| API-08 | POST | /api/v1/quotas/bulk-verify | Verify กลุ่ม | **FN-SEQ-AGQ-169** | R-02 |
| API-09 | POST | /api/v1/quotas/import | CSV import (No-Member) | **FN-SEQ-AGQ-170** | R-01 |
| API-10 | GET | /api/v1/quotas/import/template | CSV template | — | R-01 |
| API-11 | DELETE | /api/v1/quotas/:id | Soft delete (unverified) | **FN-SEQ-AGQ-171** | R-01 |
| API-12 | GET | /api/v1/quotas/:id/history | History timeline | — | R-01, R-02 |
| API-13 | GET | /api/v1/quotas/member-search | ค้นหาสมาชิก Approved + ตรวจ 1:0..1 | FN-AT-AGQ-156 + 154 | R-01 |

> Address lookup (M-01) = master API กลาง (ไม่ใช่ endpoint feature นี้)

---

## §2.2 Per-API Contract (key ones)

### API-01: GET /quotas
**Query:** `q` (เลขโควตา/ชื่อ/นามสกุล/เบอร์/เลขบัตร/อีเมล) · `verify_status` · `limit/offset` · Headers `X-Tenant-Id`
**Response 200:** `data[]` = `{ id, quota_number, first_name, last_name, phone, citizen_id_masked, email, verify_status, linked_member_id, selectable, updated_at }` + total
> ⭐ list ส่ง `citizen_id_masked` (S02-04) · `selectable = (verify_status=='unverified')`
**Calls:** FN-05 buildQuotaListQuery

### API-02: POST /quotas/from-member ⭐ FN-SEQ-AGQ-166
**Headers:** `X-Tenant-Id` · `Idempotency-Key` = `FN-SEQ-AGQ-166:{client_ref}:{user}`
**Body:** `{ linked_member_id, quota_number, ...personal, current_address{}, id_card_address{}, bank_info{}, documents[] }`
**Validation:** quota_number unique (FN-04) · member Approved + 1:0..1 (FN-11) · complex → FN-01
**Response 201:** `{ id, quota_number, verify_status:"unverified", linked_member_id, member_update_status:"success"|"scheduled_retry", created_at }`
**Errors:** 400 · 403 · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 BR_QUOTA_NUMBER_DUPLICATE · 422 BR_MEMBER_HAS_QUOTA · 422 BR_MEMBER_NOT_APPROVED
**Side effects:** INSERT T_quota + INSERT history (transaction เดียว, commit ก่อน) · **แล้วเขียน farmer_member.quota_status = has_quota เป็น step แยก idempotent (FN-12) — fail → keep quota + `member_update_status=scheduled_retry` + non-blocking banner (ไม่ rollback quota — §2.3)**
**Calls:** FN-01 createQuotaFromMember · FN-04 · FN-11 checkMemberEligible · FN-12 writeMemberQuotaStatus · FN-10 recordHistory · ENG-EXT-02 (address) · ENG-EXT-03 (farmer connector)

### API-03: POST /quotas/no-member ⭐ FN-SEQ-AGQ-167
**Body:** เหมือน API-02 แต่ `linked_member_id = null`
**Response 201:** `{ id, quota_number, verify_status:"unverified", linked_member_id:null }`
**Side effects:** INSERT T_quota · INSERT history — **ไม่เขียน quota_status** (ไม่มี member)
**Errors:** 400 · 403 · 409 · 422 BR_QUOTA_NUMBER_DUPLICATE
**Calls:** FN-02 createQuotaNoMember · FN-04 · FN-10 · ENG-EXT-02

### API-05: PUT /quotas/:id ⭐ FN-AT-AGQ-183
**Headers:** `Idempotency-Key` = `FN-AT-AGQ-183:{id}:{ts}` · Body: fields + `expected_version` (LOCK-06)
**Response 200:** `{ id, quota_number, version, updated_at }`
**Errors:** 400 · 403 · 404 · 409 ERR_STALE_DATA (version) · 409 dup idem · 422 BR_QUOTA_NUMBER_DUPLICATE
**Side effects:** UPDATE T_quota (version++) · INSERT history (diff) — ไม่เปลี่ยน verify_status (OQ-Q3: ไม่ auto re-submit)
**Calls:** FN-03 updateQuota · FN-04 · FN-10 · ENG-EXT-02

### API-06: GET /quotas/check-number ⭐ FN-AT-AGQ-176
**Query:** `quota_number` · `exclude_id?` · **Response 200:** `{ unique: boolean }` · UI blur → "เลขโควต้านี้ถูกใช้แล้ว" · **Calls:** FN-04

### API-07: POST /quotas/:id/verify ⭐ FN-SEQ-AGQ-168
**Body:** `{ verify_status:"verified"|"rejected", verified_note?:string, expected_version }`
**Validation:** ต้องเลือกผล (VR-11) · note optional แม้ reject (LOCK-09)
**Response 200:** `{ id, verify_status, verified_by, verified_at, version }`
**Errors:** 400 · 403 ERR_INSUFFICIENT_ROLE · 403 ERR_SOD_SELF_VERIFY (flag OQ-Q6) · 404 · 409 ERR_STALE_DATA · 422 BR_VERIFY_NOT_UNVERIFIED
**Side effects:** UPDATE verify fields · **reject + linked → UPDATE farmer_member.quota_status = no_quota (FN-12)** · INSERT history
**Calls:** FN-06 verifyQuota · FN-12 (reject case) · FN-10

### API-08: POST /quotas/bulk-verify ⭐ FN-SEQ-AGQ-169
**Body:** `{ verify_status, verified_note?, items:[{id, expected_version}] }`
**Response 200 (partial):** `{ total, succeeded, failed, failures:[{id, quota_number, error, message}] }` — EC-12 (ถูก verify ก่อน → ข้าม)
**Calls:** FN-07 → FN-06 → FN-12 · FN-10

### API-09: POST /quotas/import ⭐ FN-SEQ-AGQ-170 (No-Member only)
**Request:** multipart `file` (.csv ≤5MB) · `Idempotency-Key`
**CSV Contract (No-Member):** `quota_number,first_name,last_name,citizen_id,phone,address,province,district,subdistrict,birth_date,marital_status,number_of_children`
**Per-row idempotency (FN-AT-AGQ-126/132) ⭐:** แต่ละแถวใช้ key `FN-AT-AGQ-126:{source_file_hash}:{row_index}` — rerun ไฟล์เดิม (source_file_hash เดิม) → **คืนผลเดิม (idempotency hit, ไม่สร้าง duplicate)** + UI "ไฟล์นี้ถูกประมวลผลแล้ว — คืนผลเดิม" · same `batch_id` แต่ไฟล์เนื้อหาต่าง (hash ต่าง) → **409 CONFLICT**
**Response 200 (partial success):** `{ total_rows, created_count, failed_count, errors[], error_report_url, batch_id, source_file_hash }`
**Errors:** 400 ERR_CSV_INVALID_FILE · 409 ERR_CSV_BATCH_CONFLICT (same batch, different file) · 422 BR_CSV_HEADER_MISMATCH · 422 ERR_CSV_ENCODING
**Side effects:** INSERT รายแถวดี (unverified, No-Member) · batch log (MET-02) — ไม่เขียน quota_status
**Calls:** FN-09 importQuotaCsv → FN-04, FN-02 (per-row idempotent) · ENG-EXT-01 · ENG-EXT-02

### API-11: DELETE /quotas/:id ⭐ FN-SEQ-AGQ-171
**Body:** `{ expected_version }` · **Response 200:** `{ id, is_deleted:true, deleted_at }`
**Errors:** 403 · 404 · 409 ERR_STALE_DATA · 422 BR_DELETE_NOT_UNVERIFIED
**Side effects:** UPDATE is_deleted · **linked → UPDATE farmer_member.quota_status = no_quota (FN-12)** · INSERT history — soft only (LOCK-08)
**Calls:** FN-08 softDeleteQuota · FN-12 · FN-10

### API-13: GET /quotas/member-search ⭐ FN-AT-AGQ-156 + 154
**Query:** `q` — matchable keys: `first_name` / `last_name` / `phone` / `citizen_id` / **`email`** (email เป็น search key ตาม FN-AT-AGQ-115) · **Response 200:** `{ members:[{ member_id, first_name, last_name, phone, email, verify_status, has_quota }] }`
- **แสดงเฉพาะ member verify_status=approved** (R08 — CUBE ADD) · `has_quota` = true → UI block "สมาชิกนี้มีโควต้าอยู่แล้ว" (1:0..1)
- **0 match → UI แสดงข้อความมาตรฐานสีแดง "ไม่พบข้อมูลสมาชิกที่ตรงกับคำค้นหา"** (FN-AT-AGQ-115 / TC-287)
**Calls:** FN-11 checkMemberEligible · ENG-EXT-03 (farmer connector — query member API ของ F-AGM-001)

---

## §2.3 Common Concerns
### Idempotency (LOCK-06)
ทุก mutation ส่ง `Idempotency-Key` `{Legacy FN}:{id|ref}:{ts}` — cache 24 ชม.
### Optimistic Locking (LOCK-06)
API-05/07/08/11 ส่ง `expected_version` — ไม่ตรง → 409 ERR_STALE_DATA
### Cross-Module Write Integrity ⭐ (keep-quota + async idempotent retry — FN-AT-AGQ-127)
**หลักการ (authoritative):** quota mutation (create/reject/delete) **commit ก่อน** — การเขียน quota_status กลับเป็น **step แยก idempotent** (ไม่ผูก transaction เดียว) และ **ห้าม rollback quota เมื่อ write-back ล้มเหลว**
- **create-from-member (API-02):** commit quota (unverified) → เรียก FN-12 เขียน `has_quota` (idempotency key `FN-SEQ-AGQ-166:member:{quota_id}`) · member service fail (TIMEOUT/502/503) → retry sync ≤3 ครั้ง → ยังไม่ผ่าน → **persist retry task (async idempotent)** + response `member_update_status = scheduled_retry` + UI non-blocking banner "กำลังอัปเดตสถานะสมาชิก (จะ retry อัตโนมัติ)" — **ไม่ rollback quota**
- **reject/delete linked (API-07/11):** commit การ reject/delete ก่อน → เขียน `no_quota` แบบ idempotent · fail → keep การ mutation ไว้ + schedule retry การ revert (idempotent) · **ไม่ rollback**
- member หายระหว่างทาง (EC-17) → write ข้าม + log anomaly (ไม่ error)
- `member_update_status` enum: `success | scheduled_retry | failed` — ทุกกรณี **ไม่บล็อก/ไม่ย้อน** quota mutation (OQ-F03: retry queue — ห้ามปล่อยเงียบ)
### Audit (S01-07)
ทุก mutation → T_quota_history (transaction เดียว)

---

## §2.4 API → Logic Trace (summary — authoritative ที่ 03_LOGIC §3.3)
| API | Functions | Engines |
|---|---|---|
| API-01 | FN-05 | — |
| API-02 | FN-01, FN-04, FN-11, FN-12, FN-10 | ENG-EXT-02/03 |
| API-03 | FN-02, FN-04, FN-10 | ENG-EXT-02 |
| API-04 | — (serializer) | — |
| API-05 | FN-03, FN-04, FN-10 | ENG-EXT-02 |
| API-06 | FN-04 | — |
| API-07 | FN-06, FN-12, FN-10 | ENG-EXT-03 (reject) |
| API-08 | FN-07(→06,12), FN-10 | ENG-EXT-03 |
| API-09 | FN-09(→04,02), FN-10 | ENG-EXT-01/02 |
| API-10 | — (config) | ENG-EXT-01 |
| API-11 | FN-08, FN-12, FN-10 | ENG-EXT-03 |
| API-12 | — (read) | — |
| API-13 | FN-11 | ENG-EXT-03 |

---

## §2.X Cross-Module Contract ⭐ (BRD §12.1 — กับ Farmer F-AGM-001)

| Downstream/Upstream | รูปแบบ | Contract | Trigger | Payload/เงื่อนไข |
|---|---|---|---|---|
| **Farmer (READ)** | Endpoint (Quota เรียก) | `GET farmer-members/member-search?verify_status=approved` + `GET :id (has_quota check)` | create From-Member / member-search | เฉพาะ Approved (R08) + 1:0..1 (R03) |
| **Farmer (WRITE)** | Endpoint/Event | `PATCH farmer-members/:id/quota-status` `{ quota_status: has_quota\|no_quota, source_quota_id }` | create-link→has_quota · reject/delete→no_quota | step แยก idempotent (keep-quota, ไม่ rollback) + async retry + compensating |
| **Farmer (field)** | — | farmer_member.quota_status = read-only ฝั่ง Farmer (BR-AGM-13) | — | Quota เขียนเท่านั้น |
| สัญญาส่งอ้อย (อนาคต) | — | quota_number + linked_member_id (verified เท่านั้น) | quota verified | — |

- **แก้/ยกเลิกกลางทาง:** reject/delete → compensating write no_quota · member หาย → skip + log (EC-17)
- ทุกแถว trace 06_TESTS §6.9 (XT-01..04)
