# PRINT SPEC — แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าต่างประเทศ (SES)

> เอกสารประกอบสำหรับ Dev — แนบคู่ FRD/Brief ของ F-TMP-007 · ไฟล์คู่: `FM-SAL-23_template.html` (master, fonts ฝัง) + `out/<สถานะ>.html`
> **โหมด:** Replica (แบบฟอร์มลูกค้า) · **2 หน้า** ตาม thai-doc R10 · มติทั้งหมด AI-DEFAULT รอลูกค้ายืนยัน
> ⚠ **NO-BROWSER**: เครื่อง user ไม่มี browser → ไม่ได้รัน `render_pdf.py` (ส่วน PDF ของ `render_states.py`) / `compare_original.py` บนเครื่อง — ตรวจเสริมในคอนเทนเนอร์ Claude (playwright chromium) ได้ 2 หน้าทุกสถานะ 5/5 + `out/_states_sheet.png` + `compare/compare_side.png` (ไม่ใช่ผลทางการ ต้องรันซ้ำบนเครื่องที่มี browser)

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าต่างประเทศ / Sale Admin Satisfaction Summary (Overseas) — ใบสรุปของ FM-SAL-22 (SEA · Service Experience Survey)
- **ขนาด:** A4 แนวตั้ง (engine ล็อก portrait) · ต้นฉบับ Word แนวนอน · **2 หน้า** ทุกสถานะ
- **ฟอนต์:** Sarabun (ฝัง base64) · เนื้อหา 9pt (ไม่ต่ำกว่า 8pt) · หัวเรื่อง 14pt
- **CI:** Replica — หมึกเดียวตาม profile (`profile.json`)

## 2. Field Mapping + Data contract

> สัญญาข้อมูลระหว่าง backend ↔ template (`form.tpl.html`) · ใช้ทั้ง prototype (tpl_render.js) และ server (render_doc.py)
> กติกา: ค่าแสดงทุกตัวเป็น string ที่จัดรูปแล้ว · boolean ใช้เป็นเงื่อนไขเท่านั้น · ว่าง = ""
> ตรวจ: `python scripts/parity_check.py form.tpl.html *.data.json` → IDENTICAL 5/5

| key | Source (entity.field / engine) | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| `company.name` · `company.logo` | Organization → header_snapshot (ตอนออกเลข) | `บริษัท ตัวอย่าง จำกัด` · data URI | ไม่ดึงสดหลังออกเลข |
| `doc.title` · `doc.no` · `doc.is_draft` | ค่าคงที่ · ENG-DOC-NUM (SES) · status = draft | `SES-2569-0004` | ออกเลขตอนบันทึกครั้งแรก (DEC-10) |
| `doc.form_code` · `doc.revision` | F-DOCCFG print_config | `FM-SAL-23` · `Rev.00 : 01/07/2569` | |
| `period_month_text` | SesSummary.period_month (YYYY-MM) → เดือนไทย พ.ศ. | `กันยายน 2569` | ช่องเพิ่ม (DEC-06/12) |
| `blocks[]` | 2 ชุด × 4 คอลัมน์ (รวม 8) | | คอลัมน์ที่ไม่มีลูกค้า = "" (PDF แสดงครบ 8 ทุกสถานะ) · DEC-05 |
| `blocks[].cols[].name` | SesSummaryColumn.customer_name ← Customer.name (ผ่าน SEA) | `Sample Global Trading` | ชื่อลูกค้าจริงห้ามเป็นตัวอย่าง (DEC-14) |
| `blocks[].rows[].topic` · `rows[].grp` | SalesConfig.sea_topic_groups[] + sea_topics[] (ป้ายไทยใบสรุป) | `ด้านการสื่อสารและการตอบสนอง` · `ความชัดเจนในการสื่อสาร` | 13 แถวคงที่ = 3 แถวกลุ่ม (grp=true · ช่องคะแนน merge ว่าง) + 10 หัวข้อ (DEC-13) |
| `blocks[].rows[].cells[].v` | SEA.score.qN (1–5) → ตัวเลข | `5` | snapshot ตอนดึง · ว่าง = "" · แถวกลุ่มไม่มี cells |
| `conclusion_lines[].text` | SesSummary.conclusion ตัดบรรทัด ~100 ตัวอักษร | | ขั้นต่ำ 4 บรรทัด (เส้นประตามกระดาษ) · ≤ 1,000 ตัวอักษร |
| `suggestion_lines[].text` | SesSummary.suggestion ตัดบรรทัด | | ขั้นต่ำ 4 บรรทัด · ≤ 1,000 ตัวอักษร |
| `sign_rows[].signs[]` → `role` · `name` · `position` · `date` · `decision` | ผู้สรุปผลการประเมิน (เจ้าของ) + `approval_chain` (DOA snapshot) | | จำนวนช่อง = 1 + จำนวนขั้น DOA · แถวละ ≤ 4 (sign_rows.py) · คำตัดสิน role-ceo = "รับทราบและอนุมัติ" |
| `layout.dense` | ไม่ใช้ (คอลัมน์คงที่ 8) | `false` | |
| `layout.dense_signs` | ขั้น DOA > 4 | `true` | |

