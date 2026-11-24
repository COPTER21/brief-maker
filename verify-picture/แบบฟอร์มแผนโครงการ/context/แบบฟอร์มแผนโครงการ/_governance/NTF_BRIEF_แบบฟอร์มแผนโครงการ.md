# NTF_BRIEF — F-TMP-004 แบบฟอร์มแผนโครงการ
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| pjp_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-004-FN-07, F-TMP-004-FN-09) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| pjp_budget_adjusted | `→ approved และ รวมงบที่ได้รับอนุมัติ ≠ รวมงบที่ขอ (DEC-04 · DEC-17)` (03_LOGIC F-TMP-004-FN-05, F-TMP-004-FN-09) | document_owner, project_manager | **{doc_no}** อนุมัติแล้ว งบที่ได้รับอนุมัติ {total_approved} บาท จากที่ขอ {total_requested} บาท | in-app+email | ✗ บังคับ |
| pjp_activity_delayed | `approved · สถานะกิจกรรมถูกอัปเดตเป็น Delayed (DEC-04 อัปเดตสถานะหลังอนุมัติ)` (03_LOGIC F-TMP-004-FN-09, F-TMP-004-FN-11) | project_manager, role-line-manager | **{doc_no}** กิจกรรม "{activity}" สถานะ Delayed — อัปเดตโดย {actor} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มแผนโครงการ" — pjp_cancelled, pjp_budget_adjusted, pjp_activity_delayed

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
