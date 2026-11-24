# PRINT SPEC — แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ (PCL)

> เอกสารประกอบสำหรับ Dev — แนบคู่ FRD/Brief ของ F-TMP-004 · โหมด **Replica** (แบบฟอร์มลูกค้า FM-BDM-04)
> ไฟล์คู่: `form.tpl.html` (logic-less · แหล่งเดียวทั้ง prototype และ server) · `FM-BDM-04_template.html` (build แล้ว ฝังฟอนต์) · `profile.json` · `*.data.json` · `print_config.json` · `make_data.py`
> **[NO-BROWSER]** เครื่องที่ทำงานไม่มี browser → ไม่มี PDF ในชุดนี้ · แบบพิมพ์ทุกสถานะอยู่เป็น HTML (`out/*.html`) · ตรวจจำนวนหน้าด้วย Chromium บน cloud container (verify-only): ทุกสถานะ = 2 หน้า · ภาพ `out/_states_sheet.png` (หน้า 1) + `out/_states_sheet_p2.png` (หน้า 2) — ต้องรัน `render_states.py --max-pages 2` บนเครื่องที่มี browser ก่อน UAT

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ / Project Closure (No-Go) Record · doc_type `PCL` · Doc. No. FM-BDM-04 · Rev.00 : 01/07/2569
- **ขนาด:** A4 แนวตั้ง · **2 หน้า (R10)** — ตารางเหตุผล 8 แถว × 6 คอลัมน์ข้อความ + สรุปและปิดโครงการ 6 ช่องข้อความ + ลงชื่อ (สูงสุด 7 แถวเมื่อ DOA 6 ขั้น) + ประวัติ ใส่ 1 หน้าไม่ได้ที่ฟอนต์ ≥ 8pt เมื่อข้อความยาว
- **ฟอนต์:** Sarabun 8.5pt (form_fs) · หมึกเดียว (Replica)
- **โครง 2 หน้า:** หน้า 1 = หัวกระดาษ + ข้อมูลแบบฟอร์ม + ข้อมูลโครงการ + เหตุผลการไม่ดำเนินโครงการต่อ (8 แถวครบ) + "มีต่อหน้าถัดไป" · หน้า 2 = หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่) + สรุปและปิดโครงการ + บล็อกลงชื่อทั้งก้อน + ประวัติการแก้ไข · footer ทุกหน้า "หน้า N/2" + เลขที่ · ตัดหน้าตั้งใจก่อนบล็อกลงชื่อ (ตารางเหตุผลไม่ข้ามหน้า จึงไม่ต้องหัวตารางซ้ำ — thead ใส่ไว้ทุกตาราง)

