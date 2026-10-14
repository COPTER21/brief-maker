# 03_LOGIC — F-AGM-002 Quota Management

> **Audience:** BE dev (business logic) · **R8:** ทุก mutation API trace ไป ≥1 Function/Engine ใน §3.3

---

## §3.1 Functions (Scope-Local)

### F-AGM-002-FN-01: `createQuotaFromMember`
- **Purpose:** สร้างโควตาผูกสมาชิก (commit ก่อน) แล้วเขียน quota_status กลับแบบ idempotent เป็น step แยก (FN-12) — ไม่ rollback quota ถ้า write-back fail
- **Input:** `{ quotaData, linkedMemberId, tenantId, userId }` · **Output:** `Quota | Error[]`
- **Calls:** FN-04 (quota_number unique), FN-11 (member eligible: Approved + 1:0..1), ENG-EXT-02 (address/postal), FN-12 (write has_quota), FN-10
- **Side effects:** INSERT T_quota (unverified) · **UPDATE farmer_member.quota_status=has_quota via FN-12** · history event=create
- **Error:** BR_QUOTA_NUMBER_DUPLICATE, BR_MEMBER_HAS_QUOTA, BR_MEMBER_NOT_APPROVED
- **Invoked by:** API-02 · **Iron rule:** ✅ no HTTP

### F-AGM-002-FN-02: `createQuotaNoMember`
- **Purpose:** สร้างโควตา standalone (ไม่ผูกสมาชิก)
- **Input:** `{ quotaData, tenantId, userId }` · **Output:** `Quota | Error[]`
- **Calls:** FN-04, ENG-EXT-02, FN-10 · **Side effects:** INSERT T_quota (linked_member_id=null, unverified) · history — **ไม่เขียน quota_status**
- **Invoked by:** API-03, FN-09 (CSV row) · **Iron rule:** ✅

### F-AGM-002-FN-03: `updateQuota`
- **Purpose:** แก้ไขโควตา + optimistic lock (version)
- **Input:** `{ id, quotaData, expectedVersion, tenantId, userId }` · **Output:** `{ quota } | ConflictError | Error[]`
- **Logic:** load + check version → STALE ถ้าไม่ตรง · FN-04 validate (unique exclude self) · UPDATE (version++) · **ไม่เปลี่ยน verify_status** (OQ-Q3: ไม่ auto re-submit) · FN-10 (diff)
- **Invoked by:** API-05 · **Iron rule:** ✅

### F-AGM-002-FN-04: `validateQuotaData`
- **Purpose:** Complex validation รวมศูนย์ (create/edit/CSV row)
- **Rules (map 05_RULES §5.4):** citizen 13 (VR-01), phone 9-12 (VR-02), email format optional (VR-03), required set (VR-04), **quota_number unique exclude self (VR-05)**, postal match ตำบล ×2 (VR-10) ผ่าน ENG-EXT-02
- **Invoked by:** FN-01/02/03/09 · **Iron rule:** ✅

### F-AGM-002-FN-05: `buildQuotaListQuery`
- **Purpose:** list query — คำค้น 6 field + filter สถานะ + ตัด is_deleted + mask citizen_id + selectable
- **Output:** `citizen_id_masked` เท่านั้น (S02-04) · `selectable=(unverified)` · **Invoked by:** API-01

### F-AGM-002-FN-06: `verifyQuota`
- **Purpose:** ตรวจสอบยืนยันเดี่ยว + state machine + SoD + write-back
- **Logic:** optimistic lock → STALE · สถานะต้อง unverified (BR-AGQ-04) → BR_VERIFY_NOT_UNVERIFIED · SoD: created_by==userId → ERR_SOD_SELF_VERIFY (flag OQ-Q6) · UPDATE verify fields · **reject + linked → FN-12 write no_quota** · FN-10
- **Invoked by:** API-07, FN-07 · **Iron rule:** ✅

