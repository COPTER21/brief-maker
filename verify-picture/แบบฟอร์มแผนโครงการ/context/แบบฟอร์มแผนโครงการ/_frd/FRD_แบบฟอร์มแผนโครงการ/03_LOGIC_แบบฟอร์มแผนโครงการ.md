# 03_LOGIC — F-TMP-004
> ไม่มีค่าคงที่ธุรกิจใน logic — สายอนุมัติจาก DOA กลาง · เลข/แบบพิมพ์จาก F-DOCCFG · ค่าสถานะ/ความรุนแรงตามต้นฉบับ (enum)

## §3.1 Functions (Scope-Local)
### F-TMP-004-FN-01: validatePlan
- Input ตาม API-03 body → errors VR-01..06 (05 §5.4): ช่องบังคับส่วนที่ 1–3 ว่าง · end_date < start_date · goals/actions/budget ไม่มีแถวที่มีข้อมูล · แถวที่มีข้อมูลขาดช่องบังคับ · action.end_date < action.start_date · budget.requested ไม่ใช่ตัวเลข ≥ 0 · แถวว่างทั้งแถวตัดทิ้ง (BR-14)
- กิจกรรมอยู่นอกช่วงโครงการ → warning (ไม่ใช่ error · BR-03)
### F-TMP-004-FN-02: computeDerived
- duration_days = end_date − start_date + 1 (โครงการและทุกกิจกรรม · BR-01) · total_requested = SUM(budget.requested) · total_approved = SUM(budget.approved) เมื่อมีค่า (BR-04) · seq กิจกรรมเรียงตามลำดับ · budget.approved = null ในร่าง (ล้างทุกครั้งที่แก้ร่าง)
### F-TMP-004-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-13): ตรวจ F-DOCCFG status ของ doc_type PJP (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('PJP', company_ctx)` = รหัสโครงการ → snapshot ผู้จัดทำ/ตำแหน่ง/หน่วยงาน + `header_snapshot` (Organization: ชื่อบริษัท โลโก้) · ห้าม format/+1 เอง
### F-TMP-004-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-004` → steps (ไม่มีวงเงิน · ค่าเริ่ม role-line-manager → role-gm) · ผู้ resolve ได้ = ผู้จัดทำ → ข้าม/ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) · status draft→pending ขั้น 1 · ล้าง returned_* · `TODO: DOA engine` (wire จริงตาม DOA_BRIEF)
### F-TMP-004-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · คำตัดสินตาม role (decision_words.by_role) · approve ขั้นที่ไม่ใช่ขั้นสุดท้าย → ขั้นถัดไป pending · approve ขั้นสุดท้าย: รับ approved_budget[i] (ว่าง = requested · < 0 → 422 · > requested = warning) → บันทึก budget.approved → status=approved → FN-08 render + `ENG-DOC-STORE.store(pdf,'PJP',id,'approved_final')` → ถ้า total_approved ≠ total_requested → FN-09 pjp_budget_adjusted · ไม่ส่งต่อ Budget (DEC-01/02)
### F-TMP-004-FN-06: returnToDraft
- reject (เหตุผลบังคับ) → audit "{คำปฏิเสธของ role} · กลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · budget.approved ล้าง · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-11)
### F-TMP-004-FN-07: cancelPlan
- owner หรือ admin ฝ่ายพัฒนาโครงการ · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-09 pjp_cancelled (ถ้าเดิม pending)
### F-TMP-004-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company · doc · project{name, code, owner_dept, manager, start_date, end_date, duration} · ข้อความส่วนที่ 2/3/8 · goals/actions/budget/risks เติมว่างถึง print_config.min_rows {3,10,6,5} · budget_total · sign_rows[] = ผู้จัดทำ + 1 แถวต่อขั้นใน approval_chain snapshot — **จำนวนตามที่ตั้งใน DOA ไม่ fix** · คำตัดสินจาก print_config.decision_words.by_role[role_id] หรือ default · layout.dense เมื่อแถวกลุ่มใดเกิน min_rows หรือขั้น DOA > 4) → render logic-less 2 หน้า (parity กับ tpl_render.js) · เงิน `#,##0.00` · วันที่หัวโครงการเต็ม พ.ศ. · วันที่กิจกรรมย่อ
### F-TMP-004-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **pjp_cancelled** (pending→cancelled → ผู้อนุมัติขั้นปัจจุบัน) · **pjp_budget_adjusted** (→approved ∧ total_approved ≠ total_requested → ผู้จัดทำ + ผู้รับผิดชอบหลัก) · **pjp_activity_delayed** (FN-11 เปลี่ยนเป็น Delayed → ผู้รับผิดชอบหลัก + role-line-manager) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ
### F-TMP-004-FN-10: listVisible
- canSee = admin ฝ่ายพัฒนาโครงการ ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · delayed = approved ∧ ∃ action.status = Delayed · ใบไม่มีสิทธิ์ → 404 · CSV 1 แถวต่อกิจกรรม
### F-TMP-004-FN-11: updateActionStatus
- status=approved · ผู้เรียก = owner ∨ project_manager_id (BR-12) · เปลี่ยนได้เฉพาะ action.status ∈ {Not Started, In Progress, Completed, Delayed} (BR-13) · บันทึก activity_status_log (append-only) + audit · ไม่ต้องอนุมัติใหม่ · ไม่ re-render PDF ฉบับ approved_final (PDF ปัจจุบันแสดงสถานะล่าสุด) · เปลี่ยนเป็น Delayed → FN-09 pjp_activity_delayed

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,11 | FN-10 |
| 03 | FN-01, FN-02, FN-03 |
| 04 | FN-01, FN-02 |
| 05,06 | FN-04 |
| 07 | FN-05 (+FN-08, FN-09) / FN-06 |
| 08 | FN-07 (+FN-09) |
| 09 | FN-11 (+FN-09) |
| 10 | FN-08 |
ทุก FN มี API ผูก ✓ (FN-09 ถูกเรียกจาก FN-05/07/11)
