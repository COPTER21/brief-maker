# PRINT SPEC — ใบเบิกค่าใช้จ่าย (EXP) · F-HR-EXPENSE

> เอกสารประกอบสำหรับ Dev — แนบคู่ FRD/BRD ของ F-HR-EXPENSE
> ไฟล์คู่: `expense_template.html` (master, Sarabun ฝัง base64) + `expense_sample.pdf` (ตัวอย่าง A4 · 1 หน้า)
> โครงเดียวกับ tab **PDF Preview (a4)** ใน prototype `outputs/F-HR-EXPENSE/expense.html` (Pattern Q)

## 1. สรุป
- **ประเภทเอกสาร:** ใบเบิกค่าใช้จ่าย / Expense Claim
- **ขนาด:** A4 แนวตั้ง (210×297mm), ขอบ 14mm · ยืนยันแล้ว MediaBox = 594.96 × 841.92 pt
- **ฟอนต์:** Sarabun (ฝัง base64 ใน HTML — ไม่พึ่ง network)
- **CI:** CUBE NATIVE (Navy #0B1D3A / Primary #0B5CFF / Teal #00A88E) — ใช้ผ่าน class เท่านั้น
- **Renderer:** Playwright/Chromium → `print_background`, `prefer_css_page_size`
- **เลข EXP-YYYY-NNNN + สำเนา:** ออกตอน **อนุมัติ** (ENG-DOC-NUM / ENG-DOC-STORE · doccfg) — เอกสาร immutable snapshot ณ วันอนุมัติ (BR-06)

## 2. Field Mapping (UI/DB → ช่องในเอกสาร)

| ช่องในเอกสาร | Source (entity.field) | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่เอกสาร | ENG-DOC-NUM.next('EXP') | `EXP-พ.ศ.-NNNN` | ✓ | ออกตอนอนุมัติ · reset รายปี พ.ศ. · no-gap (doccfg) |
| วันที่เอกสาร | header.doc_date | วัน เดือน(ไทย) พ.ศ. | ✓ | พ.ศ. ทั้งใบ (2569) |
| ช่องทางจ่าย | header.pay_method | enum | ✓ | ผ่านรอบเงินเดือน / โอนตรง [A-EXP-01] |
| สถานะ | header.status | enum | ✓ | อนุมัติแล้ว/… (state machine §5) |
| ผู้เบิก (ชื่อ + รหัส) | Employee(snapshot) | — | ✓ | soft ref · snapshot ชื่อ/รหัส ณ ออกเอกสาร |
| ตำแหน่ง · แผนก · ศูนย์ต้นทุน | Movement assignment/resolve(as_of=วันที่เอกสาร) | — | ✓ | **snapshot ณ วันที่เอกสาร** (BR-08) · cost_center null = เว้น |
| รายการ (loop) | lines[] | 1 row = 1 line | ✓ | วันที่ · หมวด(HR Config) · รายละเอียด |
| จำนวนเงิน (ที่เบิก) | line.unit_price | `#,##0.00` | ✓ | ชิดขวา · ยอดที่ผู้เบิกกรอก |
| VAT (โหมด) | line.vat_mode | บวก 7% / รวมใน / ไม่คิด | ✓ | segmented none/add/included |
| ก่อนภาษี (net) | computed calcLineVat.netAmount | `#,##0.00` | ✓ | ฐานก่อน VAT ต่อรายการ |
| ภาษี 7% (ต่อรายการ) | computed calcLineVat.vatAmount | `#,##0.00` | ✓ | included = ถอด VAT ออกจากยอด |
| รวมรายการ (line total) | computed calcLineVat.lineTotal | `#,##0.00` | ✓ | net + vat (หรือ = ยอดที่กรอก เมื่อ included) |
| รวมเป็นเงิน (ก่อนภาษี) | totals().before | `#,##0.00` | ✓ | Σ net (single source `totals()`) |
| ภาษีมูลค่าเพิ่ม 7% | totals().vat | `#,##0.00` | ✓ | Σ vat ต่อรายการ |
| จำนวนเงินรวมทั้งสิ้น | totals().grand | `#,##0.00` | ✓ | before + vat |
| จำนวนเงิน (ตัวอักษร) | baht_text(grand_total) | ไทย | ✓ | `scripts/baht_text.py` |
| ผู้ลงนาม | DOA chain (snapshot) + ผู้เบิก + การเงิน | — | ✓ | ดู §2.1 |

### 2.1 ช่องลงนาม — DOA (สำคัญ · ไม่ hardcode tier)
- ช่องลงนาม = **ผู้เบิก** → **ผู้อนุมัติตามวงเงิน (slot ต่อลำดับจาก DOA resolve)** → **การเงิน**
- จำนวนช่อง "ผู้อนุมัติ" + ตำแหน่ง/ชื่อ = ผลจาก `GET /doa/resolve` ตาม **ยอดรวมทั้งสิ้น** (BR-04 · LK-1)
- **ห้ามพิมพ์กฎช่วงวงเงินตายตัวลงเอกสาร** (เช่น "<5,000 หัวหน้า / 5,000–50,000 ผจก.") — ช่วงวงเงินเป็น FREE ranges ตั้งค่าที่ DOA กลาง (F-DLG-001) เอกสารพิมพ์เฉพาะ "ช่องลงนามที่ระบบเลือกให้" เท่านั้น
- ตัวอย่างใน sample: ยอด 12,007.00 → resolve ได้ 2 ลำดับ (หัวหน้าสายงาน + ผู้จัดการแผนก) — **เป็นผลลัพธ์ mock ของ demo**, dev ผูกค่าจริงจาก DOA engine
- เอกสารสอดคล้อง tab "ลายเซ็น / อนุมัติ" ใน prototype (DOA timeline + sign progress)

## 3. กติกาคำนวณ (canonical — ตรง `calcLineVat` / `totals` ใน prototype)
- ต่อรายการ: `subtotal = qty × unit_price` (qty=1 เสมอในโดเมนนี้ · line = ยอดเดียว)
- `vat_mode='add'`   → `net = subtotal` · `vat = net × 0.07` · `line_total = net + vat`
- `vat_mode='included'` → `net(base) = subtotal − subtotal×0.07/1.07` · `vat = subtotal×0.07/1.07` · `line_total = subtotal`
- `vat_mode='none'`  → `net = subtotal` · `vat = 0` · `line_total = net`
- `รวมเป็นเงิน (before) = Σ net(base)` · `VAT = Σ vat` · `grand = before + VAT` (single source `totals()`)
- ปัด VAT/ยอดรวม ROUND_HALF_UP 2 ตำแหน่ง
- จำนวนเงินตัวอักษร: `scripts/baht_text.py <grand>` (เอ็ด/ยี่สิบ/ล้าน/สตางค์/ถ้วน)
- เพดานหมวด (HR Config resolve · effective_date) — เกินเพดาน = เตือน + ต้องมีเหตุผล (A-EXP-05 · ไม่ hard block) — ตรวจใน UI ก่อนออกเอกสาร ไม่แสดงบนเอกสาร

## 4. กติกาการพิมพ์ (ตาม Design Rules)
- A4 แนวตั้ง · lean type · หัวตารางแถบ navy เส้นบาง · ลายเซ็น + footer ชิดล่าง (`.doc-bottom`)
- หัวตารางซ้ำทุกหน้า (`thead{display:table-header-group}`) · ห้ามตัด row กลาง (`tr{break-inside:avoid}`)
- เลข/เงิน ชิดขวา `tabular-nums` `#,##0.00` · วันที่ พ.ศ. ทั้งใบ
- เลขผู้เสียภาษี + (สำนักงานใหญ่) บนหัวกระดาษ
- จำนวนเงิน = RESTRICTED — สำเนา (ENG-DOC-STORE) จัดเก็บผ่าน Policy Center (BR-10)

## 5. วิธี build ใหม่ (regenerate)
```bash
# Windows venv (PYTHONIOENCODING=utf-8)
.claude/venv/Scripts/python.exe .claude/skills/thai-doc-pdf-generator/scripts/build_html.py BODY.html --title "ใบเบิกค่าใช้จ่าย" -o expense_template.html
.claude/venv/Scripts/python.exe .claude/skills/thai-doc-pdf-generator/scripts/render_pdf.py expense_template.html -o expense_sample.pdf
```
Dev ฝั่งระบบ: ใช้ `expense_template.html` เป็นต้นแบบ HTML แล้ว bind ข้อมูลตาราง §2 → render PDF ด้วย engine ที่ honor `@page` + Sarabun (Chromium/Gotenberg/Puppeteer)

## 6. Checklist ก่อนส่งมอบ
- [x] A4 พอดี 1 หน้า ไม่ล้น (MediaBox 594.96×841.92 pt)
- [x] ตัวเลขชิดขวา + `#,##0.00`
- [x] VAT/ยอดรวม ถูกต้อง (11,300.00 + 707.00 = 12,007.00) + ตัวอักษรตรงยอด (หนึ่งหมื่นสองพันเจ็ดบาทถ้วน)
- [x] เลขผู้เสียภาษี + (สำนักงานใหญ่) บนหัวกระดาษ
- [x] ช่องลงนามครบ (ผู้เบิก + DOA slots + การเงิน) + วันที่
- [x] **ไม่มี** การพิมพ์กฎช่วงวงเงิน DOA ตายตัวเป็น business rule

## 7. ข้อมูลที่เป็น placeholder / mock ในตัวอย่าง (dev bind ค่าจริง)
- บริษัท/ที่อยู่/เลขผู้เสียภาษี `0105560012345 (สำนักงานใหญ่)` = placeholder มาตรฐาน 2BSimple
- เลขที่ `EXP-2569-0007` · วันที่ `31 สิงหาคม 2569` = ตัวอย่าง (จริงมาจาก doccfg ตอนอนุมัติ)
- ผู้เบิก `ธนากร พูนผล (EMP-1003) · ผู้จัดการขาย · ขาย · CC-SALES-01` = mock (มาจาก Employee + Movement snapshot)
- 4 รายการ + ยอด = mock demo (ครอบ VAT ทั้ง 3 โหมด: add / included / none)
- ตำแหน่งผู้อนุมัติ (หัวหน้าสายงาน / ผู้จัดการแผนก) = ผลลัพธ์ mock ของ DOA resolve — จริงจาก `GET /doa/resolve`
