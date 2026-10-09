# 03_LOGIC — F-HR-PAYROLL · Payroll (เงินเดือน)

> **Audience:** BE dev (business logic layer)
> **Scope:** ทุก logic ที่ไม่ใช่ HTTP — pure function · state transition · การคำนวณ · การตรวจค่า · การต่อกับต้นทาง/ปลายทาง
> **R8:** ทุก mutation API ใน `02_API` ต้อง trace มาที่ Function หรือ Engine ในไฟล์นี้ (§3.3) · **ห้ามมี logic ซ่อนใน `02_API`**
> **R9:** ไฟล์นี้บังคับทุก variant · **R10:** ทุก field ที่เป็นเงินมี Classification ใน `04_DB`

---

## §3.0 ⭐⭐ กติกาแกนสี่ข้อ — อ่านก่อนเขียนโค้ดบรรทัดแรก

> สี่ข้อนี้คือสิ่งที่ทำให้ feature นี้ถูกต้อง · ทุกข้อมี Function เจ้าของ · มี test คู่ · **และแต่ละข้อพังได้แบบเงียบถ้าเขียนแบบธรรมดา**

### §3.0.1 ⭐⭐ ประตูปิดตาย (fail-closed gate) — เมื่อไม่มีค่าให้อ่าน ระบบไม่ตัดสิน

**สภาพวันนี้ที่เป็นข้อเท็จจริง ไม่ใช่สมมติฐาน:** `F-HR-CONFIG §0.13.1` เผยแพร่ **6 group เท่านั้น** — `leave_type` · `ot_rate` · `shift_pattern` · `holiday_calendar` · `period_rule` · `appraisal_cycle` · **ไม่มี group ใดเลยที่บรรจุค่าของประกันสังคม ภาษีเงินได้หัก ณ ที่จ่าย กองทุนสำรองเลี้ยงชีพ หรือแม้แต่ตัวหารที่ใช้แปลงเงินเดือนเป็นค่าจ้างรายวัน/รายชั่วโมง**

**27 คีย์ที่ feature นี้ต้องใช้แต่ยังไม่มีให้อ่าน — 6 กลุ่ม:**

| กลุ่ม | คีย์ | จำนวน | ใช้ที่ขั้น | OQ |
|---|---|:---:|---|---|
| **`sso.*`** | `rate_employee` · `rate_employer` · `wage_floor` · `wage_ceiling` · `rounding_rule` · `section_catalog` | **6** | D4 | `OQ-STD-PAY1` |
| **`pit.*`** | `withholding_method` · `brackets[]` · `expense_deduction` · `personal_allowance` · `allowance_catalog[]` · `rounding_rule` · `filing_due_day` | **7** | D6 | `OQ-STD-PAY2` |
| **`pf.*`** | `employee_rate_range` · `employer_rate_by_tenure[]` · `wage_base` · `rounding_rule` · `registered_fund` | **5** | D5 | `OQ-STD-PAY3` |
| **`payroll_basis.*`** | `days_per_month_divisor` · `hours_per_day` · `hours_per_month_divisor` · `proration_method` · `rounding_rule` | **5** | E1 · E2 · D1 · D2 | `OQ-STD-PAY4` |
| **`payroll_deduction.*`** | `late_rule` · `absent_rule` · `unpaid_leave_rule` | **3** | D1 · D2 | `OQ-STD-PAY5` |
| **`payroll_review.variance_threshold`** (+ `bank_file.format_by_bank[]`) | — | **1 (+1)** | R | `OQ-STD-PAY6` |
| | **รวม** | **27** | | |

**กฎที่ engine ต้องเดินเมื่อคีย์ไม่มี — เจ็ดผลลัพธ์ที่ทดสอบได้ทุกข้อ:**

| # | เมื่อ | ระบบทำ | ระบบ **ไม่** ทำ | Function | Test |
|---|---|---|---|---|---|
| **G-1** | `hr-config/resolve` คืนว่ากลุ่มที่ขอ **ไม่มีอยู่จริง** หรือไม่มีเวอร์ชันที่มีผล ณ `pay_date` | ช่องค่าบนจอแสดง **"ยังไม่มีค่าให้อ่าน"** + ลิงก์ "จัดการที่ ตั้งค่า HR" | ❌ ไม่ใส่ตัวเลข ❌ ไม่ใช้ค่าจากหน่วยความจำ ❌ ไม่ใช้ค่าของบริษัทอื่น/ปีอื่น | `F-03` · `F-26` | AT-48 |
| **G-2** | คำนวณบรรทัดที่ขึ้นกับคีย์นั้น | `line_state = 'ยังคำนวณไม่ได้'` · **`amount = NULL`** · `uncomputable_reason` = ข้อความไทยที่ระบุ **ชื่อค่าที่ขาด + วันที่ที่ต้องการค่านั้น** | ⛔ **ไม่ใส่ 0** ⛔ ไม่ข้ามเงียบ ⛔ ไม่ประมาณการ | `F-26` | AT-49 · AT-50 · **IA-08** |
| **G-3** | รวมยอดสุทธิของคนนั้น | `net_total = NULL` + แสดง "ยังคำนวณไม่ได้" | ⛔ ไม่ sum ข้ามบรรทัดที่เป็น NULL แล้วได้ตัวเลข | `F-25` | AT-51 · **IA-09** |
| **G-4** | รวมยอดของรอบ | แสดง **"ยังไม่สมบูรณ์"** + `uncomputable_line_count` + `uncomputable_employee_count` | ⛔ ไม่แสดงยอดรวมที่คำนวณจากบรรทัดที่สมบูรณ์บางส่วน | `F-27` | AT-52 |
| **G-5** | เก็บเวอร์ชันที่ใช้ตัดสิน | `source_version_ids.hr_config.<group> = null` **ตรง ๆ** | ⛔ **ไม่ปลอมรหัสเวอร์ชัน** ⛔ ไม่ใส่สตริงว่าง ⛔ ไม่ใส่ `"unknown"` | `F-07` | AT-14 · **IA-10** |
| **G-6** ⭐⭐ | กดส่งอนุมัติ | **บล็อก** — ปุ่มใช้ไม่ได้ + drawer แสดงรายการที่ต้องเคลียร์ (บรรทัด · คน · กลุ่มค่าที่ขาด) | ⛔ **ไม่ปล่อยผ่านด้วยคำเตือน** | **`F-36`** | AT-53…AT-55 · **IA-11** |
| **G-7** | มีคีย์ที่ขาดชุดใหม่ | ยิง NTF `payroll.blocked_missing_legal_config` (`E2`) พร้อม `missing_config_groups[]` · **dedupe ตาม (`run_no`, `missing_config_groups[]`)** | ⛔ ไม่ยิงซ้ำทุกครั้งที่กดคำนวณ | `F-55` | AT-119 |

**เงื่อนไขทางเทคนิคที่ทำให้กติกานี้พังได้แบบเงียบ — ต้องตรวจทั้งหมด (`IA-08`):**

1. **ORM/DB default** — คอลัมน์ `amount` ต้องเป็น `NULL`-able **โดยไม่มี `DEFAULT 0`**
2. **Serializer** — `null` ต้องออกไปเป็น `null` ใน JSON ไม่ใช่ `0` และไม่ใช่ `""`
3. **UI formatter** — ตัวจัดรูปแบบเงินต้องรับ `null` แล้วคืน **ช่องว่าง** ไม่ใช่ `0.00`
4. **การรวมยอด** — `SUM()` ของ SQL ข้าม `NULL` เงียบ ๆ → **ต้องใช้ `COUNT(*) FILTER (WHERE amount IS NULL) = 0` เป็นเงื่อนไขก่อนรวม**
5. **CSV/PDF export** — ต้องไม่มีเส้นทางใดที่แปลง `null` เป็น `0.00` บนกระดาษ (`PRINT_SPEC §P.4`)

> ⭐ **ทำไมถึงเป็น fail-closed ไม่ใช่ default:** การใส่ค่าเริ่มต้นให้อัตราตามกฎหมายคือ **การตัดสินเรื่องเงินและกฎหมายด้วยการเดา** และเป็น **การ hardcode ค่าที่ต้องมี `effective_date`** ซึ่งผิด `P-8` กับ `HR-1` ตรง ๆ (governance invariant พัง = Hard Stop)
> ผลของการเลือก fail-closed คือ **ความเสี่ยงถูกย้ายจาก "ตัวเลขผิดที่ไม่มีใครเห็น" ไปเป็น "รอบส่งอนุมัติไม่ได้จนกว่าจะมีค่า"** ซึ่งเห็นทันทีและแก้ได้ที่เจ้าของค่า
> ⭐ **ไม่มีอัตรา เพดาน ขั้นบันได หรือวิธีปัดเศษตามกฎหมายอยู่ที่ใดในระบบนี้เลย — รวมถึงในข้อมูลตัวอย่าง** (`PI-1` · `IA-07`)

**สิ่งที่ยังคำนวณได้ตามปกติแม้ไม่มี 27 คีย์:** E3 (เงินได้อื่น · รายการปรับด้วยมือ) · D3 (รายการประจำ + `goal_amount`) · การเทียบรอบก่อนแบบไม่ตีธง · การเลือกสายอนุมัติ (ขั้น A ไม่ใช้คีย์ใดเลย) — **โครงทั้งหมดของ feature ส่งมอบได้โดยไม่ต้องรอคีย์ (Phase 1)**

---

### §3.0.2 ⭐ ชุดข้อมูลต้นทางที่ตรึงไว้ (input snapshot) — คำนวณจากอดีตที่หยุดนิ่ง ไม่ใช่จากปัจจุบันที่ขยับ

**หนึ่งแถวต่อหนึ่งต้นทาง** ใน `payroll_run_input_snapshot` (6 แถวต่อการดึงหนึ่งครั้ง) — แต่ละแถวเก็บ:

