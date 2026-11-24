# RUN_LOG — F-TMP-007 FM-BDM-07 แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายพัฒนาธุรกิจจัดเก็บ) (REQ-TMP-007)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: `_system/tools/to_image.py` (LibreOffice → PDF → page-1.png) จาก .xlsx — ไม่ใช่สแกนกระดาษจริง · ฟอนต์ไทยในภาพไม่แสดง (ใช้ตำแหน่ง/เส้นเท่านั้น) · ถ้อยคำยึด content.html + openpyxl (data validation · footer Doc. No./Rev.) · content.html ย้ายไป orig/out/ แล้ว
- form.title = "แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายพัฒนาธุรกิจจัดเก็บ)" ตามหัวฟอร์ม — คงวงเล็บไว้เพื่อแยกจาก FM-BDM-08 · ชื่อไฟล์ไม่เพี้ยน → ไม่ต้อง rename
- ไม่มี PREBRIEF จาก CMS → PREBRIEF v2 สร้างจาก FORM_SPEC (แบบ 1 · Standalone · --module BDM)
- impact_summary.py: regex รับเฉพาะ REQ-ตัวเลข → รันบนสำเนา .build/REQ-0000-007 แล้วแทนกลับเป็น REQ-TMP-007 (ไม่แก้สกิล)
- form_spec_check: ERROR 0 · WARN 0 · 18 ช่อง · แถวซ้ำ 1 กลุ่ม (รายการเอกสาร 12) · ลายเซ็น 3 · ข้อมูลขัดกัน 5 (DV 1–5 ค้างที่ C13:C18 · สถานะข้อมูลสมบูรณ์ทั้งที่ขาดเอกสาร · มีข้อจำกัดแต่ไม่กรอกข้อจำกัด · ผู้รับมอบบันทึก 2 ที่ · วันที่เอกสารหลังวันส่งมอบ)
- ไม่มีข้อมูลส่วนบุคคลในไฟล์ (ฟอร์มเปล่า)
- 2026-10-10 12:58 · ขั้น 1 → done · form_spec_check ERROR 0 · 18 ช่อง · 1 กลุ่มแถวซ้ำ · ลายเซ็น 3

## ขั้น 2 — gate AI-DEFAULT (unattended-policy)
- G1 ไม่เปลี่ยนค่า/ไม่ส่งต่อ — ชุดเอกสารส่งมอบเก็บที่ฝ่ายพัฒนาธุรกิจ (เอกสารในชุดผู้ใช้กรอกชื่อ/รหัส/ลิงก์เอง)
- G2 dynamic 2 ขั้นตามช่องลงชื่อ: ผู้ตรวจสอบ (ผู้จัดการฝ่ายพัฒนาธุรกิจ) → role-line-manager · ผู้อนุมัติ/รับทราบ (ฝ่ายบริหารการลงทุนเป็นผู้รับมอบ) → role-mgr-bu (ไม่มี role ฝ่ายบริหารการลงทุนใน contract → แจ้งรายงาน) · ไม่มีวงเงิน
- G3 สถานะข้อมูล/สถานะเอกสารอ่านจาก HandoverPackageConfig · ตัด DV 1–5 ค้าง · สมบูรณ์แต่ขาดเอกสาร = เตือน · มีข้อจำกัด → ต้องกรอกข้อจำกัดของข้อมูล · วันที่เอกสารหลังวันส่งมอบ = เตือน
- G4 ไม่จำกัด (PDF ≥12 แถว) · G5 1:1 · G6 แถวล่างต่อขั้น ข้อความในระบบ · G7 back_to_draft · G8 เจ้าของ/ผู้อนุมัติหลังส่ง/admin · G9 ออกเลขบันทึกครั้งแรก รหัส HOB (HOI สงวนให้ FM-BDM-08) · G10 แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- impact_summary --decisions: รันผ่านสำเนา REQ-0000-007 แล้วแทนกลับ
- 2026-10-10 12:59 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · 16 มติ · AI-DEFAULT 11

