# 05_RULES — F131 Performance / ประเมินผลงาน

> **Audience:** Backend developer + QA
> **Purpose:** Business Rules + State Machine + Validation + Edge Cases + Errors + Security
> **Principle:** Declarative — อ่านแล้วเข้าใจโดยไม่ต้องดูโค้ด

---

## §5.1 Business Rules (BR)

### BR-01: รอบ/แบบประเมินจาก HR Config #107
- **Statement:** สร้างรอบดึง appraisal_cycle + config_version จาก HR Config #107 — **ไม่ hardcode** รอบ/แบบ/เกณฑ์.
- **Enforced by:** F131-API-02 precondition + F131-FN-01
- **Tag:** CONFIGURABLE (HR Config Admin · ต่อรอบ) · **Error:** BR_CONFIG_CYCLE_NOT_FOUND → 422
- **Rationale:** ฟอร์มกลางเป็นของ F-HR-CONFIG (LK-3)

### BR-02: น้ำหนัก KPI รวม = 100%
- **Statement:** `Σweight = 100` per appraisal (มิฉะนั้น block save). พิสูจน์: sum 90 → block.
- **Enforced by:** F131-FN-03 · **Error:** BR_KPI_WEIGHT_NOT_100 (VR-01) → 422 · **Tag:** FIXED (invariant)

### BR-03: self ก่อน mgr
- **Statement:** ต้องประเมินตนเอง (self) ก่อนหัวหน้าประเมิน (mgr) — บังคับโดย state order.
- **Enforced by:** state machine (goal→self→mgr) + FN-18 stage guard · **Tag:** FIXED

### BR-04: คะแนนรวม = weighted
- **Statement:** `weighted_score = Σ(mgr_score×weight)/Σweight` (เฉพาะ KPI ที่มี mgr_score).
- **Used by:** F131-FN-19 · **Tag:** FIXED (สูตร invariant)

### BR-05: สอบทานผ่าน DOA (staged) + decision ก่อนเผยแพร่ผล
- **Statement:** ต้องสอบทานผ่าน DOA แบบ staged (เลือกผู้สอบทานจริงต่อขั้น · ไม่ hardcode) + decision ก่อน published. Publish เกิดหลังขั้นสุดท้ายเท่านั้น.
- **Enforced by:** F131-FN-06 (send/freeze) + F131-FN-07 (per-stage/publish) + ENG-DOA
- **Tag:** FIXED (flow) · **chain = DYNAMIC 🤖** (role-id รอ CL-0013 · OQ-PERF-05) · **Error:** BR_REVIEWER_SLOT_EMPTY, BR_MGR_SCORE_INCOMPLETE

### BR-06: gap → Training = hook
- **Statement:** gap → Training เป็น hook (display-only, ไม่สร้างหลักสูตร). **Error:** BR_GAP_REQUIRED (ถ้าไม่มี gap) · **Tag:** FIXED (LK-5)

### BR-07: ผล → Movement = event
- **Statement:** ผล → ปรับเงินเดือน/ตำแหน่ง เป็น **event** ให้ Movement — **ไม่ CRUD** เงินเดือน/ตำแหน่งในฟีเจอร์นี้. ส่งได้ทุกผล published (decouple จาก gap). **Tag:** FIXED (LK-2)

### BR-08: ผลประเมิน RESTRICTED · masking ตาม role (SecC)
- **Statement:** score/decision/gap/notes = RESTRICTED (SecC). masking + row-scope ตาม role. out-of-scope ไม่อยู่ใน payload/DOM.
- **Enforced by:** F131-FN-17 · **Tag:** FIXED (preset P6)

### BR-09: audit append-only · ปิดรอบล็อกแก้
- **Statement:** ทุก create/แก้/สอบทาน → audit (who+at+act) append-only ห้ามลบ/แก้. ปิดรอบ → terminal lock ทุก mutation.
- **Enforced by:** F131-FN-16 + F131-FN-02 + FN-18 · **Tag:** FIXED

