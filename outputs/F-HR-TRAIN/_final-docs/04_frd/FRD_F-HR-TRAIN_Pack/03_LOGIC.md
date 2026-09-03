# 03_LOGIC — F-HR-TRAIN · Training (อบรม)

> **Audience:** BE dev (business logic layer)
> **Scope:** non-HTTP logic — state transitions, guards, calculations, integrations
> **Iron Rule R8:** ทุก mutation API ต้อง trace ไป ≥1 Function/Engine ใน §3.3
> Naming: Functions = camelCase · Engines = kebab-case

---

## §3.1 Functions (Scope-Local)

### F-HR-TRAIN-FN-01: `createCourse`
- **Purpose:** สร้างหลักสูตรใหม่ (draft/publish) พร้อม validate (FN-01)
- **Input:** `{ name, category, instructor, duration, has_cost, budget?, description?, publish:bool }`
- **Output:** `Course | ValidationError[]`
- **Invoked by:** API-02
- **Calls:** FN-21 appendAudit
- **Side effects:** INSERT T_training_course (code AUTO `CRS-<พ.ศ.>-NNN`) · audit
- **Error cases:** ERR_VALIDATION_FAILED · BR_COURSE_BUDGET_REQUIRED (has_cost→budget · BR-01)
- **Iron rule check:** ✅ no HTTP terms

### F-HR-TRAIN-FN-02: `updateCourse`
- **Purpose:** แก้ไขข้อมูลหลักสูตร
- **Input:** `{ id, ...fields }` · **Output:** `Course | ValidationError[]`
- **Invoked by:** API-04 · **Calls:** FN-21 · **Side effects:** UPDATE + audit
- **Iron rule check:** ✅

### F-HR-TRAIN-FN-03: `publishCourse`
- **Purpose:** เปลี่ยนสถานะ draft → published (guard state)
- **Input:** `{ id }` · **Output:** `Course | StateError`
- **Invoked by:** API-05 · **Calls:** FN-21 · **Side effects:** UPDATE status='published' + audit
- **Error cases:** BR_INVALID_STATE (ต้องเป็น draft)

### F-HR-TRAIN-FN-04: `closeCourse`
- **Purpose:** ปิดหลักสูตร published → closed (soft archive · FN-91) — ไม่เปิดรอบใหม่ได้
- **Input:** `{ id }` · **Output:** `Course` · **Invoked by:** API-06 · **Calls:** FN-21
- **Side effects:** UPDATE status='closed' + audit

### F-HR-TRAIN-FN-05: `createSession` (+ update path)
- **Purpose:** สร้าง/แก้รอบอบรม · **guard: course.status='published' เท่านั้น** (FN-02 · BR-11 · FIX-02)
- **Input:** `{ course_id, start_date, end_date?, time_range?, capacity, location, [id for update] }`
- **Output:** `Session | ValidationError[]`
- **Invoked by:** API-08, API-10 · **Calls:** FN-21
- **Side effects:** INSERT/UPDATE T_training_session (code `SES-<พ.ศ.>-NNN`, status='draft') + audit
- **Error cases:** BR_SESSION_COURSE_NOT_PUBLISHED · ERR_VALIDATION_FAILED (capacity≥1)

### F-HR-TRAIN-FN-06: `openSession`
- **Purpose:** draft → open (เปิดรับสมัคร) + trigger NTF (FN-12)
- **Input:** `{ id }` · **Output:** `Session` · **Invoked by:** API-11 · **Calls:** FN-21
- **Side effects:** UPDATE status='open' + audit + **emit NTF `train_session_opened`** (ENG-NOTIFY)

### F-HR-TRAIN-FN-07: `closeSession`
- **Purpose:** open → closed (จบการอบรม · ปลดล็อกบันทึกผล FIX-01)
- **Input:** `{ id }` · **Output:** `Session` · **Invoked by:** API-12 · **Calls:** FN-21
- **Side effects:** UPDATE status='closed' + audit

