# BRD: HR Configuration (ตั้งค่าHR)

| Field | Value |
|---|---|
| BRD ID | BRD-HR-CONFIG-001 |
| Feature Name | HR Configuration — ตั้งค่าHR |
| Feature Code | F-HR-CONFIG |
| BRD Type | **New Feature** |
| Version | 1.0 |
| Status | **AI Reviewed — APPROVED** |
| Module / Wave / Lane | HR · W1 · Lane A |
| Archetype | `master/config` (A+B+C) — ยืนยันที่ STANDARD_BASELINE §3 |
| Owner | BA (lane runner · feature-lane-runner v2.3 S4) |
| Stakeholders | Strike (เจ้าของ scope/OQ) · พี่เบิร์ด (ติดตามงาน) · Architect (engine candidates) · Chin (ENG-NOTIFY) · ทีม HR (HR Admin/HR Staff) |
| Created Date | 2026-08-28 |
| Last Updated | 2026-08-28 |
| Mode | **Lane Mode v2** (brd-generator-full v2.2 · no-ask · RIF เป็น derived จาก PREBRIEF) |
| Source of truth | `PREBRIEF.md` v1.1 (35 S · 21 BR · §12) · `FUNCTION_CHECKLIST.md` (53 FN) · `STANDARD_BASELINE.md` (19 MUST · 5 states) · `STANDARD_GAP.md` · `LANE_BRIEF.md` (LOCK/OQ) · `5_DECLARATIONS/CSQ_BRIEF.md` + `NOT_NEEDED.md` · HTML `1_HTML/ตั้งค่าHR.html` (7 routes · ผ่าน S3a/S3b/S3c) |

## Changelog
- **v1.0 (2026-08-28)** — สร้าง BRD ผ่าน `brd-generator-full` v2.2 **Lane Mode v2** จาก PREBRIEF v1.1 + FUNCTION_CHECKLIST (53 FN) + HTML v9 ที่ผ่าน gate (COVERAGE_R1 🟢 PASS · UX_CHECK 🟢 PASS · audit FAIL=0) · ไม่มี RIF ต้นฉบับ — PREBRIEF ทำหน้าที่ business intent · **DIVERGENCE: ไม่มี** · `[ASSUMED]` สืบทอด 8 ข้อ (ดู §15)

---

# Section 2: Business Context

## 2.1 ปัญหา / โอกาส

**ปัญหาวันนี้:** กติกา HR ที่มีผลทางกฎหมายและทางนโยบาย — ประเภทการลาและโควตา · อัตรา OT · ปฏิทินวันหยุด · กะมาตรฐาน · รอบตัดเวลา/รอบจ่าย · รอบประเมิน — กระจายอยู่ในไฟล์ Excel, อีเมลประกาศ, และค่าที่ dev ฝังไว้ในโค้ดของแต่ละระบบย่อย ผลคือ

1. **ตอบไม่ได้ว่า "ณ วันนั้นบริษัทใช้กติกาอะไร"** — เมื่อมีข้อพิพาทแรงงานหรือการตรวจสอบย้อนหลัง ไม่มีหลักฐานว่านโยบายเปลี่ยนเมื่อไร ใครเปลี่ยน และเปลี่ยนจากอะไรเป็นอะไร
2. **แก้ที่เดียวไม่พอ** — เปลี่ยนโควตาลาพักร้อนต้องไล่แก้หลายที่ พลาดที่ใดที่หนึ่งคือคำนวณสิทธิ์พนักงานผิด
3. **feature HR แต่ละตัวสร้างหน้าตั้งค่าของตัวเอง** — ค่าเดียวกันมีหลายแหล่ง ขัดกันเอง และไม่มีใครเป็นเจ้าของ
4. **การเปลี่ยนนโยบายมีผลทันที** ไม่มีกลไก "จะมีผลวันที่ …" ทำให้แก้ค่าตอนกลางงวดแล้วกระทบยอดที่ปิดไปแล้ว

**โอกาส:** ยก "ค่าตั้งต้นเชิงนโยบาย/กฎหมาย" ทั้งหมดขึ้นมาเป็น **feature เดียวที่เป็นต้นน้ำของ HR ทั้งโมดูล** โดยเก็บทุกค่าเป็น **เวอร์ชันที่มีวันมีผล (`effective_date`)** ไม่ใช่ค่าเดียวที่ถูกเขียนทับ — ทำให้ทุก feature ปลายทาง (8 ตัว) อ่านค่าจากแหล่งเดียว และย้อนดูได้เสมอ

## 2.2 เป้าหมายทาง Business

