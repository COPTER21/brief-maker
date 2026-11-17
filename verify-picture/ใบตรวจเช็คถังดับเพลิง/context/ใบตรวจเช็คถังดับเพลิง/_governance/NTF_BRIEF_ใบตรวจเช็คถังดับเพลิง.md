# NTF_BRIEF — F-TMP-001 ใบตรวจเช็คถังดับเพลิง
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| fec_abnormal_found | `บันทึกแถวตรวจที่มีหัวข้อใดเป็น x = ผิดปกติ (DEC-04 · DEC-13)` (03_LOGIC F-TMP-001-FN-07) | role-mgr-wh | **{doc_no}** พบถังดับเพลิงผิดปกติที่ {location} ({abnormal_items}) วันที่ {check_date} — ติดต่อผู้จำหน่ายเพื่อแก้ไข | in-app+email | ✗ บังคับ |
| fec_cancelled | `active → cancelled` (03_LOGIC F-TMP-001-FN-07) | role-mgr-wh | **{doc_no}** ใบตรวจเช็คถังดับเพลิง ({location}) ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "ใบตรวจเช็คถังดับเพลิง" — fec_abnormal_found, fec_cancelled

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
