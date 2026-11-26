# NTF_BRIEF — F-TMP-002 แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| ivmj_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-002-FN-07, F-TMP-002-FN-09) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| ivmj_result_recorded | `pending_approval → approved (ขั้นสุดท้าย) — ผลการพิจารณาถูกบันทึก` (03_LOGIC F-TMP-002-FN-05, F-TMP-002-FN-09) | project_owner, reason_owners | **{doc_no}** {project_name} — ผลการพิจารณา: {result} · ประเด็นติดตาม: {follow_up} | in-app+email | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ" — ivmj_cancelled, ivmj_result_recorded

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
