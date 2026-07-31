# Golden Rules — CUBE 4.0 Trade Core

> **ตัวกลางของทั้ง 3 เส้น** — กฎที่ทุก feature ต้อง preserve ไม่ว่าจะสร้าง/แก้เมื่อไหร่
> graph `TRADE-CORE` **v4.0.0** · 2026-07-24 · 46 nodes · 94 relations · **161 rules** · feature-only (ไม่มี engine แยก)
> severity **block** = ผิดแล้วระบบผิดเชิงธุรกิจ · warn = best practice
> source: `bible` = P2P Bible · `decision` = ที่ทีมเคาะแล้ว (LD / AC / OQ-G) · `erp-standard` = SAP / Odoo research 2026-07-24
> ส่วนที่ 1-3 generate จาก `workflow_graph.json` โดยตรง — sync 100% ห้ามแก้มือ

---

## 0. Cross-Feature Rules (XR) — กฎคร่อมทุก feature

| id | กฎ | บังคับที่ | ที่มา |
|---|---|---|---|
| **XR-01 Conservation** | ทุก movement (รับ / เก็บ / หยิบ / แตก-แพ็ค / คืน / ปรับ / ย้าย / ส่ง) ต้อง conserve base qty — คำนวณสด ห้ามพึ่ง field สะสม | Goods Receipt · Putaway · Picking · Inventory Transfer · Adjustment · RTV · Sales Return · Delivery Note | LD-02 |
| **XR-02 Allocated ศักดิ์สิทธิ์** | `allocated` แก้ได้โดย **Stock Reservation** ผู้เดียว — feature อื่นอ่านได้ห้ามเขียน; ลดสต็อกได้ไม่เกิน `on_hand − allocated` | ทุก feature ที่แตะ balance | AC-ADJ-04 + OQ-G04 |
| **XR-03 เอกสาร post แล้วห้ามแก้** | validate/post แล้ว → แก้ด้วยเอกสารแก้ไขเท่านั้น (reversal ของ feature นั้น / CN / DN) ห้าม edit-delete ตรง — Tax Invoice เด็ดขาด | ทุกเอกสารธุรกรรม | audit + ภาษีไทย |
| **XR-04 Reverse ≠ Return** | กลับรายการ (บันทึกผิด ของไม่เคลื่อน) กับ คืนของจริง (ของออกจากคลัง) คนละเอกสาร คนละ movement | GRN↔RTV · Delivery Note↔Sales Return · Invoice↔CN | SAP 102 vs 122 |
| **XR-05 Refund ผ่าน CN เสมอ** | คืนเงิน (vendor หรือลูกค้า) → Payment Voucher `voucher_type=refund` ต้องอ้าง CN — ห้ามจ่ายคืนลอย | Payment Voucher · AP Credit Note · AR Credit/Debit Note | Bible |
| **XR-06 HOLD ไม่ใช่ของ** | HOLD / DAMAGED / QC ไม่นับ available — ทุก consumer (Picking, รายงาน, Adjustment ลด) ต้อง filter ออก | ทุก feature ที่อ่าน balance | Bible |
| **XR-07 3-Way ยกเว้นทางเดียว** | 3-way บังคับทุก VC ยกเว้น VC7 Direct Payment — **รวมถึง GRN แบบ non-PO ที่ต้องวิ่งเส้น Direct Payment** | AP Invoice · Payment Voucher · Direct Payment · Goods Receipt | Bible + OQ-G02 |
| **XR-08 Partial ต้องมีสถานะ** | รับขาด / ส่งขาด / หยิบขาด / จ่ายขาด → line ค้างต้องเห็นสถานะได้ (partial หรือ closed+เหตุผล) ห้ามหายเงียบ | GRN · Delivery Note · Picking · Receipt Voucher · PO/SO lines | ปิดงวดไม่ได้ถ้าค้างมองไม่เห็น |
| **XR-09 อนุมัติผ่าน DOA** | ทุกจุดอนุมัติเรียก Approval Authority — ระหว่างรอใช้ placeholder `approver_role / approved_by / approval_chain` ห้าม hardcode | PR · PO · PV · CN/DN · Adjustment · Direct Payment | กติกาเหล็ก CUBE |
| **XR-10 config ไม่ย้อนหลัง** | payment term / VC / tolerance / นโยบายส่ง / conversion factor เปลี่ยนแล้วมีผลเฉพาะเอกสารใหม่ — ที่ approve แล้ว lock ค่าตอนสร้าง | ทุก config feature | เอกสารเก่าต้อง reproduce ได้ |
| **XR-11 Lot ติดของ** | สินค้าที่เปิด tracking (ตั้งใน Inventory) → lot/serial ติดไปกับทุก movement ตลอดเส้น ห้ามรวม lot ต่างกันเป็นแถวเดียว | ทุก movement feature | OQ-G12 |
| **XR-12 Cancel/Reverse ราย feature** | ไม่มี reversal engine กลาง — แต่ละ feature ทำ cancel ของตัวเอง ภายใต้กติกาเดียวกัน | GRN · AP Invoice · PV · Delivery Note · AR Invoice | OQ-G03 |
| **XR-13 Cascade ต้องย้อนครบรอบ** | reverse เอกสารต้นทางที่มีปลายน้ำผูกอยู่ → **ต้อง cascade ยกเลิกปลายน้ำไปพร้อมกัน** ใช้ `reversal_ref` ร่วมกัน ห้าม reverse ลอยทิ้งเอกสารค้าง; **เงินที่จ่าย/รับไปแล้วเป็นเส้นหยุด** ต้อง void voucher ก่อนเสมอ | GRN→AP Invoice→GR/IR · Delivery Note→AR Invoice | OQ-G03a |
| **XR-14 Config หลายชั้น resolve แบบ specific ชนะ** | ค่าที่ตั้งได้หลายระดับ (tolerance: config กลาง → material master → เอกสาร) ให้ชั้นเจาะจงที่สุดชนะ และ **ต้องแสดงว่าใช้ค่าจากชั้นไหน** | Receiving Tolerance · Price List · Payment Term | OQ-G01a |

### ชนิดความสัมพันธ์ระหว่าง feature
| kind | ความหมาย | ตัวอย่าง |
|---|---|---|
| `config` | ต้องตั้งค่าให้เสร็จก่อนถึงใช้ feature ปลายทางได้ | Warehouse → Inventory · COA → ทุก posting · Warehouse Config → Goods Receipt |
| `data` | ส่งข้อมูล / อ้างเอกสารต้นทาง | Purchase Order → Goods Receipt |
| `trigger` | เหตุการณ์กระตุ้นให้เปิดงาน/เอกสารถัดไป | Goods Receipt → Putaway |
| `reversal` | เอกสารแก้กลับของอีกตัว | AP Credit Note → AP Invoice |

