# RUN_LOG — F-TMP-005 FM-IVM-03 แบบฟอร์มบันทึกคำถาม คำตอบ และประเด็นคงค้าง (REQ-TMP-005)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: to_image.py (LibreOffice → PDF → pypdfium2) ได้ page-1.png + content.html · ถ้อยคำยึด openpyxl/content.html · ตำแหน่ง/เส้นยึดภาพ (ภาพจาก LibreOffice ฟอนต์ไทยเป็นกล่อง — ใช้ดูโครง/เส้นเท่านั้น)
- FORM_SPEC: 21 ช่อง · แถวซ้ำ 2 (บันทึกคำถามและคำตอบ 14 แถว · รายการประเด็นคงค้าง 14 แถว) · ตัวเลือก 4 (สถานะคำถาม 5 ค่า H13:H26 · ระดับความสำคัญ 3 ค่า F30:F43 · สถานะประเด็น 4 ค่า H30:H43 · ต้องยกระดับ ใช่/ไม่ใช่ I30:I43) · สูตร 0 · ลายเซ็น 3 · anomalies 7 · form_spec_check ERROR 0
- ช่องเพิ่ม 1 ช่อง: F01 ชื่อโครงการ / ธุรกรรม — กระดาษไม่มีช่องระบุโครงการ (anomaly) · AI-DEFAULT รอลูกค้ายืนยัน
- เลขที่คำถาม Q-xxx / รหัสรายการ OI-xxx พิมพ์ล่วงหน้าบนกระดาษ → ระบบรันเลขต่อใบ (source auto)
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC (--req REQ-TMP-005 --module IVM) · impact_summary ฉบับร่าง
- ชื่อในคิวมีรหัสฟอร์มนำหน้า → dm.sh rename J005 "แบบฟอร์มบันทึกคำถาม คำตอบ และประเด็นคงค้าง" (ชื่อจากหัวฟอร์ม C1)
- ไฟล์ลูกค้าเป็นฟอร์มเปล่า ไม่มีข้อมูลตัวอย่าง/ข้อมูลส่วนบุคคล
- 2026-10-11 00:57 · ขั้น 1 → done · FORM_SPEC 21 ช่อง ERROR 0 · PREBRIEF v2

## ขั้น 2 — มติ AI (unattended · ตาม 4_knowledge/governance/unattended-policy.md)
- G1: บันทึก Q&A/ประเด็นคงค้าง ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อ · ชื่อโครงการกรอกเอง (FM-IVM-01 ยังไม่ลิงก์) · ยกระดับอ้างเลขบันทึก FM-IVM-09 ในหมายเหตุเอง
- G2: dynamic 2 ขั้นตามช่องลงชื่อ: ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน → role-line-manager) · ผู้อนุมัติ/รับทราบ (รอง กก.ผจก./กก.ผจก. → role-gm) · ไม่มีวงเงิน · ⚠ role บนกระดาษไม่มีใน doa-roles-contract
- G3: ไม่มีสูตร · เลข Q/OI รันอัตโนมัติ · ตอบแล้ว/ปิด ต้องมีคำตอบ (บล็อก) · กำหนดไม่ก่อนวันเปิด (บล็อก) · ยกระดับ=ใช่ หมายเหตุบังคับ · เลยกำหนดเตือน · ≥1 แถวก่อนส่ง
- G4: ไม่จำกัดแถว · PDF ขั้นต่ำ 14 / 14 แถว · G5: 1:1 + ช่องเพิ่ม ชื่อโครงการ / ธุรกรรม · G6: แถวล่างต่อขั้น ข้อความในระบบ
- G7: ไม่อนุมัติ → กลับร่างเลขเดิม · ยกเลิก owner+admin ร่าง/รออนุมัติ เหตุผลบังคับ · G8: เจ้าของ/ผู้อนุมัติหลังส่ง/admin ฝ่ายเห็นทั้งหมด
- G9: เอกสารภายใน ออกเลขตอนบันทึกครั้งแรก · รหัส IVMC (IVM + C = ฟอร์มลำดับ 03 ตามแบบแผนชุดนี้)
- G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock = พร้อมเริ่มทำ · 19 มติ (AI-DEFAULT 12 · VALID 7)
- 2026-10-11 00:58 · ขั้น 2 → done · DECISIONS.lock พร้อม · 19 มติ AI-DEFAULT 12
- 2026-10-11 00:58 · ขั้น 3 → done · DOA PASS (2 ขั้น dynamic) · NTF PASS (3 event) · doccfg/mdoc หลังขั้น 4