### F-AGM-002-FN-07: `bulkVerifyQuotas`
- **Purpose:** orchestrate verify กลุ่ม — per-record, partial result
- **Logic:** loop FN-06 · error รายการ (STALE/NOT_UNVERIFIED/SoD) → นับ failed + เหตุผล, อื่นไปต่อ (EC-12) · chunk > 200
- **Invoked by:** API-08

### F-AGM-002-FN-08: `softDeleteQuota`
- **Purpose:** soft delete + guard + write-back
- **Logic:** optimistic lock → สถานะต้อง unverified (BR-AGQ-06) → BR_DELETE_NOT_UNVERIFIED · set is_deleted · **linked → FN-12 write no_quota** · FN-10 (event=delete) · ไม่มี hard delete
- **Invoked by:** API-11

### F-AGM-002-FN-09: `importQuotaCsv`
- **Purpose:** orchestrate CSV import No-Member — validate ทั้งไฟล์ → รายแถว → partial success (LOCK-07)
- **Logic:** file-level (ENG-EXT-01): .csv, ≤5MB, UTF-8 (EC-09), header ตรง (EC-10) · compute `source_file_hash` · per-row: FN-04 + ซ้ำภายในไฟล์ quota_number (EC-11) + resolve ตำบล M-01 (EC-13) · แถวผ่าน → FN-02 (No-Member) ด้วย **per-row idempotency key `FN-AT-AGQ-126:{source_file_hash}:{row_index}`** · **rerun ไฟล์เดิม (hash เดิม) → คืนผลเดิม (idempotency hit, ไม่สร้าง duplicate) · same batch_id + ไฟล์เนื้อหาต่าง (hash ต่าง) → CONFLICT** (FN-AT-AGQ-126/132) · แถวเสีย → error report · batch log
- **Invoked by:** API-09 · **Iron rule:** ✅

### F-AGM-002-FN-10: `recordQuotaHistory`
- **Purpose:** Immutable Log (S01-07) — append-only + diff + write-back events
- **Input:** `{ quotaId, event, actor, note?, before, after }` — event: create/edit/approve/reject/delete/quota_status_written
- **Rule:** append-only · fail = block transaction แม่ · **Invoked by:** FN-01/02/03/06/08/09/12

### F-AGM-002-FN-11: `checkMemberEligible` ⭐ cross-module
- **Purpose:** ตรวจสมาชิกก่อนผูก — Approved + 1:0..1
- **Input:** `{ memberId, tenantId }` · **Output:** `{ eligible, reason }`
- **Logic:** ผ่าน ENG-EXT-03 query farmer_member: verify_status==approved (ไม่ใช่ → BR_MEMBER_NOT_APPROVED) + quota_status==no_quota (has_quota → BR_MEMBER_HAS_QUOTA)
- **Invoked by:** API-02, API-13 · **Iron rule:** ✅

### F-AGM-002-FN-12: `writeMemberQuotaStatus` ⭐ cross-module WRITE
- **Purpose:** เขียน farmer_member.quota_status กลับ (has_quota / no_quota) — หัวใจ cross-module
- **Input:** `{ memberId, status: 'has_quota'|'no_quota', sourceQuotaId, tenantId, userId }`
- **Logic:** PATCH ผ่าน ENG-EXT-03 (Farmer API) เป็น **step แยก idempotent หลัง mutation แม่ commit แล้ว** (key `{Legacy SEQ}:member:{quota_id}`) · member หาย → skip + log anomaly (EC-17, ไม่ error) · fail (TIMEOUT/502/503) → retry sync ≤3 → ยังไม่ผ่าน → **schedule async retry task (idempotent) + set pending flag + emit event `member.quota_status.change.requested` — ไม่ rollback mutation แม่** (คืน `member_update_status=scheduled_retry`) · บันทึก event=quota_status_written ใน history เมื่อสำเร็จ
- **Invoked by:** FN-01 (has_quota), FN-06 (reject→no_quota), FN-08 (delete→no_quota) · **Iron rule:** ✅ · idempotent + re-run ด้วย key เดิม = no duplicate side-effect (FN-AT-AGQ-127)