---

## 1. Masters & Config — ต้องมีก่อนทุกอย่าง

### `F-PRODUCT` — Product (ข้อมูลสินค้า/วัสดุ) · existing

| id | sev | source | rule |
|---|---|---|---|
| GR-PROD-01 | block | decision | 4-Code (รหัสกลาง/รหัสเก่า/รหัสพัสดุ/รหัสสินค้า) ต้อง unique และค้นหาได้ทุกรหัส |
| GR-PROD-02 | block | decision | สินค้าหยุดใช้งาน → ห้ามเพิ่มสต็อก/ออกเอกสารใหม่ (ลดเพื่อเคลียร์ได้) |
| GR-PROD-03 | block | decision | เก็บค่าเผื่อรับเกิน/ขาดต่อสินค้า เป็นชั้นกลางของ tolerance (OQ-G01a) |
| GR-PROD-04 | block | decision | เปลี่ยนหน่วยฐานหลังมีสต็อก/เอกสารแล้ว → block ต้องสร้างรหัสใหม่ |

### `F-UOM` — UOM (หน่วยวัด) · existing

| id | sev | source | rule |
|---|---|---|---|
| GR-UOM-01 | block | decision | หน่วยฐาน (factor=1) มีได้หนึ่งเดียวต่อสินค้า |
| GR-UOM-02 | block | decision · LD-01/LD-02 | เปลี่ยน conversion factor มีผลเฉพาะ movement ใหม่ — ห้าม recompute ย้อนหลัง |

### `F-BOM` — BOM (สูตร/ชุดสินค้า) · existing

| id | sev | source | rule |
|---|---|---|---|
| GR-BOM-01 | block | erp-standard | แก้สูตรมีผลเฉพาะเอกสารใหม่ — เอกสารเดิม snapshot สูตรตอนสร้าง |
| GR-BOM-02 | warn | erp-standard | ส่วนประกอบต้องเป็นสินค้าที่ active |

### `F-COA` — COA (ผังบัญชี) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-COA-01 | block | erp-standard | ทุก posting ต้องอ้างบัญชีที่ active ในผัง — ปิดบัญชีที่ยังมียอดค้างไม่ได้ |
| GR-COA-02 | block | decision | เปลี่ยนผัง/mapping มีผลเฉพาะเอกสารใหม่ (XR-10) — เอกสารเดิม snapshot บัญชีตอน post |
| GR-COA-03 | block | decision | mapping บัญชีต่อประเภทเอกสาร/reason code ต้องครบก่อนเปิดใช้เอกสารนั้น — ไม่ครบ = block การ post |

### `F-PRODUCT-CATALOG` — Product Catalog (แค็ตตาล็อกสินค้า) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-PCAT-01 | block | decision | เสนอขาย/ตั้งราคาได้เฉพาะสินค้าที่อยู่ในแค็ตตาล็อก active — นอกแค็ตตาล็อกต้องขออนุมัติ |
| GR-PCAT-02 | warn | erp-standard | แค็ตตาล็อกมีช่วงเวลา/ช่องทาง — ทับซ้อนต้องมี priority ชัด |

### `F-SALES-CHANNEL` — Sales Channel (ช่องทางการขาย) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-SCH-01 | block | decision | ทุก SO ต้องระบุช่องทางขาย — ใช้ resolve ราคาและแยกรายงาน |
| GR-SCH-02 | warn | erp-standard | ปิดช่องทางไม่กระทบเอกสารเดิม — บล็อกเฉพาะเอกสารใหม่ |

### `F-PAYMENT-TERM` — Payment Term (เงื่อนไขการชำระเงิน) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-PTERM-01 | block | decision | เงื่อนไขชำระเป็น master กลางใช้ร่วมทั้งซื้อและขาย — แก้แล้วมีผลเฉพาะเอกสารใหม่ (XR-10) |
| GR-PTERM-02 | block | decision | ทุกเอกสารต้อง snapshot เงื่อนไขตอนสร้าง ห้ามอ้าง master แบบ live |

### `F-VENDOR` — Vendor (ข้อมูลผู้ขาย) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-VEN-01 | block | erp-standard | ออก PO/จ่ายเงินได้เฉพาะ vendor active — blacklist block transaction ใหม่ (ของค้างเดิมจบได้) |

### `F-VENDOR-PRICE-LIST` — Vendor Price List (บัญชีราคาผู้ขาย) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-VENP-01 | warn | erp-standard | ราคาอ้างอิงมี valid period — ทับซ้อนต้องมี priority ชัด |

### `F-WAREHOUSE` — Warehouse (คลังและตำแหน่งจัดเก็บ) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-WH-01 | block | decision | ประเภท location กำหนดการนับ available + หน่วยแสดง — เปลี่ยนประเภทตอนมีของค้างต้อง block/ย้ายก่อน |
| GR-WH-02 | block | decision | ต้องสร้างคลัง+ตำแหน่งก่อนจึงเปิดใช้ Inventory ได้ — ห้ามมี balance ที่ไม่มี location |

### `F-WAREHOUSE-CONFIG` — Warehouse Config (ตั้งค่าคลังสินค้า) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-WHCFG-01 | block | decision | ค่าเผื่อเป็น % ตั้งได้ 3 ชั้น: config กลาง → material master (ต่อสินค้า) → PO line (OQ-G01=b + G01a) — ไม่ตั้งเลย = 0% รับเกินไม่ได้ |
| GR-WHCFG-02 | block | decision | resolve แบบ specific ชนะ: PO line > material master > config กลาง — GRN ต้องแสดงว่าใช้ค่าจากชั้นไหน |
| GR-WHCFG-03 | block | decision | แก้ค่าเผื่อที่ material master ไม่มีผลย้อนหลังกับ PO ที่ approve แล้ว (XR-10) — PO snapshot ค่าตอนสร้าง |
| GR-WHCFG-04 | block | decision | เกิน tolerance → block ที่ GRN (ไม่ใช่ warn) — ต้องแก้ PO หรือปฏิเสธของก่อนรับ |
| GR-WHCFG-05 | block | decision | ค่าตั้งของคลังเป็นค่าเริ่มต้นของทุกงานรับ-เก็บในคลังนั้น — เปลี่ยนแล้วมีผลเอกสารใหม่เท่านั้น (XR-10) |

