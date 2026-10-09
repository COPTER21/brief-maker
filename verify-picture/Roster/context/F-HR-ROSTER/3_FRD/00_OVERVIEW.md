# 00_OVERVIEW — F-HR-ROSTER · Shift & Roster (จัดกะ)

> **FRD Pack · Variant FULL** (9 ไฟล์ + INDEX · **ไม่มี `PRINT_SPEC.md`**) · สร้างโดย `frd-generator-v6` **Lane Mode v2** · 2026-08-29
> **Phase 3.5: ✅ PASSED (A–M)** — รายงานเต็มอยู่ท้าย `INDEX.md`
> **ไม่มี `PRINT_SPEC.md` โดยเจตนา** — feature นี้ไม่มีท่อ `pdfdoc` (ตารางกะไม่ใช่เอกสารที่คนถือ · ไม่มีเลขที่ · ไม่มีลายเซ็น · ไม่มีแบบฟอร์มที่ต้องพิมพ์/ยื่น) ตามที่ `5_DECLARATIONS/NOT_NEEDED.md` และ `STANDARD_BASELINE.md §3` ตัดสินไว้ · **เขียนไว้ตรงนี้เพื่อไม่ให้ถูกเข้าใจว่าไฟล์หาย**

## §0.1 Document Control

| | |
|---|---|
| FRD ID | FRD-HR-ROSTER-001 |
| Feature | Shift & Roster · **จัดกะ** (ตารางกะรายเดือน คน × วัน) |
| Feature Code | `F-HR-ROSTER` |
| Module / Wave / Lane | HR · W2 · **Lane C** (ตัวสุดท้ายของเวฟ) |
| **Archetype** | **`P-planner`** — หน่วยที่คนทำงานด้วยคือ **ช่องในกริด (คน × วัน)** · **ไม่มีเลขที่เอกสาร ไม่มีลายเซ็น ไม่มี PDF ไม่มีสายอนุมัติ** · ตระกูลเดียวกับ Team Plan ✅ · Action Plan ✅ |
| Variant | **FULL** — 9 ไฟล์ (`00`…`07` + `INDEX`) · **ไม่มี `PRINT_SPEC.md`** (ไม่มี pdfdoc) |
| Source BRD | `2_BRD/BRD_จัดกะ.md` v1.0 (**AI Reviewed — APPROVED 28/28**) |
| Source HTML | `1_HTML/จัดกะ.html` · 4,210 บรรทัด · md5 `4f9db84787e9f2e9f9ea66e88b493c1b` · **5 routes** · ผ่าน S3a (FAIL=0) · S3b (BLOCK=0 · pageerror=0) · S3c (FN 73/73) |
| Declarations | `5_DECLARATIONS/NTF_BRIEF.md` (**6 event**) · `CSQ_BRIEF.md` (**2 event · EC ท่อเดียว · `kind: estimated`**) · `NOT_NEEDED.md` (DOA · DOCCFG · PDFDOC) |
| Data Classification สูงสุดที่ feature แตะ | **Confidential** (เหตุผลการขอสลับกะ · เหตุผลการปฏิเสธ · ข้อความ "แจ้งว่าทำไม่ได้" · หมายเหตุต่อช่อง) บนฐาน **PII** (ชื่อ · รหัส · ตำแหน่ง · แผนก) — **ไม่มี Restricted เพราะไม่มีค่าจ้างและไม่มีตัวเลขเงินเลย** |
| Owner | BA (lane runner · `feature-lane-runner` v2.3 · S5) |
| Created / Updated | 2026-08-29 |

## §0.2 Revision History

| Version | วันที่ | ผู้แก้ | สาระ |
|---|---|---|---|
| 1.0 | 2026-08-29 | `frd-generator-v6` Lane Mode v2 | สร้างจาก BRD v1.0 + HTML ที่ผ่าน gate ครบ · Coverage Manifest **73 FN / 73 Story / 33 BR / 58 Scenario** · **§0.13 Published Roster Surface** (สัญญาถึง Attendance · OT · ESS) · **§0.16 Declaration Conformance** (event ⊆ brief) |

## §0.3 Scope

### In Scope

ยกมาจาก `BRD §3.1` **IN-01…IN-32** ครบทุกข้อ · สรุปเป็นก้อนงานของ dev:

| ก้อน | เนื้อหา | ไฟล์ที่ระบุรายละเอียด |
|---|---|---|
| **G-1 กริดกับการลงกะ** | กริดคน × วัน · กางจากแพทเทิร์น/กะหมุน/คัดลอกเดือนก่อน · ลาก/เลือก/ล้าง/ทาช่วง/กะแยกช่วง · หมายเหตุต่อช่อง | `01_UI §1.2 P-01` · `03_LOGIC §3.1 F-01…F-14` · `04_DB T_roster_cell` |
| **G-2 ตัวตรวจข้อขัดแย้ง** | ชนกัน (รวมข้ามคืน) · พักไม่พอ · เกินชั่วโมง · วันติดกัน · วันลา · วันหยุด · ธง OT · freeze · หลังวันออก | **`03_LOGIC §3.0` + `§3.2 ENG-ROSTER-CONFLICT`** · `05_RULES BR-06…BR-13 · BR-31 · BR-32` |
| **G-3 เวอร์ชันกับการเผยแพร่** | ร่าง/เผยแพร่/เผยแพร่ซ้ำ/ล็อก/ทิ้งร่าง · ด่านก่อนเผยแพร่ · **การปฏิเสธรายวัน** · การรับทราบคำเตือน | `01_UI §1.2 P-02` · `03_LOGIC §3.1 F-20…F-30` · `05_RULES §5.2` |
| **G-4 คำขอสลับกะ** | 6 สถานะ · ผลตรวจจาก engine ตัวเดียวกัน · atomic 2 ช่อง · ผู้ยืนยันจาก Policy Center | `01_UI §1.2 P-03` · `03_LOGIC §3.1 F-31…F-42` · `05_RULES §5.2.2` |
| **G-5 สิ่งที่เผยแพร่ให้ปลายทาง** | read model 2 มุมมอง · Module Linkage · where-used · **ไม่มีทางเขียนกลับ** | **`§0.13`** · `02_API §2.3` · `03_LOGIC §3.1 F-43…F-50` |
| **G-6 ประวัติ สิทธิ์ การรับทราบ** | ประวัติ append-only · ขอบเขตจาก Policy Center · การรับทราบกะของพนักงาน | `01_UI §1.2 P-04` · `03_LOGIC §3.1 F-51…F-57` · `04_DB T_roster_history` |
| **G-7 การประกาศ** | 6 event แจ้งเตือน (ENG-NOTIFY) · 2 event 7C (ENG-CSQ · EC `estimated`) | **`§0.16`** · `03_LOGIC §3.1 F-58…F-60` |

### Out of Scope

ยกมาจาก `BRD §3.2` **OUT-01…OUT-19** — รายการเต็มพร้อมเจ้าภาพอยู่ที่ **`§0.12.3b`** และบนหน้าจอจริงที่แท็บ *ปลายทางและขอบเขต* (19 แถว)

**สรุปสั้น:** ไม่ทำ capacity/coverage · ไม่ทำต้นทุนแรงงาน (**ไม่มีตัวเลขเงินเลย**) · ไม่ทำ optimizer · ไม่มี open shift · ไม่มีทะเบียนทักษะ · ไม่ทำพอร์ทัลพนักงาน · **ไม่มีเอกสาร/เลขที่/ลายเซ็น/PDF** · ไม่ทำหน้าตั้งค่าของ HR Configuration · **ไม่เขียนค่ากฎหมายเอง** · ไม่แตะเวลาจริง/ใบ OT/โควตาลา · **ไม่มี DOA** · ไม่มี hard delete · ไม่มีการ์ด 7C · ไม่มี UI สลับบริษัท · ไม่มีมุมมองรายกะ · ไม่มีรายงานสถิติ · ไม่มีหลายคนต่อกะ

### Out of Scope (จาก Phase 2.5 probing — บันทึกไว้ไม่ให้หายเงียบ)

| # | สิ่งที่ probe แล้วตัดสินให้ไม่ทำ | เหตุผล | tag |
|---|---|---|---|
| PB-01 | **การนำเข้าตารางจากไฟล์ตารางคำนวณ** | ไม่มีในต้นทางใด ๆ · ถ้าทำจะต้องมีตัวจับคู่ชื่อกะที่ไม่มีทะเบียนกลางรองรับ — เสี่ยงสร้างกะนอกทะเบียน (ขัด C-2) | `[AI-DEFAULT]` |
| PB-02 | **การพิมพ์ตารางเป็นไฟล์** | ไม่มีท่อ pdfdoc · การพิมพ์หน้าจอเป็นความสามารถของเบราว์เซอร์ | `[AI-DEFAULT]` |
| PB-03 | **การแจ้งเตือนแบบสรุปรายสัปดาห์** | ENG-NOTIFY เป็นเจ้าของการรวมข้อความ — feature ประกาศ event ต่อเหตุการณ์เท่านั้น | `[AI-DEFAULT]` |
| PB-04 | **การคืนค่าตารางเวอร์ชันเก่ากลับมาเป็นปัจจุบัน (rollback)** | ขัดกับ append-only ในเชิงความหมาย — ถ้าต้องการผลเดิม ให้ **แก้แล้วเผยแพร่ซ้ำเป็นเวอร์ชันใหม่** ซึ่งได้ผลเดียวกันโดยที่ร่องรอยไม่ขาด | `[AI-DEFAULT]` · **LD-ROS-09** |
| PB-05 | **การแก้ตารางแบบหลายเดือนพร้อมกัน** | ตารางผูกกับเดือนเดียวตาม OQ-R10 · การแก้ข้ามเดือนต้องเปลี่ยนหน่วยของเวอร์ชันทั้งชุด | `[AI-DEFAULT]` |

## §0.4 Roles & Responsibilities (COSO)

| Role | COSO | ทำอะไร | ที่มาของสิทธิ์ |
|---|---|---|---|
| **พนักงาน** | Maker (ของคำขอสลับกะ) · ผู้รับผลของตาราง | ยื่น/ตอบรับ/ถอนคำขอสลับกะ · รับทราบกะของตัวเอง | Policy Center (เห็นของตัวเองเฉพาะที่ `published`) |
| **คู่สลับ** | **Checker ที่ 1** | ตอบรับ/ปฏิเสธคำขอที่ยื่นมาหาตัวเอง | เป็นคู่สลับของคำขอนั้น |
| **หัวหน้า / ผู้จัดตาราง** | Maker (ของตาราง) · **Checker ที่ 2** (ของคำขอสลับ) | กางตาราง · แก้ช่อง · เผยแพร่/เผยแพร่ซ้ำ · ยืนยัน/ปฏิเสธคำขอสลับของลูกทีม | Policy Center (สายบังคับบัญชา) |
| **HR Admin** | Maker · Checker · ผู้ตั้งค่าการเชื่อม | เหมือนหัวหน้า + ข้ามทีม + ตั้ง Module Linkage | Policy Center (ระดับบริษัท) |
| **ระบบ (engine + scheduler)** | System | รันตัวตรวจ · ล็อกเมื่องวดปิด (T-5) · ปิดคำขอที่หมดอายุ (W-6) · ยิง event | — |
| **ระบบปลายทาง** | Consumer | อ่าน read model | **อ่านอย่างเดียว · ไม่มีทางเขียนกลับ** |
| **Approver** | — | **ไม่มีในระบบนี้** | **feature นี้ไม่มีสายอนุมัติ — เหตุผลเต็มที่ `BRD §4.3`** |

> **SoD:** Maker(ผู้ขอ) ≠ Checker1(คู่สลับ · บังคับที่ `05_RULES VR-14`) ≠ Checker2(หัวหน้าของผู้ขอ · `05_RULES BR-23`) · **ไม่มีเคส Maker = Approver เพราะไม่มี Approver** · กรณีขอบที่สายบังคับบัญชาชี้กลับมาที่ตัวเอง → **ปุ่มยืนยันไม่ปรากฏ** (`07_LOCKED OQ-R19`)

## §0.5 Dependencies

### Upstream (feature นี้ต้องพึ่ง)

