# RUN_LOG — F-TMP-005 FM-BDM-05 แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน (REQ-TMP-005)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: `_system/tools/to_image.py` (LibreOffice → PDF → page-1.png) จาก .xlsx — ไม่ใช่สแกนกระดาษจริง · ภาพเครื่องนี้ไม่มีฟอนต์ไทย (ตัวอักษรเป็นกล่อง) → ใช้ภาพดูโครง/เส้นเท่านั้น · ถ้อยคำยึด content.html + openpyxl (data validation 1 รายการ: สถานะ H36:H41 · footer Doc. No./Rev.)
- ไม่มี PREBRIEF จาก CMS → PREBRIEF v2 สร้างจาก FORM_SPEC (--req REQ-TMP-005 --module BDM) · รอบแรกลืม --req ได้ REQ-XXXX → ไฟล์เก่าย้ายไป .build/
- form_spec_check: ERROR 0 · 23 ช่อง · แถวซ้ำ 1 (เอกสารและเงื่อนไขประกอบ 6 บรรทัด) · ค่าคงที่ 2 · ลายเซ็น 3 · ข้อมูลขัดกัน 5
- ไม่มีข้อมูลส่วนบุคคลในไฟล์ (ฟอร์มเปล่า)
- content.html ใช้แล้ว → ย้ายไป orig/out/content.html (กัน K2 นับเป็น prototype ซ้ำ)
- 2026-10-10 12:23 · ขั้น 1 → done · form_spec_check ERROR 0 · 23 ช่อง · เงื่อนไขประกอบ 6 แถว · ลายเซ็น 3

## ขั้น 2 — gate AI-DEFAULT (unattended-policy)
- G1 ไม่เปลี่ยนค่า/ไม่ส่งต่อ — ไม่สร้าง/ผูกงบลงทุนหรือโครงการอัตโนมัติ · ชื่อโครงการผู้ใช้กรอกเอง (ไม่มีเลขโครงการบนกระดาษ)
- G2 dynamic 2 ขั้นตามช่องลงชื่อ: ผู้ตรวจสอบ (ผู้จัดการฝ่ายพัฒนาธุรกิจ / รองกรรมการผู้จัดการ) → role-line-manager · ผู้อนุมัติ/รับทราบ (กรรมการผู้จัดการ / ผู้มีอำนาจตามตาราง) → role-gm (ไม่มี role ตรงใน master → แจ้งรายงาน) · กระดาษไม่มีช่วงวงเงิน → amount none (ช่องวงเงินส่ง DOA กลางได้ — TODO: DOA engine)
- G3 สถานะเงื่อนไข 4 ค่าอ่านจาก InvestmentMemo.condition_statuses · วงเงินตัวเลข ≥0 · แถวที่กรอกต้องมีรายการ+สถานะ · ยังไม่แล้วเสร็จต้องมีผู้รับผิดชอบ+กำหนดเสร็จ · เงื่อนไขค้างตอนส่ง = เตือน
- G4 ไม่จำกัดแถว (PDF ขั้นต่ำ 6) · G5 1:1 · G6 แถวล่างต่อขั้น ข้อความในระบบ · G7 back_to_draft · G8 เจ้าของ/ผู้อนุมัติหลังส่ง/admin · G9 ออกเลขบันทึกครั้งแรก รหัส IVM (เลี่ยง ACL/PJI/RSK/SCR/PCL/IRV) · G10 แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock พร้อมเริ่มทำ · 16 มติ · AI-DEFAULT 11 · VALID 5
- 2026-10-10 12:24 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · 16 มติ · AI-DEFAULT 11

## ขั้น 3 — declaration ร่าง
- doa_tool init (IVM · dynamic 2 ขั้น · back_to_draft) → เติมคำตัดสินต่อขั้น AI-DEFAULT (ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ · อนุมัติ / รับทราบ/ไม่อนุมัติ — ไม่ใช้ "ส่งกลับแก้ไข") + role_notes + amount_note (TODO: DOA engine) · validate PASS · --print-config PASS
- ntf: ivm_cancelled + ivm_approved_open_conditions (อนุมัติแล้วยังมีเงื่อนไขไม่แล้วเสร็จ → แจ้งผู้จัดทำ) · ตัด over_limit (ฟอร์มไม่มีเกณฑ์ตัวเลข) · PASS
- doccfg IVM (--registry ไม่ชน · เลี่ยง ACL/PJI/RSK/SCR/PCL/IRV) PASS · mdoc WARN (G04 taxonomy รออนุมัติ · G09 doa pending) BLOCK 0

