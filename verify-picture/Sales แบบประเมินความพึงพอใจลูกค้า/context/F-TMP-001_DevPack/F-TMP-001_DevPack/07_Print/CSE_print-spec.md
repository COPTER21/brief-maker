# PRINT SPEC — แบบประเมินความพึงพอใจลูกค้า (CSE) · Replica FM-SAL-06
> โหมด Replica · template `form.tpl.html` (logic-less) · profile `profile.json` · print_config `print_config.json` · มติ AI-DEFAULT ทุกข้อ (รอลูกค้ายืนยัน)
> ⚠️ **[NO-BROWSER]** รอบนี้ไม่มี browser ในเครื่อง → ข้าม `render_pdf.py` (render_states ส่วน PDF/PNG/จำนวนหน้า) และ `compare_original.py` (ต้องใช้ PDF ของเรา) — ทำ template + data ครบ + parity IDENTICAL + HTML ต่อสถานะใน `out/` แล้ว · ต้องรันรอบเต็มบนเครื่องที่มี browser ก่อนส่ง UAT

## 2. Field map → data contract
| ช่องบนกระดาษ | key | source | format |
|---|---|---|---|
| โลโก้ | company.logo | Organization snapshot ตอนออกเลข | data URI |
| ชื่อเอกสาร "แบบฟอร์มประเมินความพึงพอใจของ<บริษัท>" | doc.title | "แบบฟอร์มประเมินความพึงพอใจของ" + Organization.legal_name (DEC-04/DEC-11) | text |
| 1. ชื่อห้าง/ร้านค้า: | store.name | ผู้ใช้กรอก (เสนอ: เลือกจาก Customer master) | text |
| 2. ชื่อบริษัทคู่ค้า: | partner.company_name | Organization.legal_name (ค่าเดียวกับหัวเรื่อง · DEC-11) | text |
| 3. ประเภทธุรกิจ ☐×4 | business_type.{hypermarket,supermarket,wholesales,convenience}_box | ผู้ใช้เลือก 1 | "☑"/"☐" |
| 4. ระยะเวลาที่ทำธุรกิจ ☐×4 | relationship_years.{lt1,y1_3,y3_5,gt5}_box | ผู้ใช้เลือก 1 (DEC-12) | "☑"/"☐" |
| ตาราง 9 หัวข้อ · คะแนน (1-5) | rating.{quality,on_time_delivery,stock_replenishment,communication,trade_terms,marketing_support,after_sales,sales_professionalism,overall} | ผู้ใช้เลือก 1–5 (DEC-13) · ยังไม่ให้คะแนน = "" | "1"–"5" |
| ข้อเสนอแนะ (เส้นว่าง 2 บรรทัด) | suggestion | ผู้ใช้กรอก (ไม่บังคับ) | text · R8 กล่อง (ตัดบรรทัดเอง) |
| ผู้ประเมิน (ลงชื่อ) | sign_rows[].signs[] | ผู้ประเมิน 1 ช่อง (DEC-03 ไม่มีสายอนุมัติ) — วนจาก data ไม่ fix · ถ้าเปิด DOA ภายหลังเพิ่ม `doa_step:*` ใน print_config ได้โดยไม่แก้ template | "ส่งในระบบ วันที่ เวลา" |
| Doc.No. / Rev. | doc.form_code · doc.revision | print_config | FM-SAL-06 · Rev.00: 01/07/2569 |
| footer ระบบ | doc.no · doc.is_draft | ENG-DOC-NUM (ออกตอนบันทึกครั้งแรก DEC-09) | CSE-2569-0001 |

## 5. สถานะ (data ตัวอย่างสมมติ · parity IDENTICAL 5/5 · ไม่มี {{}} หลง · ไม่มี key ขาด)
draft (กรอกบางส่วน) · submitted (ครบทุกช่อง ใกล้ตัวอย่างลูกค้า) · alt-choices-low (ตัวเลือกอีกทาง + คะแนนต่ำ) · long-suggestion (ข้อเสนอแนะยาว → dense) · blank-print (แบบเปล่าทุก ☐)
- สถานะ "DOA 6 ขั้น" ของ form-replica §5 **ไม่เกี่ยว** — DEC-03 ไม่มีสายอนุมัติ (ช่องลงชื่อวนจาก sign_rows ยังรองรับ N ช่องถ้าเปิด DOA)
- จำนวนหน้า: [NO-BROWSER] ยังไม่ได้วัด — คาดว่า 1 หน้า (ต้นฉบับ 1 หน้า)

## 7. ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ `แบบประเมินความพึงพอใจลูกค้า.docx` → `orig/SAMPLE.pdf` (LibreOffice) · compare_original: [NO-BROWSER] ข้าม
- ตั้งใจต่าง: (1) ชื่อบริษัทหัวเรื่อง + ข้อ 2 ใช้ค่าเดียวจาก Organization (ต้นฉบับ "(มหาชน)" vs "จำกัด" ไม่ตรงกัน) (2) ข้อเสนอแนะเป็นกล่อง R8 แทนเส้น 2 บรรทัด (รองรับข้อความยาว) (3) ช่องผู้ประเมินเป็น B6 (ชื่อในวงเล็บ + วันที่ส่งในระบบ) (4) footer ระบบซ้าย · Doc.No./Rev. ขวา
- profile: form_fs 10.5pt · title 16pt · logo 14mm · row_gap 6px · para_gap 16px · grid_gap 8px
