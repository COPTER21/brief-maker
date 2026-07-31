# PURCHASE CONFIG — AI CONTEXT BIBLE
**Feature:** F-PURCH-CFG-001 ตั้งค่าการจัดซื้อ (Purchase Configuration) · **Module:** จัดซื้อ (Purchase / P2P) · **CUBE NATIVE ERP (2BSimple)**
**Version:** 1.0 (2026-06-05) · **Status:** BA pipeline complete (HTML + BRD-PURCH-CFG-001 + FRD FULL pack + QA) — dev not started

---

## 0. วิธีใช้ไฟล์นี้ (READ ME FIRST — for AI)

> ไฟล์นี้คือ **single source of truth ของ "กติกาที่ตั้งค่าได้" ในงานจัดซื้อ** สำหรับให้ AI อ่านเป็น context ตอนสร้าง feature ปลายน้ำ (PR, Comparison/CP, PO และอื่น ๆ ใน P2P).
>
> **เมื่อสร้าง feature ที่เกี่ยวกับจัดซื้อ ให้ยึดกฎเหล่านี้:**
> 1. **ห้าม hardcode กติกา** — ทุก behavior ที่ตั้งค่าได้ต้อง**อ่านจาก effective config** (ดู §3) ไม่ใช่ฝังในโค้ด
> 2. **เคารพ boundary** — อะไรที่ "อยู่โมดูลอื่น" (§8) ห้ามทำซ้ำ/ตั้งค่าเองใน feature จัดซื้อ
> 3. **เคารพ locked decisions D01–D15** (§9) — เป็น business rule ตายตัว ห้ามทำเป็น toggle/option
> 4. ถ้า requirement ใหม่ขัดกับไฟล์นี้ → **หยุดแล้วถามก่อน** อย่าเดาเอง
>
> **TL;DR:** Purchase Config เป็นชั้น flag กลางที่บอกว่า "งานจัดซื้อต้องมี/บังคับขั้นไหนบ้าง". PR/CP/PO อ่านค่าพวกนี้แล้ว gate flow ของตัวเอง.

---

## 1. สิ่งที่ Purchase Config "เป็นเจ้าของ" vs "อ่านจากที่อื่น" (BOUNDARY MAP)

