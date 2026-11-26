# 03_LOGIC — F-TMP-010
> ไม่มีสูตร/ค่าคงที่ตัวเลขบนกระดาษ · ตัวเลือกอ่านจาก master list (BR-01/06) · จำนวนขั้นมาจาก DOA กลาง (ไม่ fix)

## §3.1 Functions (Scope-Local)
### F-TMP-010-FN-01: validateRequest
- Input `{project_name, subject, supporting_docs, authority_level, ivm_proposal, proposed_conditions}` → errors VR-01/02 (05 §5.4) · authority_level ∈ ivmh.authority_level_options (BR-01) · proposed_conditions ไม่บังคับ
### F-TMP-010-FN-02: attachFiles
- ผ่าน Document Center (ref_type='IVMH') · file_policy ≤20MB · pdf/doc/xls/รูป
### F-TMP-010-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type IVMH (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('IVMH', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง + `header_snapshot` (Organization: ชื่อบริษัท โลโก้ บรรทัด "… และบริษัทในเครือ") · ห้าม format/+1 เอง
### F-TMP-010-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-010&authority_level=…` → steps (ไม่มีวงเงิน · ระดับ dmd = 2 ขั้น · md = 3 ขั้น — ค่าตั้งที่ DOA กลาง) · role-line-manager = ผู้บังคับบัญชาตามผัง · role-gm ขั้น 2 = รองกรรมการผู้จัดการ · role-gm ขั้น 3 = กรรมการผู้จัดการ / ผู้มีอำนาจ (รอยืนยัน OQ-03) · ผู้ resolve ได้ = ผู้จัดทำ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) + `approver_role` ต่อขั้น · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-010-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · decision ∈ {approve, approve_cond, ack} = ผ่านขั้น: ack เฉพาะขั้นกลาง (BR-05) · approve_cond ต้องมี instruction (BR-04) → ขั้นนั้น approved + decision + instruction + decided_at + position snapshot → ขั้นถัดไป pending หรือ (ขั้นสุดท้าย) status=approved · `approved_by`/`approved_at` → FN-08 render + `ENG-DOC-STORE.store(pdf,'IVMH',id,'approved_final')` → FN-09 ivmh_conditional_approved (ถ้ามีขั้น approve_cond)
### F-TMP-010-FN-06: returnToDraft
- decision ∈ {revise, reject} (ให้แก้ไข / ไม่อนุมัติ · instruction บังคับ) → audit "ให้แก้ไข / ไม่อนุมัติ (ขั้น n)" + returned_by/at/decision/instruction · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08 · on_reject back_to_draft · BR-DOA-03 ตามปกติ)
### F-TMP-010-FN-07: cancelRequest
- owner หรือ admin role ฝ่ายบริหารการลงทุน · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending/waiting = skipped → FN-09 ivmh_cancelled (ถ้าเดิม pending)
### F-TMP-010-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company{name, name_line, logo} · doc{title, no, is_draft, form_code, revision} · approval{project_name, subject, supporting_docs, authority_level (ป้ายไทย), ivm_proposal, proposed_conditions} (ขึ้นบรรทัดใหม่ → " · ") · reviews[] {seq, reviewer_role, position, decision (ป้ายไทย), instruction, date (dd/mm/พ.ศ.), evidence} 1 แถวต่อขั้น approval_chain + เติมแถวป้ายขั้นตามกระดาษถึง print_config.min_rows_by_group.reviews (3) ด้วยผล "—" · form_revisions[] จาก F-DOCCFG · sign_rows[] = ผู้จัดทำ + 1 ช่องต่อขั้นใน approval_chain snapshot — **จำนวนตามที่ตั้งใน DOA ไม่ fix** · คำตัดสินจาก print_config.decision_words.by_role[role_id] · layout.dense) → render logic-less 2 หน้า (R10 · parity กับ tpl_render.js)
### F-TMP-010-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **ivmh_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · **ivmh_conditional_approved** (→approved และมีขั้น approve_cond → ผู้จัดทำ + admin role · payload project_name · condition_count) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ · `ivmh.approved` ประกาศไว้ ไม่ยิงรอบนี้ (DEC-02)
### F-TMP-010-FN-10: listVisible
- canSee = admin ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · กรองตามระดับอำนาจอนุมัติ · result (ผลการพิจารณาของใบ) = approved → approve / approve_cond · draft ถูกส่งกลับ → revise / reject · ใบไม่มีสิทธิ์ → 404 · CSV ใช้ตัวกรองเดียวกัน

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — `TODO: DOA engine` ฝั่ง prototype = MOCK_DOA_RESOLVED (DOA-ENGINE-HOOK) · ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,10 | FN-10 |
| 03 | FN-01, FN-03 |
| 04 | FN-01 |
| 05,06 | FN-04 |
| 07 | FN-05 (+FN-08, FN-09) / FN-06 |
| 08 | FN-07 (+FN-09) |
| 09 | FN-08 |
| 11 | FN-02 |
ทุก FN มี API ผูก ✓
