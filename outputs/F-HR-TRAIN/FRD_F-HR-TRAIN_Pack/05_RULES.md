# 05_RULES — F-HR-TRAIN · Training (อบรม)

> **Audience:** Backend developer + QA
> **Principle:** Declarative — อ่านเข้าใจโดยไม่ต้องดูโค้ด

---

## §5.1 Business Rules (BR)

### BR-01: หลักสูตร has_cost → ต้องมีงบ
- **Statement:** `has_cost=true → budget required, ≥ 0` (ห้ามว่าง)
- **Enforced by:** API-02/04 precondition + FN-01 createCourse
- **Error:** `BR_COURSE_BUDGET_REQUIRED` → 422 · **Tag:** FIXED

### BR-02: จำนวนลงทะเบียน active ≤ capacity
- **Statement:** active enrollment (status≠cancelled) count ต้อง < capacity ก่อนลงทะเบียนใหม่
- **Enforced by:** FN-08 (atomic count · row lock) · **Error:** `ERR_SESSION_CAPACITY_FULL` → 409 · **Tag:** FIXED

### BR-03: ลงทะเบียนจาก gap หรือเลือกเอง
- **Statement:** source ∈ {gap (Performance hook), manual} · gap → เก็บ gap_ref
- **Enforced by:** FN-08 · **Tag:** FIXED

### BR-04 (LOCK-01): has_cost → DOA ก่อนยืนยัน · ฟรี → ข้าม DOA
- **Statement:** has_cost=true → status='pending_doa' (ยืนยันหลังอนุมัติครบ) · has_cost=false → status='confirmed' ทันที
- **Enforced by:** FN-08, FN-09, FN-10 · **Tag:** FIXED (มติล็อก)

### BR-05 (FIX-01): บันทึกผลได้เฉพาะรอบ closed
- **Statement:** result บันทึกได้เฉพาะ session.status='closed'
- **Enforced by:** FN-14 (defense-in-depth UI+submit) · **Error:** `BR_RESULT_SESSION_NOT_CLOSED` → 422 · **Tag:** FIXED

### BR-05b (FIX-03): ต้องเช็คชื่อ attended=true ก่อนบันทึกผล
- **Statement:** result บันทึกได้เฉพาะเมื่อ attended=true · **Error:** `BR_RESULT_NOT_ATTENDED` → 422 · **Tag:** FIXED

### BR-06 (LOCK-02): ค่าอบรม = hook Expense (ไม่จ่าย/ไม่ post)
- **Statement:** ส่งมูลค่า EC เข้า Expense Claim เป็น hook display-only · **ห้าม auto-post บัญชี**
- **Enforced by:** FN-16 · **Tag:** FIXED

### BR-07 (LOCK-03): gap → หลักสูตร (hook Performance · read-only)
- **Statement:** อ่าน gap จาก Performance · **ไม่สร้าง/แก้ gap เอง** · **Enforced by:** FN-20 · **Tag:** FIXED

### BR-07C (LOCK-07): ใบรับรอง = soft ref
- **Statement:** cert = soft ref (ไม่มีเลขรัน/PDF ทางการ) · ออกได้เฉพาะ passed · **Error:** `BR_CERT_NOT_PASSED` → 422 · **Tag:** FIXED

### BR-08 (LOCK-05): audit append-only + masking ตาม role
- **Statement:** ทุก mutation → append-only log · ตัวเงิน mask ตาม role · **Enforced by:** FN-21, FN-19 · **Tag:** FIXED

### BR-09 (LOCK-04): มูลค่าอบรมอนุมัติ → CSQ EC เท่านั้น (ไม่มี AC)
- **Statement:** confirmed (has_cost) → emit `train.enrolled_paid` (EC) · **ไม่ประกาศ AC** (Expense เป็นตัวลงบัญชี)
- **Enforced by:** FN-10 · CSQ_BRIEF · **Tag:** FIXED (มติล็อก)

### BR-10: snapshot ผู้เรียน ณ ลงทะเบียน
- **Statement:** เก็บ emp_snapshot {id,name,position,dept} ณ เวลาลงทะเบียน · **Enforced by:** FN-08 · **Tag:** FIXED

### BR-11 (FIX-02): สร้างรอบได้เฉพาะหลักสูตร published
- **Statement:** สร้าง session ได้เฉพาะ course.status='published' · **Error:** `BR_SESSION_COURSE_NOT_PUBLISHED` → 422 · **Tag:** FIXED

### BR-12 (FIX-02): ส่ง Expense หลัง confirmed + กันซ้ำ
- **Statement:** ส่ง EC ได้เมื่อ status ∈ {confirmed,passed,failed} + has_cost + expense_sent=false · **Error:** `ERR_EXPENSE_ALREADY_SENT` → 409 · **Tag:** FIXED

