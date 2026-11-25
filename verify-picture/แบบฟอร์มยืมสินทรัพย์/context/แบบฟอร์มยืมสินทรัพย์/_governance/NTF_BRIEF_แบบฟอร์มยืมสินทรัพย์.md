# NTF_BRIEF — F-TMP-002 แบบฟอร์มยืมสินทรัพย์
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| aln_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-002-FN-07, F-TMP-002-FN-09) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| aln_returned | `approved → returned (ผู้รับคืนบันทึกรับคืนครบทุกรายการ)` (03_LOGIC F-TMP-002-FN-09, F-TMP-002-FN-11) | document_owner | **{doc_no}** รับคืนสินทรัพย์ครบแล้ว โดย {actor} วันที่ {returned_at} | in-app | ✓ |
| aln_overdue | `สถานะ approved และวันนี้ > วันที่ส่งคืนของรายการใด (งานตรวจรายวัน · DEC-04 เลยกำหนด = เตือน)` (03_LOGIC F-TMP-002-FN-09) | document_owner, role-mgr-acc | **{doc_no}** เลยกำหนดส่งคืนสินทรัพย์ {asset_code} ({due_date}) — กรุณาส่งคืน | in-app+email | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มยืมสินทรัพย์" — aln_cancelled, aln_returned, aln_overdue

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
