# 07_LOCKED_DECISIONS — F-MKT-CONSENT ความยินยอม PDPA

> **Audience:** All roles
> **Purpose:** Scope Lock (immutable) + Locked Decisions — ห้ามเปิดอภิปรายซ้ำ

---

## §7.0 Scope Lock (Imported from BRD §3.4 / PREBRIEF Part C) — IMMUTABLE

> สืบทอดจาก PREBRIEF Part C (10 locks) · **ห้าม override ตลอด pack + chain ปลายน้ำ** — spec ใดขัด LOCK → LOCK ชนะ

| LOCK-ID | ข้อยืนยัน | อ้างเอกสาร | สถานะใน FRD |
|---|---|---|---|
| LOCK-04 | ไม่มีสายอนุมัติภายในก่อนส่งคำขอ | Part C#2 | ✅ สอดคล้อง (ไม่มี approval chain · withdraw ทันที · doa ไม่เลือก) |
| LOCK-05 | ไม่ทำความยินยอมคุกกี้บนเว็บ | Part C#1 | ✅ (NEG-40.1) |
| LOCK-07 | สร้างคำขอ = single-screen (ไม่ wizard Pattern Q) | Part C#10 | ✅ (FN-05 · AT-05 · NEG-40.10) |
| LOCK-CSQ-01 | ไม่ประกาศท่อ OC | Part C#6 | ✅ (FN-19 declare-only) |
| LOCK-CSQ-02 | ไม่ประกาศท่อ DC ระดับเอกสาร | Part C#6 | ✅ (มาจาก DOA engine · doa/doccfg ไม่เลือก) |
| LOCK-CSQ-03 | ไม่ประกาศท่อ SC | Part C#6 | ✅ (trigger=false) |
| LOCK-CSQ-04 | ไม่คำนวณมูลค่าใด ๆ | Part C#4 | ✅ (ไม่มี amount field · NEG-40.4) |
| LOCK-CSQ-05 | ไม่มีคอลัมน์เก็บผลรายท่อ | Part C#4 | ✅ (T_consent_csq_outbox = envelope only) |
| LOCK-CSQ-06 | ไม่วาดการ์ดผล 7 ท่อบนจอ | Part C#5 | ✅ (NEG-40.5) |
| (lock#7) | ไม่ใช้ธง opt-out เดียวต่อคน — ต้อง triple | Part C#7 | ✅ (partial-unique triple · NEG-40.7) |
| (lock#8) | "ไม่ตอบ" ≠ "ไม่ยินยอม" | Part C#8 | ✅ (BR-08 · AT-20b) |
| (lock#9) | บล็อกการส่งด้วยตัวเอง — resolve ตอบอย่างเดียว | Part C#9 | ✅ (API-20 read-only) |
| (lock#3) | ไม่ส่งอีเมล/SMS/LINE จริง | Part C#3 | ✅ (mock toast · NEG-40.3) |

- **Scope Lock Ref:** **N/A — standalone** (plan `dep=""` · ไม่ผ่าน chain ใบเซ็นข้ามฟีเจอร์) — locks สืบทอดจาก PREBRIEF Part C
- **Drift พบระหว่างเขียน FRD (ชั้นที่ 3):** ไม่มี scope เกิน lock · content-model divergence (upload) = **DECLARED-01** (ประกาศไว้ ไม่ใช่ drift เงียบ) → OQ-01

---

## §7.1 Locked Decisions (LD)

### LD-01: Content model = uploaded documents (versioned) — DECLARED-01
- **Date:** 2026-09-11 (มติ PM/BA) · encode ใน FRD 2026-09-13
- **Context:** PREBRIEF BR-05/06 + S-01/02/09 + FN-01/02/09/10/11 = free-text (พิมพ์ข้อความ) · HTML ที่สร้างจริง = **เอกสารอัปโหลด versioned per purpose**
- **Options:** A) free-text ตาม PREBRIEF · B) uploaded document (built model)
- **Decision:** **B** — FRD ยึดโมเดล built (upload) · old ≥40-char free-text rule **REPLACED** by "create-purpose + new-version ต้องแนบเอกสาร"
- **Rationale:** HTML ผ่าน ux+coverage+e2e gate = de facto (v6.1 HTML-first) · เป็นมติ PM/BA ที่บันทึกใน FUNCTION_CHECKLIST header + coverage DECLARED-01
- **Implications:** 04_DB T_consent_policy_version (doc_name/doc_type/doc_ref) · FN-01/02 validate "แนบเอกสาร" · viewer = viewPolicy() `.doc-frame` · docName = `.doc-link`
- **Governance:** BA ต้อง sync PREBRIEF ให้ตรง → **OQ-01** (จนกว่า sync = divergence ที่ประกาศ ไม่นับตก)
- **Reversibility:** LOW (business decision locked)

### LD-02: `/consent/resolve` locked contract (BR-19/20)
- **Decision:** response schema = `{subject, purpose, channel, allowed, status, policy_version, granted_at, expires_at, found, reason}` · **HTTP 200 เสมอ** · never_asked = allowed:false (ไม่ 404)
- **Rationale:** downstream (campaign/F143) พึ่งสัญญานี้ — เพิ่มฟิลด์ได้ ห้ามเปลี่ยนชื่อ/ความหมายเดิม
- **Implications:** ENG-01 output immutable · contract test (06 §6.4)
- **Reversibility:** LOCKED (external contract)

### LD-03: No approval chain — withdraw immediate (LOCK-04)
- **Decision:** ไม่มี Checker/Approver · ถอนมีผลทันที · control = default-deny + evidence + append-only audit
- **Rationale:** PDPA — เจ้าของข้อมูลถอนได้ทุกเมื่อ · Part C#2
- **Declaration impact:** **doa ไม่เลือก** (ไม่มีสายอนุมัติ) · **doccfg ไม่เลือก** (ไม่ใช่เอกสารธุรกรรม/ไม่มีเลขรัน) · **ntf ไม่เลือก** (ไม่มี event แจ้งเตือน)
- **Reversibility:** LOCKED

### LD-04: Recipient view replaces in-drawer sim buttons
- **Decision:** เซ็นผ่าน full-screen recipient view (openRecipientView → recipientViewHTML → submitRecipient → applyAnswers · z=--z-recipient 70)
- **Rationale:** จำลองลิงก์ภายนอกจริง (อ่านเอกสาร→ยืนยันตัวตน→ยินยอมรายข้อ→เซ็น) · in-scope mock (ไม่ใช่ email/LINE จริง)
- **Open:** วิธียืนยันตัวตนจริง = checkbox mock → **OQ-03** (ห้าม dev เดา)
- **Reversibility:** MEDIUM (จอ locked · id_method จริงรอ BA)

### LD-05: CSQ declare-only (7 events · idempotency + reversal · no OC/DC/SC)
- **Decision:** FN-19 emitConsequence สร้าง envelope (idempotency_key `F-MKT-CONSENT:<ref>:<event>` · reversal_of ตอนถอน) · **ห้ามประกาศ/คำนวณ OC/DC/SC**
- **Rationale:** OC มาจาก Operation Process · DC ระดับเอกสารมาจาก DOA engine · SC สงวน — ประกาศซ้ำ = register reject 422
- **Events:** consent.granted/declined/withdrawn/renew_requested/reconsent_requested · policy.version_published · purpose.closed
- **Downstream:** ออก `CSQ_BRIEF_F-MKT-CONSENT.md` ที่ step 7 (csq-declaration — **ผู้ใช้สั่ง/parent จัดการ ไม่ auto**)
- **Reversibility:** LOCKED (LOCK-CSQ-01..06)

### LD-06: Engines register CUBIC at hand-off (DRAFT now)
- **Decision:** ENG-01 consent-resolution-engine + ENG-02 consent-status-evaluator = DRAFT ใน FRD → register ตอน dev hand-off (ENG-01 คู่กับ F143 review)
- **Reversibility:** EASY

### LD-07: Request answered = terminal · re-answer blocked · evidence immutable (FIX-01 · BR-23)
- **Date:** 2026-09-14 (BA-gate round)
- **Context:** เดิม applyAnswers ไม่เช็คสถานะ → คำขอ answered ถูกตอบซ้ำได้ไม่จำกัด แต่ละครั้งสร้าง consent ใหม่ + supersede หลักฐานเดิม (bypass B1/B2: consents 9→11 จากคำขอเดียว) = evidence chain (หัวใจ PDPA + ฐาน DSAR) ถูกเขียนทับ
- **Decision:** applyAnswers guard `status ∈ {draft,pending}` เท่านั้น (คุมทั้ง officer-answer + recipient-submit ที่จุดเดียว) · ตอบแล้ว set `answered_at` = terminal · ลูกค้าเปิดลิงก์ซ้ำ = หน้าสถานะปิด · **ไม่มี supersede-on-re-answer** (evidence เดิม immutable)
- **Change path (เปลี่ยนใจหลังตอบ):** คำขอใหม่ / withdraw ตาม flow ปกติ — **ไม่ทำ flow แก้คำตอบผ่านลิงก์เดิม** → **OQ-CNS-01** (ใครเปิดคำขอใหม่ได้ · Strike เคาะ)
- **Related:** publish เวอร์ชันใหม่ระหว่าง pending ค้าง = **ไม่ auto-expire** (แสดง sent-version snapshot + เตือน · FIX-03) → **OQ-CNS-02**
- **Reversibility:** LOW (PDPA evidence integrity)

### LD-08: Contract anchors (display-only) — F136 / F031 / F157 (FIX-06)
- **Decision:** ประกาศ consumer 3 ตัวเป็น anchor (comment) — resolveConsent = API ให้ **F136 Broadcast (ctl · ตรวจ opt-in ก่อนส่ง)** + **F031 Customer 360 (data)** consume · ทะเบียน consent + evidence + history = ฐานข้อมูลให้ **F157 DSAR (data)** · **display-only — ไม่ mock หน้าจอ feature อื่น** (นอกขอบเขต)
- **Rationale:** Phase B เขียน §Integration ได้ · d "เป็นฐานข้อมูลให้ DSAR" มีร่องรอย
- **Reversibility:** LOCKED (Feature List contract)

---

## §7.2 Convention Deviations

### CD-01: POST custom actions แทน PUT/PATCH
- **Convention default:** PATCH สำหรับ partial state update
- **Deviation:** POST `/…/close`, `/…/withdraw`, `/…/renew`, `/…/send`, `/…/versions`
- **Reason:** state transition = action semantics (ไม่ใช่ property update) · ตรง state machine §5.2
- **Approved by:** Tech Lead (FRD gen)

### CD-02: scope-local ID prefix `F058-`
- **Deviation:** ใช้ `F058-` (plan id) แทน `F-MKT-CONSENT-` เต็ม เพื่อกระชับในตาราง — mapping ระบุใน 00 §0.1

---

## §7.3 Open Questions (pointer → 00_OVERVIEW §0.8)
OQ-01 (governance sync PREBRIEF) · OQ-02 (caller cache) · OQ-03 (id_method จริง — BLOCKING ก่อน impl) · OQ-04 (F143 register — BLOCKING go-live) · OQ-05 (permission enforce จริงต่อ role — FIX-02 mirror sec.can() · + E3 PDF) · OQ-06 (baseline) · OQ-07/08 ([AI-DEFAULT] upload validation / timezone) · **OQ-CNS-01** (post-answer change path + ใครเปิดคำขอใหม่ · Strike) · **OQ-CNS-02** (publish v ใหม่ระหว่าง pending: auto-expire vs answer-current · Strike) · **OQ-CNS-03** (renewal trigger manual vs batch · Strike)

## §7.4 Architecture Tradeoffs
- **AT-01:** PostgreSQL RLS over app-level filtering — accepted (CUBE standard)
- **AT-02:** resolve sync call — accepted V1 (caller cache ≤5 นาที ลด load, BR-21)
- **AT-03:** CSQ outbox pattern (INSERT + async deliver) over direct call — accepted (idempotency + retry safe)

## §7.5 Decisions Deferred to Implementation
| Item | Owner | Deadline |
|---|---|---|
| document upload size limit + storage (OQ-07) | BA/dev | sprint |
| timezone rule expires_at (OQ-08) | dev | sprint |
| id_method จริง recipient view (OQ-03) | BA | ก่อน implement |
| consent receipt PDF E3 (deferred) | PM | wave DSAR |

## §7.6 References
- Convention: `knowledge/conventions.md` · CUBIC: `references/cubic-schema-templates.md`
- Source: BRD_F-MKT-CONSENT.md · PREBRIEF Part C · consent-pdpa.html
