# 03_LOGIC — F-TMP-005
> ไม่มีรายการหน่วยงาน/หน่วยนับ/เกณฑ์วัน/จำนวนแถวตายตัวใน logic — อ่านจาก ผังองค์กร · UOM Master · print_config · PurchaseConfig เท่านั้น (DEC-04)

## §3.1 Functions (Scope-Local)
### F-TMP-005-FN-01: validateReview
- Input `{report_date, org_unit_id, items[]}` → errors VR-01..10 (05 §5.4): report_date มีและ ≤ วันนี้ · org_unit มี · items ≥ 1 (แถวว่างทั้งแถวตัดทิ้ง) · ต่อแถว: pr_no หรือ po_no ≥1 (DEC-14) · มี po_no → order_date + vendor_name บังคับ · order_date ≤ วันนี้ และ ≤ report_date · receive_date ≥ order_date (DEC-13 · อนาคตได้) · description · order_qty > 0 · uom active · request_dept · outstanding_reason · current_status · corrective_action มีข้อความ · warnings: pr_no/po_no ซ้ำในรายงาน · จำนวนแถว > rows_page1 + rows_page2_max
### F-TMP-005-FN-02: resolveMasters
- อ่าน ผังองค์กร (API-12) → snapshot `org_unit_name` (header) + `request_org_unit_name` ต่อแถว · อ่าน uom_master (API-13) → snapshot `uom_name` · ผู้จัดทำ/ตำแหน่งจาก F-EMP-001 ณ บันทึก · รายงานเดิมไม่เปลี่ยนเมื่อ master เปลี่ยน (EC-05) · เลข PR/PO/ผู้ขาย = ข้อความ soft reference (F072/F078/Supplier ยังไม่มี · OQ-04)
### F-TMP-005-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type PPO (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('PPO', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง/หน่วยงาน + `header_snapshot` (Organization: ชื่อบริษัท · โลโก้) · ห้าม format/+1 เอง
### F-TMP-005-FN-04: saveItems
- แทนที่รายการทั้งชุด (seq ใหม่ตามลำดับ) · คำนวณสรุปต่อรายงาน items_count · no_po_count · ไม่แตะ PR/PO (DEC-01)
### F-TMP-005-FN-05: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-005` → steps (ไม่มีวงเงิน) · role-mgr-pur = ผู้จัดการจัดซื้อของหน่วยงานผู้จัดทำ (relative · OQ-05) · ผู้ resolve ได้ = ผู้จัดทำเอง → ขึ้นไปผู้บังคับบัญชาถัดไป / ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) · status draft/returned→pending ขั้น 1
### F-TMP-005-FN-06: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved → ขั้นถัดไป pending หรือ status=approved (ครบ) → FN-09 render + `ENG-DOC-STORE.store(pdf,'PPO',id,'approved_final')` · คำตัดสินแสดงตาม `print_config.decision_words.by_role`
### F-TMP-005-FN-07: returnToDraft
- reject (เหตุผลบังคับ) → audit "ไม่อนุมัติ" + returned_by/at/reason · status=returned (แก้ได้เหมือนร่าง · เลขเดิม) · ขั้นที่เหลือ = skipped · approval_chain เดิมเก็บใน audit แล้ว resolve ใหม่ตอนส่ง (DEC-08)
### F-TMP-005-FN-08: cancelReview
- owner หรือ admin (role-mgr-pur ของหน่วยงานเจ้าของเอกสาร) · status ∈ {draft, pending, returned} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-10 `ppo_cancelled` (ถ้าเดิม pending)
### F-TMP-005-FN-09: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (PPO_data-contract.md): company (header_snapshot) · doc{title_l1,title_l2,no,is_draft,form_code,revision} · report_date (วันที่ไทยเต็ม พ.ศ.) · org_unit · preparer{name,position} · items_p1 (แถว 1–rows_page1 · เติมแถวว่างขั้นต่ำ rows_page1_min = 8 ตามกระดาษ) · items_p2 (แถวถัดไปสูงสุด rows_page2_max · เติมแถวว่างขั้นต่ำ rows_page2_min) — ค่าทั้งหมดจาก print_config ไม่ fix ใน code · วันที่ dd/mm/yy พ.ศ. · จำนวน #,##0.## · sign_rows (`sign_rows.py`: ผู้จัดทำ + 1 ช่อง/ขั้น approval_chain · แถวละ ≤ print_config.sign_layout.max_per_row) · layout.dense → render `form.tpl.html` ด้วย render_doc (= tpl_render.js) → A4 2 หน้า (R10)
### F-TMP-005-FN-10: emitEvents
- `ENG-NOTIFY.emit`: **ppo_cancelled** (pending→cancelled → ผู้อนุมัติขั้นปัจจุบัน) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ · `ppo.approved` ประกาศไว้ไม่ยิง (DEC-02)
### F-TMP-005-FN-11: listVisible
- canSee = admin ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · รายงานไม่มีสิทธิ์ → 404 · ค้นหา q ครอบเลขที่/ผู้จัดทำ/หน่วยงาน/เลข PR-PO/ผู้ขาย/รายละเอียด · สรุปต่อรายงาน: items_count · no_po_count · CSV ระดับรายการ

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
