# NTF_BRIEF — F-FIN-ACL ใบเคลียร์เงินทดรองจ่าย
> **FINAL v1.0 — ยืนยันกับ FRD_F-FIN-ACL_Pack (frd_lint Section N BLOCK 0)** · ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_pending / doa_result / doa_escalate) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้
> ทำแบบมือ — ntf-declaration ที่ติดตั้งไม่มี ntf_tool.py · trigger อ้าง FRD 03_LOGIC หลังขั้น 7

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| acl_cancelled | `pending_approval → cancelled` (03 FN-07/FN-09) | ผู้อนุมัติขั้นปัจจุบัน | **{doc_no}** ใบเคลียร์เงินทดรองจ่ายถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| acl_overspent_approved | `→ approved` และเหลือส่งคืน < 0 (03 FN-09) | role-finance-officer | **{doc_no}** เคลียร์แล้ว ใช้เกินเงินที่เบิก {over_amount} บาท — ต้องจ่ายคืนพนักงาน {requester} | in-app+email | ✗ บังคับ |
| acl_refund_due | `→ approved` และเหลือส่งคืน > 0 (03 FN-09) | role-finance-officer | **{doc_no}** เคลียร์แล้ว มีเงินคืนบริษัท {refund_amount} บาท — ตรวจรับเงินโอน | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY)
กลุ่มใหม่ "การเงิน · เงินทดรอง" (3 event ข้างบน)

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: acl_id, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference เอง · ไม่ประกาศ F187 (DEC-11: ประกาศ ✗)
