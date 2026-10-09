# 02_API — F-HR-OT · OT / Shift (โอที)

> Audience: **BE dev (ชั้น HTTP เท่านั้น)**
> **กติกา:** ชั้นนี้ทำแค่ รับ/ตรวจรูปแบบ/เรียก Function หรือ Engine/แปลงผลลัพธ์ — **ตรรกะธุรกิจทั้งหมดอยู่ที่ `03_LOGIC`** (R8 · Logic Placement)
> **ห้ามมี `createX`/`updateX`/สูตรคำนวณ ซ่อนอยู่ในไฟล์นี้**

## §2.1 API Overview

| # | Method + Path | ทำอะไร | mutation | Function/Engine หลัก |
|---|---|---|---|---|
| API-01 | `POST /api/v1/ot/requests` | สร้างใบร่าง | ✅ | `createDraft` |
| API-02 | `PATCH /api/v1/ot/requests/{id}` | แก้ร่าง (หัวใบ) | ✅ | `updateDraft` · `validateHeader` |
| API-03 | `GET /api/v1/ot/employees/selectable` | รายชื่อผู้ขอที่เลือกได้ตาม scope | — | `resolveEmployeeScope` |
| API-04 | `PUT /api/v1/ot/requests/{id}/lines` | เพิ่ม/แก้/ลบบรรทัด + resolve ค่าทั้งชุด | ✅ | `addLine` · `updateLine` · `removeLine` · `resolveDayType` · `resolveOtRate` · `computeLineHours` · `checkLeaveConflict` · `checkOtOverlap` |
| API-05 | `GET /api/v1/ot/requests/{id}/precheck` | ผลตรวจก่อนส่ง (ขั้น 4) | — | `buildPreSubmitReport` · `resolveCap` · `computeOverCap` · `computeCapWarning` |
| API-06 | `POST /api/v1/ot/requests/{id}/submit` | **ส่งอนุมัติ** — ออกเลข · เลือก action · resolve+freeze สาย · snapshot version | ✅ | `submitRequest` |
| API-07 | `GET /api/v1/ot/requests/{id}` | อ่านใบเต็ม (ทุกแท็บ) | — | — (อ่าน) |
| API-08 | `POST /api/v1/ot/requests/{id}/approve` | อนุมัติขั้นปัจจุบัน | ✅ | `approveStep` |
| API-09 | `POST /api/v1/ot/requests/{id}/approve-partial` | อนุมัติบางส่วน | ✅ | `approvePartial` |
| API-10 | `POST /api/v1/ot/requests/{id}/reject` | ไม่อนุมัติ | ✅ | `rejectRequest` |
| API-11 | `POST /api/v1/ot/requests/{id}/cancel` | ยกเลิกใบที่รออนุมัติ | ✅ | `cancelRequest` |
| API-12 | `POST /api/v1/ot/requests/{id}/withdraw` | ขอถอน / อนุมัติการถอน | ✅ | `requestWithdrawal` · `finalizeWithdrawal` |
| API-13 | `POST /api/v1/ot/requests/{id}/confirm-hours` | **ยืนยันเวลาจริง** | ✅ | `confirmActualHours` |
| API-14 | `GET /api/v1/ot/confirm-queue` | คิวใบที่ถึงกำหนดยืนยัน + ใบติดธง | — | `buildConfirmQueue` |
| API-15 | `POST /api/v1/ot/requests/{id}/variance-ack` | รับทราบส่วนต่างเกินเวลาจริง | ✅ | `acknowledgeVariance` |
| API-16 | `POST /api/v1/ot/requests/{id}/resubmit` | แก้แล้วส่งใหม่ | ✅ | `resubmitRequest` |
| API-17 | *(inbound event)* `attendance.day_adjusted` | ตั้งธง "ต้องทวน" | ✅ | `onAttendanceDayAdjusted` |
| API-18 | `POST /api/v1/ot/requests/proxy-batch` | ยื่นแทนหลายคน → แตกเป็นใบต่อคน | ✅ | `splitProxyRequests` |
| API-19 | `POST /api/v1/ot/requests/{id}/consent` | ผู้ทำ OT กดรับทราบ | ✅ | `recordConsent` |
| **API-20** | `GET /api/v1/ot/resolve` | **read model `day`** (§0.13.2) | — | `buildDayReadModel` |
| **API-21** | `GET /api/v1/ot/periods/resolve` | **read model `period`** (§0.13.3) | — | `buildPeriodSummary` |
| API-22 | `GET /api/v1/ot/linkage` · `PATCH .../linkage/{key}` | สถานะการเชื่อมโมดูลปลายทาง + override ด้วยมือ | ✅ (patch) | `buildLinkageStatus` |
| API-23 | `POST /api/v1/ot/requests/{id}/attachments` | แนบเอกสาร | ✅ | `attachDocument` |
| API-24 | `POST /api/v1/ot/attachments/{aid}/archive` | ถอดเอกสาร (**เก็บถาวร ไม่ลบ**) | ✅ | `archiveAttachment` |
| API-25 | `POST /api/v1/ot/usage` | ลงทะเบียนผู้อ่าน read model (OT-7) | ✅ | — |
| API-26 | `POST /api/v1/ot/requests/{id}/review` | ตัดสินใบที่ติดธง "ต้องทวน" | ✅ | `adjustConfirmedHours` · `requestWithdrawal` |

