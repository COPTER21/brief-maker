# PRINT SPEC — สรุปข้อมูลประเมินความพึงพอใจลูกค้า กลุ่ม MT (MTS)

> เอกสารประกอบสำหรับ Dev — แนบคู่ FRD/Brief ของ F-TMP-008 · ไฟล์คู่: `FM-SAL-07_template.html` (master, fonts ฝัง) + `out/<สถานะ>.html`
> **โหมด:** Replica (แบบฟอร์มลูกค้า) · **2 หน้า** ตาม thai-doc R10 · มติทั้งหมด AI-DEFAULT รอลูกค้ายืนยัน
> ⚠ **NO-BROWSER**: เครื่องที่ทำไม่มี browser → ยังไม่ได้ render PDF (`render_pdf.py` / PDF ใน `render_states.py`) และไม่ได้รัน `compare_original.py` — ต้องรันรอบเต็มบนเครื่องที่มี browser

## 1. สรุป
- **ประเภทเอกสาร:** สรุปข้อมูลประเมินความพึงพอใจลูกค้า กลุ่ม MT / MT Customer Satisfaction Summary (ต่อครั้ง)
- **ขนาด:** A4 แนวตั้ง (210×297mm), ขอบ 14mm · **2 หน้า** ทุกสถานะ (ต้นฉบับ A4 แนวนอน ย่อพอดี 1 หน้า — thai-doc build_html รองรับแนวตั้งเท่านั้น)
- **ฟอนต์:** Sarabun (ฝัง base64) · ขนาดเนื้อหา 8.5pt (ไม่ต่ำกว่า 8pt) · หัวเรื่อง 14pt
- **CI:** Replica — หมึกเดียวตาม profile (`profile.json`)

## 2. Field Mapping + Data contract

> สัญญาข้อมูลระหว่าง backend ↔ template (`form.tpl.html`) · ใช้ทั้ง prototype (tpl_render.js) และ server (render_doc.py)
> กติกา: ค่าแสดงทุกตัวเป็น string ที่จัดรูปแล้ว · boolean ใช้เป็นเงื่อนไขเท่านั้น · ว่าง = "" · ไม่มี {} ว่าง
> ตรวจ: `python scripts/parity_check.py form.tpl.html *.data.json` → IDENTICAL 5/5

| key | Source (entity.field / engine) | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| `doc.title` · `doc.no` · `doc.is_draft` · `doc.is_cancelled` | ค่าคงที่ · ENG-DOC-NUM (MTS) · status | `MTS-2569-0002` | ออกเลขตอนบันทึกครั้งแรก (DEC-11) |
| `doc.form_code` · `doc.revision` | F-DOCCFG print_config | `FM-SAL-07` · `Rev.00: 01/07/2569` | |
| `round_no` | MtsSummary.round_no | `1` | ท้ายหัวเรื่อง "ครั้งที่" |
| `blocks[]` | แบ่ง channels_snapshot เป็นช่วงละ 8 (print_config.channels_per_block) | | ช่วงสุดท้ายเติมคอลัมน์ว่างให้ครบ 8 |
| `blocks[].channels[].name` | MtsSummary.channels_snapshot[].name (SalesConfig.mt_channels) | `บิ๊กซี` | คอลัมน์เติม = "" |
| `blocks[].rows[].topic` · `max` | MtsSummary.criteria_snapshot[] (SalesConfig.mt_csat_criteria) | `คุณภาพของสินค้า/บริการ` · `5` | 9 แถว |
| `blocks[].rows[].scores[].v` | MtsScore.score (criterion × channel) | `5` | ไม่ได้กรอก = "" |
| `blocks[].max_total` | computed Σ max | `45` | |
| `blocks[].totals[].v` | computed Σ score ต่อช่องทาง | `39` | ไม่ได้ประเมิน = "" |
| `blocks[].pcts[].v` | computed total ÷ max_total × 100 · 2 ตำแหน่ง ROUND_HALF_UP + "%" | `86.67%` | ไม่ครบทุกหัวข้อ = `—` |
| `blocks[].statuses[].v` | computed จาก SalesConfig.mt_csat_bands (≥95 / 80–<95 / <80) | `ต่ำกว่ามาตรฐาน` | ใช้ค่า % ก่อนปัด |
| `policy.std_pct` · `policy.low_pct` | SalesConfig.mt_csat_standard_pct · mt_csat_low_pct | `95` · `80` | |
| `legend[]` → `label` · `range` | SalesConfig.mt_csat_bands[] | `ผ่านมาตรฐาน` · `% ตั้งแต่ 95 ขึ้นไป` | แทนคำอธิบายสี (หมึกเดียว) |
| `summary.groups[]` → `label` · `channels` · `note` · `is_alert` | computed รายชื่อตามสถานะ · MtsSummary.pass_note/below_note/far_note | `makro, Foodland, …` | ไม่มีช่องทาง = `—` · is_alert = กลุ่มต่ำกว่า 80% (ตัวหนา) |
| `recommendations[]` → `no` · `text` | MtsRecommendation.text (ลำดับ) | `1.` · `วิเคราะห์จุดอ่อน…` | เติมแถวว่างจนครบ 4 (min_rows) |
| `sign_rows[].signs[]` → `role` · `name` · `position` · `date` | ผู้สรุป = ผู้สร้างเอกสาร (Employee) · date = "ยืนยันสรุปในระบบ …" | `ผู้สรุปการประเมิน` · `Sales Manager` | 1 ช่อง (ไม่มี DOA — DEC-03) |
| `assessment_date` · `summary_date` | MtsSummary.assessment_date · summary_date | `15 กันยายน 2569` | วันที่เต็ม พ.ศ. · ร่างที่ยังไม่กรอก = "" |
| `layout.dense` | recommendations.length > 8 | `true` | |