### F-HR-TRAIN-FN-08: `createEnrollment`
- **Purpose:** ลงทะเบียนผู้เรียน · has_cost gate · capacity/dup guard · snapshot (FN-03/05)
- **Input:** `{ session_id, emp_id, source:'gap'|'manual', gap_ref? }`
- **Output:** `Enrollment | BusinessError`
- **Invoked by:** API-14 · **Calls:** FN-20 (แสดง gap), FN-21
- **Logic:**
  1. guard session.status='open'
  2. **atomic:** active count < capacity (BR-02 · row lock/`SELECT ... FOR UPDATE` บน session · EC-06) — เกิน → ERR_SESSION_CAPACITY_FULL
  3. กัน emp_id เดิม active ในรอบ (ERR_ALREADY_ENROLLED)
  4. snapshot emp → emp_snapshot (BR-10)
  5. **has_cost → status='pending_doa'** (ต่อ FN-09) · **ฟรี → status='confirmed' + emit NTF `train_enroll_confirmed`** (LOCK-01)
- **Side effects:** INSERT T_training_enrollment + audit · (ฟรี) NTF
- **Iron rule check:** ✅

### F-HR-TRAIN-FN-09: `submitApprovalChain`
- **Purpose:** ผูกสาย DOA จาก slot picker (เลือกคนตามตำแหน่ง · ไม่ hardcode สาย · FN-08)
- **Input:** `{ enrollment_id, entry, steps:[{order, slot_role, slot_name, approver_id}] }`
- **Output:** `Enrollment | BusinessError`
- **Invoked by:** API-15 · **Calls:** FN-21 · **External:** DOA engine (F-DLG-001) resolve chain
- **Logic:** guard has_cost + status='pending_doa' · ทุกขั้นมี approver_id · INSERT approval_step (result='pending') · set approval_entry/current=0/done=false
- **Error cases:** BR_DOA_SLOTS_INCOMPLETE · BR_COURSE_NOT_PAID
- **⚠️ ห้าม hardcode สาย** — slot มาจาก DOA กลาง (OQ-04 role-id ยังต้องเคาะ)

### F-HR-TRAIN-FN-10: `approveEnrollmentStep`
- **Purpose:** อนุมัติ 1 ขั้น · ครบ → confirmed + NTF + EC event (FN-08)
- **Input:** `{ enrollment_id, actor }` · **Output:** `Enrollment | ConcurrencyError`
- **Invoked by:** API-16 · **Calls:** FN-21 · **External:** ENG-NOTIFY, CSQ emitter
- **Logic:**
  1. **re-check** actor.canApprove (EC-03) — ไม่ผ่าน → ERR_NOT_APPROVER
  2. optimistic lock (version · EC-01) — mismatch → ERR_STALE_DATA
  3. หา step pending ตัวถัดไป → result='approved', acted_at=today; current++
  4. ทุกขั้น approved → status='confirmed', approval_done=true, **emit NTF `train_enroll_confirmed`** + **emit CSQ `train.enrolled_paid` (EC)**
- **Side effects:** UPDATE approval_step + enrollment + audit · (confirmed) NTF + EC event
- **Iron rule check:** ✅

### F-HR-TRAIN-FN-11: `rejectEnrollment`
- **Purpose:** ไม่อนุมัติ (เหตุผลบังคับ) → cancelled (A2)
- **Input:** `{ enrollment_id, reason, actor }` · **Output:** `Enrollment`
- **Invoked by:** API-17 · **Calls:** FN-21
- **Logic:** re-check canApprove · step pending → result='rejected' · enrollment status='cancelled' · audit(kind=bad)
- **Error cases:** ERR_NOT_APPROVER · ERR_REASON_REQUIRED

### F-HR-TRAIN-FN-12: `cancelEnrollment`
- **Purpose:** ยกเลิกการลงทะเบียน soft archive คืนที่ว่าง (FN-11)
- **Input:** `{ enrollment_id }` · **Output:** `Enrollment`
- **Invoked by:** API-18 · **Calls:** FN-21
- **Logic:** guard status ∈ {pending_doa, confirmed} · UPDATE status='cancelled' · audit(kind=warn)
- **⚠️ OQ-06:** ถ้า expense_sent=true → **ไม่ auto-reverse EC** (conservative `[AI-DEFAULT]`) · flag Finance (EC-05)

