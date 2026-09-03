# 00_OVERVIEW — F-HR-TRAIN · Training (การฝึกอบรมและพัฒนาบุคลากร)

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Open Questions + Coverage Manifest

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-HR-TRAIN |
| **Feature Name** | Training / อบรม (การฝึกอบรมและพัฒนาบุคลากร) |
| **Feature Code** | F133 |
| **Module** | Human Capital → Learning & Development |
| **Archetype** | master (แคตตาล็อกหลักสูตร + การลงทะเบียน — ไม่ใช่ Pattern Q เอกสาร) |
| **Variant** | **FULL** (9 files + INDEX) |
| **Status** | DRAFT (for BA/SEC review) |
| **FRD Version** | 1.0 (2026-09-03) |
| **Generator** | frd-generator-v6 (v6.1 HTML-first) |
| **Source Brief** | — (WF-01 lane · no CODE brief · variant fallback จาก BRD) |
| **Source BRD** | BRD_อบรม.md (status: **APPROVED**, 2026-09-03) |
| **Source HTML** | อบรม.html (source of truth · 12 จอ · route `#/train/<tab>` · audit FAIL=0 · qc-ux BLOCK=0 · coverage FN 18/18) |
| **Author** | BA — ทีม Human Capital (2BSimple) |
| **Reviewers** | Tech Lead · PM · SEC · QA Lead · Finance (มุม EC) |

**Variant decision (fallback from BRD):** FULL — pages=12 (§14.6) · states: Enrollment=5 (≥4) · approval=YES (DOA) · money=YES (งบ/EC/ต้นทุนต่อหัว) · §9.5 มี Engine Management (Rate Card R17, DOA R14). เข้าเงื่อนไข `states ≥ 4 OR (approval AND money) OR Engine Management → FULL`.

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-09-03 | BA Human Capital | Initial FRD (FULL) · HTML-first · สะท้อน scope หลัง 7 FIX (FIX-01..07) |

---

## §0.3 Scope

### In Scope
1. แคตตาล็อกหลักสูตร (Course): สร้าง/แก้ไข/เผยแพร่/ปิด · has_cost + งบ · หมวดอ่านจาก HR Config (FN-01)
2. รอบอบรม (Session): สร้าง/แก้ไข · วันเวลา/สถานที่/จำนวนรับ · เปิดรับ/ปิดรอบ · guard หลักสูตร published เท่านั้น (FN-02)
3. ลงทะเบียน/มอบหมายผู้เรียน: จาก gap (Performance hook) หรือเลือกเอง · บล็อกเกินจำนวนรับ · กันลงซ้ำ (FN-03)
4. DOA gate เมื่อ has_cost → ขออนุมัติก่อนยืนยัน · slot picker เลือกคนตามตำแหน่ง (ไม่ hardcode สาย) (FN-04, FN-08)
5. หลักสูตรฟรี → ลงทะเบียนยืนยันทันที ข้าม DOA (FN-05)
6. เช็คชื่อเข้า/ขาด (attendance) → บันทึกผล (ผ่าน/ไม่ผ่าน) เฉพาะรอบ closed + ประเมิน 1-5 + comment (FN-06)
7. ออกใบรับรองผู้ผ่าน = soft ref (ไม่มีเลขรัน/PDF) (FN-07)
8. ค่าอบรม → ส่ง Expense Claim (hook display-only) + ยิงมูลค่า EC (CSQ · ไม่มี AC) · หลัง confirmed + กันส่งซ้ำ (FN-09)
9. gap จากประเมินผลงาน → แนะนำผู้เรียน (Performance hook display-only · ไม่สร้าง gap เอง) (FN-10)
10. ยกเลิกการลงทะเบียน (soft archive คืนที่ว่าง) (FN-11)
11. ประวัติอบรมรายคน + ชั่วโมงสะสม (เฉพาะรายการที่ผ่าน) (FIX-04)
12. แจ้งเตือน 3 event: เปิดรับ / ยืนยันลงทะเบียน / ประกาศผล (FN-12)
13. รายงานการอบรม: completion rate + ต้นทุนต่อหัว + filter (FN-13, FIX-05)
14. กติกากลาง: ค้นหา/filter + empty (FN-90) · ปิด/ยกเลิก confirm + soft archive (FN-91) · validate + กัน double-submit (FN-92) · audit append-only (FN-93) · masking ตาม role (FN-94)

