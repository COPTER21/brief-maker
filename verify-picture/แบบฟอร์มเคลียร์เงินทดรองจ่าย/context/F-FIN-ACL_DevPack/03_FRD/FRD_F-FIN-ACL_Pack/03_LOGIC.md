# 03_LOGIC — F-FIN-ACL
> ไม่มีตัวเลขค่าคงที่ใน logic — อ่าน config เท่านั้น (DEC-04)

## §3.1 Functions (Scope-Local)
### F-FIN-ACL-FN-01: validateClearing
- Input `{advance_ref, advance_amount, lines[]}` → errors VR-01..03 (05 §5.4)
### F-FIN-ACL-FN-02: computeClearing
- total_expense = Σ amount (ปัด 2 ตำแหน่ง) · refund_amount = advance_amount − total_expense · result = refund>0 คืนบริษัท / =0 พอดี / <0 ใช้เกิน · ทำซ้ำฝั่ง server เสมอ (ไม่เชื่อค่าจาก FE)
### F-FIN-ACL-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type ACL (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('ACL', company_ctx)` → snapshot ผู้ขอ/ตำแหน่ง/ฝ่าย + `header_snapshot` (Organization: ชื่อบริษัท โลโก้) · ห้าม format/+1 เอง
### F-FIN-ACL-FN-04: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-FIN-ACL` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง · ผู้ resolve ได้ = ผู้ขอ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้ขอ → snapshot `approval_chain` (freeze BR-DOA-02) · status draft→pending ขั้น 1 · ล้าง returned_*
### F-FIN-ACL-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved → ขั้นถัดไป pending หรือ status=approved (ครบ) → FN-08 render + `ENG-DOC-STORE.store(pdf,'ACL',id,'approved_final')` → FN-09 · ด่าน: ขั้น role_id=role-finance-officer และ refund>0 และไม่มีไฟล์ประเภท `refund_slip` → 422 REFUND_SLIP_REQUIRED (BR-04)
### F-FIN-ACL-FN-06: returnToDraft
- reject (เหตุผลบังคับ) → audit "{คำปฏิเสธของขั้น} — ส่งกลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08)
### F-FIN-ACL-FN-07: cancelClearing
- owner หรือ role-finance-officer · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-09 acl_cancelled (ถ้าเดิม pending)
### F-FIN-ACL-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company · doc · doc_date · employee · advance_ref · lines(เติมว่างถึง print_config.min_rows) · total_expense · advance_amount · refund_amount · total_amount · total_amount_text(baht_text · ติดลบ "ลบ…") · policy.clear_due_day (ExpensePolicy) · refund_account (Company.bank_accounts[purpose=advance_refund]) · sign_rows[] = แบ่งช่องลงชื่อ (ผู้ขอ + 1 ช่องต่อขั้นใน approval_chain snapshot — **จำนวนตามที่ตั้งใน DOA ไม่ fix**) เป็นแถวละ ≤ print_config.sign_layout.max_per_row (4) เฉลี่ยเท่ากัน (7→4+3 · 6→3+3) · คำตัดสินต่อช่องจาก print_config.decision_words.by_role[role_id] หรือ default · layout.dense เมื่อรายการ > min_rows หรือขั้น DOA > 4) → render logic-less (parity กับ tpl_render.js)
### F-FIN-ACL-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **acl_cancelled** (pending→cancelled → ผู้อนุมัติขั้นปัจจุบัน) · **acl_overspent_approved** (→approved และ refund<0 → role-finance-officer) · **acl_refund_due** (→approved และ refund>0 → role-finance-officer) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ
### F-FIN-ACL-FN-10: listVisible
- canSee = finance-officer ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · ใบไม่มีสิทธิ์ → 404

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,10 | FN-10 |
| 03 | FN-01, FN-02, FN-03 |
| 04 | FN-01, FN-02 |
| 05,06 | FN-04 |
| 07 | FN-05 (+FN-08, FN-09) / FN-06 |
| 08 | FN-07 (+FN-09) |
| 09 | FN-08 |
ทุก FN มี API ผูก ✓