### BR-10: snapshot ชื่อ/ตำแหน่ง/แผนก ณ รอบ
- **Statement:** appraisal เก็บ snapshot emp_name/pos/dept ณ สร้าง (ไม่ live-join). ใช้ dept snapshot สำหรับ scope. **Tag:** FIXED

### BR-11: scope การเห็น — staff=SELF · mgr=DEPT · HR=ALL
- **Statement:** scope_type: staff เห็นเฉพาะของตน · mgr เฉพาะแผนกตน (emp_dept_snap=requester.dept) · HR(manage)=ทั้งหมด.
- **Enforced by:** F131-FN-17 · **Tag:** CONFIGURABLE (SEC scope_type · Admin) · มติ OQ-PERF-03 RESOLVED (LD-04)

### BR-12: re-open published = manage + open cycle + เหตุผลบังคับ + audit ใคร/เมื่อ
- **Statement:** เปิดแก้ไขผลหลังเผยแพร่ได้เฉพาะ authorized (manage) + รอบยังไม่ปิด + reason non-empty; append-only audit ผู้แก้. ส่งกลับขั้น mgr, เคลียร์ decision/stages, คงคะแนน/gap. re-publish → CSQ ยิงซ้ำ per-person.
- **Enforced by:** F131-FN-09 · **Tag:** FIXED · มติ OQ-PERF-01 RESOLVED (LD-05)

### BR-13: CSQ 7C hook ยิงตอนเผยแพร่ผลรายคน (per-person)
- **Statement:** ยิง `perf.result.published` (SecC/DC) per-person publish. ไม่ประกาศ OC/DC-doc/SC (LK-6).
- **Used by:** ENG-CSQ · **Tag:** DYNAMIC 🤖 (EC valuation · Architect · OQ-PERF-06) · มติ OQ-PERF-02 RESOLVED trigger (LD-03)

---

## §5.2 State Machines

### §5.2.1 Cycle status
```
draft → open → in_review → calibration → closed(terminal)
```
`closed` = terminal → ทุก mutation ต่อ appraisal ในรอบ block (FIX-05 · guard cascade layer 1).

| From | To | Action | Roles | Conditions |
|---|---|---|---|---|
| (new) | open | create | manage | config_ref valid (BR-01) |
| open/in_review/calibration | closed | close | manage | confirm (soft archive) |

### §5.2.2 Appraisal status (per-person)
```
goal ──saveKpi(Σ=100)──▶ self ──saveSelf──▶ mgr ──saveMgr──▶ calibration
                                                                   │
                                            doCalibSend(freeze) ───┤ (คง calibration)
                                            doCalibStage×N ────────┤
                                                                   ▼
                                        (ขั้นสุดท้าย) ──────▶ published
                                                                   │
                       ◀── doReopen(authorized+reason) ── published ┘  → กลับ mgr
                       published ──doPip(decision ทบทวน)──▶ published(+PIP)
```

| From | To | Action | Allowed roles | Conditions (guard cascade) |
|---|---|---|---|---|
| goal | self | saveKpi | manage | open cycle · goal · Σweight=100 · titles ครบ |
| self | mgr | saveSelf | staff (own) | open cycle · self · self_score 1–5 ครบ |
| mgr | calibration | saveMgr | mgr∥manage | open cycle · mgr · mgr_score 1–5 ครบ |
| calibration | calibration | doCalibSend | manage | open cycle · calibration · weighted_score≠null · slots ครบ (freeze) |
| calibration | calibration | doCalibStage (non-last) | manage | open cycle · calibration · current stage |
| calibration | published | doCalibStage (last) | manage | open cycle · calibration · last stage → +decision +CSQ +notify |
| published | mgr | doReopen | manage | open cycle · published · reason non-empty |
| published | published | doPip | manage | open cycle · decision "ทบทวน" · gap non-empty |

