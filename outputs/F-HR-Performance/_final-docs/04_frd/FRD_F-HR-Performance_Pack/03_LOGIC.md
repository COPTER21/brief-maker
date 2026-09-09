# 03_LOGIC — F131 Performance / ประเมินผลงาน

> **Audience:** BE dev (business logic layer)
> **Scope:** All non-HTTP logic — state transitions, guards, calculations, scope/mask, integrations
> **Iron Rule R8:** ทุก mutation API ต้อง trace ไปที่ ≥1 Function/Engine ใน §3.3
> **Naming:** Function = camelCase · Engine = kebab-case

---

## §3.1 Functions (Scope-Local)

### F131-FN-01: `createCycleFromConfig`
- **Purpose:** สร้าง Cycle จาก HR Config #107 (BR-01) — snapshot config_version, ไม่ hardcode รอบ/แบบ.
- **Input:** `{ config_ref, scope_target, due }`
- **Output:** `Cycle | ValidationError[]`
- **Invoked by:** F131-API-02
- **Calls:** ENG-NOTIFY (emit `perf.cycle.opened`) · FN-16
- **Side effects:** INSERT T_perf_cycle (status='open', config_version snapshot); notify
- **Error cases:** BR_CONFIG_CYCLE_NOT_FOUND (EC-06)
- **Iron rule check:** ✅ no HTTP terms

### F131-FN-02: `closeCycle`
- **Purpose:** ปิดรอบ → terminal lock (FIX-05). หลังปิด guard cascade layer 1 block ทุก mutation ในรอบ.
- **Input:** `{ cycle_id, version }`
- **Output:** `Cycle | Error`
- **Invoked by:** F131-API-04
- **Calls:** FN-16
- **Side effects:** UPDATE cycle.status='closed', closed_at; audit
- **Error cases:** ERR_STALE_DATA, ERR_INSUFFICIENT_ROLE
- **Iron rule check:** ✅

### F131-FN-03: `saveKpiGoals`
- **Purpose:** บันทึกเป้า/KPI (BR-02 Σweight=100). โปรโตไทป์: `saveKpi` — validate ทุก title + Σ=100.
- **Input:** `{ appraisal_id, kpis:[{title,weight,target}] }`
- **Output:** `Appraisal | ValidationError[]`
- **Invoked by:** F131-API-08
- **Calls:** FN-18 guardMutation(closed→role(manage)→stage('goal')) · FN-16
- **Side effects:** REPLACE T_perf_kpi_line; status goal→self; audit "ตั้งเป้า/KPI"
- **Error cases:** BR_KPI_WEIGHT_NOT_100 (VR-01), BR_KPI_TITLE_REQUIRED, ERR_STAGE_INVALID, BR_CYCLE_CLOSED
- **Iron rule check:** ✅

### F131-FN-04: `recordSelfAssessment`
- **Purpose:** พนักงานประเมินตนเอง (FN-03 · BR-03 self ก่อน mgr). โปรโตไทป์: `saveSelf`.
- **Input:** `{ appraisal_id, scores:[{kpi_id,self_score}], self_note }`
- **Output:** `Appraisal | ValidationError[]`
- **Invoked by:** F131-API-09
- **Calls:** FN-18 guardMutation(closed→role(own staff)→stage('self')) · FN-16
- **Side effects:** UPDATE kpi_line.self_score + self_note; status self→mgr; audit "พนักงานประเมินตนเอง"
- **Error cases:** BR_SELF_SCORE_INCOMPLETE (1–5), ERR_STAGE_INVALID, BR_CYCLE_CLOSED
- **Iron rule check:** ✅

### F131-FN-05: `recordManagerReview`
- **Purpose:** หัวหน้าประเมิน + คำนวณ weighted score (FN-04 · BR-04). โปรโตไทป์: `saveMgr`.
- **Input:** `{ appraisal_id, scores:[{kpi_id,mgr_score}], mgr_note }`
- **Output:** `Appraisal`
- **Invoked by:** F131-API-10
- **Calls:** FN-19 computeWeightedScore · FN-18 guardMutation(closed→role(mgr∥manage)→stage('mgr')) · FN-16
- **Side effects:** UPDATE mgr_score + mgr_note + weighted_score; status mgr→calibration; audit "หัวหน้าประเมิน + คะแนน"
- **Error cases:** BR_MGR_SCORE_INCOMPLETE, ERR_STAGE_INVALID, ERR_INSUFFICIENT_ROLE, BR_CYCLE_CLOSED
- **Iron rule check:** ✅

