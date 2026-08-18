# PRINT SPEC — ใบหยิบสินค้า (PICK)

> ไฟล์คู่: `PICK_template.html` สำหรับ bind ข้อมูล และ `PICK_sample.pdf` สำหรับตรวจรูปแบบ A4

## 1. รูปแบบเอกสาร

- A4 แนวตั้ง 210×297 มม. ขอบ 14 มม.
- ฟอนต์ Sarabun ฝังใน HTML และพิมพ์พื้นหลัง
- เรียงรายการตามเส้นทางคลัง: Pick Face → Reserve → Bulk แล้วจึง FEFO/FIFO
- ไม่มีราคา ภาษี ยอดเงิน หรือสายอนุมัติ เพราะเป็นเอกสารปฏิบัติงานคลัง

## 2. Field mapping

| ช่อง | Source | Format / หมายเหตุ |
|---|---|---|
| เลขใบหยิบ | `pick.code` | รหัสจากระบบเอกสารของฟีเจอร์ |
| วันที่สร้าง | `pick.created_at` | วันไทย พ.ศ. + เวลา |
| คลัง | `pick.warehouse_code` → Warehouse Master | แสดง code + name |
| SO อ้างอิง | `pick.sales_orders[].code` | รองรับหลาย SO ใน wave |
| ผู้หยิบ / อุปกรณ์ | `pick.assignee`, `pick.equipment` | snapshot ตอนพิมพ์ |
| ตำแหน่ง | `pick.lines[].location_code` | ผ่าน hard eligibility แล้ว |
| สินค้า | `pick.lines[].item_code/name` | ไม่รวม service item |
| ล็อต / วันหมดอายุ | `pick.lines[].lot_no/expiry_date` | ว่างได้เฉพาะสินค้าที่ไม่คุมล็อต |
| จำนวน / หน่วยฐาน | `pick.lines[].qty_base/uom_base` | จำนวนชิดขวา |
| หน่วยขาย | `pick.lines[].source_qty/source_uom/factor` | แสดงบรรทัดรองเพื่อช่วยตรวจ |
| ช่องตรวจ | ค่าเปล่า | สำหรับติ๊กเมื่อใช้กระดาษ |

## 3. กติกา bind และพิมพ์

- หัวตารางซ้ำทุกหน้า และห้ามตัดแถวรายการกลางหน้า
- เรียงด้วย route sequence ที่ Pick คำนวณไว้ ห้ามให้ template คำนวณ FEFO/FIFO ใหม่
- แสดงเฉพาะแหล่ง SO; customer pickup ยังเดิน Pack → Delivery Note ตามปกติ
- หากตำแหน่งถูกเปลี่ยนหรือปิดขาดหลังพิมพ์ ต้องพิมพ์ฉบับใหม่และแสดงเวลาสร้างล่าสุด
- ลายเซ็น 3 ช่อง: ผู้หยิบ, ผู้ตรวจรับ Packing, หัวหน้าคลัง

## 4. วิธี regenerate

```powershell
.tools\python.cmd .agents\skills\thai-doc-pdf-generator\scripts\build_html.py outputs\16_Picking\_qa\PICK_body.html --title "ใบหยิบสินค้า" -o outputs\16_Picking\PICK_template.html
.tools\python.cmd .agents\skills\thai-doc-pdf-generator\scripts\render_pdf.py outputs\16_Picking\PICK_template.html -o outputs\16_Picking\PICK_sample.pdf
```

## 5. Checklist

- [ ] A4 ไม่ล้นและส่วนลายเซ็นอยู่ท้ายหน้า
- [ ] ตำแหน่ง/สินค้า/ล็อต/วันหมดอายุ/จำนวนอ่านได้ชัด
- [ ] ลำดับรายการตรง route sequence จาก Pick
- [ ] ไม่มีราคาและยอดเงิน
- [ ] ข้อมูลคลังและผู้หยิบเป็น snapshot ณ เวลาพิมพ์