| ส่วน | เนื้อหา | ทำไมต้องมี |
|---|---|---|
| `source_feature` | `F-HR-SALSTRUCT` · `F-HR-ATTEND` · `F-HR-LEAVE` · `F-HR-OT` · `F-HR-CONFIG` · `F-HR-ONBOARD` | ระบุว่ามาจากใคร |
| `endpoint` | path ที่เรียกจริง | ตรวจได้ว่าเรียกหน้าทางเข้าที่ถูก |
| **`params`** ⭐ | พารามิเตอร์ทั้งชุด — **ต้องมี `pay_date` ของงวดเสมอ ไม่ใช่ "วันนี้"** | `SS-1` · `AT-1` · `LV-1` · `OT-1` · `C-1` · `OB-1` — **ถามโดยไม่ระบุวันคือคำถามที่ไม่มีคำตอบเดียว** (`IA-01`) |
| `called_at` | เวลาที่เรียก | ลำดับเหตุการณ์ |
| `payload` | ผลที่คืนมา **ทั้งก้อน ไม่ตัดทอน** | ทำซ้ำการคำนวณย้อนหลังได้ |
| **`version_block`** ⭐ | `version_id` / `config_version_ids` **ทั้งก้อน** ของต้นทางนั้น | `SS-2` · `AT-2` · `LV-2` · `OT-2` · `C-2` · `OB-2` — เอกสารเก่าไม่เปลี่ยนค่าเมื่อนโยบายเปลี่ยน |
| **`period_status_at_read`** | `open` / `closed` ณ เวลาที่อ่าน | บอกได้ว่ายอดตอนนั้นนิ่งหรือยัง — ต่างจากการอ่านสถานะปัจจุบันภายหลัง |
| `row_count` | จำนวนแถวที่ได้ | ตรวจความครบ |
| `hash` | ค่าตรวจสอบของ `payload` + `version_block` | พิสูจน์ย้อนหลังว่าเนื้อหาไม่ถูกแก้ |
| `superseded_by` | ชี้ snapshot ชุดใหม่ (เมื่อดึงใหม่) | **ชุดเดิมไม่ถูกลบ ไม่ถูกทับ** (append-only) |

**กติกาการอ่านและการดึงใหม่:**

1. ⭐ **ตั้งแต่รอบเข้าสถานะ `คำนวณแล้ว` การคำนวณอ่านจาก snapshot เท่านั้น — ไม่ยิงต้นทางซ้ำอีกเลย** (`F-15` · `PI-7` · `IA-03`)
2. **การดึงใหม่ (`F-09`) ทำได้เฉพาะก่อนส่งอนุมัติ** — สถานะ `ร่าง` / `ดึงข้อมูลแล้ว` / `คำนวณแล้ว` / `รอทบทวน` เท่านั้น · **หลังเข้า `รออนุมัติ` การคำนวณถูกล็อก**
3. **การดึงใหม่ล้างผลคำนวณทิ้งทั้งหมด** — ลบบรรทัดของรอบ · รอบถอยกลับไป `ดึงข้อมูลแล้ว` · **ถามยืนยันก่อนเสมอพร้อมบอกว่าผลจะหาย**
4. ⭐ **การดึงใหม่ไม่ทับ snapshot เดิม** — เขียนแถวใหม่ 6 แถว แล้วตั้ง `superseded_by` บนแถวเก่า (`BR-29` audit append-only)
5. **ตอนปิดรอบ snapshot ถูกตรึงพร้อม hash** (`F-43`) — หลังจากนั้นแก้ไม่ได้
6. **event จากต้นทางที่มาหลังคำนวณ ไม่แตะตัวเลข** — ขึ้นธง "ข้อมูลต้นทางเปลี่ยนหลังคำนวณ" ให้ผู้อนุมัติเห็นก่อนเซ็น (`F-58`) · ผู้จัดทำเลือกได้ว่าจะถอนกลับไปดึงใหม่หรือเดินต่อ

> ⭐ **ทำไมต้องเป็น snapshot ไม่ใช่การอ่านสด:** ต้นทางทั้งหกเปลี่ยนได้ตลอดเวลาจนกว่างวดจะปิด (ใบลาถูกถอน · ชั่วโมง OT ถูกปรับ · อัตราถูกแก้) · ถ้าอ่านสด **ยอดที่ผู้อนุมัติเห็นตอนเซ็นกับยอดที่ถูกปิดรอบจะเป็นคนละตัวเลข** โดยไม่มีใครรู้ — และรอบที่ปิดแล้วจะอธิบายย้อนหลังไม่ได้เลย

---

### §3.0.3 ⭐⭐ รอบที่ปิดแล้วเป็นค่าถาวร — เจ็ดข้อที่ทดสอบได้ทุกข้อ

| # | ข้อ | กลไกที่ทำให้จริง | Function | Test |
|---|---|---|---|---|
| **C-1** | **ไม่มี transition ออกจากสถานะ `ปิดรอบแล้ว`** — ไม่ใช่แค่ซ่อนปุ่ม แต่ไม่มีเส้นทางในเครื่องสถานะ | ตาราง transition ใน `05_RULES §5.2` ไม่มีแถวใดที่คอลัมน์ "จาก" เป็น `ปิดรอบแล้ว` | (state machine) | AT-79 |
| **C-2** | **ทุกคำสั่งเขียนที่ชี้มาที่รอบที่ปิดแล้วถูกปฏิเสธ** — คำนวณใหม่ · ดึงใหม่ · แก้บรรทัด · เพิ่มรายการปรับด้วยมือ · ยกเลิก · ลบ (**6 คำสั่ง**) | ⭐ **`F-44 guardClosedRun` ถูกเรียกเป็นบรรทัดแรกของทุก mutation handler** — ไม่ใช่การซ่อนปุ่มบน UI | **`F-44`** | AT-80 · **IA-15** |
| **C-3** | **ตัวเลขไม่ขยับแม้ต้นทางเปลี่ยน** — event ที่มาหลังปิดรอบ (`attendance.day_adjusted` · `leave.withdrawn` · `ot.withdrawn` · `ofb_case_cancelled` · `salstruct.effective`) **ไม่แตะตัวเลขของรอบ** แต่สร้างรายการในคิว "ต้องพิจารณารอบปรับปรุง" | `F-45 enqueueAdjustmentCandidate` — เขียนลง `payroll_adjust_queue` **ไม่แตะ `payroll_run_line`** | **`F-45`** | AT-82 |
| **C-4** | **snapshot ถูกตรึงพร้อม hash** | `F-43 freezeSnapshot` — คำนวณ hash ตอนปิดรอบ · เทียบใหม่ได้ตลอด | `F-43` | AT-83 |
| **C-5** | **สลิปกับสำเนา PDF อยู่ในคลังสำเนาถาวร — เปิดดูซ้ำได้เอกสารเดิม ไม่ generate ใหม่** | `F-42` เก็บผ่าน `ENG-DOC-STORE.store()` ตอนปิดรอบ · การเปิดดูอ่านจาก `pdf_ref` เท่านั้น | `F-42` · `F-54` | AT-84 |
| **C-6** | **การแก้ไข = รอบใหม่ที่อ้างรอบเดิม** — `ปรับปรุง` (ส่วนต่าง) · `กลับรายการ` (กลับด้านทั้งรอบ) · `นอกรอบ` (จ่ายเพิ่ม) — **ทั้งสามผ่านสายอนุมัติเหมือนรอบปกติ** | `F-46` · `F-48` สร้าง **รอบใหม่** ผ่าน `F-01` เดิม · ไม่มี path ที่แก้รอบเดิม | `F-46` · `F-48` | AT-87 · AT-89 |
| **C-7** ⭐ | **ความสัมพันธ์เก็บที่รอบใหม่ ไม่เขียนกลับลงรอบเดิม** — หน้ารอบเดิมแสดง "ถูกกลับรายการโดย `PAY-2026-11`" จาก **ดัชนีความสัมพันธ์** | ⭐ **`F-49 recordRunRelation` เขียนแถวลง `payroll_run_relation` โดยมี `new_run_no` เป็นเจ้าของแถว** · หน้ารอบเดิม query ย้อนกลับ (`references_run_no = <รอบเดิม>`) · **`payroll_run` แถวของรอบเดิมไม่ถูก UPDATE เลย** | **`F-49`** | AT-90 · AT-91 · **IA-17** |

> ⭐ **ข้อ C-7 คือข้อที่หลุดง่ายที่สุด** — วิธีเขียนที่ "ธรรมชาติ" ที่สุดคือ `UPDATE payroll_run SET reversed_by = ... WHERE run_no = <รอบเดิม>` **ซึ่งก็คือการแก้รอบที่ปิดแล้วในอีกรูปแบบหนึ่ง** · วิธีทดสอบ: จดค่า `updated_at` ของรอบเดิม → สร้างรอบกลับรายการ → **`updated_at` ต้องไม่ขยับ** (`IA-17`)

**⭐ ความหมายของ "retro" ในระบบนี้ (`C-6` ขยายความ):**

`P-9` ของ HR Configuration เขียนไว้ตรง ๆ ว่า **"ไม่มี retro — ถ้าต้องแก้ผลย้อนหลัง = สร้างเวอร์ชันใหม่ที่มีผลวันข้างหน้า"** และ `P-7` ห้ามตั้งวันมีผลย้อนเข้างวดที่ปิด · Salary Structure ปิดประตูเดียวกันที่ `P-9′`

**ดังนั้นในระบบนี้ "retro" = "รอบปรับปรุง" เท่านั้น:**

