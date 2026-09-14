# 00_OVERVIEW — F-MKT-CONSENT ความยินยอม PDPA (Consent Management)

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Coverage Manifest + Open Questions
> **Generator:** frd-generator-v6 (v6.1 HTML-first · Design Authority Edition)

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-MKT-CONSENT (plan id **F058**) |
| **Feature Name** | ความยินยอม PDPA (Consent Management) |
| **Feature Code** | F-MKT-CONSENT |
| **Module** | Marketing |
| **Wave** | W1 |
| **Variant** | **FULL** (9 files + INDEX) |
| **Status** | DRAFT (awaiting BA/PM review — gate 2 · re-issued หลัง BA-gate fixes) |
| **FRD Version** | 1.1 (2026-09-14) — sync BA-gate round (FIX-01..08) + BRD v1.1 |
| **Generator** | frd-generator-v6 |
| **Source Brief** | — (no Brief; WF-01 lane — variant fallback จาก BRD) |
| **Source BRD** | `BRD_F-MKT-CONSENT.md` (status: **APPROVED** · v1.1 2026-09-14 — refreshed หลัง BA fixes) |
| **Source HTML** | `consent-pdpa.html` (updated · surgical BA fixes) — ผ่าน ux+coverage+e2e re-gate (2026-09-14 · เพิ่มเคส E41–E45 ครอบ FIX-01..05 · bypass B1..B8 ถูก block · FN 20/20) — **HTML-first source of truth ฝั่งหน้าจอ** |
| **Author** | tadswan@2bsimple.com (BA) |
| **Reviewers** | Tech Lead · PM · QA Lead · ทีม Security (F143 owner) |

> **ID convention note:** scope-local IDs ใช้ prefix `F058-` (= F-MKT-CONSENT) เพื่อความกระชับในตาราง เช่น `F058-API-01`, `F058-FN-01`. Global Engine IDs (`ENG-NNN`) assigned ตอน CUBIC Registry registration.

### Variant decision (fallback จาก BRD — ไม่ถาม user)
`Variant = FULL` — เหตุผล (Variant Fallback rules):
- pages = 5 surface (§14.6: registry / requests / purposes / resolve + recipient view)
- states ≥ 4 → **FULL trigger** (consent: pending/granted/declined/withdrawn + computed expired/near-expiry/stale + resolve-only never_asked)
- approval = **NO** (LOCK-04 ห้าม approval chain) · money = **NO** (LOCK-CSQ-04 ห้ามคำนวณมูลค่า)
- multi-engine = **YES** (2 engines: consent-resolution-engine + consent-status-evaluator)

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-09-13 | BA | Initial FRD generation (HTML-first · Recognize & Validate จาก consent-pdpa.html) |
| 1.1 | 2026-09-14 | BA | Re-sync หลัง BA-gate round (surgical HTML fixes + BRD v1.1). Encode: **FIX-01** answered = terminal state (re-answer blocked ที่ applyAnswers · evidence chain immutable · ลิงก์เปิดซ้ำ = หน้าสถานะปิด) · **FIX-02** role check ใน mutation function ทุกตัว (ไม่ใช่แค่ render · OQ-05) · **FIX-03** sends[] snapshot `vers:{purpose:version}` ณ เวลาส่ง + BR-06 panel เตือน stale · **FIX-04** `_busy` double-submit guard + loading state ทุก mutation · **FIX-05** sub-status guard (withdraw=granted only · resend=draft/pending only) · **FIX-06** contract anchors F136/F031/F157 · FIX-07/08 demo-only + pill column (01_UI). เพิ่ม OQ-CNS-01/02/03. |

---

## §0.3 Scope

### In Scope
- จัดการวัตถุประสงค์ (purpose) + ช่องทางที่ใช้ได้ + อายุความยินยอม + **เอกสารนโยบายแบบ versioned (อัปโหลด)** ← DECLARED-01
- สร้าง/ส่ง/ส่งซ้ำ/คัดลอกลิงก์+QR/ดาวน์โหลดเอกสาร ของคำขอความยินยอม (ส่งเป็น **mock** เท่านั้น)
- **มุมมองผู้รับ (recipient read+sign view)** — surface เต็มจอนอก ERP shell: เปิดลิงก์ → อ่านเอกสาร → ยืนยันตัวตน → ยินยอม/ไม่ยินยอมรายวัตถุประสงค์ → เซ็น
- ทะเบียนความยินยอม (triple key) + สถิติ + กรองทุกมิติ + Customer 360
- หลักฐาน 5 อย่าง + ประวัติ append-only ต่อรายการ
- ถอนแทนลูกค้า (มีผลทันที · ไม่ต้องอนุมัติ) · รายการใกล้หมดอายุ · ต่ออายุ (คำขอใหม่อ้างเดิม)
- ตัวจำลอง `/consent/resolve` (read-only simulator) + สัญญา JSON ที่ล็อกฟิลด์
- Declaration: **csq** (declare-only event hook → 7C Engine)

