# 03_LOGIC — F-HR-RECRUIT (F127) สรรหา / Recruit

> **Audience:** BE dev (business logic layer)
> **Scope:** non-HTTP logic — functions, state transitions, validations, integrations, calc
> **CUBIC:** §3.1 Functions = scope-local · §3.2 Engines = CUBIC candidate
> **R8:** ทุก mutation API trace ≥1 Function/Engine ใน §3.3
> **Naming:** Function = camelCase · Engine = kebab-case

---

## §3.1 Functions (Scope-Local)

### F127-FN-01: `createRequisition`
- **Purpose:** สร้างอัตราใหม่ (draft) + generate code + resolve+snapshot band
- **Input:** `{ position, department?, count, grade_code, hiring_manager_id, manpower_ref? }`
- **Output:** `Requisition | ValidationError[]`
- **Invoked by:** F127-API-02
- **Calls:** F127-FN-25 resolveBand · F127-FN-21 appendAudit
- **Side effects:** INSERT T_recruit_requisition · audit (kind=warn ถ้า manpower_ref=null · BR-08)
- **Error cases:** ERR_VALIDATION_FAILED · BR_INVALID_GRADE
- **Iron rule:** ✅ no HTTP terms

### F127-FN-02: `updateRequisition`
- **Purpose:** แก้อัตราขณะ draft เท่านั้น
- **Input:** `{ id, patch }` · **Output:** `Requisition | Error`
- **Invoked by:** F127-API-04 · **Calls:** appendAudit
- **Side effects:** UPDATE (guard status=draft · else ERR_INVALID_STATE) + audit

### F127-FN-03: `submitRequisitionApproval`
- **Purpose:** ส่งอนุมัติเปิดอัตรา — resolve DOA slot chain แล้วตั้ง status=pending
- **Input:** `{ id }` · **Output:** `{ status, doa_entry_ref, approval_chain }`
- **Invoked by:** F127-API-05 · **Calls:** F127-FN-26 resolveDoaChain('req') · appendAudit
- **Side effects:** UPDATE status=pending, approval_chain snapshot · **ไม่ hardcode สาย** (VR-04)
- **Error:** ERR_INVALID_STATE (ไม่ใช่ draft) · BR_DOA_UNRESOLVED

### F127-FN-04: `approveApprovalStep`
- **Purpose:** บันทึกผลอนุมัติต่อ slot (req หรือ offer) · เมื่อครบทุก slot → approved
- **Input:** `{ entity:'req'|'offer', id, slotRole, decision:'approve'|'reject', reason? }`
- **Output:** `{ status, approval_chain }`
- **Invoked by:** F127-API-06, F127-API-19 · **Calls:** appendAudit
- **Side effects:** UPDATE chain[slot].decided_at · ครบ→approved (+ready NTF) · reject→ย้อน draft/pending
- **Error:** ERR_NOT_IN_SLOT (SoD: ต้องเป็น slot role · maker≠approver) · ERR_INVALID_STATE
- **Iron rule:** ✅

### F127-FN-05: `buildRequisitionListQuery`
- **Purpose:** แปลง filter (status/q) → query · **Output:** `QuerySpec` · **Invoked by:** F127-API-01 · Side effects: — (read)

### F127-FN-06: `announceRequisition`
- **Purpose:** approved→open (ประกาศรับ ภายใน)
- **Invoked by:** F127-API-07 · **Calls:** appendAudit · Side effects: UPDATE status=open + ntf · Error: ERR_INVALID_STATE (ต้อง approved)

### F127-FN-06b: `buildCandidateListQuery`
- **Purpose:** filter ผู้สมัคร (stage/q) → query · **Invoked by:** F127-API-09 · read-only

### F127-FN-07: `closeRequisition`
- **Purpose:** ปิดอัตรา (filled auto / cancelled confirm)
- **Input:** `{ id, mode:'filled'|'cancelled', reason? }` · **Output:** `Requisition | Error`
- **Invoked by:** F127-API-08 (+ ภายในจาก hireCandidate เมื่อ filled≥count) · **Calls:** appendAudit
- **Side effects:** UPDATE status=closed/cancelled + close_reason · **Guard OQ-17 `[AI-DEFAULT]`:** cancelled + มี active candidate → require reason + warn (ไม่ยกเลิก candidate อัตโนมัติ)

