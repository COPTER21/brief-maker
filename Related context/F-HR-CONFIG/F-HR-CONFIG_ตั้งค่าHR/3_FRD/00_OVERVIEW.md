# 00_OVERVIEW — F-HR-CONFIG · HR Configuration (ตั้งค่าHR)

> **Audience:** ทุก role (PM, BA, FE, BE, QA, DBA, Architect) — **และทีมของอีก 18 feature HR ที่ต้องต่อกับ feature นี้**
> **Purpose:** Document Control + Scope + Roles + Dependencies + **สัญญาที่ feature อื่นต้องอ่าน (§0.13–§0.15)** + Coverage Manifest

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-HR-CONFIG |
| **Feature Name** | HR Configuration — ตั้งค่าHR |
| **Feature Code** | F-HR-CONFIG |
| **Module / Wave / Lane** | HR · W1 · Lane A |
| **Archetype** | master/config (A+B+C) |
| **Variant** | **FULL** (9 files + INDEX) |
| **Status** | DRAFT (พร้อม IN-REVIEW) |
| **FRD Version** | 1.0 (2026-08-28) |
| **Generator** | `frd-generator-v6` v6.1 — **Lane Mode v2 (no-ask)** · Design Authority · HTML-first |
| **Source BRD** | `2_BRD/BRD_ตั้งค่าHR.md` — status **APPROVED** (2026-08-28 · AI Review 27/28 pass · 0 fail) |
| **Source HTML** | `1_HTML/ตั้งค่าHR.html` (3,498 บรรทัด · 206,864 bytes · sha256 `426bc21d…`) — ผ่าน S3a audit FAIL=0 · S3b UX 🟢 BLOCK=0 · S3c COVERAGE_R1 🟢 FN 53/53 |
| **Source Brief (lane)** | `PREBRIEF.md` v1.1 · `FUNCTION_CHECKLIST.md` (53 FN) · `STANDARD_BASELINE.md` · `LANE_BRIEF.md` · `5_DECLARATIONS/{CSQ_BRIEF, NOT_NEEDED}.md` |
| **Author** | BA (feature-lane-runner v2.3 · S5) |
| **Reviewers** | Tech Lead · Architect · QA Lead · Strike (OQ owner) |

**Variant decision (fallback จาก BRD — ไม่มี Brief §3.4):**
`pages = 10` (BRD §14.6) · `states = 5` (BRD §8 — Draft/Scheduled/Active/Superseded/Inactive) · `approval = NO` · `money = NO`
→ **`states ≥ 4` → FULL** · Log: "Variant = FULL (fallback from BRD: pages=10, states=5, approval=N)"

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-08-28 | BA (lane S5) | Initial FRD generation — FULL pack จาก BRD v1.0 APPROVED + HTML ที่ผ่าน gate |

---

## §0.3 Scope

### In Scope
- ศูนย์ตั้งค่านโยบาย HR **6 กลุ่มค่า** — ประเภทการลา · อัตรา OT/กะมาตรฐาน · ปฏิทินวันหยุด · รอบตัดเวลา/รอบจ่าย · รอบประเมิน · ขอบเขตบริษัท
- **โครงข้อมูล 2 ชั้น** `T_hr_config_item` + `T_hr_config_version` — ทุกค่ามี `effective_date` + ประวัติเวอร์ชันเต็ม (**HR-1**)
- **State machine 5 states** ของเวอร์ชันค่า + lifecycle ย่อยของงวด (เปิด/ปิด)
- **สัญญาการอ่านค่าให้ 8 feature ปลายทาง** — `GET /hr-config/resolve` (ดู §0.13)
- **where-used** (soft reference registry) + Module Linkage สำหรับ consumer ที่ยัง ⏳
- **สร้างงวดจริงทั้งปี + ปิด/เปิดงวด** — นิยามของ "งวดที่ปิดแล้ว" ที่ BR-04 ใช้บล็อกการตั้งวันย้อนหลัง
- ประกาศ **ท่อ CSQ (SecC)** 6 event ให้ ENG-CSQ 7C

### Out of Scope
- **approval workflow ตอนแก้ค่านโยบาย** — scope note ตัด · คุมด้วย `effective_date` + audit แทน — reason: OQ-STD-01
- **retro / คำนวณย้อนหลัง** — บล็อกการตั้งวันย้อนหลังแทน — reason: OQ-STD-04 (engine candidate `hr-policy-retro-engine` · ยังไม่สร้าง)
- **สูตรคำนวณเงินเดือน / earning code mapping** — reason: เป็นของ Salary Structure (W1/B) + Payroll (W4) · ที่นี่เก็บแค่ `payroll_code` (OQ-STD-03)
- **leave balance รายคน** — reason: Leave (W2) เป็นเจ้าของ balance (OQ-HR-02)
- **UI สลับบริษัท (company switcher)** — reason: มี field company แล้วแต่ยังไม่ทำหน้าสลับ (OQ-HR-05)
- **auto-import วันหยุดราชการ · import/export config เป็นชุด · Time Profile · probation/notice period · calculation frequency** — reason: ดู BRD §14.6.3 (NS-01…NS-14 · 14 รายการ)
- **eligibility นอกเหนือระดับบริษัท** — reason: OQ-STD-02 (engine candidate `hr-eligibility-rule-engine` · ยังไม่สร้าง)
- **hard delete** — reason: มติ audit append-only — ไม่มี endpoint ลบถาวรใน 02_API แม้แต่ตัวเดียว
- **re-implement baseline engines** (DOA · Document Configuration · ENG-NOTIFY · Roles & Permissions · Audit Trail · ENG-CSQ · Operation Process) — reason: catalog §0 · เรียกใช้เท่านั้น

### Out of Scope (จาก Phase 2.5 probing)
- **PR-5 Bulk/Atomic** — ไม่ activate: ไม่มี import/bulk ในรอบนี้ (NS-08) → ถ้าเปิด OQ ให้กลับมา activate
- **PR-8 Compensation** ระดับ business — ไม่มีการ reverse ค่าเดิม (การถอน = event ใหม่ที่ชี้ version เดิม ตาม BR-CSQ-04) — บันทึกเป็น LD-05

---

## §0.4 Roles & Responsibilities (COSO)

| Role | Person/Team | Responsibilities |
|---|---|---|
| **Maker** | **HR Admin** | สร้าง/แก้ค่าเป็นเวอร์ชันใหม่ · ตั้งวันมีผล · ปิด/เปิดใช้ · ปิด/เปิดงวด |
| **Checker** | **— (ไม่มีชั้นตรวจในรอบนี้)** | ทดแทนด้วย compensating control 5 ข้อ (ดูหมายเหตุด้านล่าง) |
| **Approver** | **— (ไม่มี approval ใน feature นี้)** | OB-07 · scope note ตัด · ประเด็นยกเป็น **OQ-STD-01** ไม่ตัดเงียบ |
| **System** | scheduler + engine | Scheduled→Active เมื่อถึงวัน · Active→Superseded · เขียน audit · ยิง event SecC |
| **Owner** | หัวหน้า HR | เจ้าของนโยบาย — ทบทวนรายเดือนผ่าน Closing Report (BRD §18.4) |
| **Reader** | HR Staff · หัวหน้าสายงาน · 8 feature ปลายทาง | อ่านอย่างเดียว (LD-4C-02) |

