# 06_TESTS — F-HR-TRAIN · Training (อบรม)

> **Audience:** QA
> **Coverage source:** 02_API + 03_LOGIC + 05_RULES + HTML (ข้อความจริงบนจอ verbatim)
> **Chain:** ไฟล์นี้เป็น input ให้ ai-testcase-md-generator + qa-friendly-html-generator

---

## §6.1 Acceptance Criteria (AC)

### AC-01: สร้างหลักสูตร has_cost (FN-01)
**Given** role=hr, category ∈ HR Config **When** POST /training/courses {has_cost:true, budget:30000, publish:true}
**Then** 201, status='published', code `CRS-2569-NNN` **And** audit entry สร้าง **And** toast "สร้างหลักสูตรแล้ว"

### AC-02: สร้างหลักสูตร has_cost แต่ไม่กรอกงบ (BR-01)
**Given** has_cost=true, budget ว่าง **When** submit **Then** 422 BR_COURSE_BUDGET_REQUIRED · UI toast "กรุณากรอกข้อมูลที่ไฮไลต์ให้ครบ"

### AC-03: บันทึกร่างหลักสูตร
**When** POST publish=false **Then** status='draft' · toast "บันทึกร่างแล้ว"

### AC-04: เผยแพร่/ปิดหลักสูตร (FN-03/04)
**Given** draft **When** publish **Then** status='published' · **When** close (confirm) **Then** status='closed' · toast "ปิดหลักสูตรแล้ว"

### AC-05: สร้างรอบเฉพาะหลักสูตร published (BR-11/FN-05)
**Given** course.status≠published **When** POST /training/sessions **Then** 422 BR_SESSION_COURSE_NOT_PUBLISHED · UI toast "สร้างรอบได้เฉพาะหลักสูตรที่เผยแพร่"
**And (happy)** course published → 201 status='draft' · toast "สร้างรอบอบรมแล้ว (ร่าง) — กด "เปิดรับสมัคร" จากหน้ารายละเอียด"

### AC-06: เปิดรับสมัคร → NTF (FN-06/FN-12)
**When** POST /sessions/:id/open **Then** status='open' **And** emit `train_session_opened` · toast "เปิดรับสมัครแล้ว"

### AC-07: ลงทะเบียน manual (FN-03/FN-08)
**Given** session open, ไม่เต็ม **When** POST enroll {emp_id, source:manual} (ฟรี) **Then** 201 status='confirmed' · toast "ลงทะเบียนสำเร็จ (ยืนยันแล้ว)"

### AC-08: ลงทะเบียนจาก gap (FN-10/FN-20)
**Given** course มี gap (Performance hook) **When** เปิด modal เห็น "แนะนำจากผลประเมิน (gap · Performance)" **And** เลือก gap card **Then** source='gap', gap_ref=PERF-* · toast "เลือกผู้เรียนจาก gap แล้ว"

### AC-09: ลงทะเบียน has_cost → pending_doa (BR-04/FN-08)
**Given** course has_cost **When** enroll **Then** status='pending_doa' **And** เปิด modal DOA อัตโนมัติ · ปุ่ม "ลงทะเบียน + ส่งอนุมัติ"

### AC-10: ลงทะเบียนฟรี → ข้าม DOA (BR-04)
**Given** course ฟรี **When** enroll **Then** status='confirmed' ทันที + NTF `train_enroll_confirmed` (ไม่มี Expense)

### AC-11: ส่งอนุมัติ DOA slot picker (FN-08/FN-09)
**Given** pending_doa **When** เลือกผู้อนุมัติครบทุกขั้น + "ส่งอนุมัติ" **Then** 200, approval_step สร้าง N ขั้น · toast "ส่งอนุมัติแล้ว — รอผู้อนุมัติ (DOA)"
**And** เลือกไม่ครบ → toast "กรุณาเลือกผู้อนุมัติให้ครบทุกขั้น" (BR_DOA_SLOTS_INCOMPLETE)
**And** สาย/slot **ไม่ hardcode** — มาจาก DOA กลาง (ตรวจ role ref `role-line-manager` ฯลฯ)

### AC-12: อนุมัติครบ → confirmed + EC (FN-10/BR-09)
**Given** approver=canApprove, ทุกขั้น pending **When** approve ครบ **Then** status='confirmed' + NTF `train_enroll_confirmed` + **emit CSQ `train.enrolled_paid` (EC · ไม่มี AC)** · toast "อนุมัติและยืนยันลงทะเบียนแล้ว"

