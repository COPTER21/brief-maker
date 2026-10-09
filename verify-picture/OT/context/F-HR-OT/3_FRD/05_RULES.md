# 05_RULES — F-HR-OT · OT / Shift (โอที)

> Audience: **BE dev + QA**
> ทุก BR ยกมาจาก BRD §9.1 ครบ 30 ข้อ · ทุก VR จาก BRD §9.2 ครบ 22 ข้อ · ทุก Edge Case จาก BRD §10 ครบ 52 ข้อ

## §5.1 Business Rules (BR)

| BR | กติกา | บังคับที่ไหน (Function/DB) | Error code | Test |
|---|---|---|---|---|
| **BR-01** | อัตรา · ตัวคูณ · เพดาน · ประเภทวัน · งวด ทุกตัว resolve จาก HR Configuration **ณ `work_date`** — ห้ามมีค่าคงที่ในโค้ด/หน้าจอ | `resolveOtRate` · `resolveCap` · `resolveDayType` · **ENG-HRCFG-RESOLVE** | `ERR_UPSTREAM_UNAVAILABLE` | AT-10 · **IA-03** |
| **BR-02** | ทุกการ resolve ส่ง **`date` = `work_date`** + `company_id` เสมอ (ไม่ใช่ `now()`) | ทุกฟังก์ชันกลุ่ม C · `02_API §2.3` | `ERR_RESOLVE_DATE_REQUIRED` | AT-10 |
| **BR-03** | เก็บ `config_version_ids` ทั้งก้อนตั้งแต่ submit — ใบเก่าอ่านค่าเดิมได้ตลอดไป | `snapshotConfigVersions` · `T_ot_request.config_version_ids` **NOT NULL เมื่อ status ≥ pending** | `ERR_OT_VERSION_MISSING` | AT-11 |
| **BR-04** | **ห้าม cache ข้ามวัน** — ล้างเมื่อได้ 7 event: `hrconfig.effective` · `hrconfig.period_closed` · `attendance.day_confirmed` · `attendance.day_adjusted` · `attendance.period_summary_closed` · `leave.approved` · `leave.withdrawn` | `invalidateResolveCache` | — | AT-57 |
| **BR-05** | **ห้าม CRUD / ห้ามเขียนกลับ** HR Config · Attendance · Leave ทุกกรณี — มีแค่ลิงก์ไปหน้าต้นทาง | **ไม่มี write path ใน `02_API`** | — | **IA-02** |
| **BR-06** | **ห้ามคำนวณเอง**: ชั่วโมงในกรอบกะ · สาย · ขาด · จำนวนวันลา · ประเภทวัน | `resolveDayType` · `fetchAttendanceDay` · `checkLeaveConflict` | — | AT-13 |
| **BR-07** ⭐ | **`outside_shift_hours` = ข้อมูลดิบ ไม่ใช่ OT ที่อนุมัติ** — ห้ามส่งให้ปลายทางตรง ต้องผ่านใบจนถึง `time_confirmed` | `buildDayReadModel` (กรองสถานะ) | — | **IA-01** |
| **BR-08** | **ตรวจ `day_status` ก่อนใช้ตัวเลขเสมอ** — `exception` ≠ "ทำงาน 0 ชั่วโมง" · ไม่มีข้อมูล = ห้ามใช้ค่าวันใกล้เคียง | `fetchAttendanceDay` คืน `null` + `exception_type` | `ERR_OT_ATT_NOT_READY` | AT-22 · AT-23 |
| **BR-09** ⭐ | เพดานจาก `ot_rate.cap_hours_week` ณ `work_date` · สะสมเกิน → `over_cap = true` → **สายยาวขึ้น** · **ค่าเพดานกับจุดตัดห้ามเขียนตายทั้งในโค้ดและใน matrix ของ DOA** | `resolveCap` → `computeOverCap` → `selectApprovalAction` (**§3.0.2**) | `ERR_OT_CAP_CHANGED` | AT-15 · AT-27 · **IA-05** |
| **BR-10** ⭐ | **สายอนุมัติจาก `GET /doa/resolve` เท่านั้น** — freeze ตอน submit · แก้ทะเบียนทีหลังไม่กระทบใบที่ส่งไปแล้ว · **hardcode = Hard Stop** | `resolveApprovalChain` · `freezeApprovalChain` | `ERR_OT_CHAIN_UNAVAILABLE` | AT-24 · **IA-04** |
| **BR-11** | **resubmit → ยกเลิกงานเดิม แล้ว resolve ใหม่ทั้งสาย · จำนวนขั้นเปลี่ยนได้ · เลขเดิมคงอยู่** | `resubmitRequest` (**§3.0.3 C-1**) | — | AT-32 |
| **BR-12** | **ไม่อนุมัติ · ถอน · อนุมัติบางส่วน = บังคับเหตุผล** (การยกเลิกไม่บังคับ) | `rejectRequest` · `requestWithdrawal` · `approvePartial` | `ERR_OT_REASON_REQUIRED` | AT-29 · AT-30 · AT-40 |
| **BR-13** | **เลขออกตอน submit (ไม่ใช่ตอนร่าง) · immutable · ไม่ reuse** | `issueDocNumber` · `UNIQUE(tenant_id, ot_no)` | `ERR_OT_NO_IMMUTABLE` | AT-33 · AT-34 |
| **BR-14** | **history append-only · ไม่มี hard delete** | trigger ปฏิเสธ UPDATE/DELETE บน `T_ot_history` · `T_ot_approval_trace` | `ERR_OT_APPEND_ONLY` | AT-50 · **IA-09** |
| **BR-15** | **งวดปิด = ปฏิเสธการยื่น/อนุมัติ/ยืนยัน/ถอน** · **ไม่มี retro** · **ตรวจซ้ำ ณ วินาที commit** | `checkPeriodOpen` (เรียกสองจุด) | `ERR_OT_PERIOD_CLOSED` | AT-39 · **IA-06** |
| **BR-16** | ขอ **มากกว่า** เวลาจริง = **บล็อก** จนแก้/ผู้อนุมัติรับทราบพร้อมเหตุผล · ขอ **น้อยกว่า** = ผ่าน + ธง | `classifyVariance` · `acknowledgeVariance` (**§3.0.4**) | `ERR_OT_VARIANCE_OVER` | AT-18 · AT-19 |
| **BR-17** ⭐ | **เฉพาะใบ `time_confirmed` เท่านั้นที่เข้าสรุปงวดกับถูกเผยแพร่** — ใบ `approved` ยังไม่นับ | `buildDayReadModel` · `buildPeriodSummary` | — | **IA-01** |
| **BR-18** ⭐ | **ห้ามมีตัวเลขเงินในทุกหน้าจอ ทุก payload ทุกไฟล์** — ตัวคูณเป็นค่าอ้างอิง ห้ามใช้เป็นสูตรคูณเงิน | `assertNoMoneyField` (guard ทุก response/event) · `04_DB` (ไม่มีคอลัมน์เงิน) | `ERR_OT_MONEY_FIELD` | **IA-07** |
| **BR-19** | **ขอ OT ทับวันลาที่อนุมัติแล้ว = บล็อก** + ลิงก์ไปใบลา | `checkLeaveConflict` (ตรวจตอนกรอก + ตอน submit + ตอน approve) | `ERR_OT_LEAVE_CONFLICT` | AT-16 |
| **BR-20** | **`no_shift` / ตัดสิน day_type ไม่ได้ / ช่วงเวลาไม่ถูกต้อง = บล็อก** — ห้ามเดาว่าเป็นวันทำงานปกติ | `resolveDayType` · `validateLines` | `ERR_OT_DAYTYPE_UNRESOLVED` · `ERR_OT_TIME_RANGE` | AT-07 · AT-09 |
| **BR-21** | **อนุมัติบางส่วน:** `hours_approved ≤ hours_requested` **และ** `≤ attendance_outside_hours` (เมื่อมีค่า) · บังคับเหตุผล | `approvePartial` · `confirmActualHours` | `ERR_OT_HOURS_EXCEED` | AT-30 |
| **BR-22** | ได้ `attendance.day_adjusted` → **ใบติดธง "ต้องทวน" ทันที** · **ห้ามแก้ตัวเลขในใบเงียบ ๆ** | `onAttendanceDayAdjusted` (**§3.0.4 ท้าย**) | — | AT-42 |
| **BR-23** | ค่าที่ `inactive` เลือกใหม่ไม่ได้ แต่ **ใบเก่ายังแสดงและพิมพ์ได้** | `resolveOtRate` (กรอง `active` เฉพาะตอนเลือกใหม่) · `renderOtPdf` ใช้ snapshot | `ERR_OT_RATE_INACTIVE` | AT-12 |
| **BR-24** | **SoD:** ผู้ขอเซ็นใบตัวเองไม่ได้ — ชนกันเมื่อไร **DOA ต้อง escalate ขึ้นสายบังคับบัญชาเหนือขึ้นไป** (feature ไม่แก้เอง) | `approveStep` ตรวจ `actor ≠ requested_by ∧ actor ≠ employee_id` | `ERR_OT_SOD_VIOLATION` | AT-26 |
| **BR-25** | **ลงทะเบียน where-used ทั้ง 3 ต้นทาง** เมื่อ feature พร้อมใช้ | `registerWhereUsed` (M-5) | — | AT-58 |
| **BR-26** | **1 ใบ = 1 คน** — ยื่นแทนหลายคนแตกเป็นใบต่อคน | `splitProxyRequests` · โครงตาราง (ไม่มีตารางผู้ขอหลายคน) | — | AT-43 |
| **BR-27** | **การถอน = event ใหม่ที่ชี้ของเดิม** — ใบเดิม ประวัติเดิม สำเนา PDF เดิมไม่ถูกลบไม่ถูกแก้ | `finalizeWithdrawal` (`reversal_of`) | — | AT-41 |
| **BR-28** | **ยื่นแทน → ต้องมี consent ก่อน submit** | `validateHeader` · `recordConsent` | `ERR_OT_CONSENT_REQUIRED` | AT-43 |
| **BR-29** | **ห้ามทับซ้อนกับใบ OT อื่นของคนเดียวกันที่ยังไม่ปิด** — ตรวจตอนกรอก · ตอน submit · ตอน approve | `checkOtOverlap` · **`EXCLUDE` constraint ที่ฐานข้อมูล** (D-01) | `ERR_OT_OVERLAP` | AT-52 |
| **BR-30** | **การปัดเศษ/หน่วยขั้นต่ำต้องอ่านจาก HR Config** — ยังไม่เผยแพร่ → **ใช้ค่าดิบไม่ปัด · ห้ามใส่ตัวเลขนาทีในโค้ด** | `computeLineHours` (`rounding = null`) | — | AT-53 · **IA-10** |

