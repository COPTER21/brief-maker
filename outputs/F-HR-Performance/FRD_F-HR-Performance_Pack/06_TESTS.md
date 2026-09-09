# 06_TESTS — F131 Performance / ประเมินผลงาน

> **Audience:** QA engineer
> **Purpose:** Acceptance Criteria (per FN 18/18) + DoD + cross-module + microcopy-aware expected
> **Coverage source:** 02_API + 03_LOGIC + 05_RULES + performance.html (verbatim microcopy)

---

## §6.1 Acceptance Criteria (AC per FN)

### AC-01 · FN-01 สร้างรอบจาก HR Config
**Given** role HR, HR Config #107 มี appraisal_cycle **When** POST /cycles (config_ref valid) **Then** 201, cycle.status='open', config_version snapshot **And** toast "สร้างรอบ · เปิดกรอก · แจ้งเตือนผู้เข้าร่วมแล้ว" **And** notif "รอบประเมินเปิดกรอกแล้ว". Empty submit (ไม่เลือกรอบ) → block + "กรุณาเลือกรอบจากตั้งค่า HR".

### AC-02 · FN-11 ปิดรอบ (ล็อกจริง · FIX-05)
**Given** cycle open **When** POST /cycles/:id/close **Then** status='closed', toast "ปิดรอบแล้ว · ล็อกการแก้ไข (soft archive)" **And** ทุก mutation ต่อ appraisal ในรอบ → 409 BR_CYCLE_CLOSED ("รอบนี้ปิดแล้ว — แก้ไขไม่ได้") **And** KPI tab แสดง banner "รอบนี้ปิดแล้ว — ดูได้อย่างเดียว แก้ไขไม่ได้".

### AC-03 · FN-02 KPI Σ=100
**Given** appraisal goal, role HR **When** PUT /kpis Σweight=90 **Then** 422 BR_KPI_WEIGHT_NOT_100 "น้ำหนัก KPI รวมต้องเท่ากับ 100% (ตอนนี้ 90%)". **When** Σ=100 **Then** 200 status→self, toast "บันทึกเป้า/KPI แล้ว · เปิดให้พนักงานประเมินตนเอง".

### AC-04 · FN-03 ประเมินตนเอง
**Given** appraisal self, role staff (own) **When** POST /self (scores 1–5 ครบ) **Then** status→mgr, toast "บันทึกประเมินตนเองแล้ว · ส่งต่อหัวหน้าประเมิน". คะแนนไม่ครบ → "กรุณาให้คะแนนตนเองครบทุก KPI (1–5)".

### AC-05 · FN-04 หัวหน้าประเมิน + weighted
**Given** appraisal mgr, role mgr∥HR **When** POST /manager-review (mgr_score ครบ) **Then** status→calibration, `weighted_score = Σ(score×weight)/100` ถูกต้อง, toast "บันทึกผลหัวหน้าแล้ว · ส่งเข้าสอบทาน (DOA)". (เช่น w60×5 + w40×4 → 4.60)

### AC-06 · FN-09 overdue → เตือน
**Given** appraisal due<today, status≠published **Then** badge "เกินกำหนด" + banner "มี N แบบประเมินเกินกำหนด — ต้องเตือนผู้ประเมิน" **When** "ส่งการเตือน" **Then** toast "ส่งการเตือนผู้ที่ประเมินไม่ครบ/เกินกำหนดแล้ว".

### AC-07 · FN-05 สอบทาน + decision
**Given** appraisal calibration, ผู้สอบทานขั้นสุดท้าย **When** doCalibStage(isLast) เลือก decision **Then** status→published, decision ∈ {ผ่าน/ทบทวน (PIP)/ไม่ผ่าน}, toast "เผยแพร่ผล · บันทึกผลเข้า 7C · RESTRICTED · แจ้งเตือนพนักงานแล้ว".

### AC-08 · FN-08 staged DOA slot picker
**Given** doaCalib modal เปิด (จังหวะ 1) **Then** slot 1+2 **ว่างทั้งคู่** (ไม่ preset). กด "ส่งสอบทาน" โดยไม่เลือก → block "กรุณาเลือกผู้สอบทานให้ครบทุกขั้น". เลือกครบ → "ส่งสอบทานแล้ว · รอผู้สอบทานขั้นที่ 1 บันทึกผล", status **คง calibration**. ขั้น 1 บันทึก → "บันทึกผลสอบทานขั้น 1 แล้ว · รอผู้สอบทานขั้นถัดไป" (ยังไม่ publish, stamp at). ขั้นสุดท้าย → publish. **Publish เกิดหลังขั้นสุดท้ายเท่านั้น + ทุกขั้นมี at.**

