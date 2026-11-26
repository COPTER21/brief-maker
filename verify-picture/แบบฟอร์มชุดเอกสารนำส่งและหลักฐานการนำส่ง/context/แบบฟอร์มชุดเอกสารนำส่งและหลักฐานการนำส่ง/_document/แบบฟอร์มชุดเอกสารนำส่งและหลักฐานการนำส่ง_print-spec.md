# PRINT SPEC — แบบฟอร์มชุดเอกสารนำส่งและหลักฐานการนำส่ง (IVMG)

> เอกสารประกอบสำหรับ Dev · โหมด **Replica** (แบบฟอร์มลูกค้า FM-IVM-07) · มติ AI-DEFAULT ทั้งหมดรอลูกค้ายืนยัน
> ไฟล์คู่: `แบบฟอร์มชุดเอกสารนำส่งและหลักฐานการนำส่ง_template.html` (master, fonts ฝัง) · `form.tpl.html` (logic-less) · `*.data.json` · `out/*.html` (HTML ทุกสถานะ — NO-BROWSER ยังไม่ได้ PDF)

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มชุดเอกสารนำส่งและหลักฐานการนำส่ง / Document Dispatch Package and Delivery Evidence Form
- **ขนาด:** A4 แนวตั้ง · **2 หน้า (R10)** — ต้นฉบับ xlsx 1 หน้า แต่มีข้อมูลการนำส่ง 7 แถว + ตารางรายการตรวจสอบ 10 แถว + ตารางหลักฐาน 10 คอลัมน์ 15 แถว + ตารางลงชื่อ + ประวัติการแก้ไข ที่ฟอนต์ ≥ 8pt และสถานะบังคับ DOA 6 ขั้น (7 แถวลงชื่อ) / รายการยาว 16 แถว เกิน 1 หน้า → ออกแบบ 2 หน้าทุกสถานะเท่ากัน
- **ฟอนต์:** Sarabun 8.5pt (profile · ไม่ต่ำกว่า 8pt) · หมึกเดียว · ตารางกรอบ R9 (10 คอลัมน์ตาม A–J)

## 2. Field Mapping
| ช่องในเอกสาร | key (data) | Source (entity.field) | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่ (footer + หัวหน้า 2) | doc.no | ENG-DOC-NUM (IVMG) ออกตอนบันทึกครั้งแรก | ✓ | DEC-11 |
| บริษัท … และบริษัทในเครือ | company.name_line | Organization snapshot | ✓ | |
| ชื่อโครงการ / ธุรกรรม | dispatch.project_name | ivmg.project_name | ✓ | ข้อความอิสระ (DEC-01) |
| วัตถุประสงค์การนำส่ง | dispatch.purpose | ivmg.purpose | ✓ | |
| นำส่งให้ | dispatch.recipient | ivmg.recipient | ✓ | |
| วันที่นำส่ง | dispatch.dispatch_date | ivmg.dispatch_date | ✓ | dd/mm/yyyy |
| ผู้จัดทำ | dispatch.preparer_name | User.full_name (ผู้สร้าง) | ✓ | ระบบใส่ |
| ผู้ตรวจทาน | dispatch.reviewer_name | approval_chain[ขั้นแรก].approved_by | — | ว่างจนขั้นแรกพิจารณา (DEC-14) |
| ผู้อนุมัติ | dispatch.approver_name | approval_chain[ขั้นสุดท้าย].approved_by | — | ว่างจนอนุมัติครบ |
| รายการตรวจสอบชุดเอกสาร (loop ≥ 10 แถว) | docs[].seq/doc_name/version/status/confidentiality/remark | ivmg_doc.* | ✓ ≥1 แถว | seq ระบบรัน · status/confidentiality = label (DEC-04/05) |
| หลักฐานการนำส่งเอกสาร (loop ≥ 15 แถว) | deliveries[].seq/sent_at/sender/receiver/receiver_org/channel/docs_sent/evidence/remark/receipt_status | ivmg_delivery.* | หลังอนุมัติ | บันทึกหลังอนุมัติ (DEC-20) · channel/receipt_status = label (DEC-06) |
| หมายเหตุการใช้งาน | — | ข้อความคงที่ | — | |
| การตรวจทาน / อนุมัติ (loop) | sign_rows[].signs[] | requester + approval_chain (sign_rows.py) | ✓ | 1 แถวตารางต่อช่อง · จำนวนตาม DOA |
| ประวัติการแก้ไข (loop) | form_revisions[] | DOCCFG revision ของ IVMG | — | ข้อมูลแบบฟอร์ม ไม่ใช่ข้อมูลใบ (DEC-21) |
| Doc. No. / Rev. | doc.form_code · doc.revision | print_config | ✓ | FM-IVM-07 · Rev.00 : 01/07/2569 |