### Out of Scope (10 Locks — ดู 07_LOCKED §7.0)
- ความยินยอมคุกกี้บนเว็บ (LOCK-05) · สายอนุมัติก่อนส่งคำขอ (LOCK-04) · ส่งอีเมล/SMS/LINE จริง (mock เท่านั้น)
- คำนวณมูลค่า/คอลัมน์เก็บผลรายท่อ (LOCK-CSQ-04/05) · การ์ดผล 7 ท่อ CSQ บนจอ (LOCK-CSQ-06)
- ประกาศท่อ OC/DC/SC (LOCK-CSQ-01/02/03) · ธง opt-out เดียวต่อคน (ต้องใช้ triple)
- "ไม่ตอบ" = "ไม่ยินยอม" (lapsed ≠ declined) · บล็อกการส่งเอง (resolve ตอบอย่างเดียว) · wizard สร้างคำขอ (LOCK-07 single-screen)

### Out of Scope (Phase 2.5 — no probe skipped)
- Lane Mode: ทุก probe ที่ activate ตอบด้วย conservative default + tag `[AI-DEFAULT]` — ไม่มี probe ถูก skip (ดู §0.8 + 05_RULES §5.5)

---

## §0.4 Roles & Responsibilities (COSO)

> **ไม่มี approval chain (LOCK-04)** — COSO Checker/Approver ไม่ปรากฏในสายส่งคำขอ · การควบคุมอยู่ที่ default-deny + evidence 5 + audit trail append-only แทน SoD แบบอนุมัติ

| Role | Person/Team | Responsibilities |
|---|---|---|
| **Maker** | เจ้าหน้าที่การตลาด (officer) | สร้าง/ส่งคำขอ · ถอนแทนลูกค้า · ดูทะเบียน · resolve |
| **Maker+Admin** | ผู้ดูแลข้อมูล / DPO (dpo) | ทุกอย่างของ officer + สร้าง/แก้วัตถุประสงค์ + อัปโหลดเวอร์ชัน + ปิดวัตถุประสงค์ |
| **Read-only** | ผู้ตรวจสอบ (auditor) | อ่านทะเบียน/หลักฐาน/ประวัติ + resolve (อ่าน) — ไม่มี mutation |
| **Owner** | DPO | รักษาทะเบียน + monitor compliance |

> รายละเอียด permission ต่อ route/field → 05_RULES §5.3 Permission Matrix · ⚠️ HTML ปัจจุบันเป็น **persona switcher เดโม** (ไม่บังคับสิทธิ์จริง) → FRD ต้อง enforce จริง → OQ-05

---

## §0.5 Dependencies

### Upstream (this feature depends on)
| Dependency | Type | Source |
|---|---|---|
| ทะเบียนลูกค้า (subject CUS-xxxx) | Data (external ref เท่านั้น) | Customer Master (external) — ใช้ id อ้างอิง ไม่ join |

> **Standalone** — plan `dep=""` · ไม่มี upstream trigger เอกสารต้นทาง

### Downstream (features that depend on this) — contract anchors (FIX-06 · Feature List F058)
| Consumer | Type | What it uses |
|---|---|---|
| **F136 Broadcast** (แคมเปญส่งข้อความ/จดหมายข่าว) | **control (ctl)** | เรียก `POST /consent/resolve` ตรวจ opt-in **ก่อนส่ง Email/SMS ทุกครั้ง** (block อัตโนมัติเมื่อ allowed:false) |
| **F031 Customer 360** | **data** | สถานะ consent ผูกลูกค้า (subject) — ผล resolve + ทะเบียน |
| **F157 DSAR** | **data** | ทะเบียน consent + **evidence 5 + history append-only** = ฐานข้อมูลประกอบคำขอ DSAR (เดิม E3 receipt deferred · anchor ประกาศแล้ว) |
| **Backend Enforcement Gate (F143)** | registration | ทะเบียน endpoint `/consent/*` + review 4 ขั้น — **hard dependency ก่อน go-live** (BR-22) |
| 7C Consequence Engine (F-CSQ-01) | event (declare-only) | event envelope ทุก state change (ดู 03_LOGIC §3.4) |

