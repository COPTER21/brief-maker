# 03_LOGIC — F-HR-ROSTER · Shift & Roster (จัดกะ)

> **Audience: BE dev (ตรรกะธุรกิจ)** · **นี่คือไฟล์ที่สำคัญที่สุดของแพ็ก**
> **CUBIC 3-layer:** API (HTTP) → **Function (ตรรกะของ feature · camelCase)** → **Engine (ตรรกะบริสุทธิ์ · kebab-case)**
> **Engine ห้ามรู้จัก HTTP** — รับ object คืน object เท่านั้น (Phase 3.5 Section F)
> **ห้ามมี business logic ใน `02_API`** — ทุก mutation ต้อง trace มาที่ไฟล์นี้ (R8 · Phase 3.5 Section C)

---

## §3.0 กลไกของตัวตรวจข้อขัดแย้ง (หัวใจของแพ็ก) ⭐

> อ่านส่วนนี้ก่อนแตะโค้ดใด ๆ — **ครึ่งหนึ่งของกฎธุรกิจในแพ็กนี้เกิดขึ้นที่นี่**
> ตัวตรวจถูกห่อเป็น engine เดียวชื่อ **`roster-conflict-engine` (ENG-ROSTER-CONFLICT)** — **engine candidate ใหม่ที่ต้องเสนอ Architect ลง CUBIC** (LOCK-ENGINE)
> **กติกาเหล็ก:** **การแก้ตารางด้วยมือ (T-2) กับการตรวจคำขอสลับกะ (W-2) ต้องเรียก engine ตัวเดียวกัน** — ห้ามเขียนตรรกะตรวจสองชุด (`STANDARD_BASELINE C-17` · `06_TESTS IA-05`)

### §3.0.1 เส้นเวลาต่อเนื่อง — จุดตั้งต้นของทุกกฎ

**ปัญหา:** กะดึก `22:00–06:00` ของวันที่ 18 กับ กะเช้าสั้น `05:00–09:00` ของวันที่ 19 อยู่คนละคอลัมน์ของตาราง และถ้าเทียบเป็น **เวลานาฬิกาของวันปฏิทิน** จะไม่มีทางเห็นว่าทับกัน

**วิธีแก้ (บังคับ):** แปลงทุกกะเป็น **ช่วงบนเส้นเวลาต่อเนื่อง** ที่นับเป็น **นาทีจาก 00:00 ของ `work_date`**

```
toTimeline(cell) → interval

  start_min = minutesOf(cell.start_time)
  end_min   = minutesOf(cell.end_time) + (cell.is_overnight ? 1440 : 0)
  base      = daysBetween(anchorDate, cell.work_date) * 1440

  return { from: base + start_min, to: base + end_min, ref: cell }
```

**กติกาที่ผูกอยู่กับสูตรนี้:**

| # | กติกา | ทำไม |
|---|---|---|
| **T-A** | **`work_date` ของกะข้ามคืนคือ "วันเข้ากะ" เสมอ** — ไม่ใช่วันที่ออกกะ | **LD-01** · นิยามเดียวกับ Attendance `FN-C02` และ OT `§0.13.2` — **ห้ามตั้งนิยามใหม่** (BR-06) |
| **T-B** | **ช่วงเป็นแบบปลายเปิด `[from, to)`** | ทำให้ "จบพอดี 06:00 แล้วเริ่มพอดี 06:00" **ไม่ทับกัน** — ซึ่งถูกต้องทางกายภาพ (คนออกกะแล้วเข้ากะทันทีเป็นเรื่องของ **ช่วงพัก** ไม่ใช่ **การทับ**) |
| **T-C** | **ห้ามใช้ timestamp / timezone** — ใช้นาทีล้วนเทียบกับ `anchorDate` ของชุดที่กำลังตรวจ | เลี่ยงปัญหาเขตเวลาและ DST ที่ไม่มีความหมายในบริบทของตารางกะ (`00_OVERVIEW` PR-10) |
| **T-D** | **กะแยกช่วงในวันเดียวให้หลายช่วงจาก `work_date` เดียวกัน** — แยกด้วย `slot_seq` | ทำให้ split shift เป็นข้อมูลได้โดยไม่ต้องเปลี่ยนโครงกริด (`04_DB` unique key) |

### §3.0.2 นิยามของ "ชนกัน" — **ช่วงเวลาทับกัน ไม่ใช่ "สองกะในวันเดียว"** ⭐⭐

> **นี่คือข้อบกพร่องจริงที่ถูกจับได้และแก้ไปแล้วที่ S1.5 (`STANDARD_GAP.md` G-02)** — เขียนไว้ตรงนี้ให้ชัดที่สุดเพื่อไม่ให้ dev เขียนกลับไปเป็นแบบเดิม

**❌ ผิด (นิยามเดิมที่ถูกแก้ไปแล้ว):**
```
if (cellsOfSameEmployeeSameDay.length > 1) → conflict 'overlap'
```
นิยามนี้จะ **บล็อกกะแยกช่วง (split shift) ซึ่งถูกกฎหมายและใช้จริงในธุรกิจที่มีช่วงพีคสองช่วง** (เช่น ร้านอาหาร โรงงานที่มีช่วงเดินเครื่องสองรอบ) — และจะ **พลาดการทับข้ามคืน** เพราะสองกะนั้นอยู่คนละ `work_date`

**✅ ถูก (นิยามที่ต้องใช้):**
```
detectOverlap(intervalsOfSameEmployee) → conflicts[]

  เรียงช่วงตาม from
  สำหรับทุกคู่ (A, B) ที่ติดกันหลังเรียง:
      ทับกันเมื่อ  B.from < A.to        ← ปลายเปิด: เท่ากันพอดี = ไม่ทับ
      ถ้าทับ:
          flag = (A.ref.work_date == B.ref.work_date) ? 'overlap' : 'overnight_overlap'
          level = 'block'
          ชี้ทั้งสองช่องเสมอ (ไม่ใช่ช่องเดียว)
```

