# 05_RULES — F-MKT-CONSENT ความยินยอม PDPA

> **Audience:** Backend developer + QA
> **Purpose:** Business Rules + State Machines + Permission + Validation + Edge Cases + Errors + Security
> **Principle:** Declarative — อ่านแล้วเข้าใจโดยไม่ต้องดูโค้ด

---

## §5.1 Business Rules (BR) — จาก BRD §9 (source of truth)

| Rule | กฎ | Tag | Enforced by |
|---|---|---|---|
| BR-01 | triple key subject×purpose×channel ไม่ซ้ำ (active รายการเดียว) | FIXED | 04_DB partial-unique · FN-10 supersede |
| BR-02 | ช่องทางรองรับ 5: email/SMS/LINE/phone/post | CONFIGURABLE 🤖 | config enum (OQ Admin) |
| BR-03 | purpose กำหนดช่องทางเอง — ขอนอกรายการไม่ได้ | FIXED | FN-05 (BR_CHANNEL_NOT_SUPPORTED) |
| BR-04 | default = ไม่อนุญาต (ไม่มี record = ส่งไม่ได้) | FIXED | ENG-01 never_asked |
| BR-05 | เอกสารนโยบายเป็นเวอร์ชัน · **อัปโหลดใหม่ = ออกเวอร์ชันใหม่** · เวอร์ชันเดิมแก้ไม่ได้ | FIXED (**DECLARED-01**) | 04_DB immutable version · FN-02 |
| BR-06 | consent ผูกเวอร์ชันที่เห็นตอนเซ็น — เวอร์ชันใหม่ไม่ครอบคลุมอัตโนมัติ | FIXED | snapshot policy_version · ENG-02 policyStale |
| BR-07 | สถานะ 5 ค่า + คำนวณ expired | FIXED | §5.2 · ENG-02 |
| BR-08 | ไม่ตอบ ≠ ปฏิเสธ (เกินกำหนด = คำขอหมดอายุ) | FIXED | request status expired · resolve reason |
| BR-09 | ถอนได้ทุกเมื่อ ไม่ต้องอนุมัติ มีผลทันที | FIXED (LOCK-04) | FN-13 |
| BR-10 | ถอนต้องระบุเหตุผล + ช่องทางที่ลูกค้าแจ้ง | FIXED | FN-13 (BR_WITHDRAW_REASON/CHANNEL_REQUIRED) |
| BR-11 | อายุความยินยอมตาม purpose (default 24 เดือน) | CONFIGURABLE (รายวัตถุประสงค์ 1–120) | 04_DB CHECK · form |
| BR-12 | ใกล้หมดอายุ ≤30 วัน เตือน ไม่บล็อก | CONFIGURABLE 🤖 | ENG-02 nearExpiry |
| BR-13 | ต่ออายุ = คำขอใหม่อ้างเดิม ไม่แก้วันหมดอายุเดิม | FIXED | FN-14 |
| BR-14 | ปิด purpose = ห้ามคำขอใหม่ · consent เดิมอยู่ | FIXED | FN-04/FN-05 (BR_PURPOSE_CLOSED) |
| BR-15 | หลักฐานครบ 5 อย่างทุก consent ที่ได้รับ | FIXED | 04_DB T_consent_evidence · FN-11 |
| BR-16 | ประวัติ append-only เขียนใน tx เดียวกับ state change | FIXED | 04_DB trigger append-only |
| BR-17 | ไม่มีการลบถาวร (consent/คำขอ/วัตถุประสงค์) | FIXED | soft close/supersede, no DELETE |
| BR-18 | คำขอส่งซ้ำได้หลายครั้ง = รายการส่ง ไม่สร้างคำขอใหม่ | FIXED | FN-06 |
| BR-19 | `/consent/resolve` ตอบ 200 เสมอ · never_asked→allowed:false (ไม่ 404) | FIXED | ENG-01 · API-20 |
| BR-20 | สัญญาผล resolve ล็อก — เพิ่มฟิลด์ได้ ห้ามเปลี่ยนชื่อ/ความหมายเดิม | FIXED | ENG-01 output schema |
| BR-21 | ผู้เรียกแคช ≤5 นาที + ล้างทันทีเมื่อถอน | CONFIGURABLE (caller-side, no UI) | 02_API §2.X · OQ-02 |
| BR-22 | `/consent/*` ต้องขึ้นทะเบียน Backend Enforcement Gate + ตรวจ 4 ขั้น | FIXED (external dep) | 02_API §2.X · OQ-04 |
| BR-CSQ-01 | ทุก event ยิง 7C ผ่าน `POST /csq/events` — ห้ามเขียนผลรายท่อในตาราง feature | FIXED | FN-19 · T_consent_csq_outbox |
| BR-CSQ-02 | envelope มี idempotency_key unique ต่อ (feature, ref, action) | FIXED | `F-MKT-CONSENT:<ref>:<event_id>` UNIQUE |
| BR-CSQ-03 | payload ห้ามพก restricted ดิบ — mask ที่ผู้ส่ง | FIXED | FN-19 mask |
| BR-CSQ-04 | reversal ส่ง event มี reversal_of ชี้ event เดิม — ห้ามลบ/แก้ผลเดิม | FIXED | FN-13 withdraw reversal_of=grant_event_id |
| BR-CSQ-05 | ไม่ประกาศ/ไม่คำนวณท่อ OC + DC ระดับเอกสาร (มาจาก Operation Process / DOA engine) | FIXED (LOCK-CSQ) | FN-19 (declare-only) |

