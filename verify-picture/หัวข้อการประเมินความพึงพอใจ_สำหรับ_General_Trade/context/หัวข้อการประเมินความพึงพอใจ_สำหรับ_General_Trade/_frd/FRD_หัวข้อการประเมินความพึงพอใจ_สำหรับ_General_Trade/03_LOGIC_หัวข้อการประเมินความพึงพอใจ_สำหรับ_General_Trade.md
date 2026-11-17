# 03_LOGIC — F-TMP-002
> ไม่มีตัวเลขค่าคงที่ใน logic — หัวข้อ · น้ำหนัก · ช่วงแปลผล · เกณฑ์สั่งซื้อ อ่านจาก SalesConfig (config) เท่านั้น (DEC-04)

## Functions (Scope-Local)
### F-TMP-002-FN-01: validateSummary
- Input `{period_month, lines[], customers[]}` → errors VR-01..04 (05 §5.4) · lines ต้องครบทุก topic ที่ config กำหนด (topic_id ตรง config version ปัจจุบัน หรือ snapshot เดิมของเอกสาร)
### F-TMP-002-FN-02: computeCsat
- ต่อแถว total = Σ c* · ต่อด้าน sums[k] = Σ แถว · tot = Σ total · weighted = Σ (count × weight จาก csat_scale config) · pct = weighted ÷ (max_weight × tot) × 100 ปัด 2 ตำแหน่ง ROUND_HALF_UP · tot = 0 → null
- overall_pct = Σ weighted ทุกด้าน ÷ (max_weight × Σ tot) × 100 · overall_level = ช่วงแรกใน csat_bands (config) ที่ overall_pct ≥ min · คำนวณฝั่ง server เสมอ (ไม่เชื่อค่าจาก FE)
### F-TMP-002-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-13): ตรวจ F-DOCCFG status ของ doc_type CSM (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('CSM', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง/หน่วยงาน + `header_snapshot` (Organization: ชื่อบริษัท โลโก้) + topic_text snapshot ต่อ line · ห้าม format/+1 เอง
### F-TMP-002-FN-04: eligibleCustomers
- ลูกค้า GT ในหน่วยงาน/เขตของผู้จัดทำ (Customer · soft-ref) + `order_count = COUNT(SaleOrder where customer_id and order_date in period_month and status ≠ cancelled)` · คืนเฉพาะ order_count ≥ csat_min_orders_per_month (config) · ใช้ทั้งปุ่ม "ดึงลูกค้า" และป้ายเตือน (ต่ำกว่าเกณฑ์ = เตือนไม่บล็อก DEC-20)
### F-TMP-002-FN-05: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-002` → steps (ไม่มีวงเงิน) · ผู้ resolve ได้ = ผู้จัดทำ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) + order_count snapshot ต่อ customer · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-002-FN-06: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved → ขั้นถัดไป pending หรือ status=approved (ครบ) → snapshot overall_pct/overall_level → FN-08 render + `ENG-DOC-STORE.store(pdf,'CSM',id,'approved_final')` → FN-09 (csm_low_csat ถ้าเข้าเงื่อนไข)
### F-TMP-002-FN-07: returnToDraft / cancelSummary
- reject (เหตุผลบังคับ) → audit "ไม่อนุมัติ — กลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-11 · BR-DOA-03)
- cancel: owner หรือ Sales admin · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → FN-09 csm_cancelled (ถ้าเดิม pending)
### F-TMP-002-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (print-spec §2): company (header_snapshot) · doc · period_month (เดือนไทย พ.ศ.) · sections[] (heading · col_title · levels จาก csat_scale config · items[topic snapshot · counts · total · pct_cell เฉพาะแถวแรก {rowspan = จำนวนหัวข้อ+1, pct}] · sums · sum_total) · overall_pct · overall_level · policy (min_orders · bands จาก config) · customers (เติมแถวว่างถึง print_config.min_rows) · sign_rows[] (ผู้จัดทำ + 1 ช่องต่อขั้นใน approval_chain snapshot — **จำนวนตามที่ตั้งใน DOA ไม่ fix** · แถวละ ≤ print_config.sign_layout.max_per_row เฉลี่ย · คำตัดสินจาก print_config.decision_words) · layout.dense / dense_signs → render logic-less (parity กับ tpl_render.js) · 2 หน้า (R10)
### F-TMP-002-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **csm_cancelled** (pending→cancelled → ผู้อนุมัติขั้นปัจจุบัน) · **csm_low_csat** (→approved และ overall_pct < csat_bands[mid].min จาก config → owner + role-mgr-sales) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ · `csm.approved` ประกาศไม่ยิง (DEC-02)
### F-TMP-002-FN-10: listVisible
- canSee = sales_admin ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · ใบไม่มีสิทธิ์ → 404 · CSV ใช้ชุดเดียวกัน

## Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — ไม่มี engine ใหม่

## API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,10 | FN-10 |
| 03 | FN-01, FN-02, FN-03 |
| 04 | FN-01, FN-02 |
| 05 | FN-04 |
| 06 | FN-05 |
| 07 | FN-06 (+FN-08, FN-09) / FN-07 |
| 08 | FN-07 (+FN-09) |
| 09 | FN-08 |
ทุก FN มี API ผูก ✓
