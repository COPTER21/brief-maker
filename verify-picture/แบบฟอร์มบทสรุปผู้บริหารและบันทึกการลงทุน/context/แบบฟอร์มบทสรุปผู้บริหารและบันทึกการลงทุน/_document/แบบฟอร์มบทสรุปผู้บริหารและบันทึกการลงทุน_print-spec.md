# PRINT SPEC — แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน (IVM)

> เอกสารประกอบสำหรับ Dev — แนบคู่ FRD/Brief ของ F-TMP-005 · โหมด **Replica** (แบบฟอร์มลูกค้า FM-BDM-05)
> ไฟล์คู่: `form.tpl.html` (logic-less · แหล่งเดียวทั้ง prototype และ server) · `FM-BDM-05_template.html` (build แล้ว ฝังฟอนต์) · `profile.json` · `*.data.json` · `print_config.json` · `make_data.py`
> **[NO-BROWSER]** เครื่องที่ทำงานไม่มี browser → ไม่มี PDF ในชุดนี้ · แบบพิมพ์ทุกสถานะอยู่เป็น HTML (`out/*.html`) · ตรวจจำนวนหน้าด้วย Chromium บน cloud container (verify-only): ทุกสถานะ = 2 หน้า · ภาพ `out/_states_sheet.png` (หน้า 1) + `out/_states_sheet_p2.png` (หน้า 2) — ต้องรัน `render_states.py --max-pages 2` บนเครื่องที่มี browser ก่อน UAT

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน / Executive Summary & Investment Memo · doc_type `IVM` · Doc. No. FM-BDM-05 · Rev.00 : 01/07/2569
- **ขนาด:** A4 แนวตั้ง · **2 หน้า (R10)** — บทสรุปผู้บริหาร 13 หัวข้อข้อความยาว + ข้อมูลสรุป 4 ช่อง + ตารางเอกสารและเงื่อนไขประกอบ (ไม่จำกัดแถว ขั้นต่ำ 6) + ลงชื่อ (สูงสุด 7 แถวเมื่อ DOA 6 ขั้น) + ประวัติ ใส่ 1 หน้าไม่ได้ที่ฟอนต์ ≥ 8pt
- **ฟอนต์:** Sarabun 8.5pt (form_fs) · หมึกเดียว (Replica)
- **โครง 2 หน้า:** หน้า 1 = หัวกระดาษ + ข้อมูลแบบฟอร์ม + ข้อมูลสรุปโครงการ / การลงทุน + บทสรุปผู้บริหารและบันทึกการลงทุน 13 หัวข้อ + "มีต่อหน้าถัดไป" · หน้า 2 = หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่) + เอกสารและเงื่อนไขประกอบ (thead ซ้ำได้ถ้าข้ามหน้า) + บล็อกลงชื่อทั้งก้อน + ประวัติการแก้ไข · footer ทุกหน้า "หน้า N/2" + เลขที่ · ตัดหน้าตั้งใจก่อนตารางเงื่อนไข/บล็อกลงชื่อ

## 2. Field Mapping / Data contract
| key ใน data | ช่องบนกระดาษ | Source (entity.field) | Format | หมายเหตุ |
|---|---|---|---|---|
| `company.logo` · `company.name` · `company.group_line` | โลโก้ · บรรทัด "บริษัท … และบริษัทในเครือ" | Organization snapshot ตอนออกเลข | data URI / text | ไม่เก็บใน template |
| `doc.title` | แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน | DocCfg.name | text | |
| `doc.no` · `doc.is_draft` | footer เลขที่ | ENG-DOC-NUM (IVM) | `IVM-พ.ศ.-running` | ออกตอนบันทึกครั้งแรก (DEC-10) |
| `doc.form_code` · `doc.revision` | Doc. No. / Rev. | print_config | text | |
| `project.name` | ชื่อโครงการ | InvestmentMemo.project_name | text | ผู้ใช้กรอก (DEC-01 · DEC-16) |
| `project.type` | ประเภทโครงการ / ธุรกรรม | InvestmentMemo.project_type | text | |
| `project.proposer` | ผู้เสนอ / ผู้รับผิดชอบ | InvestmentMemo.proposer → Employee.display_name | text | |
| `project.amount_text` | วงเงินหรือมูลค่าโดยประมาณ | InvestmentMemo.estimated_amount | `#,##0.00 บาท` (string) | ตัวเลข ≥ 0 · ส่งเป็น string (parity) |
| `memo[]` (13 แถวตายตัว) | บทสรุปผู้บริหารและบันทึกการลงทุน | InvestmentMemo.* 13 ช่อง | — | ลำดับตามกระดาษ |
| ├ `topic` | หัวข้อ | ค่าคงที่ใน template data (ถ้อยคำกระดาษ) | text | |
| └ `detail` | รายละเอียด | decision_requested · project_summary · strategic_rationale · market_opportunity · business_model · implementation_plan · financial_analysis · investment_framework · key_risks · alternatives · pre_approval_conditions · bd_recommendation · next_steps | text | ช่องว่างได้ในร่าง |
| `conditions[]` (≥6 แถว) | เอกสารและเงื่อนไขประกอบ | InvestmentMemo.conditions[] | — | ไม่จำกัด (DEC-05) · เติมแถวว่างจนครบ 6 |
| ├ `seq` | ลำดับ | running | string | |
| ├ `item` · `owner` · `due_date` · `remark` | รายการเอกสาร / เงื่อนไข · ผู้รับผิดชอบ · กำหนดเสร็จ · หมายเหตุ | conditions[] | text / วันที่ไทยย่อ | |
| └ `status` | สถานะ | conditions[].status | ยังไม่เริ่ม / กำลังดำเนินการ / แล้วเสร็จ / พักงาน | config InvestmentMemo.condition_statuses (DEC-04) |
| `sign_rows[].signs[]` | การตรวจทาน / อนุมัติ (บทบาท ชื่อ ตำแหน่ง ลายเซ็น วันที่) | approval_chain snapshot + sign_rows.py | — | ผู้จัดทำ + 1 แถวต่อขั้น DOA (ไม่ fix) · คำตัดสินตาม role |
| `form_revisions[]` | ประวัติการแก้ไข | DocumentConfig.form_revisions (F003) | text | ประวัติฉบับของแบบฟอร์ม ไม่ใช่ช่องกรอกต่อใบ |
| `layout.dense` | — | ขั้น DOA > 4 หรือแถวเงื่อนไข > 12 | boolean | |

