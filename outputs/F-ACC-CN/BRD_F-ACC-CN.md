# BRD — Credit Note (ใบลดหนี้ลูกค้า) · F-ACC-CN / F096

> Business Requirements Document · **Fresh Mode (HTML-first)** · WF-01 SOW3.2
> Source of truth: `outputs/F-ACC-CN/F-ACC-CN_credit-note.html` (FINAL — ผ่าน ux gate + coverage gate R1)
> ร่วมกับ: `RIF_v2_F-ACC-CN.md` · `PREBRIEF_F-ACC-CN.md` · `FUNCTION_CHECKLIST_F-ACC-CN.md` (22 FN) · `DECLARATION_INDEX.md`

---

## 1. Document Info

| | |
|---|---|
| **BRD ID** | BRD-F-ACC-CN |
| **Feature** | Credit Note — ใบลดหนี้ลูกค้า (F-ACC-CN · F096) |
| **ประเภท** | New Feature |
| **Module** | Accounting / Accounts Receivable (AR) · Wave W5 Phase A (LITE) |
| **Version** | v1.0 |
| **Status** | APPROVED (Quality Gate ผ่าน — ดู §19 AI Review) |
| **Owner** | BA (WF-01) |
| **Stakeholders** | Strike (Policy/OQ owner) · Finance/บัญชี · Policy Center (DOA) · Dev · QA |
| **วันที่** | 2026-09-22 |
| **Conflict priority** | LOCK-XX > RIF (business intent) > HTML (หน้าจอจริง) |

### 1.1 Changelog
- **v1.0 (2026-09-22)** — Initial BRD ผ่าน brd-generator-full (Fresh Mode, HTML-first). สกัด Screen Inventory + Journey + Rules จาก HTML FINAL (`F-ACC-CN_credit-note.html`) เติม business intent จาก RIF v2 + PREBRIEF. บันทึกมติ BA 2026-09-22: end-bill discount IN scope (FN-19/BR-11/BR-12) และ **OQ-b RESOLVED — DOA tier คิดจากยอดสุทธิหลังหักส่วนลดท้ายบิล**.

---

## 2. Business Context

### 2.1 ปัญหา / โอกาส
- **PAIN-01** ปัจจุบันลดหนี้โดยแก้ยอดในใบแจ้งหนี้เดิม → ผิดหลักภาษี (ต้องออกใบลดหนี้อ้างใบกำกับเดิมตาม ม.86/10)
- **PAIN-02** ลดเกินยอดคงค้าง / ลดซ้ำบนใบเดียวกันโดยไม่มีตัวคุม
- **PAIN-03** ไม่มีสายอนุมัติตามมูลค่า — อนุมัติทางแชท ไม่มีร่องรอย

### 2.2 เป้าหมาย business
- **GOAL-01** ออกใบลดหนี้อ้างใบแจ้งหนี้ให้ถูกต้องตามกฎหมายภาษี (ม.86/10, ม.82/10)
- **GOAL-02** คุมยอดลดไม่ให้เกินยอดคงเหลือของใบอ้างอิง
- **GOAL-03** อนุมัติตามมูลค่าผ่าน DOA (3 tier) + เก็บ audit ครบ

### 2.3 ตัวชี้วัดความสำเร็จ (วัดได้)

| ตัวชี้วัด | Baseline ปัจจุบัน | Target | วัดยังไง/จากไหน | วัดเมื่อไหร่ | คู่ §17.3 |
|---|---|---|---|---|---|
| CN ที่ยอดเกินยอดคงเหลือใบอ้างอิง | ต้องเก็บ baseline ก่อน launch (เดิมไม่มีระบบคุม) | 0 ใบ | DB: นับ CN ที่ grand > outstanding ณ อนุมัติ | รายเดือน | KPI-Q1 |
| เวลาอนุมัติเฉลี่ย (ส่ง→อนุมัติครบ) | ต้องเก็บ baseline (เดิมอนุมัติทางแชท) | ≤ 1 วันทำการ | timestamp submittedAt → approved_at | รายเดือน | KPI-S1 |
| CN ที่ไม่มีเหตุผล/ไม่อ้างใบ | ต้องเก็บ baseline | 0 ใบ | DB: reason IS NULL หรือ inv IS NULL (ระบบบังคับ) | รายเดือน | KPI-C1 |
| ปริมาณงาน | ~120 ใบ/เดือน (ประมาณการ RIF §12) | รองรับได้ | นับ CN/เดือน | รายเดือน | KPI-V1 |

### 2.4 ที่มา
CONTEXT_PACK W5-LITE §2.2/§3 (OQ-CN-01) · workflow_graph edge `F-ACC-ARINV → F-ACC-CN` · BRD_F-ACC-ARINV §12.1 (contract `ar_open_item`) · FEATURE_LIST F096/F090.

---

## 3. Scope

### 3.1 In Scope
1. สร้าง/แก้ร่าง/ส่งอนุมัติ/อนุมัติ/ไม่อนุมัติ/ส่งลูกค้า/ยกเลิก ใบลดหนี้ **ที่อ้างใบแจ้งหนี้เสมอ**
2. เหตุผลการลดหนี้จาก master (รับคืนสินค้า / ส่วนลดภายหลัง / คิดราคาสูงเกิน / คิดจำนวนเกิน) — แต่ละเหตุผลมี `legal_basis`
3. Line editor ล็อกสินค้าจากใบเดิม — ลดจำนวน (RET/QTY) หรือ ลดราคาต่อหน่วย (DISC/PRICE)
4. **ส่วนลดท้ายบิล (end-bill discount)** — ฿/% · จำกัดยอดสุทธิ ≥0 และ ≤ ยอดคงค้าง · ลดฐานภาษี → คำนวณ VAT ใหม่ (FN-19 · BR-11 · BR-12 · มติ BA 2026-09-22)
5. อนุมัติตามมูลค่าผ่าน DOA 3-tier (slot picker เลือกคนต่อขั้น) — **tier คิดจากยอดสุทธิหลังหักส่วนลดท้ายบิล**
6. ออกเลข `CN-YYYY-NNNN` เมื่ออนุมัติครบ (doccfg) · ลดยอดคงค้าง AR · ลดภาษีขายเดือนที่ออก · JE (จำลอง)
7. PDF ใบลดหนี้ A4 อ้างเลข/วันที่ใบเดิม + มูลค่าเดิม/ที่ถูกต้อง/ผลต่าง + เหตุผล (pdfdoc)
8. รายการ/ค้นหา/กรอง/สถิติ/CSV · ประวัติ append-only · ทำสำเนา