### BR-13 (FIX-02): อนุมัติเฉพาะ role canApprove
- **Statement:** approve/reject ได้เฉพาะ role ที่ canApprove (re-check ที่ mutation) · **Error:** `ERR_NOT_APPROVER` → 403 · **Tag:** FIXED (RBAC · OQ-05)

### BR-14: สายอนุมัติ DOA (จำนวนขั้น + ตำแหน่งแต่ละขั้น)
- **Statement:** สายมาจาก DOA กลาง (F-DLG-001) · [DEFAULT] 2 ขั้น: หัวหน้าสายงาน (`role-line-manager`) → ผจก.พัฒนาบุคลากร · **ห้าม hardcode ในโค้ด feature**
- **Tag:** **CONFIGURABLE** 🤖 (DOA กลาง) · **OQ-04** (role-id ปลายทาง + drift `role-hr-ld-head` vs `role-hr-dev-head`)

### BR-15 (FIX-04): ชั่วโมงสะสม = Σ ชม.หลักสูตร เฉพาะ passed
- **Statement:** parse ชม.จาก duration (fallback 0) · sum เฉพาะ passed · **Enforced by:** ENG-TRN-02 · **Tag:** FIXED

### BR-16 (FIX-05): ต้นทุนต่อหัว = งบ ÷ ผู้ผ่าน (กันหารศูนย์)
- **Statement:** per_head = budget÷passed · passed=0 หรือฟรี → "—" · **Enforced by:** ENG-TRN-01 · **Tag:** FIXED

### BR-17: มูลค่า EC / อัตรากลาง
- **Statement:** อ่านจาก Rate Card (F060) เมื่อพร้อม · **ตอนนี้ display-only ห้าม hardcode**
- **Tag:** **DYNAMIC** 🤖 (Rate Card · **OQ-03**)

### BR-18 (reject reason): ไม่อนุมัติต้องระบุเหตุผล
- **Statement:** reject → reason required · **Error:** `ERR_REASON_REQUIRED` → 400 · **Tag:** FIXED (D15)

---

## §5.2 State Machines

### Course
```
draft ──publish──▶ published ──close──▶ closed
```
| From | To | Action | Roles | Conditions |
|---|---|---|---|---|
| draft | published | publish | hr, manager | fields ครบ |
| published | closed | close | hr, manager | confirm (soft archive) |
| published | — | (สร้างรอบ) | hr, manager | เฉพาะ published (BR-11) |

### Session
```
draft ──open──▶ open ──close──▶ closed
```
| draft | open | เปิดรับสมัคร | hr, manager | + NTF opened |
| open | closed | ปิดรอบ | hr, manager | ปลดล็อกบันทึกผล (FIX-01) |

### Enrollment (5 states)
```
create ─┬─(has_cost)─▶ pending_doa ──approve ครบ──▶ confirmed
        └─(ฟรี)───────────────────────────────────▶ confirmed
confirmed ──(closed + attended + result)──▶ passed / failed
passed ──issue cert──▶ (soft ref)
any(pending_doa/confirmed) ──cancel──▶ cancelled (soft archive)
pending_doa ──reject──▶ cancelled
```

---

## §5.3 Permission Matrix

| Role | View | Create/Edit (course·session) | Enroll/Cancel | Approve DOA | Attendance/Result/Cert | Send EC | Unmask money |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| HR L&D (hr) | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| หัวหน้า/ผจก. (manager · canApprove) | ✅ | ✅¹ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Viewer | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ (mask ••••••) |

¹ **OQ-05:** prototype ให้ non-viewer (รวมหัวหน้า) สร้าง/แก้ได้ (recruit precedent) — SEC/BA เคาะว่าหัวหน้า "สร้างได้" หรือ "อนุมัติอย่างเดียว"

---

## §5.4 Field Validation Rules

