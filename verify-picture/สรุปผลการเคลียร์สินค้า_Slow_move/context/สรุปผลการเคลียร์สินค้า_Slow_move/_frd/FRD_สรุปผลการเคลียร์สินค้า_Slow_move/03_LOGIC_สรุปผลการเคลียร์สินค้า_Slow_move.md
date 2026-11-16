# 03_LOGIC — F-TMP-003
> ไม่มีรายการแนวทางการเคลียร์/รายการสินค้า/จำนวนแถวตายตัวใน logic — อ่านจาก SlowMoveConfig และ Product Master เท่านั้น (DEC-04)

## §3.1 Functions (Scope-Local)
### F-TMP-003-FN-01: validateClearance
- Input `{clearance_month, items[]}` → errors VR-01..06 (05 §5.4): month ≤ เดือนปัจจุบัน · items ≥ 1 (แถวว่างทั้งแถวตัดทิ้ง) · ต่อแถว: product_code active · follow_up_date มีและ ≤ วันนี้ · clearance_method_code มี (need_note → note บังคับ) · cleared_date กับ cleared_qty คู่กัน · qty > 0 · cleared_date ≥ follow_up_date และ ≤ วันนี้ (DEC-13) · warnings: expiry_date ≤ follow_up_date (DEC-14) · product_code ซ้ำ
### F-TMP-003-FN-02: resolveMasters
- อ่าน Product Master (API-13) → snapshot `product_name_snapshot` + `uom_snapshot` ต่อแถว · อ่าน `SlowMoveConfig.clearance_methods` (API-12) → snapshot `clearance_method_label` · ใบเดิมไม่เปลี่ยนเมื่อ master/config เปลี่ยน (EC-05)
### F-TMP-003-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type SMC (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('SMC', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง/หน่วยงาน + `header_snapshot` (Organization: ชื่อบริษัท ที่อยู่ โลโก้) · ห้าม format/+1 เอง
### F-TMP-003-FN-04: saveItems
- แทนที่รายการทั้งชุด (seq ใหม่ตามลำดับ) · คำนวณสรุปต่อใบ items_count · cleared_count · expired_count · ไม่แตะสต็อก (DEC-01)
### F-TMP-003-FN-05: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-003` → steps (ไม่มีวงเงิน) · role-mgr-wh = ผู้จัดการคลังสินค้าของหน่วยงานผู้จัดทำ (relative · OQ-05) · ผู้ resolve ได้ = ผู้จัดทำเอง → ขึ้นไปผู้บังคับบัญชาถัดไป / ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) · status draft/returned→pending ขั้น 1
### F-TMP-003-FN-06: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved → ขั้นถัดไป pending หรือ status=approved (ครบ) → FN-09 render + `ENG-DOC-STORE.store(pdf,'SMC',id,'approved_final')` · คำตัดสินแสดงตาม `print_config.decision_words.by_role`
### F-TMP-003-FN-07: returnToDraft
- reject (เหตุผลบังคับ) → audit "ไม่อนุมัติ" + returned_by/at/reason · status=returned (แก้ได้เหมือนร่าง · เลขเดิม) · ขั้นที่เหลือ = skipped · approval_chain เดิมเก็บใน audit แล้ว resolve ใหม่ตอนส่ง (DEC-08)
### F-TMP-003-FN-08: cancelClearance
- owner หรือ admin (role-mgr-wh ของหน่วยงานเจ้าของเอกสาร) · status ∈ {draft, pending, returned} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-10 `smc_cancelled` (ถ้าเดิม pending)
### F-TMP-003-FN-09: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (SMC_data-contract.md): company (header_snapshot) · doc{title,no,is_draft,form_code,revision} · clearance_month (เดือนไทย พ.ศ.) · items_p1 (แถว 1–rows_page1 เติมแถวว่างให้ครบตามกระดาษ) · items_p2 (แถวถัดไป เติมแถวว่างขั้นต่ำ rows_page2_min) — ค่าทั้งหมดจาก print_config ไม่ fix ใน code · วันที่ dd/mm/yy พ.ศ. · จำนวน #,##0 · แนวทาง = label (+ note) · sign_rows (`sign_rows.py`: ผู้จัดทำ + 1 ช่อง/ขั้น approval_chain · แถวละ ≤ print_config.sign_layout.max_per_row) · layout.dense → render `form.tpl.html` ด้วย render_doc (= tpl_render.js) → A4 2 หน้า (R10)
### F-TMP-003-FN-10: emitEvents
- `ENG-NOTIFY.emit`: **smc_cancelled** (pending→cancelled → ผู้อนุมัติขั้นปัจจุบัน) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ · `smc.approved` ประกาศไว้ไม่ยิง (DEC-02)
### F-TMP-003-FN-11: listVisible
- canSee = admin ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · ใบไม่มีสิทธิ์ → 404 · ค้นหา q ครอบเลขที่/ผู้จัดทำ/รหัส-ชื่อสินค้า · สรุปต่อใบ: items_count · cleared_count · expired_count

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,10 | FN-11 |
| 03 | FN-01, FN-02, FN-03 |
| 04 | FN-01, FN-02, FN-04 |
| 05,06 | FN-05 |
| 07 | FN-06 (+FN-09) / FN-07 |
| 08 | FN-08 (+FN-10) |
| 09 | FN-09 |
| 12,13 | FN-02 |
ทุก FN มี API ผูก ✓
