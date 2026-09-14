# 02_API — F-MKT-CONSENT ความยินยอม PDPA

> **Audience:** Backend developer (HTTP layer)
> **Purpose:** API contracts (CUBIC API Entity) + Cross-Module Contract
> **🚨 Iron Rule:** ห้าม business logic >5 บรรทัดที่นี่ — ย้าย 03_LOGIC §3.1 · **R8:** ทุก mutation API ต้องมี "Calls (Logic)"
> **🚨 BR-19/20:** `/consent/resolve` ตอบ **HTTP 200 เสมอ** · response schema = **locked contract** (เพิ่มฟิลด์ได้ ห้ามเปลี่ยนชื่อ/ความหมายเดิม)

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth | FN |
|---|---|---|---|---|---|
| F058-API-01 | GET | /api/v1/consent/purposes | list วัตถุประสงค์ + สถิติ | required | FN-03 |
| F058-API-02 | POST | /api/v1/consent/purposes | สร้างวัตถุประสงค์ + upload v1 | dpo | FN-01 |
| F058-API-03 | GET | /api/v1/consent/purposes/:code | รายละเอียด + versions[] | required | FN-03 |
| F058-API-04 | POST | /api/v1/consent/purposes/:code/versions | อัปโหลดเวอร์ชันใหม่ | dpo | FN-02 |
| F058-API-05 | POST | /api/v1/consent/purposes/:code/close | ปิดวัตถุประสงค์ | dpo | FN-04 |
| F058-API-06 | GET | /api/v1/consent/requests | list คำขอ | officer/dpo | FN-05 track |
| F058-API-07 | POST | /api/v1/consent/requests | สร้างคำขอ (single-screen) | officer/dpo | FN-05 |
| F058-API-08 | GET | /api/v1/consent/requests/:id | รายละเอียดคำขอ | officer/dpo | FN-06..09 |
| F058-API-09 | POST | /api/v1/consent/requests/:id/send | ส่ง/ส่งซ้ำ (mock) | officer/dpo | FN-06/07 |
| F058-API-10 | POST | /api/v1/consent/requests/:id/link-export | คัดลอกลิงก์ / ดาวน์โหลด QR (log) | officer/dpo | FN-08 |
| F058-API-11 | GET | /api/v1/consent/requests/:id/document | ดาวน์โหลดเอกสารเวอร์ชันปัจจุบัน | officer/dpo | FN-09 |
| F058-API-12 | GET | /api/v1/consent/recipient/:token | โหลด recipient view (public via token) | token | FN-10 |
| F058-API-13 | POST | /api/v1/consent/recipient/:token/answer | ส่งคำตอบยินยอม/ปฏิเสธรายข้อ | token | FN-10/11 |
| F058-API-14 | GET | /api/v1/consent/registry | ทะเบียน + กรองทุกมิติ | required | FN-13 |
| F058-API-15 | GET | /api/v1/consent/registry/:id | รายละเอียด + evidence 5 + history | required | FN-12/18 |
| F058-API-16 | GET | /api/v1/consent/subjects/:subjectRef | Customer 360 | required | FN-14 |
| F058-API-17 | POST | /api/v1/consent/registry/:id/withdraw | ถอน (มีผลทันที) | officer/dpo | FN-15 |
| F058-API-18 | GET | /api/v1/consent/near-expiry | รายการใกล้หมดอายุ ≤30 วัน | required | FN-16 |
| F058-API-19 | POST | /api/v1/consent/registry/:id/renew | ต่ออายุ (คำขอใหม่อ้างเดิม) | officer/dpo | FN-17 |
| F058-API-20 | POST | /api/v1/consent/resolve | ตรวจสิทธิ์ (locked contract, 200 เสมอ) | required (read) | FN-19/20 |

> **Common:** ทุก endpoint ต้อง `X-Tenant-Id` · ทุก mutation รับ `Idempotency-Key` header `[AI-DEFAULT]` (PR-7) · PUT/PATCH ไม่มี (ใช้ POST action ตาม state machine)
> **Role enforcement (FIX-02 · BR-25):** คอลัมน์ Auth = สิทธิ์ที่ต้อง enforce **ภายในทุก mutation function** (ไม่ใช่แค่ render ปุ่ม) — prototype ใช้ persona mirror `sec.can()`; ระบบจริง = role จากล็อกอิน (**OQ-05**). auditor = read-only ทุก endpoint (403 ทุก mutation) · จัดการ purpose (API-02/04/05) = dpo เท่านั้น
> **Sub-status / re-answer guards (FIX-01/05 · BR-23/26):** mutation ที่ผูก lifecycle เช็คสถานะก่อนทำ — answer (API-13) เฉพาะ draft/pending · send (API-09) เฉพาะ draft/pending · withdraw (API-17) เฉพาะ granted → มิฉะนั้น 422 (ดูราย endpoint)