## ขั้น 4 — แบบพิมพ์ Replica (R9 ตารางกรอบ · R10 2 หน้า)
- 2 หน้า: หน้า 1 หัว+ข้อมูลแบบฟอร์ม+ข้อมูลสรุปโครงการ/การลงทุน+บทสรุปผู้บริหาร 13 หัวข้อ · หน้า 2 หัวย่อ (ต่อ)+เอกสารและเงื่อนไขประกอบ (≥6 แถว)+ลงชื่อ+ประวัติ · ฟอนต์ 8.5pt · ตัดหน้าก่อนบล็อกลงชื่อ · thead · หน้า N/2
- parity IDENTICAL 5/5 · ไม่มี {{}} หลง
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py เรียก render_pdf → ทำ render_doc + build_html เองด้วย .build/render_nobrowser.py ได้ out/*.html + FM-BDM-05_template.html)
- [NO-BROWSER] ข้าม compare_original.py บนเครื่อง user — verify-only บน cloud container: Chromium render 5 สถานะ = 2 หน้าทุกสถานะ · ภาพ out/_states_sheet(.png/_p2.png) ดูแล้ว (ไม่ล้น · ลายเซ็นครบตาม signs) · compare approved vs ต้นฉบับ = 0.408 WARN (region 0:0.6 = 0.357) — อธิบายใน print-spec §7 · PDF ไม่ส่งเข้า DevPack
- 2026-10-10 12:28 · ขั้น 4 → done · parity 5/5 · 2 หน้าทุกสถานะ (verify container) · compare 0.408 WARN อธิบายแล้ว · NO-BROWSER ไม่มี PDF
- 2026-10-10 12:28 · ขั้น 3 → done · doa PASS · ntf PASS · doccfg IVM PASS · mdoc WARN(BLOCK 0)

## ขั้น 5 — HTML Q-form (html-generator v9.4)
- ฐาน: Q-form shell ของ DevPack พี่น้อง F-TMP-004 (ลอก F-TMP-002 → archetype F-FIN-ACL · ผ่าน audit/e2e/U1–U28) → เขียนส่วน domain ใหม่ทั้งหมดตาม FORM_SPEC 1:1 (.build/ivm_a–d.js · ivm.css) · เปิด GOLDEN_SKELETON + ui-standard-list-drawer U1–U28 เทียบก่อน build · ประกอบด้วย .build/assemble.py
- ขั้น 1 wizard = การ์ด ① ข้อมูลสรุปโครงการ/การลงทุน (ผู้เสนอ = search-select · วงเงินตัวเลข ≥0) ② บทสรุปผู้บริหาร 13 หัวข้อ (7 บังคับตาม FORM_SPEC) ③ เอกสารและเงื่อนไขประกอบ (6 ช่อง → ตาราง · เพิ่ม/ลบแถวไม่จำกัด · ผู้รับผิดชอบ search-select · กำหนดเสร็จ be-datepicker · สถานะ 4 ค่าจาก config) · แถบสรุปสดด้านบน · เงื่อนไขค้าง = แถบเตือนใน review/ส่ง/อนุมัติ (ไม่บล็อก)
- audit รอบ 1 FAIL 0 · WARN 3 (skeleton เดิม: ss-caret/empty-icon ไม่มี w- · .uc-email · font-size px) · prune_css ตัด 0.6 KB → audit ซ้ำ FAIL 0 WARN 3
- [NO-BROWSER] ข้าม e2e_standard.py บนเครื่อง user — verify บน cloud container (Chromium): 21/21 ผ่าน (reports/e2e_report.json) · smoke flow สร้าง→ตรวจแถวเงื่อนไข (owner/due บังคับเมื่อยังไม่แล้วเสร็จ)→ส่ง→อนุมัติขั้น 1 ไม่มี pageerror · [NO-BROWSER] ข้าม render-check.py
- คำตัดสิน: ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ · อนุมัติ / รับทราบ/ไม่อนุมัติ (ไม่ใช้ "ส่งกลับแก้ไข")
- meta cube-archetype=Q-form ✓ · window.__QA__ ✓
- U1 ✓ (badge ใน sub) U2 ✓ U3 ✓ U4 ✓ U5 ✓ kebab U6 ✓ page-size 25 U7 ✓ U8 ✓ wizard 1290 U9 ✓ U10 ✓ U11 ✓ U12 ✓ U13 ✓ U14 ✓ U15 ✓ U16 n/a (ไม่มีลบเอกสาร · ลบแถวใน wizard) U17 ✓ คน=icon วงกลม U18 ✓ ชื่อโครงการ ellipsis · เงื่อนไข 1 pill U19 ✓ U20 n/a (ชุดเดียว) U21 ~ (font-size skeleton เดิม) U22 ✓ U23 ✓ (ตารางเงื่อนไขว่าง = แผงไม่มีข้อมูล) U24 ✓ search-select ผู้เสนอ/ผู้รับผิดชอบ U25 ✓ backdrop onmousedown U26–U28 n/a
- 2026-10-10 12:37 · ขั้น 5 → done · audit FAIL 0 · e2e 21/21 (container) · U1–U28 ✓
- 2026-10-10 12:37 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-005.md (+.docx md_to_docx) Prebrief Mode · Scope Lock = DEC-01..16 ตรงตัวจาก DECISIONS.lock · Quality Gate C1–C20 → APPROVED (C16 WARN ไม่มี registry ตรง — feature ใหม่)
- FRD_F-TMP-005_Pack 00–07 + INDEX + declarations/ · frd_lint รอบ 1: BLOCK 0 · WARN 0 · PASS 12
- frd_ref ใส่ตาม lint: doccfg FN-03/FN-05 · ntf FN-07/FN-09 · doccfg --final PASS (--registry ไม่ชน · IVM) · ntf --final PASS · doa validate --html PASS · mdoc WARN (G04 taxonomy · G09 doa pending) BLOCK 0
- 2026-10-10 12:42 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · declaration --final PASS

## ขั้น 8 — UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-005.md (AS-BUILT) จาก inventory (.build/make_brief.py) · brief_check รอบ 1 PASS · FAIL 0 · WARN 0
- testcases-F-TMP-005.md 31 เคส / 71 step · tc_lint ERROR 0
- [NO-BROWSER] ข้าม verify_anchors.py บนเครื่อง user — verify บน cloud container: รอบ 1 MISSING 1 (ข้อความ "กรุณากรอกชื่อโครงการ" ประกอบจากโค้ด) → แก้ anchor → DOM 111 · SOURCE 28 · MISSING 0 (reports/anchors.json)
- cases.json (Lite) 27 เคส / 64 step · QA_AUDIT drop ledger 4 · lite_audit หายเงียบ 0 · stamp แล้ว · testcase-F-TMP-005.html build (ไม่มีภาพ — [NO-BROWSER] ข้าม capture.py)
- 2026-10-10 12:47 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 · anchors MISSING 0 (container) · lite_audit หายเงียบ 0
