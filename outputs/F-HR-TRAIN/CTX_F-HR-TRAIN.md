# CTX — F-HR-TRAIN: Training / อบรม (F133)

> **derived from:** FRD_F-HR-TRAIN v1.0 (2026-09-03) · **generated:** 2026-09-03
> **module:** Human Capital → Learning & Development · **status:** active (FRD DRAFT for BA/SEC review)
> ⚠ Derived artifact — source of truth คือ FRD Pack · ถ้า FRD revise ต้อง regen CTX

---

## 1. Summary
แคตตาล็อกหลักสูตร + การลงทะเบียนอบรมของ HR L&D: สร้างหลักสูตร (มี/ไม่มีค่าใช้จ่าย + งบ) → เปิดรอบอบรม (เฉพาะหลักสูตร published) → ลงทะเบียน/มอบหมายผู้เรียน (จาก gap ผลประเมิน หรือเลือกเอง). หลักสูตร has_cost เข้าสาย DOA ก่อนยืนยัน · หลักสูตรฟรีข้าม DOA ยืนยันทันที. หลังปิดรอบ → เช็คชื่อ → บันทึกผล (ผ่าน/ไม่ผ่าน) + ประเมิน → ออกใบรับรอง soft ref. ค่าอบรมส่งเป็น hook เข้า Expense Claim + ยิงมูลค่า EC เข้า CSQ (ไม่ post บัญชีเอง). รายงาน completion rate + ต้นทุนต่อหัวรายคน/ประวัติชั่วโมงสะสม. Trigger: HR L&D สร้างงาน · Performance gap แนะนำผู้เรียน.

## 2. Data Contract

