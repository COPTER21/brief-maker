# 03_LOGIC — F-TMP-001
> ไม่มีสูตร/ค่าคงที่บนกระดาษ (DEC-04) · ผู้อนุมัติไม่ hardcode — อ่านจาก DOA เท่านั้น (DEC-14)

## §3.1 Functions (Scope-Local)
### F-TMP-001-FN-01: validateInitiation
- Input `{txn, scope}` → errors VR-01..04 (05 §5.4) · responsible_id ต้องเป็นพนักงาน active ใน tenant (F-EMP-001)
### F-TMP-001-FN-02: snapshotParties
- snapshot ชื่อ/ตำแหน่งผู้จัดทำ และชื่อผู้รับผิดชอบ ลงเอกสาร (ป้องกันชื่อเปลี่ยนภายหลัง) · ทำฝั่ง server เสมอ
### F-TMP-001-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type IVMA (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('IVMA', company_ctx)` → `header_snapshot` (Organization: ชื่อบริษัท โลโก้) · สร้าง revision ฉบับ 00 "จัดทำครั้งแรก" · ห้าม format/+1 เอง
### F-TMP-001-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-001` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง · resolve ได้ = ผู้จัดทำ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) · ถ้ามี returned_* → เพิ่ม revision ฉบับถัดไป (detail = "แก้ไขตามที่ส่งกลับ: {returned_reason}") แล้วล้าง returned_* · status draft→pending ขั้น 1
### F-TMP-001-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved → ขั้นถัดไป pending หรือ status=approved (ครบ) → revision ล่าสุด approved_by = ผู้อนุมัติขั้นสุดท้าย → FN-08 render + `ENG-DOC-STORE.store(pdf,'IVMA',id,'approved_final')` → FN-09 ivma_responsible_assigned
### F-TMP-001-FN-06: returnToDraft
- reject (เหตุผลบังคับ) → audit "{คำปฏิเสธของ role} (ขั้น n)" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08 / BR-DOA-03)
### F-TMP-001-FN-07: cancelInitiation
- owner หรือ admin_role ของฝ่าย · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-09 ivma_cancelled (ถ้าเดิม pending)
### F-TMP-001-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company · doc{title,no,is_draft,form_code,revision} · txn{name, project_owner, source, type, start_date(ไทยเต็ม), responsible, internal_units, external_parties} · scope{objective, work_scope, deliverables, data_received, open_issues} · revisions[] (เติมว่างถึง print_config.min_rows) · sign_rows (ผู้จัดทำ + 1 แถวต่อขั้นใน approval_chain · คำตัดสินตาม print_config.decision_words.by_role) · layout.dense) → render template เดียวกับ FE (parity IDENTICAL) → A4 2 หน้า (R10)
### F-TMP-001-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **ivma_cancelled** (pending→cancelled → ผู้อนุมัติขั้นปัจจุบัน) · **ivma_responsible_assigned** (→approved → ผู้รับผิดชอบ + ผู้จัดทำ) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ · `ivma.approved` ประกาศไว้ ไม่ยิง (DEC-02)
### F-TMP-001-FN-10: listVisible
- canSee = admin_role ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · returned = draft ∧ returned_reason ไม่ว่าง · ใบไม่มีสิทธิ์ → 404

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,10 | FN-10 |
| 03 | FN-01, FN-02, FN-03 |
| 04 | FN-01, FN-02 |
| 05,06 | FN-04 |
| 07 | FN-05 (+FN-08, FN-09) / FN-06 |
| 08 | FN-07 (+FN-09) |
| 09 | FN-08 |
ทุก FN มี API ผูก ✓