### `F-PURCHASE-CONFIG` — Purchase Config (ตั้งค่าจัดซื้อ) · existing

| id | sev | source | rule |
|---|---|---|---|
| GR-PURCFG-01 | block | erp-standard | เปลี่ยน payment term / VC catalog มีผลเฉพาะเอกสารใหม่ — ที่ approve แล้ว lock ค่าตอนสร้าง |

### `F-CUSTOMER-SEGMENT` — Customer Segment (กลุ่มลูกค้า) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-CSEG-01 | warn | erp-standard | ลูกค้าอยู่ segment หลักได้ 1 กลุ่มต่อช่วงเวลา — ย้ายกลุ่มมีผลราคาเอกสารใหม่เท่านั้น |

### `F-PRICE-LIST` — Price List (บัญชีราคาขาย) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-PLIST-01 | warn | erp-standard | ราคาทับซ้อน (ช่วงวันที่/segment/ปริมาณ) ต้องมี priority — resolve แบบ deterministic |

### `F-SALES-CONFIG` — Sales Configuration (ตั้งค่าการขาย) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-SCFG-01 | warn | erp-standard | เปลี่ยนนโยบายส่ง/invoice-ก่อนส่ง มีผลเฉพาะ SO ใหม่ — SO ค้างใช้ค่าตอน confirm |

## 2. Inventory & Warehouse — คลัง

### `F-INVENTORY` — Inventory (สินค้าคงคลัง) · existing

| id | sev | source | rule |
|---|---|---|---|
| GR-INV-01 | block | decision · LD-01 | ยอดเก็บเป็น base UOM — หน่วยแสดงคำนวณสดตามประเภทตำแหน่ง (bucket model) |
| GR-INV-02 | block | decision · LD-02 | conservation: dest_base = dest.n × dest.factor คำนวณสด — ห้ามพึ่ง field สะสม |
| GR-INV-03 | block | bible | HOLD/DAMAGED/QC ไม่นับ available — ทุก consumer ต้อง filter |
| GR-INV-04 | block | decision | available = on_hand − allocated; allocated แก้ได้โดย Inventory Reservation เท่านั้น |
| GR-INV-05 | block | decision · LD-04 | มูลค่า/unit_cost = Confidential (Finance/Auditor) · assignee = PII |
| GR-INV-06 | block | decision · LD-01/LD-02 | เปลี่ยน conversion factor มีผลเฉพาะ movement ใหม่ — ห้าม recompute balance ย้อนหลังอัตโนมัติ |
| GR-INV-07 | block | decision | เพิ่มสินค้าเข้าคลังได้เองในตัว — สร้าง balance ใหม่ต่อสินค้า×ตำแหน่ง (ตั้งยอดเริ่มต้น/รับเข้าเอง) ผ่านเอกสาร Stock Adjustment เท่านั้น ห้ามสร้างยอดลอย |
| GR-INV-08 | block | decision | เพิ่มสินค้าเข้าคลังได้เฉพาะเมื่อมีสินค้าใน Product ที่ active และมีตำแหน่งใน Warehouse แล้ว |
| GR-INV-09 | block | decision | เปิด tracking ต่อสินค้า = บังคับตลอดเส้น รับ/เก็บ/หยิบ/ย้าย/ส่ง/คืน (OQ-G12=a) |
| GR-INV-10 | block | erp-standard | สินค้าที่มี expiry → หยิบตาม FEFO เป็น default; override ต้องมีเหตุผล + log |
| GR-INV-11 | block | decision | lot/serial ติดไปกับทุก movement — ห้ามรวม lot ต่างกันเป็นแถวเดียว |

### `F-STOCK-ADJUSTMENT` — Stock Adjustment (ปรับยอดคงคลัง) · existing

| id | sev | source | rule |
|---|---|---|---|
| GR-ADJ-01 | block | decision · AC-ADJ-04 | ลดได้ไม่เกิน on_hand − allocated — allocated ไม่เปลี่ยนทุกกรณี |
| GR-ADJ-02 | block | decision · AC-ADJ-05 | block ตำแหน่ง locked (Break/Pack) และ loc_status blocked/frozen/inactive |
| GR-ADJ-03 | block | decision · AC-ADJ-06 | ทุกการปรับ = เอกสาร ADJ (batch+lines) + log ผู้ทำ/เวลา/เหตุผล/ก่อน→หลัง |
| GR-ADJ-04 | block | decision | block เพิ่มสต็อกของ master ที่หยุดใช้งาน (ลดเพื่อเคลียร์ได้) |
| GR-ADJ-05 | warn | decision | adjustment มูลค่าสูง → DOA placeholder รอ engine |
| GR-ADJ-06 | block | decision | reason code ต้องมี ของเสีย/ชำรุด แยกจากเหตุผลอื่น + map GL ค่าใช้จ่าย — ใช้แทนเอกสาร Scrap (OQ-G05=b) |

### `F-STOCK-RESERVATION` — Stock Reservation (การจองสินค้า) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-RSV-01 | block | decision | เป็นเจ้าของ allocated แต่ผู้เดียว — ADJ/DN/Pick อ่านได้แก้ไม่ได้ |
| GR-RSV-02 | block | decision | จองทันทีตอน SO confirm (OQ-G04=a) — ของไม่พอจองได้เท่าที่มี ส่วนขาดค้าง ไม่ block การ confirm |
| GR-RSV-03 | block | decision | ปลดจองเมื่อ DN post (ส่วนที่ส่ง) · SO cancel · line ปิด — ห้ามค้างจองข้ามสถานะปิด |

### `F-STOCK-TRANSFER` — Stock Transfer (การโอนย้ายสินค้า) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-XFER-01 | block | decision | ย้าย atomic: ตัดต้นทาง + เข้าปลายทาง base เท่ากันเสมอ |
| GR-XFER-02 | warn | erp-standard | ข้ามคลัง/บริษัท → มีเอกสารกำกับ + GL posting ถ้าข้าม company |

### `F-STOCK-COUNT` — Stock Count (การนับสินค้า) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-CNT-01 | block | decision | ผลต่างจากการนับ → สร้าง ADJ ผ่าน Inventory Adjustment เท่านั้น ห้ามแก้ balance ตรง |
| GR-CNT-02 | warn | erp-standard | lock location ระหว่างนับ — movement อื่นรอ |
| GR-CNT-03 | block | decision | รองรับสร้างรอบนับ custom ในตัว (เลือก location/สินค้า/ช่วงเวลา) — ไม่มี cycle count แยก (OQ-G11=a) |