**ไม่มี endpoint เหล่านี้ในแพ็ก (โดยเจตนา):**
- ❌ `DELETE` ใด ๆ — ไม่มีการลบถาวร (LOCK-AUDIT)
- ❌ endpoint ตั้งค่าอัตรา/ตัวคูณ/เพดาน/ปฏิทิน/กะ/งวด — เป็นของ HR Configuration (LOCK-CFG)
- ❌ endpoint เขียนกลับไป Attendance / Leave / HR Config (LOCK-ATT · LOCK-LEAVE)
- ❌ **endpoint เขียนสำหรับ consumer** — Payroll/ESS/Roster อ่านอย่างเดียว (§0.13.5)
- ❌ endpoint คำนวณเงินหรือคืนจำนวนเงิน (LOCK-MONEY)

## §2.2 Per-API Contract (ย่อเฉพาะที่มีสัญญาเฉพาะตัว)

### API-04 · `PUT /api/v1/ot/requests/{id}/lines`
```
Request:
{ "lines": [ { "line_no":1, "work_date":"2026-09-14", "time_from":"18:00",
               "time_to":"21:00", "break_hours":0, "line_note":null } ] }

Response 200:
{ "lines":[ { "line_no":1, "work_date":"2026-09-14", "time_from":"18:00", "time_to":"21:00",
    "is_overnight":false, "hours_requested":3.00,
    "day_type":"workday", "rate_type":"ot_workday", "multiplier":1.50,
    "payroll_code":"OT01", "ot_rate_version_id":"HRCFG-OT-2026-007",
    "attendance_outside_hours":3.00, "attendance_day_status":"confirmed",
    "attendance_version_id":"ATT-2026-09-14-002", "variance_hours":0.00,
    "leave_conflict_ref":null, "ot_conflict_ref":null,
    "flags":[] } ],
  "totals": { "hours_requested_total": 3.00 } }
```
- **`hours_requested` เป็น output เท่านั้น — ถ้า client ส่งมาให้ 400 `ERR_OT_HOURS_READONLY`** (FN-06 · ผู้ใช้ไม่พิมพ์ตัวเลขชั่วโมง)
- `day_type` · `rate_type` · `multiplier` · `payroll_code` เป็น output ทั้งหมด — **client ส่งมาไม่ได้** (BR-06 · BR-01)

### API-05 · `GET /api/v1/ot/requests/{id}/precheck`
```
Response 200:
{ "week_of":"2026-09-14", "hours_accumulated":34.00,
  "cap_hours_week":36.00, "cap_source":"HRCFG-OT-2026-007", "hours_remaining":2.00,
  "cap_warning":true, "over_cap":false,
  "cap_hours_day":null,     // FN-58 — ยังไม่มีค่าให้อ่าน (OQ-STD-OT5)
  "cap_hours_month":null,   // FN-58
  "variance":[ {"line_no":1,"requested":3.00,"outside":2.50,"diff":0.50,"class":"over"} ],
  "leave_conflicts":[], "ot_overlaps":[],
  "period":{"code":"2026-09","status":"open"},
  "retro":{"is_retro":false,"days_late":0,"late_flag":false},
  "predicted_chain":{"action_id":"ot_approve_within_cap","steps":2},
  "blocks":[ {"code":"ERR_OT_VARIANCE_OVER","line_no":1,"message":"ชั่วโมงที่ขอมากกว่าเวลาจริงนอกกะ 0.50 ชม."} ] }
```
- **`cap_hours_day` / `cap_hours_month` เป็น `null` เสมอในรอบนี้** — client แสดง "ยังไม่มีค่าให้อ่าน" · **ห้ามใส่ตัวเลขแทน `null`**
- `predicted_chain` เป็น **การคาดการณ์เพื่อแสดงบนจอเท่านั้น** — สายจริง resolve ที่ API-06

