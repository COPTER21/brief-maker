# RUN_LOG — F-TMP-008 FM-BDM-08 แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายบริหารการลงทุนจัดเก็บ) (REQ-TMP-008)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: `_system/tools/to_image.py` (LibreOffice → PDF → page-1.png) จาก .xlsx — ไม่ใช่สแกนกระดาษจริง · ฟอนต์ไทยในภาพเป็นกล่อง → ถ้อยคำยึด content.html + openpyxl (data validation E18/E22:E33/F22:F33 · footer Doc. No./Rev.) · content.html ย้ายไป orig/out/ แล้ว
- form.title = "แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายบริหารการลงทุนจัดเก็บ)" — หัวฟอร์มเหมือน FM-BDM-07 → คงวงเล็บไว้ให้โฟลเดอร์ DevPack ไม่ชน · ชื่อไฟล์ไม่เพี้ยน → ไม่ต้อง rename
- ไม่มี PREBRIEF จาก CMS → PREBRIEF v2 สร้างจาก FORM_SPEC (แบบ 1 · Standalone)
- form_spec_check: ERROR 0 · 18 ช่อง · แถวซ้ำ 1 กลุ่ม (ผลการตรวจรับเอกสาร 12) · ลายเซ็น 3 · ค่าคงที่ 3 · ข้อมูลขัดกัน 6 (รับมอบครบถ้วนทั้งที่มีแถวไม่ผ่าน · ไม่ได้รับแต่ครบถ้วน · แถวไม่ผ่านไม่บังคับผู้รับผิดชอบ/กำหนดส่ง · วันที่ก่อนวันรับมอบ · ไม่ครบแต่ไม่กรอกประเด็นค้าง · ไม่มีช่องผูก FM-BDM-07)
- ไม่มีข้อมูลส่วนบุคคลในไฟล์ (ฟอร์มเปล่า)
- 2026-10-10 12:58 · ขั้น 1 → done · form_spec_check ERROR 0 · 18 ช่อง · 1 กลุ่มแถวซ้ำ · ลายเซ็น 3

## ขั้น 2 — gate AI-DEFAULT (unattended-policy)
- G1 ไม่เปลี่ยนค่า/ไม่ส่งต่อ — ผลการรับมอบเก็บในเอกสารนี้ · ชื่อโครงการ/เอกสารที่ส่งมอบผู้ใช้กรอกเอง · ไม่ผูก FM-BDM-07 อัตโนมัติ
- G2 dynamic 2 ขั้นตามช่องลงชื่อ: ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน) → role-line-manager · ผู้อนุมัติ/รับทราบ (ฝ่ายพัฒนาธุรกิจรับทราบ — ข้ามฝ่าย) → role-mgr-bu (ไม่มี role ผู้จัดการฝ่ายพัฒนาธุรกิจใน contract → แจ้งรายงาน) · ไม่มีวงเงิน
- G3 ตัวเลือก 3 ชุดอ่านจาก HandoverConfig · รับมอบครบถ้วนได้เฉพาะทุกแถวได้รับ+ครบถ้วน (บังคับ) · แถวไม่ผ่านต้องมีประเด็น/ผู้รับผิดชอบ/กำหนดส่ง · วันที่ ≥ วันรับมอบ · ไม่ครบ → ประเด็นค้างบังคับ
- G4 ไม่จำกัด (PDF ≥12 แถว) · G5 1:1 · G6 แถวล่างต่อขั้น ข้อความในระบบ · G7 back_to_draft · G8 เจ้าของ/ผู้อนุมัติหลังส่ง/admin ฝ่ายบริหารการลงทุน · G9 ออกเลขบันทึกครั้งแรก รหัส HOI (HOB สงวน FM-BDM-07) · G10 แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- 2026-10-10 12:59 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · 17 มติ · AI-DEFAULT 11

## ขั้น 3 — declaration ร่าง
- doa_tool init (HOI · dynamic 2 ขั้น · back_to_draft) → เติมคำตัดสินต่อขั้น AI-DEFAULT: ผู้ตรวจสอบ ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ · ผู้อนุมัติ/รับทราบ รับทราบผลการรับมอบ/ไม่รับทราบ (ไม่ใช้ "ส่งกลับแก้ไข") · role_notes · validate PASS
- ntf: hoi_cancelled + hoi_acknowledged_open_items (รับทราบแล้วแต่ยังมีเอกสารค้าง → แจ้งผู้จัดทำ) · ตัด over_limit (review) · PASS
- doccfg HOI (ไม่ชน registry · HOB สงวน FM-BDM-07) PASS · mdoc WARN (G04 taxonomy รออนุมัติ · G09 doa pending) BLOCK 0 · doa validate --print-config PASS

