# NTF_BRIEF — F-TMP-001 แบบฟอร์มใบแจ้งซ่อมสินทรัพย์
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| rpr_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-001-FN-07, F-TMP-001-FN-09) | current_step_approver | **{doc_no}** ใบแจ้งซ่อมสินทรัพย์ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| rpr_ready_for_repair | `→ approved` (03_LOGIC F-TMP-001-FN-05, F-TMP-001-FN-09) | admin_role | **{doc_no}** ใบแจ้งซ่อมสินทรัพย์อนุมัติแล้ว {item_count} รายการ จาก {requester} ({dept}) — ดำเนินการซ่อม | in-app | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มใบแจ้งซ่อมสินทรัพย์" — rpr_cancelled, rpr_ready_for_repair

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