| ต้นทาง | อ่านอะไร | ทางเข้า | กติกาที่ต้องทำตาม |
|---|---|---|---|
| **HR Configuration ✅** | `shift_pattern` · `holiday_calendar` · `period_rule` (+`pay_period`) | `GET /api/v1/hr-config/resolve?date=&company_id=&group=` | **C-1…C-6** (`§0.14.2`) · **P-1…P-9** |
| **HR Configuration — `shift_rule` ❌** | `min_rest_hours` · `max_hours_week` · `max_consecutive_days` · `freeze_days` | (เดียวกัน) | **ยังไม่มีคีย์** → `null` → **ไม่ตรวจกฎนั้น + ป้าย "ยังไม่มีค่าให้อ่าน"** (**OQ-STD-R6 · OQ-R15**) |
| **Employee Master ✅** | คน · ตำแหน่ง · แผนก · วันพ้นสภาพ | combobox (#102) | soft ref + snapshot · **ไม่มี FK cascade** |
| **Policy Center ✅** | ขอบเขตการเห็น · สายบังคับบัญชา | `ENG-ROLESCOPE-01` | **ห้ามเขียนตรรกะสิทธิ์เอง** |
| **Attendance ✅** | `day_status` · `period_status` | `GET /api/v1/attendance/resolve` | **AT-1…AT-7** (`§0.14.3`) · **ห้ามเขียนกลับ · ห้ามคำนวณชั่วโมงเอง** |
| **Leave ✅** | วันลาที่อนุมัติแล้ว | `GET /api/v1/leave/resolve` | soft ref · display-only |
| **OT / Shift ✅** | ใบ OT ของวัน | `GET /api/v1/ot/resolve` | **OT-1…OT-7** (`§0.14.3`) · display-only |
| **ENG-NOTIFY ✅** | — (ประกาศ event) | `ENG-NOTIFY.emit(event_id, {ref, vars})` | **ห้าม hardcode ช่องทาง ห้ามเช็ค preference เอง** |
| **ENG-CSQ 7C ✅** | — (ประกาศ event) | `ENG-CSQ.emit(profile, event, payload)` | **ประกาศเท่านั้น ห้ามตีมูลค่าเอง** |

### Downstream (feature ที่พึ่ง feature นี้) — **อ่าน `§0.13`**

| ปลายทาง | สถานะ | อ่านอะไร | ทำไม |
|---|---|---|---|
| **Attendance ✅ (W1)** ⭐ | เชื่อมได้ทันที | มุมมอง `day` — `shift` object 8 ฟิลด์ + `roster_version_id` + `shift_pattern_version_id` | **`FN-C03 resolveShiftForDay` แหล่งลำดับ ①** — **นี่คือเหตุผลที่ feature นี้มีอยู่** |
| **OT / Shift ✅ (W2 lane B)** | เชื่อมได้ทันที | กรอบกะของวัน + `work_days[]` ที่ใช้จริง | ระบุว่า "นอกกะ" คือช่วงไหน · วันหยุดประจำสัปดาห์จริงของคนนั้น → ตัดสิน `rate_type` |
| **ESS Portal ⏳ (W6)** | ยังไม่มี | มุมมอง `period` + สถานะคำขอสลับกะของตัวเอง | "เวรของฉัน" · เรียกหน้าของ feature นี้เมื่อต้องทำอะไร (OQ-HR-04) |
| **ชั้นรายงาน 7C ✅** | เชื่อมได้ทันที | event `roster.published` · `roster.republished` (**EC `estimated`**) | ENG-CSQ-02 ตีมูลค่าเอง — **feature นี้ไม่มีเงินให้ตี** |
| **Payroll ⏳ (W4)** | **ไม่อ่านจากที่นี่** | — | Payroll อ่านชั่วโมงจริงจาก Attendance กับ OT · **`planned_hours` ห้ามใช้เป็นฐานจ่าย** |

### External
**ไม่มี** — feature นี้ไม่เรียกระบบภายนอกองค์กรใด ๆ

## §0.6 Stack & Architecture

```
┌── FE (SPA · hash routing) ────────────────────────────────┐
│  #/roster/grid · #/roster/publish · #/roster/swap          │
│  #/roster/history · #/roster/downstream                    │
│  (1 เมนูซ้าย + 5 tab ในหน้า — #104 · refresh-safe ทุก route)│
└───────────────┬───────────────────────────────────────────┘
                │ REST (JSON) — ทุกคำขอส่ง company_id + date
┌───────────────▼── API layer (02_API) ─────────────────────┐
│  ผูก HTTP → เรียก Function/Engine เท่านั้น                  │
│  **ห้ามมี business logic ในชั้นนี้** (Logic Placement)      │
└───────────────┬───────────────────────────────────────────┘
┌───────────────▼── Logic layer (03_LOGIC) ─────────────────┐
│  Function 60 ตัว (camelCase)                               │
│  Engine 7 ตัว (kebab-case) — ★ ENG-ROSTER-CONFLICT ใหม่    │
│  · pure object in / pure object out · ไม่รู้จัก HTTP        │
└───────────────┬───────────────────────────────────────────┘
┌───────────────▼── Data layer (04_DB) ─────────────────────┐
│  T_roster_version · T_roster_cell · T_roster_swap_request  │
│  T_roster_ack · T_roster_history (append-only ที่ชั้น DB)   │
└───────────────┬───────────────────────────────────────────┘
                │ soft reference (LD-4C-02) · ไม่มี FK cascade
┌───────────────▼── ระบบอื่น ────────────────────────────────┐
│  HR Config · Employee Master · Policy Center                │
│  Attendance · Leave · OT   ← อ่านอย่างเดียวทั้งหมด          │
│  ENG-NOTIFY · ENG-CSQ      ← ประกาศอย่างเดียว               │
└───────────────────────────────────────────────────────────┘
                ▲
     Published Roster Surface (read model · §0.13)
     ── ไม่มีลูกศรย้อนกลับเข้ามาเลย (BR-20) ──
```

**ข้อกำหนดเชิงสถาปัตยกรรมที่ห้ามผิด:**
1. **Engine ห้ามรู้จัก HTTP** — รับ/คืน object ล้วน (Phase 3.5 Section F)
2. **API ห้ามมี business logic** — ทุก mutation ต้อง trace ไป Function/Engine (R8 · Phase 3.5 Section C)
3. **`ENG-ROSTER-CONFLICT` ต้องถูกเรียกจากทั้งการแก้ด้วยมือและการสลับกะ** — **ห้ามเขียนตรรกะตรวจสองชุด** (`05_RULES C-17`)
4. **ไม่มี write endpoint สำหรับ consumer แม้แต่ตัวเดียว** (ยกเว้น `usage` ซึ่งเป็นการลงทะเบียน ไม่ใช่การเขียนข้อมูล)

## §0.7 Multi-Tenant & Security Context

- **ทุกคำขอผูกกับ `company_id`** ที่มาจาก login — ตารางหนึ่งผูกบริษัทเดียวเสมอ (`05_RULES BR-28`) · **ยังไม่มี UI สลับบริษัท** (OQ-HR-05)
- **ขอบเขตการเห็นมาจาก Policy Center (`ENG-ROLESCOPE-01`) เท่านั้น** — กรองที่ระดับ query ไม่ใช่ซ่อนปุ่ม (`05_RULES §5.3`)
- **RLS:** แถวของ `T_roster_*` ทุกตารางถูกกรองด้วย `company_id` + ขอบเขตของผู้ใช้ — คำขอข้ามผู้เช่าคืน 404 ไม่ใช่ 403
- **Security Preset: P6 (HR/PII Sensitive)** + ยืม 3 controls จาก P7 (read model เปิดให้ 3 consumer) — รายละเอียดที่ `05_RULES §5.7`

### §0.7.1 Data Classification Summary ⭐

| ชั้น | มีในระบบนี้? | ตัวอย่าง field | มาตรการ |
|---|---|---|---|
| **Restricted** | ❌ **ไม่มี** | — | **feature นี้ไม่มีค่าจ้างและไม่มีตัวเลขเงินเลย** (`05_RULES BR-27`) |
| **Confidential** | ✅ | `request_reason` · `reject_reason` · `ack_note` · `cell_note` | ไม่ส่งออกไป read model · ไม่ส่งเข้า payload 7C · เห็นเฉพาะผู้เกี่ยวข้องตามขอบเขต |
| **PII** | ✅ | `employee_id` · `employee_name_snapshot` · `employee_position_snapshot` · `employee_dept_snapshot` · `published_by` · `confirmed_by` | masking ตาม Policy Center · **payload 7C ส่งเฉพาะ id ห้ามส่งชื่อดิบ** |
| **Internal** | ✅ | `roster_version_id` · `shift_code` · เวลา · `conflict_flags[]` · `config_version_ids` | ตามขอบเขตปกติ |
| **Public** | ❌ ไม่มี | — | ไม่มี field ใดเป็นข้อมูลสาธารณะ |

**ชั้นสูงสุดที่ feature นี้แตะ = `Confidential`** — ตารางเต็มรายคอลัมน์อยู่ที่ `04_DB §4.6`

## §0.8 Open Questions

**30 ข้อ** — รายการเต็มพร้อม default · tag · เจ้าภาพ อยู่ที่ **`07_LOCKED_DECISIONS §7.3`**

**ที่บล็อกงาน dev (ต้องเคาะก่อนเริ่ม):** `OQ-R11` (ผู้ยืนยันเมื่อคนละหัวหน้า) · `OQ-R12` (ระดับของการทับวันลา) · `OQ-R19` (หัวหน้าสูงสุดของสายยื่นคำขอเอง) · `OQ-CSQ-01` (`profile_id`) · `OQ-NTF-01/02` (ชื่อ event + กลุ่มใหม่)
**ที่เร่งที่สุดเชิงความเสี่ยงแต่ไม่บล็อก:** **`OQ-STD-R6` + `OQ-R15`** — คีย์ `shift_rule.*` ที่ HR Configuration ยังไม่เผยแพร่ ทำให้ **กฎ 4 ข้อจาก 33 ข้อไม่ถูกบังคับใช้เลยในรอบนี้**

### §0.8.1 Phase 2.5 Probing — ผลที่ใช้ default (Lane Mode · no-ask)

| # | ประเด็นที่ probe | default ที่ใช้ | tag | ผูกที่ |
|---|---|---|---|---|
| PR-01 | **หน่วยของ `roster_cell` เมื่อมีกะแยกช่วง** | เพิ่ม `slot_seq` เข้า unique key แทนการเปลี่ยนโครงกริด | `[AI-DEFAULT]` | `04_DB §4.2` · `LD-ROS-04` |
| PR-02 | **เก็บ `hours_per_day` เป็นสำเนาหรือคำนวณสด** | **สำเนาจากต้นทาง** — เพราะตารางที่เผยแพร่ต้องคงที่ และ **ห้ามคำนวณเอง** (DI-01) | `[AI-DEFAULT]` | `04_DB §4.2` · `05_RULES BR-21` |
| PR-03 | **เก็บผลตรวจ (`conflict_flags`) ลงฐานข้อมูลหรือคำนวณสดทุกครั้ง** | **เก็บลงฐานข้อมูล** สำหรับเวอร์ชันที่ `published` (เพื่อพิสูจน์ย้อนหลังว่าตอนเผยแพร่ผลตรวจเป็นอย่างไร) · ร่างคำนวณสด | `[AI-DEFAULT]` | `04_DB §4.2` · `LD-ROS-05` |
| PR-04 | **การเผยแพร่ซ้ำที่ทุกวันถูกปฏิเสธ** | **ไม่ออกเวอร์ชันใหม่** · แสดงรายการวันที่ถูกปฏิเสธครบ | `[AI-DEFAULT]` | `03_LOGIC F-24` · `05_RULES ST-E04` |
| PR-05 | **การเผยแพร่ซ้ำที่ไม่มีการเปลี่ยนแปลงเลย** | **ไม่ออกเวอร์ชันใหม่** — ปุ่มอยู่ในสถานะกดไม่ได้ | `[AI-DEFAULT]` | `03_LOGIC F-23` · `05_RULES EC-25` |
| PR-06 | **ขอบเขตช่วงวันสูงสุดต่อคำขอ read model** | **62 วัน** — ตระกูลเดียวกับ Attendance `§0.13.2` | `[AI-DEFAULT]` | `02_API §2.3` · `05_RULES TH-07` |
| PR-07 | **cache ของค่าจากต้นทาง** | **ภายในวันเดียว** · ล้างเมื่อได้ `hrconfig.effective` (C-3) | `[AI-DEFAULT]` | `03_LOGIC F-02` |
| PR-08 | **ผลตรวจของคำขอสลับควรแสดงข้อขัดแย้งเดิมด้วยหรือเฉพาะที่เกิดใหม่** | **เฉพาะที่เกิดใหม่จากการสลับ** — ไม่งั้นหัวหน้าจะเห็นปัญหาที่ไม่ได้เกิดจากการตัดสินใจของตัวเอง | `[AI-DEFAULT]` | `03_LOGIC F-36` · `LD-ROS-07` |
| PR-09 | **การรับทราบกะเมื่อเผยแพร่ซ้ำ** | **รีเซ็ตเฉพาะคนที่กะเปลี่ยน** — คนที่กะไม่เปลี่ยนคงสถานะเดิม | `[AI-DEFAULT]` | `03_LOGIC F-56` · `LD-ROS-08` |
| PR-10 | **หน่วยเวลาในการเทียบเส้นเวลา** | **นาทีนับจากเที่ยงคืนของวันเข้ากะ** (`is_overnight` → +1440) — ไม่ใช้ timestamp เพื่อเลี่ยงปัญหาเขตเวลา | `[AI-DEFAULT]` | `03_LOGIC §3.0.1` · `LD-ROS-01` |

## §0.9 Glossary

ยกจาก `BRD Appendix B` — เพิ่มคำเชิงเทคนิคของแพ็กนี้:

| คำ | ความหมาย |
|---|---|
| **เส้นเวลาต่อเนื่อง (continuous timeline)** | นาทีนับจาก 00:00 ของ `work_date` — กะที่ `is_overnight` มีเวลาออก = เวลานาฬิกา + 1440 (`03_LOGIC §3.0.1`) |
| **ช่วง (interval)** | คู่ `[start_min, end_min)` บนเส้นเวลาต่อเนื่อง — **ปลายเปิด** ทำให้ "จบพอดีแล้วเริ่มพอดี" **ไม่ทับกัน** |
| **`slot_seq`** | ลำดับกะในวันเดียวกันของคนเดียวกัน (1 = กะแรก · 2+ = กะแยกช่วง) |
| **แหล่งลำดับ ①** | ลำดับแรกของ `FN-C03 resolveShiftForDay` ของ Attendance = ตารางที่ feature นี้เผยแพร่ |
| **ทางสำรอง ②** | `shift_pattern` มาตรฐาน ที่ Attendance ใช้เมื่อแหล่ง ① คืน `null` |
| **`noValue` (ยังไม่มีค่าให้อ่าน)** | สถานะของกฎที่เกณฑ์เป็น `null` เพราะต้นทางยังไม่เผยแพร่คีย์ — **ข้ามการตรวจ + แสดงป้าย** |
| **บริโภคแล้ว (consumed)** | `day_status ∈ {confirmed, locked}` ที่ Attendance **หรือ** `period_status = closed` |

## §0.10 Pack Navigation

| ไฟล์ | Audience | เนื้อหาหลัก |
|---|---|---|
| `00_OVERVIEW.md` | ทุกคน | ไฟล์นี้ — Document control · Scope · Roles · Dependencies · **§0.12 Coverage Manifest (73 FN)** · **§0.13 Published Roster Surface** · §0.14 Data Contract · §0.15 Soft Reference · **§0.16 Declaration Conformance** |
| `01_UI.md` | FE | **§1.0 Layout Decision Log** · Page Inventory **5 หน้า** · รายละเอียดต่อหน้า · COSO touchpoints · empty state |
| `02_API.md` | BE (HTTP) | endpoint ทั้งหมด · contract ของตัวที่มีสัญญาเฉพาะ · **§2.4 API → Logic Trace** · Cross-Module Contract |
| **`03_LOGIC.md`** | BE (ตรรกะ) | **§3.0 กลไกของตัวตรวจข้อขัดแย้ง (หัวใจของแพ็ก)** · 60 Function · **7 Engine (ใหม่ 3)** · Trace Table |
| `04_DB.md` | DBA / BE | 5 ตาราง · classification ครบทุกคอลัมน์ · ER · migration · retention · performance |
| `05_RULES.md` | BE + QA | BR-01…BR-33 · State machine · Permission · VR-01…VR-26 · Edge Case · **Error catalog** · Security · Compliance |
| `06_TESTS.md` | QA | **AT-01…AT-62** · **IA-01…IA-10 (invariant · ตกข้อใดข้อหนึ่ง = หยุด release)** · test data · DoD · cross-module · **microcopy verbatim** |
| `07_LOCKED_DECISIONS.md` | ทุกคน | **§7.0 Scope Lock 14 ข้อ (IMMUTABLE)** · LD-ROS-01…12 · Convention deviation · **OQ 30 ข้อ** · tradeoff |
| `INDEX.md` | ทุกคน | สารบัญ · Quick Nav · Cross-Reference · **Phase 3.5 Report** |
| ~~`PRINT_SPEC.md`~~ | — | **ไม่มีในแพ็กนี้** — feature ไม่มีท่อ `pdfdoc` (ไม่ใช่เอกสารที่คนถือ) · **ระบุไว้เพื่อไม่ให้ถูกเข้าใจว่าไฟล์หาย** |
| `UI_BRIEF_จัดกะ.md` | FE + BA | (สร้างที่ S7) สรุปหน้าจอ + **Drift Log** |

## §0.11 Scope Lock (pointer)

**14 LOCK** สืบทอดจาก `BRD §3.4` → เก็บฉบับเต็มที่ **`07_LOCKED_DECISIONS §7.0` (IMMUTABLE)**
`LOCK-DOA` · `LOCK-SLOT` · `LOCK-SOFTREF` · `LOCK-AUDIT` · `LOCK-HR1` · `LOCK-ENGINE` · `LOCK-LINKAGE` · `LOCK-7C` · `LOCK-UI` · `LOCK-UPSTREAM-CFG` · `LOCK-UPSTREAM-ATT` · `LOCK-UPSTREAM-OT` · `LOCK-MONEY` · `LOCK-MENU`

**ตรวจแล้ว: ไม่มี spec ใดในแพ็กนี้ขัด LOCK ข้อใด** (Phase 3.5 Section L)

## §0.12 Coverage Manifest ⭐ (R13 — กัน requirement หล่น BRD→FRD · **มีคอลัมน์ FN-XX ตาม Lane Mode v2**)

### §0.12.0 Function Ledger — **73/73 FN** → ที่อยู่ในแพ็ก

| FN | ความสามารถ (ย่อ) | UI | API | LOGIC | DB | RULES | TESTS |
|---|---|---|---|---|---|---|---|
| FN-01 | กางตารางเดือนเป็นกริดคน × วัน | `§1.2 P-01` | `API-01` | `F-01` `F-03` | `T_roster_version` `T_roster_cell` | BR-01 | AT-01 |
| FN-02 | resolve ณ วันของช่อง + เก็บ `config_version_ids` | `§1.2 P-01 หัวตาราง` | `API-01` | `F-02` `F-04` | `config_version_ids` · `shift_pattern_version_id` | BR-01 · BR-02 | AT-02 |
| FN-03 | คัดลอกเดือนก่อน (resolve ใหม่) | `§1.2 P-01 drawer กาง` | `API-01` | `F-05` | — | BR-01 | AT-03 |
| FN-04 | บล็อกการกางเมื่อ resolve ไม่สำเร็จ | `§1.2 P-01 toast` | `API-01` | `F-02` | — | BR-01 · VR-02 | AT-04 |
| FN-05 | ลากกะลงช่อง | `§1.2 P-01 แถบกะ` | `API-03` | `F-09` `F-14` | `T_roster_cell` | BR-07…BR-13 | AT-05 |
| FN-06 | เลือกกะจาก picker ในช่อง | `§1.2 P-01 drawer ช่อง` | `API-03` | `F-09` | — | BR-04 · VR-05 | AT-06 |
| FN-07 | ทาช่วงหลายช่อง | `§1.2 P-01 ปุ่มทาช่วง` | `API-04` | `F-10` `F-14` | — | BR-07…BR-13 | AT-07 |
| FN-08 | ล้างกะ · ช่องว่าง = วันหยุดของคนนั้น | `§1.2 P-01` | `API-03` | `F-11` | — | BR-19 · BR-26 | AT-08 |
| FN-09 | กะ `inactive` หายจาก picker แต่ช่องเก่าแสดงได้ | `§1.2 P-01 drawer ช่อง` | `API-02` | `F-06` | `shift_name_snapshot` | BR-04 | AT-09 |
| FN-10 | แถวคน inline ≤52px + combobox คน | `§1.0 LD-UI-02` `§1.2 P-01` | `API-02` | `F-07` | `employee_*_snapshot` | — | AT-10 |
| FN-11 | ชนกัน — ช่วงเวลาทับกัน (ห้าม) | `§1.2 P-01 แผงข้อขัดแย้ง` | — | **`§3.0.2` `F-15`** · **ENG-ROSTER-CONFLICT** | `conflict_flags[]` | **BR-07** | AT-11 · **IA-03** |
| FN-12 | ชนกันข้ามคืน (ห้าม) | `§1.2 P-01` | — | **`§3.0.1` `F-15`** | `is_overnight` | BR-06 · BR-07 | AT-12 · **IA-03** |
| FN-13 | พักไม่พอ (ห้าม · เมื่อมีค่า) | `§1.2 P-01` | — | **`§3.0.3` `F-16`** | — | BR-08 | AT-13 |
| FN-14 | เกินชั่วโมงสัปดาห์ (เตือน · เมื่อมีค่า) | `§1.2 P-01 drawer ช่อง` | — | `F-17` | — | BR-09 | AT-14 |
| FN-15 | วันติดกันเกิน (เตือน · เมื่อมีค่า) | `§1.2 P-01` | — | `F-18` | — | BR-10 | AT-15 |
| FN-16 | **ป้าย "ยังไม่มีค่าให้อ่าน" 4 คีย์ + ลิงก์ต้นทาง** | `§1.2 P-01 การ์ดค่านโยบาย` (5 ผิว) | `API-02` | **`§3.0.4` `F-08`** | `config_version_ids.shift_rule = null` | **BR-11** | AT-16 · **IA-06** |
| FN-17 | ทับวันลาที่อนุมัติแล้ว (ห้าม) | `§1.2 P-01` | `API-02` | `F-19` | `leave_ref` | BR-12 | AT-17 |
| FN-18 | วันหยุดนักขัตฤกษ์ (เตือน) + ระบายแกนวัน | `§1.2 P-01 หัวคอลัมน์วัน` | `API-02` | `F-20` | `holiday_ref` | BR-12 | AT-18 |
| FN-19 | ธง "มี OT" display-only | `§1.2 P-01` | `API-02` | `F-21` | `ot_ref` | BR-13 | AT-19 |
| FN-20 | แผงข้อขัดแย้งกดกระโดดไปช่อง + แยกระดับ | `§1.2 P-01` | — | `F-22` | `conflict_level` | BR-14 | AT-20 |
| FN-21 | ร่างมองไม่เห็นจากภายนอก · ไม่ยิง event | `§1.2 P-02` | `API-10` | `F-43` | `roster_status` | BR-18 | AT-21 · **IA-01** |
| FN-22 | ทิ้งร่าง (ยังอยู่ในประวัติ) | `§1.2 P-02` | `API-08` | `F-29` | `roster_status='discarded'` | BR-26 | AT-22 |
| FN-23 | เผยแพร่ + แจ้งเตือนทุกคนที่มีกะ | `§1.2 P-02` | `API-06` | `F-23` `F-25` `F-58` `F-59` | — | BR-14 · BR-15 | AT-23 |
| FN-24 | บล็อกเผยแพร่เมื่อมี "ห้าม" ค้าง | `§1.2 P-02 ด่าน` | `API-06` | `F-22` `F-23` | — | BR-14 · VR-10 | AT-24 · **IA-02** |
| FN-25 | รับทราบคำเตือน + บันทึกใครรับทราบอะไร | `§1.2 P-02 modal` | `API-05` | `F-26` | `warning_ack_*` | BR-14 · BR-26 | AT-25 |
| FN-26 | เผยแพร่ซ้ำ = เวอร์ชันใหม่ + เหตุผลบังคับ | `§1.2 P-02` | `API-07` | `F-27` `F-28` | `supersedes`/`superseded_by` | BR-15 · VR-13 | AT-26 |
| FN-27 | **ปฏิเสธรายวันที่ปลายทางบริโภคแล้ว** | `§1.2 P-02 แผงวันที่ถูกปฏิเสธ` | `API-07` | **`§3.0.5` `F-24`** | `consumed_by_attendance` | **BR-16** | AT-27 · **IA-04** |
| FN-28 | ล็อกทั้งเดือนเมื่องวดปิดที่ต้นทาง | `§1.2 P-01/P-02 แถบสถานะ` | `API-15` | `F-30` | `roster_status='locked'` | BR-16 | AT-28 |
| FN-29 | แจ้งเฉพาะคนที่กะเปลี่ยน + event ล้าง cache | `§1.2 P-02 KV` | `API-07` | `F-31` `F-58` `F-59` | — | BR-17 | AT-29 |
| FN-30 | ตารางที่เผยแพร่แล้วคงค่าเดิม | `§1.2 P-01 แถบสถานะ` | `API-16` | `F-32` | `shift_pattern_version_id` | BR-02 | AT-30 |
| FN-31 | ยื่นคำขอสลับกะจาก tab ในหน้าเดียวกัน | `§1.2 P-03 drawer 920` | `API-11` | `F-33` | `T_roster_swap_request` | VR-19 | AT-31 |
| FN-32 | บล็อกคู่สลับที่ไม่ถูกต้อง (รายกรณี) | `§1.2 P-03 การ์ดเหตุ` | `API-11` | `F-34` | — | VR-14…VR-17 | AT-32 |
| FN-33 | บล็อกการยื่นในวันที่แตะไม่ได้ | `§1.2 P-03` | `API-11` | `F-35` | — | BR-16 · VR-18 | AT-33 |
| FN-34 | คู่สลับตอบรับ/ปฏิเสธ (เหตุผลบังคับ) | `§1.2 P-03` | `API-12` `API-13` | `F-37` `F-40` | `counterpart_responded_*` | BR-24 · VR-20 | AT-34 |
| FN-35 | รัน engine ตัวเดียวกันกับผลหลังสลับ 2 ฝ่าย | `§1.2 P-03 tab ผลตรวจ` | `API-12` | **`§3.0.6` `F-36`** | `validation_result` | BR-22 | AT-35 · **IA-05** |
| FN-36 | "ห้าม" = ยืนยันไม่ได้ · "เตือน" = ต้องรับทราบ | `§1.2 P-03 footer` | `API-14` | `F-38` | `validation_ack_*` | BR-22 · VR-21 | AT-36 · **IA-05** |
| FN-37 | ยืนยันแล้วเปลี่ยนสองช่องพร้อมกัน (atomic) | `§1.2 P-03` | `API-14` | `F-39` | `resulting_roster_version_id` | BR-22 | AT-37 |
| FN-38 | ผู้ยืนยัน = หัวหน้าจาก Policy Center | `§1.2 P-03 แถบสามฝ่าย` | `API-14` | `F-41` | `confirmed_by` | **BR-23** · VR-22 | AT-38 · **IA-08** |
| FN-39 | หัวหน้าปฏิเสธ (เหตุผลบังคับ) | `§1.2 P-03 modal` | `API-13` | `F-40` | `reject_reason` | BR-24 | AT-39 |
| FN-40 | ผู้ขอถอนคำขอเอง | `§1.2 P-03` | `API-13` | `F-42` | `swap_status='cancelled'` | — | AT-40 |
| FN-41 | หมดอายุเมื่อถึงวันของกะ | `§1.2 P-03 list` | `API-17` | `F-60` | `expired_at` | BR-29 | AT-41 |
| FN-42 | **read model `day` ตอบรูปเดียวกับ `FN-C03`** | `§1.2 P-05 ตาราง read model` | **`API-18`** | `F-43` `F-44` | — | BR-18 | AT-42 · **IA-01** |
| FN-43 | คืนเฉพาะเวอร์ชัน `published` ปัจจุบัน | `§1.2 P-05` | `API-18` `API-19` | `F-43` | `roster_status` (index) | BR-18 | AT-43 · **IA-01** |
| FN-44 | ไม่มีกะ → คืน `null` | `§1.2 P-05` | `API-18` | `F-44` | — | **BR-19** | AT-44 · **IA-07** |
| FN-45 | สวิตช์ Module Linkage เปลี่ยนพฤติกรรมจริง | `§1.2 P-05 สวิตช์` | `API-20` | `F-45` | `linkage_status` | BR-19 | AT-45 · **IA-07** |
| FN-46 | OT อ่านกรอบกะ + `work_days[]` จริง | `§1.2 P-05` | `API-18` | `F-43` | `work_days[]` | BR-20 | AT-46 |
| FN-47 | ไม่มีทางเข้าให้เขียนกลับ | `§1.2 P-05` | **`§2.3` (ตรวจรายการ endpoint ทั้งหมด)** | — | — | **BR-20** | AT-47 · **IA-09** |
| FN-48 | ชั่วโมงติดป้าย "ตามแผน" | `§1.0 LD-UI-11` `§1.2 ทุกหน้า` | `API-19` | `F-46` | `planned_hours` (computed) | BR-21 · BR-27 | AT-48 |
| FN-49 | ลงทะเบียน where-used กับต้นทาง | `§1.2 P-05 ตาราง where-used` | `API-21` | `F-47` | — | BR-05 | AT-49 |
| FN-50 | แจ้งเตือน 6 เหตุการณ์ผ่าน ENG-NOTIFY | (นอกหน้าจอ) | — | `F-58` | — | **§0.16.1** | AT-50 |
| FN-51 | ขอบเขตการเห็นจาก login · ไม่มีปุ่มสลับบทบาท | `§1.0 LD-UI-10` `§1.2 P-04` | ทุก endpoint | `F-48` | RLS | BR-25 · `§5.3` | AT-51 |
| FN-52 | คนลาออก — snapshot + ห้ามลงกะหลังวันออก | `§1.2 P-01` | `API-03` | `F-12` | `employee_name_snapshot` | BR-30 · VR-06 | AT-52 |
| FN-53 | ประวัติ append-only · ไม่มีปุ่มลบ | `§1.2 P-04 timeline` | `API-22` | `F-49` | **`T_roster_history` (trigger ปฏิเสธ UPDATE/DELETE)** | BR-26 | AT-53 · **IA-10** |
| FN-54 | ผูกบริษัทเดียว · ส่ง `company_id` ทุกครั้ง | `§1.2 P-01 หัวตาราง` | ทุก endpoint | `F-50` | `company_id` | BR-28 · VR-26 | AT-54 |
| FN-55 | **ไม่มีตัวเลขเงิน/ต้นทุน/เป้าหมายคนต่อกะ** | ทุกหน้า (พิสูจน์ด้วยการไม่มี) | ทุก payload | — | ไม่มีคอลัมน์เงิน | **BR-27** | AT-55 · **IA-09** |
| FN-56 | ไม่มีโครงเอกสารธุรกรรม | ทุกหน้า | — | — | ไม่มี `doc_no` | `§0.12.3b NS-07` | AT-56 |
| FN-57 | ไม่มีการจัดกะอัตโนมัติ | ทุกหน้า | — | `F-01` `F-03` `F-05` (deterministic) | — | `§0.12.3b NS-03` | AT-57 |
| FN-58 | ไม่มีกะที่ยังไม่มีคน | — | — | — | `employee_id` NOT NULL ใน cell ที่มีกะ | `§0.12.3b NS-04` | AT-58 |
| FN-59 | ไม่มีทะเบียนทักษะ · แสดงตำแหน่ง/แผนกแทน | `§1.2 P-03 drawer` | `API-11` | `F-33` | `employee_position_snapshot` | `§0.12.3b NS-05` | AT-59 |
| FN-60 | ไม่มีหน้าพนักงานทำเองบนตาราง | `§1.2 P-01 (บทบาทพนักงาน)` | — | `F-48` | — | `§0.12.3b NS-06` | AT-60 |
| FN-61 | ไม่มีหน้าตั้งค่า · มีลิงก์ออกทุกจุด | `§1.0 LD-UI-12` (6 จุด) | — | — | — | BR-03 | AT-61 |
| FN-62 | หน้าจอนิ่ง · กริดเลื่อนสองแกน | `§1.0 LD-UI-01` `LD-UI-05` | — | — | — | — | AT-62 |
| FN-63 | ค้นหา/กรอง + empty state · filter แถวเดียว | `§1.0 LD-UI-03` `§1.2 P-01` | `API-02` | `F-13` | index | — | AT-63 |
| FN-64 | บังคับช่องที่จำเป็น + กัน double-submit | `§1.0 LD-UI-13` ทุกฟอร์ม | ทุก mutation | `F-51` | NOT NULL | VR-09 · VR-13 · VR-19 · VR-20 · VR-25 | AT-64 |
| FN-65 | กางแบบกะหมุนตามรอบ | `§1.2 P-01 drawer กาง` | `API-01` | `F-03` | `rotation_option` | BR-31 | AT-65 |
| FN-66 | กะแยกช่วงในวันเดียว | `§1.2 P-01 drawer ช่อง` | `API-03` | **`§3.0.2` `F-09`** | **`slot_seq`** | BR-07 · BR-31 | AT-66 · **IA-03** |
| FN-67 | พนักงานรับทราบ/แจ้งว่าทำไม่ได้ | `§1.2 P-01 การ์ดตารางของฉัน` | `API-09` | `F-55` `F-56` | `T_roster_ack` | BR-33 · VR-24 | AT-67 |
| FN-68 | หมายเหตุต่อช่อง | `§1.2 P-01 drawer ช่อง` | `API-03` | `F-52` | `cell_note` | VR-08 | AT-68 |
| FN-69 | freeze horizon (เตือน · เมื่อมีค่า) | `§1.2 P-01/P-02` | — | `F-53` | — | BR-32 | AT-69 |
| FN-70 | ไม่มีมุมมองรายกะ | `§1.2 P-05 ตารางขอบเขต` | — | — | — | `§0.12.3b NS-17` | AT-70 |
| FN-71 | ไม่มีรายงาน/สถิติการจัดกะ | `§1.2 P-05 ตารางขอบเขต` | — | — | — | `§0.12.3b NS-18` | AT-71 |
| FN-72 | หนึ่งเจ้าของต่อช่องเสมอ | `§1.2 P-05 ตารางขอบเขต` | — | — | unique key มี `employee_id` | `§0.12.3b NS-19` | AT-72 |
| FN-73 | ข้อห้ามยังจริงหลังเพิ่มของจาก S1.5 | ทุกหน้า | ทุก payload | — | — | `§0.12.3b` ทั้งหมด | AT-73 · **IA-09** |

**FN: 73/73 มีที่อยู่ครบทุกไฟล์ — 0 ตกหล่น**

### §0.12.1 Stories (BRD §7) — 73/73

**ST-nn ↔ FN-nn ตรงกัน 1:1 ทั้ง 73 ข้อ** (ตามที่ `BRD §7` ออกแบบไว้ให้ตรวจได้แบบกลไก) → **ที่อยู่ของ ST-nn = ที่อยู่ของ FN-nn ในตาราง §0.12.0** · Acceptance Criteria ทั้ง **155 ข้อ** ถูกแปลงเป็นเคสทดสอบที่ `06_TESTS §6.2` (AT-01…AT-73) และเป็น expected ที่ตรวจได้ด้วยตาที่ `06_TESTS §6.7 microcopy`

### §0.12.2 Business Rules (BRD §9.1) — 33/33

| BR | อยู่ที่ | Engine/Function | Test |
|---|---|---|---|
| BR-01 | `05_RULES §5.1` | `F-02` `hr-config-resolve-client` | AT-01 · AT-04 |
| BR-02 | `05_RULES §5.1` | `F-32` | AT-30 |
| BR-03 | `05_RULES §5.1` | — (ตรวจด้วยการไม่มี endpoint เขียน) | AT-61 |
| BR-04 | `05_RULES §5.1` | `F-06` | AT-09 |
| BR-05 | `05_RULES §5.1` | `F-47` | AT-49 |
| **BR-06** | `05_RULES §5.1` | **`§3.0.1 toTimeline` · ENG-ROSTER-CONFLICT** | AT-12 · **IA-03** |
| **BR-07** ⭐ | `05_RULES §5.1` | **`§3.0.2 detectOverlap`** | AT-11 · AT-66 · **IA-03** |
| BR-08 | `05_RULES §5.1` | `§3.0.3 checkRest` | AT-13 |
| BR-09 | `05_RULES §5.1` | `F-17 checkWeeklyHours` | AT-14 |
| BR-10 | `05_RULES §5.1` | `F-18 checkConsecutiveDays` | AT-15 |
| **BR-11** ⭐ | `05_RULES §5.1` | **`§3.0.4 resolveShiftRule` (คืน `noValue`)** | AT-16 · **IA-06** |
| BR-12 | `05_RULES §5.1` | `F-19` `F-20` | AT-17 · AT-18 |
| BR-13 | `05_RULES §5.1` | `F-21` | AT-19 |
| BR-14 | `05_RULES §5.1` | `F-22` `F-23` `F-26` | AT-24 · AT-25 · **IA-02** |
| BR-15 | `05_RULES §5.1` | `F-27` `F-28` | AT-26 |
| **BR-16** ⭐⭐ | `05_RULES §5.1` | **`§3.0.5 planPublish`** | AT-27 · AT-28 · **IA-04** |
| BR-17 | `05_RULES §5.1` | `F-31` `F-58` | AT-29 |
| BR-18 | `05_RULES §5.1` | `F-43` | AT-21 · AT-43 · **IA-01** |
| **BR-19** ⭐ | `05_RULES §5.1` | `F-44` `F-45` | AT-44 · AT-45 · **IA-07** |
| **BR-20** ⭐ | `05_RULES §5.1` | — (**ตรวจที่ `02_API §2.3` — ไม่มี write endpoint**) | AT-47 · **IA-09** |
| BR-21 | `05_RULES §5.1` | `F-46` | AT-48 |
| BR-22 | `05_RULES §5.1` | **`§3.0.6 validateSwap` · `F-39`** | AT-35 · AT-36 · AT-37 · **IA-05** |
| **BR-23** | `05_RULES §5.1` | `F-41 resolveConfirmer` (Policy Center) | AT-38 · **IA-08** |
| BR-24 | `05_RULES §5.1` | `F-40` | AT-34 · AT-39 |
| BR-25 | `05_RULES §5.3` | `F-48` | AT-51 |
| BR-26 | `05_RULES §5.1` | `F-49` + **trigger ที่ `04_DB`** | AT-53 · **IA-10** |
| **BR-27** ⭐ | `05_RULES §5.1` | — (ตรวจด้วยการไม่มีคอลัมน์/ไม่มี field) | AT-55 · **IA-09** |
| BR-28 | `05_RULES §5.1` | `F-50` | AT-54 |
| BR-29 | `05_RULES §5.1` | `F-60` (scheduler) | AT-41 |
| BR-30 | `05_RULES §5.1` | `F-12` | AT-52 |
| BR-31 | `05_RULES §5.1` | `§3.0.3 checkRest` (รวมช่วงว่างในวันเดียว) | AT-66 |
| BR-32 | `05_RULES §5.1` | `F-53` | AT-69 |
| BR-33 | `05_RULES §5.1` | `F-55` `F-56` | AT-67 |

**BR: 33/33 มีที่อยู่ + engine/function + test ครบ**

### §0.12.3 Edge Cases (BRD §10) — ☑ ยืนยันแล้ว 26/26 · ☐ AI-suggested 31/31

| กลุ่ม | จำนวน | อยู่ที่ | test |
|---|---:|---|---|
| จากต้นทาง (`BRD §10.1` EC-01…EC-26) | **26** | `05_RULES §5.4` | AT-01…AT-73 (กระจายตาม FN) |
| CA — Concurrent Access (4) | 4 | `05_RULES §5.4 CA` | AT-74…AT-77 |
| DI — Data Integrity (5) | 5 | `05_RULES §5.4 DI` | AT-78…AT-82 |
| CL — Calculation (5) | 5 | `05_RULES §5.4 CL` | AT-83…AT-87 |
| ST — Status/Workflow (5) | 5 | `05_RULES §5.4 ST` | AT-88…AT-92 |
| PM — Permission (5) | 5 | `05_RULES §5.4 PM` | AT-93…AT-97 |
| EN — Cross-feature (7) | 7 | `05_RULES §5.4 EN` | `06_TESTS §6.6 XT-01…XT-07` |
| **รวม** | **57** | | |

### §0.12.3b Functions Cut — รายการที่ประกาศว่า "ไม่รองรับ" (**19/19** · อยู่ในแมนิเฟสต์ ไม่หายเงียบ)

| # | ไม่รองรับ | พิสูจน์ที่ | เจ้าภาพ | OQ |
|---|---|---|---|---|
| NS-01 | ความครอบคลุม/คนไม่พอต่อกะ | `01_UI §1.2 P-05 ตารางขอบเขต แถว 1` · `06_TESTS AT-55` | Strike + BA Manpower (W6) | OQ-STD-R1 |
| NS-02 | ต้นทุนแรงงาน/ตัวเลขเงิน | `04_DB` (ไม่มีคอลัมน์เงิน) · `06_TESTS IA-09` | Strike + BA Payroll (W4) | OQ-STD-R2 |
| NS-03 | จัดกะอัตโนมัติ (optimizer) | `03_LOGIC F-01/F-03/F-05` deterministic · `AT-57` | Strike | OQ-STD-R3 |
| NS-04 | กะที่ยังไม่มีคน (open shift) | `04_DB` unique key มี `employee_id` · `AT-58` | Strike | OQ-STD-R4 |
| NS-05 | ทะเบียนทักษะ/จับคู่ทักษะ | `04_DB` ไม่มีตารางทักษะ · `AT-59` | Strike + BA Training (W5) | OQ-STD-R5 |
| NS-06 | หน้าพนักงานทำเองบนตาราง | `05_RULES §5.3` permission matrix · `AT-60` | Strike + BA ESS (W6) | OQ-STD-R7 · OQ-HR-04 |
| NS-07 | พิมพ์/ส่งออกเป็นเอกสารทางการ | **ไม่มี `PRINT_SPEC.md` ในแพ็ก** · `AT-56` | — | — |
| NS-08 | หน้าตั้งค่าของ HR Configuration | `02_API` ไม่มี endpoint เขียนไปต้นทาง · `AT-61` | BA HR Configuration | #107 · HR-1 |
| NS-09 | ค่ากฎหมายเขียนตัวเลขเอง | `03_LOGIC §3.0.4` (คืน `noValue`) · **`IA-06`** | **Strike + BA HR Config** | **OQ-STD-R6** |
| NS-10 | บันทึก/แก้เวลาจริง · คำนวณสาย-ขาด | `03_LOGIC` ไม่มี function คำนวณชั่วโมงจริง · `AT-48` | — | AT-5 · AT-6 |
| NS-11 | ออกใบ/อนุมัติ/ยืนยันชั่วโมง OT | `02_API` ไม่มี endpoint เขียนไป OT · `AT-19` | — | OT-5 |
| NS-12 | บริหารสิทธิ์/โควตาการลา | `02_API` ไม่มี endpoint เขียนไป Leave · `AT-17` | — | — |
| NS-13 | สายอนุมัติ (DOA) สำหรับการสลับกะ | `03_LOGIC F-41` เรียก Policy Center ไม่ใช่ DOA · **`IA-08`** | — | `BRD §4.3` |
| NS-14 | การลบข้อมูลถาวร | **`04_DB` trigger ปฏิเสธ DELETE** · **`IA-10`** | — | LOCK-AUDIT |
| NS-15 | การ์ดสรุปผลกระทบ 7 ด้าน | `01_UI` ไม่มีการ์ด 7 ท่อ · `§0.16.2` | — | CSQ Iron Rule |
| NS-16 | UI สลับบริษัท | `01_UI §1.2 P-01` มีป้ายบริษัทอย่างเดียว · `AT-54` | Strike | OQ-HR-05 |
| NS-17 | มุมมองรายกะ | `01_UI §1.1` ไม่มี route · `AT-70` | Strike | OQ-R16 |
| NS-18 | รายงาน/สถิติการจัดกะ | `01_UI §1.1` ไม่มี route · `AT-71` | Strike + 7C | OQ-R17 |
| NS-19 | หลายคนต่อกะ + ตำแหน่งงานในกะ | `04_DB` unique key · `AT-72` | Strike | OQ-R18 |

### §0.12.4 สรุป Coverage

| มิติ | จำนวน | อยู่ในแพ็กครบ? |
|---|---:|:---:|
| **FN (FUNCTION_CHECKLIST)** | **73** | ✅ 73/73 |
| **Story (BRD §7)** | **73** | ✅ 73/73 (1:1 กับ FN) |
| **Acceptance Criteria** | **155** | ✅ แปลงเป็น AT + microcopy ครบ |
| **Business Rule (BRD §9.1)** | **33** | ✅ 33/33 |
| **Validation Rule (BRD §9.2)** | **26** | ✅ 26/26 → `05_RULES §5.5` |
| **Scenario (PREBRIEF)** | **58** | ✅ 58/58 → `06_TESTS §6.2` |
| **Transition** | **12** (T-1…T-6 · W-1…W-6) | ✅ 12/12 → `05_RULES §5.2` |
| **Edge Case** | **57** (26 ☑ + 31 ☐) | ✅ 57/57 |
| **Functions Cut ("ไม่รองรับ")** | **19** | ✅ 19/19 (§0.12.3b) |
| **Declaration event** | **8** (NTF 6 + CSQ 2) | ✅ 8/8 → `§0.16` |
| **แถวที่ "อยู่ที่" ว่าง** | **0** | ✅ ไม่มี |

## §0.13 ⭐ Published Roster Surface — สิ่งที่ feature อื่นอ่านได้จากที่นี่

> **ส่วนนี้เขียนไว้ให้ทีมของ Attendance (W1) · OT/Shift (W2) · ESS Portal (W6) อ้างอิงโดยตรง** — ยกไปวางใน `00_OVERVIEW §Dependencies` ของ feature ตัวเองได้ทันที
> **กติกาเหล็ก:** consumer **อ่าน** กะจากที่นี่ · **ห้ามเขียนกลับทุกกรณี** (feature นี้ไม่มี endpoint เขียนสำหรับ consumer เลย — ตระกูลเดียวกับ `F-HR-ATTEND §0.13.5` และ `F-HR-OT §0.13.5`) · **ห้ามเก็บกะถาวรในตารางของตัวเองโดยไม่มี `roster_version_id`** · **ห้ามตีความ `planned_hours` ว่าเป็นชั่วโมงทำงานจริง**

### §0.13.1 อะไรบ้างที่เผยแพร่ (2 มุมมอง)

| มุมมอง | เนื้อหา | ผู้ใช้หลัก | endpoint |
|---|---|---|---|
| **`day`** (กะของคน × วัน) | กะที่ใช้จริงของวันนั้น (**`shift` object 8 ฟิลด์**) + `roster_version_id` + `shift_pattern_version_id` + `roster_status` | **Attendance** (`FN-C03 resolveShiftForDay` **แหล่งลำดับ ①**) · **OT/Shift** (กรอบกะ + วันหยุดประจำสัปดาห์จริง) · ESS | `GET /api/v1/roster/resolve` |
| **`period`** (สรุปกะของคนในงวด/เดือน) | จำนวนวันที่มีกะ · จำนวนวันหยุด · **ชั่วโมงตามแผนรวม** · ก้อนเวอร์ชันของค่าที่ใช้ | **ESS Portal (W6)** · **ชั้นรายงาน 7C** | `GET /api/v1/roster/periods/resolve` |

**สิ่งที่ไม่เผยแพร่:** ตารางร่าง (`draft`) · ตารางที่ถูกแทนที่ (`superseded`) · ร่างที่ถูกทิ้ง (`discarded`) — **ไม่หลุดออกไปเด็ดขาด** (BR-18) · `request_reason` / `reject_reason` / `ack_note` (**Confidential**) · `cell_note` (แสดงบนหน้าจอของ feature นี้กับเจ้าของช่องเท่านั้น) · **ตัวเลขเงินและตัวเลขความต้องการกำลังคน — ไม่มีในระบบนี้เลย**

### §0.13.2 หน้าทางเข้าเดียวของกะรายคนรายวัน — `GET /api/v1/roster/resolve`

```
GET /api/v1/roster/resolve
    ?date=2026-09-18            ← บังคับเสมอ (ไม่ส่ง = 400 ERR_ROSTER_DATE_REQUIRED)
    &date_to=2026-09-30         ← optional (ช่วงวัน · สูงสุด 62 วันต่อคำขอ)
    &company_id=<uuid>          ← บังคับเมื่อ tenant มีบริษัทลูก
    &employee_id=<uuid>         ← เจาะรายคน (ใช้คู่กับ scope=employee)
    &scope=employee|company     ← default employee · company = อ่านทั้งบริษัทเป็นชุด
    &page=1&page_size=500       ← เมื่อ scope=company
```

**สิ่งที่คืนกลับ (day snapshot) — โครงที่ consumer ยกไปใช้ได้เลย:**

| field | ชนิด | ความหมาย | Classification |
|---|---|---|---|
| `as_of` | date | วันที่ที่ใช้ตัดสิน (สะท้อน `date` ที่ส่งมา) | Internal |
| `employee_id` · `employee_name_snapshot` | uuid · text | คนที่กะนี้เป็นของ | **PII** |
| **`work_date`** | date | **วันที่อ้างอิง — กรณีกะข้ามคืนคือวันเข้ากะ** (**LD-01** · นิยามเดียวกับ Attendance/OT · ห้ามตั้งใหม่) | Internal |
| `company_id` | uuid | ขอบเขตบริษัท | Internal |
| **`shift`** ⭐ | object \| **`null`** | snapshot ของกะที่ใช้จริงในวันนั้น — **`null` = ไม่มีกะ (ดู §0.13.4 กรณีพิเศษ)** | Internal |
| ↳ `shift.shift_code` | text | รหัสกะ | Internal |
| ↳ `shift.shift_name` | text | ชื่อกะ | Internal |
| ↳ `shift.start_time` | time | เวลาเข้ากะ | Internal |
| ↳ `shift.end_time` | time | เวลาออกกะ | Internal |
| ↳ `shift.is_overnight` | bool | **ธงกะข้ามวัน** — `true` แปลว่า `end_time` อยู่ในวันถัดจาก `work_date` | Internal |
| ↳ `shift.break_from` · `shift.break_to` | time \| `null` | ช่วงพักในกะ | Internal |
| ↳ `shift.work_days[]` | array | **วันทำงานในสัปดาห์ของแพทเทิร์นที่ใช้** — OT ใช้ระบุวันหยุดประจำสัปดาห์จริงของคนนั้น | Internal |
| **`roster_version_id`** ⭐ | uuid | **เวอร์ชันของตารางที่ให้คำตอบนี้ — consumer ต้องเก็บคู่กับสิ่งที่บันทึกไว้** (ตระกูลเดียวกับ C-2 · AT-2) · **ไม่ใช่เลขที่เอกสาร** | Internal |
| **`shift_pattern_version_id`** ⭐ | uuid \| `null` | เวอร์ชันของแพทเทิร์นกะจาก HR Configuration ที่ใช้ตัดสิน · `null` เมื่อ `shift = null` | Internal |
| `roster_status` | const | **`published` เสมอ** — ค่าอื่นไม่มีทางออกมาจาก endpoint นี้ (BR-18) | Internal |
| `slot_seq` | int | ลำดับกะในวันเดียวกัน (1 = กะแรก · 2+ = กะแยกช่วง) — เมื่อวันนั้นมีหลายกะ จะคืน **หลายแถว** เรียงตาม `slot_seq` | Internal |
| `linked` | bool | สถานะ Module Linkage ต่อ consumer ที่เรียก — `false` แปลว่ายังไม่เชื่อม (คู่กับ `shift = null`) | Internal |
| `source_feature` | const | `F-HR-ROSTER` | Internal |

**ตัวอย่างคำตอบ (คนที่มีกะดึกวันที่ 18 ก.ย.):**

```json
{
  "as_of": "2026-09-18",
  "employee_id": "…",
  "employee_name_snapshot": "ก้องภพ …",
  "work_date": "2026-09-18",
  "company_id": "…",
  "shift": {
    "shift_code": "N",
    "shift_name": "กะดึก",
    "start_time": "22:00",
    "end_time": "06:00",
    "is_overnight": true,
    "break_from": "02:00",
    "break_to": "03:00",
    "work_days": ["MON","TUE","WED","THU","FRI","SAT"]
  },
  "roster_version_id": "…",
  "shift_pattern_version_id": "…",
  "roster_status": "published",
  "slot_seq": 1,
  "linked": true,
  "source_feature": "F-HR-ROSTER"
}
```

> **ชื่อฟิลด์ของ `shift` object ตรงกับที่ `F-HR-ATTEND §0.13.2` ประกาศไว้แล้วทุกตัว** (`shift_code · shift_name · start_time · end_time · is_overnight · break_from · break_to · work_days[]`) — **นี่ไม่ใช่ความบังเอิญ แต่เป็นข้อกำหนด** เพราะ `FN-C03 resolveShiftForDay` ของ Attendance เขียนรอไว้ตั้งแต่ W1 โดยประกาศว่าจะรับรูปนี้จากแหล่ง ① · **ห้ามเปลี่ยนชื่อฟิลด์ ห้ามเพิ่มชั้นห่อ ห้ามคืนรูปแบบใหม่**

### §0.13.3 มุมมองสรุปงวด — `GET /api/v1/roster/periods/resolve`

```
GET /api/v1/roster/periods/resolve
    ?period_code=2026-09        ← บังคับ (หรือส่ง date= เพื่อให้ระบบหางวดของวันนั้นให้)
    &company_id=<uuid>          ← บังคับเมื่อ tenant มีบริษัทลูก
    &employee_id=<uuid>         ← optional (ไม่ส่ง = ทั้งงวดของบริษัท · แบ่งหน้า)
    &page=1&page_size=500
```

คืนต่อ (คน × งวด):

| field | ชนิด | ความหมาย |
|---|---|---|
| `period_code` · `period_from` · `period_to` · `period_status` | text · date · enum | ขอบเขตงวดจาก `period_rule` ของ HR Configuration + สถานะ `open`/`closed` |
| `employee_id` · `employee_name_snapshot` | uuid · text | คน (**PII**) |
| `shift_days` | int | จำนวนวันที่มีกะอย่างน้อย 1 กะ |
| `shift_slots` | int | จำนวนกะทั้งหมด (มากกว่า `shift_days` เมื่อมีกะแยกช่วง) |
| `off_days` | int | จำนวนวันในงวดที่ไม่มีกะ — **เป็นข้อเท็จจริงของตาราง ไม่ใช่การบอกว่าคนพอ/ไม่พอ** |
| **`planned_hours`** ⭐ | decimal(7,2) | **ชั่วโมงตามแผนรวม** = Σ `hours_per_day` ของกะทั้งหมดในงวด |
| `night_shift_count` · `holiday_shift_count` | int | จำนวนกะกลางคืน · จำนวนกะที่ตรงวันหยุด — **เป็นบริบท ไม่ใช่ตัวคูณ** |
| `roster_version_id[]` | uuid[] | ทุกเวอร์ชันที่มีผลในงวดนี้ (มากกว่า 1 เมื่อมีการเผยแพร่ซ้ำ) |
| **`config_version_ids`** | object | `{ shift_pattern:[…], holiday:[…], shift_rule: uuid\|null, period: uuid }` |
| `source_feature` | const | `F-HR-ROSTER` |

> ⚠️ **`planned_hours` คือชั่วโมงตามแผน ไม่ใช่ชั่วโมงทำงาน**
> · **ห้ามใช้เป็นฐานคำนวณค่าจ้าง** — ชั่วโมงที่จ่ายได้มาจาก **Attendance** (ในกรอบกะ) กับ **OT** (นอกกรอบกะที่อนุมัติแล้ว) เท่านั้น
> · **ห้ามคูณเป็นเงิน** — feature นี้ไม่มีตัวเลขเงินเลย และไม่มี Rate Card ให้อ่าน (BR-27)
> · คนที่ถูกจัดเวรไว้แต่ลาป่วยไม่มา ยังมี `planned_hours` เต็ม — **นั่นคือเหตุผลที่ Attendance มีอยู่**

### §0.13.4 กติกา 5 ข้อที่ consumer ทุกตัวต้องทำตาม (`RO-1…RO-5`) ⭐

> **นี่คือ "กติกาเหล็ก 5 ข้อ" ที่ออกแบบไว้ตั้งแต่ S0–S1.8 และถูกยกมาไว้ที่นี่แบบไม่แก้ความหมาย**

| # | กติกา | ทำไม |
|---|---|---|
| **RO-1** | **คืนเฉพาะเวอร์ชัน `published` ที่เป็นตัวปัจจุบันเท่านั้น** — ตารางร่าง (`draft`) · ถูกแทนที่ (`superseded`) · ยกเลิกร่าง (`discarded`) **ไม่ถูกเผยแพร่เด็ดขาด** | ร่างคือความคิดที่ยังไม่ประกาศ — ถ้าหลุดออกไป พนักงานจะถูกตัดสินด้วยแผนที่ยังไม่มีใครรับผิดชอบ (BR-18 · `06_TESTS IA-01`) |
| **RO-2** ⭐⭐ | **ไม่มีตารางของ (คน × วัน) นั้น → คืน `shift: null` ห้ามเดา** — **ห้ามคืนกะมาตรฐานแทน ห้ามคืนกะของวันข้างเคียง ห้ามคืน `{}` ว่าง** | **Attendance ออกแบบไว้แล้วว่าจะตกไปแหล่ง ② (กะมาตรฐานจาก `shift_pattern`) เมื่อแหล่ง ① คืน `null`** — ถ้าที่นี่เดากะให้ **ทางสำรองของ Attendance จะไม่ทำงานทั้งระบบ และผลจะผิดโดยไม่มีใครเห็น** (BR-19 · `F-HR-ATTEND BR-20 · EC-19` · `06_TESTS IA-07`) |
| **RO-3** | **ส่ง `date` เสมอ** — วันของกะ **ไม่ใช่ "วันนี้"** · คำขอที่ไม่มี `date` ถูกปฏิเสธด้วย `400 ERR_ROSTER_DATE_REQUIRED` | ตารางเปลี่ยนตามเวอร์ชัน — ถามโดยไม่ระบุวันคือคำถามที่ไม่มีคำตอบเดียว (ตระกูลเดียวกับ **C-1 · AT-1 · OT-1**) |
| **RO-4** | **เก็บ `roster_version_id` + `shift_pattern_version_id` คู่กับสิ่งที่บันทึกไว้** | ตอบข้อพิพาทย้อนหลังได้ · และเป็น **กลไกเดียว** ที่บอก consumer ว่าค่าที่ถืออยู่เก่าแล้ว เมื่อมีการเผยแพร่ซ้ำ (ตระกูลเดียวกับ **C-2 · AT-2**) |
| **RO-5** | **ห้ามเขียนกลับทุกกรณี** — **feature นี้ไม่มี write endpoint สำหรับ consumer เลย** · การแก้กะทำที่หน้าจอของ feature นี้เท่านั้น · ใช้ลิงก์ **"จัดการที่จัดกะ" → `#/roster/<tab>`** | การเปลี่ยนกะทุกครั้งต้องมีคนรับผิดชอบพร้อมเหตุผลกับร่องรอย (BR-26) · ถ้าให้ระบบอื่นเขียนเข้ามาได้ ร่องรอยจะขาดตอนทันที (ตระกูลเดียวกับ **AT-5 · OT-5** · `06_TESTS IA-09`) |

**กรณีพิเศษที่ consumer ต้อง handle:**

| สถานการณ์ | คำตอบ | consumer ควรทำอะไร |
|---|---|---|
| **ไม่มีตารางของเดือนนั้นเลย** | `200` + `shift: null` + `reason: "NO_ROSTER_AT_DATE"` | **ตกไปแหล่งถัดไปของตัวเอง** — ห้ามถือว่าเป็นข้อผิดพลาด |
| **มีตารางแต่ช่องนั้นว่าง (คนนั้นไม่ถูกจัดเวร)** | `200` + `shift: null` + `reason: "NO_SHIFT_FOR_EMPLOYEE_DAY"` | เช่นเดียวกัน — **"ช่องว่าง" คือ "วันหยุดของคนนั้น" ไม่ใช่ "ยังไม่ได้จัด"** |
| **ตารางของเดือนนั้นยังเป็นร่าง** | `200` + `shift: null` + `reason: "ROSTER_NOT_PUBLISHED"` | เช่นเดียวกัน — **ห้ามพยายามอ่านร่าง** |
| **Module Linkage ยังไม่เชื่อม** | `200` + `shift: null` + `linked: false` + `reason: "MODULE_NOT_LINKED"` | **ใช้ทางสำรองของตัวเอง** — สวิตช์นี้ **เปลี่ยนพฤติกรรมจริง ไม่ใช่ป้าย** (BR-19) |
| **วันนั้นมีกะแยกช่วง** | `200` + **หลายแถว** เรียงตาม `slot_seq` | **ต้องรองรับหลายแถวต่อ (คน × วัน)** — ไม่ใช่หยิบแถวแรกแล้วทิ้งที่เหลือ |
| **ตารางถูกเผยแพร่ซ้ำหลังจากที่ consumer อ่านไปแล้ว** | `roster_version_id` **เปลี่ยน** | **เทียบกับค่าที่เก็บไว้ → ถ้าไม่ตรง แปลว่าค่าเก่าแล้ว ต้องอ่านใหม่** (RO-4) |
| **ขอช่วงวันเกิน 62 วัน** | `400 ERR_ROSTER_RANGE_TOO_LARGE` | แบ่งคำขอ |

### §0.13.5 ไม่มีทางเข้าสำหรับการเขียนกลับ ⭐

**feature นี้ไม่เปิด endpoint เขียนให้ consumer เลย** — เหมือน `F-HR-ATTEND` · `F-HR-LEAVE` · `F-HR-OT`
เหตุผล: **การเปลี่ยนกะทุกครั้งต้องมีคนรับผิดชอบพร้อมเหตุผล** (BR-26) และต้อง **ผ่านตัวตรวจข้อขัดแย้งชุดเดียวกันเสมอ** (BR-22 · C-17) · ถ้าให้ระบบอื่นเขียนเข้ามาได้ ทั้งร่องรอยและการตรวจจะถูกข้ามพร้อมกัน

- **Attendance ต้องการแก้กะของวันหนึ่ง** → **แก้ที่หน้าจอของ feature นี้** (`#/roster/grid`) แล้วเผยแพร่ซ้ำ — ไม่มีทางเขียนเข้ามา
- **OT ต้องการให้วันหนึ่งเป็นวันหยุดประจำสัปดาห์** → **แก้ตารางที่ feature นี้** หรือแก้ `work_days[]` ของแพทเทิร์นที่ **HR Configuration** — ไม่ใช่เขียนเข้ามา
- **ESS ต้องการให้พนักงานขอสลับกะ** → **เรียกหน้าจอของ feature นี้** (`#/roster/swap`) ไม่ทำ CRUD ซ้ำ (OQ-HR-04)
- **ระบบใดต้องการล็อกตาราง** → **ล็อกเกิดจากการปิดงวดที่ HR Configuration** ไม่ใช่คำสั่งจาก consumer (**P-7**)

> ข้อยกเว้นเดียวคือ `POST /api/v1/roster/usage` (การลงทะเบียน where-used) ซึ่งเป็น **การบอกว่าใครอ่านอยู่ ไม่ใช่การเขียนข้อมูลตาราง**

### §0.13.6 พฤติกรรมของการเผยแพร่ซ้ำ (republish) — สัญญาที่ consumer ต้องเข้าใจ ⭐⭐

**1) การเผยแพร่ซ้ำ = การมินต์เวอร์ชันใหม่ ไม่ใช่การแก้ทับ**
- ระบบ **สร้าง `roster_version` ใหม่** แล้ว **ทำเครื่องหมายเวอร์ชันเดิมเป็น `superseded`** (`superseded_by` ชี้ไปเวอร์ชันใหม่ · `supersedes` ของเวอร์ชันใหม่ชี้กลับ)
- **เวอร์ชันเดิมไม่ถูกลบและไม่ถูกแก้ค่าใดเลย** — อ่านได้ในประวัติของ feature นี้ตลอดไป (BR-15 · LOCK-AUDIT)
- **ไม่มีการย้อนเวอร์ชัน (rollback)** — ถ้าต้องการผลเหมือนเวอร์ชันเก่า ให้แก้แล้วเผยแพร่ซ้ำเป็นเวอร์ชันใหม่ (`§0.3` PB-04 · `07_LOCKED LD-ROS-09`)