---

## §5.2 State Machines

### Consent status (เก็บ 4 + คำนวณ 3 + resolve-only 1)
```
(no record) ──resolve──> never_asked            [allowed:false — ไม่เก็บ DB]
[pending] ──เจ้าของยินยอม──> [granted] ──expires_at<now──> (expired*)
[pending] ──เจ้าของปฏิเสธ──> [declined]           (terminal · ≠ ไม่ตอบ)
[pending] ──คำขอเกิน 30 วัน──> (request expired: lapsed ≠ declined)
[granted] ──ถอน──> [withdrawn]                   (terminal จนขอใหม่ · ไม่อนุมัติ)
[granted] ──policy_version<current_ver──> (stale*: ต้องขอใหม่)
[granted] ──0≤daysLeft≤30──> (near_expiry*: เตือน ไม่บล็อก)
```
`*` = computed (ENG-02) ไม่เก็บ DB

| From | To | Action | Roles | Conditions |
|---|---|---|---|---|
| — | pending | สร้าง+ส่งคำขอ | officer/dpo | purpose active + channel supported |
| pending | granted | ยินยอม (recipient view) | เจ้าของข้อมูล | verified + answer=grant |
| pending | declined | ปฏิเสธ (recipient view) | เจ้าของข้อมูล | verified + answer=decline |
| granted | withdrawn | ถอน | officer/dpo | reason + via required · ทันที |
| granted | (expired) | เวลา | system | expires_at < now (computed) |

### Request status
`draft → pending (ส่งครั้งแรก) → answered` · หรือ `pending → expired (เกิน 30 วัน)`

### Purpose status
`active → closed` (ปิดแล้วขอใหม่ไม่ได้ · consent เดิมคงอยู่)

---

## §5.3 Permission Matrix (จาก HTML `PERM()` — business intent; enforce จริง = OQ-05)

| Role | ดูทะเบียน/หลักฐาน | สร้าง/แก้ purpose + upload | สร้าง/ส่งคำขอ | ถอน | ปิด purpose | resolve |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| officer (เจ้าหน้าที่การตลาด) | ✅ | ❌ (read) | ✅ | ✅ | ❌ | ✅ |
| dpo (ผู้ดูแลข้อมูล) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| auditor (ผู้ตรวจสอบ) | ✅ (read) | ❌ | ❌ | ❌ | ❌ | ✅ (read) |

> HTML: `PERM()` → `reqCreate/send/sign/withdraw = persona!=='auditor'` · `purpose = persona==='dpo'` · ⚠️ **persona switcher เดโม** — FRD ต้อง enforce จริงต่อ role (OQ-05)

---

## §5.4 Field Validation Rules

| Field/Action | เงื่อนไข | ประเภท | Error / ข้อความ (verbatim) |
|---|---|---|---|
| สร้างวัตถุประสงค์ | name + ≥1 channel + life 1–120 + **แนบเอกสาร** | Prevent | "กรอกชื่อวัตถุประสงค์" / "เลือกช่องทางอย่างน้อย 1" / "อายุต้องอยู่ระหว่าง 1–120 เดือน" / "ต้องแนบเอกสาร PDPA" |
| อัปโหลดเวอร์ชันใหม่ | ต้องแนบเอกสาร | Prevent | "ต้องแนบเอกสาร PDPA" |
| ส่ง recipient answer | verified=true ก่อน | Prevent | "กรุณายืนยันตัวตนก่อนส่งคำตอบ" |
| recipient answer | ตอบครบทุก purpose | Prevent | "กรุณาเลือกยินยอม/ไม่ยินยอมให้ครบ..." |
| ถอน | เหตุผล + ช่องทาง | Prevent | "กรอกเหตุผล" / "เลือกช่องทางที่ลูกค้าแจ้งมา" |
| สร้างคำขอ | subject + channel + purpose ที่รองรับ channel + active | Prevent | "เลือกเจ้าของข้อมูลก่อน" / "เลือกช่องทางก่อน" / "เลือกวัตถุประสงค์ที่รองรับช่องทาง..." |
| resolve | เลือกครบ 3 ช่อง | Prevent | "เลือกให้ครบทั้ง 3 ช่องก่อนตรวจสอบ" |
| resolve never_asked | ไม่มี record | Trigger | `status:"never_asked"` + reason |

