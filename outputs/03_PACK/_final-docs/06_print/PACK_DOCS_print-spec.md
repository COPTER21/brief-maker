# PRINT SPEC — ใบแพ็คสินค้า (PACKSLIP) + ป้ายกล่อง (BOXLABEL) · F-WH-PACK

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ PREBRIEF/FRD ของ F-WH-PACK (แพ็คสินค้า)
> ไฟล์คู่: `PACKSLIP_template.html` + `PACKSLIP_sample.pdf` · `BOXLABEL_template.html` + `BOXLABEL_sample.pdf`
> ทั้งสองใบ render จากข้อมูลใบแพ็คใบเดียวกัน (1 ใบแพ็ค = 1 packing slip + N ป้ายกล่อง)

---

## 1. สรุปเอกสาร
| | ใบแพ็คสินค้า (Packing Slip) | ป้ายกล่อง (Shipping Label) |
|---|---|---|
| รหัส | PACKSLIP | BOXLABEL |
| ขนาด | **A4 แนวตั้ง** 210×297 mm · ขอบ 14 mm | **150×100 mm แนวนอน** (label thermal 6×4") · ขอบ 4.5–5 mm |
| จำนวนพิมพ์ | 1 ใบ/ใบแพ็ค (แนบไปกับสินค้า) | 1 ใบ/กล่อง (แปะข้างกล่อง) |
| เครื่องพิมพ์ | เลเซอร์/อิงค์เจ็ท A4 | label printer (Zebra/TSC) 4×6" |
| มาตรฐาน | thai-doc-pdf-generator (base.css + blocks B1/B2/B3/B4/B5/B6/B7) | CI/ฟอนต์เดียวกัน แต่ layout label (ไม่ใช้ A4) |
| ฟอนต์ | Sarabun ฝัง base64 | Sarabun ฝัง base64 |
| CI | CUBE NATIVE (Navy #0B1D3A / Primary #0B5CFF / Teal #00A88E) | เหมือนกัน |
| Renderer | Playwright/Chromium · `print_background` + `prefer_css_page_size` | เหมือนกัน (page size จาก `@page`) |

---

## 2. Field Mapping — ใบแพ็คสินค้า (A4)

| ช่องในเอกสาร | Source | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่ใบแพ็ค | `pack.code` | `PACK-พ.ศ.-NNNN` | ✓ | Document Config |
| วันที่แพ็ค | `pack.packed_at` | d MMMM พ.ศ. HH:mm น. | ✓ | ถ้ายังไม่ปิดงานใช้ `updated_at` |
| ใบสั่งขาย / เอกสารอ้างอิง | `pack.ref` (`so.code` / `transfer.code`) | — | ✓ | ป้ายชื่อเปลี่ยนตาม `src_type` |
| ใบหยิบสินค้า | `pack.pick_code` | — | ✓ | |
| ใบส่งของ | `pack.dn_ref` | — | ⬜ | ว่าง = "—" (ยังไม่ออก DN) |
| PO ลูกค้า | `so.cust_ref` | — | ⬜ | |
| คลัง / จุดแพ็ค | `pack.wh` + `pack.station` | `WH-01 · PK-01` | ✓ | |
| ผู้แพ็ค | `pack.assignee` | — | ✓ | |
| ผู้รับสินค้า (ชื่อ/ที่อยู่/รหัส/เงื่อนไขชำระ/กำหนดส่ง) | `customer.*`, `so.ship_to`, `so.term`, `so.delivery_date` | — | ✓ | pickup → เพิ่ม "ลูกค้ามารับเอง" |
| การจัดส่ง (วิธีส่ง/รถ/คนขับ/รอบ) | `pack.ship_method`, `delivery.vehicle`, `delivery.driver` | — | ⬜ | mock ในเดโม |
| ผู้หยิบ + เวลาหยิบเสร็จ | `pick.assignee`, `pick.picked_at` | — | ✓ | |
| รายการ (loop) | `pack.box[].item[]` | 1 row = 1 (สินค้า × กล่อง) | ✓ | เรียงตามเลขกล่อง |
| — ชื่อสินค้า / ของแถม | `item.name`, `so_line.is_free` | — | ✓ | ของแถมต่อท้าย "(ของแถมตามโปรโมชัน)" |
| — sub line | `item.pid`, `lot`, `exp`, `pick_location` | `รหัส · ล็อต · หมดอายุ d/m/พ.ศ. · หยิบจาก LOC` | ✓ | |
| — กล่องที่ | `box.no` | จำนวนเต็ม | ✓ | |
| — จำนวน / หน่วย | `item.qty`, `product.base_uom` | `#,##0` | ✓ | หน่วยฐาน |
| — น้ำหนัก | computed | `#,##0.00` | ✓ | `qty × unit_weight(cat)` |
| สรุปกล่อง (notes) | `pack.box[]` | `กล่อง n/N — ชนิด · ชิ้น · กก. · ป้าย CODE-nn` | ✓ | กล่องที่ยังไม่ปิดต่อท้าย "(ยังไม่ปิดกล่อง)" |
| จำนวนรายการ / ชิ้นรวม / น้ำหนักรวม | computed | `#,##0` / `#,##0.00` | ✓ | |
| จำนวนกล่องทั้งสิ้น (แถบ navy) | `count(box)` | จำนวนเต็ม | ✓ | |
| ลายเซ็น 4 ช่อง | ผู้แพ็ค / ผู้ตรวจสอบ / ผู้ส่งสินค้า / ผู้รับสินค้า | — | ✓ | COSO: Maker → Checker → ผู้ส่ง → ผู้รับ |

**ไม่มี** ราคา/VAT/ยอดเงิน — ใบแพ็คไม่ใช่เอกสารภาษี (ระบุในหมายเหตุข้อสุดท้าย)

## 3. Field Mapping — ป้ายกล่อง (100×150)

| ช่อง | Source | หมายเหตุ |
|---|---|---|
| เลขกล่อง `n/N` (ตัวใหญ่มุมขวาบน) | `box.no` / `count(box)` | อ่านจากระยะ 2 ม. |
| เลย์เอาต์ | 2 คอลัมน์: ซ้าย = ชิปเอกสาร→ผู้รับ→หมายเหตุ→บาร์โค้ด/QR · ขวา = ข้อมูลกล่อง+ตารางสินค้า→ช่องลงนาม | แนวนอนอ่านง่ายบนกล่องแบน |
| แถบชิป 3 ช่อง | `pack.dn_ref` (ไฮไลต์ navy) · `pack.ref` · `so.delivery_date` | DN ว่าง = "รอออกใบส่งของ" |
| ผู้รับ | `customer.name`, `so.ship_to` | ชื่อ 15px หนา · ที่อยู่ 11px |
| วิธีส่ง / เงื่อนไขชำระ | `pack.ship_method`, `so.term`, `so.method` | pickup → ต่อท้าย "ลูกค้ามารับเอง" |
| ข้อมูลกล่อง | `box.type/custom`, ขนาดตามชนิด, `box.weight`, `pack.assignee`, วันที่ | custom → ขนาด = "กำหนดเอง" |
| ตารางสินค้าในกล่อง | `box.item[]` + ล็อต/exp | ≤ 5 บรรทัดต่อป้าย (เกิน → ต่อ "ดูใบแพ็ค") |
| หมายเหตุขนส่ง | rule-based | สินค้าแช่เย็น (`product.cold`) → เตือนอุณหภูมิ · กล่องของแถมล้วน → "ไม่มีมูลค่าทางภาษี" · เสมอ: ตรวจนับก่อนลงนาม |
| บาร์โค้ด | `{pack.code}-{box.no:02d}` | Code128 · ความสูง 11 mm |
| QR | payload JSON: `{pack, box, dn, ref, wh}` | สแกนที่ปลายทาง/คนขับ |
| ช่องลงนาม 2 ช่อง | ผู้ส่ง/ขนส่ง · ผู้รับสินค้า+วันที่ | |
| footer | ระบบ + เวลาพิมพ์ | |

## 4. กติกาคำนวณ
- `box.weight = tare(box_type|custom) + Σ(item.qty × unit_weight(product.category))`
- `unit_weight` (mock ในเดโม): BEV 0.62 · DAIRY 1.05 · SNACK 0.09 · GROC 0.95 · HOME 0.18 กก./หน่วยฐาน → **ของจริงต้องมาจาก Item Master (`product.weight_per_base_uom`)** — OQ
- `total_weight = Σ box.weight` · `total_pieces = Σ item.qty` · `total_boxes = count(box)`
- แนะนำชนิดกล่อง: ≤60 → S · ≤200 → M · ≤600 → L · เกิน → พาเลท (ใช้ตอนเปิดกล่อง ไม่ผูกเอกสาร)

## 5. กติกาการพิมพ์
- **ใบแพ็ค**: A4 แนวตั้ง · lean type · หัวตาราง navy ตัวขาว · `thead{display:table-header-group}` ซ้ำทุกหน้า · `tr{break-inside:avoid}` · ลายเซ็น+footer ชิดล่าง (`.doc-bottom`) · หลายหน้า → footer "หน้า X / N"
- **ป้ายกล่อง**: `@page{size:150mm 100mm;margin:0}` (แนวนอน) · 1 กล่อง = 1 หน้า (`page-break-after:always`) · ไม่มีสีพื้นเต็มแผ่น (ประหยัดหมึก/ริบบอน) · บาร์โค้ดต้องเว้นขอบขาว ≥ 4 mm
- ทั้งสองใบ: ฟอนต์ Sarabun ฝัง base64 — ห้ามพึ่ง network ตอนพิมพ์หน้างาน

## 6. จุดที่เป็น placeholder ในตัวอย่าง (ต้อง bind ของจริง)
ที่อยู่/เลขผู้เสียภาษีบริษัท · ทะเบียนรถ/ชื่อคนขับ/รอบส่ง · ปริมาตร (ลบ.ม.) · เบอร์ผู้ติดต่อลูกค้า · payload QR · น้ำหนักต่อหน่วยสินค้า

## 7. Trigger การพิมพ์ (ในระบบ)
| เหตุการณ์ | เอกสารที่พิมพ์ |
|---|---|
| ปิดกล่อง (`closeBox`) | ป้ายกล่องใบนั้น 1 ใบ (auto ส่งเข้า label printer) |
| ปิดงานแพ็ค (`finishPack`) | ใบแพ็คสินค้า A4 |
| ออกใบส่งของ (`toDN`) | reprint ป้าย/ใบแพ็คได้ (มีเลข DN แล้ว) |
| เปิดกล่องแก้ไข (`reopenBox`) | ป้ายเดิมถือว่ายกเลิก — ต้องพิมพ์ใหม่หลังปิดกล่องอีกครั้ง |