### F127-FN-08: `createCandidate`
- **Purpose:** สร้างผู้สมัคร + stamp consent + ผูก req (application) + set dup flag
- **Input:** `{ name, contact_email?, contact_phone?, resume_ref?, interested_position?, req_id?, consent }`
- **Output:** `Candidate | ValidationError[]`
- **Invoked by:** F127-API-10 · **Calls:** F127-FN-09 detectDuplicate · appendAudit
- **Side effects:** INSERT T_recruit_candidate (consent_ok=consent, consent_date ถ้า true, stage=applied) · audit
- **Note:** consent=false → บันทึกได้ (gate ที่ move/assess/offer · BR-02) · **PII = Restricted**
- **Iron rule:** ✅

### F127-FN-09: `detectDuplicate`
- **Purpose:** ตรวจซ้ำ email/phone (normalize) → dup flag + note (**เตือน ไม่บล็อก** · BR-10)
- **Input:** `{ contact_email?, contact_phone? }` · **Output:** `{ dup:bool, dupNote? }`
- **Invoked by:** F127-FN-08, F127-API-09 (list flag) · **Calls:** ENG-RCT-02 candidate-duplicate-matcher
- **Side effects:** — (read)

### F127-FN-10: `updateCandidate`
- **Purpose:** แก้ข้อมูลผู้สมัคร · **Invoked by:** F127-API-12 · Calls appendAudit · Side effects UPDATE + audit

### F127-FN-11: `setCandidateConsent`
- **Purpose:** บันทึกความยินยอม PDPA (ok=true, date=today)
- **Invoked by:** F127-API-13 · **Calls:** appendAudit · Side effects: UPDATE consent_ok/date + audit (toast "บันทึกความยินยอมแล้ว")

### F127-FN-12: `moveCandidateStage` ⭐
- **Purpose:** เลื่อนสถานะ pipeline พร้อม guard consent + offer + hire-route
- **Input:** `{ id, dir|to }` · **Output:** `Candidate | GuardError`
- **Invoked by:** F127-API-14 · **Calls:** F127-FN-24 viewerGuard · appendAudit
- **Side effects:** UPDATE stage + audit (append · BR-03)
- **Guards:** dir>0 & !consent_ok → BR_CONSENT_REQUIRED · →offer ต้องมี offer → BR_OFFER_REQUIRED · →hired บล็อก (route hire เท่านั้น · FIX-01) → BR_HIRE_ROUTE_ONLY · optimistic lock (OQ-D1)
- **Iron rule:** ✅

### F127-FN-13: `scheduleInterview`
- **Purpose:** นัดสัมภาษณ์ + snapshot ผู้สัมภาษณ์ (Employee Master) + ยิง NTF
- **Input:** `{ candidate_id, scheduled_at, location?, interviewer_id }` · **Output:** `Interview`
- **Invoked by:** F127-API-15 · **Calls:** appendAudit · (external EXT-EMP snapshot) · ntf
- **Side effects:** INSERT T_recruit_interview (interviewer_snapshot · BR-09) + ntf interview_scheduled + audit

### F127-FN-14: `saveScorecard`
- **Purpose:** บันทึกคะแนน 1-5 + comment ต่อผู้สัมภาษณ์
- **Invoked by:** F127-API-16 · Calls appendAudit · Side effects INSERT T_recruit_scorecard · Error: validation score required

### F127-FN-15: `createOffer` ⭐
- **Purpose:** สร้างข้อเสนอ — resolve band + **freeze version_id** + in-band check
- **Input:** `{ candidate_id, grade_code, start_date, salary, out_of_range_reason? }`
- **Output:** `Offer | ValidationError[]`
- **Invoked by:** F127-API-17 · **Calls:** F127-FN-25 resolveBand · appendAudit
- **Side effects:** INSERT T_recruit_offer (band_version_id + band_snapshot freeze · BR-09) · UPDATE candidate.stage=offer
- **Validation:** start_date+salary required · salary นอก [min,max] → require out_of_range_reason (VR-03)
- **Iron rule:** ✅