```
งวด 2026-08 ปิดแล้ว (PAY-2026-08)                     งวด 2026-09 เปิดอยู่
  snapshot ตรึง · ตัวเลขเดิม · สลิปเดิม  ─── ไม่ถูกแตะ ───▶ ยังถูกต้องในฐานะบันทึกของวันนั้น
          │
          │  ต้นทางแก้ข้อมูลของ 2026-08 (ใบลาถูกถอน · ชั่วโมง OT ถูกปรับ)
          ▼
   คิว "ต้องพิจารณารอบปรับปรุง"  (F-45 — ไม่แตะตัวเลข)
          │
          ▼
   F-47 computeRetroDifference:
      ส่วนต่าง = (ค่าที่ควรเป็นเมื่ออ่านค่าที่แก้แล้ว) − (ค่าใน snapshot ของรอบที่ปิด)
          │
          ▼
   บรรทัด line_kind = 'รายการปรับปรุงงวดก่อน' ของ  ▶ รอบปรับปรุง PAY-2026-09-ADJ (งวดที่เปิดอยู่)
      · adjust_of_run_no = PAY-2026-08
      · adjust_of_period_code = 2026-08
      · เหตุผลรายบรรทัด + เอกสารต้นทางที่ทำให้ต่าง
          │
          ▼
   ผ่านสายอนุมัติ A-4 (4 ขั้น) เหมือนรอบอื่น  ─── ห้ามยิงเข้าเงียบ ๆ (BR-32)
          │
          ▼
   สลิปของรอบปรับปรุงมีหัวข้อ "รายการปรับปรุงงวดก่อน" ระบุงวดกับเลขรอบต้นฉบับ (PRINT_SPEC §P.3)
```

**สิ่งที่ห้ามทำเด็ดขาด:** เขียนทับตัวเลขของรอบที่ปิด · เปิดงวดที่ปิดกลับมา (**เป็นอำนาจของ HR Configuration ไม่ใช่ของเรา** — `BR-34`) · ยิงส่วนต่างเข้าไปโดยไม่ผ่านสายอนุมัติ

---

### §3.0.4 ⭐ เลขที่สองชุด — `PAY-YYYY-NN` กับ `PS-YYYY-NNNNNN`

| | **เลขรอบ** | **เลขสลิป** |
|---|---|---|
| รูปแบบ | **`PAY-YYYY-NN`** | **`PS-YYYY-NNNNNN`** |
| doc_type | `PAY` | `PS` |
| ออกเมื่อ | ⭐ **ตอนสร้างรอบ (T-01)** — ทันทีที่ผ่านด่านตรวจ | ⭐ **ตอนปิดรอบ (T-11) เท่านั้น** — ในธุรกรรมเดียวกับการตรึง snapshot |
| ออกให้ใคร | 1 เลข ต่อ 1 รอบ | **1 เลข ต่อ 1 คนในรอบ — ออกพร้อมกันทั้งหมดในธุรกรรมเดียว** |
| ผู้ออก | **`ENG-DOC-NUM.next('PAY', company_ctx)`** | **`ENG-DOC-NUM.next('PS', company_ctx)`** |
| immutable | ✅ ไม่เปลี่ยนตลอดชีวิตรอบ | ✅ ไม่เปลี่ยนตลอดชีวิตสลิป |
| reuse | ❌ **ไม่ reuse แม้รอบถูกยกเลิก** | ❌ ไม่ reuse |
| รอบจำลอง | ✅ ออกเลขรอบตามปกติ | ⛔ **ไม่ออกเลขสลิป** (`BR-42`) |
| Function | `F-01` | `F-41` |

**⭐ กติกาที่สำคัญที่สุดของสองชุดนี้ — `NN` ในเลขรอบเป็นตัวนับเอกสาร ไม่ใช่เลขงวด:**

`PAY-2026-09` **ไม่ได้แปลว่า "งวดกันยายน"** — `09` คือ **ลำดับที่ 9 ของเอกสารชนิด `PAY` ในปี 2026 ของบริษัทนั้น** ตามที่ `ENG-DOC-NUM` เดินให้ · **งวดกับชนิดรอบเป็น field ต่างหาก** (`period_code` · `run_type`)

**ทำไมข้อนี้สำคัญ:** ถ้าตีความ `NN` เป็นเลขงวด จะเกิดสามปัญหาทันที —
1. **รอบนอกรอบ/ปรับปรุง/กลับรายการของงวดเดียวกันจะชนเลขกัน** เพราะงวดเดียวมีได้หลายรอบ
2. **รอบที่ถูกยกเลิกจะทำให้ลำดับขาด** แล้วจะมีคนอยากเติมกลับ ซึ่งคือการ reuse เลข (ผิด `BR-35`)
3. **จะเกิดการ format เลขเองที่ฝั่ง feature** ("เอา `period_code` มาต่อกับ `PAY-`") ซึ่งผิด `LOCK-NUM` โดยตรง — และจะพังทันทีที่ความถี่งวดเปลี่ยนจากรายเดือนเป็นรายครึ่งเดือน

> ⛔ **ห้าม format เลขเองทุกกรณี** — เรียก `ENG-DOC-NUM.next()` แล้วรับค่าที่ได้ · **ห้ามแยกส่วนของเลขไปใช้เป็นตัวกรอง** (กรองด้วย `period_code` · `run_type` · `company_id` แทน)

**การเลือกสายอนุมัติ (ขั้น A ของ §3.0.5) — สรุปกฎที่นี่เพราะเกี่ยวกับเลขและชนิดรอบ:**

```
action_id = f(run_type, has_material_variance)          ← ฟังก์ชันตายตัว ไม่ใช่ดุลพินิจ (F-34)
   ปกติ    + has_material_variance = false        → payroll_approve_run              (3 ขั้น)
   ปกติ    + has_material_variance ∈ {true, null} → payroll_approve_run_variance     (4 ขั้น)  ⭐ null → สายยาวไว้ก่อน
   นอกรอบ                                          → payroll_approve_run_offcycle    (4 ขั้น)
   ปรับปรุง                                        → payroll_approve_run_adjustment  (4 ขั้น)
   กลับรายการ                                      → payroll_approve_run_reversal    (5 ขั้น · รวมผู้ตรวจสอบภายใน)

payload → GET /doa/resolve = { action_id, run_type, has_material_variance,
                               employee_count, period_code, company_id }
                                   ⛔ ไม่มี field ที่เป็นจำนวนเงินแม้แต่ field เดียว (F-35 · PI-9)
```

⭐ **`role-comp-admin` เป็นขั้นที่ 2 ของทุกสาย** — เป็นขั้นที่ต้องเห็นตัวเลขจริง และเป็น role เดียวกับที่ Salary Structure อนุญาตให้เห็น `base_amount`
⭐ **เหตุผลเต็มว่าทำไมไม่ส่งเงินเข้า resolve อยู่ที่ `BRD §5.4.2`** — สรุปสามข้อ: (1) ยอดรวมวัดจำนวนหัวไม่ได้วัดความเสี่ยง (2) แถบวงเงินจะเก่าเงียบ ๆ ในวันที่เวอร์ชัน SSO/PIT/กระบอกเปลี่ยน ซึ่งเป็นการ hardcode ค่าที่มี `effective_date` ในอีกรูป (3) **ยอดรวมของรอบเป็นตัวเลขที่ถูกจำกัดสิทธิ์สูงสุดของโมดูล — มันต้องไม่รั่วเข้าไปอยู่ในบันทึกการอนุมัติซึ่งมีขอบเขตสิทธิ์คนละชุดกับ Policy Center**

### §3.0.5 ลำดับการคำนวณ (gross-to-net) — ลำดับนี้มีความหมาย

```
E1 เงินได้ประจำ ──▶ E2 เงินได้ตามชั่วโมง (OT) ──▶ E3 เงินได้อื่น
                                │
                                ▼
D1 หักลาไม่ได้รับค่าจ้าง ──▶ D2 หักขาด/สาย ──▶ D3 หักประจำ
                                │
                                ▼
        ⚖️ D4 ประกันสังคม ──▶ ⚖️ D5 กองทุนสำรองเลี้ยงชีพ ──▶ ⚖️ D6 ภาษีหัก ณ ที่จ่าย
                                │
                                ▼
                          N สุทธิ ──▶ R เทียบรอบก่อน + ตั้งธง ──▶ A เลือกสายอนุมัติ
```

⭐ **D4 → D5 → D6 สลับไม่ได้:** เงินสมทบประกันสังคม (D4) กับเงินสะสมกองทุนสำรองเลี้ยงชีพ (D5) เป็น **รายการลดหย่อนของฐานภาษี** ที่ D6 ต้องใช้ · **สลับลำดับ = ภาษีผิดทุกคน** · บังคับที่ระดับ engine (`ENG-PAY-01` เดินลำดับตายตัว) **ไม่ใช่ลำดับการแสดงผล** (`AT-46` · `AT-47`)

---

## §3.1 Functions (Scope-Local · camelCase · 59 ตัว)

> **สัญญาของทุก Function:** input/output เป็น object บริสุทธิ์ · **ไม่มี HTTP term (req/res/header) แม้แต่ตัวเดียว** · เรียกจาก `02_API` เท่านั้น ไม่เรียกข้ามกัน (ยกเว้นที่ระบุ)

### หมวด A — สร้างรอบและเลขที่

**F-01 · `createPayrollRun`**
- **input:** `{company_id, period_code, run_type, scope_type, employee_ids[]?, references_run_no?, is_simulation, actor_id}`
- **ทำ:** เรียก `F-02` ตรวจก่อน → เรียก `ENG-DOC-NUM.next('PAY', company_ctx)` → เขียนแถว `payroll_run` สถานะ `ร่าง` → `F-57` บันทึกไทม์ไลน์
- **output:** `{run_no, run_status:'ร่าง'}`
- **ห้าม:** ⛔ format `run_no` เอง · ⛔ ใช้ `period_code` เป็นส่วนของเลข (`§3.0.4`)
- **rules:** BR-01 · BR-31 · BR-35 · BR-42 | **test:** AT-01 · AT-02 · AT-06

**F-02 · `validateRunCreation`**
- **input:** `{company_id, period_code, run_type, references_run_no?, scope_type, employee_ids[]?}`
- **ทำ:** ตรวจ 5 ด่าน — (1) งวดมีอยู่จริงในรายการที่ HR Config เผยแพร่ (2) รอบปกติ: `period_status = open` (3) รอบปกติ: ไม่มีรอบปกติของงวดนั้นที่ยังไม่ถูกยกเลิก (4) `ปรับปรุง`/`กลับรายการ`: `references_run_no` มีค่า **และรอบที่อ้างอยู่สถานะ `ปิดรอบแล้ว`** (5) `นอกรอบ`: `scope_type = รายชื่อที่เลือก` และมีรายชื่อ ≥ 1
- **output:** `{ok: bool, blockers: [{code, message, link?}]}`
- **rules:** BR-01 · BR-31 · BR-34 · VR-02…VR-06 | **test:** AT-04 · AT-05 · AT-08

