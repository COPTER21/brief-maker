# AI Test Cases — F131 Performance / ประเมินผลงาน

เอกสารนี้เขียนให้ **AI agent (browser-use / vision)** อ่านแล้วลงมือทดสอบบน `performance.html` จริง แล้วรายงานผลกลับ.
ทุก action ผูกกับ **ข้อความที่เห็นบนจอ** (verbatim จาก HTML) + expected เช็คได้ด้วยตา. anchor ทั้งหมด Sync Read จาก `performance.html` (ต้นทาง) → 01_UI → 06_TESTS §6.10 (ตรงกันทุกจุด, ไม่มี drift).

> **⚠ โปรโตไทป์เป็น tab-based SPA — ไม่มี hash route.** สลับหน้า = **คลิกแท็บ**; สลับบทบาท = **คลิกปุ่มใน demo strip** ด้านบน ("มุมมองสาธิต (สิทธิ์)"). โหลดหน้าใหม่ = รีเซ็ตกลับค่าเริ่มต้น (role=HR (HRBP) · แท็บ "รอบประเมิน" · ตัวกรอง=ทุกสถานะ). ไม่มี persistence — ทุกเคส refresh-safe เริ่มจากโหลดสด.
> **⚠ Mock-data note (OQ-PERF-11):** persona "หัวหน้าสายงาน" = ประสงค์ ชัยมงคล (dept=ฝ่ายผลิต) แต่ appraisal ขั้น mgr เดียว (A3 อรทัย) = ฝ่ายบัญชี → หัวหน้าเข้าไม่ถึงผ่าน UI dept-scoped. ดังนั้น **manager-review happy path รันด้วย role HR** (sec.can('saveMgr') = mgr∥manage · HR ผ่าน). เคสหัวหน้ารีวิวในขอบเขตจริงต้อง seed appraisal ขั้น mgr ในฝ่ายผลิต → mark `(ต้อง simulate/seed)`.

---

## Meta

| Field | Value |
|---|---|
| Feature ID | F131 (F-HR-PERF) |
| ชื่อ | Performance / ประเมินผลงาน |
| Module | HR · Archetype = master + cycle (ไม่ใช่ Pattern Q document) |
| App entry | `performance.html` (เปิดตรง ๆ ในเบราว์เซอร์) |
| Routes | tab-state (ไม่มี hash): `รอบประเมิน` · `แบบประเมินรายคน` · `สอบทาน + ผล & Gap` · `รายงาน` |
| ที่มา | FRD Pack F-HR-Performance (00/01/03/05/06) · BRD_performance.md · performance.html (gated: ux BLOCK=0 · coverage FN 18/18) |
| จำนวนเคส | 77 เคส · 18 กลุ่ม |
| Roles | HR (HRBP) manage/ALL · หัวหน้าสายงาน DEPT(ฝ่ายผลิต) · พนักงาน SELF(mask) |
| TODAY (mock) | 2026-09-09 |

---

## Coverage

| Group | Prefix | เคส | ความสำคัญ |
|---|---|---|---|
| รอบประเมิน (create/close/view) | TC-CY | 7 | สูง |
| KPI / ตั้งเป้า (Σ=100) | TC-KP | 5 | สูง |
| ประเมินตนเอง | TC-SF | 3 | สูง |
| หัวหน้าประเมิน + weighted | TC-MG | 4 | สูง |
| สอบทาน (staged DOA) | TC-CB | 7 | สูง |
| ผล/Gap + hooks | TC-PB | 5 | สูง |
| Re-open published | TC-RO | 5 | สูง |
| PIP | TC-PP | 2 | กลาง |
| Overdue + reminder | TC-OD | 2 | กลาง |
| แจ้งเตือน 3 event | TC-NT | 1 | กลาง |
| รายงาน distribution | TC-RP | 4 | กลาง |
| ค้นหา/filter/empty | TC-SR | 4 | กลาง |
| RESTRICTED scope/mask | TC-SC | 7 | สูง |
| audit append-only | TC-AU | 2 | สูง |
| guard cascade + double-submit | TC-GD | 6 | สูง |
| Cross-module (XT) | TC-XT | 5 | กลาง |
| Scope Lock verify | TC-LK | 6 | สูง |
| team-calibration view | TC-TM | 2 | ต่ำ |

---

## Coverage Ledger

### FR / AC (06_TESTS)
| item | cases |
|---|---|
| AC-01 / FN-01 สร้างรอบ | TC-CY01, TC-CY02, TC-LK03 |
| AC-02 / FN-11 ปิดรอบ (ล็อกจริง) | TC-CY04, TC-CY05, TC-GD04 |
| AC-03 / FN-02 KPI Σ=100 | TC-KP01, TC-KP02, TC-KP03 |
| AC-04 / FN-03 ประเมินตนเอง | TC-SF01, TC-SF02 |
| AC-05 / FN-04 หัวหน้าประเมิน + weighted | TC-MG01, TC-MG02, TC-MG03 |
| AC-06 / FN-09 overdue → เตือน | TC-OD01, TC-OD02 |
| AC-07 / FN-05 สอบทาน + decision | TC-CB03, TC-CB04, TC-CB07 |
| AC-08 / FN-08 staged DOA slot picker | TC-CB01, TC-CB02, TC-CB03, TC-CB05, TC-LK01 |
| AC-09 / FN-06 gap → Training hook | TC-PB01, TC-XT02 |
| AC-10 / FN-07 ผล → Movement event | TC-PB02, TC-XT01 |
| AC-11 / FN-10 PIP | TC-PP01, TC-PP02 |
| AC-12 / FN-12 แจ้งเตือน 3 event | TC-NT01 |
| AC-13 / FN-13 รายงาน distribution | TC-RP01, TC-RP02, TC-RP03, TC-RP04 |
| AC-14 / FN-90 search/filter/empty | TC-SR01, TC-SR02, TC-SR03, TC-SR04 |
| AC-15 / FN-92 double-submit | TC-GD05 |
| AC-16 / FN-93 audit append-only | TC-AU01, TC-AU02 |
| AC-17 / FN-94 RESTRICTED scope/mask | TC-SC01..07 |
| AC-18 re-open published | TC-RO01..05 |
| AC-19 guard cascade P1-P4 | TC-GD01, TC-GD02, TC-GD03, TC-GD04 |

### Business Rules (05_RULES)
| rule | cases |
|---|---|
| BR-01 รอบจาก HR Config #107 | TC-CY01, TC-LK03 |
| BR-02 Σweight=100 | TC-KP01, TC-KP02 |
| BR-03 self ก่อน mgr (state order) | TC-SF01, TC-GD02 |
| BR-04 weighted score | TC-MG02 |
| BR-05 staged DOA + decision ก่อน publish | TC-CB01..04, TC-CB07 |
| BR-06 gap → Training hook | TC-PB01, TC-LK05 |
| BR-07 ผล → Movement event | TC-PB02, TC-LK02 |
| BR-08 RESTRICTED + mask ตาม role | TC-SC01..07, TC-LK04 |
| BR-09 audit append-only + ปิดรอบล็อก | TC-AU01, TC-CY05, TC-GD04 |
| BR-10 snapshot ชื่อ/ตำแหน่ง/แผนก | TC-SC03 (dept scope ใช้ snapshot) |
| BR-11 scope SELF/DEPT/ALL | TC-SC01, TC-SC03, TC-SC05 |
| BR-12 re-open authorized+reason+audit | TC-RO01..05 |
| BR-13 CSQ 7C per-person publish | TC-CB04, TC-XT04, TC-RO05, TC-LK06 |

### Field Validation (05_RULES §5.4)
| VR | cases |
|---|---|
| VR-01 KPI weight≠100 | TC-KP02 |
| VR-02 slot ว่าง | TC-CB02 |
| VR-03 reopen reason ว่าง | TC-RO02 |
| VR-04 mutation รอบ closed | TC-CY05, TC-GD04 |
| VR-05 role ไม่ผ่าน | TC-GD03, TC-SC06, TC-SC07 |
| VR-06 double-submit | TC-GD05 |
| VR-07 doCalib stage/score ไม่ครบ | TC-GD01 |
| VR-08 self/mgr score ไม่ครบ 1–5 | TC-SF02, TC-MG03 |
| VR-09 ชื่อ KPI ว่าง | TC-KP03 |
| VR-10 PIP gap ว่าง | TC-PP02 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 สอบทานข้ามขั้น (FIX-01) | TC-GD01 |
| EC-02 transition ย้อนหลัง (FIX-02) | TC-GD02 |
| EC-03 staff เดินผลแทน (FIX-03) | TC-GD03, TC-SC06 |
| EC-04 staff เห็น decision/gap ผู้อื่น (FIX-04) | TC-SC01, TC-SC02 |
| EC-05 concurrent staged review `[AI-DEFAULT]` | TC-GD06 (ต้อง simulate) |
| EC-06 HR Config missing `[AI-DEFAULT]` | — ข้าม (upstream soft-ref, ไม่มีทางเข้าใน prototype · Test=TC-CFG-01 API-level) |
| EC-07 ปิดรอบยัง mutate (FIX-05) | TC-CY05, TC-GD04 |
| EC-08 DOA slot preset/คลิกเดียวจบ (FIX-06) | TC-CB01, TC-CB05, TC-LK01 |
| EC-09 overdue (FN-09) | TC-OD01, TC-OD02 |
| EC-10 mgr ย้ายแผนกกลางรอบ `[AI-DEFAULT]` | TC-SC03 (snapshot dept · ต้อง seed) |

### Error Codes (05_RULES §5.6 — UI สังเกตผ่าน toast/guard)
| error | cases |
|---|---|
| ERR_INSUFFICIENT_ROLE ("สิทธิ์ไม่พอ") | TC-GD03, TC-SC06 (ต้อง simulate call) |
| ERR_STAGE_INVALID | TC-GD01, TC-GD02 (UI: editor/ปุ่มไม่ render + simulate toast) |
| BR_CYCLE_CLOSED ("รอบนี้ปิดแล้ว — แก้ไขไม่ได้") | TC-CY05, TC-GD04 |
| BR_KPI_WEIGHT_NOT_100 | TC-KP02 |
| BR_KPI_TITLE_REQUIRED | TC-KP03 |
| BR_SELF_SCORE_INCOMPLETE | TC-SF02 |
| BR_MGR_SCORE_INCOMPLETE | TC-MG03, TC-GD01 |
| BR_REVIEWER_SLOT_EMPTY | TC-CB02 |
| BR_REASON_REQUIRED | TC-RO02 |
| BR_GAP_REQUIRED | TC-PP02 |
| BR_CONFIG_CYCLE_NOT_FOUND / ERR_CONFIG_UPSTREAM_DOWN | — ข้าม (EC-06 · API-level, ไม่มี UI hook) |
| ERR_STALE_DATA (concurrency) | TC-GD06 (ต้อง simulate) |

### Permission Matrix (role × action) — 05_RULES §5.3
| cell | cases |
|---|---|
| HR create/close cycle = allow | TC-CY01, TC-CY04 |
| staff/mgr create cycle = deny (ปุ่มไม่ render) | TC-CY03 |
| HR saveKpi(goal) = allow · deny อื่น | TC-KP01, TC-GD03 |
| staff saveSelf(own) = allow | TC-SF01 |
| mgr∥HR saveMgr = allow · staff = deny | TC-MG01, TC-SC06 |
| HR doCalib/doPip/reopen/send* = allow | TC-CB, TC-PP01, TC-RO01, TC-PB |
| staff/mgr ไม่เห็นคิวสอบทาน/ปุ่ม mutation | TC-SC02, TC-SC04, TC-SC05, TC-SC07 |
| staff เห็นผล/decision/gap ผู้อื่น = deny (mask+ไม่อยู่ DOM) | TC-SC01, TC-SC02 |

### Cross-Module (XT — 06_TESTS §6.9)
| XT | Downstream | Case |
|---|---|---|
| XT-01 movement_requested | Movement (F-HR-MOVE) | TC-XT01 |
| XT-02 gap.training_requested | Training | TC-XT02 |
| XT-03 result.succession_candidate | Succession (F134) | TC-XT03 |
| XT-04 result.published → CSQ 7C per-person | ENG-CSQ | TC-XT04 |
| XT-05 re-open → re-publish (movement+CSQ ซ้ำ, ผลเดิมไม่ลบ) | Movement + CSQ | TC-XT05 |

### Scope Lock (07_LOCKED §7.0)
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LK-1 | DOA เลือกคนจริงต่อขั้น · ห้าม preset | TC-LK01 |
| LK-2 | ผล → Movement = event (ไม่ CRUD) | TC-LK02 |
| LK-3 | รอบ/แบบ จาก HR Config #107 (ไม่สร้างเอง) | TC-LK03 |
| LK-4 | ผล = RESTRICTED + audit append-only | TC-LK04 |
| LK-5 | gap → Training = hook (ไม่สร้างหลักสูตร) | TC-LK05 |
| LK-6 | CSQ ประกาศ SecC+DC เท่านั้น | TC-LK06 |

### States / Events / Views
| item | cases |
|---|---|
| empty (list ค้นไม่พบ) | TC-SR02 |
| empty (คิวสอบทาน) | TC-SC05 (staff) / TC-CB06 |
| empty (ผลเผยแพร่) | TC-SC02 (staff) |
| closed read-only banner | TC-CY05 |
| overdue banner | TC-OD01 |
| notif panel 3 event | TC-NT01 |
| team-calibration view (LD-07 KEPT) | TC-TM01, TC-TM02 |
| weight tag ok/bad | TC-KP01, TC-KP02 |

---

## Data Sets

### บทบาท (Roles — สลับที่ demo strip)
| ปุ่มบนจอ | ชื่อผู้ใช้ (แสดงมุมขวา) | scope | หมายเหตุ |
|---|---|---|---|
| **HR (HRBP)** | สุนิสา คำแก้ว | ALL (manage) | ค่าเริ่มต้นเมื่อโหลดหน้า |
| **หัวหน้าสายงาน** | ประสงค์ ชัยมงคล | DEPT = ฝ่ายผลิต | เห็นเฉพาะ appraisal แผนกฝ่ายผลิต |
| **พนักงาน** | สมชาย ใจดี | SELF (mask) | เห็นเฉพาะแบบประเมินของตน (= A2) |