### 3.2 Out of Scope (Functions Cut — ตัดสินแล้ว)
- **ลดหนี้ไม่อ้างใบแจ้งหนี้ (ลดลอย)** — ปิดไว้ (tile "ปิดไว้" ในหน้าจอ) · [OQ-CN-01]
- **ลดเกินยอดคงเหลือ** — บล็อกทั้งตอนส่งและตอนอนุมัติ
- **คืนเงินเมื่อชำระครบ (refund)** — ไม่รองรับใน LITE → ไปทาง RV/PV · [OQ-CN-03]
- **ยกเลิกใบลดหนี้หลังอนุมัติ** — ไม่รองรับ → ใช้ "ออกเอกสารแก้ไข" (display-only) · [OQ-CN-02]
- **หน้าจอรับคืนสินค้าจริง (Sales Return)** — เป็นของ F090 W4-LITE (mock [ASSUMED contract])

### 3.3 Assumptions
- AR Invoice (F-ACC-ARINV, ba-done) พร้อมใช้ contract `ar_open_item` (invGrand/paid/cn_applied) — **[ASSUMED contract F094]**
- Sales Return (F090), Journal Entry (F093), RV/PV (W6), DOA engine = **mock [ASSUMED contract]** ในรอบนี้ (forward-wire)
- CN reason master + DOA entry `DOA-ACC-CN` เป็น config — **[ASSUMED]** รอ Policy/Finance ยืนยันรายการสุดท้าย

### 3.4 Scope Lock ⭐
**scope_lock_ref:** CONTEXT_PACK W5-LITE §2.2 + §3 (OQ-CN-01) + GOLDEN_RULES 1–12

| LOCK | ข้อความ | สถานะใน BRD |
|---|---|---|
| LOCK-01 | Pattern Q-document + B2 v2 line editor | ✅ ยึด (§14.6) |
| LOCK-02 | อ้าง AR Invoice (ในเลน · หลัง AR ba-done) | ✅ §3.1 / §12.1 |
| LOCK-03 | เหตุผล master config: รับคืน (SR mock)/ส่วนลดภายหลัง/ผิดราคา | ✅ §9 (CN_REASONS) |
| LOCK-04 | ลดไม่เกินยอดคงเหลือใบอ้างอิง (OQ-CN-01) | ✅ BR-02 |
| LOCK-05 | DOA slot picker ตามมูลค่า | ✅ BR-07 / §5 |
| LOCK-06 | doccfg `CN-YYYY-NNNN` + pdfdoc อ้างเลขใบเดิม+เหตุผลตามประกาศสรรพากร | ✅ BR-08 / §14 |
| LOCK-07 | ระบุผลกระทบ VAT ขายใน BRD | ✅ §9 (BR-12) / §12.1 |
| LOCK-08 | dep ข้ามเลน (Sales Return/JE) = mock [ASSUMED contract] | ✅ §3.3 |
| LOCK-09 | UI #67.1/#104/#105/#106 = enforce | ✅ ส่งต่อ FRD (§14.6) |
| LOCK-10 | ค.ศ. · append-only | ✅ §7 data behaviour / §8 |

> **SCOPE DRIFT:** ไม่มี — In Scope ทุกข้ออยู่ใต้ Scope Lock. End-bill discount (FN-19) เป็นการ **ขยายภายใต้ LOCK-04/LOCK-07 ที่ BA เคาะเพิ่ม 2026-09-22** (คุมยอดสุทธิ ≤ คงค้าง + สะท้อน VAT) — ไม่ชน Exclusion.
> **LOCK conflict:** ไม่มี.

---

## 4. User Roles & Permissions

| Role (role_id) | สร้าง/ร่าง/แก้ | ส่งอนุมัติ | อนุมัติ/ไม่อนุมัติ | ส่งลูกค้า | ยกเลิก (draft/pending) | COSO |
|---|:--:|:--:|:--:|:--:|:--:|---|
| เจ้าหน้าที่ลูกหนี้ (`role-officer-ar`) | ✅ | ✅ | ❌ | ✅ | ✅ | Maker |
| ผู้จัดการฝ่ายขาย (`role-mgr-sales`) | ❌ | ❌ | ✅ (ขั้นตาม DOA) | ❌ | ❌ | Checker/Approver |
| ผู้จัดการบัญชี (`role-mgr-acc`) | ❌ | ❌ | ✅ (tier 2+) | ❌ | ❌ | Approver |
| CFO (`role-cfo`) | ❌ | ❌ | ✅ (tier 3) | ❌ | ❌ | Approver |

- **SoD (BR-07):** ผู้ส่ง (Maker) ไม่เห็นปุ่มอนุมัติใบของตัวเอง — เห็นได้แค่ปุ่ม "ยกเลิก" (ถอนจากรออนุมัติ)
- role-ids ทั้งชุดเป็น **[ASSUMED]** (OQ-AR-06) — รอ Policy Center ยืนยัน
- หมายเหตุ: HTML มี persona switcher เป็น **DEMO-only** (สลับบทบาททดสอบ) — ไม่ใช่ฟีเจอร์ production

---

## 5. User Journey (with COSO)

| # | Step | ผู้ทำ | หน้า / route | COSO | Action → ผล |
|:--:|---|---|---|---|---|
| 1 | เลือกใบแจ้งหนี้ที่ยังมียอดคงค้าง | เจ้าหน้าที่ลูกหนี้ | P-02 step1 `#/create` | Maker | ดึงลูกค้า/ที่อยู่/เลขภาษี/บรรทัดจากใบเดิม |
| 2 | เลือกเหตุผล (master) · ถ้ารับคืน→เลือกใบรับคืน · กรอกคำอธิบาย ≥10 ตัว | เจ้าหน้าที่ลูกหนี้ | P-02 step2 | Maker | กำหนดโหมดบรรทัด (qty/price) |
| 3 | ระบุจำนวน/ราคาที่ลด (≤ คงเหลือ) + ส่วนลดท้ายบิล (ถ้ามี) | เจ้าหน้าที่ลูกหนี้ | P-02 step3 | Maker | VAT/ยอดสุทธิคำนวณสด |
| 4 | แนบเอกสาร (ถ้ามี) → ทบทวน → ส่งอนุมัติ (เลือกคนต่อขั้น) | เจ้าหน้าที่ลูกหนี้ | P-02 step4/5 + submit modal | Maker | draft → pending_approval |
| 5 | อนุมัติ/ไม่อนุมัติ ตามขั้น DOA | ผจก.ขาย/บัญชี/CFO | P-04 sign tab + approve modal | Checker/Approver | ครบสาย → approved + ออกเลข CN |
| 5b | (System) ออกเลข CN · ลด ar_open_item · ลดภาษีขาย · JE mock · NTF/CSQ | System | — | System | ผลลง AR/VAT/JE |
| 6 | ส่งให้ลูกค้า (เก็บสำเนา PDF) | เจ้าหน้าที่ลูกหนี้ | P-04 send modal | Maker | approved → sent |

