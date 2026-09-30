# BASELINE — F-WH-GRN · GRN รับของ (เทียบ ERP standard)

> feature-review-standard · 2026-09-10 · module Warehouse · wave W3P
> เทียบกับ: SAP S/4HANA MM (MIGO / inbound delivery) · Odoo 17 Inventory+Quality · Dynamics 365 SCM (Product receipt / Arrival journal) · NetSuite (Item Receipt) · ERPNext (Purchase Receipt)
> **สถานะการค้น: `[PARTIAL ONLINE BASELINE]`** — WebSearch 2 query คืนเฉพาะหัวข้อ/URL ไม่มี snippet เนื้อหา (sandbox) → ยืนยันได้เฉพาะ "มีอยู่จริงในมาตรฐาน" ของ over/under-delivery tolerance + delivery-completed indicator + quality inspection stock · รายละเอียดกลไกที่เหลือมาจากความรู้ ERP ของ runner เอง ไม่ใช่การอ้างข้อความจากเว็บ

**Query ที่ยิง (2/3):**
1. `goods receipt note GRN ERP standard features over-delivery tolerance quality inspection quarantine SAP Odoo`
2. `SAP MIGO goods receipt partial delivery over-delivery tolerance underdelivery quality inspection stock GR/IR clearing account`

**Sources (หัวข้อที่ได้กลับมา — ใช้ยืนยันการมีอยู่ของ concept เท่านั้น):**
- [Applying Tolerances and the Delivery Completed Indicator — SAP Learning](https://learning.sap.com/courses/inventory-management-and-physical-inventory-in-sap-s-4hana/applying-tolerances-and-the-delivery-completed-indicator)
- [Over-delivery/under-delivery tolerances — SAP Community](https://community.sap.com/t5/enterprise-resource-planning-blog-posts-by-members/over-delivery-under-delivery-tolerances/ba-p/13522481)
- [SAP Goods Receipt: Process, Checks and Invoice Matching — Doxis](https://www.doxis.com/en/blog/goods-receipt-checks)
- [Executing Expected Goods Receipts Processes — SAP Learning (EWM)](https://learning.sap.com/courses/processes-in-sap-s-4hana-ewm/executing-expected-goods-receipts-processes)
- [Odoo Quality: Control Points, Alerts, and Inspection Routines](https://www.dasolo.ai/blog/odoo-apps-9/odoo-quality-control-points-alerts-and-inspection-routines-568)
- [Goods Receipt Note (GRN) Explained — ProcurementAIAgents](https://procurementaiagents.com/blog/goods-receipt-note)
- [Goods Received Note (GRN) Explained 2026 — WareIQ](https://wareiq.com/resources/blogs/goods-received-note-grn/)

---

## 1. GRN คืออะไรในมาตรฐาน (สรุปร่วม 5 ระบบ)

GRN / Goods Receipt / Product Receipt / Item Receipt / Purchase Receipt = **เอกสารยืนยันการรับของจริงเทียบกับ PO** — เป็นจุดที่ (ก) ปริมาณจริงถูกบันทึกกลับไปที่ PO line (ข) **stock movement เกิดขึ้นจริง** (ค) เกิดขาบัญชี GR/IR (Goods Receipt / Invoice Receipt clearing) และ (ง) เป็นขาที่ 2 ของ **3-way match** (PO ↔ GRN ↔ Invoice)

| ระบบ | ชื่อเอกสาร | จุดเด่นที่เกี่ยว |
|---|---|---|
| SAP S/4HANA MM | Goods Receipt (MIGO / MB01) | over/under-delivery tolerance ต่อ PO item · "Delivery Completed" indicator ปิดยอดค้างด้วยมือ · movement type 101 · GR blocked stock (103/105) · quality inspection stock |
| Odoo | Receipt (stock.picking type incoming) | รับบางส่วน = backorder อัตโนมัติ · Quality Check point ที่ receipt · Lot/Serial · scrap/quarantine location |
| D365 SCM | Arrival journal → Product receipt | over/under delivery % ต่อบรรทัด · registration ก่อน post · quarantine order |
| NetSuite | Item Receipt | รับหลายรอบต่อ PO · inspection ผ่าน quality mgmt SuiteApp · bin/lot |
| ERPNext | Purchase Receipt | over-receipt allowance % (global + ต่อ item) · rejected qty + **rejected warehouse** (= quarantine ในตัว) · quality inspection ผูก receipt |

---

## 2. Must-have (M-01..M-16) — ถ้าไม่มี = GRN ไม่ใช่ GRN

| # | ความสามารถ | มาตรฐานที่ยืนยัน | CUBE รอบนี้ |
|---|---|---|---|
| M-01 | รับของ **อ้าง PO** — ดึง line มาตั้งต้น (สินค้า/จำนวนสั่ง/หน่วย/คงเหลือรับ) | ทั้ง 5 | ✅ in scope |
| M-02 | **รับบางส่วน** — ยอดรับ < สั่ง แล้ว PO ค้างรับ + เปิด GRN รอบถัดไปได้ | ทั้ง 5 (Odoo=backorder) | ✅ in scope |
| M-03 | **รับครบ** → ปิด PO line + ปิดใบ PO อัตโนมัติ | ทั้ง 5 | ✅ in scope |
| M-04 | **over-delivery tolerance %** — รับเกินได้ในกรอบที่ตั้งไว้ นอกกรอบ = บล็อก | SAP (ยืนยันจาก source) · D365 · ERPNext | ✅ in scope — `OQ-PO-01 [ASSUMED]` default 0% |
| M-05 | **under-delivery / delivery-completed** — ปิดยอดค้างรับด้วยมือแม้ยังไม่ครบ | SAP "Delivery Completed" (ยืนยันจาก source) | ⚠️ อยู่ฝั่ง **PO short-close (S-12)** ไม่ทำซ้ำที่ GRN — ต้องระบุใน PREBRIEF ว่าเป็นเจตนา |
| M-06 | **QC / inspection ตอนรับ** — แยกของที่ไม่ผ่านออกจาก stock ขายได้ | SAP quality inspection stock · Odoo Quality Check · ERPNext rejected warehouse | ✅ in scope — `OQ-GRN-01 [ASSUMED]` quarantine location |
| M-07 | **stock movement เกิดจริงตอน post** + ระบุคลัง/location ปลายทาง | ทั้ง 5 | ✅ in scope (ระดับ location · bin ละเอียด = Putaway W3Q) |
| M-08 | **movement/journal แก้ไม่ได้ ยกเลิกด้วย reversal** | SAP cancel = 102 · ERPNext cancel+amend | ✅ in scope — append-only (GOLDEN_RULES §4) |
| M-09 | **GR/IR (2-way ก่อน invoice)** — ตั้งพักหนี้ตอนรับ ล้างตอน invoice | SAP GR/IR clearing (ยืนยันจาก source Doxis) · D365 · NetSuite | ⚠️ **note ใน BRD เท่านั้น** — JE = mock + `TODO: JE posting` (W5) |
| M-10 | รองรับ **หลาย GRN ต่อ 1 PO** และ 1 GRN ครอบหลาย PO line | ทั้ง 5 | ✅ หลาย GRN ต่อ PO = in scope · หลาย PO ต่อ 1 GRN = ดู N-08 |
| M-11 | **เลขที่เอกสารรัน + เอกสารพิมพ์ได้** | ทั้ง 5 | ✅ doccfg `GRN-YYYY-NNNN` + pdfdoc |
| M-12 | **ข้อมูลการส่งจริง**: เลขที่ใบส่งของผู้ขาย · วันที่รับจริง · ผู้ส่ง/ทะเบียนรถ · ผู้รับของ | ทั้ง 5 | ✅ in scope |
| M-13 | **เอกสารแนบ** (ใบส่งของ/ใบชั่ง/รูปสภาพสินค้า) | ทั้ง 5 | ✅ in scope (Pattern Q landing) |
| M-14 | **audit trail ทุก event** | ทั้ง 5 | ✅ append-only |
| M-15 | **ยกเลิก/กลับรายการ GRN** พร้อมคืนยอดรับสะสมที่ PO | ทั้ง 5 | ✅ in scope — reversal เท่านั้น |
| M-16 | **บล็อกการรับจาก PO ที่ยังไม่ส่ง / ยกเลิก / short-closed** | ทั้ง 5 | ✅ in scope (BR-14 ของ PO) |

**สรุป: must-have 16 ข้อ — in scope เต็ม 13 · in scope แบบมีเงื่อนไข 3 (M-05 อยู่ฝั่ง PO · M-09 mock · M-07 ระดับ location)**

---

## 3. Nice-to-have (N-01..N-10) — มาตรฐานมี CUBE ยังไม่ทำรอบนี้

| # | ความสามารถ | ใครมี | มติรอบนี้ |
|---|---|---|---|
| N-01 | Lot / Batch / Serial + วันหมดอายุ ตอนรับ | ทั้ง 5 | **backlog** — ยังไม่มี Lot master ในเลนนี้ |
| N-02 | Bin/location putaway ละเอียด + putaway strategy | SAP EWM · D365 · NetSuite | **backlog → F-WH-PUTAWAY (W3Q)** |
| N-03 | Barcode / RF scanning ตอนรับ | ทั้ง 5 | backlog |
| N-04 | ASN / Inbound delivery (ผู้ขายแจ้งล่วงหน้า) | SAP · D365 | backlog — ยังไม่มี vendor portal |
| N-05 | Landed cost ผูกกับ receipt | ทั้ง 5 | **backlog → F069 (W4)** |
| N-06 | Costing/valuation ตอนรับ (FIFO/Avg) | ทั้ง 5 | **backlog → F070 (W4)** |
| N-07 | Quality inspection plan/checklist มีขั้นตอนของตัวเอง (sampling, spec) | SAP QM · Odoo Quality | รอบนี้ = ผล QC ระดับบรรทัด (ผ่าน/ไม่ผ่าน/จำนวนที่ไม่ผ่าน + เหตุผล) ไม่มี inspection plan |
| N-08 | 1 GRN รับข้าม PO หลายใบพร้อมกัน | SAP · D365 | **ไม่รองรับรอบนี้** — 1 GRN = 1 PO (ลดความซับซ้อนของการ sync สถานะกลับ) |
| N-09 | รับของแบบไม่มี PO (unplanned receipt) | SAP (movement 501) · Odoo | **ไม่รองรับรอบนี้** — ของเข้าโดยไม่มี PO ให้ใช้ Stock Adjustment (W3Q) |
| N-10 | Subcontracting / consignment receipt | SAP · D365 | backlog |

---

## 4. Out of scope (ยืนยันว่าตั้งใจไม่ทำ)

- JE / GL posting จริง → **W5** (รอบนี้ mock + `TODO: JE posting`) — แต่ **ต้องมี GR/IR note ใน BRD** ตาม CHECKLIST
- 3-way match กับ Invoice (ขาที่ 3) → ฝั่ง AP (W5)
- RTV คืนของ → **F-PUR-RTV** (ตัวถัดไปในเลน) — GRN แค่พาของไป quarantine
- Putaway bin/location → **F-WH-PUTAWAY** (W3Q)
- Cycle count / physical inventory → นอก pack (OQ-STK-01)
- DOA อนุมัติการรับของ → **ไม่มีโดยเจตนา** (CONTEXT_PACK §2.2 — รับของไม่ใช่การอนุมัติ)

---

## 5. Gap vs CUBE — สิ่งที่ PREBRIEF ต้องเติมให้ครบ

| G | ช่องว่างที่เห็น | ต้องเติมที่ |
|---|---|---|
| **G-01** | มาตรฐานมี **under-delivery / delivery-completed** ที่ตัวเอกสารรับของ แต่ CUBE ย้ายไปเป็น short-close ฝั่ง PO → ต้องเขียนให้ชัดว่าเป็นเจตนา + GRN ต้องแสดง "ยอดค้างรับหลังใบนี้" ให้ผู้ใช้ตัดสินใจได้ | PREBRIEF scenario รับบางส่วน + §7 data behaviour |
| **G-02** | tolerance รับเกิน — มาตรฐานตั้งได้ทั้ง % และจำนวน และมีทั้ง over/under · CUBE รอบนี้ = **% ต่อบรรทัด · config ต่อ tenant · default 0%** → ต้องมาร์ก `[ASSUMED OQ-PO-01]` + ระบุพฤติกรรมตอนเกิน (บล็อก ไม่ใช่เตือน) | scenario รับเกิน + BR + line editor |
| **G-03** | QC ไม่ผ่าน — มาตรฐานมีทั้ง reject ที่ประตู (ไม่รับเข้าเลย) และ quarantine/rejected warehouse · CUBE เลือก **quarantine เสมอ** (`OQ-GRN-01`) → ต้องเขียนว่า movement ยังเกิด (เข้า quarantine) และของออกจาก quarantine ได้ทางเดียวคือ **RTV** | scenario QC + state machine + movement |
| **G-04** | **GR/IR** — มาตรฐาน post บัญชีตอนรับ · CUBE รอบนี้ไม่ post → PREBRIEF/BRD ต้องมี note ว่าใบนี้ "จะ" ก่อ GR/IR entry อะไร (Dr สินค้าคงคลัง / Cr GR-IR clearing) เพื่อให้ W5 ต่อได้ + `TODO: JE posting` | PREBRIEF §7/§9 + BRD section GR/IR |
| **G-05** | **ยกเลิก GRN** — มาตรฐานมี reversal doc · CUBE ต้องระบุว่า reversal คืนยอดรับสะสมที่ PO และดันสถานะ PO กลับ (`closed → partially received`) ได้จริง และ movement เดิมไม่ถูกลบ | scenario ยกเลิก + state machine PO sync |
| **G-06** | **บรรทัดประเภทบริการ** (ค้างมาจาก OQ-PO-06) — มาตรฐานใช้ service entry sheet แยก · CUBE รอบนี้ต้องตอบ: GRN รับบรรทัดบริการไหม | PREBRIEF §3.2 + OQ ใหม่ |
| **G-07** | **ผู้รับของ = คนจริง** — ไม่มี DOA แต่ต้องมีผู้รับผิดชอบที่ระบุตัวได้ (ใช้ในแท็บลายเซ็นของ Pattern Q) | PREBRIEF §3.1 + tab ลายเซ็น |

**สรุป: must-have 16 ตัว ครอบได้ 16 (3 ตัวมีเงื่อนไขตามกติกา forward-wire/แบ่ง feature) · gap ที่ต้องเติมใน S1 = 7 ข้อ (G-01..G-07)**
