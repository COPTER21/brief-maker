# NTF_BRIEF — F-TMP-008 หนังสือยินยอมในการเก็บรวบรวม ใช้ และเปิดเผยข้อมูลส่วนบุคคล
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_pending / doa_result / doa_escalate — เอกสารนี้ไม่มีสายอนุมัติ (DEC-03) จึงไม่มี event จาก DOA engine, pdc_over_limit_approved (จาก suggest) — ตัดออก เอกสารไม่มีวงเงินและไม่มีการอนุมัติ) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| pdc_consent_recorded | `S: draft → confirmed (เจ้าของข้อมูลยืนยันความยินยอม · ระบบบันทึกวันที่ให้ความยินยอมและฉบับของหนังสือ)` (03_LOGIC F-TMP-008-FN-09) | role-mgr-hr | **{doc_no}** {subject_name} ให้ความยินยอมแล้ว (ฉบับ {form_revision}) — บันทึกเป็นหลักฐานความยินยอมเรียบร้อย | in-app | ✓ |
| pdc_consent_withdrawn | `S: confirmed → withdrawn (เจ้าของข้อมูลถอนความยินยอม · DEC-14)` (03_LOGIC F-TMP-008-FN-06, F-TMP-008-FN-09) | role-mgr-hr, role-compliance | **{doc_no}** {subject_name} ถอนความยินยอม {withdrawn_scope} เมื่อ {withdrawn_at} — ต้องหยุดประมวลผลข้อมูลส่วนที่ถอนทันที | in-app+email | ✗ บังคับ |
| pdc_sensitive_refused | `ตอนยืนยัน พบข้อ 1-5 (ข้อมูลอ่อนไหว ม.26) ที่เลือก "ไม่ยินยอม" อย่างน้อย 1 ข้อ (DEC-15)` (03_LOGIC F-TMP-008-FN-09) | role-mgr-hr | **{doc_no}** {subject_name} ไม่ยินยอมข้อมูลอ่อนไหว {refused_items} — ตรวจสอบผลต่อกระบวนการที่เกี่ยวข้องก่อนดำเนินการต่อ | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "หนังสือยินยอมในการเก็บรวบรวม ใช้ และเปิดเผยข้อมูลส่วนบุคคล" — pdc_consent_recorded, pdc_consent_withdrawn, pdc_sensitive_refused

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