### F131-FN-06: `sendCalibration`
- **Purpose:** ส่งสอบทาน — freeze ผู้สอบทาน staged (FN-08 · LK-1 · FIX-06). status **คง calibration** (ยังไม่ publish). Precondition `weighted_score != null` (FIX-01).
- **Input:** `{ appraisal_id, reviewers:[{stage_no,role_slot,reviewer_ref}] }`
- **Output:** `{ approvals:[...] } | Error`
- **Invoked by:** F131-API-11
- **Calls:** ENG-DOA (resolve reviewer per role_slot) · FN-18 guardMutation(closed→role(manage)→stage('calibration')) · FN-16
- **Side effects:** INSERT T_perf_calibration_stage (stage1='current', rest 'pending'); audit "ส่งสอบทาน · เลือกผู้สอบทาน 2 ขั้น (คง calibration)"
- **Error cases:** BR_REVIEWER_SLOT_EMPTY (VR-02), BR_MGR_SCORE_INCOMPLETE (FIX-01), ERR_STAGE_INVALID, BR_CYCLE_CLOSED
- **Iron rule check:** ✅

### F131-FN-07: `recordCalibrationStage`
- **Purpose:** ผู้สอบทานขั้น current บันทึกผล (stamp at/actor); ขั้นสุดท้าย → publish + decision + CSQ 7C + notify (FN-05 · FIX-06/07). โปรโตไทป์: `doCalibStage`.
- **Input:** `{ appraisal_id, decision? }` (decision เฉพาะขั้นสุดท้าย)
- **Output:** `{ stage_status } | { status:'published', decision }`
- **Invoked by:** F131-API-12
- **Calls (non-last):** FN-16 · FN-18(closed→role(manage)→stage('calibration'))
- **Calls (last):** ENG-CSQ (emit `perf.result.published` per-person · SecC/DC) · ENG-NOTIFY (emit `perf.result.published`) · FN-16
- **Side effects (non-last):** UPDATE stage.status='done'+acted_at+actor_ref; advance next='current'; audit "สอบทานขั้น N"
- **Side effects (last):** UPDATE status='published'+decision; ถ้า "ทบทวน"→gap default; audit "เผยแพร่ผล · decision:X" + "บันทึกผลประเมินเข้า 7C"; CSQ + notify
- **Error cases:** ERR_NO_CURRENT_STAGE, ERR_STAGE_INVALID, ERR_INSUFFICIENT_ROLE, BR_CYCLE_CLOSED
- **Iron rule check:** ✅ (CSQ/notify ผ่าน engine call, ไม่มี HTTP term)

### F131-FN-08: `openPip`
- **Purpose:** เปิดแผน PIP (FN-10) เมื่อ decision "ทบทวน". โปรโตไทป์: `doPip`.
- **Input:** `{ appraisal_id, gap, duration, plan }`
- **Output:** `Appraisal | ValidationError`
- **Invoked by:** F131-API-13
- **Calls:** FN-18(closed→role(manage)) · FN-16
- **Side effects:** UPDATE gap + pip_duration + pip_plan; audit "เปิดแผน PIP · {duration}"
- **Error cases:** BR_GAP_REQUIRED, ERR_INSUFFICIENT_ROLE, BR_CYCLE_CLOSED
- **Iron rule check:** ✅

### F131-FN-09: `reopenPublished`
- **Purpose:** เปิดแก้ไขผลหลังเผยแพร่ (OQ-PERF-01 · BR-12) — authorized manage + open cycle + reason บังคับ + append-only audit. ส่งกลับขั้น mgr, เคลียร์ decision+stages, **คงคะแนน/gap**. โปรโตไทป์: `doReopen`.
- **Input:** `{ appraisal_id, reason }`
- **Output:** `Appraisal | Error`
- **Invoked by:** F131-API-14
- **Calls:** FN-18(closed→role(manage)→stage('published')) · FN-16
- **Side effects:** append audit "เปิดแก้ไขผลหลังเผยแพร่ · เหตุผล:{reason}" (who+at); DELETE calibration_stage; UPDATE status='mgr', decision=null
- **Error cases:** BR_REASON_REQUIRED (VR-03), ERR_STAGE_INVALID (published only), BR_CYCLE_CLOSED
- **Note:** re-publish → flow เดิม · staged DOA ซ้ำ · CSQ ยิงซ้ำ per-person
- **Iron rule check:** ✅

