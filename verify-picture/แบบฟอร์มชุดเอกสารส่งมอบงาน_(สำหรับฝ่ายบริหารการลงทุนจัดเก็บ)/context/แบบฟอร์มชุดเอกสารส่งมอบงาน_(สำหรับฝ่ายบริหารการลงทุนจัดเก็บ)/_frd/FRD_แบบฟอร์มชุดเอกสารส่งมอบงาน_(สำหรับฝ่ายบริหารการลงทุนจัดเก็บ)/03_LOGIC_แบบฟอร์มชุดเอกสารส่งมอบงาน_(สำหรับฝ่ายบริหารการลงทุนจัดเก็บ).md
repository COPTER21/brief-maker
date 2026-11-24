# 03_LOGIC — F-TMP-008
> ไม่มีรายการตัวเลือก hardcode ใน logic — อ่าน HandoverConfig เท่านั้น (DEC-04) · ไม่มีช่องคำนวณตัวเลข

## §3.1 Functions (Scope-Local)
### F-TMP-008-FN-01: validateHandover
- Input `{handover, items[], followup}` → errors VR-01..08 (05 §5.4) · handover 6 ช่องบังคับ · received_date ≤ วันนี้ · received_time HH:MM · result ∈ HandoverConfig.handover_results · ≥1 แถว items · received ∈ received_options · completeness ∈ completeness_options
- DEC-13: received = not_received ∧ completeness = complete_ok → error · DEC-14: แถวไม่ผ่าน (FN-02) ต้องมี issue + fix_owner + due_date · DEC-15: due_date / followup_date ≥ received_date · DEC-12: result = complete_result ∧ open_items > 0 → error ที่ result · DEC-16: result ≠ complete_result → open_issues required
### F-TMP-008-FN-02: computeOpenItems
- rowFail(item) = ¬(received = received_ok ∧ completeness = complete_ok) (ค่า received_ok/complete_ok จาก HandoverConfig) · open_items = จำนวนแถวที่ rowFail · ทำฝั่ง server เสมอ (FE แสดงสดเพื่อช่วยกรอก)
### F-TMP-008-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type HOI (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('HOI', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง/ฝ่าย + `header_snapshot` (Organization: ชื่อบริษัท · โลโก้ · บรรทัดบริษัทในเครือ) · ห้าม format/+1 เอง
### F-TMP-008-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-008` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง (ผู้จัดการฝ่ายบริหารการลงทุน) · role-mgr-bu ตาม DOA กลาง (ฝ่ายพัฒนาธุรกิจ) · ผู้ resolve ได้ = ผู้จัดทำ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-008-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved (คำอนุมัติของ role + ความเห็นเก็บใน chain/audit) → ขั้นถัดไป pending หรือ status=approved (ครบ) → FN-08 render + `ENG-DOC-STORE.store(pdf,'HOI',id,'approved_final')` → FN-09
### F-TMP-008-FN-06: returnToDraft
- reject (เหตุผลบังคับ) → audit "{คำปฏิเสธ} — กลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08)
### F-TMP-008-FN-07: cancelRecord
- owner หรือ admin_role ฝ่ายบริหารการลงทุน · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-09 hoi_cancelled (ถ้าเดิม pending)
### F-TMP-008-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company{name,logo,group_line} · doc{title,no,is_draft,form_code,revision} · handover{project_name, sender, receiver, received_at "dd/mm/พ.ศ. HH:MM น.", package_version, result} · items_p1[] = แถวที่ 1..print_config.rows_page1 · items_p2[] = ที่เหลือ (เติมแถวว่างจนครบ print_config.min_rows) · has_p2_rows · followup{open_issues, pending_docs, followup_date, remark} · วันที่ dd/mm/พ.ศ. string · sign_rows[] = ผู้จัดทำ + 1 ช่องต่อขั้นใน approval_chain snapshot (**จำนวนตาม DOA ไม่ fix**) · คำตัดสินจาก print_config.decision_words.by_role[role_id] หรือ default · form_revisions[] จาก DocumentConfig (F003) · layout.dense เมื่อแถว > dense_when_rows_over หรือขั้น DOA > 4) → render logic-less (parity กับ tpl_render.js) · ทุกสถานะ 2 หน้า (R10)
### F-TMP-008-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **hoi_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · **hoi_acknowledged_open_items** (→approved และ result ≠ complete_result / open_items > 0 → ผู้จัดทำ · in-app) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ
### F-TMP-008-FN-10: listVisible
- canSee = admin_role ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · filter result · ใบไม่มีสิทธิ์ → 404

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
