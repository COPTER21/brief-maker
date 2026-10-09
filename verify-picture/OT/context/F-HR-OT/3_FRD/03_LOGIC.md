# 03_LOGIC — F-HR-OT · OT / Shift (โอที)

> Audience: **BE dev (ชั้นตรรกะธุรกิจ)**
> Scope: ตรรกะที่ไม่ใช่ HTTP ทั้งหมด — pure function · การเปลี่ยนสถานะ · การคำนวณ · การตรวจ · การเชื่อมต่อ
> **Convention:** Function = `camelCase` (scope-local) · Engine = `kebab-case` / `ENG-XXX` (นำกลับมาใช้ได้ · ขึ้นทะเบียน CUBIC)
> **Iron Rule ของ Engine:** ห้ามอ้างอิงสิ่งที่เป็น HTTP (req/res/header) · input/output เป็น object ล้วน · feature ห้ามข้าม API ไปเรียก Engine ตรง

---

## §3.0 ⭐ กลไกเพดานกับการเลือกสายอนุมัติ — ส่วนที่สำคัญที่สุดของแพ็กนี้

> อ่านส่วนนี้ก่อนเขียนโค้ดใด ๆ ที่เกี่ยวกับ `over_cap` — ถ้าเข้าใจผิด feature จะละเมิดหลักธรรมาภิบาลโดยที่ทุก test ยังผ่าน

### §3.0.1 ทำไมจึงต้องมีธง แทนที่จะเทียบตัวเลขตรง ๆ ตอนอนุมัติ

**ค่าเพดานชั่วโมงล่วงเวลาเป็นพารามิเตอร์ที่มีวันที่มีผล (effective-dated) และอยู่ที่ HR Configuration** (`ot_rate.cap_hours_week` · HR-1 · P-1 · P-8) — องค์กรเปลี่ยนได้เมื่อกฎหมายเปลี่ยนหรือเมื่อนโยบายภายในเปลี่ยน โดยประกาศล่วงหน้าให้มีผลในอนาคต

ผลที่ตามมา 3 ข้อ:
1. **"เกินเพดานหรือไม่" ไม่ใช่คุณสมบัติของตัวเลขชั่วโมง แต่เป็นคุณสมบัติของ (ชั่วโมง, วันที่, บริษัท)** — 40 ชั่วโมงในเดือนกันยายนอาจไม่เกิน แต่ในเดือนตุลาคมอาจเกิน ถ้าเพดานใหม่มีผลวันที่ 1 ตุลาคม
2. **คำถามต้องถูกถามด้วย `work_date` เสมอ ไม่ใช่ `now()`** — ใบย้อนหลังต้องถูกตัดสินด้วยเพดานของวันที่ทำงานจริง (BR-02)
3. **คำตอบต้องถูกตรึงไว้บนใบ** — `cap_snapshot_hours_week` คือหลักฐานว่าใบนี้ถูกตัดสินด้วยค่าเวอร์ชันไหน มิฉะนั้นการตรวจสอบย้อนหลังทำไม่ได้ (BR-03 · O-9)

ธง `over_cap` จึงเป็น **ผลลัพธ์ที่ถูกตรึง (frozen decision)** ไม่ใช่การเปรียบเทียบที่คำนวณใหม่ทุกครั้งที่มีคนเปิดใบ

### §3.0.2 ⭐ ทำไมชั้นที่สามถูกเลือกด้วย **action id** ไม่ใช่ช่วงตัวเลขใน matrix ของ DOA

ทะเบียนสายอนุมัติกลาง (DOA Engine) ออกแบบ matrix ด้วยขอบตัวเลข (`amount_from` / `amount_to`) ซึ่งเป็นรูปแบบที่ถูกต้องสำหรับ **วงเงิน** — และเป็นกับดักโดยตรงสำหรับ feature นี้

**ทางที่ผิด (ห้ามทำ):**
```
matrix set 1: hours_from 0   → hours_to 36  → 2 steps
matrix set 2: hours_from 36  → hours_to null → 3 steps
```
ทางนี้ดูสมเหตุสมผล แต่สร้าง **แหล่งความจริงสองที่ทันที**:
- ที่หนึ่ง: `ot_rate.cap_hours_week` ที่ HR Configuration (มีวันที่มีผล · มีเวอร์ชัน · มีคนดูแล)
- ที่สอง: เลข `36` ที่ฝังอยู่ในขอบของ matrix (ไม่มีวันที่มีผล · ไม่มีเวอร์ชัน · ไม่มีใครรู้ว่ามีอยู่)

วันที่ HR ประกาศเพดานใหม่ที่ 30 ชั่วโมงให้มีผลเดือนหน้า **matrix ที่ DOA จะเงียบ ๆ ผิดทันที** — ใบที่ควรผ่าน 3 ขั้นจะผ่านแค่ 2 ขั้น โดย **ไม่มี error ไม่มี alert ไม่มีใครรู้** จนกว่าผู้ตรวจสอบจะมาพบ นี่คือการ hardcode ค่ากฎหมายในอีกรูปแบบหนึ่ง ซึ่งผิด **P-8** ตรง ๆ (`06_TESTS IA-05` มีเคสจับข้อนี้โดยเฉพาะ)

**ทางที่ใช้ (บังคับ):**
```
feature: resolveCap(work_date, company_id)      → cap_hours_week (มาจาก HR Config · มี version)
feature: computeWeeklyAccumulated(...)          → hours_accumulated
feature: computeOverCap(accumulated, cap)       → over_cap : bool
feature: selectApprovalAction(over_cap)         → 'ot_approve_within_cap' | 'ot_approve_over_cap'
DOA:     GET /doa/resolve(action_id, …)         → chain 2 ขั้น หรือ 3 ขั้น

matrix set 1 (ot_approve_within_cap): amount_from 0, amount_to null → 2 steps
matrix set 2 (ot_approve_over_cap):   amount_from 0, amount_to null → 3 steps
                                      ↑ ไม่มีตัวเลขชั่วโมงเป็นขอบเลย
```

