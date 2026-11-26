# NTF_BRIEF — F-TMP-009 แบบฟอร์มชุดเอกสารนำส่งและหลักฐานการนำส่ง
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| ivmg_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-009-FN-08, F-TMP-009-FN-11) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| ivmg_delivery_failed | `approved — บันทึกแถวหลักฐานการนำส่งที่สถานะการรับ = ส่งไม่สำเร็จ` (03_LOGIC F-TMP-009-FN-10, F-TMP-009-FN-11) | requester, admin_role | **{doc_no}** {project_name} — นำส่งไม่สำเร็จถึง {receiver} ({channel}) · {remark} | in-app+email | ✗ บังคับ |
| ivmg_dispatch_closed | `approved → closed (ปิดการนำส่ง)` (03_LOGIC F-TMP-009-FN-11, F-TMP-009-FN-13) | approval_chain, admin_role | **{doc_no}** {project_name} — ปิดการนำส่งแล้ว · รับแล้ว {received_count} รายการ | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มชุดเอกสารนำส่งและหลักฐานการนำส่ง" — ivmg_cancelled, ivmg_delivery_failed, ivmg_dispatch_closed

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