**F-03 · `resolvePayPeriod`**
- **input:** `{company_id, date}`
- **ทำ:** เรียก `X-API-05` (`hr-config/resolve?group=period_rule`) → คืนรายการงวดพร้อม `period_status` · `pay_date` · `version_id`
- **⭐ พฤติกรรมเมื่อกลุ่มไม่มี:** ไม่เกิดขึ้นกับ `period_rule` (มีอยู่แล้ว) — แต่ฟังก์ชันนี้ยัง**ใช้รูปแบบเดียวกันกับกลุ่มอื่น**: กลุ่มที่ไม่มี → คืน `{available:false, version_id:null}` **ไม่ throw ไม่เดา** (`G-1`)
- **rules:** BR-04 · BR-41 | **test:** AT-03 · AT-48

**F-04 · `cancelPayrollRun`**
- **input:** `{run_no, cancel_reason, actor_id}`
- **ทำ:** `F-44` ก่อน → ตรวจสถานะอยู่ใน {ร่าง, ดึงข้อมูลแล้ว, คำนวณแล้ว, รอทบทวน, ไม่อนุมัติ} → ตั้ง `run_status = ยกเลิก` → `F-57`
- **⭐ เลขที่คงอยู่ ไม่ reuse** | **rules:** BR-35 · VR-18 | **test:** AT-09 · AT-76

### หมวด B — ดึงข้อมูลและ snapshot

**F-05 · `pullSourceData`**
- **input:** `{run_no, sources[]? (default = ทั้ง 6)}`
- **ทำ:** สำหรับแต่ละต้นทาง เรียก `X-API-01…X-API-06` โดย **ส่ง `pay_date` ของงวดเป็นพารามิเตอร์วันที่เสมอ** → ส่งผลให้ `F-06` เขียน snapshot · ถ้ามีต้นทางล้ม → **รอบค้างที่ `ร่าง`** พร้อม `failed_sources[]`
- **output:** `{ok, failed_sources[], snapshot_ids[]}`
- **ห้าม:** ⛔ ส่ง "วันนี้" · ⛔ เรียกต่อเมื่อรอบอยู่สถานะ ≥ `รออนุมัติ`
- **rules:** BR-02 · BR-05 · VR-07 · VR-08 | **test:** AT-10 · AT-11 · AT-15 · **IA-01**

**F-06 · `buildInputSnapshot`**
- **input:** `{run_no, source_feature, endpoint, params, payload, version_block, period_status_at_read}`
- **ทำ:** คำนวณ `row_count` + `hash` → เขียนแถวใหม่ใน `payroll_run_input_snapshot` · **ไม่ UPDATE แถวเดิม**
- **rules:** BR-05 · BR-29 | **test:** AT-12 · **IA-02**

**F-07 · `collectSourceVersionIds`**
- **input:** `{run_no}`
- **ทำ:** รวม `version_block` ของทั้ง 6 ต้นทางเป็นก้อนเดียวเก็บที่ `payroll_run.source_version_ids`
- **⭐ คีย์ที่ต้นทางไม่มี → เก็บ `null` ตรง ๆ** — โดยเฉพาะ `hr_config.{sso, pit, pf, payroll_basis, payroll_deduction, payroll_review}` ซึ่งวันนี้เป็น `null` ทั้งหมด
- **ห้าม:** ⛔ ใส่สตริงว่าง ⛔ ใส่ `"unknown"` ⛔ ใส่รหัสเวอร์ชันของกลุ่มอื่น
- **rules:** BR-05 · BR-18 | **test:** AT-13 · AT-14 · **IA-10**

**F-08 · `retryFailedSource`** — เรียก `F-05` เฉพาะต้นทางที่ล้ม | **test:** AT-16

**F-09 · `repullSourceData`**
- **input:** `{run_no, reason?, actor_id}`
- **ทำ:** `F-44` → ตรวจสถานะ ≤ `รอทบทวน` → **ลบบรรทัดผลคำนวณทั้งหมดของรอบ** → ตั้ง `superseded_by` บน snapshot ชุดเดิม (**ไม่ลบ**) → เรียก `F-05` ใหม่ → รอบกลับไป `ดึงข้อมูลแล้ว` → `F-57`
- **rules:** BR-06 · BR-29 | **test:** AT-17 · AT-18

**F-10 · `buildRunScope`**
- **input:** `{run_no}` (ใช้ snapshot ของ On/Offboard)
- **ทำ:** คัดคนเข้ารอบ — **อ่าน `employment_state` ประกอบเสมอ ห้ามตัดสินจาก `last_working_day = null` เพียงอย่างเดียว** · คนที่ `employment_state = left` และ `last_working_day < period_from` → **ไม่อยู่ในรอบ** พร้อมเหตุผล · คนที่ `last_working_day` อยู่ในงวด → ทำเครื่องหมาย **"รอบจ่ายสุดท้าย"**
- **output:** `{included[], excluded: [{employee_id, reason}], final_pay_employees[]}`
- **rules:** BR-20 · BR-21 | **test:** AT-34 · AT-35

### หมวด C — ความพร้อมของข้อมูล

**F-11 · `evaluateReadiness`**
- **ทำ:** อ่านจาก snapshot 6 ต้นทาง แล้วสร้าง 6 แถวความพร้อม — ธง "ยอดยังไม่นิ่ง" มาจาก `unconfirmed_days` · `pending_exception_days` (Attendance) · `open_request_count` (Leave) · `unconfirmed_hours` · `pending_docs` · `needs_review_docs` (OT) · `period_status` (ทุกต้นทาง) · **การ์ดค่าตามกฎหมาย 6 กลุ่ม แสดง "ยังไม่มีค่าให้อ่าน"** (HR Config)
- **output:** `{rows: [{source_feature, status, flags[], affected_count, manage_link}]}`
- **⭐ ธงไม่บล็อกการคำนวณ — แต่ติดค้างไปถึงหน้าอนุมัติ** | **rules:** BR-03 · BR-41 | **test:** AT-21…AT-23 · AT-30

**F-12 · `detectMissingRateEmployees`** — Salary Structure คืน `rate: null` + `NO_RATE_AT_DATE` → เข้ารายการ "ต้องแก้ก่อน" · ⛔ **ห้ามใช้อัตราของวันใกล้เคียง** | **rules:** VR-13 | **test:** AT-24 · AT-25

**F-13 · `detectMaskedRateBlock`** — Salary Structure คืน `masked = true` → ⭐ **บล็อกทั้งรอบ** (`F-15` ปฏิเสธ · `F-36` ปฏิเสธ) + ชี้ไป Policy Center · ⛔ **ไม่มี code path ใดที่พยายามอ่านตัวเลขทางอื่น** | **rules:** BR-39 · VR-09 | **test:** AT-26 · AT-27

**F-14 · `detectIncompleteTimeDays`** — วันที่ `day_status = exception` (ต้นทางคืน `work_hours = 0`) → เข้ารายการ "ข้อมูลเวลาไม่ครบ" · ⭐ **ห้ามตีความว่า "ไม่ได้ทำงาน"** · **ไม่ส่งค่า 0 นั้นเข้า `F-20`** | **rules:** BR-09 | **test:** AT-28 · AT-29 · **IA-05**

### หมวด D — คำนวณ (เรียกผ่าน `ENG-PAY-01`)

**F-15 · `calculateRun`** ⭐ *orchestrator*
- **input:** `{run_no, actor_id}`
- **ทำ:** `F-44` → ตรวจสถานะ ∈ {ดึงข้อมูลแล้ว, คำนวณแล้ว, รอทบทวน, ไม่อนุมัติ} → ถ้า `F-13` บล็อก → ปฏิเสธ → **ลบบรรทัดเดิมของรอบ** → เดิน `ENG-PAY-01` ตามลำดับ E1·E2·E3 → D1·D2·D3 → **D4→D5→D6** → N ต่อคน → `F-27` นับบรรทัดที่คำนวณไม่ได้ → `F-30` เทียบรอบก่อน → `F-31` ตั้งธง → รอบเข้า `คำนวณแล้ว`
- ⭐ **อ่านจาก snapshot เท่านั้น — ไม่มี call ออกไปหาต้นทางในฟังก์ชันนี้หรือฟังก์ชันลูกใด ๆ**
- **rules:** BR-06 · BR-11 · BR-43 | **test:** AT-19 · AT-20 · AT-32 · **IA-03**

**F-16 · `calcFixedEarnings` (E1)** — จาก `base_amount` + `components[].direction = รายได้` · prorate เฉพาะที่ `prorate_by_payment_days = true` (ผ่าน `F-29`) · **ต้องการ `payroll_basis.proration_method` + `days_per_month_divisor`** → ไม่มี → `F-26` | ⛔ **ห้ามคำนวณ `compa-ratio` เอง — ใช้ `band_position` ที่คืนมา** | **rules:** BR-08 · BR-23 | **test:** AT-32

**F-17 · `calcHourlyEarnings` (E2)** — ต่อ `by_rate_type[]`: `total_hours_confirmed` × `multiplier` × อัตรารายชั่วโมง · อัตรารายชั่วโมง = Σ(องค์ประกอบที่ `is_ot_base = true`) ÷ `payroll_basis.hours_per_month_divisor` · **แยกบรรทัดต่อ `payroll_code` ของแต่ละ `rate_type` — ไม่รวมเป็นก้อนเดียว**
- ⛔ **ห้ามอ่าน `outside_shift_hours` / `total_outside_shift_hours` จากทุกที่ — ไม่มี code path ใดที่แตะ field นี้** (ตรวจได้ด้วยการ grep ชื่อ field)
- ⛔ ใช้เฉพาะชั่วโมงจากใบ `time_confirmed` (ต้นทางคืนมาแล้วเฉพาะแบบนั้น) · **`multiplier` เป็นค่าอ้างอิงของอัตรา ไม่ใช่จำนวนเงิน**
- **ไม่มี `hours_per_month_divisor` → `F-26`** | **rules:** BR-10 · BR-11 · BR-13 | **test:** AT-30 · AT-31 · AT-36 · AT-37 · **IA-06**

