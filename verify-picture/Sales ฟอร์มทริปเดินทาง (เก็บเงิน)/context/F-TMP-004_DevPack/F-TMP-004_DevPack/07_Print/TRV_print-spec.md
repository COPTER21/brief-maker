# PRINT SPEC — ใบเดินทาง : เขตการขาย General Trade (TRV)

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD/Brief ของ F-TMP-004
> ไฟล์คู่: `TRV_template.html` (master, fonts ฝัง) + `out/<state>.html` (ตัวอย่างแต่ละสถานะ)
> **โหมด: Replica** (แบบฟอร์มลูกค้า) — กรอก §7–§9 ครบ

## 1. สรุป
- **ประเภทเอกสาร:** ใบเดินทาง เขตการขาย General Trade (เก็บเงิน) / Sales Territory Travel Sheet
- **ขนาด:** **A4 แนวนอน (297×210mm) ขอบ 6mm — ตรงต้นฉบับ** (แก้ 2026-10-10 · เดิมเคยทำแนวตั้งแล้วเละ — ดู §7)
- **ฟอนต์:** Sarabun (ฝัง base64)
- **CI:** Replica = หมึกเดียวตาม profile ลูกค้า (ไม่ใช้สี CI ของ CUBE ในเนื้อฟอร์ม)
- **Renderer:** Playwright/Chromium → `print_background`, `prefer_css_page_size`
- **บล็อก:** R1 โลโก้ซ้าย + R2 ชื่อเอกสาร 2 บรรทัด (บรรทัดเดียวกันแบบกระดาษ) · กล่อง TO/CC ช่องเติมเส้น (ไม่ใช่ตาราง) · **R9 ตารางกรอบ 21 คอลัมน์ (รวมคอลัมน์ว่าง B, E ตามกระดาษ) กว้างตามสัดส่วน xlsx** · B6 sign_rows (แถวละ ≤7 ในแนวนอน) · B7 footer

## 2. Field Mapping
ดูตารางเต็มใน `TRV_data-contract.md` (38 ช่องตาม FORM_SPEC: หัวเอกสาร 6 · แถวซ้ำ 19 ต่อแถว · รวมยอด 13)

| ช่องในเอกสาร | Source | Format | บังคับ |
|---|---|---|---|
| เลขที่เอกสาร (footer) | ENG-DOC-NUM · ออกตอนบันทึกครั้งแรก (DEC-10) | `TRV-พ.ศ.-running` | ✓ |
| TO / CC | `trip_sheet.to` · `trip_sheet.cc` | ข้อความ | TO ✓ · CC — |
| ผู้รับผิดชอบเขต / ตำแหน่ง | `Employee.full_name` · `Employee.position` (F-EMP-001) | ข้อความ | ✓ |
| เขต / รอบการขาย | `trip_sheet.territory` · `trip_sheet.sales_period` | ข้อความ | ✓ |
| ตารางวันทำงาน (loop) | `trip_sheet_line[]` | 1 row = 1 วันทำงาน | — |
| ช่องจำนวนเงินทุกช่อง | `*_amount` | `#,##0.00` ชิดขวา | — |
| ช่องจำนวนใบ/ร้าน | `*_count` · `*_shop` | `#,##0` ชิดขวา | — |
| รวมยอด 13 ช่อง | computed | ตามชนิดของคอลัมน์ | ✓ |
| ผู้ลงนาม | ผู้นำเสนอ + 1 ช่องต่อขั้น DOA | — | ✓ |

## 3. กติกาคำนวณ
- `totals.<col> = Σ lines[].<col>` **ทุกแถวของตาราง** (DEC-12 — ต้นฉบับมีสูตรครอบช่วงไม่ครบ 8 ช่อง ให้ถือว่าผิดและแก้)
- ไม่มีภาษี/ส่วนลด/จำนวนเงินตัวอักษรในฟอร์มนี้
- เตือน (ไม่บล็อก) เมื่อช่อง Accual ของกลุ่มใด > ช่องแผนของกลุ่มเดียวกัน (DEC-04)
- ช่อง "จังหวัดที่ปฎิบัติงาน" ไม่ผูกสูตรกับช่องใด (DEC-13 — ต้นฉบับมีสูตรค้าง `=D39`)

## 4. กติกาการพิมพ์
- A4 · ตารางกรอบเส้นทึบ (`.form-grid`) · ตัวเลขชิดขวา (`g-num`)
- ห้ามตัด row กลาง · block ลายเซ็น (`.signs-block`) ไม่ขึ้นหน้าใหม่แยกจากเนื้อหา
- `layout.dense` = true เสมอสำหรับฟอร์มนี้ (min_rows 31)

## 5. วิธี build ใหม่
```bash
export SKILLS_ROOT=<workspace>/_system/skills
S=$SKILLS_ROOT/pack/thai-doc-pdf-generator/scripts
TD_SCRIPTS=$S python3 -I make_data.py                       # data ตัวอย่าง 5 สถานะ
python3 $S/parity_check.py form.tpl.html *.data.json
python3 $S/build_html.py form.tpl.html --title "ใบเดินทาง : เขตการขาย General Trade" --mode replica --profile profile.json -o TRV_template.html
python3 $S/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "ใบเดินทาง : เขตการขาย General Trade"   # ต้องมี browser
python3 $S/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare --region 0:0.80                                               # ต้องมี browser
```

