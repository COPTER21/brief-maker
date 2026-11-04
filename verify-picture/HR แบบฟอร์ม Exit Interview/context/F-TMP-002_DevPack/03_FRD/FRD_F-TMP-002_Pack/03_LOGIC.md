# 03_LOGIC — F-TMP-002
> ไม่มีค่าคงที่ตัวเลขบนกระดาษ (FORM_SPEC.constants ว่าง) · ถ้อยคำประเด็น/ปัจจัย = master ของแบบฟอร์ม Rev.00 (mdoc v1) ไม่ hardcode ใน logic

## §3.1 Functions (Scope-Local)
### F-TMP-002-FN-01: prefillEmployee
- อ่าน Employee (F-EMP-001) + OrgUnit/Position (F-ORG-001) → snapshot: full_name, employee_code, position, division, department, hire_date · ค่าเริ่ม probation_status, employment_type, education_degree, education_major · ไม่มีค่า = ว่าง (กรอกเอง)
- เรียก FN-02.calc เพื่อเติม age_years / service_years / service_months
### F-TMP-002-FN-02: validateAndCalc
- calc (DEC-04): ref_date = resign_date (sep_type=resign) หรือ Employee.contract_end_date (contract_end) หรือวันนี้ · age_years = ปีเต็ม(birth_date→ref_date) · service = ปี/เดือนเต็ม(hire_date→ref_date) · calc_manual=true = ไม่คำนวณทับ
- validate (ใช้ทั้ง save draft และ submit — draft ตรวจเฉพาะ employee_id): VR-01..VR-09 (05 §5.4) · ทำซ้ำฝั่ง server เสมอ
### F-TMP-002-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type EXI (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('EXI', company_ctx)` → snapshot ข้อมูลพนักงาน + `header_snapshot` (Organization: ชื่อบริษัท โลโก้) · ห้าม format/+1 เอง · owner_id = ผู้สร้าง
### F-TMP-002-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-002` → steps (ค่าเริ่ม 0 · DEC-03) · validate FN-02 ครบ (VR-02..VR-08) · assignees ครบทุกขั้น ≠ ผู้ให้ข้อมูล
- 0 ขั้น (ค่าเริ่ม): status draft→**submitted** · submitted_at · emit `exi_submitted` (FN-09)
- N ขั้น: ไม่อยู่ในรอบนี้ (DEC-03) — ถ้า OQ-02 เปลี่ยน ใช้ pattern DOA มาตรฐาน (approval_chain snapshot · BR-DOA-02)
### F-TMP-002-FN-05: acknowledgeStep (ไม่ใช้รอบนี้ — DEC-03 · สำรองสำหรับ OQ-02)
- ถ้าลูกค้าเพิ่มขั้นภายหลังเท่านั้น · เฉพาะ assignee ขั้นปัจจุบัน (มีเมื่อ DOA ตั้งขั้น) · ขั้น→approved · ถัดไป pending หรือ status=approved → approved_by/at · `ENG-DOC-STORE.store(pdf,'EXI',id,'approved_final')` เฉพาะเมื่อ flag snapshot.approved_final เปิดที่ F-DOCCFG (ค่าเริ่มปิด)
### F-TMP-002-FN-06: returnToDraft (ไม่ใช้รอบนี้ — DEC-03 · สำรองสำหรับ OQ-02)
- ส่งกลับ (เหตุผลบังคับ) → status=draft เลขเดิม (policy G7) · chain เดิมลง audit แล้วล้าง (resolve ใหม่ตอนส่ง) · ใช้ BR-DOA-03 ตามมาตรฐาน (reject → draft)
### F-TMP-002-FN-07: cancelInterview
- owner/informant หรือ role-mgr-hr · status ∈ {draft, submitted, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-09 `exi_cancelled` (เมื่อเดิม submitted/pending)
### F-TMP-002-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (print/EXI_data-contract.md): company (header_snapshot) · doc · employee · service · probation/employment_type/separation/contract_end_reason (glyph ☑☐) · rate.qNN.c5..c1 ("✓"/"") · reason.rNN ("[n]"/"☐") + reason.other_text · improvements (เติมว่างถึง print_config.min_rows=5) · other_comments · sign_rows[] = ผู้ให้ข้อมูล + 1 ช่องต่อขั้นใน approval_chain (จำนวนตาม DOA ไม่ fix · แถวละ ≤ print_config.sign_layout.max_per_row) · layout.dense เมื่อแถว > min_rows → render logic-less (parity กับ tpl_render.js)
### F-TMP-002-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **exi_submitted** (draft→submitted · ผู้รับ role-mgr-hr · ข้อความไม่ใส่คำตอบ) · **exi_cancelled** (submitted/pending→cancelled · HR + ผู้สร้าง) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ
### F-TMP-002-FN-10: listVisible
- canSee = role-mgr-hr ∨ owner_id=ฉัน ∨ employee_id=ฉัน ∨ (status≠draft ∧ อยู่ใน approval_chain) · ผู้บังคับบัญชาไม่มีสิทธิ์โดยตำแหน่ง (DEC-17) · ใบไม่มีสิทธิ์ → 404 · CSV ใช้เงื่อนไขเดียวกัน

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) · Document Center — ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| FN | API |
|---|---|
| FN-01 | API-03 |
| FN-02 | API-03, 04, 05, 07 |
| FN-03 | API-04 |
| FN-04 | API-06, 07 |
| FN-05 / FN-06 | API-08 |
| FN-07 | API-09 |
| FN-08 | API-10 |
| FN-09 | (จาก FN-04, FN-07) |
| FN-10 | API-01, 02, 11 |
ทุก FN มี API ผูก ✓
