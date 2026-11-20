# PRINT SPEC — แบบฟอร์มประเมินความเสี่ยง (RSK)

> เอกสารประกอบสำหรับ Dev — แนบคู่ FRD/Brief ของ F-TMP-002 · โหมด **Replica** (แบบฟอร์มลูกค้า FM-BDM-02)
> ไฟล์คู่: `form.tpl.html` (logic-less · แหล่งเดียวทั้ง prototype และ server) · `FM-BDM-02_template.html` (build แล้ว ฝังฟอนต์) · `profile.json` · `*.data.json` · `print_config.json`
> **[NO-BROWSER]** เครื่องที่ทำงานไม่มี browser → ไม่มี PDF ในชุดนี้ · แบบพิมพ์ทุกสถานะอยู่เป็น HTML (`out/*.html`) · ตรวจจำนวนหน้าด้วย Chromium บน cloud container (verify-only): ทุกสถานะ = 2 หน้า · ภาพ `out/_states_sheet.png` (หน้า 1) + `out/_states_sheet_p2.png` (หน้า 2) — ต้องรัน `render_states.py --max-pages 2` บนเครื่องที่มี browser ก่อน UAT

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มประเมินความเสี่ยง / Risk Assessment Form · doc_type `RSK` · Doc. No. FM-BDM-02 · Rev.00 : 01/07/2569
- **ขนาด:** A4 แนวตั้ง · **2 หน้า (R10)** — ตาราง 10 คอลัมน์ 18 แถว + เกณฑ์ + สรุประดับ + ลงชื่อ + ประวัติ ใส่ 1 หน้าไม่ได้ที่ฟอนต์ ≥ 8pt
- **ฟอนต์:** Sarabun 8pt (form_fs) · หมึกเดียว (Replica)
- **โครง 2 หน้า:** หน้า 1 = หัวกระดาษ + ข้อมูลแบบฟอร์ม + เกณฑ์การประเมิน + ทะเบียนแถว 1–14 + "มีต่อหน้าถัดไป" · หน้า 2 = หัวย่อ (ชื่อเอกสาร + เลขที่) + ทะเบียนต่อ (แถว 15+, thead ซ้ำ) + สรุประดับความเสี่ยง + บล็อกลงชื่อทั้งก้อน + ประวัติการแก้ไข · footer ทุกหน้า "หน้า N/2" + เลขที่

## 2. Field Mapping / Data contract
| key ใน data | ช่องบนกระดาษ | Source (entity.field) | Format | หมายเหตุ |
|---|---|---|---|---|
| `company.logo` · `company.name` · `company.group_line` | โลโก้ · บรรทัด "บริษัท … และบริษัทในเครือ" | Organization snapshot ตอนออกเลข | data URI / text | ไม่เก็บใน template |
| `doc.title` | แบบฟอร์มประเมินความเสี่ยง | DocCfg.name | text | |
| `doc.no` · `doc.is_draft` | footer เลขที่ | ENG-DOC-NUM (RSK) | `RSK-พ.ศ.-running` | ออกตอนบันทึกครั้งแรก (DEC-10) |
| `doc.form_code` · `doc.revision` | Doc. No. / Rev. | print_config | text | |
| `criteria[]` {score,l_name,l_desc,i_name,i_desc} | ตารางเกณฑ์ 5 แถว | RiskMatrix.likelihood_scale + impact_scale | text | config (DEC-04) |
| `risks_p1[]` / `risks_p2[]` | ทะเบียนความเสี่ยง | RiskAssessment.risks[] | — | data แบ่ง: หน้า 1 = 14 แถว · หน้า 2 = ที่เหลือ · เติมแถวว่างครบ 18 (min_rows) |
| ├ `seq` | ลำดับ | auto | "1".. | |
| ├ `category` | ประเภทความเสี่ยง | risks[].category | text | RiskMatrix.categories |
| ├ `description` · `cause_effect` · `control_measure` | รายละเอียด · สาเหตุ / ผลกระทบ · มาตรการควบคุม | risks[] | text | |
| ├ `likelihood` · `impact` | โอกาสเกิด/ผลกระทบก่อนควบคุม | risks[] | "1"–"5" | |
| ├ `inherent_score` | คะแนนก่อนควบคุม | computed = likelihood × impact | string | ว่างถ้ายังกรอกไม่ครบ (DEC-14) |
| ├ `residual_score` | คะแนนคงเหลือ | risks[] | string | ชุดผลคูณเท่านั้น (DEC-12) |
| └ `status` | สถานะ | risks[] | เปิด / อยู่ระหว่างจัดการ / ติดตามผล / ปิดแล้ว | |
| `has_p2_rows` | — | computed | boolean (section เท่านั้น) | |
| `level_rows[]` | สรุประดับความเสี่ยง (2 ช่วงต่อแถว) | RiskMatrix.level_bands | text | config |
| `sign_rows[].signs[]` | การตรวจทาน / อนุมัติ (บทบาท ชื่อ ตำแหน่ง ลายเซ็น วันที่) | approval_chain snapshot + sign_rows.py | — | ผู้จัดทำ + 1 แถวต่อขั้น DOA (ไม่ fix) · คำตัดสินตาม role |
| `form_revisions[]` | ประวัติการแก้ไข | DocumentConfig.form_revisions (F003) | text | ประวัติฉบับของแบบฟอร์ม ไม่ใช่ช่องกรอกต่อใบ |
| `layout.dense` | — | rows > 18 หรือขั้น DOA > 4 | boolean | |

