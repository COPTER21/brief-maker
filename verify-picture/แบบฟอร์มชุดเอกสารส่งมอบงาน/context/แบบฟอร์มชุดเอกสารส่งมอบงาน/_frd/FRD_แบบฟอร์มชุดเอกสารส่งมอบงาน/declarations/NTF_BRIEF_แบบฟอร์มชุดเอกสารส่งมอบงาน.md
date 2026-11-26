# NTF_BRIEF — F-TMP-008 แบบฟอร์มชุดเอกสารส่งมอบงาน
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| ivmf_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-008-FN-08, F-TMP-008-FN-10) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| ivmf_handover_followup | `pending_approval → approved (ขั้นสุดท้าย) และผลการรับมอบ = รับมอบแบบมีเงื่อนไข หรือ ยังไม่รับมอบ` (03_LOGIC F-TMP-008-FN-06, F-TMP-008-FN-10) | requester, admin_role | **{doc_no}** {project_name} — {handover_result} · รายการต้องส่งเพิ่ม {pending_count} รายการ · กำหนดส่งเร็วสุด {earliest_due} | in-app+email | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มชุดเอกสารส่งมอบงาน" — ivmf_cancelled, ivmf_handover_followup

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
