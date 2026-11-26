# 03_LOGIC — F-TMP-002
> ไม่มีค่าคงที่/สูตรตัวเลขบนกระดาษ · ตัวเลือกผลการพิจารณาอ่านจาก master list (BR-05)

## §3.1 Functions (Scope-Local)
### F-TMP-002-FN-01: validateRecord
- Input `{project_name, owner_employee_id, proposed_date, stopped_at_step, reasons[], summary}` → errors VR-01..06 (05 §5.4) · ≥1 แถว selected=yes (BR-01) · แถว yes ต้องมี detail (BR-02) · result=continue_conditional ต้องมี instruction (BR-03) · proposed_date ≤ วันนี้
### F-TMP-002-FN-02: attachFiles
- ผ่าน Document Center (ref_type='IVMJ') · file_policy ≤20MB · pdf/doc/xls/รูป
### F-TMP-002-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type IVMJ (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('IVMJ', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง + `header_snapshot` (Organization: ชื่อบริษัท โลโก้ บรรทัด "… และบริษัทในเครือ") · ห้าม format/+1 เอง
### F-TMP-002-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-002` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง · role-gm ตาม DOA · ผู้ resolve ได้ = ผู้จัดทำ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) + `approver_role` ต่อขั้น · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-002-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved (คำตามบทบาท: role-line-manager = ตรวจสอบแล้ว · role-gm = อนุมัติ) → ขั้นถัดไป pending หรือ (ขั้นสุดท้าย) รับ `result`/`instruction` ที่ยืนยัน (BR-04 · audit ค่าเดิม→ใหม่ · BR-03) → status=approved · `approved_by`/`approved_at` → FN-08 render + `ENG-DOC-STORE.store(pdf,'IVMJ',id,'approved_final')` → FN-09 ivmj_result_recorded
### F-TMP-002-FN-06: returnToDraft
- reject (เหตุผลบังคับ) → audit "{คำปฏิเสธของขั้น} (ขั้น n)" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08 · BR-DOA-03 ตามปกติ)
### F-TMP-002-FN-07: cancelRecord
- owner หรือ admin role ฝ่ายบริหารการลงทุน · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending/waiting = skipped → FN-09 ivmj_cancelled (ถ้าเดิม pending)
### F-TMP-002-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company{name, name_line, logo} · doc{title, no, is_draft, form_code, revision} · project{name, owner} · proposed_date (วันที่ไทยเต็ม) · stopped_at_step · authority_name (ผู้พิจารณาขั้นสุดท้าย) · reasons[] (selected = "ใช่"/"ไม่ใช่" · เติมว่างถึง print_config.min_rows) · summary{reason, supporting_docs, result(ป้ายไทย), instruction, archive_plan, follow_up} · form_revisions[] จาก F-DOCCFG · sign_rows[] = ผู้จัดทำ + 1 ช่องต่อขั้นใน approval_chain snapshot — **จำนวนตามที่ตั้งใน DOA ไม่ fix** · คำตัดสินจาก print_config.decision_words.by_role[role_id] · layout.dense) → render logic-less 2 หน้า (R10 · parity กับ tpl_render.js)
### F-TMP-002-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **ivmj_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · **ivmj_result_recorded** (→approved → ผู้รับผิดชอบโครงการ + ผู้รับผิดชอบในตารางเหตุผล) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ · `ivmj.approved` ประกาศไว้ ไม่ยิงรอบนี้ (DEC-02)
### F-TMP-002-FN-10: listVisible
- canSee = admin ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · ใบไม่มีสิทธิ์ → 404 · CSV ใช้ตัวกรองเดียวกัน

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
