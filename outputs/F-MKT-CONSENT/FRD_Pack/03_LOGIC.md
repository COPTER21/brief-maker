# 03_LOGIC — F-MKT-CONSENT ความยินยอม PDPA

> **Audience:** BE dev (business logic layer)
> **Scope:** non-HTTP logic — functions, state evaluation, evidence, CSQ declare-only, resolve
> **CUBIC:** §3.1 Functions = scope-local · §3.2 Engines = CUBIC candidate
> **R8:** ทุก mutation API → ≥1 Function/Engine ใน §3.3
> **แหล่งอ้าง (observed):** ชื่อ function ตรงกับ `consent-pdpa.html` — FRD สกัด business logic ออกจาก HTTP/render

---

## §3.1 Functions (Scope-Local · camelCase)

### F058-FN-01: `createPurpose`
- **Purpose:** สร้างวัตถุประสงค์ใหม่พร้อมเอกสารนโยบาย v1 (DECLARED-01 upload)
- **Input:** `{ name, channels[], lifespan_months, document{name,type,ref,size} }`
- **Output:** `Purpose | ValidationError[]`
- **Invoked by:** F058-API-02
- **Calls:** —
- **Side effects:** INSERT T_consent_purpose · INSERT T_consent_policy_version(v1) · audit
- **Error cases:** BR_DOCUMENT_REQUIRED, ERR_VALIDATION_FAILED
- **Iron rule:** ✅ no HTTP terms
- **HTML ref:** `submitPurCreate()` (validates name/≥1 channel/1–120/แนบเอกสาร)

### F058-FN-02: `publishPolicyVersion`
- **Purpose:** ออกเวอร์ชันเอกสารใหม่ (v+1) + คำนวณ consent เวอร์ชันเดิมที่ไม่ครอบคลุม
- **Input:** `{ purpose_code, document{...}, expected_version }`
- **Output:** `{ new_ver, stale_count }`
- **Invoked by:** F058-API-04
- **Calls:** F058-FN-17 computePolicyStale
- **Side effects:** INSERT T_consent_policy_version(immutable) · UPDATE purpose.current_ver, version · emit CSQ `policy.version_published`
- **Error cases:** BR_DOCUMENT_REQUIRED, ERR_STALE_DATA (409)
- **Iron rule:** ✅ · **HTML ref:** `doPublishVersion()` (toast "ออกเอกสาร vN แล้ว · M รายการต้องขอใหม่")

### F058-FN-03: `computePurposeStats`
- **Purpose:** สถิติต่อวัตถุประสงค์ (ยินยอม/ถอน/หมดอายุ/%ครอบคลุม)
- **Input:** `{ purpose_code }` · **Output:** `{ granted, withdrawn, expired, coverage_pct }`
- **Invoked by:** F058-API-01, API-03 · **Calls:** F058-ENG-02 · **Side effects:** — (read)
- **Iron rule:** ✅ · **HTML ref:** `purposeStats()`

### F058-FN-04: `closePurpose`
- **Purpose:** ปิดวัตถุประสงค์ (ห้ามคำขอใหม่ · consent เดิมคงอยู่)
- **Input:** `{ purpose_code }` · **Output:** `Purpose`
- **Invoked by:** F058-API-05 · **Side effects:** UPDATE status=closed · emit CSQ `purpose.closed`
- **Error:** — · **Iron rule:** ✅ · **HTML ref:** `doClosePurpose()`

### F058-FN-05: `createRequestRecord`
- **Purpose:** สร้างคำขอ single-screen (subject + purposes[] + channel → link + QR)
- **Input:** `{ subject_ref, purpose_codes[], channel, ref_old? }`
- **Output:** `ConsentRequest | ValidationError[]`
- **Invoked by:** F058-API-07, F058-FN-14 (renew), F058-FN-15 (reconsent)
- **Calls:** — · **Side effects:** INSERT T_consent_request + T_consent_request_purpose[] · gen link_token + qr
- **Error:** BR_CHANNEL_NOT_SUPPORTED (BR-03), BR_PURPOSE_CLOSED (BR-14)
- **Iron rule:** ✅ · **HTML ref:** `createRequestRecord()` / `submitReqCreate()` — **LOCK-07 single-screen**