### `F-GOODS-RECEIPT` — Goods Receipt (GRN) (ใบรับสินค้า) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-GRN-01 | block | decision | รับลอย (ไม่มี PO) ทำได้ทั่วไป (OQ-G02=c) — แต่ทุก GRN ต้องระบุ source PO-based/non-PO + เหตุผล; non-PO ไม่เข้า 3-way ห้ามไหลเข้า PV อัตโนมัติ ต้องผ่านเส้น Direct Payment |
| GR-GRN-02 | block | bible | จังหวะรับตาม VC: VC1/4/5/6 รับทันที · VC2 หลัง PV confirm · VC3 หลัง PV มัดจำ |
| GR-GRN-03 | block | erp-standard | รับเกิน > tolerance → block; ยืนยันรับเกินแล้วต้องจบที่ RTV หรือ vendor CN ห้ามค้าง |
| GR-GRN-04 | block | bible | รับขาด → PO line ค้าง partial จนครบ หรือ Close Balance + เหตุผล → effective qty ลดตาม |
| GR-GRN-05 | block | bible | QC inline: pass → available + เปิด Putaway · fail → HOLD (ไม่นับ available) → ตัดสิน RTV หรือ ADJ reason=ของเสีย ภายใน SLA |
| GR-GRN-06 | block | bible | Close-Balance trigger เกิดที่ GRN เท่านั้น (invariant ของ P2P) |
| GR-GRN-07 | block | decision | cancel/reverse GRN เป็น logic ของ feature นี้เอง (ไม่มี engine กลาง · OQ-G03=b) — reverse ≠ RTV (ของไม่เคลื่อนออกไปหา vendor) |
| GR-GRN-08 | block | decision | reverse GRN ที่ invoice match แล้ว ทำได้ แต่ต้องเป็น cascade: ยกเลิก AP Invoice ที่ผูกอยู่ในรายการเดียวกันไปพร้อมกันเสมอ ห้าม reverse ลอยทิ้ง invoice ไว้ (OQ-G03a) — ทั้ง 2 เอกสารอ้าง reversal_ref เดียวกัน |
| GR-GRN-09 | block | decision | cascade reversal block เมื่อมี Payment Voucher จ่ายแล้ว — ต้อง void PV ก่อน (เงินออกไปแล้วห้ามย้อนเงียบ) |
| GR-GRN-10 | block | decision | reverse GRN แล้วต้องคืนสถานะทุกอย่างครบรอบ: PO line กลับเป็น open · GR/IR accrual กลับรายการ · สต็อกที่รับเข้าถูกตัดออก (block ถ้าของถูก putaway/หยิบ/ขายไปแล้ว) |
| GR-GRN-11 | warn | erp-standard | GRN ก่อน invoice → ตั้ง GR/IR accrual รอ clear ตอน invoice มา |
| GR-GRN-12 | block | decision · LD-01 | หน่วยรับ = หน่วยของ location แต่บันทึกจริงเป็น base เสมอ |

### `F-PUTAWAY` — Putaway (จัดเก็บเข้าตำแหน่ง) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-PUT-01 | block | bible | putaway เฉพาะของ QC pass — จาก receiving/QC → PICK_FACE/RESERVE |
| GR-PUT-02 | block | decision | ไม่มี auto putaway rule (OQ-G10=b) — เลือกตำแหน่งปลายทางมือทุกครั้ง + log ผู้เลือก |
| GR-PUT-03 | block | decision · LD-03 pattern | ระหว่างย้าย lock ของ+ตำแหน่ง กันหยิบซ้ำ |

### `F-PICKING` — Picking (การหยิบสินค้า) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-PICK-01 | block | bible | หยิบเฉพาะ available ตาม allocation — ห้ามหยิบจาก HOLD/locked |
| GR-PICK-02 | block | decision | หยิบข้ามหน่วย/ตำแหน่งต้องแปลงผ่าน bucket model — บันทึก base |
| GR-PICK-03 | block | decision | หยิบขาด → partial pick → ค้างเป็นสถานะบน SO line + เหตุผล ห้ามเงียบ (OQ-G09=b) |

### `F-PACKING` — Packing (การแพ็คสินค้า) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-PACK-01 | block | erp-standard | qty pack ≤ qty picked ต่อ line — เกิน block |
| GR-PACK-02 | warn | decision | bundle ตาม BOM ต้อง conserve ส่วนประกอบครบสูตร |

### `F-DELIVERY-NOTE` — Delivery Note (ใบส่งของ) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-DN-01 | block | erp-standard | DN อ้าง SO/pack — ส่งเกิน SO ไม่ได้ |
| GR-DN-02 | block | decision | ส่งไม่ครบ → ค้างเป็นสถานะ partial บน SO line (ไม่มีเอกสาร backorder แยก · OQ-G09=b) — ยอดค้างต้องเห็นทุก line |
| GR-DN-03 | block | erp-standard | post DN = ตัดสต็อกจริง + ปลด allocated — ยกเลิกหลัง post ต้อง reverse movement |
| GR-DN-04 | warn | decision | ไม่มี credit block ก่อนส่ง (OQ-G07=c) — ส่งได้โดยไม่เช็ควงเงิน |

### `F-RETURN-TO-VENDOR` — Return to Vendor (คืนของผู้ขาย) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-RTV-01 | block | bible | RTV ดึงของจาก HOLD/DAMAGED เท่านั้น — ห้ามดึงจาก PICK_FACE/available |
| GR-RTV-02 | block | erp-standard | ก่อน invoice → ลด qty matched · หลัง invoice → ต้องมี vendor CN ผูกก่อนปิดงาน |
| GR-RTV-03 | block | erp-standard | ทุก RTV อ้าง GRN ต้นทาง + เหตุผล + ผู้อนุมัติ |
| GR-RTV-04 | block | bible | RTV สร้าง movement ตัด HOLD จริง (conservation base) |

### `F-SALES-RETURN` — Sales Return (RMA) (รับคืนจากลูกค้า) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-RMA-01 | block | erp-standard | RMA อ้าง DN/SO — คืนเกิน qty ที่ส่งไม่ได้ |
| GR-RMA-02 | block | erp-standard | ของคืนเข้า QC ก่อน: pass → available · fail → HOLD แล้วตัดด้วย ADJ reason=ของเสีย |
| GR-RMA-03 | block | erp-standard | ลำดับเงิน: จ่ายแล้ว → CN + refund · ยังไม่จ่าย → CN ลดหนี้ · เปลี่ยนสินค้า → RMA + DN รอบใหม่ไม่แตะเงิน |