**Cross-field:** `expires_at = granted_at + lifespan_months` (ENG-02) · `policy_version` = snapshot ณ เซ็น (ไม่ตาม current_ver)

---

## §5.5 Edge Cases (Phase 2.5 Probing — Lane Mode no-ask · conservative default + `[AI-DEFAULT]`)

**Probes activated (FULL ≥3):** PR-1 (Concurrency), PR-2 (Stale), PR-7 (Idempotency), PR-8 (Compensation) — PR-9 (financial race) N/A (ไม่มี inventory/money · LOCK-CSQ-04)

### EC-01: never_asked (BRD §10 ☑ · FN-20)
- **Scenario:** resolve triple ที่ไม่เคยมี record · **Resolution:** `allowed:false, status:'never_asked', found:false` — ไม่ 404/declined (BR-04/19) · **Test:** AT-20

### EC-02: ถอน ↔ resolve race + caller cache (PR-1 · BR-21)
- **Scenario:** ลูกค้าถอน ขณะ campaign เพิ่ง cache ผล granted · **Resolution:** withdraw มีผลทันทีในทะเบียน · caller ต้องล้าง cache ทันที (contract ≤5 นาที) · `[AI-DEFAULT]`: caller-side, ไม่มี server push · **Test:** AT-15b / XT-03 · **OQ-02**

### EC-03: version stale (PR-2 · BRD §10 ☑ · BR-06)
- **Scenario:** consent granted กับ v1 แล้ว purpose ออก v2 · **Resolution:** ENG-02 policyStale → resolve `allowed:false` reason "ยินยอมไว้กับนโยบายเวอร์ชัน 1 แต่เวอร์ชันปัจจุบันคือ 2 — ต้องขอความยินยอมใหม่" · reConsent สร้างคำขอใหม่ · **Test:** AT-19c

### EC-04: double-submit / retry (PR-7 · BR-CSQ-02 `[AI-DEFAULT]`)
- **Scenario:** double-click ส่งคำขอ / recipient answer · **Resolution:** Idempotency-Key header (24 ชม.) + CSQ idempotency_key unique · **Test:** AT-ID

### EC-05: ไม่ตอบ ≠ ปฏิเสธ (BRD §10 ☑ · BR-08)
- **Scenario:** คำขอ pending เกิน 30 วัน · **Resolution:** request → expired (lapsed) · consent ยัง never/pending · resolve reason "ส่งคำขอไปแล้วแต่ยังไม่ได้รับคำตอบ — ...การไม่ตอบไม่ใช่การยินยอม" · **Test:** AT-20b

### EC-06: ยินยอมบางวัตถุประสงค์ (BRD §10 ☑ · S-11 · FN-11)
- **Scenario:** คำขอ 3 purpose ยินยอม 2 ปฏิเสธ 1 · **Resolution:** applyAnswers บันทึกแยกรายข้อ (granted+declined records) · **Test:** AT-11

### EC-07: ปิด purpose → consent เดิมคงอยู่ (BRD §10 ☑ · BR-14/17)
- **Scenario:** ปิด purpose ที่มี consent granted · **Resolution:** status=closed · consent เดิมอยู่เป็นหลักฐาน · resolve ต่อท้าย reason "· วัตถุประสงค์นี้ถูกปิดใช้งานแล้ว" allowed:false · สร้างคำขอใหม่ไม่ได้ · **Test:** AT-04

### EC-08: withdraw = compensation (PR-8 · BR-CSQ-04)
- **Scenario:** ถอน consent ที่ granted · **Resolution:** ไม่ลบ record · emit `consent.withdrawn` reversal_of=grant_event_id (7C กลับผลเดิม ไม่ลบ) · **Test:** AT-15c

### EC-09 `[AI-DEFAULT]`: อัปโหลดไฟล์ใหญ่/ชนิดไม่รองรับ (BRD §10.2 [FU])
- **Scenario:** อัปโหลดเอกสารเกินขนาด/ชนิดนอก .pdf/.doc/.docx/.txt · **Resolution (default):** accept 4 ชนิด · validate size จริง = TBD (ปัจจุบัน mock) · **OQ-07**

