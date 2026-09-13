# CSQ_BRIEF — F-MKT-CONSENT · ความยินยอม PDPA

> **ใบประกาศ 7C Consequence (declare-only)** — ออกโดย skill `csq-declaration` v1.0 (companion ของ F-CSQ-01 Consequence Engine)
> **สถานะ:** DECLARE-ONLY — feature เป็น **ผู้ประกาศ event** เท่านั้น · ไม่ตีมูลค่า · ไม่ประทับผลรายท่อ · ไม่วาดการ์ดผล 7 ท่อ
> **Source of truth:** `FRD_Pack/03_LOGIC.md §3.1 FN-19 · §3.4` · `FRD_Pack/05_RULES.md §5.1 (BR-CSQ-01..05)` · `FRD_Pack/04_DB.md §4.2 T_consent_csq_outbox` · `consent-pdpa.html emitConsequence()` (L2315–2327)
> ⚠️ **csq-contract.md master ไม่มีในเครื่อง** (skill flat มีแค่ SKILL.md) — ค่า enum ของ "ชื่อท่อ" ที่ตรวจไม่ได้กับ master ถูกติด `[DEFAULT — รอยืนยัน]` + ยกเป็น OQ

---

## §1 · Identity

| Field | Value |
|---|---|
| profile_id | `CSQ-F058` `[DEFAULT — รอยืนยัน]` — เลขคาน `CSQ-NN` จริงจัดสรรโดย 7C Profile Registry ตอน register (OQ-CSQ-01) |
| feature_code | `F-MKT-CONSENT` (plan id F058) |
| feature_name | ความยินยอม PDPA (Consent Management) |
| module | Marketing / PDPA · Policy Center scope |
| กลุ่ม (backfill class) | **B** (SecC on sensitive/permission change) `[DEFAULT — รอยืนยัน]` |
| version | v1.0 (2026-09-13) |
| producer contract | Envelope ตาม F-CSQ-01 §2.3 · `POST /csq/events` |

---

## §2 · Declared Events (7 events — ยืนยันจาก FRD §3.4 + HTML `emitConsequence`)

> **`event_id`** ยึด vocabulary ที่ enumerate ไว้แล้วใน FRD/HTML — **ไม่คิดคำใหม่**
> **ท่อที่ยิง** = ท่อที่ **feature ประกาศ**เท่านั้น · การประเมินผล/ตีมูลค่ารายท่อเป็นหน้าที่ ENG-CSQ-02 (ไม่ใช่ feature)
> ท่อที่ประกาศทั้งใบ = **SecC** `[DEFAULT — รอยืนยัน]` (เหตุผล §3) · **ไม่มี** OC/DC/SC/EC/AC/FC (ล็อกดู §3)