## 3. Purchase & Sales — เอกสารต้นทาง

### `F-PR` — PR (ใบขอซื้อ) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-PR-01 | block | erp-standard | PR ต้องผ่าน budget check + อนุมัติ (DOA) ก่อนแปลงเป็น PO — เกินงบ block หรือเข้า approval พิเศษ |
| GR-PR-02 | block | erp-standard | PR ที่แปลงเป็น PO แล้ว lock แก้ไข — แก้ต้อง revision ใหม่อ้างเดิม |
| GR-PR-03 | warn | erp-standard | แปลงครบ/บางส่วนได้ — line ค้างต้องเห็นสถานะ open/partial/closed |

### `F-CP` — CP (ใบเทียบราคา) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-CP-01 | block | decision | มูลค่าเกิน threshold (config) ต้องเทียบ ≥ N vendor — ต่ำกว่าข้ามได้แต่ log เหตุผล |
| GR-CP-02 | warn | decision | ผู้ชนะ + ราคา ต้อง trace เข้า PO ได้ (cmp_no บน PO) |

### `F-PO` — PO (ใบสั่งซื้อ) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-PO-01 | block | bible · D01/D05 | เลือก VC (โครงสร้างจ่ายเงิน) ที่ Wizard Step 2 — เปลี่ยนหลัง approve ไม่ได้ ต้อง cancel + สร้างใหม่ |
| GR-PO-02 | block | bible · D12 | Subcontract Unit Conversion → lock VC1 Full Postpay อัตโนมัติ |
| GR-PO-03 | block | bible | ทุก line ต้อง track qty ordered/received/invoiced — Close Balance ปรับ effective qty และเกิดจาก GRN เท่านั้น |
| GR-PO-04 | block | decision | อนุมัติ PO ผ่าน DOA ตาม threshold — ห้าม hardcode chain |
| GR-PO-05 | warn | erp-standard | tolerance ต่อ line: default จาก config + override ได้ระดับ line |
| GR-PO-06 | block | erp-standard | cancel PO ได้เฉพาะยังไม่มี GRN/Invoice อ้าง — มีแล้วปิดด้วย Close Balance + เหตุผล |

### `F-PROSPECT` — Prospect (ผู้สนใจ (ลีด)) · existing

| id | sev | source | rule |
|---|---|---|---|
| GR-PROSP-01 | warn | decision · HL-01 | Conversion Rate = converted / (total − archived) |
| GR-PROSP-02 | block | decision | converted เป็น terminal — ห้าม reverse; undo = สร้าง Prospect ใหม่ link Customer เดิม |

### `F-CUSTOMER` — Customer Master (ข้อมูลลูกค้า) · existing

| id | sev | source | rule |
|---|---|---|---|
| GR-CUST-01 | block | decision · HL-02 | Convert จาก Prospect ผ่าน Create Modal handoff + prefill ตาม mapping ที่ lock ไว้ |

### `F-PROMOTION` — Promotion (โปรโมชัน) · existing

| id | sev | source | rule |
|---|---|---|---|
| GR-PROMO-01 | warn | erp-standard | โปรโมชันซ้อนกันต้องมีกติกา stacking/priority ชัด — ห้ามลดซ้ำเงียบ ๆ |

### `F-QUOTATION` — Quotation (ใบเสนอราคา) · existing

| id | sev | source | rule |
|---|---|---|---|
| GR-QT-01 | warn | erp-standard | ราคา/ส่วนลดมาจาก pricelist + promotion — override ต้องมีสิทธิ์ + log |
| GR-QT-02 | warn | erp-standard | quotation หมดอายุ (valid_until) → convert ไม่ได้ ต้อง revise |

### `F-SALES-ORDER` — Sales Order (คำสั่งขาย) · existing

| id | sev | source | rule |
|---|---|---|---|
| GR-SO-01 | block | decision | SO confirm → จอง allocated ทันทีผ่าน Inventory Reservation (OQ-G04=a) — ของไม่พอ confirm ได้แต่จองเท่าที่มี |
| GR-SO-02 | warn | decision | ระบบ v1 ไม่คุมวงเงินเครดิต (OQ-G07=c) — ฝ่ายขายรับผิดชอบเอง ห้าม dev ใส่ block เองโดยไม่แก้ decision นี้ |
| GR-SO-03 | block | erp-standard | แก้ SO หลัง confirm ที่กระทบ qty/ราคา → revision log + re-check allocation |
| GR-SO-04 | block | erp-standard | cancel: ก่อนส่ง = ปลด allocation · หลังส่ง = ต้องผ่าน RMA · หลัง invoice = ต้องผ่าน CN — ห้ามลบเอกสาร |

## 4. Accounting & Finance — ตั้งหนี้ / รับ-จ่ายเงิน

