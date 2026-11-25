# 03_LOGIC — F-TMP-003
> ไม่มีค่าคงที่ธุรกิจใน logic — สายอนุมัติจาก DOA กลาง · เลข/แบบพิมพ์จาก F-DOCCFG

## §3.1 Functions (Scope-Local)
### F-TMP-003-FN-01: validateRequest
- Input `{request_type, add, edit, cancel}` → errors VR-01..06 (05 §5.4): request_type ว่าง · add: ไม่มีชื่อบัญชีที่ไม่ว่าง / ชื่อซ้ำในใบ / add.purpose ว่าง · edit: account_code / change_to / purpose ว่าง · cancel: account_code / account_name / purpose ว่าง
### F-TMP-003-FN-02: normalizeByType
- เก็บเฉพาะส่วนของ request_type · ส่วนอื่นเป็นค่าว่าง (DEC-13) · add lines: trim · ตัดบรรทัดว่าง · seq เรียงตามลำดับ
### F-TMP-003-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type ACR (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('ACR', company_ctx)` → snapshot ผู้ขอ/ตำแหน่ง/ฝ่าย + `header_snapshot` (Organization: ชื่อบริษัท โลโก้) · ห้าม format/+1 เอง
### F-TMP-003-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-003` → steps (ไม่มีวงเงิน · ค่าเริ่ม role-line-manager › role-mgr-acc) · ผู้ resolve ได้ = ผู้ขอ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้ขอ → snapshot `approval_chain` (freeze BR-DOA-02) · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-003-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve → ขั้นนั้น approved → ขั้นถัดไป pending หรือ status=approved (ครบ) → FN-08 render + `ENG-DOC-STORE.store(pdf,'ACR',id,'approved_final')` + FN-09 acr_ready_to_record · ไม่แตะ COA (DEC-01)
### F-TMP-003-FN-06: returnToDraft
- reject (เหตุผลบังคับ DEC-14) → audit "{คำไม่อนุมัติของ role} · กลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08)
### F-TMP-003-FN-07: cancelRequest
- owner หรือ admin ฝ่ายบัญชี · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-09 acr_cancelled (ถ้าเดิม pending)
### F-TMP-003-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company · doc · req_date · req_type.{add_box,edit_box,cancel_box} · add_lines (เติมว่างถึง print_config.min_rows = 4 · ไม่ใช่ add = ว่างทั้งหมด) · add.purpose · edit.* · cancel.* · approval.{approve_box, reject_box, reject_reason} · sign_rows[] = ผู้ขอ + 1 ช่องต่อขั้นใน approval_chain snapshot — **จำนวนตามที่ตั้งใน DOA ไม่ fix** แบ่งแถวละ ≤ print_config.sign_layout.max_per_row (4) เฉลี่ย · คำตัดสินจาก print_config.decision_words.by_role[role_id] (role-line-manager = ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ) หรือ default · recorder.{status,name,date} จาก recorded_* (ว่าง = เส้นประ) · layout.dense เมื่อชื่อบัญชี > 4 หรือขั้น DOA > 4) → render logic-less (parity กับ tpl_render.js)
### F-TMP-003-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **acr_cancelled** (pending→cancelled → ผู้อนุมัติขั้นปัจจุบัน) · **acr_ready_to_record** (→ approved → admin ฝ่ายบัญชี) · **acr_recorded** (approved→recorded → ผู้ขอ) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ
### F-TMP-003-FN-10: listVisible
- canSee = admin บัญชี ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · to_record = approved (admin) · ใบไม่มีสิทธิ์ → 404
### F-TMP-003-FN-11: recordToSystem
- status=approved · ผู้เรียก = admin ฝ่ายบัญชี · recorded_at ≤ วันนี้ ∧ ≥ approved_at → recorded_by/recorded_at · status=recorded · FN-08 re-render (บรรทัดผู้บันทึกเข้าระบบ) · FN-09 acr_recorded · ไม่แก้ COA (DEC-01)

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,11 | FN-10 |
| 03 | FN-01, FN-02, FN-03 |
| 04 | FN-01, FN-02 |
| 05,06 | FN-04 |
| 07 | FN-05 (+FN-08, FN-09) / FN-06 |
| 08 | FN-07 (+FN-09) |
| 09 | FN-11 (+FN-08, FN-09) |
| 10 | FN-08 |
ทุก FN มี API ผูก ✓ (FN-09 ถูกเรียกจาก FN-05/07/11)