**F-18 · `calcOtherEarnings` (E3)** — รายการเบิกที่จ่ายผ่านเงินเดือน (Module Linkage ปิด → **กลุ่มว่างและไม่บล็อก**) + รายการปรับด้วยมือฝั่งรายได้ | **rules:** BR-40 | **test:** AT-38

**F-19 · `calcLeaveDeduction` (D1)** — ต่อ `by_leave_type[]`: `total_days` × (1 − `paid_percent`) × อัตรารายวัน · **ใช้ป้าย `is_paid`/`paid_percent` ตามที่ต้นทางส่งมา ห้ามตีความใหม่** · **ต้องการ `payroll_deduction.unpaid_leave_rule` + `payroll_basis.days_per_month_divisor`** → ไม่มี → `F-26` | **rules:** BR-12 | **test:** AT-40

**F-20 · `calcAbsenceLateDeduction` (D2)** — ใช้ `absent_days` · `late_count` · `late_minutes_total` ที่ต้นทางส่งมา **ห้ามนับเอง** · **ต้องการ `payroll_deduction.absent_rule` + `late_rule`** → ไม่มี → `F-26`
- ⭐ **วันที่ `F-14` ทำเครื่องหมายว่า "ข้อมูลเวลาไม่ครบ" ต้องไม่ถูกนับเป็นวันขาด** | **rules:** BR-09 · BR-11 · BR-15 | **test:** AT-29 · AT-41

**F-21 · `calcRecurringDeduction` (D3)** — จาก `recurring[]` ที่มีผล ณ `pay_date` · เทียบ `accrued_amount` กับ `goal_amount` → **งวดที่ทำให้เกินเป้าให้หักเท่าที่เหลือแล้วหยุด** · แสดงยอดคงเหลือบนสลิป | **test:** AT-42

**F-22 · `calcSocialSecurity` (D4)** ⚖️
- **ต้องการ:** `sso.rate_employee` · `sso.rate_employer` · `sso.wage_floor` · `sso.wage_ceiling` · `sso.rounding_rule` · `sso.section_catalog` **+ มาตราประกันสังคมของคนนั้น** (`OQ-PAY-07`)
- **ทำ:** ฐาน = Σ(องค์ประกอบที่ `is_ssf_base = true`) → clamp ด้วย floor/ceiling → × อัตรา → ปัดเศษตาม `rounding_rule` → **สร้างสองบรรทัด: `SSO-EE` (หักจากพนักงาน) กับ `SSO-ER` (ส่วนนายจ้าง — แสดงเพื่อความโปร่งใส ไม่หัก)**
- ⭐ **วันนี้ไม่มีคีย์ใดเลย → ทั้งสองบรรทัดเป็น `ยังคำนวณไม่ได้` ผ่าน `F-26`**
- **rules:** BR-14 · BR-15 | **test:** AT-43 · AT-44 · **IA-07**

**F-23 · `calcProvidentFund` (D5)** ⚖️
- **ต้องการ:** `pf.employee_rate_range` · `pf.employer_rate_by_tenure[]` · `pf.wage_base` · `pf.rounding_rule` · `pf.registered_fund` **+ ธง `is_pf_base` จาก Salary Structure (`OQ-PAY-06`) + สถานะสมาชิก/อัตราสะสมที่พนักงานเลือก (`OQ-PAY-07`)**
- **ทำ:** ฐาน = Σ(องค์ประกอบที่ `is_pf_base = true`) → × อัตราสะสมของพนักงาน (บรรทัด `PF-EE`) → × อัตราสมทบนายจ้างตามอายุงาน (บรรทัด `PF-ER`)
- ⛔ **ห้ามเดาว่า "ใช้ฐานเดียวกับประกันสังคม"** — ธง `is_pf_base` ยังไม่มี → `F-26`
- **rules:** BR-14 · BR-15 | **test:** AT-45

**F-24 · `calcWithholdingTax` (D6)** ⚖️
- **ต้องการ:** `pit.withholding_method` · `pit.brackets[]` · `pit.expense_deduction` · `pit.personal_allowance` · `pit.allowance_catalog[]` · `pit.rounding_rule` **+ ธง `is_pit_base` (`OQ-PAY-06`) + ข้อมูลลดหย่อนรายคน (`OQ-PAY-07`) + YTD (`F-53`)**
- **ทำ:** เงินได้พึงประเมิน (ฐาน `is_pit_base`) − ค่าใช้จ่ายเหมา − ค่าลดหย่อน (**รวมเงินสะสม PF จาก D5 กับเงินสมทบ SSO จาก D4**) → ขั้นบันได → ภาษีทั้งปี ÷ จำนวนงวด − ภาษีที่หักไปแล้ว (YTD)
- ⭐ **ต้องเรียกหลัง `F-22` กับ `F-23` เสมอ — บังคับที่ `ENG-PAY-01` ไม่ใช่ที่ลำดับการแสดงผล**
- ⛔ **ห้ามใช้ค่าตั้งต้น "โสด ไม่มีบุตร"** — นั่นคือการเดาเรื่องภาษี → `F-26`
- **rules:** BR-14 · BR-15 | **test:** AT-46 · AT-47 · AT-56

**F-25 · `calcNetTotal` (N)** — Σ รายได้ − Σ รายหัก · ⭐ **ถ้าคนนั้นมีบรรทัดใดที่ `line_state = ยังคำนวณไม่ได้` → `net_total = NULL`** · ⛔ **ห้ามใช้ `SUM()` ที่ข้าม NULL เงียบ ๆ — ต้องตรวจ `COUNT(*) FILTER (WHERE amount IS NULL) = 0` ก่อน** | **rules:** BR-16 | **test:** AT-51 · **IA-09**

**F-26 · `markLineUncomputable`** ⭐⭐
- **input:** `{line_id | line_draft, missing_key, needed_at_date}`
- **ทำ:** ตั้ง `line_state = 'ยังคำนวณไม่ได้'` · **`amount = NULL`** · เขียน `uncomputable_reason` เป็นข้อความไทยที่ระบุ **ชื่อค่าที่ขาดกับวันที่ที่ต้องการค่านั้น** เช่น *"ยังไม่มีอัตราเงินสมทบประกันสังคมที่มีผล ณ 30/09/2026"*
- ⛔ **ห้ามใส่ 0 · ห้ามใส่สตริงว่างในช่องจำนวนเงิน · ห้ามข้ามการสร้างบรรทัด** (บรรทัดต้องมีอยู่เพื่อให้เห็นว่าขาดอะไร)
- **rules:** BR-15 · VR-23 | **test:** AT-49 · AT-50 · **IA-08**

**F-27 · `countUncomputable`** — นับ `uncomputable_line_count` + `uncomputable_employee_count` + `missing_config_groups[]` เก็บที่หัวรอบ · เป็นแหล่งของการ์ด "ยอดรวมของรอบ = ยังไม่สมบูรณ์" กับเงื่อนไขของ `F-36` | **rules:** BR-17 · BR-19 | **test:** AT-52

**F-28 · `addManualLine`** — `F-44` → ตรวจสถานะ ≤ `รอทบทวน` → **บังคับ `manual_reason` + `manual_doc_ref`** → สร้างบรรทัด `line_kind = 'รายการปรับด้วยมือ'` `is_manual = true` (**ป้ายติดถาวร**) | **rules:** VR-10 · VR-11 | **test:** AT-39

**F-29 · `prorateByPaymentDays`** — prorate ตาม `payroll_basis.proration_method` เฉพาะองค์ประกอบที่ `prorate_by_payment_days = true` · ใช้ `start_date`/`last_working_day` จาก On/Offboard | **rules:** BR-23 | **test:** AT-33 · AT-34

### หมวด E — ทบทวนเทียบรอบก่อน

**F-30 · `buildVarianceReport` (R)** — หา **รอบปกติล่าสุดที่ `ปิดรอบแล้ว` ของ `company_id` + `scope` เดียวกัน** → เทียบรายคน × รายองค์ประกอบ + ยอดรวม → แยก "คนที่เพิ่งเข้ามา" กับ "คนที่หายไป" · ⛔ **ห้ามเทียบกับรอบของขอบเขตอื่นหรือรอบที่ยังไม่ปิด** · ไม่มีรอบก่อน → คืน `{has_baseline:false}` **ไม่ใช่ error** | **test:** AT-57…AT-60

**F-31 · `evaluateMaterialVariance`** — อ่าน `payroll_review.variance_threshold` (+ `version_id` → `variance_threshold_version_id`) → ตีธงรายรายการที่เกินเกณฑ์ → ตั้ง `has_material_variance`
- ⭐ **ไม่มีเกณฑ์ → `has_material_variance = NULL` และไม่ตีธงรายการใด** (ไม่ใช่ `false`)
- **rules:** BR-24 | **test:** AT-61 · AT-63 · AT-64

**F-32 · `markVarianceReviewed`** — ตีธง "ทบทวนแล้ว" รายรายการ (append-only) | **test:** AT-62

**F-33 · `summarizeCostByCenter`** `[AI-DEFAULT]` — รวมยอดตาม `cost_center` × `payroll_code` · ผ่าน `F-59` ก่อนส่งออก · **เป็นฐานของ `F-52` (payload GL) ด้วย** | **test:** AT-65

### หมวด F — อนุมัติ

**F-34 · `pickApprovalAction`** — ฟังก์ชันตายตัวตามตารางใน `§3.0.4` · ⛔ **ไม่มี input ที่เป็นจำนวนเงิน** · ⛔ **ห้ามให้ผู้ใช้เลือกเอง** · ⭐ `has_material_variance = NULL` → คืนสายที่ยาวกว่า (`payroll_approve_run_variance`) | **rules:** BR-24 · BR-25 | **test:** AT-66 · AT-64