ผลลัพธ์: **invariant สองข้ออยู่ครบพร้อมกัน**
- สายอนุมัติมาจาก DOA 100% — feature ไม่รู้จักชื่อคนหรือลำดับขั้นเลย (LOCK-DOA)
- ค่าเพดานอยู่ที่ HR Configuration 100% — DOA ไม่รู้จักตัวเลขเพดานเลย (LOCK-CFG · P-8)

**สิ่งที่ feature ส่งเข้า DOA คือ "การตัดสินแล้ว" (`over_cap` → action id) ไม่ใช่ "วัตถุดิบให้ DOA ไปตัดสิน" (ชั่วโมง)** — เพราะการตัดสินต้องใช้ค่าที่มีวันที่มีผลซึ่ง DOA ไม่มีทางรู้

> **ทางเลือกที่ Architect ต้องเคาะ (OQ-DOA-03):** ถ้า DOA รองรับมิติจุดตัดที่ไม่ใช่เงิน (เช่น `threshold_key: ot_over_cap` แบบ boolean ที่ feature ส่งเข้าไป) ให้ยุบเหลือ **1 action 2 set** ได้ — โครงตรรกะข้างบนไม่เปลี่ยน เปลี่ยนแค่รูปแบบการเรียก · **ไม่ว่าเลือกทางไหน ห้ามใส่ตัวเลขชั่วโมงเป็นขอบของ set เด็ดขาด**

### §3.0.3 ⭐ การตรวจซ้ำกลางทาง — ใบที่ต้องถูกตีกลับไป resolve ใหม่

ธง `over_cap` ถูกตรึงตอน submit แต่ **โลกเปลี่ยนได้ระหว่างที่ใบยังเดินสายอยู่** มี 3 กรณีที่ทำให้ค่าที่ตรึงไว้ไม่ตรงกับความจริงอีกต่อไป:

| กรณี | เกิดอะไร | ระบบต้องทำอะไร |
|---|---|---|
| **C-1 · ผู้ขอแก้ชั่วโมงแล้วส่งใหม่** (T-7 · `resubmitRequest`) | ชั่วโมงเปลี่ยน → `over_cap` อาจพลิกจาก true เป็น false หรือกลับกัน | **ยกเลิกงานอนุมัติเดิมทั้งสาย → คำนวณธงใหม่ → เลือก action ใหม่ → resolve สายใหม่ → freeze ใหม่** · **เลขที่เดิมคงอยู่** (BR-11 · BR-13) |
| **C-2 · มีใบอื่นของคนเดียวกันถูกอนุมัติแทรกเข้ามาในสัปดาห์เดียวกัน** | ชั่วโมงสะสมของสัปดาห์เพิ่มขึ้น → ใบที่กำลังรออนุมัติอาจกลายเป็นเกินเพดานทั้งที่ตอน submit ยังไม่เกิน | **`approveStep` ตรวจซ้ำก่อน commit** — ถ้า `computeOverCap()` ปัจจุบัน ≠ `over_cap` ที่ตรึงไว้ → **ปฏิเสธการอนุมัติด้วย `ERR_OT_CAP_CHANGED` แล้วตีใบกลับไปสถานะที่ต้อง re-resolve** |
| **C-3 · HR Configuration ประกาศเพดานใหม่ที่มีผลคร่อมวันที่ทำ OT** | `cap_hours_week` ที่ resolve ได้ ณ `work_date` เปลี่ยนไปจากตอน submit | **`approveStep` ตรวจ `cap_snapshot_hours_week` เทียบค่าที่ resolve ใหม่** — ต่างกัน → `ERR_OT_CAP_CHANGED` เช่นเดียวกัน |

**หลักการเบื้องหลังการตรวจซ้ำ:** ลายเซ็นที่ได้มาแล้วเป็นลายเซ็นบน **สายที่ถูกต้อง ณ ตอนนั้น** — ถ้าจำนวนชั้นที่ควรจะเป็นเปลี่ยนไป การเดินสายเดิมต่อจะได้เอกสารที่มีคนเซ็นไม่ครบตามอำนาจที่ควรมี ซึ่งเป็นความล้มเหลวด้านธรรมาภิบาล **ไม่ใช่แค่ตัวเลขคลาดเคลื่อน**

**สิ่งที่ห้ามทำเด็ดขาดเมื่อพบว่าธงเปลี่ยน:**
- ❌ **ห้ามเติม slot ที่สามเข้าไปในสายที่ freeze แล้วเงียบ ๆ** — สายที่ตรึงไว้เป็นหลักฐาน แก้ไม่ได้ (BR-10 · O-3)
- ❌ **ห้ามปล่อยผ่านเพราะ "ต่างกันนิดเดียว"** — ไม่มีเกณฑ์ผ่อนผัน
- ❌ **ห้ามคำนวณ `over_cap` ใหม่แล้วเขียนทับค่าเดิมบนใบ** — ค่าเดิมคือหลักฐานว่าตอน submit ตัดสินอย่างไร
- ✅ **ต้องตีกลับให้ผู้ขอส่งใหม่** (`resubmitRequest`) ซึ่งจะสร้างสายใหม่พร้อมร่องรอยครบว่าทำไมสายเดิมถูกยกเลิก

**ผลข้างเคียงที่ยอมรับ:** ใบอาจถูกตีกลับแม้ผู้ขอไม่ได้ทำอะไรผิด (กรณี C-2) — ยอมรับได้ เพราะทางเลือกอีกทางคือเอกสารที่ผ่านการอนุมัติไม่ครบชั้น · ข้อความบนจอต้องอธิบายให้ชัดว่าเกิดจากอะไร (`05_RULES §5.6 ERR_OT_CAP_CHANGED`)