**2) วันที่ปลายทางบริโภคไปแล้ว — ถูกปฏิเสธรายวันพร้อมชี้วันที่ชน**
- **นิยามของ "บริโภคแล้ว":** `day_status ∈ {confirmed, locked}` ที่ **Attendance** **หรือ** `period_status = closed`
- พฤติกรรม: ระบบ **แยกผลรายวัน** เป็น *ผ่าน* กับ *ถูกปฏิเสธ* แล้ว **commit เฉพาะวันที่ผ่าน** · วันที่ถูกปฏิเสธถูกคืนกลับมาเป็น **`rejected_locked_dates[]` พร้อมเหตุรายวัน**
- **ไม่ใช่การเตือนแล้วปล่อยผ่าน** และ **ไม่ใช่การบล็อกทั้งเดือน** — **วันอื่นในเดือนเดียวกันที่ยังไม่ถูกบริโภคยังเปลี่ยนได้ตามปกติ** (BR-16 · **P-7 · AT-4** · `03_LOGIC §3.0.5` · `06_TESTS IA-04`)
- ผลกับ consumer: **Attendance ไม่มีวันเจอกะที่ขัดกับสิ่งที่ยืนยันไปแล้ว** เพราะ feature นี้ปฏิเสธการเปลี่ยนตั้งแต่ต้นทาง

