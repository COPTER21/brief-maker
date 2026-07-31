# Build Order — CUBE 4.0 Trade Core

> `workflow_graph.json` **v4.0.0** (2026-07-24) — 46 nodes · 94 edges · 161 golden rules
> บังคับลำดับด้วย dependency `data` / `config` เท่านั้น — `trigger` / `reversal` ไม่บล็อกการ build

## Wave 0 — มีแล้ว / นอก scope

| Feature | Status | Artifacts |
|---|---|---|
| `F-INVENTORY` Inventory | existing | BRD_inventory-stock-by-location.md · FRD Pack 9 files · stock-by-location.html |
| `F-STOCK-ADJUSTMENT` Stock Adjustment | existing | 00_BRIEF.md (ENH pack) · 05_FRD_DELTA.md · stock-by-location.html v2 |
| `F-PROSPECT` Prospect | existing | BRD_core_marketing_prospect.md v2.0 · FRD_core_marketing_prospect.md · core-marketing-prospect.html |
| `F-CUSTOMER` Customer Master | existing | sales-module.html (H only) |
| `F-QUOTATION` Quotation | existing | sales-module.html (H only) |
| `F-SALES-ORDER` Sales Order | existing | sales-module.html (H only) |
| `F-PROMOTION` Promotion | existing | sales-module.html (H only) |
| `F-PURCHASE-CONFIG` Purchase Config | existing | — |
| `F-PRODUCT` Product | existing | ✓ · ✓ · ✓ |
| `F-UOM` UOM | existing | ✓ · ✓ · ✓ |
| `F-BOM` BOM | existing | ✓ · ✓ · ✓ |
| `F-GL-POSTING` GL Posting | existing | sales-module.html (H) |
| `F-APPROVAL-DOA` Approval Authority (DOA) | boundary | — |
| `F-USER-ACCESS` User Access (Policy Center) | boundary | — |
| `F-NOTIFICATION` Notification | boundary | — |
| `F-BUDGET-CONTROL` Budget Control | boundary | — |

## Waves

| Wave | Features | เหตุผล | ปลดล็อก |
|---|---|---|---|
| **1** | `F-PRODUCT` · `F-UOM` · `F-BOM` · `F-COA` · `F-PRODUCT-CATALOG` · `F-SALES-CHANNEL` · `F-PAYMENT-TERM` · `F-VENDOR` · `F-VENDOR-PRICE-LIST` · `F-WAREHOUSE` · `F-WAREHOUSE-CONFIG` · `F-PURCHASE-CONFIG` · `F-CUSTOMER-SEGMENT` · `F-PRICE-LIST` · `F-SALES-CONFIG` | Masters & Config ทั้งหมดต้องมาก่อน — Product / UOM / Warehouse เป็นเงื่อนไขของ Inventory · COA เป็นเงื่อนไขของทุก posting · Payment Term / Catalog / Channel เป็นฐานของเอกสารซื้อ-ขาย | เปิดใช้ Inventory ได้ · เอกสารทุกใบมี master และบัญชีให้อ้าง |
| **2** | `F-INVENTORY` · `F-STOCK-ADJUSTMENT` · `F-STOCK-RESERVATION` · `F-STOCK-TRANSFER` · `F-STOCK-COUNT` | Inventory core — ยอดคงคลัง (รวม lot/serial/expiry tracking ในตัว) + งานที่กระทำต่อสต็อกโดยตรง | สต็อกเดินได้จริงด้วยตัวเอง · allocated มีเจ้าของ · ทุก movement พก lot ได้ |
| **3** | `F-PROSPECT` · `F-CUSTOMER` · `F-QUOTATION` · `F-SALES-ORDER` · `F-PROMOTION` | Sales front — ส่วนใหญ่มี HTML แล้ว ต้องเก็บ BRD/FRD/Testcase ให้ครบ + ผูก Sales Channel และ Stock Reservation | มี SO เป็น contract ให้งานส่งของและ invoice อ้าง |
| **4** | `F-PR` · `F-CP` · `F-PO` | เอกสารต้นทางฝั่งซื้อ: PR → CP → PO | มี PO ให้รับของและตั้งหนี้ |
| **5** | `F-GOODS-RECEIPT` · `F-PUTAWAY` | Inbound — รับของเข้าคลัง: GRN (รับ + QC + tolerance + Close Balance) แล้วต่อด้วย Putaway | ของเข้าคลังได้จริงจากเส้นซื้อ |
| **6** | `F-PICKING` · `F-PACKING` · `F-DELIVERY-NOTE` | Outbound — ส่งของออก: Picking → Packing → Delivery Note (flow เดียวกัน ทำเรียงกัน) | ส่งของได้จริง + มี DN ให้ออก invoice ตามส่งจริง |
| **7** | `F-AP-INVOICE` · `F-AR-INVOICE` · `F-SALES-RETURN` | Billing — ตั้งหนี้ 2 ฝั่ง (AP Invoice มี 3-way match + โหมดจ่ายตรงในตัว · AR Invoice ตามส่งจริงหรือออกตรงได้) + รับคืนจากลูกค้า | เส้นซื้อ-ขายเดินครบรอบ + ยอดลูกหนี้/เจ้าหนี้คำนวณได้ |
| **8** | `F-RETURN-TO-VENDOR` · `F-CREDIT-DEBIT-NOTE` · `F-RECEIPT-VOUCHER` · `F-GRIR-ACCRUAL` | Exceptions & เอกสารแก้กลับ: RTV จาก GRN · Credit/Debit Note ใบเดียวครอบทั้ง 2 ฝั่ง · Receipt Voucher รับเงิน · GR/IR clear accrual | cascade reversal ครบเส้น + รับเงินได้ |
| **9** | `F-PAYMENT-VOUCHER` | ปลายเส้นจ่ายเงิน — ต้องมี 3-way + CN/DN + approval จ่ายตรง ครบก่อน | จบเส้น P2P: จ่าย vendor + refund ได้ทุก VC |

## Engines ที่ถูกยุบ (v2.0)

| engine เดิม | ยุบเข้า | rules ที่ย้าย |
|---|---|---|
| ENG-3WAY (3-Way Match) | `F-AP-INVOICE` | GR-APINV-09, GR-APINV-10 |
| ENG-INV-UOM (UOM Conversion) | `F-INVENTORY-BALANCE` | GR-INVBAL-06 |
| F-RESERVE (Reservation engine) | กลายเป็น feature `F-INVENTORY-RESERVATION` | GR-RSV-01..03 |
| ENG-DOA | `F-APPROVAL-DOA` (boundary) | บังคับผ่าน rule ของ feature ผู้เรียก |

## ⚠️ ค้างอยู่
- **OQ-G01a** — tolerance ตั้งที่ material master ด้วยไหม หรือแค่ config กลาง + PO line
- **OQ-G03a** — reverse GRN ที่ invoice match แล้ว เปิดให้ทำได้ไหม — ตอนนี้ตั้ง **block** ไว้ก่อน
- `F-PURCHASE-CONFIG` + `F-INVENTORY-BALANCE`: Bible ว่า dev done / registry ว่า (—) — เช็คพี่เบิร์ด
