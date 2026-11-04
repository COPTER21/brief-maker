# NTF_BRIEF — F-TMP-003 คำขอมีและใช้ลายเซ็นดิจิทัล (Digital Signature)
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| dsr_cancelled | `pending_approval → cancelled (ยกเลิกโดยเจ้าของหรือ admin role · DEC-08)` (03_LOGIC FN-09) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| dsr_name_change_requested | `draft → pending_approval เมื่อ case = change (กรณีที่ 3 ขอเปลี่ยนลายเซ็นดิจิทัลเพราะเปลี่ยนชื่อ/นามสกุล · DEC-13/DEC-14)` (03_LOGIC FN-13) | role-mgr-hr | **{doc_no}** {requester} ขอเปลี่ยนลายเซ็นดิจิทัลจากการเปลี่ยนชื่อ-นามสกุล — โปรดตรวจสอบทะเบียนพนักงานให้ตรงกัน | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "คำขอมีและใช้ลายเซ็นดิจิทัล (Digital Signature)" — dsr_cancelled, dsr_name_change_requested

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