---

## §2.2 Per-API Contract (คีย์ที่สำคัญ — ที่เหลือตาม pattern เดียวกัน)

### F058-API-02: POST /api/v1/consent/purposes  (FN-01)
| Field | Value |
|---|---|
| roles | dpo |
| headers | X-Tenant-Id, Idempotency-Key |

**Request (multipart — เอกสารแนบ, DECLARED-01):**
```
name: string (required)
channels: string[] (required, ≥1, subset of email/sms/line/phone/post)
lifespan_months: int (required, 1–120)
document: file (required — .pdf/.doc/.docx/.txt)  ← ต้องแนบ (BR-05)
```
**Validation (field-level ≤5 บรรทัด):** name required · channels ≥1 · lifespan 1–120 · document required
→ complex/orchestration → 03_LOGIC F058-FN-01 createPurpose

**Response 201:** `{ code:"PUR-0x", name, channels, lifespan_months, status:"active", current_ver:1, versions:[{v:1, doc_name, doc_type, published_at}] }`
**Errors:** 400 ERR_VALIDATION_FAILED · 403 ERR_INSUFFICIENT_ROLE · 422 BR_DOCUMENT_REQUIRED (ไม่แนบเอกสาร)
**Side effects:** INSERT T_consent_purpose + T_consent_policy_version(v1) + T_audit_log
**Calls (Logic):** F058-FN-01 createPurpose

### F058-API-04: POST /api/v1/consent/purposes/:code/versions  (FN-02)
**Request (multipart):** `document: file (required)`
**Response 200:** `{ code, current_ver:<n+1>, stale_count:<N>, versions:[...] }` — N = consent เวอร์ชันเดิมที่ไม่ครอบคลุม (BR-06)
**Errors:** 422 BR_DOCUMENT_REQUIRED · 409 ERR_STALE_DATA (optimistic lock `[AI-DEFAULT]`)
**Side effects:** INSERT T_consent_policy_version(v+1) · UPDATE purpose.current_ver · emit CSQ `policy.version_published`
**Calls (Logic):** F058-FN-02 publishPolicyVersion · F058-FN-17 computePolicyStale

### F058-API-05: POST /api/v1/consent/purposes/:code/close  (FN-04)
**Response 200:** `{ code, status:"closed" }`
**BR-14:** ปิดแล้วสร้างคำขอใหม่ไม่ได้ · consent เดิมคงอยู่ (ไม่ลบ, BR-17)
**Side effects:** UPDATE status=closed · emit CSQ `purpose.closed`
**Calls (Logic):** F058-FN-04 closePurpose

### F058-API-07: POST /api/v1/consent/requests  (FN-05 · single-screen)
**Request:** `{ subject_ref, purpose_codes:string[] (active only), channel }`
**Validation:** subject required · purpose_codes ≥1 · channel ต้องอยู่ในช่องทางที่ **ทุก** purpose รองรับ (BR-03) · purpose ต้อง status=active (BR-14)
**Response 201:** `{ code:"REQ-xxxx", subject_ref, purpose_codes, channel, status:"draft", link_token, qr_ref }`
**Errors:** 400 · 422 BR_CHANNEL_NOT_SUPPORTED · 422 BR_PURPOSE_CLOSED
**Side effects:** INSERT T_consent_request + T_consent_request_purpose[]
**Calls (Logic):** F058-FN-05 createRequestRecord
> **LOCK-07:** single-screen (no wizard/stepper)

