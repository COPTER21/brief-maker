# NTF_BRIEF — F-TMP-006 รายงานการเข้า-ออก ห้อง server
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| sral_certify_pending | `บันทึกแถวการเข้าห้องใหม่ (สถานะแถว = รอรับรอง)` (03_LOGIC F-TMP-006-FN-02, F-TMP-006-FN-08) | admin_role | **{doc_no}** มีการเข้าห้อง server รอรับรอง: {visitor_name} ({in_date} {in_time}) — {purpose} | in-app | ✗ บังคับ |
| sral_overstay | `แถวที่ยังไม่บันทึกเวลาออก และอยู่ในห้องนานเกิน ServerRoomAccessConfig.max_stay_hours (ค่าเริ่ม 12 ชม.) — DEC-04 เตือนไม่บล็อก` (03_LOGIC F-TMP-006-FN-02, F-TMP-006-FN-08) | admin_role | **{doc_no}** {visitor_name} อยู่ในห้อง server เกิน {max_stay_hours} ชม. ยังไม่บันทึกเวลาออก | in-app+email | ✗ บังคับ |
| sral_submitted | `draft → submitted (ปิดรอบรายงาน)` (03_LOGIC F-TMP-006-FN-04, F-TMP-006-FN-08) | admin_role | **{doc_no}** ปิดรอบรายงานการเข้า-ออกห้อง server แล้ว ({row_count} รายการ) | in-app | ✓ |
| sral_cancelled | `draft/submitted → cancelled (เจ้าของ หรือ admin role · ต้องมีเหตุผล)` (03_LOGIC F-TMP-006-FN-06, F-TMP-006-FN-08) | owner, admin_role | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "รายงานการเข้า-ออก ห้อง server" — sral_certify_pending, sral_overstay, sral_submitted, sral_cancelled

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
