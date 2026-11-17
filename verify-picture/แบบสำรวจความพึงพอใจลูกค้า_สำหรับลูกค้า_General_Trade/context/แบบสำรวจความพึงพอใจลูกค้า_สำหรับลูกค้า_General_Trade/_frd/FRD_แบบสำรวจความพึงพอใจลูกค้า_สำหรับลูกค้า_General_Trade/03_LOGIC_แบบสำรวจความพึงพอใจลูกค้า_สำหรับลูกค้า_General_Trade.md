# 03_LOGIC — F-TMP-001
> ไม่มีค่าคงที่บนกระดาษ (FORM_SPEC.constants = 0) · เกณฑ์คะแนนต่ำอ่านจาก config (Sales Configuration · ค่าเริ่ม 2)

## §3.1 Functions (Scope-Local)
### F-TMP-001-FN-01: validateSurvey
- Input `{customer_id, survey_date, period_month, scores, ...}` → VR-01..03 (05 §5.4) · score ∈ {1..5} · survey_date ≤ วันนี้ · period_month ≠ เดือนของ survey_date → warning `DATE_OUTSIDE_MONTH` (ไม่บล็อก · DEC-13)
### F-TMP-001-FN-02: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-09): ตรวจ F-DOCCFG status ของ doc_type CSG (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('CSG', company_ctx)` → snapshot `customer_name_snapshot` (Customer master) + `header_snapshot` (Organization: ชื่อบริษัท · โลโก้) · ห้าม format/+1 เอง
### F-TMP-001-FN-03: recordSurvey
- เฉพาะเจ้าของ · status = draft · ตอบครบ 16 คีย์ (q1_1…q3_8) ไม่งั้น 422 SCORES_INCOMPLETE (BR-02) → status = recorded · recorded_at · audit "บันทึกผลแบบสำรวจ" · ไม่มีขั้นพิจารณา (DEC-03 · DOA resolve = 0 ขั้น) → FN-06
### F-TMP-001-FN-04: computeLowScore
- low_count = จำนวนข้อที่ score ≤ `SalesConfig.survey_low_score_threshold` (ค่าเริ่ม 2 · OQ-03) · avg = ค่าเฉลี่ยข้อที่ตอบ (แสดงผล/list/CSV เท่านั้น — ไม่เก็บ · ไม่พิมพ์ · BR-10)
### F-TMP-001-FN-05: cancelSurvey
- เจ้าของ หรือ role-mgr-sales · status ∈ {draft, recorded} · เหตุผลบังคับ → cancelled · audit (append-only) → FN-06 csg_cancelled (เมื่อผู้ยกเลิก ≠ เจ้าของ)
### F-TMP-001-FN-06: emitEvents
- `ENG-NOTIFY.emit`: **csg_low_score_recorded** (draft→recorded และ low_count > 0 → role-mgr-sales · vars: doc_no, customer_name, low_count, period_month) · **csg_cancelled** (→cancelled โดยไม่ใช่เจ้าของ → เจ้าของ · vars: doc_no, actor, reason) · ไม่มี doa_* · ไม่ส่งต่อระบบอื่น (DEC-02)
### F-TMP-001-FN-07: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company · doc{title,no,is_draft,is_cancelled,form_code,revision} · period_month_text (เดือนเต็ม พ.ศ.) · survey_date_text (วัน เดือนเต็ม พ.ศ.) · customer.name · contact.dept/phone · sections[3].items[].{label,s5..s1 = "✓"/""} · comment_staff_lines/comment_other_lines (ตัดบรรทัด ~105 ตัวอักษร เติมว่างให้ครบ print_config.min_rows = 3) · sign_rows (จาก DOA snapshot = 0 ขั้น → [] · DEC-07) · layout.dense เมื่อข้อเสนอแนะ > 3 บรรทัด) → render logic-less (parity กับ tpl_render.js) · ไม่เก็บสำเนา PDF (snapshot flags = ✗)
### F-TMP-001-FN-08: listVisible
- canSee = role-mgr-sales ∨ owner (ร่างของคนอื่นไม่เห็น) · count ต่อสถานะสำหรับ tabs · ใบไม่มีสิทธิ์ → 404 · CSV ไม่รวม contact_phone

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-NOTIFY · Customer master API (อ่าน) — ไม่มี engine ใหม่ · ไม่ใช้ ENG-DOC-STORE (เอกสารภายใน)

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