### §3.0.4 ⭐ กติกาส่วนต่างระหว่างชั่วโมงที่ขอกับชั่วโมงจริง

ใบ OT มีตัวเลข **สามตัวที่อยู่คู่กันตลอดชีวิตของเอกสาร ไม่เขียนทับกัน** (O-5):

| ตัวเลข | ใครใส่ | ความหมาย |
|---|---|---|
| `hours_requested` | ผู้ขอ (ระบบคำนวณจากช่วงเวลา) | **สิ่งที่ขอ** |
| `hours_approved` | ผู้อนุมัติ | **สิ่งที่ผู้มีอำนาจรับรอง** (≤ ที่ขอ) |
| `hours_confirmed` | ผู้ยืนยัน | **สิ่งที่ผูกกับเวลาจริงแล้ว — ตัวเดียวที่จ่ายได้** |

และมีตัวเลขที่สี่ที่ **ไม่ใช่ของ feature นี้**: `attendance_outside_hours` — ชั่วโมงนอกกรอบกะที่ Attendance บันทึกไว้ ซึ่งต้นทางประกาศเองว่า **ยังไม่ใช่ OT ที่อนุมัติ** (`F-HR-ATTEND §0.13.2` · BR-07)

**กติกาการเทียบ (`computeVariance` + `classifyVariance`):**
```
variance = hours_requested − attendance_outside_hours

variance > 0  (ขอมากกว่าที่ทำจริง)   → class 'over'   → บล็อกการส่งอนุมัติ
variance < 0  (ขอน้อยกว่าที่ทำจริง)  → class 'under'  → ผ่าน + ติดธงให้ผู้อนุมัติเห็น
variance = 0                          → class 'match'  → ผ่านเงียบ
outside_shift_hours = null            → class 'unknown' → ยื่นได้ (ถ้าเป็นคำขอล่วงหน้า)
                                                          แต่ยืนยันเวลาจริงยังไม่ได้
```

**ทำไมสองทิศทางถูกปฏิบัติต่างกัน:**
- **ขอมากกว่าที่ทำจริง = องค์กรกำลังจะจ่ายเงินสำหรับเวลาที่ไม่มีหลักฐาน** → ต้องมีคนรับผิดชอบเป็นลายลักษณ์อักษร จึงบล็อกไว้จนกว่าจะแก้ตัวเลข **หรือ** ผู้อนุมัติกดรับทราบพร้อมเหตุผล (`acknowledgeVariance` เก็บ `variance_ack_by` · `variance_ack_at` · `variance_reason`) — **การรับทราบเป็นทางออกที่มีร่องรอย ไม่ใช่การปิดการตรวจ**
- **ขอน้อยกว่าที่ทำจริง = พนักงานสละสิทธิ์บางส่วน** → ไม่ใช่ความเสี่ยงทางการเงินขององค์กร แต่เป็นสิ่งที่ผู้อนุมัติควรเห็น (อาจเป็นความเข้าใจผิดของผู้ขอ) จึงผ่านแต่ติดธง

**ทำไมไม่มีเกณฑ์ผ่อนผัน (tolerance) ในรอบนี้:** เพราะยังไม่มีใครเคาะว่าเท่าไรจึงยอมได้ (**OQ-STD-OT6**) — และการเดาตัวเลขผ่อนผันเองมีผลเท่ากับการสร้างนโยบายค่าจ้างขึ้นมาลอย ๆ ในโค้ด · รอบนี้จึงใช้ **เกณฑ์ที่เข้มที่สุด (ต่างเกิน 0 = บล็อก)** ซึ่งเป็นค่าที่ปลอดภัยและถอยได้ง่ายเมื่อมีคำตอบ

**ที่ `hours_confirmed` กติกาเข้มขึ้นอีกชั้น (BR-21):**
```
hours_confirmed ≤ hours_approved  AND  hours_confirmed ≤ attendance_outside_hours
```
— ตัวเลขที่จะถูกจ่ายจริงต้องไม่เกินทั้งสิ่งที่ผู้มีอำนาจรับรอง และไม่เกินสิ่งที่เกิดขึ้นจริง **ทั้งสองเงื่อนไขพร้อมกัน**

**เมื่อเวลาจริงเปลี่ยนย้อนหลัง** (`attendance.day_adjusted` · C-3 ของ §3.0.3 คนละเรื่องกัน): ใบที่อนุมัติ/ยืนยันแล้วติดธง `needs_review` — **ห้ามแก้ `hours_confirmed` โดยอัตโนมัติ** เพราะตัวเลขนั้นมีคนเซ็นรับรองไว้แล้ว · ต้องให้คนตัดสินผ่าน `adjustConfirmedHours` (ซึ่งยิง `ot.hours_adjusted` ที่ชี้ค่าเดิม) หรือ `requestWithdrawal` (BR-22)

---

## §3.1 Functions (Scope-Local) — 65 ฟังก์ชัน

> ทุกฟังก์ชันอ้าง FN-XX ของ `FUNCTION_CHECKLIST.md` · ทุกฟังก์ชันถูก trace จาก ≥1 API ที่ `§3.3`

