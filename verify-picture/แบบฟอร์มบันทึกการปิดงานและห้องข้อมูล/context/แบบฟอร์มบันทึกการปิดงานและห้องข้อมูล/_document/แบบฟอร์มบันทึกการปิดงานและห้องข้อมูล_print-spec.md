# PRINT SPEC — แบบฟอร์มบันทึกการปิดงานและห้องข้อมูล (IVMK)

> เอกสารประกอบสำหรับ Dev · โหมด **Replica** (แบบฟอร์มลูกค้า FM-IVM-11) · มติ AI-DEFAULT ทั้งหมดรอลูกค้ายืนยัน
> ไฟล์คู่: `แบบฟอร์มบันทึกการปิดงานและห้องข้อมูล_template.html` (master, fonts ฝัง) · `form.tpl.html` (logic-less) · `*.data.json` · `out/*.html`

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มบันทึกการปิดงานและห้องข้อมูล / Transaction Closing & Data Room Record
- **ขนาด:** A4 แนวตั้ง · **2 หน้า (R10)** — สรุปการปิดงาน 5 ช่อง + รายการตรวจสอบ 8 แถว + บทเรียน 10 แถว + ตารางลงชื่อ + ประวัติการแก้ไข เกิน 1 หน้าที่ฟอนต์ ≥ 8pt
- **ฟอนต์:** Sarabun 8.5pt (profile) · หมึกเดียว · ตารางกรอบ R9

## 2. Field Mapping
| ช่องในเอกสาร | key (data) | Source (entity.field) | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่ (footer + หัวหน้า 2) | doc.no | ENG-DOC-NUM (IVMK) ออกตอนบันทึกครั้งแรก | ✓ | G9 |
| บริษัท … และบริษัทในเครือ | company.name_line | Organization snapshot | ✓ | |
| ชื่อโครงการ / ธุรกรรม | project.name | ivmk.project_name | ✓ | |
| วันที่ปิดงาน | closing.date | ivmk.closing_date (วันที่ไทย พ.ศ.) | ✓ | |
| ผลลัพธ์ของธุรกรรม | closing.outcome | ivmk.outcome | ✓ | |
| ผู้รับผิดชอบหลังปิดงาน | closing.post_owner | Employee.full_name (ivmk.post_owner_id) | ✓ | PDPA |
| สถานที่จัดเก็บเอกสารถาวร | closing.archive_location | ivmk.archive_location | ✓ | |
| ตารางรายการตรวจสอบ (8 แถวคงที่) | checklist[].item/status/owner/done_date/remark | ivmk_check.* · item จาก config ivmk.checklist_items | ✓ | status = 1 ใน 4 ค่า |
| ตารางบทเรียน (loop ≥ 10 แถว) | lessons[].topic/lesson/owner/due_date | ivmk_lesson.* | — | |
| การตรวจทาน / อนุมัติ (loop) | sign_rows[].signs[] | requester + approval_chain (sign_rows.py) | ✓ | 1 แถวตารางต่อช่อง · จำนวนตาม DOA |
| ประวัติการแก้ไข (loop) | form_revisions[] | DOCCFG revision ของ IVMK | — | ข้อมูลแบบฟอร์ม ไม่ใช่ข้อมูลใบ |
| Doc. No. / Rev. | doc.form_code · doc.revision | print_config | ✓ | FM-IVM-11 · Rev.00 : 01/07/2569 |

## 3. กติกาคำนวณ / ตรวจ
- ไม่มีสูตรเงิน · กติกาตรวจ (DECISIONS.lock G3): ส่งได้เมื่อทุกรายการ = แล้วเสร็จ/ไม่เกี่ยวข้อง · แล้วเสร็จ → ผู้รับผิดชอบ + วันที่ · ไม่เกี่ยวข้อง → หมายเหตุ · วันที่ดำเนินการ ≤ วันที่ปิดงาน · ข้อ 8 แล้วเสร็จ → บทเรียน ≥ 1 แถว

## 4. กติกาการพิมพ์
- หน้า 1 = หัว + ข้อมูลกระบวนการ + สรุปการปิดงาน + รายการตรวจสอบ 8 แถว · ท้ายหน้า "มีต่อหน้าถัดไป" · footer "หน้า 1/2"
- หน้า 2 (`.page-break`) = หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่) + บทเรียน + หมายเหตุการใช้งาน + การตรวจทาน/อนุมัติ (`.signs-block`) + ประวัติการแก้ไข · footer "หน้า 2/2"
- แถวบทเรียนเกิน → หัวตารางซ้ำ (thead) · แถวไม่ตัดกลาง · > 10 แถว = dense (ยัง ≥ 8pt)

