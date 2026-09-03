# CTX — F-HR-RECRUIT: สรรหา (Recruit)

> **derived from:** FRD_F-HR-RECRUIT v1.0 · **generated:** 2026-09-03
> **module:** HR · Wave W9 · **status:** active (FRD status = DRAFT, awaiting review)
> ⚠ Derived artifact — source of truth คือ FRD · ถ้า FRD revise ต้อง regen CTX

---

## 1. Summary
บริหารการสรรหา end-to-end: เปิดอัตรา (requisition) → คลังผู้สมัคร (candidate pool) → บอร์ด pipeline (kanban) → นัดสัมภาษณ์ + scorecard → ออกข้อเสนอจ้าง → รับเข้าทำงาน (hired). ผู้ใช้หลัก = เจ้าหน้าที่สรรหา (recruiter/maker) · hiring manager (checker/approver) · HR owner · viewer (read-only). Trigger = เปิดอัตราใหม่ (มี/ไม่มี Manpower hook). จบที่ candidate.stage = hired แล้ว **ยิง event handoff เข้า On/Offboard เท่านั้น — ไม่สร้าง employee / ไม่ทำสัญญาจ้างเอง** (LOCK-OB1). อนุมัติ req + offer ผ่าน DOA slot picker (ไม่ผูกวงเงิน · resolve runtime) · เงินเดือน offer อ้าง band จาก Salary Structure แบบ freeze snapshot · ผู้สมัคร = ข้อมูล RESTRICTED + PDPA (consent gate).

## 2. Data Contract

### Entities  (owned = 6 tables `T_recruit_*`; เฉพาะ fields ที่ feature อื่น join/อ่าน)
| Entity | PK | Key Fields (cross-ref) | หมายเหตุ |
|---|---|---|---|
| T_recruit_requisition | id (uuid) | code (REQ-xxxx, ≠ เลขรันเอกสาร), tenant_id, grade_code, band_snapshot{min,mid,max,version_id}, hiring_manager(jsonb snapshot), manpower_ref(uuid, **nullable hook** → F124), status, approval_status, doa_entry_ref, approval_chain(jsonb), count, filled(0..count), version | อัตราที่เปิด · RLS · optimistic lock (version) |
| T_recruit_candidate ⚠RESTRICTED | id (uuid) | tenant_id, name/contact_email/contact_phone/resume_ref = **Restricted+PII**, interested_position, req_id(FK→requisition, nullable = application link), consent_ok(PDPA gate), consent_date, retention_until(display-only จาก Policy Center · ห้าม hardcode), stage, dup_flag, onboard_sent, terminate_reason, applied_at, hired_at, version | ผู้สมัคร · PDPA · mask ตาม role |
| T_recruit_offer | id (uuid) | tenant_id, candidate_id(FK, **UNIQUE** 1:1), position, grade_code, salary(Confidential), band_version_id(freeze snapshot เช่น SS-2569-03), band_snapshot, out_of_range_reason, start_date, status, doa_entry_ref, approval_chain, version | 1 offer / candidate |
| T_recruit_interview | id (uuid) | tenant_id, candidate_id(FK), scheduled_at, location, interviewer_snapshot(jsonb, Confidential+PII · Employee snapshot BR-09) | นัดสัมภาษณ์ |
| T_recruit_scorecard | id (uuid) | tenant_id, candidate_id(FK), interviewer_snapshot(Confidential+PII), score(1–5), comment | ผลประเมินต่อผู้สัมภาษณ์ |
| T_recruit_audit | id (uuid) | tenant_id, entity_type, entity_id, action, actor_id, kind(info/warn), diff(jsonb, mask PII), created_at | **append-only** (no UPDATE/DELETE) · retention ≥7y |

**External (read-only · ไม่ own):** Salary Structure band (F-HR-SALSTRUCT) · Employee Master (F011) · Manpower (F124, nullable hook).

