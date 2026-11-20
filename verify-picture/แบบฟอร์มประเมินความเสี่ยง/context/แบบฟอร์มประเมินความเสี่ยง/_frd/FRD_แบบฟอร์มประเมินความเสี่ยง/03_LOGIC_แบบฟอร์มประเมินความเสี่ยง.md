# 03_LOGIC — F-TMP-002
> ไม่มีค่าคงที่ของเกณฑ์ใน logic — อ่าน RiskMatrix config เท่านั้น (DEC-04)

## §3.1 Functions (Scope-Local)
### F-TMP-002-FN-01: validateAssessment
- Input `{items[]}` → errors VR-01..02 (05 §5.4) · ≥1 item · residual_score ต้องอยู่ใน RiskMatrix config ชุดผลคูณ (ตัดค่าที่คูณไม่ได้ — DEC-12) · status ปิดแล้ว ต้องมี residual_score
### F-TMP-002-FN-02: computeScores
- inherent_score = likelihood × impact (ทั้งคู่มีค่าเท่านั้น ไม่งั้น null — DEC-14) · level_key = band จาก RiskMatrix.level_bands (config) · residual_over_inherent = residual > inherent (เตือน ไม่บล็อก — DEC-13) · ทำซ้ำฝั่ง server เสมอ (ไม่เชื่อค่าจาก FE)
### F-TMP-002-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type RSK (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('RSK', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง/ฝ่าย + `header_snapshot` (Organization: ชื่อบริษัท · โลโก้ · บรรทัดบริษัทในเครือ) · ห้าม format/+1 เอง
### F-TMP-002-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-002` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง · role-gm ตาม DOA กลาง · ผู้ resolve ได้ = ผู้จัดทำ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-002-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved → ขั้นถัดไป pending หรือ status=approved (ครบ) → FN-08 render + `ENG-DOC-STORE.store(pdf,'RSK',id,'approved_final')` → FN-09
### F-TMP-002-FN-06: returnToDraft
- reject (เหตุผลบังคับ) → audit "{คำปฏิเสธของขั้น} — ส่งกลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08)
### F-TMP-002-FN-07: cancelAssessment
- owner หรือ admin_role ฝ่ายพัฒนาธุรกิจ · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-09 rsk_cancelled (ถ้าเดิม pending)
### F-TMP-002-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company{name,logo,group_line} · doc{title,no,is_draft,form_code,revision} · criteria[] จาก RiskMatrix scale · level_rows[] จาก RiskMatrix.level_bands (2 ช่วงต่อแถว) · risks_p1[] = แถวที่ 1..print_config.rows_page1 · risks_p2[] = ที่เหลือ (เติมแถวว่างจนครบ print_config.min_rows) · has_p2_rows · sign_rows[] = ผู้จัดทำ + 1 ช่องต่อขั้นใน approval_chain snapshot (**จำนวนตาม DOA ไม่ fix**) · คำตัดสินจาก print_config.decision_words.by_role[role_id] หรือ default · form_revisions[] จาก DocumentConfig (F003) · layout.dense เมื่อรายการ > min_rows หรือขั้น DOA > 4) → render logic-less (parity กับ tpl_render.js) · ทุกสถานะ 2 หน้า (R10)
### F-TMP-002-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **rsk_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · **rsk_very_high_approved** (→approved และมี item ที่ inherent หรือ residual อยู่ในช่วงสูงสุดของ RiskMatrix.level_bands config → ผู้จัดทำ · in-app+email) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ
### F-TMP-002-FN-10: listVisible
- canSee = admin_role ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · level filter = band ของ max(inherent) · ใบไม่มีสิทธิ์ → 404

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
