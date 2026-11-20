# RUN_LOG — F-TMP-003 FM-BDM-03 แบบฟอร์มสรุปผลการคัดกรองโครงการเบื้องต้น (REQ-TMP-003)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: `_system/tools/to_image.py` (LibreOffice → PDF → page-1.png) จาก .xlsx — ไม่ใช่สแกนกระดาษจริง (ฟอนต์ไทยในภาพไม่ขึ้น ใช้ดูตำแหน่ง/เส้นเท่านั้น) · ถ้อยคำยึด openpyxl + content.html (ย้ายไป orig/out/ แล้ว)
- ไม่มี PREBRIEF จาก CMS → PREBRIEF v2 สร้างจาก FORM_SPEC (--module BDM)
- form_spec_check: ERROR 0 · WARN 0 · 14 ช่อง · เกณฑ์ 8 แถว (คงที่) · สูตร 3 · ค่าคงที่ 3 · ลายเซ็น 3 · ข้อมูลขัดกัน 6 (DV ผ่าน/ไม่ผ่านทับช่องคะแนน · 0 แสดงก่อนให้คะแนน · ผลพิจารณาขัดผลเสนอ · มีเงื่อนไขแต่ไม่ระบุ · ไม่มีช่องโครงการ · น้ำหนักไม่ตรวจผลรวม)
- ไม่มีข้อมูลส่วนบุคคลในไฟล์ (ฟอร์มเปล่า)
- 2026-10-10 09:16 · ขั้น 1 → done · form_spec_check ERROR 0 · 14 ช่อง · เกณฑ์ 8 แถว · ลายเซ็น 3

## ขั้น 2 — gate AI-DEFAULT (unattended-policy)
- G1 ไม่เปลี่ยนค่า/ไม่ส่งต่อ — ผลคัดกรองเก็บในเอกสารนี้ · ผล "ไม่ดำเนินการต่อ" ผู้ใช้ทำ FM-BDM-04 เอง (ไม่ผูกอัตโนมัติ)
- G2 dynamic 2 ขั้นตามช่องลงชื่อ: ผู้ตรวจสอบ (ผู้จัดการฝ่ายพัฒนาธุรกิจ) → role-line-manager · ผู้อนุมัติ/รับทราบ (รองกรรมการผู้จัดการ / ผู้มีอำนาจตามตารางอำนาจอนุมัติ) → role-gm (ไม่มี role รองกรรมการผู้จัดการใน contract → แจ้งรายงาน) · ไม่มีวงเงิน
- G3 เกณฑ์/น้ำหนัก/เกณฑ์ 80-60 อ่านจาก ScreeningCriteria config · ถ่วงน้ำหนัก = น้ำหนัก×คะแนน/5 · ตัด DV ผ่าน/ไม่ผ่านที่ทับช่องคะแนน · มีเงื่อนไข → บังคับเงื่อนไข · ผลพิจารณาขัดผลเสนอ = เตือน
- G4 เกณฑ์ 8 แถวคงที่ · G5 1:1 · G6 แถวล่างต่อขั้น ข้อความในระบบ · G7 back_to_draft · G8 เจ้าของ/ผู้อนุมัติหลังส่ง/admin · G9 ออกเลขบันทึกครั้งแรก รหัส SCR (ไม่ชน ACL/PJI/RSK) · G10 แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock พร้อมเริ่มทำ · 17 มติ · AI-DEFAULT 11 · VALID 6
- 2026-10-10 09:16 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · 17 มติ · AI-DEFAULT 11

## ขั้น 3 — declaration ร่าง
- doa_tool init (G7 back_to_draft) → เติมคำตัดสินต่อ role AI-DEFAULT: ผู้ตรวจสอบ ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ · ผู้อนุมัติ/รับทราบ อนุมัติ / รับทราบ/ไม่อนุมัติ (ไม่ใช้ "ส่งกลับแก้ไข" — ชนปุ่มแก้ไขใน e2e) · role_notes role-gm ชั่วคราว · validate PASS · brief PASS
- ntf: scr_cancelled + scr_not_proceed_approved (ผลพิจารณา ไม่ดำเนินการต่อ → แจ้งผู้จัดทำทำ FM-BDM-04 · in-app+email) · ตัด over_limit (review — ผลพิจารณาขัดผลเสนอเตือนตอนกรอกแล้ว) · BLOCK 0
- doccfg SCR (--registry ไม่ชน ACL/PJI/RSK · เลี่ยงรหัสที่ FM-BDM-04 น่าจะใช้) PASS · mdoc WARN (G04 taxonomy รออนุมัติ · G09 doa pending) BLOCK 0