### F127-FN-16: `submitOfferApproval`
- **Purpose:** ส่งอนุมัติ offer — resolve DOA · **Invoked by:** F127-API-18 · Calls F127-FN-26 resolveDoaChain('offer') · Side effects status pending→(chain) + audit

### F127-FN-17: `approveApprovalStep(offer)` — reuse F127-FN-04 with entity='offer'

### F127-FN-18a: `sendOffer`
- **Purpose:** approved→sent + ntf offer_sent · **Invoked by:** F127-API-20 · Error: ERR_INVALID_STATE (ต้อง approved)

### F127-FN-18: `respondOffer`
- **Purpose:** บันทึกผลตอบรับ/ปฏิเสธ
- **Input:** `{ candidate_id, decision:'accepted'|'declined', reason? }` · **Output:** `Offer`
- **Invoked by:** F127-API-21 · **Calls:** appendAudit · ntf selection_result
- **Side effects:** UPDATE offer.status accepted/declined · declined → candidate.stage=withdrawn · audit

### F127-FN-19: `hireCandidate` ⭐ (handoff)
- **Purpose:** รับเข้าทำงาน — filled++ · auto-close req · ยิง event handoff (**ไม่สร้าง employee**)
- **Input:** `{ candidate_id }` · **Output:** `{ stage:'hired', onboard_sent:true, req_filled }`
- **Invoked by:** F127-API-22 · **Calls:** F127-FN-07 closeRequisition (ถ้า filled≥count) · appendAudit · emitHandoffEvent
- **Precondition:** offer.status=accepted (else BR_OFFER_NOT_ACCEPTED)
- **Side effects:** UPDATE candidate (hired, onboard_sent=true, hired_at) · req.filled++ · **Emit `recruit.candidate.hired` (fire-and-forget · ไม่รอ ack · LOCK-OB1)** · audit · ntf candidate_accepted
- **⚠️ OQ-15:** ไม่สร้าง employee · ไม่เรียก endpoint On/Offboard ปลายทาง (ยังไม่ออกแบบ) · event = outbound contract เท่านั้น (02_API §2.X)
- **Iron rule:** ✅

### F127-FN-20: `terminateCandidate`
- **Purpose:** ไม่ผ่าน/ถอนตัว/talent pool + เหตุผลบังคับ (soft archive · BR-07)
- **Input:** `{ id, result:'rejected'|'withdrawn'|'talent_pool', reason }` · **Invoked by:** F127-API-23
- **Calls:** appendAudit · Side effects: UPDATE stage + terminate_reason + audit · Error: reason required

### F127-FN-21: `appendAudit`
- **Purpose:** เขียน audit trail (append-only) — เรียกจากทุก mutation function
- **Input:** `{ entity_type, entity_id, action, actor_id, kind, diff? }` · **Output:** `void`
- **Invoked by:** ทุก mutation function ข้างบน · **Side effects:** INSERT T_recruit_audit (no update/delete · BR-03/BR-07/D9)
- **Iron rule:** ✅

### F127-FN-22: `buildFunnelReport`
- **Purpose:** สร้าง funnel + time-to-hire จาก candidate data (filter req)
- **Input:** `{ req_id? }` · **Output:** `{ funnel, avg_time_to_hire_days, by_req }`
- **Invoked by:** F127-API-24, F127-API-25 · **Calls:** ENG-RCT-01 recruitment-funnel-engine · Side effects: — (read/aggregate)

### F127-FN-23: `maskCandidatePII`
- **Purpose:** ปิดบัง name/contact ตาม role + consent (maskEmail/maskPhone · PERSONAS.unmask)
- **Input:** `{ candidate, role }` · **Output:** `MaskedCandidate`
- **Invoked by:** F127-API-09 (list), F127-API-11 (detail) · **Side effects:** — (transform) · BR-06/D-CLASS

### F127-FN-24: `viewerGuard`
- **Purpose:** re-check role ต้นทุก mutation — viewer → block (FIX-02 · 15 จุด)
- **Input:** `{ role, action }` · **Output:** `void | PermissionError`
- **Invoked by:** ทุก mutation (ต้น) · **Error:** ERR_INSUFFICIENT_ROLE (toast "สิทธิ์อ่านอย่างเดียว") · re-guard mid-drawer (OQ-D3)

