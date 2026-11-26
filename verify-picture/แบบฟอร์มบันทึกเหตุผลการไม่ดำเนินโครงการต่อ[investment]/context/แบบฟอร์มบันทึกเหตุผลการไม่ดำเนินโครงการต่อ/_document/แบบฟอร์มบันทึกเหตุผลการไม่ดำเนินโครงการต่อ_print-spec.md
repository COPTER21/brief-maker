# PRINT SPEC — แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ (IVMJ)

> เอกสารประกอบสำหรับ Dev · โหมด **Replica** (แบบฟอร์มลูกค้า FM-IVM-10) · มติ AI-DEFAULT ทั้งหมดรอลูกค้ายืนยัน
> ไฟล์คู่: `แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ_template.html` (master, fonts ฝัง) · `form.tpl.html` (logic-less) · `*.data.json` · `out/*.pdf`

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ / Project Discontinuation Record
- **ขนาด:** A4 แนวตั้ง · **2 หน้า (R10)** — ตารางเหตุผล 8 คอลัมน์ + ข้อสรุป 6 ช่อง + ตารางลงชื่อ + ประวัติการแก้ไข เกิน 1 หน้าที่ฟอนต์ ≥ 8pt
- **ฟอนต์:** Sarabun 8.5pt (profile) · หมึกเดียว · ตารางกรอบ R9

## 2. Field Mapping
| ช่องในเอกสาร | key (data) | Source (entity.field) | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่ (footer + หัวหน้า 2) | doc.no | ENG-DOC-NUM (IVMJ) ออกตอนบันทึกครั้งแรก | ✓ | DEC-10 |
| บริษัท … และบริษัทในเครือ | company.name_line | Organization snapshot | ✓ | |
| ชื่อโครงการ / ธุรกรรม | project.name | ivmj.project_name | ✓ | |
| ผู้รับผิดชอบ | project.owner | Employee.full_name (ivmj.owner_id) | ✓ | PDPA |
| วันที่เสนอไม่ดำเนินการต่อ | proposed_date | ivmj.proposed_date (วันที่ไทย พ.ศ.) | ✓ | |
| ขั้นตอนที่ยุติ | stopped_at_step | ivmj.stopped_at_step | ✓ | |
| ผู้มีอำนาจพิจารณา | authority_name | approval_chain[last].assignee → Employee.full_name | ✓ | DOA |
| ตารางเหตุผล (loop ≥ 8 แถว) | reasons[].reason/selected/detail/evidence_ref/impact/reconsider_condition/owner/remark | ivmj_reason.* | ✓ | selected = "ใช่"/"ไม่ใช่" |
| สรุปเหตุผล … ประเด็นที่ต้องติดตาม | summary.* | ivmj.summary_* | บางช่อง | result = 1 ใน 4 ค่า |
| การตรวจทาน / อนุมัติ (loop) | sign_rows[].signs[] | requester + approval_chain (sign_rows.py) | ✓ | 1 แถวตารางต่อช่อง · จำนวนตาม DOA |
| ประวัติการแก้ไข (loop) | form_revisions[] | DOCCFG revision ของ IVMJ | — | ข้อมูลแบบฟอร์ม ไม่ใช่ข้อมูลใบ |
| Doc. No. / Rev. | doc.form_code · doc.revision | print_config | ✓ | FM-IVM-10 · Rev.00 : 01/07/2569 |

## 3. กติกาคำนวณ / ตรวจ
- ไม่มีสูตรเงิน · กติกาตรวจ (DEC-04/13/14): ≥ 1 แถว "ใช่" + แถว "ใช่" ต้องมีรายละเอียดประกอบ · ผล "ดำเนินการต่อแบบมีเงื่อนไข" → ข้อสั่งการ/เงื่อนไข บังคับ

## 4. กติกาการพิมพ์
- หน้า 1 = หัว + ข้อมูลกระบวนการ + ข้อมูลโครงการ + ตารางเหตุผล · ท้ายหน้า "มีต่อหน้าถัดไป" · footer "หน้า 1/2"
- หน้า 2 (`.page-break`) = หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่) + ข้อสรุป + หมายเหตุการใช้งาน + การตรวจทาน/อนุมัติ (`.signs-block`) + ประวัติการแก้ไข · footer "หน้า 2/2"
- แถวเหตุผลเกินหน้า 1 → หัวตารางซ้ำ (thead) · แถวไม่ตัดกลาง

## 5. วิธี build ใหม่
```bash
TD_SCRIPTS=$TD/scripts python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ" --max-pages 2
```