### กลุ่ม A · ร่างและหัวใบ
| # | Function | Input → Output | ทำอะไร | FN |
|---|---|---|---|---|
| F-01 | `createDraft` | `{employee_id, request_mode?, actor}` → `ot_request` | สร้างใบร่าง — **ไม่ออกเลข ไม่ resolve สาย** | FN-08 |
| F-02 | `updateDraft` | `{ot_request_id, patch, row_version}` → `ot_request` | แก้หัวใบร่าง · เพิ่ม `row_version` | FN-08 |
| F-03 | `discardDraft` | `{ot_request_id}` → `void` | ทิ้งร่าง — **ตั้งสถานะ ไม่ลบแถว · ไม่กินเลข** | FN-08 |
| F-04 | `resolveEmployeeScope` | `{actor, scope}` → `employee[]` | คืนคนที่ actor เลือกเป็นผู้ขอได้ (own / team / company) | FN-02 · FN-60 |
| F-05 | `inferRequestMode` | `{work_date, today}` → `'advance' \| 'retro'` | เดาโหมดจากวันที่ · **ผู้ใช้ยืนยันหรือเปลี่ยนได้** | FN-04 |
| F-06 | `validateHeader` | `{ot_request}` → `violation[]` | ตรวจ `reason` · `work_done` · consent · โหมด | FN-03 · FN-65 |
| F-07 | `checkRetroCutoff` | `{work_date, today, cutoff_days}` → `{days_late, late_flag}` | ตั้งธง "ยื่นเกินกำหนด" — **ไม่บล็อก** · `cutoff_days` `[ASSUMED A-3]` | FN-63 |

### กลุ่ม B · บรรทัดและการคำนวณชั่วโมง
| # | Function | Input → Output | ทำอะไร | FN |
|---|---|---|---|---|
| F-08 | `addLine` | `{ot_request_id, line}` → `line` | เพิ่มบรรทัด แล้วเรียกชุด resolve | FN-06 |
| F-09 | `updateLine` | `{ot_line_id, patch}` → `line` | แก้บรรทัด แล้ว resolve ใหม่ทั้งแถว | FN-06 |
| F-10 | `removeLine` | `{ot_line_id}` → `void` | ลบบรรทัด **เฉพาะตอนยังเป็นร่าง** — หลัง submit แก้ได้ทาง resubmit เท่านั้น | FN-06 |
| F-11 | `detectOvernight` | `{time_from, time_to}` → `bool` | `time_to < time_from` = ข้ามวัน | FN-05 |
| F-12 | `computeLineHours` | `{time_from, time_to, is_overnight, break_hours, rounding?}` → `hours` | คำนวณชั่วโมง (บวก 24 เมื่อข้ามวัน แล้วหักพัก) · **`rounding` เป็น `null` ในรอบนี้ → ใช้ค่าดิบ ห้ามใส่ตัวเลขนาทีในโค้ด** | FN-05 · **FN-62** |
| F-13 | `validateLines` | `{lines}` → `violation[]` | ช่วงเวลาไม่ถูกต้อง · ทับกันเองในใบ | FN-07 |

### กลุ่ม C · อ่านค่าจากต้นทาง
| # | Function | Input → Output | ทำอะไร | FN |
|---|---|---|---|---|
| F-14 | `resolveDayType` | `{work_date, employee_id, company_id}` → `day_type \| null` | อ่านผลของวัน + ปฏิทิน + กะ จาก Attendance — **`null` = ตัดสินไม่ได้ → บล็อก ห้ามเดา** | FN-09 · FN-13 |
| F-15 | `mapRateType` | `{day_type, ot_rate_set}` → `rate_type` | map ตามนิยามของ HR Config — **ไม่ใช่ตารางที่ feature นิยามเอง** | FN-13 |
| F-16 | `resolveOtRate` | `{rate_type, work_date, company_id}` → `{multiplier, payroll_code, version_id, active}` | อ่านอัตรา ณ `work_date` · ค่า `inactive` เลือกใหม่ไม่ได้แต่ใบเก่ายังอ่านได้ | FN-10 · FN-12 |
| F-17 | `resolveCap` ⭐ | `{work_date, company_id}` → `{cap_hours_week, cap_hours_day, cap_hours_month, version_id}` | อ่านเพดานจาก HR Config · **`cap_hours_day` / `cap_hours_month` เป็น `null` เสมอในรอบนี้ — ห้ามแทนด้วยตัวเลข** | FN-10 · **FN-58** |
| F-18 | `fetchAttendanceDay` | `{work_date, employee_id}` → `{outside_shift_hours \| null, day_status, version_id, exception_type?}` | อ่านวันจาก Attendance — **สถานะข้อยกเว้นคืน `null` ไม่ใช่ 0** | FN-17 · FN-23 · FN-24 |
| F-19 | `checkLeaveConflict` | `{work_date, employee_id}` → `leave_conflict_ref \| null` | อ่านวันลาที่อนุมัติแล้ว — **ไม่คำนวณจำนวนวันลาเอง** | FN-16 |
| F-20 | `snapshotConfigVersions` | `{ot_request}` → `config_version_ids` | รวบรวมทุก version_id เป็นก้อนเดียว | FN-11 |
| F-21 | `invalidateResolveCache` | `{event}` → `void` | ล้าง cache ตาม 7 event (BR-04) | — |
| F-22 | `registerWhereUsed` | `{}` → `void` | ลงทะเบียนที่ 3 ต้นทาง | FN-52 |

### กลุ่ม D · เพดานและการเลือกสาย ⭐
| # | Function | Input → Output | ทำอะไร | FN |
|---|---|---|---|---|
| F-23 | `computeWeeklyAccumulated` | `{employee_id, week_start, exclude_request_id?}` → `hours` | รวมชั่วโมงที่ `approved`/`time_confirmed` ในสัปดาห์นั้น + ชั่วโมงที่กำลังขอ · ขอบสัปดาห์จาก `period_rule` `[ASSUMED A-1]` | FN-14 |
| F-24 | `computeOverCap` ⭐ | `{accumulated, cap_hours_week}` → `bool` | `accumulated > cap` · **ค่าเพดานเป็น input ไม่ใช่ค่าคงที่ในฟังก์ชัน** | **FN-15** |
| F-25 | `computeCapWarning` | `{accumulated, cap_hours_week, warn_ratio}` → `bool` | `warn_ratio` `[ASSUMED A-2 · OQ-OT-10]` — **ควรย้ายไป HR Config** | FN-14 |
| F-26 | `selectApprovalAction` ⭐ | `{over_cap}` → `'ot_approve_within_cap' \| 'ot_approve_over_cap'` | **หัวใจของ §3.0.2** — แปลงธงเป็น action id · **ฟังก์ชันนี้ต้องไม่รับตัวเลขชั่วโมงเป็น input เลย** | **FN-28** |
| F-27 | `resolveApprovalChain` | `{action_id, employee_id, company_id}` → `chain[]` | เรียก **ENG-DOA-01** · **ไม่มีรายชื่อหรือลำดับขั้นในโค้ดของ feature** | FN-25 · FN-26 |
| F-28 | `freezeApprovalChain` | `{ot_request_id, chain, picked_assignees}` → `void` | ตรึงสายลงใบ + เขียน trace ทุก step | FN-25 |
| F-29 | `buildSignatureSlots` | `{approval_chain}` → `slot[]` | สร้างช่องลงนามสำหรับ PDF — **จำนวน = `chain.length + 1`** | FN-32 · **FN-37** |

