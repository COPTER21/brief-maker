# 02_API — F-HR-ROSTER · Shift & Roster (จัดกะ)

> **Audience: BE dev (ชั้น HTTP)**
> **กฎเหล็ก:** **ชั้นนี้ห้ามมี business logic** — ทุก endpoint เป็นเปลือก HTTP ที่ผูก request → เรียก Function/Engine ใน `03_LOGIC` → แปลงผลเป็น response (Logic Placement Matrix · Phase 3.5 Section G)
> **Convention:** path `/api/v1/roster/...` · field `snake_case` · error code `UPPER_SNAKE` · Function `camelCase` · Engine `kebab-case`

## §2.0 กติกาที่ใช้กับทุก endpoint

| # | กติกา | ผลถ้าไม่ทำ |
|---|---|---|
| **AP-1** | **ทุกคำขอต้องมี `company_id`** (จาก login หรือ query) — คำขอที่ไม่มีถูกปฏิเสธ | ค่านโยบายผิดบริษัท (BR-28 · VR-26) |
| **AP-2** | **ทุกคำขอที่เกี่ยวกับวัน ต้องส่ง `date`** — ไม่ส่ง = `400 ERR_ROSTER_DATE_REQUIRED` | **C-1 · AT-1 · OT-1 · RO-3** |
| **AP-3** | **ทุกคำตอบที่มีข้อมูลตาราง ต้องมี `roster_version_id`** | consumer เดาไม่ได้ว่าค่าเก่าหรือยัง (RO-4) |
| **AP-4** | **RLS ที่ระดับ query** — คำขอข้ามผู้เช่า/ข้ามขอบเขตคืน **404 ไม่ใช่ 403** | ไม่เปิดเผยว่ามีข้อมูลอยู่ (`05_RULES §5.3`) |
| **AP-5** | **ทุก mutation ต้อง idempotent ผ่าน `Idempotency-Key` header** | กดซ้ำแล้วได้เวอร์ชันซ้ำ (VR-25) |
| **AP-6** | **ไม่มี endpoint ใดเขียนไปยัง HR Config / Attendance / Leave / OT** — ตรวจได้จากรายการทั้งหมดใน §2.1–§2.3 | **C-4 · AT-5 · OT-5** |
| **AP-7** | **ไม่มี write endpoint สำหรับ consumer** (ยกเว้น `usage` ซึ่งเป็นการลงทะเบียน) | **BR-20 · RO-5** (`06_TESTS IA-09`) |
| **AP-8** | **ไม่มี field ใดใน request/response เป็นจำนวนเงินหรือเลขความต้องการกำลังคน** | **BR-27** |

## §2.1 Endpoint ภายใน feature (ผู้ใช้เรียกจากหน้าจอ)

| # | Method · Path | ทำอะไร | Function หลัก | mutation |
|---|---|---|---|---|
| **API-01** | `POST /api/v1/roster/versions` | สร้างตารางร่างของเดือน (โหมด `pattern` / `rotation` / `copy_previous`) | `F-01` | ✅ |
| **API-02** | `GET /api/v1/roster/versions/:id/grid` | อ่านกริดของเวอร์ชัน (พร้อมผลตรวจ · ธง OT/ลา/วันหยุด · ตัวกรอง) | `F-13` `F-48` | — |
| **API-03** | `PATCH /api/v1/roster/versions/:id/cells` | ใส่/เปลี่ยน/ล้างกะ 1 ช่อง หรือ ใส่หมายเหตุ | `F-12` → `F-09`/`F-11`/`F-52` | ✅ |
| **API-04** | `POST /api/v1/roster/versions/:id/cells/paint` | ทาช่วงหลายช่อง | `F-12` → `F-10` | ✅ |
| **API-05** | `POST /api/v1/roster/versions/:id/warnings/ack` | รับทราบคำเตือน | `F-26` | ✅ |
| **API-06** | `POST /api/v1/roster/versions/:id/publish` | เผยแพร่ครั้งแรก (T-3) | `F-23` → `F-25` | ✅ |
| **API-07** | `POST /api/v1/roster/versions/:id/republish` | เผยแพร่ซ้ำ (T-4) | `F-23` → **`F-24`** → `F-28` | ✅ |
| **API-08** | `POST /api/v1/roster/versions/:id/discard` | ทิ้งร่าง (T-6) | `F-29` | ✅ |
| **API-09** | `POST /api/v1/roster/versions/:id/ack` | พนักงานรับทราบกะ / แจ้งว่าทำไม่ได้ | `F-55` | ✅ |
| **API-10** | `GET /api/v1/roster/versions/:id/publish-plan` | ดูผลของการเผยแพร่ซ้ำแบบ dry-run (ผ่าน/ถูกปฏิเสธ รายวัน) | `F-23` `F-24` `F-27` | — |
| **API-11** | `POST /api/v1/roster/swaps` | ยื่นคำขอสลับกะ (W-1) | `F-34` `F-35` → `F-33` | ✅ |
| **API-12** | `POST /api/v1/roster/swaps/:id/accept` | คู่สลับตอบรับ (W-2) | `F-37` → **`F-36`** | ✅ |
| **API-13** | `POST /api/v1/roster/swaps/:id/reject` · `/cancel` | ปฏิเสธ (W-4) · ถอน (W-5) | `F-40` / `F-42` | ✅ |
| **API-14** | `POST /api/v1/roster/swaps/:id/confirm` | หัวหน้ายืนยัน (W-3 → T-4) | `F-38` → `F-36` → `F-39` | ✅ |
| **API-16** | `GET /api/v1/roster/versions?period_month=&scope_team=` | ห่วงโซ่เวอร์ชัน + diff ระหว่างเวอร์ชัน | `F-32` + `roster-version-chain-engine` | — |
| **API-20** | `PUT /api/v1/roster/linkage` | ตั้ง Module Linkage (HR Admin) | `F-45` | ✅ |
| **API-22** | `GET /api/v1/roster/history?version_id=&swap_id=` | อ่านประวัติ (append-only) | `F-48` | — |

