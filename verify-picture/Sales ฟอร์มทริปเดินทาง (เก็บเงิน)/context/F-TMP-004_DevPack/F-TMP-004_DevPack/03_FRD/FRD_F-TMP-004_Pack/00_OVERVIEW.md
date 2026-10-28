# 00_OVERVIEW — F-TMP-004 ใบเดินทาง : เขตการขาย General Trade (TRV)

> REQ: REQ-TMP-004 (รหัสชั่วคราว) · Module: Sales · Platform: cube_core
> ที่มา: แบบฟอร์มลูกค้า `ฟอร์มทริปเดินทาง (เก็บเงิน).xlsx` (1 ชีท `ทริปเดือน เก็บเงิน sales`) → FORM_SPEC → PREBRIEF v2 → DECISIONS.lock
> **มติทุกข้อในชุดนี้เป็น `[AI-DEFAULT]`** (ทำในโหมดไม่เฝ้า) — ต้องให้ลูกค้ายืนยันในใบลงนามก่อน UAT
> ประเภทงาน: แบบ 2 · ดึงข้อมูลเดิม (ผู้รับผิดชอบเขต/ตำแหน่ง อ่านจาก Employee · ที่เหลือเก็บในเอกสารนี้)

## 1. ขอบเขตของ FRD ฉบับนี้
ขึ้นแบบฟอร์มกระดาษ "ใบเดินทาง : เขตการขาย General Trade" เป็นเอกสารในระบบ CUBE NATIVE
— กรอกแผน/ผลการออกตลาดรายวันของเขตการขาย 1 รอบ · ยอดรวมคำนวณให้ · ส่งอนุมัติตามสาย DOA · พิมพ์ PDF ให้เหมือนกระดาษเดิม
**ไม่อยู่ในขอบเขต:** เปลี่ยนค่าตั้งต้นในระบบ · ส่งข้อมูลต่อระบบอื่น (DEC-01 · DEC-02) · ทำซ้ำเอกสาร · ประกาศเมื่ออนุมัติ (DEC-11)

## 2. ไฟล์ในชุด
| ไฟล์ | เนื้อหา |
|---|---|
| `01_UI.md` | หน้าทะเบียน · drawer สร้าง/แก้ไข 3 ขั้น · drawer ดู 4 แท็บ |
| `02_API.md` | endpoint · payload · รหัสผลลัพธ์ · event |
| `03_LOGIC.md` | state machine + FN-01…FN-12 |
| `04_DB.md` | ตาราง `trip_sheet` · `trip_sheet_line` · chain · attachment · audit |
| `05_RULES.md` | business rule · validation · DOA · สิทธิ์ · กฎจากตัวอย่างลูกค้า |
| `06_TESTS.md` | เคสทดสอบ รวมเคสปฏิเสธสิทธิ์ |
| `07_LOCKED_DECISIONS.md` | มติ DEC-01…DEC-16 (แทน Scope Lock ชั่วคราว) |

## 3. ของที่ต้องมีก่อนเริ่มพัฒนา
- `DOCCFG_BRIEF_F-TMP-004.md` — doc_type `TRV` (ต้อง register ที่ F-DOCCFG ก่อนเปิดใช้)
- `DOA_BRIEF_F-TMP-004.md` — สายอนุมัติ 2 ขั้น ตั้งที่ DOA กลาง (F-DLG-001) · `wire_status: pending`
- `NTF_BRIEF_F-TMP-004.md` — event `trv_cancelled`
- `MDOC_BRIEF_TRV.md` — ทะเบียนแบบเอกสาร F185
- แบบพิมพ์: `print/form.tpl.html` + `print/print_config.json` + `print/TRV_print-spec.md` + `print/TRV_data-contract.md`

## 4. ต้นแบบหน้าจอ
`feature.html` (html-generator-v9.2 · archetype **Q-form**) — audit FAIL 0
> **[NO-BROWSER]** รอบนี้ยังไม่ได้รัน `e2e_standard.py` / `render-check.py` / `render_states.py` / `compare_original.py`
> ต้องรันรอบเต็มบนเครื่องที่มี browser ก่อน UAT (ดู `reports/e2e_report.json`)
