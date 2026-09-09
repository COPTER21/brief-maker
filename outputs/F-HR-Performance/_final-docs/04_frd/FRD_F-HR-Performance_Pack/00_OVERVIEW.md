# 00_OVERVIEW — F131 Performance / ประเมินผลงาน

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA, Architect)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Open Questions + Coverage Manifest
> **Generated:** frd-generator-v6.1 · HTML-first (Recognize & Validate) + Lane Mode (no-ask)

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F131 |
| **Feature Name** | Performance / ประเมินผลงาน |
| **Feature Code** | F-HR-PERF |
| **Module** | HR |
| **Archetype** | master + cycle (แบบประเมิน/KPI master + รอบ cycle · **ไม่ใช่ Pattern Q document**) |
| **Variant** | **FULL** (9 files + INDEX) |
| **Status** | DRAFT (FRD) — pending BA/Architect review of OQ register |
| **FRD Version** | 1.0 (2026-09-09) |
| **Generator** | frd-generator-v6.1 (Design Authority · HTML-first) |
| **Source Brief** | — (WF-01 lane · no standalone Brief) — PREBRIEF.md + FUNCTION_CHECKLIST.html (18 FN) + STANDARD_BASELINE.md (MUST 10) |
| **Source BRD** | BRD_performance.md (status: **APPROVED**, 2026-09-09) |
| **Source HTML** | performance.html (gated: ux BLOCK=0 · coverage FN 18/18 · BA re-gate after fix order F131) |
| **Author** | tadswan@2bsimple.com (BA) |
| **Reviewers** | Strike (governance) · Architect (CSQ EC) · Tech Lead · QA Lead |

### Variant decision (fallback from BRD — no Brief)
`Variant = FULL` — pages=4, appraisal states=5 (goal→self→mgr→calibration→published) + cycle states=5 (draft→open→in_review→calibration→closed), approval=YES (staged DOA), money-adjacent=YES (Movement salary/promotion event), Engine Management=YES (BRD §13 Phase 4 ENG-CSQ). Rule: `states ≥ 4 OR (approval AND money) OR §9.5 Engine Management` → FULL.

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-09-09 | BA | Initial FRD from APPROVED BRD v2.0 + gated performance.html (post BA re-gate: CRITICAL 5 + HIGH 4 fixes live in HTML) |

---

## §0.3 Scope

