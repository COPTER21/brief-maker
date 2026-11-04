# NTF_BRIEF — F-TMP-004 ใบกำหนดหน้าที่งานประจำตำแหน่ง (JD)
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_escalate, doa_pending, doa_result, jd_over_limit_approved) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| jd_cancelled | `pending_approval → cancelled (เจ้าของหรือ HR ยกเลิกระหว่างรออนุมัติ พร้อมเหตุผล)` (03_LOGIC F-TMP-004-FN-07, F-TMP-004-FN-09) | current_step_approver, ผู้สร้างเอกสาร | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |
| jd_ack_requested | `approved และ HR ระบุผู้ดำรงตำแหน่ง (acknowledged_by ถูกกำหนด)` (03_LOGIC F-TMP-004-FN-09, F-TMP-004-FN-10) | ผู้ดำรงตำแหน่งที่ระบุ | ใบกำหนดหน้าที่งาน **{doc_no}** ตำแหน่ง {position_name} อนุมัติแล้ว — กรุณาอ่านและกดรับทราบ | in-app+email | ✗ บังคับ |
| jd_acknowledged | `approved → acknowledged (ผู้ดำรงตำแหน่งกดรับทราบ)` (03_LOGIC F-TMP-004-FN-09, F-TMP-004-FN-11) | ผู้สร้างเอกสาร, role-mgr-hr | **{doc_no}** ตำแหน่ง {position_name} — ผู้ดำรงตำแหน่งรับทราบแล้ว | in-app | ✓ |
| jd_superseded | `ฉบับใหม่ของตำแหน่งเดียวกันอนุมัติ → ฉบับเดิม approved/acknowledged → superseded` (03_LOGIC F-TMP-004-FN-09) | ผู้สร้างเอกสาร, ผู้ดำรงตำแหน่งที่ระบุ | **{doc_no}** ตำแหน่ง {position_name} ถูกแทนที่ด้วยฉบับ **{new_doc_no}** | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "ใบกำหนดหน้าที่งานประจำตำแหน่ง (JD)" — jd_cancelled, jd_ack_requested, jd_acknowledged, jd_superseded

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