**F-35 · `buildDoaResolvePayload`** ⭐⭐
- **output:** `{action_id, run_type, has_material_variance, employee_count, period_code, company_id}`
- ⛔ **ต้องไม่มี field ที่เป็นจำนวนเงินแม้แต่ field เดียว** — ไม่มี `net_total` · `gross_total` · `total_amount` · `base_amount` · `amount` · หรือชื่อใด ๆ ที่มีค่าเป็นเงิน
- **ทำต่อ:** เรียก `X-API-07` (`GET /doa/resolve`) → ได้ `approval_chain[]` ที่มีจำนวนขั้นจริง (3–5)
- ⛔ **ห้าม hardcode chain · ห้าม cache chain ข้ามการส่ง** (ส่งใหม่ = resolve ใหม่ทั้งสาย)
- **rules:** BR-25 · BR-26 · VR-24 | **test:** AT-67…AT-69 · **IA-12 · IA-13**

**F-36 · `submitForApproval`** ⭐⭐
- **ทำ (ตามลำดับ):** `F-44` → ตรวจสถานะ = `รอทบทวน` → **ตรวจ `is_simulation = false`** → ⭐ **ตรวจ `uncomputable_line_count = 0`** → ตรวจไม่มีคนในรายการ "ต้องแก้ก่อน" (`F-12`) → ตรวจ `F-13` ไม่บล็อก → `F-34` → `F-35` → ตรวจ **SoD: `submitted_by ∉ approval_chain[].assignee_id`** → ตั้งสถานะ `รออนุมัติ` + **ล็อกการคำนวณ** → `F-57`
- **output เมื่อบล็อก:** `{ok:false, blockers:{uncomputable_lines, uncomputable_employees, missing_config_groups[], no_rate_employees[]}}`
- ⭐ **นี่คือประตูปิดตายของ feature** — ถ้าข้อใดไม่ผ่าน **ไม่มีทางเดินต่อ** และไม่มีทางลัด
- **rules:** BR-19 · BR-27 · VR-12…VR-16 | **test:** AT-53…AT-55 · AT-70 · AT-71 · **IA-11 · IA-14**

**F-37 · `recordApprovalStep`** — บันทึกการอนุมัติของขั้นปัจจุบัน (append-only) · ครบทุกขั้น → `อนุมัติแล้ว` | **test:** AT-72

**F-38 · `rejectRun`** — **บังคับ `reject_reason`** → `ไม่อนุมัติ` | **rules:** VR-17 | **test:** AT-72

**F-39 · `resubmitRun`** — จาก `ไม่อนุมัติ` → `คำนวณแล้ว` → ผู้จัดทำแก้แล้วเรียก `F-36` ใหม่ · ⭐ **resolve สายใหม่ทั้งสาย · ชั้นเปลี่ยนได้ถ้าธงเปลี่ยน · เลขที่รอบคงอยู่** | **test:** AT-73

**F-58 · `applySourceChangeFlag`** — รับ event ต้นทางระหว่างที่รอบอยู่ `คำนวณแล้ว`…`รออนุมัติ` → ⭐ **ไม่แตะตัวเลข** · ตั้งธง `source_changed_after_calc` + รายละเอียด ให้ผู้อนุมัติเห็นก่อนเซ็น | **rules:** BR-03 · BR-06 | **test:** AT-74 · AT-75

### หมวด G — ปิดรอบและความถาวร

**F-40 · `closePayrollRun`** ⭐⭐ *ธุรกรรมเดียว*
- **ทำ (ต้องสำเร็จครบทุกข้อ มิฉะนั้น rollback ทั้งหมด):**
  1. `F-44` → ตรวจสถานะ = `อนุมัติแล้ว` → ตรวจ `is_simulation = false`
  2. `F-41` ออกเลข `PS-YYYY-NNNNNN` ให้ **ทุกคนในรอบ**
  3. `F-42` render PDF ทุกใบ → เก็บสำเนาผ่าน `ENG-DOC-STORE.store()`
  4. `F-43` ตรึง snapshot + คำนวณ `snapshot_hash`
  5. ตั้ง `run_status = ปิดรอบแล้ว` · `closed_at` · `closed_by`
  6. ⭐ **ยิง event หลัง commit ครบเท่านั้น** — NTF `payroll.run_closed` (`E3`) + `payroll.payslip_available` (`E4` · fan-out รายคน เป็น batch) · CSQ `payroll.run_closed` (FC+AC+EC) + `payroll.employer_contribution_committed` + `payroll.withholding_tax_accrued`
- ⛔ **ถ้า render PDF ใบใดล้ม → ไม่ปิดรอบเลย และไม่ยิง event ใด ๆ** (`OQ-BRD-03`)
- **rules:** BR-36 · BR-40 · BR-42 · VR-19 | **test:** AT-77 · AT-78

**F-41 · `issuePayslipNumbers`** — `ENG-DOC-NUM.next('PS', company_ctx)` ต่อคน · ⛔ ห้าม format เอง ⛔ รอบจำลองไม่ออกเลข | **rules:** BR-35 · BR-36 | **test:** AT-92 · AT-86

**F-42 · `renderAndStorePayslipPdf`** — ประกอบข้อมูลตาม `PRINT_SPEC §P.2` → render (WeasyPrint) → `ENG-DOC-STORE.store()` → เก็บ `pdf_ref` · **การเปิดดูซ้ำอ่านจาก `pdf_ref` ไม่ render ใหม่** · ⛔ **ถ้าเจอบรรทัดที่ `amount IS NULL` ให้หยุด render แล้วรายงาน — ห้ามพิมพ์ `0.00`** (โดยโครงสร้างไม่ควรเกิด เพราะ `BR-19` กันไว้แล้ว) | **test:** AT-84 · AT-94 · AT-95

**F-43 · `freezeSnapshot`** — คำนวณ `snapshot_hash` จาก payload + version_block ของทั้ง 6 แถว → เก็บที่หัวรอบ | **rules:** BR-05 | **test:** AT-83

**F-44 · `guardClosedRun`** ⭐⭐
- **input:** `{run_no, command}`
- **ทำ:** ถ้า `run_status = ปิดรอบแล้ว` → **ปฏิเสธทันที** ด้วย `ERR_RUN_CLOSED_IMMUTABLE` พร้อมข้อความชี้ทาง *"รอบที่ปิดแล้วแก้ไม่ได้ — ต้องสร้างรอบปรับปรุงหรือรอบกลับรายการ"*
- ⭐ **ต้องถูกเรียกเป็นบรรทัดแรกของ handler ทุกตัวที่เขียนข้อมูล** — `F-04` · `F-05` · `F-09` · `F-15` · `F-28` · `F-36` และคำสั่งลบทุกชนิด
- ⭐ **ไม่ใช่การซ่อนปุ่มบน UI** — ปุ่มที่ซ่อนไม่ได้กันคำสั่งที่ยิงตรงเข้า API
- **rules:** BR-28 · BR-30 · VR-20 | **test:** AT-79…AT-81 · AT-118 · **IA-15**

**F-45 · `enqueueAdjustmentCandidate`** — รับ event ต้นทางที่อ้างงวดของรอบที่ **ปิดแล้ว** → เขียนแถวลง `payroll_adjust_queue` (`{run_no, source_feature, event_id, employee_id, detail, occurred_at}`) · ⭐ **ไม่แตะ `payroll_run` และ `payroll_run_line` เลย** | **rules:** BR-22 · BR-28 | **test:** AT-82

**F-46 · `createAdjustmentRun`** — จากหน้ารอบที่ปิด หรือจากคิว → เรียก `F-01` สร้าง **รอบใหม่** `run_type = ปรับปรุง` ในงวดที่ **เปิดอยู่** พร้อม `references_run_no` → `F-47` → `F-49` | **rules:** BR-31 · BR-32 | **test:** AT-87

**F-47 · `computeRetroDifference`** ⭐
- **ทำ:** ต่อคน ต่อองค์ประกอบ — **ส่วนต่าง = (ค่าที่ควรเป็นเมื่ออ่านค่าที่แก้แล้ว) − (ค่าใน snapshot ของรอบที่ปิด)** → สร้างบรรทัด `line_kind = 'รายการปรับปรุงงวดก่อน'` พร้อม `adjust_of_run_no` · `adjust_of_period_code` · เหตุผลรายบรรทัด · `source_ref` ของเอกสารที่ทำให้ต่าง
- ⛔ **ไม่คำนวณงวดเก่าใหม่ ไม่แตะ snapshot ของรอบเดิม ไม่แตะบรรทัดของรอบเดิม**
- ⛔ **ส่วนต่างต้องผ่านสายอนุมัติเหมือนรอบอื่น — ห้ามยิงเข้าเงียบ ๆ**
- **rules:** BR-30 · BR-32 · BR-43 | **test:** AT-88 · AT-96 · **IA-16**

**F-48 · `createReversalRun`** — เรียก `F-01` สร้างรอบใหม่ `run_type = กลับรายการ` พร้อม `references_run_no` → คัดลอกบรรทัดของรอบต้นฉบับแล้ว **กลับเครื่องหมายทั้งรอบ** → `F-49` · ⭐ **รอบต้นฉบับไม่ถูกแก้ ไม่ถูกลบ ไม่ถูกเขียนธงทับ** | **rules:** BR-33 | **test:** AT-89

**F-49 · `recordRunRelation`** ⭐⭐
- **ทำ:** เขียนแถวเดียวลง `payroll_run_relation` = `{new_run_no (owner), relation_kind: 'ปรับปรุง'|'กลับรายการ', references_run_no, created_at, created_by}`
- ⭐ **แถวนี้เป็นของรอบใหม่** · หน้ารอบเดิมแสดงความสัมพันธ์ด้วยการ query ย้อน (`WHERE references_run_no = <รอบเดิม>`)
- ⛔ **ห้าม `UPDATE payroll_run` ของรอบเดิมเพื่อเขียนธง** — นั่นคือการแก้รอบที่ปิดแล้ว (`C-7`)
- **rules:** BR-33 | **test:** AT-90 · AT-91 · **IA-17**

### หมวด H — ผลผลิตปลายทาง