## §5.2 State Machine

**7 สถานะ:** `draft` · `pending_approval` · `approved` · **`time_confirmed`** · `rejected` · `cancelled` · `withdrawn`
**2 ธง (ไม่ใช่สถานะ):** `period_locked` (เจ้าของ = HR Configuration) · `needs_review` (จาก `attendance.day_adjusted`)

| T | จาก → ไป | ใครกด | Guard | ผลข้างเคียง |
|---|---|---|---|---|
| T-1 | — → `draft` | ผู้ขอ / หัวหน้า | — | ไม่ออกเลข · ไม่ resolve สาย |
| T-2 | `draft` → `pending_approval` | ผู้ขอ | ผ่าน BR-20 · BR-19 · BR-29 · BR-15 · BR-16 · BR-28 ครบ | **ออกเลข** · คำนวณ `over_cap` · **เลือก action** · resolve+freeze สาย · snapshot version + cap · ยิง `ot_submitted` (+ `ot_cap_exceeded`) |
| T-3 | `pending_approval` → `pending_approval` (ขั้นถัดไป) | ผู้ถือ slot | เจ้าของ slot · SoD (BR-24) · **ตรวจซ้ำ §3.0.3** | เดินสาย · เขียน trace |
| T-4 | `pending_approval` → `approved` | ผู้ถือ slot สุดท้าย | เหมือน T-3 + งวดยังเปิด | ตั้ง `hours_approved_total` · **สร้าง PDF + เก็บสำเนา** · `ot_decided` · **`ot.approved` (FC)** |
| T-5 | `pending_approval` → `rejected` | ผู้ถือ slot ใดก็ได้ | **เหตุผลบังคับ** | เลขคงอยู่ · `ot_decided` · **`ot.rejected` (FC avoided)** |
| T-6 | `pending_approval` → `cancelled` | ผู้ขอ | ใบยังไม่อนุมัติ | ปิดงานที่ค้าง · `ot_cancelled` · **ไม่ยิง 7C** |
| T-7 | `pending_approval` → `pending_approval` (resubmit) | ผู้ขอ | ใบยังไม่อนุมัติ หรือถูกตีกลับ | **ยกเลิกงานเดิม → re-resolve (ขั้นเปลี่ยนได้) → freeze ใหม่** · เลขเดิม |
| T-8 ⭐ | `approved` → `time_confirmed` | หัวหน้า/HR (หรืออัตโนมัติเมื่อเป็น retro ที่วันนั้นยืนยันแล้ว) | `work_date < today` · `day_status ∈ {confirmed, locked}` · `attendance_version_id` ตรงกับตอนเปิดหน้า · BR-21 · งวดเปิด | ตั้ง `hours_confirmed_total` · **เริ่มเผยแพร่** · **`ot.time_confirmed` (EC + FC)** |
| T-9 | `approved` / `time_confirmed` → `withdrawn` | ผู้ขอ/หัวหน้า → **ผ่านสายอีกครั้ง** | **เหตุผลบังคับ** · งวดยังเปิด | **รายการกลับที่ชี้ของเดิม** · `ot_withdrawn` · **`ot.withdrawn`** |
| T-10 | *(ธง)* ใด ๆ → `period_locked` | ระบบ (สัญญาณจาก HR Config) | — | ปฏิเสธทุก transition ที่กระทบงวดนั้น |
| T-11 | *(ธง)* `approved`/`time_confirmed` → `needs_review` | ระบบ (`attendance.day_adjusted`) | — | ตั้งธง + แจ้ง HR · รอคนตัดสิน (`adjustConfirmedHours` หรือ `requestWithdrawal`) |