## 5. วิธี build ใหม่
```bash
TD_SCRIPTS=$TD/scripts python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มบันทึกการปิดงานและห้องข้อมูล" --max-pages 2
```

## 6. Checklist
- [ ] ทุกสถานะ 2 หน้าเท่ากัน — **ยังไม่ได้ตรวจ** (เครื่องผู้ใช้ NO-BROWSER · ข้าม render_states.py/render_pdf.py) → รันรอบเต็มบนเครื่องที่มี browser
- [x] ไม่มี {{}} หลง (HTML ทุกสถานะจาก render_doc.py + build_html.py) · [x] ฟอนต์ ≥ 8pt (profile 8.5pt) · [x] ลายเซ็นครบตามสาย DOA (3 / 7 ช่อง) · [x] parity IDENTICAL 5/5

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `11. FM-IVM-11 แบบฟอร์มบันทึกการปิดงานและห้องข้อมูล.xlsx` · Doc. No. FM-IVM-11 · Rev.00 : 01/07/2569
- Profile token ที่ต่าง: form_fs 8.5pt · form_title_fs 14pt · form_logo_h 11mm · form_title_gap 2px · form_grid_gap 4px
- ความต่างที่ตั้งใจ: แบ่ง 2 หน้า (R10) · ตารางลงชื่อวนตาม DOA (ไม่ fix 3 แถว) · ช่องลายเซ็น = ☐/☑ คำตัดสิน + "พิจารณาในระบบ วันที่ เวลา" (G6) · footer เลขที่ + CUBE NATIVE · โลโก้จาก Organization · ตารางรายการตรวจสอบรวมคอลัมน์ที่ merge (A:C · E:F · G:H · I:J) เป็น 5 คอลัมน์ · ตารางบทเรียน 4 คอลัมน์ · แถบหัวหมวดสีน้ำเงินเข้ม → หมึกเดียวตัวหนา · แถวว่างท้ายประวัติการแก้ไขในต้นฉบับ (~20 แถว) ย่อเหลือ revision + 1 แถวว่าง
- compare_original: **ยังไม่ได้รัน** ([NO-BROWSER] ไม่มี PDF ของเรา) — ต้องรันบนเครื่องที่มี browser แล้วบันทึกคะแนนที่นี่ · คาดว่า WARN เพราะแบ่ง 2 หน้า

## 8. (Replica) Data contract + สถานะ
- parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: draft (รายการยังไม่ครบ) · approved · rejected (ผู้ตรวจสอบส่งกลับ) · long-14lessons (บทเรียน 14 แถว) · approved-doa6steps (7 ช่องลงชื่อ)

### Data contract
| key | source | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| company.name · company.name_line · company.logo | Organization snapshot | บริษัท ตัวอย่าง จำกัด (มหาชน) | logo = data URI |
| doc.no · doc.is_draft · doc.form_code · doc.revision | ENG-DOC-NUM · state · print_config | IVMK-2569-0007 | is_draft ใช้เป็นเงื่อนไขเท่านั้น |
| project.name | ivmk | โครงการลงทุนตัวอย่าง A | |
| closing.date · closing.outcome · closing.post_owner · closing.archive_location | ivmk | 9 ตุลาคม 2569 | post_owner PDPA |
| checklist[] {item,status,owner,done_date,remark} | ivmk_check + config | แล้วเสร็จ | 8 แถวคงที่ |
| lessons[] {topic,lesson,owner,due_date} | ivmk_lesson | — | เติมแถวว่างจนครบ 10 |
| sign_rows[].signs[] {role,name,position,date,decision} | sign_rows.py | ☑ ตรวจสอบแล้ว ☐ ส่งกลับ | คำตัดสินตาม role |
| form_revisions[] | DOCCFG | 00 · 01/07/2569 | |
| layout.dense | บทเรียน > 10 หรือขั้น > 4 | false | |

## 9. (Replica) print_config
```json
{
  "doc_type": "IVMK",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-IVM-11",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages": 2,
  "min_rows": 10,
  "dense_when_rows_over": 10,
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
    "form_revisions": "DOCCFG.revisions[] ของ IVMK",
    "checklist[].item": "config ivmk.checklist_items (8 รายการตั้งต้น)"
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
  "page_break": "ก่อนหมวด \"บทเรียนที่ได้รับและการติดตามผล\" — หน้า 1 = หัว+สรุปการปิดงาน+รายการตรวจสอบ 8 รายการ · หน้า 2 = บทเรียน+หมายเหตุ+การตรวจทาน/อนุมัติ+ประวัติการแก้ไข (R10)",
  "min_rows_by_group": {
    "checklist": 8,
    "lessons": 10
  }
}
```
