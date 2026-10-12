# 02_API — F-HR-CERT · หนังสือรับรอง

> Audience: **Backend (HTTP layer)** · base path `/api/v1/certificate`
> ⭐ **กติกาของไฟล์นี้:** ที่นี่มีแต่ **สัญญาของ endpoint** — ⭐ **ห้ามมี `createX` / `updateX` / สูตรคำนวณ / การตัดสินใจทางธุรกิจ ซ่อนอยู่ที่นี่** ตรรกะทั้งหมดอยู่ที่ `03_LOGIC` (R8)
> ทุก mutation ต้องมี **`Idempotency-Key`** (ยกเว้นที่ระบุ) และ **`row_version`** สำหรับ optimistic lock

## §2.0 Convention

| หัวข้อ | ค่า |
|---|---|
| Path | `/api/v1/certificate/*` (snake_case ใน body · camelCase ห้ามใช้) |
| Auth | Bearer token · ⭐ **สิทธิ์ตัดสินที่ Policy Center ทุกครั้ง ไม่ cache** |
| Tenant | ⭐ **`company_id` บังคับทุก request** (query หรือ body) |
| Concurrency | `If-Match: <row_version>` บน PATCH/POST ที่เปลี่ยนสถานะ → ไม่ตรง = `409 ERR_ROW_VERSION_CONFLICT` |
| Idempotency | `Idempotency-Key` บน POST ที่มีผลข้างเคียงภายนอก (submit · issue · deliver · revoke · reissue) |
| Error | `{ "code": "ERR_*", "message": "<ข้อความไทยที่ผู้ใช้อ่านได้>", "detail": {...}, "link": "<ลิงก์ต้นทาง ถ้ามี>" }` — catalog เต็มที่ `05_RULES §5.6` |
| Paging | `page` · `page_size` (default 50 · max 500) |

## §2.1 Endpoint Inventory (30 ตัว + 11 cross-module outbound)