## ขั้น 4 — แบบพิมพ์ Replica (R9 ตารางกรอบ · R10 2 หน้า)
- รอบแรกออกแบบ 1 หน้า 9pt → verify Chromium container: long-text / DOA 6 ขั้น ล้นเป็น 2 หน้า (หน้าไม่เท่ากัน) → ออกแบบ 2 หน้าตาม R10
- รอบ 2 ตัดก่อนบล็อกลงชื่อ → long-text ยังได้ 3 หน้า (ข้อสรุปยาวล้นหน้า 1) → รอบ 3 ตัดหลังตารางการประเมิน: หน้า 1 = หัว + 8 เกณฑ์ + คะแนนรวม + "มีต่อหน้าถัดไป" · หน้า 2 = หัวย่อ (ต่อ + เลขที่) + ข้อสรุป + บล็อกลงชื่อทั้งก้อน + ประวัติ · ฟอนต์ 9pt · "หน้า N/2"
- data 5 สถานะ (draft 3/8 · approved 73 มีเงื่อนไข · rejected 48 · long-text dense · approved-doa6steps 7 ช่อง 4+3) · ข้อมูลสมมติทั้งหมด
- parity IDENTICAL 5/5 · ไม่มี {{}} หลง · missing keys 0 · out/*.html + FM-BDM-03_template.html
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py เรียก render_pdf → ทำ render_doc + build_html แทน ได้ out/*.html)
- verify-only (Chromium container): 5 สถานะ = 2 หน้าทุกสถานะ · _states_sheet หน้า 1/2 ดูแล้ว (ไม่ล้น · ลายเซ็นครบตาม signs) · PDF/ภาพไม่ใส่ในชุด
- [NO-BROWSER] ข้าม compare_original.py บนเครื่อง user — container: approved vs ต้นฉบับ region 0:0.6 = 0.403 WARN อธิบายใน print-spec §7 (Excel ย่อ 48% 1 หน้า vs ระบบ 2 หน้า 9pt)
- print_config.json (SCR · pages 2 · sign_boxes doa_step:* · decision_words.by_role) · SCR_print-spec.md · doa validate --print-config PASS (G8/G9)
- 2026-10-10 09:22 · ขั้น 4 → done · parity 5/5 · 2 หน้าทุกสถานะ (verify container) · compare 0.403 WARN อธิบายแล้ว · NO-BROWSER ไม่มี PDF
- 2026-10-10 09:22 · ขั้น 3 → done · doa PASS · ntf PASS · doccfg SCR PASS · mdoc WARN(BLOCK 0)

## ขั้น 5 — HTML Q-form (html-generator v9.4)
- ฐาน: feature.html ของ J002 (Q-form ผ่าน audit FAIL 0 · e2e 21/21 · ลอก generic ตาม form-archetype README) → เขียน domain ใหม่ตาม FORM_SPEC 1:1 · เทียบ GOLDEN_SKELETON + U1–U28 ก่อน build
- ขั้น 1 wizard: แถบสรุปสด (ให้คะแนนแล้ว x/8 · คะแนนรวม · ผลเสนอ · เกณฑ์ ≥80/≥60) + ตารางเกณฑ์ 8 แถวคงที่ (6 ช่อง → ตาราง Rule #107 · คะแนนถ่วงน้ำหนักคำนวณสด) + ข้อสรุป 6 หัวข้อ (ผลการพิจารณา 3 ค่า → track-card) · ผลพิจารณาขัดผลเสนอ = เตือน + บังคับเงื่อนไข / ข้อสั่งการ · มีเงื่อนไข = บังคับเงื่อนไข
- ScreeningCriteria (items/น้ำหนัก/bands) เป็น config mock แยก const · snapshot ลงใบตอนสร้าง · docPrintData → parity_check IDENTICAL กับ form.tpl.html (approved + draft จาก prototype) · key set ตรง print/*.data.json
- ตัดคอลัมน์ "ฝ่าย" ออกจากตาราง list (ล้นความกว้าง 1440 — U18) · ฝ่ายยังเป็น filter + อยู่ใน drawer
- audit.sh FAIL 0 · WARN 3 (เท่าฐาน: lucide class ใน helper · .uc-email · hardcoded font-size) · prune_css ตัด 0.4 KB → audit ซ้ำ FAIL 0
- [NO-BROWSER] ข้าม e2e_standard.py · ข้าม render-check.py บนเครื่อง user — verify บน cloud container (Chromium): e2e 21/21 ผ่าน (ไม่ใส่ในชุด · สำเนาที่ .build/e2e_report.container.json) · smoke สร้าง→ส่ง→ตรวจสอบแล้ว→อนุมัติ/รับทราบ = approved · JS error 0
- meta cube-archetype=Q-form ✓ · window.__QA__ ✓
- U1 ✓ (ไม่มี stat cards · badge ใน sub) U2 ✓ U3 ✓ U4 ✓ U5 ✓ kebab U6 ✓ page-size 25 U7 ✓ U8 ✓ U9 ✓ U10 ✓ U11 ✓ U12 ✓ U13 ✓ U14 ✓ wizard 1290 U15 ✓ U16 n/a (ไม่มีลบ) U17 ✓ คน=icon วงกลม U18 ✓ (ตัดคอลัมน์ฝ่าย) U19 ✓ sub = คะแนนรวม · ผลพิจารณา U20 n/a (ชุดเดียว) U21 ~ (font-size ฐานเดิม) U22 ✓ U23 ✓ U24 ✓ search-select U25 ✓ backdrop onmousedown U26–U28 n/a (ไม่มีหน้าตั้งค่า)
- 2026-10-10 09:33 · ขั้น 5 → done · audit FAIL 0 · e2e 21/21 (container) · U1–U28 ✓
- 2026-10-10 09:33 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-003.md (+.docx) Prebrief Mode · Quality Gate C1–C20 → APPROVED (C16 WARN ไม่มี registry ตรง — feature ใหม่)
- FRD_F-TMP-003_Pack 00–07 + INDEX + declarations/ · 07 สร้างจาก DECISIONS.lock (DEC-01..17 ครบ) + LD-01..07
- frd_lint รอบ 1: BLOCK 0 · WARN 0 · PASS 15 (reports/_SECTION_N.md)
- frd_ref ใส่ตาม lint: doccfg numbering FN-03 · snapshot FN-05 · ntf scr_cancelled FN-07/09 · scr_not_proceed_approved FN-09 · doccfg --final --registry PASS (SCR ไม่ชน) · ntf --final PASS · doa PASS · mdoc WARN (G04 taxonomy · G09 doa pending) BLOCK 0
- 2026-10-10 09:38 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · declaration --final PASS

## ขั้น 8 — UI Brief → test case AI → UAT
- HTML แก้ก่อนทำ brief: openSubmit ตรวจความครบ (isComplete — ร่างที่ให้คะแนนไม่ครบส่งไม่ได้ · toast เตือน) · PREFLIGHT comment อัปเดตเป็น SCR → audit FAIL 0 · e2e 21/21 (container) · smoke ผ่าน
- UI_BRIEF_F-TMP-003.md (AS-BUILT จาก extract_anchors) · brief_check PASS · FAIL 0 · WARN 0 (รอบ 1 FAIL B5 `.sc-chip` ค้างจากฐาน → ลบ)
- testcases-F-TMP-003.md 31 เคส / 68 step · tc_lint ERROR 0
- [NO-BROWSER] ข้าม verify_anchors.py บนเครื่อง user — verify บน cloud container: DOM 87 · SOURCE 27 · DATA 5 · MISSING 0 (สำเนา .build/anchors.container.json · ไม่ใส่ในชุด)
- cases.json (Lite) 25 เคส / 58 step · QA_AUDIT drop ledger 6 · lite_audit หายเงียบ 0 · stamp แล้ว · testcase-F-TMP-003.html build (ไม่มีภาพ — [NO-BROWSER] ข้าม capture.py)
- 2026-10-10 12:18 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 · anchors MISSING 0 (container) · lite_audit หายเงียบ 0
