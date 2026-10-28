# 00_OVERVIEW — F-TMP-007 ใบเดินทางและสถานที่ปฎิบัติงาน  สำหรับ General Trade (TWP)

> REQ: REQ-TMP-007 (รหัสชั่วคราว) · Module: Sales · Platform: cube_core
> ที่มา: แบบฟอร์มลูกค้า `ฟอร์มใบเดินทางและสถานที่ปฏิบัติงาน.xlsx` (1 ชีท `Sheet1` · A4 แนวนอน · `Doc.No.FM-SAL-13 Rev.00: 01/07/2569`) → FORM_SPEC → PREBRIEF v2 → DECISIONS.lock
> **มติทุกข้อในชุดนี้เป็น `[AI-DEFAULT]`** (ทำในโหมดไม่เฝ้า) — ต้องให้ลูกค้ายืนยันในใบลงนามก่อน UAT
> ประเภทงาน: แบบ 2 · ดึงข้อมูลเดิม (ผู้จัดทำ/ตำแหน่ง/โทรศัพท์ อ่านจาก Employee · ที่เหลือเก็บในเอกสารนี้)

## 1. ขอบเขตของ FRD ฉบับนี้
ขึ้นแบบฟอร์มกระดาษ "ใบเดินทางและสถานที่ปฎิบัติงาน สำหรับ General Trade" เป็นเอกสารในระบบ CUBE NATIVE
— บันทึกวันทำงาน เส้นทาง/ตลาดที่ปฏิบัติงาน สถานที่พัก และค่าใช้จ่ายที่ขอเบิกรายวันของรอบการขาย 1 รอบ
· ยอดรวมรายแถวและรายคอลัมน์คำนวณให้ · สรุปท้ายใบ (ค่าโทรศัพท์ · รวมทั้งสิ้น · เบิกเงินสำรอง · คงเหลือ) คำนวณให้
· ส่งอนุมัติตามสาย DOA · พิมพ์ PDF ให้เหมือนกระดาษเดิม
**ไม่อยู่ในขอบเขต:** เปลี่ยนค่าตั้งต้นในระบบ · ส่งข้อมูลต่อระบบอื่น เช่น ตั้งหนี้/จ่ายเงิน (DEC-01 · DEC-02) · ทำซ้ำเอกสาร · ประกาศเมื่ออนุมัติ (DEC-12)

## 2. ไฟล์ในชุด
| ไฟล์ | เนื้อหา |
|---|---|
| `01_UI.md` | หน้าทะเบียน · drawer สร้าง/แก้ไข 3 ขั้น · drawer ดู 4 แท็บ |
| `02_API.md` | endpoint · payload · รหัสผลลัพธ์ · event |
| `03_LOGIC.md` | state machine + FN-01…FN-13 |
| `04_DB.md` | ตาราง `travel_sheet` · `travel_sheet_line` · `travel_sheet_attachment_line` · chain · ไฟล์แนบ · audit |
| `05_RULES.md` | business rule · validation · DOA · สิทธิ์ · กฎจากตัวอย่างลูกค้า |
| `06_TESTS.md` | เคสทดสอบ รวมเคสปฏิเสธสิทธิ์ |
| `07_LOCKED_DECISIONS.md` | มติ DEC-01…DEC-17 (แทน Scope Lock ชั่วคราว) |

## 3. ของที่ต้องมีก่อนเริ่มพัฒนา
- `DOCCFG_BRIEF_F-TMP-007.md` — doc_type `TWP` (ต้อง register ที่ F-DOCCFG ก่อนเปิดใช้)
- `DOA_BRIEF_F-TMP-007.md` — สายอนุมัติค่าเริ่ม 1 ขั้น ตั้งที่ DOA กลาง (F-DLG-001) · `wire_status: pending`
- `NTF_BRIEF_F-TMP-007.md` — event `twp_cancelled`
- `MDOC_BRIEF_TWP.md` — ทะเบียนแบบเอกสาร F185
- แบบพิมพ์: `print/form.tpl.html` + `print/print_config.json` + `print/TWP_print-spec.md` + `print/TWP_data-contract.md`

## 4. ต้นแบบหน้าจอ
`feature.html` (html-generator-v9.2 · archetype **Q-form**) — audit FAIL 0 · WARN 4 (ตกทอดจาก base-kit ของ archetype)
> **[NO-BROWSER]** รอบนี้ยังไม่ได้รัน `e2e_standard.py` / `render-check.py` / `render_states.py` / `compare_original.py`
> แทนด้วย `reports/nodom_smoke.js` (node + stub DOM) → `reports/nodom_smoke_report.txt` = ALL CHECKS OK
> ต้องรันรอบเต็มบนเครื่องที่มี browser ก่อน UAT
