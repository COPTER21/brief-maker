# CTX — F131: Performance (ประเมินผลงาน)

> **derived from:** FRD_F-HR-Performance v1.0 (2026-09-09) · **generated:** 2026-09-09
> **module:** HR (CUBE 4.0) · **feature code:** F-HR-PERF · **status:** active (FRD DRAFT · pending BA/Architect review of OQ register)
> ⚠ Derived artifact — source of truth คือ FRD Pack · ถ้า FRD revise ต้อง regen CTX

---

## 1. Summary

ระบบ **ประเมินผลงานพนักงานตามรอบ (cycle)** หน้าจอเดียว 4 tabs. HR สร้างรอบจาก **HR Configuration #107** (appraisal_cycle + config_version · ไม่ hardcode ฟอร์มกลาง) → ตั้งเป้า/KPI ต่อคน (Σweight=100) → พนักงานประเมินตนเอง → หัวหน้าประเมิน + คะแนนถ่วงน้ำหนัก → **สอบทาน (calibration) ผ่าน DOA แบบ staged** (เลือกผู้สอบทานจริงต่อขั้น) + decision → **เผยแพร่ผลรายคน (per-person · RESTRICTED)**. ผลที่เผยแพร่ยิง **CSQ 7C (SecC/DC)** และป้อนเป็น event/hook ไป 3 ปลายทาง (Movement=ปรับเงินเดือน/ตำแหน่ง · Training=gap · Succession=top performer) โดย**ไม่ CRUD ปลายทาง**. รองรับ re-open ผลหลังเผยแพร่ (authorized + reason + audit) · PIP (decision ทบทวน) · masking ตาม role (SELF/DEPT/ALL) · audit append-only. **ไม่ปรับเงินเดือน/สร้างหลักสูตร/สร้างรอบ-ฟอร์มกลางเอง** (out of scope · event/hook เท่านั้น).

## 2. Data Contract

> Source: FRD 04_DB (+ 05_RULES §5.2 state machine). เอาเฉพาะ entities/fields ที่ feature อื่น join/อ่าน + keys/status/score/decision/refs. Field UI ล้วน (seq/created_at ฯลฯ) ตัดออก. Owner ทุกตาราง = F131 เว้นที่ระบุ soft-ref.

