# CTX — F-MKT-CONSENT: ความยินยอม PDPA (Consent Management)

> **derived from:** FRD_F-MKT-CONSENT v1.1 (2026-09-14) · **generated:** 2026-09-14
> **module:** การตลาด (Marketing · PDPA/Policy Center scope) · **feature code:** F-MKT-CONSENT (plan id F058) · **wave:** W1 · **variant:** FULL · **status:** active (FRD DRAFT · re-issued หลัง BA-gate fixes · awaiting gate 2)
> ⚠ Derived artifact — source of truth คือ FRD Pack · ถ้า FRD revise ต้อง regen CTX
> **v1.1 delta:** re-sync BA-gate round (FIX-01..08) — answered=terminal (BR-23) · send version snapshot `vers` (BR-24) · role check ใน mutation function (BR-25) · double-submit + sub-status guard (BR-26) · contract anchors F136/F031/F157 (FIX-06) · +OQ-CNS-01/02/03

---

## 1. Summary

ระบบจัดการความยินยอม PDPA — **ต้นน้ำของสิทธิ์การสื่อสารทุกช่องทางการตลาด**. DPO/เจ้าหน้าที่การตลาดสร้าง **วัตถุประสงค์ (purpose)** พร้อม **เอกสารนโยบายแบบ versioned (อัปโหลด · DECLARED-01)**, ออกคำขอความยินยอมแบบ single-screen แล้วส่ง/ส่งซ้ำ/คัดลอกลิงก์+QR (ส่งเป็น **mock**). เจ้าของข้อมูลเปิด **recipient view** (surface เต็มจอนอก ERP · เข้าผ่าน token) → อ่านเอกสาร → ยืนยันตัวตน → ยินยอม/ไม่ยินยอม **รายวัตถุประสงค์** → เก็บ **หลักฐาน 5 อย่าง**. ทะเบียนใช้ **triple key (subject × purpose × channel)** แบบ **default-deny** — 1 active record ต่อ triple. ถอนได้ทันที (ไม่ต้องอนุมัติ · LOCK-04), ต่ออายุ = คำขอใหม่อ้างเดิม. คำขอ **ตอบได้ครั้งเดียว (answered = terminal · BR-23)** — เปลี่ยนใจ = คำขอใหม่/withdraw. Interface หลักต่อ feature อื่น = **`POST /consent/resolve`** (ตอบ **HTTP 200 เสมอ** · สัญญาผลล็อก) ให้ระบบปลายทางเช็คก่อนส่งทุกครั้ง. ทุก state change ประกาศ event เข้า **7C Consequence Engine (declare-only)**. **Standalone** (plan `dep=""`) · consumers = F136 Broadcast (control) · F031 Customer 360 (data) · F157 DSAR (data).

## 2. Data Contract

> Source: FRD 04_DB. เจ้าของ 9 ตาราง (+ T_audit_log shared) · multi-tenant RLS ทุกตาราง · **ไม่มี Restricted field** (ไม่มี amount/financial · LOCK-CSQ-04) · highest classification = **Confidential**. Customer (subject) = external ref `CUS-xxxx` (ไม่ join).