| # | Method + Path | ทำอะไร | Function/Engine (`03_LOGIC`) | หน้าจอ |
|---|---|---|---|---|
| API-01 | `GET /certificates` | รายการคำขอ (ค้น · กรอง · เรียง · แบ่งหน้า) | `F-42 listCertificates` | P-01 |
| API-02 | `GET /certificates/{id}` | รายละเอียดใบ + snapshot (ถ้ามี) + สายอนุมัติ | `F-42` | P-01 มุมมองใบ |
| API-03 | `POST /certificates` | สร้างร่าง | `F-01 createDraft` · `F-04` | ตัวช่วยขั้น 1 |
| API-04 | `PATCH /certificates/{id}` | แก้ร่าง (`If-Match`) | `F-02 updateDraft` · `F-04` | ตัวช่วยขั้น 1–2 |
| API-05 | `DELETE /certificates/{id}` | ⭐ ลบร่าง **เฉพาะที่ยังไม่มีเลขที่** | `F-03 deleteDraft` | ตัวช่วย · P-01 |
| API-06 ⭐ | `POST /certificates/{id}/submit` | ⭐ **T-02** — ออกเลข + resolve สาย + แช่แข็ง + ตรวจ SoD + ตรวจร่องรอยความยินยอม | `F-13 submitCertificate` (orchestrator) | ตัวช่วยขั้น 5 |
| API-07 | `GET /certificates/{id}/approval-chain/preview` | ดูรูปสายก่อนกดส่ง (ยังไม่แช่แข็ง) | `F-05` · `F-06` · `F-12` | ตัวช่วยขั้น 4 |
| API-08 | `POST /certificates/{id}/approve` | อนุมัติขั้นปัจจุบัน | `F-14 approveStep` | P-02 · มุมมองใบ |
| API-09 | `POST /certificates/{id}/reject` | ไม่อนุมัติ (เหตุผลบังคับ) | `F-15 rejectCertificate` | P-02 · มุมมองใบ |
| API-10 | `POST /certificates/{id}/cancel` | ผู้ขอยกเลิก | `F-16 cancelCertificate` | มุมมองใบ |
| **API-11** ⭐⭐ | `POST /certificates/{id}/issue` | ⭐⭐ **T-06 จุดตรึงข้อเท็จจริง** | `F-26 issueCertificate` (orchestrator) → `F-20 buildSnap` · `F-21 assertIssuable` · `F-22` · `F-23` · `F-24` · `F-25` | มุมมองใบ (สถานะอนุมัติแล้ว) |
| API-12 | `GET /certificates/{id}/preview-facts` | ⭐ อ่านสดจากต้นทางเพื่อแสดงในขั้นที่ 3 — **ไม่ตรึง ไม่บันทึก** | `F-17 previewFacts` · `F-18` · `F-19` | ตัวช่วยขั้น 3 |
| API-13 | `GET /certificates/{id}/document?rendition=&mode=view\|download` | แสดง/ดาวน์โหลดเอกสาร | `F-22` · `F-23` · `F-28 recordAccess` | แท็บเอกสาร · P-03 · P-04 |
| API-14 | `POST /certificates/{id}/deliver` | **T-07** บันทึกการส่งมอบ/ดาวน์โหลด | `F-27 recordDelivery` · `F-24` | มุมมองใบ · P-04 |
| API-15 | `POST /certificates/{id}/revoke` | **T-08** เพิกถอน (เหตุผลบังคับ) | `F-29 revokeCertificate` · `F-24` · `F-39` | มุมมองใบ · P-03 |
| API-16 | `POST /certificates/{id}/reissue` | **T-09** ออกใหม่แทน → สร้างใบใหม่ | `F-30 reissueCertificate` | มุมมองใบ |
| API-17 | `GET /certificates/{id}/history` | timeline + รหัสเวอร์ชันต้นทาง | `F-42` | แท็บประวัติ |
| API-18 | `GET /certificates/{id}/access-log` | ร่องรอยการเปิด/ดาวน์โหลด | `F-42` | แท็บประวัติ |
| API-19 | `GET /certificates/register` | ทะเบียนที่ออกแล้ว + ค้น 6 ทาง | `F-34 searchRegister` · `ENG-04` | P-03 |
| API-20 | `GET /certificates/verify?code=` | ค้นด้วย `verification_code` | `F-35 verifyByCode` | P-03 |
| API-21 | `GET /certificate-types` | รายการประเภทที่ Document Configuration เผยแพร่ | (proxy อ่านอย่างเดียว) | ตัวช่วยขั้น 1 |
| API-22 | `GET /certificate-templates?language=` | แม่แบบที่เผยแพร่ + `template_version_id` + สถานะ active | (proxy อ่านอย่างเดียว) | ตัวช่วยขั้น 2 |
| API-23 | `POST /certificates/{id}/attachments` | แนบเอกสารประกอบคำขอ | `F-02` | ตัวช่วยขั้น 5 · แท็บรายละเอียด |
| API-24 | `GET /certificates/duplicate-check?employee_id=&cert_type=&language=` | ตรวจใบซ้ำที่รออนุมัติ | `F-11 checkDuplicatePending` | ตัวช่วยขั้น 5 |
| API-25 | `GET /certificates/employees/search?q=&include_left=` | ⭐ ค้นพนักงาน **รวมผู้ที่พ้นสภาพ** (proxy Employee Master) | (proxy) | ตัวช่วยขั้น 1 |
| API-26 | `GET /certificates/mine` | คำขอ + หนังสือของผู้ใช้ที่ล็อกอิน | `F-42` | P-04 |
| API-27 | `GET /certificates/inbox` | ใบที่ผู้ใช้อยู่ในขั้นปัจจุบัน | `F-42` | P-02 |
| API-28 | `POST /certificates/{id}/upstream-flag/ack` | HR รับทราบธงข้อมูลต้นทางเปลี่ยน | `F-33 ackUpstreamChangedFlag` | P-03 |
| API-29 | `GET /read-model/register` | ⭐ **มุมมองที่เผยแพร่** (ESS ⏳W6) — §0.13.2 | `F-43 buildRegisterReadModel` | (ปลายทาง) |
| API-30 | `GET /certificates/link-status` · `POST /certificates/link-status/override` | สถานะ Module Linkage + สวิตช์ยืนยันด้วยมือ | `F-43` | P-03 |
| — | `POST /certificate/usage` | ให้ consumer ลงทะเบียนว่าอ่านทะเบียนอยู่ (CT-4) | (registry) | — |

