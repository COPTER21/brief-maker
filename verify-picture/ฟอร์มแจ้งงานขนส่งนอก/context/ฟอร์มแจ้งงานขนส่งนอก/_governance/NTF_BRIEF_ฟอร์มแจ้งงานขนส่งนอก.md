# NTF_BRIEF — F-TMP-003 ฟอร์มแจ้งงานขนส่งนอก
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| otn_submitted | `draft → submitted (ผู้จัดทำกด "ส่งแจ้งงาน")` (03_LOGIC F-TMP-003-FN-06) | role-mgr-sales | **{doc_no}** แจ้งงานขนส่งนอก {carrier_name} รอบวันที่ {round_date} — {line_count} รายการ | in-app | ✓ |
| otn_early_delivery_date | `draft → submitted และมีแถวที่ วันที่นัดส่ง ก่อน รอบวันที่ (DEC-04/DEC-13 เตือน ไม่บล็อก)` (03_LOGIC F-TMP-003-FN-06) | role-mgr-sales | **{doc_no}** มี {count} รายการที่วันที่นัดส่งก่อนรอบวันที่ {round_date} — โปรดตรวจสอบ | in-app | ✓ |
| otn_cancelled | `submitted → cancelled (ยกเลิกโดย admin role ที่ไม่ใช่เจ้าของ)` (03_LOGIC F-TMP-003-FN-05, F-TMP-003-FN-06) | document_owner | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "ฟอร์มแจ้งงานขนส่งนอก" — otn_submitted, otn_early_delivery_date, otn_cancelled

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