### แบบประเมิน seed (รอบ CY1 "รอบครึ่งปีหลัง 2569" · open)
| id | พนักงาน | แผนก | สถานะ (pill) | due | decision | gap | weighted (หัวหน้า) |
|---|---|---|---|---|---|---|---|
| A1 | มะลิ ดอกไม้ | คลังสินค้า | ตั้งเป้า (goal) | 2026-09-20 | — | — | — (Σw KPI=100) |
| A2 | สมชาย ใจดี | ฝ่ายผลิต | ประเมินตนเอง (self) | 2026-09-05 | — | — | — (overdue) |
| A3 | อรทัย แสนสุข | ฝ่ายบัญชี | หัวหน้าประเมิน (mgr) | 2026-09-30 | — | — | — (ยังไม่มี mgr score) |
| A4 | ธนากร พูนผล | ฝ่ายขาย | รอสอบทาน (calibration) | 2026-09-28 | — | — | 4.60 |
| A5 | กนกพร วงศ์ไทย | ฝ่ายการตลาด | เผยแพร่ผล (published) | 2026-08-30 | ผ่าน | ทักษะการนำเสนอ | 4.00 (top) |
| A6 | ปิยะ มั่นคง | คลังสินค้า | เผยแพร่ผล (published) | 2026-08-30 | ทบทวน (PIP) | ความถูกต้องในงาน | 2.30 |

### รอบประเมิน (Cycles)
| id | ชื่อ | สถานะ (pill) |
|---|---|---|
| CY1 | รอบครึ่งปีหลัง 2569 | เปิดกรอก (open) |
| CY2 | รอบครึ่งปีแรก 2569 | ปิดรอบ (closed) — ไม่มี appraisal |

### รอบใน "ตั้งค่า HR" (configCycles — เลือกตอนสร้างรอบ)
`รอบครึ่งปีหลัง 2569 (ก.ค.–ธ.ค.)` · `รอบประเมินโบนัสปลายปี 2569` · `รอบทดลองงาน (probation)`

### บุคคลสำหรับ slot ผู้สอบทาน (people)
ประสงค์ ชัยมงคล · สุนิสา คำแก้ว · วิชัย เจริญสุข · อรพิน สมบูรณ์ · ธีรพงษ์ ทองดี

### ชุดค่า KPI
- **KPI-OK:** ตั้ง 2 แถว น้ำหนัก 60 + 40 = 100 (ชื่อ+เป้าหมายกรอกครบ)
- **KPI-BAD-SUM:** แก้แถวหนึ่งเป็น 50 → รวม 90 (≠100)
- **KPI-BAD-NAME:** เว้นชื่อ KPI แถวหนึ่งว่าง

### ไฟล์ทดสอบ (Files)
— ไม่มี (feature นี้ไม่มี upload/CSV/PDF)

---

## Test Cases

### กลุ่ม TC-CY · รอบประเมิน (สร้าง/ปิด/ดู)

#### TC-CY01 — สร้างรอบประเมินจาก ตั้งค่า HR (happy)
- group: รอบประเมิน · ความสำคัญ: สูง · trace: FN-01 / AC-01 / BR-01 / LK-3 / event รอบเปิด
- actor: HR (HRBP)
- Setup: role=hr · seed=default · files=—
- Start: OPEN performance.html (โหลดสด, role=HR, แท็บ "รอบประเมิน")
- ผ่านเมื่อ: drawer ปิด + toast "สร้างรอบ · เปิดกรอก · แจ้งเตือนผู้เข้าร่วมแล้ว" + แถวรอบใหม่ pill "เปิดกรอก" โผล่บนสุดของตาราง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แท็บบนสุด "รอบประเมิน" is-active + ปุ่มมุมขวาบน | — | เห็นปุ่ม **สร้างรอบประเมิน** (มีเฉพาะ role HR ที่แท็บนี้) | ☐ |
| 2 | CLICK ปุ่ม **สร้างรอบประเมิน** | — | drawer เปิดหัวข้อ **สร้างรอบประเมิน** + note "รอบ/แบบฟอร์ม/เกณฑ์คะแนน อ่านจาก ตั้งค่า HR — หน้านี้ไม่สร้าง/แก้ฟอร์มกลาง" | ☐ |
| 3 | CLICK ช่อง **เลือกรอบจาก ตั้งค่า HR** (search-select placeholder "ค้นหารอบที่ประกาศไว้…") | — | dropdown แสดง 3 ตัวเลือก (รอบครึ่งปีหลัง / โบนัสปลายปี / ทดลองงาน) | ☐ |
| 4 | CLICK ตัวเลือก **รอบครึ่งปีหลัง 2569 (ก.ค.–ธ.ค.)** | — | ช่องแสดงค่าที่เลือก · error "กรุณาเลือกรอบจากตั้งค่า HR" ไม่ขึ้น | ☐ |
| 5 | CLICK ปุ่ม **สร้างและเปิดกรอก** | — | ปุ่มขึ้น "กำลังบันทึก…" ชั่วครู่ | ☐ |
| 6 | WAIT จน toast ปรากฏ (≤3s) | — | toast **สร้างรอบ · เปิดกรอก · แจ้งเตือนผู้เข้าร่วมแล้ว** + drawer ปิด | ☐ |
| 7 | VERIFY แถวบนสุดของตารางรอบ | — | เห็น "รอบใหม่ 2569" pill **เปิดกรอก** (badge แท็บ "รอบประเมิน" +1) | ☐ |

#### TC-CY02 — สร้างรอบโดยไม่เลือกรอบ (negative · validate)
- group: รอบประเมิน · ความสำคัญ: สูง · trace: FN-01 / AC-01 / VR (config select)
- actor: HR · Setup: role=hr · seed=default · files=—
- Start: OPEN performance.html → CLICK ปุ่ม **สร้างรอบประเมิน**
- ผ่านเมื่อ: block + toast "กรุณาเลือกรอบจากตั้งค่า HR" + ช่องเลือกรอบขึ้นสถานะ invalid

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY drawer **สร้างรอบประเมิน** เปิด | — | ช่อง "เลือกรอบจาก ตั้งค่า HR" ว่าง | ☐ |
| 2 | CLICK ปุ่ม **สร้างและเปิดกรอก** (ยังไม่เลือกรอบ) | — | toast **กรุณาเลือกรอบจากตั้งค่า HR** + ช่องเลือกรอบไฮไลต์ error (is-invalid) | ☐ |
| 3 | VERIFY ตารางรอบ | — | ไม่มีรอบใหม่ถูกเพิ่ม (badge เท่าเดิม) | ☐ |

#### TC-CY03 — บทบาทอื่นไม่มีปุ่มสร้างรอบ (permission)
- group: รอบประเมิน · ความสำคัญ: สูง · trace: FN-01 / §5.3 (create=manage) / FIX-03
- actor: พนักงาน + หัวหน้าสายงาน · Setup: role=staff→mgr · seed=default · files=—
- Start: OPEN performance.html
- ผ่านเมื่อ: ปุ่ม "สร้างรอบประเมิน" ไม่ render ให้ staff และ mgr

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **พนักงาน** (demo strip) | — | ชื่อผู้ใช้มุมขวา = "สมชาย ใจดี" · role = พนักงาน | ☐ |
| 2 | VERIFY มุมขวาบนของแท็บ "รอบประเมิน" | — | **ไม่มี** ปุ่ม "สร้างรอบประเมิน" | ☐ |
| 3 | CLICK ปุ่ม **หัวหน้าสายงาน** (demo strip) | — | ชื่อผู้ใช้ = "ประสงค์ ชัยมงคล" | ☐ |
| 4 | VERIFY มุมขวาบน | — | **ไม่มี** ปุ่ม "สร้างรอบประเมิน" | ☐ |

#### TC-CY04 — เปิด drawer รอบ + ปิดรอบ (happy)
- group: รอบประเมิน · ความสำคัญ: สูง · trace: FN-11 / AC-02 / BR-09 / FN-91
- actor: HR · Setup: role=hr · seed=CY1 open · files=—
- Start: OPEN performance.html (แท็บ "รอบประเมิน")
- ผ่านเมื่อ: modal ยืนยัน → toast "ปิดรอบแล้ว · ล็อกการแก้ไข (soft archive)" + pill รอบ CY1 = "ปิดรอบ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **CY1 · รอบครึ่งปีหลัง 2569** | — | drawer viewCycle เปิด แสดงรายละเอียดรอบ | ☐ |
| 2 | VERIFY ปุ่มใน drawer | — | เห็นปุ่ม **ปิดรอบ** (แดง · เฉพาะ HR + รอบ open) | ☐ |
| 3 | CLICK ปุ่ม **ปิดรอบ** | — | modal **ปิดรอบประเมิน?** + subtitle "ปิดรอบจะล็อกการแก้ไขทั้งหมด (soft archive) — ย้อนกลับไม่ได้" | ☐ |
| 4 | VERIFY เนื้อ modal | — | ข้อความ 'ต้องการปิดรอบ "รอบครึ่งปีหลัง 2569" ใช่หรือไม่' + ปุ่ม "ยกเลิก"/"ปิดรอบ" | ☐ |
| 5 | CLICK ปุ่ม **ปิดรอบ** (ใน modal) | — | ปุ่มขึ้น "กำลังปิด…" | ☐ |
| 6 | WAIT จน toast ปรากฏ | — | toast **ปิดรอบแล้ว · ล็อกการแก้ไข (soft archive)** + modal+drawer ปิด | ☐ |
| 7 | VERIFY แถว CY1 ในตาราง | — | pill สถานะ = **ปิดรอบ** (pill-muted) | ☐ |

#### TC-CY05 — รอบปิดแล้ว = แก้ไขไม่ได้ (edge: EC-07 · closed read-only)
- group: รอบประเมิน · ความสำคัญ: สูง · trace: FN-11 / AC-02 / VR-04 / BR_CYCLE_CLOSED / guard layer 1
- actor: HR · Setup: role=hr · seed=ปิด CY1 ก่อน (ทำตาม TC-CY04 ในเซสชันเดียว) · files=—
- Start: หลังปิด CY1 → CLICK แท็บ **แบบประเมินรายคน**
- ผ่านเมื่อ: เปิด appraisal → tab KPI แสดง banner read-only + ไม่มีปุ่มบันทึก/mutation

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **แบบประเมินรายคน** | — | ตารางแบบประเมินรอบ CY1 (6 แถว) | ☐ |
| 2 | CLICK แถว **มะลิ ดอกไม้ (A1)** | — | drawer เปิด tab "รายละเอียด" | ☐ |
| 3 | CLICK tab **KPI / คะแนน** (ใน drawer) | — | banner is-warn **รอบนี้ปิดแล้ว — ดูได้อย่างเดียว แก้ไขไม่ได้** | ☐ |
| 4 | VERIFY ส่วน KPI | — | ตาราง KPI แสดงแบบอ่านอย่างเดียว · **ไม่มี** ปุ่ม "บันทึกเป้า/KPI"/"เพิ่ม KPI" | ☐ |
| 5 | VERIFY footer drawer | — | มีแต่ปุ่ม "ปิด" · ไม่มีปุ่ม mutation | ☐ |

#### TC-CY06 — badge นับรอบ + pill สถานะรอบถูกต้อง (VERIFY)
- group: รอบประเมิน · ความสำคัญ: ต่ำ · trace: FN-01 / 01_UI P-01
- actor: HR · Setup: role=hr · seed=default · files=—
- Start: OPEN performance.html
- ผ่านเมื่อ: ตารางรอบ 2 แถว pill ตรง seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY badge แท็บ "รอบประเมิน" | — | = 2 | ☐ |
| 2 | VERIFY แถว CY1 | — | pill **เปิดกรอก** (เขียว) · คอลัมน์ "แบบประเมิน" = 6 | ☐ |
| 3 | VERIFY แถว CY2 · รอบครึ่งปีแรก 2569 | — | pill **ปิดรอบ** (เทา) · แบบประเมิน = 0 | ☐ |

#### TC-CY07 — sub-note รอบอ้าง ตั้งค่า HR (VERIFY · LK-3 surface)
- group: รอบประเมิน · ความสำคัญ: ต่ำ · trace: FN-01 / LK-3 / CD-02 (ไม่โชว์ id ภายใน)
- actor: HR · Setup: role=hr · seed=default · files=—
- Start: OPEN performance.html
- ผ่านเมื่อ: แต่ละแถวรอบมี sub-note "อ้าง … (อ่านจาก ตั้งค่า HR)" และไม่โชว์ #107/snake_case

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ใต้ชื่อรอบ CY1 | — | sub-note **อ้าง แบบฟอร์มประเมินมาตรฐาน (อ่านจาก ตั้งค่า HR)** | ☐ |
| 2 | VERIFY ทั้งหน้า | — | ไม่มีเลข "#107" / "appraisal_cycle" / snake_case โผล่บนจอ | ☐ |

---

### กลุ่ม TC-KP · KPI / ตั้งเป้า (Σweight=100)

#### TC-KP01 — ตั้งเป้า/KPI ครบ Σ=100 (happy)
- group: KPI · ความสำคัญ: สูง · trace: FN-02 / AC-03 / BR-02 / state goal→self
- actor: HR · Setup: role=hr · seed=A1 (goal, KPI 60+40=100) · files=—
- Start: OPEN performance.html → CLICK แท็บ **แบบประเมินรายคน** → CLICK แถว **มะลิ ดอกไม้ (A1)** → CLICK tab **KPI / คะแนน**
- ผ่านเมื่อ: tag "น้ำหนักรวม 100%" (ok) + บันทึกได้ → toast "บันทึกเป้า/KPI แล้ว · เปิดให้พนักงานประเมินตนเอง" + สถานะ A1 → ประเมินตนเอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัวข้อ KPI editor | — | เห็น **ตั้งเป้า / KPI** + tag เขียว **น้ำหนักรวม 100%** | ☐ |
| 2 | VERIFY 2 แถว KPI | — | "ความถูกต้องสต๊อก" 60% · "ความปลอดภัยในการทำงาน" 40% (แก้ได้) + ปุ่ม "เพิ่ม KPI" | ☐ |
| 3 | CLICK ปุ่ม **บันทึกเป้า/KPI** | — | ปุ่มขึ้น "กำลังบันทึก…" | ☐ |
| 4 | WAIT จน toast ปรากฏ | — | toast **บันทึกเป้า/KPI แล้ว · เปิดให้พนักงานประเมินตนเอง** | ☐ |
| 5 | VERIFY แถว A1 ในตาราง (ปิด drawer) | — | pill สถานะ = **ประเมินตนเอง** (เดิม "ตั้งเป้า") | ☐ |