### F058-FN-06: `recordSend`
- **Purpose:** บันทึกการส่ง/ส่งซ้ำ (mock) — ครั้งที่ N ในคำขอเดิม
- **Input:** `{ request_id, channel }` · **Output:** `{ send_seq, status }`
- **Invoked by:** F058-API-09 · **Side effects:** INSERT T_consent_request_send · UPDATE status=pending (ครั้งแรก) · **ไม่ส่งจริง (BR: mock)**
- **Iron rule:** ✅ · **HTML ref:** `sendVia()` (toast จำลอง) · BR-18 (ไม่สร้างคำขอใหม่)

### F058-FN-07: `recordLinkExport`
- **Purpose:** log การนำลิงก์/QR ออก + ดาวน์โหลดเอกสารของคำขอ
- **Input:** `{ request_id, kind }` (link_export/qr_download/document) · **Output:** `void`
- **Invoked by:** F058-API-10, API-11 · **Side effects:** INSERT T_consent_request_send(kind)
- **Iron rule:** ✅ · **HTML ref:** `copyLink()`, `downloadQR()`, `downloadPdfForm()`/`downloadBlob()`

### F058-FN-08: `buildRecipientView`
- **Purpose:** ประกอบข้อมูลหน้า recipient — คำขอ + เอกสารเวอร์ชันปัจจุบันรายวัตถุประสงค์
- **Input:** `{ link_token }` · **Output:** `{ request, purposes[{code,name,doc_name,doc_body,policy_version}] } | { expired:true }`
- **Invoked by:** F058-API-12 · **Side effects:** — (read) · lapsed → expired:true (ไม่ 404)
- **Iron rule:** ✅ · **HTML ref:** `openRecipientView()`/`recipientViewHTML()`/`renderRecipient()`

### F058-FN-09: `applyAnswers` ⭐
- **Purpose:** แปลงคำตอบผู้รับ → registry rows (granted/declined ต่อ purpose) + evidence 5 + history + supersede + CSQ
- **Input:** `{ request, answers:[{purpose_code, grant}], verified }`
- **Output:** `{ granted, declined }`
- **Invoked by:** F058-API-13
- **Calls:** F058-FN-10 supersede, F058-FN-11 buildEvidence, F058-FN-19 emitConsequence
- **Side effects (per purpose):** supersede คู่ triple เดิม · INSERT T_consent(granted/declined) + T_consent_evidence(5) + T_consent_history · UPDATE request.status=answered · emit `consent.granted`/`consent.declined`
- **Error:** BR_IDENTITY_NOT_VERIFIED (verified=false), BR_ANSWERS_INCOMPLETE
- **Iron rule:** ✅ (render() ถูกถอดออก — เป็น HTTP/UI) · **HTML ref:** `applyAnswers()` (policy_version = snapshot p.currentVer, BR-06)

### F058-FN-10: `supersede`
- **Purpose:** ปิดสถานะ record คู่ triple เดิม (subject×purpose×channel) เมื่อมี record ใหม่ — คงไว้เป็นหลักฐาน (ไม่ลบ, BR-17)
- **Input:** `{ subject_ref, purpose_code, channel, new_id }` · **Output:** `void`
- **Invoked by:** F058-FN-09 · **Side effects:** UPDATE old.superseded_by = new_id
- **Iron rule:** ✅ · **HTML ref:** `supersede()` · รักษา partial-unique triple (BR-01)

### F058-FN-11: `buildEvidence` + `filterConsents`
- **Purpose (buildEvidence):** สร้าง object หลักฐาน 5 อย่าง (BR-15)
- **Input:** `{ request_channel, id_method, policy_version, ip_device }` · **Output:** `Evidence{answered_at, request_channel, id_method, policy_version, ip_device}`
- **Purpose (filterConsents):** กรองทะเบียนทุกมิติ (search/status/channel/purpose/near-expiry) + Customer 360
- **Invoked by:** F058-FN-09 (evidence) · F058-API-14/16 (filter)
- **Calls:** F058-ENG-02 (compute eff status) · **Side effects:** — (read/build)
- **Iron rule:** ✅ · **HTML ref:** `ev()`, `filteredConsents()`, `finder()`

