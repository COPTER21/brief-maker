# NTF_BRIEF — F-TMP-007 ใบคำร้องขอดำเนินการด้านเอกสาร
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| dar_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-007-FN-06) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| dar_distributed | `pending_approval → approved (DOA ครบทุกขั้น) — แจกจ่ายเอกสารควบคุมตามหน่วยงานที่เลือก` (03_LOGIC F-TMP-007-FN-04) | distribution_departments, distribution_emails | **{doc_no}** แจกจ่ายเอกสาร {target_doc_no} {target_doc_name} ({purpose}) มีผลบังคับใช้ {effective_date} — โปรดลงนามรับเอกสารควบคุม | in-app+email | ✗ บังคับ |
| dar_received | `approved → received (ลงนามรับเอกสารควบคุม)` (03_LOGIC F-TMP-007-FN-08) | owner, role-doc-controller | **{doc_no}** {receiver} ลงนามรับเอกสารควบคุมแล้ว | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "ใบคำร้องขอดำเนินการด้านเอกสาร" — dar_cancelled, dar_distributed, dar_received

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
