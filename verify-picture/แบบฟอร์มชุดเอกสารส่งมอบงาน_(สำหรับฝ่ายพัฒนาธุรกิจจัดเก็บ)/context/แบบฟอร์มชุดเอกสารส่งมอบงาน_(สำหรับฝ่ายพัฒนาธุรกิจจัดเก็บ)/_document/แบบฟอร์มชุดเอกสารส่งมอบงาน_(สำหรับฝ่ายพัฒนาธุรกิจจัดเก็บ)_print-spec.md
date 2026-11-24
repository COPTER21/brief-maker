# PRINT SPEC — แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายพัฒนาธุรกิจจัดเก็บ) (HOB)

> เอกสารประกอบสำหรับ Dev — แนบคู่ FRD/Brief ของ F-TMP-007 · โหมด **Replica** (แบบฟอร์มลูกค้า FM-BDM-07)
> ไฟล์คู่: `form.tpl.html` (logic-less · แหล่งเดียวทั้ง prototype และ server) · `FM-BDM-07_template.html` (build แล้ว ฝังฟอนต์) · `profile.json` · `*.data.json` · `print_config.json`
> **[NO-BROWSER]** เครื่องที่ทำงานไม่มี browser → ไม่มี PDF ในชุดนี้ · แบบพิมพ์ทุกสถานะอยู่เป็น HTML (`out/*.html`) · ตรวจจำนวนหน้าด้วย Chromium บน cloud container (verify-only, ไม่ใส่ผลเข้าชุด): ทุกสถานะ = 2 หน้า — ต้องรัน `render_states.py --max-pages 2` + `compare_original.py` บนเครื่องที่มี browser ก่อน UAT

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายพัฒนาธุรกิจจัดเก็บ) / Handover Document Package (BD copy) · doc_type `HOB` · Doc. No. FM-BDM-07 · Rev.00 : 01/07/2569
- **ขนาด:** A4 แนวตั้ง · **2 หน้า (R10)** — ข้อมูลการส่งมอบ 6 แถว + รายการเอกสาร 12+ แถว (ข้อความหลายบรรทัด) + สมมติฐาน 4 แถว + ลงชื่อ (สูงสุด 7 แถว) + ประวัติ ใส่ 1 หน้าไม่ได้ที่ฟอนต์ ≥ 8pt
- **ฟอนต์:** Sarabun 8pt (form_fs) · หมึกเดียว (Replica)
- **โครง 2 หน้า:** หน้า 1 = หัวกระดาษ + ข้อมูลแบบฟอร์ม (ใช้ในขั้นตอน · วัตถุประสงค์ · ผู้จัดทำ · ผู้ตรวจสอบ · ผู้อนุมัติ/รับทราบ) + ข้อมูลการส่งมอบ + รายการเอกสารแถว 1–14 + "มีต่อหน้าถัดไป" · หน้า 2 = หัวย่อ (ชื่อเอกสาร + เลขที่) + รายการเอกสารต่อ (แถว 15+, thead ซ้ำ) + สมมติฐาน ประเด็นค้าง และข้อจำกัด + บล็อกลงชื่อทั้งก้อน + ประวัติการแก้ไข · footer ทุกหน้า "หน้า N/2" + เลขที่