### F131-FN-10: `dispatchTraining` · F131-FN-11: `dispatchMovement` · F131-FN-12: `dispatchSuccession`
- **Purpose:** integration — ส่งต่อผลเป็น event/hook (matrix #8, display-only, ไม่ CRUD ปลายทาง · LK-2/LK-5 · FIX-09).
- **Input:** `{ appraisal_id }`
- **Output:** `{ dispatched:true, event }`
- **Invoked by:** F131-API-16 / API-17 / API-18
- **Calls:** FN-18(closed→role(manage)) · emit event (fire-and-forget)
- **Side effects:** emit `perf.gap.training_requested` / `perf.result.movement_requested` / `perf.result.succession_candidate` (payload → 02_API §2.X). **ไม่มี write ปลายทาง.**
- **Error cases:** BR_GAP_REQUIRED (training), ERR_INSUFFICIENT_ROLE, BR_CYCLE_CLOSED
- **Iron rule check:** ✅

### F131-FN-13: `sendReminder`
- **Purpose:** ส่งการเตือน overdue (FN-09). โปรโตไทป์: `sendReminder`.
- **Input:** `{ appraisal_id? }` · **Output:** `{ sent:true }` · **Invoked by:** F131-API-15
- **Calls:** ENG-NOTIFY (emit `perf.deadline.overdue`)
- **Side effects:** notify overdue assignees
- **Iron rule check:** ✅

### F131-FN-14: `buildAppraisalListQuery`
- **Purpose:** สร้าง query list/detail (FN-90) — คู่กับ FN-17 scope.
- **Input:** `{ cycle_id?, status?, q?, requester }` · **Output:** `Appraisal[]`
- **Invoked by:** F131-API-06 / API-07 / API-01 / API-03
- **Calls:** FN-17 applyScopeAndMask
- **Side effects:** — (read-only)
- **Iron rule check:** ✅

### F131-FN-15: `buildDistributionReport`
- **Purpose:** รายงานการกระจายคะแนน (FN-13) — stat tiles + buckets.
- **Input:** `{ cycle_id, requester }` · **Output:** `{ total, published, pip, buckets }`
- **Invoked by:** F131-API-19
- **Calls:** FN-20 bucketDistribution · ENG-GRADE (team-calib grade) · FN-17 (scope aggregate)
- **Side effects:** — (read-only)
- **Iron rule check:** ✅

### F131-FN-16: `pushAudit`
- **Purpose:** append-only audit (FN-93 · BR-09). โปรโตไทป์: `pushAudit` (unshift, stamp who+at).
- **Input:** `{ appraisal_id, act, who }` · **Output:** `void`
- **Invoked by:** ทุก mutation function (FN-01..FN-09)
- **Side effects:** INSERT T_perf_audit (immutable, newest-first)
- **Iron rule check:** ✅

### F131-FN-17: `applyScopeAndMask`  ⭐ (security core · FN-94)
- **Purpose:** บังคับ scope_type (SELF/DEPT/ALL) + RESTRICTED masking (BR-08/BR-11). โปรโตไทป์: `scopeSelf()` + `mask()`.
- **Input:** `{ list, requester }` · **Output:** `Appraisal[]` (out-of-scope rows removed; Restricted columns masked/excluded)
- **Logic:** staff(mask) → filter employee_ref=self · mgr → filter emp_dept_snap=requester.dept · manage → all. Restricted fields (score/decision/gap/notes) → excluded/`•••` ถ้า role ไม่ผ่าน. **out-of-scope ไม่อยู่ใน payload (ไม่ใช่แค่ UI hide).**
- **Invoked by:** FN-14, FN-15 (ทุก read path)
- **Iron rule check:** ✅ pure filter/transform

### F131-FN-18: `guardMutation`  ⭐ (guard cascade · FIX-01..06)
- **Purpose:** 4-guard cascade เรียงกัน — **closed-cycle → role(sec.can) → stage(status) → scope/validate**. ป้องกัน bypass ทุก mutation.
- **Input:** `{ appraisal, action, requiredStage, requester }` · **Output:** `void | GuardError`
- **Logic:** (1) `cycleClosed(a)` → BR_CYCLE_CLOSED (FIX-05); (2) `!sec.can(action)` → ERR_INSUFFICIENT_ROLE (FIX-03); (3) `a.status != requiredStage` → ERR_STAGE_INVALID (FIX-01/02); (4) scope/field validate.
- **Invoked by:** ทุก mutation function (FN-02..FN-12)
- **Iron rule check:** ✅
- **sec.can mapping (server mirror):** `saveMgr` → mgr∥manage; ทุก action อื่น (doCalib/doPip/doCloseCycle/reopen/send*) → manage only.

### F131-FN-19: `computeWeightedScore`
- **Purpose:** คะแนนรวมถ่วงน้ำหนัก (BR-04) = Σ(mgr_score×weight)/Σweight (เฉพาะ KPI ที่มี mgr_score). โปรโตไทป์: `rawScore()`/`wsum()`.
- **Input:** `{ kpis:[{weight,mgr_score}] }` · **Output:** `number | null`
- **Invoked by:** FN-05, FN-15 · **Iron rule check:** ✅ pure

### F131-FN-20: `bucketDistribution`
- **Purpose:** จัดกลุ่มคะแนนเป็น buckets (ต่ำ<3.0 / ปานกลาง 3.0–3.9 / ดี 4.0–4.5 / ดีเยี่ยม >4.5) สำหรับ report.
- **Input:** `{ appraisals[] }` · **Output:** `{ bucket:count }` · **Invoked by:** FN-15 · **Iron rule check:** ✅ pure

---

## §3.2 Engines (Reusable / CUBIC-Registered)

### ENG-DOA: `delegation-of-authority` [EXISTING]
| Field | Value |
|---|---|
| code | `delegation-of-authority` |
| name | Delegation of Authority (staged calibration slot resolve) |
| category | approval/workflow |
| status | **EXISTING** (F-DLG-001 · Policy Center) |
| owner | shared (central engine) |

**Input Schema:** `{ role_slot, context:{ appraisal_id, cycle_id, dept } }`
**Output Schema:** `{ resolved_reviewer_ref, role_id }`
**Logic Outline:** resolve ผู้สอบทานตามตำแหน่ง/สายอนุมัติที่ config ไว้ (ไม่ hardcode ในฟีเจอร์ · LK-1). Feature **ประกาศ slot** เท่านั้น.
**Used by:** F131 (calibration send) + features อื่นที่มีสายอนุมัติ
**Iron rule check:** ✅ pure resolve, no HTTP
**⚠️ OPEN (OQ-PERF-05 · CL-0013):** executive DOA chain role-ids รอ BA ระบุตอน config — **feature ไม่ hardcode**. ดู 03_DOA_BRIEF. **ไม่มีวงเงิน** (สอบทานผลประเมิน — ไม่ใช่ PR/PO).

### ENG-NOTIFY: `notification` [EXISTING]
| Field | Value |
|---|---|
| code | `notification` · name | Notification Center · category | notification |
| status | **EXISTING** (F-NOTIFY) · owner | shared |

**Input Schema:** `{ event, payload, audience }`
**Output Schema:** `{ dispatched:true }`
**Events (business, feature-declared):** `perf.cycle.opened` · `perf.deadline.overdue` · `perf.result.published`.
> **แยกจาก doa_pending/doa_result** — มาจาก ENG-DOA อัตโนมัติ (ห้ามประกาศซ้ำ). ดู 03_NTF_BRIEF.
**Used by:** F131 + ทุก feature ที่มี event · **Iron rule check:** ✅

### ENG-CSQ: `compliance-sensitive-queue` (7C) [EXISTING]
| Field | Value |
|---|---|
| code | `compliance-sensitive-queue` · name | CSQ 7C · category | compliance |
| status | **EXISTING** · owner | shared |

**Input Schema:** `{ event:'perf.result.published', payload:{ appraisal_id, employee_ref, classification:'SecC', decision:'DC' } }`
**Output Schema:** `{ queued:true }`
**Logic Outline:** hook per-person publish → เข้าคิว 7C (SecC masking + DC decision). **ไม่ประกาศ OC/DC-doc/SC** (สงวนของ engine · LK-6).
**Trigger (OQ-PERF-02 RESOLVED):** per-person publish (F131-API-12 isLast) + re-publish (ยิงซ้ำ).
**Used by:** F131 + features ที่มีข้อมูล sensitive · **Iron rule check:** ✅
**⚠️ OPEN (OQ-PERF-06):** **EC valuation** (มูลค่า EC + ท่อ 7C detail) รอ Architect. ดู 03_CSQ_BRIEF.

### ENG-GRADE: `performance-grade-mapper` [DRAFT — owned candidate]
| Field | Value |
|---|---|
| code | `performance-grade-mapper` · name | Performance Grade Mapper · category | calculation |
| status | **DRAFT** (register CUBIC Phase 2 · LD-06) · owner | F131 (this) |

**Input Schema:** `{ weighted_score:number }`
**Output Schema:** `{ grade:'A'|'B'|'C'|'D' }`
**Logic Outline:** >4.5→A · ≥4→B · ≥3→C · else→D (โปรโตไทป์ `gradeOf()`). ใช้ใน team-calibration + distribution.
**Used by:** F131 (team calib + report) · candidate reuse (Succession/Movement grading)
**Iron rule check:** ✅ pure · **CUBIC note:** DRAFT → register ตอนยืนยัน reuse (Phase 2).

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor · MANDATORY)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| API-01 | GET | /cycles | FN-14 | — |
| API-02 | POST | /cycles | FN-01, FN-16 | ENG-NOTIFY |
| API-03 | GET | /cycles/:id | FN-14 | — |
| API-04 | POST | /cycles/:id/close | FN-02, FN-16 | — |
| API-05 | GET | /config/appraisal-cycles | — (proxy) | — |
| API-06 | GET | /appraisals | FN-14, FN-17 | — |
| API-07 | GET | /appraisals/:id | FN-14, FN-17 | — |
| API-08 | PUT | /appraisals/:id/kpis | FN-03, FN-18, FN-16 | — |
| API-09 | POST | /appraisals/:id/self | FN-04, FN-18, FN-16 | — |
| API-10 | POST | /appraisals/:id/manager-review | FN-05, FN-19, FN-18, FN-16 | — |
| API-11 | POST | /appraisals/:id/calibration/send | FN-06, FN-18, FN-16 | ENG-DOA |
| API-12 | POST | /appraisals/:id/calibration/stage | FN-07, FN-18, FN-16 | ENG-CSQ, ENG-NOTIFY |
| API-13 | POST | /appraisals/:id/pip | FN-08, FN-18, FN-16 | — |
| API-14 | POST | /appraisals/:id/reopen | FN-09, FN-18, FN-16 | — |
| API-15 | POST | /appraisals/:id/reminder | FN-13 | ENG-NOTIFY |
| API-16 | POST | /appraisals/:id/dispatch/training | FN-10, FN-18 | — (event) |
| API-17 | POST | /appraisals/:id/dispatch/movement | FN-11, FN-18 | — (event) |
| API-18 | POST | /appraisals/:id/dispatch/succession | FN-12, FN-18 | — (event) |
| API-19 | GET | /reports/distribution | FN-15, FN-20, FN-17 | ENG-GRADE |