> **FIX-06 (display-only):** anchor 3 contract ประกาศเป็น comment ในหน้าจอ (`consent-pdpa.html` head + tab resolve + registry) — **ห้าม mock หน้าจอ F136/F031/F157** ในรอบนี้ (นอกขอบเขต) · รายละเอียดสัญญา → 02_API §2.X

### External
| Service | Purpose |
|---|---|
| 7C Consequence Engine (F-CSQ-01) | `POST /csq/events` — declare-only sink (ดู CSQ_BRIEF step 7) |
| Backend Enforcement Gate (F143) | endpoint registry + 4-step review |

---

## §0.6 Stack & Architecture

| Layer | Technology |
|---|---|
| Frontend | React / Next.js / Tailwind (CUBE Warm Light CI — ยึด html-generator-v9 Sync Read, ห้าม hardcode hex) |
| API | Node.js / Strapi |
| Database | PostgreSQL (RLS multi-tenant) |
| Engine layer | CUBIC Registry (consent-resolution-engine, consent-status-evaluator) |
| Auth | JWT + role-based |
| Public surface | recipient view = tokenized public link (นอก ERP shell) |

**สถาปัตยกรรมหน้าจอ (observed จาก HTML):** โมดูล ERP หน้าเดียว **4 แท็บ** (hash route ใต้ `#/consent/...`) + recipient view เป็น surface แยกเต็มจอ + drawers/modals · default route = `#/consent/registry`

---

## §0.7 Multi-Tenant & Security Context

- [x] Multi-tenant feature: **YES**
- [x] PII data involved: **YES** (subject, evidence: idMethod / ipDevice — ดู 04_DB §4.2 + §4.6)
- [ ] Financial data: **NO** (LOCK-CSQ-04 ห้ามคำนวณมูลค่า — ไม่มี amount field)
- [x] Audit log required: **YES** (BR-16/17 append-only history + T_audit_log)

**Security Bible domains applied:** D2 (Auth) · D7 (PII) · D9 (Audit) · D15 (Admin actions) · D17 (Multi-tenant) · D-CLASS — see 05_RULES §5.7

### §0.7.1 Data Classification Summary (v5.1)
Highest classification level ที่ feature นี้แตะ:
- [ ] Has Restricted fields — **ไม่มี** (ไม่มี salary/financial/board — LOCK-CSQ-04)
- [x] **Has Confidential fields** ← highest level = **Confidential** (subject id, evidence idMethod/ipDevice, policy body)
- [x] Internal (default) — status/timestamps/audit
- [ ] Public-facing — recipient view แสดง policy body แต่ผ่าน token gate (ไม่ใช่ public data)

**Linkage:** ฟิลด์ Confidential + PII → register ที่ Policy Center → Data Classification + PDPA consent scope (ดู 04_DB §4.6.6)

---

## §0.8 Open Questions

> ยกเข้า `PROPOSALS_outbound.md` ที่ step 12 · carry ตรงจาก BRD §15 + FRD Phase 2.5

