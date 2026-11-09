# NTF_BRIEF — F-TMP-002 แบบฟอร์มตรวจเช็คความเรียบร้อยห้อง Server
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| src_abnormal_found | `บันทึกแถวตรวจเช็คที่เข้าเกณฑ์เตือน (DEC-04): อุณหภูมินอก 18-27°C · ความชื้นนอก 40-55 %RH · ทะเบียนคุมเข้าออก = ไม่มี · อุปกรณ์ใด = ไม่ปกติ` (03_LOGIC F-TMP-002-FN-02, F-TMP-002-FN-08) | admin_role | **{doc_no}** ห้อง Server พบรายการผิดปกติวันที่ {check_date}: {detail} | in-app+email | ✗ บังคับ |
| src_submitted | `draft → submitted (ปิดรอบการตรวจเช็ค)` (03_LOGIC F-TMP-002-FN-04, F-TMP-002-FN-08) | admin_role | **{doc_no}** ปิดรอบตรวจเช็คห้อง Server แล้ว ({row_count} รายการ · ผิดปกติ {abnormal_count}) | in-app | ✓ |
| src_cancelled | `draft/submitted → cancelled (เจ้าของ หรือ admin role · ต้องมีเหตุผล)` (03_LOGIC F-TMP-002-FN-06, F-TMP-002-FN-08) | owner, admin_role | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มตรวจเช็คความเรียบร้อยห้อง Server" — src_abnormal_found, src_submitted, src_cancelled

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