## ขั้น 3–4 — หมายเหตุ
- DOA: doa_tool init เขียน on_reject: draft → แก้เป็น back_to_draft (ตรง DEC-09) · เติมคำตัดสินขั้น 2 (อนุมัติ/ไม่อนุมัติ) · validate PASS (+print_config PASS) · mock → IVMC.doa.mock.js
- ⚠ role บนกระดาษไม่มีใน doa-roles-contract: "ผู้จัดการฝ่ายบริหารการลงทุน" (ใช้ role-line-manager) · "รองกรรมการผู้จัดการ/กรรมการผู้จัดการ" (ใช้ role-gm) · module investment ไม่อยู่ใน Module Registry
- NTF: ตัด ivmc_over_limit_approved (เลยกำหนดแสดงเตือนขณะกรอก) · เพิ่ม ivmc_log_approved (แจ้งผู้รับผิดชอบตอบ/ผู้รับผิดชอบประเด็น) + ivmc_escalation_flagged (แจ้ง role-gm เมื่อมีประเด็นต้องยกระดับ) · PASS
- DOCCFG IVMC PASS (--registry ไม่ชน IVMA/IVMB/IVMJ/IVMK) · MDOC WARN (G04 taxonomy รออนุมัติ · G09 doa pending) · function_code F01 ค่าชั่วคราว
- แบบพิมพ์: R9 ตารางกรอบ 10 คอลัมน์ · 28 แถวซ้ำ (14+14) > ~20 → ออกแบบ 2 หน้าตาม R10 (ตัดหน้าก่อน "รายการประเด็นคงค้าง" · หัวย่อหน้า 2 · thead ซ้ำ · มีต่อหน้าถัดไป · หน้า 1/2, 2/2) · ฟอนต์ 8pt
- data 5 สถานะ (draft · approved · rejected · long-18questions-16issues · approved-doa6steps) ข้อมูลสมมติทั้งหมด · parity IDENTICAL 5/5 · render_doc --strict + build_html ไม่มี {{}} หลง
- [NO-BROWSER] ข้าม render_states.py (เรียก render_pdf.py) — ยังไม่ได้ PDF/จำนวนหน้า/_states_sheet.png
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ PDF สถานะ approved)
- 2026-10-11 01:00 · ขั้น 4 → done · Replica 2 หน้า R10 · parity 5/5 · NO-BROWSER: ยังไม่ render PDF/compare

