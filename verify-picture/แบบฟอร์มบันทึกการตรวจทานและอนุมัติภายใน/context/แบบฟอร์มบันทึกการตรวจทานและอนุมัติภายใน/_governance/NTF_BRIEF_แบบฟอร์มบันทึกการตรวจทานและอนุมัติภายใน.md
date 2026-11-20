# NTF_BRIEF — F-TMP-006 แบบฟอร์มบันทึกการตรวจทานและอนุมัติภายใน
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| irv_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-006-FN-07, F-TMP-006-FN-09) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| irv_approved_open_items | `→ approved และมีรายการบันทึกการตรวจทานที่สถานะ = เปิด หรือ กำลังดำเนินการ` (03_LOGIC F-TMP-006-FN-09) | requester | **{doc_no}** อนุมัติแล้ว — ยังมีข้อแก้ไขค้าง {count} รายการ กรุณาติดตามให้ปิด | in-app | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มบันทึกการตรวจทานและอนุมัติภายใน" — irv_cancelled, irv_approved_open_items

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