## §2.2 Contract ของ endpoint ที่มีสัญญาเฉพาะ (6 ตัว)

### API-06 · `POST /certificates/{id}/submit` ⭐ (T-02)

```
POST /api/v1/certificate/certificates/{id}/submit
Headers: If-Match: <row_version> · Idempotency-Key: <uuid>
Body: { "company_id": "<uuid>",
        "approver_slots": [ { "step_seq": 1, "employee_id": "<uuid>" },
                            { "step_seq": 2, "employee_id": "<uuid>" } ],   ← จำนวนเท่าที่ resolve ได้จริง
        "consent_ack": true, "consent_note": "…",                            ← บังคับเมื่อเข้าเงื่อนไข
        "duplicate_confirmed": false, "duplicate_reason": null }
```

**ลำดับที่เซิร์ฟเวอร์ทำ (ห้ามสลับ — `03_LOGIC §3.0.2`):**
1. ตรวจสถานะต้องเป็น `draft` → ไม่ใช่ = `409 ERR_STATE_CHANGED`
2. `F-09 validateSubmit` (ช่องบังคับครบ · ภาษา EN มีชื่อ EN)
3. `F-10 checkConsentTrace` → ขาด = `422 ERR_CONSENT_REQUIRED`
4. `F-11 checkDuplicatePending` → มีใบซ้ำและยังไม่ยืนยัน = `409 ERR_DUPLICATE_PENDING`
5. `F-04 computeHasSalaryFigure` → `F-05 pickAction` → `F-06 resolveApprovalChain` (⭐ **ไม่ส่งค่าเงิน**)
6. `F-12 assertSoD` → ละเมิด = `422 ERR_SOD_VIOLATION`
7. ตรวจว่า slot ครบตามจำนวนขั้นจริง → ไม่ครบ = `422 ERR_APPROVER_SLOT_INCOMPLETE`
8. ⭐ `F-08 issueDocNo` — `ENG-DOC-NUM.next('CERT', company_ctx)`
9. `F-07 freezeApprovalChain` → เขียน `T_certificate_approval_trace`
10. สถานะ → `pending_approval` · เขียน history · `F-38` ยิง `cert_requested`

**Response 200:** `{ "cert_doc_no": "CERT-2026-0043", "status": "pending_approval", "approval_chain": [...], "row_version": 2 }`

> ⭐ **ข้อ 8 อยู่หลังข้อ 7 เสมอ** — ออกเลขก่อนแล้วตรวจไม่ผ่าน = เลขหายไปเปล่า ๆ (เลขไม่ reuse)

### API-11 · `POST /certificates/{id}/issue` ⭐⭐ (T-06 · หัวใจของฟีเจอร์)

```
POST /api/v1/certificate/certificates/{id}/issue
Headers: If-Match: <row_version> · Idempotency-Key: <uuid>
Body: { "company_id": "<uuid>",
        "issue_date": "2026-08-30",              ← default = วันนี้ · ⭐ ค่านี้เป็น as_of ของทุกอย่าง
        "template_id": "<uuid>",
        "changed_facts_confirmed": false,        ← บังคับ true เมื่อ F-19 พบว่าข้อมูลเปลี่ยนตั้งแต่วันยื่น
        "scheduled_warning_ack": false }         ← บันทึกว่าผู้ออกเห็นคำเตือนแล้ว (ไม่บล็อก)
```

