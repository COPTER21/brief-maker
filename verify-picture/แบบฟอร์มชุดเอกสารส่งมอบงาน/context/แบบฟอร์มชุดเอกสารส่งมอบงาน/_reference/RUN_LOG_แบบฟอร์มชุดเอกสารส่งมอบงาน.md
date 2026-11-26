# RUN_LOG — F-TMP-008 FM-IVM-06 แบบฟอร์มชุดเอกสารส่งมอบงาน (REQ-TMP-008)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: to_image.py (LibreOffice → PDF → pypdfium2) ได้ page-1.png + content.html · ถ้อยคำยึด openpyxl/content.html · ตำแหน่ง/เส้นยึดภาพ (ภาพฟอนต์ไทยไม่ขึ้น แต่โครงตาราง/เส้นชัด)
- FORM_SPEC: 18 ช่อง · แถวซ้ำ 1 (ผลการตรวจรับเอกสาร 12 แถว) · ตัวเลือก 3 (data validation E18 · E22:E33 · F22:F33) · สูตร 0 · ค่าคงที่ 0 · ลายเซ็น 3 · anomalies 7 · form_spec_check ERROR 0 (รอบแรก ERROR 1: F06 ไม่อยู่ใน block → เพิ่ม row B16)
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC (--req REQ-TMP-008 --module investment) · impact_summary ฉบับร่าง
- ไฟล์ลูกค้าเป็นฟอร์มเปล่า ไม่มีข้อมูลตัวอย่าง/ข้อมูลส่วนบุคคล · ช่องชื่อคน (F02 F03 F13) ติด pdpa
- ชื่อฟอร์มจากหัวฟอร์ม = "แบบฟอร์มชุดเอกสารส่งมอบงาน" (C1 มีเว้นวรรคท้าย ตัดออก)
- 2026-10-11 01:27 · ขั้น 1 → done · FORM_SPEC 18 ช่อง ERROR 0 · PREBRIEF v2

## ขั้น 2 — มติ AI (unattended · ตาม 4_knowledge/governance/unattended-policy.md)
- G1: บันทึกรับมอบชุดเอกสาร ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อ · ชื่อโครงการกรอกเอง (FM-IVM-01/05 ยังไม่ลิงก์)
- G2: dynamic 2 ขั้นตามช่องลงชื่อ: ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน → role-line-manager) · ผู้อนุมัติ/รับทราบ (ฝ่ายพัฒนาธุรกิจรับทราบผลการรับมอบ → role-mgr-bu หัวหน้าหน่วยธุรกิจ ใกล้สุดใน contract) · ไม่มีวงเงิน · ⚠ role บนกระดาษไม่มีใน doa-roles-contract
- G3: ไม่มีค่าคงที่/สูตร · กฎขัดกันชัดเจนบล็อก (ไม่ได้รับ→ไม่ครบถ้วน · แถวไม่ครบต้องมีประเด็น/ผู้รับผิดชอบ/กำหนดส่ง · ผลการรับมอบต้องสอดคล้องตาราง · กำหนดส่ง ≥ วันที่รับมอบ) · คำแนะนำผลการรับมอบ = เตือน
- G4: ไม่จำกัดแถว · PDF ขั้นต่ำ 12 · G5: 1:1 ไม่เพิ่มช่อง · G6: แถวล่างต่อขั้น ข้อความในระบบ
- G7: ส่งกลับ → ร่างเลขเดิม · ยกเลิก owner+admin ร่าง/รออนุมัติ เหตุผลบังคับ · G8: เจ้าของ/ผู้อนุมัติหลังส่ง/admin ฝ่ายเห็นทั้งหมด
- G9: เอกสารภายใน ออกเลขตอนบันทึกครั้งแรก · รหัส IVMF (IVM + F = ฟอร์มลำดับ 06)
- G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock = พร้อมเริ่มทำ · 18 มติ (AI-DEFAULT 11 · VALID 7)
- 2026-10-11 01:28 · ขั้น 2 → done · DECISIONS.lock พร้อม · 18 มติ AI-DEFAULT 11

