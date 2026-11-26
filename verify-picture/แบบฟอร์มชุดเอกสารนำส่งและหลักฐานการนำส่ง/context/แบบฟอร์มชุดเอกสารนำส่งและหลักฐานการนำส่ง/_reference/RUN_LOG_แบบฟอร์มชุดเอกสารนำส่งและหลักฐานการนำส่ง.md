# RUN_LOG — F-TMP-009 FM-IVM-07 แบบฟอร์มชุดเอกสารนำส่งและหลักฐานการนำส่ง (REQ-TMP-009)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: to_image.py (LibreOffice → PDF → pypdfium2) ได้ page-1.png + content.html · ถ้อยคำยึด openpyxl/content.html · ตำแหน่ง/เส้นยึดภาพ (ภาพฟอนต์ไทยไม่ขึ้น แต่โครงตาราง/เส้นชัด)
- FORM_SPEC: 23 ช่อง (ระบบ 3 · กรอก 18 · ระบบใส่ 2) · แถวซ้ำ 2 (รายการตรวจสอบชุดเอกสาร 10 แถว · หลักฐานการนำส่งเอกสาร 15 แถว) · ตัวเลือก 4 (data validation D22:D31 · E22:E31 · F35:F49 · J35:J49) · สูตร 0 · ค่าคงที่ 0 · ลายเซ็น 3 · anomalies 9 · form_spec_check ERROR 0
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC (--req REQ-TMP-009 --module investment) · impact_summary ฉบับร่าง
- ไฟล์ลูกค้าเป็นฟอร์มเปล่า ไม่มีข้อมูลตัวอย่าง/ข้อมูลส่วนบุคคล · ช่องชื่อคน (F05–F07 F16 F17) ติด pdpa
- ชื่อฟอร์มจากหัวฟอร์ม (C1) = "แบบฟอร์มชุดเอกสารนำส่งและหลักฐานการนำส่ง" · ชื่อในคิวมี FM-IVM-07 นำหน้า → dm.sh rename
- หัวฟอร์ม/ชื่อชีตเป็น INV-FM-07 แต่ footer Doc. No. = FM-IVM-07 → ยึด FM-IVM-07
- 2026-10-11 07:57 · ขั้น 1 → done · FORM_SPEC 23 ช่อง ERROR 0 · PREBRIEF v2

## ขั้น 2 — มติ AI (unattended · ตาม 4_knowledge/governance/unattended-policy.md)
- G1: บันทึกจัดชุด/หลักฐานการนำส่ง ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อ · ระบบไม่ส่งเอกสารออกเอง · ชื่อโครงการกรอกเอง (FM-IVM-01 ยังไม่ลิงก์)
- G2: dynamic 2 ขั้นตามช่องลงชื่อ: ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน → role-line-manager) · ผู้อนุมัติ/รับทราบ (รอง กก.ผจก./กก.ผจก. → role-gm) · ไม่มีวงเงิน · ⚠ ตำแหน่งบนกระดาษไม่มีใน doa-roles-contract (ใช้ role แทนตามคำสั่งชุดนี้)
- G3: ไม่มีค่าคงที่/สูตร · ขัดกันชัดเจนบล็อก (ขาดเอกสาร/มีข้อจำกัด ต้องมีหมายเหตุ · รับแล้วต้องมีหลักฐาน · อื่น ๆ/ส่งไม่สำเร็จ/ยกเลิก ต้องมีหมายเหตุ · เวลาอนาคตบล็อก · ปิดการนำส่งต้องรับแล้ว ≥1 และไม่มีรอยืนยัน) · ขาดเอกสาร/ส่งก่อนวันที่นำส่ง = เตือน · ลำดับงาน อนุมัติชุดก่อน → บันทึกหลักฐานหลังอนุมัติไม่ต้องอนุมัติซ้ำ → ปิดการนำส่ง
- G4: ไม่จำกัดแถว · PDF ขั้นต่ำ 10/15 · G5: 1:1 ไม่เพิ่มช่อง (คง ผู้ตรวจทาน/ผู้ตรวจสอบ ตามกระดาษ) · G6: แถวล่างต่อขั้น ข้อความในระบบ
- G7: ส่งกลับ → ร่างเลขเดิม · ยกเลิก owner+admin ร่าง/รออนุมัติ เหตุผลบังคับ · G8: เจ้าของ/ผู้อนุมัติหลังส่ง/admin ฝ่ายเห็นทั้งหมด
- G9: เอกสารภายใน ออกเลขตอนบันทึกครั้งแรก · รหัส IVMG (IVM + G = ฟอร์มลำดับ 07)
- G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock = พร้อมเริ่มทำ · 21 มติ (AI-DEFAULT 12 · VALID 9)
- 2026-10-11 07:58 · ขั้น 2 → done · DECISIONS.lock พร้อม · 21 มติ AI-DEFAULT 12

