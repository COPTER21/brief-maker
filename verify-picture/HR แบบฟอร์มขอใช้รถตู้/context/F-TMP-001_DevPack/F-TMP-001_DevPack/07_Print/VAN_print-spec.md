# PRINT SPEC — แบบฟอร์มขอใช้รถตู้ (VAN)

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD/BRD ของ F-TMP-001
> ไฟล์คู่: `VAN_template.html` (master · ฝัง Sarabun) + `form.tpl.html` (template logic-less) + `profile.json`
> **โหมด: Replica** (แบบฟอร์มลูกค้า FM-HRM-22) — กรอก §7–§9 ครบ

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มขอใช้รถตู้ / Van Request Form
- **ขนาด:** A4 แนวตั้ง (210×297mm) ขอบ 14mm
- **ฟอนต์:** Sarabun (ฝัง base64 ใน HTML)
- **CI:** Replica = หมึกเดียวตาม profile ลูกค้า (ห้ามใช้สี CI CUBE ในเนื้อฟอร์ม)
- **Renderer:** Playwright/Chromium → `print_background`, `prefer_css_page_size`

## 2. Field Mapping (UI/DB → ช่องในเอกสาร)
ดูตารางเต็มใน `VAN_data-contract.md` — สรุปกลุ่ม:

| กลุ่มช่อง | Source | Format | บังคับ |
|---|---|---|---|
| เลขที่เอกสาร (footer) | ENG-DOC-NUM (VAN) | `VAN-พ.ศ.-####` | ✓ |
| วันที่ (หัวฟอร์ม) | `van_request.doc_date` | วัน เดือน(ไทย) พ.ศ. | ✓ |
| ผู้ขอ (ชื่อ · รหัส · ตำแหน่ง · ฝ่าย · แผนก) | Employee / OrgUnit (อ่านอย่างเดียว) | — | ✓ |
| ช่วงวันที่ขอใช้ + จำนวนวัน | user + computed | วันที่ไทย · จำนวนเต็ม | ✓ |
| ลักษณะการเดินทาง (3 ตัวเลือก) | `trip_mode` | `☑`/`☐` | ✓ |
| วัตถุประสงค์ | user | — | ✓ |
| รายชื่อผู้เดินทาง (loop) | `travelers[]` | 1 row = 1 คน · เติมว่างครบ 5 | – |
| การเดินทางขาไป/ขากลับ (สถานที่ + เวลา) | user | เวลา `HH:MM` | ตามตัวเลือก |
| ช่องลงชื่อ | ผู้ขอ + `approval_chain` (DOA) | ไม่ fix จำนวน | ✓ |

## 3. กติกาคำนวณ
- `use.total_days = (use_date_to − use_date_from) + 1` (นับรวมวันเริ่มและวันสิ้นสุด) — DEC-04 / DEC-13
- `use_date_to < use_date_from` = **บล็อก** (ขัดแย้งทางตรรกะ)
- ติ๊ก `เดินทางเฉพาะขาไป` → `return_trip.*` = `""` · `เฉพาะขากลับ` → `outbound.*` = `""` · `ไป-กลับ` → ครบทั้งสอง — DEC-14
- `dropoff_time < pickup_time` ในขาเดียวกัน = **เตือน** (ไม่บล็อก)
- ไม่มีค่าคงที่/สูตรเงินบนกระดาษ → ไม่ใช้ `baht_text`

## 4. กติกาการพิมพ์
- A4 แนวตั้ง · lean type 9.6pt · เส้นประช่องกรอก (`.fill`) · ลายเซ็น + footer ชิดล่าง (`.doc-bottom`)
- บล็อกลงชื่อห่อ `.signs-block` → ไม่ถูกตัดข้ามหน้า
- ขั้น DOA > 4 → `layout.dense` · แถวละ ≤ 4 ช่อง (7 ช่อง = 4+3)
- รายชื่อผู้เดินทาง > 5 แถว → `layout.dense`

## 5. วิธี build ใหม่ (regenerate)
```bash
source _system/vars.sh
cd <work>/print
TD_SCRIPTS=$TD/scripts python3 make_data.py                                  # data 5 สถานะ
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json                # ต้อง IDENTICAL ทุกไฟล์
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out \
        --mode replica --profile profile.json --title "แบบฟอร์มขอใช้รถตู้"   # ★ ต้องมี browser
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf \
        -o out/compare --region 0:0.72                                       # ★ ต้องมี browser
python3 $TD/scripts/build_html.py form.tpl.html --title "แบบฟอร์มขอใช้รถตู้" \
        --mode replica --profile profile.json -o VAN_template.html
```

