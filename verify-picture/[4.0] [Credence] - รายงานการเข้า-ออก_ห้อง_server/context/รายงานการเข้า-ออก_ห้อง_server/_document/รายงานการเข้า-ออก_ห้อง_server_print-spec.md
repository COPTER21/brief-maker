# PRINT SPEC — รายงานการเข้า-ออก ห้อง server (SRAL)

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD ของ F-TMP-006 (รหัสชั่วคราว) · **โหมด Replica** · มติทั้งหมด AI-DEFAULT (รอลูกค้ายืนยัน)
> ไฟล์คู่: `form.tpl.html` (template logic-less · แหล่งเดียวทั้ง prototype และ server) · `รายงานการเข้า-ออก_ห้อง_server_template.html` (build แล้ว ฝังฟอนต์) · `out/<state>.html`
> **[NO-BROWSER]** เครื่องที่ทำรอบนี้ไม่มี browser → ยังไม่มี PDF/ภาพ states sheet/compare — ต้องรัน `render_states.py --max-pages 2` + `compare_original.py` บนเครื่องที่มี browser ก่อน UAT

## 1. สรุป
- **ประเภทเอกสาร:** รายงานการเข้า-ออก ห้อง server / Server Room Access Log
- **ขนาด:** A4 แนวตั้ง **2 หน้า** (R10) — ต้นฉบับ Excel A4 แนวนอน 1 หน้า 21 แถว · engine กลาง (base.css) รองรับแนวตั้งเท่านั้น + ช่องลายเซ็นเป็นข้อความระบบ 2 บรรทัด → 12 แถวต่อหน้า · หัวตารางซ้ำทุกหน้า
- **ฟอนต์:** Sarabun 8pt (ขั้นต่ำตาม R10 — ไม่บีบต่ำกว่านี้) · ชื่อเอกสาร 14pt
- **หมึก:** ตาม profile (หมึกเดียว) · ไม่ใช้สี CI ในเนื้อฟอร์ม

## 2. Field Mapping
| ช่องในเอกสาร | Source (entity.field) | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| โลโก้ | Organization snapshot ตอนออกเลข → `company.logo` | data URI | ✓ | ต้นฉบับเป็นรูปฝังมุมซ้ายบน |
| ชื่อเอกสาร | `doc.title` (DOCCFG name_th) | ข้อความ | ✓ | "รายงานการเข้า-ออก ห้อง server" |
| ชื่อ–นามสกุล | `entries[].visitor_name` | ข้อความ | ✓ | พนักงาน = Employee.full_name · บุคคลภายนอก = พิมพ์เอง |
| ฝ่าย/แผนก | `entries[].visitor_department` | ข้อความ | ✓ | |
| วันที่เข้า · เวลาที่เข้า | `entries[].in_date` · `in_time` | DD/MM/YYYY (พ.ศ.) · HH:MM | ✓ | |
| วันที่ออก · เวลาที่ออก | `entries[].out_date` · `out_time` | DD/MM/YYYY (พ.ศ.) · HH:MM | ปิดรอบ ✓ | ว่างได้ระหว่างอยู่ในห้อง (DEC-04) |
| เหตุผลการเข้าใช้ | `entries[].purpose` | ข้อความ | ✓ | |
| ลายเซ็นผู้เข้า | `entries[].visitor_signed` + `visitor_signed_at` | ชื่อ + "ลงชื่อในระบบ dd/mm/yyyy HH:MM" | ✓ | แทนลายมือชื่อ (DEC-07) |
| ลายเซ็นผู้รับรอง | `entries[].certified_by` + `certified_at` | ชื่อ + "รับรองในระบบ dd/mm/yyyy HH:MM" | ปิดรอบ ✓ | เจ้าหน้าที่ IT ผู้ดูแลห้อง · ≠ ผู้เข้า (DEC-13) |
| เลขที่ · หน้า | `doc.no` · `pages[].page_no/page_total` | SRAL-YYYY-NNNN · "หน้า 1/2" | ✓ | ทุกหน้า |
| Doc No./Rev. | `doc.form_code` · `doc.revision` | FM-ITS-09 · Rev.00 : 01/07/2569 | ✓ | footer ขวา |

## 3. กติกาคำนวณ / จัดรูป (ทำใน data ไม่ใช่ template)
- ไม่มีสูตร · วันที่/เวลาส่งเป็น string ที่จัดรูปแล้ว
- แถว: เติมแถวว่างจนครบ `min_rows` = 21 แล้วปัดขึ้นเต็มหน้า (`pad_rows_to_page`) → แบ่งหน้า `rows_per_page` = 12 (หน้า 1 = 12 · หน้า 2 = 12) · `pages[].is_cont` = หน้าต่อ · `has_next` = มีหน้าถัดไป
- ≤ 24 แถว = 2 หน้า · > 24 แถว = หน้า 3 อัตโนมัติ (หัวตารางซ้ำ) + `layout.dense`

## 4. กติกาการพิมพ์
- `.page-break` ตั้งใจก่อนตารางหน้า 2 · หน้า 2 มีบรรทัด "ชื่อเอกสาร · เลขที่ … (ต่อ)" + หัวตารางซ้ำ
- ท้ายหน้า 1 "มีต่อหน้าถัดไป" · ทุกหน้า "เลขที่ … · หน้า X/N"
- ไม่มีบล็อกลงชื่อท้ายใบ (กระดาษไม่มี · ไม่มีการอนุมัติ DEC-03)
- `tr { break-inside:avoid }` · หัวตาราง `thead` ซ้ำ

