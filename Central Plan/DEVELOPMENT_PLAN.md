# Development Plan — CUBE 4.0 Trade Core

> จาก `workflow_graph.json` **v4.0.0** (2026-07-24) · feature-only · 41 features เรียงลำดับ (30 ต้องทำใหม่ · 11 มีแล้ว)
> **Rules** = จำนวน golden rules (ในวงเล็บ = severity `block` ที่ต้อง map เป็น AC ใน BRD)
> ลำดับมาจาก dependency `data`/`config` — สลับได้ภายใน phase เดียวกัน แต่ห้ามข้าม phase

## Feature Index — ทุก feature ในแผนที่ (เช็คความครบ)

จัดตาม flow · ตัวเลขในวงเล็บคือ wave ที่ต้องทำ

| กลุ่ม | Features |
|---|---|
| **Masters & Config** | Product (W1) · UOM (W1) · BOM (W1) · COA (W1) · Product Catalog (W1) · Sales Channel (W1) · Payment Term (W1) · Vendor (W1) · Vendor Price List (W1) · Warehouse (W1) · Warehouse Config (W1) · Purchase Config (W1) · Customer Segment (W1) · Price List (W1) · Sales Configuration (W1) |
| **Inventory / Stock** | Inventory (W2) · Stock Adjustment (W2) · Stock Reservation (W2) · Stock Transfer (W2) · Stock Count (W2) |
| **Warehouse Operations** | Goods Receipt (GRN) (W5) · Putaway (W5) · Picking (W6) · Packing (W6) · Delivery Note (W6) · Return to Vendor (W8) · Sales Return (RMA) (W7) |
| **Purchase (ขาซื้อ)** | PR (W4) · CP (W4) · PO (W4) |
| **Sales (ขาขาย)** | Prospect (W3) · Customer Master (W3) · Quotation (W3) · Sales Order (W3) · Promotion (W3) |
| **Accounting / Finance** | AP Invoice (3-Way Match) (W7) · AR Invoice / Tax Invoice (W7) · Credit / Debit Note (W8) · GR/IR Accrual (W8) · Receipt Voucher (W8) · Payment Voucher (W9) |

## Phase 0 — Rework existing (ENH ไม่ใช่ feature ใหม่)
ต้องทำก่อน Phase 1 เพราะ OQ-G04 / G12 ย้อนกระทบของที่เสร็จแล้ว

| # | Task | Existing feature | Reason |
|---|---|---|---|
| 0.1 | Add lot / serial / expiry dimension | F-INVENTORY-BALANCE | OQ-G12=a บังคับทั้งเส้น — schema ต้องรองรับก่อนทุก movement |
| 0.2 | Add damage reason code + GL mapping | F-INVENTORY-ADJUSTMENT | OQ-G05=b ใช้ ADJ แทนเอกสาร Scrap |
| 0.3 | Reserve on confirm + partial line status | F-SALES-ORDER | OQ-G04=a จองทันที · OQ-G09=b ค้างส่งเป็น status |
| 0.4 | Add receiving tolerance fields (over/under %) | F-PRODUCT-MASTER *(boundary)* | OQ-G01a — tolerance resolve 3 ชั้น ต้องมีชั้น material master |
| 0.5 | Complete BRD / FRD / Testcase | F-CUSTOMER · F-QUOTATION · F-SALES-ORDER · F-PROMOTION | มีแค่ HTML — Phase 2 จะอ้าง SO เป็น contract |

## Phase 1 — Masters & Config · 15 features
ต้องเสร็จก่อนทุกอย่าง — Product / UOM / Warehouse เป็นเงื่อนไขของ Inventory

