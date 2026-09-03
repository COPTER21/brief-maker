# 02_API — F-HR-RECRUIT (F127) สรรหา / Recruit

> **Audience:** Backend developer (HTTP layer)
> **Purpose:** API contracts — CUBIC API Entity format
> **🚨 Iron Rule:** ห้าม business logic >5 lines ที่นี่ — ย้ายไป 03_LOGIC §3.1
> **🚨 R8:** ทุก mutation API ต้องระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3
> **Base path:** `/api/v1/recruit`

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth |
|---|---|---|---|---|
| F127-API-01 | GET | /recruit/requisitions | List อัตรา + filter | required |
| F127-API-02 | POST | /recruit/requisitions | เปิดอัตรา (draft) | recruiter/manager |
| F127-API-03 | GET | /recruit/requisitions/:id | รายละเอียดอัตรา | required |
| F127-API-04 | PUT | /recruit/requisitions/:id | แก้อัตรา (draft) | recruiter/manager |
| F127-API-05 | POST | /recruit/requisitions/:id/submit-approval | ส่งอนุมัติเปิด (DOA) | recruiter/manager |
| F127-API-06 | POST | /recruit/requisitions/:id/approve | อนุมัติ/ไม่อนุมัติ (slot) | manager (slot) |
| F127-API-07 | POST | /recruit/requisitions/:id/announce | ประกาศรับ (open) | recruiter/manager |
| F127-API-08 | POST | /recruit/requisitions/:id/close | ปิด/ยกเลิกอัตรา | recruiter/manager |
| F127-API-09 | GET | /recruit/candidates | List ผู้สมัคร (masked) + filter | required |
| F127-API-10 | POST | /recruit/candidates | เพิ่มผู้สมัคร (+consent+dup) | recruiter/manager |
| F127-API-11 | GET | /recruit/candidates/:id | รายละเอียดผู้สมัคร (ACL) | required |
| F127-API-12 | PUT | /recruit/candidates/:id | แก้ผู้สมัคร | recruiter/manager |
| F127-API-13 | POST | /recruit/candidates/:id/consent | บันทึกความยินยอม PDPA | recruiter/manager |
| F127-API-14 | POST | /recruit/candidates/:id/move-stage | เลื่อนสถานะ pipeline | recruiter/manager |
| F127-API-15 | POST | /recruit/candidates/:id/interviews | นัดสัมภาษณ์ (+NTF) | recruiter/manager |
| F127-API-16 | POST | /recruit/candidates/:id/scores | บันทึก scorecard | recruiter/manager/interviewer |
| F127-API-17 | POST | /recruit/candidates/:id/offer | สร้างข้อเสนอ (band freeze) | recruiter/manager |
| F127-API-18 | POST | /recruit/candidates/:id/offer/submit-approval | ส่งอนุมัติ offer (DOA) | recruiter/manager |
| F127-API-19 | POST | /recruit/candidates/:id/offer/approve | อนุมัติ offer (slot) | manager (slot) |
| F127-API-20 | POST | /recruit/candidates/:id/offer/send | เสนอ offer (sent) | recruiter/manager |
| F127-API-21 | POST | /recruit/candidates/:id/offer/respond | ตอบรับ/ปฏิเสธ | recruiter/manager |
| F127-API-22 | POST | /recruit/candidates/:id/hire | รับเข้าทำงาน + handoff event | recruiter/manager |
| F127-API-23 | POST | /recruit/candidates/:id/terminate | ไม่ผ่าน/ถอนตัว/talent pool | recruiter/manager |
| F127-API-24 | GET | /recruit/report/funnel | funnel + time-to-hire + filter | required |
| F127-API-25 | GET | /recruit/report/export | Export CSV (stub → dev) | required |
| — external read (consumed, ไม่ own) — | | | | |
| EXT-BAND | GET | /api/v1/salary-structure/bands/resolve | grade+date → band + version_id | required |
| EXT-EMP | GET | /api/v1/employees?status=active | ผู้สัมภาษณ์/hiring manager picker | required |
| EXT-DOA | (resolve) | Policy Center DOA | resolve slot chain (ไม่ hardcode) | server-side |

