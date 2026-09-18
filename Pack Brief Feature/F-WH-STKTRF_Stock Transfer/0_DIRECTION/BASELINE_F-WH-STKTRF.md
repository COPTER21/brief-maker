# BASELINE — F-WH-STKTRF · Stock Transfer (ย้ายคลัง/สาขา)

> Stage S0.5 · เทียบกับ ERP Standard ระดับโลก: **SAP S/4HANA (STO / two-step transfer)** · **Odoo (Inter-warehouse transfer via transit location)** · **Dynamics 365 F&O / BC (Transfer Order: Ship → Receive)** · **NetSuite (Inventory Transfer vs Transfer Order)** · **ERPNext (Stock Entry: Material Transfer / Material Transfer for Manufacture)**
> WebSearch รันได้ 3 query (คืนเฉพาะรายการลิงก์ ไม่มี snippet) → เนื้อหาเชิงกลไกด้านล่างมาจากความรู้ ERP ประกอบ · ข้อที่เป็นมาตรฐานอุตสาหกรรมมาร์ก `[STD]`
> วันที่ 2026-09-10 · ปี **ค.ศ. ล้วน**

---

## 1. ระบบมาตรฐานทำ Stock Transfer อย่างไร (สรุปกลไกร่วม)

| ระบบ | โครงสร้าง | กลไก in-transit | ปิดใบเมื่อ |
|---|---|---|---|
| **SAP S/4HANA** | STO (Stock Transport Order) · Movement type `641/301` (one-step) vs `641 → 101` (two-step) | **two-step**: ออกจาก plant ต้นทาง → ยอดค้างที่ *stock in transit* ของ plant ปลายทาง → GR ที่ปลายทางจึงเข้า unrestricted | GR ที่ปลายทาง (ปริมาณอาจน้อยกว่า → ค้าง in transit) |
| **Odoo** | Internal Transfer 2 ใบ (Delivery จากคลัง A + Receipt ที่คลัง B) ผูกด้วย **Transit Location** (`Inter-warehouse transit`) | ของอยู่ที่ virtual location `Physical Locations/Inter-warehouse transit` จนกว่าปลายทาง validate | validate ใบ Receipt ที่คลังปลายทาง |
| **D365 F&O / BC** | Transfer Order 1 ใบ 2 จังหวะ: **Ship** แล้ว **Receive** | ยอดอยู่ในสถานะ *In transit* ระหว่าง 2 จังหวะ · มี **Undo transfer shipment** (BC) | Receive ครบ · รับไม่ครบ = ใบยัง open + ยอดค้าง in transit |
| **NetSuite** | **Inventory Transfer** (ทันทีขา 1 จังหวะ) vs **Transfer Order** (Fulfill → Receive + In Transit) | Transfer Order เท่านั้นที่มี In Transit; Inventory Transfer ไม่มี | Receive |
| **ERPNext** | Stock Entry `Material Transfer` (จังหวะเดียว) · ข้ามคลังไกลใช้ 2 ใบ + warehouse "In Transit" | Warehouse ประเภท *Transit* | ใบรับปลายทาง |

**ข้อสรุปที่ทุกเจ้าตรงกัน** `[STD]`
1. **ย้ายใกล้ (ภายในคลัง/ข้าม bin) = จังหวะเดียว** — ไม่ต้องมี in-transit
2. **ย้ายไกล (ข้ามคลัง/สาขา/นิติบุคคล) = 2 จังหวะ** — ส่งออก แล้วปลายทางรับ · ระหว่างนั้นของอยู่ใน **transit location เสมือน** ที่ยัง**นับเป็นทรัพย์สินของกิจการ**
3. **ส่วนต่างระหว่างส่ง–รับ ต้องมีที่ให้มันอยู่** — ค้างที่ in-transit จนกว่าจะสะสาง (รับเพิ่มภายหลัง หรือตัดของหาย)
4. **ไม่มีการลบ movement** — แก้ด้วย reversal / undo shipment ที่สร้างรายการตรงข้าม

---

## 2. Must-have (M) — ระบบระดับสากลมีทุกเจ้า → CUBE ต้องมีรอบนี้

