# PRINT SPEC — แบบสอบถามบุคลากรที่พ้นจากงาน (Exit Interview) (EXI)

> เอกสารประกอบสำหรับ Dev — แนบคู่ FRD ของ F-TMP-002 · ไฟล์คู่: `EXI_template.html` (master, fonts ฝัง) · `form.tpl.html` (logic-less) · `*.data.json`
> **โหมด:** Replica (แบบฟอร์มลูกค้า FM-HRM-06) · มติทั้งหมด AI-DEFAULT (DECISIONS.lock) รอลูกค้ายืนยัน
> **[NO-BROWSER]** รอบนี้เครื่องไม่มี browser → ยังไม่ได้ render PDF / _states_sheet.png / compare_original — ต้องรันรอบเต็มบนเครื่องที่มี browser

## 1. สรุป
- A4 แนวตั้ง · 3 หน้าตามกระดาษ (เนื้อหาไหลต่อหน้า — ตาราง 26 ข้อแบ่งข้ามหน้าได้ ห้ามตัดกลางแถว) · Sarabun ฝัง · หมึกเดียวตาม profile
- เอกสารลับ (DEC-17): ผู้บังคับบัญชาของผู้ให้ข้อมูลไม่เห็น/พิมพ์ไม่ได้ · HR (role-mgr-hr) + เจ้าของ

## 2. Field Mapping
| ช่องในเอกสาร | key | Source | ชนิด | บังคับ | หมายเหตุ |
|---|---|---|---|---|---|
| ชื่อ-นามสกุล | `employee.full_name` | Employee.full_name | text | ✓ | PDPA  |
| รหัสพนักงาน | `employee.code` | Employee.employee_code | text | ✓ |   |
| ตำแหน่ง | `employee.position` | Employee.position → Position.name | text | ✓ |   |
| สังกัดฝ่าย | `employee.division` | Employee.org_unit → OrgUnit.division_name | text | ✓ |   |
| สังกัดแผนก | `employee.department` | Employee.org_unit → OrgUnit.name | text | ✓ |   |
| อายุตัว ….ปี | `employee.age_years` | คำนวณ | number | ✓ | PDPA คำนวณจาก Employee.birth_date ณ วันที่พ้นจากงาน |
| อายุงาน ….. ปี | `service.years` | คำนวณ | number | ✓ |   |
| ….. เดือน | `service.months` | คำนวณ | number | ✓ |   |
| ระดับการศึกษา คุณวุฒิ | `employee.education_degree` | ผู้ใช้กรอก | text | ✓ |  ค่าเริ่มจาก Employee.education (ถ้ามีในระบบ) แก้ได้ |
| สาขา | `employee.education_major` | ผู้ใช้กรอก | text | ✓ |  ค่าเริ่มจาก Employee.education (ถ้ามีในระบบ) แก้ได้ |
| วันที่เริ่มปฏิบัติงาน | `employee.hire_date` | Employee.hire_date | date | ✓ |   |
| วันที่ลาออก | `separation.resign_date` | ผู้ใช้กรอก | date |  |  บังคับเมื่อเลือก "วันที่ลาออก" |
| อื่น ๆ | `separation.contract_end_other` | ผู้ใช้กรอก | text |  |   |
| ปัจจัย (กล่องที่ระบุหมายเลข) | `exit_reasons[].reason` | ผู้ใช้กรอก | select | ✓ |  ค่าจาก choice exit_reason_list |
| หมายเลข 1, 2, 3 เรียงตามลำดับความสำคัญ | `exit_reasons[].rank` | ผู้ใช้กรอก | number | ✓ |   |
| อื่นๆ โปรดระบุ | `exit_reasons_other_text` | ผู้ใช้กรอก | text |  |  บังคับเมื่อเลือก "อื่นๆ" |
| สิ่งที่ควรปรับปรุง | `improvements[].item` | ผู้ใช้กรอก | text |  |   |
| เหตุผล/แนวทางการปรับปรุง | `improvements[].reason` | ผู้ใช้กรอก | text |  |   |
| ความคิดเห็น/ข้อเสนอแนะอื่นๆ เพิ่มเติม | `other_comments` | ผู้ใช้กรอก | textarea |  |   |
| วันที่ | `signed_at` | ระบบใส่ | date | ✓ |  วันที่ส่งในระบบ |
| ☐ พ้น/ยังไม่พ้นทดลองงาน | `probation.*_box` | Employee.probation_status (ปรับได้) | glyph | ✓ | |
| ☐ ลูกจ้างประจำ/ชั่วคราว | `employment_type.*_box` | Employee.employment_type (ปรับได้) | glyph | ✓ | |
| ☐ วันที่ลาออก / ไม่จ้างต่อ | `separation.resign_box` · `contract_end_box` | ผู้ใช้เลือก 1 | glyph | ✓ | |
| ข้อ 5 ☐ ×3 | `contract_end_reason.*_box` | ผู้ใช้เลือก (เฉพาะ contract_end) | glyph | เงื่อนไข | |
| ส่วนที่ 2 ข้อ 1–26 × 5 ระดับ | `rate.qNN.c5..c1` | ratings.qNN (5..1) | "✓"/"" | ✓ ครบ 26 | |
| ส่วนที่ 3 ปัจจัย 21 กล่อง | `reason.r01..r20, reason.other` | exit_reasons[] {reason, rank} | "[n]" / "☐" | ≥1 | rank ไม่ซ้ำ 1..N |
| ผู้ให้ข้อมูล | `sign_rows[].signs[]` | ผู้ส่ง + เวลาส่ง | — | ✓ | ไม่มีขั้น DOA |

