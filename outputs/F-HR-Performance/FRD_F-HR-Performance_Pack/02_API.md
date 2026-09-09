# 02_API — F131 Performance / ประเมินผลงาน

> **Audience:** Backend developer (HTTP layer)
> **Purpose:** API contracts — CUBIC API Entity format
> **🚨 Iron Rule:** ห้าม business logic >5 lines ที่นี่ — ย้ายไป 03_LOGIC §3.1
> **🚨 R8:** ทุก mutation API ต้องระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3
> **Guard cascade (ทุก appraisal mutation):** closed-cycle → role(sec.can) → stage(status) → scope/field-validate. รายละเอียด 05_RULES §5.5.

Base path: `/api/v1/performance`. Auth: JWT + `X-Tenant-Id` (RLS). Role source = server-side mirror ของ `sec.can()`.

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth (role) |
|---|---|---|---|---|
| F131-API-01 | GET | /cycles | List รอบประเมิน | required |
| F131-API-02 | POST | /cycles | สร้างรอบจาก HR Config (FN-01) | manage (HR) |
| F131-API-03 | GET | /cycles/:id | Cycle detail + per-person status (FN-11) | required |
| F131-API-04 | POST | /cycles/:id/close | ปิดรอบ (FN-11/FN-91) | manage (HR) |
| F131-API-05 | GET | /config/appraisal-cycles | Lookup รอบจาก HR Config #107 (soft-ref) | manage (HR) |
| F131-API-06 | GET | /appraisals | List แบบประเมิน (scoped+masked · FN-90/94) | required |
| F131-API-07 | GET | /appraisals/:id | Appraisal detail (scoped+masked · FN-94) | required |
| F131-API-08 | PUT | /appraisals/:id/kpis | ตั้งเป้า/KPI Σ=100 (FN-02) | manage · goal stage |
| F131-API-09 | POST | /appraisals/:id/self | ประเมินตนเอง (FN-03) | staff (own) · self stage |
| F131-API-10 | POST | /appraisals/:id/manager-review | หัวหน้าประเมิน (FN-04) | mgr∥manage · mgr stage |
| F131-API-11 | POST | /appraisals/:id/calibration/send | ส่งสอบทาน — freeze reviewers (FN-08) | manage · calibration |
| F131-API-12 | POST | /appraisals/:id/calibration/stage | บันทึกผลรายขั้น / publish บนขั้นสุดท้าย (FN-05/08) | manage (reviewer stage) |
| F131-API-13 | POST | /appraisals/:id/pip | เปิดแผน PIP (FN-10) | manage |
| F131-API-14 | POST | /appraisals/:id/reopen | เปิดแก้ไขผลหลังเผยแพร่ (OQ-PERF-01) | manage · published |
| F131-API-15 | POST | /appraisals/:id/reminder | ส่งการเตือน overdue (FN-09) | manage |
| F131-API-16 | POST | /appraisals/:id/dispatch/training | gap → Training hook (FN-06) | manage |
| F131-API-17 | POST | /appraisals/:id/dispatch/movement | ผล → Movement event (FN-07) | manage |
| F131-API-18 | POST | /appraisals/:id/dispatch/succession | ผล → Succession hook (FIX-09) | manage |
| F131-API-19 | GET | /reports/distribution | รายงานการกระจายคะแนน (FN-13) | required (scoped) |

---

## §2.2 Per-API Contract

### F131-API-02: POST /cycles
| Field | Value |
|---|---|
| summary | สร้างรอบประเมินจาก HR Config #107 (BR-01 · ไม่ hardcode รอบ/แบบ) |
| auth | required · role manage (HR) |

