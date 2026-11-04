# RUN_LOG — F-TMP-002 แบบฟอร์ม Exit Interview (REQ-TMP-002)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพฟอร์ม: to_image.py วิธี LibreOffice → PDF → pypdfium2 (3 หน้า) = หน้ากระดาษจริงจาก docx (ฟอนต์ไทยในเครื่องไม่มี ภาพแสดงกล่องแทนอักษร) → ถ้อยคำยึด content.html · ตำแหน่ง/เส้นยึดภาพ
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC ล้วน
- form_spec_check: ERROR 0 · WARN 0 · 20 ช่อง · ตัวเลือก 31 (ตารางความพึงพอใจ 26 ข้อ = choice ละ 5 ระดับ) · แถวซ้ำ 2 · ลายเซ็น 1 (ผู้ให้ข้อมูล — ไม่มีช่องผู้อนุมัติ)
- ฟอร์มว่าง ไม่มีข้อมูลส่วนบุคคลตัวอย่าง · ชื่อเอกสารไม่เพี้ยน (ไม่ต้อง rename) · หัวฟอร์ม "แบบสอบถามบุคลากรที่พ้นจากงาน ( Exit Interview)" FM-HRM-06
- feature ที่ใกล้: HR · Offboard (FEATURE_REGISTRY ยังไม่มีรหัส) → ใช้ F-TMP-002 ชั่วคราว
- 2026-10-08 12:34 · ขั้น 1 → done · FORM_SPEC ERROR 0 · PREBRIEF v2 จาก FORM_SPEC

## ขั้น 2 · gate (unattended — AI-DEFAULT)
- G1: ไม่เปลี่ยน config/ไม่ส่งต่อ — เป็นแบบสอบถาม การพ้นสภาพพนักงานอยู่ HR·Offboard
- G2: กระดาษมีแค่ "ผู้ให้ข้อมูล" ไม่มีช่องผู้อนุมัติ → ไม่มี DOA (ส่งแล้ว HR รับทราบ/ปิดใบ) · G7 จึงไม่มี DEC (ยกเลิกได้: เจ้าของ+HR ที่ร่าง/ส่งแล้ว ระบุเหตุผล — ใส่ใน FRD)
- G3: คำนวณอายุตัว/อายุงานอัตโนมัติ ปรับได้ · กฎบล็อกตามตรรกะฟอร์ม · G4: ไม่จำกัดแถว · G5: 1:1 แก้ "กรอบ→กรอก", "P→✓"
- G8: ความลับ — ผู้บังคับบัญชาไม่เห็น (มีคำถามประเมินหัวหน้า) · HR (role-mgr-hr) เห็นทั้งหมด · G9: EXI ออกเลขบันทึกครั้งแรก · G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock พร้อมเริ่มทำ (17 มติ · AI-DEFAULT 11 · VALID 6) · dm.sh tag แล้ว
- 2026-10-08 12:35 · ขั้น 2 → done · 17 มติ · AI-DEFAULT 11

## ขั้น 3 · declaration ร่าง
- doa: ไม่ทำ — DEC-03 ไม่มีการอนุมัติ (doa_tool init ตอบ "ไม่ต้องทำ DOA_BRIEF · ห้ามยัด DOA") → DOA BLOCK 0 (N/A) · ฟิลด์ approver_role/approved_by/approval_chain ไม่ใช้ (ไม่มีอนุมัติ)
- ntf: exi_submitted (→ role-mgr-hr) · exi_cancelled · ตัด exi_over_limit_approved จาก suggest · VERDICT PASS
- doccfg (หลังขั้น 4): EXI · {PREFIX}-{YYYY}-{run:4} · first_save · --registry ไม่ชน · VERDICT PASS
- mdoc: EXI · FRM · function_code F01 ชั่วคราว (ไม่มีตาราง taxonomy) · source=declaration (REQ-TMP-002 ไม่ใช่รูปแบบ REQ-YYYY-NNNN → G10 BLOCK ถ้าเป็น request) · VERDICT WARN (G04 taxonomy_def_id ว่าง)