| ผลลัพธ์ที่ต้องได้ | ตัวอย่าง | ผล |
|---|---|---|
| สองกะวันเดียวกัน **ทับเวลา** | `M 06:00–14:00` + `D 10:00–18:00` วันที่ 25 | **`overlap` · ระดับห้าม** (FN-11) |
| สองกะวันเดียวกัน **ไม่ทับเวลา (split shift)** | `H1 05:00–09:00` + `H2 16:00–20:00` วันที่ 9 | **ไม่เป็นข้อขัดแย้ง** — แต่ **ช่วงว่าง 09:00–16:00 ถูกวัดเป็นช่วงพัก** และชั่วโมงทั้งสองกะถูกนับเข้าสัปดาห์ (FN-66 · BR-31) |
| **กะข้ามคืนคาบเกี่ยววันถัดไป** | `N 22:00–06:00` วันที่ 18 (= 1320→1800) + `H1 05:00–09:00` วันที่ 19 (= 1740→1980) | **`overnight_overlap` · ระดับห้าม** — เพราะ `1740 < 1800` (FN-12) |
| **กะข้ามคืนจบพอดีแล้วเริ่มพอดี** | `N 22:00–06:00` วันที่ 18 + `M 06:00–14:00` วันที่ 19 | **ไม่ทับ** (ปลายเปิด) → **ไม่เป็น `overlap`** · ถูกจับด้วย **กฎช่วงพัก** แทน — **ซึ่งในรอบนี้ยังตรวจไม่ได้เพราะ `min_rest_hours` เป็น `null`** (EC-04 · `05_RULES §5.4` · **ความเสี่ยง R-01**) |

### §3.0.3 ช่วงพักระหว่างกะ — รวมช่วงว่างของกะแยกช่วงด้วย

```
checkRest(intervals, minRestHours) → conflicts[]

  ถ้า minRestHours == null → return { skipped:true, reason:'noValue' }   ← §3.0.4

  เรียงช่วงตาม from
  สำหรับทุกคู่ (A, B) ที่ติดกันหลังเรียง:
      gapMinutes = B.from - A.to
      ถ้า gapMinutes >= 0 และ gapMinutes < minRestHours * 60:
          flag  = 'insufficient_rest'
          level = 'block'
```

**ข้อสำคัญ:** ลูปนี้เดินบน **ช่วงทั้งหมดของคนคนนั้นเรียงตามเวลา** — จึงครอบทั้ง **ช่วงพักข้ามวัน** และ **ช่วงว่างระหว่างกะแยกช่วงในวันเดียวกัน** โดยอัตโนมัติ (**BR-31** — ไม่ต้องเขียนสาขาแยก)

### §3.0.4 กฎที่ยังไม่มีค่าให้อ่าน — `noValue` ⭐⭐

**สถานการณ์จริงของรอบนี้:** HR Configuration เผยแพร่ 6 กลุ่มค่า (`leave_type` · `ot_rate` · `shift_pattern` · `holiday_calendar` · `period_rule` · `appraisal_cycle`) — **ไม่มีกลุ่ม `shift_rule` เลย** และ `T_hr_legal_minimum` มีเฉพาะขั้นต่ำ OT กับโควตาลาพักร้อน

```
resolveShiftRule(date, company_id) → {
    min_rest_hours:        number | null,
    max_hours_week:        number | null,
    max_consecutive_days:  number | null,
    freeze_days:           number | null,
    version_id:            uuid   | null      ← null เมื่อกลุ่มยังไม่ถูกเผยแพร่
}
```

**กติกาที่ห้ามผิด:**

| # | กติกา | ผลถ้าผิด |
|---|---|---|
| **NV-1** | **ค่าที่เป็น `null` → ข้ามการตรวจกฎนั้นทั้งข้อ** และคืน `{ skipped:true, reason:'noValue', key:'<ชื่อคีย์>' }` | ถ้าไม่ข้าม จะ throw หรือเทียบกับ `undefined` แล้วได้ผลสุ่ม |
| **NV-2** | **UI ต้องแสดงป้าย "ยังไม่มีค่าให้อ่าน" + ลิงก์ต้นทาง ทุกจุดที่กฎนั้นควรปรากฏ (5 ผิว)** | ผู้ใช้จะเข้าใจผิดว่าตารางผ่านกฎครบแล้ว — **นี่คือความเสี่ยงอันดับหนึ่งของ feature** (`00_OVERVIEW §0.14.1 R-7`) |
| **NV-3** | **ห้ามมีค่าคงที่ตัวเลขของเกณฑ์ใด ๆ ในโค้ด** — grep แล้วต้องไม่พบตัวเลขที่ทำหน้าที่เป็นเกณฑ์กฎหมาย | ผิด **P-8** ทันที |
| **NV-4** ⭐ | **ห้ามอ่านหรืออ้างถึง `ot_rate.cap_hours_week` เด็ดขาด** — นั่นคือ **เพดานของ OT คนละก้อนกับเพดานของกะปกติ** | จะได้เพดานที่ผิดความหมาย แล้วบล็อก/ปล่อยผิดทั้งระบบ |
| **NV-5** | **ตัวตรวจ "ชนกัน" (§3.0.2) ต้องทำงานเต็มรูปแบบเสมอ** เพราะไม่ต้องใช้ค่ากฎหมายเลย | ถ้าเผลอปิดทั้ง engine เมื่อค่าเป็น `null` จะสูญเสียการตรวจข้อที่รุนแรงที่สุด |
| **NV-6** | **สาขาการตรวจของทั้ง 4 กฎต้องมีอยู่จริงในโค้ด** และถูกข้ามด้วยเงื่อนไข `== null` — **ไม่ใช่ "ยังไม่เขียน"** | เมื่อต้นทางปล่อยคีย์มา ต้องทำงานทันทีโดยไม่ต้องแก้ตรรกะ (`§13 P3-01` ของ BRD) |

**4 กฎที่อยู่ในสถานะ `noValue` ตลอดรอบนี้:** `min_rest_hours` (BR-08) · `max_hours_week` (BR-09) · `max_consecutive_days` (BR-10) · `freeze_days` (BR-32) → **OQ-STD-R6 · OQ-R15**

### §3.0.5 การเผยแพร่ซ้ำ — ปฏิเสธรายวัน ไม่ใช่เตือนแล้วปล่อยผ่าน ⭐⭐

