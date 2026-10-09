# 00_OVERVIEW — F-HR-OT · OT / Shift (โอที)

> **FRD Pack variant: FULL (9 ไฟล์ + INDEX + PRINT_SPEC)** — fallback จาก BRD: pages=4 · states=7 · approval=Yes (สายอนุมัติจริง **2 ชั้น/3 ชั้น**) · money=No แต่ **มี state machine 7 สถานะ + 11 transition + 2 สายอนุมัติ + 5 ท่อประกาศ** → เกณฑ์ `states ≥ 4` เข้าเงื่อนไข FULL
> **Design Authority (v6.1 dual mode): มี HTML ที่ผ่าน gate → โหมด "สกัด + ตรวจ + บันทึก"** — FRD ห้ามเขียน spec ที่สวนกับจอจริง (R14)
> Lane Mode v2 · `frd-generator-v6` · S5 · 2026-08-29 · **ห้ามถาม (no-ask)**

## §0.1 Document Control

| | |
|---|---|
| FRD ID | FRD-HR-OT-001 |
| Feature | OT / Shift · โอที (ใบขอทำงานล่วงเวลา) |
| Feature Code | `F-HR-OT` |
| Module / Wave / Lane | HR · W2 · Lane B |
| Archetype | **Q-document** (Pattern Q · wizard 5 ขั้น · view tabs รายละเอียด›PDF›ลายเซ็น›ประวัติ · เอกสารแนบใน landing · line editor B2 v2 แบบไม่มีเงิน) |
| Pack Variant | **FULL** — `00_OVERVIEW` `01_UI` `02_API` `03_LOGIC` `04_DB` `05_RULES` `06_TESTS` `07_LOCKED_DECISIONS` `INDEX` **+ `PRINT_SPEC`** (มีท่อเอกสาร PDF) |
| Version / Status | 1.0 · **Phase 3.5 PASSED** |
| Source BRD | `2_BRD/BRD_โอที.md` v1.0 · **Status = APPROVED** (Quality Gate 28/28) |
| Source HTML | `1_HTML/โอที.html` · 4,707 บรรทัด · **4 route** · ผ่าน S3a (FAIL=0) · S3b (BLOCK=0 · pageerror=0 · 54 ภาพ) · S3c (FN 65/65 · DECL 5/5 · SURFACE 6/6) |
| Declarations | `5_DECLARATIONS/` — `DOA_BRIEF` · `NTF_BRIEF` · `CSQ_BRIEF` · `DOCCFG_BRIEF` · `PDFDOC/{template.html, sample.pdf, print-spec.md}` · `NOT_NEEDED.md` |
| Upstream contract | `F-HR-CONFIG §0.13` (config surface · `resolve(date, company)` · C-1…C-6) · `§0.14` (P-1…P-9) · `§0.15` (soft reference) · `F-HR-ATTEND §0.13` (time surface · AT-1…AT-7 · **`outside_shift_hours` = ยังไม่ใช่ OT ที่อนุมัติ**) · `F-HR-LEAVE §0.13` (leave surface · LV-1…LV-7) |
| Downstream | **Payroll (⏳W4)** · **ESS Portal (⏳W6)** · Shift & Roster (⏳W2 lane C) · ชั้นรายงาน 7C — **อ่าน §0.13 ของแพ็กนี้** |
| Audience | 01_UI → FE · 02_API → BE (ชั้น HTTP) · 03_LOGIC → BE (ตรรกะธุรกิจ) · 04_DB → DBA/BE · 05_RULES → BE+QA · 06_TESTS → QA · PRINT_SPEC → ทีมทำเอกสาร |

## §0.2 Revision History

| Version | Date | โดย | อะไรเปลี่ยน |
|---|---|---|---|
| 1.0 | 2026-08-29 | `frd-generator-v6` (Lane Mode v2 · S5) | สร้างแพ็กครั้งแรกจาก BRD v1.0 (APPROVED) + HTML v9 ที่ผ่าน gate ครบ · Phase 2.5 probing ทำแบบ no-ask (ดู §0.8.1) · Phase 3.5 A–M ผ่านทั้งหมด |

## §0.3 Scope

### In Scope

| # | ขอบเขต | ที่อยู่ในแพ็ก |
|---|---|---|
| 1 | ใบขอ OT ล่วงหน้า/ย้อนหลัง ผ่านตัวช่วย 5 ขั้น | `01_UI §1.2 P-01` · `03_LOGIC §3.1` |
| 2 | บรรทัดช่วงเวลาหลายบรรทัดต่อใบ พร้อมประเภทวัน/อัตรา/ตัวคูณ/ชั่วโมงรายบรรทัด | `01_UI §1.2 P-01` · `04_DB §4.2 T_ot_request_line` |
| 3 | **resolve อัตรา · ตัวคูณ · เพดาน · ประเภทวัน · งวด จาก HR Configuration ณ `work_date`** + เก็บ `config_version_ids` | `03_LOGIC ENG-HRCFG-READ` · `05_RULES BR-01…BR-03` |
| 4 | ตรวจเพดานรายสัปดาห์ → ธง `over_cap` → **สายอนุมัติยาวขึ้น** | `03_LOGIC §3.1 resolveCap/computeOverCap` · `05_RULES BR-09` |
| 5 | สายอนุมัติจาก DOA Engine (2 ขั้น / 3 ขั้น) เลือกด้วย **action id** | `03_LOGIC §3.1 selectApprovalAction` · `02_API API-06` |
| 6 | อนุมัติ / ไม่อนุมัติ / อนุมัติบางส่วน / ยกเลิก / ถอน | `02_API API-08…API-12` · `05_RULES §5.2` |
| 7 | เทียบชั่วโมงที่ขอกับ `outside_shift_hours` + ธง/บล็อก/การรับทราบส่วนต่าง | `03_LOGIC §3.1 computeVariance` · `05_RULES BR-16` |
| 8 | **ยืนยันเวลาจริง → `time_confirmed`** (สถานะเดียวที่ถูกเผยแพร่) | `02_API API-13` · `05_RULES BR-17` |
| 9 | เลขที่ `OT-YYYY-NNNN` จาก ENG-DOC-NUM ตอน submit · immutable | `03_LOGIC ENG-DOC-NUM` · `05_RULES BR-13` |
| 10 | ใบ OT PDF (A4 1 หน้า) + ช่องลงนาม 3/4 ช่อง + สำเนา `approved_final` | **`PRINT_SPEC.md`** · `03_LOGIC ENG-DOC-STORE` |
| 11 | **Published OT Surface** (`day` + `period`) ให้ Payroll/ESS/Roster อ่าน — **ไม่มีเงิน** | **§0.13** · `02_API API-20 · API-21` |
| 12 | สรุปงวดต่อคนแยกตาม `rate_type` + ตรึงยอดเมื่อปิดงวด | `01_UI §1.2 P-04` · `03_LOGIC §3.1 buildPeriodSummary` |
| 13 | ธง `needs_review` เมื่อ `attendance.day_adjusted` | `03_LOGIC §3.1 onAttendanceDayAdjusted` · `05_RULES BR-22` |
| 14 | ยื่นแทนลูกทีม → แตก 1 ใบต่อคน + ช่องรับทราบ | `03_LOGIC §3.1 splitProxyRequests` · `05_RULES BR-26 · BR-28` |
| 15 | 7 event แจ้งเตือน (NTF) + 5 event ผลกระทบ 7C (CSQ · EC+FC) | **§0.16** |
| 16 | ประวัติ append-only ทุกการเปลี่ยน · ไม่มี hard delete | `04_DB T_ot_history` · `05_RULES BR-14` |

### Out of Scope

**17 รายการตาม BRD §14.6.3 (NS-01…NS-17)** — ยกมาครบใน **§0.12.3b** เพื่อให้อยู่ในแมนิเฟสต์ ไม่หายเงียบ
สรุปหัวข้อ: คำนวณเงิน · ชดเชยเป็นวันหยุด · ค่ากะ/กลางคืน · คุมงบ · จัดกะ/เวร · เพดานรายวัน-รายเดือน · หน้าตั้งค่า · แก้เวลาเข้า-ออก · บริหารสิทธิ์ลา · ลบถาวร · การ์ด 7 ด้าน · สลับบริษัท · อนุมัติอัตโนมัติ · on-call/standby · แดชบอร์ดแนวโน้ม · พิมพ์หลายใบ · มอบฉันทะ/เตือนซ้ำ

### Out of Scope (จาก Phase 2.5 probing — บันทึกไว้ไม่ให้หายเงียบ)

| # | ที่ probe เจอ | ตัดสินอย่างไร |
|---|---|---|
| PR-A | การแนบไฟล์ขนาดใหญ่ / สแกนไวรัส | ใช้บริการไฟล์กลางของแพลตฟอร์ม — ไม่ทำในแพ็กนี้ · ระบุเป็นข้อกำหนดของแพลตฟอร์มใน `05_RULES §5.7` |
| PR-B | การส่งออกเป็น Excel ของสรุปงวด | อยู่ในขอบเขต แต่ **ต้องผ่านชั้น masking เดียวกับหน้าจอ + audit** (`05_RULES §5.8 D-08`) |
| PR-C | การแบ่งหน้าเมื่อ `scope=company` | กำหนดใน `02_API API-20` (page_size สูงสุด 500) |
| PR-D | เขตเวลา | ทั้งระบบใช้เขตเวลาเดียวของผู้เช่า — `07_LOCKED LD-OT-09` |
| PR-E | การย้อนสถานะจาก `withdrawn` กลับ | **ไม่มี** — ยื่นใบใหม่เท่านั้น (`05_RULES §5.2` · LOCK-AUDIT) |

## §0.4 Roles & Responsibilities (COSO)

| Role | COSO | ทำอะไรได้ในระบบ | ขอบเขตข้อมูล |
|---|---|---|---|
| พนักงาน (ผู้ขอ) | **Maker** | สร้าง/แก้ร่างของตัวเอง · submit · cancel · ขอ withdraw · ดูใบ+ชั่วโมงสะสมของตัวเอง · พิมพ์ใบตัวเอง | `scope=own` |
| หัวหน้างาน | **Maker** (ยื่นแทน) · **Checker** (slot 1) | ทุกอย่างของลูกทีม + ยื่นแทน + อนุมัติ/อนุมัติบางส่วน + **ยืนยันเวลาจริง** | `scope=team` |
| ฝ่ายบุคคล | **Approver** (slot 2) · **Checker** (ทวนใบติดธง) | ดูทุกใบ · อนุมัติ · ยืนยันเวลาจริง · สรุปงวด · ตัดสินใบที่ติดธง `needs_review` | `scope=company` |
| ผู้บริหารต้นสังกัด | **Approver ชั้น 3** | อนุมัติ **เฉพาะใบที่ `over_cap = true`** | ตามที่ DOA resolve |
| ระบบ | **System** | resolve ค่า · คำนวณชั่วโมง/ธง · ออกเลข · render PDF · ยิง event · scheduler | — |
| Payroll · ESS · Roster | — | **อ่านผ่าน §0.13 เท่านั้น — ไม่มี write endpoint** | ตาม §0.13.5 |

**SoD (บังคับ · `05_RULES BR-24`):** `requested_by ≠ ผู้ถือ slot ใด ๆ` · เมื่อชนกัน DOA ต้อง escalate ขึ้นสายบังคับบัญชาเหนือขึ้นไป (OQ-DOA-02 · OQ-DOA-04) — **feature ห้ามแก้เอง**

## §0.5 Dependencies

### Upstream (feature นี้ต้องพึ่ง)

| ระบบ | สถานะ | อ่านอะไร | endpoint / สัญญา | บังคับ? |
|---|---|---|---|---|
| **HR Configuration** | ✅ W1 | `ot_rate` (`rate_type` · `multiplier` · `base` · `cap_hours_week` · `payroll_code`) · `holiday_calendar` · `shift_pattern` · `period_rule` + `pay_period` | `GET /api/v1/hr-config/resolve?date=<work_date>&company_id=&group=` (§0.13.2 ของแพ็กนั้น) | **ใช่ — ไม่มีค่าก็ออกใบไม่ได้** |
| **Attendance** | ✅ W1 | `day`: **`outside_shift_hours`** · `day_status` · `day_result[]` · `shift` · `holiday` · `period_code`/`period_status` · `version_id` · `period`: `total_outside_shift_hours` · `unconfirmed_days` | `GET /api/v1/attendance/resolve` · `GET /api/v1/attendance/periods/resolve` | **ใช่ — ไม่มีก็ยืนยันเวลาจริงไม่ได้** |
| **Leave** | ✅ W2 | วันลาที่อนุมัติแล้ว (`leave_no` · `leave_type_snapshot` · `day_part` · `leave_status`) | `GET /api/v1/leave/resolve?date=&employee_id=` (§0.13.2 ของแพ็กนั้น) | **ใช่ — ใช้กันทับวันลา (BR-19)** |
| **DOA Engine** | ✅ | สายอนุมัติ + slot ที่ต้องเลือกคน | `GET /doa/resolve` (**action id** = `ot_approve_within_cap` / `ot_approve_over_cap`) | **ใช่ (LOCK-DOA)** |
| **Document Configuration** | ✅ | เลขรัน + policy สำเนา | `ENG-DOC-NUM.next('OT', company_ctx)` · `ENG-DOC-STORE.store()` | **ใช่** |
| **ENG-NOTIFY** | ✅ | — (ยิงออก) | `ENG-NOTIFY.emit(event_id, {ref, vars})` | ใช่ |
| **ENG-CSQ** | ✅ | — (ยิงออก) | envelope `CSQ-HROT` (EC + FC) | ใช่ |
| **Employee Master · Organization · Policy Center** | ✅ | คน · บริษัท · สิทธิ์/masking | runtime | ใช่ |