### EC-10 `[AI-DEFAULT]`: timezone ของ expires_at (BRD §10.2 [CL])
- **Scenario:** lifespan เดือน ข้ามเขตเวลา/เดือนไม่เท่ากัน · **Resolution (default):** เก็บ/คำนวณ UTC · display tenant TZ · **OQ-08**

### EC-11 `[AI-DEFAULT]`: optimistic lock (PR-2)
- **Scenario:** 2 dpo ออกเวอร์ชัน/แก้ purpose พร้อมกัน · **Resolution (default):** `version` column → 409 ERR_STALE_DATA · **Test:** AT-VER-lock

---

## §5.6 Error Catalog

| Code | HTTP | Message (i18n key) | Cause |
|---|---|---|---|
| ERR_VALIDATION_FAILED | 400 | error.validation.failed | field validation |
| ERR_NOT_AUTHENTICATED | 401 | error.auth.unauth | no/invalid token |
| ERR_INSUFFICIENT_ROLE | 403 | error.auth.role | role mismatch (OQ-05 enforce) |
| ERR_DUPLICATE_IDEMPOTENCY_KEY | 409 | error.idempotency.dup | same key, diff body |
| ERR_STALE_DATA | 409 | error.concurrency.stale | version mismatch (EC-11) |
| BR_DOCUMENT_REQUIRED | 422 | br.consent.doc.required | ไม่แนบเอกสาร (BR-05) |
| BR_CHANNEL_NOT_SUPPORTED | 422 | br.consent.channel.unsupported | ช่องทางนอก purpose (BR-03) |
| BR_PURPOSE_CLOSED | 422 | br.consent.purpose.closed | สร้างคำขอกับ purpose closed (BR-14) |
| BR_IDENTITY_NOT_VERIFIED | 422 | br.consent.identity.unverified | recipient ไม่ verified (BR-15) |
| BR_ANSWERS_INCOMPLETE | 422 | br.consent.answers.incomplete | ตอบไม่ครบทุก purpose |
| BR_WITHDRAW_REASON_REQUIRED | 422 | br.consent.withdraw.reason | ถอนไม่มีเหตุผล (BR-10) |
| BR_WITHDRAW_CHANNEL_REQUIRED | 422 | br.consent.withdraw.channel | ถอนไม่มีช่องทาง (BR-10) |
| CSQ_ERR_DUPLICATE_ENVELOPE | 422 | (7C) | idempotency_key ซ้ำ (BR-CSQ-02) — กันซ้ำ |

> **หมายเหตุ:** resolve (API-20) **ไม่มี error business** — ตอบ 200 เสมอ (BR-19) · ผลลบสื่อผ่าน `allowed:false + status + reason`

---

## §5.7 Security Bible Application

> Domains triggered: **D2, D7, D9, D15, D17, D-CLASS** (ไม่มี D5 Financial — LOCK-CSQ-04 ไม่มี amount)

### D2: Authentication & Session — JWT ทุก endpoint (ยกเว้น recipient token link — API-12/13 ใช้ token + rate-limit)
### D7: PII Protection — subject_ref / id_method / ip_device encrypt at rest · payload CSQ mask ก่อนส่ง (BR-CSQ-03) · logs ใช้ id reference
### D9: Audit Logging — ทุก mutation → T_audit_log + T_consent_history append-only (BR-16/17) · immutable
### D15: Admin Actions — ถอน/ปิด purpose/ออกเวอร์ชัน logged พร้อม actor + reason (ถอน)
### D17: Multi-Tenant — PostgreSQL RLS + X-Tenant-Id middleware

### D-CLASS: Data Classification
| Layer | Confidential fields (subject_ref, id_method, ip_device, doc_ref) |
|---|---|
| API response | mask ถ้า role ไม่ผ่าน (auditor เห็น · external campaign เห็นแค่ allowed/status/reason) |
| UI display | mask `***` |
| Audit | log view + mutation |
> **ไม่มี Restricted field** → ไม่ wire Restricted Resources · **Wire:** Policy Center → Data Classification + PDPA consent scope

---

## §5.8 Compliance & Audit
| Requirement | Implementation |
|---|---|
| PDPA (หลัก) | consent registry + evidence 5 + version-binding + withdraw + audit-ready |
| หลักฐานย้อนกลับ | T_consent_evidence + T_consent_history append-only (BR-15/16) |
| ไม่ลบถาวร | no hard delete (BR-17) |
| resolve gate ก่อนส่ง | BR-04/19 + Backend Enforcement Gate register (BR-22) |
| ISO 27001 | access control (§5.3) + audit log (D9) |
