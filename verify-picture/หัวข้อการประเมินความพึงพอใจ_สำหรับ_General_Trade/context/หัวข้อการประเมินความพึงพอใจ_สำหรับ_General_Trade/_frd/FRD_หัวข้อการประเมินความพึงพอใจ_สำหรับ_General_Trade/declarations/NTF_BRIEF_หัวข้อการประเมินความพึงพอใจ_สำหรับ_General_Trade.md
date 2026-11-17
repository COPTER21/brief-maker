# NTF_BRIEF — F-TMP-002 หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| csm_cancelled | `pending_approval → cancelled` (03_LOGIC F-TMP-002-FN-07, F-TMP-002-FN-09) | current_step_approver | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| csm_low_csat | `→ approved และ overall_pct < SalesConfig.csat_bands[mid].min (60) — ผลแปลผล "ลูกค้าอาจมีความไม่พึงพอใจ"` (03_LOGIC F-TMP-002-FN-06, F-TMP-002-FN-09) | owner, role-mgr-sales | **{doc_no}** ผลประเมินความพึงพอใจ GT เดือน {period_month} โดยรวม {overall_pct}% — ลูกค้าอาจมีความไม่พึงพอใจ | in-app+email | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade" — csm_cancelled, csm_low_csat

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