### F058-FN-12: `getConsentDetail`
- **Purpose:** รายละเอียด consent 1 รายการ (evidence 5 + timeline append-only)
- **Input:** `{ consent_id }` · **Output:** `{ consent, evidence, history[], computed }`
- **Invoked by:** F058-API-15 · **Calls:** F058-ENG-02 · **Side effects:** — (read)
- **Iron rule:** ✅ · **HTML ref:** `openConsentView()`/`consentViewDrawer()`/`evItem()`

### F058-FN-13: `withdrawConsent`
- **Purpose:** ถอนความยินยอม (เหตุผล+ช่องทาง) มีผลทันที ไม่ต้องอนุมัติ
- **Input:** `{ consent_id, reason, via }` · **Output:** `Consent`
- **Invoked by:** F058-API-17
- **Calls:** F058-FN-19 emitConsequence
- **Side effects:** UPDATE status=withdrawn, updated_at · INSERT T_consent_history(reason,via) · emit `consent.withdrawn` **reversal_of=grant_event_id**
- **Error:** BR_WITHDRAW_REASON_REQUIRED, BR_WITHDRAW_CHANNEL_REQUIRED (BR-10)
- **Iron rule:** ✅ · **HTML ref:** `doWithdraw()` (BR-09/10 · toast "ถอนความยินยอมแล้ว — มีผลทันที...")

### F058-FN-14: `renewConsent`
- **Purpose:** ต่ออายุ = สร้างคำขอใหม่อ้างเดิม (ไม่แก้ expires_at เดิม, BR-13)
- **Input:** `{ consent_id }` · **Output:** `ConsentRequest`
- **Invoked by:** F058-API-19 · **Calls:** F058-FN-05, F058-FN-19 (`consent.renew_requested`)
- **Side effects:** INSERT T_consent_request(ref_old) · **HTML ref:** `openRenew()`

### F058-FN-15: `reConsent`
- **Purpose:** ขอความยินยอมใหม่กับ consent ที่ stale (policy version ใหม่) — คำขอใหม่อ้างเดิม
- **Input:** `{ consent_ids[] }` · **Output:** `{ created_count }`
- **Invoked by:** F058-API-04 flow / registry action · **Calls:** F058-FN-05, F058-FN-19 (`consent.reconsent_requested`)
- **Side effects:** INSERT T_consent_request(ref_old) per code · **HTML ref:** `reConsent()`

### F058-FN-16: `computeEffStatus` *(delegates ENG-02)*
- **Purpose:** สถานะที่แสดงจริง (granted→expired เมื่อ daysLeft<0)
- **Input:** `Consent` · **Output:** `granted|declined|withdrawn|pending|expired`
- **Invoked by:** ทุก read ที่แสดงสถานะ · **Calls:** F058-ENG-02 · **HTML ref:** `effStatus()`

### F058-FN-17: `computePolicyStale` *(delegates ENG-02)*
- **Purpose:** consent.policy_version < purpose.current_ver → stale (BR-06)
- **Input:** `Consent` · **Output:** `boolean` + stale_count · **HTML ref:** `policyStale()`, `staleCount()`

### F058-FN-18: `computeNearExpiry` *(delegates ENG-02)*
- **Purpose:** 0 ≤ daysLeft ≤ 30 → near-expiry (เตือน ไม่บล็อก, BR-12)
- **Input:** `Consent` · **Output:** `{ near_expiry:boolean, days_left }`
- **Invoked by:** F058-API-18, registry · **HTML ref:** `nearExpiry()`, `daysLeft()`