### กลุ่ม E · การเทียบเวลาจริง
| # | Function | Input → Output | ทำอะไร | FN |
|---|---|---|---|---|
| F-30 | `computeVariance` | `{hours_requested, outside_shift_hours}` → `hours \| null` | ผลต่าง · `null` เมื่อไม่มีข้อมูล | FN-17 |
| F-31 | `classifyVariance` | `{variance}` → `'over' \| 'under' \| 'match' \| 'unknown'` | ตาม §3.0.4 | FN-19 · FN-20 |
| F-32 | `acknowledgeVariance` | `{ot_request_id, actor, reason}` → `void` | บันทึกการรับทราบส่วนต่าง — **ทางออกเดียวของการบล็อก** | FN-19 |

### กลุ่ม F · การตรวจก่อนส่งและการชน
| # | Function | Input → Output | ทำอะไร | FN |
|---|---|---|---|---|
| F-33 | `checkOtOverlap` | `{employee_id, work_date, time_from, time_to, exclude_request_id}` → `ot_conflict_ref \| null` | เรียก **ENG-OVERLAP** · ตรวจกับใบที่ยังไม่ปิด | **FN-61** |
| F-34 | `checkPeriodOpen` | `{work_date, company_id}` → `{period_code, status}` | **เรียกทั้งตอนเปิดหน้าและ ณ วินาที commit** | FN-40 |
| F-35 | `buildPreSubmitReport` | `{ot_request}` → `precheck` | รวมผลตรวจทั้งหมดสำหรับขั้น 4 | FN-14 · FN-15 · FN-58 |

### กลุ่ม G · การเปลี่ยนสถานะ
| # | Function | Input → Output | ทำอะไร | FN |
|---|---|---|---|---|
| F-36 | `issueDocNumber` | `{doc_type:'OT', company_ctx}` → `ot_no` | เรียก **ENG-DOC-NUM** — **ห้าม format เอง ห้าม +1 เอง · เรียกหลัง resolve สายสำเร็จเท่านั้น** | FN-34 · FN-35 |
| F-37 | `submitRequest` ⭐ | `{ot_request_id, slots, row_version}` → `ot_request` | ลำดับ 7 ขั้นตาม `02_API API-06` | FN-25…FN-28 · FN-34 |
| F-38 | `resubmitRequest` ⭐ | `{ot_request_id, row_version}` → `ot_request` | **ยกเลิกงานเดิม → คำนวณธงใหม่ → เลือก action ใหม่ → resolve+freeze ใหม่ · เลขเดิม** (§3.0.3 C-1) | **FN-33** |
| F-39 | `approveStep` ⭐ | `{ot_request_id, actor, note?, row_version}` → `ot_request` | ตรวจเจ้าของ slot · SoD · **ตรวจซ้ำ 3 อย่างของ §3.0.3** · เดินสาย · ขั้นสุดท้ายสร้าง PDF + เก็บสำเนา | FN-29 · FN-38 |
| F-40 | `approvePartial` | `{ot_request_id, hours_by_line, reason}` → `ot_request` | ตรวจ BR-21 ทั้งสองเงื่อนไข | FN-31 |
| F-41 | `rejectRequest` | `{ot_request_id, reason}` → `ot_request` | **เหตุผลบังคับ · เลขคงอยู่** | FN-30 |
| F-42 | `cancelRequest` | `{ot_request_id, reason?}` → `ot_request` | ปิดงานอนุมัติที่ค้าง · **เหตุผลไม่บังคับ** (OQ-OT-14) | FN-39 |
| F-43 | `requestWithdrawal` | `{ot_request_id, reason}` → `ot_request` | **เหตุผลบังคับ** · เข้าสายอนุมัติอีกครั้ง | FN-41 |
| F-44 | `finalizeWithdrawal` | `{ot_request_id}` → `ot_request` | สร้าง **รายการกลับที่ชี้ของเดิม** · ของเดิมไม่ถูกแตะ | FN-42 |
| F-45 | `confirmActualHours` ⭐ | `{ot_request_id, hours_by_line, row_version}` → `ot_request` | guard ครบตาม `02_API API-13` → `time_confirmed` → **เริ่มเผยแพร่** | **FN-21** |
| F-46 | `autoConfirmRetro` | `{ot_request_id}` → `ot_request \| null` | ใบ retro ที่วันนั้นยืนยันแล้ว → ยืนยันต่อเนื่องหลังอนุมัติ | FN-22 |

