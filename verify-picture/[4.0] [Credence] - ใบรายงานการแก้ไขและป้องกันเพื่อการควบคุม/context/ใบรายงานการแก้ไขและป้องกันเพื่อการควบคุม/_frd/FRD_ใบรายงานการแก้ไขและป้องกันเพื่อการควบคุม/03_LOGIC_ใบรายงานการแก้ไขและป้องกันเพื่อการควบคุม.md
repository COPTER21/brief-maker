# 03_LOGIC — F-TMP-008
> ไม่มีค่าคงที่ธุรกิจใน logic — เกณฑ์เวลาเริ่มวิเคราะห์อ่านจาก CarConfig.analysis_start_minutes · สาย DOA จาก DOA กลาง · เลข/แบบพิมพ์จาก F-DOCCFG (DEC-03/04/27)

## §3.1 Functions (Scope-Local)
### F-TMP-008-FN-01: validateReport
- Input ช่วงการจัดทำ (หัว · 1 · 2 · total_qty · symptoms[] · attendees[] · analysis_doc_no · why*_prep · root_prep · actions_prep · fixes_prep · prevent_prep · docs_to_fix · risk_*) → errors VR-01..06
- found_date+found_time > now → error (BR-03) · symptoms: is_new=true และมี recur_no → error · is_new=false และ recur_no < 1 → error (BR-05) · ตัวเลขต้องเป็นจำนวนเต็ม ≥ 0
- warnings (ไม่บล็อก): Σ qty / Σ eff_qty > total_qty (BR-02) · ระดับทำไมถัดไปมีแถวแต่ระดับก่อนไม่มี proven=true (BR-06) · กำหนดเสร็จ < found_date (BR-09)
### F-TMP-008-FN-02: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-27): ตรวจ F-DOCCFG status ของ doc_type CAR (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('CAR', company_ctx)` → snapshot department ของผู้จัดทำ + `header_snapshot` (Organization: ชื่อบริษัท โลโก้) · ห้าม format/+1 เอง
- เทียบเวลาบันทึกครั้งแรกกับ found_date+found_time: เกิน CarConfig.analysis_start_minutes (config) → เก็บ late_start_minutes + เตือน (BR-04)
### F-TMP-008-FN-03: calcSymptoms
- pct = qty ÷ total_qty × 100 (ปัด 2 ตำแหน่ง) · eff_pct แบบเดียวกันจาก eff_qty · sum_qty/sum_pct/sum_eff_qty/sum_eff_pct = ผลรวม · total_qty ว่าง/ศูนย์ → pct ว่าง (EC-01) · คำนวณฝั่ง server ทุกครั้งที่บันทึก (ไม่เชื่อค่าจาก client)
### F-TMP-008-FN-04: submitForReview
- เจ้าของ · status=draft · ตรวจขั้นต่ำ BR-07 (ขาด → 400 SUBMIT_INCOMPLETE + รายการ) · `GET /doa/resolve?feature_id=F-TMP-008` → steps (ไม่มีวงเงิน · ค่าเริ่ม 4 ขั้น GM/AMD/ผู้จัดการฝ่าย → MD → IC → IC Mgr.) · validate assignees ครบทุกขั้น + ≠ ผู้จัดทำ (SoD) → snapshot `approval_chain` (freeze BR-DOA-02 · ทุกขั้น waiting) · ตั้ง reviewer (role-ic-officer) · resolve ผู้ลงนามตรวจสอบ 7 จุดตาม role → `car_review_signs` · status draft→in_review · ล้าง returned_* → emit `car_submitted_for_review` (FN-13)
### F-TMP-008-FN-05: saveReview
- เฉพาะ reviewer · status=in_review · บันทึก why1_rev/why2_rev/why3_rev/root_rev · actions_rev · d_rev_due/d_rev_owner · fixes_rev · fix_rev_due/fix_rev_owner · prevent_rev · doc3_check (DEC-31) · warnings BR-06 (ช่วงการตรวจสอบ)
### F-TMP-008-FN-06: signReviewPoint
- status=in_review · ผู้เรียก = assignee ของจุดนั้น (hod=role-line-manager ของผู้จัดทำ · icm_d/icm_61/icm_10/icm_11=role-ic-mgr · md_61/md_11=role-md) · ผู้เรียก ≠ ผู้จัดทำ (403 SOD_SELF · BR-10) · บันทึก signed_by/signed_at (ลงนามหลายจุดในคำสั่งเดียวได้ · EC-07) · audit "ลงนามตรวจสอบ · {label}"
### F-TMP-008-FN-07: returnFromReview
- reviewer · status=in_review · เหตุผลบังคับ → status=draft เลขเดิม · returned_* (kind=review) · ล้าง car_review_signs + approval_chain (ย้ายลง audit · DEC-25 · EC-08) · emit `car_review_returned` → owner
### F-TMP-008-FN-08: sendForApproval
- reviewer · status=in_review · car_review_signs ครบ 7 จุด (ไม่ครบ → 400 REVIEW_SIGNS_INCOMPLETE · BR-08) → approval_chain ขั้น 1 = pending · status=pending · sent_at · DOA engine แจ้งผู้พิจารณา (doa_pending)
### F-TMP-008-FN-09: decideStep (approve)
- เฉพาะ assignee ขั้นปัจจุบัน (403 NOT_CURRENT_APPROVER) · ขั้นนั้น approved → ขั้นถัดไป pending (sequential) หรือ status=approved (ครบทุกขั้น) → FN-12 render + `ENG-DOC-STORE.store(pdf,'CAR',id,'approved_final')` · ไม่เปลี่ยนค่าในระบบ/ไม่ส่งต่อ (DEC-01/02)
### F-TMP-008-FN-10: rejectToDraft
- ผู้พิจารณาขั้นปัจจุบัน (ขั้นใดก็ได้) · เหตุผลบังคับ → audit "ไม่อนุมัติ — กลับเป็นร่าง" + returned_* (kind=doa) · status=draft เลขเดิม · ล้าง approval_chain + car_review_signs (resolve ใหม่ตอนส่ง · DEC-25 · BR-DOA-03) · ร่างที่ตีกลับผู้พิจารณาไม่เห็น (DEC-26)
### F-TMP-008-FN-11: cancelReport
- เจ้าของ หรือ admin role IC · status ∈ {draft, in_review, pending} · เหตุผลบังคับ → cancelled · ขั้น pending = skipped → emit `car_cancelled` (ผู้ตรวจสอบเมื่อเดิม in_review / ผู้พิจารณาขั้นปัจจุบันเมื่อเดิม pending)
### F-TMP-008-FN-12: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (CAR_print-spec §8): company(header_snapshot) · doc{title,title_full,no,is_draft,form_code,revision ← print_config} · head{doc_name,doc_ref_no,dept,finder,found_date,found_time} · problem · kpi_target · total_qty · symptoms[] (เติมแถวว่างถึง print_config.group_min_rows) · sum · attendee_rows (4 คอลัมน์/แถว · เลข 1,2 ซ้อนคอลัมน์แรก) · analysis_doc_no · analysis_note (จาก CarConfig) · w12_prep/w12_rev/w3r_prep/w3r_rev ({a,b}) · act_rows/fix_rows/prev_rows ({p,r}) · act_due/fix_due · docs_rows (3 ช่อง/แถว) · risk · doc3_rows (first/span) · rv.{hod,icm_d,md_61,icm_61,icm_10,md_11,icm_11} · sign_rows (1 ช่อง/ขั้น approval_chain · ไม่มีช่องผู้จัดทำ · แถวละ ≤ sign_layout.max_per_row · คำตัดสินจาก decision_words.by_role)
- render server = `render_doc.py` (ผลตรง tpl_render.js — parity IDENTICAL) · A4 2 หน้า (print_config.pages)
### F-TMP-008-FN-13: emitNotify
- เรียก `ENG-NOTIFY.emit(event_id, {ref, vars})` ตาม NTF_BRIEF — car_submitted_for_review (FN-04) · car_review_returned (FN-07) · car_cancelled (FN-11) — ห้ามเช็ค preference เอง · DOA events มาจาก DOA engine
### F-TMP-008-FN-14: listVisible
- filter ตามสิทธิ์ (DEC-26): admin role IC = ทั้งหมด · อื่น = ของตน + ใบที่ status ≠ draft และตนเป็น reviewer / assignee ใน car_review_signs / approval_chain · tab act = (pending และขั้นปัจจุบัน) หรือ (in_review และ reviewer) หรือ (in_review และมีจุดลงนามของตนค้าง) · tab mine = ของตน

