# BASELINE — Credit Note (F-ACC-CN) เทียบ ERP Standard
| # | ความสามารถ | SAP | Odoo | D365 | NetSuite | ระดับ | CUBE LITE |
|---|---|---|---|---|---|---|---|
| B-01 | ลดหนี้อ้างใบแจ้งหนี้ (reverse/partial) | ✓ | ✓ | ✓ | ✓ | Must | ✅ |
| B-02 | ลดบางส่วน/หลายรอบ + กันเกิน | ✓ | ✓ | ✓ | ✓ | Must | ✅ RULE-02/03 |
| B-03 | reason code | ✓ | ✓ | ✓ | ✓ | Must | ✅ master config |
| B-04 | อ้างใบรับคืน (return) | ✓ | ✓ | ✓ | ✓ | Must | ✅ SR mock |
| B-05 | อนุมัติก่อนออก (billing block/workflow) | ✓ (CMR) | ◐ | ✓ | ✓ | Must | ✅ DOA ตามมูลค่า |
| B-06 | ลด VAT ขายตามใบลดหนี้ | ✓ | ✓ | ✓ | ✓ | Must | ✅ BRD §12 |
| B-07 | ฟอร์มใบลดหนี้ตามกฎหมาย (อ้างใบเดิม+เหตุผล) | ✓TH | ✓TH | ✓ | ✓ | Must | ✅ pdfdoc ม.86/10 |
| B-08 | ลดหนี้ไม่อ้างใบ | ✓ | ✓ | ✓ | ✓ | Must | ⏭ ปิด OQ-CN-01 |
| B-09 | คืนเงินเมื่อชำระครบแล้ว (refund) | ✓ | ✓ | ✓ | ✓ | Must | ⏭ OQ-CN-03 (ไป RV/PV) |
| B-10 | ยกเลิก/กลับรายการ CN ที่ออกแล้ว | ✓ | ✓ | ✓ | ✓ | Should | ⏭ OQ-CN-02 |
Sources: [Odoo credit notes](https://www.odoo.com/documentation/19.0/applications/finance/accounting/customer_invoices/credit_notes.html) · [SAP CMR approval](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/4cef93946a0b48ec89533b3c34443b85/1755404abd5d43a3a8d71e951c277cf9.html) · [Revenue Code §86 (credit note)](https://library.siam-legal.com/thai-law/revenue-code-tax-invoice-debit-note-credit-note-section-86/)