## 6. Checklist ก่อนส่งมอบ
- [x] parity JS ↔ Python IDENTICAL 5/5 · ไม่มีคำเตือน (float/boolean/`{}` ว่าง)
- [x] ไม่มี `{{…}}` หลงใน body ทุกสถานะ
- [x] ช่องลงชื่อไม่ fix จำนวน (1 + จำนวนขั้น DOA) · คำตัดสินผูก role
- [x] ไม่มีข้อมูลส่วนบุคคลจากไฟล์ลูกค้าใน data ตัวอย่าง (ใช้ชื่อสมมติทั้งหมด)
- [ ] **A4 พอดี 1 หน้าทุกสถานะ** — ค้าง: ไม่มี browser ในเครื่องนี้ (ดู §8)
- [ ] **เทียบต้นฉบับ (compare_original)** — ค้าง: ไม่มี browser ในเครื่องนี้ (ดู §7)
- [ ] ดูภาพ `_states_sheet.png` + `compare/compare_side.png` — ค้าง

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `orig/HR แบบฟอร์มขอใช้รถตู้.docx` (→ `orig/SAMPLE.pdf`) · Doc No. `FM-HRM-22` · `Rev. 00 : 01/07/2569`
- Profile `profile.json` — token ที่ต่างจาก default: `form_title_fs 13pt` · `form_logo_h 14mm` · `form_row_gap 7px` · `form_indent 10mm` · `form_fill_m 28mm`
- **ความต่างจากกระดาษ (ตั้งใจ + เหตุผล)**
  1. บล็อกลงชื่อทั้งหมด (ผู้ขอ + ผู้บังคับบัญชา + ผู้จัดการฝ่ายทรัพยากรบุคคล) ย้ายมาเป็น **แถวล่าง 1 ช่องต่อขั้น DOA** — DEC-07 (G6) · จำนวนช่องเปลี่ยนตาม DOA กลางได้โดยไม่แก้แบบพิมพ์
  2. ชื่อผู้พิจารณาไม่พิมพ์ตายตัว — ต้นฉบับพิมพ์ชื่อบุคคลจริงไว้ใต้ช่องผู้จัดการฝ่ายทรัพยากรบุคคล · ระบบ resolve จาก DOA ตอนส่ง (DEC-12 · PDPA)
  3. ลายมือชื่อแทนด้วยข้อความ "ส่งในระบบ / พิจารณาในระบบ วันที่ เวลา" — DEC-07 (ไม่ใช้ภาพลายเซ็น)
  4. footer ซ้ายเพิ่ม "เลขที่ … · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE" — ของมาตรฐานระบบ
  5. "รวมเป็นจำนวน … วัน" คำนวณให้อัตโนมัติแทนการกรอกเอง — DEC-04 / DEC-13
  6. ไม่เพิ่ม/ตัดช่องใด ๆ จากกระดาษ (G5 1:1 · 22 ช่อง ครบ)
- **ผล compare_original: ยังไม่ได้รัน — `[NO-BROWSER]`** (เครื่องนี้ไม่มี Edge/Chrome/Chromium) · ต้องรันรอบเต็มด้วย `--region 0:0.72` (ตัดส่วนลายเซ็นที่ตั้งใจย้าย) บนเครื่องที่มี browser

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- ตาราง contract: `VAN_data-contract.md`
- parity JS ↔ Python: **IDENTICAL 5/5**
- สถานะที่สร้าง data + body HTML (ไม่มี `{{}}` หลง): `draft` · `approved` · `rejected` (เลือก "เดินทางเฉพาะขาไป" → บล็อกขากลับว่าง) · `long-12rows-3signs` (ผู้เดินทาง 12 คน · ลงชื่อ 4 ช่อง · dense) · `approved-doa6steps` (DOA 6 ขั้น → ลงชื่อ 7 ช่อง 2 แถว 4+3)
- **จำนวนหน้า: ยังไม่ทราบ — `[NO-BROWSER]` ไม่ได้ render PDF** (ดู `out/_states.json`) → ต้องยืนยัน "1 หน้าทุกสถานะ" บนเครื่องที่มี browser

## 9. (Replica) print_config (ส่งให้ F-DOCCFG ผ่าน doccfg-declaration)
ดู `print_config.json` ในโฟลเดอร์เดียวกัน — `doc_type VAN` · `sign_boxes: requester + doa_step:*` · `decision_words.by_role.role-mgr-hr = เห็นควร/ไม่เห็นควร` · `sign_layout.max_per_row 4`
