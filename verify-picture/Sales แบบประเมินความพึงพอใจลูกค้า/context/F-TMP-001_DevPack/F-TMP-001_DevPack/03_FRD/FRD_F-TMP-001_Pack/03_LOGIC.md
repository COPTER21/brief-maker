# 03_LOGIC — F-TMP-001
> ไม่มีค่าคงที่บนกระดาษ (FORM_SPEC.constants = 0) · ชื่อบริษัทอ่าน Organization เท่านั้น (DEC-04 · DEC-11)

## §3.1 Functions (Scope-Local)
### F-TMP-001-FN-01: validateEvaluation
- mode `draft`: store.name บังคับ (VR-01) · mode `submit`: + business_type (VR-02) · relationship_years (VR-03) · rating 9 ข้อเป็นจำนวนเต็ม 1–5 ครบ (VR-04 · DEC-13) · enum ตรวจค่าที่อนุญาตเท่านั้น (DEC-12)
### F-TMP-001-FN-02: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-09): ตรวจ F-DOCCFG status ของ doc_type CSE (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('CSE', company_ctx)` → `header_snapshot` (Organization: legal_name · logo) · ห้าม format/+1 เอง
### F-TMP-001-FN-03: submitEvaluation
- เจ้าของ · status=draft · FN-01(submit) ผ่าน → `GET /doa/resolve?feature_id=F-TMP-001` (DOA-ENGINE-HOOK) → ค่าเริ่มต้น 0 ขั้น (DEC-03) → status=submitted · submitted_at · audit "ส่งแบบประเมิน" → FN-05
- ถ้า DOA กลางตั้งขั้นให้ CSE ภายหลัง = นอก scope รอบนี้ (EC-08) → ต้องทำ DOA_BRIEF + state รอพิจารณา เป็น enhancement · prototype มี hook รองรับแล้ว (TODO: DOA engine)
### F-TMP-001-FN-04: cancelEvaluation
- เจ้าของ หรือ role-mgr-sales · status ∈ {draft, submitted} · เหตุผลบังคับ → cancelled · cancel_reason · audit
### F-TMP-001-FN-05: emitEvents
- `ENG-NOTIFY.emit('cse_submitted', {ref: id, vars:{doc_no, store_name, overall}})` ที่ draft→submitted · ไม่ยิง `cse.submitted` ไป CRM (DEC-02)
### F-TMP-001-FN-06: docPrintData + renderPdf
- data contract ตรงคีย์ `print/form.tpl.html`: company{name ← header_snapshot.legal_name, logo} · doc{title = "แบบฟอร์มประเมินความพึงพอใจของ" + legal_name, no, is_draft, form_code ← print_config, revision ← print_config} · store.name · partner.company_name (= legal_name) · business_type.{hypermarket,supermarket,wholesales,convenience}_box (☑/☐) · relationship_years.{lt1,y1_3,y3_5,gt5}_box · rating.{9 คีย์} (string "1"–"5" หรือ "") · suggestion · sign_rows[] = ผู้ประเมิน 1 ช่อง (date = "ส่งในระบบ วันที่ เวลา" หรือเส้นประ) แบ่งแถวตาม print_config.sign_layout.max_per_row · layout.dense เมื่อข้อเสนอแนะยาว
- render logic-less (parity กับ tpl_render.js — parity_check IDENTICAL 5/5) · ไม่เก็บสำเนา (snapshot flags false)
### F-TMP-001-FN-07: exportCsv
- คอลัมน์: เลขที่ · วันที่ · ห้าง/ร้านค้า · บริษัทคู่ค้า · ประเภทธุรกิจ · ระยะเวลา · 9 หัวข้อ · ข้อเสนอแนะ · ผู้บันทึก · สถานะ · ตามตัวกรอง + สิทธิ์ FN-08 · UTF-8 BOM
### F-TMP-001-FN-08: listVisible
- canSee = role-mgr-sales ∨ owner (ไม่มีสายพิจารณา) · ใบไม่มีสิทธิ์ → 404 · filter q/status/business_type · sort doc_no/created_at/rating_overall
### F-TMP-001-FN-09: attachFiles
- Document Center `ref_type='CSE'` · pdf/jpg/png ≤10 MB (VR-06) · เฉพาะ draft ของเจ้าของ

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-NOTIFY · DOA resolve (F-DLG-001 · hook) — ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01, 02 | FN-08 |
| 03 | FN-01, FN-02 |
| 04 | FN-01 |
| 05 | FN-01, FN-03, FN-05 |
| 06 | FN-04 |
| 07 | FN-06 |
| 08 | FN-07 |
| 09 | FN-09 |
ทุก FN มี API ผูก ✓