**Transition ที่ไม่มี (โดยเจตนา):**
- ❌ `withdrawn` / `rejected` / `cancelled` → กลับไปสถานะอื่น — **ยื่นใบใหม่เท่านั้น** (PR-E · LOCK-AUDIT)
- ❌ `time_confirmed` → `approved` — ย้อนกลับไม่ได้ · ถ้าต้องแก้ให้ถอนแล้วยื่นใหม่
- ❌ transition ใดที่ข้าม slot — สายเดินทีละขั้นเสมอ

## §5.3 Permission Matrix

| Action | พนักงาน | หัวหน้า | HR | ผู้บริหาร | เงื่อนไขเพิ่ม |
|---|:---:|:---:|:---:|:---:|---|
| สร้าง/แก้ร่างของตัวเอง | ✅ | ✅ | ✅ | ✅ | — |
| สร้างใบแทนลูกทีม | ❌ | ✅ | ✅ | ❌ | แตกเป็นใบต่อคน |
| ส่งอนุมัติ | ✅ | ✅ | ✅ | ✅ | เฉพาะใบที่ตัวเองเป็นผู้ยื่น |
| กด consent | ✅ | ❌ | ❌ | ❌ | **เฉพาะผู้ทำ OT ของใบนั้น** |
| อนุมัติ / ไม่อนุมัติ / บางส่วน | ❌ | ✅ | ✅ | ✅ | **เฉพาะผู้ถือ slot ปัจจุบัน** + SoD |
| ยกเลิก | ✅ | ✅ | ✅ | ❌ | ใบยังไม่อนุมัติ |
| ขอถอน | ✅ | ✅ | ✅ | ❌ | ใบอนุมัติ/ยืนยันแล้ว · งวดยังเปิด |
| ยืนยันเวลาจริง | ❌ | ✅ | ✅ | ❌ | `[ASSUMED A-5]` |
| ตัดสินใบติดธง | ❌ | ✅ | ✅ | ❌ | — |
| ดูสรุปงวด | ✅ own | ✅ team | ✅ company | ✅ ตามขอบเขต | — |
| **แก้ค่านโยบาย / แก้เวลาเข้างาน / ลบข้อมูล** | ❌ | ❌ | ❌ | ❌ | **ไม่มี endpoint** |