**3) การแจ้งเตือนแคบเฉพาะคนที่กะเปลี่ยนจริง**
- ระบบ **เทียบเวอร์ชันเก่ากับใหม่ก่อน** แล้วส่ง `roster_shift_changed` (**N2**) **เฉพาะพนักงานที่กะของตัวเองเปลี่ยนจริงในเวอร์ชันใหม่** — **ห้ามส่งให้ทุกคนในตาราง** (BR-17 · `NTF_BRIEF §5`)
- เหตุผล: แจ้งทุกคนทุกครั้ง = noise ที่ทำให้คนเลิกอ่าน แล้วจะพลาดครั้งที่สำคัญจริง

**4) consumer รู้ว่าค่าที่ถืออยู่เก่าจาก `roster_version_id` ใหม่**
- ไม่มีการ push ค่าไปให้ consumer และ **ห้ามให้ consumer เดาเอง** — กลไกเดียวคือ **เทียบ `roster_version_id` ที่เก็บไว้กับที่ได้ใหม่** (RO-4)
- feature นี้ยิง **`roster.republished` (E2)** ให้ชั้นรายงาน ซึ่ง consumer ที่ฟัง event ได้ก็ใช้เป็นสัญญาณล้าง cache ได้ (ตระกูลเดียวกับ **C-3 · AT-3**)

