# 03_LOGIC — F-AGM-001 Farmer Member Management

> **Audience:** BE dev (business logic layer)
> **Scope:** All non-HTTP logic — state transitions, validations, orchestration
> **Iron Rule R8:** ทุก mutation API trace ไปที่ ≥ 1 Function/Engine ใน §3.3

---

## §3.1 Functions (Scope-Local)

### F-AGM-001-FN-01: `createFarmerMember`
- **Purpose:** สร้างสมาชิกใหม่ — gen member_id จาก Document Numbering กลาง + ตั้งสถานะเริ่มต้น
- **Input:** `{ memberData, tenantId, userId }`
- **Output:** `FarmerMember | ValidationError[]`
- **Invoked by:** API-02, FN-08 (ต่อแถว CSV)
- **Calls:** FN-03 (validate), ENG-EXT-02 (address resolve/postal), Document Numbering กลาง (seed prefix FM, `%06d` ต่อ tenant — **ห้ามเขียน gen เอง** BRD §14.2), FN-09
- **Side effects:** INSERT T_farmer_member (`verify_status='pending_approval'` เสมอ — BR-AGM-02) · history event=create
- **Error cases:** BR_CITIZEN_ID_DUPLICATE, BR_POSTAL_CODE_MISMATCH, ERR_VALIDATION_FAILED
- **Iron rule check:** ✅ no HTTP terms

### F-AGM-001-FN-02: `updateFarmerMember`
- **Purpose:** แก้ไขสมาชิก + state rule ตาม LOCK-06/07 ใน transaction เดียว
- **Input:** `{ id, memberData, expectedUpdatedAt, tenantId, userId }`
- **Output:** `{ member, resubmitted: boolean } | ConflictError | ValidationError[]`
- **Invoked by:** API-04
- **Logic outline:**
  1. Load current + check optimistic lock (`expected_updated_at`) → ไม่ตรง = STALE
  2. FN-03 validate (unique citizen_id ยกเว้นตัวเอง, postal match)
  3. สถานะเดิม `rejected` → set `verify_status='pending_approval'`, ย้าย verified_note เดิมเข้า history entry, เคลียร์ verified_by/at/note, `resubmitted=true` (LOCK-06)
  4. สถานะเดิม `approved` → แก้ได้ทุก field สถานะคงเดิม (LOCK-07); ถ้า citizen_id เปลี่ยน → mark anomaly + emit `farmer_member_citizen_id_changed_event`
  5. UPDATE + FN-09 (event=edit/resubmit, diff before/after) — transaction เดียว
- **Error cases:** ERR_STALE_DATA, BR_CITIZEN_ID_DUPLICATE, BR_POSTAL_CODE_MISMATCH
- **Iron rule check:** ✅

### F-AGM-001-FN-03: `validateFarmerMemberData`
- **Purpose:** Complex validation รวมศูนย์ (ใช้ ≥ 3 จุด: create / update / CSV row)
- **Input:** `{ memberData, tenantId, excludeId? }`
- **Output:** `ValidationError[]` (empty = ผ่าน) — `{ field, code, message }` ต่อรายการ
- **Rules (map 05_RULES §5.4):** citizen_id 13 หลักเป๊ะ strip non-digit (VR-01) · phone 9–12 หลัก (VR-02) · **email required + format** (VR-03 — authoritative, LOCK-08 optional superseded 2026-07-22; blank → "กรุณากรอกอีเมล") · required set (VR-04, รวม email) · citizen_id unique ต่อ tenant ยกเว้น excludeId (VR-05) · province/district/subdistrict สอดคล้อง hierarchy + postal match ตำบล (VR-09) ผ่าน ENG-EXT-02
- **Invoked by:** FN-01, FN-02, FN-08
- **Iron rule check:** ✅ pure-ish (read-only DB lookup for uniqueness)

### F-AGM-001-FN-04: `buildMemberListQuery`
- **Purpose:** ประกอบ query list — คำค้น 5 field + filter สถานะ + ตัด is_deleted + mask citizen_id + selectable flag
- **Input:** `{ q?, verifyStatus?, limit, offset, tenantId }`
- **Output:** `{ rows: MemberListItem[], total }` — `citizen_id_masked` เท่านั้น (S02-04), `selectable = (verify_status=='pending_approval')`
- **Search normalization (GAP-10, authoritative TC-271):** trim + ยุบช่องว่างซ้ำใน `q` ก่อน match · phone normalize ทั้งค่า stored และคำค้น (strip non-digit, `+66`→`0`) — ค้นเจอไม่ว่าจะเก็บ/พิมพ์รูปแบบใด
- **Invoked by:** API-01
- **Iron rule check:** ✅

