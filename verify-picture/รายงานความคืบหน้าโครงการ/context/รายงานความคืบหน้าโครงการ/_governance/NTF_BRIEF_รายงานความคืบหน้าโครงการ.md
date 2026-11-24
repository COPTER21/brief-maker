# NTF_BRIEF — F-TMP-005 รายงานความคืบหน้าโครงการ
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| ppr_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-005-FN-07, F-TMP-005-FN-09) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| ppr_draft_for_pm | `draft บันทึกโดยผู้จัดทำที่ไม่ใช่ผู้จัดการโครงการ (กด "แจ้งผู้จัดการโครงการ") (DEC G3 · ส่งได้เฉพาะ PM)` (03_LOGIC F-TMP-005-FN-09, F-TMP-005-FN-11) | project_manager | **{doc_no}** รายงานความคืบหน้า {project_name} รอบ {period} พร้อมให้ตรวจและส่งอนุมัติ — จัดทำโดย {actor} | in-app | ✗ บังคับ |
| ppr_urgent_decision | `draft → pending_approval และ สรุปสถานะโครงการ = ล่าช้า หรือมีปัญหา` (03_LOGIC F-TMP-005-FN-04, F-TMP-005-FN-09) | role-gm, document_owner | **{doc_no}** โครงการ {project_name} สถานะ ล่าช้า หรือมีปัญหา — มีประเด็นที่ต้องการการตัดสินใจ {decision_count} เรื่อง | in-app+email | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "รายงานความคืบหน้าโครงการ" — ppr_cancelled, ppr_draft_for_pm, ppr_urgent_decision

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
