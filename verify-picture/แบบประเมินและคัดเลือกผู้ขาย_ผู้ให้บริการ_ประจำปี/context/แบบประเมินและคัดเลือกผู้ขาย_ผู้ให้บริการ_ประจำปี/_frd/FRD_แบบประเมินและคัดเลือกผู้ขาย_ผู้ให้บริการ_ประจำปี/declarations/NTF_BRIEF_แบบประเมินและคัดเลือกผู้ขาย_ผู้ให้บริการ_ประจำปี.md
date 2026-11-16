# NTF_BRIEF — F-TMP-004 แบบประเมินและคัดเลือกผู้ขาย/ผู้ให้บริการ ประจำปี
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| vev_evaluation_failed | `draft → pending_approval โดยผลประเมิน = ไม่ผ่าน (คะแนนรวม < เกณฑ์ผ่าน) — DEC-13/DEC-14 · ยิงครั้งเดียวต่อการส่ง` (03_LOGIC F-TMP-004-FN-05, F-TMP-004-FN-10 · 05 §5.6) | role-mgr-pur, role-gm | **{doc_no}** ผู้ขาย/ผู้ให้บริการ {vendor_name} ไม่ผ่านการประเมิน (คะแนนรวม {score_total}/{max_total}) — ผู้จัดการฝ่ายจัดซื้อและผู้บริหารต้องพิจารณาคัดเลือก | in-app+email | ✗ บังคับ |
| vev_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-004-FN-08, F-TMP-004-FN-10 · 05 §5.6) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบประเมินและคัดเลือกผู้ขาย/ผู้ให้บริการ ประจำปี" — vev_evaluation_failed, vev_cancelled

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