| ID | Question | Blocking? | Owner |
|---|---|---|---|
| **OQ-01** | **[GOVERNANCE]** BA sync PREBRIEF BR-05/06 + S-01/02/09 + FN-01/02/09/10/11 ให้เป็นโมเดล **"เอกสารอัปโหลด"** (DECLARED-01) — จนกว่า sync ถือเป็น divergence ที่ประกาศ ไม่นับตก | NO (declared) | BA |
| **OQ-02** | BR-21 caller-side cache ≤5 นาที + ล้างทันทีเมื่อถอน — สัญญาฝั่งผู้เรียก (document ใน 02_API §2.X · ไม่ทำ UI) | NO | ทีม integration |
| **OQ-03** | วิธียืนยันตัวตนจริงใน recipient view (ปัจจุบัน **checkbox mock** → ลิงก์/OTP/สแกนกระดาษ) — **ห้าม dev เดา** | **YES** (ก่อน implement วิธีจริง) | BA |
| **OQ-04** | BR-22 `/consent/*` ขึ้นทะเบียน Backend Enforcement Gate (F143) + review 4 ขั้น — confirm timeline/ขั้นตอน | **YES** (hard dependency go-live) | ทีม Security |
| **OQ-05** | Permission enforcement จริงต่อ role (แทน persona switcher เดโม) + consent receipt PDF (E3) deferred | NO | BA/PM |
| **OQ-06** | เก็บ baseline ตัวชี้วัด (BRD §2.3) ก่อน launch | NO (action) | PM |
| **OQ-07** `[AI-DEFAULT]` | อัปโหลดเอกสาร: validation ชนิด/ขนาดจริง (ปัจจุบัน accept `.pdf .doc .docx .txt`, mock ไม่ validate size) → default: allow 4 types + max size TBD | NO | BA/dev |
| **OQ-08** `[AI-DEFAULT]` | timezone rule ของ `expires_at` (lifespan เดือน) — default: คำนวณ UTC + display tenant TZ | NO | dev |
| **OQ-CNS-01** | เปลี่ยนใจ **หลังตอบคำขอแล้ว** — ปัจจุบันแก้ผ่านลิงก์เดิมไม่ได้ (FIX-01 answered=terminal) เส้นทางถูกคือ **คำขอใหม่ / withdraw** · **ใครมีสิทธิ์เปิดคำขอใหม่** → 03_LOGIC state machine | NO | Strike |
| **OQ-CNS-02** | ออกนโยบายเวอร์ชันใหม่ระหว่างคำขอ **pending ค้าง** — auto-expire คำขอเก่า (บังคับสร้างใหม่) vs ให้ตอบกับเวอร์ชันปัจจุบัน · **build ปัจจุบัน = ไม่ auto-expire** (แสดงเวอร์ชัน ณ ตอนส่ง + ป้ายเตือน FIX-03) → 03_LOGIC + BR | NO | Strike |
| **OQ-CNS-03** | รอบ **ต่ออายุ** — near-expiry 30 วันมีแล้ว ใคร/อะไร trigger คำขอต่ออายุ (manual จาก registry vs batch อัตโนมัติ · NTF ฝั่ง F136) | NO | Strike |

> Resolved → move to 07_LOCKED as LD-NN
> **OQ-CNS-01/02/03** = ประเด็นใหม่จาก BA-gate (Strike เคาะ) — build ปัจจุบันเลือก conservative (answered=terminal · no auto-expire) แขวนรอมติ ห้าม dev เดา

---

## §0.9 Glossary

| Term | Definition |
|---|---|
| **triple key** | เจ้าของข้อมูล × วัตถุประสงค์ × ช่องทาง (subject × purpose × channel) — คู่นี้ไม่ซ้ำในทะเบียน (BR-01) |
| **default-deny** | ไม่มี record ในทะเบียน = ส่งไม่ได้ (BR-04) |
| **never_asked** | ผล resolve เมื่อไม่เคยมี record ของ triple นี้ — `allowed:false`, ไม่ใช่ 404, ไม่ใช่ declined (BR-19) |
| **lapsed** | คำขอเกินกำหนดตอบ 30 วัน = คำขอ expired · **≠ declined** (BR-08) |
| **stale (policyStale)** | consent granted แต่ policyVersion < currentVer → ไม่ครอบคลุมเวอร์ชันปัจจุบัน (BR-06) |
| **recipient view** | หน้าจำลองเต็มจอที่เจ้าของข้อมูลเห็นเมื่อกดลิงก์ — mock ของลิงก์ภายนอก (z=--z-recipient) |
| **evidence 5** | answeredAt · requestChannel · idMethod · policyVersion · ipDevice (BR-15) |
| **CSQ (7C)** | Consequence Engine — feature ประกาศ event เท่านั้น (declare-only) · ห้ามคำนวณ/ประทับผลรายท่อ |

---

## §0.10 Pack Navigation

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW.md | All | meta + scope + roles + coverage manifest |
| 01_UI.md | FE dev | Layout Decision Log + Pages + Components + Journey |
| 02_API.md | BE dev (HTTP) | API contracts + Cross-Module Contract |
| 03_LOGIC.md | BE dev (logic) | Functions + Engines + Trace |
| 04_DB.md | DBA / BE | Tables + Fields + Classification |
| 05_RULES.md | BE + QA | Business Rules + State + Edge Cases + Errors + Security |
| 06_TESTS.md | QA | Acceptance + FN-40 negatives + Cross-Module + DoD |
| 07_LOCKED_DECISIONS.md | All | Scope Lock + LDs |
| INDEX.md | All | Cross-reference quick nav |

