# 03_LOGIC — F-TMP-006
> ไม่มีค่าคงที่บนกระดาษ (FORM_SPEC.constants = 0) · เกณฑ์คะแนนต่ำอ่านจาก config (Sales Configuration · ค่าเริ่ม 2)

## §3.1 Functions (Scope-Local)
### F-TMP-006-FN-01: validateEval
- Input `{period_month, customer_id, contact_person, scores, ...}` → VR-01..03 (05 §5.4) · score ∈ {1..5} · q_key ∈ q1…q10 · contact_person trim ≤ 120 · period_month ค่าเริ่ม = เดือนปัจจุบัน (DEC-13)
### F-TMP-006-FN-02: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-09): ตรวจ F-DOCCFG status ของ doc_type SEA (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('SEA', company_ctx)` → snapshot `customer_name_snapshot` (Customer master) + `header_snapshot` (Organization: ชื่อบริษัทภาษาอังกฤษ · โลโก้) · ห้าม format/+1 เอง
### F-TMP-006-FN-03: recordEval
- เฉพาะเจ้าของ · status = draft · ตอบครบ 10 คีย์ (q1…q10) ไม่งั้น 422 SCORES_INCOMPLETE (BR-02) → status = recorded · recorded_at · audit "บันทึกผลแบบประเมิน" · ไม่มีขั้นพิจารณา (DEC-03 · DOA resolve = 0 ขั้น) → response `approver_role` = null · `approved_by` = null · `approval_chain` = [] · `TODO: DOA engine` (ถ้ามติเปลี่ยน ให้ resolve จาก DOA กลาง ไม่ hardcode) → FN-06
### F-TMP-006-FN-04: computeLowScore
- low_count = จำนวนข้อที่ score ≤ `SalesConfig.sa_eval_low_threshold` (ค่าเริ่ม 2 · OQ-03) · avg รวม/ต่อกลุ่ม = ค่าเฉลี่ยข้อที่ตอบ (แสดงผล/list/CSV เท่านั้น — ไม่เก็บ · ไม่พิมพ์ · BR-10)
### F-TMP-006-FN-05: cancelEval
- เจ้าของ หรือ role-mgr-sales · status ∈ {draft, recorded} · เหตุผลบังคับ → cancelled · audit (append-only) → FN-06 sea_cancelled (เมื่อผู้ยกเลิก ≠ เจ้าของ)
### F-TMP-006-FN-06: emitEvents
- `ENG-NOTIFY.emit`: **sea_low_score_recorded** (draft→recorded และ low_count > 0 → role-mgr-sales · vars: doc_no, customer_name, low_count, period_month) · **sea_cancelled** (→cancelled โดยไม่ใช่เจ้าของ → เจ้าของ · vars: doc_no, actor, reason) · ไม่มี doa_* · ไม่ส่งต่อระบบอื่น (DEC-02)
### F-TMP-006-FN-07: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company{name,logo} · doc{title,no,is_draft,is_cancelled,form_code,revision} · period_month_text (เดือนอังกฤษ ค.ศ. "March 2026") · customer.name · contact_person · groups[3].{name, items[].{label,s1..s5 = "✓"/""}} ตาม print_config.score_groups · comment_lines (ตัดบรรทัด ~105 ตัวอักษร เติมว่างให้ครบ print_config.min_rows = 5) · sign_rows (DOA snapshot 0 ขั้น → [] · DEC-07) · layout.dense เมื่อ feedback > 5 บรรทัด) → render logic-less (parity กับ tpl_render.js) · ไม่เก็บสำเนา PDF (snapshot flags = ✗)
### F-TMP-006-FN-08: listVisible
- canSee = role-mgr-sales ∨ owner (ร่างของคนอื่นไม่เห็น) · count ต่อสถานะสำหรับ tabs · ใบไม่มีสิทธิ์ → 404 · CSV ใส่หัวคอลัมน์คะแนนเป็นถ้อยคำอังกฤษตามกระดาษ

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-NOTIFY · Customer master API (อ่าน) — ไม่มี engine ใหม่ · ไม่ใช้ ENG-DOC-STORE (เอกสารภายใน) · DOA engine: ไม่เรียก (DEC-03) — TODO: DOA engine ถ้ามติเปลี่ยน

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01, 02, 08 | FN-08 (+FN-04 avg) |
| 03 | FN-01, FN-02 |
| 04 | FN-01 |
| 05 | FN-03, FN-04, FN-06 |
| 06 | FN-05, FN-06 |
| 07 | FN-07 |
ทุก FN มี API ผูก ✓