```
planPublish(versionId, changedCells[]) → { ok: cell[], rejected: [{ work_date, reason, employee_id }] }

  1) รวมวันที่ถูกแตะทั้งหมดจาก changedCells → dates[]
  2) เรียก Attendance ครั้งเดียวเป็นชุด:
        GET /api/v1/attendance/resolve?date=<min>&date_to=<max>&company_id=…&scope=company
     (ห้ามยิงทีละวัน — ดู §3.0.7 Throughput)
  3) สำหรับแต่ละ cell ที่จะเปลี่ยน:
        st = attendanceOf(cell.employee_id, cell.work_date)
        ถ้า st == null (อ่านไม่ได้)                     → **บล็อกทั้งการเผยแพร่** (EN-02)
        ถ้า st.day_status ∈ {confirmed, locked}          → rejected += { reason:'DAY_CONSUMED' }
        ถ้า st.period_status == 'closed'                 → rejected += { reason:'PERIOD_CLOSED' }
        มิฉะนั้น                                          → ok += cell
  4) ถ้า ok.length == 0 → **ไม่ออกเวอร์ชันใหม่** (คืน rejected ทั้งหมดให้ UI แสดง)
  5) มิฉะนั้น commit เฉพาะ ok:
        - ตรวจ st ซ้ำอีกครั้งภายใน transaction  ← กัน CA-04 (Attendance ยืนยันพอดีตอนกำลัง commit)
        - มินต์ roster_version ใหม่ · เวอร์ชันเดิม → superseded
        - เก็บ rejected_locked_dates[] ไว้กับเวอร์ชันใหม่ (เป็นบริบทการปฏิบัติตาม P-7)
```

| ทางที่ **ห้าม** เดิน | ทำไม |
|---|---|
| เตือนแล้วปล่อยผ่านทั้งชุด | ยอดที่ Attendance ยืนยันไปแล้วจะเปลี่ยน → Payroll ใช้ตัวเลขที่ไม่ตรงกับตาราง (ผิด **P-7 · AT-4**) |
| บล็อกทั้งเดือนเมื่อมีวันใดวันหนึ่งชน | ผู้จัดตารางจะแก้เดือนที่ยืนยันไปครึ่งเดือนไม่ได้เลย ทั้งที่ครึ่งหลังยังแก้ได้โดยชอบ |
| ถือว่า "อ่าน Attendance ไม่ได้" = "ไม่ถูกบริโภค" | **อันตรายที่สุด** — จะแก้ทับวันที่ยืนยันแล้วโดยไม่มีใครรู้ (EN-02) |

### §3.0.6 การตรวจคำขอสลับกะ — engine ตัวเดียวกัน ไม่มีทางลัด ⭐

```
validateSwap(swapRequest) → { block: [], warn: [], noValue: [] }

  1) โหลดสถานะปัจจุบันของทั้งสองฝ่ายจากเวอร์ชัน published ปัจจุบัน
  2) สร้าง "สถานะจำลองหลังสลับ" (simulated) โดยสลับ cell ของทั้งคู่
  3) baseline = ENG-ROSTER-CONFLICT.run(current, ทั้งสองคน)
     after    = ENG-ROSTER-CONFLICT.run(simulated, ทั้งสองคน)   ← **engine ตัวเดียวกับ T-2**
  4) newConflicts = after − baseline      ← เฉพาะข้อขัดแย้งที่ "เกิดใหม่จากการสลับ"
  5) เก็บลง swap_request.validation_result
```

| # | กติกา | ทำไม |
|---|---|---|
| **SW-1** | **ต้องเรียก `ENG-ROSTER-CONFLICT` ตัวเดียวกับการแก้ด้วยมือ** — ห้ามเขียนตรรกะตรวจชุดที่สอง | ถ้าเขียนสองชุด จะเกิดทางลัดที่ "สลับแล้วได้ตารางที่ผิดกฎ" ซึ่ง **C-17** ห้ามไว้ตรง ๆ (`06_TESTS IA-05`) |
| **SW-2** | **แสดงเฉพาะข้อขัดแย้งที่เกิดใหม่** (ข้อ 4) | ถ้าแสดงของเดิมด้วย หัวหน้าจะเห็นปัญหาที่ไม่ได้เกิดจากการตัดสินใจของตัวเอง แล้วจะเลิกอ่าน (`00_OVERVIEW` PR-08) |
| **SW-3** | **ตรวจของ *ทั้งสองฝ่าย*** — ไม่ใช่แค่ฝ่ายผู้ขอ | การสลับเปลี่ยนตารางของสองคน |
| **SW-4** | **`block` ไม่ว่าง → ปุ่มยืนยันปิด** และ **`confirmSwapRequest` ต้องตรวจซ้ำอีกชั้นตอนกดจริง** | กันกรณีตารางเปลี่ยนระหว่างที่คำขอรออยู่ (VR-23) |
| **SW-5** | **ถ้า `source_roster_version_id` ไม่ตรงกับเวอร์ชันปัจจุบัน → ต้องทวนผลตรวจใหม่ก่อนยืนยัน** | ตารางอาจถูกเผยแพร่ซ้ำระหว่างที่คำขอรออยู่ (EC-20) |

### §3.0.7 ลำดับการรัน engine กับ Throughput

```
runEngine(scope) — scope = { employeeIds[], dateFrom, dateTo }

  1) ดึง cell ของ scope + **ขยายขอบ 1 วันทั้งสองด้าน**   ← จำเป็นสำหรับ overnight_overlap
  2) resolveShiftRule(date, company)  ← 1 ครั้งต่อการรัน (cache ภายในวัน · C-3)
  3) ต่อพนักงาน 1 คน:
        intervals = cells.map(toTimeline)              §3.0.1
        conflicts += detectOverlap(intervals)          §3.0.2   ← ทำงานเสมอ
        conflicts += checkRest(intervals, minRest)     §3.0.3   ← ข้ามถ้า noValue
        conflicts += checkWeeklyHours(cells, maxWeek)           ← ข้ามถ้า noValue
        conflicts += checkConsecutiveDays(cells, maxDays)       ← ข้ามถ้า noValue
        conflicts += checkFreeze(cells, freezeDays)             ← ข้ามถ้า noValue
        conflicts += checkLeave(cells)     ← block  (อ่าน Leave · display-only)
        conflicts += checkHoliday(cells)   ← warn   (อ่าน holiday_calendar)
        conflicts += checkOtFlag(cells)    ← info   (อ่าน OT · ไม่บล็อก)
        conflicts += checkAfterExit(cells) ← block  (Employee Master)
  4) derive conflict_level ต่อ cell:  มี block ใด ๆ → 'block' · มี warn → 'warn' · มี info → 'info'
```