### F058-API-09: POST /api/v1/consent/requests/:id/send  (FN-06/07)
**Request:** `{ channel }`
**Guard (FIX-05):** ส่ง/ส่งซ้ำได้เฉพาะ request.status ∈ {draft, pending} — answered/expired → 422 BR_REQUEST_CLOSED ("คำขอนี้ปิดแล้ว") · role check ใน function (FIX-02)
**Response 200:** `{ request_id, status:"pending", send_seq:<N>, vers:{ "<purpose_code>": <version>, ... } }`
**BR-18:** ส่งซ้ำ = INSERT send record (ครั้งที่ N) — **ไม่สร้างคำขอใหม่** · **mock** (ไม่ส่งอีเมล/LINE จริง — toast "บันทึกการส่งทาง<channel> (จำลอง...)")
**BR-24 (FIX-03 · version snapshot):** แต่ละ send record บันทึก **`vers` = snapshot เวอร์ชันนโยบายปัจจุบันต่อ purpose ณ เวลาส่ง** (`snapshotVers()`) → panel "เนื้อหาที่ให้เซ็น" render เวอร์ชันที่ส่งจริง (ไม่ใช่ current) + เตือนเมื่อ current ใหม่กว่า · `viewPolicy(code, ver)` โหลดเวอร์ชันประวัติจาก T_consent_policy_version
**Side effects:** INSERT T_consent_request_send (พร้อม `vers` jsonb) · UPDATE request.status=pending (ครั้งแรก)
**Calls (Logic):** F058-FN-06 recordSend → F058-FN-21 snapshotVers

### F058-API-12: GET /api/v1/consent/recipient/:token  (FN-10 load)
**Auth:** token (public link · ไม่ต้อง JWT) — **read-only** โหลดคำขอ + เอกสารเวอร์ชันที่ส่งของแต่ละ purpose (จาก send snapshot `vers`, FIX-03)
**Response 200 (form):** `{ request:{...}, purposes:[{code, name, doc_name, doc_body, policy_version}] }`
**Response 200 (closed-state · FIX-01):** ถ้า request.status ∉ {draft, pending} → `{ closed:true, status, answered_at }` — client แสดงหน้าสถานะปิด "คำขอนี้ตอบแล้ว เมื่อ..." **ไม่แสดงฟอร์ม** (ลูกค้าเปิดลิงก์ซ้ำ)
**Errors:** 200 พร้อม `{ expired:true }` ถ้า request เกินกำหนด (lapsed) — ไม่ 404
**Calls (Logic):** F058-FN-08 buildRecipientView

### F058-API-13: POST /api/v1/consent/recipient/:token/answer  (FN-10/11)
**Request:** `{ verified:true, answers:[{purpose_code, grant:boolean}] }`
**Guard (FIX-01 · BR-23 · re-answer block — CRITICAL):** applyAnswers เช็คแรกสุด — request.status ต้อง ∈ {draft, pending} เท่านั้น · answered/closed/expired → **422 BR_REQUEST_CLOSED** ("คำขอนี้ปิดแล้ว — ตอบซ้ำไม่ได้") **ก่อน** supersede/INSERT ใด ๆ → กัน evidence chain ถูกเขียนทับ (bypass B1/B2) · guard นี้คุมทั้ง officer-answer และ recipient-submit (จุดเดียวที่ applyAnswers)
**Guard (FIX-02):** role check ใน function (sign) — auditor เรียกตรง → 403/ปฏิเสธ (ไม่ใช่แค่ render)
**Validation:** `verified` ต้อง true (BR-15 ยืนยันตัวตนก่อน — mock, OQ-03) · answers ครบทุก purpose ในคำขอ
**Response 200:** `{ granted:N, declined:M, evidence_complete:true }`
**Errors:** **422 BR_REQUEST_CLOSED** (answered=terminal, FIX-01) · 422 BR_IDENTITY_NOT_VERIFIED ("กรุณายืนยันตัวตนก่อนส่งคำตอบ") · 422 BR_ANSWERS_INCOMPLETE · 403 ERR_INSUFFICIENT_ROLE
**Side effects (per purpose · เฉพาะเมื่อผ่าน guard):** supersede คู่ triple เดิม · INSERT T_consent (granted/declined) + T_consent_evidence(5) + T_consent_history · **UPDATE request.status=answered + set `answered_at`** (terminal, BR-23) · emit CSQ `consent.granted` / `consent.declined`
**Calls (Logic):** F058-FN-09 applyAnswers (guard answered=terminal) → F058-FN-10 supersede, F058-FN-11 buildEvidence