### Entities (เฉพาะที่ feature อื่นน่าจะอ่าน/อ้าง)
| Entity | PK | Key Fields | หมายเหตุ |
|---|---|---|---|
| `T_consent_purpose` | id (uuid) | tenant_id (RLS), code `PUR-0x` (UNIQUE/tenant), name, channels[] (jsonb ≥1), lifespan_months (1–120, def 24), status, current_ver | header วัตถุประสงค์ |
| `T_consent_policy_version` | id | tenant_id, purpose_id (FK), v, doc_name, doc_type, `doc_ref` (Confidential), published_at | **immutable** (no UPDATE/DELETE · BR-05) · UNIQUE(tenant,purpose,v) |
| `T_consent_request` | id | tenant_id, code `REQ-xxxx`, `subject_ref` (Confidential+PII), channel, status, `answered_at` **[FIX-01]**, `link_token` (Confidential), `ref_old` (FK renew/reconsent), expires_at (created+30วัน) | header คำขอ · **answered/expired = terminal** |
| `T_consent_request_purpose` | id | request_id (FK), purpose_id (FK) | join · UNIQUE(request,purpose) |
| `T_consent_request_send` | id | request_id (FK), channel, sent_at, `vers` (jsonb) **[FIX-03/BR-24]**, kind | **append-only** (การส่ง/ส่งซ้ำ · BR-18) · `vers` = snapshot เวอร์ชันนโยบายต่อ purpose ณ เวลาส่ง `{"PUR-01":2,...}` (immutable ต่อ record) |
| `T_consent` | id | tenant_id, code `CNS-xxxx`, `subject_ref` (Confidential+PII), purpose_id, channel, status, `policy_version` (snapshot ณ เซ็น), granted_at, expires_at, `grant_event_id`, `superseded_by` | **ทะเบียน triple key** · **Partial UNIQUE(tenant,subject_ref,purpose_id,channel) WHERE superseded_by IS NULL** = 1 active triple (BR-01) |
| `T_consent_evidence` | id | consent_id (FK 1:1), answered_at, request_channel, `id_method` (Confidential+PII), policy_version, `ip_device` (Confidential+PII) | **หลักฐาน 5 อย่าง** (BR-15) · immutable หลัง answered (BR-23) · NULL ได้เฉพาะ declined/pending |
| `T_consent_history` | id | consent_id (FK), at, action, label, reason, via | **append-only** (BR-16/17) |
| `T_consent_csq_outbox` | id | feature, event_id, ref, `idempotency_key` (UNIQUE), reversal_of, payload (masked), delivered | envelope CSQ declare-only · **ไม่มีคอลัมน์ผลรายท่อ/amount** (LOCK-CSQ-04/05) |

> Customer (`CUS-xxxx`) = external ref จาก Customer Master — อ้าง id เท่านั้น ไม่ join (upstream อ่านอย่างเดียว).

### Enums / States (ครบทุกค่า — ห้าม compress · R6)
| Field | Values | Transition owner |
|---|---|---|
| `purpose.status` | `active` → `closed` (ปิดแล้วขอใหม่ไม่ได้ · consent เดิมคงอยู่) | feature นี้ |
| `request.status` | `draft` → `pending` (ส่งครั้งแรก) → `answered` **★ terminal (BR-23 · set `answered_at`)** · หรือ `pending` → `expired` (เกิน 30 วัน = lapsed ≠ declined) | feature นี้ |
| `consent.status` (เก็บ DB) | `pending` · `granted` · `declined` · `withdrawn` | feature นี้ |
| consent computed (ENG-02 · ไม่เก็บ DB) | `expired` (granted & daysLeft<0) · `near_expiry` (0≤daysLeft≤30) · `stale`/policyStale (policy_version < current_ver) | ENG-02 |
| **resolve `status`** (ผลของ `/consent/resolve`) | `granted` · `declined` · `withdrawn` · `expired` · `pending` · **`never_asked`** (ไม่เคยมี record → allowed:false · ไม่ใช่ 404/declined) | ENG-01 |
| `channel` (triple key part) | `email` · `sms` · `line` · `phone` · `post` | feature นี้ (config enum · BR-02) |
| `history.action` | `requested` · `granted` · `declined` · `withdrawn` · `renew_requested` · `reconsent_requested` | feature นี้ |
| `send.kind` | `send` · `link_export` · `qr_download` | feature นี้ |
| CSQ `event_id` (7) | `consent.granted` · `consent.declined` · `consent.withdrawn` · `consent.renew_requested` · `consent.reconsent_requested` · `policy.version_published` · `purpose.closed` | feature นี้ (declare-only) |
| Data Classification | `Internal` (default) · `Confidential` (highest) — **ไม่มี Restricted / Public** | Policy Center |