## §2.2 Endpoint ภายในระบบ (ไม่ใช่ผู้ใช้เรียก)

| # | Method · Path | ทำอะไร | Function | หมายเหตุ |
|---|---|---|---|---|
| **API-15** | `POST /internal/roster/upstream-events` | รับ event จาก HR Configuration: `hrconfig.period_closed` (→ T-5) · `hrconfig.effective` (ล้าง cache) · `hrconfig.deactivated` (กะปิดใช้) | `F-30` `F-02` `F-06` | **ต้นทางเป็นผู้เรียก · feature นี้เป็นผู้ฟัง** |
| **API-17** | (scheduler รายวัน) | ปิดคำขอที่หมดอายุ (W-6) | `F-60` | **ไม่ใช่ HTTP endpoint สาธารณะ** |
| **API-21** | `POST /api/v1/roster/usage` | **consumer** ลงทะเบียนว่าตัวเองอ่าน read model อยู่ | `F-47` | **ข้อยกเว้นเดียวของ AP-7** — เป็นการลงทะเบียน ไม่ใช่การเขียนข้อมูลตาราง |

> **ตรวจแล้ว: ไม่มี endpoint ใดในแพ็กนี้เขียนไปยัง HR Configuration · Attendance · Leave · OT** — feature นี้เรียกต้นทางเฉพาะ `GET .../resolve` และ `POST .../usage` (การลงทะเบียน where-used ซึ่งต้นทางเป็นผู้กำหนดสัญญา) เท่านั้น (**AP-6** · `06_TESTS IA-09`)

## §2.3 Cross-Module Contract — Published Roster Surface ⭐

> **สัญญาฉบับเต็มอยู่ที่ `00_OVERVIEW §0.13`** — ส่วนนี้เป็น contract ระดับ HTTP

### API-18 · `GET /api/v1/roster/resolve` (มุมมอง `day`)

```
GET /api/v1/roster/resolve
    ?date=2026-09-18            ← บังคับ · ไม่ส่ง = 400 ERR_ROSTER_DATE_REQUIRED
    &date_to=2026-09-30         ← optional · ช่วงสูงสุด 62 วัน
    &company_id=<uuid>          ← บังคับเมื่อ tenant มีบริษัทลูก
    &employee_id=<uuid>         ← ใช้คู่กับ scope=employee
    &scope=employee|company     ← default employee
    &page=1&page_size=500
```

**Response 200 — เมื่อมีกะ:**
```json
{
  "as_of":"2026-09-18","employee_id":"…","employee_name_snapshot":"…",
  "work_date":"2026-09-18","company_id":"…",
  "shift":{ "shift_code":"N","shift_name":"กะดึก","start_time":"22:00","end_time":"06:00",
            "is_overnight":true,"break_from":"02:00","break_to":"03:00",
            "work_days":["MON","TUE","WED","THU","FRI","SAT"] },
  "roster_version_id":"…","shift_pattern_version_id":"…",
  "roster_status":"published","slot_seq":1,"linked":true,
  "source_feature":"F-HR-ROSTER"
}
```