### F058-API-14: GET /api/v1/consent/registry  (FN-13)
**Query:** `search, status, channel, purpose, near_expiry, limit, offset`
**Response 200:** `{ data:[...consent + computed eff_status/near_expiry/policy_stale], total, stats:{granted, withdrawn, near_expiry, total} }`
**Calls (Logic):** F058-FN-11 filterConsents · F058-ENG-02 consent-status-evaluator (compute)

### F058-API-17: POST /api/v1/consent/registry/:id/withdraw  (FN-15)
**Request:** `{ reason (required), via (required) }` (BR-10)
**Guard (FIX-05 · BR-26):** ถอนได้เฉพาะ eff_status = granted — withdrawn/declined/expired/pending → 422 BR_NOT_GRANTED ("รายการนี้ไม่อยู่ในสถานะยินยอม") → กัน history/CSQ reversal ยิงซ้ำ (bypass B3) · role check ใน function (FIX-02)
**Response 200:** `{ id, status:"withdrawn", updated_at }`
**BR-09:** มีผลทันที · **ไม่ต้องอนุมัติ** (LOCK-04) · caller cache ต้องล้างทันที (BR-21 — ดู §2.X)
**Side effects:** UPDATE status=withdrawn · INSERT T_consent_history(reason,via) · emit CSQ `consent.withdrawn` **reversal_of=grant_event_id** (BR-CSQ-04)
**Calls (Logic):** F058-FN-13 withdrawConsent

### F058-API-19: POST /api/v1/consent/registry/:id/renew  (FN-17)
**Response 201:** `{ new_request_code:"REQ-xxxx", ref_old:<consent id> }`
**BR-13:** สร้าง **คำขอใหม่อ้างเดิม** — **ไม่แก้ expires_at เดิม**
**Side effects:** INSERT T_consent_request(ref_old) · emit CSQ `consent.renew_requested`
**Calls (Logic):** F058-FN-14 renewConsent → F058-FN-05 createRequestRecord

### F058-API-20: POST /api/v1/consent/resolve  ⭐ (FN-19/20 · LOCKED CONTRACT · 200 เสมอ)
| Field | Value |
|---|---|
| roles | required (read) — ระบบปลายทาง / dev |
| **HTTP status** | **200 เสมอ** (BR-19) — never 404/500 for business outcomes |

**Request:** `{ subject, purpose, channel }`
**Response 200 (LOCKED — BR-20, verbatim จาก `resolveConsent()`):**
```json
{
  "subject": "CUS-1001",
  "purpose": "PUR-01",
  "channel": "email",
  "allowed": true,
  "status": "granted",
  "policy_version": 2,
  "granted_at": "iso8601 | null",
  "expires_at": "iso8601 | null",
  "found": true,
  "reason": "ยินยอมอยู่ (นโยบาย v2) หมดอายุ ..."
}
```
**never_asked case (FN-20 — MUST):**
```json
{
  "subject": "...", "purpose": "...", "channel": "...",
  "allowed": false, "status": "never_asked",
  "policy_version": null, "granted_at": null, "expires_at": null,
  "found": false,
  "reason": "ยังไม่เคยขอความยินยอมสำหรับคู่นี้ — ค่าเริ่มต้นคือส่งไม่ได้"
}
```
> **status enum (observed):** granted / declined / withdrawn / expired / pending / **never_asked** · closed purpose → allowed:false + reason ต่อท้าย "· วัตถุประสงค์นี้ถูกปิดใช้งานแล้ว"
> **Contract lock:** เพิ่มฟิลด์ได้ · ห้ามเปลี่ยนชื่อ/ความหมาย `allowed/status/found/reason/policy_version/granted_at/expires_at` (BR-20)
**Calls (Logic):** F058-ENG-01 consent-resolution-engine (via F058-FN-20 resolveConsent) · F058-ENG-02 consent-status-evaluator

---

