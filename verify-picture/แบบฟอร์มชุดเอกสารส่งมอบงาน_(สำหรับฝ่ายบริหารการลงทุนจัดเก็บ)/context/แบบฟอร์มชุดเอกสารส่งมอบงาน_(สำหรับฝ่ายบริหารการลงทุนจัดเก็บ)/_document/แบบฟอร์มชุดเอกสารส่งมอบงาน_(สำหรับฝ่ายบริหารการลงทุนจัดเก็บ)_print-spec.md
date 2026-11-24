# PRINT SPEC — แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายบริหารการลงทุนจัดเก็บ) (HOI)

> เอกสารประกอบสำหรับ Dev — แนบคู่ FRD/Brief ของ F-TMP-008 · โหมด **Replica** (แบบฟอร์มลูกค้า FM-BDM-08)
> ไฟล์คู่: `form.tpl.html` (logic-less · แหล่งเดียวทั้ง prototype และ server) · `FM-BDM-08_template.html` (build แล้ว ฝังฟอนต์) · `profile.json` · `*.data.json` · `print_config.json`
> **[NO-BROWSER]** เครื่องที่ทำงานไม่มี browser → ไม่มี PDF ในชุดนี้ · แบบพิมพ์ทุกสถานะอยู่เป็น HTML (`out/*.html`) · ตรวจจำนวนหน้าด้วย Chromium บน cloud container (verify-only — ผลไม่ใส่เข้าชุด): ทุกสถานะ = 2 หน้า · ต้องรัน `render_states.py --max-pages 2` + `compare_original.py` บนเครื่องที่มี browser ก่อน UAT

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายบริหารการลงทุนจัดเก็บ) / Handover Package Record (Investment Management) · doc_type `HOI` · Doc. No. FM-BDM-08 · Rev.00 : 01/07/2569
- **ขนาด:** A4 แนวตั้ง · **2 หน้า (R10)** — ข้อมูลการรับมอบ 6 แถว + ผลการตรวจรับ 12+ แถว (ข้อความหลายบรรทัด) + ประเด็นค้าง 4 แถว + ลงชื่อ (สูงสุด 7 แถว) + ประวัติ ใส่ 1 หน้าไม่ได้ที่ฟอนต์ ≥ 8pt
- **ฟอนต์:** Sarabun 8pt (form_fs) · หมึกเดียว (Replica)
- **โครง 2 หน้า:** หน้า 1 = หัวกระดาษ + ข้อมูลแบบฟอร์ม (ใช้ในขั้นตอน · วัตถุประสงค์ · ผู้จัดทำ · ผู้ตรวจสอบ · ผู้อนุมัติ/รับทราบ) + ข้อมูลการรับมอบ + ผลการตรวจรับเอกสารแถว 1–12 + "มีต่อหน้าถัดไป" · หน้า 2 = หัวย่อ (ชื่อเอกสาร + เลขที่) + ผลการตรวจรับต่อ (แถว 13+, thead ซ้ำ) + ประเด็นค้างและข้อตกลงการติดตาม + บล็อกลงชื่อทั้งก้อน + ประวัติการแก้ไข · footer ทุกหน้า "หน้า N/2" + เลขที่