### F-HR-TRAIN-FN-13: `setAttendance`
- **Purpose:** เช็คชื่อเข้า/ขาด (FIX-03)
- **Input:** `{ enrollment_id, attended:bool }` · **Output:** `Enrollment`
- **Invoked by:** API-19 · **Calls:** FN-21
- **Logic:** guard session.status='closed' + enrollment.status='confirmed' · UPDATE attended · audit
- **Error cases:** BR_ATTENDANCE_SESSION_NOT_CLOSED

### F-HR-TRAIN-FN-14: `recordResult`
- **Purpose:** บันทึกผล + ประเมิน + ประกาศผล (FN-06)
- **Input:** `{ enrollment_id, result:'pass'|'fail', eval_score?, eval_comment? }`
- **Output:** `Enrollment | BusinessError`
- **Invoked by:** API-20 · **Calls:** FN-21 · **External:** ENG-NOTIFY
- **Logic (defense-in-depth FIX-01/03):** guard session.status='closed' + status='confirmed' + **attended=true** + result present · set result, status=passed/failed, eval · audit · **emit NTF `train_result`**
- **Error cases:** BR_RESULT_SESSION_NOT_CLOSED (BR-05) · BR_RESULT_NOT_ATTENDED (BR-05b) · ERR_RESULT_REQUIRED

### F-HR-TRAIN-FN-15: `issueCertificate`
- **Purpose:** ออกใบรับรองผู้ผ่าน soft ref (FN-07)
- **Input:** `{ enrollment_id }` · **Output:** `Enrollment`
- **Invoked by:** API-21 · **Calls:** FN-21
- **Logic:** guard status='passed' + !cert · set cert `{id:CERT-REF-*, issued_at, note}` (**ไม่มีเลขรัน/PDF** LOCK-07) · audit
- **Error cases:** BR_CERT_NOT_PASSED

### F-HR-TRAIN-FN-16: `sendExpenseClaim`
- **Purpose:** ส่งมูลค่า EC เข้า Expense Claim (hook display-only · FN-09)
- **Input:** `{ enrollment_id }` · **Output:** `Enrollment`
- **Invoked by:** API-22 · **Calls:** FN-21 · **External:** Expense Claim (F101) hook
- **Logic (FIX-02):** guard status ∈ {confirmed,passed,failed} + has_cost + **expense_sent=false** · set expense_sent=true · audit · **ไม่จ่าย/ไม่ post** — display-only hook
- **Error cases:** ERR_EXPENSE_ALREADY_SENT · BR_EXPENSE_NOT_CONFIRMED · BR_COURSE_NOT_PAID

### F-HR-TRAIN-FN-17: `buildEmployeeHistory`
- **Purpose:** รวมประวัติอบรมรายคน + ชั่วโมงสะสม (FIX-04)
- **Input:** `{ emp_id }` · **Output:** `{ employee, total_hours, passed_count, items[] }`
- **Invoked by:** API-27 · **Calls:** ENG-TRN-02 (parse+sum hours)
- **Logic:** list enrollment ที่ไม่ cancelled · ชม.สะสม = ENG-TRN-02(เฉพาะ passed)
- **Side effects:** read-only

### F-HR-TRAIN-FN-18: `buildTrainingReport`
- **Purpose:** รายงาน completion + ต้นทุนต่อหัว (FN-13/FIX-05)
- **Input:** `{ course_id?:'all'|id }` · **Output:** `{ stats, per_course[], cost_per_head[] }`
- **Invoked by:** API-23 · **Calls:** ENG-TRN-01, FN-19 maskMoneyByRole
- **Logic:** completion rate นับเฉพาะ closed-result (FIX-01) · ต้นทุนต่อหัว = budget÷passed (กันหารศูนย์ → null) · mask ตาม role
- **Side effects:** read-only

### F-HR-TRAIN-FN-19: `maskMoneyByRole`
- **Purpose:** ปิดบังตัวเงินตาม role (FN-94)
- **Input:** `{ amount, role_can_unmask:bool }` · **Output:** `string` (`x,xxx` | `••••••`)
- **Invoked by:** API-23, API-27, API-01/03/09 (field budget) · **Calls:** —
- **Iron rule check:** ✅ pure