**Alternative / Exception paths:**
- ไม่อนุมัติ (ใส่เหตุผล) → กลับเป็น draft + เก็บ `approval_history` (append-only) — เห็น badge "ถูกตีกลับ N ครั้ง"
- ยกเลิก draft/pending (ใส่เหตุผล) → cancelled (ไม่ลบใบ · คืนยอดที่กันไว้)
- ใบเดิมถูกชำระ/ลดเพิ่มระหว่างรออนุมัติ → ขั้นสุดท้าย re-check ยอดคงค้าง ถ้าไม่พอ = อนุมัติไม่ได้ (ให้ตีกลับไปแก้)
- approved/sent → "ออกเอกสารแก้ไข" (display-only) — ไม่เปลี่ยนสถานะ/ไม่ถอนยอด (OQ-CN-02)

> **SoD check:** ทุก approval step มี Maker ≠ Approver (บังคับด้วย `s.submittedBy === ME.name` → ซ่อนปุ่มอนุมัติ). ✅
> **HTML alignment:** ทุก step map กับ route/ปุ่มที่มีจริงในไฟล์ HTML — ไม่มี step ลอย.

---

## 6. Data Entity & Fields

### 6.1 Entities
- **credit_note** (header) 1—N **credit_note_line** → (soft-ref) **ar_invoice_line**
- soft-ref: `credit_note.inv → ar_invoice`, `credit_note.sr → sales_return` (mock), `credit_note_line.src_line → ar_invoice_line`
- child: `approval_chain` (snapshot ณ ส่ง) · `approval_history` (รอบที่ถูกตีกลับ) · `audit` (append-only) · `attachments`

### 6.2 Header Fields

| # | Field | Label UI | Type | จำเป็น | ค่า/ที่มา | เงื่อนไข |
|--:|---|---|---|:--:|---|---|
| 1 | code | เลขที่ | AUTO (readonly) | ระบบ | ENG-DOC-NUM `CN-YYYY-NNNN` | ออกเมื่ออนุมัติครบ |
| 2 | inv | ใบแจ้งหนี้อ้างอิง | LOOKUP | ✓ | ar_open_item (F094) | outstanding > 0 · issued/sent |
| 3 | partner / billTo / taxId | ลูกค้า · ที่อยู่ · เลขภาษี | readonly / TEXTAREA | ✓ | ดึงจากใบเดิม | billTo แก้ได้ (ตามใบกำกับเดิม) |
| 4 | cnDate | วันที่ใบลดหนี้ | DATE | ✓ | วันนี้ | ≥ วันที่ใบเดิม |
| 5 | reason | เหตุผลการลดหนี้ | DROPDOWN-SINGLE | ✓ | CN reason master | กำหนด mode (qty/price) + legal_basis |
| 6 | sr | ใบรับคืนสินค้า | LOOKUP | ✓ เมื่อ reason=RET | Sales Return (mock) | ของใบแจ้งหนี้เดียวกัน |
| 7 | reasonText | คำอธิบายเหตุผล (พิมพ์บนใบ) | TEXTAREA | ✓ | input | ≥ 10 ตัวอักษร |
| 8 | rep | พนักงานขาย | LOOKUP (combobox) | ✓ | Employee (จากใบเดิม) | — |
| 9 | endbill | ส่วนลดท้ายบิล | TOGGLE + NUMBER + mode(฿/%) | — | input | ยอดสุทธิ ≥0 · ≤ คงค้าง (BR-11) |
| 10 | note | หมายเหตุภายใน | TEXTAREA | — | input | — |
| 11 | attachments | เอกสารแนบ | FILE | — | input | — |

### 6.3 Line Fields (B2 v2 — ล็อกจากใบเดิม)

| Field | Label | Type | เงื่อนไข |
|---|---|---|---|
| item_code / item_name | สินค้า | readonly (lock) | จากบรรทัดใบเดิม (`src_line`) |
| qty | จำนวนลด | NUMBER | ≤ (จำนวนเดิม − ลดแล้ว) · ≤ จำนวนใบรับคืน (RET) |
| unit_price | ราคาต่อหน่วยที่ลด | NUMBER | ≤ ราคาเดิม (mode price) |
| vat_mode / vat_pct | VAT | readonly | ตามบรรทัดเดิม (VAT7) |
| meta (computed) | จำนวนเดิม · ลดแล้ว · ลดได้อีก · มูลค่าลดได้อีก | display | จาก `lineRoom()` |

### 6.4 Computed
- `totals()` → before (ฐานก่อน VAT) · vat · after · **end-bill:** ebRaw → ebCap (เพดาน grand≥0) → ebAmt → ebVat (แบ่งตามสัดส่วน VAT) · **netBefore** (ฐานหลังหักส่วนลด) · **netVat** (ภาษีขายที่ลดจริง ม.86/10) · **grand** (ยอดลดหนี้สุทธิ = after − ebAmt, ≥0)
- outstanding = invGrand − paid − cn_applied(approved/sent) · available = outstanding − cn_held(draft/pending)

### 6.5 Audit / Snapshot Fields
ทุก entity: createdBy/At · updatedBy/At · approval_chain (snapshot) · approval_history · audit[] (append-only, ไม่มี hard delete) · cancelInfo (by/at/reason) · sentAt/By

### 6.6 ER Diagram
```
ar_invoice ──(1:N soft)──▶ credit_note ──(1:N)──▶ credit_note_line
                                │                        │
sales_return ──(referenced)────┘        (soft-ref)──────▶ ar_invoice_line
credit_note ──(N:1)──▶ cn_reason_master · doa_entry(DOA-ACC-CN) · employee(rep)
credit_note ──(effect on approve)──▶ ar_open_item (cn_applied) · vat_output_line(negative) · journal_entry(mock)
```

