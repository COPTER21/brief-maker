# PRINT SPEC — แบบฟอร์มตารางติดตามงานและแผนฐาน (IVMB)

> เอกสารประกอบสำหรับ Dev · โหมด **Replica** (แบบฟอร์มลูกค้า FM-IVM-02) · มติ AI-DEFAULT ทั้งหมดรอลูกค้ายืนยัน
> ไฟล์คู่: `แบบฟอร์มตารางติดตามงานและแผนฐาน_template.html` (master, fonts ฝัง) · `form.tpl.html` (logic-less) · `*.data.json` · `out/*.html` (HTML ทุกสถานะ — NO-BROWSER ยังไม่ได้ PDF)

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มตารางติดตามงานและแผนฐาน / Deal Tracker and Baseline Plan
- **ขนาด:** A4 แนวตั้ง · **2 หน้า (R10)** — ตาราง 10 คอลัมน์ 2 ชุด (หมุดหมาย 8 แถว + รายการติดตามงาน 18 แถว = 26 แถว > ~20) + ตารางลงชื่อ + ประวัติการแก้ไข เกิน 1 หน้าที่ฟอนต์ ≥ 8pt
- **ฟอนต์:** Sarabun 8pt (profile · ไม่ต่ำกว่า 8pt) · หมึกเดียว · ตารางกรอบ R9

## 2. Field Mapping
| ช่องในเอกสาร | key (data) | Source (entity.field) | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่ (footer + หัวหน้า 2) | doc.no | ENG-DOC-NUM (IVMB) ออกตอนบันทึกครั้งแรก | ✓ | DEC-11 |
| บริษัท … และบริษัทในเครือ | company.name_line | Organization snapshot | ✓ | |
| ชื่อโครงการ / ธุรกรรม | project.name | ivmb.project_name | ✓ | ช่องเพิ่ม (DEC-07/14 · AI-DEFAULT) วางในแถวว่างใต้ชื่อบริษัท |
| แผนฐานและหมุดหมายสำคัญ (loop ≥ 8 แถว) | milestones[].no/milestone/deliverable/owner/baseline_date/revised_date/predecessor/status/variance_days/remark | ivmb_milestone.* | ✓ ≥1 แถว | variance_days = revised − baseline (backend · string) |
| รายการติดตามงาน (loop ≥ 18 แถว) | tasks[].no/category/task/owner/due_date/predecessor/status/issue/last_updated/progress_pct | ivmb_task.* | ✓ ≥1 แถว | progress_pct = "40%" · last_updated = ระบบใส่ |
| การตรวจทาน / อนุมัติ (loop) | sign_rows[].signs[] | requester + approval_chain (sign_rows.py) | ✓ | 1 แถวตารางต่อช่อง · จำนวนตาม DOA |
| ประวัติการแก้ไข (loop) | form_revisions[] | DOCCFG revision ของ IVMB | — | ข้อมูลแบบฟอร์ม ไม่ใช่ข้อมูลใบ |
| Doc. No. / Rev. | doc.form_code · doc.revision | print_config | ✓ | FM-IVM-02 · Rev.00 : 01/07/2569 |

## 3. กติกาคำนวณ / ตรวจ
- ความคลาดเคลื่อน (วัน) = วันที่ปรับปรุง − วันที่ตามแผนฐาน · ว่างถ้าวันใดว่าง (ตรงสูตร Excel I13:I20) · บวก = ช้ากว่าแผน (เตือน)
- ร้อยละความคืบหน้า 0–100 (บล็อก) · แล้วเสร็จ แต่ < 100% → เตือน · สถานะ 5 ค่า: ยังไม่เริ่ม / กำลังดำเนินการ / รอตรวจทาน / แล้วเสร็จ / พักงาน (DEC-04/16/17/18)

## 4. กติกาการพิมพ์
- หน้า 1 = หัว + ชื่อโครงการ + ข้อมูลกระบวนการ + แผนฐานและหมุดหมายสำคัญ · ท้ายหน้า "มีต่อหน้าถัดไป" · footer "หน้า 1/2"
- หน้า 2 (`.page-break`) = หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่) + รายการติดตามงาน + หมายเหตุการใช้งาน + การตรวจทาน/อนุมัติ (`.signs-block` ไม่ตัดข้ามหน้า) + ประวัติการแก้ไข · footer "หน้า 2/2"
- ตารางหมุดหมาย/รายการงานมี `thead` → แถวเกินหน้า หัวตารางซ้ำ · แถวไม่ตัดกลาง

