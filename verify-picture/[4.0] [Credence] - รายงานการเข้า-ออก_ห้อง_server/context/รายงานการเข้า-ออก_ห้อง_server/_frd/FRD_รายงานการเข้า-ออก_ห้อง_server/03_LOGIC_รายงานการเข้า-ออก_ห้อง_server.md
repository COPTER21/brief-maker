# 03_LOGIC — F-TMP-006
> ไม่มีตัวเลขเกณฑ์ใน logic — อ่าน ServerRoomAccessConfig เท่านั้น (DEC-04)

## §3.1 Functions (Scope-Local)
### F-TMP-006-FN-01: validateEntries
- Input `entries[]` → errors VR-01..04 (05 §5.4) · แถวที่ชื่อและเหตุผลว่าง (แถวเตรียมกรอก) ตัดทิ้งก่อนตรวจ · out_date/out_time ต้องมาคู่กัน · `out ≥ in` (ออกก่อนเข้า = 422 OUT_BEFORE_IN · บล็อก DEC-04/12)
### F-TMP-006-FN-02: evaluateEntries
- ต่อแถว: issues = [ชั่วโมงอยู่ในห้อง (ถ้ายังไม่ออก = ถึงเวลาปัจจุบัน) > config.max_stay_hours] · ใบ: open_count · pending_cert_count · ผู้เข้าคนเดิมมีแถวค้างซ้อน (เตือน) · ทำซ้ำฝั่ง server เสมอ (ไม่เชื่อค่าจาก FE)
- แถวใหม่: visitor_signed_by = ผู้เรียก API · visitor_signed_at = now (BR-04) · visitor_emp_id = จับคู่ Employee ถ้าเลือกจากรายชื่อ
- แถวใหม่ → FN-08 sral_certify_pending · แถวที่ issues ใหม่ → FN-08 sral_overstay (เตือน ไม่บล็อก DEC-04) · job รายชั่วโมงตรวจแถวที่ยังไม่ออกแล้วเกินเกณฑ์ → sral_overstay (ครั้งเดียวต่อแถว)
### F-TMP-006-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-09): ตรวจ F-DOCCFG status ของ doc_type SRAL (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('SRAL', company_ctx)` → snapshot ผู้บันทึก/ฝ่าย + `header_snapshot` (Organization: ชื่อบริษัท โลโก้) · ห้าม format/+1 เอง
### F-TMP-006-FN-04: submitAndClose
- owner · status=draft · ทุกแถวมี out_date/out_time (422 ENTRIES_OPEN) และ certified_by (422 ENTRIES_NOT_CERTIFIED) → submitted · submitted_at = closed_at · FN-08 sral_submitted · ไม่มีขั้นพิจารณา (DEC-03 — ไม่มี DOA entry ของ feature นี้ · DOA engine จึงไม่ยิง doa_pending)
- ลูกค้าต้องการขออนุมัติก่อนเข้าห้อง (OQ-02) = enhancement: DOA_BRIEF + field สายพิจารณา + FN ตัดสินขั้น
### F-TMP-006-FN-05: (ไม่มี — สงวนสำหรับ enhancement ขั้นพิจารณา)
### F-TMP-006-FN-06: cancelLog
- owner หรือ admin role (ฝ่าย IT) · status ∈ {draft, submitted} · เหตุผลบังคับ → cancelled → FN-08 sral_cancelled
### F-TMP-006-FN-07: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html`: company · doc{title,no,is_draft,is_cancelled,form_code,revision} · pages[] = entries เรียงตามวันเวลาเข้า (visitor_name · visitor_department · in_date · in_time · out_date · out_time · purpose · visitor_signed · visitor_signed_at "ลงชื่อในระบบ dd/mm/yyyy HH:MM" · certified_by · certified_at "รับรองในระบบ …") เติมแถวว่างถึง print_config.min_rows แล้วปัดเต็มหน้า (pad_rows_to_page) แบ่ง print_config.rows_per_page ต่อหน้า (page_no · page_total · is_cont · has_next) · sign_rows[] = [] (ไม่มีบล็อกลงชื่อท้ายใบ DEC-07 · template รองรับไว้แล้ว) · layout.dense เมื่อแถว > print_config.dense_when_rows_over → render logic-less (parity กับ tpl_render.js) · วันที่ DD/MM/พ.ศ.
### F-TMP-006-FN-08: emitEvents
- `ENG-NOTIFY.emit`: **sral_certify_pending** (บันทึกแถวใหม่ → admin role ฝ่าย IT) · **sral_overstay** (แถวเกินเกณฑ์เวลา → admin role) · **sral_submitted** (draft→submitted → admin role) · **sral_cancelled** (→cancelled → owner + admin role)
### F-TMP-006-FN-09: listVisible
- canSee = admin role ∨ owner · cert filter: pend = pending_cert_count>0 · ใบไม่มีสิทธิ์ → 404
### F-TMP-006-FN-10: certifyEntry
- guard: status=draft · ผู้เรียกมี role-it-officer (หรือ admin role) และเห็นเอกสาร · แถวออกแล้ว · ยังไม่รับรอง · ผู้เรียก ≠ ผู้เข้า (visitor_emp_id และชื่อ — SoD DEC-13) → certified_by = ผู้เรียก · certified_at = now · audit "รับรองการเข้า-ออก" · แถวล็อกแก้ไข

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-NOTIFY — ไม่มี engine ใหม่ · ไม่ใช้ DOA (DEC-03)

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,09 | FN-09 |
| 03 | FN-01, FN-02, FN-03 (+FN-08) |
| 04 | FN-01, FN-02 (+FN-08) |
| 05 | FN-04 (+FN-08) |
| 06 | FN-10 |
| 07 | FN-06 (+FN-08) |
| 08 | FN-07 |
ทุก FN มี API ผูก ✓