### In Scope
- **รอบประเมิน (Cycle):** สร้างรอบจาก HR Config appraisal_cycle (#107) → เปิดกรอก · ปิดรอบ (ล็อกจริง)
- **แบบประเมินรายคน (Appraisal):** ตั้งเป้า/KPI (Σweight=100) · พนักงานประเมินตนเอง · หัวหน้าประเมิน + คะแนนถ่วงน้ำหนัก
- **สอบทาน (Calibration):** staged DOA slot picker (เลือกผู้สอบทานจริงต่อขั้น) + decision + team-calibration view
- **ผล & Gap:** เผยแพร่ผลรายคน (RESTRICTED) · ระบุ gap · เปิดแผน PIP · re-open ผลหลังเผยแพร่ (authorized)
- **ส่งต่อ (hook/event, display-only):** gap→Training · ผล→Movement event (ปรับเงินเดือน/ตำแหน่ง) · ผล→Succession
- **รายงาน:** การกระจายคะแนน (distribution) + filter รอบ/แผนก
- **ระบบ:** ค้นหา/filter + empty state · confirm ปิดรอบ · validate + กัน double-submit · audit append-only · masking RESTRICTED ตาม role · แจ้งเตือน 3 event

### Out of Scope (ตัดโดยมติ — ไม่ใช่ตกหล่น)
- **ปรับเงินเดือน/เลื่อนตำแหน่งเอง** — ส่ง event ให้ Movement (F-HR-MOVE) เท่านั้น [LK-2 · OB-3]
- **สร้าง/แก้รอบประเมิน-แบบฟอร์มกลาง** — อ่านจาก HR Configuration #107 เท่านั้น [LK-3]
- **สร้างหลักสูตรอบรม** — hook ส่งไป Training feature เท่านั้น [LK-5]
- **360 feedback / competency model / continuous check-in** — NICE, ไม่รองรับรอบนี้ [OQ-PERF-08]

### Out of Scope (from Phase 2.5 skipped/deferred probes)
- Concurrent staged-review lock policy (PR-1) → resolved with conservative default `[AI-DEFAULT]` (optimistic lock 409) — see 05_RULES EC-05 + OQ-PERF-09
- HR Config #107 missing appraisal_cycle → error-state default `[AI-DEFAULT]` — see 05_RULES EC-06

---

## §0.4 Roles & Responsibilities (COSO)

| Role | Person/Team | Responsibilities | scope_type (SEC) |
|---|---|---|---|
| **Maker** | HR/HRBP (`hr`, manage) · พนักงาน (`staff`) · หัวหน้า (`mgr`) | HR: สร้างรอบ/KPI · พนักงาน: ประเมินตนเอง · หัวหน้า: ประเมิน+คะแนน | HR=ALL · staff=SELF · mgr=DEPT |
| **Checker** | ผู้สอบทาน DOA ต่อขั้น | บันทึกผลสอบทานรายขั้น (staged) | resolved by ENG-DOA per position |
| **Approver** | ผู้สอบทานขั้นสุดท้าย (DOA) | เผยแพร่ผล + decision (ผ่าน/ไม่ผ่าน/ทบทวน) | last stage only |
| **Owner** | HR/HRBP (manage) | ปิดรอบ · re-open · ส่ง event ปลายทาง | ALL |

> **SoD:** Maker (หัวหน้าประเมิน) ≠ Approver (ผู้สอบทานขั้นสุดท้าย) — บังคับด้วย stage guard (คะแนน mgr ต้องครบ + สอบทานครบทุกขั้น ก่อน published). รายละเอียด touchpoints → `01_UI §1.4`.

---

## §0.5 Dependencies

### Upstream (this feature depends on)
| Dependency | Type | Source | Status |
|---|---|---|---|
| HR Configuration #107 (appraisal_cycle + KPI/form template + config_version) | Data / Config lookup | F-HR-CONFIG | ⚠️ soft-ref — ยังไม่ build (freeze payload contract ที่ 02_API §2.X) |
| Employee Master (emp/pos/dept snapshot) | Data | Employee Master feature | ⚠️ soft-ref |
| **ENG-DOA** (delegation-of-authority · staged calibration slot resolve) | Engine (existing) | CUBIC / F-DLG-001 | ⚠️ role-id chain รอ BA (CL-0013 · OQ-PERF-05) |
| **ENG-NOTIFY** (F-NOTIFY event catalog) | Engine (existing) | F-NOTIFY | ⚠️ wire 3 business events (ดู 03_NTF_BRIEF) |
| **ENG-CSQ** (7C compliance-sensitive queue) | Engine (existing) | CUBIC / ENG-CSQ | ⚠️ EC valuation รอ Architect (OQ-PERF-06) |

### Downstream (features that depend on this)
| Consumer | What it uses |
|---|---|
| Movement (F-HR-MOVE) | `perf.result.movement_requested` event (payload ผล → ปรับเงินเดือน/ตำแหน่ง) — ⚠️ soft-ref |
| Training | `perf.gap.training_requested` hook (gap payload) — ⚠️ soft-ref |
| Succession (F134) | `perf.result.succession_candidate` hook (top performer) — ba-done, soft-ref |
| ENG-CSQ (7C) | `perf.result.published` (SecC/DC) per-person publish |
| ENG-NOTIFY | 3 business events (รอบเปิด / ครบกำหนด / ผลเผยแพร่) |

### External
| Service | Purpose |
|---|---|
| — | ไม่มี 3rd-party external (ไม่มี payment/print/PDF) |

---

## §0.6 Stack & Architecture

| Layer | Technology |
|---|---|
| Frontend | vanilla JS single-file SPA (prototype) → React/Next equivalent (dev) · CI CUBE Warm Light · tab-based shell (4 tabs, no per-tab hash route) |
| API | Node.js / Strapi (HTTP layer only) |
| Database | PostgreSQL (RLS multi-tenant) |
| Engine layer | CUBIC Registry — integrates ENG-DOA / ENG-NOTIFY / ENG-CSQ (existing); declares 1 owned candidate (grade-mapper) |
| Auth | JWT + role-based (`sec.can` server-side mirror) |

---

## §0.7 Multi-Tenant & Security Context

- [x] Multi-tenant feature: **YES** (RLS by tenant)
- [x] PII data involved: **YES** — employee name/pos/dept snapshot (Confidential + PII); details in 04_DB §4.2 + §4.6
- [~] Financial data: **INDIRECT** — no salary CRUD here; salary/promotion adjustment is an **event to Movement** (LK-2). Scores are RESTRICTED performance data, not money.
- [x] Audit log required: **YES** — append-only (BR-09/BR-12)

**Security Bible domains applied:** D2 (Auth), D7 (PII), D9 (Audit), D13 (RBAC/scope), D-CLASS (Data Classification) — see 05_RULES §5.7. Preset **P6 (HR/PII Sensitive · 15 controls)**.

### §0.7.1 Data Classification Summary ⭐

Highest classification level ที่ feature นี้แตะ:
- [x] **Has Restricted fields** — คะแนน self/mgr · decision · gap (SecC · masking ตาม role) — ระบุใน 04_DB §4.2
- [x] Has Confidential fields — employee snapshot (name/pos/dept) + PII
- [x] Internal — status, timestamps, audit meta
- [ ] Public-facing data — none

**Linkage:** Restricted fields (score/decision/gap) → register ที่ Policy Center → Data Classification + Restricted Resources (ดู 04_DB §4.6.6). **Wire status = OPEN** (OQ-PERF-10).

---

## §0.8 Open Questions

> Carried from BRD §15 + BA fix-order §4 + Phase 2.5 probing. **ไม่เดา — ให้ owner เคาะ.**

| ID | Question | Blocking? | Owner | Impact (FRD section) |
|---|---|---|---|---|
| OQ-PERF-05 | **DOA chain executive role-ids (CL-0013)** — สายอนุมัติสอบทานปลายทางใช้ role-id ไหน | NO (feature ประกาศ slot เท่านั้น ไม่ hardcode) | BA (ที่ config) | 03_LOGIC §3.2 ENG-DOA · 03_DOA_BRIEF |
| OQ-PERF-06 | **CSQ EC valuation** — มูลค่า EC ของ perf.result.published คิดยังไง + ท่อ 7C detail | NO (event ยิงถูกจุดแล้ว) | Architect | 03_LOGIC §3.2 ENG-CSQ · §Integration · 03_CSQ_BRIEF |
| OQ-PERF-07 | soft-ref ปลายทางยังไม่ build (HR Config #107 · Movement F-HR-MOVE · Employee Master · Succession F134 · ENG-DOA/NOTIFY/CSQ) — freeze payload contract | NO (contract frozen ที่ 02_API §2.X) | PM | 02_API §2.X Cross-Module Contract |
| OQ-PERF-08 | 360 feedback / competency model / continuous check-in — NICE, wave ถัดไปหรือถาวรตัด | NO | Strike | Scope (out) |
| OQ-PERF-09 | Concurrent staged-review — 2 ผู้สอบทานบันทึกพร้อมกัน · lock/last-write policy | NO `[AI-DEFAULT]` optimistic 409 | Architect | 05_RULES EC-05 |
| OQ-PERF-10 | Restricted fields wire กับ Restricted Resources registry (Policy Center) เสร็จหรือยัง | NO | Security/Policy Center | 04_DB §4.6.6 · 05_RULES D-CLASS |
| OQ-PERF-11 | Mock-data gap (R8-awareness · **spec-level, ไม่แก้ HTML**): mgr persona dept=ฝ่ายผลิต แต่ mock appraisal ขั้น mgr (อรทัย A3) = ฝ่ายบัญชี → หัวหน้าเข้าไม่ถึงผ่าน UI dept-scoped · **แนะนำเพิ่ม mock ขั้น mgr ในฝ่ายผลิต** เพื่อสาธิต manager-review ในขอบเขต | NO (demo/QA note) | BA/QA | 06_TESTS §6.3 |

> Resolved OQ (from BRD/PM/BA) → 07_LOCKED §7.1 (LD-01..LD-08).

---

## §0.9 Glossary

| Term | Definition |
|---|---|
| Cycle (รอบประเมิน) | รอบประเมินผลตามช่วงเวลา — header, อ้าง config_version จาก HR Config #107 |
| Appraisal (แบบประเมินรายคน) | แบบประเมิน 1 คน × 1 รอบ — snapshot emp/pos/dept ณ รอบ |
| KPI line | รายการ KPI ต่อ appraisal (น้ำหนัก·เป้า·คะแนน self·คะแนน mgr) |
| Calibration (สอบทาน) | ขั้นสอบทานผ่าน DOA — staged, เลือกผู้สอบทานจริงต่อขั้น |
| Staged DOA | สอบทานแบ่งเป็นขั้น (send=freeze รายชื่อ → per-stage record → publish บนขั้นสุดท้าย) |
| Weighted score (wsum/rawScore) | คะแนนรวมถ่วงน้ำหนัก = Σ(mgrScore×weight)/Σweight |
| RESTRICTED (SecC) | ข้อมูลลับต่อบุคคล — masking ตาม role scope |
| CSQ 7C | Compliance-Sensitive Queue — ยิง event `perf.result.published` per-person ตอนเผยแพร่ |
| scope_type | ระดับการเห็น: SELF (staff) / DEPT (mgr เฉพาะแผนกตน) / ALL (HR) |
| PIP | Performance Improvement Plan — แผนพัฒนา เมื่อ decision "ทบทวน" |

---

## §0.10 Pack Navigation

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW.md | All | This file — meta + scope + coverage manifest |
| 01_UI.md | FE dev | Layout Decision Log + Pages (4 tabs) + Journey |
| 02_API.md | BE dev (HTTP) | 19 API contracts + Cross-Module Contract |
| 03_LOGIC.md | BE dev (logic) | Functions + Engines (ENG-DOA/NOTIFY/CSQ) + Trace |
| 04_DB.md | DBA / BE | 5 tables + Data Classification |
| 05_RULES.md | BE + QA | BR + guards + Edge Cases + Errors + Security |
| 06_TESTS.md | QA | AC per FN + DoD + cross-module cases |
| 07_LOCKED_DECISIONS.md | All | §7.0 Scope Lock + LD-01..08 |
| INDEX.md | All | Cross-reference + R8 matrix + quick nav |

---

## §0.11 Scope Lock
> FULL variant → อยู่ที่ **07_LOCKED §7.0** (imported ครบ LK-1..LK-6). Ref: BRD §3.4 (สืบทอดจากใบเซ็น current-state §3 · fix order · F-HR-MOVE OB-3).

---

## §0.12 Coverage Manifest ⭐ (กัน requirement หล่น BRD→FRD)

> ทุก FN (18) + Story (BRD §7) + Rule (§9) + Edge confirmed (§10.1) มีแถว — ไม่มีที่ลง = OQ.

| BRD/FN Ref | Requirement (ย่อ) | อยู่ที่ใน Pack |
|---|---|---|
| FN-01 · S-01 · BR-01 | สร้างรอบจาก HR Config → เปิดกรอก | 01_UI P-01 · 02_API-02 (+API-05 lookup) · 03_FN-01 · 05_RULES BR-01 · 06 AC-01 |
| FN-11 · S-10 · BR-09 | ปิดรอบ (ล็อกแก้จริง) | 01_UI P-01 · 02_API-04 · 03_FN-02 · 05_RULES BR-09/SM · 06 AC-02 |
| FN-02 · S-02 · BR-02 | ตั้งเป้า/KPI Σweight=100 | 01_UI P-02 · 02_API-08 · 03_FN-03 · 05_RULES BR-02/VR-01 · 06 AC-03 |
| FN-03 · S-03 · BR-03 | พนักงานประเมินตนเอง | 01_UI P-02 · 02_API-09 · 03_FN-04 · 05_RULES BR-03 · 06 AC-04 |
| FN-04 · S-04 · BR-04 | หัวหน้าประเมิน + weighted | 01_UI P-02 · 02_API-10 · 03_FN-05 · 05_RULES BR-04 · 06 AC-05 |
| FN-09 · S-08 · BR-09 | ประเมินไม่ครบ/overdue → เตือน | 01_UI P-02 · 02_API-15 · 03_FN-13 · 05_RULES BR-09 · 06 AC-06 |
| FN-05 · S-05 · BR-05 | สอบทาน + decision | 01_UI P-03 · 02_API-12 · 03_FN-07 · 05_RULES BR-05/SM · 06 AC-07 |
| FN-08 · S-05 · BR-05 | สอบทานผ่าน DOA slot picker (ไม่ hardcode, staged) | 01_UI P-03 · 02_API-11+12 · 03_FN-06+07 · ENG-DOA · 05_RULES BR-05 · 06 AC-08 |
| FN-06 · S-06 · BR-06 | gap → Training hook | 01_UI P-03 · 02_API-16 · 03_FN-10 · 05_RULES BR-06 · 06 AC-09 · XT-02 |
| FN-07 · S-07 · BR-07 | ผล → Movement event | 01_UI P-03 · 02_API-17 · 03_FN-11 · 05_RULES BR-07 · 06 AC-10 · XT-01 |
| FN-10 · S-09 · BR-05 | คะแนนต่ำ/ทบทวน → PIP | 01_UI P-03 · 02_API-13 · 03_FN-08 · 05_RULES BR-05 · 06 AC-11 |
| FN-12 · S-11 · BR-08 | แจ้งเตือน 3 event | 01_UI §1.5 · 02_API (side-effect) · 03_FN-07 (notify) · ENG-NOTIFY · 06 AC-12 |
| FN-13 · S-12 · BR-08 | รายงาน distribution + filter | 01_UI P-04 · 02_API-19 · 03_FN-15 · 06 AC-13 |
| FN-90 | ค้นหา/filter + empty state | 01_UI P-02 · 02_API-06 · 03_FN-14 · 06 AC-14 |
| FN-91 | ปิด/ยกเลิกผ่าน confirm + soft archive | 01_UI P-01 (closeCycle modal) · 02_API-04 · 05_RULES SM · 06 AC-02 |
| FN-92 | validate + กัน double-submit | 05_RULES VR-06 (`_busy`) · 02_API §2.3 idempotency · 06 AC-15 |
| FN-93 | audit append-only ทุก create/แก้/สอบทาน | 03_FN-16 pushAudit · 04_DB T_perf_audit · 05_RULES BR-09 · 06 AC-16 |
| FN-94 | ปิดบังผลประเมิน (RESTRICTED) ตาม role | 03_FN-17 applyScopeAndMask · 04_DB §4.6 · 05_RULES BR-08/BR-11/D-CLASS · 06 AC-17 |
| §7 OQ-PERF-01 (resolved) | re-open published (authorized + reason + audit) | 01_UI P-03 · 02_API-14 · 03_FN-09 · 05_RULES BR-12 · 06 AC-18 |
| §10.1 (BA fixes FIX-01..06) | guard cascade (closed→role→stage→scope) + staged DOA | 03_FN-18 guardMutation · 05_RULES §5.5 EC-01..04 · 06 AC-19 |

**สรุป:** FN 18/18 ✅ · Stories 12/12 ✅ · BR 13/13 ✅ · Edges (§10.1 confirmed) 10/10 ✅ · ไม่มี requirement ที่ไม่มีที่ลง → OQ ที่เหลือเป็น downstream/config (OQ-PERF-05..11), ไม่ block FRD.