## 3. กติกาคำนวณ (DEC-04 · DEC-13–17)
- รวมคะแนนต่อช่องทาง = Σ คะแนน 9 หัวข้อ (ต้นฉบับไม่มีสูตร) · รวมคะแนนเต็ม = Σ คะแนนเต็ม (45)
- % = รวมคะแนน ÷ รวมคะแนนเต็ม × 100 (ตามสูตรต้นฉบับ =D12/C12) · 2 ตำแหน่ง ROUND_HALF_UP · ช่องทางที่ยังกรอกไม่ครบ/ไม่ได้ประเมิน → "—"
- สถานะ: ≥ 95 ผ่านมาตรฐาน · 80 – < 95 ต่ำกว่ามาตรฐาน · < 80 ค่อนข้างต่ำกว่ามาตรฐาน · รายชื่อในภาพรวมโดยสรุปสร้างจากสถานะ

## 4. กติกาการพิมพ์ (R9 ตารางกรอบ + R10 2 หน้า)
- หน้า 1: หัวเรื่อง + ครั้งที่ · ตารางคะแนน 2 ช่วง (ช่องทาง 1–8 · 9–15 + คอลัมน์ว่าง 1) แต่ละช่วงมีหัวตาราง "หัวข้อประเมิน · คะแนน (1-5) · ชื่อช่องทาง" · แถวรวม · แถว 100%/% · แถวผลเทียบมาตรฐาน · มาตรฐานที่กำหนด 95% · คำอธิบายผล · "มีต่อหน้าถัดไป" · footer "หน้า 1/2"
- หน้า 2 (`.page-break` ตั้งใจ): หัวย่อ · ภาพรวมโดยสรุป 3 กลุ่ม · ข้อเสนอแนะ (≥ 4 บรรทัด) · บล็อกผู้สรุป (signs-block ไม่ถูกตัด) · เอกสารประเมิน วันที่ / สรุปข้อมูล วันที่ · footer "หน้า 2/2"
- ตารางแต่ละช่วง `.keep-together` · ห้ามบีบฟอนต์ < 8pt

## 5. วิธี build ใหม่
```bash
python3 render_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "สรุปข้อมูลประเมินความพึงพอใจลูกค้า กลุ่ม MT" --max-pages 2   # ต้องมี browser
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/final.pdf -o out/compare --region 0:0.40       # ต้องมี browser
```

## 6. Checklist ก่อนส่งมอบ
- [x] parity JS ↔ Python IDENTICAL 5/5 · ไม่มี `{{}}` หลง (render_doc --strict 5/5)
- [ ] ทุกสถานะ 2 หน้า (ประเมินความสูง: หน้า 1 ≈ 220mm · หน้า 2 ≤ 200mm จาก 269mm) — **ยืนยันด้วย render_states บนเครื่องที่มี browser**
- [ ] ภาพ `_states_sheet.png` · `compare_side.png` — NO-BROWSER ยังไม่มี

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `7. FM-SAL-07 แบบฟอร์มรายงานสรุปข้อมูล แบบประเมิณความพึงพอใจของลูกค้า MT.xlsx` (ชีต "สรุปการประเมิณครั้งที่1") · Doc.No.FM-SAL-07 · Rev.00: 01/07/2569 · A4 แนวนอน 1 หน้า
- ความต่างจากกระดาษ (ตั้งใจ):
  1. A4 แนวตั้ง 2 หน้า (R10) และตาราง 15 ช่องทางแบ่ง 2 ช่วง ช่วงละ 8 — ตัวพิมพ์ไม่ต่ำกว่า 8pt (ต้นฉบับย่อทั้งชีตแนวนอน)
  2. สีเซลล์ % (เขียว/เหลือง/แดง) → ข้อความผลเทียบมาตรฐานในตาราง + คำอธิบายผลเป็นข้อความ (หมึกเดียว) · คำนวณจาก % ไม่ระบายเอง (DEC-14/15)
  3. รายชื่อช่องทางในภาพรวมโดยสรุปสร้างจากสถานะ · ข้อความแนะนำกลุ่ม "ต่ำกว่า 80%" ตัวหนา (ต้นฉบับตัวหนาสีแดง)
  4. ผู้สรุป: กล่องลงชื่อแถวล่าง (ชื่อ + ตำแหน่ง + "ยืนยันสรุปในระบบ วันที่ เวลา") แทนชื่อพิมพ์ · ไม่มีช่องผู้อนุมัติ (ตามกระดาษ)
  5. แก้คำสะกด "ประเมิณ/ลุกค้า" · footer ซ้าย "เลขที่ … · ร่าง/ยกเลิก · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE" + "หน้า n/2"
