# BRD — Debit Note (ใบลดหนี้ผู้ขาย) · F-ACC-DN / F097

> Business Requirements Document · **Fresh Mode (HTML-first · Lane-like no-ask)** · WF-01 SOW3.2
> Source of truth: `outputs/F-ACC-DN/F-ACC-DN_debit-note.html` (FINAL — ผ่าน ux gate + coverage gate R1 · 2026-09-23 BA FIX)
> ร่วมกับ: `PREBRIEF_F-ACC-DN.md` · `FUNCTION_CHECKLIST_F-ACC-DN.md` (24 FN) · `DECLARATION_INDEX.md`
> Mirror ของ **F-ACC-CN (Credit Note · ใบลดหนี้ลูกค้า)** ฝั่ง AR — re-domain เป็น AP/ผู้ขาย

---

## 1. Document Info

| | |
|---|---|
| **BRD ID** | BRD-F-ACC-DN |
| **Feature** | Debit Note — ใบลดหนี้ผู้ขาย (F-ACC-DN · F097) |
| **ประเภท** | New Feature |
| **Module** | Accounting / Accounts Payable (AP) · Wave W5 Phase A (LITE) |
| **Version** | v1.0 |
| **Status** | APPROVED (Quality Gate ผ่าน — ดู §19b AI Review) |
| **Owner** | BA (WF-01) |
| **Stakeholders** | Strike (Policy/OQ owner) · Finance/บัญชี · จัดซื้อ · Policy Center (DOA) · Dev · QA |
| **วันที่** | 2026-09-23 |
| **Conflict priority** | LOCK-XX > PREBRIEF (business intent) > HTML (หน้าจอจริง) |

### 1.1 Changelog
- **v1.0 (2026-09-23)** — Initial BRD ผ่าน brd-generator-full (Fresh Mode, HTML-first, no-ask). สกัด Screen Inventory + Journey + Rules จาก HTML FINAL (`F-ACC-DN_debit-note.html`) เติม business intent จาก PREBRIEF + FUNCTION_CHECKLIST (24 FN). โครงสร้าง mirror จาก BRD_F-ACC-CN (AR) re-domain → AP. บันทึกมติ BA 2026-09-23: **FIX-01 เครดิตคงเหลือกับผู้ขาย (FN-04 กลับด้าน + FN-20/BR-13)** · **FIX-02 ภาษีซื้อยึด vendorCn+วันที่ (FN-21/BR-14)** · end-bill discount IN scope (FN-19/BR-11/BR-12).

---

## 2. Business Context

### 2.1 ปัญหา / โอกาส
- **PAIN-01** ปัจจุบันลดหนี้ผู้ขายโดยแก้ยอดในใบตั้งหนี้เดิม → ผิดหลักภาษี (ต้องออกใบลดหนี้อ้างใบกำกับเดิม + ยึดใบลดหนี้จากผู้ขายในการกลับภาษีซื้อ ตาม ม.86/10, ม.82/10)
- **PAIN-02** ลดเกินมูลค่าที่ลดได้ / ลดซ้ำบนใบตั้งหนี้เดียวกันโดยไม่มีตัวคุม
- **PAIN-03** คืนของหลังจ่ายเงินครบแล้ว ไม่มีที่บันทึก "เครดิตคงเหลือกับผู้ขาย" — ตกหล่น/ทวงยาก
- **PAIN-04** ไม่มีสายอนุมัติตามมูลค่า — อนุมัติทางแชท ไม่มีร่องรอย

### 2.2 เป้าหมาย business
- **GOAL-01** ออกใบลดหนี้ผู้ขายอ้างใบตั้งหนี้ให้ถูกต้องตามกฎหมายภาษี (ม.86/10, ม.82/10)
- **GOAL-02** คุมยอดลดไม่ให้เกินมูลค่าที่ลดได้ของใบอ้างอิง + จับส่วนที่เกินคงค้างเป็นเครดิตคงเหลือกับผู้ขาย
- **GOAL-03** กลับภาษีซื้อในเดือนที่ถูกต้อง (ตามวันที่ได้รับใบลดหนี้จากผู้ขาย) — กันกลับภาษีซื้อก่อนมีเอกสาร
- **GOAL-04** อนุมัติตามมูลค่าผ่าน DOA (3 tier) + เก็บ audit ครบ

### 2.3 ตัวชี้วัดความสำเร็จ (วัดได้)

| ตัวชี้วัด | Baseline ปัจจุบัน | Target | วัดยังไง/จากไหน | วัดเมื่อไหร่ | คู่ §17.3 |
|---|---|---|---|---|---|
| DN ที่ยอดเกินมูลค่าที่ลดได้ของใบอ้างอิง | ต้องเก็บ baseline ก่อน launch (เดิมไม่มีระบบคุม) | 0 ใบ | DB: นับ DN ที่ grand > dnRoom ณ อนุมัติ | รายเดือน | KPI-Q1 |
| ภาษีซื้อที่กลับก่อนมีใบลดหนี้ผู้ขาย | ต้องเก็บ baseline (เดิมแก้มือ) | 0 รายการ | DB: input_vat_line applied ที่ vendorCn IS NULL | รายเดือน | KPI-C2 |
| เวลาอนุมัติเฉลี่ย (ส่ง→อนุมัติครบ) | ต้องเก็บ baseline (เดิมอนุมัติทางแชท) | ≤ 1 วันทำการ | timestamp submittedAt → approved_at | รายเดือน | KPI-S1 |
| DN ที่ไม่มีเหตุผล/ไม่อ้างใบ | ต้องเก็บ baseline | 0 ใบ | DB: reason IS NULL หรือ inv IS NULL (ระบบบังคับ) | รายเดือน | KPI-C1 |
| ปริมาณงาน | ~80 ใบ/เดือน (ประมาณการ · ฝั่งซื้อ) | รองรับได้ | นับ DN/เดือน | รายเดือน | KPI-V1 |

