# 03_LOGIC — F-TMP-007
> ไม่มีค่าคงที่ใน logic — หัวข้อ · กลุ่มหัวข้อ · ป้ายสเกล · น้ำหนัก · เกณฑ์คะแนนต่ำ · จำนวนลูกค้าสูงสุด อ่านจาก SalesConfig (config) เท่านั้น (DEC-04/05)

## Functions (Scope-Local)
### F-TMP-007-FN-01: validateSummary
- Input `{period_month, columns[], conclusion, suggestion}` → errors VR-01..05 (05 §5.4) · columns ไม่ซ้ำ customer_id · จำนวน ≤ SalesConfig.ses_max_customers (8) · ทุก sea_id ต้องเป็น SEA สถานะ recorded ของ customer + period_month เดียวกัน · conclusion บังคับเฉพาะตอนส่ง (ร่างบันทึกได้) · ความยาว ≤ 1,000
### F-TMP-007-FN-02: pullSurveys
- อ่าน F-TMP-006 SEA (read-only): `status = recorded AND period_month = :period` จัดกลุ่มตาม customer → ใบล่าสุด (survey_date สูงสุด) + count · คืน customer_name · sea_doc_no · survey_date · score_q1..q10 · ใช้ทั้ง API-05 (ปุ่มดึง/เพิ่มทีละราย) และตอนบันทึก (server เติม snapshot เอง ไม่เชื่อค่าจาก FE)
### F-TMP-007-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type SES (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('SES', company_ctx)` → snapshot ผู้สรุป/ตำแหน่ง/หน่วยงาน + `header_snapshot` (Organization: ชื่อบริษัท โลโก้) + topic_text snapshot · ห้าม format/+1 เอง
### F-TMP-007-FN-04: resolveAndSubmit
- ตรวจ FN-01 (รวม conclusion) + ทุกคอลัมน์ SEA ยัง recorded (ไม่ใช่ → 422 SOURCE_SURVEY_CANCELLED) · `GET /doa/resolve?feature_id=F-TMP-007` → steps (ไม่มีวงเงิน) · ผู้ resolve ได้ = ผู้สรุป → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้สรุป → snapshot ฟิลด์อนุมัติ (02 §2.3 · freeze BR-DOA-02) · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-007-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved → ขั้นถัดไป pending หรือ status=approved (ครบ) → FN-07 render + `ENG-DOC-STORE.store(pdf,'SES',id,'approved_final')` → FN-08 (ses_low_score_approved ถ้ามีช่องคะแนนต่ำ)
### F-TMP-007-FN-06: returnToDraft / cancelSummary
- reject (เหตุผลบังคับ) → audit "ไม่อนุมัติ — กลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · สายอนุมัติเดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08 · BR-DOA-03)
- cancel: owner หรือ role-mgr-sales · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-08 ses_cancelled (ถ้าเดิม pending)
### F-TMP-007-FN-07: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (print-spec §2): company (header_snapshot) · doc · period_month_text (เดือนไทย พ.ศ.) · blocks[2] × cols[4] (name = customer_name snapshot) + rows[13] (แถวกลุ่ม grp=true จาก sea_topic_groups 3 แถว + หัวข้อ 10 แถว · topic snapshot · cells = คะแนนตัวเลข 1–5) — เติมคอลัมน์ว่างจนครบ print_config.max_rows (8) · conclusion_lines / suggestion_lines (ตัดบรรทัด ~100 ตัวอักษร · ขั้นต่ำ print_config.text_min_lines) · sign_rows[] (ผู้สรุป + 1 ช่องต่อขั้นใน snapshot สายอนุมัติ — **จำนวนตามที่ตั้งใน DOA ไม่ fix** · แถวละ ≤ print_config.sign_layout.max_per_row · คำตัดสินจาก print_config.decision_words.by_role) · layout.dense_signs → render logic-less (parity กับ tpl_render.js) · 2 หน้า (R10)
### F-TMP-007-FN-08: emitEvents
- `ENG-NOTIFY.emit`: **ses_cancelled** (pending→cancelled → ผู้อนุมัติขั้นปัจจุบัน) · **ses_low_score_approved** (→approved และมีช่อง weight ≤ เกณฑ์คะแนนต่ำใน config → owner + role-mgr-sales · ส่ง low_count + low_customers) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ · `ses.approved` ประกาศไม่ยิง (DEC-02)
### F-TMP-007-FN-09: listVisible
- canSee = role-mgr-sales ∨ owner ∨ (status≠draft ∧ อยู่ในสาย) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · ใบไม่มีสิทธิ์ → 404 · ร่างที่มีคอลัมน์ SEA ถูกยกเลิก → flag `stale_columns[]` ให้ FE แสดง banner · CSV ใช้ชุดเดียวกัน

## Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — ไม่มี engine ใหม่

## API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,10 | FN-09 |
| 03 | FN-01, FN-02, FN-03 |
| 04 | FN-01, FN-02 |
| 05 | FN-02 |
| 06 | FN-04 |
| 07 | FN-05 (+FN-07, FN-08) / FN-06 |
| 08 | FN-06 (+FN-08) |
| 09 | FN-07 |
ทุก FN มี API ผูก ✓