| # | ความสามารถ | เหตุผล / ที่มา | CUBE รอบนี้ |
|---|---|---|---|
| **M-01** | เอกสารใบย้าย มีเลขที่ · หัวใบ · หลายบรรทัด | ทุกเจ้า | ✅ Q-document · `TRF-YYYY-NNNN` |
| **M-02** | ระบุ **คลัง/location ต้นทาง** และ **คลัง/location ปลายทาง** ระดับบรรทัด | ทุกเจ้า | ✅ §3.2 |
| **M-03** | **2 โหมด**: ย้ายภายในคลัง (จังหวะเดียว) vs ข้ามคลัง (2 จังหวะผ่าน transit) | `[STD]` SAP one-step/two-step · Odoo · D365 | ✅ **หัวใจ feature นี้** (OQ-TRF-01) |
| **M-04** | **in-transit location** ที่นับเป็นทรัพย์สิน แต่ยังไม่พร้อมเบิก/ขายที่ปลายทาง | `[STD]` ทุกเจ้า | ✅ ใช้ `WH-TRN` จากสัญญา Putaway §3.0 |
| **M-05** | **ขาส่ง (ship/issue)** — ตัดยอดจาก bin ต้นทาง เข้า in-transit | `[STD]` | ✅ |
| **M-06** | **ขารับ (receive/confirm)** ที่ปลายทาง — ตัดจาก in-transit เข้า bin ปลายทาง แล้ว **ปิดใบ** | `[STD]` | ✅ |
| **M-07** | **รับไม่ครบ (partial receipt)** — ใบยังเปิด ยอดที่เหลือค้าง in-transit | `[STD]` D365/SAP/Odoo | ✅ scenario บังคับ |
| **M-08** | **ตรวจยอดคงเหลือต้นทางก่อนส่ง** — ห้ามส่งเกินของที่มี | ทุกเจ้า | ✅ BR |
| **M-09** | **ตรวจความเข้ากันได้ของประเภท location** (ของกักกันห้ามไหลเข้าที่เก็บปกติ) | SAP stock type (unrestricted/blocked/QI) · Odoo location type | ✅ สืบทอด Putaway §3.0.2 |
| **M-10** | **movement append-only + reversal/undo** | `[STD]` (BC "Undo transfer shipment") | ✅ สืบทอด StockAdj §3.4/§5.2 |
| **M-11** | **สายอนุมัติก่อนส่งของ** (ยิ่งมูลค่าสูงยิ่งต้องอนุมัติ) | D365 workflow · SAP release strategy | ✅ DOA slot picker คนจริง |
| **M-12** | **พิมพ์เอกสารกำกับการย้าย** (transfer slip / delivery note) ให้คนขับรถถือไป | `[STD]` | ✅ pdfdoc `print-spec-trf.md` |
| **M-13** | **ผลกระทบบัญชี** — ข้ามนิติบุคคล/สาขา ต้องมี JE | ทุกเจ้า | 🟡 **mock + `TODO: JE posting`** (W5) |
| **M-14** | **ประวัติ/audit ครบ ใคร-เมื่อไหร่-อะไร** ทั้ง 2 ขา | ทุกเจ้า | ✅ tab ประวัติ |
| **M-15** | **ยกเลิกใบก่อนส่ง** ได้ · หลังส่งแล้วต้อง reversal ไม่ใช่ลบ | `[STD]` | ✅ |
| **M-16** | **soft-reference master** (item/uom/warehouse) ไม่พังเมื่อ master ถูก archive | หลักการ CUBE LD-4C-02 | ✅ |

---

## 3. Nice-to-have (N) — มีในบางเจ้า · **ไม่อยู่ scope รอบนี้** (ห้ามงอก)