#### TC-KP02 — น้ำหนัก KPI รวม ≠ 100 (negative · VR-01)
- group: KPI · ความสำคัญ: สูง · trace: FN-02 / AC-03 / VR-01 / BR_KPI_WEIGHT_NOT_100
- actor: HR · Setup: role=hr · seed=A1 (goal) · files=—
- Start: OPEN performance.html → แท็บ **แบบประเมินรายคน** → แถว **A1 มะลิ ดอกไม้** → tab **KPI / คะแนน**
- ผ่านเมื่อ: แก้น้ำหนักให้รวม 90 → tag แดง "น้ำหนักรวม 90% ≠ 100" + บันทึก block toast "น้ำหนัก KPI รวมต้องเท่ากับ 100% (ตอนนี้ 90%)"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "50" → ช่องน้ำหนักแถวแรก (ความถูกต้องสต๊อก) | KPI-BAD-SUM | tag เปลี่ยนเป็นแดง **น้ำหนักรวม 90% ≠ 100** (สด ไม่ต้อง save) | ☐ |
| 2 | CLICK ปุ่ม **บันทึกเป้า/KPI** | — | toast **น้ำหนัก KPI รวมต้องเท่ากับ 100% (ตอนนี้ 90%)** | ☐ |
| 3 | VERIFY สถานะ A1 | — | ยังเป็น "ตั้งเป้า" (ไม่เลื่อนขั้น) | ☐ |

#### TC-KP03 — ชื่อ KPI ว่าง (negative · VR-09)
- group: KPI · ความสำคัญ: กลาง · trace: FN-02 / VR-09 / BR_KPI_TITLE_REQUIRED
- actor: HR · Setup: role=hr · seed=A1 (goal) · files=—
- Start: OPEN performance.html → แท็บ **แบบประเมินรายคน** → แถว **A1** → tab **KPI / คะแนน**
- ผ่านเมื่อ: เว้นชื่อ KPI ว่าง → toast "กรุณากรอกชื่อ KPI ให้ครบ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **เพิ่ม KPI** | — | แถว KPI ใหม่ว่าง (ชื่อว่าง · น้ำหนัก 0) | ☐ |
| 2 | CLICK ปุ่ม **บันทึกเป้า/KPI** (มีแถวชื่อว่าง) | KPI-BAD-NAME | toast **กรุณากรอกชื่อ KPI ให้ครบ** | ☐ |

#### TC-KP04 — เพิ่ม/ลบแถว KPI (edit) + tag อัปเดตสด
- group: KPI · ความสำคัญ: ต่ำ · trace: FN-02 / KPI editor
- actor: HR · Setup: role=hr · seed=A1 (goal) · files=—
- Start: OPEN performance.html → แท็บ **แบบประเมินรายคน** → แถว **A1** → tab **KPI / คะแนน**
- ผ่านเมื่อ: เพิ่มแถวได้/ลบแถวได้ + tag น้ำหนักรวมคำนวณใหม่ทันที

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **เพิ่ม KPI** | — | มี 3 แถว KPI | ☐ |
| 2 | CLICK ไอคอนถังขยะ ท้ายแถวที่ 3 | — | กลับเหลือ 2 แถว | ☐ |
| 3 | TYPE "30" → น้ำหนักแถวแรก | — | tag แดง **น้ำหนักรวม 70% ≠ 100** (30+40) | ☐ |

#### TC-KP05 — KPI ที่ขั้นอื่นไม่ให้แก้ (stage-gated editor · VERIFY)
- group: KPI · ความสำคัญ: กลาง · trace: FN-02 / FIX-02 / EC-02 (UI evidence)
- actor: HR · Setup: role=hr · seed=A4 (calibration) · files=—
- Start: OPEN performance.html → แท็บ **แบบประเมินรายคน** → แถว **ธนากร พูนผล (A4)** → tab **KPI / คะแนน**
- ผ่านเมื่อ: KPI editor ไม่ให้แก้ (อ่านอย่างเดียว) เพราะ A4 อยู่ขั้น calibration ไม่ใช่ goal

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตาราง KPI ของ A4 | — | แสดงคะแนน (ตนเอง/หัวหน้า) แบบอ่านอย่างเดียว · **ไม่มี** ช่องแก้ชื่อ/น้ำหนัก · ไม่มีปุ่ม "บันทึกเป้า/KPI"/"เพิ่ม KPI" | ☐ |
| 2 | VERIFY totbox | — | "คะแนนรวมถ่วงน้ำหนัก (หัวหน้า): 4.60 / 5" | ☐ |

---

### กลุ่ม TC-SF · ประเมินตนเอง

#### TC-SF01 — พนักงานประเมินตนเองครบทุก KPI (happy)
- group: ประเมินตนเอง · ความสำคัญ: สูง · trace: FN-03 / AC-04 / BR-03 / state self→mgr
- actor: พนักงาน (สมชาย ใจดี = A2) · Setup: role=staff · seed=A2 (self, 3 KPI) · files=—
- Start: OPEN performance.html → CLICK ปุ่ม **พนักงาน** (demo strip) → CLICK แท็บ **แบบประเมินรายคน** → CLICK แถว **สมชาย ใจดี (A2)** → CLICK tab **KPI / คะแนน**
- ผ่านเมื่อ: กรอกคะแนนตนเอง 1–5 ครบ → toast "บันทึกประเมินตนเองแล้ว · ส่งต่อหัวหน้าประเมิน" + สถานะ A2 → หัวหน้าประเมิน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หลังสลับ role | — | ชื่อผู้ใช้มุมขวา = "สมชาย ใจดี" · ตารางเห็นเฉพาะแถวของตน (A2) | ☐ |
| 2 | VERIFY tab KPI | — | คอลัมน์ "ตนเอง" เป็นช่องกรอกได้ (input 1–5) 3 แถว | ☐ |
| 3 | TYPE "4" → ช่องตนเองแถว 1 (ส่งงานตรงเวลา) | — | ช่องรับค่า | ☐ |
| 4 | TYPE "4" → ช่องตนเองแถว 2 (คุณภาพงาน) | — | ช่องรับค่า | ☐ |
| 5 | TYPE "5" → ช่องตนเองแถว 3 (ทำงานเป็นทีม) | — | ช่องรับค่า | ☐ |
| 6 | CLICK ปุ่ม **บันทึกประเมินตนเอง** | — | ปุ่ม "กำลังบันทึก…" | ☐ |
| 7 | WAIT จน toast ปรากฏ | — | toast **บันทึกประเมินตนเองแล้ว · ส่งต่อหัวหน้าประเมิน** | ☐ |
| 8 | VERIFY แถว A2 | — | pill = **หัวหน้าประเมิน** | ☐ |

#### TC-SF02 — คะแนนตนเองไม่ครบ (negative · VR-08)
- group: ประเมินตนเอง · ความสำคัญ: สูง · trace: FN-03 / VR-08 / BR_SELF_SCORE_INCOMPLETE
- actor: พนักงาน · Setup: role=staff · seed=A2 (self) · files=—
- Start: OPEN performance.html → ปุ่ม **พนักงาน** → แท็บ **แบบประเมินรายคน** → แถว **A2** → tab **KPI / คะแนน**
- ผ่านเมื่อ: ปล่อยช่องตนเองว่าง ≥1 → toast "กรุณาให้คะแนนตนเองครบทุก KPI (1–5)"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "4" → ช่องตนเองแถว 1 (เว้นแถว 2,3 ว่าง) | — | เฉพาะแถว 1 มีค่า | ☐ |
| 2 | CLICK ปุ่ม **บันทึกประเมินตนเอง** | — | toast **กรุณาให้คะแนนตนเองครบทุก KPI (1–5)** | ☐ |
| 3 | VERIFY สถานะ A2 | — | ยัง "ประเมินตนเอง" | ☐ |

#### TC-SF03 — พนักงานเปิด KPI ก่อนถึงขั้นตนเอง (stage · VERIFY)
- group: ประเมินตนเอง · ความสำคัญ: ต่ำ · trace: FN-03 / BR-03 (self ก่อน mgr enforced by state)
- actor: HR (ดูสถานะขั้น) · Setup: role=hr · seed=A1 (goal, ยังไม่ถึง self) · files=—
- Start: OPEN performance.html → แท็บ **แบบประเมินรายคน** → แถว **A1** → tab **KPI / คะแนน**
- ผ่านเมื่อ: A1 (goal) ไม่มีช่องกรอกคะแนน "ตนเอง"/"หัวหน้า" (ต้องผ่านขั้นตั้งเป้าก่อน)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY A1 tab KPI | — | อยู่ในโหมด KPI editor (ตั้งเป้า) · ยังไม่มีคอลัมน์กรอกคะแนน "ตนเอง"/"หัวหน้า" | ☐ |

---

### กลุ่ม TC-MG · หัวหน้าประเมิน + weighted

#### TC-MG01 — HR บันทึกผลหัวหน้า (happy · mgr∥manage)
- group: หัวหน้าประเมิน · ความสำคัญ: สูง · trace: FN-04 / AC-05 / BR-04 / state mgr→calibration
- actor: HR (manage · เพราะ mgr persona เข้าไม่ถึง A3 · OQ-PERF-11) · Setup: role=hr · seed=A3 (mgr stage, ฝ่ายบัญชี) · files=—
- Start: OPEN performance.html → แท็บ **แบบประเมินรายคน** → CLICK แถว **อรทัย แสนสุข (A3)** → CLICK tab **KPI / คะแนน**
- ผ่านเมื่อ: กรอกคะแนนหัวหน้า 1–5 ครบ → toast "บันทึกผลหัวหน้าแล้ว · ส่งเข้าสอบทาน (DOA)" + สถานะ A3 → รอสอบทาน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY tab KPI ของ A3 | — | คอลัมน์ "หัวหน้า" เป็นช่องกรอก (input 1–5) · totbox "คะแนนรวมถ่วงน้ำหนัก (หัวหน้า)" | ☐ |
| 2 | TYPE "5" → ช่องหัวหน้าแถว 1 (ปิดงบตรงเวลา · w50) | — | liveScore อัปเดต | ☐ |
| 3 | TYPE "4" → ช่องหัวหน้าแถว 2 (ความแม่นยำ · w50) | — | **liveScore = 4.50 / 5** ((5×50+4×50)/100) | ☐ |
| 4 | CLICK ปุ่ม **บันทึกผลหัวหน้า** | — | ปุ่ม "กำลังบันทึก…" | ☐ |
| 5 | WAIT จน toast ปรากฏ | — | toast **บันทึกผลหัวหน้าแล้ว · ส่งเข้าสอบทาน (DOA)** | ☐ |
| 6 | VERIFY แถว A3 | — | pill = **รอสอบทาน** | ☐ |

#### TC-MG02 — คะแนนถ่วงน้ำหนักคำนวณถูก (VERIFY · BR-04)
- group: หัวหน้าประเมิน · ความสำคัญ: สูง · trace: FN-04 / FN-19 / BR-04 (weighted invariant)
- actor: HR · Setup: role=hr · seed=A4 (calibration, mgr score 5/4 · w60/40) · files=—
- Start: OPEN performance.html → แท็บ **แบบประเมินรายคน** → แถว **ธนากร พูนผล (A4)** → tab **KPI / คะแนน**
- ผ่านเมื่อ: คะแนนรวม = 4.60 (= (5×60 + 4×40)/100)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY totbox tab KPI | — | "คะแนนรวมถ่วงน้ำหนัก (หัวหน้า): **4.60 / 5**" | ☐ |
| 2 | CLICK tab **รายละเอียด** | — | ช่อง "คะแนนรวม (หัวหน้า)" = **4.60 / 5** (สอดคล้อง) | ☐ |

#### TC-MG03 — คะแนนหัวหน้าไม่ครบ (negative · VR-08)
- group: หัวหน้าประเมิน · ความสำคัญ: กลาง · trace: FN-04 / VR-08 / BR_MGR_SCORE_INCOMPLETE
- actor: HR · Setup: role=hr · seed=A3 (mgr stage) · files=—
- Start: OPEN performance.html → แท็บ **แบบประเมินรายคน** → แถว **A3** → tab **KPI / คะแนน**
- ผ่านเมื่อ: เว้นคะแนนหัวหน้า ≥1 ช่อง → toast "กรุณาให้คะแนนหัวหน้าครบทุก KPI (1–5)"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "5" → ช่องหัวหน้าแถว 1 (เว้นแถว 2 ว่าง) | — | เฉพาะแถว 1 มีค่า | ☐ |
| 2 | CLICK ปุ่ม **บันทึกผลหัวหน้า** | — | toast **กรุณาให้คะแนนหัวหน้าครบทุก KPI (1–5)** | ☐ |
| 3 | VERIFY สถานะ A3 | — | ยัง "หัวหน้าประเมิน" | ☐ |

#### TC-MG04 — พนักงานไม่มีสิทธิ์บันทึกผลหัวหน้า (permission · VERIFY)
- group: หัวหน้าประเมิน · ความสำคัญ: กลาง · trace: FN-04 / §5.3 / FIX-03 (saveMgr = mgr∥manage)
- actor: พนักงาน · Setup: role=staff · seed=default · files=—
- Start: OPEN performance.html → ปุ่ม **พนักงาน** → แท็บ **แบบประเมินรายคน**
- ผ่านเมื่อ: staff เห็นเฉพาะ A2 (ขั้น self ของตน) · ไม่มีคอลัมน์/ปุ่ม "บันทึกผลหัวหน้า" ที่ไหน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตารางของ staff | — | มีเฉพาะแถวของตน (สมชาย ใจดี) · ไม่มี A3 หรือแบบประเมินขั้น mgr ของผู้อื่น | ☐ |
| 2 | CLICK แถว **สมชาย ใจดี (A2)** → tab **KPI / คะแนน** | — | มีเฉพาะช่องกรอก "ตนเอง" + ปุ่ม "บันทึกประเมินตนเอง" · **ไม่มี** ปุ่ม "บันทึกผลหัวหน้า" | ☐ |

---

### กลุ่ม TC-CB · สอบทาน (staged DOA)

