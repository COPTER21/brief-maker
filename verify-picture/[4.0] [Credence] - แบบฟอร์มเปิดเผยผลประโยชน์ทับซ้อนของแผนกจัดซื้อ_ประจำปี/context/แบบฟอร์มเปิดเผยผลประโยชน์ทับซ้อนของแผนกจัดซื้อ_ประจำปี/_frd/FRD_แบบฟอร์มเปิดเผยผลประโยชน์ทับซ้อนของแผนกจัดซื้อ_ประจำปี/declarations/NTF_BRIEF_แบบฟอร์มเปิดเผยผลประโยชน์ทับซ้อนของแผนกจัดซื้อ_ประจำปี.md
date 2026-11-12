# NTF_BRIEF — F-TMP-006 แบบฟอร์มเปิดเผยผลประโยชน์ทับซ้อนประจำปี
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| coi_conflict_declared | `draft → pending_approval โดยเลือก "มี" ผลประโยชน์ทับซ้อน — DEC-13/DEC-16 · ยิงครั้งเดียวต่อการส่ง` (03_LOGIC F-TMP-006-FN-05, F-TMP-006-FN-10 · 05 §5.6) | role-compliance | **{doc_no}** มีการเปิดเผยผลประโยชน์ทับซ้อน ประจำปี {disclosure_year} จาก {declarant_name} — เปิดดูรายละเอียดในระบบ | in-app | ✗ บังคับ |
| coi_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-006-FN-08, F-TMP-006-FN-10 · 05 §5.6) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มเปิดเผยผลประโยชน์ทับซ้อนประจำปี" — coi_conflict_declared, coi_cancelled

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
