# BASELINE — F-WH-PUTAWAY · Putaway (เทียบ ERP Standard)

> S0.5 · 2026-09-10 · pack CUBE-LANE-W3-LITE · WAVE W3Q · arch **master/console (ห้าม Pattern Q)**
> อ้างอิงจริง: SAP S/4HANA EWM (putaway rules / storage bin determination / direct putaway), Odoo Inventory (Putaway Rules + Storage Categories), Microsoft Dynamics 365 SCM (location directives + work policies + location status), ERPNext (Putaway Rule + capacity), NetSuite WMS (directed putaway / bin management)
> ระดับความมั่นใจ: **ONLINE** (ยืนยัน concept ผ่าน WebSearch 2 query) · รายละเอียดเชิงพฤติกรรมบางข้อเป็นความรู้ ERP ทั่วไป

---

## 1. ภาพรวม — putaway ในโลก ERP คืออะไร

ทุกเจ้ามองเหมือนกัน: **putaway = ขาที่สองของ inbound** ต่อจากการรับของ
เส้นมาตรฐานคือ `Receive (GRN) → ของอยู่ที่ staging/receiving zone → Putaway → ของอยู่ที่ bin จริง → พร้อมขาย/เบิก`

จุดร่วมของทุกเจ้า 4 ข้อ:
1. **การรับของกับการเก็บของแยกกัน** — GRN ทำให้ของ "มีอยู่ในคลัง" แต่ยัง "ยังไม่อยู่ในที่ของมัน"
2. **ระบบเป็นคนแนะนำที่เก็บ** (directed putaway) จาก rule/strategy ที่ config ไว้ ไม่ใช่คนจำเอง
3. **คนหน้างาน override ได้เสมอ** — เพราะของจริงหน้าคลังไม่ตรง master ตลอด (bin เต็ม/พัง/ปิด)
4. **ยืนยันแล้วเกิด stock movement** จาก location ต้นทาง → bin ปลายทาง (append-only)

**Putaway ไม่ใช่เอกสาร** — SAP เรียก Warehouse Task, D365 เรียก Work, Odoo เรียก Internal Transfer/Move line, ERPNext ผูกกับ Stock Entry
→ ไม่มีเลขรันแบบเอกสารธุรกิจ ไม่มีสายอนุมัติ ไม่มีใบพิมพ์ **ตรงกับมติของเลนนี้ที่ว่า Putaway = console ไม่ใช่ Pattern Q** ✅

---

## 2. Must-have (มาตรฐานขั้นต่ำ — ขาดแล้วเรียกว่า putaway ไม่ได้)

| # | ความสามารถ | ใครมี | ทำไมขาดไม่ได้ |
|---|---|---|---|
| **M-01** | **Location structure หลายชั้น** อย่างน้อย warehouse › zone/area › bin (+ ประเภท bin) | SAP (storage type/section/bin) · D365 (site/warehouse/location + location profile) · Odoo (location tree) · ERPNext (warehouse tree) · NetSuite (bin) | ถ้าไม่มีชั้น zone ก็ทำ rule แนะนำที่เก็บไม่ได้เลย |
| **M-02** | **คิวงานค้าง putaway** ที่รู้ว่ามาจากการรับของใบไหน บรรทัดไหน จำนวนเท่าไหร่ | ทุกเจ้า (SAP Warehouse Task queue · D365 Work list · Odoo "Ready" transfers) | เป็นตัวงานหลักของหน้านี้ |
| **M-03** | **แนะนำ bin อัตโนมัติจาก rule** — อย่างน้อย: bin ว่าง · โซนตามประเภทสินค้า/หมวด · bin ที่มีสินค้าตัวเดียวกันอยู่แล้ว | SAP putaway strategy · Odoo Putaway Rules (product/category → location) · D365 Location directive · ERPNext Putaway Rule | คือคุณค่าหลักของ feature |
| **M-04** | **ความจุ bin + กันของล้น** (ปริมาณ/น้ำหนัก/จำนวนสินค้าต่อ bin) | ERPNext (capacity บังคับ) · Odoo (Storage Category capacity) · D365 (location profile max) · SAP (capacity check) | rule ที่ไม่ดูความจุ = แนะนำ bin เต็ม |
| **M-05** | **Override ที่เก็บได้ด้วยมือ** | ทุกเจ้า | ของจริงหน้างานเบี่ยงจาก master เสมอ |
| **M-06** | **ยืนยันการเก็บ (confirm) แล้วเกิด movement** ต้นทาง → bin | ทุกเจ้า | ถ้าไม่ยืนยัน ยอดต่อ bin ไม่มีวันตรง |
| **M-07** | **เก็บบางส่วน / แยกหลาย bin (split)** — ของ 100 ชิ้นลง bin เดียวไม่พอ | SAP (split warehouse task) · D365 (split work line) · Odoo (move line หลายเส้น) | ของล็อตใหญ่ปกติต้องแตก |
| **M-08** | **ยอดคงเหลือแยกราย bin** (stock by location) | ทุกเจ้า | ปลายทางทั้งหมดของ putaway |
| **M-09** | **ของ quarantine / blocked แยกจากของขายได้** | SAP (blocked stock type) · D365 (inventory status) · Odoo (Quality/scrap location) | ของ QC ไม่ผ่านห้ามหลุดไป bin ขาย |
| **M-10** | **Audit / movement append-only** — ใครเก็บ เมื่อไหร่ จากไหนไปไหน · ยกเลิก = reversal | ทุกเจ้า | กฎบัญชีคลัง |
| **M-11** | **ผู้ปฏิบัติงาน (คนจริง) ต่อรายการที่เก็บ** | ทุกเจ้า | ความรับผิดชอบ |

