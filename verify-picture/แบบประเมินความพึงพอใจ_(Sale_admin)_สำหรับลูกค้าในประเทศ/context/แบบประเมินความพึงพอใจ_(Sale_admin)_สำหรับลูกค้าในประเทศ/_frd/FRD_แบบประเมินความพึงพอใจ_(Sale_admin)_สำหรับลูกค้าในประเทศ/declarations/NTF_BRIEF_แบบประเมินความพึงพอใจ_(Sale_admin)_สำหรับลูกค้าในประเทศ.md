# NTF_BRIEF — F-TMP-004 แบบประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าในประเทศ
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result, sda_over_limit_approved) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| sda_low_score_recorded | `draft → recorded และมีข้ออย่างน้อย 1 ข้อได้ระดับ "น้อย" หรือ "ควรปรับปรุง" (≤ 2) (DEC-04 · เกินเกณฑ์ = เตือน ไม่บล็อก)` (03_LOGIC F-TMP-004-FN-06) | role-mgr-sales | **{doc_no}** ลูกค้า {customer_name} ให้ระดับต่ำ {low_count} ข้อ (เดือน {period_month}) — โปรดติดตาม | in-app | ✓ |
| sda_cancelled | `recorded → cancelled (ยกเลิกโดย admin role ที่ไม่ใช่เจ้าของ)` (03_LOGIC F-TMP-004-FN-05, F-TMP-004-FN-06) | document_owner | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "แบบประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าในประเทศ" — sda_low_score_recorded, sda_cancelled

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
