# NTF_BRIEF — F-TMP-003 แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| acr_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-003-FN-07, F-TMP-003-FN-09) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| acr_ready_to_record | `→ approved (รอบันทึกเข้าระบบ)` (03_LOGIC F-TMP-003-FN-05, F-TMP-003-FN-09) | admin_role | **{doc_no}** อนุมัติแล้ว — ขอ{req_type_label}รหัสบัญชี รอบันทึกเข้าระบบ | in-app+email | ✗ บังคับ |
| acr_recorded | `approved → recorded` (03_LOGIC F-TMP-003-FN-09, F-TMP-003-FN-11) | owner | **{doc_no}** บันทึกเข้าระบบแล้วโดย {actor} เมื่อ {recorded_at} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี" — acr_cancelled, acr_ready_to_record, acr_recorded

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