### AC-09 · FN-06 gap → Training hook
**Given** appraisal published + gap **When** "ส่งไปอบรม" **Then** toast 'ส่งจุดที่ต้องพัฒนา "…" ไปหลักสูตรอบรม (ส่งต่อ ไม่แก้ที่นี่) — ไม่สร้างหลักสูตรในหน้านี้' **And** ไม่มี write ปลายทาง.

### AC-10 · FN-07 ผล → Movement event
**Given** appraisal published (มี/ไม่มี gap) **When** "ส่งเรื่องปรับตำแหน่ง/เงินเดือน" **Then** toast "ส่งเรื่องปรับเงินเดือน/เลื่อนตำแหน่งให้ระบบโยกย้าย (ไม่ปรับเอง)", emit `perf.result.movement_requested` **And** ไม่ CRUD เงินเดือน/ตำแหน่ง.

### AC-11 · FN-10 PIP
**Given** published decision "ทบทวน" **When** "เปิดแผน PIP" (gap+ระยะ+แผน) **Then** toast "เปิดแผน PIP แล้ว", audit "เปิดแผน PIP · {duration}". gap ว่าง → "กรุณาระบุประเด็นที่ต้องพัฒนา".

### AC-12 · FN-12 แจ้งเตือน 3 event
**Then** notif panel มี 3 ประเภท: "รอบประเมินเปิดกรอกแล้ว" · "ใกล้ครบกำหนดประเมิน" · "ผลประเมินเผยแพร่แล้ว" (ไม่นับ doa_*).

### AC-13 · FN-13 report distribution
**Given** cycle มี appraisal คะแนน **When** GET /reports/distribution **Then** stat tiles (แบบประเมินในรอบ/เผยแพร่ผลแล้ว/ทบทวน PIP) + buckets (ต่ำ<3.0/ปานกลาง 3.0–3.9/ดี 4.0–4.5/ดีเยี่ยม>4.5), filter รอบ เปลี่ยนค่าได้.

### AC-14 · FN-90 search/filter/empty
**When** ค้นหาไม่พบ **Then** empty state "ไม่พบแบบประเมินที่ค้นหา" + "ลองปรับคำค้นหรือล้างตัวกรอง" + ปุ่ม "ล้างตัวกรอง". Filter status ทำงาน.

### AC-15 · FN-92 double-submit
**When** double-click submit **Then** `_busy`/idempotency block → audit เกิด **entry เดียว** (ไม่ซ้ำ).

### AC-16 · FN-93 audit append-only
**When** ทุก create/แก้/สอบทาน **Then** audit entry (act·who·at) เพิ่ม newest-first, ไม่ลบ/แก้ของเดิม. Re-open ไม่ลบผลเดิม.

### AC-17 · FN-94 RESTRICTED scope/mask
**Given** role staff **Then** เห็นเฉพาะแบบประเมินของตน (คนอื่นไม่อยู่ DOM/payload); tab สอบทานซ่อน; เปิดของผู้อื่น → "ข้อมูลนี้เป็นความลับ (RESTRICTED) — ดูได้เฉพาะแบบประเมินของตนเอง". **Given** role mgr (dept=ฝ่ายผลิต) **Then** เห็นเฉพาะ appraisal แผนกตน; เปิดนอกแผนก → "หัวหน้าดูได้เฉพาะแผนกของตน". **Given** HR **Then** ALL. คะแนน mask = `•••` เมื่อ role.mask.

### AC-18 · re-open published (OQ-PERF-01)
**Given** published, open cycle, role HR **When** "เปิดแก้ไขผล" reason ว่าง → block "กรุณาระบุเหตุผล". reason มี → status→mgr, decision เคลียร์, audit "เปิดแก้ไขผลหลังเผยแพร่ · เหตุผล:…" (who+at, ผลเดิมไม่ลบ), toast "เปิดแก้ไขผลแล้ว · ส่งกลับขั้นหัวหน้าประเมิน · บันทึกผู้แก้ไว้ในประวัติ". closed cycle → block. non-published → "เปิดแก้ไขได้เฉพาะผลที่เผยแพร่แล้ว". Re-publish → CSQ ยิงซ้ำ per-person.

### AC-19 · guard cascade bypass (FIX-01..06 · negative)
**Given** bypass attempts **Then**: (P2) doCalib กับ record goal/mgr null → block ERR_STAGE_INVALID/BR_MGR_SCORE_INCOMPLETE. (P1) saveSelf/saveKpi/saveMgr กับ published → ERR_STAGE_INVALID. (P3) staff เรียก saveMgr/doCalib/send* → ERR_INSUFFICIENT_ROLE + UI ไม่มีปุ่ม. (P4) closed cycle → BR_CYCLE_CLOSED. Order = closed→role→stage→scope.