## 6. Checklist ก่อนส่งมอบ
- [x] parity JS ↔ Python IDENTICAL 5/5
- [x] ไม่มี `{{}}` หลงในผล render ทุกสถานะ (render_doc.py --strict)
- [x] ตัวเลขชิดขวา + `#,##0.00`
- [x] ลายเซ็นครบสาย (ผู้นำเสนอ + 1 ช่อง/ขั้น) + วันที่
- [x] **A4 พอดี ไม่ล้นหน้า** — ทุกสถานะ 1 หน้า (2026-10-10)
- [x] **ภาพวางคู่กับต้นฉบับ** — `out/compare/compare_side.png` + คนดูแล้ว (2026-10-10 · ดู §7)

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `ฟอร์มทริปเดินทาง (เก็บเงิน).xlsx` / FM-SAL-12 (1 ชีท `ทริปเดือน เก็บเงิน sales`) · **ไม่มี Doc No. / Rev. บนกระดาษ**
- Profile: `profile.json` — form_fs 8pt (ขั้นต่ำตาม R10) · form_lh 1.2 · form_title_fs 10pt · form_logo_h 8mm/left · form_grid_pad 1px · form_grid_row_h 4.2mm / dense 3.8mm
- **Override ระดับเอกสาร (หัวไฟล์ `form.tpl.html` — รอ token ใน thai-doc-pdf-generator v2.3):**
  1. `@page A4 landscape; margin 6mm` — ต้นฉบับเป็นแนวนอน (engine มีแต่ portrait) · **เคาะแล้ว 2026-10-10: ทำตามต้นฉบับ** (รอบก่อนทำแนวตั้ง 19 คอลัมน์ 5.6pt → อ่านไม่ออก)
  2. ความกว้าง 21 คอลัมน์ผ่าน `<colgroup>` + class `cw-a…cw-u` — สัดส่วนวัดจาก column width ของ xlsx ต้นฉบับ (ปรับ S +0.8 / T −0.8 กันเลขรวม Accual ล้น)
  3. ตัด padding บน-ล่างของ cell (replica.css ล็อกไว้ 2px ทำให้ 31 แถวไม่จบหน้า)
  4. บล็อกลงชื่อไร้กรอบ + เส้นลอย ตามกระดาษ (`.form-grid--signs{border:0}`)
- **ความต่างจากกระดาษ (ตั้งใจ + เหตุผล)**
  1. **ลายเซ็น dynamic ตาม DOA** — ผู้นำเสนอ + 1 ช่องต่อขั้น ไม่ fix 3 ช่องแบบกระดาษ (DEC-07) · ไม่มีบรรทัด "ตำแหน่ง" (กระดาษไม่มี) · มี ☑/☐ + บรรทัดพิจารณาในระบบ ตามมาตรฐาน B6
  2. **โลโก้/ชื่อบริษัท** มาจาก Organization snapshot (ตัวอย่างใช้ placeholder)
  3. **footer ซ้าย** เพิ่ม "เลขที่ … · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE"
  4. **คงคำสะกดตามกระดาษ** "Accual" และ "ปฎิบัติงาน" (DEC-15 · DEC-16)
  5. ช่องเติมหัวเอกสาร (TO/CC ฯลฯ) ใช้เส้นประมาตรฐาน engine แทนเส้นทึบของกระดาษ
- ผล compare_original (`out/compare/compare_side.png`): **WARN 0.36–0.46** — ต้นฉบับเป็นฟอร์มเปล่า + ฟอนต์ไทยใน SAMPLE.pdf extract เป็น text ไม่ได้ ตัวเทียบจับบรรทัดได้น้อย · **คนดูภาพวางคู่แล้ว 2026-10-10: โครง/คอลัมน์/แถว/ลายเซ็นตรงต้นฉบับ** (บันทึกตามกติกา WARN ไม่บล็อก)
## 8. (Replica) Data contract + สถานะที่ทดสอบ
- ตาราง contract: `TRV_data-contract.md` (key เดิมทั้งหมด — แก้รอบนี้ไม่กระทบ data contract)
- parity JS ↔ Python: **IDENTICAL 5/5** (รัน 2026-10-10 หลังแก้ template)
- สถานะที่ render (`out/`): ร่าง 5 แถว · อนุมัติแล้ว 31 แถว · ไม่อนุมัติ 12 แถว · **เต็มเดือน 31 แถวทุกช่อง (`long-full31` — ฟอร์มเป็นรอบรายเดือน แถว > 31 เป็นไปไม่ได้ จึงแทน long-36rows เดิม)** · DOA 6 ขั้น → **7 ช่อง 1 แถว** (แนวนอนกว้างพอ · `sign_layout.max_per_row = 7`)
- จำนวนหน้า: **ทุกสถานะ 1 หน้า ✅** (render_states 2026-10-10 · `_states_sheet.png`)
## 9. (Replica) print_config (ค่าเริ่มต้นส่งให้ F-DOCCFG)
```json
{
  "doc_type": "TRV",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "",
  "revision": "",
  "paper": "A4-landscape",
  "paper_original": "A4-landscape",
  "min_rows": 31,
  "dense_when_rows_over": 31,
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    { "box": "requester", "label": "ผู้นำเสนอ", "show_date": true },
    { "box": "doa_step:*", "label": "from_doa_step", "show_decision": true, "show_date": true }
  ],
  "decision_words": {
    "default": { "approve": "อนุมัติ", "reject": "ไม่อนุมัติ" }
  },
  "config_reads": {},
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "",
  "footer_right_note": "ต้นฉบับไม่มี Doc No./Rev. บนกระดาษ → ปล่อยว่างจนกว่า F-DOCCFG จะกำหนดรหัสแบบพิมพ์",
  "sign_layout": {
    "source": "approval_chain snapshot (ผู้ขอ + จำนวนขั้นตามที่ตั้งใน DOA)",
    "max_per_row": 7,
    "split": "even",
    "dense_when_steps_over": 4,
    "keep_together": true
  }
}
```
