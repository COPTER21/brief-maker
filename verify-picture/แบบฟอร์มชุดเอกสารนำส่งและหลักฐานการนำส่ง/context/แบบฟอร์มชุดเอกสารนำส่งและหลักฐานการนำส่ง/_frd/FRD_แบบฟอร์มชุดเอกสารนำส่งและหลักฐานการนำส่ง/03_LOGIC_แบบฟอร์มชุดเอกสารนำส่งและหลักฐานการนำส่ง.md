# 03_LOGIC — F-TMP-009
> ไม่มีสูตร/ค่าคงที่ตัวเลขบนกระดาษ · ตัวเลือกอ่านจาก master list (BR-10) · คำเตือน (ขาดเอกสาร · ส่งก่อนวันที่นำส่ง) อ่านจาก config (BR-04 · BR-08)

## §3.1 Functions (Scope-Local)
### F-TMP-009-FN-01: validateDispatch
- Input `{project_name, purpose, recipient, dispatch_date, docs[]}` → errors VR-01..04 (05 §5.4) · docs ≥ 1 แถว (BR-02) · ต่อแถว: doc_name + version บังคับ · status ∈ {missing, limited} → remark บังคับ (BR-03) · คืน `warnings[]` DOCS_MISSING เมื่อมี status = missing (BR-04) ไม่บล็อก
### F-TMP-009-FN-02: computeRows
- `seq` = 1, 2, 3 … ต่อใบตามลำดับแถว ทั้ง docs และ deliveries (BR-01 · ลบแถวกลาง = รันใหม่ · ไม่ใช่ key) · `missing_count` · `complete_count` · `top_confidentiality` = ระดับสูงสุดในชุด (secret > confidential > internal > public) · `received_count` · `pending_count` · `failed_count`
### F-TMP-009-FN-03: attachFiles
- ผ่าน Document Center (ref_type='IVMG') · ระดับใบ + หลักฐานต่อแถว (`evidence_file_id`) · file_policy ≤20MB · pdf/doc/xls/รูป/eml/msg
### F-TMP-009-FN-04: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-11): ตรวจ F-DOCCFG status ของ doc_type IVMG (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('IVMG', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง + `header_snapshot` (Organization: ชื่อบริษัท โลโก้ บรรทัด "… และบริษัทในเครือ") · ห้าม format/+1 เอง
### F-TMP-009-FN-05: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-009` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง · role-gm = รองกรรมการผู้จัดการ / กรรมการผู้จัดการ (รอยืนยัน OQ-03) · ผู้ resolve ได้ = ผู้จัดทำ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) + `approver_role` ต่อขั้น · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-009-FN-06: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved (คำตามบทบาท: role-line-manager = ตรวจสอบแล้ว · role-gm = อนุมัติ) → ขั้นถัดไป pending หรือ (ขั้นสุดท้าย) status=approved · `approved_by`/`approved_at` → FN-09 render + `ENG-DOC-STORE.store(pdf,'IVMG',id,'approved_final')` · ผู้ตรวจทาน (PDF/จอ) = approval_chain[ขั้นแรก] · ผู้อนุมัติ = approval_chain[ขั้นสุดท้าย] (DEC-14)
### F-TMP-009-FN-07: returnToDraft
- reject = "ส่งกลับ" (เหตุผลบังคับ) → audit "ส่งกลับ (ขั้น n)" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-09 · BR-DOA-03 ตามปกติ)
### F-TMP-009-FN-08: cancelDispatch
- owner หรือ admin role ฝ่ายบริหารการลงทุน · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending/waiting = skipped → FN-11 ivmg_cancelled (ถ้าเดิม pending)
### F-TMP-009-FN-09: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company{name, name_line, logo} · doc{title, no, is_draft, form_code, revision} · dispatch{project_name, purpose, recipient, dispatch_date (dd/mm/พ.ศ.), preparer_name, reviewer_name, approver_name} · docs[] {seq, doc_name, version, status (ป้ายไทย), confidentiality (ป้ายไทย), remark} เติมแถวว่าง (มีลำดับ) ถึง print_config.min_rows_by_group.docs (10) · deliveries[] {seq, sent_at (dd/mm/พ.ศ. HH:mm น.), sender, receiver, receiver_org, channel (ป้ายไทย), docs_sent, evidence, remark, receipt_status (ป้ายไทย)} เติมถึง min_rows_by_group.deliveries (15) · form_revisions[] จาก F-DOCCFG · sign_rows[] = ผู้จัดทำ + 1 ช่องต่อขั้นใน approval_chain snapshot — **จำนวนตามที่ตั้งใน DOA ไม่ fix** · คำตัดสินจาก print_config.decision_words.by_role[role_id] · layout.dense) → render logic-less 2 หน้า (R10 · parity กับ tpl_render.js)
### F-TMP-009-FN-10: saveDeliveries
- เฉพาะ status = approved · owner หรือ admin (DEC-20) · แทนชุดแถวทั้งหมด (audit before/after "บันทึกหลักฐานการนำส่ง") · ต่อแถว VR-05..08: sent_at (วันที่ + HH:mm) ≤ now (อนาคต → 422) · sender · receiver · receiver_org · docs_sent บังคับ · receipt_status = received → evidence หรือ evidence_file_id บังคับ (BR-06) · channel = other ∨ receipt_status ∈ {failed, cancelled} → remark บังคับ (BR-07) · sent_at < dispatch_date → `warnings[]` SENT_BEFORE_DISPATCH_DATE (BR-08) · ≥ 1 แถว (VR-09) · ไม่เปลี่ยน approval_chain / status (ไม่ต้องอนุมัติซ้ำ) · แถวใหม่หรือเปลี่ยนเป็น failed → FN-11 ivmg_delivery_failed
### F-TMP-009-FN-11: emitEvents
- `ENG-NOTIFY.emit`: **ivmg_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · **ivmg_delivery_failed** (FN-10 แถว failed ใหม่ → ผู้จัดทำ + admin role · payload project_name · receiver · channel · remark) · **ivmg_dispatch_closed** (FN-13 approved→closed → approval_chain + admin role · payload project_name · received_count) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ · `ivmg.approved` / `ivmg.closed` ประกาศไว้ ไม่ยิงรอบนี้ (DEC-02)
### F-TMP-009-FN-12: listVisible
- canSee = admin ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · confidentiality = มีเอกสารระดับนั้นในชุด · ใบไม่มีสิทธิ์ → 404 · CSV ใช้ตัวกรองเดียวกัน
### F-TMP-009-FN-13: closeDispatch
- owner หรือ admin · status = approved · received_count ≥ 1 (else 422 NO_RECEIVED) · pending_count = 0 (else 422 PENDING_CONFIRMATION) (BR-09) → status=closed · closed_by/at · audit "ปิดการนำส่ง" → FN-11 ivmg_dispatch_closed · หลังปิด ล็อกทั้งใบ

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — `TODO: DOA engine` ฝั่ง prototype = MOCK_DOA_RESOLVED (DOA-ENGINE-HOOK) · ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,10 | FN-12 |
| 03 | FN-01, FN-02, FN-04 |
| 04 | FN-01, FN-02 |
| 05,06 | FN-05 |
| 07 | FN-06 (+FN-09) / FN-07 |
| 08 | FN-08 (+FN-11) |
| 09 | FN-09 |
| 11 | FN-03 |
| 12 | FN-10 (+FN-02, FN-11) |
| 13 | FN-13 (+FN-11) |
ทุก FN มี API ผูก ✓
