# 03_LOGIC — F-TMP-003
> ค่าคงที่บนกระดาษ 1 จุด (ชื่อบริษัท) อ่านจาก Organization header_snapshot (DEC-04/DEC-13) — ไม่ hardcode ใน logic · สายอนุมัติอ่านจาก DOA กลาง (DEC-03)

## §3.1 Functions (Scope-Local)
### F-TMP-003-FN-01: prefillHost
- อ่าน Employee (F-EMP-001) + OrgUnit/line_manager (F-ORG-001) ของ host_employee_id → host.full_name, host.position, host.division, host.line_manager (snapshot ตอนบันทึก) · ค่าเริ่ม host = ผู้ใช้ปัจจุบัน (ยกเว้น role-mgr-hr เลือกเอง)
### F-TMP-003-FN-02: validate
- ใช้ทั้ง save draft (ตรวจเฉพาะ VR-01 รูปแบบ ไม่บังคับครบ) และ submit (VR-01..VR-07 ครบ) · ทำซ้ำฝั่ง server เสมอ · คำเตือน VR-08 (sign_date < request_date · request_date < วันนี้) ส่งกลับเป็น warnings ไม่บล็อก
### F-TMP-003-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type VAR (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('VAR', company_ctx)` → `header_snapshot` (Organization: Company.name_th · โลโก้) · ห้าม format/+1 เอง · owner_id = ผู้บันทึก
### F-TMP-003-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-003` → steps (ค่าเริ่ม 1 ขั้น role-line-manager · DEC-03) · role-line-manager resolve = line_manager ของ host · host ไม่มีผู้บังคับบัญชา → 409 HOST_NO_MANAGER
- assignees ครบทุกขั้น ≠ host ≠ owner (BR-DOA-04) · snapshot `approval_chain` (BR-DOA-02 freeze) · status draft→pending · ขั้น 1 pending · submitted_at · doa_ref · DOA engine ยิง doa_pending
- 0 ขั้น (ถ้า DOA กลางตั้งเป็น 0): status → approved ทันที
### F-TMP-003-FN-05: decideStep (DOA callback)
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้น→approved (note = ความเห็นผู้บังคับบัญชา · ไม่บังคับ) · ขั้นถัดไป pending หรือครบทุกขั้น → status=approved · approved_by/approved_at · `ENG-DOC-STORE.store(pdf,'VAR',id,'approved_final')` เฉพาะเมื่อ flag snapshot.approved_final เปิดที่ F-DOCCFG
- reject (BR-DOA-03 · DEC-08): note บังคับ (DEC-14) → status=draft เลขเดิม · เก็บ last_reject {by, at, note} · chain เดิมลง audit แล้วล้าง (resolve ใหม่ตอนส่ง) · DOA engine ยิง doa_result
### F-TMP-003-FN-06: cancelRequest
- owner/host หรือ role-mgr-hr · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-08 `var_cancelled` (เมื่อเดิม pending)
### F-TMP-003-FN-07: docPrintData + renderPdf
- data contract ตรงคีย์ `print/form.tpl.html` (print/VAR_data-contract.md): company (header_snapshot) · doc · visit (request_date พ.ศ. · purpose_line1/2 ตัดที่ช่องว่าง ~95 ตัวอักษร) · visitor · host · approval (comment + approve_box/reject_box จากผลสุดท้าย: approved → ☑ อนุมัติ · draft ที่มี last_reject → ☑ ไม่อนุมัติ) · sign_rows[] = พนักงานผู้รับการติดต่อ + 1 ช่องต่อขั้นใน approval_chain (จำนวนตาม DOA ไม่ fix · แถวละ ≤ print_config.sign_layout.max_per_row · คำตัดสินตาม decision_words.by_role) · layout.dense เมื่อขั้น > 4 → render logic-less (parity กับ tpl_render.js)
### F-TMP-003-FN-08: emitEvents
- `ENG-NOTIFY.emit`: **var_cancelled** (pending→cancelled · ผู้รับ: ผู้อนุมัติขั้นปัจจุบัน + ผู้สร้าง · ข้อความมีเลขที่ + เหตุผล ไม่ใส่โทรศัพท์) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ
### F-TMP-003-FN-09: listVisible
- canSee = role-mgr-hr ∨ owner_id=ฉัน ∨ host_employee_id=ฉัน ∨ (status≠draft ∧ อยู่ใน approval_chain) · ใบไม่มีสิทธิ์ → 404 · CSV ใช้เงื่อนไขเดียวกัน ไม่ส่งออก visitor_phone

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve/decide (F-DLG-001) · Document Center — ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| FN | API |
|---|---|
| FN-01 | API-03 |
| FN-02 | API-04, 05, 07, 12 |
| FN-03 | API-04 |
| FN-04 | API-06, 07 |
| FN-05 | API-08 |
| FN-06 | API-09 |
| FN-07 | API-10 |
| FN-08 | (จาก FN-06) |
| FN-09 | API-01, 02, 11 |
ทุก FN มี API ผูก ✓
