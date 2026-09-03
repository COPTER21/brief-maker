# 00_OVERVIEW — F-HR-SALSTRUCT · Salary Structure (โครงเงินเดือน)

> **Audience:** ทุกบทบาท — อ่านไฟล์นี้ก่อนเสมอ
> **สิ่งที่ feature ปลายทางต้องอ่าน:** **§0.13 Published Rate Surface** · **§0.14 Invariants** · **§0.15 Soft-Reference Read Model** — ยกไปวางใน `00_OVERVIEW §Dependencies` ของ feature ตัวเองได้ทันที

## §0.1 Document Control

| Field | Value |
|---|---|
| Feature Code | `F-HR-SALSTRUCT` |
| Feature Name | Salary Structure — โครงเงินเดือน |
| Module / Wave / Lane | HR · W1 · Lane B |
| FRD Version | 1.0 |
| Pack Variant | **FULL** (9 files + INDEX) — เหตุผล: `pages=6` · `states≥4` (3 state machine · 6+5+4 state) · `money=yes` (จำนวนเงิน + กติกาเทียบกระบอก) · `approval=no` — เข้าเงื่อนไข `states ≥ 4` → FULL |
| Archetype | `master/config` (A+B+C) — **ไม่ใช่ Pattern Q** (ไม่มีอนุมัติ · ไม่มีเลขที่เอกสาร · ไม่มีลายเซ็น · ไม่มี PDF) |
| Data Classification (สูงสุดที่แตะ) | **RESTRICTED** |
| Source BRD | `2_BRD/BRD_โครงเงินเดือน.md` v1.0 — **APPROVED** (C01–C23 + PE01–PE05 = 28/28) |
| Source HTML | `1_HTML/โครงเงินเดือน.html` (5 routes · md5 `1980d75c6ce095a2c63598d1662ff10b` · ผ่าน S3a audit FAIL=0 · S3b UX BLOCK=0 · S3c coverage 65/65 FN) |
| Mode | **Lane Mode v2** (frd-generator-v6 · no-ask · Phase 2.5 probing ตอบเองแล้ว tag `[AI-DEFAULT]`) |
| Design Authority | **Mode A — Recognize & Validate** (มี HTML ที่ผ่าน gate) → FRD สกัด+ตรวจ+บันทึก · ห้ามเขียน spec สวนจอ |
| **PRINT_SPEC** | **ไม่มีในแพ็กนี้โดยเจตนา** — feature นี้ไม่มีท่อ `pdfdoc` (`DECL.json` · `5_DECLARATIONS/NOT_NEEDED.md`) · ไม่มีเอกสารที่คนถือ/ยื่น/พิมพ์ · หนังสือรับรองเงินเดือน = feature **หนังสือรับรอง (W3)** · payslip = **Payroll (W4)** |
| Created | 2026-08-28 |

## §0.2 Revision History

| Version | Date | Change | By |
|---|---|---|---|
| 1.0 | 2026-08-28 | สร้าง FRD Pack จาก BRD v1.0 (APPROVED) + HTML v9 ที่ผ่าน gate · Phase 3.5 A–M ผ่านทั้งหมด | frd-generator-v6 (Lane Mode v2) |

## §0.3 Scope

### In Scope
1. ระดับ + กระบอกเงินเดือน (min–mid–max) แบบมีเวอร์ชันกับวันมีผล · ไม่ทับช่วง · append-only
2. ทะเบียนองค์ประกอบค่าจ้าง + `payroll_code` + แฟล็กอ้างอิง (`include_in_band_base` · `is_ot_base` · `is_ssf_base` · `prorate_by_payment_days`)
3. อัตราค่าจ้างรายคน (effective-dated · ประวัติเต็ม · ประเภทการเปลี่ยน + เหตุผล + เลขที่คำสั่งอ้างอิง)
4. เงินได้/เงินหักประจำคงที่รายคน + ยอดเป้าหมาย + การปิดรายการอัตโนมัติ
5. ตัวชี้วัดตำแหน่งในกระบอก (compa-ratio · range penetration · ฐานเทียบเต็มเวลาเมื่อ FTE < 1) — **แสดงผลอย่างเดียว**
6. การเตือนนอกกระบอก + การเตือนต่ำกว่าค่าแรงขั้นต่ำตามกฎหมาย (ค่ามาจาก HR Configuration)
7. การปิดบังข้อมูลตาม role + audit ทุกการเปิดดู (ผ่าน Policy Center)
8. การอ่านค่านโยบายจาก HR Configuration (`resolve(date, company)` + `version_id` + ฟัง 3 event)
9. **Published Rate Surface** (§0.13) — สัญญาการอ่านสำหรับ Payroll · Manpower Planning · หนังสือรับรอง · Employee Movement
10. ทะเบียนการใช้งาน (where-used) + Module Linkage
11. จุดรับอัตราใหม่จาก Employee Movement (idempotent ตามเลขที่คำสั่ง)

