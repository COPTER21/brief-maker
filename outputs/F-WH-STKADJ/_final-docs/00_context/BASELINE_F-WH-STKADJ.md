# BASELINE — F-WH-STKADJ · Stock Adjustment (ปรับยอดสต๊อก)

> เทียบกับ ERP standard: **SAP S/4HANA & Business One · Odoo 18/19 · Microsoft Dynamics 365 BC/SCM · NetSuite · ERPNext**
> วิธี: `feature-review-standard` · web search 2 query (คืนเฉพาะ title/URL ไม่มี snippet) + ความรู้ ERP ของ runner
> สถานะ: **`[PARTIAL-ONLINE BASELINE]`** — ยืนยันชื่อ feature/หน้าเอกสารได้จากผลค้นหา แต่รายละเอียด field-level มาจากความรู้ ERP → ทุกข้อที่เป็นการตีความติด `[AI-DRAFT]`
> module Warehouse · wave W3Q · fid F082 · arch Q-document · 2026-09-10

---

## 0. ที่ยืนของ feature ใน ERP มาตรฐาน

| ERP | ชื่อที่ใช้ | รูปแบบ |
|---|---|---|
| SAP S/4HANA | **Post Goods Movement (MIGO / MB1A-MB1B-MB1C)** + movement type 701/702 (physical inventory diff), 551/552 (scrapping) + **Reason Code (`MB_REASON`)** | เอกสาร material document + reason code บังคับต่อ movement type |
| SAP Business One | **Inventory Posting / Goods Receipt-Issue (Inventory Adjustment)** | เอกสารมีเลขรัน + approval procedure |
| Odoo 18/19 | **Inventory Adjustments** (`stock.quant` inline edit) + **Scrap Orders** | ไม่ใช่เอกสารเต็มใบ — แก้ quant + `stock.move` ที่มี "Inventory adjustment" location เสมือน |
| D365 BC | **Item Journal / Physical Inventory Journal** + **Reason Code** ต่อบรรทัด | journal + approval workflow |
| NetSuite | **Inventory Adjustment** transaction + **Adjustment Account** + Memo | transaction เต็มใบ + approval routing |
| ERPNext | **Stock Reconciliation** + **Stock Entry (Material Receipt/Issue)** | เอกสารมีเลขรัน + workflow state |

**สรุปที่ยืน:** ERP ระดับ tier-1 ทุกตัวถือว่า Stock Adjustment = **เอกสารธุรกรรมที่มีผลทางบัญชีทันที** ไม่ใช่แค่แก้ตัวเลข → **ยืนยันการเลือก arch = Q-document ของ CUBE ว่าถูกต้อง** (Odoo เป็นข้อยกเว้นที่ทำเป็น inline edit ซึ่งเป็นจุดอ่อนด้าน audit ที่ CUBE ไม่ควรลอก)

---

## 1. MUST-HAVE (ERP standard บังคับ — ขาดแล้วถือว่า feature ไม่ครบ)

