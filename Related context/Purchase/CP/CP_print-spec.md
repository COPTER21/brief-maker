# PRINT SPEC — ใบเปรียบเทียบราคา (CP)

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD/Brief ของ F-CP-001 (เปรียบเทียบราคา)
> ไฟล์คู่: `CP_template.html` (master, fonts ฝัง) + `CP_sample.pdf` (ตัวอย่าง A4)

## 1. สรุป
- **ประเภทเอกสาร:** ใบเปรียบเทียบราคา / Price Comparison
- **ขนาด:** A4 แนวตั้ง (210×297mm), ขอบ 14mm
- **ฟอนต์:** Sarabun (ฝัง base64 ใน HTML — ไม่ต้องพึ่ง network)
- **CI:** CUBE NATIVE (Navy #0B1D3A / Primary #0B5CFF / Teal #00A88E)
- **Renderer:** Playwright/Chromium → `print_background`, `prefer_css_page_size`
- **ฐาน type:** ดัดแปลงจากเอกสารตาราง (QO/PO) — เพิ่มคอลัมน์ราคา/หน่วยต่อผู้ขาย + คอลัมน์ผู้ที่คัดเลือก

## 2. Field Mapping (UI/DB → ช่องในเอกสาร)

| ช่องในเอกสาร | Source (entity.field) | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่เอกสาร | cp.cp_no | `CP-พ.ศ.-running` | ✓ | running จากระบบ |
| วันที่ | cp.cp_date | วัน เดือน(ไทย) พ.ศ. | ✓ | |
| อ้างอิงใบขอซื้อ | cp.pr_refs[] | `PR-พ.ศ.-running` | ✓ | 1 CP = 1+ PR |
| ผู้จัดทำ / แผนก | cp.buyer / cp.dept | — | ✓ | |
| ผู้ขายที่เปรียบเทียบ (loop 2–3) | cp.vendors[] (vendor master) | — | ✓ | ชื่อ + เลขผู้เสียภาษี + เครดิต + ผู้ติดต่อ |
| รายการ (loop) | cp.lines[] | — | ✓ | 1 row = 1 สินค้า (ชื่อ + item_code) |
| จำนวน + หน่วย | line.qty / line.unit | `#,##0 + หน่วย` | ✓ | center |
| ราคา/หน่วย ต่อผู้ขาย | cp.prices[line][vendor] | `#,##0.00` | ✓ | ชิดขวา · ดึง preset จาก vendor price list (แก้ได้) |
| ผู้ที่คัดเลือก (winner) | cp.winners[line] | tag เขียว | ✓ | ราคาผู้ชนะ = **ตัวหนา** ในคอลัมน์ผู้ขายนั้น |
| รวมราคาที่คัดเลือก (ก่อน VAT) | computed | `#,##0.00` | ✓ | Σ(winner.qty × winner.price) |
| VAT 7% | computed | `#,##0.00` | ✓ | ฐาน = รวมก่อน VAT |
| รวมทั้งสิ้น | computed | `#,##0.00` | ✓ | ก่อน VAT + VAT |
| จำนวนเงินตัวอักษร | computed | ไทย | ✓ | baht_text(grand_total) |
| ผลแยก PO (PO Split) | derive จาก winners group by vendor | — | ✓ | 1 ผู้ขาย = 1 PO · แสดงจำนวนรายการ + ยอดต่อใบ |
| ผู้ลงนาม (3 ชั้น) | DOA resolver {feature_id:F-CP-001, cost_center, amount} | — | ✓ | Maker/Checker/Approver — **ไม่ hardcode** |

## 3. กติกาคำนวณ
- `winner_subtotal = Σ(line.qty × price[line][winner])` เฉพาะรายการที่เลือกผู้ชนะแล้ว
- `vat = round(winner_subtotal × 0.07, 2)` *(ROUND_HALF_UP)*
- `grand_total = winner_subtotal + vat`
- เกณฑ์คัดเลือก default = ราคาต่ำสุดต่อรายการ (line-by-line) — buyer override ได้ (เลือกผู้ชนะเอง)
- PO Split: group รายการที่ชนะ ตาม winner vendor → แต่ละกลุ่ม = 1 PO (ยอด = Σ ของกลุ่ม)
- จำนวนเงินตัวอักษร: `scripts/baht_text.py <grand_total>`

## 4. กติกาการพิมพ์ (ตาม Design Rules)
- A4 แนวตั้ง · lean type · หัวตาราง navy เส้นบาง · ลายเซ็น+footer ชิดล่าง (.doc-bottom)
- หัวตารางซ้ำทุกหน้า · ห้ามตัด row กลาง · ราคาชิดขวา (`.num`) · ราคาผู้ชนะ `<b>`
- ผู้ที่คัดเลือก = `<span class="tag tag--ok">ชื่อย่อผู้ขาย</span>`
- ผู้ขายเกิน 3 ราย → ตารางอาจกว้างเกิน A4 ให้ตัดเหลือ 3 รายที่เข้ารอบ หรือพิมพ์แนวนอน (นอก scope ปัจจุบัน)

## 5. วิธี build ใหม่ (regenerate)
```bash
python scripts/build_html.py cp_body.html --title "ใบเปรียบเทียบราคา CP-..." -o CP_template.html
python scripts/render_pdf.py CP_template.html -o CP_sample.pdf
```
Dev: ใช้ `CP_template.html` เป็นต้นแบบ → bind ข้อมูลตาราง §2 → render ด้วย engine ที่ honor `@page` + Sarabun

## 6. Placeholder ที่ใช้ในตัวอย่าง (ต้องแทนค่าจริงตอน bind)
- ที่อยู่/โทร/อีเมล/เลขผู้เสียภาษี บริษัท + ผู้ขายทั้ง 3 = placeholder
- ผู้ลงนาม (ตำแหน่ง) = placeholder รอ DOA resolve · เลขที่ CP/PR + วันที่ = ตัวอย่าง
- ราคา/หน่วยทั้งหมด = ตัวอย่างจาก vendor price list mock

## 7. Checklist ก่อนส่งมอบ
- [x] A4 พอดี ไม่ล้นหน้า
- [x] ตัวเลขชิดขวา + `#,##0.00` · ราคาผู้ชนะตัวหนา
- [x] VAT/ยอดรวม ถูกต้อง (13,700.00 + 959.00 = 14,659.00) + ตัวอักษรตรงยอด
- [x] ผลแยก PO ตรงกับผู้ชนะ (สยามออฟฟิศ 9,050 / ที.เค. 4,650)
- [x] ลายเซ็นครบ 3 สาย + วันที่