| # | Wave | Feature ID | Feature | ไทย | Domain | Status | Depends on | Rules |
|---|---|---|---|---|---|---|---|---|
| 1 | W1 | `F-PRODUCT` | **Product** | ข้อมูลสินค้า/วัสดุ | Master | ✅ มีแล้ว | — | 4 (4) |
| 2 | W1 | `F-UOM` | **UOM** | หน่วยวัด | Master | ✅ มีแล้ว | — | 2 (2) |
| 3 | W1 | `F-BOM` | **BOM** | สูตร/ชุดสินค้า | Master | ✅ มีแล้ว | — | 2 (1) |
| 4 | W1 | `F-COA` | **COA** | ผังบัญชี | Accounting | ต้องทำ | — | 3 (3) |
| 5 | W1 | `F-PRODUCT-CATALOG` | **Product Catalog** | แค็ตตาล็อกสินค้า | Master | ต้องทำ | — | 2 (1) |
| 6 | W1 | `F-SALES-CHANNEL` | **Sales Channel** | ช่องทางการขาย | Sales | ต้องทำ | — | 2 (1) |
| 7 | W1 | `F-PAYMENT-TERM` | **Payment Term** | เงื่อนไขการชำระเงิน | Master | ต้องทำ | — | 2 (2) |
| 8 | W1 | `F-VENDOR` | **Vendor** | ข้อมูลผู้ขาย | Purchase | ต้องทำ | — | 1 (1) |
| 9 | W1 | `F-VENDOR-PRICE-LIST` | **Vendor Price List** | บัญชีราคาผู้ขาย | Purchase | ต้องทำ | F-VENDOR | 1 (0) |
| 10 | W1 | `F-WAREHOUSE` | **Warehouse** | คลังและตำแหน่งจัดเก็บ | Warehouse | ต้องทำ | — | 2 (2) |
| 11 | W1 | `F-WAREHOUSE-CONFIG` | **Warehouse Config** | ตั้งค่าคลังสินค้า | Warehouse | ต้องทำ | — | 5 (5) |
| 12 | W1 | `F-PURCHASE-CONFIG` | **Purchase Config** | ตั้งค่าจัดซื้อ | Purchase | ✅ มีแล้ว | — | 1 (1) |
| 13 | W1 | `F-CUSTOMER-SEGMENT` | **Customer Segment** | กลุ่มลูกค้า | Sales | ต้องทำ | — | 1 (0) |
| 14 | W1 | `F-PRICE-LIST` | **Price List** | บัญชีราคาขาย | Sales | ต้องทำ | F-PRODUCT-CATALOG · F-SALES-CHANNEL | 1 (0) |
| 15 | W1 | `F-SALES-CONFIG` | **Sales Configuration** | ตั้งค่าการขาย | Sales | ต้องทำ | — | 1 (0) |

## Phase 2 — Inventory Core · 5 features
ยอดคงคลัง + งานที่กระทำต่อสต็อกโดยตรง (เพิ่ม / ปรับ / จอง / ย้าย / นับ)

| # | Wave | Feature ID | Feature | ไทย | Domain | Status | Depends on | Rules |
|---|---|---|---|---|---|---|---|---|
| 16 | W2 | `F-INVENTORY` | **Inventory** | สินค้าคงคลัง | Inventory | ✅ มีแล้ว | F-STOCK-RESERVATION · F-WAREHOUSE | 11 (11) |
| 17 | W2 | `F-STOCK-ADJUSTMENT` | **Stock Adjustment** | ปรับยอดคงคลัง | Inventory | ✅ มีแล้ว | F-COA | 6 (5) |
| 18 | W2 | `F-STOCK-RESERVATION` | **Stock Reservation** | การจองสินค้า | Inventory | ต้องทำ | — | 3 (3) |
| 19 | W2 | `F-STOCK-TRANSFER` | **Stock Transfer** | การโอนย้ายสินค้า | Warehouse | ต้องทำ | F-WAREHOUSE | 2 (1) |
| 20 | W2 | `F-STOCK-COUNT` | **Stock Count** | การนับสินค้า | Warehouse | ต้องทำ | F-WAREHOUSE | 3 (2) |

## Phase 3 — Front Documents · 8 features
เอกสารต้นทาง 2 ฝั่ง — Sales front (Prospect→SO) และ Purchase (PR→CP→PO)

