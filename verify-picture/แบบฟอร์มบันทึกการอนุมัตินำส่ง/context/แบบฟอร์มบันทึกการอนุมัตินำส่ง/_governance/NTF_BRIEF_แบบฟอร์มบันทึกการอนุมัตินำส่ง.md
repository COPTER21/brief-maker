# NTF_BRIEF — F-TMP-010 แบบฟอร์มบันทึกการอนุมัตินำส่ง
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| ivmh_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-010-FN-07, F-TMP-010-FN-09) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| ivmh_conditional_approved | `pending_approval → approved (ขั้นสุดท้าย) และมีขั้นใดผลการพิจารณา = อนุมัติแบบมีเงื่อนไข` (03_LOGIC F-TMP-010-FN-05, F-TMP-010-FN-09) | requester, admin_role | **{doc_no}** {project_name} — อนุมัติแบบมีเงื่อนไข {condition_count} ข้อ · ต้องดำเนินการตามเงื่อนไขก่อนนำส่ง | in-app+email | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มบันทึกการอนุมัตินำส่ง" — ivmh_cancelled, ivmh_conditional_approved

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
