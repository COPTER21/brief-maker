# Tax Code — Decision Log (สืบทอดจากแชท Codex + cross-check กับ HTML)

สถานะ: GROUNDING DOC สำหรับ skill 5-9 (BRD → FRD → html-ui-brief → ai-testcase → qa-friendly)
วันที่ compile: 2026-08-05
Feature ID: F-TAX
แหล่ง: Codex session `rollout-2026-08-05T09-37-39-019fcfc8` (usage หมด — Claude ทำต่อ)
คู่กับ: [[AI_DEFAULTS.md]] (Scope Lock + 11 AI defaults)

> เอกสารนี้บันทึก **decision ที่คุยด้วยปากในแชท Codex แล้วต้อง cross-check ว่าลงไฟล์จริงหรือยัง** เพื่อกันเอกสาร downstream สืบทอดของที่ไม่ตรง HTML
> ทุกบรรทัดอ้าง (msg #) จากแชท + (L#) จาก `outputs/10_Tax-Code/01_HTML/TaxCode.html`

---

## A. กติกางาน (ยึดตลอด pipeline)

| # | กติกา | ที่มา |
|---|-------|-------|
| A1 | ใช้ **เฉพาะ skill ในลิสต์** — ห้าม plan-from-spec หรือ skill นอกลำดับ | msg #91 |
| A2 | ลำดับ skill: html-generator-v7 → thai-doc-pdf (ถ้ามี) → qc-ux → qc-coverage → brd-generator-full → frd-generator-v6 → html-ui-brief → ai-testcase-md-generator → qa-friendly-html-generator | msg #91 |
| A3 | artifact ทั้งหมดลง `outputs/10_Tax-Code/` — **ไม่เขียนทับ input** ที่ `Pack Brief Feature/10_Tax-Code/` | msg #106 |
| A4 | ไม่มี context ต้นทาง → เดินด้วย `[AI-DEFAULT]` + External Contract, ไม่สมมติว่าระบบอื่น implement แล้ว | msg #137, #148 |
| A5 | หยุดให้ user ตรวจทุกหัวเลี้ยว — ไม่ยิงรวด | msg #767, #778 |
| A6 | thai-doc-pdf-generator = **SKIP** (feature เป็น master/config ไม่มีเอกสารธุรกรรมของตัวเอง) | AI_DEFAULTS.md §Out of Scope |

---

## B. Feature overview (ตกลงแล้ว)

Tax Code = **Master Data กลาง** สำหรับ "รหัสภาษี" (VAT + WHT) ที่บริษัทใช้ ไม่ใช่ฟีเจอร์ที่จบในหน้าตัวเอง — เอกสารธุรกรรม/รายงานอื่นเรียกไปใช้ (msg #1460):

| Feature ที่เรียกใช้ | ใช้ Tax Code อย่างไร |
|---|---|
| เอกสารขาย (SO/AR Invoice) | เลือก VAT ขาย ตามวันที่เอกสาร → snapshot ลงเอกสาร |
| เอกสารซื้อ (PO/AP Invoice) | เลือก VAT ซื้อ; WHT = คำแนะนำ |
| ใบสำคัญจ่าย (Payment Voucher) | จุดยืนยัน WHT จริง |
| รายงานภาษี (VAT/WHT report) | อ่านจาก snapshot / payment result |

---

## C. Design decisions + cross-check กับ HTML

สถานะ: ✅ VERIFIED (ตรงกับ HTML แล้ว) · ⚠️ FLAG (ต้อง user ยืนยันก่อน BRD)

### C1 — ตารางแสดง "ช่วงวันมีผล" แยก 2 คอลัมน์ ✅
- **ขอ:** เพิ่มคอลัมน์ช่วงวันมีผล เพราะ list เห็นแค่ "พร้อมใช้วันนี้/ไม่พร้อม" ไม่เห็นวันที่ที่ใช้ตัดสิน (msg #1482, #1493)
- **HTML:** L2352 header มี `วันมีผลเริ่ม` + `วันมีผลสิ้นสุด` แยกกัน — ยืนยัน 8 คอลัมน์

### C2 — GL picker filter ตามทิศทาง/ตระกูล ✅ (+⚠️ 1 จุด)
- **ขอ:** ขาย → แสดงเฉพาะ GL ภาษีขาย · ซื้อ → เฉพาะ GL ภาษีซื้อ (เดิมแสดงทุก GL) (msg #1571)
- **HTML:** L2575 `glOptions('VAT_SALE')`, L2578 `glOptions('VAT_PURCHASE')`, L2581 `glOptions('WHT_PAYABLE')` + validation `isAllowedGL(...)` L2606-2609 บังคับ role ตรง
- **GL field แสดงตาม direction:** L2486-2494 (both→ทั้ง 2 field, sale→เฉพาะขาย, purchase→เฉพาะซื้อ)
- ⚠️ **FLAG-1:** msg #1571 ข้อ 2 เขียนว่า "GL ภาษีหัก ณ ที่จ่ายค้างจ่าย => เหมือนตอนนี้แสดงทุก GL" (กำกวม) แต่ HTML filter WHT เป็น `WHT_PAYABLE` เท่านั้น (สอดคล้อง AI_DEFAULT #3) — **ยืนยัน:** WHT picker ควร filter เฉพาะ WHT_PAYABLE (ตามที่ทำ) หรือแสดงทุก GL?

### C3 — เอา hint / ข้อความรก ออกจาก drawer ✅
- **ขอ:** เอา "ต้องผูกบัญชี GL ให้ครบก่อน... กดบันทึกร่าง" ออก · แยกคอลัมน์ที่ซ้อนบรรทัด · เอา hint ออก (ทั้ง 2 tab) รวม date-picker modal + view drawer (msg #1638, #1678)
- **HTML:** ไม่พบประโยค hint ในฟอร์ม/date modal (L2803-2813)/view drawer (L2690-2701) — hint ถูกย้ายไป ⓘ tooltip hover (L1302 `#33/#67`) ปุ่ม "บันทึกร่าง" ยังอยู่ (เป็น action ไม่ใช่ hint, L2540)

### C4 — validation เอา "(BR-xx)" ออกจากข้อความที่ user เห็น ✅
- **ขอ:** ลบ (BR-xx) ออกจาก validation (msg #1606)
- **HTML:** `BR-xx` เหลือเฉพาะ **code comment** (L2424, L2473) — ไม่มีในข้อความ user-facing

### C5 — แท็บ VAT/WHT ห่างจากตาราง + density ✅
- **ขอ:** แท็บ VAT/WHT ชิดตารางเกินไป (msg #1606)
- **HTML:** L1347 tab `height:36px; padding:2px 16px 0` (Pattern A density contract #63)

### C6 — CI/ขนาด (BA ติ "สีเพี้ยน + ใหญ่แปลก") ✅
- **ขอ:** ทำตาม html-generator-v7 ให้ตรง (msg #1725)
- **HTML:** เอา `color-mix()` ออกหมด (0 จุด); สี token จริง `#FF3B30`/`#FF9A1F`/`#111111` (L25-31); focus ring แดง CI `rgba(255,59,48,.10)` (L1029); density `--row-h:44px --fs-table:12.5px` (L1317-18) padding 8×12 (L1350); avatar VAT แดง→ส้ม / WHT charcoal→ส้ม (L1411-12)
- **Audit:** PREFLIGHT stamp (L2829-2837) self_audit PASS 26 counters=0, font=8, audit.sh FAIL=0 WARN=3 (locked base-kit)

---

## D. กติกาธุรกิจหลัก (จาก AI_DEFAULTS.md — จะเป็น business rules ใน BRD/FRD)

- D1 Tax Code แยกตามบริษัท, รหัส unique case-insensitive ในบริษัทเดียว (AI-DEFAULT #1)
- D2 หน้า UI ทำงานใน current-company context, เปลี่ยนบริษัทในฟอร์มไม่ได้ (#2)
- D3 GL lookup รับเฉพาะบัญชีบริษัทปัจจุบัน status=active + posting_allowed=true (#3) — HTML L2101
- D4 VAT: STANDARD/ZERO_RATED/EXEMPT + ทิศทาง ขาย/ซื้อ/ทั้งคู่ + vat_report_category (#4)
- D5 WHT เก็บ income category; แบบ ภ.ง.ด. resolve ที่ payment/reporting ไม่ hardcode (#5)
- D6 AP เสนอ WHT ได้ แต่ Payment Voucher = จุดยืนยันหัก; report อ่านจาก payment result (#6)
- D7 picker ใช้ **วันที่เอกสาร** ไม่ใช่วันที่ระบบ + บันทึก **immutable tax snapshot** ลงเอกสาร (#7)
- D8 **ไม่มี hard delete** — deactivate/archive + append-only audit (#8)
- D9 อัตราของรหัสที่ถูกใช้แล้ว **แก้ไม่ได้** — ต้องสร้าง replacement code + เก็บ lineage (#9)
- D10 permissions: `tax_code.view/create/update/activate/deactivate/view_audit` (#10)
- D11 route prod `/accounting/setup/tax-codes`; prototype `TaxCode.html#/accounting/setup/tax-codes` (#11)

## E. Out of Scope (ห้ามเผลอเติมใน BRD/FRD)

- ค่าเริ่มต้น Tax Code รายชนิดเอกสาร
- Incoming WHT / หนังสือรับรองภาษีหัก ณ ที่จ่ายฝั่งรับ
- การยื่นแบบ / เชื่อมต่อกรมสรรพากรโดยตรง
- การสร้างเอกสาร PDF (skip thai-doc-pdf-generator)

---

## F. Open flags

1. **FLAG-1 (C2): ✅ RESOLVED (user 2026-08-05)** — WHT GL picker filter **เฉพาะ `WHT_PAYABLE`** (ตามที่ HTML ทำอยู่ L2581/2609 + สอดคล้อง AI-DEFAULT#3). BRD/FRD ให้ระบุ WHT GL constrained = WHT_PAYABLE role เท่านั้น เช่นเดียวกับ VAT_SALE/VAT_PURCHASE.
2. **Gate re-run: ✅ DONE (2026-08-05)** — qc-ux (R2) = PASS 0 warning (render จริง 12 ภาพ ยืนยัน BA complaint แก้แล้ว, self_audit นับสด=stamp) · qc-coverage (R2) = PASS 28/28 (evidence R1 ยังอยู่ครบ, ไม่มี scope creep). Report: `02_QC/TaxCode_UX_CHECK_REPORT.md`, `02_QC/TaxCode_COVERAGE_REPORT.md`
