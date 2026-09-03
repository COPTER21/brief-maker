# 02_API — F-HR-ONBOARD · On/Offboard (เข้าออกงาน)

---

## §2.0 กติกาที่ใช้กับทุก endpoint

| # | กติกา |
|---|---|
| A-1 | base path = `/api/v1/onboard` · REST · error envelope มาตรฐาน CUBE (`§2.5`) |
| A-2 | ทุก request กรองด้วย `tenant_id` จาก token · `company_id` บังคับเมื่อผู้เช่ามีบริษัทลูก |
| A-3 | **ทุก mutation ต้องมี `Idempotency-Key`** — unique ต่อ (feature, case, ref, action) · ยิงซ้ำด้วยคีย์เดิม = คืนผลเดิม ไม่สร้างซ้ำ |
| A-4 | **ทุก mutation trace ไปที่ Function หรือ Engine ใน `03_LOGIC`** (R8 · ตารางเต็มที่ `03_LOGIC §3.3`) |
| A-5 | **การปิดบังทำที่ชั้น API ไม่ใช่ UI** — field ชั้น Confidential ถูกแทนด้วย `null` เมื่อผู้เรียกไม่มีสิทธิ์ พร้อมเขียนร่องรอยการเข้าถึง |
| A-6 | **ทุกการอ่านค่าจากต้นทางส่ง `date`/`as_of` เสมอ และเก็บ `version_id`** (C-1 · C-2 · AT-1 · LV-1 · OB-1) |
| A-7 ⭐ | **ไม่มี endpoint ใดในไฟล์นี้ที่เขียนข้อมูลสิทธิ์** — ดู §2.2.1 |
| A-8 | **ไม่มี endpoint ลบ** — ทุกตารางเป็น append-only / soft archive |
| A-9 | **ไม่มี field จำนวนเงินใน request หรือ response ของ endpoint ใดเลย** (LOCK-MONEY) |
| A-10 | **การกรองสิทธิ์ทำที่ระดับ query** — ทรัพยากรที่อยู่นอกขอบเขตของผู้เรียกคืน **404** ไม่ใช่ 403 |

---

## §2.1 Endpoint ภายใน feature (ผู้ใช้เรียกจากหน้าจอ)

