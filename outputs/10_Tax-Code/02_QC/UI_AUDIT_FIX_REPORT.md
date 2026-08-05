# Tax Code — UI Fix Report

วันที่แก้ไข: 5 สิงหาคม 2026

## ผลลัพธ์

- แก้ `TaxCode.html` ตาม defect ที่ยืนยันจาก UI audit แล้ว
- E2E regression ผ่าน 3/3 รอบ รวม 48/48 checks และไม่พบ JavaScript page error
- UI behavior confirmation ผ่าน 17/17 checks
- ตรวจภาพด้วยตาครบ 56/56 ภาพ ครอบคลุม Chromium ที่ 1280, 1440, 1920 และ 2560 พิกเซล
- ไม่พบ clipping, horizontal overflow, ตารางล้น, input เหลื่อม, dropdown หลุดจาก drawer หรือ overlay ซ้อนลำดับผิด
- Syntax check ของ `uikit.py` และ `ui-audit-tax-code.py` ผ่าน

## สิ่งที่แก้ใน TaxCode.html

1. แก้ Esc chain ให้กด Esc ครั้งแรกปิด modal และครั้งถัดไปปิด drawer ได้ทันที
2. เพิ่ม keyboard support ให้ user menu และ KPI filter cards ด้วย Enter/Space
3. เพิ่ม accessible name ให้ปุ่มแจ้งเตือน
4. เพิ่ม global `:focus-visible` สำหรับ interactive controls
5. เพิ่มปุ่มปิดที่ขวาสุดของ modal header
6. ปรับสี primary, danger และ muted text ให้มี contrast สูงขึ้น
7. ปรับ active sidebar ให้ใช้ primary token ที่เข้มขึ้น แทน `#FF3B30` แบบ hardcode

สี primary หลังผสมมีค่าประมาณ `rgb(184, 46, 39)` และ contrast กับข้อความสีขาวประมาณ `6.08:1` ซึ่งสูงกว่าเกณฑ์ WCAG AA `4.5:1` สำหรับข้อความขนาดปกติ

## การจำแนกผล UI audit confirmation

ผลอัตโนมัติรอบยืนยันก่อน patch สุดท้ายรายงาน 4 errors:

- 1 รายการเป็น defect จริง: active sidebar ยังใช้สีแดงเดิมแบบ hardcode — แก้แล้วใน HTML
- 2 รายการเป็น false positive: ตัวตรวจอ่าน computed color แบบ `color(srgb …)` ไม่ได้ จึงไล่ไปใช้สีพื้นหลัง parent ผิด — แก้ parser ใน `uikit.py` แล้ว
- 1 รายการเป็น visual-stability deviation ระดับ sub-pixel: ต่าง 7 พิกเซลจาก 1,152,000 พิกเซล (`0.000608%`) และ channel ต่างสูงสุด 1 ระดับ มองไม่เห็นด้วยตา

## ข้อจำกัดการยืนยัน

ไม่ได้รัน Playwright รอบที่สามอัตโนมัติ เพราะ `check_ui_prompt.md` กำหนดให้หยุดและรายงานเมื่อ confirmation run ยังมี finding ดังนั้น patch สุดท้ายของ active sidebar และ color parser ผ่าน static/syntax review แล้ว แต่ยังรอผู้ใช้อนุญาตรัน UI audit เพิ่มอีกหนึ่งรอบหากต้องการผล runtime ใหม่

BRD และเอกสาร downstream ยังไม่ได้เริ่มทำตามคำสั่งพักงานเดิม