**F-50 · `generateBankFile`** — ตรวจ `run_status = ปิดรอบแล้ว` → เลือกธนาคาร → อ่าน `bank_file.format_by_bank[]` (⚠️ **ยังไม่มี → ใช้รูปแบบกลาง CSV คอลัมน์มาตรฐาน `[AI-DEFAULT A-8]` และระบุชัดบนหน้าจอว่ายังไม่ใช่รูปแบบของธนาคารใด**) → **คนที่ไม่มีเลขบัญชีถูกแยกเป็นรายการ "ต้องจ่ายด้วยวิธีอื่น"** → `F-56` ยิง SecC `payroll.bank_file_exported` | **rules:** VR-21 | **test:** AT-100 · AT-101

**F-51 · `markBankFileSent`** — ⭐ **คนกดยืนยันเอง — ไม่มีการยืนยันอัตโนมัติจากธนาคาร** | **test:** AT-102

**F-52 · `buildGlPayload`** — จาก `F-33` → ประกอบตาม `00_OVERVIEW §0.13.5` (ครบด้าน) · ⛔ **ส่ง `payroll_code` + `cost_center` ไม่ส่งเลขบัญชี** (`OQ-PAY-08`) · **Module Linkage ปิด → สถานะ "รอปลายทาง" · ไม่ post · ไม่บล็อกการปิดรอบ** | **rules:** BR-40 | **test:** AT-103 · AT-104

**F-53 · `computeYtd`** — สะสมจากรอบที่ `ปิดรอบแล้ว` · `is_simulation = false` · **ปีภาษีเดียวกับ `pay_date`** `[AI-DEFAULT]` · ใช้ทั้งบนสลิป · ในสูตร D6 · และ surface PS-3 | **rules:** BR-42 | **test:** AT-113 · AT-86

**F-54 · `resolvePayslipAccess`** ⭐
- **ทำ:** ตัดสินสิทธิ์การเข้าถึงสลิป — เจ้าของ / (HR Payroll Officer · Comp Admin · ผู้อนุมัติของรอบ) ในขอบเขตบริษัทนั้น → **เอกสารเต็ม** (+ SecC เมื่อไม่ใช่เจ้าของ) · **อื่นทั้งหมด → `403 ERR_PAYSLIP_FORBIDDEN` + SecC `payroll.access_denied`**
- ⛔ **ไม่มีสาขาใดที่คืนเอกสารโดยที่ field เงินเป็น `null`/ปิดบัง — all-or-nothing**
- **rules:** BR-37 · VR-22 | **test:** AT-98 · AT-99 · **IA-19**

**F-59 · `maskAmountByPolicy`** — ถาม Policy Center ว่าผู้เรียกเห็น field ใดได้ → field ที่ไม่มีสิทธิ์คืน **สัญลักษณ์ปิดบัง ไม่ใช่ `0` และไม่ใช่ `null`** (แยกจาก `null` ของ `ยังคำนวณไม่ได้` อย่างชัดเจน) · ⛔ **feature นี้ไม่ทำ matrix สิทธิ์เอง** | **rules:** BR-38 | **test:** AT-105 · AT-106

### หมวด I — ร่องรอยและ event

**F-55 · `emitNotifyEvent`** — ยิง 7 event ตาม `05_RULES §5.9.1` · ⭐ **ยิงหลังธุรกรรมสำเร็จเท่านั้น** · `E2` **dedupe ตาม (`run_no`, `missing_config_groups[]`)** · `E4` เป็น fan-out รายคนที่ต้องส่งเป็น batch · ⛔ **ห้ามใส่จำนวนเงินใน payload · ห้ามแนบไฟล์** | **test:** AT-119 · **IA-22**

**F-56 · `emitCsqEvent`** — ยิง 8 event ตาม `05_RULES §5.9.2` (FC · AC · EC · SecC) · ⛔ **ไม่ตีมูลค่าเอง — ส่งจำนวนเงินที่คำนวณแล้วให้ `ENG-CSQ-02` เป็นผู้ตีมูลค่า** · ⛔ **payload ของ SecC ไม่มีตัวเลขที่ถูกเปิดดู** | **test:** AT-107 · AT-108 · **IA-21**

**F-57 · `logRunTimeline`** — เขียนไทม์ไลน์ **append-only** ทุกการกระทำ (ใคร/ทำอะไร/เมื่อไร/ผล) · ⛔ **ไม่มีการลบ ไม่มีการเขียนทับ** | **rules:** BR-29 | **test:** AT-109 · AT-110

---

## §3.2 Engines (Reusable / CUBIC-Registered)

> **Iron Rules (CUBIC 3-layer):** ⛔ engine ไม่รู้จัก HTTP (`req`/`res`/`header`/`status`) · input/output เป็น pure object · **feature ห้ามข้าม API ไปเรียก engine ตรง** — เรียกผ่าน Function ใน §3.1 เท่านั้น

### §3.2.1 ⭐ Engine ใหม่ที่เสนอให้ลงทะเบียน (7 ตัว — engine candidate สำหรับ Architect)

**ENG-PAY-01 · `payroll-gross-to-net-engine` (NEW)** ⭐⭐
- **หน้าที่:** เดินลำดับ E1·E2·E3 → D1·D2·D3 → **D4→D5→D6** → N ต่อคนหนึ่งคน · **ลำดับตายตัวบังคับที่ engine ไม่ใช่ที่การแสดงผล**
- **input:** `{employee_snapshot, salary_snapshot, attendance_snapshot, leave_snapshot, ot_snapshot, employment_window, config_bundle}` (ทั้งหมดเป็น pure object จาก snapshot)
- **output:** `{lines[]: {payroll_code, line_kind, direction, quantity, unit, rate_used, multiplier, amount|null, line_state, uncomputable_reason|null, source_ref}, net_total|null}`
- **⭐ สัญญาที่สำคัญที่สุด:** `config_bundle` ที่กลุ่มใดเป็น `null` → บรรทัดที่ขึ้นกับกลุ่มนั้นออกมาเป็น `line_state = 'ยังคำนวณไม่ได้'` · `amount = null` · **engine ไม่มีค่าเริ่มต้นภายในตัวเองเลย**
- **reusable ที่ไหน:** ทุกโมดูลที่ต้องแปลงเวลาเป็นเงินตามโครงเงินเดือน (Payroll · Expense ที่จ่ายผ่านเงินเดือน · การจำลองต้นทางในอนาคต)

**ENG-PAY-02 · `payroll-statutory-deduction-engine` (NEW)** ⭐⭐
- **หน้าที่:** คำนวณ D4 · D5 · D6 จากคีย์ config ล้วน ๆ — ประกันสังคม (ทั้งสองฝ่าย) · กองทุนสำรองเลี้ยงชีพ (สะสม+สมทบ) · ภาษีหัก ณ ที่จ่ายรายเดือน
- **input:** `{base_components[], flags:{is_ssf_base,is_pf_base,is_pit_base}, employee_statutory_profile, ytd, sso_config|null, pf_config|null, pit_config|null}`
- **output:** `{sso:{employee,employer}|null, pf:{employee,employer}|null, pit:{amount}|null, uncomputable:[{item, missing_keys[]}]}`
- ⭐ **engine นี้ต้องไม่มีตัวเลขตามกฎหมายอยู่ในตัวเองแม้แต่ตัวเดียว** — ทุกอัตรา เพดาน ขั้นบันได วิธีปัดเศษ มาจาก `*_config` ที่ส่งเข้ามา · `null` → `uncomputable` (`PI-1` · `IA-07`)
- **reusable ที่ไหน:** ทุกที่ที่ต้องคำนวณเงินหักตามกฎหมายไทย (Payroll · การจำลองต้นทุนพนักงานใหม่ · Accounting เมื่อมี)

**ENG-PAY-03 · `payroll-input-snapshot-engine` (NEW)**
- **หน้าที่:** เรียกต้นทางหลายที่ด้วย **วันที่ของเหตุการณ์ทางธุรกิจเดียวกัน** → ประกอบ snapshot + version block + hash + `superseded_by` chain
- **input:** `{sources[]: {feature, endpoint, params}, as_of_date}` · **output:** `{snapshots[], failed[], combined_version_ids}`
- **reusable ที่ไหน:** ทุก feature ที่ต้องตรึงข้อมูลหลายต้นทางไว้กับเอกสาร (Payroll · หนังสือรับรอง · รายงานที่ต้องทำซ้ำได้)

**ENG-PAY-04 · `payroll-variance-compare-engine` (NEW)**
- **หน้าที่:** เทียบชุดตัวเลขสองชุด (รายคน × รายองค์ประกอบ + ยอดรวม) → ส่วนต่างเป็นจำนวนกับร้อยละ + คนเข้า/คนหาย + ตีธงตามเกณฑ์ที่ส่งเข้ามา
- **input:** `{current_lines[], baseline_lines[], threshold|null}` · **output:** `{by_employee[], by_code[], entrants[], leavers[], flagged[], has_material_variance: bool|null}`
- ⭐ **`threshold = null` → `has_material_variance = null` และ `flagged = []`** (ไม่ใช่ `false`)
- **reusable ที่ไหน:** ทุกการทบทวนแบบเทียบงวดก่อน (Payroll · งบประมาณ · รายงานผลต่าง)

**ENG-PAY-05 · `payroll-retro-difference-engine` (NEW)**
- **หน้าที่:** คำนวณ **(ค่าที่ควรเป็นเมื่ออ่านค่าที่แก้แล้ว) − (ค่าใน snapshot ของรอบที่ปิด)** ต่อคนต่อองค์ประกอบ พร้อมเหตุผลที่ผูกกับเอกสารต้นทางที่ทำให้ต่าง
- **input:** `{closed_run_snapshot, current_source_data, employees[]}` · **output:** `{diff_lines[]: {employee_id, payroll_code, amount_diff, reason, source_ref}}`
- ⛔ **engine นี้ไม่มีสิทธิ์เขียนอะไรลงรอบเดิม — input เป็น read-only snapshot**
- **reusable ที่ไหน:** ทุกที่ที่ต้องทำ "รายการปรับปรุงงวดก่อน" โดยไม่คำนวณงวดเก่าใหม่ (`P-9`)

