# PRINT SPEC — หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade (CSM)

> เอกสารประกอบสำหรับ Dev — แนบคู่ FRD/Brief ของ F-TMP-002 · ไฟล์คู่: `FM-SAL-11_template.html` (master, fonts ฝัง) + `out/<สถานะ>.html`
> **โหมด:** Replica (แบบฟอร์มลูกค้า) · **2 หน้า** ตาม thai-doc R10 · มติทั้งหมด AI-DEFAULT รอลูกค้ายืนยัน
> ⚠ **NO-BROWSER**: เครื่องที่ทำไม่มี browser → ยังไม่ได้ render PDF (`render_pdf.py` / PDF ใน `render_states.py`) และไม่ได้รัน `compare_original.py` — ต้องรันรอบเต็มบนเครื่องที่มี browser

## 1. สรุป
- **ประเภทเอกสาร:** หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade / GT Customer Satisfaction Summary (Monthly)
- **ขนาด:** A4 แนวตั้ง (210×297mm), ขอบ 14mm · **2 หน้า** ทุกสถานะ
- **ฟอนต์:** Sarabun (ฝัง base64) · ขนาดเนื้อหา 9pt (ไม่ต่ำกว่า 8pt)
- **CI:** Replica — หมึกเดียวตาม profile (`profile.json`)

## 2. Field Mapping + Data contract

> สัญญาข้อมูลระหว่าง backend ↔ template (`form.tpl.html`) · ใช้ทั้ง prototype (tpl_render.js) และ server (render_doc.py)
> กติกา: ค่าแสดงทุกตัวเป็น string ที่จัดรูปแล้ว · boolean ใช้เป็นเงื่อนไขเท่านั้น · ว่าง = "" · ไม่มี {} ว่าง
> ตรวจ: `python scripts/parity_check.py form.tpl.html *.data.json` → IDENTICAL 5/5 · มติ AI-DEFAULT (DECISIONS.lock) รอลูกค้ายืนยัน

| key | Source (entity.field / engine) | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| `company.name` · `company.logo` | Organization → header_snapshot (ตอนออกเลข) | `บริษัท ตัวอย่าง จำกัด` · data URI | ไม่ดึงสดหลังออกเลข |
| `doc.title` · `doc.no` · `doc.is_draft` | ค่าคงที่ · ENG-DOC-NUM (CSM) · status = draft | `CSM-2569-0009` | ออกเลขตอนบันทึกครั้งแรก (DEC-13) |
| `doc.form_code` · `doc.revision` | F-DOCCFG print_config | `FM-SAL-11` · `Rev.00: 01/07/2569` | |
| `period_month` | CsmSummary.period_month (YYYY-MM) | `กันยายน 2569` | เดือนเต็มภาษาไทย พ.ศ. |
| `sections[]` | SalesConfig.csat_topics[] จัดกลุ่มตามด้าน (3 ด้าน) | | แถว = หัวข้อใน config (4/4/8) · ผู้ใช้ไม่เพิ่ม/ลบแถว |
| `sections[].heading` · `col_title` | SalesConfig.csat_topics[].section | `1) ด้านคุณภาพสินค้า/บริการ` | |
| `sections[].levels[].label` | SalesConfig.csat_scale[] | `มากที่สุด` … `ต้องปรับปรุง` | น้ำหนัก 5–1 ไม่พิมพ์ |
| `sections[].items[].topic` | SalesConfig.csat_topics[].text | `1. คุณภาพของสินค้าโดยรวม` | snapshot ตอนออกเลข |
| `sections[].items[].counts[].v` | CsmSummaryLine.c5…c1 (จำนวนเต็ม ≥ 0) | `6` | ร่างที่ยังไม่กรอก = "" |
| `sections[].items[].total` | computed Σ c5…c1 | `12` | |
| `sections[].items[].pct_cell` | computed — มีเฉพาะแถวแรก `{rowspan, pct}` · แถวอื่น null | `{"rowspan":"5","pct":"86.67"}` | rowspan = จำนวนหัวข้อ + 1 (รวมแถว "รวม") |
| `sections[].sums[].v` · `sum_total` | computed Σ ทุกแถว ต่อคอลัมน์ (ครบ 5 คอลัมน์) | `20` | DEC-16/17 |
| `overall_pct` | computed Σw ÷ (5 × Σรวม) × 100 · 2 ตำแหน่ง ROUND_HALF_UP | `85.83` | รวม = 0 → `—` (DEC-18/19) |
| `overall_level` | computed จาก SalesConfig.csat_bands | `ลูกค้ามีความพึงพอใจสูง` | |
| `policy.min_orders` | SalesConfig.csat_min_orders_per_month | `3` | |
| `policy.bands[]` → `range` · `text` | SalesConfig.csat_bands[] | `80% – 100%` · `ลูกค้ามีความพึงพอใจสูง` | |
| `customers[]` → `name` · `order_count` | Customer.name · COUNT(SaleOrder ในเดือน) | `ร้านค้าตัวอย่าง GT 01` · `5` | เติมแถวว่างจนครบ 14 (min_rows) · ชื่อลูกค้า = ข้อมูลส่วนบุคคลได้ |
| `sign_rows[].signs[]` → `role` · `name` · `date` · `decision` | ผู้จัดทำ (Sales Manager) + `approval_chain` (DOA snapshot) | | จำนวนช่อง = 1 + จำนวนขั้น DOA · แถวละ ≤ 4 (sign_rows.py) |
| `layout.dense` | customers.length > 14 | `true` | |
| `layout.dense_signs` | ขั้น DOA > 4 | `true` | |


