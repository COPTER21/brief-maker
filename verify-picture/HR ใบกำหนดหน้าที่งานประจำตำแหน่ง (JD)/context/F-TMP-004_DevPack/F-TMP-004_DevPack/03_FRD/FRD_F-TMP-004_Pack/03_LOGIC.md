# 03_LOGIC — F-TMP-004
> ไม่มีค่าคงที่ตัวเลขบนกระดาษ (FORM_SPEC.constants ว่าง) · หัวข้อแบบฟอร์ม = Rev.00 (mdoc v1) · ไม่ hardcode สายอนุมัติ (`TODO: DOA engine`)

## §3.1 Functions (Scope-Local)
### F-TMP-004-FN-01: prefillPosition
- อ่าน Position (name_th · org_unit · reports_to) + OrgUnit (แผนก · ฝ่าย) → snapshot position_name_th, department, division · ค่าเริ่ม reports_to = Position(reports_to).name_th · ค่าเริ่ม superiors[0] = {reports_to, 1} · คืนฉบับใช้งานเดิมของตำแหน่ง (ถ้ามี) เพื่อเตือน
### F-TMP-004-FN-02: validateAndCalc
- calc (DEC-13): subordinate_summary = "N ตำแหน่ง · M คน" จากแถว subordinates ที่มี position · ไม่มี = "ไม่มี"
- validate (draft ตรวจเฉพาะ position_id · submit ตรวจครบ): VR-01..VR-08 (05 §5.4) · เตือน (ไม่บล็อก) superiors[0].position ≠ reports_to (DEC-14) · ทำซ้ำฝั่ง server เสมอ
### F-TMP-004-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-11): ตรวจ F-DOCCFG status ของ doc_type JD (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('JD', company_ctx)` → snapshot ตำแหน่ง + `header_snapshot` (Organization: ชื่อบริษัท โลโก้) · ห้าม format/+1 เอง · owner_id = ผู้สร้าง
### F-TMP-004-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-004` → steps (ค่าเริ่ม 1 ขั้น role-line-manager · DEC-03) · validate FN-02 ครบ · assignees ครบทุกขั้น ≠ owner (BR-DOA-04)
- snapshot `approval_chain` (append-only · BR-DOA-02 freeze) · approver_role = role ขั้นปัจจุบัน · status draft→**pending** · submitted_at · DOA engine ยิง doa_pending
### F-TMP-004-FN-05: approveStep
- เฉพาะ assignee ขั้นปัจจุบัน · ขั้น→approved · ถัดไป pending หรือ (ขั้นสุดท้าย) status=**approved** · approved_by/approved_at · เรียก FN-09 supersede + emit · `ENG-DOC-STORE.store(pdf,'JD',id,'approved_final')` (flag snapshot.approved_final ที่ F-DOCCFG)
### F-TMP-004-FN-06: rejectToDraft
- ไม่อนุมัติ (เหตุผลบังคับ) → status=draft เลขเดิม (DEC-09 · BR-DOA-03 มาตรฐาน) · chain เดิมลง audit แล้วล้าง (resolve ใหม่ตอนส่ง)
### F-TMP-004-FN-07: cancelJd
- owner หรือ role-mgr-hr · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → emit `jd_cancelled` (เมื่อเดิม pending)
### F-TMP-004-FN-08: docPrintData + renderPdf
- data contract ตรงคีย์ `print/form.tpl.html` (print/JD_data-contract.md): company (header_snapshot) · doc · position{name_th,name_en,department,division,reports_to} · subordinate_summary · *_lines[] (แยก \n เติมว่างถึง print_config.text_min_lines) · org_rows[] (จับคู่ superiors/subordinates ≥ print_config.min_rows=3) · sign_rows[] = ผู้จัดทำ + 1 ช่องต่อขั้นใน approval_chain (คำตัดสินตาม decision_words.by_role) + ผู้ดำรงตำแหน่ง · แถวละ ≤4 · layout.dense → render logic-less (parity กับ tpl_render.js)
### F-TMP-004-FN-09: supersedeAndEmit
- เมื่อ FN-05 ขั้นสุดท้าย: ใบอื่นของ position_id เดียวกันที่ status ∈ {approved, acknowledged} → **superseded** (superseded_by = ใบนี้) + emit `jd_superseded` · ถ้ามี acknowledged_by → emit `jd_ack_requested`
- `ENG-NOTIFY.emit` ทุก event: jd_cancelled · jd_ack_requested · jd_acknowledged · jd_superseded · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ
### F-TMP-004-FN-10: setIncumbent
- role-mgr-hr · status = approved · acknowledged_by = employee_id → emit `jd_ack_requested`
### F-TMP-004-FN-11: acknowledge
- ผู้ใช้ = acknowledged_by · status = approved → status=**acknowledged** · acknowledged_at → emit `jd_acknowledged` · อื่น 403 NOT_INCUMBENT
### F-TMP-004-FN-12: listVisible
- canSee = role-mgr-hr ∨ owner_id=ฉัน ∨ (status≠draft ∧ อยู่ใน approval_chain) ∨ (acknowledged_by=ฉัน ∧ status ∈ {approved, acknowledged, superseded}) · ใบไม่มีสิทธิ์ → 404 · CSV ใช้เงื่อนไขเดียวกัน

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) · Document Center — ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| FN | API |
|---|---|
| FN-01 | API-03 |
| FN-02 | API-04, 05, 07 |
| FN-03 | API-04 |
| FN-04 | API-06, 07 |
| FN-05 / FN-06 | API-08 |
| FN-07 | API-09 |
| FN-08 | API-10 |
| FN-09 | (จาก FN-05, FN-07, FN-10, FN-11) |
| FN-10 | API-13 |
| FN-11 | API-14 |
| FN-12 | API-01, 02, 11 |
ทุก FN มี API ผูก ✓
