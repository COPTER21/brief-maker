# NTF_BRIEF — F-TMP-003 แบบฟอร์มการขอทำลายข้อมูล
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| drits_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-003-FN-06) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| drits_ready_for_it | `pending_approval → approved (DOA ครบทุกขั้น) — เข้าคิวงานทำลายข้อมูลของฝ่าย IT` (03_LOGIC F-TMP-003-FN-04) | role-it-officer | **{doc_no}** อนุมัติให้ทำลายข้อมูลแล้ว — โปรแกรม {program} ช่วง {period_from}–{period_to} | in-app | ✗ บังคับ |
| drits_destroyed | `approved → destroyed (เจ้าหน้าที่ IT กด บันทึกการทำลายแล้ว · บันทึก performed_by/performed_at)` (03_LOGIC F-TMP-003-FN-07) | owner | **{doc_no}** ทำลายข้อมูลเรียบร้อยแล้ว โดย {actor} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มการขอทำลายข้อมูล" — drits_cancelled, drits_ready_for_it, drits_destroyed

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