### State transitions (owner = feature นี้ · จาก 05_RULES §5.2 + 03_LOGIC §3.5)
| From | To | Action | Actor | Condition |
|---|---|---|---|---|
| — | pending | สร้าง+ส่งคำขอ | officer/dpo | purpose active + channel supported |
| pending | granted | ยินยอม (recipient view) | เจ้าของข้อมูล | verified + answer=grant · request draft/pending เท่านั้น (BR-23) |
| pending | declined | ปฏิเสธ (recipient view) | เจ้าของข้อมูล | verified + answer=decline · request draft/pending เท่านั้น (BR-23) |
| pending | (request expired) | เกินกำหนด 30 วัน | system | lapsed ≠ declined (BR-08) |
| answered | ✗ (blocked) | ตอบซ้ำ | — | **BR_REQUEST_CLOSED — re-answer ถูกบล็อก · evidence immutable (BR-23)** |
| granted | withdrawn | ถอน (มีผลทันที · ไม่อนุมัติ) | officer/dpo | reason + via required · eff_status=granted เท่านั้น (BR-26) |
| granted | (expired/near_expiry/stale) | คำนวณ (ENG-02) | system | computed · ไม่เก็บ DB |

### Relationships
- `T_consent_purpose` 1—N `T_consent_policy_version` (immutable versions) · 1—N `T_consent`
- `T_consent_purpose` N—N `T_consent_request` ผ่าน `T_consent_request_purpose`
- `T_consent_request` 1—N `T_consent_request_send` (append-only · เก็บ `vers` snapshot) · 1—N `T_consent` (split per-purpose ตอน answer)
- `T_consent` 1:1 `T_consent_evidence` · 1—N `T_consent_history` (append-only)
- `T_consent.ref_old` / `superseded_by` → `T_consent` (renew / supersede — คงของเดิม ไม่ลบ · BR-17)
- Customer (`CUS-xxxx`, external) —N `T_consent` (subject_ref · **no FK join**)
- ทุก mutation → `T_consent_csq_outbox` (declare-only)

## 3. API Surface

> Source: FRD 02_API. ทุก endpoint ต้อง `X-Tenant-Id` (RLS) · ทุก mutation รับ `Idempotency-Key` header · ไม่มี PUT/PATCH (ใช้ POST action ตาม state machine). recipient endpoints (API-12/13) เข้าผ่าน **token** (public link · ไม่ต้อง JWT). **Role enforcement (BR-25/FIX-02):** คอลัมน์ Auth = สิทธิ์ที่ต้อง enforce **ภายในทุก mutation function** (ไม่ใช่แค่ render) — auditor = read-only (403 ทุก mutation) · purpose (API-02/04/05) = dpo เท่านั้น · enforce จริงจากล็อกอิน = OQ-05.