### Out of Scope (ตัดโดยมติ — unsupported 5)
- **จ่ายเงินค่าอบรมจริง / ลงบัญชี** — ส่ง hook Expense Claim เท่านั้น (LOCK-02 · OB-1)
- **ประเมินผลงาน / สร้าง gap เอง** — อ่านจาก Performance (hook) เท่านั้น (LOCK-03 · OB-2)
- **eLearning content / SCORM · competency/skill mapping** — NICE ไม่รองรับรอบนี้ (OQ)
- **ใบรับรองเลขรัน / PDF ทางการ** — soft ref (ไม่ใช้ doccfg/pdfdoc · LOCK-07)
- **สร้าง/แก้ config หมวดหลักสูตรกลาง** — อ่านจาก HR Configuration #107 เท่านั้น (LOCK-06)

### Out of Scope (mark from Phase 2.5 skipped probes)
- ไม่มี probe ที่ skip — Lane Mode ตอบ probe ครบด้วย conservative default (`[AI-DEFAULT]` · ดู 05_RULES §5.5) · ทุก default carry เป็น OQ ให้ BA/SEC confirm

---

## §0.4 Roles & Responsibilities (COSO)

| Role | Person/Team | Responsibilities |
|---|---|---|
| **Maker** | HR L&D (เจ้าหน้าที่ฝึกอบรม) | สร้างหลักสูตร/รอบ · ลงทะเบียน · ส่งอนุมัติ (DOA) · เช็คชื่อ · บันทึกผล · ออกใบรับรอง · ส่ง Expense |
| **Approver** | หัวหน้าสายงาน + ผจก.ฝ่ายพัฒนาบุคลากร | อนุมัติ/ไม่อนุมัติการลงทะเบียนที่มีค่าใช้จ่าย (DOA) |
| **Viewer** | ผู้มีสิทธิ์อ่าน | ดูอย่างเดียว · ตัวเงิน mask |
| **Owner** | HR L&D + ผู้บริหารพัฒนาบุคลากร | ติดตาม completion rate / ต้นทุนต่อหัว |

> **SoD:** Maker (HR L&D · ลงทะเบียน/ส่งอนุมัติ) ≠ Approver (หัวหน้า/ผจก. · อนุมัติ DOA) — ผ่าน
> รายละเอียดต่อ workflow → ดู `01_UI.md §1.3 Journey` + `05_RULES §5.3 Permission Matrix`

---

## §0.5 Dependencies