## ขั้น 3 — หมายเหตุ
- DOA: doa_tool init เขียน on_reject: draft → แก้เป็น back_to_draft (ตรง DEC-09) · คำตัดสิน ขั้น 1 ตรวจสอบแล้ว/ส่งกลับ · ขั้น 2 อนุมัติ/ส่งกลับ · role_notes · TODO: DOA engine · validate PASS · mock → IVMG.doa.mock.js
- ⚠ ตำแหน่งบนกระดาษไม่มีใน doa-roles-contract: "ผู้จัดการฝ่ายบริหารการลงทุน" (ใช้ role-line-manager) · "รองกรรมการผู้จัดการ / กรรมการผู้จัดการ / ผู้มีอำนาจตามตารางอำนาจอนุมัติ" (ใช้ role-gm รอยืนยัน) · module investment ไม่อยู่ใน Module Registry
- NTF: ตัด ivmg_over_limit_approved (ไม่มีเกณฑ์ตัวเลข) · เพิ่ม ivmg_delivery_failed (แถวหลักฐาน ส่งไม่สำเร็จ → ผู้จัดทำ + admin role) · ivmg_dispatch_closed (ปิดการนำส่ง → สายอนุมัติ + admin role) · PASS
- 2026-10-11 07:58 · ขั้น 3 → done · DOA PASS (2 ขั้น dynamic) · NTF PASS (3 event) · doccfg/mdoc หลังขั้น 4

## ขั้น 4 — หมายเหตุ
- แบบพิมพ์: R9 ตารางกรอบ 10 คอลัมน์ (A–J) · ต้นฉบับ 1 หน้า แต่ ข้อมูลการนำส่ง 7 แถว + รายการตรวจสอบ 10 แถว + หลักฐาน 15 แถว 10 คอลัมน์ + DOA 6 ขั้น (7 แถวลงชื่อ) เกิน A4 ที่ ≥ 8pt → ออกแบบ 2 หน้าตาม R10 (ตัดหน้าก่อน "หลักฐานการนำส่งเอกสาร" · หัวย่อหน้า 2 · thead ซ้ำทั้งสองตาราง · มีต่อหน้าถัดไป · หน้า 1/2, 2/2) · ฟอนต์ 8.5pt
- ช่องลงชื่อ sign_rows.py (ผู้จัดทำ + 1 แถว/ขั้น DOA) · decision_words by_role: role-line-manager ตรวจสอบแล้ว/ส่งกลับ · role-gm อนุมัติ/ส่งกลับ
- data 5 สถานะ (draft · approved · rejected · long-16rows · approved-doa6steps) ข้อมูลสมมติทั้งหมด · parity IDENTICAL 5/5 · render_doc --strict + build_html ไม่มี {{}} หลง
- DOCCFG IVMG PASS (--registry ไม่ชน) · MDOC WARN (G04 taxonomy รออนุมัติ · G09 doa pending) · doa validate --print-config PASS (BLOCK 0)
- [NO-BROWSER] ข้าม render_states.py (เรียก render_pdf.py) — ยังไม่ได้ PDF/จำนวนหน้า/_states_sheet.png
- [NO-BROWSER] ข้าม render_pdf.py · [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ PDF สถานะ approved)
- 2026-10-11 08:01 · ขั้น 4 → done · Replica 2 หน้า R10 · parity 5/5 · NO-BROWSER: ยังไม่ render PDF/compare