### Entities
| Entity | PK | Key Fields | หมายเหตุ |
|---|---|---|---|
| `T_training_course` | id (uuid) | code (AUTO `CRS-<พ.ศ.>-NNN`, running ในโค้ด ไม่ใช่ doccfg), name, category (อ่านจาก HR Config #107), has_cost, budget (Restricted), status | หลักสูตร header master · UNIQUE(tenant_id, code) |
| `T_training_session` | id (uuid) | code (`SES-<พ.ศ.>-NNN`), course_id (FK, published เท่านั้น ตอนสร้าง), capacity (≥1), start_date, location, status | รอบอบรม · 1 course : N session |
| `T_training_enrollment` | id (uuid) | session_id (FK), emp_id (FK Employee · PII), emp_snapshot (jsonb {id,name,position,dept}), source, gap_ref, status, attended, result, eval_score, cert (jsonb soft ref), expense_sent, approval_entry/current/done | การลงทะเบียน · UNIQUE(tenant_id, session_id, emp_id) WHERE status≠cancelled (กันลงซ้ำ active) |
| `T_training_approval_step` | id (uuid) | enrollment_id (FK), step_order, slot_role (จาก DOA · ไม่ hardcode คน), slot_name, approver_id (FK Employee), result | ขั้นสาย DOA · เกิดเมื่อ has_cost · UNIQUE(enrollment_id, step_order) |
| `T_training_audit_log` | id (bigserial) | entity_type, entity_id, action, detail, kind, actor, at | append-only (NO UPDATE/DELETE) · polymorphic (FN-93) · ≥7 ปี |

> Existing (ref, read-only · ไม่ FK ข้าม service): `T_employee` (F011) · performance gap (F131) · hr_config category #107 (F164)

### Enums / States (ครบทุกค่า — ห้าม conform ผิดค่า)
| Field | Values | Transition owner |
|---|---|---|
| `course.status` | `draft` → `published` → `closed` | F-HR-TRAIN |
| `session.status` | `draft` → `open` → `closed` | F-HR-TRAIN |
| `enrollment.status` | `pending_doa` → `confirmed` → `passed` / `failed` · `cancelled` (soft archive จาก pending_doa/confirmed) | F-HR-TRAIN |
| `enrollment.source` | `gap` / `manual` | F-HR-TRAIN |
| `enrollment.attended` | `null` (ยัง) / `true` (เข้า) / `false` (ขาด) | F-HR-TRAIN |
| `enrollment.result` | `null` / `pass` / `fail` | F-HR-TRAIN |
| `enrollment.eval_score` | `1..5` หรือ null (ไม่บังคับ) | F-HR-TRAIN |
| `approval_step.result` | `pending` / `approved` / `rejected` | F-HR-TRAIN (ผ่าน DOA) |
| `audit_log.entity_type` | `course` / `session` / `enrollment` | F-HR-TRAIN |
| `audit_log.kind` | `ok` / `warn` / `bad` | F-HR-TRAIN |

**State transition (enrollment):** create ─(has_cost)→ pending_doa ─(approve ครบ)→ confirmed ; create ─(ฟรี)→ confirmed ; confirmed ─(closed + attended=true + result)→ passed/failed ; passed ─(issue cert)→ soft ref ; pending_doa ─(reject)→ cancelled.

### Relationships
- `course` 1—N `session` (fk: session.course_id) · `session` 1—N `enrollment` (fk: enrollment.session_id)
- `enrollment` 1—N `approval_step` (fk: approval_step.enrollment_id · embedded summary ใน enrollment)
- `T_employee` 1—N `enrollment` (emp_id + emp_snapshot) · `T_employee` 1—N `approval_step` (approver_id)
- อ้าง master (read-only): Performance gap F131 → enrollment.source/gap_ref · HR Config #107 F164 → course.category · Rate Card F060 (pending) → มูลค่า EC/ต้นทุนต่อหัว (display-only)
- ทุก entity → `T_training_audit_log` (append-only)

## 3. API Surface
Base: `/api/v1/training` · Headers: `X-Tenant-Id` (required) · mutation: `Idempotency-Key` (required)

| Method | Endpoint | ทำอะไร | Payload หลัก |
|---|---|---|---|
| GET | /training/courses · /courses/:id | list/รายละเอียดหลักสูตร (filter หมวด/สถานะ/ค้นหา) | — |
| POST | /training/courses | สร้างหลักสูตร (draft/publish) | `{ name, category, instructor, duration, has_cost, budget, publish }` |
| PUT | /training/courses/:id | แก้ไขหลักสูตร | course fields |
| POST | /training/courses/:id/publish · /close | เผยแพร่ (draft→published) · ปิด (soft archive) | `{}` |
| GET | /training/sessions · /sessions/:id | list/รายละเอียดรอบ (+ผู้เรียน +approval) | — |
| POST | /training/sessions | สร้างรอบ (guard course published · BR-11) | `{ course_id, start_date, end_date?, time_range?, capacity, location }` |
| PUT | /training/sessions/:id | แก้ไขรอบ | session fields |
| POST | /training/sessions/:id/open · /close | เปิดรับ (draft→open → NTF) · ปิดรอบ (open→closed) | `{}` |
| GET | /training/enrollments | list ลงทะเบียน (result/report filter) | — |
| POST | /training/sessions/:id/enrollments | ลงทะเบียนผู้เรียน (has_cost gate) | `{ emp_id, source, gap_ref? }` |
| POST | /training/enrollments/:id/submit-approval | ส่งอนุมัติ DOA (slot picker) | `{ entry, steps:[{order, slot_role, approver_id}] }` |
| POST | /training/enrollments/:id/approve · /reject | อนุมัติ 1 ขั้น (ครบ→confirmed) · ไม่อนุมัติ | reject: `{ reason }` (required) |
| POST | /training/enrollments/:id/cancel | ยกเลิกลงทะเบียน (soft archive คืนที่ว่าง) | `{}` |
| POST | /training/enrollments/:id/attendance | เช็คชื่อ (รอบ closed) | `{ attended }` |
| POST | /training/enrollments/:id/result | บันทึกผล + ประเมิน (→ NTF) | `{ result, eval_score?, eval_comment? }` |
| POST | /training/enrollments/:id/certificate | ออกใบรับรอง (soft ref · เฉพาะ passed) | `{}` |
| POST | /training/enrollments/:id/expense | ส่งมูลค่า EC เข้า Expense Claim (hook display-only) | — (กัน expense_sent ซ้ำ) |
| GET | /training/report | completion rate + ต้นทุนต่อหัว (mask money) | — |
| GET | /training/employees/:id/history | ประวัติอบรม + ชั่วโมงสะสม (mask money) | — |
| GET | /employees?status=active&q= | (ref F011) ผู้เรียน/ผู้อนุมัติ | — |
| GET | /performance/gaps?course_id= | (hook F131) gap read-only | — |
| GET | /hr-config/course-categories | (ref F164 #107) หมวด | — |
| GET | /rate-card/training-rate?course_id= | **PENDING (F060)** มูลค่า EC/อัตรากลาง — display-only ห้าม hardcode | — |

### Events emitted
| Event | Type | Trigger point | Payload key |
|---|---|---|---|
| `train_session_opened` | NTF (ENG-NOTIFY) | session draft→open (API-11 / FN-06) | `ref=session_id` · `{course, session}` |
| `train_enroll_confirmed` | NTF (ENG-NOTIFY) | enrollment→confirmed (ฟรี FN-08 หรือ DOA ครบ FN-10) · ยิงครั้งเดียว/enrollment | `ref=enrollment_id` · `{course, date}` (default app+email · lock on) |
| `train_result` | NTF (ENG-NOTIFY) | enrollment confirmed→passed/failed (API-20 / FN-14) | `ref=enrollment_id` · `{course, result}` |
| `train.enrolled_paid` | CSQ (EC · ไม่มี AC) | อนุมัติ DOA ครบ → confirmed (API-16 / FN-10) | `{ ref:enroll_id, course, value_declared, currency:'THB', basis:'declared' }` |

> `doa_pending`/`doa_result`/`doa_escalate` มาจาก DOA engine อัตโนมัติ — feature **ไม่ประกาศซ้ำ**. `train_*` events ยังไม่อยู่ในทะเบียนกลาง F-NOTIFY (มีเฉพาะสาย Sales/DOA) → เสนอกลุ่มใหม่ "ฝึกอบรม (HR)" · exact event_id ต้องยืนยันก่อน dev wire (OQ-NTF-01).

## 4. Shared Rules (cross-boundary เท่านั้น)
| Rule ID | Rule | กระทบใคร |
|---|---|---|
| BR-04 (LOCK-01) | has_cost=true → DOA ก่อน confirmed · ฟรี → confirmed ทันที ข้าม DOA | DOA / Expense / CSQ |
| BR-06 (LOCK-02) | ค่าอบรม = hook Expense Claim display-only — **ไม่จ่าย/ไม่ auto-post บัญชี** | Expense Claim F101 |
| BR-09 (LOCK-04) | confirmed (has_cost) → emit `train.enrolled_paid` (**EC เท่านั้น · ไม่มี AC** — Expense เป็นตัวลงบัญชี) | CSQ / โครงสร้างต้นทุน |
| BR-07 (LOCK-03) | gap อ่านจาก Performance (hook read-only) — **ไม่สร้าง/แก้ gap เอง** | Performance F131 |
| BR-11 (FIX-02) | สร้าง session ได้เฉพาะ course.status='published' | ผู้เรียก create session |
| BR-14 / LD-05 | สาย DOA มาจาก DOA กลาง (F-DLG-001) — feature **ประกาศเท่านั้น ห้าม hardcode คน/ลำดับ** · [DEFAULT] 2 ขั้น | DOA F-DLG-001 (OQ-04 role-id + drift) |
| BR-08 (LOCK-05) | audit append-only ทุก mutation + masking ตัวเงินตาม role | Policy Center (audit/Restricted) |
| BR-07C (LOCK-07) | ใบรับรอง = soft ref (ไม่มีเลขรัน/PDF · ไม่ใช้ doccfg/pdfdoc) | — (ยืนยัน scope) |
| BR-17 (R17) | มูลค่า EC/อัตรากลางอ่านจาก Rate Card F060 — display-only ห้าม hardcode จนพร้อม | Rate Card F060 (pending) |
| EC-05 / LD-04 | cancel หลัง expense_sent=true → **ไม่ auto-reverse EC** (conservative) · flag Finance | Expense / Finance (OQ-06) |

## 5. Integration
- **Depends on (upstream):**
  - Employee **F011** (done) — `GET /employees?status=active&q=` (ผู้เรียน/ผู้อนุมัติ)
  - Performance gap **F131** (done) — `GET /performance/gaps?course_id=` (hook read-only · แนะนำผู้เรียน)
  - HR Configuration **F164** #107 (done) — `GET /hr-config/course-categories` (หมวดหลักสูตร · read-only ห้าม CRUD)
  - Rate Card **F060** (**ยังไม่ dev**) — `GET /rate-card/training-rate` มูลค่า EC/ต้นทุนต่อหัว **display-only contract-pending** (OQ-03)
  - DOA engine **F-DLG-001** (Policy Center) — resolve สายอนุมัติ (external · ประกาศเท่านั้น)
  - ENG-NOTIFY **F-NOTIFY** — 3 event แจ้งเตือน
- **Depended by (downstream):**
  - Expense Claim **F101** — รับมูลค่าอบรม (EC hook display-only) เมื่อกดส่ง · **ไม่ auto-post**
  - CSQ / โครงสร้างต้นทุน — event `train.enrolled_paid` (EC เท่านั้น · ไม่มี AC)
  - ประวัติอบรม/ชั่วโมงสะสมรายคน — ผล passed + ชั่วโมงหลักสูตร (ป้อน competency อนาคต)
- **Declarations:**
  - **DOA:** yes · scope `policy_approve` · kind `train_enroll` · gate = has_cost (ไม่มีวงเงิน · amount 0→null) · 1 สาย [DEFAULT] 2 ขั้น (หัวหน้าสายงาน `role-line-manager` → ผจก.พัฒนาบุคลากร) · entry `DOA-TRAIN-ENROLL-001` · wire_status pending · role-id ต้องเคาะ (OQ-04 · drift `role-hr-ld-head` vs `role-hr-dev-head`)
  - **NTF:** yes · 3 event (train_session_opened · train_enroll_confirmed · train_result) · เสนอกลุ่มใหม่ "ฝึกอบรม (HR)" (OQ-NTF-01)
  - **CSQ:** yes · 1 event `train.enrolled_paid` → EC (ไม่ประกาศ AC/OC/DC/SC)
  - **DOCCFG:** no · **PDF:** no (ใบรับรอง soft ref · LOCK-07 · CD-02)
- **Engine hooks:** ENG-TRN-01 (training-completion-metrics · report) · ENG-TRN-02 (training-hours-accumulator · ชั่วโมงสะสม) — ทั้งคู่ CUBIC scope-local DRAFT (LD-02) · external: DOA (F-DLG-001) · ENG-NOTIFY (F-NOTIFY)

---
*trace: §1 ← FRD 00_OVERVIEW + BRD · §2 ← FRD 04_DB · §3 ← FRD 02_API + NTF/CSQ_BRIEF · §4 ← FRD 05_RULES + 07_LOCKED · §5 ← BRD §12.1 + DOA/NTF/CSQ_BRIEF + 03_LOGIC engines*