| # | Method · Path | ทำอะไร | Function/Engine | สิทธิ์ |
|---|---|---|---|---|
| **API-01** | `GET /cases` | รายการรอบ (กรอง: `case_type` · `q` · `department` · `status` · ช่วงวัน · `has_pending_access`) · แบ่งหน้า | `listCases` | ตามขอบเขต |
| **API-02** | `GET /cases/:id` | รอบหนึ่งใบพร้อมงาน · ทะเบียนสิทธิ์ · ทรัพย์สิน · สายอนุมัติ | `getCase` | ตามขอบเขต · **เขียนร่องรอยการเปิดดูข้อมูลอ่อนไหว** |
| **API-03** | `POST /cases` | สร้างรอบ (เข้า/ออก) · generate งานเป็น SOW · สร้างทะเบียนสิทธิ์ตั้งต้น | `createCase` → `ENG-OPSOW-01` · `ENG-WORKDAY-01` | HR · หัวหน้า (ออกงานเท่านั้น) |
| **API-04** | `GET /cases/preview` | preview งานที่จะถูกสร้างพร้อมกำหนดเสร็จ (ยังไม่บันทึก) | `previewTasks` → `ENG-WORKDAY-01` | เดียวกับ API-03 |
| **API-05** | `PATCH /cases/:id/dates` | แก้วันเริ่มงาน/วันแจ้ง/วันทำงานวันสุดท้าย → **คำนวณกำหนดเสร็จของงานที่ยังไม่เสร็จใหม่** | `updateCaseDates` → `ENG-WORKDAY-01` | HR · หัวหน้า (ก่อนส่งอนุมัติ) |
| **API-06** | `POST /cases/:id/submit` | ส่งอนุมัติ — **resolve สายจาก DOA แล้ว freeze** | `submitCase` → `ENG-DOA-01` | HR · หัวหน้า |
| **API-07** | `POST /cases/:id/approve` | อนุมัติขั้นปัจจุบัน · ครบสาย → `approved` + **ตั้ง `revocation_due_at`** + เผยแพร่วันสุดท้าย | `approveCase` → `ENG-DOA-01` | **ผู้ถือ slot ปัจจุบันเท่านั้น** |
| **API-08** | `POST /cases/:id/reject` | ไม่อนุมัติ (**บังคับ `reject_reason`**) | `rejectCase` | ผู้ถือ slot ปัจจุบัน |
| **API-09** | `POST /cases/:id/cancel` | ยกเลิกรอบ (**บังคับ `cancel_reason`**) · ปิดงานค้าง · ถอนค่าที่เผยแพร่ · **ออกคำขอคืนสิทธิ์ถ้าเคยเพิกถอน** | `cancelCase` → `ENG-REVOKE-01` | HR (+ A-3 เมื่อผ่าน T-13/T-14) |
| **API-10** | `POST /cases/:id/access-requests` ⭐ | **ส่งคำขอเปิดสิทธิ์** ไปยัง Roles & Permissions (รายการที่ผู้ใช้ยืนยัน) | `requestGrant` → `ENG-REVOKE-01` | HR · ผู้รับผิดชอบงาน IT |
| **API-11** | `POST /cases/:id/revocation-requests` ⭐ | **ส่งคำขอเพิกถอนทุกรายการ** ของรอบ | `requestRevokeAll` → `ENG-REVOKE-01` | HR · ผู้รับผิดชอบงาน IT · **เฉพาะรอบที่ `approved` ขึ้นไป** |
| **API-12** | `POST /access-items/:id/retry` | ส่งคำขอซ้ำสำหรับรายการที่ล้มเหลว/ไม่ตอบ (นับ `retry_count`) | `retryAccessRequest` | เดียวกับ API-11 |
| **API-13** | `POST /cases/:id/access-items` | เพิ่มรายการสิทธิ์ที่พบภายหลัง (**บังคับ `add_reason`**) | `addLateAccessItem` | HR · ผู้รับผิดชอบ |
| **API-14** | `POST /cases/:id/temp-access` | **ขอสิทธิ์ชั่วคราวให้ผู้รับมอบข้อมูล** (**บังคับผู้รับมอบ**) | `requestTempAccess` | HR · ผู้รับผิดชอบ |
| **API-15** | `POST /cases/:id/tasks` · `PATCH /tasks/:id` | เพิ่ม/ปิดงานเฉพาะรอบ (**บังคับ `change_reason`**) · สะท้อนสถานะจาก OP | `addCaseTask` · `updateCaseTask` → `ENG-OPSOW-01` | HR · หัวหน้า · ผู้รับผิดชอบ |
| **API-16** | `POST /tasks/:id/evidence` | แนบหลักฐานผ่าน Document Center (เก็บเฉพาะ `evidence_ref`) | `attachEvidence` | ผู้ปิดงาน |
| **API-17** | `PATCH /cases/:id/linkage` | ปรับสถานะการเชื่อมของ Module Linkage (สวัสดิการ · เงินเดือน · ทรัพย์สิน · สรรหา) | `setLinkage` | HR |
| **API-18** | `GET /templates` | รายการแม่แบบชุดงาน (อ่านจาก Operation Process) | `listTemplates` | ทุกบทบาทที่เห็นฟีเจอร์ |
| **API-19** | `POST /cases/:id/close` | **ปิดรอบ** — ตรวจ `closeBlockers` ครบก่อน · บันทึกธงจ้างกลับ | `closeCase` | HR |
| **API-21** | `GET /cases/:id/history` | ประวัติ append-only | `getCaseHistory` | ตามขอบเขต |
| **API-22** | `POST /cases/:id/assets` · `PATCH /assets/:id` | เพิ่ม/บันทึกส่งมอบ-คืนทรัพย์สิน (**คืนไม่ได้ ต้องมีเหตุผล**) | `upsertAssetItem` | HR · หัวหน้า · ธุรการ · พนักงาน |
| **API-23** | `PATCH /cases/:id/probation-review` | บันทึกผลการทบทวนทดลองงาน (ผ่าน/ไม่ผ่าน/ขยายเวลา) | `setProbationReview` | HR · หัวหน้า |
| **API-24** | `GET /watchlist` | รายการงานที่ต้องจับตา (รอบติดธง overdue · งานเลยกำหนด · คำขอที่ล้มเหลว) — **ขอบเขตเฉพาะรอบของฟีเจอร์นี้** | `getWatchlist` → `ENG-REVOKE-01` | ตามขอบเขต |

> **ไม่มี** `DELETE` ที่ endpoint ใดเลย (A-8) · **ไม่มี** endpoint แก้ `revocation_due_at` (AR-3) · **ไม่มี** endpoint ปิดรายการสิทธิ์โดยคน (AR-2)

---

## §2.2 Endpoint ภายในระบบ (ไม่ใช่ผู้ใช้เรียก)