> **transition ย้อนหลัง block (FIX-02):** saveKpi/saveSelf/saveMgr เรียกกับ status ที่ไม่ตรงขั้น → ERR_STAGE_INVALID. **ข้ามขั้น block (FIX-01):** doCalibSend ต้อง weighted_score≠null.

---

## §5.3 Permission Matrix (scope_type)

| Role | scope | สร้าง/ปิดรอบ | KPI(goal) | self | mgr review | calib(send/stage) | PIP | reopen | send hooks | เห็นผล/decision/gap ผู้อื่น |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| พนักงาน (staff) | SELF | — | — | ✅ own | — | — | — | — | — | ❌ (mask + ไม่อยู่ DOM) |
| หัวหน้า (mgr) | DEPT | — | — | — | ✅ (mgr stage) | — | — | — | — | เฉพาะแผนกตน (DEPT) |
| HR/HRBP (manage) | ALL | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (ALL) |

> **sec.can (server mirror):** `saveMgr` = mgr∥manage; ทุก action อื่น = manage เท่านั้น. 2 ชั้น: function guard + UI (ไม่ render ปุ่มให้ role ที่ไม่ผ่าน · FIX-03).

---

## §5.4 Field Validation Rules

| VR | Field/Action | เงื่อนไข | ประเภท | Error / ข้อความ (verbatim) |
|---|---|---|---|---|
| VR-01 | KPI weight | Σ ≠ 100 | Error 422 | BR_KPI_WEIGHT_NOT_100 · "น้ำหนัก KPI รวมต้องเท่ากับ 100% (ตอนนี้ N%)" |
| VR-02 | doCalibSend | slot ผู้สอบทานว่าง | Prevent 422 | BR_REVIEWER_SLOT_EMPTY · "กรุณาเลือกผู้สอบทานให้ครบทุกขั้น" |
| VR-03 | doReopen | reason ว่าง | Error 422 | BR_REASON_REQUIRED · "กรุณาระบุเหตุผล" |
| VR-04 | ทุก mutation | รอบ closed | Prevent 409 | BR_CYCLE_CLOSED · "รอบนี้ปิดแล้ว — แก้ไขไม่ได้" |
| VR-05 | mutation | role ไม่ผ่าน sec.can | Prevent 403 | ERR_INSUFFICIENT_ROLE · "สิทธิ์ไม่พอ" |
| VR-06 | submit | `_busy`=true / dup idempotency | Prevent | (กัน double-submit เงียบ · FN-92) |
| VR-07 | doCalib | status ≠ calibration ∥ mgr score ไม่ครบ | Prevent 409/422 | ERR_STAGE_INVALID / BR_MGR_SCORE_INCOMPLETE · "สอบทานได้เฉพาะแบบประเมินที่ให้คะแนนหัวหน้าครบและรอสอบทาน" |
| VR-08 | saveSelf/saveMgr | คะแนนไม่ครบ 1–5 | Error 422 | "กรุณาให้คะแนน[ตนเอง/หัวหน้า]ครบทุก KPI (1–5)" |
| VR-09 | saveKpi | ชื่อ KPI ว่าง | Error 422 | "กรุณากรอกชื่อ KPI ให้ครบ" |
| VR-10 | doPip | gap ว่าง | Error 422 | BR_GAP_REQUIRED · "กรุณาระบุประเด็นที่ต้องพัฒนา" |

### Cross-field
- `weighted_score` = computed (ไม่ user input) → ENG/FN-19.
- publish ต้องมีทุก stage.status='done'.

---

## §5.5 Edge Cases (BA fix order §10.1 confirmed + Phase 2.5 probing)

### EC-01: สอบทาน+เผยแพร่ข้ามขั้น (FIX-01)
- **Scenario:** record ยัง goal/ไม่มีคะแนน mgr → doCalib → published "ผ่าน"
- **Resolution:** guard `status=calibration && weighted_score≠null` (FN-06/FN-18); ไม่ผ่าน → toast + return
- **Error:** BR_MGR_SCORE_INCOMPLETE / ERR_STAGE_INVALID · **Test:** AC-19 / e2e P2

