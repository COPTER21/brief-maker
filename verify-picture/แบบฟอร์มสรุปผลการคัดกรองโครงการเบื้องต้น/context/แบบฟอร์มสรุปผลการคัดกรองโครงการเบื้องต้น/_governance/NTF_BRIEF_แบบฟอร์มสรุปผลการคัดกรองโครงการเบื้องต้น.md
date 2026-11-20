# NTF_BRIEF — F-TMP-003 แบบฟอร์มสรุปผลการคัดกรองโครงการเบื้องต้น
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| scr_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-003-FN-07, F-TMP-003-FN-09) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| scr_not_proceed_approved | `→ approved และผลการพิจารณา = ไม่ดำเนินการต่อ` (03_LOGIC F-TMP-003-FN-09) | requester | **{doc_no}** อนุมัติแล้ว — ผลการพิจารณา ไม่ดำเนินการต่อ · จัดทำแบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ (FM-BDM-04) | in-app+email | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มสรุปผลการคัดกรองโครงการเบื้องต้น" — scr_cancelled, scr_not_proceed_approved

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
