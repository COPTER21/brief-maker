# 03_LOGIC — F-TMP-005
> ไม่มีสูตร/ค่าคงที่ตัวเลขบนกระดาษ · ตัวเลือกอ่านจาก master list (BR-06) · เกณฑ์เตือนเลยกำหนดอ่านจาก config (BR-05)

## §3.1 Functions (Scope-Local)
### F-TMP-005-FN-01: validateLog
- Input `{project_name, questions[], issues[]}` → errors VR-01..08 (05 §5.4) · questions + issues รวม ≥ 1 แถว (BR-07) · ต่อแถวคำถาม: asked_date · question · asker · responder บังคับ · status ∈ {answered, closed} → answer บังคับ (BR-02) · due_date ≥ asked_date (BR-03) · ต่อแถวประเด็น: opened_date · issue · owner · due_date บังคับ · due_date ≥ opened_date (BR-03) · escalate = yes → remark บังคับ (BR-04) · คืน `warnings[]` OVERDUE_QUESTION / OVERDUE_ISSUE (BR-05) ไม่บล็อก
### F-TMP-005-FN-02: computeRows
- `q_no = 'Q-' + lpad(seq,3,'0')` · `oi_no = 'OI-' + lpad(seq,3,'0')` ต่อใบตามลำดับแถว (BR-01) · seq ต่อเนื่อง (ลบแถวกลาง = รันใหม่ · เลขไม่ใช่ key) · overdue = due_date < today ∧ status ∉ {answered, closed, ปิดแล้ว}
### F-TMP-005-FN-03: attachFiles
- ผ่าน Document Center (ref_type='IVMC') · file_policy ≤20MB · pdf/doc/xls/รูป
### F-TMP-005-FN-04: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-11): ตรวจ F-DOCCFG status ของ doc_type IVMC (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('IVMC', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง + `header_snapshot` (Organization: ชื่อบริษัท โลโก้ บรรทัด "… และบริษัทในเครือ") · ห้าม format/+1 เอง
### F-TMP-005-FN-05: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-005` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง · role-gm ตาม DOA · ผู้ resolve ได้ = ผู้จัดทำ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) + `approver_role` ต่อขั้น · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-005-FN-06: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved (คำตามบทบาท: role-line-manager = ตรวจสอบแล้ว · role-gm = อนุมัติ) → ขั้นถัดไป pending หรือ (ขั้นสุดท้าย) status=approved · `approved_by`/`approved_at` → FN-09 render + `ENG-DOC-STORE.store(pdf,'IVMC',id,'approved_final')` → FN-10 ivmc_log_approved (+ ivmc_escalation_flagged ถ้ามี escalate = yes)
### F-TMP-005-FN-07: returnToDraft
- reject (เหตุผลบังคับ) → audit "{คำปฏิเสธของขั้น} (ขั้น n)" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-09 · BR-DOA-03 ตามปกติ)
### F-TMP-005-FN-08: cancelLog
- owner หรือ admin role ฝ่ายบริหารการลงทุน · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending/waiting = skipped → FN-10 ivmc_cancelled (ถ้าเดิม pending)
### F-TMP-005-FN-09: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company{name, name_line, logo} · doc{title, no, is_draft, form_code, revision} · project{name} · questions[] {q_no, asked_date (dd/mm/พ.ศ.), question, asker, responder, answer, evidence, status (ป้ายไทย), due_date, remark} เติมว่าง (มีเลข Q-) ถึง print_config.min_rows_by_group.questions (14) · issues[] {oi_no, opened_date, issue, category, owner, priority (ป้ายไทย), due_date, status, escalate (ใช่/ไม่ใช่), remark} เติมว่างถึง 14 · form_revisions[] จาก F-DOCCFG · sign_rows[] = ผู้จัดทำ + 1 ช่องต่อขั้นใน approval_chain snapshot — **จำนวนตามที่ตั้งใน DOA ไม่ fix** · คำตัดสินจาก print_config.decision_words.by_role[role_id] · layout.dense) → render logic-less 2 หน้า (R10 · parity กับ tpl_render.js)
### F-TMP-005-FN-10: emitEvents
- `ENG-NOTIFY.emit`: **ivmc_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · **ivmc_log_approved** (→approved → ผู้รับผิดชอบตอบ/ผู้รับผิดชอบประเด็น ที่ map เป็นผู้ใช้ได้) · **ivmc_escalation_flagged** (→approved และมี escalate = yes ≥ 1 → role-gm) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ · `ivmc.approved` ประกาศไว้ ไม่ยิงรอบนี้ (DEC-02)
### F-TMP-005-FN-11: listVisible
- canSee = admin ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · late = มีคำถาม/ประเด็น overdue ≥ 1 · ใบไม่มีสิทธิ์ → 404 · CSV ใช้ตัวกรองเดียวกัน

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — `TODO: DOA engine` ฝั่ง prototype = MOCK_DOA_RESOLVED (DOA-ENGINE-HOOK) · ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,10 | FN-11 |
| 03 | FN-01, FN-02, FN-04 |
| 04 | FN-01, FN-02 |
| 05,06 | FN-05 |
| 07 | FN-06 (+FN-09, FN-10) / FN-07 |
| 08 | FN-08 (+FN-10) |
| 09 | FN-09 |
| 11 | FN-03 |
ทุก FN มี API ผูก ✓