| # | ความสามารถ | ที่มา | CUBE รอบนี้ |
|---|---|---|---|
| M-01 | **เอกสารมีเลขรัน + สถานะชัดเจน** (draft → รออนุมัติ → อนุมัติ → posted → ยกเลิก) | SAP B1 · NetSuite · ERPNext | ✅ `ADJ-YYYY-NNNN` ผ่าน doccfg |
| M-02 | **ปรับได้ทั้ง + และ −** ในใบเดียว | ทุกเจ้า | ✅ ใน scope |
| M-03 | **Reason code บังคับต่อบรรทัด** จาก master ที่ config ได้ | SAP `MB_REASON` · D365 Reason Code · NetSuite Memo | ✅ **บังคับ** (OQ-STK-01) |
| M-04 | **อ้าง location ระดับ bin** ไม่ใช่แค่คลัง | SAP storage bin (EWM/WM) · D365 bin · NetSuite bin | ✅ ใช้ location model จาก Putaway §3.0 |
| M-05 | **แสดงยอดระบบ (system qty) เทียบยอดจริง (counted qty) + ผลต่าง** ตอนกรอก | ทุกเจ้า | ✅ B2 v2 line editor 3 คอลัมน์ |
| M-06 | **มูลค่าผลกระทบ (valuation impact)** คำนวณให้เห็นก่อน post | SAP · NetSuite · Odoo | ✅ แสดงมูลค่า/บรรทัด + รวมใบ (**ต้นทุนมาจาก mock — engine จริง W5**) |
| M-07 | **สายอนุมัติตามมูลค่า/นัยสำคัญ** | SAP approval procedure · NetSuite approval routing · ERPNext workflow | ✅ DOA ตามมูลค่าที่ปรับ |
| M-08 | **Post แล้วเกิด stock movement ที่ย้อนรอยได้** | ทุกเจ้า | ✅ movement append-only |
| M-09 | **ยกเลิก/กลับรายการหลัง post = reversing document ไม่ใช่ลบ** | SAP MBST cancel · NetSuite · ERPNext | ✅ reversal เท่านั้น (LOCK) |
| M-10 | **ผูก GL/JE** (COGS / Inventory Adjustment Account) | NetSuite adjustment account · Odoo · SAP | ⚠️ **mock + `TODO: JE posting`** (W5) |
| M-11 | **Audit trail: ใคร-เมื่อไหร่-แก้อะไร** | ทุกเจ้า | ✅ tab ประวัติ + append-only |
| M-12 | **แนบหลักฐาน** (รูปของเสีย/บันทึกหัวหน้าคลัง) | NetSuite · ERPNext · D365 | ✅ เอกสารแนบใน landing (Pattern Q) |
| M-13 | **พิมพ์เอกสาร/PDF สำหรับเซ็น** | SAP B1 · ERPNext print format | ✅ pdfdoc + print-spec + tab ลายเซ็น |
| M-14 | **กัน adjust สินค้าใน location ที่ไม่ควรแตะ** (blocked/quarantine/transit) | SAP blocked stock · D365 blocking | ✅ กติกาข้ามประเภทจาก Putaway §3.0.2 |

---

## 2. NICE-TO-HAVE (มีแล้วดี · ERP บางเจ้าเท่านั้น · รอบนี้ทำเท่าที่ scope อนุญาต)

| # | ความสามารถ | ที่มา | CUBE รอบนี้ |
|---|---|---|---|
| N-01 | นำเข้าไฟล์ CSV/Excel รายการปรับจำนวนมาก | D365 · NetSuite CSV import | ❌ backlog (ไม่อยู่ scope) |
| N-02 | จำกัดสิทธิ์ reason code ต่อกลุ่มผู้ใช้ (ใครใช้ "สูญหาย" ได้บ้าง) | SAP authorization · NetSuite role | 🟡 ประกาศเป็น config note ใน PREBRIEF (ไม่ทำ UI รอบนี้) |
| N-03 | Threshold แจ้งเตือนเมื่อผลต่างเกิน % ของยอดระบบ | D365 tolerance · NetSuite | 🟡 **อยู่ NC rules** ไม่อยู่ feature code (GOLDEN §2.10) |
| N-04 | รายงาน KPI: ความถี่การปรับต่อ bin / ต่อเหตุผล / ต่อคน | ทุกเจ้า | 🟡 นับได้จาก movement — ไม่ทำหน้า report รอบนี้ |
| N-05 | ปรับยอดหลายคลังในใบเดียว | NetSuite (subsidiary-level) | ❌ **1 ใบ = 1 คลัง** (ตัดออกเพื่อความชัดของ DOA + JE) |
| N-06 | Serial/Lot-level adjustment | SAP · D365 · NetSuite | ❌ ไม่มี Lot master ในเลนนี้ |
| N-07 | Landed cost / revaluation (ปรับ**ราคา** ไม่ปรับจำนวน) | SAP MR21 · Odoo · NetSuite | ❌ คนละ feature (valuation W5) |
| N-08 | ปรับยอดจากมือถือ/RF scanner | SAP EWM RF · D365 warehouse app | ❌ backlog |

