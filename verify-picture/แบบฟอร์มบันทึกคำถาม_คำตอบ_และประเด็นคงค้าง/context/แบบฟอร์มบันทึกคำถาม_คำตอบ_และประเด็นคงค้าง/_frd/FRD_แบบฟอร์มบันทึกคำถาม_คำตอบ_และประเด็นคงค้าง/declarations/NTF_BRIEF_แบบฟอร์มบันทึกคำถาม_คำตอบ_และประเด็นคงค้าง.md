# NTF_BRIEF — F-TMP-005 แบบฟอร์มบันทึกคำถาม คำตอบ และประเด็นคงค้าง
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| ivmc_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-005-FN-08, F-TMP-005-FN-10) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| ivmc_escalation_flagged | `pending_approval → approved (ขั้นสุดท้าย) และมีประเด็นคงค้าง ต้องยกระดับ = ใช่ ≥ 1 แถว` (03_LOGIC F-TMP-005-FN-06, F-TMP-005-FN-10) | role-gm | **{doc_no}** {project_name} — มีประเด็นคงค้างที่ต้องยกระดับ {escalate_count} รายการ | in-app | ✗ บังคับ |
| ivmc_log_approved | `pending_approval → approved (ขั้นสุดท้าย) — บันทึกคำถาม/ประเด็นคงค้างมีผล` (03_LOGIC F-TMP-005-FN-06, F-TMP-005-FN-10) | question_responders, issue_owners | **{doc_no}** {project_name} — บันทึกอนุมัติแล้ว · มีรายการที่คุณรับผิดชอบ {item_count} รายการ กำหนดแรก {first_due} | in-app+email | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มบันทึกคำถาม คำตอบ และประเด็นคงค้าง" — ivmc_cancelled, ivmc_escalation_flagged, ivmc_log_approved

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
