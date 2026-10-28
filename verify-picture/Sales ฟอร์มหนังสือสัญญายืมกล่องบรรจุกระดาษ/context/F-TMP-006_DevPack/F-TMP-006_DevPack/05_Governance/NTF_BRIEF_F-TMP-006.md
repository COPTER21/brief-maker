# NTF_BRIEF — F-TMP-006 หนังสือสัญญายืม
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result, loa_over_limit_approved) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| loa_cancelled | `pending_approval → cancelled` (03_LOGIC FN-09) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| loa_signed_copy_attached | `approved → แนบไฟล์หนังสือที่คู่สัญญาลงนามแล้วเข้าเอกสาร (G10 แนบไฟล์)` (03_LOGIC FN-12) | document_owner, role-mgr-sales | **{doc_no}** ได้รับหนังสือสัญญายืมที่ลงนามครบสองฝ่ายแล้ว — {attachment_name} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "หนังสือสัญญายืม" — loa_cancelled, loa_signed_copy_attached

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
