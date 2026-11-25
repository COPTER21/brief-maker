# PRINT SPEC — แบบฟอร์มห้องข้อมูล มาตรฐานชื่อไฟล์ และทะเบียนควบคุมเอกสาร (IVMD)

> เอกสารประกอบสำหรับ Dev · โหมด **Replica** (แบบฟอร์มลูกค้า FM-IVM-04) · มติ AI-DEFAULT ทั้งหมดรอลูกค้ายืนยัน
> ไฟล์คู่: `แบบฟอร์มห้องข้อมูล มาตรฐานชื่อไฟล์ และทะเบียนควบคุมเอกสาร_template.html` (master, fonts ฝัง) · `form.tpl.html` (logic-less) · `*.data.json` · `out/*.html` (HTML ทุกสถานะ — NO-BROWSER ยังไม่ได้ PDF)

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มห้องข้อมูล มาตรฐานชื่อไฟล์ และทะเบียนควบคุมเอกสาร / Data Room Index, File Naming Standard and Document Control Register
- **ขนาด:** A4 แนวตั้ง · **2 หน้า (R10)** — ตารางแถวซ้ำ 4 ชุด (โฟลเดอร์ 8 + ทะเบียนเอกสาร 5 + การเปลี่ยนแปลง 5 + สิทธิ 5 = 23 แถว > ~20) + มาตรฐานชื่อไฟล์ + ตารางลงชื่อ + ประวัติการแก้ไข เกิน 1 หน้าที่ฟอนต์ ≥ 8pt
- **ฟอนต์:** Sarabun 8pt (profile · ไม่ต่ำกว่า 8pt) · หมึกเดียว · ตารางกรอบ R9

## 2. Field Mapping
| ช่องในเอกสาร | key (data) | Source (entity.field) | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่ (footer + หัวหน้า 2) | doc.no | ENG-DOC-NUM (IVMD) ออกตอนบันทึกครั้งแรก | ✓ | DEC-13 |
| บริษัท … และบริษัทในเครือ | company.name_line | Organization snapshot | ✓ | |
| ชื่อโครงการ / ธุรกรรม | project.name | ivmd.project_name | ✓ | ช่องเพิ่ม (DEC-09/16 · AI-DEFAULT) วางในแถวว่างใต้ชื่อบริษัท |
| โครงสร้างโฟลเดอร์ห้องข้อมูล (loop ≥ 8 แถว) | folders[].folder_no/folder_name/owner/access_level/required_docs/remark | ivmd_folder.* | ✓ ≥1 แถว | ใบใหม่ตั้งต้น 8 โฟลเดอร์จาก DataRoomPolicy.default_folders · access_level = label ไทย |
| มาตรฐานการตั้งชื่อไฟล์ (5 แถว) | naming.pattern/date_format/version_format/status_tokens/example | FileNamingPolicy (snapshot ตอนออกเลข) | ✓ | ค่าคงที่ (DEC-04) ไม่ใช่ช่องกรอก |
| ทะเบียนสถานะเอกสารและประวัติฉบับ (loop ≥ 5 แถว) | documents[].doc_code/doc_name/owner/version/version_date/doc_status/location/reviewer/approver/remark | ivmd_document.* | ✓ ≥1 แถว | doc_code D-nnn ระบบรัน · version Vnn/Final |
| การเปลี่ยนแปลงเอกสาร (loop ≥ 5 แถว) | changes[].change_code/change_date/doc_ref/detail/reason/impact/approver/effective_date/status/remark | ivmd_change.* | — | change_code CH-nnn ระบบรัน |
| บันทึกสิทธิการเข้าถึงข้อมูล (loop ≥ 5 แถว) | access[].seq/user_name/org_unit/role/access_level/scope/granted_date/revoked_date/approver/status | ivmd_access.* | — | seq ระบบรัน |
| การตรวจทาน / อนุมัติ (loop) | sign_rows[].signs[] | requester + approval_chain (sign_rows.py) | ✓ | 1 แถวตารางต่อช่อง · จำนวนตาม DOA |
| ประวัติการแก้ไข (loop) | form_revisions[] | DOCCFG revision ของ IVMD | — | ข้อมูลแบบฟอร์ม ไม่ใช่ข้อมูลใบ |
| Doc. No. / Rev. | doc.form_code · doc.revision | print_config | ✓ | FM-IVM-04 · Rev.00 : 01/07/2569 |

