# AI Test Cases — Training / อบรม (F-HR-TRAIN · F133)

เอกสารนี้เป็น **Test Case สำหรับ AI agent (browser-use / vision)** อ่านแล้วลงมือทดสอบบน HTML prototype `อบรม.html` จริง แล้วรายงานผลกลับ. ทุก action ผูกกับ **ข้อความ/ป้ายที่เห็นบนจอ (verbatim)** จาก HTML ต้นทาง + route จริง. Expected เช็คได้ด้วยตา.

> **ที่มา anchor:** อบรม.html (source of truth · verbatim) > FRD 01_UI > microcopy กลาง html-generator-v9.
> **Prototype demo model:** สลับบทบาทที่แถบบนขวา **"Demo · ดูในฐานะ"** — ปุ่ม `เจ้าหน้าที่อบรม` (=hr) · `หัวหน้า (ผู้อนุมัติ)` (=manager) · `ผู้ชมทั่วไป` (=viewer). ข้อมูลเป็น seed ในเครื่อง (DB คงที่ · refresh คืนค่าเริ่มต้น).
> **หมายเหตุ QA column:** ผลติ๊กเป็น localStorage runtime — tester ติ๊กตอนรัน browser (แก้ไฟล์ไม่ได้). Ledger FN↔TC ด้านล่างคือหลักฐานความครบ.

---

## Meta

| Field | Value |
|---|---|
| Feature ID | F-HR-TRAIN (F133) |
| ชื่อ | Training / อบรม (การฝึกอบรมและพัฒนาบุคลากร) |
| เวอร์ชัน | TC v1.0 (2026-09-03) · จาก FRD 1.0 (FULL) |
| App entry | เปิด `อบรม.html` → sidebar "พัฒนาบุคลากร" → `#/train/course` |
| Routes | `#/train/course` · `#/train/plan` · `#/train/result` · `#/train/report` (in-page tabs: หลักสูตร · แผน / ลงทะเบียน · ผล / ใบรับรอง · รายงาน) |
| Overlay | drawer (course/session form+view · P-08 4 sub-tabs) · modal (enroll/doa/result/history/confirm/reason) — ไม่มี route แยก · ปิดด้วย Esc/backdrop/ปุ่มปิด |
| ที่มา | FRD_F-HR-TRAIN_Pack (00/01/03/05/06/07) · BRD_อบรม.md · อบรม.html · FUNCTION_CHECKLIST (18 FN) |
| จำนวนเคส | **84 เคส** / 11 group |
| Persona seed | `hr`=เจ้าหน้าที่อบรม · `manager`=หัวหน้า (canApprove) · `viewer`=ผู้ชมทั่วไป (mask money) |
| Seed courses | CRS-2569-001 (จป. · **has_cost** งบ 30,000 · published) · 002 (Leadership · **has_cost** 50,000 · published) · 003 (การสื่อสาร · **ฟรี** · published) · 004 (Orientation · **ฟรี** · published) |
| Seed sessions | SES-2569-001 (**open**) · SES-2569-002 (**closed**) · +1 draft |
| Seed enrollments | mix: pending_doa · confirmed · passed · failed |

---

## Coverage

| group | เคส | ความสำคัญ |
|---|---|---|
| G1 หลักสูตร (Course · FN-01) | 9 | สูง |
| G2 รอบอบรม (Session · FN-02) | 7 | สูง |
| G3 ลงทะเบียน + DOA (FN-03/04/05/08/10) | 12 | สูง |
| G4 เช็คชื่อ + ผล + ใบรับรอง (FN-06/07 · FIX-01/03) | 11 | สูง |
| G5 ค่าใช้จ่าย EC + ยกเลิก (FN-09/11) | 7 | สูง |
| G6 รายงาน + ประวัติ (FN-13 · FIX-04/05) | 7 | กลาง |
| G7 กติกากลาง (FN-90..94) | 9 | กลาง |
| G8 Permission (3 persona · mask) | 6 | สูง |
| G9 Negatives — "ห้ามมี" (แทน FN-40) | 5 | สูง |
| G10 Edge cases (EC-01..08) | 6 | กลาง |
| G11 Cross-module (XT-01..04) | 4 | กลาง |
| แถม Notifications (FN-12) | 1 | กลาง |

---

## Coverage Ledger

> ★ FN cross-check (FUNCTION_CHECKLIST 18 FN): ทุก FN มี TC ≥1 · capability FIX-01..07 มี TC · negatives 5 ตัว

### FN — FUNCTION_CHECKLIST (18/18)
| FN | S-XX / BR | Requirement (ย่อ) | TC ids |
|---|---|---|---|
| FN-01 | S-01 · BR-01 | สร้างหลักสูตร (has_cost/งบ) | TC-C01, TC-C02, TC-C03, TC-C04, TC-C05, TC-C09 |
| FN-02 | S-02 · BR-11 | สร้างรอบอบรม (guard published) | TC-S01, TC-S02, TC-S03, TC-S04 |
| FN-03 | S-03 · BR-02/03 | ลงทะเบียน (gap/manual · เกิน→บล็อก) | TC-E01, TC-E02, TC-E03, TC-E10, TC-RACE01 |
| FN-04 | S-04 · BR-04 | has_cost → DOA ก่อนยืนยัน | TC-E04, TC-E05, TC-E06 |
| FN-05 | S-05 · BR-04 | ฟรี → ยืนยันทันที ข้าม DOA | TC-E07 |
| FN-06 | S-06 · BR-05 | บันทึกผล (closed+attended) + eval | TC-R04, TC-R05, TC-R06, TC-R07 |
| FN-07 | S-07 · BR-07C | ออกใบรับรอง (soft ref) | TC-R08, TC-R09 |
| FN-08 | S-04 · BR-13/14 | อนุมัติ DOA slot picker (ไม่ hardcode) | TC-E05, TC-E06, TC-E08, TC-E09, TC-PR01 |
| FN-09 | S-08 · BR-06/09/12 | ค่าอบรม → Expense hook + EC | TC-X01, TC-X02, TC-X03, TC-XT01, TC-XT02 |
| FN-10 | S-09 · BR-07 | gap → แนะนำผู้เรียน (hook read) | TC-E02, TC-N02, TC-XT04 |
| FN-11 | S-10 · BR-08 | ยกเลิกการลงทะเบียน (soft archive) | TC-X05, TC-X06, TC-CANEC01 |
| FN-12 | S-11 · BR-08 | แจ้งเตือน 3 event | TC-S05, TC-E07, TC-R06, TC-NTF01 |
| FN-13 | S-12 · BR-16 | รายงาน completion + ต้นทุนต่อหัว | TC-RP01, TC-RP02, TC-RP03, TC-RP04 |
| FN-90 | กติกากลาง | ค้นหา/filter + empty | TC-G01, TC-G02, TC-G03 |
| FN-91 | กติกากลาง | ปิด/ยกเลิก confirm + soft archive | TC-C07, TC-S06, TC-X05, TC-G04 |
| FN-92 | กติกากลาง | validate + กัน double-submit | TC-C02, TC-G05, TC-ID01 |
| FN-93 | กติกากลาง | audit append-only | TC-G06, TC-G07 |
| FN-94 | BR-08 | masking ตาม role | TC-P05, TC-P06, TC-MASK01 |

### Capability ใหม่ (FIX-01..07) — ต้องมี TC
| FIX | เนื้อหา | TC ids |
|---|---|---|
| FIX-01 | บันทึกผลเฉพาะรอบปิด (closed) + completion นับเฉพาะรอบปิด | TC-R01, TC-R04, TC-RP01 |
| FIX-02 | function guards: published (BR-11) · canApprove (BR-13) · expense-dup (BR-12) | TC-S03, TC-PR01, TC-X02 |
| FIX-03 | เช็คชื่อ (attended) ก่อนบันทึกผล + ประเมิน 1-5 | TC-R02, TC-R03, TC-R05, TC-R07 |
| FIX-04 | ประวัติรายคน + ชั่วโมงสะสม (เฉพาะ passed) | TC-H01, TC-H02, TC-HRS01 |
| FIX-05 | ต้นทุนต่อหัว = งบ÷ผู้ผ่าน (กันหารศูนย์ + mask) | TC-RP03, TC-RP04, TC-MASK01 |
| FIX-06¹ | DOA gate has_cost + slot picker | TC-E04, TC-E05, TC-E08 |
| FIX-07¹ | ต้นทุน/มูลค่า EC display-only (Rate Card pending · ห้าม hardcode) | TC-XT04, TC-N01 |

¹ FIX-06/07 = capability ที่ prompt สั่งเพิ่มครอบ (DOA gate+slot picker · Rate Card display-only) — จับคู่กับ FN-04/08 และ BR-17/LD-03.

### Business Rules (05_RULES §5.1)
| rule | cases |
|---|---|
| BR-01 has_cost→งบ required | TC-C01, TC-C02 |
| BR-02 active ≤ capacity | TC-E03, TC-E10, TC-RACE01 |
| BR-03 source gap/manual | TC-E01, TC-E02 |
| BR-04 (LOCK-01) has_cost→DOA · ฟรี→ข้าม | TC-E04, TC-E07 |
| BR-05 (FIX-01) ผลเฉพาะ closed | TC-R01, TC-R04 |
| BR-05b (FIX-03) attended ก่อนผล | TC-R02, TC-R05 |
| BR-06 (LOCK-02) EC hook ไม่จ่าย/ไม่ post | TC-X01, TC-N01, TC-XT02 |
| BR-07 (LOCK-03) gap read-only | TC-E02, TC-N02, TC-XT04 |
| BR-07C (LOCK-07) cert soft ref | TC-R08, TC-R09, TC-N04 |
| BR-08 (LOCK-05) audit + mask | TC-G06, TC-P05 |
| BR-09 (LOCK-04) EC เท่านั้น (ไม่มี AC) | TC-XT01, TC-N01 |
| BR-10 snapshot ผู้เรียน | TC-E01, TC-EC06 |
| BR-11 (FIX-02) รอบเฉพาะ published | TC-S03 |
| BR-12 (FIX-02) EC หลัง confirmed + กันซ้ำ | TC-X02, TC-X03 |
| BR-13 (FIX-02) approve เฉพาะ canApprove | TC-E08, TC-PR01, TC-P04 |
| BR-14 สาย DOA ไม่ hardcode | TC-E05, TC-E08 |
| BR-15 (FIX-04) ชม.สะสมเฉพาะ passed | TC-H01, TC-H02 |
| BR-16 (FIX-05) ต้นทุนต่อหัว กันหารศูนย์ | TC-RP03, TC-RP04 |
| BR-17 มูลค่า EC display-only (Rate Card) | TC-XT04 |
| BR-18 reject ต้องมีเหตุผล | TC-E09, TC-G08 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 concurrent approval (409 stale) | TC-EC01 (ต้อง simulate) |
| EC-02 permission mid-flight (403 revoked) | TC-PR01 (ต้อง simulate) |
| EC-03 double-submit idempotency | TC-ID01 |
| EC-04 capacity race ที่นั่งสุดท้าย | TC-RACE01 (ต้อง simulate) |
| EC-05 cancel หลังส่ง EC (ไม่ auto-reverse · OQ-06) | TC-CANEC01 |
| EC-06 master ปิดใช้งานระหว่างค้าง (snapshot กัน) | TC-EC06 |
| EC-07 duration parse fallback 0 | TC-HRS01 |
| EC-08 viewer mask money + export | TC-MASK01 |

### Error Codes (05_RULES §5.6)
| error | cases |
|---|---|
| ERR_VALIDATION_FAILED | TC-C02, TC-G05 |
| ERR_RESULT_REQUIRED | TC-R05 |
| ERR_REASON_REQUIRED | TC-E09, TC-G08 |
| ERR_INSUFFICIENT_ROLE (viewer) | TC-P01, TC-P02, TC-P03 |
| ERR_NOT_APPROVER | TC-P04, TC-PR01 |
| ERR_PERMISSION_REVOKED | TC-PR01 |
| ERR_ALREADY_ENROLLED | TC-E10 |
| ERR_SESSION_CAPACITY_FULL | TC-E03, TC-RACE01 |
| ERR_STALE_DATA | TC-EC01 |
| ERR_EXPENSE_ALREADY_SENT | TC-X03 |
| ERR_DUPLICATE_IDEMPOTENCY_KEY / idempotency | TC-ID01 |
| BR_COURSE_BUDGET_REQUIRED | TC-C02 |
| BR_SESSION_COURSE_NOT_PUBLISHED | TC-S03 |
| BR_RESULT_SESSION_NOT_CLOSED | TC-R01 |
| BR_RESULT_NOT_ATTENDED | TC-R02 |
| BR_ATTENDANCE_SESSION_NOT_CLOSED | TC-R11 |
| BR_CERT_NOT_PASSED | TC-R09 |
| BR_EXPENSE_NOT_CONFIRMED / BR_COURSE_NOT_PAID | TC-X04, TC-N01 |
| BR_DOA_SLOTS_INCOMPLETE | TC-E08 |

### Permission Matrix (role × action)
| cell | cases |
|---|---|
| hr create/edit course = allow | TC-C01, TC-P... (baseline ทุก G1-G5) |
| hr enroll/cancel = allow | TC-E01, TC-X05 |
| hr approve DOA = **deny** | TC-P04 |
| manager approve DOA = allow | TC-E08 |
| manager create/edit = allow (OQ-05) | TC-C08 |
| viewer create = deny (ปุ่มหาย/RO toast) | TC-P01 |
| viewer enroll = deny | TC-P02 |
| viewer record result = deny | TC-P03 |
| viewer unmask money = deny (mask ••••••) | TC-P05, TC-P06, TC-MASK01 |

### Cross-Module (XT — 06_TESTS §6.9)
| XT | Downstream | Case |
|---|---|---|
| XT-01 อนุมัติ DOA ครบ → EC event | CSQ (EC · ไม่มี AC) | TC-XT01 |
| XT-01b/02 ส่ง Expense (confirmed) | Expense Claim F101 (display-only) | TC-XT02 |
| XT-02 cancel หลังส่ง EC (ไม่ auto-reverse) | Expense/CSQ · OQ-06 | TC-CANEC01 |
| XT-03 ลงทะเบียนจาก gap | Performance F131 (read-only) | TC-XT03 |
| XT-04 render มูลค่า EC/ต้นทุนต่อหัว | Rate Card F060 (display-only) | TC-XT04 |

### Scope Lock (07_LOCKED §7.0) — ทุกข้อมีเคส verify
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LOCK-01 | DOA เมื่อ has_cost · ฟรี ข้าม | TC-E04, TC-E07 |
| LOCK-02 | ค่าอบรม = hook Expense (ไม่จ่าย/ไม่ post) | TC-XT02, TC-N01 |
| LOCK-03 | gap = hook Performance (อ่านอย่างเดียว) | TC-XT03, TC-N02 |
| LOCK-04 | CSQ = EC เท่านั้น (ไม่มี AC) | TC-XT01, TC-N01 |
| LOCK-05 | audit append-only + mask | TC-G06, TC-P05 |
| LOCK-06 | หมวดอ่านจาก HR Config (ไม่ CRUD) | TC-N03 |
| LOCK-07 | cert soft ref (ไม่มีเลขรัน/PDF) | TC-R08, TC-N04 |