---

## §6.2 Test Case Inventory

| TC ID | Name | Type | Maps to | Priority |
|---|---|---|---|---|
| TC-01..13 | AC-01..13 happy per FN | API/E2E | FN-01..13 | P0/P1 |
| TC-14 | search/filter/empty | UI | AC-14 | P1 |
| TC-15 | double-submit | API | AC-15 | P0 |
| TC-16 | audit append-only | API | AC-16 | P0 |
| TC-17 | RESTRICTED scope/mask (staff/mgr/HR) | API/E2E | AC-17 | P0 |
| TC-18 | re-open published | API | AC-18 | P1 |
| TC-19 | guard cascade bypass P1-P4 | API negative | AC-19 | P0 |
| TC-CC-01 | concurrent staged review (EC-05) | stress | EC-05 | P1 |
| TC-CFG-01 | HR Config missing (EC-06) | integration | EC-06 | P2 |
| TC-DEPT-01 | mgr dept snapshot scope (EC-10) | API | EC-10 | P2 |
| XT-01..05 | cross-module dispatch | integration | §6.9 | P1 |

---

## §6.3 Test Data Setup

> **⚠️ Mock-data note (OQ-PERF-11 · spec-level, ไม่แก้ HTML):** ในโปรโตไทป์ mgr persona dept=**ฝ่ายผลิต** แต่ appraisal ขั้น mgr เดียว (อรทัย A3) = **ฝ่ายบัญชี** → หัวหน้าเข้าไม่ถึงผ่าน UI dept-scoped. **แนะนำเพิ่ม mock appraisal ขั้น mgr ในฝ่ายผลิต** เพื่อ QA สาธิต manager-review ในขอบเขต. (ไม่บล็อก — เป็น demo/coverage gap)

### Roles (mirror PERF.roles)
- `hr` (HR/HRBP · manage=true · mask=false · ALL)
- `mgr` (หัวหน้าสายงาน · manage=false · dept=ฝ่ายผลิต · DEPT)
- `staff` (พนักงาน · mask=true · SELF)

### Data (mirror PERF)
- 2 cycles: CY1 (open) · CY2 (closed) · appraisals ครบทุก state (goal/self/mgr/calibration/published×2 incl. PIP) · KPI 2–3/คน · audit seeds.

---