---

## 7. User Stories & Acceptance Criteria

| ID | Story (Given-When-Then) | AC |
|---|---|---|
| US-01 | ในฐานะเจ้าหน้าที่ลูกหนี้ ต้องเลือกใบแจ้งหนี้ที่ยังมียอดคงค้างเพื่อสร้างใบลดหนี้ | (1) เห็นยอดสุทธิ/ลดแล้ว/คงค้างต่อใบ (2) ใบ void/ชำระครบไม่โผล่ (3) เลือกแล้วดึงลูกค้า+บรรทัดอัตโนมัติ |
| US-02 | ต้องระบุเหตุผลจาก master พร้อมคำอธิบาย | (1) เหตุผล=รับคืน ต้องเลือกใบรับคืน (2) คำอธิบาย ≥10 ตัว มิฉะนั้นบล็อก |
| US-03 | ต้องปรับจำนวน/ราคาที่ลดภายในเพดานของบรรทัด | (1) จำนวนลด ≤ คงเหลือของบรรทัด (2) ราคาลด ≤ ราคาเดิม (3) เกิน = เตือน/บล็อก |
| US-04 | ต้องใส่ส่วนลดท้ายบิลได้เมื่อจำเป็น | (1) เปิด/ปิด toggle · โหมด ฿/% (2) ยอดสุทธิห้ามติดลบ/เกินคงค้าง (3) VAT ลดตามฐานใหม่ |
| US-05 | ต้องส่งอนุมัติตามสายที่แปรตามมูลค่า | (1) เลือกคนครบทุกขั้น (2) tier แปรตามยอดสุทธิ |
| US-06 | ผู้อนุมัติต้องอนุมัติ/ไม่อนุมัติตามสิทธิ์ขั้น | (1) ครบสาย=ออกเลข CN (2) ไม่อนุมัติ=กลับร่าง+เหตุผล (3) ไม่เห็นปุ่มอนุมัติใบตัวเอง |
| US-07 | ต้องส่งใบที่อนุมัติแล้วให้ลูกค้า | (1) สถานะ→ส่งลูกค้าแล้ว (2) เก็บสำเนา PDF (3) sent สามารถส่งสำเนาซ้ำ |
| US-08 | ต้องเห็นผลกระทบต่อ AR/VAT/บัญชี | (1) แท็บอ้างอิงแสดงคงค้างก่อน/หลัง (2) ภาษีขายที่ลด (3) JE จำลอง |

> C05 check: ทุก Story description ไม่มีคำว่า "และ" เป็นตัวเชื่อม action (แต่ละ story = 1 เจตนา). ✅

---

## 8. Status & Lifecycle

```
        A-02 บันทึกร่าง        A-04 ส่งอนุมัติ         A-05 อนุมัติครบสาย       A-07 ส่งลูกค้า
  (—) ───────────────▶ draft ───────────────▶ pending_approval ───────────────▶ approved ───────────────▶ sent
                         ▲                          │                                │  │
                         │  A-06 ไม่อนุมัติ (เหตุผล)  │                                │  │ (display-only)
                         └──────────────────────────┘                                └──┴─▶ "ออกเอกสารแก้ไข" (ไม่เปลี่ยน state)
        draft/pending ──── A-08 ยกเลิก (เหตุผล) ────▶ cancelled
```

| จาก | Action | ไป | ใคร | เงื่อนไข |
|---|---|---|---|---|
| — | A-02 | draft | officer | — |
| draft | A-04 | pending_approval | officer | grand ≤ available · DOA resolve · slot ครบ |
| pending_approval | A-05 (ครบสาย) | approved | approver ขั้นสุดท้าย | re-check grand ≤ outstanding → ออกเลข CN |
| pending_approval | A-06 | draft | approver | ใส่เหตุผล · append history |
| draft/pending | A-08 | cancelled | officer | ใส่เหตุผล |
| approved | A-07 | sent | officer | — |
| approved/sent | ออกเอกสารแก้ไข | (คงเดิม) | officer | display-only · OQ-CN-02 |

Status guards (จาก HTML): cancel เฉพาะ draft/pending · send เฉพาะ approved (sent=ส่งสำเนาซ้ำ) · submit เฉพาะ draft · edit เฉพาะ draft · approved/sent locked แก้ไข.

---

## 9. Business Rules + Validation (พร้อม Tags)

| BR | กติกา | ประเภท | Tag | ที่มา / FN |
|---|---|---|---|---|
| BR-01 | เลือกใบแจ้งหนี้ได้เฉพาะ issued/sent ที่ outstanding > 0 (void/ชำระครบ ไม่โผล่) | Prevent | FIXED | FN-01,FN-04 |
| BR-02 | ยอด CN สุทธิ ≤ outstanding ใบอ้างอิง — ตรวจทั้งตอนส่ง (available) และตอนอนุมัติขั้นสุดท้าย (outstanding) | Error/Prevent | FIXED | FN-09,FN-17 · LOCK-04 |
| BR-03 | จำนวนลดต่อบรรทัด ≤ จำนวนใบเดิม − ลดแล้ว (ทุกใบรวมกัน) | Error | FIXED | FN-07,FN-08 |
| BR-04 | ราคาลดต่อหน่วย ≤ ราคาเดิม (mode price) | Error | FIXED | FN-06 |
| BR-05 | เหตุผลจาก master + คำอธิบาย ≥ 10 ตัวอักษร | Error | FIXED (ข้อความ) / CONFIGURABLE (master) | FN-05,FN-10 |
| BR-06 | เหตุผล "รับคืน" ต้องอ้างใบรับคืนของใบเดียวกัน · จำนวนไม่เกินที่รับคืน | Error | FIXED [ASSUMED contract] | FN-05 |
| BR-07 | DOA resolve ตามมูลค่า ณ กดส่ง (freeze snapshot) · ผู้ขอไม่อนุมัติเอง (SoD) | Trigger/Prevent | CONFIGURABLE (ผ่าน DOA กลาง) | FN-11,FN-14 · LOCK-05 |
| BR-08 | เลข CN ออกเมื่ออนุมัติครบสาย (no-gap running number) | Trigger | CONFIGURABLE (doccfg) | FN-12 · LOCK-06 |
| BR-09 | อนุมัติครบ → cn_applied ใบเดิมเพิ่ม + JE (จำลอง: Dr รับคืน/ส่วนลด · Dr ภาษีขาย · Cr ลูกหนี้) + ลดภาษีขายเดือนที่ออก | Trigger | FIXED (logic) | FN-18 |
| BR-10 | ร่าง/รออนุมัติกันยอด (cn_held) ชั่วคราว — available = outstanding − held | Trigger | FIXED | FN-08 |
| **BR-11** | **ส่วนลดท้ายบิล (฿/%) หักเพิ่มจากยอดรวม · เพดาน = ยอดสุทธิ ≥0 และ ≤ ยอดคงค้าง (เกิน = บล็อก + เตือนสูงสุด)** | Error/Prevent | CONFIGURABLE | FN-19 · [BA 2026-09-22] |
| **BR-12** | **ส่วนลดท้ายบิลลดฐานภาษี → คำนวณ VAT ใหม่บนยอดหลังหักส่วนลด (แบ่งตามสัดส่วน VAT) · ภ.พ.30 + JE + PDF สะท้อนภาษีขายที่ลดจริง (ม.86/10)** | Trigger | FIXED (logic) | FN-19 · [BA 2026-09-22] |
| BR-13 | ประวัติ append-only ทุกการกระทำ · ไม่มี hard delete · วันที่เก็บเป็น ค.ศ. | Trigger | FIXED | FN-91 · LOCK-10 |
| BR-14 | ลดหนี้ไม่อ้างใบ = ปิด (tile "ปิดไว้") | Prevent | FIXED | FN-02 · OQ-CN-01 |
| BR-15 | เหตุผลแต่ละตัวพก `legal_basis` (ตามประกาศอธิบดีฯ VAT ฉบับ 82 / ม.86/10) — DISC มี trade_discount_warn (ส่วนลดทางการค้าล้วนไม่ใช่เหตุออกใบลดหนี้ภาษี) | Warning | CONFIGURABLE | OQ-CN-01 |

