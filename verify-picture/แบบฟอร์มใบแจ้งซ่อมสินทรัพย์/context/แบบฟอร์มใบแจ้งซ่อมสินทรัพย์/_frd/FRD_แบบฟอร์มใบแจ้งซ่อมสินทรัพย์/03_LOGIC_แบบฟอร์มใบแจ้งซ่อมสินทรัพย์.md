# 03_LOGIC — F-TMP-001
> ไม่มีค่าคงที่บนกระดาษ (FORM_SPEC.constants ว่าง) · ไม่มีสูตร · จำนวนช่องลงชื่อ/ขั้นอนุมัติอ่านจาก DOA + print_config เท่านั้น

## §3.1 Functions (Scope-Local)
### F-TMP-001-FN-01: validateRequest
- Input `{items[]}` → errors VR-01/02 (05 §5.4) · ≥1 แถว · description/symptom/location ไม่ว่าง (trim) · qty จำนวนเต็ม > 0 · asset_code/remark ว่างได้ · ทำซ้ำฝั่ง server เสมอ
### F-TMP-001-FN-02: validateHistory
- ใช้ใน API-07 เมื่อผู้ตัดสินเป็นขั้นแรกของ approval_chain (step = 1) · แต่ละแถว: repair_count ว่าง หรือ จำนวนเต็ม ≥0 (VR-05) · last_repair_date ≤ วันนี้ · เก็บเฉพาะแถวที่มี description และ (last_repair_date หรือ repair_count) → แทนที่ history เดิมทั้งชุด (DEC-04)
### F-TMP-001-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-11): ตรวจ F-DOCCFG status ของ doc_type RPR (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('RPR', company_ctx)` → snapshot ผู้แจ้ง/ตำแหน่ง/ฝ่าย + `header_snapshot` (Organization: ชื่อบริษัท โลโก้) · ห้าม format/+1 เอง
### F-TMP-001-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-001` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง · role อื่น = ผู้ถือ role ใน DOA กลาง · ผู้ resolve ได้ = ผู้แจ้ง → ว่าง (เลือกเอง) · validate assignees ครบทุกขั้น + ≠ ผู้แจ้ง → snapshot `approval_chain` (freeze BR-DOA-02 · เก็บ words ต่อขั้นจาก decision_words.by_role) · status draft→pending ขั้น 1 · submitted_by/at · ล้าง returned_*
### F-TMP-001-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน (อื่น → 403 NOT_CURRENT_APPROVER) · approve: ถ้าขั้นแรก → FN-02 บันทึก history · ขั้นนั้น approved + note → ขั้นถัดไป pending หรือ status=approved (ครบ) → FN-08 render + `ENG-DOC-STORE.store(pdf,'RPR',id,'approved_final')` → FN-09 rpr_ready_for_repair · audit "{คำอนุมัติของ role} (ขั้น n)"
### F-TMP-001-FN-06: returnToDraft
- reject (เหตุผลบังคับ · DEC-14) → ขั้นนั้น rejected + note · ขั้นที่เหลือ skipped · audit "{คำปฏิเสธของ role} — ตีกลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-09) · history คงไว้ (ผู้ตรวจสอบแก้ได้รอบถัดไป)
### F-TMP-001-FN-07: cancelRequest
- owner หรือ admin role · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-09 rpr_cancelled (ถ้าเดิม pending)
### F-TMP-001-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (FM-ASM-03_data-contract.md): company (header_snapshot) · doc{title, no, is_draft, form_code, revision_suffix} · employee{name, position, dept} · items[] (เติมแถวว่างถึง print_config.min_rows_by_group.items · `no` 1..N พิมพ์ทุกแถว) · history[] (เติมว่างถึง min_rows_by_group.history · `no` ว่างในแถวว่าง · วันที่ไทยย่อ) · requester_sign{name, day, month(ชื่อเดือนเต็ม), year(พ.ศ.)} จาก submitted_at (ร่าง = ว่าง · DEC-13) · sign_rows[] = ผู้แจ้งซ่อม + 1 ช่องต่อขั้นใน approval_chain snapshot (**จำนวนตาม DOA ไม่ fix**) แบ่งแถวละ ≤ print_config.sign_layout.max_per_row (4) เฉลี่ย · คำตัดสินจาก print_config.decision_words.by_role[role_id] หรือ default · วันที่ช่อง = "ส่งในระบบ/พิจารณาในระบบ วันที่ เวลา" หรือเส้นประ · layout.dense เมื่อ items > min หรือ history > min หรือขั้น DOA > 4 → render logic-less (parity กับ tpl_render.js — IDENTICAL 5/5)
### F-TMP-001-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **rpr_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · **rpr_ready_for_repair** (→approved → admin role ฝ่ายบริหารสินทรัพย์) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ · domain event `rpr.approved` ประกาศแต่ไม่ยิง (DEC-02)
### F-TMP-001-FN-10: listVisible
- canSee = admin ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · returned = draft ∧ returned_at not null · ใบไม่มีสิทธิ์ → 404 · CSV ใช้ตัวกรองเดียวกัน

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,10 | FN-10 |
| 03 | FN-01, FN-03 |
| 04 | FN-01 |
| 05,06 | FN-04 |
| 07 | FN-02 + FN-05 (+FN-08, FN-09) / FN-06 |
| 08 | FN-07 (+FN-09) |
| 09 | FN-08 |
ทุก FN มี API ผูก ✓
