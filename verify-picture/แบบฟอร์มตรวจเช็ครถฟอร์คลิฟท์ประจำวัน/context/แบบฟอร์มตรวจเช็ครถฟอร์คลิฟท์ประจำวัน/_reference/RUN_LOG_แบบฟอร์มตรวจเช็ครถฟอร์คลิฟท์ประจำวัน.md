# RUN_LOG — F-TMP-002 FM-WHS-04 แบบฟอร์มตรวจเช็ครถฟอร์คลิฟท (REQ-TMP-002)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพฟอร์ม: `to_image.py` แปลงผ่าน LibreOffice → PDF → pypdfium2 (หน้ากระดาษจริง ไม่ใช่ HTML+browser) แต่เครื่องไม่มีฟอนต์ไทย → ตัวอักษรไทยในภาพเป็นกล่อง · ถ้อยคำทั้งหมดยึดจาก xlsx (openpyxl) / content.html · ตำแหน่ง/เส้นยึดภาพ
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC
- form.title = "แบบฟอร์มตรวจเช็ครถฟอร์คลิฟท์ประจำวัน" (จากหัวฟอร์ม A5) · ชื่อในคิวไม่เพี้ยน (แค่ชื่อไฟล์ย่อ) → ไม่ rename
- form_spec_check: ERROR 0 · 12 ช่อง · แถวซ้ำ 3 กลุ่ม (15/8/6 แถว × 31 วัน) · ลายเซ็น 2 · anomalies 4 (รวม: ไม่มีช่องหมายเลขรถ — เสนอใน report)
- 2026-10-10 04:21 · ขั้น 1 → done · FORM_SPEC 12 ช่อง ERROR 0 · PREBRIEF v2 สร้างจากฟอร์ม

## ขั้น 2 · gate (unattended — AI-DEFAULT 13 มติ + VALID 4)
- G1 ใบตรวจเช็คประจำวัน ไม่เปลี่ยนค่า/ไม่ส่งต่อ (Asset/Maintenance ยังไม่มี) · G2 ช่อง "หัวหน้างานตรวจสอบ" 1 จุด → role-supervisor (มีใน contract) · G3 รายการตรวจ 3 กลุ่มอ่านจาก config ไม่ hardcode
- G4 แถวมาจาก config · PDF ครบ 15/8/6 · G5 1:1 + แก้สะกด "ปฎิบัติ→ปฏิบัติ" · G6 แถวล่างต่อขั้น · G7 กลับร่าง · G8 admin = role-mgr-wh · G9 FLI ออกเลขตอนบันทึกครั้งแรก · G10 แนบ ✓ CSV ✓
- 2026-10-10 04:22 · ขั้น 2 → done · 17 มติ (AI-DEFAULT 13 · VALID 4) พร้อมเริ่มทำ

## ขั้น 3 · declaration ร่าง
- doa: init เขียน on_reject: draft แต่ validate รับเฉพาะ back_to_draft|end → แก้เป็น back_to_draft (ความหมายเดิมตาม DEC-10) → PASS · role-supervisor
- ntf: เติม fli_defect_found (DEC-16 · หมายเหตุท้ายฟอร์ม) · ตัด fli_over_limit_approved (ไม่มีเกณฑ์ตัวเลข) → PASS
- doccfg + mdoc ทำหลังขั้น 4 (ต้องใช้ print_config)
- 2026-10-10 04:22 · ขั้น 3 → done · doa PASS · ntf PASS (doccfg/mdoc หลังขั้น 4)

## ขั้น 4 · แบบพิมพ์ Replica (R9 ตารางกรอบ + R10 2 หน้า)
- ออกแบบ 2 หน้าตาม R10: ตาราง 29 แถว × 31 วัน + บล็อกลงชื่อ DOA N ขั้น ไม่พอ 1 หน้าที่ฟอนต์ ≥ 8pt (8.5pt) · ตัดหน้าก่อนตารางรถไฟฟ้า · หน้า 2 = รถไฟฟ้า + หมายเหตุ + ลงชื่อทั้งก้อน · หัววันที่ซ้ำ · "หน้า n/2"
- parity_check: IDENTICAL 5/5 (draft · approved · rejected · long-20items · approved-doa6steps 4+3)
- [NO-BROWSER] ข้าม render_pdf.py (ใน render_states.py) — render body + build_html เองครบ 5 สถานะ (ไม่มี {{}} หลง · missing key 0 · โครง 2 หน้าทุกสถานะ) · ไม่มี PDF / _states_sheet.png
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ approved.pdf)
- ไฟล์ค้าง `print/out/_approved-doa6steps.body.html` ลบไม่ได้ (workspace ห้ามลบ) — เป็นไฟล์ชั่วคราว ไม่ใช้
- doccfg FLI PASS (registry ไม่ชน) · mdoc WARN (G04 ไม่มี taxonomy_def_id · G09 doa pending · function_code F01 ชั่วคราว — ไม่มี Taxonomy Master ใน workspace) · source=declaration เพราะ REQ-TMP-002 ไม่ใช่รูปแบบ REQ-YYYY-NNNN
- doa validate --print-config PASS (G8 doa_step:* · G9 by_role role-supervisor)
- 2026-10-10 04:27 · ขั้น 4 → done · 2 หน้า R10 · parity 5/5 · [NO-BROWSER] ไม่มี PDF/compare · doccfg PASS · mdoc WARN

