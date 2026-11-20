# PRINT SPEC — แบบฟอร์มสรุปผลการคัดกรองโครงการเบื้องต้น (SCR)

> เอกสารประกอบสำหรับ Dev — แนบคู่ FRD/Brief ของ F-TMP-003 · โหมด **Replica** (แบบฟอร์มลูกค้า FM-BDM-03)
> ไฟล์คู่: `form.tpl.html` (logic-less · แหล่งเดียวทั้ง prototype และ server) · `FM-BDM-03_template.html` (build แล้ว ฝังฟอนต์) · `profile.json` · `*.data.json` · `print_config.json`
> **[NO-BROWSER]** เครื่องที่ทำงานไม่มี browser → ไม่มี PDF ในชุดนี้ · แบบพิมพ์ทุกสถานะอยู่เป็น HTML (`out/*.html`) · ตรวจจำนวนหน้าด้วย Chromium บน cloud container (verify-only, ไม่ใส่ผลในชุด): ทุกสถานะ = 2 หน้า — ต้องรัน `render_states.py --max-pages 2` บนเครื่องที่มี browser ก่อน UAT

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มสรุปผลการคัดกรองโครงการเบื้องต้น / Preliminary Project Screening Summary · doc_type `SCR` · Doc. No. FM-BDM-03 · Rev.00 : 01/07/2569
- **ขนาด:** A4 แนวตั้ง · **2 หน้า (R10)** — ที่ 9pt ตารางเกณฑ์ 8 แถว (ข้อความเหตุผลหลายบรรทัด) + ข้อสรุป 6 หัวข้อ + ลงชื่อ (DOA 6 ขั้น = 7 แถว) + ประวัติ ใส่ 1 หน้าไม่ได้ (ทดสอบ 1 หน้าแล้ว DOA 6 ขั้น/ข้อความยาว ล้นเป็น 2 หน้า)
- **ฟอนต์:** Sarabun 9pt (form_fs) · หมึกเดียว (Replica)
- **โครง 2 หน้า:** หน้า 1 = หัวกระดาษ + ข้อมูลแบบฟอร์ม + การประเมินและคัดกรองโครงการ (8 เกณฑ์ + คะแนนรวมถ่วงน้ำหนัก + ผลเสนอ) + "มีต่อหน้าถัดไป" · หน้า 2 = หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่) + ข้อสรุปการคัดกรอง + บล็อกลงชื่อทั้งก้อน (ไม่ตัดข้ามหน้า) + ประวัติการแก้ไข · footer ทุกหน้า "หน้า N/2" + เลขที่
- ตัดหน้าตั้งใจหลังตารางการประเมิน (ไม่ใช่ก่อนบล็อกลงชื่อพอดี) เพราะข้อความยาวในตารางเกณฑ์ + ข้อสรุป ทำให้หน้า 1 ล้น — บล็อกลงชื่ออยู่หน้า 2 ทั้งก้อนเสมอ · ตารางเกณฑ์มี thead (ซ้ำเองถ้าล้น)

## 2. Field Mapping / Data contract
| key ใน data | ช่องบนกระดาษ | Source (entity.field) | Format | หมายเหตุ |
|---|---|---|---|---|
| `company.logo` · `company.name` · `company.group_line` | โลโก้ · บรรทัด "บริษัท … และบริษัทในเครือ" | Organization snapshot ตอนออกเลข | data URI / text | ไม่เก็บใน template |
| `doc.title` | แบบฟอร์มสรุปผลการคัดกรองโครงการเบื้องต้น | DocCfg.name | text | |
| `doc.no` · `doc.is_draft` | footer เลขที่ | ENG-DOC-NUM (SCR) | `SCR-พ.ศ.-running` | ออกตอนบันทึกครั้งแรก |
| `doc.form_code` · `doc.revision` | Doc. No. / Rev. | print_config | text | |
| `criteria[]` | ตารางการประเมิน 8 แถว | ScreeningResult.criteria[] (snapshot ScreeningCriteria.items) | — | 8 แถวคงที่ |
| ├ `criterion` · `weight` | เกณฑ์ประเมิน · น้ำหนัก (%) | ScreeningCriteria.items[].name / weight_pct | text / "15" | config snapshot |
| ├ `score` | คะแนน (1-5) | criteria[].score | "1"–"5" | ว่างได้ในร่าง |
| ├ `weighted_score` | คะแนนถ่วงน้ำหนัก | computed = weight × score / 5 | string | ว่างถ้ายังไม่ให้คะแนน |
| └ `rationale` · `risk_condition` | เหตุผล / หลักฐาน · ความเสี่ยง / เงื่อนไข | criteria[] | text | |
| `screening.total_score` | คะแนนรวมถ่วงน้ำหนัก | computed = Σ weighted_score | string | ว่างจนกว่าให้คะแนนครบ 8 |
| `screening.recommendation` | ข้อความหลังคะแนนรวม | computed ตาม ScreeningCriteria.recommend_bands | text | ≥80 / ≥60 / <60 |
| `summary.strengths` · `concerns` · `info_needed` · `decision` · `conditions` · `next_steps` | ข้อสรุปการคัดกรอง 6 หัวข้อ | ScreeningResult.summary.* | text | decision = ดำเนินการต่อ / ดำเนินการต่อแบบมีเงื่อนไข / ไม่ดำเนินการต่อ |
| `sign_rows[].signs[]` | การตรวจทาน / อนุมัติ (บทบาท ชื่อ ตำแหน่ง ลายเซ็น วันที่) | approval_chain snapshot + sign_rows.py | — | ผู้จัดทำ + 1 แถวต่อขั้น DOA (ไม่ fix) · คำตัดสินตาม role |
| `form_revisions[]` | ประวัติการแก้ไข | DocumentConfig.form_revisions (F003) | text | ประวัติฉบับของแบบฟอร์ม |
| `layout.dense` | — | ข้อความยาว หรือขั้น DOA > 4 | boolean | section เท่านั้น |