## ขั้น 4 · แบบพิมพ์ Replica
- form.tpl.html สร้างจาก FORM_SPEC ด้วย print/make_print.py (ถ้อยคำในเทมเพลต · data มีแค่ค่า) · R4 เส้นประ (ส่วน 1) + R9 ตาราง (ส่วน 2/3/4) + R8 + B6 sign_rows + B7
- data 4 สถานะ (สมมติทั้งหมด ไม่ใช้ข้อมูลลูกค้า): draft · submitted · contract-end · long-12rows-allreasons · สถานะ "DOA 6 ขั้น" ไม่ใช้ (ไม่มี DOA — DEC-03)
- parity_check: IDENTICAL 4/4 · ไม่มี {{}} หลง · missing keys 0 · build_html ทุกสถานะ → print/out/*.html + EXI_template.html
- [NO-BROWSER] ข้าม render_pdf.py (ใน render_states.py) — ไม่ได้ PDF/_states_sheet.png/จำนวนหน้า → ทำ HTML ต่อสถานะแทน (print/out/*.html)
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ PDF ที่ render จาก browser)
- หมายเหตุ QA: ผู้ทำได้ตรวจด้วยตาจาก browser นอกเครื่อง (sandbox) — submitted = 3 หน้า, long = 3 หน้า, layout ตรงลำดับกระดาษ (ไม่ใช่ผลด่านทางการ)
- 2026-10-08 12:40 · ขั้น 4 → done · parity 4/4 · [NO-BROWSER] ไม่มี PDF/compare
- 2026-10-08 12:40 · ขั้น 3 → done · DOA N/A (DEC-03) · ntf PASS · doccfg PASS · mdoc WARN G04

## ขั้น 5 · HTML Q-form
- ฐาน: html-generator-v9 references/form-archetype/_SOURCE (Q2) + เทียบ GOLDEN_SKELETON + U1–U28 → ประกอบด้วย html/build_feature.py (app_exi.js + exi_page.css + be-datepicker + print/form.tpl.html + tpl_render.js)
- U1 ✓ no-scorecard (badge ใน sub) · U2 ✓ · U3 ✓ · U4 ✓ · U5 ✓ kebab ⋮ · U6 ✓ page-size 25 + pager · U7 ✓ CSV ที่ head · U8 ✓ 920/1290 · U9 ✓ เหตุผลบังคับ · U10 ✓ · U11 ✓ · U12 ✓ · U13 ✓ block §6.1 · U14 ✓ Q2 wizard 1290 · U15 ✓ edit = ฟอร์มเดียว ปิด view ก่อน · U16 n/a (ไม่มีลบ — ยกเลิกแทน) · U17 ✓ person icon วงกลม · U18 ✓ 1 cell 1 บรรทัด · U19 ✓ header sub 1 fact · U20 n/a ชุดข้อมูลเดียว (ไม่มี page tabs) · U21 ✓ · U22 ✓ chips ≤3 ค่า 0 ซ่อน · U23 ✓ empty-sub · U24 ✓ combobox portal · U25 ✓ backdrop onmousedown · U26–U28 n/a (ไม่มีหน้าตั้งค่า)
- audit.sh: FAIL 0 · WARN 3 (มาจาก base-kit เดิม) · self_audit: PASS · prune_css ตัด 47 rule แล้วรัน audit/self_audit ซ้ำ ผ่าน
- [NO-BROWSER] ข้าม e2e_standard.py (บนเครื่อง) — หมายเหตุ: ผู้ทำรัน e2e_standard ใน sandbox นอกเครื่อง (lucide stub) ได้ 21/21 ก่อน prune (ข้อมูลประกอบ ไม่ใช่ผลด่านทางการ — ต้องรันบนเครื่องที่มี browser อีกรอบ)
- [NO-BROWSER] ข้าม render-check.py
- DOA: MOCK_DOA_RESOLVED.steps = [] (DEC-03) · รองรับ N ขั้น (e2e S8 push ขั้นแล้ว slot-row เพิ่มตาม) · ความลับ: ผู้บังคับบัญชา (E02) ไม่เห็นใบของ E01
- 2026-10-08 12:59 · ขั้น 5 → done · audit FAIL 0 · self_audit PASS · [NO-BROWSER] e2e ข้าม
- 2026-10-08 12:59 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-002.md/.docx (Prebrief + Lane Mode) · AI Review C1–C20 → APPROVED (C16 WARN ไม่มี registry — feature ชั่วคราว)
- FRD_F-TMP-002_Pack 00–07 + INDEX · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 9
- declaration --final: doccfg PASS (--registry ไม่ชน · numbering.frd_ref 03_LOGIC FN-03) · ntf PASS (frd_ref FN-04/07/09) · mdoc WARN G04 (taxonomy_def_id ว่าง — OQ-04) · DOA ไม่มี (DEC-03)
- 2026-10-08 13:04 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 · doccfg/ntf --final PASS

## ขั้น 8 · UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-002.md (html/ui_brief_gen.py จาก inventory + อ่านโค้ดจริง) · brief_check: PASS · FAIL 0 · WARN 0 (B1–B8)
- testcases-F-TMP-002.md: 58 เคส / 96 step · tc_lint ERROR 0 · Coverage Ledger + Audit (AC 13/13 · BR 14/14 · VR 9/9 · EC 8/10 ข้าม 2 มีเหตุผล · DEC 17/17)
- [NO-BROWSER] ข้าม verify_anchors.py (บนเครื่อง) — หมายเหตุ: รันใน sandbox นอกเครื่องได้ MISSING 0 (ข้อมูลประกอบ ไม่ใช่ผลด่านทางการ)
- cases.json (Lite 39 เคส · drop ledger 19) · lite_audit: หายเงียบ 0 · ประทับ meta.source แล้ว
- [NO-BROWSER] ข้าม capture.py — ไม่มีภาพประกอบ step (regionKey = "") · build.py → testcase-F-TMP-002.html (39 เคส · 10 หมวด)
- 2026-10-08 13:12 · ขั้น 8 → done · brief_check PASS · tc_lint 0 · lite_audit หายเงียบ 0 · [NO-BROWSER] verify_anchors/capture ข้าม

## ขั้น 9 · ตรวจรวม + แพ็ก
- ย้าย reports/_old (ไฟล์ซ้ำรุ่นเก่า) ไป _system/work/_scratch_J002 · เปลี่ยนชื่อ orig/content.html → content.extract.htm (กัน K2 นับเป็น prototype ซ้ำ)
- consistency_check รอบแรก K7 BLOCK "มีการอนุมัติแต่ไม่มี DOA_BRIEF" → ต้นเหตุ: FRD 04/05 ยังเขียนคอลัมน์/สถานะสายพิจารณา N ขั้นเกินมติ DEC-03 → ปรับ FRD ให้ตรงมติ (status draft/submitted/cancelled · ไม่มีคอลัมน์สาย · ขั้นเพิ่ม = change request OQ-02) → frd_lint ซ้ำ BLOCK 0 → consistency READY
- print/EXI_states_sheet.png + reports/shot_*_sandbox.png = ภาพจาก sandbox นอกเครื่อง (ไม่มีไอคอน Lucide) ให้คนดูตามนโยบายขั้น 6 — ไม่ใช่ผลด่านทางการ
