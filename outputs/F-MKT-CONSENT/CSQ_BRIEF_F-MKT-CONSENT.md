# CSQ_BRIEF — F-MKT-CONSENT · ความยินยอม PDPA

> **ใบประกาศ 7C Consequence (declare-only)** — ออกโดย skill `csq-declaration` v1.0 (companion ของ F-CSQ-01 Consequence Engine)
> **สถานะ:** DECLARE-ONLY — feature เป็น **ผู้ประกาศ event** เท่านั้น · ไม่ตีมูลค่า · ไม่ประทับผลรายท่อ · ไม่วาดการ์ดผล 7 ท่อ
> **Source of truth (FRD v1.1 · re-gate refresh):** `FRD_Pack/03_LOGIC.md §3.1 FN-19 · §3.4` · `FRD_Pack/05_RULES.md §5.1 (BR-CSQ-01..05 + BR-23..26)` · `FRD_Pack/04_DB.md §4.2 T_consent_csq_outbox` · `consent-pdpa.html emitConsequence()` (L2332–2344)
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
| version | v1.1 (2026-09-14) — refresh หลัง BA-gate + FRD v1.1 (FIX-01..05) · **envelope/7 events ไม่เปลี่ยน** |
| producer contract | Envelope ตาม F-CSQ-01 §2.3 · `POST /csq/events` |

---

## §2 · Declared Events (7 events — ยืนยันจาก FRD §3.4 + HTML `emitConsequence` call sites)

> **`event_id`** ยึด vocabulary ที่ enumerate ไว้แล้วใน FRD/HTML — **ไม่คิดคำใหม่**
> **ท่อที่ยิง** = ท่อที่ **feature ประกาศ**เท่านั้น · การประเมินผล/ตีมูลค่ารายท่อเป็นหน้าที่ ENG-CSQ-02 (ไม่ใช่ feature)
> ท่อที่ประกาศทั้งใบ = **SecC** `[DEFAULT — รอยืนยัน]` (เหตุผล §3) · **ไม่มี** OC/DC/SC/EC/AC/FC (ล็อกดู §3)

| # | event_id | trigger point (FRD ref) | ท่อที่ยิง | เงื่อนไข (เมื่อไหร่ยิง) | ref (idempotency subject) | payload fields |
|:--:|---|---|---|---|---|---|
| 1 | `consent.granted` | FN-09 `applyAnswers` (03_LOGIC §3.1) · API-13 · BR-06/15 | SecC `[DEFAULT]` | recipient ยืนยันตัวตน + ตอบ "ยินยอม" ต่อ purpose → INSERT T_consent(granted) · guard answered=terminal (BR-23) | `CNS-xxxx` (consent id) | subject, purpose, channel, policy_version |
| 2 | `consent.declined` | FN-09 `applyAnswers` (03_LOGIC §3.1) · API-13 · EC-06/S-11 | SecC `[DEFAULT]` | recipient ตอบ "ไม่ยินยอม" ต่อ purpose → INSERT T_consent(declined) · guard answered=terminal (BR-23) | `CNS-xxxx` (consent id) | subject, purpose, channel |
| 3 | `consent.withdrawn` | FN-13 `withdrawConsent` (03_LOGIC §3.1) · API-17 · BR-09/10 · EC-08 · **FIX-05/BR-26** | SecC `[DEFAULT]` | เจ้าหน้าที่/dpo ถอน (มีผลทันที ไม่อนุมัติ) → UPDATE status=withdrawn · **ยิงได้เฉพาะเมื่อ eff_status=granted** (UI guard กันยิงซ้ำ · §4.1) | `CNS-xxxx` (consent id) | subject, purpose, channel, **reversal_of = grant_event_id** (BR-CSQ-04) |
| 4 | `consent.renew_requested` | FN-14 `renewConsent` → FN-05 (03_LOGIC §3.1) · API-19 · BR-13 | SecC `[DEFAULT]` | สร้างคำขอต่ออายุอ้างรายการเดิม (ไม่แก้ expires_at เดิม) | `REQ-xxxx` (new request id) | subject, refOld |
| 5 | `consent.reconsent_requested` | FN-15 `reConsent` → FN-05 (03_LOGIC §3.1) · API-04 flow / registry action · EC-03/BR-06 | SecC `[DEFAULT]` | ขอความยินยอมใหม่กับ consent ที่ policy stale (v เดิม < current_ver) | `REQ-xxxx` (new request id) | subject, purpose, refOld |
| 6 | `policy.version_published` | FN-02 `publishPolicyVersion` → FN-17 (03_LOGIC §3.1) · API-04 · BR-05 | SecC `[DEFAULT]` | อัปโหลดเอกสารนโยบายใหม่ → ออก v+1 (immutable) + คำนวณ stale | `PUR-xx` (purpose code) | purpose, version |
| 7 | `purpose.closed` | FN-04 `closePurpose` (03_LOGIC §3.1) · API-05 · BR-14 | SecC `[DEFAULT]` | ปิดวัตถุประสงค์ (ห้ามคำขอใหม่ · consent เดิมคงอยู่) | `PUR-xx` (purpose code) | purpose |