### F058-FN-19: `emitConsequence` ⭐ (CSQ declare-only)
- **Purpose:** สร้าง Event Envelope ส่งเข้า 7C Engine — **declare-only** (ไม่ตีมูลค่า ไม่ประทับผลรายท่อ · LOCK-CSQ-04/05/06)
- **Input:** `{ event_id, ref, payload{...reversal_of?} }`
- **Output:** `Envelope{ feature:'F-MKT-CONSENT', event_id, ref, idempotency_key:'F-MKT-CONSENT:<ref>:<event_id>', reversal_of, payload }`
- **Invoked by:** FN-02/04/09/13/14/15
- **Calls:** external `POST /csq/events` (F-CSQ-01 — ดู §3.4)
- **Side effects:** INSERT T_consent_csq_outbox (idempotency_key unique · masked payload BR-CSQ-03)
- **Iron rule:** ✅ pure envelope · **HTML ref:** `emitConsequence()` (BR-CSQ-01..05)
- **⚠️ LOCK:** ห้ามประกาศ/คำนวณท่อ OC (มาจาก Operation Process) · DC ระดับเอกสาร (มาจาก DOA engine) · SC — ประกาศซ้ำ = register reject 422

### F058-FN-20: `resolveConsent` *(wrapper ของ ENG-01)*
- **Purpose:** ตรวจสิทธิ์ triple → allowed + status + reason (locked contract)
- **Input:** `{ subject, purpose, channel }` · **Output:** resolve contract object (ดู 02_API-20)
- **Invoked by:** F058-API-20 · **Calls:** F058-ENG-01, F058-ENG-02 · **Side effects:** — (read-only, LOCK #9)
- **Iron rule:** ✅ · **HTML ref:** `resolveConsent()`/`runResolve()`

---

## §3.2 Engines (Reusable / CUBIC-Registered · kebab-case)

### F058-ENG-01: `consent-resolution-engine` [NEW]
| Field | Value |
|---|---|
| code | `consent-resolution-engine` |
| name | Consent Resolution Engine |
| category | policy-evaluation |
| status | DRAFT (register CUBIC ตอน hand-off) |
| owner | F-MKT-CONSENT |

**Input Schema:** `{ subject, purpose, channel, consents[], purpose_meta{status,current_ver} }`
**Output Schema (LOCKED — BR-20):** `{ subject, purpose, channel, allowed, status, policy_version, granted_at, expires_at, found, reason }`
**Logic Outline:**
1. filter consents ตาม triple (subject×purpose×channel) เรียง updated desc
2. ว่าง → `{ allowed:false, status:'never_asked', found:false, reason:'ยังไม่เคยขอ...' }` (BR-04/19/FN-20)
3. เอา record ล่าสุด → eval eff status (ENG-02): granted→check policyStale → allowed/false + reason
4. expired/withdrawn/declined/pending → allowed:false + reason เฉพาะกรณี (lapsed≠declined, BR-08)
5. purpose.status=closed → allowed:false + reason ต่อท้าย
**Used by:** F-MKT-CONSENT (this) · **Backend Enforcement Gate F143** (planned — resolve gate)
**Iron rule:** ✅ pure (no I/O direct — รับ consents[] เข้า) · reusable 2+ · substantial (named algorithm)
**Registration:** DRAFT → register + expose ผ่าน `/consent/resolve` (F143 review 4 ขั้น, BR-22)

### F058-ENG-02: `consent-status-evaluator` [NEW]
| Field | Value |
|---|---|
| code | `consent-status-evaluator` |
| name | Consent Status Evaluator |
| category | validation / date-calculation |
| status | DRAFT |
| owner | F-MKT-CONSENT |

**Input Schema:** `{ consent{status, granted_at, expires_at, policy_version}, current_ver, now }`
**Output Schema:** `{ eff_status, policy_stale:boolean, near_expiry:boolean, days_left }`
**Logic Outline:**
1. daysLeft = (expires_at − now) / วัน
2. granted & daysLeft<0 → eff_status='expired' (computed, ไม่เก็บ DB)
3. granted & 0≤daysLeft≤30 → near_expiry=true (BR-12)
4. policy_version < current_ver → policy_stale=true (BR-06)
**Used by:** ENG-01 + F058-API-14/15/16/18 · **Iron rule:** ✅ pure date/status calc · reusable · **HTML ref:** `effStatus()`,`policyStale()`,`nearExpiry()`,`daysLeft()`

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| API-01 | GET | /consent/purposes | FN-03 | ENG-02 |
| API-02 | POST | /consent/purposes | FN-01 | — |
| API-03 | GET | /consent/purposes/:code | FN-03 | — |
| API-04 | POST | /consent/purposes/:code/versions | FN-02, FN-17 | — |
| API-05 | POST | /consent/purposes/:code/close | FN-04 | — |
| API-06 | GET | /consent/requests | FN-11 | — |
| API-07 | POST | /consent/requests | FN-05 | — |
| API-08 | GET | /consent/requests/:id | — (single read) | — |
| API-09 | POST | /consent/requests/:id/send | FN-06 | — |
| API-10 | POST | /consent/requests/:id/link-export | FN-07 | — |
| API-11 | GET | /consent/requests/:id/document | FN-07 | — |
| API-12 | GET | /consent/recipient/:token | FN-08 | — |
| API-13 | POST | /consent/recipient/:token/answer | FN-09, FN-10, FN-11 | — |
| API-14 | GET | /consent/registry | FN-11 | ENG-02 |
| API-15 | GET | /consent/registry/:id | FN-12 | ENG-02 |
| API-16 | GET | /consent/subjects/:subjectRef | FN-11 | ENG-02 |
| API-17 | POST | /consent/registry/:id/withdraw | FN-13, FN-19 | — |
| API-18 | GET | /consent/near-expiry | FN-18 | ENG-02 |
| API-19 | POST | /consent/registry/:id/renew | FN-14, FN-05, FN-19 | — |
| API-20 | POST | /consent/resolve | FN-20 | ENG-01, ENG-02 |

### Trace Verification (Self-Check)
- [x] ทุก mutation API (POST) มี ≥1 Function/Engine
- [x] ไม่มี orphan Function — FN-01..20 ปรากฏใน trace (FN-15 reConsent = registry action/API-04 flow; FN-16 delegate ใช้ทุก read; FN-19 ใน withdraw/renew/version/close)
- [x] ไม่มี orphan Engine — ENG-01 (API-20), ENG-02 (API-01/14/15/16/18/20 + ENG-01)
- [x] ไม่มี hidden logic ใน 02_API

---

## §3.4 Dependencies

### External Engine/Feature called
- **F-CSQ-01 (7C Consequence Engine)** — `POST /csq/events` (declare-only) · FN-19 emits **7 events**:
  1. `consent.granted` · 2. `consent.declined` · 3. `consent.withdrawn` (reversal_of) · 4. `consent.renew_requested` · 5. `consent.reconsent_requested` · 6. `policy.version_published` · 7. `purpose.closed`
  > **ห้ามประกาศซ้ำท่อ OC/DC/SC** (มาอัตโนมัติจาก Operation Process / DOA engine) — ประกาศซ้ำ = 422
- **Backend Enforcement Gate (F143)** — เรียก ENG-01 ผ่าน `/consent/resolve` (BR-22 register + 4-step review)
- **Customer Master (external)** — subject_ref lookup (ไม่ join)

### External that calls into this feature
- F143 + campaign features → `consent-resolution-engine` (ผ่าน API-20)

---

## §3.5 Open Questions / Locked Decisions Referenced
- **LD-01** (07): content model = **upload** (DECLARED-01) — old ≥40-char free-text rule REPLACED by "ต้องแนบเอกสาร"
- **LD-02** (07): resolve contract locked (BR-20) — ENG-01 output schema immutable
- **LD-03** (07): no approval chain (LOCK-04) — withdraw immediate
- **LD-04** (07): ENG-01/02 register CUBIC ตอน hand-off (DRAFT now)
- **OQ-03**: id_method จริง (checkbox mock) — FN-09 evidence.id_method ปัจจุบัน = "ลิงก์ที่ส่งถึงเจ้าตัว" (mock)
- **[AI-DEFAULT]**: optimistic lock (FN-02/13), idempotency-key header (all mutation) — ดู 05_RULES §5.5

---

## Audience Cheat-Sheet
| Reader | Sections |
|---|---|
| BE dev | §3.1 + §3.2 + §3.3 |
| QA | §3.3 + FN Side effects + ENG I/O |
| Architect / CUBIC | §3.2 + §3.4 |
| PM | §3.3 (table) |