## ขั้น 3 — หมายเหตุ
- DOA: doa_tool init เขียน on_reject: draft → แก้เป็น back_to_draft (ตรง DEC-08) · คำตัดสินขั้น 2 = รับทราบ/ส่งกลับ · role_notes · TODO: DOA engine · validate PASS · mock → IVMF.doa.mock.js
- ⚠ role บนกระดาษไม่มีใน doa-roles-contract: "ผู้จัดการฝ่ายบริหารการลงทุน" (ใช้ role-line-manager) · "ฝ่ายพัฒนาธุรกิจรับทราบผลการรับมอบ" (ใช้ role-mgr-bu รอยืนยัน) · module investment ไม่อยู่ใน Module Registry
- NTF: ตัด ivmf_over_limit_approved (ไม่มีเกณฑ์ตัวเลข) · เพิ่ม ivmf_handover_followup (อนุมัติแล้วแต่รับมอบแบบมีเงื่อนไข/ยังไม่รับมอบ → แจ้งผู้จัดทำ + admin role ติดตามเอกสารค้าง) · PASS
- 2026-10-11 01:29 · ขั้น 3 → done · DOA PASS (2 ขั้น dynamic) · NTF PASS (2 event) · doccfg/mdoc หลังขั้น 4

## ขั้น 4 — หมายเหตุ
- ทำต่อจาก agent ก่อนหน้า: print/ ว่าง (ยังไม่เริ่ม) → ทำใหม่ทั้งหมด · ยึดโครงพี่น้อง J005 (FM-IVM-03)
- แบบพิมพ์: R9 ตารางกรอบ 8 คอลัมน์ · ต้นฉบับ 1 หน้า แต่ 5 หมวด + DOA 6 ขั้น (7 แถวลงชื่อ) + รายการยาว เกิน A4 ที่ ≥ 8pt → ออกแบบ 2 หน้าตาม R10 (ตัดหน้าก่อน "ประเด็นค้างและข้อตกลงการติดตาม" · หัวย่อหน้า 2 · thead ซ้ำ · มีต่อหน้าถัดไป · หน้า 1/2, 2/2) · ฟอนต์ 8.5pt
- ช่องลงชื่อ sign_rows.py (ผู้จัดทำ + 1 แถว/ขั้น DOA) · decision_words by_role: role-line-manager ตรวจสอบแล้ว/ส่งกลับ · role-mgr-bu รับทราบ/ส่งกลับ
- data 5 สถานะ (draft · approved · rejected · long-16rows · approved-doa6steps) ข้อมูลสมมติทั้งหมด · parity IDENTICAL 5/5 · render_doc --strict + build_html ไม่มี {{}} หลง
- DOCCFG IVMF PASS (--registry ไม่ชน) · MDOC WARN (G04 taxonomy รออนุมัติ · G09 doa pending) · doa validate --print-config PASS (BLOCK 0)
- [NO-BROWSER] ข้าม render_states.py (เรียก render_pdf.py) — ยังไม่ได้ PDF/จำนวนหน้า/_states_sheet.png
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ PDF สถานะ approved)
- 2026-10-11 07:36 · ขั้น 4 → done · Replica 2 หน้า R10 · parity 5/5 · NO-BROWSER: ยังไม่ render PDF/compare