| ข้อกำหนดด้านประสิทธิภาพ | ค่า | ทำไม |
|---|---|---|
| แก้ 1 ช่อง | **รันเฉพาะ scope ของคนคนนั้น ± 1 วัน** ไม่ใช่ทั้งเดือนทุกคน | SLA-02 ≤ 300 มิลลิวินาที |
| ทาช่วง | รัน scope ของทุกคนที่ถูกแตะ ± 1 วัน · **รันครั้งเดียวหลังจบทั้งช่วง** | SLA-03 ≤ 2 วินาที |
| กางตารางใหม่ | รันทั้งเดือน 1 ครั้ง | SLA-01 ≤ 5 วินาที |
| การอ่านต้นทาง (Attendance/Leave/OT) | **เป็นชุด (batch) เสมอ · ห้ามยิงทีละวันทีละคน** | ตาราง 100 คน × 31 วัน = 3,100 คำขอถ้ายิงทีละช่อง |

---

## §3.1 Functions (60 ตัว · camelCase)

### กลุ่ม A — การกางตารางกับการอ่านค่านโยบาย

| # | Function | Input | Output | สาระ | trace |
|---|---|---|---|---|---|
| **F-01** | `generateRoster` | `{company_id, period_month, scope_team, mode, rotation_option?}` | `roster_version` + `cells[]` | สร้างตารางร่างของเดือน · `mode ∈ {pattern, rotation, copy_previous}` · **deterministic ทุกโหมด** | FN-01 · FN-57 |
| **F-02** | `resolveHrConfig` | `{date, company_id, group}` | `{value, version_id}` | เรียก `GET /hr-config/resolve` · **ส่ง `date` ของช่องเสมอ** · cache ภายในวัน · ล้างเมื่อได้ `hrconfig.effective` | **C-1 · C-3** · BR-01 · BR-02 |
| **F-03** | `expandPattern` | `{shift_patterns[], holiday_calendar, employees[], month, rotation_option?}` | `cells[]` | กางกะตาม `work_days[]` · โหมด `rotation` หมุนตาม `seq` + `cycle_weeks` + `start_offset` | FN-01 · FN-65 |
| **F-04** | `captureConfigVersions` | `{resolved[]}` | `config_version_ids` | รวมก้อนเวอร์ชัน 4 กลุ่ม · **`shift_rule` เป็น `null` ได้** | **C-2** · FN-02 |
| **F-05** | `copyPreviousMonth` | `{source_month, target_month}` | `cells[]` | ยกรูปแบบกะมา แล้ว **resolve ค่านโยบายใหม่ตามวันของเดือนปลายทาง** (ไม่ลอก `version_id` เก่า) | FN-03 |
| **F-06** | `activeShiftsAt` | `{date, company_id}` | `shift[]` | คืนเฉพาะกะที่ `active` ณ วันนั้น — **กะ `inactive` ไม่อยู่ในผล แต่ช่อง snapshot เดิมยังแสดงได้** | **C-5** · BR-04 · FN-09 |
| **F-07** | `listEmployeesInScope` | `{company_id, scope_team, actor}` | `employee[]` | เรียก Policy Center · คืนคนที่ actor เห็นได้ | BR-25 · FN-10 |
| **F-08** | `resolveShiftRule` | `{date, company_id}` | 4 ค่า + `version_id` (ทุกตัวเป็น `null` ได้) | **§3.0.4** — คืน `noValue` เมื่อต้นทางยังไม่เผยแพร่ · **ห้ามอ่าน `ot_rate.cap_hours_week`** | **BR-11** · FN-16 |

### กลุ่ม B — การแก้ช่อง

| # | Function | Input | Output | สาระ | trace |
|---|---|---|---|---|---|
| **F-09** | `applyShiftToCell` | `{version_id, employee_id, work_date, shift_code?, slot_seq?}` | `cell` + `history_row` | ใส่/เปลี่ยนกะ 1 ช่อง · `slot_seq` ที่ว่างถัดไปเมื่อเป็นกะแยกช่วง · เขียน snapshot ครบ + `shift_pattern_version_id` | FN-05 · FN-06 · **FN-66** |
| **F-10** | `paintRange` | `{version_id, employees[], dateFrom, dateTo, shift_code?}` | `cells[]` + `skipped[]` | ทาสี่เหลี่ยม · **ข้ามช่องที่แก้ไม่ได้พร้อมนับจำนวน** · รัน engine ครั้งเดียวหลังจบ | FN-07 |
| **F-11** | `clearCell` | `{version_id, employee_id, work_date, slot_seq}` | `cell` (ว่าง) + `history_row` | ล้างกะ — **เป็นสถานะใหม่ + แถวประวัติ ไม่ใช่การลบข้อมูล** | BR-26 · FN-08 |
| **F-12** | `guardCell` | `{employee, work_date, cell_state}` | `{editable:boolean, reason?}` | ด่านเดียวที่ทุกการแก้ต้องผ่าน: งวดปิด · วันถูกบริโภค · หลัง `exit_date` · เวอร์ชันไม่ใช่ `draft`/`published` | BR-16 · **BR-30** · FN-52 |
| **F-13** | `filterGrid` | `{cells[], query, dept?, shift?, onlyConflict?}` | `rows[]` | กรองแถวคน · คืน empty state เมื่อไม่พบ | FN-63 |
| **F-14** | `runEngine` | `{scope}` | `cells[] with conflict_flags/level` | **§3.0.7** — เรียก `ENG-ROSTER-CONFLICT` | FN-05 · FN-07 |

### กลุ่ม C — ตัวตรวจข้อขัดแย้ง (บาง function เป็นเปลือกบาง ๆ ของ engine)