| # | เป้าหมาย |
|---|---|
| G-01 | มี **แหล่งเดียว (single source)** ของค่านโยบาย HR ทั้ง 6 กลุ่ม — feature อื่นอ่าน ไม่สร้างเอง (#107) |
| G-02 | ทุกค่าเชิงกฎหมาย/นโยบายมี **`effective_date` + ประวัติเวอร์ชัน** ตอบข้อพิพาทย้อนหลังได้ (HR-1) |
| G-03 | เปลี่ยนนโยบายแบบ **ตั้งล่วงหน้า** ได้ (Scheduled) โดยไม่กระทบงวดที่ปิดไปแล้ว |
| G-04 | ก่อนปิดใช้ค่าใด ๆ **เห็นผลกระทบปลายทาง** (where-used) ก่อนเสมอ |
| G-05 | รองรับ **หลายบริษัทลูก** — ค่ากลางใช้ร่วม บริษัทลูก override ได้ |
| G-06 | ไม่มีการลบถาวร — ทุกอย่าง soft archive + audit append-only |

## 2.3 ตัวชี้วัดความสำเร็จ (Success Metrics) — บังคับวัดได้

| # | ตัวชี้วัด | Baseline ปัจจุบัน | Target | วัดยังไง / จากไหน | วัดเมื่อไหร่ | KPI คู่ (§17.3) |
|---|---|---|---|---|---|---|
| M-01 | จำนวน feature HR ที่มีหน้าตั้งค่าของตัวเอง (ละเมิด #107) | **ต้องเก็บ baseline ก่อน launch** — ปัจจุบันมี feature HR เสร็จ 1 ตัว (Employee Master) ยังวัดไม่ได้ | **0** | ตรวจ `FEATURE_REGISTRY` + code review ตอนปิดแต่ละ feature HR (18 ตัวที่เหลือ) | ทุกครั้งที่ปิด feature HR ใหม่ | K-01 |
| M-02 | สัดส่วนค่านโยบายที่มี `effective_date` ครบถ้วน | **0%** (วันนี้ค่าอยู่ใน Excel/hardcode ไม่มีวันมีผล) | **100%** | `count(config_version where effective_date is not null and status<>Draft) / count(config_version where status<>Draft)` | รายเดือน | K-02 |
| M-03 | เวลาเฉลี่ยตอบคำถาม "ณ วันที่ X บริษัทใช้กติกาอะไร" | **~120 นาที** (ค้น Excel/อีเมล — ตัวเลขประมาณจาก HR · **ต้อง re-baseline ด้วยการจับเวลาจริง 5 เคสก่อน launch**) | **≤ 2 นาที** | จับเวลาตั้งแต่เปิดหน้า → ใช้ตัวกรอง "ดูค่าที่มีผล ณ วันที่" → ได้คำตอบ (UAT + spot check ราย 3 เดือน) | ราย 3 เดือน | K-03 |
| M-04 | จำนวนครั้งที่ค่าที่ Active ถูกแก้ทับโดยไม่เกิดเวอร์ชันใหม่ | **ไม่ทราบ** (ระบบเดิมไม่มี log) | **0 ครั้ง/เดือน** | นับ event `config_version.update` ที่ `target_status=Active` ใน Policy Center Audit Trail (by design ต้อง = 0) | รายเดือน | K-04 |
| M-05 | สัดส่วนการปิดใช้ค่าที่ผู้ใช้เห็น where-used ก่อนยืนยัน | **0%** (ไม่มีฟังก์ชัน) | **100%** | audit event `config_item.deactivate` ที่มี attribute `where_used_shown=true` และ `reason.length>=10` | รายเดือน | K-05 |
| M-06 | จำนวนครั้งที่ตั้ง `effective_date` ย้อนเข้างวดที่ปิดแล้วได้สำเร็จ | **ไม่ทราบ** (ระบบเดิมไม่มีนิยาม "งวดปิด") | **0 ครั้ง** | นับ audit event ที่ `effective_date < period.close_date` และ result=success (ต้องถูกบล็อกที่ BR-04 ทุกครั้ง) | รายเดือน | K-06 |

> ตัวชี้วัดทุกตัวมีคู่ใน §17.3 KPI ครบ (C22) · M-01 และ M-03 ระบุชัดว่า **ต้องเก็บ baseline ก่อน launch** เป็น action ไม่ใช่เว้นว่าง

## 2.4 ที่มาของ Requirement

- **scope note จากผู้เลือกงาน (verbatim):** "ศูนย์ตั้งค่า HR ที่ทุก feature อ่าน (ห้าม feature อื่นสร้างเอง #107): ประเภทการลา+โควตา/เงื่อนไขสะสม · อัตรา OT/วันหยุด/กะมาตรฐาน · ปฏิทินวันหยุดบริษัท · รอบตัดเวลา/รอบจ่าย · รอบประเมิน · ทุกค่ามี effective_date + ประวัติเวอร์ชัน (HR-1) · เปิด/ปิดค่าตามบริษัทลูก (multi-company ready) · ไม่ทำ payroll formula (อยู่ Salary Structure) · ไม่มี approval"
- **มติ/LOCK ที่ผูกงานนี้:** HR-1 (current-state §3) · #107 (TASTE_LOG 2026-08-26 Consent run 3) · LD-4C-02 · audit append-only
- **ERP benchmark (STANDARD_BASELINE · web search 6 ครั้ง 2026-08-28):** Odoo 17–19 Time Off Configuration · D365 HR Leave/Absence + pay cycles + shared parameters · SAP SuccessFactors EC Time Management + Foundation Objects (effective dating เป็นแกนของระบบ) — 24 capability · **19 MUST**
- **ช่องว่างที่พบรอบ S1.5 (STANDARD_GAP):** G-01 งวดจริงของรอบจ่าย (MUST → merge) · G-02 ปฏิทินหลายชุดต่อสถานที่ · G-03 รอบบันทึกเวลาแยกจากรอบจ่าย · G-07 ลาต่อเนื่องสูงสุด (SHOULD → merge) · G-04/G-05/G-06 (→ "ไม่รองรับ" + OQ)

---

# Section 3: Scope

## 3.1 In Scope

| # | รายการ | อ้าง |
|---|---|---|
| IN-01 | **ประเภทการลา + โควตา/เงื่อนไขสะสม** — หน่วยนับ · จ่าย/ไม่จ่าย/จ่ายบางส่วน · โควตาต่อปี · ขั้นตามอายุงาน (milestone) · ยกยอด + วันหมดอายุ · prorate + ปัดเศษ · กติกานับวันลา · ต้องแนบเอกสาร · ลาต่อเนื่องสูงสุด · ติดลบได้ถึง | S-01,S-05,S-06,S-07,S-21 · §3.3ก |
| IN-02 | **อัตรา OT / อัตราวันหยุด / กะมาตรฐาน** — ตัวคูณต่อประเภท · ฐานคำนวณ · เพดาน ชม./สัปดาห์ · `payroll_code` (soft ref) · กะ (เข้า-ออก · พัก · ข้ามวัน · วันทำงานในสัปดาห์ · ชม./วัน computed) | S-08,S-09,S-10 |
| IN-03 | **ปฏิทินวันหยุดบริษัท** — วันหยุดประจำปี · วันหยุดชดเชยที่อ้างวันต้นทาง · แยกชุดตามสถานที่/สาขา (`location`) · กะที่ได้รับผล | S-11,S-12,S-32 |
| IN-04 | **รอบตัดเวลา + รอบจ่าย** — ความถี่ · วันตัด · วันจ่าย · ล็อกงวดที่ปิด · **ความถี่รอบบันทึกเวลาแยกจากรอบจ่าย** · **สร้างงวดจริงทั้งปี + ปิด/เปิดงวด** | S-13,S-14,S-31 |
| IN-05 | **รอบประเมิน** — ชื่อรอบ · ปี · ช่วงประเมิน · ช่วงเปิดกรอก · ความถี่ | S-15,S-16 |
| IN-06 | **ขอบเขตบริษัท (multi-company ready)** — ค่ากลาง (shared) vs เฉพาะบริษัท · ลำดับ resolve บริษัทลูกทับค่ากลาง · field `applies_to` เป็น hook | S-17,S-22 |
| IN-07 | **แกน HR-1:** ทุกค่าเป็นเวอร์ชันที่มี `effective_date` · ประวัติเวอร์ชันเต็ม · ดูค่าที่มีผล ณ วันที่ย้อนหลัง · แก้ = สร้างเวอร์ชันใหม่ ห้ามเขียนทับ | S-01..S-04,S-20 |
| IN-08 | **ปิดใช้ (soft archive) + where-used** — เตือนพร้อมรายการ feature ปลายทางที่อ้างอยู่ก่อนยืนยัน · เปิดใช้กลับได้ · ไม่มีลบถาวร | S-18,S-19 |
| IN-09 | **สัญญาการอ่านค่าให้ 8 feature ปลายทาง** — ขอค่าพร้อม "วันที่" เสมอ → คืนเวอร์ชันที่ Active ณ วันนั้น (soft reference display-only) | §7 · §9 |
| IN-10 | **ประกาศท่อ CSQ (SecC)** — เวอร์ชันมีผล/ปิดใช้ = เปลี่ยนสิทธิ์พนักงาน → ส่ง event ให้ ENG-CSQ 7C (เรียกใช้ ไม่ทำเอง) | §12 · CSQ_BRIEF |

## 3.2 Out of Scope (สำคัญ — ประกาศบนจอด้วย ไม่เงียบ)

| # | ไม่ทำ | เจ้าของจริง | อ้าง |
|---|---|---|---|
| OUT-01 | approval workflow ตอนแก้ค่านโยบาย | — (คุมด้วย effective_date + audit) | S-23 · FN-40 · **OQ-STD-01** |
| OUT-02 | คำนวณย้อนหลัง (retro recalculation) | engine candidate `hr-policy-retro-engine` | S-24 · FN-41 · **OQ-STD-04** |
| OUT-03 | สูตรคำนวณเงินเดือน / mapping earning code เต็มรูป | Salary Structure (W1/B) · Payroll (W4) | S-25 · FN-42 · **OQ-STD-03** |
| OUT-04 | ยอดวันลาคงเหลือรายคน (leave balance) | Leave (W2) | S-26 · FN-43 · **OQ-HR-02** |
| OUT-05 | UI สลับบริษัท (company switcher) บนหัวจอ | รอบถัดไป (มี field company แล้ว) | S-27 · FN-44 · **OQ-HR-05** |
| OUT-06 | auto-import วันหยุดราชการตามประเทศ | — (NICE · C-23) | S-28 · FN-45 |
| OUT-07 | แจ้งเตือนพนักงานเมื่อนโยบาย/ปฏิทินเปลี่ยน | feature ปลายทาง (Leave/OT/Shift&Roster) | S-29 · FN-46 · **OQ-STD-05** |
| OUT-08 | import/export ค่า config เป็นชุด (mass upload) | Attendance (W1/C) เป็นเจ้าของ pattern import | S-30 · FN-47 |
| OUT-09 | ระยะทดลองงาน (probation) / ระยะบอกกล่าวล่วงหน้า | On/Offboard · Employee Movement (W3) | S-33 · FN-51 · **OQ-STD-06** |
| OUT-10 | ความถี่การคำนวณจ่าย (calculation frequency) รายสัปดาห์/รายปักษ์ | Payroll (W4) | S-34 · FN-52 · **OQ-HR-01** |
| OUT-11 | Time Profile (มัดชุดค่าเวลา assign ให้กลุ่มพนักงาน) | — | S-35 · FN-53 · **OQ-STD-02** |
| OUT-12 | eligibility ตามประเภทจ้าง/ระดับ/แผนก | — (เผื่อ field `applies_to` เป็น hook) | S-22 · FN-30 · **OQ-STD-02** |
| OUT-13 | ลบค่าถาวร (hard delete) | — (มติ audit append-only) | BR-07 · FN-24 |
| OUT-14 | หน้าตั้งค่าของ feature HR อื่น | ทุก feature อ้างมาที่นี่ | **#107** |
| OUT-15 | ตารางกะจริงรายคน (roster) · เวลาเข้างานจริง · แบบฟอร์มประเมิน | Shift & Roster · Attendance · Performance | LANE_BRIEF "ไม่ทำรอบนี้" |
| OUT-16 | **re-implement baseline engines** — DOA Engine · Document Configuration · ENG-NOTIFY · Roles & Permissions/Data Masking/Audit Trail · Employee Master combobox · ENG-CSQ 7C · Operation Process | baseline (catalog §0) | OB-15 |

## 3.3 Assumptions

| # | สมมติฐาน | tag |
|---|---|---|
| A-01 | ไม่มี approval ในการเปลี่ยนนโยบาย — `effective_date` + audit append-only + สถานะ Draft→Scheduled เป็นตัวคุมแทน | `[ASSUMED]` OQ-STD-01 |
| A-02 | eligibility ของค่า config จำกัดที่ระดับบริษัทเท่านั้นรอบนี้ · `applies_to` = "ทั้งบริษัท" อ่านอย่างเดียว | `[ASSUMED]` OQ-STD-02 |
| A-03 | `payroll_code` เป็น soft reference (text) เท่านั้น ไม่ผูกสูตรคำนวณเงินใด ๆ | `[ASSUMED]` OQ-STD-03 |
| A-04 | ไม่มี retro — บล็อกการตั้ง `effective_date` ย้อนเข้างวดที่ปิดแล้วแทน | `[ASSUMED]` OQ-STD-04 |
| A-05 | การแจ้งเตือนพนักงานเกิดที่ feature ปลายทาง — feature นี้ไม่ประกาศท่อ NTF | `[ASSUMED]` OQ-STD-05 |
| A-06 | ระยะทดลองงาน/ระยะบอกกล่าวล่วงหน้าไม่อยู่ที่นี่รอบนี้ (นอก 6 กลุ่มค่าใน scope note) | `[ASSUMED]` OQ-STD-06 |
| A-07 | Payroll สร้างเองเต็ม — กระทบ feature นี้แค่ "รอบจ่าย" | `[ASSUMED]` OQ-HR-01 |
| A-08 | แหล่งข้อมูลเวลาเข้างาน = import ไฟล์ + กรอกมือ — กระทบ feature นี้แค่ "รอบตัดเวลา" | `[ASSUMED]` OQ-HR-03 |
| A-09 | consumer ทั้ง 8 ตัวยัง ⏳ ยังไม่ทำ → where-used ใช้ Module Linkage + manual status override · ห้าม mock หน้าจอ feature ปลายทาง | OB-14 |
| A-10 | ผู้ใช้ทั้งหมด login ผ่าน Roles & Permissions (Policy Center) — ไม่มี persona switch บนหน้า (demo อยู่ `.demo-strip`) | #105 |

## 3.4 Scope Lock ⭐ (สืบทอดจาก `LANE_BRIEF.md` §LOCK — ศักดิ์เท่าใบเซ็น)

| LOCK ID | มติ | ผลกับ BRD นี้ |
|---|---|---|
| **HR-1** | legal/policy parameter ทุกตัวมี `effective_date` เสมอ · ห้าม hardcode | §6 แยก `config_item`/`config_version` · BR-01,BR-02 = FIXED ห้ามลด |
| **#107** | feature อื่นห้ามสร้างหน้า config เอง — อ้างมาที่นี่ | §12.1 downstream ทุกแถวเป็น "อ่าน" ไม่ใช่ "มี config ของตัวเอง" · OUT-14 |
| **LD-4C-02** | soft reference: master = picker assist · nullable · ไม่มี FK cascade · **ห้าม CRUD ของ feature อื่น** | §6 ทุก reference เป็น snapshot/display-only · where-used เป็น list + ลิงก์เท่านั้น |
| **DOA iron rule** | ไม่มี hardcoded approval chain | N/A รอบนี้ (ไม่มี approval เลย) · ถ้า OQ-STD-01 เคาะกลับ → แทรก `GET /doa/resolve` ที่ transition Draft→Scheduled จุดเดียว |
| **Audit append-only** | ไม่มี hard delete — soft archive/deactivate เท่านั้น | BR-07,BR-14 = FIXED · §6 ไม่มี field `deleted_at` แบบ hard |
| **7C ท่อต้องห้าม** | ห้ามประกาศ OC (จาก OP) · DC ระดับเอกสาร (จาก DOA) · SC (สงวน) → register 422 | §16 · CSQ ประกาศ **SecC เท่านั้น** |
| **Module Linkage** | config เชื่อม/ไม่เชื่อม + manual status override | §12.1 · where-used แสดง ⏳/✅ |
| **UI standard** | #102 combobox anatomy · #103 lean list · #104 1 feature = 1 เมนูซ้าย · #105 demo persona ใน `.demo-strip` · #106 ห้าม hint banner · CI Warm Light | §14.6 UI Signals (spec จริงเป็นของ FRD) |

**Scope Drift check:** ตรวจ In Scope ทุกข้อเทียบ scope note + LOCK → **ไม่พบข้อที่เกินใบเซ็น**
- IN-04 ส่วน "สร้างงวดจริง + ปิดงวด" (S-31/FN-48) มาจาก **STANDARD_GAP G-01 = MUST** และเป็นนิยามที่ BR-04 ต้องใช้ (ปิด `[AI-DRAFT]` เดิม) → อยู่ในกลุ่มค่าที่ 4 ของ scope note **ไม่ใช่ scope ใหม่**
- IN-03 ส่วน `location` (S-32/FN-49) และ IN-04 ส่วน `workPeriod` (FN-50) = SHOULD จาก G-02/G-03 → merge พร้อม tag `[AI-DRAFT]` รอ BA เคาะ (§15 Q-11, Q-12) — **ไม่ใช่ SCOPE DRIFT** แต่เป็นการขยาย field ภายในกลุ่มค่าเดิม
- **⚠️ SCOPE DRIFT: ไม่มี**

---

# Section 4: User Roles & Permissions

## 4.1 Roles ที่เกี่ยวข้อง

| Role | ที่มาของสิทธิ์ | คำอธิบาย |
|---|---|---|
| **HR Admin** | Roles & Permissions (Policy Center) | เจ้าของ feature — ตั้ง/แก้ค่านโยบายทุกกลุ่ม |
| **HR Staff** | Roles & Permissions | ดูได้ทุก tab + ประวัติ แก้ไม่ได้ |
| **หัวหน้าสายงาน / ผู้ใช้ทั่วไป** | Roles & Permissions | ดูค่าที่มีผลปัจจุบัน (read-only) ผ่านลิงก์จาก feature ต้นทาง |
| **ระบบ (feature ปลายทาง 8 ตัว)** | service account | อ่านค่าที่ Active ณ วันที่ที่ขอ (LD-4C-02 · read-only) |
| **ระบบ (scheduler)** | system | เปลี่ยน Scheduled→Active เมื่อถึงวันมีผล · Active→Superseded เมื่อมีเวอร์ชันใหม่ |

## 4.2 Permission Matrix

| Action | HR Admin | HR Staff | หัวหน้า/ทั่วไป | ระบบ/ปลายทาง |
|---|:---:|:---:|:---:|:---:|
| ดู list ทุก tab + ค้นหา/filter | ✅ | ✅ | ✅ (เฉพาะค่าที่ Active) | — |
| ดูค่าที่มีผล ณ วันที่ย้อนหลัง (as-of) | ✅ | ✅ | ❌ | — |
| ดู tab ประวัติเวอร์ชัน | ✅ | ✅ | ❌ | — |
| ดู tab "ใครใช้ค่านี้" (where-used) | ✅ | ✅ | ❌ | — |
| สร้างค่าใหม่ / บันทึกร่าง | ✅ | ❌ | ❌ | ❌ |
| แก้ค่า → สร้างเวอร์ชันใหม่ + ตั้ง `effective_date` | ✅ | ❌ | ❌ | ❌ |
| ยกเลิกเวอร์ชันที่รอมีผล | ✅ | ❌ | ❌ | ❌ |
| ปิดใช้ (soft archive) / เปิดใช้กลับ | ✅ | ❌ | ❌ | ❌ |
| สร้างงวดทั้งปี / ปิดงวด / เปิดงวดกลับ | ✅ | ❌ | ❌ | ❌ |
| ลบถาวร (hard delete) | ❌ **ไม่มีใครทำได้** | ❌ | ❌ | ❌ |
| อ่านค่าที่ Active ณ วันที่ (resolve) | ✅ | ✅ | ✅ | ✅ |
| เปลี่ยนสถานะเวอร์ชันตามเวลา | ❌ | ❌ | ❌ | ✅ (system) |

- สิทธิ์ทั้งหมดมาจาก **Roles & Permissions / Data Masking (Policy Center)** — feature นี้ไม่ทำ permission เอง [OB-15]
- Data classification ของค่า config = **INTERNAL** (ไม่มีข้อมูลรายบุคคล) แต่หน้าจอยังอยู่ใต้ Policy Center

---

# Section 5: User Journey (with COSO) ⭐

> **หมายเหตุ COSO ที่ต้องอ่านก่อน:** feature นี้ **ไม่มี approval step** ตาม scope note (OB-07 · S-23 · FN-40) — คอลัมน์ **Approver จึงเป็น "—" ทุกแถวโดยเจตนา** ไม่ใช่ข้อมูลขาด
> **Compensating control แทน Approver:** (1) `effective_date` บังคับ + สถานะ Draft→Scheduled ทำให้การเปลี่ยนไม่มีผลทันที (2) เหตุผลการเปลี่ยนบังคับ ≥10 ตัวอักษรตั้งแต่เวอร์ชันที่ 2 (3) audit append-only ทุก transition (4) where-used บังคับดูก่อนปิดใช้ (5) event CSQ SecC ทุกครั้งที่สิทธิ์พนักงานเปลี่ยน
> **SoD (PE02):** ไม่มีแถวใดที่ Maker = Approver เพราะไม่มี Approver — **ผ่านโดยไม่มีข้อยกเว้น** · ประเด็น "ควรมี approval ไหม" ถูกยกเป็น **OQ-STD-01** ไม่ตัดเงียบ (Lane Mode default จาก `coso-defaults.md` = ไม่มีชั้นอนุมัติสำหรับ config ที่ scope ตัด)

## 5.1 Happy Path — ตั้งค่าใหม่ให้มีผลวันข้างหน้า

| # | Step | หน้าจอ/ปุ่ม | Maker | Checker | Approver | System | trace |
|---|---|---|---|---|---|---|---|
| J-01 | เปิดเมนู "ตั้งค่า HR" → เลือก tab กลุ่มค่า | `#/hr-config/leave` (และ 5 tab อื่น) | HR Admin | — | — | โหลดค่าตามสิทธิ์ Policy Center · แสดง pill สถานะ + badge "รอมีผล" | S-01 · FN-90 |
| J-02 | กด **+ สร้างค่าใหม่** → drawer wizard ขั้น 1 "ข้อมูลค่า" | drawer 920px step 1 | HR Admin | — | — | auto-gen `code` จากชื่อ · default `company_scope`=ค่ากลาง · `applies_to`=ทั้งบริษัท (อ่านอย่างเดียว) | S-01 · FN-01,FN-30 |
| J-03 | ขั้น 2 "ค่าที่ใช้" — กรอก payload ตามกลุ่ม | step 2 | HR Admin | — | — | validate ต่อ field ตามกลุ่ม (BR-05,09,10,11,12,16,17) | S-05..S-15 |
| J-04 | ขั้น 3 "ตรวจสอบและยืนยัน" — กรอก **วันมีผล** + เหตุผล | step 3 | HR Admin | — | — | default `effective_date` = วันแรกของเดือนถัดไป · เช็ค BR-01,BR-03,BR-04 | S-01 · FN-01 |
| J-05 | กด **บันทึก + ตั้งวันมีผล** | ปุ่ม primary ล่างขวา | HR Admin | — | — | สร้าง `config_version` สถานะ **Scheduled** (หรือ Active ถ้าวันมีผล=วันนี้) · เขียน audit append-only · ยิง event **CSQ SecC** · disable ปุ่มกัน double-submit | S-01 · BR-01,BR-14 · FN-02,FN-92 |
| J-06 | ถึงวันมีผล | — (ไม่มีคนกด) | — | — | — | **System**: Scheduled→Active · เวอร์ชันเดิม→Superseded · set `effective_to` = วันมีผลใหม่ − 1 · เขียน audit · ยิง event CSQ SecC | S-01,S-02 · BR-02 |
| J-07 | feature ปลายทางขอค่าพร้อมวันที่ | (API — ไม่มีหน้าจอ) | — | — | — | **System**: resolve ตาม BR-13 (บริษัทลูก → ค่ากลาง) แล้วคืนเวอร์ชันที่ Active ณ วันนั้น · Draft/Scheduled ไม่ถูกส่ง (BR-19) | S-18,S-19 · FN-03 |

## 5.2 Alternative Paths

### 5.2.1 บันทึกร่าง (Draft)
| # | Step | Maker | Checker | Approver | System | trace |
|---|---|---|---|---|---|---|
| A1-1 | กรอกไม่ครบ → กด "บันทึกร่าง" | HR Admin | — | — | บันทึกสถานะ **Draft** โดยไม่ต้องมี `effective_date` · ไม่ขึ้น where-used · ไม่ส่งปลายทาง | S-03 · BR-19 · FN-06 |

### 5.2.2 แก้ค่าที่ใช้อยู่ → สร้างเวอร์ชันใหม่
| # | Step | Maker | Checker | Approver | System | trace |
|---|---|---|---|---|---|---|
| A2-1 | กด "แก้ไข" บนค่าที่ Active | HR Admin | — | — | เปิดฟอร์ม **สร้างเวอร์ชันใหม่** (copy payload เดิม) — ไม่เขียนทับ | S-02 · BR-02 · FN-04 |
| A2-2 | กรอกเหตุผลการเปลี่ยน (≥10 ตัวอักษร) + วันมีผลใหม่ | HR Admin | — | — | บังคับเหตุผลตั้งแต่เวอร์ชันที่ 2 · เวอร์ชันเก่าเป็น Superseded เมื่อถึงวัน | S-02 · BR-03 · FN-05 |

### 5.2.3 ยกเลิกเวอร์ชันที่รอมีผล
| # | Step | Maker | Checker | Approver | System | trace |
|---|---|---|---|---|---|---|
| A3-1 | กด "ยกเลิกเวอร์ชันที่รอมีผล" + กรอกเหตุผล | HR Admin | — | — | ยกเลิกได้ก่อนถึงวันเท่านั้น · ปุ่มหายเมื่อ Active แล้ว · ค่า Active เดิมใช้ต่อ · audit | S-04 · BR-20 · FN-07 |

### 5.2.4 ปิดใช้ (soft archive) พร้อมดูผลกระทบ
| # | Step | Maker | Checker | Approver | System | trace |
|---|---|---|---|---|---|---|
| A4-1 | กด "ปิดใช้" บนแถว | HR Admin | — | — | เช็ค where-used ก่อน → modal แสดงรายการ feature ที่อ้างอยู่ | S-19 · BR-08 · FN-26 |
| A4-2 | อ่านรายการผลกระทบ + กรอกเหตุผล → ยืนยัน | HR Admin | — | — | สถานะ **Inactive** · เลือกใหม่ไม่ได้ · ของเดิมยังอ่านได้ · **ไม่มีปุ่มลบ** · audit + event CSQ SecC | S-18 · BR-07 · FN-24,FN-25 |

### 5.2.5 เปิดใช้กลับ
| # | Step | Maker | Checker | Approver | System | trace |
|---|---|---|---|---|---|---|
| A5-1 | กด "เปิดใช้กลับ" บนค่าที่ปิดใช้ | HR Admin | — | — | สร้าง**เวอร์ชันใหม่**พร้อมวันมีผล (ไม่ revert ของเดิม) · audit | S-18 · FN-25 |

### 5.2.6 สร้างงวดจริงทั้งปี + ปิด/เปิดงวด
| # | Step | Maker | Checker | Approver | System | trace |
|---|---|---|---|---|---|---|
| A6-1 | tab รอบเวลา/รอบจ่าย → กด "สร้างงวดทั้งปี" | HR Admin | — | — | สร้างแถวงวดครบทั้งปีจากกติกา (วันเริ่ม–จบ · วันจ่าย · สถานะ เปิด) | S-31 · BR-21 · FN-48 |
| A6-2 | ปิดงวดที่จ่ายแล้ว (confirm) | HR Admin | — | — | สถานะงวด = ปิด → เป็นฐานของ BR-04 · บันทึกผู้ปิด/วันที่ปิด · audit | S-31 · BR-21 |
| A6-3 | เปิดงวดกลับ (ต้องมีเหตุผล) | HR Admin | — | — | บังคับเหตุผล + audit (append-only) | S-31 · BR-21 |

### 5.2.7 ดูประวัติ + ดูค่าที่มีผล ณ วันที่
| # | Step | Maker | Checker | Approver | System | trace |
|---|---|---|---|---|---|---|
| A7-1 | เปิด view drawer → tab "ประวัติเวอร์ชัน" | HR Admin / HR Staff | — | — | timeline ค่าเก่า→ใหม่ · ผู้แก้ไข · เมื่อไร · เหตุผล (read-only · append-only) | S-20 · BR-14 · FN-27 |
| A7-2 | ตั้งตัวกรอง "มีผล ณ วันที่ …" | HR Admin / HR Staff | — | — | list เปลี่ยนเป็นค่าที่ Active ณ วันนั้น + badge "กำลังดูย้อนหลัง" | S-20 · FN-28 |
| A7-3 | เปิด tab "ใครใช้ค่านี้" | HR Admin / HR Staff | — | — | list 8 feature ปลายทาง + สถานะ ⏳/✅ + ลิงก์ (soft ref — **ห้าม CRUD**) | S-19 · FN-33 |

## 5.3 Exception Paths (ทุกข้อมี Business Rule คู่)

| # | เหตุการณ์ | ผลลัพธ์ | Maker | System | trace |
|---|---|---|---|---|---|
| E-01 | ตัวคูณ OT ต่ำกว่าขั้นต่ำกฎหมาย (เช่น 1.2x สำหรับ OT วันทำงาน) | **บล็อก** + บอกขั้นต่ำ 1.5 เท่า | HR Admin | validate ค้างที่ขั้น 2 | S-09 · BR-05 · FN-13 |
| E-02 | ตั้ง `effective_date` ย้อนเข้างวดที่ปิดแล้ว | **บล็อก** + บอกวันที่เร็วที่สุดที่ตั้งได้ | HR Admin | อ้างงวดที่ status=ปิด | S-14 · BR-04,BR-21 · FN-19 |
| E-03 | เพิ่มวันหยุดซ้ำวันเดิมใน บริษัท+ปี เดียวกัน | **บล็อก** + ชี้รายการเดิม | HR Admin | ตรวจซ้ำทั้งภายในชุดและข้ามชุด | S-12 · BR-09 · FN-17 |
| E-04 | รอบประเมินทับซ้อนรอบเดิมในปีเดียวกัน | **บล็อก** + แสดงชื่อรอบที่ชน | HR Admin | ตรวจ overlap ช่วงวัน | S-16 · BR-10 · FN-21 |
| E-05 | วันตัดเวลา > วันจ่าย ในงวดเดียวกัน | **บล็อก** | HR Admin | เทียบวันในงวด | S-13 · BR-11 · FN-18 |
| E-06 | ขั้นอายุงาน (milestone) ทับซ้อน/มีช่องว่าง | **บล็อก** + ชี้ช่วงที่ขาดหรือชน | HR Admin | ตรวจความต่อเนื่องของช่วง | S-05 · BR-16 · FN-08 |
| E-07 | กะเวลาออก ≤ เวลาเข้า โดยไม่ติ๊ก "ข้ามวัน" หรือช่วงพักอยู่นอกช่วงกะ | **บล็อก** | HR Admin | คำนวณ ชม./วัน ใหม่ทุกครั้ง | S-10 · BR-17 · FN-14 |
| E-08 | ยกยอด > 0 แต่ไม่ระบุวันหมดอายุยกยอด | **บล็อก** | HR Admin | เช็คคู่ field | S-06 · BR-12 · FN-09 |
| E-09 | โควตาลาพักร้อน < 6 วัน/ปี (พนักงานอายุงานครบ 1 ปี) | **เตือน ไม่บล็อก** — ให้ยืนยันต่อได้ | HR Admin | modal เตือน "ต่ำกว่าขั้นต่ำตามกฎหมาย" | S-01 · BR-06 · FN-32 |
| E-10 | `effective_date` ซ้ำ/คร่อมกับเวอร์ชันอื่นของค่าเดียวกัน + บริษัทเดียวกัน | **บล็อก** + แสดงเวอร์ชันที่ชน | HR Admin | ตรวจ overlap ของช่วง effective | S-02 · BR-03 · FN-05 |
| E-11 | ประเภทลาที่ "จ่ายค่าจ้าง" แต่ไม่ระบุ `payroll_code` | **เตือนเบา ไม่บล็อก** (soft ref nullable) | HR Admin | hint ที่ field | S-08,S-25 · BR-18 · FN-12 |

## 5.4 Process Diagram

```
                    ┌─────────────────────────────────────────┐
                    │  HR Admin — ตั้งค่า HR (1 เมนูซ้าย)       │
                    │  6 tab: ลา · OT/กะ · ปฏิทิน · รอบเวลา/จ่าย │
                    │         · รอบประเมิน · ขอบเขตบริษัท        │
                    └───────────────┬─────────────────────────┘
                                    │ + สร้างค่าใหม่ / แก้ไข
                                    ▼
                 ┌──────────────────────────────────────┐
                 │ drawer wizard 3 ขั้น                  │
                 │ 1 ข้อมูลค่า › 2 ค่าที่ใช้ › 3 ตรวจสอบฯ  │
                 │ ขั้น 3 บังคับ effective_date + เหตุผล   │
                 └──────────────┬───────────────────────┘
                     validate BR-01,03,04,05,09,10,11,12,16,17
                                │ ผ่าน                    │ ไม่ผ่าน
                                ▼                         ▼
                    ┌───────────────────┐        ┌──────────────────┐
                    │ config_version    │        │ บล็อก + ชี้ field  │
                    │ Scheduled/Active  │        │ (E-01..E-10)     │
                    └─────────┬─────────┘        └──────────────────┘
              audit append-only │ + event CSQ SecC
                                ▼
              ┌─────────────────────────────────────┐
              │ System: ถึงวันมีผล → Active           │
              │         เวอร์ชันเดิม → Superseded     │
              └─────────────────┬───────────────────┘
                                ▼  resolve(date, company) — BR-13
   ┌───────────────────────────────────────────────────────────────────┐
   │ 8 feature ปลายทาง (อ่านอย่างเดียว · soft ref LD-4C-02)              │
   │ Leave · OT/Shift · Shift&Roster · Attendance · Payroll ·          │
   │ Performance · Welfare · Salary Structure                          │
   └───────────────────────────────────────────────────────────────────┘
```

---

# Section 6: Data Entity & Fields

## 6.1 Entity Overview

> **หลักการโครงสร้าง (รูปธรรมของ HR-1 · OB-01):** ข้อมูลเป็น **2 ชั้นเสมอ** — `hr_config_item` (ตัวค่า: ชื่อ/รหัส/กลุ่ม/ขอบเขตบริษัท) + `hr_config_version` (เวอร์ชันของค่านั้น: `effective_date` + payload จริง) · payload แยกตารางตามกลุ่มค่า

| # | Entity | ชนิด | คำอธิบาย |
|---|---|---|---|
| E-01 | `hr_config_item` | Header (master) | ตัวค่า 1 ตัว — ไม่เก็บค่าจริง เก็บแค่ identity + ขอบเขต |
| E-02 | `hr_config_version` | Version | เวอร์ชันของค่า — **หัวใจ HR-1** · ทุก item มี ≥1 version |
| E-03 | `hr_leave_policy` | Payload (กลุ่ม ก) | กติกาประเภทการลา |
| E-04 | `hr_leave_milestone` | Payload line (กลุ่ม ก) | ขั้นโควตาตามอายุงาน (1:N ของ E-03) |
| E-05 | `hr_ot_rate` | Payload (กลุ่ม ข) | อัตรา OT / อัตราวันหยุด |
| E-06 | `hr_shift_pattern` | Payload (กลุ่ม ข) | กะมาตรฐาน |
| E-07 | `hr_shift_break` | Payload line (กลุ่ม ข) | ช่วงพักของกะ (1:N ของ E-06) |
| E-08 | `hr_holiday_calendar` | Payload (กลุ่ม ค) | ชุดปฏิทินวันหยุด (ปี + `location`) |
| E-09 | `hr_holiday_day` | Payload line (กลุ่ม ค) | วันหยุดรายวัน (1:N ของ E-08) |
| E-10 | `hr_period_rule` | Payload (กลุ่ม ง) | กติการอบตัดเวลา/รอบจ่าย |
| E-11 | `hr_pay_period` | Payload line (กลุ่ม ง) | **งวดจริง** ที่สร้างจากกติกา (1:N ของ E-10) — นิยามของ "งวดที่ปิดแล้ว" |
| E-12 | `hr_appraisal_cycle` | Payload (กลุ่ม จ) | รอบประเมิน |
| E-13 | `hr_config_usage` | Soft-ref registry | ทะเบียน where-used — feature ปลายทางที่อ้างค่านี้ (display-only) |

**Audit Fields — ทุก entity (E-01…E-13) มีครบ 4 ช่องนี้เสมอ:**
`created_by` (soft ref Employee Master) · `created_date` · `modified_by` (soft ref Employee Master) · `modified_date`
> ไม่มี `deleted_at` / hard delete ที่ entity ใด — การเลิกใช้ทำผ่าน `status` เท่านั้น (BR-07 · LOCK audit append-only)
> **audit trail จริงเขียนที่ Policy Center Audit Trail** (append-only) — feature นี้ไม่มีตาราง audit ของตัวเอง [OB-15]

## 6.2 Entity: `hr_config_item` (Header)

| # | Field Name | Label UI | Input Type | ค่า/ตัวเลือก | จำเป็น | เงื่อนไข | หมายเหตุ |
|---|---|---|---|---|:---:|---|---|
| 1 | `id` | — | AUTO | uuid | ✅ | — | PK |
| 2 | `code` | รหัสค่า | TEXT | ตัวพิมพ์ใหญ่+ตัวเลข | ✅ | ไม่ซ้ำภายใน `group` + `company_scope` | auto-gen จากชื่อ แก้ได้ |
| 3 | `name_th` | ชื่อค่า (ไทย) | TEXT | ≤80 ตัวอักษร | ✅ | — | — |
| 4 | `name_en` | ชื่อค่า (EN) | TEXT | — | ⬜ | — | `[AI-DRAFT]` |
| 5 | `group` | กลุ่มค่า | DROPDOWN-SINGLE | ประเภทการลา · อัตรา OT/กะ · ปฏิทินวันหยุด · รอบเวลา/รอบจ่าย · รอบประเมิน | ✅ | default = tab ที่เปิด · แก้ไม่ได้หลังสร้าง | ตรึงกลุ่มค่าไว้ 5 กลุ่ม (กลุ่มที่ 6 "ขอบเขตบริษัท" เป็นมุมมองข้ามกลุ่ม ไม่ใช่ group ใหม่) |
| 6 | `company_scope` | ขอบเขตบริษัท | DROPDOWN-SINGLE | `shared` (ค่ากลาง) · `company` (เฉพาะบริษัท) | ✅ | default `shared` | BR-13 |
| 7 | `companies[]` | บริษัท | LOOKUP (multi · soft ref Organization) | รายชื่อบริษัทลูก | ⬜ / ✅ เมื่อ `company_scope=company` | nullable · **ไม่มี FK cascade** | LD-4C-02 |
| 8 | `applies_to` | ขอบเขตการใช้ | TEXT (read-only) | "ทั้งบริษัท" | ✅ | รอบนี้แก้ไม่ได้ — hook | S-22 · OQ-STD-02 |
| 9 | `payroll_code` | รหัสอ้างอิงจ่ายเงิน | TEXT (soft ref) | — | ⬜ | display-only ที่ปลายทาง · **ไม่ผูกสูตร** | BR-18 · OQ-STD-03 |
| 10 | `status` | สถานะการใช้งาน | DROPDOWN-SINGLE | `active` (ใช้งาน) · `inactive` (ปิดใช้) | ✅ | เปลี่ยนได้ทางเดียวผ่าน confirm | BR-07 |
| 11 | `deactivate_reason` | เหตุผลการปิดใช้ | TEXTAREA | ≥10 ตัวอักษร | ✅ เมื่อ `status=inactive` | — | BR-08 |
| 12 | `owner_employee_id` | ผู้รับผิดชอบ | LOOKUP (combobox Employee Master) | avatar → ชื่อ → ตำแหน่ง · แผนก | ✅ | #102 anatomy | BR-15 |
| 13 | `note` | หมายเหตุ | TEXTAREA | — | ⬜ | — | `[AI-DRAFT]` |
| 14–17 | audit fields | — | AUTO | `created_by/date` · `modified_by/date` | ✅ | — | ทุก entity |

## 6.3 Entity: `hr_config_version` (หัวใจ HR-1)

| # | Field Name | Label UI | Input Type | ค่า/ตัวเลือก | จำเป็น | เงื่อนไข | หมายเหตุ |
|---|---|---|---|---|:---:|---|---|
| 1 | `id` | — | AUTO | uuid | ✅ | — | PK |
| 2 | `config_item_id` | — | AUTO | FK → `hr_config_item` | ✅ | — | 1:N |
| 3 | `version_no` | เวอร์ชันที่ | AUTO | 1,2,3… | ✅ | นับต่อ item | — |
| 4 | **`effective_date`** | **วันมีผล** | DATE | — | ✅ **เสมอ** (ยกเว้น Draft) | ห้ามซ้อนช่วงกับเวอร์ชันอื่นของ item+company เดียวกัน (BR-03) · ห้ามย้อนเข้างวดที่ปิด (BR-04) | **HR-1** |
| 5 | `effective_to` | วันสิ้นสุดผล | AUTO (computed) | — | — | = `effective_date` ของเวอร์ชันถัดไป − 1 วัน · null = ยังมีผลอยู่ | S-20 |
| 6 | `status` | สถานะเวอร์ชัน | DROPDOWN-SINGLE | `draft` · `scheduled` · `active` · `superseded` · `inactive` | ✅ | เปลี่ยนตาม §8 เท่านั้น | OB-11 · 5 states |
| 7 | `change_reason` | เหตุผลการเปลี่ยน | TEXTAREA | ≥10 ตัวอักษร | ✅ เมื่อ `version_no ≥ 2` | — | S-02 · `[AI-DRAFT]` |
| 8 | `cancel_reason` | เหตุผลการยกเลิก | TEXTAREA | ≥10 ตัวอักษร | ✅ เมื่อยกเลิกเวอร์ชัน Scheduled | — | BR-20 |
| 9 | `payload_ref` | — | AUTO | FK → payload entity ตาม `group` | ✅ | 1:1 | §6.4–6.8 |
| 10–13 | audit fields | — | AUTO | ครบ 4 ช่อง | ✅ | — | — |

## 6.4 Payload กลุ่ม ก — `hr_leave_policy` + `hr_leave_milestone`

**`hr_leave_policy`**

| # | Field | Label UI | Input Type | ค่า/ตัวเลือก | จำเป็น | เงื่อนไข |
|---|---|---|---|---|:---:|---|
| 1 | `unit` | หน่วยนับ | DROPDOWN-SINGLE | วัน · ชั่วโมง | ✅ | — |
| 2 | `paid_type` | จ่ายค่าจ้าง | DROPDOWN-SINGLE | จ่าย · ไม่จ่าย · จ่ายบางส่วน | ✅ | — |
| 3 | `paid_pct` | เปอร์เซ็นต์ที่จ่าย | NUMBER | 1–99 | ✅ เมื่อ `paid_type=จ่ายบางส่วน` | — |
| 4 | `quota_per_year` | โควตาต่อปี | NUMBER | ≥0 | ✅ | 0 = ไม่จำกัด ต้องติ๊ก `unlimited` · <6 (ลาพักร้อน) → **เตือน** BR-06 |
| 5 | `unlimited` | ไม่จำกัด | TOGGLE | — | ⬜ | — |
| 6 | `grant_frequency` | ความถี่การให้สิทธิ์ | DROPDOWN-SINGLE | ต้นปี · รายเดือนสะสม · ตามอายุงาน | ✅ | — |
| 7 | `prorate` | prorate พนักงานเข้าใหม่ | DROPDOWN-SINGLE | ตามเดือน · ตามวัน · ไม่ prorate | ✅ | — |
| 8 | `rounding` | วิธีปัดเศษ | DROPDOWN-SINGLE | ขึ้น · ลง · ครึ่งวันใกล้สุด | ✅ | — |
| 9 | `carry_max` | ยกยอดสูงสุด | NUMBER | ≥0 | ✅ | BR-12 |
| 10 | `carry_expiry` | วันหมดอายุยกยอด | DATE (วัน/เดือน) | — | ✅ เมื่อ `carry_max>0` | ต้องอยู่ในปีถัดไป (BR-12) |
| 11 | `need_doc` | ต้องแนบเอกสาร | TOGGLE | — | ✅ | — |
| 12 | `doc_note` | เงื่อนไขเอกสาร | TEXT | — | ✅ เมื่อ `need_doc=true` | เช่น "ลาป่วย >3 วัน ต้องมีใบรับรองแพทย์" |
| 13 | `advance_days` | ลาล่วงหน้ากี่วัน | NUMBER | ≥0 | ⬜ | — |
| 14 | `max_consecutive` | ลาต่อเนื่องสูงสุด/ครั้ง | NUMBER | ≥0 · 0 = ไม่จำกัด | ⬜ | `[STD]` `[AI-DRAFT]` (G-07) |
| 15 | `negative_limit` | ติดลบได้ถึง | NUMBER | ≥0 · default 0 | ⬜ | `[STD]` Odoo |
| 16 | `count_holiday` | นับวันหยุดในช่วงลา | TOGGLE | default = ไม่นับ | ✅ | S-21 |
| 17 | `half_day` | อนุญาตครึ่งวัน | TOGGLE | — | ✅ | S-21 |
| 18–21 | audit fields | — | AUTO | ครบ 4 ช่อง | ✅ | — |

**`hr_leave_milestone`** (1:N)

| # | Field | Label UI | Input Type | จำเป็น | เงื่อนไข |
|---|---|---|---|:---:|---|
| 1 | `seq` | ลำดับ | AUTO | ✅ | — |
| 2 | `year_from` | อายุงานจาก (ปี) | NUMBER | ✅ | ช่วงต่อเนื่อง **ไม่ทับซ้อน ไม่มีช่องว่าง** (BR-16) |
| 3 | `year_to` | อายุงานถึง (ปี) | NUMBER | ✅ | null = ขึ้นไป |
| 4 | `days` | จำนวนวัน | NUMBER | ✅ | ≥0 |
| 5–8 | audit fields | — | AUTO | ✅ | — |

## 6.5 Payload กลุ่ม ข — `hr_ot_rate` · `hr_shift_pattern` · `hr_shift_break`

**`hr_ot_rate`**

| # | Field | Label UI | Input Type | ค่า/ตัวเลือก | จำเป็น | เงื่อนไข |
|---|---|---|---|---|:---:|---|
| 1 | `rate_type` | ประเภทอัตรา | DROPDOWN-SINGLE | OT วันทำงาน · ทำงานวันหยุด · OT วันหยุด | ✅ | — |
| 2 | `multiplier` | ตัวคูณ (x) | NUMBER (decimal) | — | ✅ | **≥ ขั้นต่ำกฎหมาย** 1.5 / 1.0 / 3.0 ตามประเภท (BR-05) |
| 3 | `base` | ฐานคำนวณ | DROPDOWN-SINGLE | ค่าจ้างรายชั่วโมง · รายวัน | ✅ | — |
| 4 | `cap_hours_week` | เพดานชั่วโมง/สัปดาห์ | NUMBER | default 36 | ✅ | >0 `[STD]` |
| 5–8 | audit fields | — | AUTO | — | ✅ | — |

**`hr_shift_pattern`**

| # | Field | Label UI | Input Type | จำเป็น | เงื่อนไข |
|---|---|---|---|:---:|---|
| 1 | `shift_name` | ชื่อกะ | TEXT | ✅ | ไม่ซ้ำในบริษัท |
| 2 | `time_in` | เวลาเข้า | DATETIME (time) | ✅ | — |
| 3 | `time_out` | เวลาออก | DATETIME (time) | ✅ | ต้อง > `time_in` เว้นแต่ `overnight=true` (BR-17) |
| 4 | `overnight` | ข้ามวัน | TOGGLE | ✅ | — |
| 5 | `hours_per_day` | ชั่วโมงทำงาน/วัน | AUTO (computed) | — | = (ออก − เข้า) − พัก |
| 6 | `workdays[]` | วันทำงานในสัปดาห์ | DROPDOWN-MULTI (จ–อา) | ✅ | ≥1 วัน |
| 7–10 | audit fields | — | AUTO | ✅ | — |

**`hr_shift_break`** (1:N) — `break_from` · `break_to` (ต้องอยู่ในช่วงกะ · BR-17) + audit fields

## 6.6 Payload กลุ่ม ค — `hr_holiday_calendar` + `hr_holiday_day`

**`hr_holiday_calendar`**

| # | Field | Label UI | Input Type | จำเป็น | เงื่อนไข |
|---|---|---|---|:---:|---|
| 1 | `calendar_name` | ชื่อชุดปฏิทิน | TEXT | ✅ | — |
| 2 | `year` | ปี | NUMBER | ✅ | — |
| 3 | `location` | ชุดปฏิทิน / สถานที่ | TEXT (soft ref · nullable) | ⬜ | แยกชุดตามสาขา/โรงงาน `[STD]` `[AI-DRAFT]` (S-32) |
| 4–7 | audit fields | — | AUTO | ✅ | — |

**`hr_holiday_day`** (1:N)

| # | Field | Label UI | Input Type | จำเป็น | เงื่อนไข |
|---|---|---|---|:---:|---|
| 1 | `holiday_date` | วันที่ | DATE | ✅ | **ไม่ซ้ำใน บริษัท+ปี** (BR-09) — ตรวจทั้งในชุดและข้ามชุด |
| 2 | `holiday_name` | ชื่อวันหยุด | TEXT | ✅ | — |
| 3 | `holiday_type` | ประเภท | DROPDOWN-SINGLE | ✅ | วันหยุดราชการ · วันหยุดบริษัท · วันหยุดชดเชย |
| 4 | `source_date` | วันหยุดต้นทาง | DATE | ✅ เมื่อ `holiday_type=ชดเชย` | ต้องเป็นวันหยุดที่มีอยู่แล้ว |
| 5 | `shifts[]` | กะที่ได้รับผล | DROPDOWN-MULTI | ⬜ | default = ทุกกะ |
| 6–9 | audit fields | — | AUTO | ✅ | — |

## 6.7 Payload กลุ่ม ง — `hr_period_rule` + `hr_pay_period`

**`hr_period_rule`**

| # | Field | Label UI | Input Type | จำเป็น | เงื่อนไข |
|---|---|---|---|:---:|---|
| 1 | `frequency` | ความถี่ | DROPDOWN-SINGLE | ✅ | รายเดือน · ครึ่งเดือน |
| 2 | `cut_day` | วันตัดเวลา | NUMBER (1–31 หรือ "สิ้นเดือน") | ✅ | ≤ `pay_day` ในงวดเดียวกัน (BR-11) |
| 3 | `pay_day` | วันจ่าย | NUMBER (1–31 หรือ "สิ้นเดือน") | ✅ | — |
| 4 | `lock_closed_period` | ล็อกงวดที่ปิดแล้ว | TOGGLE | ✅ | default = ล็อก (บังคับ BR-04) |
| 5 | `work_period_frequency` | ความถี่รอบบันทึกเวลา | DROPDOWN-SINGLE | ✅ | ใช้รอบเดียวกับรอบจ่าย (default) · รายสัปดาห์ · รายปักษ์ `[STD]` `[AI-DRAFT]` (G-03) |
| 6–9 | audit fields | — | AUTO | ✅ | — |

**`hr_pay_period`** (1:N) — **นิยามของ "งวดที่ปิดแล้ว" ที่ BR-04 อ้างถึง**

| # | Field | Label UI | Input Type | จำเป็น | เงื่อนไข |
|---|---|---|---|:---:|---|
| 1 | `period_code` | งวด | AUTO | ✅ | เช่น `2569-09` |
| 2 | `date_from` / `date_to` | วันเริ่ม – วันจบ | DATE × 2 | ✅ | สร้างจากกติกา (S-31) |
| 3 | `pay_date` | วันจ่าย | DATE | ✅ | — |
| 4 | `period_status` | สถานะงวด | DROPDOWN-SINGLE | ✅ | `open` (เปิด) · `closed` (ปิด) |
| 5 | `closed_by` | ผู้ปิดงวด | LOOKUP (Employee Master) | ✅ เมื่อ `closed` | #102 |
| 6 | `closed_at` | วันที่ปิดงวด | DATETIME | ✅ เมื่อ `closed` | — |
| 7 | `reopen_reason` | เหตุผลการเปิดงวดกลับ | TEXTAREA | ✅ เมื่อเปิดกลับ | ≥10 ตัวอักษร + audit (BR-21) |
| 8–11 | audit fields | — | AUTO | ✅ | — |

## 6.8 Payload กลุ่ม จ — `hr_appraisal_cycle`

| # | Field | Label UI | Input Type | จำเป็น | เงื่อนไข |
|---|---|---|---|:---:|---|
| 1 | `cycle_name` | ชื่อรอบ | TEXT | ✅ | — |
| 2 | `year` | ปี | NUMBER | ✅ | — |
| 3 | `period_from` / `period_to` | ช่วงประเมิน | DATE × 2 | ✅ | **ไม่ทับซ้อนรอบอื่นในปีเดียวกัน** (BR-10) |
| 4 | `entry_from` / `entry_to` | ช่วงเปิดกรอก | DATE × 2 | ✅ | อยู่หลังหรือคร่อมช่วงประเมิน |
| 5 | `frequency` | ความถี่ | DROPDOWN-SINGLE | ✅ | ปีละ 1 · ปีละ 2 · รายไตรมาส |
| 6–9 | audit fields | — | AUTO | ✅ | — |

## 6.9 Entity: `hr_config_usage` (where-used registry · soft ref)

| # | Field | Label UI | Input Type | จำเป็น | หมายเหตุ |
|---|---|---|---|:---:|---|
| 1 | `config_item_id` | — | AUTO (FK) | ✅ | — |
| 2 | `consumer_feature` | feature ปลายทาง | TEXT | ✅ | 8 ตัว: Leave · OT/Shift · Shift&Roster · Attendance · Payroll · Performance · Welfare · Salary Structure |
| 3 | `link_status` | สถานะการเชื่อม | DROPDOWN-SINGLE | ✅ | `ready` (✅ พร้อมใช้) · `pending` (⏳ ยังไม่ทำ) — **Module Linkage + manual override** [OB-14] |
| 4 | `usage_note` | ใช้ค่าอะไร | TEXT | ⬜ | เช่น "ประเภทลา + กติกานับวัน" |
| 5 | `deeplink` | ลิงก์ไป feature | TEXT | ⬜ | กดไปได้ · **ห้าม CRUD ปลายทาง** (LD-4C-02) |
| 6–9 | audit fields | — | AUTO | ✅ | — |

## 6.10 Entity Relationship

```
Organization (master ✅) ──(soft ref · nullable · no cascade)──▶ hr_config_item.companies[]
Employee Master (master ✅) ──(soft ref · combobox #102)──────▶ hr_config_item.owner_employee_id
                                                              └▶ audit fields ทุก entity
                                                              └▶ hr_pay_period.closed_by

hr_config_item ──(1:N)──▶ hr_config_version ──(1:1 ตาม group)──▶ hr_leave_policy ──(1:N)──▶ hr_leave_milestone
                                              │                └▶ hr_ot_rate
                                              │                └▶ hr_shift_pattern ──(1:N)──▶ hr_shift_break
                                              │                └▶ hr_holiday_calendar ──(1:N)──▶ hr_holiday_day
                                              │                └▶ hr_period_rule ──(1:N)──▶ hr_pay_period
                                              └────────────────└▶ hr_appraisal_cycle

hr_config_item ──(1:N)──▶ hr_config_usage ──(soft ref · display-only)──▶ 8 feature ปลายทาง (⏳/✅)

Policy Center Audit Trail ◀──(append-only write ทุก transition)── hr_config_version
ENG-CSQ 7C (SecC) ◀──(event: publish · activate · cancel · deactivate · reactivate · close-period)── hr_config_version
```

| ความสัมพันธ์ | ประเภท | FK | ทิศทาง | หมายเหตุ |
|---|---|---|---|---|
| `hr_config_item` → `hr_config_version` | 1:N | `config_item_id` | เจ้าของ | ลบ item ไม่ได้ (ไม่มี hard delete) |
| `hr_config_version` → payload entity | 1:1 | `payload_ref` | เจ้าของ | เลือกตาราง payload ตาม `group` |
| `hr_leave_policy` → `hr_leave_milestone` | 1:N | `leave_policy_id` | เจ้าของ | BR-16 ตรวจความต่อเนื่อง |
| `hr_period_rule` → `hr_pay_period` | 1:N | `period_rule_id` | เจ้าของ | งวดที่ `closed` เป็นฐานของ BR-04 |
| `hr_config_item` → Organization | N:M | **soft ref** | อ่านอย่างเดียว | nullable · ไม่มี cascade (LD-4C-02) |
| `hr_config_item` → Employee Master | N:1 | **soft ref** | อ่านอย่างเดียว | combobox #102 |
| `hr_config_item` → `hr_config_usage` | 1:N | `config_item_id` | อ่าน + Module Linkage | ห้าม CRUD ปลายทาง |

---

# Section 7: User Stories & Acceptance Criteria

> กติกา: description ของทุก Story เป็น **single action** — ไม่มีคำว่า "และ" (C05) · ทุก Story มี AC ≥2 ข้อ แบบ Given-When-Then (C06)

## Story ST-01: ตั้งวันมีผลให้ทุกค่าที่สร้าง
**ในฐานะ** HR Admin **ฉันต้องการ** ระบุวันมีผลของค่าทุกครั้งที่บันทึก **เพื่อ** ให้ตอบได้เสมอว่าช่วงไหนบริษัทใช้กติกาอะไร
### Acceptance Criteria
- **AC-01.1** Given อยู่ขั้น "ตรวจสอบและยืนยัน" ของ drawer สร้างค่า · When เว้นช่อง "วันมีผล" ว่างแล้วกดบันทึก · Then ระบบบล็อกพร้อมชี้ไปที่ช่องวันมีผล
- **AC-01.2** Given กรอกวันมีผลเป็นวันในอนาคต · When กดบันทึก · Then เวอร์ชันถูกสร้างสถานะ "รอมีผล" พร้อม badge วันที่บนแถว list
> trace: S-01 · BR-01 · **FN-01, FN-02**

## Story ST-02: กันไม่ให้ค่าที่รอมีผลรั่วไปถึงปลายทาง
**ในฐานะ** ระบบ **ฉันต้องการ** ส่งเฉพาะเวอร์ชันที่ Active ให้ feature ปลายทาง **เพื่อ** ป้องกันการใช้นโยบายก่อนวันที่มีผล
### Acceptance Criteria
- **AC-02.1** Given มีเวอร์ชันสถานะ Draft ของค่าหนึ่ง · When feature ปลายทางขอค่า ณ วันนี้ · Then ระบบคืนเฉพาะเวอร์ชัน Active ไม่คืน Draft
- **AC-02.2** Given มีเวอร์ชัน Scheduled ที่ยังไม่ถึงวัน · When เปิด tab "ใครใช้ค่านี้" · Then ส่วน "เวอร์ชันที่ปลายทางอ่านอยู่ตอนนี้" แสดงเวอร์ชัน Active เท่านั้น
> trace: S-01,S-03 · BR-19 · **FN-03, FN-06**

## Story ST-03: แก้ค่าที่ใช้อยู่โดยไม่ทับของเดิม
**ในฐานะ** HR Admin **ฉันต้องการ** ให้การแก้ค่าที่ Active กลายเป็นการสร้างเวอร์ชันใหม่ **เพื่อ** รักษาหลักฐานของกติกาเดิมไว้
### Acceptance Criteria
- **AC-03.1** Given ค่าหนึ่งมีเวอร์ชันสถานะ Active · When กดปุ่ม "แก้ไข" · Then ระบบเปิดฟอร์มสร้างเวอร์ชันใหม่ที่ copy ค่าเดิมมาให้ ไม่ใช่ฟอร์มแก้ทับ
- **AC-03.2** Given กำลังสร้างเวอร์ชันที่ 2 ขึ้นไป · When กรอกเหตุผลการเปลี่ยนน้อยกว่า 10 ตัวอักษร · Then ระบบบล็อกการบันทึก
- **AC-03.3** Given เวอร์ชันใหม่ถึงวันมีผล · When ระบบประมวลผล · Then เวอร์ชันเดิมเปลี่ยนเป็น "ถูกแทน" โดยยังเปิดอ่านได้
> trace: S-02 · BR-02, BR-03 · **FN-04, FN-05**

## Story ST-04: ยกเลิกเวอร์ชันที่ยังไม่ถึงวันมีผล
**ในฐานะ** HR Admin **ฉันต้องการ** ยกเลิกเวอร์ชันที่รอมีผลได้ก่อนถึงวัน **เพื่อ** แก้ความผิดพลาดโดยไม่กระทบค่าที่ใช้อยู่
### Acceptance Criteria
- **AC-04.1** Given เวอร์ชันสถานะ "รอมีผล" · When กดยกเลิกแล้วกรอกเหตุผล · Then เวอร์ชันถูกยกเลิกโดยค่าที่ Active เดิมยังใช้ต่อ
- **AC-04.2** Given เวอร์ชันเปลี่ยนเป็น Active แล้ว · When เปิดแถวนั้น · Then ปุ่ม "ยกเลิกเวอร์ชันที่รอมีผล" ไม่ปรากฏ
> trace: S-04 · BR-20 · **FN-07**

## Story ST-05: ย้อนดูกติกาที่ใช้ ณ วันที่ต้องการ
**ในฐานะ** HR Staff **ฉันต้องการ** ดูค่าที่มีผล ณ วันที่ที่เลือก **เพื่อ** ตอบคำถามย้อนหลังเรื่องสิทธิ์พนักงาน
### Acceptance Criteria
- **AC-05.1** Given อยู่หน้า list ของ tab ใดก็ได้ · When เลือกวันที่ย้อนหลังในตัวกรอง "มีผล ณ วันที่" · Then list เปลี่ยนเป็นค่าที่ Active ณ วันนั้นพร้อม badge บอกว่ากำลังดูย้อนหลัง
- **AC-05.2** Given เปิด view drawer ของค่าหนึ่ง · When เข้า tab "ประวัติเวอร์ชัน" · Then เห็น timeline ค่าเก่าไปค่าใหม่ พร้อมผู้แก้ไข เวลา เหตุผล
> trace: S-20 · BR-14 · **FN-27, FN-28**

## Story ST-06: ตั้งโควตาลาแบบขั้นตามอายุงาน
**ในฐานะ** HR Admin **ฉันต้องการ** กำหนดโควตาเป็นขั้นตามอายุงาน **เพื่อ** ให้สิทธิ์เพิ่มตามความอาวุโสได้อัตโนมัติที่ปลายทาง
### Acceptance Criteria
- **AC-06.1** Given กรอกขั้น 0–2 ปี แล้วขั้นถัดไปเริ่มที่ 4 ปี · When กดบันทึก · Then ระบบบล็อกพร้อมชี้ช่วงที่ขาด
- **AC-06.2** Given กรอกขั้น 0–2 ปี แล้วขั้นถัดไป 2–5 ปี · When กดบันทึก · Then ระบบบล็อกพร้อมชี้ช่วงที่ทับซ้อน
> trace: S-05 · BR-16 · **FN-08**

## Story ST-07: ตั้งเงื่อนไขยกยอดวันลา
**ในฐานะ** HR Admin **ฉันต้องการ** กำหนดยกยอดสูงสุดพร้อมวันหมดอายุ **เพื่อ** ให้ Leave ตัดยอดตามกติกาเดียวกันทั้งบริษัท
### Acceptance Criteria
- **AC-07.1** Given กรอกยกยอดสูงสุด 5 วันโดยเว้นวันหมดอายุ · When กดบันทึก · Then ระบบบล็อก
- **AC-07.2** Given กรอกยกยอด 5 วันพร้อมวันหมดอายุ 31 มีนาคมของปีถัดไป · When กดบันทึก · Then บันทึกสำเร็จ
> trace: S-06 · BR-12 · **FN-09**

## Story ST-08: ตั้งวิธี prorate พนักงานเข้าใหม่
**ในฐานะ** HR Admin **ฉันต้องการ** เลือกวิธี prorate พร้อมวิธีปัดเศษ **เพื่อ** ให้พนักงานที่เข้ากลางปีได้สิทธิ์ตามสัดส่วนที่ถูกต้อง
### Acceptance Criteria
- **AC-08.1** Given เลือก prorate "ตามเดือน" · When บันทึกแล้วเปิดดูค่า · Then ค่าที่บันทึกแสดงวิธี prorate ตามที่เลือก
- **AC-08.2** Given เลือกวิธีปัดเศษ "ครึ่งวันใกล้สุด" · When บันทึก · Then ค่าถูกส่งต่อให้ Leave ผ่านสัญญาการอ่านค่า
> trace: S-07 · **FN-10**

## Story ST-09: ตั้งกติกาการนับวันลา
**ในฐานะ** HR Admin **ฉันต้องการ** กำหนดว่านับวันหยุดในช่วงลาหรือไม่ **เพื่อ** ให้จำนวนวันของใบลาคำนวณตรงกันทุกที่
### Acceptance Criteria
- **AC-09.1** Given เปิดตัวเลือก "นับวันหยุดในช่วงลา" · When บันทึก · Then ค่าถูกเก็บในเวอร์ชันที่มีวันมีผล
- **AC-09.2** Given ปิดตัวเลือก "อนุญาตครึ่งวัน" · When บันทึก · Then กติกาที่ Leave อ่านไปไม่มีหน่วยครึ่งวัน
> trace: S-21 · **FN-29**

## Story ST-10: ตั้งประเภทลาแบบจ่ายบางส่วนพร้อมเงื่อนไขเอกสาร
**ในฐานะ** HR Admin **ฉันต้องการ** ระบุการจ่ายค่าจ้างพร้อมเงื่อนไขการแนบเอกสาร **เพื่อ** ให้ใบลาที่ปลายทางบังคับเอกสารได้ถูกกรณี
### Acceptance Criteria
- **AC-10.1** Given เลือก "จ่ายบางส่วน" โดยไม่กรอกเปอร์เซ็นต์ · When กดบันทึก · Then ระบบบล็อก
- **AC-10.2** Given เปิด "ต้องแนบเอกสาร" พร้อมระบุเงื่อนไข "ลาป่วยเกิน 3 วัน" · When บันทึก · Then เงื่อนไขถูกเก็บไว้ให้ Leave อ่าน
> trace: S-01 · §3.3ก · **FN-31**

## Story ST-11: เตือนเมื่อโควตาต่ำกว่าขั้นต่ำตามกฎหมาย
**ในฐานะ** HR Admin **ฉันต้องการ** ได้รับคำเตือนเมื่อตั้งโควตาลาพักร้อนต่ำกว่าขั้นต่ำ **เพื่อ** ไม่ตั้งค่าผิดกฎหมายโดยไม่รู้ตัว
### Acceptance Criteria
- **AC-11.1** Given กรอกโควตาลาพักร้อน 4 วันต่อปี · When กดบันทึก · Then ระบบแสดงคำเตือนว่าต่ำกว่าขั้นต่ำตามกฎหมาย
- **AC-11.2** Given เห็นคำเตือนแล้ว · When กดยืนยัน · Then ระบบบันทึกให้ (เตือน ไม่บล็อก)
> trace: S-01 · BR-06 · **FN-32**

## Story ST-12: ตั้งอัตรา OT พร้อมเพดานชั่วโมง
**ในฐานะ** HR Admin **ฉันต้องการ** กำหนดตัวคูณ OT ต่อประเภทพร้อมเพดานชั่วโมงต่อสัปดาห์ **เพื่อ** ให้ OT/Shift คิดค่าตอบแทนจากอัตราชุดเดียว
### Acceptance Criteria
- **AC-12.1** Given เลือกประเภท "OT วันทำงาน" พร้อมตัวคูณ 1.5 ฐานรายชั่วโมง เพดาน 36 · When บันทึก · Then เวอร์ชันถูกสร้างพร้อมวันมีผล
- **AC-12.2** Given เว้นเพดานชั่วโมงว่าง · When กดบันทึก · Then ระบบบล็อก
> trace: S-08 · BR-05 · **FN-11**

## Story ST-13: บันทึกรหัสอ้างอิงจ่ายเงินเป็นช่องอ้างอิง
**ในฐานะ** HR Admin **ฉันต้องการ** ใส่รหัสอ้างอิงจ่ายเงินไว้ที่ค่าอัตรา **เพื่อ** ให้ Salary Structure จับคู่องค์ประกอบค่าจ้างได้ภายหลัง
### Acceptance Criteria
- **AC-13.1** Given กรอกรหัสอ้างอิงจ่ายเงิน "OT01" · When บันทึก · Then ค่าถูกเก็บโดยไม่มีการคำนวณเงินใด ๆ ในหน้านี้
- **AC-13.2** Given เว้นรหัสอ้างอิงจ่ายเงินว่างในประเภทที่จ่ายค่าจ้าง · When บันทึก · Then ระบบเตือนเบา ๆ แต่บันทึกให้
> trace: S-08, S-25 · BR-18 · **FN-12**

## Story ST-14: บล็อกอัตรา OT ที่ต่ำกว่ากฎหมาย
**ในฐานะ** ระบบ **ฉันต้องการ** ปฏิเสธตัวคูณที่ต่ำกว่าขั้นต่ำตามกฎหมาย **เพื่อ** ป้องกันการตั้งค่าที่ทำให้บริษัทผิดกฎหมายแรงงาน
### Acceptance Criteria
- **AC-14.1** Given กรอกตัวคูณ 1.2 สำหรับ OT วันทำงาน · When กดถัดไป · Then ระบบบล็อกพร้อมข้อความบอกขั้นต่ำ 1.5 เท่า
- **AC-14.2** Given ถูกบล็อก · When ดูตำแหน่งใน wizard · Then ยังค้างอยู่ขั้นเดิม ไม่ข้ามไปขั้นถัดไป
> trace: S-09 · BR-05 · **FN-13**

## Story ST-15: สร้างกะมาตรฐานรวมกะข้ามวัน
**ในฐานะ** HR Admin **ฉันต้องการ** สร้างกะพร้อมช่วงพัก **เพื่อ** ให้ Shift & Roster ใช้เป็น pattern ตั้งต้น
### Acceptance Criteria
- **AC-15.1** Given กรอกเวลาเข้า 22:00 ออก 06:00 โดยไม่ติ๊กข้ามวัน · When บันทึก · Then ระบบบล็อก
- **AC-15.2** Given กรอกเวลาเข้า 08:00 ออก 17:00 พัก 12:00–13:00 · When บันทึก · Then ชั่วโมงทำงานต่อวันแสดงเป็น 8 ชั่วโมงโดยอัตโนมัติ
> trace: S-10 · BR-17 · **FN-14**

## Story ST-16: จัดปฏิทินวันหยุดประจำปี
**ในฐานะ** HR Admin **ฉันต้องการ** เพิ่มวันหยุดของบริษัทเป็นรายปี **เพื่อ** ให้ทุก feature กันวันจากปฏิทินชุดเดียวกัน
### Acceptance Criteria
- **AC-16.1** Given เลือกปี 2570 แล้วเพิ่มวันหยุด 16 รายการ · When บันทึก · Then ชุดปฏิทินแสดงจำนวนวันหยุดครบตามที่เพิ่ม
- **AC-16.2** Given เปิดชุดปฏิทินของอีกปีหนึ่ง · When ดูรายการ · Then เห็นเฉพาะวันหยุดของปีนั้น
> trace: S-11 · **FN-15**

## Story ST-17: บันทึกวันหยุดชดเชยที่อ้างวันต้นทาง
**ในฐานะ** HR Admin **ฉันต้องการ** ระบุวันหยุดต้นทางของวันหยุดชดเชย **เพื่อ** ให้ตรวจสอบย้อนกลับได้ว่าชดเชยมาจากวันไหน
### Acceptance Criteria
- **AC-17.1** Given เลือกประเภท "วันหยุดชดเชย" โดยไม่ระบุวันต้นทาง · When บันทึก · Then ระบบบล็อก
- **AC-17.2** Given ระบุวันต้นทางที่มีอยู่จริงในชุดปฏิทิน · When บันทึก · Then บันทึกสำเร็จพร้อมแสดงการอ้างอิง
> trace: S-11 · **FN-16**

## Story ST-18: แยกชุดปฏิทินตามสถานที่
**ในฐานะ** HR Admin **ฉันต้องการ** สร้างชุดปฏิทินแยกตามสาขา **เพื่อ** ให้โรงงานกับสำนักงานหยุดต่างกันได้
### Acceptance Criteria
- **AC-18.1** Given สร้างชุดปฏิทินใหม่พร้อมระบุสถานที่ "โรงงานระยอง" · When บันทึก · Then ชุดนั้นแยกจากชุดของสำนักงาน
- **AC-18.2** Given เว้นช่องสถานที่ว่าง · When บันทึก · Then บันทึกได้ (ชุดกลางของบริษัท)
> trace: S-32 · BR-09 · **FN-49** `[AI-DRAFT]`

## Story ST-19: บล็อกวันหยุดซ้ำ
**ในฐานะ** ระบบ **ฉันต้องการ** ปฏิเสธวันหยุดที่ซ้ำวันเดิม **เพื่อ** ไม่ให้การกันวันของปลายทางนับซ้ำ
### Acceptance Criteria
- **AC-19.1** Given มีวันหยุด 13 เมษายน 2570 อยู่แล้วในบริษัทเดียวกัน · When เพิ่มวันเดิมอีกครั้ง · Then ระบบบล็อกพร้อมชี้รายการเดิม
- **AC-19.2** Given วันเดิมอยู่คนละชุดปฏิทินแต่บริษัทและปีเดียวกัน · When เพิ่ม · Then ระบบยังบล็อก
> trace: S-12 · BR-09 · **FN-17**

## Story ST-20: ตั้งรอบตัดเวลาพร้อมรอบจ่าย
**ในฐานะ** HR Admin **ฉันต้องการ** กำหนดวันตัดเวลากับวันจ่าย **เพื่อ** ให้ Attendance ปิดยอดตรงกับงวดจ่ายของ Payroll
### Acceptance Criteria
- **AC-20.1** Given กรอกวันตัด 28 กับวันจ่าย 25 ในงวดเดียวกัน · When บันทึก · Then ระบบบล็อก
- **AC-20.2** Given กรอกวันตัด 25 กับวันจ่าย 30 ความถี่รายเดือน · When บันทึก · Then บันทึกสำเร็จ
> trace: S-13 · BR-11 · **FN-18**

## Story ST-21: สร้างงวดจริงทั้งปีจากกติกา
**ในฐานะ** HR Admin **ฉันต้องการ** สร้างงวดจริงทั้งปีจากกติกาที่ตั้งไว้ **เพื่อ** ให้มีนิยามของงวดที่ระบบใช้ล็อกการแก้ย้อนหลัง
### Acceptance Criteria
- **AC-21.1** Given ตั้งกติกาตัด 25 จ่าย 30 รายเดือนไว้แล้ว · When กด "สร้างงวดทั้งปี" · Then ระบบสร้างแถวงวดครบทั้งปีพร้อมวันเริ่ม วันจบ วันจ่าย
- **AC-21.2** Given งวดหนึ่งจ่ายเสร็จแล้ว · When กดปิดงวดพร้อมยืนยัน · Then สถานะงวดเป็น "ปิด" พร้อมบันทึกผู้ปิดกับเวลา
- **AC-21.3** Given งวดที่ปิดแล้ว · When กดเปิดงวดกลับโดยไม่กรอกเหตุผล · Then ระบบบล็อก
> trace: S-31 · BR-21 · **FN-48**

## Story ST-22: แยกความถี่รอบบันทึกเวลาออกจากรอบจ่าย
**ในฐานะ** HR Admin **ฉันต้องการ** ตั้งความถี่รอบบันทึกเวลาแยกจากรอบจ่าย **เพื่อ** รองรับองค์กรที่ตัดเวลารายสัปดาห์แต่จ่ายรายเดือน
### Acceptance Criteria
- **AC-22.1** Given เปิดฟอร์มรอบเวลาครั้งแรก · When ดูค่าเริ่มต้นของความถี่รอบบันทึกเวลา · Then ค่าเริ่มต้นคือ "ใช้รอบเดียวกับรอบจ่าย"
- **AC-22.2** Given เลือก "รายสัปดาห์" · When บันทึก · Then ค่าถูกเก็บแยกจากความถี่รอบจ่าย
> trace: S-13 · §3.3ง · **FN-50** `[AI-DRAFT]`

## Story ST-23: ตั้งรอบประเมิน
**ในฐานะ** HR Admin **ฉันต้องการ** กำหนดช่วงประเมินพร้อมช่วงเปิดกรอก **เพื่อ** ให้ Performance เปิดรอบได้ตรงเวลา
### Acceptance Criteria
- **AC-23.1** Given กรอกรอบกลางปี 1 มกราคม ถึง 30 มิถุนายน พร้อมช่วงเปิดกรอก 1–15 กรกฎาคม · When บันทึก · Then บันทึกสำเร็จ
- **AC-23.2** Given กรอกช่วงเปิดกรอกก่อนช่วงประเมินเริ่ม · When บันทึก · Then ระบบบล็อก
> trace: S-15 · **FN-20**

## Story ST-24: บล็อกรอบประเมินที่ทับซ้อน
**ในฐานะ** ระบบ **ฉันต้องการ** ปฏิเสธรอบประเมินที่ช่วงวันทับซ้อนรอบเดิม **เพื่อ** ไม่ให้ผลประเมินของพนักงานถูกนับซ้ำรอบ
### Acceptance Criteria
- **AC-24.1** Given มีรอบ 1 มกราคม ถึง 30 มิถุนายน 2570 อยู่แล้ว · When สร้างรอบใหม่ 1 พฤษภาคม ถึง 31 ตุลาคม 2570 · Then ระบบบล็อกพร้อมแสดงชื่อรอบที่ชน
- **AC-24.2** Given สร้างรอบเดียวกันแต่คนละปี · When บันทึก · Then บันทึกสำเร็จ
> trace: S-16 · BR-10 · **FN-21**

## Story ST-25: กำหนดขอบเขตค่ากลางกับค่าเฉพาะบริษัท
**ในฐานะ** HR Admin **ฉันต้องการ** เลือกได้ว่าค่านี้เป็นค่ากลางหรือเฉพาะบริษัทลูก **เพื่อ** รองรับกลุ่มบริษัทที่นโยบายไม่เหมือนกัน
### Acceptance Criteria
- **AC-25.1** Given เลือก "เฉพาะบริษัท" โดยไม่เลือกบริษัทใดเลย · When บันทึก · Then ระบบบล็อก
- **AC-25.2** Given เลือก "เฉพาะบริษัท" พร้อมเลือกบริษัทลูกหนึ่งราย · When บันทึก · Then คอลัมน์ขอบเขตของแถวแสดงชื่อบริษัทนั้น
> trace: S-17 · BR-13 · **FN-22**

## Story ST-26: ให้ค่าของบริษัทลูกทับค่ากลาง
**ในฐานะ** ระบบ **ฉันต้องการ** เลือกค่าของบริษัทลูกก่อนค่ากลางเสมอ **เพื่อ** ให้ผลลัพธ์ที่ปลายทางตรงกับนโยบายของบริษัทนั้น
### Acceptance Criteria
- **AC-26.1** Given มีทั้งค่ากลางกับค่าเฉพาะของบริษัท A ในค่าเดียวกัน · When ปลายทางขอค่าสำหรับบริษัท A · Then ระบบคืนค่าของบริษัท A
- **AC-26.2** Given บริษัท B ไม่มีค่าเฉพาะ · When ปลายทางขอค่าสำหรับบริษัท B · Then ระบบคืนค่ากลาง
> trace: S-17 · BR-13 · **FN-23**

## Story ST-27: เผื่อช่องขอบเขตการใช้ไว้เป็น hook
**ในฐานะ** BA **ฉันต้องการ** เห็นช่องขอบเขตการใช้ที่ล็อกไว้ที่ "ทั้งบริษัท" **เพื่อ** ให้ขยายเป็น eligibility ระดับกลุ่มพนักงานได้โดยไม่ต้องรื้อโครง
### Acceptance Criteria
- **AC-27.1** Given เปิด drawer สร้างค่า · When ดูช่องขอบเขตการใช้ · Then ช่องแสดงค่า "ทั้งบริษัท" แบบอ่านอย่างเดียว
- **AC-27.2** Given ชี้ที่ไอคอนอธิบายข้างช่อง · When อ่านคำอธิบาย · Then เห็นว่ารอบนี้จำกัดที่ระดับบริษัท
> trace: S-22 · **FN-30** · OQ-STD-02

## Story ST-28: ปิดใช้ค่าโดยไม่ลบถาวร
**ในฐานะ** HR Admin **ฉันต้องการ** ปิดใช้ค่าที่เลิกใช้แล้ว **เพื่อ** ไม่ให้ถูกเลือกใหม่โดยที่ข้อมูลเก่ายังอ่านได้
### Acceptance Criteria
- **AC-28.1** Given อยู่หน้า list ของทุก tab · When มองหาปุ่มลบถาวร · Then ไม่มีปุ่มลบที่ใดในหน้า
- **AC-28.2** Given กดปิดใช้แล้วยืนยัน · When ดูสถานะแถว · Then สถานะเป็น "ปิดใช้" พร้อมโน้ตว่าเลือกใหม่ไม่ได้
> trace: S-18 · BR-07 · **FN-24, FN-25**

## Story ST-29: เห็นผลกระทบปลายทางก่อนปิดใช้
**ในฐานะ** HR Admin **ฉันต้องการ** เห็นรายการ feature ที่ยังอ้างค่านี้ก่อนยืนยันการปิดใช้ **เพื่อ** ไม่ตัดกติกาที่ยังมีคนใช้อยู่โดยไม่รู้ตัว
### Acceptance Criteria
- **AC-29.1** Given ค่าหนึ่งมี feature ปลายทางอ้างอยู่ · When กดปิดใช้ · Then ระบบแสดงรายการ feature ที่อ้างก่อนให้ยืนยัน
- **AC-29.2** Given อยู่ในหน้ายืนยันการปิดใช้ · When กรอกเหตุผลน้อยกว่า 10 ตัวอักษร · Then ระบบบล็อก
> trace: S-19 · BR-08 · **FN-26**

## Story ST-30: ดูว่าใครใช้ค่านี้บ้าง
**ในฐานะ** HR Staff **ฉันต้องการ** เห็นรายชื่อ feature ปลายทางที่อ่านค่านี้ **เพื่อ** ประเมินผลกระทบก่อนเสนอเปลี่ยนนโยบาย
### Acceptance Criteria
- **AC-30.1** Given เปิด view drawer ของค่าหนึ่ง · When เข้า tab "ใครใช้ค่านี้" · Then เห็นรายชื่อ feature ปลายทางพร้อมสถานะพร้อมใช้หรือยังไม่ทำ
- **AC-30.2** Given กดลิงก์ไป feature ปลายทางที่ยังไม่ทำ · When ระบบตอบกลับ · Then แสดงสถานะยังไม่พร้อมใช้งานโดยไม่เปิดหน้าจอปลอม
> trace: S-19 · §9 · **FN-33**

## Story ST-31: บล็อกการตั้งวันมีผลย้อนเข้างวดที่ปิดแล้ว
**ในฐานะ** ระบบ **ฉันต้องการ** ปฏิเสธวันมีผลที่ย้อนเข้างวดที่ปิดแล้ว **เพื่อ** ไม่ให้ยอดที่จ่ายไปแล้วเปลี่ยนย้อนหลัง
### Acceptance Criteria
- **AC-31.1** Given งวดกรกฎาคมถูกปิดแล้ว · When ตั้งวันมีผลเป็นวันในงวดนั้น · Then ระบบบล็อกพร้อมบอกวันที่เร็วที่สุดที่ตั้งได้
- **AC-31.2** Given ตั้งวันมีผลเป็นวันแรกของงวดที่ยังเปิด · When บันทึก · Then บันทึกสำเร็จ
> trace: S-14 · BR-04, BR-21 · **FN-19**

## Story ST-32: กรองรายการค่าในแต่ละกลุ่ม
**ในฐานะ** HR Staff **ฉันต้องการ** กรองรายการค่าในตารางให้เหลือเฉพาะที่สนใจ **เพื่อ** หาค่าที่ต้องการโดยไม่ต้องไล่ทั้งตาราง
### Acceptance Criteria
- **AC-32.1** Given อยู่หน้า list · When กรองด้วยสถานะหรือบริษัท · Then ตารางเปลี่ยนเฉพาะส่วนตาราง โดยส่วนอื่นของหน้าไม่ขยับ
- **AC-32.2** Given กรองจนไม่เหลือรายการ · When ดูพื้นที่ตาราง · Then เห็น empty state ที่บอกสิ่งที่ทำต่อได้
> trace: กติกากลาง · **FN-90**

## Story ST-33: ยืนยันทุกครั้งก่อนปิดหรือยกเลิก
**ในฐานะ** HR Admin **ฉันต้องการ** ให้ทุกการปิดใช้หรือยกเลิกมีขั้นยืนยัน **เพื่อ** ป้องกันการกดพลาดที่กระทบสิทธิ์พนักงาน
### Acceptance Criteria
- **AC-33.1** Given กดปิดใช้ ยกเลิกเวอร์ชัน ปิดงวด หรือเปิดงวดกลับ · When ระบบตอบสนอง · Then มีหน้าต่างยืนยันทุกครั้ง
- **AC-33.2** Given ยืนยันแล้ว · When ตรวจข้อมูล · Then เป็น soft archive ไม่มีข้อมูลถูกลบ
> trace: BR-07 กติกากลาง · **FN-91**

## Story ST-34: กันการบันทึกซ้ำระหว่างรอผล
**ในฐานะ** ระบบ **ฉันต้องการ** ปิดปุ่มบันทึกระหว่างประมวลผล **เพื่อ** ไม่ให้เกิดเวอร์ชันซ้ำจากการกดสองครั้ง
### Acceptance Criteria
- **AC-34.1** Given กดบันทึกหนึ่งครั้ง · When ระบบกำลังประมวลผล · Then ปุ่มถูก disable พร้อมแสดงตัวโหลด
- **AC-34.2** Given field บังคับยังไม่ครบ · When กดไปขั้นถัดไป · Then ระบบบล็อกพร้อมชี้ field ที่ขาด
> trace: กติกากลาง · **FN-92**

## Story ST-35: บันทึกร่องรอยทุกการเปลี่ยนแปลง
**ในฐานะ** ผู้ตรวจสอบ **ฉันต้องการ** เห็นร่องรอยทุกการเปลี่ยนนโยบายแบบเพิ่มอย่างเดียว **เพื่อ** ใช้เป็นหลักฐานตอนถูกตรวจ
### Acceptance Criteria
- **AC-35.1** Given มีการสร้าง แก้ ตั้งวันมีผล ยกเลิก หรือปิดใช้ · When เปิด tab ประวัติเวอร์ชัน · Then เห็นรายการครบพร้อมผู้ทำ เวลา ค่าเก่าไปค่าใหม่
- **AC-35.2** Given เปิดหน้าประวัติ · When มองหาปุ่มแก้หรือลบรายการประวัติ · Then ไม่มีปุ่มดังกล่าว
> trace: BR-14 กติกากลาง · **FN-93**

## Story ST-36: เลือกคนจากทะเบียนพนักงานแบบเดียวกันทุกช่อง
**ในฐานะ** HR Admin **ฉันต้องการ** ให้ทุกช่องที่เป็นคนเป็น combobox พนักงานหน้าตาเดียวกัน **เพื่อ** ไม่ต้องพิมพ์ชื่อเองแล้วสะกดไม่ตรงกัน
### Acceptance Criteria
- **AC-36.1** Given เปิดช่องผู้รับผิดชอบ · When พิมพ์ค้นหา · Then ตัวเลือกแสดงลำดับ ชื่อ แล้วตำแหน่ง กับแผนก
- **AC-36.2** Given เปิดช่องคนที่จุดอื่นในหน้า · When เทียบหน้าตา · Then เหมือนกันทุกจุด
> trace: BR-15 · #102 · **FN-94**

## Story ST-37: แยก persona ทดสอบออกจากหัวหน้าจอ
**ในฐานะ** ผู้ตรวจ prototype **ฉันต้องการ** ให้ตัวสลับ persona อยู่ใน demo strip **เพื่อ** ไม่ให้ถูกเข้าใจผิดว่าเป็นฟังก์ชันจริงของระบบ
### Acceptance Criteria
- **AC-37.1** Given เปิดหน้าใดก็ได้ · When ดู page header · Then ไม่มีตัวสลับ persona อยู่บนนั้น
- **AC-37.2** Given สลับ persona เป็นผู้อ่าน · When ดูปุ่มหลัก · Then ปุ่มที่ต้องใช้สิทธิ์แก้ไขถูก disable
> trace: #105 · **FN-95**

## 7.4 Function Ledger — FN ครบทั้ง 53 ข้อ (Lane Mode v2 · ทุก FN ต้องปรากฏใน BRD)

| FN | Story / ที่อยู่ใน BRD | S-XX | สถานะ |
|---|---|---|---|
| FN-01 | ST-01 · §5 J-02,J-04 | S-01 | ✅ in scope |
| FN-02 | ST-01 · §5 J-05 | S-01 | ✅ |
| FN-03 | ST-02 · §5 J-07 | S-01 | ✅ |
| FN-04 | ST-03 · §5.2.2 | S-02 | ✅ |
| FN-05 | ST-03 · §5.2.2 · E-10 | S-02 | ✅ |
| FN-06 | ST-02 · §5.2.1 | S-03 | ✅ |
| FN-07 | ST-04 · §5.2.3 | S-04 | ✅ |
| FN-08 | ST-06 · §5.3 E-06 | S-05 | ✅ |
| FN-09 | ST-07 · §5.3 E-08 | S-06 | ✅ |
| FN-10 | ST-08 | S-07 | ✅ |
| FN-11 | ST-12 · §5 J-03 | S-08 | ✅ |
| FN-12 | ST-13 · §5.3 E-11 | S-08 | ✅ |
| FN-13 | ST-14 · §5.3 E-01 | S-09 | ✅ |
| FN-14 | ST-15 · §5.3 E-07 | S-10 | ✅ |
| FN-15 | ST-16 | S-11 | ✅ |
| FN-16 | ST-17 | S-11 | ✅ |
| FN-17 | ST-19 · §5.3 E-03 | S-12 | ✅ |
| FN-18 | ST-20 · §5.3 E-05 | S-13 | ✅ |
| FN-19 | ST-31 · §5.3 E-02 | S-14 | ✅ |
| FN-20 | ST-23 | S-15 | ✅ |
| FN-21 | ST-24 · §5.3 E-04 | S-16 | ✅ |
| FN-22 | ST-25 | S-17 | ✅ |
| FN-23 | ST-26 | S-17 | ✅ |
| FN-24 | ST-28 · §5.2.4 | S-18 | ✅ |
| FN-25 | ST-28 · §5.2.5 | S-18 | ✅ |
| FN-26 | ST-29 · §5.2.4 A4-1 | S-19 | ✅ |
| FN-27 | ST-05 · §5.2.7 A7-1 | S-20 | ✅ |
| FN-28 | ST-05 · §5.2.7 A7-2 | S-20 | ✅ |
| FN-29 | ST-09 | S-21 | ✅ |
| FN-30 | ST-27 · §6.2 field 8 | S-22 | ✅ (hook) |
| FN-31 | ST-10 · §6.4 | S-01 | ✅ |
| FN-32 | ST-11 · §5.3 E-09 | S-01 | ✅ |
| FN-33 | ST-30 · §5.2.7 A7-3 · §6.9 | S-19 | ✅ |
| FN-48 | ST-21 · §5.2.6 · §6.7 | S-31 | ✅ |
| FN-49 | ST-18 · §6.6 | S-32 | ✅ `[AI-DRAFT]` |
| FN-50 | ST-22 · §6.7 | S-13 | ✅ `[AI-DRAFT]` |
| FN-90 | ST-32 | — | ✅ |
| FN-91 | ST-33 | — | ✅ |
| FN-92 | ST-34 | — | ✅ |
| FN-93 | ST-35 | — | ✅ |
| FN-94 | ST-36 · §6.2 field 12 | — | ✅ |
| FN-95 | ST-37 | — | ✅ |
| FN-40 | §3.2 OUT-01 · §14.6 Functions Cut | S-23 | ⛔ ไม่รองรับ (ประกาศบนจอ) |
| FN-41 | §3.2 OUT-02 · §14.6 | S-24 | ⛔ ไม่รองรับ |
| FN-42 | §3.2 OUT-03 · §14.6 | S-25 | ⛔ ไม่รองรับ |
| FN-43 | §3.2 OUT-04 · §14.6 | S-26 | ⛔ ไม่รองรับ |
| FN-44 | §3.2 OUT-05 · §14.6 | S-27 | ⛔ ไม่รองรับ |
| FN-45 | §3.2 OUT-06 · §14.6 | S-28 | ⛔ ไม่รองรับ |
| FN-46 | §3.2 OUT-07 · §14.6 | S-29 | ⛔ ไม่รองรับ |
| FN-47 | §3.2 OUT-08 · §14.6 | S-30 | ⛔ ไม่รองรับ |
| FN-51 | §3.2 OUT-09 · §14.6 | S-33 | ⛔ ไม่รองรับ |
| FN-52 | §3.2 OUT-10 · §14.6 | S-34 | ⛔ ไม่รองรับ |
| FN-53 | §3.2 OUT-11 · §14.6 | S-35 | ⛔ ไม่รองรับ |

**รวม 53 FN — in scope 42 · ไม่รองรับ 11 · ไม่มี FN ใดหลุด**

---

# Section 8: Status & Lifecycle

> **หน่วยของ lifecycle = 1 เวอร์ชันของค่า config 1 ตัว** (ไม่ใช่ตัว record) — ตาม STANDARD_BASELINE §2 · ครบ **5 state** (OB-11)

## 8.1 State Diagram

```
                    ┌──────────────┐
     สร้าง/บันทึกร่าง  │    Draft     │  ยังไม่มีผลกับ feature ใด
        ─────────────▶│  (ฉบับร่าง)   │
                    └──┬────────┬──┘
       publish (ตั้ง eff)│        │ ทิ้งร่าง + confirm
      eff > วันนี้        │        ▼
                        │   ┌───────────┐
                        │   │ Discarded │
                        │   └───────────┘
                        ▼
                 ┌──────────────┐  ยกเลิกก่อนมีผล + เหตุผล   ┌────────────────┐
                 │  Scheduled   │──────────────────────────▶│ Draft/Cancelled │
                 │  (รอมีผล)     │                           └────────────────┘
                 └──────┬───────┘
        ถึงวันมีผล (system) │           ◀── publish ที่ eff = วันนี้ (จาก Draft)
                        ▼
                 ┌──────────────┐  มีเวอร์ชันใหม่ถึงวันมีผล (system)  ┌──────────────┐
                 │   Active     │──────────────────────────────────▶│  Superseded  │
                 │  (ใช้อยู่)     │                                   │ (read-only)  │
                 └──────┬───────┘                                   └──────────────┘
      ปิดใช้ + confirm    │  ▲ เปิดใช้กลับ (สร้างเวอร์ชันใหม่)
      + where-used check │  │
                        ▼  │
                 ┌──────────────┐
                 │   Inactive   │  soft archive — เลือกใหม่ไม่ได้ · ของเดิมยังอ่านได้
                 │  (ปิดใช้)      │  ❌ ไม่มี hard delete
                 └──────────────┘
```

## 8.2 State Transition Table

| # | จาก | Trigger | ไป | ใครกด | เงื่อนไข | Scenario · FN |
|---|---|---|---|---|---|---|
| T-01 | — | กด "สร้าง" / "บันทึกร่าง" | **Draft** | HR Admin | มีชื่อค่า | S-03 · FN-06 |
| T-02 | Draft | บันทึก + ตั้งวันมีผลอนาคต | **Scheduled** | HR Admin | ผ่าน BR-01,03,04 + payload ครบ | S-01 · FN-01,FN-02 |
| T-03 | Draft | บันทึก + วันมีผล = วันนี้ | **Active** | HR Admin | ผ่าน BR-01,03,04 + ไม่มีเวอร์ชันชน | S-01 · FN-01 |
| T-04 | Draft | ทิ้งร่าง + confirm | **Discarded** | HR Admin | confirm | S-03 · FN-91 |
| T-05 | Scheduled | ถึงวันมีผล | **Active** | **ระบบ** | อัตโนมัติ (scheduler) | S-01 · FN-02 |
| T-06 | Scheduled | ยกเลิกก่อนถึงวัน + เหตุผล | **Draft/Cancelled** | HR Admin | ยังไม่ถึงวันมีผล (BR-20) | S-04 · FN-07 |
| T-07 | Active | มีเวอร์ชันใหม่ถึงวันมีผล | **Superseded** | **ระบบ** | set `effective_to` ของเวอร์ชันเดิม | S-02 · FN-05 |
| T-08 | Active | ปิดใช้ + confirm + ผ่าน where-used | **Inactive** | HR Admin | เหตุผล ≥10 ตัวอักษร (BR-07,BR-08) | S-18,S-19 · FN-24,FN-26 |
| T-09 | Scheduled | ปิดใช้ค่าทั้งตัวก่อนเวอร์ชันมีผล | **Inactive** | HR Admin | confirm | S-18 · FN-24 |
| T-10 | Inactive | เปิดใช้กลับ (สร้างเวอร์ชันใหม่ + วันมีผล) | **Scheduled/Active** | HR Admin | ต้องมีวันมีผลใหม่ | S-18 · FN-25 |
| T-11 | Superseded | — | **Superseded** | — | read-only ตลอดไป (หลักฐาน HR-1) | S-20 · FN-27 |

- **ทุก transition เขียน audit append-only** ที่ Policy Center Audit Trail (BR-14) — feature นี้เรียกใช้ ไม่ทำเอง
- **ทุก transition ที่เปลี่ยนสิทธิ์/entitlement ของพนักงาน** (T-02, T-03, T-05, T-06, T-08, T-10 + ปิด/เปิดงวด) **ยิง event ให้ ENG-CSQ ท่อ SecC** — ดู `5_DECLARATIONS/CSQ_BRIEF.md` (E1–E6)
- **DOA placeholder: N/A** — ไม่มี approval ในรอบนี้ · ถ้า OQ-STD-01 เคาะว่าต้องมี ให้แทรก `GET /doa/resolve` ที่ **T-02 (Draft → Scheduled) จุดเดียว** — ห้าม hardcode chain

## 8.3 State ของ "งวด" (`hr_pay_period`) — lifecycle ย่อย

| จาก | Trigger | ไป | เงื่อนไข | trace |
|---|---|---|---|---|
| — | กด "สร้างงวดทั้งปี" | **open (เปิด)** | มีกติการอบเวลา/รอบจ่ายที่ Active | S-31 · FN-48 |
| open | ปิดงวด + confirm | **closed (ปิด)** | บันทึก `closed_by` + `closed_at` · **กลายเป็นฐานของ BR-04** | S-31 · BR-21 |
| closed | เปิดงวดกลับ + เหตุผล | **open** | เหตุผล ≥10 ตัวอักษร + audit | S-31 · BR-21 |

---

# Section 9: Business Rules + Validation (with Tags)

## 9.1 Business Rules

> Tag: **FIXED** = ค่าคงที่ ห้ามเปลี่ยนโดยไม่แก้โค้ด/มติ · **CONFIGURABLE** = ค่าเปลี่ยนได้ผ่านหน้าตั้งค่า · **DYNAMIC** = เงื่อนไขซับซ้อน/หลายชั้น ต้องมีที่จัดการกฎ · **WARNING** = ยังตัดสินไม่ได้

| BR | กติกา | พฤติกรรมเมื่อชน | Scenario | **Tag** | ใครเปลี่ยน + บ่อยแค่ไหน + ระดับ | ที่มา |
|---|---|---|---|---|---|---|
| **BR-01** | ทุกเวอร์ชันต้องมี `effective_date` — บันทึกโดยไม่มีไม่ได้ (ยกเว้น Draft) | บล็อก + ชี้ field | S-01,S-02 | **FIXED** | ไม่มีใครเปลี่ยน — เป็น invariant ของ HR-1 | **[มติ HR-1]** |
| **BR-02** | ห้ามแก้ทับเวอร์ชันที่ Active — การแก้ = สร้างเวอร์ชันใหม่พร้อมวันมีผล | ปุ่ม "แก้ไข" เปิดฟอร์มเวอร์ชันใหม่เสมอ | S-02 | **FIXED** | ไม่มีใครเปลี่ยน | **[มติ HR-1]** |
| **BR-03** | เวอร์ชันของค่าเดียวกัน + บริษัทเดียวกัน ห้ามมี `effective_date` ซ้ำ/คร่อมกัน | บล็อก + แสดงเวอร์ชันที่ชน | S-02 | **FIXED** | ไม่มีใครเปลี่ยน | [แผน] |
| **BR-04** | ห้ามตั้ง `effective_date` ย้อนหลังเข้าไปในงวดที่ปิดแล้ว | บล็อก + แนะวันที่ถัดไปที่ตั้งได้ | S-14 | **CONFIGURABLE** | HR Admin เปิด/ปิดผ่าน `lock_closed_period` (default = ล็อก) · นาน ๆ ครั้ง · **Admin Panel** | [ปิด `[AI-DRAFT]` แล้วที่ S1.5 · นิยาม "งวดปิด" = BR-21] |
| **BR-05** | ตัวคูณ OT ต้อง ≥ ขั้นต่ำตามกฎหมายแรงงานไทย (OT วันทำงาน 1.5 · ทำงานวันหยุด 1.0 · OT วันหยุด 3.0) | บล็อก + บอกขั้นต่ำ | S-08,S-09 | **CONFIGURABLE** | ตัวเลขขั้นต่ำเปลี่ยนตามกฎหมาย — HR Admin/IT · นาน ๆ ครั้ง · **Admin Panel** (ตาราง legal minimum + `effective_date`) | `[STD]` + กฎหมายแรงงานไทย |
| **BR-06** | โควตาลาพักร้อน < 6 วัน/ปี (อายุงานครบ 1 ปี) = **เตือน ไม่บล็อก** | เตือน + ให้ยืนยัน | S-01 | **CONFIGURABLE** | HR Admin · นาน ๆ ครั้ง · **Admin Panel** (ค่าขั้นต่ำ + เตือน/บล็อก) | `[STD]` `[AI-DRAFT]` |
| **BR-07** | ไม่มี hard delete — ปิดใช้ (soft archive) เท่านั้น | ไม่มีปุ่ม "ลบ" ที่ใดเลย | S-18 | **FIXED** | ไม่มีใครเปลี่ยน | **[มติ audit append-only]** |
| **BR-08** | ปิดใช้ค่าที่ยังมี feature ปลายทางอ้างอยู่ → ต้องแสดง where-used + ยืนยัน | modal + รายการ feature | S-19 | **FIXED** | ไม่มีใครเปลี่ยน | [OB-02] #107 |
| **BR-09** | วันหยุดห้ามซ้ำวันเดียวกันใน บริษัท+ปี เดียวกัน (ตรวจข้ามชุดปฏิทินด้วย) | บล็อก + ชี้รายการเดิม | S-12,S-32 | **FIXED** | ไม่มีใครเปลี่ยน | [แผน] |
| **BR-10** | ช่วงรอบประเมินห้ามทับซ้อนกันในปีเดียวกัน | บล็อก + แสดงรอบที่ชน | S-16 | **FIXED** | ไม่มีใครเปลี่ยน | [แผน] |
| **BR-11** | วันตัดเวลา ≤ วันจ่าย ในงวดเดียวกัน | บล็อก | S-13 | **FIXED** | ไม่มีใครเปลี่ยน | `[AI-DRAFT]` → คงตามที่เขียน |
| **BR-12** | ยกยอดสูงสุด ≥ 0 · ถ้า > 0 ต้องมีวันหมดอายุยกยอดในปีถัดไป | บล็อก | S-06 | **FIXED** | ไม่มีใครเปลี่ยน (ค่าจริงเป็น data ไม่ใช่กฎ) | `[STD]` |
| **BR-13** | ลำดับ resolve ค่า: **บริษัทลูก → ค่ากลาง (shared)** — บริษัทลูกทับค่ากลางเสมอ | ระบบเลือกอัตโนมัติ + badge "ใช้ค่าของบริษัท X" | S-17 | **DYNAMIC** 🤖 | ผู้บริหาร/BA · เปลี่ยนเมื่อโครงกลุ่มบริษัทเปลี่ยน · **Rule Management** — ปัจจุบัน 2 ชั้น อนาคตอาจเป็น บริษัท → ภูมิภาค → กลุ่ม | `[STD]` D365 shared parameters |
| **BR-14** | ทุก transition/แก้ไข เขียน audit append-only (เรียก Policy Center Audit Trail) | ไม่มีทางปิด | ทุก S | **FIXED** | ไม่มีใครเปลี่ยน | **[มติ audit]** [OB-15] |
| **BR-15** | ทุก field ที่เป็นคน = combobox Employee Master (avatar → ชื่อ → ตำแหน่ง · แผนก) | — | §6.2 | **FIXED** | ไม่มีใครเปลี่ยน | **#102** [OB-03] |
| **BR-16** | ขั้นอายุงาน (milestone) ต้องต่อเนื่อง ไม่ทับซ้อน ไม่มีช่องว่าง | บล็อก + ชี้ช่วงที่ขาด/ชน | S-05 | **FIXED** | ไม่มีใครเปลี่ยน | `[STD]` |
| **BR-17** | กะ: เวลาออก > เวลาเข้า เว้นแต่ติ๊ก "ข้ามวัน" · ช่วงพักต้องอยู่ในช่วงกะ | บล็อก | S-10 | **FIXED** | ไม่มีใครเปลี่ยน | `[AI-DRAFT]` → คงตามที่เขียน |
| **BR-18** | ประเภทลา/อัตราที่ "จ่ายค่าจ้าง" ควรระบุ `payroll_code` — ไม่บังคับ (soft ref nullable) | เตือนเบา ไม่บล็อก | S-08,S-25 | **CONFIGURABLE** | BA (Salary Structure) · นาน ๆ ครั้ง · **Admin Panel** (สลับ เตือน/บังคับ เมื่อ Salary Structure พร้อม) | **LD-4C-02** [OQ-STD-03] |
| **BR-19** | ค่าที่สถานะ Draft/Scheduled ไม่ถูกส่งให้ feature ปลายทางเห็น | — | S-01,S-03 | **FIXED** | ไม่มีใครเปลี่ยน | [แผน] |
| **BR-20** | เวอร์ชัน Scheduled ยกเลิกได้ก่อนถึงวันมีผลเท่านั้น — ถึงวันแล้วแก้ไม่ได้ (สร้างใหม่แทน) | ปุ่มยกเลิกหายเมื่อ Active | S-04 | **FIXED** | ไม่มีใครเปลี่ยน | [แผน] · OB-11 |
| **BR-21** | งวดที่สถานะ "ปิด" ห้ามแก้ค่าที่กระทบงวดนั้น — **เป็นนิยามของ "งวดที่ปิดแล้ว" ใน BR-04** · เปิดงวดกลับต้องมีเหตุผล + audit | บล็อก + ชี้งวดที่ปิด | S-31,S-14 | **CONFIGURABLE** | HR Admin ปิด/เปิดงวดเอง · รายเดือน · **Admin Panel** (ควบคู่ `lock_closed_period`) | `[STD]` D365 pay period |

## 9.2 Validation Rules

| VR | Field / Action | เงื่อนไข | ประเภท | ข้อความ | trace |
|---|---|---|---|---|---|
| VR-01 | `effective_date` | ว่างขณะ publish | **Error** | "กรุณาระบุวันมีผล" | BR-01 · FN-01 |
| VR-02 | `effective_date` | ซ้อนช่วงกับเวอร์ชันอื่นของค่า+บริษัทเดียวกัน | **Error** | "มีเวอร์ชันที่มีผลช่วงเดียวกันอยู่แล้ว: [เวอร์ชัน]" | BR-03 |
| VR-03 | `effective_date` | อยู่ในงวดที่ `period_status=closed` | **Prevent** | "ตั้งวันมีผลย้อนเข้างวด [งวด] ที่ปิดแล้วไม่ได้ — วันที่ตั้งได้เร็วที่สุดคือ [วันที่]" | BR-04,BR-21 · FN-19 |
| VR-04 | `change_reason` | `version_no ≥ 2` และความยาว < 10 | **Error** | "กรอกเหตุผลอย่างน้อย 10 ตัวอักษร" | BR-02 · FN-05 |
| VR-05 | `cancel_reason` / `deactivate_reason` / `reopen_reason` | ความยาว < 10 | **Error** | "กรอกเหตุผลอย่างน้อย 10 ตัวอักษร" | BR-20,BR-08,BR-21 |
| VR-06 | `multiplier` | < ขั้นต่ำตามประเภทอัตรา | **Prevent** | "ตัวคูณต้องไม่น้อยกว่า [ขั้นต่ำ] เท่า ตามกฎหมายแรงงาน" | BR-05 · FN-13 |
| VR-07 | `cap_hours_week` | ว่าง หรือ ≤ 0 | **Error** | "ระบุเพดานชั่วโมงต่อสัปดาห์มากกว่า 0" | §3.3ข · FN-11 |
| VR-08 | `quota_per_year` (ลาพักร้อน) | < 6 และอายุงานครบ 1 ปี | **Warning** | "โควตาต่ำกว่าขั้นต่ำตามกฎหมาย — ยืนยันเพื่อบันทึกต่อ" | BR-06 · FN-32 |
| VR-09 | `quota_per_year` | = 0 โดยไม่ติ๊ก "ไม่จำกัด" | **Error** | "โควตา 0 ต้องติ๊กไม่จำกัด" | §3.3ก |
| VR-10 | `paid_pct` | `paid_type=จ่ายบางส่วน` และไม่อยู่ 1–99 | **Error** | "กรอกเปอร์เซ็นต์ที่จ่ายระหว่าง 1–99" | §3.3ก · FN-31 |
| VR-11 | `doc_note` | `need_doc=true` และว่าง | **Error** | "ระบุเงื่อนไขเอกสารที่ต้องแนบ" | §3.3ก · FN-31 |
| VR-12 | `carry_expiry` | `carry_max > 0` และว่าง หรือไม่อยู่ในปีถัดไป | **Error** | "ระบุวันหมดอายุยกยอดในปีถัดไป" | BR-12 · FN-09 |
| VR-13 | `hr_leave_milestone` | ช่วงอายุงานทับซ้อนหรือมีช่องว่าง | **Error** | "ช่วงอายุงาน [x–y] ทับซ้อน/ขาดช่วงกับ [a–b]" | BR-16 · FN-08 |
| VR-14 | `time_out` vs `time_in` | `time_out ≤ time_in` และ `overnight=false` | **Error** | "เวลาออกต้องมากกว่าเวลาเข้า หรือติ๊กข้ามวัน" | BR-17 · FN-14 |
| VR-15 | `hr_shift_break` | ช่วงพักอยู่นอกช่วงกะ | **Error** | "ช่วงพักต้องอยู่ในช่วงเวลาของกะ" | BR-17 |
| VR-16 | `workdays[]` | เลือก 0 วัน | **Error** | "เลือกวันทำงานอย่างน้อย 1 วัน" | §3.3ข |
| VR-17 | `holiday_date` | ซ้ำใน บริษัท+ปี เดียวกัน (ข้ามชุดด้วย) | **Prevent** | "วันที่นี้มีอยู่แล้วในชุด [ชื่อชุด]" | BR-09 · FN-17 |
| VR-18 | `source_date` | `holiday_type=ชดเชย` และว่าง/ไม่มีวันต้นทางจริง | **Error** | "ระบุวันหยุดต้นทางของวันหยุดชดเชย" | §3.3ค · FN-16 |
| VR-19 | `cut_day` vs `pay_day` | `cut_day > pay_day` ในงวดเดียวกัน | **Error** | "วันตัดเวลาต้องไม่เกินวันจ่ายในงวดเดียวกัน" | BR-11 · FN-18 |
| VR-20 | `period_from/to` (รอบประเมิน) | ทับซ้อนรอบอื่นในปีเดียวกัน | **Prevent** | "ช่วงประเมินทับซ้อนกับรอบ [ชื่อรอบ]" | BR-10 · FN-21 |
| VR-21 | `entry_from/to` | อยู่ก่อนช่วงประเมินเริ่ม | **Error** | "ช่วงเปิดกรอกต้องอยู่หลังหรือคร่อมช่วงประเมิน" | §3.3จ · FN-20 |
| VR-22 | `companies[]` | `company_scope=company` และเลือก 0 บริษัท | **Error** | "เลือกบริษัทอย่างน้อย 1 รายการ" | BR-13 · FN-22 |
| VR-23 | `code` | ซ้ำภายใน `group` + `company_scope` | **Error** | "รหัสค่านี้ถูกใช้แล้ว" | §6.2 |
| VR-24 | `name_th` | ว่าง หรือ > 80 ตัวอักษร | **Error** | "ชื่อค่าไม่เกิน 80 ตัวอักษร" | §6.2 |
| VR-25 | `payroll_code` | ประเภทที่จ่ายค่าจ้างแต่เว้นว่าง | **Warning** | "ยังไม่ระบุรหัสอ้างอิงจ่ายเงิน — Salary Structure จะจับคู่ไม่ได้" | BR-18 · FN-12 |
| VR-26 | ปุ่มบันทึกทุกจุด | กดซ้ำระหว่างประมวลผล | **Prevent** | ปุ่ม disable + loader | FN-92 |
| VR-27 | ปิดใช้ / ยกเลิก / ปิดงวด / เปิดงวด | ไม่ผ่านหน้ายืนยัน | **Prevent** | modal ยืนยันทุกครั้ง | FN-91 |
| VR-28 | ปิดใช้ค่าที่มี where-used | ยังไม่แสดงรายการปลายทาง | **Prevent** | modal แสดงรายการ feature ก่อนยืนยัน | BR-08 · FN-26 |
| VR-29 | ทุก field ที่เป็นคน | พิมพ์ชื่ออิสระแทนการเลือกจาก combobox | **Prevent** | combobox Employee Master เท่านั้น | BR-15 · FN-94 |
| VR-30 | `applies_to` | พยายามแก้ค่า | **Prevent** | read-only รอบนี้ (hook) | S-22 · FN-30 |

## 9.5 สรุประดับความยืดหยุ่น (Flexibility Attribution)

| Rule | Tag | ระดับ | เหตุผล | ที่มา |
|---|---|---|---|---|
| BR-01, BR-02, BR-03, BR-07, BR-08, BR-09, BR-10, BR-11, BR-12, BR-14, BR-15, BR-16, BR-17, BR-19, BR-20 | **FIXED** | — (ฝังในโค้ด/มติ) | เป็น invariant ของ HR-1 · audit append-only · #102 · หรือ validation เชิงโครงสร้างที่ไม่มีเหตุให้เปลี่ยน | ✅ ยืนยันจาก LOCK/มติใน LANE_BRIEF |
| **BR-04** | CONFIGURABLE | **Admin Panel** | Admin เปิด/ปิดการล็อกงวด · นาน ๆ ครั้ง · แค่เปลี่ยนค่า boolean | 🤖 AI-inferred (ระดับ Admin Panel — ปล่อยผ่านได้ · mark 🤖) |
| **BR-05** | CONFIGURABLE | **Admin Panel** | ตัวเลขขั้นต่ำตามกฎหมายแรงงานเปลี่ยนเมื่อกฎหมายเปลี่ยน — ต้องเป็นตารางที่มี `effective_date` **ห้าม hardcode** | 🤖 AI-inferred · **ยกเป็น OQ-STD-07 ใน §15** (กระทบกฎหมาย) |
| **BR-06** | CONFIGURABLE | **Admin Panel** | ค่าขั้นต่ำโควตา + สลับ เตือน/บล็อก · นาน ๆ ครั้ง | 🤖 AI-inferred |
| **BR-18** | CONFIGURABLE | **Admin Panel** | สลับ เตือน/บังคับ เมื่อ Salary Structure พร้อม | 🤖 AI-inferred |
| **BR-21** | CONFIGURABLE | **Admin Panel** | HR Admin ปิด/เปิดงวดเอง · รายเดือน · เปลี่ยนสถานะข้อมูล ไม่ใช่ logic | 🤖 AI-inferred |
| **BR-13** | **DYNAMIC** | **Rule Management** | ลำดับ resolve ค่า (บริษัทลูก → ค่ากลาง) เป็น logic หลายชั้น · ถ้ากลุ่มบริษัทขยายเป็น ภูมิภาค/กลุ่ม จะกลายเป็น 3–4 ชั้น | 🤖 AI-inferred + **DYNAMIC → บังคับลง §15 OQ (Q-09)** ตาม C23 |

**Escalation (C23):** rule ที่ 🤖 AI-inferred และระดับ **DYNAMIC/Engine Management** = **BR-13** → ลง §15 Open Questions (Q-09) ให้ stakeholder ยืนยันก่อนพัฒนา Phase 3 · rule ที่ 🤖 + Admin Panel (BR-04, BR-06, BR-18, BR-21) ปล่อยผ่านได้แต่ mark 🤖 ไว้ · **BR-05 แม้เป็น Admin Panel ก็ยกเป็น OQ เพิ่ม** เพราะเป็นตัวเลขทางกฎหมาย (Q-10)

---

# Section 10: Edge Cases

## 10.0 Scenario Ledger — S-01…S-35 ครบทุกข้อ (Lane Mode v2)

| S | ประเภท | ที่อยู่ใน BRD | FN |
|---|---|---|---|
| S-01 | Happy | §5 J-01…J-05 · ST-01, ST-10, ST-11 | FN-01,02,03,31,32 |
| S-02 | Happy | §5.2.2 · ST-03 · §8 T-07 | FN-04,05 |
| S-03 | Alt | §5.2.1 · ST-02 · §8 T-01,T-04 | FN-06 |
| S-04 | Alt | §5.2.3 · ST-04 · §8 T-06 | FN-07 |
| S-05 | Alt | §5.3 E-06 · ST-06 · §6.4 | FN-08 |
| S-06 | Alt | §5.3 E-08 · ST-07 | FN-09 |
| S-07 | Alt | ST-08 · §6.4 field 7–8 | FN-10 |
| S-08 | Happy | §5 J-03 · ST-12, ST-13 | FN-11,12 |
| S-09 | Exception | §5.3 E-01 · ST-14 · §10.1 EC-01 | FN-13 |
| S-10 | Happy | ST-15 · §6.5 | FN-14 |
| S-11 | Happy | ST-16, ST-17 · §6.6 | FN-15,16 |
| S-12 | Exception | §5.3 E-03 · ST-19 · §10.1 EC-03 | FN-17 |
| S-13 | Happy | ST-20, ST-22 · §6.7 | FN-18,50 |
| S-14 | Exception | §5.3 E-02 · ST-31 · §10.1 EC-02 | FN-19 |
| S-15 | Happy | ST-23 · §6.8 | FN-20 |
| S-16 | Exception | §5.3 E-04 · ST-24 · §10.1 EC-04 | FN-21 |
| S-17 | Alt | ST-25, ST-26 · §9.1 BR-13 | FN-22,23 |
| S-18 | Alt | §5.2.4, §5.2.5 · ST-28 · §8 T-08,T-09,T-10 | FN-24,25 |
| S-19 | Exception | §5.2.4 A4-1 · ST-29, ST-30 · §6.9 | FN-26,33 |
| S-20 | Alt | §5.2.7 · ST-05 | FN-27,28 |
| S-21 | Alt | ST-09 · §6.4 field 16–17 | FN-29 |
| S-22 | Alt | ST-27 · §6.2 field 8 | FN-30 |
| S-31 | Happy | §5.2.6 · ST-21 · §8.3 · §6.7 | FN-48 |
| S-32 | Alt | ST-18 · §6.6 field 3 | FN-49 |
| S-23 | **ไม่รองรับ** | §3.2 OUT-01 · §14.6 | FN-40 |
| S-24 | **ไม่รองรับ** | §3.2 OUT-02 · §14.6 | FN-41 |
| S-25 | **ไม่รองรับ** | §3.2 OUT-03 · §14.6 | FN-42 |
| S-26 | **ไม่รองรับ** | §3.2 OUT-04 · §14.6 | FN-43 |
| S-27 | **ไม่รองรับ** | §3.2 OUT-05 · §14.6 | FN-44 |
| S-28 | **ไม่รองรับ** | §3.2 OUT-06 · §14.6 | FN-45 |
| S-29 | **ไม่รองรับ** | §3.2 OUT-07 · §14.6 | FN-46 |
| S-30 | **ไม่รองรับ** | §3.2 OUT-08 · §14.6 | FN-47 |
| S-33 | **ไม่รองรับ** | §3.2 OUT-09 · §14.6 | FN-51 |
| S-34 | **ไม่รองรับ** | §3.2 OUT-10 · §14.6 | FN-52 |
| S-35 | **ไม่รองรับ** | §3.2 OUT-11 · §14.6 | FN-53 |

**รวม 35 scenario — in scope 24 · ไม่รองรับ 11 · ครบ**

## 10.1 Edge Cases ที่ระบุจากต้นทาง (PREBRIEF/FUNCTION_CHECKLIST — default ☑ ยืนยันแล้ว)

| # | Edge Case | หมวด | ผลที่ต้องการ | trace |
|---|---|---|---|---|
| ☑ EC-01 | ตั้งตัวคูณ OT 1.2x สำหรับ OT วันทำงาน | **VA (Validation)** | บล็อก + บอกขั้นต่ำ 1.5 · ค้างที่ขั้นเดิมของ wizard | S-09 · BR-05 |
| ☑ EC-02 | ตั้งวันมีผลย้อนเข้างวดที่ปิดแล้ว | **ST (Status/Workflow)** | บล็อก + บอกวันแรกที่ตั้งได้ | S-14 · BR-04,21 |
| ☑ EC-03 | เพิ่มวันหยุดซ้ำวันเดิม (ทั้งในชุดและข้ามชุดของบริษัท+ปีเดียวกัน) | **DI (Data Integrity)** | บล็อก + ชี้รายการเดิม | S-12 · BR-09 |
| ☑ EC-04 | สร้างรอบประเมินที่คร่อมรอบเดิม | **DI** | บล็อก + แสดงชื่อรอบที่ชน | S-16 · BR-10 |
| ☑ EC-05 | ตั้งโควตาลาพักร้อนต่ำกว่าขั้นต่ำกฎหมาย | **VA** | เตือน ไม่บล็อก · ยืนยันแล้วบันทึกได้ | S-01 · BR-06 |
| ☑ EC-06 | ปิดใช้ค่าที่ยังมี feature ปลายทางอ้างอยู่ | **PM (Permission/Impact)** | เตือน + แสดง where-used + บังคับเหตุผล | S-19 · BR-08 |
| ☑ EC-07 | milestone อายุงานมีช่องว่างหรือทับซ้อน | **CL (Calculation)** | บล็อก + ชี้ช่วง | S-05 · BR-16 |
| ☑ EC-08 | กะข้ามวันโดยไม่ติ๊ก "ข้ามวัน" | **CL** | บล็อก | S-10 · BR-17 |
| ☑ EC-09 | ยกยอด > 0 แต่ไม่ระบุวันหมดอายุ | **VA** | บล็อก | S-06 · BR-12 |
| ☑ EC-10 | วันตัดเวลามากกว่าวันจ่าย | **VA** | บล็อก | S-13 · BR-11 |
| ☑ EC-11 | เลือก "เฉพาะบริษัท" แต่ไม่เลือกบริษัท | **VA** | บล็อก | S-17 · BR-13 |
| ☑ EC-12 | `effective_date` ซ้ำ/คร่อมกับเวอร์ชันเดิม | **DI** | บล็อก + แสดงเวอร์ชันที่ชน | S-02 · BR-03 |
| ☑ EC-13 | ประเภทที่จ่ายค่าจ้างแต่ไม่มี `payroll_code` | **DI** | เตือนเบา ไม่บล็อก | S-25 · BR-18 |
| ☑ EC-14 | เปิดงวดที่ปิดแล้วกลับโดยไม่ให้เหตุผล | **ST** | บล็อก + บังคับเหตุผล + audit | S-31 · BR-21 |
| ☑ EC-15 | กดบันทึกซ้ำระหว่างประมวลผล | **CA (Concurrent Access)** | disable ปุ่ม + loader | FN-92 |

## 10.2 Edge Cases จาก AI Pattern Matching (default ☐ — BA ต้อง confirm ที่ SOW3.7)

> ☐ = "แนะนำ" — dev ยังไม่ต้อง implement จนกว่า BA ติ๊ก ☑ หรือ FRD ระบุ · ข้อที่กระทบเงิน/สิทธิ์/ข้อมูลสูญหาย → **ยกเป็น Open Question ทันที** (ทำเครื่องหมาย 🔺)

### CA (Concurrent Access) Patterns
- ☐ **EA-01** HR Admin สองคนสร้างเวอร์ชันของค่าเดียวกันด้วย `effective_date` เดียวกันพร้อมกัน → คนที่บันทึกทีหลังต้องถูกบล็อกด้วย BR-03 ไม่ใช่เขียนทับ (optimistic lock ที่ `config_item_id + effective_date`)
- ☐ 🔺 **EA-02** ปิดงวดขณะที่อีกคนกำลังบันทึกเวอร์ชันที่มีผลในงวดนั้น → ต้อง re-validate BR-04 ตอน commit ไม่ใช่ตอนเปิดฟอร์ม (**กระทบสิทธิ์/เงิน → Q-13**)
- ☐ **EA-03** ปิดใช้ค่าขณะที่อีกคนเปิด drawer แก้ค่าเดียวกันค้างอยู่ → ตอน submit ต้องแจ้งว่าค่าถูกปิดใช้แล้ว

### ST (Status/Workflow) Patterns
- ☐ **EA-04** scheduler ไม่ทำงาน (ระบบล่ม) ตรงวันมีผลพอดี → เมื่อกลับมาต้อง catch-up เปลี่ยน Scheduled→Active ย้อนหลังให้ครบ ไม่ข้าม
- ☐ 🔺 **EA-05** มีเวอร์ชัน Scheduled หลายเวอร์ชันซ้อนกันในอนาคต (v3 eff 2027-01-01 · v4 eff 2027-07-01) แล้วยกเลิก v3 → v4 ต้องยังคงอยู่ และ `effective_to` ของ v2 ต้องคำนวณใหม่ (**กระทบสิทธิ์ → Q-14**)
- ☐ **EA-06** เปิดใช้กลับค่าที่ปิดใช้ไปแล้วโดยตั้งวันมีผลย้อนหลัง → ต้องถูก BR-04 บล็อกเหมือนกรณีปกติ
- ☐ **EA-07** ค่าที่มีเฉพาะเวอร์ชัน Draft (ยังไม่เคย publish) ถูกกดปิดใช้ → ควรเป็นการทิ้งร่าง ไม่ใช่ soft archive

### CL (Calculation) Patterns
- ☐ **EA-08** กะข้ามวันที่มีช่วงพักคร่อมเที่ยงคืน (เข้า 22:00 พัก 00:30–01:00 ออก 06:00) → คำนวณ ชม./วัน ต้องถูกต้อง
- ☐ **EA-09** ปีอธิกสุรทิน (29 ก.พ.) ในการสร้างงวดทั้งปีและวันหมดอายุยกยอด
- ☐ **EA-10** วันตัด/วันจ่าย = 31 ในเดือนที่มี 30 วันหรือกุมภาพันธ์ → ต้อง fallback เป็นสิ้นเดือน
- ☐ **EA-11** milestone ขั้นสุดท้ายที่ `year_to` = null (ขึ้นไป) — BR-16 ต้องถือว่าไม่มีช่องว่าง

### DI (Data Integrity / Lookup Master) Patterns
- ☐ **EA-12** บริษัทลูกที่ถูกอ้างใน `companies[]` ถูกปิดใช้ที่ Organization → soft ref ต้องยังแสดงชื่อเดิมได้ (snapshot) ไม่พัง (LD-4C-02)
- ☐ **EA-13** พนักงานที่เป็น `owner_employee_id` ลาออก → ยังต้องแสดงชื่อในประวัติเวอร์ชันได้
- ☐ **EA-14** วันหยุดชดเชยที่อ้างวันต้นทาง แล้ววันต้นทางถูกลบออกจากชุด → ต้องบล็อกการลบวันต้นทาง หรือเตือนก่อน

### PM (Permission) Patterns
- ☐ **EA-15** HR Staff เปิด URL ของ drawer สร้างค่าโดยตรง → ต้องถูกปฏิเสธที่ระดับสิทธิ์ ไม่ใช่แค่ซ่อนปุ่ม
- ☐ 🔺 **EA-16** feature ปลายทางขอค่าโดยไม่ส่ง "วันที่" มาด้วย → ต้องปฏิเสธหรือ default เป็นวันนี้อย่างชัดเจน (**สัญญากับ 8 feature → Q-15**)

### EM (Notification) Patterns — เกี่ยวข้องแม้ไม่ประกาศท่อ NTF
- ☐ **EA-17** เวอร์ชันที่ Scheduled ถึงวันมีผลแล้วแต่ไม่มีใครรู้ → รอบนี้ไม่แจ้งจากที่นี่ (OQ-STD-05) แต่ feature ปลายทางต้องอ่านค่าใหม่ทันทีในการเรียกครั้งถัดไป ไม่ cache ข้ามวัน

### Tag Review Report
```
✅ BR-01,02,03,07,08,09,10,11,12,14,15,16,17,19,20: FIXED — ถูกต้อง (invariant/มติ)
✅ BR-04,05,06,18,21: CONFIGURABLE + ระดับ Admin Panel — ถูกต้อง
⚠️ BR-05: แม้ระดับ Admin Panel แต่เป็นตัวเลขทางกฎหมาย → ต้องมีตาราง legal minimum ที่มี effective_date เอง (ยก OQ Q-10)
✅ BR-13: DYNAMIC + Rule Management — ถูกต้อง (หลายชั้น) → บังคับลง OQ (Q-09) ตาม C23
❌ ไม่มี rule ที่มีตัวเลข/เงื่อนไขแล้วไม่ติด Tag — ครบทั้ง 21 ข้อ
```

---

# Section 11: Impact Analysis / Regression Scope

**N/A — BRD ประเภท New Feature**
- ไม่มี artifact เดิมของ feature นี้ (LANE_BRIEF: "ประเภทงาน = new · ไม่มี artifact เดิม")
- ไม่มี "ของเก่า vs ของใหม่" และไม่มี Regression Scope ของ feature เดิมที่ต้อง test ซ้ำ
- **ผลกระทบข้ามระบบ** (ซึ่งมีจริงและสำคัญมากสำหรับ feature นี้) อยู่ที่ **§12.1 Value Stream & Downstream Impact Map** ไม่ใช่ที่นี่
- **Data migration:** มี — ค่านโยบายที่วันนี้อยู่ใน Excel/อีเมล ต้องถูกนำเข้าเป็น "เวอร์ชันแรก" พร้อม `effective_date` ย้อนหลังตามจริง (seed ตอน go-live · ดู §13 Phase 1 · §14.1)

---

# Section 12: System Context & Cross-Module Impact ⭐

## 12.1 Value Stream & Downstream Impact ⭐

**Positioning:** HR Configuration เป็น **ต้นน้ำสุดของ Value Stream "Hire-to-Retire" ฝั่งกติกา** — ไม่ได้อยู่ในสายเอกสารธุรกรรม แต่เป็น **แหล่งพารามิเตอร์** ที่ทุกเอกสาร HR ต้องอ่านก่อนคำนวณ
> อ้าง `knowledge/CONTEXT_PACK/HR.md` data flow แถวแรก: `HR Configuration ──(ประเภทลา/โควตา/อัตรา OT/ปฏิทิน/กะ/รอบ · effective_date)──> ทุก feature`
> **ยังไม่ได้ confirm กับ VS Bible โดยตรง** (`cube-master-knowledge` เข้าถึงผ่าน catalog/current-state เท่านั้นในเลนนี้) → ดู §15 Q-16

**Upstream (feature นี้รับอะไรเข้ามา):**

| ต้นทาง | ข้อมูลที่รับ | รูปแบบ | สถานะ |
|---|---|---|---|
| **Employee Master** ✅ | คน / ตำแหน่ง / แผนก → combobox ผู้รับผิดชอบ + audit fields + ผู้ปิดงวด | soft ref (#102) | เสร็จแล้ว |
| **Organization** ✅ | รายชื่อบริษัทลูก → `companies[]` | soft ref (nullable · no cascade) | เสร็จแล้ว |
| **Roles & Permissions / Data Masking (Policy Center)** ✅ | สิทธิ์เห็น-แก้ | เรียกใช้ | เสร็จแล้ว |
| **Audit Trail (Policy Center)** | ปลายทางของ log ทุก transition | เรียกใช้ (append-only) | baseline |
| **กฎหมายแรงงานไทย** (ภายนอก) | ขั้นต่ำ OT 1.5/1.0/3.0 · ลาพักร้อน 6 วัน | ตารางค่า legal minimum ที่มี `effective_date` เอง | ดู Q-10 |

**Downstream Impact Map — "แล้วไงต่อ" ตอบได้ทุกแถว (8 consumer + 1 engine):**

| ปลายทาง | ข้อมูลที่ไหลไป | Trigger | ถ้าค่าที่นี่เปลี่ยน/ถูกปิดใช้ จะกระทบยังไง | สถานะ |
|---|---|---|---|---|
| **Leave** (W2) | ประเภทลา · โควตา/milestone · ยกยอด · prorate · counting rule · เงื่อนไขเอกสาร | ทุกครั้งที่คำนวณสิทธิ์/สร้างใบลา (ขอพร้อมวันที่) | เปลี่ยนโควตา → ใบลาที่ยื่น**หลัง**วันมีผลใช้ค่าใหม่ · ใบลาเดิมยังอิงเวอร์ชันที่ Active ตอนนั้น (ไม่ retro) · ปิดใช้ประเภทลา → เลือกใหม่ไม่ได้ แต่ใบลาเดิมยังอ่านได้ · **balance เป็นของ Leave ไม่ใช่ที่นี่** [OQ-HR-02] | ⏳ ยังไม่ทำ |
| **OT / Shift** (W2) | อัตรา OT ต่อประเภท · ฐานคำนวณ · เพดาน ชม./สัปดาห์ · `payroll_code` | ทุกครั้งที่สร้าง/อนุมัติใบ OT | เปลี่ยนตัวคูณ → ใบ OT ที่เกิดหลังวันมีผลคิดอัตราใหม่ · ใบเดิมคงอัตราเดิม (snapshot ที่ปลายทาง) · ลดเพดาน → ใบ OT ที่เกินเพดานใหม่ต้องถูกเตือนที่ OT ไม่ใช่ที่นี่ | ⏳ |
| **Shift & Roster** (W2) | กะมาตรฐาน (pattern ตั้งต้น) · ปฏิทินวันหยุด (+ `location`) | ตอนจัดตารางกะ | แก้กะมาตรฐาน → ตารางที่ **เผยแพร่แล้ว** ไม่เปลี่ยน (Roster ถือ snapshot) · ตารางที่ยังไม่เผยแพร่ใช้ pattern ใหม่ · ปิดใช้กะ → เลือกใหม่ไม่ได้ | ⏳ |
| **Attendance** (W1/C) | ปฏิทินวันหยุด · กะ · **วันตัดเวลา** · งวด (open/closed) | ทุกวันที่ประมวลผลเวลา + ตอนปิดยอดงวด | เพิ่มวันหยุดย้อนหลังในงวดที่ยัง open → Attendance ต้องคำนวณใหม่ · **งวดที่ closed แก้ไม่ได้ (BR-04/BR-21)** จึงไม่มีการคำนวณย้อน | ⏳ |
| **Payroll** (W4) | **รอบจ่าย + งวดจริง** · อัตรา OT · `payroll_code` | ตอนเปิด/ปิดรอบจ่าย | เปลี่ยนวันจ่าย → มีผลกับงวดที่ยังไม่สร้าง/ยังไม่ปิดเท่านั้น · **สูตรคำนวณเงินไม่ได้อยู่ที่นี่** [OQ-STD-03] · ปิดงวดที่นี่ = Payroll ล็อกยอดงวดนั้น | ⏳ |
| **Performance** (W5) | รอบประเมิน (ช่วงประเมิน · ช่วงเปิดกรอก · ความถี่) | ตอนเปิดรอบประเมิน | เลื่อนช่วงเปิดกรอก → รอบที่ยังไม่เปิดใช้ค่าใหม่ · รอบที่เปิดแล้วไม่ย้อน · **แบบฟอร์ม/หัวข้อประเมินเป็นของ Performance** | ⏳ |
| **Welfare** (W4) | นโยบายสิทธิ์ที่เกี่ยวข้อง (อ่านอย่างเดียว) | ตอนตรวจสิทธิ์สวัสดิการ | เปลี่ยนนโยบาย → สิทธิ์ที่ใช้หลังวันมีผลเปลี่ยนตาม | ⏳ |
| **Salary Structure** (W1/B) | **รอบจ่าย** · `payroll_code` | ตอนจับคู่องค์ประกอบค่าจ้าง | เปลี่ยน `payroll_code` → Salary Structure จับคู่ใหม่ · **ถ้าเว้นว่าง จับคู่ไม่ได้** (BR-18 เตือน) | ⏳ |
| **ENG-CSQ 7C (SecC)** | event ทุกครั้งที่เวอร์ชันมีผล/ถูกยกเลิก/ปิดใช้/เปิดกลับ/ปิดงวด | 6 event (E1–E6 ใน CSQ_BRIEF) | เปลี่ยนนโยบาย = **เปลี่ยนสิทธิ์/entitlement ของพนักงาน** → ต้องมี consequence record ที่ 7C · **ประกาศได้เฉพาะ SecC** (OC/DC-เอกสาร/SC = 422) | baseline |

**ผลกระทบแนวขวาง:**

| ด้าน | กระทบอย่างไร |
|---|---|
| **บัญชี / GL** | ทางอ้อมผ่าน Payroll เท่านั้น — รอบจ่ายเปลี่ยน = งวดที่ลง GL เปลี่ยน · **feature นี้ไม่แตะ GL โดยตรง** |
| **งบประมาณ** | ไม่กระทบโดยตรง (ไม่มีจำนวนเงินในหน้านี้) — ผลจริงเกิดที่ Payroll/Welfare |
| **รายงาน** | ทุกรายงาน HR ที่อ้าง "กติกา ณ ช่วงเวลา" ต้องอ่านผ่าน resolve(date) ไม่ใช่ค่าปัจจุบัน มิฉะนั้นรายงานย้อนหลังจะผิด |
| **กฎหมาย/ตรวจสอบ** | ประวัติเวอร์ชัน = หลักฐานทางกฎหมาย — ถ้า audit trail ขาดช่วง จะตอบข้อพิพาทแรงงานไม่ได้ (นี่คือเหตุผลที่ BR-14 เป็น FIXED) |
| **ทุก feature HR ที่ยังไม่ทำ (18 ตัว)** | ต้อง **ห้ามสร้างหน้า config ของตัวเอง** (#107) — ทุกตัวอ้างมาที่นี่ผ่านลิงก์ "จัดการที่ HR Configuration" |

**Document flow chain:**
```
[กฎหมาย/นโยบายบริษัท] → HR Configuration (เวอร์ชัน + effective_date)
        │
        ├─ resolve(date, company) ─→ Leave ─→ ใบลา ─→ Attendance ─→ Payroll ─→ payslip ─→ ESS
        ├─ resolve(date, company) ─→ OT/Shift ─→ ใบ OT ─→ Payroll
        ├─ resolve(date, company) ─→ Shift & Roster ─→ ตารางกะ ─→ Attendance
        ├─ resolve(date, company) ─→ Performance ─→ รอบประเมิน ─→ Employee Movement
        └─ event SecC ─→ ENG-CSQ 7C (consequence ของการเปลี่ยนสิทธิ์)
```

## 12.2 Module & External Dependencies

| Dependency | ประเภท | ใช้ทำอะไร | สถานะ | ถ้าไม่มีจะเป็นยังไง |
|---|---|---|---|---|
| Employee Master | Module (internal) | combobox คนทุกช่อง (#102) | ✅ เสร็จ | ไม่มี — dep พร้อมแล้ว |
| Organization | Module (internal) | รายชื่อบริษัทลูก | ✅ เสร็จ | — |
| Roles & Permissions / Data Masking (Policy Center) | Baseline engine | สิทธิ์เห็น-แก้ | ✅ | ห้ามทำ permission เอง [OB-15] |
| Audit Trail (Policy Center) | Baseline engine | เขียน log append-only ทุก transition | ✅ | ห้ามทำ audit เอง [OB-15] |
| ENG-CSQ 7C | Baseline engine | รับ event SecC | ✅ | ประกาศผ่าน `5_DECLARATIONS/CSQ_BRIEF.md` |
| Scheduler / job runner | Infra | เปลี่ยน Scheduled→Active ตามวัน · Active→Superseded | ต้องมี | ถ้าไม่มี ต้อง resolve แบบ lazy ตอนอ่าน (ดู §14.3) |
| DOA Engine · Document Configuration · ENG-NOTIFY · Operation Process | Baseline engine | **ไม่ใช้ในรอบนี้** | — | ประกาศไว้ที่ `5_DECLARATIONS/NOT_NEEDED.md` |
| External: ประกาศวันหยุดราชการรายปี | External | รอบนี้กรอกมือ | — | auto-import = OUT-06 |

## 12.3 Existing System Reference

| Rule / ความสามารถ | ระดับ | มีอยู่แล้ว? | Reference |
|---|---|:---:|---|
| BR-14 audit append-only | Engine (baseline) | ✅ | **Policy Center → Audit Trail** — เรียกใช้ ห้ามสร้างใหม่ |
| §4 Permission Matrix | Engine (baseline) | ✅ | **Policy Center → Roles & Permissions / Data Masking** |
| BR-15 combobox คน | Component (baseline) | ✅ | **Employee Master** combobox #102 |
| §6.2 `companies[]` | Master (baseline) | ✅ | **Organization** |
| event SecC (§8) | Engine (baseline) | ✅ | **ENG-CSQ 7C** — ประกาศ SecC เท่านั้น |
| BR-04, BR-05, BR-06, BR-18, BR-21 (Admin Panel) | Admin Panel | ❌ **ยังไม่มี** | ต้องสร้างใหม่ใน Phase 2 — ตาราง parameter ของ feature นี้เอง (`hr_config_param`) |
| BR-13 ลำดับ resolve | Rule Management | ❌ **ยังไม่มี** | ต้องสร้างใน Phase 3 — engine candidate `hr-config-resolve` |
| retro recalculation (OUT-02) | Engine Management | ❌ **ยังไม่มี** | Phase 4 ถ้า OQ-STD-04 เคาะกลับ — engine candidate `hr-policy-retro-engine` |
| eligibility นอกเหนือบริษัท (OUT-12) | Rule Management | ❌ **ยังไม่มี** | Phase 3/4 ถ้า OQ-STD-02 เคาะกลับ — engine candidate `hr-eligibility-rule-engine` |
| approval ตอนแก้ค่านโยบาย (OUT-01) | Engine (baseline) | ✅ **DOA Engine มีอยู่แล้ว** | ถ้า OQ-STD-01 เคาะว่าต้องมี → เรียก `GET /doa/resolve` ที่ T-02 จุดเดียว **ห้ามสร้าง approval ใหม่** |
| **⚠️ ไม่มี `System_Module_Registry.md/.csv` ในเวิร์กสเปซนี้** | — | — | ตารางนี้อ้างจาก `knowledge/CONTEXT_PACK/HR.md` + current-state §2 baseline แทน · ขอ Registry ภายหลังเพื่อความสมบูรณ์ (§15 Q-17) |

---

# Section 13: Delivery Phases

## Phase 1: Feature Launch (ต้องเสร็จก่อน go-live)

| # | งาน | รายละเอียด |
|---|---|---|
| P1-01 | **โครงข้อมูล 2 ชั้น** | `hr_config_item` + `hr_config_version` + payload 11 ตาราง ตาม §6 · audit fields ครบทุกตาราง · **ไม่มี hard delete ที่ใดเลย** |
| P1-02 | **Config Table + Seed** ของทุก rule ที่ไม่ใช่ FIXED | BR-04, BR-05, BR-06, BR-18, BR-21 → เก็บใน `hr_config_param` **ห้าม hardcode ตั้งแต่วันแรก** (แม้ Admin Panel จะยังไม่มี UI ใน Phase 1) |
| P1-03 | **ตาราง legal minimum** | ขั้นต่ำ OT (1.5/1.0/3.0) + โควตาลาพักร้อนขั้นต่ำ (6) เก็บเป็นแถวที่มี `effective_date` ของตัวเอง — กฎหมายเปลี่ยนแล้วไม่ต้องแก้โค้ด |
| P1-04 | **State machine 5 states + scheduler** | T-01…T-11 · job เปลี่ยน Scheduled→Active รายวัน + **catch-up ย้อนหลังถ้า job ขาด** (EA-04) |
| P1-05 | **สัญญาการอ่านค่า `resolve(date, company)`** | จุดเดียวที่ 8 feature ปลายทางเรียก · บังคับส่ง "วันที่" เสมอ · resolve ตาม BR-13 · **Draft/Scheduled ไม่ถูกคืน** (BR-19) |
| P1-06 | **สร้างงวดทั้งปี + ปิด/เปิดงวด** | `hr_pay_period` — เป็นฐานของ BR-04 ต้องมีตั้งแต่ Phase 1 ไม่งั้น BR-04 บังคับไม่ได้ |
| P1-07 | **where-used registry** | `hr_config_usage` + Module Linkage (manual status override) สำหรับ consumer 8 ตัวที่ยัง ⏳ |
| P1-08 | **เชื่อม baseline** | Policy Center Audit Trail (append-only) · Roles & Permissions · Employee Master combobox · Organization · **event SecC → ENG-CSQ** |
| P1-09 | **Data migration / seed** | นำค่านโยบายที่อยู่ใน Excel/อีเมลวันนี้เข้าเป็นเวอร์ชันแรก พร้อม `effective_date` ย้อนหลังตามจริง (ทำครั้งเดียวตอน go-live · ต้องบันทึกว่าเป็น migration ใน audit) |
| P1-10 | **ประกาศขอบเขตบนจอ** | 11 ข้อที่ไม่รองรับต้องเห็นบนหน้าจอผ่าน ⓘ `.tip` (#106 — ห้าม hint banner) ไม่ใช่เงียบ |

## Phase 2: Admin Panel

| Rule | ต้องทำอะไร |
|---|---|
| BR-04 | หน้าตั้งค่า: เปิด/ปิด `lock_closed_period` |
| BR-05 | หน้าตั้งค่า: แก้ตาราง legal minimum ต่อประเภทอัตรา (พร้อม `effective_date` ของตัวเอง) |
| BR-06 | หน้าตั้งค่า: ค่าขั้นต่ำโควตา + สลับ เตือน/บล็อก |
| BR-18 | หน้าตั้งค่า: สลับ `payroll_code` เตือน ↔ บังคับ (เปิดใช้เมื่อ Salary Structure พร้อม) |
| BR-21 | หน้าตั้งค่า: นโยบายการเปิดงวดกลับ (ใครทำได้ · ต้องมีเหตุผลไหม) |

## Phase 3: Rule Management

| Rule | ต้องทำอะไร | engine candidate |
|---|---|---|
| BR-13 | จัดการลำดับ resolve ค่าเป็นกฎที่แก้ได้ (บริษัทลูก → ค่ากลาง · เผื่อขยายเป็น บริษัท → ภูมิภาค → กลุ่ม) — **รอ Q-09 เคาะก่อน** | **`hr-config-resolve`** |
| OUT-12 / OQ-STD-02 | eligibility นอกเหนือระดับบริษัท (ประเภทจ้าง/ระดับ/แผนก) ที่ field `applies_to` — **รอ OQ-STD-02 เคาะ** | **`hr-eligibility-rule-engine`** |

## Phase 4: Engine Management

| ประเด็น | ต้องทำอะไร | engine candidate |
|---|---|---|
| OUT-02 / OQ-STD-04 | คำนวณย้อนหลังเมื่อแก้นโยบายคร่อมงวดที่ปิดแล้ว — **รอ OQ-STD-04 เคาะ · ถ้าเคาะว่าไม่ทำ Phase นี้ไม่เกิด** | **`hr-policy-retro-engine`** |
| OUT-01 / OQ-STD-01 | ถ้าเคาะว่าต้องมี approval → **เรียก DOA Engine ที่มีอยู่** ที่ transition T-02 จุดเดียว — **ไม่ใช่ engine ใหม่** | (ใช้ DOA Engine เดิม) |

> **engine candidate ที่ต้องส่งให้ Architect:** `hr-config-resolve` · `hr-policy-retro-engine` · `hr-eligibility-rule-engine` — ทั้ง 3 ตัวจะถูกยืนยัน/ระบุสัญญาใน **FRD §3.2**

---

# Section 14: Dev Requirements Summary "ใบสั่ง"

## 14.1 Config Foundation ที่ต้องเตรียม

| # | โครงสร้าง | รองรับ Rule ไหน | มีอยู่แล้ว? |
|---|---|---|---|
| CF-01 | `hr_config_item` + `hr_config_version` (2 ชั้น) | BR-01, BR-02, BR-03, BR-19, BR-20 | ❌ สร้างใหม่ |
| CF-02 | payload 11 ตาราง (`hr_leave_policy`/`_milestone`, `hr_ot_rate`, `hr_shift_pattern`/`_break`, `hr_holiday_calendar`/`_day`, `hr_period_rule`/`hr_pay_period`, `hr_appraisal_cycle`) | BR-05…BR-12, BR-16, BR-17, BR-21 | ❌ สร้างใหม่ |
| CF-03 | `hr_config_param` (ตารางพารามิเตอร์ของ feature เอง + seed) | BR-04, BR-05, BR-06, BR-18, BR-21 | ❌ สร้างใหม่ — **ห้าม hardcode ตั้งแต่วันแรก** |
| CF-04 | ตาราง legal minimum (มี `effective_date` เอง) | BR-05, BR-06 | ❌ สร้างใหม่ |
| CF-05 | `hr_config_usage` + Module Linkage | BR-08, FN-33 | ❌ สร้างใหม่ |
| CF-06 | State machine 5 states + scheduler + catch-up | §8 T-01…T-11 | ❌ สร้างใหม่ |
| CF-07 | สัญญา `resolve(date, company)` | BR-13, BR-19 | ❌ สร้างใหม่ — **จุดเดียวที่ปลายทางเรียก** |
| CF-08 | Audit Trail (append-only) | BR-14 | ✅ **ใช้ Policy Center ที่มีอยู่แล้ว ไม่ต้องสร้างใหม่** |
| CF-09 | Roles & Permissions / Data Masking | §4 | ✅ **ใช้ Policy Center ที่มีอยู่แล้ว** |
| CF-10 | combobox Employee Master (#102) · Organization | BR-15, §6.2 | ✅ **ใช้ของเดิม** |
| CF-11 | event bus → ENG-CSQ (SecC) | §8 · CSQ_BRIEF E1–E6 | ✅ **ใช้ ENG-CSQ ที่มีอยู่แล้ว — ประกาศ SecC เท่านั้น** |

## 14.2 ข้อกำหนดจาก Tag

| Rule | Tag | ระดับ | Dev ต้องทำอะไร (ชัดเจน) |
|---|---|---|---|
| BR-04 | CONFIGURABLE | Admin Panel | เก็บ `lock_closed_period` ใน `hr_config_param` · อ่านค่าตอน validate `effective_date` **ไม่ใช่ `if(true)`** |
| BR-05 | CONFIGURABLE | Admin Panel | ขั้นต่ำ OT อ่านจาก **ตาราง legal minimum ที่ join ด้วย `effective_date`** — ห้ามเขียน `1.5` ในโค้ด |
| BR-06 | CONFIGURABLE | Admin Panel | ค่าขั้นต่ำโควตา + โหมด (เตือน/บล็อก) อ่านจาก `hr_config_param` |
| BR-18 | CONFIGURABLE | Admin Panel | โหมด `payroll_code` (เตือน/บังคับ) อ่านจาก `hr_config_param` |
| BR-21 | CONFIGURABLE | Admin Panel | นโยบายการเปิดงวดกลับอ่านจาก `hr_config_param` · ทุกครั้งเขียน audit |
| BR-13 | **DYNAMIC** | **Rule Management** | Phase 1 implement เป็น **ตารางลำดับ resolve** (ไม่ใช่ if-else ในโค้ด) เพื่อยกเป็น Rule Management ได้ใน Phase 3 โดยไม่ต้อง refactor — **รอ Q-09 ยืนยันก่อนเริ่ม Phase 3** |
| BR-01, BR-02, BR-03, BR-07, BR-08, BR-09…BR-12, BR-14…BR-17, BR-19, BR-20 | FIXED | — | implement ตรงตามข้อความ · **BR-07 ห้ามมี endpoint ลบถาวรแม้แต่ตัวเดียว** · BR-14 เรียก Policy Center ไม่เขียน audit เอง |

## 14.3 ข้อกำหนดจาก Edge Cases / Validation

| # | Dev ต้อง handle เป็นพิเศษ | มาจาก |
|---|---|---|
| D-01 | **Re-validate BR-04 ตอน commit ไม่ใช่ตอนเปิดฟอร์ม** — งวดอาจถูกปิดระหว่างที่ผู้ใช้กรอกอยู่ | EA-02 🔺 |
| D-02 | **Optimistic lock ที่ `config_item_id + effective_date`** — สองคนสร้างเวอร์ชันชนกันต้องแพ้ทางที่ BR-03 ไม่ใช่เขียนทับ | EA-01 |
| D-03 | **Scheduler catch-up** — ถ้า job ขาดไปหลายวัน ต้องเปลี่ยน Scheduled→Active ย้อนให้ครบตามลำดับวัน ไม่ข้าม · ทางเลือกที่ปลอดภัยกว่าคือ resolve แบบ lazy (คำนวณสถานะจาก `effective_date` ตอนอ่าน) — เลือกทางใดต้องระบุใน FRD | EA-04 |
| D-04 | **ยกเลิกเวอร์ชัน Scheduled ที่มีเวอร์ชันอื่นซ้อนอยู่ข้างหลัง** → ต้องคำนวณ `effective_to` ของเวอร์ชันก่อนหน้าใหม่ | EA-05 🔺 |
| D-05 | **BR-09 ต้องตรวจข้ามชุดปฏิทิน** ไม่ใช่แค่ในชุดเดียวกัน (บริษัท + ปี เป็น key) | EC-03 · S-32 |
| D-06 | **กะข้ามวัน + ช่วงพักคร่อมเที่ยงคืน** — คำนวณ ชม./วัน ด้วยเวลาเชิงเส้น ไม่ใช่ modulo 24 ตรง ๆ | EA-08 |
| D-07 | **วันตัด/วันจ่าย = 31 หรือ "สิ้นเดือน"** — ต้อง fallback ตามจำนวนวันจริงของเดือน (รวมปีอธิกสุรทิน) | EA-09, EA-10 |
| D-08 | **soft ref ต้องเก็บ snapshot ชื่อ** — บริษัท/พนักงานที่ถูกปิดใช้หรือลาออก ต้องยังแสดงชื่อในประวัติได้ (LD-4C-02 · ไม่มี FK cascade) | EA-12, EA-13 |
| D-09 | **`resolve()` ต้องบังคับพารามิเตอร์ "วันที่"** — ถ้าไม่ส่งมา ให้ปฏิเสธหรือ default เป็นวันนี้อย่างชัดเจน (ต้องระบุใน FRD) · **ห้าม cache ข้ามวัน** | EA-16 🔺, EA-17 |
| D-10 | **ปิดใช้ค่าที่มีเฉพาะเวอร์ชัน Draft** ควรเป็นการทิ้งร่าง ไม่ใช่ soft archive | EA-07 |
| D-11 | **ลบวันหยุดต้นทางที่มีวันชดเชยอ้างอยู่** ต้องบล็อกหรือเตือนก่อน | EA-14 |
| D-12 | **สิทธิ์ต้องบังคับที่ระดับ API ไม่ใช่ซ่อนปุ่ม** — HR Staff เรียก endpoint สร้าง/แก้ตรง ๆ ต้องถูกปฏิเสธ | EA-15 |

## 14.4 WARNING / ประเด็นที่รอข้อสรุป

| ประเด็น | หารือกับใคร | กำหนดวันที่ | สถานะ | บล็อกอะไร |
|---|---|---|---|---|
| Q-09 BR-13 เป็น DYNAMIC/Rule Management | **Strike + Architect** | ก่อนเริ่ม Phase 3 | ⚠️ รอ | Phase 3 เท่านั้น — Phase 1 เดินต่อได้ (implement เป็นตาราง) |
| Q-10 ตาราง legal minimum (BR-05/BR-06) | **Strike + ฝ่ายกฎหมาย/HR** | ก่อน go-live | ⚠️ รอ | Phase 1 P1-03 — ต้องรู้ค่าจริงและแหล่งอ้างอิงกฎหมายก่อน seed |
| Q-13 re-validate ตอน commit (EA-02) | **Architect** | ก่อนปิด FRD | ⚠️ รอ | D-01 |
| Q-14 การยกเลิกเวอร์ชันซ้อน (EA-05) | **BA + Architect** | ก่อนปิด FRD | ⚠️ รอ | D-04 |
| Q-15 สัญญา `resolve()` ต้องส่งวันที่เสมอ (EA-16) | **Architect** | ก่อนปิด FRD | ⚠️ รอ | D-09 · กระทบสัญญากับ 8 feature |
| OQ-STD-01…06 · OQ-HR-01/03 | **Strike** | ก่อนรอบถัดไป | ⚠️ รอ (เดินต่อด้วย default + `[ASSUMED]`) | ไม่บล็อก Phase 1 |

> **ห้ามเริ่มพัฒนา Phase 3 และ Phase 4 จนกว่า Q-09 / OQ-STD-02 / OQ-STD-04 จะ resolve**

## 14.5 Regression Scope
**N/A — New Feature** (ไม่มี feature เดิมของงานนี้ให้ test ซ้ำ · ดู §11)

## 14.6 Screen Inventory + UI Signals + **Functions Cut ("ไม่รองรับ")** ⭐

> BRD ไม่ตัดสิน layout — spec จริง (pattern/CI/px/iron rules) เป็นของ **FRD (frd-generator-v6 = Design Authority)** · ตารางนี้ **สกัดจาก HTML ที่ผ่าน gate แล้ว** (`1_HTML/ตั้งค่าHR.html` · 7 routes · COVERAGE_R1 🟢 · UX_CHECK 🟢) ตาม `_lane/COVERAGE_MAP.md` — **ไม่แต่งหน้าเพิ่ม ไม่ตัดหน้า**

### 14.6.1 Screen Inventory (สกัดจาก HTML)

| # | ชื่อหน้า/ส่วน | route (จริงใน HTML) | ประเภทหยาบ | ผู้ใช้หลัก | หน้าที่ของหน้า (business) | หมายเหตุ |
|---|---|---|---|---|---|---|
| P-01 | ตั้งค่า HR (เข้าหน้า) | `#/hr-config` | หน้าแรก-landing | HR Admin, HR Staff | เข้าแล้วเด้งไป tab แรก | 1 เมนูซ้าย (#104) |
| P-02 | tab ประเภทการลา | `#/hr-config/leave` | หน้ารายการ | HR Admin, HR Staff | ดู/ค้นหา/สร้างกติกาประเภทลา | FN-08,09,10,29,31,32 |
| P-03 | tab อัตรา OT / กะ | `#/hr-config/ot` | หน้ารายการ | HR Admin, HR Staff | ดู/สร้างอัตรา OT + กะมาตรฐาน | FN-11,12,13,14 |
| P-04 | tab ปฏิทินวันหยุด | `#/hr-config/holiday` | หน้ารายการ | HR Admin, HR Staff | ดู/สร้างชุดปฏิทินรายปี + วันหยุดชดเชย | FN-15,16,17,49 |
| P-05 | tab รอบเวลา / รอบจ่าย | `#/hr-config/period` | หน้ารายการ | HR Admin, HR Staff | ตั้งกติการอบ + สร้างงวดทั้งปี + ปิด/เปิดงวด | FN-18,48,50 |
| P-06 | tab รอบประเมิน | `#/hr-config/appraisal` | หน้ารายการ | HR Admin, HR Staff | ตั้งรอบประเมินรายปี | FN-20,21 |
| P-07 | tab ขอบเขตบริษัท | `#/hr-config/company` | หน้ารายการ | HR Admin, HR Staff | ดูค่าทุกกลุ่มโดยเน้นคอลัมน์ขอบเขต | FN-22,23,30 |
| P-08 | สร้างค่าใหม่ / สร้างเวอร์ชันใหม่ | (drawer บน P-02…P-07) | ฟอร์มสร้าง (หลายขั้น — 3 ขั้น) | HR Admin | กรอกข้อมูลค่า › ค่าที่ใช้ › ตรวจสอบและยืนยัน (วันมีผล + เหตุผล) | FN-01…FN-07 |
| P-09 | ดูค่า (view) | (drawer บน P-02…P-07) | หน้ารายละเอียด | HR Admin, HR Staff | 3 tab: รายละเอียด › ประวัติเวอร์ชัน › ใครใช้ค่านี้ | FN-27,28,33 |
| P-10 | หน้ายืนยัน (ปิดใช้ · ยกเลิกเวอร์ชัน · เปิดใช้กลับ · ปิด/เปิดงวด · เตือนโควตา) | (modal บนทุกหน้า) | หน้ายืนยัน | HR Admin | ยืนยันพร้อมเหตุผล + แสดงผลกระทบ | FN-24,25,26,32,48,91 |

**รวมโดยประมาณ:** **~10 ส่วน** — หน้ารายการ 6 (+1 landing) · ฟอร์มสร้างหลายขั้น 1 · หน้ารายละเอียด 1 · หน้ายืนยัน 1 (ใช้ซ้ำหลายกรณี) · **ไม่มี dashboard · ไม่มีรายงาน · ไม่มีหน้า print**

### 14.6.2 UI Signals ให้ FRD (แค่ signal ไม่ใช่ spec)

| Signal | ค่า | เหตุผล |
|---|---|---|
| เป็น Document/Transaction (approver + พิมพ์เอกสาร + ลายเซ็น) | **ไม่ใช่** | ไม่มี approval · ไม่มีเลขที่เอกสาร · ไม่มีลายเซ็น · ไม่มี PDF → **ไม่ใช่ Pattern Q** |
| ต้องการ print / PDF | **ไม่มีหน้าไหนต้องพิมพ์** | ไม่มี `pdfdoc` · **ไม่มี `PRINT_SPEC.md` ในชุดส่งมอบนี้โดยเจตนา** (ดู §14.6.4) |
| archetype | **master/config (A+B+C)** | ยืนยันแล้วที่ STANDARD_BASELINE §3 · lifecycle เป็นเวอร์ชันของค่า ไม่ใช่เอกสารที่คนถือ |
| โครงเมนู | **1 เมนูซ้าย + 6 tab ในหน้า** | #104 (TASTE_LOG 2026-08-25 Consent run 1) |
| จำนวนขั้นของ wizard | **3 ขั้น** (ไม่ใช่ 5) | Rule #100 (5 ขั้นล็อก) ใช้กับ Pattern Q เอกสารธุรกรรมเท่านั้น · archetype นี้ใช้ Rule #47 stepper กลาง (2–5 ขั้น) — `[ASSUMED]` จาก S2 |
| persona switch | **อยู่ `.demo-strip` เท่านั้น** | #105 — ห้ามบน page header |
| คำอธิบายบนจอ | **ⓘ `.tip` เท่านั้น ห้าม hint banner** | #106 |
| combobox คน | **#102 anatomy** (avatar/icon → ชื่อ → ตำแหน่ง · แผนก) | BR-15 |
| NON-STANDARD flag | **ไม่มี** | ไม่มีคำสั่ง "keep original UI" จากต้นทาง |
| หน้าที่ต้องประกาศขอบเขตบนจอ | **ทุก tab** — 11 ข้อที่ไม่รองรับต้องมี ⓘ | ไม่ตัดเงียบ |

### 14.6.3 **Functions Cut — "ไม่รองรับ" (จาก `FUNCTION_CHECKLIST.md` หมวด 9 + ท้ายไฟล์)**

> ตัดสินแล้ว — **อย่าเผลอทำ** · ทุกข้อต้อง **เห็นบนหน้าจอ** ผ่าน ⓘ `.tip` และปรากฏใน BRD/FRD ไม่ใช่หายเงียบ

| # | สิ่งที่ไม่รองรับ | FN | Scenario | เหตุผล / เจ้าของจริง | OQ |
|---|---|---|---|---|---|
| NS-01 | **approval workflow ตอนแก้ค่านโยบาย** — ไม่มีปุ่ม "ส่งอนุมัติ/อนุมัติ" ที่ใดในหน้านี้ | FN-40 | S-23 | scope note ระบุ "ไม่มี approval" · คุมด้วย `effective_date` + audit append-only แทน (D365/SAP มี → ยกเป็น OQ ไม่ตัดเงียบ) | **OQ-STD-01** |
| NS-02 | **คำนวณย้อนหลัง (retro recalculation)** เมื่อแก้นโยบายคร่อมงวดที่ปิดแล้ว | FN-41 | S-24 | บล็อกการตั้งวันย้อนหลังแทน (BR-04) · ถ้าเคาะว่าต้องมี = engine candidate `hr-policy-retro-engine` | **OQ-STD-04** |
| NS-03 | **สูตรคำนวณเงินเดือน / mapping earning code เต็มรูป** | FN-42 | S-25 | อยู่ Salary Structure (W1/B) และ Payroll (W4) · ที่นี่เก็บแค่ `payroll_code` เป็น soft reference | **OQ-STD-03** |
| NS-04 | **ยอดวันลาคงเหลือรายคน (leave balance)** | FN-43 | S-26 | Leave (W2) เป็นเจ้าของ balance · ที่นี่เก็บ policy เท่านั้น | **OQ-HR-02** (ตอบแล้ว) |
| NS-05 | **UI สลับบริษัท (company switcher)** บนหัวจอ | FN-44 | S-27 | มี field company แล้ว แต่ยังไม่ทำหน้าสลับรอบนี้ | **OQ-HR-05** (ตอบแล้ว) |
| NS-06 | **ดึงวันหยุดราชการอัตโนมัติตามประเทศ** | FN-45 | S-28 | NICE ใน STANDARD_BASELINE C-23 · รอบนี้กรอกมือ/นำเข้าภายหลัง | — |
| NS-07 | **แจ้งเตือนพนักงานเมื่อนโยบาย/ปฏิทินเปลี่ยน** | FN-46 | S-29 | feature ปลายทางประกาศ NTF เอง — กันประกาศซ้ำ | **OQ-STD-05** |
| NS-08 | **import/export ค่า config เป็นชุด (mass upload)** | FN-47 | S-30 | SHOULD ใน C-22 · pattern import เป็นของ Attendance (W1/C) รอบนี้ไม่ทำ `[AI-DRAFT]` | — |
| NS-09 | **eligibility ตามประเภทจ้าง/ระดับ/แผนก** | (FN-30 hook) | S-22 | รอบนี้ขอบเขตแค่ระดับบริษัท · เผื่อ field `applies_to` ไว้เป็น hook | **OQ-STD-02** |
| NS-10 | **หน้าตั้งค่าของ feature HR อื่น** | — | — | ทุก feature อ้างมาที่นี่ ห้ามสร้างหน้า config ของตัวเอง | **#107** |
| NS-11 | **ลบค่าถาวร (hard delete)** | FN-24 (negative) | S-18 | มติ audit append-only — มีแต่ปิดใช้ (soft archive) | — |
| NS-12 | **ระยะทดลองงาน (probation) / ระยะบอกกล่าวล่วงหน้า** | FN-51 | S-33 | อยู่นอก 6 กลุ่มค่าที่ scope note ระบุ · ผู้ใช้หลักคือ On/Offboard และ Employee Movement (W3) — 3/3 ค่ายมี จึงยกเป็น OQ ไม่ตัดเงียบ | **OQ-STD-06** |
| NS-13 | **ความถี่การคำนวณจ่าย รายสัปดาห์/รายปักษ์ (calculation frequency)** | FN-52 | S-34 | เป็นของ Payroll (W4) · ที่นี่หยุดที่ "รอบจ่าย" | **OQ-HR-01** |
| NS-14 | **Time Profile** (มัดชุดประเภทลา + กะ + ปฏิทิน แล้ว assign ให้กลุ่มพนักงาน) | FN-53 | S-35 | รอบนี้ขอบเขตแค่ระดับบริษัท | **OQ-STD-02** |

**รวม 14 รายการ "ไม่รองรับ" — ตรงกับ `FUNCTION_CHECKLIST.md` ครบทุกข้อ · ครอบ FN-40…FN-47, FN-51…FN-53 (11 FN) และ S-23…S-30, S-33…S-35 (11 scenario)**

### 14.6.4 หมายเหตุ PRINT_SPEC

**ชุดส่งมอบนี้ไม่มี `PRINT_SPEC.md` โดยเจตนา** — feature นี้ไม่มีท่อ `pdfdoc` (`_lane/DECL.json` → `pdfdoc.need=false` · `5_DECLARATIONS/NOT_NEEDED.md`) เพราะไม่มีเอกสารที่คนถือ/ยื่น/พิมพ์ส่ง และไม่มีช่องลายเซ็น · **การไม่มีไฟล์นี้ไม่ใช่ของขาด** — ระบุไว้ที่นี่และซ้ำใน `3_FRD/00_OVERVIEW` เพื่อไม่ให้ผู้รับงานเข้าใจผิด

---

# Section 15: Open Questions

> เลนเดินต่อด้วย **default + `[ASSUMED]`** ตาม `gate-policy.md` default table — **ไม่หยุดถาม** · ทุกข้อขึ้น REVIEW_SHEET ให้ Strike/BA เคาะ

| # | คำถาม | สถานะ | ค่าที่เลนใช้ (default) | เจ้าภาพ | บล็อกอะไร |
|---|---|:---:|---|---|---|
| **Q-01** (OQ-STD-01) | ต้องมี approval ตอนแก้ค่านโยบายไหม (D365/SAP บังคับ workflow ก่อน config มีผล) | ⚠️ รอ | **ไม่มี approval** — `effective_date` + audit append-only + Draft→Scheduled เป็นตัวคุม `[ASSUMED]` | Strike | ไม่บล็อก · ถ้าเคาะกลับ → เรียก DOA Engine ที่ T-02 จุดเดียว (ห้ามสร้างใหม่) |
| **Q-02** (OQ-STD-02) | eligibility นอกเหนือ company (ประเภทจ้าง/ระดับ/แผนก) | ⚠️ รอ | รอบนี้ = ทั้งบริษัท + field `applies_to` เป็น hook `[ASSUMED]` | Strike / BA | บล็อก Phase 3 (`hr-eligibility-rule-engine`) |
| **Q-03** (OQ-STD-03) | ผูก OT rate → earning code / payroll element | ⚠️ รอ | เก็บ `payroll_code` เป็น soft ref เท่านั้น `[ASSUMED]` | BA (Salary Structure) | ไม่บล็อก · กระทบ BR-18 mode |
| **Q-04** (OQ-STD-04) | ต้องคำนวณย้อนหลังเมื่อแก้นโยบายคร่อมงวดเก่าไหม | ⚠️ รอ | **ไม่ทำ retro** — บล็อกการตั้งวันย้อนหลัง (BR-04) `[ASSUMED]` | Strike | บล็อก Phase 4 (`hr-policy-retro-engine`) |
| **Q-05** (OQ-STD-05) | แจ้งเตือนพนักงานเมื่อนโยบาย/ปฏิทินเปลี่ยน — แจ้งจากที่นี่หรือปลายทาง | ⚠️ รอ | **ปลายทางแจ้ง** — ที่นี่ไม่ประกาศท่อ NTF `[ASSUMED]` | Chin (ENG-NOTIFY) | ไม่บล็อก · ถ้าเคาะกลับ → `ntf-declaration` event `hrconfig.published` |
| **Q-06** (OQ-STD-06) | ระยะทดลองงาน (probation) + ระยะบอกกล่าวล่วงหน้า ควรอยู่ที่ HR Configuration ไหม (3/3 ค่ายเก็บเป็น param กลาง) | ⚠️ รอ | **ไม่ทำรอบนี้** — นอก 6 กลุ่มค่าใน scope note · กัน scope drift `[ASSUMED]` | Strike | ไม่บล็อก · กระทบ On/Offboard + Employee Movement (W3) |
| **Q-07** (OQ-HR-01) | Payroll สร้างเองเต็มไหม | ⚠️ รอ | สร้างเอง — กระทบที่นี่แค่ "รอบจ่าย" `[ASSUMED]` | Strike | ไม่บล็อก |
| **Q-08** (OQ-HR-03) | แหล่งข้อมูลเวลาเข้างาน | ⚠️ รอ | import ไฟล์ + กรอกมือ — กระทบที่นี่แค่ "วันตัดเวลา" `[ASSUMED]` | Strike | ไม่บล็อก |
| **Q-09** ⭐ **ใหม่ (C23 escalation)** | BR-13 ลำดับ resolve ค่า ถูกจัดเป็น **DYNAMIC + Rule Management โดย AI** 🤖 — ยืนยันหรือลดเป็น CONFIGURABLE? กลุ่มบริษัทจะขยายเกิน 2 ชั้นไหม | ⚠️ รอ | implement เป็น **ตารางลำดับ** ใน Phase 1 (ยกเป็น Rule Management ได้โดยไม่ refactor) | Strike + Architect | บล็อก Phase 3 |
| **Q-10** ⭐ **ใหม่** | ค่าขั้นต่ำตามกฎหมาย (OT 1.5/1.0/3.0 · ลาพักร้อน 6 วัน) — แหล่งอ้างอิงทางกฎหมายที่เป็นทางการคืออะไร ใครเป็นเจ้าของการอัปเดต | ⚠️ รอ | seed ตามที่ระบุใน PREBRIEF + เก็บเป็นตารางที่มี `effective_date` เอง (ห้าม hardcode) | Strike + ฝ่ายกฎหมาย/HR | **บล็อก P1-03 ก่อน go-live** |
| **Q-11** ⭐ **ใหม่** (`[AI-DRAFT]` G-02) | ปฏิทินวันหยุดแยกตามสถานที่/สาขา (`location`) — ยืนยันว่าต้องมีรอบนี้ไหม | ⚠️ รอ | **merge แล้ว** (FN-49) ตาม STANDARD_GAP G-02 = SHOULD · tag `[AI-DRAFT]` | BA | ไม่บล็อก |
| **Q-12** ⭐ **ใหม่** (`[AI-DRAFT]` G-03) | ความถี่รอบบันทึกเวลาแยกจากรอบจ่าย — ยืนยันว่าต้องมีรอบนี้ไหม | ⚠️ รอ | **merge แล้ว** (FN-50) · ค่าเริ่ม = ใช้รอบเดียวกัน · tag `[AI-DRAFT]` | BA | ไม่บล็อก |
| **Q-13** ⭐ **ใหม่** (EA-02 🔺) | ปิดงวดขณะที่มีคนกำลังบันทึกเวอร์ชันที่มีผลในงวดนั้น — re-validate ตอน commit หรือ lock งวดตอนเปิดฟอร์ม | ⚠️ รอ | **re-validate ตอน commit** (D-01) | Architect | บล็อกการปิด FRD |
| **Q-14** ⭐ **ใหม่** (EA-05 🔺) | ยกเลิกเวอร์ชัน Scheduled ที่มีเวอร์ชันอื่นซ้อนอยู่ข้างหลัง — คำนวณ `effective_to` ใหม่อย่างไร | ⚠️ รอ | คำนวณ `effective_to` ของเวอร์ชันก่อนหน้าใหม่จากเวอร์ชันถัดไปที่เหลืออยู่ (D-04) | BA + Architect | บล็อกการปิด FRD |
| **Q-15** ⭐ **ใหม่** (EA-16 🔺) | สัญญา `resolve()` — ถ้าปลายทางไม่ส่ง "วันที่" มา ให้ปฏิเสธหรือ default เป็นวันนี้ | ⚠️ รอ | **บังคับส่งวันที่ · ไม่ส่ง = ปฏิเสธ** (D-09) · ห้าม cache ข้ามวัน | Architect | บล็อกการปิด FRD · กระทบสัญญากับ 8 feature |
| **Q-16** ⭐ **ใหม่** (C21) | ยืนยัน positioning ของ feature นี้กับ **VS Bible** โดยตรง (เลนอ้างผ่าน CONTEXT_PACK + current-state เท่านั้น) | ⚠️ รอ | ใช้ data flow ใน `CONTEXT_PACK/HR.md` เป็นหลักฐานชั่วคราว | Architect | ไม่บล็อก |
| **Q-17** ⭐ **ใหม่** (C16) | ขอ `System_Module_Registry` เพื่อทำ §12.3 ให้สมบูรณ์ | ⚠️ รอ | ใช้ CONTEXT_PACK + current-state §2 baseline แทน (placeholder) | PM / Architect | ไม่บล็อก |
| **Q-18** (ตอบแล้ว · OQ-HR-02) | ยอดวันลาคงเหลือเก็บที่ไหน | ✅ ตอบแล้ว | Leave (W2) เก็บ balance · ที่นี่เก็บ policy | Strike | — |
| **Q-19** (ตอบแล้ว · OQ-HR-05) | multi-company ทำถึงไหน | ✅ ตอบแล้ว | มี field company · **ยังไม่ทำ UI สลับบริษัท** | Strike | — |
| **Q-20** (ปิดแล้วที่ S1.5) | นิยาม "งวดที่ปิดแล้ว" ใน BR-04 | ✅ ปิดแล้ว | = งวดที่สถานะ "ปิด" ในตารางงวด (S-31 · BR-21) — HR Admin เป็นคนปิด `[STD]` | BA | — |
| **Q-21** (OQ-HR-04) | ESS | ✅ N/A รอบนี้ | ESS อ่านอย่างเดียว เรียกหน้าของ feature ต้นทาง | Strike | — |

**`[ASSUMED]` รวม 8 ข้อ:** A-01…A-08 (§3.3) = OQ-STD-01, 02, 03, 04, 05, 06 + OQ-HR-01, 03
**`[ASSUMED]` ที่สืบทอดจาก S2 (COVERAGE_MAP):** `applies_to` hook ใช้ `.tip` แทน comment TODO · chip counts รวมกับ stat card · tab ขอบเขตบริษัทสลับคอลัมน์ · wizard 3 ขั้น (ไม่ใช่ 5)
**DIVERGENCE: — ไม่มี** (ไม่มีข้อใดขัดกับ LOCK/มติใน LANE_BRIEF)

---

# Section 16: Security & Compliance ⭐ Philosophy

## 16.1 Security Preset

**Preset ที่เลือก: P6 — HR/PII Sensitive (15 controls)**
**เหตุผล:** Module = HR (ตาม Step 6.1 inference: HR/Payroll/Employee → P6)
**ข้อสังเกตที่ต้องบันทึก:** ข้อมูลของ feature นี้เองเป็น **INTERNAL ไม่ใช่ RESTRICTED** — ไม่มีข้อมูลรายบุคคลอยู่ในค่า config (มีแต่ **การอ้างถึง** พนักงานผ่าน soft ref: ผู้รับผิดชอบ · ผู้แก้ไข · ผู้ปิดงวด) · จึงคง P6 ไว้เป็น baseline ของโมดูล แต่ **control หมวด privacy (S07-xx) ถูก mark เป็น ○ Optional พร้อมเหตุผล** ไม่ตัดออกเงียบ ๆ — การบังคับจริงอยู่ที่ Policy Center ระดับแพลตฟอร์ม

## 16.2 Applicable Standards (14 มาตรฐาน)

| # | Standard | Applicable? | เหตุผล |
|---|---|:---:|---|
| 1 | COSO — Internal Control & SoD | ✅ | มีการเปลี่ยนแปลงที่กระทบสิทธิ์พนักงาน ต้องมีร่องรอย + แยกหน้าที่ |
| 2 | ISO/IEC 27001 — Information Security | ✅ | ควบคุมการเข้าถึง · session · classification |
| 3 | NIST CSF 2.0 — Cyber Resilience | ✅ | detect/respond ต่อการเปลี่ยนนโยบายที่ผิดปกติ |
| 4 | COBIT 2019 — IT Governance | ✅ | change management ของ config ระดับองค์กร |
| 5 | CIS Controls v8 — System Hardening | ❌ | ไม่ใช่ระดับ feature — เป็นงานแพลตฟอร์ม |
| 6 | NIST SP 800-53 — Advanced Access & Audit | ✅ | ABAC + audit content มาตรฐาน |
| 7 | ISO/IEC 27701 — Privacy & PDPA/GDPR | ✅ | เพราะค่าที่ตั้งกระทบสิทธิ์ของบุคคล แม้ตัว record ไม่ใช่ PII |
| 8 | NIST Privacy Framework | ○ บางส่วน | ไม่มี PII ในค่า config — ใช้ผ่าน Policy Center |
| 9 | IEC 62443 — IT/OT Network Security | ❌ | ไม่มี OT/IoT |
| 10 | NIST SP 800-82 — OT Operations | ❌ | ไม่มี OT |
| 11 | SOC 2 (Type I & II) — Continuous Evidence | ✅ | ประวัติเวอร์ชัน = evidence ต่อเนื่อง |
| 12 | ISO 22301 — Business Continuity | ○ บางส่วน | ถ้า `resolve()` ล่ม ทุก feature HR คำนวณสิทธิ์ไม่ได้ → ต้องมีแผน (ดู R-05) |
| 13 | NIST AI RMF — AI Safety & Limits | ❌ | ไม่มีการตัดสินใจด้วย AI ใน feature นี้ |
| 14 | OWASP API Security — Gateway Protection | ✅ | `resolve()` เป็น API ที่ 8 feature เรียก |

## 16.3 Control Checklist (P6 · 15 controls)

| Control ID | Standard | Control | Required | Implementation Notes (ในบริบท feature นี้) |
|---|---|---|:---:|---|
| S01-04 | COSO | SoD Conflict Matrix | ✓ Must | สิทธิ์ "แก้ค่านโยบาย" ต้องไม่ผูกกับ role ที่อนุมัติใบลา/ใบ OT ที่ปลายทาง — บังคับที่ Roles & Permissions (§4) |
| S01-07 | COSO | Immutable Master Data Log | ✓ Must | **แกนของ feature** — `hr_config_version` เก็บ before/after ทุกเวอร์ชัน · **ห้ามลบ** (BR-07, BR-14) |
| S02-02 | ISO 27001 | MFA Enforcer | ○ Optional | ผูกกับนโยบาย login ระดับแพลตฟอร์ม — แนะนำบังคับสำหรับ role HR Admin |
| S02-04 | ISO 27001 | Data Masking / Obfuscation | ○ Optional | ค่า config เป็น INTERNAL ไม่ต้อง mask · แต่ชื่อพนักงานใน audit ต้องตามนโยบาย masking ของ Policy Center |
| S02-05 | ISO 27001 | Data Classification Tags | ✓ Must | ติด tag **INTERNAL** ให้ทุก entity ของ feature นี้ (§7 Data behaviour) |
| S02-06 | ISO 27001 | Export Limits | ○ Optional | รอบนี้ไม่มี export (OUT-08) — เปิดใช้เมื่อทำ import/export |
| S06-01 | NIST 800-53 | ABAC | ✓ Must | สิทธิ์ตาม role + company scope — HR Admin ของบริษัทลูกเห็นเฉพาะค่าของบริษัทตน (บังคับที่ Policy Center) |
| S06-03 | NIST 800-53 | Standardized Audit Content | ✓ Must | ทุก log ต้องมี Who / What / When / Where / Result · **เรียก Policy Center Audit Trail** ไม่เขียนเอง (BR-14) |
| S06-05 | NIST 800-53 | Payload Encryption | ○ Optional | ไม่มีข้อมูลอ่อนไหวใน payload — ใช้ TLS ระดับแพลตฟอร์มพอ |
| S07-01 | ISO 27701 | Granular Consent | ○ Optional | **ไม่ใช้** — ไม่มีการเก็บ/ประมวลผล PII ที่ต้องขอความยินยอมใน feature นี้ (ระบุเหตุผลไว้ ไม่ตัดเงียบ) |
| S07-02 | ISO 27701 | Consent Withdrawal | ○ Optional | เช่นเดียวกับ S07-01 |
| S07-03 | ISO 27701 | Automated Data Portability | ○ Optional | ไม่มี PII ให้ port · export ของ config = OUT-08 |
| S07-04 | ISO 27701 | Anonymization (RTBF) | ○ Optional | **ห้ามลบข้อมูลประวัติเวอร์ชัน** (BR-07/BR-14 · หลักฐานทางกฎหมายแรงงาน) — ถ้าพนักงานใช้สิทธิ์ RTBF ให้ anonymize **ชื่อผู้แก้ไข** ที่ Policy Center ไม่ใช่ลบเวอร์ชัน |
| S07-05 | ISO 27701 | Dynamic Data Purging | ○ Optional | **ขัดกับ audit append-only** — ห้าม purge ประวัติเวอร์ชัน · ระบุไว้เพื่อไม่ให้ถูกเปิดใช้โดยพลาด |
| S07-06 | ISO 27701 | PII Tagging & Masking | ✓ Must | field ที่อ้างถึงคน (`owner_employee_id`, `created_by`, `modified_by`, `closed_by`) ต้องติด tag PII เพื่อให้ masking ของ Policy Center ทำงาน |
| **เพิ่มนอก preset** S14-02 | OWASP API | Payload Schema Validation | ✓ Must | `resolve(date, company)` ต้อง validate schema — โดยเฉพาะ **บังคับพารามิเตอร์ "วันที่"** (Q-15 · D-09) |

## 16.4 Risk Statement

| Risk ID | Risk | ผลกระทบ | Mitigated by Control / Rule |
|---|---|---|---|
| **R-01** | HR Admin เปลี่ยนค่านโยบายโดยไม่มีใครตรวจ (ไม่มี approval ในรอบนี้) แล้วสิทธิ์พนักงานเปลี่ยนทันที | สูง — กระทบเงิน/สิทธิ์ของพนักงานทั้งบริษัท | S01-07 (immutable log) + BR-01/BR-02 (`effective_date` ทำให้ไม่มีผลทันที) + BR-14 (audit) + event CSQ SecC + **OQ-STD-01 ยกไว้ให้เคาะ** |
| **R-02** | ประวัติเวอร์ชันถูกลบ/แก้ย้อนหลัง → ตอบข้อพิพาทแรงงานไม่ได้ | สูงมาก — ความเสี่ยงทางกฎหมาย | S01-07 + BR-07 (ไม่มี hard delete) + S07-05 ห้าม purge + S06-03 audit content |
| **R-03** | ตั้งค่าที่ต่ำกว่าขั้นต่ำตามกฎหมาย (OT/โควตาลา) | สูง — บริษัทผิดกฎหมายแรงงาน | BR-05 (บล็อก) + BR-06 (เตือน) + ตาราง legal minimum ที่มี `effective_date` (P1-03) + **Q-10** |
| **R-04** | แก้นโยบายย้อนหลังเข้างวดที่จ่ายเงินไปแล้ว | สูง — ยอดจ่ายที่ปิดแล้วเปลี่ยน | BR-04 + BR-21 (นิยามงวดปิด) + D-01 re-validate ตอน commit |
| **R-05** | `resolve()` ล่ม/ตอบผิด → ทุก feature HR คำนวณสิทธิ์ผิดพร้อมกัน (single point of dependency) | สูงมาก — กระทบ 8 feature พร้อมกัน | S14-02 schema validation + ISO 22301 (ต้องมีแผน fallback/cache นโยบาย + monitoring §17.2/§18.5) + **ห้าม cache ข้ามวัน** (D-09) |
| **R-06** | HR Staff หรือ role อื่นเรียก API สร้าง/แก้ค่าตรง ๆ โดยข้าม UI | กลาง | S06-01 ABAC + D-12 (บังคับสิทธิ์ที่ระดับ API ไม่ใช่ซ่อนปุ่ม) |
| **R-07** | ปิดใช้ค่าที่ feature ปลายทางยังอ้างอยู่ โดยไม่รู้ผลกระทบ | กลาง–สูง | BR-08 + FN-26 (where-used บังคับก่อนยืนยัน) + `hr_config_usage` |

---

# Section 17: Health Check ⭐ Philosophy

## 17.1 SLA

| # | Step | SLA | Owner | Action when breached |
|---|---|---|---|---|
| SLA-01 | เวอร์ชัน Scheduled → Active เมื่อถึงวันมีผล | ภายใน **1 ชั่วโมง** หลังเที่ยงคืนของวันมีผล | ทีมระบบ (scheduler) | alert ทีมระบบ + รัน catch-up ทันที (EA-04 · D-03) |
| SLA-02 | `resolve(date, company)` ตอบกลับ | **P95 ≤ 300 ms** | ทีมระบบ | alert + ตรวจ index/cache (กระทบ 8 feature พร้อมกัน — R-05) |
| SLA-03 | ปิดงวดหลังวันจ่ายผ่านไป | ภายใน **5 วันทำการ** | HR Admin | เตือน HR Admin — งวดที่ยังไม่ปิดทำให้ BR-04 บังคับไม่ได้ |
| SLA-04 | ตั้งค่าที่ต้องมีผลต้นปี (ปฏิทินวันหยุด/รอบประเมิน) | ตั้งล่วงหน้า **≥ 30 วัน** ก่อนวันมีผล | HR Admin | เตือนเมื่อเหลือ < 30 วันและยังไม่มีเวอร์ชัน Scheduled ของปีถัดไป |
| SLA-05 | เขียน audit หลัง transition | **ทันที (synchronous)** — ถ้าเขียน audit ไม่สำเร็จ ต้อง rollback transition | ทีมระบบ | alert ทันที · ห้ามปล่อยให้ transition สำเร็จโดยไม่มี log (R-02) |

## 17.2 Control Points

| Control ID (จาก §16) | Where | When | Result |
|---|---|---|---|
| S01-07 | ทุก transition ของ `hr_config_version` | ทุกครั้ง | เขียน before/after ลง Policy Center Audit Trail · rollback ถ้าเขียนไม่ได้ (SLA-05) |
| S06-03 | ทุก audit entry | ทุกครั้ง | ตรวจว่ามีครบ Who/What/When/Where/Result |
| S06-01 | ทุก endpoint สร้าง/แก้/ปิดใช้/ปิดงวด | ทุก request | บล็อกถ้า role ไม่ผ่าน ABAC (ไม่ใช่แค่ซ่อนปุ่มบน UI) |
| S02-05 | ทุก entity ของ feature | ตอน deploy schema | ตรวจว่าติด tag INTERNAL ครบ |
| S07-06 | field ที่อ้างถึงคน 4 ช่อง | ตอน deploy + ตอน export audit | ตรวจว่าติด tag PII เพื่อให้ masking ทำงาน |
| S14-02 | `resolve(date, company)` | ทุก request | ปฏิเสธ request ที่ไม่มีพารามิเตอร์ "วันที่" (Q-15) |
| S01-04 | ตอนกำหนด role | ตอน onboarding role | บล็อกถ้า role เดียวกันมีทั้งสิทธิ์แก้ค่านโยบายและอนุมัติเอกสารปลายทาง |

## 17.3 KPI

| KPI ID | KPI | Category | Target | Measure | คู่กับตัวชี้วัด §2.3 |
|---|---|---|---|---|---|
| **K-01** | จำนวน feature HR ที่มีหน้า config ของตัวเอง (ละเมิด #107) | Compliance | **0** | ตรวจ FEATURE_REGISTRY + code review ตอนปิดแต่ละ feature | **M-01** |
| **K-02** | สัดส่วนเวอร์ชันที่มี `effective_date` ครบ | Quality | **100%** | `count(effective_date not null) / count(*)` ของ version ที่ไม่ใช่ Draft | **M-02** |
| **K-03** | เวลาเฉลี่ยตอบคำถาม "ณ วันที่ X ใช้กติกาอะไร" | Speed | **≤ 2 นาที** | จับเวลาการใช้ตัวกรอง as-of (UAT + spot check) | **M-03** |
| **K-04** | จำนวนการแก้ทับเวอร์ชัน Active | Quality | **0 / เดือน** | นับ audit event `update` ที่ target เป็น Active | **M-04** |
| **K-05** | สัดส่วนการปิดใช้ที่ผ่านการดู where-used | Compliance | **100%** | audit event `deactivate` ที่มี `where_used_shown=true` | **M-05** |
| **K-06** | จำนวนการตั้งวันมีผลย้อนเข้างวดปิดที่สำเร็จ | Compliance | **0** | audit event ที่ `effective_date < period.close_date` และ result=success | **M-06** |
| **K-07** | จำนวนคำขอ `resolve()` ต่อวัน | Volume | baseline ตอน launch → ติดตามการเติบโต | นับ request/day แยกตาม feature ปลายทาง | (operational) |
| **K-08** | อัตราการบล็อกจาก validation ต่อการบันทึกทั้งหมด | Quality | **≤ 15%** | `blocked_submits / total_submits` (สูงกว่านี้แปลว่า UX/ข้อความยังไม่ชัด) | (operational) |
| **K-09** | จำนวนงวดที่เลยวันจ่ายเกิน 5 วันทำการแต่ยังไม่ปิด | Compliance | **0** | นับ `hr_pay_period` ที่ `pay_date + 5 วันทำการ < today` และ `status=open` | (operational · คู่ SLA-03) |

## 17.4 Threshold

| Metric | Min | Max | Action when breached |
|---|---|---|---|
| K-02 สัดส่วน `effective_date` ครบ | **100%** | — | Alert ทีมระบบทันที — แปลว่ามีทางลัดที่ข้าม BR-01 |
| K-04 การแก้ทับ Active | — | **0** | Alert + ตรวจ audit ทันที (ละเมิด BR-02 = ช่องโหว่ทางกฎหมาย) |
| K-06 ตั้งวันย้อนเข้างวดปิดสำเร็จ | — | **0** | Alert + ตรวจ BR-04/BR-21 |
| K-05 where-used ก่อนปิดใช้ | **100%** | — | Alert BA |
| SLA-02 `resolve()` P95 | — | **300 ms** | Alert ทีมระบบ · ที่ **500 ms** = ยกระดับเป็น incident (กระทบ 8 feature) |
| K-08 อัตราการบล็อก | — | **15%** | ทบทวนข้อความ validation กับ BA |
| K-09 งวดค้างไม่ปิด | — | **0 งวด** | เตือน HR Admin · ค้าง > 2 งวด = แจ้งหัวหน้า HR |
| จำนวนเวอร์ชัน Scheduled ที่ค้างเกิน 180 วัน | — | **5 รายการ** | เตือน HR Admin ให้ทบทวน (อาจตั้งไว้แล้วลืม) |

## 17.5 Throughput

| ด้าน | ค่า | ที่มา |
|---|---|---|
| **Capacity (การตั้งค่า)** | ~**500 config item** · ~**3,000 version** ต่อองค์กร (6 กลุ่มค่า × หลายบริษัทลูก × ประวัติหลายปี) | ประมาณจาก mock spec §8 (38 ค่าที่ใช้อยู่) × 10 ปี × บริษัทลูก |
| **Baseline (การตั้งค่า)** | ~**20–50 การเปลี่ยนแปลงต่อปี** (นโยบายเปลี่ยนไม่บ่อย — ส่วนใหญ่กระจุกตอนต้นปีและตอนกฎหมายเปลี่ยน) | ธรรมชาติของงาน HR policy |
| **Capacity (การอ่าน)** | `resolve()` เป็น **hot path** — ทุกใบลา/ใบ OT/การประมวลผลเวลา เรียกอย่างน้อย 1 ครั้ง → ประมาณ **50,000–200,000 request/วัน** ที่พนักงาน 1,000 คน | 8 feature × ปริมาณธุรกรรมรายวัน |
| **Stress Point** | `resolve()` > **500 request/วินาที** หรือ P95 > 300 ms → ต้องมี read replica หรือ cache แบบ **invalidate ตอนเวอร์ชันมีผล** (ห้าม cache ข้ามวันแบบตายตัว · D-09) | R-05 |
| **จุดกระจุกตัวที่ต้องเฝ้า** | **ต้นปีปฏิทิน** (ปฏิทินวันหยุด + รอบประเมินปีใหม่มีผลพร้อมกัน) และ **วันตัดเวลา/วันจ่าย** ของทุกเดือน | §12.1 |

---

# Section 18: Monitoring ⭐ Philosophy

## 18.1 Reports Overview

| Report | Type | Frequency | ผู้ใช้ |
|---|---|---|---|
| HR Config Performance | Performance | รายวัน | ทีมระบบ |
| HR Config Closing (สรุปการเปลี่ยนนโยบายรายเดือน) | Closing | รายเดือน | หัวหน้า HR · ผู้ตรวจสอบ |
| HR Config Anomaly | Anomaly | real-time | ทีมระบบ · ผู้ตรวจสอบ |
| HR Config Transaction Log (ประวัติเวอร์ชันเต็ม) | Transaction | on-demand | ผู้ตรวจสอบ · ฝ่ายกฎหมาย |

## 18.2 Dashboard Widgets

| Widget | Source KPI | Threshold (§17.4) |
|---|---|---|
| ค่าที่ใช้อยู่ / รอมีผล / ปิดใช้ (นับตามกลุ่มค่า) | — (สถานะปัจจุบัน) | เวอร์ชัน Scheduled ค้าง > 180 วัน เกิน 5 รายการ → เหลือง |
| สัดส่วน `effective_date` ครบ | K-02 | < 100% → แดง |
| การแก้ทับเวอร์ชัน Active (เดือนนี้) | K-04 | > 0 → แดง |
| ตั้งวันย้อนเข้างวดปิดที่สำเร็จ | K-06 | > 0 → แดง |
| where-used ก่อนปิดใช้ | K-05 | < 100% → แดง |
| `resolve()` P95 latency | SLA-02 / K-07 | > 300 ms → เหลือง · > 500 ms → แดง |
| อัตราการบล็อกจาก validation | K-08 | > 15% → เหลือง |
| งวดค้างไม่ปิด | K-09 | > 0 → เหลือง · > 2 → แดง |
| feature HR ที่ยังไม่เชื่อม (where-used ⏳) | K-01 | — (ติดตามความคืบหน้า Module Linkage) |

## 18.3 Performance Report (รายวัน)
- จำนวน `resolve()` ต่อวัน แยกตาม feature ปลายทางและกลุ่มค่า
- latency P50/P95/P99 ของ `resolve()`
- ผลการทำงานของ scheduler (Scheduled→Active สำเร็จกี่รายการ · ขาดกี่รายการ · catch-up กี่รายการ)
- จำนวนการบันทึกที่สำเร็จ vs ถูกบล็อก แยกตาม VR

## 18.4 Closing Report (รายเดือน)
- สรุปการเปลี่ยนนโยบายทั้งหมดของเดือน: กลุ่มค่า · ค่าอะไร · จากอะไรเป็นอะไร · มีผลเมื่อไร · ใครเปลี่ยน · เหตุผล
- รายการค่าที่ปิดใช้ พร้อม where-used ณ เวลาที่ปิด
- สถานะงวดของเดือน (เปิด/ปิด · ใครปิด · เปิดกลับกี่ครั้งและเพราะอะไร)
- เวอร์ชันที่จะมีผลในเดือนถัดไป (early warning ให้ feature ปลายทาง)

## 18.5 Anomaly Report (real-time)
- **แก้ทับเวอร์ชัน Active สำเร็จ** (ต้องเป็น 0 — ถ้าเกิดคือช่องโหว่ · R-02)
- **ตั้ง `effective_date` ย้อนเข้างวดที่ปิดแล้วสำเร็จ** (ต้องเป็น 0 · R-04)
- **transition ที่ไม่มี audit entry คู่** (ต้องเป็น 0 · SLA-05 · R-02)
- **ปิดใช้โดยไม่มีการแสดง where-used** (ต้องเป็น 0 · R-07)
- เปิดงวดที่ปิดแล้วกลับ (ทุกครั้ง — ต้องมีเหตุผลและถูกตรวจ)
- ตั้งค่าที่ถูกเตือนว่าต่ำกว่าขั้นต่ำกฎหมายแล้วผู้ใช้ยืนยันต่อ (BR-06 · R-03)
- เวอร์ชันหลายเวอร์ชันของค่าเดียวกันถูกสร้างภายในเวลาสั้นผิดปกติ (< 5 นาที)
- `resolve()` ที่ถูกเรียกโดยไม่ส่งพารามิเตอร์ "วันที่" (ต้องเป็น 0 · Q-15)

## 18.6 Transaction Report (on-demand)
- ประวัติเวอร์ชันเต็มของค่าใดค่าหนึ่ง: ทุกเวอร์ชัน · ช่วงที่มีผล · ค่าเก่า→ค่าใหม่ · ผู้แก้ไข · เวลา · เหตุผล
- **"ค่าที่มีผล ณ วันที่ X"** ของทั้งบริษัท (snapshot ย้อนหลัง) — ใช้เป็นหลักฐานตอบข้อพิพาทแรงงาน
- ร่องรอยการเปลี่ยนสถานะงวดทั้งหมด
- รายการ event SecC ที่ถูกส่งให้ ENG-CSQ พร้อมผลลัพธ์

---

# Appendix

## A. Screen List
ดู **§14.6.1 Screen Inventory** (สกัดจาก HTML จริง 7 routes + drawer/modal)

## B. Glossary

| คำ | ความหมาย |
|---|---|
| **HR-1** | มติที่กำหนดว่า legal/policy parameter ทุกตัวต้องมี `effective_date` และห้าม hardcode |
| **#107** | มติที่ห้าม feature อื่นสร้างหน้า config ของตัวเอง — ต้องอ้างมาที่ HR Configuration |
| **LD-4C-02** | มติ soft reference — master เป็นตัวช่วยเลือก · nullable · ไม่มี FK cascade · ห้าม CRUD ของ feature อื่น |
| **config_item / config_version** | โครง 2 ชั้น: ตัวค่า vs เวอร์ชันของค่า |
| **effective_date** | วันที่เวอร์ชันเริ่มมีผล — หัวใจของ HR-1 |
| **Scheduled / Superseded** | สถานะเวอร์ชัน "รอมีผล" / "ถูกแทนแล้ว (อ่านได้อย่างเดียว)" |
| **soft archive** | ปิดใช้โดยไม่ลบข้อมูล — ของเดิมที่อ้างอยู่ยังอ่านได้ |
| **where-used** | รายการ feature ปลายทางที่อ่านค่านี้อยู่ |
| **งวดที่ปิดแล้ว** | แถวใน `hr_pay_period` ที่สถานะ `closed` — เป็นนิยามที่ BR-04 ใช้บล็อกการตั้งวันย้อนหลัง |
| **resolve(date, company)** | สัญญาการอ่านค่าจุดเดียวสำหรับ 8 feature ปลายทาง |
| **SecC** | ท่อ Security Consequence ของ ENG-CSQ 7C — ท่อเดียวที่ feature นี้ประกาศได้ |
| **`[ASSUMED]`** | ค่าที่เลนเดาตาม default table เพราะยังไม่มีคำตอบ — ต้องให้ Strike/BA เคาะ |
| **`[AI-DRAFT]`** | ข้อเสนอที่ AI ร่างจากมาตรฐาน ERP — รอ BA ยืนยันผ่าน wireframe review |

## C. Document Control

| | |
|---|---|
| แหล่งข้อมูล | PREBRIEF.md v1.1 · FUNCTION_CHECKLIST.md (53 FN) · STANDARD_BASELINE.md (19 MUST · 5 states) · STANDARD_GAP.md (G-01…G-07) · LANE_BRIEF.md · CONTEXT_PACK/HR.md · 1_HTML/ตั้งค่าHR.html (ผ่าน S3a/S3b/S3c) · 5_DECLARATIONS/{CSQ_BRIEF, NOT_NEEDED}.md |
| Conflict Resolution ที่ใช้ | LOCK > business intent (PREBRIEF) > HTML หน้าจอจริง — **ไม่พบ conflict** |
| ⚠️ HTML–INTENT DRIFT | **ไม่พบ** — ทุก route ใน HTML มี FN คู่ · ทุก FN มีที่ยืนใน HTML (COVERAGE_R1: FN 53/53 ✓) |
| เอกสารถัดไป | `frd-generator-v6` (S5) → `3_FRD/00_OVERVIEW…07_LOCKED + INDEX` |
| ไม่มีในชุดนี้โดยเจตนา | `PRINT_SPEC.md` (ไม่มีท่อ pdfdoc) · `DOA_BRIEF.md` · `NTF_BRIEF.md` · `DOCCFG_BRIEF.md` (ดู `5_DECLARATIONS/NOT_NEEDED.md`) |

---

# AI Review Report

```
═══════════════════════════════════════════════════════
AI REVIEW REPORT — brd-generator-full v2.2 (Lane Mode v2)
═══════════════════════════════════════════════════════
BRD: BRD-HR-CONFIG-001 — HR Configuration (ตั้งค่าHR)
ประเภท: New Feature
วันที่ตรวจ: 2026-08-28
Checklist ที่รัน: C01-C23 + PE01-PE05  (Total Checks: 28)

CORE CHECKLIST (C01-C19)
───────────────────────────────────────────────────────
✅ C01: Business Objective ชัดเจน วัดผลได้ — §2.2 (G-01…G-06) + §2.3 มี 6 ตัวชี้วัดพร้อมตัวเลข
✅ C02: User Roles ครบ — §4.1 5 roles + §4.2 Permission Matrix 12 action
✅ C03: Scope ชัดเจน — §3.1 In Scope 10 ข้อ · §3.2 Out of Scope 16 ข้อ · §3.3 Assumptions 10 ข้อ
✅ C04: User Journey มี Happy Path + Alt Path — §5.1 (J-01…J-07) + §5.2 (7 alt paths) + §5.3 (11 exception paths)
✅ C05: Story Breakdown ไม่มีคำว่า "และ" — ตรวจ description ของ ST-01…ST-37 ทั้ง 37 story: ไม่พบ
✅ C06: AC แบบ Given-When-Then — ทุก story มี AC ≥2 ข้อ (ST-03/ST-21 มี 3 ข้อ)
✅ C07: Data Entity + ER Diagram — §6.1 13 entity · §6.2–6.9 field table · §6.10 ER diagram + relationship table
✅ C08: Audit Fields ทุก Entity — created_by/date + modified_by/date ครบทั้ง E-01…E-13 (ระบุใน §6.1)
✅ C09: Status & Lifecycle มี State Diagram — §8.1 diagram 5 states + §8.2 transition table 11 แถว + §8.3 lifecycle ย่อยของงวด
✅ C10: Business Rules ติด Tag ครบ — BR-01…BR-21 ทั้ง 21 ข้อมี Tag (FIXED 15 · CONFIGURABLE 5 · DYNAMIC 1) · ไม่มี rule ที่มีตัวเลขแล้วไม่ติด tag
✅ C11: ระดับความยืดหยุ่นชัดเจน — §9.5 ทุก CONFIGURABLE/DYNAMIC ระบุระดับ (Admin Panel ×5 · Rule Management ×1)
✅ C12: Validation Rules ครบ — §9.2 VR-01…VR-30 ครอบทุก required field + ทุก BR ที่บล็อก/เตือน
✅ C13: Edge Cases ครบหมวด — §10.2 มี 6 หมวด (CA · ST · CL · DI · PM · EM) เกินเกณฑ์ 3 หมวด
✅ C14: แยก BA-confirmed + AI-suggested — §10.1 ☑ 15 ข้อ (จากต้นทาง) · §10.2 ☐ 17 ข้อ (AI) + 🔺 4 ข้อยกเป็น OQ ทันที
✅ C15: Dependencies ครบ — §12.2 8 dependency พร้อมสถานะ + ผลถ้าไม่มี
⚠️ C16: ไม่มี System_Module_Registry ในเวิร์กสเปซ → §12.3 ใช้ CONTEXT_PACK + current-state §2 แทน + placeholder + Q-17 (informational — ไม่ FAIL ตาม checklist)
✅ C17: Delivery Phases 1-4 — §13 Phase 1 (10 งาน) · Phase 2 (5 rule) · Phase 3 (2 + engine candidate) · Phase 4 (2 + engine candidate)
✅ C18: WARNING ทุกข้อมีแผนหารือ — §14.4 ทุกแถวระบุ "หารือกับใคร + กำหนดวันที่ + บล็อกอะไร" ครบ 6 แถว · §15 ทุก OQ มีเจ้าภาพ
✅ C19: Section 14 ใบสั่งครบ — 14.1 (11 CF) · 14.2 (tag → dev action) · 14.3 (12 D-XX) · 14.4 (WARNING) · 14.5 (N/A New Feature ระบุเหตุผล) · 14.6 (screen + UI signals + Functions Cut)

BUSINESS COMPLETENESS (C20-C23)
───────────────────────────────────────────────────────
✅ C20: Scope Lock — §3.4 ยก LOCK ครบ 8 รายการจาก LANE_BRIEF · Scope Drift check ทำแล้ว = ไม่มีข้อเกินใบเซ็น · S-31/S-32/FN-50 อธิบายที่มา (STANDARD_GAP MUST/SHOULD) ไม่ใส่เงียบ
✅ C21: Value Stream & Downstream — §12.1 positioning + upstream 5 แถว + Downstream Impact Map 9 แถว (ทุกแถวตอบ "ข้อมูลอะไรไหลไป / trigger อะไร / เปลี่ยนแล้วกระทบยังไง") + ผลกระทบแนวขวาง 6 ด้าน + document flow chain · ข้อที่ยืนยันไม่ได้ (VS Bible) ยกเป็น Q-16 ไม่เว้นว่าง
✅ C22: ตัวชี้วัดวัดได้จริง — §2.3 M-01…M-06 ทุกตัวมี Baseline/Target/วิธีวัด/จังหวะวัด · M-01, M-03 ระบุ "ต้องเก็บ baseline ก่อน launch" เป็น action · ทุกตัวมีคู่ใน §17.3 (K-01…K-06)
✅ C23: Flexibility Attribution — §9.5 ทุก rule มี marker 🤖/✅ · 🤖 + DYNAMIC (BR-13) อยู่ใน §15 Q-09 แล้ว · BR-05 (🤖 + Admin Panel แต่เป็นตัวเลขกฎหมาย) ยกเป็น Q-10 เพิ่มเอง

PHILOSOPHY EMBED CHECKLIST (PE01-PE05)
───────────────────────────────────────────────────────
✅ PE01: COSO Roles ครบทุก step — §5.1/§5.2/§5.3 ทุกแถวมี Maker/Checker/Approver/System ครบ 4 คอลัมน์ · คอลัมน์ Approver = "—" ทุกแถว **โดยเจตนา** พร้อมเหตุผลที่หัว §5 (ไม่ใช่ข้อมูลขาด)
✅ PE02: SoD ผ่าน — ไม่มี approval step ใน feature นี้ → ไม่มีแถวที่ Maker = Approver · compensating control 5 ข้อระบุไว้ที่หัว §5 · ประเด็นถูกยกเป็น OQ-STD-01 ไม่ตัดเงียบ
✅ PE03: Security Preset + Controls — §16.1 P6 (HR/PII Sensitive · 15 controls) + เหตุผล · §16.2 ครบ 14 standards พร้อม ✅/❌/○ · §16.3 Control Checklist 15+1 controls พร้อม Implementation Notes · §16.4 Risk Statement 7 risks (เกินเกณฑ์ 3)
✅ PE04: Section 17 ครบ 5 sub-section — 17.1 SLA 5 · 17.2 Control Points 7 · 17.3 KPI 9 (เกิน 3) · 17.4 Threshold 8 พร้อม Min/Max/Action · 17.5 Throughput (Capacity/Baseline/Stress Point + จุดกระจุกตัว)
✅ PE05: Cross-Section Coverage
      · BC → Edge Case: BR-01…BR-21 ทุกข้อมี EC/EA คู่ใน §10 ✅
      · Control (runtime) → Control Point: S01-04, S01-07, S02-05, S06-01, S06-03, S07-06, S14-02 → §17.2 ครบ 7 ✅
      · SLA/KPI/Threshold → Widget/Report: K-01…K-09 + SLA-01…SLA-05 → §18.2 widget 9 ใบ + §18.3–18.6 ✅

LANE MODE v2 EXTRA CHECKS
───────────────────────────────────────────────────────
✅ ทุก FN-XX (53) ปรากฏใน BRD — §7.4 Function Ledger (in scope 42 · ไม่รองรับ 11)
✅ ทุก S-XX (35) ปรากฏใน BRD — §10.0 Scenario Ledger (in scope 24 · ไม่รองรับ 11)
✅ §14.6 Functions Cut = หมวด "ไม่รองรับ" ของ FUNCTION_CHECKLIST ครบ **14 รายการ** (NS-01…NS-14)
✅ Screen Inventory สกัดจาก HTML จริง (7 routes + drawer/modal) — ไม่แต่งหน้าเพิ่ม ไม่ตัดหน้า
✅ Declarations ตรงกับ _lane/DECL.json — CSQ (SecC) need · DOA/NTF/DOCCFG/PDFDOC not needed · ไม่ประกาศ OC/DC-เอกสาร/SC
✅ PRINT_SPEC ไม่มีโดยเจตนา — ระบุเหตุผลไว้ที่ §14.6.4 ไม่ปล่อยหายเงียบ
✅ MUST ทั้ง 19 จาก STANDARD_BASELINE ถูกปิดหรือยกเป็น OQ — C-01…C-17 มี S/FN/BR ตรง · C-18→OQ-STD-01 · C-19→OQ-STD-04 · C-20→OQ-STD-03 (ไม่มี MUST ใดถูกตัดเงียบ)
✅ DIVERGENCE: — ไม่มี

SUMMARY
───────────────────────────────────────────────────────
ผ่าน (✅): 27/28
เตือน (⚠️): 1/28 — C16 (ไม่มี System_Module_Registry · informational ตาม checklist "⚠️ ถ้าไม่มี Registry → placeholder + warn")
ไม่ผ่าน (❌): 0/28

Verdict Logic: fail_count == 0 → APPROVED
Override check: C18 ✅ · PE02 ✅ · C20 ✅ · C22 ✅ · C21 ✅ · C23 ✅ — ไม่มี override ทำงาน

สถานะ: ✅ **APPROVED** — พร้อมเข้า frd-generator-v6 (S5)

หมายเหตุ (ไม่บล็อก):
- C16: ขอ System_Module_Registry เพื่อทำ §12.3 ให้สมบูรณ์ขึ้น (Q-17)
- Q-13, Q-14, Q-15 ต้องปิดก่อนปิด FRD (กระทบสัญญา resolve() กับ 8 feature)
- Q-10 ต้องปิดก่อน go-live (ค่าขั้นต่ำตามกฎหมาย)
```