## ขั้น 5 — HTML Q-form
- ฐาน: references/form-archetype/_SOURCE_form-request-reference.html (เปลือก/CSS/BASE-KIT) + app script ของ IVMF (_build/app1–5.js · build_feature.py · ดัดจากโครง J005) + be-datepicker (Rule #114) · DOC_TPL = print/form.tpl.html · tpl_render.js วางตรง
- เทียบ GOLDEN_SKELETON v9.4 + U1–U28 ก่อน build: ไม่มี stat cards (ตัวเลขเป็น badge ใน ph-sub) · kebab ⋮ · คน = วงกลม icon (ผู้จัดทำ/ผู้ส่งมอบ/ผู้รับมอบ) · pagination 25 + page-size · backdrop onmousedown · drawer header lean (sub = ผลการรับมอบ · เอกสารครบ x/y) · ไม่มี page tabs (ชุดเดียว)
- แถวซ้ำ 8 คอลัมน์ → ตารางกรอก (Rule #107) · กำหนดส่ง = bedateHTML ต่อแถว · ได้รับแล้ว/ความครบถ้วน/ผลการรับมอบ = select ตาม data validation · ไม่ได้รับ → ไม่ครบถ้วนอัตโนมัติ + option ครบถ้วน disabled · ลำดับระบบรัน · ไม่มีทำซ้ำ (DEC-11)
- U1✓ U2✓ U3✓ U4✓ U5✓ U6✓ U7✓ U8✓ U9✓ U10✓ U11✓ U12✓ U13✓ U14✓(wizard wide 3 ขั้น) U15✓ U16 n/a(ไม่มีลบ ใช้ยกเลิก) U17✓ U18✓ U19✓ U20 n/a(ชุดเดียว) U21✓ U22✓ U23✓ U24✓ U25✓ U26–U28 n/a(ไม่มีหน้าตั้งค่า)
- กันบั๊ก modal อนุมัติ/ส่งกลับพังตอนกำลังปิด: render() วาด modal เฉพาะ state.modal.open + guard curStep ใน renderModal
- audit.sh FAIL 0 · WARN 3 (เท่ากับ canonical: Rule #21 ใน BASE-KIT · .uc-email ใน kit · token font-size) · self_audit PASS (แก้ hint ยาว 1) · prune_css ตัด 72 rule แล้ว audit/self_audit ซ้ำผ่าน · node --check ผ่าน
- smoke test แบบไม่มี browser (jsdom · timer จริง · _build/smoke.js): 53/53 — U1/U5/U6 · สิทธิ์ (owner/approver/admin) · view ทุกใบ × 4 แท็บ × 3 persona ไม่มี error · validate (ช่องหลัก/เวลา HH:mm · ไม่ได้รับ→ไม่ครบถ้วน · แถวไม่ครบต้องมีประเด็น/ผู้รับผิดชอบ/กำหนดส่ง · ครบถ้วนแต่มีแถวค้าง บล็อก · กำหนดส่งก่อนวันรับมอบ บล็อก · มีเงื่อนไขต้องมีประเด็นค้าง+กำหนดติดตาม · ยังไม่รับมอบต้องมีหมายเหตุ · ไม่ตรงคำแนะนำ = เตือน · ไม่มีแถว บล็อก) · ออกเลข IVMF-2569-0012 · ส่ง/ส่งกลับเป็นร่างเลขเดิม/ส่งใหม่/อนุมัติ 2 ขั้น modal ปิดไม่พัง · API ล้ม · ยกเลิก · PDF เติมแถว 12 · คำตัดสินตาม role · DOA 6 ขั้น = 7 ช่อง · CSV · DOC.active=false · ไม่มี JS error
- parity PDF ใน prototype: docPrintData(R1) → render_doc.py (Python) = tplRender (JS) IDENTICAL
- [NO-BROWSER] ข้าม e2e_standard.py · [NO-BROWSER] ข้าม render-check.py
- 2026-10-11 07:44 · ขั้น 5 → done · audit FAIL0 · self_audit PASS · smoke 53/53 · NO-BROWSER ข้าม e2e
- 2026-10-11 07:44 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-008.md (+ .docx md_to_docx) · brd-generator-full v2.3 Prebrief Mode · Quality Gate C1–C20 → APPROVED · §2.4 = DECISIONS.lock 18 DEC · OQ-01..08
- FRD_F-TMP-008_Pack 00–07 + INDEX (Input Mode 0 · FULL) · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 12
- declaration --final: DOCCFG IVMF PASS (--registry · frd_ref FN-04/FN-06) · NTF PASS (frd_ref FN-06/08/10 · 2 event) · DOA PASS (+print_config +html) · MDOC WARN (G04 taxonomy รอ · G09 doa pending) → สำเนาใน FRD_Pack/declarations
- 2026-10-11 07:50 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK0 WARN0 · decl final PASS

## ขั้น 8 — UI Brief → test case → UAT
- UI_BRIEF_F-TMP-008.md (AS-BUILT จาก inventory · _build/build_uibrief.py) · brief_check PASS · FAIL 0 · WARN 0
- testcases-F-TMP-008.md 42 เคส / 233 step · tc_lint ERROR 0 · cases.json (Lite 37 เคส) + QA_AUDIT drop ledger 5 · lite_audit หายเงียบ 0 (--stamp) · testcase-F-TMP-008.html (build.py · shots ว่าง)
- เคส TC-A01/A02/R01 ตรวจ "modal ปิดเรียบร้อย" (บั๊กใบก่อน)
- [NO-BROWSER] ข้าม verify_anchors.py · [NO-BROWSER] ข้าม capture.py (เอกสาร UAT build แบบไม่มีภาพ)
- ตรวจ anchor แบบ static แทน: 138 anchor · ตรงตัวใน feature.html 99 · ที่เหลือ 39 = ข้อความประกอบ/ตัวเลขที่สร้างตอนรัน · สุ่มยืนยันใน jsdom 13/13 ok · ต้องรัน verify_anchors.py บนเครื่องที่มี browser
- 2026-10-11 07:54 · ขั้น 8 → done · brief_check PASS · tc_lint 0 · lite_audit 0 · NO-BROWSER: ข้าม verify_anchors/capture
