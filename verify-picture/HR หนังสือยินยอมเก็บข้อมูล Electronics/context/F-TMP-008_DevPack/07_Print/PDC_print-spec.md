# PRINT SPEC — หนังสือยินยอมในการเก็บรวบรวม ใช้ และเปิดเผยข้อมูลส่วนบุคคล (PDC)

> ไฟล์คู่: `PDC_template.html` (master, fonts ฝัง) + `out/*.html` (5 สถานะ) · **โหมด: Replica**
> ⚠ รอบนี้รันในเครื่องที่ไม่มี browser (NO-BROWSER) → ยังไม่ได้ PDF · ต้องรัน `render_states.py` + `compare_original.py` ซ้ำบนเครื่องที่มี browser ก่อนส่งลูกค้า

## 1. สรุป
- **ประเภทเอกสาร:** หนังสือยินยอมในการเก็บรวบรวม ใช้ และเปิดเผยข้อมูลส่วนบุคคล / Personal Data Consent Form
- **ขนาด:** A4 แนวตั้ง (210×297mm), ขอบ 14mm · ต้นฉบับ 2 หน้า
- **ฟอนต์:** Sarabun (ฝัง base64) · **CI:** Replica — หมึกเดียวตาม profile ลูกค้า (ไม่ใช้สี CI CUBE ในเนื้อฟอร์ม)
- **Renderer:** Playwright/Chromium (`print_background`, `prefer_css_page_size`)

## 2. Field Mapping — ดู `PDC_data-contract.md` (เอกสารนี้มี 3 ช่องกรอก + ตารางความยินยอม 8 ข้อ)

| ช่องในเอกสาร | Source | Format | บังคับ |
|---|---|---|---|
| ข้าพเจ้า นาย/นาง/นางสาว | `consent.data_subject_name` | ข้อความ | ✓ |
| ความยินยอม ข้อ 1-8 | `consent.lines[].choice` → ☑/☐ | glyph | ✓ ทุกข้อ |
| ( ) ใต้ลายเซ็น | computed จากชื่อเจ้าของข้อมูล | ข้อความ | ✓ |
| วันที่ | `consent.consented_at` (ระบบใส่ตอนยืนยัน) | วัน เดือน(ไทย) พ.ศ. | ✓ |
| เลขที่เอกสาร | ENG-DOC-NUM `PDC-พ.ศ.-running` | — | ✓ |

## 3. กติกาคำนวณ
ไม่มีการคำนวณตัวเลข · กติกาที่บังคับคือ **ความครบของการเลือก**: ข้อ 1-8 ต้องมีคำตอบทุกข้อ และเลือกได้ข้อละ 1 ช่อง (DEC-13)

## 4. กติกาการพิมพ์
- A4 แนวตั้ง · 9pt (profile) · ตารางความยินยอมเป็นตารางกรอบ (R9 `.form-grid`) · `tr { break-inside:avoid }`
- บล็อกลงชื่อห่อ `.signs-block` ไม่ตัดข้ามหน้า · footer ชิดล่าง (`.doc-bottom`)
- ความยินยอมเป็นถ้อยคำกฎหมาย — ห้ามตัดคำ ห้ามย่อ ห้ามเรียบเรียง

## 5. วิธี build ใหม่
```bash
python3 scripts/render_doc.py form.tpl.html <state>.data.json -o out/<state>.body.html --strict
python3 scripts/build_html.py out/<state>.body.html --mode replica --profile profile.json --title "…" -o out/<state>.html
# เครื่องที่มี browser:
python3 scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "…" --max-pages 2
python3 scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare --region 0:0.80
```

## 6. Checklist ก่อนส่งมอบ
- [x] parity JS ↔ Python IDENTICAL 5/5
- [x] ไม่มี `{{}}` หลงเหลือทุกสถานะ (`--strict` + `check_states.js`)
- [x] ตารางความยินยอม 8 แถว · ช่องติ๊ก 16 ช่อง ทุกสถานะ
- [x] ช่องลงชื่อ dynamic (1 ช่องปกติ · 7 ช่องเมื่อ chain 6 ขั้น)
- [ ] **ค้าง (NO-BROWSER):** PDF ทุกสถานะ · จำนวนหน้า · `_states_sheet.png` · `compare_side.png`

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `orig/หนังสือยินยอม PDPA กรณีสมัครงาน.docx` (แปลงเป็น `orig/SAMPLE.pdf` 2 หน้า) · Doc No. `FM-HRM-31` · `Rev. 00 : 01/07/2569`
- Profile token ที่ต่างจาก default: `form_fs 9pt` · `form_title_fs 12pt` · `form_logo_h 13mm` · `form_title_gap 10px` · `form_para_gap 10px/7px` · `form_grid_gap 10px` · `form_indent 10mm`
- ความต่างจากกระดาษ (ตั้งใจ + เหตุผล):
  1. **คอลัมน์เลขลำดับรวมเข้ากับคอลัมน์ "ข้อมูลส่วนบุคคล"** (แสดงเป็น "1. …") — `.form-grid` เป็น `table-layout:fixed` และ helper มีเฉพาะ `g-25/50/75` การแยกคอลัมน์เลขทำให้คอลัมน์ "ยินยอม/ไม่ยินยอม" แคบจนหัวตารางถูกตัด · ข้อมูลที่แสดงเท่าเดิมทุกตัว
  2. **บล็อกลงชื่อย้ายมาแถวล่าง** ตาม B6 (มติ 2026-10-05) และจำนวนช่องมาจาก DOA — ต้นฉบับเป็นลายมือกลางหน้า
  3. **บรรทัดวันที่ในช่องลงชื่อ** ใช้ข้อความ "ยืนยันในระบบ …" แทนลายมือ (DEC-07 ไม่ใช้ภาพลายเซ็น)
  4. **ตารางความยินยอมไม่ขึ้นหัวตารางซ้ำกลางตาราง** — ต้นฉบับซ้ำหัวตารางตรงรอยต่อหน้า 1/2 ซึ่งเป็นผลของการแบ่งหน้าใน Word ไม่ใช่โครงฟอร์ม
  5. **เพิ่มบล็อก "บันทึกการถอนความยินยอม"** แสดงเฉพาะเมื่อใบถูกถอน (DEC-14) — ไม่แสดงในใบปกติ จึงไม่กระทบความตรงกระดาษ
- ผล compare_original: **ยังไม่ได้รัน (NO-BROWSER)** — ต้องรันด้วย `--region 0:0.80` (ตัดส่วนลายเซ็นที่ตั้งใจย้าย) บนเครื่องที่มี browser

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- ตาราง contract: `PDC_data-contract.md`
- parity JS ↔ Python: **IDENTICAL 5/5**
- สถานะที่ render (HTML): ร่าง · ยืนยันแล้ว (ยินยอมทุกข้อ) · ไม่ยินยอมบางข้อ · ยาว + ถอนความยินยอม (dense) · สายลงนาม 6 ขั้น (7 ช่อง 2 แถว)
- จำนวนหน้า: **ยังวัดไม่ได้ (NO-BROWSER)** — ต้นฉบับ 2 หน้า ตั้ง `--max-pages 2` ตอนรันรอบเต็ม

## 9. (Replica) print_config — ดู `print_config.json` (doccfg-declaration อ่านต่อ)