**ลำดับที่เซิร์ฟเวอร์ทำ — `03_LOGIC §3.0.1` (ห้ามสลับ):**
```
1. lock แถวใบ  → สถานะต้องเป็น approved · ไม่ใช่ = 409 ERR_STATE_CHANGED / ERR_ALREADY_ISSUED
2. F-20 buildSnap(employee_id, as_of = issue_date, cert_type, language)
     → เรียก X-API-01…05 ทั้งหมดด้วย as_of เดียวกัน
     → ต้นทางล้ม = 502 ERR_UPSTREAM_UNAVAILABLE (ระบุว่าต้นทางไหน) · ⭐ ไม่ตรึงอะไรเลย
3. F-21 assertIssuable(snap)  → ตกด่านใดด่านหนึ่ง = 4xx + ลิงก์ต้นทาง · ⭐ ไม่ตรึงอะไรเลย
     ERR_SALARY_MASKED (+ ยิง cert.issue_blocked_masked) · ERR_NO_RATE_AT_DATE
     ERR_NO_EMPLOYMENT_WINDOW · ERR_NOT_STARTED · ERR_NO_EN_NAME · ERR_TEMPLATE_INACTIVE
4. F-22 selectRendition(language, has_salary_figure) → 1 ใน 4 ค่า
5. เขียน T_certificate_snapshot (INSERT เดียว · ไม่มี UPDATE ตลอดกาล)
6. F-23 renderDocument(snapshot, rendition, template_version_id)
7. F-24 storeDocumentCopy(pdf, 'issued')   ← ล้ม = ไม่เปลี่ยนสถานะ ไม่ยิงอะไร (PR-5)
8. F-25 generateVerificationCode
9. สถานะ → issued · เขียน history
10. F-38 ยิง cert_issued (+ cert_ready_for_pickup ถ้ารับที่ HR) · F-39 ยิง cert.issued (SecC)
```

**Response 200:** `{ "status": "issued", "issue_date": "…", "rendition": "salary_th", "verification_code": "7K2M-9QX4", "source_version_ids": {...}, "row_version": 5 }`
**Response 422 (masked):** `{ "code": "ERR_SALARY_MASKED", "message": "ต้องมีสิทธิ์เข้าถึงข้อมูลค่าจ้างจึงจะออกหนังสือประเภทนี้ได้", "detail": { "cert_type": "salary" } }`
⭐ **ไม่มี response แบบ "ออกสำเร็จแต่ไม่มีตัวเลข"** — ไม่มี code path นั้น

### API-12 · `GET /certificates/{id}/preview-facts` ⭐

อ่านสดจากต้นทางเพื่อแสดงในขั้นที่ 3 — ⭐ **ไม่เขียนอะไรลงฐาน ไม่ตรึงอะไร**
คืน: บล็อกข้อเท็จจริง + `warnings[]` 3 แบบ (`SCHEDULED_MOVEMENT_PENDING` · `FACTS_CHANGED_SINCE_SUBMIT` · `CERT_POLICY_NOT_PUBLISHED`) + `blockers[]` (ถ้ามี)
⭐ **`warnings` กับ `blockers` เป็นคนละ array** — warning ไม่กันการเดินต่อ · blocker กัน

### API-13 · `GET /certificates/{id}/document`