#### TC-CB01 — ส่งสอบทาน: เลือกผู้สอบทาน 2 ขั้น (happy jังหวะ 1 · freeze)
- group: สอบทาน · ความสำคัญ: สูง · trace: FN-08 / AC-08 / BR-05 / LD-02 / EC-08
- actor: HR · Setup: role=hr · seed=A4 (calibration, ยังไม่มี approvals) · files=—
- Start: OPEN performance.html → CLICK แท็บ **สอบทาน + ผล & Gap**
- ผ่านเมื่อ: 2 slot ว่าง → เลือกครบ → "ส่งสอบทาน" → toast "ส่งสอบทานแล้ว · รอผู้สอบทานขั้นที่ 1 บันทึกผล" + A4 คงสถานะ "รอสอบทาน" (ยังไม่ published)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section **รอสอบทาน (calibration · DOA)** | — | มีแถว "ธนากร พูนผล" + ปุ่ม **สอบทาน (DOA)** | ☐ |
| 2 | CLICK ปุ่ม **สอบทาน (DOA)** (แถว ธนากร) | — | modal **สอบทานผล (DOA) — เลือกผู้สอบทาน** · subtitle "ธนากร พูนผล · คะแนน 4.60 / 5" | ☐ |
| 3 | VERIFY 2 slot | — | slot 1 = "หัวหน้าสายงาน" · slot 2 = "ผู้สอบทาน (HRBP/ผู้บริหาร)" · **ทั้งคู่ว่าง** (placeholder "เลือกผู้สอบทาน…") | ☐ |
| 4 | CLICK slot 1 → CLICK ตัวเลือก **ประสงค์ ชัยมงคล** | — | slot 1 แสดง "ประสงค์ ชัยมงคล" | ☐ |
| 5 | CLICK slot 2 → CLICK ตัวเลือก **วิชัย เจริญสุข** | — | slot 2 แสดง "วิชัย เจริญสุข" | ☐ |
| 6 | CLICK ปุ่ม **ส่งสอบทาน** | — | ปุ่ม "กำลังส่ง…" | ☐ |
| 7 | WAIT จน toast ปรากฏ | — | toast **ส่งสอบทานแล้ว · รอผู้สอบทานขั้นที่ 1 บันทึกผล** | ☐ |
| 8 | VERIFY แถว A4 | — | ยังอยู่ section "รอสอบทาน" (pill ยัง "รอสอบทาน" · **ไม่** เลื่อนไปผลเผยแพร่) | ☐ |

#### TC-CB02 — ส่งสอบทานโดย slot ว่าง (negative · VR-02)
- group: สอบทาน · ความสำคัญ: สูง · trace: FN-08 / VR-02 / BR_REVIEWER_SLOT_EMPTY
- actor: HR · Setup: role=hr · seed=A4 (calibration, ยังไม่มี approvals) · files=—
- Start: OPEN performance.html → แท็บ **สอบทาน + ผล & Gap** → CLICK **สอบทาน (DOA)** (แถว ธนากร)
- ผ่านเมื่อ: กด "ส่งสอบทาน" โดยไม่เลือกครบ → toast "กรุณาเลือกผู้สอบทานให้ครบทุกขั้น"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งสอบทาน** (ยังไม่เลือก slot ใด) | — | toast **กรุณาเลือกผู้สอบทานให้ครบทุกขั้น** | ☐ |
| 2 | CLICK slot 1 → เลือก **ประสงค์ ชัยมงคล** (slot 2 ยังว่าง) | — | slot 1 มีค่า | ☐ |
| 3 | CLICK ปุ่ม **ส่งสอบทาน** | — | toast **กรุณาเลือกผู้สอบทานให้ครบทุกขั้น** (ยังบล็อกเพราะ slot 2 ว่าง) | ☐ |

#### TC-CB03 — บันทึกผลสอบทานขั้น 1 (jังหวะ 2 · ยังไม่เผยแพร่)
- group: สอบทาน · ความสำคัญ: สูง · trace: FN-05/08 / AC-08 / BR-05 (publish หลังขั้นสุดท้าย)
- actor: HR (แทนผู้สอบทานขั้น current ในโปรโต) · Setup: role=hr · seed=A4 หลังส่งสอบทานแล้ว (ทำ TC-CB01 ก่อนในเซสชันเดียว) · files=—
- Start: หลัง TC-CB01 → แท็บ **สอบทาน + ผล & Gap** → CLICK **สอบทาน (DOA)** (แถว ธนากร)
- ผ่านเมื่อ: timeline 2 ขั้น (ขั้น 1 current) → "บันทึกผลสอบทานขั้น 1" → toast "บันทึกผลสอบทานขั้น 1 แล้ว · รอผู้สอบทานขั้นถัดไป" + ยัง "รอสอบทาน"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY modal เปิดในโหมดบันทึกผล | — | หัวข้อ **สอบทานผล (DOA) — บันทึกผลรายขั้น** + timeline: ขั้น 1 (ประสงค์) "รอบันทึกผล (ขั้นนี้)" · ขั้น 2 (วิชัย) "รอคิว" | ☐ |
| 2 | VERIFY ปุ่ม + note | — | ปุ่ม **บันทึกผลสอบทานขั้น 1** · note "บันทึกผลขั้นนี้แล้วส่งต่อผู้สอบทานขั้นถัดไป (ยังไม่เผยแพร่)" · **ไม่มี** dropdown ผลการตัดสิน | ☐ |
| 3 | CLICK ปุ่ม **บันทึกผลสอบทานขั้น 1** | — | ปุ่ม "กำลังบันทึก…" | ☐ |
| 4 | WAIT จน toast ปรากฏ | — | toast **บันทึกผลสอบทานขั้น 1 แล้ว · รอผู้สอบทานขั้นถัดไป** | ☐ |
| 5 | VERIFY แถว A4 | — | ยัง section "รอสอบทาน" · **ไม่** อยู่ผลเผยแพร่ (publish ยังไม่เกิด) | ☐ |

#### TC-CB04 — บันทึกผล + เผยแพร่ผล (ขั้นสุดท้าย · publish + CSQ)
- group: สอบทาน · ความสำคัญ: สูง · trace: FN-05 / AC-07 / BR-05 / BR-13 / CSQ per-person / XT-04
- actor: HR · Setup: role=hr · seed=A4 หลังบันทึกขั้น 1 แล้ว (ทำ TC-CB01→CB03 ในเซสชันเดียว) · files=—
- Start: หลัง TC-CB03 → แท็บ **สอบทาน + ผล & Gap** → CLICK **สอบทาน (DOA)** (แถว ธนากร)
- ผ่านเมื่อ: ขั้น 2 current + isLast → เลือก decision → "บันทึกผล + เผยแพร่ผล" → toast "เผยแพร่ผล · บันทึกผลเข้า 7C · RESTRICTED · แจ้งเตือนพนักงานแล้ว" + A4 → เผยแพร่ผล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY timeline | — | ขั้น 1 (ประสงค์) "บันทึกแล้ว …" · ขั้น 2 (วิชัย) "รอบันทึกผล (ขั้นนี้)" | ☐ |
| 2 | VERIFY ขั้นสุดท้าย | — | มี dropdown **ผลการตัดสิน** (ผ่าน / ทบทวน (เปิด PIP) / ไม่ผ่าน) · ปุ่ม **บันทึกผล + เผยแพร่ผล** · note "ขั้นสุดท้าย: บันทึกแล้วเผยแพร่ผล …" | ☐ |
| 3 | SELECT "ผ่าน" → dropdown **ผลการตัดสิน** | — | เลือก "ผ่าน" | ☐ |
| 4 | CLICK ปุ่ม **บันทึกผล + เผยแพร่ผล** | — | ปุ่ม "กำลังบันทึก…" | ☐ |
| 5 | WAIT จน toast ปรากฏ | — | toast **เผยแพร่ผล · บันทึกผลเข้า 7C · RESTRICTED · แจ้งเตือนพนักงานแล้ว** + modal ปิด | ☐ |
| 6 | VERIFY section "ผล & Gap (เผยแพร่แล้ว)" | — | มีแถว "ธนากร พูนผล … decision: ผ่าน" (เพิ่มเข้ามา) | ☐ |
| 7 | CLICK แท็บ **แบบประเมินรายคน** → แถว **ธนากร** → tab **ประวัติ** | — | รายการบนสุดมี "เผยแพร่ผล · decision: ผ่าน" และ "บันทึกผลประเมินเข้า 7C" (CSQ hook · newest-first) | ☐ |

#### TC-CB05 — slot ว่างจริง ไม่ preset (edge: EC-08 · LK-1 surface)
- group: สอบทาน · ความสำคัญ: สูง · trace: FN-08 / EC-08 / LK-1 / FIX-06
- actor: HR · Setup: role=hr · seed=A4 (calibration, ยังไม่ส่งสอบทาน) · files=—
- Start: OPEN performance.html → แท็บ **สอบทาน + ผล & Gap** → CLICK **สอบทาน (DOA)** (แถว ธนากร)
- ผ่านเมื่อ: ทั้ง 2 slot ว่าง (ไม่ preset ชื่อใด) + มี note "เลือกครบทั้ง 2 ขั้นก่อนส่งสอบทาน"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY 2 slot ตอนเปิด modal | — | slot 1 + slot 2 = placeholder "เลือกผู้สอบทาน…" · **ไม่มี** ชื่อ preset | ☐ |
| 2 | VERIFY note ใต้ slot | — | note is-warn "ผล/คะแนน = RESTRICTED · เลือกครบทั้ง 2 ขั้นก่อนส่งสอบทาน" | ☐ |
| 3 | CLICK slot 1 (search-select) | — | รายชื่อบุคคลจริงให้เลือก (ประสงค์/สุนิสา/วิชัย/อรพิน/ธีรพงษ์) | ☐ |

#### TC-CB06 — ไม่มีคิวสอบทาน (empty state)
- group: สอบทาน · ความสำคัญ: ต่ำ · trace: FN-05 / 01_UI §1.6 (empty queue)
- actor: HR · Setup: role=hr · seed=สอบทาน A4 จนเผยแพร่แล้ว (ทำ TC-CB01→CB04 ก่อน) · files=—
- Start: หลัง A4 published → แท็บ **สอบทาน + ผล & Gap**
- ผ่านเมื่อ: section รอสอบทานว่าง → "ไม่มีแบบประเมินที่รอสอบทาน"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section **รอสอบทาน (calibration · DOA)** | — | ข้อความ **ไม่มีแบบประเมินที่รอสอบทาน** (ไม่มี A ใดค้าง calibration) | ☐ |

#### TC-CB07 — decision 3 ตัวเลือกครบ (VERIFY · state machine)
- group: สอบทาน · ความสำคัญ: กลาง · trace: FN-05 / AC-07 / decision ∈ {ผ่าน/ทบทวน/ไม่ผ่าน}
- actor: HR · Setup: role=hr · seed=A4 หลังบันทึกถึงขั้นสุดท้าย (TC-CB01→CB03) · files=—
- Start: เปิด modal DOA ของ A4 ที่ขั้นสุดท้าย
- ผ่านเมื่อ: dropdown ผลการตัดสินมี 3 ค่าตรงตาม spec

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK dropdown **ผลการตัดสิน** | — | 3 ตัวเลือก: **ผ่าน** · **ทบทวน (เปิด PIP)** · **ไม่ผ่าน** | ☐ |

---

### กลุ่ม TC-PB · ผล/Gap + hooks (display-only)

#### TC-PB01 — ส่งไปอบรม (gap → Training hook)
- group: ผล/Gap · ความสำคัญ: สูง · trace: FN-06 / AC-09 / BR-06 / LK-5 / XT-02
- actor: HR · Setup: role=hr · seed=A5 (published, gap="ทักษะการนำเสนอ") · files=—
- Start: OPEN performance.html → CLICK แท็บ **สอบทาน + ผล & Gap**
- ผ่านเมื่อ: ปุ่ม "ส่งไปอบรม" → toast 'ส่งจุดที่ต้องพัฒนา "ทักษะการนำเสนอ" ไปหลักสูตรอบรม (ส่งต่อ ไม่แก้ที่นี่) — ไม่สร้างหลักสูตรในหน้านี้'

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section "ผล & Gap (เผยแพร่แล้ว)" แถว กนกพร วงศ์ไทย | — | hookbox "Gap ที่พบ: **ทักษะการนำเสนอ**" + ปุ่ม **ส่งไปอบรม** | ☐ |
| 2 | CLICK ปุ่ม **ส่งไปอบรม** | — | toast **ส่งจุดที่ต้องพัฒนา "ทักษะการนำเสนอ" ไปหลักสูตรอบรม (ส่งต่อ ไม่แก้ที่นี่) — ไม่สร้างหลักสูตรในหน้านี้** | ☐ |
| 3 | VERIFY หน้าจอ | — | ไม่มีการสร้าง/เปลี่ยนข้อมูล gap หรือหลักสูตรบนจอ (hook อย่างเดียว) | ☐ |

#### TC-PB02 — ส่งเรื่องปรับตำแหน่ง/เงินเดือน (Movement event)
- group: ผล/Gap · ความสำคัญ: สูง · trace: FN-07 / AC-10 / BR-07 / LK-2 / XT-01
- actor: HR · Setup: role=hr · seed=A5 (published) · files=—
- Start: OPEN performance.html → แท็บ **สอบทาน + ผล & Gap**
- ผ่านเมื่อ: ปุ่ม "ส่งเรื่องปรับตำแหน่ง/เงินเดือน" → toast "ส่งเรื่องปรับเงินเดือน/เลื่อนตำแหน่งให้ระบบโยกย้าย (ไม่ปรับเอง)" + ไม่มีการแก้เงินเดือน/ตำแหน่งบนจอ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งเรื่องปรับตำแหน่ง/เงินเดือน** (แถว กนกพร) | — | toast **ส่งเรื่องปรับเงินเดือน/เลื่อนตำแหน่งให้ระบบโยกย้าย (ไม่ปรับเอง)** | ☐ |
| 2 | VERIFY หน้าจอ | — | ไม่มีฟิลด์เงินเดือน/ตำแหน่งให้แก้ (event อย่างเดียว · decouple จาก gap) | ☐ |