> **หมายเหตุ SoD:** ไม่มี approval step → ไม่มีแถวที่ Maker = Approver · **SoD ผ่านโดยไม่มีข้อยกเว้น**
> **Compensating control แทน Approver:** (1) `effective_date` บังคับ ทำให้การเปลี่ยนไม่มีผลทันที (2) เหตุผลบังคับ ≥10 ตัวอักษรตั้งแต่เวอร์ชันที่ 2 (3) audit append-only ทุก transition (4) where-used บังคับดูก่อนปิดใช้ (5) event SecC ทุกครั้งที่สิทธิ์พนักงานเปลี่ยน
> รายละเอียดต่อ workflow → `01_UI.md §1.3 Journey` + `§1.4 COSO Touchpoints`

---

## §0.5 Dependencies

### Upstream (feature นี้ต้องพึ่ง)
| Dependency | Type | Source | สถานะ |
|---|---|---|---|
| **Employee Master** | Data (soft ref · combobox #102) | F-HR-EMP ✅ | เสร็จแล้ว |
| **Organization** | Data (soft ref · รายชื่อบริษัทลูก) | Organization master ✅ | เสร็จแล้ว |
| **Roles & Permissions / Data Masking** | Engine (baseline) | Policy Center ✅ | เรียกใช้ — ห้ามทำเอง |
| **Audit Trail** | Engine (baseline · append-only) | Policy Center ✅ | เรียกใช้ — ห้ามทำเอง |
| **ENG-CSQ 7C** | Engine (baseline) | ENG-CSQ ✅ | รับ event SecC 6 ตัว |
| **Scheduler / job runner** | Infra | platform | ต้องมี — ดู LD-02 (fallback = lazy resolve) |

### Downstream (feature ที่พึ่ง feature นี้)
| Consumer | ใช้อะไร | ผ่านทาง | สถานะ |
|---|---|---|---|
| **Leave** (W2) | ประเภทลา · โควตา/milestone · ยกยอด · prorate · counting rule · เงื่อนไขเอกสาร | `ENG-HRCFG-01 hr-config-resolve` ผ่าน `F-HR-CONFIG-API-13` | ⏳ |
| **OT / Shift** (W2) | อัตรา OT · ฐานคำนวณ · เพดาน ชม./สัปดาห์ · `payroll_code` | เดียวกัน | ⏳ |
| **Shift & Roster** (W2) | กะมาตรฐาน · ปฏิทินวันหยุด (+`location`) | เดียวกัน | ⏳ |
| **Attendance** (W1/C) | ปฏิทินวันหยุด · กะ · วันตัดเวลา · **สถานะงวด** | เดียวกัน + `API-17` | ⏳ |
| **Payroll** (W4) | รอบจ่าย · **งวดจริง** · อัตรา OT · `payroll_code` | เดียวกัน + `API-17` | ⏳ |
| **Performance** (W5) | รอบประเมิน | เดียวกัน | ⏳ |
| **Welfare** (W4) | นโยบายสิทธิ์ที่เกี่ยว | เดียวกัน | ⏳ |
| **Salary Structure** (W1/B) | รอบจ่าย · `payroll_code` | เดียวกัน | ⏳ |

### External
| Service | Purpose |
|---|---|
| ประกาศวันหยุดราชการรายปี (ภายนอก) | รอบนี้ **กรอกมือ** — ไม่มี integration (NS-06) |

---

## §0.6 Stack & Architecture

| Layer | Technology |
|---|---|
| Frontend | React / Next.js / Tailwind (hash routing — 7 routes) |
| API | Node.js / Strapi (REST · `/api/v1/hr-config/*`) |
| Database | PostgreSQL (RLS multi-tenant) |
| Engine layer | CUBIC Registry (`hr-config-resolve`, `hr-period-generator`) |
| Auth | JWT + role-based (Policy Center) |
| Scheduler | job runner รายวัน (พร้อม catch-up) — ดู LD-02 |

---

## §0.7 Multi-Tenant & Security Context

- [x] Multi-tenant feature: **YES** (RLS + `company_scope` ภายใน tenant)
- [x] PII data involved: **YES (ทางอ้อมเท่านั้น)** — feature นี้ไม่เก็บข้อมูลบุคคล แต่มี **การอ้างถึง** พนักงาน 4 ช่อง (`owner_employee_id`, `created_by`, `modified_by`, `closed_by`) → ดู 04_DB §4.2 + §4.6
- [ ] Financial data: **NO** — ไม่มีจำนวนเงินใน feature นี้ (มีแต่ "อัตรา"/"ตัวคูณ" ที่เป็นพารามิเตอร์)
- [x] Audit log required: **YES — append-only บังคับทุก transition** (BR-14)

**Security Bible domains applied:** **D2** (Auth/Session) · **D7** (PII — เฉพาะ field อ้างถึงคน) · **D9** (Audit) · **D15** (Admin Actions) · **D17** (Multi-Tenant) · **D-CLASS** (Data Classification) — ดู `05_RULES.md §5.7`
**Security Preset (จาก BRD §16.1):** **P6 — HR/PII Sensitive (15 controls)**

### §0.7.1 Data Classification Summary

Highest classification level ที่ feature นี้แตะ:
- [ ] Has Restricted fields — **ไม่มี** (ไม่มีเงินเดือน/ข้อมูลอ่อนไหวระดับบุคคลใน feature นี้)
- [x] **Has Confidential fields** — 4 field ที่อ้างถึงพนักงาน (`owner_employee_id`, `created_by`, `modified_by`, `closed_by`) = **Confidential + PII**
- [x] Internal (default ของ field ที่เหลือทั้งหมด — ค่านโยบายเป็น INTERNAL)
- [ ] Public-facing data — **ไม่มี field ใดเป็น Public**

**Linkage:** field Confidential + PII → register ที่ **Policy Center → Data Classification** + อยู่ใน **PDPA consent scope** (ดู 04_DB §4.6.6)
**ไม่มี Restricted field → ไม่ต้อง wire Restricted Resources registry ในรอบนี้** (บันทึกไว้ไม่ให้เข้าใจว่าลืม)

---

## §0.8 Open Questions

> สืบทอดจาก BRD §15 ทั้งชุด + probe ที่ใช้ default ใน Phase 2.5

| ID | Question | Blocking? | Owner | ที่มา |
|---|---|---|---|---|
| OQ-01 | ต้องมี approval ตอนแก้ค่านโยบายไหม | NO (ไม่บล็อก Phase 1) | Strike | BRD Q-01 · OQ-STD-01 |
| OQ-02 | eligibility นอกเหนือ company (ประเภทจ้าง/ระดับ/แผนก) | **YES — บล็อก Phase 3** | Strike / BA | BRD Q-02 · OQ-STD-02 |
| OQ-03 | ผูก OT rate → earning code / payroll element | NO | BA (Salary Structure) | BRD Q-03 · OQ-STD-03 |
| OQ-04 | ต้องคำนวณย้อนหลัง (retro) ไหม | **YES — บล็อก Phase 4** | Strike | BRD Q-04 · OQ-STD-04 |
| OQ-05 | แจ้งเตือนพนักงานจากที่นี่หรือปลายทาง | NO | Chin (ENG-NOTIFY) | BRD Q-05 · OQ-STD-05 |
| OQ-06 | probation / notice period ควรอยู่ที่นี่ไหม | NO | Strike | BRD Q-06 · OQ-STD-06 |
| OQ-07 | Payroll สร้างเองเต็มไหม | NO | Strike | BRD Q-07 · OQ-HR-01 |
| OQ-08 | แหล่งข้อมูลเวลาเข้างาน | NO | Strike | BRD Q-08 · OQ-HR-03 |
| OQ-09 | BR-13 ลำดับ resolve = DYNAMIC/Rule Management จริงไหม 🤖 | **YES — บล็อก Phase 3** | Strike + Architect | BRD Q-09 · C23 escalation |
| OQ-10 | แหล่งอ้างอิงทางกฎหมายของค่าขั้นต่ำ (OT 1.5/1.0/3.0 · ลาพักร้อน 6 วัน) | **YES — บล็อกก่อน go-live** | Strike + กฎหมาย/HR | BRD Q-10 |
| OQ-11 | ปฏิทินแยกตาม `location` ต้องมีรอบนี้ไหม `[AI-DRAFT]` | NO | BA | BRD Q-11 · G-02 |
| OQ-12 | ความถี่รอบบันทึกเวลาแยกจากรอบจ่าย ต้องมีรอบนี้ไหม `[AI-DRAFT]` | NO | BA | BRD Q-12 · G-03 |
| OQ-13 | ปิดงวดชนกับการบันทึกเวอร์ชัน — re-validate ตอน commit? | **YES — บล็อกการปิด FRD** | Architect | BRD Q-13 · **Phase 2.5 PR-1/PR-2 → `[AI-DEFAULT]`** |
| OQ-14 | ยกเลิกเวอร์ชัน Scheduled ที่มีเวอร์ชันซ้อนข้างหลัง | **YES — บล็อกการปิด FRD** | BA + Architect | BRD Q-14 |
| OQ-15 | `resolve()` ถ้าไม่ส่ง "วันที่" — ปฏิเสธหรือ default วันนี้ | **YES — บล็อกการปิด FRD · กระทบ 8 feature** | Architect | BRD Q-15 · **`[AI-DEFAULT]` = ปฏิเสธ 400** |
| OQ-16 | ยืนยัน positioning กับ VS Bible โดยตรง | NO | Architect | BRD Q-16 |
| OQ-17 | ขอ System_Module_Registry | NO | PM / Architect | BRD Q-17 |
| OQ-18 | `hrconfig.period_closed` (E6) ควรเป็น SecC หรือไม่ประกาศ | NO | Architect / Strike | CSQ_BRIEF OQ-CSQ-01 |
| OQ-19 | `profile_id` จริงของ CSQ (`CSQ-HRCFG` เป็น default) | NO | Architect (7C Engine) | CSQ_BRIEF OQ-CSQ-02 |
| OQ-20 | Engine `hr-config-resolve` + `hr-period-generator` register CUBIC รอบนี้หรือ Phase 2 | NO | Architect | LD-03 (ตัดสินแล้ว = Phase 2) |

> Resolved → ย้ายไป `07_LOCKED_DECISIONS.md` เป็น LD-NN

**Phase 2.5 Probing Log (Lane Mode — ห้ามถาม · ใช้ conservative default + `[AI-DEFAULT]`):**

| Probe | Activate? | คำตอบที่ใช้ | ที่มาของคำตอบ | tag |
|---|---|---|---|---|
| **PR-1** Concurrency | ✅ (mutation + state) | Optimistic lock ที่ `version` column + unique `(config_item_id, effective_date, company_scope)` → ชนกัน = 409 | BRD §10.2 EA-01 | — |
| **PR-2** Stale Data | ✅ | `If-Match` = `updated_at` บน PUT · **re-validate BR-04 ตอน commit ไม่ใช่ตอนเปิดฟอร์ม** | BRD EA-02 (🔺) | `[AI-DEFAULT]` → OQ-13 |
| **PR-3** Permission Mid-flight | ✅ | ตรวจ role ที่ mutation time ไม่ใช่ GET time → 403 `ERR_PERMISSION_REVOKED` | BRD EA-15 | — |
| **PR-4** Network Failure | ✅ | Idempotency-Key + retry 3 ครั้ง exponential backoff | conservative default | `[AI-DEFAULT]` |
| **PR-5** Bulk/Atomic | ❌ ไม่ activate | ไม่มี import/bulk รอบนี้ (NS-08) | BRD §3.2 OUT-08 | — |
| **PR-6** Draft/Resume | ✅ (wizard 3 ขั้น) | Draft เก็บได้โดยไม่ต้องมี `effective_date` · resume ได้จาก list | BRD S-03 · FN-06 | — |
| **PR-7** Idempotency | ✅ (mandatory) | `Idempotency-Key` บังคับทุก mutation · cache 24 ชม. · key เดิม+body ต่าง = 409 | conservative default + CSQ_BRIEF §4 | — |
| **PR-8** Compensation | ✅ (cancel/reactivate) | **ไม่ reverse ของเดิม** — ยกเลิก/ปิดใช้ = event ใหม่ที่ชี้ version เดิม (BR-CSQ-04) · re-compute `effective_to` ของเวอร์ชันก่อนหน้า | BRD EA-05 (🔺) | `[AI-DEFAULT]` → OQ-14 |
| **PR-9** Race Condition | ✅ (ปิดงวด vs publish) | ปิดงวดกับ publish ที่กระทบงวดนั้น = serialize ผ่าน row lock ของ `T_hr_pay_period` ตอน commit | BRD EA-02 | `[AI-DEFAULT]` → OQ-13 |

---

## §0.9 Glossary

| Term | Definition |
|---|---|
| **HR-1** | มติ: legal/policy parameter ทุกตัวต้องมี `effective_date` · ห้าม hardcode · ห้ามเขียนทับ |
| **#107** | มติ: feature อื่นห้ามสร้างหน้า config เอง — อ้างมาที่ HR Configuration |
| **LD-4C-02** | มติ soft reference: master = picker assist · nullable · ไม่มี FK cascade · ห้าม CRUD ของ feature อื่น |
| **config item / config version** | โครง 2 ชั้น — ตัวค่า vs เวอร์ชันของค่า |
| **effective window** | ช่วง `[effective_date, effective_to]` ของเวอร์ชันหนึ่ง (`effective_to` = วันมีผลของเวอร์ชันถัดไป − 1 วัน · null = ยังมีผล) |
| **resolve** | การขอค่าพร้อม "วันที่" แล้วได้เวอร์ชันที่ Active ณ วันนั้น — สัญญาหลักกับ 8 feature |
| **งวดที่ปิดแล้ว** | แถวใน `T_hr_pay_period` ที่ `period_status='closed'` — นิยามที่ BR-04 ใช้ |
| **SecC** | ท่อ Security Consequence ของ ENG-CSQ 7C — **ท่อเดียวที่ feature นี้ประกาศได้** |
| **`[ASSUMED]`** | ค่าที่เลนเดาตาม default table (gate-policy) เพราะยังไม่มีคำตอบ |
| **`[AI-DEFAULT]`** | คำตอบ probe ที่ FRD ตอบเองแบบ conservative ใน Lane Mode — รอ BA/Architect ยืนยัน |
| **`[AI-DRAFT]`** | ข้อเสนอที่ AI ร่างจากมาตรฐาน ERP — รอ BA ยืนยันผ่าน wireframe review |

---

## §0.10 Pack Navigation

| File | Audience | Purpose |
|---|---|---|
| `00_OVERVIEW.md` | All + **ทีมของ feature HR อื่น** | ไฟล์นี้ — meta + scope + **สัญญาข้าม feature §0.13–§0.15** + Coverage Manifest |
| `01_UI.md` | FE dev | Layout Decision Log + Pages (7 routes) + Components + Journey |
| `02_API.md` | BE dev (HTTP) | API contracts 17 ตัว + Cross-Module Contract |
| `03_LOGIC.md` | BE dev (logic) | Functions 20 + Engines 2 (+ candidate 2) + Trace Table |
| `04_DB.md` | DBA / BE | 15 tables + Field Dictionary + Classification |
| `05_RULES.md` | BE + QA | BR-01…BR-21 + BR-CSQ-01…05 + Validation + Edge Cases + Errors |
| `06_TESTS.md` | QA | AC + Test Inventory + DoD + Cross-Module cases |
| `07_LOCKED_DECISIONS.md` | All | Scope Lock (§7.0 immutable) + LD-01…LD-08 |
| `INDEX.md` | All | Cross-reference + R8 matrix + Quick Nav |
| `UI_BRIEF_ตั้งค่าHR.md` | FE dev + designer | (S7) สรุปหน้าจอจริง + Drift Log |

> **ไม่มี `PRINT_SPEC.md` ในชุดนี้โดยเจตนา** — feature นี้ไม่มีท่อ `pdfdoc` (`_lane/DECL.json` → `pdfdoc.need=false` · `5_DECLARATIONS/NOT_NEEDED.md`) เพราะไม่มีเอกสารที่คนถือ/ยื่น/พิมพ์ส่ง และไม่มีช่องลายเซ็น · **การไม่มีไฟล์นี้ไม่ใช่ของขาด** (ซ้ำกับ BRD §14.6.4)

---

## §0.11 Scope Lock (pointer)

> FULL variant → Scope Lock ฉบับเต็มอยู่ที่ **`07_LOCKED_DECISIONS.md §7.0` (IMMUTABLE)**
> Scope Lock Ref: `LANE_BRIEF.md` §LOCK (2026-08-28) — มติภายใน CUBE (ไม่ใช่ใบเซ็นลูกค้าภายนอก)
> LOCK ที่ผูก: **HR-1 · #107 · LD-4C-02 · DOA iron rule · Audit append-only · 7C ท่อต้องห้าม · Module Linkage · UI standard**
> **Drift พบระหว่างเขียน FRD (ชั้นที่ 3): ไม่มี**

---

## §0.12 Coverage Manifest ⭐ (R13 — กัน requirement หล่น BRD→FRD · **มีคอลัมน์ FN-XX ตาม Lane Mode v2**)

### §0.12.1 Stories (BRD §7) — 37/37

| BRD Ref | Requirement (ย่อ) | **FN** | อยู่ที่ใน Pack |
|---|---|---|---|
| §7 ST-01 | ตั้งวันมีผลทุกครั้งที่บันทึก | FN-01, FN-02 | 01_UI P-08 · 02_API-06 · 03_LOGIC FN-06 · 05_RULES BR-01 · 06 AT-01 |
| §7 ST-02 | ค่าที่รอมีผลไม่รั่วไปปลายทาง | FN-03, FN-06 | 02_API-13 · 03_LOGIC ENG-HRCFG-01 · 05_RULES BR-19 · 06 AT-02 |
| §7 ST-03 | แก้ค่า Active = เวอร์ชันใหม่ | FN-04, FN-05 | 01_UI P-08 · 02_API-04 · 03_LOGIC FN-03 · 05_RULES BR-02, BR-03 · 06 AT-03 |
| §7 ST-04 | ยกเลิกเวอร์ชันรอมีผล | FN-07 | 02_API-07 · 03_LOGIC FN-07 · 05_RULES BR-20 · 06 AT-04 |
| §7 ST-05 | ย้อนดูกติกา ณ วันที่ | FN-27, FN-28 | 01_UI P-09 · 02_API-01, API-12 · 03_LOGIC FN-01, FN-11 · 06 AT-05 |
| §7 ST-06 | โควตาขั้นตามอายุงาน | FN-08 | 01_UI P-08 · 03_LOGIC FN-05 · 05_RULES BR-16 · 06 AT-06 |
| §7 ST-07 | ยกยอด + วันหมดอายุ | FN-09 | 03_LOGIC FN-05 · 05_RULES BR-12 · 06 AT-07 |
| §7 ST-08 | prorate + ปัดเศษ | FN-10 | 04_DB T_hr_leave_policy · 05_RULES §5.4 · 06 AT-08 |
| §7 ST-09 | กติกาการนับวันลา | FN-29 | 04_DB T_hr_leave_policy · 02_API-13 payload · 06 AT-09 |
| §7 ST-10 | จ่ายบางส่วน + เงื่อนไขเอกสาร | FN-31 | 03_LOGIC FN-05 · 05_RULES VR-10, VR-11 · 06 AT-10 |
| §7 ST-11 | เตือนโควตาต่ำกว่าขั้นต่ำ | FN-32 | 03_LOGIC FN-05 · 05_RULES BR-06 · 06 AT-11 |
| §7 ST-12 | อัตรา OT + เพดาน | FN-11 | 01_UI P-03 · 03_LOGIC FN-05 · 05_RULES BR-05 · 06 AT-12 |
| §7 ST-13 | `payroll_code` เป็นช่องอ้างอิง | FN-12 | 04_DB T_hr_config_item · 05_RULES BR-18 · 06 AT-13 |
| §7 ST-14 | บล็อกอัตรา OT ต่ำกว่ากฎหมาย | FN-13 | 03_LOGIC FN-05 · 05_RULES BR-05 · 06 AT-14 |
| §7 ST-15 | กะมาตรฐาน + ข้ามวัน | FN-14 | 03_LOGIC FN-05, FN-18 · 05_RULES BR-17 · 06 AT-15 |
| §7 ST-16 | ปฏิทินวันหยุดรายปี | FN-15 | 01_UI P-04 · 04_DB T_hr_holiday_day · 06 AT-16 |
| §7 ST-17 | วันหยุดชดเชยอ้างวันต้นทาง | FN-16 | 03_LOGIC FN-05 · 05_RULES VR-18 · 06 AT-17 |
| §7 ST-18 | ชุดปฏิทินตามสถานที่ | FN-49 | 04_DB T_hr_holiday_calendar.location · 06 AT-18 |
| §7 ST-19 | บล็อกวันหยุดซ้ำ | FN-17 | 03_LOGIC FN-05 · 05_RULES BR-09 · 06 AT-19 |
| §7 ST-20 | รอบตัดเวลา + รอบจ่าย | FN-18 | 01_UI P-05 · 03_LOGIC FN-05 · 05_RULES BR-11 · 06 AT-20 |
| §7 ST-21 | สร้างงวดทั้งปี + ปิดงวด | FN-48 | 02_API-14, API-15, API-16 · 03_LOGIC FN-13, FN-14, FN-15, ENG-HRCFG-02 · 05_RULES BR-21 · 06 AT-21 |
| §7 ST-22 | ความถี่รอบบันทึกเวลาแยก | FN-50 | 04_DB T_hr_period_rule.work_period_frequency · 06 AT-22 |
| §7 ST-23 | รอบประเมิน | FN-20 | 01_UI P-06 · 04_DB T_hr_appraisal_cycle · 06 AT-23 |
| §7 ST-24 | บล็อกรอบประเมินทับซ้อน | FN-21 | 03_LOGIC FN-05 · 05_RULES BR-10 · 06 AT-24 |
| §7 ST-25 | ค่ากลาง vs เฉพาะบริษัท | FN-22 | 01_UI P-07 · 05_RULES VR-22 · 06 AT-25 |
| §7 ST-26 | บริษัทลูกทับค่ากลาง | FN-23 | 03_LOGIC ENG-HRCFG-01 · 05_RULES BR-13 · 06 AT-26 |
| §7 ST-27 | `applies_to` เป็น hook | FN-30 | 01_UI P-08 · 04_DB T_hr_config_item.applies_to · 05_RULES VR-30 · 06 AT-27 |
| §7 ST-28 | ปิดใช้โดยไม่ลบถาวร | FN-24, FN-25 | 02_API-09, API-10 · 03_LOGIC FN-09, FN-10 · 05_RULES BR-07 · 06 AT-28 |
| §7 ST-29 | เห็น where-used ก่อนปิดใช้ | FN-26 | 02_API-11 · 03_LOGIC FN-12, FN-09 · 05_RULES BR-08 · 06 AT-29 |
| §7 ST-30 | ดูว่าใครใช้ค่านี้ | FN-33 | 01_UI P-09 tab 3 · 02_API-11 · 03_LOGIC FN-12 · 06 AT-30 |
| §7 ST-31 | บล็อกวันมีผลย้อนเข้างวดปิด | FN-19 | 03_LOGIC FN-20 · 05_RULES BR-04, BR-21 · 06 AT-31 |
| §7 ST-32 | กรองรายการในตาราง | FN-90 | 01_UI P-02…P-07 · 02_API-01 · 03_LOGIC FN-01 · 06 AT-32 |
| §7 ST-33 | ยืนยันทุกครั้งก่อนปิด/ยกเลิก | FN-91 | 01_UI P-10 · 05_RULES §5.4 · 06 AT-33 |
| §7 ST-34 | กันบันทึกซ้ำ | FN-92 | 02_API §2.3 Idempotency · 05_RULES EC-02 · 06 AT-34 |
| §7 ST-35 | audit append-only ทุกการเปลี่ยน | FN-93 | 03_LOGIC FN-17 · 05_RULES BR-14 · 06 AT-35 |
| §7 ST-36 | combobox คนแบบเดียวกันทุกช่อง | FN-94 | 01_UI §1.2 P-08 · 04_DB §4.5 · 06 AT-36 |
| §7 ST-37 | persona อยู่ demo strip | FN-95 | 01_UI §1.0 + §1.2 (demo-strip) · 06 AT-37 |

### §0.12.2 Business Rules (BRD §9) — 21/21

| BRD Ref | Rule (ย่อ) | อยู่ที่ใน Pack |
|---|---|---|
| §9 BR-01 | ทุกเวอร์ชันต้องมี `effective_date` | 05_RULES BR-01 · 03_LOGIC FN-06 · 06 AT-01 |
| §9 BR-02 | ห้ามแก้ทับ Active | 05_RULES BR-02 · 03_LOGIC FN-03 · 06 AT-03 |
| §9 BR-03 | ห้าม effective ซ้ำ/คร่อม | 05_RULES BR-03 · 04_DB unique constraint · 06 AT-38 |
| §9 BR-04 | ห้ามย้อนเข้างวดที่ปิด | 05_RULES BR-04 · 03_LOGIC FN-20 · 06 AT-31 |
| §9 BR-05 | ตัวคูณ OT ≥ ขั้นต่ำกฎหมาย | 05_RULES BR-05 · 04_DB T_hr_legal_minimum · 06 AT-14 |
| §9 BR-06 | เตือนโควตาต่ำกว่าขั้นต่ำ | 05_RULES BR-06 · 06 AT-11 |
| §9 BR-07 | ไม่มี hard delete | 05_RULES BR-07 · 02_API (ไม่มี DELETE endpoint) · 06 AT-28 |
| §9 BR-08 | where-used ก่อนปิดใช้ | 05_RULES BR-08 · 03_LOGIC FN-09 · 06 AT-29 |
| §9 BR-09 | วันหยุดห้ามซ้ำ | 05_RULES BR-09 · 04_DB unique · 06 AT-19 |
| §9 BR-10 | รอบประเมินห้ามทับซ้อน | 05_RULES BR-10 · 06 AT-24 |
| §9 BR-11 | วันตัด ≤ วันจ่าย | 05_RULES BR-11 · 06 AT-20 |
| §9 BR-12 | ยกยอด > 0 ต้องมีวันหมดอายุ | 05_RULES BR-12 · 06 AT-07 |
| §9 BR-13 | resolve บริษัทลูก → ค่ากลาง | 05_RULES BR-13 · 03_LOGIC ENG-HRCFG-01 · 06 AT-26 |
| §9 BR-14 | audit append-only | 05_RULES BR-14 · 03_LOGIC FN-17 · 06 AT-35 |
| §9 BR-15 | field คน = combobox Employee Master | 05_RULES §5.4 · 01_UI §1.2 · 06 AT-36 |
| §9 BR-16 | milestone ต่อเนื่อง | 05_RULES BR-16 · 06 AT-06 |
| §9 BR-17 | กะข้ามวัน + ช่วงพัก | 05_RULES BR-17 · 03_LOGIC FN-18 · 06 AT-15 |
| §9 BR-18 | `payroll_code` soft ref (เตือน) | 05_RULES BR-18 · 06 AT-13 |
| §9 BR-19 | Draft/Scheduled ไม่ส่งปลายทาง | 05_RULES BR-19 · 03_LOGIC ENG-HRCFG-01 · 06 AT-02 |
| §9 BR-20 | ยกเลิกได้ก่อนมีผลเท่านั้น | 05_RULES BR-20 · 03_LOGIC FN-07 · 06 AT-04 |
| §9 BR-21 | งวดที่ปิด = ฐานของ BR-04 | 05_RULES BR-21 · 03_LOGIC FN-14, FN-15 · 06 AT-21 |

### §0.12.3 Edge Cases (BRD §10) — ☑ ยืนยันแล้ว 15/15 · ☐ AI-suggested 17/17

| BRD Ref | Edge (ย่อ) | อยู่ที่ใน Pack |
|---|---|---|
| §10.1 EC-01…EC-15 | edge ที่ยืนยันแล้วทั้ง 15 ข้อ | 05_RULES §5.5 EC-01…EC-15 · 06_TESTS TC ตามตาราง §6.2 |
| §10.2 EA-01 | สร้างเวอร์ชันชนกัน | 05_RULES §5.5 EA-01 · 02_API §2.3 optimistic lock · 06 TC-CC-01 |
| §10.2 EA-02 🔺 | ปิดงวดชนกับการบันทึก | 05_RULES §5.5 EA-02 · 03_LOGIC FN-20 · 06 TC-CC-02 · **OQ-13** |
| §10.2 EA-03 | ปิดใช้ระหว่างมีคนแก้ค้าง | 05_RULES §5.5 EA-03 · 06 TC-CC-03 |
| §10.2 EA-04 | scheduler ขาด → catch-up | 05_RULES §5.5 EA-04 · 03_LOGIC FN-06 · LD-02 · 06 TC-ST-01 |
| §10.2 EA-05 🔺 | ยกเลิกเวอร์ชันซ้อน | 05_RULES §5.5 EA-05 · 03_LOGIC FN-07, FN-19 · 06 TC-ST-02 · **OQ-14** |
| §10.2 EA-06 | เปิดใช้กลับด้วยวันย้อนหลัง | 05_RULES §5.5 EA-06 · 03_LOGIC FN-10, FN-20 · 06 TC-ST-03 |
| §10.2 EA-07 | ปิดใช้ค่าที่มีแต่ Draft | 05_RULES §5.5 EA-07 · 03_LOGIC FN-09 · 06 TC-ST-04 |
| §10.2 EA-08 | กะข้ามวัน + พักคร่อมเที่ยงคืน | 05_RULES §5.5 EA-08 · 03_LOGIC FN-18 · 06 TC-CL-01 |
| §10.2 EA-09 | ปีอธิกสุรทิน | 05_RULES §5.5 EA-09 · 03_LOGIC ENG-HRCFG-02 · 06 TC-CL-02 |
| §10.2 EA-10 | วันตัด/จ่าย = 31 หรือสิ้นเดือน | 05_RULES §5.5 EA-10 · 03_LOGIC ENG-HRCFG-02 · 06 TC-CL-03 |
| §10.2 EA-11 | milestone ขั้นสุดท้าย `year_to = null` | 05_RULES §5.5 EA-11 · 03_LOGIC FN-05 · 06 TC-CL-04 |
| §10.2 EA-12 | บริษัทที่ถูกปิดใช้ที่ Organization | 05_RULES §5.5 EA-12 · 04_DB snapshot column · 06 TC-DI-01 |
| §10.2 EA-13 | พนักงานที่ลาออก | 05_RULES §5.5 EA-13 · 04_DB snapshot column · 06 TC-DI-02 |
| §10.2 EA-14 | ลบวันหยุดต้นทางที่มีวันชดเชยอ้าง | 05_RULES §5.5 EA-14 · 03_LOGIC FN-05 · 06 TC-DI-03 |
| §10.2 EA-15 | เรียก API ตรงโดยข้าม UI | 05_RULES §5.5 EA-15 · 02_API §2.3 · 06 TC-PR-01 |
| §10.2 EA-16 🔺 | `resolve()` ไม่ส่งวันที่ | 05_RULES §5.5 EA-16 · 02_API-13 · 06 TC-XT-09 · **OQ-15** |
| §10.2 EA-17 | ห้าม cache ข้ามวัน | 05_RULES §5.5 EA-17 · 02_API-13 §Caching · 06 TC-XT-10 |

### §0.12.3b Functions Cut — FN ที่ประกาศว่า "ไม่รองรับ" (11/11 · ต้องอยู่ในแมนิเฟสต์ ไม่ใช่หายเงียบ)

| FN | ไม่รองรับอะไร | Scenario | อยู่ที่ใน Pack |
|---|---|---|---|
| **FN-40** | ไม่มีปุ่ม/endpoint ส่งอนุมัติ-อนุมัติ | S-23 | `05_RULES §5.9 NS-01` · `07_LOCKED §7.1 LD-04` · `02_API §2.3` (ไม่มี endpoint approve) · `06 AT-28` (ตรวจว่าไม่มีปุ่ม) |
| **FN-41** | ไม่มีการคำนวณย้อนหลัง | S-24 | `05_RULES §5.9 NS-02` · `03_LOGIC §3.4` (candidate `hr-policy-retro-engine`) · `07_LOCKED §7.4 AT-02` |
| **FN-42** | ไม่มีสูตรเงินเดือน/earning code mapping | S-25 | `05_RULES §5.9 NS-03` · `04_DB` (`payroll_code` เป็น soft ref) · `06 AT-13` |
| **FN-43** | ไม่มียอดวันลาคงเหลือรายคน | S-26 | `05_RULES §5.9 NS-04` · `00_OVERVIEW §0.3 Out of Scope` |
| **FN-44** | ไม่มีตัวสลับบริษัทบนหัวจอ | S-27 | `05_RULES §5.9 NS-05` · `01_UI §1.0` (ไม่มี surface) |
| **FN-45** | ไม่มีการดึงวันหยุดราชการอัตโนมัติ | S-28 | `05_RULES §5.9 NS-06` · `00_OVERVIEW §0.5 External` |
| **FN-46** | ไม่มีการแจ้งเตือนพนักงานจาก feature นี้ | S-29 | `05_RULES §5.9 NS-07` · `01_UI §1.5` (ไม่ประกาศท่อ NTF) |
| **FN-47** | ไม่มี import/export ค่าเป็นชุด | S-30 | `05_RULES §5.9 NS-08` · `02_API §2.3` (ไม่มี bulk endpoint · PR-5 ไม่ activate) |
| **FN-51** | ไม่มีระยะทดลองงาน/ระยะบอกกล่าว | S-33 | `05_RULES §5.9 NS-12` · `00_OVERVIEW §0.3` |
| **FN-52** | ไม่มีความถี่การคำนวณจ่าย (รายสัปดาห์/ปักษ์) | S-34 | `05_RULES §5.9 NS-13` · `04_DB T_hr_period_rule` (มีแค่รอบจ่าย) |
| **FN-53** | ไม่มี Time Profile (มัดชุดค่าให้กลุ่มพนักงาน) | S-35 | `05_RULES §5.9 NS-14` · `03_LOGIC §3.4` (candidate `hr-eligibility-rule-engine`) |

### §0.12.4 สรุป Coverage

| หมวด | ครบ? |
|---|---|
| **Stories (BRD §7)** | **37/37 ✅** |
| **Business Rules (BRD §9)** | **21/21 ✅** |
| **Validation Rules (BRD §9.2)** | **VR-01…VR-30 30/30 ✅** → `05_RULES §5.4` |
| **Edge Cases ยืนยันแล้ว (BRD §10.1)** | **15/15 ✅** |
| **Edge Cases AI-suggested (BRD §10.2)** | **17/17 ✅** (ยกลง 05_RULES พร้อม tag ☐ / 🔺) |
| **FN (FUNCTION_CHECKLIST)** | **53/53 ✅** — in scope 42 อยู่ในตาราง §0.12.1 · **ไม่รองรับ 11 (FN-40…FN-47, FN-51…FN-53)** อยู่ที่ `05_RULES §5.9 Functions Cut` + `07_LOCKED §7.0` |
| **Scenario (PREBRIEF)** | **35/35 ✅** — in scope 24: S-01 (ST-01/10/11) · S-02 (ST-03) · S-03 (ST-02) · S-04 (ST-04) · S-05 (ST-06) · S-06 (ST-07) · S-07 (ST-08) · S-08 (ST-12/13) · S-09 (ST-14) · S-10 (ST-15) · S-11 (ST-16/17) · S-12 (ST-19) · S-13 (ST-20/22) · S-14 (ST-31) · S-15 (ST-23) · S-16 (ST-24) · S-17 (ST-25/26) · S-18 (ST-28) · S-19 (ST-29/30) · S-20 (ST-05) · S-21 (ST-09) · S-22 (ST-27) · S-31 (ST-21) · S-32 (ST-18) · **ไม่รองรับ 11: S-23…S-30, S-33…S-35 → `05_RULES §5.9` (NS-01…NS-14) + §0.12.3b** |
| **CSQ events** | **6/6 ✅** — E1…E6 ตรงกับ `CSQ_BRIEF.md §2` เป๊ะ · **ไม่มี event เกินจาก brief** |
| **ไม่มีที่ลง → OQ** | **ไม่มี** — ทุกแถวมีที่อยู่จริงใน pack |

---

## §0.13 ⭐ Published Config Surface — สิ่งที่ feature อื่นอ่านได้จากที่นี่

> **ส่วนนี้เขียนไว้ให้ทีมของอีก 18 feature HR อ้างอิงโดยตรง** — ยกไปวางใน FRD ของ feature ตัวเองได้ทันที
> **กติกาเหล็ก:** ทุก feature HR **อ่าน** ค่าจากที่นี่ · **ห้ามสร้างหน้า config ของตัวเอง** (#107) · ห้ามคัดลอกค่าไปเก็บถาวรในตารางของตัวเอง (ยกเว้น snapshot ณ เวลาสร้างเอกสาร ซึ่งต้องเก็บ `version_id` คู่มาด้วย)

### §0.13.1 กลุ่มค่าที่เผยแพร่ (5 `group` + 1 มุมมอง)

| `group` (ค่าใน API) | เนื้อหาที่เผยแพร่ | ผู้ใช้หลัก |
|---|---|---|
| `leave_type` | หน่วยนับ · จ่าย/ไม่จ่าย/บางส่วน(%) · โควตาต่อปี · milestone อายุงาน · ความถี่ให้สิทธิ์ · prorate + ปัดเศษ · ยกยอด + วันหมดอายุ · ต้องแนบเอกสาร · ลาล่วงหน้า · ลาต่อเนื่องสูงสุด · ติดลบได้ถึง · นับวันหยุดในช่วงลา · ครึ่งวัน | Leave · Payroll · ESS |
| `ot_rate` | ประเภทอัตรา · ตัวคูณ · ฐานคำนวณ · เพดาน ชม./สัปดาห์ · `payroll_code` | OT/Shift · Payroll · Salary Structure |
| `shift_pattern` | ชื่อกะ · เวลาเข้า–ออก · ข้ามวัน · ช่วงพัก · ชม./วัน (computed) · วันทำงานในสัปดาห์ | Shift & Roster · Attendance |
| `holiday_calendar` | ปี · `location` · รายการวันหยุด (วันที่ · ชื่อ · ประเภท · วันต้นทางกรณีชดเชย · กะที่ได้รับผล) | Attendance · Leave · Shift & Roster · Payroll |
| `period_rule` | ความถี่ · วันตัดเวลา · วันจ่าย · ล็อกงวดที่ปิด · ความถี่รอบบันทึกเวลา · **+ รายการงวดจริง (`pay_period`) พร้อมสถานะ เปิด/ปิด** | Attendance · Payroll · Salary Structure |
| `appraisal_cycle` | ชื่อรอบ · ปี · ช่วงประเมิน · ช่วงเปิดกรอก · ความถี่ | Performance |
| *(มุมมอง)* ขอบเขตบริษัท | ไม่ใช่ group ใหม่ — เป็นคอลัมน์ `company_scope` + `companies[]` ที่ติดมากับทุก item | ทุก consumer |

### §0.13.2 หน้าทางเข้าเดียว — `GET /api/v1/hr-config/resolve`

```
GET /api/v1/hr-config/resolve
    ?date=2026-09-01            ← บังคับเสมอ (ไม่ส่ง = 400 ERR_RESOLVE_DATE_REQUIRED)
    &company_id=<uuid>          ← บังคับเมื่อ tenant มีบริษัทลูก (ใช้ตัดสิน BR-13)
    &group=leave_type           ← optional (ไม่ส่ง = คืนทุกกลุ่ม)
    &code=LV-VAC                ← optional (เจาะค่าเดียว)
```
คืน **เฉพาะเวอร์ชันที่ `status='active'` ณ `date` นั้น** พร้อม `version_id` และ `effective_window`
รายละเอียด schema เต็ม → `02_API.md §2.2 F-HR-CONFIG-API-13` · logic → `03_LOGIC.md §3.2 ENG-HRCFG-01`

### §0.13.3 กติกา 6 ข้อที่ consumer ทุกตัวต้องทำตาม

| # | กติกา | ทำไม |
|---|---|---|
| **C-1** | **ส่ง `date` เสมอ** — วันที่ของ "เหตุการณ์ทางธุรกิจ" ไม่ใช่วันนี้เสมอไป (เช่น ใบลาที่ลาย้อนหลังต้องใช้กติกาของวันที่ลา) | ไม่งั้นคำนวณสิทธิ์ผิดทันทีที่นโยบายเปลี่ยน |
| **C-2** | **เก็บ `version_id` คู่กับเอกสารที่สร้าง** (snapshot) — ใบลา/ใบ OT ต้องรู้ว่าคิดจากเวอร์ชันไหน | ตอบข้อพิพาทย้อนหลังได้ · ป้องกันเอกสารเก่าเปลี่ยนค่าเมื่อนโยบายเปลี่ยน |
| **C-3** | **ห้าม cache ข้ามวัน** — cache ได้ภายในวันเดียวและต้อง invalidate เมื่อได้รับ event `hrconfig.effective` | เวอร์ชันเปลี่ยนสถานะตอนเที่ยงคืน (EA-17) |
| **C-4** | **ห้าม CRUD ข้อมูลของ HR Configuration** — ไม่มี endpoint เขียนสำหรับ consumer · ลิงก์ "จัดการที่ HR Configuration" เท่านั้น | LD-4C-02 · #107 |
| **C-5** | **ค่าที่ `status='inactive'` เลือกใหม่ไม่ได้ แต่ต้องยังแสดงผลได้** สำหรับเอกสารเก่าที่อ้างอยู่ | BR-07 soft archive |
| **C-6** | **ลงทะเบียนตัวเองใน where-used** — เรียก `POST /hr-config/items/:id/usage` (หรือแจ้ง BA ให้ตั้ง Module Linkage) เมื่อ feature พร้อมใช้ | BR-08 · HR Admin ต้องเห็นผลกระทบก่อนปิดใช้ค่า |

### §0.13.4 event ที่ consumer ฟังได้

| event | เมื่อไร | consumer ควรทำอะไร |
|---|---|---|
| `hrconfig.published` | เวอร์ชันใหม่ถูกประกาศพร้อมวันมีผล | เตรียมตัว — **ยังไม่เปลี่ยนพฤติกรรม** (ยังไม่ถึงวันมีผล) |
| `hrconfig.effective` | เวอร์ชันเริ่มมีผลจริง | **invalidate cache** + ใช้ค่าใหม่กับเอกสารที่สร้างตั้งแต่วันนี้ |
| `hrconfig.cancelled` | เวอร์ชันที่รอมีผลถูกถอน | ยกเลิกการเตรียมตัว |
| `hrconfig.deactivated` | ค่าถูกปิดใช้ | ซ่อนจากตัวเลือกใหม่ · **ห้ามลบข้อมูลเก่าที่อ้างอยู่** |
| `hrconfig.reactivated` | ค่าถูกเปิดใช้กลับ | นำกลับเข้าตัวเลือก |
| `hrconfig.period_closed` | งวดถูกปิด | ล็อกการแก้ไขข้อมูลของงวดนั้นที่ฝั่งตัวเอง |

> event ทั้ง 6 ตัว = **ท่อ SecC ของ ENG-CSQ 7C เท่านั้น** — ประกาศไว้ที่ `5_DECLARATIONS/CSQ_BRIEF.md §2`
> **feature นี้ไม่ประกาศท่อ NTF** — การแจ้งเตือนพนักงานเป็นหน้าที่ของ consumer (OQ-STD-05)

---

## §0.14 ⭐ Effective-Dated Parameter Contract (HR-1) — สัญญาที่ห้ามผิด

> **นี่คือ invariant ที่ทำให้ feature นี้มีอยู่** — ทุก feature HR ต้องเข้าใจตรงกัน

| # | ข้อผูกพัน | รูปธรรมใน FRD นี้ |
|---|---|---|
| **P-1** | **ค่านโยบาย/กฎหมายทุกตัวมี `effective_date` เสมอ** — ไม่มีค่าไหนที่ "มีผลทันทีเมื่อบันทึก" ยกเว้นตั้งวันมีผล = วันนี้เอง | `T_hr_config_version.effective_date` NOT NULL เมื่อ `status ≠ 'draft'` · BR-01 · VR-01 |
| **P-2** | **ห้ามเขียนทับค่าที่มีผลอยู่** — การแก้ = สร้างเวอร์ชันใหม่ที่มีวันมีผลของตัวเอง | ไม่มี endpoint แก้ version ที่ `status='active'` (02_API-05 รับเฉพาะ `draft`) · BR-02 |
| **P-3** | **ทุกเวอร์ชันมีช่วงเวลาที่ชัดเจนและไม่ทับกัน** — `[effective_date, effective_to]` ต่อ (item, company_scope) | unique constraint + `FN-19 computeEffectiveWindow` · BR-03 |
| **P-4** | **ประวัติเวอร์ชันเป็น append-only** — ไม่มีการลบ ไม่มีการแก้ย้อนหลัง | ไม่มี DELETE endpoint · BR-07 · BR-14 · audit ที่ Policy Center |
| **P-5** | **ถามค่าต้องบอกวันที่เสมอ** — API ไม่มีโหมด "ค่าปัจจุบัน" ที่ไม่ระบุวัน | `API-13` บังคับ `date` (ไม่ส่ง = 400) · OQ-15 |
| **P-6** | **ค่าที่ยังไม่ถึงวันมีผล (Scheduled) และร่าง (Draft) ไม่ถูกเผยแพร่** | `ENG-HRCFG-01` กรอง `status='active'` เท่านั้น · BR-19 |
| **P-7** | **ห้ามตั้งวันมีผลย้อนเข้าไปในงวดที่ปิดแล้ว** — นิยาม "งวดที่ปิด" = `T_hr_pay_period.period_status='closed'` | `FN-20 assertNotInClosedPeriod` (ตรวจซ้ำตอน commit) · BR-04 + BR-21 |
| **P-8** | **ห้าม hardcode ค่าที่มาจากกฎหมาย** — ขั้นต่ำ OT/โควตาลา อยู่ใน `T_hr_legal_minimum` ที่มี `effective_date` ของตัวเอง | 04_DB `T_hr_legal_minimum` · BR-05 · BR-06 · OQ-10 |
| **P-9** | **ไม่มี retro** — ถ้าต้องแก้ผลย้อนหลัง = สร้างเวอร์ชันใหม่ที่มีผลวันข้างหน้า | OQ-STD-04 · engine candidate `hr-policy-retro-engine` (ยังไม่สร้าง) |

---

## §0.15 ⭐ Soft-Reference Read Model (LD-4C-02) — วิธีที่ feature อื่นเชื่อมกับที่นี่

> **หลัก:** การเชื่อมทุกเส้นเป็น **soft reference** — อ่าน/แสดงผลเท่านั้น · nullable · ไม่มี FK cascade · ห้าม CRUD ข้ามฝั่ง

### §0.15.1 ทิศทาง "เข้า" — feature นี้อ้างของคนอื่น

| อ้างอะไร | จากไหน | เก็บอย่างไร | ถ้าต้นทางเปลี่ยน/ถูกปิด |
|---|---|---|---|
| ผู้รับผิดชอบ / ผู้แก้ไข / ผู้ปิดงวด | Employee Master | เก็บ `employee_id` + **snapshot ชื่อ ณ เวลาบันทึก** (`*_name_snapshot`) | พนักงานลาออก → ยังแสดงชื่อในประวัติได้ (EA-13) — **ห้าม join แบบ hard** |
| บริษัทลูก | Organization | เก็บ `company_id` + snapshot ชื่อ | บริษัทถูกปิดใช้ → ค่าที่อ้างยังอ่านได้ (EA-12) |
| สิทธิ์การเข้าถึง | Policy Center | ไม่เก็บ — เรียกตอน runtime | — |

### §0.15.2 ทิศทาง "ออก" — คนอื่นอ้าง feature นี้

| ใครอ้าง | อ้างอะไร | รูปแบบที่ถูกต้อง | รูปแบบที่ **ห้าม** |
|---|---|---|---|
| 8 consumer | ค่านโยบาย ณ วันที่ | `resolve(date, company_id)` + เก็บ `version_id` เป็น snapshot ในเอกสารของตัวเอง | ❌ คัดลอกค่าไปเก็บถาวรโดยไม่มี `version_id` · ❌ hardcode ค่าไว้ในโค้ดตัวเอง · ❌ สร้างหน้า config ของตัวเอง (#107) |
| 8 consumer | ลิงก์กลับมาแก้ค่า | ปุ่ม/ลิงก์ "จัดการที่ HR Configuration" → `#/hr-config/<tab>` | ❌ เรียก API เขียนของ feature นี้ |
| where-used | ลงทะเบียนว่าตัวเองใช้ค่าอะไร | `T_hr_config_usage` (1 แถวต่อ consumer ต่อ item) + Module Linkage สถานะ ⏳/✅ | ❌ ให้ feature นี้ไป query ข้อมูลของ consumer เอง |

### §0.15.3 ทำไมต้อง soft — ไม่ใช่ FK จริง

- consumer ทั้ง 8 ตัว **ยังไม่มีอยู่จริง** (⏳) — FK จริงจะทำให้ deploy feature นี้ไม่ได้จนกว่าจะครบ
- ค่านโยบายถูก **ปิดใช้** ได้ แต่เอกสารเก่าที่อ้างอยู่ต้องอ่านได้ตลอดไป — FK cascade จะทำลายหลักฐาน
- แต่ละ feature deploy คนละ wave — hard coupling = ปล่อยของไม่ได้

> **สรุปสำหรับคนเขียน FRD ของ feature HR ตัวอื่น:** ยก §0.13.2 (endpoint) + §0.13.3 (กติกา C-1…C-6) + §0.14 (P-1…P-9) ไปใส่ใน `00_OVERVIEW §Dependencies` ของ feature ตัวเอง แล้วอ้างกลับมาที่ไฟล์นี้ — **ห้ามเขียนกติกาใหม่เอง**
