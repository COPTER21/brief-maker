# 03_LOGIC — F-TMP-001
> ไม่มีค่าคงที่ตัวเลขบนกระดาษ (FORM_SPEC.constants ว่าง) · เครื่องหมาย / x มาจาก print_config.row_marks

## §3.1 Functions (Scope-Local)
### F-TMP-001-FN-01: validateCard
- Input `{location_id}` → VR-01 · ตรวจใบสถานะ active ของ location เดียวกัน → VR-02 (409 LOCATION_HAS_ACTIVE_CARD)
### F-TMP-001-FN-02: validateCheck
- Input `{check_date, gauge, seal_pin, hose, body}` → ครบ 4 หัวข้อ (VR-05) · check_date ≤ วันนี้ตาม timezone tenant (VR-03) · ไม่ซ้ำวันในใบ (VR-04) · ใบต้อง active
### F-TMP-001-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-09): ตรวจ F-DOCCFG status ของ doc_type FEC (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('FEC', company_ctx)` → snapshot `location_name_snapshot` + `header_snapshot` (Organization: ชื่อ ที่อยู่ โลโก้) · ห้าม format/+1 เอง
### F-TMP-001-FN-04: addCheck
- inspector_id = ผู้ใช้ปัจจุบัน (BR-06 · ไม่รับจาก body) · snapshot ชื่อ · is_abnormal = มีหัวข้อ abnormal ≥ 1 (BR-02) · คำนวณ last_check_date / last_result ของใบใหม่ (แถววันที่ล่าสุด)
### F-TMP-001-FN-05: editCheck
- เฉพาะ recorded_by = ผู้ใช้ และ date(recorded_at) = วันนี้ (BR-07) → 403 NOT_RECORDER / EDIT_WINDOW_CLOSED · audit เก็บค่าก่อน-หลัง · คำนวณ last_* ใหม่
### F-TMP-001-FN-06: cancelCard
- เจ้าของ หรือ role-mgr-wh · status = active · เหตุผลบังคับ → cancelled + cancel_reason · ล็อกการบันทึก
### F-TMP-001-FN-07: emitEvents
- `ENG-NOTIFY.emit`: **fec_abnormal_found** (FN-04/05 แถวมี x → role-mgr-wh · payload doc_no, location, abnormal_items, check_date) · **fec_cancelled** (FN-06 → role-mgr-wh · payload doc_no, location, actor, reason) · ห้าม hardcode ช่องทาง
### F-TMP-001-FN-08: listVisible
- canSee = role-mgr-wh ∨ warehouse_staff ∨ owner (DEC-08) · ใบไม่มีสิทธิ์ → 404 · ตัวกรอง status / last_result / zone
### F-TMP-001-FN-09: docPrintData + renderPdf
- data contract ตรงคีย์ `print/form.tpl.html`: company (header_snapshot) · doc{title,no,is_cancelled,form_code,revision} · location · checks[] (เรียงวันที่ · check_date "d MMM yy" พ.ศ. · เครื่องหมายจาก print_config.row_marks · inspector) เติมแถวว่างถึง print_config.min_rows · layout.dense เมื่อ checks > min_rows → render logic-less (parity กับ tpl_render.js) · ไม่มี sign_rows (DEC-07)

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-NOTIFY · Document Center — ไม่มี engine ใหม่ · ไม่ใช้ DOA (DEC-03)

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01, 02, 08 | FN-08 |
| 03 | FN-01, FN-02, FN-03, FN-04, FN-07 |
| 04 | FN-02, FN-04, FN-07 |
| 05 | FN-02, FN-05, FN-07 |
| 06 | FN-06, FN-07 |
| 07 | FN-09 |
ทุก FN มี API ผูก ✓