**DOA tier matrix (BR-07 · entry `DOA-ACC-CN`, sequential) — คิดจาก `grand` (ยอดสุทธิหลังหักส่วนลดท้ายบิล):**

| Tier | ช่วงมูลค่า (ยอดสุทธิ) | ขั้นอนุมัติ |
|:--:|---|---|
| 1 | 0 – 50,000 | ผจก.ขาย |
| 2 | 50,000.01 – 300,000 | ผจก.ขาย → ผจก.บัญชี |
| 3 | > 300,000 | ผจก.ขาย → ผจก.บัญชี → CFO |

> ⭐ **มติ BA 2026-09-22 (OQ-b RESOLVED):** DOA tier คำนวณบน **ยอดสุทธิหลังหักส่วนลดท้ายบิล** (`resolveDoa()` ใช้ `totals(s).grand`). ยืนยันตรงกับ HTML — ไม่เป็น open question อีกต่อไป.

**Validation messages (verbatim จาก HTML — ส่งต่อ FRD/QA):**
- "ยอดลดหนี้เกินยอดคงเหลือของใบแจ้งหนี้อ้างอิง — ลดได้ ฿X · ใบนี้ ฿Y · เกิน ฿Z" (hard-warn)
- "ส่วนลดท้ายบิลเกินยอดที่ลดได้ (สูงสุด ฿X) — ยอดสุทธิห้ามติดลบ"
- "อนุมัติไม่ได้ — ยอดคงค้าง X เหลือ ฿Y น้อยกว่ายอดลดหนี้ ... ให้ไม่อนุมัติกลับไปแก้"
- field-error: "ระบุคำอธิบายอย่างน้อย 10 ตัวอักษร" · "เลือกใบรับคืนของใบแจ้งหนี้นี้" · "ต้องไม่ก่อนวันที่ใบแจ้งหนี้"

### 9.5 สรุประดับความยืดหยุ่น

| Rule | ระดับ | เหตุผล | ที่มา |
|---|---|---|---|
| BR-05 (reason master), BR-15 (legal_basis) | Admin Panel / Rule Mgmt | รายการเหตุผล+เหตุตามกฎหมายเปลี่ยนตามประกาศสรรพากร | 🤖 AI-inferred → **OQ-CN-01** |
| BR-07 (DOA tier), BR-08 (doc numbering) | Rule Management (DOA/doccfg กลาง) | ตั้งค่าที่ engine กลาง ไม่ hardcode | ✅ Stakeholder (LOCK-05/06) |
| BR-11 (end-bill cap %) | Admin Panel | เพดาน/นโยบายส่วนลดปรับได้ | ✅ Stakeholder (BA 2026-09-22) |
| BR-01,02,03,04,06,09,10,12,13,14 | FIXED | กฎภาษี/คุมยอด/ตรรกะคำนวณ ไม่ควรเปลี่ยนค่า | ✅ |

> Escalation: BR-05/BR-15 (🤖 + config เหตุผลกฎหมาย) → ลง §15 OQ-CN-01 ให้ Finance ยืนยันรายการสุดท้ายก่อนพัฒนา config.

---

## 10. Edge Cases

### 10.1 ที่ user/RIF ระบุ (☑ ยืนยันแล้ว)
- ☑ EDGE-01 ใบเดิมถูกชำระ/ลดเพิ่มระหว่างรออนุมัติ → re-check ตอนอนุมัติขั้นสุดท้าย (มี DEMO harness `demoPay` พิสูจน์ S-11)
- ☑ EDGE-02 ลดหลายรอบบนใบเดียว → บรรทัดแสดง จำนวนเดิม/ลดแล้ว/ลดได้อีก ถูกต้อง (cn_applied + cn_held)
- ☑ EDGE-03 ใบเดิม void → CN ที่ร่างค้างอ้างไม่ได้ (ไม่โผล่ใน picker)
- ☑ EDGE-04 ใบชำระครบ → ไม่โผล่ (refund ไม่รองรับ LITE)
- ☑ EDGE-05 ยกเลิก draft/pending → คืนยอดที่กันไว้
- ☑ EDGE-06 ไม่อนุมัติ → เก็บ approval_history + badge "ถูกตีกลับ N ครั้ง"

