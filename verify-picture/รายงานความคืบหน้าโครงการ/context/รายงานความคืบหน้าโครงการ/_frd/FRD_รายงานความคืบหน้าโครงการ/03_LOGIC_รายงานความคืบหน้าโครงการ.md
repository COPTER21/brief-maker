# 03_LOGIC — F-TMP-005
> ไม่มีค่าคงที่ธุรกิจใน logic — สายอนุมัติจาก DOA กลาง · เลข/แบบพิมพ์จาก F-DOCCFG · ค่าเริ่มจาก F-TMP-004 · ถ้อยคำตัวเลือกตามต้นฉบับ (enum)

## §3.1 Functions (Scope-Local)
### F-TMP-005-FN-01: validateReport
- Input ตาม API-03 body → errors VR-01..07 (05 §5.4): ช่องบังคับว่าง · period_to < period_from · pct นอก 0–100 · งบ < 0 · performance ไม่มีแถวที่มีข้อมูล · แถวที่มีข้อมูลขาดช่องบังคับ · overall=delayed ∧ issues ว่าง
- warnings (ไม่บล็อก · BR-05/06): delayed ∧ decisions ว่าง · at_risk ∧ issues ว่าง · report_date < period_to · รอบทับรายงาน (≠ cancelled) ของ project_plan เดียวกัน · budget_actual > budget_plan · due_date < report_date
### F-TMP-005-FN-02: loadProjectAndDefaults
- project_plan_id ต้องเป็น PJP สถานะ approved (API-13 · มิฉะนั้น 422 PROJECT_NOT_APPROVED) → snapshot project_code · project_name · project_manager_id/name
- ค่าเริ่ม (FE เรียกตอนเลือก · BE ไม่ทับค่าที่ผู้ใช้กรอก): performance ← actions[] (activity · plan "เสร็จ {end_date}") · schedule_plan ← start–end · budget_plan ← total_approved · kpis ← goals[].kpi — ไม่เขียนกลับ PJP (DEC-01)
### F-TMP-005-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-14): ตรวจ F-DOCCFG status ของ doc_type PPR (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('PPR', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง/หน่วยงาน + header_snapshot (Organization ชื่อ/โลโก้)
### F-TMP-005-FN-04: resolveAndSubmit
- ผู้เรียกต้องเป็น project_manager_id ของแผน (403 NOT_PROJECT_MANAGER · BR-07) · `GET /doa/resolve?feature_id=F-TMP-005&requester={pm}` → steps (ค่าเริ่ม role-line-manager ของ PM → role-gm · ไม่มีวงเงิน) · validate assignees ครบ + ≠ PM → snapshot approval_chain + doa_ref · submitted_by/at = PM · status=pending ขั้น 1 · overall=delayed → FN-09 ppr_urgent_decision
### F-TMP-005-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · คำตัดสินตาม role (decision_words.by_role) · approve ขั้น n<N → ขั้นถัดไป pending · approve ขั้น N → approved + approved_by/at + ENG-DOC-STORE.store(pdf,'PPR',id,'approved_final') · note ลง chain + audit
### F-TMP-005-FN-06: returnToDraft
- reject (เหตุผลบังคับ) → audit "{คำปฏิเสธของ role} · กลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง) · submitted_* ล้าง
### F-TMP-005-FN-07: cancelReport
- owner หรือ admin ฝ่ายพัฒนาโครงการ · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-09 ppr_cancelled (ถ้าเดิม pending)
### F-TMP-005-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company · doc · project{name, code, manager} · report{period, date} · status{*_box ☑/☐} · status_note · performance/kpis/issues/next_plan/decisions_needed เติมว่างถึง print_config.min_rows {9,8,11,10,11} · schedule · budget `#,##0.00` · owner_due "ชื่อ / d MMM yyyy" · sign_rows = ผู้จัดทำ + ผู้จัดการโครงการ (ส่งในระบบ) + 1 ช่องต่อขั้น approval_chain (sign_rows.py) · layout.dense) → render_doc.py → PDF A4 2 หน้า (parity กับ tpl_render.js)
### F-TMP-005-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **ppr_cancelled** (pending→cancelled → ผู้อนุมัติขั้นปัจจุบัน) · **ppr_draft_for_pm** (FN-11 → project_manager) · **ppr_urgent_decision** (draft→pending ∧ overall=delayed → role-gm + ผู้จัดทำ · in-app+email) — doa_pending/doa_result มาจาก DOA engine ไม่ประกาศซ้ำ
### F-TMP-005-FN-10: listVisible
- canSee = admin ฝ่ายพัฒนาโครงการ ∨ owner ∨ project_manager ของแผน ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · mine_to_submit = draft ∧ PM = ฉัน · ใบไม่มีสิทธิ์ → 404 · CSV 1 แถวต่อกิจกรรม
### F-TMP-005-FN-11: notifyProjectManager
- status=draft · ผู้เรียก = owner ที่ไม่ใช่ PM → audit "แจ้งผู้จัดการโครงการ" → FN-09 ppr_draft_for_pm

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) · F-TMP-004 read API — ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,11 | FN-10 |
| 03 | FN-01, FN-02, FN-03 |
| 04 | FN-01, FN-02 |
| 05,06 | FN-04 (+FN-09) |
| 07 | FN-05 (+FN-08) / FN-06 |
| 08 | FN-07 (+FN-09) |
| 09 | FN-11 (+FN-09) |
| 10 | FN-08 |
| 13 | FN-02 |
ทุก FN มี API ผูก ✓ (FN-09 ถูกเรียกจาก FN-04/07/11)