### `F-AP-INVOICE` — AP Invoice (3-Way Match) (ใบแจ้งหนี้เจ้าหนี้) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-APINV-01 | block | bible | 3-Way Match บังคับทุก VC ยกเว้น VC7 Direct Payment |
| GR-APINV-02 | block | bible | ฐาน match: PO effective qty = GRN qty = Invoice net (Invoice + ΣDN − ΣCN) |
| GR-APINV-03 | block | erp-standard | invoice มาก่อนของ (VC2) หรือของมาก่อน invoice ต้อง match ได้ทั้งสองลำดับ |
| GR-APINV-04 | block | bible | mismatch → สถานะ Hold ห้ามไหลเข้า PV จนแก้ (CN/DN/แก้เอกสาร/Close Balance) |
| GR-APINV-05 | block | bible | due date ตาม VC — VC6 = วันออก + N วัน; งวดตาม payment term |
| GR-APINV-06 | block | bible | Direct mode: ไม่มี PO ref → จำกัดหมวดค่าใช้จ่าย (config) + approval พิเศษ |
| GR-APINV-07 | block | decision | cancel invoice ที่ validate แล้ว = reversal document ใน feature นี้เอง (OQ-G03=b) — block ถ้ามี PV จ่ายแล้ว ต้อง void PV ก่อน |
| GR-APINV-08 | block | decision | จ่ายตรง (ไม่มี PO) เป็น **โหมดของ AP Invoice** ไม่ใช่เอกสารแยก — ติ๊กที่หัวเอกสารแล้วข้าม PR/PO/GRN; เฉพาะหมวดที่ config อนุญาต |
| GR-APINV-09 | block | decision | โหมดจ่ายตรง bypass 3-way → ต้องผ่าน approval สูงกว่าเส้นปกติ + audit trail ครบ (ใครติ๊ก ใครอนุมัติ เมื่อไหร่) |
| GR-APINV-10 | block | decision | ถูก cascade ยกเลิกจาก reverse GRN ได้ (OQ-G03a) — เมื่อโดน cascade ต้องอ้าง reversal_ref เดียวกับ GRN และห้ามให้ผู้ใช้แก้ระหว่างทาง |
| GR-APINV-11 | block | decision | ค่าขนส่ง/ภาษีนำเข้า ลงเป็นค่าใช้จ่ายแยก ห้ามกระจายเข้า unit_cost ของสินค้า (OQ-G14=b) |
| GR-APINV-12 | block | bible | 3-way match ต่อ VC ตามตาราง Bible — VC5 Partial Delivery match ต่อ round |
| GR-APINV-13 | block | decision | input ของ match คำนวณสดทุกครั้ง (PO effective / GRN สะสม / Invoice net) — ห้าม cache ข้ามเอกสาร |
| GR-APINV-14 | block | bible | ใช้ได้เฉพาะหมวดที่ config อนุญาต — หมวดที่ต้องมี PO ห้ามเข้าเส้นนี้ |
| GR-APINV-15 | block | bible | bypass 3-way → approval สูงกว่าเส้นปกติ + audit trail ครบ |

### `F-AR-INVOICE` — AR Invoice / Tax Invoice (ใบแจ้งหนี้/ใบกำกับภาษี) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-ARINV-01 | block | erp-standard | invoice ตาม qty ส่งจริง (DN) — ยกเว้นมัดจำ/invoice ก่อนส่งตาม config |
| GR-ARINV-02 | block | erp-standard | Tax Invoice ออกแล้วแก้/ยกเลิกไม่ได้ — ปรับด้วย CN/DN เท่านั้น (ภาษีไทย) |
| GR-ARINV-03 | block | bible | due ตาม payment term ลูกค้า — invoice มัดจำหักออกจาก invoice balance |
| GR-ARINV-04 | block | erp-standard | validate → posting AR + ภาษีขาย ทันที |
| GR-ARINV-05 | block | decision | ออก AR Invoice ตรงได้โดยไม่มี SO/DN (บริการ/ขายปลีก) ตาม config — เป็นโหมดของเอกสารเดียวกัน ไม่ใช่ feature แยก |
| GR-ARINV-06 | block | erp-standard | ยอดลูกหนี้คงค้าง = Invoice − ΣRV − ΣCN คำนวณจากเอกสาร ไม่เก็บยอด mutable (ไม่มี AR Ledger แยก) |
| GR-ARINV-07 | warn | erp-standard | ยอดค้าง/aging ต้อง trace ถึงเอกสารต้นทางได้ทุกบรรทัด |
| GR-ARINV-08 | block | erp-standard | ยอดลูกหนี้ = Σinvoice − ΣRV − ΣCN ต่อลูกค้า — คำนวณจากเอกสาร ไม่เก็บยอด mutable |
| GR-ARINV-09 | warn | erp-standard | ยอดค้าง/aging ต้องดูย้อนได้ถึงเอกสารต้นทางทุกบรรทัด |

### `F-CREDIT-DEBIT-NOTE` — Credit / Debit Note (ใบลดหนี้/เพิ่มหนี้) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-CN-01 | block | bible | CN ผูก invoice แบบ many-to-one ได้ — Invoice net คำนวณจาก ΣCN สด |
| GR-CN-02 | block | bible | ต้องมี vendor CN ref + ไฟล์แนบ ก่อน validate |
| GR-CN-03 | block | bible | ปิด CN ได้ 2 ทางเท่านั้น: offset งวดถัดไป หรือ refund ผ่าน PV voucher_type=refund |
| GR-CN-04 | block | decision | Full Prepay (VC2) refund ต้องวิ่งผ่าน CN link เสมอ ห้ามจ่ายคืนลอย |
| GR-CN-05 | block | decision | DN vendor เป็นเอกสารแยก (OQ-G06=a) ห้ามแก้ invoice เดิม — อ้าง invoice/PO ต้นทางเสมอ |
| GR-CN-06 | block | decision | DN เข้า 3-way รวมเป็น Invoice net ฝั่งบวก: net = Invoice + ΣDN − ΣCN |
| GR-CN-07 | block | decision | เอกสารเดียวครอบ 4 แบบ: CN/DN × ฝั่งเจ้าหนี้/ลูกหนี้ — แยกด้วย doc_type + party ห้ามสร้างเอกสารซ้ำซ้อนคนละชนิด |
| GR-CN-08 | block | erp-standard | อ้าง invoice ต้นทางเสมอ (many-to-one ได้) — ห้ามออกลอย |
| GR-CN-09 | block | bible | net = Invoice + ΣDN − ΣCN คำนวณสดทุกครั้ง |
| GR-CN-10 | block | decision | ห้ามแก้ invoice เดิมทุกกรณี — CN/DN คือทางเดียวที่แก้เอกสารที่ validate แล้ว (XR-03) |
| GR-CN-11 | block | bible | ฝั่งเจ้าหนี้: ต้องมี CN/DN ref จาก vendor + ไฟล์แนบ ก่อน validate |
| GR-CN-12 | block | erp-standard | CN จากการคืนของ ออกได้หลังรับของจริงแล้วเท่านั้น (RTV / Sales Return) — ลดราคาโดยไม่คืนของ ไม่ต้องมีเอกสารคืน |
| GR-CN-13 | block | bible | ปิด CN ได้ 2 ทาง: offset งวดถัดไป หรือ refund ผ่าน Payment Voucher voucher_type=refund |
| GR-CN-14 | block | decision | Full Prepay (VC2) refund ต้องวิ่งผ่าน CN link เสมอ ห้ามจ่ายคืนลอย |
| GR-CN-15 | block | decision | เกิน threshold ต้องผ่าน DOA |
| GR-CN-16 | block | erp-standard | CN อ้าง invoice (many-to-one ได้) · DN เรียกเก็บเพิ่มแยกเอกสารเสมอ |
| GR-CN-17 | block | erp-standard | CN จากการคืนของ ออกได้หลัง RMA รับของแล้วเท่านั้น — ลดราคา (ลูกค้าเก็บของ) ไม่ต้องมี RMA |
| GR-CN-18 | block | decision | refund เงินสด → PV voucher_type=refund อ้าง CN; ยังไม่จ่าย → ลดหนี้บน AR |
| GR-CN-19 | block | decision | CN/DN เกิน threshold ต้องผ่าน DOA |