| หมวด | Purchase Config เป็นเจ้าของ? | ที่อยู่จริง |
|---|---|---|
| เปรียบเทียบราคา (มี/บังคับ/ขั้นต่ำ/threshold/เกณฑ์ชนะ) | ✅ ใช่ | Purchase Config |
| เส้นทางเอกสาร (require PR ก่อน PO) | ✅ ใช่ | Purchase Config |
| ประเภทการชำระ — เปิดใช้ + ค่าเริ่มต้น (inherit→PO) | ✅ ใช่ (แต่ "รายการ" ดึงจาก Payment Term) | Purchase Config |
| ฟิลด์บังคับ PR (item/qty/need_by/quote) | ✅ ใช่ | Purchase Config |
| การเลือกผู้ขาย (approved-only / pricelist autofill) | ✅ ใช่ | Purchase Config |
| รูปแบบเลขที่เอกสาร (PR/CP/PO) | ✅ ใช่ | Purchase Config |
| **เงื่อนไขการชำระจริง (Payment Term master)** | ❌ อ่านอย่างเดียว | **Finance** |
| **บังคับอ้างใบปลดอายัด / release-ref** | ❌ อ่านอย่างเดียว | **Budget Config (#4)** — key `release_require_unlock_ref` |
| **ผู้มีอำนาจอนุมัติตามวงเงิน (สายอนุมัติ)** | ❌ ส่ง amount ให้ตัดสิน | **DOA (Policy Center)** |
| **รับของ / QC inline / Putaway / over-receipt tolerance** | ❌ ไม่เกี่ยว | **Inventory Config** |
| **Direct Payment (จ่ายตรง bypass PR/PO/GRN)** | ❌ ไม่เกี่ยว | **Finance/Accounting — เปิดที่ AP Invoice** |
| **ข้อมูล Vendor / Vendor Price List** | ❌ อ่านอย่างเดียว | **Master Data** |

---

## 2. CONFIG KEYS CATALOG (ทุก key ที่ feature ปลายน้ำต้องรู้)

> ตาราง `T_purchase_config` มี **1 แถวต่อ tenant** · ทุก field = Data Classification **Internal**

### 2.1 Comparison (เปรียบเทียบราคา / RFQ)
| key | type | default | ความหมาย |
|---|---|---|---|
| `enable_comparison` | boolean | true | ระบบมีขั้นเปรียบเทียบราคา (CP) หรือไม่ |
| `comparison_required` | boolean | true | บังคับทำ CP หรือไม่ (ถ้า enable=false → ค่านี้ไม่มีผล) |
| `comparison_min_quotes` | int | 3 | จำนวนผู้เสนอราคาขั้นต่ำเมื่อบังคับ CP |
| `comparison_threshold_amount` | numeric | 50000 | บังคับ CP เฉพาะยอด ≥ ค่านี้ (ต่ำกว่า = ข้ามได้แม้ตั้งบังคับ) |
| `comparison_award_rule` | enum | lowest | `lowest`=เลือกราคาต่ำสุดอัตโนมัติ · `manual`=เลือกเอง (ต้องระบุเหตุผลถ้าไม่ใช่ต่ำสุด) |

### 2.2 Flow Gating (เส้นทางเอกสาร)
| key | type | default | ความหมาย |
|---|---|---|---|
| `require_pr_before_po` | boolean | true | PO ต้องอ้าง PR ก่อน · ถ้า false = เปิด PO ลอยได้ |

### 2.3 Payment Types (เปิดใช้ + ค่าเริ่มต้น · inherit→PO)
| key | type | default | ความหมาย |
|---|---|---|---|
| `pt_enabled` | jsonb | ทุกตัว=true | ประเภทที่เปิดใช้ `{postpay,prepay,deposit,installment,partial,credit}` |
| `default_payment_type` | enum | postpay | ค่าเริ่มต้นตอนเปิด PO (ต้อง ∈ ที่ pt_enabled=true) |
| `deposit_default_pct` | numeric | 30 | % มัดจำเริ่มต้น (Deposit) — inherit→PO ปรับได้ราย PO (D08) |
| `installment_default_terms` | int | 3 | จำนวนงวดเริ่มต้น (Installment) — inherit→PO ปรับ %/งวด/due ได้ (D09) |
| `credit_default_days` | int | 30 | วันเครดิตเริ่มต้น (Credit) — due = วันที่ออก + N |

> **รายการ payment types มาจาก Payment Term master (Finance)** — Purchase Config แค่เลือกว่าจะ "เปิดใช้" อันไหน + ตั้งค่าเริ่มต้น แล้ว **inherit ไปเป็นค่าเริ่มต้นตอนเปิด PO** (เลือกจริง + ปรับราย PO ได้)

### 2.4 PR Document
| key | type | default | ความหมาย |
|---|---|---|---|
| `pr_mandatory.item` | boolean | true | บังคับระบุสินค้า/รายการใน PR |
| `pr_mandatory.qty` | boolean | true | บังคับระบุจำนวน |
| `pr_mandatory.need_by` | boolean | false | บังคับระบุวันที่ต้องการ |
| `quote_attachment_required` | boolean | false | บังคับแนบใบเสนอราคา |

> ⚠️ **ไม่มี** `cost_center` / `budget_account` ใน PR mandatory — ดู §6 (มากับใบปลดอายัด)

### 2.5 Vendor Sourcing
| key | type | default | ความหมาย |
|---|---|---|---|
| `require_approved_vendor_only` | boolean | true | PR/PO เลือกได้เฉพาะ vendor สถานะ active/approved |
| `vendor_pricelist_autofill` | boolean | true | autofill ราคาจาก **Vendor Price List** เมื่อเลือกผู้ขาย+สินค้า |

### 2.6 Document Numbering → ดู §4 (มีตารางแยก `T_doc_numbering`)

---

## 3. EFFECTIVE CONFIG CONTRACT (วิธีที่ feature ปลายน้ำอ่าน config)

> **PR/CP/PO ต้องอ่าน config ผ่าน endpoint นี้เสมอ — real-time, read-only, forward-only**

- **GET** `/api/purchase/config/effective`
- คืน config keys ทั้งหมดใน §2 **+ resolve ค่าข้ามโมดูลให้แล้ว:**
  - `release_require_unlock_ref` (จาก Budget Config #4) — บังคับอ้างใบปลดอายัดใน PR หรือไม่
  - `payment_term_list` (จาก Finance Payment Term master) — รายการประเภทที่ใช้ได้
- **forward-only:** config มีผลกับเอกสารที่สร้าง**ใหม่** เท่านั้น — เอกสารเดิมไม่เปลี่ยนเมื่อ config เปลี่ยน
- **อ่านสดทุกครั้ง** ที่เปิดฟอร์ม/validate (อย่า cache ค้าง)

```
// pseudo: PR feature ตอนเปิดฟอร์ม
cfg = GET /api/purchase/config/effective
if (cfg.release_require_unlock_ref) → PR ต้องมีช่อง "เลขใบปลดอายัด (UNLK)" + บังคับกรอก
if (!cfg.enable_comparison) → PR สามารถไป PO ได้เลย (ไม่ต้องผ่าน CP)
if (cfg.pr_mandatory.item) → validate item required
```

---

## 4. NUMBERING ENGINE CONTRACT — ENG-DOCNUM-01 (doc-number-generator)

> Engine reusable · **ทุกโมดูลที่ออกเลขเอกสารต้องเรียก engine นี้ ไม่สร้างเลขเอง**

### 4.1 ตาราง `T_doc_numbering` (ต่อ tenant × doc_type)
| field | ความหมาย |
|---|---|
| `doc_type` | `PR` / `CP` / `PO` (ขยายได้) |
| `prefix` | คำนำหน้า เช่น `PR` |
| `digits` | จำนวนหลักเลขรัน เช่น 4 → `0001` |
| `reset_cycle` | `none` / `yearly` / `monthly` |
| `next_no` | เลขรันถัดไป |
| `last_reset_period` | `YYYY` หรือ `YYYY-MM` (กันรีเซ็ตซ้ำ) |

### 4.2 รูปแบบเลข
`{prefix}-{ปีพ.ศ.}-{next_no zero-padded ตาม digits}` → ตัวอย่าง: `PR-2569-0232`

### 4.3 Engine methods
| method | พฤติกรรม | ใช้เมื่อ |
|---|---|---|
| `issue(doc_type)` | **atomic** (SELECT FOR UPDATE): ตรวจ reset → format เลข → **increment next_no** → return | ตอน **create เอกสารจริง** (PR/CP/PO) ภายใน transaction |
| `peek(doc_type)` | เหมือน issue แต่ **ไม่ increment** | แสดง preview ในหน้าตั้งค่า / preview ก่อนบันทึก |

### 4.4 กฎสำคัญ (ห้ามพลาด)
- **issue ต้อง atomic** (FOR UPDATE) → กันเลขซ้ำเมื่อสร้างเอกสารพร้อมกัน (concurrent)
- **reset ครั้งเดียวต่อรอบ** — เทียบ period ปัจจุบันกับ `last_reset_period`; yearly เทียบ `YYYY`, monthly เทียบ `YYYY-MM`; `none`=ไม่รีเซ็ต
- เรียก `issue` **ใน transaction เดียวกับการ create เอกสาร** — ถ้า rollback เลขต้องไม่หาย/ไม่ข้าม (ใช้ค่าที่ commit จริง)

---

## 5. BUDGET LINKAGE — ใบปลดอายัด (UNLK) [สำคัญมากสำหรับ PR]

> **กฎ:** ศูนย์ต้นทุน (cost_center) + รหัสงบ (budget_account) **ไม่ได้กรอกแยกใน PR** — มัน**มากับใบปลดอายัด (UNLK)** ที่ออกจากงบแผนก (F-BGT-REQ-001)

- เลขใบปลดอายัดรูปแบบ: **`UNLK-{ปีพ.ศ.}-{NNNN}`** เช่น `UNLK-2569-0014`
- 1 ใบปลดอายัด carry: `cost_center (dept)` + `budget_account (code/รหัสงบ)` + `bp_version (ก้อนงบ)` + `amount`
- **บังคับอ้าง UNLK ใน PR หรือไม่** = อ่านจาก **Budget Config** key `release_require_unlock_ref` (ผ่าน effective config §3)
  - ถ้า `true` → PR **ต้อง** ref เลข UNLK (block ถ้าไม่กรอก) · cost center + รหัสงบ ดึงมาจาก UNLK อัตโนมัติ
  - ถ้า `false` → สร้าง PR **ได้เลย** โดยไม่ผูกงบ (ไม่มีช่อง UNLK บังคับ)
- **3-stage budget tracking** (ฝั่งงบ): ปลดอายัด → ผูกจัดซื้อ (PR/PO = committed) → จ่ายแล้ว (PV = paid) → คงเหลือคืนได้. PR/PO ที่ ref UNLK = ส่วน "committed" ของงบ.

---

## 6. ENTITIES (ตารางที่ feature ปลายน้ำควรรู้)
| ตาราง | เจ้าของ | feature อื่นเกี่ยวยังไง |
|---|---|---|
| `T_purchase_config` (1 แถว/tenant) | Purchase Config | อ่านผ่าน effective config (§3) — อย่า query ตรง |
| `T_doc_numbering` (tenant×doc_type) | Purchase Config | เรียกผ่าน ENG-DOCNUM-01 (§4) — อย่า update ตรง |
| `T_purchase_config_log` (audit) | Purchase Config | append-only — feature อื่นไม่ยุ่ง |
| `M_payment_term` | Finance | source ของ payment types |
| `T_budget_config` | Budget #4 | `release_require_unlock_ref` |
| `T_budget_txn` (UNLK) | Budget #6 | PR ref เลข UNLK จากที่นี่ |
| `M_vendor_price_list` | Master | autofill ราคา (ถ้า `vendor_pricelist_autofill`) |

---

## 7. LOCKED DECISIONS D01–D15 (ห้ามทำเป็น config/toggle — เป็น business rule ตายตัว)

| # | Decision |
|---|---|
| D01 | Payment term เลือกที่ **PO เท่านั้น** — PR/Comparison ไม่มี payment term (เริ่มที่ PO wizard step 2) |
| D02 | GRN trigger ตาม payment type — Full Prepay/Deposit = รอ PV confirm ก่อน · ที่เหลือ = GRN ทันที |
| D03 | รับไม่ครบ = **Partial เสมอ** — ไม่มี exception |
| D04 | Auto-close PO เมื่อ GRN cumulative = PO qty (manual close = กด 'ไม่รอ' ที่ GRN เท่านั้น) |
| D05 | เปลี่ยน payment type **ไม่ได้หลัง PO approve** — ต้อง cancel + สร้าง PO ใหม่ |
| D06 | **3-Way Match บังคับทุกกรณี** (PO eff = GRN = Invoice net) — ไม่มี bypass ยกเว้น Direct Payment |
| D07 | Close PO Balance trigger ที่ **GRN เท่านั้น** (บันทึก audit log) |
| D08 | Deposit: % inherit จาก config · ปรับได้ที่ PO |
| D09 | Installment: ตาราง %/งวด/due inherit จาก config · ปรับได้ที่ PO |
| D10 | Partial Delivery: **GRN qty กำหนดยอดจ่าย** (GRN qty = Invoice qty = PV amount ต่อ round) |
| D11 | Credit overdue: แสดง badge เตือน · **ไม่ block** PO ใหม่/GRN |
| D12 | Unit Conversion (Subcontract) = lock payment_type=full_postpay อัตโนมัติ |
| D13 | Payment Voucher 2 types (`payment`/`refund`) ใน document เดียว — ไม่สร้าง Refund Voucher แยก |
| D14 | **CN ต้องมาจาก vendor เท่านั้น** — ต้องแนบไฟล์ CN ของ vendor เป็น ref เสมอ |
| D15 | Installment (ส่งรอบเดียว แบ่งจ่าย N งวด) ≠ Partial Delivery (ส่งหลายรอบ จ่ายตาม GRN) — คนละ type |

---

## 8. BEHAVIOR MATRIX — config เปลี่ยน flow ยังไง (สำหรับ PR/CP/PO)

| สถานการณ์ config | เส้นทางที่ feature ต้องทำ |
|---|---|
| `enable_comparison=false` | PR → PO ตรง (ไม่มีขั้น CP) |
| `enable_comparison=true` + `comparison_required=false` | PR → (CP optional) → PO · ผู้ใช้เลือกข้ามได้ |
| `enable_comparison=true` + `comparison_required=true` | PR → CP (≥ `comparison_min_quotes` เจ้า) → PO · บังคับ |
| ยอด < `comparison_threshold_amount` | ข้าม CP ได้แม้ตั้งบังคับ |
| `require_pr_before_po=false` | เปิด PO ได้โดยไม่ต้องมี PR |
| `release_require_unlock_ref=true` (Budget Config) | PR ต้อง ref UNLK + บังคับกรอก |
| `release_require_unlock_ref=false` | สร้าง PR ได้เลย ไม่ผูกงบ |
| `require_approved_vendor_only=true` | dropdown vendor แสดงเฉพาะ active/approved |
| `vendor_pricelist_autofill=true` | เลือก vendor+item → autofill ราคาจาก Vendor Price List |

---

## 9. PER-CONSUMER INTEGRATION GUIDE

### 9.1 PR (ใบขอซื้อ · F-PR-001)
อ่าน effective config แล้ว:
- ฟิลด์บังคับ: ตาม `pr_mandatory.*` + `quote_attachment_required`
- ช่อง UNLK: แสดง/บังคับตาม `release_require_unlock_ref` (จาก Budget Config) — cost center+รหัสงบ ดึงจาก UNLK ที่เลือก (ไม่กรอกเอง)
- vendor: กรองตาม `require_approved_vendor_only` · ราคา autofill ตาม `vendor_pricelist_autofill`
- เลขที่: `ENG-DOCNUM-01.issue('PR')` ตอน create
- **ไม่มี** payment term ใน PR (D01)
- ปุ่มไปต่อ: ถ้า `enable_comparison` → ไป CP ; ไม่งั้น → ไป PO (ตาม behavior matrix §8)

### 9.2 Comparison / CP (เปรียบเทียบราคา · F-CMP-001)
- มีอยู่ก็ต่อเมื่อ `enable_comparison=true`
- บังคับ ≥ `comparison_min_quotes` เจ้า เมื่อ `comparison_required=true` และยอด ≥ `comparison_threshold_amount`
- เลือกผู้ชนะตาม `comparison_award_rule` (`lowest` auto / `manual` ต้องระบุเหตุผลถ้าไม่ใช่ต่ำสุด)
- เลขที่: `ENG-DOCNUM-01.issue('CP')`
- **ไม่มี** payment term ใน CP (D01)

### 9.3 PO (ใบสั่งซื้อ · F-PO-001)
- ต้องมี PR ก่อนถ้า `require_pr_before_po=true`
- **payment type เลือกที่นี่** (D01, wizard step 2) — ตัวเลือก = `pt_enabled` · ค่าเริ่มต้น = `default_payment_type` · มัดจำ/งวด/วันเครดิต = inherit จาก `deposit_default_pct`/`installment_default_terms`/`credit_default_days` (ปรับได้ราย PO ตาม D08/D09)
- payment **term** จริง (เงื่อนไข) มาจาก Finance Payment Term master
- approval: ส่ง amount ให้ **DOA** (ไม่ตัดสินเอง)
- เลขที่: `ENG-DOCNUM-01.issue('PO')`
- หลัง PO: flow GRN/3-way/PV เป็นไปตาม payment type (ดู D02/D06 + P2P cheat sheet)

---

## 10. GLOSSARY / IDs
- **F-PURCH-CFG-001** = Purchase Configuration feature · prefix `PCFG`
- **ENG-DOCNUM-01** = doc-number-generator engine (issue/peek)
- **UNLK-{พ.ศ.}-{NNNN}** = เลขใบปลดอายัดงบ (จาก Budget #6) carry cost_center+budget_account
- **effective config** = config ที่ resolve ค่าข้ามโมดูลแล้ว (อ่านผ่าน `GET /api/purchase/config/effective`)
- **forward-only** = config เปลี่ยนมีผลกับเอกสารใหม่เท่านั้น
- **CP** = Comparison/เปรียบเทียบราคา · **PR** = ใบขอซื้อ · **PO** = ใบสั่งซื้อ · **PV** = Payment Voucher · **GRN** = รับของ · **CN** = ใบลดหนี้ · **RTV** = คืนผู้ขาย · **DOA** = Delegation of Authority (สายอนุมัติ)

---

## 11. SOURCE & CHANGELOG
- **อ้างอิงจาก:** BRD-PURCH-CFG-001 + FRD_F-PURCH-CFG-001_Pack (FULL 9 ไฟล์) + prototype `purchase-config.html` + P2P Payment Cheat Sheet v1.0 (D01–D15)
- **boundaries ที่ stakeholder ยืนยัน:** release-ref→Budget Config · approval→DOA · payment term→Finance · GRN/QC/Putaway→Inventory Config · Direct Payment→AP Invoice (Finance/Accounting) · payment types ดึงจาก Payment Term
- v1.0 (2026-06-05): ฉบับแรก — สร้างจาก BA pipeline ที่เสร็จครบ

> **หมายเหตุสถานะ:** ไฟล์นี้สะท้อน "การออกแบบ (BA)" ที่เสร็จแล้ว — feature จริงบน tracking sheet ยังไม่ deploy. เมื่อ dev สร้างจริงและมีการเปลี่ยน contract ให้ **อัปเดตไฟล์นี้ให้ตรง** ก่อนใช้เป็น context ต่อ.