### Enums / States  (ครบทุกค่า · R6)
| Field | Values | Transition owner |
|---|---|---|
| requisition.status | `draft` · `pending` · `approved` · `open` · `closed` · `cancelled` | FN-03/04/06/07 (submit→approve→announce→close) |
| requisition.approval_status | `none` · `pending` · `approved` | FN-03/04 (DOA) |
| candidate.stage | `applied` · `screening` · `interview` · `offer` · `hired` · `rejected` · `withdrawn` · `talent_pool` | FN-12 moveCandidateStage · FN-19 hire (route เดียว) · FN-20 terminate |
| offer.status | `pending` · `approved` · `sent` · `accepted` · `declined` | FN-16/17/18a/18 (submit→approve→send→respond) |
| audit.kind | `info` · `warn` | appendAudit (warn เมื่อ manpower null ฯลฯ) |
| audit.action | `create` · `edit` · `move` · `approve` · `reject` · `hire` · `close` · `announce` · `warn` | ทุก mutation |

**State machine guards (cross-boundary สำคัญ):** เลื่อน stage dir>0 → ต้อง `consent_ok=true` (BR-02) · เข้า offer stage → ต้องมี offer object · เข้า `hired` → offer.status=accepted **และ route ผ่าน hire (API-22) เท่านั้น** (LD-01/FIX-01 · move-stage→hired ถูกบล็อก).

### Relationships
- requisition (1) —< (N) candidate  (`candidate.req_id` · application link · nullable)
- candidate (1) —1 (1) offer  (`offer.candidate_id` UNIQUE)
- candidate (1) —< (N) interview · candidate (1) —< (N) scorecard (ต่อผู้สัมภาษณ์)
- all mutations —> (N) audit (append-only)
- **External read/snapshot:** Salary Structure —(read·freeze)→ requisition.band_snapshot / offer.band_version_id · Employee Master —(read·snapshot)→ requisition.hiring_manager / interview.interviewer_snapshot · Manpower F124 —(hook·nullable)→ requisition.manpower_ref · candidate(hired) —(event handoff)→ On/Offboard

## 3. API Surface
**Base path:** `/api/v1/recruit` · common headers: `X-Tenant-Id` (all) · `Idempotency-Key` (mutation) · `If-Match` (state-change, optimistic lock) · viewer = 403 ทุก mutation.

| Method | Endpoint | ทำอะไร | Payload หลัก |
|---|---|---|---|
| GET | /requisitions | list + filter | `?status,q,limit,offset` |
| POST | /requisitions | เปิดอัตรา (draft) | position, count, grade_code, hiring_manager_id, manpower_ref? |
| GET | /requisitions/:id | รายละเอียดอัตรา | — |
| PUT | /requisitions/:id | แก้อัตรา (draft) | (req fields) |
| POST | /requisitions/:id/submit-approval | ส่งอนุมัติเปิด (DOA resolve) | `{}` (server resolve slot) |
| POST | /requisitions/:id/approve | อนุมัติ/ไม่อนุมัติ (slot · SoD) | decision(approve/reject), reason? |
| POST | /requisitions/:id/announce | ประกาศรับ (approved→open) | — |
| POST | /requisitions/:id/close | ปิด/ยกเลิกอัตรา | mode(filled/cancelled), reason? |
| GET | /candidates | list ผู้สมัคร (**masked ตาม role**) + filter | `?stage,q,limit,offset` |
| POST | /candidates | เพิ่มผู้สมัคร (+consent+dup) | name, contact_email?, contact_phone?, resume_ref?, interested_position?, req_id?, consent |
| GET | /candidates/:id | รายละเอียดผู้สมัคร (ACL + access audit) | — |
| PUT | /candidates/:id | แก้ผู้สมัคร | (candidate fields) |
| POST | /candidates/:id/consent | บันทึกความยินยอม PDPA | consent(true) |
| POST | /candidates/:id/move-stage | เลื่อน pipeline (guard consent/offer/hire) | dir(1/-1) หรือ to(stage) |
| POST | /candidates/:id/interviews | นัดสัมภาษณ์ (+NTF) | scheduled_at, location?, interviewer_id |
| POST | /candidates/:id/scores | บันทึก scorecard | interviewer_id, score(1–5), comment? |
| POST | /candidates/:id/offer | สร้างข้อเสนอ (band freeze) | grade_code, start_date, salary, out_of_range_reason? |
| POST | /candidates/:id/offer/submit-approval | ส่งอนุมัติ offer (DOA) | `{}` |
| POST | /candidates/:id/offer/approve | อนุมัติ offer (slot · SoD) | decision, reason? |
| POST | /candidates/:id/offer/send | เสนอ offer (approved→sent, +NTF) | — |
| POST | /candidates/:id/offer/respond | ตอบรับ/ปฏิเสธ (+NTF) | decision(accepted/declined), reason? |
| POST | /candidates/:id/hire ⭐ | รับเข้าทำงาน + **emit handoff event** | `{}` (confirm) — precond offer.status=accepted |
| POST | /candidates/:id/terminate | ไม่ผ่าน/ถอนตัว/talent pool (soft archive) | result(rejected/withdrawn/talent_pool), reason(บังคับ) |
| GET | /report/funnel | funnel + time-to-hire + filter | `?req_id` |
| GET | /report/export | Export CSV (stub → dev) | — |

