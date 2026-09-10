# NTF_BRIEF — F-HR-EXPENSE · เบิกค่าใช้จ่าย
> ยิงผ่าน ENG-NOTIFY เท่านั้น · DOA events (doa_pending/result) มาอัตโนมัติ ไม่อยู่ในใบนี้

| Event ID | Trigger (อ้าง PREBRIEF) | ผู้รับ | ข้อความ template | Channel | ปิดได้ |
|---|---|---|---|---|---|
| expense_submitted | draft→submitted (S-01) | ผู้อนุมัติชั้นแรก | ใบเบิก **{doc_no|ยอด {total}}** จาก {employee} รออนุมัติ | in-app | ✓ |
| expense_result | pending→approved/rejected (S-01/S-06) | ผู้เบิก | ใบเบิก **{doc_no}** {ผล: อนุมัติ/ตีกลับ} {reason} | in-app+email | ✗ บังคับ |
| expense_over_cap | รายการเกินเพดานหมวด (S-03·BR-02) | ผู้เบิก | รายการ {category} เกินเพดาน **{cap}** — ต้องระบุเหตุผล | in-app | ✓ |
| expense_paid | sent_to_pay→paid (S-14·hook) | ผู้เบิก | ใบเบิก **{doc_no}** จ่ายแล้ว ({channel}) | in-app | ✓ |

## เพิ่มเข้า Event Catalog
- กลุ่มใหม่ "ค่าใช้จ่าย (expense_*)" — 4 event
## Dev wiring note
- ENG-NOTIFY.emit(event_id,{ref:doc_no, vars}) ที่ transition · expense_paid ยิงเมื่อ hook จ่ายกลับ (Payroll/Finance) ไม่ใช่ Expense ตัดสินเอง
