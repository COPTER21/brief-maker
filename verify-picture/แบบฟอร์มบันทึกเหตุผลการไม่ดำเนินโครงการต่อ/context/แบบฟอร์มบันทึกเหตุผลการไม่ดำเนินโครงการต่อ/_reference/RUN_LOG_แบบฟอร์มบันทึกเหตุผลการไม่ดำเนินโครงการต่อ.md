# RUN_LOG — F-TMP-004 FM-BDM-04 แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ (REQ-TMP-004)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: `_system/tools/to_image.py` (LibreOffice → PDF → page-1.png) จาก .xlsx — ไม่ใช่สแกนกระดาษจริง · ภาพเครื่องนี้ไม่มีฟอนต์ไทย (ตัวอักษรเป็นกล่อง) → ใช้ภาพดูโครง/เส้นเท่านั้น · ถ้อยคำยึด content.html + openpyxl (data validation 2 รายการ: เลือก ใช่/ไม่ใช่ C20:C27 · สถานะการปิดโครงการ E36 · footer Doc. No./Rev.)
- ไม่มี PREBRIEF จาก CMS → PREBRIEF v2 สร้างจาก FORM_SPEC (--module BDM)
- form_spec_check: ERROR 0 · 16 ช่อง · แถวซ้ำ 1 (เหตุผล 8 แถวตายตัว) · ค่าคงที่ 2 · ลายเซ็น 3 · ข้อมูลขัดกัน 5
- ไม่มีข้อมูลส่วนบุคคลในไฟล์ (ฟอร์มเปล่า)
- content.html ใช้แล้ว → ย้ายไป orig/out/content.html (กัน K2 นับเป็น prototype ซ้ำ)
- 2026-10-10 09:16 · ขั้น 1 → done · form_spec_check ERROR 0 · 16 ช่อง · เหตุผล 8 แถว · ลายเซ็น 3

## ขั้น 2 — gate AI-DEFAULT (unattended-policy)
- G1 ไม่เปลี่ยนค่า/ไม่ส่งต่อ — ไม่ปิดสถานะโครงการต้นทางอัตโนมัติ · ชื่อโครงการผู้ใช้กรอกเอง (ไม่มีเลขโครงการบนกระดาษ)
- G2 dynamic 2 ขั้นตามช่องลงชื่อ: ผู้ตรวจสอบ (ผู้จัดการฝ่ายพัฒนาธุรกิจ) → role-line-manager · ผู้อนุมัติ/รับทราบ (รองกรรมการผู้จัดการ/กรรมการผู้จัดการ/ผู้มีอำนาจตามตาราง) → role-gm (ไม่มี role ตรงใน master → แจ้งรายงาน) · ไม่มีวงเงิน
- G3 รายการเหตุผล 8 ข้อ + สถานะปิดโครงการ อ่านจาก ProjectClosure config · กฎ: ≥1 เหตุผล 'ใช่' · แถว 'ใช่' ต้องมีรายละเอียด · 'ติดตามเงื่อนไขในอนาคต' ต้องมีข้อเสนอติดตาม
- G4 8 แถวตายตัว · G5 1:1 · G6 แถวล่างต่อขั้น ข้อความในระบบ · G7 back_to_draft · G8 เจ้าของ/ผู้อนุมัติหลังส่ง/admin · G9 ออกเลขบันทึกครั้งแรก รหัส PCL (เลี่ยง PJI/RSK/SCR) · G10 แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock พร้อมเริ่มทำ · 16 มติ · AI-DEFAULT 11 · VALID 5
- 2026-10-10 09:16 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · 16 มติ · AI-DEFAULT 11

## ขั้น 3 — declaration ร่าง
- doa_tool init (PCL · dynamic 2 ขั้น · back_to_draft) → เติมคำตัดสินต่อขั้น AI-DEFAULT (ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ · อนุมัติ / รับทราบ/ไม่อนุมัติ — ไม่ใช้ "ส่งกลับแก้ไข") + role_notes · validate PASS · --print-config PASS
- ntf: pcl_cancelled + pcl_followup_approved (อนุมัติแล้วสถานะ 'ติดตามเงื่อนไขในอนาคต' → แจ้งผู้จัดทำ) · ตัด over_limit (ฟอร์มไม่มีเกณฑ์ตัวเลข) · PASS
- doccfg PCL (--registry ไม่ชน · เลี่ยง PJI/RSK/SCR) PASS · mdoc WARN (G04 taxonomy รออนุมัติ · G09 doa pending) BLOCK 0

