# 03_LOGIC — F-TMP-008
> ไม่มีสูตร/ค่าคงที่ตัวเลขบนกระดาษ · ตัวเลือกอ่านจาก master list (BR-08) · กติกาแนะนำผลการรับมอบอ่านจาก config (BR-07)

## §3.1 Functions (Scope-Local)
### F-TMP-008-FN-01: validateHandover
- Input `{project_name, sender_name, receiver_name, handover_at, package_version, handover_result, items[], open_issues, pending_docs, followup_schedule, ivm_remark}` → errors VR-01..10 (05 §5.4) · items ≥ 1 แถว (BR-09) · ต่อแถว: doc_name บังคับ · received = no ∧ completeness = complete → 422 (BR-02) · แถวไม่ใช่ (received = yes ∧ completeness = complete) → issue · fix_owner · due_date บังคับ (BR-03) · due_date ≥ date(handover_at) (BR-04) · handover_result = full → ทุกแถวครบ (BR-05) · conditional → open_issues + followup_schedule บังคับ · not_accepted → ivm_remark บังคับ (BR-06) · คืน `warnings[]` RESULT_NOT_SUGGESTED เมื่อ result ∈ {full, conditional} ≠ suggested (BR-07) ไม่บล็อก
### F-TMP-008-FN-02: computeRows
- `seq` = 1, 2, 3 … ต่อใบตามลำดับแถว (BR-01 · ลบแถวกลาง = รันใหม่ · ไม่ใช่ key) · received = no → completeness = incomplete (BR-02) · `suggested_result` = items ทุกแถวครบ ? full : conditional · `pending_count` = จำนวนแถวไม่ครบ · `earliest_due` = min(due_date ของแถวไม่ครบ)
### F-TMP-008-FN-03: attachFiles
- ผ่าน Document Center (ref_type='IVMF') · file_policy ≤20MB · pdf/doc/xls/รูป
### F-TMP-008-FN-04: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type IVMF (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('IVMF', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง + `header_snapshot` (Organization: ชื่อบริษัท โลโก้ บรรทัด "… และบริษัทในเครือ") · ห้าม format/+1 เอง
### F-TMP-008-FN-05: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-008` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง · role-mgr-bu = หัวหน้าหน่วยธุรกิจฝ่ายพัฒนาธุรกิจ (ฝ่ายผู้ส่งมอบ · รอยืนยัน OQ-03) · ผู้ resolve ได้ = ผู้จัดทำ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) + `approver_role` ต่อขั้น · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-008-FN-06: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved (คำตามบทบาท: role-line-manager = ตรวจสอบแล้ว · role-mgr-bu = รับทราบ) → ขั้นถัดไป pending หรือ (ขั้นสุดท้าย) status=approved · `approved_by`/`approved_at` → FN-09 render + `ENG-DOC-STORE.store(pdf,'IVMF',id,'approved_final')` → FN-10 ivmf_handover_followup (ถ้า handover_result ≠ full)
### F-TMP-008-FN-07: returnToDraft
- reject = "ส่งกลับ" (เหตุผลบังคับ) → audit "ส่งกลับ (ขั้น n)" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08 · BR-DOA-03 ตามปกติ)
### F-TMP-008-FN-08: cancelHandover
- owner หรือ admin role ฝ่ายบริหารการลงทุน · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending/waiting = skipped → FN-10 ivmf_cancelled (ถ้าเดิม pending)
### F-TMP-008-FN-09: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company{name, name_line, logo} · doc{title, no, is_draft, form_code, revision} · handover{project_name, sender_name, receiver_name, handover_at (dd/mm/พ.ศ. HH:mm น.), package_version, result (ป้ายไทย)} · items[] {seq, doc_name, doc_ref, received (ป้ายไทย), completeness (ป้ายไทย), issue, fix_owner, due_date (dd/mm/พ.ศ.)} เติมแถวว่าง (มีลำดับ) ถึง print_config.min_rows_by_group.items (12) · followup{open_issues, pending_docs, schedule, ivm_remark} · form_revisions[] จาก F-DOCCFG · sign_rows[] = ผู้จัดทำ + 1 ช่องต่อขั้นใน approval_chain snapshot — **จำนวนตามที่ตั้งใน DOA ไม่ fix** · คำตัดสินจาก print_config.decision_words.by_role[role_id] · layout.dense) → render logic-less 2 หน้า (R10 · parity กับ tpl_render.js)
### F-TMP-008-FN-10: emitEvents
- `ENG-NOTIFY.emit`: **ivmf_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · **ivmf_handover_followup** (→approved และ handover_result ∈ {conditional, not_accepted} → ผู้จัดทำ + admin role · payload project_name · handover_result · pending_count · earliest_due) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ · `ivmf.approved` ประกาศไว้ ไม่ยิงรอบนี้ (DEC-02)
### F-TMP-008-FN-11: listVisible
- canSee = admin ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · result = กรองตามผลการรับมอบ · ใบไม่มีสิทธิ์ → 404 · CSV ใช้ตัวกรองเดียวกัน

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
