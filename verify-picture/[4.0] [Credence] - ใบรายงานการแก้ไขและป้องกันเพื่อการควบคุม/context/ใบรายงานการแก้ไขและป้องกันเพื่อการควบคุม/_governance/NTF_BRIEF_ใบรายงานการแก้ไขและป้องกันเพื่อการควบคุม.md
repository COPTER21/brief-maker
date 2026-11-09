# NTF_BRIEF — F-TMP-008 ใบรายงานการแก้ไขและป้องกันเพื่อการควบคุม
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| car_cancelled | `in_review / pending_approval → cancelled` (03_LOGIC F-TMP-008-FN-11, F-TMP-008-FN-13) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| car_submitted_for_review | `draft → in_review (ผู้จัดทำกดส่งตรวจสอบ)` (03_LOGIC F-TMP-008-FN-04, F-TMP-008-FN-13) | role-ic-officer | **{doc_no}** รอตรวจสอบ — {subject} · กรอกช่วง "การตรวจสอบ" และลงนามตรวจสอบ | in-app | ✗ บังคับ |
| car_review_returned | `in_review → draft (ผู้ตรวจสอบส่งกลับแก้ไข · ล้างจุดลงนามตรวจสอบ)` (03_LOGIC F-TMP-008-FN-07, F-TMP-008-FN-13) | owner | **{doc_no}** ถูกส่งกลับแก้ไขโดย {actor} — {reason} | in-app | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "ใบรายงานการแก้ไขและป้องกันเพื่อการควบคุม" — car_cancelled, car_submitted_for_review, car_review_returned

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
