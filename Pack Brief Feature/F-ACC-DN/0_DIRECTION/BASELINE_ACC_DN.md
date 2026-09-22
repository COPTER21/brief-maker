# BASELINE — Debit Note ฝั่งซื้อ (F-ACC-DN) เทียบ ERP Standard
| # | ความสามารถ | SAP | Odoo | D365 | NetSuite | ระดับ | CUBE LITE |
|---|---|---|---|---|---|---|---|
| B-01 | ลดหนี้ผู้ขายอ้างใบตั้งหนี้ (subsequent credit / vendor refund) | ✓ | ✓ | ✓ | ✓ | Must | ✅ |
| B-02 | ลดบางส่วน/หลายรอบ + กันเกิน | ✓ | ✓ | ✓ | ✓ | Must | ✅ |
| B-03 | reason code | ✓ | ✓ | ✓ | ✓ | Must | ✅ master |
| B-04 | อ้างใบคืนสินค้า (return to vendor) | ✓ | ✓ | ✓ | ✓ | Must | ✅ RTV mock |
| B-05 | workflow อนุมัติ | ✓ | ◐ | ✓ | ✓ | Must | ✅ DOA ตามมูลค่า |
| B-06 | กลับภาษีซื้อ | ✓ | ✓ | ✓ | ✓ | Must | ✅ input_vat_line ติดลบ |
| B-07 | ฟอร์มอ้างใบเดิม + เหตุผล | ✓TH | ✓TH | ✓ | ✓ | Must | ✅ pdfdoc |
| B-08 | ลดหนี้ไม่อ้างใบ | ✓ | ✓ | ✓ | ✓ | Should | ⏭ OQ-DN-01 |
| B-09 | เรียกเงินคืนเมื่อจ่ายครบ | ✓ | ✓ | ✓ | ✓ | Should | ⏭ OQ-DN-03 |
Sources: ใช้ผลค้นหา S0.5 ของ AP Invoice (SAP MIRO subsequent credit · Odoo vendor bills/refunds) + [Revenue Code §86/10](https://library.siam-legal.com/thai-law/revenue-code-tax-invoice-debit-note-credit-note-section-86/) — ไม่ค้นเพิ่ม (เลนเดียวกัน)