## 3. กติกาคำนวณ / ตรวจ
- ไม่มีสูตร · วงเงินจัดรูปแบบเป็น string ก่อนส่ง template
- แถวเงื่อนไขที่กรอกต้องมีรายการ + สถานะ · สถานะยังไม่ "แล้วเสร็จ" ต้องมีผู้รับผิดชอบ + กำหนดเสร็จ (ตรวจตอนส่ง — แบบพิมพ์แสดงตามข้อมูล)

## 4. กติกาการพิมพ์
- ห้ามตัดแถวกลาง · `.signs-block` ไม่ตัดข้ามหน้า · `.page-break` ก่อนหน้า 2 (ตั้งใจ) · ทุกสถานะ 2 หน้า (แถวเงื่อนไข ≤ 20 · เกินนั้นตารางข้ามหน้า + thead ซ้ำ — ต้องยืนยันกับลูกค้า)

## 5. วิธี build ใหม่
```bash
python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน" --max-pages 2
```

## 6. Checklist
- [x] parity IDENTICAL 5/5 · [x] ไม่มี {{}} หลง · [x] ฟอนต์ 8.5pt (≥ 8pt) · [x] ทุกสถานะ 2 หน้า (verify Chromium container) · [ ] PDF จริงบนเครื่องที่มี browser

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `5. FM-BDM-05 แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน.xlsx` (1 ชีต · พิมพ์ย่อทั้งชีตลง 1 หน้า) · Doc No. FM-BDM-05 · Rev.00 : 01/07/2569
- Profile: form_fs 8.5pt · form_lh 1.35 · title 14pt · logo 11mm · grid row 6mm
- ความต่างที่ตั้งใจ: (1) 2 หน้าแทน 1 หน้า (R10 — ข้อความยาว 13 หัวข้อ + ตารางเงื่อนไขไม่จำกัด + ลงชื่อ DOA หลายขั้น) (2) ช่องลงชื่อเป็นแถวต่อขั้น DOA (ผู้จัดทำ + N ขั้น) ข้อความ "ส่งในระบบ/พิจารณาในระบบ" + คำตัดสินตาม role แทนลายมือ (3) แถบหัวหมวดตัวหนาพื้นขาวแทนพื้นน้ำเงินเข้ม (หมึกเดียว) (4) footer เลขที่ + "หน้า N/2" (5) หัวย่อหน้า 2 "(ต่อ)" + เลขที่
- ผล compare_original (approved หน้า 1 vs ต้นฉบับ · เต็มหน้า): score 0.408 (**WARN**) · region 0:0.6 = 0.357 — อธิบายได้: ต้นฉบับเป็นภาพ Excel ย่อทั้งชีตลง 1 หน้า (ตัวอักษรเล็กมาก ครึ่งล่างว่าง) ส่วนแบบพิมพ์ระบบเป็น 2 หน้าที่ 8.5pt ตารางเงื่อนไข/ลงชื่อ/ประวัติย้ายไปหน้า 2 ตำแหน่งบรรทัดจึงไม่ตรง แต่ลำดับบล็อก/ถ้อยคำ/คอลัมน์ตรงกระดาษครบ (cols 0.58 · ดู `compare/compare_side.png`) · ภาพต้นฉบับ render บนเครื่องที่ไม่มีฟอนต์ไทย · AI ดูภาพวางคู่แล้ว (unattended — ให้คนยืนยันจาก _BATCH_REPORT)

## 8. (Replica) สถานะที่ทดสอบ
- parity JS ↔ Python: IDENTICAL 5/5
- draft (กรอก 3 หัวข้อ · เงื่อนไข 1 แถว + แถวว่าง · รอพิจารณา) · approved (ครบ 13 หัวข้อ · เงื่อนไข 4 แถว 4 สถานะ · 2 ขั้น) · rejected (ผู้ตรวจสอบไม่ผ่าน) · long-12conditions (ข้อความยาวทุกหัวข้อ + เงื่อนไข 12 แถว) · approved-doa6steps (DOA 6 ขั้น → 7 ช่อง · dense) → ทุกสถานะ 2 หน้า

## 9. (Replica) print_config
```json
{
  "doc_type": "IVM",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-BDM-05",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages": 2,
  "page_break": "ก่อนหน้า 2 = เอกสารและเงื่อนไขประกอบ + บล็อกลงชื่อ + ประวัติการแก้ไข (หน้า 1 = หัว + ข้อมูลแบบฟอร์ม + ข้อมูลสรุปโครงการ/การลงทุน + บทสรุปผู้บริหาร 13 หัวข้อ)",
  "min_rows": 6,
  "rows_page1": 0,
  "rows_page2_max": 20,
  "dense_when_rows_over": 12,
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
    "conditions[].status": "InvestmentMemo.condition_statuses",
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