| # | event_id | trigger point (FRD ref) | ท่อที่ยิง | เงื่อนไข (เมื่อไหร่ยิง) | ref (idempotency subject) | payload fields |
|:--:|---|---|---|---|---|---|
| 1 | `consent.granted` | FN-09 `applyAnswers` (03_LOGIC §3.1) · API-13 · BR-06/15 | SecC `[DEFAULT]` | recipient ยืนยันตัวตน + ตอบ "ยินยอม" ต่อ purpose → INSERT T_consent(granted) | `CNS-xxxx` (consent id) | subject, purpose, channel, policy_version |
| 2 | `consent.declined` | FN-09 `applyAnswers` (03_LOGIC §3.1) · API-13 · EC-06/S-11 | SecC `[DEFAULT]` | recipient ตอบ "ไม่ยินยอม" ต่อ purpose → INSERT T_consent(declined) | `CNS-xxxx` (consent id) | subject, purpose, channel |
| 3 | `consent.withdrawn` | FN-13 `withdrawConsent` (03_LOGIC §3.1) · API-17 · BR-09/10 · EC-08 | SecC `[DEFAULT]` | เจ้าหน้าที่/dpo ถอน (มีผลทันที ไม่อนุมัติ) → UPDATE status=withdrawn | `CNS-xxxx` (consent id) | subject, purpose, channel, **reversal_of = grant_event_id** (BR-CSQ-04) |
| 4 | `consent.renew_requested` | FN-14 `renewConsent` → FN-05 (03_LOGIC §3.1) · API-19 · BR-13 | SecC `[DEFAULT]` | สร้างคำขอต่ออายุอ้างรายการเดิม (ไม่แก้ expires_at เดิม) | `REQ-xxxx` (new request id) | subject, refOld |
| 5 | `consent.reconsent_requested` | FN-15 `reConsent` → FN-05 (03_LOGIC §3.1) · API-04 flow / registry action · EC-03/BR-06 | SecC `[DEFAULT]` | ขอความยินยอมใหม่กับ consent ที่ policy stale (v เดิม < current_ver) | `REQ-xxxx` (new request id) | subject, purpose, refOld |
| 6 | `policy.version_published` | FN-02 `publishPolicyVersion` → FN-17 (03_LOGIC §3.1) · API-04 · BR-05 | SecC `[DEFAULT]` | อัปโหลดเอกสารนโยบายใหม่ → ออก v+1 (immutable) + คำนวณ stale | `PUR-xx` (purpose code) | purpose, version |
| 7 | `purpose.closed` | FN-04 `closePurpose` (03_LOGIC §3.1) · API-05 · BR-14 | SecC `[DEFAULT]` | ปิดวัตถุประสงค์ (ห้ามคำขอใหม่ · consent เดิมคงอยู่) | `PUR-xx` (purpose code) | purpose |

**idempotency_key** ทุก event = `F-MKT-CONSENT:<ref>:<event_id>` (BR-CSQ-02 · UNIQUE ที่ T_consent_csq_outbox) — ยืนยันตรงกับ HTML L2320.

> ⚠️ ไม่ใช่ทุก transition = event: `draft → pending` (สร้าง/ส่งคำขอ, FN-05/06) **ไม่ประกาศ** (ยังไม่มีผลต่อสถานะความยินยอม) · `pending → expired` (คำขอหมดเวลา 30 วัน, BR-08) **ไม่ประกาศ** (lapsed ≠ decision — เป็น timeout ฝั่งคำขอ ไม่ใช่ผลของ subject)

---

## §3 · ท่อที่ **ไม่** ประกาศ (และเหตุผล) — สำคัญที่สุด

| ท่อ | ประกาศ? | เหตุผล |
|---|:--:|---|
| **OC** (Operation Cost) | ❌ ห้าม | OP เป็นเจ้าของท่อ OC เจ้าเดียว · event ทั้ง 7 ไม่ได้มาจาก Operation Process — ประกาศซ้ำ = register **reject 422** (LOCK-CSQ-01 · BR-CSQ-05 · Quality Gate G1) |
| **DC** (Decision) | ❌ ห้าม | การยินยอม/ถอน = การตัดสินใจของ **เจ้าของข้อมูล** ผ่าน recipient view + ไม่มีสายอนุมัติภายใน (LOCK-04, BR-09) · DC ระดับเอกสารมาจาก DOA engine อัตโนมัติ — feature ห้ามประกาศ (LOCK-CSQ-02 · Quality Gate G2) |
| **SC** (สงวน) | ❌ ห้าม | สงวนไว้ทั้งระบบ (OQ-C3 ยังไม่เคาะ) — trigger=false เสมอ (LOCK-CSQ-03 · Quality Gate G3) |
| **EC** (Economic/มูลค่า-ต้นทุน) | ⛔ no-effect | ไม่มีมูลค่า/ต้นทุน/amount ในทุก event · LOCK-CSQ-04 ห้ามคำนวณมูลค่า + 04_DB ห้ามมีคอลัมน์ amount · PR-9 (financial race) = N/A |
| **AC** (Accounting) | ⛔ no-effect | ไม่เกิดรายการทางบัญชี (ไม่ตั้งหนี้/ตัดหนี้/ลงบัญชี/ค่าเสื่อม) |
| **FC** (Financial/เงินสด-งบ) | ⛔ no-effect | ไม่กระทบเงินสด/commit/งบประมาณ |
| **SecC** (Security/ข้อมูลอ่อนไหว) | ✅ ประกาศ `[DEFAULT — รอยืนยัน]` | consent lifecycle = **เปลี่ยนสิทธิ์/นโยบายการใช้ข้อมูลส่วนบุคคล (PII)** ต่อคู่ subject×purpose×channel → เข้านิยาม SecC ตาม §Trigger Rule ("แก้ข้อมูลอ่อนไหว / เปลี่ยนสิทธิ์-นโยบาย") · field PII: subject_ref/id_method/ip_device (04_DB §4.6.4) · **ยังไม่ยืนยันกับ csq-contract master (ไฟล์ไม่มีในเครื่อง)** → OQ-CSQ-02 |