**idempotency_key** ทุก event = `F-MKT-CONSENT:<ref>:<event_id>` (BR-CSQ-02 · UNIQUE ที่ T_consent_csq_outbox) — ยืนยันตรงกับ HTML L2337.

> ⚠️ ไม่ใช่ทุก transition = event:
> - `draft → pending` (สร้าง/ส่งคำขอ, FN-05/06) **ไม่ประกาศ** (ยังไม่มีผลต่อสถานะความยินยอม)
> - `pending → expired` (คำขอหมดเวลา 30 วัน, BR-08) **ไม่ประกาศ** (lapsed ≠ decision — เป็น timeout ฝั่งคำขอ ไม่ใช่ผลของ subject)
> - **การส่ง/snapshot เวอร์ชัน (FN-06 recordSend + FN-21 `snapshotVers` · BR-24 · FIX-03 NEW)** **ไม่ประกาศ** — เป็นหลักฐาน "ส่งเอกสารเวอร์ชันไหน" ฝั่งคำขอ ไม่ใช่ผลของ subject · **FN-21 ไม่เพิ่ม event ใหม่เข้า 7C**

---

## §3 · ท่อที่ **ไม่** ประกาศ (และเหตุผล) — สำคัญที่สุด

| ท่อ | ประกาศ? | เหตุผล |
|---|:--:|---|
| **OC** (Operation Cost) | ❌ ห้าม | OP เป็นเจ้าของท่อ OC เจ้าเดียว · event ทั้ง 7 ไม่ได้มาจาก Operation Process — ประกาศซ้ำ = register **reject 422** (LOCK-CSQ-01 · BR-CSQ-05 · Quality Gate G1) |
| **DC** (Decision) | ❌ ห้าม | การยินยอม/ถอน = การตัดสินใจของ **เจ้าของข้อมูล** ผ่าน recipient view + ไม่มีสายอนุมัติภายใน (LOCK-04, BR-09) · DC ระดับเอกสารมาจาก DOA engine อัตโนมัติ — feature ห้ามประกาศ (LOCK-CSQ-02 · Quality Gate G2) |
| **SC** (สงวน) | ❌ ห้าม | สงวนไว้ทั้งระบบ (OQ-C3 ยังไม่เคาะ) — trigger=false เสมอ (LOCK-CSQ-03 · Quality Gate G3) |
| **EC** (Economic/มูลค่า-ต้นทุน) | ⛔ no-effect | ไม่มีมูลค่า/ต้นทุน/amount ในทุก event · LOCK-CSQ-04 ห้ามคำนวณมูลค่า + 04_DB ห้ามมีคอลัมน์ amount · PR-9 (financial race) = N/A (05_RULES §5.5) |
| **AC** (Accounting) | ⛔ no-effect | ไม่เกิดรายการทางบัญชี (ไม่ตั้งหนี้/ตัดหนี้/ลงบัญชี/ค่าเสื่อม) |
| **FC** (Financial/เงินสด-งบ) | ⛔ no-effect | ไม่กระทบเงินสด/commit/งบประมาณ |
| **SecC** (Security/ข้อมูลอ่อนไหว) | ✅ ประกาศ `[DEFAULT — รอยืนยัน]` | consent lifecycle = **เปลี่ยนสิทธิ์/นโยบายการใช้ข้อมูลส่วนบุคคล (PII)** ต่อคู่ subject×purpose×channel → เข้านิยาม SecC ตาม §Trigger Rule ("แก้ข้อมูลอ่อนไหว / เปลี่ยนสิทธิ์-นโยบาย") · field PII: subject_ref/id_method/ip_device (04_DB §4.6 · 05_RULES D7) · **ยังไม่ยืนยันกับ csq-contract master (ไฟล์ไม่มีในเครื่อง)** → OQ-CSQ-02 |

