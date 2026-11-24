# 03_LOGIC — F-TMP-007
> ไม่มีรายการสถานะ hardcode ใน logic — อ่าน HandoverPackageConfig เท่านั้น (DEC-04) · ไม่มีช่องคำนวณ (DEC-12)

## §3.1 Functions (Scope-Local)
### F-TMP-007-FN-01: validatePackage
- Input `{handover, items[], notes}` → errors VR-01..05 (05 §5.4) · handover 6 ช่องบังคับ · ≥1 แถวรายการ · doc_name + status บังคับทุกแถว · status ∈ HandoverPackageConfig.doc_statuses · data_status ∈ HandoverPackageConfig.data_statuses · data_limits บังคับเมื่อ data_status = limited_data หรือมีแถว status = limited_doc (DEC-14)
### F-TMP-007-FN-02: computeWarnings
- gap_items = จำนวนแถว status ∈ gap_doc (config) · warnings: `complete_with_gap` (data_status = complete_data ∧ gap_items > 0 — DEC-13) · `doc_after_handover` (doc_date > handover_date — DEC-16) · เตือนไม่บล็อก · ทำฝั่ง server เสมอ
### F-TMP-007-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type HOB (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('HOB', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง/ฝ่าย + `header_snapshot` (Organization: ชื่อบริษัท · โลโก้ · บรรทัดบริษัทในเครือ) · ห้าม format/+1 เอง
### F-TMP-007-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-007` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง · role-mgr-bu = **receiver_id ของเอกสาร** (DEC-15 · ว่าง → ตาม DOA กลาง) · ผู้ resolve ได้ = ผู้จัดทำ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-007-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved + ความเห็นลง chain/audit → ขั้นถัดไป pending หรือ status=approved (ครบ) → FN-08 render + `ENG-DOC-STORE.store(pdf,'HOB',id,'approved_final')` → FN-09
### F-TMP-007-FN-06: returnToDraft
- reject (เหตุผลบังคับ) → audit "{คำปฏิเสธ} — กลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08)
### F-TMP-007-FN-07: cancelPackage
- owner หรือ admin_role ฝ่ายพัฒนาธุรกิจ · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-09 hob_cancelled (ถ้าเดิม pending)
### F-TMP-007-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company{name,logo,group_line} · doc{title,no,is_draft,form_code,revision} · handover{project_name, sender, receiver, handover_date, package_version, data_status} · notes{assumptions, open_issues, data_limits, bd_support} · docs_p1[] = แถวที่ 1..print_config.rows_page1 · docs_p2[] = ที่เหลือ (เติมแถวว่างจนครบ print_config.min_rows) · has_p2_rows · วันที่ dd/mm/พ.ศ. string · sign_rows[] = ผู้จัดทำ + 1 ช่องต่อขั้นใน approval_chain snapshot (**จำนวนตาม DOA ไม่ fix**) · คำตัดสินจาก print_config.decision_words.by_role[role_id] หรือ default · form_revisions[] จาก DocumentConfig (F003) · layout.dense เมื่อแถวรายการ > dense_when_rows_over หรือขั้น DOA > 4) → render logic-less (parity กับ tpl_render.js) · ทุกสถานะ 2 หน้า (R10)
### F-TMP-007-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **hob_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · **hob_received_with_gaps** (→approved และ gap_items > 0 หรือ data_status ≠ complete_data → ผู้จัดทำ · in-app) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ
### F-TMP-007-FN-10: listVisible
- canSee = admin_role ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · filter data_status · ใบไม่มีสิทธิ์ → 404

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