**Request:** Headers `X-Tenant-Id`, `Idempotency-Key`. Body:
```json
{ "config_ref": "CFG-A", "scope_target": "org", "due": "2026-12-31" }
```
**Validation (≤5 lines):** `config_ref` required + exists ใน HR Config lookup (F131-API-05); `scope_target` ∈ {org,dept}; complex/snapshot → F131-FN-01.
**Response 201:** `{ "id":"uuid", "name":"...", "status":"open", "config_version":"v3", "due":"..." }`
**Errors:** 400 ERR_VALIDATION_FAILED · 403 ERR_INSUFFICIENT_ROLE · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 BR_CONFIG_CYCLE_NOT_FOUND (BR-01 / EC-06).
**Preconditions:** HR Config #107 มี appraisal_cycle ตาม config_ref.
**Side effects:** INSERT T_perf_cycle (snapshot config_version); INSERT T_perf_audit(cycle-level ถ้ามี); emit notify `perf.cycle.opened`.
**Calls (Logic):** F131-FN-01 createCycleFromConfig · (notify via ENG-NOTIFY).

---

### F131-API-04: POST /cycles/:id/close
| Field | Value |
|---|---|
| summary | ปิดรอบ (terminal) → ล็อกทุก mutation ต่อ appraisal ในรอบ (FIX-05) |
| auth | manage (HR) |

**Response 200:** `{ "id":"...", "status":"closed", "closed_at":"..." }`
**Errors:** 403 ERR_INSUFFICIENT_ROLE · 404 ERR_NOT_FOUND · 409 ERR_STALE_DATA.
**Preconditions:** cycle.status ≠ closed.
**Side effects:** UPDATE cycle.status='closed'; INSERT audit. หลังปิด → guard cascade layer 1 block ทุก appraisal mutation ในรอบ.
**Calls (Logic):** F131-FN-02 closeCycle.

---

### F131-API-05: GET /config/appraisal-cycles
| Field | Value |
|---|---|
| summary | Lookup รอบที่ประกาศไว้ที่ HR Config #107 (feature อ่าน ไม่สร้าง) |
| auth | manage |