## §3.2 Engines (ใช้ของกลาง)
ENG-DOC-NUM (เลข) · ENG-DOC-STORE (สำเนา PDF) · ENG-NOTIFY (แจ้งเตือน) · DOA engine (resolve/decide hook) — ไม่มี engine ใหม่

## §3.3 State machine
| จาก | event | ไป | FN |
|---|---|---|---|
| — | create | draft | FN-01/02/03 |
| draft | submit-review | in_review | FN-04 → FN-13 |
| in_review | save-review / sign | in_review | FN-05 / FN-06 |
| in_review | return | draft (เลขเดิม) | FN-07 → FN-13 |
| in_review | send-approval (ลงนามครบ 7) | pending (ขั้น 1) | FN-08 |
| pending | approve ขั้น n<N | pending (ขั้น n+1) | FN-09 |
| pending | approve ขั้น N | approved | FN-09 → FN-12 |
| pending | reject | draft (เลขเดิม) | FN-10 |
| draft/in_review/pending | cancel | cancelled | FN-11 → FN-13 |

## §3.4 API ↔ Logic Trace
| API | FN |
|---|---|
| API-01/02/14 | FN-14 |
| API-03 | FN-01 → FN-02 → FN-03 |
| API-04 | FN-01 → FN-03 |
| API-05 | FN-04 |
| API-06 | FN-05 |
| API-07 | FN-06 |
| API-08 | FN-07 |
| API-09 | FN-08 |
| API-10 | FN-09 / FN-10 |
| API-11 | FN-11 |
| API-12 | FN-12 |
