# 03_LOGIC — F-TMP-003
> ไม่มีสูตรตัวเลข · ค่าคงที่บนกระดาษ 1 ชุด = รายการตรวจสอบ 8 ข้อ → อ่านจาก config ivmk.checklist_items (BR-01 · ห้าม hardcode)

## §3.1 Functions (Scope-Local)
### F-TMP-003-FN-01: validateRecord
- Input `{project_name, closing_date, outcome, post_owner_employee_id, archive_location, checks[], lessons[]}` → errors VR-01..06/09 (05 §5.4) · closing_date ≤ วันนี้
- ต่อรายการ: status=done → owner + done_date บังคับ · done_date ≤ closing_date (BR-03/04) · status=na → remark บังคับ · ถ้อยคำ/จำนวนรายการต้องตรง snapshot ของใบ (ห้ามเพิ่ม/ลบ)
- บทเรียน: มี topic → lesson บังคับ · มีช่องอื่นแต่ไม่มี topic → error · แถวว่างทั้งแถวตัดทิ้ง
- `forSubmit=true` (API-06): ทุกรายการ ∈ {done, na} (BR-02 · 422 CHECKLIST_INCOMPLETE) · รายการ "บันทึกบทเรียนที่ได้รับ" = done → lessons ≥ 1 (BR-05 · 422 LESSON_REQUIRED) · บันทึกร่าง (API-03/04) ไม่ตรวจข้อนี้
### F-TMP-003-FN-02: attachFiles
- ผ่าน Document Center (ref_type='IVMK') · file_policy ≤20MB · pdf/doc/xls/รูป
### F-TMP-003-FN-03: issueNumber + initChecklist
- เรียกตอนบันทึกครั้งแรก (DEC-11): ตรวจ F-DOCCFG status ของ doc_type IVMK (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('IVMK', company_ctx)` → snapshot ผู้จัดทำ/ตำแหน่ง + `header_snapshot` (Organization: ชื่อบริษัท โลโก้ บรรทัด "… และบริษัทในเครือ") · ห้าม format/+1 เอง
- initChecklist: อ่าน config `ivmk.checklist_items` (company_ctx · เวอร์ชันที่มีผล ณ วันที่สร้าง) → สร้าง ivm_closing_check ทุกข้อ status=not_started · เก็บ `item_text` + `checklist_config_ver` (snapshot — แก้ config ภายหลังไม่กระทบใบเดิม · EC-07) · API-12 คืนชุดเดียวกันให้ฟอร์มใหม่
### F-TMP-003-FN-04: resolveAndSubmit
- FN-01(forSubmit) ต้องผ่านก่อน → `GET /doa/resolve?feature_id=F-TMP-003` → steps (ไม่มีวงเงิน) · role-line-manager = ผู้บังคับบัญชาตามผัง · role-gm ตาม DOA · ผู้ resolve ได้ = ผู้จัดทำ → ว่าง (เลือกเอง) · validate assignees ครบ + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) + `approver_role` ต่อขั้น · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-003-FN-05: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve: ขั้นนั้น approved (คำตามบทบาท: role-line-manager = ตรวจสอบแล้ว · role-gm = อนุมัติ) → ขั้นถัดไป pending หรือ (ขั้นสุดท้าย) status=approved · `approved_by`/`approved_at` → FN-08 render + `ENG-DOC-STORE.store(pdf,'IVMK',id,'approved_final')` → FN-09 ivmk_closed_handover + ivmk_lesson_assigned
### F-TMP-003-FN-06: returnToDraft
- reject (เหตุผลบังคับ) → audit "{คำปฏิเสธของขั้น} (ขั้น n)" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-09 · BR-DOA-03 ตามปกติ)
### F-TMP-003-FN-07: cancelRecord
- owner หรือ admin role ฝ่ายบริหารการลงทุน · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending/waiting = skipped → FN-09 ivmk_cancelled (ถ้าเดิม pending)
### F-TMP-003-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (company{name, name_line, logo} · doc{title, no, is_draft, form_code, revision} · project{name} · closing{date (วันที่ไทยเต็ม), outcome, post_owner, archive_location} · checklist[]{item, status (ป้ายไทย), owner, done_date (วันที่ไทยย่อ), remark} · lessons[]{topic, lesson, owner, due_date} (เติมว่างถึง 10 แถว) · form_revisions[] จาก F-DOCCFG · sign_rows[] = ผู้จัดทำ + 1 ช่องต่อขั้นใน approval_chain snapshot — **จำนวนตามที่ตั้งใน DOA ไม่ fix** · คำตัดสินจาก print_config.decision_words.by_role[role_id] · layout.dense (บทเรียน > 10 หรือ ขั้น > 4)) → render logic-less 2 หน้า (R10 · parity กับ tpl_render.js)
### F-TMP-003-FN-09: emitEvents
- `ENG-NOTIFY.emit`: **ivmk_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · **ivmk_closed_handover** (→approved → ผู้รับผิดชอบหลังปิดงาน + ผู้รับผิดชอบรายการตรวจสอบ) · **ivmk_lesson_assigned** (→approved → ผู้รับผิดชอบบทเรียนแต่ละแถวที่มีกำหนดส่ง) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ · `ivmk.approved` ประกาศไว้ ไม่ยิงรอบนี้ (DEC-02)
### F-TMP-003-FN-10: listVisible
- canSee = admin ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · checklist=complete ⇔ ทุกข้อ done/na · ใบไม่มีสิทธิ์ → 404 · CSV ใช้ตัวกรองเดียวกัน

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — `TODO: DOA engine` ฝั่ง prototype = MOCK_DOA_RESOLVED (DOA-ENGINE-HOOK) · ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,10 | FN-10 |
| 03 | FN-01, FN-03 |
| 04 | FN-01 |
| 05 | FN-04 |
| 06 | FN-01, FN-04 |
| 07 | FN-05 (+FN-08, FN-09) / FN-06 |
| 08 | FN-07 (+FN-09) |
| 09 | FN-08 |
| 11 | FN-02 |
| 12 | FN-03 |
ทุก FN มี API ผูก ✓
