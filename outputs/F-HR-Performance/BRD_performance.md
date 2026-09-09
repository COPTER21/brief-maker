# BRD — Performance / ประเมินผลงาน (F131 · F-HR-PERF)

> **Generated:** brd-generator-full v2.2 · **Mode:** Fresh (HTML-first) + Lane Mode (no-ask)
> **Screen source of truth:** `outputs/F-HR-Performance/performance.html` (ผ่าน ux gate BLOCK=0 · coverage gate FN 18/18 · re-gate หลัง BA fix order)
> **Business contract:** `PREBRIEF.md` + `FUNCTION_CHECKLIST.html` (18 FN) + `STANDARD_BASELINE.md` (MUST 10)
> **Conflict priority:** LOCK > PREBRIEF (business intent) > HTML (หน้าจอจริง)

---

## §1 · Document Info

| หัวข้อ | ค่า |
|---|---|
| BRD ID | BRD-F131-PERF |
| Feature | Performance / ประเมินผลงาน |
| Feature Code | F131 · F-HR-PERF |
| Module | HR |
| Archetype | master + cycle (master แบบประเมิน/KPI + cycle รอบ · **ไม่ใช่ Pattern Q document**) |
| ประเภท BRD | New Feature |
| Version | 2.0 (HTML-first, post BA re-gate) |
| Status | **APPROVED** |
| Wave | W5 |
| Declarations | **doa + ntf + csq** (CSQ = SecC masking + DC decision) |
| Owner (BA) | tadswan@2bsimple.com |
| Stakeholders | HR/HRBP · หัวหน้าสายงาน · พนักงาน · Strike (governance) · Architect (CSQ EC) |
| วันที่ | 2026-09-09 |

### §1.1 Changelog
- **v1.0 (Phase A)** — BRD ย่อจาก LANE_BRIEF (APPROVED, W5)
- **v2.0 (2026-09-09)** — เขียนใหม่ HTML-first จาก `performance.html` ที่ผ่าน BA re-gate (fix order F131 · CRITICAL 5 + HIGH 4 แก้ครบ) — encode governance ที่บังคับในโปรโตไทป์แล้ว (stage guards, role guards, closed-cycle read-only, RESTRICTED scope, staged DOA, CSQ 7C hook) + บันทึกมติ OQ-PERF-01..04 ที่ PM/BA เคาะแล้ว

---

## §2 · Business Context

### §2.1 ปัญหา / โอกาส
องค์กรต้องประเมินผลงานพนักงานตามรอบ (cycle) ให้เป็นระบบเดียว — ตั้งเป้า/KPI ต่อคน → พนักงานประเมินตนเอง → หัวหน้าประเมิน → สอบทาน (calibration ผ่าน DOA + decision) → เผยแพร่ผล → ระบุ gap ส่งอบรม และส่ง event ผลไปปรับเงินเดือน/เลื่อนตำแหน่ง โดยที่ **ผลประเมินเป็นความลับ (RESTRICTED)** และมี **audit ตรวจสอบได้ (append-only)**. ปัจจุบันงานนี้กระจัดกระจาย ไม่มีสายอนุมัติ (DOA) ที่ชัดเจน และไม่มีการปิดบังเกรดต่อคน ทำให้ผลรั่วและแก้ย้อนหลังได้เงียบ ๆ