#### TC-PB03 — ส่งเข้า Succession (top/ผ่าน เท่านั้น)
- group: ผล/Gap · ความสำคัญ: กลาง · trace: FN-07 / XT-03 / FIX-09 (topPerf)
- actor: HR · Setup: role=hr · seed=A5 (ผ่าน · top) + A6 (ทบทวน · ไม่ top) · files=—
- Start: OPEN performance.html → แท็บ **สอบทาน + ผล & Gap**
- ผ่านเมื่อ: A5 (ผ่าน) มีปุ่ม "ส่งเข้า Succession Planning" → toast "ส่งผลเข้า Succession Planning (ส่งต่อ ไม่แก้ที่นี่)"; A6 (ทบทวน, คะแนน 2.30) ไม่มีปุ่มนี้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถว กนกพร (A5 · ผ่าน) | — | มีปุ่ม **ส่งเข้า Succession Planning** | ☐ |
| 2 | CLICK ปุ่ม **ส่งเข้า Succession Planning** | — | toast **ส่งผลเข้า Succession Planning (ส่งต่อ ไม่แก้ที่นี่)** | ☐ |
| 3 | VERIFY แถว ปิยะ (A6 · ทบทวน · 2.30) | — | **ไม่มี** ปุ่ม "ส่งเข้า Succession Planning" (ไม่ใช่ top/ผ่าน) | ☐ |

#### TC-PB04 — top ไม่มี gap ยังส่ง Movement ได้ (decouple · VERIFY)
- group: ผล/Gap · ความสำคัญ: ต่ำ · trace: FN-07 / BR-07 (ส่งได้ทุกผล published · decouple gap)
- actor: HR · Setup: role=hr · seed=A5 (มี gap) · files=—
- Start: OPEN performance.html → แท็บ **สอบทาน + ผล & Gap**
- ผ่านเมื่อ: ทุกผล published มีปุ่ม Movement เสมอ (อบรมเฉพาะเมื่อมี gap)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถวผลเผยแพร่ทั้งหมด (กนกพร, ปิยะ) | — | ทุกแถวมีปุ่ม "ส่งเรื่องปรับตำแหน่ง/เงินเดือน"; "ส่งไปอบรม" ปรากฏเฉพาะแถวที่มี gap | ☐ |

#### TC-PB05 — ส่งต่อผลจาก drawer รายละเอียด (hook ในหน้ารายละเอียด)
- group: ผล/Gap · ความสำคัญ: ต่ำ · trace: FN-06/07 / 01_UI P-02 tabDetail
- actor: HR · Setup: role=hr · seed=A5 (published) · files=—
- Start: OPEN performance.html → แท็บ **แบบประเมินรายคน** → CLICK แถว **กนกพร วงศ์ไทย (A5)** (tab รายละเอียด)
- ผ่านเมื่อ: ส่วน "ส่งต่อผล" ใน tab รายละเอียดมีปุ่ม hook ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY tab รายละเอียด (A5) | — | ช่อง "ผลการตัดสิน"=ผ่าน · "จุดที่ต้องพัฒนา"=ทักษะการนำเสนอ · section **ส่งต่อผล** + ปุ่ม "ส่งไปอบรม"/"ส่งเรื่องปรับตำแหน่ง/เงินเดือน"/"ส่งเข้า Succession Planning" | ☐ |

---

### กลุ่ม TC-RO · Re-open published (OQ-PERF-01 / BR-12)

#### TC-RO01 — เปิดแก้ไขผลหลังเผยแพร่ (happy · reason มี)
- group: Re-open · ความสำคัญ: สูง · trace: FN-09(re-open) / AC-18 / BR-12 / LD-05
- actor: HR · Setup: role=hr · seed=A5 (published, open cycle) · files=—
- Start: OPEN performance.html → CLICK แท็บ **สอบทาน + ผล & Gap**
- ผ่านเมื่อ: ปุ่ม "เปิดแก้ไขผล" → กรอกเหตุผล → toast "เปิดแก้ไขผลแล้ว · ส่งกลับขั้นหัวหน้าประเมิน · บันทึกผู้แก้ไว้ในประวัติ" + A5 → หัวหน้าประเมิน (decision เคลียร์)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถว กนกพร (A5) | — | มีปุ่ม **เปิดแก้ไขผล** | ☐ |
| 2 | CLICK ปุ่ม **เปิดแก้ไขผล** | — | modal **เปิดแก้ไขผลที่เผยแพร่แล้ว?** + subtitle "กนกพร วงศ์ไทย · คะแนน 4.00 / 5 · decision: ผ่าน" | ☐ |
| 3 | VERIFY เนื้อ modal | — | list "ส่งแบบประเมินกลับขั้น หัวหน้าประเมิน …" + "บันทึกผู้เปิดแก้ไข + เวลา + เหตุผล … ผลเดิมไม่ถูกลบ" + ช่อง "เหตุผลการเปิดแก้ไข *" | ☐ |
| 4 | TYPE "คะแนนผิด ต้องแก้" → ช่อง **เหตุผลการเปิดแก้ไข** | — | ช่องแสดงข้อความ | ☐ |
| 5 | CLICK ปุ่ม **เปิดแก้ไขผล** (ใน modal) | — | ปุ่ม "กำลังเปิดแก้ไข…" | ☐ |
| 6 | WAIT จน toast ปรากฏ | — | toast **เปิดแก้ไขผลแล้ว · ส่งกลับขั้นหัวหน้าประเมิน · บันทึกผู้แก้ไว้ในประวัติ** + modal ปิด | ☐ |
| 7 | CLICK แท็บ **แบบประเมินรายคน** → VERIFY แถว กนกพร | — | pill = **หัวหน้าประเมิน** (กลับขั้น mgr · decision เคลียร์) | ☐ |

#### TC-RO02 — เปิดแก้ไขผลโดยไม่ระบุเหตุผล (negative · VR-03)
- group: Re-open · ความสำคัญ: สูง · trace: FN-09 / VR-03 / BR_REASON_REQUIRED
- actor: HR · Setup: role=hr · seed=A5 (published) · files=—
- Start: OPEN performance.html → แท็บ **สอบทาน + ผล & Gap** → CLICK **เปิดแก้ไขผล** (แถว กนกพร)
- ผ่านเมื่อ: กด "เปิดแก้ไขผล" โดยเหตุผลว่าง → block + error "กรุณาระบุเหตุผล" (ไม่มี toast success, สถานะไม่เปลี่ยน)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **เปิดแก้ไขผล** (ใน modal, เหตุผลว่าง) | — | ช่องเหตุผลขึ้นสถานะ invalid + ข้อความ **กรุณาระบุเหตุผล** · modal ไม่ปิด | ☐ |
| 2 | VERIFY สถานะ A5 | — | ยัง "เผยแพร่ผล" (ไม่กลับขั้น mgr) | ☐ |

#### TC-RO03 — re-open ไม่ได้เมื่อรอบปิด (negative · closed guard)
- group: Re-open · ความสำคัญ: กลาง · trace: FN-09 / BR-12 (open cycle only) / FIX-05
- actor: HR · Setup: role=hr · seed=ปิด CY1 ก่อน (TC-CY04) · files=—
- Start: หลังปิด CY1 → แท็บ **สอบทาน + ผล & Gap**
- ผ่านเมื่อ: ปุ่ม "เปิดแก้ไขผล"/mutation ต่อผลที่เผยแพร่ถูกซ่อน (รอบปิด → guard layer 1)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section ผล & Gap (แถว กนกพร/ปิยะ) หลังรอบปิด | — | **ไม่มี** ปุ่ม "เปิดแก้ไขผล"/"เปิดแผน PIP"/hook (ปุ่ม mutation ถูกซ่อนเพราะรอบปิด) | ☐ |