## 3. กติกาคำนวณ
- `inherent_score = likelihood × impact` (ทั้งคู่ต้องมีค่า ไม่งั้น "")
- ระดับ = RiskMatrix.level_bands (1-4 ต่ำ · 5-9 ปานกลาง · 10-16 สูง · 17-25 สูงมาก) — แบบพิมพ์ไม่เพิ่มคอลัมน์ (DEC-16) · หน้าจอแสดงสี
- `residual_score ∈ {1,2,3,4,5,6,8,9,10,12,15,16,20,25}` · > inherent = เตือน (DEC-13)

## 4. กติกาการพิมพ์
- thead ซ้ำ · ห้ามตัดแถวกลาง · `.signs-block` ไม่ตัดข้ามหน้า · `.page-break` ก่อนหน้า 2 (ตั้งใจ) · ทุกสถานะ 2 หน้า

## 5. วิธี build ใหม่
```bash
python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มประเมินความเสี่ยง" --max-pages 2
```

## 6. Checklist
- [x] parity IDENTICAL 5/5 · [x] ไม่มี {{}} หลง · [x] ฟอนต์ 8pt (ไม่ต่ำกว่า) · [x] ทุกสถานะ 2 หน้า (verify Chromium container) · [ ] PDF จริงบนเครื่องที่มี browser

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `2. FM-BDM-02 แบบฟอร์มประเมินความเสี่ยง.xlsx` (1 ชีต · พิมพ์ย่อทั้งชีตลง 1 หน้า) · Doc No. FM-BDM-02 · Rev.00 : 01/07/2569
- Profile: form_fs 8pt · form_lh 1.35 · title 14pt · logo 11mm · grid row 5.6mm
- ความต่างที่ตั้งใจ: (1) 2 หน้าแทน 1 หน้า (R10 — ต้นฉบับ Excel ย่อสเกลจนตัวอักษร < 8pt) (2) ทะเบียนแบ่ง 14 + ต่อหน้า 2 พร้อมหัวตารางซ้ำ (3) ช่องลงชื่อเป็นแถวต่อขั้น DOA (ผู้จัดทำ + N ขั้น) ข้อความ "ส่งในระบบ/พิจารณาในระบบ" + คำตัดสินตาม role แทนลายมือ (4) ไม่ระบายสีคะแนน (หมึกเดียว) (5) footer เลขที่ + "หน้า N/2" (6) ตัด "0" ในแถวว่าง
- ผล compare_original (approved หน้า 1 vs ต้นฉบับ · region 0:0.6): score 0.226 (**WARN**) — อธิบายได้: ต้นฉบับเป็นภาพ Excel ย่อทั้งชีตลง 1 หน้า (ตัวอักษรเล็กมาก) ส่วนแบบพิมพ์ระบบเป็น 2 หน้าที่ 8pt ตำแหน่งบรรทัดจึงไม่ตรง แต่ลำดับบล็อก/ถ้อยคำ/คอลัมน์ตรงกระดาษครบ (ดู `compare/compare_side.png`) · AI ดูภาพวางคู่แล้ว (unattended — ให้คนยืนยันจาก _BATCH_REPORT)

## 8. (Replica) สถานะที่ทดสอบ
- parity JS ↔ Python: IDENTICAL 5/5
- draft (3 รายการ · รอพิจารณา) · approved (8 รายการ · 2 ขั้น) · rejected (ผู้ตรวจสอบส่งกลับแก้ไข) · long-24rows (24 แถว 14+10 · dense) · approved-doa6steps (DOA 6 ขั้น → 7 ช่อง) → ทุกสถานะ 2 หน้า

## 9. (Replica) print_config
```json
{
  "doc_type": "RSK",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-BDM-02",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages": 2,
  "page_break": "ก่อนหน้า 2 = ทะเบียนความเสี่ยงต่อ (แถวที่ 15 ขึ้นไป) + สรุประดับความเสี่ยง + บล็อกลงชื่อ + ประวัติการแก้ไข",
  "min_rows": 18,
  "rows_page1": 14,
  "rows_page2_max": 16,
  "dense_when_rows_over": 18,
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
        "reject": "ไม่ผ่านการตรวจสอบ"
      },
      "role-gm": {
        "approve": "อนุมัติ / รับทราบ",
        "reject": "ไม่อนุมัติ"
      }
    }
  },
  "config_reads": {
    "criteria": "RiskMatrix.likelihood_scale + RiskMatrix.impact_scale",
    "level_rows": "RiskMatrix.level_bands",
    "risks[].category": "RiskMatrix.categories",
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
