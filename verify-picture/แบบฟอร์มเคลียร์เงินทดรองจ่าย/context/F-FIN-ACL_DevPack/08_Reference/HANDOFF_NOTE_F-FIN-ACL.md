# Handoff note — F-FIN-ACL ใบเคลียร์เงินทดรองจ่าย

## ถึงพี่เบิร์ด (ปิดก่อน dev)
1. role id `role-line-manager` · `role-finance-officer` · `role-finance-manager` ตรง master DOA ไหม (OQ-03)
2. Core มี `ExpensePolicy.advance_clear_due_day` + `Company.bank_accounts[purpose=advance_refund]` หรือยัง (OQ-04)
3. รหัส `ACL` ชน doc_type อื่นใน F003 ไหม (OQ-06)
4. อัป Google Sheet สถานะ H·B·F·Q

## ฝั่งลูกค้า (ก่อน UAT)
- OQ-02: Credence เซ็นยืนยัน DEC-03..11 (AI-DEFAULT) — ทำใบลงนาม NF-SO
- เปลี่ยน REQ-2569-0000 / F-FIN-ACL เป็นรหัสจริง

## ปรับสกิล
- thai-doc v2.1: เพิ่ม R9 `.form-grid` (ไฟล์ `07_Print/base_form_patch.css`)
- ติดตั้ง declaration ×4 รุ่นที่มี `*_tool.py`