## 3. กติกาค่าในตาราง (DEC-04 · DEC-12/13/14)
- คอลัมน์ = แบบประเมิน SEA ที่ "บันทึกผลแล้ว" 1 ใบ ต่อ 1 ลูกค้า ในเดือนที่เลือก · ลูกค้าซ้ำในใบเดียวกัน = บล็อก · หลายใบในเดือน = ใช้ใบล่าสุด
- ค่าช่อง = คะแนน 1–5 (1 Very Dissatisfied … 5 Very Satisfied) จาก SEA.score.q1–q10 · พิมพ์ตัวเลข · ไม่คำนวณคะแนนรวม/เฉลี่ย (กระดาษไม่มี)
- หัวข้อ q1–q10 จับคู่ตามลำดับกับ FM-SAL-22 (อังกฤษ) — พิมพ์ถ้อยคำไทยตามกระดาษ FM-SAL-23

## 4. กติกาการพิมพ์ (R9 ตารางกรอบ + R10 2 หน้า)
- หน้า 1: โลโก้ (Organization) · ชื่อเอกสาร · ประจำเดือน · ตาราง 2 ชุด (หัวตารางซ้ำทุกชุด: หัวข้อการประเมิน | ชื่อลูกค้า | ระดับความพึงพอใจ) · "มีต่อหน้าถัดไป" · footer "หน้า 1/2"
- หน้า 2 (`.page-break` ตั้งใจ ก่อนบล็อกสรุป + ลงชื่อ): หัวย่อ (ชื่อ + เลขที่ + เดือน) · สรุปผลการประเมิน · ข้อเสนอแนะ · บล็อกลงชื่อ (`.signs-block` ไม่ถูกตัด) · footer "หน้า 2/2"
- ตารางแต่ละชุด `.keep-together` · ห้ามบีบฟอนต์ < 8pt

## 5. วิธี build ใหม่
```bash
python3 render_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าต่างประเทศ" --max-pages 2   # ต้องมี browser
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o compare        # ต้องมี browser (approved.pdf)
```

## 6. Checklist ก่อนส่งมอบ
- [x] parity JS ↔ Python IDENTICAL 5/5 · ไม่มี `{{}}` หลง · ไม่มี key ขาด
- [x] ทุกสถานะ 2 หน้า — ตรวจเสริมในคอนเทนเนอร์ Claude (playwright chromium) 5/5 = 2 หน้า · **ยืนยันซ้ำบนเครื่องที่มี browser**
- [x] `out/_states_sheet.png` · `compare/compare_side.png` (ทำในคอนเทนเนอร์ · ดูแล้ว)

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `23. FM-SAL-23 สรุปแบบประเมินความพึงพอใจ  (ต่างประเทศ).docx` · Doc No.FM-SAL-23 · Rev.00 : 01/07/2569 · Word 1 หน้า แนวนอน
- Profile: form_fs 9pt · form_title_fs 14pt · logo 12mm · grid row 6mm · gap ระหว่างชุดตาราง 4mm
- ความต่างจากกระดาษ (ตั้งใจ):
  1. แนวตั้ง 2 หน้า (R10) แทนแนวนอน 1 หน้า — engine thai-doc ล็อก A4 portrait · คอลัมน์ลูกค้า 4 → 2 ชุด × 4 (รองรับ 8 ราย/ใบ · DEC-05)
  2. เพิ่มช่อง "ประจำเดือน" ใต้ชื่อเอกสาร (DEC-06/12)
  3. ชื่อลูกค้า 4 รายที่พิมพ์ตายตัวบนกระดาษ → ดึงจากแบบประเมิน SEA (DEC-14) · ตัวอย่างใช้ชื่อสมมติ
  4. ลายเซ็นย้ายเป็นแถวล่างแบบตารางกรอบ — ผู้สรุปผลการประเมิน (ซ้าย) + 1 ช่องต่อขั้น DOA (ค่าเริ่ม: ผู้รับทราบและอนุมัติ · Managing Director) · เส้นลงชื่อเท่ากันทุกช่อง (DEC-15) · ไม่พิมพ์ชื่อบุคคลจริงจากต้นฉบับ
  5. footer ซ้าย "เลขที่ … · ร่าง · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE" + "หน้า n/2"
  6. ถ้อยคำหัวข้อชิดซ้าย (กระดาษจัดกลาง) — อ่านง่ายเมื่อคอลัมน์แคบลงในแนวตั้ง
