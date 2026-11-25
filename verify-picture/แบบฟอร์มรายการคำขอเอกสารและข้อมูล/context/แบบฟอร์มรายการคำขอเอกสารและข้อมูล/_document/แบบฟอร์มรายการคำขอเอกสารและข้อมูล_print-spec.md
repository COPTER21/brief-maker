# PRINT SPEC — แบบฟอร์มรายการคำขอเอกสารและข้อมูล (IVME)

> เอกสารประกอบสำหรับ Dev · โหมด **Replica** (แบบฟอร์มลูกค้า FM-IVM-05) · มติ AI-DEFAULT ทั้งหมดรอลูกค้ายืนยัน
> ไฟล์คู่: `แบบฟอร์มรายการคำขอเอกสารและข้อมูล_template.html` (master, fonts ฝัง) · `form.tpl.html` (logic-less) · `*.data.json` · `out/*.html` (HTML ทุกสถานะ — NO-BROWSER ยังไม่ได้ PDF)

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มรายการคำขอเอกสารและข้อมูล / Document & Information Request List
- **ขนาด:** A4 แนวตั้ง · **2 หน้า (R10)** — ตารางคำขอ 10 คอลัมน์ขั้นต่ำ 20 แถว (ไม่จำกัด · G4) + ตารางลงชื่อตาม DOA (3–7 แถว) + ประวัติการแก้ไข เกิน 1 หน้าเมื่อแถว > 20 หรือ DOA หลายขั้น ที่ฟอนต์ ≥ 8pt → ตัดหน้าตั้งใจก่อนบล็อกลงชื่อ ทุกสถานะ 2 หน้าเท่ากัน
- **ฟอนต์:** Sarabun 8pt (profile · ไม่ต่ำกว่า 8pt) · หมึกเดียว · ตารางกรอบ R9

## 2. Field Mapping
| ช่องในเอกสาร | key (data) | Source (entity.field) | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่ (footer + หัวหน้า 2) | doc.no | ENG-DOC-NUM (IVME) ออกตอนบันทึกครั้งแรก | ✓ | DEC-10 |
| บริษัท … และบริษัทในเครือ | company.name_line | Organization snapshot | ✓ | |
| ชื่อโครงการ / ธุรกรรม | project.name | ivme.project_name | ✓ | ช่องเพิ่ม (DEC-06/13 · AI-DEFAULT) วางในแถวว่างใต้ชื่อบริษัท · ซ้ำบนหัวหน้า 2 |
| รายการคำขอเอกสารและข้อมูล (loop ≥ 20 แถว) | requests[].request_code/item/requestee/owner/request_date/due_date/status/received_date/remark/doc_link | ivme_request.* | ✓ ≥1 แถว | request_code DR-nnn ระบบรัน · status = label ไทย 6 ค่า · วันที่ dd/mm/yyyy พ.ศ. |
| หมายเหตุการใช้งาน | usage_note | DocRequestPolicy.usage_note (snapshot) | ✓ | ค่าคงที่ (DEC-04) |
| สรุปรายการคำขอ (หน้า 2) | summary.total/received/partial/pending/closed | คำนวณจาก requests[].status ตอนพิมพ์ | — | ไม่เก็บ · ช่วยผู้ลงนามเห็นภาพรวม |
| การตรวจทาน / อนุมัติ (loop) | sign_rows[].signs[] | requester + approval_chain (sign_rows.py) | ✓ | 1 แถวตารางต่อช่อง · จำนวนตาม DOA |
| ประวัติการแก้ไข (loop) | form_revisions[] | DOCCFG revision ของ IVME | — | ข้อมูลแบบฟอร์ม ไม่ใช่ข้อมูลใบ (DEC-18) |
| Doc. No. / Rev. | doc.form_code · doc.revision | print_config | ✓ | FM-IVM-05 · Rev.00 : 01/07/2569 |

## 3. กติกาคำนวณ / ตรวจ
- ไม่มีสูตรคำนวณ · รหัส DR-nnn ระบบรันต่อใบ (prefix จาก config)
- ขอแล้ว/ได้รับบางส่วน/ได้รับครบ ต้องมีวันที่ขอ · ได้รับครบ ต้องมีวันที่ได้รับ · ยังไม่ขอ ห้ามมีวันที่ได้รับ · กำหนดส่ง/วันที่ได้รับ ≥ วันที่ขอ · ไม่เกี่ยวข้อง/ยกเลิก ต้องมีหมายเหตุ (บล็อก) · เกินกำหนดส่ง/ลิงก์มีคำว่ารหัสผ่าน → เตือน (DEC-04 · DEC-14..17)
- ตัวเลือก: สถานะ 6 ค่า (ยังไม่ขอ · ขอแล้ว · ได้รับบางส่วน · ได้รับครบ · ไม่เกี่ยวข้อง · ยกเลิก) ตาม data validation G13:G32 · พิมพ์เป็น label ไทย

## 4. กติกาการพิมพ์
- หน้า 1 = หัว + ชื่อโครงการ + ข้อมูลกระบวนการ + รายการคำขอ (thead ซ้ำเมื่อแถวล้นหน้า · แถวไม่ตัดกลาง) + หมายเหตุการใช้งาน · ท้ายหน้า "มีต่อหน้าถัดไป" · footer "หน้า 1/2"
- หน้า 2 (`.page-break`) = หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่) + ชื่อโครงการ + สรุปรายการคำขอ + การตรวจทาน/อนุมัติ (`.signs-block` ไม่ตัดข้ามหน้า) + ประวัติการแก้ไข · footer "หน้า 2/2"
- รองรับในหน้า 1 ได้ถึง ~30 แถวที่ 8pt (สถานะ long-28requests ใช้ dense)

