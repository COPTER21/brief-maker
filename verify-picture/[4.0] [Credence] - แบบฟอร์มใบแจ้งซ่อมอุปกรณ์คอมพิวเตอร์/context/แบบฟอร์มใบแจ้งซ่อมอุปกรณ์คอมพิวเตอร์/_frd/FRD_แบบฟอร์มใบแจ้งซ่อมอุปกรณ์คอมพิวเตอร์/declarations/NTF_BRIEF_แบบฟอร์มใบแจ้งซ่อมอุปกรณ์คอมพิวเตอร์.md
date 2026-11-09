# NTF_BRIEF — F-TMP-004 แบบฟอร์มใบแจ้งซ่อมอุปกรณ์คอมพิวเตอร์
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result, crr_over_limit_approved) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| crr_reported | `draft → reported (ผู้แจ้งซ่อมกด ส่งแจ้งซ่อม)` (03_LOGIC F-TMP-004-FN-03) | role-it-officer | **{doc_no}** แจ้งซ่อม {item_name} ({device_type}) — {problem} | in-app | ✗ บังคับ |
| crr_received | `reported → inspecting (เจ้าหน้าที่ IT กด รับแจ้ง · บันทึก received_by/received_at)` (03_LOGIC F-TMP-004-FN-04) | owner | **{doc_no}** เจ้าหน้าที่ IT {actor} รับแจ้งซ่อมแล้ว | in-app | ✓ |
| crr_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-004-FN-11) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| crr_repaired | `approved → repaired (เจ้าหน้าที่ IT บันทึกผลการซ่อม)` (03_LOGIC F-TMP-004-FN-09) | owner | **{doc_no}** บันทึกผลการซ่อมแล้ว: {repair_result} — กรุณารับทราบ | in-app | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มใบแจ้งซ่อมอุปกรณ์คอมพิวเตอร์" — crr_reported, crr_received, crr_cancelled, crr_repaired

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