| # | ความสามารถ | ใครมี | รอบนี้ |
|---|---|---|---|
| N-01 | **Transfer Order จาก replenishment rule อัตโนมัติ** (min/max, reordering rule) | Odoo · D365 · SAP | ❌ backlog — ไม่มี planning ในเลนนี้ |
| N-02 | **ค่าขนส่ง / ผู้ให้บริการขนส่ง / tracking number / freight reconciliation** | D365 TMS · NetSuite | ❌ backlog — ไม่มี module ขนส่ง |
| N-03 | **Lot / Serial / Batch tracking ตอนย้าย + FEFO** | ทุกเจ้า | ❌ ไม่มี Lot master ในเลนนี้ (ตรงกับ GRN N-04 · Putaway S-26 · StockAdj) |
| N-04 | **Pallet / Handling Unit / License Plate** | SAP HU · D365 | ❌ backlog |
| N-05 | **RF scan / barcode ยิงตอน pick & ship** | ทุกเจ้า | ❌ รอบนี้เป็น console desktop — **แต่ layout ต้องเผื่อช่องยิงรหัส** |
| N-06 | **Pick list / picking wave ก่อนส่ง** | SAP · D365 · Odoo (3-step) | ❌ backlog — รอบนี้ส่งจาก bin ตรง |
| N-07 | **Intercompany transfer + transfer price + markup** | SAP · D365 | ❌ backlog — รอบนี้ข้าม**สาขา**ภายในนิติบุคคลเดียว |
| N-08 | **Transfer แบบข้ามหน่วยนับ (UOM conversion)** | ทุกเจ้า | ❌ ไม่แปลงหน่วยรอบนี้ (ตรงกับ StockAdj) |
| N-09 | **นัดหมายวันที่ส่ง/วันที่ถึง + ETA tracking board** | D365 | 🟡 มีแค่ **วันที่คาดว่าถึง** เป็นข้อมูล ไม่มีหน้า tracking |
| N-10 | **การอนุมัติของ "ฝั่งปลายทาง" ก่อนส่ง (request/approve transfer request)** | SAP STO จาก PR | ❌ backlog — รอบนี้ต้นทางเป็นคนเปิดใบ |
| N-11 | **Quality inspection ตอนรับปลายทาง** | SAP QM | ❌ backlog — QC อยู่ที่ GRN |
| N-12 | **นำเข้าบรรทัดจาก CSV** | บางเจ้า | ❌ backlog (ตรงกับ StockAdj) |
| N-13 | **Cycle count / ใบนับ** | ทุกเจ้า | ❌ **backlog (OQ-STK-01)** — ห้ามงอกเด็ดขาด |
| N-14 | **ปรับยอด/แก้ยอดคงเหลือในใบย้าย** | — | ❌ **เป็นของ F-WH-STKADJ** — ห้ามงอก |

---

## 4. Out-of-scope ชัดเจน (คนละ feature — เขียนไว้กันสับสน)

| เรื่อง | เจ้าของจริง |
|---|---|
| ปรับยอด / ตัดจำหน่ายของเสีย / ปรับยอดกักกัน | **F-WH-STKADJ** |
| เก็บของจาก GRN เข้า bin + แนะนำ bin | **F-WH-PUTAWAY** |
| รับของจากผู้ขาย + QC | **F-WH-GRN** |
| คืนของผู้ขาย (ทางออกของ quarantine) | **F-PUR-RTV** |
| สร้าง/แก้ผัง warehouse · zone · bin · ความจุ | **Location Master (config)** |
| ลงบัญชีจริง / valuation | **W5** |
| สายอนุมัติจริง + วงเงิน | **DOA กลาง F-DLG-001** |
| เลขรัน + สำเนาเอกสาร | **F-DOCCFG / ENG-DOC-NUM / ENG-DOC-STORE** |

---

## 5. Gap vs CUBE — ช่องที่ PREBRIEF (S1) ต้องปิดให้ครบ