### กลุ่ม H · ธง "ต้องทวน" และการปรับ
| # | Function | Input → Output | ทำอะไร | FN |
|---|---|---|---|---|
| F-47 | `onAttendanceDayAdjusted` | `{event}` → `void` | รับสัญญาณ → หาใบที่อ้างวันนั้น → ตั้งธง + เก็บค่าก่อน/หลัง → แจ้ง HR · **ห้ามแก้ตัวเลขในใบ** | **FN-43** |
| F-48 | `resolveNeedsReview` | `{ot_request_id}` → `review_context` | รวมข้อมูลให้คนตัดสิน (ค่าก่อน/หลัง · ทางเลือก 2 ทาง) | FN-43 |
| F-49 | `adjustConfirmedHours` | `{ot_request_id, hours_after, reason}` → `ot_request` | ปรับชั่วโมงที่รับรอง → ยิง `ot.hours_adjusted` ที่ **`supersedes`** ค่าเดิม | FN-43 |

### กลุ่ม I · ยื่นแทนและการรับทราบ
| # | Function | Input → Output | ทำอะไร | FN |
|---|---|---|---|---|
| F-50 | `splitProxyRequests` | `{employee_ids[], template}` → `ot_request[]` | **แตก 1 ใบต่อคน** · **ทั้งชุดเป็นธุรกรรมเดียว ล้มทั้งชุด** (PR-5) | **FN-44** |
| F-51 | `recordConsent` | `{ot_request_id, actor}` → `void` | บันทึกการรับทราบ — **actor ต้องเป็นผู้ทำ OT เท่านั้น** | FN-44 |

### กลุ่ม J · เอกสารและ PDF
| # | Function | Input → Output | ทำอะไร | FN |
|---|---|---|---|---|
| F-52 | `attachDocument` | `{ot_request_id, file}` → `attachment` | แนบได้ทั้งก่อนและหลังยื่น | FN-64 |
| F-53 | `archiveAttachment` | `{attachment_id}` → `void` | **ตั้งธงเก็บถาวร ไม่ลบ** | FN-64 |
| F-54 | `renderOtPdf` | `{ot_request, signature_slots}` → `pdf` | ใช้ `PDFDOC/template.html` — **ห้ามวาดใบขึ้นใหม่** · ใช้ค่า snapshot ทั้งหมด | FN-36 · FN-12 |
| F-55 | `storeApprovedCopy` | `{pdf, ot_request_id}` → `void` | **ENG-DOC-STORE** `approved_final` — **render จากข้อมูล ณ เวลาอนุมัติ ห้าม re-render ภายหลัง** | FN-38 |

### กลุ่ม K · Read model และสรุปงวด
| # | Function | Input → Output | ทำอะไร | FN |
|---|---|---|---|---|
| F-56 | `buildDayReadModel` ⭐ | `{filter}` → `day_row[]` | **กรอง `status ∈ {time_confirmed, withdrawn}` เท่านั้น** (BR-17) · ไม่มีช่องเงิน | **FN-45 · FN-46** |
| F-57 | `buildPeriodSummary` | `{period_code, employee_id?}` → `period_row[]` | รวมชั่วโมง **แยกตาม `rate_type`** + นับใบที่ยังไม่ปิด/ติดธง | FN-47 |
| F-58 | `freezePeriodSummary` | `{period_code}` → `void` | ตรึงยอดเมื่อได้สัญญาณปิดงวด — **ห้าม UPDATE อีก** | FN-48 |
| F-59 | `buildCapDashboard` | `{employee_id, week_of}` → `cap_view` | ข้อมูลหน้า `#/ot/cap` | FN-14 · FN-58 |
| F-60 | `buildConfirmQueue` | `{scope}` → `queue_row[]` | คิวหน้า `#/ot/confirm` | FN-21 · FN-43 |
| F-61 | `buildLinkageStatus` | `{}` → `linkage[]` | สถานะการเชื่อมโมดูลปลายทาง 5 รายการ | FN-49 |

### กลุ่ม L · ร่องรอย เหตุการณ์ และงานตามเวลา
| # | Function | Input → Output | ทำอะไร | FN |
|---|---|---|---|---|
| F-62 | `appendHistory` | `{ot_request_id, action, before, after, reason, actor}` → `void` | **append-only · ไม่มี update ไม่มี delete** | FN-59 |
| F-63 | `appendApprovalTrace` | `{ot_request_id, step}` → `void` | append-only | FN-32 |
| F-64 | `emitNotification` | `{event_id, ref, vars}` → `void` | **ENG-NOTIFY** — **ห้ามเลือกช่องทางเอง · ห้ามใส่ `reason`/`work_done` ลง vars** | FN-50 · FN-51 |
| F-65 | `emitImpactEvent` | `{event_id, payload}` → `void` | **ENG-CSQ** ท่อ EC/FC — **ห้ามคำนวณมูลค่า** | — |
| F-66 | `sweepPendingConfirm` | *(scheduler รายวัน)* → `void` | กวาดใบที่เลยกำหนดยืนยัน + ใบติดธง → ยิง `ot_confirm_pending` | **FN-51** |
| F-67 | `assertNoMoneyField` | `{payload}` → `void` | **guard ที่ทุก response/event ต้องผ่าน** — ปฏิเสธ key ที่เป็นจำนวนเงิน | **FN-53** |

> **หมายเหตุการนับ:** ฟังก์ชันในไฟล์นี้มี **67 รายการ** ครอบ **65 FN** — F-67 `assertNoMoneyField` และ F-21 `invalidateResolveCache` เป็นฟังก์ชันโครงสร้างที่รับใช้ FN-53 และ BR-04 ตามลำดับ

## §3.2 Engines (Reusable / CUBIC-Registered) — 12 ตัว (**ใหม่ 4**)