### Cross-cutting / Events / States
| item | cases |
|---|---|
| event train_session_opened | TC-S05, TC-NTF01 |
| event train_enroll_confirmed | TC-E07, TC-NTF01 |
| event train_result | TC-R06, TC-NTF01 |
| doa_* ไม่ประกาศเอง | TC-NTF01 |
| Course state draft→published→closed | TC-C06, TC-C07 |
| Session state draft→open→closed | TC-S04, TC-S05, TC-S06 |
| Enrollment 5 states | TC-E04..E07, TC-R06, TC-X05 |
| empty state (list) | TC-G02, TC-G03, TC-H03 |
| loading/error state | TC-G09 (สังเกต) |

---

## Data Sets

### ชุด A — หลักสูตรมีค่าใช้จ่าย (valid)
| ฟิลด์ | ค่า |
|---|---|
| ชื่อหลักสูตร | การบริหารเวลา (Time Management) |
| หมวด | การสื่อสาร / Soft skills |
| ผู้สอน | อ.สมชาย ใจดี |
| ระยะเวลา | 6 ชม. |
| มีค่าใช้จ่าย (toggle) | เปิด |
| งบ | 20000 |

### ชุด B — หลักสูตรมีค่าใช้จ่าย แต่ไม่กรอกงบ (invalid)
| ฟิลด์ | ค่า |
|---|---|
| ชื่อ · หมวด · ผู้สอน · ระยะเวลา | เหมือนชุด A |
| มีค่าใช้จ่าย | เปิด |
| งบ | (เว้นว่าง) |

### ชุด C — หลักสูตรฟรี (valid)
| ฟิลด์ | ค่า |
|---|---|
| ชื่อ | ปฐมนิเทศความปลอดภัย (ฟรี) |
| หมวด | ความปลอดภัย & อาชีวอนามัย |
| ผู้สอน | อ.วิภา รักงาน |
| ระยะเวลา | 3 ชม. |
| มีค่าใช้จ่าย | ปิด |

### ชุด D — รอบอบรม (session · valid)
| ฟิลด์ | ค่า |
|---|---|
| หลักสูตร | (เลือกหลักสูตร published — เช่น การสื่อสารภายในองค์กร) |
| วันเริ่ม | 20 ต.ค. 2569 |
| วันสิ้นสุด | 20 ต.ค. 2569 |
| ช่วงเวลา | 09:00–16:00 |
| จำนวนรับ | 2 |
| สถานที่ | ห้องประชุม A ชั้น 3 |

### ชุด E — บันทึกผล + ประเมิน
| ฟิลด์ | ค่า |
|---|---|
| ผลการอบรม | ผ่าน |
| ประเมิน (1-5) | 4 |
| ความเห็น | เข้าอบรมครบ ตั้งใจดี |

### ชุด F — เหตุผลไม่อนุมัติ
| ฟิลด์ | ค่า |
|---|---|
| เหตุผล | งบประมาณรอบนี้ไม่เพียงพอ ขอเลื่อนเป็นรอบหน้า |

### ไฟล์ทดสอบ (Files)
- ไม่มี — feature นี้ไม่มี CSV import / upload ไฟล์ (`files=—` ทุกเคส)

---

## Test Cases

### G1 · หลักสูตร (Course · FN-01)

#### TC-C01 — สร้างหลักสูตรมีค่าใช้จ่าย + เผยแพร่ (happy)
- group: หลักสูตร · ความสำคัญ: สูง · trace: FN-01 / BR-01, BR-10 / AC-01 · event audit
- actor: hr
- Setup: role=hr · seed=หมวด HR Config พร้อมใช้ · files=—
- Start: OPEN `#/train/course`
- ชุดข้อมูล: A
- ผ่านเมื่อ: บันทึกได้ + toast `สร้างหลักสูตรแล้ว` + drawer ปิด + แถวใหม่โผล่ในตาราง สถานะ = published

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/train/course` | — | tab `หลักสูตร` active · ตารางหลักสูตร 7 คอลัมน์ (หลักสูตร/รหัส · หมวด · ผู้สอน · ระยะเวลา · ค่าใช้จ่าย · งบ · สถานะ) | ☐ |
| 2 | CLICK ปุ่ม `สร้างหลักสูตร` (มุมขวาบน) | — | drawer เปิด ฟอร์มหลักสูตร (section ข้อมูลหลักสูตร + ค่าใช้จ่าย) | ☐ |
| 3 | TYPE → ช่อง `ชื่อหลักสูตร` | A | ช่องแสดงค่าที่กรอก | ☐ |
| 4 | SELECT `หมวด` (search-select อ่านจาก HR Config) | A: การสื่อสาร / Soft skills | ช่องหมวดแสดงค่าที่เลือก | ☐ |
| 5 | TYPE → `ระยะเวลา` + `ผู้สอน` | A: 6 ชม. / อ.สมชาย ใจดี | ช่องแสดงค่า | ☐ |
| 6 | TOGGLE `มีค่าใช้จ่าย` เปิด | — | ช่อง `งบ` + การ์ด EC "อ้างอิง Rate Card · เชื่อมเมื่อพร้อม" ปรากฏ | ☐ |
| 7 | TYPE → `งบ` | A: 20000 | ช่องงบแสดง 20000 | ☐ |
| 8 | CLICK ปุ่ม `เผยแพร่หลักสูตร` (primary) | — | busy `กำลังบันทึก…` แล้ว drawer ปิด | ☐ |
| 9 | WAIT จน toast ปรากฏ | — | toast success `สร้างหลักสูตรแล้ว` | ☐ |
| 10 | VERIFY แถวใหม่ในตาราง | — | เห็นชื่อ "การบริหารเวลา" · รหัส `CRS-2569-NNN` · สถานะ pill = **เผยแพร่/published** · งบแสดง 20,000 | ☐ |

#### TC-C02 — has_cost แต่ไม่กรอกงบ (negative · BR-01)
- group: หลักสูตร · ความสำคัญ: สูง · trace: FN-01 / BR-01 / AC-02 / BR_COURSE_BUDGET_REQUIRED
- actor: hr
- Setup: role=hr · seed=— · files=—
- Start: OPEN `#/train/course`
- ชุดข้อมูล: B
- ผ่านเมื่อ: บันทึกไม่ผ่าน + toast เตือน + ช่องงบถูกไฮไลต์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม `สร้างหลักสูตร` | — | drawer ฟอร์มเปิด | ☐ |
| 2 | TYPE → ชื่อ/ระยะเวลา/ผู้สอน + SELECT หมวด | B | ช่องแสดงค่า | ☐ |
| 3 | TOGGLE `มีค่าใช้จ่าย` เปิด (ปล่อยงบว่าง) | — | ช่องงบปรากฏแต่ว่าง | ☐ |
| 4 | CLICK `เผยแพร่หลักสูตร` | — | ไม่ปิด drawer · toast warning `กรุณากรอกข้อมูลที่ไฮไลต์ให้ครบ` · ช่อง `งบ` มีกรอบไฮไลต์ (invalid) | ☐ |

#### TC-C03 — บันทึกร่างหลักสูตร (draft)
- group: หลักสูตร · ความสำคัญ: กลาง · trace: FN-01 / AC-03
- actor: hr
- Setup: role=hr · seed=— · files=—
- Start: OPEN `#/train/course`
- ชุดข้อมูล: A
- ผ่านเมื่อ: toast `บันทึกร่างแล้ว` + แถวใหม่สถานะ ร่าง/draft

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `สร้างหลักสูตร` → กรอกชุด A | A | ฟอร์มครบ | ☐ |
| 2 | CLICK ปุ่ม `บันทึกร่าง` (secondary) | — | drawer ปิด | ☐ |
| 3 | WAIT toast | — | toast info `บันทึกร่างแล้ว` | ☐ |
| 4 | VERIFY แถวใหม่ | — | สถานะ pill = **ร่าง/draft** | ☐ |

#### TC-C04 — สร้างหลักสูตรฟรี (has_cost off)
- group: หลักสูตร · ความสำคัญ: กลาง · trace: FN-01 / BR-04 (ฟรี)
- actor: hr
- Setup: role=hr · seed=— · files=—
- Start: OPEN `#/train/course`
- ชุดข้อมูล: C
- ผ่านเมื่อ: สร้างได้โดยไม่ต้องกรอกงบ · ตารางแสดง ค่าใช้จ่าย = ฟรี/—

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `สร้างหลักสูตร` → กรอกชุด C | C | ฟอร์มครบ | ☐ |
| 2 | VERIFY toggle `มีค่าใช้จ่าย` = ปิด | — | ไม่มีช่องงบ (ไม่บังคับงบ) | ☐ |
| 3 | CLICK `เผยแพร่หลักสูตร` → WAIT toast | — | toast `สร้างหลักสูตรแล้ว` | ☐ |
| 4 | VERIFY แถวใหม่ | — | คอลัมน์ค่าใช้จ่าย = ฟรี (หรือ —) · งบ = — | ☐ |

#### TC-C05 — แก้ไขหลักสูตร (edit + diff)
- group: หลักสูตร · ความสำคัญ: กลาง · trace: FN-01 (update) / audit
- actor: hr
- Setup: role=hr · seed=CRS-2569-003 (การสื่อสาร · published) · files=—
- Start: OPEN `#/train/course`
- ผ่านเมื่อ: toast `บันทึกการแก้ไขแล้ว` + ค่าที่แก้แสดงในตาราง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "การสื่อสารภายในองค์กร" | — | drawer view รายละเอียดหลักสูตรเปิด | ☐ |
| 2 | CLICK ปุ่ม `แก้ไข` (header) | — | drawer ฟอร์ม edit (ปุ่ม primary = `บันทึกการแก้ไข`) | ☐ |
| 3 | TYPE → `ผู้สอน` แก้เป็น | อ.ทดสอบ แก้ไข | ช่องแสดงค่าใหม่ | ☐ |
| 4 | CLICK `บันทึกการแก้ไข` → WAIT toast | — | toast `บันทึกการแก้ไขแล้ว` · ตารางแสดงผู้สอนใหม่ | ☐ |

#### TC-C06 — เผยแพร่หลักสูตรร่าง (draft→published)
- group: หลักสูตร · ความสำคัญ: กลาง · trace: state draft→published / FN-03
- actor: hr
- Setup: role=hr · seed=หลักสูตร draft ≥1 (จาก TC-C03 หรือสร้างใหม่) · files=—
- Start: OPEN `#/train/course`
- ผ่านเมื่อ: toast `เผยแพร่หลักสูตรแล้ว` + สถานะเป็น published

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวหลักสูตรสถานะ ร่าง | — | drawer view เปิด · header มีปุ่ม `แก้ไข` + `เผยแพร่หลักสูตร` | ☐ |
| 2 | CLICK ปุ่ม `เผยแพร่หลักสูตร` | — | drawer ปิด/refresh | ☐ |
| 3 | WAIT toast → VERIFY | — | toast `เผยแพร่หลักสูตรแล้ว` · สถานะแถว = published | ☐ |

#### TC-C07 — ปิดหลักสูตร (confirm + soft archive · FN-91)
- group: หลักสูตร · ความสำคัญ: กลาง · trace: FN-91 / state published→closed / AC-04
- actor: hr
- Setup: role=hr · seed=CRS-2569-004 (Orientation · published) · files=—
- Start: OPEN `#/train/course`
- ผ่านเมื่อ: ผ่าน confirm modal → toast `ปิดหลักสูตรแล้ว` · สถานะ closed · ข้อมูลเดิมคงอยู่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "ปฐมนิเทศพนักงานใหม่" | — | drawer view เปิด · header มีปุ่ม `ปิดหลักสูตร` | ☐ |
| 2 | CLICK ปุ่ม `ปิดหลักสูตร` | — | modal confirm หัวข้อ `ปิดหลักสูตรนี้?` body กล่าวถึง soft archive · ไม่เปิดรอบใหม่ได้ | ☐ |
| 3 | CLICK ปุ่มยืนยันใน modal | — | modal ปิด | ☐ |
| 4 | WAIT toast → VERIFY | — | toast `ปิดหลักสูตรแล้ว` · สถานะแถว = ปิด/closed · แถวยังอยู่ (ไม่ถูกลบจริง) | ☐ |