---

## 3. OUT-OF-SCOPE รอบนี้ (มีใน ERP มาตรฐาน แต่ **CHECKLIST ตัดออกชัดเจน** — ห้ามทำ)

| # | ความสามารถ | ทำไมตัด | เจ้าของจริง |
|---|---|---|---|
| O-01 | ★ **Cycle Count / Physical Inventory Count sheet** (นับสต๊อกรอบ, count schedule, blind count, count variance approval) | `OQ-STK-01 [ASSUMED]` ระบุชัด "cycle count = backlog ไม่อยู่ scope นี้" | **backlog** — owner Strike |
| O-02 | ★ **เปลี่ยน/ย้าย location ของสินค้า** | CHECKLIST W3Q: "เพิ่ม/ลด เท่านั้น — เปลี่ยน location ไม่อยู่ตัวนี้" | **F-WH-STKTRF** (Stock Transfer) |
| O-03 | เขียนของเข้า/ออก `in-transit` | Putaway §3.0.2 OB-11 — จองไว้ให้ StockTransfer | **F-WH-STKTRF** |
| O-04 | สร้าง/แก้ Location Master (zone/bin/ความจุ) | soft-ref LD-4C-02 — เป็น config | **Location Master (config)** |
| O-05 | โพสต์ JE จริงเข้า GL | dep ข้ามเลน | **W5 (GL/JE)** — mock + `TODO: JE posting` |
| O-06 | คำนวณต้นทุนจริง (FIFO/Moving Average engine) | dep ข้ามเลน | **W5 valuation** — รอบนี้ต้นทุนมาจาก mock `[ASSUMED contract]` |
| O-07 | ตั้งค่าสายอนุมัติ/วงเงินในหน้า feature | GOLDEN §3 — ห้าม hardcode สายอนุมัติ | **DOA กลาง (F-DLG-001)** — feature แค่ประกาศ |
| O-08 | ตั้งค่ารูปแบบเลขรันในหน้า feature | GOLDEN §3 | **F-DOCCFG** — feature แค่ประกาศ |

---

## 4. GAP vs CUBE (สิ่งที่ต้องระวังตอนทำ PREBRIEF/HTML)