**5) การสลับกะที่ยืนยันแล้วก็คือการเผยแพร่ซ้ำ**
- W-3 (หัวหน้ายืนยัน) ทำให้เกิด **T-4** เหมือนกับการแก้ด้วยมือ — ออกเวอร์ชันใหม่ · แจ้งเฉพาะคนที่เปลี่ยน · ยิง E2
- **ต่างกันที่ `adjust_kind: shift_swap`** (แทน `manual_edit`) เพื่อให้ชั้นรายงานแยกได้ว่าการเปลี่ยนนี้มาจากการแลกเวร **และเพื่อไม่ให้การสลับถูกนับสองครั้ง** (`CSQ_BRIEF §3`)

### §0.13.7 event ที่ consumer ฟังได้ (2 event · **ท่อ EC เท่านั้น**)

| event | เมื่อไร | payload หลัก | consumer ควรทำอะไร |
|---|---|---|---|
| **`roster.published`** | ตารางถูกเผยแพร่ครั้งแรกของเดือน (`03_LOGIC §3.1 F-25` · **T-3**) | `roster_version_id` · `company_id` · `period_month` · `scope_team` · `employee_id[]` · `planned_shift_count` · `planned_hours_total` · `planned_hours_by_employee[]` · `night_shift_count` · `holiday_shift_count` · `config_version_ids` · `published_by` · `published_at` · `warning_ack_items[]` | เริ่มอ่าน `GET /roster/resolve` ได้ · ชั้นรายงานรับเป็น **EC `kind: estimated`** |
| **`roster.republished`** | ตารางถูกเผยแพร่ซ้ำ (`F-28` · **T-4** — ทั้งจากการแก้ด้วยมือและจากการยืนยันคำขอสลับกะ) | ทุก field ของ event แรก + **`supersedes`** (ชี้ event ของเวอร์ชันก่อน) · **`adjust_kind`** (`manual_edit` \| `shift_swap`) · `changed_cell_count` · `affected_employee_id[]` · `planned_hours_delta_by_employee[]` · `publish_note` · `rejected_locked_dates[]` | **ล้าง cache แล้วอ่านค่าใหม่** — **event เดิมไม่ถูกลบ ไม่ถูกแก้** (BR-CSQ-04) |

