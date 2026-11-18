# 03_LOGIC — F-TMP-009
> ไม่มีค่าคงที่บนกระดาษ (FORM_SPEC.constants = 0) · ไม่มีสูตร · ทุกค่าตั้งค่าอ่านจาก DOA / F-DOCCFG / print_config

## §3.1 Functions (Scope-Local)
### F-TMP-009-FN-01: validateRequest
- Input `{contract_type, purpose, change_reason, counterparty_name, contract_start, contract_end, owner_unit_id}` → errors VR-01..06 (05 §5.4) · contract_type ∈ 8 ค่า · purpose ∈ 5 ค่า · purpose=amend → change_reason บังคับ / อื่น ๆ ล้างเป็นว่าง
### F-TMP-009-FN-02: snapshotParties
- snapshot ผู้รับผิดชอบ (ชื่อ/ตำแหน่ง/หน่วยงาน · F-EMP-001) + owner_unit_snapshot (F-ORG-001) ณ วันที่บันทึก
### F-TMP-009-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type CTR (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('CTR', company_ctx)` → `header_snapshot` (Organization: ชื่อบริษัท โลโก้) · ห้าม format/+1 เอง
### F-TMP-009-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-009` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง · role อื่น = ผู้ถือ role จาก DOA กลาง · ผู้ resolve ได้ = ผู้ขอ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้ขอ → snapshot `approval_chain` (freeze BR-DOA-02) · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-009-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved (คำตัดสินตาม role: role-compliance = รับทราบ) → ขั้นถัดไป pending หรือ status=approved (รอลงทะเบียน) เมื่อครบ → FN-09 render + `ENG-DOC-STORE.store(pdf,'CTR',id,'approved_final')`
### F-TMP-009-FN-06: returnToDraft
- reject (เหตุผลบังคับ) → audit "{คำปฏิเสธของขั้น} — ส่งกลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08)
### F-TMP-009-FN-07: cancelRequest
- owner หรือ ผู้ดูแลสัญญา · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-10 ctr_cancelled (ถ้าเดิม pending)
### F-TMP-009-FN-08: registerAndReceive
- register: เฉพาะผู้ดูแลสัญญา · status=approved → `ENG-DOC-NUM.next('CTR-REG', company_ctx)` (ลำดับทะเบียน — รูปแบบรอ OQ-06) → register_no · registered_by/at · status=registered → FN-10 ctr_registered
- receive: status=registered · original_received_date ≤ วันนี้ → status=completed → FN-10 ctr_original_received
### F-TMP-009-FN-09: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company · doc · req_date · contract_type.*_box · purpose.*_box · change_reason · counterparty_name · contract_period (เริ่ม - สิ้นสุด วันที่เต็ม พ.ศ.) · owner_unit · admin.register_no · admin.received_date · sign_rows[] = แบ่งช่องลงชื่อ (ผู้รับผิดชอบ + 1 ช่องต่อขั้นใน approval_chain snapshot — **จำนวนตามที่ตั้งใน DOA ไม่ fix**) แถวละ ≤ print_config.sign_layout.max_per_row (4) · คำตัดสินต่อช่องจาก print_config.decision_words.by_role[role_id] หรือ default · layout.dense เมื่อขั้น DOA > 4) → render logic-less (parity กับ tpl_render.js)
### F-TMP-009-FN-10: emitEvents
- `ENG-NOTIFY.emit`: **ctr_registered** (approved→registered → ผู้ขอ) · **ctr_original_received** (registered→completed → ผู้ขอ) · **ctr_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ
### F-TMP-009-FN-11: listVisible
- canSee = ผู้ดูแลสัญญา ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · to_register = approved (ผู้ดูแลเท่านั้น) · ใบไม่มีสิทธิ์ → 404 · CSV ใช้ตัวกรองเดียวกัน

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| API-01/02/12 | FN-11 |
| API-03 | FN-01 · FN-02 · FN-03 |
| API-04 | FN-01 · FN-02 |
| API-05 | FN-04 |
| API-06 | FN-05 · FN-09 |
| API-07 | FN-06 |
| API-08 | FN-07 · FN-10 |
| API-09/10 | FN-08 · FN-10 |
| API-11 | FN-09 |
