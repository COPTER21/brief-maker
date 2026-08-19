# PRINT SPEC — ใบแพ็คสินค้า (PACKSLIP)

> ไฟล์คู่: `PACKSLIP_template.html` + `PACKSLIP_sample.pdf`

## 1. สรุป

- ประเภทเอกสาร: ใบแพ็คสินค้า / Packing Slip
- ขนาด: A4 แนวตั้ง 210×297 mm, ขอบ 14 mm
- ฟอนต์: Sarabun ฝังใน HTML
- Renderer: Playwright/Chromium, `print_background`, `prefer_css_page_size`
- ไม่มีราคา, VAT หรือยอดเงิน เพราะไม่ใช่เอกสารภาษี

## 2. Field Mapping

| ช่องในเอกสาร | Source | Format | บังคับ |
|---|---|---|---|
| เลขที่ใบแพ็ค | `pack.code` | document number จากระบบ | ✓ |
| วันที่แพ็ค | `pack.packed_at` หรือ `updated_at` | d MMMM พ.ศ. HH:mm น. | ✓ |
| เอกสารต้นทาง | `pack.source_type`, `pack.source_ref` | SO; Transfer รอข้อสรุป OQ | ✓ |
| ใบหยิบสินค้า | `pack.pick_code` | — | เมื่อมาจาก Picking |
| ใบส่งของ | `pack.dn_ref` | ว่างแสดง `—` | ไม่บังคับ |
| คลัง / จุดแพ็ค | `pack.warehouse`, `pack.station` | `WH-01 · PK-01` | ✓ |
| ผู้แพ็ค | `pack.assignee` | snapshot ชื่อ | ✓ |
| ผู้รับ / ที่อยู่ส่ง | `customer.*`, `sales_order.ship_to_snapshot` | snapshot | ✓ |
| รายการ | `pack_boxes[].items[]` | เรียง box no.; 1 row ต่อสินค้า×กล่อง | ✓ |
| lot / expiry / location | item allocation snapshot | วันที่ พ.ศ. | ตามสินค้า |
| น้ำหนัก | `box.tare_weight + Σ(qty × weight_per_base_uom)` | `#,##0.00` กก. | ✓ |
| สรุป | computed | จำนวนรายการ/ชิ้น/น้ำหนัก/กล่อง | ✓ |
| ลายเซ็น | packer/checker/shipper/receiver | 4 ช่อง | ✓ |

## 3. กติกาคำนวณ

- `box_weight = tare_weight + Σ(qty × product.weight_per_base_uom)`
- `total_weight = Σ(box_weight)`
- `total_pieces = Σ(box_item.qty)`
- `total_boxes = count(pack_boxes)`
- น้ำหนักต่อหน่วยจริงต้องมาจาก Item Master; ค่า mock ในตัวอย่างห้ามใช้ใน production

## 4. กติกาการพิมพ์

- A4 แนวตั้ง, lean type 9pt, หัวตาราง navy และลายเซ็น/footer ชิดล่าง
- `thead` ซ้ำเมื่อหลายหน้า; ห้ามตัด row กลางหน้า
- Trigger: ปิดงานแพ็คสำเร็จ; reprint ได้ตามสิทธิ์และต้องบันทึก audit
- เลขเอกสารต้องมาจาก contract กลางที่ระบบกำหนด ห้าม generate ใน client

## 5. วิธี regenerate

```powershell
.tools/python.cmd .agents/skills/thai-doc-pdf-generator/scripts/build_html.py outputs/03_PACK/06_PRINT/_source/PACKSLIP_body.html --title "ใบแพ็คสินค้า" -o outputs/03_PACK/06_PRINT/PACKSLIP_template.html
.tools/python.cmd .agents/skills/thai-doc-pdf-generator/scripts/render_pdf.py outputs/03_PACK/06_PRINT/PACKSLIP_template.html -o outputs/03_PACK/06_PRINT/PACKSLIP_sample.pdf
```

## 6. Checklist

- [x] A4 และ font ฝังในไฟล์
- [x] ไม่มีราคา/VAT
- [x] จำนวนและน้ำหนักชิดขวา
- [x] สรุป reconcile กับรายการตัวอย่าง
- [x] ลายเซ็น 4 ช่อง
- [ ] เปลี่ยนข้อมูลบริษัทและข้อมูลลูกค้าตัวอย่างเป็นข้อมูลจริงตอน bind