**External consumed (read · ไม่ own):**
| Method | Endpoint | ทำอะไร |
|---|---|---|
| GET | /api/v1/salary-structure/bands/resolve | grade+date → band + version_id (freeze) |
| GET | /api/v1/employees?status=active | ผู้สัมภาษณ์ / hiring manager picker (snapshot) |
| (resolve) | Policy Center DOA (F-DLG-001) | resolve slot chain (server-side · ไม่ hardcode) |

### Events emitted
| Event | Trigger point | Payload key |
|---|---|---|
| `recruit.candidate.hired` (handoff · outbound · fire-and-forget) | hire (API-22 · FN-19) candidate.stage→hired | candidate_id, position, grade_code, start_date, offer_snapshot{salary,band_version_id}, hired_at — **ไม่มี employee_id** · OQ-15 ฝั่งรับ undesigned |
| `recruit_interview_scheduled` (NTF) | scheduleInterview (FN-13 · API-15) | ref=candidate_id · vars{candidate(masked),position,scheduled_at,location?} |
| `recruit_stage_changed` (NTF, ปิดได้) | moveCandidateStage (FN-12 · API-14) | ref=candidate_id · vars{candidate,position,stage} |
| `recruit_offer_sent` (NTF) | sendOffer (FN-18a · API-20) | ref=candidate_id · vars{candidate,position,offer_ref} |
| `recruit_offer_result` (NTF) | respondOffer (FN-18 · API-21) | ref=candidate_id · vars{candidate,position,offer_ref,decision} |
| `recruit.candidate_stored` (CSQ · SecC/PDPA) | เพิ่ม/แก้ผู้สมัคร (BR-02/BR-06) | ref=candidate_id · consent_pdpa, retention_until, action(view/store) |
| `recruit.hired` (CSQ · EC) | offer accepted→hired | ref=req_id · cost_declared, currency=THB `[AI-DRAFT]` |

> DOA events (`doa_pending`/`doa_result`/`doa_escalate`) = DOA engine เจ้าของ ยิงอัตโนมัติ · feature **ไม่ประกาศซ้ำ**.