**Response 200 — เมื่อไม่มีกะ (4 เหตุ):**
```json
{ "as_of":"…","employee_id":"…","work_date":"…","company_id":"…",
  "shift": null,
  "reason":"NO_SHIFT_FOR_EMPLOYEE_DAY",   // | NO_ROSTER_AT_DATE | ROSTER_NOT_PUBLISHED | MODULE_NOT_LINKED
  "roster_version_id": null, "shift_pattern_version_id": null,
  "linked": true, "source_feature":"F-HR-ROSTER" }
```

| กติกาของ endpoint นี้ | รายละเอียด |
|---|---|
| **คืนเฉพาะ `published` ปัจจุบัน** | กรองที่ระดับ query — ร่าง/ถูกแทนที่/ยกเลิกร่างไม่มีทางออกมา (**RO-1** · `06_TESTS IA-01`) |
| **`shift: null` เมื่อไม่มีกะ — ห้ามเดา** | **ห้ามคืนกะมาตรฐาน ห้ามคืนกะของวันข้างเคียง ห้ามคืน `{}`** (**RO-2** · `06_TESTS IA-07`) |
| **กะแยกช่วง = หลายแถว** | เรียงตาม `slot_seq` — consumer ต้องรองรับ ไม่ใช่หยิบแถวแรกแล้วทิ้งที่เหลือ |
| **ชื่อฟิลด์ของ `shift` ล็อกไว้แล้ว** | ตรงกับ `F-HR-ATTEND §0.13.2` ทุกตัว — **ห้ามเปลี่ยนชื่อ ห้ามเพิ่มชั้นห่อ** |
| **rate limit + schema validation** | ยืมจาก preset P7 (`05_RULES §5.7` S14-01 · S14-02) |

### API-19 · `GET /api/v1/roster/periods/resolve` (มุมมอง `period`)

```
GET /api/v1/roster/periods/resolve?period_code=2026-09&company_id=…&employee_id=…
```
คืน: `period_code` · `period_from/to` · `period_status` · `employee_id` · `shift_days` · `shift_slots` · `off_days` · **`planned_hours`** · `night_shift_count` · `holiday_shift_count` · `roster_version_id[]` · `config_version_ids` · `source_feature`

> ⚠️ **`planned_hours` = ชั่วโมงตามแผน ไม่ใช่ชั่วโมงทำงาน** — **ห้ามใช้เป็นฐานคำนวณค่าจ้าง ห้ามคูณเป็นเงิน** · ชั่วโมงที่จ่ายได้มาจาก Attendance (ในกรอบกะ) กับ OT (นอกกรอบกะ) เท่านั้น

### Cross-Module Contract ที่ feature นี้ **เรียกออก** (อ่านอย่างเดียวทั้งหมด)

| ปลายทาง | endpoint | ใช้ทำอะไร | กติกา |
|---|---|---|---|
| HR Configuration | `GET /api/v1/hr-config/resolve?date=&company_id=&group=` | `shift_pattern` · `holiday_calendar` · `period_rule` · **`shift_rule` (ยังไม่มี → `null`)** | **C-1…C-3** · **ห้าม CRUD (C-4)** |
| Attendance | `GET /api/v1/attendance/resolve?date=&date_to=&company_id=&scope=company` | `day_status` · `period_status` **เท่านั้น** — **ไม่อ่านชั่วโมงมาใช้เลย** | **AT-1…AT-4 · AT-6** · **ห้ามเขียนกลับ (AT-5)** |
| Leave | `GET /api/v1/leave/resolve?date=&date_to=&employee_id=` | วันลาที่อนุมัติแล้ว (display-only) | ห้ามคำนวณวันลาเอง · ห้ามเขียนกลับ |
| OT | `GET /api/v1/ot/resolve?date=&date_to=&company_id=&employee_id=` | ธง "มี OT" (display-only) · **กรอง `withdrawn` ออก** | **OT-4 · OT-5 · OT-6** · ห้ามอ่าน `multiplier` |
| Policy Center | `ENG-ROLESCOPE-01` | ขอบเขตการเห็น + สายบังคับบัญชา (**ผู้ยืนยันคำขอสลับ**) | **ไม่เรียก DOA เลย** (`§0.16.4`) |
| Employee Master | combobox / lookup | คน · ตำแหน่ง · แผนก · `exit_date` | soft ref + snapshot |
| where-used | `POST /hr-config/items/:id/usage` · `POST /attendance/usage` · `POST /leave/usage` · `POST /ot/usage` | ลงทะเบียนตอน deploy | **C-6 · AT-7 · OT-7** |
| ENG-NOTIFY | `emit(event_id, {ref, vars})` | 6 event (`§0.16.1`) | **ห้าม hardcode ช่องทาง** |
| ENG-CSQ | `emit(profile, event, payload)` | 2 event ท่อ EC (`§0.16.2`) | **ห้ามตีมูลค่าเอง** |

