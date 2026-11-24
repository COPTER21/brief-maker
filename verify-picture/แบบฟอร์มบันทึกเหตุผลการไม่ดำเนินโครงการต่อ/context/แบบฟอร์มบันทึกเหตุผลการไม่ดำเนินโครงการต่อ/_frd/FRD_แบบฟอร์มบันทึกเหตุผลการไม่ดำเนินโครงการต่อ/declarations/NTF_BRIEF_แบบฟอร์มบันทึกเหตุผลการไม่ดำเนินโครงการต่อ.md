# NTF_BRIEF — F-TMP-004 แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| pcl_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-004-FN-07, F-TMP-004-FN-09) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| pcl_followup_approved | `→ approved และสถานะการปิดโครงการ = 'ติดตามเงื่อนไขในอนาคต'` (03_LOGIC F-TMP-004-FN-09) | requester | **{doc_no}** อนุมัติแล้ว — โครงการ {project_name} อยู่ในสถานะติดตามเงื่อนไขในอนาคต: {future_followup} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ" — pcl_cancelled, pcl_followup_approved

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