| # | Function | Engine ที่เรียก | สาระ | trace |
|---|---|---|---|---|
| **F-15** | `detectOverlapConflicts` | **ENG-ROSTER-CONFLICT** | **§3.0.2** — `overlap` / `overnight_overlap` · ระดับ `block` · **ชี้ทั้งสองช่องเสมอ** | **BR-06 · BR-07** · FN-11 · FN-12 |
| **F-16** | `checkMinimumRest` | **ENG-ROSTER-CONFLICT** | **§3.0.3** — `insufficient_rest` · `block` · **ข้ามเมื่อ `noValue`** · ครอบช่วงว่างของกะแยกช่วง | BR-08 · **BR-31** · FN-13 |
| **F-17** | `checkWeeklyHours` | **ENG-ROSTER-CONFLICT** | Σ `hours_per_day` ต่อสัปดาห์ (**รวมทุก `slot_seq`**) เทียบเพดาน · `warn` · ข้ามเมื่อ `noValue` · คืน **ยอดสะสม / เพดาน / ส่วนที่เกิน** ครบสามค่า | BR-09 · FN-14 |
| **F-18** | `checkConsecutiveDays` | **ENG-ROSTER-CONFLICT** | นับวันที่มีกะติดกัน · `warn` · ข้ามเมื่อ `noValue` · **ชี้ช่วงวันที่ติดกัน** | BR-10 · FN-15 |
| **F-19** | `checkLeaveOverlap` | `leave-resolve-client` | อ่านวันลาที่อนุมัติแล้ว → `on_leave` · **`block`** · เก็บ `leave_ref` display-only · **ห้ามคำนวณวันลาเอง ห้ามเขียนกลับ** | BR-12 · FN-17 |
| **F-20** | `checkPublicHoliday` | `hr-config-resolve-client` | วันในปฏิทินวันหยุด → `public_holiday` · **`warn` ไม่ใช่ `block`** | BR-12 · FN-18 |
| **F-21** | `checkOtFlag` | `ot-resolve-client` | อ่าน `GET /ot/resolve` → ธง `has_ot` · **`info` ไม่บล็อก** · **กรองใบที่ `withdrawn` ออก** · **ไม่อ่าน `multiplier` · ไม่คำนวณชั่วโมง** | **BR-13 · OT-4 · OT-6** · FN-19 |
| **F-22** | `buildConflictPanel` | — | จัดกลุ่มผลตรวจเป็นรายการ · แยก `block`/`warn`/`noValue` · ให้จุดกระโดดไปช่อง | BR-14 · FN-20 |
| **F-53** | `checkFreezeHorizon` | **ENG-ROSTER-CONFLICT** | วันที่เหลือเวลาน้อยกว่า `freeze_days` → `freeze_window` · **`warn`** · **ข้ามเมื่อ `noValue`** | BR-32 · FN-69 |
| **F-54** | `checkAfterExit` | — | มีกะในวันหลัง `employee.exit_date` → `after_exit` · `block` | BR-30 · FN-52 |

### กลุ่ม D — เวอร์ชันกับการเผยแพร่

| # | Function | Input | Output | สาระ | trace |
|---|---|---|---|---|---|
| **F-23** | `checkPublishGate` | `{version_id}` | `{pass, blockers[]}` | **ด่าน 4 ข้อ:** ไม่มี `block` ค้าง · `warn` รับทราบครบ · งวดยังเปิด · ค่านโยบายอ่านได้ · คืน **ช่องแรกที่ผิด** ให้ UI กระโดด | **BR-14** · FN-24 |
| **F-24** | `planPublish` | `{version_id, changedCells[]}` | `{ok[], rejected[]}` | **§3.0.5** — แยกผลรายวัน · **ปฏิเสธเฉพาะวันที่ถูกบริโภค** | **BR-16** · FN-27 |
| **F-25** | `publishRoster` | `{version_id, actor}` | `roster_version(published)` | T-3 · มินต์เวอร์ชัน · เปิด read model · **emit N1 + E1** | FN-23 · §0.16 |
| **F-26** | `acknowledgeWarnings` | `{version_id, items[], actor}` | `warning_ack_*` | บันทึก **ใครรับทราบอะไรเมื่อไร** เป็นรายการจริง | BR-14 · BR-26 · FN-25 |
| **F-27** | `applyManualEdits` | `{version_id, edits[], reason}` | `pendingChanges[]` | รวมการแก้หลังเผยแพร่ · **`reason` บังคับ** | VR-09 · FN-26 |
| **F-28** | `republishRoster` | `{version_id, publish_note, actor}` | `roster_version ใหม่` + `superseded เดิม` | T-4 · เรียก `F-24` ก่อนเสมอ · **`publish_note` บังคับ** · **emit N2 + E2 (`adjust_kind`)** | **BR-15 · BR-17** · FN-26 · FN-29 |
| **F-29** | `discardDraft` | `{version_id, actor}` | `roster_version(discarded)` | T-6 · **เฉพาะร่างที่ยังไม่เคยเผยแพร่** · ยังอยู่ในห่วงโซ่ | BR-26 · FN-22 |
| **F-30** | `onPeriodClosed` | `{event: hrconfig.period_closed}` | `roster_version(locked)` | T-5 · **ระบบเป็นผู้กระทำ** · เขียนประวัติ `upstream_event` · **ไม่มีทางกลับจากหน้านี้** | **P-7** · BR-16 · FN-28 |
| **F-31** | `diffChangedEmployees` | `{old_version, new_version}` | `employee_id[]` + จำนวนวันที่เปลี่ยนต่อคน | **คำนวณก่อน emit N2 เสมอ** — **ห้าม emit ให้ทุกคนในตาราง** | **BR-17** · FN-29 |
| **F-32** | `freezePublishedValues` | `{version_id}` | — | ตารางที่ `published` แช่ค่ากะไว้พร้อม `shift_pattern_version_id` รายช่อง · ร่าง resolve สดทุกครั้ง | BR-02 · FN-30 |

### กลุ่ม E — คำขอสลับกะ