### 2.4 ที่มา
CONTEXT_PACK §2 ข้อ 4 (W5Q#2) · workflow_graph edge `F-ACC-APINV → F-ACC-DN` · BRD_F-ACC-APINV §12.1 (contract `ap_open_item`) · FEATURE_LIST F097 · sibling F096 (Credit Note) เป็น structural template.

---

## 3. Scope

### 3.1 In Scope
1. สร้าง/แก้ร่าง/ส่งอนุมัติ/อนุมัติ/ไม่อนุมัติ/ส่งผู้ขาย/ยกเลิก ใบลดหนี้ผู้ขาย **ที่อ้างใบตั้งหนี้ (AP Invoice) เสมอ**
2. เหตุผลการลดหนี้จาก master (คืนสินค้า RTV / ราคาเกิน / ของขาด) — แต่ละเหตุผลมี `legal_basis`
3. Line editor ล็อกสินค้าจากใบตั้งหนี้เดิม — ลดจำนวน (ของขาด) หรือ ลดราคาต่อหน่วย (ราคาเกิน)
4. **ส่วนลดท้ายบิล (end-bill discount)** — ฿/% · จำกัดยอดสุทธิ ≥0 และ ≤ ยอดคงค้าง · ลดฐานภาษี → คำนวณภาษีซื้อใหม่ (FN-19 · BR-11 · BR-12 · มติ 2026-09-23)
5. **เครดิตคงเหลือกับผู้ขาย (vendor credit)** — เพดาน DN = มูลค่าที่ลดได้ (dnRoom = grand − ลดหนี้แล้ว − กันยอด · **ไม่หัก paid**) · ใบจ่ายครบยังออก DN ได้ (คืนของหลังจ่าย) · แยกยอด หักจากหนี้ค้าง / เครดิตคงเหลือ · card + section รายผู้ขาย (display-only) (FN-04/FN-20 · BR-13 · มติ BA FIX-01)
6. อนุมัติตามมูลค่าผ่าน DOA 3-tier (slot picker เลือกคนต่อขั้น) — **tier คิดจากยอดสุทธิหลังหักส่วนลดท้ายบิล**
7. ออกเลข `DN-YYYY-NNNN` เมื่ออนุมัติครบ (doccfg) · ลดยอดคงค้าง AP (dn_applied) · JE (จำลอง)
8. **กลับภาษีซื้อ (ภ.พ.30) ตาม vendorCn** — กรอกเลขที่ + วันที่ใบลดหนี้จากผู้ขาย · ไม่มี → "รอเอกสาร" · เดือนภาษี = เดือนของวันที่ได้รับ · ปุ่มบันทึกภายหลังบนใบ approved/sent (FN-21 · BR-14 · มติ BA FIX-02)
9. PDF ใบลดหนี้ฝั่งซื้อ A4 อ้างเลข/วันที่ใบกำกับเดิม + มูลค่าเดิม/ที่ถูกต้อง/ผลต่าง + เหตุผล · ค.ศ. (pdfdoc)
10. รายการ/ค้นหา/กรอง/สถิติ/CSV · ประวัติ append-only · ทำสำเนา

### 3.2 Out of Scope (Functions Cut — จากหมวด "สิ่งที่ไม่รองรับ" ของ FUNCTION_CHECKLIST)
- **ลดหนี้ไม่อ้างใบตั้งหนี้ (ลดลอย)** — ปิดไว้ (tile "ปิดไว้" ในหน้าจอ) · [OQ-DN-01]
- **เรียกเงินคืนเมื่อจ่ายครบ (refund/FC)** — ไม่รองรับใน LITE → ส่วนเกินไปเป็นเครดิตคงเหลือกับผู้ขายแทน · [OQ-DN-03]
- **ยกเลิกใบลดหนี้หลังอนุมัติ** — ไม่รองรับ → ใช้ "ออกเอกสารแก้ไข" (display-only) · [OQ-DN-04]
- **หน้าจอคืนสินค้าจากผู้ขาย (RTV) จริง** — เป็นของ W3-LITE (mock lookup [ASSUMED contract])

### 3.3 Assumptions
- AP Invoice (F-ACC-APINV) พร้อมใช้ contract `ap_open_item` (invGrand/paid/dn_applied) — **[ASSUMED contract]**
- RTV (คืนสินค้าจากผู้ขาย, W3-LITE), Journal Entry (F093), PV (W6), DOA engine = **mock/forward-wire [ASSUMED contract]** ในรอบนี้
- DN reason master + DOA entry `DOA-ACC-DN` + doc_type `DN` เป็น config — **[ASSUMED]** รอ Policy/Finance ยืนยันรายการสุดท้าย
- **legal basis ฝั่งซื้อ (การกลับภาษีซื้อ ม.82/10)** = **[ASSUMED — mirror ของ CN ฝั่ง AR]** รอ BA รับรองอย่างเป็นทางการ (OQ-DN-05)
- DOA tier boundaries (50k/300k) = **[ASSUMED — mirror CN]** รอ `DOA-ACC-DN` ยืนยัน

### 3.4 Scope Lock ⭐
**scope_lock_ref:** PREBRIEF §0 Obligations (OB-1..OB-9) + CONTEXT_PACK §2 ข้อ 4 + GOLDEN_RULES (GR)

| LOCK | ข้อความ | สถานะใน BRD |
|---|---|---|
| LOCK-01 | Pattern Q-document + B2 v2 line editor (OB-9 · UI #67.1/#104/#105/#106) | ✅ ยึด (§14.6) |
| LOCK-02 | อ้าง AP Invoice (ในเลน · OB-1) | ✅ §3.1 / §12.1 |
| LOCK-03 | เหตุผล master config: คืนของ RTV/ราคาเกิน/ของขาด (OB-3) | ✅ §9 (DN_REASONS) |
| LOCK-04 | ลดไม่เกินมูลค่าที่ลดได้ของใบอ้างอิง (OB-2) | ✅ BR-02 / BR-13 |
| LOCK-05 | DOA slot picker ตามมูลค่า (OB-5) | ✅ BR-07 / §5 |
| LOCK-06 | doccfg `DN-YYYY-NNNN` + pdfdoc อ้างเลขใบเดิม+เหตุผล (OB-6) | ✅ BR-08 / §14 |
| LOCK-07 | ระบุผลกระทบ VAT ซื้อใน BRD (OB-7) | ✅ §9 (BR-09/BR-12/BR-14) / §12.1 |
| LOCK-08 | dep ข้ามเลน (RTV/JE/PV) = mock [ASSUMED contract] (OB-4) | ✅ §3.3 |
| LOCK-09 | UI #67.1/#104/#105/#106 = enforce (OB-9) | ✅ ส่งต่อ FRD (§14.6) |
| LOCK-10 | ค.ศ. · append-only (OB-9) | ✅ §7 data behaviour / §8 |

> **SCOPE DRIFT:** ไม่มี — In Scope ทุกข้ออยู่ใต้ Scope Lock.
> - End-bill discount (FN-19) = ขยายภายใต้ LOCK-04/LOCK-07 (คุมยอดสุทธิ ≤ คงค้าง + สะท้อน VAT) — มติ 2026-09-23
> - เครดิตคงเหลือกับผู้ขาย (FN-20/BR-13) = ปรับความหมาย LOCK-04 ตามมติ BA FIX-01 (เพดาน = มูลค่าที่ลดได้ ไม่หัก paid; ส่วนเกินคงค้าง = vendor credit) — ไม่ชน Exclusion (refund ยังปิด)
> **LOCK conflict:** ไม่มี.

---

## 4. User Roles & Permissions

| Role (role_id) | สร้าง/ร่าง/แก้ | ส่งอนุมัติ | อนุมัติ/ไม่อนุมัติ | ส่งผู้ขาย | บันทึก vendorCn | ยกเลิก (draft/pending) | COSO |
|---|:--:|:--:|:--:|:--:|:--:|:--:|---|
| เจ้าหน้าที่เจ้าหนี้ (`role-officer-ap`) | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | Maker |
| ผู้จัดการจัดซื้อ (`role-mgr-purchase`) | ❌ | ❌ | ✅ (ขั้นตาม DOA) | ❌ | ❌ | ❌ | Checker/Approver |
| ผู้จัดการบัญชี (`role-mgr-acc`) | ❌ | ❌ | ✅ (tier 2+) | ❌ | ✅ | ❌ | Approver |
| CFO (`role-cfo`) | ❌ | ❌ | ✅ (tier 3) | ❌ | ❌ | ❌ | Approver |

- **SoD (BR-07):** ผู้ส่ง (Maker) ไม่เห็นปุ่มอนุมัติใบของตัวเอง — เห็นได้แค่ปุ่ม "ยกเลิก" (ถอนจากรออนุมัติ)
- role-ids ทั้งชุดเป็น **[ASSUMED]** (OQ-AP-06) — รอ Policy Center ยืนยัน
- หมายเหตุ: HTML มี persona switcher เป็น **DEMO-only** (`data-demo="persona-switch"` + DEMO badge) — ไม่ใช่ฟีเจอร์ production

---

## 5. User Journey (with COSO)

| # | Step | ผู้ทำ | หน้า / route | COSO | Action → ผล |
|:--:|---|---|---|---|---|
| 1 | เลือกใบตั้งหนี้ที่ยังมีมูลค่าที่ลดได้ | เจ้าหน้าที่เจ้าหนี้ | P-02 step1 `#/create` | Maker | ดึงผู้ขาย/ที่อยู่/เลขภาษี/เลขใบกำกับเดิม/บรรทัดจากใบเดิม |
| 2 | เลือกเหตุผล (master) · ถ้าคืนของ→เลือกใบ RTV · กรอกคำอธิบาย ≥10 ตัว | เจ้าหน้าที่เจ้าหนี้ | P-02 step2 | Maker | กำหนดโหมดบรรทัด (จำนวน/ราคา) |
| 3 | ระบุจำนวน/ราคาที่ลด (≤ มูลค่าที่ลดได้) + ส่วนลดท้ายบิล (ถ้ามี) | เจ้าหน้าที่เจ้าหนี้ | P-02 step3 | Maker | ภาษีซื้อ/ยอดสุทธิคำนวณสด |
| 4 | แนบเอกสาร (ถ้ามี) → ทบทวน → ส่งอนุมัติ (เลือกคนต่อขั้น) | เจ้าหน้าที่เจ้าหนี้ | P-02 step4/5 + submit modal | Maker | draft → pending_approval |
| 5 | อนุมัติ/ไม่อนุมัติ ตามขั้น DOA | ผจก.จัดซื้อ/บัญชี/CFO | P-04 sign tab + approve modal | Checker/Approver | ครบสาย → approved + ออกเลข DN |
| 5b | (System) ออกเลข DN · ลด ap_open_item (applyToAp) · แยก vendorCredit · JE mock · NTF/CSQ | System | — | System | ผลลง AP/JE · ภาษีซื้อ **รอ vendorCn** |
| 6 | บันทึกเลขที่+วันที่ใบลดหนี้จากผู้ขาย (vendorCn) | เจ้าหน้าที่เจ้าหนี้/ผจก.บัญชี | P-04 ref tab · `openVendorCn` | Maker/Approver | ภาษีซื้อลดในเดือนของวันที่ได้รับ (ม.82/10) |
| 7 | ส่งให้ผู้ขาย (เก็บสำเนา PDF) | เจ้าหน้าที่เจ้าหนี้ | P-04 send modal | Maker | approved → sent |

**Alternative / Exception paths:**
- ไม่อนุมัติ (ใส่เหตุผล) → กลับเป็น draft + เก็บ `approval_history` (append-only) — เห็น badge "ถูกตีกลับ N ครั้ง"
- ยกเลิก draft/pending (ใส่เหตุผล) → cancelled (ไม่ลบใบ · คืนยอดที่กันไว้)
- ใบเดิมถูกลดหนี้เพิ่มระหว่างรออนุมัติจน **มูลค่าที่ลดได้ (dnRoom) ไม่พอ** → ขั้นสุดท้าย re-check ถ้าไม่พอ = อนุมัติไม่ได้ (ให้ตีกลับไปแก้) — *การจ่ายเงินไม่บล็อกอีกต่อไป: เกินคงค้าง = เครดิตคงเหลือ*
- ใบตั้งหนี้จ่ายครบ → ยังออก DN ได้ (คืนของหลังจ่าย) · ส่วนเกินคงค้าง = เครดิตคงเหลือกับผู้ขาย
- approved/sent → "ออกเอกสารแก้ไข" (display-only) — ไม่เปลี่ยนสถานะ/ไม่ถอนยอด (OQ-DN-04)

> **SoD check:** ทุก approval step มี Maker ≠ Approver (บังคับด้วย `canActStep`: `submittedBy === ME` → ซ่อนปุ่มอนุมัติ). ✅
> **HTML alignment:** ทุก step map กับ route/ปุ่มที่มีจริงในไฟล์ HTML — ไม่มี step ลอย.

---

## 6. Data Entity & Fields

### 6.1 Entities
- **debit_note** (header) 1—N **debit_note_line** → (soft-ref) **ap_invoice_line**
- soft-ref: `debit_note.inv → ap_invoice`, `debit_note.rtv → rtv_return` (mock), `debit_note_line.src_line → ap_invoice_line`
- child: `approval_chain` (snapshot ณ ส่ง) · `approval_history` (รอบที่ถูกตีกลับ) · `audit` (append-only) · `attachments`
- derived (display-only): `vendor_credit_ledger` (รวมเครดิตคงเหลือรายผู้ขาย จาก DN approved/sent ที่ vendorCredit > 0)

### 6.2 Header Fields

| # | Field | Label UI | Type | จำเป็น | ค่า/ที่มา | เงื่อนไข |
|--:|---|---|---|:--:|---|---|
| 1 | code | เลขที่ | AUTO (readonly) | ระบบ | ENG-DOC-NUM `DN-YYYY-NNNN` | ออกเมื่ออนุมัติครบ |
| 2 | inv | ใบตั้งหนี้อ้างอิง | LOOKUP | ✓ | ap_open_item | **มีมูลค่าที่ลดได้ (dnRoom) > 0** · approved/posted |
| 3 | partner / billTo / taxId | ผู้ขาย · ที่อยู่ · เลขภาษี | readonly / TEXTAREA | ✓ | ดึงจากใบเดิม | ตามใบกำกับเดิม |
| 4 | vinv | เลขใบกำกับเดิมของผู้ขาย | readonly | ✓ | ดึงจากใบเดิม | อ้างบน DN/PDF |
| 5 | dnDate | วันที่ใบลดหนี้ | DATE | ✓ | วันนี้ | ≥ วันที่ใบกำกับเดิม |
| 6 | reason | เหตุผลการลดหนี้ | DROPDOWN-SINGLE | ✓ | DN reason master (≤7) | กำหนด mode (qty/price) + legal_basis |
| 7 | rtv | ใบคืนสินค้า (RTV) | LOOKUP | ✓ เมื่อ reason=คืนของ | RTV (mock) | ของใบตั้งหนี้เดียวกัน |
| 8 | reasonText | คำอธิบายเหตุผล (พิมพ์บนใบ) | TEXTAREA | ✓ | input | ≥ 10 ตัวอักษร |
| 9 | endbill | ส่วนลดท้ายบิล | TOGGLE + NUMBER + mode(฿/%) | — | input | ยอดสุทธิ ≥0 · ≤ คงค้าง (BR-11) |
| 10 | vendorCn / vendorCnDate | เลขที่ + วันที่ใบลดหนี้จากผู้ขาย | TEXT + DATE | — (บังคับก่อนกลับภาษีซื้อ) | input | คุมเดือนภาษี ภ.พ.30 (BR-14) |
| 11 | note | หมายเหตุภายใน | TEXTAREA | — | input | — |
| 12 | attachments | เอกสารแนบ | FILE (`<input type="file" multiple>`) | — | input | — |

### 6.3 Line Fields (B2 v2 — ล็อกจากใบเดิม)

| Field | Label | Type | เงื่อนไข |
|---|---|---|---|
| item_code / item_name | สินค้า | readonly (lock) | จากบรรทัดใบเดิม (`src_line`) |
| qty | จำนวนลด | NUMBER | ≤ (จำนวนเดิม − ลดแล้ว) · ≤ จำนวนใบ RTV (คืนของ) |
| unit_price | ราคาต่อหน่วยที่ลด | NUMBER | ≤ ราคาเดิม (mode price) |
| vat_mode / vat_pct | VAT | readonly | ตามบรรทัดเดิม (VAT7 ภาษีซื้อ) |
| meta (computed) | จำนวนเดิม · ลดแล้ว · ลดได้อีก · มูลค่าลดได้อีก | display | จาก `lineRoom()`/`lineMeta` |

### 6.4 Computed
- `totals()` → netBefore (ฐานก่อน VAT) · **end-bill:** ebRaw → ebCap (เพดาน grand≥0/≤คงค้าง) → ebAmt → ebVat (แบ่งตามสัดส่วน VAT) · **netVat** (ภาษีซื้อที่ลดจริง ม.86/10) · **grand** (ยอดลดหนี้สุทธิ ≥0)
- **`dnRoom(inv)`** = มูลค่าที่ลดได้ = grand ใบเดิม − ลดหนี้แล้ว(approved/sent) − กันยอด(draft/pending) · **ไม่หัก paid** (BR-13)
- **`dnSplit(inv, grand)`** → applyToAp = min(grand, outstanding) · vendorCredit = max(0, grand − applyToAp) · outstanding
- `invOutstanding` = invGrand − paid − dn_applied

### 6.5 Audit / Snapshot Fields
ทุก entity: createdBy/At · updatedBy/At · approval_chain (snapshot) · approval_history · audit[] (append-only, ไม่มี hard delete) · cancelInfo (by/at/reason) · sentAt/By · vendorCn/vendorCnDate/vendorCnBy/At

### 6.6 ER Diagram
```
ap_invoice ──(1:N soft)──▶ debit_note ──(1:N)──▶ debit_note_line
                               │                        │
rtv_return ──(referenced)──────┘        (soft-ref)──────▶ ap_invoice_line
debit_note ──(N:1)──▶ dn_reason_master · doa_entry(DOA-ACC-DN) · employee(rep)
debit_note ──(effect on approve)──▶ ap_open_item (dn_applied) · vendor_credit_ledger · input_vat_line(negative) · journal_entry(mock)
```

---

## 7. User Stories & Acceptance Criteria

| ID | Story (Given-When-Then) | AC |
|---|---|---|
| US-01 | ในฐานะเจ้าหน้าที่เจ้าหนี้ ต้องเลือกใบตั้งหนี้ที่ยังมีมูลค่าที่ลดได้เพื่อสร้างใบลดหนี้ | (1) เห็นยอดสุทธิ/จ่ายแล้ว/ลดหนี้แล้ว/คงค้างต่อใบ (2) ใบที่ลดเต็มมูลค่าแล้วไม่โผล่ (3) ใบจ่ายครบยังโผล่ (คืนของหลังจ่าย) (4) เลือกแล้วดึงผู้ขาย+บรรทัดอัตโนมัติ |
| US-02 | ต้องระบุเหตุผลจาก master พร้อมคำอธิบาย | (1) เหตุผล=คืนของ ต้องเลือกใบ RTV (2) คำอธิบาย ≥10 ตัว มิฉะนั้นบล็อก |
| US-03 | ต้องปรับจำนวน/ราคาที่ลดภายในเพดานของบรรทัด | (1) จำนวนลด ≤ คงเหลือของบรรทัด (2) ราคาลด ≤ ราคาเดิม (3) เกิน = เตือน/บล็อก |
| US-04 | ต้องใส่ส่วนลดท้ายบิลได้เมื่อจำเป็น | (1) เปิด/ปิด toggle · โหมด ฿/% (2) ยอดสุทธิห้ามติดลบ/เกินคงค้าง (3) ภาษีซื้อลดตามฐานใหม่ |
| US-05 | ต้องออกใบลดหนี้ให้ใบที่จ่ายครบแล้วได้ | (1) เพดาน = มูลค่าที่ลดได้ ไม่หัก paid (2) ส่วนเกินคงค้าง = เครดิตคงเหลือกับผู้ขาย (3) เห็น card แยก หักหนี้ค้าง/เครดิตคงเหลือ |
| US-06 | ต้องส่งอนุมัติตามสายที่แปรตามมูลค่า | (1) เลือกคนครบทุกขั้น (2) tier แปรตามยอดสุทธิ |
| US-07 | ผู้อนุมัติต้องอนุมัติ/ไม่อนุมัติตามสิทธิ์ขั้น | (1) ครบสาย=ออกเลข DN (2) ไม่อนุมัติ=กลับร่าง+เหตุผล (3) ไม่เห็นปุ่มอนุมัติใบตัวเอง |
| US-08 | ต้องกลับภาษีซื้อเมื่อได้รับใบลดหนี้จากผู้ขาย | (1) กรอก vendorCn+วันที่ (2) ไม่มี → ภ.พ.30 "รอเอกสาร" (3) มีครบ → เดือนภาษี = วันที่ได้รับ |
| US-09 | ต้องส่งใบที่อนุมัติแล้วให้ผู้ขาย | (1) สถานะ→ส่งผู้ขายแล้ว (2) เก็บสำเนา PDF |
| US-10 | ต้องเห็นผลกระทบต่อ AP/VAT/บัญชี | (1) แท็บอ้างอิงแสดงคงค้างก่อน/หลัง (2) ภาษีซื้อที่ลด (3) JE จำลอง |

> C05 check: ทุก Story description ไม่มีคำว่า "และ" เป็นตัวเชื่อม action (แต่ละ story = 1 เจตนา). ✅

---

## 8. Status & Lifecycle

```
        A-02 บันทึกร่าง        A-04 ส่งอนุมัติ         A-05 อนุมัติครบสาย       A-07 ส่งผู้ขาย
  (—) ───────────────▶ draft ───────────────▶ pending_approval ───────────────▶ approved ───────────────▶ sent
                         ▲                          │                                │  │
                         │  A-06 ไม่อนุมัติ (เหตุผล)  │                                │  │ (display-only)
                         └──────────────────────────┘                                └──┴─▶ "ออกเอกสารแก้ไข" (ไม่เปลี่ยน state)
        draft/pending ──── A-08 ยกเลิก (เหตุผล) ────▶ cancelled
```

| จาก | Action | ไป | ใคร | เงื่อนไข |
|---|---|---|---|---|
| — | A-02 | draft | officer | — |
| draft | A-04 | pending_approval | officer | grand ≤ dnRoom · DOA resolve · slot ครบ |
| pending_approval | A-05 (ครบสาย) | approved | approver ขั้นสุดท้าย | re-check grand ≤ dnRoom → ออกเลข DN |
| pending_approval | A-06 | draft | approver | ใส่เหตุผล · append history |
| draft/pending | A-08 | cancelled | officer | ใส่เหตุผล |
| approved | A-07 | sent | officer | — |
| approved/sent | บันทึก vendorCn | (คงเดิม) | officer/mgr-acc | กลับภาษีซื้อในเดือนของวันที่ได้รับ |
| approved/sent | ออกเอกสารแก้ไข | (คงเดิม) | officer | display-only · OQ-DN-04 |

Status guards (จาก HTML): cancel เฉพาะ draft/pending (double-guard) · send เฉพาะ approved · submit เฉพาะ draft · edit เฉพาะ draft (เปิดที่ step 2) · approved/sent locked แก้ไข (แต่บันทึก vendorCn ได้).
statusMap: `draft` ฉบับร่าง · `pending_approval` รออนุมัติ · `approved` อนุมัติแล้ว · รอส่ง · `sent` ส่งผู้ขายแล้ว · `cancelled` ยกเลิก.

---

## 9. Business Rules + Validation (พร้อม Tags)

| BR | กติกา | ประเภท | Tag | ที่มา / FN |
|---|---|---|---|---|
| BR-01 | เลือกใบตั้งหนี้ได้เฉพาะ approved/posted ที่ **มีมูลค่าที่ลดได้ (dnRoom) > 0** (ลดเต็มแล้ว ไม่โผล่) | Prevent | FIXED | FN-01,FN-04 |
| BR-02 | ยอด DN สุทธิ ≤ dnRoom ใบอ้างอิง — ตรวจทั้งตอนส่ง (submitGuard) และตอนอนุมัติขั้นสุดท้าย (approveGuard) | Error/Prevent | FIXED | FN-09,FN-17 · LOCK-04 |
| BR-03 | จำนวนลดต่อบรรทัด ≤ จำนวนใบเดิม − ลดแล้ว (ทุกใบรวมกัน) | Error | FIXED | FN-07,FN-08 |
| BR-04 | ราคาลดต่อหน่วย ≤ ราคาเดิม (mode price) | Error | FIXED | FN-06 |
| BR-05 | เหตุผลจาก master + คำอธิบาย ≥ 10 ตัวอักษร | Error | FIXED (ข้อความ) / CONFIGURABLE (master) | FN-05,FN-10 |
| BR-06 | เหตุผล "คืนของ" ต้องอ้างใบ RTV ของใบเดียวกัน · จำนวนไม่เกินที่คืน | Error | FIXED [ASSUMED contract] | FN-05 |
| BR-07 | DOA resolve ตามมูลค่า ณ กดส่ง (freeze snapshot) · ผู้ขอไม่อนุมัติเอง (SoD) | Trigger/Prevent | CONFIGURABLE (ผ่าน DOA กลาง) | FN-11,FN-14 · LOCK-05 |
| BR-08 | เลข DN ออกเมื่ออนุมัติครบสาย (no-gap running number) | Trigger | CONFIGURABLE (doccfg) | FN-12 · LOCK-06 |
| BR-09 | อนุมัติครบ → dn_applied ใบเดิมเพิ่ม + JE (จำลอง: Dr เจ้าหนี้ · Cr รับคืน/ส่วนลด · Cr ภาษีซื้อ) · input_vat_line ติดลบ (กลับตาม vendorCn — ดู BR-14) | Trigger | FIXED (logic) | FN-18 |
| BR-10 | ร่าง/รออนุมัติกันยอด (dn_held) ชั่วคราว — dnRoom หัก held | Trigger | FIXED | FN-08 |
| **BR-11** | **ส่วนลดท้ายบิล (฿/%) หักเพิ่มจากยอดรวม · เพดาน = ยอดสุทธิ ≥0 และ ≤ ยอดคงค้าง (เกิน = บล็อก + เตือนสูงสุด)** | Error/Prevent | CONFIGURABLE | FN-19 · [มติ 2026-09-23] |
| **BR-12** | **ส่วนลดท้ายบิลลดฐานภาษี → คำนวณภาษีซื้อใหม่บนยอดหลังหักส่วนลด (แบ่งตามสัดส่วน VAT) · ภ.พ.30 + JE + PDF สะท้อนภาษีซื้อที่ลดจริง (ม.86/10)** | Trigger | FIXED (logic) | FN-19 · [มติ 2026-09-23 · legal basis ฝั่งซื้อรอ BA รับรอง] |
| **BR-13** | **เพดานลดหนี้ = มูลค่าที่ลดได้ (dnRoom = grand − ลดหนี้แล้ว − กันยอด · ไม่หัก paid) → ใบจ่ายครบออก DN ได้ · ยอดที่เกินคงค้าง = เครดิตคงเหลือกับผู้ขาย (applyToAp = min(grand, คงค้าง)) · ใบที่ลดเต็มมูลค่าแล้วไม่โผล่** | Trigger/Prevent | FIXED (logic) | FN-04,FN-20 · [มติ BA FIX-01 2026-09-23] |
| **BR-14** | **กลับภาษีซื้อ (ภ.พ.30) ได้เมื่อมีเลขที่+วันที่ใบลดหนี้จากผู้ขาย (vendorCn) · เดือนภาษี = เดือนของวันที่ได้รับ · ไม่มี → "รอเอกสาร" (ลด AP ได้แต่ยังไม่ลดภาษีซื้อ) — ม.82/10** | Trigger/Prevent | FIXED (logic) | FN-21 · [มติ BA FIX-02 2026-09-23 · OQ-DN-05] |
| BR-15 | ประวัติ append-only ทุกการกระทำ · ไม่มี hard delete · วันที่เก็บเป็น ค.ศ. | Trigger | FIXED | FN-91 · LOCK-10 |
| BR-16 | ลดหนี้ไม่อ้างใบ = ปิด (tile "ปิดไว้") | Prevent | FIXED | FN-02 · OQ-DN-01 |
| BR-17 | เหตุผลแต่ละตัวพก `legal_basis` (ตามประกาศอธิบดีฯ VAT / ม.86/10 ฝั่งซื้อ) | Warning | CONFIGURABLE | OQ-DN-05 |

**DOA tier matrix (BR-07 · entry `DOA-ACC-DN`, sequential) — คิดจาก `grand` (ยอดสุทธิหลังหักส่วนลดท้ายบิล):**

| Tier | ช่วงมูลค่า (ยอดสุทธิ) | ขั้นอนุมัติ |
|:--:|---|---|
| 1 | 0 – 50,000 | ผจก.จัดซื้อ |
| 2 | 50,000.01 – 300,000 | ผจก.จัดซื้อ → ผจก.บัญชี |
| 3 | > 300,000 | ผจก.จัดซื้อ → ผจก.บัญชี → CFO |

> ⭐ DOA tier คำนวณบน **ยอดสุทธิหลังหักส่วนลดท้ายบิล** (`resolveDoa()` อ่าน `{lines, endbill}` → `totals(s).grand`). ยืนยันตรงกับ HTML. **ช่วงมูลค่า 50k/300k = [ASSUMED — mirror CN]** รอ `DOA-ACC-DN` ยืนยัน (OQ-AP-06).

**Validation messages (verbatim จาก HTML — ส่งต่อ FRD/QA):**
- "ยอดลดหนี้เกินมูลค่าที่ลดได้ของใบตั้งหนี้ (ลดได้ ฿X) — แก้ไขร่างก่อน" (hard-warn/submitGuard)
- "ส่วนลดท้ายบิลเกินยอดที่ลดได้ (สูงสุด ฿X) — แก้ไขร่างก่อน" + helper "ลดได้สูงสุด ฿X"
- "อนุมัติไม่ได้ — มูลค่าที่ลดได้ของ X เหลือ ฿Y น้อยกว่ายอดลดหนี้ (มีใบลดหนี้อื่นได้รับอนุมัติเพิ่มระหว่างรออนุมัติ) · ให้ไม่อนุมัติกลับไปแก้"
- note.warn "รอใบลดหนี้ผู้ขาย" ในแท็บภาษีซื้อ (read-only · ม.82/10)
- field-error: "ระบุคำอธิบายเหตุผลก่อนส่งอนุมัติ" · "เลือกใบคืนสินค้าของใบตั้งหนี้นี้" · "ต้องไม่ก่อนวันที่ใบกำกับเดิม"

### 9.5 สรุประดับความยืดหยุ่น

| Rule | ระดับ | เหตุผล | ที่มา |
|---|---|---|---|
| BR-05 (reason master), BR-17 (legal_basis) | Admin Panel / Rule Mgmt | รายการเหตุผล+เหตุตามกฎหมายเปลี่ยนตามประกาศสรรพากร | 🤖 AI-inferred → **OQ-DN-05** |
| BR-07 (DOA tier), BR-08 (doc numbering) | Rule Management (DOA/doccfg กลาง) | ตั้งค่าที่ engine กลาง ไม่ hardcode | ✅ Stakeholder (LOCK-05/06) |
| BR-11 (end-bill cap %) | Admin Panel | เพดาน/นโยบายส่วนลดปรับได้ | ✅ Stakeholder (มติ 2026-09-23) |
| BR-01,02,03,04,06,09,10,12,13,14,15,16 | FIXED | กฎภาษี/คุมยอด/ตรรกะคำนวณ/เครดิต ไม่ควรเปลี่ยนค่า | ✅ |

> Escalation: BR-05/BR-17 (🤖 + config เหตุผลกฎหมาย) + BR-12/BR-14 (legal basis ฝั่งซื้อ [ASSUMED mirror CN]) → ลง §15 OQ-DN-05 ให้ Finance/BA รับรองก่อนพัฒนา config.

---

## 10. Edge Cases

### 10.1 ที่ user/PREBRIEF ระบุ (☑ ยืนยันแล้ว)
- ☑ EDGE-01 ใบเดิมถูกลดหนี้เพิ่มระหว่างรออนุมัติ → re-check dnRoom ตอนอนุมัติขั้นสุดท้าย (มี DEMO harness พิสูจน์ S-11)
- ☑ EDGE-02 ลดหลายรอบบนใบเดียว → บรรทัดแสดง จำนวนเดิม/ลดแล้ว/ลดได้อีก ถูกต้อง (dn_applied + dn_held)
- ☑ EDGE-03 ใบตั้งหนี้จ่ายครบ → ยังออก DN ได้ · ส่วนเกินคงค้าง = เครดิตคงเหลือกับผู้ขาย (S-13)
- ☑ EDGE-04 ใบที่ลดเต็มมูลค่าแล้ว → ไม่โผล่ใน picker
- ☑ EDGE-05 ยกเลิก draft/pending → คืนยอดที่กันไว้
- ☑ EDGE-06 ไม่อนุมัติ → เก็บ approval_history + badge "ถูกตีกลับ N ครั้ง"
- ☑ EDGE-07 ยังไม่ได้รับใบลดหนี้จากผู้ขาย → ภ.พ.30 "รอเอกสาร" (ลด AP แล้วแต่ยังไม่ลดภาษีซื้อ)

### 10.2 จาก AI Pattern Matching (☐ = แนะนำ — รอ BA/FRD ยืนยันที่ SOW3.7)
- ☐ CL-01 (Calculation) ปัดเศษ VAT/ส่วนลดหลายอัตรา — ยืนยันวิธีปัด (HTML ใช้ปัด 2 ตำแหน่ง, แบ่ง ebVat ตามสัดส่วน)
- ☐ ST-01 (Status) แข่งกันอนุมัติ 2 คนพร้อมกันบนขั้นเดียว (concurrent) — กำหนด lock ระดับ record
- ☐ PD-01 (PDF) เนื้อหาบังคับบนใบลดหนี้ฝั่งซื้อตามสรรพากร (เลขใบเดิม/เหตุผล/ผลต่าง) — ครบใน pdfdoc spec แล้ว
- ☐ FU-01 (File) ชนิด/ขนาดไฟล์แนบที่อนุญาต (มี real file-input แล้ว — ต้อง validate)
- ☐ PM-01 (Permission) การมองเห็นใบข้ามแผนก/สาขา
- ⚠️ CA-01 vendorCn กรอกซ้ำ/เดือนภาษีปิดงวดแล้ว — **กระทบภาษี → ยกเป็น OQ ทันที** (ยืนยัน UX เมื่อเดือนภาษีถูกปิด)
- ⚠️ CA-02 การใช้/ตัดยอดเครดิตคงเหลือกับผู้ขาย (หักใบถัดไป/อายุ/ขอคืน) — **กระทบเงิน → OQ-DN-06** (ปัจจุบัน display-only)

---

## 11. Impact / Regression
New Feature — ไม่มี regression ภายใน feature. ผลกระทบข้ามระบบดู §12.1 (AP Invoice / VAT Report / JE / PV / Vendor Credit).

---

## 12. System Context

### 12.1 Value Stream & Downstream Impact ⭐
**Value Stream:** Procure-to-Pay → AP sub-stream (หลัง AP Invoice/ใบตั้งหนี้ 3-way, ก่อน Payment/PV).
**Upstream:** AP Invoice (F-ACC-APINV, approved/posted, contract `ap_open_item`) · RTV คืนสินค้าจากผู้ขาย (W3-LITE, mock) เป็น trigger สำหรับเหตุคืนของ.

| ปลายทาง (Downstream) | ข้อมูลที่ไหลไป | Trigger | ถ้า DN เปลี่ยน/ยกเลิก → แล้วไงต่อ |
|---|---|---|---|
| AP Invoice / ap_open_item | dn_applied (applyToAp) เพิ่ม → outstanding ลด (ปิดเมื่อ=0) | อนุมัติครบ (approved/sent) | ยกเลิกก่อนอนุมัติ = คืนยอด (held) · หลังอนุมัติยกเลิกไม่ได้ → ออกเอกสารแก้ไข (OQ-DN-04) |
| Vendor Credit Ledger | vendorCredit (ส่วนเกินคงค้าง) → เครดิตคงเหลือรายผู้ขาย | อนุมัติครบ (grand > คงค้าง) | display-only ในรอบนี้ · flow ใช้/ตัดยอด = OQ-DN-06 |
| VAT Report ภ.พ.30 | `input_vat_line` (ค่าลบ) = netVat · เดือน = เดือนของ **vendorCnDate** (ม.82/10) | บันทึก vendorCn ครบ | ไม่มี vendorCn = "รอเอกสาร" (ยังไม่ลงภ.พ.30) — forward-wire |
| Journal Entry (F093) | Dr 2110 เจ้าหนี้ (applyToAp) · Cr รับคืน/ส่วนลด (netBefore) · Cr ภาษีซื้อ (netVat) | อนุมัติครบ | mock [ASSUMED] — forward-wire F093 |
| Payment (PV, W6) | อ่าน outstanding หลังลด | — | ส่วนที่จ่ายครบแล้วคืนของ = เครดิตคงเหลือ (ไม่ refund ใน LITE, OQ-DN-03) |

**ผลกระทบแนวขวาง:** บัญชี (GL ผ่าน JE) · ภาษี (ภ.พ.30 ภาษีซื้อติดลบ) · AP aging/outstanding · เครดิตคงเหลือกับผู้ขาย · ไม่กระทบสต๊อก (สต๊อกอยู่ที่ RTV จริง).

### 12.3 Existing System Reference

| Rule/ฟังก์ชัน | ระดับ | มีอยู่แล้ว? | Reference |
|---|---|:--:|---|
| BR-07 DOA tier | Rule Mgmt (DOA engine) | ⚠️ engine กลาง มีแล้ว · entry `DOA-ACC-DN` ต้องตั้งค่า | DOA_BRIEF_F-ACC-DN |
| BR-08 running number DN | doccfg กลาง | ⚠️ engine มีแล้ว · doc_type DN ต้อง register | DOCCFG_BRIEF_F-ACC-DN |
| notification events | ENG-NOTIFY | ⚠️ มีแล้ว · ต้อง wire dn.issued/dn.sent | NTF_BRIEF_F-ACC-DN |
| 7C consequence | ENG-CSQ | ⚠️ มีแล้ว · register dn.issued→AC(+EC) · dn.vat_applied (OQ-DN-07) | CSQ_BRIEF_F-ACC-DN |
| ap_open_item | AP Invoice (F-ACC-APINV) | ⚠️ contract [ASSUMED] | BRD_F-ACC-APINV §12.1 |
| RTV / JE / PV | W3-LITE / F093 / W6 | ❌ mock ในรอบนี้ | [ASSUMED contract] |

---

## 13. Delivery Phases

- **Phase 1 (Feature Launch):** ตาราง debit_note/line + state machine + config seed (reason master, DOA-ACC-DN entry, doc_type DN) · line editor + end-bill engine + vendor-credit split (dnRoom/dnSplit) + vendorCn gating · guards BR-01..16 · PDF A4 · CSV. ห้าม hardcode ตั้งแต่วันแรก. Reuse: AP ap_open_item, DOA engine, doccfg engine, ENG-NOTIFY, ENG-CSQ.
- **Phase 2 (Admin Panel):** จัดการ DN reason master + เพดานส่วนลดท้ายบิล (BR-05/BR-11) — เมื่อ Finance ยืนยัน OQ-DN-05.
- **Phase 3 (Rule Management):** DOA tier ปรับผ่านหน้า DOA กลาง (BR-07) — dependency DOA engine wire.
- **Phase 4 (Engine/Integration wire):** เชื่อม RTV จริง (W3), JE จริง (F093), VAT Report จริง, PV, **flow ใช้/ตัดยอดเครดิตคงเหลือกับผู้ขาย (OQ-DN-06)** (แทน mock/DEMO harness/display-only).

---

## 14. Dev Requirements Summary ("ใบสั่ง")

### 14.1 Config Foundation ที่ต้องเตรียม
- `dn_reason_master` (code/name/mode qty|price/needRTV/legal_basis) — seed 3 เหตุผล (คืนของ/ราคาเกิน/ของขาด)
- DOA entry `DOA-ACC-DN` (sequential, 3-tier by value — ค่า 50k/300k [ASSUMED mirror CN]) — ตั้งที่ DOA กลาง
- doc_type `DN` running `DN-YYYY-NNNN` (no-gap, ออกตอน final approve) — ที่ doccfg กลาง

### 14.2 ข้อกำหนดจาก Tag (non-FIXED)
- BR-05/BR-17 (reason+legal): อ่านจาก master config — ห้าม hardcode รายการเหตุผล/เหตุตามกฎหมาย
- BR-07 (DOA): resolve จาก DOA engine ตามมูลค่า **grand หลังหักส่วนลดท้ายบิล** · freeze snapshot ณ ส่ง · SoD บังคับ
- BR-08 (number): ใช้ ENG-DOC-NUM.next() ไม่ generate เอง
- BR-11 (end-bill cap): เพดานปรับได้ผ่าน Admin Panel

### 14.3 Edge/Validation ที่ Dev ต้อง handle เป็นพิเศษ
- re-check dnRoom ณ อนุมัติขั้นสุดท้าย (BR-02/approveGuard) — กันลดหนี้เพิ่มระหว่างรอ
- dn_held (draft/pending) กันยอดชั่วคราว — dnRoom หัก held
- **vendor-credit split (BR-13):** applyToAp = min(grand, outstanding) · vendorCredit = ส่วนเกิน · เพดาน = dnRoom (ไม่หัก paid)
- **vendorCn gating (BR-14):** ภาษีซื้อลง ภ.พ.30 เฉพาะเมื่อมี vendorCn+วันที่ · เดือนภาษี = วันที่ได้รับ · ปุ่มบันทึกภายหลังบน approved/sent
- end-bill VAT recompute (BR-12): แบ่ง ebVat ตามสัดส่วน VAT ในยอดรวม
- **ลบ DEMO artifacts ก่อน production:** persona switcher (`data-demo`) · S-11 harness (`demoPay`/dnRoom) · `.demo-only` blocks — HTML ทำเครื่องหมายไว้แล้ว (FIX-04)

### 14.4 WARNING ที่รอข้อสรุป → ดู §15 (ห้ามเริ่มพัฒนาส่วนที่เกี่ยว จนกว่า resolve)
- legal basis การกลับภาษีซื้อ (ม.82/10 ฝั่งซื้อ) = [ASSUMED mirror CN] · flow เครดิตคงเหลือ (OQ-DN-06) · CSQ profile (OQ-DN-07)

### 14.6 Screen Inventory + UI Signals (หยาบ — spec จริงไป FRD)

| # | ชื่อหน้า | route (จาก HTML) | ประเภทหยาบ | ผู้ใช้หลัก | หน้าที่ (business) |
|---|---|---|---|---|---|
| P-01 | รายการใบลดหนี้ผู้ขาย | `#/list` | หน้ารายการ + stat | เจ้าหน้าที่เจ้าหนี้ · ผู้อนุมัติ | ค้นหา/กรอง (สถานะ/เหตุผล/ผู้ขาย) · stat tiles · CSV · row menu · empty state |
| P-02 | สร้างใบลดหนี้ | `#/create` (+`/dup-:id`) | ฟอร์มสร้าง (wizard 5 ขั้น, drawer) | เจ้าหน้าที่เจ้าหนี้ | s1 เลือกแหล่ง (ใบตั้งหนี้; tile "ลดลอย" ปิด) · s2 ข้อมูลหลัก (เหตุผล/RTV/vendorCn) · s3 line+ส่วนลดท้ายบิล · s4 แนบ (real file-input) · s5 ทบทวน+DOA preview |
| P-03 | แก้ไขใบลดหนี้ | `#/edit/:id` | ฟอร์มแก้ไข (draft only, เปิดที่ขั้น 2) | เจ้าหน้าที่เจ้าหนี้ | แก้ร่าง |
| P-04 | รายละเอียดใบลดหนี้ | `#/view/:id` | หน้ารายละเอียด (drawer, 5 tabs) | ทุก role | tabs: รายละเอียด / ใบตั้งหนี้อ้างอิง·ภาษีซื้อ (+เครดิตคงเหลือ+vendorCn) / PDF Preview / ลายเซ็น·อนุมัติ / ประวัติ |
| (modal) | ส่งอนุมัติ (slot picker DOA) · อนุมัติ · ไม่อนุมัติ · ยกเลิก (เหตุผล) · ส่งผู้ขาย · บันทึก vendorCn · ออกเอกสารแก้ไข | overlay | — | ผู้ใช้ตามสิทธิ์ | actions ตาม state |

**สรุปจำนวนหน้า:** ~4 หน้าหลัก (รายการ 1 · wizard สร้าง/แก้ 1 · รายละเอียด 1) + overlay actions. ตรงกับจำนวน route ใน HTML เป๊ะ (`getRoute`: list/create/edit/view) — **ไม่มี HTML-PREBRIEF drift.**

**UI Signals ส่งต่อ FRD:**
- เป็น **Document/Transaction (Pattern Q)** — มี approver + PDF + ลายเซ็น + ประวัติ + เอกสารแนบ (LOCK-01)
- ต้อง **print/PDF** (pdfdoc — A4 ฝั่งซื้อ · FN-92)
- Line editor = **B2 v2** (LOCK-01)
- Iron rules #67.1/#104/#105/#106 = enforce (LOCK-09) — Design Authority ที่ FRD/html-generator-v9
- **หมายเหตุ governance:** hard-warn + max-cap helper ของ end-bill + note.warn "รอใบลดหนี้ผู้ขาย" เป็นข้อความจอที่ BA ควรขยาย allow-list §6 ของ PREBRIEF พร้อมรับ FN-19/FN-21 (ux gate ยืนยันไม่ละเมิด #67.1)

### 14.7 Function Coverage Map (24 FN → BRD section)

| FN | ความสามารถ (ย่อ) | อยู่ที่ section |
|---|---|---|
| FN-01 | เลือกใบตั้งหนี้ค้าง เห็นสุทธิ/จ่าย/ลดแล้ว/คงค้าง | §5 step1 · §6.2 #2 · §9 BR-01 · US-01 |
| FN-02 | tile "ลดหนี้ไม่อ้างใบ" ปิดไว้ | §3.2 · §9 BR-16 · §15 OQ-DN-01 |
| FN-03 | เลือกใบ→ผู้ขาย/เลขใบกำกับเดิม/บรรทัดถูกดึง | §5 step1 · §6.2 #3/#4 · §6.3 · US-01 AC(4) |
| FN-04 | ใบลดเต็มแล้วไม่โผล่ · ใบจ่ายครบยังออกได้ | §3.1(5) · §9 BR-01/BR-13 · §10 EDGE-03/04 · US-01/US-05 |
| FN-05 | คืนของ→เลือก RTV · จำนวนจาก RTV | §5 step2 · §6.2 #7 · §9 BR-06 · US-02 |
| FN-06 | ราคาเกิน: ลดราคา/หน่วย ≤ เดิม | §6.3 · §9 BR-04 · US-03 |
| FN-07 | ของขาด: ลดจำนวนเฉพาะบรรทัด | §6.3 · §9 BR-03 · US-03 |
| FN-08 | ลดหลายรอบ: เดิม/ลดแล้ว/ลดได้อีก | §6.3 meta · §9 BR-03/BR-10 · §10 EDGE-02 |
| FN-09 | เกินคงเหลือ/จำนวน→บล็อก+บอกยอด | §9 BR-02 + validation msgs · US-03 |
| FN-10 | คำอธิบายเหตุผล ≥10 ตัว | §6.2 #8 · §9 BR-05 · US-02 |
| FN-11 | ส่งอนุมัติ สายตามมูลค่า · เลือกคนครบ | §5 step4 · §9 BR-07 + DOA matrix · US-06 |
| FN-12 | อนุมัติครบ→เลข DN-ปี-ลำดับ | §5 step5 · §8 A-05 · §9 BR-08 · US-07 |
| FN-13 | ไม่อนุมัติต้องเหตุผล→ร่าง+รอบก่อน | §5 exception · §8 A-06 · §10 EDGE-06 · US-07 AC(2) |
| FN-14 | ผู้ส่งไม่เห็นปุ่มอนุมัติใบตัวเอง (SoD) | §4 SoD · §5 SoD check · §9 BR-07 · US-07 AC(3) |
| FN-15 | ยกเลิกร่าง/รออนุมัติ+เหตุผล | §5 exception · §8 A-08 · §10 EDGE-05 |
| FN-16 | ส่งให้ผู้ขาย→"ส่งผู้ขายแล้ว" | §5 step7 · §8 A-07 · US-09 |
| FN-17 | เพดานลดลงระหว่างรอ→อนุมัติขั้นสุดท้ายไม่ได้ | §5 exception · §9 BR-02/BR-13 · §10 EDGE-01 |
| FN-18 | แท็บใบอ้างอิง: คงค้างก่อน/หลัง · ภาษีซื้อที่ลด · บัญชี | §9 BR-09 · §12.1 · §14.6 P-04 · US-10 |
| FN-19 | ส่วนลดท้ายบิล: cap net≥0 + VAT ม.86/10 | §3.1(4) · §6.4 · §9 BR-11/BR-12 · US-04 |
| FN-20 | เครดิตคงเหลือกับผู้ขาย (dnRoom · split · card) | §3.1(5) · §6.1/§6.4 · §9 BR-13 · §12.1 · US-05 |
| FN-21 | ภาษีซื้อกลับตาม vendorCn (เดือนภาษี/รอเอกสาร) | §3.1(8) · §5 step6 · §6.2 #10 · §9 BR-14 · §10 EDGE-07 · US-08 |
| FN-90 | ค้นหา/กรอง + empty state | §14.6 P-01 · §18.6 |
| FN-91 | ประวัติ append-only | §7 data behaviour · §9 BR-15 · §16.3 |
| FN-92 | PDF อ้างเลข/วันที่ใบเดิม · ผลต่าง · เหตุผล · ค.ศ. | §3.1(9) · §14.6 · §19 pdfdoc |

> ครบ 24/24 · ไม่มี FN ตกหล่น · หมวด "สิ่งที่ไม่รองรับ" ของ FUNCTION_CHECKLIST → §3.2 Functions Cut.

---

## 15. Open Questions

| OQ | คำถาม | สถานะ | owner |
|---|---|---|---|
| OQ-DN-01 | รายการเหตุผลตามกฎหมายฉบับสุดท้าย + จุดยืน "ลดหนี้ไม่อ้างใบ" (ปัจจุบัน disabled) | ⚠️ รอ | Strike + Finance |
| OQ-DN-03 | เรียกเงินคืนเมื่อจ่ายครบ (refund) — ปัจจุบันไปเป็นเครดิตคงเหลือกับผู้ขายแทน | ⚠️ รอ | Strike + Finance |
| OQ-DN-04 | เส้นทาง "ออกเอกสารแก้ไข"/ยกเลิกหลังอนุมัติ (ปัจจุบัน display-only) | ⚠️ รอ | Strike |
| OQ-DN-05 | legal basis การกลับภาษีซื้อ ม.82/10 ฝั่งซื้อ (ยืนยันยึดวันที่ได้รับใบลดหนี้ผู้ขาย) — **[ASSUMED mirror CN]** | ⚠️ รอ | Policy/Finance + BA |
| OQ-DN-06 | flow ใช้/ตัดยอด **เครดิตคงเหลือกับผู้ขาย** (หักใบถัดไป/ขอคืนเงิน/อายุ) · เจ้าของ F097 หรือ AP | ⚠️ รอ | Strike + AP |
| OQ-DN-07 | CSQ profile — `dn.issued` vs `dn.vat_applied` event เดียว/แยก | ⚠️ รอ | Strike + Finance |
| OQ-AP-06 | role-ids จริง (officer-ap / mgr-purchase / mgr-acc [ASSUMED]) + DOA tier boundaries (50k/300k) | ⚠️ รอ | Policy Center |
| — AP Invoice contract | ยืนยัน contract `ap_open_item` (invGrand/paid/dn_applied) | [ASSUMED] | AP team |

> หมายเหตุ semantic reversal (BA FIX-01): FN-04/S-13/S-11 กลับด้านจาก mirror CN — **ใบตั้งหนี้จ่ายครบ ยังออก DN ได้** (คืนของหลังจ่าย → เครดิตคงเหลือ) · การจ่ายเงินไม่บล็อกเพดานอีกต่อไป (เพดาน = dnRoom ไม่หัก paid).

---

## 16. Security & Compliance

### 16.1 Preset
**P4 — Financial/Payment (16 controls)** — เหตุผล: กระทบยอดเจ้าหนี้/ภาษีซื้อ/GL โดยตรง + มีสายอนุมัติตามมูลค่า.

### 16.2 Applicable Standards
COSO (Maker/Checker/Approver + SoD) · Thai Revenue Code ม.86/10 (ออกใบลดหนี้อ้างใบกำกับเดิม) · ม.82/10 (เดือนภาษีตามวันที่ได้รับใบลดหนี้ผู้ขาย) · PDPA (ข้อมูลผู้ขาย) · Audit trail (append-only).

### 16.3 Control Checklist (สำคัญ)
- ✓Must SoD: ผู้ส่งไม่อนุมัติใบตัวเอง (BR-07)
- ✓Must Approval-by-value ผ่าน DOA (BR-07)
- ✓Must Immutable audit / no hard delete (BR-15)
- ✓Must Snapshot approval_chain ณ ส่ง (freeze)
- ✓Must Number integrity no-gap ตอน final approve (BR-08)
- ✓Must Amount ceiling ≤ dnRoom ทั้งส่ง+อนุมัติ (BR-02/BR-13)
- ✓Must Input-VAT reversal gated by vendorCn (BR-14) — กันกลับภาษีซื้อก่อนมีเอกสาร
- ○Opt Field-level lock (approved/sent) — enforced (ยกเว้น vendorCn)
- ○Opt Attachment type/size validation (Edge FU-01, รอ FRD)

### 16.4 Risk Statement
| Risk | Mitigated by |
|---|---|
| R-A ลดหนี้เกินมูลค่าที่ลดได้ → เจ้าหนี้/งบผิด | BR-02 (re-check ส่ง+อนุมัติ), BR-03/04, BR-10 held, BR-13 dnRoom |
| R-B ผู้ขออนุมัติเอง → ทุจริต | BR-07 SoD |
| R-C กลับภาษีซื้อก่อนมีใบลดหนี้ผู้ขาย → ค่าปรับสรรพากร | BR-14 vendorCn gating, "รอเอกสาร" state |
| R-D คืนของหลังจ่าย → เครดิตตกหล่น | BR-13 vendor credit ledger (display-only) + OQ-DN-06 flow |
| R-E แก้ยอด/ลบใบย้อนหลัง | BR-15 append-only, "ออกเอกสารแก้ไข" แทนยกเลิก |

---

## 17. Health Check

### 17.1 SLA
- หน้ารายการ/สร้าง p95 < 3s
- เวลาอนุมัติเฉลี่ย (ส่ง→ครบสาย) ≤ 1 วันทำการ (owner: ผู้อนุมัติแต่ละขั้น)

### 17.2 Control Points
map จาก §16.3: SoD gate · amount-ceiling gate (ส่ง+อนุมัติ, dnRoom) · number-issue gate (final approve) · vendorCn gate (ก่อนลงภ.พ.30) · audit-write ทุก transition.

### 17.3 KPI

| KPI | ประเภท | Target | คู่ §2.3 |
|---|---|---|---|
| KPI-Q1 DN เกินมูลค่าที่ลดได้ | Quality/Compliance | 0 | ✔ |
| KPI-C2 ภาษีซื้อกลับก่อนมี vendorCn | Compliance | 0 | ✔ |
| KPI-S1 เวลาอนุมัติเฉลี่ย | Speed | ≤ 1 วัน | ✔ |
| KPI-C1 DN ไม่มีเหตุผล/ไม่อ้างใบ | Compliance | 0 | ✔ |
| KPI-V1 ปริมาณ DN/เดือน | Volume | ~80 | ✔ |

### 17.4 Threshold
- ยอดลดหนี้/เดือน เทียบยอดซื้อ → เกิน X% = alert (นโยบาย Finance, รอค่า)
- DN ตีกลับ > N ครั้ง/ใบ = flag ทบทวนคุณภาพงาน
- DN approved ที่ vendorCn ค้าง > N วัน = flag ติดตามใบลดหนี้จากผู้ขาย

### 17.5 Throughput
Baseline ~80 ใบ/เดือน · Stress point: การ re-check dnRoom พร้อมกันหลายใบต่อใบตั้งหนี้เดียว (concurrent — ดู Edge ST-01).

---

## 18. Monitoring

- **18.1 Reports:** Performance (เวลาอนุมัติ) · Closing (ภาษีซื้อที่ลด/เดือน สำหรับ ภ.พ.30) · Anomaly (DN เกินมูลค่าที่ลดได้/vendorCn ค้าง/ตีกลับบ่อย) · Transaction (รายการ DN)
- **18.2 Dashboard Widgets:** stat tiles ในหน้ารายการ (รออนุมัติ + ยอด · ลดหนี้เดือนนี้ · ฉบับร่าง · **ภาษีซื้อที่ลดเดือนนี้**) — อ้าง KPI §17.3
- **18.3 Performance Report:** สาย DOA ที่ค้างนาน per tier
- **18.4 Closing Report:** สรุป netVat รายเดือน (เฉพาะที่มี vendorCn) → กระทบ ภ.พ.30 · รายการ "รอเอกสาร"
- **18.5 Anomaly Report:** DN ที่ block เพราะเกินมูลค่าที่ลดได้ · ใบตีกลับ · vendorCn ค้างนาน · เครดิตคงเหลือกับผู้ขายค้าง
- **18.6 Transaction Report:** DN ทั้งหมด + สถานะ + ยอด (applyToAp/vendorCredit) + ภาษีซื้อที่ลด (= CSV export)

---

## 19. Declarations (รอบนี้)

| ท่อ | ใช้ | สรุป |
|---|:--:|---|
| **doa** | ✅ | `DOA-ACC-DN` sequential 3-tier by value (50k/300k [ASSUMED]) — tier บนยอดสุทธิหลังส่วนลด · slot picker · SoD |
| **ntf** | ✅ | events: `dn.issued`→ผู้สร้าง+AP · `dn.sent`→ผู้ขาย · (`doa_pending`/`doa_result` มาจาก DOA engine — ห้ามประกาศซ้ำ) |
| **csq** | ✅ | `dn.issued`→AC (ลด AP + JE) (+EC) · `dn.vat_applied` (เมื่อมี vendorCn) → AC ภาษีซื้อ · DC จาก DOA engine — ห้ามซ้ำ · (event เดียว/แยก = OQ-DN-07) |
| **doccfg** | ✅ | doc_type `DN` running `DN-YYYY-NNNN` no-gap ตอน final approve |
| **pdfdoc** | ✅ | A4 print (thai-doc-pdf-generator) ฝั่งซื้อ (template.html + sample.pdf + print-spec.md · DN_print-spec.md) |

> DECLARATION_INDEX: DIVERGENCE = ไม่มี (chip ตรง detect ทุกท่อ · plan chip F097 = doa/ntf/csq/doccfg/pdfdoc).
> ⚠️ กติกา WF-01 C3.10: `*-declaration` skills รันเฉพาะเมื่อผู้ใช้สั่ง — BRD บันทึกไว้เพื่อ traceability เท่านั้น ไม่ได้เรียกเอง.

---

## 19b. AI Review Report (Quality Gate)

```
BRD: BRD-F-ACC-DN — Debit Note (ใบลดหนี้ผู้ขาย) · New Feature · 2026-09-23
CHECKLIST:
✅ C01 Business objective วัดผลได้ (§2.3 มี baseline/target/แหล่งวัด)
✅ C02 User roles ครบ (§4)   ✅ C05 Story ไม่มีคำว่า "และ"
✅ C10 ทุก rule ที่มีตัวเลข/เงื่อนไข ติด Tag (§9)
✅ C13 Edge cases ครบหมวด (§10.1 BA + 10.2 AI)
✅ C18 WARNING ทุกข้อมีแผน/owner (§15)   ✅ C19 §14 ใบสั่งครบ
✅ C20 Scope Lock §3.4 ครบ 10 LOCK · ไม่มี drift เงียบ
✅ C21 Value Stream §12.1 upstream+downstream ตอบ "แล้วไงต่อ" ทุกแถว
✅ C22 ตัวชี้วัด §2.3 มีคู่ §17.3 ครบ
✅ C23 §9.5 marker 🤖/✅ ครบ · 🤖 config เหตุผล + legal basis → OQ-DN-05
✅ PE01 COSO ทุก step (§5)   ✅ PE02 SoD (Maker≠Approver)
✅ PE03 Security preset P4 + controls   ✅ PE04 SLA/KPI/Threshold (§17)
✅ PE05 Cross-section coverage (BC↔Edge, Control↔Health, Metric↔Monitor)

FN COVERAGE: 24/24 (FN-01..21 + FN-90/91/92) ปรากฏใน §5/§7/§9/§14.6 ครบ
SCENARIO COVERAGE: S-01..S-16 ครบ (§5 journey + exception + §10 edge)

SUMMARY: ผ่าน 23/23 + PE 5/5
สถานะ: ✅ APPROVED — พร้อมเข้า frd-generator-v6
หมายเหตุ: มี 7 OQ + 1 ASSUMED contract เปิดค้าง (ไม่บล็อก BRD — ต้อง resolve ก่อนพัฒนา Phase ที่เกี่ยว)
  โดยเฉพาะ OQ-DN-05 (legal basis ภาษีซื้อ ม.82/10 = [ASSUMED mirror CN]) · OQ-DN-06 (flow เครดิตคงเหลือ) · OQ-DN-07 (CSQ profile)
```

**Next step:** BRD พร้อมส่งเข้า `frd-generator-v6` (step 7 · ใช้ BRD นี้ + HTML FINAL + declaration briefs).
</content>
</invoke>