- ผล compare_original (คอนเทนเนอร์ · approved): **WARN 0.361** — อธิบายได้: ต้นฉบับแนวนอน vs ของเราแนวตั้ง 2 ชุดตาราง (เส้นแนวนอนตรงตำแหน่ง 4/17) · ภาพต้นฉบับฟอนต์ไทยไม่ขึ้น · ดูภาพวางคู่แล้ว โครงตาราง (หัวข้อ 10 ข้อ + แถวกลุ่ม 3 แถว × ลูกค้า 4 คอลัมน์ · แถว "ระดับความพึงพอใจ") ตรงกัน

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- ตาราง contract: `§2 ของไฟล์นี้`
- parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: draft (2 ลูกค้า · ยังไม่กรอกสรุป · ช่องลงชื่อผู้อนุมัติว่าง) · approved (4 ลูกค้า · ☑ รับทราบและอนุมัติ) · rejected (4 ลูกค้า 2 รายมีคะแนน 1–2 · ☑ ไม่อนุมัติ) · long-8customers (8 ลูกค้าเต็ม 2 ชุด · สรุป 12 บรรทัด · ข้อเสนอแนะ 6 บรรทัด) · approved-doa6steps (DOA 6 ขั้น → ช่องลงชื่อ 7 ช่อง 4+3 · dense_signs)

## 9. (Replica) print_config
```json
{
  "doc_type": "SES",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-SAL-23",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "paper_original": "A4-landscape (ต้นฉบับ Word) — engine thai-doc ล็อก A4 แนวตั้ง → แบ่งคอลัมน์ลูกค้าเป็น 2 ชุด × 4",
  "pages": 2,
  "page_break": "ก่อนบล็อก 'สรุปผลการประเมิน' — หน้า 1 = หัว + ประจำเดือน + ตารางหัวข้อ×ลูกค้า 2 ชุด (หัวตารางซ้ำทุกชุด) · หน้า 2 = สรุปผลการประเมิน + ข้อเสนอแนะ + บล็อกลงชื่อ",
  "min_rows": 8,
  "max_rows": 8,
  "cols_per_block": 4,
  "text_min_lines": 4,
  "text_max_chars": 1000,
  "dense_when_rows_over": 99,
  "repeat_groups": {
    "customers": {
      "min_rows": 8,
      "max_rows": 8,
      "orientation": "columns",
      "print_columns": 8
    },
    "rows[].topic": {
      "rows_from": "SalesConfig.sea_topic_groups[] + sea_topics[] (3 กลุ่ม · 10 ข้อตามกระดาษ)"
    }
  },
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    {
      "box": "requester",
      "label": "ผู้สรุปผลการประเมิน",
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
      "role-ceo": {
        "approve": "รับทราบและอนุมัติ",
        "reject": "ไม่อนุมัติ"
      }
    }
  },
  "config_reads": {
    "rows[].topic": "SalesConfig.sea_topic_groups[] + sea_topics[] (ป้ายไทยใบสรุป)",
    "cells[].v": "SalesConfig.sea_scale[] (weight 1–5 จาก SEA.score.qN · พิมพ์ตัวเลข)"
  },
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc No.{form_code} · {revision} · หน้า n/2",
  "sign_layout": {
    "source": "approval_chain snapshot (ผู้สรุป + จำนวนขั้นตามที่ตั้งใน DOA)",
    "max_per_row": 4,
    "split": "even",
    "dense_when_steps_over": 4,
    "keep_together": true
  }
}
```
