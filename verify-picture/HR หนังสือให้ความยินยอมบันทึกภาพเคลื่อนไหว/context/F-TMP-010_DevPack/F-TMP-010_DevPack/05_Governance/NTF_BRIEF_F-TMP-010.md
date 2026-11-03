# NTF_BRIEF — F-TMP-010 หนังสือให้ความยินยอมในการบันทึกและเผยแพร่ภาพถ่าย หรือภาพเคลื่อนไหว
> **FINAL — ยืนยันกับ FRD** · ntf-declaration v1.2 · Verdict **PASS**
> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode ช่องทาง · DOA events (doa_pending / doa_result / doa_escalate — เอกสารนี้ไม่มีสายอนุมัติ (DEC-03) จึงไม่มี event จาก DOA engine, imc_over_limit_approved (จาก suggest) — ตัดออก เอกสารไม่มีวงเงินและไม่มีการอนุมัติ) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้

| Event ID | Trigger | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| imc_consent_recorded | `S: draft → confirmed (ผู้ให้ความยินยอมยืนยันในระบบ · ระบบบันทึกวันที่ให้ความยินยอมและฉบับของหนังสือ)` (03_LOGIC F-TMP-010-FN-06) | role-mgr-hr | **{doc_no}** {subject_name} ให้ความยินยอมบันทึกและเผยแพร่ภาพแล้ว (บูธ {booth_location} ฉบับ {form_revision}) — บันทึกเป็นหลักฐานความยินยอมเรียบร้อย | in-app | ✓ |
| imc_consent_withdrawn | `S: confirmed → withdrawn (ถอนความยินยอมรายข้อหรือทั้งฉบับ · DEC-15)` (03_LOGIC F-TMP-010-FN-08) | role-mgr-hr, role-compliance | **{doc_no}** {subject_name} ถอนความยินยอม {withdrawn_scope} เมื่อ {withdrawn_at} — ต้องหยุดเผยแพร่ภาพส่วนที่ถอนทันที | in-app+email | ✗ บังคับ |
| imc_minor_consent_recorded | `ตอนยืนยัน พบว่าอายุผู้ให้ความยินยอมต่ำกว่าเกณฑ์ผู้เยาว์ใน config และมีผู้ปกครองรับรอง (DEC-04)` (03_LOGIC F-TMP-010-FN-06) | role-mgr-hr | **{doc_no}** {subject_name} เป็นผู้เยาว์ ({subject_age} ปี) — รับรองโดยผู้ปกครอง {guardian_name} ตรวจเอกสารยืนยันตัวตนผู้ปกครองก่อนใช้ภาพ | in-app | ✓ |
| imc_cancelled | `S: draft / pending → cancelled (ยกเลิกใบก่อนยืนยัน · DEC-07)` (03_LOGIC F-TMP-010-FN-09) | role-mgr-hr | **{doc_no}** ถูกยกเลิกโดย {actor} — {reason} | in-app | ✓ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
กลุ่ม "หนังสือให้ความยินยอมในการบันทึกและเผยแพร่ภาพถ่าย หรือภาพเคลื่อนไหว" — imc_consent_recorded, imc_consent_withdrawn, imc_minor_consent_recorded, imc_cancelled

## Dev wiring note
`ENG-NOTIFY.emit(event_id, {ref: <doc_id>, vars})` ที่ transition ตามตาราง — ห้ามเช็ค preference/ช่องทางเอง

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | N1–N7 | ผ่านทุกข้อ |