## ขั้น 3 — declaration ร่าง
- doa_tool init (HOB · dynamic 2 ขั้น · back_to_draft) → เติมคำตัดสินต่อขั้น AI-DEFAULT: ผู้ตรวจสอบ ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ · ผู้อนุมัติ/รับทราบ รับมอบ / รับทราบ/ไม่รับมอบ (ไม่ใช้ "ส่งกลับแก้ไข") · role_notes · validate PASS
- ntf: hob_cancelled + hob_received_with_gaps (รับมอบแล้วยังขาดเอกสาร/มีข้อจำกัด → แจ้งผู้จัดทำ) · ตัด over_limit (review) · BLOCK 0
- doccfg HOB (--registry ไม่ชน · HOI สงวน FM-BDM-08) PASS · mdoc WARN (G04 taxonomy รออนุมัติ · G09 doa pending) BLOCK 0 · doa validate --print-config PASS

## ขั้น 4 — แบบพิมพ์ Replica (R9 ตารางกรอบ · R10 2 หน้า)
- 2 หน้า: หน้า 1 หัว+ข้อมูลแบบฟอร์ม+ข้อมูลการส่งมอบ+รายการเอกสาร 14 แถว · หน้า 2 รายการต่อ+สมมติฐาน/ประเด็นค้าง/ข้อจำกัด+ลงชื่อ+ประวัติ · ฟอนต์ 8pt · thead ซ้ำ · หน้า N/2
- parity IDENTICAL 5/5 · ไม่มี {{}} หลง · missing keys 0
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py เรียก render_pdf → ทำเฉพาะ render_doc + build_html ได้ out/*.html)
- verify-only: Chromium บน cloud container render 5 สถานะ = 2 หน้าทุกสถานะ · ดูภาพ approved/long-24rows หน้า 1–2 แล้ว · PDF/ภาพไม่ส่งเข้า DevPack
- [NO-BROWSER] ข้าม compare_original.py — ไม่มีคะแนนเทียบต้นฉบับ (บันทึกใน print-spec §7)
- 2026-10-10 13:02 · ขั้น 4 → done · parity 5/5 · 2 หน้าทุกสถานะ (verify container) · NO-BROWSER ไม่มี PDF/compare
- 2026-10-10 13:02 · ขั้น 3 → done · doa PASS · ntf PASS · doccfg HOB PASS · mdoc WARN(BLOCK 0)
- 2026-10-10 · ขั้น 4 → done · ขั้น 3 → done (doccfg/mdoc หลังแบบพิมพ์)

## ขั้น 5 — HTML Q-form (html-generator v9.4)
- ฐาน: shell/CSS/framework จาก DevPack ที่ผ่านแล้วแผนกเดียวกัน (J006 FM-BDM-06 · Q-form v9.4) + เขียน domain script ใหม่ตาม FORM_SPEC 1:1 (.build/hob_a1–a9.js + assemble.py) · เทียบ GOLDEN_SKELETON + U1–U28 ก่อน build
- wizard 3 ขั้น: ข้อมูลการส่งมอบและรายการเอกสาร (ตาราง 7 ช่อง · Rule #107) › สมมติฐาน ข้อจำกัด และเอกสารแนบ › ตรวจสอบและยืนยัน · DEC-13/16 เตือน · DEC-14 บังคับข้อจำกัดของข้อมูล · DEC-15 ผู้รับมอบ = ค่าเริ่มขั้นรับทราบ
- node --check 4 script ผ่าน · audit FAIL 0 · WARN 3 (skeleton เดิม: ss-caret/empty-icon ไม่มี w- · .uc-email · font-size px) · prune_css ตัด 0 KB
- [NO-BROWSER] ข้าม e2e_standard.py บนเครื่อง user — verify บน cloud container (Chromium): 21/21 ผ่าน · smoke flow สร้าง→ส่ง→ตรวจสอบ→รับมอบ ไม่มี pageerror (ผลไม่ใส่ชุด) · [NO-BROWSER] ข้าม render-check.py
- meta cube-archetype=Q-form ✓ · window.__QA__ ✓
- U1 ✓ (ไม่มี stat cards · badge ใน sub) U2 ✓ U3 ✓ U4 ✓ U5 ✓ kebab U6 ✓ page-size 25 U7 ✓ U8 ✓ U9 ✓ U10 ✓ U11 ✓ U12 ✓ U13 ✓ U14 ✓ wizard 1290 U15 ✓ U16 n/a (ไม่มีลบ) U17 ✓ คน=icon วงกลม U18 ✓ (ชื่อโครงการ ellipsis) U19 ✓ U20 n/a (ชุดเดียว) U21 ~ (font-size skeleton เดิม) U22 ✓ U23 ✓ U24 ✓ search-select ผู้ส่งมอบ/ผู้รับมอบ U25 ✓ backdrop onmousedown U26–U28 n/a (ไม่มีหน้าตั้งค่า)
- 2026-10-10 13:14 · ขั้น 5 → done · audit FAIL 0 · e2e 21/21 (container verify) · U1–U28 ✓
- 2026-10-10 13:14 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-007.md (+.docx md_to_docx) Prebrief Mode · Quality Gate C1–C20 → APPROVED (C16 WARN ไม่มี registry ตรง — feature ใหม่)
- FRD_F-TMP-007_Pack 00–07 + INDEX + declarations/ · 07 §7.0 สร้างจาก DECISIONS.lock ตรงตัว · frd_lint รอบ 1: BLOCK 0 · WARN 0 · PASS 12
- frd_ref ใส่ตาม lint: doccfg FN-03/FN-05 · ntf FN-07/FN-09 · doccfg --final --registry PASS (HOB ไม่ชน) · ntf --final PASS · doa validate --print-config PASS · mdoc WARN (G04 taxonomy · G09 doa pending) BLOCK 0
- 2026-10-10 13:19 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · declaration --final PASS
- 2026-10-10 · ขั้น 7 → done

## ขั้น 8 — UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-007.md (AS-BUILT) จาก inventory (extract_anchors) + เนื้อหา §2–§8/§10–§13 · brief_check รอบ 1 PASS · FAIL 0 · WARN 0
- testcases-F-TMP-007.md 30 เคส / 73 step · tc_lint รอบ 1 ERROR 1 (TC-E01 step ไม่ขึ้นต้น verb) → แก้ · รอบ 2 ERROR 0
- [NO-BROWSER] ข้าม verify_anchors.py บนเครื่อง user — verify บน cloud container: DOM 92 · SOURCE 27 · DATA 23 · MISSING 0 (ผลไม่ใส่ชุด)
- cases.json (Lite) 24 เคส / 62 step · QA_AUDIT drop ledger 6 · lite_audit หายเงียบ 0 · stamp แล้ว · testcase-F-TMP-007.html build (ไม่มีภาพ — [NO-BROWSER] ข้าม capture.py)
- 2026-10-10 13:25 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 · anchors MISSING 0 (container) · lite_audit หายเงียบ 0
- 2026-10-10 · ขั้น 8 → done

## ขั้น 9 — ตรวจรวม + แพ็ก
- manifest_scan · consistency_check รอบ 1 READY · WARN 2 (K4 microcopy "กรุณาเลือกผู้ส่งมอบ/ผู้รับมอบ" ใน FRD 06 → แก้เป็นข้อความจริง 2 ข้อความ · K9 ไม่มี e2e report) · รอบ 2 READY · BLOCK 0 · WARN 1 (K9 — [NO-BROWSER] e2e verify บน container เท่านั้น ไม่ใส่ผลเข้าชุด)
- dm.sh pack J007 → _pack/F-TMP-007_DevPack.zip · [NO-BROWSER] ไม่มี PDF แบบพิมพ์ในชุด → ส่งแบบมีเงื่อนไข (ต้องรัน render_states/compare_original/e2e/verify_anchors/capture บนเครื่องที่มี browser)
- 2026-10-10 13:25 · ขั้น 9 → done · consistency READY · BLOCK 0 · zip _pack/F-TMP-007_DevPack.zip