## 2. Field Mapping / Data contract
| key ใน data | ช่องบนกระดาษ | Source (entity.field) | Format | หมายเหตุ |
|---|---|---|---|---|
| `company.logo` · `company.name` · `company.group_line` | โลโก้ · บรรทัด "บริษัท … และบริษัทในเครือ" | Organization snapshot ตอนออกเลข | data URI / text | ไม่เก็บใน template |
| `doc.title` | แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ | DocCfg.name | text | |
| `doc.no` · `doc.is_draft` | footer เลขที่ | ENG-DOC-NUM (PCL) | `PCL-พ.ศ.-running` | ออกตอนบันทึกครั้งแรก (DEC-10) |
| `doc.form_code` · `doc.revision` | Doc. No. / Rev. | print_config | text | |
| `project.name` | ชื่อโครงการ | ProjectClosure.project_name | text | ผู้ใช้กรอก (DEC-01 · DEC-16) |
| `project.owner` | ผู้รับผิดชอบ | ProjectClosure.owner → Employee.display_name | text | |
| `project.decision_date` | วันที่มีมติไม่ดำเนินการต่อ | ProjectClosure.decision_date | วันที่ไทยเต็ม | |
| `project.stopped_stage` | ขั้นตอนที่ยุติ | ProjectClosure.stopped_stage | text | |
| `reasons[]` (8 แถวตายตัว) | เหตุผลการไม่ดำเนินโครงการต่อ | ProjectClosure.reasons[] | — | ลำดับตาม ProjectClosure.reason_types (DEC-04/05) |
| ├ `reason` | เหตุผลหลัก | reason_types[].name | text | config |
| ├ `selected` | เลือก | reasons[].selected | "ใช่" / "ไม่ใช่" / "" (ร่างที่ยังไม่ตอบ) | ≥1 แถว "ใช่" (DEC-12) |
| └ `detail` · `evidence` · `impact` · `revisit_condition` | รายละเอียดประกอบ · หลักฐานอ้างอิง · ผลกระทบ · เงื่อนไขที่จะพิจารณาใหม่ | reasons[] | text | แถว "ใช่" ต้องมี detail (DEC-13/14) · แถว "ไม่ใช่" = "" |
| `closure.summary` · `decision_documents` · `lessons_learned` · `archive_method` · `future_followup` | สรุปและปิดโครงการ 5 หัวข้อ | ProjectClosure.* | text | future_followup บังคับเมื่อสถานะ "ติดตามเงื่อนไขในอนาคต" (DEC-15) |
| `closure.status` | สถานะการปิดโครงการ | ProjectClosure.closure_status | ปิดโครงการแล้ว / รอจัดเก็บเอกสาร / ติดตามเงื่อนไขในอนาคต | config closure_statuses |
| `sign_rows[].signs[]` | การตรวจทาน / อนุมัติ (บทบาท ชื่อ ตำแหน่ง ลายเซ็น วันที่) | approval_chain snapshot + sign_rows.py | — | ผู้จัดทำ + 1 แถวต่อขั้น DOA (ไม่ fix) · คำตัดสินตาม role |
| `form_revisions[]` | ประวัติการแก้ไข | DocumentConfig.form_revisions (F003) | text | ประวัติฉบับของแบบฟอร์ม ไม่ใช่ช่องกรอกต่อใบ |
| `layout.dense` | — | ขั้น DOA > 4 | boolean | |

## 3. กติกาคำนวณ / ตรวจ
- ไม่มีสูตร · `selected` ส่งเป็นคำ (ไม่ใช่ boolean) · แถว "ไม่ใช่" ส่งช่องข้อความว่าง
- ต้องมี "ใช่" ≥ 1 แถว · "เหตุผลอื่น" = ใช่ ต้องมีรายละเอียดประกอบ · สถานะ "ติดตามเงื่อนไขในอนาคต" ต้องมีข้อเสนอให้ติดตามในอนาคต (ตรวจตอนส่ง — แบบพิมพ์แสดงตามข้อมูล)

## 4. กติกาการพิมพ์
- ห้ามตัดแถวกลาง · `.signs-block` ไม่ตัดข้ามหน้า · `.page-break` ก่อนหน้า 2 (ตั้งใจ) · ทุกสถานะ 2 หน้า

## 5. วิธี build ใหม่
```bash
python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ" --max-pages 2
```