## ขั้น 5 — HTML Q-form
- ฐาน: references/form-archetype/_SOURCE_form-request-reference.html (เปลือก/CSS/BASE-KIT) + app script ใหม่ของ IVMC (_build/app1–5.js · build_feature.py) + be-datepicker (Rule #114) · DOC_TPL = print/form.tpl.html · tpl_render.js วางตรง
- เทียบ GOLDEN_SKELETON v9.4 + U1–U28 ก่อน build: ไม่มี stat cards (ตัวเลขเป็น badge ใน ph-sub) · kebab ⋮ · คน = วงกลม icon · pagination 25 + page-size · backdrop onmousedown · drawer header lean (sub = คำถามค้างตอบ/ประเด็นยังไม่ปิด/เลยกำหนด) · ไม่มี page tabs (ชุดเดียว)
- แถวซ้ำ 10 คอลัมน์ → ตารางกรอก (Rule #107 > 4 ช่อง) · วันที่ = bedateHTML ต่อช่อง · สถานะ/ระดับความสำคัญ/ยกระดับ = select ตาม data validation · เลข Q-/OI- ระบบรันตามลำดับแถว · ไม่มีทำซ้ำ (DEC-12)
- U1✓ U2✓ U3✓ U4✓ U5✓ U6✓ U7✓ U8✓ U9✓ U10✓ U11✓ U12✓ U13✓ U14✓(wizard wide 3 ขั้น) U15✓ U16 n/a(ไม่มีลบ ใช้ยกเลิก) U17✓ U18✓ U19✓ U20 n/a(ชุดเดียว) U21✓ U22✓ U23✓ U24✓ U25✓ U26–U28 n/a(ไม่มีหน้าตั้งค่า)
- แก้บั๊กที่พบในใบก่อน: modal อนุมัติ/ส่งกลับพังตอนกำลังปิดหลังตัดสิน (render() เรียก renderModal ขณะ S.md ยังค้าง 200ms แต่ curStep = undefined) → render modal เฉพาะ state.modal.open + guard ใน renderModal
- audit.sh FAIL 0 · WARN 3 (เท่ากับ canonical: Rule #21 ใน BASE-KIT · .uc-email ใน kit · token font-size) · self_audit PASS (แก้ hint ยาว 1) · prune_css ตัด 74 rule แล้ว audit/self_audit ซ้ำผ่าน · node --check ผ่าน
- smoke test แบบไม่มี browser (jsdom · timer จริง · _build/smoke.js): 47/47 — U1/U5/U6 · สิทธิ์ G8 (owner/approver/admin) · view ทุกใบ × 4 แท็บ × 3 persona ไม่มี error · validate (ตอบแล้วไม่มีคำตอบ บล็อก · ยกระดับไม่มีหมายเหตุ บล็อก · กำหนดก่อนวันเปิด บล็อก · ไม่มีแถว บล็อก · เลยกำหนด เตือน) · ออกเลข IVMC-2569-0012 · ส่ง/ส่งกลับเป็นร่างเลขเดิม/ส่งใหม่/อนุมัติ 2 ขั้น โดย modal ปิดไม่พัง · API ล้ม · ยกเลิก · PDF เติมแถว 14/14 · DOA 6 ขั้น = 7 ช่องลงนาม · CSV · DOC.active=false · ไม่มี JS error
- parity PDF ใน prototype: data จาก docPrintData(R1) → render_doc.py (Python) = tplRender (JS) IDENTICAL
- [NO-BROWSER] ข้าม e2e_standard.py · [NO-BROWSER] ข้าม render-check.py
- 2026-10-11 01:08 · ขั้น 5 → done · audit FAIL0 · self_audit PASS · smoke 47/47 · NO-BROWSER ข้าม e2e
- 2026-10-11 01:08 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-005.md (+ .docx md_to_docx) · brd-generator-full v2.3 Prebrief Mode · Quality Gate C1–C20 → APPROVED · §2.4 = DECISIONS.lock 19 DEC · OQ-01..08
- FRD_F-TMP-005_Pack 00–07 + INDEX (Input Mode 0 · FULL) · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 13
- declaration --final: DOCCFG IVMC PASS (--registry · frd_ref FN-04/FN-06) · NTF PASS (frd_ref FN-06/08/10 · 3 event) · DOA PASS (+print_config) · MDOC WARN (G04 taxonomy รอ · G09 doa pending) → สำเนาใน FRD_Pack/declarations
- 2026-10-11 01:12 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK0 WARN0 · decl final PASS

## ขั้น 8 — UI Brief → test case → UAT
- UI_BRIEF_F-TMP-005.md (AS-BUILT จาก inventory · _build/build_uibrief.py) · brief_check PASS · FAIL 0 · WARN 0
- testcases-F-TMP-005.md 40 เคส / 202 step · tc_lint ERROR 0 · cases.json (Lite 35 เคส) + QA_AUDIT drop ledger 5 · lite_audit หายเงียบ 0 (--stamp) · testcase-F-TMP-005.html (build.py · shots ว่าง)
- เคส TC-A01/A02/R01 ตรวจ "modal ปิดเรียบร้อย" (บั๊กใบก่อน)
- [NO-BROWSER] ข้าม verify_anchors.py · [NO-BROWSER] ข้าม capture.py (เอกสาร UAT build แบบไม่มีภาพ)
- 2026-10-11 01:17 · ขั้น 8 → done · brief_check PASS · tc_lint 0 · lite_audit 0 · NO-BROWSER: ข้าม verify_anchors/capture
