# RUN_LOG — F-TMP-006 FM-BDM-06 แบบฟอร์มบันทึกการตรวจทานและอนุมัติภายใน (REQ-TMP-006)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: `_system/tools/to_image.py` (LibreOffice → PDF → page-1.png) จาก .xlsx — ไม่ใช่สแกนกระดาษจริง · ถ้อยคำยึด content.html + openpyxl (data validation · footer Doc. No./Rev.) · content.html ย้ายไป orig/out/ แล้ว
- ไม่มี PREBRIEF จาก CMS → PREBRIEF v2 สร้างจาก FORM_SPEC (แบบ 1 · Standalone)
- impact_summary.py: regex รับเฉพาะ REQ-ตัวเลข → รันบนสำเนา .build/REQ-0000-006 แล้วแทนกลับเป็น REQ-TMP-006 (ไม่แก้สกิล)
- form_spec_check: ERROR 0 · WARN 0 · 17 ช่อง · แถวซ้ำ 2 กลุ่ม (ตรวจทาน 10 · อนุมัติภายใน 3) · ลายเซ็น 3 · ข้อมูลขัดกัน 6 (data validation/สูตรค้างจาก FM-BDM-02 · อนุมัติครบถ้วนทั้งที่ข้อแก้ไขยังเปิด · ผู้อนุมัติบันทึก 2 ที่ · ไม่มีช่องโครงการ · วันที่มีผลเมื่อไม่อนุมัติ)
- ไม่มีข้อมูลส่วนบุคคลในไฟล์ (ฟอร์มเปล่า) · ชื่อไฟล์ไม่เพี้ยน → ไม่ต้อง rename
- 2026-10-10 12:24 · ขั้น 1 → done · form_spec_check ERROR 0 · 17 ช่อง · 2 กลุ่มแถวซ้ำ · ลายเซ็น 3

## ขั้น 2 — gate AI-DEFAULT (unattended-policy)
- G1 ไม่เปลี่ยนค่า/ไม่ส่งต่อ — บันทึกการตรวจทาน/อนุมัติเก็บในเอกสารนี้ (เอกสารที่ถูกตรวจทานกรอกในรายการเอง)
- G2 dynamic 2 ขั้นตามช่องลงชื่อ: ผู้ตรวจสอบ (ผู้จัดการฝ่ายพัฒนาธุรกิจ/รองกรรมการผู้จัดการ) → role-line-manager · ผู้อนุมัติ/รับทราบ (กรรมการผู้จัดการ/ผู้มีอำนาจตามตารางอำนาจอนุมัติ) → role-gm (ไม่มี role กรรมการผู้จัดการใน contract → แจ้งรายงาน) · ไม่มีวงเงิน
- G3 สถานะข้อแก้ไข/สถานะการอนุมัติ อ่านจาก ReviewApprovalConfig · ตัด DV/สูตรค้างจาก FM-BDM-02 · อนุมัติครบถ้วนแต่ข้อแก้ไขยังเปิด = เตือน · วันที่มีผลบังคับเฉพาะสถานะอนุมัติ
- G4 ไม่จำกัด (PDF ≥10/≥3 แถว) · G5 1:1 · G6 แถวล่างต่อขั้น ข้อความในระบบ · G7 back_to_draft · G8 เจ้าของ/ผู้อนุมัติหลังส่ง/admin · G9 ออกเลขบันทึกครั้งแรก รหัส IRV (EXS/IVM สงวนให้ FM-BDM-05) · G10 แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- impact_summary --decisions: รันผ่านสำเนา REQ-0000-006 แล้วแทนกลับ
- 2026-10-10 12:24 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · 18 มติ · AI-DEFAULT 12

## ขั้น 3 — declaration ร่าง
- doa_tool init (IRV · dynamic 2 ขั้น · back_to_draft) → เติมคำตัดสินต่อขั้น AI-DEFAULT: ผู้ตรวจสอบ ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ · ผู้อนุมัติ อนุมัติ / รับทราบ/ไม่อนุมัติ (ไม่ใช้ "ส่งกลับแก้ไข" กันชนปุ่มแก้ไขใน e2e) · role_notes · validate PASS · validate --print-config PASS (G8/G9)
- ntf: irv_cancelled + irv_approved_open_items (อนุมัติแล้วยังมีข้อแก้ไขเปิด → แจ้งผู้จัดทำ) · ตัด over_limit (review) · BLOCK 0
- doccfg IRV (ไม่ชน registry · EXS/IVM สงวน FM-BDM-05) PASS · mdoc WARN (G04 taxonomy รออนุมัติ · G09 doa pending) BLOCK 0

