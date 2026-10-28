# PRINT SPEC — แบบฟอร์มสำรวจสมรรถนะ (CMP)

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD/Brief ของ F-TMP-005
> ไฟล์คู่: `CMP_template.html` (master · fonts ฝัง) + `out/<state>.html` (ตัวอย่างทุกสถานะ)
> **โหมด: Replica** (แบบฟอร์มลูกค้า FM-HRM-40)

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มสำรวจสมรรถนะ / Competency Survey Form
- **ขนาด:** A4 แนวตั้ง (210×297mm) · **ฟอนต์:** Sarabun (ฝัง base64)
- **CI:** Replica → หมึกเดียวตาม `profile.json` (ไม่ใช้สี CI CUBE ในเนื้อฟอร์ม)
- **Renderer:** Chromium/Playwright → `print_background`, `prefer_css_page_size`
- ⚠️ **รอบนี้รันในโหมด NO-BROWSER** — ยังไม่ได้ออก PDF/ภาพ (ดู §8)

## 2. Field Mapping
ดู `CMP_data-contract.md` (ตารางเต็ม key → entity.field → ตัวอย่าง)

## 3. กติกาคำนวณ
- **ไม่มีสูตรบนกระดาษ** (FORM_SPEC.formulas = 0) — ไม่มีการคำนวณใด ๆ ในแบบพิมพ์
- ตารางระดับ 1–4 เป็น **ค่าจาก config** `CompetencyLevelConfig.levels[]` (DEC-04) ห้าม hardcode

## 4. กติกาการพิมพ์
- หัวตารางซ้ำทุกหน้า · ห้ามตัด row กลาง · บล็อกลงชื่อ `break-inside: avoid` (`.signs-block`)
- แถวว่างเติมใน data จนครบขั้นต่ำตามกระดาษ (core 5 · func 6) — template ไม่นับ
- ตัวเลือก ☐/☑ ส่งเป็น glyph จาก data

## 5. วิธี build ใหม่
```bash
source _system/vars.sh
python3 $TD/scripts/build_html.py form.tpl.html --title "แบบฟอร์มสำรวจสมรรถนะ" --mode replica --profile profile.json -o CMP_template.html
python3 $TD/scripts/render_pdf.py CMP_template.html -o CMP_sample.pdf        # ต้องมี browser
python3 print/make_data.py                                                   # สร้าง data 5 สถานะใหม่
```

## 6. Checklist ก่อนส่งมอบ
- [x] parity JS ↔ Python IDENTICAL 5/5
- [x] ไม่มี `{{}}` หลงในทุกสถานะ
- [x] ช่องลงชื่อมาจาก `sign_rows` (ไม่ fix จำนวน) — ทดสอบ 1 ขั้น (2 ช่อง) และ 6 ขั้น (7 ช่อง → 4+3)
- [ ] **ค้าง (NO-BROWSER):** PDF ทุกสถานะ · `_states_sheet.png` · `compare/compare_side.png` · จำนวนหน้า

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `ฟอร์มสำรวจสมรรถนะ.docx` (2 หน้า) · Doc No. `FM-HRM-40` · `REV.00 : 01/07/2569` · โลโก้ Credence
- Profile: `profile.json` — token ที่ต่างจาก default: `form_fs 9pt` · `form_title_fs 15pt` · `form_logo_h 13mm` · `form_title_gap 10px` · `form_grid_gap 4px` · `form_row_gap 6px`
- **ความต่างจากกระดาษ (ตั้งใจ + เหตุผล)**
  1. โลโก้ลูกค้า (Credence) → `{{{company.logo}}}` จาก Organization snapshot (หลักข้อ 4 ของ form-replica)
  2. ช่อง "ลงชื่อผู้ประเมิน / ลงชื่อผู้รับประเมิน" บนกระดาษ (2 บรรทัดชิดขวา) → **บล็อกลงชื่อแถวล่าง B6** ช่องตามสาย DOA (DEC-08) · ลำดับในระบบ = ผู้รับประเมิน (เจ้าของใบ) ก่อน แล้วตามด้วยผู้ประเมินตามขั้น DOA
  3. ใช้ข้อความ "ส่งในระบบ / พิจารณาในระบบ …" แทนลายมือชื่อ (DEC-08 · ไม่ใช้ภาพลายเซ็น)
  4. footer ซ้าย "เลขที่ … · ร่าง · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE" (สิ่งที่ระบบเพิ่มได้โดยไม่ต้องถาม)
  5. ตารางระดับ 1–4 กลายเป็น loop จาก config (ถ้อยคำเดิมทุกตัวอักษร) — ลูกค้าแก้คำอธิบายได้โดยไม่แก้แบบพิมพ์
  6. ต้นฉบับแบ่ง 2 หน้าเพราะตารางสมรรถนะเฉพาะสายงานถูกตัด — ฉบับระบบจัดต่อเนื่อง จำนวนหน้าขึ้นกับจำนวนแถวจริง
- **ผล compare_original: ยังไม่ได้รัน** — โหมด NO-BROWSER (ต้องรันรอบเต็มบนเครื่องที่มี browser · แนะนำ `--region 0:0.78` เพื่อตัดบล็อกลงชื่อที่ตั้งใจย้าย)

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- ตาราง contract: `CMP_data-contract.md`
- parity JS ↔ Python: **IDENTICAL 5/5**
- สถานะที่สร้าง data + render body แล้ว (HTML ครบ · PDF ยังไม่ได้ออก):
  | สถานะ | ไฟล์ | ช่องลงชื่อ |
  |---|---|---|
  | ร่าง | `draft` | 2 (1 แถว) |
  | อนุมัติแล้ว | `approved` | 2 (1 แถว) |
  | ไม่อนุมัติ (ส่งกลับแก้ไข) | `rejected` | 2 (1 แถว) |
  | ยาว 12+12 แถว + dense | `long-12rows` | 2 (1 แถว) |
  | DOA 6 ขั้น | `approved-doa6steps` | 7 (2 แถว 4+3) |
- **ค้างตรวจ:** จำนวนหน้า/การตัดหน้า ต้องยืนยันด้วย `render_states.py` บนเครื่องที่มี browser

## 9. (Replica) print_config
ดู `print_config.json` (doc_type `CMP` · `sign_boxes: requester + doa_step:*` · `decision_words.by_role[role-line-manager] = เห็นชอบ/ส่งกลับแก้ไข`)