### Upstream (this feature depends on)
| Dependency | Type | Source |
|---|---|---|
| Employee (ผู้เรียน/ผู้อนุมัติ) | Data / API (read) | F011 (done) — `GET /employees?status=active&q=` |
| Performance gap | Data / hook (read-only) | F131 (done) — `GET /performance/gaps?course_id=` |
| HR Configuration (หมวดหลักสูตร #107) | Data / API (read) | F164 (done) — read-only, ห้าม CRUD |
| DOA engine (สายอนุมัติ) | Engine (external) | F-DLG-001 Policy Center — feature ประกาศเท่านั้น (DOA_BRIEF) |
| ENG-NOTIFY (แจ้งเตือน) | Engine (external) | F-NOTIFY — 3 event (NTF_BRIEF) |
| Rate Card (อัตรากลาง/มูลค่า EC) | Data / API | **F060 — ยังไม่ dev** → มูลค่า EC/ต้นทุนต่อหัว **display-only (contract-pending)** ห้าม hardcode |

### Downstream (features/engines that consume from this feature)
| Consumer | What it uses |
|---|---|
| Expense Claim (F101) | รับมูลค่าอบรม (EC hook display-only) เมื่อกดส่ง — ไม่ auto-post |
| CSQ / โครงสร้างต้นทุน | event `train.enrolled_paid` → **EC** เท่านั้น (ไม่มี AC · ดู CSQ_BRIEF) |
| ประวัติอบรม/ชั่วโมงสะสมรายคน | ผล passed + ชั่วโมงหลักสูตร (ป้อน competency อนาคต) |

### External
| Service | Purpose |
|---|---|
| Policy Center (F-DLG-001) | DOA chain resolve (สายอนุมัติ · ไม่มีวงเงินรอบนี้) |
| Policy Center (Data Classification / Restricted Resources) | wire field Restricted (งบ/มูลค่า EC · ดู 04_DB §4.6.6) |

---

## §0.6 Stack & Architecture

| Layer | Technology |
|---|---|
| Frontend | vanilla JS SPA (prototype) → React/Next.js (build) · hash route `#/train/<tab>` |
| API | Node.js / Strapi (REST · `/api/v1/training/...`) |
| Database | PostgreSQL (RLS multi-tenant) |
| Engine layer | CUBIC Registry (training-completion-metrics, training-hours-accumulator) + external (DOA, ENG-NOTIFY) |
| Auth | JWT + role-based (RBAC กลาง · persona demo = scaffolding) |

---

## §0.7 Multi-Tenant & Security Context

- [x] Multi-tenant feature: **YES** (RLS by tenant)
- [x] PII data involved: **YES** (ผู้เรียน snapshot: ชื่อ/ตำแหน่ง/แผนก — ดู 04_DB §4.2 + §4.6)
- [x] Financial data: **YES** (งบหลักสูตร · มูลค่า EC · ต้นทุนต่อหัว)
- [x] Audit log required: **YES** (append-only ทุก mutation · FN-93)

**Security Bible domains applied:** D2 (Auth) · D5 (Financial) · D7 (PII) · D9 (Audit) · D15 (Admin/approval) · D17 (Multi-tenant) — ดู 05_RULES §5.7

### §0.7.1 Data Classification Summary

Highest classification level ที่ feature นี้แตะ:
- [x] **Has Restricted fields** — `budget` (งบหลักสูตร), มูลค่า EC (display-only) → mask ตาม role (FN-94)
- [x] **Has Confidential fields** — employee snapshot (name/position/dept · PII), `gap_ref`/perf_ref, approver identity
- [x] Internal (default) — สถานะ, timestamps, audit
- [ ] Public-facing data — ไม่มี

**Linkage:** Restricted (งบ/มูลค่า EC) → register Policy Center → Restricted Resources · PII (ผู้เรียน snapshot) → PDPA consent scope (ดู 04_DB §4.6.6)

---

## §0.8 Open Questions

> Carry ครบจาก BRD §15 (ห้ามหายเงียบ) + Phase 2.5 `[AI-DEFAULT]` ที่ต้อง confirm

| ID | Question | Blocking? | Owner |
|---|---|---|---|
| OQ-01 | **FN-10 framing:** จอทำ "แนะนำผู้เรียนที่มี gap" · checklist เขียน "แนะนำหลักสูตร" — hook เนื้อในครบ (qc นับครอบ) · เป็นเรื่องถ้อยคำ ไม่กระทบ logic | NO | BA |
| OQ-02 | ใบรับรอง = soft ref (ไม่มีเลขรัน/PDF) — ยืนยันไม่ต้องออกเอกสารทางการรอบนี้ ([ASSUMED] ตาม LOCK-07) | NO | BA |
| OQ-03 | **Rate Card (F060) ยังไม่ dev** → มูลค่า EC/ต้นทุนต่อหัว display-only (contract-pending) จนกว่าพร้อม · ห้าม hardcode (R17 DYNAMIC) | NO (ไม่บล็อก launch · dev ห้ามผูกตัวเลขจนกว่าพร้อม) | dev Rate Card / BA |
| OQ-04 | **สาย DOA (R14):** จำนวนขั้น/ตำแหน่งจริง + DOA role-id master · ใช้ [DEFAULT] 2 ขั้น (หัวหน้าสายงาน + ผจก.พัฒนาบุคลากร) · **drift:** DOA_BRIEF ระบุ `role-hr-ld-head` แต่ HTML ใช้ `role-hr-dev-head` (ตำแหน่งเดียวกัน) — role-id ปลายทางต้องเคาะที่ DOA declaration · CL-0013 (สายผู้บริหาร) แขวน | **YES** (dev ห้าม hardcode สาย · role-id เดาผิดมีคนตั้งค่าจริง) | SEC/BA + DOA declaration |
| OQ-05 | **RBAC matrix:** หัวหน้า "สร้างได้/อนุมัติอย่างเดียว"? prototype ให้ non-viewer (รวมหัวหน้า) สร้าง/แก้ได้ (recruit precedent) | YES (ก่อนตั้ง RBAC จริง) | SEC/BA |
| OQ-06 | **ยกเลิกการลงทะเบียนหลังส่ง Expense (EC) แล้ว → นโยบาย reverse EC** · รอบนี้ระบบ**ไม่ auto-reverse** (conservative `[AI-DEFAULT]`) — cancel ได้แต่ EC hook ที่ส่งไปแล้วไม่ถูกถอนอัตโนมัติ | **YES** (กระทบเงิน) | BA/Finance |
| OQ-UX | ศัพท์ระบบบนจอ (hook / EC / CSQ) · แถวชื่อหลักสูตรยาว | NO | BA |
| OQ-07 | **Declarations (DOA/NTF/CSQ):** brief มีครบใน pack (`5_DECLARATIONS/`) · รันสคริปต์ declaration **หลัง step 7 โดยผู้ใช้สั่ง** — FRD event/slot/EC ⊆ brief แล้ว | NO | ผู้ใช้ (post-step-7) |

> Resolved → move to 07_LOCKED_DECISIONS §7.3

---

## §0.9 Glossary

| Term | Definition |
|---|---|
| has_cost | ธงระดับหลักสูตร: มีค่าใช้จ่ายหรือไม่ — ตัวชี้ทั้ง DOA gate + Expense hook (LOCK-01) |
| DOA | Delegation of Authority — สายอนุมัติกลาง (F-DLG-001) · feature ประกาศเท่านั้น |
| EC | Expense Category — มูลค่าอบรม (ผลได้พนักงาน) ยิงเข้าโครงสร้างต้นทุน (CSQ) · **ไม่มี AC** (Expense เป็นตัวลงบัญชี) |
| AC | Accounting Cost — การลงบัญชี · ไม่ประกาศในฟีเจอร์นี้ (LOCK-04) |
| gap | ช่องว่างจากผลประเมินผลงาน (Performance F131) → แนะนำผู้เรียน (hook read-only) |
| soft ref (cert) | ใบรับรองอ้างอิง ไม่มีเลขรัน/PDF ทางการ |
| completion rate | ผ่าน ÷ บันทึกผล (นับเฉพาะผลจากรอบ closed · FIX-01) |
| ต้นทุนต่อหัว | งบหลักสูตร ÷ ผู้ผ่าน (ผู้ผ่าน=0 หรือฟรี → "—" กันหารศูนย์ · FIX-05) |

---

## §0.10 Pack Navigation

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW.md | All | meta + scope + coverage |
| 01_UI.md | FE dev | Layout Decision Log + Pages + Journey |
| 02_API.md | BE dev (HTTP) | API contracts |
| 03_LOGIC.md | BE dev (logic) | Functions + Engines + Trace |
| 04_DB.md | DBA / BE | Tables + Fields + Classification |
| 05_RULES.md | BE + QA | Rules + Edge Cases + Errors + Security |
| 06_TESTS.md | QA | AC + DoD + Cross-module |
| 07_LOCKED_DECISIONS.md | All | Scope Lock + LDs |
| INDEX.md | All | Cross-reference quick nav |

---

## §0.11 Scope Lock

> FULL variant → รายละเอียดอยู่ที่ **07_LOCKED §7.0** (immutable) · ที่นี่สรุป ref เท่านั้น
> **Scope Lock Ref:** LANE_BRIEF + STANDARD_BASELINE (MUST 9) + HANDOFF §3 (LOCK 17 ส.ค.) · BRD §3.4 (LOCK-01..07)

---

## §0.12 Coverage Manifest (กัน requirement หล่น BRD→FRD)

> ทุก FN (18) + Story (BRD §7) + Rule (§9) + Edge confirmed (§10) → ที่อยู่ใน pack · **คอลัมน์ FN-XX บังคับ (Lane Mode)**

| FN | BRD Ref | Requirement (ย่อ) | อยู่ที่ใน Pack |
|---|---|---|---|
| **FN-01** | §7 US-01 · §9 R01 | สร้างหลักสูตร (has_cost/งบ) | 01_UI P-01/P-05 · 02_API-02 · 03_FN-01 · 04_DB T_training_course · 05_RULES BR-01 · 06 AC-01 |
| **FN-02** | §7 US-02 · §9 R11 | สร้างรอบอบรม (guard published) | 01_UI P-02/P-07 · 02_API-08 · 03_FN-05 · 05_RULES BR-11 · 06 AC-05 |
| **FN-03** | §7 US-03 · §9 R02/R03 | ลงทะเบียน (gap/manual · เกินจำนวนบล็อก) | 01_UI P-09 · 02_API-14 · 03_FN-08 · 05_RULES BR-02/BR-03 · 06 AC-07/AC-08 |
| **FN-04** | §7 US-04 · §9 R04 | has_cost → DOA ก่อนยืนยัน | 01_UI P-10 · 02_API-15 · 03_FN-09 · 05_RULES BR-04 · 06 AC-09 |
| **FN-05** | §7 US-04 · §9 R04 | ฟรี → ยืนยันทันที ข้าม DOA | 01_UI P-09 · 02_API-14 · 03_FN-08 · 05_RULES BR-04 · 06 AC-10 |
| **FN-06** | §7 US-06 · §9 R05/R05b | บันทึกผล (closed + attended) + eval | 01_UI P-11 · 02_API-19/20 · 03_FN-13/FN-14 · 05_RULES BR-05/BR-05b · 06 AC-13/AC-14 |
| **FN-07** | §7 US-07 · §9 R07(cert) | ออกใบรับรอง (soft ref) | 01_UI P-03/P-08 · 02_API-21 · 03_FN-15 · 05_RULES BR-07C · 06 AC-15 |
| **FN-08** | §7 US-05 · §9 R13/R14 | อนุมัติ DOA slot picker (ไม่ hardcode) | 01_UI P-10 · 02_API-15/16 · 03_FN-09/FN-10 · 05_RULES BR-13/BR-14 · 06 AC-11 |
| **FN-09** | §7 US-08 · §9 R06/R09/R12 | ค่าอบรม → Expense hook + EC | 01_UI P-08(approval tab) · 02_API-22 · 03_FN-16 · 05_RULES BR-06/BR-09/BR-12 · 06 AC-16 · XT-01 |
| **FN-10** | §7 US-03 · §9 R07 | gap → แนะนำผู้เรียน (hook read) | 01_UI P-09 · 02_API-25 · 03_FN-20 · 05_RULES BR-07 · 06 AC-08 · OQ-01 |
| **FN-11** | §5 A3 · §9 R08 | ยกเลิกการลงทะเบียน (soft archive) | 01_UI P-08 · 02_API-18 · 03_FN-12 · 05_RULES BR-08 · 06 AC-17 |
| **FN-12** | §7 · §9 R08 | แจ้งเตือน 3 event | 01_UI §1.5 · 02_API-11/14/16/20 · 03_FN-06/FN-10/FN-14 · NTF_BRIEF · 06 AC-19 |
| **FN-13** | §7 US-10 · §9 R16 | รายงาน completion + ต้นทุนต่อหัว | 01_UI P-04 · 02_API-23 · 03_FN-18 + ENG-TRN-01 · 05_RULES BR-16 · 06 AC-18 |
| **FN-90** | กติกากลาง | ค้นหา/filter + empty | 01_UI §1.6 · 02_API-01/07/13 · 03_FN (list) · 06 AC-20 |
| **FN-91** | กติกากลาง | ปิด/ยกเลิก confirm + soft archive | 01_UI P-06/P-08 · 02_API-06/12/18 · 03_FN-04/FN-07/FN-12 · 05_RULES BR-08 · 06 AC-17/AC-21 |
| **FN-92** | กติกากลาง | validate + กัน double-submit | 02_API §2.3 idempotency · 03_FN-01/FN-08/FN-16 · 05_RULES EC-04/EC-07 · 06 AC-22 |
| **FN-93** | กติกากลาง · §9 R08 | audit append-only | 03_FN-21 · 04_DB T_training_audit_log · 05_RULES §5.7 D9 · 06 AC-23 |
| **FN-94** | §9 R08 · §4 note | masking ตาม role | 01_UI §1.2 · 03_FN-19 · 04_DB §4.6 · 05_RULES §5.7 D-CLASS · 06 AC-24 |
| **FIX-04** | §7 US-09 · §9 R15 | ประวัติรายคน + ชั่วโมงสะสม | 01_UI P-12 · 02_API-27 · 03_FN-17 + ENG-TRN-02 · 05_RULES BR-15 · 06 AC-25 |
| **FIX-05** | §7 US-10 · §9 R16 | ต้นทุนต่อหัว กันหารศูนย์ + mask | 01_UI P-04 · 03_FN-18 + ENG-TRN-01 · 05_RULES BR-16 · 06 AC-18 |

**สรุป:** FN **18/18** ครอบ (FN-01..13 + FN-90..94) + capability FIX-01..07 ครบ · Stories 10/10 · Rules R01–R17 → 05_RULES ครบ · Edges §10.1 (8 ☑) + §10.2 (6 probe) → 05_RULES §5.5 · **ไม่มี requirement ที่ไม่มีที่ลง** · ของที่ยังต้องเคาะ → OQ-01..07
