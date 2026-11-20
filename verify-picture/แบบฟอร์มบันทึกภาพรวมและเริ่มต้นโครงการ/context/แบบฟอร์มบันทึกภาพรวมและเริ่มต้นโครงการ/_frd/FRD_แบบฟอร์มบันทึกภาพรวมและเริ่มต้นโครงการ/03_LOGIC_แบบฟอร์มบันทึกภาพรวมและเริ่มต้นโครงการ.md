# 03_LOGIC — F-TMP-001
> ไม่มีค่าคงที่ทางธุรกิจใน logic · ตัวเลือก/สายอนุมัติ/หัวกระดาษอ่านจาก config/DOA/Organization เท่านั้น

## §3.1 Functions (Scope-Local)
### F-TMP-001-FN-01: validateInitiation
- Input header + plan[] → errors VR-01..05 (05 §5.4) · วันที่เป้าหมาย < วันที่เริ่มต้น = VR-02 · วันครบกำหนด < วันเริ่มต้น = VR-04 (บล็อก · DEC-04/13/14)
### F-TMP-001-FN-02: savePlanAndRevisionNote
- แทนที่ plan[] ทั้งชุด (seq เรียงใหม่ 1..n) · เก็บ revision_detail ไว้ใช้ตอนอนุมัติครบ · ผูกไฟล์แนบ Document Center (ref_type='PJI')
### F-TMP-001-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-11): ตรวจ F-DOCCFG status ของ doc_type PJI (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('PJI', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง/ฝ่าย + `header_snapshot` (Organization: ชื่อบริษัท โลโก้ บรรทัดบริษัทในเครือ) · ห้าม format/+1 เอง
### F-TMP-001-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-001` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง · ผู้ resolve ได้ = ผู้จัดทำ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-001-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved → ขั้นถัดไป pending หรือ status=approved (ครบ) → เพิ่มแถว `project_initiation_revision` (version = ลำดับ 2 หลัก · detail = revision_detail หรือ "จัดทำครั้งแรก" · prepared_by = ผู้จัดทำ · approved_by = ผู้พิจารณาขั้นสุดท้าย) → FN-08 render + `ENG-DOC-STORE.store(pdf,'PJI',id,'approved_final')` → FN-09 pji_owner_assigned
### F-TMP-001-FN-06: returnToDraft
- reject (เหตุผลบังคับ) → audit "{คำปฏิเสธของขั้น} — ส่งกลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-09)
### F-TMP-001-FN-07: cancelInitiation
- owner หรือ admin_role · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-09 pji_cancelled (ถ้าเดิม pending)
### F-TMP-001-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html`: company (name · logo · group_line จาก header_snapshot) · doc (title · department · no · is_draft · form_code · revision จาก print_config) · project (name · origin · type_opportunity · owner · supporters · date_range = วันที่เริ่มต้น + " / " + วันที่เป้าหมาย (วันที่เต็ม พ.ศ.) · priority_status) · scope (6 ช่อง) · plan[] (เติมแถวว่างถึง print_config.min_rows_by_group.plan พร้อมเลขลำดับ) · revisions[] (เติมถึง min_rows_by_group.revisions) · sign_rows[] = ผู้จัดทำ + 1 ช่องต่อขั้นใน approval_chain snapshot (**จำนวนตาม DOA ไม่ fix**) แบ่งแถวละ ≤ print_config.sign_layout.max_per_row · คำตัดสินจาก print_config.decision_words.by_role[role_id] หรือ default · layout.dense เมื่อแผนงาน > dense_when_rows_over หรือขั้น DOA > 4 → render logic-less (parity กับ tpl_render.js) · 2 หน้าทุกสถานะ (R10)
### F-TMP-001-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **pji_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · **pji_owner_assigned** (→approved ขั้นสุดท้าย → ผู้รับผิดชอบหลัก + ผู้รับผิดชอบกิจกรรม แบบไม่ซ้ำ) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ
### F-TMP-001-FN-10: listVisible
- canSee = admin_role ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · ใบไม่มีสิทธิ์ → 404

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
| 11 | FN-02 |
ทุก FN มี API ผูก ✓