| # | Wave | Feature ID | Feature | ไทย | Domain | Status | Depends on | Rules |
|---|---|---|---|---|---|---|---|---|
| 21 | W3 | `F-PROSPECT` | **Prospect** | ผู้สนใจ (ลีด) | Marketing | ✅ มีแล้ว | — | 2 (1) |
| 22 | W3 | `F-CUSTOMER` | **Customer Master** | ข้อมูลลูกค้า | Sales | ✅ มีแล้ว | F-CUSTOMER-SEGMENT · F-PAYMENT-TERM | 1 (1) |
| 23 | W3 | `F-QUOTATION` | **Quotation** | ใบเสนอราคา | Sales | ✅ มีแล้ว | F-PRICE-LIST · F-PRODUCT-CATALOG | 2 (0) |
| 24 | W3 | `F-SALES-ORDER` | **Sales Order** | คำสั่งขาย | Sales | ✅ มีแล้ว | F-SALES-CHANNEL · F-SALES-CONFIG | 4 (3) |
| 25 | W3 | `F-PROMOTION` | **Promotion** | โปรโมชัน | Sales | ✅ มีแล้ว | — | 1 (0) |
| 26 | W4 | `F-PR` | **PR** | ใบขอซื้อ | Purchase | ต้องทำ | — | 3 (2) |
| 27 | W4 | `F-CP` | **CP** | ใบเทียบราคา | Purchase | ต้องทำ | F-PR · F-VENDOR-PRICE-LIST | 2 (1) |
| 28 | W4 | `F-PO` | **PO** | ใบสั่งซื้อ | Purchase | ต้องทำ | F-CP · F-PAYMENT-TERM · F-PR · F-VENDOR | 6 (5) |

## Phase 4 — Warehouse Operations · 5 features
งานคลังจริง — Inbound (รับ+เก็บ) และ Outbound (หยิบ+แพ็ค+ส่ง)

| # | Wave | Feature ID | Feature | ไทย | Domain | Status | Depends on | Rules |
|---|---|---|---|---|---|---|---|---|
| 29 | W5 | `F-GOODS-RECEIPT` | **Goods Receipt (GRN)** | ใบรับสินค้า | Warehouse | ต้องทำ | F-PO · F-WAREHOUSE · F-WAREHOUSE-CONFIG | 12 (11) |
| 30 | W5 | `F-PUTAWAY` | **Putaway** | จัดเก็บเข้าตำแหน่ง | Warehouse | ต้องทำ | — | 3 (3) |
| 31 | W6 | `F-PICKING` | **Picking** | การหยิบสินค้า | Warehouse | ต้องทำ | — | 3 (3) |
| 32 | W6 | `F-PACKING` | **Packing** | การแพ็คสินค้า | Warehouse | ต้องทำ | F-PICKING | 2 (1) |
| 33 | W6 | `F-DELIVERY-NOTE` | **Delivery Note** | ใบส่งของ | Warehouse | ต้องทำ | F-PACKING | 4 (3) |

## Phase 5 — Billing, Exceptions & Money · 8 features
ตั้งหนี้ 2 ฝั่ง · คืนของ · เอกสารแก้กลับ · จ่าย/รับเงิน

| # | Wave | Feature ID | Feature | ไทย | Domain | Status | Depends on | Rules |
|---|---|---|---|---|---|---|---|---|
| 34 | W7 | `F-AP-INVOICE` | **AP Invoice (3-Way Match)** | ใบแจ้งหนี้เจ้าหนี้ | Accounting | ต้องทำ | F-COA · F-GOODS-RECEIPT · F-PAYMENT-TERM · F-PO | 15 (15) |
| 35 | W7 | `F-AR-INVOICE` | **AR Invoice / Tax Invoice** | ใบแจ้งหนี้/ใบกำกับภาษี | Accounting | ต้องทำ | F-COA · F-DELIVERY-NOTE · F-PAYMENT-TERM | 9 (7) |
| 36 | W7 | `F-SALES-RETURN` | **Sales Return (RMA)** | รับคืนจากลูกค้า | Warehouse | ต้องทำ | F-DELIVERY-NOTE | 3 (3) |
| 37 | W8 | `F-RETURN-TO-VENDOR` | **Return to Vendor** | คืนของผู้ขาย | Warehouse | ต้องทำ | — | 4 (4) |
| 38 | W8 | `F-CREDIT-DEBIT-NOTE` | **Credit / Debit Note** | ใบลดหนี้/เพิ่มหนี้ | Accounting | ต้องทำ | — | 19 (19) |
| 39 | W8 | `F-RECEIPT-VOUCHER` | **Receipt Voucher** | ใบสำคัญรับ | Finance | ต้องทำ | F-AR-INVOICE · F-COA | 2 (1) |
| 40 | W8 | `F-GRIR-ACCRUAL` | **GR/IR Accrual** | บัญชีพักรับของ-รอใบแจ้งหนี้ | Accounting | ต้องทำ | F-COA | 3 (2) |
| 41 | W9 | `F-PAYMENT-VOUCHER` | **Payment Voucher** | ใบสำคัญจ่าย | Finance | ต้องทำ | F-AP-INVOICE · F-COA · F-CREDIT-DEBIT-NOTE | 6 (6) |