| # | Function | Input | Output | สาระ | trace |
|---|---|---|---|---|---|
| **F-33** | `createSwapRequest` | `{requester, counterpart, dates, reason}` | `swap_request(requested)` | W-1 · เก็บ snapshot กะทั้งสองฝั่ง + `source_roster_version_id` · **emit N3** | FN-31 |
| **F-34** | `validateSwapCounterpart` | `{requester, counterpart, dates}` | `{ok, reason?}` | ตรวจ 4 กรณี: **ตัวเอง** · ไม่มีกะในวันนั้น · นอกขอบเขต · ตารางยังเป็นร่าง — **คืนเหตุรายกรณี** | **SoD** · VR-14…VR-17 · FN-32 |
| **F-35** | `validateSwapDates` | `{dates[]}` | `{ok, reason?}` | ตรวจว่าวันของทั้งสองฝั่งยังแก้ได้ (ล็อก / งวดปิด / ถูกบริโภค) | BR-16 · VR-18 · FN-33 |
| **F-36** | `validateSwap` | `{swap_request}` | `validation_result` | **§3.0.6** — เรียก **ENG-ROSTER-CONFLICT ตัวเดียวกับ T-2** | **BR-22 · C-17** · FN-35 |
| **F-37** | `acceptSwapRequest` | `{swap_id, actor}` | `swap_request(accepted)` | W-2 · เรียก `F-36` แล้ว **emit N4** | FN-34 |
| **F-38** | `canConfirmSwap` | `{swap_request, actor}` | `boolean` | ปุ่มยืนยันปรากฏเมื่อ actor = ผู้ยืนยันจริง **และ** `validation_result.block` ว่าง | VR-21 · VR-22 · FN-36 |
| **F-39** | `confirmSwapRequest` | `{swap_id, actor}` | `roster_version ใหม่` | W-3 · **ตรวจซ้ำ (SW-4/SW-5)** → **สลับสองช่องใน transaction เดียว** → เรียก `F-28` (T-4) · **emit N5 + E2(`shift_swap`)** | **BR-22** · FN-37 |
| **F-40** | `rejectSwapRequest` | `{swap_id, actor, reason}` | `swap_request(rejected)` | W-4 · **`reason` บังคับ** · บันทึก `rejected_by_role` · **emit N5** | BR-24 · FN-34 · FN-39 |
| **F-41** | `resolveConfirmer` | `{requester_id}` | `employee_id` | **เรียก `ENG-ROLESCOPE-01` เท่านั้น** — **ไม่มีรายชื่อ/ตำแหน่งในโค้ด · ไม่เรียก DOA เลย** · คืน `null` เมื่อสายชี้กลับมาที่ผู้ขอเอง (**OQ-R19**) | **BR-23** · FN-38 |
| **F-42** | `cancelSwapRequest` | `{swap_id, actor}` | `swap_request(cancelled)` | W-5 · เฉพาะผู้ขอ · เฉพาะก่อน `confirmed` | FN-40 |
| **F-60** | `expireStaleSwapRequests` | (scheduler รายวัน) | `swap_request(expired)[]` | W-6 · **เงื่อนไข = ถึงวันของกะแล้วยังไม่มีข้อสรุป · ไม่มีจำนวนวันเป็นตัวเลขในโค้ด** · **emit N6** | BR-29 · FN-41 |

### กลุ่ม F — สิ่งที่เผยแพร่ให้ปลายทาง

| # | Function | Input | Output | สาระ | trace |
|---|---|---|---|---|---|
| **F-43** | `resolveRosterDay` ⭐ | `{employee_id, work_date, company_id, consumer}` | `day snapshot[]` (หลายแถวเมื่อมีกะแยกช่วง) | **หัวใจของ `§0.13.2`** — คืน `shift` object 8 ฟิลด์ + `roster_version_id` + `shift_pattern_version_id` · **กรอง `roster_status='published'` ที่ระดับ query** | **BR-18** · FN-42 · FN-43 · FN-46 |
| **F-44** | `emptyShiftResult` | `{reason}` | `{shift:null, reason}` | **คืน `null` เสมอเมื่อไม่มีกะ** — 4 เหตุ: `NO_ROSTER_AT_DATE` · `NO_SHIFT_FOR_EMPLOYEE_DAY` · `ROSTER_NOT_PUBLISHED` · `MODULE_NOT_LINKED` · **ห้ามเดา ห้ามส่งกะมาตรฐาน** | **BR-19** · FN-44 |
| **F-45** | `checkModuleLinkage` | `{company_id, consumer}` | `{linked:boolean}` | ตรวจสวิตช์ก่อนคืนค่า — **ปิดแล้วคืน `{linked:false, shift:null}` จริง ไม่ใช่ป้าย** | BR-19 · FN-45 |
| **F-46** | `computePlannedHours` | `{cells[], period}` | `planned_hours` + `shift_days` + `off_days` + บริบท | Σ `hours_per_day` · **ติดป้าย "ชั่วโมงตามแผน" ทุกจุดที่แสดง** · **ห้ามคำนวณชั่วโมงจริง** | **BR-21 · BR-27** · FN-48 |
| **F-47** | `registerWhereUsed` | (ตอน deploy) | — | `POST` usage ไป **HR Config 4 กลุ่ม** (รวม `shift_rule` แม้ยังไม่มีค่า) + Attendance + Leave + OT | **C-6 · AT-7 · OT-7** · FN-49 |
| **F-50** | `bindCompanyScope` | `{actor}` | `company_id` | ผูก `company_id` เข้าทุกคำขอ · **ปฏิเสธคำขอที่ไม่มี** | BR-28 · VR-26 · FN-54 |

### กลุ่ม G — ประวัติ · สิทธิ์ · การรับทราบ · การประกาศ

