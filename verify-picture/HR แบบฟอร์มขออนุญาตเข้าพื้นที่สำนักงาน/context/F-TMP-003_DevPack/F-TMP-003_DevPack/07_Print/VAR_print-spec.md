# PRINT SPEC — แบบฟอร์มขออนุญาตเข้าพื้นที่สำนักงาน (VAR)

> โหมด **Replica** (thai-doc-pdf-generator v2.1) · ไฟล์คู่: `VAR_template.html` · `form.tpl.html` · `profile.json` · `*.data.json` · `print_config.json`
> [NO-BROWSER] รอบนี้ไม่มี PDF / `_states_sheet.png` / compare — ต้องรัน `render_states.py` + `compare_original.py` บนเครื่องที่มี browser

## 1. สรุป
- ประเภทเอกสาร: แบบฟอร์มขออนุญาตเข้าพื้นที่สำนักงาน / Office Visitor Access Request · A4 แนวตั้ง 1 หน้า · ฟอนต์ Sarabun (ฝังใน HTML)
- หมึกเดียวตาม profile ลูกค้า (ไม่ใช้สี CI CUBE ในเนื้อฟอร์ม)

## 2. Field Mapping
ดู `VAR_data-contract.md` (key ↔ entity.field) · ช่องทั้งหมดตาม FORM_SPEC 14 ช่อง 1:1 (DEC-06)

## 3. กติกาคำนวณ
- ไม่มีสูตรตัวเลข · `host.*` ดึงจากพนักงานที่เลือก (DEC-12) · `company.name` ค่าเดียวจาก Organization (DEC-13)
- ☐ อนุมัติ / ☐ ไม่อนุมัติ ในกรอบเจ้าหน้าที่ = ผลพิจารณาสุดท้ายของสาย DOA

## 4. กติกาการพิมพ์
- บล็อกลงชื่อ `.signs-block` ไม่ตัดข้ามหน้า · DOA > 4 ขั้น → `layout.dense` · ข้อความ "ส่งในระบบ / พิจารณาในระบบ วันที่ เวลา" แทนลายมือ (DEC-07)

## 5. วิธี build ใหม่
```bash
python3 make_print.py                                   # template + data ทุกสถานะ
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มขออนุญาตเข้าพื้นที่สำนักงาน"
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare --region 0:0.72
```

## 6. Checklist
- [x] parity IDENTICAL 5/5 · ไม่มี {{}} หลง · missing keys 0
- [ ] จำนวนหน้า 1 ทุกสถานะ — รอรันบนเครื่องที่มี browser
- [ ] compare_original ≥ 0.6 — รอรันบนเครื่องที่มี browser

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `แบบฟอร์มขออนุญาตเข้าพื้นที่สำนักงาน.docx` · Doc No. FM-HRM-05 · Rev. 00 : 01/07/2569
- Profile token ที่ต่างจาก default: form_fs 10pt · form_logo_h 14mm · form_row_gap 10px · form_para_gap 18px · form_date_w 60mm
- ความต่างจากกระดาษ (ตั้งใจ):
  1. ช่องลงชื่อพนักงานผู้รับการติดต่อ + ผู้บังคับบัญชาต้นสังกัด ย้ายเป็นแถวล่าง (B6 sign_rows · จำนวนช่องตาม DOA) — บนกระดาษอยู่ในกรอบเจ้าหน้าที่
  2. ช่องลงนามผู้มาติดต่อคงไว้ในเนื้อฟอร์ม (บุคคลภายนอกเซ็นมือ) · ชื่อในวงเล็บเติมจากระบบ
  3. ชื่อบริษัท 2 จุดใช้ค่าเดียวจาก Organization (กระดาษเขียน "(มหาชน)" ไม่ตรงกัน) — DEC-13
  4. หัวข้อส่วนบนกระดาษขีดเส้นใต้ → แสดงตัวหนา (class form-section · ไม่มี token ขีดเส้นใต้ · ห้ามเขียน style ใน body)
  5. footer ซ้าย "เลขที่ … · ร่าง · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE"
- compare_original: [NO-BROWSER] ยังไม่ได้รัน

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: draft (ร่าง · ☐ ทั้งหมด) · approved (☑ อนุมัติ) · rejected (☑ ไม่อนุมัติ + ความเห็น) · long-3steps (วัตถุประสงค์ 2 บรรทัด + DOA 3 ขั้น = 4 ช่อง) · approved-doa6steps (7 ช่อง 2 แถว 4+3 · dense) → HTML ต่อสถานะใน `out/` (ไม่มี PDF)
- ไม่มีรายการซ้ำบนกระดาษ (สถานะ "ยาว ≥12 แถว" ไม่ใช้ — ทดสอบความยาวด้วยวัตถุประสงค์ 2 บรรทัดแทน)

## 9. (Replica) print_config
```json
{
  "doc_type": "VAR",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-HRM-05",
  "revision": "Rev. 00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages_on_paper": 1,
  "min_rows": 0,
  "dense_when_rows_over": 0,
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    { "box": "requester", "label": "พนักงานผู้รับการติดต่อ", "show_date": true },
    { "box": "doa_step:*", "label": "from_doa_role", "show_decision": true, "show_date": true }
  ],
  "decision_words": { "default": { "approve": "อนุมัติ", "reject": "ไม่อนุมัติ" }, "by_role": {} },
  "config_reads": { "company.name": "Organization.Company.name_th (snapshot ตอนออกเลข · DEC-04/DEC-13)" },
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc No. {form_code} · {revision}",
  "sign_layout": { "source": "approval_chain snapshot (ผู้ขอ + จำนวนขั้นตามที่ตั้งใน DOA)", "max_per_row": 4, "split": "even", "dense_when_steps_over": 4, "keep_together": true },
  "note": "ช่อง 'ลงนามผู้มาติดต่อ' (บุคคลภายนอก) คงไว้ในเนื้อฟอร์มให้ลงนามด้วยมือ — ไม่ใช่ขั้น DOA · ☐ อนุมัติ/ไม่อนุมัติ ในกรอบเจ้าหน้าที่ = ผลพิจารณาสุดท้ายของสาย"
}

```