**ที่มาของ scope:** token เท่านั้น — **ไม่มี persona switch ในหน้าจอ** (#105 · FN-60)

## §5.4 Field Validation Rules

| VR | Field / Action | เงื่อนไข | ประเภท | Error code |
|---|---|---|---|---|
| VR-01 | ผู้ขอ | ต้องเลือกคน + อยู่ใน scope | Error | `ERR_OT_EMPLOYEE_REQUIRED` |
| VR-02 | `reason` | ห้ามว่างตั้งแต่ submit | Error | `ERR_OT_REASON_REQUIRED` |
| VR-03 | `work_done` | ห้ามว่างตั้งแต่ submit | Error | `ERR_OT_WORKDONE_REQUIRED` |
| VR-04 | ช่วงเวลา | ต้องได้ชั่วโมง > 0 | Error | `ERR_OT_TIME_RANGE` |
| VR-05 | บรรทัดในใบเดียว | ห้ามทับกันเอง | Error | `ERR_OT_LINE_OVERLAP` |
| VR-06 | บรรทัดข้ามใบ | ห้ามทับกับใบอื่นของคนเดียวกันที่ยังไม่ปิด | Error | `ERR_OT_OVERLAP` |
| VR-07 | `day_type` | ต้องตัดสินได้จากต้นทาง | Prevent | `ERR_OT_DAYTYPE_UNRESOLVED` |
| VR-08 | `work_date` | ห้ามทับวันลาที่อนุมัติแล้ว | Error | `ERR_OT_LEAVE_CONFLICT` |
| VR-09 | ชั่วโมงที่ขอ vs เวลาจริง | ขอเกิน = บล็อก | Prevent | `ERR_OT_VARIANCE_OVER` |
| VR-10 | ชั่วโมงที่ขอ vs เวลาจริง | ขอน้อยกว่า = เตือน | Warning | — |
| VR-11 | ชั่วโมงสะสมสัปดาห์ | ถึงเกณฑ์เตือน | Warning + Trigger | — |
| VR-12 | ชั่วโมงสะสมสัปดาห์ | เกินเพดาน | Trigger (ไม่บล็อก) | — |
| VR-13 | งวด | ต้องเปิดอยู่ | Prevent | `ERR_OT_PERIOD_CLOSED` |
| VR-14 | สายอนุมัติ | ต้องเลือกคนครบทุก slot + จำนวน = จำนวน step ที่ engine คืน | Error | `ERR_OT_SLOT_INCOMPLETE` |
| VR-15 | การไม่อนุมัติ | เหตุผลห้ามว่าง | Error | `ERR_OT_REASON_REQUIRED` |
| VR-16 | อนุมัติบางส่วน | เหตุผลห้ามว่าง · ชั่วโมง ≤ ที่ขอ **และ** ≤ เวลาจริง | Error | `ERR_OT_HOURS_EXCEED` |
| VR-17 | การถอน | เหตุผลห้ามว่าง | Error | `ERR_OT_REASON_REQUIRED` |
| VR-18 | consent | ต้องมีก่อน submit เมื่อยื่นแทน | Prevent | `ERR_OT_CONSENT_REQUIRED` |
| VR-19 | ยืนยันเวลาจริง | `day_status ∈ {confirmed, locked}` | Prevent | `ERR_OT_ATT_NOT_READY` |
| VR-20 | `ot_no` | อ่านอย่างเดียวทุกจุด | Prevent | `ERR_OT_NO_IMMUTABLE` |
| VR-21 | การกดซ้ำ | `Idempotency-Key` + ปุ่ม disable | Prevent | (คืนผลเดิม) |
| VR-22 | อ่านค่าต้นทางไม่สำเร็จ | บล็อก ห้าม fallback | Prevent | `ERR_UPSTREAM_UNAVAILABLE` |

## §5.5 Edge Cases

### ☑ ยืนยันแล้วจากต้นทาง (24 ข้อ)

| # | Edge Case | พฤติกรรมที่ต้องได้ | trace |
|---|---|---|---|
| EC-01 | สิ้นสุดก่อนเริ่ม / 0 ชั่วโมง | บล็อกตั้งแต่กรอก ชี้บรรทัด | BR-20 |
| EC-02 | บรรทัดทับกันเองในใบ | บล็อก ชี้คู่ที่ทับ | BR-20 |
| EC-03 | ข้ามเที่ยงคืน | `work_date` = วันเข้ากะ + ธง `overnight` | BR-06 |
| EC-04 | `no_shift` | บล็อก + ลิงก์ · **ไม่เดา** | BR-20 |
| EC-05 | Attendance ไม่มีข้อมูลของวัน | "ยังยืนยันเวลาจริงไม่ได้" · **ไม่ใช้ค่าวันใกล้เคียง** | BR-08 |
| EC-06 | วันอยู่สถานะ exception | แสดงเหตุ + ลิงก์ · **ไม่ตีความ 0 ชั่วโมง** | BR-08 |
| EC-07 | ขอมากกว่าเวลาจริง | บล็อกจนแก้/ack | BR-16 |
| EC-08 | ขอน้อยกว่าเวลาจริง | ผ่าน + ธง | BR-16 |
| EC-09 | เวลาถูกแก้ย้อนหลังหลังอนุมัติ | ธง "ต้องทวน" + ค่าก่อน/หลัง | BR-22 |
| EC-10 | ทับวันลาที่อนุมัติแล้ว | บล็อก + เลขที่ใบลา + ลิงก์ | BR-19 |
| EC-11 | ทับใบ OT อื่นของคนเดียวกัน | บล็อก + ลิงก์ (ตรวจ 3 จุด) | BR-29 |
| EC-12 | งวดปิด | ปฏิเสธทุกการเปลี่ยน | BR-15 |
| EC-13 | อัตราถูก inactive | ใบเก่ายังพิมพ์ได้ · เลือกใหม่ไม่ได้ | BR-23 |
| EC-14 | นโยบายเปลี่ยนหลังสร้างใบ | ใบเก่าใช้ค่าเดิมตาม version | BR-03 |
| EC-15 | สะสมข้ามเพดานพอดี | `over_cap` = true → สาย 3 ชั้น + แจ้งแบบปิดไม่ได้ | BR-09 |
| EC-16 | แก้จนกลับมาในเพดานแล้วส่งใหม่ | สาย re-resolve เหลือ 2 ชั้น · เลขเดิม | BR-11 · **§3.0.3 C-1** |
| EC-17 | หัวหน้ายื่นแทนแล้วเป็น slot 1 ด้วย | **DOA escalate ขึ้นไป** · feature ไม่แก้เอง | BR-24 |
| EC-18 | ยังไม่ consent | ส่งอนุมัติไม่ได้ | BR-28 |
| EC-19 | ถอนหลังเผยแพร่แล้ว | รายการกลับ · ยอดสรุปเปลี่ยน | BR-27 |
| EC-20 | ถอนใบที่อยู่ในงวดปิด | ปฏิเสธ | BR-15 |
| EC-21 | ยื่นย้อนหลังเกินกำหนด | ธง "ยื่นเกินกำหนด" ไม่บล็อก | FN-63 |
| EC-22 | เพดานรายวัน/รายเดือนไม่มีค่า | **"ยังไม่มีค่าให้อ่าน" · ไม่มีตัวเลขเดา** | FN-58 · OQ-STD-OT5 |
| EC-23 | ยังไม่มีกติกาปัดเศษ | ใช้ค่าดิบ · ไม่มีตัวเลขนาทีในโค้ด | BR-30 |
| EC-24 | ร่างถูกทิ้ง | ไม่กินเลข | BR-13 |

### ☐ AI-suggested (28 ข้อ · `[AI-SUGGESTED]` — BA ยืนยันที่ SOW3.7)

| # | Edge Case | ค่าที่ใช้ในแพ็กนี้ | tag |
|---|---|---|---|
| CA-01 | สองคนอนุมัติขั้นเดียวกันพร้อมกัน | ล็อกแถวใบ + ตรวจ `current_step` ซ้ำ → `ERR_OT_STEP_TAKEN` | `[AI-DEFAULT]` |
| CA-02 | ยกเลิกชนกับอนุมัติ | การกระทำแรกที่ commit ชนะ → อีกฝ่าย `ERR_OT_STALE` | `[AI-DEFAULT]` |
| CA-03 ⭐ | ยื่นสองใบช่วงทับกันพร้อมกัน | **`EXCLUDE` constraint ที่ฐานข้อมูล** — ไม่พึ่งการตรวจที่หน้าจอ | `[AI-DEFAULT]` · **ยกเป็น OQ** |
| CA-04 | งวดปิดระหว่างที่เปิดใบค้าง | ตรวจซ้ำ ณ วินาที commit | ✅ จาก BRD |
| CA-05 | เวลาถูกแก้ระหว่างยืนยัน | ตรวจ `attendance_version_id` ซ้ำก่อน commit | `[AI-DEFAULT]` |
| DI-01 | HR Config ล่ม | **บล็อก** `ERR_UPSTREAM_UNAVAILABLE` — ห้าม fallback | ✅ จาก BRD |
| DI-02 | Leave ล่ม | **บล็อกการ submit** — ห้ามปล่อยผ่าน | ✅ จาก BRD |
| DI-03 | ผู้ขอลาออกหลังสร้างใบ | ใบเก่าอ่านได้จาก snapshot | `[AI-DEFAULT]` |
| DI-04 ⭐ | ผู้อนุมัติลาออกระหว่างใบค้าง | สายที่ freeze ยังชี้คนเดิม → **เป็นเรื่องของ DOA ไม่ใช่ของ feature** | **ยกเป็น OQ** |
| DI-05 | version_id ของอัตราหายจากต้นทาง | ใบยังแสดง snapshot + ป้ายว่าอ้างเวอร์ชันที่ต้นทางไม่มีแล้ว | `[AI-DEFAULT]` |
| CL-01 | ช่วงพักคาบเกี่ยวบางส่วน | หักเฉพาะส่วนที่ทับ · **ค่าพักมาจากกะ** | `[AI-DEFAULT]` |
| CL-02 | ข้ามวันคร่อมวันหยุดกับวันทำงาน | ประเภทวันยึดวันเข้ากะทั้งช่วง | `[AI-DEFAULT]` · **ยกเป็น OQ ถ้าต้องแยกอัตราตามช่วง** |
| CL-03 | สัปดาห์คร่อมสองงวด | สะสมตามสัปดาห์ · สรุปตามงวด (คนละแกน) | `[AI-DEFAULT]` |
| CL-04 | อนุมัติบางส่วนระดับบรรทัด | Σ บรรทัด = ยอดหัวใบเสมอ | `[AI-DEFAULT]` |
| CL-05 | ชั่วโมงทศนิยมยาว | เก็บ 2 ตำแหน่ง · **ไม่ปัดเป็นบล็อก** | `[AI-DEFAULT]` · BR-30 |
| ST-E01 | ใบค้างขั้นเดิมนาน | **ไม่ทำ reminder ที่ feature** — เป็นของ DOA + ENG-NOTIFY | ✅ จาก BRD (G-11) |
| ST-E02 | ใบถูกตีกลับแล้วไม่แก้ | ค้างที่ `rejected` — ยื่นใหม่เป็นใบใหม่ | `[AI-DEFAULT]` |
| ST-E03 | ถอนแล้วอยากได้คืน | **ไม่มีการย้อนสถานะ** — ยื่นใหม่ | ✅ จาก BRD |
| ST-E04 ⭐ | ใบติดธงค้างถึงวันปิดงวด | **ต้องเคลียร์ก่อนปิดงวด** | `[AI-DEFAULT]` · **OQ-FRD-01** |
| PM-01 | หัวหน้าย้ายแผนกระหว่างใบค้าง | สายที่ freeze ใช้คนเดิม · ขอบเขตการเห็นใช้ค่าปัจจุบัน | `[AI-DEFAULT]` |
| PM-02 | เหตุผลหลุดไปในแจ้งเตือน | **ห้ามใส่ `reason`/`work_done` ใน vars ทุกกรณี** | ✅ จาก brief |
| PM-03 | การส่งออกสรุปงวด | ผ่าน masking เดียวกับหน้าจอ + audit | `[AI-DEFAULT]` |
| PM-04 | ผู้บริหารเห็นใบแผนกอื่น | ขอบเขตมาจาก DOA + Policy Center | `[AI-DEFAULT]` |
| EN-01 | ปลายทางไม่เก็บ version | read model มี `config_version_ids` เสมอ | ✅ จาก §0.13 |
| EN-02 | มีคนสร้างเส้นเขียนกลับ Attendance | **ต้องไม่มี** — มีชุดทดสอบยืนยัน | ✅ IA-02 |
| EN-03 | Payroll อ่านยอดของงวดที่ยังเปิด | มี `period_status` + `pending_docs` + `unconfirmed_hours` ให้ตรวจ | ✅ จาก §0.13.3 |
| EN-04 | Roster ยังไม่มีตัวจริง | จุดเชื่อมแสดงสถานะ + override ด้วยมือ | ✅ จาก BRD |
| EN-05 | ประกาศท่อซ้ำเจ้าของจริง | **EC + FC เท่านั้น** — ท่ออื่นถูกปฏิเสธที่ทะเบียน | ✅ LOCK-7C |

**ธงของบรรทัด (13 ค่า):** `overnight` · `retro` · `over_cap` · `variance_over` · `variance_under` · `no_attendance` · `attendance_exception` · `leave_conflict` · `ot_conflict` · `period_closed` · `no_shift` · `needs_review` · `late_submit`

## §5.6 Error Catalog

| Code | HTTP | ข้อความ (ไทย) | เกิดเมื่อ |
|---|---|---|---|
| `ERR_RESOLVE_DATE_REQUIRED` | 400 | ต้องระบุวันที่ | ไม่ส่ง `date` ให้ read model |
| `ERR_OT_EMPLOYEE_REQUIRED` | 400 | เลือกผู้ขอก่อน | VR-01 |
| `ERR_OT_REASON_REQUIRED` | 400 | ต้องระบุเหตุผล | VR-02 · VR-15 · VR-17 |
| `ERR_OT_WORKDONE_REQUIRED` | 400 | ต้องระบุงานที่ทำ | VR-03 |
| `ERR_OT_TIME_RANGE` | 400 | ช่วงเวลาของบรรทัดที่ {n} ไม่ถูกต้อง | VR-04 |
| `ERR_OT_LINE_OVERLAP` | 400 | บรรทัดที่ {n} ทับกับบรรทัดที่ {m} | VR-05 |
| `ERR_OT_OVERLAP` | 409 | ช่วงนี้ทับกับใบ {ot_no} | VR-06 · BR-29 |
| `ERR_OT_DAYTYPE_UNRESOLVED` | 422 | หากะของวันที่ {date} ไม่ได้ — จัดการที่เวลาเข้างาน | VR-07 |
| `ERR_OT_LEAVE_CONFLICT` | 409 | วันนี้มีใบลา {leave_no} อนุมัติแล้ว | VR-08 |
| `ERR_OT_VARIANCE_OVER` | 422 | ชั่วโมงที่ขอมากกว่าเวลาจริงนอกกะ {x} ชม. | VR-09 |
| `ERR_OT_PERIOD_CLOSED` | 409 | งวด {period_code} ปิดแล้ว — เปิดงวดที่ตั้งค่า HR ก่อน | VR-13 |
| `ERR_OT_SLOT_INCOMPLETE` | 400 | เลือกผู้อนุมัติให้ครบทุกขั้น | VR-14 |
| `ERR_OT_HOURS_EXCEED` | 422 | ชั่วโมงที่รับรองต้องไม่เกินที่ขอและไม่เกินเวลาจริง | VR-16 · BR-21 |
| `ERR_OT_CONSENT_REQUIRED` | 422 | ผู้ทำ OT ยังไม่ได้กดรับทราบ | VR-18 |
| `ERR_OT_ATT_NOT_READY` | 422 | ยังยืนยันเวลาจริงไม่ได้ | VR-19 · BR-08 |
| `ERR_OT_NO_IMMUTABLE` | 403 | เลขที่เอกสารแก้ไม่ได้ | VR-20 |
| `ERR_OT_HOURS_READONLY` | 400 | ชั่วโมงคำนวณโดยระบบ | client ส่ง `hours_requested` มา |
| `ERR_OT_SOD_VIOLATION` | 403 | ผู้ขอเซ็นอนุมัติใบของตัวเองไม่ได้ | BR-24 |
| `ERR_OT_STALE` | 409 | ใบถูกเปลี่ยนไปแล้ว — โหลดใหม่อีกครั้ง | `row_version` ไม่ตรง (PR-1) |
| `ERR_OT_STEP_TAKEN` | 409 | ขั้นนี้ถูกเซ็นไปแล้ว | CA-01 |
| **`ERR_OT_CAP_CHANGED`** ⭐ | 409 | เพดานหรือชั่วโมงสะสมเปลี่ยนไปหลังส่งอนุมัติ — ต้องส่งใบใหม่เพื่อขอสายอนุมัติที่ถูกต้อง | **§3.0.3 C-2 · C-3** |
| `ERR_OT_CHAIN_UNAVAILABLE` | 503 | ขอสายอนุมัติไม่สำเร็จ — ลองใหม่ | DOA ล่ม (**ห้าม fallback**) |
| `ERR_OT_RATE_INACTIVE` | 422 | อัตรานี้ถูกปิดใช้แล้ว | BR-23 |
| `ERR_OT_VERSION_MISSING` | 500 | ใบไม่มีรหัสเวอร์ชันที่ใช้ตัดสิน | O-9 (ข้อมูลเสียหาย) |
| `ERR_OT_APPEND_ONLY` | 403 | ประวัติแก้หรือลบไม่ได้ | BR-14 |
| `ERR_OT_MONEY_FIELD` | 500 | พบช่องจำนวนเงินในข้อมูลที่ส่งออก | **guard `assertNoMoneyField`** |
| `ERR_UPSTREAM_UNAVAILABLE` | 503 | อ่านค่าจากต้นทางไม่สำเร็จ — ลองใหม่หรือแจ้งผู้ดูแล | DI-01 · DI-02 · BR-04 |

## §5.7 Security Bible Application

**Preset P6 (HR / PII Sensitive · 15 controls · Must 9)** — รายละเอียดเต็มที่ BRD §16.3

| Control | ทำอย่างไรในแพ็กนี้ |
|---|---|
| S01-04 SoD | `approveStep` ตรวจ `actor ≠ requested_by ∧ actor ≠ employee_id` → `ERR_OT_SOD_VIOLATION` · การ escalate เป็นของ DOA |
| S01-07 Immutable log | trigger ปฏิเสธ UPDATE/DELETE บน `T_ot_history` · `T_ot_approval_trace` (IA-09) |
| S02-04 Masking | `reason` · `work_done` · ชื่อไฟล์แนบ ถูกปิดบังตาม `04_DB §4.6.3` |
| S02-05 Classification tags | ทุกคอลัมน์มีป้ายใน `04_DB §4.2` |
| S02-06 Export limits | การส่งออกสรุปงวดผ่าน masking เดียวกับหน้าจอ + audit (D-08) |
| S06-01 ABAC | `scope` จาก token · ผู้บริหารเห็นเฉพาะใบที่เป็น slot (PM-04) |
| S06-03 Audit content | `T_ot_history` เก็บ ใคร/ทำอะไร/เมื่อไร/ใบไหน/ค่าก่อน-หลัง/เหตุผล |
| S06-05 Encryption | `reason` · `work_done` · เนื้อไฟล์ เข้ารหัสทั้งขณะส่งและขณะเก็บ |
| S07-06 PII tagging | `employee_id` เป็น ref เสมอ · ชื่อใช้เฉพาะ template ที่แสดงต่อผู้มีสิทธิ์ |

**ข้อกำหนดของแพลตฟอร์มที่แพ็กนี้พึ่ง (ไม่ทำเอง):** การสแกนไฟล์แนบ · MFA · การจัดการคำขอสิทธิ์เจ้าของข้อมูล · นโยบายการเก็บรักษา (PR-A)

## §5.8 Compliance & Audit Requirements

| # | ข้อกำหนด | บังคับที่ไหน |
|---|---|---|
| CA-01 | **ทุกใบที่จ่ายได้ต้องมีลายเซ็นครบตามอำนาจ ณ เวลานั้น** | `approval_chain` freeze + ตรวจซ้ำ §3.0.3 |
| CA-02 | **ใบที่เกินเพดานต้องมีลายเซ็นชั้นที่ 3 เสมอ** | `selectApprovalAction` · **IA-05** |
| CA-03 | **ทุกใบต้องพิสูจน์ได้ว่าคิดจากนโยบายเวอร์ชันไหน** | `config_version_ids` + `cap_snapshot_hours_week` (O-9) |
| CA-04 | **ชั่วโมงที่จ่ายต้องผูกกับเวลาจริงที่บันทึกไว้** | `time_confirmed` + BR-21 |
| CA-05 | **ความยินยอมของลูกจ้างเมื่อถูกยื่นแทน** (กฎหมายแรงงานไทย) | `consent_ack_*` · **รูปแบบหลักฐานรอ OQ-STD-OT7** |
| CA-06 | **ไม่มีการลบข้อมูลถาวร** | ไม่มี DELETE ในระบบ (IA-09) |
| CA-07 | **การส่งออกข้อมูลรายคนต้องมีร่องรอย** | D-08 |
| **CA-08** ⚠️ | **เพดานรายวันกับรายเดือนยังบังคับใช้ไม่ได้** | **ความเสี่ยงที่เปิดอยู่จริง — แสดงบนจอว่า "ยังไม่มีค่าให้อ่าน" · OQ-STD-OT5 · BRD §16.4 R-04** |
