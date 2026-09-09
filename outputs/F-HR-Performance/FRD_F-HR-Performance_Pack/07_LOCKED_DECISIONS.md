# 07_LOCKED_DECISIONS — F131 Performance / ประเมินผลงาน

> **Audience:** All roles
> **Purpose:** Scope Lock (immutable) + Locked Decisions — ห้ามเปิดอภิปรายซ้ำ

---

## §7.0 Scope Lock (Imported from BRD §3.4) ⭐ — IMMUTABLE

> ข้อยืนยันจากใบเซ็น/มติ — ห้าม override ตลอด pack + chain ปลายน้ำ. spec ขัด LOCK → LOCK ชนะ.

| LOCK-ID | ข้อยืนยัน | อ้างเอกสาร | สถานะใน FRD |
|---|---|---|---|
| **LK-1** | สอบทาน = DOA (มติ 17 ส.ค. 2026) — เลือก "คน" จริงต่อขั้น · ห้าม hardcode/auto-preset | current-state §3 · FIX-06 | ✅ สอดคล้อง (FN-06 staged, slot ว่าง, ENG-DOA resolve) |
| **LK-2** | ผล → Movement = **event** (ไม่ CRUD เงินเดือน/ตำแหน่งในฟีเจอร์นี้) | F-HR-MOVE · OB-3 | ✅ (FN-11 dispatchMovement event only) |
| **LK-3** | รอบ/แบบประเมิน จาก HR Configuration #107 — ไม่สร้าง/แก้ในฟีเจอร์นี้ | F-HR-CONFIG · OB-1 | ✅ (FN-01 + API-05 lookup, snapshot config_version) |
| **LK-4** | ผลประเมิน = **RESTRICTED (SecC)** · masking ตาม role · audit **append-only** | current-state §3 · OB-5 | ✅ (BR-08/09 · FN-16/17 · 04_DB §4.6) |
| **LK-5** | gap → Training = **hook** (ไม่สร้างหลักสูตร) | A-PERF-02 · OB-4 | ✅ (FN-10 dispatchTraining hook) |
| **LK-6** | CSQ ประกาศ **SecC (masking) + DC (decision)** เท่านั้น — **ห้าม** OC / DC-doc / SC | PREBRIEF §12 · STANDARD_BASELINE §4 | ✅ (ENG-CSQ payload SecC/DC only) |

- **Scope Lock Ref:** BRD §3.4 (สืบทอด current-state §3 · fix order F131 · F-HR-MOVE OB-3) · 2026-09-09.
- **Drift พบระหว่างเขียน FRD (ชั้นที่ 3):** ไม่มี. Screen inventory 4 tab = BRD = PREBRIEF; ทุก FN มี hook; ไม่มี scope creep.

---

## §7.1 Locked Decisions (LD)

### LD-01: Guard cascade order (closed → role → stage → scope)
- **Date:** 2026-09-09 · **Context:** BA fix order FIX-01..05 (bypass ทุก transition)
- **Decision:** ทุก appraisal mutation ผ่าน `F131-FN-18 guardMutation` 4 ชั้นเรียงกัน: closed-cycle → role(sec.can) → stage(status) → scope/validate.
- **Rationale:** ป้องกัน bypass ทุกรูปแบบที่พิสูจน์ในโปรโตไทป์ (goal→published ข้ามขั้น, ย้อนหลัง, staff เดินผล, closed mutate).
- **Implications:** 03_LOGIC FN-18; 02_API guard cascade block ทุก mutation; 06_TESTS AC-19 (P1-P4).
- **Reversibility:** LOW (governance core — ห้ามอ่อน).

### LD-02: Staged DOA (send freeze → per-stage → publish last)
- **Date:** 2026-09-09 · **Context:** FIX-06 (คลิกเดียวจบ 2 ขั้น + slot preset)
- **Decision:** สอบทานแยก ≥2 action: `sendCalibration` (freeze รายชื่อ, คง calibration) → `recordCalibrationStage` per-stage (stamp at/actor) → publish บนขั้นสุดท้ายเท่านั้น. Slot ว่าง (เลือกคนจริง · LK-1).
- **Rationale:** SoD จริง — ผู้สอบทานแต่ละขั้นกระทำเอง; ป้องกันเผยแพร่โดยผู้ประเมิน.
- **Implications:** T_perf_calibration_stage; API-11/12; ENG-DOA.
- **Reversibility:** LOW.

### LD-03: CSQ 7C trigger = per-person publish (OQ-PERF-02 RESOLVED)
- **Date:** 2026-09-09 · **Decision:** ยิง `perf.result.published` (SecC/DC) ตอนเผยแพร่ผลรายคน (ทุกครั้ง รวม re-publish). ไม่ประกาศ OC/DC-doc/SC (LK-6).
- **Open (deferred):** EC valuation detail = Architect (OQ-PERF-06).
- **Reversibility:** MEDIUM (trigger locked; valuation deferred).

