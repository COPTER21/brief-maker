# 03_LOGIC — F-TMP-003
> ไม่มีค่าคงที่ธุรกิจใน logic — สาย DOA จาก DOA กลาง · เลข/แบบพิมพ์จาก F-DOCCFG (DEC-03/10)

## §3.1 Functions (Scope-Local)
### F-TMP-003-FN-01: validateRequest
- Input `{detail, program, data_types[], period_from, period_to, destroy_reasons[], destroy_reason_other, destroy_methods[], destroy_method_other}` → errors VR-01..09 (05 §5.4) · period_to < period_from → error (BR-03) · period_to > req_date → warning (ไม่ error · BR-04)
### F-TMP-003-FN-02: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type DRITS (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('DRITS', company_ctx)` → snapshot ชื่อ/ตำแหน่งผู้ร้องขอ + `header_snapshot` (Organization: ชื่อบริษัท โลโก้) · ห้าม format/+1 เอง
### F-TMP-003-FN-03: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-003` → steps (ไม่มีวงเงิน · ค่าเริ่ม 2 ขั้น) · role-line-manager = ผู้บังคับบัญชาตามผัง · role-mgr-it = ผู้จัดการฝ่าย IT · resolve ไม่ได้ → ว่าง (เลือกเอง) · validate assignees ครบทุกขั้น + ≠ ผู้ร้องขอ → snapshot `approval_chain` (freeze BR-DOA-02) · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-003-FN-04: decideStep (approve)
- เฉพาะ assignee ขั้นปัจจุบัน · ขั้นนั้น approved → ขั้นถัดไป pending (sequential) หรือ status=approved (ครบ) → FN-08 render + `ENG-DOC-STORE.store(pdf,'DRITS',id,'approved_final')` → emit `drits_ready_for_it` (ENG-NOTIFY → role-it-officer) · ไม่เปลี่ยนค่าในระบบ/ไม่ส่งต่อ (DEC-01/02)
### F-TMP-003-FN-05: returnToDraft (reject)
- ขั้นใดก็ได้ · เหตุผลบังคับ → audit "ไม่อนุมัติ — กลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08 · BR-DOA-03)
### F-TMP-003-FN-06: cancelRequest
- เจ้าของ หรือ role-it-officer · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → emit `drits_cancelled` (ถ้าเดิม pending → ผู้พิจารณาขั้นปัจจุบัน)
### F-TMP-003-FN-07: markDestroyed
- role-it-officer · status=approved → done (ทำลายแล้ว) · performed_by = ผู้ใช้ · performed_at = now · done_note (ไม่บังคับ) → FN-08 render ใหม่ (ช่อง เจ้าหน้าที่ IT) → emit `drits_destroyed` (→ ผู้ร้องขอ)
### F-TMP-003-FN-08: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (ดู print-spec §8): company(header_snapshot) · doc{title,no,is_draft,form_code,revision ← print_config} · req_date · employee{name,position} · detail_lines/program_lines (แตก \n · เติมว่างถึง print_config.text_min_rows 3/2) · data_type{10 keys → ☑/☐} · period_from/period_to · destroy_reason{4 keys} · destroy_reason_other · destroy_method{4 keys} · destroy_method_other · sign_rows (ผู้ร้องขอ + 1 ช่อง/ขั้น approval_chain + เจ้าหน้าที่ IT · แถวละ ≤ sign_layout.max_per_row · คำตัดสินจาก decision_words.by_role) · layout.dense
- render server = `render_doc.py` (ผลตรง tpl_render.js — parity IDENTICAL)
### F-TMP-003-FN-09: emitNotify
- เรียก `ENG-NOTIFY.emit(event_id, {ref, vars})` ตาม NTF_BRIEF — ห้ามเช็ค preference เอง
### F-TMP-003-FN-10: listVisible
- filter ตามสิทธิ์ (DEC-09): role-it-officer = ทั้งหมด · อื่น = ของตน + ใบที่ status ≠ draft และอยู่ใน approval_chain · tab act = pending และผู้พิจารณาขั้นปัจจุบัน · tab mine = ของตน

## §3.2 Engines (ใช้ของกลาง)
ENG-DOC-NUM (เลข) · ENG-DOC-STORE (สำเนา PDF) · ENG-NOTIFY (แจ้งเตือน) · DOA engine (resolve/decide hook) — ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| API-01/02/11 | FN-10 |
| API-03 | FN-01 → FN-02 |
| API-04 | FN-01 |
| API-06 | FN-03 |
| API-07 | FN-04 / FN-05 → FN-09 |
| API-08 | FN-07 → FN-08 → FN-09 |
| API-09 | FN-06 → FN-09 |
| API-10 | FN-08 |
