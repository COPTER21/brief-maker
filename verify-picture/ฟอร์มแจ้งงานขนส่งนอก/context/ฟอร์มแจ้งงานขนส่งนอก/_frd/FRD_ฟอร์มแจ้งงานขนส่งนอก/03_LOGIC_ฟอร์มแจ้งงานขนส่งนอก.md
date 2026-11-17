# 03_LOGIC — F-TMP-003
> ไม่มีค่าคงที่บนกระดาษ (FORM_SPEC.constants = 0) · ระดับเตือนวันที่นัดส่งอ่านจาก config (Sales Configuration · ค่าเริ่ม = เตือน)

## §3.1 Functions (Scope-Local)
### F-TMP-003-FN-01: validateNotice
- Input `{carrier_id, round_date, lines[], ...}` → VR-01/02 (05 §5.4) · ตัดแถวว่างทั้งแถว · แถวที่เริ่มกรอกต้องครบ 5 ช่อง (VR-03 · ตอนส่ง) · qty จำนวนเต็ม > 0 (VR-04) · delivery_date < round_date → warning `DELIVERY_BEFORE_ROUND` (ไม่บล็อก · DEC-13)
### F-TMP-003-FN-02: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-09): ตรวจ F-DOCCFG status ของ doc_type OTN (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('OTN', company_ctx)` → snapshot `carrier_name_snapshot` (Vendor master) + `header_snapshot` (Organization: ชื่อบริษัท · โลโก้) · ห้าม format/+1 เอง
### F-TMP-003-FN-03: submitNotice
- เฉพาะเจ้าของ · status = draft · ≥ 1 แถวครบ และไม่มีแถวไม่ครบ ไม่งั้น 422 NO_LINES / LINES_INCOMPLETE (BR-02) → status = submitted · submitted_at · prepared_by = ผู้ส่ง · audit "ส่งแจ้งงานขนส่ง" · ไม่มีขั้นพิจารณา (DEC-03 · DOA resolve = 0 ขั้น → approval_chain = [] · approver_role/approved_by ว่าง · TODO: DOA engine) → FN-06
### F-TMP-003-FN-04: computeLineSummary
- line_count = จำนวนแถวที่ใช้ · qty_total = ผลรวม qty (แสดงผล/list/สรุปเท่านั้น — ไม่เก็บ · ไม่พิมพ์ · BR-11) · early_rows = แถวที่ delivery_date < round_date
### F-TMP-003-FN-05: cancelNotice
- เจ้าของ หรือ role-mgr-sales · status ∈ {draft, submitted} · เหตุผลบังคับ → cancelled · audit (append-only) → FN-06 otn_cancelled (เมื่อผู้ยกเลิก ≠ เจ้าของ)
### F-TMP-003-FN-06: emitEvents
- `ENG-NOTIFY.emit`: **otn_submitted** (draft→submitted → role-mgr-sales · vars: doc_no, carrier_name, round_date, line_count) · **otn_early_delivery_date** (draft→submitted และ early_rows > 0 → role-mgr-sales · vars: doc_no, count, round_date) · **otn_cancelled** (→cancelled โดยไม่ใช่เจ้าของ → เจ้าของ · vars: doc_no, actor, reason) · ไม่มี doa_* · ไม่ส่งต่อระบบอื่น (DEC-02)
### F-TMP-003-FN-07: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company · doc{title,no,is_draft,is_cancelled,form_code,revision} · carrier_name · round_date_text (วัน เดือนเต็ม พ.ศ.) · lines[].{origin,destination,po_no,qty "#,##0",delivery_date "dd/mm/yyyy พ.ศ."} เติมแถวว่างให้ครบ print_config.min_rows = 20 · approver_role/approved_by/approval_chain (TODO: DOA engine) · sign_rows = ผู้จัดทำ (ชื่อ + "ส่งในระบบ dd/mm/yyyy hh:mm" หรือเส้นประวันที่) + 1 ช่องต่อขั้น DOA snapshot (= 0 ขั้น) แถวละ ≤ 4 · layout.dense เมื่อแถว > 20 / ข้อความต้นทาง-ปลายทาง > 30 ตัวอักษร / ขั้น DOA > 4) → render logic-less (parity กับ tpl_render.js) · ไม่เก็บสำเนา PDF (snapshot flags = ✗ · OQ-07)
### F-TMP-003-FN-08: listVisible
- canSee = role-mgr-sales ∨ owner (ร่างของคนอื่นไม่เห็น) · count ต่อสถานะสำหรับ tabs · ใบไม่มีสิทธิ์ → 404 · CSV 1 แถวต่อรายการ (ใบที่ไม่มีรายการ = 1 แถวว่าง)

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-NOTIFY · Vendor master API (อ่าน) — ไม่มี engine ใหม่ · ไม่ใช้ ENG-DOC-STORE (OQ-07)

## §3.4 DOA hook (TODO: DOA engine — ไม่ใช้งานรอบนี้ · DEC-03)
คอลัมน์ใน `outsourced_transport_notice` (เตรียมไว้ ไม่ต้องย้าย schema เมื่อเปิด DOA กลาง):
| column | type | null | หมายเหตุ |
|---|---|---|---|
| approver_role | varchar(60) | Y | role ของขั้นสุดท้ายจาก DOA กลาง (ต้องมีใน doa-roles-contract) — ปัจจุบันว่าง |
| approved_by | uuid | Y | ผู้ตัดสินขั้นสุดท้าย — ปัจจุบันว่าง |
| approval_chain | jsonb | N default '[]' | snapshot สาย DOA ตอนส่ง (FN-03) — ปัจจุบัน [] (0 ขั้น) |
- FN-03 เรียก `DOA.resolve('outsourced_transport', ctx)` → ได้ 0 ขั้น → บันทึก [] · ห้าม hardcode กฎ/ผู้พิจารณาใน feature
- ถ้าลูกค้าเปลี่ยนมติให้มีผู้พิจารณา: ตั้ง entry ที่ DOA กลาง + ทำ DOA_BRIEF → FN-03 เปลี่ยน status เป็นรอพิจารณา (FRD รอบใหม่) · แบบพิมพ์เพิ่มช่องลงชื่อเองจาก sign_rows

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01, 02, 08 | FN-08 (+FN-04 summary) |
| 03 | FN-01, FN-02 |
| 04 | FN-01 |
| 05 | FN-03, FN-04, FN-06 |
| 06 | FN-05, FN-06 |
| 07 | FN-07 |
ทุก FN มี API ผูก ✓