## Notes
- ⚠️ **Phase 1 ห้ามข้าม** — `F-PRODUCT` + `F-UOM` + `F-WAREHOUSE` ไม่ครบ = เปิดใช้ Inventory ไม่ได้ (GR-INV-08, GR-WH-02)
- ⚠️ **F-STOCK-RESERVATION** ต้องมาก่อน `F-PICKING` ในเฟสเดียวกัน — เป็นเจ้าของ `allocated` แต่ผู้เดียว
- **F-INVENTORY เพิ่มสินค้าเข้าคลังได้เอง** — สร้าง balance ใหม่ต่อสินค้า×ตำแหน่งผ่านเอกสาร Stock Adjustment เท่านั้น ห้ามสร้างยอดลอย · lot/serial/expiry tracking รวมอยู่ในตัวแล้ว
- **ไม่มี Direct Payment / AR Ledger เป็น feature แยก** — จ่ายตรงเป็นโหมดบนหัว AP Invoice · ยอดลูกหนี้คำนวณจากเอกสารใน AR Invoice
- **Credit/Debit Note ใบเดียว** ครอบ 4 แบบ (CN/DN × เจ้าหนี้/ลูกหนี้) แยกด้วย doc_type + party
- ⚠️ **F-GOODS-RECEIPT** หนักสุดทั้งแผนที่ (9 rules / 8 block) — รับเกิน/ขาด · QC · รับลอย · reverse · accrual · Close Balance รวมที่เดียว
- **F-AP-INVOICE** รวม 3-Way Match ไว้ในตัวแล้ว (ไม่มี engine แยก)
- **Cascade reversal (XR-13)**: reverse GRN หลัง match → ยกเลิก AP Invoice + กลับรายการ GR/IR พร้อมกัน · PV ที่จ่ายแล้วเป็นเส้นหยุด — feature 4 ตัวนี้ต้องออกแบบ reversal ร่วมกันตั้งแต่ Phase 2
- ทุก feature: อ่าน `NODE_BRIEFS/<id>.md` ก่อนเริ่ม · rule severity=block ทุกข้อต้องกลายเป็น AC · edge ออกทุกเส้นต้องมี hook ใน HTML

## Domain summary

| Domain | Features to build |
|---|---|
| Warehouse (11) | F-WAREHOUSE · F-WAREHOUSE-CONFIG · F-STOCK-TRANSFER · F-STOCK-COUNT · F-GOODS-RECEIPT · F-PUTAWAY · F-PICKING · F-PACKING · F-DELIVERY-NOTE · F-SALES-RETURN · F-RETURN-TO-VENDOR |
| Sales (8) | F-SALES-CHANNEL · F-CUSTOMER-SEGMENT · F-PRICE-LIST · F-SALES-CONFIG · F-CUSTOMER · F-QUOTATION · F-SALES-ORDER · F-PROMOTION |
| Purchase (6) | F-VENDOR · F-VENDOR-PRICE-LIST · F-PURCHASE-CONFIG · F-PR · F-CP · F-PO |
| Master (5) | F-PRODUCT · F-UOM · F-BOM · F-PRODUCT-CATALOG · F-PAYMENT-TERM |
| Accounting (5) | F-COA · F-AP-INVOICE · F-AR-INVOICE · F-CREDIT-DEBIT-NOTE · F-GRIR-ACCRUAL |
| Inventory (3) | F-INVENTORY · F-STOCK-ADJUSTMENT · F-STOCK-RESERVATION |
| Finance (2) | F-RECEIPT-VOUCHER · F-PAYMENT-VOUCHER |
| Marketing (1) | F-PROSPECT |