### F-HR-TRAIN-FN-20: `readPerformanceGaps`
- **Purpose:** อ่าน gap จาก Performance (hook read-only · FN-10 · ไม่สร้าง gap เอง)
- **Input:** `{ course_id? }` · **Output:** `Gap[]` (emp + gap desc + perf_ref)
- **Invoked by:** API-25, ใช้ภายใน FN-08 (แสดง picker) · **External:** Performance (F131) read
- **Side effects:** read-only (ห้ามแก้ Performance)

### F-HR-TRAIN-FN-21: `appendAudit`
- **Purpose:** เขียน audit log append-only (FN-93)
- **Input:** `{ entity_type, entity_id, action, detail?, kind?, actor }` · **Output:** `void`
- **Invoked by:** ทุก mutation function · **Calls:** — · **Side effects:** INSERT T_training_audit_log (ห้าม UPDATE/DELETE)
- **Iron rule check:** ✅

---

## §3.2 Engines (Reusable / CUBIC-Registered)

### ENG-TRN-01: `training-completion-metrics` [NEW]

| Field | Value |
|---|---|
| id | (assigned at CUBIC registration) |
| code | `training-completion-metrics` |
| name | Training Completion & Cost-per-Head Metrics |
| category | financial-calculation |
| status | DRAFT (this FRD) |
| owner | F-HR-TRAIN |

**Input Schema:**
```json
{ "enrollments":[{"status","result","session_closed":bool,"course_id","course_budget"}],
  "courses":[{"id","name","has_cost","budget"}], "scope":"all|<course_id>" }
```
**Output Schema:**
```json
{ "stats":{"passed","failed","recorded","rate"},
  "per_course":[{"course_id","passed","recorded","rate"}],
  "cost_per_head":[{"course_id","budget","passed","per_head":number|null}] }
```
**Logic Outline:**
1. filter enrollments (ไม่ cancelled · ตาม scope)
2. นับ passed/failed **เฉพาะ session_closed=true** (FIX-01)
3. rate = passed ÷ (passed+failed) (recorded=0 → 0%)
4. cost_per_head = budget ÷ passed (**passed=0 หรือ !has_cost → null** กันหารศูนย์ · FIX-05)
**Used by:** F-HR-TRAIN (report) · (planned) HR analytics dashboard
**Iron rule check:** ✅ pure (no I/O, no HTTP) · reusable · substantial (metrics algorithm) · **ไม่ mask ในนี้** (mask ทำที่ FN-19 นอก engine)
**CUBIC note:** DRAFT → register ตอน dev hand-off (LD-02)

### ENG-TRN-02: `training-hours-accumulator` [NEW]

| Field | Value |
|---|---|
| code | `training-hours-accumulator` |
| name | Training Hours Parser & Accumulator |
| category | generation / calculation |
| status | DRAFT |
| owner | F-HR-TRAIN |

**Input Schema:** `{ enrollments:[{status, course_duration}] }`
**Output Schema:** `{ total_hours:int, per_item:[{hours:int}] }`
**Logic Outline:**
1. parse ชม.จาก duration ด้วย regex `/(\d+)\s*ชม/` (fallback 0 · FIX-04)
2. sum เฉพาะ enrollment ที่ status='passed'
**Used by:** F-HR-TRAIN (emp history) · (planned) competency/พัฒนาบุคลากร
**Iron rule check:** ✅ pure · reusable · substantial (parser + fallback)
**CUBIC note:** DRAFT → register Phase 2