### Out of Scope
1. อนุมัติ / สาย DOA / เลขที่เอกสาร / ลายเซ็น / PDF → **Employee Movement (W3)**
2. ภาษี · ประกันสังคม · กองทุนสำรองเลี้ยงชีพ · ยอดจ่ายสุทธิ · payslip → **Payroll (W4)**
3. ปรับค่าจ้างหมู่ (mass revision) · merit worksheet → **Employee Movement (W3)** + **Performance (W5)**
4. หน้าตั้งค่าพารามิเตอร์ HR ทุกชนิด → **HR Configuration** (#107)
5. หลายสกุลเงิน · geo zone · step ในระดับ · variable pay · mass import/export · retro engine → ดู `07_LOCKED_DECISIONS §7.3` + BRD §14.6
6. permission engine / masking engine / audit store ของตัวเอง → **Policy Center**

### Out of Scope (จาก Phase 2.5 probing — บันทึกไว้ไม่ให้หายเงียบ)
- **PR-5 (bulk operation):** ไม่มี bulk ในรอบนี้ (สอดคล้อง NS-06) — probe ตอบว่า "ไม่ทำ" ตาม BRD
- **PR-8 (file upload):** ไม่มีการแนบไฟล์ — หลักฐานการปรับเงินเดือนแนบที่ Employee Movement
- **PR-9 (soft delete vs hard delete):** hard delete ไม่มีในระบบนี้ (P-4) — probe ตอบด้วย LOCK ไม่ใช่ default

## §0.4 Roles & Responsibilities (COSO)

| Role | Maker | Checker | Approver | System | หมายเหตุ |
|---|:---:|:---:|:---:|:---:|---|
| HR Comp Admin | ✅ | — | — | — | ผู้สร้าง/แก้ทุกอย่างในแพ็กนี้ |
| HR Manager | — | ✅ | — | — | สอบทานรายงานนอกกระบอก / ต่ำกว่าขั้นต่ำ · ปิดใช้/เปิดใช้ระดับ |
| หัวหน้าสายงาน | — | — | — | — | อ่านอย่างเดียว (เห็นเฉพาะลูกทีมตาม ABAC ของ Policy Center) |
| พนักงานทั่วไป | — | — | — | — | เห็นกระบอกของระดับ · ตัวเลขรายบุคคลถูกปิดบัง |
| ระบบ (scheduler) | — | — | — | ✅ | เปลี่ยนสถานะตามวันมีผล · ปิดช่วง · ปิดรายการที่ครบเป้า |
| Employee Movement (W3) | — | — | **✅ (นอก feature นี้)** | — | **การอนุมัติทั้งหมดอยู่ที่นั่น** — feature นี้ไม่มีขั้นอนุมัติ (BR-21) |

> **SoD:** Maker (HR Comp Admin) ≠ Checker (HR Manager) เสมอ · ไม่มีเคส Maker = Approver เพราะ **ไม่มี Approver ในแพ็กนี้โดยเจตนา** — ประกาศไว้ที่ BRD §5 หัวข้อ COSO

## §0.5 Dependencies

### Upstream (feature นี้ต้องพึ่ง)

| Feature / Engine | สถานะ | ใช้อะไร | สัญญา |
|---|---|---|---|
| **HR Configuration** `F-HR-CONFIG` | ✅ ส่งมอบ 2026-08-28 | `period_rule` (+ `pay_period` สถานะเปิด/ปิด) · `ot_rate` · **`legal_minimum` (ขอเพิ่ม — OQ-STD-11)** | `GET /api/v1/hr-config/resolve?date&company_id&group` → คืน `version_id` · กติกา **C-1…C-6** (§0.14.2) |
| **Employee Master** | ✅ | พนักงาน · ตำแหน่ง · แผนก (combobox #102) | soft ref `employee_id` + `employee_name_snapshot` |
| **Organization** | ✅ | บริษัท/หน่วยงาน | soft ref `company_id` + snapshot |
| **Policy Center** | ✅ | role · นโยบาย masking (ABAC) · audit store | เรียกตอน runtime — ไม่เก็บสำเนาสิทธิ์ |
| **ENG-CSQ 7C** | ✅ | ปลายทางของ 10 event (EC · SecC) | `5_DECLARATIONS/CSQ_BRIEF.md` |
| **Employee Movement** | ⏳ W3 | อัตราใหม่ที่อนุมัติแล้ว + `movement_doc_no` | `POST /rates/from-movement` (idempotent) — รอบนี้กรอกมือได้ |
| **On/Offboard** | ⏳ W3 | คนเข้าใหม่ · วันพ้นสภาพ | รอบนี้กรอกมือ |

### Downstream (feature ที่พึ่ง feature นี้) — **อ่าน §0.13**

| Feature | สถานะ | อ่านอะไร | ผ่านอะไร |
|---|---|---|---|
| **Payroll** `F-HR-PAYROLL` | ⏳ W4 | อัตราปัจจุบัน + องค์ประกอบ + รายการประจำ + `version_id` ณ วันงวด | `GET /api/v1/salary-structure/resolve` (§0.13.2) |
| **Manpower Planning** `F-HR-MANPOWER` | ⏳ W6 | mid-point ต่อระดับ + จำนวนคนต่อระดับ | `GET /api/v1/salary-structure/bands/resolve` (§0.13.3) |
| **หนังสือรับรอง** `F-HR-CERT` | ⏳ W3 | เงินเดือนปัจจุบัน ณ วันออกหนังสือ (snapshot) | `GET /api/v1/salary-structure/resolve` (§0.13.2) |
| **Employee Movement** `F-HR-MOVEMENT` | ⏳ W3 | อัตราปัจจุบัน + กระบอก (เพื่อร่างคำสั่ง) · เขียนกลับ: อัตราใหม่ | อ่าน §0.13.2 · เขียน `POST /rates/from-movement` |
| **ESS Portal** | ⏳ W6 | มุมมองของพนักงานเอง | อ่านผ่าน feature ต้นทาง — ไม่เรียกตรง (OQ-HR-04) |

### External
ไม่มีการเชื่อมระบบภายนอกใน feature นี้

## §0.6 Stack & Architecture

| ชั้น | สิ่งที่ใช้ | หมายเหตุ |
|---|---|---|
| UI | SPA hash routing 5 route ภายใต้ 1 เมนูซ้าย (#104) · Pattern A (list) + B (wizard 3 ขั้น) + C (view drawer tabbed) + D (modal 440) + M (workspace) | ยึดตาม HTML v9 ที่ผ่าน gate — `01_UI §1.0` |
| API | REST `/api/v1/salary-structure/*` — HTTP layer บาง ไม่มี business logic | `02_API` |
| Logic | Functions (scope-local) + Engines (reusable) | `03_LOGIC` — R8: ทุก mutation API trace ไป Function/Engine |
| DB | ตาราง 9 ชุด · effective-dated + append-only · ไม่มี DELETE | `04_DB` |
| Integration | เรียก `hr-config/resolve` (ขาเข้า) · publish 10 CSQ event (ขาออก) · เปิด read contract ให้ 4 consumer | `02_API §2.X` |
| Scheduler | งานเบื้องหลังรายวัน 00:00 — เลื่อนสถานะตามวันมีผล · ปิดรายการที่ครบเป้า | `03_LOGIC` ENG-EFFDATE-01 |

## §0.7 Multi-Tenant & Security Context

- **Tenant isolation:** ทุกตารางมี `tenant_id` · ทุก query กรองด้วย tenant เสมอ (D17)
- **Company scope:** ระดับ/กระบอกมี `company_scope` + `companies[]` — ค่าเฉพาะบริษัททับค่ากลาง (แพทเทิร์นเดียวกับ HR Configuration) · **ยังไม่มี UI สลับบริษัท** (OQ-HR-05)
- **Security Preset:** **P6 (HR/PII Sensitive)** — 15 controls · Must 9 ข้อ (BRD §16.3)
- **สิทธิ์:** จาก Policy Center (RBAC + **ABAC** สำหรับ "หัวหน้าเห็นเฉพาะลูกทีม") — feature นี้ไม่ประกาศ permission เอง

### §0.7.1 Data Classification Summary ⭐

| ระดับสูงสุดที่ feature นี้แตะ | **RESTRICTED** |
|---|---|
| Restricted | `base_amount` · `amount` / `percent` ของรายการประจำ · `goal_amount` · `accrued_amount` · `total_fixed_monthly` (computed) · `compa_ratio` เมื่อผูกกับบุคคล |
| Confidential | `min/mid/max` ของกระบอก · `mid_amount` ที่ Manpower อ่าน · `out_of_range_reason` · `change_reason` |
| Internal | `grade_code` · `grade_name` · `component_code` · `payroll_code` · สถานะ · วันมีผล · ทะเบียนการใช้งาน |
| Public | — (ไม่มี field ใดใน feature นี้เป็น Public) |
| PII overlay | `employee_id` · `employee_name_snapshot` · `changed_by` / `created_by` |

> **Restricted fields → ต้องผูกกับ Policy Center Restricted Resources** — ดู Open Question **OQ-FRD-05** (§0.8) และ `04_DB §4.6.6`

## §0.8 Open Questions

> สืบทอดจาก BRD §15 (24 ข้อ) + เพิ่มระดับ FRD 6 ข้อ · ทุกข้อมี default ที่ใช้ไปก่อน — **ไม่มีข้อใดบล็อกการพัฒนา Phase 1**

| # | คำถาม | Default ที่ใช้ไปก่อน | tag | เจ้าภาพ | promote ไป |
|---|---|---|---|---|---|
| OQ-STD-01…13 · OQ-SS-01…03 · OQ-HR-01 · OQ-HR-05 · OQ-CSQ-01 · OQ-BRD-01…05 | ดู BRD §15 (ยกมาทั้งชุด ไม่ตัด) | ตาม BRD | `[ASSUMED]` / `[AI-DRAFT]` / `[AI-DEFAULT]` | ตาม BRD | `07_LOCKED_DECISIONS §7.3` |
| **OQ-FRD-01** | `GET /salary-structure/resolve` ควรรองรับโหมดอ่านทั้งบริษัทในครั้งเดียวหรือไม่ (Payroll ยิงทีละคน 5,000 ครั้งไม่ไหว) | **รองรับ** — `scope=company` คืนเป็นชุด + เพจ (ดู §0.13.2) | `[AI-DEFAULT]` | Architect / Payroll | 02_API-24 |
| **OQ-FRD-02** | การเปลี่ยนสถานะตามวันมีผล ใช้ scheduler หรือคำนวณ as-of ตอนอ่าน | **ทำทั้งคู่** — as-of เป็นความจริงตอนอ่าน · scheduler เขียน `record_status` ให้รายงาน/ตัวกรองเร็ว (idempotent · รันซ้ำได้) | `[AI-DEFAULT]` | Tech Lead | 03_LOGIC ENG-EFFDATE-01 |
| **OQ-FRD-03** | เก็บ `version_id` ของ HR Config ที่ระดับไหน | เก็บที่ระดับ **เรคคอร์ดที่ถูกตรวจ** (`legal_min_version_id`, `period_version_id`) + ตารางอ้างอิงรวม `T_salstruct_cfg_ref` | `[AI-DEFAULT]` | Architect | 04_DB §4.2 |
| **OQ-FRD-04** | `masked` ควรทำที่ชั้น API หรือชั้น UI | **ชั้น API เท่านั้น** — UI ไม่เคยได้รับตัวเลขจริงถ้าไม่มีสิทธิ์ (D7 · S02-04) | `[AI-DEFAULT]` (ตาม LOCK BR-16) | Security | 02_API §2.3 · 05_RULES §5.7 |
| **OQ-FRD-05** | ผูก Restricted fields เข้า Policy Center Restricted Resources ตอนไหน | **ก่อน go-live Phase 1** — ไม่มี masking = ไม่เปิดหน้าอัตรา | `[AI-DEFAULT]` | Security / BA | 04_DB §4.6.6 |
| **OQ-FRD-06** | ถ้า `hr-config/resolve` ล่ม ระบบควรทำอย่างไรกับการบันทึกที่ต้องใช้ค่านั้น | **ปิดปุ่มบันทึกเฉพาะเส้นทางที่ต้องใช้ค่า** + แสดงเหตุผล · ห้าม fallback เป็นค่าที่จำไว้ข้ามวัน | `[AI-DEFAULT]` | Tech Lead | 05_RULES EC-19 · Error `ERR_HRCFG_UNAVAILABLE` |

## §0.9 Glossary
ดู BRD Appendix B (ใช้ชุดเดียวกัน) · เพิ่มเฉพาะคำเชิงเทคนิคของแพ็กนี้:

| คำ | ความหมาย |
|---|---|
| **rate snapshot** | ชุดข้อมูลที่ §0.13.2 คืนกลับ: อัตราฐาน + องค์ประกอบ + รายการประจำ + `version_id` + `as_of` |
| **as-of read** | การอ่านที่คำนวณสถานะจากวันที่ที่ส่งมา ไม่ใช่จากคอลัมน์สถานะที่เก็บไว้ |
| **effective window** | ช่วง `[effective_date, effective_to]` ที่ระบบคำนวณให้เอง ห้ามกรอกมือ |
| **masked value** | ค่าที่ API คืนเป็น `null` พร้อม `masked: true` (ไม่เคยส่งตัวเลขจริงออกจากเซิร์ฟเวอร์) |

## §0.10 Pack Navigation

| ไฟล์ | ใครอ่าน | มีอะไร |
|---|---|---|
| `00_OVERVIEW.md` | ทุกคน | scope · dependencies · **§0.13 published surface** · §0.14 invariants · §0.15 read model · §0.12 coverage manifest |
| `01_UI.md` | FE | Layout Decision Log · 6 หน้า · journey · empty state |
| `02_API.md` | BE | 27 endpoint + cross-module contract + trace ไป logic |
| `03_LOGIC.md` | BE | 55 function + 6 engine + trace table |
| `04_DB.md` | DBA / BE | 9 ตาราง + classification + retention |
| `05_RULES.md` | BE / QA | BR-24 ข้อ · VR · state machine · edge case · error catalog · Security Bible |
| `06_TESTS.md` | QA | AC · test inventory · DoD · cross-module test |
| `07_LOCKED_DECISIONS.md` | ทุกคน | Scope Lock (immutable) · LD · OQ ที่ promote ขึ้นมา |
| `INDEX.md` | ทุกคน | cross-reference + R8 matrix + สถิติ |
| `UI_BRIEF_โครงเงินเดือน.md` | FE / BA | สรุปหน้าจอจาก HTML จริง + Drift Log (S7) |
| **`PRINT_SPEC.md`** | — | **ไม่มีโดยเจตนา** (ไม่มีท่อ pdfdoc — ดู §0.1) |

## §0.11 Scope Lock (pointer)
Scope Lock ฉบับเต็ม (immutable) อยู่ที่ **`07_LOCKED_DECISIONS §7.0`** — ยกมาจาก BRD §3.4 ทั้งชุด: HR-1 · C-1…C-6 · P-1…P-9 · #107 · LD-4C-02 · DOA iron rule · audit append-only · 7C ท่อต้องห้าม · Data Masking · UI standard

## §0.12 Coverage Manifest ⭐ (R13 — กัน requirement หล่น BRD→FRD · **มีคอลัมน์ FN-XX ตาม Lane Mode v2**)

### §0.12.0 Function Ledger — **65/65 FN** → ที่อยู่ในแพ็ก

| FN | Story | UI | API | LOGIC | DB | RULES | TESTS |
|---|---|---|---|---|---|---|---|
| FN-01 | ST-01 | P-01 wizard | API-02 | `createBandDraft` | `T_ss_grade` · `T_ss_band_version` | BR-01 · VR-01/02 | AT-01 |
| FN-02 | ST-02 | P-01 wizard ขั้น 2–3 | API-04 | `publishBandVersion` | `T_ss_band_version` | BR-02 · VR-03/04/05 | AT-02 |
| FN-03 | ST-03 | P-01 list (ตัวกรอง as-of) | API-01 | `resolveBandAt` · `advanceEffectiveStates` | `T_ss_band_version` | BR-02 | AT-03 |
| FN-04 | ST-04 · ST-05 | P-01 + P-06 drawer | API-02 · API-09 | `applyPercentAdjust` · `buildVersionDiff` | `T_ss_band_version` | BR-02 · BR-01 | AT-04 · AT-05 |
| FN-05 | ST-06 | P-01 wizard error | API-02 | `assertBandOrder` | — | BR-01 · VR-02 | AT-06 |
| FN-06 | ST-07 | P-01 view drawer | API-03 (ปฏิเสธ) | `assertVersionEditable` | — | BR-02 · ERR_VERSION_NOT_EDITABLE | AT-07 |
| FN-07 | ST-08 | P-01 wizard error | API-02 · API-04 | `assertNoOverlap` | unique index | BR-03 · VR-03 | AT-08 |
| FN-08 | ST-09 | P-01 modal | API-05 | `withdrawBandVersion` | `T_ss_band_version` | BR-02 · VR-05 | AT-09 |
| FN-09 | ST-10 | P-01 modal ปิดใช้ | API-06 · API-21 | `deactivateGrade` · `countWhereUsed` | `T_ss_grade` · `T_ss_consumer_usage` | BR-05 · BR-22 · VR-19 | AT-10 |
| FN-10 | ST-11 | P-01 list · P-03 drawer | API-01 · API-13 | `listGradeOptions` | — | BR-05 · BR-18 · VR-17 | AT-11 |
| FN-11 | ST-12 | P-01 modal เปิดใช้ | API-07 | `reactivateGrade` | `T_ss_band_version` | BR-02 | AT-12 |
| FN-12 | ST-13 | P-01 drawer tab ประวัติ | API-08 | `listVersionHistory` | `T_ss_band_version` | BR-02 · BR-05 | AT-13 |
| FN-13 | ST-14 | P-02 wizard | API-11 | `createPayComponent` | `T_ss_pay_component` | BR-12 · VR-12 | AT-14 |
| FN-14 | ST-15 | P-02 wizard (ช่องรหัสส่งจ่ายเงิน) | API-11 | `createPayComponent` | `payroll_code` | BR-13 · VR-13 | AT-15 |
| FN-15 | ST-16 | P-02 wizard (สวิตช์ฐานกระบอก) | API-11 | `computeBandBase` | `include_in_band_base` | BR-06 | AT-16 |
| FN-16 | ST-18 | P-02 wizard error | API-11 | `detectComponentCycle` | — | BR-12 · VR-12 | AT-17 |
| FN-17 | ST-19 | P-02 modal | API-12 | `deactivateComponent` · `countWhereUsed` | `status` | BR-05 · BR-22 | AT-18 |
| FN-18 | ST-20 | P-03 wizard ขั้น 1 | API-13 · API-14 | `suggestGradeForEmployee` | `employee_id` + snapshot | BR-19 | AT-19 |
| FN-19 | ST-21 | P-03 wizard ขั้น 2 | API-14 | `assertCompRecordComplete` | — | BR-10 · VR-05/07 | AT-20 |
| FN-20 | ST-23 | P-03 list (pill รอมีผล) | API-13 · API-24 | `resolveCurrentRate` | `record_status` | BR-11 · P-6 | AT-21 |
| FN-21 | ST-24 | P-03 list + drawer (แถบกระบอก) | API-13 | `computeCompaRatio` · `computeRangePenetration` | computed | BR-07 | AT-22 |
| FN-22 | ST-25 | P-03 wizard note | API-14 | `evaluateOutOfRange` | `out_of_range_flag` · `out_of_range_reason` | BR-08 · VR-08 | AT-23 |
| FN-23 | ST-26 | P-03 wizard note | API-14 | `evaluateOutOfRange` | เดียวกัน | BR-08 · VR-08 | AT-24 |
| FN-24 | ST-28 | P-03 drawer (ฐานเทียบเต็มเวลา) | API-13 | `computeFteAdjustedBase` | `fte` | BR-09 · VR-11 | AT-25 |
| FN-25 | ST-29 | P-03 stat card + filter | API-13 (`unassigned=true`) | `computeUnassignedCount` | (LEFT JOIN Employee) | BR-19 | AT-26 |
| FN-26 | ST-30 | P-03 drawer tab ประวัติ | API-14 · API-17 | `closePreviousCompRecord` | `effective_to` · `record_status` | BR-05 · BR-11 | AT-27 |
| FN-27 | ST-31 | P-03 modal ถอน | API-15 | `withdrawCompRecord` | `record_status` | BR-10 | AT-28 |
| FN-28 | ST-32 | P-03 modal ปิดช่วง | API-16 | `endCompRecord` | `effective_to` | BR-05 | AT-29 |
| FN-29 | ST-33 | P-03 wizard error + ปุ่มวันเร็วที่สุด | API-14 | `assertNotInClosedPeriod` · `earliestOpenDate` | `period_version_id` | BR-04 · VR-04 | AT-30 |
| FN-30 | ST-34 | P-04 wizard | API-19 | `createRecurringItem` | `T_ss_recurring_item` | BR-15 · VR-14/15 | AT-31 |
| FN-31 | ST-35 | P-04 wizard (ยอดเป้าหมาย) | API-19 | `createRecurringItem` | `goal_amount` | BR-14 · VR-16 | AT-32 |
| FN-32 | ST-36 | P-04 list สถานะ | (scheduler) | `evaluateRecurringEnd` | `item_status` | BR-14 | AT-33 |
| FN-33 | ST-37 | P-04 wizard error | API-19 | `assertNoOverlap` | unique index | BR-15 · VR-14 | AT-34 |
| FN-34 | ST-38 | P-03 drawer (ยอดรวม) | API-13 | `computeTotalFixedMonthly` | computed | BR-13 | AT-35 |
| FN-35 | ST-39 | ทุก route | ทุก API ที่คืนเงิน | `maskMoney` | classification | BR-16 · D7 | AT-36 |
| FN-36 | ST-40 | P-03 drawer เปิดดู | API-13 (detail) | `logRestrictedView` | (ส่งออก Policy Center) | BR-16 · D9 | AT-37 |
| FN-37 | ST-41 | `.demo-strip` | — | — | — | #105 | AT-38 |
| FN-38 | ST-42 | P-05 · drawer SEC | API-21 | `resolveHrConfig` | `T_ss_cfg_ref` | BR-17 · C-1/C-2 | AT-39 |
| FN-39 | ST-43 | ทุกจุดที่แสดงค่านโยบาย | — (ลิงก์ออก) | — | — | #107 · C-4 | AT-40 |
| FN-40 | ST-44 | ตัวเลือกในฟอร์ม | API-01 · API-10 | `filterActiveOptions` | `status` | BR-18 · C-5 | AT-41 |
| FN-41 | ST-45 | P-05 ปุ่มรับสัญญาณ | API-23 | `invalidateConfigCache` | `T_ss_cfg_ref.fetched_at` | BR-17 · C-3 | AT-42 |
| FN-42 | ST-46 | P-03 drawer ประวัติ | API-17 | `renderPersonSnapshot` | `employee_name_snapshot` | BR-19 | AT-43 |
| FN-43 | ST-47 | P-03 wizard + P-05 SEC | API-14 · **API-26** | `ingestMovementRate` | `movement_doc_no` | BR-10 · BR-21 | AT-44 · CT-04 |
| FN-44 | ST-48 | P-05 การ์ด consumer | **API-24** | `buildRateSnapshot` | ทุกตาราง | BR-20 · P-5 | AT-45 · CT-01 |
| FN-45 | ST-49 | P-05 การ์ด consumer | **API-24 · API-25** | `buildRateSnapshot` · `buildBandSnapshot` | เดียวกัน | BR-19 · BR-20 | AT-46 · CT-02 · CT-03 |
| FN-46 | ST-50 | P-05 | API-21 · API-22 | `registerWhereUsed` · `setLinkStatus` | `T_ss_consumer_usage` | BR-22 · C-6 | AT-47 |
| FN-47 | ST-55 | ทุก route (พิสูจน์ไม่มี) | — | — | — | BR-21 | AT-48 |
| FN-48 | ST-55 | P-05 SEC "งานที่ไม่ได้ทำที่นี่" | — | — | — | BR-21 | AT-48 |
| FN-49 | ST-15 | ทุกฟอร์ม (พิสูจน์ไม่มี) | — | — | — | BR-13 | AT-49 |
| FN-50 | ST-54 | drawer KV สกุลเงิน | — | `formatMoney` | `currency` = THB | BR-20 | AT-50 |
| FN-51 | ST-33 | P-03 note งวดปิด | API-14 | `earliestOpenDate` | — | BR-04 · P-9 | AT-30 |
| FN-52 | — (NS-05) | P-01 form (มีแค่ขอบเขตบริษัท) | — | — | ไม่มีคอลัมน์ geo | BR-03 | AT-51 |
| FN-53 | — (NS-06) | P-05 SEC | — | — | — | BR-05 | AT-51 |
| FN-54 | — (NS-08) | P-05 SEC | — | — | — | BR-21 | AT-51 |
| FN-55 | — (NS-09) | P-01 form (สายงาน = ป้าย) | — | — | `job_family` (label) | BR-06 | AT-51 |
| FN-56 | ST-27 | P-01 · P-03 note | API-02 · API-14 | `resolveLegalMinimum` · `evaluateBelowLegalMin` | `legal_min_version_id` | BR-23 · VR-09/10 · P-8 | AT-52 · AT-53 |
| FN-57 | ST-17 | P-02 wizard สวิตช์ | API-11 | `createPayComponent` | `prorate_by_payment_days` | BR-13 | AT-54 |
| FN-58 | ST-22 | P-03 wizard ช่องประเภท | API-14 | `assertChangeReasonCode` | `T_ss_change_reason` | BR-24 · VR-06 | AT-55 |
| FN-59 | — (NS-10) | ทุกฟอร์ม (พิสูจน์ไม่มี) | — | — | — | BR-13 | AT-51 |
| FN-60 | — (NS-11) | P-01 form (พิสูจน์ไม่มี) | — | — | — | BR-06 | AT-51 |
| FN-90 | ST-51 | ทุก list (filter แถวเดียว) | API-01/10/13/18 | `buildListQuery` | index ค้นหา | #40.1 | AT-56 |
| FN-91 | ST-52 | ทุก route | — (ไม่มี DELETE endpoint) | — | ไม่มี DELETE | BR-05 · P-4 | AT-57 |
| FN-92 | ST-53 | ทุกฟอร์ม | ทุก mutation (Idempotency-Key) | `assertIdempotent` | `T_ss_idempotency` | PR-7 | AT-58 |
| FN-93 | ST-40 | P-05 SEC บันทึกการใช้งาน | ทุก API | `emitAuditEvent` | ส่งออก Policy Center | BR-16 · D9 | AT-59 |
| FN-94 | ST-54 | ทุก route | — | `formatMoney` | `numeric(14,2)` | VR-21 | AT-50 |

**65/65 FN มีที่อยู่ครบ — ไม่มีแถวที่ช่อง "อยู่ที่" ว่าง**

### §0.12.1 Stories (BRD §7) — 55/55

| Story | ชื่อย่อ | FN | อยู่ที่ (file §) |
|---|---|---|---|
| ST-01 | สร้างระดับพร้อมกระบอก | FN-01 | 01_UI P-01 · 02_API-02 · 03_LOGIC `createBandDraft` · 05_RULES BR-01 · 06_TESTS AT-01 |
| ST-02 | ประกาศเวอร์ชันพร้อมวันมีผล | FN-02 | 01_UI P-01 · 02_API-04 · 03_LOGIC `publishBandVersion` · 05_RULES BR-02 · AT-02 |
| ST-03 | เปลี่ยนสถานะเองเมื่อถึงวันมีผล | FN-03 | 03_LOGIC ENG-EFFDATE-01 · 05_RULES §5.2 · AT-03 |
| ST-04 | คัดลอกเวอร์ชันเพื่อปรับทั้งชุด | FN-04 | 01_UI P-01 · 03_LOGIC `applyPercentAdjust` · AT-04 |
| ST-05 | เทียบค่าเก่ากับค่าใหม่ | FN-04 | 01_UI P-06 · 02_API-09 · 03_LOGIC `buildVersionDiff` · AT-05 |
| ST-06 | บล็อกกระบอกที่ค่าไม่สมเหตุผล | FN-05 | 05_RULES BR-01 · VR-02 · AT-06 |
| ST-07 | กันการแก้เวอร์ชันที่ใช้งาน | FN-06 | 02_API-03 · 05_RULES ERR_VERSION_NOT_EDITABLE · AT-07 |
| ST-08 | บล็อกช่วงวันทับกัน | FN-07 | 03_LOGIC `assertNoOverlap` · 04_DB unique index · AT-08 |
| ST-09 | ถอนเวอร์ชันที่รอมีผล | FN-08 | 02_API-05 · AT-09 |
| ST-10 | ปิดใช้ระดับโดยเห็นผลกระทบ | FN-09 | 02_API-06 · 03_LOGIC `countWhereUsed` · AT-10 |
| ST-11 | ระดับที่ปิดใช้ยังอ่านได้ | FN-10 | 05_RULES BR-18 · VR-17 · AT-11 |
| ST-12 | เปิดใช้ระดับกลับ | FN-11 | 02_API-07 · AT-12 |
| ST-13 | ดูประวัติเวอร์ชัน | FN-12 | 02_API-08 · 01_UI P-01 tab · AT-13 |
| ST-14 | สร้างองค์ประกอบค่าจ้าง | FN-13 | 02_API-11 · AT-14 |
| ST-15 | รหัสส่งจ่ายเงินเป็นสะพาน | FN-14 · FN-49 | 04_DB `payroll_code` · AT-15 · AT-49 |
| ST-16 | ระบุฐานเทียบกระบอก | FN-15 | 03_LOGIC `computeBandBase` · AT-16 |
| ST-17 | แฟล็กขึ้นกับวันทำงานจริง | FN-57 | 04_DB `prorate_by_payment_days` · AT-54 |
| ST-18 | บล็อกการอ้างวน | FN-16 | 03_LOGIC `detectComponentCycle` · AT-17 |
| ST-19 | ปิดใช้องค์ประกอบที่มีคนใช้ | FN-17 | 02_API-12 · AT-18 |
| ST-20 | ผูกอัตราผ่านทะเบียนพนักงาน | FN-18 | 01_UI P-03 · AT-19 |
| ST-21 | บังคับข้อมูลครบก่อนบันทึก | FN-19 | 05_RULES VR-05/07 · AT-20 |
| ST-22 | เลือกประเภทการเปลี่ยน | FN-58 | 04_DB `T_ss_change_reason` · AT-55 |
| ST-23 | กันอัตราที่รอมีผลจากการถูกใช้ | FN-20 | 03_LOGIC `resolveCurrentRate` · AT-21 |
| ST-24 | เห็นตำแหน่งในกระบอก | FN-21 | 03_LOGIC ENG-SALBAND-01 · AT-22 |
| ST-25 | เตือนต่ำกว่า min | FN-22 | 05_RULES BR-08 · AT-23 |
| ST-26 | เตือนเกิน max | FN-23 | 05_RULES BR-08 · AT-24 |
| ST-27 | เตือนต่ำกว่าค่าแรงขั้นต่ำตามกฎหมาย | FN-56 | 03_LOGIC `resolveLegalMinimum` · AT-52 · AT-53 |
| ST-28 | เทียบกระบอกให้พนักงานไม่เต็มเวลา | FN-24 | ENG-SALBAND-01 · AT-25 |
| ST-29 | ตามหาพนักงานที่ยังไม่มีอัตรา | FN-25 | 02_API-13 · AT-26 |
| ST-30 | อัตราเดิมเป็นประวัติที่แก้ไม่ได้ | FN-26 | 03_LOGIC `closePreviousCompRecord` · AT-27 |
| ST-31 | ถอนอัตราที่รอมีผล | FN-27 | 02_API-15 · AT-28 |
| ST-32 | ปิดช่วงเมื่อพ้นสภาพ | FN-28 | 02_API-16 · AT-29 |
| ST-33 | บล็อกวันย้อนเข้างวดที่ปิด | FN-29 · FN-51 | 03_LOGIC `assertNotInClosedPeriod` · AT-30 |
| ST-34 | เพิ่มเงินได้ประจำ | FN-30 | 02_API-19 · AT-31 |
| ST-35 | เพิ่มเงินหักประจำ + ยอดเป้าหมาย | FN-31 | 04_DB `goal_amount` · AT-32 |
| ST-36 | ปิดรายการเองเมื่อครบเป้า | FN-32 | ENG-RECUR-01 · AT-33 |
| ST-37 | บล็อกรายการที่ช่วงทับ | FN-33 | 03_LOGIC `assertNoOverlap` · AT-34 |
| ST-38 | เห็นยอดค่าจ้างประจำต่อเดือน | FN-34 | 03_LOGIC `computeTotalFixedMonthly` · AT-35 |
| ST-39 | ปิดบังตัวเลขตามสิทธิ์ | FN-35 | 03_LOGIC `maskMoney` · ENG-MASK-01 · AT-36 |
| ST-40 | บันทึกร่องรอยการเปิดดู | FN-36 · FN-93 | 03_LOGIC `logRestrictedView` · AT-37 · AT-59 |
| ST-41 | แยก demo persona ออกจากหัวจอ | FN-37 | 01_UI §1.2 · AT-38 |
| ST-42 | แสดงค่าจากตั้งค่า HR พร้อมเวอร์ชัน | FN-38 | 02_API-21 · 04_DB `T_ss_cfg_ref` · AT-39 |
| ST-43 | ลิงก์ไปจัดการที่ตั้งค่า HR | FN-39 | 01_UI ทุกหน้า · AT-40 |
| ST-44 | กันการเลือกค่าที่ปิดใช้ | FN-40 | 03_LOGIC `filterActiveOptions` · AT-41 |
| ST-45 | ล้างค่าที่ดึงไว้เมื่อปิดงวด | FN-41 | 02_API-23 · AT-42 |
| ST-46 | อ่านประวัติของคนที่พ้นสภาพ | FN-42 | 04_DB snapshot · AT-43 |
| ST-47 | รับอัตราจากคำสั่ง | FN-43 | **02_API-26** · AT-44 · CT-04 |
| ST-48 | Payroll อ่านอัตราพร้อมเวอร์ชัน | FN-44 | **02_API-24** · §0.13.2 · CT-01 |
| ST-49 | หนังสือรับรอง/Manpower อ่าน snapshot | FN-45 | **02_API-24 · API-25** · CT-02 · CT-03 |
| ST-50 | ทะเบียนการใช้งาน + สถานะเชื่อม | FN-46 | 02_API-21/22 · AT-47 |
| ST-51 | ค้นหาในทุกรายการ | FN-90 | 01_UI ทุก list · AT-56 |
| ST-52 | ไม่มีปุ่มลบถาวร | FN-91 | 02_API (ไม่มี DELETE) · AT-57 |
| ST-53 | กันการกดบันทึกซ้ำ | FN-92 | 02_API §2.3 Idempotency · AT-58 |
| ST-54 | รูปแบบจำนวนเงินเดียวกัน | FN-94 · FN-50 | 03_LOGIC `formatMoney` · AT-50 |
| ST-55 | พิสูจน์ว่าไม่มีขั้นอนุมัติ | FN-47 · FN-48 | 05_RULES BR-21 · AT-48 |

### §0.12.2 Business Rules (BRD §9) — 24/24

| BR | อยู่ที่ | บังคับใช้ที่ | Test |
|---|---|---|---|
| BR-01 | 05_RULES BR-01 | `assertBandOrder` (03_LOGIC) | AT-06 |
| BR-02 | 05_RULES BR-02 | `assertVersionEditable` · `publishBandVersion` | AT-02 · AT-07 |
| BR-03 | 05_RULES BR-03 | `assertNoOverlap` + unique index (04_DB) | AT-08 |
| BR-04 | 05_RULES BR-04 | `assertNotInClosedPeriod` (ตรวจซ้ำตอน commit) | AT-30 |
| BR-05 | 05_RULES BR-05 | ไม่มี DELETE endpoint · trigger กัน UPDATE ประวัติ | AT-27 · AT-57 |
| BR-06 | 05_RULES BR-06 | `computeBandBase` | AT-16 |
| BR-07 | 05_RULES BR-07 | ENG-SALBAND-01 | AT-22 |
| BR-08 | 05_RULES BR-08 | `evaluateOutOfRange` | AT-23 · AT-24 |
| BR-09 | 05_RULES BR-09 | `computeFteAdjustedBase` | AT-25 |
| BR-10 | 05_RULES BR-10 | `assertCompRecordComplete` | AT-20 |
| BR-11 | 05_RULES BR-11 | `closePreviousCompRecord` + exclusion constraint | AT-21 · AT-27 |
| BR-12 | 05_RULES BR-12 | `detectComponentCycle` | AT-17 |
| BR-13 | 05_RULES BR-13 | schema (ไม่มี field ภาษี) + review checklist | AT-15 · AT-49 |
| BR-14 | 05_RULES BR-14 | ENG-RECUR-01 | AT-33 |
| BR-15 | 05_RULES BR-15 | `assertNoOverlap` (recurring) | AT-34 |
| BR-16 | 05_RULES §5.7 D7/D-CLASS | `maskMoney` · `logRestrictedView` · ENG-MASK-01 | AT-36 · AT-37 |
| BR-17 | 05_RULES BR-17 | `resolveHrConfig` (ส่ง date เสมอ · เก็บ version_id) | AT-39 · AT-42 |
| BR-18 | 05_RULES BR-18 | `filterActiveOptions` | AT-41 |
| BR-19 | 05_RULES BR-19 | schema soft ref + snapshot (ไม่มี FK ข้าม feature) | AT-43 |
| BR-20 | 05_RULES BR-20 | `buildRateSnapshot` (คืน `version_id` เสมอ) | CT-01 |
| BR-21 | 05_RULES BR-21 | ไม่มี endpoint/สถานะอนุมัติทั้งแพ็ก | AT-48 |
| BR-22 | 05_RULES BR-22 | `countWhereUsed` · `registerWhereUsed` | AT-10 · AT-47 |
| BR-23 | 05_RULES BR-23 | `resolveLegalMinimum` · `evaluateBelowLegalMin` | AT-52 · AT-53 |
| BR-24 | 05_RULES BR-24 | `assertChangeReasonCode` + config table | AT-55 |

### §0.12.3 Edge Cases (BRD §10) — ☑ ยืนยันแล้ว 15/15 · ☐ AI-suggested 17/17

| EC | อยู่ที่ | หมายเหตุ |
|---|---|---|
| EC-01…EC-15 (☑) | `05_RULES §5.5` EC-01…EC-15 | implement ใน Phase 1 ทั้งหมด |
| EC-16 ⚠️ | `05_RULES §5.5` EC-16 + `02_API §2.3 Optimistic Locking` | `[AI-DEFAULT]` OQ-BRD-03 |
| EC-17, EC-18 | `05_RULES §5.5` | ☐ รอ BA confirm |
| EC-19 ⚠️ | `05_RULES §5.5` + Error `ERR_HRCFG_UNAVAILABLE` | OQ-FRD-06 |
| EC-20 ⚠️ | `05_RULES §5.5` + `02_API-23` | OQ-BRD-04 |
| EC-21, EC-22 | `05_RULES §5.5` | ☐ |
| EC-23, EC-24 | `05_RULES §5.5` | ☐ |
| EC-25 ⚠️ | `05_RULES §5.5` + `04_DB accrued_amount` (read-only) | OQ-SS-02 |
| EC-26 ⚠️ | `05_RULES §5.7 D7` (ABAC) | OQ-BRD-05 |
| EC-27 | `05_RULES §5.5` + CSQ_BRIEF OQ-CSQ-01 | ☐ |
| EC-28 | `05_RULES §5.7 D2` | ☐ |
| EC-29…EC-32 | `05_RULES §5.5` + `06_TESTS §6.9` cross-module | ☐ |

### §0.12.3b Functions Cut — FN ที่ประกาศว่า "ไม่รองรับ" (15/15 · อยู่ในแมนิเฟสต์ ไม่หายเงียบ)

| NS | สิ่งที่ไม่รองรับ | FN ที่พิสูจน์ | อยู่ที่ | OQ |
|---|---|---|---|---|
| NS-01 | approval ในตัว feature | FN-47 | 05_RULES BR-21 · 07_LOCKED §7.3 | OQ-STD-01 |
| NS-02 | ปรับค่าจ้างหมู่ | FN-48 | 01_UI P-05 SEC · 07_LOCKED §7.3 | OQ-STD-04 |
| NS-03 | หลายสกุลเงิน | FN-50 | 04_DB `currency` (คงที่ THB) | OQ-STD-02 |
| NS-04 | retro recalculation | FN-51 | 05_RULES BR-04 · P-9 | OQ-STD-05 |
| NS-05 | geo zone | FN-52 | 04_DB (ไม่มีคอลัมน์) | OQ-STD-07 |
| NS-06 | mass import/export | FN-53 | 02_API (ไม่มี endpoint) | OQ-STD-10 |
| NS-07 | คำนวณภาษี/ปกส./ยอดสุทธิ | FN-49 | 04_DB (ไม่มี field) · 05_RULES BR-13 | มติ scope note |
| NS-08 | merit worksheet | FN-54 | 01_UI P-05 SEC | มติ กติกา 1 |
| NS-09 | eligibility ตามประเภทจ้าง | FN-55 | 04_DB `job_family` = label | OQ-STD-06 |
| NS-10 | variable pay / โบนัส | FN-59 | 04_DB (ไม่มี field) | OQ-STD-12 |
| NS-11 | step ในระดับ | FN-60 | 04_DB (ไม่มีคอลัมน์) | OQ-STD-13 |
| NS-12 | เก็บตัวเลขค่าแรงขั้นต่ำเอง | FN-56 | 03_LOGIC `resolveLegalMinimum` (อ่านอย่างเดียว) | OQ-STD-11 |
| NS-13 | หน้าตั้งค่า HR | FN-39 | 01_UI (ลิงก์ออกเท่านั้น) | มติ #107 |
| NS-14 | แจ้งเตือนพนักงาน | — | `NOT_NEEDED.md` (NTF) | OQ-STD-08 |
| NS-15 | เลขที่เอกสาร / PDF | — | `NOT_NEEDED.md` (DOCCFG · PDFDOC) · **ไม่มี PRINT_SPEC** | มติ scope note |

### §0.12.4 สรุป Coverage

| หมวด | จาก BRD | มีที่ลงในแพ็ก | หล่น |
|---|---|---|---|
| Stories | 55 | 55 | **0** |
| Functions (FN) | 65 | 65 | **0** |
| Business Rules | 24 | 24 | **0** |
| Scenarios | 47 | 47 (ผ่าน FN/Story/§14.6) | **0** |
| Edge Cases ☑ | 15 | 15 | **0** |
| Edge Cases ☐ | 17 | 17 | **0** |
| Functions Cut | 15 | 15 | **0** |
| Open Questions | 24 (BRD) + 6 (FRD) | 30 → `07_LOCKED §7.3` | **0** |

---

## §0.13 ⭐ Published Rate Surface — สิ่งที่ feature อื่นอ่านได้จากที่นี่

> **ส่วนนี้เขียนไว้ให้ทีมของ Payroll (W4) · Manpower Planning (W6) · หนังสือรับรอง (W3) · Employee Movement (W3) อ้างอิงโดยตรง** — ยกไปวางใน `00_OVERVIEW §Dependencies` ของ feature ตัวเองได้ทันที
> **กติกาเหล็ก:** consumer **อ่าน** อัตราจากที่นี่ · **ห้ามเก็บตัวเลขค่าจ้างถาวรในตารางของตัวเองโดยไม่มี `version_id`** · **ห้ามเขียนกลับ** ยกเว้น Employee Movement ผ่านทางเข้าเดียวที่ §0.13.5 · **ห้ามคำนวณ compa-ratio เอง** (เรียกค่าที่คืนมา)

### §0.13.1 อะไรบ้างที่เผยแพร่ (3 มุมมอง)

| มุมมอง | เนื้อหา | ผู้ใช้หลัก | endpoint |
|---|---|---|---|
| **`rate`** (อัตรารายคน) | เงินเดือนฐาน · FTE · ระดับ · องค์ประกอบที่ผูก · รายการประจำที่ยังมีผล · ตำแหน่งในกระบอก · `version_id` | Payroll · หนังสือรับรอง · Employee Movement · ESS (ผ่านต้นทาง) | `GET /api/v1/salary-structure/resolve` |
| **`band`** (กระบอกต่อระดับ) | min · mid · max ต่อระดับ ณ วันที่ + ขอบเขตบริษัท + `version_id` · จำนวนคนต่อระดับ (ไม่ระบุตัวบุคคล) | Manpower Planning · Employee Movement | `GET /api/v1/salary-structure/bands/resolve` |
| **`component`** (ทะเบียนองค์ประกอบ) | รหัส · ชื่อ · รายได้/รายหัก · วิธีคิด · `payroll_code` · แฟล็ก `is_ot_base` / `is_ssf_base` / `prorate_by_payment_days` / `include_in_band_base` | Payroll | รวมอยู่ในผลของ `resolve` + `GET /components` |

**สิ่งที่ไม่เผยแพร่:** ร่าง (`ร่าง`) · เวอร์ชันที่ยังไม่ถึงวันมีผล (`รอมีผล`) · เรคคอร์ดที่ `ถอนแล้ว` — ดู **P-6′** ใน §0.14

### §0.13.2 หน้าทางเข้าเดียวของอัตรารายคน — `GET /api/v1/salary-structure/resolve`

```
GET /api/v1/salary-structure/resolve
    ?date=2026-09-30            ← บังคับเสมอ (ไม่ส่ง = 400 ERR_RESOLVE_DATE_REQUIRED)
    &company_id=<uuid>          ← บังคับเมื่อ tenant มีบริษัทลูก
    &employee_id=<uuid>         ← เจาะรายคน (ใช้คู่กับ scope=employee)
    &scope=employee|company     ← default employee · company = อ่านทั้งบริษัทเป็นชุด (Payroll · OQ-FRD-01)
    &include=components,recurring,band_position   ← optional (default ทั้งหมด)
    &page=1&page_size=500       ← เมื่อ scope=company
```

**สิ่งที่คืนกลับ (rate snapshot) — โครงที่ consumer ยกไปใช้ได้เลย:**

| field | ชนิด | ความหมาย | Classification |
|---|---|---|---|
| `as_of` | date | วันที่ที่ใช้ตัดสิน (สะท้อน `date` ที่ส่งมา) | Internal |
| `employee_id` · `employee_name_snapshot` | uuid · text | คนที่อัตรานี้เป็นของ | PII |
| `grade_code` · `grade_name` | text | ระดับ ณ วันนั้น | Internal |
| `base_amount` | money \| `null` | **เงินเดือนฐาน** — `null` เมื่อ `masked = true` | **RESTRICTED** |
| `fte` | decimal(3,2) | สัดส่วนเวลาทำงาน | Confidential |
| `currency` | enum | `THB` (สกุลเดียวรอบนี้) | Internal |
| `effective_date` · `effective_to` | date | ช่วงที่อัตรานี้มีผล (`effective_to = null` = ยังมีผลอยู่) | Internal |
| `record_id` · `record_status` | uuid · enum | เรคคอร์ดอัตราที่ถูกเลือก (`ปัจจุบัน` เท่านั้น) | Internal |
| `change_reason_code` · `movement_doc_no` | enum · text \| `null` | ที่มาของอัตรานี้ | Confidential |
| `components[]` | array | องค์ประกอบที่ผูก: `component_code` · `payroll_code` · `direction` · `calc_type` · `amount`/`percent` (RESTRICTED) · `include_in_band_base` · `is_ot_base` · `is_ssf_base` · `prorate_by_payment_days` | mixed |
| `recurring[]` | array | รายการประจำที่ **มีผล ณ `as_of`**: `item_id` · `component_code` · `direction` · `amount`/`percent` (RESTRICTED) · `effective_from` · `effective_to` · `goal_amount` · `accrued_amount` | **RESTRICTED** |
| `band_position` | object \| `null` | `min` · `mid` · `max` · `compa_ratio` · `range_penetration` · `out_of_range_flag` · `fte_adjusted_base` — `null` เมื่อไม่มีกระบอกของระดับนั้น ณ วันที่ | **RESTRICTED** (เมื่อผูกกับบุคคล) |
| `total_fixed_monthly` | money \| `null` | ยอดค่าจ้างประจำต่อเดือน — **ไม่ใช่ยอดจ่ายสุทธิ** | **RESTRICTED** |
| `masked` | bool | `true` = ผู้เรียกไม่มีสิทธิ์เห็นตัวเลข → ทุก field ที่เป็นเงินเป็น `null` | — |
| **`version_id`** | object | **`{ band: <uuid|null>, hr_config: { period_rule: <uuid>, legal_minimum: <uuid|null> } }`** — เวอร์ชันทั้งหมดที่ใช้ตัดสินคำตอบนี้ | Internal |
| `source_feature` | const | `F-HR-SALSTRUCT` | Internal |

**กรณีไม่มีข้อมูล:** ถ้าพนักงานยังไม่มีอัตรา ณ วันนั้น → คืน `200` พร้อม `rate: null` + `reason: "NO_RATE_AT_DATE"` — **ห้ามคืนค่าอัตราของวันใกล้เคียง** (EC-31)

### §0.13.3 มุมมองกระบอก — `GET /api/v1/salary-structure/bands/resolve`

```
GET /api/v1/salary-structure/bands/resolve?date=2027-01-01&company_id=<uuid>[&grade_code=P3]
```
คืนต่อระดับ: `grade_code` · `grade_name` · `level_order` · `min_amount` · `mid_amount` · `max_amount` · `currency` · `effective_date` · `effective_to` · `version_id` · `headcount` (จำนวนคนที่อ้างระดับนั้น ณ วันที่ — **ไม่ระบุตัวบุคคล ไม่ต้องมีสิทธิ์ RESTRICTED**)
> **Manpower Planning ใช้ `mid_amount` เป็นฐานงบอัตรากำลัง** — ห้ามใช้ค่าเฉลี่ยของอัตราจริงแทน เพราะนั่นเป็นข้อมูล RESTRICTED

### §0.13.4 กติกา 7 ข้อที่ consumer ทุกตัวต้องทำตาม (`SS-1…SS-7`)

| # | กติกา | ทำไม |
|---|---|---|
| **SS-1** | **ส่ง `date` เสมอ** — วันที่ของเหตุการณ์ทางธุรกิจ (วันจ่ายของงวด · วันออกหนังสือ · วันมีผลของคำสั่ง) ไม่ใช่ "วันนี้" เสมอไป | นโยบายกับอัตราเปลี่ยนตามเวลา — ถามโดยไม่ระบุวันคือคำถามที่ไม่มีคำตอบเดียว (P-5) |
| **SS-2** | **เก็บ `version_id` ทั้งก้อนคู่กับเอกสารที่สร้าง** (งวดจ่าย · หนังสือรับรอง · คำสั่ง) | ตอบข้อพิพาทย้อนหลัง · เอกสารเก่าไม่เปลี่ยนค่าเมื่อโครงเปลี่ยน (C-2 ของ HR Config ตระกูลเดียวกัน) |
| **SS-3** | **ห้าม cache ข้ามวัน** — cache ได้ภายในวันเดียว · ต้องล้างเมื่อได้ event `salstruct.effective` · `salcomp.assigned` · `salcomp.ended` · `salrecur.started` · `salrecur.ended` | สถานะเปลี่ยนตอนเที่ยงคืนตามวันมีผล |
| **SS-4** | **ห้าม CRUD ข้อมูลของ feature นี้** — ไม่มี endpoint เขียนสำหรับ consumer ยกเว้น §0.13.5 · ใช้ลิงก์ "จัดการที่โครงเงินเดือน" → `#/salary-structure/<tab>` | LD-4C-02 · #107 |
| **SS-5** | **ค่าที่ `masked = true` ห้ามหาทางอ้อมเพื่อให้ได้ตัวเลข** — ถ้า service ปลายทางต้องใช้ตัวเลขจริง ต้องเรียกด้วยสิทธิ์ service ที่ Policy Center อนุมัติแล้ว | RESTRICTED · S02-04 · S06-01 |
| **SS-6** | **ห้ามคำนวณ compa-ratio / range penetration / ฐานเทียบเต็มเวลา เอง** — ใช้ `band_position` ที่คืนมา | นิยามฐานเทียบเป็นค่าที่ตั้งได้ (BR-06) — คำนวณเองแล้วจะเพี้ยนเมื่อค่าเปลี่ยน |
| **SS-7** | **ลงทะเบียนตัวเองใน where-used** — `POST /api/v1/salary-structure/usage` (หรือแจ้ง BA ให้ตั้ง Module Linkage) เมื่อ feature พร้อมใช้ | HR Comp Admin ต้องเห็นผลกระทบก่อนปิดใช้ระดับ/องค์ประกอบ (BR-22 · ตระกูลเดียวกับ C-6) |

### §0.13.5 ทางเข้าเดียวสำหรับการเขียนกลับ (เฉพาะ Employee Movement)

```
POST /api/v1/salary-structure/rates/from-movement
Headers: Idempotency-Key: <movement_doc_no>
Body: { employee_id, grade_code, base_amount, fte, effective_date,
        change_reason_code, change_reason, movement_doc_no, approved_by }
```
- **สร้างเรคคอร์ดสถานะ `รอมีผล` เท่านั้น** — feature นี้ **ไม่อนุมัติซ้ำ** (คำสั่งถูกอนุมัติมาแล้วที่ต้นทาง · BR-21)
- **idempotent ตาม `movement_doc_no`** — ส่งซ้ำไม่สร้างซ้ำ (EC-30)
- ถ้าชนงวดที่ปิด → `422 ERR_EFFECTIVE_IN_CLOSED_PERIOD` พร้อม `earliest_open_date` — **ไม่สร้างเรคคอร์ดค้าง** (EC-29)
- ถ้าคำสั่งถูกยกเลิกที่ต้นทาง → เรียก `POST /rates/{id}/withdraw` พร้อมเหตุผล (S-20)

### §0.13.6 event ที่ consumer ฟังได้ (10 event · ท่อ EC · SecC)

| event | เมื่อไร | consumer ควรทำอะไร |
|---|---|---|
| `salstruct.published` | เวอร์ชันกระบอกถูกประกาศพร้อมวันมีผล | เตรียมตัว — **ยังไม่เปลี่ยนพฤติกรรม** |
| `salstruct.effective` | เวอร์ชันเริ่มมีผลจริง | **ล้าง cache** · Manpower คำนวณงบใหม่ตั้งแต่วันมีผล |
| `salstruct.cancelled` | เวอร์ชันที่รอมีผลถูกถอน | ยกเลิกการเตรียมตัว |
| `salstruct.deactivated` | ระดับ/องค์ประกอบถูกปิดใช้ | ซ่อนจากตัวเลือกใหม่ · **ห้ามลบข้อมูลเก่าที่อ้างอยู่** |
| `salcomp.assigned` | อัตราของพนักงานเริ่มมีผล | ล้าง cache ของคนนั้น · Payroll ใช้อัตราใหม่ตั้งแต่งวดที่ครอบวันมีผล |
| `salcomp.cancelled` | อัตราที่รอมีผลถูกถอน | ยกเลิกการเตรียมตัวของคนนั้น |
| `salcomp.ended` | พนักงานพ้นสภาพ → ปิดช่วงอัตรา | Payroll คิดงวดสุดท้ายถึงวันสุดท้าย |
| `salrecur.started` | รายการประจำเริ่มมีผล | Payroll เพิ่มรายการเข้ารอบถัดไป |
| `salrecur.ended` | รายการประจำสิ้นสุด (ครบเป้า/ถึงวัน/ถอน) | Payroll **หยุดหัก** |
| `salcomp.viewed_restricted` | มีการเปิดดูตัวเลขที่ปกติถูกปิดบัง | (ปกติ consumer ไม่ต้องทำอะไร — ใช้เชิงกำกับดูแล · ดู OQ-CSQ-01) |

> event ทั้ง 10 ตัว = ท่อ **EC + SecC** ของ ENG-CSQ 7C เท่านั้น — ประกาศไว้ที่ `5_DECLARATIONS/CSQ_BRIEF.md §2`
> **feature นี้ไม่ประกาศท่อ NTF** — การแจ้งเตือนพนักงานเป็นหน้าที่ของ Employee Movement กับ Payroll (OQ-STD-08)
> **ท่อต้องห้าม:** OC · DC ระดับเอกสาร · SC — ห้ามประกาศ (register 422)

---

## §0.14 ⭐ Effective-Dated Rate Contract — invariant ที่ห้ามผิด

> **สืบทอดตรงจาก HR Configuration `00_OVERVIEW §0.14` (P-1…P-9)** — feature นี้เป็น consumer ของ P-1…P-9 **และ** เป็นผู้บังคับใช้มันซ้ำกับข้อมูลของตัวเอง

### §0.14.1 invariant ของ feature นี้ (P-1′…P-9′ — คู่ขนานกับ P-1…P-9)

| # | ข้อผูกพัน | รูปธรรมในแพ็กนี้ |
|---|---|---|
| **P-1′** | ทุกอัตรา/กระบอก/รายการประจำมี `effective_date` เสมอ | `04_DB` NOT NULL เมื่อ `status ≠ 'draft'` · BR-02 · VR-03 |
| **P-2′** | **ห้ามเขียนทับค่าที่มีผลอยู่** — การแก้ = สร้างเวอร์ชัน/เรคคอร์ดใหม่ | `02_API-03` รับเฉพาะ `ร่าง` · ไม่มี endpoint แก้ `base_amount` ของเรคคอร์ดที่ `ปัจจุบัน`/`ประวัติ` · BR-02 |
| **P-3′** | ทุกช่วงเวลาชัดเจน + ไม่ทับกัน `[effective_date, effective_to]` | exclusion constraint (04_DB) + `assertNoOverlap` + `computeEffectiveWindow` · BR-03 · BR-11 · BR-15 |
| **P-4′** | ประวัติ append-only — ไม่ลบ ไม่แก้ย้อนหลัง | ไม่มี DELETE endpoint ทั้งแพ็ก · trigger ปฏิเสธ UPDATE บนแถวสถานะ `ประวัติ` · BR-05 |
| **P-5′** | **ถามอัตราต้องบอกวันที่เสมอ** — ไม่มีโหมด "ค่าปัจจุบัน" ที่ไม่ระบุวัน | `API-24` บังคับ `date` (ไม่ส่ง = 400) · SS-1 |
| **P-6′** | ร่างกับค่าที่ยังไม่ถึงวันมีผล **ไม่ถูกเผยแพร่** | `buildRateSnapshot` กรองเฉพาะ `ปัจจุบัน` / `ใช้งาน` · BR-11 |
| **P-7′** | **ห้ามตั้งวันมีผลย้อนเข้าไปในงวดที่ปิดแล้ว** (นิยามงวดปิดมาจาก HR Configuration) | `assertNotInClosedPeriod` ตรวจ 2 ครั้ง (ตอน validate + ตอน commit) · BR-04 |
| **P-8′** | **ห้าม hardcode ค่าที่มาจากกฎหมาย** — ค่าแรงขั้นต่ำอยู่ที่ HR Configuration | `resolveLegalMinimum` เท่านั้น · ไม่มีคอลัมน์/ค่าคงที่เก็บตัวเลขขั้นต่ำในแพ็กนี้ · BR-23 |
| **P-9′** | **ไม่มี retro** — ต้องแก้ผลย้อนหลัง = สร้างเรคคอร์ดใหม่ที่มีผลวันข้างหน้า | ไม่มี engine คำนวณย้อนหลัง · UI เสนอวันที่เร็วที่สุดที่ตั้งได้ · FN-51 |

### §0.14.2 กติกาที่ feature นี้ต้องทำตามในฐานะ consumer ของ HR Configuration (C-1…C-6)

| # | กติกา | รูปธรรม |
|---|---|---|
| C-1 | ส่ง `date` เสมอ | `resolveHrConfig(date, companyId, group)` — ไม่มี overload ที่ไม่รับวันที่ |
| C-2 | เก็บ `version_id` คู่กับสิ่งที่สร้าง | `legal_min_version_id` · `period_version_id` ในเรคคอร์ด + `T_ss_cfg_ref` |
| C-3 | ห้าม cache ข้ามวัน | `T_ss_cfg_ref.fetched_at` + `invalidateConfigCache` เมื่อได้ `hrconfig.effective` / `hrconfig.period_closed` |
| C-4 | ห้าม CRUD ของ HR Configuration | ไม่มี client เขียนในแพ็กนี้ · มีเฉพาะลิงก์ `#/hr-config/<tab>` |
| C-5 | ค่าที่ `inactive` เลือกใหม่ไม่ได้ แต่ยังแสดงได้ | `filterActiveOptions` (ตัวเลือก) vs `renderHistoricalValue` (การแสดงผล) |
| C-6 | ลงทะเบียน where-used | `registerWhereUsed` → `POST /hr-config/items/:id/usage` |

---

## §0.15 ⭐ Soft-Reference Read Model (LD-4C-02) — วิธีที่ feature อื่นเชื่อมกับที่นี่

> **หลัก:** ทุกเส้นข้าม feature เป็น **soft reference** — อ่าน/แสดงผลเท่านั้น · nullable · **ไม่มี FK cascade** · ห้าม CRUD ข้ามฝั่ง

### §0.15.1 ทิศทาง "เข้า" — feature นี้อ้างของคนอื่น

| อ้างอะไร | จากไหน | เก็บอย่างไร | ถ้าต้นทางเปลี่ยน/ถูกปิด |
|---|---|---|---|
| พนักงาน (เจ้าของอัตรา · ผู้บันทึก) | Employee Master | `employee_id` + **snapshot ชื่อ ณ เวลาบันทึก** (`employee_name_snapshot`) | ลาออก → ประวัติอัตรายังอ่านได้ + ป้าย "(พ้นสภาพ)" (EC-13) — **ห้าม join แบบ hard** |
| บริษัท (ขอบเขตกระบอก) | Organization | `company_id` + snapshot ชื่อ | บริษัทถูกปิด → ค่าที่อ้างยังอ่านได้ |
| ค่านโยบาย (งวด · อัตรา OT · ค่าขั้นต่ำ) | HR Configuration | **ไม่เก็บค่า** — เก็บเฉพาะ `version_id` ที่ใช้ตัดสิน | ค่าถูก deactivate → ของเดิมแสดงได้ เลือกใหม่ไม่ได้ (C-5) |
| คำสั่งปรับเงินเดือน | Employee Movement | `movement_doc_no` (text · nullable) | คำสั่งถูกยกเลิก → ถอนอัตราที่รอมีผล (ไม่ลบประวัติ) |
| สิทธิ์ / masking | Policy Center | ไม่เก็บ — เรียกตอน runtime | role เปลี่ยน → การมองเห็นเปลี่ยนรอบโหลดถัดไป |

### §0.15.2 ทิศทาง "ออก" — คนอื่นอ้าง feature นี้

| ใครอ้าง | อ้างอะไร | รูปแบบที่ถูกต้อง | รูปแบบที่ **ห้าม** |
|---|---|---|---|
| Payroll · หนังสือรับรอง · ESS(ผ่านต้นทาง) | อัตรา ณ วันที่ | `resolve(date, employee_id)` + เก็บ `version_id` เป็น snapshot ในเอกสารของตัวเอง | ❌ คัดลอก `base_amount` ไปเก็บถาวรโดยไม่มี `version_id` · ❌ อ่านจากตารางของ feature นี้ตรง ๆ · ❌ คำนวณ compa-ratio เอง |
| Manpower Planning | mid-point + headcount ต่อระดับ | `bands/resolve(date, company_id)` | ❌ ใช้ค่าเฉลี่ยอัตราจริง (RESTRICTED) แทน mid-point |
| Employee Movement | อัตราปัจจุบัน (อ่าน) · อัตราใหม่ (เขียน) | อ่าน §0.13.2 · เขียน §0.13.5 ด้วย `Idempotency-Key` | ❌ เขียนตรงเข้าตาราง · ❌ ขออนุมัติซ้ำที่ feature นี้ |
| ทุก consumer | ลิงก์กลับมาแก้ | ปุ่ม "จัดการที่โครงเงินเดือน" → `#/salary-structure/<tab>` | ❌ เรียก API เขียนอื่นใดนอกจาก §0.13.5 |
| where-used | ลงทะเบียนว่าตัวเองใช้อะไร | `POST /api/v1/salary-structure/usage` + Module Linkage ⏳/✅ | ❌ ให้ feature นี้ไป query ข้อมูลของ consumer เอง |

### §0.15.3 ทำไมต้อง soft — ไม่ใช่ FK จริง

- consumer ทั้ง 4 ตัว **ยังไม่มีอยู่จริง** (⏳ W3/W4/W6) — FK จริงจะทำให้ deploy feature นี้ไม่ได้จนกว่าจะครบ
- ระดับ/องค์ประกอบถูก **ปิดใช้** ได้ แต่ประวัติอัตราที่อ้างอยู่ต้องอ่านได้ตลอดไป — FK cascade จะทำลายหลักฐาน
- ข้อมูลอัตราเป็น **RESTRICTED** — การให้ปลายทาง join ตรงเข้าตารางจะข้ามชั้น masking ทั้งชั้น

> **สรุปสำหรับคนเขียน FRD ของ Payroll · Manpower Planning · หนังสือรับรอง · Employee Movement:**
> ยก **§0.13.2** (endpoint + rate snapshot) + **§0.13.4** (กติกา SS-1…SS-7) + **§0.14.1** (P-1′…P-9′) ไปใส่ใน `00_OVERVIEW §Dependencies` ของ feature ตัวเอง แล้วอ้างกลับมาที่ไฟล์นี้ — **ห้ามเขียนกติกาใหม่เอง**