#### TC-C08 — manager สร้างหลักสูตรได้ (OQ-05 · permission allow)
- group: หลักสูตร · ความสำคัญ: กลาง · trace: permission (manager create) / OQ-05
- actor: manager
- Setup: role=manager · seed=— · files=—
- Start: สลับ persona → OPEN `#/train/course`
- ผ่านเมื่อ: manager เห็นปุ่มสร้างและสร้างได้ (prototype ให้ non-viewer สร้าง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถบ `หัวหน้า (ผู้อนุมัติ)` (Demo · ดูในฐานะ) | — | persona = manager (ปุ่มถูก highlight) | ☐ |
| 2 | VERIFY ปุ่ม `สร้างหลักสูตร` | — | ปุ่มยังปรากฏ (manager สร้างได้) | ☐ |
| 3 | CLICK `สร้างหลักสูตร` → กรอกชุด C → `เผยแพร่หลักสูตร` | C | toast `สร้างหลักสูตรแล้ว` (ไม่มี toast สิทธิ์อ่านอย่างเดียว) | ☐ |

#### TC-C09 — ค้นหา/filter ในตารางหลักสูตร (FN-90 baseline)
- group: หลักสูตร · ความสำคัญ: กลาง · trace: FN-90 / AC-20
- actor: hr
- Setup: role=hr · seed=4 courses · files=—
- Start: OPEN `#/train/course`
- ผ่านเมื่อ: filter ตามหมวด/สถานะ + ค้นหาแล้วตารางกรองถูก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY filter bar | — | มีช่องค้นหา + chip หมวด + chip สถานะ + `ล้างตัวกรอง` | ☐ |
| 2 | TYPE → ช่องค้นหา | Leadership | ตารางเหลือเฉพาะแถวที่ตรง (ภาวะผู้นำ) | ☐ |
| 3 | CLICK `ล้างตัวกรอง` | — | ตารางกลับมาครบ 4+ แถว | ☐ |
| 4 | CLICK chip สถานะ (เช่น เผยแพร่/published) | — | ตารางเหลือเฉพาะ published | ☐ |

---

### G2 · รอบอบรม (Session · FN-02)

#### TC-S01 — สร้างรอบอบรมจากหลักสูตร published (happy)
- group: รอบอบรม · ความสำคัญ: สูง · trace: FN-02 / BR-11 / AC-05(happy)
- actor: hr
- Setup: role=hr · seed=หลักสูตร published (CRS-2569-003) · files=—
- Start: OPEN `#/train/plan`
- ชุดข้อมูล: D
- ผ่านเมื่อ: toast `สร้างรอบอบรมแล้ว (ร่าง) — กด "เปิดรับสมัคร" จากหน้ารายละเอียด` + แถวรอบใหม่สถานะ ร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/train/plan` | — | tab `แผน / ลงทะเบียน` active · ตารางรอบอบรม | ☐ |
| 2 | CLICK ปุ่ม `สร้างรอบอบรม` | — | drawer ฟอร์มรอบ (section หลักสูตร + กำหนดการ) | ☐ |
| 3 | SELECT `หลักสูตร` (search-select เฉพาะ published) | D: การสื่อสารภายในองค์กร | ช่องแสดงหลักสูตร + note cost/free | ☐ |
| 4 | TYPE → วันเริ่ม · จำนวนรับ · สถานที่ | D | ช่องแสดงค่า (จำนวนรับ 2) | ☐ |
| 5 | CLICK ปุ่ม `สร้างรอบ (ร่าง)` / `สร้างรอบอบรม` | — | drawer ปิด | ☐ |
| 6 | WAIT toast → VERIFY | — | toast `สร้างรอบอบรมแล้ว (ร่าง) — กด "เปิดรับสมัคร" จากหน้ารายละเอียด` · แถวรอบใหม่สถานะ ร่าง | ☐ |

#### TC-S02 — จำนวนรับต้อง ≥1 (validate)
- group: รอบอบรม · ความสำคัญ: กลาง · trace: FN-02 / field validate (capacity≥1)
- actor: hr
- Setup: role=hr · seed=หลักสูตร published · files=—
- Start: OPEN `#/train/plan`
- ผ่านเมื่อ: จำนวนรับ 0/ว่าง → บันทึกไม่ผ่าน (ไฮไลต์/เตือน)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `สร้างรอบอบรม` → SELECT หลักสูตร published | — | ฟอร์มเปิด | ☐ |
| 2 | TYPE → จำนวนรับ | 0 (หรือเว้นว่าง) | — | ☐ |
| 3 | CLICK สร้างรอบ | — | ไม่บันทึก · ช่องจำนวนรับ/ที่จำเป็นถูกไฮไลต์ · toast เตือนกรอกให้ครบ | ☐ |

#### TC-S03 — สร้างรอบจากหลักสูตรไม่ published = บล็อก (negative · BR-11/FIX-02)
- group: รอบอบรม · ความสำคัญ: สูง · trace: FN-02 / BR-11 / AC-05 / BR_SESSION_COURSE_NOT_PUBLISHED
- actor: hr
- Setup: role=hr · seed=หลักสูตร draft ≥1 (สร้างจาก TC-C03) · files=—
- Start: OPEN `#/train/plan`
- ผ่านเมื่อ: หลักสูตร draft ไม่ปรากฏใน search-select **หรือ** ถ้าเลือกได้ → toast `สร้างรอบได้เฉพาะหลักสูตรที่เผยแพร่`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `สร้างรอบอบรม` → เปิด search-select หลักสูตร | — | รายการหลักสูตรให้เลือก | ☐ |
| 2 | VERIFY รายการ | — | หลักสูตรสถานะ ร่าง **ไม่อยู่ในรายการ** (มีเฉพาะ published) | ☐ |
| 3 | (ถ้าระบบยอมให้ยิง draft) VERIFY guard | — | toast `สร้างรอบได้เฉพาะหลักสูตรที่เผยแพร่` (ไม่สร้างรอบ) `⚠ ยืนยัน anchor` (path อาจถูกกันที่ UI ตั้งแต่ step 2) | ☐ |

#### TC-S04 — แก้ไขรอบอบรม (draft)
- group: รอบอบรม · ความสำคัญ: ต่ำ · trace: FN-02 (update)
- actor: hr
- Setup: role=hr · seed=รอบ draft ≥1 · files=—
- Start: OPEN `#/train/plan`
- ผ่านเมื่อ: แก้สถานที่/จำนวนรับได้ · toast `บันทึกการแก้ไขแล้ว`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวรอบ ร่าง → CLICK `แก้ไข` | — | drawer ฟอร์ม edit | ☐ |
| 2 | TYPE → สถานที่ ใหม่ | ห้องประชุม B | ช่องแสดงค่า | ☐ |
| 3 | CLICK `บันทึกการแก้ไข` → WAIT | — | toast `บันทึกการแก้ไขแล้ว` | ☐ |

#### TC-S05 — เปิดรับสมัคร (draft→open + NTF · FN-12)
- group: รอบอบรม · ความสำคัญ: สูง · trace: FN-02/FN-06 / state open / event train_session_opened / AC-06
- actor: hr
- Setup: role=hr · seed=รอบ draft ≥1 · files=—
- Start: OPEN `#/train/plan`
- ผ่านเมื่อ: toast `เปิดรับสมัครแล้ว` · สถานะ open · (NTF emit — สังเกตจาก toast/สถานะ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวรอบ ร่าง | — | drawer view รอบ (4 sub-tabs: รายละเอียด · ผู้เรียน · อนุมัติ/ค่าใช้จ่าย · ประวัติ) · header มีปุ่ม `เปิดรับสมัคร` | ☐ |
| 2 | CLICK ปุ่ม `เปิดรับสมัคร` | — | สถานะเปลี่ยน | ☐ |
| 3 | WAIT toast → VERIFY | — | toast `เปิดรับสมัครแล้ว` · สถานะรอบ = เปิดรับสมัคร/open | ☐ |

#### TC-S06 — ปิดรอบอบรม (open→closed · confirm · FN-91)
- group: รอบอบรม · ความสำคัญ: สูง · trace: FN-91 / state closed (ปลดล็อกบันทึกผล FIX-01)
- actor: hr
- Setup: role=hr · seed=SES-2569-001 (open) · files=—
- Start: OPEN `#/train/plan`
- ผ่านเมื่อ: confirm `ปิดรอบอบรมนี้?` → toast `ปิดรอบแล้ว` · สถานะ closed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวรอบ SES-2569-001 (open) | — | drawer view · header มีปุ่ม `ปิดรอบ` | ☐ |
| 2 | CLICK ปุ่ม `ปิดรอบ` | — | modal confirm หัวข้อ `ปิดรอบอบรมนี้?` (กล่าว soft archive · ไม่รับลงเพิ่ม) | ☐ |
| 3 | CLICK ยืนยัน → WAIT toast | — | toast `ปิดรอบแล้ว` · สถานะรอบ = ปิด/closed | ☐ |

#### TC-S07 — empty รอบอบรม (filter ไม่เจอ · FN-90)
- group: รอบอบรม · ความสำคัญ: ต่ำ · trace: FN-90 / empty state
- actor: hr
- Setup: role=hr · seed=— · files=—
- Start: OPEN `#/train/plan`
- ผ่านเมื่อ: ค้นหาคำที่ไม่มี → empty `ไม่พบรอบอบรม`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา (แผน) | zzzไม่มีจริง | ตารางว่าง | ☐ |
| 2 | VERIFY empty state | — | ข้อความ `ไม่พบรอบอบรม` (+ ปุ่ม `สร้างรอบอบรม` หรือ `ล้างตัวกรอง`) | ☐ |

---

### G3 · ลงทะเบียน + DOA (FN-03/04/05/08/10)

#### TC-E01 — ลงทะเบียนผู้เรียนแบบเลือกเอง หลักสูตรฟรี (manual · happy)
- group: ลงทะเบียน · ความสำคัญ: สูง · trace: FN-03 / BR-03, BR-10 / AC-07
- actor: hr
- Setup: role=hr · seed=รอบ open ของหลักสูตร**ฟรี** (SES-2569-001 ถ้าอิงหลักสูตรฟรี · ถ้าไม่ ให้สร้างรอบฟรีแล้วเปิดรับ) · files=—
- Start: OPEN `#/train/plan`
- ผ่านเมื่อ: toast `ลงทะเบียนสำเร็จ (ยืนยันแล้ว)` · ผู้เรียนโผล่ในแท็บผู้เรียน สถานะ ยืนยัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวรอบ open (หลักสูตรฟรี) | — | drawer view เปิด | ☐ |
| 2 | CLICK sub-tab `ผู้เรียน` | — | แสดงรายชื่อผู้เรียน + ปุ่มลงทะเบียน (cap bar n/2) | ☐ |
| 3 | CLICK ปุ่มลงทะเบียน (เพิ่มผู้เรียน) | — | modal ลงทะเบียน (note ฟรี · search-select ผู้เรียน) | ☐ |
| 4 | SELECT ผู้เรียนจาก search-select | อนุชา รักษ์ดี | ช่องแสดงชื่อผู้เรียน (snapshot) | ☐ |
| 5 | CLICK ปุ่ม `ลงทะเบียน (ยืนยัน)` | — | modal ปิด | ☐ |
| 6 | WAIT toast → VERIFY | — | toast `ลงทะเบียนสำเร็จ (ยืนยันแล้ว)` · แถวผู้เรียนใหม่ สถานะ ยืนยัน/confirmed · cap bar +1 | ☐ |

#### TC-E02 — ลงทะเบียนจาก gap (Performance hook · FN-10)
- group: ลงทะเบียน · ความสำคัญ: สูง · trace: FN-10 / BR-03, BR-07 / AC-08 · [AI-DEFAULT]-ref (hook read-only)
- actor: hr
- Setup: role=hr · seed=รอบ open ของหลักสูตรที่มี gap (Performance mock) · files=—
- Start: OPEN `#/train/plan`
- ผ่านเมื่อ: เลือก gap card → source=gap · toast `เลือกผู้เรียนจาก gap แล้ว` (หรือลงทะเบียนต่อได้)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวรอบ open → sub-tab `ผู้เรียน` → ปุ่มลงทะเบียน | — | modal ลงทะเบียนเปิด | ☐ |
| 2 | VERIFY ส่วน gap | — | เห็นหัวข้อ `แนะนำจากผลประเมิน` (gap · Performance) + การ์ด gap คลิกได้ `⚠ ยืนยัน anchor` (ข้อความเต็มอาจเป็น "แนะนำจากผลประเมิน (gap · Performance)") | ☐ |
| 3 | CLICK การ์ด gap ใบแรก | — | ช่องผู้เรียนถูกเติมจาก gap · toast `เลือกผู้เรียนจาก gap แล้ว` (source=gap) | ☐ |
| 4 | CLICK ปุ่มลงทะเบียน (ยืนยัน/ส่งอนุมัติ ตาม cost) → WAIT | — | ลงทะเบียนสำเร็จตามชนิดหลักสูตร | ☐ |

#### TC-E03 — ลงทะเบียนเกินจำนวนรับ = บล็อก (negative · BR-02)
- group: ลงทะเบียน · ความสำคัญ: สูง · trace: FN-03 / BR-02 / ERR_SESSION_CAPACITY_FULL
- actor: hr
- Setup: role=hr · seed=รอบ open จำนวนรับ=n ที่มีผู้เรียน active ครบ n แล้ว (เต็ม) · files=—
- Start: OPEN `#/train/plan`
- ผ่านเมื่อ: ปุ่มลงทะเบียน disabled `จำนวนเต็มแล้ว` + note จำนวนรับเต็ม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวรอบที่เต็ม → sub-tab `ผู้เรียน` | — | cap bar เต็ม (n/n) | ☐ |
| 2 | VERIFY ปุ่มลงทะเบียน | — | ปุ่ม disabled ข้อความ `จำนวนเต็มแล้ว` · note `จำนวนรับเต็มแล้ว (n/cap) — ลงทะเบียนเพิ่มไม่ได้จนกว่าจะมีการยกเลิก` | ☐ |
| 3 | (ถ้ากดได้) VERIFY guard | — | toast `จำนวนรับเต็มแล้ว — ลงทะเบียนเพิ่มไม่ได้` | ☐ |

#### TC-E04 — ลงทะเบียนหลักสูตรมีค่าใช้จ่าย → pending_doa (BR-04/DOA gate)
- group: ลงทะเบียน · ความสำคัญ: สูง · trace: FN-04 / BR-04 / LOCK-01 / FIX-06 / AC-09
- actor: hr
- Setup: role=hr · seed=รอบ open ของหลักสูตร**has_cost** (อิง CRS-2569-001/002) · files=—
- Start: OPEN `#/train/plan`
- ผ่านเมื่อ: เลือกผู้เรียน → ปุ่ม `ลงทะเบียน + ส่งอนุมัติ` · หลังกด → modal DOA เปิดอัตโนมัติ (สถานะ pending_doa)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวรอบ open (หลักสูตร has_cost) → sub-tab `ผู้เรียน` → ปุ่มลงทะเบียน | — | modal ลงทะเบียน · note ระบุ มีค่าใช้จ่าย | ☐ |
| 2 | SELECT ผู้เรียน | ธนกฤต พงษ์ศิริ | ช่องแสดงผู้เรียน | ☐ |
| 3 | VERIFY ปุ่ม footer | — | ปุ่ม primary = `ลงทะเบียน + ส่งอนุมัติ` (ไม่ใช่ "ลงทะเบียน (ยืนยัน)") | ☐ |
| 4 | CLICK `ลงทะเบียน + ส่งอนุมัติ` | — | modal ลงทะเบียนปิด → **modal ส่งอนุมัติ (DOA) เปิดอัตโนมัติ** (slot picker) · enrollment สถานะ รออนุมัติ/pending_doa | ☐ |

#### TC-E05 — ส่งอนุมัติ DOA ครบทุกขั้น (slot picker · FN-08)
- group: ลงทะเบียน · ความสำคัญ: สูง · trace: FN-08 / BR-14 / FIX-06 / AC-11
- actor: hr
- Setup: role=hr · seed=enrollment pending_doa (ต่อจาก TC-E04) · files=—
- Start: (modal DOA เปิดจาก TC-E04) หรือ OPEN `#/train/plan` → รอบ → ผู้เรียน pending → ส่งอนุมัติ
- ผ่านเมื่อ: เลือกผู้อนุมัติครบทุก slot → toast `ส่งอนุมัติแล้ว — รอผู้อนุมัติ (DOA)`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY modal DOA | — | note ระบุ "สายจาก DOA กลาง (F-DLG-001)" · มี slot ต่อขั้น (slot ตามตำแหน่ง · ไม่ hardcode คน) | ☐ |
| 2 | SELECT ผู้อนุมัติ slot ที่ 1 | (หัวหน้าสายงาน) | slot 1 แสดงชื่อผู้อนุมัติ | ☐ |
| 3 | SELECT ผู้อนุมัติ slot ที่ 2 | (ผจก.พัฒนาบุคลากร) | slot 2 แสดงชื่อผู้อนุมัติ | ☐ |
| 4 | CLICK ปุ่ม `ส่งอนุมัติ` | — | modal ปิด | ☐ |
| 5 | WAIT toast → VERIFY | — | toast `ส่งอนุมัติแล้ว — รอผู้อนุมัติ (DOA)` · enrollment สถานะ รออนุมัติ (approval timeline สร้าง 2 ขั้น) | ☐ |

#### TC-E06 — อนุมัติครบ 2 ขั้น → confirmed + EC event (XT-01/FN-08)
- group: ลงทะเบียน · ความสำคัญ: สูง · trace: FN-08 / BR-09 / AC-12 / XT-01 · event train_enroll_confirmed + CSQ
- actor: manager
- Setup: role=manager (canApprove) · seed=enrollment pending_doa ที่ส่งอนุมัติแล้ว (ผู้อนุมัติ = persona นี้) · files=—
- Start: สลับ persona → OPEN `#/train/plan` (inbox note งานรออนุมัติ)
- ผ่านเมื่อ: อนุมัติทุกขั้น → toast `อนุมัติและยืนยันลงทะเบียนแล้ว` · สถานะ confirmed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถบ `หัวหน้า (ผู้อนุมัติ)` | — | persona=manager · หน้าแผนแสดง inbox `งานรออนุมัติของฉัน · N รายการ` | ☐ |
| 2 | CLICK แถวรอบที่มี pending → sub-tab `ผู้เรียน` | — | แถวผู้เรียน pending_doa แสดงปุ่ม `อนุมัติ` / `ไม่อนุมัติ` | ☐ |
| 3 | CLICK ปุ่ม `อนุมัติ` (ขั้นที่ 1) | — | WAIT · toast `อนุมัติขั้นนี้แล้ว` (ยังไม่ครบ) | ☐ |
| 4 | (ถ้าขั้น 2 = persona เดียวกัน) CLICK `อนุมัติ` อีกครั้ง | — | ครบทุกขั้น | ☐ |
| 5 | WAIT toast → VERIFY | — | toast `อนุมัติและยืนยันลงทะเบียนแล้ว` · สถานะ enrollment = ยืนยัน/confirmed | ☐ |

#### TC-E07 — ลงทะเบียนฟรี → ยืนยันทันที ข้าม DOA (FN-05/BR-04)
- group: ลงทะเบียน · ความสำคัญ: สูง · trace: FN-05 / BR-04 / LOCK-01 / AC-10 · event train_enroll_confirmed
- actor: hr
- Setup: role=hr · seed=รอบ open ของหลักสูตร**ฟรี** · files=—
- Start: OPEN `#/train/plan`
- ผ่านเมื่อ: ปุ่ม = `ลงทะเบียน (ยืนยัน)` · หลังกด → confirmed ทันที **ไม่มี** modal DOA

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวรอบฟรี → ผู้เรียน → ปุ่มลงทะเบียน | — | modal · note ระบุ ฟรี (ไม่มีค่าใช้จ่าย) | ☐ |
| 2 | VERIFY ปุ่ม footer | — | ปุ่ม primary = `ลงทะเบียน (ยืนยัน)` (ไม่ใช่ "+ ส่งอนุมัติ") | ☐ |
| 3 | SELECT ผู้เรียน → CLICK `ลงทะเบียน (ยืนยัน)` | สุนิสา แก้วมณี | modal ปิด · **ไม่มี** modal DOA เปิดตาม | ☐ |
| 4 | WAIT toast → VERIFY | — | toast `ลงทะเบียนสำเร็จ (ยืนยันแล้ว)` · สถานะ confirmed ทันที | ☐ |

#### TC-E08 — ส่งอนุมัติแต่เลือกผู้อนุมัติไม่ครบ = บล็อก (negative · BR-13/14)
- group: ลงทะเบียน · ความสำคัญ: สูง · trace: FN-08 / BR_DOA_SLOTS_INCOMPLETE / BR-14 (slot ไม่ hardcode)
- actor: hr
- Setup: role=hr · seed=enrollment pending_doa · files=—
- Start: OPEN `#/train/plan` → รอบ → ผู้เรียน pending → ส่งอนุมัติ
- ผ่านเมื่อ: เลือกไม่ครบ → toast `กรุณาเลือกผู้อนุมัติให้ครบทุกขั้น` (ไม่ส่ง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด modal DOA (slot picker) | — | มี ≥2 slot · slot มาจากตำแหน่ง (ไม่มีชื่อคน default เติมไว้) | ☐ |
| 2 | SELECT ผู้อนุมัติเฉพาะ slot 1 (เว้น slot 2) | — | slot 2 ยังว่าง | ☐ |
| 3 | CLICK `ส่งอนุมัติ` | — | ไม่ปิด modal · toast `กรุณาเลือกผู้อนุมัติให้ครบทุกขั้น` | ☐ |

#### TC-E09 — ไม่อนุมัติ (reject) ต้องระบุเหตุผล (BR-18)
- group: ลงทะเบียน · ความสำคัญ: สูง · trace: FN-08(reject) / BR-18 / ERR_REASON_REQUIRED / A2
- actor: manager
- Setup: role=manager · seed=enrollment pending_doa ที่รออนุมัติ · files=—
- Start: สลับ persona → OPEN `#/train/plan` → รอบ → ผู้เรียน
- ผ่านเมื่อ: กดไม่อนุมัติ → modal เหตุผล · เว้นว่าง→เตือน · กรอก→ toast `ไม่อนุมัติแล้ว` · สถานะ cancelled

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม `ไม่อนุมัติ` ที่แถวผู้เรียน pending | — | modal เหตุผล (reason) เปิด | ☐ |
| 2 | CLICK ยืนยันโดยเว้นเหตุผลว่าง | — | toast `กรุณาระบุเหตุผล` (ไม่ปิด) | ☐ |
| 3 | TYPE → ช่องเหตุผล | F | ช่องแสดงเหตุผล | ☐ |
| 4 | CLICK ยืนยัน → WAIT | — | toast `ไม่อนุมัติแล้ว` · สถานะ enrollment = ยกเลิก/cancelled | ☐ |

#### TC-E10 — ลงทะเบียนซ้ำคนเดิม = บล็อก (negative · ERR_ALREADY_ENROLLED)
- group: ลงทะเบียน · ความสำคัญ: กลาง · trace: FN-03 / ERR_ALREADY_ENROLLED
- actor: hr
- Setup: role=hr · seed=รอบ open มีผู้เรียน active อยู่แล้ว 1 คน · files=—
- Start: OPEN `#/train/plan`
- ผ่านเมื่อ: เลือกคนเดิมซ้ำ → toast `ผู้เรียนคนนี้ลงทะเบียนรอบนี้แล้ว`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK รอบ open → ผู้เรียน → ปุ่มลงทะเบียน | — | modal เปิด | ☐ |
| 2 | SELECT ผู้เรียนที่ลงแล้ว (ชื่อที่มีในแท็บผู้เรียน) | (คนเดิม) | เลือกได้ | ☐ |
| 3 | CLICK ปุ่มลงทะเบียน | — | toast `ผู้เรียนคนนี้ลงทะเบียนรอบนี้แล้ว` (ไม่เพิ่มแถว) `⚠ ยืนยัน anchor` (ระบบอาจกันไม่ให้เลือกคนซ้ำใน search-select ตั้งแต่ต้น) | ☐ |

#### TC-E11 — ยกเลิกฟอร์มลงทะเบียน (dirty-check/close)
- group: ลงทะเบียน · ความสำคัญ: ต่ำ · trace: UX (ปิด modal)
- actor: hr
- Setup: role=hr · seed=รอบ open · files=—
- Start: OPEN `#/train/plan`
- ผ่านเมื่อ: ปิด modal ด้วย Esc/ปุ่มยกเลิก → ไม่มีการลงทะเบียน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด modal ลงทะเบียน → PRESS Esc | — | modal ปิด · ไม่มีผู้เรียนเพิ่ม · ไม่มี toast สำเร็จ | ☐ |
| 2 | เปิดใหม่ → CLICK ปุ่ม `ยกเลิก` | — | modal ปิด (backdrop คลิกก็ปิดได้) | ☐ |

#### TC-RACE01 — ที่นั่งสุดท้าย 2 คนพร้อมกัน (edge EC-04 · stress)
- group: ลงทะเบียน · ความสำคัญ: กลาง · trace: EC-04 / BR-02 / AC-29 / ERR_SESSION_CAPACITY_FULL `(ต้อง simulate)`
- actor: hr
- Setup: role=hr · seed=รอบ open เหลือ 1 ที่นั่ง · files=— · inject: ยิง enroll 2 request พร้อมกัน (ต้องทำที่ backend จริง — prototype กดมือทีละครั้ง)
- Start: OPEN `#/train/plan`
- ผ่านเมื่อ: คนแรกสำเร็จ · คนสองเต็ม (`จำนวนรับเต็มแล้ว`) — prototype ตรวจได้แค่ลำดับ (คนที่ 2 เจอเต็ม)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ลงทะเบียนคนที่ 1 (ที่นั่งสุดท้าย) | — | สำเร็จ · cap bar เต็ม | ☐ |
| 2 | พยายามลงทะเบียนคนที่ 2 ทันที | — | ปุ่ม disabled `จำนวนเต็มแล้ว` หรือ toast `จำนวนรับเต็มแล้ว — ลงทะเบียนเพิ่มไม่ได้` (สถานการณ์ concurrent จริงต้อง test ที่ API — mark simulate) | ☐ |

---

### G4 · เช็คชื่อ + บันทึกผล + ใบรับรอง (FN-06/07 · FIX-01/03)

#### TC-R01 — บันทึกผลก่อนปิดรอบ = บล็อก (negative · BR-05/FIX-01)
- group: ผล/ใบรับรอง · ความสำคัญ: สูง · trace: FN-06 / BR-05 / FIX-01 / AC-13 / BR_RESULT_SESSION_NOT_CLOSED
- actor: hr
- Setup: role=hr · seed=enrollment confirmed ในรอบ **open (ยังไม่ปิด)** · files=—
- Start: OPEN `#/train/result`
- ผ่านเมื่อ: ปุ่มบันทึกผล disabled + tooltip `บันทึกผลได้หลังปิดรอบอบรม (จบการอบรม)`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/train/result` | — | tab `ผล / ใบรับรอง` · ตารางผู้เรียนทุกรอบ (ยกเว้น cancelled) | ☐ |
| 2 | VERIFY แถวผู้เรียน confirmed ในรอบ open | — | ปุ่ม `บันทึกผล` **disabled** · hover/tooltip `บันทึกผลได้หลังปิดรอบอบรม (จบการอบรม)` | ☐ |
| 3 | (ถ้าพยายามกด) VERIFY | — | ไม่เปิด modal บันทึกผล · toast `บันทึกผลได้หลังปิดรอบอบรม (จบการอบรม)` | ☐ |

#### TC-R02 — บันทึกผลก่อนเช็คชื่อ = บล็อก (negative · BR-05b/FIX-03)
- group: ผล/ใบรับรอง · ความสำคัญ: สูง · trace: FN-06 / BR-05b / FIX-03 / AC-14 / BR_RESULT_NOT_ATTENDED
- actor: hr
- Setup: role=hr · seed=enrollment confirmed ในรอบ **closed** แต่ **ยังไม่เช็คชื่อ (attended≠true)** · files=—
- Start: OPEN `#/train/plan` → รอบ closed → ผู้เรียน
- ผ่านเมื่อ: ปุ่มบันทึกผล disabled + tooltip `ต้องเช็คชื่อเข้าอบรมก่อน`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK รอบ SES-2569-002 (closed) → sub-tab `ผู้เรียน` | — | แถวผู้เรียน confirmed แสดง toggle เช็คชื่อ (เข้า/ขาด) + ปุ่มบันทึกผล | ☐ |
| 2 | VERIFY ปุ่ม `บันทึกผล` (ยังไม่ toggle เข้า) | — | ปุ่ม **disabled** · tooltip `ต้องเช็คชื่อเข้าอบรมก่อน` | ☐ |

#### TC-R03 — เช็คชื่อเข้าอบรม (attendance · FIX-03)
- group: ผล/ใบรับรอง · ความสำคัญ: สูง · trace: FN-06(attendance) / FIX-03
- actor: hr
- Setup: role=hr · seed=enrollment confirmed ในรอบ closed · files=—
- Start: OPEN `#/train/plan` → รอบ closed → ผู้เรียน
- ผ่านเมื่อ: toggle เข้า → ปุ่มบันทึกผล enabled

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK รอบ closed → ผู้เรียน | — | แถวผู้เรียน confirmed | ☐ |
| 2 | TOGGLE เช็คชื่อ = เข้า (ที่แถวผู้เรียน) | — | สถานะเช็คชื่อ = เข้า | ☐ |
| 3 | VERIFY ปุ่ม `บันทึกผล` | — | ปุ่ม **enabled** (ไม่มี tooltip disabled แล้ว) | ☐ |

#### TC-R04 — บันทึกผล ผ่าน + ประเมิน (happy · FN-06/FIX-03)
- group: ผล/ใบรับรอง · ความสำคัญ: สูง · trace: FN-06 / FIX-01, FIX-03 / AC-14(happy) · event train_result
- actor: hr
- Setup: role=hr · seed=enrollment confirmed + closed + attended=true · files=—
- Start: OPEN `#/train/plan` → รอบ closed → ผู้เรียน (attended)
- ชุดข้อมูล: E
- ผ่านเมื่อ: toast `บันทึกผลและประกาศผลแล้ว` · สถานะ ผ่าน/passed + eval chip

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม `บันทึกผล` ที่แถวผู้เรียน (attended) | — | modal บันทึกผล (ผลการอบรม + ประเมิน 1-5 + ความเห็น) | ☐ |
| 2 | CLICK เลือกผล `ผ่าน` | E | ตัวเลือก ผ่าน ถูกเลือก | ☐ |
| 3 | SELECT/CLICK คะแนนประเมิน | E: 4 | คะแนน 4 ถูกเลือก | ☐ |
| 4 | TYPE → ความเห็น | E | ช่องแสดงความเห็น | ☐ |
| 5 | CLICK ปุ่ม `บันทึก + ประกาศผล` | — | modal ปิด | ☐ |
| 6 | WAIT toast → VERIFY | — | toast `บันทึกผลและประกาศผลแล้ว` · สถานะ enrollment = ผ่าน/passed · eval chip แสดง 4 | ☐ |

#### TC-R05 — บันทึกผลโดยไม่เลือกผล = เตือน (negative · ERR_RESULT_REQUIRED)
- group: ผล/ใบรับรอง · ความสำคัญ: กลาง · trace: FN-06 / ERR_RESULT_REQUIRED
- actor: hr
- Setup: role=hr · seed=enrollment confirmed+closed+attended · files=—
- Start: OPEN `#/train/plan` → รอบ closed → ผู้เรียน → บันทึกผล
- ผ่านเมื่อ: กดบันทึกโดยไม่เลือกผล → toast `กรุณาเลือกผล (ผ่าน/ไม่ผ่าน)`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด modal บันทึกผล (ไม่เลือกผล) | — | modal เปิด | ☐ |
| 2 | CLICK `บันทึก + ประกาศผล` | — | toast `กรุณาเลือกผล (ผ่าน/ไม่ผ่าน)` (ไม่ปิด modal) | ☐ |

#### TC-R06 — บันทึกผล ไม่ผ่าน (failed path + NTF)
- group: ผล/ใบรับรอง · ความสำคัญ: กลาง · trace: FN-06 / state failed / event train_result
- actor: hr
- Setup: role=hr · seed=enrollment confirmed+closed+attended · files=—
- Start: OPEN `#/train/plan` → รอบ closed → ผู้เรียน → บันทึกผล
- ผ่านเมื่อ: เลือก ไม่ผ่าน → toast `บันทึกผลและประกาศผลแล้ว` · สถานะ ไม่ผ่าน/failed · **ไม่มี**ปุ่มออกใบรับรอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด modal บันทึกผล → CLICK `ไม่ผ่าน` | — | ตัวเลือกไม่ผ่านถูกเลือก | ☐ |
| 2 | CLICK `บันทึก + ประกาศผล` → WAIT | — | toast `บันทึกผลและประกาศผลแล้ว` · สถานะ = ไม่ผ่าน/failed | ☐ |
| 3 | VERIFY action cell | — | ไม่มีปุ่ม `ออกใบรับรอง` (เฉพาะ passed เท่านั้น) | ☐ |

#### TC-R07 — ประเมิน 1-5 ไม่บังคับ (บันทึกผลได้โดยไม่ให้คะแนน)
- group: ผล/ใบรับรอง · ความสำคัญ: ต่ำ · trace: FN-06 / eval optional (FIX-03)
- actor: hr
- Setup: role=hr · seed=enrollment confirmed+closed+attended · files=—
- Start: OPEN `#/train/plan` → รอบ closed → ผู้เรียน → บันทึกผล
- ผ่านเมื่อ: เลือกผลอย่างเดียว (ไม่ให้คะแนน) → บันทึกได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด modal บันทึกผล → CLICK `ผ่าน` (ไม่แตะคะแนน) | — | ผล ผ่าน ถูกเลือก · คะแนนว่าง | ☐ |
| 2 | CLICK `บันทึก + ประกาศผล` → WAIT | — | toast `บันทึกผลและประกาศผลแล้ว` (คะแนนไม่บังคับ) | ☐ |

#### TC-R08 — ออกใบรับรอง soft ref (happy · FN-07/BR-07C)
- group: ผล/ใบรับรอง · ความสำคัญ: สูง · trace: FN-07 / BR-07C / LOCK-07 / AC-15
- actor: hr
- Setup: role=hr · seed=enrollment **passed** ที่ยังไม่ออก cert · files=—
- Start: OPEN `#/train/result`
- ผ่านเมื่อ: confirm `ออกใบรับรองผู้ผ่าน (soft ref)?` → toast `ออกใบรับรอง (soft ref) แล้ว` · chip `ออกใบรับรองแล้ว`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/train/result` → หาแถวผู้เรียน passed | — | แถวมีปุ่ม `ออกใบรับรอง` | ☐ |
| 2 | CLICK `ออกใบรับรอง` | — | modal confirm `ออกใบรับรองผู้ผ่าน (soft ref)?` (ระบุ ไม่มีเลขรัน/PDF) | ☐ |
| 3 | CLICK ยืนยัน → WAIT | — | toast `ออกใบรับรอง (soft ref) แล้ว` · คอลัมน์ใบรับรองแสดง chip `ออกใบรับรองแล้ว` (ไอคอน award) | ☐ |
| 4 | VERIFY ไม่มีเลขรัน/PDF | — | ไม่มีเลขเอกสาร/ไม่มีปุ่มดาวน์โหลด PDF (soft ref เท่านั้น) | ☐ |

#### TC-R09 — ออกใบรับรองกับคนไม่ผ่าน = บล็อก (negative · BR_CERT_NOT_PASSED)
- group: ผล/ใบรับรอง · ความสำคัญ: กลาง · trace: FN-07 / BR-07C / BR_CERT_NOT_PASSED
- actor: hr
- Setup: role=hr · seed=enrollment failed · files=—
- Start: OPEN `#/train/result`
- ผ่านเมื่อ: แถว failed **ไม่มี**ปุ่มออกใบรับรอง (หรือกดแล้ว toast `ออกใบรับรองได้เฉพาะผู้ผ่านการอบรม`)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/train/result` → หาแถว failed | — | แถว failed | ☐ |
| 2 | VERIFY action cell | — | **ไม่มี**ปุ่ม `ออกใบรับรอง` (guard ที่ UI) | ☐ |
| 3 | (ถ้ามี path กดได้) VERIFY guard | — | toast `ออกใบรับรองได้เฉพาะผู้ผ่านการอบรม` | ☐ |

#### TC-R10 — ผล/ใบรับรอง empty (FN-90)
- group: ผล/ใบรับรอง · ความสำคัญ: ต่ำ · trace: FN-90 / empty
- actor: hr
- Setup: role=hr · seed=— · files=—
- Start: OPEN `#/train/result`
- ผ่านเมื่อ: filter ไม่เจอ → empty `ไม่พบรายการลงทะเบียน`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/train/result` → TYPE ค้นหา คำที่ไม่มี | zzzไม่มี | ตารางว่าง | ☐ |
| 2 | VERIFY empty | — | `ไม่พบรายการลงทะเบียน` (หรือ `บันทึกผลได้เมื่อผู้เรียนยืนยันลงทะเบียนแล้ว`) | ☐ |

#### TC-R11 — เช็คชื่อก่อนปิดรอบ = บล็อก (negative · BR_ATTENDANCE_SESSION_NOT_CLOSED)
- group: ผล/ใบรับรอง · ความสำคัญ: กลาง · trace: FIX-03 / BR_ATTENDANCE_SESSION_NOT_CLOSED
- actor: hr
- Setup: role=hr · seed=enrollment confirmed ในรอบ **open** · files=—
- Start: OPEN `#/train/plan` → รอบ open → ผู้เรียน
- ผ่านเมื่อ: toggle เช็คชื่อ disabled/บล็อก → toast `เช็คชื่อได้หลังปิดรอบอบรม`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK รอบ open → ผู้เรียน confirmed | — | แถวผู้เรียน | ☐ |
| 2 | พยายาม TOGGLE เช็คชื่อ | — | ถูกบล็อก · toast `เช็คชื่อได้หลังปิดรอบอบรม` (เช็คชื่อได้เฉพาะรอบ closed) | ☐ |

---

### G5 · ค่าใช้จ่าย EC + ยกเลิก (FN-09/11)

#### TC-X01 — ส่ง Expense Claim (hook display-only · happy · FN-09)
- group: ค่าใช้จ่าย · ความสำคัญ: สูง · trace: FN-09 / BR-06, BR-12 / AC-16 / XT-01b
- actor: hr
- Setup: role=hr · seed=enrollment **confirmed** ของหลักสูตร **has_cost** ที่ยังไม่ส่ง EC (expense_sent=false) · files=—
- Start: OPEN `#/train/plan` → รอบ has_cost → sub-tab `อนุมัติ / ค่าใช้จ่าย`
- ผ่านเมื่อ: toast `ส่งไปยัง Expense Claim (hook) แล้ว — ไม่จ่าย/ไม่ post`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวรอบ (หลักสูตร has_cost) → sub-tab `อนุมัติ / ค่าใช้จ่าย` | — | EC block (Rate Card ref display-only) + ปุ่ม `ส่ง Expense Claim (มูลค่า EC)` | ☐ |
| 2 | VERIFY มูลค่า EC | — | แสดงแบบ display-only "อ้างอิง Rate Card · เชื่อมเมื่อพร้อม" (ไม่มีตัวเลข hardcode) | ☐ |
| 3 | CLICK ปุ่ม `ส่ง Expense Claim (มูลค่า EC)` | — | WAIT | ☐ |
| 4 | WAIT toast → VERIFY | — | toast `ส่งไปยัง Expense Claim (hook) แล้ว — ไม่จ่าย/ไม่ post` · สถานะ expense = ส่งแล้ว | ☐ |

#### TC-X02 — ส่ง EC ก่อน confirmed = บล็อก (negative · BR-12)
- group: ค่าใช้จ่าย · ความสำคัญ: กลาง · trace: FN-09 / BR-12 / FIX-02 / BR_EXPENSE_NOT_CONFIRMED
- actor: hr
- Setup: role=hr · seed=enrollment **pending_doa** ของหลักสูตร has_cost · files=—
- Start: OPEN `#/train/plan` → รอบ → `อนุมัติ / ค่าใช้จ่าย`
- ผ่านเมื่อ: ปุ่มส่ง EC disabled/บล็อก → toast `ส่งได้หลังการลงทะเบียนได้รับอนุมัติ`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK รอบ has_cost ที่มี enrollment pending_doa → `อนุมัติ / ค่าใช้จ่าย` | — | ปุ่มส่ง EC | ☐ |
| 2 | พยายาม CLICK `ส่ง Expense Claim (มูลค่า EC)` | — | ถูกบล็อก · toast `ส่งได้หลังการลงทะเบียนได้รับอนุมัติ` (ต้อง confirmed ก่อน) | ☐ |

#### TC-X03 — ส่ง EC ซ้ำ = บล็อก (negative · ERR_EXPENSE_ALREADY_SENT)
- group: ค่าใช้จ่าย · ความสำคัญ: สูง · trace: FN-09 / BR-12 / AC-16 / ERR_EXPENSE_ALREADY_SENT
- actor: hr
- Setup: role=hr · seed=enrollment confirmed has_cost ที่ **ส่ง EC ไปแล้ว** (expense_sent=true) · files=—
- Start: OPEN `#/train/plan` → รอบ → `อนุมัติ / ค่าใช้จ่าย`
- ผ่านเมื่อ: กดส่งซ้ำ → toast `ส่ง Expense Claim ไปแล้ว` (ไม่ส่งใหม่)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK รอบ → `อนุมัติ / ค่าใช้จ่าย` (enrollment ส่ง EC แล้ว) | — | แสดงสถานะส่งแล้ว | ☐ |
| 2 | CLICK ปุ่มส่ง EC ซ้ำ (ถ้ายังกดได้) | — | toast `ส่ง Expense Claim ไปแล้ว` (กันซ้ำ · ไม่เกิด record ใหม่) | ☐ |

#### TC-X04 — ส่ง EC กับหลักสูตรฟรี = ไม่มีปุ่ม/บล็อก (negative · BR_COURSE_NOT_PAID)
- group: ค่าใช้จ่าย · ความสำคัญ: กลาง · trace: FN-09 / BR_COURSE_NOT_PAID
- actor: hr
- Setup: role=hr · seed=รอบของหลักสูตร **ฟรี** มี enrollment confirmed · files=—
- Start: OPEN `#/train/plan` → รอบฟรี → `อนุมัติ / ค่าใช้จ่าย`
- ผ่านเมื่อ: EC block แสดง "ข้าม/ไม่มีค่าใช้จ่าย" · **ไม่มี**ปุ่มส่ง Expense

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK รอบฟรี → sub-tab `อนุมัติ / ค่าใช้จ่าย` | — | ระบุ ฟรี (ข้าม EC) | ☐ |
| 2 | VERIFY | — | **ไม่มี**ปุ่ม `ส่ง Expense Claim (มูลค่า EC)` (หลักสูตรฟรีไม่มี EC) | ☐ |

#### TC-X05 — ยกเลิกการลงทะเบียน (soft archive คืนที่ · FN-11/FN-91)
- group: ค่าใช้จ่าย · ความสำคัญ: สูง · trace: FN-11 / BR-08 / AC-17 · state cancelled
- actor: hr
- Setup: role=hr · seed=enrollment confirmed (pending_doa/confirmed) ในรอบ open, cap bar n/2 · files=—
- Start: OPEN `#/train/plan` → รอบ open → ผู้เรียน
- ผ่านเมื่อ: confirm `ยกเลิกการลงทะเบียน?` → toast `ยกเลิกการลงทะเบียนแล้ว` · cap bar ลด 1 (คืนที่ว่าง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK รอบ open → sub-tab `ผู้เรียน` → VERIFY+จด cap bar | — | บันทึก cap ปัจจุบัน (เช่น 2/2) อ้างใน step หลัง | ☐ |
| 2 | CLICK ปุ่มยกเลิก (ท้ายแถวผู้เรียน) | — | modal confirm `ยกเลิกการลงทะเบียน?` (ระบุ soft archive · คืนที่ว่าง · ประวัติยังอยู่) | ☐ |
| 3 | CLICK ยืนยัน → WAIT | — | toast `ยกเลิกการลงทะเบียนแล้ว` | ☐ |
| 4 | VERIFY cap bar | — | จำนวนผู้เรียนลด 1 เทียบค่าที่จดใน step 1 (เช่น 2/2 → 1/2) · แถวผู้เรียนเป็น ยกเลิก (ประวัติคงอยู่ ไม่หายจริง) | ☐ |

#### TC-X06 — ยกเลิกแล้วรายการหายจาก result list (ยกเว้น cancelled)
- group: ค่าใช้จ่าย · ความสำคัญ: ต่ำ · trace: FN-11 / list filter (result ไม่แสดง cancelled)
- actor: hr
- Setup: role=hr · seed=enrollment ที่เพิ่งยกเลิก (จาก TC-X05) · files=—
- Start: OPEN `#/train/result`
- ผ่านเมื่อ: รายการ cancelled ไม่อยู่ในตาราง ผล/ใบรับรอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/train/result` → ค้นหาชื่อผู้เรียนที่ยกเลิก | (ชื่อผู้เรียน) | ไม่พบในตาราง (result list ยกเว้น cancelled) | ☐ |

#### TC-CANEC01 — ยกเลิกหลังส่ง EC = ไม่ auto-reverse (edge EC-05/XT-02 · OQ-06)
- group: ค่าใช้จ่าย · ความสำคัญ: กลาง · trace: FN-11 / EC-05 / XT-02 / LD-04 · `[AI-DEFAULT]` (OQ-06)
- actor: hr
- Setup: role=hr · seed=enrollment confirmed has_cost ที่ **ส่ง EC แล้ว** (expense_sent=true) · files=—
- Start: OPEN `#/train/plan` → รอบ → ผู้เรียน
- ผ่านเมื่อ: cancel ได้ (soft archive) แต่สถานะ EC ที่ส่งไปแล้ว **ไม่ถูกถอนอัตโนมัติ** (conservative default — ผลนี้ AI ตัดสินแทน BA · fail อาจแปลว่า default ผิด)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จด สถานะ EC = ส่งแล้ว | — | บันทึก expense_sent=true อ้างใน step หลัง | ☐ |
| 2 | CLICK ยกเลิกการลงทะเบียน → ยืนยัน | — | toast `ยกเลิกการลงทะเบียนแล้ว` · สถานะ cancelled | ☐ |
| 3 | VERIFY สถานะ EC หลังยกเลิก | — | EC ที่ส่งไปแล้ว **ยังคงส่งแล้ว** (ไม่ถูก reverse อัตโนมัติ) เทียบกับ step 1 · (policy reverse = OQ-06 รอ BA/Finance) `[AI-DEFAULT]` | ☐ |

---

### G6 · รายงาน + ประวัติ (FN-13 · FIX-04/05)

#### TC-RP01 — รายงาน completion rate นับเฉพาะรอบ closed (FN-13/FIX-01)
- group: รายงาน · ความสำคัญ: กลาง · trace: FN-13 / BR-16, FIX-01 / AC-18
- actor: hr
- Setup: role=hr · seed=enrollments mix (passed/failed จากรอบ closed + confirmed จากรอบ open) · files=—
- Start: OPEN `#/train/report`
- ผ่านเมื่อ: stat cards + funnel แสดง · rate = passed÷recorded (นับเฉพาะรอบ closed) · มี note ระบุกติกา

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/train/report` | — | tab `รายงาน` · 5 stat cards (หลักสูตร/รอบ/ลงทะเบียน/ผ่าน/อัตราผ่าน) | ☐ |
| 2 | VERIFY funnel completion | — | funnel completion rate ต่อหลักสูตร | ☐ |
| 3 | VERIFY note กติกา | — | note ระบุ "นับเฉพาะผลจากรอบ closed" (+ Rate Card display-only · กันหารศูนย์) | ☐ |

#### TC-RP02 — filter รายงานตามหลักสูตร
- group: รายงาน · ความสำคัญ: ต่ำ · trace: FN-13 / filter
- actor: hr
- Setup: role=hr · seed=หลาย course · files=—
- Start: OPEN `#/train/report`
- ผ่านเมื่อ: เลือกหลักสูตร → widget อัปเดตเฉพาะหลักสูตรนั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จด ค่า stat cards (ทั้งหมด) | — | บันทึกค่าเริ่มต้น อ้างใน step หลัง | ☐ |
| 2 | SELECT/CLICK filter หลักสูตร (เลือก 1 หลักสูตร) | (เช่น Leadership) | widget/funnel อัปเดตเฉพาะหลักสูตรที่เลือก (ต่างจากค่าที่จดใน step 1) | ☐ |

#### TC-RP03 — ต้นทุนต่อหัว กันหารศูนย์ (FIX-05/BR-16)
- group: รายงาน · ความสำคัญ: กลาง · trace: FN-13 / FIX-05 / BR-16 / AC-18
- actor: hr
- Setup: role=hr · seed=หลักสูตร has_cost ที่ผู้ผ่าน=0 + หลักสูตรฟรี · files=—
- Start: OPEN `#/train/report`
- ผ่านเมื่อ: cost-per-head cards แสดง งบ · ผู้ผ่าน · ต้นทุนต่อหัว · ผู้ผ่าน=0 หรือฟรี → `—`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY cost-per-head cards | — | แต่ละหลักสูตรแสดง งบ + ผู้ผ่าน + ต้นทุนต่อหัว | ☐ |
| 2 | VERIFY หลักสูตรผู้ผ่าน=0 หรือฟรี | — | ต้นทุนต่อหัว = `—` (กันหารศูนย์ · ไม่ใช่ 0 หรือ error) | ☐ |
| 3 | VERIFY หลักสูตร has_cost ที่มีผู้ผ่าน>0 | — | ต้นทุนต่อหัว = งบ÷ผู้ผ่าน (ตัวเลขปกติ hr เห็นชัด) | ☐ |

#### TC-RP04 — Export CSV = ต่อ dev (stub)
- group: รายงาน · ความสำคัญ: ต่ำ · trace: FN-13 / Export (Phase 2)
- actor: hr
- Setup: role=hr · seed=— · files=—
- Start: OPEN `#/train/report`
- ผ่านเมื่อ: กด Export → toast `ส่งออกรายงาน (CSV) — ต่อ dev` (ไม่ดาวน์โหลดจริง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม `Export CSV` | — | toast `ส่งออกรายงาน (CSV) — ต่อ dev` (stub · ไม่มีไฟล์ออกจริง) | ☐ |

#### TC-H01 — ประวัติอบรมรายคน + ชั่วโมงสะสม (FIX-04/BR-15)
- group: ประวัติ · ความสำคัญ: กลาง · trace: FIX-04 / FN(history) / BR-15 / AC-25
- actor: hr
- Setup: role=hr · seed=ผู้เรียนที่มี ≥1 รายการ passed (มีชม.สะสม) · files=—
- Start: OPEN `#/train/result` (หรือ plan → ผู้เรียน)
- ผ่านเมื่อ: modal `ประวัติอบรม — {name}` · ชั่วโมงสะสม = Σ ชม.เฉพาะ passed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ชื่อผู้เรียน (ในตาราง result หรือแท็บผู้เรียน) | — | modal ประวัติเปิด หัวข้อ `ประวัติอบรม — {ชื่อ}` | ☐ |
| 2 | VERIFY summary | — | แสดง ชั่วโมงสะสม + จำนวนหลักสูตรที่ผ่าน + รายการทั้งหมด | ☐ |
| 3 | VERIFY list รายการ | — | ตารางรายการอบรม (หลักสูตร · รหัสรอบ · วันที่ · สถานะ · ผล · eval · cert · +ชม.นับสะสม) | ☐ |
| 4 | VERIFY กติกาชั่วโมง | — | note ระบุ "ชม.สะสมนับเฉพาะผ่าน" · รายการ failed ไม่บวกชั่วโมง | ☐ |

#### TC-H02 — ชั่วโมงสะสมไม่รวม failed (FIX-04)
- group: ประวัติ · ความสำคัญ: กลาง · trace: FIX-04 / BR-15
- actor: hr
- Setup: role=hr · seed=ผู้เรียนที่มีทั้ง passed และ failed · files=—
- Start: OPEN `#/train/result` → คลิกชื่อผู้เรียน
- ผ่านเมื่อ: ชั่วโมงสะสม = Σ ชม.ของ passed เท่านั้น (รายการ failed แสดงแต่ +ชม.=0/ไม่นับ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด modal ประวัติของผู้เรียน (มี passed+failed) → VERIFY+จด ชม.สะสม | — | บันทึกยอดชม.สะสมที่แสดง | ☐ |
| 2 | VERIFY แถว failed ในรายการ | — | แถว failed แสดงแต่คอลัมน์ +ชม.นับสะสม = 0/ไม่บวก (ยอดรวมตรงกับ Σ passed ที่จด) | ☐ |

#### TC-H03 — ประวัติว่าง (empty)
- group: ประวัติ · ความสำคัญ: ต่ำ · trace: FN-90 / empty (`ยังไม่มีประวัติอบรม`)
- actor: hr
- Setup: role=hr · seed=ผู้เรียนที่ยังไม่มีรายการอบรม (ถ้าเข้าถึงได้) · files=—
- Start: OPEN `#/train/result`
- ผ่านเมื่อ: modal ประวัติของคนไม่มีรายการ → `ยังไม่มีประวัติอบรม`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด modal ประวัติของผู้เรียนที่ไม่มีรายการ | — | empty `ยังไม่มีประวัติอบรม` `⚠ ยืนยัน anchor` (prototype seed อาจไม่มีคนว่าง — ถ้าไม่มีให้ mark N/A) | ☐ |

---

### G7 · กติกากลาง (FN-90..94)

#### TC-G01 — ค้นหาหลักสูตร (FN-90)
- group: กติกากลาง · ความสำคัญ: กลาง · trace: FN-90 / AC-20
- actor: hr
- Setup: role=hr · seed=4 courses · files=—
- Start: OPEN `#/train/course`
- ผ่านเมื่อ: พิมพ์คำค้น → ตารางกรอง · ล้างตัวกรอง → กลับครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา | ความปลอดภัย | ตารางเหลือเฉพาะ จป. | ☐ |
| 2 | CLICK `ล้างตัวกรอง` | — | ตารางครบเหมือนเดิม | ☐ |

#### TC-G02 — empty state หลักสูตร (filter ไม่เจอ · FN-90)
- group: กติกากลาง · ความสำคัญ: กลาง · trace: FN-90 / empty
- actor: hr
- Setup: role=hr · seed=— · files=—
- Start: OPEN `#/train/course`
- ผ่านเมื่อ: ค้นหาคำไม่มี → `ไม่พบหลักสูตร` + `ลองปรับคำค้นหรือล้างตัวกรอง แล้วลองอีกครั้ง` + ปุ่ม `ล้างตัวกรอง`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา | zzzไม่มีจริง | ตารางว่าง | ☐ |
| 2 | VERIFY empty | — | `ไม่พบหลักสูตร` + คำอธิบาย + ปุ่ม `ล้างตัวกรอง` | ☐ |
| 3 | CLICK `ล้างตัวกรอง` | — | ตารางกลับมา | ☐ |

#### TC-G03 — filter สถานะทุกค่า (FN-90)
- group: กติกากลาง · ความสำคัญ: ต่ำ · trace: FN-90 / filter enum
- actor: hr
- Setup: role=hr · seed=courses หลายสถานะ · files=—
- Start: OPEN `#/train/course`
- ผ่านเมื่อ: เลือก chip สถานะแต่ละค่า (ร่าง/เผยแพร่/ปิด) → ตารางกรองถูก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK chip สถานะ `เผยแพร่/published` | — | เหลือเฉพาะ published | ☐ |
| 2 | CLICK chip สถานะ `ร่าง/draft` | — | เหลือเฉพาะ draft (ถ้ามี) | ☐ |
| 3 | CLICK chip `ทั้งหมด` (reset) | — | ตารางครบ | ☐ |

#### TC-G04 — ปิด/ยกเลิกทุกจุดผ่าน confirm (FN-91)
- group: กติกากลาง · ความสำคัญ: กลาง · trace: FN-91 / AC-21 (Pattern D confirm)
- actor: hr
- Setup: role=hr · seed=course published + session open + enrollment · files=—
- Start: OPEN `#/train/course` / `#/train/plan`
- ผ่านเมื่อ: ปิดหลักสูตร/ปิดรอบ/ยกเลิกลงทะเบียน ทุกจุด **ผ่าน modal confirm** ก่อน · ข้อมูลเดิมคงอยู่ (soft archive)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปิดหลักสูตร | — | modal confirm `ปิดหลักสูตรนี้?` (ไม่ทำทันที) | ☐ |
| 2 | CLICK ปิดรอบ | — | modal confirm `ปิดรอบอบรมนี้?` | ☐ |
| 3 | CLICK ยกเลิกการลงทะเบียน | — | modal confirm `ยกเลิกการลงทะเบียน?` | ☐ |
| 4 | VERIFY หลังยืนยันจุดใดจุดหนึ่ง | — | record ยัง(soft archive)อยู่ในระบบ ไม่ถูกลบจริง | ☐ |

#### TC-G05 — validate ฟอร์ม (required · FN-92)
- group: กติกากลาง · ความสำคัญ: กลาง · trace: FN-92 / AC-22 / ERR_VALIDATION_FAILED
- actor: hr
- Setup: role=hr · seed=— · files=—
- Start: OPEN `#/train/course`
- ผ่านเมื่อ: เว้นช่อง required (ชื่อ/ระยะเวลา/ผู้สอน/หมวด) → เตือน + ไฮไลต์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `สร้างหลักสูตร` → CLICK `เผยแพร่หลักสูตร` (ฟอร์มว่าง) | — | ไม่บันทึก · toast `กรุณากรอกข้อมูลที่ไฮไลต์ให้ครบ` (หรือ `กรุณาเลือกหมวดหลักสูตร`) · ช่อง required ถูกไฮไลต์ | ☐ |
| 2 | กรอกครบยกเว้นหมวด → CLICK เผยแพร่ | — | toast `กรุณาเลือกหมวดหลักสูตร` | ☐ |

#### TC-G06 — audit ประวัติ append-only แสดงในรายละเอียด (FN-93)
- group: กติกากลาง · ความสำคัญ: กลาง · trace: FN-93 / BR-08 / AC-23
- actor: hr
- Setup: role=hr · seed=course/session ที่มี mutation · files=—
- Start: OPEN `#/train/course` → รายละเอียด (หรือ session view → ประวัติ)
- ผ่านเมื่อ: sub-section/แท็บ `ประวัติ` แสดง timeline ทุก create/แก้/อนุมัติ/บันทึกผล (append เรียงเวลา)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวหลักสูตร → VERIFY section ประวัติ | — | timeline รายการ action (สร้าง/แก้ไข/เผยแพร่ ฯลฯ) พร้อมผู้ทำ + เวลา | ☐ |
| 2 | ทำ mutation ใหม่ (แก้ไขผู้สอน) → กลับดูประวัติ | — | มีรายการใหม่ **เพิ่มต่อท้าย** (ของเดิมไม่ถูกลบ/แก้ = append-only) | ☐ |

#### TC-G07 — session ประวัติ (sub-tab ประวัติ · FN-93)
- group: กติกากลาง · ความสำคัญ: ต่ำ · trace: FN-93 / audit
- actor: hr
- Setup: role=hr · seed=session ที่มี event (open/enroll/approve) · files=—
- Start: OPEN `#/train/plan` → รอบ → sub-tab `ประวัติ`
- ผ่านเมื่อ: timeline แสดง event ของรอบเรียงเวลา

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK รอบ → sub-tab `ประวัติ` | — | timeline append-only ของรอบ (เปิดรับ/ลงทะเบียน/อนุมัติ ฯลฯ) | ☐ |

#### TC-G08 — reject reason required (FN-92 · BR-18 recap)
- group: กติกากลาง · ความสำคัญ: กลาง · trace: FN-92 / BR-18 / ERR_REASON_REQUIRED
- actor: manager
- Setup: role=manager · seed=enrollment pending_doa · files=—
- Start: สลับ persona → OPEN `#/train/plan` → รอบ → ผู้เรียน
- ผ่านเมื่อ: ไม่อนุมัติโดยเว้นเหตุผล → toast `กรุณาระบุเหตุผล`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `ไม่อนุมัติ` → เว้นเหตุผล → ยืนยัน | — | toast `กรุณาระบุเหตุผล` (บังคับกรอก) | ☐ |

#### TC-G09 — double-submit กัน (busy state · FN-92)
- group: กติกากลาง · ความสำคัญ: กลาง · trace: FN-92 / EC-03 / idempotency (busy)
- actor: hr
- Setup: role=hr · seed=— · files=—
- Start: OPEN `#/train/course`
- ผ่านเมื่อ: กดปุ่มบันทึกรัว → ปุ่มขึ้น `กำลังบันทึก…` disabled ระหว่างส่ง (ไม่เกิด record ซ้ำ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `สร้างหลักสูตร` → กรอกชุด A → CLICK `เผยแพร่หลักสูตร` เร็ว ๆ 2 ครั้ง | A | ปุ่มเปลี่ยนเป็น `กำลังบันทึก…` + disabled หลังคลิกแรก · เกิดหลักสูตรใหม่ **1 แถว** (ไม่ซ้ำ) | ☐ |

---

### G8 · Permission (3 persona · mask money)

#### TC-P01 — viewer สร้างหลักสูตรไม่ได้ (permission deny)
- group: Permission · ความสำคัญ: สูง · trace: permission (viewer create=deny) / ERR_INSUFFICIENT_ROLE
- actor: viewer
- Setup: role=viewer · seed=— · files=—
- Start: สลับ persona `ผู้ชมทั่วไป` → OPEN `#/train/course`
- ผ่านเมื่อ: ไม่มีปุ่มสร้าง (หรือกดแล้ว toast `สิทธิ์อ่านอย่างเดียว`)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถบ `ผู้ชมทั่วไป` (Demo · ดูในฐานะ) | — | persona=viewer | ☐ |
| 2 | VERIFY ปุ่ม `สร้างหลักสูตร` | — | ปุ่ม**ไม่ปรากฏ** (viewer อ่านอย่างเดียว) | ☐ |
| 3 | (ถ้ามี action อื่นที่ viewer กด) VERIFY | — | toast `สิทธิ์อ่านอย่างเดียว` (warning) | ☐ |

#### TC-P02 — viewer ลงทะเบียนไม่ได้ (permission deny)
- group: Permission · ความสำคัญ: สูง · trace: permission (viewer enroll=deny)
- actor: viewer
- Setup: role=viewer · seed=รอบ open · files=—
- Start: สลับ persona → OPEN `#/train/plan`
- ผ่านเมื่อ: ไม่มีปุ่มสร้างรอบ/ลงทะเบียน (RO)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หน้าแผน (viewer) | — | ไม่มีปุ่ม `สร้างรอบอบรม` | ☐ |
| 2 | CLICK รอบ → sub-tab `ผู้เรียน` | — | ไม่มีปุ่มลงทะเบียน / ปุ่ม action ถูกซ่อน (RO) | ☐ |

#### TC-P03 — viewer บันทึกผลไม่ได้ (permission deny)
- group: Permission · ความสำคัญ: กลาง · trace: permission (viewer result=deny)
- actor: viewer
- Setup: role=viewer · seed=รอบ closed มีผู้เรียน · files=—
- Start: สลับ persona → OPEN `#/train/result`
- ผ่านเมื่อ: ไม่มีปุ่มบันทึกผล/ออกใบรับรอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตาราง result (viewer) | — | คอลัมน์จัดการไม่มีปุ่ม `บันทึกผล`/`ออกใบรับรอง` (RO) | ☐ |

#### TC-P04 — hr อนุมัติ DOA ไม่ได้ (SoD · permission deny)
- group: Permission · ความสำคัญ: สูง · trace: permission (hr approve=deny · SoD) / BR-13 / ERR_NOT_APPROVER
- actor: hr
- Setup: role=hr · seed=enrollment pending_doa · files=—
- Start: OPEN `#/train/plan` → รอบ → ผู้เรียน pending
- ผ่านเมื่อ: hr ไม่เห็น/กดปุ่มอนุมัติไม่ได้ (เฉพาะ manager/canApprove) → toast `เฉพาะผู้อนุมัติ (DOA) เท่านั้น`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (persona=hr) CLICK รอบ has_cost pending → ผู้เรียน pending_doa | — | แถวผู้เรียน pending | ☐ |
| 2 | VERIFY ปุ่มอนุมัติ | — | hr ไม่เห็นปุ่ม `อนุมัติ` (เห็นแต่ ยกเลิก) — SoD Maker≠Approver | ☐ |
| 3 | (ถ้ามี path) VERIFY guard | — | toast `เฉพาะผู้อนุมัติ (DOA) เท่านั้น` | ☐ |

#### TC-P05 — viewer เห็นงบ mask ในตาราง (FN-94)
- group: Permission · ความสำคัญ: สูง · trace: FN-94 / BR-08 / D-CLASS / AC-24
- actor: viewer
- Setup: role=viewer · seed=course has_cost (งบ 30,000) · files=—
- Start: สลับ persona → OPEN `#/train/course`
- ผ่านเมื่อ: คอลัมน์งบแสดง `••••••` (mask) สำหรับ viewer

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (persona=hr) VERIFY+จด คอลัมน์งบ CRS-2569-001 | — | เห็น 30,000 (hr unmask) — จดไว้ | ☐ |
| 2 | CLICK แถบ `ผู้ชมทั่วไป` → VERIFY คอลัมน์งบแถวเดียวกัน | — | งบแสดง `••••••` (mask · ต่างจากค่าที่จด step 1) | ☐ |

#### TC-P06 — viewer เห็นรายงานตัวเงิน mask (FN-94)
- group: Permission · ความสำคัญ: สูง · trace: FN-94 / FIX-05 / AC-24
- actor: viewer
- Setup: role=viewer · seed=report มีตัวเงิน · files=—
- Start: สลับ persona → OPEN `#/train/report`
- ผ่านเมื่อ: cost-per-head cards แสดง งบ/ต้นทุนต่อหัว = `••••••` (viewer)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (persona=viewer) OPEN `#/train/report` | — | รายงานแสดง (viewer เห็นรายงานได้) | ☐ |
| 2 | VERIFY cost-per-head cards | — | งบ + ต้นทุนต่อหัว = `••••••` (mask · funnel/จำนวนคนยังเห็น) | ☐ |

---

### G9 · Negatives — "ห้ามมี" (แทน FN-40)

> feature นี้ไม่มี FN-40 — negatives ยืนยัน scope ที่ **ถูกตัด** (unsupported 5 · LOCK) ทำไม่ได้บนจอ

#### TC-N01 — ห้ามจ่ายเงินจริง/ลงบัญชี (OB-1 · LOCK-02/04)
- group: Negatives · ความสำคัญ: สูง · trace: LOCK-02, LOCK-04, BR-06, BR-09 / unsupported #1
- actor: hr
- Setup: role=hr · seed=enrollment confirmed has_cost · files=—
- Start: OPEN `#/train/plan` → รอบ has_cost → `อนุมัติ / ค่าใช้จ่าย`
- ผ่านเมื่อ: มีแค่ hook Expense (display-only) — **ไม่มี**ปุ่ม "จ่ายเงิน"/"ลงบัญชี"/"post GL" · toast ส่ง EC ระบุชัด `ไม่จ่าย/ไม่ post`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY EC block ทั้งหน้า | — | มีเฉพาะ `ส่ง Expense Claim (มูลค่า EC)` (hook) · **ไม่มี**ปุ่ม จ่ายเงิน/ลงบัญชี/โพสต์ GL/AC | ☐ |
| 2 | CLICK ส่ง EC → VERIFY toast | — | toast ระบุ `ส่งไปยัง Expense Claim (hook) แล้ว — ไม่จ่าย/ไม่ post` (ยืนยันไม่ลงบัญชี) | ☐ |
| 3 | VERIFY มูลค่า EC | — | display-only "อ้างอิง Rate Card · เชื่อมเมื่อพร้อม" (ไม่มีตัวเลขจ่ายจริง hardcode) | ☐ |

#### TC-N02 — ห้ามสร้าง/แก้ gap เอง (OB-2 · LOCK-03)
- group: Negatives · ความสำคัญ: สูง · trace: LOCK-03, BR-07, FN-10 / unsupported #2
- actor: hr
- Setup: role=hr · seed=รอบ open (หลักสูตรมี gap) · files=—
- Start: OPEN `#/train/plan` → รอบ → ผู้เรียน → ลงทะเบียน
- ผ่านเมื่อ: gap เป็น read-only (เลือกได้) — **ไม่มี**ปุ่ม "สร้าง gap"/"แก้ gap"/"เพิ่มช่องว่างทักษะ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด modal ลงทะเบียน → VERIFY ส่วน gap | — | gap cards แสดงเพื่อ**เลือก**เท่านั้น (จาก Performance) | ☐ |
| 2 | VERIFY | — | **ไม่มี**ปุ่ม สร้าง gap / แก้ gap / เพิ่มช่องว่าง (อ่านจาก Performance อย่างเดียว) | ☐ |

#### TC-N03 — ห้ามสร้าง/แก้ config หมวดหลักสูตร (LOCK-06 · #107)
- group: Negatives · ความสำคัญ: สูง · trace: LOCK-06 / unsupported #5
- actor: hr
- Setup: role=hr · seed=— · files=—
- Start: OPEN `#/train/course` → `สร้างหลักสูตร` → ช่องหมวด
- ผ่านเมื่อ: หมวดเป็น search-select อ่านจาก HR Config — **ไม่มี**ปุ่ม "เพิ่มหมวด"/"แก้หมวด"/"จัดการหมวด"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิดฟอร์มหลักสูตร → เปิด dropdown `หมวด` | — | รายการหมวด (ความปลอดภัย/ภาวะผู้นำ/การสื่อสาร/ปฐมนิเทศ) เลือกได้ | ☐ |
| 2 | VERIFY | — | **ไม่มี**ปุ่ม/ลิงก์ เพิ่มหมวด/แก้ไขหมวด/จัดการหมวด (อ่านจาก HR Config #107 อย่างเดียว) | ☐ |

#### TC-N04 — ห้ามออกใบรับรองเลขรัน/PDF (LOCK-07)
- group: Negatives · ความสำคัญ: สูง · trace: LOCK-07, BR-07C, CD-02 / unsupported #4
- actor: hr
- Setup: role=hr · seed=enrollment passed มี cert · files=—
- Start: OPEN `#/train/result`
- ผ่านเมื่อ: cert = soft ref — **ไม่มี**เลขเอกสาร running · **ไม่มี**ปุ่มดาวน์โหลด/พิมพ์ PDF ใบรับรอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | หาแถวผู้เรียน passed ที่ออก cert แล้ว → VERIFY | — | chip `ออกใบรับรองแล้ว` (soft ref) | ☐ |
| 2 | VERIFY | — | **ไม่มี**เลขรันใบรับรอง · **ไม่มี**ปุ่ม ดาวน์โหลด PDF / พิมพ์ใบรับรอง (ไม่ใช่ doccfg/pdfdoc) | ☐ |

#### TC-N05 — ห้าม SCORM/eLearning/competency mapping (OQ NICE)
- group: Negatives · ความสำคัญ: กลาง · trace: unsupported #3 (SCORM/competency)
- actor: hr
- Setup: role=hr · seed=— · files=—
- Start: OPEN `#/train/course` / `#/train/result`
- ผ่านเมื่อ: ทั้งฟีเจอร์ **ไม่มี**ส่วน eLearning content/SCORM upload · **ไม่มี** competency/skill mapping

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สำรวจทุก tab (course/plan/result/report) + drawer หลักสูตร | — | ไม่มีส่วนอัปโหลด SCORM/เนื้อหา eLearning · ไม่มีเมนู competency/mapping ทักษะ | ☐ |
| 2 | VERIFY ฟอร์มหลักสูตร | — | fields = ชื่อ/หมวด/ผู้สอน/ระยะเวลา/งบ เท่านั้น (ไม่มี SCORM package / competency) | ☐ |

---

### G10 · Edge cases (EC-01..08)

#### TC-ID01 — idempotency double-submit (EC-03 · AC-22)
- group: Edge · ความสำคัญ: สูง · trace: EC-03 / FN-92 / AC-22/28 / ERR_DUPLICATE_IDEMPOTENCY_KEY
- actor: hr
- Setup: role=hr · seed=รอบ open · files=— · inject: กด submit ซ้ำเร็ว (double-click) — backend idempotency-key
- Start: OPEN `#/train/plan`
- ผ่านเมื่อ: กดลงทะเบียน/บันทึกซ้ำ → เกิด record เดียว (busy state กันซ้ำ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด modal ลงทะเบียน → เลือกผู้เรียน → CLICK ปุ่มลงทะเบียน 2 ครั้งเร็ว | — | ปุ่ม disabled/busy หลังคลิกแรก · เกิดผู้เรียน **1 รายการ** (ไม่ซ้ำ) · (concurrent จริง = 409 idempotency ที่ API · mark simulate) | ☐ |

#### TC-PR01 — permission mid-flight approver ถูก demote (EC-02 · AC-27)
- group: Edge · ความสำคัญ: กลาง · trace: EC-02 / BR-13 / ERR_PERMISSION_REVOKED / ERR_NOT_APPROVER `(ต้อง simulate)`
- actor: manager→(demoted)
- Setup: role=manager เปิดหน้าอนุมัติ · seed=enrollment pending_doa · inject: เปลี่ยน role เป็น non-approver ระหว่างเปิดหน้า (สลับ persona เป็น viewer/hr แล้วลองกดอนุมัติ) · files=—
- Start: OPEN `#/train/plan` → รอบ → ผู้เรียน pending
- ผ่านเมื่อ: หลัง demote กดอนุมัติ → ถูกปฏิเสธ (403) — prototype จำลองด้วยการสลับ persona

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (persona=manager) เปิดแถวผู้เรียน pending เห็นปุ่ม `อนุมัติ` | — | ปุ่มอนุมัติปรากฏ | ☐ |
| 2 | สลับ persona → `เจ้าหน้าที่อบรม` (จำลอง demote) แล้วดูแถวเดิม | — | ปุ่ม `อนุมัติ` หายไป (re-check สิทธิ์) — hr ไม่ใช่ approver | ☐ |
| 3 | VERIFY (backend) | — | ถ้ายิง approve หลัง demote → 403 `ERR_PERMISSION_REVOKED`/`ERR_NOT_APPROVER` (mark simulate — ต้อง test ที่ API) | ☐ |

#### TC-EC01 — concurrent approval 2 คนชนกัน (EC-01 · AC-26)
- group: Edge · ความสำคัญ: กลาง · trace: EC-01 / LD-01 / ERR_STALE_DATA `(ต้อง simulate)` · `[AI-DEFAULT]`
- actor: manager ×2
- Setup: role=manager · seed=enrollment ที่ 2 approver กด approve ขั้นเดียวกันพร้อมกัน · inject: 2 session ยิงพร้อมกัน (ต้อง test ที่ backend — prototype กดทีละครั้ง) · files=—
- Start: OPEN `#/train/plan`
- ผ่านเมื่อ: คนแรก commit · คนสอง → 409 ERR_STALE_DATA (optimistic lock · version)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | approve ขั้นเดียวกันจาก session ที่ 1 | — | สำเร็จ (version+1) | ☐ |
| 2 | approve ขั้นเดิมจาก session ที่ 2 (stale version) | — | 409 `ERR_STALE_DATA` (mark simulate — prototype ตรวจได้แค่ว่ากดขั้นที่ approved ไปแล้วซ้ำ → toast `อนุมัติขั้นนี้แล้ว` / `ไม่มีขั้น pending`) | ☐ |

#### TC-EC06 — master ถูกปิดใช้งานระหว่างค้าง — snapshot กันชื่อเพี้ยน (EC-06)
- group: Edge · ความสำคัญ: ต่ำ · trace: EC-06 / BR-10 (snapshot) `(ต้อง simulate)`
- actor: hr
- Setup: role=hr · seed=enrollment ที่ผู้เรียนถูกปิดใช้งานใน Employee master ภายหลัง · inject: ปิดใช้งาน emp (ทำที่ HR master — นอก prototype) · files=—
- Start: OPEN `#/train/plan` → รอบ → ผู้เรียน
- ผ่านเมื่อ: ชื่อผู้เรียนใน enrollment ใช้ snapshot (ไม่เปลี่ยนย้อนหลังแม้ master เปลี่ยน)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ชื่อ/ตำแหน่ง/แผนกผู้เรียนใน enrollment | — | แสดง snapshot ณ เวลาลงทะเบียน (คงที่แม้ master แก้ภายหลัง) — mark simulate (ต้องแก้ master จริง) | ☐ |

#### TC-HRS01 — duration parse ไม่ได้ → ชม.=0 (EC-07)
- group: Edge · ความสำคัญ: ต่ำ · trace: EC-07 / BR-15 / FIX-04 (fallback 0)
- actor: hr
- Setup: role=hr · seed=หลักสูตรที่ duration รูปแบบแปลก (parse ชม.ไม่ได้) มีผู้ผ่าน · files=—
- Start: OPEN `#/train/result` → คลิกชื่อผู้เรียน
- ผ่านเมื่อ: รายการนั้นบวกชม. = 0 (ไม่ทำให้ยอดรวมพัง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด modal ประวัติผู้เรียน → หาแถว duration แปลก | — | คอลัมน์ +ชม.นับสะสม = 0 (fallback) · ยอดรวมยังคำนวณได้ (ไม่ NaN/error) `⚠ ยืนยัน anchor` (ขึ้นกับ seed มี duration แปลกหรือไม่) | ☐ |

#### TC-MASK01 — viewer mask money + export mask (EC-08 · AC-24)
- group: Edge · ความสำคัญ: กลาง · trace: EC-08 / FN-94 / FIX-05 / AC-24
- actor: viewer
- Setup: role=viewer · seed=report + list มีตัวเงิน · files=—
- Start: สลับ persona → OPEN `#/train/report`
- ผ่านเมื่อ: ตัวเงิน mask ทั้ง list · report · (export ก็ต้อง mask ตาม role — ตรวจ concept)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (viewer) OPEN `#/train/course` VERIFY งบ | — | งบ = `••••••` | ☐ |
| 2 | OPEN `#/train/report` VERIFY ต้นทุนต่อหัว/งบ | — | `••••••` | ☐ |
| 3 | CLICK Export CSV | — | toast `ส่งออกรายงาน (CSV) — ต่อ dev` · (spec: export ต้อง mask ตาม role — dev enforce · ตรวจจริงตอน dev) | ☐ |

---

### G11 · Cross-module (XT-01..04)

#### TC-XT01 — อนุมัติ DOA ครบ → emit EC event (CSQ · ไม่มี AC)
- group: Cross-module · ความสำคัญ: กลาง · trace: XT-01 / BR-09 / LOCK-04 / AC-12 `(ต้อง simulate — downstream)`
- actor: manager
- Setup: role=manager · seed=enrollment has_cost ที่ approve ครบทำให้ confirmed · files=— · downstream: CSQ mock (assert emit `train.enrolled_paid`)
- Start: OPEN `#/train/plan` → อนุมัติครบ
- ผ่านเมื่อ: confirmed → emit CSQ `train.enrolled_paid` (EC เท่านั้น · **ไม่มี AC** · GL ไม่กระทบ) — prototype ตรวจจากสถานะ confirmed + toast

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | อนุมัติครบทุกขั้น → WAIT toast | — | toast `อนุมัติและยืนยันลงทะเบียนแล้ว` · สถานะ confirmed | ☐ |
| 2 | VERIFY event (downstream mock) | — | emit `train.enrolled_paid` (EC) · **ไม่มี** AC/GL posting (mark simulate — assert ที่ CSQ mock) | ☐ |

#### TC-XT02 — ส่ง Expense → Expense Claim รับ hook (display-only · ไม่ post)
- group: Cross-module · ความสำคัญ: กลาง · trace: XT-01b/02 / BR-06 / LOCK-02 `(ต้อง simulate)`
- actor: hr
- Setup: role=hr · seed=enrollment confirmed has_cost · files=— · downstream: Expense Claim (F101) mock (assert payload, no post)
- Start: OPEN `#/train/plan` → `อนุมัติ / ค่าใช้จ่าย`
- ผ่านเมื่อ: hook ส่ง payload display-only · Expense **ไม่ auto-post** บัญชี

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `ส่ง Expense Claim (มูลค่า EC)` → WAIT | — | toast `ส่งไปยัง Expense Claim (hook) แล้ว — ไม่จ่าย/ไม่ post` | ☐ |
| 2 | VERIFY downstream (mock) | — | Expense Claim รับ hook (display-only) · **ไม่มี**การ post บัญชีอัตโนมัติ (mark simulate — assert ที่ F101 mock) | ☐ |

#### TC-XT03 — ลงทะเบียนจาก gap → Performance ไม่ถูกแก้ (read-only)
- group: Cross-module · ความสำคัญ: กลาง · trace: XT-03 / LOCK-03 / BR-07 `(ต้อง simulate)`
- actor: hr
- Setup: role=hr · seed=course มี gap (Performance F131 mock) · files=—
- Start: OPEN `#/train/plan` → ลงทะเบียนจาก gap
- ผ่านเมื่อ: เลือก gap → enrollment source=gap เก็บ gap_ref · Performance (ต้นทาง) **ไม่ถูกแก้**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ลงทะเบียนโดยเลือก gap card | — | source=gap · toast `เลือกผู้เรียนจาก gap แล้ว` | ☐ |
| 2 | VERIFY Performance (downstream mock) | — | gap ต้นทางไม่ถูก mutate (read-only) — mark simulate (assert ที่ F131 mock) | ☐ |

#### TC-XT04 — render มูลค่า EC/ต้นทุนต่อหัว = display-only (Rate Card pending · FIX-07)
- group: Cross-module · ความสำคัญ: กลาง · trace: XT-04 / BR-17 / LD-03 / FIX-07 / OQ-03 · `[AI-DEFAULT]`-adjacent
- actor: hr
- Setup: role=hr · seed=course has_cost · files=—
- Start: OPEN `#/train/plan` → `อนุมัติ / ค่าใช้จ่าย` (และ P-05 ฟอร์ม toggle มีค่าใช้จ่าย)
- ผ่านเมื่อ: มูลค่า EC แสดง "อ้างอิง Rate Card · เชื่อมเมื่อพร้อม" — **ไม่มี**ตัวเลข hardcode (Rate Card F060 ยังไม่ dev)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิดฟอร์มหลักสูตร → TOGGLE มีค่าใช้จ่าย เปิด → VERIFY การ์ด EC | — | การ์ด "อ้างอิง Rate Card · เชื่อมเมื่อพร้อม" (ไม่มีมูลค่า EC เป็นตัวเลขคงที่) | ☐ |
| 2 | เปิด `อนุมัติ / ค่าใช้จ่าย` ของรอบ has_cost → VERIFY มูลค่า EC | — | display-only ref Rate Card · ไม่มีตัวเลข EC hardcode | ☐ |

---

### แถม · Notifications

#### TC-NTF01 — แจ้งเตือน 3 event ของ feature (FN-12 · AC-19)
- group: Notifications · ความสำคัญ: กลาง · trace: FN-12 / AC-19 / events (opened/confirmed/result) `(ต้อง simulate emit)`
- actor: hr
- Setup: role=hr · seed=รอบ draft + enrollment ฟรี + enrollment attended · files=— · NTF mock (assert emit)
- Start: OPEN `#/train/plan`
- ผ่านเมื่อ: 3 event ของ feature emit ถูกจุด · doa_* **ไม่ประกาศเอง** (มาจาก DOA engine)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิดรับสมัครรอบ | — | emit `train_session_opened` (toast `เปิดรับสมัครแล้ว` · assert ที่ NTF mock) | ☐ |
| 2 | ลงทะเบียนฟรี (confirmed) | — | emit `train_enroll_confirmed` | ☐ |
| 3 | บันทึกผล (passed/failed) | — | emit `train_result` | ☐ |
| 4 | VERIFY doa_* | — | ระบบ**ไม่ประกาศ** doa_pending/doa_result เอง (มาจาก DOA engine) — mark simulate | ☐ |
| 5 | CLICK ไอคอนกระดิ่ง (topbar) | — | toast `ศูนย์แจ้งเตือน (ENG-NOTIFY) — เชื่อมจริงตอน dev` (stub) | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `อบรม.html` ใน browser (โหลด Lucide icons + fonts จาก CDN — ต้องมีเน็ต).
2. **หนึ่งเคส = refresh ก่อนเริ่ม** (prototype seed คงที่ · refresh คืนค่าเริ่มต้น). ยกเว้นเคสที่ Setup ระบุ chain ต่อจากเคสก่อน (เช่น TC-E04→E05).
3. สลับบทบาทที่แถบบนขวา **"Demo · ดูในฐานะ"** ตาม `Setup: role=` — `เจ้าหน้าที่อบรม`=hr · `หัวหน้า (ผู้อนุมัติ)`=manager · `ผู้ชมทั่วไป`=viewer.
4. เดินตาม `Start` → ทำ step ตามลำดับ · เทียบ Expected กับสิ่งที่เห็นจริง · ติ๊ก Result (☐→pass/fail) ในเครื่อง (localStorage runtime).
5. เคส `(ต้อง simulate)` = ต้องมี backend/mock ปลายทาง — บน prototype ทำได้แค่บางส่วน (สังเกต UI/สถานะ) · ที่เหลือ mark **blocked** พร้อม evidence.
6. anchor ที่ติด `⚠ ยืนยัน anchor` = ให้เทียบกับ UI จริง ถ้าข้อความ/ปุ่มต่างจากที่เขียน ให้บันทึก evidence (ไม่ถือว่า fail ทันที).
7. กรอกผลกลับตาม `Result Report (schema)` ด้านล่าง.

---

## Coverage Audit

| หมวด | covered / total |
|---|---|
| FN (FUNCTION_CHECKLIST) | **18 / 18** ✅ |
| Capability FIX-01..07 | **7 / 7** ✅ |
| Business rules (BR-01..18) | 18 / 18 ✅ |
| Edge cases (EC-01..08) | 8 / 8 ✅ |
| Error codes (catalog) | 19 / 22 (ที่มีผลสังเกตบน UI) |
| Permission cells (สำคัญ) | 9 / 9 ✅ |
| Cross-Module (XT-01..04) | 4 / 4 ✅ (+XT-01b/02) |
| Scope Lock (LOCK-01..07) | 7 / 7 ✅ |
| Negatives "ห้ามมี" | **5 / 5** ✅ (unsupported 1–5) |
| Events / States | ครบ (3 event feature + doa_* ไม่ประกาศเอง · course/session/enrollment state) |
| AC (06_TESTS AC-01..25) | 25 / 25 ✅ |

- **FN cross-check: ✅ 18/18** (ทุก FN ใน FUNCTION_CHECKLIST มี TC ≥1)
- **Capability FIX cross-check: ✅ 7/7** (FIX-01..05 + DOA gate/slot FIX-06 + Rate Card display-only FIX-07)
- **Negatives: 5/5** (จ่ายเงินจริง · สร้าง gap เอง · SCORM/competency · cert เลขรัน/PDF · แก้ config หมวด)
- **Permission: 3 persona ครบ** (hr/manager/viewer + mask money) · SoD (hr approve=deny)
- **Cross-module hooks:** Expense (display-only) · Performance (read-only) · HR Config (read-only) · Rate Card (display-only) · CSQ (EC ไม่มี AC)
- **Scope Lock (LOCK): 7/7**
- **Manifest cross-check (FRD §0.12): ✅ 20/20** (FN-01..13 + FN-90..94 + FIX-04/FIX-05 rows ทุกแถว manifest มีคู่ใน Ledger)

### ข้าม (พร้อมเหตุผล)
- **Error codes ที่ไม่มีเคสตรง (3):** `ERR_NOT_AUTHENTICATED` (401 · ไม่มี login flow ใน prototype) · `ERR_NOT_FOUND` (404 · record หาย — hidden path) · `BR_NO_PENDING_STEP` (ครอบทางอ้อมใน TC-EC01 "ไม่มีขั้น pending") — ทั้งหมดเป็น backend guard ไม่มีทางเข้าที่ UI prototype โดยตรง
- **EC-01/EC-02/EC-04/EC-06 + XT-01..03 + NTF emit:** ทำได้บางส่วนบน prototype · ส่วน concurrent/downstream mark `(ต้อง simulate)` — ต้องรันที่ backend/mock จริง (ระบุใน Setup)
- **นอกขอบเขตใบเซ็น (Exclusions):** unsupported 5 → ไม่สร้างเคส "ทำได้" (สร้างแต่เคส negative ยืนยัน "ทำไม่ได้" G9) ตาม R18

### Drift / หมายเหตุ (สำหรับคนตามเช็ค)
- **Routes:** HTML ใช้ `#/train/<tab>` (getRoute แปลง `train/course`→tab) — 01_UI ถูกต้อง ✅ (route เปล่า `#/course` ไม่ทำงาน · ต้อง `#/train/course`)
- **Toast create course:** HTML publish→`สร้างหลักสูตรแล้ว` · draft→`บันทึกร่างแล้ว` (ตรงกับ 06_TESTS §6.10) · ปุ่ม primary = `เผยแพร่หลักสูตร` (label≠toast — ปกติ)
- **Tooltip disabled:** HTML verbatim = `บันทึกผลได้หลังปิดรอบอบรม (จบการอบรม)` / `ต้องเช็คชื่อเข้าอบรมก่อน` (06_TESTS §6.10 เขียนย่อ — ใช้ HTML)
- **gap header:** HTML มี "แนะนำจากผลประเมิน" · AC-08 ระบุเต็ม "(gap · Performance)" → ติด `⚠ ยืนยัน anchor` ที่ TC-E02
- **QA column:** ผลติ๊กเป็น localStorage runtime — tester ติ๊กใน browser (แก้ไฟล์ไม่ได้) · Ledger FN↔TC ด้านบนคือหลักฐานความครบ

---

## Result Report (schema)

```json
{
  "feature_id": "F-HR-TRAIN",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-C01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 84, "pass": 0, "fail": 0, "blocked": 0 }
}
```

> `evidence` = สิ่งที่ agent **เห็นจริง** ตอน fail/blocked (ข้อความ error จริง · route ที่ค้าง · สิ่งที่แสดงแทน Expected). `note` = หมายเหตุ (เช่น "prototype ตรวจได้แค่ UI · ส่วน concurrent ต้อง backend").
> เคส `(ต้อง simulate)` ที่รันบน prototype ไม่ได้ครบ → `blocked` + ระบุว่าต้องมี mock/backend อะไร.
