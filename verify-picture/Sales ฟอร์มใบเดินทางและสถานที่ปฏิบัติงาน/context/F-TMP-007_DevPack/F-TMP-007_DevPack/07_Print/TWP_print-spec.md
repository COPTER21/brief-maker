# PRINT SPEC — ใบเดินทางและสถานที่ปฎิบัติงาน  สำหรับ General Trade (TWP)

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD/Brief ของ F-TMP-007
> ไฟล์คู่: `TWP_template.html` (master, fonts ฝัง) + `out/<state>.html` (ตัวอย่างแต่ละสถานะ)
> **โหมด: Replica** (แบบฟอร์มลูกค้า) — กรอก §7–§9 ครบ

## 1. สรุป
- **ประเภทเอกสาร:** ใบเดินทางและสถานที่ปฎิบัติงาน สำหรับ General Trade / General Trade Travel and Work Place Sheet
- **เลขแบบพิมพ์บนกระดาษ:** `Doc.No.FM-SAL-13` · `Rev.00: 01/07/2569` (อยู่ที่ footer ของชีทต้นฉบับ)
- **ขนาด:** A4 แนวตั้ง (210×297mm) ขอบ 14mm — **ต้นฉบับเป็น A4 แนวนอน** (ดู §7 ความต่างที่ตั้งใจ)
- **ฟอนต์:** Sarabun (ฝัง base64)
- **CI:** Replica = หมึกเดียวตาม profile ลูกค้า (ไม่ใช้สี CI ของ CUBE ในเนื้อฟอร์ม)
- **Renderer:** Playwright/Chromium → `print_background`, `prefer_css_page_size`
- **บล็อก:** R1 โลโก้ · R2 ชื่อเอกสาร 2 บรรทัด · **R9 ตารางกรอบ 21 คอลัมน์** · R9 ตารางสรุป/เอกสารแนบ · B6 sign_rows · B7 footer

## 2. Field Mapping
ดูตารางเต็มใน `TWP_data-contract.md` (45 ช่องตาม FORM_SPEC: หัวเอกสาร 6 · แถวซ้ำ 21 ต่อแถว · รวมยอด 11 · สรุปท้ายใบ 4 · ท้ายกระดาษ 3)

| ช่องในเอกสาร | Source | Format | บังคับ |
|---|---|---|---|
| เลขที่เอกสาร (footer) | ENG-DOC-NUM · ออกตอนบันทึกครั้งแรก (DEC-11) | `TWP-พ.ศ.-running` | ✓ |
| เรียน (2 บรรทัด) | `travel_sheet.to` · `travel_sheet.to_line2` | ข้อความ | บรรทัดแรก ✓ |
| จาก / โทรศัพท์ | `Employee.full_name` · `Employee.phone` (F-EMP-001) | ข้อความ | จาก ✓ |
| Date | `travel_sheet.doc_date` (ระบบใส่) | วันที่ไทย | ✓ |
| รอบการขายที่ | `travel_sheet.sales_period` | ข้อความ | ✓ |
| ตารางวันทำงาน (loop) | `travel_sheet_line[]` | 1 row = 1 วันทำงาน | — |
| ช่องจำนวนเงินทุกช่อง | `cost_*` · `fuel_amount` · `summary.*` | `#,##0.00` ชิดขวา | — |
| เลขไมล์ / ลิตร | `odometer_*` · `fuel_liter` | `#,##0` ชิดขวา | — |
| รวมยอด 11 ช่อง | computed | ตามชนิดของคอลัมน์ | ✓ |
| บล็อกสรุปท้ายใบ 4 บรรทัด | `summary.*` | `#,##0.00` ชิดขวา | ✓ |
| เอกสารที่แนบ (loop 3 บรรทัด) | `travel_sheet_attachment[]` | ข้อความ | — |
| ผู้ลงนาม | ผู้จัดทำ + 1 ช่องต่อขั้น DOA | — | ✓ |