### AC-13: บันทึกผลก่อนปิดรอบ = บล็อก (BR-05/FIX-01)
**Given** confirmed, session.status≠closed **When** พยายามบันทึกผล **Then** ปุ่ม disabled (tooltip "บันทึกผลได้หลังปิดรอบ") · API 422 BR_RESULT_SESSION_NOT_CLOSED

### AC-14: บันทึกผลก่อนเช็คชื่อ = บล็อก (BR-05b/FIX-03)
**Given** closed, attended≠true **When** บันทึกผล **Then** ปุ่ม disabled (tooltip "ต้องเช็คชื่อเข้าอบรมก่อน") · API 422 BR_RESULT_NOT_ATTENDED
**And (happy)** attended=true → บันทึกผล+eval 1-5 → status passed/failed + NTF `train_result` · toast "บันทึกผลและประกาศผลแล้ว"

### AC-15: ออกใบรับรอง soft ref (FN-07/BR-07C)
**Given** passed, !cert **When** ออกใบรับรอง (confirm "ออกใบรับรองผู้ผ่าน (soft ref)?") **Then** cert soft ref (ไม่มีเลขรัน/PDF) · toast "ออกใบรับรอง (soft ref) แล้ว"
**And** status≠passed → 422 BR_CERT_NOT_PASSED

### AC-16: ส่ง Expense hook + กันซ้ำ (FN-09/BR-06/BR-12)
**Given** confirmed, has_cost, !sent **When** "ส่ง Expense Claim (มูลค่า EC)" **Then** expense_sent=true · hook display-only (ไม่จ่าย/ไม่ post) · toast "ส่งไปยัง Expense Claim (hook) แล้ว — ไม่จ่าย/ไม่ post"
**And** ส่งซ้ำ → 409 ERR_EXPENSE_ALREADY_SENT · toast "ส่ง Expense Claim ไปแล้ว"

### AC-17: ยกเลิกการลงทะเบียน (FN-11/FN-91)
**When** cancel (confirm "ยกเลิกการลงทะเบียน?") **Then** status='cancelled' (soft archive) คืนที่ว่าง · toast "ยกเลิกการลงทะเบียนแล้ว"

### AC-18: รายงาน completion + ต้นทุนต่อหัว (FN-13/FIX-01/FIX-05)
**Given** enrollments (mix) **When** GET /training/report **Then** rate = passed÷recorded **นับเฉพาะรอบ closed** · ต้นทุนต่อหัว = งบ÷ผู้ผ่าน (ผู้ผ่าน=0/ฟรี → "—")
**And** viewer → ตัวเงิน mask `••••••`

### AC-19: แจ้งเตือน 3 event (FN-12)
ตรวจ emit: open→`train_session_opened` · confirmed→`train_enroll_confirmed` · result→`train_result` · **doa_* ไม่ประกาศเอง** (มาจาก DOA engine)

### AC-20: ค้นหา/filter + empty (FN-90)
**When** filter ไม่เจอ **Then** empty state "ไม่พบหลักสูตร/รอบอบรม/รายการลงทะเบียน" + ปุ่ม "ล้างตัวกรอง"

### AC-21: ปิด/ยกเลิกผ่าน confirm + soft archive (FN-91)
close course/session/cancel enroll → ผ่าน modal confirm (Pattern D) · ข้อมูลเดิมคงอยู่

### AC-22: validate + กัน double-submit (FN-92)
double-click submit → Idempotency-Key กัน INSERT ซ้ำ (200 cached, ไม่ 201 ใหม่) · busy state "กำลังบันทึก…"

### AC-23: audit append-only (FN-93)
ทุก create/แก้/อนุมัติ/บันทึกผล → T_training_audit_log entry · **UPDATE/DELETE ถูกปฏิเสธ**

### AC-24: masking ตาม role (FN-94)
viewer → งบ/ต้นทุนต่อหัว mask `••••••` ทั้ง list · report · export

### AC-25: ประวัติรายคน + ชั่วโมงสะสม (FIX-04)
**When** คลิกชื่อผู้เรียน **Then** modal "ประวัติอบรม — {name}" · ชั่วโมงสะสม = Σ ชม. **เฉพาะ passed**

### AC-26..AC-29 (Edge · Phase 2.5) — ดู §6.2 TC-CC/PR/ID/RACE

---

## §6.2 Test Case Inventory