### LD-04: scope_type SELF/DEPT/ALL (OQ-PERF-03 RESOLVED)
- **Date:** 2026-09-09 · **Decision:** staff=SELF · mgr=DEPT (เฉพาะแผนกตน, snapshot dept) · HR(manage)=ALL. Enforce row+column server-side (FN-17), ไม่ใช่แค่ UI.
- **Reversibility:** MEDIUM (config SEC scope_type).

### LD-05: Re-open published — authorized + reason + append-only audit (OQ-PERF-01 RESOLVED)
- **Date:** 2026-09-09 · **Decision:** อนุญาต re-open เฉพาะ authorized (manage) + open cycle + reason บังคับ + audit ผู้แก้; ส่งกลับขั้น mgr, เคลียร์ decision/stages, คงคะแนน/gap; re-publish → CSQ ยิงซ้ำ per-person. ผลเดิมไม่ลบ.
- **Reversibility:** LOW.

### LD-06: ENG-GRADE register CUBIC at Phase 2 (scope-local now)
- **Date:** 2026-09-09 · **Decision:** `performance-grade-mapper` = DRAFT scope-local; register CUBIC เมื่อยืนยัน reuse (Succession/Movement grading).
- **Owner:** Architect team · **Reversibility:** EASY.

### LD-07: team-calibration KEPT this wave (OQ-PERF-04 RESOLVED)
- **Date:** 2026-09-09 · **Decision:** teamCalibHTML view เก็บรอบนี้ (mock adjust, ยังไม่ผูกปลายทาง).
- **Reversibility:** EASY (ตัดได้ wave ถัดไปถ้า Strike เคาะ).

### LD-08: Archetype = master+cycle (NOT Pattern Q)
- **Date:** 2026-09-09 · **Decision:** ไม่ใช่ transaction document — ไม่มีเลขรัน/PDF/ลายเซ็น/เอกสารคนถือ. doccfg ✗ · pdfdoc ✗. P-02 = view drawer tabbed (C), ไม่ใช่ G+H+I.
- **Reversibility:** LOW (archetype confirmed PREBRIEF).

---

## §7.2 Convention Deviations
### CD-01: "route" = tab id (ไม่มี hash route แยกต่อ tab)
- **Convention default:** หน้า = hash route.
- **Deviation:** โปรโตไทป์ tab-based SPA (`state.tab`) — base-kit มี getRoute()/navigate() scaffold แต่ feature ใช้ tab-state.
- **Reason:** 1 feature = 1 เมนู (Iron Rule) · 4 tab ในหน้าเดียว. dev ผูก tab id (`cycle/appr/review/report`) แทน hash.
- **Approved by:** observed จาก gated HTML (Mode A) — ไม่แก้จอ.

### CD-02: ไม่โชว์ snake_case/id ภายในบนจอ (Iron Rule #81)
- appraisal_cycle id (#107 v3/v2) ไม่โชว์ — ใช้ชื่อผู้ใช้ (cfg label). scope_type/status enum แปลงเป็นภาษาไทยบน UI.

---

## §7.3 Open Questions (ยังไม่ resolved — carry ใน 00_OVERVIEW §0.8)
> ไม่เดา — รอ owner. ไม่ block FRD (downstream/config).

| OQ | รอใคร |
|---|---|
| OQ-PERF-05 DOA chain role-ids (CL-0013) | BA (config) |
| OQ-PERF-06 CSQ EC valuation | Architect |
| OQ-PERF-07 soft-ref ปลายทางยังไม่ build | PM |
| OQ-PERF-08 360/competency/check-in scope | Strike |
| OQ-PERF-09 concurrent staged-review lock | Architect (`[AI-DEFAULT]` optimistic) |
| OQ-PERF-10 Restricted Resources wire | Security/Policy Center |
| OQ-PERF-11 mock-data gap (mgr-stage ฝ่ายผลิต) | BA/QA (spec note, ไม่แก้ HTML) |

---

## §7.4 Architecture Tradeoffs
### AT-01: RESTRICTED enforce ที่ payload (ไม่ใช่แค่ UI hide)
- **Tradeoff:** query complexity (scope filter server-side) vs. security. **Accepted:** YES — out-of-scope ต้องไม่อยู่ใน DOM/payload (FIX-04 บทเรียน).

### AT-02: soft-ref ปลายทาง (Movement/Training/Succession/HR Config/ENG-*) = event/hook contract frozen ก่อน build
- **Tradeoff:** ปลายทางยังไม่ build → payload contract freeze ที่ 02_API §2.X. **Accepted:** YES (OQ-PERF-07).

---

## §7.5 Decisions Deferred to Implementation
| Item | Owner | Deadline |
|---|---|---|
| DOA chain role-id (CL-0013) | BA | ก่อน Phase 3 (BRD Delivery) |
| CSQ EC valuation | Architect | ก่อน Phase 4 |
| ENG-GRADE CUBIC registration | Architect | Phase 2 |
| Restricted Resources ACL wire | Policy Center | Pre-deploy |

## §7.6 References
- Convention: `knowledge/conventions.md` · Scope Lock: BRD §3.4 · Fix order: REVIEW_FIX_ORDER_F131 · Declarations: 03_DOA/NTF/CSQ_BRIEF (รันหลัง step 7)