### Downstream (feature ที่พึ่ง feature นี้) — **อ่าน §0.13**

| ระบบ | สถานะ | อ่านอะไร | trigger |
|---|---|---|---|
| **Payroll** | ⏳ W4 | มุมมอง `day` + `period` — ชั่วโมงที่ `time_confirmed` แยกตาม `rate_type` พร้อม `multiplier` · `payroll_code` · `config_version_ids` · **ไม่มีเงิน** | ใบเข้าสถานะ `time_confirmed` (BR-17) |
| **ESS Portal** | ⏳ W6 | ใบของฉัน + ชั่วโมงสะสมของฉัน | ผู้ใช้เปิดดู (เรียกหน้าจอของ feature นี้ · OQ-HR-04) |
| **Shift & Roster** | ⏳ W2 lane C | วัน/ช่วงที่มีใบ OT `approved` ขึ้นไป | Module Linkage (soft ref · display-only) |
| **ชั้นรายงาน 7C** | ✅ (ENG-CSQ) | 5 event `ot.*` ท่อ EC + FC | ตาม §0.16.2 |

### External
ไม่มีการเชื่อมต่อระบบภายนอกองค์กรในแพ็กนี้

## §0.6 Stack & Architecture

| ชั้น | เทคโนโลยี / รูปแบบ | หมายเหตุ |
|---|---|---|
| UI | SPA · hash routing · **1 feature = 1 เมนู 4 แท็บ** (#104) | `#/ot/list` `#/ot/cap` `#/ot/confirm` `#/ot/period` |
| Layout | **Pattern Q** (ตัวสร้างหน้าจอ v9) — list · wizard 5 ขั้น · view tabs 4 · PDF+ลายเซ็น · DOA modals · line editor B2 v2 | ยืนยัน 6 surface ที่ `COVERAGE_R1 §3` |
| API | REST · `/api/v1/ot/*` · JSON | `02_API` |
| Logic | Function (scope-local) + Engine (reusable) แยกตาม logic-placement-matrix | `03_LOGIC` |
| DB | PostgreSQL · append-only history · **ไม่มี hard delete** | `04_DB` |
| Async | Event bus (ENG-NOTIFY · ENG-CSQ) + scheduler รายวันของ feature | `03_LOGIC §3.1 sweepPendingConfirm` |
| PDF | เอกสาร A4 1 หน้า จาก `PDFDOC/template.html` — engine ใดก็ได้ที่ honor `@page` + Sarabun | **`PRINT_SPEC.md`** |

**หลักสถาปัตยกรรมที่บังคับในแพ็กนี้:**
1. **ไม่มีค่านโยบายใดอยู่ในโค้ดของ feature** — ทุกค่ามาจาก `resolve(date, company)` (P-8)
2. **ไม่มีสายอนุมัติในโค้ดของ feature** — มาจาก `GET /doa/resolve` (LOCK-DOA)
3. **ไม่มีตัวเลขเงินในทุกชั้น** — UI · API · DB · PDF · event (LOCK-MONEY)
4. **ไม่มี write path ไปยัง upstream** — Attendance · Leave · HR Config อ่านอย่างเดียว (AT-5 · LV-5 · C-4)

## §0.7 Multi-Tenant & Security Context

| หัวข้อ | ค่า |
|---|---|
| Tenant isolation | ทุก query กรองด้วย `tenant_id` + `company_id` |
| Company scope | `company_id` บังคับส่งทุกครั้งที่ resolve (C-1 · AT-1 · LV-1) · **ยังไม่มี UI สลับบริษัท** (OQ-HR-05) |
| Security Preset | **P6 — HR / PII Sensitive (15 controls · Must 9)** — ดู `05_RULES §5.7` |
| Permission model | ABAC — `scope ∈ {own, team, company}` มาจาก login + Policy Center · **ไม่มี persona switch ในหน้าจอ** (#105) |
| Audit | ทุก mutation เขียน `T_ot_history` (append-only) + `T_ot_approval_trace` |

### §0.7.1 Data Classification Summary ⭐

| ระดับ | มีในแพ็กนี้ไหม | ตัวอย่าง field |
|---|:---:|---|
| Public | ❌ | — |
| Internal | ✅ | `ot_no` · `work_date` · `time_from`/`time_to` · `rate_type` · `multiplier` · `payroll_code` · `status` · `over_cap` · `config_version_ids` |
| **Confidential** | ✅ **(ระดับสูงสุดที่ feature นี้แตะ)** | `reason` · `work_done` · `employee_snapshot` · `hours_*` รายคน · `attachment.file_name` · `reject_reason`/`withdraw_reason`/`partial_reason` |
| Restricted | ❌ **ไม่มี** | — **feature นี้ไม่มีตัวเลขเงินและไม่มีข้อมูลค่าจ้าง** (LOCK-MONEY) จึงไม่แตะระดับนี้ |

> **ผลของการไม่มี Restricted:** ไม่ต้อง wire Restricted Resources · แต่ **ทุก field ระดับ Confidential ต้องมี masking rule ครบ** (`04_DB §4.6` · `05_RULES §5.7`)

## §0.8 Open Questions

**31 ข้อ ยกมาจาก BRD §15 ครบ** — รายละเอียดเต็มพร้อมค่าที่ใช้ไปก่อนอยู่ที่ `07_LOCKED_DECISIONS §7.3`
ข้อที่ **บล็อกการพัฒนาบางส่วน** (8 ข้อ · BRD §14.4 W-01…W-09):

| # | ประเด็น | บล็อกอะไร | เจ้าภาพ |
|---|---|---|---|
| **OQ-STD-OT5** ⭐ | เพดาน OT รายวัน/รายเดือน — HR Config มีแต่ `ot_rate.cap_hours_week` · `T_hr_legal_minimum` ไม่มีคีย์ `ot_cap.*` | การบังคับเพดานรายวัน/รายเดือน — **รอบนี้แสดง "ยังไม่มีค่าให้อ่าน" ห้ามเดา** | Strike + BA HR Configuration |
| **OQ-OT-16** ⭐ | หน่วยขั้นต่ำ/การปัดเศษของชั่วโมง (`ot_rate` ไม่มีฟิลด์) | การปัดเศษ — รอบนี้ใช้ค่าดิบ · **ห้ามใส่ตัวเลขนาทีในโค้ด** · **เคาะพร้อม OQ-STD-OT5 เป็นชุดเดียว** | Strike + BA HR Configuration |
| OQ-STD-OT6 | ค่าความคลาดเคลื่อนที่ยอมได้ระหว่าง `hours_requested` กับ `outside_shift_hours` | Rule Management (Phase 3) | Strike |
| OQ-STD-OT7 | รูปแบบความยินยอมของลูกจ้างตามกฎหมายแรงงาน | รูปแบบหลักฐาน (ช่อง `consent_ack_*` ต้องมีตั้งแต่ Phase 1) | Strike / ฝ่ายกฎหมาย |
| OQ-OT-12 · OQ-DOA-01 · OQ-DOA-02 | `role-*` id จริงของ 3 slot + กติกา escalate เมื่อชน SoD | การตั้งค่า DOA matrix จริง | Architect / Policy Center |
| **OQ-DOA-03** ⭐ | DOA รองรับมิติจุดตัดที่ไม่ใช่เงินหรือไม่ | รูปแบบการตั้ง matrix — **ไม่ว่าทางไหนก็ห้ามใส่ตัวเลขชั่วโมงเป็นขอบของ set** | Architect |
| OQ-NTF-01 | ชื่อ event ชนกับ catalog เดิมหรือไม่ | การ register event | Architect / เจ้าของ ENG-NOTIFY |
| OQ-OT-13 | `doc_type = OT` ชนกับ registry เดิมหรือไม่ | การ register doc_type | Architect / เจ้าของทะเบียนเลข |

### §0.8.1 Phase 2.5 Probing — ผลที่ใช้ default (Lane Mode · no-ask)

| Probe | ประเด็น | คำตอบที่ใช้ | ที่มา | tag |
|---|---|---|---|---|
| PR-1 | Concurrent update ของใบเดียวกัน | **optimistic lock ด้วย `row_version` → 409 `ERR_OT_STALE`** | conservative default | `[AI-DEFAULT]` |
| PR-2 | Race ของการอนุมัติสองคนพร้อมกัน | ล็อกแถวใบตอน transition + ตรวจ `current_step` ซ้ำ → 409 | BRD §10.2 CA-01 | ✅ จาก BRD |
| PR-3 | Idempotency ของ mutation | **`Idempotency-Key` บังคับที่ submit · approve · confirm · withdraw** | conservative default | `[AI-DEFAULT]` |
| PR-4 | Upstream ล่ม | **บล็อก ห้าม fallback ห้ามใช้ cache ข้ามวัน** → 503 `ERR_UPSTREAM_UNAVAILABLE` | BRD §10.2 DI-01/DI-02 · BR-04 | ✅ จาก BRD |
| PR-5 | Partial failure ตอนแตกใบ proxy | **ทั้งชุดเป็น transaction เดียว — ล้มทั้งชุด** | conservative default | `[AI-DEFAULT]` |
| PR-6 | Pagination ของ read model | `page_size` default 100 · สูงสุด 500 | convention กลาง | `[AI-DEFAULT]` |
| PR-7 | การกดส่งซ้ำจากหน้าจอ | ปุ่ม disable + idempotency key (PR-3) | BRD VR-21 | ✅ จาก BRD |
| PR-8 | Timezone | เขตเวลาเดียวของผู้เช่า · เก็บ `timestamptz` | conservative default | `[AI-DEFAULT]` · LD-OT-09 |
| PR-9 | `needs_review` ค้างถึงวันปิดงวด | **ต้องเคลียร์ก่อนปิดงวด** (ค่าที่ปลอดภัยกว่า) | BRD ST-E04 | `[AI-DEFAULT]` · **OQ-FRD-01** |

> ทุก `[AI-DEFAULT]` ถูก tag ไว้ใน `05_RULES` และยกขึ้น `07_LOCKED §7.3` ให้ BA ยืนยันตอน review

## §0.9 Glossary

ดู BRD §Appendix B — เพิ่มคำที่ใช้เฉพาะในแพ็กนี้:

| คำ | ความหมาย |
|---|---|
| `over_cap` | ธง bool ที่คำนวณจาก `weeklyAccumulatedHours > cap_snapshot_hours_week` — **ตัวเลือก action id ของ DOA** |
| `cap_snapshot_hours_week` | สำเนาเพดานที่ใช้ตัดสิน ณ วินาที submit — หลักฐานว่าตัดสินด้วย version ไหน |
| `config_version_ids` | `{ ot_rate, holiday, shift, period, attendance_day[] }` |
| `time_confirmed` | สถานะที่ผูกชั่วโมงกับเวลาจริงแล้ว — **สถานะเดียวที่ §0.13 คืนออกไป** |
| `outside_shift_hours` | ชั่วโมงนอกกรอบกะจาก Attendance — **ข้อมูลดิบ ยังไม่ใช่ OT ที่อนุมัติ** |
| `needs_review` | ธง "ต้องทวน" จาก event `attendance.day_adjusted` |
| `reversal_of` / `supersedes` | การชี้กลับของ event ที่กลับรายการ / แทนที่ค่าเดิม — **ไม่ลบของเดิม** |

## §0.10 Pack Navigation

| ต้องการรู้อะไร | ไปที่ |
|---|---|
| หน้าจอมีอะไร · route อะไร · pattern ไหน | `01_UI` |
| endpoint · request/response · error | `02_API` |
| ตรรกะธุรกิจ · การเลือกสาย DOA · การคำนวณเพดาน | **`03_LOGIC`** |
| ตาราง · คอลัมน์ · index · classification | `04_DB` |
| กฎธุรกิจ · state machine · validation · error catalog · security | `05_RULES` |
| เกณฑ์รับ · ชุดทดสอบ · DoD | `06_TESTS` |
| LOCK · Locked Decision · Open Question | `07_LOCKED_DECISIONS` |
| **วิธีพิมพ์ใบ OT · field mapping ของเอกสาร** | **`PRINT_SPEC.md`** |
| **สิ่งที่ feature อื่นอ่านได้จากที่นี่** | **`00_OVERVIEW §0.13`** |
| ตารางอ้างอิงไขว้ · สถิติแพ็ก · ผล Phase 3.5 | `INDEX` |

## §0.11 Scope Lock (pointer)

**LOCK ทั้ง 11 รายการอยู่ที่ `07_LOCKED_DECISIONS §7.0` (IMMUTABLE)** — นำเข้าครบจาก BRD §3.4
**ตรวจแล้ว: ไม่มี spec ใดในแพ็กนี้ขัด LOCK** (Phase 3.5 Section L)

---

## §0.12 Coverage Manifest ⭐ (R13 — กัน requirement หล่น BRD→FRD · **มีคอลัมน์ FN-XX ตาม Lane Mode v2**)

### §0.12.0 Function Ledger — **65/65 FN** → ที่อยู่ในแพ็ก

| FN | ความสามารถ (ย่อ) | UI | API | LOGIC | RULES | TESTS |
|---|---|---|---|---|---|---|
| FN-01 | ตัวช่วยสร้าง 5 ขั้น ย้อนกลับได้ | `§1.2 P-01 W1–W5` | API-01 · API-02 | `createDraft` · `updateDraft` | — | AT-01 |
| FN-02 | เลือกผู้ขอจาก Employee Master | `§1.2 P-01 W1` | API-03 | `resolveEmployeeScope` | BR-24 | AT-02 |
| FN-03 | เหตุผล + งานที่ทำ เป็นช่องบังคับ | `§1.2 P-01 W3` | API-02 · API-06 | `validateHeader` | VR-02 · VR-03 | AT-03 |
| FN-04 | โหมด advance/retro + ธง | `§1.2 P-01 W1` | API-02 | `inferRequestMode` | BR-15 | AT-04 |
| FN-05 | ช่วงคร่อมเที่ยงคืน + ธง overnight | `§1.2 P-01 W2` | API-04 | `detectOvernight` · `computeLineHours` | BR-06 · BR-20 | AT-05 |
| FN-06 | หลายบรรทัดต่อใบ + ยอดรวม | `§1.2 P-01 W2` | API-04 | `addLine` · `updateLine` · `removeLine` | BR-21 | AT-06 |
| FN-07 | กันช่วงเวลาผิดตั้งแต่กรอก | `§1.2 P-01 W2` | API-04 | `validateLines` | BR-20 · VR-04 · VR-05 | AT-07 |
| FN-08 | บันทึกร่างโดยไม่กินเลข | `§1.2 P-01 W*` | API-01 · API-02 | `createDraft` · `discardDraft` | BR-13 · BR-14 | AT-08 |
| FN-09 | บล็อกเมื่อ `no_shift` / ตัดสิน day_type ไม่ได้ | `§1.2 P-01 W2` | API-04 | `resolveDayType` | BR-20 · VR-07 | AT-09 |
| FN-10 | resolve อัตรา/ตัวคูณ/เพดาน ณ `work_date` | `§1.2 P-01 W2 · W4` · `P-02` | API-04 · API-05 | `resolveOtRate` · `resolveCap` · **ENG-HRCFG-RESOLVE** | BR-01 · BR-02 | AT-10 · IA-03 |
| FN-11 | เก็บ `config_version_ids` ทั้งก้อน | `§1.2 P-01 V-detail` | API-06 | `snapshotConfigVersions` | BR-03 | AT-11 |
| FN-12 | ใบเก่าแสดง/พิมพ์ได้เมื่อค่าถูก inactive | `§1.2 P-01 V-detail · V-pdf` | API-07 | `renderOtPdf` | BR-23 | AT-12 |
| FN-13 | day_type จากปฏิทิน+กะ ไม่คำนวณเอง | `§1.2 P-01 W2` | API-04 | `resolveDayType` · `mapRateType` | BR-01 · BR-06 | AT-13 |
| FN-14 | เตือนใกล้ถึงเพดาน | `§1.2 P-01 W4` · `P-02` | API-05 | `computeCapWarning` · **ENG-OTCAP** | BR-09 | AT-14 |
| FN-15 | ธง `over_cap` + บอกว่าสายจะยาวขึ้น | `§1.2 P-01 W4 · W5` | API-05 · API-06 | `computeOverCap` · `selectApprovalAction` | BR-09 | AT-15 |
| FN-16 | บล็อกเมื่อทับวันลาที่อนุมัติแล้ว | `§1.2 P-01 W2 · W4` | API-04 · API-06 | `checkLeaveConflict` · **ENG-LEAVE-RESOLVE** | BR-19 · VR-08 | AT-16 |
| FN-17 | แสดง `outside_shift_hours` เทียบที่ขอ | `§1.2 P-01 W4 · V-detail` · `P-03` | API-04 · API-14 | `fetchAttendanceDay` · `computeVariance` | BR-07 | AT-17 |
| FN-18 | ห้ามใช้ชั่วโมงนอกกะเป็น OT โดยตรง | — (negative) | API-20 | `buildDayReadModel` | BR-07 · BR-17 | **IA-01** |
| FN-19 | บล็อกเมื่อขอเกินเวลาจริงจนกว่าจะ ack | `§1.2 P-01 W4` · modal | API-06 · API-15 | `classifyVariance` · `acknowledgeVariance` | BR-16 · VR-09 | AT-18 |
| FN-20 | ธงเมื่อขอน้อยกว่าเวลาจริง | `§1.2 P-01 W4` | API-04 | `classifyVariance` | BR-16 · VR-10 | AT-19 |
| FN-21 | ยืนยันเวลาจริง → `time_confirmed` | `§1.2 P-03` · `P-01 V-detail` | API-13 | `confirmActualHours` | BR-17 · VR-19 | AT-20 |
| FN-22 | ใบ retro เข้าสถานะยืนยันได้ทันที | `§1.2 P-03` | API-13 | `autoConfirmRetro` | BR-17 | AT-21 |
| FN-23 | "ยังยืนยันเวลาจริงไม่ได้" เมื่อไม่มีข้อมูล | `§1.2 P-01 W4` · `P-03` | API-14 | `fetchAttendanceDay` | BR-08 | AT-22 |
| FN-24 | แสดงเหตุ exception + ลิงก์ต้นทาง | `§1.2 P-01 W4` · `P-03` | API-14 | `fetchAttendanceDay` | BR-08 | AT-23 |
| FN-25 | สายอนุมัติจาก `GET /doa/resolve` เท่านั้น | `§1.2 P-01 W5` | API-06 | `resolveApprovalChain` · **ENG-DOA-01** | BR-10 | AT-24 · **IA-04** |
| FN-26 | ทุก slot เลือก "คน" ในตำแหน่ง | `§1.2 P-01 W5` | API-06 | `resolveApprovalChain` | BR-10 · VR-14 | AT-25 |
| FN-27 | ใบในเพดาน = 2 ขั้น + SoD | `§1.2 P-01 W5 · V-sign` | API-06 · API-08 | `selectApprovalAction` | BR-24 | AT-26 |
| FN-28 | ใบเกินเพดาน = 3 ขั้น เลือกด้วยธง | `§1.2 P-01 W5 · V-sign` | API-06 · API-08 | `selectApprovalAction` · `computeOverCap` | BR-09 · BR-10 | AT-27 · **IA-05** |
| FN-29 | ปุ่มตัดสินเฉพาะเจ้าของ slot ปัจจุบัน | `§1.2 P-01 V-detail` | API-08 | `approveStep` | BR-10 · §5.3 | AT-28 |
| FN-30 | ไม่อนุมัติ = บังคับเหตุผล + เลขคงอยู่ | `§1.2 P-01 modal` | API-10 | `rejectRequest` | BR-12 · BR-13 · VR-15 | AT-29 |
| FN-31 | อนุมัติบางส่วน + เหตุผล + 2 ตัวเลขบนใบ | `§1.2 P-01 modal · V-pdf` | API-09 | `approvePartial` | BR-21 · VR-16 | AT-30 |
| FN-32 | แท็บลายเซ็นเห็นครบทุกชั้น | `§1.2 P-01 V-sign` | API-07 | `buildSignatureSlots` | BR-10 | AT-31 |
| FN-33 | แก้แล้วส่งใหม่ = re-resolve · เลขเดิม | `§1.2 P-01 W* · V-detail` | API-16 | `resubmitRequest` | BR-11 · BR-13 | AT-32 |
| FN-34 | ออกเลข `OT-YYYY-NNNN` ตอน submit | `§1.2 P-01 W5` | API-06 | `issueDocNumber` · **ENG-DOC-NUM** | BR-13 | AT-33 |
| FN-35 | เลขที่อ่านอย่างเดียวทุกจุด | ทุกหน้า | — | — | BR-13 · VR-20 | AT-34 |
| FN-36 | แท็บ PDF ใช้ template เดียวกับที่พิมพ์จริง | `§1.2 P-01 V-pdf` | API-07 | `renderOtPdf` | — | AT-35 · **PRINT_SPEC** |
| FN-37 | ช่องลงนาม 3/4 ช่องตามสายจริง | `§1.2 P-01 V-pdf` | API-07 | `buildSignatureSlots` | BR-10 | AT-36 · **PRINT_SPEC §P.2** |
| FN-38 | เก็บสำเนา PDF ณ เวลาอนุมัติครบสาย | — (system) | API-08 | `storeApprovedCopy` · **ENG-DOC-STORE** | BR-03 | AT-37 |
| FN-39 | ยกเลิกใบที่ยังรออนุมัติ | `§1.2 P-01 modal` | API-11 | `cancelRequest` | BR-14 | AT-38 |
| FN-40 | ปฏิเสธทุกการเปลี่ยนในงวดที่ปิด | ทุกหน้า · `P-04` | ทุก mutation | `checkPeriodOpen` | BR-15 · VR-13 | AT-39 · **IA-06** |
| FN-41 | ขอถอน = บังคับเหตุผล + ผ่านสายอีกครั้ง | `§1.2 P-01 modal` | API-12 | `requestWithdrawal` · `finalizeWithdrawal` | BR-12 · VR-17 | AT-40 |
| FN-42 | การถอนเกิด reversal ที่ชี้ของเดิม | `§1.2 P-01 V-history` · `P-04` | API-12 · API-20 | `finalizeWithdrawal` · `emitImpactEvent` | BR-27 | AT-41 |
| FN-43 | ธง `needs_review` เมื่อเวลาเข้างานถูกแก้ | `§1.2 P-01 list · V-detail` · `P-03` | API-17 (event in) | `onAttendanceDayAdjusted` · `resolveNeedsReview` | BR-22 | AT-42 |
| FN-44 | ยื่นแทนหลายคน → 1 ใบต่อคน + รับทราบ | `§1.2 P-01 W1 · W5` | API-18 · API-19 | `splitProxyRequests` · `recordConsent` | BR-26 · BR-28 · VR-18 | AT-43 |
| FN-45 | เผยแพร่เฉพาะใบ `time_confirmed` | — (read model) | API-20 · API-21 | `buildDayReadModel` | BR-17 | **IA-01** |
| FN-46 | ส่งชั่วโมง + บริบท โดยไม่มีเงิน | — (read model) | API-20 · API-21 | `buildDayReadModel` · `buildPeriodSummary` | BR-18 | **IA-07** |
| FN-47 | สรุปงวดต่อคนแยกตาม `rate_type` | `§1.2 P-04` | API-21 | `buildPeriodSummary` | BR-15 · BR-17 | AT-44 |
| FN-48 | ตรึงยอดเมื่องวดถูกปิด | `§1.2 P-04` | API-21 | `freezePeriodSummary` · **ENG-PERIOD-FREEZE** | BR-15 | AT-45 |
| FN-49 | จุดเชื่อมให้ Shift & Roster อ่าน | `§1.2 P-04` | API-22 | `buildLinkageStatus` | BR-05 | AT-46 |
| FN-50 | แจ้งเตือน submit · decision · cap | — (event out) | — | `emitNotification` · **ENG-NOTIFY** | §0.16.1 | AT-47 |
| FN-51 | แจ้งเตือนค้างยืนยัน · ธงต้องทวน | — (event out) | — | `sweepPendingConfirm` · `emitNotification` | §0.16.1 | AT-48 |
| FN-52 | ไม่มี write path ไปยัง upstream | — (negative) | — | — | BR-05 · BR-25 | **IA-02** |
| FN-53 | ไม่มีตัวเลขเงินที่ใดเลย | — (negative) | — | `assertNoMoneyField` (guard) | BR-18 | **IA-07** |
| FN-54 | ไม่มีการชดเชย OT เป็นวันหยุด | — (negative) | — | — | BR-05 | **IA-08** |
| FN-55 | ไม่มีค่ากะ/ค่าทำงานกลางคืน | — (negative) | — | — | BR-18 | **IA-08** |
| FN-56 | ไม่มีการคุมงบ/พยากรณ์ | — (negative) | — | — | BR-18 | **IA-08** |
| FN-57 | ไม่มีตารางจัดกะ/เวร | — (negative) | — | — | BR-05 | **IA-08** |
| FN-58 | เพดานรายวัน/รายเดือน = "ยังไม่มีค่าให้อ่าน" | `§1.2 P-01 W4` · `P-02` | API-05 | `resolveCap` | BR-09 | AT-49 |
| FN-59 | ประวัติ append-only ไม่มีปุ่มลบ | `§1.2 P-01 V-history` | API-07 | `appendHistory` | BR-14 | AT-50 · **IA-09** |
| FN-60 | สิทธิ์จาก login · ไม่มี persona switch | ทุกหน้า | ทุก API | `resolveEmployeeScope` | §5.3 | AT-51 |
| FN-61 | บล็อกช่วงเวลาที่ทับใบ OT ใบอื่น | `§1.2 P-01 W2 · W4` | API-04 · API-06 | `checkOtOverlap` · **ENG-OVERLAP** | BR-29 · VR-06 | AT-52 |
| FN-62 | ใช้ค่าดิบเมื่อยังไม่มีกติกาการปัดเศษ | `§1.2 P-01 W2` | API-04 | `computeLineHours` | BR-30 | AT-53 · **IA-10** |
| FN-63 | ธง "ยื่นเกินกำหนด" | `§1.2 P-01 W1 · W5 · list` | API-06 | `checkRetroCutoff` | BR-15 | AT-54 |
| FN-64 | เอกสารแนบใน landing + แนบเพิ่มหลังยื่น | `§1.2 P-01 W3 · V-detail` | API-23 · API-24 | `attachDocument` · `archiveAttachment` | BR-14 | AT-55 |
| FN-65 | รหัสเหตุผลแบบไม่บังคับ | `§1.2 P-01 W3` | API-02 | `validateHeader` | BR-01 | AT-56 |

**65/65 FN มีที่ลงครบ — ไม่มีแถวที่ "อยู่ที่" ว่าง**

### §0.12.1 Stories (BRD §7) — 65/65

| BRD Ref | Story | อยู่ที่ |
|---|---|---|
| §7 ST-01…ST-09 | ตัวช่วย 5 ขั้น · ผู้ขอ · เหตุผล/งานที่ทำ · โหมด · ข้ามคืน · หลายบรรทัด · ช่วงเวลาผิด · ร่าง · บล็อก no_shift | `01_UI §1.2 P-01 (W1–W3)` + `02_API API-01…API-04` + `03_LOGIC §3.1` + `06_TESTS AT-01…AT-09` |
| §7 ST-10…ST-16 | resolve อัตรา/เพดาน · version ids · ใบเก่าพิมพ์ได้ · day_type · เตือนเพดาน · ธง over_cap · ทับวันลา | `01_UI §1.2 P-01 (W2·W4) · P-02` + `02_API API-04 · API-05` + `03_LOGIC §3.1 · §3.2 ENG-OTCAP` + `06_TESTS AT-10…AT-16` |
| §7 ST-17…ST-24 | เทียบเวลาจริง · ห้ามใช้ตรง · บล็อก/ack ส่วนต่าง · ธงน้อยกว่า · ยืนยันเวลาจริง · retro ทันที · ไม่มีข้อมูล · exception | `01_UI §1.2 P-01 (W4) · P-03` + `02_API API-13 · API-14 · API-15` + `03_LOGIC §3.1 · §3.2 ENG-VARIANCE` + `06_TESTS AT-17…AT-23 · IA-01` |
| §7 ST-25…ST-33 | DOA resolve · slot คน · 2 ขั้น · 3 ขั้น · ปุ่มตามคิว · reject · partial · แท็บลายเซ็น · resubmit | `01_UI §1.2 P-01 (W5 · V-sign)` + `02_API API-06 · API-08…API-10 · API-16` + `03_LOGIC §3.1 · §3.2 ENG-DOA-01` + `06_TESTS AT-24…AT-32 · IA-04 · IA-05` |
| §7 ST-34…ST-38 | ออกเลข · เลข read-only · PDF template · ช่องลงนาม · สำเนา | `01_UI §1.2 P-01 (V-pdf)` + `02_API API-06 · API-07` + `03_LOGIC §3.1` + **`PRINT_SPEC`** + `06_TESTS AT-33…AT-37` |
| §7 ST-39…ST-44 | ยกเลิก · งวดปิด · ถอน · reversal · needs_review · proxy+consent | `01_UI §1.2 P-01 (modal) · P-03` + `02_API API-11 · API-12 · API-17…API-19` + `03_LOGIC §3.1` + `06_TESTS AT-38…AT-43 · IA-06` |
| §7 ST-45…ST-49 | เผยแพร่เฉพาะ confirmed · ไม่มีเงิน · สรุปงวด · ตรึงยอด · linkage | **`00_OVERVIEW §0.13`** + `02_API API-20…API-22` + `03_LOGIC §3.1 · §3.2 ENG-PERIOD-FREEZE` + `06_TESTS AT-44…AT-46 · IA-01 · IA-07` |
| §7 ST-50…ST-51 | 7 event NTF + scheduler | **`00_OVERVIEW §0.16.1`** + `03_LOGIC §3.1 emitNotification · sweepPendingConfirm` + `06_TESTS AT-47 · AT-48` |
| §7 ST-52…ST-57 | negative assertion 6 ข้อ (ไม่มี write-back · ไม่มีเงิน · ไม่มี TOIL · ไม่มีค่ากะ · ไม่มีคุมงบ · ไม่มีจัดกะ) | `05_RULES §5.7 · §5.8` + `06_TESTS **IA-02 · IA-07 · IA-08**` |
| §7 ST-58…ST-60 | เพดานรายวัน/เดือนว่าง · history append-only · สิทธิ์จาก login | `01_UI §1.2 P-01 (W4 · V-history) · P-02` + `05_RULES §5.3` + `06_TESTS AT-49…AT-51 · IA-09` |
| §7 ST-61…ST-65 | ทับใบอื่น · ค่าดิบ · ธงยื่นช้า · เอกสารแนบ · รหัสเหตุผล | `01_UI §1.2 P-01 (W1–W3)` + `02_API API-04 · API-23 · API-24` + `03_LOGIC §3.2 ENG-OVERLAP` + `06_TESTS AT-52…AT-56 · IA-10` |

### §0.12.2 Business Rules (BRD §9) — 30/30

| BRD Ref | Rule (ย่อ) | อยู่ที่ | Test |
|---|---|---|---|
| BR-01 | resolve ค่าทุกตัว ณ `work_date` · ห้าม hardcode | `05_RULES BR-01` · `03_LOGIC ENG-HRCFG-RESOLVE` | AT-10 · **IA-03** |
| BR-02 | ส่ง `date` + `company_id` เสมอ | `05_RULES BR-02` · `02_API §2.3` | AT-10 |
| BR-03 | เก็บ `config_version_ids` ตั้งแต่ submit | `05_RULES BR-03` · `04_DB §4.2` | AT-11 |
| BR-04 | ห้าม cache ข้ามวัน · ล้างตาม 7 event | `05_RULES BR-04` · `03_LOGIC invalidateResolveCache` | AT-57 |
| BR-05 | ห้าม CRUD/เขียนกลับ upstream | `05_RULES BR-05` · `§5.7` | **IA-02** |
| BR-06 | ห้ามคำนวณ day_type/ชั่วโมงในกะ/วันลาเอง | `05_RULES BR-06` | AT-13 |
| BR-07 | `outside_shift_hours` = ข้อมูลดิบ | `05_RULES BR-07` · **§0.13.5** | **IA-01** |
| BR-08 | ตรวจ `day_status` ก่อนใช้ตัวเลข | `05_RULES BR-08` · `03_LOGIC fetchAttendanceDay` | AT-22 · AT-23 |
| BR-09 | เพดาน → `over_cap` → สายยาวขึ้น · ห้าม hardcode ทั้งโค้ดและ matrix | `05_RULES BR-09` · `03_LOGIC §3.1 · ENG-OTCAP` | AT-15 · AT-27 · **IA-05** |
| BR-10 | สายจาก DOA เท่านั้น + freeze | `05_RULES BR-10` · `03_LOGIC ENG-DOA-01` | AT-24 · **IA-04** |
| BR-11 | resubmit = cancel เดิม + re-resolve | `05_RULES BR-11` | AT-32 |
| BR-12 | reject/withdraw/partial บังคับเหตุผล | `05_RULES BR-12` · `§5.4` | AT-29 · AT-30 · AT-40 |
| BR-13 | เลขออกตอน submit · immutable · ไม่ reuse | `05_RULES BR-13` · `03_LOGIC ENG-DOC-NUM` | AT-33 · AT-34 |
| BR-14 | history append-only · ไม่มี hard delete | `05_RULES BR-14` · `04_DB §4.2` | AT-50 · **IA-09** |
| BR-15 | งวดปิด = ปฏิเสธทุกการเปลี่ยน · ตรวจซ้ำตอน commit | `05_RULES BR-15` · `03_LOGIC checkPeriodOpen` | AT-39 · **IA-06** |
| BR-16 | ขอเกินเวลาจริง = บล็อกจนแก้/ack · ขอน้อย = ธง | `05_RULES BR-16` · `03_LOGIC ENG-VARIANCE` | AT-18 · AT-19 |
| BR-17 | เฉพาะ `time_confirmed` เท่านั้นที่เผยแพร่ | `05_RULES BR-17` · **§0.13** | **IA-01** |
| BR-18 | ห้ามมีตัวเลขเงินทุกชั้น | `05_RULES BR-18` · `04_DB §4.6` | **IA-07** |
| BR-19 | ทับวันลาที่อนุมัติแล้ว = บล็อก | `05_RULES BR-19` · `03_LOGIC checkLeaveConflict` | AT-16 |
| BR-20 | `no_shift`/ช่วงเวลาผิด = บล็อก | `05_RULES BR-20` | AT-07 · AT-09 |
| BR-21 | partial ≤ requested และ ≤ outside_shift_hours | `05_RULES BR-21` | AT-30 |
| BR-22 | `attendance.day_adjusted` → `needs_review` | `05_RULES BR-22` · `03_LOGIC onAttendanceDayAdjusted` | AT-42 |
| BR-23 | ค่า inactive เลือกใหม่ไม่ได้ · ใบเก่ายังพิมพ์ได้ | `05_RULES BR-23` | AT-12 |
| BR-24 | SoD — ผู้ขอเซ็นใบตัวเองไม่ได้ | `05_RULES BR-24` · `§5.3` | AT-26 |
| BR-25 | ลงทะเบียน where-used 3 ต้นทาง | `05_RULES BR-25` · `03_LOGIC registerWhereUsed` | AT-58 |
| BR-26 | 1 ใบ = 1 คน | `05_RULES BR-26` · `03_LOGIC splitProxyRequests` | AT-43 |
| BR-27 | ถอน = event ใหม่ที่ชี้ของเดิม | `05_RULES BR-27` | AT-41 |
| BR-28 | proxy ต้องมี consent ก่อน submit | `05_RULES BR-28` | AT-43 |
| BR-29 | ห้ามทับซ้อนกับใบ OT อื่นของคนเดียวกัน | `05_RULES BR-29` · `03_LOGIC ENG-OVERLAP` | AT-52 |
| BR-30 | การปัดเศษต้องอ่านจากต้นทาง · รอบนี้ใช้ค่าดิบ | `05_RULES BR-30` | AT-53 · **IA-10** |

### §0.12.3 Edge Cases (BRD §10) — ☑ ยืนยันแล้ว 24/24 · ☐ AI-suggested 28/28

| กลุ่ม | จำนวน | อยู่ที่ |
|---|---|---|
| ☑ EC-01…EC-24 (จากต้นทาง) | 24 | `05_RULES §5.5` (EC-01…EC-24) + `06_TESTS §6.2` |
| ☐ CA-01…CA-05 (concurrent) | 5 | `05_RULES §5.5 CA-*` + `§5.6 ERR_OT_STALE` · `ERR_OT_STEP_TAKEN` |
| ☐ DI-01…DI-05 (integrity/lookup) | 5 | `05_RULES §5.5 DI-*` + `§5.6 ERR_UPSTREAM_UNAVAILABLE` |
| ☐ CL-01…CL-05 (calculation) | 5 | `05_RULES §5.5 CL-*` + `03_LOGIC computeLineHours` |
| ☐ ST-E01…ST-E04 (status/workflow) | 4 | `05_RULES §5.5 ST-*` + `§5.2` |
| ☐ PM-01…PM-04 (permission/PII) | 4 | `05_RULES §5.5 PM-*` + `§5.7` |
| ☐ EN-01…EN-05 (cross-feature) | 5 | `05_RULES §5.5 EN-*` + `06_TESTS §6.9` |

**52/52 edge case มีที่ลง** — ☐ ทุกข้อ tag `[AI-SUGGESTED]` รอ BA ยืนยันที่ SOW3.7 · ข้อที่กระทบการนับซ้ำ/สิทธิ์ (CA-03 · DI-04 · ST-E04) ยกขึ้น Open Question แล้ว

### §0.12.3b Functions Cut — รายการที่ประกาศว่า "ไม่รองรับ" (**17/17** · อยู่ในแมนิเฟสต์ ไม่หายเงียบ)

| # | ไม่รองรับ | เหตุผล | OQ | พิสูจน์ที่ |
|---|---|---|---|---|
| NS-01 | คำนวณค่าล่วงเวลาเป็นเงิน | Payroll (W4) เป็นผู้คิด | OQ-STD-OT1 | `06_TESTS IA-07` |
| NS-02 | ชดเชย OT เป็นวันหยุด (TOIL) | ต้องเขียนเข้า ledger ของ Leave ซึ่งล็อกไว้ | OQ-STD-OT2 | `06_TESTS IA-08` |
| NS-03 | ค่ากะ / ค่าทำงานกลางคืน | องค์ประกอบค่าจ้าง — Salary Structure + Payroll | OQ-STD-OT3 | `06_TESTS IA-08` |
| NS-04 | คุมงบ / พยากรณ์ค่าล่วงเวลา | ประกาศท่อ FC แทน | OQ-STD-OT4 | `06_TESTS IA-08` · §0.16.2 |
| NS-05 | จัดกะ / ตารางเวร / ขอสลับกะ | Shift & Roster (W2 lane C) | — (scope note) | `06_TESTS IA-08` |
| NS-06 | **เพดาน OT รายวัน / รายเดือน** | HR Config มีแต่ `cap_hours_week` · ไม่มีคีย์ `ot_cap.*` | **OQ-STD-OT5** | `06_TESTS AT-49` |
| NS-07 | หน้าตั้งค่าอัตรา/ตัวคูณ/เพดาน/ปฏิทิน/กะ/งวด | HR Configuration เป็นเจ้าของ (#107) | — (LOCK-CFG) | `06_TESTS IA-11` |
| NS-08 | แก้เวลาเข้า-ออกจริง / ยืนยันวันทำงาน | Attendance เป็นเจ้าของ · ที่นี่อ่านอย่างเดียว | — (AT-5) | `06_TESTS IA-02` |
| NS-09 | บริหารสิทธิ์/โควตาการลา | Leave เป็นเจ้าของ | — (LV-5) | `06_TESTS IA-02` |
| NS-10 | การลบข้อมูลถาวร | append-only ทั้งระบบ | — (LOCK-AUDIT) | `06_TESTS IA-09` |
| NS-11 | การ์ดสรุปผลกระทบ 7 ด้าน | ENG-CSQ เป็นเจ้าของ | — (CSQ Iron) | `06_TESTS IA-11` |
| NS-12 | สลับบริษัทในหน้าจอ | ยังไม่มี UI | OQ-HR-05 | `06_TESTS IA-11` |
| NS-13 | อนุมัติอัตโนมัติเมื่อชั่วโมงต่ำกว่าเกณฑ์ | ต้องตั้งที่ DOA กลาง ไม่ใช่ใน feature | OQ-OT-19 | `06_TESTS IA-11` |
| NS-14 | on-call / standby | time type คนละตัว | OQ-OT-20 | `06_TESTS IA-08` |
| NS-15 | รายงาน/แดชบอร์ดแนวโน้ม OT | ชั้นรายงาน 7C (#107) | OQ-OT-21 | `06_TESTS IA-11` |
| NS-16 | พิมพ์ใบหลายใบพร้อมกัน | convenience ล้วน | OQ-OT-22 | `06_TESTS IA-11` |
| NS-17 | มอบฉันทะผู้อนุมัติ · เตือนซ้ำเมื่อใบค้าง | DOA + ENG-NOTIFY เป็นเจ้าของ | — (G-10 · G-11) | `06_TESTS IA-11` · §0.16.1 |

### §0.12.4 สรุป Coverage

| หมวด | จาก BRD | มีที่ลงในแพ็ก | หล่น |
|---|---:|---:|---:|
| Function (FN) | 65 | **65** | **0** |
| Story (ST) | 65 | **65** | **0** |
| Business Rule (BR) | 30 | **30** | **0** |
| Edge Case ☑ ยืนยันแล้ว | 24 | **24** | **0** |
| Edge Case ☐ AI-suggested | 28 | **28** | **0** |
| Scenario (S) | 45 | **45** (ผ่าน FN/BR/Edge ที่ trace ถึง) | **0** |
| Functions Cut (ไม่รองรับ) | 17 | **17** | **0** |
| Open Question | 31 | **31** (`07_LOCKED §7.3`) | **0** |
| `[ASSUMED]` จาก HTML | 6 | **6** (`07_LOCKED §7.3`) | **0** |

**ไม่มีแถวใดที่ "อยู่ที่" ว่าง — Phase 3.5 Section K ผ่าน**

---

## §0.13 ⭐ Published OT Surface — สิ่งที่ feature อื่นอ่านได้จากที่นี่

> **ส่วนนี้เขียนไว้ให้ทีมของ Payroll (⏳ W4) · ESS Portal (⏳ W6) · Shift & Roster (⏳ W2 lane C) · ชั้นรายงาน 7C อ้างอิงโดยตรง** — ยกไปวางใน `00_OVERVIEW §Dependencies` ของ feature ตัวเองได้ทันที
> **กติกาเหล็ก 5 ข้อ:**
> 1. consumer **อ่าน** ชั่วโมง OT จากที่นี่ · **ห้ามเขียนกลับทุกกรณี** — feature นี้ไม่มี write endpoint สำหรับ consumer เลย (§0.13.5)
> 2. **คืนเฉพาะใบสถานะ `time_confirmed` เท่านั้น** — ใบที่แค่ `approved` **ยังไม่ถูกคืน** (BR-17) เพราะยังไม่ผูกกับเวลาจริง
> 3. **ห้ามเก็บชั่วโมงถาวรในตารางของตัวเองโดยไม่มี `config_version_ids`**
> 4. **ห้ามคำนวณชั่วโมง OT เอง** — ใช้ `hours_confirmed` ที่คืนมา · โดยเฉพาะ **ห้ามใช้ `outside_shift_hours` ของ Attendance เป็นชั่วโมง OT โดยตรง** (BR-07 · `F-HR-ATTEND §0.13.2` ประกาศไว้แล้วว่าค่านั้น *ยังไม่ใช่ OT ที่อนุมัติ*)
> 5. **ห้ามตีความ `multiplier` เป็นจำนวนเงิน** — เป็นค่าอ้างอิงของอัตรา · **การแปลงเป็นเงินเป็นของ Payroll ทั้งหมด** (BR-18)

### §0.13.1 อะไรบ้างที่เผยแพร่ (2 มุมมอง)

| มุมมอง | เนื้อหา | ผู้ใช้หลัก | endpoint |
|---|---|---|---|
| **`day`** (OT ที่ยืนยันแล้ว รายคนรายวันรายช่วง) | เลขที่ใบ · วันที่ · ช่วงเวลา · `rate_type` · **`multiplier` (snapshot)** · `payroll_code` · **`hours_confirmed`** · สถานะใบ · ธงถูกถอนภายหลัง · `config_version_ids` | **Payroll** (ฐานตั้งต้นการคิดค่าล่วงเวลา) · **ESS** · **Shift & Roster** (กันจัดกะทับ) | `GET /api/v1/ot/resolve` |
| **`period`** (สรุปต่อคนต่องวด **แยกตาม `rate_type`**) | รหัสงวด · สถานะงวด · **ชั่วโมงรวมแยกตาม `rate_type` พร้อม `multiplier` + `payroll_code` ของแต่ละกลุ่ม** · จำนวนใบที่ยังไม่ปิด · ชั่วโมงที่ยังไม่ยืนยัน · `config_version_ids` · `snapshot_frozen_at` | **Payroll** (ฐานตั้งต้นของรอบจ่าย) | `GET /api/v1/ot/periods/resolve` |

**สิ่งที่ไม่เผยแพร่:**
- ใบสถานะ `draft` · `pending_approval` · `rejected` · `cancelled` (ยังไม่มีผลกับใคร)
- **ใบสถานะ `approved` ที่ยังไม่ `time_confirmed`** — จงใจไม่คืน (BR-17) · ปรากฏเฉพาะเป็นตัวเลข `unconfirmed_hours` + `pending_docs` ในมุมมอง `period` เพื่อให้ปลายทางรู้ว่ายอด**ยังไม่นิ่ง**
- **`reason` (เหตุผลความจำเป็น) และ `work_done` (งานที่ทำ)** — Confidential · ไม่อยู่ในมุมมองใดเลย
- ชื่อไฟล์แนบ / เนื้อไฟล์ — Confidential
- **จำนวนเงินทุกชนิด — ไม่มีในระบบนี้เลย** (BR-18 · FN-53)

### §0.13.2 หน้าทางเข้าเดียวของ OT รายคนรายวัน — `GET /api/v1/ot/resolve`

```
GET /api/v1/ot/resolve
    ?date=2026-09-14            ← บังคับเสมอ (ไม่ส่ง = 400 ERR_RESOLVE_DATE_REQUIRED)
    &date_to=2026-09-30         ← optional (ช่วงวัน · สูงสุด 62 วันต่อคำขอ)
    &company_id=<uuid>          ← บังคับเมื่อผู้เช่ามีบริษัทลูก
    &employee_id=<uuid>         ← เจาะรายคน (ใช้คู่กับ scope=employee)
    &scope=employee|company     ← default employee · company = อ่านทั้งบริษัทเป็นชุด
    &include_withdrawn=false    ← optional · true = คืนใบที่ถูกถอนด้วย (พร้อมธง)
    &page=1&page_size=500       ← เมื่อ scope=company
```

**สิ่งที่คืนกลับ (day view) — โครงที่ consumer ยกไปใช้ได้เลย · 1 แถว = 1 บรรทัดช่วงเวลาที่ยืนยันแล้ว:**

| field | ชนิด | ความหมาย | Classification |
|---|---|---|---|
| `as_of` | date | วันที่ที่ใช้ตัดสิน (สะท้อน `date` ที่ส่งมา) | Internal |
| `employee_id` · `employee_name_snapshot` | uuid · text | คนที่ชั่วโมงนี้เป็นของ | **PII** |
| `company_id` | uuid | ขอบเขตบริษัท | Internal |
| **`ot_no`** | text | เลขที่ใบ `OT-YYYY-NNNN` — **immutable · ไม่ reuse** (BR-13) · ใช้เป็นคีย์อ้างอิงข้ามระบบ | Internal |
| `line_no` | int | บรรทัดที่เท่าไรของใบนั้น | Internal |
| **`work_date`** | date | **วันเข้ากะ** — กรณีข้ามเที่ยงคืนใช้วันเข้ากะ กติกาเดียวกับ Attendance (LD-01 · BR-06) | Internal |
| `time_from` · `time_to` | time · time | ช่วงเวลาที่ทำ OT | Internal |
| `is_overnight` | bool | ช่วงนี้ข้ามเที่ยงคืน | Internal |
| **`rate_type`** | enum | `ot_workday` · `work_holiday` · `ot_holiday` — **ค่ามาจาก `ot_rate` ของ HR Configuration ไม่ใช่ enum ที่ feature นี้นิยามเอง** | Internal |
| **`multiplier`** | numeric(4,2) | **สำเนาตัวคูณ ณ เวลาสร้างใบ** — **เป็นค่าอ้างอิงของอัตรา ไม่ใช่จำนวนเงิน · ห้ามคูณเป็นเงินที่ฝั่งอื่นนอกจาก Payroll** (BR-18) | Internal |
| **`payroll_code`** | text | รหัสจ่ายที่ Payroll ใช้จับคู่กับองค์ประกอบค่าจ้าง (สำเนา) | Internal |
| **`hours_confirmed`** | decimal(5,2) | **ชั่วโมงที่รับรองสุดท้ายของบรรทัดนี้ — ตัวเลขเดียวที่ใช้จ่ายได้** | **Confidential** |
| `hours_requested` | decimal(5,2) | ชั่วโมงที่ขอเดิม — คืนมาเพื่อให้กระทบยอดได้ว่าถูกตัดตรงไหน | **Confidential** |
| **`ot_status`** | enum | **`time_confirmed` · `withdrawn` — คืนเฉพาะสองค่านี้** (draft/pending/approved/rejected/cancelled ไม่เผยแพร่) | Internal |
| `withdrawn_at` · `reversal_of` | timestamp \| null · text \| null | เวลาที่ใบถูกถอน + เลขที่/รายการเดิมที่ถูกกลับ · `null` = ยังมีผล | Internal |
| **`over_cap`** · **`cap_snapshot_hours_week`** | bool · numeric(5,2) | ใบนี้เกินเพดานรายสัปดาห์หรือไม่ + **ค่าเพดานที่ใช้ตัดสินจริง** — บริบทการปฏิบัติตามกฎหมายแรงงานสำหรับชั้นรายงาน | Internal |
| `period_code` · `period_status` | text · enum | งวดที่บรรทัดนี้สังกัด + `open` / `closed` | Internal |
| **`config_version_ids`** | object | `{ ot_rate, holiday, shift, period, attendance_day }` — **ก้อนรหัสเวอร์ชันที่ใช้ตัดสินบรรทัดนี้** (C-2 · AT-2 · BR-03) | Internal |
| `source_feature` | const | `F-HR-OT` | Internal |

**กรณีพิเศษที่ consumer ต้อง handle:**
- **ไม่มีใบ OT ของวันนั้น** → `200` พร้อม `days: []` — **ห้ามตีความว่า "ไม่ได้ทำ OT"** อาจมีใบที่ยัง `approved` แต่ยังไม่ยืนยันเวลาจริง (ดู `unconfirmed_hours` ในมุมมอง `period`)
- **ใบถูกถอนภายหลัง** → เมื่อ `include_withdrawn=true` จะคืนแถวเดิมพร้อม `ot_status='withdrawn'` + `withdrawn_at` + `reversal_of` — **แถวเดิมไม่ถูกลบ** · consumer ที่เก็บค่าไว้ต้องอ่านใหม่แล้วกลับรายการฝั่งตัวเอง (BR-27)
- **หนึ่งวันมีได้หลายแถว** (หลายช่วงเวลา / หลายใบ) — แต่ **ช่วงเวลาของคนเดียวกันจะไม่ทับกัน** เพราะกติกากันการทับซ้อนรับประกันไว้ตั้งแต่ต้นทาง (BR-29)
- **`over_cap = true` ไม่ได้แปลว่าใบไม่ถูกต้อง** — แปลว่าใบนี้ผ่านการอนุมัติเพิ่มอีกหนึ่งขั้นแล้ว (สาย 3 ชั้น)

### §0.13.3 มุมมองสรุปงวด — `GET /api/v1/ot/periods/resolve` ⭐ (Payroll ใช้ตัวนี้เป็นหลัก)

```
GET /api/v1/ot/periods/resolve
    ?period_code=2026-09        ← บังคับ (หรือส่ง date= เพื่อให้ระบบหางวดของวันนั้นให้)
    &company_id=<uuid>          ← บังคับเมื่อผู้เช่ามีบริษัทลูก
    &employee_id=<uuid>         ← optional (ไม่ส่ง = ทั้งงวดของบริษัท · แบ่งหน้า)
    &page=1&page_size=500
```

คืนต่อ (คน × งวด):

| field | ชนิด | ความหมาย |
|---|---|---|
| `period_code` · `period_from` · `period_to` · `period_status` | text · date · date · enum | ขอบเขตงวดจาก `period_rule`/`pay_period` ของ HR Configuration + `open` / `closed` |
| `employee_id` · `employee_name_snapshot` | uuid · text | คน (**PII**) |
| **`by_rate_type[]`** ⭐ | array | **แกนกลางของมุมมองนี้** — ต่อประเภทอัตรา: `{ rate_type, rate_name_snapshot, multiplier, payroll_code, ot_rate_version_id, total_hours_confirmed }` |
| **`total_hours_confirmed`** | decimal(6,2) | ผลรวมชั่วโมงที่รับรองทั้งงวดของคนนั้น (ทุกประเภทอัตรา) |
| **`unconfirmed_hours`** | decimal(6,2) | ชั่วโมงของใบที่ `approved` แต่**ยังไม่** `time_confirmed` — **ไม่ถูกนับใน `total_hours_confirmed`** · **> 0 แปลว่ายอดยังไม่นิ่ง** |
| **`pending_docs`** | int | จำนวนใบของคนนั้นที่ยังไม่ปิดในงวดนี้ (`draft` + `pending_approval` + `approved` ที่ยังไม่ยืนยัน) |
| `withdrawn_hours` | decimal(6,2) | ชั่วโมงที่ถูกถอนไปแล้วในงวดนี้ (หักออกจากยอดรวมแล้ว · แสดงเพื่อการกระทบยอด) |
| `needs_review_docs` | int | จำนวนใบที่ติดธง "ต้องทวน" ในงวดนี้ — **> 0 แปลว่ายอดอาจเปลี่ยนได้อีก** |
| `over_cap_docs` | int | จำนวนใบที่ `over_cap = true` ในงวดนี้ (บริบทการปฏิบัติตามกฎหมาย) |
| `ot_no_list[]` | array of text | เลขที่ใบทั้งหมดที่ประกอบเป็นยอดนี้ — ให้ปลายทางไล่กลับได้ |
| **`config_version_ids`** | object | `{ ot_rate: [...], holiday: [...], shift: [...], period: <uuid> }` — **ทุกเวอร์ชันที่ถูกใช้ในงวดนี้** |
| `snapshot_frozen_at` | timestamp \| `null` | เวลาที่งวดถูกปิดแล้วยอดกลายเป็นค่าคงที่ · `null` = งวดยังเปิด ยอดยังเปลี่ยนได้ |
| `source_feature` | const | `F-HR-OT` |

> **Payroll ต้องอ่าน 4 ค่านี้ก่อนใช้ตัวเลขเสมอ: `period_status` · `pending_docs` · `unconfirmed_hours` · `needs_review_docs`** — งวดที่ `open` หรือมีใบค้าง/ใบติดธงอยู่ ยอดยังเปลี่ยนได้ · งวดที่ `closed` เป็นค่าคงที่ (`snapshot_frozen_at` มีค่า) ตาม P-7
> **`multiplier` กับ `payroll_code` ใน `by_rate_type[]` เป็นบริบทให้ Payroll จับคู่องค์ประกอบค่าจ้าง ไม่ใช่จำนวนเงิน** — **การคูณเกิดที่ Payroll ที่เดียว** (BR-18 · LOCK-MONEY)
> **ไม่มีช่องใดในมุมมองนี้เป็นจำนวนเงิน** — ตรวจอัตโนมัติด้วย `06_TESTS IA-07`

### §0.13.4 กติกา 7 ข้อที่ consumer ทุกตัวต้องทำตาม (`OT-1…OT-7`)

| # | กติกา | ทำไม |
|---|---|---|
| **OT-1** | **ส่ง `date` / `period_code` เสมอ** — วันที่ของเหตุการณ์ทางธุรกิจ ไม่ใช่ "วันนี้" | อัตรา ตัวคูณ เพดาน เปลี่ยนตามเวอร์ชัน — ถามโดยไม่ระบุวันคือคำถามที่ไม่มีคำตอบเดียว (P-5 · C-1) |
| **OT-2** | **เก็บ `config_version_ids` ทั้งก้อนคู่กับเอกสารที่สร้าง** (สลิป · งวดจ่าย · รายงาน) | ตอบข้อพิพาทย้อนหลังได้ · เอกสารเก่าไม่เปลี่ยนค่าเมื่อนโยบายเปลี่ยน (ตระกูลเดียวกับ C-2 · AT-2 · LV-2) |
| **OT-3** | **ห้าม cache ข้ามวัน** — cache ได้ภายในวันเดียว · ต้องล้างเมื่อได้ event `ot.time_confirmed` · `ot.withdrawn` · `ot.hours_adjusted` | ใบถูกถอนหรือปรับชั่วโมงได้ตลอดจนกว่างวดจะปิด |
| **OT-4** | **ห้ามคำนวณชั่วโมง OT เอง** — ใช้ `hours_confirmed` ที่คืนมา · **ห้ามใช้ `outside_shift_hours` ของ Attendance เป็นชั่วโมง OT** | ชั่วโมงนอกกะเป็นข้อมูลดิบที่ยังไม่ผ่านการอนุมัติ (BR-07 · `F-HR-ATTEND §0.13.2` NS-04) — ใช้ตรงคือการจ่ายเงินจากตัวเลขที่ไม่มีใครรับผิดชอบ |
| **OT-5** | **ห้ามเขียนกลับทุกกรณี** — feature นี้ **ไม่มี write endpoint สำหรับ consumer เลย** · การแก้ใบ OT ทำที่หน้าจอของ feature นี้เท่านั้น · ใช้ลิงก์ "จัดการที่โอที" → `#/ot/list` | LD-4C-02 · #107 · ทุกการเปลี่ยนใบต้องผ่านสายอนุมัติพร้อมร่องรอย (BR-10 · BR-14) |
| **OT-6** | **ห้ามตีความ `multiplier` เป็นจำนวนเงิน** — เป็นค่าอ้างอิงของอัตรา · การแปลงเป็นเงินเป็นของ **Payroll** เท่านั้น | ระบบนี้ไม่มีตัวเลขเงินเลย (BR-18 · FN-53) — การตีมูลค่าที่ปลายทางอื่นจะทำให้เกิดตัวเลขสองชุด |
| **OT-7** | **ลงทะเบียนตัวเองใน where-used** — `POST /api/v1/ot/usage` (หรือแจ้ง BA ให้ตั้งสถานะการเชื่อม) เมื่อ feature พร้อมใช้ | HR ต้องเห็นว่าใครอ่านชั่วโมง OT อยู่บ้าง ก่อนเปลี่ยนโครง (ตระกูลเดียวกับ C-6 · AT-7 · LV-7) |

### §0.13.5 ไม่มีทางเข้าสำหรับการเขียนกลับ ⭐

**feature นี้ไม่เปิด endpoint เขียนให้ consumer เลย** — เหมือน `F-HR-ATTEND` และ `F-HR-LEAVE`
เหตุผล: **ทุกการเปลี่ยนชั่วโมง OT ต้องผ่านสายอนุมัติที่ทะเบียนกลางคืนมา พร้อมเหตุผลกับร่องรอย** (BR-10 · BR-12 · BR-14) · ถ้าให้ระบบอื่นเขียนเข้ามาได้ ร่องรอยจะขาดตอนทันที และชั่วโมงที่จ่ายจะไม่มีคนรับผิดชอบ

- **Payroll ต้องการปรับชั่วโมง** → **ไม่ใช่หน้าที่ของ Payroll** · ต้องให้ผู้อนุมัติปรับที่ใบ (อนุมัติบางส่วน) หรือถอนใบแล้วยื่นใหม่ที่หน้าจอของ feature นี้
- **Payroll ต้องการล็อกยอด** → **ล็อกเกิดจากการปิดงวดที่ HR Configuration** ไม่ใช่คำสั่งจาก Payroll (P-7)
- **ESS ต้องการให้พนักงานยื่นใบ OT** → **เรียกหน้าจอของ feature นี้** ไม่ทำ CRUD ซ้ำ (OQ-HR-04)
- **Shift & Roster ต้องการกันจัดกะทับวันที่มี OT** → **อ่าน `GET /ot/resolve` แล้วเตือนฝั่งตัวเอง** (ทิศทางเดียวกับที่ feature นี้ทำกับ Leave)
- **Attendance ต้องการรู้ว่าวันนี้มี OT** → **อ่านจากที่นี่** · **feature นี้ไม่เขียนกลับเข้า Attendance เด็ดขาด** (AT-5 · `F-HR-ATTEND §0.13.5`)

> ข้อยกเว้นเดียวคือ `POST /api/v1/ot/usage` (OT-7) ซึ่งเป็นการ **ลงทะเบียนว่าใครอ่านอยู่** ไม่ใช่การเขียนข้อมูล OT

### §0.13.6 event ที่ consumer ฟังได้ (5 event · **ท่อ EC + FC**)

| event | เมื่อไร | payload หลัก | consumer ควรทำอะไร |
|---|---|---|---|
| `ot.approved` | ใบเข้าสถานะอนุมัติแล้ว (`03_LOGIC §3.1 approveStep` ขั้นสุดท้าย) | `employee_id` · `ot_no` · `company_id` · `work_date` · `rate_type` · `multiplier` · `payroll_code` · `ot_rate_version_id` · **`hours_approved`** · `over_cap` · `cap_snapshot_hours_week` · `period_code` · `approved_by` | **ยังห้ามใช้เป็นชั่วโมงที่จ่ายได้** — เป็นภาระผูกพัน (FC · `estimated`) · Shift & Roster ใช้กันจัดกะทับได้ |
| **`ot.time_confirmed`** ⭐ | ใบเข้าสถานะยืนยันเวลาจริงแล้ว (`confirmActualHours`) | ทุก field ของ `ot.approved` + **`hours_confirmed`** · `attendance_outside_hours` · `attendance_version_ids` · `confirmed_by` · **`supersedes`** (ชี้ event `ot.approved` ของใบเดียวกัน) | **ล้าง cache ของวันนั้น · อ่าน `GET /ot/resolve` ไปใช้** — นี่คือจุดที่ชั่วโมงกลายเป็นของจริง (EC `actual` + FC `actual`) |
| `ot.withdrawn` | ใบที่อนุมัติ/ยืนยันแล้วถูกถอน (`finalizeWithdrawal`) | ทุก field ของ event ก่อนหน้า + **`reversal_of`** · `withdraw_reason` · `withdrawn_by` | **อ่านค่าล่าสุดใหม่ · กลับรายการฝั่งตัวเอง** — **event เดิมไม่ถูกลบ ไม่ถูกแก้** (BR-27 · BR-CSQ-04) |
| `ot.rejected` | ใบถูกปฏิเสธ (`rejectRequest`) | `employee_id` · `ot_no` · `work_date` · `rate_type` · `multiplier` · `payroll_code` · **`hours_requested`** · `reject_reason` · `rejected_by` | ภาระผูกพันที่อาจเกิดถูกหยุด (FC `avoided`) — ไม่มีชั่วโมงจริงเกิดขึ้น |
| `ot.hours_adjusted` | อนุมัติบางส่วน หรือปรับชั่วโมงหลังธง "ต้องทวน" (`approvePartial` · `adjustConfirmedHours`) | `employee_id` · `ot_no` · `hours_before` · `hours_after` · `adjust_kind` (`partial_approval` \| `attendance_adjusted`) · `adjust_reason` · **`supersedes`** · `adjusted_by` | อ่านค่าล่าสุดใหม่ — **ห้ามแก้ผลเดิม เป็น event ใหม่ที่ชี้ของเดิม** |

> **`ot.time_confirmed` ยิง 2 ท่อพร้อมกัน (EC + FC)** — ชั่วโมงล่วงเวลาที่ยืนยันแล้วคือ **แรงงานนอกกรอบกะที่องค์กรใช้ไปจริง** (EC · `kind: actual` · `basis: declared` · **หน่วยชั่วโมง**) และภาระผูกพันเดิมกลายเป็นค่าใช้จ่ายที่แน่นอน (FC เปลี่ยนจาก `estimated` เป็น `actual`) — รอ Architect ยืนยันว่ายิงสองท่อจากเหตุการณ์เดียวได้ (**OQ-CSQ-02** · ตระกูลเดียวกับที่ `F-HR-LEAVE` ถามไว้)
> **EC ของแพ็กนี้ไม่ซ้ำกับใคร:** Attendance ยิง EC ของ **ชั่วโมงในกรอบกะ** และประกาศเองว่า `outside_shift_hours` ยังไม่ใช่ OT · Leave ยิง EC เป็น **หน่วยวัน** · แพ็กนี้ยิง **ชั่วโมงนอกกะที่ผ่านการอนุมัติแล้ว** ซึ่งเป็นคนละก้อนโดยนิยาม (`CSQ_BRIEF §2`)
> **ไม่มี event อื่นนอกจากนี้** — การบันทึกร่าง · การส่งอนุมัติ · การเตือนเพดาน · การยกเลิก · การ validate · การเผยแพร่ให้ปลายทางอ่าน **ไม่ยิง event 7C** (กันนับซ้ำ · `CSQ_BRIEF §3`)
> **event ท่อ 7C ทั้ง 5 ตัวนี้เป็นคนละชุดกับ 7 event แจ้งเตือนของ ENG-NOTIFY** — ดู §0.16 (สองชุด **disjoint** ไม่มีชื่อซ้ำกันแม้แต่ตัวเดียว)
> **feature นี้ไม่ประกาศท่อ OC · DC ระดับเอกสาร · SC · AC · SecC** — DC ระดับเอกสารเป็นของ **DOA Engine** ซึ่ง feature นี้มีการอนุมัติจริง **ถึงสองชั้น** จึงยิ่งต้องไม่ประกาศซ้ำ (`CSQ_BRIEF §3` · register 422)

### §0.13.7 ตัวอย่างการใช้จริง (สำหรับทีม Payroll)

```
รอบจ่ายเดือนกันยายน 2026:
1. GET /api/v1/ot/periods/resolve?period_code=2026-09&company_id=<uuid>
2. ตรวจ 4 ค่าก่อนใช้:  period_status == 'closed'
                       pending_docs == 0
                       unconfirmed_hours == 0
                       needs_review_docs == 0
   → ถ้าข้อใดไม่ผ่าน = ยอดยังไม่นิ่ง ห้ามปิดรอบจ่าย
3. อ่าน by_rate_type[] ของแต่ละคน:
      { rate_type: 'ot_workday',   multiplier: 1.50, payroll_code: 'OT01', total_hours_confirmed: 12.50 }
      { rate_type: 'ot_holiday',   multiplier: 3.00, payroll_code: 'OT03', total_hours_confirmed:  6.00 }
4. Payroll คูณเป็นเงินเองด้วย rate card ของตัวเอง — **F-HR-OT ไม่ส่งเงินมาให้ และไม่มีเงินให้ส่ง**
5. เก็บ config_version_ids ทั้งก้อนไว้กับสลิป (OT-2)
```

## §0.14 ⭐ OT Data Contract — invariant ที่ห้ามผิด

### §0.14.1 invariant ของ feature นี้ (`O-1…O-9`)

| # | invariant | บังคับที่ไหน |
|---|---|---|
| **O-1** | **1 ใบ = 1 คน** — ไม่มีใบที่มีผู้ขอมากกว่าหนึ่งคนในทุกกรณี | `05_RULES BR-26` · `04_DB` (ไม่มีตารางผู้ขอหลายคน) |
| **O-2** | **เลขที่ออกตอน submit · immutable · ไม่ reuse** — ใบที่ rejected/cancelled/withdrawn คงเลขเดิม | `05_RULES BR-13` · `04_DB unique(ot_no)` |
| **O-3** | **`approval_chain` ถูก freeze ตอน submit** — แก้ DOA ทีหลังไม่กระทบใบที่ส่งไปแล้ว · จำนวน step = 2 หรือ 3 | `05_RULES BR-10` · `03_LOGIC freezeApprovalChain` |
| **O-4** ⭐ | **จำนวนชั้นของสายมาจาก action id ที่เลือกด้วยธง `over_cap` — ไม่ใช่จากตัวเลขชั่วโมงในตารางของ DOA** | `03_LOGIC §3.1 selectApprovalAction` · `DOA_BRIEF §3.1` · `06_TESTS IA-05` |
| **O-5** | **3 ตัวเลขชั่วโมงอยู่คู่กันเสมอ ไม่เขียนทับกัน** — `hours_requested` / `hours_approved` / `hours_confirmed` | `04_DB §4.2` · `05_RULES BR-21` |
| **O-6** | **เฉพาะ `time_confirmed` เท่านั้นที่เผยแพร่** | `05_RULES BR-17` · **§0.13** · `06_TESTS IA-01` |
| **O-7** | **ไม่มีตัวเลขเงินในทุกชั้น** (UI · API · DB · PDF · event) | `05_RULES BR-18` · `04_DB §4.6` · `06_TESTS IA-07` |
| **O-8** | **append-only · ไม่มี hard delete** — ทุกการยกเลิก/ถอน/ถอดไฟล์เป็นสถานะหรือธงใหม่ | `05_RULES BR-14` · `04_DB` (ไม่มี DELETE statement) |
| **O-9** | **`cap_snapshot_hours_week` + `config_version_ids` ต้องมีค่าตั้งแต่วินาที submit** — ใบที่ไม่มีสองค่านี้ถือว่าเสียหาย | `04_DB` (NOT NULL เมื่อ `status ≥ pending_approval`) · `05_RULES BR-03 · BR-09` |

### §0.14.2 กติกาที่ feature นี้ต้องทำตามในฐานะ consumer ของ HR Configuration (C-1…C-6 · P-1…P-9)

| # | กติกา | ทำอย่างไรในแพ็กนี้ |
|---|---|---|
| C-1 | ส่ง `date` + `company_id` ทุกครั้ง | `03_LOGIC resolveOtRate` · `resolveCap` — **`date` = `work_date` เสมอ ไม่ใช่ `now()`** |
| C-2 | เก็บ `config_version_ids` คู่กับเอกสาร | `snapshotConfigVersions` ตอน submit |
| C-3 | ห้าม cache ข้ามวัน | `invalidateResolveCache` ผูกกับ 7 event (BR-04) |
| C-4 | ห้าม CRUD ค่าของ HR Config | **ไม่มีหน้าตั้งค่าในแพ็กนี้** (#107) · มีแต่ลิงก์ `#/hr-config/ot-rate` |
| C-5 | ค่า `inactive` เลือกใหม่ไม่ได้ แต่ใบเก่าต้องแสดง/พิมพ์ได้ | `05_RULES BR-23` · `renderOtPdf` ใช้ snapshot |
| C-6 | ลงทะเบียน where-used | `registerWhereUsed` (BR-25) |
| **P-7** | **งวดปิด = ปฏิเสธการเปลี่ยน** | `checkPeriodOpen` ตรวจ **ทั้งตอนเปิดหน้าและ ณ วินาที commit** |
| **P-8** | **ห้าม hardcode ค่ากฎหมาย** | **ไม่มีตัวเลขเพดาน/ตัวคูณ/นาทีปัดเศษในซอร์สเลย** — `06_TESTS IA-03` ตรวจอัตโนมัติ |
| **P-9** | **ไม่มี retro** | ไม่มีเส้นทางแก้ข้อมูลของงวดที่ปิดแล้วในทุก API |

### §0.14.3 กติกาที่ feature นี้ต้องทำตามในฐานะ consumer ของ Attendance (AT-1…AT-7) และ Leave (LV-1…LV-7)

| # | กติกา | ทำอย่างไรในแพ็กนี้ |
|---|---|---|
| AT-1 · LV-1 | ส่ง `date` เสมอ | `fetchAttendanceDay` · `checkLeaveConflict` ใช้ `work_date` |
| AT-2 · LV-2 | เก็บ `version_id` ของต้นทาง | `config_version_ids.attendance_day[]` |
| AT-3 · LV-3 | ห้าม cache ข้ามวัน | `invalidateResolveCache` |
| **AT-4** | **`day_status = exception` ≠ "ทำงาน 0 ชั่วโมง"** | `05_RULES BR-08` · `fetchAttendanceDay` คืน `null` + เหตุ ไม่คืน 0 |
| **AT-5 · LV-5** | **ห้ามเขียนกลับ** | **ไม่มี write path ในแพ็กนี้** · `06_TESTS IA-02` |
| **AT-6 · LV-4** | **ห้ามคำนวณชั่วโมงในกะ/วันลาเอง** | `05_RULES BR-06` — ใช้ `day_result[]` · `counted_days` ที่คืนมา |
| AT-7 · LV-7 | ลงทะเบียน where-used | `registerWhereUsed` เรียกทั้ง 3 ต้นทาง |

## §0.15 ⭐ Soft-Reference Read Model (LD-4C-02) — วิธีที่ feature อื่นเชื่อมกับที่นี่

### §0.15.1 ทิศทาง "เข้า" — feature นี้อ้างของคนอื่น

| อ้างอะไร | เก็บอย่างไร | nullable | FK จริง? |
|---|---|:---:|:---:|
| `employee_id` (Employee Master) | id + `employee_snapshot` (code · name · position · department) | ✓ | ❌ soft |
| `ot_rate` (HR Configuration) | `rate_type` + `multiplier` + `payroll_code` + `ot_rate_version_id` (สำเนาทั้งชุด) | ✓ | ❌ soft |
| `attendance_day` (Attendance) | `attendance_outside_hours` + `attendance_day_status` + `version_id` | ✓ | ❌ soft |
| `leave_request` (Leave) | `leave_conflict_ref = { leave_no, leave_type_snapshot }` | ✓ | ❌ soft |
| `doa_entry` (DOA Engine) | `doa_entry_ref` + `approval_chain` (สำเนา) | ✓ | ❌ soft |
| `pay_period` (HR Configuration) | `period_code` + `period_status` (สำเนา) | ✓ | ❌ soft |

### §0.15.2 ทิศทาง "ออก" — คนอื่นอ้าง feature นี้

| ใครอ้าง | อ้างด้วยอะไร | เก็บอะไรไว้ฝั่งตัวเอง | ห้ามทำอะไร |
|---|---|---|---|
| **Payroll** | `ot_no` + `work_date` + `line_no` | ชั่วโมง + `rate_type` + `payroll_code` + **`config_version_ids`** | ❌ ห้ามเขียนกลับ · ❌ ห้ามคำนวณชั่วโมงเอง · ❌ ห้ามอ่านใบที่ยังไม่ `time_confirmed` |
| **ESS Portal** | `ot_no` | ไม่เก็บ — เรียกอ่านทุกครั้ง | ❌ ห้ามทำหน้าจอ CRUD ซ้ำ |
| **Shift & Roster** | `ot_no` + `work_date` + ช่วงเวลา | ธง "วันนี้มี OT" (display-only) | ❌ ห้ามเขียนกลับ · ❌ ห้ามถือว่าใบที่ถอนแล้วยังมีผล |
| **ชั้นรายงาน 7C** | `event_id` + `ot_no` | ผลกระทบที่ ENG-CSQ-02 ตีมูลค่าแล้ว | ❌ ห้ามตีมูลค่าเองจาก `multiplier` |

### §0.15.3 ทำไมต้อง soft — ไม่ใช่ FK จริง

1. **ใบ OT เป็นหลักฐานทางแรงงานที่ต้องอ่านได้ตลอด** — คนลาออก อัตราถูกปิดใช้ ปฏิทินถูกแก้ ใบเก่าต้องยังเปิดกับพิมพ์ได้ (BR-23 · C-5)
2. **feature ปลายทางยังไม่มีตัวจริง** (Payroll W4 · ESS W6 · Roster lane C) — FK จริงจะทำให้ deploy ไม่ได้จนกว่าทุกฝ่ายจะพร้อม
3. **การลบตามกันเป็นสิ่งต้องห้ามในระบบนี้** — ไม่มี hard delete ที่ใดเลย FK cascade จึงไม่มีความหมาย (LOCK-AUDIT)
4. **ข้ามขอบเขตผู้เช่า/บริษัท** — soft reference ทำให้ขอบเขตข้อมูลถูกบังคับที่ชั้น query ไม่ใช่ที่ชั้นตาราง

---

## §0.16 ⭐ Declaration Conformance — event ⊆ brief (Lane Mode v2 gate)

> **กติกาของ gate:** ทุก event / action / doc_type / เอกสาร ที่ FRD พูดถึง **ต้องเป็นสับเซ็ตของ `5_DECLARATIONS/`** · ถ้า FRD ต้องการเพิ่ม → **ต้อง append ในใบ brief เดิม ห้ามออกใบใหม่**
> **ผลการตรวจรอบนี้: ไม่มีการเพิ่มใด — FRD ใช้ครบพอดีตามที่ brief ประกาศไว้ทุกใบ** (append เฉพาะคอลัมน์ trigger ที่ชี้ `03_LOGIC` จริง)

### §0.16.1 NTF — **7 event ธุรกิจ** (⊆ `NTF_BRIEF.md §2`)

| # | event_id | trigger จริงใน FRD | ผู้รับ | ช่องทาง default | ปิดได้ |
|---|---|---|---|---|---|
| 1 | `ot_submitted` | `03_LOGIC §3.1 submitRequest` (หลัง freeze chain สำเร็จ) | ผู้ถือ slot ปัจจุบัน + ผู้ขอ (สำเนา) | in-app | ✓ |
| 2 | `ot_decided` | `approveStep` (ขั้นสุดท้าย) · `approvePartial` · `rejectRequest` | ผู้ขอ + หัวหน้าโดยตรง | in-app + email | ✗ บังคับ |
| 3 | `ot_cap_warning` | `computeCapWarning` (ตอนกรอกบรรทัด · ตอน submit) | ผู้ขอ + หัวหน้าโดยตรง | in-app | ✓ |
| 4 | `ot_cap_exceeded` | `computeOverCap` = true ที่ `submitRequest` | ผู้ขอ + หัวหน้า + HR | in-app + email | ✗ บังคับ |
| 5 | `ot_cancelled` | `cancelRequest` | ผู้ถือ slot ที่ค้างอยู่ | in-app | ✓ |
| 6 | `ot_withdrawn` | `finalizeWithdrawal` | ผู้ขอ + หัวหน้า + HR | in-app + email | ✗ บังคับ |
| 7 | `ot_confirm_pending` | `sweepPendingConfirm` (scheduler รายวัน) · `onAttendanceDayAdjusted` (ธง "ต้องทวน") | หัวหน้า + HR | in-app (+email เมื่อเป็นธง "ต้องทวน") | ✓ |

**ตรวจ:** 7 = 7 ✅ · **ไม่มี event ใหม่ที่ FRD คิดขึ้นเอง**
**ไม่ประกาศ (และต้องไม่ประกาศ):** `doa_pending` · `doa_result` · `doa_escalate` · reminder เมื่อใบค้าง · การมอบฉันทะ — **DOA Engine + ENG-NOTIFY ยิงเอง** · ประกาศซ้ำ = BLOCK (`NTF_BRIEF §3`)

### §0.16.2 CSQ — **5 event · 2 ท่อ (EC + FC เท่านั้น)** (⊆ `CSQ_BRIEF.md §2`)

| # | event_id | trigger จริงใน FRD | ท่อ | kind · basis | payload หลัก |
|---|---|---|---|---|---|
| E1 | `ot.approved` | `03_LOGIC §3.1 approveStep` (ขั้นสุดท้าย) | **FC** | `estimated` · `declared` | `hours_approved` · `rate_type` · `multiplier` · `payroll_code` · `ot_rate_version_id` · `over_cap` · `cap_snapshot_hours_week` · `period_code` |
| E2 ⭐ | `ot.time_confirmed` | `03_LOGIC §3.1 confirmActualHours` | **EC + FC** | `actual` · `declared` | field ของ E1 + `hours_confirmed` · `attendance_outside_hours` · `attendance_version_ids` · **`supersedes`** |
| E3 | `ot.withdrawn` | `03_LOGIC §3.1 finalizeWithdrawal` | **EC + FC** | `actual` / ตามสถานะที่ถอน | field ของ E1/E2 + **`reversal_of`** · `withdraw_reason` |
| E4 | `ot.rejected` | `03_LOGIC §3.1 rejectRequest` | **FC** | `avoided` | `hours_requested` · `rate_type` · `multiplier` · `payroll_code` · `reject_reason` |
| E5 | `ot.hours_adjusted` | `03_LOGIC §3.1 approvePartial` · `adjustConfirmedHours` | **EC + FC** | `actual` / `estimated` | `hours_before` · `hours_after` · `adjust_kind` · **`supersedes`** |

**ตรวจท่อ:** ประกาศ **EC · FC** เท่านั้น ✅
**ไม่ประกาศ (บังคับ):** **OC** ❌ (มาจาก Operation Process) · **DC ระดับเอกสาร** ❌ (**DOA เป็นเจ้าของ — feature นี้มีการอนุมัติจริงถึงสองชั้น ยิ่งต้องไม่ประกาศซ้ำ**) · **SC** ❌ (สงวน) · **AC** ⬜ (รายการบัญชีเกิดที่ Payroll/Accounting) · **SecC** ⬜ (นโยบาย OT เป็นของ HR Configuration ซึ่งประกาศไว้แล้ว — ประกาศที่นี่ = นับซ้ำ)
**`idempotency_key`:** `F-HR-OT:{ot_no}:{event_id}` สำหรับ E1–E4 · `F-HR-OT:{ot_no}:{event_id}:{seq}` สำหรับ E5
**ห้ามคำนวณมูลค่า:** ไม่มี `cost = hours × multiplier × rate` ที่ใดในแพ็กนี้ — **ENG-CSQ-02 เป็นเจ้าของการตีมูลค่า** (`06_TESTS IA-07`)

### §0.16.3 ⭐ สองชุด event เป็นคนละชุดกัน (disjoint) — ตรวจแล้ว

| | NTF (แจ้งคน) | CSQ (ผลกระทบ 7C) |
|---|---|---|
| จำนวน | **7** | **5** |
| รูปแบบชื่อ | `ot_<verb>` (underscore) | `ot.<verb>` (dot) |
| ชื่อที่ซ้ำกัน | **0 ตัว** — ตรวจแบบตัวต่อตัวแล้ว | |
| ตัวอย่างที่ดูคล้ายแต่คนละตัว | `ot_decided` = **การแจ้งผู้ขอด้วยภาษาใบ OT** (รวม approve/reject/partial ไว้ตัวเดียว) | `ot.approved` · `ot.rejected` · `ot.hours_adjusted` = **3 event ผลกระทบแยกกัน** เพราะท่อกับ kind ต่างกันคนละเรื่อง |
| เจ้าของ | ENG-NOTIFY | ENG-CSQ |
| **ทั้งสองชุดไม่ประกาศ `doa_pending` / `doa_result` / DC ระดับเอกสาร** | ✅ | ✅ |

### §0.16.4 DOA — **2 matrix · 6 action** (⊆ `DOA_BRIEF.md §2–§3`)

| action_id | ใช้เมื่อ | matrix | จำนวน step |
|---|---|---|---|
| `ot_approve_within_cap` | `over_cap = false` | set 1 | **2** (หัวหน้าโดยตรง → ผจก.ฝ่ายบุคคล) |
| `ot_approve_over_cap` ⭐ | `over_cap = true` | set 2 | **3** (+ ผู้บริหารต้นสังกัด) |
| `ot_confirm_actual_hours` | ยืนยันเวลาจริง | ใช้ matrix ตาม `over_cap` | — |
| `ot_approve_partial` | อนุมัติบางส่วน | ใช้ matrix ตาม `over_cap` | — |
| `ot_approve_withdrawal` | อนุมัติการถอน | ใช้ matrix ตาม `over_cap` | — |
| `ot_approve_resubmit` | อนุมัติใบที่แก้แล้วส่งใหม่ | **re-resolve ใหม่ — matrix อาจเปลี่ยน** | 2 หรือ 3 |

**ตรวจ:** 6 = 6 ✅ · 2 matrix = 2 ✅
**invariant ที่สำคัญที่สุด:** ทั้งสอง matrix ใช้ `amount_from: 0` · `amount_to: null` — **ไม่มีตัวเลขชั่วโมงเป็นขอบของ set ใดเลย** · การเลือกชั้นเกิดจาก **action id** ที่ feature ส่งเข้าไป (`03_LOGIC §3.1 selectApprovalAction` · `06_TESTS IA-05`)

### §0.16.5 DOCCFG — **1 doc_type** (⊆ `DOCCFG_BRIEF.md §1`)

| doc_type | รูปแบบ | ออกเมื่อ | reset | สำเนา |
|---|---|---|---|---|
| `OT` | `OT-YYYY-NNNN` | `submitRequest` (ไม่ใช่ตอนร่าง) | รายปี `[ASSUMED]` OQ-DOCCFG-01 | `ENG-DOC-STORE.store(pdf, 'OT', ot_request_id, 'approved_final')` ตอนอนุมัติครบสาย |

**ตรวจ:** 1 = 1 ✅ · **ไม่มี doc_type อื่นในแพ็ก**

### §0.16.6 PDFDOC — **1 เอกสาร** (⊆ `PDFDOC/print-spec.md`)

| เอกสาร | ขนาด | ช่องลงนาม | ตัวเลขเงิน |
|---|---|---|---|
| ใบขอทำงานล่วงเวลา (Overtime Request Form) | A4 แนวตั้ง · **1 หน้า** (ขยายได้เมื่อมีหลายบรรทัด) | **3 ช่องปกติ · 4 ช่องเมื่อ `over_cap`** — จำนวน = `approval_chain.length + 1` **ห้าม render ตายตัว** | **ไม่มี** |

**ตรวจ:** 1 = 1 ✅ · รายละเอียดเต็มอยู่ที่ **`PRINT_SPEC.md`** ของแพ็กนี้

### §0.16.7 สรุปผล gate

| ท่อ | brief ประกาศ | FRD ใช้ | ⊆ ? | เพิ่มใหม่? |
|---|---:|---:|:---:|---|
| NTF | 7 | 7 | ✅ | ไม่มี |
| CSQ | 5 (2 ท่อ) | 5 (2 ท่อ) | ✅ | ไม่มี |
| DOA | 6 action · 2 matrix | 6 · 2 | ✅ | ไม่มี |
| DOCCFG | 1 doc_type | 1 | ✅ | ไม่มี |
| PDFDOC | 1 เอกสาร | 1 | ✅ | ไม่มี |

**Declaration Conformance: ✅ PASS — event ⊆ brief ทุกใบ · EC+FC เท่านั้น · สองชุด event disjoint · ไม่มีใบใดประกาศซ้ำ `doa_pending`/`doa_result` หรือ DC ระดับเอกสาร**

---

**จบ 00_OVERVIEW** → ต่อที่ `01_UI.md` · สรุปผล Phase 3.5 A–M อยู่ที่ `INDEX.md`