### F-AGM-001-FN-05: `verifyFarmerMember`
- **Purpose:** ตรวจสอบยืนยันรายคน — enforce state machine + SoD + note rule
- **Input:** `{ id, verifyStatus, verifiedNote?, expectedUpdatedAt, tenantId, userId }`
- **Output:** `FarmerMember | ConflictError | RuleError`
- **Logic outline:**
  1. Optimistic lock check → STALE = ERR_STALE_DATA
  2. สถานะปัจจุบันต้อง `pending_approval` (BR-AGM-03) → ไม่ใช่ = BR_VERIFY_NOT_PENDING
  3. `rejected` ต้องมี verifiedNote (VR-07)
  4. SoD: `created_by == userId` → ERR_SOD_SELF_VERIFY (หลัง feature flag — OQ-02; flag ปิด = log anomaly แทน block)
  5. UPDATE verify_status/verified_by/verified_at/verified_note + FN-09 (event=approve/reject)
- **Invoked by:** API-05, FN-06
- **Iron rule check:** ✅

### F-AGM-001-FN-06: `bulkVerifyFarmerMembers`
- **Purpose:** Orchestrate verify กลุ่ม — per-record, ไม่ atomic ทั้งชุด (partial result)
- **Input:** `{ items: [{id, expectedUpdatedAt}], verifyStatus, verifiedNote?, tenantId, userId }`
- **Output:** `{ total, succeeded, failed, failures: [{id, member_id, error, message}] }`
- **Logic:** loop เรียก FN-05 ต่อรายการ — error รายการใด (STALE/NOT_PENDING/SoD) → นับ failed + เหตุผล, รายการอื่นไปต่อ (EC-12) · แนะนำ chunk ฝั่ง server เมื่อ > 200 รายการ (BRD §17.5)
- **Invoked by:** API-06
- **Iron rule check:** ✅

### F-AGM-001-FN-07: `softDeleteFarmerMember`
- **Purpose:** Soft delete พร้อม guard สถานะ
- **Input:** `{ id, expectedUpdatedAt, tenantId, userId }`
- **Output:** `FarmerMember | RuleError`
- **Logic:** optimistic lock → สถานะต้อง `pending_approval` (BR-AGM-05) ไม่ใช่ = BR_DELETE_NOT_PENDING → set is_deleted/deleted_at/deleted_by (ไม่มี hard delete — S06-03) + FN-09 (event=delete)
- **Invoked by:** API-07
- **Iron rule check:** ✅

### F-AGM-001-FN-08: `importFarmerMembersCsv`
- **Purpose:** Orchestrate CSV import — validate ทั้งไฟล์ก่อน → process รายแถว → partial success + error report (LOCK-04)
- **Input:** `{ file, batchId, tenantId, userId }`
- **Output:** `{ totalRows, createdCount, failedCount, errors: [{row, field, message, data}], errorReportRef }`
- **Batch idempotency (GAP-05, authoritative FN-AT-AGM-108/109 + FN-SEQ-AGM-114):** ก่อน process — เช็ค `batchId + file_hash` : เจอผลเดิม → return รายงานเดิม (ไม่ทำซ้ำ) · `batchId` เดิม + file_hash ต่าง → ERR_BATCH_CONFLICT · แต่ละแถวใช้ idempotency key `{FN-AT-AGM-109}:{batchId}:{row_index}:{citizen_id}` เพื่อกัน retry/resume สร้างซ้ำ
- **Logic outline:**
  1. File-level (ผ่าน ENG-EXT-01 + Import Config): .csv เท่านั้น, ≤ limit (config — ห้าม hardcode 5MB), encoding UTF-8 (EC-09), header ตรง 10 คอลัมน์เป๊ะ (คอลัมน์ที่ 6 = `address` → map DB `address_line`; EC-10 — reject ทั้งไฟล์ + บอกคอลัมน์ผิด)
  2. Per-row: FN-03 validate + ตรวจซ้ำภายในไฟล์ (citizen_id เดิมแถวก่อนหน้า → แถวหลัง error "เลขบัตรประชาชนซ้ำภายในไฟล์" — EC-11) + resolve ตำบลกับ M-01 (สะกดไม่ตรง → "ไม่พบตำบลใน[อำเภอ]" — EC-13) + postal ว่าง → auto จากตำบล / ระบุ → ต้อง match (VR-09)
  3. แถวผ่าน → FN-01 create · แถวเสีย → collect error (ไม่ block แถวอื่น)
  4. สรุป + error report (แถว/ฟิลด์/ข้อความ/ข้อมูล) download ได้ + batch log (MET-02)
- **Invoked by:** API-08
- **Iron rule check:** ✅

### F-AGM-001-FN-09: `recordMemberHistory`
- **Purpose:** เขียน Immutable Master Data Log (S01-07) — ทุก event พร้อม diff Before/After
- **Input:** `{ memberId, event, actor, note?, before, after }` — event: create/edit/resubmit/approve/reject/delete
- **Output:** `HistoryEntry`
- **Rule:** append-only ห้าม UPDATE/DELETE · เขียน fail = block transaction แม่ (BRD §17.2) · resubmit event เก็บ verified_note เดิมไว้ใน entry
- **Invoked by:** FN-01/02/05/07 (ผ่าน transaction), FN-08
- **Iron rule check:** ✅