**ENG-PAY-06 · `payroll-bank-file-engine` (NEW)**
- **หน้าที่:** ประกอบไฟล์โอนตามรูปแบบของธนาคาร + แยกรายการที่โอนไม่ได้
- **input:** `{payment_lines[], bank_format|null}` · **output:** `{file_content, record_count, excluded[]}`
- ⭐ **`bank_format = null` → ใช้รูปแบบกลาง แล้วติดธงว่ายังไม่ใช่รูปแบบของธนาคารใด** `[AI-DEFAULT]`

**ENG-PAY-07 · `payroll-gl-payload-engine` (NEW)**
- **หน้าที่:** ประกอบชุดรายการบัญชีที่ **ครบด้าน** จากบรรทัดของรอบ (ค่าใช้จ่าย ↔ เจ้าหนี้)
- **input:** `{run_lines[], cost_centers[]}` · **output:** `{entries[]: {side, payroll_code, cost_center, amount}, balanced: bool}`
- ⛔ **ไม่ map เป็นเลขบัญชี** (`OQ-PAY-08`) · **`balanced` ต้องเป็น `true` เสมอ** — ถ้าไม่ ให้ล้มการปิดรอบ (ซึ่งไม่ควรเกิดเพราะ `BR-19` กันไว้)

### §3.2.2 Engine/Baseline ที่มีอยู่แล้ว — เรียกใช้ ไม่ implement ซ้ำ

| Engine | เจ้าของ | ใช้ทำอะไร | เรียกจาก |
|---|---|---|---|
| **`doa-resolve`** (DOA Engine) | baseline | คืนสายอนุมัติจริง (3–5 ขั้น) จาก `action_id` + บริบทที่ไม่ใช่เงิน | `F-35` |
| **`ENG-DOC-NUM`** | Document Configuration | ออกเลข `PAY-YYYY-NN` · `PS-YYYY-NNNNNN` | `F-01` · `F-41` |
| **`ENG-DOC-STORE`** | Document Configuration | เก็บ/คืนสำเนา PDF ถาวร | `F-42` · `F-54` |
| **`ENG-NOTIFY`** | baseline | ส่งการแจ้งเตือน 7 event | `F-55` |
| **`ENG-CSQ` (7C)** | baseline | รับ 8 event ผลลัพธ์ · **`ENG-CSQ-02` เป็นผู้ตีมูลค่า** | `F-56` |
| **Policy Center** | baseline | ตัดสินว่าผู้เรียกเห็น field ใดได้ | `F-59` · `F-54` |

> ⭐ **สิ่งที่ feature นี้ต้องไม่ทำเอง:** สายอนุมัติ · รูปแบบเลขเอกสาร · คลังไฟล์ · การส่งอีเมล · การตีมูลค่าท่อ 7C · matrix สิทธิ์ · **และค่าตามกฎหมายทุกตัว**

---

## §3.3 API ↔ Logic Trace Table (Phase 3.5 Anchor · R8)

| API | ชนิด | Function / Engine ที่ถูกเรียก | ตาราง (04_DB) |
|---|---|---|---|
| `API-01` GET `/payroll/runs` | read | — (query ตรง) + `F-59` | `payroll_run` |
| `API-02` GET `/payroll/runs/{run_no}` | read | `F-27` · `F-59` | `payroll_run` · `payroll_run_relation` |
| `API-03` POST `/payroll/runs` | **mutation** | **`F-01`** · `F-02` · `F-03` · `F-46` · `F-48` · `F-49` · `ENG-DOC-NUM` | `payroll_run` · `payroll_run_relation` |
| `API-04` GET `/payroll/periods` | read | `F-03` | — (อ่านจาก HR Config) |
| `API-05` POST `/payroll/runs/{run_no}/cancel` | **mutation** | **`F-44`** · `F-04` · `F-57` | `payroll_run` · `payroll_run_event` |
| `API-06` POST `/payroll/runs/{run_no}/pull` | **mutation** | **`F-44`** · `F-05` · `F-06` · `F-07` · `F-10` · `ENG-PAY-03` | `payroll_run_input_snapshot` · `payroll_run` |
| `API-07` GET `/payroll/runs/{run_no}/snapshot` | read | `F-06` · `F-07` · `F-43` | `payroll_run_input_snapshot` |
| `API-08` POST `/payroll/runs/{run_no}/pull/retry` | **mutation** | **`F-44`** · `F-08` → `F-05` | `payroll_run_input_snapshot` |
| `API-09` POST `/payroll/runs/{run_no}/repull` | **mutation** | **`F-44`** · `F-09` · `F-57` | `payroll_run_input_snapshot` · `payroll_run_line` |
| `API-10` GET `/payroll/runs/{run_no}/readiness` | read | `F-11` · `F-12` · `F-13` · `F-14` | `payroll_run_input_snapshot` |
| `API-11` GET `/payroll/runs/{run_no}/excluded` | read | `F-10` | `payroll_run` |
| `API-12` POST `/payroll/runs/{run_no}/calculate` | **mutation** | **`F-44`** · `F-15` · `F-16`…`F-27` · `F-29` · `F-30` · `F-31` · `ENG-PAY-01` · `ENG-PAY-02` · `ENG-PAY-04` | `payroll_run_line` · `payroll_run` |
| `API-13` GET `/payroll/runs/{run_no}/lines` | read | `F-59` | `payroll_run_line` |
| `API-14` GET `/payroll/runs/{run_no}/blockers` | read | `F-27` · `F-12` · `F-13` | `payroll_run_line` · `payroll_run` |
| `API-15` POST `/payroll/runs/{run_no}/lines/manual` | **mutation** | **`F-44`** · `F-28` · `F-57` | `payroll_run_line` |
| `API-16` GET `/payroll/runs/{run_no}/variance` | read | `F-30` · `F-31` · `F-59` · `ENG-PAY-04` | `payroll_run_line` |
| `API-17` POST `/payroll/runs/{run_no}/variance/{line_id}/review` | **mutation** | **`F-44`** · `F-32` | `payroll_run_line` |
| `API-18` GET `/payroll/runs/{run_no}/cost-summary` | read | `F-33` · `F-59` | `payroll_run_line` |
| `API-19` POST `/payroll/runs/{run_no}/submit` | **mutation** | **`F-44`** · **`F-36`** · `F-34` · `F-35` · `F-57` · `doa-resolve` | `payroll_run` |
| `API-20` GET `/payroll/runs/{run_no}/approval` | read | `F-34` · `F-35` | `payroll_run` |
| `API-21` POST `/payroll/runs/{run_no}/approve` | **mutation** | **`F-44`** · `F-37` · `F-57` | `payroll_run` |
| `API-22` POST `/payroll/runs/{run_no}/reject` | **mutation** | **`F-44`** · `F-38` · `F-39` · `F-57` | `payroll_run` |
| `API-23` POST `/payroll/runs/{run_no}/close` | **mutation** | **`F-44`** · **`F-40`** · `F-41` · `F-42` · `F-43` · `F-53` · `F-55` · `F-56` · `ENG-DOC-NUM` · `ENG-DOC-STORE` | `payroll_run` · `payslip` · `payroll_run_input_snapshot` |
| `API-24` GET `/payroll/runs/{run_no}/payslips` | read | `F-54` · `F-59` | `payslip` |
| `API-25` GET `/payroll/payslips/{payslip_no}` | read | **`F-54`** · `F-53` · `F-56` | `payslip` |
| `API-26` GET `/payroll/payslips/{payslip_no}/pdf` | read | **`F-54`** · `F-42` (อ่านสำเนา) · `F-56` | `payslip` |
| `API-27` POST `/payroll/runs/{run_no}/bank-file` | **mutation** | **`F-44`** · `F-50` · `F-56` · `ENG-PAY-06` | `payroll_run` · `payroll_run_event` |
| `API-28` POST `/payroll/runs/{run_no}/bank-file/mark-sent` | **mutation** | **`F-44`** · `F-51` · `F-57` | `payroll_run` |
| `API-29` GET `/payroll/runs/{run_no}/gl-payload` | read | `F-52` · `F-33` · `ENG-PAY-07` | `payroll_run_line` |
| `API-30` GET `/payroll/runs/{run_no}/timeline` | read | `F-57` | `payroll_run_event` |
| `API-31` GET `/payroll/adjust-queue` | read | `F-45` | `payroll_adjust_queue` |
| `API-32` GET `/payroll/runs/{run_no}/relations` | read | `F-49` | `payroll_run_relation` |
| `API-33` GET `/payroll/employees/{employee_id}/ytd` | read | `F-53` · `F-59` | `payslip` · `payroll_run` |
| `API-34` GET `/payroll/payslips` | read | `F-54` · `F-59` | `payslip` |
| `EVT-01` (listener) `attendance.*` · `leave.*` · `ot.*` · `salstruct.*` · `ofb_case_*` · `hrconfig.*` | **mutation** | `F-58` (ก่อนปิดรอบ) · **`F-45`** (หลังปิดรอบ) | `payroll_run` · `payroll_adjust_queue` |

**ตรวจ R8 (Phase 3.5 §C):**
- ✅ **mutation API ทั้ง 14 ตัว มี Function ≥ 1 ตัวใน trace** — และ **ทุกตัวเรียก `F-44 guardClosedRun` เป็นบรรทัดแรก**
- ✅ **Function ทั้ง 59 ตัวใน §3.1 ถูก trace อย่างน้อย 1 API** (ดูตารางย้อนกลับใน `INDEX.md §R8 Verification Matrix`)
- ✅ **Engine ทั้ง 7 ตัวใน §3.2.1 ถูก trace ผ่าน Function** — ไม่มี engine ที่ API เรียกตรง
- ✅ **ไม่มี orphan Function/Engine**
- ✅ **ไม่มี logic ซ่อนใน `02_API`** — `02_API` มีแต่สัญญา HTTP · validation ระดับ schema · แล้วเรียกต่อ