## §2.4 API → Logic Trace (สรุป · ฉบับเต็มที่ `03_LOGIC §3.3`)

| API | mutation? | Function/Engine | R8 ผ่าน? |
|---|:---:|---|:---:|
| API-01 | ✅ | `F-01` `F-02` `F-03` `F-04` `F-05` `F-14` | ✅ |
| API-02 | — | `F-06` `F-07` `F-13` `F-48` `F-19` `F-20` `F-21` | ✅ |
| API-03 | ✅ | `F-12` `F-09` `F-11` `F-52` `F-14` `F-49` | ✅ |
| API-04 | ✅ | `F-12` `F-10` `F-14` `F-49` | ✅ |
| API-05 | ✅ | `F-26` `F-49` | ✅ |
| API-06 | ✅ | `F-23` `F-25` `F-32` `F-49` `F-58` `F-59` | ✅ |
| API-07 | ✅ | `F-23` **`F-24`** `F-28` `F-31` `F-56` `F-49` `F-58` `F-59` | ✅ |
| API-08 | ✅ | `F-29` `F-49` | ✅ |
| API-09 | ✅ | `F-55` `F-49` | ✅ |
| API-10 | — | `F-23` `F-24` `F-27` | ✅ |
| API-11 | ✅ | `F-34` `F-35` `F-33` `F-49` `F-58` | ✅ |
| API-12 | ✅ | `F-37` **`F-36`** `F-49` `F-58` | ✅ |
| API-13 | ✅ | `F-51` `F-40` `F-42` `F-49` `F-58` | ✅ |
| API-14 | ✅ | `F-38` `F-36` `F-39` `F-28` `F-49` `F-58` `F-59` | ✅ |
| API-15 | ✅ | `F-30` `F-02` `F-06` `F-49` | ✅ |
| API-16 | — | `F-32` + `roster-version-chain-engine` | ✅ |
| API-17 | ✅ | `F-60` `F-49` `F-58` | ✅ |
| API-18 | — | **`F-45` `F-43` `F-44`** | ✅ |
| API-19 | — | `F-45` `F-46` | ✅ |
| API-20 | ✅ | `F-45` `F-49` | ✅ |
| API-21 | ✅ | `F-47` | ✅ |
| API-22 | — | `F-48` | ✅ |

**สรุป R8: mutation API 14 ตัว · ทุกตัวมี Function/Engine ใน trace · ไม่มี orphan · ไม่มี business logic ในชั้น API**

## §2.5 Error Response

รูปแบบเดียวกันทุก endpoint:
```json
{ "error": { "code":"ERR_ROSTER_DATE_REQUIRED", "message":"…", "details": { … } } }
```
**Error catalog ฉบับเต็ม (24 code) อยู่ที่ `05_RULES §5.6`** — code ที่ consumer ต้องรู้จัก:

| code | HTTP | เมื่อไร |
|---|---|---|
| `ERR_ROSTER_DATE_REQUIRED` | 400 | เรียก `API-18/19` โดยไม่ส่ง `date`/`period_code` (**RO-3**) |
| `ERR_ROSTER_RANGE_TOO_LARGE` | 400 | ช่วงวันเกิน 62 วัน |
| `ERR_ROSTER_COMPANY_REQUIRED` | 400 | ไม่ส่ง `company_id` ใน tenant ที่มีบริษัทลูก |
| `ERR_ROSTER_NOT_FOUND` | 404 | เวอร์ชัน/คำขอไม่มีอยู่ **หรืออยู่นอกขอบเขตของผู้เรียก** (AP-4) |
| `ERR_ROSTER_UPSTREAM_UNAVAILABLE` | 503 | อ่าน Attendance ไม่ได้ตอนวางแผนเผยแพร่ซ้ำ (**ห้ามถือว่าไม่ถูกบริโภค** · EN-02) |
