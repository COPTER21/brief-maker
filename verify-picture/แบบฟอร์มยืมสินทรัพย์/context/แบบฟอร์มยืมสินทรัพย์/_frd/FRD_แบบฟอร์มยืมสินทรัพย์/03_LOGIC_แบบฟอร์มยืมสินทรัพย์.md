# 03_LOGIC — F-TMP-002
> ไม่มีค่าคงที่ธุรกิจใน logic — สายอนุมัติจาก DOA กลาง · เลข/แบบพิมพ์จาก F-DOCCFG

## §3.1 Functions (Scope-Local)
### F-TMP-002-FN-01: validateBorrow
- Input `{purpose, items[]}` → errors VR-01..04 (05 §5.4): purpose ว่าง · item ขาด asset_code/qty_requested(≥1)/borrow_date/return_date · return_date < borrow_date · asset_code ซ้ำในใบ
### F-TMP-002-FN-02: snapshotItems
- asset_name = Asset Master.name ของ asset_code (snapshot ตอนบันทึก · BR-01) · seq เรียงตามลำดับ · qty_lent = null ในร่าง (ล้างทุกครั้งที่แก้ร่าง)
### F-TMP-002-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type ALN (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('ALN', company_ctx)` → snapshot ผู้ยืม/ตำแหน่ง/ฝ่าย + `header_snapshot` (Organization: ชื่อบริษัท โลโก้) · ห้าม format/+1 เอง
### F-TMP-002-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-002` → steps (ไม่มีวงเงิน · ค่าเริ่ม role-mgr-acc) · ผู้ resolve ได้ = ผู้ยืม → ข้ามไปคนอื่น/ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้ยืม → snapshot `approval_chain` (freeze BR-DOA-02) · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-002-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: validate qty_lent[i] ∈ [1, qty_requested] (BR-02 → 422 QTY_LENT_INVALID) → บันทึก qty_lent → ขั้นนั้น approved → ขั้นถัดไป pending หรือ status=approved (ครบ) → FN-08 render + `ENG-DOC-STORE.store(pdf,'ALN',id,'approved_final')` · ไม่แตะ Asset Master (DEC-01)
### F-TMP-002-FN-06: returnToDraft
- reject (เหตุผลบังคับ) → audit "ไม่ให้ยืม · กลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · qty_lent ล้าง · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08)
### F-TMP-002-FN-07: cancelBorrow
- owner หรือ admin ฝ่ายบริหารสินทรัพย์ · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-09 aln_cancelled (ถ้าเดิม pending)
### F-TMP-002-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company · doc · employee · purpose · lines (เติมว่างถึง print_config.min_rows = 11) · sign_rows[] = ผู้ยืม + 1 ช่องต่อขั้นใน approval_chain snapshot — **จำนวนตามที่ตั้งใน DOA ไม่ fix** แบ่งแถวละ ≤ print_config.sign_layout.max_per_row (4) เฉลี่ย · คำตัดสินจาก print_config.decision_words.by_role[role_id] (role-mgr-acc = ให้ยืม/ไม่ให้ยืม) หรือ default · return_signs[2] = ผู้ส่งคืน/ผู้รับคืน จาก return_record (ว่าง = เส้นประวันที่) · layout.dense เมื่อรายการ > 11 หรือขั้น DOA > 4) → render logic-less (parity กับ tpl_render.js)
### F-TMP-002-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **aln_cancelled** (pending→cancelled → ผู้อนุมัติขั้นปัจจุบัน) · **aln_returned** (approved→returned → ผู้ยืม) · **aln_overdue** (งานรายวัน: status=approved ∧ วันนี้ > return_date ของรายการใด → ผู้ยืม + role-mgr-acc · ครั้งเดียวต่อวัน) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ
### F-TMP-002-FN-10: listVisible
- canSee = admin สินทรัพย์ ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · overdue = approved ∧ ∃ return_date < วันนี้ · ใบไม่มีสิทธิ์ → 404
### F-TMP-002-FN-11: recordReturn
- status=approved · ผู้เรียก = admin สินทรัพย์ ∨ assignee ที่ approved ในสาย · received_at ≤ วันนี้ ∧ ≥ min(borrow_date) → return_record {returned_by_emp = owner, received_by = ผู้เรียก, received_at} · status=returned · FN-08 re-render (ส่วนรับคืน) · FN-09 aln_returned

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — ไม่มี engine ใหม่ · งานรายวัน aln_overdue ใช้ scheduler กลาง

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,11 | FN-10 |
| 03 | FN-01, FN-02, FN-03 |
| 04 | FN-01, FN-02 |
| 05,06 | FN-04 |
| 07 | FN-05 (+FN-08) / FN-06 |
| 08 | FN-07 (+FN-09) |
| 09 | FN-11 (+FN-08, FN-09) |
| 10 | FN-08 |
ทุก FN มี API ผูก ✓ (FN-09 ถูกเรียกจาก FN-07/FN-11 + scheduler)