### 10.2 จาก AI Pattern Matching (☐ = แนะนำ — รอ BA/FRD ยืนยันที่ SOW3.7)
- ☐ CL-01 (Calculation) ปัดเศษ VAT/ส่วนลดหลายอัตรา — ยืนยันวิธีปัด (HTML ใช้ปัด 2 ตำแหน่ง, แบ่ง ebVat ตามสัดส่วน)
- ☐ ST-01 (Status) แข่งกันอนุมัติ 2 คนพร้อมกันบนขั้นเดียว (concurrent) — กำหนด lock ระดับ record
- ☐ PD-01 (PDF) เนื้อหาบังคับบนใบลดหนี้ตามสรรพากร (เลขใบเดิม/เหตุผล/ผลต่าง) — ครบใน pdfdoc spec แล้ว
- ☐ FU-01 (File) ชนิด/ขนาดไฟล์แนบที่อนุญาต
- ☐ PM-01 (Permission) การมองเห็นใบข้ามแผนก/สาขา
- ⚠️ CA-01 ใบเดิมถูกลด/ชำระเกิน available หลัง freeze DOA แต่ก่อนอนุมัติ — **กระทบเงิน → ยกเป็น OQ ทันที** (มี guard BR-02 re-check แล้ว แต่ควรยืนยัน UX เมื่อ block)

---

## 11. Impact / Regression
New Feature — ไม่มี regression ภายใน feature. ผลกระทบข้ามระบบดู §12.1 (AR Invoice / VAT Report / JE / RV).

---

## 12. System Context

### 12.1 Value Stream & Downstream Impact ⭐
**Value Stream:** Order-to-Cash → AR sub-stream (หลัง AR Invoice, ก่อน Receipt/Collection).
**Upstream:** AR Invoice (F-ACC-ARINV, issued/sent, contract `ar_open_item`) · Sales Return (F090 W4-LITE, mock) เป็น trigger สำหรับเหตุ RET.

| ปลายทาง (Downstream) | ข้อมูลที่ไหลไป | Trigger | ถ้า CN เปลี่ยน/ยกเลิก → แล้วไงต่อ |
|---|---|---|---|
| AR Invoice / ar_open_item (F094) | cn_applied เพิ่ม → outstanding ลด (ปิดเมื่อ=0) | อนุมัติครบ (approved/sent) | ยกเลิกก่อนอนุมัติ = คืนยอด (held) · หลังอนุมัติยกเลิกไม่ได้ → ออกเอกสารแก้ไข (OQ-CN-02) |
| VAT Report ภ.พ.30 | `output_vat_line` (ค่าลบ) = netVat · เดือน = เดือน cnDate (ม.82/10) | อนุมัติครบ | contract output_vat_line (negative) — forward-wire |
| Journal Entry (F093) | Dr 4110/4120 (netBefore) · Dr 2150 ภาษีขาย (netVat) · Cr 1130 ลูกหนี้ (grand) | อนุมัติครบ | mock [ASSUMED] — forward-wire F093 |
| Receipt/Payment (RV/PV, W6) | อ่าน outstanding หลังลด | — | refund กรณีชำระครบ = นอก scope → RV/PV (OQ-CN-03) |

**ผลกระทบแนวขวาง:** บัญชี (GL ผ่าน JE) · ภาษี (ภ.พ.30) · AR aging/outstanding · ไม่กระทบสต๊อก (สต๊อกอยู่ที่ Sales Return จริง).

### 12.3 Existing System Reference

| Rule/ฟังก์ชัน | ระดับ | มีอยู่แล้ว? | Reference |
|---|---|:--:|---|
| BR-07 DOA tier | Rule Mgmt (DOA engine) | ⚠️ engine กลาง มีแล้ว · entry `DOA-ACC-CN` ต้องตั้งค่า | DOA_BRIEF_F-ACC-CN |
| BR-08 running number CN | doccfg กลาง | ⚠️ engine มีแล้ว · doc_type CN ต้อง register | DOCCFG_BRIEF_F-ACC-CN |
| notification events | ENG-NOTIFY | ⚠️ มีแล้ว · ต้อง wire cn.issued/cn.sent | NTF_BRIEF_F-ACC-CN |
| 7C consequence | ENG-CSQ | ⚠️ มีแล้ว · register cn.issued→AC(+EC) | CSQ_BRIEF_F-ACC-CN |
| ar_open_item | AR Invoice F094 | ✅ ba-done (contract) | BRD_F-ACC-ARINV §12.1 |
| Sales Return / JE | F090 / F093 | ❌ mock ในรอบนี้ | [ASSUMED contract] |

---

## 13. Delivery Phases

- **Phase 1 (Feature Launch):** ตาราง credit_note/line + state machine + config seed (reason master, DOA-ACC-CN entry, doc_type CN) · line editor + end-bill engine · guards BR-01..14 · PDF A4 · CSV. ห้าม hardcode ตั้งแต่วันแรก. Reuse: AR ar_open_item, DOA engine, doccfg engine, ENG-NOTIFY, ENG-CSQ.
- **Phase 2 (Admin Panel):** จัดการ CN reason master + เพดานส่วนลดท้ายบิล (BR-05/BR-11) — เมื่อ Finance ยืนยัน OQ-CN-01.
- **Phase 3 (Rule Management):** DOA tier ปรับผ่านหน้า DOA กลาง (BR-07) — dependency DOA engine wire.
- **Phase 4 (Engine/Integration wire):** เชื่อม Sales Return จริง (F090), JE จริง (F093), VAT Report จริง, RV/PV (แทน mock/DEMO harness).

---

## 14. Dev Requirements Summary ("ใบสั่ง")

### 14.1 Config Foundation ที่ต้องเตรียม
- `cn_reason_master` (code/name/mode qty|price/needSR/legal_basis/trade_discount_warn) — seed 4 เหตุผล
- DOA entry `DOA-ACC-CN` (sequential, 3-tier by value 50k/300k) — ตั้งที่ DOA กลาง
- doc_type `CN` running `CN-YYYY-NNNN` (no-gap, ออกตอน final approve) — ที่ doccfg กลาง

### 14.2 ข้อกำหนดจาก Tag (non-FIXED)
- BR-05/BR-15 (reason+legal): อ่านจาก master config — ห้าม hardcode รายการเหตุผล/เหตุตามกฎหมาย
- BR-07 (DOA): resolve จาก DOA engine ตามมูลค่า **grand หลังหักส่วนลดท้ายบิล** · freeze snapshot ณ ส่ง · SoD บังคับ
- BR-08 (number): ใช้ ENG-DOC-NUM.next() ไม่ generate เอง
- BR-11 (end-bill cap): เพดานปรับได้ผ่าน Admin Panel