## 2. Field Mapping / Data contract
| key ใน data | ช่องบนกระดาษ | Source (entity.field) | Format | หมายเหตุ |
|---|---|---|---|---|
| `company.logo` · `company.name` · `company.group_line` | โลโก้ · บรรทัด "บริษัท … และบริษัทในเครือ" | Organization snapshot ตอนออกเลข | data URI / text | ไม่เก็บใน template |
| `doc.title` | แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายบริหารการลงทุนจัดเก็บ) | DocCfg.name | text | |
| `doc.no` · `doc.is_draft` | footer เลขที่ | ENG-DOC-NUM (HOI) | `HOI-พ.ศ.-running` | ออกตอนบันทึกครั้งแรก (DEC-10) |
| `doc.form_code` · `doc.revision` | Doc. No. / Rev. | print_config | text | |
| `handover.project_name` | ชื่อโครงการ | Handover.project_name | text | |
| `handover.sender` · `handover.receiver` | ผู้ส่งมอบจากฝ่ายพัฒนาธุรกิจ · ผู้รับมอบจากฝ่ายบริหารการลงทุน | Handover.sender / receiver | text | ชื่อพนักงาน (+ ตำแหน่ง) |
| `handover.received_at` | วันที่ / เวลารับมอบ | Handover.received_at | dd/mm/พ.ศ. HH:mm น. | |
| `handover.package_version` | ฉบับชุดเอกสาร | Handover.package_version | text | |
| `handover.result` | ผลการรับมอบ | Handover.result | รับมอบครบถ้วน / รับมอบแบบมีเงื่อนไข / ยังไม่รับมอบ | HandoverConfig.handover_results (DEC-04) |
| `items_p1[]` / `items_p2[]` | ผลการตรวจรับเอกสาร | Handover.items[] | — | data แบ่ง: หน้า 1 = 12 แถว · หน้า 2 = ที่เหลือ · เติมแถวว่างครบ 12 (min_rows) |
| ├ `seq` | ลำดับ | auto | "1".. | |
| ├ `doc_name` · `doc_code_rev` | ชื่อเอกสาร · รหัส / ฉบับ | items[] | text | |
| ├ `received` | ได้รับแล้ว | items[].received | ได้รับ / ไม่ได้รับ | HandoverConfig.received_options |
| ├ `completeness` | ความครบถ้วน | items[].completeness | ครบถ้วน / ไม่ครบถ้วน / ต้องตรวจสอบเพิ่มเติม | HandoverConfig.completeness_options |
| ├ `issue` · `fix_owner` | ประเด็นที่พบ · ผู้รับผิดชอบแก้ไข | items[] | text | บังคับเมื่อแถวไม่ผ่าน (DEC-14) |
| └ `due_date` | กำหนดส่งเพิ่มเติม | items[].due_date | dd/mm/พ.ศ. | ≥ วันที่รับมอบ (DEC-15) |
| `has_p2_rows` | — | computed | boolean (section เท่านั้น) | |
| `followup.open_issues` · `pending_docs` · `followup_date` · `remark` | ประเด็นค้างจากการรับมอบ · เอกสาร / ข้อมูลที่ต้องส่งเพิ่มเติม · กำหนดการติดตาม · หมายเหตุจากฝ่ายบริหารการลงทุน | Handover.followup | text / dd/mm/พ.ศ. | ประเด็นค้างบังคับเมื่อผลการรับมอบ ≠ ครบถ้วน (DEC-16) |
| `sign_rows[].signs[]` | การตรวจทาน / อนุมัติ (บทบาท ชื่อ ตำแหน่ง ลายเซ็น วันที่) | approval_chain snapshot + sign_rows.py | — | ผู้จัดทำ + 1 แถวต่อขั้น DOA (ไม่ fix) · คำตัดสินตาม role |
| `form_revisions[]` | ประวัติการแก้ไข | DocumentConfig.form_revisions (F003) | text | ประวัติฉบับของแบบฟอร์ม ไม่ใช่ช่องกรอกต่อใบ |
| `layout.dense` | — | rows > 20 หรือขั้น DOA > 4 | boolean | |

## 3. กติกา (ไม่มีสูตรคำนวณ)
- ผลการรับมอบ = รับมอบครบถ้วน ได้เมื่อทุกแถว ได้รับ + ครบถ้วน (DEC-12)
- แถว ไม่ได้รับ → ความครบถ้วน ≠ ครบถ้วน (DEC-13) · แถวไม่ผ่าน → ประเด็นที่พบ + ผู้รับผิดชอบแก้ไข + กำหนดส่งเพิ่มเติม (DEC-14)
- วันที่กำหนดส่ง/ติดตาม ≥ วันที่รับมอบ (DEC-15) · ผลการรับมอบ ≠ ครบถ้วน → ประเด็นค้างบังคับ (DEC-16)

