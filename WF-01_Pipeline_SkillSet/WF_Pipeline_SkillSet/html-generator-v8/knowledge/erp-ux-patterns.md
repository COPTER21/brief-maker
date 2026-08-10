# ERP UX Patterns — Reference จากระบบสากล (v1.0)

> ตอบข้อเสนอ user (2026-07-27): เพิ่ม process research ERP สากล (Odoo / SAP Fiori / Dynamics 365)
> เป็น reference การวาง UX/UI — ใช้ 2 ชั้น:
> **ชั้น 1 (ไฟล์นี้ — offline เสมอ):** pattern ที่กลั่นแล้วจากระบบจริง อ่านทุกครั้งที่ gen
> **ชั้น 2 (online ถ้าทำได้):** Phase 0.5 ใน SKILL — search UI จริงของ feature type นั้นสั้น ๆ
> แล้ว log สิ่งที่หยิบใช้ · หาไม่ได้/ไม่มี network → ใช้ชั้น 1 อย่างเดียว ห้าม block การ gen

---

## หลักที่ทั้งสามเจ้าเห็นตรงกัน (ใช้เป็น default ทุก feature)

| หลัก | Odoo | SAP Fiori | D365 | เราใช้ยังไง |
|---|---|---|---|---|
| **Header = identity + สถานะ + actions** | statusbar ขวาบน + smart buttons | Object Page header facets | header + record state | drawer header เป็น identity block (#72) — สถานะเป็น pill บน header ไม่ใช่ field ในฟอร์ม (#75) |
| **เนื้อหาแบ่ง section มีหัวข้อ** | notebook tabs | sections + anchor bar | FastTabs (ยุบ/ขยาย) | tab สำหรับกลุ่มใหญ่ + section title ในแต่ละ tab (#71) |
| **List = high-density + tools ครบ** | filter/group-by/favorite | table toolbar + variant | grid + views | #63 density + #70 anatomy (stat row, chips, sortable) |
| **Field อธิบายตัวเองด้วยตัวอย่าง ไม่ใช่ย่อหน้า** | placeholder + inline example | value help ⓘ | field hint icon | #67 hint→ⓘ + #77 mock ครบ |
| **Related data = การ์ด/smart button มีตัวเลข** | smart buttons (นับ) | related apps facet | related grids | tab counts (#72) + hook cards มีจำนวน |

## Pattern เฉพาะที่กลั่นมาแล้ว — Master Data (Product/Vendor/Customer)

**Form (สร้าง/แก้ไข):**
- Odoo: ชื่อใหญ่บนสุด → แถว checkbox พฤติกรรม (can be sold / purchased) → notebook แยก
  General / Sales / Purchase / Inventory / Accounting → **เอามาใช้:** พฤติกรรมจากประเภทเป็น
  chip/toggle กลุ่มเดียวชิดกัน (ตรงภาพ vibe: นับสต๊อก·ขายได้·ซื้อได้) — ไม่กระจาย
- SAP: views ต่อ facet — basic data / units / accounting แยกชัด → **เอามาใช้:** wizard step ตามกลุ่มข้อมูล
  (ข้อมูลหลัก → หน่วยนับ → ราคา/บัญชี → สต๊อก/ไฟล์ → ยืนยัน) — step สุดท้าย = review summary (#71)
- UOM: ทุกเจ้าแสดง conversion เป็น**ความสัมพันธ์อ่านได้** ไม่ใช่ตาราง factor เปล่า →
  **เอามาใช้:** #77 compound widget (สมการ + ตัวอย่าง + role chips)

**Detail (drawer/page):**
- identity header: avatar/initial + code + ชื่อ + status pill + actions (แก้ไข/ปิดใช้งาน) ขวา
- definition grid เป็นกลุ่ม (ข้อมูลหลัก / รหัส / หน่วยนับ / ราคา / บัญชี·สต๊อก / เอกสาร)
  — ตรงกับที่ user ชี้ว่าเวอร์ชัน vibe "ดูเป็นระบบ"
- related/hook section: การ์ดต่อปลายทาง + field ที่ส่ง + ป้าย "นอกขอบเขต" — คุมด้วย 1 บรรทัด/การ์ด
  คำอธิบายแนวคิดยาว ๆ (เช่นอธิบาย self-slice) → ⓘ เดียวที่หัว section ไม่ใช่ banner เต็มจอ

## กติกาการใช้ (Phase 0.5 ใน SKILL)
1. อ่านไฟล์นี้ทุกครั้ง — เลือก pattern ตรง feature type แล้ว**บันทึกใน gen log ว่าหยิบข้อไหน**
2. มี network: search 1-2 query ("odoo <feature> form", "fiori <object> page") ดู screenshot
   → หยิบเฉพาะ **โครงการวาง** (ห้ามหยิบสี/ฟอนต์/spacing — ของเรายึด CI + กฎเราเอง)
3. ขัดกันเมื่อไหร่: กฎเรา (#1-77) > ไฟล์นี้ > ผล search สด
4. เจอ pattern ใหม่ที่ดีจาก search → เสนอเพิ่มเข้าไฟล์นี้ (ผ่าน user) — ไฟล์นี้คือ knowledge สะสม
