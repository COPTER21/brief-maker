# BRD · F-BNK — Bank Master (ธนาคาร / บัญชีธนาคารบริษัท)

> Business Requirements Document — 2BSimple Core ERP · Value Stream: **Finance** · Module group: **Shared Foundation (master กลาง)**
> สร้างโดย `brd-generator-full` v2.2 (HTML-first · Fresh Mode · **Lane Mode / no-ask**)
> Source of truth (หน้าจอ): `outputs/09_Bank-Master/01_HTML/BankMaster.html` (gate PASS: qc-ux 🟢 / qc-coverage 🟡 24/25)
> Business intent: `PREBRIEF_F-BNK_BankMaster.md` + `_SEED_NOTES.md` · Locked decisions: `00_CONTEXT/DECISION_LOG.md` + `AI_DEFAULTS.md`

---

## Section 1 — Document Info

| หัวข้อ | ค่า |
|---|---|
| BRD ID | BRD-F-BNK |
| ชื่อ Feature | Bank Master — ธนาคาร / บัญชีธนาคารบริษัท |
| ประเภท BRD | **New Feature** (Master Data · Shared Foundation) |
| Module / Value Stream | Finance (การเงิน) · Core ERP |
| Version | 1.0 |
| Status | **APPROVED** (Quality Gate ผ่าน — ดู §7 / AI Review Report) |
| Owner (BA) | 2BSimple BA |
| Stakeholders | Finance Admin (ผู้ใช้หลัก), Accounting (GL owner), Policy/Security (canRevealFull tier), PM/Strike |
| วันที่ | 2026-08-06 |
| Input chain | PREBRIEF (RIF/intake) + HTML v7 (gated) + DECISION_LOG + AI_DEFAULTS + Central Plan v2 |
| Downstream | `frd-generator-v6` → UI Brief → Test Cases → QA |

### Changelog
- **v1.0 (2026-08-06):** Initial via `brd-generator-full` (Fresh Mode, HTML-first, Lane Mode).
  - Screen Inventory สกัดจาก `BankMaster.html` (source of truth · ผ่าน ux+coverage gate)
  - Scope Lock สืบทอดจาก PREBRIEF + DECISION_LOG (D1–D5) → §3.4
  - OQ-1 / OQ-2 = `[AI-DEFAULT]` → §15 Open Questions
  - W1 (custom bank hard-delete used=0) = exception to Global Contract #7 → §9 R-08
  - W2 (Payroll downstream) = ตั้งชื่อชัดใน §12.1 Downstream Impact Map → ปิด coverage WARN
  - Data classification (account number = sensitive) → §6 + §16

---

## Section 2 — Business Context

### 2.1 ปัญหา / โอกาส
องค์กรที่ใช้ Core ERP มีหลายบริษัท (multi-company) และแต่ละบริษัทมีบัญชีธนาคารหลายบัญชีสำหรับรับ-จ่ายเงิน ปัจจุบันข้อมูลธนาคารและบัญชีธนาคารกระจัดกระจาย/คีย์ซ้ำในแต่ละเอกสาร ทำให้:
- เอกสารการเงิน (ใบสำคัญจ่าย/รับ, กระทบยอด, เงินเดือน) อ้างอิงบัญชีไม่ตรงกัน / พิมพ์เลขบัญชีผิด
- ไม่มีจุดกลางผูกบัญชีธนาคารกับผังบัญชี (GL) เพื่อ posting
- เลขบัญชีธนาคาร (ข้อมูลอ่อนไหว) ถูกแสดงเต็มโดยไม่มีการควบคุมสิทธิ์/ร่องรอยการเข้าถึง

**โอกาส:** สร้าง master กลาง 2 ระดับ (รายชื่อธนาคารมาตรฐาน ธปท. + บัญชีธนาคารต่อบริษัท) เป็น golden record ให้ทุก feature การเงินดึงไปใช้เป็น picker (soft-reference) — คีย์ครั้งเดียว ใช้ได้ทั้ง value stream.

### 2.2 เป้าหมาย business
1. เป็นแหล่งข้อมูลบัญชีธนาคารเดียว (single source) ที่ Payment Voucher / Receipt Voucher / Bank Reconciliation / Payroll ดึงไปใช้
2. ควบคุมความถูกต้อง: เลขบัญชีไม่ซ้ำในบริษัทเดียวกัน, ผูก GL ครบก่อนใช้งาน, ค่าเริ่มต้นจ่าย/รับ ชัดเจน
3. ปกป้องข้อมูลอ่อนไหว: mask เลขบัญชี + เปิดดูเต็มตามสิทธิ์ + audit ทุกครั้ง
4. รักษา integrity ของเอกสารเดิม: แก้ master ไม่ย้อนเอกสารที่ออกไปแล้ว (soft-reference)

### 2.3 ตัวชี้วัดความสำเร็จ (บังคับวัดได้)

| ตัวชี้วัด | Baseline ปัจจุบัน | Target | วัดยังไง / จากไหน | วัดเมื่อไหร่ |
|---|---|---|---|---|
| M-1 · อัตราความผิดพลาดเลขบัญชีในเอกสารการเงิน | ต้องเก็บ baseline ก่อน launch (ปัจจุบันไม่มีระบบวัด) | ≤ 0.5% ของเอกสารที่อ้างบัญชี | นับ error report / correction voucher ที่มีสาเหตุ "บัญชีผิด" เทียบยอดเอกสารทั้งหมด | รายเดือน หลัง launch 3 เดือน |
| M-2 · % เอกสารการเงินที่เลือกบัญชีจาก master (ไม่คีย์เอง) | 0% (ยังไม่มี master) | ≥ 95% | log การเลือกใน picker ของ PV/RV/Recon/Payroll ÷ เอกสารทั้งหมด | รายเดือน |
| M-3 · % บัญชี active ที่ผูก GL ครบ | ต้องเก็บ baseline (ข้อมูลเดิมไม่ครบ) | 100% | query บัญชี status=active ที่ glCode ไม่ null | ณ go-live + รายไตรมาส |
| M-4 · การเข้าถึงเลขบัญชีเต็มที่ผ่านสิทธิ์ + ถูก audit | ไม่มีการควบคุม (แสดงเต็มเสมอ) | 100% ของ reveal มี audit entry | นับ reveal event ที่มี audit log คู่ (append-only) | ต่อเนื่อง (compliance) |
| M-5 · เวลาเตรียมบัญชีเริ่มต้นต่อบริษัทใหม่ | ไม่มี baseline | < 15 นาที/บริษัท | จับเวลาจาก onboarding checklist | ต่อ onboarding บริษัทใหม่ |

> ทุกตัวชี้วัดมีคู่ใน §17.3 KPI. รายการที่ยังไม่มี baseline → action: **เก็บ baseline ก่อน/ณ launch** (บันทึกใน §15 OQ-6).

### 2.4 ที่มา
- PREBRIEF §0 Obligations OB-1..OB-4 (2 ชั้น master, consumer PV/RV/Recon/Payroll, soft-reference, ผูก GL)
- Central Plan v2 §Finance box: `Bank Master → Bank Reconciliation`, `Bank Master → Payment Voucher` เป็นเส้น `[config]`
- Registry: Bank Master ระบุ "อยู่ Registry (ระบบเดิมมี)" → feature นี้ทำให้เป็น master กลางมาตรฐานของ Core ERP

---

## Section 3 — Scope