> **สรุปเจตนา:** feature นี้ **ปล่อย envelope อย่างเดียว** (declare-only) — LOCK-CSQ-04 (ไม่ตีมูลค่า) · LOCK-CSQ-05 (ไม่มีคอลัมน์ผลรายท่อใน T_consent_csq_outbox) · LOCK-CSQ-06 (ไม่วาดการ์ดผล 7 ท่อบนหน้าจอ) ยืนยันตรงกับ HTML `emitConsequence` (L2341 "invisible sink") และ 04_DB §4.2 (T_consent_csq_outbox เก็บ envelope เท่านั้น)

---

## §4 · Payload Contract (envelope → 7C Engine)

**Envelope (ระดับซอง — ยืนยันจาก HTML L2333–2340):**

| field | ชนิด | มาจาก | หมายเหตุ |
|---|---|---|---|
| `feature` | string const | — | `'F-MKT-CONSENT'` |
| `event_id` | enum(7) | §2 | ชื่อ event ทั้ง 7 |
| `ref` | string | CNS/REQ/PUR code | รายการอ้างอิง (idempotency subject) |
| `idempotency_key` | string | derived | `F-MKT-CONSENT:<ref>:<event_id>` · UNIQUE (BR-CSQ-02) |
| `reversal_of` | string \| null | `T_consent.grant_event_id` | ตั้งค่าเฉพาะ `consent.withdrawn` (BR-CSQ-04) · default null |
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

> **ไม่มี Restricted field** ใน 04_DB (05_RULES §5.7 D-CLASS) → ไม่มี field ที่ต้องตัดทิ้ง แต่ **subject_ref เป็น Confidential+PII ต้อง mask** ที่ producer ก่อน enqueue (BR-CSQ-03)
> **Sink:** ทุก event enqueue ที่ `T_consent_csq_outbox` (04_DB §4.2) → `delivered` flag → deploy pipeline ส่งเข้า 7C

### §4.1 · Idempotency + UI backstop (envelope idempotent เดิม · FIX-05 เสริมฝั่ง UI)

- **ชั้น envelope (ไม่เปลี่ยน):** `idempotency_key = F-MKT-CONSENT:<ref>:<event_id>` UNIQUE(tenant_id, idempotency_key) ที่ T_consent_csq_outbox → ยิงซ้ำ/retry ตัวเดียวกันถูก dedupe เสมอ (BR-CSQ-02 · CSQ_ERR_DUPLICATE_ENVELOPE 422 กันซ้ำ). **การันตี idempotency มาจากชั้นนี้เป็นหลัก**
- **ชั้น UI backstop (ใหม่จาก FIX-05 · BR-26):** UI คุมไม่ให้ `consent.withdrawn` ถูก emit **สองครั้ง**สำหรับ consent เดียวกัน — `doWithdraw()` มี guard `effStatus(c)!=='granted' → return` (HTML L3034) จึงถอนได้เฉพาะรายการที่ยัง granted อยู่ (withdrawn/declined/expired/pending กดไม่ติด). เช่นเดียวกัน sendVia คุม draft/pending เท่านั้น + `guardBusy` กัน double-click ทุก mutation.
  - **นัยต่อ CSQ:** envelope เป็น idempotent อยู่แล้ว — FIX-05 คือ **backstop เสริมฝั่ง UI** ให้ไม่มีแม้แต่การพยายามยิง duplicate ตั้งแต่ต้นทาง (defense-in-depth) · **ไม่เพิ่ม/ไม่ลบ event · ไม่เปลี่ยน payload/envelope** — 7 events + schema เดิมทุกประการ

---

## §5 · Register Checklist (ก่อน deploy จะ register profile สำเร็จ)

