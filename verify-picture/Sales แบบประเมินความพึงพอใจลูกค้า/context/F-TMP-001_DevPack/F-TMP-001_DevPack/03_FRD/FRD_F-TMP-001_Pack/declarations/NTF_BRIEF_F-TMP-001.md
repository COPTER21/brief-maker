# NTF_BRIEF — F-TMP-001 แบบประเมินความพึงพอใจลูกค้า
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| cse_submitted | `draft → submitted (ผู้ประเมินกดส่งแบบประเมิน)` (03_LOGIC F-TMP-001-FN-05) | role-mgr-sales | ได้รับแบบประเมินความพึงพอใจ **{doc_no}** จาก {store_name} — คะแนนโดยรวม {overall} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบประเมินความพึงพอใจลูกค้า" — cse_submitted

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
