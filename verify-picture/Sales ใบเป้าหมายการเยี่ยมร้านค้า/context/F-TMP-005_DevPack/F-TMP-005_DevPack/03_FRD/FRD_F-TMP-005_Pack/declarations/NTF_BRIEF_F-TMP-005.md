# NTF_BRIEF — F-TMP-005 ใบเป้าหมายการเยี่ยมร้านค้า
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result, svt_over_limit_approved) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| svt_cancelled | `pending_approval → cancelled (เจ้าของหรือผู้จัดการฝ่ายขายยกเลิกระหว่างรออนุมัติ พร้อมเหตุผล)` (03_LOGIC F-TMP-005-FN-07, F-TMP-005-FN-09) | current_step_approver, ผู้สร้างเอกสาร | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| svt_plan_published | `pending_approval → approved (อนุมัติขั้นสุดท้าย) แจ้งผู้รับตามช่อง TO / CC` (03_LOGIC F-TMP-005-FN-09) | TO (to_recipient), CC (cc_recipients) | ใบเป้าหมายการเยี่ยมร้านค้า **{doc_no}** เขต {territory} รอบ {sales_cycle} อนุมัติแล้ว — {work_days} วัน · {total_customers} ร้าน | in-app+email | ✗ บังคับ |
| svt_superseded | `ใบใหม่ของเขต + รอบการขายเดียวกันอนุมัติ → ใบเดิม approved → superseded` (03_LOGIC F-TMP-005-FN-09) | ผู้สร้างเอกสาร, TO (to_recipient) | **{doc_no}** เขต {territory} รอบ {sales_cycle} ถูกแทนที่ด้วยใบ **{new_doc_no}** | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "ใบเป้าหมายการเยี่ยมร้านค้า" — svt_cancelled, svt_plan_published, svt_superseded

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