### F127-FN-25: `resolveBand` (integration wrapper — read)
- **Purpose:** เรียก Salary Structure (EXT-BAND) grade+date → band + version_id
- **Input:** `{ grade_code, date? }` · **Output:** `{ min, mid, max, currency, version_id }`
- **Invoked by:** F127-FN-01, F127-FN-15 · **Calls:** external `GET /api/v1/salary-structure/bands/resolve`
- **Note:** read-only · **freeze snapshot ที่ caller** (ไม่ CRUD band · scope lock) · fail → BR_BAND_UNRESOLVED

### F127-FN-26: `resolveDoaChain` (integration wrapper — read)
- **Purpose:** เรียก Policy Center resolve สาย DOA slot ตามตำแหน่ง (ไม่ผูกวงเงิน)
- **Input:** `{ kind:'req'|'offer', context }` · **Output:** `{ entry, steps:[{order,slot,slotName}] }`
- **Invoked by:** F127-FN-03, F127-FN-16 · **Calls:** external Policy Center (EXT-DOA)
- **Note:** **ไม่ hardcode สาย** (VR-04) · fail → BR_DOA_UNRESOLVED · slot ว่าง = คน resolve runtime

> **Iron rule check:** ทุก function ✅ no HTTP terms (req/res/header/status) — integration wrappers (FN-25/26) เรียก external service แต่ input/output = pure objects.

---

## §3.2 Engines (Reusable / CUBIC-Registered)

### ENG-RCT-01: `recruitment-funnel-engine` [NEW]
| Field | Value |
|---|---|
| id | (assigned at CUBIC registration) |
| code | `recruitment-funnel-engine` |
| name | Recruitment Funnel & Time-to-Hire Engine |
| category | analytics-calculation |
| status | **DRAFT** (this FRD) |
| owner | F-HR-RECRUIT (candidate reuse: HR Dashboard) |

**Input Schema:**
```json
{ "candidates": [{ "stage":"str", "applied_at":"iso", "hired_at":"iso|null" }], "filter": { "req_id":"uuid|null" } }
```
**Output Schema:**
```json
{ "funnel": {"applied":n,"screening":n,"interview":n,"offer":n,"hired":n},
  "avg_time_to_hire_days": number, "by_req": [{ "req_id":"uuid", "funnel":{}, "avg":number }] }
```
**Logic Outline:**
1. Bucket candidates by stage (นับ cumulative funnel)
2. time-to-hire = avg(hired_at − applied_at) เฉพาะ hired
3. Group by req_id (optional filter)
**Used by:** F-HR-RECRUIT (current) · HR Dashboard (planned)
**Iron rule:** [x] Pure (no I/O) · [x] Reusable · [x] Substantial (aggregation algorithm)
**CUBIC:** DRAFT → register at dev hand-off (LD-02)

### ENG-RCT-02: `candidate-duplicate-matcher` [NEW]
| Field | Value |
|---|---|
| code | `candidate-duplicate-matcher` |
| name | Candidate Duplicate/Rehire Matcher |
| category | matcher |
| status | **DRAFT** |
| owner | F-HR-RECRUIT (candidate reuse: Employee rehire check) |

**Input Schema:** `{ "candidate": {"email?":"str","phone?":"str"}, "pool": [{"email","phone"}], "match_fields": ["email","phone"] }`
**Output Schema:** `{ "is_duplicate": bool, "matches": [{ "candidate_id":"uuid", "matched_on":"email|phone" }] }`
**Logic Outline:**
1. Normalize email (lowercase/trim) + phone (strip non-digits)
2. Compare against pool by configurable match_fields (BR-10 CONFIGURABLE)
3. Return matches (**เตือน ไม่บล็อก**)
**Used by:** F-HR-RECRUIT (current) · Employee rehire (planned)
**Iron rule:** [x] Pure · [x] Reusable · [x] Substantial (normalization + match)
**CUBIC:** DRAFT → register at hand-off