| # | Function | Input | Output | สาระ | trace |
|---|---|---|---|---|---|
| **F-48** | `applyScopeFilter` | `{query, actor}` | `query'` | เติมเงื่อนไขขอบเขตของ Policy Center **ที่ระดับ query** — ไม่ใช่ซ่อนปุ่ม | BR-25 · FN-51 |
| **F-49** | `pushHistory` | `{action, target_ref, before, after, reason, actor}` | `history_row` | **เพิ่มอย่างเดียว** · `actor` เป็น `system` ได้เฉพาะ T-5 กับ W-6 | **BR-26** · FN-53 |
| **F-51** | `requireReason` | `{field, value}` | `{ok, message?}` | บังคับเหตุผล 3 จุด + กัน double-submit ผ่านสถานะ busy | VR-09 · VR-13 · VR-19 · VR-20 · VR-25 · FN-64 |
| **F-52** | `saveCellNote` | `{cell_ref, note, actor}` | `cell` + `history_row` | หมายเหตุ ≤200 ตัวอักษร · **ห้ามมีจำนวนเงิน** · เข้าประวัติ | VR-08 · FN-68 |
| **F-55** | `acknowledgeMyShifts` | `{version_id, employee_id, status, note?}` | `roster_ack` | พนักงานกด **รับทราบ** / **แจ้งว่าทำไม่ได้** (note บังคับ) | BR-33 · VR-24 · FN-67 |
| **F-56** | `resetAckOnRepublish` | `{old_version, new_version}` | — | **รีเซ็ตสถานะรับทราบเฉพาะคนที่กะเปลี่ยน** — คนที่กะไม่เปลี่ยนคงสถานะเดิม | `00_OVERVIEW` PR-09 · FN-67 |
| **F-57** | `countUnacknowledged` | `{version_id}` | `int` | ตัวนับให้หัวหน้า — **ไม่บล็อกอะไร** | BR-33 · FN-67 |
| **F-58** | `emitNotification` | `{event_id, ref, vars}` | — | เรียก **ENG-NOTIFY เท่านั้น** · **ห้ามเลือกช่องทางเอง ห้ามเช็ค preference เอง** · N1/N2 ห้ามยิงพร้อมกัน · N5 ยิงครั้งเดียวต่อคำขอ | **§0.16.1** · FN-50 |
| **F-59** | `emitImpactEvent` | `{event, payload}` | — | เรียก **ENG-CSQ เท่านั้น** · **EC ท่อเดียว · `kind: estimated`** · สร้าง `idempotency_key` · **payload ห้ามมีชื่อดิบ ห้ามมีจำนวนเงิน** | **§0.16.2** · BR-27 |

---

## §3.2 Engines (7 ตัว · kebab-case)

| Engine | สถานะ | หน้าที่ | Input → Output | เรียกจาก |
|---|---|---|---|---|
| **`roster-conflict-engine`** ⭐ **NEW** | **candidate — เสนอ Architect ลง CUBIC** | **§3.0.1–§3.0.4 · §3.0.7** — แปลงเส้นเวลา · ตรวจ 9 ชนิดข้อขัดแย้ง · derive `conflict_level` · คืน `noValue` เมื่อเกณฑ์เป็น `null` | `{cells[], employees[], shiftRule, holidays, leaves, otRefs, exitDates}` → `{conflicts[], levels{}, skipped[]}` | `F-14` `F-15` `F-16` `F-17` `F-18` `F-53` · **และ `F-36` (การสลับกะ) — ตัวเดียวกัน** |
| **`roster-publish-planner-engine`** ⭐ **NEW** | **candidate** | **§3.0.5** — แยกผลรายวันเป็นผ่าน/ถูกปฏิเสธ ตามสถานะปลายทาง | `{cells[], attendanceStates{}, periodStates{}}` → `{ok[], rejected[]}` | `F-24` |
| **`roster-version-chain-engine`** ⭐ **NEW** | **candidate** | มินต์เวอร์ชันใหม่ · ผูก `supersedes`/`superseded_by` · **รับประกันว่าห่วงโซ่ไม่ขาด** · คำนวณ diff ระหว่างเวอร์ชัน | `{currentVersion, changes[]}` → `{newVersion, supersededVersion, diff[]}` | `F-25` `F-28` `F-31` |
| `hr-config-resolve-client` | existing | เรียก `resolve(date, company, group)` · จัดการ cache ภายในวัน | `{date, company_id, group}` → `{value, version_id}` | `F-02` `F-06` `F-08` `F-20` |
| `attendance-resolve-client` | existing | อ่านสถานะวัน/งวดเป็นชุด | `{dates, company_id, employees}` → `{day_status, period_status}[]` | `F-24` `F-12` |
| `leave-resolve-client` | existing | อ่านวันลาที่อนุมัติแล้ว | `{dates, employees}` → `leave_ref[]` | `F-19` |
| `ot-resolve-client` | existing | อ่านใบ OT ของวัน · **กรอง `withdrawn` ออก** | `{dates, employees}` → `ot_ref[]` | `F-21` |
| `notification-engine` (ENG-NOTIFY) | existing | ส่งการแจ้งเตือน | `{event_id, ref, vars}` → — | `F-58` |
| `impact-valuation-engine` (ENG-CSQ) | existing | รับ event ผลกระทบ | `{profile, event, payload}` → — | `F-59` |
| `role-scope-engine` (ENG-ROLESCOPE-01) | existing | ขอบเขตการเห็น + สายบังคับบัญชา | `{actor}` → `{scope, supervisor_of}` | `F-07` `F-41` `F-48` |

> **Engine Iron Rules ที่ตรวจแล้ว (Phase 3.5 Section F):**
> · engine ทั้ง 3 ตัวใหม่ **ไม่มีการอ้างถึง `req` / `res` / header / status code ใด ๆ**
> · input/output เป็น **pure object** ทั้งหมด — ไม่มี side effect นอกจากค่าที่คืน
> · **feature ไม่ข้าม API ไปเรียก engine ตรง** — ทุกทางเข้าผ่าน Function
> · **`roster-conflict-engine` ต้องถูกเรียกจากทั้ง `F-14` และ `F-36`** — เป็นข้อกำหนด ไม่ใช่คำแนะนำ (`06_TESTS IA-05`)

## §3.3 API ↔ Logic Trace Table (Phase 3.5 Anchor · R8)

