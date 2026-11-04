# RUN_LOG — F-TMP-004 ใบกำหนดหน้าที่งานประจำตำแหน่ง (JD) (REQ-TMP-004)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพฟอร์ม: to_image.py วิธี LibreOffice → PDF → pypdfium2 (2 หน้า) = หน้ากระดาษจริงจาก docx (ฟอนต์ไทยในเครื่องไม่มี ภาพแสดงกล่องแทนอักษร) → ถ้อยคำยึด content.html · ตำแหน่ง/เส้นยึดภาพ · Doc No./Rev. อ่านจาก footer1.xml
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC ล้วน
- form_spec_check: ERROR 0 (รอบแรก ERROR 1 ช่องลายเซ็นไม่อยู่ใน block → เพิ่ม row ใต้ sign) · WARN 0 · 20 ช่อง · แถวซ้ำ 2 (หัวหน้า/ลูกน้อง 3 แถว) · ตัวเลือก 0 · ลายเซ็น 3 (ผู้จัดทำ · ผู้อนุมัติ · ผู้ดำรงตำแหน่งรับทราบ)
- ฟอร์มว่าง ไม่มีข้อมูลส่วนบุคคลตัวอย่าง · ชื่อเอกสารไม่เพี้ยน (ไม่ต้อง rename) · หัวฟอร์ม "ใบกำหนดหน้าที่งานประจำตำแหน่ง (Job Description)" FM-HRM-32 Rev. 00 : 01/07/2569
- feature ที่ใกล้: Organization · Position & Tier / HR · Organization (HR) (FEATURE_REGISTRY ยังไม่มีรหัส) → ใช้ F-TMP-004 ชั่วคราว
- 2026-10-08 13:17 · ขั้น 1 → done · FORM_SPEC ERROR 0 · PREBRIEF v2 จาก FORM_SPEC

## ขั้น 2 · gate (unattended — AI-DEFAULT)
- G1: ไม่เปลี่ยน config/ไม่ส่งต่อ — JD เก็บในเอกสารนี้ ไม่แก้ Position master (F-ORG Position & Tier)
- G2: ช่อง "ผู้อนุมัติ (Approved By)" 1 ช่อง ไม่ระบุตำแหน่ง → dynamic 1 ขั้น role-line-manager (relative role — ยังไม่อยู่ใน DOA master 14 role → แจ้งในรายงาน) · ไม่มีวงเงิน
- G3: ดึงชื่อตำแหน่ง/แผนก/ฝ่าย/รายงานต่อจาก Position master · ผู้ใต้บังคับบัญชาส่วนที่ 1 คำนวณจากตาราง · ตารางหัวหน้า ≥1 แถว · จำนวนคนจำนวนเต็ม ≥1 · ฉบับอนุมัติใหม่แทนฉบับเดิมของตำแหน่งเดียวกัน · ผู้ดำรงตำแหน่งรับทราบหลังอนุมัติ (ไม่บังคับ)
- G4: ไม่จำกัดแถว PDF ≥3 · G5: 1:1 · G6: แถวล่างต่อขั้น DOA · G7: ไม่อนุมัติ → กลับร่าง · ยกเลิก เจ้าของ+HR ร่าง/รออนุมัติ ระบุเหตุผล
- G8: เจ้าของ · ผู้อนุมัติหลังส่ง · HR (role-mgr-hr) ทั้งหมด · ผู้ดำรงตำแหน่งเห็นเฉพาะใบอนุมัติแล้วของตน · G9: JD ออกเลขบันทึกครั้งแรก · G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock พร้อมเริ่มทำ (17 มติ · AI-DEFAULT 12 · VALID 5) · dm.sh tag แล้ว
- 2026-10-08 13:18 · ขั้น 2 → done · 17 มติ · AI-DEFAULT 12

## ขั้น 3 · declaration ร่าง
- doa: init → validate BLOCK G5 "on_reject ต้องเป็น back_to_draft หรือ end" (init แปลง G7 on_reject: draft ตรงตัว) → แก้ yaml เป็น back_to_draft → PASS · 1 ขั้น role-line-manager (INFO G1 relative role — ยืนยันกับ DOA กลาง) · validate --print-config PASS (G8 doa_step:* · G9)
- ntf: jd_cancelled · jd_ack_requested (→ ผู้ดำรงตำแหน่ง) · jd_acknowledged · jd_superseded · ตัด jd_over_limit_approved (ไม่มีเกณฑ์ตัวเลข) · VERDICT PASS
- doccfg (หลังขั้น 4): JD · {PREFIX}-{YYYY}-{run:4} · first_save · snapshot approved_final · --registry ไม่ชน · VERDICT PASS
- mdoc: JD · FRM · function_code F01 ชั่วคราว · source=declaration (REQ-TMP-004 ไม่ใช่รูปแบบ REQ-YYYY-NNNN) · doa pending · VERDICT WARN (G04 taxonomy_def_id ว่าง · G09 doa pending)