| Method | Endpoint (`/api/v1`) | ทำอะไร | FN |
|---|---|---|---|
| GET | `/consent/purposes` · `/:code` | list วัตถุประสงค์ + สถิติ · รายละเอียด + versions[] | FN-03 |
| POST | `/consent/purposes` | สร้าง purpose + upload เอกสาร v1 (multipart · dpo) | FN-01 |
| POST | `/consent/purposes/:code/versions` | อัปโหลดเวอร์ชันใหม่ (v+1 immutable) + คืน stale_count (dpo) | FN-02/17 |
| POST | `/consent/purposes/:code/close` | ปิดวัตถุประสงค์ (dpo) | FN-04 |
| GET | `/consent/requests` · `/:id` | list / รายละเอียดคำขอ | FN-05/06..09 |
| POST | `/consent/requests` | สร้างคำขอ **single-screen** (subject + purpose_codes[] + channel) | FN-05 |
| POST | `/consent/requests/:id/send` | ส่ง/ส่งซ้ำ (**mock**) — **guard status ∈ {draft,pending}** (BR-26) · คืน `vers` snapshot (BR-24) | FN-06/21 |
| POST | `/consent/requests/:id/link-export` | คัดลอกลิงก์ / ดาวน์โหลด QR (log) | FN-07 |
| GET | `/consent/requests/:id/document` | ดาวน์โหลดเอกสารเวอร์ชันปัจจุบัน | FN-07 |
| GET | `/consent/recipient/:token` | โหลด recipient view (public via token · lapsed → 200 `{expired:true}` · answered/closed → 200 `{closed:true}` หน้าสถานะปิด · ไม่ 404) | FN-08 |
| POST | `/consent/recipient/:token/answer` | ส่งคำตอบยินยอม/ปฏิเสธ **รายข้อ** (verified=true) → registry + evidence 5 · **guard answered=terminal (BR-23)** | FN-09/10/11 |
| GET | `/consent/registry` · `/:id` | ทะเบียน + กรองทุกมิติ + stats · รายละเอียด + evidence 5 + history | FN-11/12/18 |
| GET | `/consent/subjects/:subjectRef` | Customer 360 (consent ทั้งหมดของ subject) | FN-11 |
| POST | `/consent/registry/:id/withdraw` | ถอน (มีผลทันที · reason + via required) · **guard eff_status=granted (BR-26)** | FN-13 |
| GET | `/consent/near-expiry` | รายการใกล้หมดอายุ ≤30 วัน | FN-18 |
| POST | `/consent/registry/:id/renew` | ต่ออายุ = คำขอใหม่อ้างเดิม (ไม่แก้ expires_at เดิม) | FN-14 |
| POST | **`/consent/resolve`** ⭐ | ตรวจสิทธิ์ triple → allowed + status + reason · **LOCKED CONTRACT · HTTP 200 เสมอ** | FN-20 |

### `/consent/resolve` — Locked Contract (BR-19/20 · consumers ต้อง honor)
- **Request:** `{ subject, purpose, channel }`
- **Response 200 (ล็อก — เพิ่มฟิลด์ได้ ห้ามเปลี่ยนชื่อ/ความหมายเดิม):** `{ subject, purpose, channel, allowed:boolean, status, policy_version, granted_at, expires_at, found:boolean, reason }`
- **never_asked (FN-20 · MUST):** `{ allowed:false, status:"never_asked", found:false, policy_version:null, granted_at:null, expires_at:null, reason:"ยังไม่เคยขอ..." }`
- **closed purpose:** `allowed:false` + reason ต่อท้าย "· วัตถุประสงค์นี้ถูกปิดใช้งานแล้ว" · **stale:** `allowed:false` (ยินยอมกับ version เก่า — ต้องขอใหม่)
- ไม่มี error business — ผลลบสื่อผ่าน `allowed:false + status + reason` (ไม่ 404/500)

### Error contract (codes only · consumers/gateway ต้อง honor · จาก 05_RULES §5.6)
| Code | HTTP | Cause |
|---|---|---|
| ERR_VALIDATION_FAILED | 400 | field validation |
| ERR_NOT_AUTHENTICATED / ERR_INSUFFICIENT_ROLE | 401 / 403 | no token / role mismatch (enforce จริง = OQ-05) |
| ERR_DUPLICATE_IDEMPOTENCY_KEY / ERR_STALE_DATA | 409 | same key diff body / optimistic-lock version mismatch |
| BR_DOCUMENT_REQUIRED | 422 | ไม่แนบเอกสารตอนสร้าง/ออกเวอร์ชัน (BR-05) |
| BR_CHANNEL_NOT_SUPPORTED / BR_PURPOSE_CLOSED | 422 | ช่องทางนอก purpose (BR-03) / คำขอกับ purpose closed (BR-14) |
| BR_IDENTITY_NOT_VERIFIED / BR_ANSWERS_INCOMPLETE | 422 | recipient ไม่ verified / ตอบไม่ครบทุก purpose |
| BR_WITHDRAW_REASON_REQUIRED / BR_WITHDRAW_CHANNEL_REQUIRED | 422 | ถอนไม่มีเหตุผล / ไม่มีช่องทาง (BR-10) |
| **BR_REQUEST_CLOSED** | 422 | ตอบ/ส่งคำขอที่ปิดแล้ว (answered/expired · **FIX-01/05 · BR-23/26**) |
| **BR_NOT_GRANTED** | 422 | ถอน consent ที่ไม่ได้อยู่สถานะ granted (**FIX-05 · BR-26**) |