## ขั้น 5 — HTML Q-form
- ฐาน: references/form-archetype/_SOURCE_form-request-reference.html (เปลือก/CSS/BASE-KIT) + app script ของ IVMG (_build/app1–5.js · build_feature.py · ดัดจากโครงพี่น้อง J008) + be-datepicker (Rule #114) · DOC_TPL = print/form.tpl.html · tpl_render.js วางตรง
- เทียบ GOLDEN_SKELETON v9.4 + U1–U28 ก่อน build: ไม่มี stat cards (ตัวเลขเป็น badge ใน ph-sub) · kebab ⋮ · คน = วงกลม icon (ผู้จัดทำ/ผู้ตรวจทาน/ผู้อนุมัติ/ผู้ส่ง) · pagination 25 + page-size · backdrop onmousedown · drawer header lean (sub = จำนวนเอกสาร · ขาด · รับแล้ว x/y) · ไม่มี page tabs (ชุดเดียว)
- รายการตรวจสอบ 6 คอลัมน์ → ตารางกรอกใน wizard (Rule #107) · หลักฐานการนำส่ง 10 คอลัมน์ → drawer "บันทึกหลักฐานการนำส่ง" หลังอนุมัติ (DEC-20 · ไม่ต้องอนุมัติซ้ำ · แนบไฟล์ต่อแถวได้) → modal "ปิดการนำส่ง" (รับแล้ว ≥1 · ไม่มีรอยืนยัน) · สถานะ ร่าง/รออนุมัติ/อนุมัติแล้ว·รอปิดการนำส่ง/ปิดการนำส่งแล้ว/ยกเลิก · ผู้ตรวจทาน/ผู้อนุมัติ = approval_chain · ไม่มีทำซ้ำ (DEC-12)
- U1✓ U2✓ U3✓ U4✓ U5✓ U6✓ U7✓ U8✓ U9✓ U10✓ U11✓ U12✓ U13✓ U14✓(wizard wide 3 ขั้น) U15✓ U16 n/a(ไม่มีลบ ใช้ยกเลิก) U17✓ U18✓ U19✓ U20 n/a(ชุดเดียว) U21✓ U22✓ U23✓ U24✓ U25✓ U26–U28 n/a(ไม่มีหน้าตั้งค่า)
- กันบั๊ก modal อนุมัติ/ส่งกลับพังตอนกำลังปิด: render() วาด modal เฉพาะ state.modal.open + guard curStep / status ใน renderModal (approve · reject · close)
- audit.sh FAIL 0 · WARN 3 (เท่ากับ canonical: Rule #21 ใน BASE-KIT · .uc-email ใน kit · token font-size) · self_audit PASS (แก้ hint ยาว 2) · prune_css ตัด 72 rule แล้ว audit/self_audit/smoke ซ้ำผ่าน · node --check ผ่าน
- smoke test แบบไม่มี browser (jsdom · timer จริง · _build/smoke.js): 64/64 — U1/U5/U6 · สิทธิ์ (owner/ผู้ตรวจสอบ/ผู้อนุมัติ/admin) · view ทุกใบ × 4 แท็บ × 4 persona ไม่มี error · validate (ช่องหลัก · แถวเอกสาร · ขาดเอกสาร/มีข้อจำกัด ต้องมีหมายเหตุ · ขาดเอกสาร = เตือน · ไม่มีแถว บล็อก) · ออกเลข IVMG-2569-0012 · ส่ง/ส่งกลับเป็นร่างเลขเดิม/ส่งใหม่/อนุมัติ 2 ขั้น modal ปิดไม่พัง · หลักฐาน (รับแล้วต้องมีหลักฐาน · อื่น ๆ/ส่งไม่สำเร็จต้องมีหมายเหตุ · เวลาอนาคตบล็อก · ก่อนวันที่นำส่งเตือน · แจ้ง ivmg_delivery_failed) · ปิดการนำส่ง (รอยืนยันบล็อก → ปิดได้ · modal ปิดไม่พัง) · API ล้ม · ยกเลิก · PDF เติมแถว 10/15 · ผู้ตรวจทาน/ผู้อนุมัติจาก chain · คำตัดสินตาม role · DOA 6 ขั้น = 7 ช่อง · CSV · DOC.active=false · ไม่มี JS error
- parity PDF ใน prototype: docPrintData(R3) → render_doc.py (Python) = tplRender (JS) IDENTICAL
- [NO-BROWSER] ข้าม e2e_standard.py · [NO-BROWSER] ข้าม render-check.py
- 2026-10-11 08:16 · ขั้น 5 → done · audit FAIL0 · self_audit PASS · smoke 64/64 · NO-BROWSER ข้าม e2e
- 2026-10-11 08:16 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-009.md (+ .docx md_to_docx) · brd-generator-full v2.3 Prebrief Mode · Quality Gate C1–C20 → APPROVED (C16 ไม่มี Registry = WARN) · §2.4 = DECISIONS.lock 21 DEC · OQ-01..10
- FRD_F-TMP-009_Pack 00–07 + INDEX (Input Mode 0 · FULL · 4 หน้า · 13 API · 13 FN) · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 13
- declaration --final: DOCCFG IVMG PASS (--registry · frd_ref FN-04/FN-06) · NTF PASS (frd_ref FN-08/10/11/13 · 3 event) · DOA PASS (+print_config +html) · MDOC WARN (G04 taxonomy รอ · G09 doa pending) → สำเนาใน FRD_Pack/declarations
- 2026-10-11 08:21 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK0 WARN0 · decl final PASS

## ขั้น 8 — UI Brief → test case → UAT
- UI_BRIEF_F-TMP-009.md (AS-BUILT จาก inventory · _build/build_uibrief.py) · brief_check PASS · FAIL 0 · WARN 0
- testcases-F-TMP-009.md 45 เคส / 229 step · tc_lint ERROR 0 · cases.json (Lite 40 เคส) + QA_AUDIT drop ledger 5 · lite_audit หายเงียบ 0 (--stamp) · testcase-F-TMP-009.html (build.py · shots ว่าง)
- เคส TC-A01/A02/R01/H06 ตรวจ "modal ปิดเรียบร้อย" (บั๊กใบก่อน)
- [NO-BROWSER] ข้าม verify_anchors.py · [NO-BROWSER] ข้าม capture.py (เอกสาร UAT build แบบไม่มีภาพ)
- ตรวจ anchor แบบ static แทน: 153 anchor · ตรงตัวใน feature.html 117 · ที่เหลือ 36 = ข้อความประกอบ/ตัวเลขที่สร้างตอนรัน · สุ่มยืนยันใน jsdom 15/15 ok (ข้อความ footer PDF อยู่ใน iframe srcdoc) · ต้องรัน verify_anchors.py บนเครื่องที่มี browser
- 2026-10-11 08:26 · ขั้น 8 → done · brief_check PASS · tc_lint 0 · lite_audit 0 · NO-BROWSER: ข้าม verify_anchors/capture