| API | Method | Function / Engine ที่ถูกเรียก | mutation? |
|---|---|---|---|
| `API-01` สร้างตารางร่าง | POST | `F-01` → `F-02` `F-03` `F-04` `F-05` · `F-14` | ✅ |
| `API-02` อ่านกริด | GET | `F-06` `F-07` `F-13` `F-48` · `F-19` `F-20` `F-21` | — |
| `API-03` แก้ช่อง | PATCH | `F-12` → `F-09` / `F-11` / `F-52` → `F-14` → `F-49` | ✅ |
| `API-04` ทาช่วง | POST | `F-12` → `F-10` → `F-14` → `F-49` | ✅ |
| `API-05` รับทราบคำเตือน | POST | `F-26` → `F-49` | ✅ |
| `API-06` เผยแพร่ | POST | `F-23` → `F-25` → `F-32` `F-49` `F-58`(N1) `F-59`(E1) | ✅ |
| `API-07` เผยแพร่ซ้ำ | POST | `F-23` → **`F-24`** → `F-28` → `F-31` `F-56` `F-49` `F-58`(N2) `F-59`(E2) | ✅ |
| `API-08` ทิ้งร่าง | POST | `F-29` → `F-49` | ✅ |
| `API-09` รับทราบกะของฉัน | POST | `F-55` → `F-49` | ✅ |
| `API-10` อ่านสถานะการเผยแพร่ | GET | `F-23` `F-24`(dry-run) `F-27` | — |
| `API-11` ยื่นคำขอสลับกะ | POST | `F-34` `F-35` → `F-33` → `F-49` `F-58`(N3) | ✅ |
| `API-12` ตอบรับคำขอ | POST | `F-37` → **`F-36`** → `F-49` `F-58`(N4) | ✅ |
| `API-13` ปฏิเสธ/ถอนคำขอ | POST | `F-51` → `F-40` / `F-42` → `F-49` `F-58`(N5) | ✅ |
| `API-14` ยืนยันคำขอ | POST | `F-38` → **`F-36`(ตรวจซ้ำ)** → `F-39` → `F-28` → `F-49` `F-58`(N5) `F-59`(E2) | ✅ |
| `API-15` รับ event จากต้นทาง | POST (internal) | `F-30` (period_closed) · `F-02` cache clear (effective) · `F-06` (deactivated) → `F-49` | ✅ |
| `API-16` อ่านห่วงโซ่เวอร์ชัน | GET | `F-32` + `roster-version-chain-engine.diff` | — |
| `API-17` งานตามเวลา (scheduler) | internal | `F-60` → `F-49` `F-58`(N6) | ✅ |
| **`API-18`** อ่าน read model `day` ⭐ | GET | **`F-45` → `F-43` / `F-44`** | — |
| `API-19` อ่าน read model `period` | GET | `F-45` → `F-46` | — |
| `API-20` ตั้ง Module Linkage | PUT | `F-45` (เขียนค่า) → `F-49` | ✅ |
| `API-21` ลงทะเบียน where-used | POST | `F-47` | ✅ (ต้นทาง) |
| `API-22` อ่านประวัติ | GET | `F-48` (กรองขอบเขต) | — |

**R8 check:**
- ✅ **ทุก mutation API (14 ตัว) มี ≥1 Function/Engine ใน trace**
- ✅ **ทุก Function ใน §3.1 (60 ตัว) ถูก trace อย่างน้อย 1 API** (function ที่ไม่ถูกเรียกตรงจาก API — `F-15…F-18` · `F-53` `F-54` — ถูกเรียกผ่าน `F-14`/`F-36` ซึ่ง trace อยู่แล้ว)
- ✅ **Engine ทั้ง 10 ตัวถูก trace ผ่าน Function** — ไม่มี orphan
- ✅ **ไม่มี business logic ใน `02_API`** — ทุก endpoint เป็นเปลือก HTTP ล้วน (Phase 3.5 Section G)

## §3.4 ลำดับการทำงานที่ต้องเป็นแบบนี้เท่านั้น (sequence ที่ผิดแล้วพัง)

| # | ลำดับ | ถ้าสลับลำดับจะเกิดอะไร |
|---|---|---|
| SQ-1 | `F-12 guardCell` → **แล้วค่อย** `F-09/F-10/F-11` | ถ้าแก้ก่อนแล้วค่อยตรวจ จะเขียนทับวันที่ถูกบริโภคไปแล้ว |
| SQ-2 | `F-09/F-10/F-11` → **แล้วค่อย** `F-14 runEngine` | ผลตรวจจะเป็นของสถานะก่อนแก้ |
| SQ-3 | `F-23 checkPublishGate` → **แล้วค่อย** `F-24 planPublish` → **แล้วค่อย** `F-28 republish` | ถ้ามินต์เวอร์ชันก่อนตรวจ จะได้เวอร์ชันขยะเมื่อทุกวันถูกปฏิเสธ |
| SQ-4 | `F-24 planPublish` **ตรวจ `day_status` ซ้ำภายใน transaction** ก่อน commit | Attendance อาจยืนยันพอดีระหว่างที่ผู้ใช้กำลังกด (CA-04) |
| SQ-5 | `F-31 diffChangedEmployees` → **แล้วค่อย** `F-58 emit N2` | ถ้า emit ก่อน diff จะส่งให้ทุกคนในตาราง (ผิด **BR-17**) |
| SQ-6 | `F-36 validateSwap` **ถูกเรียกซ้ำ** ที่ `F-39 confirmSwapRequest` ก่อน commit | ตารางอาจถูกเผยแพร่ซ้ำระหว่างที่คำขอรออยู่ (SW-5) |
| SQ-7 | `F-39` สลับสองช่อง → **แล้วค่อย** `F-28` มินต์เวอร์ชัน — **ทั้งหมดใน transaction เดียว** | ถ้าแยก transaction จะเกิดสภาพ "สลับครึ่งเดียว" ซึ่ง **C-18** ห้าม |
| SQ-8 | `F-28 republish` สำเร็จ → **แล้วค่อย** `F-56 resetAckOnRepublish` | ถ้ารีเซ็ตก่อน แล้ว republish ล้ม จะได้สถานะรับทราบที่หายไปโดยไม่มีเหตุ |
| SQ-9 | `F-25/F-28` commit สำเร็จ → **แล้วค่อย** `F-58` และ `F-59` | **ห้าม emit ก่อน commit** — ถ้า commit ล้มจะประกาศเหตุการณ์ที่ไม่เคยเกิด |
| SQ-10 | `F-58` (NOTIFY) และ `F-59` (CSQ) เป็น **สองการเรียกแยกกัน** ที่จุดเดียวกัน | เป็นคนละระบบคนละ catalog (`§0.16.3`) — **ไม่ใช่การยิงซ้ำ** |