> **`/consent/resolve` ไม่มี error business** — ตอบ 200 เสมอ (BR-19). PII fields (subject_ref/id_method/ip_device) mask ก่อนส่งถ้า role ไม่ผ่าน · campaign ปลายทางเห็นแค่ allowed/status/reason (D-CLASS).

### Events emitted (CSQ · declare-only → 7C `POST /csq/events`)
| Event | Trigger point (FN) | ref · payload key |
|---|---|---|
| `consent.granted` / `consent.declined` | FN-09 applyAnswers (recipient ตอบรายข้อ) | `CNS-xxxx` · subject, purpose, channel, policy_version |
| `consent.withdrawn` | FN-13 withdraw | `CNS-xxxx` · **reversal_of = grant_event_id** (BR-CSQ-04) |
| `consent.renew_requested` | FN-14 renew | `REQ-xxxx` · subject, refOld |
| `consent.reconsent_requested` | FN-15 reConsent (policy stale) | `REQ-xxxx` · subject, purpose, refOld |
| `policy.version_published` | FN-02 publishPolicyVersion | `PUR-xx` · purpose, version |
| `purpose.closed` | FN-04 closePurpose | `PUR-xx` · purpose |

> `idempotency_key` ทุก event = `F-MKT-CONSENT:<ref>:<event_id>` (UNIQUE · BR-CSQ-02). `subject` เป็น Confidential+PII → **mask ก่อนส่ง** (BR-CSQ-03). **ไม่ประกาศท่อ OC/DC/SC** (มาอัตโนมัติจาก Operation Process / DOA engine — ประกาศซ้ำ = reject 422). **FN-21 `snapshotVers` (การส่ง/version snapshot · BR-24) ไม่เพิ่ม event ใหม่เข้า 7C.** Engines: `consent-resolution-engine` (ENG-01) + `consent-status-evaluator` (ENG-02) — CUBIC DRAFT, register ตอน hand-off.

## 4. Shared Rules (cross-boundary เท่านั้น)

> Source: FRD 05_RULES. เอาเฉพาะ rule ที่ feature/module อื่นต้อง conform หรือถูกกระทบ. Rule ภายใน (form validation, masking UI, empty state) ตัดออก.

