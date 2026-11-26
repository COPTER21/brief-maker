# NTF_BRIEF — F-TMP-003 แบบฟอร์มบันทึกการปิดงานและห้องข้อมูล
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| ivmk_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-003-FN-07, F-TMP-003-FN-09) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| ivmk_closed_handover | `pending_approval → approved (ขั้นสุดท้าย) — ปิดงานธุรกรรมสมบูรณ์` (03_LOGIC F-TMP-003-FN-05, F-TMP-003-FN-09) | post_close_owner, checklist_owners | **{doc_no}** {project_name} ปิดงานแล้ว — ผู้รับผิดชอบหลังปิดงาน: {post_owner} · เอกสารถาวรที่ {archive_location} | in-app+email | ✗ บังคับ |
| ivmk_lesson_assigned | `pending_approval → approved (ขั้นสุดท้าย) · ต่อแถวบทเรียนที่มีผู้รับผิดชอบ + กำหนดส่ง` (03_LOGIC F-TMP-003-FN-05, F-TMP-003-FN-09) | lesson_owner | **{doc_no}** มอบหมายติดตามบทเรียน: {topic} · กำหนดส่ง {due_date} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มบันทึกการปิดงานและห้องข้อมูล" — ivmk_cancelled, ivmk_closed_handover, ivmk_lesson_assigned

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
