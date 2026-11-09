# 03_LOGIC — F-TMP-004
> ไม่มีค่าคงที่ธุรกิจใน logic — สาย DOA จาก DOA กลาง · เลข/แบบพิมพ์จาก F-DOCCFG (DEC-03/10)

## §3.1 Functions (Scope-Local)
### F-TMP-004-FN-01: validateRequest
- Input `{device_type, device_type_other, item_name, asset_code, problem, due_date, delivery_location}` → errors VR-01..06 (05 §5.4) · due_date < report_date → warning (ไม่ error · BR-03)
### F-TMP-004-FN-02: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type CRR (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('CRR', company_ctx)` → doc_date = วันนี้ · snapshot ชื่อ/ตำแหน่งผู้แจ้งซ่อม + `header_snapshot` (Organization: ชื่อบริษัท โลโก้) · ห้าม format/+1 เอง
### F-TMP-004-FN-03: report
- เจ้าของ · draft → reported · report_date = now · ล็อกแก้ไขส่วนที่ 1 → emit `crr_reported` (→ role-it-officer)
### F-TMP-004-FN-04: receive
- role-it-officer · reported → inspecting · received_by = ผู้ใช้ · received_at = now → emit `crr_received` (→ ผู้แจ้งซ่อม)
### F-TMP-004-FN-05: saveInspection
- role-it-officer · inspecting · validate VR-07..09 · check_result ไม่ใช่ 3 ตัวเลือกล่าง → ล้าง claim_* · claim_period_to < claim_period_from → warning (BR-03) · บันทึก inspected_by · audit "บันทึกผลตรวจเช็ค" (บันทึกซ้ำได้จนกว่าจะส่ง)
### F-TMP-004-FN-06: resolveAndSubmit
- role-it-officer · inspecting · ผลตรวจเช็คครบ (ไม่ครบ → 422 INSPECTION_INCOMPLETE) → `GET /doa/resolve?feature_id=F-TMP-004` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาของ**ผู้ส่ง** (เจ้าหน้าที่ IT) ตามผัง · ไม่มีผู้บังคับบัญชา → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้ส่ง → snapshot `approval_chain` (freeze BR-DOA-02) · status inspecting→pending ขั้น 1 · approval_submitted_at = now · ล้าง returned_*
- หมายเหตุ BR-DOA-01: `inspecting` = draft ของขั้นอนุมัติ (ร่างผลตรวจเช็คส่วนที่ 2) — DOA ส่งได้จากสถานะนี้เท่านั้น
### F-TMP-004-FN-07: decideStep (approve)
- เฉพาะ assignee ขั้นปัจจุบัน · ขั้นนั้น approved → ขั้นถัดไป pending หรือ status=approved (ครบ = รอผลซ่อม) → FN-12 render + `ENG-DOC-STORE.store(pdf,'CRR',id,'approved_final')` · ไม่เปลี่ยนค่าในระบบ/ไม่ส่งต่อ (DEC-01/02) · DOA engine แจ้ง doa_result
### F-TMP-004-FN-08: returnToInspecting (reject)
- เหตุผลบังคับ → audit "ไม่อนุมัติ — กลับร่างผลตรวจเช็ค" + returned_by/at/reason · status=inspecting เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08 · BR-DOA-03) · ผลตรวจเช็คเดิมคงไว้ให้ IT แก้
### F-TMP-004-FN-09: recordRepair
- role-it-officer · approved → repaired · repair_result (VR-11) · repair_note บังคับเมื่อ unfixable (VR-12) · repaired_by/at → FN-12 render ใหม่ → emit `crr_repaired` (→ ผู้แจ้งซ่อม)
### F-TMP-004-FN-10: acknowledge
- เจ้าของ · repaired → closed · acknowledged_at = now · ล็อกเอกสาร · FN-12 render ฉบับสุดท้าย
### F-TMP-004-FN-11: cancelRequest
- เจ้าของ หรือ role-it-officer · status ∈ {draft, reported, inspecting, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → emit `crr_cancelled` (ถ้าเดิม pending → ผู้พิจารณาขั้นปัจจุบัน)
### F-TMP-004-FN-12: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (ดู print-spec §8): company(header_snapshot) · doc{title,no,is_draft,form_code,revision ← print_config} · doc_date · report_date · employee{name,position} · due_date · delivery_location · device_type{4 keys → ☑/☐} · device_type_other · item_name · asset_code · problem_lines (แตก \n · เติมว่างถึง text_min_rows 2) · signs_part1 [ผู้แจ้งซ่อม · ผู้รับแจ้ง] · repair_date · check_result{done,in_progress} · claim_sets[3] (☑ + ค่าเฉพาะชุดที่เลือก) · sign_rows (ผู้ดำเนินการ + 1 ช่อง/ขั้น approval_chain · แถวละ ≤ sign_layout.max_per_row · คำตัดสินจาก decision_words.by_role) · repair_result{fixed,unfixable} · repair_note_lines (≥2) · signs_part3 [ผู้ดำเนินการ · ผู้แจ้งซ่อม] · layout.dense
- render server = `render_doc.py` (ผลตรง tpl_render.js — parity IDENTICAL) · 2 หน้า A4 (R10)
### F-TMP-004-FN-13: listVisible + emitNotify
- filter ตามสิทธิ์ (DEC-09): role-it-officer = ทั้งหมด · อื่น = ของตน + ใบที่ status ≠ draft และอยู่ใน approval_chain · tab todo = งานที่ผู้ใช้ต้องทำตามสถานะ · tab mine = ของตน · CSV ตามตัวกรอง
- `ENG-NOTIFY.emit(event_id, {ref, vars})` ตาม NTF_BRIEF — ห้ามเช็ค preference เอง

## §3.2 Engines (ใช้ของกลาง)
ENG-DOC-NUM (เลข) · ENG-DOC-STORE (สำเนา PDF) · ENG-NOTIFY (แจ้งเตือน) · DOA engine (resolve/decide hook) — ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| API-01/02 | FN-13 |
| API-03 | FN-01 → FN-02 |
| API-04 | FN-01 |
| API-05 | FN-03 → FN-13 |
| API-06 | FN-04 → FN-13 |
| API-07 | FN-05 |
| API-09 | FN-06 |
| API-10 | FN-07 / FN-08 |
| API-11 | FN-09 → FN-12 → FN-13 |
| API-12 | FN-10 → FN-12 |
| API-13 | FN-11 → FN-13 |
| API-14 | FN-12 · FN-13 |