## 3. กติกาคำนวณ (DEC-04 · DEC-16–19)
- รวมต่อแถว = c5 + c4 + c3 + c2 + c1 · แถว "รวม" = Σ ต่อคอลัมน์ ครบ 5 คอลัมน์ (ต้นฉบับขาด)
- % ต่อด้าน = (5·c5 + 4·c4 + 3·c3 + 2·c2 + 1·c1) ÷ (5 × รวม) × 100 · 2 ตำแหน่ง ROUND_HALF_UP · รวม = 0 → "—"
- % โดยรวม = Σ คะแนนถ่วงน้ำหนัก 3 ด้าน ÷ (5 × Σ รวม 3 ด้าน) × 100 → ข้อความแปลผลตาม SalesConfig.csat_bands (≥80 · 60–79.99 · <60)

## 4. กติกาการพิมพ์ (R9 ตารางกรอบ + R10 2 หน้า)
- หน้า 1: โลโก้ (Organization) · ชื่อเอกสาร · ประจำเดือน · ตาราง 3 ด้าน (หัวตาราง 2 แถว: คะแนนการประเมิน 5 ระดับ · รวม · %) · "มีต่อหน้าถัดไป" · footer "หน้า 1/2"
- หน้า 2 (`.page-break` ตั้งใจ): หัวย่อ (ชื่อ + เลขที่ + เดือน) · เกณฑ์ ≥ 3 ครั้ง/เดือน · สรุปผลโดยรวม · การแปลผล CSAT · ตารางรายชื่อลูกค้า (หัวตารางซ้ำ · ≥ 14 แถว) · บล็อกลงชื่อทั้งก้อน (`.signs-block`) · footer "หน้า 2/2"
- ตารางคะแนนแต่ละด้าน `.keep-together` · แถวไม่ถูกตัดกลาง · ห้ามบีบฟอนต์ < 8pt
- คอลัมน์ % ผสานแนวตั้งตลอดตาราง (rowspan จาก data) ตามกระดาษ

## 5. วิธี build ใหม่
```bash
python3 render_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade" --max-pages 2   # ต้องมี browser
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare --region 0:0.55        # ต้องมี browser (approved.pdf)
```