## 6. Checklist
- [x] ทุกสถานะ 2 หน้าเท่ากัน (ตรวจด้วย Chromium นอกเครื่องผู้ใช้ — เครื่องผู้ใช้ NO-BROWSER) · [x] ไม่มี {{}} หลง · [x] ฟอนต์ ≥ 8pt · [x] ลายเซ็นครบตามสาย DOA (3 / 7 ช่อง)

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `10. FM-IVM-10แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ.xlsx` · Doc. No. FM-IVM-10 · Rev.00 : 01/07/2569
- Profile token ที่ต่าง: form_fs 8.5pt · form_title_fs 14pt · form_logo_h 11mm · form_title_gap 2px · form_grid_gap 4px
- ความต่างที่ตั้งใจ: แบ่ง 2 หน้า (R10) · ตารางลงชื่อวนตาม DOA (ไม่ fix 3 แถว) · ช่องลายเซ็น = ☐/☑ คำตัดสิน + "พิจารณาในระบบ วันที่ เวลา" (DEC-07) · footer เลขที่ + CUBE NATIVE · โลโก้จาก Organization · คอลัมน์ I–J ที่ไม่มีหัวไม่แสดง (DEC-15) · แถบหัวหมวดสีน้ำเงินเข้ม → หมึกเดียวตัวหนา
- compare_original (approved หน้า 1 vs ต้นฉบับ): **score 0.554 WARN** — เหตุผล: ต้นฉบับ 1 หน้าส่วนเราแบ่ง 2 หน้า (ส่วนข้อสรุป/ลงชื่อย้ายไปหน้า 2) และภาพต้นฉบับ render ฟอนต์ไทยเป็นกล่อง · โครงหัว/ข้อมูลโครงการ/ตารางเหตุผลตรงตำแหน่ง (ดู compare/compare_side.png)

## 8. (Replica) Data contract + สถานะ
- parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: draft · approved · rejected (ผู้ตรวจสอบส่งกลับ) · long-12rows-conditional (12 แถว + ดำเนินการต่อแบบมีเงื่อนไข) · approved-doa6steps (7 ช่องลงชื่อ) → ทุกสถานะ 2 หน้า

### Data contract
| key | source | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| company.name · company.name_line · company.logo | Organization snapshot | บริษัท ตัวอย่าง จำกัด (มหาชน) | logo = data URI |
| doc.no · doc.is_draft · doc.form_code · doc.revision | ENG-DOC-NUM · state · print_config | IVMJ-2569-0007 | is_draft ใช้เป็นเงื่อนไขเท่านั้น |
| project.name · project.owner | ivmj | โครงการลงทุนตัวอย่าง A | owner PDPA |
| proposed_date · stopped_at_step · authority_name | ivmj · approval_chain | 9 ตุลาคม 2569 | string จัดรูปแล้ว |
| reasons[] (8 key) | ivmj_reason | ใช่ / ไม่ใช่ | เติมแถวว่างจนครบ 8 |
| summary.* (6 key) | ivmj | อนุมัติไม่ดำเนินการต่อ | |
| sign_rows[].signs[] {role,name,position,date,decision} | sign_rows.py | ☑ ตรวจสอบแล้ว ☐ ส่งกลับ | คำตัดสินตาม role |
| form_revisions[] {rev,date,detail,prepared_by,approved_by} | DOCCFG | 00 · 01/07/2569 | |
| layout.dense | rows > 8 หรือขั้น > 4 | false | |

## 9. (Replica) print_config
```json
{
  "doc_type": "IVMJ",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-IVM-10",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages": 2,
  "min_rows": 8,
  "dense_when_rows_over": 8,
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    {
      "box": "requester",
      "label": "ผู้จัดทำ",
      "show_date": true
    },
    {
      "box": "doa_step:*",
      "label": "from_doa_step",
      "show_decision": true,
      "show_date": true
    }
  ],
  "decision_words": {
    "default": {
      "approve": "อนุมัติ",
      "reject": "ไม่อนุมัติ"
    },
    "by_role": {
      "role-line-manager": {
        "approve": "ตรวจสอบแล้ว",
        "reject": "ส่งกลับ"
      },
      "role-gm": {
        "approve": "อนุมัติ",
        "reject": "ไม่อนุมัติ"
      }
    }
  },
  "config_reads": {
    "company.name_line": "Organization.legal_name_line (snapshot ตอนออกเลข)",
    "form_revisions": "DOCCFG.revisions[] ของ IVMJ"
  },
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc. No. : {form_code} · {revision}",
  "sign_layout": {
    "source": "approval_chain snapshot (ผู้ขอ + จำนวนขั้นตามที่ตั้งใน DOA)",
    "max_per_row": 4,
    "split": "even",
    "dense_when_steps_over": 4,
    "keep_together": true,
    "render": "ตารางตามกระดาษ — 1 แถวตารางต่อช่องลงชื่อ (บทบาท | ชื่อ | ตำแหน่ง | ลายเซ็น | วันที่) วนจาก sign_rows[].signs[]"
  },
  "page_break": "ก่อนหมวด \"ข้อสรุป การอนุมัติ และการปิดโครงการ\" — หน้า 1 = หัว+ข้อมูลโครงการ+ตารางเหตุผล · หน้า 2 = ข้อสรุป+หมายเหตุ+การตรวจทาน/อนุมัติ+ประวัติการแก้ไข (R10)"
}```
