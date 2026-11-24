# NTF_BRIEF — F-TMP-008 แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายบริหารการลงทุนจัดเก็บ)
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| hoi_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-008-FN-07, F-TMP-008-FN-09) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| hoi_acknowledged_open_items | `→ approved และ ผลการรับมอบ ≠ รับมอบครบถ้วน (มีแถว ไม่ได้รับ / ไม่ครบถ้วน / ต้องตรวจสอบเพิ่มเติม)` (03_LOGIC F-TMP-008-FN-09) | requester | **{doc_no}** รับทราบแล้ว — ยังมีเอกสารต้องส่งเพิ่มเติม {count} รายการ กำหนดติดตาม {followup_date} | in-app | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายบริหารการลงทุนจัดเก็บ)" — hoi_cancelled, hoi_acknowledged_open_items

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
