---
file_id: KB-04-04
title: WF-01 Run List — CUBE 4.0 Trade Core (41 features · 9 waves)
version: 1.0.0
last_updated: 2026-07-26
status: stable
source: Central_Plan workflow_graph v4.0.0 (2026-07-24) — 46 nodes · 94 edges · 161 rules
---

# WF-01 Run List — ลำดับรัน 41 feature ตั้งแต่ต้นจนจบ

> checklist กลางสำหรับรอบ "ทำใหม่ตั้งแต่แรกจนจบ" — 1 แถว = 1 LANE_BRIEF = 1 lane run
> ★ = มีของเดิม → brief ต้องระบุ ENH/อ้าง artifact เดิม (กัน Hard Stop สร้างซ้ำ)
> อัพเดตคอลัมน์สถานะเมื่อ feature จบเลน (ผ่าน chat: "อัพเดต run list — F-XXX done")

**กติกาการรัน:** ยึด wave เท่านั้น — dependency `data`/`config` บังคับลำดับ · ข้าม wave = coverage gate BLOCK ปลายทาง


## Wave 1 — Masters & Config (15)

| # | Feature | ชื่อ | rules (block) | ของเดิม | สถานะรัน |
|---|---|---|---|---|---|
| 1 | `F-PRODUCT` | ข้อมูลสินค้า/วัสดุ | 4 (4) | ★ | ☐ |
| 2 | `F-UOM` | หน่วยวัด | 2 (2) | ★ | ☐ |
| 3 | `F-BOM` | สูตร/ชุดสินค้า | 2 (1) | ★ | ☐ |
| 4 | `F-COA` | ผังบัญชี | 3 (3) |  | ☐ |
| 5 | `F-PRODUCT-CATALOG` | แค็ตตาล็อกสินค้า | 2 (1) |  | ☐ |
| 6 | `F-SALES-CHANNEL` | ช่องทางการขาย | 2 (1) |  | ☐ |
| 7 | `F-PAYMENT-TERM` | เงื่อนไขการชำระเงิน | 2 (2) |  | ☐ |
| 8 | `F-VENDOR` | ข้อมูลผู้ขาย | 1 (1) |  | ☐ |
| 9 | `F-VENDOR-PRICE-LIST` | บัญชีราคาผู้ขาย | 1 (0) |  | ☐ |
| 10 | `F-WAREHOUSE` | คลังและตำแหน่งจัดเก็บ | 2 (2) |  | ☐ |
| 11 | `F-WAREHOUSE-CONFIG` | ตั้งค่าคลังสินค้า | 5 (5) |  | ☐ |
| 12 | `F-PURCHASE-CONFIG` | ตั้งค่าจัดซื้อ | 1 (1) | ★ | ☐ |
| 13 | `F-CUSTOMER-SEGMENT` | กลุ่มลูกค้า | 1 (0) |  | ☐ |
| 14 | `F-PRICE-LIST` | บัญชีราคาขาย | 1 (0) |  | ☐ |
| 15 | `F-SALES-CONFIG` | ตั้งค่าการขาย | 1 (0) |  | ☐ |

## Wave 2 — Inventory Core (5)

| # | Feature | ชื่อ | rules (block) | ของเดิม | สถานะรัน |
|---|---|---|---|---|---|
| 16 | `F-INVENTORY` | สินค้าคงคลัง | 11 (11) | ★ | ☐ |
| 17 | `F-STOCK-ADJUSTMENT` | ปรับยอดคงคลัง | 6 (5) | ★ | ☐ |
| 18 | `F-STOCK-RESERVATION` | การจองสินค้า | 3 (3) |  | ☐ |
| 19 | `F-STOCK-TRANSFER` | การโอนย้ายสินค้า | 2 (1) |  | ☐ |
| 20 | `F-STOCK-COUNT` | การนับสินค้า | 3 (2) |  | ☐ |

## Wave 3 — Sales Front (5)

| # | Feature | ชื่อ | rules (block) | ของเดิม | สถานะรัน |
|---|---|---|---|---|---|
| 21 | `F-PROSPECT` | ผู้สนใจ (ลีด) | 2 (1) | ★ | ☐ |
| 22 | `F-CUSTOMER` | ข้อมูลลูกค้า | 1 (1) | ★ | ☐ |
| 23 | `F-QUOTATION` | ใบเสนอราคา | 2 (0) | ★ | ☐ |
| 24 | `F-SALES-ORDER` | คำสั่งขาย | 4 (3) | ★ | ☐ |
| 25 | `F-PROMOTION` | โปรโมชัน | 1 (0) | ★ | ☐ |

