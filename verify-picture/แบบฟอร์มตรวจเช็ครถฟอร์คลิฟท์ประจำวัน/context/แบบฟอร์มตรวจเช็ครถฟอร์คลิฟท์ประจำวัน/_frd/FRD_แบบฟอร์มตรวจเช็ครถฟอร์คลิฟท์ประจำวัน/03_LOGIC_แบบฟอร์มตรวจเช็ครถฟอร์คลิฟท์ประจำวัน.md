# 03_LOGIC — F-TMP-002
> ไม่มีรายการตรวจ/จำนวนแถวตายตัวใน logic — อ่านจาก ForkliftChecklistConfig และปฏิทินของเดือนเท่านั้น (DEC-04)

## §3.1 Functions (Scope-Local)
### F-TMP-002-FN-01: validateInspection
- Input `{vehicle_type, inspection_month, results[]}` → errors VR-01..04 (05 §5.4): vehicle_type ∈ {fuel, electric} · month ≤ เดือนปัจจุบัน · day ≤ จำนวนวันของเดือน และ ≤ วันนี้ (DEC-15) · section ∈ {general, vehicle_type} (DEC-14) · วันที่มีผลต้องครบทุก item ของ section ที่ใช้ · ≥1 วันครบ
### F-TMP-002-FN-02: loadChecklist
- อ่าน `ForkliftChecklistConfig.items` (general/fuel/electric · ลำดับ + ถ้อยคำ) ณ วันสร้าง → snapshot ลง `forklift_inspection.checklist_snapshot` · ใบเดิมไม่เปลี่ยนเมื่อ config เปลี่ยน (EC-09)
### F-TMP-002-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-12): ตรวจ F-DOCCFG status ของ doc_type FLI (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('FLI', company_ctx)` → snapshot ผู้ตรวจสอบ/ตำแหน่ง/แผนก + `header_snapshot` (Organization: ชื่อบริษัท ที่อยู่ โลโก้) · ห้าม format/+1 เอง
### F-TMP-002-FN-04: saveResults
- upsert ผลรายวัน (แทนที่ทั้งวันที่ส่งมา) · เปลี่ยน vehicle_type = ลบผล section เดิมที่ไม่ใช่ general (DEC-14) · เปลี่ยนเดือน = ลบผลทั้งหมด · นับ ng ก่อน/หลัง → ng เพิ่ม → FN-10 `fli_defect_found` (DEC-16)
### F-TMP-002-FN-05: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-002` → steps (ไม่มีวงเงิน) · role-supervisor = หัวหน้างานตามผังองค์กร (relative · OQ-05) · ผู้ resolve ได้ = ผู้ตรวจสอบเอง → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้ตรวจสอบ → snapshot `approval_chain` (freeze BR-DOA-02) · status draft/returned→pending ขั้น 1
### F-TMP-002-FN-06: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved → ขั้นถัดไป pending หรือ status=approved (ครบ) → FN-09 render + `ENG-DOC-STORE.store(pdf,'FLI',id,'approved_final')` · คำตัดสินแสดงตาม `print_config.decision_words.by_role`
### F-TMP-002-FN-07: returnToDraft
- reject (เหตุผลบังคับ) → audit "ส่งกลับแก้ไข" + returned_by/at/reason · status=returned (แก้ได้เหมือนร่าง · เลขเดิม) · ขั้นที่เหลือ = skipped · approval_chain เดิมเก็บใน audit แล้ว resolve ใหม่ตอนส่ง (DEC-10)
### F-TMP-002-FN-08: cancelInspection
- owner หรือ role-mgr-wh · status ∈ {draft, pending, returned} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-10 `fli_cancelled` (ถ้าเดิม pending)
### F-TMP-002-FN-09: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (FLI_data-contract.md): company (header_snapshot) · doc{title,title_en,no,is_draft,form_code,revision} · vehicle{fuel_box,electric_box} · inspection_month (เดือนไทย พ.ศ.) · days_hdr (หัว 1–31 ตามกระดาษ) · gen_items/fuel_items/elec_items (จาก checklist_snapshot · ช่องวันเกินเดือนหรือ section ที่ไม่ได้ใช้ = "") · sign_rows (`sign_rows.py`: ผู้ตรวจสอบ + 1 ช่อง/ขั้น approval_chain · แถวละ ≤ print_config.sign_layout.max_per_row) · layout.dense → render `form.tpl.html` ด้วย render_doc (= tpl_render.js) → A4 2 หน้า (R10)
### F-TMP-002-FN-10: emitEvents
- `ENG-NOTIFY.emit`: **fli_defect_found** (บันทึกที่ ng เพิ่ม → role-supervisor ของผู้ตรวจสอบ · บังคับ · in-app+email) · **fli_cancelled** (pending→cancelled → ผู้อนุมัติขั้นปัจจุบัน) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ · `fli.defect_recorded` ประกาศไว้ไม่ยิง (DEC-02)
### F-TMP-002-FN-11: listVisible
- canSee = role-mgr-wh ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · ใบไม่มีสิทธิ์ → 404 · สรุปต่อใบ: done_days · ng_count

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,10 | FN-11 |
| 03 | FN-01, FN-02, FN-03 |
| 04 | FN-01, FN-04 (+FN-10) |
| 05,06 | FN-05 |
| 07 | FN-06 (+FN-09) / FN-07 |
| 08 | FN-08 (+FN-10) |
| 09 | FN-09 |
| 12 | FN-02 |
ทุก FN มี API ผูก ✓