- `rendition` optional — ⭐ **ถ้าไม่ส่ง เซิร์ฟเวอร์ใช้ค่าที่แช่แข็งไว้บนใบ** · **ส่งค่าที่ไม่ตรงกับที่แช่แข็ง = `422 ERR_RENDITION_MISMATCH`** (กันการขอ rendition ที่มีตัวเลขจากใบที่ไม่มี)
- ⭐ **ACL ตรวจที่ตัวไฟล์ทุกครั้ง** — ไม่มีสิทธิ์ RESTRICTED + ไฟล์มีตัวเลข = `403 ERR_RESTRICTED_FILE_ACCESS`
- ทุกครั้งที่สำเร็จ → `F-28 recordAccess` + (ถ้าไฟล์มีตัวเลข) `F-39` ยิง `cert.restricted_viewed`
- ⭐ **ก่อนสถานะ `issued` = render จากค่าที่อ่านสด (ตัวอย่าง) · ตั้งแต่ `issued` = render จาก snapshot เท่านั้น**

### API-16 · `POST /certificates/{id}/reissue` ⭐

```
Body: { "reissue_reason": "…", "cert_type": "…", "language": "…", "copies": 1, "delivery_method": "…" }
```
**สร้างใบใหม่เป็นร่างที่ `supersedes = <เลขเดิม>`** → ผู้ใช้เดินตัวช่วยต่อ → กดส่ง → **เดินสายอนุมัติใหม่ทั้งสาย**
⭐ **ใบเดิมยังไม่เปลี่ยนสถานะ ณ จุดนี้** — เปลี่ยนเป็น `superseded` เมื่อ **ใบใหม่ออกสำเร็จ** เท่านั้น (`F-31` ถูกเรียกจาก `F-26` ไม่ใช่จาก `F-30`)
> เหตุผล: เปลี่ยนใบเดิมก่อน = ช่วงหนึ่งพนักงานไม่มีเอกสารที่ใช้ได้เลย

### API-29 · `GET /read-model/register` — มุมมองที่เผยแพร่

โครงเต็มอยู่ที่ **`00_OVERVIEW §0.13.2`** · ⭐ **ไม่คืนจำนวนเงิน · ไม่คืนข้อความอิสระ · ไม่คืนสายอนุมัติรายขั้น**

## §2.3 API ที่เปลี่ยนสถานะ → transition

| API | transition | สถานะก่อน → หลัง |
|---|---|---|
| API-03 | T-01 | (ใหม่) → `draft` |
| API-06 | T-02 | `draft` → `pending_approval` |
| API-09 | T-03 | `pending_approval` → `rejected` |
| API-10 | T-04 | `draft` / `pending_approval` → `cancelled` |
| API-08 (ขั้นสุดท้าย) | T-05 | `pending_approval` → `approved` |
| **API-11** | **T-06** | `approved` → `issued` |
| API-13 (download) / API-14 | T-07 | `issued` → `delivered` |
| API-15 | T-08 | `issued` / `delivered` → `revoked` |
| (ภายใน `F-26` ของใบใหม่) | T-09 | `issued` / `delivered` → `superseded` |
| (นาฬิกา) | T-10 | `approved` → `approved` (⭐ ไม่เปลี่ยนสถานะ · เตือนอย่างเดียว) |
| (event listener) | T-11 | (⭐ ไม่เปลี่ยนสถานะ · ติดธง) |
| API-13 · API-14 | T-12 | (⭐ ไม่เปลี่ยนสถานะ · บันทึกร่องรอย) |

## §2.4 API → Logic Trace Table (Phase 3.5 Anchor · R8)