## 3. กติกาคำนวณ (DEC-04)
- อายุตัว = ปีเต็ม (ref_date − Employee.birth_date) · อายุงาน = ปี/เดือนเต็ม (ref_date − hire_date) · ref_date = วันที่ลาออก หรือวันสิ้นสุดสัญญา (Employee.contract_end_date) · ทุกค่าปรับได้
- ทุกค่าส่งเป็น string ที่จัดรูปแล้ว · วันที่ไทยเต็ม พ.ศ.

## 4. กติกาการพิมพ์
- `.form-grid tr` ห้ามตัดกลางแถว · `.signs-block` ไม่ตัดข้ามหน้า · footer เลขที่/ร่าง/Doc No.

## 5. วิธี build ใหม่
```bash
python3 make_print.py                                     # template + data จาก FORM_SPEC (ข้อมูลสมมติ)
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "…" --max-pages 3   # ต้องมี browser
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/submitted.pdf -o out/compare              # ต้องมี browser
```

## 6. Checklist
- [x] parity JS ↔ Python IDENTICAL 4/4 · ไม่มี {{}} หลง · missing keys 0
- [ ] PDF ≤ 3 หน้าทุกสถานะ — [NO-BROWSER] ยังไม่ได้ตรวจบนเครื่องนี้
- [ ] compare_original ≥ 0.6 — [NO-BROWSER] ยังไม่ได้รัน

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `แบบฟอร์ม Exit Interview.docx` → SAMPLE.pdf (LibreOffice) · Doc No. FM-HRM-06 · Rev. 00 : 01/07/2569
- Profile token ต่างจาก default: form_fs 9.2pt · form_title_fs 13pt · form_logo_h 14mm · form_row_gap 6px · form_para_gap 14px · form_grid_row_h 5.6mm
- ความต่าง (ตั้งใจ): "โปรดกรอบ" → "โปรดกรอก" (DEC-12) · "P" (Wingdings) → ✓ (DEC-13) · ลงชื่อผู้ให้ข้อมูลเป็นแถวล่าง B6 + "ส่งในระบบ วันที่ เวลา" (DEC-08) · footer เลขที่ · กล่องลำดับส่วนที่ 3 แสดง [n] / ☐ · หัวตารางส่วนที่ 2 ไม่พิมพ์ซ้ำแบบกระดาษ (-2-)
- compare_original: [NO-BROWSER] ยังไม่ได้รัน

## 8. (Replica) Data contract + สถานะ
- contract: ภาคผนวกท้ายไฟล์นี้ (EXI_data-contract.md) · parity IDENTICAL 4/4
- สถานะ: draft (ร่าง ตอบบางส่วน) · submitted (ลาออก ครบ) · contract-end (ไม่จ้างต่อ + อื่น ๆ) · long-12rows-allreasons (ข้อเสนอแนะ 12 แถว · เลือกครบ 21 ปัจจัย · ความเห็นยาว)
- สถานะ "DOA 6 ขั้น" ไม่ใช้ — ไม่มีสายอนุมัติ (DEC-03) จึงมีช่องลงชื่อเดียว (ผู้ให้ข้อมูล)

## 9. (Replica) print_config
```json
{
  "doc_type": "EXI",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-HRM-06",
  "revision": "Rev. 00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages_on_paper": 3,
  "min_rows": 5,
  "dense_when_rows_over": 5,
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    { "box": "requester", "label": "ผู้ให้ข้อมูล", "show_date": true }
  ],
  "decision_words": { "default": { "approve": "รับทราบ", "reject": "-" } },
  "config_reads": {},
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc No. {form_code} · {revision}",
  "sign_layout": { "source": "ผู้ให้ข้อมูลเท่านั้น (ไม่มีสายอนุมัติ — DEC-03)", "max_per_row": 4, "split": "even", "dense_when_steps_over": 4, "keep_together": true },
  "confidential": true,
  "note": "ไม่มีขั้น DOA (DEC-03) → ไม่มี doa_step:* · แบบพิมพ์ 3 หน้าตามกระดาษ"
}
```


## Appendix — Data contract (EXI_data-contract.md)

### DATA CONTRACT — EXI (FM-HRM-06)