### API-06 · `POST /api/v1/ot/requests/{id}/submit` ⭐
```
Headers: Idempotency-Key: <uuid>            ← บังคับ (PR-3)
Request:
{ "row_version": 3,
  "slots": [ {"step_no":1,"assignee_id":"<uuid>"}, {"step_no":2,"assignee_id":"<uuid>"} ] }

Response 201:
{ "ot_no":"OT-2026-0001", "status":"pending_approval",
  "approval_action_id":"ot_approve_within_cap",
  "doa_entry_ref":"DOA-HROT-01",
  "approval_chain":[ {"step_no":1,"slot_role":"role-supervisor-direct","assignee_id":"…","assignee_snapshot":{…}},
                     {"step_no":2,"slot_role":"role-mgr-hr","assignee_id":"…","assignee_snapshot":{…}} ],
  "over_cap": false, "cap_snapshot_hours_week": 36.00,
  "config_version_ids": { "ot_rate":"HRCFG-OT-2026-007", "holiday":"…", "shift":"…",
                          "period":"…", "attendance_day":["ATT-2026-09-14-002"] },
  "submitted_at":"2026-09-10T09:14:22+07:00", "row_version": 4 }
```
**ลำดับที่ห้ามสลับ (บังคับใน `03_LOGIC §3.1 submitRequest`):**
1. validate ทุกด่าน (รวม **ตรวจงวดซ้ำ ณ วินาทีนี้**)
2. `resolveCap(work_date)` → `computeOverCap()` → **`selectApprovalAction()`**
3. `GET /doa/resolve` ด้วย **action id ที่เลือกได้** → ตรวจว่าจำนวน slot ที่ client ส่งมา = จำนวน step ที่ engine คืน
4. `issueDocNumber()` — **หลังจาก resolve สายสำเร็จเท่านั้น** (ถ้าสายล้ม เลขต้องไม่ถูกกิน)
5. `snapshotConfigVersions()` + เก็บ `cap_snapshot_hours_week`
6. `freezeApprovalChain()` → เขียน `T_ot_approval_trace` ทุก step
7. `appendHistory()` → `emitNotification('ot_submitted')` (+ `ot_cap_exceeded` เมื่อ `over_cap`)

> **ห้าม** ออกเลขก่อน resolve สาย · **ห้าม** ส่งจำนวน slot จาก client ไปกำหนดจำนวนขั้น (client เป็นแค่ผู้เลือกคน)

### API-08 · `POST /api/v1/ot/requests/{id}/approve`
```
Headers: Idempotency-Key: <uuid>
Request:  { "row_version": 4, "note": null }
Response: { "status":"pending_approval"|"approved", "current_step":2|null,
            "approved_at":null|"…", "pdf_stored":false|true, "row_version": 5 }
```
- **ตรวจซ้ำก่อน commit:** เจ้าของ slot · SoD · งวดยังเปิด · ไม่ทับวันลา · ไม่ทับใบอื่น · **`cap_snapshot_hours_week` ยังเท่าเดิม**
- ถ้าเป็น **ขั้นสุดท้าย** → `renderOtPdf()` + `storeApprovedCopy()` + `emitImpactEvent('ot.approved')` + `emitNotification('ot_decided')`

### API-13 · `POST /api/v1/ot/requests/{id}/confirm-hours` ⭐
```
Headers: Idempotency-Key: <uuid>
Request:  { "row_version": 5,
            "lines": [ {"line_no":1,"hours_confirmed":3.00} ] }
Response: { "status":"time_confirmed", "hours_confirmed_total":3.00,
            "published": true, "row_version": 6 }
```
- **Guard:** `status = approved` · `work_date < today` · `attendance_day_status ∈ {confirmed, locked}` · **`attendance_version_id` ต้องตรงกับตอนเปิดหน้า** (CA-05) · งวดยังเปิด
- `hours_confirmed ≤ hours_approved` **และ** `≤ attendance_outside_hours` (BR-21)
- หลังสำเร็จ → **ใบเริ่มปรากฏใน API-20 / API-21 ทันที** (SLA-06) + `emitImpactEvent('ot.time_confirmed')`

### API-20 · `GET /api/v1/ot/resolve` — read model `day`
สัญญาเต็มอยู่ที่ **`00_OVERVIEW §0.13.2`** (ห้ามเขียนซ้ำสองที่)
- **คืนเฉพาะ `ot_status ∈ {time_confirmed, withdrawn}`** — ใบ `approved` ที่ยังไม่ยืนยัน **ไม่ถูกคืน** (BR-17 · IA-01)
- `date` บังคับ (400 `ERR_RESOLVE_DATE_REQUIRED`) · ช่วงสูงสุด 62 วัน · `page_size` ≤ 500

