# 02_API — F-HR-TRAIN · Training (อบรม)

> **Audience:** Backend developer (HTTP layer)
> **🚨 Iron Rule:** ห้าม business logic > 5 บรรทัดที่นี่ — ย้ายไป 03_LOGIC §3.1
> **🚨 R8:** ทุก mutation API ต้องระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3
> Base path: `/api/v1/training` · Headers: `X-Tenant-Id` (required) · mutation: `Idempotency-Key` (required · FN-92)

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth (role) |
|---|---|---|---|---|
| API-01 | GET | /training/courses | List หลักสูตร (filter หมวด/สถานะ/ค้นหา) | any |
| API-02 | POST | /training/courses | สร้างหลักสูตร (draft/publish) | hr, manager |
| API-03 | GET | /training/courses/:id | รายละเอียดหลักสูตร | any |
| API-04 | PUT | /training/courses/:id | แก้ไขหลักสูตร | hr, manager |
| API-05 | POST | /training/courses/:id/publish | เผยแพร่หลักสูตร | hr, manager |
| API-06 | POST | /training/courses/:id/close | ปิดหลักสูตร (soft archive) | hr, manager |
| API-07 | GET | /training/sessions | List รอบอบรม | any |
| API-08 | POST | /training/sessions | สร้างรอบ (guard course published) | hr, manager |
| API-09 | GET | /training/sessions/:id | รายละเอียดรอบ + ผู้เรียน + approval | any |
| API-10 | PUT | /training/sessions/:id | แก้ไขรอบ | hr, manager |
| API-11 | POST | /training/sessions/:id/open | เปิดรับสมัคร (→ NTF) | hr, manager |
| API-12 | POST | /training/sessions/:id/close | ปิดรอบ (จบการอบรม) | hr, manager |
| API-13 | GET | /training/enrollments | List ลงทะเบียน (result/report filter) | any |
| API-14 | POST | /training/sessions/:id/enrollments | ลงทะเบียนผู้เรียน (has_cost gate) | hr, manager |
| API-15 | POST | /training/enrollments/:id/submit-approval | ส่งอนุมัติ DOA (slot picker) | hr, manager |
| API-16 | POST | /training/enrollments/:id/approve | อนุมัติ (1 ขั้น · ครบ→confirmed) | approver (canApprove) |
| API-17 | POST | /training/enrollments/:id/reject | ไม่อนุมัติ (เหตุผล) | approver (canApprove) |
| API-18 | POST | /training/enrollments/:id/cancel | ยกเลิกการลงทะเบียน (soft archive) | hr, manager |
| API-19 | POST | /training/enrollments/:id/attendance | เช็คชื่อเข้า/ขาด (รอบ closed) | hr, manager |
| API-20 | POST | /training/enrollments/:id/result | บันทึกผล + ประเมิน (→ NTF) | hr, manager |
| API-21 | POST | /training/enrollments/:id/certificate | ออกใบรับรอง (soft ref) | hr, manager |
| API-22 | POST | /training/enrollments/:id/expense | ส่งมูลค่า EC เข้า Expense Claim (hook) | hr, manager |
| API-23 | GET | /training/report | completion rate + ต้นทุนต่อหัว | any (mask money) |
| API-24 | GET | /employees?status=active&q= | (ref F011) ผู้เรียน/ผู้อนุมัติ | any |
| API-25 | GET | /performance/gaps?course_id= | (hook F131) gap read-only | any |
| API-26 | GET | /hr-config/course-categories | (ref F164 #107) หมวด | any |
| API-27 | GET | /training/employees/:id/history | ประวัติอบรม + ชั่วโมงสะสม | any (mask money) |
| API-28 | GET | /rate-card/training-rate?course_id= | **PENDING (F060)** มูลค่า EC/อัตรากลาง — display-only | any |

> **Mutation APIs (ต้อง trace §2.4/R8):** API-02, 04, 05, 06, 08, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22

---

## §2.2 Per-API Contract (key endpoints)

### API-02: POST /training/courses
| Field | Value |
|---|---|
| roles | hr, manager | 
| headers | X-Tenant-Id, Idempotency-Key (required) |

**Body:**
```json
{ "name":"...", "category":"safety", "instructor":"...", "duration":"2 วัน (12 ชม.)",
  "has_cost":true, "budget":30000, "description":"...", "publish":true }
```
**Validation (field-level ≤5 lines):** name/instructor/duration required · category ∈ HR Config · `has_cost=true → budget required, ≥0` · **complex → 03_LOGIC FN-01 createCourse**
**Response 201:** `{ "id":"uuid","code":"CRS-2569-005","status":"published" }` (publish=false → "draft")
**Errors:** 400 ERR_VALIDATION_FAILED · 403 ERR_INSUFFICIENT_ROLE · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 BR_COURSE_BUDGET_REQUIRED (BR-01)
**Preconditions:** category exists in HR Config
**Side effects:** INSERT T_training_course · INSERT T_training_audit_log
**Calls (Logic):** FN-01 createCourse · FN-21 appendAudit

---

### API-05: POST /training/courses/:id/publish
**Response 200:** `{ "id","status":"published" }`
**Preconditions:** status = 'draft'
**Side effects:** UPDATE status='published' · audit
**Calls (Logic):** FN-03 publishCourse · FN-21

### API-06: POST /training/courses/:id/close
**Body:** `{}` · confirm ที่ UI (Pattern D) · **Preconditions:** status='published'
**Side effects:** UPDATE status='closed' (soft archive) · audit · **Errors:** 422 BR_COURSE_HAS_OPEN_SESSION? → ไม่บังคับ (HTML ปิดได้ · รอบเดิมคงอยู่)
**Calls (Logic):** FN-04 closeCourse · FN-21

---

### API-08: POST /training/sessions
**Body:** `{ "course_id","start_date","end_date?","time_range?","capacity","location" }`
**Validation:** start_date/capacity(≥1)/location required · course_id required · **complex → FN-05**
**Preconditions (R11/BR-11):** course.status = **'published'** เท่านั้น
**Response 201:** `{ "id","code":"SES-2569-003","status":"draft" }`
**Errors:** 422 BR_SESSION_COURSE_NOT_PUBLISHED (BR-11) · 400 ERR_VALIDATION_FAILED
**Side effects:** INSERT T_training_session · audit
**Calls (Logic):** FN-05 createSession · FN-21

### API-11: POST /training/sessions/:id/open
**Preconditions:** status='draft' · **Side effects:** UPDATE status='open' · audit · **emit NTF `train_session_opened`**
**Calls (Logic):** FN-06 openSession · FN-21

### API-12: POST /training/sessions/:id/close
**Preconditions:** status='open' · **Side effects:** UPDATE status='closed' (ปลดล็อกบันทึกผล FIX-01) · audit
**Calls (Logic):** FN-07 closeSession · FN-21

---

### API-14: POST /training/sessions/:id/enrollments
| Field | Value |
|---|---|
| roles | hr, manager | headers | X-Tenant-Id, Idempotency-Key |

**Body:** `{ "emp_id":"uuid", "source":"gap|manual", "gap_ref":"PERF-...?" }`
**Validation:** emp_id required · source ∈ {gap,manual}
**Preconditions / Business (→ FN-08):**
- session.status = 'open'
- active enrollment count < capacity (**BR-02** · race-safe · EC-06)
- ไม่มี enrollment ของ emp_id เดิมที่ยัง active (กันลงซ้ำ)
- snapshot emp (BR-10)
- **has_cost → status='pending_doa'** (ต่อด้วย API-15) · **ฟรี → status='confirmed' + emit NTF `train_enroll_confirmed`** (LOCK-01)
**Response 201:** `{ "id","status":"pending_doa|confirmed" }`
**Errors:** 409 ERR_SESSION_CAPACITY_FULL (BR-02) · 409 ERR_ALREADY_ENROLLED · 422 BR_SESSION_NOT_OPEN
**Side effects:** INSERT T_training_enrollment · audit · (ฟรี) NTF
**Calls (Logic):** FN-08 createEnrollment · FN-20 readPerformanceGaps (ตอนแสดง picker) · FN-21

---

### API-15: POST /training/enrollments/:id/submit-approval (DOA)
**Body:** `{ "entry":"DOA-TRAIN-ENROLL-001", "steps":[{"order":1,"slot_role":"role-line-manager","approver_id":"uuid"}, ...] }`
**Preconditions:** enrollment.status='pending_doa' · course.has_cost=true · เลือกผู้อนุมัติครบทุกขั้น · **สายมาจาก DOA กลาง (F-DLG-001) — ห้าม hardcode** (FN-08/DOA_BRIEF)
**Response 200:** `{ "id","status":"pending_doa","approval_entry":"..." }`
**Errors:** 422 BR_DOA_SLOTS_INCOMPLETE · 422 BR_COURSE_NOT_PAID
**Side effects:** INSERT T_training_approval_step (N ขั้น) · UPDATE enrollment approval_* · audit · (DOA engine emit `doa_pending` อัตโนมัติ — ไม่ประกาศเอง)
**Calls (Logic):** FN-09 submitApprovalChain · FN-21

### API-16: POST /training/enrollments/:id/approve
**Preconditions:** caller role canApprove (**re-check ที่ mutation** · EC-03/BR-13) · มีขั้น pending · optimistic lock (version · EC-01)
**Behavior (→ FN-10):** approve ขั้น pending ตัวถัดไป · ถ้าครบทุกขั้น → status='confirmed' + emit NTF `train_enroll_confirmed` + **emit CSQ event `train.enrolled_paid` (EC)**
**Response 200:** `{ "id","status":"pending_doa|confirmed","approval_current":n }`
**Errors:** 403 ERR_NOT_APPROVER · 409 ERR_STALE_DATA (EC-01) · 422 BR_NO_PENDING_STEP
**Side effects:** UPDATE approval_step + enrollment · audit · (confirmed) NTF + EC event
**Calls (Logic):** FN-10 approveEnrollmentStep · FN-21

### API-17: POST /training/enrollments/:id/reject
**Body:** `{ "reason":"..." }` (required · BR-15/D15)
**Preconditions:** canApprove · มีขั้น pending
**Side effects:** UPDATE step result='rejected' · enrollment status='cancelled' · audit(kind=bad)
**Calls (Logic):** FN-11 rejectEnrollment · FN-21

---

### API-18: POST /training/enrollments/:id/cancel
**Body:** `{}` (confirm ที่ UI) · **Preconditions:** status ∈ {pending_doa, confirmed} (ไม่ยกเลิกที่ passed/failed ปกติ · HTML เปิดปุ่มเฉพาะ pending/confirmed)
**Side effects:** UPDATE status='cancelled' (soft archive · คืนที่ว่าง) · audit(kind=warn)
**⚠️ OQ-06:** ถ้า `expense_sent=true` → **ไม่ auto-reverse EC** (conservative default) · flag ให้ Finance · ดู 05_RULES EC-05
**Calls (Logic):** FN-12 cancelEnrollment · FN-21

### API-19: POST /training/enrollments/:id/attendance
**Body:** `{ "attended": true|false }`
**Preconditions (FIX-03):** session.status='closed' · enrollment.status='confirmed'
**Side effects:** UPDATE attended · audit
**Calls (Logic):** FN-13 setAttendance · FN-21

### API-20: POST /training/enrollments/:id/result
**Body:** `{ "result":"pass|fail", "eval_score":1..5?, "eval_comment":"?" }`
**Preconditions (FIX-01/03 defense-in-depth):** session.status='closed' · enrollment.status='confirmed' · **attended=true** · result required
**Side effects:** UPDATE result + status(passed/failed) + eval · audit · **emit NTF `train_result`**
**Errors:** 422 BR_RESULT_SESSION_NOT_CLOSED (BR-05) · 422 BR_RESULT_NOT_ATTENDED (BR-05b) · 400 ERR_RESULT_REQUIRED
**Calls (Logic):** FN-14 recordResult · FN-21

### API-21: POST /training/enrollments/:id/certificate
**Preconditions:** status='passed' · !cert · **Side effects:** UPDATE cert(soft ref · ไม่มีเลขรัน/PDF) · audit
**Errors:** 422 BR_CERT_NOT_PASSED
**Calls (Logic):** FN-15 issueCertificate · FN-21

### API-22: POST /training/enrollments/:id/expense (EC hook)
**Preconditions (FIX-02):** status ∈ {confirmed, passed, failed} · course.has_cost=true · **expense_sent=false** (กันซ้ำ)
**Behavior:** hook display-only — **ไม่จ่าย/ไม่ post บัญชี** · ส่งมูลค่า EC ให้ Expense Claim (F101)
**Side effects:** UPDATE expense_sent=true · audit · (contract downstream — ดู §2.X)
**Errors:** 409 ERR_EXPENSE_ALREADY_SENT · 422 BR_EXPENSE_NOT_CONFIRMED · 422 BR_COURSE_NOT_PAID
**Calls (Logic):** FN-16 sendExpenseClaim · FN-21

---

### API-23: GET /training/report?course_id=
**Response 200:** `{ "stats":{courses,sessions,enrollments,passed,rate}, "per_course":[{course_id,name,passed,recorded,rate}], "cost_per_head":[{course_id,budget,passed,per_head|null}] }`
**Business:** completion rate นับเฉพาะ **isClosedResult** (รอบ closed · FIX-01) · ต้นทุนต่อหัว = budget ÷ passed (passed=0/ฟรี → null "—" · FIX-05) · **mask money ตาม role**
**Calls (Logic):** FN-18 buildTrainingReport → ENG-TRN-01 · FN-19 maskMoneyByRole

### API-27: GET /training/employees/:id/history
**Response 200:** `{ "employee":{...}, "total_hours":12, "passed_count":n, "items":[...] }`
**Business:** ชั่วโมงสะสม = Σ ชม.หลักสูตร เฉพาะ passed (parse duration · FIX-04)
**Calls (Logic):** FN-17 buildEmployeeHistory → ENG-TRN-02

### API-25: GET /performance/gaps?course_id= (hook read F131)
Read-only · ไม่แก้ Performance · **Calls (Logic):** FN-20 readPerformanceGaps

### API-28: GET /rate-card/training-rate?course_id= (PENDING · F060)
**สถานะ:** contract-pending — F060 ยังไม่ dev · รอบนี้ FE render "อ้างอิง Rate Card · เชื่อมเมื่อพร้อม" · **ห้าม hardcode ตัวเลข** (R17/OQ-03) · เมื่อพร้อม → คืนอัตรากลาง/มูลค่า EC

---

## §2.3 Common Concerns

### Idempotency (PR-7 · FN-92)
ทุก mutation รับ `Idempotency-Key` · cache 24 ชม. · key เดิม+body เดิม → คืน cached (ไม่ INSERT ซ้ำ) · key เดิม+body ต่าง → 409 · **sendExpense เพิ่มชั้น `expense_sent` flag กันซ้ำเชิงธุรกิจ**

### Optimistic Locking (PR-1/EC-01)
approve/update ใช้ `version` (หรือ `If-Match: updated_at`) · mismatch → 409 ERR_STALE_DATA (กัน 2 approver ชนกัน)

### Permission re-check (PR-3/EC-03)
role/canApprove ตรวจที่ **mutation time** ไม่ใช่แค่ GET → 403 ERR_PERMISSION_REVOKED

### Multi-Tenant
ทุก endpoint บังคับ X-Tenant-Id · DB filter ผ่าน RLS

### Audit Log (FN-93)
ทุก mutation เขียน T_training_audit_log (append-only) ผ่าน FN-21 · เก็บ actor/action/detail/kind/at

### Masking (FN-94)
field Restricted (budget/มูลค่า EC/ต้นทุนต่อหัว) → API คืน `••••••` หรือ excluded เมื่อ role ไม่ unmask · **export/report ก็ mask ตาม role** (§10.2 PM edge)

---

## §2.4 API → Logic Trace (Anchor for R8)

> **Authoritative:** 03_LOGIC §3.3 · ที่นี่ summary

| API | Calls Functions | Calls Engines |
|---|---|---|
| API-01/07/13 GET list | FN (list build) | — |
| API-02 POST course | FN-01, FN-21 | — |
| API-04 PUT course | FN-02, FN-21 | — |
| API-05 publish | FN-03, FN-21 | — |
| API-06 close course | FN-04, FN-21 | — |
| API-08 POST session | FN-05, FN-21 | — |
| API-10 PUT session | FN-05(update path), FN-21 | — |
| API-11 open | FN-06, FN-21 | — |
| API-12 close session | FN-07, FN-21 | — |
| API-14 enroll | FN-08, FN-20, FN-21 | — |
| API-15 submit-approval | FN-09, FN-21 | — |
| API-16 approve | FN-10, FN-21 | — |
| API-17 reject | FN-11, FN-21 | — |
| API-18 cancel | FN-12, FN-21 | — |
| API-19 attendance | FN-13, FN-21 | — |
| API-20 result | FN-14, FN-21 | — |
| API-21 certificate | FN-15, FN-21 | — |
| API-22 expense | FN-16, FN-21 | — |
| API-23 report | FN-18, FN-19 | ENG-TRN-01 |
| API-25 gaps | FN-20 | — |
| API-27 history | FN-17 | ENG-TRN-02 |

> **R8 Check:** ทุก mutation row มี ≥1 Function ✅ (FN-21 appendAudit ทุก mutation)

---

## §2.X Cross-Module Contract (จาก BRD §12.1 Downstream Impact Map)

| Downstream | รูปแบบ | Contract | Trigger | Payload หลัก |
|---|---|---|---|---|
| Expense Claim (F101) | Event/hook (display-only) | `training.expense_hook` | กดส่ง (API-22 · confirmed + has_cost + !sent) | `{ enroll_id, course_id, emp_id, value_declared(null จน Rate Card), currency:'THB' }` — **ไม่ auto-post** |
| CSQ / โครงสร้างต้นทุน | Event | `train.enrolled_paid` (**EC** · ไม่มี AC) | อนุมัติ DOA ครบ → confirmed (API-16) | `{ ref:enroll_id, course, value_declared, currency:'THB', basis:'declared' }` (CSQ_BRIEF) |
| DOA กลาง (F-DLG-001) | Engine (external) | resolve chain `DOA-TRAIN-ENROLL-001` เมื่อ has_cost | ส่งอนุมัติ (API-15) | slots ตามตำแหน่ง (ไม่ hardcode) |
| ENG-NOTIFY | Event | 3 event (opened/confirmed/result) | state transition | ดู NTF_BRIEF / 01_UI §1.5 |
| Rate Card (F060 · pending) | Endpoint (อ่าน) | GET /rate-card/training-rate (API-28) | render EC/ต้นทุนต่อหัว | **display-only จนพร้อม (OQ-03)** |

- **compensating (ยกเลิกกลางทาง):** cancel enrollment หลังส่ง EC → **ไม่มี compensating event อัตโนมัติ** รอบนี้ (OQ-06 · policy pending) → trace 06_TESTS XT-02
- ทุกแถวที่มี data ไหล → trace 06_TESTS §6.9 (XT-01/XT-02) อย่างน้อย 1 case