## 3. กติกาคำนวณ
- `lines[].line_total = cost_lodging + cost_hotel + cost_perdiem + cost_laundry + cost_fee + cost_post + cost_parking + cost_other` (DEC-14 — ต้นฉบับปล่อยช่องนี้ว่างไม่มีสูตร)
- `totals.<col> = Σ lines[].<col>` **ทุกแถวของตาราง** รวมคอลัมน์ "ค่าใช้จ่ายที่พัก — ที่พัก" ที่ต้นฉบับไม่มีสูตร (DEC-13)
- `summary.grand_total = totals.line_total + summary.phone_cost` (DEC-13 — ต้นฉบับใช้ `=P36` ไม่บวกค่าโทรศัพท์)
- `summary.balance = summary.grand_total - summary.advance_received` · ค่าลบ = ต้องคืนบริษัท (เตือนไม่บล็อก)
- เตือน (ไม่บล็อก) เมื่อเลขไมล์สิ้นสุด < เลขไมล์เริ่มต้นในแถวเดียวกัน (DEC-04)
- ไม่มีภาษี/ส่วนลด/จำนวนเงินตัวอักษรในฟอร์มนี้

## 4. กติกาการพิมพ์
- A4 · ตารางกรอบเส้นทึบ (`.form-grid`) · ตัวเลขชิดขวา (`g-num`)
- ห้ามตัด row กลาง · block ลายเซ็น (`.signs-block`) ไม่ขึ้นหน้าใหม่แยกจากเนื้อหา
- `layout.dense` = true เสมอสำหรับฟอร์มนี้ (min_rows 27)

## 5. วิธี build ใหม่
```bash
export SKILLS_ROOT=<workspace>/_system/skills
S=$SKILLS_ROOT/pack/thai-doc-pdf-generator/scripts
TD_SCRIPTS=$S python3 -I make_data.py                       # data ตัวอย่าง 5 สถานะ
python3 $S/parity_check.py form.tpl.html *.data.json
python3 $S/build_html.py form.tpl.html --title "ใบเดินทางและสถานที่ปฎิบัติงาน  สำหรับ General Trade" --mode replica --profile profile.json -o TWP_template.html
python3 $S/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "ใบเดินทางและสถานที่ปฎิบัติงาน  สำหรับ General Trade"   # ต้องมี browser
python3 $S/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare --region 0:0.80                                                                   # ต้องมี browser
```