## 3. กติกาคำนวณ
- `weighted_score = weight × score / 5` (แสดงจำนวนเต็มถ้าลงตัว ไม่งั้น 2 ตำแหน่ง)
- `total_score = Σ weighted_score` (เต็ม 100) · `recommendation`: ≥ 80 เสนอให้ดำเนินการต่อ · ≥ 60 ดำเนินการต่อแบบมีเงื่อนไข · < 60 ไม่เสนอให้ดำเนินการต่อ
- ยังไม่ให้คะแนน → ช่องว่าง (ต้นฉบับ Excel แสดง 0 และ "ไม่เสนอ…" — แก้ตาม anomaly)

## 4. กติกาการพิมพ์
- thead ซ้ำ · ห้ามตัดแถวกลาง · `.signs-block` ไม่ตัดข้ามหน้า · `.page-break` ก่อนหน้า 2 (ตั้งใจ) · ทุกสถานะ 2 หน้า

## 5. วิธี build ใหม่
```bash
python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มสรุปผลการคัดกรองโครงการเบื้องต้น" --max-pages 2
```

## 6. Checklist
- [x] parity IDENTICAL 5/5 · [x] ไม่มี {{}} หลง · [x] ฟอนต์ 9pt (≥ 8pt) · [x] ทุกสถานะ 2 หน้า (verify Chromium container) · [ ] PDF จริงบนเครื่องที่มี browser

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `3. FM-BDM-03 แบบฟอร์มสรุปผลการคัดกรองโครงการเบื้องต้น.xlsx` (1 ชีต · พิมพ์ย่อ scale 48% ลง 1 หน้า) · Doc No. FM-BDM-03 · Rev.00 : 01/07/2569
- Profile: form_fs 9pt · form_lh 1.35 · title 14pt · logo 11mm · grid row 5.8mm
- ความต่างที่ตั้งใจ: (1) 2 หน้าแทน 1 หน้า (R10 — ต้นฉบับย่อ 48% ตัวอักษร < 8pt) (2) ช่องลงชื่อเป็นแถวต่อขั้น DOA (ผู้จัดทำ + N ขั้น) ข้อความ "ส่งในระบบ/พิจารณาในระบบ" + คำตัดสินตาม role แทนลายมือ (3) หัวตารางสีพื้นเข้ม → หมึกเดียว (4) footer เลขที่ + "หน้า N/2" (5) ตัด "0" ในแถวที่ยังไม่ให้คะแนน
- ผล compare_original (approved หน้า 1 vs ต้นฉบับ · region 0:0.6 · Chromium container): score 0.403 (**WARN**) — อธิบายได้: ต้นฉบับเป็นภาพ Excel ย่อทั้งชีตลง 1 หน้า ส่วนแบบพิมพ์ระบบเป็น 2 หน้าที่ 9pt ตำแหน่งบรรทัดจึงไม่ตรง แต่ลำดับบล็อก/ถ้อยคำ/คอลัมน์ตรงกระดาษครบ · AI ดูภาพวางคู่แล้ว (unattended — ให้คนยืนยันจาก _BATCH_REPORT)

## 8. (Replica) สถานะที่ทดสอบ
- parity JS ↔ Python: IDENTICAL 5/5
- draft (ให้คะแนน 3/8 · รอพิจารณา) · approved (คะแนน 73 มีเงื่อนไข · 2 ขั้น) · rejected (คะแนน 48 · ผู้ตรวจสอบไม่ผ่าน) · long-text (ข้อความยาวทุกช่อง · dense) · approved-doa6steps (DOA 6 ขั้น → 7 ช่อง 4+3) → ทุกสถานะ 2 หน้า

## 9. (Replica) print_config
```json
{
  "doc_type": "SCR",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-BDM-03",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages": 2,
  "page_break": "ตั้งใจหลังตารางการประเมิน: หน้า 1 = หัว + การประเมิน 8 เกณฑ์ + คะแนนรวม · หน้า 2 = ข้อสรุปการคัดกรอง + การตรวจทาน / อนุมัติ (ช่องลงชื่อ dynamic ตาม DOA · ไม่ตัดข้ามหน้า) + ประวัติการแก้ไข",
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
        "reject": "ไม่ผ่านการตรวจสอบ"
      },
      "role-gm": {
        "approve": "อนุมัติ / รับทราบ",
        "reject": "ไม่อนุมัติ"
      }
    }
  },
  "config_reads": {
    "criteria[].criterion + criteria[].weight": "ScreeningCriteria.items (snapshot ลงเอกสารตอนสร้าง)",
    "screening.recommendation": "ScreeningCriteria.recommend_bands (≥80 / ≥60 / <60)",
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