## §6.4 Definition of Done
### Code
- [ ] AC-01..19 implemented + unit tests · guard cascade (FN-18) coverage ครบ 4 ชั้น
- [ ] Integration (API+DB+ENG-DOA/NOTIFY/CSQ) pass · E2E happy + bypass P1-P4 pass
- [ ] Coverage ≥80% logic layer
### Documentation
- [ ] 07_LOCKED reflects final · ENG-GRADE (§3.2) register CUBIC (Phase 2 · LD-06)
### QA
- [ ] P0/P1 pass · no P0/P1 bugs · RESTRICTED scope verified (staff/mgr/HR)
### Deployment
- [ ] Migration + RLS + append-only trigger tested · soft-ref stubs (HR Config #107 / ENG-*) mocked in staging

---

## §6.5 WebSocket / Realtime Events
- `perf.cycle.opened` → participants notif panel
- `perf.result.published` → employee notif (per-person)
- `perf.deadline.overdue` → assignee reminder
> doa_pending/doa_result มาจาก ENG-DOA (ไม่ทดสอบซ้ำที่นี่). Verify: publish → พนักงานเห็น notif "ผลประเมินเผยแพร่แล้ว".

---

## §6.6 Performance Benchmarks
| Endpoint | P95 | 
|---|---|
| GET /appraisals (scoped list) | <500ms |
| GET /reports/distribution | <600ms |
| POST /calibration/stage (publish + CSQ + notify) | <1200ms |

## §6.7 Test Environment Notes
- Staging tenant + mock HR Config #107 (appraisal_cycle) + ENG-DOA/CSQ/NOTIFY in TEST mode (deterministic).
- Runtime e2e ตัวจริงอยู่ที่ `outputs/F-HR-Performance/_e2e/` (Phase A · FN 18/18 · FN-40 negative).

---

## §6.8 Trace: AC → Logic Coverage

| AC | API | Functions | Engines |
|---|---|---|---|
| AC-01 | API-02 | FN-01 | ENG-NOTIFY |
| AC-02 | API-04 | FN-02, FN-18 | — |
| AC-03 | API-08 | FN-03 | — |
| AC-04 | API-09 | FN-04 | — |
| AC-05 | API-10 | FN-05, FN-19 | — |
| AC-06 | API-15 | FN-13 | ENG-NOTIFY |
| AC-07/08 | API-11/12 | FN-06, FN-07 | ENG-DOA, ENG-CSQ, ENG-NOTIFY |
| AC-09 | API-16 | FN-10 | — |
| AC-10 | API-17 | FN-11 | — |
| AC-11 | API-13 | FN-08 | — |
| AC-13 | API-19 | FN-15, FN-20 | ENG-GRADE |
| AC-14 | API-06 | FN-14 | — |
| AC-16 | (all mutation) | FN-16 | — |
| AC-17 | API-06/07 | FN-17 | — |
| AC-18 | API-14 | FN-09 | — |
| AC-19 | (all mutation) | FN-18 | — |

> ทุก Function/Engine ใน 03_LOGIC ถูก trace ≥1 AC ✅.

---

## §6.9 Cross-Module Test Cases ⭐ (จาก BRD §12.1)

| ID | Scenario | Downstream | Expected |
|---|---|---|---|
| XT-01 | publish + "ส่งเรื่องปรับตำแหน่ง/เงินเดือน" | Movement (F-HR-MOVE) | emit `perf.result.movement_requested` payload {appraisal_id, employee_ref, decision, weighted_score}; ไม่ CRUD ปลายทาง |
| XT-02 | published + gap + "ส่งไปอบรม" | Training | emit `perf.gap.training_requested` {gap}; ไม่สร้างหลักสูตร |
| XT-03 | decision ผ่าน/top + "ส่งเข้า Succession" | Succession (F134) | emit `perf.result.succession_candidate` |
| XT-04 | publish per-person | ENG-CSQ 7C | `perf.result.published` (SecC/DC) ยิง per-person |
| XT-05 | **re-open → re-publish** | Movement + CSQ | ผลเดิมไม่ลบ (audit); re-publish → movement event ใหม่ (ปลายทางยกเลิก/ส่งใหม่) + CSQ ยิงซ้ำ per-person |

---

## §6.10 Microcopy-Aware Expected Text ⭐ (verbatim จากจอ — performance.html)

> ยึดข้อความจริงบนจอก่อนเสมอ (ai-testcase-md-generator จะ match 1:1).

| Action | Expected (verbatim) |
|---|---|
| create cycle success | สร้างรอบ · เปิดกรอก · แจ้งเตือนผู้เข้าร่วมแล้ว |
| create cycle validate | กรุณาเลือกรอบจากตั้งค่า HR |
| saveKpi success | บันทึกเป้า/KPI แล้ว · เปิดให้พนักงานประเมินตนเอง |
| saveKpi weight | น้ำหนัก KPI รวมต้องเท่ากับ 100% (ตอนนี้ N%) |
| saveSelf success | บันทึกประเมินตนเองแล้ว · ส่งต่อหัวหน้าประเมิน |
| saveMgr success | บันทึกผลหัวหน้าแล้ว · ส่งเข้าสอบทาน (DOA) |
| calibration send | ส่งสอบทานแล้ว · รอผู้สอบทานขั้นที่ 1 บันทึกผล |
| calibration stage (non-last) | บันทึกผลสอบทานขั้น N แล้ว · รอผู้สอบทานขั้นถัดไป |
| calibration publish | เผยแพร่ผล · บันทึกผลเข้า 7C · RESTRICTED · แจ้งเตือนพนักงานแล้ว |
| slot empty | กรุณาเลือกผู้สอบทานให้ครบทุกขั้น |
| close cycle | ปิดรอบแล้ว · ล็อกการแก้ไข (soft archive) |
| closed guard | รอบนี้ปิดแล้ว — แก้ไขไม่ได้ |
| role guard | สิทธิ์ไม่พอ |
| PIP success | เปิดแผน PIP แล้ว |
| reopen success | เปิดแก้ไขผลแล้ว · ส่งกลับขั้นหัวหน้าประเมิน · บันทึกผู้แก้ไว้ในประวัติ |
| reopen reason | กรุณาระบุเหตุผล |
| sendMovement | ส่งเรื่องปรับเงินเดือน/เลื่อนตำแหน่งให้ระบบโยกย้าย (ไม่ปรับเอง) |
| sendSuccession | ส่งผลเข้า Succession Planning (ส่งต่อ ไม่แก้ที่นี่) |
| empty appr | ไม่พบแบบประเมินที่ค้นหา / ลองปรับคำค้นหรือล้างตัวกรอง |
| RESTRICTED (staff) | ข้อมูลนี้เป็นความลับ (RESTRICTED) — ดูได้เฉพาะแบบประเมินของตนเอง |
| RESTRICTED (mgr) | ข้อมูลนี้เป็นความลับ (RESTRICTED) — หัวหน้าดูได้เฉพาะแผนกของตน |
| closed read-only | รอบนี้ปิดแล้ว — ดูได้อย่างเดียว แก้ไขไม่ได้ |
