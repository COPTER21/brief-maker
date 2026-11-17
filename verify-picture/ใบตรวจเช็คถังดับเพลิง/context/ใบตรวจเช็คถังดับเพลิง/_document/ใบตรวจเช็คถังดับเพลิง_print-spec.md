# PRINT SPEC — ใบตรวจเช็คถังดับเพลิง (FEC)

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD/Brief ของ F-TMP-001
> ไฟล์คู่: `ใบตรวจเช็คถังดับเพลิง_template.html` (master, fonts ฝัง) · `out/*.html` ทุกสถานะ
> **โหมด:** Replica (แบบฟอร์มลูกค้า FM-WHS-03) · **[NO-BROWSER]** รอบนี้ไม่ได้ render PDF/PNG — ต้องรันรอบเต็มบนเครื่องที่มี browser

## 1. สรุป
- **ประเภทเอกสาร:** ใบตรวจเช็คถังดับเพลิง / Fire Extinguisher Inspection Card
- **ขนาด:** A4 แนวตั้ง · 1 หน้า (pages: 1) · ฟอนต์ Sarabun ฝังใน HTML
- **Replica:** หมึกเดียว + แถบชื่อเอกสารสีส้มอ่อนตามต้นฉบับ (token `form_grid_head_bg`)

## 2. Field Mapping
| ช่องในเอกสาร | Source | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| โลโก้ + ชื่อ/ที่อยู่บริษัท | Organization snapshot | — | ✓ | |
| สถานที่ | WarehouseLocation.name | ข้อความ | ✓ | |
| วันที่ (ต่อแถว) | fec_check.check_date | d MMM yy (พ.ศ.) | ✓ | |
| มาตรวัด · ซีล/สลัก · สายฉีด · สภาพถัง | fec_check.* | `/` ปกติ · `x` ผิดปกติ | ✓ | |
| ผู้ตรวจ | Employee.full_name (ผู้บันทึก) | ข้อความ | ✓ | ไม่มีลายมือชื่อ (DEC-07) |
| เลขที่ / Doc. No. / Rev. | ENG-DOC-NUM · print_config | — | ✓ | footer |

## 3. กติกาคำนวณ
- ไม่มีสูตร · `layout.dense = checks.length > 12`

## 4. กติกาการพิมพ์
- ตารางกรอบ R9 · `thead` ซ้ำทุกหน้า · แถวไม่ถูกตัดกลาง · ไม่มีบล็อกลงชื่อ
- 24 แถว (dense 6mm) ประเมินยังพอดี 1 หน้า (≈ หัว 70mm + 24×6mm + footer) — ยืนยันด้วย render_states บนเครื่องที่มี browser
- เกิน ~30 แถว → แนะนำพิมพ์ตามช่วงปี (1 ใบต่อสถานที่ต่อปี ≈ 12 แถว ตามกระดาษ) — บันทึกเป็นข้อเสนอใน BRD

## 5. วิธี build ใหม่
```bash
python3 render_data.py   # สร้าง *.data.json ทุกสถานะ (ข้อมูลสมมติ)
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "ใบตรวจเช็คถังดับเพลิง" --max-pages 1
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/full-12rows.pdf -o compare
```

## 6. Checklist ก่อนส่งมอบ
- [x] parity IDENTICAL 5/5 · ไม่มี {{}} หลง · ไม่มี key หาย
- [ ] A4 1 หน้าทุกสถานะ — [NO-BROWSER] รอยืนยัน
- [ ] compare_original — [NO-BROWSER] รอยืนยัน

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `3. FM-WHS-03 ใบตรวจเช็คถังดับเพลิง.xlsx` · Doc No. FM-WHS-03 · Rev.00 :01/07/2569
- Profile token ที่ต่าง: form_fs 10pt · form_logo_h 12mm · form_logo_align left · form_grid_head_bg #F4AC84 · form_grid_row_h 8mm / dense 6mm · form_grid_gap 6px · form_row_gap 6px
- ความต่างจากกระดาษ (ตั้งใจ): 1 ใบ = 1 สถานที่ (ต้นฉบับวาง 2 การ์ดซ้าย-ขวา ล้น A4 · DEC-11) · แก้ "ผู้จำหนาย" → "ผู้จำหน่าย" (DEC-12) · footer ซ้ายเลขที่เอกสารระบบ · Doc No./Rev. รวมในบรรทัด footer เดียว
- compare_original: **[NO-BROWSER] ข้าม** — ไม่มี PDF ของแบบพิมพ์ระบบให้เทียบ

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- contract: ภาคผนวกท้ายไฟล์นี้
- parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: active-3rows · full-12rows · abnormal (มี x 2 แถว) · long-24rows (dense) · cancelled → HTML ครบ · จำนวนหน้า: รอ render (NO-BROWSER)
- ไม่มีสถานะร่าง/อนุมัติ/ไม่อนุมัติ/DOA หลายขั้น เพราะเอกสารไม่มีการอนุมัติ (DEC-03) และไม่มีช่องลงชื่อ