| Engine | ชนิด | หน้าที่ | input → output | ใครใช้ได้อีก |
|---|---|---|---|---|
| **`ot-cap-evaluation-engine`** (`ENG-OTCAP`) ⭐ **NEW** | คำนวณ | รวมชั่วโมงสะสมตามขอบเวลาที่กำหนด แล้วเทียบกับเพดานที่ถูกส่งเข้ามา คืน `{accumulated, remaining, warning, over}` — **เพดานเป็น input เสมอ ไม่มีค่าคงที่ในเครื่องยนต์** | `{entries[], window, cap, warn_ratio}` → `{accumulated, remaining, warning, over}` | **รองรับเพดานรายวัน/รายเดือนได้ทันทีที่ HR Config เผยแพร่คีย์ (OQ-STD-OT5)** · ใช้ซ้ำได้กับเพดานวันลาต่อเนื่อง · เพดานชั่วโมงทำงานรายสัปดาห์ |
| **`time-variance-engine`** (`ENG-VARIANCE`) ⭐ **NEW** | คำนวณ | เทียบปริมาณที่ประกาศกับปริมาณที่วัดได้ แล้วจัดประเภทส่วนต่างพร้อมกติกาการบล็อก | `{claimed, actual\|null, policy}` → `{variance, class, blocking}` | ใช้ซ้ำได้กับทุกเอกสารที่มี "สิ่งที่ขอ vs สิ่งที่วัดได้" — เบิกวัสดุ vs ที่ใช้จริง · ชั่วโมงเครื่องจักร · ระยะทางที่เบิก |
| **`overlap-detection-engine`** (`ENG-OVERLAP`) ⭐ **NEW** | ตรวจ | ตรวจการทับซ้อนของช่วงเวลาในชุดข้อมูลที่กำหนด คืนคู่ที่ชน | `{ranges[], candidate, exclude_id}` → `conflict[]` | ใช้ซ้ำได้กับ จัดกะ/เวร · การจองห้อง · การจองรถ · ใบลาที่ทับกัน |
| **`period-snapshot-freeze-engine`** (`ENG-PERIOD-FREEZE`) ⭐ **NEW (candidate)** | สถานะ | ตรึงยอดสรุปของงวดเมื่อได้สัญญาณปิดงวด แล้วปฏิเสธการแก้ทุกกรณีหลังจากนั้น | `{period_code, rows[]}` → `frozen_rows[]` | **ตระกูลเดียวกับสรุปงวดของ Leave และ Attendance — สมควรรวมเป็นตัวเดียวทั้งโมดูล HR** (เสนอให้ Architect) |
| `doa-resolution-engine` (`ENG-DOA-01`) | EXISTING | คืนสายอนุมัติจาก action id + บริบท | `{action_id, actor, company}` → `chain[]` | ทุก feature ที่มีการอนุมัติ |
| `document-numbering-engine` (`ENG-DOC-NUM`) | EXISTING | ออกเลขรันตาม doc_type | `{doc_type, company_ctx}` → `doc_no` | ทุกเอกสาร |
| `document-store-engine` (`ENG-DOC-STORE`) | EXISTING | เก็บสำเนาเอกสารที่ตรึงค่า | `{pdf, doc_type, ref, kind}` → `void` | ทุกเอกสาร |
| `notification-engine` (`ENG-NOTIFY`) | EXISTING | ยิงการแจ้งเตือนตาม catalog | `{event_id, ref, vars}` → `void` | ทุก feature |
| `impact-valuation-engine` (`ENG-CSQ-02`) | EXISTING | **ตีมูลค่าผลกระทบ — feature ห้ามทำเอง** | `{envelope}` → `void` | ทุก feature |
| `hr-config-resolve-client` (`ENG-HRCFG-RESOLVE`) | EXISTING | อ่านค่านโยบายด้วย `(date, company, group)` + คืน version_id | `{date, company_id, group}` → `config` | ทุก feature ในโมดูล HR |
| `attendance-resolve-client` (`ENG-ATT-RESOLVE`) | EXISTING | อ่านวันทำงานรายคน + สถานะของวัน | `{date, employee_id}` → `day` | OT · Payroll · Leave |
| `leave-resolve-client` (`ENG-LEAVE-RESOLVE`) | EXISTING | อ่านวันลาที่อนุมัติแล้ว | `{date, employee_id}` → `leave_day[]` | OT · Attendance · Roster |

**Engine Iron Rules (ตรวจแล้ว):** ไม่มี Engine ใดอ้างอิงสิ่งที่เป็น HTTP ✅ · input/output เป็น object ล้วน ✅ · feature เรียก Engine ผ่านชั้น Function เท่านั้น ไม่ข้าม API ✅

> **Engine candidate ที่ต้องส่งให้ Architect (4 ตัว):** `ot-cap-evaluation-engine` · `time-variance-engine` · `overlap-detection-engine` · `period-snapshot-freeze-engine` — ทั้งสี่ตัวถูกออกแบบให้ **ไม่มีค่านโยบายอยู่ข้างใน** (ค่าเป็น input เสมอ) จึงนำกลับมาใช้ข้าม feature ได้จริง

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

