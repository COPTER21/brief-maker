# 03_LOGIC — F-TMP-004
> ไม่มีหัวข้อ/คะแนนเต็ม/เกณฑ์ผ่านตายตัวใน logic — อ่านจาก VendorEvaluationConfig เท่านั้น (DEC-04)

## §3.1 Functions (Scope-Local)
### F-TMP-004-FN-01: validateEvaluation
- โหมดร่าง: vendor_name/vendor_code required · คะแนนที่กรอกต้องเป็นตัวเลข ทศนิยม ≤1 และ 0 ≤ score ≤ max_score (ไม่บังคับครบ)
- โหมดส่ง (submit): + ≥1 ประเภท (supply_goods ∨ supply_service) · ประเภทที่เลือกต้องมีรายละเอียด · คะแนนครบทุกหัวข้อ (DEC-15) · certifications มี 'other' → cert_other_text required → errors VR-01..08 (05 §5.4)
### F-TMP-004-FN-02: loadCriteria
- อ่าน `VendorEvaluationConfig` (criteria[]{text, details[], max_score} · pass_threshold · certifications[]) ณ วันสร้าง → snapshot ลง `vendor_evaluation.criteria_snapshot` · ใบเดิมไม่เปลี่ยนเมื่อ config เปลี่ยน (EC-10)
### F-TMP-004-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type VEV (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('VEV', company_ctx)` → snapshot ผู้ประเมิน/ตำแหน่ง/แผนก + `header_snapshot` (Organization: โลโก้) · ห้าม format/+1 เอง
### F-TMP-004-FN-04: saveEvaluation
- upsert header + คะแนนรายหัวข้อ · คำนวณ `score_total = Σ score` · `eval_result = all scored ? (score_total < pass_threshold ? 'fail' : 'pass') : null` (DEC-13 · ผู้ใช้ส่งค่าเองไม่ได้) · ยกเลิกประเภท = ล้างรายละเอียดของประเภทนั้น · คืน `duplicate_in_year[]` = ใบอื่นที่ vendor_code ตรง (ไม่สนตัวพิมพ์) ปีเดียวกัน status ≠ cancelled (เตือน ไม่บล็อก)
### F-TMP-004-FN-05: resolveAndSubmit
- FN-01 (โหมดส่ง) → `GET /doa/resolve?feature_id=F-TMP-004&eval_result=…` → steps ค่าเริ่ม 2 ขั้น (role-pur-officer → role-mgr-pur) · eval_result = fail → DOA กลางเพิ่มขั้น role-gm "ผู้บริหาร (กรณีไม่ผ่านการประเมิน)" (TODO: DOA engine — เงื่อนไขที่ไม่ใช่วงเงิน · DEC-14) · ผู้ resolve ได้ = ผู้ประเมินเอง → เลือกคนอื่นในกลุ่ม role · validate assignees ครบ + ≠ ผู้ประเมิน → snapshot `approval_chain` (freeze BR-DOA-02) · status draft/returned→pending ขั้น 1 · fail → FN-10 `vev_evaluation_failed`
### F-TMP-004-FN-06: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved → ขั้นถัดไป pending หรือ status=approved (ครบ) → FN-09 render + `ENG-DOC-STORE.store(pdf,'VEV',id,'approved_final')` · คำตัดสินแสดงตาม `print_config.decision_words.by_role` (role-pur-officer = เห็นด้วย/ไม่เห็นด้วย)
### F-TMP-004-FN-07: returnToDraft
- reject (ไม่เห็นด้วย/ไม่อนุมัติ · เหตุผลบังคับ) → audit + returned_by/at/reason · status=returned (แก้ได้เหมือนร่าง · เลขเดิม) · ขั้นที่เหลือ = skipped · resolve ใหม่ตอนส่ง (ผลประเมินอาจเปลี่ยน → จำนวนขั้นเปลี่ยน) (DEC-08)
### F-TMP-004-FN-08: cancelEvaluation
- owner หรือ role-mgr-pur · status ∈ {draft, pending, returned} · เหตุผลบังคับ → cancelled · ขั้น pending/waiting = skipped → FN-10 `vev_cancelled` (ถ้าเดิม pending)
### F-TMP-004-FN-09: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (VEV_data-contract.md): company.logo (header_snapshot) · doc{title,title_en,no,is_draft,form_code,revision} · vendor{name,code} · supply{goods_box,goods_specific,service_box,service_specific} · reference_no · credit_term · criteria[] (จาก criteria_snapshot: no,title,details[].t,max_score,score) · max_total · score_total · cert_rows[] (มาตรฐานซ้าย/ขวาจาก config · อื่นๆ + r_fill) · result{threshold,fail_box,pass_box} · evaluator{name,date} (ว่างจนส่ง) · evaluator_comment · sign_rows (`sign_rows.py`: ผู้ประเมิน + 1 ช่อง/ขั้น approval_chain · แถวละ ≤ print_config.sign_layout.max_per_row) · layout.dense → render ด้วย render_doc (= tpl_render.js) → A4 2 หน้า (R10)
### F-TMP-004-FN-10: emitEvents
- `ENG-NOTIFY.emit`: **vev_evaluation_failed** (ส่งใบที่ eval_result=fail → role-mgr-pur + role-gm · บังคับ · in-app+email) · **vev_cancelled** (pending→cancelled → ผู้อนุมัติขั้นปัจจุบัน) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ · `vev.evaluation_approved` ประกาศไว้ไม่ยิง (DEC-02)
### F-TMP-004-FN-11: listVisible
- canSee = role-mgr-pur ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · filter result ∈ {pass, fail, none} · ใบไม่มีสิทธิ์ → 404 · CSV มีคะแนนรายหัวข้อ

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,10 | FN-11 |
| 03 | FN-01, FN-02, FN-03 |
| 04 | FN-01, FN-04 |
| 05,06 | FN-05 (+FN-01, FN-10) |
| 07 | FN-06 (+FN-09) / FN-07 |
| 08 | FN-08 (+FN-10) |
| 09 | FN-09 |
| 12 | FN-02 |
ทุก FN มี API ผูก ✓