## ขั้น 4 — แบบพิมพ์ Replica (R9 ตารางกรอบ · R10 2 หน้า)
- 2 หน้า: หน้า 1 หัว+ข้อมูลแบบฟอร์ม+ข้อมูลโครงการ+ตารางเหตุผล 8 แถว · หน้า 2 หัวย่อ (ต่อ)+สรุปและปิดโครงการ+ลงชื่อ+ประวัติ · ฟอนต์ 8.5pt · ตัดหน้าก่อนบล็อกลงชื่อ · thead · หน้า N/2
- parity IDENTICAL 5/5 · ไม่มี {{}} หลง
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py เรียก render_pdf → ทำ render_doc + build_html เองได้ out/*.html)
- verify-only: Chromium บน cloud container render 5 สถานะ = 2 หน้าทุกสถานะ · ภาพ out/_states_sheet(.png/_p2.png) ดูแล้ว (ไม่ล้น · ลายเซ็นครบตาม signs) · PDF ไม่ส่งเข้า DevPack
- compare_original (container) approved vs ต้นฉบับ = 0.467 WARN (region 0:0.6 = 0.402) — อธิบายใน print-spec §7 (ต้นฉบับ Excel ย่อ 1 หน้า vs ระบบ 2 หน้า 8.5pt · cols 0.78)
- 2026-10-10 09:21 · ขั้น 4 → done · parity 5/5 · 2 หน้าทุกสถานะ (verify container) · compare 0.467 WARN อธิบายแล้ว · NO-BROWSER ไม่มี PDF
- 2026-10-10 09:21 · ขั้น 3 → done · doa PASS · ntf PASS · doccfg PCL PASS · mdoc WARN(BLOCK 0)

## ขั้น 5 — HTML Q-form (html-generator v9.4)
- ฐาน: Q-form shell ของ DevPack พี่น้อง (F-TMP-002 ซึ่งลอก archetype F-FIN-ACL · ผ่าน audit/e2e/U1–U28) → เขียนส่วน domain ใหม่ทั้งหมดตาม FORM_SPEC 1:1 · เปิด GOLDEN_SKELETON + ui-standard-list-drawer U1–U28 เทียบก่อน build · ประกอบด้วย .build/assemble.py
- ขั้น 1 wizard = การ์ด ① ข้อมูลโครงการ ② ตารางเหตุผล 8 แถวตายตัว (6 ช่อง → ตาราง · "ไม่ใช่" ปิดช่อง) ③ สรุปและปิดโครงการ (สถานะ 3 ค่า → track card) · แถบสรุปสดด้านบน
- Rule #114: audit รอบ 1 FAIL 1 (input type=date) → ใส่ be-datepicker (bedateHTML) จาก templates/blocks → audit FAIL 0 · WARN 3 (skeleton เดิม: ss-caret/empty-icon ไม่มี w- · .uc-email · font-size px)
- prune_css ตัด 0.4 KB → audit ซ้ำ FAIL 0
- [NO-BROWSER] ข้าม e2e_standard.py บนเครื่อง user — verify บน cloud container (Chromium): 21/21 ผ่าน (reports/e2e_report.json) · smoke flow สร้าง→ส่ง→อนุมัติขั้น 1 ไม่มี pageerror · render-check.py ข้าม
- คำตัดสิน: ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ · อนุมัติ / รับทราบ/ไม่อนุมัติ (ไม่ใช้ "ส่งกลับแก้ไข")
- meta cube-archetype=Q-form ✓ · window.__QA__ ✓
- U1 ✓ (badge ใน sub) U2 ✓ U3 ✓ U4 ✓ U5 ✓ kebab U6 ✓ page-size 25 U7 ✓ U8 ✓ wizard 1290 U9 ✓ U10 ✓ U11 ✓ U12 ✓ U13 ✓ U14 ✓ U15 ✓ U16 n/a (ไม่มีลบ) U17 ✓ คน=icon วงกลม U18 ✓ ชื่อโครงการ ellipsis U19 ✓ U20 n/a (ชุดเดียว) U21 ~ (font-size skeleton เดิม) U22 ✓ U23 ✓ (ตารางเหตุผล 8 แถวเสมอ) U24 ✓ search-select ผู้รับผิดชอบ U25 ✓ backdrop onmousedown U26–U28 n/a
- 2026-10-10 09:31 · ขั้น 5 → done · audit FAIL 0 · e2e 21/21 (container) · U1–U28 ✓
- 2026-10-10 09:31 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-004.md (+.docx) Prebrief Mode · Scope Lock = DEC-01..16 ตรงตัวจาก DECISIONS.lock · Quality Gate C1–C20 → APPROVED (C16 WARN ไม่มี registry ตรง — feature ใหม่)
- FRD_F-TMP-004_Pack 00–07 + INDEX + declarations/ · frd_lint รอบ 1: BLOCK 0 · WARN 0 · PASS 12
- frd_ref ใส่ตาม lint: doccfg FN-03/FN-05 · ntf FN-07/FN-09 · doccfg --final PASS (--registry ไม่ชน · PCL) · ntf --final PASS · doa validate --html PASS · mdoc WARN (G04 taxonomy · G09 doa pending) BLOCK 0
- 2026-10-10 09:36 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · declaration --final PASS

## ขั้น 8 — UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-004.md (AS-BUILT) จาก inventory · brief_check รอบ 1 FAIL 1 (B5 อ้าง #in-* ที่ประกอบจากโค้ด) → เขียน anchor ใหม่ → PASS · FAIL 0 · WARN 0
- testcases-F-TMP-004.md 30 เคส / 66 step · tc_lint ERROR 0
- [NO-BROWSER] ข้าม verify_anchors.py บนเครื่อง user — verify บน cloud container: รอบ 1 MISSING 1 (หัว modal "ไม่ผ่านการตรวจสอบ?" ประกอบจากโค้ด) → แก้ anchor → DOM 98 · SOURCE 28 · MISSING 0 (reports/anchors.json)
- cases.json (Lite) 26 เคส / 59 step · QA_AUDIT drop ledger 4 · lite_audit หายเงียบ 0 · stamp แล้ว · testcase-F-TMP-004.html build (ไม่มีภาพ — [NO-BROWSER] ข้าม capture.py)
- 2026-10-10 12:21 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 · anchors MISSING 0 (container) · lite_audit หายเงียบ 0