## 3. กติกาคำนวณ / ตรวจ
- ไม่มีสูตรคำนวณ · รหัส D-nnn / CH-nnn / ลำดับ / เลขที่โฟลเดอร์ 2 หลัก ระบบรันต่อใบ
- ฉบับ Vnn หรือ Final (บล็อก) · ฉบับสมบูรณ์ แต่ฉบับไม่ใช่ Final → เตือน · นำไปใช้แล้ว ต้องมีวันที่มีผล (บล็อก) · วันที่ยกเลิกสิทธิ ≥ วันที่ให้สิทธิ · หมดอายุ/ยกเลิก ต้องมีวันที่ยกเลิกสิทธิ (บล็อก) (DEC-04/19/20/21)
- ตัวเลือก: สถานะเอกสาร 6 · สถานะการเปลี่ยนแปลง 4 · ระดับสิทธิ 4 · สถานะสิทธิ 3 (ตาม data validation ต้นฉบับ) · พิมพ์เป็น label ไทย

## 4. กติกาการพิมพ์
- หน้า 1 = หัว + ชื่อโครงการ + ข้อมูลกระบวนการ + โครงสร้างโฟลเดอร์ + มาตรฐานการตั้งชื่อไฟล์ + ทะเบียนเอกสาร (D-) · ท้ายหน้า "มีต่อหน้าถัดไป" · footer "หน้า 1/2"
- หน้า 2 (`.page-break`) = หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่) + การเปลี่ยนแปลงเอกสาร (หัว "ทะเบียนสถานะเอกสารและประวัติฉบับ (ต่อ)") + บันทึกสิทธิ + หมายเหตุการใช้งาน + การตรวจทาน/อนุมัติ (`.signs-block` ไม่ตัดข้ามหน้า) + ประวัติการแก้ไข · footer "หน้า 2/2"
- ทุกตารางแถวซ้ำมี `thead` → แถวเกินหน้า หัวตารางซ้ำ · แถวไม่ตัดกลาง

## 5. วิธี build ใหม่
```bash
TD_SCRIPTS=$TD/scripts python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มห้องข้อมูล มาตรฐานชื่อไฟล์ และทะเบียนควบคุมเอกสาร" --max-pages 2   # ต้องมี browser
```

## 6. Checklist
- [x] parity IDENTICAL 5/5 · [x] ไม่มี {{}} หลง (render_doc --strict + build_html ทุกสถานะ) · [x] ฟอนต์ ≥ 8pt · [x] ลายเซ็นครบตามสาย DOA (3 / 7 ช่อง)
- [ ] ทุกสถานะ 2 หน้าเท่ากัน — **[NO-BROWSER] ยังไม่ได้ตรวจ** (render_states/render_pdf ข้าม) → รันรอบเต็มบนเครื่องที่มี browser

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `4. FM-IVM-04 แบบฟอร์มห้องข้อมูล มาตรฐานชื่อไฟล์ และทะเบียนควบคุมเอกสาร.xlsx` · Doc. No. FM-IVM-04 · Rev.00 : 01/07/2569
- Profile token ที่ต่าง: form_fs 8pt · form_title_fs 14pt · form_logo_h 11mm · form_title_gap 2px · form_grid_gap 4px
- ความต่างที่ตั้งใจ: แบ่ง 2 หน้า (R10) ตัดก่อนตารางการเปลี่ยนแปลง · ช่องเพิ่ม ชื่อโครงการ / ธุรกรรม (แถว 4 ที่ว่างบนกระดาษ · DEC-09) · หัว "(ต่อ)" ของตารางการเปลี่ยนแปลงบนหน้า 2 (กระดาษไม่มีหัวหมวด · DEC-17) · ตารางโฟลเดอร์ 6 คอลัมน์ขยายเต็มกรอบ (DEC-22) · ตารางลงชื่อวนตาม DOA (ไม่ fix 3 แถว) · ช่องลายเซ็น = ☐/☑ คำตัดสิน + "พิจารณาในระบบ วันที่ เวลา" (DEC-10) · footer เลขที่ + CUBE NATIVE · โลโก้จาก Organization · แถบหัวหมวดสีน้ำเงินเข้ม → หมึกเดียวตัวหนา
- compare_original: **[NO-BROWSER] ข้าม** (ต้องใช้ PDF สถานะ approved) — ต้องรันบนเครื่องที่มี browser แล้วบันทึกคะแนนที่นี่

