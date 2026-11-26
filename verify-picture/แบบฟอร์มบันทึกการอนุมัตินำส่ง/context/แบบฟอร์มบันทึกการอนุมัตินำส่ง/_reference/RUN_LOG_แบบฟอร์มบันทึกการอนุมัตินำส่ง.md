# RUN_LOG — F-TMP-010 FM-IVM-08 แบบฟอร์มบันทึกการอนุมัตินำส่ง (REQ-TMP-010)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: to_image.py (LibreOffice → PDF → pypdfium2) ได้ page-1.png + content.html · ถ้อยคำยึด openpyxl/content.html · ตำแหน่ง/เส้นยึดภาพ (ภาพฟอนต์ไทยไม่ขึ้น แต่โครงตาราง/เส้นชัด) · ภาพไม่ใช่หน้ากระดาษจริง ห้ามเทียบ layout 1:1
- FORM_SPEC: 13 ช่อง (กรอก 6 · ระบบใส่ 7) · แถวซ้ำ 1 (ผลการพิจารณา 3 แถว = ขั้น DOA) · ตัวเลือก 2 (ระดับอำนาจอนุมัติ — AI-DEFAULT · ผลการพิจารณา = data validation D22:D24 5 ค่า) · สูตร 0 · ค่าคงที่ 0 · ลายเซ็น 3 · anomalies 7 · form_spec_check ERROR 0 WARN 0
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC (--req REQ-TMP-010 --module investment) · impact_summary ฉบับร่าง
- ไฟล์ลูกค้าเป็นฟอร์มเปล่า ไม่มีข้อมูลตัวอย่าง/ข้อมูลส่วนบุคคล · ช่องหลักฐาน/ลายเซ็น (F13) ติด pdpa
- ชื่อฟอร์มจากหัวฟอร์ม (C1) = "แบบฟอร์มบันทึกการอนุมัตินำส่ง" → dm.sh rename (ชื่อในคิวมี FM-IVM-08 นำหน้า)
- 2026-10-11 07:57 · ขั้น 1 → done · FORM_SPEC 13 ช่อง ERROR 0 · PREBRIEF v2

## ขั้น 2 — มติ AI (unattended · ตาม 4_knowledge/governance/unattended-policy.md)
- G1: บันทึกการอนุมัติก่อนนำส่ง ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อ · ชื่อโครงการ/ธุรกรรมกรอกเอง (FM-IVM-01 ยังไม่ลิงก์)
- G2: dynamic ค่าเริ่ม 3 ขั้นตามแถวผลการพิจารณา: ผู้จัดการฝ่ายบริหารการลงทุน → role-line-manager · รองกรรมการผู้จัดการ → role-gm · กรรมการผู้จัดการ / ผู้มีอำนาจ → role-gm · ระดับอำนาจอนุมัติ (ช่องข้อความบนกระดาษ → ตัวเลือก) กำหนด 2/3 ขั้น ส่งให้ DOA กลาง resolve (TODO: DOA engine) · ไม่มีวงเงิน · ⚠ role บนกระดาษไม่มีใน doa-roles-contract
- G3: ไม่มีค่าคงที่/สูตร · ผลการพิจารณา 5 ค่าตาม data validation · มีเงื่อนไข/ให้แก้ไข/ไม่อนุมัติ ต้องมีข้อสั่งการ (บล็อก) · รับทราบเฉพาะขั้นกลาง (บล็อก) · พิจารณาเรียงขั้น · บล็อกลงชื่อใช้ข้อมูล DOA ชุดเดียวกับตาราง
- G4: แถวผลการพิจารณา = 1 ต่อขั้น DOA ไม่จำกัด · PDF ขั้นต่ำ 3 · G5: 1:1 ไม่เพิ่มช่อง · G6: แถวล่างต่อขั้น ข้อความในระบบ
- G7: ให้แก้ไข/ไม่อนุมัติ → ร่างเลขเดิม (back_to_draft) · ยกเลิก owner+admin ร่าง/รออนุมัติ เหตุผลบังคับ · G8: เจ้าของ/ผู้อนุมัติหลังส่ง/admin ฝ่ายเห็นทั้งหมด
- G9: เอกสารภายใน ออกเลขตอนบันทึกครั้งแรก · รหัส IVMH (IVM + H = ฟอร์มลำดับ 08)
- G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock = พร้อมเริ่มทำ · 18 มติ (AI-DEFAULT 11 · VALID 7)
- 2026-10-11 07:58 · ขั้น 2 → done · DECISIONS.lock พร้อม · 18 มติ AI-DEFAULT 11