> **Common:** ทุก endpoint ต้องมี `X-Tenant-Id`. Mutation ต้องมี `Idempotency-Key` (OQ-D2). PUT/state-change ใช้ `If-Match` (optimistic lock · OQ-D1). Auth = JWT. **viewer = ไม่มี mutation** (403 · VR-05).

---

## §2.2 Per-API Contract (representative — mutation + guarded)

### F127-API-02: POST /recruit/requisitions
| Field | Value |
|---|---|
| id | F127-API-02 · method POST · roles recruiter/manager |
| headers | X-Tenant-Id, Idempotency-Key (required) |

**Body:**
```json
{ "position":"str", "department":"str?", "count":1, "grade_code":"G4",
  "hiring_manager_id":"uuid", "manpower_ref":"uuid|null" }
```
**Validation (≤5 lines):** position required · count required int ≥1 · grade_code required (in HR Config) · hiring_manager_id required, active. **Complex → 03_LOGIC F127-FN-01.**
**Response 201:** `{ "id","code":"REQ-...","status":"draft","band_snapshot":{...,"version_id":"SS-2569-03"} }`
**Errors:** 400 ERR_VALIDATION_FAILED · 403 ERR_INSUFFICIENT_ROLE · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY
**Preconditions:** grade exists (HR Config). manpower_ref **null = อนุญาต** (BR-08 · เตือน display-only, ไม่บล็อก).
**Side effects:** INSERT T_recruit_requisition · INSERT T_recruit_audit (kind=info; kind=warn ถ้า manpower null).
**Calls (Logic):** F127-FN-01 createRequisition (+ EXT-BAND resolve via F127-FN-25 resolveBand)

---

### F127-API-05: POST /recruit/requisitions/:id/submit-approval
**Body:** `{}` (server resolves slot). **Precondition:** status=draft.
**Response 200:** `{ "status":"pending","doa_entry_ref":"DOA-REQ-OPEN-001","approval_chain":[{order,slot,slotName}] }`
**Errors:** 409 ERR_INVALID_STATE · 422 BR_DOA_UNRESOLVED (Policy Center ไม่คืน chain)
**Side effects:** UPDATE status=pending · resolve DOA (EXT-DOA) · **NTF doa_pending มาจาก DOA engine (ไม่ประกาศซ้ำ)** · audit.
**Calls (Logic):** F127-FN-03 submitRequisitionApproval · F127-FN-26 resolveDoaChain (external Policy Center)

---

### F127-API-06: POST /recruit/requisitions/:id/approve
**Body:** `{ "decision":"approve|reject", "reason":"str?" }` (reason required ถ้า reject).
**Response 200:** `{ "status":"approved|draft","approval_chain":[...] }`
**Rule:** ทุก slot อนุมัติครบ → approved (BR-01). SoD: approver ต้องเป็น slot role (ไม่ใช่ maker). Errors: 403 ERR_NOT_IN_SLOT · 409 ERR_INVALID_STATE.
**Side effects:** UPDATE approval_chain[slot].decided · เมื่อครบ → status approved + NTF announced-ready · audit.
**Calls (Logic):** F127-FN-04 approveApprovalStep

---

### F127-API-07 announce / F127-API-08 close
- **announce:** precondition status=approved → open. Response `{status:"open"}`. Calls F127-FN-06 announceRequisition.
- **close:** body `{ "mode":"filled|cancelled", "reason":"str?" }`. **Guard (OQ-17 `[AI-DEFAULT]`):** ถ้ามี active candidate ค้าง pipeline และ mode=cancelled → require confirm + reason; filled auto เมื่อ filled≥count. Response `{status:"closed|cancelled"}`. Calls F127-FN-07 closeRequisition.

---