| TC ID | Name | Type | Maps to | Priority |
|---|---|---|---|---|
| TC-01 | สร้างหลักสูตร happy | API/E2E | AC-01 | P0 |
| TC-02 | หลักสูตร has_cost ไม่กรอกงบ | negative | AC-02 | P1 |
| TC-03 | สร้างรอบ course ไม่ published | negative | AC-05 | P0 |
| TC-04 | เปิดรับสมัคร + NTF | API | AC-06 | P0 |
| TC-05 | ลงทะเบียน gap/manual | API/E2E | AC-07/08 | P0 |
| TC-06 | has_cost → DOA flow | E2E | AC-09/11/12 | P0 |
| TC-07 | ฟรี → ข้าม DOA | E2E | AC-10 | P0 |
| TC-08 | บันทึกผลก่อนปิดรอบ/เช็คชื่อ | negative | AC-13/14 | P0 |
| TC-09 | บันทึกผล + eval happy | E2E | AC-14 | P0 |
| TC-10 | ออกใบรับรอง soft ref | API | AC-15 | P1 |
| TC-11 | ส่ง Expense + กันซ้ำ | API | AC-16 | P0 |
| TC-12 | ยกเลิกลงทะเบียน | API | AC-17 | P1 |
| TC-13 | รายงาน completion/ต้นทุนต่อหัว | API | AC-18 | P1 |
| TC-14 | ประวัติ + ชม.สะสม | API | AC-25 | P1 |
| TC-CC-01 | concurrent approve (EC-01) | stress | AC-26 | P1 |
| TC-PR-01 | permission mid-flight (EC-02) | API | AC-27 | P2 |
| TC-ID-01 | idempotency double-submit (EC-03) | API | AC-22/28 | P0 |
| TC-RACE-01 | capacity ที่นั่งสุดท้าย (EC-04) | stress | AC-29 | P1 |
| TC-CANCEL-EC-01 | ยกเลิกหลังส่ง EC (EC-05/OQ-06) | integration | XT-02 | P1 |
| TC-DI-01 | approver ถูกปิดใช้งานระหว่างค้าง (EC-06) | API | — | P2 |
| TC-HRS-01 | duration parse fallback 0 (EC-07) | unit | — | P2 |
| TC-MASK-01 | mask money viewer + export (EC-08) | API/E2E | AC-24 | P1 |

---

## §6.3 Test Data Setup
- 2 tenant (isolated) · 7 employees (ผู้เรียน/ผู้อนุมัติ mix) · 4 courses (2 มีค่าใช้จ่าย · 2 ฟรี) · 2 sessions (1 open/upcoming · 1 closed/past) · 6 enrollments (ต่าง state: pending_doa · confirmed+expense · passed+cert · failed · confirmed)
- Roles: `qa_hr` (hr) · `qa_manager` (manager/canApprove) · `qa_viewer` (viewer/mask)
- Rate Card (F060) = **mock unavailable** → EC/ต้นทุนต่อหัว display-only

---

## §6.4 Definition of Done (DoD)
### Code
- [ ] ทุก AC (01–29) implement + unit tests pass · FIX-01..07 acceptance ผ่านครบ
- [ ] Integration (API+DB+Engine) · E2E happy + edge (EC-01..08)
- [ ] test coverage ≥ 80% logic layer
### Documentation
- [ ] API docs (จาก 02_API) · FRD 07_LOCKED สะท้อน final · CUBIC: ENG-TRN-01/02 registered (Phase 2)
### QA
- [ ] P0+P1 pass · ไม่มี P0/P1 bug เปิด · security (D2/D5/D7/D9/D15/D17) verified · masking (FN-94) ตรวจ export
### Deployment
- [ ] migration staging · **ไม่ผูกตัวเลข EC จน Rate Card พร้อม (OQ-03)** · monitoring completion rate · rollback plan

---

## §6.5 WebSocket Events (optional)
- `train_session_opened` → channel `tenant:<id>:training` (กลุ่มเป้าหมาย)
- `train_enroll_confirmed` → channel `tenant:<id>:user:<emp_id>`
- `train_result` → channel `tenant:<id>:user:<emp_id>`
> ปกติ in-app/email ผ่าน ENG-NOTIFY — WS optional สำหรับ dashboard realtime (My Approval inbox)

---

## §6.6 Performance Benchmarks
| Endpoint | P95 | Throughput |
|---|---|---|
| GET /training/courses (list) | < 500ms | 200/s |
| POST /enrollments | < 1000ms | 50/s |
| POST /enrollments/:id/approve | < 800ms | 100/s |
| GET /training/report | < 800ms | 100/s |

---

## §6.7 Test Environment Notes
- staging tenant `tenant-test-001` · DOA engine (F-DLG-001) = mock resolve 2 ขั้น (role-line-manager → ผจก.พัฒนาบุคลากร) — **role-id จริงรอ OQ-04**
- ENG-NOTIFY mock (assert emit) · Expense Claim (F101) mock hook (assert payload, no post) · Rate Card unavailable (display-only)

