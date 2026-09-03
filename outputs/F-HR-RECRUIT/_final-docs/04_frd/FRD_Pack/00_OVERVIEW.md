# 00_OVERVIEW — F-HR-RECRUIT (F127) สรรหา / Recruit · Candidate Pool

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Coverage Manifest + Open Questions

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-HR-RECRUIT (Feature Code: F127) |
| **Feature Name** | สรรหา (Recruit / Candidate Pool) |
| **Module** | HR · Wave W9 |
| **Archetype** | master (requisition/candidate) + pipeline board (Pattern L kanban) |
| **Variant** | **FULL** (9 files + INDEX) |
| **Status** | DRAFT (FRD generated · awaiting review) |
| **FRD Version** | 1.0 (2026-09-03) |
| **Generator** | frd-generator-v6 (v6.1 · HTML-first · Lane Mode) |
| **Source Brief** | PREBRIEF.md + FUNCTION_CHECKLIST.html (21 FN) + STANDARD_BASELINE.md (MUST 12) |
| **Source BRD** | BRD_สรรหา.md (status: **APPROVED** with OQ-15/16/17, 2026-09-03) |
| **Source HTML** | สรรหา.html (ผ่าน ux gate PASS 0 BLOCK + coverage gate PASS FN 21/21 + REVIEW_FIX_ORDER FIX-01..07) |
| **Author** | BA (bird@2bsimple.com) |
| **Reviewers** | Tech Lead · PM · QA Lead · Strike (integration/PDPA) |

**Variant decision (Fallback from BRD):** `Variant = FULL` — pages=4 main+drawer(4 tabs)+6 modals, **states ≥ 4** (Requisition 6 · Candidate pipeline 8 · Offer 5), approval=YES (DOA req+offer), money=band in-range check + funnel calc → rule `states ≥ 4 OR (approval AND money)` ⇒ FULL.

**HTML mode:** Mode A — **Recognize & Validate** (HTML ผ่าน gate = de facto layout; FRD สกัด+ตรวจ+บันทึก · ไม่เขียน spec สวนจอ · R14 HTML Fidelity).

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-09-03 | BA | Initial FRD generation (FULL) via frd-generator-v6 · HTML-first จาก สรรหา.html · Lane Mode (Phase 2.5 no-ask, `[AI-DEFAULT]` tagged) |

---

## §0.3 Scope

### In Scope
- เปิดอัตรา (requisition): ตำแหน่ง · จำนวน · ระดับ (grade) · ช่วงเงินเดือน (band soft-ref) · hiring manager · manpower_ref (hook nullable)
- ส่งอนุมัติเปิดอัตรา + ข้อเสนอจ้าง ผ่าน **DOA slot picker** (ตามตำแหน่ง · ไม่ผูกวงเงิน · resolve runtime)
- ประกาศรับ (ภายใน) · ปิดอัตรา (รับครบ auto / ยกเลิก confirm)
- คลังผู้สมัคร: เพิ่ม/แก้ผู้สมัคร · ผูก application กับอัตรา · **consent PDPA gate** · ตรวจซ้ำ email/phone (เตือน)
- บอร์ดสรรหา (kanban): เลื่อนสถานะ คัดกรอง→สัมภาษณ์→ข้อเสนอ→รับ + เส้นแยก (rejected/withdrawn/talent_pool)
- นัดสัมภาษณ์ + NTF ผู้สัมภาษณ์/ผู้สมัคร · ประเมิน scorecard (ต่อผู้สัมภาษณ์ · snapshot)
- ออกข้อเสนอจ้าง (เงินตามระดับ + **freeze band version_id**) → DOA → เสนอ → ตอบรับ/ปฏิเสธ
- รับ (hired) → **ยิง event handoff เข้า On/Offboard** (soft-linkage · ไม่สร้าง employee)
- รายงาน funnel / time-to-hire + filter · Export CSV (stub → dev)
- กติกากลาง: ค้นหา/filter + empty state · confirm + soft archive · validate + กัน double-submit · audit append-only · masking RESTRICTED/PDPA ตาม role · viewer read-only guard