- ผล compare_original: **ยังไม่ได้รัน (NO-BROWSER)** — แนะนำ `--region 0:0.40` (ส่วนตาราง) และคาดว่าเป็น WARN เพราะเปลี่ยนแนวกระดาษ

## 8. (Replica) สถานะที่ทดสอบ
- parity JS ↔ Python: IDENTICAL 5/5
- draft (กรอก 1 ช่องทางครบ + 1 ช่องทางบางส่วน → % "—") · final (15 ช่องทาง 3 กลุ่ม) · final-allpass (ทุกช่องทางผ่าน · กลุ่มอื่น "—") · cancelled (ประเมิน 8 ช่องทาง · footer "ยกเลิก") · long-12recs (ข้อเสนอแนะ 12 ข้อ dense + ข้อความแนะนำยาว) → เป้า 2 หน้าทุกสถานะ (ยืนยันบนเครื่องที่มี browser)
- ไม่มีสถานะ ไม่อนุมัติ / DOA 6 ขั้น — เอกสารนี้ไม่มีการอนุมัติ (DEC-03)

## 9. (Replica) print_config
```json
{
  "doc_type": "MTS",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-SAL-07",
  "revision": "Rev.00: 01/07/2569",
  "paper": "A4-portrait",
  "pages": 2,
  "page_break": "ก่อนบล็อก 'ภาพรวมโดยสรุป' — หน้า 1 = หัวเรื่อง + ครั้งที่ + ตารางคะแนน (แบ่ง 2 ช่วง ช่วงละ 8 ช่องทาง) + มาตรฐาน 95% + คำอธิบายผล · หน้า 2 = ภาพรวมโดยสรุป + ข้อเสนอแนะ + บล็อกผู้สรุป + วันที่",
  "min_rows": 4,
  "dense_when_rows_over": 8,
  "channels_per_block": 8,
  "repeat_groups": { "recommendations": { "min_rows": 4, "max_rows": null }, "blocks[].rows": { "rows_from": "SalesConfig.mt_csat_criteria[] (ตามกระดาษ 9 หัวข้อ)" }, "blocks[].channels": { "cols_from": "SalesConfig.mt_channels[] (ตามกระดาษ 15 ช่องทาง) แบ่งช่วงละ 8 คอลัมน์ เติมคอลัมน์ว่างให้ครบช่วง" } },
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    { "box": "requester", "label": "ผู้สรุปการประเมิน", "show_date": true }
  ],
  "decision_words": {
    "default": { "approve": "อนุมัติ", "reject": "ไม่อนุมัติ" },
    "by_role": {}
  },
  "config_reads": {
    "policy.std_pct": "SalesConfig.mt_csat_standard_pct",
    "policy.low_pct": "SalesConfig.mt_csat_low_pct",
    "legend[]": "SalesConfig.mt_csat_bands[] (label)",
    "blocks[].rows[].topic · max": "SalesConfig.mt_csat_criteria[] (text + max_score)",
    "blocks[].channels[].name": "SalesConfig.mt_channels[]",
    "summary.groups[].note (ค่าเริ่ม)": "SalesConfig.mt_csat_bands[].default_note"
  },
  "footer_left": "เลขที่ {doc.no} · (ร่าง/ยกเลิก) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc.No.{form_code} · {revision} · หน้า n/2",
  "sign_layout": {
    "source": "ผู้สรุป (ผู้สร้างเอกสาร) 1 ช่อง — ไม่มีสายอนุมัติ (DEC-03)",
    "max_per_row": 4,
    "split": "even",
    "dense_when_steps_over": 4,
    "keep_together": true
  }
}
```