## 5. วิธี build ใหม่
```bash
TD_SCRIPTS=$TD/scripts python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มตารางติดตามงานและแผนฐาน" --max-pages 2   # ต้องมี browser
```

## 6. Checklist
- [x] parity IDENTICAL 5/5 · [x] ไม่มี {{}} หลง (render_doc --strict + build_html ทุกสถานะ) · [x] ฟอนต์ ≥ 8pt · [x] ลายเซ็นครบตามสาย DOA (3 / 7 ช่อง)
- [ ] ทุกสถานะ 2 หน้าเท่ากัน — **[NO-BROWSER] ยังไม่ได้ตรวจ** (render_states/render_pdf ข้าม) → รันรอบเต็มบนเครื่องที่มี browser

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `2. FM-IVM-02 แบบฟอร์มตารางติดตามงานและแผนฐาน.xlsx` · Doc. No. FM-IVM-02 · Rev.00 : 01/07/2569
- Profile token ที่ต่าง: form_fs 8pt · form_title_fs 14pt · form_logo_h 11mm · form_title_gap 2px · form_grid_gap 4px
- ความต่างที่ตั้งใจ: แบ่ง 2 หน้า (R10) · ช่องเพิ่ม ชื่อโครงการ / ธุรกรรม (แถว 4 ที่ว่างบนกระดาษ · DEC-07) · ตารางลงชื่อวนตาม DOA (ไม่ fix 3 แถว) · ช่องลายเซ็น = ☐/☑ คำตัดสิน + "พิจารณาในระบบ วันที่ เวลา" (DEC-08) · footer เลขที่ + CUBE NATIVE · โลโก้จาก Organization · แถวว่างไม่มีเลข 2 แถวท้ายรายการงานไม่แสดง (DEC-15) · แถบหัวหมวดสีน้ำเงินเข้ม → หมึกเดียวตัวหนา
- compare_original: **[NO-BROWSER] ข้าม** (ต้องใช้ PDF สถานะ approved) — ต้องรันบนเครื่องที่มี browser แล้วบันทึกคะแนนที่นี่

## 8. (Replica) Data contract + สถานะ
- parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: draft (2+2 แถว) · approved · rejected (ผู้ตรวจสอบส่งกลับ) · long-12milestones-18tasks (หมุดหมาย 12 + งาน 18 แถวเต็ม · dense) · approved-doa6steps (7 ช่องลงชื่อ)

### Data contract
| key | source | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| company.name · company.name_line · company.logo | Organization snapshot | บริษัท ตัวอย่าง จำกัด (มหาชน) | logo = data URI |
| doc.no · doc.is_draft · doc.form_code · doc.revision | ENG-DOC-NUM · state · print_config | IVMB-2569-0003 | is_draft ใช้เป็นเงื่อนไขเท่านั้น |
| project.name | ivmb | โครงการลงทุนตัวอย่าง A | |
| milestones[] (10 key) | ivmb_milestone | 01/10/2569 · แล้วเสร็จ · "2" | เติมแถวว่างจนครบ 8 (no ต่อเนื่อง) |
| tasks[] (10 key) | ivmb_task | กฎหมาย · "40%" | เติมแถวว่างจนครบ 18 |
| sign_rows[].signs[] {role,name,position,date,decision} | sign_rows.py | ☑ ตรวจสอบแล้ว ☐ ส่งกลับ | คำตัดสินตาม role |
| form_revisions[] {rev,date,detail,prepared_by,approved_by} | DOCCFG | 00 · 01/07/2569 | |
| layout.dense | หมุดหมาย > 8 หรืองาน > 18 หรือขั้น > 4 | false | |

## 9. (Replica) print_config
```json
{
  "doc_type": "IVMB",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-IVM-02",
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
    "form_revisions": "DOCCFG.revisions[] ของ IVMB",
    "status_labels": "ivmb.status_options (5 ค่า ตาม data validation ต้นฉบับ)"
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
  "page_break": "ก่อนหมวด \"รายการติดตามงาน\" — หน้า 1 = หัว+ข้อมูลกระบวนการ+แผนฐานและหมุดหมายสำคัญ · หน้า 2 = หัวย่อ+รายการติดตามงาน+หมายเหตุการใช้งาน+การตรวจทาน/อนุมัติ+ประวัติการแก้ไข (R10)",
  "min_rows_by_group": {
    "milestones": 8,
    "tasks": 18
  }
}
```