### Trace Verification (Self-Check)
- [x] **Every mutation API** has ≥1 Function/Engine ✅
- [x] **No orphan Function** — FN-01..FN-20 ทุกตัวปรากฏใน trace (FN-16/FN-18 ผ่าน mutation rows; FN-17 ผ่าน read rows; FN-19/FN-20 ผ่าน FN-05/FN-15) ✅
- [x] **No orphan Engine** — ENG-DOA(API-11), ENG-NOTIFY(API-02/12/15), ENG-CSQ(API-12), ENG-GRADE(API-19) ✅
- [x] **No hidden logic in 02_API** — business logic ทั้งหมด traced ที่นี่ ✅

---

## §3.4 Dependencies

### External Engine called
- `ENG-DOA` (Policy Center F-DLG-001) — resolve reviewer, role-id OQ-PERF-05
- `ENG-NOTIFY` (F-NOTIFY) — 3 business events
- `ENG-CSQ` (7C) — per-person publish, EC OQ-PERF-06

### External data (soft-ref · OQ-PERF-07)
- HR Config #107 appraisal_cycle (via API-05)
- Employee Master (snapshot emp/pos/dept)

### External features that consume this feature's events
- Movement (F-HR-MOVE), Training, Succession (F134) — ดู 02_API §2.X

---

## §3.5 Locked Decisions Referenced (ดู 07_LOCKED)
- **LD-01** guard cascade order (closed→role→stage→scope) immutable
- **LD-02** staged DOA (send freeze → per-stage → publish last)
- **LD-03** CSQ per-person publish trigger (OQ-PERF-02 resolved)
- **LD-04** scope_type SELF/DEPT/ALL (OQ-PERF-03 resolved)
- **LD-05** re-open published authorized+reason+audit (OQ-PERF-01 resolved)
- **LD-06** ENG-GRADE register CUBIC Phase 2 (scope-local now)

---

## Audience Cheat-Sheet
| Reader | Read sections |
|---|---|
| BE dev | §3.1 + §3.2 + §3.3 |
| QA | §3.3 + FN Side effects + guard cascade (FN-18) |
| Architect / CUBIC | §3.2 (ENG-CSQ EC · ENG-DOA chain · ENG-GRADE register) + §3.4/§3.5 |
| PM | §3.3 (coverage view) |