| key | source | ตัวอย่าง (สมมติ) | หมายเหตุ |
|---|---|---|---|
| `company.name` | Organization snapshot | บริษัท ตัวอย่าง จำกัด |  |
| `company.logo` | Organization snapshot | data:image/… |  |
| `doc.title` | EXI record / Employee | แบบสอบถามบุคลากรที่พ้นจากงาน ( Exit Inte |  |
| `doc.no` | EXI record / Employee | EXI-2569-0003 |  |
| `doc.is_draft` | EXI record / Employee | False |  |
| `doc.form_code` | EXI record / Employee | FM-HRM-06 |  |
| `doc.revision` | EXI record / Employee | Rev. 00 : 01/07/2569 |  |
| `employee.full_name` | EXI record / Employee | สมชาย ทดสอบดี |  |
| `employee.code` | EXI record / Employee | EMP-00123 |  |
| `employee.position` | EXI record / Employee | เจ้าหน้าที่ขาย |  |
| `employee.division` | EXI record / Employee | ฝ่ายขายและการตลาด |  |
| `employee.department` | EXI record / Employee | แผนกขายในประเทศ |  |
| `employee.age_years` | EXI record / Employee | 29 |  |
| `employee.education_degree` | EXI record / Employee | ปริญญาตรี |  |
| `employee.education_major` | EXI record / Employee | บริหารธุรกิจ |  |
| `employee.hire_date` | EXI record / Employee | 1 มิถุนายน 2566 |  |
| `service.years` | EXI record / Employee | 3 |  |
| `service.months` | EXI record / Employee | 5 |  |
| `probation.passed_box` | EXI record / Employee | ☑ |  |
| `probation.not_passed_box` | EXI record / Employee | ☐ |  |
| `employment_type.permanent_box` | EXI record / Employee | ☑ |  |
| `employment_type.temporary_box` | EXI record / Employee | ☐ |  |
| `separation.resign_box` | EXI record / Employee | ☑ |  |
| `separation.contract_end_box` | EXI record / Employee | ☐ |  |
| `separation.resign_date` | EXI record / Employee | 31 ตุลาคม 2569 |  |
| `separation.contract_end_other` | EXI record / Employee |  |  |
| `contract_end_reason.employee_box` | EXI record / Employee | ☐ |  |
| `contract_end_reason.unit_box` | EXI record / Employee | ☐ |  |
| `contract_end_reason.other_box` | EXI record / Employee | ☐ |  |
| `rate.q01.c5` | EXI record / Employee |  | q01..q26 เหมือนกัน |
| `rate.q01.c4` | EXI record / Employee | ✓ | q01..q26 เหมือนกัน |
| `rate.q01.c3` | EXI record / Employee |  | q01..q26 เหมือนกัน |
| `rate.q01.c2` | EXI record / Employee |  | q01..q26 เหมือนกัน |
| `rate.q01.c1` | EXI record / Employee |  | q01..q26 เหมือนกัน |
| `reason.r01` | EXI record / Employee | ☐ |  |
| `reason.r02` | EXI record / Employee | ☐ |  |
| `reason.r03` | EXI record / Employee | [2] |  |
| `reason.r04` | EXI record / Employee | [1] |  |
| `reason.r05` | EXI record / Employee | ☐ |  |
| `reason.r06` | EXI record / Employee | ☐ |  |
| `reason.r07` | EXI record / Employee | ☐ |  |
| `reason.r08` | EXI record / Employee | ☐ |  |
| `reason.r09` | EXI record / Employee | ☐ |  |
| `reason.r10` | EXI record / Employee | ☐ |  |
| `reason.r11` | EXI record / Employee | ☐ |  |
| `reason.r12` | EXI record / Employee | ☐ |  |
| `reason.r13` | EXI record / Employee | ☐ |  |
| `reason.r14` | EXI record / Employee | [3] |  |
| `reason.r15` | EXI record / Employee | ☐ |  |
| `reason.r16` | EXI record / Employee | ☐ |  |
| `reason.r17` | EXI record / Employee | ☐ |  |
| `reason.r18` | EXI record / Employee | ☐ |  |
| `reason.r19` | EXI record / Employee | ☐ |  |
| `reason.r20` | EXI record / Employee | ☐ |  |
| `reason.other` | EXI record / Employee | ☐ |  |
| `reason.other_text` | EXI record / Employee |  |  |
| `improvements[].no` | EXI record / Employee | 1 |  |
| `improvements[].item` | EXI record / Employee | การวางแผนเส้นทางเยี่ยมลูกค้า |  |
| `improvements[].reason` | EXI record / Employee | ให้ระบบช่วยจัดเส้นทาง ลดเวลาเดินทาง |  |
| `other_comments` | EXI record / Employee | ขอบคุณสำหรับโอกาสในการทำงาน |  |
| `sign_rows[].signs[].role` | EXI record / Employee | ผู้ให้ข้อมูล |  |
| `sign_rows[].signs[].name` | EXI record / Employee | สมชาย ทดสอบดี |  |
| `sign_rows[].signs[].position` | EXI record / Employee | เจ้าหน้าที่ขาย |  |
| `sign_rows[].signs[].date` | EXI record / Employee | ส่งในระบบ 25 ต.ค. 2569 10:30 น. |  |
| `sign_rows[].signs[].decision` | EXI record / Employee | None |  |
| `layout.dense` | EXI record / Employee | False |  |
