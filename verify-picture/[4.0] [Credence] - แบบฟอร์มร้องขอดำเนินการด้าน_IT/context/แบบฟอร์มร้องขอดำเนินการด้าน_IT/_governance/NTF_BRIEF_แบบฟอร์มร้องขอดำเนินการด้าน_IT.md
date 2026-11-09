# NTF_BRIEF — F-TMP-001 แบบฟอร์มร้องขอดำเนินการด้าน IT
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| itrs_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-001-FN-06) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| itrs_ready_for_it | `pending_approval → approved (DOA ครบทุกขั้น) — เข้าคิวงานฝ่าย IT` (03_LOGIC F-TMP-001-FN-04) | role-it-officer | **{doc_no}** {subject} อนุมัติแล้ว — ต้องการส่งมอบ {due_date} ที่ {delivery_location} | in-app | ✗ บังคับ |
| itrs_completed | `approved → completed (เจ้าหน้าที่ IT กด ดำเนินการแล้ว · บันทึก performed_by/performed_at)` (03_LOGIC F-TMP-001-FN-07) | owner | **{doc_no}** {subject} ดำเนินการเสร็จแล้ว โดย {actor} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มร้องขอดำเนินการด้าน IT" — itrs_cancelled, itrs_ready_for_it, itrs_completed

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
