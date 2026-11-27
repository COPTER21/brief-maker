# NTF_BRIEF — F-TMP-011 แบบฟอร์มการบันทึกการยกระดับประเด็น
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| ivmi_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-011-FN-08, F-TMP-011-FN-10) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| ivmi_log_approved | `pending_approval → approved (ขั้นสุดท้าย) — บันทึกการยกระดับมีผล` (03_LOGIC F-TMP-011-FN-06, F-TMP-011-FN-10) | action_owners | **{doc_no}** {project_name} — บันทึกการยกระดับอนุมัติแล้ว · มีประเด็นที่คุณรับผิดชอบดำเนินการ {item_count} รายการ กำหนดส่งแรก {first_due} | in-app+email | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มการบันทึกการยกระดับประเด็น" — ivmi_cancelled, ivmi_log_approved

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