## 9. (Replica) print_config
```json
{
  "doc_type": "FEC",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-WHS-03",
  "revision": "Rev.00 :01/07/2569",
  "paper": "A4-portrait",
  "pages": 1,
  "min_rows": 12,
  "dense_when_rows_over": 12,
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [],
  "decision_words": { "default": {}, "by_role": {} },
  "row_marks": { "normal": "/", "abnormal": "x" },
  "config_reads": {
    "location": "WarehouseLocation.name (จุดติดตั้งถังดับเพลิง)",
    "company": "Company Master (Organization snapshot ตอนออกเลข)"
  },
  "footer_left": "เลขที่ {doc.no} · (ยกเลิก) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc. No. : {form_code} · {revision}",
  "sign_layout": { "source": "ไม่มีช่องลงชื่อ (DEC-03 ไม่มีอนุมัติ · DEC-07) — ผู้ตรวจแสดงเป็นข้อความต่อแถว", "max_per_row": 4, "split": "even", "dense_when_steps_over": 4, "keep_together": true }
}
```

---

## ภาคผนวก — DATA CONTRACT — ใบตรวจเช็คถังดับเพลิง (FEC)

> สัญญาข้อมูลระหว่าง backend ↔ template (`form.tpl.html`) · ใช้ทั้ง prototype (tpl_render.js) และ server (render_doc.py)
> กติกา: ค่าแสดงทุกตัวเป็น string ที่จัดรูปแล้ว · boolean ใช้เป็นเงื่อนไขเท่านั้น · เครื่องหมาย = "/" หรือ "x" (จาก print_config.row_marks) · ว่าง = ""
> ตรวจ: `python scripts/parity_check.py form.tpl.html *.data.json` → IDENTICAL 5/5

| key | Source (entity.field / engine) | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| `company.name` · `company.address_line1` · `company.address_line2` · `company.logo` | Organization (Company Master) → header_snapshot ตอนออกเลข | `บริษัท ตัวอย่าง จำกัด (มหาชน)` · data URI | ไม่ดึงสดหลังออกเลข |
| `doc.title` | ค่าคงที่ | `ใบตรวจเช็คถังดับเพลิง` | |
| `doc.no` | ENG-DOC-NUM (ออกตอนบันทึกครั้งแรก · DEC-09) | `FEC-2569-0001` | |
| `doc.is_cancelled` | status = cancelled | `false` | เงื่อนไข footer "· ยกเลิก" |
| `doc.form_code` · `doc.revision` | F-DOCCFG print_config | `FM-WHS-03` · `Rev.00 :01/07/2569` | |
| `location` | WarehouseLocation.name (จุดติดตั้ง) | `โซน A1 คลังสินค้า` | 1 ใบ = 1 สถานที่ (DEC-11) |
| `checks[].check_date` | fec_check.check_date | `5 ม.ค. 69` | วันที่ไทยย่อ พ.ศ. 2 หลัก ตามกระดาษ |
| `checks[].gauge` · `seal_pin` · `hose` · `body` | fec_check.* enum normal/abnormal → `/` / `x` | `/` | DEC-04 |
| `checks[].inspector` | Employee.full_name ของผู้บันทึกแถว (F-EMP-001) | `สมชาย ตรวจดี` (สมมติ) | PDPA — ห้ามใช้ชื่อจริงลูกค้าเป็นตัวอย่าง |
| `layout.dense` | checks.length > 12 | `true` | แถวเตี้ยลง 8mm → 6mm |

เติมแถวว่างจนครบ `min_rows = 12` ใน data (template ไม่นับ)