> **ทั้ง 2 event เป็นท่อ EC เท่านั้น · `kind: estimated` · `basis: declared` หน่วยชั่วโมง** — ประกาศไว้ที่ `5_DECLARATIONS/CSQ_BRIEF.md §2`
> **ไม่มี event อื่นนอกจากนี้** — การกางตาราง · การลากกะ · การบันทึกร่าง · การทิ้งร่าง · การยื่น/ตอบรับ/ปฏิเสธ/ถอน/หมดอายุคำขอสลับ · การตรวจพบข้อขัดแย้ง · การรับทราบคำเตือน · การรับทราบกะ · การล็อกเมื่องวดปิด **ไม่ยิง event 7C** (กันนับซ้ำ · `CSQ_BRIEF §3`)
> **feature นี้ไม่ประกาศท่อ FC** — การจัดกะยังไม่ผูกพันเงินขององค์กร (ภาระผูกพันเกิดที่ OT ตอนอนุมัติ และที่ Payroll ตอนจ่าย) · **ไม่ประกาศ AC** (ไม่มีรายการบัญชี) · **ไม่ประกาศ SecC** (นโยบายกะเป็นของ HR Configuration ซึ่งประกาศ SecC ไว้แล้วที่ `CSQ-HRCFG` E1–E6) · **ไม่ประกาศ OC / DC ระดับเอกสาร / SC** (register 422)
> **event ท่อ 7C ทั้ง 2 ตัวนี้เป็นคนละชุดกับ 6 event แจ้งเตือนของ ENG-NOTIFY** — ดู `§0.16.3` (สองชุด **disjoint** ไม่มีชื่อซ้ำกันแม้แต่ตัวเดียว)

### §0.13.8 ตัวอย่างการใช้จริง (สำหรับทีม Attendance)

```
วันทำงานของพนักงานคนหนึ่ง วันที่ 18 ก.ย. 2026:

1. Attendance เรียก FN-C03 resolveShiftForDay({employee_id, work_date:'2026-09-18', company_id})
2. FN-C03 ลองแหล่ง ① ก่อน:
      GET /api/v1/roster/resolve?date=2026-09-18&employee_id=…&company_id=…
3. ผลที่เป็นไปได้:
   (ก) { shift: {…8 ฟิลด์…}, roster_version_id, shift_pattern_version_id, linked:true }
       → ใช้กะนี้เลย · เก็บ version_id.shift = shift_pattern_version_id
         และเก็บ roster_version_id ไว้ด้วย เพื่อรู้ทีหลังว่าค่าเก่าหรือยัง (RO-4)
   (ข) { shift: null, reason:'NO_SHIFT_FOR_EMPLOYEE_DAY' }
       → **ตกไปแหล่ง ② ตามที่ Attendance ออกแบบไว้เอง** (กะมาตรฐานจาก shift_pattern)
         ★ ห้ามตีความ null ว่าเป็นข้อผิดพลาด และห้ามให้ Roster เดากะให้ (RO-2)
   (ค) { shift: null, linked:false, reason:'MODULE_NOT_LINKED' }
       → เหมือน (ข) — ทางสำรองทำงานตามปกติ

4. เมื่อ Roster เผยแพร่ซ้ำ:
   · วันที่ Attendance ยัง pending → กะเปลี่ยนได้ · Attendance อ่านใหม่แล้วพบ roster_version_id ใหม่
   · วันที่ Attendance confirmed/locked → **Roster ปฏิเสธการเปลี่ยนตั้งแต่ต้นทาง**
     Attendance จึงไม่มีวันเจอค่าที่ขัดกับสิ่งที่ยืนยันไปแล้ว (BR-16)

5. Attendance ห้ามเขียนอะไรกลับมาที่ Roster เลย (RO-5) — การแก้กะทำที่ #/roster/grid เท่านั้น
```