| API | Function / Engine ที่เรียก | เป็น mutation ไหม |
|---|---|---|
| API-01 · API-02 · API-17 · API-18 · API-26 · API-27 | `F-42 listCertificates` | ✗ |
| API-03 | `F-01 createDraft` → `F-04 computeHasSalaryFigure` | ✅ |
| API-04 | `F-02 updateDraft` → `F-04` | ✅ |
| API-05 | `F-03 deleteDraft` | ✅ |
| **API-06** | `F-13 submitCertificate` → `F-09` · `F-10` · `F-11` · `F-04` · `F-05` · `F-06` · `F-12` · `F-08` · `F-07` · `F-38` | ✅ |
| API-07 | `F-04` · `F-05` · `F-06` · `F-12` · `ENG-03` · `ENG-08` | ✗ |
| API-08 | `F-14 approveStep` → `F-38` | ✅ |
| API-09 | `F-15 rejectCertificate` → `F-38` | ✅ |
| API-10 | `F-16 cancelCertificate` | ✅ |
| **API-11** | `F-26 issueCertificate` → `F-20` · `F-21` · `F-22` · `F-23` · `F-24` · `F-25` · `F-31` · `F-36` · `F-37` · `F-38` · `F-39` · `ENG-01` · `ENG-02` · `ENG-07` | ✅ |
| API-12 | `F-17 previewFacts` → `F-18` · `F-19` · `F-36` · `F-37` · `ENG-05` · `ENG-06` | ✗ |
| API-13 | `F-22` · `F-23` · `F-28 recordAccess` · `F-39` | ✅ (เขียน access log) |
| API-14 | `F-27 recordDelivery` → `F-24` · `F-39` | ✅ |
| API-15 | `F-29 revokeCertificate` → `F-24` · `F-38` · `F-39` | ✅ |
| API-16 | `F-30 reissueCertificate` → `F-01` | ✅ |
| API-19 | `F-34 searchRegister` → `ENG-04` | ✗ |
| API-20 | `F-35 verifyByCode` | ✗ |
| API-21 · API-22 · API-25 | (proxy อ่านอย่างเดียว — **ไม่มี logic**) | ✗ |
| API-23 | `F-02` | ✅ |
| API-24 | `F-11 checkDuplicatePending` | ✗ |
| API-28 | `F-33 ackUpstreamChangedFlag` | ✅ |
| API-29 · API-30 | `F-43 buildRegisterReadModel` | ✗ |
| (นาฬิกา) | `F-41 escalatePendingIssue` → `F-38` | ✅ (เขียน history) |
| (event listener) | `F-32 applyUpstreamChangedFlag` | ✅ |
| (bootstrap) | `F-40 registerWhereUsed` | ✅ (ที่ต้นทาง) |

**ตรวจ R8:** ทุก mutation API มี ≥1 Function/Engine ✅ **16/16** · ทุก Function ถูก trace ✅ **44/44** · ทุก Engine ถูก trace ✅ **8/8** · ไม่มี orphan ✅

## §2.5 Cross-Module Contract (11 ตัว — outbound)