### Entities
| Entity | PK | Key Fields | หมายเหตุ |
|---|---|---|---|
| T_perf_cycle | id (uuid · UI CY-xxx) | tenant_id, name, year_be, period_start/end, config_ref (FK-lookup #107 · snapshot), config_version, scope_target (org/dept), due, status, closed_at, version | รอบประเมิน (header) · config snapshot จาก HR Config #107 ไม่ hardcode (BR-01) · UNIQUE(tenant, config_ref, config_version, year_be) |
| T_perf_appraisal | id (uuid · UI A-xxx) | tenant_id, cycle_id (FK), employee_ref (FK-ref soft), emp_name/pos/dept_snap (Confidential+PII · snapshot BR-10), status, self_note/mgr_note (Restricted), decision (Restricted·DC), gap (Restricted), pip_duration/pip_plan, due, weighted_score (Restricted·computed), version | แบบประเมิน 1 คน × 1 รอบ · UNIQUE(tenant, cycle_id, employee_ref) · emp_dept_snap ใช้ scope DEPT (BR-11) · weighted_score 1–5 |
| T_perf_kpi_line | id (uuid) | tenant_id, appraisal_id (FK cascade), seq, title (Confidential), weight (Σ=100 · BR-02), target (Confidential), self_score (Restricted 1–5), mgr_score (Restricted 1–5) | KPI ต่อ appraisal · CASCADE on appraisal delete |
| T_perf_calibration_stage | id (uuid) | tenant_id, appraisal_id (FK cascade), stage_no, role_slot, reviewer_ref (Confidential+PII · resolve ENG-DOA), reviewer_name_snap, stage_status, acted_at, actor_ref | ขั้นสอบทาน DOA (staged · ไม่ hardcode LK-1) · UNIQUE(appraisal_id, stage_no) · re-open → rows ถูก DELETE/reset (ประวัติคงใน audit) |
| T_perf_audit | id (uuid) | tenant_id, appraisal_id (FK), act, who (Confidential+PII), who_ref, at | append-only · **NO UPDATE/DELETE** (trigger RAISE · BR-09/BR-12) · newest-first |
| hr_config.appraisal_cycle | (existing #107) | config_ref, config_version | soft-ref read-only (owner F-HR-CONFIG · ยังไม่ build) |
| T_employee | (existing) | — | soft-ref snapshot emp/pos/dept (owner Employee Master · read-only, no FK cascade) |

> **ไม่มี** T_perf_balance/running-number — feature นี้ archetype master+cycle (ไม่ใช่ Pattern Q document · ไม่มีเลขรัน/PDF · LD-08).

### Enums / States (ครบทุกค่า — ห้าม compress)
| Field | Values | Transition owner |
|---|---|---|
| cycle.status | `draft` → `open` → `in_review` → `calibration` → `closed`(terminal) | feature นี้ (closed = terminal lock ทุก mutation ในรอบ · FIX-05) |
| appraisal.status | `goal` → `self` → `mgr` → `calibration` → `published`; branch: `published`→`mgr` (re-open) · `published`→`published` (PIP) | feature นี้ (5 states per-person) |
| appraisal.decision | `ผ่าน` · `ทบทวน (PIP)` · `ไม่ผ่าน` (terminal · บันทึกขั้นสุดท้าย calibration · Restricted·DC) | feature นี้ |
| calibration.stage_status | `pending` · `current` · `done` (staged one-step advance) | feature นี้ (ENG-DOA resolve reviewer per role_slot) |
| cycle.scope_target | `org` · `dept` | feature นี้ |
| scope_type (SEC · การเห็น) | `SELF` (staff · employee_ref=self) · `DEPT` (mgr · emp_dept_snap=requester.dept) · `ALL` (HR/manage) | Policy Center (CONFIGURABLE · BR-11) |
| kpi_line.self_score / mgr_score | integer `1`–`5` (Restricted · SecC) | feature นี้ |
| weighted_score | numeric(4,2) `1.00`–`5.00` (computed Σ(mgr_score×weight)/Σweight · ไม่ user input · BR-04) | feature นี้ (FN-19) |
| audit.act (ตัวอย่าง) | create/แก้/ตั้งเป้า KPI · ประเมินตนเอง · หัวหน้าประเมิน · สอบทานขั้น N · เผยแพร่ผล · เปิดแก้ไขผลหลังเผยแพร่ · บันทึกผลประเมินเข้า 7C · เปิดแผน PIP | feature นี้ (append-only) |

### State transitions — appraisal (ครบทุกเส้น · guard cascade: closed → role → stage → validate)
| From | To | Action | Allowed roles | Condition / effect |
|---|---|---|---|---|
| goal | self | saveKpi | manage (HR) | open cycle · goal · Σweight=100 · titles ครบ (VR-01/09) |
| self | mgr | saveSelf | staff (own) | open cycle · self · self_score 1–5 ครบ |
| mgr | calibration | saveMgr | mgr∥manage | open cycle · mgr · mgr_score 1–5 ครบ → คำนวณ weighted_score |
| calibration | calibration | doCalibSend (freeze) | manage | open cycle · calibration · weighted_score≠null (FIX-01) · slots ครบ → INSERT stages (stage1=current) · **คง calibration ยังไม่ publish** |
| calibration | calibration | doCalibStage (non-last) | manage (reviewer ขั้น current) | open cycle · current stage → stage.done + เลื่อนขั้นถัดไป=current |
| calibration | published | doCalibStage (last) | manage (reviewer ขั้นสุดท้าย) | ทุก stage=done + decision → **CSQ perf.result.published + NOTIFY + (ถ้า ทบทวน → gap default)** |
| published | mgr | doReopen | manage (authorized) | open cycle · reason non-empty · เคลียร์ decision + DELETE stages · **คงคะแนน/gap** · append-only audit → re-publish = DOA/CSQ ยิงซ้ำ per-person (BR-12) |
| published | published | doPip | manage | decision "ทบทวน" · gap non-empty → เปิดแผน PIP (30/60/90) |

### Relationships
- hr_config.appraisal_cycle (#107) —(read/snapshot: config_ref + config_version)→ T_perf_cycle
- T_perf_cycle (1) —< (N) T_perf_appraisal
- T_perf_appraisal (1) —< (N) T_perf_kpi_line / T_perf_calibration_stage (**ON DELETE CASCADE**) / T_perf_audit (append-only · no cascade delete)
- T_employee (1) —(snapshot: emp_*_snap + employee_ref · **no FK cascade** · BR-10)→ T_perf_appraisal
- **Masters read (soft-ref · read-only · snapshot):** HR Configuration #107 (appraisal_cycle · config_version · ปีสิทธิ์รอบ) · Employee Master (emp/pos/dept)

## 3. API Surface

> Base path: `/api/v1/performance`. ทุก endpoint: `X-Tenant-Id` + JWT (RLS · role source = server mirror `sec.can()`). Mutations รับ `Idempotency-Key` (cache 24h · FN-92) + optimistic `version` (mismatch=409 ERR_STALE_DATA). ทุก read ผ่าน FN-17 applyScopeAndMask **ก่อน** ส่ง response (out-of-scope rows/columns ไม่อยู่ใน payload · ไม่ใช่แค่ UI hide). Source: FRD 02_API.

| Method | Endpoint | ทำอะไร | Auth / stage |
|---|---|---|---|
| GET | /cycles · /cycles/:id | list / detail + per-person status | required |
| POST | /cycles | สร้างรอบจาก HR Config (snapshot config_version) | manage (HR) |
| POST | /cycles/:id/close | ปิดรอบ (terminal · lock ทุก mutation ในรอบ) | manage |
| GET | /config/appraisal-cycles | lookup รอบจาก HR Config #107 (soft-ref proxy · read-only) | manage |
| GET | /appraisals · /appraisals/:id | list+filter (`cycle_id`,`status`,`q`) / detail — **scoped+masked** | required (own scope) |
| PUT | /appraisals/:id/kpis | ตั้งเป้า/KPI Σ=100 (goal→self) | manage · goal stage |
| POST | /appraisals/:id/self | ประเมินตนเอง (self→mgr) | staff (own) · self stage |
| POST | /appraisals/:id/manager-review | หัวหน้าประเมิน + weighted (mgr→calibration) | mgr∥manage · mgr stage |
| POST | /appraisals/:id/calibration/send | ส่งสอบทาน — freeze reviewers staged (คง calibration) | manage · calibration |
| POST | /appraisals/:id/calibration/stage | บันทึกผลรายขั้น / publish บนขั้นสุดท้าย + decision | manage (reviewer ขั้น current) |
| POST | /appraisals/:id/pip | เปิดแผน PIP | manage · published + decision ทบทวน |
| POST | /appraisals/:id/reopen | เปิดแก้ไขผลหลังเผยแพร่ (reason บังคับ) | manage · published + open cycle |
| POST | /appraisals/:id/reminder | ส่งการเตือน overdue | manage |
| POST | /appraisals/:id/dispatch/training | gap → Training hook | manage · published |
| POST | /appraisals/:id/dispatch/movement | ผล → Movement event | manage · published |
| POST | /appraisals/:id/dispatch/succession | ผล → Succession hook | manage · published |
| GET | /reports/distribution | รายงานการกระจายคะแนน (buckets · scoped aggregate) | required (scoped) |

**Masters read (external · consumed, ไม่ owned):**
- GET /config/appraisal-cycles — HR Config #107 (config_ref + config_version · **502 ERR_CONFIG_UPSTREAM_DOWN** ถ้ายังไม่ build · EC-06)
- (snapshot) Employee Master — emp/pos/dept (soft-ref · no FK cascade)
- (engine) ENG-DOA resolve reviewer per role_slot ณ calibration/send (role-id chain = **OQ-PERF-05 · CL-0013**)

### Events emitted
| Event | ท่อ/Engine | Trigger point | Payload key |
|---|---|---|---|
| `perf.result.published` (7C) | CSQ · **SecC + DC เท่านั้น** (LK-6) | calibration/stage isLast (calibration→published) · **per-person** · รวม re-publish | `{ appraisal_id, employee_ref, classification:'SecC', decision:'DC' }` |
| `perf.result.published` (notify) | NTF (ENG-NOTIFY) | เผยแพร่ผลรายคน (จุดเดียวกับ CSQ · คนละ engine) | `{ ref:appraisal_id, employee_ref, cycle }` |
| `perf.cycle.opened` | NTF | createCycleFromConfig (cycle draft→open · API-02) | `{ ref:cycle_id, cycle }` → พนักงาน+หัวหน้าในรอบ |
| `perf.deadline.overdue` | NTF | sendReminder · isOverdue (status≠published && due<today · API-15/EC-09) | `{ ref:appraisal_id/cycle_id, cycle, date }` |
| `perf.result.movement_requested` | Cross-module event → Movement (F-HR-MOVE) | dispatch/movement (published · ทุกผล · decouple จาก gap) | `{ appraisal_id, employee_ref, decision, weighted_score, cycle_id }` |
| `perf.gap.training_requested` | Cross-module hook → Training | dispatch/training (published + gap≠null) | `{ appraisal_id, employee_ref, gap }` |
| `perf.result.succession_candidate` | Cross-module hook → Succession (F134) | dispatch/succession (decision ผ่าน หรือ weighted_score≥4) | `{ appraisal_id, employee_ref, weighted_score }` |

> DOA events (`doa_pending`/`doa_result`) = จาก ENG-DOA อัตโนมัติ (staged calibration) — **feature ห้ามประกาศซ้ำ**. re-open **ไม่มี event แยก** (S-05 ครอบ re-publish · CSQ+NOTIFY ยิงซ้ำ per-person).

## 4. Shared Rules (cross-boundary เท่านั้น)

> Source: FRD 05_RULES. เอาเฉพาะ rule ที่ module/feature อื่นต้อง conform หรือถูกกระทบ. Rule ภายใน (form validation VR-01..10, UI behavior) ตัดออก.

| Rule ID | Rule | กระทบใคร |
|---|---|---|
| BR-08 / BR-11 (D-CLASS) | ผลประเมิน (score/decision/gap/notes/weighted_score) = **RESTRICTED (SecC)** · masking + row-scope ตาม role: **staff=SELF · mgr=DEPT (emp_dept_snap=requester.dept) · HR(manage)=ALL** · out-of-scope **ไม่อยู่ใน payload/DOM** (enforce backend ที่ FN-17 · ไม่ใช่แค่ UI hide) | Policy Center (Data Classification · Restricted Resources · OQ-PERF-10 OPEN), all consumers, report/dashboard |
| BR-13 / LK-6 | ยิง CSQ `perf.result.published` **per-person publish** · ท่อ **SecC + DC เท่านั้น** — ไม่ประกาศ OC/DC-doc/SC/AC/FC (สงวนของ engine · DC = decision เชิงผล ไม่ใช่ doc signature) | ENG-CSQ (7C) · Architect (EC valuation = OQ-PERF-06) |
| BR-07 / LK-2 | ผล → ปรับเงินเดือน/ตำแหน่ง = **event ให้ Movement** — feature **ไม่ CRUD** เงินเดือน/ตำแหน่ง · ส่งได้ทุกผล published (decouple จาก gap) | Movement (F-HR-MOVE) |
| BR-06 / LK-5 | gap → Training = **hook display-only** — feature **ไม่สร้างหลักสูตร** · gap ต้องมีค่า (BR_GAP_REQUIRED) | Training |
| BR-12 (re-open) | re-open published = authorized (manage) + open cycle + reason บังคับ + **append-only audit** (ผลเดิมไม่ลบ) · ส่งกลับขั้น mgr · เคลียร์ decision+stages · **คงคะแนน/gap** · re-publish → **CSQ/NOTIFY/staged DOA ยิงซ้ำ per-person** | Movement/Training/Succession (ต้อง re-evaluate/ยกเลิกของเดิม · ปลายทางจัดการ), CSQ, audit |
| BR-01 / LK-3 | รอบ/แบบ/เกณฑ์ดึงจาก **HR Config #107** (appraisal_cycle + config_version · snapshot) — **ไม่ hardcode** · config หาย/down = block ก่อนสร้างรอบ (ไม่สร้าง cycle เปล่า · EC-06) | HR Configuration #107 (F-HR-CONFIG) |
| BR-05 / LK-1 | สอบทานผ่าน **DOA แบบ staged** (เลือกผู้สอบทานจริงต่อขั้น · slot ว่าง ไม่ preset) + decision ก่อน published · publish หลังขั้นสุดท้ายเท่านั้น · **ห้าม hardcode chain** (resolve ตอน send แล้ว freeze snapshot) | DOA (ENG-DOA · F-DLG-001) |
| BR-10 | snapshot emp_name/pos/dept ณ สร้าง appraisal (ไม่ live-join) · dept snapshot ใช้ scope · **soft-ref ไม่มี FK cascade** — Employee/HR Config เปลี่ยน/ลบ ไม่ย้อนกระทบใบเดิม | Employee Master, HR Config #107 |
| BR-09 | audit append-only ทุก create/แก้/สอบทาน (who+at+act) · **no update/delete** (trigger) · ปิดรอบ = terminal lock ทุก mutation | audit/finance, DBA |
| SoD (§0.4) | Maker (หัวหน้าประเมิน · saveMgr) ≠ Approver (ผู้สอบทานขั้นสุดท้าย) — บังคับด้วย guard cascade (คะแนน mgr ครบ + ทุกขั้น done ก่อน published) | ผู้อนุมัติ, governance (Strike) |

**Permission capabilities (backend-enforced · sec.can 2 ชั้น function+UI · FIX-03):** — anyone enforcing/consuming must honor
- `saveMgr` = mgr ∥ manage (หัวหน้าประเมิน · mgr stage เฉพาะแผนกตน)
- `saveSelf` = staff (own only · self stage)
- create/close cycle · saveKpi · calibration(send/stage) · PIP · reopen · dispatch hooks · reminder = **manage (HR) เท่านั้น**
- เห็นผล/decision/gap ผู้อื่น: staff=❌ (mask + ไม่อยู่ DOM) · mgr=เฉพาะ DEPT · manage=ALL

## 5. Integration

- **Depends on (upstream · soft-ref/engine read-only):**
  - HR Configuration #107 (F-HR-CONFIG) — appraisal_cycle + KPI/form template + config_version (resolve ตอนสร้างรอบ · ⚠️ ยังไม่ build · freeze payload contract 02_API §2.X)
  - Employee Master — emp/pos/dept snapshot (soft-ref · no FK cascade)
  - ENG-DOA (F-DLG-001) — staged calibration slot resolve (role-id chain = OQ-PERF-05 · CL-0013)
  - ENG-NOTIFY (F-NOTIFY) — 3 business events
  - ENG-CSQ (7C) — EC valuation รอ Architect (OQ-PERF-06)
- **Depended by (downstream · Value Stream HR/Talent):**
  - Movement (F-HR-MOVE) — `perf.result.movement_requested` event (ปรับเงินเดือน/ตำแหน่ง · ⚠️ soft-ref)
  - Training — `perf.gap.training_requested` hook (gap payload · ⚠️ soft-ref)
  - Succession (F134) — `perf.result.succession_candidate` hook (top performer · ba-done soft-ref)
  - ENG-CSQ (7C) — `perf.result.published` (SecC/DC) per-person publish
  - ENG-NOTIFY — 3 business events (รอบเปิด / ครบกำหนด / ผลเผยแพร่)
- **Declarations (รอบนี้ 2026-09-09 · doa + ntf + csq):**
  - **DOA** [yes] — scope `policy_approve` (สอบทานผลประเมิน · ไม่ใช่ document_sign · ไม่ออก PDF/ลายเซ็น). **❌ ไม่มีวงเงิน** → 1 ชุด `amount_from:0 · amount_to:null` · chainMode `sequential` **staged 2 ขั้น** (stage1 "หัวหน้าสายงาน" → stage2 "ผู้สอบทาน HRBP/ผู้บริหาร") · departments=merged · **no amount tier · no exec path**. slot ว่าง (resolve+freeze ณ send). role-id ทั้ง 2 ขั้น = **[OQ-PERF-05]** (CL-0013 · BA เคาะที่ DOA กลาง · LEAVE AS OQ)
  - **NTF** [yes] — กลุ่มใหม่ "ประเมินผลงาน (Performance)" · 3 events: `perf.cycle.opened` · `perf.deadline.overdue` · `perf.result.published`. DOA events (doa_pending/doa_result) + dispatch cross-module events **ไม่ประกาศซ้ำ**. re-open ไม่มี event แยก
  - **CSQ** [yes] — ท่อ **SecC + DC** (per-person `perf.result.published`) · ไม่ประกาศ OC/DC-doc/SC/AC/FC. EC valuation = **[OQ-PERF-06]** (Architect)
  - **DOCCFG / PDFDOC** [no] — NOT-NEEDED (archetype master+cycle · ไม่มีเลขรัน/เอกสารพิมพ์ A4/ลายเซ็น · LD-08)
- **Engine hooks:** ENG-DOA (F-DLG-001) · ENG-CSQ (7C · SecC/DC) · ENG-NOTIFY (F-NOTIFY) — external, existing · ENG-GRADE (grade-mapper) — **owned candidate [NEW]** register CUBIC ตอน hand-off (distribution buckets · API-19)
- **Open dependencies (blocking / [not documented] contract):**
  - `[OQ-PERF-05]` DOA chain executive role-ids (CL-0013) — feature ประกาศ slot เท่านั้น · role-id = `[not documented]` (BA เคาะที่ config · deadline ก่อน Phase 3)
  - `[OQ-PERF-06]` CSQ EC valuation ของ perf.result.published + ท่อ 7C detail (Architect · trigger locked · valuation deferred Phase 4)
  - `[OQ-PERF-07]` soft-ref ปลายทางยังไม่ build (HR Config #107 · F-HR-MOVE · Employee Master · Succession F134) — payload frozen ที่ 02_API §2.X
  - `[OQ-PERF-09]` concurrent staged review lock — optimistic first-write-wins 409 `[AI-DEFAULT]` (Architect confirm)
  - `[OQ-PERF-10]` Restricted fields wire กับ Restricted Resources registry (Policy Center) — OPEN
  - `[OQ-PERF-08]` 360 feedback / competency model / continuous check-in = out of scope (Strike · wave ถัดไปหรือถาวรตัด)

---
*trace: §2 ← FRD 04_DB (+ 05_RULES §5.2 state machine) · §3 ← FRD 02_API · §4 ← FRD 05_RULES · §5 ← BRD §12.1/§13 + DOA/NTF/CSQ briefs + 00_OVERVIEW §0.5/§0.8*
