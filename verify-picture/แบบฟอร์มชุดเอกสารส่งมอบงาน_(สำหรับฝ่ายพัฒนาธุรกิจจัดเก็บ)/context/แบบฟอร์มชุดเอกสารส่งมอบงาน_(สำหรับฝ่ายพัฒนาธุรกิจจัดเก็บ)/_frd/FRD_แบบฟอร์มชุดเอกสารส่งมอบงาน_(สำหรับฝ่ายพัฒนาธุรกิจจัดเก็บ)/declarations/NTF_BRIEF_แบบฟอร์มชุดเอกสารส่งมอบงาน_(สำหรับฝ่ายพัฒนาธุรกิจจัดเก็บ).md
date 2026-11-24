# NTF_BRIEF — F-TMP-007 แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายพัฒนาธุรกิจจัดเก็บ)
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| hob_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-007-FN-07, F-TMP-007-FN-09) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| hob_received_with_gaps | `→ approved และมีรายการเอกสารสถานะ = ขาดเอกสาร หรือ มีข้อจำกัด (หรือ สถานะข้อมูล ≠ สมบูรณ์)` (03_LOGIC F-TMP-007-FN-09) | requester | **{doc_no}** ฝ่ายบริหารการลงทุนรับมอบแล้ว — ยังมีเอกสารขาด/มีข้อจำกัด {count} รายการ กรุณาติดตามส่งเพิ่ม | in-app | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายพัฒนาธุรกิจจัดเก็บ)" — hob_cancelled, hob_received_with_gaps

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