> **External engines (ไม่ใช่ของ feature นี้ — reference):**
> - DOA engine (F-DLG-001) — resolve สายอนุมัติ (ห้าม hardcode)
> - ENG-NOTIFY (F-NOTIFY) — emit 3 event
> - Rate Card (F060 · **ยังไม่ dev**) — มูลค่า EC/อัตรากลาง (display-only จนพร้อม)

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor · MANDATORY)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| API-01 | GET | /training/courses | (list build) | — |
| API-02 | POST | /training/courses | FN-01, FN-21 | — |
| API-03 | GET | /training/courses/:id | — | — |
| API-04 | PUT | /training/courses/:id | FN-02, FN-21 | — |
| API-05 | POST | /courses/:id/publish | FN-03, FN-21 | — |
| API-06 | POST | /courses/:id/close | FN-04, FN-21 | — |
| API-07 | GET | /training/sessions | (list build) | — |
| API-08 | POST | /training/sessions | FN-05, FN-21 | — |
| API-09 | GET | /training/sessions/:id | — | — |
| API-10 | PUT | /training/sessions/:id | FN-05, FN-21 | — |
| API-11 | POST | /sessions/:id/open | FN-06, FN-21 | — |
| API-12 | POST | /sessions/:id/close | FN-07, FN-21 | — |
| API-13 | GET | /training/enrollments | (list build) | — |
| API-14 | POST | /sessions/:id/enrollments | FN-08, FN-20, FN-21 | — |
| API-15 | POST | /enrollments/:id/submit-approval | FN-09, FN-21 | — |
| API-16 | POST | /enrollments/:id/approve | FN-10, FN-21 | — |
| API-17 | POST | /enrollments/:id/reject | FN-11, FN-21 | — |
| API-18 | POST | /enrollments/:id/cancel | FN-12, FN-21 | — |
| API-19 | POST | /enrollments/:id/attendance | FN-13, FN-21 | — |
| API-20 | POST | /enrollments/:id/result | FN-14, FN-21 | — |
| API-21 | POST | /enrollments/:id/certificate | FN-15, FN-21 | — |
| API-22 | POST | /enrollments/:id/expense | FN-16, FN-21 | — |
| API-23 | GET | /training/report | FN-18, FN-19 | ENG-TRN-01 |
| API-25 | GET | /performance/gaps | FN-20 | — |
| API-27 | GET | /training/employees/:id/history | FN-17 | ENG-TRN-02 |

### Trace Verification (Self-Check)
- [x] Every mutation API (17 ตัว) has ≥1 Function ✅ (ทุกตัวมี FN-21 appendAudit อย่างน้อย)
- [x] No orphan Function — FN-01..21 ปรากฏใน trace ครบ (FN-19 ผ่าน API-23/27/list; FN-20 ผ่าน API-14/25; FN-21 ทุก mutation)
- [x] No orphan Engine — ENG-TRN-01 (API-23), ENG-TRN-02 (API-27) traced
- [x] No hidden logic ใน 02_API — business logic อยู่ที่นี่ทั้งหมด

---

## §3.4 Dependencies

### External Function/Engine called
- DOA engine `resolve(entry, context)` from F-DLG-001 (Policy Center) — ผ่าน FN-09
- `ENG-NOTIFY.emit(event, payload)` from F-NOTIFY — ผ่าน FN-06/FN-10/FN-14
- CSQ emitter `emit('train.enrolled_paid', ...)` (EC · ไม่มี AC) — ผ่าน FN-10
- Performance gap read (F131) — ผ่าน FN-20
- HR Config category read (F164 #107) — ผ่าน list/form
- Rate Card read (F060 · pending) — ผ่าน API-28 (display-only)

### External that calls into this feature
- Expense Claim (F101) รับ hook จาก FN-16 (display-only)

---

## §3.5 Locked Decisions Referenced
- LD-01: optimistic locking (version) กัน concurrent approve (EC-01) — ดู 07_LOCKED
- LD-02: ENG-TRN-01/02 register CUBIC Phase 2 (scope-local ก่อน)
- LD-03: มูลค่า EC/ต้นทุนต่อหัว = display-only จน Rate Card (F060) พร้อม — ห้าม hardcode (OQ-03)
- LD-04: cancel หลังส่ง EC = ไม่ auto-reverse (OQ-06 · policy pending)

---

## Audience Cheat-Sheet
| Reader | Read |
|---|---|
| BE dev | §3.1 + §3.2 + §3.3 |
| QA | §3.3 + §3.1 Side effects + §3.2 I/O |
| Architect / CUBIC | §3.2 + §3.4 + §3.5 |