## Wave 4 — เอกสารต้นทางฝั่งซื้อ (3)

| # | Feature | ชื่อ | rules (block) | ของเดิม | สถานะรัน |
|---|---|---|---|---|---|
| 26 | `F-PR` | ใบขอซื้อ | 3 (2) |  | ☐ |
| 27 | `F-CP` | ใบเทียบราคา | 2 (1) |  | ☐ |
| 28 | `F-PO` | ใบสั่งซื้อ | 6 (5) |  | ☐ |

## Wave 5 — Inbound (2)

| # | Feature | ชื่อ | rules (block) | ของเดิม | สถานะรัน |
|---|---|---|---|---|---|
| 29 | `F-GOODS-RECEIPT` | ใบรับสินค้า ⚠️ เคาะ OQ-G01a/G03a ก่อน | 12 (11) |  | ☐ |
| 30 | `F-PUTAWAY` | จัดเก็บเข้าตำแหน่ง | 3 (3) |  | ☐ |

## Wave 6 — Outbound (3)

| # | Feature | ชื่อ | rules (block) | ของเดิม | สถานะรัน |
|---|---|---|---|---|---|
| 31 | `F-PICKING` | การหยิบสินค้า | 3 (3) |  | ☐ |
| 32 | `F-PACKING` | การแพ็คสินค้า | 2 (1) |  | ☐ |
| 33 | `F-DELIVERY-NOTE` | ใบส่งของ | 4 (3) |  | ☐ |

## Wave 7 — Billing (3)

| # | Feature | ชื่อ | rules (block) | ของเดิม | สถานะรัน |
|---|---|---|---|---|---|
| 34 | `F-AP-INVOICE` | ใบแจ้งหนี้เจ้าหนี้ | 15 (15) |  | ☐ |
| 35 | `F-AR-INVOICE` | ใบแจ้งหนี้/ใบกำกับภาษี | 9 (7) |  | ☐ |
| 36 | `F-SALES-RETURN` | รับคืนจากลูกค้า | 3 (3) |  | ☐ |

## Wave 8 — Exceptions & เอกสารแก้กลับ (4)

| # | Feature | ชื่อ | rules (block) | ของเดิม | สถานะรัน |
|---|---|---|---|---|---|
| 37 | `F-RETURN-TO-VENDOR` | คืนของผู้ขาย | 4 (4) |  | ☐ |
| 38 | `F-CREDIT-DEBIT-NOTE` | ใบลดหนี้/เพิ่มหนี้ | 19 (19) |  | ☐ |
| 39 | `F-RECEIPT-VOUCHER` | ใบสำคัญรับ | 2 (1) |  | ☐ |
| 40 | `F-GRIR-ACCRUAL` | บัญชีพักรับของ-รอใบแจ้งหนี้ | 3 (2) |  | ☐ |

## Wave 9 — ปลายเส้น (1)

| # | Feature | ชื่อ | rules (block) | ของเดิม | สถานะรัน |
|---|---|---|---|---|---|
| 41 | `F-PAYMENT-VOUCHER` | ใบสำคัญจ่าย | 6 (6) |  | ☐ |

## จุดระวังรายทาง
- **Wave 1-3 rules เบา (3-5 ข้อ)** — ใช้เป็นสนาม harden เลน ก่อนถึงของหนัก
- **Wave 5 `F-GOODS-RECEIPT` (12 rules)** — ต้องเคาะ OQ-G01a (tolerance ชั้นไหน) + OQ-G03a (reverse หลัง match — ตั้ง block ไว้ก่อน) ให้จบก่อนออก brief
- **Wave 7 `F-AP-INVOICE` (15) / Wave 8 `F-CREDIT-DEBIT-NOTE` (19)** — rules หนักสุดในระบบ เผื่อ fix rounds มากกว่าปกติ
- **Wave 3 ★ ทั้ง wave** — มี HTML แล้ว งานคือเก็บ BRD/FRD/TC ให้ครบ + ผูก Sales Channel / Stock Reservation

## Boundary — ไม่เข้าเลน (5)
`F-GL-POSTING` ★ · `F-APPROVAL-DOA` · `F-USER-ACCESS` · `F-NOTIFICATION` · `F-BUDGET-CONTROL`
→ feature ที่แตะ approval ใช้ placeholder pattern (approver_role/approved_by/approval_chain + TODO) รอ wire DOA

## Change Log
- **1.0.0** (2026-07-26): สร้างจาก Central_Plan v4.0.0 — 41 features / 9 waves / 161 rules