## 6. Checklist ก่อนส่งมอบ
- [x] parity JS ↔ Python IDENTICAL 5/5 · ไม่มี `{{}}` หลง (render_doc --strict 5/5)
- [ ] ทุกสถานะ 2 หน้า (ประเมินจากความสูง: หน้า 1 ≈ 245mm · หน้า 2 ≤ 215mm จาก 269mm) — **ยืนยันด้วย render_states บนเครื่องที่มี browser**
- [ ] ภาพ `_states_sheet.png` · `compare_side.png` — NO-BROWSER ยังไม่มี

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `11. FM-SAL-11 แบบสรุปหัวข้อการประเมินความพึงพอใจ สำหรับ General Trade.xlsx` (ชีตชื่อ FM-SAL-10) · Doc.No.FM-SAL-11 · Rev.00: 01/07/2569 · 1 หน้า (Excel ย่อพอดีหน้า)
- Profile: form_fs 9pt · form_title_fs 15pt · form_logo_h 11mm · grid row 6.6mm (dense 5.2mm) · gap ปรับกระชับ
- ความต่างจากกระดาษ (ตั้งใจ):
  1. แบ่งเป็น 2 หน้า (R10) — ต้นฉบับย่อทั้งชีตลง 1 หน้า ตัวอักษรเล็กกว่า 8pt เมื่อพิมพ์จริง
  2. ลายเซ็นย้ายเป็นแถวล่างแบบตารางกรอบ — ผู้จัดทำ (Sales Manager) + 1 ช่องต่อขั้น DOA (ค่าเริ่ม: ผู้อำนวยการสายงานการขาย) · ข้อความ "ส่งในระบบ/พิจารณาในระบบ" แทนลายมือ (DEC-10)
  3. หัวตารางสีพื้น (เขียว/ชมพู/ฟ้า) → เทาเดียวตาม replica หมึกเดียว · ข้อความแปลผลสีเขียว → หมึกเดียว
  4. แถว "รวม" มีครบ 5 คอลัมน์ · % คำนวณจริง · "85.83 %" คำนวณจากตาราง (DEC-16–19)
  5. ตารางรายชื่อลูกค้ากว้างเต็มหน้า (ต้นฉบับกว้าง ~ 2/3)
  6. footer ซ้าย "เลขที่ … · ร่าง · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE" + "หน้า n/2"
- ผล compare_original: **ยังไม่ได้รัน (NO-BROWSER)** — แนะนำ `--region 0:0.55` (ส่วนตาราง 3 ด้าน)

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- ตาราง contract: `§2 ของไฟล์นี้`
- parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: draft (ยังไม่กรอกคะแนน · 5 ลูกค้า) · approved (85.83% สูง · 12 ลูกค้า) · rejected (57.08% อาจไม่พึงพอใจ · ☑ ไม่อนุมัติ) · long-22customers (22 แถว dense) · approved-doa6steps (7 ช่อง 4+3) → เป้า 2 หน้าทุกสถานะ (ยืนยันเมื่อมี browser)

## 9. (Replica) print_config
```json
{
  "doc_type": "CSM",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-SAL-11",
  "revision": "Rev.00: 01/07/2569",
  "paper": "A4-portrait",
  "pages": 2,
  "page_break": "ก่อนบล็อก 'ประเมินจากลูกค้าที่มีการสั่งซื้อ…' — หน้า 1 = หัว + ประจำเดือน + ตาราง 3 ด้าน · หน้า 2 = สรุปผล + การแปลผล + รายชื่อลูกค้า + บล็อกลงชื่อ",
  "min_rows": 14,
  "dense_when_rows_over": 14,
  "repeat_groups": { "customers": { "min_rows": 14, "max_rows": null }, "sections[].items": { "rows_from": "SalesConfig.csat_topics[] (ตามกระดาษ 4/4/8)" } },
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    { "box": "requester", "label": "Sales Manager", "show_date": true },
    { "box": "doa_step:*", "label": "from_doa_step", "show_decision": true, "show_date": true }
  ],
  "decision_words": {
    "default": { "approve": "อนุมัติ", "reject": "ไม่อนุมัติ" },
    "by_role": {}
  },
  "config_reads": {
    "policy.min_orders": "SalesConfig.csat_min_orders_per_month",
    "policy.bands": "SalesConfig.csat_bands[]",
    "sections[].levels": "SalesConfig.csat_scale[] (label + weight)",
    "sections[].items[].topic": "SalesConfig.csat_topics[]"
  },
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc.No.{form_code} · {revision} · หน้า n/2",
  "sign_layout": {
    "source": "approval_chain snapshot (ผู้ขอ + จำนวนขั้นตามที่ตั้งใน DOA)",
    "max_per_row": 4,
    "split": "even",
    "dense_when_steps_over": 4,
    "keep_together": true
  }
}

```
