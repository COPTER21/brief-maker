# NTF_BRIEF — F-TMP-002 แบบสอบถามบุคลากรที่พ้นจากงาน (Exit Interview)
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| exi_submitted | `draft → submitted (ผู้ให้ข้อมูลหรือ HR กดส่งแบบสอบถาม)` (03_LOGIC F-TMP-002-FN-04, F-TMP-002-FN-09) | role-mgr-hr | แบบสอบถามพ้นจากงาน **{doc_no}** ส่งแล้ว — รอ HR รับทราบ | in-app | ✗ บังคับ |
| exi_cancelled | `submitted → cancelled (เจ้าของหรือ HR ยกเลิก พร้อมเหตุผล)` (03_LOGIC F-TMP-002-FN-07, F-TMP-002-FN-09) | role-mgr-hr, ผู้สร้างเอกสาร | แบบสอบถามพ้นจากงาน **{doc_no}** ถูกยกเลิก — เหตุผล: {reason} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบสอบถามบุคลากรที่พ้นจากงาน (Exit Interview)" — exi_submitted, exi_cancelled

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
