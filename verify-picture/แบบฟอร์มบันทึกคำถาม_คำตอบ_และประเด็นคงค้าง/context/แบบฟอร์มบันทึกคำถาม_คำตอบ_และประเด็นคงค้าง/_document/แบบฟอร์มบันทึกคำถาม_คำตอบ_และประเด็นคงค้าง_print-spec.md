# PRINT SPEC — แบบฟอร์มบันทึกคำถาม คำตอบ และประเด็นคงค้าง (IVMC)

> เอกสารประกอบสำหรับ Dev · โหมด **Replica** (แบบฟอร์มลูกค้า FM-IVM-03) · มติ AI-DEFAULT ทั้งหมดรอลูกค้ายืนยัน
> ไฟล์คู่: `แบบฟอร์มบันทึกคำถาม คำตอบ และประเด็นคงค้าง_template.html` (master, fonts ฝัง) · `form.tpl.html` (logic-less) · `*.data.json` · `out/*.html` (HTML ทุกสถานะ — NO-BROWSER ยังไม่ได้ PDF)

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มบันทึกคำถาม คำตอบ และประเด็นคงค้าง / Q&A and Open Issues Log
- **ขนาด:** A4 แนวตั้ง · **2 หน้า (R10)** — ตาราง 10 คอลัมน์ 2 ชุด (คำถาม 14 แถว + ประเด็นคงค้าง 14 แถว = 28 แถว > ~20) + ตารางลงชื่อ + ประวัติการแก้ไข เกิน 1 หน้าที่ฟอนต์ ≥ 8pt
- **ฟอนต์:** Sarabun 8pt (profile · ไม่ต่ำกว่า 8pt) · หมึกเดียว · ตารางกรอบ R9

## 2. Field Mapping
| ช่องในเอกสาร | key (data) | Source (entity.field) | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่ (footer + หัวหน้า 2) | doc.no | ENG-DOC-NUM (IVMC) ออกตอนบันทึกครั้งแรก | ✓ | DEC-11 |
| บริษัท … และบริษัทในเครือ | company.name_line | Organization snapshot | ✓ | |
| ชื่อโครงการ / ธุรกรรม | project.name | ivmc.project_name | ✓ | ช่องเพิ่ม (DEC-07/14 · AI-DEFAULT) วางในแถวว่างใต้ชื่อบริษัท |
| บันทึกคำถามและคำตอบ (loop ≥ 14 แถว) | questions[].q_no/asked_date/question/asker/responder/answer/evidence/status/due_date/remark | ivmc_question.* | ✓ ≥1 แถว (รวมกับประเด็น) | q_no = Q-001… ระบบรัน (DEC-15) |
| รายการประเด็นคงค้าง (loop ≥ 14 แถว) | issues[].oi_no/opened_date/issue/category/owner/priority/due_date/status/escalate/remark | ivmc_issue.* | — | oi_no = OI-001… ระบบรัน · escalate = ใช่/ไม่ใช่ |
| การตรวจทาน / อนุมัติ (loop) | sign_rows[].signs[] | requester + approval_chain (sign_rows.py) | ✓ | 1 แถวตารางต่อช่อง · จำนวนตาม DOA |
| ประวัติการแก้ไข (loop) | form_revisions[] | DOCCFG revision ของ IVMC | — | ข้อมูลแบบฟอร์ม ไม่ใช่ข้อมูลใบ |
| Doc. No. / Rev. | doc.form_code · doc.revision | print_config | ✓ | FM-IVM-03 · Rev.00 : 01/07/2569 |

## 3. กติกาตรวจ
- สถานะคำถาม 5 ค่า: เปิด / อยู่ระหว่างจัดทำคำตอบ / รอตรวจทาน / ตอบแล้ว / ปิด · ตอบแล้ว/ปิด ต้องมีคำตอบ (DEC-04/16)
- ระดับความสำคัญ สูง/กลาง/ต่ำ · สถานะประเด็น เปิด / กำลังดำเนินการ / รอข้อมูล / ปิดแล้ว · ต้องยกระดับ ใช่ → หมายเหตุบังคับ (DEC-17)
- กำหนดตอบ ≥ วันที่ · กำหนดเสร็จ ≥ วันที่เปิด (บล็อก) · เลยกำหนดยังไม่ปิด → เตือน (DEC-18)

## 4. กติกาการพิมพ์
- หน้า 1 = หัว + ชื่อโครงการ + ข้อมูลกระบวนการ + บันทึกคำถามและคำตอบ · ท้ายหน้า "มีต่อหน้าถัดไป" · footer "หน้า 1/2"
- หน้า 2 (`.page-break`) = หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่) + รายการประเด็นคงค้าง + หมายเหตุการใช้งาน + การตรวจทาน/อนุมัติ (`.signs-block` ไม่ตัดข้ามหน้า) + ประวัติการแก้ไข · footer "หน้า 2/2"
- ตารางคำถาม/ประเด็นมี `thead` → แถวเกินหน้า หัวตารางซ้ำ · แถวไม่ตัดกลาง

## 5. วิธี build ใหม่
```bash
TD_SCRIPTS=$TD/scripts python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มบันทึกคำถาม คำตอบ และประเด็นคงค้าง" --max-pages 2   # ต้องมี browser
```

## 6. Checklist
- [x] parity IDENTICAL 5/5 · [x] ไม่มี {{}} หลง (render_doc --strict + build_html ทุกสถานะ) · [x] ฟอนต์ ≥ 8pt · [x] ลายเซ็นครบตามสาย DOA (3 / 7 ช่อง)
- [ ] ทุกสถานะ 2 หน้าเท่ากัน — **[NO-BROWSER] ยังไม่ได้ตรวจ** (render_states/render_pdf ข้าม) → รันรอบเต็มบนเครื่องที่มี browser

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `3. FM-IVM-03 แบบฟอร์มบันทึกคำถาม คำตอบ และประเด็นคงค้าง.xlsx` · Doc. No. FM-IVM-03 · Rev.00 : 01/07/2569
- Profile token ที่ต่าง: form_fs 8pt · form_title_fs 14pt · form_logo_h 11mm · form_title_gap 2px · form_grid_gap 4px
- ความต่างที่ตั้งใจ: แบ่ง 2 หน้า (R10) · ช่องเพิ่ม ชื่อโครงการ / ธุรกรรม (แถว 4 ที่ว่างบนกระดาษ · DEC-07) · เลข Q/OI ระบบรัน (ไม่พิมพ์ล่วงหน้า) · แถวว่างไม่มีเลขท้ายตาราง (แถว 27, 44–45) ไม่แสดง (DEC-15) · ตารางลงชื่อวนตาม DOA (ไม่ fix 3 แถว) · ช่องลายเซ็น = ☐/☑ คำตัดสิน + "พิจารณาในระบบ วันที่ เวลา" (DEC-08) · footer เลขที่ + CUBE NATIVE · โลโก้จาก Organization · แถบหัวหมวดสีน้ำเงินเข้ม → หมึกเดียวตัวหนา
- compare_original: **[NO-BROWSER] ข้าม** (ต้องใช้ PDF สถานะ approved) — ต้องรันบนเครื่องที่มี browser แล้วบันทึกคะแนนที่นี่

## 8. (Replica) Data contract + สถานะ
- สถานะ: draft · approved · rejected · long-18questions-16issues · approved-doa6steps (ข้อมูลสมมติทั้งหมด)
- parity JS ↔ Python: IDENTICAL 5/5