---

## §6.8 Trace: AC → Logic Coverage
| AC | API | Functions | Engines |
|---|---|---|---|
| AC-01/02/03 | API-02 | FN-01, FN-21 | — |
| AC-04 | API-05/06 | FN-03/FN-04 | — |
| AC-05 | API-08 | FN-05 | — |
| AC-06 | API-11 | FN-06 | — |
| AC-07/08/09/10 | API-14 | FN-08, FN-20 | — |
| AC-11 | API-15 | FN-09 | — |
| AC-12/26/27 | API-16 | FN-10 | — |
| AC-13/14 | API-19/20 | FN-13/FN-14 | — |
| AC-15 | API-21 | FN-15 | — |
| AC-16/28 | API-22 | FN-16 | — |
| AC-17 | API-18 | FN-12 | — |
| AC-18/24 | API-23 | FN-18, FN-19 | ENG-TRN-01 |
| AC-25 | API-27 | FN-17 | ENG-TRN-02 |
| AC-19 | API-11/16/20 | FN-06/FN-10/FN-14 | — |
| AC-23 | ทุก mutation | FN-21 | — |

> **Coverage check:** ทุก Function (FN-01..21) + Engine (ENG-TRN-01/02) ถูก trace ≥1 AC ✅

---

## §6.9 Cross-Module Test Cases (จาก BRD §12.1)

| ID | Scenario | Downstream | Expected |
|---|---|---|---|
| XT-01 | อนุมัติ DOA ครบ (has_cost) → confirmed | CSQ (EC) | emit `train.enrolled_paid` (EC) · **ไม่มี AC** · GL ไม่กระทบ |
| XT-01b | กดส่ง Expense (confirmed) | Expense Claim (F101) | รับ hook display-only · **ไม่ auto-post บัญชี** |
| XT-02 | ยกเลิก enrollment หลังส่ง EC (EC-05) | Expense/CSQ | **ไม่ auto-reverse** · flag Finance → **OQ-06** (ยืนยัน policy) |
| XT-03 | ลงทะเบียนจาก gap | Performance (F131) | อ่าน gap อย่างเดียว · Performance ไม่ถูกแก้ |
| XT-04 | render มูลค่า EC/ต้นทุนต่อหัว | Rate Card (F060) | display-only "อ้างอิง Rate Card · เชื่อมเมื่อพร้อม" · **ไม่มีตัวเลข hardcode** |

---

## §6.10 Microcopy-Aware Expected Text
> ยึด **ข้อความจริงบนจอ (verbatim)** จาก อบรม.html ก่อน fallback microcopy กลาง v9
- toast: "สร้างหลักสูตรแล้ว" · "บันทึกร่างแล้ว" · "สร้างรอบอบรมแล้ว (ร่าง) — กด "เปิดรับสมัคร" จากหน้ารายละเอียด" · "เปิดรับสมัครแล้ว" · "ลงทะเบียนสำเร็จ (ยืนยันแล้ว)" · "ส่งอนุมัติแล้ว — รอผู้อนุมัติ (DOA)" · "อนุมัติและยืนยันลงทะเบียนแล้ว" · "บันทึกผลและประกาศผลแล้ว" · "ออกใบรับรอง (soft ref) แล้ว" · "ส่งไปยัง Expense Claim (hook) แล้ว — ไม่จ่าย/ไม่ post" · "ยกเลิกการลงทะเบียนแล้ว" · "สิทธิ์อ่านอย่างเดียว"
- ปุ่ม: "สร้างหลักสูตร" · "เผยแพร่หลักสูตร" · "สร้างรอบอบรม" · "ลงทะเบียน + ส่งอนุมัติ" / "ลงทะเบียน (ยืนยัน)" · "ส่งอนุมัติ" · "บันทึกผล" · "บันทึก + ประกาศผล" · "ออกใบรับรอง" · "ส่ง Expense Claim (มูลค่า EC)"
- confirm: "ปิดหลักสูตรนี้?" · "ปิดรอบอบรมนี้?" · "ยกเลิกการลงทะเบียน?" · "ออกใบรับรองผู้ผ่าน (soft ref)?"
- tooltip disabled: "บันทึกผลได้หลังปิดรอบ" · "ต้องเช็คชื่อเข้าอบรมก่อน (แท็บผู้เรียน)"
- empty: "ไม่พบหลักสูตร" · "ไม่พบรอบอบรม" · "ไม่พบรายการลงทะเบียน" · "ยังไม่มีประวัติอบรม"
