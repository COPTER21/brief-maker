# PRINT SPEC — แบบฟอร์มการบันทึกการยกระดับประเด็น (IVMI)

> เอกสารประกอบสำหรับ Dev · โหมด **Replica** (แบบฟอร์มลูกค้า FM-IVM-09) · มติ AI-DEFAULT ทั้งหมดรอลูกค้ายืนยัน
> ไฟล์คู่: `แบบฟอร์มการบันทึกการยกระดับประเด็น_template.html` (master, fonts ฝัง) · `form.tpl.html` (logic-less) · `*.data.json` · `out/*.html` (HTML ทุกสถานะ — NO-BROWSER ยังไม่ได้ PDF)

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มการบันทึกการยกระดับประเด็น / Issue Escalation Log
- **ขนาด:** A4 แนวตั้ง · **2 หน้า (R10)** — ตาราง 10 คอลัมน์ 20 แถวขั้นต่ำ (ข้อความยาวได้ทุกช่อง) + หัว 8 แถว + ตารางลงชื่อ + ประวัติการแก้ไข เกิน 1 หน้าที่ฟอนต์ ≥ 8pt เมื่อข้อความยาว/DOA หลายขั้น
- **ฟอนต์:** Sarabun 8pt (profile · ไม่ต่ำกว่า 8pt) · หมึกเดียว · ตารางกรอบ R9

## 2. Field Mapping
| ช่องในเอกสาร | key (data) | Source (entity.field) | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่ (footer + หัวหน้า 2) | doc.no | ENG-DOC-NUM (IVMI) ออกตอนบันทึกครั้งแรก | ✓ | DEC-10 |
| บริษัท … และบริษัทในเครือ | company.name_line | Organization snapshot | ✓ | |
| ชื่อโครงการ / ธุรกรรม | project.name | ivmi.project_name | ✓ | ช่องเพิ่ม (DEC-06/13 · AI-DEFAULT) วางในแถวว่างใต้ชื่อบริษัท |
| บันทึกการยกระดับประเด็น (loop ≥ 20 แถว) | escalations[].esc_no/esc_date/issue/impact/decision_needed/escalate_to/action_owner/due_date/status/remark | ivmi_escalation.* | ✓ ≥1 แถว | esc_no = ESC-001… ระบบรัน (DEC-14) |
| การตรวจทาน / อนุมัติ (loop) | sign_rows[].signs[] | requester + approval_chain (sign_rows.py) | ✓ | 1 แถวตารางต่อช่อง · จำนวนตาม DOA |
| ประวัติการแก้ไข (loop) | form_revisions[] | DOCCFG revision ของ IVMI | — | ข้อมูลแบบฟอร์ม ไม่ใช่ข้อมูลใบ |
| Doc. No. / Rev. | doc.form_code · doc.revision | print_config | ✓ | FM-IVM-09 · Rev.00 : 01/07/2569 |

## 3. กติกาตรวจ
- ผลการพิจารณา / สถานะ 5 ค่า: เสนอแล้ว / อยู่ระหว่างพิจารณา / มีข้อสั่งการแล้ว / ปิดประเด็น / ยกเลิก (data validation I13:I32)
- มีข้อสั่งการแล้ว / ยกเลิก → หมายเหตุบังคับ (ข้อสั่งการ/เหตุผล) (DEC-04/15)
- กำหนดส่ง ≥ วันที่ (บล็อก) · เลยกำหนดยังไม่ปิด/ยกเลิก → เตือน (DEC-17)

## 4. กติกาการพิมพ์
- หน้า 1 = หัว + ชื่อโครงการ + ข้อมูลกระบวนการ + บันทึกการยกระดับประเด็น · ท้ายหน้า "มีต่อหน้าถัดไป" · footer "หน้า 1/2"
- หน้า 2 (`.page-break`) = หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่ + ชื่อโครงการ) + หมายเหตุการใช้งาน + การตรวจทาน/อนุมัติ (`.signs-block` ไม่ตัดข้ามหน้า) + ประวัติการแก้ไข · footer "หน้า 2/2" — ตัดหน้าตั้งใจก่อนบล็อกลงชื่อ (R10)
- ตารางยกระดับมี `thead` → แถวเกินหน้า หัวตารางซ้ำ · แถวไม่ตัดกลาง

## 5. วิธี build ใหม่
```bash
TD_SCRIPTS=$TD/scripts python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มการบันทึกการยกระดับประเด็น" --max-pages 2   # ต้องมี browser
```

## 6. Checklist
- [x] parity IDENTICAL 5/5 · [x] ไม่มี {{}} หลง (render_doc --strict + build_html ทุกสถานะ) · [x] ฟอนต์ ≥ 8pt · [x] ลายเซ็นครบตามสาย DOA (3 / 7 ช่อง)
- [ ] ทุกสถานะ 2 หน้าเท่ากัน — **[NO-BROWSER] ยังไม่ได้ตรวจ** (render_states/render_pdf ข้าม) → รันรอบเต็มบนเครื่องที่มี browser

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `9. FM-IVM-09 แบบฟอร์มการบันทึกการยกระดับประเด็น.xlsx` · Doc. No. FM-IVM-09 · Rev.00 : 01/07/2569
- Profile token ที่ต่าง: form_fs 8pt · form_title_fs 14pt · form_logo_h 11mm · form_title_gap 2px · form_grid_gap 4px
- ความต่างที่ตั้งใจ: แบ่ง 2 หน้า (R10) · ช่องเพิ่ม ชื่อโครงการ / ธุรกรรม (แถว 4 ที่ว่างบนกระดาษ · DEC-06) · เลข ESC ระบบรัน (ไม่พิมพ์ล่วงหน้า) · แถวว่างไม่มีเลขท้ายตาราง (แถว 33) ไม่แสดง (DEC-14) · ตารางลงชื่อวนตาม DOA (ไม่ fix 3 แถว) · ช่องลายเซ็น = ☐/☑ คำตัดสิน + "พิจารณาในระบบ วันที่ เวลา" (DEC-07) · footer เลขที่ + CUBE NATIVE · โลโก้จาก Organization · แถบหัวหมวดสีน้ำเงินเข้ม → หมึกเดียวตัวหนา
- compare_original: **[NO-BROWSER] ข้าม** (ต้องใช้ PDF สถานะ approved) — ต้องรันบนเครื่องที่มี browser แล้วบันทึกคะแนนที่นี่

## 8. (Replica) Data contract + สถานะ
- สถานะ: draft · approved · rejected · long-24escalations · approved-doa6steps (ข้อมูลสมมติทั้งหมด)
- parity JS ↔ Python: IDENTICAL 5/5
