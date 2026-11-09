# 03_LOGIC — F-TMP-002
> ไม่มีตัวเลขเกณฑ์ใน logic — อ่าน ServerRoomCheckConfig เท่านั้น (DEC-04)

## §3.1 Functions (Scope-Local)
### F-TMP-002-FN-01: validateRows
- Input `rows[]` → errors VR-01..03 (05 §5.4) · แถวที่ทุกค่าว่าง (แถวเตรียมกรอก) ตัดทิ้งก่อนตรวจ
### F-TMP-002-FN-02: evaluateRows
- ต่อแถว: issues = [อุณหภูมินอก criteria.temp_min_c..temp_max_c · ความชื้นนอก criteria.rh_min..rh_max · access_log=no · อุปกรณ์ใด=abnormal] · ใบ: abnormal_days · duplicate_dates · ทำซ้ำฝั่ง server เสมอ (ไม่เชื่อค่าจาก FE) · checked_by = ผู้เรียก API สำหรับแถวใหม่/แถวที่แก้ (BR-04)
- แถวที่ issues ใหม่ (ไม่มีในเวอร์ชันก่อน) → FN-08 src_abnormal_found (เตือน ไม่บล็อก DEC-04)
### F-TMP-002-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-09): ตรวจ F-DOCCFG status ของ doc_type SRC (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('SRC', company_ctx)` → snapshot ผู้บันทึก/ฝ่าย + `header_snapshot` (Organization: ชื่อบริษัท โลโก้) + `criteria_snapshot` (ServerRoomCheckConfig ณ เวลานั้น) · ห้าม format/+1 เอง
### F-TMP-002-FN-04: submitAndClose
- owner · status=draft → submitted · submitted_at = closed_at · FN-08 src_submitted · ไม่มีขั้นพิจารณา (DEC-03 — ไม่มี DOA entry ของ feature นี้ · DOA engine จึงไม่ยิง doa_pending)
- ลูกค้าต้องการผู้ตรวจทาน (OQ-02) = enhancement: DOA_BRIEF + field สายพิจารณา + FN ตัดสินขั้น
### F-TMP-002-FN-05: (ไม่มี — สงวนสำหรับ enhancement ผู้ตรวจทาน)
### F-TMP-002-FN-06: cancelCheck
- owner หรือ admin role (ฝ่าย IT) · status ∈ {draft, submitted} · เหตุผลบังคับ → cancelled → FN-08 src_cancelled
### F-TMP-002-FN-07: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html`: company · doc{title,no,is_draft,is_cancelled,form_code,revision} · criteria{temp_text,rh_text} (จาก criteria_snapshot) · pages[] = rows เรียงตามวันที่ เติมแถวว่างถึง print_config.min_rows แล้วแบ่ง print_config.rows_per_page ต่อหน้า (page_no · page_total · is_cont · has_next) · sign_rows[] = [] (ไม่มีบล็อกลงชื่อ DEC-07 · template รองรับไว้แล้ว) · layout.dense เมื่อแถว > print_config.dense_when_rows_over → render logic-less (parity กับ tpl_render.js) · วันที่ DD/MM/พ.ศ. · ตัวเลข 0.0 เป็น string
### F-TMP-002-FN-08: emitEvents
- `ENG-NOTIFY.emit`: **src_abnormal_found** (บันทึกแถวที่เข้าเกณฑ์เตือนใหม่ → admin role) · **src_submitted** (draft→submitted → admin role) · **src_cancelled** (→cancelled → owner + admin role)
### F-TMP-002-FN-09: listVisible
- canSee = admin role ∨ owner · result filter: abn = abnormal_days>0 · ใบไม่มีสิทธิ์ → 404

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-NOTIFY — ไม่มี engine ใหม่ · ไม่ใช้ DOA (DEC-03)

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,09 | FN-09 |
| 03 | FN-01, FN-02, FN-03 (+FN-08) |
| 04 | FN-01, FN-02 (+FN-08) |
| 05 | FN-04 (+FN-08) |
| 07 | FN-06 (+FN-08) |
| 08 | FN-07 |
ทุก FN มี API ผูก ✓