---

## §3.2 Engines (Reusable / EXISTING)

### ENG-EXT-01: `csv-import-framework` [EXISTING — CUBE core]
- config ต่อ entity=quota (No-Member) · max 5MB · template columns · UTF-8 — used by FN-09, API-10

### ENG-EXT-02: `m01-address-hierarchy` [EXISTING — M-01 master]
- lookup cascade ×2 (current + id_card) · resolve postal · validate postal↔ตำบล — used by FN-01/02/03/04/09 + UI

### ENG-EXT-03: `farmer-member-connector` [NEW — cross-module adapter] ⭐
| Field | Value |
|---|---|
| **code** | `farmer-member-connector` · **category** | integration · **status** | DRAFT (register CUBIC) |
| **capability** | (a) query member (search Approved), (b) check member quota_status (1:0..1), (c) **PATCH member quota_status** (write-back) |
| **input/output** | pure objects — wrap Farmer F-AGM-001 API (`GET member-search`, `GET :id`, `PATCH :id/quota-status`) |
- **Iron rule:** ✅ reusable (feature อื่นที่แตะ member ใช้ได้) · pure (wrap API) · substantial (cross-module contract)
- **Used by:** FN-11, FN-12 · **CUBIC note:** register — เป็น connector มาตรฐานของ AGM cross-module

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

| API | Method | Path | Functions | Engines |
|---|---|---|---|---|
| API-01 | GET | /quotas | FN-05 | — |
| API-02 | POST | /from-member | FN-01, FN-04, FN-11, FN-12, FN-10 | ENG-EXT-02, ENG-EXT-03 |
| API-03 | POST | /no-member | FN-02, FN-04, FN-10 | ENG-EXT-02 |
| API-04 | GET | /:id | — (serializer) | — |
| API-05 | PUT | /:id | FN-03, FN-04, FN-10 | ENG-EXT-02 |
| API-06 | GET | /check-number | FN-04 | — |
| API-07 | POST | /:id/verify | FN-06, FN-12, FN-10 | ENG-EXT-03 |
| API-08 | POST | /bulk-verify | FN-07(→06,12), FN-10 | ENG-EXT-03 |
| API-09 | POST | /import | FN-09(→04,02), FN-10 | ENG-EXT-01, ENG-EXT-02 |
| API-10 | GET | /import/template | — (config) | ENG-EXT-01 |
| API-11 | DELETE | /:id | FN-08, FN-12, FN-10 | ENG-EXT-03 |
| API-12 | GET | /:id/history | — (read) | — |
| API-13 | GET | /member-search | FN-11 | ENG-EXT-03 |

### Trace Verification
- [x] ทุก mutation (02/03/05/07/08/09/11) มี ≥1 Function ✅
- [x] FN-01..12 ถูก trace ครบ (FN-10 ทุก mutation, FN-12 cross-module create/reject/delete) ✅
- [x] Engine 3 ตัว trace ครบ ✅ · ไม่มี orphan · ไม่มี hidden logic ใน API ✅

---

## §3.4 Dependencies
### External called
- **F-AGM-001 Farmer Member API** (ผ่าน ENG-EXT-03) — member-search, get member, patch quota-status
- ENG-EXT-01/02
### Called into this feature
- (อนาคต) สัญญาส่งอ้อย → อ่าน quota verified

---

## §3.5 Locked Decisions Referenced
- LOCK-05: write-back FN-12 = step แยก idempotent หลัง mutation แม่ commit (keep-quota, ไม่ rollback) + compensating (EC-17) + async retry (OQ-F03 / FN-AT-AGQ-127)
- LOCK-06: optimistic lock (version) + idempotency ทุก mutation
- OQ-Q2: has_quota เขียนตอน create-link (FN-01) · OQ-Q3: edit ไม่ auto re-submit (FN-03) · OQ-Q6: SoD ใน FN-06 หลัง flag