## ขั้น 3 — หมายเหตุ
- DOA: doa_tool init เขียน on_reject: draft → แก้เป็น back_to_draft (ตรง DEC G7) · ป้ายขั้นตามกระดาษ 3 ขั้น (role-line-manager · role-gm · role-gm) · init ใส่คำตัดสินผิด (reject = อนุมัติแบบมีเงื่อนไข) → แก้เป็น อนุมัติ/ไม่อนุมัติ + decision_options 5 ค่าตาม data validation (รับทราบ เฉพาะขั้นกลาง) · resolve_params authority_level (2/3 ขั้น) · role_notes · TODO: DOA engine · validate PASS · mock → IVMH.doa.mock.js
- ⚠ role บนกระดาษไม่มีใน doa-roles-contract: "ผู้จัดการฝ่ายบริหารการลงทุน" (ใช้ role-line-manager) · "รองกรรมการผู้จัดการ" / "กรรมการผู้จัดการ / ผู้มีอำนาจ" (ใช้ role-gm ทั้งคู่) · module investment ไม่อยู่ใน Module Registry
- ⚠ doa_tool รองรับคำตัดสินคู่ approve/reject เท่านั้น — 5 ผลการพิจารณาอยู่ใน decision_options (ต้องยืนยันว่า DOA กลางรองรับ อนุมัติแบบมีเงื่อนไข/ให้แก้ไข/รับทราบ)
- NTF: ตัด ivmh_over_limit_approved (ไม่มีเกณฑ์ตัวเลข) · เพิ่ม ivmh_conditional_approved (อนุมัติแบบมีเงื่อนไข → แจ้งผู้จัดทำ + admin role) · PASS
- 2026-10-11 07:59 · ขั้น 3 → done · DOA PASS (3 ขั้น dynamic) · NTF PASS (2 event) · doccfg/mdoc หลังขั้น 4

## ขั้น 4 — หมายเหตุ
- แบบพิมพ์: R9 ตารางกรอบ 7 คอลัมน์ (ตัดคอลัมน์ว่าง H–J ของ xlsx) · ยึดโครงพี่น้อง J008 (FM-IVM-06) · ต้นฉบับ 1 หน้า แต่หัว 5 แถว + รายละเอียด 6 แถว (ข้อความยาวได้) + ผลการพิจารณา (1 แถว/ขั้น DOA) + ลงชื่อ + ประวัติ เกิน A4 ที่ ≥ 8pt ในสถานะ DOA 6 ขั้น/ข้อความยาว → ออกแบบ 2 หน้าตาม R10 (ตัดหน้าก่อน "หมายเหตุการใช้งาน" = ก่อนบล็อกลงชื่อ · หัวย่อหน้า 2 · thead ซ้ำ · มีต่อหน้าถัดไป · หน้า 1/2, 2/2) · ฟอนต์ 8.5pt
- ตารางผลการพิจารณา = 1 แถวต่อขั้นใน approval_chain · เติมแถวป้ายขั้นตามกระดาษให้ครบ 3 · ขั้นที่ไม่ต้องพิจารณาตามระดับ → "—" + "ไม่ต้องพิจารณาตามระดับอำนาจอนุมัติ"
- ช่องลงชื่อ sign_rows.py (ผู้จัดทำ + 1 แถว/ขั้น DOA) · decision_words by_role: role-line-manager ตรวจสอบแล้ว/ส่งกลับ · role-gm อนุมัติ / รับทราบ/ส่งกลับ (doa.yaml decision ปรับให้ตรง)
- data 5 สถานะ (draft · approved · rejected (2 ขั้น ให้แก้ไข) · long-text · approved-doa6steps) ข้อมูลสมมติทั้งหมด · parity IDENTICAL 5/5 · render_doc --strict + build_html ไม่มี {{}} หลง
- DOCCFG IVMH PASS (--registry ไม่ชน) · MDOC WARN (taxonomy_def_id รออนุมัติ · doa pending) · doa validate --print-config PASS (BLOCK 0)
- [NO-BROWSER] ข้าม render_states.py (เรียก render_pdf.py) — ยังไม่ได้ PDF/จำนวนหน้า/_states_sheet.png
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ PDF สถานะ approved)
- 2026-10-11 08:02 · ขั้น 4 → done · Replica 2 หน้า R10 · parity 5/5 · NO-BROWSER: ยังไม่ render PDF/compare

