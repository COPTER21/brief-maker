# 00_OVERVIEW — F-TMP-006 หนังสือสัญญายืม (LOA)

> REQ: REQ-TMP-006 (รหัสชั่วคราว) · Module: Sales · Platform: cube_core
> ที่มา: แบบฟอร์มลูกค้า `ฟอร์มหนังสือสัญญายืมกล่องบรรจุกระดาษ.doc` (Doc No. FM-SAL-14 Rev.00 · 2 หน้า = ต้นฉบับ + สำเนา) → FORM_SPEC → PREBRIEF v2 → DECISIONS.lock
> **มติทุกข้อในชุดนี้เป็น `[AI-DEFAULT]`** (ทำในโหมดไม่เฝ้า) — ต้องให้ลูกค้ายืนยันในใบลงนามก่อน UAT
> ประเภทงาน: แบบ 2 · ดึงข้อมูลเดิม (ลูกค้าอ่านจาก Customer · ผู้ลงนามอ่านจาก Employee · ที่เหลือเก็บในเอกสารนี้)

## 1. ขอบเขตของ FRD ฉบับนี้
ขึ้น **หนังสือสัญญา 2 ฝ่าย** "หนังสือสัญญายืม" เป็นเอกสารในระบบ CUBE NATIVE
— บริษัทให้ลูกค้ายืมกล่องบรรจุกระดาษไปใช้ในกิจการโดยไม่คิดมูลค่า · ผู้ส่งมอบฝ่ายบริษัทลงนามในระบบ · พิมพ์ 2 ชุดให้คู่สัญญาลงนามรับมอบ
เนื้อสัญญาเป็นถ้อยคำคงที่ 2 ข้อ แก้รายฉบับไม่ได้ · มีช่องเติมแทรกในเนื้อความ 1 จุด
**ไม่อยู่ในขอบเขต:** เปลี่ยนค่าตั้งต้นในระบบ · ตัดสต๊อก/ลงบัญชี/ส่งต่อระบบอื่น (DEC-01 · DEC-02) · สร้างใบใหม่จากใบเดิม · ประกาศเมื่อลงนามครบ (DEC-11) · ติดตามการคืนกล่อง (DEC-16)

## 2. ไฟล์ในชุด
| ไฟล์ | เนื้อหา |
|---|---|
| `01_UI.md` | หน้าทะเบียน · drawer สร้าง/แก้ไข 3 ขั้น · drawer ดู 4 แท็บ |
| `02_API.md` | endpoint · payload · รหัสผลลัพธ์ · event |
| `03_LOGIC.md` | state machine + FN-01…FN-12 |
| `04_DB.md` | ตาราง `box_loan_agreement` · `box_loan_agreement_line` · chain · attachment · audit |
| `05_RULES.md` | business rule · validation · DOA · สิทธิ์ · กฎจากตัวอย่างลูกค้า |
| `06_TESTS.md` | เคสทดสอบ รวมเคสปฏิเสธสิทธิ์ |
| `07_LOCKED_DECISIONS.md` | มติ DEC-01…DEC-16 (แทน Scope Lock ชั่วคราว) |

## 3. ของที่ต้องมีก่อนเริ่มพัฒนา
- `DOCCFG_BRIEF_F-TMP-006.md` — doc_type `LOA` (ต้อง register ที่ F-DOCCFG ก่อนเปิดใช้)
- `DOA_BRIEF_F-TMP-006.md` — สายอนุมัติ 1 ขั้น ตั้งที่ DOA กลาง (F-DLG-001) · `wire_status: pending`
- `NTF_BRIEF_F-TMP-006.md` — event `loa_cancelled` · `loa_signed_copy_attached`
- `MDOC_BRIEF_LOA.md` — ทะเบียนแบบเอกสาร F185 (ชุด 2 แบบพิมพ์ ใช้เลขที่เดียว)
- config `SalesPolicy.box_free_replace_pct` — **ยังไม่มีในระบบ ต้องสร้างก่อน**
- แบบพิมพ์: `print/form.tpl.html` + `print/print_config.json` + `print/LOA_print-spec.md` + `print/LOA_data-contract.md`

## 4. ต้นแบบหน้าจอ
`feature.html` (html-generator-v9.2 · archetype **Q-form**) — audit FAIL 0
> **[NO-BROWSER]** รอบนี้ยังไม่ได้รัน `e2e_standard.py` / `render-check.py` / `render_states.py` / `compare_original.py`
> ใช้ node stub-DOM smoke test แทน (S1–S11 PASS) — ต้องรันรอบเต็มบนเครื่องที่มี browser ก่อน UAT (ดู `reports/e2e_report.json`)
