# NTF_BRIEF — F-TMP-009 แบบฟอร์มขอลงทะเบียนควบคุมสัญญา/เอกสารสำคัญ
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| ctr_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-009-FN-07, F-TMP-009-FN-10) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| ctr_registered | `approved → registered (ผู้ดูแลสัญญารับลงทะเบียน ระบบออกทะเบียนควบคุมเลขที่)` (03_LOGIC F-TMP-009-FN-08, F-TMP-009-FN-10) | requester | **{doc_no}** ลงทะเบียนควบคุมแล้ว เลขที่ **{register_no}** — กรุณาส่งต้นฉบับ/คู่ฉบับให้ผู้ดูแลสัญญา | in-app+email | ✗ บังคับ |
| ctr_original_received | `registered → completed (บันทึก ได้รับต้นฉบับ/คู่ฉบับ วันที่)` (03_LOGIC F-TMP-009-FN-08, F-TMP-009-FN-10) | requester | **{doc_no}** ผู้ดูแลสัญญาได้รับต้นฉบับ/คู่ฉบับแล้ว วันที่ {received_date} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มขอลงทะเบียนควบคุมสัญญา/เอกสารสำคัญ" — ctr_cancelled, ctr_registered, ctr_original_received

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