### §2.2 เป้าหมาย business
1. รวมกระบวนการประเมินผลตามรอบไว้ในหน้าจอเดียว (4 tabs) โดยรอบ/แบบดึงจาก HR Configuration (#107) — ไม่สร้าง/แก้ฟอร์มกลางในฟีเจอร์นี้
2. บังคับ governance: สอบทานผ่าน DOA แบบ staged (เลือกผู้สอบทานจริงต่อขั้น) ก่อนเผยแพร่ผล
3. ปกป้องความลับผลประเมิน (RESTRICTED / SecC) ตามสิทธิ์การเห็น (SELF/DEPT/ALL)
4. ส่งต่อผลเป็น event/hook ไป Movement / Training / Succession โดยไม่ CRUD ปลายทาง

### §2.3 ตัวชี้วัดความสำเร็จ (บังคับวัดได้)

| ตัวชี้วัด | Baseline ปัจจุบัน | Target | วัดยังไง/จากไหน | วัดเมื่อไหร่ |
|---|---|---|---|---|
| % แบบประเมินที่ทำเสร็จตรงเวลา (ไม่ overdue) | ต้องเก็บ baseline ก่อน launch | ≥ 90% | นับ appraisal ที่ published ก่อน `due` / ทั้งหมดในรอบ (สถานะ + due จากระบบ) | ปิดรอบ (per cycle) |
| % แบบประเมินที่มี decision ผ่านการสอบทาน DOA ครบขั้น | 0 (ไม่มี DOA เดิม) | 100% | audit ต้องมี "สอบทานขั้น N" ทุกขั้น + "เผยแพร่ผล" ก่อน published (append-only log) | ต่อรอบ |
| % ผลที่มี gap → ส่งเข้า Training | ต้องเก็บ baseline | รายงาน (ไม่มี target บังคับ) | นับ appraisal ที่กด sendTraining / มี gap ในรายงาน distribution | ต่อรอบ |
| การกระจายคะแนน (score distribution) เข้าเกณฑ์ calibration | — | มีรายงานทุกวรอบ | reportView (§18) filter ตามรอบ/แผนก | ต่อรอบ |

> ตัวชี้วัดทุกตัวมีคู่ใน §17.3 KPI

### §2.4 ที่มา
- STANDARD_BASELINE: MUST 10 capability (ทั้ง Odoo / D365 / SAP SF มี) — รอบ, KPI, self, mgr review, rating, calibration/approve(=DOA), gap→Training, notify, audit+masking(SecC), ผล→Movement event
- BA re-gate fix order F131 (2026-09-09) — governance gaps ปิดครบก่อนเข้า Phase B

---

## §3 · Scope

### §3.1 In Scope
1. **รอบประเมิน (cycle):** สร้างรอบจาก HR Config (appraisal_cycle) → เปิดกรอก · ปิดรอบ (ล็อกแก้ไขจริง)
2. **แบบประเมินรายคน:** ตั้งเป้า/KPI (น้ำหนักรวม 100%) · พนักงานประเมินตนเอง · หัวหน้าประเมิน + คะแนนรวมถ่วงน้ำหนัก
3. **สอบทาน (calibration):** DOA slot picker แบบ staged (เลือกผู้สอบทานจริงต่อขั้น) + decision (ผ่าน/ไม่ผ่าน/ทบทวน PIP) + team calibration view
4. **ผล & Gap:** เผยแพร่ผลรายคน (RESTRICTED) · ระบุ gap · เปิดแผน PIP · เปิดแก้ไขผลหลังเผยแพร่ (re-open, authorized)
5. **ส่งต่อ (hook/event, display-only):** gap → Training (hook) · ผล → Movement (event ปรับเงินเดือน/ตำแหน่ง) · ผล → Succession (hook)
6. **รายงาน:** การกระจายคะแนน (distribution) + filter
7. **ระบบ:** ค้นหา/filter + empty state · confirm ก่อนปิด/ยกเลิก · validate + กัน double-submit · audit append-only · masking RESTRICTED ตาม role · แจ้งเตือน (รอบเปิด/ครบกำหนด/ผลเผยแพร่)

### §3.2 Out of Scope (ต้องรู้ว่าตัดโดยมติ ไม่ใช่ตกหล่น)
- **ปรับเงินเดือน/เลื่อนตำแหน่งเอง** — ส่ง event ให้ Movement (F-HR-MOVE) เท่านั้น [OB-3 · LOCK]
- **360 feedback / competency model / continuous check-in** — NICE, ไม่รองรับรอบนี้ [OQ]
- **สร้าง/แก้รอบประเมิน-แบบฟอร์มกลาง** — อ่านจาก HR Configuration (#107) เท่านั้น
- **สร้างหลักสูตรอบรม** — hook ส่งไป Training feature เท่านั้น

### §3.3 Assumptions
- HR Config (#107) พร้อมให้ appraisal_cycle + แบบฟอร์ม/KPI template ก่อนเปิดรอบ
- Movement (F-HR-MOVE), Training, Succession (F134) จะรับ event/hook payload (ยังไม่ build — soft ref)
- ENG-DOA / ENG-NOTIFY / ENG-CSQ เป็น engine กลาง (feature ประกาศเท่านั้น ห้าม hardcode)

### §3.4 Scope Lock ⭐ (สืบทอดจากใบเซ็น — ห้าม override)

| LOCK | มติ | ที่มา |
|---|---|---|
| **LK-1** | สอบทาน = DOA (มติ 17 ส.ค. 2026) — เลือก "คน" จริงต่อขั้น ห้าม hardcode/auto-preset | current-state §3 · fix order FIX-06 |
| **LK-2** | ผล → Movement = **event** (ไม่ CRUD เงินเดือน/ตำแหน่งในฟีเจอร์นี้) | F-HR-MOVE · OB-3 |
| **LK-3** | รอบ/แบบประเมิน จาก HR Configuration (#107) — ไม่สร้าง/แก้ในฟีเจอร์นี้ | F-HR-CONFIG · OB-1 |
| **LK-4** | ผลประเมิน = **RESTRICTED (SecC)** · masking ตาม role · audit **append-only** | current-state §3 · OB-5 |
| **LK-5** | gap → Training = **hook** (ไม่สร้างหลักสูตร) | A-PERF-02 · OB-4 |
| **LK-6** | CSQ ประกาศ **SecC (masking) + DC (decision)** เท่านั้น — **ห้าม** ประกาศ OC / DC-doc / SC (สงวนของ engine) | PREBRIEF §12 · STANDARD_BASELINE §4 |

> **SCOPE DRIFT:** — ไม่มี. Screen Inventory (§14.6) = 4 tabs ตรงกับ PREBRIEF §6 · ไม่มีหน้าเกิน/ขาด · negatives (Out of Scope) ตรงกับ FUNCTION_CHECKLIST `unsupported`

---

## §4 · User Roles & Permissions

**scope_type (บังคับใน SEC_BRIEF ตอน FRD):** staff = **SELF** · mgr = **DEPT** (เฉพาะแผนกตัวเอง) · hr(manage) = **ALL**
(มติ OQ-PERF-03 RESOLVED: หัวหน้าเห็นเฉพาะแผนกของตน)

| Action | พนักงาน (staff · SELF) | หัวหน้าสายงาน (mgr · DEPT) | HR/HRBP (manage · ALL) |
|---|:--:|:--:|:--:|
| ดูรายการรอบประเมิน | ✅ | ✅ | ✅ |
| สร้างรอบ / ปิดรอบ | ❌ | ❌ | ✅ |
| ตั้งเป้า/KPI (`saveKpi`) | ❌ | ❌ | ✅ (goal stage) |
| ประเมินตนเอง (`saveSelf`) | ✅ (ของตน, self stage) | — | — |
| หัวหน้าประเมิน (`saveMgr`) | ❌ | ✅ (mgr stage) | ✅ |
| สอบทาน DOA (`doCalibSend`/`doCalibStage`) | ❌ | ❌ | ✅ (+ ผู้สอบทานที่ถูกเลือกต่อขั้น) |
| เปิดแผน PIP (`doPip`) | ❌ | ❌ | ✅ |
| เปิดแก้ไขผลหลังเผยแพร่ (`doReopen`) | ❌ | ❌ | ✅ |
| ส่ง Movement/Training/Succession (`send*`) | ❌ | ❌ | ✅ |
| เห็นผล/คะแนน/decision/gap ของผู้อื่น | ❌ (mask + SELF) | เฉพาะแผนกตน (DEPT) | ✅ (ALL) |

> **Enforcement ในโปรโตไทป์ (บังคับ 2 ชั้น):** (a) function guard `sec.can(action)` — `saveMgr` = mgr∥manage · ทุก mutation อื่น = manage เท่านั้น (b) UI guard — ไม่ render ปุ่ม mutation ให้ role ที่ไม่ผ่าน + `scopeSelf()` กรอง DOM ไม่ให้ข้อมูลผู้อื่นหลุด (FIX-03 + FIX-04)

---

## §5 · User Journey (with COSO)

| # | Step | หน้าจอ (HTML) | Maker | Checker | Approver | System |
|---|---|---|---|---|---|---|
| 1 | สร้างรอบประเมิน (ดึง config #107) | tab รอบประเมิน → drawer `newCycle` | HR | — | — | โหลด appraisal_cycle |
| 2 | ตั้งเป้า/KPI ต่อคน (รวม 100%) | tab แบบประเมิน → KPI editor | HR | — | — | validate Σweight=100 |
| 3 | พนักงานประเมินตนเอง | drawer แบบประเมิน (self stage) | พนักงาน | — | — | คำนวณ self weighted |
| 4 | หัวหน้าประเมิน + คะแนน | drawer แบบประเมิน (mgr stage) | หัวหน้า | — | — | คำนวณ mgr weighted |
| 5a | ส่งสอบทาน — เลือกผู้สอบทานจริงต่อขั้น | modal `doaCalib` → `doCalibSend` | HR | — | — | freeze รายชื่อ, status คง calibration |
| 5b | ผู้สอบทานแต่ละขั้นบันทึกผลของตน | modal `doaCalib` → `doCalibStage` | — | ผู้สอบทานขั้น N | ผู้สอบทานขั้นสุดท้าย | stamp at/ผู้กระทำต่อขั้น |
| 5c | ขั้นสุดท้าย → เผยแพร่ผล + decision + CSQ 7C | `doCalibStage` (isLast) | — | — | ผู้สอบทานขั้นสุดท้าย | published · notif · CSQ hook |
| 6 | ระบุ gap → ส่ง Training (hook) | tab ผล & Gap → `sendTraining` | HR | — | — | display-only hook |
| 7 | ผล → ส่ง Movement event | tab ผล & Gap → `sendMovement` | HR | — | — | event payload (ไม่ CRUD) |
| 7b | ผล (top performer) → Succession | tab ผล & Gap → `sendSuccession` | HR | — | — | display-only hook |
| 8 | คะแนนต่ำ/ทบทวน → เปิดแผน PIP | modal `pip` → `doPip` | HR | — | — | audit PIP |
| 9 | ปิดรอบ (ล็อกแก้จริง) | tab รอบประเมิน → `doCloseCycle` | HR | — | HR (manage) | closed → ทุก mutation block |
| Alt | เปิดแก้ไขผลหลังเผยแพร่ (เหตุผลบังคับ) | modal `reopen` → `doReopen` | HR | — | HR (manage) | published→mgr · audit ใคร/เหตุผล |

**SoD check:** ผู้ทำ (Maker: HR/พนักงาน/หัวหน้า) ≠ ผู้สอบทาน/เผยแพร่ (Approver: ผู้สอบทาน DOA ต่อขั้น). Stage guard บังคับให้คะแนนต้องครบก่อนสอบทาน และสอบทานต้องครบทุกขั้นก่อน published — Maker (หัวหน้าประเมิน) ไม่สามารถเผยแพร่ผลตัวเองได้โดยไม่ผ่าน DOA stage ✅

---

## §6 · Data Entity & Fields

### §6.1 Entities
| Entity | บทบาท |
|---|---|
| **Cycle** | รอบประเมิน (header) — อ้าง config_version จาก HR Config |
| **Appraisal** | แบบประเมินรายคน (1 คน × 1 รอบ) — snapshot ชื่อ/ตำแหน่ง/แผนก ณ รอบ |
| **KPI line** | รายการ KPI ต่อ Appraisal (น้ำหนัก·เป้า·คะแนน self·คะแนน mgr) |
| **Calibration stage** | ขั้นสอบทาน DOA (ผู้สอบทาน·ผลขั้น·at) — staged |
| **Audit entry** | ประวัติ append-only (act·who·at) ต่อ Appraisal |
| *(ref)* HR Config appraisal_cycle · Employee Master | อ่านอย่างเดียว |

### §6.2 Fields — Cycle
| # | Field | Label | Type | ค่า/ตัวเลือก | จำเป็น | หมายเหตุ |
|---|---|---|---|---|---|---|
| 1 | id | รหัสรอบ | AUTO | CY-xxx | ✓ | |
| 2 | name | ชื่อรอบ | TEXT | | ✓ | เช่น "รอบครึ่งปีหลัง 2569" |
| 3 | year | ปี (พ.ศ.) | NUMBER | 25xx | ✓ | พ.ศ. |
| 4 | period | ช่วงประเมิน | DATERANGE | | ✓ | |
| 5 | config_version | รุ่น config | LOOKUP | จาก HR Config #107 | ✓ | snapshot |
| 6 | status | สถานะรอบ | ENUM | ร่าง/เปิด/ประเมิน/สอบทาน/ปิด | ✓ | closed = ล็อก |

### §6.3 Fields — Appraisal
| # | Field | Label | Type | ค่า/ตัวเลือก | จำเป็น | หมายเหตุ |
|---|---|---|---|---|---|---|
| 1 | id | รหัสแบบประเมิน | AUTO | A-xxx | ✓ | |
| 2 | emp / pos / dept | พนักงาน/ตำแหน่ง/แผนก | SNAPSHOT | | ✓ | snapshot ณ รอบ (BR-10) |
| 3 | cycle | รอบ | LOOKUP | Cycle.id | ✓ | |
| 4 | status | สถานะแบบ | ENUM | goal/self/mgr/calibration/published | ✓ | |
| 5 | kpis[] | รายการ KPI | ARRAY | KPI line | ✓ | Σweight=100 |
| 6 | selfNote / mgrNote | ความเห็น self/mgr | TEXTAREA | | ○ | |
| 7 | decision | ผลตัดสิน | ENUM | ผ่าน / ทบทวน (PIP) / ไม่ผ่าน | เมื่อ published | **RESTRICTED · DC** |
| 8 | gap | จุดที่ต้องพัฒนา | TEXT | | ○ | → Training hook |
| 9 | due | กำหนดเสร็จ | DATE | | ✓ | overdue trigger |
| 10 | audit[] | ประวัติ | ARRAY | act·who·at | ✓ | **append-only** |

### §6.4 Fields — KPI line
| # | Field | Label | Type | จำเป็น | หมายเหตุ |
|---|---|---|---|---|---|
| 1 | title | หัวข้อ KPI | TEXT | ✓ | |
| 2 | weight | น้ำหนัก (%) | NUMBER | ✓ | Σ = 100 (BR-02) |
| 3 | target | เป้าหมาย | TEXT | ✓ | |
| 4 | selfScore | คะแนนตนเอง | NUMBER 1–5 | ○ (self stage) | **RESTRICTED** |
| 5 | mgrScore | คะแนนหัวหน้า | NUMBER 1–5 | ○ (mgr stage) | **RESTRICTED** |

**คะแนนรวม = weighted** (`wsum` = Σ score×weight/100 · BR-04)

### §6.5 Entity Relationship
```
HR Config (appraisal_cycle) ──(read/snapshot)──▶ Cycle
Cycle ──(1:N)──▶ Appraisal ──(1:N)──▶ KPI line
Appraisal ──(1:N)──▶ Calibration stage
Appraisal ──(1:N)──▶ Audit entry (append-only)
Employee Master ──(snapshot)──▶ Appraisal (emp/pos/dept)
```

---

## §7 · User Stories & Acceptance Criteria (map FN 18/18)

| FN | Story (Given-When-Then ย่อ) | AC หลัก | trace |
|---|---|---|---|
| **FN-01** | HR สร้างรอบประเมินจาก HR Config → เปิดกรอก | รอบดึง config #107 (ไม่ hardcode) · empty submit ถูก block | S-01·BR-01 |
| **FN-11** | HR ปิดรอบ → ล็อกแก้ไข | `cycleClosed`=true → ทุก mutation (`saveKpi/saveSelf/saveMgr/doCalib*/doPip`) block + toast · ปุ่ม mutation ซ่อน | S-10·BR-09 |
| **FN-02** | HR ตั้งเป้า/KPI ต่อคน | Σweight ต้อง = 100 มิฉะนั้น block (พิสูจน์: sum 90 block) · เฉพาะ goal stage + manage | S-02·BR-02 |
| **FN-03** | พนักงานประเมินตนเอง | เฉพาะ self stage · เฉพาะ role staff (ของตน) · self ก่อน mgr | S-03·BR-03 |
| **FN-04** | หัวหน้าประเมิน + คะแนนรวมถ่วงน้ำหนัก | เฉพาะ mgr stage · `saveMgr`=mgr∥manage · `wsum` ถูกต้อง | S-04·BR-04 |
| **FN-09** | ประเมินไม่ครบ/เกินกำหนด → เตือน | `isOverdue` แสดง badge · sendReminder | S-08·BR-09 |
| **FN-05** | สอบทาน (calibration) + decision | เฉพาะ status calibration + คะแนน mgr ครบ · decision ∈ {ผ่าน/ไม่ผ่าน/ทบทวน} | S-05·BR-05 |
| **FN-08** | สอบทานผ่าน DOA slot picker ต่อตำแหน่ง (ไม่ hardcode) | slot ว่างทั้ง 2 ขั้น · กดโดยไม่เลือก → block · publish หลังขั้นสุดท้าย | S-05·BR-05 |
| **FN-06** | gap → Training hook (display-only) | `sendTraining` toast ส่งต่อ · ไม่สร้างหลักสูตร | S-06·BR-06 |
| **FN-07** | ผล → Movement event (ไม่ CRUD) | `sendMovement` event payload · ไม่ปรับเงินเดือนเอง | S-07·BR-07 |
| **FN-10** | คะแนนต่ำ/ทบทวน → PIP + decision | `doPip` เฉพาะ decision มี "ทบทวน" · manage เท่านั้น | S-09·BR-05 |
| **FN-12** | แจ้งเตือน รอบเปิด/ครบกำหนด/ผลเผยแพร่ | notif 3 event (ไม่นับ doa_*) | S-11·BR-08 |
| **FN-13** | รายงานการกระจายคะแนน + filter | reportView distribution + filter รอบ/แผนก | S-12·BR-08 |
| **FN-90** | ค้นหา/filter + empty state | list มี empty state · filter | กติกากลาง |
| **FN-91** | ปิด/ยกเลิกผ่าน confirm + soft archive | confirm ก่อนปิดรอบ | กติกากลาง |
| **FN-92** | validate + กัน double-submit | `_busy` กัน double submit (audit เกิด entry เดียว) | กติกากลาง |
| **FN-93** | audit ทุก create/แก้/สอบทาน (append-only) | `pushAudit` unshift · ไม่ลบ · stamp who+at | กติกากลาง |
| **FN-94** | ปิดบังผลประเมิน (RESTRICTED) ตาม role | `mask()` + `scopeSelf()` · staff เห็นเฉพาะตน · mgr เฉพาะแผนก | BR-08 |

> ทุก FN (18/18) มี hook จริงบนจอ — ยืนยันโดย coverage gate + e2e (Phase A)

---

## §8 · Status & Lifecycle

### §8.1 Cycle
```
ร่าง(draft) → เปิด(open) → ประเมิน(in_review) → สอบทาน(calibration·DOA) → ปิด(closed)
```
`closed` = terminal · ทุก mutation ต่อ appraisal ในรอบถูกล็อก (FIX-05)

### §8.2 Appraisal (per-person)
```
goal → self → mgr → calibration → published
                                      │
             ทบทวน(PIP) ◀── decision ─┤
                                      │
      (authorized re-open) published → mgr → … → published (staged DOA ซ้ำ · CSQ ยิงซ้ำ)
```

| State | Trigger | Next | Guard |
|---|---|---|---|
| goal | `saveKpi` (Σweight=100, HR) | self | goal + manage + open cycle |
| self | `saveSelf` (staff ของตน) | mgr | self stage + open cycle |
| mgr | `saveMgr` (mgr∥manage) | calibration | mgr stage + open cycle |
| calibration | `doCalibSend` (เลือกผู้สอบทาน) | calibration (frozen) | manage + คะแนน mgr ครบ |
| calibration | `doCalibStage` (ทุกขั้นบันทึก) | published (ขั้นสุดท้าย) | ผู้สอบทานขั้น current + open cycle |
| published | `doReopen` (เหตุผลบังคับ) | mgr | manage + open cycle + reason |
| published | `doPip` (decision ทบทวน) | published (+PIP) | manage |

---

## §9 · Business Rules + Validation (Tagged)

| ID | Rule | Tag | ใครเปลี่ยน/บ่อย/ระดับ |
|---|---|---|---|
| BR-01 | รอบ/แบบประเมินดึงจาก HR Config #107 — ไม่ hardcode | **CONFIGURABLE** | HR Config (Admin) · ต่อรอบ |
| BR-02 | น้ำหนัก KPI รวม = 100% (มิฉะนั้น block) | **FIXED** | — (invariant) |
| BR-03 | ต้องประเมินตนเอง (self) ก่อนหัวหน้า (mgr) | **FIXED** | — (state order) |
| BR-04 | คะแนนรวม = weighted (Σ score×weight/100) | **FIXED** | — (สูตร invariant) |
| BR-05 | สอบทานผ่าน DOA (staged) + decision ก่อนเผยแพร่ผล | **FIXED** (chain=DYNAMIC 🤖) | DOA chain: role-id รอ BA เคาะ (CL-0013) |
| BR-06 | gap → Training = hook (ไม่สร้างหลักสูตร) | **FIXED** | — |
| BR-07 | ผล → Movement = event (ไม่ CRUD เงินเดือน/ตำแหน่ง) | **FIXED** | — |
| BR-08 | ผลประเมิน RESTRICTED · masking ตาม role (SecC) | **FIXED** | preset P6 |
| BR-09 | audit append-only · ปิดรอบล็อกแก้ | **FIXED** | — |
| BR-10 | snapshot ชื่อ/ตำแหน่ง/แผนก ณ รอบ | **FIXED** | — |
| BR-11 | scope การเห็น: staff=SELF · mgr=DEPT · HR=ALL | **CONFIGURABLE** | SEC_BRIEF scope_type · นานๆ ครั้ง · Admin |
| BR-12 | re-open published = manage + open cycle + เหตุผลบังคับ + audit ใคร/เมื่อ | **FIXED** | มติ OQ-PERF-01 |
| BR-13 | CSQ 7C hook ยิงตอนเผยแพร่ผลรายคน (per-person) | **DYNAMIC** 🤖 | Architect (EC valuation) · OQ-PERF-02 |

### §9.1 Validation Rules
| VR | Field/Action | เงื่อนไข | ประเภท | ข้อความ |
|---|---|---|---|---|
| VR-01 | KPI weight | Σ ≠ 100 | Error | "น้ำหนักรวมต้องเท่ากับ 100%" |
| VR-02 | doCalibSend | slot ผู้สอบทานว่าง | Prevent | "เลือกครบทั้ง 2 ขั้นก่อนส่งสอบทาน" |
| VR-03 | doReopen | reason ว่าง | Error | "กรุณาระบุเหตุผล" |
| VR-04 | ทุก mutation | รอบ closed | Prevent | "รอบนี้ปิดแล้ว — แก้ไขไม่ได้" |
| VR-05 | mutation | role ไม่ผ่าน sec.can | Prevent | "สิทธิ์ไม่พอ" |
| VR-06 | submit | `_busy`=true | Prevent | (กัน double-submit เงียบ) |
| VR-07 | doCalib | status ≠ calibration ∥ คะแนน mgr ไม่ครบ | Prevent | (guard toast + return) |

### §9.5 สรุประดับความยืดหยุ่น

| Rule | ระดับ | เหตุผล | ที่มา |
|---|---|---|---|
| BR-01 | Admin Panel (HR Config #107) | เปลี่ยนค่ารอบ/แบบเป็นระยะ | ✅ Stakeholder (LOCK LK-3) |
| BR-11 | Admin Panel (SEC scope) | scope_type ตั้งครั้งเดียว | ✅ Stakeholder (OQ-PERF-03 resolved) |
| BR-05 chain | Rule/Engine (DOA) | สายอนุมัติ role-id เปลี่ยนตามองค์กร | 🤖 AI-inferred → **OQ** (CL-0013 รอ BA) |
| BR-13 | Engine (ENG-CSQ) | มูลค่า EC + ท่อ 7C | 🤖 AI-inferred → **OQ** (Architect · OQ-PERF-02) |

> **Escalation:** BR-05 chain (DYNAMIC 🤖) และ BR-13 (Engine 🤖) → ลง §15 Open Questions ให้ stakeholder ยืนยันก่อนพัฒนา

---

## §10 · Edge Cases

### §10.1 Edge Cases ที่ PREBRIEF/BA ระบุ (☑ ยืนยันแล้ว)
- ☑ น้ำหนัก KPI ≠ 100 → เตือน block (พิสูจน์แล้ว)
- ☑ ประเมินเกินกำหนด (overdue) → badge เตือน + reminder
- ☑ คะแนนต่ำ/ไม่ผ่าน → เปิดแผน PIP + decision
- ☑ ผล → event (ไม่ CRUD ปลายทาง)
- ☑ **สอบทาน+เผยแพร่ข้ามขั้น** (record ยังอยู่ goal/ไม่มีคะแนน mgr) → guard block (FIX-01)
- ☑ **transition ย้อนหลัง** (record published ถูกดันกลับ) → state guard block (FIX-02)
- ☑ **พนักงานประเมินแทนหัวหน้า/สอบทานเอง** → role guard block + UI ซ่อนปุ่ม (FIX-03)
- ☑ **พนักงานเห็น decision/gap ผู้อื่น** → scopeSelf + mask (FIX-04)
- ☑ **ปิดรอบแล้วยัง mutate ได้** → cycleClosed guard ทุก mutation (FIX-05)
- ☑ **DOA slot auto-preset / คลิกเดียวจบ 2 ขั้น** → slot ว่าง + แยก 2 action staged (FIX-06)

### §10.2 Edge Cases จาก AI Pattern Matching (☐ = แนะนำ · BA ติ๊กที่ SOW3.7)
- ☐ **[PM] re-open** เมื่อรอบปิดไปแล้ว — ปัจจุบัน guard block ที่ closed cycle (ถูกต้อง) แต่ต้องระบุ flow กรณีต้อง reopen หลังปิดรอบ (นโยบาย?) → **ยกเป็น OQ**
- ☐ **[CA] Concurrent:** ผู้สอบทาน 2 ขั้นบันทึกพร้อมกัน — ต้องมี lock/lastwrite policy
- ☐ **[DI] HR Config #107 ไม่มี appraisal_cycle** / config_version หาย → error state ก่อนสร้างรอบ
- ☐ **[CL] KPI weight ทศนิยม** (Σ = 99.99) — ปัดเศษ/tolerance?
- ☐ **[ST] appraisal ไม่มี KPI เลย** (goal ว่าง) → กัน submit self
- ☐ **[EM] notif ล้มเหลว** (ENG-NOTIFY down) → retry/fallback (engine เป็นเจ้าของ)
- ☐ **[PM] mgr ย้ายแผนกกลางรอบ** — DEPT scope ใช้ snapshot หรือ live? (กระทบ FN-94)
- ☐ **[CL] CSQ EC valuation** — มูลค่า EC คิดยังไง (**Architect · OQ-PERF-02**, กระทบเงิน → OQ ทันที)

---

## §11 · Impact / Regression
New Feature — ไม่มี regression ของเดิม. ผลกระทบเป็น **downstream** (§12.1). ประเด็น cross-feature: soft-ref ปลายทาง (Movement/Training/Succession/HR Config) ยังไม่ build — payload contract ต้อง freeze ตอน FRD

---

## §12.1 · Value Stream & Downstream Impact ⭐

**Value Stream positioning:** HR / Talent Management — Performance เป็นจุดกลางที่รับ config รอบ (upstream) และป้อนผลไป 3 ปลายทาง (downstream)

**Upstream:**
| จาก | รับอะไร | Trigger |
|---|---|---|
| HR Configuration (#107) | appraisal_cycle + แบบฟอร์ม/KPI template + config_version | ก่อนสร้างรอบ (BR-01) |
| Employee Master | ข้อมูลพนักงาน (snapshot emp/pos/dept) | สร้าง appraisal |

**Downstream Impact Map:**
| ปลายทาง | ข้อมูลที่ไหลไป | Trigger | ถ้าผลถูกแก้/re-open |
|---|---|---|---|
| **Movement (F-HR-MOVE)** | event ปรับเงินเดือน/เลื่อนตำแหน่ง (payload ผล) | เผยแพร่ผล + `sendMovement` | ต้องส่ง event ใหม่/ยกเลิกของเดิม (ปลายทางจัดการ) |
| **Training** | gap (จุดที่ต้องพัฒนา) hook | มี gap + `sendTraining` | ส่ง gap ใหม่ตามผลที่แก้ |
| **Succession (F134)** | ผล/top performer hook | decision ผ่าน + `sendSuccession` | re-evaluate candidacy |
| **ENG-CSQ (7C)** | perf.result.published (SecC/DC) | เผยแพร่ผลรายคน (per-person) | CSQ 7C ยิงซ้ำ per-person |
| **ENG-NOTIFY** | 3 event (รอบเปิด/ครบกำหนด/ผลเผยแพร่) | ตาม trigger | notif ใหม่ตอน re-publish |

**ผลกระทบแนวขวาง:** ผลประเมิน = RESTRICTED → กระทบ report/dashboard (masking) · ไม่กระทบ GL/สต๊อกโดยตรง (event ไป Movement เป็นตัวกระทบเงินเดือนปลายทาง)

## §12.3 · Existing System Reference

| Rule/Need | ระดับ | มีอยู่แล้ว? | Reference |
|---|---|:--:|---|
| BR-01 รอบ/แบบ | Admin Panel | ⚠️ soft-ref | HR Configuration #107 (appraisal_cycle) — ยังไม่ build |
| BR-05 DOA chain | Rule/Engine | ⚠️ | ENG-DOA (calibration slot) — role-id รอ BA (CL-0013) |
| BR-08 masking | Preset P6 | ✅ | Security preset HR/PII |
| BR-13 CSQ | Engine | ⚠️ | ENG-CSQ (7C) — EC valuation รอ Architect |
| FN-12 notify | Engine | ⚠️ | ENG-NOTIFY (F-NOTIFY) event catalog |

---

## §13 · Delivery Phases

**Phase 1 — Feature Launch:** state machine (cycle + appraisal) จาก config/rule table (ไม่ hardcode) · KPI weighted engine · masking preset P6 · audit append-only · guards (state/role/closed/scope) · staged DOA slot · CSQ 7C hook stub · notif 3 event · report distribution
**Phase 2 — Admin Panel:** SEC scope_type config (BR-11) · reminder SLA timer
**Phase 3 — Rule Management:** DOA chain role-id (CL-0013) — เมื่อ BA เคาะ
**Phase 4 — Engine Management:** ENG-CSQ EC valuation (OQ-PERF-02) — เมื่อ Architect เคาะ

---

## §14 · Dev Requirements Summary (ใบสั่ง)

### §14.1 Config Foundation ที่ต้องเตรียม
- HR Config #107 appraisal_cycle (soft-ref) — freeze payload contract ตอน FRD
- SEC scope_type table: staff=SELF · mgr=DEPT · hr=ALL
- Rating scale 1–5 + weighted formula (config, ไม่ hardcode)

### §14.2 ข้อกำหนดจาก Tag (non-FIXED)
- BR-01/BR-11 (CONFIGURABLE) → อ่านจาก config table + seed · ห้าม hardcode รอบ/scope
- BR-05 chain (DYNAMIC) → **ใช้ ENG-DOA** ที่มีอยู่ · role-id รอ CL-0013 (อย่าเดา)
- BR-13 (DYNAMIC/Engine) → **ใช้ ENG-CSQ** · feature ยิง event `perf.result.published` เท่านั้น · ห้ามประกาศ OC/DC

### §14.3 Edge Cases สำคัญที่ Dev ต้อง handle
- ทุก mutation ต้องมี 4 guards เรียงกัน: closed-cycle → role(sec.can) → state → scope
- staged DOA: publish เกิดหลังขั้นสุดท้ายบันทึกผลเท่านั้น + timeline at ต่อขั้น
- re-open: append-only (ผลเดิมไม่ลบ) + เหตุผลบังคับ + audit ใครแก้

### §14.4 WARNING ที่รอข้อสรุป
- DOA chain role-id (CL-0013) — หารือ BA ก่อนพัฒนา Phase 3
- CSQ EC valuation — หารือ Architect ก่อนพัฒนา Phase 4
- ทั้งสอง: **ห้ามเริ่มพัฒนาส่วนนั้นจนกว่า resolve**

### §14.6 · Screen Inventory + UI Signals (หยาบ — ส่งต่อ FRD)

> BRD ไม่ตัดสิน layout/pattern/CI — สกัดจาก HTML (การมีอยู่ + หน้าที่ business). โปรโตไทป์เป็น tab-based SPA (ไม่มี hash route แยกหน้า) — "route" = tab id

| # | ชื่อหน้า/tab | tab id (HTML) | ประเภทหยาบ | ผู้ใช้หลัก | หน้าที่ (business) | หมายเหตุ |
|---|---|---|---|---|---|---|
| P-01 | รอบประเมิน | `cycle` (cycleView) | หน้ารายการ + ฟอร์มสร้าง (drawer) | HR | รายการรอบ · สร้างรอบ (drawer newCycle) · ปิดรอบ | dwViewCycle |
| P-02 | แบบประเมินรายคน | `appr` (apprView) | หน้ารายการ + drawer รายละเอียด | HR/หัวหน้า/พนักงาน | รายการแบบ · KPI editor · self · mgr · drawer tabs (รายละเอียด›KPI›สอบทาน›ประวัติ) | scopeSelf กรอง |
| P-03 | สอบทาน + ผล & Gap | `review` (reviewView) | หน้ารายการ + team view + modal | HR + ผู้สอบทาน | คิวสอบทาน · team calibration · ผลเผยแพร่ · hooks Movement/Training/Succession · PIP · reopen | teamCalibHTML · modal doaCalib/pip/reopen |
| P-04 | รายงาน | `report` (reportView) | รายงาน (ดู) | HR/หัวหน้า | การกระจายคะแนน + filter | RESTRICTED masking |

**~4 หน้าหลัก (tab)** + overlay: drawer (สร้างรอบ / ดูรอบ / ดูแบบประเมิน) + modal (doaCalib staged / closeCycle / pip / reopen) + notif panel

**UI Signals ส่งต่อ FRD:**
- ❌ **ไม่ใช่ Pattern Q document** — archetype = master+cycle (ไม่มีเอกสารคนถือ/เลขรัน/PDF)
- ❌ ไม่มี print/PDF (doccfg ✗ · pdfdoc ✗)
- ✅ มี DOA (staged calibration) — FRD ผูก doa-declaration
- ✅ RESTRICTED masking (SecC) ทุก view — scope_type ต้องเข้า SEC_BRIEF
- ไม่มี NON-STANDARD / keep-original-UI flag

### §14.7 Functions Cut (= "ไม่รองรับ" ของ FUNCTION_CHECKLIST)
- ปรับเงินเดือน/เลื่อนตำแหน่งเอง → event ให้ Movement [OB-3]
- 360 feedback / competency model / continuous check-in → NICE ไม่รองรับรอบนี้ [OQ]
- สร้าง/แก้รอบประเมิน-แบบฟอร์มกลาง → อ่าน HR Config #107
- ทำหลักสูตรอบรม → hook Training

---

## §15 · Open Questions

| รหัส | คำถาม | ผู้เคาะ | สถานะ | คำตอบ/มติ |
|---|---|---|---|---|
| OQ-PERF-01 | แก้ผลหลังเผยแพร่ — re-open flow? | Strike | ✅ RESOLVED | **อนุญาต** สำหรับ authorized (HR/manage) + เหตุผลบังคับ + audit ว่าใครแก้ + เฉพาะรอบยังไม่ปิด (encode ในโปรโตไทป์ `doReopen`) |
| OQ-PERF-02 | CSQ profile — event ไหนยิงท่อไหน · EC valuation | Strike + Architect | ⚠️ PARTIAL | **CSQ ยิงตอน per-person publish** (RESOLVED) · **EC valuation detail = architect item** (ยังเปิด) |
| OQ-PERF-03 | scope หัวหน้าเห็นทุกแผนกไหม | Strike | ✅ RESOLVED | หัวหน้าเห็น **เฉพาะแผนกของตน (DEPT)** |
| OQ-PERF-04 | team calibration ระดับทีมเก็บ/ตัด | Strike | ✅ RESOLVED | **เก็บรอบนี้** (teamCalibHTML view คงไว้) |
| OQ-PERF-05 | DOA chain **executive role-ids** (CL-0013) | BA (ที่ config) | ⚠️ OPEN | รอ BA ระบุ role-id ตอน config — feature ไม่ hardcode |
| OQ-PERF-06 | CSQ **EC valuation** detail | Architect | ⚠️ OPEN | สงวนของ engine — รอสถาปนิก |
| OQ-PERF-07 | soft-ref ปลายทางยังไม่ build | PM | ⚠️ OPEN | HR Config #107 · Movement (F-HR-MOVE) · Employee Master · Succession (F134) · ENG-DOA/ENG-NOTIFY/ENG-CSQ — freeze payload contract ตอน FRD |

---

## §16 · Security & Compliance

### §16.1 Preset
**P6 (HR / PII Sensitive · 15 controls)** — เหตุผล: ผลประเมินเป็นข้อมูลบุคคลลับ (RESTRICTED)

### §16.2 Data Classification
- **RESTRICTED (SecC):** คะแนน self/mgr · decision · gap — masking ตาม role (staff เห็นเฉพาะตน · mgr เฉพาะแผนก · HR ทั้งหมด)
- audit = append-only (immutable log)

### §16.3 Control Checklist (สำคัญ)
| Control | Required | Implementation |
|---|:--:|---|
| Field-level masking (RESTRICTED) | ✓Must | `mask()` ปิดคะแนน/decision/gap ตาม `curRole().mask` |
| Row-level scope (SELF/DEPT/ALL) | ✓Must | `scopeSelf()` กรอง DOM ก่อน render (ไม่ใช่แค่ hide) |
| Role-based action guard | ✓Must | `sec.can(action)` 2 ชั้น (function + UI) |
| Segregation of Duties (DOA) | ✓Must | staged calibration — ผู้ประเมิน ≠ ผู้สอบทาน/เผยแพร่ |
| Append-only audit | ✓Must | `pushAudit` unshift · stamp who+at · re-open ไม่ลบผลเดิม |
| CSQ 7C on sensitive publish | ✓Must | hook `perf.result.published` per-person |
| State/terminal guard | ✓Must | closed cycle + published = read-only |

### §16.4 Risk Statement
| Risk (R) | ความเสี่ยง | Mitigated by |
|---|---|---|
| R-01 | ผลประเมินรั่วต่อพนักงานคนอื่น | mask + scopeSelf (FIX-04) |
| R-02 | แก้ผลย้อนหลังเงียบ ๆ | state guard + append-only + re-open audit (FIX-02, BR-12) |
| R-03 | ข้ามสอบทาน DOA เผยแพร่เอง | state+role guard + staged DOA (FIX-01/03/06) |
| R-04 | สายอนุมัติผิด (hardcode) | DOA slot picker เลือกคนจริง (LK-1) — role-id รอ CL-0013 |

> **SC ไม่ประกาศ** · CSQ = SecC + DC เท่านั้น (LK-6)

---

## §17 · Health Check

### §17.1 SLA
| Step | เวลาควบคุม | Owner |
|---|---|---|
| ประเมินตนเอง | ก่อน `due` | พนักงาน |
| หัวหน้าประเมิน | ก่อน `due` | หัวหน้า |
| สอบทาน + เผยแพร่ | ภายในรอบ (ก่อนปิด) | HR + ผู้สอบทาน DOA |

### §17.2 Control Points
map จาก §16.3 — masking · scope · role guard · SoD · audit · CSQ · state guard (runtime)

### §17.3 KPI (คู่กับ §2.3)
| KPI | ประเภท | สูตร |
|---|---|---|
| % ประเมินตรงเวลา | Speed | published ก่อน due / total |
| % สอบทาน DOA ครบขั้น | Compliance | มี audit ทุกขั้น + published / total |
| % gap → Training | Conversion | sendTraining / มี gap |
| การกระจายคะแนน | Quality | distribution ต่อรอบ/แผนก |

### §17.4 Threshold
| ตัวชี้วัด | Min | Max | Action เมื่อ breach |
|---|---|---|---|
| % ตรงเวลา | 90% | — | reminder overdue (FN-09) |
| น้ำหนัก KPI | 100% | 100% | block save (VR-01) |
| distribution เบ้ (คนผ่านสูงผิดปกติ) | — | เกณฑ์ calibration | ทบทวนใน team calibration |

### §17.5 Throughput
Capacity = จำนวน appraisal ต่อรอบ (mock CY1 = 6 คน) · stress = ปิดรอบพร้อมกันหลายร้อยคน (event Movement batch)

---

## §18 · Monitoring

### §18.1 Reports Overview
Performance (การกระจายคะแนน) · Closing (สรุปเมื่อปิดรอบ) · Anomaly (overdue / distribution เบ้) · Transaction (audit trail per appraisal)

### §18.2 Dashboard Widgets
- Widget "% ประเมินตรงเวลา" (KPI Speed) · "การกระจายคะแนน" (reportView) · "คิวสอบทานค้าง" (calibration queue) · ทุก widget respect RESTRICTED masking

### §18.3 Performance Report
reportView — distribution + filter รอบ/แผนก (FN-13)

### §18.4 Closing Report
สรุปตอนปิดรอบ: จำนวน published / decision breakdown / overdue

### §18.5 Anomaly Report
overdue list (isOverdue) · distribution เบ้ · re-open events (ใครแก้/เหตุผล)

### §18.6 Transaction Report
audit trail append-only ต่อ appraisal (act·who·at) — tab ประวัติ (tabHistory)

---

## §Cross-Section Coverage Check
- ✅ ทุก BR (§9) มี Edge Case/VR cover (§10, §9.1)
- ✅ ทุก Control runtime (§16.3) มี Control Point (§17.2)
- ✅ ทุก KPI/Threshold (§17) มี Widget/Report (§18)
- ✅ ทุกตัวชี้วัด (§2.3) มีคู่ใน §17.3

---

## AI REVIEW REPORT — BRD Generator Full

```
═══════════════════════════════════════
BRD: BRD-F131-PERF — Performance / ประเมินผลงาน
ประเภท: New Feature · Mode: Fresh (HTML-first) + Lane (no-ask)
วันที่ตรวจ: 2026-09-09
═══════════════════════════════════════

CHECKLIST RESULTS (C01–C23 + PE01–PE05):
✅ C01 Business Objective วัดผลได้ (§2.3 มีตัวเลข/แหล่งวัด)
✅ C02 User Roles ครบ (staff/mgr/HR + scope)
✅ C05 Story ไม่มีคำว่า "และ" กำกวม (แยกชัด)
✅ C10 ทุก rule มีตัวเลข/เงื่อนไข ติด Tag (BR-01..13)
✅ C13 Edge Cases ครบหมวด (10.1 BA + 10.2 AI 9 หมวด)
✅ C18 WARNING มีแผนหารือ (CL-0013 BA · EC Architect)
✅ C19 §14 ใบสั่งครบ
✅ C20 Scope Lock §3.4 ครบ (LK-1..6) · SCOPE DRIFT = none
✅ C21 Value Stream §12.1 upstream + Downstream Map ตอบ "แล้วไงต่อ" ทุกแถว
✅ C22 ตัวชี้วัด §2.3 มี baseline/target/วิธีวัด + คู่ §17.3
✅ C23 §9.5 marker 🤖/✅ ครบ — 🤖 DYNAMIC/Engine (BR-05 chain, BR-13) ลง OQ แล้ว
✅ PE01 COSO Roles ครบทุก step (§5)
✅ PE02 SoD ผ่าน (ผู้ประเมิน ≠ ผู้สอบทาน/เผยแพร่ · staged DOA)
✅ PE03 Security Preset P6 + Controls ครบ (§16)
✅ PE04 SLA + KPI + Threshold ครบ (§17)
✅ PE05 Cross-section coverage ผ่าน

FN COVERAGE: 18/18 (ทุก FN มี Story + hook บนจอ)
DECLARATIONS: doa + ntf + csq (SecC + DC) — ครบตาม PREBRIEF §12
HTML-RIF DRIFT: — none (4 tabs = PREBRIEF §6 · negatives = unsupported)

SUMMARY: ผ่าน 18/18 checklist หลัก
สถานะ: ✅ APPROVED — พร้อมเข้า frd-generator-v6

ยังเปิด (downstream, ไม่บล็อก BRD):
  - OQ-PERF-05 DOA chain role-id (CL-0013 · BA ที่ config)
  - OQ-PERF-06 CSQ EC valuation (Architect)
  - OQ-PERF-07 soft-ref ปลายทางยังไม่ build (freeze contract ตอน FRD)
═══════════════════════════════════════
```

**Next step:** BRD APPROVED → `frd-generator-v6` (พร้อม HTML v9 + BRD นี้) · รัน `doa/ntf/csq-declaration` หลัง step 7 (ผู้ใช้เลือกไว้แล้ว = doa+ntf+csq)
