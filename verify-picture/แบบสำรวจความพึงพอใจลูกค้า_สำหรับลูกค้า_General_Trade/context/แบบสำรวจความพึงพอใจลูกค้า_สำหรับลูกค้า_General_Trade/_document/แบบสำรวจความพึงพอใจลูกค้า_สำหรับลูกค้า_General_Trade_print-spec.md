# PRINT SPEC — แบบสำรวจความพึงพอใจลูกค้า สำหรับลูกค้า General Trade (CSG) · Replica FM-SAL-10
> โหมด Replica · template `form.tpl.html` (logic-less) · profile `profile.json` · print_config `print_config.json` · data ตัวอย่าง `make_data.py` (ข้อมูลสมมติ · โลโก้ placeholder)
> ⚠️ NO-BROWSER: เครื่องที่ทำงานไม่มี browser → ไม่ได้ render PDF ในชุดนี้ (มีแค่ HTML ต่อสถานะใน `out/`) · ต้องรัน `render_states.py … --max-pages 1` + `compare_original.py` ซ้ำบนเครื่องที่มี browser

## 1. หน้ากระดาษ
A4 แนวตั้ง · 1 หน้า (ต้นฉบับ 1 หน้า — คอลัมน์ "1" หลุดหน้า 2 เพราะ print area ของ Excel → แก้ให้อยู่หน้าเดียว DEC-12) · ไม่มีบล็อกลงชื่อ (DEC-03/07)

## 2. Field map → data contract
| ช่องบนกระดาษ | key | source | format |
|---|---|---|---|
| โลโก้ | company.logo | Organization snapshot ตอนออกเลข | data URI |
| ชื่อเอกสาร | doc.title | FORM_SPEC.form.title | text |
| ประจำเดือน | period_month_text | survey.period_month | เดือนเต็ม พ.ศ. "มีนาคม 2569" |
| วันที่ : | survey_date_text | survey.survey_date | วัน เดือนเต็ม พ.ศ. |
| ชื่อบริษัท : | customer.name | Customer master (customerId) snapshot | text |
| ฝ่าย/แผนก : | contact.dept | survey.contact_dept | text |
| เบอร์โทร.ติดต่อ : | contact.phone | survey.contact_phone (PDPA) | text |
| หัวกลุ่ม 1)–3) | sections[].title | FORM_SPEC (คงที่) | text |
| 16 หัวข้อ × คะแนน 5 4 3 2 1 | sections[].items[].label · s5…s1 | score.q1_1…q3_8 | "✓" ช่องที่เลือก · "" ช่องอื่น |
| ข้อเสนอแนะด้านเจ้าหน้าที่ฯ | comment_staff_lines[].text | survey.comment_staff — backend ตัดบรรทัด ~105 ตัวอักษร เติมว่างครบ 3 | text |
| ข้อเสนอแนะอื่นๆ ฯ | comment_other_lines[].text | survey.comment_other — เหมือนข้างบน | text |
| footer ซ้าย | doc.no · doc.is_draft · doc.is_cancelled | ENG-DOC-NUM · สถานะ | "เลขที่ … · ร่าง/ยกเลิก · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE" |
| footer ขวา | doc.form_code · doc.revision | print_config | "Doc.No.FM-SAL-10 · Rev.00: 01/07/2569" |
| layout.dense | — | ข้อเสนอแนะ > 3 บรรทัด | bool (เงื่อนไข section เท่านั้น) |

## 5. สถานะที่ทำ (parity IDENTICAL 5/5 · ไม่มี {{}} หลง · ไม่มี key ขาด)
| สถานะ | สิ่งที่ต้องเห็น |
|---|---|
| draft | footer "· ร่าง" · ให้คะแนน 6/16 ข้อ · ช่องที่ยังไม่กรอกว่าง |
| recorded | ครบทุกช่อง (ใกล้ตัวอย่างลูกค้าที่สุด) |
| low-score | ตัวเลือกอีกทาง: คะแนน 1–3 หลายข้อ (เข้าเกณฑ์ event `csg_low_score_recorded`) |
| long-comments | ข้อเสนอแนะ 5 + 4 บรรทัด → `layout.dense` · ยังต้อง 1 หน้า |
| cancelled | footer "· ยกเลิก" |
- สถานะ DOA หลายขั้น: **ไม่ใช้** — เอกสารไม่มีการอนุมัติ/ช่องลงชื่อ (DEC-03)

## 7. ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ `10. FM-SAL-10 …xlsx` (Rev.00: 01/07/2569) · ภาพต้นฉบับจาก LibreOffice ไม่มีฟอนต์ไทย (กล่อง) → ตำแหน่งเทียบได้ ถ้อยคำเทียบไม่ได้
- compare (ตรวจนอกเครื่อง user ด้วยภาพ PDF ที่ render ในคอนเทนเนอร์ ไม่ได้แพ็ก) = **0.595 WARN** (บรรทัดตรง 9/18 · cols 0.82) — เหตุผล: ต้นฉบับเป็นกล่องแทนอักษรไทย · หัวเรื่องต้นฉบับล้นขวา · คอลัมน์ "1" ต้นฉบับหลุดหน้า · คนดูภาพวางคู่แล้ว โครงตรง (หัว → 4 บรรทัดข้อมูล → หัวข้อการประเมิน → 3 ตารางคะแนน 4/4/8 → ข้อเสนอแนะ 2 ส่วน × 3 บรรทัด)
- ตั้งใจต่าง: (1) "นัดหมายไว้่" → "นัดหมายไว้" (DEC-11) (2) ช่องคะแนน 5–1 ครบในหน้าเดียว (DEC-12) (3) ตารางคะแนนมีกรอบทั้งแถว (ต้นฉบับกรอบเฉพาะช่องคะแนน — ใช้ R9 `.form-grid` มาตรฐาน ไม่แก้ CSS รายลูกค้า) (4) footer ระบบซ้าย · Doc.No. ย้ายจาก footer Excel มา footer ขวา
- profile: form_fs 9pt · lh 1.5 · title 15pt · logo 13mm · grid row 5.6mm · head bg ขาว (ตามกระดาษ)

## 8. print_config → F-DOCCFG
`print_config.json` (doc_type CSG · form_code FM-SAL-10 · sign_boxes [] · min_rows 3 = บรรทัดข้อเสนอแนะ · score_scale 5–1)

## 9. ภาพประกอบ (NO-BROWSER)
- `_states_sheet.png` + `compare_preview/` = render ในคอนเทนเนอร์ Claude (Playwright) จาก HTML ต่อสถานะใน `out/` — ใช้ดูหน้าตาเท่านั้น · ทุกสถานะ 1 หน้า · PDF ทางการต้อง render ซ้ำบนเครื่องที่มี browser (`render_states.py … --max-pages 1`)
- `orig/content_extract.html.txt` = ถ้อยคำ/ตารางที่ to_image.py สกัดจาก xlsx (เปลี่ยนนามสกุลกันถูกนับเป็น prototype)
