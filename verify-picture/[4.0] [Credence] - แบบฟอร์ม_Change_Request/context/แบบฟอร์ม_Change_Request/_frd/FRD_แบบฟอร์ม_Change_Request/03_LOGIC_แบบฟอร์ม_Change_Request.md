# 03_LOGIC — F-TMP-005
> ไม่มีค่าคงที่ธุรกิจใน logic — สาย DOA จาก DOA กลาง · เลข/แบบพิมพ์จาก F-DOCCFG (DEC-03/10)

## §3.1 Functions (Scope-Local)
### F-TMP-005-FN-01: validateRequest
- Input `{subject, change_types[], change_type_other, due_date, delivery_location, change_detail, objective, impact, action_plan}` → errors VR-01..09 (05 §5.4) · change_types ว่าง → error (BR-01) · มี other แต่ไม่ระบุ → error (BR-02) · due_date < request_date → warning (ไม่ error · BR-03)
### F-TMP-005-FN-02: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type ITCR (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('ITCR', company_ctx)` → snapshot ชื่อ/ตำแหน่งผู้ขอ + `header_snapshot` (Organization: ชื่อบริษัท โลโก้) · ห้าม format/+1 เอง
### F-TMP-005-FN-03: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-005` → steps (ไม่มีวงเงิน · ค่าเริ่ม 2 ขั้น "ตรวจสอบโดย" → "อนุมัติโดย") · role-line-manager = ผู้บังคับบัญชาตามผัง · role-mgr-it = ผู้จัดการฝ่าย IT · resolve ไม่ได้ → ว่าง (เลือกเอง) · validate assignees ครบทุกขั้น + ≠ ผู้ขอ → snapshot `approval_chain` (freeze BR-DOA-02) · status draft→pending ขั้น 1 · ล้าง returned_*
### F-TMP-005-FN-04: decideStep (approve)
- เฉพาะ assignee ขั้นปัจจุบัน · ขั้นนั้น approved → ขั้นถัดไป pending (sequential) หรือ status=approved (ครบทุกขั้น) → FN-07 render + `ENG-DOC-STORE.store(pdf,'ITCR',id,'approved_final')` → emit `itcr_approved_for_it` (ENG-NOTIFY → role-it-officer) · ไม่เปลี่ยนค่าในระบบ/ไม่ส่งต่อ (DEC-01/02)
### F-TMP-005-FN-05: returnToDraft (reject)
- ผู้พิจารณาขั้นปัจจุบัน (ขั้นใดก็ได้) · เหตุผลบังคับ → audit "ไม่อนุมัติ — กลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08 · BR-DOA-03) · ร่างที่ตีกลับผู้พิจารณาไม่เห็น (DEC-09)
### F-TMP-005-FN-06: cancelRequest
- เจ้าของ หรือ role-it-officer · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → emit `itcr_cancelled` (ถ้าเดิม pending → ผู้พิจารณาขั้นปัจจุบัน)
### F-TMP-005-FN-07: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (ดู ITCR_print-spec §8): company(header_snapshot) · doc{title,no,is_draft,form_code,revision ← print_config} · req_date · employee{name,position} · due_date · delivery_location · subject · change_type{software,hardware,network,security,other → ☑/☐} · change_type_other · detail_lines/objective_lines/impact_lines/plan_lines (แตก \n · เติมว่างถึง print_config.text_min_rows 1/1/1/2) · sign_rows (ผู้ขอซื้อ + 1 ช่อง/ขั้น approval_chain · แถวละ ≤ sign_layout.max_per_row · คำตัดสินจาก decision_words.by_role) · layout.dense (บรรทัดเกินขั้นต่ำ > dense_when_rows_over หรือขั้น > dense_when_steps_over)
- render server = `render_doc.py` (ผลตรง tpl_render.js — parity IDENTICAL)
### F-TMP-005-FN-08: emitNotify
- เรียก `ENG-NOTIFY.emit(event_id, {ref, vars})` ตาม NTF_BRIEF — ห้ามเช็ค preference เอง
### F-TMP-005-FN-09: listVisible
- filter ตามสิทธิ์ (DEC-09): role-it-officer = ทั้งหมด · อื่น = ของตน + ใบที่ status ≠ draft และอยู่ใน approval_chain · tab act = pending และผู้พิจารณาขั้นปัจจุบัน · tab mine = ของตน

## §3.2 Engines (ใช้ของกลาง)
ENG-DOC-NUM (เลข) · ENG-DOC-STORE (สำเนา PDF) · ENG-NOTIFY (แจ้งเตือน) · DOA engine (resolve/decide hook) — ไม่มี engine ใหม่

## §3.3 State machine
| จาก | event | ไป | FN |
|---|---|---|---|
| — | create | draft | FN-01/02 |
| draft | submit | pending (ขั้น 1) | FN-03 |
| pending | approve ขั้น n<N | pending (ขั้น n+1) | FN-04 |
| pending | approve ขั้น N | approved | FN-04 → FN-07 → FN-08 |
| pending | reject | draft (เลขเดิม) | FN-05 |
| draft/pending | cancel | cancelled | FN-06 → FN-08 |

## §3.4 API ↔ Logic Trace
| API | FN |
|---|---|
| API-01/02/10 | FN-09 |
| API-03 | FN-01 → FN-02 |
| API-04 | FN-01 |
| API-06 | FN-03 |
| API-07 | FN-04 / FN-05 → FN-08 |
| API-08 | FN-06 → FN-08 |
| API-09 | FN-07 |