### API-21 · `GET /api/v1/ot/periods/resolve` — read model `period`
สัญญาเต็มอยู่ที่ **`00_OVERVIEW §0.13.3`**
- **ต้องคืน `period_status` · `pending_docs` · `unconfirmed_hours` · `needs_review_docs` เสมอ** — เป็นสัญญาณให้ Payroll รู้ว่ายอดนิ่งหรือยัง
- **ไม่มีช่องใดเป็นจำนวนเงิน** (IA-07)

### API-25 · `POST /api/v1/ot/usage` (where-used ขาออก)
```
Request: { "consumer_feature_code":"F-HR-PAYROLL", "views_used":["day","period"], "contact":"…" }
```
> **นี่คือ endpoint เขียนตัวเดียวที่ consumer เรียกได้** — และมันไม่ได้เขียนข้อมูล OT (§0.13.5)

## §2.3 Common Concerns

| หัวข้อ | กติกา |
|---|---|
| **Auth** | Bearer token ของแพลตฟอร์ม · `tenant_id` + `company_id` + `scope` มาจาก token **ไม่ใช่จาก body** |
| **Idempotency** | `Idempotency-Key` **บังคับ** ที่ API-06 · 08 · 09 · 10 · 11 · 12 · 13 · 16 · 18 (PR-3 · VR-21) |
| **Optimistic lock** | ทุก mutation ต้องส่ง `row_version` · ไม่ตรง → **409 `ERR_OT_STALE`** (PR-1) |
| **การส่ง date ไปต้นทาง** | **`date` = `work_date` เสมอ ห้ามใช้ `now()`** (C-1 · AT-1 · LV-1 · BR-02) |
| **Upstream ล่ม** | **503 `ERR_UPSTREAM_UNAVAILABLE` + บล็อก** — ห้าม fallback ห้ามใช้ cache ข้ามวัน (BR-04 · DI-01) |
| **Pagination** | `page` (1-based) · `page_size` default 100 · สูงสุด 500 |
| **Timezone** | เขตเวลาเดียวของผู้เช่า · timestamp เป็น `timestamptz` (LD-OT-09) |
| **Error format** | `{ "error": { "code":"UPPER_SNAKE", "message":"ไทย", "line_no":N?, "ref":"…"? } }` |
| **ไม่มีช่องเงิน** | ทุก response ผ่านตัวตรวจอัตโนมัติที่ปฏิเสธ key ที่มีคำว่า `amount`/`price`/`total_baht`/`currency` (IA-07) |

## §2.4 API → Logic Trace (Anchor for R8)