## 6. Checklist
- [x] parity IDENTICAL 5/5 · [x] ไม่มี {{}} หลง · [x] ฟอนต์ 8.5pt (≥ 8pt) · [x] ทุกสถานะ 2 หน้า (verify Chromium container) · [ ] PDF จริงบนเครื่องที่มี browser

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `4. FM-BDM-04 แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ.xlsx` (1 ชีต A1:J46 · พิมพ์ย่อทั้งชีตลง 1 หน้า) · Doc No. FM-BDM-04 · Rev.00 : 01/07/2569
- Profile: form_fs 8.5pt · form_lh 1.35 · title 14pt · logo 11mm · grid row 6mm
- ความต่างที่ตั้งใจ: (1) 2 หน้าแทน 1 หน้า (R10 — ข้อความยาวในตารางเหตุผล/สรุป + ลงชื่อ DOA หลายขั้น) (2) ช่องลงชื่อเป็นแถวต่อขั้น DOA (ผู้จัดทำ + N ขั้น) ข้อความ "ส่งในระบบ/พิจารณาในระบบ" + คำตัดสินตาม role แทนลายมือ (3) แถบหัวหมวดสีเทาอ่อนแทนพื้นน้ำเงินเข้ม (หมึกเดียว) (4) footer เลขที่ + "หน้า N/2" (5) หัวย่อหน้า 2 "(ต่อ)" + เลขที่
- ผล compare_original (approved หน้า 1 vs ต้นฉบับ · เต็มหน้า): score 0.467 (**WARN**) · region 0:0.6 = 0.402 — อธิบายได้: ต้นฉบับเป็นภาพ Excel ย่อทั้งชีตลง 1 หน้า (ตัวอักษรเล็กมาก ส่วนล่างครึ่งหน้าว่าง) ส่วนแบบพิมพ์ระบบเป็น 2 หน้าที่ 8.5pt ตำแหน่งบรรทัดจึงไม่ตรง แต่ลำดับบล็อก/ถ้อยคำ/คอลัมน์ตรงกระดาษครบ (cols 0.78 · ดู `compare/compare_side.png`) · ภาพต้นฉบับ render บนเครื่องที่ไม่มีฟอนต์ไทย · AI ดูภาพวางคู่แล้ว (unattended — ให้คนยืนยันจาก _BATCH_REPORT)

## 8. (Replica) สถานะที่ทดสอบ
- parity JS ↔ Python: IDENTICAL 5/5
- draft (เลือก 2 เหตุผล แถวอื่นยังไม่ตอบ · รอพิจารณา) · approved (3 เหตุผล · ปิดโครงการแล้ว · 2 ขั้น) · rejected (ผู้ตรวจสอบไม่ผ่าน · ติดตามเงื่อนไขในอนาคต + เหตุผลอื่น) · long-8reasons (เลือกครบ 8 · ข้อความยาวทุกช่อง) · approved-doa6steps (DOA 6 ขั้น → 7 ช่อง · dense) → ทุกสถานะ 2 หน้า

## 9. (Replica) print_config
```json
{
  "doc_type": "PCL",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-BDM-04",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages": 2,
  "page_break": "ก่อนหน้า 2 = สรุปและปิดโครงการ + บล็อกลงชื่อ + ประวัติการแก้ไข (หน้า 1 = หัว + ข้อมูลโครงการ + ตารางเหตุผล 8 แถว)",
  "min_rows": 8,
  "rows_page1": 8,
  "rows_page2_max": 0,
  "dense_when_rows_over": 8,
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    { "box": "requester", "label": "ผู้จัดทำ", "show_date": true },
    { "box": "doa_step:*", "label": "from_doa_step", "show_decision": true, "show_date": true }
  ],
  "decision_words": {
    "default": { "approve": "อนุมัติ", "reject": "ไม่อนุมัติ" },
    "by_role": {
      "role-line-manager": { "approve": "ตรวจสอบแล้ว", "reject": "ไม่ผ่านการตรวจสอบ" },
      "role-gm": { "approve": "อนุมัติ / รับทราบ", "reject": "ไม่อนุมัติ" }
    }
  },
  "config_reads": {
    "reasons[].reason": "ProjectClosure.reason_types",
    "closure.status": "ProjectClosure.closure_statuses",
    "form_revisions": "DocumentConfig.form_revisions (F003)",
    "company.group_line": "Organization.legal_name_group_line"
  },
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc. No. : {form_code} · {revision} · หน้า N/2",
  "sign_layout": {
    "source": "approval_chain snapshot (ผู้จัดทำ + จำนวนขั้นตามที่ตั้งใน DOA)",
    "style": "table-rows (1 แถวต่อช่อง ตามตารางบนกระดาษ: บทบาท | ชื่อ | ตำแหน่ง | ลายเซ็น | วันที่)",
    "max_per_row": 4,
    "split": "even",
    "dense_when_steps_over": 4,
    "keep_together": true
  }
}
```
