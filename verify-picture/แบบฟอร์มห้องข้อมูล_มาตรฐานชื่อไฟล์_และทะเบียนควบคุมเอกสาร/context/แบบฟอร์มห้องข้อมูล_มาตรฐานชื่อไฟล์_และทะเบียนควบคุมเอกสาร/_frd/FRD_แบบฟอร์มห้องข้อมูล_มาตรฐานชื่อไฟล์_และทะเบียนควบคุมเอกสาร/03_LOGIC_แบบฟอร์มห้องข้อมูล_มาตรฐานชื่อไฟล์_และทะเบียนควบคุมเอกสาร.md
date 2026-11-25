# 03_LOGIC — F-TMP-006
> ไม่มีสูตรตัวเลขบนกระดาษ · ค่าคงที่ (มาตรฐานชื่อไฟล์ + โฟลเดอร์มาตรฐาน) อ่านจาก config (FN-12 · BR-01/02) · ตัวเลือกอ่านจาก master list (BR-09) · เกณฑ์เตือนอ่านจาก config (BR-05/07)

## §3.1 Functions (Scope-Local)
### F-TMP-006-FN-01: validateRegister
- Input `{project_name, folders[], documents[], changes[], access[]}` → errors VR-01..10 (05 §5.4) · ≥1 โฟลเดอร์ + ≥1 เอกสาร (BR-10) · ต่อแถวโฟลเดอร์: folder_name · owner · access_level บังคับ · ต่อแถวเอกสาร: doc_name · owner · version · version_date · doc_status บังคับ + version ตรง `^(V\d{2}|Final)$` (BR-04) · ต่อแถวการเปลี่ยนแปลง: change_date · doc_ref · detail · status บังคับ + applied ต้องมี effective_date (BR-07) · ต่อแถวสิทธิ: user_name · access_level · scope · granted_date · status บังคับ + revoked_date ≥ granted_date + expired/revoked ต้องมี revoked_date (BR-08) · คืน `warnings[]` NOT_FINAL_VERSION (BR-05) · EFFECTIVE_BEFORE_DATE (BR-07) ไม่บล็อก
### F-TMP-006-FN-02: computeRows
- เลขรันตามลำดับแถวในใบ: `folder_no` = 2 หลัก (01, 02 …) · `doc_code` = D-001 … · `change_code` = CH-001 … · `seq` = 1, 2 … (BR-03) · `std_file_name` = `YYYYMMDD(version_date)_doc_name(ช่องว่าง→_)_version[_token]` · token จาก doc_status: working→Working · in_review/pending_approval→Review · final→Final · external→External · cancelled→(ไม่มี) (BR-06 · DEC-18)
### F-TMP-006-FN-03: attachFiles
- ผ่าน Document Center (ref_type='IVMD') · file_policy ≤20MB · pdf/doc/xls/รูป
### F-TMP-006-FN-04: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-13): ตรวจ F-DOCCFG status ของ doc_type IVMD (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('IVMD', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง + `header_snapshot` (Organization: ชื่อบริษัท โลโก้ บรรทัด "… และบริษัทในเครือ") + `naming_snapshot` (FN-12) · ห้าม format/+1 เอง
### F-TMP-006-FN-05: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-006` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง · role-gm ตาม DOA · ผู้ resolve ได้ = ผู้จัดทำ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) + `approver_role` ต่อขั้น · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-006-FN-06: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved (คำตามบทบาท: role-line-manager = ตรวจสอบแล้ว · role-gm = อนุมัติ) → ขั้นถัดไป pending หรือ (ขั้นสุดท้าย) status=approved · `approved_by`/`approved_at` → FN-09 render + `ENG-DOC-STORE.store(pdf,'IVMD',id,'approved_final')` → FN-10 ivmd_register_approved · ไม่สร้างสิทธิจริงในไดรฟ์ (BR-17)
### F-TMP-006-FN-07: returnToDraft
- reject (เหตุผลบังคับ) → audit "{คำปฏิเสธของขั้น} (ขั้น n)" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-11 · BR-DOA-03 ตามปกติ)
### F-TMP-006-FN-08: cancelRegister
- owner หรือ admin role ฝ่ายบริหารการลงทุน · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending/waiting = skipped → FN-10 ivmd_cancelled (ถ้าเดิม pending)
### F-TMP-006-FN-09: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company{name, name_line, logo} · doc{title, no, is_draft, form_code, revision} · project{name} · naming{pattern, date_format, version_format, status_tokens, example} จาก naming_snapshot · folders[] {folder_no, folder_name, owner, access_level (ป้ายไทย), required_docs, remark} เติมถึง print_config.min_rows_by_group.folders (8 · ชื่อโฟลเดอร์มาตรฐาน) · documents[] {doc_code, doc_name, owner, version, version_date (dd/mm/พ.ศ.), doc_status (ป้ายไทย), location, reviewer, approver, remark} เติมถึง 5 (รหัสต่อเนื่อง) · changes[] {change_code, change_date, doc_ref, detail, reason, impact, approver, effective_date, status, remark} เติมถึง 5 · access[] {seq, user_name, org_unit, role, access_level, scope, granted_date, revoked_date, approver, status} เติมถึง 5 · form_revisions[] จาก F-DOCCFG · sign_rows[] = ผู้จัดทำ + 1 ช่องต่อขั้นใน approval_chain snapshot — **จำนวนตามที่ตั้งใน DOA ไม่ fix** · คำตัดสินจาก print_config.decision_words.by_role[role_id] · layout.dense) → render logic-less 2 หน้า (R10 · parity กับ tpl_render.js)
### F-TMP-006-FN-10: emitEvents
- `ENG-NOTIFY.emit`: **ivmd_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · **ivmd_register_approved** (→approved → ผู้จัดทำ + admin role ฝ่าย ให้ไปตั้งสิทธิจริงตามทะเบียน) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ · `ivmd.approved` ประกาศไว้ ไม่ยิงรอบนี้ (DEC-02)
### F-TMP-006-FN-11: listVisible
- canSee = admin ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · open_docs = มีเอกสาร doc_status ∈ {in_review, pending_approval} · ใบไม่มีสิทธิ์ → 404 · CSV ใช้ตัวกรองเดียวกัน
### F-TMP-006-FN-12: loadDefaults
- อ่าน config `FileNamingPolicy.{pattern, date_format, version_format, status_tokens, example}` + `DataRoomPolicy.default_folders` (8 ชื่อ) → ใบใหม่ตั้งต้นโฟลเดอร์ 8 แถว (BR-02) · มาตรฐานชื่อไฟล์แสดงอ่านอย่างเดียว (BR-01) · ห้าม hardcode ค่าในโค้ด · config เปลี่ยนหลังออกเลข → ใบเดิมใช้ naming_snapshot (EC-13)

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
| 12 | FN-12 |
ทุก FN มี API ผูก ✓