| G | ช่องว่าง | ทำไมสำคัญ | ต้องปิดที่ |
|---|---|---|---|
| **G-01** | **สถานะเอกสารต้องแยก 2 ขาให้ชัด** — StockAdj มีแค่ `ผ่านรายการ` จบ แต่ Transfer ต้องมี `ส่งออกแล้ว (อยู่ระหว่างทาง)` แยกจาก `รับครบ/ปิดใบ` | ไม่งั้นจะกลายเป็น one-step แล้วขัด OQ-TRF-01 | PREBRIEF §5.1 state machine |
| **G-02** | **2 โหมด (ในคลัง vs ข้ามคลัง) ต่างกันตรงไหนบ้าง** — จำนวนจังหวะ · จำนวน movement · ใครกดปุ่ม · in-transit มีหรือไม่ | เป็นข้อที่ทีมพลาดบ่อยที่สุด | PREBRIEF §1 + §5.1 + ตารางเทียบโหมด |
| **G-03** | **รับไม่ครบ / ของหายระหว่างทาง** — ส่วนต่างค้างที่ไหน · ใครสะสาง · สะสางด้วยอะไร | ถ้าไม่ตอบ ยอด in-transit จะค้างตลอดกาล | PREBRIEF scenario + BR + §9 |
| **G-04** | **ฐาน DOA ของ Transfer คืออะไร** (มูลค่าที่ย้าย? ข้ามคลังเท่านั้น? ในคลังต้องอนุมัติไหม) | StockAdj ใช้ Σ\|มูลค่า\| — Transfer ต้องนิยามของตัวเองให้ไม่ขัดกัน | PREBRIEF §3.3 + BR + DOA_BRIEF |
| **G-05** | **ต้นทุน/มูลค่าของบรรทัด** มาจากไหน (ย้ายไม่เปลี่ยนมูลค่ารวม แต่ต้องมีตัวเลขให้ DOA + JE) | ต้องสอดคล้อง StockAdj (mock จาก Item Master + `[ASSUMED contract]`) | PREBRIEF §3.2 |
| **G-06** | **ใครเป็นคน confirm รับที่ปลายทาง** (คนคลังปลายทาง ≠ คนเปิดใบ) + สิทธิ์ | ถ้าให้คนเดิมกดเองทั้ง 2 ขา = in-transit ไร้ความหมาย | PREBRIEF §1 สิทธิ์ + §6.4 |
| **G-07** | **ยกเลิก/กลับรายการ ทำได้ตอนไหนบ้าง** (ก่อนส่ง · ระหว่างทาง · หลังรับครบ) | 3 จุดพฤติกรรมต่างกัน | PREBRIEF §5.1 + BR |
| **G-08** | **ของที่ถึงปลายทางแล้ว เข้าที่ bin ไหน** (ระบุตอนเปิดใบ หรือตอน confirm รับ) | กระทบ UX ขารับ | PREBRIEF §3.2 + `[AI-DRAFT]` |
| **G-09** | **ยอด in-transit ดูที่ไหน** — ต้องมีมุมมองให้เห็นว่าอะไรยังอยู่ระหว่างทาง | เป็นสิ่งที่ทุก ERP มี (stock in transit report) | PREBRIEF §6.1 landing KPI + filter |
| **G-10** | **ย้ายของ quarantine / damage ได้ไหม** | สัญญากลาง Putaway §3.0.2 บอกว่า quarantine ออกได้ทางเดียวคือ RTV — ต้องเขียนให้ชัดว่า Transfer ทำอะไรได้บ้าง | PREBRIEF §3.0 + BR |
| **G-11** | **1 ใบ = 1 คู่คลัง (ต้นทาง→ปลายทาง) หรือหลายคู่** | กระทบ line editor + in-transit bin ที่ใช้ | PREBRIEF BR + `[AI-DRAFT]` |
| **G-12** | **ห้ามงอกเป็น "ปรับยอด"** — ผู้ใช้ที่อยากแก้ยอดต้องถูกชี้ไป StockAdj | กัน scope creep ทั้ง 2 ทาง (StockAdj BR-05 ชี้มาทางนี้แล้ว ต้องชี้กลับ) | PREBRIEF §3.6 "สิ่งที่ไม่มี" + microcopy |

---

## 6. สรุป verdict S0.5

- Must-have **16 ข้อ** → อยู่ใน scope รอบนี้ **15 ข้อเต็ม** + **1 ข้อ mock** (M-13 JE posting → W5)
- Nice-to-have **14 ข้อ** → ตัดออกทั้งหมด (1 ข้อเหลือแบบอ่อน N-09 วันที่คาดว่าถึง)
- Gap ที่ PREBRIEF ต้องปิด **12 ข้อ (G-01…G-12)** — ตรวจย้อนที่ S1.5

**Sources (WebSearch 2026-09-10):**
- [SAP Help — Stock Transfer Using a Stock Transport Order](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/91b21005dded4984bcccf4a69ae1300c/5213b953495bb44ce10000000a174cb4.html)
- [SAP Learning — Performing Stock Transfers Between Plants](https://learning.sap.com/courses/inventory-management-and-physical-inventory-in-sap-s-4hana/performing-stock-transfers-between-plants)
- [SAP Community — Stock in Transfer vs Stock in Transit](https://community.sap.com/t5/enterprise-resource-planning-blog-posts-by-sap/stock-in-transfer-vs-stock-in-transit-where-to-find-it-how-to-remove-it/ba-p/13577561)
- [Odoo Docs — Inter-warehouse replenishment (transit location)](https://www.odoo.com/documentation/18.0/applications/inventory_and_mrp/inventory/warehouses_storage/replenishment/resupply_warehouses.html)
- [Microsoft Learn — Undo transfer shipments (Business Central)](https://learn.microsoft.com/en-us/dynamics365/release-plan/2023wave1/smb/dynamics365-business-central/undo-transfer-shipments)
- [Dynamics Chronicles — D365 F&O Transfer order processing](https://dynamics-chronicles.com/article/dynamics-365-fo-transfer-order-processing)
