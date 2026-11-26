# PRINT SPEC — แบบฟอร์มบันทึกการอนุมัตินำส่ง (IVMH)

> เอกสารประกอบสำหรับ Dev · โหมด **Replica** (แบบฟอร์มลูกค้า FM-IVM-08) · มติ AI-DEFAULT ทั้งหมดรอลูกค้ายืนยัน
> ไฟล์คู่: `แบบฟอร์มบันทึกการอนุมัตินำส่ง_template.html` (master, fonts ฝัง) · `form.tpl.html` (logic-less) · `*.data.json` · `out/*.html` (HTML ทุกสถานะ — NO-BROWSER ยังไม่ได้ PDF)

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มบันทึกการอนุมัตินำส่ง / Pre-submission Approval Record
- **ขนาด:** A4 แนวตั้ง · **2 หน้า (R10)** — ต้นฉบับ xlsx 1 หน้า แต่มีหัวข้อมูลกระบวนการ 5 แถว + รายละเอียดการขออนุมัติ 6 แถว (ข้อความยาวได้) + ตารางผลการพิจารณา 7 คอลัมน์ (1 แถวต่อขั้น DOA) + หมายเหตุการใช้งาน + ตารางลงชื่อ + ประวัติการแก้ไข ที่ฟอนต์ ≥ 8pt และสถานะบังคับ DOA 6 ขั้น (ผลการพิจารณา 6 แถว + ลงชื่อ 7 แถว) / ข้อความยาว เกิน 1 หน้า → ออกแบบ 2 หน้าทุกสถานะเท่ากัน · ตัดหน้าก่อนบล็อกลงชื่อ
- **ฟอนต์:** Sarabun 8.5pt (profile · ไม่ต่ำกว่า 8pt) · หมึกเดียว · ตารางกรอบ R9

## 2. Field Mapping
| ช่องในเอกสาร | key (data) | Source (entity.field) | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่ (footer + หัวหน้า 2) | doc.no | ENG-DOC-NUM (IVMH) ออกตอนบันทึกครั้งแรก | ✓ | DEC-10 |
| บริษัท … และบริษัทในเครือ | company.name_line | Organization snapshot | ✓ | |
| ชื่อโครงการ / ธุรกรรม | approval.project_name | ivmh.project_name | ✓ | ข้อความอิสระ (DEC-01) |
| เรื่องที่ขออนุมัติ | approval.subject | ivmh.subject | ✓ | |
| เอกสารประกอบ | approval.supporting_docs | ivmh.supporting_docs | ✓ | หลายบรรทัด → ต่อด้วย " · " ใน data · ไฟล์แนบแสดงในระบบ (DEC-11) |
| ระดับอำนาจอนุมัติ | approval.authority_level | ivmh.authority_level → label | ✓ | รองกรรมการผู้จัดการ / กรรมการผู้จัดการ / ผู้มีอำนาจ (DEC-04/14) |
| ข้อเสนอของฝ่ายบริหารการลงทุน | approval.ivm_proposal | ivmh.ivm_proposal | ✓ | |
| เงื่อนไขการอนุมัติ | approval.proposed_conditions | ivmh.proposed_conditions | — | เงื่อนไขที่ฝ่ายเสนอ |
| ผลการพิจารณา (loop ≥ 3 แถว) | reviews[].seq/reviewer_role/position/decision/instruction/date/evidence | approval_chain snapshot + ivmh_review.* | ✓ | 1 แถวต่อขั้น DOA (DEC-05/13) · ขั้นที่ไม่ต้องพิจารณาตามระดับ → "—" + "ไม่ต้องพิจารณาตามระดับอำนาจอนุมัติ" (DEC-14) · decision = label 5 ค่า |
| การตรวจทาน / อนุมัติ (loop) | sign_rows[].signs[] | requester + approval_chain (sign_rows.py) | ✓ | 1 แถวตารางต่อช่อง · จำนวนตาม DOA (DEC-07) |
| ประวัติการแก้ไข (loop) | form_revisions[] | DOCCFG revision ของ IVMH | — | ข้อมูลแบบฟอร์ม ไม่ใช่ข้อมูลใบ (DEC-18) |
| Doc. No. / Rev. | doc.form_code · doc.revision | print_config | ✓ | FM-IVM-08 · Rev.00 : 01/07/2569 (DEC-12) |