| API | Function ที่ถูกเรียก | Engine |
|---|---|---|
| API-01 | F-01 · F-62 | — |
| API-02 | F-02 · F-05 · F-06 · F-07 · F-62 | — |
| API-03 | F-04 | — |
| API-04 | F-08 · F-09 · F-10 · F-11 · F-12 · F-13 · F-14 · F-15 · F-16 · F-18 · F-19 · F-30 · F-31 · F-33 | ENG-HRCFG-RESOLVE · ENG-ATT-RESOLVE · ENG-LEAVE-RESOLVE · ENG-OVERLAP · ENG-VARIANCE |
| API-05 | F-17 · F-23 · F-24 · F-25 · F-34 · F-35 · F-07 | ENG-OTCAP |
| API-06 | F-06 · F-13 · F-34 · F-17 · F-23 · F-24 · **F-26** · F-27 · F-36 · F-20 · F-28 · F-63 · F-62 · F-64 · F-37 | ENG-OTCAP · ENG-DOA-01 · ENG-DOC-NUM · ENG-NOTIFY |
| API-07 | F-29 | — |
| API-08 | F-39 · F-34 · F-19 · F-33 · F-17 · F-24 · F-54 · F-55 · F-63 · F-62 · F-64 · F-65 · F-46 | ENG-DOC-STORE · ENG-NOTIFY · ENG-CSQ-02 |
| API-09 | F-40 · F-62 · F-64 · F-65 | ENG-NOTIFY · ENG-CSQ-02 |
| API-10 | F-41 · F-62 · F-64 · F-65 | ENG-NOTIFY · ENG-CSQ-02 |
| API-11 | F-42 · F-62 · F-64 | ENG-NOTIFY |
| API-12 | F-43 · F-44 · F-27 · F-28 · F-62 · F-64 · F-65 | ENG-DOA-01 · ENG-NOTIFY · ENG-CSQ-02 |
| API-13 | F-45 · F-18 · F-34 · F-56 · F-62 · F-65 | ENG-ATT-RESOLVE · ENG-CSQ-02 |
| API-14 | F-60 · F-48 | — |
| API-15 | F-32 · F-62 | — |
| API-16 | F-38 · F-24 · **F-26** · F-27 · F-28 · F-62 | ENG-OTCAP · ENG-DOA-01 |
| API-17 | F-47 · F-48 · F-62 · F-64 | ENG-NOTIFY |
| API-18 | F-50 · F-01 · F-62 | — |
| API-19 | F-51 · F-62 | — |
| API-20 | F-56 · F-67 | — |
| API-21 | F-57 · F-58 · F-67 | ENG-PERIOD-FREEZE |
| API-22 | F-61 | — |
| API-23 | F-52 · F-62 | — |
| API-24 | F-53 · F-62 | — |
| API-25 | F-22 | — |
| API-26 | F-49 · F-43 · F-62 · F-65 | ENG-CSQ-02 |
| *(scheduler)* | F-66 · F-64 | ENG-NOTIFY |
| *(event listener)* | F-21 | — |
| *(ทุก response/event)* | **F-67** | — |

**ตรวจ R8:**
- ทุก mutation API มี ≥ 1 Function ✅ (26/26)
- ทุก Function ใน §3.1 ถูก trace อย่างน้อย 1 จุด ✅ (67/67 — F-59 ผ่าน API-05/หน้า cap · F-66 · F-21 · F-67 ผ่านจุดที่ระบุไว้ท้ายตาราง)
- ทุก Engine ใน §3.2 ถูก trace ผ่าน Function ✅ (12/12)
- **ไม่มี orphan Function/Engine** ✅

## §3.4 Dependencies

| ต้องมีก่อน | ใช้ทำอะไร | ถ้าไม่มี |
|---|---|---|
| ENG-HRCFG-RESOLVE | อัตรา · ตัวคูณ · **เพดาน** · ปฏิทิน · กะ · งวด | **บล็อกทั้ง feature** |
| ENG-ATT-RESOLVE | ชั่วโมงนอกกรอบกะ · สถานะของวัน | ยืนยันเวลาจริงไม่ได้ |
| ENG-LEAVE-RESOLVE | วันลาที่อนุมัติแล้ว | **บล็อกการส่งอนุมัติ** (ห้ามปล่อยผ่าน) |
| ENG-DOA-01 | สายอนุมัติ | **บล็อกการส่งอนุมัติ — ห้าม fallback เป็นสายที่เขียนตาย** |
| ENG-DOC-NUM · ENG-DOC-STORE | เลขที่ · สำเนา | บล็อกการส่งอนุมัติ / การอนุมัติขั้นสุดท้าย |
| ENG-NOTIFY · ENG-CSQ-02 | แจ้งเตือน · ผลกระทบ | ไม่บล็อกเอกสาร แต่ต้องบันทึกว่ายิงไม่สำเร็จ |

## §3.5 Open Questions / Locked Decisions Referenced

| อ้างถึง | เรื่อง |
|---|---|
| **OQ-STD-OT5** | `resolveCap` คืน `cap_hours_day` · `cap_hours_month` เป็น `null` เสมอ — **โครงพร้อมรับค่าทันทีที่ต้นทางเผยแพร่** |
| **OQ-OT-16** | `computeLineHours` รับ `rounding` เป็น `null` — **ไม่มีตัวเลขนาทีในโค้ด** |
| OQ-OT-10 | `computeCapWarning` รับ `warn_ratio` เป็น input — ค่าเริ่มต้นอยู่ในตารางค่า ไม่ใช่ในฟังก์ชัน |
| OQ-OT-09 | `computeWeeklyAccumulated` รับขอบสัปดาห์เป็น input |
| **OQ-DOA-03** | `selectApprovalAction` เป็นจุดเดียวที่ต้องแก้ถ้า DOA รองรับมิติจุดตัดที่ไม่ใช่เงิน |
| OQ-STD-OT6 | `classifyVariance` รับ `policy` เป็น input — พร้อมรับเกณฑ์ผ่อนผันเมื่อมีคำตอบ |
| OQ-STD-OT7 | `recordConsent` โครงพร้อม — รูปแบบหลักฐานรอฝ่ายกฎหมาย |
| LD-OT-01…LD-OT-12 | ดู `07_LOCKED_DECISIONS §7.1` |

## Audience Cheat-Sheet

| คำถาม | ไปที่ |
|---|---|
| ทำไมชั้นที่สามไม่ได้มาจากตัวเลขใน matrix | **§3.0.2** |
| ใบถูกตีกลับตอนไหน ทำไม | **§3.0.3** |
| ขอเกินเวลาจริงแล้วต้องทำอย่างไร | **§3.0.4** |
| ฟังก์ชันไหนเขียนคอลัมน์ไหน | `04_DB §4.2` + ตาราง §3.1 |
| API ไหนเรียกอะไรบ้าง | **§3.3** |
| Engine ตัวไหนใหม่ ตัวไหนของเดิม | **§3.2** |