> **Integration wrappers (band/DOA) ≠ Engines** — เป็น external service read (FN-25/26 §3.1). Matrix #8 wrap-by-API pattern; ยังไม่ own engine เพราะ logic อยู่ที่ปลายทาง (Salary Structure / Policy Center).

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| API-01 | GET | requisitions | FN-05 | — |
| API-02 | POST | requisitions | FN-01, FN-25 | — |
| API-03 | GET | requisitions/:id | — (trivial read) | — |
| API-04 | PUT | requisitions/:id | FN-02 | — |
| API-05 | POST | requisitions/:id/submit-approval | FN-03, FN-26 | — |
| API-06 | POST | requisitions/:id/approve | FN-04 | — |
| API-07 | POST | requisitions/:id/announce | FN-06 | — |
| API-08 | POST | requisitions/:id/close | FN-07 | — |
| API-09 | GET | candidates | FN-06b, FN-23, FN-09 | ENG-RCT-02 |
| API-10 | POST | candidates | FN-08, FN-09 | ENG-RCT-02 |
| API-11 | GET | candidates/:id | FN-23 | — |
| API-12 | PUT | candidates/:id | FN-10 | — |
| API-13 | POST | candidates/:id/consent | FN-11 | — |
| API-14 | POST | candidates/:id/move-stage | FN-12, FN-24 | — |
| API-15 | POST | candidates/:id/interviews | FN-13 | — |
| API-16 | POST | candidates/:id/scores | FN-14 | — |
| API-17 | POST | candidates/:id/offer | FN-15, FN-25 | — |
| API-18 | POST | candidates/:id/offer/submit-approval | FN-16, FN-26 | — |
| API-19 | POST | candidates/:id/offer/approve | FN-17 (=FN-04) | — |
| API-20 | POST | candidates/:id/offer/send | FN-18a | — |
| API-21 | POST | candidates/:id/offer/respond | FN-18 | — |
| API-22 | POST | candidates/:id/hire | FN-19, FN-07 | — |
| API-23 | POST | candidates/:id/terminate | FN-20 | — |
| API-24 | GET | report/funnel | FN-22 | ENG-RCT-01 |
| API-25 | GET | report/export | FN-22 | ENG-RCT-01 |

> **appendAudit (FN-21)** เรียกภายในทุก mutation function → ไม่ list ต่อ row (cross-cutting · FN-93). **viewerGuard (FN-24)** เรียกต้นทุก mutation.

### Trace Verification (Self-Check)
- [x] Every mutation API มี ≥1 Function
- [x] No orphan Function — ทุก FN-01..26 ปรากฏใน trace (FN-21/24 = cross-cutting; FN-25/26 via FN-01/03/15/16)
- [x] No orphan Engine — ENG-RCT-01 (API-24/25) · ENG-RCT-02 (API-09/10)
- [x] No hidden logic in 02_API — business logic ทั้งหมด trace ที่นี่

---

## §3.4 Dependencies

### External Function/Engine called
- `salary-structure/bands/resolve` (Salary Structure API-25) — via FN-25 resolveBand (read + freeze)
- Policy Center DOA resolve — via FN-26 resolveDoaChain (read · ไม่ hardcode)
- `employees?status=active` (Employee Master) — snapshot ผู้สัมภาษณ์/hiring manager
- ENG-NOTIFY — ntf events (interview/offer/result/accepted)

### External that calls into this feature
- On/Offboard (F-HR-ONBOARD) — consume event `recruit.candidate.hired` (**OQ-15 · ฝั่งรับยังไม่ออกแบบ**)
- HR Dashboard — reuse ENG-RCT-01 (planned)

---

## §3.5 Open Questions / Locked Decisions Referenced
- **LD-01:** hire route เดียว (candHireHandoff) — ห้าม skip board → hired (FIX-01)
- **LD-02:** ENG-RCT-01/02 register CUBIC ที่ dev hand-off (ไม่รอบนี้)
- **LD-03:** band/DOA = external read wrapper (FN-25/26) ไม่ own engine
- **OQ-15:** hireCandidate emit event only — ฝั่งรับ inbound = integration phase (ไม่เดา endpoint)
- **OQ-16:** retention/withdraw consent logic ยังไม่ออกแบบ (retention_until display-only)

---

## Audience Cheat-Sheet
| Reader | Sections |
|---|---|
| BE dev | §3.1 + §3.2 + §3.3 |
| QA | §3.3 + §3.1 Side effects |
| Architect / CUBIC | §3.2 + §3.4 + §3.5 |
| PM | §3.3 (coverage) |