## 3. กติกาตรวจ (อ้าง DECISIONS.lock)
- ระดับอำนาจอนุมัติต้องเลือก · รองกรรมการผู้จัดการ = 2 ขั้น · กรรมการผู้จัดการ / ผู้มีอำนาจ = 3 ขั้น (resolve ที่ DOA กลาง) (DEC-03/04/14)
- อนุมัติแบบมีเงื่อนไข / ให้แก้ไข / ไม่อนุมัติ → ต้องมีเงื่อนไข / ข้อสั่งการ (DEC-15)
- รับทราบ เฉพาะขั้นกลาง (DEC-16) · พิจารณาเรียงขั้น (DEC-17) · ให้แก้ไข / ไม่อนุมัติ → กลับเป็นร่างเลขเดิม (DEC-08)

## 4. กติกาการพิมพ์
- หน้า 1 = หัว + ข้อมูลกระบวนการ + รายละเอียดการขออนุมัติ + ผลการพิจารณา · ท้ายหน้า "มีต่อหน้าถัดไป" · footer "หน้า 1/2"
- หน้า 2 (`.page-break`) = หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่) + หมายเหตุการใช้งาน + การตรวจทาน/อนุมัติ (`.signs-block` ไม่ตัดข้ามหน้า) + ประวัติการแก้ไข · footer "หน้า 2/2"
- ตารางผลการพิจารณามี `thead` → แถวเกินหน้า หัวตารางซ้ำ · แถวไม่ตัดกลาง

## 5. วิธี build ใหม่
```bash
TD_SCRIPTS=$TD/scripts python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มบันทึกการอนุมัตินำส่ง" --max-pages 2   # ต้องมี browser
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o compare --region 0:0.72        # ต้องมี PDF
```

## 6. Checklist
- [x] parity IDENTICAL 5/5 · [x] ไม่มี {{}} หลง (render_doc --strict + build_html ทุกสถานะ) · [x] ฟอนต์ ≥ 8pt · [x] ลายเซ็นครบตามสาย DOA (3–4 / 7 แถว) · [x] ผลการพิจารณา ≥ 3 แถว (6 แถวใน DOA 6 ขั้น)
- [ ] ทุกสถานะ 2 หน้าเท่ากัน — **[NO-BROWSER] ยังไม่ได้ตรวจ** (render_states/render_pdf ข้าม) → รันรอบเต็มบนเครื่องที่มี browser

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `8. FM-IVM-08 แบบฟอร์มบันทึกการอนุมัตินำส่ง.xlsx` (ชีต INV-FM-08) · Doc. No. FM-IVM-08 · Rev.00 : 01/07/2569
- Profile token ที่ต่าง: form_fs 8.5pt · form_title_fs 14pt · form_logo_h 11mm · form_title_gap 2px · form_grid_gap 4px
- ความต่างที่ตั้งใจ: แบ่ง 2 หน้า (R10) · ตารางผลการพิจารณาวนตาม DOA (ไม่ fix 3 แถว · แถวป้ายขั้นตามกระดาษเมื่อยังไม่พิจารณา) · ระดับอำนาจอนุมัติแสดงเป็น label · ตารางลงชื่อวนตาม DOA · ช่องลายเซ็น = ☐/☑ คำตัดสินตาม role + "ส่งในระบบ / พิจารณาในระบบ วันที่ เวลา" (DEC-07) · คอลัมน์ว่าง H–J ของ xlsx ตัดออก (7 คอลัมน์) · footer เลขที่ + CUBE NATIVE · โลโก้จาก Organization · แถบหัวหมวดสีน้ำเงินเข้ม → หมึกเดียวตัวหนา · ตัดแถวเว้นว่างคั่นหมวด
- compare_original: **[NO-BROWSER] ข้าม** (ต้องใช้ PDF สถานะ approved) — ต้องรันบนเครื่องที่มี browser แล้วบันทึกคะแนนที่นี่

## 8. (Replica) Data contract + สถานะ
- สถานะ: draft (รอพิจารณา 3 ขั้น) · approved (อนุมัติ → รับทราบ → อนุมัติแบบมีเงื่อนไข) · rejected (ระดับรองกรรมการผู้จัดการ 2 ขั้น · ขั้น 2 ให้แก้ไข · แถว 3 "—") · long-text (ข้อความยาวทุกช่อง) · approved-doa6steps (ข้อมูลสมมติทั้งหมด)
- parity JS ↔ Python: IDENTICAL 5/5
- print_config: `print/print_config.json` (IVMH · decision_words by_role: role-line-manager = ตรวจสอบแล้ว/ส่งกลับ · role-gm = อนุมัติ / รับทราบ/ส่งกลับ)
