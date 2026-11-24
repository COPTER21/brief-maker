# 03_LOGIC — F-TMP-004
> ไม่มีรายการเหตุผล/สถานะปิดโครงการใน logic — อ่าน ProjectClosure config เท่านั้น (DEC-04)

## §3.1 Functions (Scope-Local)
### F-TMP-004-FN-01: validateDiscontinuation
- Input header + reasons[] + closure → errors VR-01..06 (05 §5.4) · reasons ครบตาม ProjectClosure.reason_types (ไม่เพิ่ม/ลบแถว — DEC-05) · ≥1 แถว selected = ใช่ (DEC-12) · แถว ใช่ ต้องมี detail รวมแถวเหตุผลอื่น (DEC-13/14) · closure_status ∈ ProjectClosure.closure_statuses · สถานะ key=follow ต้องมี future_followup (DEC-15) · decision_date ≤ วันนี้
### F-TMP-004-FN-02: normalizeReasons
- แถว selected = ไม่ใช่ → ล้าง detail/evidence/impact/revisit_condition (DEC-14) · snapshot reason_name จาก config ณ เวลาบันทึก · selected_count = จำนวน ใช่ · ทำซ้ำฝั่ง server เสมอ (ไม่เชื่อค่าจาก FE)
### F-TMP-004-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type PCL (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('PCL', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง/ฝ่าย + ผู้รับผิดชอบ + `header_snapshot` (Organization: ชื่อบริษัท · โลโก้ · บรรทัดบริษัทในเครือ) · ห้าม format/+1 เอง
### F-TMP-004-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-004` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง · role-gm ตาม DOA กลาง · ผู้ resolve ได้ = ผู้จัดทำ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-004-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved → ขั้นถัดไป pending หรือ status=approved (ครบ) → FN-08 render + `ENG-DOC-STORE.store(pdf,'PCL',id,'approved_final')` → FN-09 · ไม่เปลี่ยนค่า/ไม่ปิดโครงการในระบบอื่น (DEC-01/02)
### F-TMP-004-FN-06: returnToDraft
- reject (เหตุผลบังคับ) → audit "{คำปฏิเสธของขั้น} — ส่งกลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08)
### F-TMP-004-FN-07: cancelDiscontinuation
- owner หรือ admin_role ฝ่ายพัฒนาธุรกิจ · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-09 pcl_cancelled (ถ้าเดิม pending)
### F-TMP-004-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company{name,logo,group_line} · doc{title,no,is_draft,form_code,revision} · project{name,owner,decision_date (วันที่ไทยเต็ม),stopped_stage} · reasons[] ครบตาม config (reason · selected · detail · evidence · impact · revisit_condition — แถวไม่ใช่ส่งข้อความว่าง) · closure{summary,decision_documents,lessons_learned,archive_method,future_followup,status} · sign_rows[] = ผู้จัดทำ + 1 ช่องต่อขั้นใน approval_chain snapshot (**จำนวนตาม DOA ไม่ fix**) · คำตัดสินจาก print_config.decision_words.by_role[role_id] หรือ default · form_revisions[] จาก DocumentConfig (F003) · layout.dense เมื่อขั้น DOA > 4) → render logic-less (parity กับ tpl_render.js) · ทุกสถานะ 2 หน้า (R10)
### F-TMP-004-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **pcl_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · **pcl_followup_approved** (→approved และ closure_status เป็นสถานะ key=follow ของ ProjectClosure config → ผู้จัดทำ · in-app) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ
### F-TMP-004-FN-10: listVisible
- canSee = admin_role ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · filter closure_status · ค้นหา doc_no/project_name/ผู้จัดทำ/ชื่อเหตุผล · ใบไม่มีสิทธิ์ → 404

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