## §2.3 Common Concerns
- **Double-submit backstop (FIX-04 · BR-26):** ทุก mutation function มี `_busy` re-entrancy guard (UI) + ปุ่ม loading state (Rule #44) — ป้องกันคำขอ/รายการซ้ำจาก double-click (bypass B8) · เป็น backstop คู่กับ server-side `Idempotency-Key` (ไม่แทนกัน)
- **Idempotency (PR-7 `[AI-DEFAULT]`):** mutation รับ `Idempotency-Key` → cache 24 ชม. · same key+body → cached · CSQ envelope มี idempotency_key ของตัวเอง (BR-CSQ-02)
- **Optimistic Locking (PR-2 `[AI-DEFAULT]`):** purpose version publish + consent withdraw ใช้ `version` column → mismatch = 409 ERR_STALE_DATA
- **Multi-Tenant:** ทุก endpoint `X-Tenant-Id` → RLS
- **Audit:** ทุก mutation → T_audit_log (middleware) + T_consent_history (BR-16)
- **Public token endpoints (API-12/13):** rate-limit + token expiry (request timeout 30 วัน) · ไม่ leak PII เกินที่จำเป็น

---

## §2.4 API → Logic Trace (Anchor for R8)
> Authoritative: `03_LOGIC §3.3`

| API | Functions | Engines |
|---|---|---|
| API-01 GET purposes | FN-03 | ENG-02 (stats) |
| API-02 POST purposes | FN-01 | — |
| API-03 GET purpose/:code | FN-03 | — |
| API-04 POST versions | FN-02, FN-17 | — |
| API-05 POST close | FN-04 | — |
| API-06 GET requests | FN-11 | — |
| API-07 POST requests | FN-05 | — |
| API-08 GET request/:id | — (read) | — |
| API-09 POST send | FN-06, FN-21 (snapshotVers) | — |
| API-10 POST link-export | FN-07 | — |
| API-11 GET document | FN-07 | — |
| API-12 GET recipient | FN-08 | — |
| API-13 POST answer | FN-09, FN-10, FN-11 | — |
| API-14 GET registry | FN-11 | ENG-02 |
| API-15 GET registry/:id | FN-12 | ENG-02 |
| API-16 GET subject 360 | FN-11 | ENG-02 |
| API-17 POST withdraw | FN-13, FN-19(emit) | — |
| API-18 GET near-expiry | FN-18 | ENG-02 |
| API-19 POST renew | FN-14, FN-05 | — |
| API-20 POST resolve | FN-20 | ENG-01, ENG-02 |

> **R8 Check:** ทุก mutation row มี ≥1 Function/Engine ✅

---

## §2.X Cross-Module Contract (BRD §12.1 Downstream Impact)

> **FIX-06 contract anchors** — 3 consumer ประกาศชัด (Feature List F058) · anchor เป็น comment ในหน้าจอ (head + tab resolve + registry) · **display-only — ไม่ mock หน้าจอ feature อื่น**

| Downstream | รูปแบบ | Contract | Trigger | Payload หลัก |
|---|---|---|---|---|
| **F136 Broadcast** (control) | Endpoint (ปลายทางเรียก) | `POST /api/v1/consent/resolve` (200 เสมอ, locked) → ตรวจ opt-in **ก่อนส่ง Email/SMS block อัตโนมัติ** | ก่อนส่งทุกครั้ง | { subject, purpose, channel } → { allowed, status, reason } |
| **F031 Customer 360** (data) | Endpoint / read | `POST /consent/resolve` + ทะเบียน consent (สถานะผูกลูกค้า) | เปิดหน้าลูกค้า | subject → consent status per purpose |
| **F157 DSAR** (data) | Data source (read) | ทะเบียน consent + **evidence 5 + history append-only** = ฐานข้อมูลประกอบคำขอ DSAR | DSAR request | subject → consent + evidence + timeline (เดิม E3 consent-receipt deferred) |
| **Backend Enforcement Gate (F143)** | Registration | `/consent/*` ต้องขึ้นทะเบียน + review 4 ขั้น | deploy | endpoint manifest — **hard dependency go-live (BR-22 → OQ-04)** |
| 7C Consequence Engine (F-CSQ-01) | Event (declare-only) | `POST /csq/events` envelope | ทุก state change | 7 events (ดู 03_LOGIC §3.4) · reversal_of ตอนถอน |
| Caller cache contract (BR-21) | Contract (no UI) | ผู้เรียกแคชผล resolve **≤5 นาที** + **ล้างทันทีเมื่อถอน** | — | documented only → **OQ-02** |

- **Compensating:** ถอน → resolve ตอบ `allowed:false` ทันที + caller ล้างแคช (BR-21) · CSQ ส่ง `consent.withdrawn` reversal_of (ไม่ลบผลเดิม)
- ทุกแถว trace → 06_TESTS §6.9 (XT-01..05)