## 6. Checklist ก่อนส่งมอบ
- [x] parity JS ↔ Python IDENTICAL 5/5
- [x] ไม่มี `{{}}` หลงในผล render ทุกสถานะ (render_doc.py)
- [x] ตัวเลขชิดขวา + `#,##0.00`
- [x] ลายเซ็นครบสาย (ผู้จัดทำ + 1 ช่อง/ขั้น) + วันที่
- [ ] **A4 พอดี ไม่ล้นหน้า** — ยังไม่ได้ยืนยัน (NO-BROWSER · ดู §8)
- [ ] **ภาพวางคู่กับต้นฉบับ** — ยังไม่ได้ทำ (NO-BROWSER · ดู §7)

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `ฟอร์มใบเดินทางและสถานที่ปฏิบัติงาน.xlsx` (1 ชีท `Sheet1` · A4 แนวนอน) · **มี Doc No./Rev. ที่ footer ของชีท**
- Profile: `profile.json` — token ที่ต่างจาก default: form_fs 5.4pt · form_lh 1.22 · form_title_fs 11pt · form_title_gap 6px · form_logo_h 10mm · form_logo_maxw 45mm · form_logo_align left · form_grid_pad 1px · form_grid_row_h 5.0mm · form_grid_row_h_dense 4.1mm
- **ความต่างจากกระดาษ (ตั้งใจ + เหตุผล)**
  1. **แนวกระดาษ** — ต้นฉบับ A4 **แนวนอน** · engine (base.css `@page size:A4 portrait`) รองรับแนวตั้งอย่างเดียว และห้ามแก้ base.css รายเอกสาร → ทำเป็น A4 แนวตั้ง + ย่อขนาดตัวอักษร/ระยะผ่าน profile · **ต้องให้คนเคาะ**: รับแบบแนวตั้ง หรือเพิ่ม token แนวกระดาษใน thai-doc-pdf-generator
  2. **สัดส่วนความกว้างคอลัมน์** — โหมด Replica ห้ามเขียน style ใน body และมีคลาสความกว้างแค่ `g-25/g-50/g-75` → ใช้ `table-layout:fixed` 21 คอลัมน์เท่ากัน ไม่ตรงสัดส่วนต้นฉบับ (ต้นฉบับคอลัมน์ "สถานที่พัก"/"หมายเหตุ" กว้างกว่าคอลัมน์ตัวเลข) · **ต้องให้คนเคาะ**: เพิ่มคลาส/token ความกว้างคอลัมน์ในสกิล
  3. **ลายเซ็นย้ายเป็นแถวล่าง** ตามหลัก B6 — ช่องตามขั้น DOA (ผู้จัดทำ + 1 ช่อง/ขั้น) ไม่ fix 2 ช่องแบบกระดาษ (DEC-08) · กระดาษไม่มีคำกำกับว่าช่องไหนเป็นใคร จึงกำหนดค่าเริ่มตาม DEC-16
  4. **บล็อกสรุปท้ายใบ + เอกสารที่แนบ** ต้นฉบับวางลอยในเซลล์ (M37:P40 / H42:H44) → ทำเป็นตารางกรอบ 4 แถวต่อจากตารางหลัก เพื่อให้ render ได้ด้วย R9 เดียวกัน
  5. **โลโก้/ชื่อบริษัท** มาจาก Organization snapshot (ตัวอย่างใช้ placeholder) — ไม่ใช้โลโก้/ชื่อบริษัทของลูกค้าในตัวอย่าง
  6. **footer ซ้าย** เพิ่ม "เลขที่ … · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE" (สิ่งที่ระบบเพิ่มได้โดยไม่ต้องถาม) · footer ขวา = Doc.No./Rev. ตามกระดาษ
  7. **คงคำสะกดตามกระดาษ** "ปฎิบัติงาน" ในหัวเรื่อง (หัวคอลัมน์ในตารางสะกด "ปฏิบัติงาน" ถูกต้องอยู่แล้ว) (DEC-17) — เสนอให้ลูกค้าแก้ในรอบปรับปรุงฟอร์ม
- ผล compare_original: **ยังไม่ได้รัน — [NO-BROWSER]** · ต้องรันรอบเต็มบนเครื่องที่มี browser แล้วดู `out/compare/compare_side.png`

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- ตาราง contract: `TWP_data-contract.md`
- parity JS ↔ Python: **IDENTICAL 5/5**
- สถานะที่ทำ data + render (HTML ฝั่ง Python): ร่าง 5 แถว · อนุมัติแล้ว 18 แถว · ไม่อนุมัติ 12 แถว · ยาว 34 แถว (dense) · **DOA 6 ขั้น → 7 ช่อง 2 แถว (4+3)**
- จำนวนหน้า: **ยังไม่ได้ยืนยัน — [NO-BROWSER]** (render_states.py / `_states_sheet.png` ข้าม)

## 9. (Replica) print_config (ค่าเริ่มต้นส่งให้ F-DOCCFG)
ดูไฟล์จริง `print/print_config.json` — ค่าหลัก: `doc_type TWP` · `mode replica` · `paper A4-portrait` (`paper_original A4-landscape`) · `min_rows 27` · `min_rows_attachments 3` · `form_code FM-SAL-13` · `revision Rev.00: 01/07/2569` · `sign_boxes` = requester (ผู้จัดทำ) + `doa_step:*` · `decision_words.default` = อนุมัติ/ไม่อนุมัติ · `sign_layout.max_per_row 4`