> **สรุปเจตนา:** feature นี้ **ปล่อย envelope อย่างเดียว** (declare-only) — LOCK-CSQ-04 (ไม่ตีมูลค่า) · LOCK-CSQ-05 (ไม่มีคอลัมน์ผลรายท่อใน T_consent_csq_outbox) · LOCK-CSQ-06 (ไม่วาดการ์ดผล 7 ท่อบนหน้าจอ) ยืนยันตรงกับ HTML `emitConsequence` (L2324 "invisible sink") และ 04_DB §4.2 (T_consent_csq_outbox เก็บ envelope เท่านั้น)

---

## §4 · Payload Contract (envelope → 7C Engine)

**Envelope (ระดับซอง — ยืนยันจาก HTML L2316–2323):**

| field | ชนิด | มาจาก | หมายเหตุ |
|---|---|---|---|
| `feature` | string const | — | `'F-MKT-CONSENT'` |
| `event_id` | enum(7) | §2 | ชื่อ event ทั้ง 7 |
| `ref` | string | CNS/REQ/PUR code | รายการอ้างอิง (idempotency subject) |
| `idempotency_key` | string | derived | `F-MKT-CONSENT:<ref>:<event_id>` · UNIQUE (BR-CSQ-02) |
| `reversal_of` | string \| null | `T_consent.grant_event_id` | ตั้งค่าเฉพาะ `consent.withdrawn` (BR-CSQ-04) |
| `payload` | jsonb | ตามตารางล่าง | **masked** ก่อนส่ง (BR-CSQ-03) |

**Payload fields (ทุก field มีอยู่จริงใน 04_DB — Quality Gate G5 ✅):**

| payload field | DB field (table) | ชนิด | Classification | mask? |
|---|---|---|---|---|
| `subject` | `subject_ref` (T_consent / T_consent_request) | varchar(32) | **Confidential + PII** | ✅ **ต้อง mask** ก่อนส่ง (BR-CSQ-03 · D7) |
| `purpose` | `purpose_id → code` (T_consent / T_consent_purpose) | uuid→code | Internal | — |
| `channel` | `channel` (T_consent) | enum(5) | Internal | — |
| `policy_version` | `policy_version` (T_consent) | integer | Internal | — (snapshot ณ เซ็น, BR-06) |
| `reversal_of` | `grant_event_id` (T_consent) | varchar(128) | Internal | — |
| `refOld` | `ref_old` (T_consent_request) | uuid | Internal | — |
| `version` | `v` (T_consent_policy_version) | integer | Internal | — |

> **ไม่มี Restricted field** ใน 04_DB (§4.6.1) → ไม่มี field ที่ต้องตัดทิ้ง แต่ **subject_ref เป็น Confidential+PII ต้อง mask** ที่ producer ก่อน enqueue (BR-CSQ-03)
> **Sink:** ทุก event enqueue ที่ `T_consent_csq_outbox` (04_DB §4.2) → `delivered` flag → deploy pipeline ส่งเข้า 7C

---

## §5 · Register Checklist (ก่อน deploy จะ register profile สำเร็จ)