## 5. วิธี build ใหม่
```bash
TD_SCRIPTS=$TD/scripts python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มรายการคำขอเอกสารและข้อมูล" --max-pages 2   # ต้องมี browser
```

## 6. Checklist
- [x] parity IDENTICAL 5/5 · [x] ไม่มี {{}} หลง (render_doc --strict + build_html ทุกสถานะ) · [x] ฟอนต์ ≥ 8pt · [x] ลายเซ็นครบตามสาย DOA (3 / 7 ช่อง)
- [ ] ทุกสถานะ 2 หน้าเท่ากัน — **[NO-BROWSER] ยังไม่ได้ตรวจ** (render_states/render_pdf ข้าม) → รันรอบเต็มบนเครื่องที่มี browser

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `5. FM-IVM-05 แบบฟอร์มรายการคำขอเอกสารและข้อมูล.xlsx` (ชีต INV-FM-05) · Doc. No. FM-IVM-05 · Rev.00 : 01/07/2569
- Profile token ที่ต่าง: form_fs 8pt · form_title_fs 14pt · form_logo_h 11mm · form_title_gap 2px · form_grid_gap 4px
- ความต่างที่ตั้งใจ: แบ่ง 2 หน้า (R10) ตัดก่อนบล็อกลงชื่อ · ช่องเพิ่ม ชื่อโครงการ / ธุรกรรม (แถว 4 ที่ว่างบนกระดาษ · DEC-13) · หน้า 2 มีสรุปรายการคำขอ (คำนวณ ไม่ใช่ช่องกรอก) · ตารางลงชื่อวนตาม DOA (ไม่ fix 3 แถว) · ช่องลายเซ็น = ☐/☑ คำตัดสิน + "พิจารณาในระบบ วันที่ เวลา" (DEC-07) · เส้นตารางว่างใต้ประวัติการแก้ไขบนกระดาษไม่พิมพ์ (DEC-18) · footer เลขที่ + CUBE NATIVE · โลโก้จาก Organization · แถบหัวหมวดสีน้ำเงินเข้ม → หมึกเดียวตัวหนา
- compare_original: **[NO-BROWSER] ข้าม** (ต้องใช้ PDF สถานะ approved) — ต้องรันบนเครื่องที่มี browser แล้วบันทึกคะแนนที่นี่

## 8. (Replica) Data contract + สถานะ
- parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: draft (คำขอ 3 แถว) · approved (6 แถว) · rejected (ผู้ตรวจสอบส่งกลับ) · long-28requests (dense) · approved-doa6steps (7 ช่องลงชื่อ)

### Data contract
| key | source | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| company.name · company.name_line · company.logo | Organization snapshot | บริษัท ตัวอย่าง จำกัด (มหาชน) | logo = data URI |
| doc.no · doc.is_draft · doc.form_code · doc.revision | ENG-DOC-NUM · state · print_config | IVME-2569-0003 | is_draft ใช้เป็นเงื่อนไขเท่านั้น |
| project.name | ivme | โครงการลงทุนตัวอย่าง A | |
| usage_note | DocRequestPolicy | ให้ผู้รับผิดชอบปรับปรุงข้อมูล… | snapshot ตอนออกเลข |
| requests[] (10 key) | ivme_request | DR-001 · ได้รับครบ | เติมแถวว่างจนครบ 20 (รหัสต่อเนื่อง) |
| summary.{total,received,partial,pending,closed} | คำนวณ | 6 · 2 · 1 · 2 · 1 | pending = ยังไม่ขอ + ขอแล้ว · closed = ไม่เกี่ยวข้อง + ยกเลิก |
| sign_rows[].signs[] {role,name,position,date,decision} | sign_rows.py | ☑ ตรวจสอบแล้ว ☐ ส่งกลับ | คำตัดสินตาม role |
| form_revisions[] {rev,date,detail,prepared_by,approved_by} | DOCCFG | 00 · 01/07/2569 | |
| layout.dense | แถว > 20 หรือขั้น > 4 | false | |

## 9. (Replica) print_config
```json
{
  "doc_type": "IVME",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-IVM-05",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages": 2,
  "min_rows": 20,
  "dense_when_rows_over": 20,
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
    "form_revisions": "DOCCFG.revisions[] ของ IVME",
    "usage_note": "DocRequestPolicy.usage_note (ข้อความหมายเหตุการใช้งาน · snapshot ตอนออกเลข · DEC-04)",
    "request_code": "DocRequestPolicy.code_prefix = DR- (รันต่อใบ DR-001 …)",
    "status_labels": "ivme.request_status (6) ตาม data validation ต้นฉบับ G13:G32",
    "summary": "คำนวณจาก requests[].status ตอนพิมพ์ (ไม่เก็บ)"
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
  "page_break": "ก่อนบล็อก 'การตรวจทาน / อนุมัติ' — หน้า 1 = หัว+ข้อมูลกระบวนการ+รายการคำขอ (ขั้นต่ำ 20 แถว · หัวตารางซ้ำเมื่อแถวล้น)+หมายเหตุการใช้งาน · หน้า 2 = หัวย่อ \"(ต่อ)\"+ชื่อโครงการ+สรุปรายการคำขอ+การตรวจทาน/อนุมัติ+ประวัติการแก้ไข (R10)",
  "min_rows_by_group": {
    "requests": 20
  }
}
```
