# NTF_BRIEF — F-TMP-005 แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| ivm_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-005-FN-07, F-TMP-005-FN-09) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| ivm_approved_open_conditions | `→ approved และมีเอกสาร/เงื่อนไขประกอบที่สถานะยังไม่ 'แล้วเสร็จ'` (03_LOGIC F-TMP-005-FN-09) | requester | **{doc_no}** อนุมัติแล้ว — โครงการ {project_name} ยังมีเอกสาร/เงื่อนไขประกอบค้าง {open_count} รายการ | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน" — ivm_cancelled, ivm_approved_open_conditions

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
