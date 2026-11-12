# 03_LOGIC — F-TMP-007
> ไม่มีค่าคงที่ธุรกิจใน logic — สาย DOA จาก DOA กลาง · เลข/แบบพิมพ์จาก F-DOCCFG · หน่วยงานแจกจ่ายจาก Organization (DEC-03/10/12)

## §3.1 Functions (Scope-Local)
### F-TMP-007-FN-01: validateDar
- Input `{purpose, issue_type, target_doc_no, target_revision, target_doc_name, effective_date, pl_wi_step, origin, origin_detail, change_before, change_after, related[], distribution_units[], distribution_remark, receive_methods[], distribution_emails}` → errors VR-01..10 (05 §5.4)
- purpose/issue_type ต้องมี 1 ค่า (BR-01/02) · purpose = revise → change_before + change_after · purpose ∈ {new, other} → change_after (BR-03) · origin = other → origin_detail (BR-04) · distribution_units ≥1 · receive_methods ≥1 · email → distribution_emails แยกด้วย , ; เว้นวรรค ≥1 และทุกที่อยู่รูปแบบถูก (BR-05) · related แต่ละแถว: กรอกช่องเดียว = error (BR-07) · effective_date < dar_date → warning ไม่ error (BR-06)
### F-TMP-007-FN-02: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type DAR (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('DAR', company_ctx)` → snapshot ชื่อ/ฝ่าย/แผนกผู้จัดทำ + `header_snapshot` (Organization: ชื่อบริษัท โลโก้) · ห้าม format/+1 เอง
### F-TMP-007-FN-03: resolveAndSubmit
- `GET /doa/resolve?feature_id=F-TMP-007` → steps (ไม่มีวงเงิน · ค่าเริ่ม 4 ขั้น "ผู้ตรวจสอบ" role-line-manager → "ผู้อนุมัติ" role-mgr-bu → "ผู้ควบคุมเอกสาร" role-doc-controller → "ผู้จัดการฝ่ายสำนักเลขานุการบริษัท" role-mgr-ocs) · role-line-manager = ผู้บังคับบัญชาตามผัง · resolve ไม่ได้ → ว่าง (เลือกเอง) · validate assignees ครบทุกขั้น + ≠ ผู้จัดทำ → snapshot `approval_chain` (freeze BR-DOA-02) · status draft→pending ขั้น 1 · ล้าง returned_* · `TODO: DOA engine`
### F-TMP-007-FN-04: decideStep (approve)
- เฉพาะ assignee ขั้นปัจจุบัน · ขั้นนั้น approved → ขั้นถัดไป pending (sequential) หรือ status=approved (ครบทุกขั้น) → FN-07 render + `ENG-DOC-STORE.store(pdf,'DAR',id,'approved_final')` → emit `dar_distributed` (ENG-NOTIFY → หน่วยงานใน distribution_units + distribution_emails) · ไม่เปลี่ยนค่าในระบบ/ไม่ส่งต่อ (DEC-01/02)
### F-TMP-007-FN-05: returnToDraft (reject)
- ผู้พิจารณาขั้นปัจจุบัน (ขั้นใดก็ได้) · เหตุผลบังคับ → audit "ไม่อนุมัติ — กลับเป็นร่าง" + returned_by/at/reason · status=draft เลขเดิม · approval_chain เดิมย้ายลง audit แล้วล้าง (resolve ใหม่ตอนส่ง — DEC-08 · BR-DOA-03) · ร่างที่ตีกลับผู้พิจารณาไม่เห็น (DEC-09)
### F-TMP-007-FN-06: cancelDar
- เจ้าของ หรือ role-doc-controller · status ∈ {draft, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → emit `dar_cancelled` (ถ้าเดิม pending → ผู้พิจารณาขั้นปัจจุบัน)
### F-TMP-007-FN-07: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (ดู DAR_print-spec §8 · DAR_data-contract.md): company(header_snapshot) · doc{title,no,is_draft,is_cancelled,form_code,revision ← print_config} · dar_date · requester{name,division,department} · target{doc_no,revision,doc_name,effective_date,pl_wi_step} · purpose/issue/origin{… → ☑/☐} · origin_detail · change_rows (แตก \n เดิม/ใหม่ · เติมว่างถึง print_config.change_min_rows) · related_p1 (หน้า 1 = print_config.page1_row_budget − จำนวนแถวแก้ไข · เติมว่าง) · related_cont + has_related_cont (ส่วนเกิน → ตารางต่อหน้า 2) · dist_rows (หน่วยงานจาก Organization แถวละ print_config.dist_cols) · distribution{remark,emails} · receive{email,paper} · receipt{name,date} · sign_rows (ผู้จัดทำ + 1 ช่อง/ขั้น approval_chain · แถวละ ≤ sign_layout.max_per_row · คำตัดสินจาก decision_words.by_role) · layout.dense (related > dense_when_rows_over หรือขั้น > dense_when_steps_over)
- render server = `render_doc.py` (ผลตรง tpl_render.js — parity IDENTICAL) · A4 แนวตั้ง 2 หน้า (print_config.pages)
### F-TMP-007-FN-08: recordReceipt (ลงนามรับเอกสารควบคุม)
- role-doc-controller · status = approved · receiver_id บังคับ (≠ ผู้จัดทำบันทึกเอง) → received_by/at/recorded_by · status=received · audit "ลงนามรับเอกสารควบคุม" → emit `dar_received` (เจ้าของ + role-doc-controller) · ไม่ใช่ขั้น DOA (DEC-07)
### F-TMP-007-FN-09: emitNotify
- เรียก `ENG-NOTIFY.emit(event_id, {ref, vars})` ตาม NTF_BRIEF (dar_cancelled · dar_distributed · dar_received) — ห้ามเช็ค preference เอง
### F-TMP-007-FN-10: listVisible
- filter ตามสิทธิ์ (DEC-09): role-doc-controller (admin) = ทั้งหมด · อื่น = ของตน + ใบที่ status ≠ draft และอยู่ใน approval_chain · tab act = (pending และผู้พิจารณาขั้นปัจจุบัน) หรือ (approved และ admin) · tab mine = ของตน

## §3.2 Engines (ใช้ของกลาง)
ENG-DOC-NUM (เลข) · ENG-DOC-STORE (สำเนา PDF) · ENG-NOTIFY (แจ้งเตือน) · DOA engine (resolve/decide hook) — ไม่มี engine ใหม่

## §3.3 State machine
| จาก | event | ไป | FN |
|---|---|---|---|
| — | create | draft | FN-01/02 |
| draft | submit | pending (ขั้น 1) | FN-03 |
| pending | approve ขั้น n<N | pending (ขั้น n+1) | FN-04 |
| pending | approve ขั้น N | approved | FN-04 → FN-07 → FN-09 |
| pending | reject | draft (เลขเดิม) | FN-05 |
| approved | receive | received | FN-08 → FN-09 |
| draft/pending | cancel | cancelled | FN-06 → FN-09 |

## §3.4 API ↔ Logic Trace
| API | FN |
|---|---|
| API-01/02/11 | FN-10 |
| API-03 | FN-01 → FN-02 |
| API-04 | FN-01 |
| API-06 | FN-03 |
| API-07 | FN-04 / FN-05 → FN-09 |
| API-08 | FN-06 → FN-09 |
| API-09 | FN-08 → FN-09 |
| API-10 | FN-07 |