| Rule ID | Rule | กระทบใคร |
|---|---|---|
| BR-04 | **default-deny** — ไม่มี record ในทะเบียน = ส่งไม่ได้ (resolve → never_asked) | ทุก caller ที่เช็คสิทธิ์ก่อนส่ง |
| BR-19 | `/consent/resolve` ตอบ **HTTP 200 เสมอ** · never_asked → `allowed:false` (ไม่ 404) | แคมเปญ/ส่งข้อความ · F136 · F143 · gateway |
| BR-20 | สัญญาผล resolve **ล็อก** — เพิ่มฟิลด์ได้ ห้ามเปลี่ยนชื่อ/ความหมาย `allowed/status/found/reason/policy_version/granted_at/expires_at` | ทุก consumer ของ resolve |
| BR-01 | triple key subject×purpose×channel ไม่ซ้ำ (1 active record) — ผล resolve อิง triple | consumers ที่ส่ง { subject, purpose, channel } |
| BR-08 | ไม่ตอบ ≠ ปฏิเสธ (คำขอเกิน 30 วัน = lapsed) — resolve reason สื่อว่ายังไม่ได้รับคำตอบ | caller (ตีความ status/reason) |
| BR-06 | consent ผูก policy_version ที่เห็นตอนเซ็น — version ใหม่ไม่ครอบคลุมอัตโนมัติ (stale → allowed:false) | caller · reconsent flow |
| BR-21 | ผู้เรียกแคชผล resolve **≤5 นาที + ล้างทันทีเมื่อถอน** (caller-side contract · no UI · OQ-02) | ทีม integration / แคมเปญ (F136) |
| BR-22 | `/consent/*` ต้องขึ้นทะเบียน **Backend Enforcement Gate (F143)** + review 4 ขั้น | ทีม Security (F143) · **hard dep go-live · OQ-04** |
| BR-23 | **[FIX-01]** คำขอ **answered = terminal** — ตอบครั้งเดียว · re-answer บล็อก · **evidence chain immutable** · เปลี่ยนใจ = คำขอใหม่/withdraw | F157 DSAR (หลักฐานแช่แข็ง เชื่อถือได้) · OQ-CNS-01 (ใครเปิดคำขอใหม่) |
| BR-24 | **[FIX-03]** การส่งเก็บ **snapshot เวอร์ชันนโยบายต่อ purpose (`vers`)** ณ เวลาส่ง — หลักฐาน "ส่งเอกสารเวอร์ชันไหน" | F157 DSAR (evidence/timeline) · OQ-CNS-02 (publish v ใหม่ระหว่าง pending) |
| BR-CSQ-01 | ทุก event ยิง 7C ผ่าน `POST /csq/events` — declare-only · ห้ามเขียนผลรายท่อในตาราง feature | 7C Engine (F-CSQ-01) |
| BR-CSQ-02 | envelope มี `idempotency_key` unique ต่อ (feature, ref, action) · BR-26 = UI backstop เสริม (defense-in-depth) | 7C Engine |
| BR-CSQ-03 | payload ห้ามพก Confidential/PII ดิบ — mask ที่ producer (subject_ref) | 7C Engine · D7 PII |
| BR-CSQ-04 | reversal (`consent.withdrawn`) แนบ `reversal_of` ชี้ event เดิม — ห้ามลบ/แก้ผลเดิม | 7C Engine |
| BR-CSQ-05 | ไม่ประกาศ/ไม่คำนวณท่อ OC + DC ระดับเอกสาร (มาจาก Operation Process / DOA engine) | 7C Engine · register gate |

**Permission (business intent · BR-25/FIX-02 · role check ใน mutation function · enforce จริง = OQ-05):** officer = ดูทะเบียน/สร้าง-ส่งคำขอ/ถอน/resolve (❌ purpose/close) · dpo = ทุกอย่าง (+ สร้าง/แก้ purpose, upload version, close) · auditor = read + resolve(read) เท่านั้น (403 ทุก mutation). **role check อยู่ต้นทุก mutation function** (ไม่ใช่แค่ render ปุ่ม — auditor เรียก mutation ตรงถูกปฏิเสธ · bypass B4). **BR-26 (FIX-04/05):** double-submit guard (`_busy`) + sub-status guard (withdraw=granted only · resend=draft/pending only) = UI idempotency backstop. **ไม่มี approval chain** (LOCK-04) — การควบคุมอยู่ที่ default-deny + evidence 5 + audit append-only.

## 5. Integration

- **Depends on:** **none** — Standalone (plan `dep=""` · ไม่มี upstream trigger เอกสารต้นทาง). อ้าง Customer Master เป็น **external ref** (`CUS-xxxx`) เท่านั้น (อ่าน id · ไม่ join).
- **Depended by (downstream · FIX-06 contract anchors · Feature List F058):**
  - **F136 Broadcast (control · ctl)** — เรียก `POST /consent/resolve` ตรวจ opt-in **ก่อนส่ง Email/SMS ทุกครั้ง** (block อัตโนมัติเมื่อ allowed:false) · ถอน → resolve ตอบ false ทันที + caller ล้างแคช ≤5 นาที (BR-21)
  - **F031 Customer 360 (data)** — สถานะ consent ผูกลูกค้า (subject) จาก resolve + ทะเบียน (เปิดหน้าลูกค้า)
  - **F157 DSAR (data)** — ทะเบียน consent + **evidence 5 + history append-only** = ฐานข้อมูลประกอบคำขอ DSAR (BR-16/17/23 กันแก้/ลบ · anchor ประกาศแล้ว · **consent receipt PDF ยังเป็น E3 deferred**)
  - **Backend Enforcement Gate (F143)** — ขึ้นทะเบียน `/consent/*` + review 4 ขั้น · เรียก ENG-01 ผ่าน resolve · **hard dependency ก่อน go-live (BR-22)**
  - **7C Consequence Engine (F-CSQ-01)** — รับ event envelope (declare-only · 7 events) ทุก state change
  > FIX-06: anchor 3 contract (F136/F031/F157) = **display-only** ในหน้าจอ — **ไม่ mock หน้าจอ feature อื่น** ในรอบนี้
