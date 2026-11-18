# PRINT SPEC — แบบประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าในประเทศ (SDA) · Replica FM-SAL-20
> โหมด Replica · template `form.tpl.html` (logic-less) · profile `profile.json` · print_config `print_config.json` · data ตัวอย่าง `make_data.py` (ข้อมูลสมมติ · โลโก้ placeholder)
> ⚠️ NO-BROWSER: เครื่องที่ทำงานไม่มี browser → ไม่ได้ render PDF ในชุดนี้ (มีแค่ HTML ต่อสถานะใน `out/`) · ต้องรัน `render_states.py … --max-pages 1` + `compare_original.py` ซ้ำบนเครื่องที่มี browser

## 1. หน้ากระดาษ
A4 แนวตั้ง · 1 หน้า (ต้นฉบับ Word 1 หน้า · 5 หัวข้อ — ไม่เกิน A4 จึงไม่ใช้ R10 2 หน้า) · ไม่มีบล็อกลงชื่อ (DEC-03/07)

## 2. Field map → data contract
| ช่องบนกระดาษ | key | source | format |
|---|---|---|---|
| โลโก้ | company.logo | Organization snapshot ตอนออกเลข | data URI |
| ชื่อเอกสาร | doc.title | FORM_SPEC.form.title | text |
| ประจำเดือน | period_month_text | survey.period_month | เดือนเต็ม พ.ศ. "มีนาคม 2569" |
| ชื่อลูกค้า | customer.name | Customer master (customerId) snapshot | text |
| วันที่ | survey_date_text | survey.survey_date | วัน เดือนเต็ม พ.ศ. |
| หัวตาราง 2 ชั้น (รายละเอียด · ระดับความพึงพอใจ: มากที่สุด/มาก/ปานกลาง/น้อย/ควรปรับปรุง) | — | คงที่ใน template (= FORM_SPEC.choices options) | text |
| 5 หัวข้อ × 5 ระดับ | items[].label · s5…s1 | score.q1…q5 (5=มากที่สุด … 1=ควรปรับปรุง) | "✓" ช่องที่เลือก · "" ช่องอื่น |
| ข้อเสนอแนะเพิ่มเติม | comment_lines[].text | survey.comment — backend ตัดบรรทัด ~110 ตัวอักษร เติมว่างครบ 5 | text |
| footer ซ้าย | doc.no · doc.is_draft · doc.is_cancelled | ENG-DOC-NUM · สถานะ | "เลขที่ … · ร่าง/ยกเลิก · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE" |
| footer ขวา | doc.form_code · doc.revision | print_config | "Doc No.FM-SAL-20 · Rev.00 : 01/07/2569" |
| layout.dense | — | ข้อเสนอแนะ > 5 บรรทัด | bool (เงื่อนไข section เท่านั้น) |

## 5. สถานะที่ทำ (parity IDENTICAL 5/5 · ไม่มี {{}} หลง · ไม่มี key ขาด)
| สถานะ | สิ่งที่ต้องเห็น |
|---|---|
| draft | footer "· ร่าง" · ให้ระดับ 2/5 ข้อ · ช่องที่ยังไม่กรอกว่าง |
| recorded | ครบทุกช่อง |
| low-score | ระดับ น้อย/ควรปรับปรุง 3 ข้อ (เข้าเกณฑ์ event `sda_low_score_recorded`) |
| long-comments | ข้อเสนอแนะ 9 บรรทัด → `layout.dense` · ยังต้อง 1 หน้า |
| cancelled | footer "· ยกเลิก" |
- สถานะ DOA หลายขั้น: **ไม่ใช้** — เอกสารไม่มีการอนุมัติ/ช่องลงชื่อ (DEC-03)

## 7. ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ `20. FM-SAL-20 …docx` (Rev.00 : 01/07/2569) · ภาพต้นฉบับจาก LibreOffice ไม่มีฟอนต์ไทย (กล่อง) → ตำแหน่งเทียบได้ ถ้อยคำเทียบไม่ได้
- compare (ตรวจนอกเครื่อง user ด้วยภาพ PDF ที่ render ในคอนเทนเนอร์ ไม่ได้แพ็ก) = **0.445 WARN** (บรรทัดตรง 6/15 · cols 0.55) — เหตุผล: (1) ต้นฉบับเป็นกล่องแทนอักษรไทย หัวเรื่องจึงกว้างจนขึ้น 2 บรรทัด (ของเรา 1 บรรทัด) (2) ข้อเสนอแนะต้นฉบับเป็นจุดไข่ปลาชิดกัน 5 บรรทัด ของเราเป็นบรรทัดเขียนได้จริง ระยะ 1 บรรทัดข้อความ (3) footer ต้นฉบับเป็นภาพที่อยู่บริษัท/เว็บไซต์ (ภาพฝัง header/footer Word) — ระบบใช้ footer มาตรฐาน · ดูภาพวางคู่แล้ว โครงตรง (โลโก้ → หัวเรื่อง → ประจำเดือน → ชื่อลูกค้า+วันที่ → ตาราง 2 ชั้น 5 ข้อ × 5 ระดับ → ข้อเสนอแนะ 5 บรรทัด → Doc No./Rev.)
- ตั้งใจต่าง: (1) วันที่ไว้บรรทัดเดียวกับชื่อลูกค้า (ต้นฉบับเส้นประของวันที่ล้นขึ้นบรรทัดใหม่) (2) footer ระบบซ้าย · Doc No. ขวา (3) ภาพที่อยู่ท้ายกระดาษของลูกค้าไม่ใส่ (ระบบใช้ข้อมูล Organization)
- profile: form_fs 11pt · lh 1.5 · title 16pt · logo 18mm · grid row 10mm · head bg ขาว (ตามกระดาษ)

## 8. print_config → F-DOCCFG
`print_config.json` (doc_type SDA · form_code FM-SAL-20 · sign_boxes [] · min_rows 5 = บรรทัดข้อเสนอแนะ · score_scale 5–1 + ป้ายคำ)

## 9. ภาพประกอบ (NO-BROWSER)
- `_states_sheet.png` + `compare_preview/` = render ในคอนเทนเนอร์ Claude (Playwright) จาก HTML ต่อสถานะใน `out/` — ใช้ดูหน้าตาเท่านั้น · ทุกสถานะ 1 หน้า · PDF ทางการต้อง render ซ้ำบนเครื่องที่มี browser (`render_states.py … --max-pages 1`)
- `orig/out/content.html` = ถ้อยคำ/ตารางที่ to_image.py สกัดจาก docx