### F127-API-10: POST /recruit/candidates
**Body:**
```json
{ "name":"str","contact_email":"str?","contact_phone":"str?","resume_ref":"str?",
  "interested_position":"str?","req_id":"uuid|null","consent":false }
```
**Validation:** name required · contact อย่างน้อย 1 (email/phone). **Complex (dup detect) → 03_LOGIC.**
**Response 201:** `{ "id","stage":"applied","consent_ok":bool,"consent_date":date|null,"dup_flag":bool,"dupNote":"str?" }`
**Rule:** consent=false → **บันทึกเข้าคลังได้ แต่ดำเนินต่อไม่ได้** (BR-02 · gate ที่ move/assess/offer). dup → เตือน ไม่บล็อก (BR-10).
**Side effects:** INSERT T_recruit_candidate · dup check (ENG-RCT-02) · audit.
**Data classification:** name/contact/resume = **Restricted** — response mask ตาม role (recruiter unmask / อื่น mask).
**Calls (Logic):** F127-FN-08 createCandidate · F127-FN-09 detectDuplicate (ENG-RCT-02)

---

### F127-API-13: POST /recruit/candidates/:id/consent
**Body:** `{ "consent":true }`. Response `{consent_ok:true, consent_date:"YYYY-MM-DD"}`. Side effects: UPDATE + audit. Calls F127-FN-11 setCandidateConsent.

---

### F127-API-14: POST /recruit/candidates/:id/move-stage
**Body:** `{ "dir":1|-1 }` หรือ `{ "to":"screening" }`.
**Guards (BR-02/BR-03 · state machine §5.2):**
- dir>0 และ `consent_ok=false` → **422 BR_CONSENT_REQUIRED** (toast "ยังไม่ได้รับความยินยอม PDPA — เลื่อนสถานะไม่ได้")
- → offer stage: ต้องมี offer object (else 422 BR_OFFER_REQUIRED)
- → hired: **บล็อก** — ต้องผ่าน F127-API-22 hire เท่านั้น (offer.accepted · FIX-01) → 422 BR_HIRE_ROUTE_ONLY
- viewer → 403 (VR-05)
**Response 200:** `{ stage }`. Side effects: UPDATE stage + audit (append). Optimistic lock (If-Match · OQ-D1).
**Calls (Logic):** F127-FN-12 moveCandidateStage · F127-FN-24 viewerGuard

---

### F127-API-15 interviews / F127-API-16 scores
- **interviews:** body `{ scheduled_at, location?, interviewer_id }`. Response interview obj. Side effects: INSERT T_recruit_interview (interviewer **snapshot** BR-09) + **ntf interview_scheduled** (ผู้สัมภาษณ์+ผู้สมัคร) + audit. Calls F127-FN-13 scheduleInterview.
- **scores:** body `{ interviewer_id, score:1-5, comment? }`. Validation score 1–5 required (toast "กรุณาให้คะแนนก่อน"). Side effects INSERT T_recruit_scorecard + audit. Calls F127-FN-14 saveScorecard.

---

### F127-API-17: POST /recruit/candidates/:id/offer
**Body:** `{ "grade_code":"G4","start_date":"date","salary":62000,"out_of_range_reason":"str?" }`
**Validation:** start_date + salary required (toast "กรุณากรอกวันเริ่มงานและเงินเดือน"). salary นอก band → require out_of_range_reason (toast "เงินนอกช่วง band — กรุณาระบุเหตุผล" · VR-03).
**Response 201:** `{ id, status:"pending", band_version_id:"SS-2569-03", band_snapshot:{...} }`
**Rule (BR-09):** resolve band (EXT-BAND, start_date) → **freeze version_id + band_snapshot** ณ สร้าง (ไม่ re-resolve ภายหลัง).
**Side effects:** INSERT T_recruit_offer · UPDATE candidate.stage=offer · audit.
**Calls (Logic):** F127-FN-15 createOffer · F127-FN-25 resolveBand (EXT-BAND)

---