**Response 200:** `{ "data":[ { "config_ref":"CFG-A", "label":"รอบครึ่งปีหลัง 2569 (ก.ค.–ธ.ค.)", "sub":"ประกาศไว้ในตั้งค่า HR", "config_version":"v3" } ] }`
**Errors:** 502 ERR_CONFIG_UPSTREAM_DOWN (EC-06 · HR Config #107 ยังไม่ build — soft-ref).
**Side effects:** — (read-only proxy to HR Config #107).
**Calls (Logic):** — (thin proxy).

---

### F131-API-06: GET /appraisals
| Field | Value |
|---|---|
| summary | List แบบประเมิน — **scope + mask ตาม role** (FN-90/94) |
| auth | required (staff/mgr/hr) |

**Query:** `cycle_id`, `status` (goal/self/mgr/calibration/published), `q` (ค้นหา emp/pos/dept), `limit`, `offset`.
**Response 200:** `{ "data":[ { "id":"A2","emp_name":"...", "status":"self", "weight_sum":100, "weighted_score":"•••", "decision":null, "due":"...","overdue":true } ], "total":N }`
> **⚠️ Restricted rule:** rows out-of-scope **ไม่อยู่ใน data**; columns `weighted_score/decision/gap/*_score` ถูก mask/excluded ถ้า role ไม่ผ่าน (F131-FN-17). staff เห็นเฉพาะ `employee_ref=self`; mgr เฉพาะ `emp_dept_snap=self.dept`.
**Errors:** 401 · 403.
**Calls (Logic):** F131-FN-14 buildAppraisalListQuery → F131-FN-17 applyScopeAndMask.

---

### F131-API-08: PUT /appraisals/:id/kpis
| Field | Value |
|---|---|
| summary | ตั้งเป้า/KPI (BR-02 Σweight=100) |
| auth | manage · **goal stage only** |

**Body:** `{ "kpis":[ {"title":"...","weight":60,"target":"99%"} ] }`
**Validation:** ทุก title ไม่ว่าง; `Σweight = 100` (มิฉะนั้น 422 · VR-01); complex → F131-FN-03.
**Response 200:** `{ "id":"...", "status":"self", "weight_sum":100 }` (status goal→self).
**Errors:** 403 ERR_INSUFFICIENT_ROLE · 409 BR_CYCLE_CLOSED (FIX-05) · 409 ERR_STAGE_INVALID ("เฉพาะขั้นตั้งเป้า" · FIX-02) · 422 BR_KPI_WEIGHT_NOT_100.
**Guard cascade:** closed → role(manage) → stage(goal) → validate(Σ=100, titles).
**Side effects:** REPLACE T_perf_kpi_line; UPDATE appraisal.status='self'; INSERT audit "ตั้งเป้า/KPI".
**Calls (Logic):** F131-FN-03 saveKpiGoals · F131-FN-16 pushAudit · F131-FN-18 guardMutation.

---

### F131-API-09: POST /appraisals/:id/self
| Field | Value |
|---|---|
| summary | พนักงานประเมินตนเอง (FN-03 · BR-03 self ก่อน mgr) |
| auth | staff (own only) · **self stage** |

**Body:** `{ "scores":[ {"kpi_id":"...","self_score":5} ], "self_note":"..." }`
**Validation:** ทุก KPI มี self_score 1–5.
**Response 200:** status self→mgr.
**Errors:** 403 (ไม่ใช่ของตน/role) · 409 BR_CYCLE_CLOSED · 409 ERR_STAGE_INVALID · 422 (คะแนนไม่ครบ).
**Guard cascade:** closed → role(own staff) → stage(self) → validate(scores 1–5).
**Side effects:** UPDATE kpi_line.self_score + appraisal.self_note; status='mgr'; audit "พนักงานประเมินตนเอง".
**Calls (Logic):** F131-FN-04 recordSelfAssessment · FN-16 · FN-18.

---

### F131-API-10: POST /appraisals/:id/manager-review
| Field | Value |
|---|---|
| summary | หัวหน้าประเมิน + weighted score (FN-04 · BR-04) |
| auth | **mgr∥manage** (sec.can('saveMgr')) · **mgr stage** |

**Body:** `{ "scores":[ {"kpi_id":"...","mgr_score":4} ], "mgr_note":"..." }`
**Validation:** ทุก KPI มี mgr_score 1–5.
**Response 200:** `{ "status":"calibration", "weighted_score":4.20 }` (คำนวณ Σ score×weight/100).
**Errors:** 403 · 409 BR_CYCLE_CLOSED · 409 ERR_STAGE_INVALID · 422.
**Guard cascade:** closed → role(mgr∥manage) → stage(mgr) → validate(scores).
**Side effects:** UPDATE mgr_score + mgr_note + weighted_score; status='calibration'; audit "หัวหน้าประเมิน + คะแนน".
**Calls (Logic):** F131-FN-05 recordManagerReview → F131-FN-19 computeWeightedScore · FN-16 · FN-18.

---

### F131-API-11: POST /appraisals/:id/calibration/send
| Field | Value |
|---|---|
| summary | ส่งสอบทาน — freeze ผู้สอบทาน 2 ขั้น (FN-08 · LK-1 ไม่ hardcode · FIX-06) |
| auth | manage · **calibration stage + คะแนน mgr ครบ** |

**Body:** `{ "reviewers":[ {"stage_no":1,"role_slot":"หัวหน้าสายงาน","reviewer_ref":"P1"}, {"stage_no":2,"role_slot":"ผู้สอบทาน (HRBP/ผู้บริหาร)","reviewer_ref":"P3"} ] }`
**Validation:** slot ครบทุกขั้น (ว่าง = 422 VR-02); precondition `weighted_score != null` (FIX-01).
**Response 200:** `{ "status":"calibration", "approvals":[{stage_no:1,status:"current"},{stage_no:2,status:"pending"}] }` (status **คง calibration** — ไม่ publish).
**Errors:** 403 · 409 BR_CYCLE_CLOSED · 409 ERR_STAGE_INVALID · 422 BR_REVIEWER_SLOT_EMPTY · 422 BR_MGR_SCORE_INCOMPLETE (FIX-01).
**Side effects:** INSERT T_perf_calibration_stage (staged, stage1=current); audit "ส่งสอบทาน · เลือกผู้สอบทาน 2 ขั้น (คง calibration)"; **ENG-DOA resolve** reviewer per role_slot (role-id chain OQ-PERF-05).
**Calls (Logic):** F131-FN-06 sendCalibration → ENG-DOA · FN-16 · FN-18.

---

### F131-API-12: POST /appraisals/:id/calibration/stage
| Field | Value |
|---|---|
| summary | ผู้สอบทานขั้น current บันทึกผล; ขั้นสุดท้าย → publish + decision + CSQ + notify (FN-05 · FIX-06/07) |
| auth | manage (ผู้สอบทานขั้น current) · **calibration stage** |

**Body:** `{ "decision":"ผ่าน" }` (เฉพาะขั้นสุดท้าย; enum ผ่าน / ทบทวน (PIP) / ไม่ผ่าน).
**Response 200 (non-last):** `{ "stage_no":1,"stage_status":"done","next":2,"status":"calibration" }`
**Response 200 (last/publish):** `{ "status":"published","decision":"ผ่าน","weighted_score":4.20 }`
**Errors:** 403 · 409 BR_CYCLE_CLOSED · 409 ERR_STAGE_INVALID ("เฉพาะแบบประเมินที่รอสอบทาน") · 409 ERR_NO_CURRENT_STAGE.
**Side effects (non-last):** UPDATE stage.status='done' + acted_at + actor_ref; ต่อขั้น current; audit "สอบทานขั้น N (role) · reviewer".
**Side effects (last/publish):** UPDATE appraisal.status='published' + decision; ถ้า "ทบทวน" → gap default; audit "เผยแพร่ผล · decision:X" + audit "บันทึกผลประเมินเข้า 7C"; **emit CSQ `perf.result.published` (per-person · SecC/DC)**; emit notify `perf.result.published`.
**Calls (Logic):** F131-FN-07 recordCalibrationStage → ENG-CSQ (publish) + ENG-NOTIFY · FN-16 · FN-18.
> **CSQ (OQ-PERF-02 RESOLVED):** trigger = per-person publish. EC valuation detail = OQ-PERF-06 (Architect). ไม่ประกาศ OC/DC-doc/SC (LK-6).

---

### F131-API-14: POST /appraisals/:id/reopen
| Field | Value |
|---|---|
| summary | เปิดแก้ไขผลหลังเผยแพร่ (OQ-PERF-01 RESOLVED · BR-12) |
| auth | manage (authorized HR) · **published + open cycle** |

**Body:** `{ "reason":"คะแนนผิด" }` (**reason บังคับ non-empty** · VR-03).
**Response 200:** `{ "status":"mgr","decision":null }` (กลับขั้นหัวหน้าประเมิน; เคลียร์ decision + calibration stages; **คงคะแนน/gap ไว้อ้างอิง**).
**Errors:** 403 · 409 BR_CYCLE_CLOSED (open cycle only) · 409 ERR_STAGE_INVALID ("เฉพาะผลที่เผยแพร่แล้ว") · 422 BR_REASON_REQUIRED.
**Side effects:** **append-only audit** "เปิดแก้ไขผลหลังเผยแพร่ · เหตุผล: {reason}" (who+at — ผลเดิมไม่ลบ); DELETE calibration_stage rows; UPDATE status='mgr', decision=null.
> Re-publish ผ่าน flow เดิม (mgr→calibration→published) · staged DOA ซ้ำ · **CSQ ยิงซ้ำ per-person**.
**Calls (Logic):** F131-FN-09 reopenPublished · FN-16 · FN-18.

---

### F131-API-16 / 17 / 18: dispatch (Training / Movement / Succession)
| Field | Value |
|---|---|
| summary | ส่งต่อผล — **display-only hook / event** (ไม่ CRUD ปลายทาง · LK-2/LK-5) |
| auth | manage · appraisal.status=published |

- **API-16 training (FN-06 · BR-06):** body `{}` → emit `perf.gap.training_requested` payload `{ appraisal_id, gap }`. Gap ต้องมีค่า. **ไม่สร้างหลักสูตร.**
- **API-17 movement (FN-07 · BR-07):** emit `perf.result.movement_requested` payload `{ appraisal_id, employee_ref, decision, weighted_score }`. **ไม่ปรับเงินเดือน/ตำแหน่งเอง.** ส่งได้ทุกผลที่ published (decouple จาก gap — top performer ไม่มี gap ก็เลื่อนขั้นได้).
- **API-18 succession (FIX-09):** เมื่อ decision=ผ่าน หรือ weighted_score≥4 → emit `perf.result.succession_candidate` payload `{ appraisal_id, employee_ref }`.
**Response 200:** `{ "dispatched":true, "event":"perf.result.movement_requested" }`
**Errors:** 403 · 409 BR_CYCLE_CLOSED · 422 BR_GAP_REQUIRED (training).
**Side effects:** emit event (fire-and-forget); audit optional. **ไม่มี write ปลายทาง.**
**Calls (Logic):** F131-FN-10 dispatchTraining / F131-FN-11 dispatchMovement / F131-FN-12 dispatchSuccession.

---

### F131-API-19: GET /reports/distribution
| Field | Value |
|---|---|
| summary | การกระจายคะแนน (FN-13) — buckets ต่ำ/ปานกลาง/ดี/ดีเยี่ยม |
| auth | required (scoped · masked aggregate) |

**Query:** `cycle_id` (or `all`).
**Response 200:** `{ "total":6, "published":2, "pip":1, "buckets":{ "ต่ำ (<3.0)":0, "ปานกลาง (3.0–3.9)":1, "ดี (4.0–4.5)":2, "ดีเยี่ยม (>4.5)":1 } }`
> aggregate นับเฉพาะ appraisal ที่ role เห็น (scope) — masking ไม่รั่วผ่าน count.
**Calls (Logic):** F131-FN-15 buildDistributionReport → FN-17 (scope).

---

> **API-01/03/07/13/15** (list cycles / cycle detail / appraisal detail / pip / reminder): contract straightforward — GET reads (FN-14 scope), POST /pip (F131-FN-08, validate gap non-empty, manage-only, audit "เปิดแผน PIP · {duration}"), POST /reminder (F131-FN-13, toast "ส่งการเตือน…"). Guard cascade + errors ตาม pattern เดียวกับข้างบน.

---

## §2.3 Common Concerns

### Idempotency (PR-7 · FN-92)
ทุก mutation POST/PUT รับ `Idempotency-Key` — cache 24h. โปรโตไทป์ใช้ `state._busy` กัน double-submit (audit เกิด entry เดียว); server mirror ด้วย idempotency key + optimistic `version`.

### Optimistic Locking (PR-1 · EC-05)
PUT/POST mutation ใช้ `version` (T_perf_appraisal/T_perf_cycle) → mismatch = 409 ERR_STALE_DATA. `[AI-DEFAULT]` optimistic first-write-wins (OQ-PERF-09).

### Multi-Tenant
`X-Tenant-Id` middleware + PostgreSQL RLS ทุก endpoint.

### RESTRICTED scope/mask (BR-08/BR-11 · FN-94)
ทุก read endpoint ผ่าน F131-FN-17 applyScopeAndMask **ก่อน** ส่ง response — out-of-scope rows/columns ไม่อยู่ใน payload (ไม่ใช่แค่ UI hide).

### Audit (BR-09 · FN-93)
ทุก mutation → T_perf_audit append-only (who+at+act). Immutable (no UPDATE/DELETE).

---

## §2.4 API → Logic Trace (Anchor for R8)

| API | Calls Functions | Calls Engines |
|---|---|---|
| API-01 GET /cycles | FN-14 | — |
| API-02 POST /cycles | FN-01 | ENG-NOTIFY |
| API-03 GET /cycles/:id | FN-14 | — |
| API-04 POST /cycles/:id/close | FN-02 | — |
| API-05 GET /config/appraisal-cycles | — (proxy) | — |
| API-06 GET /appraisals | FN-14, FN-17 | — |
| API-07 GET /appraisals/:id | FN-14, FN-17 | — |
| API-08 PUT /kpis | FN-03, FN-16, FN-18 | — |
| API-09 POST /self | FN-04, FN-16, FN-18 | — |
| API-10 POST /manager-review | FN-05, FN-19, FN-16, FN-18 | — |
| API-11 POST /calibration/send | FN-06, FN-16, FN-18 | ENG-DOA |
| API-12 POST /calibration/stage | FN-07, FN-16, FN-18 | ENG-CSQ, ENG-NOTIFY |
| API-13 POST /pip | FN-08, FN-16, FN-18 | — |
| API-14 POST /reopen | FN-09, FN-16, FN-18 | — |
| API-15 POST /reminder | FN-13 | ENG-NOTIFY |
| API-16 POST /dispatch/training | FN-10 | — (event) |
| API-17 POST /dispatch/movement | FN-11 | — (event) |
| API-18 POST /dispatch/succession | FN-12 | — (event) |
| API-19 GET /reports/distribution | FN-15, FN-17, FN-20 | ENG-GRADE (grade-mapper) |

> **R8 Check:** ทุก mutation row มี ≥1 Function/Engine ✅ (verified 03_LOGIC §3.3).

---

## §2.X Cross-Module Contract ⭐ (จาก BRD §12.1 Downstream Impact Map)

> ปลายทางยังไม่ build (soft-ref · OQ-PERF-07) — **freeze payload contract ที่นี่**.

| Downstream | รูปแบบ | Contract (event/endpoint) | Trigger | Payload หลัก | Compensating |
|---|---|---|---|---|---|
| **Movement (F-HR-MOVE)** | Event | `perf.result.movement_requested` | publish + API-17 | `{ appraisal_id, employee_ref, decision, weighted_score, cycle_id }` | re-open (API-14) → ปลายทางยกเลิก/ส่ง event ใหม่ (ปลายทางจัดการ) |
| **Training** | Event/Hook | `perf.gap.training_requested` | มี gap + API-16 | `{ appraisal_id, employee_ref, gap }` | ส่ง gap ใหม่ตามผลที่แก้ |
| **Succession (F134)** | Event/Hook | `perf.result.succession_candidate` | decision ผ่าน/top + API-18 | `{ appraisal_id, employee_ref, weighted_score }` | re-evaluate candidacy |
| **ENG-CSQ (7C)** | Engine event | `perf.result.published` (SecC/DC) | per-person publish (API-12 isLast) | `{ appraisal_id, employee_ref, classification:'SecC', decision:'DC' }` | re-publish → CSQ ยิงซ้ำ per-person |
| **ENG-NOTIFY** | Engine event | `perf.cycle.opened` · `perf.deadline.overdue` · `perf.result.published` | ตาม trigger (ไม่นับ doa_*) | ตาม 03_NTF_BRIEF | notif ใหม่ตอน re-publish |
| **HR Config #107** | Endpoint (feature เรียก) | GET /config/appraisal-cycles (API-05) | สร้างรอบ | รับ config_ref + config_version | — (read-only) |

- ทุกแถวมี cross-module test → 06_TESTS §6.9 (XT-01..XT-05).