---

## §3.2 Engines (Reusable / CUBIC-Registered)

> ไม่มี engine ใหม่ใน feature นี้ — reuse ของกลาง 2 ตัว (EXISTING):

### ENG-EXT-01: `csv-import-framework` [EXISTING — CUBE core]
| Field | Value |
|---|---|
| **code** | `csv-import-framework` |
| **status** | REGISTERED (CUBE core) — ⚠️ ต้องเพิ่ม config ต่อ entity `farmer_member` (BRD §12.3) |
| **config ที่ต้อง seed** | entity=farmer_member · max_size=5MB · template 10 columns (LOCK-04) · encoding=UTF-8 |
- **Used by:** FN-08, API-09 (template gen)
- Import Config อ่านจาก Admin Panel (Phase 2 มีหน้า config — Phase 1 seed ผ่าน config table)

### ENG-EXT-02: `m01-address-hierarchy` [EXISTING — CUBE core master]
| Field | Value |
|---|---|
| **code** | `m01-address-hierarchy` |
| **status** | REGISTERED (M-01 master กลาง) |
- **Capability ที่ใช้:** lookup จังหวัด→อำเภอ→ตำบล (cascade) · resolve postal จากตำบล · validate postal↔ตำบล · resolve ชื่อตำบลจาก text (CSV — EC-13)
- **Used by:** FN-01, FN-02, FN-03, FN-08 + UI search-select (ผ่าน master API กลาง)

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| API-01 | GET | /farmer-members | FN-04 | — |
| API-02 | POST | /farmer-members | FN-01, FN-03, FN-09 | ENG-EXT-02 |
| API-03 | GET | /farmer-members/:id | — (serializer masking ตาม D-CLASS) | — |
| API-04 | PUT | /farmer-members/:id | FN-02, FN-03, FN-09 | ENG-EXT-02 |
| API-05 | POST | /farmer-members/:id/verify | FN-05, FN-09 | — |
| API-06 | POST | /farmer-members/bulk-verify | FN-06 (→FN-05), FN-09 | — |
| API-07 | DELETE | /farmer-members/:id | FN-07, FN-09 | — |
| API-08 | POST | /farmer-members/import | FN-08 (→FN-03, FN-01), FN-09 | ENG-EXT-01, ENG-EXT-02 |
| API-09 | GET | /import/template | — (config read) | ENG-EXT-01 |
| API-10 | GET | /:id/history | — (read-only) | — |

### Trace Verification (Self-Check)
- [x] ทุก mutation API (02/04/05/06/07/08) มี ≥ 1 Function ✅
- [x] ทุก FN-01..09 ถูก trace อย่างน้อย 1 จุด ✅ (FN-09 ผ่าน mutation ทุกตัว)
- [x] Engine ทั้ง 2 ถูก trace ✅
- [x] ไม่มี hidden logic ใน 02_API ✅

---

## §3.4 Dependencies

### External called
- Document Numbering service (CUBE Admin config) — FN-01 gen `FM-%06d`
- ENG-EXT-01 / ENG-EXT-02 (ดู §3.2)

### Called into this feature
- Module Quota (อนาคต) → API-03 / API-01 filter approved (ดู 02_API §2.X)

---

## §3.5 Locked Decisions Referenced
- LOCK-03: idempotency key format `{Legacy FN}:{id}:{user}` — enforce ที่ middleware + FN ทุก mutation
- LOCK-06/07: state rules อยู่ใน FN-02 (procedural) + 05_RULES §5.2 (declarative) — สองที่ต้องตรงกันเสมอ
- OQ-02: SoD block ใน FN-05 อยู่หลัง feature flag `sod_self_verify_block` (default: log-only)

### §3.5.1 Legacy ↔ Authoritative FN reconciliation (GAP-06, 2026-07-22) ⚠️
Scope-local FN-01..09 ของ pack นี้ map พฤติกรรมครบทุกฟังก์ชันของ authoritative scheme **FN-AT/SEQ-AGM 99–114** (ตารางเต็มที่ 02_API §2.1.1). Legacy binding `FN-AT-AGM-103` (ผูก Verify) และ `FN-SEQ-AGM-110` (ผูก CSV import) **predate การ renumber** และ mirror as-built code — **คงไว้ใน idempotency key เดิม** แต่ dev **ต้องอ้าง authoritative 99–114 เมื่อ cross-ref**: authoritative **103 = Search** (=FN-04), **106 = Verify single** (=FN-05), **107 = Bulk Verify** (=FN-06), **110 = Create** (=FN-01 orchestration), **114 = Upload CSV** (=FN-08). CSV idempotency ใช้ **108/109/114** ตาม authoritative.
