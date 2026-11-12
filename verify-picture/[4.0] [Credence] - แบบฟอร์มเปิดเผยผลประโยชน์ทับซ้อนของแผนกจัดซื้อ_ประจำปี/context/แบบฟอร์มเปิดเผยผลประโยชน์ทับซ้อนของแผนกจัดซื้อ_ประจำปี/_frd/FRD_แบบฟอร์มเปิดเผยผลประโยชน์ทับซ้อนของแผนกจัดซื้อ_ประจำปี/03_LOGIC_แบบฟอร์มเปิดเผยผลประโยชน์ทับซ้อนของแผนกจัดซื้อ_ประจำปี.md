# 03_LOGIC — F-TMP-006
> ไม่มีปีหรือถ้อยคำตายตัวใน logic — อ่านจาก CoiDisclosureConfig เท่านั้น (DEC-04)

## §3.1 Functions (Scope-Local)
### F-TMP-006-FN-01: validateDisclosure
- โหมดร่าง: ไม่บังคับช่องใด (has_conflict อาจว่าง) · ถ้า has_conflict = none → ล้าง conflict_detail
- โหมดส่ง (submit): has_conflict ∈ {none, has} (DEC-14) · has → conflict_detail.trim().length ≥ config.detail_min (DEC-15) · confirmed = true (DEC-04) → errors VR-01..03 (05 §5.4)
### F-TMP-006-FN-02: loadConfig
- อ่าน `CoiDisclosureConfig` (current_year · statement_text · closing_text · statement_version · detail_min) ณ วันสร้าง → `disclosure_year` snapshot ลงใบ · ถ้อยคำ snapshot ตอนส่ง (FN-05) · ใบเดิมไม่เปลี่ยนเมื่อ config เปลี่ยน (EC-10)
### F-TMP-006-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-10): ตรวจ F-DOCCFG status ของ doc_type COI (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('COI', company_ctx)` → snapshot ผู้เปิดเผย (คำนำหน้า/ชื่อ/ตำแหน่ง/แผนก) + `header_snapshot` (Organization: โลโก้) · หา supersedes: ใบ approved ปีเดียวกันของคนเดียวกัน (ไม่ถูกแทนที่) → supersedes_no (DEC-17)
### F-TMP-006-FN-04: saveDisclosure
- upsert header · has_conflict = none → conflict_detail = null (DEC-15) · confirmed → confirmed_at = now / ยกเลิกติ๊ก = null · ไม่รับ declarant/year จาก client
### F-TMP-006-FN-05: resolveAndSubmit
- FN-01 (โหมดส่ง) → `GET /doa/resolve?feature_id=F-TMP-006&declarant_id=…` → steps ค่าเริ่ม 1 ขั้น (role-line-manager "ผู้บังคับบัญชา") — DOA กลางเพิ่มขั้น role-compliance ได้ (OQ-03 · TODO: DOA engine) · client เลือก assignee ต่อขั้น (≠ owner) → snapshot `approval_chain` + statement_text_snapshot/closing_text_snapshot/statement_version · status=pending · submitted_at · มีใบปีเดียวกัน → warning DUPLICATE_YEAR (ไม่บล็อก) → FN-10 (has → coi_conflict_declared)
### F-TMP-006-FN-06: decideStep
- เฉพาะ assignee ขั้นปัจจุบัน · approve (รับทราบ) + note (ข้อคิดเห็น ไม่บังคับ) → ขั้นนั้น approved → ขั้นถัดไป pending หรือ status=approved (ครบ) → ใบที่ supersedes_no ชี้ = superseded_by_no ← doc_no นี้ → FN-09 render + `ENG-DOC-STORE.store(pdf,'COI',id,'approved_final')` · คำตัดสินแสดงตาม `print_config.decision_words.by_role` (role-line-manager = รับทราบ/ส่งกลับแก้ไข)
### F-TMP-006-FN-07: returnToDraft
- reject (ส่งกลับแก้ไข · เหตุผลบังคับ) → audit + returned_by/at/reason · status=returned (แก้ได้เหมือนร่าง · เลขเดิม) · ขั้นที่เหลือ = skipped · resolve ใหม่ตอนส่ง
### F-TMP-006-FN-08: cancelDisclosure
- owner หรือ role-compliance · status ∈ {draft, pending, returned} · เหตุผลบังคับ → cancelled · ขั้น pending/waiting = skipped → FN-10 `coi_cancelled` (ถ้าเดิม pending)
### F-TMP-006-FN-09: docPrintData + renderPdf
- ตรวจ canSee ก่อน · สร้าง data contract ตรงคีย์ `print/form.tpl.html` (COI_data-contract.md): company.logo (header_snapshot) · doc{title, year=disclosure_year, no, is_draft, supersedes, form_code, revision} · declarant{name, position} · statement_paras[] / closing_paras[] (snapshot) · conflict{none_box, has_box} · detail_lines[] (แยกบรรทัด เติมว่างครบ min_rows 3 · first) · comment_lines[] (approval_chain[].comment + ป้ายขั้น · เติมครบ 3) · sign_rows (`sign_rows.py` · ผู้เปิดเผย + 1 ช่อง/ขั้น · แถวละ ≤4) · layout.dense (รายละเอียด > 5 บรรทัด หรือ ขั้น > 4) → render HTML → PDF A4 1 หน้า (`--max-pages 1`)
### F-TMP-006-FN-10: emitEvents
- `ENG-NOTIFY.emit`: **coi_conflict_declared** (ส่งใบที่ has_conflict=has → role-compliance · บังคับ · in-app · vars ไม่มีรายละเอียด) · **coi_cancelled** (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน) · doa_pending/doa_result เป็นของ DOA engine ห้ามยิง
### F-TMP-006-FN-11: listVisible
- canSee = role-compliance ∨ owner ∨ (status≠draft ∧ อยู่ใน chain) · mine_to_act = pending ∧ assignee ขั้นปัจจุบัน = ฉัน · filter has_conflict ∈ {none, has, null} · year · ใบไม่มีสิทธิ์ → 404 · list/CSV ไม่คืน conflict_detail/comment

## §3.2 Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · DOA resolve (F-DLG-001) — ไม่มี engine ใหม่

## §3.3 API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,10 | FN-11 |
| 03 | FN-01, FN-02, FN-03 |
| 04 | FN-01, FN-04 |
| 05,06 | FN-05 (+FN-01, FN-10) |
| 07 | FN-06 (+FN-09) / FN-07 |
| 08 | FN-08 (+FN-10) |
| 09 | FN-09 |
| 12 | FN-02 |
ทุก FN มี API ผูก ✓