## §0.14 ⭐ Roster Data Contract — invariant ที่ห้ามผิด

### §0.14.1 invariant ของ feature นี้ (`R-1…R-10`)

| # | invariant | ถ้าผิดจะเกิดอะไร | ทดสอบที่ |
|---|---|---|---|
| **R-1** | **มุมมองที่เผยแพร่คืนเฉพาะเวอร์ชัน `published` ปัจจุบัน** — ร่าง/ถูกแทนที่/ยกเลิกร่าง ไม่หลุดออกไป | พนักงานถูกตัดสินด้วยแผนที่ยังไม่มีใครประกาศ | `06_TESTS IA-01` |
| **R-2** | **ไม่มีกะ → คืน `null` เสมอ ห้ามเดา** | **ทางสำรองของ Attendance พังทั้งระบบ** | `06_TESTS IA-07` |
| **R-3** | **ตารางที่มีข้อขัดแย้งระดับ `block` ค้าง เผยแพร่ไม่ได้** | ตารางผิดกฎออกไปถึงปลายทาง | `06_TESTS IA-02` |
| **R-4** | **ช่วงเวลาที่ทับกันของคนเดียวกันเป็น `block` เสมอ · ช่วงที่ไม่ทับกันไม่เป็นข้อขัดแย้ง** | (ผิดทางหนึ่ง) ตารางสั่งสิ่งที่เป็นไปไม่ได้ · (ผิดอีกทาง) กะแยกช่วงที่ถูกกฎถูกบล็อกผิด | `06_TESTS IA-03` |
| **R-5** | **กะของวันที่ปลายทางบริโภคแล้ว เปลี่ยนไม่ได้** — ปฏิเสธรายวันพร้อมชี้วัน | ยอดที่ Payroll ใช้ไม่ตรงกับตาราง ตอบข้อพิพาทไม่ได้ | `06_TESTS IA-04` |
| **R-6** | **การแก้ด้วยมือกับการสลับกะเรียก engine ตรวจตัวเดียวกัน** | เกิดทางลัดที่สลับแล้วได้ตารางผิดกฎ (ขัด **C-17**) | `06_TESTS IA-05` |
| **R-7** | **ไม่มีตัวเลขค่ากฎหมายในโค้ดหรือในหน้าจอ** — ไม่มีค่าเกณฑ์ = ไม่ตรวจ + ป้าย | ผิด **P-8** · ผู้ใช้เข้าใจผิดว่าตารางผ่านกฎครบ | `06_TESTS IA-06` |
| **R-8** | **ผู้ยืนยันคำขอสลับมาจาก Policy Center เท่านั้น — ไม่มีรายชื่อ/ตำแหน่งในโค้ด และไม่เรียก DOA** | ขัด **LOCK-DOA** · สายบังคับบัญชาจริงเปลี่ยนแล้วระบบไม่รู้ | `06_TESTS IA-08` |
| **R-9** | **ไม่มีตัวเลขเงิน ไม่มีตัวเลขความต้องการกำลังคน ในทุกหน้าจอทุก payload · ไม่มี write endpoint สำหรับ consumer** | scope drift ทันที · ร่องรอยขาดตอน | `06_TESTS IA-09` |
| **R-10** | **ตารางประวัติรับได้เฉพาะการเพิ่มแถว — ปฏิเสธ UPDATE/DELETE ที่ชั้นฐานข้อมูล** | ร่องรอยแก้ได้ = ไม่ใช่ร่องรอย | `06_TESTS IA-10` |

> **ตกข้อใดข้อหนึ่ง = หยุด release** — ไม่ใช่ข้อสังเกต

### §0.14.2 กติกาที่ feature นี้ต้องทำตามในฐานะ consumer ของ HR Configuration (`C-1…C-6` · `P-1…P-9`)

| # | กติกา | ทำที่ไหนในแพ็กนี้ |
|---|---|---|
| **C-1** | ส่ง `date` ของเหตุการณ์ธุรกิจเสมอ — **คือวันของช่องในตาราง ไม่ใช่ "วันนี้"** | `03_LOGIC F-02` · `05_RULES BR-01` · `06_TESTS AT-02` |
| **C-2** | เก็บ `version_id` คู่กับตารางที่เผยแพร่ — **ทั้งที่หัว (`config_version_ids`) และรายช่อง (`shift_pattern_version_id`)** | `04_DB §4.2` · `06_TESTS AT-02` |
| **C-3** | ห้าม cache ข้ามวัน · ล้างเมื่อได้ `hrconfig.effective` | `03_LOGIC F-02` (PR-07) · `05_RULES BR-02` |
| **C-4** | ห้าม CRUD ของ HR Config — **ไม่มี endpoint เขียนไปต้นทางแม้แต่ตัวเดียว** | `02_API §2.1` (ตรวจรายการ) · `05_RULES BR-03` |
| **C-5** | กะที่ `inactive` เลือกใหม่ไม่ได้ **แต่ตารางเก่าที่อ้างอยู่ต้องแสดงได้** | `03_LOGIC F-06` · `05_RULES BR-04` · `06_TESTS AT-09` |
| **C-6** | ลงทะเบียน where-used — `POST /hr-config/items/:id/usage` **4 กลุ่มค่า** (`shift_pattern` · `holiday_calendar` · `period_rule` · **`shift_rule` แม้ยังไม่มีค่า**) | `03_LOGIC F-47` · `02_API API-21` |
| **P-1** | ค่านโยบายมี `effective_date` เสมอ | อ่านผ่าน resolve เท่านั้น |
| **P-2** | ห้ามเขียนทับค่าที่มีผลแล้ว | ตารางที่ `published` คงค่าเดิมตาม `config_version_ids` (`05_RULES BR-02`) |
| **P-5** | ถามค่าต้องระบุวันเสมอ | เหมือน C-1 |
| **P-7** ⭐ | **ห้ามแตะงวดที่ปิดแล้ว** | `03_LOGIC §3.0.5` · `F-30` · `05_RULES BR-16` · `06_TESTS IA-04` |
| **P-8** ⭐ | **ห้าม hardcode ค่าที่มาจากกฎหมาย** | `03_LOGIC §3.0.4` · `05_RULES BR-11` · `06_TESTS IA-06` |
| **P-9** | ไม่มี retro — แก้ผลย้อนหลังของสิ่งที่ถูกบริโภคแล้วทำไม่ได้ | `05_RULES BR-16` |

### §0.14.3 กติกาที่ feature นี้ต้องทำตามในฐานะ consumer ของ Attendance (`AT-1…AT-7`) · Leave · OT (`OT-1…OT-7`)

| # | กติกา | ทำที่ไหนในแพ็กนี้ |
|---|---|---|
| **AT-1 / OT-1** | ส่ง `date` เสมอ | `03_LOGIC F-19` `F-21` `F-24` |
| **AT-2 / OT-2** | เก็บ `version_id` ของค่าที่อ่านมา | `04_DB` `consumed_by_attendance` · `ot_ref` เก็บ snapshot |
| **AT-3 / OT-3** | ห้าม cache ข้ามวัน · ล้างเมื่อได้ event ของต้นทาง | `03_LOGIC F-24` |
| **AT-4** ⭐ | **ตรวจ `day_status` ก่อนใช้ค่า** — `exception` แปลว่าข้อมูลยังไม่ครบ ไม่ใช่ "ทำงาน 0 ชั่วโมง" · **feature นี้ใช้ `day_status` เพื่อตัดสินว่าวันไหนแตะไม่ได้เท่านั้น ไม่เอาชั่วโมงมาใช้เลย** | `03_LOGIC §3.0.5` · `05_RULES BR-16` |
| **AT-5 / OT-5** ⭐ | **ห้ามเขียนกลับทุกกรณี** | `02_API §2.2` (ตรวจรายการ — ไม่มี endpoint เขียนไป Attendance/OT/Leave) |
| **AT-6** ⭐ | **ห้ามคำนวณ สาย/ขาด/ชั่วโมงจริง เอง** | `03_LOGIC` ไม่มี function ใดคำนวณชั่วโมงจริง · `05_RULES BR-21` · `06_TESTS AT-48` |
| **OT-4** | **ห้ามคำนวณชั่วโมง OT เอง** · ห้ามใช้ `outside_shift_hours` เป็นชั่วโมง OT | `03_LOGIC F-21` (อ่านมาแสดงธงอย่างเดียว) |
| **OT-6** | **ห้ามตีความ `multiplier` เป็นจำนวนเงิน** | `03_LOGIC F-21` ไม่อ่าน `multiplier` เลย |
| **AT-7 / OT-7** | ลงทะเบียน where-used — `POST /attendance/usage` · `POST /ot/usage` (+ `POST /leave/usage`) | `03_LOGIC F-47` · `02_API API-21` |
| **OT §0.13.2 กรณีพิเศษ** | ใบที่ `withdrawn` ถือว่าไม่มีผล · **"ไม่มีใบ" ≠ "ไม่ได้ทำ OT"** | `03_LOGIC F-21` · `05_RULES BR-13` · `06_TESTS AT-19` |
| **Leave** | อ่านวันลาที่อนุมัติแล้ว display-only · ห้ามคำนวณวันลาเอง ห้ามเขียนกลับ | `03_LOGIC F-19` · `05_RULES BR-12` |

## §0.15 ⭐ Soft-Reference Read Model (LD-4C-02) — วิธีที่ feature อื่นเชื่อมกับที่นี่

### §0.15.1 ทิศทาง "เข้า" — feature นี้อ้างของคนอื่น

| อ้างอะไร | เก็บอะไรไว้ | nullable? | FK cascade? | ถ้าต้นทางหาย |
|---|---|---|---|---|
| คน (Employee Master) | `employee_id` + `employee_name_snapshot` + ตำแหน่ง/แผนก snapshot | ✅ | ❌ **ไม่มี** | แถวยังแสดงชื่อจาก snapshot (BR-30) |
| บริษัท (Organization) | `company_id` + `company_name_snapshot` | ❌ (บังคับ) | ❌ | เช่นเดียวกัน |
| กะ/วันหยุด/งวด (HR Config) | `shift_code` + snapshot ทุกฟิลด์ + `shift_pattern_version_id` | ✅ | ❌ | ช่องเก่ายังแสดงได้แม้กะถูกปิดใช้ (C-5) |
| วันลา (Leave) | `leave_ref = {leave_no, leave_type_snapshot}` | ✅ | ❌ | ธงหาย · ไม่กระทบตาราง |
| ใบ OT (OT) | `ot_ref = {ot_no, time_from, time_to, ot_status}` | ✅ | ❌ | ธงหาย · ไม่กระทบตาราง |
| สถานะวัน (Attendance) | `consumed_by_attendance = {day_status, period_status}` | ✅ | ❌ | **ต้องบล็อกการเผยแพร่ซ้ำ ห้ามถือว่า "ไม่ถูกบริโภค"** (EN-02) |
| สายบังคับบัญชา (Policy Center) | ไม่เก็บ — **resolve สดทุกครั้ง** | — | ❌ | ปุ่มยืนยันไม่ปรากฏ |

### §0.15.2 ทิศทาง "ออก" — คนอื่นอ้าง feature นี้

| ใครอ้าง | อ้างด้วยอะไร | เก็บอะไรไว้ที่ฝั่งเขา | ห้ามทำอะไร |
|---|---|---|---|
| **Attendance** | `roster_version_id` + `shift_pattern_version_id` | `version_id.shift` ของวันนั้น + `roster_version_id` | **ห้ามเขียนกลับ · ห้ามเก็บกะโดยไม่มี version_id** |
| **OT** | `roster_version_id` | `config_version_ids.shift` ของใบ | เช่นเดียวกัน |
| **ESS (W6)** | `roster_version_id` | — (แสดงสด) | **ไม่ทำ CRUD ซ้ำ — เรียกหน้าของ feature นี้** |
| **ชั้นรายงาน 7C** | `roster_version_id` (`ref` ของ envelope) | event log | **ห้ามแก้ event เดิม — ปรับปรุงด้วย event ใหม่ที่ `supersedes`** |

### §0.15.3 ทำไมต้อง soft — ไม่ใช่ FK จริง

1. **feature คนละรอบส่งมอบ** — Attendance เสร็จก่อน (W1) · ESS ยังไม่เกิด (W6) · FK จริงจะทำให้ deploy ผูกกันแน่นจนแยกไม่ออก
2. **ข้อมูลบุคคลเปลี่ยนแล้วตารางเก่าต้องอ่านได้** — คนลาออกแล้วตารางเดือนที่แล้วต้องยังตอบข้อพิพาทได้ (BR-30)
3. **การลบที่ต้นทางต้องไม่ลบร่องรอยที่นี่** — cascade delete จะทำลาย audit trail ซึ่งขัด **LOCK-AUDIT** โดยตรง
4. **ทิศทางการอ่านเป็นเส้นเดียว** — feature นี้อ่านจากต้นทาง 6 แหล่ง และให้ปลายทาง 4 รายอ่าน · **ไม่มีเส้นไหนเป็นสองทาง** จึงไม่มีความจำเป็นต้องมี referential integrity ข้ามฝั่ง

## §0.16 ⭐ Declaration Conformance — event ⊆ brief (Lane Mode v2 gate)

> **กติกาของ gate:** ทุก event ที่แพ็กนี้ระบุ **ต้องเป็นสมาชิกของใบประกาศที่ออกไว้แล้วที่ S1.8** — **ห้ามเพิ่ม event ใหม่ที่ FRD** · ถ้าจำเป็นต้องเพิ่ม ต้อง **append ในใบเดิม** ไม่ใช่ออกใบใหม่

### §0.16.1 NTF — **6 event ธุรกิจ** (⊆ `NTF_BRIEF.md §2`)