- [ ] จัดสรรเลข `CSQ-NN` จริงจาก 7C Profile Registry แทน `CSQ-F058` (OQ-CSQ-01)
- [ ] ยืนยันชื่อท่อ **SecC** กับ `csq-contract.md` master / F-CSQ-01 owner (OQ-CSQ-02) — enum ต้องตรง catalog ก่อน register ไม่งั้น reject
- [ ] ตรวจว่า **ไม่มี** `oc` / `dc` / `sc` ในใบประกาศ (Quality Gate G1/G2/G3 — ระบบ enforce จริง reject 422) ✅ ผ่านแล้วในใบนี้
- [ ] dev wire `emitConsequence` (FN-19) ที่ transition จริงทั้ง 7 จุดเรียก (FN-02/04/09×2 [granted+declined]/13/14/15) + ใส่ `idempotency_key`
- [ ] mask `subject_ref` ที่ producer ก่อนส่ง (BR-CSQ-03)
- [ ] `consent.withdrawn` แนบ `reversal_of = grant_event_id` เสมอ (BR-CSQ-04) + wire guard granted-only (FIX-05 · BR-26) ให้ยิงครั้งเดียวต่อ consent
- [ ] UNIQUE(tenant_id, idempotency_key) ที่ T_consent_csq_outbox พร้อม (กันยิงซ้ำ retry — ชั้นการันตีหลัก)
- [ ] deploy → ตรวจแถวใน Profile Registry ของ 7C เปลี่ยนเป็น **เชื่อมแล้ว** + Event Log event แรกไม่ค้าง "ยังไม่ประเมิน"

---

## §6 · Open Questions

| OQ | คำถาม | ใครตอบ | ผลถ้าเดาผิด |
|---|---|---|---|
| OQ-CSQ-01 | เลข profile `CSQ-NN` ที่ถูกต้องของ feature นี้คือเลขอะไร (ตอนนี้ placeholder `CSQ-F058`) | BA + 7C Profile Registry owner | register ชนเลข/ผิดคาน |
| OQ-CSQ-02 | ท่อที่ถูกต้องของ consent lifecycle events คือ **SecC** ตามที่ประกาศไว้หรือไม่ (`[DEFAULT]` — csq-contract.md master **ไม่มีในเครื่อง** จึงยืนยัน enum กับ catalog กลางไม่ได้) | BA + F-CSQ-01 owner | ประกาศผิดท่อ = ผลกระทบไปประทับผิดหมวดใน 7C |
| OQ-CSQ-03 | consent event ควรถือเป็น **DC (terminal decision ของเจ้าของข้อมูล)** เพิ่มเติมด้วยหรือไม่ — ใบนี้ **ไม่ประกาศ DC** ตาม LOCK-CSQ-02 (DC ระดับเอกสารมาจาก DOA อัตโนมัติ) | BA + F-CSQ-01 owner | ถ้า policy ตีความว่าต้องมี DC จริง จะขาด declaration |
| OQ-CSQ-03b | (สืบเนื่อง OQ-03 ใน 03_LOGIC §3.6) `id_method` จริง (ตอนนี้ mock "ลิงก์ที่ส่งถึงเจ้าตัว") — ไม่กระทบ envelope แต่กระทบ evidence | BA | — |

---

### ภาคผนวก · Traceability

- **7 events:** ยืนยันครบตรงกัน 3 แหล่ง — FRD `03_LOGIC §3.4` (list 1–7) · HTML `emitConsequence` call sites (**L2691 renew · L2777 granted · L2782 declined · L2946 reconsent · L3041 withdrawn · L3062 version_published · L3074 purpose.closed**) · 04_DB `T_consent_csq_outbox.event_id` enum
- **declare-only:** HTML L2328–2343 ("renders NOTHING · no pipe cards · no value calc" · "invisible sink" L2341) · 04_DB §4.2 LOCK-CSQ-04/05 · BR-CSQ-01/05
- **FIX-05 UI idempotency backstop:** HTML `doWithdraw` guard L3034 (`effStatus(c)!=='granted' → return`) + emit L3041 · 05_RULES BR-26 · EC-13 · 03_LOGIC FN-13 guard order — **envelope idempotency (BR-CSQ-02) ไม่เปลี่ยน · 7 events ไม่เปลี่ยน**
- **Quality Gate self-check:** G1 ✅ (no oc) · G2 ✅ (no dc-approval) · G3 ✅ (no sc) · G4 ✅ (ทุก event มี FN/BR ref) · G5 ✅ (payload ⊂ 04_DB) · G6/G7 N/A (ไม่มี EC) · G8 ✅ (SecC + profile_id + group ติด `[DEFAULT — รอยืนยัน]`) · G9 ✅ (ใช้ vocabulary เดิม)
</content>
</invoke>