## ขั้น 4 — แบบพิมพ์ Replica (R9 ตารางกรอบ · R10 2 หน้า)
- 2 หน้า: หน้า 1 หัว+ข้อมูลแบบฟอร์ม+บันทึกการตรวจทาน 14 แถว · หน้า 2 ตรวจทานต่อ+อนุมัติภายใน+สถานะสุดท้าย+ลงชื่อ+ประวัติ · ฟอนต์ 8pt · thead ซ้ำ · หน้า N/2
- parity IDENTICAL 5/5 · ไม่มี {{}} หลง · missing keys 0
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py เรียก render_pdf → ทำเฉพาะ render_doc + build_html ได้ out/*.html)
- verify-only: Chromium บน cloud container render 5 สถานะ = 2 หน้าทุกสถานะ · ภาพ _states_sheet(.png/_p2.png) ดูแล้ว · รอบ 1 วันที่ตัดบรรทัด → ลำดับ 2→1 คอลัมน์ วันที่ 2→3 · PDF ไม่ส่งเข้า DevPack
- [NO-BROWSER] ข้าม compare_original.py บนเครื่อง user — รันใน container (verify): approved vs ต้นฉบับ region 0:0.6 = 0.367 WARN — อธิบายใน print-spec §7
- 2026-10-10 12:30 · ขั้น 4 → done · parity 5/5 · 2 หน้าทุกสถานะ (verify container) · compare 0.367 WARN อธิบายแล้ว · NO-BROWSER ไม่มี PDF
- 2026-10-10 12:30 · ขั้น 3 → done · doa PASS · ntf PASS · doccfg IRV PASS · mdoc WARN(BLOCK 0)

## ขั้น 5 — HTML Q-form (html-generator v9.4)
- ฐาน: shell/CSS/framework จาก DevPack ที่ผ่านแล้วแผนกเดียวกัน (J002 FM-BDM-02 · Q-form v9.4) + เขียน domain script ใหม่ตาม FORM_SPEC 1:1 · เทียบ GOLDEN_SKELETON + U1–U28 ก่อน build
- wizard 3 ขั้น: บันทึกการตรวจทาน (ตาราง 7 ช่อง · Rule #107) › อนุมัติภายในและสถานะสุดท้าย (+ เอกสารแนบ) › ตรวจสอบและยืนยัน · DEC-16 ผลพิจารณา DOA เติมแถวบันทึกการอนุมัติภายในอัตโนมัติ · DEC-18 วันที่มีผล enable ตามสถานะ
- audit รอบ 1 FAIL 1 (Rule #114 type=date) → เปลี่ยนเป็น bedateHTML() (be-datepicker block + CSS) · รอบ 2 พบ CSS bedate หลุดเข้า PDF_CSS (rindex </style>) → ย้ายเข้า <style> หลัก · prune_css ตัด 1.1 KB → audit FAIL 0 · WARN 3 (skeleton เดิม: ss-caret/empty-icon ไม่มี w- · .uc-email · font-size px)
- [NO-BROWSER] ข้าม e2e_standard.py บนเครื่อง user — verify บน cloud container (Chromium): 21/21 ผ่าน (reports/e2e_report.json) · smoke flow สร้าง→ส่ง→อนุมัติ ไม่มี pageerror · render-check.py ข้าม
- meta cube-archetype=Q-form ✓ · window.__QA__ ✓
- U1 ✓ (ไม่มี stat cards · badge ใน sub) U2 ✓ U3 ✓ U4 ✓ U5 ✓ kebab U6 ✓ page-size 25 U7 ✓ U8 ✓ U9 ✓ U10 ✓ U11 ✓ U12 ✓ U13 ✓ U14 ✓ wizard 1290 U15 ✓ U16 n/a (ไม่มีลบ) U17 ✓ คน=icon วงกลม U18 ✓ U19 ✓ U20 n/a (ชุดเดียว) U21 ~ (font-size skeleton เดิม) U22 ✓ U23 ✓ U24 ✓ search-select U25 ✓ backdrop onmousedown U26–U28 n/a (ไม่มีหน้าตั้งค่า)
- 2026-10-10 12:44 · ขั้น 5 → done · audit FAIL 0 · e2e 21/21 (container) · U1–U28 ✓
- 2026-10-10 12:44 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-006.md (+.docx) Prebrief Mode · Quality Gate C1–C20 → APPROVED (C16 WARN ไม่มี registry ตรง — feature ใหม่)
- FRD_F-TMP-006_Pack 00–07 + INDEX + declarations/ · 07 §7.0 สร้างจาก DECISIONS.lock ตรงตัว · frd_lint รอบ 1: BLOCK 0 · WARN 0 · PASS 12
- frd_ref ใส่ตาม lint: doccfg FN-03/FN-05 · ntf FN-07/FN-09 · doccfg --final --registry PASS (IRV ไม่ชน) · ntf --final PASS · doa validate --print-config PASS · mdoc WARN (G04 taxonomy · G09 doa pending) BLOCK 0
- 2026-10-10 12:49 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · declaration --final PASS

## ขั้น 8 — UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-006.md (AS-BUILT) จาก inventory · brief_check รอบ 1 FAIL 1 (B5 อ้าง id ปฏิทินที่สร้างจากโค้ด #bd-vd/#bd-at/#bd-feff) → เปลี่ยนเป็น .bedate + key · รอบ 2 PASS · FAIL 0 · WARN 0
- testcases-F-TMP-006.md 32 เคส / 72 step · tc_lint ERROR 0
- [NO-BROWSER] ข้าม verify_anchors.py บนเครื่อง user — verify บน cloud container: รอบ 1 MISSING 2 (หัว modal ที่ประกอบจากโค้ด) → ถอดตัวหนา → DOM 98 · SOURCE 40 · MISSING 0 (reports/anchors.json)
- cases.json (Lite) 26 เคส · QA_AUDIT drop ledger 6 · lite_audit หายเงียบ 0 · stamp แล้ว · testcase-F-TMP-006.html build (ไม่มีภาพ — [NO-BROWSER] ข้าม capture.py)
- 2026-10-10 12:55 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 · anchors MISSING 0 (container) · lite_audit หายเงียบ 0