## ขั้น 4 · แบบพิมพ์ Replica
- form.tpl.html สร้างจาก print/make_print.py (ถ้อยคำในเทมเพลตตาม content.html) · R9 ตาราง (ส่วน 1 + ตารางหัวหน้า/ลูกน้อง) + R4 บรรทัดเส้นประ (ส่วน 2–6 · data เติมบรรทัดครบตามกระดาษ 4/8/4/4/4) + B6 sign_rows แบบตาราง (ผู้จัดทำ + DOA N ขั้น + ผู้ดำรงตำแหน่ง) + B7
- data 5 สถานะ (สมมติทั้งหมด): draft · approved · rejected · long-12rows · approved-doa6steps (8 ช่อง 4+4)
- parity_check: IDENTICAL 5/5 · render_doc --strict ไม่มี {{}} หลง · build_html ทุกสถานะ → print/out/*.html + JD_template.html
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py ล้มที่ launch browser) — ทำ HTML ต่อสถานะด้วย render_doc.py + build_html.py แทน · ไฟล์ body กลางย้ายไป _system/work/_scratch_J004
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ PDF ที่ render จาก browser)
- หมายเหตุ QA: ผู้ทำตรวจด้วยตาจาก Chromium นอกเครื่อง (ข้อมูลสมมติ ไม่ใช่ไฟล์ลูกค้า) — approved/doa6/long = 2 หน้าเท่ากระดาษ · ลำดับตรงกระดาษ (ไม่ใช่ผลด่านทางการ)
- 2026-10-08 13:23 · ขั้น 4 → done · parity 5/5 · [NO-BROWSER] ไม่มี PDF/compare
- 2026-10-08 13:23 · ขั้น 3 → done · DOA PASS 1 ขั้น · ntf PASS · doccfg PASS · mdoc WARN G04/G09

## ขั้น 5 · HTML Q-form
- ฐาน: html-generator-v9 references/form-archetype/_SOURCE (Q2) + เทียบ GOLDEN_SKELETON + U1–U28 → ประกอบด้วย html/build_feature.py (app_jd.js + jd_page.css + be-datepicker + print/form.tpl.html + tpl_render.js) · โครง generic ตาม J002 (ผ่าน v9.4 แล้ว) + flow DOA ของ OSW
- domain: เลือกตำแหน่งจาก Position master → ดึงแผนก/ฝ่าย/รายงานต่อ · หัวข้อ 2–6 (textarea) · ตารางหัวหน้า/ลูกน้อง (การ์ดต่อแถว · จำนวนคน inputmode numeric) · ผู้ใต้บังคับบัญชาคำนวณสด · เตือนหัวหน้าแถวแรกไม่ตรงรายงานต่อ (ไม่บล็อก) · ผู้ดำรงตำแหน่ง → รับทราบหลังอนุมัติ · HR ระบุ/เปลี่ยนผู้ดำรงตำแหน่ง · อนุมัติขั้นสุดท้ายแล้วฉบับเดิมของตำแหน่งเดียวกัน → ถูกแทนที่
- U1 ✓ no-scorecard (badge ใน sub) · U2 ✓ · U3 ✓ · U4 ✓ · U5 ✓ kebab ⋮ · U6 ✓ page-size 25 + pager · U7 ✓ CSV ที่ head · U8 ✓ 920/1290 · U9 ✓ เหตุผลบังคับ · U10 ✓ · U11 ✓ · U12 ✓ · U13 ✓ block §6.1 · U14 ✓ Q2 wizard 1290 · U15 ✓ edit = ฟอร์มเดียว ปิด view ก่อน · U16 n/a (ไม่มีลบ — ยกเลิกแทน) · U17 ✓ person icon วงกลม · U18 ✓ · U19 ✓ header sub = ชื่อตำแหน่ง 1 fact · U20 n/a ชุดข้อมูลเดียว · U21 ✓ · U22 ✓ badge ≤3 ค่า 0 ซ่อน · U23 ✓ empty-sub · U24 ✓ combobox portal · U25 ✓ backdrop onmousedown · U26–U28 n/a
- audit.sh: FAIL 0 · WARN 3 (มาจาก base-kit เดิม) · self_audit: รอบแรก FAIL (naked_hints 3 · missing_ids 'sec-') → ย่อ hint ≤60 + querySelector → PASS · prune_css ตัด 64 rule แล้วรัน audit/self_audit ซ้ำ ผ่าน
- [NO-BROWSER] ข้าม e2e_standard.py (บนเครื่อง) — หมายเหตุ: ผู้ทำรัน e2e_standard ใน sandbox นอกเครื่อง (ไม่มี lucide) ได้ 21/21 หลัง prune + flow สร้าง→ส่ง→อนุมัติ→ระบุผู้ดำรงตำแหน่ง→รับทราบ→ฉบับเดิมถูกแทนที่ · ไม่อนุมัติ→กลับร่าง ไม่มี pageerror (ข้อมูลประกอบ ไม่ใช่ผลด่านทางการ)
- [NO-BROWSER] ข้าม render-check.py
- DOA: MOCK_DOA_RESOLVED 1 ขั้น role-line-manager (DOA-ENGINE-HOOK + TODO: DOA engine) · รองรับ N ขั้น (e2e S8) · field approver_role/approved_by/approval_chain อยู่ใน FRD
- ภาพประกอบ (sandbox · ไม่ใช่ผลด่านทางการ): print/JD_states_sheet.png (5 สถานะ × 2 หน้า — ตารางหัวหน้า/ลูกน้องอาจขึ้นหน้า 2 แยกจากหัวตารางเมื่อเนื้อหาสั้น: replica ห้าม style ใน body → ให้คนดู) · reports/shot_*_sandbox.png
- 2026-10-08 13:38 · ขั้น 5 → done · audit FAIL 0 · self_audit PASS · [NO-BROWSER] e2e ข้าม
- 2026-10-08 13:38 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-004.md/.docx (Prebrief + Lane Mode · md_to_docx.py) · AI Review C1–C20 + PE02 SoD → APPROVED (C16 WARN ไม่มี registry — feature ชั่วคราว)
- FRD_F-TMP-004_Pack 00–07 + INDEX + declarations/ · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 14
- declaration --final: doccfg PASS (--registry ไม่ชน · numbering.frd_ref 03_LOGIC FN-03 · snapshot FN-05) · ntf PASS (frd_ref FN-07/09/10/11) · doa PASS (--print-config) · mdoc WARN (G04 taxonomy_def_id ว่าง — OQ-04 · G09 doa pending รอ wire)
- 2026-10-08 13:43 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 · doccfg/ntf --final PASS

## ขั้น 8 · UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-004.md (html/ui_brief_gen.py จาก inventory + อ่านโค้ดจริง) · brief_check: PASS · FAIL 0 · WARN 0 (B1–B8)
- testcases-F-TMP-004.md: 54 เคส / 94 step · tc_lint ERROR 0 · Coverage Ledger + Audit (AC 15/15 · BR 16/16 · VR 9/9 · EC 8/10 ข้าม 2 มีเหตุผล · DEC 17/17)
- [NO-BROWSER] ข้าม verify_anchors.py (บนเครื่อง) — หมายเหตุ: รันใน sandbox นอกเครื่อง รอบแรก MISSING 6 (ปุ่ม "เพิ่มลูกน้อง"/ข้อความ error/ toast ประกอบจาก template) → แก้ app_jd.js ให้เป็นข้อความคงที่ + ปรับ expected → MISSING 0 (ข้อมูลประกอบ ไม่ใช่ผลด่านทางการ) · rebuild feature.html แล้วรัน audit FAIL 0 / self_audit PASS / brief_check PASS / e2e sandbox 21/21 ซ้ำ
- cases.json (Lite 45 เคส · drop ledger 9) · lite_audit: หายเงียบ 0 · ประทับ meta.source แล้ว
- [NO-BROWSER] ข้าม capture.py — ไม่มีภาพประกอบ step (regionKey = "") · build.py → testcase-F-TMP-004.html (45 เคส · 11 หมวด)
- 2026-10-08 13:51 · ขั้น 8 → done · brief_check PASS · tc_lint 0 · lite_audit หายเงียบ 0 · [NO-BROWSER] verify_anchors/capture ข้าม