## 8. (Replica) Data contract + สถานะ
- parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: draft (โฟลเดอร์ 3 + เอกสาร 1) · approved · rejected (ผู้ตรวจสอบส่งกลับ) · long-10folders-8docs-7changes-8access (dense) · approved-doa6steps (7 ช่องลงชื่อ)

### Data contract
| key | source | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| company.name · company.name_line · company.logo | Organization snapshot | บริษัท ตัวอย่าง จำกัด (มหาชน) | logo = data URI |
| doc.no · doc.is_draft · doc.form_code · doc.revision | ENG-DOC-NUM · state · print_config | IVMD-2569-0003 | is_draft ใช้เป็นเงื่อนไขเท่านั้น |
| project.name | ivmd | โครงการลงทุนตัวอย่าง A | |
| naming.* (5 key) | FileNamingPolicy | YYYYMMDD | snapshot ตอนออกเลข |
| folders[] (6 key) | ivmd_folder | 01 · จำกัดเฉพาะกลุ่ม | เติมแถวจนครบ 8 (ชื่อโฟลเดอร์มาตรฐาน) |
| documents[] (10 key) | ivmd_document | D-001 · V03 · ฉบับสมบูรณ์ | เติมแถวว่างจนครบ 5 (รหัสต่อเนื่อง) |
| changes[] (10 key) | ivmd_change | CH-001 · นำไปใช้แล้ว | เติมแถวว่างจนครบ 5 |
| access[] (10 key) | ivmd_access | 1 · อ่านอย่างเดียว · ใช้งาน | เติมแถวว่างจนครบ 5 |
| sign_rows[].signs[] {role,name,position,date,decision} | sign_rows.py | ☑ ตรวจสอบแล้ว ☐ ส่งกลับ | คำตัดสินตาม role |
| form_revisions[] {rev,date,detail,prepared_by,approved_by} | DOCCFG | 00 · 01/07/2569 | |
| layout.dense | แถวเกินขั้นต่ำกลุ่มใดกลุ่มหนึ่ง หรือขั้น > 4 | false | |

## 9. (Replica) print_config
```json
{
  "doc_type": "IVMD",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-IVM-04",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages": 2,
  "min_rows": 5,
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
    "form_revisions": "DOCCFG.revisions[] ของ IVMD",
    "naming": "FileNamingPolicy.{pattern,date_format,version_format,status_tokens,example} (snapshot ตอนออกเลข · DEC-04)",
    "folders_default": "DataRoomPolicy.default_folders (8 โฟลเดอร์ 01–08 ตั้งต้นใบใหม่)",
    "status_labels": "ivmd.doc_status (6) · ivmd.change_status (4) · ivmd.access_level (4) · ivmd.access_status (3) ตาม data validation ต้นฉบับ"
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
  "page_break": "ก่อนตารางการเปลี่ยนแปลงเอกสาร (CH-) — หน้า 1 = หัว+ข้อมูลกระบวนการ+โครงสร้างโฟลเดอร์+มาตรฐานชื่อไฟล์+ทะเบียนเอกสาร · หน้า 2 = หัวย่อ+การเปลี่ยนแปลงเอกสาร (หัว \"(ต่อ)\")+บันทึกสิทธิ+หมายเหตุการใช้งาน+การตรวจทาน/อนุมัติ+ประวัติการแก้ไข (R10)",
  "min_rows_by_group": {
    "folders": 8,
    "documents": 5,
    "changes": 5,
    "access": 5
  }
}
```