## ขั้น 5 — HTML Q-form
- ฐาน: references/form-archetype/_SOURCE_form-request-reference.html (เปลือก/CSS/BASE-KIT) + app script ของ IVMH (_build/app1–5.js · build_feature.py · ดัดจากโครงพี่น้อง J008) + be-datepicker (Rule #114) · DOC_TPL = print/form.tpl.html · tpl_render.js วางตรง
- เทียบ GOLDEN_SKELETON v9.4 + U1–U28 ก่อน build: ไม่มี stat cards (ตัวเลขเป็น badge ใน ph-sub) · kebab ⋮ · คน = วงกลม icon · pagination 25 + page-size · backdrop onmousedown · drawer header lean (sub = ระดับอำนาจอนุมัติ · ผลการพิจารณา) · ไม่มี page tabs (ชุดเดียว)
- ระดับอำนาจอนุมัติ = track-card 2 ค่า (Rule #107) → สายอนุมัติ 2/3 ขั้น · ตารางผลการพิจารณา = ระบบเติมจาก approval_chain (ผู้จัดทำไม่กรอก) · modal พิจารณา: อนุมัติ / อนุมัติแบบมีเงื่อนไข / รับทราบ (ขั้นกลาง) · modal ส่งกลับ: ให้แก้ไข / ไม่อนุมัติ → กลับร่างเลขเดิม · เงื่อนไข / ข้อสั่งการ บังคับเมื่อ มีเงื่อนไข/ให้แก้ไข/ไม่อนุมัติ · ไม่มีทำซ้ำ (DEC-11)
- U1✓ U2✓ U3✓ U4✓ U5✓ U6✓ U7✓ U8✓ U9✓ U10✓ U11✓ U12✓ U13✓ U14✓(wizard wide 3 ขั้น) U15✓ U16 n/a(ไม่มีลบ ใช้ยกเลิก) U17✓ U18✓ U19✓ U20 n/a(ชุดเดียว) U21✓ U22✓ U23✓ U24✓ U25✓ U26–U28 n/a(ไม่มีหน้าตั้งค่า)
- กันบั๊ก modal อนุมัติ/ส่งกลับพังตอนกำลังปิด: render() วาด modal เฉพาะ state.modal.open + guard curStep ใน renderModal (approve/reject)
- audit.sh FAIL 0 · WARN 3 (เท่ากับ canonical: Rule #21 ใน BASE-KIT · .uc-email ใน kit · token font-size) · self_audit PASS · prune_css ตัด 68 rule แล้ว audit/self_audit/smoke ซ้ำผ่าน · node --check ผ่าน · มี meta cube-archetype + window.__QA__
- smoke test แบบไม่มี browser (jsdom · timer จริง · _build/smoke.js): 58/58 — U1/U5/U6 · สิทธิ์ (owner/approver/admin) · view ทุกใบ × 4 แท็บ × 3 persona ไม่มี error · ระดับ → 2/3 ขั้น · validate 5 ช่องบังคับ + ระดับ · ออกเลข IVMH-2569-0013 · ขั้น 1 ไม่มีรับทราบ · มีเงื่อนไขไม่มีข้อสั่งการ บล็อก · ส่งกลับต้องมีข้อสั่งการ · ไม่อนุมัติ = ร่างเลขเดิม · ส่งใหม่ · มีเงื่อนไข → รับทราบ (ขั้นกลาง) → อนุมัติ (ขั้นสุดท้ายไม่มีรับทราบ) modal ปิดไม่พัง · API ล้ม · ยกเลิก · แก้ไขร่าง prefill · PDF แถว 3 "—" ตามระดับ · คำตัดสินตาม role · DOA 6 ขั้น = 7 ช่อง + 6 แถว · CSV · DOC.active=false · ไม่มี JS error
- parity PDF ใน prototype: docPrintData(R1) → render_doc.py (Python) = tplRender (JS) IDENTICAL
- [NO-BROWSER] ข้าม e2e_standard.py · [NO-BROWSER] ข้าม render-check.py
- 2026-10-11 08:15 · ขั้น 5 → done · audit FAIL0 · self_audit PASS · smoke 58/58 · NO-BROWSER ข้าม e2e
- 2026-10-11 08:15 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-010.md (+ .docx md_to_docx) · brd-generator-full v2.3 Prebrief Mode · Quality Gate C1–C20 → APPROVED · §2.4 = DECISIONS.lock 18 DEC · OQ-01..10 (สร้างด้วย _build/make_docs.py — ตาราง DEC ดึงจาก DECISIONS.lock)
- FRD_F-TMP-010_Pack 00–07 + INDEX (Input Mode 0 · FULL) · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 12
- declaration --final: DOCCFG IVMH PASS (--registry · frd_ref FN-03/FN-05) · NTF PASS (frd_ref FN-05/07/09 · 2 event) · DOA PASS (+print_config +html · frd_ref FN-04/05/06/08) · MDOC WARN (G04 taxonomy รอ · G09 doa pending) → สำเนาใน FRD_Pack/declarations
- 2026-10-11 08:20 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK0 WARN0 · decl final PASS

## ขั้น 8 — UI Brief → test case → UAT
- UI_BRIEF_F-TMP-010.md (AS-BUILT จาก inventory · _build/build_uibrief.py) · brief_check PASS · FAIL 0 · WARN 0
- testcases-F-TMP-010.md 42 เคส / 171 step · tc_lint ERROR 0 · cases.json (Lite 37 เคส) + QA_AUDIT drop ledger 5 · lite_audit หายเงียบ 0 (--stamp) · testcase-F-TMP-010.html (build.py · shots ว่าง)
- เคส TC-A01/A03/A04/R01 ตรวจ "modal ปิดเรียบร้อย" (บั๊ก modal พังตอนกำลังปิด)
- [NO-BROWSER] ข้าม verify_anchors.py · [NO-BROWSER] ข้าม capture.py (เอกสาร UAT build แบบไม่มีภาพ)
- ตรวจ anchor แบบ static แทน: 128 anchor · ตรงตัวใน feature.html 93 · ที่เหลือ 35 = ข้อความ/ตัวเลขที่สร้างตอนรัน (toast · x–y จาก N · เลขที่) · สุ่มยืนยันใน jsdom 20/20 ok (_tmp/anchors) · ต้องรัน verify_anchors.py บนเครื่องที่มี browser
- 2026-10-11 08:25 · ขั้น 8 → done · brief_check PASS · tc_lint 0 · lite_audit 0 · NO-BROWSER: ข้าม verify_anchors/capture
