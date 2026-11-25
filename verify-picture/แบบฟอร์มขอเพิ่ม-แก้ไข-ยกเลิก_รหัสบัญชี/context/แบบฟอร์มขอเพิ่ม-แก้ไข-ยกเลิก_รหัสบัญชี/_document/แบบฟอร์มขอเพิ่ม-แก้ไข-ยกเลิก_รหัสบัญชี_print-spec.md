# PRINT SPEC — แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี (ACR) · Replica FM-ACC-01
> โหมด Replica · template `form.tpl.html` (logic-less) · profile `profile.json` · print_config `print_config.json` · thai-doc-pdf-generator v2.2
> มติอ้างอิง: DECISIONS.lock DEC-04 · DEC-05 · DEC-06 · DEC-07 · DEC-12–14 (ทุกข้อ AI-DEFAULT รอลูกค้ายืนยัน)

## 1. สรุป
- A4 แนวตั้ง · Sarabun ฝังใน HTML · หมึกเดียว (#111111) · **1 หน้า** ทุกสถานะที่ทดสอบ
- ต้นฉบับ: `1. FM-ACC-01 แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี.docx` · Doc No. FM-ACC-01 · Rev.00 : 01/07/2569

## 2. Field map → data contract
| ช่องบนกระดาษ | key | source | format |
|---|---|---|---|
| โลโก้ | company.logo / company.name | Organization snapshot ตอนออกเลข | data URI |
| ชื่อเอกสาร | doc.title | คงที่ (FORM_SPEC.form.title) | text |
| เลขที่เอกสาร | doc.no | ENG-DOC-NUM (ACR) ออกตอนบันทึกครั้งแรก (DEC-10) | ACR-2569-0004 |
| วันที่ | req_date | doc.created_at | วัน เดือนเต็ม พ.ศ. |
| ☐ เพิ่ม / แก้ไข / ยกเลิกรหัสบัญชี | req_type.add_box / edit_box / cancel_box | request_type (add·edit·cancel) — เลือกได้ 1 (DEC-13) | ☑ / ☐ |
| ชื่อบัญชีที่ต้องการขอเพิ่ม (แถวซ้ำ) | add_lines[].account_name | ผู้ใช้กรอก · เติมแถวว่างจนครบ 4 (DEC-05) · ไม่ใช่ add = 4 แถวว่าง | text |
| วัตถุประสงค์ในการเพิ่ม | add.purpose | ผู้ใช้กรอก (เฉพาะ add) | text |
| รหัสบัญชี / แก้ไขเป็น / วัตถุประสงค์ในการแก้ไข | edit.account_code / edit.change_to / edit.purpose | ผู้ใช้กรอก (เฉพาะ edit) | text |
| รหัสบัญชี / ชื่อบัญชี / วัตถุประสงค์ในการยกเลิก | cancel.account_code / cancel.account_name / cancel.purpose | ผู้ใช้กรอก (เฉพาะ cancel) · ป้ายแก้คำผิดจาก "แก้ไข" (DEC-12) | text |
| สำหรับผู้อนุมัติ ☐ อนุมัติ ☐ ไม่อนุมัติ เหตุผล | approval.approve_box / reject_box / reject_reason | ผลรวมของ approval_chain (อนุมัติครบทุกขั้น = ☑ อนุมัติ · มีขั้นไม่อนุมัติ = ☑ ไม่อนุมัติ + เหตุผลของขั้นนั้น) | ☑/☐ · text |
| หมายเหตุ | — | ข้อความคงที่ตรงตัว | — |
| ช่องลงชื่อ (dynamic) | sign_rows[].signs[] | ผู้ขอ + 1 ช่องต่อขั้นใน approval_chain (จำนวนตาม DOA · ไม่ fix) · แถวละ ≤4 เฉลี่ยเท่ากัน · คำตัดสินตาม role (`decision_words.by_role`: role-line-manager = ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ) · `scripts/sign_rows.py` / `tplSignRows()` | "ส่ง/พิจารณาในระบบ วันที่ เวลา" |
| ผู้บันทึกเข้าระบบ … ( … ) / วันที่ … | recorder.status / recorder.name / recorder.date | การกด "บันทึกเข้าระบบแล้ว" ของ admin role ฝ่ายบัญชี หลังอนุมัติ (ไม่ใช่ขั้น DOA) | "บันทึกแล้ว" · ชื่อ · วันที่ |
| footer | doc.no · doc.is_draft · doc.form_code · doc.revision | ระบบ | — |

## 5. สถานะที่ render (parity IDENTICAL 6/6 · ทุกไฟล์ 1 หน้า)
draft (เพิ่ม 2 แถว · รอส่ง) · approved (เพิ่ม 3 แถว · 2 ขั้นอนุมัติ · บันทึกเข้าระบบแล้ว) · rejected (ยกเลิก · ขั้น 2 ไม่อนุมัติ + เหตุผล) · edit-pending (แก้ไข · ขั้น 1 ผ่าน ขั้น 2 รอ) · long-12rows (เพิ่ม 12 แถว · dense) · approved-doa6steps (DOA 6 ขั้น → 7 ช่อง 2 แถว 4+3)
- กรณีสุดขั้ว 12 แถว + DOA 6 ขั้น = 2 หน้า โดยบล็อกลงชื่อทั้งก้อนขึ้นหน้า 2 (`.signs-block` ไม่ตัดกลาง) ตาม form-replica §5 — ไม่อยู่ในชุดสถานะบังคับ (data เก็บที่ `.build/long-12rows-doa6steps.data.json`)
- render บน Chromium ใน container (เครื่องผู้ใช้ NO-BROWSER) แล้วคัดผลกลับ — ดู RUN_LOG

## 7. ต้นฉบับ + ความต่างที่ตั้งใจ
- compare_original region 0:0.72 = **0.132 WARN** (อธิบายได้ — ดูภาพ `compare/compare_side.png` แล้ว):
  1. ภาพต้นฉบับได้จาก LibreOffice บนเครื่องที่ไม่มีฟอนต์ไทย → ตัวอักษรเป็นกล่องและบรรทัดเลื่อน/ล้นเป็น 2 หน้า จึงเทียบตำแหน่งบรรทัดไม่ได้ (lines_original 6 vs ours 19)
  2. ตั้งใจต่าง: ช่องลงชื่อย้ายเป็นแถวล่างตาม DOA (DEC-07) · กรอบสี่เหลี่ยมรอบส่วนกรอก/ส่วนผู้อนุมัติไม่วาด (Replica เส้นประ R4) · ป้าย "วัตถุประสงค์ในการยกเลิก" (DEC-12) · บรรทัดต่อของวัตถุประสงค์รวมเป็นช่องเดียว (ข้อความยาวตัดบรรทัดในช่อง) · footer ระบบซ้าย
  3. ลำดับส่วน/ถ้อยคำตรงกระดาษทุกส่วน (หัว → ☐ 3 ตัวเลือก → เพิ่ม → แก้ไข → ยกเลิก → ผู้อนุมัติ → หมายเหตุ → ผู้บันทึกเข้าระบบ)
- profile: logo 14mm · row_gap 6px · para_gap 12px (dense 8px) · title_gap 10px

## 8. Data contract
ดู §A ท้ายไฟล์นี้ · กฎ: ทุกค่าที่แสดงเป็น string · ☑/☐ จาก backend · ไม่มีค่า = "" · ส่วนที่ไม่ได้เลือกประเภท = ว่างทั้งหมด

## 9. print_config
`print_config.json` (doc_type ACR · sign_boxes requester + `doa_step:*` · decision_words.by_role · post_approval_box recorder · sign_layout max 4/แถว)

## §A Data contract (รวมจาก แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี_data-contract.md)
| key | source entity.field | ตัวอย่าง (สมมติ) | หมายเหตุ |
|---|---|---|---|
| company.name / company.logo | Organization snapshot | บริษัท ตัวอย่าง จำกัด / data URI | snapshot ตอนออกเลข |
| doc.title | คงที่ | แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี | |
| doc.no | account_code_request.doc_no | ACR-2569-0004 | ENG-DOC-NUM |
| doc.is_draft | status = draft | true/false | ใช้เป็นเงื่อนไขเท่านั้น |
| doc.form_code / doc.revision | print_config | FM-ACC-01 / Rev.00 : 01/07/2569 | |
| req_date | account_code_request.req_date | 7 ตุลาคม 2569 | วันที่ไทยเต็ม |
| req_type.add_box / edit_box / cancel_box | account_code_request.request_type | ☑ / ☐ / ☐ | |
| add_lines[].account_name | account_code_request_line.account_name | รายได้ค่าบริการติดตั้ง | เติมแถวว่างครบ 4 |
| add.purpose | account_code_request.add_purpose | … | |
| edit.account_code / edit.change_to / edit.purpose | account_code_request.edit_* | 5210-01 / … / … | |
| cancel.account_code / cancel.account_name / cancel.purpose | account_code_request.cancel_* | 5390-09 / … / … | |
| approval.approve_box / reject_box / reject_reason | approval_chain (สรุปผล) | ☑ / ☐ / "" | |
| sign_rows[].signs[] {role,name,position,date,decision{approve_box,reject_box,approve_word,reject_word}} | approval_chain snapshot + requester | ดู *.data.json | sign_rows.py |
| recorder.status / name / date | account_code_request.recorded_by / recorded_at | บันทึกแล้ว / กานดา บัญชีงาม / 8 ต.ค. 2569 | ว่างจนกว่าจะบันทึก |
| layout.dense | rows > 4 หรือ ขั้น DOA > 4 | false | |