---

## §0.11 Scope Lock (pointer)
> FULL variant → Scope Lock อยู่ที่ **07_LOCKED §7.0** (IMMUTABLE) · Scope Lock Ref: **N/A — standalone** (plan `dep=""`, ไม่ผ่าน chain ใบเซ็นข้ามฟีเจอร์) แต่ LOCK-04/05/07 + LOCK-CSQ-01…06 สืบทอดจาก PREBRIEF Part C

---

## §0.12 Coverage Manifest (R13 — กัน requirement หล่น BRD→FRD)

### Stories (BRD §7 · FN)
| BRD Ref | Requirement (ย่อ) | อยู่ที่ใน Pack |
|---|---|---|
| US-01 / FN-01 | สร้างวัตถุประสงค์ + อัปโหลดเอกสาร v1 | 01_UI P-03+D-purCreate · 02_API-02 · 03_FN-01 · 06 AT-01 |
| US-02 / FN-02 | อัปโหลดเวอร์ชันใหม่ + เตือน stale N | 01_UI M-newVersion · 02_API-04 · 03_FN-02 · 06 AT-02 |
| US-03 / FN-03 | ตารางวัตถุประสงค์ + สถิติ | 01_UI P-03 · 02_API-01/03 · 03_FN-03 · 06 AT-03 |
| US-04 / FN-04 | ปิดวัตถุประสงค์ | 01_UI M-closePurpose · 02_API-05 · 03_FN-04 · 06 AT-04 |
| US-05 / FN-05 | สร้างคำขอ single-screen (ไม่ wizard) | 01_UI D-reqCreate · 02_API-07 · 03_FN-05 · 06 AT-05 |
| US-06 / FN-06 | ส่งคำขอทางอีเมล | 01_UI D-reqView · 02_API-09 · 03_FN-06 · 06 AT-06 |
| US-07 / FN-07 | ส่งซ้ำช่องทางอื่น = ส่งครั้งที่ N | 01_UI D-reqView · 02_API-09 · 03_FN-06 · 06 AT-07 |
| US-08 / FN-08 | คัดลอกลิงก์ / ดาวน์โหลด QR | 01_UI D-reqView · 02_API-10 · 03_FN-07 · 06 AT-08 |
| US-09 / FN-09 | ดาวน์โหลดเอกสารของคำขอ | 01_UI D-reqView · 02_API-11 · 03_FN-07 · 06 AT-09 |
| US-10 / FN-10 | เซ็นผ่าน recipient view + evidence 5 | 01_UI P-05 · 02_API-12/13 · 03_FN-08/09 · 06 AT-10 |
| US-11 / FN-11 | ยินยอมบางวัตถุประสงค์ (แยกข้อ) | 01_UI P-05 · 02_API-13 · 03_FN-09 · 06 AT-11 |
| US-12 / FN-12 | ดูหลักฐาน 1 รายการ (5 ฟิลด์) | 01_UI D-consentView · 02_API-15 · 03_FN-12 · 06 AT-12 |
| US-13 / FN-13 | ทะเบียนทั้งหมด + กรองทุกมิติ | 01_UI P-01 · 02_API-14 · 03_FN-11 · 06 AT-13 |
| US-14 / FN-14 | Customer 360 | 01_UI D-c360 · 02_API-16 · 03_FN-11 · 06 AT-14 |
| US-15 / FN-15 | ถอนแทนลูกค้า (มีผลทันที) | 01_UI M-withdraw · 02_API-17 · 03_FN-13 · 06 AT-15 |
| US-16 / FN-16 | รายการใกล้หมดอายุ ≤30 วัน | 01_UI P-01 filter · 02_API-18 · 03_FN-18 · 06 AT-16 |
| US-17 / FN-17 | ต่ออายุ = คำขอใหม่อ้างเดิม | 01_UI M-renew · 02_API-19 · 03_FN-14 · 06 AT-17 |
| US-18 / FN-18 | ประวัติ 1 รายการ (append-only) | 01_UI D-consentView · 02_API-15 · 03_FN-12 · 06 AT-18 |
| US-19 / FN-19 | ตัวจำลอง `/consent/resolve` | 01_UI P-04 · 02_API-20 · 03_ENG-01/FN-20 · 06 AT-19 |
| US-20 / FN-20 | never_asked (ไม่ใช่ 404/declined) | 01_UI P-04 · 02_API-20 · 03_ENG-01 · 06 AT-20 |