- [ ] จัดสรรเลข `CSQ-NN` จริงจาก 7C Profile Registry แทน `CSQ-F058` (OQ-CSQ-01)
- [ ] ยืนยันชื่อท่อ **SecC** กับ `csq-contract.md` master / F-CSQ-01 owner (OQ-CSQ-02) — enum ต้องตรง catalog ก่อน register ไม่งั้น reject
- [ ] ตรวจว่า **ไม่มี** `oc` / `dc` / `sc` ในใบประกาศ (Quality Gate G1/G2/G3 — ระบบ enforce จริง reject 422) ✅ ผ่านแล้วในใบนี้
- [ ] dev wire `emitConsequence` (FN-19) ที่ transition จริงทั้ง 6 จุดเรียก (FN-02/04/09/13/14/15) + ใส่ `idempotency_key`
- [ ] mask `subject_ref` ที่ producer ก่อนส่ง (BR-CSQ-03)
- [ ] `consent.withdrawn` แนบ `reversal_of = grant_event_id` เสมอ (BR-CSQ-04)
- [ ] UNIQUE(tenant_id, idempotency_key) ที่ T_consent_csq_outbox พร้อม (กันยิงซ้ำ retry)
- [ ] deploy → ตรวจแถวใน Profile Registry ของ 7C เปลี่ยนเป็น **เชื่อมแล้ว** + Event Log event แรกไม่ค้าง "ยังไม่ประเมิน"

---

## §6 · Open Questions

| OQ | คำถาม | ใครตอบ | ผลถ้าเดาผิด |
|---|---|---|---|
| OQ-CSQ-01 | เลข profile `CSQ-NN` ที่ถูกต้องของ feature นี้คือเลขอะไร | BA + 7C Profile Registry owner | register ชนเลข/ผิดคาน |
| OQ-CSQ-02 | ท่อที่ถูกต้องของ consent lifecycle events คือ **SecC** ตามที่ประกาศไว้หรือไม่ (csq-contract.md master ไม่มีในเครื่อง จึงยืนยัน enum ไม่ได้) | BA + F-CSQ-01 owner | ประกาศผิดท่อ = ผลกระทบไปประทับผิดหมวดใน 7C |
| OQ-CSQ-03 | consent event ควรถือเป็น **DC (terminal decision ของเจ้าของข้อมูล)** เพิ่มเติมด้วยหรือไม่ — ใบนี้ **ไม่ประกาศ DC** ตามคำสั่งงาน/LOCK-CSQ-02 (DC มาจาก DOA อัตโนมัติ) | BA + F-CSQ-01 owner | ถ้า policy ตีความว่าต้องมี DC จริง จะขาด declaration |
| OQ-CSQ-03b | (สืบเนื่อง OQ-03 ใน 03_LOGIC §3.5) `id_method` จริง (ตอนนี้ mock) — ไม่กระทบ envelope แต่กระทบ evidence | BA | — |

---

### ภาคผนวก · Traceability
- **7 events:** ยืนยันครบตรงกัน 3 แหล่ง — FRD `03_LOGIC §3.4` (list 1–7) · HTML `emitConsequence` call sites (L2664/2737/2742/2898/2990/3008/3017) · 04_DB `T_consent_csq_outbox.event_id` enum
- **declare-only:** HTML L2312–2325 ("renders NOTHING · no pipe cards · no value calc" · "invisible sink") · 04_DB §4.2 LOCK-CSQ-04/05 · BR-CSQ-01/05
- **Quality Gate self-check:** G1 ✅ (no oc) · G2 ✅ (no dc-approval) · G3 ✅ (no sc) · G4 ✅ (ทุก event มี FN/BR ref) · G5 ✅ (payload ⊂ 04_DB) · G6/G7 N/A (ไม่มี EC) · G8 ✅ (SecC + profile_id + group ติด `[DEFAULT — รอยืนยัน]`) · G9 ✅ (ใช้ vocabulary เดิม)
