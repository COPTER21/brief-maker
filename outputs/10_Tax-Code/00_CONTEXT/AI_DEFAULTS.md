# Tax Code — AI Defaults และ Scope Lock

สถานะ: LOCKED สำหรับการสร้างเอกสารส่งต่อ AI Coding Agent  
วันที่: 2026-08-05  
Feature ID: F-TAX

## แหล่งข้อมูลหลัก

- `Pack Brief Feature/10_Tax-Code/PREBRIEF_F-TAX_TaxCode.md`
- `Pack Brief Feature/10_Tax-Code/_SEED_NOTES.md`
- `Pack Brief Feature/10_Tax-Code/TaxCode.html`
- `Central Plan v2/CENTRAL_PLAN_CORE_ERP.md` เป็นแหล่งจริงของ graph และ global contracts
- `Central Plan v2/CUBE_Core_ERP.html` และ `Central Plan v2/WAVE_PLAN_CORE_ERP.html` เป็น derived views; ตัวเลขที่เก่ากว่าไม่ override central plan

## AI Defaults ที่อนุมัติแล้ว

1. `[AI-DEFAULT]` Tax Code แยกตามบริษัท และรหัส unique แบบ case-insensitive ภายในบริษัทเดียวกัน
2. `[AI-DEFAULT]` หน้า UI ทำงานใน current-company context โดยไม่ให้เปลี่ยนบริษัทในฟอร์ม
3. `[AI-DEFAULT]` GL lookup รับเฉพาะบัญชีของบริษัทปัจจุบันที่ `status=active` และ `posting_allowed=true`
4. `[AI-DEFAULT]` VAT รองรับ `STANDARD`, `ZERO_RATED`, `EXEMPT` และทิศทางขาย/ซื้อ/ทั้งคู่ พร้อมสำรอง `vat_report_category`
5. `[AI-DEFAULT]` WHT เก็บ income category; แบบ ภ.ง.ด. resolve ที่ payment/reporting จากประเภทผู้รับเงินและบริบทการจ่าย ไม่ hardcode ที่ Tax Code
6. `[AI-DEFAULT]` AP อาจเสนอ WHT แต่ Payment Voucher เป็นจุดยืนยันรายการหัก; WHT report อ่านจาก payment result
7. `[AI-DEFAULT]` picker ใช้วันที่เอกสาร ไม่ใช้วันที่ระบบ และบันทึก immutable tax snapshot ลงเอกสาร
8. `[AI-DEFAULT]` ไม่มี hard delete ทุกกรณี; ใช้ deactivate หรือ archive พร้อม append-only audit
9. `[AI-DEFAULT]` อัตราของรหัสที่ถูกใช้แล้วแก้ไม่ได้ การเปลี่ยนอัตราต้องสร้าง replacement code และเก็บ lineage
10. `[AI-DEFAULT]` permissions: `tax_code.view/create/update/activate/deactivate/view_audit`
11. `[AI-DEFAULT]` production route: `/accounting/setup/tax-codes`; prototype route: `TaxCode.html#/accounting/setup/tax-codes`

## Out of Scope

- ค่าเริ่มต้น Tax Code รายชนิดเอกสาร
- Incoming WHT / หนังสือรับรองภาษีหัก ณ ที่จ่ายฝั่งรับ
- การยื่นแบบหรือเชื่อมต่อกรมสรรพากรโดยตรง
- การสร้างเอกสาร PDF; feature นี้เป็น master/configuration จึงข้าม `thai-doc-pdf-generator`

