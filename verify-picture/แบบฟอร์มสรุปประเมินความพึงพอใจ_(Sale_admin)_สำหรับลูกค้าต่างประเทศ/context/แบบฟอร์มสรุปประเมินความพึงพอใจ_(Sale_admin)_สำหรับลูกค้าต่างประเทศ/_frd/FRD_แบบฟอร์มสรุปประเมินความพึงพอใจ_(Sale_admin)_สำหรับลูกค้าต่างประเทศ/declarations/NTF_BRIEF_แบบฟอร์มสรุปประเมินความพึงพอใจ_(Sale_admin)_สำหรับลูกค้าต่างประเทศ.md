# NTF_BRIEF — F-TMP-007 แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าต่างประเทศ
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| ses_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-007-FN-06, F-TMP-007-FN-08) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| ses_low_score_approved | `→ approved และมีช่องคะแนน 1 หรือ 2 อย่างน้อย 1 ช่อง (weight ≤ 2 ตาม SalesConfig.sea_scale)` (03_LOGIC F-TMP-007-FN-05, F-TMP-007-FN-08) | owner, role-mgr-sales | **{doc_no}** สรุปความพึงพอใจลูกค้าต่างประเทศ เดือน {period_month} มี {low_count} ช่องที่ได้คะแนนต่ำ — ดูลูกค้า {low_customers} | in-app | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าต่างประเทศ" — ses_cancelled, ses_low_score_approved

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