| # | event_id | trigger จริงใน `03_LOGIC` | ผู้รับ | ⊆ brief? |
|---|---|---|---|---|
| **N1** | `roster_published` | **`F-25 publishRoster`** (T-3 · การเผยแพร่ครั้งแรกของเดือน) | พนักงานทุกคนที่มีกะ ≥1 ช่อง + ผู้จัดตาราง (สำเนา) | ✅ |
| **N2** ⭐ | `roster_shift_changed` | **`F-31 notifyChangedEmployees`** ที่ถูกเรียกจาก `F-28 republishRoster` (T-4) | **เฉพาะพนักงานที่กะเปลี่ยนจริง** (คำนวณจาก diff ก่อน emit) | ✅ |
| **N3** | `roster_swap_requested` | **`F-33 createSwapRequest`** (W-1) | คู่สลับ | ✅ |
| **N4** | `roster_swap_accepted` | **`F-37 acceptSwapRequest`** (W-2) | หัวหน้าของผู้ขอ + ผู้ขอ (สำเนา) | ✅ |
| **N5** | `roster_swap_decided` | **`F-39 confirmSwapRequest`** (W-3) **และ** **`F-40 rejectSwapRequest`** (W-4 · ทั้งคู่สลับปฏิเสธและหัวหน้าปฏิเสธ) | ผู้ขอ + คู่สลับ | ✅ |
| **N6** | `roster_swap_expired` | **`F-60 expireStaleSwapRequests`** (W-6 · scheduler) | ผู้ขอ + คู่สลับ (+ หัวหน้าที่ค้างงาน) | ✅ |

**ข้อบังคับที่ยกมาจาก `NTF_BRIEF §5` และต้องบังคับที่โค้ด:**
- **N1 กับ N2 ห้ามยิงพร้อมกันในการกระทำเดียว** — เผยแพร่ครั้งแรก = N1 · เผยแพร่ซ้ำ = N2 เท่านั้น (`03_LOGIC F-25` vs `F-28`)
- **N2 ต้องคำนวณ "ใครกะเปลี่ยน" จาก diff ก่อน emit** แล้ว emit ทีละคนพร้อมจำนวนวันที่เปลี่ยนของคนนั้น — **ห้าม emit ให้ทุกคนในตาราง** (BR-17)
- **N5 ยิงครั้งเดียวต่อคำขอ** ไม่ว่าจบด้วยยืนยันหรือปฏิเสธ (ค่า `{decision}` เป็นตัวแยก)
- **ข้อความต้นแบบทั้ง 6 อยู่ในใบประกาศ ไม่ฝังในโค้ดของ feature** · **ห้ามเช็ค user preference เอง ห้ามเลือกช่องทางเอง**
- **ไม่มี `doa_pending` / `doa_result` / `doa_escalate` ให้ประกาศ — เพราะ feature นี้ไม่มีสายอนุมัติเลย** (`NOT_NEEDED.md`)

**event ที่จงใจไม่ประกาศ (⊆ `NTF_BRIEF §3` · ตรวจแล้วว่าแพ็กนี้ไม่ได้แอบเพิ่ม):**
การบันทึกร่าง · การทิ้งร่าง · การแก้ช่องระหว่างร่าง · การรับทราบคำเตือน · ข้อขัดแย้งที่ตรวจพบ · การล็อกเมื่องวดปิด (ต้นทางเป็นผู้ประกาศ) · การรับทราบกะของพนักงาน (**เป็นส่วนขยายของ N1/N2 ไม่ใช่ event ใหม่** · BR-33) · `hrconfig.*` / `attendance.*` / `ot.*` / `leave.*` (ต้นทางเป็นเจ้าของ) · การที่ปลายทางอ่าน read model (เป็น pull ไม่ใช่ push)
**ค้างอยู่:** การเตือน "ยังมีวันที่ยังไม่จัดกะก่อนถึงวัน" — **ยังประกาศไม่ได้เพราะต้องมี `shift_rule.freeze_days` ซึ่งต้นทางยังไม่เผยแพร่** (`OQ-NTF-03` · **OQ-R15**) · เมื่อ Strike เคาะแล้วให้ **append ใน `NTF_BRIEF` เดิม ห้ามออกใบใหม่**

### §0.16.2 CSQ — **2 event · 1 ท่อ (EC เท่านั้น)** (⊆ `CSQ_BRIEF.md §2`)

| # | event_id | trigger จริงใน `03_LOGIC` | ท่อ · kind | ⊆ brief? |
|---|---|---|---|---|
| **E1** | `roster.published` | **`F-25 publishRoster`** (T-3) | **EC** · `kind: estimated` · `basis: declared` (หน่วยชั่วโมง) | ✅ |
| **E2** | `roster.republished` | **`F-28 republishRoster`** (T-4 — ทั้งจาก `F-27 applyManualEdits` และจาก `F-39 confirmSwapRequest`) | **EC** · `kind: estimated` | ✅ |

**Payload field ทุกตัวมีจริงใน `04_DB` แล้ว (ปิด `CSQ_BRIEF §5 G5` ที่ค้างอยู่ตั้งแต่ S1.8):**

| field | มีจริงที่ | หมายเหตุ |
|---|---|---|
| `roster_version_id` · `company_id` · `period_month` · `scope_team` | `04_DB T_roster_version` | `ref` ของ envelope |
| `employee_id[]` · `affected_employee_id[]` | `04_DB T_roster_cell.employee_id` (derive) | **PII — ส่ง id เท่านั้น ห้ามส่งชื่อดิบ** |
| `planned_shift_count` · `planned_hours_total` · `planned_hours_by_employee[]` · `planned_hours_delta_by_employee[]` | `04_DB §4.4` (computed จาก `hours_per_day`) | **ปริมาณล้วน ไม่มีเงิน** |
| `night_shift_count` · `holiday_shift_count` | `04_DB §4.4` (derive จาก `is_overnight` · `holiday_ref`) | **บริบท ไม่ใช่ตัวคูณ** |
| `config_version_ids` | `04_DB T_roster_version.config_version_ids` | **`shift_rule` เป็น `null` ได้** (OQ-STD-R6 · **OQ-CSQ-02**) |
| `published_by` · `published_at` · `warning_ack_items[]` | `04_DB T_roster_version` | ร่องรอยการรับทราบคำเตือน |
| `changed_cell_count` · `publish_note` | `04_DB T_roster_version` + `T_roster_cell` (derive) | เฉพาะ E2 |
| **`adjust_kind`** (`manual_edit` \| `shift_swap`) | `04_DB T_roster_version.adjust_kind` | **เฉพาะ E2 — ตัวแยกที่ทำให้การสลับกะไม่ถูกนับสองครั้ง** |
| `rejected_locked_dates[]` | `04_DB T_roster_version.rejected_locked_dates` | บริบทการปฏิบัติตาม **P-7** |
| `supersedes` | `04_DB T_roster_version.supersedes` | **ชี้ event เดิม ห้ามแก้ผลเดิม** (BR-CSQ-04) |
| `idempotency_key` | สร้างที่ `03_LOGIC F-59` | unique ต่อ (`F-HR-ROSTER`, `roster_version_id`, action) |

**ทำไมไม่ทับกับ EC ของพี่น้องในโมดูลเดียวกัน (ยกมาจาก `CSQ_BRIEF §2` — ห้ามลืม):**

| feature | event | ท่อ · kind | ก้อนอะไร |
|---|---|---|---|
| **Attendance** | `attendance.day_confirmed` | EC **`actual`** | ชั่วโมงที่ทำงานจริงในกรอบกะ |
| **OT** | `ot.time_confirmed` | EC **`actual`** + FC | ชั่วโมงล่วงเวลาที่อนุมัติและยืนยันแล้ว (นอกกรอบกะ) |
| **Shift & Roster** *(แพ็กนี้)* | `roster.published` | EC **`estimated`** | **ชั่วโมง-กะที่วางแผนไว้** |

**สามก้อนนี้เป็นคนละชั้นเวลาโดยนิยาม:** *แผน (estimated) → ของจริงในกรอบกะ (actual) → ของจริงนอกกรอบกะที่อนุมัติแล้ว (actual)* — Engine แยกด้วย `kind` ได้ตรง ๆ **ไม่ต้องพึ่งการตีความ** · **ถ้าประกาศเป็น `actual` จะเป็นการนับซ้ำทันที** เพราะคนที่ถูกจัดเวรไว้แต่ลาป่วยไม่มา ไม่ได้ใช้แรงงานขององค์กรเลย

**ท่อที่ไม่ประกาศ (⊆ `CSQ_BRIEF §3`):** **OC** (มาจาก Operation Process — 422) · **DC ระดับเอกสาร** (มาจาก DOA ซึ่ง feature นี้ไม่มีเลย — 422) · **SC** (สงวน — 422) · **FC** (การจัดกะยังไม่ผูกพันเงิน — ภาระผูกพันเกิดที่ OT ตอนอนุมัติ) · **AC** (ไม่มีรายการบัญชี) · **SecC** (นโยบายกะเป็นของ HR Configuration ซึ่งประกาศไว้แล้วที่ `CSQ-HRCFG` E1–E6 — ประกาศที่นี่ = นับซ้ำ)

### §0.16.3 ⭐ สองชุด event เป็นคนละชุดกัน (disjoint) — ตรวจแล้ว

| ชุด | ชื่อ event | ปลายทาง |
|---|---|---|
| **ENG-NOTIFY (6)** | `roster_published` · `roster_shift_changed` · `roster_swap_requested` · `roster_swap_accepted` · `roster_swap_decided` · `roster_swap_expired` | **คน** (in-app + email) |
| **ENG-CSQ 7C (2)** | `roster.published` · `roster.republished` | **ชั้นรายงาน** (ท่อ EC) |

**ตรวจชื่อชนกันแล้ว: ไม่มีชื่อซ้ำแม้แต่ตัวเดียว** — ชุดแจ้งเตือนใช้ `snake_case` ทั้งชื่อ (`roster_published`) · ชุด 7C ใช้ `dot.notation` (`roster.published`) · **`roster_published` ≠ `roster.published`** เป็นคนละสตริง คนละ catalog คนละปลายทาง
**จุดที่ยิงพร้อมกันคือ T-3 และ T-4** — แต่เป็น **การยิงคนละระบบ ไม่ใช่การยิงซ้ำ** (`03_LOGIC F-58` = NOTIFY · `F-59` = CSQ)

### §0.16.4 DOA — **ไม่มี** (⊆ `NOT_NEEDED.md`)

**feature นี้ไม่ประกาศ DOA และไม่เรียก `GET /doa/resolve` เลย** — เหตุผลเต็มที่ `BRD §4.3`:
1. scope note ตัดสินตรง: *"ขอสลับกะ (พนักงาน→หัวหน้ายืนยัน **ไม่ผ่าน DOA**)"*
2. จุดตัดสินใจเดียว (W-3) เป็น **สิทธิ์ตามสายบังคับบัญชาจาก Policy Center** — ไม่มีเลขที่เอกสาร ไม่มีลายเซ็น ไม่มีวงเงิน ไม่มีหลายชั้น ไม่มีการมอบฉันทะ → **ไม่มีอะไรให้ทะเบียนกลาง resolve**
3. **ผลพลอยได้:** ไม่มี DOA → **ไม่มีท่อ DC ระดับเอกสารให้ประกาศตั้งแต่ต้น** (§0.16.2) และ **ไม่มี `doa_*` ให้ประกาศซ้ำในใบแจ้งเตือน** (§0.16.1)

**ตรวจที่โค้ด:** `03_LOGIC F-41 resolveConfirmer` เรียก **`ENG-ROLESCOPE-01` เท่านั้น** · `02_API` ไม่มี endpoint ใดเรียก DOA · `06_TESTS IA-08` พิสูจน์ข้อนี้

### §0.16.5 DOCCFG — **ไม่มี** (⊆ `NOT_NEEDED.md`)

**ไม่มีเลขที่เอกสารที่คนอ้างถึงข้ามระบบ** — `roster_version_id` และ `swap_request_id` เป็น **uuid ภายในของ feature** ไม่ใช่เลขรันที่ Document Configuration ออกให้ · **ตรวจที่โค้ด:** `03_LOGIC` ไม่มี function ใดเรียกระบบออกเลขเอกสาร · `04_DB` ไม่มีคอลัมน์ `doc_no` · `06_TESTS AT-56`

### §0.16.6 PDFDOC — **ไม่มี** (⊆ `NOT_NEEDED.md`) ⭐

**ไม่มีแบบฟอร์มทางการที่ต้องพิมพ์/ลงนาม/ยื่น** — **นี่คือเหตุผลที่แพ็กนี้ไม่มี `PRINT_SPEC.md`**
การพิมพ์ตารางออกมาติดบอร์ดเป็น **ความสะดวกในการพิมพ์หน้าจอของเบราว์เซอร์** ไม่ใช่ความสามารถของ feature และไม่ใช่เอกสารที่มีเลขและลายเซ็น (`STANDARD_BASELINE §3` · `BRD §14.6.3 NS-07`)
**ตรวจที่โค้ด:** `01_UI` ไม่มีหน้า/แท็บ PDF · ไม่มีแท็บลายเซ็น · ไม่มี `.a4` · `06_TESTS AT-56`

### §0.16.7 สรุปผล gate

| ท่อ | brief ที่ออกไว้ที่ S1.8 | จำนวนใน FRD | ⊆ brief? | หมายเหตุ |
|---|---|---:|:---:|---|
| **NTF** | `NTF_BRIEF.md` **6 event** | **6** | ✅ | ไม่เพิ่ม ไม่ลด · trigger ถูกแทนที่ด้วย `03_LOGIC F-xx` จริงแล้ว (ปิด G4 ที่ค้าง) |
| **CSQ** | `CSQ_BRIEF.md` **2 event · EC ท่อเดียว** | **2** | ✅ | **ปิด G5 ที่ค้าง** — ทุก payload field ยืนยันแล้วว่ามีจริงใน `04_DB` (§0.16.2) |
| **DOA** | `NOT_NEEDED.md` | **0** | ✅ | ไม่มีการเรียก DOA ที่ใดในแพ็ก |
| **DOCCFG** | `NOT_NEEDED.md` | **0** | ✅ | ไม่มีคอลัมน์เลขที่เอกสาร |
| **PDFDOC** | `NOT_NEEDED.md` | **0** | ✅ | **ไม่มี `PRINT_SPEC.md` ในแพ็ก — โดยเจตนา** |

**Gate ผ่าน: event ⊆ brief ครบทั้ง 5 ท่อ · ไม่มี event ใดถูกเพิ่มที่ FRD**
**สิ่งที่ต้อง append กลับเข้าใบประกาศเดิม (ไม่ใช่ออกใบใหม่):** `CSQ_BRIEF §5` ให้ติ๊ก **G4** (trigger อ้าง `03_LOGIC` จริง) และ **G5** (payload มีจริงใน `04_DB`) — หลักฐานอยู่ที่ **§0.16.2** ของไฟล์นี้