| # | Method · Path | ผู้เรียก | ทำอะไร |
|---|---|---|---|
| **API-20** ⭐⭐ | `POST /access-items/:id/ack` | **Roles & Permissions (webhook)** | **รับผลตอบกลับของคำขอสิทธิ์** — เปิด/เพิกถอน/คืน · **ต้องมี `ack_by` · `ack_at` · `ack_ref` ครบ มิฉะนั้นปฏิเสธ 422** · idempotent ต่อ `request_id` |
| API-25 | `POST /internal/scan-revocation-due` | scheduler (ทุก 15 นาที) | ส่งคำขอเพิกถอนของรอบที่ถึงกำหนด · ประเมินธง overdue · ยิง event |
| API-26 | `POST /internal/advance-started-cases` | scheduler (รายวัน 00:05) | เปลี่ยนรอบเข้างานที่ถึงวันเริ่มงานเป็น "กำลังดำเนินการ" + เผยแพร่ `start_date` |
| API-27 | `POST /internal/reconcile-access-ack` | scheduler (ทุก 1 ชม.) | **ทางสำรองของ webhook** — ถาม Roles & Permissions ว่าคำขอที่ยังไม่มีผลตอบกลับมีสถานะอย่างไร (OQ-FRD-01) |
| API-28 | `POST /usage` | consumer (OB-6) | ลงทะเบียน where-used ว่าใครอ่านขอบเขตวันที่อยู่ |

### §2.2.1 ⭐ ทำไมไม่มี endpoint ที่เขียนข้อมูลสิทธิ์ — และไม่มีตารางสิทธิ์ที่ feature นี้เป็นเจ้าของ

**ข้อเท็จจริงเชิงสถาปัตยกรรม:**