### 14.3 Edge/Validation ที่ Dev ต้อง handle เป็นพิเศษ
- re-check outstanding ณ อนุมัติขั้นสุดท้าย (BR-02) — กันชำระ/ลดเพิ่มระหว่างรอ
- cn_held (draft/pending) กันยอดชั่วคราว — available = outstanding − held
- end-bill VAT recompute (BR-12): แบ่ง ebVat ตามสัดส่วน VAT ในยอดรวม (รองรับหลายอัตรา/VAT-inclusive)
- **ลบ DEMO artifacts ก่อน production:** persona switcher · `demoPay` (จำลอง RV) · `.demo-only` blocks — HTML ทำเครื่องหมาย `DEMO-ONLY: ห้าม render ใน production build` ไว้แล้ว

### 14.4 WARNING ที่รอข้อสรุป → ดู §15 (ห้ามเริ่มพัฒนาส่วนที่เกี่ยว จนกว่า resolve)

### 14.6 Screen Inventory + UI Signals (หยาบ — spec จริงไป FRD)

| # | ชื่อหน้า | route (จาก HTML) | ประเภทหยาบ | ผู้ใช้หลัก | หน้าที่ (business) |
|---|---|---|---|---|---|
| P-01 | รายการใบลดหนี้ | `#/list` | หน้ารายการ + stat | เจ้าหน้าที่ลูกหนี้ · ผู้อนุมัติ | ค้นหา/กรอง (สถานะ/เหตุผล/ลูกค้า) · stat 4 tile · CSV · row menu |
| P-02 | สร้างใบลดหนี้ | `#/create` | ฟอร์มสร้าง (wizard 5 ขั้น) | เจ้าหน้าที่ลูกหนี้ | s1 เลือกแหล่ง(ใบแจ้งหนี้; tile "ลดลอย" ปิด) · s2 ข้อมูลหลัก · s3 line+ส่วนลดท้ายบิล · s4 แนบ · s5 ทบทวน+DOA preview |
| P-03 | แก้ไขใบลดหนี้ | `#/edit/:id` | ฟอร์มแก้ไข (draft only, เปิดที่ขั้น 2) | เจ้าหน้าที่ลูกหนี้ | แก้ร่าง |
| P-04 | รายละเอียดใบลดหนี้ | `#/view/:id` | หน้ารายละเอียด (drawer, 5 tabs) | ทุก role | tabs: รายละเอียด / ใบแจ้งหนี้อ้างอิง·ภาษีขาย / PDF Preview / ลายเซ็น·อนุมัติ / ประวัติ |
| (modal) | ส่งอนุมัติ (slot picker DOA) · อนุมัติ · ไม่อนุมัติ · ยกเลิก (เหตุผล) · ส่งลูกค้า · ออกเอกสารแก้ไข | overlay | — | ผู้ใช้ตามสิทธิ์ | actions ตาม state |

**สรุปจำนวนหน้า:** ~4 หน้าหลัก (รายการ 1 · wizard สร้าง/แก้ 1 · รายละเอียด 1) + overlay actions. ตรงกับจำนวน route ใน HTML เป๊ะ — **ไม่มี HTML-RIF drift.**

**UI Signals ส่งต่อ FRD:**
- เป็น **Document/Transaction (Pattern Q)** — มี approver + PDF + ลายเซ็น + ประวัติ + เอกสารแนบ (LOCK-01)
- ต้อง **print/PDF** (pdfdoc — A4 ที่ `outputs/F-ACC-CN/_print/`)
- Line editor = **B2 v2** (LOCK-01)
- Iron rules #67.1/#104/#105/#106 = enforce (LOCK-09) — Design Authority ที่ FRD/html-generator-v9

---

## 15. Open Questions

| OQ | คำถาม | สถานะ | owner |
|---|---|---|---|
| OQ-CN-01 | รายการเหตุผลตามกฎหมายฉบับสุดท้าย + จุดยืน "ส่วนลดทางการค้าล้วน" (trade_discount_warn) | ⚠️ รอ | Strike + Finance |
| OQ-CN-02 | เส้นทาง "ออกเอกสารแก้ไข" หลังอนุมัติ — Debit Note vs CN ใหม่อ้างใบนี้ (ปัจจุบัน display-only) | ⚠️ รอ | Strike |
| OQ-CN-03 | CSQ profile / กรณีชำระครบแล้วต้องการลด (refund → FC path) | ⚠️ รอ | Strike + Finance |
| OQ-CN-04 | เดือนภาษี (tax month) ที่ลง ภ.พ.30 — ยืนยันยึดวันที่ออกใบลดหนี้ (ม.82/10) | ⚠️ รอ | Policy/Finance |
| OQ-AR-06 | role-ids จริง (officer-ar / mgr-acc [ASSUMED]) | ⚠️ รอ | Policy Center |
| — AR Invoice contract F094 | ยืนยัน contract `ar_open_item` (invGrand/paid/cn_applied) | [ASSUMED] | AR team |
| ~~OQ-b~~ | ~~DOA tier คิดบนยอดก่อนหรือหลังส่วนลดท้ายบิล~~ | ✅ **RESOLVED 2026-09-22** — คิดบน **ยอดสุทธิหลังหักส่วนลด** | BA |

---

## 16. Security & Compliance

### 16.1 Preset
**P4 — Financial/Payment (16 controls)** — เหตุผล: กระทบยอดลูกหนี้/ภาษี/GL โดยตรง + มีสายอนุมัติตามมูลค่า.

### 16.2 Applicable Standards
COSO (Maker/Checker/Approver + SoD) · Thai Revenue Code ม.86/10 (ออกใบลดหนี้อ้างใบกำกับเดิม) · ม.82/10 (เดือนภาษี) · PDPA (ข้อมูลลูกค้า) · Audit trail (append-only).

### 16.3 Control Checklist (สำคัญ)
- ✓Must SoD: ผู้ส่งไม่อนุมัติใบตัวเอง (BR-07)
- ✓Must Approval-by-value ผ่าน DOA (BR-07)
- ✓Must Immutable audit / no hard delete (BR-13)
- ✓Must Snapshot approval_chain ณ ส่ง (freeze)
- ✓Must Number integrity no-gap ตอน final approve (BR-08)
- ✓Must Amount ceiling ≤ outstanding ทั้งส่ง+อนุมัติ (BR-02)
- ○Opt Field-level lock (approved/sent) — enforced
- ○Opt Attachment type/size validation (Edge FU-01, รอ FRD)

