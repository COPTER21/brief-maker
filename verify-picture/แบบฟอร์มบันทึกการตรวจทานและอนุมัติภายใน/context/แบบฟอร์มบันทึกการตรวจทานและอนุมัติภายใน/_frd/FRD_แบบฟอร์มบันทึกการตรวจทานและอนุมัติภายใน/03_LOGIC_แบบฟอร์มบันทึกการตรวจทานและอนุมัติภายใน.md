# 03_LOGIC — F-TMP-006
> ไม่มีรายการสถานะ hardcode ใน logic — อ่าน ReviewApprovalConfig เท่านั้น (DEC-04) · ไม่มีช่องคำนวณ (DEC-14)

## §3.1 Functions (Scope-Local)
### F-TMP-006-FN-01: validateReview
- Input `{reviews[], approvals[], final}` → errors VR-01..04 (05 §5.4) · ≥1 แถวตรวจทาน · status ∈ ReviewApprovalConfig.review_statuses · review_date/decided_date ≤ วันนี้ · แถว approvals manual ต้องครบ 4 ช่อง · final.approval_status ∈ ReviewApprovalConfig.final_statuses · effective_date บังคับเมื่อ approval_status ∈ final_needs_effective และต้องว่างเมื่อไม่อยู่ (DEC-18)
### F-TMP-006-FN-02: computeWarnings
- open_items = จำนวนแถว status ≠ closed_status (config) · warnings: `complete_with_open` (approval_status = complete_status ∧ open_items > 0 — DEC-15) · `closed_without_owner` (status = closed_status ∧ fix_owner ว่าง ∧ comment ว่าง) · เตือนไม่บล็อก · ทำฝั่ง server เสมอ
### F-TMP-006-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-11): ตรวจ F-DOCCFG status ของ doc_type IRV (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('IRV', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง/ฝ่าย + `header_snapshot` (Organization: ชื่อบริษัท · โลโก้ · บรรทัดบริษัทในเครือ) · ห้าม format/+1 เอง
### F-TMP-006-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-006` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง · role-gm ตาม DOA กลาง · ผู้ resolve ได้ = ผู้จัดทำ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-006-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved · append แถว `internal_review_approval` source=doa {ชื่อ/ตำแหน่ง snapshot ผู้พิจารณา · decision = คำอนุมัติของ role + ความเห็น · decided_date · evidence "พิจารณาในระบบ"} (DEC-16) → ขั้นถัดไป pending หรือ status=approved (ครบ) → FN-08 render + `ENG-DOC-STORE.store(pdf,'IRV',id,'approved_final')` → FN-09
### F-TMP-006-FN-06: returnToDraft
- reject (เหตุผลบังคับ) → append แถวอนุมัติภายใน source=doa (คำปฏิเสธของ role — เหตุผล) · audit "{คำปฏิเสธ} — กลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-09)
### F-TMP-006-FN-07: cancelReview
- owner หรือ admin_role ฝ่ายพัฒนาธุรกิจ · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-09 irv_cancelled (ถ้าเดิม pending)
### F-TMP-006-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company{name,logo,group_line} · doc{title,no,is_draft,form_code,revision} · reviews_p1[] = แถวที่ 1..print_config.rows_page1 · reviews_p2[] = ที่เหลือ (เติมแถวว่างจนครบ print_config.min_rows) · has_p2_rows · approvals[] (เติมแถวว่างจนครบ print_config.min_rows_approvals) · final{approval_status, effective_date, remark} · วันที่ dd/mm/พ.ศ. string · sign_rows[] = ผู้จัดทำ + 1 ช่องต่อขั้นใน approval_chain snapshot (**จำนวนตาม DOA ไม่ fix**) · คำตัดสินจาก print_config.decision_words.by_role[role_id] หรือ default · form_revisions[] จาก DocumentConfig (F003) · layout.dense เมื่อแถวตรวจทาน > dense_when_rows_over หรือขั้น DOA > 4) → render logic-less (parity กับ tpl_render.js) · ทุกสถานะ 2 หน้า (R10)
### F-TMP-006-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **irv_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · **irv_approved_open_items** (→approved และ open_items > 0 → ผู้จัดทำ · in-app) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ
### F-TMP-006-FN-10: listVisible
- canSee = admin_role ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · filter final_status · ใบไม่มีสิทธิ์ → 404

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