### `F-GRIR-ACCRUAL` — GR/IR Accrual (บัญชีพักรับของ-รอใบแจ้งหนี้) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-GRIR-01 | block | decision | ตั้ง accrual ตอน GRN post / clear ตอน invoice match (OQ-G13=a) — ยอดค้างต้องกระทบยอดกับ GRN ที่ยังไม่มี invoice ได้เสมอ |
| GR-GRIR-02 | warn | erp-standard | accrual ค้างเกิน SLA ต้องโผล่ report ก่อนปิดงวด — ห้ามปิดงวดทั้งที่มียอดค้างไม่ทราบสาเหตุ |
| GR-GRIR-03 | block | decision | cascade reversal จาก GRN → accrual ต้องกลับรายการตามด้วยเสมอ ห้ามค้างยอดพักลอย (OQ-G03a) |

### `F-RECEIPT-VOUCHER` — Receipt Voucher (ใบสำคัญรับ) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-RV-01 | block | erp-standard | RV อ้าง invoice — รับขาด/เกิน → ค้าง partial บน AR ห้าม auto-close |
| GR-RV-02 | warn | erp-standard | reconcile กับ bank statement ก่อนปิดงวด |

### `F-PAYMENT-VOUCHER` — Payment Voucher (ใบสำคัญจ่าย) · planned

| id | sev | source | rule |
|---|---|---|---|
| GR-PV-01 | block | bible | จ่ายได้เมื่อ 3-way pass (หรือ VC7 approved) เท่านั้น — Hold = จ่ายไม่ได้ |
| GR-PV-02 | block | bible | voucher_type payment/refund — refund ต้องอ้าง CN (vendor หรือลูกค้า) เสมอ |
| GR-PV-03 | block | bible | จ่ายตามจังหวะ VC: มัดจำ/งวด 1..N/balance แยก PV ต่อจังหวะ ผูกเอกสารเดียวกัน |
| GR-PV-04 | block | decision | อนุมัติจ่ายผ่าน DOA — threshold ต่อรายการ + สะสมต่อ vendor |
| GR-PV-05 | block | decision | void PV หลังจ่ายจริง = reversal ใน feature นี้เอง (OQ-G03=b) → แจ้ง GL + คืนสถานะ invoice เป็นค้างจ่าย |
| GR-PV-06 | block | decision | PV ที่จ่ายแล้วเป็นตัวหยุด cascade reversal ของ GRN/Invoice — ต้อง void ที่นี่ก่อนเสมอ |

---

## 4. เคสแปลก ๆ → เดินตามกฎไหน

| เคส | เส้นทาง | กฎที่คุม |
|---|---|---|
| ของมาเกิน PO | เกิน % tolerance → **block ที่ Goods Receipt** ต้องแก้ PO หรือปฏิเสธของก่อนรับ | GR-WHCFG-01/02 · GR-GRN-03 |
| ของมาขาด | GRN partial → รอครบ หรือ Close Balance + เหตุผล | GR-GRN-04 · GR-PO-03 · XR-08 |
| รับของไม่มี PO (รับลอย) | ทำได้ แต่ต้องระบุ source=non-PO + เหตุผล → ไม่เข้า 3-way → วิ่งเส้น Direct Payment | GR-GRN-01 · XR-07 |
| ของถึงก่อนใบแจ้งหนี้ | GRN → ตั้ง GR/IR accrual → clear ตอน invoice match | GR-GRN-08 · GR-GRIR-01 |
| ใบแจ้งหนี้ถึงก่อนของ (prepay VC2) | AP Invoice → PV → GRN ทีหลัง → match ย้อน | GR-GRN-02 · GR-APINV-03 |
| QC ไม่ผ่าน | HOLD → **Return to Vendor** หรือ **Adjustment reason=ของเสีย** | GR-GRN-05 · GR-RTV-01 · GR-ADJ-06 · XR-06 |
| บันทึกรับผิด (ของไม่เคลื่อน) | cancel/reverse ใน Goods Receipt เอง — ของยังไม่ถูก putaway/หยิบ/ขาย | GR-GRN-07 · GR-GRN-12 · XR-04 · XR-12 |
| บันทึกรับผิด **หลัง invoice match แล้ว** | reverse GRN ได้ แต่ **cascade ยกเลิก AP Invoice + กลับรายการ GR/IR ไปพร้อมกัน** (reversal_ref เดียวกัน) — ถ้า PV จ่ายแล้วต้อง void PV ก่อน | GR-GRN-10/11 · GR-APINV-11 · GR-PV-06 · GR-GRIR-03 · XR-13 |
| ค่าเผื่อรับของขัดกันหลายชั้น | PO line ชนะ material master ชนะ config กลาง — GRN ต้องบอกว่าใช้ค่าจากชั้นไหน | GR-WHCFG-01/03 · XR-14 |
| vendor ลดหนี้ | AP Credit Note → offset งวดถัดไป หรือ refund ผ่าน PV | GR-CN-07 · XR-05 |
| vendor เก็บเพิ่ม | **Credit/Debit Note ใบเดียว เลือก doc_type=DN ฝั่งเจ้าหนี้** — net = Invoice + ΣDN − ΣCN | GR-CN-01/03 |
| จ่ายมัดจำ / งวด / เครดิต N วัน | PV แยกต่อจังหวะตาม VC — gate ด้วย 3-way ต่อ round | GR-PV-03 · GR-APINV-09 |
| ยกเลิก PV ที่จ่ายแล้ว | reversal ใน Payment Voucher เอง → แจ้ง GL + invoice กลับเป็นค้างจ่าย | GR-PV-05 · XR-12 |
| ปรับสต็อกชนยอดจอง | ลดได้แค่ `on_hand − allocated` — allocated ไม่เปลี่ยน | GR-ADJ-01 · XR-02 |
| SO ยืนยันแต่ของไม่พอ | confirm ได้ จองเท่าที่มี ส่วนขาดค้าง partial (ไม่ block) | GR-SO-01 · GR-RSV-02 |
| ย้ายของข้ามหน่วย / คลัง | atomic + พก lot/serial + เอกสารข้ามบริษัท | GR-XFER-01/02 · XR-01 · XR-11 |
| นับสินค้าไม่ตรง | Stock Count (สร้างรอบ custom ได้) → ผลต่างออกเป็น Stock Adjustment เท่านั้น | GR-CNT-01/03 · GR-ADJ-03 |
| สินค้าใกล้หมดอายุ | หยิบตาม FEFO เป็น default — override ต้องมีเหตุผล + log | GR-INV-10 |
| ส่งลูกค้าไม่ครบ | ค้างเป็นสถานะ partial บน SO line (ไม่มีเอกสาร backorder) | GR-DN-02 · GR-PICK-03 · XR-08 |
| ลูกค้าเครดิตเต็ม | **ระบบ v1 ไม่คุม** — ฝ่ายขายรับผิดชอบเอง | GR-SO-02 · GR-DN-04 |
| ลูกค้าคืนของ | Sales Return → QC → pass เข้า available / fail → Adjustment ของเสีย → ออก CN | GR-RMA-01/02/03 |
| ยกเลิก SO | ก่อนส่ง = ปลดจอง · หลังส่ง = ผ่าน Sales Return · หลัง invoice = ผ่าน CN | GR-SO-04 · GR-RSV-03 · XR-03 |
| แก้ Tax Invoice ที่ออกแล้ว | ไม่ได้ — CN/DN เท่านั้น | GR-ARINV-02 · XR-03 |
| ลูกค้าจ่ายไม่ครบ/เกิน | Receipt Voucher partial ค้างบน AR Ledger ห้าม auto-close | GR-RV-01 · XR-08 |
| คืนเงินลูกค้า | AR Credit Note → PV `voucher_type=refund` | GR-CN-07 · XR-05 |
| ค่าขนส่ง / ภาษีนำเข้า | ลงค่าใช้จ่ายแยก **ห้ามเข้า unit_cost** | GR-APINV-08 |
| จ่ายค่าไฟ/ค่าบริการ ไม่มี PO | ออก **AP Invoice แล้วติ๊กโหมดจ่ายตรง** (ไม่มี feature Direct Payment แยก) — เฉพาะหมวดที่อนุญาต + approval สูงกว่าปกติ | GR-APINV-12/13 |
| ขายบริการ ไม่มี SO/DN | ออก **AR Invoice ตรง** ตาม config — โหมดของเอกสารเดียวกัน | GR-ARINV-05 |
| อยากรู้ยอดลูกหนี้คงค้าง | คำนวณจากเอกสาร: Invoice − ΣRV − ΣCN (ไม่มี AR Ledger แยก ไม่เก็บยอด mutable) | GR-ARINV-06/07 |
| บัญชียังไม่ได้ map | post ไม่ได้ — mapping COA ต่อประเภทเอกสาร/reason ต้องครบก่อน | GR-COA-03 |
| **เพิ่มสินค้าเข้าคลังครั้งแรก** | ต้องมี Product active + ตำแหน่งใน Warehouse → สร้าง balance ผ่าน Stock Adjustment (ตั้งยอดเริ่มต้น) ห้ามสร้างยอดลอย | GR-INV-07/08 · GR-WH-02 · GR-ADJ-03 |
| สินค้าไม่อยู่ในแค็ตตาล็อกแต่อยากขาย | เสนอ/ตั้งราคาไม่ได้ ต้องเพิ่มเข้าแค็ตตาล็อกก่อน หรือขออนุมัติ | GR-PCAT-01 |
| ราคาต่างกันตามช่องทาง | Price List แยกตาม Sales Channel — SO ต้องระบุช่องทางเพื่อ resolve ราคา | GR-SCH-01 · GR-PLIST-01 |