### F127-API-18/19/20/21 (offer lifecycle)
- **submit-approval:** pending→(DOA resolve). Calls F127-FN-16 submitOfferApproval + FN-26 resolveDoaChain.
- **approve:** slot approve → status approved (BR-04, SoD). Calls F127-FN-17 approveApprovalStep(offer).
- **send:** approved→sent + ntf offer_sent (toast "ส่งข้อเสนอแล้ว"). Calls F127-FN-18a sendOffer.
- **respond:** body `{ "decision":"accepted|declined","reason":"str?" }`. accepted→ candidate พร้อม hire; declined→ candidate.stage=withdrawn + ntf selection_result. Calls F127-FN-18 respondOffer.

---

### F127-API-22: POST /recruit/candidates/:id/hire ⭐ (handoff)
**Precondition:** offer.status = **accepted** (else 422 BR_OFFER_NOT_ACCEPTED · toast "ต้องให้ผู้สมัครตอบรับข้อเสนอก่อน").
**Body:** `{}` (confirm via M-06).
**Response 200:** `{ stage:"hired", onboard_sent:true, req_filled: n }`
**Side effects:**
- UPDATE candidate.stage=hired, onboard_sent=true, hired_at=now
- requisition.filled++ · auto-close เมื่อ filled≥count
- **Emit event `recruit.candidate.hired`** (fire-and-forget · ไม่รอ ack · **ไม่สร้าง employee** — LOCK-OB1) → ดู §2.X
- audit + ntf candidate_accepted
**Calls (Logic):** F127-FN-19 hireCandidate
> ⚠️ **OQ-15:** ฝั่งรับ On/Offboard ยังไม่ออกแบบ — event schema ด้านล่าง = outbound contract เท่านั้น. **ห้ามเดา endpoint ปลายทาง / ห้ามทำ inbound sync ในรอบนี้.**

---

### F127-API-23: terminate
**Body:** `{ "result":"rejected|withdrawn|talent_pool","reason":"str" }` (reason **บังคับ** · toast "กรุณาระบุเหตุผล"). Side effects: UPDATE stage + terminate_reason + audit (soft archive · BR-07). Calls F127-FN-20 terminateCandidate.

---

### F127-API-24 funnel / F127-API-25 export
- **funnel:** query `?req_id=`. Response `{ funnel:{applied,screening,interview,offer,hired}, avg_time_to_hire_days, by_req:[...] }`. Calls F127-FN-22 buildFunnelReport (ENG-RCT-01). **avg_time_to_hire = คำนวณจริงจาก applied_at→hired_at** (prototype hardcode "23 วัน" = mock; dev bind ค่าจริง).
- **export:** stub รอบนี้ (dev binds CSV stream) — response 202 + toast "ส่งออกรายงาน (CSV) — ต่อ dev".

---

### GET endpoints (list/detail — trivial reads)
- **API-01/09 (list):** query params `status/stage`, `q` (search), `limit/offset`. Calls buildListQuery (F127-FN-05/06). API-09 response = **masked ตาม role** (F127-FN-23 maskCandidatePII).
- **API-03/11 (detail):** single read; API-11 candidate = ACL + audit access (Restricted).

---

## §2.3 Common Concerns
- **Idempotency (OQ-D2):** mutation รับ `Idempotency-Key` · cache 24h · same key+body → cached · diff body → 409.
- **Optimistic Locking (OQ-D1):** state-change ใช้ `If-Match: <updated_at/version>` · mismatch → 409 ERR_STALE_DATA (concurrent stage move).
- **Multi-Tenant:** ทุก endpoint `X-Tenant-Id` → RLS.
- **Audit:** ทุก mutation → T_recruit_audit (append-only middleware · actor/action/entity/diff/timestamp). การเข้าถึง Restricted (candidate detail) → audit access log.
- **Permission:** viewer = read-only (403 ทุก mutation) · masking response ตาม role.
- **DOA:** slot chain resolve server-side จาก Policy Center — **ไม่ hardcode สายในโค้ด feature** (VR-04).

---

