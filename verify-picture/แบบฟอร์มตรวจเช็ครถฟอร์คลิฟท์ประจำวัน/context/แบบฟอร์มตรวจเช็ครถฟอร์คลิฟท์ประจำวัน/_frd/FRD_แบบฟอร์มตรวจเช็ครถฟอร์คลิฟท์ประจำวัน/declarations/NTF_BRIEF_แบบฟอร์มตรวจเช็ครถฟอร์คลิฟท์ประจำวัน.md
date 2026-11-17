# NTF_BRIEF — F-TMP-002 แบบฟอร์มตรวจเช็ครถฟอร์คลิฟท์ประจำวัน
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result, fli_over_limit_approved) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| fli_defect_found | `บันทึกผลตรวจรายวันที่มีอย่างน้อย 1 ช่องเป็น ✗ (ผิดปกติ/ต้องแก้ไข) — DEC-16 · ยิงครั้งเดียวต่อวันต่อใบ` (03_LOGIC F-TMP-002-FN-04, F-TMP-002-FN-10 · 05 §5.6) | role-supervisor | **{doc_no}** พบรายการผิดปกติ {defect_count} รายการ ({items}) วันที่ {day} — {vehicle_type} · โปรดตรวจสอบก่อนใช้งานรถ | in-app+email | ✗ บังคับ |
| fli_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-002-FN-08, F-TMP-002-FN-10 · 05 §5.6) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มตรวจเช็ครถฟอร์คลิฟท์ประจำวัน" — fli_defect_found, fli_cancelled

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