#### TC-RO04 — re-open ผลเดิมไม่ถูกลบ (audit preserved · VERIFY)
- group: Re-open · ความสำคัญ: สูง · trace: FN-09 / BR-12 / BR-09 (append-only)
- actor: HR · Setup: role=hr · seed=A5 re-open แล้ว (TC-RO01) · files=—
- Start: หลัง TC-RO01 → แท็บ **แบบประเมินรายคน** → CLICK แถว **กนกพร** → tab **ประวัติ**
- ผ่านเมื่อ: ประวัติมีทั้งรายการ "เปิดแก้ไขผลหลังเผยแพร่ · เหตุผล: …" (บนสุด) + รายการเผยแพร่เดิม (ไม่ถูกลบ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY tab ประวัติ | — | รายการบนสุด = **เปิดแก้ไขผลหลังเผยแพร่ · เหตุผล: คะแนนผิด ต้องแก้** (who=สุนิสา คำแก้ว + เวลา) | ☐ |
| 2 | VERIFY รายการเดิม | — | รายการ "เผยแพร่ผล · decision: ผ่าน" เดิมยังอยู่ (ไม่ถูกลบ) | ☐ |

#### TC-RO05 — re-open → re-publish → CSQ ยิงซ้ำ (XT-05)
- group: Re-open · ความสำคัญ: สูง · trace: FN-09 / XT-05 / BR-13 (re-publish CSQ per-person)
- actor: HR · Setup: role=hr · seed=A5 re-open แล้ว (สถานะ mgr) · files=— · (ต้อง simulate downstream · verify ผ่าน audit/toast)
- Start: หลัง TC-RO01 → เดิน flow ใหม่: บันทึกผลหัวหน้า → ส่งสอบทาน → บันทึก 2 ขั้น → เผยแพร่ใหม่
- ผ่านเมื่อ: เผยแพร่ใหม่ได้ → toast "เผยแพร่ผล · บันทึกผลเข้า 7C · …" + ประวัติมี "บันทึกผลประเมินเข้า 7C" รอบใหม่ (ยิงซ้ำ) เพิ่มจากของเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **แบบประเมินรายคน** → แถว **กนกพร** → tab **KPI / คะแนน** | — | คะแนนหัวหน้าแก้ได้ (ขั้น mgr) · คะแนน/gap เดิมยังอยู่ | ☐ |
| 2 | TYPE คะแนนหัวหน้าครบ → CLICK **บันทึกผลหัวหน้า** | — | toast "บันทึกผลหัวหน้าแล้ว · ส่งเข้าสอบทาน (DOA)" · สถานะ → รอสอบทาน | ☐ |
| 3 | แท็บ **สอบทาน + ผล & Gap** → ส่งสอบทาน (เลือก 2 ผู้) → บันทึกขั้น 1 → เลือก decision → **บันทึกผล + เผยแพร่ผล** | — | toast **เผยแพร่ผล · บันทึกผลเข้า 7C · RESTRICTED · แจ้งเตือนพนักงานแล้ว** | ☐ |
| 4 | VERIFY tab ประวัติ กนกพร | — | มีรายการ "บันทึกผลประเมินเข้า 7C" **≥2 ครั้ง** (ยิงซ้ำ per re-publish) + ผลเดิมยังอยู่ | ☐ |

---

### กลุ่ม TC-PP · PIP

#### TC-PP01 — เปิดแผน PIP (happy · decision ทบทวน)
- group: PIP · ความสำคัญ: กลาง · trace: FN-10 / AC-11 / BR-05
- actor: HR · Setup: role=hr · seed=A6 (published, decision="ทบทวน (PIP)", gap="ความถูกต้องในงาน") · files=—
- Start: OPEN performance.html → CLICK แท็บ **สอบทาน + ผล & Gap**
- ผ่านเมื่อ: ปุ่ม "เปิดแผน PIP" (แดง) → modal → "เปิดแผน PIP" → toast "เปิดแผน PIP แล้ว"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถว ปิยะ มั่นคง (A6 · ทบทวน) | — | มีปุ่ม **เปิดแผน PIP** (แดง) | ☐ |
| 2 | CLICK ปุ่ม **เปิดแผน PIP** | — | modal **เปิดแผนพัฒนา (PIP)** + subtitle "ปิยะ มั่นคง · คะแนน 2.30 / 5 · decision: ทบทวน (PIP)" | ☐ |
| 3 | VERIFY ฟิลด์ modal | — | ช่อง "ประเด็นที่ต้องพัฒนา (Gap)" = "ความถูกต้องในงาน" · "ระยะเวลา PIP" (30/60/90 วัน) · "แนวทาง/เป้าหมาย" | ☐ |
| 4 | SELECT "60 วัน" → **ระยะเวลา PIP** | — | เลือก 60 วัน | ☐ |
| 5 | CLICK ปุ่ม **เปิดแผน PIP** (ใน modal) | — | toast **เปิดแผน PIP แล้ว** + modal ปิด | ☐ |
| 6 | CLICK แถว **ปิยะ** (แท็บแบบประเมินรายคน) → tab **ประวัติ** | — | รายการบนสุด "เปิดแผน PIP · 60 วัน" | ☐ |

#### TC-PP02 — เปิด PIP โดย gap ว่าง (negative · VR-10)
- group: PIP · ความสำคัญ: กลาง · trace: FN-10 / VR-10 / BR_GAP_REQUIRED
- actor: HR · Setup: role=hr · seed=A6 (ลบ gap ในช่องก่อนกด) · files=—
- Start: OPEN performance.html → แท็บ **สอบทาน + ผล & Gap** → CLICK **เปิดแผน PIP** (แถว ปิยะ)
- ผ่านเมื่อ: ล้างช่อง Gap ว่าง → กด "เปิดแผน PIP" → toast "กรุณาระบุประเด็นที่ต้องพัฒนา"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLEAR ช่อง **ประเด็นที่ต้องพัฒนา (Gap)** (ลบข้อความให้ว่าง) | — | ช่องว่าง | ☐ |
| 2 | CLICK ปุ่ม **เปิดแผน PIP** | — | toast **กรุณาระบุประเด็นที่ต้องพัฒนา** · modal ไม่ปิด | ☐ |

---

### กลุ่ม TC-OD · Overdue + reminder

#### TC-OD01 — banner เกินกำหนด + ส่งการเตือน (FN-09)
- group: Overdue · ความสำคัญ: กลาง · trace: FN-09 / AC-06 / EC-09
- actor: HR · Setup: role=hr · seed=A2 (self, due 2026-09-05 < TODAY 09-09 → overdue) · files=—
- Start: OPEN performance.html → CLICK แท็บ **แบบประเมินรายคน**
- ผ่านเมื่อ: banner "มี 1 แบบประเมินเกินกำหนด — ต้องเตือนผู้ประเมิน" + ปุ่ม "ส่งการเตือน" → toast "ส่งการเตือนผู้ที่ประเมินไม่ครบ/เกินกำหนดแล้ว"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ด้านบนตารางแบบประเมิน | — | banner is-warn **มี 1 แบบประเมินเกินกำหนด — ต้องเตือนผู้ประเมิน** + ปุ่ม **ส่งการเตือน** | ☐ |
| 2 | CLICK ปุ่ม **ส่งการเตือน** | — | toast **ส่งการเตือนผู้ที่ประเมินไม่ครบ/เกินกำหนดแล้ว** | ☐ |

#### TC-OD02 — badge เกินกำหนดใน drawer รายละเอียด (VERIFY)
- group: Overdue · ความสำคัญ: ต่ำ · trace: FN-09 / isOverdue
- actor: HR · Setup: role=hr · seed=A2 (overdue) · files=—
- Start: OPEN performance.html → แท็บ **แบบประเมินรายคน** → CLICK แถว **สมชาย ใจดี (A2)**
- ผ่านเมื่อ: tab รายละเอียดมี note "เกินกำหนดประเมิน (…)" + ปุ่ม "ส่งการเตือน"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY tab รายละเอียด A2 | — | note is-warn **เกินกำหนดประเมิน (…)** + ปุ่ม "ส่งการเตือน" | ☐ |

---

### กลุ่ม TC-NT · แจ้งเตือน 3 event

#### TC-NT01 — notif panel มี 3 ประเภท (FN-12)
- group: แจ้งเตือน · ความสำคัญ: กลาง · trace: FN-12 / AC-12 / ENG-NOTIFY (ไม่นับ doa_*)
- actor: HR · Setup: role=hr · seed=default · files=—
- Start: OPEN performance.html
- ผ่านเมื่อ: เปิดกระดิ่ง → เห็น 3 ประเภท: รอบเปิด / ใกล้ครบกำหนด / ผลเผยแพร่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอนกระดิ่ง (มุมขวาบน header) | — | panel เปิด หัวข้อ "การแจ้งเตือน (รอบเปิด · ครบกำหนด · ผล)" | ☐ |
| 2 | VERIFY รายการ | — | 3 รายการ: **รอบประเมินเปิดกรอกแล้ว** · **ใกล้ครบกำหนดประเมิน** · **ผลประเมินเผยแพร่แล้ว** (ไม่มี doa_pending/doa_result) | ☐ |

---

### กลุ่ม TC-RP · รายงาน distribution (FN-13)

#### TC-RP01 — stat tiles ถูกต้อง (VERIFY)
- group: รายงาน · ความสำคัญ: กลาง · trace: FN-13 / AC-13
- actor: HR · Setup: role=hr · seed=default (repCycle=CY1) · files=—
- Start: OPEN performance.html → CLICK แท็บ **รายงาน**
- ผ่านเมื่อ: 3 stat tile ค่าตรง seed CY1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY stat tiles | — | **แบบประเมินในรอบ = 6** · **เผยแพร่ผลแล้ว = 2** · **ทบทวน (PIP) = 1** | ☐ |

#### TC-RP02 — buckets การกระจายคะแนน (VERIFY)
- group: รายงาน · ความสำคัญ: กลาง · trace: FN-13 / AC-13 (buckets)
- actor: HR · Setup: role=hr · seed=default · files=—
- Start: OPEN performance.html → แท็บ **รายงาน**
- ผ่านเมื่อ: funnel 4 bucket ค่า: ต่ำ=1 (A6 2.30) · ปานกลาง=0 · ดี=1 (A5 4.00) · ดีเยี่ยม=1 (A4 4.60) [เฉพาะ appraisal ที่มีคะแนนหัวหน้า]

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY funnel "การกระจายคะแนน" | — | **ต่ำ (<3.0) = 1** · **ปานกลาง (3.0–3.9) = 0** · **ดี (4.0–4.5) = 1** · **ดีเยี่ยม (>4.5) = 1** | ☐ |

#### TC-RP03 — เปลี่ยน filter รอบ (VERIFY)
- group: รายงาน · ความสำคัญ: กลาง · trace: FN-13 / AC-13 (filter รอบ)
- actor: HR · Setup: role=hr · seed=default · files=—
- Start: OPEN performance.html → แท็บ **รายงาน**
- ผ่านเมื่อ: dropdown filter มี ทุกรอบ / CY1 / CY2 · เลือก CY2 (ไม่มี appraisal) → stat = 0

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK dropdown filter (w220, ค่าเริ่ม "รอบครึ่งปีหลัง 2569") | — | ตัวเลือก: ทุกรอบ · รอบครึ่งปีหลัง 2569 · รอบครึ่งปีแรก 2569 | ☐ |
| 2 | SELECT "รอบครึ่งปีแรก 2569" (CY2) | — | stat "แบบประเมินในรอบ" = **0** · funnel ทุก bucket = 0 | ☐ |
| 3 | SELECT "ทุกรอบ" | — | stat กลับเป็น 6 · funnel เท่าเดิม (CY2 ว่าง) | ☐ |

#### TC-RP04 — รายงานเคารพ mask ตาม role (permission · VERIFY)
- group: รายงาน · ความสำคัญ: ต่ำ · trace: FN-13 / BR-08 (aggregate เฉพาะที่ role เห็น)
- actor: พนักงาน · Setup: role=staff · seed=default · files=—
- Start: OPEN performance.html → ปุ่ม **พนักงาน** → CLICK แท็บ **รายงาน**
- ผ่านเมื่อ: staff เห็น aggregate เฉพาะ scope ของตน (นับเฉพาะ appraisal ที่ role เห็น — สมชายไม่มีผลเผยแพร่)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY stat tiles (role staff) | — | ค่านับสะท้อนเฉพาะ scope ของ staff (ไม่รั่วคะแนน/จำนวนของผู้อื่นเกิน scope) | ☐ |

---

### กลุ่ม TC-SR · ค้นหา/filter/empty (FN-90)

#### TC-SR01 — ค้นหาเจอ
- group: ค้นหา · ความสำคัญ: กลาง · trace: FN-90 / AC-14
- actor: HR · Setup: role=hr · seed=default · files=—
- Start: OPEN performance.html → CLICK แท็บ **แบบประเมินรายคน**
- ผ่านเมื่อ: พิมพ์ชื่อ → ตารางกรองเหลือแถวที่ตรง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ธนากร" → ช่องค้นหา | — | ตารางเหลือแถว "ธนากร พูนผล" | ☐ |
| 2 | VERIFY | — | แถวอื่นหายไป | ☐ |

#### TC-SR02 — ค้นหาไม่พบ → empty state
- group: ค้นหา · ความสำคัญ: กลาง · trace: FN-90 / AC-14 (empty)
- actor: HR · Setup: role=hr · seed=default · files=—
- Start: OPEN performance.html → แท็บ **แบบประเมินรายคน**
- ผ่านเมื่อ: พิมพ์คำที่ไม่มี → empty "ไม่พบแบบประเมินที่ค้นหา" + "ลองปรับคำค้นหรือล้างตัวกรอง" + ปุ่ม "ล้างตัวกรอง"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "zzzzz" → ช่องค้นหา | — | empty state: **ไม่พบแบบประเมินที่ค้นหา** + **ลองปรับคำค้นหรือล้างตัวกรอง** + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 2 | CLICK ปุ่ม **ล้างตัวกรอง** | — | ตารางกลับมาครบทุกแถว | ☐ |

#### TC-SR03 — filter สถานะ
- group: ค้นหา · ความสำคัญ: กลาง · trace: FN-90 / AC-14 (filter)
- actor: HR · Setup: role=hr · seed=default · files=—
- Start: OPEN performance.html → แท็บ **แบบประเมินรายคน**
- ผ่านเมื่อ: filter "เผยแพร่ผล" → เหลือ 2 แถว (A5, A6)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "เผยแพร่ผล" → dropdown สถานะ | — | ตารางเหลือ 2 แถว (กนกพร, ปิยะ) pill "เผยแพร่ผล" | ☐ |
| 2 | SELECT "ตั้งเป้า" → dropdown สถานะ | — | เหลือ 1 แถว (มะลิ ดอกไม้) | ☐ |

#### TC-SR04 — filter ทุกค่า (enum sweep · VERIFY)
- group: ค้นหา · ความสำคัญ: ต่ำ · trace: FN-90 (derivation: filter enum ครบทุกค่า)
- actor: HR · Setup: role=hr · seed=default · files=—
- Start: OPEN performance.html → แท็บ **แบบประเมินรายคน**
- ผ่านเมื่อ: dropdown มี 6 ค่า ตรง seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK dropdown สถานะ | — | 6 ตัวเลือก: ทุกสถานะ / ตั้งเป้า / ประเมินตนเอง / หัวหน้าประเมิน / รอสอบทาน / เผยแพร่ผล | ☐ |
| 2 | SELECT "ประเมินตนเอง" | — | เหลือ A2 (สมชาย) · SELECT "หัวหน้าประเมิน" → A3 · SELECT "รอสอบทาน" → A4 | ☐ |

---

### กลุ่ม TC-SC · RESTRICTED scope/mask (FN-94 · AC-17)

#### TC-SC01 — พนักงานเห็นเฉพาะแบบประเมินของตน (SELF · row-scope)
- group: Scope · ความสำคัญ: สูง · trace: FN-94 / AC-17 / BR-11 / EC-04 / FIX-04
- actor: พนักงาน (สมชาย ใจดี) · Setup: role=staff · seed=default · files=—
- Start: OPEN performance.html → CLICK ปุ่ม **พนักงาน** → CLICK แท็บ **แบบประเมินรายคน**
- ผ่านเมื่อ: ตารางมีเฉพาะแถวของสมชาย (A2) · คนอื่นไม่อยู่ในตาราง (ไม่ใช่แค่ mask — ไม่อยู่ DOM)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตาราง (role staff) | — | มีแถวเดียว "สมชาย ใจดี" · ไม่มี มะลิ/อรทัย/ธนากร/กนกพร/ปิยะ | ☐ |
| 2 | VERIFY badge แท็บ | — | (badge อาจนับรวมทั้งระบบ แต่ตารางที่แสดง = 1 แถวของตน) | ☐ |

#### TC-SC02 — พนักงานไม่เห็นคิวสอบทาน/ผลผู้อื่น (queue+published ซ่อน)
- group: Scope · ความสำคัญ: สูง · trace: FN-94 / EC-04 / FIX-04
- actor: พนักงาน · Setup: role=staff · seed=default · files=—
- Start: OPEN performance.html → ปุ่ม **พนักงาน** → CLICK แท็บ **สอบทาน + ผล & Gap**
- ผ่านเมื่อ: ไม่มี team-calibration + ไม่มีคิวสอบทาน + ผลเผยแพร่ = เฉพาะของตน (สมชายไม่มี → "ยังไม่มีผลที่เผยแพร่")

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หน้า review (role staff) | — | **ไม่มี** section "Calibration ระดับทีม" · **ไม่มี** section "รอสอบทาน (calibration · DOA)" | ☐ |
| 2 | VERIFY section ผล & Gap | — | "ยังไม่มีผลที่เผยแพร่" (สมชายไม่มีผล published · ผู้อื่นไม่อยู่ DOM) | ☐ |

#### TC-SC03 — หัวหน้าเห็นเฉพาะแผนกตน (DEPT · snapshot)
- group: Scope · ความสำคัญ: สูง · trace: FN-94 / AC-17 / BR-11 / EC-10 / OQ-PERF-03
- actor: หัวหน้าสายงาน (ประสงค์ · dept=ฝ่ายผลิต) · Setup: role=mgr · seed=default · files=—
- Start: OPEN performance.html → CLICK ปุ่ม **หัวหน้าสายงาน** → CLICK แท็บ **แบบประเมินรายคน**
- ผ่านเมื่อ: ตารางมีเฉพาะ appraisal แผนกฝ่ายผลิต (A2 สมชาย) · แผนกอื่นไม่อยู่ DOM

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตาราง (role mgr) | — | มีเฉพาะแถวแผนก **ฝ่ายผลิต** (สมชาย ใจดี · A2) · ไม่มี อรทัย(บัญชี)/ธนากร(ขาย)/กนกพร(การตลาด)/มะลิ,ปิยะ(คลัง) | ☐ |

#### TC-SC04 — หัวหน้าไม่มีปุ่ม mutation ของ staff (permission)
- group: Scope · ความสำคัญ: กลาง · trace: FN-94 / §5.3 (mgr = view/mgr-stage only)
- actor: หัวหน้าสายงาน · Setup: role=mgr · seed=default · files=—
- Start: OPEN performance.html → ปุ่ม **หัวหน้าสายงาน** → แท็บ **แบบประเมินรายคน** → CLICK แถว **สมชาย ใจดี (A2)**
- ผ่านเมื่อ: A2 อยู่ขั้น self → ไม่มีปุ่มบันทึกหัวหน้า (ยังไม่ถึงขั้น mgr) · ไม่มีปุ่มสร้าง/ปิดรอบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY drawer A2 (role mgr) tab KPI | — | ยังขั้น "ประเมินตนเอง" → ไม่มีช่องกรอกคะแนนหัวหน้า/ปุ่ม "บันทึกผลหัวหน้า" (ต้องรอ staff บันทึก self ก่อน · BR-03) | ☐ |

#### TC-SC05 — HR เห็นทั้งหมด (ALL · baseline)
- group: Scope · ความสำคัญ: กลาง · trace: FN-94 / BR-11 (HR=ALL)
- actor: HR · Setup: role=hr · seed=default · files=—
- Start: OPEN performance.html → CLICK แท็บ **แบบประเมินรายคน**
- ผ่านเมื่อ: ตารางมีครบ 6 แถวทุกแผนก + คะแนนไม่ mask

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตาราง (role HR) | — | 6 แถว (มะลิ/สมชาย/อรทัย/ธนากร/กนกพร/ปิยะ) ครบทุกแผนก | ☐ |
| 2 | CLICK แถว **ธนากร (A4)** → tab รายละเอียด | — | "คะแนนรวม (หัวหน้า)" = **4.60 / 5** (ตัวเลขจริง ไม่ใช่ ••• เพราะ HR ไม่ mask) | ☐ |

#### TC-SC06 — พนักงานเปิดแบบประเมินของผู้อื่น → RESTRICTED note (staff)
- group: Scope · ความสำคัญ: สูง · trace: FN-94 / AC-17 / EC-03/04
- actor: พนักงาน · Setup: role=staff · seed=default · files=— · (ปกติผู้อื่นไม่อยู่ตาราง — เคสนี้ยืนยัน guard ระดับเปิด detail)
- Start: OPEN performance.html → ปุ่ม **พนักงาน** → แท็บ **แบบประเมินรายคน**
- ผ่านเมื่อ: ถ้าเข้าถึง detail ของผู้อื่นได้ → note "ข้อมูลนี้เป็นความลับ (RESTRICTED) — ดูได้เฉพาะแบบประเมินของตนเอง"; ปกติแถวผู้อื่นไม่อยู่ DOM อยู่แล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตาราง staff | — | ผู้อื่นไม่อยู่ตาราง (defense-in-depth: guard ระดับเปิด detail จะโชว์ note RESTRICTED "…ดูได้เฉพาะแบบประเมินของตนเอง") | ☐ |
| 2 | (ถ้า simulate เปิด id ผู้อื่น) VERIFY | — | note is-warn **ข้อมูลนี้เป็นความลับ (RESTRICTED) — ดูได้เฉพาะแบบประเมินของตนเอง** · ไม่มีคะแนน/decision/gap ใน DOM | ☐ |

#### TC-SC07 — หัวหน้าเปิดแบบประเมินนอกแผนก → RESTRICTED note (mgr)
- group: Scope · ความสำคัญ: กลาง · trace: FN-94 / AC-17 / OQ-PERF-03
- actor: หัวหน้าสายงาน · Setup: role=mgr · seed=default · files=— · (ต้อง simulate เปิด id นอกแผนก)
- Start: OPEN performance.html → ปุ่ม **หัวหน้าสายงาน** → แท็บ **แบบประเมินรายคน**
- ผ่านเมื่อ: เปิด appraisal นอกแผนกตน → note "ข้อมูลนี้เป็นความลับ (RESTRICTED) — หัวหน้าดูได้เฉพาะแผนกของตน"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตาราง mgr | — | เห็นเฉพาะแผนกฝ่ายผลิต (ผู้อื่นไม่อยู่ตาราง) | ☐ |
| 2 | (ถ้า simulate เปิด id นอกแผนก เช่น A4 ฝ่ายขาย) VERIFY | — | note is-warn **ข้อมูลนี้เป็นความลับ (RESTRICTED) — หัวหน้าดูได้เฉพาะแผนกของตน** | ☐ |

---

### กลุ่ม TC-AU · audit append-only (FN-93)

#### TC-AU01 — ทุก mutation เพิ่ม audit newest-first (VERIFY)
- group: Audit · ความสำคัญ: สูง · trace: FN-93 / AC-16 / BR-09
- actor: HR · Setup: role=hr · seed=A1 (goal) · files=—
- Start: OPEN performance.html → แท็บ **แบบประเมินรายคน** → แถว **A1** → tab **KPI / คะแนน** → บันทึกเป้า/KPI
- ผ่านเมื่อ: หลังบันทึก → tab ประวัติมีรายการ "ตั้งเป้า/KPI" ใหม่บนสุด (ของเดิมไม่ถูกแก้)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **บันทึกเป้า/KPI** (A1, Σ=100) | — | toast success | ☐ |
| 2 | CLICK แถว **A1** → tab **ประวัติ** | — | รายการบนสุด = **ตั้งเป้า/KPI** (who=สุนิสา คำแก้ว + เวลา วันนี้) | ☐ |

#### TC-AU02 — audit ประวัติ published แสดงครบ (VERIFY)
- group: Audit · ความสำคัญ: กลาง · trace: FN-93 / BR-09 (immutable trail)
- actor: HR · Setup: role=hr · seed=A5 (published, audit seed 3 รายการ) · files=—
- Start: OPEN performance.html → แท็บ **แบบประเมินรายคน** → แถว **กนกพร (A5)** → tab **ประวัติ**
- ผ่านเมื่อ: ประวัติแสดง ≥3 รายการ newest-first (เผยแพร่ผล / สอบทานผล / หัวหน้าประเมิน) พร้อม who+at

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY tab ประวัติ A5 | — | รายการ: "เผยแพร่ผล · decision: ผ่าน" (บนสุด) · "สอบทานผล (DOA)" · "หัวหน้าประเมิน + คะแนน" — แต่ละรายการมีชื่อผู้ทำ + เวลา | ☐ |

---

### กลุ่ม TC-GD · guard cascade + double-submit (FN-18 · FN-92)

#### TC-GD01 — กันสอบทานข้ามขั้น/คะแนนไม่ครบ (P2 · EC-01 · VR-07)
- group: Guard · ความสำคัญ: สูง · trace: FN-18 / AC-19(P2) / EC-01 / BR_MGR_SCORE_INCOMPLETE
- actor: HR · Setup: role=hr · seed=A1(goal)/A3(mgr, ยังไม่มี mgr score) · files=— · (UI: ปุ่มสอบทานไม่ render กับ record ที่ยังไม่ถึง calibration)
- Start: OPEN performance.html → แท็บ **สอบทาน + ผล & Gap**
- ผ่านเมื่อ: คิวสอบทานมีเฉพาะ record ที่ calibration + คะแนนหัวหน้าครบ (A4) · A1/A3 ไม่โผล่ให้กดสอบทาน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section "รอสอบทาน" | — | มีเฉพาะ "ธนากร พูนผล" (A4 · calibration + weighted 4.60) · **ไม่มี** มะลิ(goal)/อรทัย(mgr ไม่มีคะแนน) | ☐ |
| 2 | (simulate: เรียก doCalibSend กับ A3/goal ตรง ๆ) VERIFY | — | ถูกบล็อก toast "สอบทานได้เฉพาะแบบประเมินที่ให้คะแนนหัวหน้าครบและรอสอบทาน" (ต้อง simulate) | ☐ |

#### TC-GD02 — กัน transition ย้อนหลัง (P2 · EC-02 · FIX-02)
- group: Guard · ความสำคัญ: สูง · trace: FN-18 / AC-19(P2) / EC-02 / ERR_STAGE_INVALID
- actor: HR · Setup: role=hr · seed=A4(calibration)/A5(published) · files=—
- Start: OPEN performance.html → แท็บ **แบบประเมินรายคน** → แถว **A5 (published)** → tab **KPI / คะแนน**
- ผ่านเมื่อ: record published/calibration ไม่มี KPI editor/self input/mgr input (แก้ย้อนขั้นไม่ได้ผ่าน UI)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY tab KPI ของ A5 (published) | — | อ่านอย่างเดียว · ไม่มีช่องแก้ KPI/คะแนนตนเอง/หัวหน้า · ไม่มีปุ่มบันทึกขั้นก่อนหน้า | ☐ |
| 2 | (simulate: เรียก saveKpi/saveSelf/saveMgr กับ published) VERIFY | — | toast "…ได้เฉพาะขั้น…" (ERR_STAGE_INVALID · ต้อง simulate) | ☐ |

#### TC-GD03 — staff เดินผลแทนหัวหน้า/สอบทานเอง ถูกกัน (P3 · EC-03 · FIX-03)
- group: Guard · ความสำคัญ: สูง · trace: FN-18 / AC-19(P3) / EC-03 / ERR_INSUFFICIENT_ROLE
- actor: พนักงาน · Setup: role=staff · seed=default · files=—
- Start: OPEN performance.html → ปุ่ม **พนักงาน** → เดินดูทุกแท็บ
- ผ่านเมื่อ: staff ไม่เห็นปุ่ม mutation ใด ๆ (สร้างรอบ/ปิดรอบ/สอบทาน/PIP/reopen/send*) · เห็นเฉพาะ self ของตน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แท็บ "รอบประเมิน" (staff) | — | ไม่มีปุ่ม "สร้างรอบประเมิน"; เปิด drawer รอบไม่มีปุ่ม "ปิดรอบ" | ☐ |
| 2 | VERIFY แท็บ "สอบทาน + ผล & Gap" (staff) | — | ไม่มี team-calibration/คิวสอบทาน/ปุ่ม "สอบทาน (DOA)"/"เปิดแผน PIP"/"เปิดแก้ไขผล"/hook | ☐ |
| 3 | (simulate: staff เรียก saveMgr/doCalib) VERIFY | — | toast **สิทธิ์ไม่พอ** (ต้อง simulate call) | ☐ |

#### TC-GD04 — ปิดรอบแล้ว mutation ทุกตัวถูกกัน (P4 · EC-07 · FIX-05)
- group: Guard · ความสำคัญ: สูง · trace: FN-18 / AC-19(P4) / EC-07 / BR_CYCLE_CLOSED
- actor: HR · Setup: role=hr · seed=ปิด CY1 ก่อน (TC-CY04) · files=—
- Start: หลังปิด CY1 → เดินทุกแท็บ
- ผ่านเมื่อ: ทุกปุ่ม mutation ต่อแบบประเมินในรอบถูกซ่อน + banner read-only เมื่อเปิด KPI

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **แบบประเมินรายคน** | — | banner "รอบนี้ปิดแล้ว — ดูได้อย่างเดียว แก้ไขไม่ได้" เมื่อเปิด KPI (ทดสอบใน TC-CY05) | ☐ |
| 2 | CLICK แท็บ **สอบทาน + ผล & Gap** | — | คิวสอบทานแสดง "รอบปิดแล้ว" แทนปุ่มสอบทาน · ผลเผยแพร่ไม่มีปุ่ม PIP/reopen/hook | ☐ |
| 3 | (simulate: เรียก mutation ใด ๆ) VERIFY | — | toast **รอบนี้ปิดแล้ว — แก้ไขไม่ได้** (ต้อง simulate) | ☐ |

#### TC-GD05 — กัน double-submit (FN-92 · VR-06)
- group: Guard · ความสำคัญ: สูง · trace: FN-92 / AC-15 / VR-06 (`_busy`/idempotency)
- actor: HR · Setup: role=hr · seed=A1 (goal, Σ=100) · files=—
- Start: OPEN performance.html → แท็บ **แบบประเมินรายคน** → แถว **A1** → tab **KPI / คะแนน**
- ผ่านเมื่อ: ดับเบิลคลิก "บันทึกเป้า/KPI" → ปุ่ม disable + spinner ทันที คลิกซ้ำไม่ทำงาน + ประวัติได้ entry เดียว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **บันทึกเป้า/KPI** 2 ครั้งเร็ว ๆ | — | ปุ่มเปลี่ยนเป็น "กำลังบันทึก…" + disable หลังคลิกแรก · คลิกที่ 2 ไม่มีผล | ☐ |
| 2 | WAIT → CLICK แถว **A1** → tab **ประวัติ** | — | มีรายการ "ตั้งเป้า/KPI" **entry เดียว** (ไม่ซ้ำ) | ☐ |

#### TC-GD06 — concurrent staged review (EC-05 · `[AI-DEFAULT]`)
- group: Guard · ความสำคัญ: กลาง · trace: EC-05 / OQ-PERF-09 / ERR_STALE_DATA `[AI-DEFAULT]`
- actor: HR (2 session) · Setup: role=hr · seed=A4 ส่งสอบทานแล้ว (2 ขั้น) · files=— · **(ต้อง simulate 2 ผู้บันทึกพร้อมกัน)**
- Start: 2 session เปิด modal DOA ของ A4 ขั้นเดียวกัน
- ผ่านเมื่อ: first-write-wins · second ได้ 409 ERR_STALE_DATA (`[AI-DEFAULT]` optimistic lock — เกณฑ์ AI ตัดสินแทน BA)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) บันทึกผลสอบทานขั้นเดียวกันจาก 2 session พร้อมกัน | — | session แรกสำเร็จ · session ที่สอง error concurrency (ERR_STALE_DATA) — mark BLOCKED ถ้า simulate ไม่ได้ | ☐ |