1. **API-10 · API-11 · API-12 · API-13 · API-14 ไม่ได้ "เปิด" หรือ "ปิด" สิทธิ์ใด ๆ** — ทั้งห้าตัว **สร้างคำขอ (request)** แล้วส่งต่อไปยัง **Roles & Permissions / User Management** ซึ่งเป็นเจ้าของข้อมูลสิทธิ์จริง (#107) · สิ่งที่เขียนลงฐานข้อมูลของ feature นี้คือ **`request_id` · `requested_at` · `revoke_state = requested`** เท่านั้น
2. **API-20 ไม่ได้เขียนสิทธิ์เช่นกัน** — มันเขียน **หลักฐานว่าต้นทางทำแล้ว** (`ack_by` · `ack_at` · `ack_ref`) ลงในทะเบียนของรอบ · ตัวสิทธิ์จริงถูกเปลี่ยนที่ระบบต้นทางไปแล้วก่อนที่ผลตอบกลับจะมาถึง
3. ⭐ **`T_onb_access_item` ไม่ใช่ตารางสิทธิ์** — มันคือ **ทะเบียนหลักฐานของรอบ** (evidence register) ที่บันทึกว่า *"รอบนี้ขออะไรไป ต้นทางตอบว่าอย่างไร เมื่อไร โดยใคร"* · **ไม่มีที่ใดในฐานข้อมูลของ feature นี้ที่เก็บว่าใครมีสิทธิ์อะไรอยู่ในปัจจุบัน** — คำถามนั้นตอบได้ที่ Roles & Permissions เท่านั้น
4. **ผลที่ตามมาที่ต้องรู้:** ถ้าผู้ดูแลสิทธิ์ไปเพิกถอนที่ระบบต้นทางโดยไม่ผ่านคำขอของที่นี่ **ทะเบียนของรอบจะยังค้างอยู่จนกว่าจะมีผลตอบกลับ** — ซึ่งถูกต้องตามการออกแบบ เพราะ **สิ่งที่ feature นี้รับประกันคือ "มีหลักฐานว่าทำแล้ว" ไม่ใช่ "สิทธิ์ถูกปิดแล้ว"** · การกวาดหาความไม่ตรงกันเป็นของ **Policy Center** (NS-16 · OQ-STD-OB9)

> **สรุปสั้นสำหรับ dev:** ที่นี่มีแต่ **คำขอ** กับ **หลักฐาน** — **ไม่มีสิทธิ์** · ใครที่กำลังจะเขียน `UPDATE role...` ในโค้ดของ feature นี้ กำลังทำผิด **LOCK-NOWRITE** และ **#107**

---

## §2.3 Cross-Module Contract — Published Employment Window ⭐

| # | Method · Path | ผู้เรียก | รายละเอียด |
|---|---|---|---|
| **API-30** | `GET /employment-window/resolve` | **Attendance ✅ · Leave ✅ · Payroll ⏳ · Welfare ⏳ · ESS ⏳** | โครง query และ response เต็มที่ **`00_OVERVIEW §0.13.2`** · **`as_of` บังคับ** (ไม่ส่ง = `400 ERR_RESOLVE_DATE_REQUIRED`) |

**สัญญาที่ผูกกับ endpoint นี้ (ยกจาก `00_OVERVIEW §0.13.3`):**

| # | ข้อผูกพัน |
|---|---|
| OB-1 | ส่ง `as_of` เสมอ |
| OB-2 | เก็บ `case_ref` + `config_version_ids` คู่กับเอกสารของตัวเอง |
| OB-3 | ห้าม cache ข้ามวัน · ล้างเมื่อได้ `ofb_case_approved` · `ofb_case_cancelled` · `onb_start_date_changed` |
| **OB-4** ⭐ | **ห้ามตีความ `null` ว่า "ไม่มีวันสิ้นสุด"** — ใช้ `employment_state` เป็นตัวตัดสิน |
| **OB-5** ⭐ | **ห้ามเขียนกลับ** — **ไม่มี endpoint เขียนสำหรับ consumer เลย** |
| OB-6 | ลงทะเบียน where-used ที่ `POST /usage` (API-28) |

**สิ่งที่ endpoint นี้ **ไม่** คืน:** `termination_reason` · `is_immediate_exit` · ทะเบียนสิทธิ์รายรายการ · `probation_review_result` · `rehire_*` · งาน checklist รายใบ · **จำนวนเงินทุกชนิด**

### §2.3.1 Downstream Contract Matrix (R12)

| ปลายทาง | อ่าน field ไหน | ใช้ทำอะไร | ทดสอบข้ามระบบที่ |
|---|---|---|---|
| **Leave ✅** | `last_working_day` · `employment_state` | กัน/เตือนใบลาที่คร่อมวันพ้นสภาพ — **ปิด `OQ-L11`** | `06_TESTS XT-01` |
| **Attendance ✅** | `start_date` · `last_working_day` · `employment_state` | หยุดตั้งวันรอสแกนหลังพ้นสภาพ | `06_TESTS XT-02` |
| **Payroll ⏳** | `start_date` · `last_working_day` | ทำเครื่องหมายรอบจ่ายสุดท้าย (**ไม่มีตัวเลขเงินจากที่นี่**) | `06_TESTS XT-03` |
| **Welfare ⏳** | `signal.joiner` · `signal.leaver` | เริ่ม/สิ้นสุดสิทธิ์สวัสดิการ | `06_TESTS XT-04` |
| **Roles & Permissions ✅** | (ส่งเข้า) `POST /access-items/:id/ack` | ส่งผลตอบกลับพร้อมหลักฐาน | `06_TESTS XT-05` |
| **Operation Process ✅** | (ส่งออก) การประกาศ SOW | งานโผล่ใน "งานของฉัน" | `06_TESTS XT-06` |
| **ENG-CSQ · ENG-NOTIFY ✅** | (ส่งออก) event ตาม `00_OVERVIEW §0.16` | ผลกระทบและการแจ้งเตือน | `06_TESTS XT-07` |

---

## §2.4 API → Logic Trace (สรุป · ฉบับเต็มที่ `03_LOGIC §3.3`)

| API | Function หลัก | Engine ที่ถูกเรียก |
|---|---|---|
| API-03 | `createCase` | `ENG-WORKDAY-01` · `ENG-OPSOW-01` · `ENG-HRCFG-READ` · `ENG-ACCESSREG-01` |
| API-04 | `previewTasks` | `ENG-WORKDAY-01` · `ENG-HRCFG-READ` |
| API-05 | `updateCaseDates` | `ENG-WORKDAY-01` · `ENG-PERIOD-GUARD` |
| API-06 | `submitCase` | **`ENG-DOA-01`** · `ENG-PERIOD-GUARD` |
| API-07 | `approveCase` | **`ENG-DOA-01`** · `ENG-PERIOD-GUARD` · `ENG-REVOKE-01` (ตั้ง `revocation_due_at`) |
| API-08 | `rejectCase` | `ENG-DOA-01` |
| API-09 | `cancelCase` | **`ENG-REVOKE-01`** (ออกคำขอคืนสิทธิ์) · `ENG-OPSOW-01` (ปิดงานค้าง) |
| API-10 · API-11 · API-12 · API-13 · API-14 | `requestGrant` · `requestRevokeAll` · `retryAccessRequest` · `addLateAccessItem` · `requestTempAccess` | **`ENG-REVOKE-01`** |
| **API-20** ⭐ | `receiveAccessAck` | **`ENG-REVOKE-01`** (ปิดรายการ + ประเมินความครบ + ยิง SecC) |
| API-15 · API-16 | `addCaseTask` · `updateCaseTask` · `attachEvidence` | `ENG-OPSOW-01` |
| API-19 | `closeCase` | `ENG-REVOKE-01` (ตรวจความครบ) · `ENG-OPSOW-01` |
| API-24 | `getWatchlist` | `ENG-REVOKE-01` (`severity`) |
| API-25 · API-26 · API-27 | `scanRevocationDue` · `advanceStartedCases` · `reconcileAccessAck` | `ENG-REVOKE-01` · `ENG-WORKDAY-01` |
| API-30 | `resolveEmploymentWindow` | — (อ่านจาก read model ตรง) |

---

## §2.5 Error Response

```json
{ "error": { "code": "ERR_XXX", "message": "ข้อความภาษาไทยที่ผู้ใช้อ่านรู้เรื่อง",
             "details": { "field": "...", "hint": "..." } } }
```

| HTTP | code | เมื่อไร |
|---|---|---|
| 400 | `ERR_RESOLVE_DATE_REQUIRED` | เรียก read model โดยไม่ส่ง `as_of` |
| 400 | `ERR_REQUIRED_FIELD` | ช่องบังคับว่าง (VR-01…VR-06 · VR-14…VR-16) |
| 400 | `ERR_REASON_REQUIRED` | ยกเลิก/ไม่อนุมัติ/เพิ่มงาน/เพิ่มสิทธิ์ โดยไม่มีเหตุผล (VR-07…VR-10) |
| 409 | `ERR_PERIOD_CLOSED` | วันที่ตกในงวดที่ปิดแล้ว (พร้อม `earliest_allowed_date`) |
| 409 | `ERR_INVALID_TRANSITION` | เปลี่ยนสถานะที่ state machine ไม่อนุญาต |
| 409 | `ERR_NOT_CURRENT_APPROVER` | ผู้เรียกไม่ใช่ผู้ถือ slot ปัจจุบัน |
| 409 | `ERR_SOD_VIOLATION` | ผู้สร้างรอบ/ผู้ที่จะออก เป็นผู้ถือ slot |
| 409 | `ERR_CASE_NOT_APPROVED` | ส่งคำขอเพิกถอนก่อนรอบได้รับอนุมัติ (BR-DOA-07) |
| **409** | **`ERR_CLOSE_BLOCKED`** ⭐ | ปิดรอบทั้งที่ยังมีของค้าง — `details.blockers[]` **แยกเป็นรายบรรทัด** |
| **409** | **`ERR_REVOCATION_OVERDUE`** ⭐ | ปิดรอบทั้งที่ติดธง overdue |
| **422** | **`ERR_ACK_INCOMPLETE`** ⭐⭐ | **ผลตอบกลับที่ไม่มี `ack_by` / `ack_at` / `ack_ref` ครบ — ปฏิเสธ ไม่ปิดรายการ** |
| 422 | `ERR_ACK_UNKNOWN_REQUEST` | ผลตอบกลับอ้าง `request_id` ที่ไม่มีในระบบ |
| 422 | `ERR_TEMPLATE_INACTIVE` | เลือกแม่แบบที่ถูกปิดใช้ (BR-30) |
| 422 | `ERR_SOW_CREATE_FAILED` | Operation Process ไม่รับการประกาศ SOW — **รอบไม่ถูกสร้าง** (EN-01) |
| 422 | `ERR_EMPLOYEE_NOT_FOUND` | เลือกคนที่ไม่อยู่ในทะเบียนพนักงาน (FN-81) |
| 423 | `ERR_CASE_CLOSED` | แก้รอบที่ปิดแล้ว |
| 404 | `ERR_NOT_FOUND` | ทรัพยากรไม่มี **หรืออยู่นอกขอบเขตของผู้เรียก** (A-10) |
| 409 | `ERR_STALE_VERSION` | มีคนแก้รอบนี้ไปก่อน — ให้โหลดใหม่ (CA-01) |
| 429 | `ERR_RATE_LIMITED` | เกินเพดานของ read model หรือ endpoint รับผลตอบกลับ |
| 502 | `ERR_UPSTREAM_UNAVAILABLE` | ต้นทาง (HR Config · OP · Roles · DOA) ไม่ตอบ — **ห้ามถือว่าสำเร็จ** (S-29) |

> **ข้อสังเกต:** ไม่มี error code ใดที่เกี่ยวกับเงิน · ไม่มี code ที่เกี่ยวกับเลขที่เอกสาร · ไม่มี code ที่เกี่ยวกับการลบ
