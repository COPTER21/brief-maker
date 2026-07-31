# _KNOWLEDGE_SYNC — patch เข้า cube-master-knowledge
> Trade Core Feature Map `TRADE-CORE` **v4.0.0** · 2026-07-24 (เวอร์ชันล่าสุด)

## 1. เพิ่มใน `03_value_streams/`
`trade-core-feature-map.md` → graph TRADE-CORE **v4.0.0**: **46 nodes · 94 relations · 161 golden rules**
9 waves / 5 phases · **30 features ต้องทำ · 11 มีแล้ว · 5 boundary**
`GOLDEN_RULES.md` = ตัวกลางของทุกเส้น — RIF/BRD/FRD/TC ทุก feature ต้องอ้าง `GR-*` / `XR-*`

## 2. Convention
- ชื่อ feature ตรงกับโฟลเดอร์จริง: Product · UOM · BOM · COA · Product Catalog · Sales Channel · Payment Term · Vendor · Vendor Price List · Warehouse · PR · CP · PO · Purchase Config
- งานที่กระทำต่อสต็อกใช้คำว่า **Stock** (Adjustment / Transfer / Count / Reservation) · ตัวยอดคงคลังคือ **Inventory**
- ไม่มี engine แยก · ไม่มี feature ที่เป็นแค่ "โหมด" ของเอกสารอื่น
- **Domain split (segregation of duties):** `Accounting` = ตั้งหนี้ / ออกเอกสาร / ลงบัญชี (AP Invoice, AR Invoice, Credit/Debit Note, GR/IR, COA, GL) · `Finance` = เงินเข้า-ออกจริง (Payment Voucher, Receipt Voucher)
- ความสัมพันธ์ 4 ชนิด: `config` ตั้งค่าก่อน · `data` ส่งข้อมูล/อ้างเอกสาร · `trigger` กระตุ้นงานถัดไป · `reversal` เอกสารแก้กลับ

## 3. โครงสร้างที่ยุบ/รวม (v4.0.0)
| เรื่อง | ผล |
|---|---|
| Credit Note / Debit Note | รวมเป็น **`F-CREDIT-DEBIT-NOTE` ใบเดียว** ครอบ 4 แบบ (CN/DN × เจ้าหนี้/ลูกหนี้) แยกด้วย `doc_type` + `party` |
| Direct Payment | **ไม่เป็น feature** — เป็นโหมดบนหัว `F-AP-INVOICE` (ติ๊กจ่ายตรง ข้าม PR/PO/GRN) |
| AR Ledger | **ไม่เป็น feature** — ยอดลูกหนี้คำนวณจากเอกสารใน `F-AR-INVOICE` (Invoice − ΣRV − ΣCN) |
| Lot / Serial / Expiry | **ยุบเข้า `F-INVENTORY`** — tracking + FEFO อยู่ในตัวยอดคงคลัง |
| Receiving Tolerance Config | **เปลี่ยนเป็น `F-WAREHOUSE-CONFIG`** (ตั้งค่าคลัง: tolerance + กติกาการรับของ) |
| COA | **เพิ่มใหม่** `F-COA` ผังบัญชี + mapping ต่อประเภทเอกสาร/reason — เงื่อนไขของทุก posting |

## 4. ลำดับการพัฒนา
| Phase | Wave | เนื้อหา |
|---|---|---|
| 1 Masters & Config | W1 | Product · UOM · BOM · **COA** · Product Catalog · Sales Channel · Payment Term · Vendor · Vendor Price List · Warehouse · **Warehouse Config** · Purchase Config · Customer Segment · Price List · Sales Config |
| 2 Inventory Core | W2 | Inventory (รวม lot/serial) · Stock Adjustment · Stock Reservation · Stock Transfer · Stock Count |
| 3 Front Documents | W3-W4 | Prospect · Customer · Quotation · Sales Order · Promotion ‖ PR · CP · PO |
| 4 Warehouse Operations | W5-W6 | **Inbound:** Goods Receipt · Putaway ‖ **Outbound:** Picking · Packing · Delivery Note |
| 5 Billing / Exceptions / Money | W7-W9 | AP Invoice · AR Invoice · Sales Return → RTV · **Credit/Debit Note** · Receipt Voucher · GR/IR → Payment Voucher |

**กฎเหล็กของลำดับ:** Product + UOM + Warehouse ไม่ครบ = เปิดใช้ Inventory ไม่ได้ · COA ไม่ครบ = post บัญชีไม่ได้

## 5. Cross-feature invariants XR-01..XR-14
Conservation · allocated เป็นของ Stock Reservation ผู้เดียว · post แล้วแก้ด้วยเอกสารแก้ไข · Reverse ≠ Return · Refund ผ่าน CN · HOLD ไม่นับ available · 3-way ยกเว้น VC7 + non-PO · Partial ต้องมีสถานะ · อนุมัติผ่าน DOA · config ไม่ย้อนหลัง · Lot ติดของทุก movement · Cancel/Reverse ราย feature · Cascade ต้องย้อนครบรอบ · Config หลายชั้น specific ชนะ

## 6. Decision log (ปิดครบ)
G01 tolerance 3 ชั้น (config กลาง → Product → PO line) · G02 รับลอยได้ทั่วไป · G03 cancel ราย feature · G04 จองทันทีตอน SO confirm · G05 ของเสียใช้ Stock Adjustment reason · G06 vendor เก็บเพิ่ม = DN (ในเอกสาร CN/DN ใบเดียว) · G07 ไม่คุมเครดิตลูกค้า · G08 วันส่งกรอกมือ · G09 ค้างส่งเป็น status · G10 putaway เลือกมือ · G11 นับรอบ custom ใน Stock Count · G12 lot/serial บังคับทั้งเส้น · G13 ตั้ง GR/IR accrual · G14 ค่าขนส่งลงค่าใช้จ่ายแยก · G01a tolerance เก็บที่ Product ด้วย · G03a cascade reversal (PV จ่ายแล้ว = เส้นหยุด)

## 7. ผลกระทบย้อนกลับ feature ที่เสร็จแล้ว (ต้องออก ENH)
- `F-INVENTORY` + `F-STOCK-ADJUSTMENT`: lot/serial/expiry dimension · reason code ของเสีย + map COA · ยืนยันการเพิ่มสินค้าเข้าคลังเอง
- `F-SALES-ORDER`: เรียก Stock Reservation ตอน confirm · สถานะ partial line · ระบุ Sales Channel
- `F-PRODUCT`: field ค่าเผื่อรับเกิน/ขาด ต่อสินค้า
- `F-QUOTATION` / `F-PRICE-LIST`: ผูก Product Catalog + Sales Channel

## 8. Pending manual
- [ ] `FEATURE_REGISTRY.md`: feature ชุด v4.0.0 + ลำดับ 9 waves + decision log
- [ ] แจ้งพี่เบิร์ด: สถานะ `F-PURCHASE-CONFIG` (Bible ว่า done / registry ว่า —) + อัพ H·F·Q sheet
- [ ] คุย Accounting: ผังบัญชี COA + บัญชีพัก GR/IR + mapping reason code → GL ของ Stock Adjustment
- [ ] ยืนยันกับ Strike: domain split Accounting/Finance + การรวม CN/DN เป็นใบเดียว