---

### กลุ่ม TC-XT · Cross-module dispatch (06_TESTS §6.9)

#### TC-XT01 — Movement event (XT-01)
- group: XT · ความสำคัญ: กลาง · trace: XT-01 / FN-07 / BR-07 · **(prototype ไม่มีหน้า Movement → verify ผ่าน toast/no-CRUD)**
- actor: HR · Setup: role=hr · seed=A5 (published) · files=— · (ต้อง simulate การ capture event ปลายทาง)
- Start: OPEN performance.html → แท็บ **สอบทาน + ผล & Gap**
- ผ่านเมื่อ: กด Movement → toast "ส่งเรื่องปรับเงินเดือน/เลื่อนตำแหน่งให้ระบบโยกย้าย (ไม่ปรับเอง)" + ไม่ CRUD บนจอ (payload {appraisal_id, employee_ref, decision, weighted_score} = simulate)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งเรื่องปรับตำแหน่ง/เงินเดือน** (แถว กนกพร) | — | toast **ส่งเรื่องปรับเงินเดือน/เลื่อนตำแหน่งให้ระบบโยกย้าย (ไม่ปรับเอง)** | ☐ |
| 2 | VERIFY | — | ไม่มีการเปลี่ยนเงินเดือน/ตำแหน่งบนจอ (event เท่านั้น) | ☐ |

#### TC-XT02 — Training hook (XT-02)
- group: XT · ความสำคัญ: กลาง · trace: XT-02 / FN-06 / BR-06
- actor: HR · Setup: role=hr · seed=A5 (gap="ทักษะการนำเสนอ") · files=—
- Start: OPEN performance.html → แท็บ **สอบทาน + ผล & Gap**
- ผ่านเมื่อ: กด "ส่งไปอบรม" → toast มีชื่อ gap + "ไม่สร้างหลักสูตรในหน้านี้"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งไปอบรม** (แถว กนกพร) | — | toast **ส่งจุดที่ต้องพัฒนา "ทักษะการนำเสนอ" ไปหลักสูตรอบรม (ส่งต่อ ไม่แก้ที่นี่) — ไม่สร้างหลักสูตรในหน้านี้** | ☐ |

