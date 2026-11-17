# NTF_BRIEF — F-TMP-008 สรุปข้อมูลประเมินความพึงพอใจลูกค้า กลุ่ม MT
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result, mts_over_limit_approved) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| mts_low_channel | `draft → final (ยืนยันสรุป) และมีช่องทางสถานะ "ค่อนข้างต่ำกว่ามาตรฐาน" (% < SalesConfig.mt_csat_low_pct = 80) อย่างน้อย 1 ช่องทาง` (03_LOGIC F-TMP-008-FN-04, F-TMP-008-FN-08) | role-mgr-bu, admin_role | **{doc_no}** สรุปความพึงพอใจลูกค้า MT ครั้งที่ {round_no} — ช่องทางต่ำกว่า 80%: {far_channels} | in-app+email | ✗ บังคับ |
| mts_cancelled | `final → cancelled โดย Sales admin (ผู้ยกเลิกไม่ใช่เจ้าของ)` (03_LOGIC F-TMP-008-FN-05, F-TMP-008-FN-08) | owner | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "สรุปข้อมูลประเมินความพึงพอใจลูกค้า กลุ่ม MT" — mts_low_channel, mts_cancelled

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