### Rules (BRD §9)
| BRD Ref | อยู่ที่ |
|---|---|
| BR-01…04 (structure/default-deny) | 05_RULES §5.1 · 04_DB triple constraint · 06 AT-05/13/19 |
| BR-05/06 (versioned upload / version-binding) | 05_RULES §5.1 · 04_DB T_consent_policy_version · 03_FN-02 · 06 AT-02 |
| BR-07/08 (5 statuses / lapsed≠declined) | 05_RULES §5.2 · 03_ENG-02 · 06 AT-20/EC |
| BR-09/10 (withdraw immediate + reason/channel) | 05_RULES §5.1 · 03_FN-13 · 06 AT-15 |
| BR-11/12/13/14 (lifespan/near-expiry/renew/close) | 05_RULES §5.1 · 03_FN-14/18 · 06 AT-16/17/04 |
| BR-15/16/17 (evidence 5 / append-only / no delete) | 05_RULES §5.1 · 04_DB T_consent_evidence/T_consent_history · 06 AT-10/18 |
| BR-18 (resend = send record) | 05_RULES §5.1 · 03_FN-06 · 06 AT-07 |
| BR-19/20 (resolve 200 always / contract lock) | 05_RULES §5.1 · 02_API-20 · 03_ENG-01 · 06 AT-19/20 |
| BR-21 (caller cache ≤5min + clear-on-withdraw) | 02_API §2.X Cross-Module · 05_RULES §5.5 EC-02 · OQ-02 |
| BR-22 (register Backend Enforcement Gate) | 02_API §2.X · 00 §0.5 · OQ-04 |
| BR-23 **[FIX-01]** answered = terminal · re-answer blocked · evidence immutable | 05_RULES §5.2 State + §5.4 · 03_LOGIC §3.1 FN-09 guard · 02_API-13 · 04_DB `answered_at` · 06 AT-21 |
| BR-24 **[FIX-03]** send snapshot เวอร์ชันนโยบาย (`vers` ต่อ purpose) + BR-06 panel เตือน stale | 02_API-09 · 04_DB T_consent_request_send.vers · 03_FN-06 · 06 AT-22 |
| BR-25 **[FIX-02]** role check ใน mutation function (ไม่ใช่แค่ render) | 05_RULES §5.3 · 03_LOGIC §3.1 (guard ทุก mutation) · 06 AT-23 · OQ-05 |
| BR-26 **[FIX-04/05]** double-submit guard (`_busy`) + sub-status guard (withdraw=granted · resend=draft/pending) — UI idempotency backstop | 05_RULES §5.4 §5.5 EC-12/13 · 02_API §2.3 · 06 AT-24/25 |
| BR-CSQ-01…05 (7C declare-only) | 03_LOGIC §3.4 + §3.1 FN-19 · 05_RULES §5.1 · CSQ_BRIEF (step 7) |

### Edges (BRD §10 confirmed ☑)
| BRD Ref | อยู่ที่ |
|---|---|
| ยินยอมบางข้อ (S-11) | 05_RULES §5.5 EC-06 · 06 AT-11 |
| ไม่ตอบ ≠ ปฏิเสธ | 05_RULES §5.5 EC-05 · 06 AT-20b |
| never_asked | 05_RULES §5.5 EC-01 · 06 AT-20 |
| version stale | 05_RULES §5.5 EC-03 · 06 AT-19c |
| ปิด purpose → consent เดิมคงอยู่ | 05_RULES §5.5 EC-07 · 06 AT-04 |

**สรุป:** Stories 20/20 ✅ · Rules 22+CSQ + BR-23..26 (BA-gate fixes) ✅ · Edges 5/5 confirmed + EC-12/13 (FIX-04/05) ✅ · ไม่มีแถวที่ "อยู่ที่" ว่าง · requirement ที่ยังต้อง BA เคาะ → OQ-01…08 + OQ-CNS-01/02/03 (ไม่หายเงียบ)