| # | Gap | ผลถ้าไม่จัดการ | ทางออกรอบนี้ |
|---|---|---|---|
| G-01 | **มูลค่าที่ปรับ = qty × ต้นทุน** แต่ CUBE ยังไม่มี valuation engine (W5) | DOA ตามมูลค่าจะคำนวณไม่ได้ → กติกาอนุมัติพัง | ใช้ **ต้นทุนอ้างอิงจาก Item Master (mock)** + ป้าย `[ASSUMED contract]` บนช่องมูลค่า + `FWD-WIRE: valuation engine` `[AI-DRAFT]` |
| G-02 | ERP ส่วนใหญ่คิด DOA จาก **ค่าสัมบูรณ์ของผลกระทบสุทธิ** แต่ใบเดียวมีทั้ง + และ − | ปรับ +1M/−1M แล้วสุทธิ = 0 → หลุดอนุมัติ | **ใช้ผลรวมค่าสัมบูรณ์ (Σ\|มูลค่าต่อบรรทัด\|) เป็นฐาน DOA** ไม่ใช่ยอดสุทธิ — `[AI-DRAFT]` เขียนเป็น BR ชัดใน PREBRIEF |
| G-03 | Odoo ทำ adjustment เป็น inline edit ไม่มีใบ | ถ้าลอก Odoo จะไม่มี audit/approval | **ไม่ลอก** — ยึด SAP B1/NetSuite/ERPNext = เอกสารเต็มใบ (ตรงกับ arch Q-document) |
| G-04 | ยอดระบบ (system qty) เปลี่ยนได้ระหว่างที่ใบยังรออนุมัติ | อนุมัติเสร็จแล้ว post ทับยอดที่เปลี่ยนไป | **snapshot ยอดระบบตอนสร้างบรรทัด + ตรวจซ้ำตอน post ถ้าต่างให้เตือน** `[AI-DRAFT]` (ERP เรียก recount warning) |
| G-05 | reason code ของ ERP ผูกกับ **บัญชีปลายทาง** (scrap → COGS-scrap) | JE ตอน W5 ไม่รู้จะลงบัญชีไหน | ให้ master เหตุผลมี field **"บัญชีปลายทาง (mock)"** ประกาศไว้ใน CSQ/DOCCFG + `TODO: JE posting` |
| G-06 | quarantine/damage มีกติกาข้ามประเภทเฉพาะ | คนทำ HTML อาจปล่อยให้เลือก bin อะไรก็ได้ | **filter bin ตาม `location_type`** ตั้งแต่ใน picker + BR ชัด: `in-transit` ไม่โผล่เลย |
| G-07 | ERP มี tolerance % ก่อนต้องอนุมัติพิเศษ | อาจถูกยัดเป็นเลขใน feature code | **อยู่ NC rules** — feature แค่แสดงป้ายเตือน ไม่เก็บเลข |
| G-08 | cycle count เป็นเพื่อนบ้านที่ใกล้มาก คนทำอาจเผลอทำ "นับสต๊อก" | scope creep ชน O-01 | **ห้ามมีคำว่า "นับสต๊อก/cycle count/ใบนับ" เป็น feature** — ใน UI ใช้คำว่า "ยอดนับได้จริง" ที่ระดับบรรทัดเท่านั้น (เป็น input ของการปรับ ไม่ใช่กระบวนการนับ) |

---

## 5. สรุป verdict baseline
- **arch Q-document = ตรงกับ ERP มาตรฐาน** (SAP B1 / NetSuite / ERPNext) ✅
- must-have 14 ข้อ → รอบนี้ครอบ **13 เต็ม + 1 mock (M-10 JE)** — ไม่มีข้อไหนตกโดยไม่ตั้งใจ
- ความเสี่ยงหลัก = **G-02 (ฐาน DOA)** และ **G-08 (scope creep ไป cycle count)** → ต้องเขียนเป็น BR ล็อกใน PREBRIEF

**Sources (web search 2026-09-10):**
- [SAP: Defining Movement Types and Reason Codes (S/4HANA Cloud)](https://learning.sap.com/courses/exploring-foundations-of-physical-inventory-in-sap-s-4hana-cloud-private-edition/defining-movement-types-and-reason-codes)
- [SAP Community: Stock Adjustment Approval workflow in MIGO](https://community.sap.com/t5/technology-q-a/stock-adjustment-approval-workflow-in-migo/qaq-p/7744781)
- [SAP Business One Inventory Adjustment — definition & process](https://www.hyperbots.com/glossary/sap-business-one-inventory-adjustment)
- [SAP Inventory Management — Inventory Adjustment (positive & negative) PDF](https://www.rfgen.com/wp-content/uploads/2021/01/SAP_IM_Adjustment.pdf)
- [Odoo 19 documentation — Inventory adjustments](https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management/count_products.html)
- [Odoo — Inventory postings & valuation](https://odootricks.tips/inventory-postings-valuation/)
- [NetSuite — Inventory Write-Offs: how-to guide with example entry](https://www.netsuite.com/portal/resource/articles/inventory-management/inventory-write-off.shtml)
- [MangoApps — Inventory Adjustment Journal SOP template](https://www.mangoapps.com/templates/sop/inventory-adjustment-journal-sop)
