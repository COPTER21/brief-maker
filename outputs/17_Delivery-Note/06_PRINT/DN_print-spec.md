# PRINT SPEC — ใบส่งของ (Delivery Note)

## 1. รูปแบบ

- A4 แนวตั้ง 210×297 มม. ขอบ 14 มม.
- ฟอนต์ Sarabun ฝังใน `DN_template.html`; render ด้วย Chromium โดยเปิด background และใช้ CSS page size
- เป็นเอกสารไม่มีราคา/ภาษี แสดงเฉพาะสินค้า จำนวน หน่วย กล่อง และหลักฐานการรับ
- เลขเอกสารต้องรับจาก Document Configuration ผ่าน `ENG-DOC-NUM.next()`; ห้ามสร้างเลขรันใน feature

## 2. Field mapping

| ช่องพิมพ์ | Source | บังคับ | รูปแบบ/หมายเหตุ |
|---|---|---:|---|
| เลขที่ใบส่งของ | `delivery_note.code` | ✓ | snapshot ณ เวลาสร้าง |
| วันที่เอกสาร | `delivery_note.created_at` | ✓ | วัน เดือน พ.ศ. |
| เอกสารอ้างอิง | `delivery_note.references[]` | ✓ | หลาย SO ได้เมื่อ customer + ship-to เดียวกัน; รองรับ Stock Transfer |
| ใบแพ็ค | `delivery_note.pack_refs[]` | เฉพาะ reference | Manual แสดง `—` |
| คลังต้นทาง | `delivery_note.warehouse_code` | ✓ | รหัสคลัง |
| ผู้รับ/ที่อยู่ | recipient snapshot | ✓ | ต้องเก็บ snapshot ไม่อ่าน master ย้อนหลังตอนพิมพ์ซ้ำ |
| ขนส่ง/รถ/คนขับ | delivery snapshot | ✓ | ตามชนิดขนส่ง |
| รายการสินค้า | `delivery_note.lines[]` | ✓ | product, lot, expiry, qty, uom, box count |
| ยอดรวม | computed | ✓ | จำนวนรายการ/ชิ้น/กล่อง/น้ำหนัก ไม่มีมูลค่าเงิน |
| ผู้ลงนาม 4 ฝ่าย | signature/POD | ✓ | ผู้จัดทำ, ผู้ตรวจสอบ, ผู้ส่ง, ผู้รับ |

## 3. กฎพิมพ์

- `thead` ต้องซ้ำทุกหน้า และห้ามตัดรายการหนึ่งบรรทัดข้ามหน้า
- บล็อกสรุป ลายเซ็น และ footer ต้องไม่ถูกตัดกลาง
- พิมพ์ซ้ำต้องได้ข้อมูล snapshot เดิมและระบุสำเนาตาม policy จาก `ENG-DOC-STORE.store()`
- เอกสาร Manual ต้องติดป้าย “Manual” และไม่แสดงเลขใบแพ็คปลอม
- Stock Transfer ใช้เลขอ้างอิง TR และแสดงคลังต้นทาง → ปลายทางแทนชื่อลูกค้า

## 4. ไฟล์และวิธี regenerate

```powershell
.tools\python.cmd .agents\skills\thai-doc-pdf-generator\scripts\build_html.py outputs\17_Delivery-Note\06_PRINT\_source\DN_body.html --title "ใบส่งของ / Delivery Note" -o outputs\17_Delivery-Note\06_PRINT\DN_template.html
.tools\python.cmd .agents\skills\thai-doc-pdf-generator\scripts\render_pdf.py outputs\17_Delivery-Note\06_PRINT\DN_template.html -o outputs\17_Delivery-Note\06_PRINT\DN_sample.pdf
```

## 5. Acceptance checklist

- [x] A4 แนวตั้ง 1 หน้าใน sample และฟอนต์ไทยฝังในไฟล์
- [x] ไม่มีราคา/VAT/ยอดเงิน
- [x] ช่องลงนาม 4 ฝ่ายพร้อมวันที่
- [x] แสดงหลายเอกสารอ้างอิงและหลายใบแพ็ค
- [x] ตารางจำนวนชิดขวาและข้อมูลรับสินค้าตรวจด้วยตาได้
