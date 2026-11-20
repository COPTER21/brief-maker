# 03_LOGIC — F-TMP-003
> ไม่มีค่าคงที่ของเกณฑ์/น้ำหนัก/เกณฑ์ผลเสนอใน logic — อ่าน ScreeningCriteria config เท่านั้น (DEC-04)

## §3.1 Functions (Scope-Local)
### F-TMP-003-FN-01: validateScreening
- Input `{criteria[], summary}` → errors VR-01..03 (05 §5.4) · criteria ครบทุก item ของ snapshot · score เป็นจำนวนเต็ม 1..ScreeningCriteria.score_max (ไม่รับ ผ่าน/ไม่ผ่าน — DEC-12) · strengths · concerns · decision บังคับ · conditions บังคับเมื่อ decision = ดำเนินการต่อแบบมีเงื่อนไข (DEC-15) หรือ decision_mismatch (DEC-14)
### F-TMP-003-FN-02: computeScores
- weighted_score = weight_pct_snapshot × score ÷ ScreeningCriteria.score_max (มี score เท่านั้น ไม่งั้น null) · total_score = Σ weighted_score เมื่อให้คะแนนครบทุกเกณฑ์ ไม่งั้น null (DEC-13) · recommendation = band แรกใน ScreeningCriteria.recommend_bands ที่ total_score ≥ min (config) · decision_mismatch = decision ≠ band.decision (เตือน ไม่บล็อก) · ทำซ้ำฝั่ง server เสมอ (ไม่เชื่อค่าจาก FE)
### F-TMP-003-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type SCR (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('SCR', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง/ฝ่าย + `header_snapshot` (Organization: ชื่อบริษัท · โลโก้ · บรรทัดบริษัทในเครือ) + เกณฑ์/น้ำหนักจาก ScreeningCriteria.items ณ เวลาสร้าง · ห้าม format/+1 เอง
### F-TMP-003-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-003` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง · role-gm ตาม DOA กลาง · ผู้ resolve ได้ = ผู้จัดทำ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-003-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved → ขั้นถัดไป pending หรือ status=approved (ครบ) → FN-08 render + `ENG-DOC-STORE.store(pdf,'SCR',id,'approved_final')` → FN-09
### F-TMP-003-FN-06: returnToDraft
- reject (เหตุผลบังคับ) → audit "{คำปฏิเสธของขั้น} — ส่งกลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08)
### F-TMP-003-FN-07: cancelScreening
- owner หรือ admin_role ฝ่ายพัฒนาธุรกิจ · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-09 scr_cancelled (ถ้าเดิม pending)
### F-TMP-003-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company{name,logo,group_line} · doc{title,no,is_draft,form_code,revision} · criteria[]{criterion,weight,score,weighted_score,rationale,risk_condition} จาก snapshot · screening{total_score,recommendation} · summary{strengths,concerns,info_needed,decision,conditions,next_steps} · sign_rows[] = ผู้จัดทำ + 1 ช่องต่อขั้นใน approval_chain snapshot (**จำนวนตาม DOA ไม่ fix**) · คำตัดสินจาก print_config.decision_words.by_role[role_id] หรือ default · form_revisions[] จาก DocumentConfig (F003) · layout.dense เมื่อขั้น DOA > 4) → ทุกค่าเป็น string จัดรูปแล้ว (ว่าง = "") → render logic-less (parity กับ tpl_render.js) · ทุกสถานะ 2 หน้า (R10)
### F-TMP-003-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **scr_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · **scr_not_proceed_approved** (→approved และ decision = ไม่ดำเนินการต่อ → ผู้จัดทำ · in-app+email · ข้อความชี้ให้ทำ FM-BDM-04) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ
### F-TMP-003-FN-10: listVisible
- canSee = admin_role ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · filter decision / dept / status · sort total_score · ใบไม่มีสิทธิ์ → 404

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