### EC-02: transition ย้อนหลัง (FIX-02)
- **Scenario:** record published ถูกดันกลับ/แก้คะแนน
- **Resolution:** stage guard: saveKpi=goal · saveSelf=self · saveMgr=mgr เท่านั้น
- **Error:** ERR_STAGE_INVALID · **Test:** AC-19 / e2e P1

### EC-03: พนักงานประเมินแทนหัวหน้า/สอบทานเอง (FIX-03)
- **Scenario:** staff เรียก saveMgr/doCalib/doPip/send*
- **Resolution:** role guard (function `sec.can` + UI ไม่ render ปุ่ม)
- **Error:** ERR_INSUFFICIENT_ROLE · **Test:** AC-17/AC-19 / e2e P3

### EC-04: พนักงานเห็น decision/gap ผู้อื่น (FIX-04)
- **Scenario:** staff เปิดแท็บสอบทาน เห็น decision+gap ทุกคน
- **Resolution:** scopeSelf (SELF) + mask; queue ซ่อน; out-of-scope ไม่อยู่ DOM/payload (FN-17)
- **Test:** AC-17

### EC-05: Concurrent staged review (PR-1) `[AI-DEFAULT]`
- **Scenario:** ผู้สอบทาน 2 ขั้นบันทึกพร้อมกัน
- **Resolution:** optimistic lock `version` → first-write-wins, second 409 `[AI-DEFAULT]`
- **Error:** ERR_STALE_DATA · **OQ-PERF-09** (Architect confirm) · **Test:** TC-CC-01

### EC-06: HR Config #107 ไม่มี appraisal_cycle `[AI-DEFAULT]`
- **Scenario:** config_version หาย / upstream down
- **Resolution:** error-state ก่อนสร้างรอบ (ไม่สร้าง cycle เปล่า) `[AI-DEFAULT]`
- **Error:** BR_CONFIG_CYCLE_NOT_FOUND / ERR_CONFIG_UPSTREAM_DOWN · **Test:** TC-CFG-01

### EC-07: ปิดรอบแล้วยัง mutate ได้ (FIX-05)
- **Scenario:** closed cycle → saveSelf ยังผ่าน
- **Resolution:** cycleClosed guard ต้นทุก mutation (guard cascade layer 1)
- **Error:** BR_CYCLE_CLOSED · **Test:** AC-02 / e2e P4

### EC-08: DOA slot auto-preset / คลิกเดียวจบ 2 ขั้น (FIX-06)
- **Scenario:** slot preset P1/P2 + publish ใน action เดียว
- **Resolution:** slot ว่าง (value:null) + แยก 2 action (send freeze → per-stage → publish last), stamp at/actor ต่อขั้น
- **Test:** AC-08 / e2e slot-empty

### EC-09: overdue (FN-09)
- **Scenario:** ประเมินเกินกำหนด → badge + reminder · **Resolution:** `isOverdue` (status≠published && due<today) · **Test:** AC-06

### EC-10: mgr ย้ายแผนกกลางรอบ (BRD §10.2) `[AI-DEFAULT]`
- **Scenario:** DEPT scope ใช้ snapshot หรือ live? · **Resolution:** ใช้ `emp_dept_snap` (snapshot ณ รอบ · BR-10) `[AI-DEFAULT]` → mgr scope เทียบกับ snapshot dept · **OQ:** flag ใน BRD §10.2 (ไม่ block) · **Test:** TC-DEPT-01

---

## §5.6 Error Catalog