| Field | Rule | Error |
|---|---|---|
| `name` | required | ERR_VALIDATION_FAILED |
| `category` | required, ∈ HR Config (#107) | ERR_VALIDATION_FAILED |
| `instructor` / `duration` | required | ERR_VALIDATION_FAILED |
| `budget` | has_cost=true → required, ≥0 | BR_COURSE_BUDGET_REQUIRED |
| `capacity` | required, ≥1 | ERR_VALIDATION_FAILED |
| `start_date` / `location` | required | ERR_VALIDATION_FAILED |
| `end_date` | ≥ start_date (ถ้ามี) | ERR_VALIDATION_FAILED |
| `emp_id` (enroll) | required, ไม่ซ้ำ active, ≤ capacity | ERR_ALREADY_ENROLLED / ERR_SESSION_CAPACITY_FULL |
| `result` | required ∈ {pass,fail} | ERR_RESULT_REQUIRED |
| `eval_score` | 1..5 (optional) | ERR_VALIDATION_FAILED |
| `reason` (reject) | required | ERR_REASON_REQUIRED |

**Cross-field:** ต้นทุนต่อหัว = budget÷passed (computed, ไม่ input) · attended=true precede result · session closed precede attendance/result

---

## §5.5 Edge Cases (from Phase 2.5 Probing · Lane Mode `[AI-DEFAULT]`)

> Feature patterns → probes: approve/multi-step → **PR-1, PR-3** · mutation → **PR-4, PR-7** · cancel/reverse → **PR-8** · financial/capacity → **PR-9**
> ทุก `[AI-DEFAULT]` = conservative default (ล็อกไว้ก่อน) → carry เป็น OQ ให้ BA/SEC confirm

### EC-01: Concurrent approval (PR-1) `[AI-DEFAULT]`
- **Scenario:** 2 approver กด approve/reject ขั้นเดียวกันพร้อมกัน (BRD §10.2 [CA])
- **Resolution:** optimistic lock (`version`) — first commits, second → 409 `ERR_STALE_DATA`
- **Test:** TC-CC-01 (AC-26)

### EC-02: Permission mid-flight (PR-3) `[AI-DEFAULT]`
- **Scenario:** approver โดน demote ระหว่างเปิดหน้า แล้วกด approve
- **Resolution:** re-check canApprove ที่ **mutation time** → 403 `ERR_PERMISSION_REVOKED`
- **Test:** TC-PR-01 (AC-27) · เกี่ยว OQ-05 (RBAC)

### EC-03: Network failure / double-submit (PR-4/PR-7) `[AI-DEFAULT]` (บางส่วน confirmed)
- **Scenario:** กด submit/enroll/approve ซ้ำ (network ขาด/double-click)
- **Resolution:** Idempotency-Key (cache 24ชม) ทุก mutation · **sendExpense confirmed ใน HTML** ผ่าน expense_sent flag (FIX-02)
- **Test:** TC-ID-01 (AC-22/AC-28)

### EC-04: Capacity race — ที่นั่งสุดท้าย (PR-9) `[AI-DEFAULT]`
- **Scenario:** 2 คนลงทะเบียนพร้อมกันที่นั่งสุดท้าย (BRD §10.2 [CA])
- **Resolution:** atomic count ด้วย row lock บน session (`SELECT ... FOR UPDATE`) — คนแรก commit, คนสอง → 409 `ERR_SESSION_CAPACITY_FULL`
- **Test:** TC-RACE-01 (AC-29)

### EC-05: ยกเลิกหลังส่ง Expense (PR-8) `[AI-DEFAULT]` → **OQ-06**
- **Scenario:** cancel enrollment หลัง expense_sent=true (BRD §10.2 [ST] · กระทบเงิน)
- **Resolution (conservative):** cancel ได้ (soft archive) แต่ **ไม่ auto-reverse EC** · flag ให้ Finance ทบทวน · policy reverse = **OQ-06 (รอ BA/Finance)**
- **Test:** TC-CANCEL-EC-01 (XT-02)

### EC-06: master ถูกปิดใช้งานระหว่างค้างในสาย (PR-3 variant) `[AI-DEFAULT]`
- **Scenario:** ผู้เรียน/หมวด/ผู้อนุมัติถูกปิดใช้งานใน master ระหว่าง enrollment ค้าง pending_doa (BRD §10.2 [DI])
- **Resolution:** ใช้ snapshot (emp_snapshot) กันชื่อเปลี่ยนย้อนหลัง · ถ้า approver ถูกปิด → block approve + แจ้ง reassign (policy) → **OQ (flag)**
- **Test:** TC-DI-01

### EC-07: duration parse ไม่ได้ (CL) — fallback มีแล้ว
- **Scenario:** duration รูปแบบแปลก parse ชม.ไม่ได้ · **Resolution:** ENG-TRN-02 fallback 0 (FIX-04) · **Test:** TC-HRS-01

### EC-08: viewer เห็นตัวเงิน mask — export/report ก็ mask (PM)
- **Resolution:** FN-19 mask ทั้ง UI + API response + export · **Test:** TC-MASK-01 (AC-24)

---

## §5.6 Error Catalog

| Code | HTTP | Message (i18n key) | Cause |
|---|---|---|---|
| `ERR_VALIDATION_FAILED` | 400 | error.validation.failed | field validate (FN-92) |
| `ERR_RESULT_REQUIRED` | 400 | error.result.required | ไม่เลือกผล |
| `ERR_REASON_REQUIRED` | 400 | error.reason.required | reject ไม่ระบุเหตุผล |
| `ERR_NOT_AUTHENTICATED` | 401 | error.auth.unauth | no token |
| `ERR_INSUFFICIENT_ROLE` | 403 | error.auth.role | role ไม่พอ (viewer กระทำ) |
| `ERR_NOT_APPROVER` | 403 | error.auth.approver | ไม่ใช่ canApprove (BR-13/EC-02) |
| `ERR_PERMISSION_REVOKED` | 403 | error.auth.revoked | role เปลี่ยนกลางคัน (EC-02) |
| `ERR_NOT_FOUND` | 404 | error.notfound | record หาย |
| `ERR_ALREADY_ENROLLED` | 409 | error.enroll.dup | ลงซ้ำ active |
| `ERR_SESSION_CAPACITY_FULL` | 409 | error.capacity.full | เกิน capacity (BR-02/EC-04) |
| `ERR_STALE_DATA` | 409 | error.concurrency.stale | version mismatch (EC-01) |
| `ERR_EXPENSE_ALREADY_SENT` | 409 | error.expense.dup | ส่ง EC ซ้ำ (BR-12) |
| `ERR_DUPLICATE_IDEMPOTENCY_KEY` | 409 | error.idempotency.dup | key เดิม body ต่าง |
| `BR_COURSE_BUDGET_REQUIRED` | 422 | br.course.budget | BR-01 |
| `BR_SESSION_COURSE_NOT_PUBLISHED` | 422 | br.session.notpublished | BR-11 |
| `BR_SESSION_NOT_OPEN` | 422 | br.session.notopen | ลงทะเบียนตอนไม่ open |
| `BR_RESULT_SESSION_NOT_CLOSED` | 422 | br.result.notclosed | BR-05 |
| `BR_RESULT_NOT_ATTENDED` | 422 | br.result.notattended | BR-05b |
| `BR_ATTENDANCE_SESSION_NOT_CLOSED` | 422 | br.attendance.notclosed | FIX-03 |
| `BR_CERT_NOT_PASSED` | 422 | br.cert.notpassed | BR-07C |
| `BR_EXPENSE_NOT_CONFIRMED` | 422 | br.expense.notconfirmed | BR-12 |
| `BR_COURSE_NOT_PAID` | 422 | br.course.notpaid | ส่ง EC/DOA กับหลักสูตรฟรี |
| `BR_DOA_SLOTS_INCOMPLETE` | 422 | br.doa.slots | เลือกผู้อนุมัติไม่ครบ |
| `BR_NO_PENDING_STEP` | 422 | br.doa.nopending | ไม่มีขั้น pending |

---

## §5.7 Security Bible Application

> Domains: **D2, D5, D7, D9, D15, D17**

### D2 Authentication — JWT ทุก endpoint · role-based (RBAC กลาง)
### D5 Financial — budget/มูลค่า EC → audit mandatory · **ไม่ auto-post บัญชี** (LOCK-02/04) · approval (DOA) เมื่อ has_cost
### D7 PII — emp_snapshot/approver = PII → PDPA scope · no PII in logs (ref id) · encrypt at rest (column)

### D-CLASS: Data Classification (per-field ดู 04_DB §4.2/§4.6)
| Layer | Confidential (emp/gap/approver) | Restricted (budget/EC/ต้นทุนต่อหัว) |
|---|---|---|
| API response | mask ถ้าไม่ผ่าน role | excluded/mask ถ้าไม่ unmask |
| UI | `***`/snapshot | `••••••` (viewer) |
| Export/Print | excluded ถ้า role ไม่ผ่าน | mask + require Restricted Resources |
| Audit | view+mutation | view+mutation+export |

**Wire:** Policy Center → Data Classification + Restricted Resources (OQ · 00_OVERVIEW §0.8)

### D9 Audit — ทุก mutation → T_training_audit_log (append-only · 7 ปี · immutable)
### D15 Admin/Approval — approve/reject/result logged · approver identity · reason required (reject)
### D17 Multi-Tenant — RLS + X-Tenant-Id · cross-tenant forbidden

---

## §5.8 Compliance & Audit
| Requirement | Implementation |
|---|---|
| PDPA (ข้อมูลพนักงาน) | D7 encryption + retention + snapshot |
| SoD/COSO (Maker≠Approver) | HR ลงทะเบียน · หัวหน้า/ผจก. อนุมัติ |
| Audit trail | T_training_audit_log append-only |
| Access control | RBAC (OQ-05) + masking (FN-94) |
