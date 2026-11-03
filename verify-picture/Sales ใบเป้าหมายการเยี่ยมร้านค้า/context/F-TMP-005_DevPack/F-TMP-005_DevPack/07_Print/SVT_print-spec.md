# PRINT SPEC — ใบเป้าหมายการเยี่ยมร้านค้า : เขตการขาย General Trade (SVT)

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD/Brief ของ F-TMP-005
> ไฟล์คู่: `SVT_template.html` (master, fonts ฝัง) · `out/*.html` (ทุกสถานะ) — [NO-BROWSER] ยังไม่มี PDF ตัวอย่าง
> **โหมด:** Replica (แบบฟอร์มลูกค้า FM-SAL-09)

## 1. สรุป
- **ประเภทเอกสาร:** ใบเป้าหมายการเยี่ยมร้านค้า (แผนเยี่ยมร้านรายวันของพนักงานขาย ต่อรอบการขาย)
- **ขนาด:** ต้นฉบับ **A4 แนวนอน** · แบบพิมพ์รอบนี้ A4 แนวตั้ง (ข้อจำกัดสกิล — ดู §7) · ฟอนต์ Sarabun ฝัง base64
- **Renderer:** Playwright/Chromium (`render_pdf.py`) — รอบนี้ข้าม (NO-BROWSER)

## 2. Field Mapping
ดู `SVT_data-contract.md`

## 3. กติกาคำนวณ
- `customer_count` = จำนวนร้านของวันนั้น (DEC-14) · `totals.customers` = รวมทุกวัน · `totals.work_days` = จำนวนแถวที่มีวันที่ (DEC-17)
- ร้าน ≤ 7 → ช่องละร้าน · ร้าน > 7 → 6 ช่องแรกช่องละร้าน ช่องที่ 7 ต่อชื่อที่เหลือ (DEC-15)
- ตารางพิมพ์ 31 แถวเสมอ (แถวว่างตามกระดาษ) · เรียงตามวันที่

## 4. กติกาการพิมพ์
- ตารางลงนามห่อ `.signs-block` ไม่ตัดข้ามหน้า · ขั้น DOA > 4 = dense

## 5. วิธี build ใหม่
```bash
python3 make_print.py                         # สร้าง form.tpl.html + *.data.json (ข้อมูลสมมติ)
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "ใบเป้าหมายการเยี่ยมร้านค้า"
python3 $TD/scripts/build_html.py form.tpl.html --mode replica --profile profile.json -o SVT_template.html
```

## 6. Checklist ก่อนส่งมอบ
- [x] parity IDENTICAL 5/5 · ไม่มี {{}} หลง (render_doc --strict)
- [x] ลายเซ็นครบสาย (ผู้นำเสนอ + DOA N ขั้น) · DOA 6 ขั้น = 7 ช่อง 2 แถว (4+3)
- [ ] จำนวนหน้า / compare_original — รอเครื่องที่มี browser
- [ ] แนวกระดาษ A4 landscape — รอสกิล thai-doc รองรับ orientation

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `ใบเป้าหมายการเยี่ยมร้านค้า.xlsx` (sheet FM-SAL-09 · print area B1:P44) · Doc No. `FM-SAL-09` · Rev. `Rev.00:01/07/2569` · 1 หน้า A4 แนวนอน
- Profile: `profile.json` — form_fs 8pt · title 12pt · โลโก้ซ้าย 9mm · grid row 5mm (dense 4.4mm) · หัวตารางพื้นขาวตามกระดาษ
- ความต่างจากกระดาษ (ตั้งใจ / ข้อจำกัด):
  - **แนวกระดาษ:** thai-doc v2.1 `base.css` ล็อก `@page A4 portrait` และ profile ไม่มี token orientation → แบบพิมพ์ prototype เป็นแนวตั้ง (ตาราง 15 คอลัมน์แคบลง ชื่อร้านตัดบรรทัด) · `print_config.paper = A4-landscape` ให้ server ตั้งตามต้นฉบับ — **แจ้งเจ้าของสกิลเพิ่ม token orientation**
  - ความกว้างคอลัมน์ใช้ attribute `<col width>` (ไม่ใช่ style) ประมาณสัดส่วนจาก xlsx
  - หัว TO/CC/ผู้รับผิดชอบเขต/ตำแหน่ง/เขต/รอบการขาย ทำเป็นตารางกรอบ (กระดาษเป็นกรอบ + เส้นใต้)
  - ช่องผู้อนุมัติเพิ่มตามขั้น DOA (ค่าเริ่ม 2 = เท่ากระดาษ) · บรรทัดคำตัดสิน ☐ อนุมัติ ☐ ไม่อนุมัติ · ข้อความ "ส่งในระบบ/พิจารณาในระบบ" แทนลายมือ · footer เลขที่เอกสาร
  - แถวรวมท้ายตาราง (กระดาษว่าง) แสดงจำนวนวันทำงาน + จำนวนลูกค้ารวม (DEC-17)
  - แถว 30–31 พิมพ์รูปแบบเดียวกับแถว 1–29 (มี "=") (DEC-13)
- ผล compare_original: [NO-BROWSER] ข้าม (ต้องใช้ PDF จาก browser)

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- ตาราง contract: `SVT_data-contract.md`
- parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: draft (5 วัน) · approved (22 วัน · 2 ขั้น) · rejected (ขั้น 2 ไม่อนุมัติ) · long-31rows (31 วัน · บางวัน 12 ร้าน) · approved-doa6steps (7 ช่อง 2 แถว 4+3)

## 9. (Replica) print_config
ดู `print_config.json`