---

## 5. การตัดสินใจ OQ-G01..G14 (2026-07-24)

| OQ | คำตอบ | ผล |
|---|---|---|
| G01 tolerance | % config กลาง + override ต่อ PO line | เก็บเป็น feature `F-RECEIVING-TOLERANCE-CONFIG` |
| G02 รับลอย | ได้ทั่วไป | ไม่มี config switch · แก้ GR-GRN-01 + XR-07 |
| G03 ยกเลิกเอกสาร | แต่ละ feature ทำเอง | ไม่มี reversal engine · เพิ่ม XR-12 |
| G04 allocated | จองทันทีตอน SO confirm | `F-INVENTORY-RESERVATION` (Wave 1) |
| G05 ของเสีย | ใช้ Adjustment reason | ไม่มีเอกสาร Scrap · GR-ADJ-06 |
| G06 vendor เก็บเพิ่ม | เอกสาร DN แยก | `F-AP-DEBIT-NOTE` (Wave 5) |
| G07 เครดิตลูกค้า | ไม่คุมในระบบ v1 | บันทึกเป็น decision rule กัน dev ใส่เอง |
| G08 วันส่ง | กรอกมือ | ไม่มี ATP |
| G09 ค้างส่ง | status บน SO line | ไม่มีเอกสาร backorder |
| G10 putaway | เลือกมือ | GR-PUT-02 |
| G11 นับสินค้า | ยกคลัง + รอบ custom ใน Inventory Count | GR-CNT-03 |
| G12 lot/serial | ต้องมี บังคับทั้งเส้น | `F-LOT-SERIAL-TRACKING` (Wave 1) + XR-11 |
| G13 GR/IR | ตั้ง accrual | `F-GRIR-ACCRUAL` (Wave 5) |
| G14 landed cost | ลงค่าใช้จ่ายแยก | GR-APINV-08 |

### OQ รอบเก็บตก (ปิดแล้ว 2026-07-24)
| OQ | คำตอบ | ผล |
|---|---|---|
| **G01a** tolerance ที่ material master | ตั้งที่ material master ด้วย | resolve 3 ชั้น: config กลาง → material master → PO line (specific ชนะ) · เพิ่ม XR-14 + GR-TOL-03/04 · **Product Master ต้องเพิ่ม field ค่าเผื่อ** |
| **G03a** reverse GRN หลัง invoice match | ทำได้ แต่ต้องย้อนหมด — ยกเลิก invoice ไปด้วย | **cascade reversal** ใช้ `reversal_ref` ร่วมกัน: GRN + AP Invoice + GR/IR กลับพร้อมกัน · **PV ที่จ่ายแล้วเป็นเส้นหยุด** ต้อง void ก่อน · เพิ่ม XR-13 + GR-GRN-10/11/12 · GR-APINV-11 · GR-PV-06 · GR-GRIR-03 |

> **✅ OQ ค้าง = 0** — ทุกข้อตัดสินครบ
