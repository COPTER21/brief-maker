# NTF_BRIEF — F-TMP-001 แบบสำรวจความพึงพอใจลูกค้า สำหรับลูกค้า General Trade
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| csg_low_score_recorded | `draft → recorded และมีข้ออย่างน้อย 1 ข้อได้คะแนน ≤ 2 (DEC-04 · เกินเกณฑ์ = เตือน ไม่บล็อก)` (03_LOGIC F-TMP-001-FN-06) | role-mgr-sales | **{doc_no}** ลูกค้า {customer_name} ให้คะแนนต่ำ {low_count} ข้อ (เดือน {period_month}) — โปรดติดตาม | in-app | ✓ |
| csg_cancelled | `recorded → cancelled (ยกเลิกโดย admin role ที่ไม่ใช่เจ้าของ)` (03_LOGIC F-TMP-001-FN-05, F-TMP-001-FN-06) | document_owner | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบสำรวจความพึงพอใจลูกค้า สำหรับลูกค้า General Trade" — csg_low_score_recorded, csg_cancelled

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