### Out of Scope (จาก FUNCTION_CHECKLIST §unsupported — 5 ข้อ · Scope Lock R11)
- **จ้างจริง / สร้าง employee record / สัญญาจ้าง** — On/Offboard เป็นเจ้าภาพ (LOCK-OB1) · Recruit ส่ง handoff เท่านั้น
- **ประกาศงานบน job board ภายนอก** — external integration (hook)
- **แบบทดสอบ/assessment · sourcing agency** — NICE, ไม่รองรับ
- **offer letter PDF เลขรัน** — soft-ref รอบนี้ (ไม่มี doccfg/pdfdoc)
- **สร้าง/แก้ระดับ-band เงินเดือน** — อ่าน HR Configuration (#107) เท่านั้น, ไม่ CRUD

### Out of Scope (mark from Phase 2.5 skipped probes)
- ไม่มี probe ถูก skip — Lane Mode ตอบทุก probe ด้วย conservative default + `[AI-DEFAULT]` (ดู §0.8 + 05_RULES §5.5)

---

## §0.4 Roles & Responsibilities (COSO)

| Role | Person/Team | Responsibilities |
|---|---|---|
| **Maker** | เจ้าหน้าที่สรรหา (recruiter) | สร้าง req/candidate/offer · ส่งอนุมัติ · เลื่อนสถานะ · นัดสัมภาษณ์ · รับเข้าทำงาน |
| **Checker** | Hiring Manager | review pipeline · ประเมิน scorecard · co-sign hire/move |
| **Approver** | ผู้จัดการสายงาน / หัวหน้าฝ่ายสรรหา (DOA slot) | อนุมัติเปิดอัตรา + ข้อเสนอจ้าง (resolve จาก Policy Center) |
| **Owner** | HR สรรหา | monitor funnel/time-to-hire · maintain pool |
| **Viewer** | ผู้ชมทั่วไป | read-only (mask RESTRICTED · ไม่มี mutation) |

> **SoD:** Maker (recruiter สร้าง req/offer) ≠ Approver (manager) ในทุก approval step. รายละเอียด workflow → `01_UI §1.3 Journey` + `01_UI §1.4 COSO Touchpoints`.

---

## §0.5 Dependencies

### Upstream (this feature depends on)
| Dependency | Type | Source |
|---|---|---|
| Salary Structure (band resolve) | External API (read) | `GET /api/v1/salary-structure/bands/resolve` — คืน band + `version_id` · **freeze snapshot** คู่ offer |
| Employee Master (ผู้สัมภาษณ์ · hiring manager) | External API (read/snapshot) | `GET /api/v1/employees?status=active` |
| Policy Center — DOA (F-DLG-001) | External resolve (runtime) | สายอนุมัติ req/offer slot · **ไม่ hardcode** |
| Policy Center — PDPA retention config | External config (read) | ระยะเก็บผู้สมัคร → `retentionLabel()` display-only · **OQ-16** |
| Notification (ENG-NOTIFY / F-NOTIFY) | Event sink | interview_scheduled · offer_sent · selection_result · candidate_accepted |
| Manpower Planning (F124) | Hook (nullable) | `manpower_ref` display-only — **F124 ยังไม่ dev** · null = ไม่บังคับ |

### Downstream (features that depend on this)
| Consumer | What it uses |
|---|---|
| On/Offboard (F-HR-ONBOARD) | รับ event `recruit.candidate.hired` (id, position, start_date, offer snapshot) — **OQ-15 ฝั่งรับยังไม่ออกแบบ** · ปัจจุบัน fire-and-forget |
| HR Dashboard | funnel / time-to-hire metrics (ENG-RCT-01) |

### External
| Service | Purpose |
|---|---|
| ENG-NOTIFY (Notification Center) | ส่ง event แจ้งเตือน (wire ผ่าน ntf-declaration) |
| Policy Center | DOA chain resolve + Data Classification + PDPA retention |

---

## §0.6 Stack & Architecture

| Layer | Technology |
|---|---|
| Frontend | vanilla JS single-file SPA (prototype) → React/Next.js (prod) · CI CUBE Warm Light |
| API | Node.js / Strapi (HTTP layer — 02_API) |
| Database | PostgreSQL (RLS multi-tenant) |
| Engine layer | CUBIC Registry (ENG-RCT-01 funnel · ENG-RCT-02 duplicate-matcher) |
| Auth | JWT + role-based (recruiter/manager/viewer) |
| Integration | Salary Structure API · Employee Master API · Policy Center (DOA/PDPA) · ENG-NOTIFY |

---

## §0.7 Multi-Tenant & Security Context

- [x] Multi-tenant feature: **YES** (RLS)
- [x] PII data involved: **YES** — ข้อมูลผู้สมัคร (ชื่อ/ติดต่อ/resume) · ดูรายละเอียดต่อ field ใน 04_DB §4.2 + §4.6
- [ ] Financial data: partial — band/เงินเดือน = read snapshot (ไม่ใช่ payroll)
- [x] Audit log required: **YES** — append-only ทุก create/แก้/เลื่อน/อนุมัติ

**Security Bible domains applied:** D2 (Auth), D7 (PII/PDPA), D9 (Audit), D15 (Admin/approval), D17 (Multi-tenant) — see 05_RULES §5.7. Security Preset = **P6 (HR / PII Sensitive)**.

### §0.7.1 Data Classification Summary ⭐

Highest classification level ที่ feature นี้แตะ:
- [x] **Has Restricted fields** — ผู้สมัคร: `name`, `contact`, `resume` = **Restricted + PII** (ระบุใน 04_DB §4.2)
- [x] Has Confidential fields — offer.salary, scorecard.score
- [ ] Internal only
- [ ] Public-facing data

**Linkage:** Restricted fields (candidate PII) ต้อง register ที่ Policy Center → Data Classification + **Restricted Resources registry** (ดู 04_DB §4.6.6) · PII fields → PDPA consent scope. **Open Question: wire Restricted Resources ยัง — ดู OQ-R1 §0.8.**

---

## §0.8 Open Questions

| ID | Question | Blocking? | Owner |
|---|---|---|---|
| **OQ-15** | Inbound handoff: hired → สร้าง Employee + เปิด On/Offboard จริงอย่างไร? ปัจจุบัน soft-linkage ยิง event `recruit.candidate.hired` อย่างเดียว (fire-and-forget · comment stub ในโค้ด) — ต้องออกแบบฝั่งรับ + ack. **FRD กัน scope นี้: ไม่ระบุ endpoint ปลายทาง, ไม่ทำ ack, ไม่ retry** (ดู 02_API §2.X Cross-Module + 03_LOGIC hireCandidate) | **NO** (event ออกฝั่งเราเสร็จ · ฝั่งรับ = integration phase) | Strike (F-HR-ONBOARD) |
| **OQ-16** | PDPA retention ผู้สมัคร: ระยะเก็บกี่เดือน/ปี? ครบกำหนด ลบ/anonymize? Talent Pool ต่ออายุ consent อย่างไร? **withdraw consent** แล้วข้อมูลที่เก็บทำอย่างไร? — เป็น config ที่ Policy Center · **ห้าม hardcode ระยะ**. FRD: `retention_until` = display-only อ่านจาก Policy Center (`retentionLabel()`), retention/withdraw logic **ยังไม่ออกแบบ** จนกว่าเคาะ | **NO** สำหรับ launch UI · **YES** สำหรับ retention/withdraw job (Phase 4) | Strike / พี่เบิร์ด |
| **OQ-17** | req ถูกปิด (closed/cancelled) ขณะมีผู้สมัครค้าง pipeline → พฤติกรรม? (Edge 10.2 ST) — FRD ตั้ง conservative default `[AI-DEFAULT]`: pipeline ค้างไม่ถูกยกเลิกอัตโนมัติ, req.close บล็อกด้วย warn ถ้ามี active candidate (ยกเว้น cancel มี override + เหตุผล) | **NO** | BA / HR |
| **OQ-R1** | Restricted Resources wiring — candidate PII (Restricted) ต้อง register ACL per-record ที่ Policy Center Restricted Resources หรือยัง? รอบนี้ enforce ผ่าน role masking (recruiter unmask / manager·viewer mask) — ยังไม่ผูก per-person ACL | NO | Security / Strike |
| **OQ-D1** `[AI-DEFAULT]` | PR-1 concurrent stage move — 2 recruiter เลื่อนผู้สมัครคนเดียวกัน → default **optimistic lock (409 ERR_STALE_DATA)** + audit ทั้งคู่ | NO | BA confirm |
| **OQ-D2** `[AI-DEFAULT]` | PR-7 idempotency — mutation ต้องมี `Idempotency-Key` (create req/candidate/offer, submit approval, hire) | NO | BA confirm |
| **OQ-D3** `[AI-DEFAULT]` | PR-3 permission revoked mid-drawer (recruiter→viewer ระหว่างเปิด drawer) → re-guard `viewerRO()` ตอน submit (มีบนจอแล้ว 15 จุด) | NO | BA confirm |
| **OQ-D4** `[AI-DEFAULT]` | EM — ยิง NTF ล้มเหลว → queue/retry ผ่าน ENG-NOTIFY (ไม่บล็อก business transition) | NO | BA confirm |

> Resolved questions → move to 07_LOCKED_DECISIONS §7.3 as LD-NN.

---

## §0.9 Glossary

| Term | Definition |
|---|---|
| Requisition (อัตรา) | คำขอเปิดตำแหน่งงาน — ต้นทางการสรรหา |
| Candidate (ผู้สมัคร) | บุคคลในคลังสรรหา — ข้อมูล **RESTRICTED + PDPA** |
| Offer (ข้อเสนอ) | ข้อเสนอจ้าง 1:1 ต่อผู้สมัคร — freeze band version |
| Band | ช่วงเงินเดือนต่อ grade (min/mid/max) — อ่านจาก Salary Structure |
| version_id (band) | เวอร์ชัน band ที่ freeze ณ สร้าง offer (เช่น SS-2569-03) |
| DOA | Delegation of Authority — สายอนุมัติ slot-based จาก Policy Center (F-DLG-001) · ไม่ผูกวงเงินใน feature นี้ |
| Handoff | event ส่งผู้สมัครที่ hired เข้า On/Offboard (soft-linkage · ไม่สร้าง employee) |
| Talent Pool | ผู้สมัครไม่ผ่าน/ถอน ที่ soft-archive เก็บไว้ |
| Manpower hook | อ้าง F124 (ยังไม่มีจริง) — display-only, nullable |

---

## §0.10 Pack Navigation

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW.md | All | This file — meta + scope + Coverage Manifest |
| 01_UI.md | FE dev | Layout Decision Log + Pages + Journey |
| 02_API.md | BE dev (HTTP) | API contracts + Cross-Module Contract |
| 03_LOGIC.md | BE dev (logic) | Functions + Engines + Trace |
| 04_DB.md | DBA / BE | Tables + Fields + Classification |
| 05_RULES.md | BE + QA | Business Rules + Edge Cases + Errors + Security |
| 06_TESTS.md | QA | Acceptance + DoD + Cross-Module |
| 07_LOCKED_DECISIONS.md | All | Scope Lock §7.0 + LDs |
| INDEX.md | All | Cross-reference quick nav |

---

## §0.11 Scope Lock (pointer)
> FULL variant → Scope Lock อยู่ที่ **07_LOCKED_DECISIONS §7.0** (imported จาก BRD §3.4, immutable). Scope Lock Ref: LANE_BRIEF F-HR-RECRUIT + current-state §3 (DOA slot picker 2026-08-17).

---

## §0.12 Coverage Manifest ⭐ (กัน requirement หล่น BRD→FRD · FN 21/21)

> ทุก FN (FUNCTION_CHECKLIST) + Story (BRD §7) + Rule (§9) + Edge confirmed (§10) มีแถว — ไม่มีที่ลง = Open Question.

### FN Coverage (21/21 — Lane ledger)

| FN | ต้องทำได้ | Story | อยู่ที่ใน Pack |
|---|---|---|---|
| FN-01 | เปิดอัตรา | US-01 | 01_UI P-01/M-01 · 02_API-02 · 03_FN-01 createRequisition · 04_DB T_recruit_requisition · 05 BR-01/VR-01 · 06 AT-01 |
| FN-02 | เปิดอัตราไม่มี Manpower → เตือนทำได้ (hook) | US-02 | 01_UI M-01 · 02_API-02 · 03_FN-01 · 05 BR-08 · 06 AT-02 |
| FN-03 | เพิ่มผู้สมัคร (ชื่อ·ติดต่อ·resume·ตำแหน่ง) | US-03 | 01_UI P-02/M-02 · 02_API-10 · 03_FN-08 createCandidate · 04_DB T_recruit_candidate · 05 VR-01 · 06 AT-05 |
| FN-04 | ผูกผู้สมัครกับอัตรา (application) | US-03 | 01_UI M-02 (cand_req combobox) · 02_API-10/12 · 03_FN-08/10 · 04_DB candidate.req_id · 06 AT-06 |
| FN-05 | consent PDPA — ไม่ยินยอม = ดำเนินต่อไม่ได้ | US-03 | 01_UI M-02/D-01 · 02_API-13 · 03_FN-11 setCandidateConsent + FN-12 moveCandidateStage guard · 05 BR-02/EC-01 · 06 AT-07/AT-11 |
| FN-06 | เลื่อนสถานะใน pipeline board | US-04 | 01_UI P-03 · 02_API-14 · 03_FN-12 moveCandidateStage · 05 §5.2 state machine/BR-03 · 06 AT-10 |
| FN-07 | นัดสัมภาษณ์ + แจ้งเตือน | US-05 | 01_UI D-01(assess)/M-04 · 02_API-15 · 03_FN-13 scheduleInterview · 04_DB T_recruit_interview · 05 BR-09 · 06 AT-12 |
| FN-08 | ส่งอนุมัติ (req/offer) ผ่าน DOA slot picker | US-01/US-07 | 01_UI M-03 · 02_API-05/06/18/19 · 03_FN-03/04/16/17 · 05 VR-04/BR-01/BR-04 · 06 AT-03/AT-15 |
| FN-09 | ประเมิน scorecard ต่อผู้สัมภาษณ์ | US-06 | 01_UI D-01(assess) · 02_API-16 · 03_FN-14 saveScorecard · 04_DB T_recruit_scorecard · 06 AT-13 |
| FN-10 | สร้างข้อเสนอ (เงินตามระดับ·วันเริ่ม) → ส่งอนุมัติ | US-07 | 01_UI D-01(offer) · 02_API-17 · 03_FN-15 createOffer (band freeze) · 04_DB T_recruit_offer · 05 BR-04/BR-09/VR-03 · 06 AT-14 |
| FN-11 | ตอบรับ → hired → ส่ง On/Offboard (ไม่ทำเอง) | US-08 | 01_UI M-06 · 02_API-21/22 + §2.X Cross-Module · 03_FN-18 respondOffer + FN-19 hireCandidate · 05 BR-05/§5.2 · 06 AT-16 + XT-01 · **OQ-15** |
| FN-12 | ปฏิเสธ/ถอนตัว (บันทึกเหตุ) | US-09 | 01_UI M-05 · 02_API-23 · 03_FN-20 terminateCandidate · 05 §5.2/BR-07 · 06 AT-17 |
| FN-13 | ไม่ผ่าน (เหตุ) → เก็บ talent pool | US-09 | 01_UI M-05 · 02_API-23 · 03_FN-20 · 05 BR-07 · 06 AT-18 |
| FN-14 | ตรวจซ้ำ email/phone → เตือน (ไม่บล็อก) | US-10 | 01_UI M-02 (live note) · 02_API-10 · 03_FN-09 detectDuplicate + ENG-RCT-02 · 05 BR-10/EC-02 · 06 AT-08 |
| FN-15 | รายงาน funnel/time-to-hire + filter | US-11 | 01_UI P-04 · 02_API-24/25 · 03_FN-22 buildFunnelReport + ENG-RCT-01 · 06 AT-19 |
| FN-16 | ปิดอัตรา (รับครบ/ยกเลิก) | US-12 | 01_UI P-01/M(confirm) · 02_API-08 · 03_FN-07 closeRequisition · 05 §5.2/BR-07 · 06 AT-04 · **OQ-17** |
| FN-90 | ค้นหา/filter list + empty state | — | 01_UI P-01/P-02 §1.6 · 02_API-01/09 (query) · 03_FN-05/06 buildListQuery · 06 AT-20 |
| FN-91 | ปิด/ยกเลิกผ่าน confirm + soft archive | — | 01_UI M-05/M(confirm) · 02_API-08/23 · 03_FN-07/20 · 05 BR-07 · 06 AT-04/AT-17 |
| FN-92 | field validate + กัน double-submit | — | 01_UI §1.6 · 02_API validation blocks · 03 (markInvalidFields note) · 05 VR-01/VR-02 · 06 AT-21 |
| FN-93 | audit ทุก create/แก้/เลื่อน/อนุมัติ (append-only) | — | 02_API side-effects (all mutations) · 03_FN-21 appendAudit · 04_DB T_recruit_audit · 05 BR-03/BR-07/D9 · 06 AT-22 |
| FN-94 | ปิดบังข้อมูลผู้สมัคร RESTRICTED ตาม role | — | 01_UI §1.2 P-02 · 03_FN-23 maskCandidatePII · 04_DB §4.6 · 05 BR-06/D-CLASS · 06 AT-23 |

**FN สรุป: 21/21 ครอบครบ ✅** — ไม่มี FN หล่น · ไม่มีแถวที่ "อยู่ที่" ว่าง.

### Story / Rule / Edge Coverage

| BRD Ref | Requirement (ย่อ) | อยู่ที่ใน Pack |
|---|---|---|
| §7 US-01..12 | User stories | map ครบใน FN table ด้านบน (คอลัมน์ Story) |
| §9 BR-01 | req อนุมัติ DOA ก่อนประกาศ | 05_RULES BR-01 · §5.2 · 06 AT-03 |
| §9 BR-02 | consent PDPA + retention ก่อนเก็บ/ดำเนิน | 05_RULES BR-02 · EC-01 · 06 AT-07/AT-11 |
| §9 BR-03 | pipeline transition audit | 05_RULES BR-03 · 03_FN-21 · 06 AT-22 |
| §9 BR-04 | offer อนุมัติ DOA + เงินตามระดับ | 05_RULES BR-04 · 06 AT-14/AT-15 |
| §9 BR-05 | hired → handoff event (ไม่สร้าง employee) | 05_RULES BR-05 · 02 §2.X · 06 XT-01 |
| §9 BR-06 | ผู้สมัคร RESTRICTED masking + PDPA | 05_RULES BR-06/D-CLASS · 04_DB §4.6 · 06 AT-23 |
| §9 BR-07 | audit append-only + soft archive | 05_RULES BR-07 · 04_DB §4.7 · 06 AT-22 |
| §9 BR-08 | Manpower hook · null ไม่บังคับ | 05_RULES BR-08 · 06 AT-02 |
| §9 BR-09 | snapshot ผู้สัมภาษณ์ + band version freeze | 05_RULES BR-09 · 03_FN-13/FN-15 · 06 AT-14 |
| §9 BR-10 | duplicate email/phone → เตือน | 05_RULES BR-10 · ENG-RCT-02 · 06 AT-08 |
| §9 VR-01..05 | field required · double-submit · in-band · DOA dynamic · viewer RO | 05_RULES §5.4 + BR/§5.3 · 06 AT-21/AT-24 |
| §10 E1 no-consent block | Edge | 05_RULES EC-01 · 06 AT-11 |
| §10 E2 duplicate warn | Edge | 05_RULES EC-02 · 06 AT-08 |
| §10 A1 no-manpower warn | Edge | 05_RULES BR-08 · 06 AT-02 |
| §10 A3/FIX-01 board→hired guard | Edge | 05_RULES EC-05 · 03_FN-19 · 06 AT-16 |
| §10 FIX-02 viewer indirect mutation | Edge | 05_RULES VR-05/EC-06 · 03_FN-24 viewerGuard · 06 AT-24 |
| §10 offer นอก band → เตือน+เหตุผล | Edge | 05_RULES VR-03/EC-07 · 06 AT-14 |
| §10 ST req closed w/ pipeline | Edge (OQ-17) | 05_RULES EC-08 `[AI-DEFAULT]` · 06 AT-25 |

**สรุป:** FN 21/21 ✅ · Stories 12/12 ✅ · Rules (BR 10 + VR 5) 15/15 ✅ · Edges (confirmed + probes) ✅ · ไม่มีที่ลง → OQ: OQ-15, OQ-16, OQ-17, OQ-R1 (+ `[AI-DEFAULT]` OQ-D1..D4).