## 3. Nice-to-have (มาตรฐานมี แต่ไม่จำเป็นรอบนี้)

| # | ความสามารถ | ใครมี | ท่าทีของ CUBE รอบนี้ |
|---|---|---|---|
| N-01 | RF / barcode scan ยิง bin + สินค้า (mobile picking device) | SAP RF, D365 mobile app, NetSuite WMS | **backlog** — รอบนี้เป็นหน้าจอ desktop console (แต่ layout ต้องเผื่อ scan field ในอนาคต) |
| N-02 | Cross-docking (ของเข้ามาแล้วส่งออกเลยไม่ต้องเก็บ) | SAP EWM, D365 | **backlog** |
| N-03 | Slotting / ABC velocity optimization (ของขายเร็วอยู่ใกล้ประตู) | SAP EWM, NetSuite | **backlog** — แต่ zone model ต้องรองรับแนวคิดนี้ในอนาคต |
| N-04 | Lot / Batch / Serial + FEFO ตอนเก็บ | ทุกเจ้า | **ไม่รองรับ** — ยังไม่มี Lot master ในเลนนี้ (ตรงกับ GRN N-01) |
| N-05 | หน่วยบรรจุ / pallet / handling unit (HU) | SAP HU, D365 License Plate | **ไม่รองรับรอบนี้** — เก็บระดับ ชิ้น/หน่วยนับ |
| N-06 | Wave / batch putaway หลายคนพร้อมกัน + assign งานให้พนักงาน | SAP, D365 work pools | **บางส่วน** — รอบนี้มี "รับงาน" ระดับ list ได้ แต่ไม่ทำ wave engine |
| N-07 | ระยะทาง/เส้นทางเดินในคลัง (travel optimization) | SAP EWM advanced | **backlog** |
| N-08 | Replenishment / min-max ต่อ bin | ทุกเจ้า | **ไม่อยู่ scope** (คนละ feature) |
| N-09 | Putaway จากแหล่งอื่นนอกจากรับของ (คืนจากลูกค้า / ผลิตเสร็จ) | ทุกเจ้า | **ไม่อยู่ scope W3** — รอบนี้แหล่งเดียวคือ **GRN** |

## 4. Out-of-scope (ยืนยันว่า "ไม่ทำ" ไม่ใช่ "ลืม")

| # | เรื่อง | เหตุผล |
|---|---|---|
| O-01 | ออกเอกสาร/PDF/เลขรัน `PUT-YYYY-NNNN` | **Putaway ไม่ใช่เอกสาร** — chip ไม่มี doccfg/pdfdoc · ERP มาตรฐานก็ไม่ออกใบ |
| O-02 | สายอนุมัติ DOA | ไม่มีเจ้าไหนให้อนุมัติการเก็บของ — เป็นงาน execution |
| O-03 | ปรับยอด (นับได้ไม่ตรง) | = **F-WH-STKADJ** |
| O-04 | ย้ายของหลังเก็บเข้า bin แล้ว | = **F-WH-STKTRF** |
| O-05 | คืนของผู้ขาย (ของ quarantine) | = **F-PUR-RTV** (ปิดแล้ว) |
| O-06 | ต้นทุน / JE | W5 — `TODO: JE posting` · putaway เป็นการย้ายภายในคลังเดียวกัน โดยหลักไม่กระทบมูลค่ารวม |
| O-07 | Cycle count | backlog ตาม `OQ-STK-01` |

---

## 5. Gap vs CUBE (สิ่งที่ PREBRIEF รอบนี้ **ต้องเติมให้ครบ**)