### 16.4 Risk Statement
| Risk | Mitigated by |
|---|---|
| R-A ลดหนี้เกินยอดจริง → หนี้สูญ/งบผิด | BR-02 (re-check ส่ง+อนุมัติ), BR-03/04, BR-10 held |
| R-B ผู้ขออนุมัติเอง → ทุจริต | BR-07 SoD |
| R-C ออกใบลดหนี้ผิดหลักภาษี → ค่าปรับสรรพากร | BR-06/BR-12/BR-15, legal_basis, pdfdoc อ้างใบเดิม |
| R-D แก้ยอด/ลบใบย้อนหลัง | BR-13 append-only, "ออกเอกสารแก้ไข" แทนยกเลิก |

---

## 17. Health Check

### 17.1 SLA
- หน้ารายการ/สร้าง p95 < 3s (RIF §12)
- เวลาอนุมัติเฉลี่ย (ส่ง→ครบสาย) ≤ 1 วันทำการ (owner: ผู้อนุมัติแต่ละขั้น)

### 17.2 Control Points
map จาก §16.3: SoD gate · amount-ceiling gate (ส่ง+อนุมัติ) · number-issue gate (final approve) · audit-write ทุก transition.

### 17.3 KPI

| KPI | ประเภท | Target | คู่ §2.3 |
|---|---|---|---|
| KPI-Q1 CN เกินคงเหลือ | Quality/Compliance | 0 | ✔ |
| KPI-S1 เวลาอนุมัติเฉลี่ย | Speed | ≤ 1 วัน | ✔ |
| KPI-C1 CN ไม่มีเหตุผล/ไม่อ้างใบ | Compliance | 0 | ✔ |
| KPI-V1 ปริมาณ CN/เดือน | Volume | ~120 | ✔ |

### 17.4 Threshold
- ยอดลดหนี้/เดือน เทียบยอดขาย → เกิน X% = alert (นโยบาย Finance, รอค่า)
- CN ตีกลับ > N ครั้ง/ใบ = flag ทบทวนคุณภาพงาน

### 17.5 Throughput
Baseline ~120 ใบ/เดือน · Stress point: การ re-check outstanding พร้อมกันหลายใบต่อใบแจ้งหนี้เดียว (concurrent — ดู Edge CA-01).

---

## 18. Monitoring

- **18.1 Reports:** Performance (เวลาอนุมัติ) · Closing (ภาษีขายที่ลด/เดือน สำหรับ ภ.พ.30) · Anomaly (CN เกินคงเหลือ/ตีกลับบ่อย) · Transaction (รายการ CN)
- **18.2 Dashboard Widgets:** stat tiles ในหน้ารายการ (รออนุมัติ + ยอด · ลดหนี้เดือนนี้ · ฉบับร่าง · **ภาษีขายที่ลดเดือนนี้**) — อ้าง KPI §17.3
- **18.3 Performance Report:** สาย DOA ที่ค้างนาน per tier
- **18.4 Closing Report:** สรุป netVat รายเดือน → กระทบ ภ.พ.30
- **18.5 Anomaly Report:** CN ที่ block เพราะเกินคงเหลือ · ใบตีกลับ
- **18.6 Transaction Report:** CN ทั้งหมด + สถานะ + ยอด + ภาษีขายที่ลด (= CSV export)

---

## 19. Declarations (รอบนี้)

| ท่อ | ใช้ | สรุป |
|---|:--:|---|
| **doa** | ✅ | `DOA-ACC-CN` sequential 3-tier by value (50k/300k) — tier บนยอดสุทธิหลังส่วนลด · slot picker · SoD |
| **ntf** | ✅ | events: `cn.issued`→ผู้สร้าง+AR · `cn.sent`→ลูกค้า · (`doa_pending`/`doa_result` มาจาก DOA engine — ห้ามประกาศซ้ำ) |
| **csq** | ✅ | `cn.issued`→AC (ลด AR + กลับภาษีขาย) (+EC) · FC ตาม CSQ_BRIEF (รอ OQ-CN-03) · DC จาก DOA engine — ห้ามซ้ำ |
| **doccfg** | ✅ | doc_type `CN` running `CN-YYYY-NNNN` no-gap ตอน final approve |
| **pdfdoc** | ✅ | A4 print (thai-doc-pdf-generator) ที่ `outputs/F-ACC-CN/_print/` (template.html + sample.pdf + print-spec.md) |

> DECLARATION_INDEX: DIVERGENCE = ไม่มี (chip ตรง detect ทุกท่อ).

---

## 19b. AI Review Report (Quality Gate)

```
BRD: BRD-F-ACC-CN — Credit Note (ใบลดหนี้ลูกค้า) · New Feature · 2026-09-22
CHECKLIST:
✅ C01 Business objective วัดผลได้ (§2.3 มี baseline/target/แหล่งวัด)
✅ C02 User roles ครบ (§4)   ✅ C05 Story ไม่มีคำว่า "และ"
✅ C10 ทุก rule ที่มีตัวเลข/เงื่อนไข ติด Tag (§9)
✅ C13 Edge cases ครบหมวด (§10.1 BA + 10.2 AI)
✅ C18 WARNING ทุกข้อมีแผน/owner (§15)   ✅ C19 §14 ใบสั่งครบ
✅ C20 Scope Lock §3.4 ครบ 10 LOCK · ไม่มี drift เงียบ
✅ C21 Value Stream §12.1 upstream+downstream ตอบ "แล้วไงต่อ" ทุกแถว
✅ C22 ตัวชี้วัด §2.3 มีคู่ §17.3 ครบ
✅ C23 §9.5 marker 🤖/✅ ครบ · 🤖 config เหตุผล → OQ-CN-01
✅ PE01 COSO ทุก step (§5)   ✅ PE02 SoD (Maker≠Approver)
✅ PE03 Security preset P4 + controls   ✅ PE04 SLA/KPI/Threshold (§17)
✅ PE05 Cross-section coverage (BC↔Edge, Control↔Health, Metric↔Monitor)

SUMMARY: ผ่าน 23/23 + PE 5/5
สถานะ: ✅ APPROVED — พร้อมเข้า frd-generator-v6
หมายเหตุ: ยังมี 5 OQ + 1 ASSUMED contract เปิดค้าง (ไม่บล็อก BRD — ต้อง resolve ก่อนพัฒนา Phase ที่เกี่ยว)
```

**Next step:** BRD พร้อมส่งเข้า `frd-generator-v6` (step 7 · ใช้ BRD นี้ + HTML FINAL + declaration briefs).