## 2. Field Mapping / Data contract
| key ใน data | ช่องบนกระดาษ | Source (entity.field) | Format | หมายเหตุ |
|---|---|---|---|---|
| `company.logo` · `company.name` · `company.group_line` | โลโก้ · บรรทัด "บริษัท … และบริษัทในเครือ" | Organization snapshot ตอนออกเลข | data URI / text | ไม่เก็บใน template |
| `doc.title` | แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายพัฒนาธุรกิจจัดเก็บ) | DocCfg.name | text | |
| `doc.no` · `doc.is_draft` | footer เลขที่ | ENG-DOC-NUM (HOB) | `HOB-พ.ศ.-running` | ออกตอนบันทึกครั้งแรก (DEC-10) |
| `doc.form_code` · `doc.revision` | Doc. No. / Rev. | print_config | text | |
| `handover.project_name` | ชื่อโครงการ | HandoverPackage.project_name | text | |
| `handover.sender` | ผู้ส่งมอบ | HandoverPackage.sender | text | ชื่อพนักงาน |
| `handover.receiver` | ผู้รับมอบ / ฝ่ายบริหารการลงทุน | HandoverPackage.receiver | text | ค่าเริ่มผู้พิจารณาขั้นรับทราบ (DEC-15) |
| `handover.handover_date` | วันที่ส่งมอบ | HandoverPackage.handover_date | dd/mm/พ.ศ. | |
| `handover.package_version` | ฉบับชุดเอกสาร | HandoverPackage.package_version | text | |
| `handover.data_status` | สถานะข้อมูล | HandoverPackage.data_status | สมบูรณ์ / มีข้อจำกัด / รอข้อมูลเพิ่มเติม | HandoverPackageConfig.data_statuses |
| `docs_p1[]` / `docs_p2[]` | รายการเอกสารในชุดส่งมอบ | HandoverPackage.docs[] | — | data แบ่ง: หน้า 1 = 14 แถว · หน้า 2 = ที่เหลือ · เติมแถวว่างครบ 12 (min_rows) |
| ├ `seq` | ลำดับ | auto | "1".. | |
| ├ `doc_name` · `doc_ref` | ชื่อเอกสาร · รหัส / ฉบับ | docs[] | text | ผู้ใช้กรอกเลขอ้างอิงเอง (DEC-01) |
| ├ `doc_date` | วันที่เอกสาร | docs[].doc_date | dd/mm/พ.ศ. | ≤ วันที่ส่งมอบ (เตือน · DEC-16) |
| ├ `owner` | ผู้รับผิดชอบ | docs[].owner | text | |
| ├ `status` | สถานะ | docs[].status | ครบถ้วน / มีข้อจำกัด / ขาดเอกสาร / ไม่เกี่ยวข้อง | HandoverPackageConfig.doc_statuses |
| └ `location` · `remark` | ตำแหน่งจัดเก็บ / ลิงก์ · หมายเหตุ | docs[] | text | |
| `has_p2_rows` | — | computed | boolean (section เท่านั้น) | |
| `notes.assumptions` · `notes.open_issues` · `notes.data_limits` · `notes.bd_support` | สมมติฐานสำคัญ · ประเด็นค้าง · ข้อจำกัดของข้อมูล · งานที่ฝ่ายพัฒนาธุรกิจยังต้องสนับสนุน | HandoverPackage.notes | text | ข้อจำกัดของข้อมูลบังคับเมื่อมีข้อจำกัด (DEC-14) |
| `sign_rows[].signs[]` | การตรวจทาน / อนุมัติ (บทบาท ชื่อ ตำแหน่ง ลายเซ็น วันที่) | approval_chain snapshot + sign_rows.py | — | ผู้จัดทำ + 1 แถวต่อขั้น DOA (ไม่ fix) · คำตัดสินตาม role |
| `form_revisions[]` | ประวัติการแก้ไข | DocumentConfig.form_revisions (F003) | text | ประวัติฉบับของแบบฟอร์ม ไม่ใช่ช่องกรอกต่อใบ |
| `layout.dense` | — | rows > 20 หรือขั้น DOA > 4 | boolean | |

## 3. กติกา (ไม่มีสูตรคำนวณ)
- ไม่ใช้รายการตัวเลือกค้าง 1–5 ที่ C13:C18 ของต้นฉบับ (DEC-12)
- สถานะข้อมูล = สมบูรณ์ ขณะมีรายการ ขาดเอกสาร/มีข้อจำกัด = เตือน (DEC-13)
- สถานะข้อมูล = มีข้อจำกัด หรือมีรายการสถานะ มีข้อจำกัด → ต้องกรอกข้อจำกัดของข้อมูล (DEC-14)
- วันที่เอกสาร > วันที่ส่งมอบ = เตือน (DEC-16)