## ขั้น 4 — แบบพิมพ์ Replica (R9 ตารางกรอบ · R10 2 หน้า)
- 2 หน้า: หน้า 1 หัว+ข้อมูลแบบฟอร์ม+ข้อมูลการรับมอบ+ผลการตรวจรับ 12 แถว · หน้า 2 ผลการตรวจรับต่อ+ประเด็นค้าง+ลงชื่อ+ประวัติ · ฟอนต์ 8pt · thead ซ้ำ · หน้า N/2
- parity IDENTICAL 5/5 · ไม่มี {{}} หลง · missing keys 0 · data สมมติทั้งหมด (make_data.py)
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py เรียก render_pdf → ทำเฉพาะ render_doc + build_html ได้ out/*.html + FM-BDM-08_template.html)
- verify-only: Chromium บน cloud container render 5 สถานะ = 2 หน้าทุกสถานะ · ดูภาพหน้า 1/2 แล้ว (ไม่ล้น · ลงชื่อ 7 แถวไม่ตัดหน้า) · PDF/ภาพไม่ส่งเข้า DevPack
- [NO-BROWSER] ข้าม compare_original.py บนเครื่อง user — รันใน container (verify): approved vs ต้นฉบับ 0.434 WARN (region 0:0.6 = 0.379) — อธิบายใน print-spec §7
- 2026-10-10 13:03 · ขั้น 4 → done · parity 5/5 · 2 หน้าทุกสถานะ (verify container) · compare 0.434 WARN อธิบายแล้ว · NO-BROWSER ไม่มี PDF
- 2026-10-10 13:03 · ขั้น 3 → done · doa PASS · ntf PASS · doccfg HOI PASS · mdoc WARN(BLOCK 0)

## ขั้น 5 — HTML Q-form (html-generator v9.4)
- ฐาน: shell/CSS/framework จาก DevPack ที่ผ่านแล้วแผนกเดียวกัน (J006 FM-BDM-06 · Q-form v9.4) + เขียน domain script ใหม่ตาม FORM_SPEC 1:1 · เทียบ GOLDEN_SKELETON + U1–U28 ก่อน build
- wizard 3 ขั้น: ข้อมูลการรับมอบและผลการตรวจรับ (6 ช่อง + ตาราง 7 ช่อง · Rule #107) › ประเด็นค้างและการติดตาม (+ เอกสารแนบ) › ตรวจสอบและยืนยัน · DEC-12 บล็อก "รับมอบครบถ้วน" เมื่อมีแถวไม่ผ่าน · DEC-13/14/15/16 ตรวจในขั้น 1–2 · เวลารับมอบเป็นช่องข้อความ HH:MM (ไม่ใช้ช่องวันที่/เวลาเบราว์เซอร์ · วันที่ใช้ bedateHTML)
- audit FAIL 0 · WARN 3 (skeleton เดิม: ss-caret/empty-icon ไม่มี w- · .uc-email · font-size px) · prune_css ตัด 0.1 KB
- [NO-BROWSER] ข้าม e2e_standard.py บนเครื่อง user — verify บน cloud container (Chromium): 21/21 ผ่าน · smoke flow สร้าง→ตรวจกฎ DEC-12/13/14/16→ส่ง→ตรวจสอบแล้ว→รับทราบ ไม่มี pageerror (ผลเก็บ .build/ ไม่ใส่ชุด) · [NO-BROWSER] ข้าม render-check.py
- meta cube-archetype=Q-form ✓ · window.__QA__ ✓
- U1 ✓ (ไม่มี stat cards · badge ใน sub) U2 ✓ U3 ✓ U4 ✓ U5 ✓ kebab U6 ✓ page-size 25 U7 ✓ U8 ✓ U9 ✓ U10 ✓ U11 ✓ U12 ✓ U13 ✓ U14 ✓ wizard 1290 U15 ✓ U16 n/a (ไม่มีลบ) U17 ✓ คน=icon วงกลม U18 ✓ (ชื่อโครงการ ellipsis) U19 ✓ (sub 2 fact) U20 n/a U21 ~ (font-size skeleton เดิม) U22 ✓ U23 ✓ U24 ✓ search-select U25 ✓ backdrop onmousedown U26–U28 n/a
- 2026-10-10 13:14 · ขั้น 5 → done · audit FAIL 0 · e2e 21/21 (container) · U1–U28 ✓
- 2026-10-10 13:14 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-008.md (+.docx) Prebrief Mode · Quality Gate C1–C20 → APPROVED (C16 WARN ไม่มี registry ตรง — feature ใหม่)
- FRD_F-TMP-008_Pack 00–07 + INDEX + declarations/ · 07 §7.0 สร้างจาก DECISIONS.lock ตรงตัว · frd_lint รอบ 1: BLOCK 0 · WARN 0 · PASS 12
- frd_ref ใส่ตาม lint: doccfg FN-03/FN-05 · ntf FN-07/FN-09 · doccfg --final --registry PASS (HOI ไม่ชน) · ntf --final PASS · doa validate --print-config PASS · mdoc WARN (G04 taxonomy · G09 doa pending) BLOCK 0
- 2026-10-10 13:20 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · declaration --final PASS

## ขั้น 8 — UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-008.md (AS-BUILT) จาก inventory · brief_check รอบ 1 PASS · FAIL 0 · WARN 0
- testcases-F-TMP-008.md 30 เคส / 65 step · tc_lint รอบ 1 ERROR 1 (TC-V07 step ไม่ขึ้นต้น verb) → แก้ · รอบ 2 ERROR 0
- [NO-BROWSER] ข้าม verify_anchors.py บนเครื่อง user — verify บน cloud container: DOM 103 · SOURCE 35 · MISSING 0 (ผลไม่ใส่ชุด)
- cases.json (Lite) 26 เคส / 56 step · QA_AUDIT drop ledger 4 · lite_audit หายเงียบ 0 · stamp แล้ว · testcase-F-TMP-008.html build (ไม่มีภาพ — [NO-BROWSER] ข้าม capture.py)
- 2026-10-10 13:25 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 · anchors MISSING 0 (container) · lite_audit หายเงียบ 0
