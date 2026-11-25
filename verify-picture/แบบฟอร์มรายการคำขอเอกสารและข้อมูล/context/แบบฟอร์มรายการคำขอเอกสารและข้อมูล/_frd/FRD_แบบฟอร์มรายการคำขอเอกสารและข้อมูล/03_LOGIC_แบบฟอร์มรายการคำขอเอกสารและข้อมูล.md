# 03_LOGIC — F-TMP-007
> ไม่มีสูตรตัวเลขบนกระดาษ · ค่าคงที่ (รูปแบบรหัสคำขอ + หมายเหตุการใช้งาน) อ่านจาก config (FN-12 · BR-01/02) · ตัวเลือกอ่านจาก master list (BR-10) · เกณฑ์เตือนอ่านจาก config (BR-07/09)

## §3.1 Functions (Scope-Local)
### F-TMP-007-FN-01: validateRequestList
- Input `{project_name, items[]}` → errors VR-01..09 (05 §5.4) · ต่อแถว: item · requestee · owner · due_date · status บังคับ · status ∈ {requested, partial, received} ต้องมี request_date (BR-04) · received ต้องมี received_date · not_requested ต้องไม่มี received_date (BR-05) · due_date ≥ request_date · received_date ≥ request_date (BR-06) · status ∈ {not_applicable, cancelled} ต้องมี remark (BR-08) · doc_link ว่าง หรือ ตรง `^(https?://\S+|[^\s/\\].*[/\\].*)$` (BR-09) · คืน `warnings[]` OVERDUE (due_date < วันนี้ ∧ status ∉ {received, not_applicable, cancelled} · BR-07) · CREDENTIAL_WORD (doc_link/remark มี password|passwd|รหัสผ่าน · BR-09) ไม่บล็อก · ร่างบันทึกได้แม้ items ว่าง (≥1 ตรวจตอนส่ง FN-05)
### F-TMP-007-FN-02: assignCodesAndSummary
- แถวใหม่ (ไม่มี request_code) → `DocRequestPolicy.code_prefix` + เลข 3 หลัก = max(รหัสเดิมในใบ)+1 · แถวเดิมคงรหัส · ลบแถวไม่รันใหม่ (BR-01) · summary = total · received · partial · pending (not_requested + requested) · closed (not_applicable + cancelled) · overdue — คำนวณตอนอ่าน ไม่เก็บ
### F-TMP-007-FN-03: attachFiles
- ผ่าน Document Center (ref_type='IVME') · file_policy ≤20MB · pdf/doc/xls/รูป
### F-TMP-007-FN-04: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type IVME (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('IVME', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง + `header_snapshot` (Organization: ชื่อบริษัท โลโก้ บรรทัด "… และบริษัทในเครือ") + `usage_note_snapshot` (FN-12) · ห้าม format/+1 เอง
### F-TMP-007-FN-05: resolveAndSubmit
- items ≥ 1 (VR-10 · 422 NO_ITEMS) → `GET /doa/resolve?feature_id=F-TMP-007` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง · role-gm ตาม DOA · ผู้ resolve ได้ = ผู้จัดทำ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) + `approver_role` ต่อขั้น · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-007-FN-06: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved (คำตามบทบาท: role-line-manager = ตรวจสอบแล้ว · role-gm = อนุมัติ) → ขั้นถัดไป pending หรือ (ขั้นสุดท้าย) status=approved · `approved_by`/`approved_at` → FN-09 render + `ENG-DOC-STORE.store(pdf,'IVME',id,'approved_final')` → FN-10 ivme_request_list_approved · ไม่ส่งคำขอถึงผู้ถูกขอข้อมูล (BR-18)
### F-TMP-007-FN-07: returnToDraft
- reject (เหตุผลบังคับ) → audit "{คำปฏิเสธของขั้น} (ขั้น n)" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08 · BR-DOA-03 ตามปกติ)
### F-TMP-007-FN-08: cancelRequestList
- owner หรือ admin role ฝ่ายบริหารการลงทุน · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending/waiting = skipped → FN-10 ivme_cancelled (ถ้าเดิม pending)
### F-TMP-007-FN-09: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company{name, name_line, logo} · doc{title, no, is_draft, form_code, revision} · project{name} · usage_note (snapshot) · requests[] {request_code, item, requestee, owner, request_date (dd/mm/พ.ศ.), due_date, status (ป้ายไทย), received_date, remark, doc_link} เติมแถวว่างถึง print_config.min_rows_by_group.requests (20) โดยรหัสรันต่อจากรหัสสูงสุด · summary{total, received, partial, pending, closed} · form_revisions[] จาก F-DOCCFG · sign_rows[] = ผู้จัดทำ + 1 ช่องต่อขั้นใน approval_chain snapshot — **จำนวนตามที่ตั้งใน DOA ไม่ fix** · คำตัดสินจาก print_config.decision_words.by_role[role_id] · layout.dense = items > 20 ∨ ขั้น > 4) → render logic-less 2 หน้า (R10 · ตัดหน้าก่อนบล็อก "การตรวจทาน / อนุมัติ" · parity กับ tpl_render.js)
### F-TMP-007-FN-10: emitEvents
- `ENG-NOTIFY.emit`: **ivme_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · **ivme_request_list_approved** (→approved → ผู้จัดทำ + admin role ฝ่าย ให้เริ่มส่งคำขอนอกระบบ · vars request_count / received_count) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ · `ivme.approved` ประกาศไว้ ไม่ยิงรอบนี้ (DEC-02)
### F-TMP-007-FN-11: listVisible
- canSee = admin ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · overdue = มีแถว OVERDUE (FN-01) · ใบไม่มีสิทธิ์ → 404 · CSV ใช้ตัวกรองเดียวกัน (1 แถวต่อคำขอ)
### F-TMP-007-FN-12: loadDefaults
- อ่าน config `DocRequestPolicy.code_prefix` (ค่าเริ่ม DR-) + `DocRequestPolicy.usage_note` → ใบใหม่ตั้งต้น 1 แถว สถานะ ยังไม่ขอ (BR-03) · หมายเหตุการใช้งานแสดงอ่านอย่างเดียว (BR-02) · ห้าม hardcode ค่าในโค้ด · config เปลี่ยนหลังออกเลข → ใบเดิมใช้ snapshot (EC-16)

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — `TODO: DOA engine` ฝั่ง prototype = MOCK_DOA_RESOLVED (DOA-ENGINE-HOOK) · ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,10 | FN-11 (+FN-02 summary) |
| 03 | FN-01, FN-02, FN-04 |
| 04 | FN-01, FN-02 |
| 05,06 | FN-05 |
| 07 | FN-06 (+FN-09, FN-10) / FN-07 |
| 08 | FN-08 (+FN-10) |
| 09 | FN-09 |
| 11 | FN-03 |
| 12 | FN-12 |
ทุก FN มี API ผูก ✓