## 3. กติกาตรวจ (อ้าง DECISIONS.lock)
- สถานะ ขาดเอกสาร / มีข้อจำกัด ต้องมีหมายเหตุ (บล็อกตอนส่ง) (DEC-15) · มีแถว ขาดเอกสาร = เตือน (DEC-16)
- สถานะการรับ รับแล้ว ต้องมีหลักฐาน / ลิงก์ หรือไฟล์แนบ (DEC-17) · ช่องทาง อื่น ๆ / ส่งไม่สำเร็จ / ยกเลิก ต้องมีหมายเหตุ (DEC-18)
- วันที่ / เวลาส่ง ในอนาคต บล็อก · ก่อนวันที่นำส่ง เตือน (DEC-19)

## 4. กติกาการพิมพ์
- หน้า 1 = หัว + ข้อมูลกระบวนการ + ข้อมูลการนำส่ง + รายการตรวจสอบชุดเอกสาร · ท้ายหน้า "มีต่อหน้าถัดไป" · footer "หน้า 1/2"
- หน้า 2 (`.page-break`) = หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่) + หลักฐานการนำส่งเอกสาร + หมายเหตุการใช้งาน + การตรวจทาน/อนุมัติ (`.signs-block` ไม่ตัดข้ามหน้า) + ประวัติการแก้ไข · footer "หน้า 2/2"
- ตารางทั้งสองมี `thead` → แถวเกินหน้า หัวตารางซ้ำ · แถวไม่ตัดกลาง

## 5. วิธี build ใหม่
```bash
TD_SCRIPTS=$TD/scripts python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มชุดเอกสารนำส่งและหลักฐานการนำส่ง" --max-pages 2   # ต้องมี browser
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o compare --region 0:0.72        # ต้องมี PDF
```

## 6. Checklist
- [x] parity IDENTICAL 5/5 · [x] ไม่มี {{}} หลง (render_doc --strict + build_html ทุกสถานะ) · [x] ฟอนต์ ≥ 8pt · [x] ลายเซ็นครบตามสาย DOA (3 / 7 แถว)
- [ ] ทุกสถานะ 2 หน้าเท่ากัน — **[NO-BROWSER] ยังไม่ได้ตรวจ** (render_states/render_pdf ข้าม) → รันรอบเต็มบนเครื่องที่มี browser · จุดเสี่ยง: หน้า 2 สถานะ long-16rows (หลักฐาน 16 แถว 10 คอลัมน์แคบ) + DOA 6 ขั้น

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `7. FM-IVM-07 แบบฟอร์มชุดเอกสารนำส่งและหลักฐานการนำส่ง.xlsx` (ชีต INV-FM-07) · Doc. No. FM-IVM-07 · Rev.00 : 01/07/2569
- Profile token ที่ต่าง: form_fs 8.5pt · form_title_fs 14pt · form_logo_h 11mm · form_title_gap 2px · form_grid_gap 4px
- ความต่างที่ตั้งใจ: แบ่ง 2 หน้า (R10) · ตารางรายการตรวจสอบ: เอกสาร ขยาย B–D · หมายเหตุ ขยาย H–J (ต้นฉบับใช้ A–F แล้ว G–J ว่าง) · ลำดับแถวระบบรัน (แถวว่างยังพิมพ์เลขต่อจนครบ 10 / 15 ตามกระดาษ) · dropdown แสดงเป็นข้อความ label · ตารางลงชื่อวนตาม DOA (ไม่ fix 3 แถว) · ช่องลายเซ็น = ☐/☑ คำตัดสินตาม role + "ส่งในระบบ / พิจารณาในระบบ วันที่ เวลา" (DEC-08) · footer เลขที่ + CUBE NATIVE · โลโก้จาก Organization · แถบหัวหมวดสีน้ำเงินเข้ม → หมึกเดียวตัวหนา · ตัดแถวเว้นว่างคั่นหมวด · มุมหัวฟอร์ม INV-FM-07 ไม่พิมพ์ (ใช้ FM-IVM-07 ที่ footer · DEC-13)
- compare_original: **[NO-BROWSER] ข้าม** (ต้องใช้ PDF สถานะ approved) — ต้องรันบนเครื่องที่มี browser แล้วบันทึกคะแนนที่นี่

## 8. (Replica) Data contract + สถานะ
- สถานะ: draft · approved (อนุมัติแล้ว + หลักฐาน 3 แถว รับแล้ว 2 / ส่งไม่สำเร็จ 1) · rejected (ส่งกลับที่ขั้นผู้ตรวจสอบ) · long-16rows (รายการ 16 + หลักฐาน 16) · approved-doa6steps (ข้อมูลสมมติทั้งหมด)
- parity JS ↔ Python: IDENTICAL 5/5
- print_config: `print/print_config.json` (IVMG · decision_words by_role: role-line-manager = ตรวจสอบแล้ว/ส่งกลับ · role-gm = อนุมัติ/ส่งกลับ)