- **Declarations (รอบนี้ 2026-09-14 · csq only):**
  - **CSQ** [yes · declare-only] — 7 events เข้าท่อ **SecC** `[DEFAULT — รอยืนยัน · OQ-CSQ-02]` (PII/permission change) · ไม่ประกาศ OC/DC/SC/EC/AC/FC · profile_id `CSQ-F058` `[DEFAULT · OQ-CSQ-01]` · sink = `T_consent_csq_outbox` → deploy pipeline ส่งเข้า 7C · v1.1 refresh: envelope/7 events **ไม่เปลี่ยน** (FIX-05 = UI backstop เท่านั้น)
  - **DOA** [no] · **DOCCFG** [no] · **NTF** [no] — ไม่มีสายอนุมัติ (LOCK-04) · ไม่มีเลขรันเอกสารธุรกรรม · ไม่มี event แจ้งเตือนที่ประกาศผ่าน ENG-NOTIFY
- **Engine hooks:** `consent-resolution-engine` (ENG-01 · resolve) + `consent-status-evaluator` (ENG-02 · eff-status/stale/near-expiry) — NEW · CUBIC DRAFT · register ตอน hand-off · external sink `POST /csq/events` (F-CSQ-01).
- **Open dependencies (BLOCKING — ห้าม dev เดา):**
  - **OQ-03** (YES · ก่อน implement) — วิธียืนยันตัวตนจริงใน recipient view (ปัจจุบัน checkbox **mock** → ลิงก์/OTP/สแกน) · กระทบ `evidence.id_method`
  - **OQ-04** (YES · hard dep go-live) — `/consent/*` register Backend Enforcement Gate (F143) + review 4 ขั้น · confirm timeline/ขั้นตอนกับทีม Security
- **Open decisions (BA-gate · Strike เคาะ · build ปัจจุบัน = conservative):**
  - **OQ-CNS-01** — เปลี่ยนใจหลังตอบแล้ว: answered=terminal (BR-23) → เส้นทางถูก = คำขอใหม่/withdraw · **ใครมีสิทธิ์เปิดคำขอใหม่** → 03_LOGIC state machine
  - **OQ-CNS-02** — publish นโยบายเวอร์ชันใหม่ระหว่างคำขอ pending ค้าง: build = **ไม่ auto-expire** (แสดงเวอร์ชัน ณ ส่ง `vers` + ป้ายเตือน · FIX-03) vs auto-expire
  - **OQ-CNS-03** — รอบต่ออายุ: near-expiry 30 วันมีแล้ว ใคร/อะไร trigger คำขอต่ออายุ (manual จาก registry vs batch · NTF ฝั่ง F136)
  - (non-blocking) OQ-02 caller cache · OQ-05 permission enforce จริงต่อ role + consent receipt PDF (E3) deferred · OQ-07 file validation จริง · OQ-08 timezone `expires_at` · OQ-CSQ-01/02 profile_id + ชื่อท่อ SecC

---
*trace: §1 ← FRD 00_OVERVIEW §0.3 + BRD §12.1 · §2 ← FRD 04_DB (answered_at/vers = FIX-01/03) · §3 ← FRD 02_API (+03_LOGIC §3.1/§3.4/§3.5 guards+events) · §4 ← FRD 05_RULES §5.1 (BR-23..26) + §5.3 · §5 ← FRD 00_OVERVIEW §0.5 + BRD §12.1 + CSQ_BRIEF v1.1 + PROPOSALS_outbound*