### 3.1 In Scope
1. **ระดับ 1 — รายชื่อธนาคาร (Bank):** preset มาตรฐาน ธปท. 22 ราย (BOT code / ชื่อไทย / SWIFT / ชื่อย่อ / ประเภท local|foreign) แบบ read-only + เพิ่ม/แก้/ลบ **ธนาคารที่สร้างเอง (custom)** สำหรับธนาคารต่างประเทศ/นอก preset (กรอก SWIFT เอง)
2. **ระดับ 2 — บัญชีธนาคารบริษัท (CompanyBankAccount):** ต่อ company — เลือกธนาคาร (combobox Rule #94) + เลขบัญชี + ชื่อบัญชี + ประเภท (ออมทรัพย์/กระแสรายวัน/ฝากประจำ) + สาขา + สกุลเงิน (THB) + ผูก GL (combobox จาก CoA) + ค่าเริ่มต้นจ่าย/รับ
3. **Multi-company:** สลับดูบัญชีตามบริษัท · ค่าเริ่มต้นจ่าย/รับ อย่างละ 1 ต่อบริษัท
4. **Lifecycle:** active ⇄ inactive → archived (soft archive; ไม่มี hard delete บนบัญชี)
5. **Data protection:** mask เลขบัญชี (โชว์ 4 ตัวท้าย) + "ดูเต็ม" ตามสิทธิ์ (`canRevealFull`) + audit log ทุกการ reveal
6. **Audit:** append-only ทั้ง 2 ระดับ (บัญชี + รายชื่อธนาคาร)
7. **Consumer hooks (soft-reference picker):** expose บัญชีให้ Payment Voucher, Receipt Voucher, Bank Reconciliation, Payroll (mock picker ใน prototype)
8. **Inbound:** ผูก GL account จาก Chart of Accounts (CoA)

### 3.2 Out of Scope (Scope Lock — ห้ามทำเฟสนี้)
| # | ไม่ทำ | เหตุผล / ที่มา |
|---|---|---|
| OOS-1 | **Bank API / auto statement import** (S-06) | เลื่อนเป็นเฟสถัดไป (ของ Bank Reconciliation) — PREBRIEF S-06 [มติ] |
| OOS-2 | **Multi-currency** — รองรับ **THB เท่านั้น** | OQ-2 [AI-DEFAULT] · field `currency` มีใน schema แล้วเพื่อเปิดภายหลังโดยไม่แก้ schema |
| OOS-3 | **Tier / Lite-Full linkage** — ไม่มี dual-mode 🔗/✋ | Shared-Foundation master ไม่มี tier (Central Plan §กลุ่ม module) — ห้ามประดิษฐ์ tier behavior |
| OOS-4 | PromptPay / e-payment ID บนบัญชี | ADD-1 [AI-DEFAULT] — recommended future field ตัดสินตอนทำ Payment/Receipt Voucher |
| OOS-5 | per-account purpose tag (เช่น payroll-only) | ADD-2 — over-engineer สำหรับ master เฟสนี้ |
| OOS-6 | ตาราง format เลขบัญชีต่อธนาคาร | S-04 [AI-DEFAULT] — ตรวจแค่ตัวเลข 10–15 หลักรวม ๆ |

### 3.3 Assumptions
- A-1: มี 2 บริษัทใน mock (C1, C2) — โครงสร้าง multi-company มาจาก Company Master (Shared Foundation)
- A-2: CoA (Chart of Accounts) มีอยู่แล้วเป็น master ต้นทางของ GL — Bank Master เป็นผู้บริโภค (inbound)
- A-3: ผู้ใช้เป็น Finance Admin (mock `canRevealFull=true`) — tier จริงรอ Policy (OQ-1)
- A-4: consumer เอกสาร (PV/RV/Recon/Payroll) ยังไม่พัฒนา → mock เป็น picker simulation
- A-5: บัญชีที่ inactive/archived ยังต้องแสดงในเอกสารเดิมที่อ้างถึง (soft-reference)

### 3.4 Scope Lock ⭐ (สืบทอดจาก PREBRIEF + DECISION_LOG — ห้าม override ตลอด chain)

| LOCK ID | Locked Decision | ที่มา |
|---|---|---|
| **LOCK-01** | Feature = Shared-Foundation **MASTER · NO tier / no Lite-Full linkage** — ห้ามประดิษฐ์ tier behavior | PREBRIEF · Central Plan · task |
| **LOCK-02** | **2 ระดับเท่านั้น:** รายชื่อธนาคาร (preset ธปท. 22) + บัญชีธนาคารบริษัท (ต่อ company) | OB-1 · DECISION_LOG |
| **LOCK-03** | **Downstream (config/soft-ref picker) = Payment Voucher · Receipt Voucher · Bank Reconciliation · Payroll** (Payroll ระบุชื่อชัด — ปิด W2) · **Inbound = Chart of Accounts (GL)** | OB-2 · Central Plan Finance box · task |
| **LOCK-04** | **OUT this phase:** bank API / auto statement import (S-06) · multi-currency (THB only) | PREBRIEF S-06 · OQ-2 |
| **LOCK-05** | D1: adopt `BankMaster.html` เป็น source of truth หน้าจอ (ผ่าน ux+coverage gate) — ไม่ประดิษฐ์หน้าจอเกิน/ขาด | DECISION_LOG D1 |
| **LOCK-06** | D3: coverage baseline = PREBRIEF + Central Plan edges (ไม่มี workflow_graph) · ห้ามขยาย scope นอก FN-01..06+90 / BR-01..05 / edges §9 | DECISION_LOG D3 |
| **LOCK-07** | W1: custom bank hard-delete อนุญาต **เฉพาะ used=0** — เป็น exception ที่ชัดเจนของ Global Contract #7 (ดู §9 R-08) | DECISION_LOG W1 RESOLVED |

> **SCOPE DRIFT check:** In Scope ทุกข้ออยู่ใต้ LOCK — **ไม่พบ scope creep** (ยืนยันโดย `_COVERAGE_REPORT.md`: scope creep = 0). ไม่มีข้อที่ต้อง flag SCOPE DRIFT.
> **LOCK conflict:** ไม่มี business rule ใดขัด LOCK ในเอกสารนี้.

---

## Section 4 — User Roles & Permissions

| Role | ดู list/รายละเอียด | สร้าง/แก้บัญชี | เปิด-ปิดใช้งาน / archive | เปิดดูเลขบัญชีเต็ม (canRevealFull) | จัดการรายชื่อธนาคาร custom |
|---|:--:|:--:|:--:|:--:|:--:|
| **Finance Admin** (ผู้ใช้หลัก) | ✅ | ✅ | ✅ | ✅ *(กำหนดโดยสิทธิ์ — OQ-1)* | ✅ (สร้าง/แก้/ลบ used=0) |
| **Finance User / ผู้ดูทั่วไป** | ✅ (masked) | ❌ | ❌ | ❌ (เห็นแต่ 4 ตัวท้าย) | ❌ |
| **Accounting (GL owner)** | ✅ | — (ref เท่านั้น) | ❌ | ตามสิทธิ์ | ❌ |
| **System (ระบบ)** | — | validate · audit · enforce default-unique | audit บันทึกทุก transition | บังคับ mask + log ทุก reveal | audit bank-added/removed |

> **OQ-1 [AI-DEFAULT]:** `canRevealFull` = permission ระดับ **Finance-admin** (mock: ผู้ใช้ปัจจุบันมีสิทธิ์). **tier/role จริง TBD by Policy** → §15 OQ-1.
> Master นี้ **ไม่มี tier** (LOCK-01) — สิทธิ์เป็น RBAC ปกติ ไม่ใช่ package entitlement.

---

## Section 5 — User Journey (with COSO)

> COSO roles สำหรับ **Master Data** (อ้าง `coso-defaults.md`): master maintenance ไม่ใช่เอกสารมี DOA — Maker = Finance Admin, Checker/Approver = System validation + peer review (ไม่มีสายเซ็นการเงิน), System = enforce+audit. **SoD:** การกระทำที่กระทบเงินจริง (การจ่าย/รับ) เกิดที่ **เอกสารปลายทาง (PV/RV) ซึ่งมี DOA ของตัวเอง** — Bank Master เป็น config ต้นทางเท่านั้น.

### 5.1 Happy Path — สร้างบัญชีธนาคารบริษัท (S-01)
| # | Step | Route/หน้าจอ (HTML) | Maker | Checker | Approver | System |
|---|---|---|---|---|---|---|
| 1 | เลือกบริษัท (company switcher) | `#/bank-master` แท็บ "บัญชีธนาคาร" · `changeCompany()` | Finance Admin | — | — | โหลดบัญชีของ company |
| 2 | กด "สร้างบัญชี" → เปิด drawer 680 | `headerHTML()` → create drawer | Finance Admin | — | — | เปิดฟอร์มว่าง |
| 3 | เลือกธนาคาร (combobox #94: ชื่อ/รหัส/SWIFT) | `searchSelectHTML('acc-bank')` | Finance Admin | — | — | ดึง preset ธปท. |
| 4 | กรอกเลขบัญชี (10–15 หลัก) + ชื่อบัญชี + ประเภท + สาขา | account form | Finance Admin | — | — | validate on-blur (format + duplicate) |
| 5 | ผูก GL (combobox จาก CoA) | `searchSelectHTML('acc-gl')` | Finance Admin | — | — | ดึง CoA (inbound) |
| 6 | ตั้งค่าเริ่มต้นจ่าย/รับ (optional) | `dtoggle-row` | Finance Admin | — | — | enforce unique 1/บริษัท |
| 7 | กด "ยืนยันสร้าง" | drawer footer | Finance Admin | System (validation gate) | — | commit + `pushAudit('created')` + refresh list |

### 5.2 Happy Path — เปิดดูเลขบัญชีเต็ม (reveal · FN-05)
| # | Step | Maker | System |
|---|---|---|---|
| 1 | ในหน้า list/รายละเอียด เห็นเลข masked (••••1234) | Finance Admin | mask last-4 default |
| 2 | กด "ดูเต็ม" | Finance Admin | เช็ค `canRevealFull` → ถ้ามีสิทธิ์: reveal + `pushAudit('revealed')`; ถ้าไม่มี: toast "ไม่มีสิทธิ์" (masked ค้าง) |

### 5.3 Alternative / Config Paths
- **A2 · สลับบริษัท** — ดูบัญชีคนละชุดต่อ company
- **A3 · ปิดใช้งาน (active→inactive)** — เอกสารใหม่เลือกไม่ได้, เอกสารเดิมแสดงปกติ · reversible (inactive→active)
- **A4 · เก็บถาวร (→archived)** — terminal, reactivate ไม่ได้; ใช้เมื่อบัญชีถูกใช้ในเอกสารแล้ว (ลบถาวรไม่ได้)
- **A5 · เพิ่มธนาคาร custom (S-05)** — แท็บ "ธนาคาร" → สร้างธนาคารต่างประเทศ + SWIFT (8/11)
- **A6 · ลบธนาคาร custom** — เฉพาะ `used=0` (ดู R-08); preset ธปท. ลบไม่ได้

### 5.4 Consumer Journey (mock — soft-reference picker)
เอกสารปลายทาง (PV/RV/Recon/Payroll) เปิด picker → เห็นเฉพาะบัญชี **active** ของบริษัทนั้น → เลือก → snapshot ค่าลงเอกสาร (ไม่ lookup สดย้อนหลัง).

> **HTML alignment:** ทุก step §5.1–5.3 map กับ route/ปุ่มที่มีจริงใน `BankMaster.html` (ยืนยันโดย `_COVERAGE_REPORT.md`). **ไม่พบ step ที่ไม่มีที่ยืนบนจอ.**

---

## Section 6 — Data Entity & Fields

### 6.1 Entities

**E1 · Bank (รายชื่อธนาคาร — ระดับ 1)** — lookup master
| # | Field | Label UI | Type | ค่า/ตัวเลือก | จำเป็น | หมายเหตุ |
|---|---|---|---|---|:--:|---|
| 1 | code | รหัส ธปท. | TEXT(3) | 3 หลัก | ○ (custom) / preset มี | custom เว้นได้ |
| 2 | nameTh | ชื่อธนาคาร | TEXT | | ✅ | |
| 3 | abbr | ชื่อย่อ | TEXT | uppercase | ✅ | |
| 4 | swift | SWIFT / BIC | TEXT | `^[A-Z0-9]{8}$|^[A-Z0-9]{11}$` | ✅ | 8/11 หลัก |
| 5 | type | ประเภท | DROPDOWN-SINGLE | local / foreign | ✅ | |
| 6 | color | สีแบรนด์ | DATA | hex (identity) | ○ | fallback token |
| 7 | custom | สร้างเอง? | TOGGLE(sys) | true/false | sys | preset=false read-only |
| 8 | used | จำนวนบัญชีที่อ้าง | AUTO(derived) | count | sys | คุม R-08 (delete guard) |

**E2 · CompanyBankAccount (บัญชีธนาคารบริษัท — ระดับ 2)** — master transaction
| # | Field | Label UI | Type | ค่า/ตัวเลือก | จำเป็น | หมายเหตุ |
|---|---|---|---|---|:--:|---|
| 1 | id | รหัสบัญชี | AUTO | BA-NNN | sys | running number |
| 2 | company | บริษัท | LOOKUP | Company Master | ✅ | scope key |
| 3 | bankCode | ธนาคาร | LOOKUP (#94) | Bank (E1) | ✅ | soft-ref |
| 4 | accNo | เลขที่บัญชี | TEXT (numeric) | 10–15 หลัก | ✅ | **SENSITIVE — masked** |
| 5 | accName | ชื่อบัญชี | TEXT | | ✅ | |
| 6 | acctType | ประเภทบัญชี | DROPDOWN-SINGLE | savings/current/fixed | ✅ | |
| 7 | branch | สาขา | TEXT | | ○ | |
| 8 | glCode | บัญชี GL | LOOKUP (#94) | CoA (inbound) | ✅ | posting |
| 9 | currency | สกุลเงิน | READONLY | THB | ✅ (locked) | field มีไว้เปิด multi-currency ภายหลัง (OQ-2) |
| 10 | status | สถานะ | STATE | active/inactive/archived | sys | ดู §8 |
| 11 | defaultPay | บัญชีจ่ายเริ่มต้น | TOGGLE | bool | ○ | unique 1/บริษัท (R-02) |
| 12 | defaultReceive | บัญชีรับเริ่มต้น | TOGGLE | bool | ○ | unique 1/บริษัท (R-02) |
| 13 | usedInDoc | ถูกใช้ในเอกสาร? | AUTO(flag) | bool | sys | คุม R-06 archive-lock |
| Audit | created_by/at, modified_by/at | | AUTO | | sys | audit fields |

**E3 · AuditEntry (append-only — Global Contract #7)** — 2 stream
| Field | หมายเหตุ |
|---|---|
| accountId / bankCode | key (บัญชี หรือ ธนาคาร) |
| action | created / edited / revealed / deactivated / activated / archived / default-changed / bank-added / bank-removed |
| detail, actor, timestamp | append-only (`unshift`), ไม่มี edit/delete |

> **Data Classification (สำคัญ — feeds FRD R10):** `E2.accNo` = **ข้อมูลอ่อนไหว (sensitive)**. Default **masked เหลือ 4 ตัวท้าย** ในทุก list/รายละเอียด/picker. **Full reveal ต้องผ่าน permission `canRevealFull` + เขียน append-only audit log ทุกครั้งที่ reveal.** ต้องมีชุด negative/permission test cases (ผู้ไม่มีสิทธิ์ reveal ไม่ได้ + เห็นแต่ masked). ดู §16.

### 6.2 Entity Relationship
```
Company Master ──(1:N)──▶ CompanyBankAccount (E2)
Bank (E1) ──(referenced by, soft-ref)──▶ CompanyBankAccount.bankCode   [no FK cascade]
Chart of Accounts (CoA) ──(referenced by, inbound)──▶ CompanyBankAccount.glCode
CompanyBankAccount ──(1:N append-only)──▶ AuditEntry (E3, accountId)
Bank (E1) ──(1:N append-only)──▶ AuditEntry (E3, bankCode)
CompanyBankAccount ──(picker/soft-ref)──▶ PV · RV · Bank Recon · Payroll  [snapshot on pick]
```
- FK ทั้งหมด **nullable, no cascade** (Global Contract #6 soft-reference).

---

## Section 7 — User Stories & Acceptance Criteria

**US-01** — ในฐานะ Finance Admin ฉันต้องการสร้างบัญชีธนาคารของบริษัท เพื่อให้เอกสารการเงินเลือกใช้ได้
- AC1: Given ฟอร์มบัญชี, When เลือกธนาคาร + กรอกเลข 10–15 หลัก + ผูก GL + กดยืนยัน, Then บันทึกสำเร็จ + ขึ้นในรายการทันที + audit 'created'
- AC2: Given เลขบัญชีไม่ครบ 10 หลัก / มีอักขระไม่ใช่ตัวเลข, When ยืนยัน, Then บล็อก + error inline

**US-02** — ในฐานะ Finance Admin ฉันต้องการสลับดูบัญชีตามบริษัท เพื่อจัดการแยกแต่ละนิติบุคคล
- AC1: Given มี ≥2 บริษัท, When เปลี่ยน company switcher, Then รายการแสดงเฉพาะบัญชีของบริษัทนั้น
- AC2: Given บริษัทไม่มีบัญชี, When เปิดดู, Then แสดง empty state พร้อมปุ่มสร้าง

**US-03** — ในฐานะ Finance Admin ฉันต้องการกำหนดบัญชีจ่ายเริ่มต้นและบัญชีรับเริ่มต้น เพื่อให้เอกสารเลือกให้อัตโนมัติ
- AC1: Given มีบัญชีจ่ายเริ่มต้นอยู่แล้ว, When ตั้งบัญชีอื่นเป็นจ่ายเริ่มต้น, Then ค่าเดิมถูกยกเลิกอัตโนมัติ (เหลือ 1/บริษัท)
- AC2: Given บัญชีจ่ายเริ่มต้น + รับเริ่มต้นแยกกัน, Then ทั้งสองอยู่ได้พร้อมกัน (คนละ flag)

**US-04** — ในฐานะ Finance User ฉันต้องการเห็นเลขบัญชีแบบปิดบัง เพื่อป้องกันข้อมูลอ่อนไหวรั่วไหล
- AC1: Given ไม่มีสิทธิ์ `canRevealFull`, When เปิดหน้า list, Then เห็นเฉพาะ 4 ตัวท้าย
- AC2: Given ไม่มีสิทธิ์, When กด "ดูเต็ม", Then ถูกปฏิเสธ + toast "ไม่มีสิทธิ์" (เลขยังปิดบัง)

**US-05** — ในฐานะ Finance Admin ที่มีสิทธิ์ ฉันต้องการเปิดดูเลขบัญชีเต็ม เพื่อยืนยันความถูกต้อง โดยระบบบันทึกร่องรอย
- AC1: Given มีสิทธิ์, When กด "ดูเต็ม", Then แสดงเลขเต็ม + เขียน audit 'revealed' (append-only)
- AC2: Given reveal แล้ว, Then audit entry มี actor + timestamp + accountId

**US-06** — ในฐานะ Finance Admin ฉันต้องการปิดใช้งานบัญชีที่เลิกใช้ เพื่อกันไม่ให้เอกสารใหม่เลือก
- AC1: Given บัญชี active, When ปิดใช้งาน, Then status=inactive + หายจาก picker เอกสารใหม่ + audit 'deactivated'
- AC2: Given บัญชี inactive, When เปิดใช้งาน, Then กลับเป็น active (reversible)

**US-07** — ในฐานะ Finance Admin ฉันต้องการเก็บถาวรบัญชีที่ถูกใช้แล้ว เพื่อคง integrity ของเอกสารเดิม
- AC1: Given บัญชี `usedInDoc=true`, When พยายามลบถาวร, Then ระบบไม่มีทางลบถาวร (soft archive เท่านั้น)
- AC2: Given archive แล้ว, Then status=archived (terminal, ไม่มีปุ่มเปิดใช้งาน) + audit 'archived'

**US-08** — ในฐานะ Finance Admin ฉันต้องการเพิ่มธนาคารต่างประเทศนอก preset เพื่อรองรับบัญชีสกุลพิเศษ
- AC1: Given แท็บธนาคาร, When สร้างธนาคาร + SWIFT ถูก format (8/11), Then บันทึก custom bank + audit 'bank-added'
- AC2: Given SWIFT ผิด format, When ยืนยัน, Then บล็อก + error

**US-09** — ในฐานะ Finance Admin ฉันต้องการลบธนาคาร custom ที่ไม่มีบัญชีอ้างถึง เพื่อล้างรายการที่สร้างผิด
- AC1: Given custom bank `used=0`, When ลบ, Then ลบออกจากรายการ + audit 'bank-removed'
- AC2: Given custom bank `used>0` หรือ preset ธปท., When ลบ, Then ปุ่มลบ disabled + warning (ห้ามลบ)

> **C05 check:** ไม่มี Story ที่มีคำว่า "และ" ในประโยคหลักที่ทำให้เป็นสองงาน (แต่ละ Story = 1 ความสามารถ). ✅

---

## Section 8 — Status & Lifecycle

### 8.1 State Diagram (CompanyBankAccount)
```
        [สร้าง]
           │
           ▼
        ┌────────┐   ปิดใช้งาน    ┌──────────┐
        │ active │ ─────────────▶ │ inactive │
        │        │ ◀───────────── │          │
        └────────┘   เปิดใช้งาน    └──────────┘
           │                          │
           │ เก็บถาวร (used)          │ เก็บถาวร
           ▼                          ▼
        ┌──────────────────────────────────┐
        │        archived (TERMINAL)        │  ← reactivate ไม่ได้
        └──────────────────────────────────┘
```

### 8.2 State × Trigger × Next
| Current | Trigger | Next | Guard / Rule |
|---|---|---|---|
| (none) | สร้างบัญชี | active | validate ผ่าน (R-01,R-03,R-04) |
| active | ปิดใช้งาน | inactive | หายจาก picker เอกสารใหม่ (R-05) |
| inactive | เปิดใช้งาน | active | reversible |
| active/inactive | เก็บถาวร | archived | ใช้เมื่อ used-in-doc; **terminal** |
| archived | — | — | ไม่มี transition ออก (A2: no reactivate) |

- **Bank (E1) lifecycle:** preset = คงที่ (read-only) · custom = สร้าง → (used=0 ลบได้) — ไม่มี state machine ซับซ้อน.

---

## Section 9 — Business Rules + Validation (with Change-Likelihood Tags)

| Rule | ข้อความกฎ | ประเภท | ข้อความผู้ใช้ | Tag | ใครเปลี่ยน / บ่อย / ระดับ |
|---|---|---|---|---|---|
| **R-01** | เลขบัญชี unique ต่อบริษัท (company + accNo) | Error/Prevent | "เลขบัญชีนี้มีอยู่แล้วในบริษัทนี้" | **FIXED** | — (business invariant) |
| **R-02** | บัญชีจ่ายเริ่มต้น / รับเริ่มต้น อย่างละ **1 ต่อบริษัท** | Trigger/Enforce | "ตั้งค่าได้เพียง 1 บัญชีต่อบริษัท" | **FIXED** | — |
| **R-03** | เลขบัญชี = ตัวเลข **10–15 หลัก** (ไม่มี format ต่อธนาคาร) | Error | "เลขบัญชีต้องเป็นตัวเลข 10–15 หลัก" | **CONFIGURABLE** 🤖 | Admin (นานๆครั้ง) · Admin Panel — [AI-DEFAULT] ช่วงหลักอาจปรับ (S-04) |
| **R-04** | SWIFT = **8 หรือ 11** ตัว alnum (ธนาคาร custom) | Error | "รหัส SWIFT ต้อง 8 หรือ 11 หลัก" | **FIXED** | — (มาตรฐานสากล) |
| **R-05** | บัญชี inactive/archived → หายจาก picker เอกสารใหม่ · เอกสารเดิมแสดงปกติ (soft-ref) | Prevent | — | **FIXED** | — (Global Contract #6) |
| **R-06** | บัญชีที่ถูกใช้ในเอกสาร (`usedInDoc=true`) **ลบถาวรไม่ได้** → soft archive เท่านั้น + audit | Prevent | "บัญชีนี้ถูกใช้ในเอกสาร…ลบถาวรไม่ได้ ทำได้เพียงเก็บถาวร" | **FIXED** | — (Global Contract #7) |
| **R-07** | ทุก action (create/edit/reveal/status/default/bank add-remove) เขียน **append-only audit** | System | — | **FIXED** | — (Global Contract #7) |
| **R-08** ⭐ | **ธนาคาร custom ลบถาวรได้เฉพาะ `used=0`** (ไม่มีบัญชีอ้าง `bankCode`); ถ้า used>0 หรือ preset ธปท. → บล็อก (ปุ่มลบ disabled + warning). Preset ธปท. ลบไม่ได้เสมอ | Prevent | "ลบไม่ได้ — มี N บัญชีอ้างถึงธนาคารนี้" | **FIXED (exception to Global Contract #7)** | — · **W1 RESOLVED** — exception ที่ชัดเจนของ #7 สำหรับ unused custom lookup entry |
| **R-09** | เลขบัญชี **mask เหลือ 4 ตัวท้าย** ทุกที่ default; full reveal ต้อง `canRevealFull` + audit 'revealed' | Prevent/Trigger | "คุณไม่มีสิทธิ์ดูเลขบัญชีเต็ม" | **CONFIGURABLE** 🤖 | Policy/Security กำหนด tier ที่ได้ `canRevealFull` (OQ-1) · Rule/Permission mgmt |
| **R-10** | สกุลเงิน = **THB เท่านั้น** (readonly); field `currency` มีใน schema เพื่อเปิด multi-currency ภายหลัง | Prevent | info-tip "เฟสนี้รองรับ THB เท่านั้น" | **CONFIGURABLE** 🤖 | Strike (roadmap) · toggle ภายหลัง — **ไม่ใช่ schema change** (OQ-2) |
| **R-11** | GL account (glCode) **จำเป็น** ก่อนใช้บัญชีในเอกสาร/posting | Error | "กรุณาผูกบัญชี GL" | **FIXED** | — (OB-4 posting) |
| **R-12** | Preset ธนาคาร ธปท. 22 ราย = read-only (แก้/ลบไม่ได้) · แก้ได้เฉพาะ custom | Prevent | "ธนาคารมาตรฐาน ธปท. แก้ไขไม่ได้" | **FIXED** | — |

### 9.5 สรุประดับความยืดหยุ่น (Flexibility Summary)
| Rule | ระดับ | เหตุผล | ที่มา |
|---|---|---|---|
| R-01,R-02,R-04,R-05,R-06,R-07,R-11,R-12 | **FIXED** | business invariant / Global Contract | ✅ (LOCK/Contract) |
| R-03 (ช่วงหลักเลขบัญชี) | **CONFIGURABLE — Admin Panel** | ค่าอาจปรับได้ (S-04 [AI-DEFAULT]) | 🤖 AI-inferred |
| R-08 (custom bank delete guard) | **FIXED (exception #7)** | มติ user (W1 RESOLVED) | ✅ Stakeholder (DECISION_LOG) |
| R-09 (canRevealFull tier) | **CONFIGURABLE — Permission/Policy** | tier จริงรอ Policy (OQ-1) | 🤖 AI-inferred → **§15 OQ-1** |
| R-10 (multi-currency toggle) | **CONFIGURABLE — roadmap toggle** | เปิดภายหลังไม่แก้ schema (OQ-2) | 🤖 AI-inferred → **§15 OQ-2** |

> **Escalation (C23):** 🤖 R-09 และ R-10 เป็น policy/roadmap-level → ยกเข้า §15 Open Questions ให้ stakeholder ยืนยันก่อนพัฒนา. R-03 (Admin Panel level) mark 🤖 ปล่อยผ่านได้แต่บันทึกไว้.

---

## Section 10 — Edge Cases

### 10.1 Edge Cases ที่ RIF/BA ระบุ (default ☑)
- ☑ EC-01: เลขบัญชีซ้ำในบริษัทเดียว → บล็อก (R-01)
- ☑ EC-02: เลขบัญชีไม่ครบ 10–15 หลัก / มีตัวอักษร → บล็อก + strip non-digit (R-03)
- ☑ EC-03: ตั้งบัญชีจ่ายเริ่มต้นซ้อน → ย้ายค่าเริ่มต้นอัตโนมัติ (R-02)
- ☑ EC-04: บัญชี inactive → หายจาก picker เอกสารใหม่ / เอกสารเดิมยังโชว์ (R-05)
- ☑ EC-05: reveal โดยไม่มีสิทธิ์ → ถูกปฏิเสธ, masked ค้าง (R-09)
- ☑ EC-06: ลบบัญชีที่ใช้แล้ว → ทำไม่ได้ → เก็บถาวรแทน (R-06)
- ☑ EC-07: SWIFT ผิด format (ไม่ใช่ 8/11) → บล็อก (R-04)
- ☑ EC-08: ลบธนาคาร custom ที่ used>0 → บล็อก + ปุ่ม disabled (R-08)
- ☑ EC-09: archived แล้วพยายาม reactivate → ไม่มี path (terminal, A2)

### 10.2 Edge Cases จาก AI Pattern Matching (☐ = แนะนำ — BA confirm ที่ SOW3.7)
**DI · Lookup Master Data:**
- ☐ EC-10: ธนาคารที่เลือกถูกลบ/archive หลังบัญชีสร้างแล้ว → บัญชีเดิมยังอ้างชื่อ snapshot ได้ (soft-ref — no cascade)
- ☐ EC-11: CoA (GL) ที่ผูกไว้ถูกปิดใน CoA master → บัญชียังชี้ code เดิม; แจ้งเตือนตอนใช้ใน posting (ยกเป็น FRD note)

**CA · Concurrent Access:**
- ☐ EC-12: 2 ผู้ใช้ตั้งบัญชีจ่ายเริ่มต้นคนละบัญชีพร้อมกัน → last-write-wins + audit ทั้งคู่ (ต้อง confirm พฤติกรรม)

**PM · Permission:**
- ☐ EC-13: ผู้ใช้ที่ไม่มีสิทธิ์แก้ไข เข้าถึง URL/drawer ตรง ๆ → ต้องกันที่ backend ไม่ใช่แค่ซ่อนปุ่ม *(กระทบสิทธิ์ — ยก OQ ทันที: §15 OQ-4)*

**ST · Status/Workflow:**
- ☑ EC-14: บัญชีจ่าย/รับเริ่มต้นถูก deactivate/archive → **warn + clear** (เตือนใน confirm modal ว่าค่าเริ่มต้นจะถูกยกเลิก + เคลียร์ default flag) — **RESOLVED 2026-08-06** (OQ-5 ปิดแล้ว)

**DATA (sensitive):**
- ☐ EC-15: export/print รายการบัญชี → ต้อง mask เลขบัญชีเสมอ (เว้นผู้มีสิทธิ์ + audit) *(กระทบข้อมูลอ่อนไหว — ยก OQ: §15 OQ-3)*

---

## Section 11 — Impact / Regression
- **New Feature** → ไม่มี regression ของฟีเจอร์เดิม (Bank Master เดิมอยู่ Registry แต่ทำใหม่เป็น master กลาง)
- Impact ต่อ downstream = ดู §12.1 (Value Stream). ไม่มี migration schema (feature ใหม่)
- **Data migration note:** ถ้ามีบัญชีธนาคารเดิมใน Registry → ต้องมี migration + backfill glCode (ยกเป็น §15 OQ-6 baseline/migration).

---

## Section 12.1 — Value Stream & Downstream Impact ⭐

### 12.1.1 Positioning
Bank Master อยู่ใน **Value Stream: Finance** กลุ่ม **Shared Foundation master** (Central Plan v2 §Finance box). เป็น **config master** (`[config]`) — ป้อนข้อมูลบัญชีให้เอกสารการเงินดึงเป็น picker (soft-reference, snapshot on pick).

### 12.1.2 Upstream (รับข้อมูล/trigger จาก)
| ต้นทาง | ข้อมูลที่รับ | ทิศ |
|---|---|---|
| **Chart of Accounts (CoA / Accounting)** | GL account code สำหรับผูกบัญชี (posting) | inbound `[config]` (PULL ตอนสร้างบัญชี) |
| **Company Master (Shared Foundation)** | รายการบริษัท (scope key) | inbound |

### 12.1.3 Downstream Impact Map (ทุกแถวตอบ "แล้วไงต่อ")
| ปลายทาง | ข้อมูลที่ไหลไป | Trigger | ถ้าบัญชีถูกปิด/เก็บถาวร/แก้ |
|---|---|---|---|
| **Payment Voucher** (จ่ายจากบัญชีธนาคาร) | บัญชี + GL (จ่าย) — snapshot | เลือกใน picker ตอนสร้าง PV | บัญชี inactive → หายจาก picker ใหม่ · PV เดิมยัง snapshot ค่าเดิม (soft-ref) |
| **Receipt Voucher** (รับเข้าบัญชี) | บัญชีรับเริ่มต้น + GL — snapshot | เลือก/auto-default ตอนสร้าง RV | เหมือน PV · default-receive ช่วย pre-select |
| **Bank Reconciliation** (กระทบยอด) | บัญชี + เลขบัญชี + GL | ตั้งงวดกระทบยอดต่อบัญชี | บัญชี archived ต้องคงประวัติ recon เดิม (no cascade) |
| **Payroll** ⭐ (บัญชีจ่ายเงินเดือน) | บัญชีจ่าย + GL "เงินฝากธนาคาร - บัญชีเงินเดือน" (1010-06) | รอบจ่ายเงินเดือนเลือกบัญชีจ่าย | บัญชีจ่ายเงินเดือน inactive → รอบใหม่เลือกไม่ได้; รอบเดิม snapshot ไว้ · **Payroll = named downstream consumer (ปิด coverage W2)** |

### 12.1.4 ผลกระทบแนวขวาง
- **บัญชี/GL:** ทุกบัญชีผูก GL → posting ของ PV/RV/Payroll ผ่าน GL Posting Group (Bank Master ไม่ post เอง — เป็น config)
- **รายงาน:** รายการบัญชีธนาคารต่อบริษัท feed dashboard การเงิน (§18)
- **สต๊อก/งบประมาณ:** ไม่กระทบ (master การเงิน ไม่ผูก inventory/budget)

> **C21 check:** upstream + downstream ครบ ทุกแถวตอบ "แล้วไงต่อ" ✅ · Payroll ระบุชื่อชัด (W2 ปิด).

---

## Section 12.3 — Existing System Reference
| Rule/ความสามารถ | ระดับ | มีอยู่แล้ว? | Reference |
|---|---|:--:|---|
| R-03 ช่วงหลักเลขบัญชี | Admin Panel (config) | ❌ | ต้องสร้าง config entry (ไม่ hardcode) |
| R-09 canRevealFull permission | Permission/Policy | ⚠️ บางส่วน | มี RBAC/Registry Audit กลาง แต่ tier `canRevealFull` ยังไม่กำหนด (OQ-1) |
| R-07 append-only audit | Platform | ✅ | Audit Trail กลาง (Central Plan Registry — append-only) |
| GL binding (CoA) | Master | ✅ | Chart of Accounts (Accounting) มีอยู่ |
| Company scope | Master | ✅ | Company Master (Shared Foundation) |

> ⚠️ ไม่มี System Module Registry ฉบับเต็มในสายนี้ (D3) — mapping ข้างต้นอ้าง Central Plan §Registry. รายการ ⚠️/❌ ยืนยันภายหลังกับ Registry จริง.

---

## Section 13 — Delivery Phases
**Phase 1 · Feature Launch (must):**
- Entities E1/E2/E3 + seed preset ธปท. 22 · state machine active/inactive/archived · validation R-01..R-08,R-11,R-12 เป็น config/rule table (ห้าม hardcode) · masking + reveal-audit (R-09 mechanism) · picker hooks (mock) · audit append-only 2 stream · reuse: Company Master, CoA, Audit Trail กลาง

**Phase 2 · Admin Panel:**
- R-03 (ช่วงหลักเลขบัญชี) เป็น config ปรับได้ · (ถ้าต้องการ) จัดการ preset ธนาคารผ่าน admin

**Phase 3 · Rule / Permission Management:**
- R-09 tier `canRevealFull` ผูกกับ Policy/Permission engine (หลัง Policy เคาะ OQ-1)

**Phase 4 · Engine / Roadmap:**
- R-10 เปิด multi-currency toggle (OQ-2) · เชื่อม bank API / auto statement import (S-06 — เฟส Bank Reconciliation)

---

## Section 14 — Dev Requirements Summary ("ใบสั่ง")

### 14.1 Config Foundation ที่ต้องเตรียม
- Bank preset seed (ธปท. 22) เป็น data table read-only + flag custom · CoA lookup (inbound) · Company scope · Audit Trail กลาง (append-only, 2 key: accountId / bankCode)
- Config entry: `accNo_length_range` (default 10–15) — R-03 ไม่ hardcode

### 14.2 ข้อกำหนดจาก Tag (rule ที่ไม่ FIXED)
- **R-03 (CONFIGURABLE/Admin Panel):** ช่วงหลักเลขบัญชีอ่านจาก config ไม่ hardcode `{10,15}`
- **R-09 (CONFIGURABLE/Permission):** `canRevealFull` = permission check (ไม่ hardcode true) — mock = true ต้องเปลี่ยนเป็น RBAC จริงเมื่อ Policy เคาะ · **backend ต้องบังคับ** (ไม่ใช่แค่ซ่อนปุ่ม)
- **R-10 (CONFIGURABLE/toggle):** field `currency` เก็บ THB แต่ schema รองรับค่าอื่น — เปิดด้วย feature toggle ภายหลัง **ไม่แก้ schema**
- FIXED rules (R-01,R-02,R-04..R-08,R-11,R-12): ใช้ Global Contract/rule table ที่มี — ไม่สร้าง config UI

### 14.3 ข้อกำหนดจาก Edge/Validation (Dev handle พิเศษ)
- **Sensitive data (R-09):** mask เลขบัญชีที่ **ทุก surface รวม export/print** (EC-15) · reveal เขียน audit ทุกครั้ง (accountId+actor+timestamp) — append-only, ห้าม update/delete
- **R-08 delete guard:** เช็ค `used` count (นับบัญชีที่อ้าง bankCode) ก่อนลบ custom bank; preset ลบไม่ได้เสมอ
- **default-unique (R-02):** enforce ที่ transaction/DB ระดับบริษัท (กัน concurrent EC-12)

### 14.4 WARNING ที่รอข้อสรุป (ห้ามพัฒนาส่วนที่เกี่ยวจนกว่า resolve)
- **OQ-1** tier ที่ได้ `canRevealFull` → รอ Policy/Strike (กระทบ R-09 permission binding, Phase 3)
- **OQ-3/OQ-4** (export mask / backend permission gate) → confirm ก่อน implement ส่วนที่กระทบ
- **OQ-5** (default-account-on-deactivate) → **RESOLVED 2026-08-06: warn + clear** (เตือนใน confirm modal + เคลียร์ default flag) — implement ได้เลย

### 14.5 Regression Scope — ไม่มี (New Feature)

### 14.6 Screen Inventory + UI Signals

**Screen Inventory** (สกัดจาก `BankMaster.html` — single-file SPA, route `#/bank-master`; หน้าเชิง business = 2 แท็บ + drawers/modals ในหน้าเดียว):

| # | ชื่อหน้า/มุมมอง | route/anchor (HTML) | ประเภทหยาบ | ผู้ใช้หลัก | หน้าที่ (business) | หมายเหตุ |
|---|---|---|---|---|---|---|
| P-01 | แท็บ "บัญชีธนาคาร" (list) | `#/bank-master` · `state.tab='accounts'` | หน้ารายการ | Finance Admin/User | company switcher + filter status + stat row + ตารางบัญชี (masked) + row actions | mask last-4 + "ดูเต็ม" |
| P-02 | แท็บ "ธนาคาร" (preset list) | `state.tab='banks'` · `banksTabHTML()` | หน้ารายการ | Finance Admin | รายชื่อธนาคาร ธปท. 22 (read-only) + CRUD custom + section ประวัติการเปลี่ยนแปลงธนาคาร | preset ลบ/แก้ไม่ได้ |
| P-03 | Drawer สร้าง/แก้บัญชี | `renderDrawerEl()` mode account · 680 | ฟอร์มสร้าง/แก้ (ขั้นเดียว) | Finance Admin | กรอกบัญชี + combobox ธนาคาร/GL (#94) + default toggle | currency readonly (THB) |
| P-04 | Drawer ดูรายละเอียดบัญชี | view mode · 680 | หน้ารายละเอียด | Finance Admin | ดูข้อมูล + แท็บ "ประวัติ" (audit) + toggle default/status + reveal | reveal-on-permission |
| P-05 | Drawer สร้าง/แก้ธนาคาร custom | `bankFormHTML()` · 680 | ฟอร์มสร้าง/แก้ | Finance Admin | ชื่อ/ชื่อย่อ/รหัส ธปท./SWIFT/ประเภท | SWIFT 8/11 |
| M-01 | Modal ยืนยันเก็บถาวร | `archiveModalHTML()` · 440 | หน้ายืนยัน | Finance Admin | confirm archive (used-in-doc note) | destructive confirm |
| M-02 | Modal ยืนยันปิดใช้งาน | `deactivateModalHTML()` · 440 | หน้ายืนยัน | Finance Admin | confirm deactivate | reversible |
| M-03 | Doc picker (จำลอง) | `docPickerHTML()` | หน้ายืนยัน (mock) | consumer เอกสาร | จำลองเลือกบัญชีในเอกสาร (PV ฯลฯ) | simulation ตั้งใจ (I-05) |

- **สรุปจำนวนหน้า:** ~2 หน้าหลัก (2 แท็บในหนึ่ง route) + 3 drawer + 3 modal/picker = โครง master 2 ระดับในไฟล์เดียว.
- **HTML-RIF drift:** **ไม่พบ** — ทุกหน้าใน inventory ตรงกับ FN/BR ที่ RIF ขอ (ยืนยัน `_COVERAGE_REPORT.md` 24/25, scope creep 0). Payroll เป็น concept downstream (ไม่มีหน้าจอของตัวเองใน master นี้ — ถูกต้อง).

**UI Signals ส่งต่อ FRD (signal ไม่ใช่ spec):**
- ไม่ใช่เอกสารธุรกรรม A4 (master) → **ไม่มี print/PDF/ลายเซ็น** (D2: thai-doc-pdf-generator SKIP)
- มี combobox master (Rule #94) 2 จุด: ธนาคาร + GL → FRD ยึด pattern #94
- มี **sensitive field masking + reveal-on-permission** → FRD R10 Data Classification + permission test cases (บังคับ)
- ไม่มี NON-STANDARD / keep-original-UI flag
- drawer 680 + modal 440 + page-tabs (`.ptabs` custom — v7 base-kit ไม่มี page-tab กลาง; flag ไป FRD/catalog ตาม I-03)

---

## Section 15 — Open Questions

| # | คำถาม | สถานะ | ค่า default ที่ใช้ระหว่างรอ ([AI-DEFAULT]) | เจ้าภาพ |
|---|---|:--:|---|---|
| **OQ-1** | role/tier ใดได้ `canRevealFull` (เปิดดูเลขบัญชีเต็ม) | ⚠️ รอ | Finance-admin-level permission; mock `canRevealFull=true` · reveal ทุกครั้ง audit | Policy / Strike |
| **OQ-2** | รองรับ multi-currency เมื่อไหร่ | ⚠️ รอ | THB locked เฟสนี้; field `currency` มีใน schema → เปิดภายหลัง = toggle ไม่ใช่ schema change | Strike (roadmap) |
| **OQ-3** | export/print รายการบัญชีต้อง mask เลขบัญชีไหม (sensitive) | ⚠️ รอ | mask เสมอ เว้นผู้มีสิทธิ์ + audit (EC-15) | Policy / BA (SOW3.7) |
| **OQ-4** | backend ต้องบังคับ permission gate (ไม่ใช่แค่ซ่อนปุ่ม) | ⚠️ รอ | บังคับที่ backend (EC-13) | Tech Lead |
| **OQ-5** | ถ้าบัญชีจ่าย/รับเริ่มต้นถูก deactivate ต้อง clear flag หรือเตือน? | ✅ RESOLVED 2026-08-06 | **warn + clear** — confirm modal เตือนว่าค่าเริ่มต้นจะถูกยกเลิก + เคลียร์ default flag (EC-14) | BA / Finance |
| **OQ-6** | baseline ตัวชี้วัด (M-1,M-3,M-5) + migration บัญชีเดิมจาก Registry | ⚠️ รอ | เก็บ baseline ก่อน/ณ launch; ทำ migration + backfill glCode | PM / BA |

> ทุก OQ propagate ด้วย tag `[AI-DEFAULT]` ตลอด chain (BRD/FRD/TC/QA) ตาม DECISION_LOG D4.

---

## Section 16 — Security & Compliance

### 16.1 Preset ที่เลือก + เหตุผล
- **P3 · Master Data (baseline, 10 controls)** — feature เป็น master lookup/config
- **Augmented ด้วย field-level protection (ยืมจาก P4/P6):** เพราะ `accNo` = **sensitive financial data** → เพิ่ม controls: field masking, reveal-on-permission, reveal audit logging
- เหตุผลที่ไม่ยก P4 เต็ม: Bank Master ไม่ทำธุรกรรมเงิน/posting เอง (นั่นคือ PV/RV/Payroll) — เป็น config ต้นทาง; แต่ข้อมูลอ่อนไหวจึงต้องเสริม controls เฉพาะจุด.

### 16.2 Applicable Standards (สรุป)
| มาตรฐาน | ใช้ | หมายเหตุ |
|---|:--:|---|
| Access Control (RBAC) | ✅ | canRevealFull + edit permission |
| Audit Trail (append-only) | ✅ | Global Contract #7 |
| Data Masking / PII-like protection | ✅ | accNo last-4 |
| Data Integrity (soft-ref, no cascade) | ✅ | Global Contract #6 |
| Input Validation | ✅ | R-01,R-03,R-04 |
| Non-repudiation | ✅ | reveal audit (actor+timestamp) |
| Encryption at rest (accNo) | ○ | แนะนำ (FRD/infra) |
| Segregation of Duties | ✅ | การจ่ายจริงเกิดที่ PV (มี DOA) — master เป็น config |

### 16.3 Control Checklist (สำคัญ)
| Control | Required | Implementation Note |
|---|:--:|---|
| C-ACC-01 · RBAC edit/view | ✓ Must | Finance Admin แก้ได้; user ดู masked |
| C-SEN-01 · Field masking (accNo last-4) | ✓ Must | ทุก surface รวม export (OQ-3) |
| C-SEN-02 · Reveal gated by `canRevealFull` | ✓ Must | backend enforce (OQ-4) |
| C-AUD-01 · Append-only audit ทุก action + reveal | ✓ Must | 2 stream (accountId/bankCode); no update/delete |
| C-INT-01 · No hard delete (soft archive) | ✓ Must | account เท่านั้น; custom bank exception used=0 (R-08) |
| C-VAL-01 · Server-side validation | ✓ Must | R-01,R-03,R-04,R-11 |
| C-ENC-01 · Encrypt accNo at rest | ○ Optional | แนะนำ (infra) |

### 16.4 Risk Statement
| Rule/จุด | Risk | Mitigated by |
|---|---|---|
| R-09 accNo | เลขบัญชีรั่วไหล / เข้าถึงโดยไม่มีสิทธิ์ | C-SEN-01, C-SEN-02, C-AUD-01 |
| R-06/R-08 delete | ลบบัญชี/ธนาคารที่ถูกอ้าง → เอกสารเดิมพัง | C-INT-01, R-08 guard (used=0) |
| R-01/R-11 | บัญชีซ้ำ/ไม่ผูก GL → posting ผิด | C-VAL-01 |
| R-02 default | บัญชีจ่าย/รับ ชนกัน → เอกสารเลือกผิด | enforce-unique + audit |

---

## Section 17 — Health Check

### 17.1 SLA
| Action | เป้าเวลา | Owner |
|---|---|---|
| สร้าง/แก้บัญชี (save) | < 2 วินาที | System |
| reveal เลขบัญชีเต็ม (+audit write) | < 1 วินาที + audit ต้องสำเร็จ 100% | System |
| เตรียมบัญชีเริ่มต้นต่อบริษัทใหม่ | < 15 นาที (M-5) | Finance Admin |

### 17.2 Control Points (map จาก §16)
- CP-1: ทุก reveal → มี audit entry (C-AUD-01) · CP-2: ทุก save → validation pass (C-VAL-01) · CP-3: ทุก delete attempt → guard check (C-INT-01/R-08)

### 17.3 KPI (คู่กับ §2.3)
| KPI | ประเภท | Target | คู่ metric |
|---|---|---|---|
| K-1 error เลขบัญชีในเอกสาร | Quality | ≤0.5% | M-1 |
| K-2 % เอกสารเลือกจาก master | Conversion/Adoption | ≥95% | M-2 |
| K-3 % active ผูก GL ครบ | Compliance | 100% | M-3 |
| K-4 reveal ที่มี audit | Compliance | 100% | M-4 |
| K-5 จำนวนบัญชี active ต่อบริษัท | Volume | — (monitor) | ops |

### 17.4 Threshold
| ตัวชี้วัด | Min | Max | Action เมื่อเกิน |
|---|---|---|---|
| reveal ต่อผู้ใช้ต่อวัน | — | > 50 | Anomaly alert (อาจ scraping) |
| audit write fail | 0 | > 0 | Block reveal + แจ้ง admin |
| บัญชี active ไม่ผูก GL | 0 | > 0 | แจ้งเตือน compliance |

### 17.5 Throughput
- Capacity: ~10s–100s บัญชีต่อ tenant (multi-company) · Baseline: 5 บัญชี/2 บริษัท (mock) · Stress: list rendering + masking ที่ >200 บัญชี → พิจารณา pagination/sticky (NC/I-04).

---

## Section 18 — Monitoring

### 18.1 Reports Overview
- **Performance:** เวลา save/reveal · **Closing:** สรุปบัญชี active ต่อบริษัท ต่อรอบปิดงวด · **Anomaly:** reveal ผิดปกติ / audit fail · **Transaction:** audit trail (create/edit/reveal/status/bank changes)

### 18.2 Dashboard Widgets (อ้าง §17)
- W-1: จำนวนบัญชี active/inactive/archived ต่อบริษัท (K-5) · W-2: % ผูก GL ครบ (K-3) · W-3: reveal count + audit coverage (K-4) · W-4: บัญชีไม่มี default จ่าย/รับ (ops)

### 18.3 Performance Report — response time save/reveal เทียบ SLA §17.1
### 18.4 Closing Report — snapshot บัญชีต่อบริษัท ณ ปิดงวด (feed Bank Reconciliation)
### 18.5 Anomaly Report — reveal > threshold, audit write fail, active-ไม่ผูก-GL
### 18.6 Transaction Report — append-only audit trail (2 stream) เรียงเวลา

### 6.5 Cross-Section Coverage Check
- BC (§9 R-01..R-12) ↔ Edge Cases (§10 EC-01..EC-15) — ครบ ✅
- Control (§16) ↔ Control Point (§17.2) — ครบ ✅
- Metric (§2.3 / §17.3 KPI) ↔ Widget/Report (§18) — ครบ ✅

---

## Section 7 (Quality) — AI Review Report

```
═══════════════════════════════════════
AI REVIEW REPORT — BRD Generator Full (v2.2)
═══════════════════════════════════════
BRD: BRD-F-BNK — Bank Master
ประเภท: New Feature (Master · Shared Foundation)
Mode: Fresh / HTML-first / Lane Mode (no-ask)
วันที่ตรวจ: 2026-08-06

CHECKLIST RESULTS (C01–C23 + PE01–PE05):
───────────────────────────────────────
✅ C01 Business Objective วัดผลได้ (§2.3 มีตัวเลข/แหล่งวัด)
✅ C02 User Roles ครบ (§4) — ไม่มี tier (LOCK-01 ถูกต้อง)
✅ C03 Scope In/Out + Assumptions (§3)
✅ C04 Journey ครบ happy+alt (§5)
✅ C05 Story ไม่มีคำ "และ" ที่ทำให้เป็นสองงาน
✅ C06 AC ≥2 ต่อ Story
✅ C07 State machine + terminal archived (§8)
✅ C08 Data entity + ER + audit fields (§6)
✅ C09 Snapshot/soft-ref สะท้อน (§6.2, R-05)
✅ C10 ทุก rule ที่มีตัวเลข/เงื่อนไข ติด Tag (§9)
✅ C11 Flexibility summary + ที่มา (§9.5)
✅ C12 Data-entity/validation align กับ edge cases
✅ C13 Edge Cases ครบหมวด (DI/CA/PM/ST/DATA) (§10)
✅ C14 Existing System ref (§12.3) + warn ไม่มี Registry เต็ม
✅ C15 Delivery Phases 1–4 (§13)
✅ C16 Security preset + controls (§16)
✅ C17 Health/Monitoring (§17–18)
✅ C18 WARNING ทุกข้อมีแผน/เจ้าภาพ (§14.4/§15)
✅ C19 Dev Summary "ใบสั่ง" ครบ (§14)
✅ C20 Scope Lock §3.4 ครบจาก PREBRIEF/DECISION_LOG · SCOPE DRIFT = 0
✅ C21 Value Stream §12.1 upstream + downstream map ตอบ "แล้วไงต่อ" ทุกแถว (Payroll ระบุชื่อ → W2 ปิด)
✅ C22 ตัวชี้วัด §2.3 มี baseline/target/วิธีวัด + คู่ใน §17.3 (baseline ที่ขาด → action OQ-6)
✅ C23 §9.5 marker 🤖/✅ ครบ — 🤖 R-09/R-10 (policy/roadmap) ยกเข้า §15 OQ
✅ PE01 COSO roles ทุก step §5 (master maintenance — coso-defaults)
✅ PE02 SoD — การจ่ายจริงเกิดที่ PV (มี DOA); master เป็น config → ผ่าน
✅ PE03 Security preset (P3 + sensitive augmentation) + controls ครบ
✅ PE04 SLA+KPI+Threshold §17 ครบ
✅ PE05 Cross-section coverage (§6.5) ผ่าน

Scope/LOCK compliance:
- LOCK-01..07 honored · no tier invented · THB locked · S-06 out
- W1 → R-08 exception to Contract #7 (used=0) documented
- W2 → Payroll named downstream (§12.1) — coverage WARN closed
- OQ-1/OQ-2/OQ-3-6 = [AI-DEFAULT], escalated §15
- Data classification (accNo sensitive) → §6 + §16 + FRD R10 handoff

SUMMARY:
ผ่าน: 28/28 (C01–C23 + PE01–PE05)
ไม่ผ่าน: 0
สถานะ: ✅ APPROVED — พร้อมเข้า frd-generator-v6

หมายเหตุ: OQ ที่เปิดอยู่เป็น policy/roadmap-level (ไม่บล็อก BRD) —
Dev ต้องไม่ implement R-09 tier binding / R-10 toggle จนกว่า OQ-1/OQ-2 resolve.
```

**สถานะเอกสาร: ✅ APPROVED**

---

*จบ BRD-F-BNK v1.0 — สร้างโดย brd-generator-full v2.2 (Lane Mode). Downstream: frd-generator-v6 (ยึด BRD นี้ + HTML source of truth + Security Bible).*