## 4. กติกาการพิมพ์
- thead ซ้ำ · ห้ามตัดแถวกลาง · `.signs-block` ไม่ตัดข้ามหน้า · `.page-break` ก่อนหน้า 2 (ตั้งใจ) · ทุกสถานะ 2 หน้า

## 5. วิธี build ใหม่
```bash
python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายพัฒนาธุรกิจจัดเก็บ)" --max-pages 2
```

## 6. Checklist
- [x] parity IDENTICAL 5/5 · [x] ไม่มี {{}} หลง · [x] ฟอนต์ 8pt (ไม่ต่ำกว่า) · [x] ทุกสถานะ 2 หน้า (verify Chromium container) · [ ] PDF จริง + compare_original บนเครื่องที่มี browser

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `7. FM-BDM-07 แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายพัฒนาธุรกิจจัดเก็บ).xlsx` (1 ชีต · พิมพ์ย่อทั้งชีตลง 1 หน้า) · Doc No. FM-BDM-07 · Rev.00 : 01/07/2569
- Profile: form_fs 8pt · form_lh 1.35 · title 13pt · logo 11mm · grid row 5.6mm
- ความต่างที่ตั้งใจ: (1) 2 หน้าแทน 1 หน้า (R10) (2) รายการเอกสารแบ่ง 14 + ต่อหน้า 2 พร้อมหัวตารางซ้ำ (3) ช่องลงชื่อเป็นแถวต่อขั้น DOA (ผู้จัดทำ + N ขั้น) ข้อความ "ส่งในระบบ/พิจารณาในระบบ" + คำตัดสินตาม role แทนลายมือ (4) แถบหัวข้อหมึกเดียว (ไม่ระบายสีพื้นเข้ม) (5) footer เลขที่ + "หน้า N/2"
- **[NO-BROWSER] ข้าม compare_original.py** — ยังไม่มีคะแนนเทียบต้นฉบับ · ลำดับบล็อก/ถ้อยคำ/คอลัมน์ตรงกระดาษครบ (AI ดูภาพหน้า 1–2 จาก Chromium container แล้ว · unattended — ให้คนยืนยันจาก _BATCH_REPORT)

## 8. (Replica) สถานะที่ทดสอบ
- parity JS ↔ Python: IDENTICAL 5/5
- draft (3 รายการ · รอพิจารณา) · approved (8 รายการ มีขาดเอกสาร/ไม่เกี่ยวข้อง · 2 ขั้น รับมอบแล้ว · สถานะข้อมูล มีข้อจำกัด) · rejected (7 รายการ · ผู้ตรวจสอบไม่ผ่าน · รอข้อมูลเพิ่มเติม) · long-24rows (24 แถว 14+10 · dense) · approved-doa6steps (DOA 6 ขั้น → 7 ช่อง) → ทุกสถานะ 2 หน้า

## 9. (Replica) print_config
```json
{
  "doc_type": "HOB",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-BDM-07",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages": 2,
  "page_break": "ก่อนหน้า 2 = รายการเอกสารต่อ (แถวที่ 15 ขึ้นไป) + สมมติฐาน ประเด็นค้าง และข้อจำกัด + บล็อกลงชื่อ + ประวัติการแก้ไข",
  "min_rows": 12,
  "rows_page1": 14,
  "rows_page2_max": 14,
  "dense_when_rows_over": 20,
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    { "box": "requester", "label": "ผู้จัดทำ", "show_date": true },
    { "box": "doa_step:*", "label": "from_doa_step", "show_decision": true, "show_date": true }
  ],
  "decision_words": {
    "default": { "approve": "อนุมัติ", "reject": "ไม่อนุมัติ" },
    "by_role": {
      "role-line-manager": { "approve": "ตรวจสอบแล้ว", "reject": "ไม่ผ่านการตรวจสอบ" },
      "role-mgr-bu": { "approve": "รับมอบ / รับทราบ", "reject": "ไม่รับมอบ" }
    }
  },
  "config_reads": {
    "docs[].status": "HandoverPackageConfig.doc_statuses",
    "handover.data_status": "HandoverPackageConfig.data_statuses",
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