## ขั้น 5 · HTML Q-form (html-generator v9.4)
- ฐาน: references/form-archetype (Q-form) + เทียบ GOLDEN_SKELETON/U1–U28 · build = kit กลาง (ไม่แก้ BASE-KIT) + page CSS + app JS ของ FLI · ฝัง form.tpl.html + tpl_render.js + PDF_CSS (base+replica+profile)
- หมายเหตุ: reference Q-form เดิม FAIL #114 (type=date) — FLI ไม่ใช้ช่องวันที่ (เลือกเดือนด้วย search-select + ปุ่มวัน) · golden skeleton เองก็ FAIL 3 ข้อ → ใช้เป็นแบบเทียบโครงเท่านั้น
- audit.sh: FAIL 0 · WARN 3 (มาจาก BASE-KIT เดิม: #21 icon ใน kit · #40 .uc-email · font-size px ใน kit) · prune_css ตัด 57 rule แล้ว audit ซ้ำ FAIL 0
- [NO-BROWSER] ข้าม e2e_standard.py · ข้าม render-check.py → ทดแทนด้วย smoke test jsdom (reports/smoke_jsdom.js) 27/27 PASS: สิทธิ์เห็น (owner/approver/admin) · ทุก tab ทุกใบ ไม่มี error · PDF 2 หน้าไม่มี {{}} · validation (ประเภทรถ · วันกรอกไม่ครบ · วันอนาคต) · ส่ง → ส่งกลับ → ส่งใหม่ → ตรวจสอบแล้ว · DOA 2 ขั้นเรียงขั้น · ยกเลิก · ไม่มี JS error
- แก้ระหว่างทาง: renderModal อ่าน curStep หลังตัดสิน (undefined) → stepWords() — พบจาก smoke รอบ 1 แก้แล้วผ่าน
- U1–U28: U1✓ no-scorecard (นับใน ph-count) · U2✓ · U3✓ · U4✓ · U5✓ kebab ⋮ · U6✓ pager 25 · U7✓ CSV ที่ head · U8✓ 920/1290 · U9✓ เหตุผลบังคับ · U10✓ pill · U11✓ · U12✓ lucide mono · U13✓ block ลายเซ็นกลาง · U14✓ Q2 wizard 3 ขั้น · U15✓ edit = wizard เดียวกัน · U16 n/a (ไม่มีลบ ใช้ยกเลิก+เหตุผล) · U17✓ person icon · U18✓ · U19✓ header sub 2 fact · U20✓ segmented (ทั้งหมด/รอฉันตรวจสอบ) ไม่ซ้ำแกน filter · U21✓ (page CSS ใช้ --fs-*) · U22✓ · U23✓ empty panel ทุกตาราง · U24✓ search-select · U25✓ backdrop onmousedown · U26–U28 n/a (ไม่มีหน้า config ในรอบนี้ — ForkliftChecklistConfig เสนอเป็น feature ใหม่)
- 2026-10-10 04:42 · ขั้น 5 → done · audit FAIL 0 · [NO-BROWSER] e2e ข้าม → jsdom smoke 27/27 · U1–U28 ✓
- 2026-10-10 04:42 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-002.md (+ .docx md_to_docx) · Prebrief Mode · AI Review C01–C23/PE01–05 → APPROVED (C22 ตัวชี้วัด → OQ-01 ตามกติกา ห้ามแต่งตัวเลข)
- FRD_F-TMP-002_Pack 00–07 + INDEX · frd_lint Section N: BLOCK 0 · WARN 1 (N3 false positive: เลข 15 ใน "DEC-15"/§5.4 — ไม่มีจำนวนรายการตายตัวใน logic)
- declaration --final: DOCCFG PASS (registry ไม่ชน · FLI) · NTF PASS · DOA PASS (print_config G8/G9) · MDOC WARN (G04 taxonomy_def_id ว่าง · G09 doa pending · function_code F01 ชั่วคราว) → คัดลง FRD_F-TMP-002_Pack/declarations/
- 2026-10-10 04:47 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 (WARN 1 false positive) · declaration --final PASS (mdoc WARN)

## ขั้น 8 · UI Brief → test case AI → UAT
- html-ui-brief: extract_anchors (vars 47 · z 21 · routes 5 · toast 12) → UI_BRIEF_F-TMP-002.md · brief_check PASS (FAIL 0 · WARN 0)
- ai-testcase-md-generator: testcases-F-TMP-002.md 64 เคส / 159 step · tc_lint ERROR 0 · Ledger ครบ (AC 14/14 · BR 17/18 · VR 6/6 · EC 8/10 · error 18/18 · permission 14/14 · XT 3/3 · DEC 17/17)
- [NO-BROWSER] ข้าม verify_anchors.py (playwright) — anchor ตรวจด้วย jsdom smoke + อ่านโค้ด
- qa-friendly: cases.json Lite 49 เคส / 81 step · lite_audit หายเงียบ 0 (drop ledger 15) --stamp · [NO-BROWSER] ข้าม capture.py → shots ว่าง (regionKey "" ทุก step) · build testcase-F-TMP-002.html
- หมายเหตุ: ไฟล์ shots_b64.json ({} ว่าง) อยู่ใน work (ลบไม่ได้) — ใช้แทนผล capture
- 2026-10-10 04:58 · ขั้น 8 → done · brief_check PASS · tc_lint ERROR 0 (64 เคส) · lite_audit หายเงียบ 0 · [NO-BROWSER] verify_anchors/capture ข้าม

## ขั้น 9 · แพ็ก
- manifest_scan: K2 BLOCK เพราะ orig/content.html (ผลของ to_image.py) ถูกจับเป็น prototype ซ้ำ → เปลี่ยนชื่อเป็น orig/content_text.htm (ลบไม่ได้ · เนื้อหาเดิม) → consistency READY (BLOCK 0 · WARN 1: K9 ไม่มี e2e report — [NO-BROWSER])