| G | ช่องว่าง | ทำไมสำคัญกับเลนนี้ | ต้องไปโผล่ที่ |
|---|---|---|---|
| **G-01** | **CUBE ยังไม่มี location structure ที่ระบุชัด** — GRN รับเข้าได้แค่ระดับ *location* และเขียนไว้ว่า "bin = Putaway W3Q" | ★ StockAdj + StockTransfer ทั้งคู่รออยู่ · ถ้า Putaway ไม่นิยาม สองตัวถัดไปจะ invent เอง = model แตก | PREBRIEF §3 **location model** (บังคับ) |
| **G-02** | **in-transit location** ยังไม่มีใครนิยาม แต่ `OQ-TRF-01` บอกว่า StockTransfer ข้ามสาขาต้องมี | ถ้า Putaway ไม่จองประเภท location นี้ไว้ใน model StockTransfer จะสร้างชนกัน | PREBRIEF §3 ประเภท location |
| **G-03** | **quarantine location** GRN ใช้แล้ว (`OQ-GRN-01`) แต่ยังไม่มีนิยามเชิงโครงสร้าง (เป็น zone? เป็น bin ประเภทพิเศษ?) | ต้องล็อกให้ตรงกับที่ GRN ใช้ ไม่งั้นของ quarantine หาไม่เจอ | PREBRIEF §3 + คิวแยก quarantine |
| **G-04** | **เกณฑ์แนะนำ bin** ยังไม่เคยเขียนที่ไหนในเลน | คือหัวใจของ feature (M-03) | PREBRIEF §4 BR + §6 UI คอลัมน์ "เหตุผลที่แนะนำ" |
| **G-05** | **ความจุ bin** ยังไม่มี (M-04) | rule ที่ไม่ดูความจุ = แนะนำ bin เต็ม → คนไม่เชื่อระบบ | PREBRIEF §3 field bin + BR |
| **G-06** | **override ต้องบันทึกเหตุผลไหม** | ERP ส่วนใหญ่ให้ override เงียบ ๆ แต่ CUBE เน้น audit → ต้องเคาะ | PREBRIEF §4 BR + OQ |
| **G-07** | **GRN `BR-16`** บอกว่ากลับรายการ GRN ไม่ได้ถ้าของถูก Putaway ไปแล้ว — Putaway ต้องเปิดสถานะให้ GRN อ่าน | ไม่งั้น GRN reversal พังเงียบ | PREBRIEF §5 state + §9 edges |
| **G-08** | **เก็บบางส่วน / split หลาย bin** (M-07) ยังไม่มีในเลน | ของล็อตใหญ่จริงต้องแตก bin | PREBRIEF §2 scenario + §6 |
| **G-09** | **ยกเลิกการเก็บที่ยืนยันแล้ว** ต้องเป็น reversal (movement append-only) | กฎ lock ของเลน | PREBRIEF §2 + §4 BR + §5 |
| **G-10** | **หน้าจอ stock by bin** — ปลายทางของงานนี้ยังไม่มีที่ให้ดู | M-08 · ถ้าไม่มีคนพิสูจน์ไม่ได้ว่า putaway ได้ผล | PREBRIEF §6 (แท็บ/มุมมองผัง bin ใน console) |
| **G-11** | **ผู้ปฏิบัติงานคนจริง** (M-11) | TASTE_LOG บังคับ picker คนจริงทุกที่ที่ระบุคน | PREBRIEF §3 header field |

---

## 6. สรุปท่าทีรอบนี้

- ทำครบ **M-01 … M-11** (must-have ทุกข้อ) — ไม่มีข้อไหนที่ตัดออกได้
- N-01/N-06 ทำ **เผื่อโครง** (ช่อง scan · การรับงาน) แต่ไม่ทำ engine
- N-02/N-03/N-04/N-05/N-07/N-08/N-09 = **backlog ประกาศชัดใน PREBRIEF §2 ตาราง "ไม่รองรับ"**
- ★ ของที่สำคัญที่สุดรอบนี้ไม่ใช่หน้าจอ แต่คือ **location model (G-01/G-02/G-03)** เพราะ StockAdj + StockTransfer จะหยิบไปใช้ทันที

**Sources:**
- [Applying Putaway Rules — SAP Learning](https://learning.sap.com/courses/basic-customizing-in-sap-s-4hana-ewm/applying-putaway-rules)
- [Storage Bin Determination for Putaway — SAP Help](https://help.sap.com/doc/saphelp_ewm900/9.0/en-US/ac/c0b14068a4c24ee10000000a1550b0/content.htm?no_cache=true)
- [Strategy: Empty Storage Bin — SAP Help Portal](https://help.sap.com/docs/PRODUCT_ID/f41048b9ca054326bb9774db1d46e866/54cccb53ad377114e10000000a174cb4.html)
- [Warehouse location status — Dynamics 365 SCM](https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/warehouse-location-status)
- [Set up a location directive for purchase order putaway — Dynamics 365 SCM](https://learn.microsoft.com/lv-lv/dynamics365/supply-chain/warehousing/tasks/set-up-location-directive-purchase-order-put-away)
- [Work policies — Dynamics 365 SCM](https://learn.microsoft.com/en-us/dynamics365/supply-chain/warehousing/warehouse-work-policies)
- [Putaway Rule — ERPNext Docs](https://docs.erpnext.com/docs/v13/user/manual/en/stock/putaway-rule)
