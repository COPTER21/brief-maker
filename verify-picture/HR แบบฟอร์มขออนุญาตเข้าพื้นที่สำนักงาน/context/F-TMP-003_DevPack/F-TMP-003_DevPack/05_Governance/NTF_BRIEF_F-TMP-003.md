# NTF_BRIEF — F-TMP-003 แบบฟอร์มขออนุญาตเข้าพื้นที่สำนักงาน
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result, var_over_limit_approved) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| var_cancelled | `submitted → cancelled (เจ้าของหรือ HR ยกเลิกระหว่างรอพิจารณา พร้อมเหตุผล)` (03_LOGIC F-TMP-003-FN-06, F-TMP-003-FN-08) | ผู้อนุมัติขั้นปัจจุบัน, ผู้สร้างเอกสาร | คำขอเข้าพื้นที่สำนักงาน **{doc_no}** ถูกยกเลิก — เหตุผล: {reason} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มขออนุญาตเข้าพื้นที่สำนักงาน" — var_cancelled

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