| API | mutation? | Function / Engine ที่ถูกเรียก |
|---|:---:|---|
| API-01 | ✅ | `createDraft` · `appendHistory` |
| API-02 | ✅ | `updateDraft` · `validateHeader` · `inferRequestMode` · `checkRetroCutoff` · `appendHistory` |
| API-03 | — | `resolveEmployeeScope` |
| API-04 | ✅ | `addLine` · `updateLine` · `removeLine` · `computeLineHours` · `detectOvernight` · `resolveDayType` · `mapRateType` · `resolveOtRate` · `fetchAttendanceDay` · `computeVariance` · `classifyVariance` · `checkLeaveConflict` · `checkOtOverlap` · `validateLines` · **ENG-HRCFG-RESOLVE · ENG-ATT-RESOLVE · ENG-LEAVE-RESOLVE · ENG-OVERLAP · ENG-VARIANCE** |
| API-05 | — | `buildPreSubmitReport` · `resolveCap` · `computeWeeklyAccumulated` · `computeOverCap` · `computeCapWarning` · `checkPeriodOpen` · `checkRetroCutoff` · **ENG-OTCAP** |
| API-06 | ✅ | `submitRequest` → `validateHeader` · `validateLines` · `checkPeriodOpen` · `resolveCap` · `computeOverCap` · **`selectApprovalAction`** · `resolveApprovalChain` · `issueDocNumber` · `snapshotConfigVersions` · `freezeApprovalChain` · `appendApprovalTrace` · `appendHistory` · `emitNotification` · **ENG-DOA-01 · ENG-DOC-NUM · ENG-NOTIFY** |
| API-07 | — | `buildSignatureSlots` (สำหรับแท็บลายเซ็น/PDF) |
| API-08 | ✅ | `approveStep` · `checkPeriodOpen` · `checkLeaveConflict` · `checkOtOverlap` · `renderOtPdf` · `storeApprovedCopy` · `appendApprovalTrace` · `appendHistory` · `emitNotification` · `emitImpactEvent` · **ENG-DOC-STORE · ENG-CSQ** |
| API-09 | ✅ | `approvePartial` · `appendHistory` · `emitNotification` · `emitImpactEvent` |
| API-10 | ✅ | `rejectRequest` · `appendHistory` · `emitNotification` · `emitImpactEvent` |
| API-11 | ✅ | `cancelRequest` · `appendHistory` · `emitNotification` |
| API-12 | ✅ | `requestWithdrawal` · `finalizeWithdrawal` · `resolveApprovalChain` · `appendHistory` · `emitNotification` · `emitImpactEvent` |
| API-13 | ✅ | `confirmActualHours` · `fetchAttendanceDay` · `checkPeriodOpen` · `buildDayReadModel` (refresh) · `appendHistory` · `emitImpactEvent` |
| API-14 | — | `buildConfirmQueue` · `resolveNeedsReview` |
| API-15 | ✅ | `acknowledgeVariance` · `appendHistory` |
| API-16 | ✅ | `resubmitRequest` → `selectApprovalAction` · `resolveApprovalChain` · `freezeApprovalChain` · `appendHistory` |
| API-17 | ✅ | `onAttendanceDayAdjusted` · `resolveNeedsReview` · `appendHistory` · `emitNotification` |
| API-18 | ✅ | `splitProxyRequests` · `createDraft` (ต่อคน) · `appendHistory` |
| API-19 | ✅ | `recordConsent` · `appendHistory` |
| API-20 | — | `buildDayReadModel` |
| API-21 | — | `buildPeriodSummary` · `freezePeriodSummary` · **ENG-PERIOD-FREEZE** |
| API-22 | ✅ | `buildLinkageStatus` |
| API-23 | ✅ | `attachDocument` · `appendHistory` |
| API-24 | ✅ | `archiveAttachment` · `appendHistory` |
| API-25 | ✅ | `registerWhereUsed` |
| API-26 | ✅ | `adjustConfirmedHours` · `requestWithdrawal` · `appendHistory` · `emitImpactEvent` |

**ตรวจ R8:** ทุก mutation API มี ≥ 1 Function/Engine ✅ · ไม่มี Function ใน `03_LOGIC §3.1` ที่ไม่ถูก trace ✅ (ดูตารางเต็มที่ `03_LOGIC §3.3`)

## §2.X Cross-Module Contract ⭐ (จาก BRD §12.1 Downstream Impact Map)

| ปลายทาง | สัญญาที่ feature นี้ให้ | ทิศทาง | หมายเหตุ |
|---|---|---|---|
| **Payroll (⏳W4)** | `GET /api/v1/ot/resolve` · `GET /api/v1/ot/periods/resolve` (§0.13) | **ขาออก อ่านอย่างเดียว** | **ไม่มี write endpoint** · Payroll คูณเป็นเงินเอง |
| **ESS Portal (⏳W6)** | เรียกหน้าจอ `#/ot/list` ของ feature นี้ + `GET /api/v1/ot/resolve` (scope=own) | ขาออก | ไม่ทำ CRUD ซ้ำ (OQ-HR-04) |
| **Shift & Roster (⏳lane C)** | `GET /api/v1/ot/resolve` (วันที่มีใบอนุมัติ/ยืนยันแล้ว) + `GET /api/v1/ot/linkage` | ขาออก | soft ref · display-only |
| **ชั้นรายงาน 7C** | 5 event `ot.*` (§0.16.2) | ขาออก (event) | ENG-CSQ-02 เป็นผู้ตีมูลค่า |
| **Attendance** | *(ไม่มีสัญญาขาออก)* — **ห้ามเขียนกลับ** | — | AT-5 · `F-HR-ATTEND §0.13.5` |
| **Leave** | *(ไม่มีสัญญาขาออก)* — **ห้ามเขียนกลับ** | — | LV-5 |
| **HR Configuration** | `POST /hr-config/items/{id}/usage` (ลงทะเบียนผู้อ่าน) | ขาเข้าเชิงทะเบียน | C-6 |
| **ทั้ง 3 ต้นทาง** | ฟัง event: `hrconfig.effective` · `hrconfig.period_closed` · `attendance.day_confirmed` · **`attendance.day_adjusted`** · `attendance.period_summary_closed` · `leave.approved` · `leave.withdrawn` | ขาเข้า | ล้าง cache (BR-04) · `attendance.day_adjusted` → ตั้งธง (BR-22) |