## 4. Shared Rules (cross-boundary เท่านั้น)
| Rule ID | Rule | กระทบใคร |
|---|---|---|
| BR-05 / LOCK-OB1 | hired → emit `recruit.candidate.hired` (fire-and-forget) · **ไม่สร้าง employee record** — On/Offboard เป็นเจ้าภาพ onboarding | On/Offboard (F-HR-ONBOARD) · integration phase |
| BR-09 / LD-03 | band_version_id + band_snapshot **freeze ณ สร้าง offer** (ไม่ re-resolve); ผู้สัมภาษณ์/hiring manager = Employee snapshot | Salary Structure · Employee Master (read-only) |
| BR-01 / BR-04 / LOCK-OB3 / VR-04 | req + offer ต้องอนุมัติ DOA ครบทุก slot ก่อน announce/send · สาย resolve runtime จาก Policy Center · **ไม่ hardcode · ไม่ผูกวงเงิน** (LOCK-DOA) | Policy Center DOA (F-DLG-001) |
| BR-02 / LOCK-OB2 | consent PDPA ก่อนดำเนินต่อ (guard เลื่อน/สัมภาษณ์/offer) · retention_until = display-only จาก Policy Center | Policy Center PDPA · CSQ SecC · **OQ-16** |
| BR-06 / LOCK-OB5 | candidate name/contact/resume = **Restricted + PII** · mask ตาม role (recruiter unmask · manager/viewer mask) + mask เมื่อ !consent | ทุก consumer ที่อ่าน candidate · Policy Center Restricted Resources (OQ-R1) |
| BR-08 / LOCK-OB4 | manpower_ref = hook · null = ไม่บังคับ (บันทึกได้ + audit warn + chip "ไม่มีแผน") | Manpower F124 (ยังไม่ dev) |
| BR-03 / BR-07 | ทุก mutation → append T_recruit_audit (append-only, no delete, ≥7y) · terminate = soft archive | Audit/Compliance (D9) |
| LOCK-DOCCFG | ไม่มีเลขรันเอกสาร (offer letter = soft-ref) · requisition.code ≠ เลขรันเอกสาร | — (ไม่ต้อง DOCCFG) |

## 5. Integration
- **Depends on:**
  - **F-HR-SALSTRUCT (F062) Salary Structure** — GET bands/resolve (read-only · freeze band + version_id คู่ offer/req).
  - **Employee Master (F011)** — GET employees?status=active (read/snapshot · hiring manager + ผู้สัมภาษณ์).
  - **Policy Center DOA (F-DLG-001)** — resolve slot chain req/offer runtime (ไม่ hardcode · slot-based ไม่มีวงเงิน).
  - **Policy Center PDPA** — retention config (display-only `retention_until` · OQ-16) + Restricted Resources (OQ-R1, รอบนี้ role masking).
  - **Manpower (F124)** — `manpower_ref` display-only hook · **F124 ยังไม่ dev = null nullable, warn-only** (ไม่บล็อก).
  - **ENG-NOTIFY (F-NOTIFY)** — event sink (4 NTF events).
- **Depended by:**
  - **On/Offboard (F-HR-ONBOARD / F064)** — รับ event `recruit.candidate.hired` (soft-linkage · fire-and-forget) · **inbound contract UNDESIGNED = OQ-15**.
  - **HR Dashboard (planned)** — funnel / time-to-hire metrics (ENG-RCT-01).
  - **Employee rehire (planned)** — duplicate-matcher (ENG-RCT-02).
- **Declarations:**
  - **DOA:** yes — 2 actions (requisition + offer) · `policy_approve` · role-based ไม่ผูกวงเงิน · roles ทุกตัวติดแท็ก `[DEFAULT—รอยืนยัน]` (DOA master ไม่มีในติดตั้งนี้ = **OQ-DOA**) · wire_status pending.
  - **NTF:** 4 events (interview_scheduled/stage_changed/offer_sent/offer_result) · กลุ่มใหม่ "สรรหา (Recruit)" ใน EVENT_GROUPS · `doa_*` excluded.
  - **CSQ:** 2 events (`candidate_stored`→SecC PDPA · `hired`→EC) · **carried verbatim** (WF-01 ไม่มี skill csq-declaration · ยังไม่ผ่าน gate · BA ต้องทวน).
  - **DOCCFG:** not-needed (ไม่มีเลขรันเอกสาร · LOCK-DOCCFG).
- **Engine hooks:** ENG-RCT-01 recruitment-funnel-engine (API-24/25 · DRAFT) · ENG-RCT-02 candidate-duplicate-matcher (API-09/10 · DRAFT) · ENG-NOTIFY (4 NTF) · ENG-CSQ (2 CSQ · SecC/EC). ENG-RCT-01/02 register CUBIC ที่ dev hand-off (LD-02).

---
*trace: §2 ← FRD 04_DB · §3 ← FRD 02_API (+§2.X Cross-Module) · §4 ← FRD 05_RULES + 07_LOCKED · §5 ← 00_OVERVIEW §0.5 + DOA/NTF/CSQ briefs*