| Code | HTTP | Message (i18n) | Cause |
|---|---|---|---|
| ERR_NOT_AUTHENTICATED | 401 | error.auth.unauth | No/invalid token |
| ERR_INSUFFICIENT_ROLE | 403 | error.auth.role · "สิทธิ์ไม่พอ" | sec.can fail (FIX-03) |
| ERR_NOT_FOUND | 404 | error.notfound | appraisal/cycle missing |
| ERR_STAGE_INVALID | 409 | error.stage.invalid | status ≠ required stage (FIX-01/02) |
| BR_CYCLE_CLOSED | 409 | br.cycle.closed · "รอบนี้ปิดแล้ว — แก้ไขไม่ได้" | closed cycle (FIX-05) |
| ERR_STALE_DATA | 409 | error.concurrency.stale | version mismatch (EC-05) |
| ERR_NO_CURRENT_STAGE | 409 | error.calib.nostage | no current calibration stage |
| BR_KPI_WEIGHT_NOT_100 | 422 | br.kpi.weight · "น้ำหนัก KPI รวมต้องเท่ากับ 100%" | VR-01 |
| BR_KPI_TITLE_REQUIRED | 422 | br.kpi.title | VR-09 |
| BR_SELF_SCORE_INCOMPLETE | 422 | br.self.score | VR-08 |
| BR_MGR_SCORE_INCOMPLETE | 422 | br.mgr.score | VR-08 / FIX-01 |
| BR_REVIEWER_SLOT_EMPTY | 422 | br.reviewer.empty · "กรุณาเลือกผู้สอบทานให้ครบทุกขั้น" | VR-02 |
| BR_REASON_REQUIRED | 422 | br.reason.required · "กรุณาระบุเหตุผล" | VR-03 |
| BR_GAP_REQUIRED | 422 | br.gap.required · "กรุณาระบุประเด็นที่ต้องพัฒนา" | VR-10 |
| BR_CONFIG_CYCLE_NOT_FOUND | 422 | br.config.notfound | BR-01 / EC-06 |
| ERR_CONFIG_UPSTREAM_DOWN | 502 | error.config.upstream | HR Config #107 soft-ref down (EC-06) |

---

## §5.7 Security Bible Application

> Domains: **D2 (Auth), D7 (PII), D9 (Audit), D13 (RBAC/scope), D-CLASS**. Preset **P6 (HR/PII · 15 controls)**.

### D2: Auth & Session — ทุก endpoint JWT; role source server-side.
### D7: PII — emp/reviewer/who snapshots → encrypt at rest (column-level) + PDPA scope; logs ใช้ ref ไม่ใช่ชื่อเต็ม.
### D9: Audit — ทุก mutation → T_perf_audit append-only (who+at+diff-act), immutable, retention ≥7 ปี. re-open ไม่ลบผลเดิม (BR-12).
### D13: RBAC/scope — sec.can 2 ชั้น (function+UI); scope_type SELF/DEPT/ALL (BR-11) row+column.

### D-CLASS: Data Classification ⭐
Per-field ที่ 04_DB §4.2 + §4.6. **Enforcement summary:**

| Layer | Confidential (emp/reviewer/who names, KPI title/target) | Restricted (score/decision/gap/notes) |
|---|---|---|
| API response | mask if no permission | **excluded จาก payload ถ้าไม่ผ่าน scope** (ไม่ใช่แค่ UI) |
| UI display | `***` | `•••` / out-of-scope ไม่อยู่ DOM |
| Export/Report | excluded column | require Restricted Resources approval; aggregate count ไม่รั่ว |
| Audit | log view + mutation | log view + mutation + export attempt |

**Wire points:** Policy Center → Data Classification (master/override) · Restricted Resources (ACL per-record · **OQ-PERF-10 OPEN**) · DOA (staged calibration).

---

## §5.8 Compliance & Audit
| Requirement | Implementation |
|---|---|
| ผลประเมินลับต่อบุคคล (RESTRICTED) | BR-08 + FN-17 + D-CLASS |
| Segregation of Duties (สอบทาน) | staged DOA (Maker ≠ Approver · §1.4 SoD) |
| Immutable audit trail | BR-09 + T_perf_audit append-only |
| CSQ 7C compliance | BR-13 + ENG-CSQ per-person publish |
| PDPA | D7 encryption + retention (04_DB §4.7) |