#### TC-XT03 — Succession candidate (XT-03)
- group: XT · ความสำคัญ: กลาง · trace: XT-03 / FN-07 / FIX-09
- actor: HR · Setup: role=hr · seed=A5 (ผ่าน/top) · files=—
- Start: OPEN performance.html → แท็บ **สอบทาน + ผล & Gap**
- ผ่านเมื่อ: กด "ส่งเข้า Succession Planning" (เฉพาะ top/ผ่าน) → toast "ส่งผลเข้า Succession Planning (ส่งต่อ ไม่แก้ที่นี่)"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งเข้า Succession Planning** (แถว กนกพร) | — | toast **ส่งผลเข้า Succession Planning (ส่งต่อ ไม่แก้ที่นี่)** | ☐ |

#### TC-XT04 — CSQ 7C per-person publish (XT-04)
- group: XT · ความสำคัญ: กลาง · trace: XT-04 / BR-13 / LD-03 · **(CSQ payload = simulate; verify ผ่าน audit)**
- actor: HR · Setup: role=hr · seed=A4 สอบทานถึงเผยแพร่ (TC-CB01→CB04) · files=—
- Start: หลังเผยแพร่ A4 → แท็บ **แบบประเมินรายคน** → แถว **ธนากร** → tab **ประวัติ**
- ผ่านเมื่อ: ประวัติมี "บันทึกผลประเมินเข้า 7C" ทันทีหลัง "เผยแพร่ผล" (ยิง per-person)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY tab ประวัติ ธนากร | — | มีรายการ "เผยแพร่ผล · decision: ผ่าน" + "บันทึกผลประเมินเข้า 7C" (CSQ hook per-person publish) | ☐ |

#### TC-XT05 — re-open → re-publish → movement/CSQ ซ้ำ (XT-05)
- group: XT · ความสำคัญ: กลาง · trace: XT-05 / BR-12/13 · (ครอบโดย TC-RO05)
- actor: HR · Setup: role=hr · seed=A5 re-open+re-publish (TC-RO05) · files=—
- Start: อ้างผล TC-RO05
- ผ่านเมื่อ: re-publish → "บันทึกผลประเมินเข้า 7C" ยิงซ้ำ + ผลเดิมไม่ลบ + สามารถส่ง Movement ใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หลัง re-publish (อ้าง TC-RO05) | — | ประวัติมี "บันทึกผลประเมินเข้า 7C" ≥2 · ปุ่ม "ส่งเรื่องปรับตำแหน่ง/เงินเดือน" ใช้ได้อีก (ส่ง event ใหม่) | ☐ |

---

### กลุ่ม TC-LK · Scope Lock verify (07_LOCKED §7.0)

#### TC-LK01 — LK-1 DOA เลือกคนจริงต่อขั้น ไม่ preset
- group: LOCK · ความสำคัญ: สูง · trace: LK-1 / FN-08 / EC-08
- actor: HR · Setup: role=hr · seed=A4 (calibration) · files=—
- Start: OPEN performance.html → แท็บ **สอบทาน + ผล & Gap** → CLICK **สอบทาน (DOA)** (แถว ธนากร)
- ผ่านเมื่อ: 2 slot ว่าง (ไม่มีชื่อ preset) + ต้องเลือกคนจริงจากรายชื่อ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY slot ทั้งสอง | — | ว่างทั้งคู่ (placeholder "เลือกผู้สอบทาน…") · ไม่มีชื่อ preset ล่วงหน้า | ☐ |

#### TC-LK02 — LK-2 Movement = event ไม่ CRUD
- group: LOCK · ความสำคัญ: สูง · trace: LK-2 / BR-07
- actor: HR · Setup: role=hr · seed=A5 (published) · files=—
- Start: OPEN performance.html → แท็บ **สอบทาน + ผล & Gap**
- ผ่านเมื่อ: กด Movement → toast event · ไม่มีฟอร์มแก้เงินเดือน/ตำแหน่งในฟีเจอร์นี้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ทั้งฟีเจอร์ | — | ไม่มีหน้า/ฟอร์มแก้เงินเดือนหรือตำแหน่ง (ผลส่งเป็น event ไป Movement เท่านั้น) | ☐ |

#### TC-LK03 — LK-3 รอบ/แบบจาก HR Config (ไม่สร้างเอง)
- group: LOCK · ความสำคัญ: สูง · trace: LK-3 / BR-01
- actor: HR · Setup: role=hr · seed=default · files=—
- Start: OPEN performance.html → CLICK **สร้างรอบประเมิน**
- ผ่านเมื่อ: drawer อ่านรอบจาก ตั้งค่า HR + note ยืนยันไม่สร้าง/แก้ฟอร์มกลาง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY drawer สร้างรอบ | — | note **รอบ/แบบฟอร์ม/เกณฑ์คะแนน อ่านจาก ตั้งค่า HR — หน้านี้ไม่สร้าง/แก้ฟอร์มกลาง** · ช่องเลือกจาก config (ไม่มีฟอร์มสร้างแบบประเมินใหม่เอง) | ☐ |

#### TC-LK04 — LK-4 ผล RESTRICTED + mask + append-only
- group: LOCK · ความสำคัญ: สูง · trace: LK-4 / BR-08/09
- actor: พนักงาน + HR · Setup: role=staff→hr · seed=default · files=—
- Start: OPEN performance.html
- ผ่านเมื่อ: role ที่ mask เห็นคะแนนเป็น ••• (ถ้าอยู่ในบริบทที่ mask) · HR เห็นเลขจริง · ประวัติ append-only (TC-AU)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (staff บริบทที่มีคะแนนผู้อื่น) | — | คะแนนของผู้อื่น = ••• หรือไม่อยู่ DOM (RESTRICTED) | ☐ |
| 2 | VERIFY (HR) คะแนน A4 | — | แสดงเลขจริง 4.60 (ไม่ mask) | ☐ |

#### TC-LK05 — LK-5 gap → Training = hook ไม่สร้างหลักสูตร
- group: LOCK · ความสำคัญ: สูง · trace: LK-5 / BR-06
- actor: HR · Setup: role=hr · seed=A5 (gap) · files=—
- Start: OPEN performance.html → แท็บ **สอบทาน + ผล & Gap** → CLICK **ส่งไปอบรม**
- ผ่านเมื่อ: toast มีวลี "ไม่สร้างหลักสูตรในหน้านี้"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งไปอบรม** (แถว กนกพร) | — | toast มีวลี **— ไม่สร้างหลักสูตรในหน้านี้** | ☐ |

#### TC-LK06 — LK-6 CSQ ประกาศ SecC+DC เท่านั้น
- group: LOCK · ความสำคัญ: กลาง · trace: LK-6 / BR-13 / LD-03 · **(payload = simulate; verify surface)**
- actor: HR · Setup: role=hr · seed=A4 เผยแพร่แล้ว · files=—
- Start: หลังเผยแพร่ A4 → tab ประวัติ ธนากร
- ผ่านเมื่อ: audit CSQ = "บันทึกผลประเมินเข้า 7C" · ไม่มีการประกาศ OC/DC-doc/SC บนจอ (payload SecC/DC only = simulate)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ประวัติ | — | มีเฉพาะ "บันทึกผลประเมินเข้า 7C" (ไม่มี hook OC/DC-doc/SC โผล่บนจอ) | ☐ |

---

### กลุ่ม TC-TM · team-calibration view (LD-07 KEPT)

#### TC-TM01 — มุม Calibration ระดับทีม แสดงคะแนน/เกรด (VERIFY)
- group: Team calib · ความสำคัญ: ต่ำ · trace: LD-07 / OQ-PERF-04 KEPT / 01_UI P-03 section 1
- actor: HR · Setup: role=hr · seed=default (มี appraisal ที่มีคะแนน) · files=—
- Start: OPEN performance.html → CLICK แท็บ **สอบทาน + ผล & Gap**
- ผ่านเมื่อ: section "Calibration ระดับทีม" แสดงตารางคะแนน + เกรด + distribution (mock)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section แรกของหน้า review | — | ตารางเทียบคะแนน/เกรดทั้งทีม + แถบ "การกระจายเกรด (distribution) · … A n · B n · C n · D n" | ☐ |
| 2 | VERIFY dropdown เกรดต่อแถว | — | แต่ละแถวมี select เกรด A/B/C/D (mock adjust · ยังไม่ผูกปลายทาง) | ☐ |

#### TC-TM02 — team-calibration ซ่อนจากพนักงาน (permission)
- group: Team calib · ความสำคัญ: ต่ำ · trace: LD-07 / FIX-04 (ผู้สอบทานเท่านั้น)
- actor: พนักงาน · Setup: role=staff · seed=default · files=—
- Start: OPEN performance.html → ปุ่ม **พนักงาน** → CLICK แท็บ **สอบทาน + ผล & Gap**
- ผ่านเมื่อ: staff ไม่เห็น section Calibration ระดับทีม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หน้า review (staff) | — | **ไม่มี** section "Calibration ระดับทีม" (แสดงเฉพาะผู้สอบทาน/manage) | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิดไฟล์ `performance.html` ในเบราว์เซอร์ (โหลดสด = รีเซ็ต state: role=HR · แท็บ "รอบประเมิน" · ตัวกรอง=ทุกสถานะ · repCycle=CY1). โปรโตไทป์ไม่มี persistence — **เริ่มแต่ละเคสด้วยการโหลดหน้าใหม่** เว้นเคสที่ระบุ Setup ว่าอิงผลเคสก่อน (TC-CY05/CB03/CB04/CB06/RO04/RO05/XT04 — ทำต่อเนื่องในเซสชันเดียว).
2. **สลับบทบาท** = คลิกปุ่มใน demo strip ("HR (HRBP)" / "หัวหน้าสายงาน" / "พนักงาน") ยืนยันด้วยชื่อผู้ใช้มุมขวาบน.
3. **สลับหน้า** = คลิกแท็บ ("รอบประเมิน" / "แบบประเมินรายคน" / "สอบทาน + ผล & Gap" / "รายงาน").
4. ทำตามคอลัมน์ Action (verb tag) ทีละ step, ตรวจ Expected ด้วยตา, ติ๊ก `Result`.
5. เคสที่ mark **(ต้อง simulate)** = ต้อง inject การเรียก function/สภาพที่กดมือไม่ได้ (concurrent, direct API call). ถ้า runner ทำไม่ได้ → mark `blocked` พร้อม note.
6. toast เป็น transient — ใช้ `WAIT` ก่อนอ่าน (≤3s). ปุ่ม submit เปลี่ยนเป็นสถานะ "กำลัง…" ชั่วครู่ก่อน toast.
7. กรอกผลกลับตาม Result Report schema ด้านล่าง.

---

## Coverage Audit

| หมวด | covered / total |
|---|---|
| FN (FUNCTION_CHECKLIST) | **18 / 18** |
| AC (06_TESTS §6.1) | 19 / 19 |
| Business rules (BR-01..13) | 13 / 13 |
| Field validation (VR-01..10) | 10 / 10 |
| Edge cases (EC-01..10) | 8 ครอบ UI + 2 ข้าม (EC-06 API-only, EC-05 simulate) |
| Error codes (catalog) | 12 ครอบ (UI-observable) + 3 ข้าม (config upstream/stale = API-level) |
| Permission cells (§5.3) | ครบทุก role × action สำคัญ (create/close/kpi/self/mgr/calib/pip/reopen/send*/view) |
| Cross-Module (XT-01..05) | 5 / 5 (downstream = toast/audit + simulate) |
| Scope Lock (LK-1..6) | 6 / 6 |
| States/events/views | ครบ (empty×3 · closed banner · overdue · notif · team-calib · weight tag) |

**FN cross-check: ✅ 18/18** — FN-01(CY01) FN-02(KP01) FN-03(SF01) FN-04(MG01) FN-05(CB04) FN-06(PB01) FN-07(PB02) FN-08(CB01) FN-09/re-open→ดู AC map(RO01)+FN-09 overdue(OD01) FN-10(PP01) FN-11(CY04) FN-12(NT01) FN-13(RP01) FN-90(SR01) FN-91(CY04) FN-92(GD05) FN-93(AU01) FN-94(SC01) FN-18 guard(GD01-04).
> หมายเหตุ trace: 06_TESTS §6.8 map FN-09=re-open(AC-18) และ overdue อยู่ที่ FN-13/AC-06; testcase คลุมทั้งสอง (RO01-05 re-open + OD01-02 overdue).

**Manifest cross-check (FRD §0.12): ✅ 18/18** — ทุกแถว Coverage Manifest (FN-01..13, 90..94, OQ-PERF-01 re-open, §10.1 guard cascade) มีคู่ใน Ledger + เคส.

### ข้าม (พร้อมเหตุผล)
- **EC-06 / BR_CONFIG_CYCLE_NOT_FOUND / ERR_CONFIG_UPSTREAM_DOWN** — upstream HR Config #107 เป็น soft-ref, ไม่มี hook เข้าใน prototype (Test=TC-CFG-01 API-level). `[AI-DEFAULT]` error-state.
- **EC-05 / ERR_STALE_DATA** — concurrent staged review ต้องมี 2 session พร้อมกัน → TC-GD06 mark `(ต้อง simulate)`. `[AI-DEFAULT]` optimistic 409.
- **XT downstream write** (Movement/Training/Succession/CSQ payload) — prototype ไม่มีหน้าโมดูลปลายทาง → verify ผ่าน toast + audit ฝั่งต้นทาง; capture event จริง = simulate.
- **นอกขอบเขตใบเซ็น (Exclusions §0.3):** ปรับเงินเดือน/ตำแหน่งเอง · สร้าง/แก้ฟอร์มกลาง · สร้างหลักสูตร · 360/competency/check-in — **ไม่สร้างเคส** (LK-2/3/5 · OQ-PERF-08); แทนที่ด้วยเคส verify ว่า "ไม่มีความสามารถนี้บนจอ" (TC-LK02/03/05).
- **[AI-DEFAULT] flag:** เคส TC-GD06 (EC-05) + note EC-10 (TC-SC03) มาจาก rule ที่ AI ตัดสินแทน BA — ผล fail อาจแปลว่า "default ผิด" ไม่ใช่ "โค้ดผิด".

---

## Result Report (schema)

```json
{
  "feature_id": "F131",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-CY01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 77, "pass": 0, "fail": 0, "blocked": 0 }
}
```
> `evidence` = สิ่งที่ agent **เห็นจริง** ตอน fail/blocked (ข้อความ toast จริง, route/แท็บที่ค้าง, สิ่งที่แสดงแทน Expected). `note` = หมายเหตุ (เช่น "simulate ไม่ได้ → blocked").