| # | ปลายทาง | Method + Path | เมื่อไร | กติกา |
|---|---|---|---|---|
| **X-API-01** | Salary Structure | `GET /api/v1/salary-structure/resolve?date=<issue_date>&company_id=&employee_id=&scope=employee` | `F-20` (เฉพาะ `cert_type = salary`) · `F-17` (ขั้น 3 · ไม่แสดงตัวเลข) | ⭐ `date` = `issue_date` เสมอ · เก็บ `version_id.band` · **ห้าม cache ข้ามวัน** · `masked = true` → **ปฏิเสธการออก** |
| **X-API-02** | Employee Movement | `GET /api/v1/movement/assignment/resolve?as_of=<issue_date>&company_id=&employee_id=&include=source,scheduled` | `F-20` · `F-17` · `F-18` | ⭐ **`scheduled[]` ใช้เฉพาะ `F-18` (คำเตือน) — ห้ามไหลเข้า `F-20`** · เก็บ `source_movement_doc_no` |
| **X-API-03** | Employee Movement | `GET /api/v1/movement/history/resolve?employee_id=&as_of=<issue_date>&company_id=` | `F-20` (เมื่อ `show_position_history = true`) | ⭐ **ใช้เฉพาะกลุ่ม `effective[]`** — `scheduled[]` ห้ามพิมพ์ |
| **X-API-04** | On/Offboard | `GET /api/v1/onboard/employment-window/resolve?as_of=<issue_date>&company_id=&employee_id=&include=case` | `F-20` · `F-17` | ⭐ `window: null` → บล็อก **ห้ามตีความว่าไม่ใช่พนักงาน** · `config_version_ids.employment_term` เป็น `null` เสมอ — **ต้องรับได้** |
| **X-API-05** | HR Configuration | `GET /api/v1/hr-config/resolve?date=<issue_date>&company_id=&group=cert_policy` | `F-20` · `F-17` | ⭐ **404 / ไม่มีกลุ่ม = ค่าว่าง ไม่ใช่ error** (PR-8) · `hr_config = null` · **ไม่บล็อกการออก** |
| **X-API-06** | DOA Engine | `GET /doa/resolve?action_id=&employee_id=&company_id=` | `F-06` | ⭐⭐ **ไม่ส่ง parameter ที่เป็นจำนวนเงินเลย** · ผลลัพธ์คือรูปสาย 1 หรือ 2 ขั้น |
| **X-API-07** | Document Configuration | `ENG-DOC-NUM.next('CERT', company_ctx)` | `F-08` (ที่ T-02 เท่านั้น) | **ห้ามฟอร์แมตเอง ห้าม +1 เอง** |
| **X-API-08** | Document Configuration | `ENG-DOC-STORE.store(pdf, 'CERT', cert_id, <event>)` — `issued` · `sent_external` · `revoked` · `superseded` | `F-24` | ⭐ **idempotent ต่อ `(cert_id, event)`** · **ลบไม่ได้ ทับไม่ได้ — เพิ่มสำเนาใหม่เสมอ** |
| **X-API-09** | ENG-NOTIFY | `emit(event_id, { ref: cert_id, vars: {...} })` | `F-38` | ⭐ **ห้ามใส่จำนวนเงินใน `vars`** · **ห้ามยิง `doa_*`** · `cert_issued` ยิงหลัง `store()` สำเร็จเท่านั้น |
| **X-API-10** | ENG-CSQ | `POST /csq/events` | `F-39` | ⭐ **ท่อ `secc` ท่อเดียว** · **payload ไม่มีจำนวนเงิน** · `idempotency_key = F-HR-CERT:{cert_doc_no}:{event}:{seq}` |
| **X-API-11** | ต้นทาง 4 ตัว | `POST /api/v1/salary-structure/usage` · `/movement/usage` · `/onboard/usage` · `/hr-config/items/{id}/usage` | `F-40` (bootstrap) | ⭐ **เป็นการลงทะเบียนว่าอ่านอยู่ ไม่ใช่การเขียนข้อมูล** — ข้อยกเว้นเดียวของ LOCK-NOWRITE |

> ⭐⭐ **ไม่มี outbound ตัวใดที่เขียนข้อมูลกลับเข้าต้นทาง** — X-API-07/08 เป็นการเรียกใช้บริการของ engine · X-API-11 เป็นการลงทะเบียน where-used · ดู `00_OVERVIEW §0.13.5(ข)`

## §2.6 Inbound Event Listener

| event ที่ฟัง | มาจาก | ทำอะไร |
|---|---|---|
| `ofb_case_cancelled` · `onb_start_date_changed` | On/Offboard | `F-32` — ⭐ **ติดธง `upstream_changed_flag` บนใบที่ออกไปแล้วซึ่งอ้าง `case_ref` นั้น · ไม่แก้เนื้อหา ไม่เปลี่ยนสถานะ** |
| `move_cancelled_before_effective` · `move_superseded` · `move_voided_employee_left` · `move_effective` | Employee Movement | `F-32` (สำหรับใบที่ออกแล้ว) + ล้าง cache ภายในวัน (`MV-5`) |
| `salstruct.effective` · `salcomp.*` | Salary Structure | ล้าง cache ภายในวัน (`SS-3`) — ⭐ **ใบที่ออกแล้วไม่กระทบ** |
| `hrconfig.effective` | HR Configuration | ล้าง cache ภายในวัน (`C-3`) |
