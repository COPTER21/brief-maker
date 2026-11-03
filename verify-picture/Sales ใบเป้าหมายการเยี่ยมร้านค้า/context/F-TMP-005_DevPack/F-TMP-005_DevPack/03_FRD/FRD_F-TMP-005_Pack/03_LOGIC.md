# 03_LOGIC — F-TMP-005
> ไม่มีค่าคงที่ตัวเลขบนกระดาษ (FORM_SPEC.constants ว่าง) · 7 ช่องร้าน / 31 แถว = รูปแบบแบบพิมพ์ (print_config) · ไม่ hardcode สายอนุมัติ (`TODO: DOA engine`)

## §3.1 Functions (Scope-Local)
### F-TMP-005-FN-01: prefillTerritory
- อ่าน SalesTerritory (code · name · owner_employee_id) → Employee (ชื่อ · ตำแหน่ง) → snapshot territory_owner_name, territory_owner_position · ค่าเริ่ม to_recipient = ผู้อนุมัติขั้นแรก (resolve role-line-manager ของ owner) · รายชื่อ Customer ในเขต · คืนใบใช้งานเดิมของเขต+รอบ (ถ้ามี) เพื่อเตือน · เขตที่เลือกได้ = owner_employee_id = ผู้ใช้ (role-mgr-sales เลือกได้ทุกเขต)
### F-TMP-005-FN-02: validateAndCalc
- calc (DEC-14 · DEC-17): days[].customer_count = count(stores) · total_customer_count = Σ customer_count · work_days = count(days ที่มี visit_date)
- validate (draft ตรวจเฉพาะ territory + sales_cycle · submit ตรวจครบ): VR-01..VR-09 (05 §5.4) · เตือน (ไม่บล็อก) stores > 7 (W-01 · DEC-15) · ทำซ้ำฝั่ง server เสมอ · เรียง days ตาม visit_date ก่อนบันทึก
### F-TMP-005-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type SVT (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('SVT', company_ctx)` → `header_snapshot` (Organization: ชื่อบริษัท โลโก้) · ห้าม format/+1 เอง · owner_id = ผู้รับผิดชอบเขต
### F-TMP-005-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-005` → steps (ค่าเริ่ม 2 ขั้น role-line-manager → role-mgr-sales · DEC-03) · validate FN-02 ครบ · assignees ครบทุกขั้น ≠ owner (BR-DOA-04)
- snapshot `approval_chain` (append-only · BR-DOA-02 freeze) · approver_role = role ขั้นปัจจุบัน · status draft→**pending** · submitted_at · DOA engine ยิง doa_pending
### F-TMP-005-FN-05: approveStep
- เฉพาะ assignee ขั้นปัจจุบัน · ขั้น→approved · ถัดไป pending หรือ (ขั้นสุดท้าย) status=**approved** · approved_by/approved_at · เรียก FN-09 · `ENG-DOC-STORE.store(pdf,'SVT',id,'approved_final')` (flag snapshot.approved_final ที่ F-DOCCFG)
### F-TMP-005-FN-06: rejectToDraft
- ไม่อนุมัติ (เหตุผลบังคับ) ขั้นใดก็ได้ → status=draft เลขเดิม (DEC-08 · BR-DOA-03 มาตรฐาน) · chain เดิมลง audit แล้วล้าง (resolve ใหม่ตอนส่ง)
### F-TMP-005-FN-07: cancelTarget
- owner หรือ role-mgr-sales · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → emit `svt_cancelled` (เมื่อเดิม pending)
### F-TMP-005-FN-08: docPrintData + renderPdf
- data contract ตรงคีย์ `print/form.tpl.html` (print/SVT_data-contract.md): company (header_snapshot) · doc · to_recipient · cc_recipients · territory_owner · territory_owner_position · territory · sales_cycle · visit_rows[] (31 แถว เติมว่าง · s1..s7 · ร้าน >7 ต่อชื่อในช่อง s7) · totals{work_days, customers} · sign_rows[] = ผู้นำเสนอ + 1 ช่องต่อขั้นใน approval_chain (คำตัดสินตาม decision_words.by_role) · แถวละ ≤4 · layout.dense → render logic-less (parity กับ tpl_render.js) · กระดาษ A4 แนวนอน (print_config.paper)
### F-TMP-005-FN-09: supersedeAndEmit
- เมื่อ FN-05 ขั้นสุดท้าย: ใบอื่นของ territory_id + sales_cycle เดียวกันที่ status = approved → **superseded** (superseded_by = ใบนี้) + emit `svt_superseded` · emit `svt_plan_published` → to_recipient + cc_recipients
- `ENG-NOTIFY.emit` ทุก event: svt_cancelled · svt_plan_published · svt_superseded · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ
### F-TMP-005-FN-10: listVisible
- canSee = role-mgr-sales ∨ owner_id=ฉัน ∨ (status≠draft ∧ อยู่ใน approval_chain) ∨ ((to_recipient=ฉัน ∨ ฉัน ∈ cc_recipients) ∧ status ∈ {approved, superseded}) · ใบไม่มีสิทธิ์ → 404 · CSV ใช้เงื่อนไขเดียวกัน

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
| FN-09 | (จาก FN-05, FN-07) |
| FN-10 | API-01, 02, 11 |
ทุก FN มี API ผูก ✓