## 5. วิธี build ใหม่
```bash
python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "รายงานการเข้า-ออก ห้อง server" --max-pages 2
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/submitted.pdf -o out/compare
```

## 6. Checklist ก่อนส่งมอบ
- [x] parity JS ↔ Python IDENTICAL 5/5
- [x] ไม่มี {{…}} หลง · ไม่มี key ขาดใน data (render_doc --strict 5/5)
- [x] ทุกสถานะออกแบบ 2 หน้าเท่ากัน (โครง data: 12 + 12 แถว)
- [ ] [NO-BROWSER] ยืนยันจำนวนหน้าจริงจาก PDF (`--max-pages 2`) · ภาพ `_states_sheet.png`
- [ ] [NO-BROWSER] compare_original กับต้นฉบับ

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `9. FM-ITS-09 แบบฟอร์มรายงานการเข้า-ออก ห้อง server.xlsx` (→ `orig/SAMPLE.pdf` ผ่าน LibreOffice) · Doc No. FM-ITS-09 · Rev.00 : 01/07/2569
- Profile: `form_fs 8pt` · `form_title_fs 14pt` · `form_logo_h 12mm` · `form_grid_row_h 9mm` · gap กระชับ
- ความต่างจากกระดาษ (ตั้งใจ):
  1. แนวนอน 1 หน้า 21 แถว → แนวตั้ง 2 หน้า 24 แถว (R10) — คอลัมน์/ถ้อยคำ/ลำดับเหมือนเดิม 1:1
  2. footer ซ้าย "เลขที่ … · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE" + "หน้า X/N"
  3. ลายเซ็นผู้เข้า/ผู้รับรองเป็นข้อความจากระบบ (ชื่อ + วันเวลา) ไม่ใช่ลายมือ
  4. ตัดช่องว่างท้าย "เหตุผลการเข้าใช้" (DEC-14)
- ผล compare_original: **ยังไม่ได้รัน [NO-BROWSER]** — คาดว่า WARN เพราะเปลี่ยนแนวกระดาษ (ต้องมีคนดูภาพวางคู่)

## 8. (Replica) Data contract + สถานะที่ทดสอบ
| key | source | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| company.name / company.logo | Organization snapshot | บริษัท ตัวอย่าง จำกัด / data URI | ตัวอย่างใช้ placeholder ไม่ใช่โลโก้ลูกค้า |
| doc.title / no / is_draft / is_cancelled / form_code / revision | SRAL record + DOCCFG | SRAL-2569-0003 | boolean ใช้เป็น section เท่านั้น |
| pages[].rows[] (11 key ต่อแถว) | entries[] | ดู §2 | แถวว่าง = "" ทุก key |
| pages[].page_no / page_total / is_cont / has_next | คำนวณใน data | "1" / "2" / false / true | |
| layout.dense | แถวที่มีข้อมูล > 24 | false | |
| sign_rows | sign_rows.py (DOA) | [] | ไม่มี DOA (DEC-03) — ถ้าเพิ่มภายหลัง ช่องงอกเองไม่แก้ template |
- parity JS ↔ Python: **IDENTICAL 5/5**
- สถานะ (ข้อมูลสมมติทั้งหมด): `draft` (3 แถว · มีแถวยังไม่ออก) · `submitted` (12 แถว · ปิดรอบครบ) · `pending-cert` (แถวรอรับรอง/ยังไม่ออก) · `long-24rows` (24 แถว เต็ม 2 หน้า) · `cancelled` (ยกเลิก) → ทุกสถานะ 2 หน้า
- สถานะ "ไม่อนุมัติ" และ "DOA 6 ขั้น" **ไม่ใช้กับเอกสารนี้** — ไม่มีการอนุมัติ (DEC-03) จึงไม่มีช่องลงชื่อท้ายใบ

## 9. (Replica) print_config
```json
{
  "doc_type": "SRAL",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-ITS-09",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "paper_note": "ต้นฉบับ A4 แนวนอน (Excel) 21 แถว · engine กลางรองรับ A4 แนวตั้งเท่านั้น (base.css) → ออกแบบ 2 หน้าตาม R10 · หัวตารางซ้ำทุกหน้า",
  "pages": 2,
  "rows_per_page": 12,
  "page_break": "ก่อนแถวที่ 13 (ตารางหน้า 2 มีหัวตารางซ้ำ + บรรทัดชื่อเอกสาร/เลขที่ (ต่อ))",
  "min_rows": 21,
  "pad_rows_to_page": true,
  "dense_when_rows_over": 24,
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [],
  "sign_note": "กระดาษไม่มีช่องลงชื่อท้ายใบ (DEC-03 ไม่มีการอนุมัติ · DEC-07) — ลายเซ็นผู้เข้า/ผู้รับรอง พิมพ์เป็นข้อความระบบในคอลัมน์ต่อแถว (ชื่อ + 'ลงชื่อในระบบ'/'รับรองในระบบ' + วันเวลา)",
  "decision_words": { "default": { "approve": "อนุมัติ", "reject": "ไม่อนุมัติ" }, "by_role": {} },
  "config_reads": {},
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc. No. : {form_code} · {revision}",
  "sign_layout": { "source": "ไม่มี (no DOA)", "max_per_row": 4, "split": "even", "dense_when_steps_over": 4, "keep_together": true }
}
```