## 4. กติกาการพิมพ์
- thead ซ้ำ · ห้ามตัดแถวกลาง · `.signs-block` ไม่ตัดข้ามหน้า · `.page-break` ก่อนหน้า 2 (ตั้งใจ) · ทุกสถานะ 2 หน้า

## 5. วิธี build ใหม่
```bash
python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายบริหารการลงทุนจัดเก็บ)" --max-pages 2
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o compare
```

## 6. Checklist
- [x] parity IDENTICAL 5/5 · [x] ไม่มี {{}} หลง · missing keys 0 · [x] ฟอนต์ 8pt (ไม่ต่ำกว่า) · [x] ทุกสถานะ 2 หน้า (verify Chromium container) · [ ] PDF จริง + compare บนเครื่องที่มี browser

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `8. FM-BDM-08 แบบฟอร์มชุดเอกสารส่งมอบงาน  (สำหรับฝ่ายบริหารการลงทุนจัดเก็บ).xlsx` (1 ชีต · พิมพ์ย่อทั้งชีตลง 1 หน้า) · Doc No. FM-BDM-08 · Rev.00 : 01/07/2569
- Profile: form_fs 8pt · form_lh 1.35 · title 13pt · logo 11mm · grid row 5.6mm
- ความต่างที่ตั้งใจ: (1) 2 หน้าแทน 1 หน้า (R10) (2) ผลการตรวจรับ 12 แถวหน้า 1 + ต่อหน้า 2 พร้อมหัวตารางซ้ำ (3) ช่องลงชื่อเป็นแถวต่อขั้น DOA (ผู้จัดทำ + N ขั้น) ข้อความ "ส่งในระบบ/พิจารณาในระบบ" + คำตัดสินตาม role แทนลายมือ (4) แถบหัวข้อหมึกเดียว (5) footer เลขที่ + "หน้า N/2"
- ผล compare_original (verify บน container · approved vs ต้นฉบับ): score 0.434 (**WARN**) · region 0:0.6 = 0.379 — อธิบายได้: ต้นฉบับเป็นภาพ Excel ย่อทั้งชีตลง 1 หน้า (แถบหัวข้อทึบ) ส่วนแบบพิมพ์ระบบเป็น 2 หน้าที่ 8pt ตำแหน่งบรรทัดจึงไม่ตรง แต่ลำดับบล็อก/ถ้อยคำ/คอลัมน์ตรงกระดาษครบ · AI ดูภาพวางคู่แล้ว (unattended — ให้คนยืนยันจาก _BATCH_REPORT)

## 8. (Replica) สถานะที่ทดสอบ
- parity JS ↔ Python: IDENTICAL 5/5
- draft (3 รายการ · รอพิจารณา) · approved (6 รายการครบ · 2 ขั้น · รับมอบครบถ้วน) · rejected (8 รายการ มีไม่ได้รับ/ต้องตรวจสอบ · ผู้ตรวจสอบไม่ผ่าน · รับมอบแบบมีเงื่อนไข + ประเด็นค้าง) · long-24rows (24 แถว 12+12 · dense) · approved-doa6steps (DOA 6 ขั้น → 7 ช่อง) → ทุกสถานะ 2 หน้า

## 9. (Replica) print_config
```json
{
  "doc_type": "HOI",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-BDM-08",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages": 2,
  "page_break": "ก่อนหน้า 2 = ผลการตรวจรับเอกสารต่อ (แถวที่ 13 ขึ้นไป) + ประเด็นค้างและข้อตกลงการติดตาม + บล็อกลงชื่อ + ประวัติการแก้ไข",
  "min_rows": 12,
  "rows_page1": 12,
  "rows_page2_max": 16,
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
      "role-mgr-bu": { "approve": "รับทราบผลการรับมอบ", "reject": "ไม่รับทราบ" }
    }
  },
  "config_reads": {
    "handover.result": "HandoverConfig.handover_results",
    "items[].received": "HandoverConfig.received_options",
    "items[].completeness": "HandoverConfig.completeness_options",
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