## §2.4 API → Logic Trace (Anchor for R8 · authoritative = 03_LOGIC §3.3)

| API | Calls Functions | Calls Engines |
|---|---|---|
| API-01 GET requisitions | F127-FN-05 | — |
| API-02 POST requisitions | F127-FN-01, F127-FN-25 | — |
| API-03 GET requisition/:id | — (trivial) | — |
| API-04 PUT requisition | F127-FN-02 | — |
| API-05 submit-approval (req) | F127-FN-03, F127-FN-26 | — |
| API-06 approve (req) | F127-FN-04 | — |
| API-07 announce | F127-FN-06 | — |
| API-08 close | F127-FN-07 | — |
| API-09 GET candidates | F127-FN-06b, F127-FN-23 | ENG-RCT-02 (dup flag) |
| API-10 POST candidates | F127-FN-08, F127-FN-09 | ENG-RCT-02 |
| API-11 GET candidate/:id | F127-FN-23 | — |
| API-12 PUT candidate | F127-FN-10 | — |
| API-13 consent | F127-FN-11 | — |
| API-14 move-stage | F127-FN-12, F127-FN-24 | — |
| API-15 interviews | F127-FN-13 | — |
| API-16 scores | F127-FN-14 | — |
| API-17 offer create | F127-FN-15, F127-FN-25 | — |
| API-18 offer submit-approval | F127-FN-16, F127-FN-26 | — |
| API-19 offer approve | F127-FN-17 | — |
| API-20 offer send | F127-FN-18a | — |
| API-21 offer respond | F127-FN-18 | — |
| API-22 hire | F127-FN-19 | — |
| API-23 terminate | F127-FN-20 | — |
| API-24 funnel | F127-FN-22 | ENG-RCT-01 |
| API-25 export | F127-FN-22 | ENG-RCT-01 |

> **R8:** ทุก mutation row มี ≥1 Function ✅ (audit ผ่าน F127-FN-21 appendAudit เรียกภายในทุก mutation function).

---

## §2.X Cross-Module Contract ⭐ (จาก BRD §12.1 Downstream Impact Map)

| Downstream | รูปแบบ | Contract | Trigger | Payload หลัก |
|---|---|---|---|---|
| **On/Offboard (F-HR-ONBOARD)** | **Event (outbound · fire-and-forget)** | `recruit.candidate.hired` | candidate.stage → hired (API-22) | `{ candidate_id, position, grade_code, start_date, offer_snapshot:{salary,band_version_id}, hired_at }` — **ไม่มี employee_id (ไม่สร้าง employee)** |
| Salary Structure | Read (freeze) | EXT-BAND resolve | สร้าง offer/req | freeze `version_id` — ถ้า band แก้ภายหลัง offer เดิมยึด snapshot |
| Employee Master | Read (snapshot) | EXT-EMP | นัดสัมภาษณ์ / เลือก hiring manager | snapshot {id,name,position} |
| Notification (ENG-NOTIFY) | Event | interview_scheduled · offer_sent · selection_result · candidate_accepted | state transition | ผูก ntf-declaration (doa_* ไม่นับ) |
| Policy Center (DOA) | Resolve | EXT-DOA slot chain | submit-approval | slot[] resolve (ไม่ hardcode) |
| Policy Center (PDPA) | Read config | retention period | เก็บผู้สมัคร | display-only `retention_until` · **OQ-16** |

**Compensating / cancel:**
- ยกเลิก req (cancelled) ขณะ pipeline ค้าง → **OQ-17 `[AI-DEFAULT]`**: ไม่ยกเลิก candidate อัตโนมัติ + warn + reason (ดู 05_RULES EC-08).
- hired handoff = fire-and-forget → **ไม่มี compensating event รอบนี้** (OQ-15 · ฝั่งรับออกแบบ ack/rollback ภายหลัง).

> ทุกแถวที่มี data ไหล trace กับ 06_TESTS §6.9 (XT-01 handoff · XT-02 band freeze · XT-03 ntf).
