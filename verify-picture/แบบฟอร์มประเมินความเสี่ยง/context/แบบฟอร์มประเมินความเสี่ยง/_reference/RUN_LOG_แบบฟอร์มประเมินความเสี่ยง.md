# RUN_LOG — F-TMP-002 FM-BDM-02 แบบฟอร์มประเมินความเสี่ยง (REQ-TMP-002)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: `_system/tools/to_image.py` (LibreOffice → PDF → page-1.png) จาก .xlsx — ไม่ใช่สแกนกระดาษจริง · ถ้อยคำยึด content.html + openpyxl (data validation 4 รายการ · สูตร G=E×F · footer Doc. No./Rev.)
- ไม่มี PREBRIEF จาก CMS → PREBRIEF v2 สร้างจาก FORM_SPEC
- impact_summary.py: regex รับเฉพาะ REQ-ตัวเลข → รันบนสำเนาชั่วคราว REQ-0000-002 แล้วแทนกลับเป็น REQ-TMP-002 (ไม่แก้สกิล)
- form_spec_check: ERROR 0 · WARN 0 · ข้อมูลขัดกัน 5 (คะแนนคงเหลือมี 7 · คงเหลือ > ก่อนควบคุม · 0 ในแถวว่าง · ไม่มีช่องโครงการ · ไม่มีคอลัมน์ระดับ)
- ไม่มีข้อมูลส่วนบุคคลในไฟล์ (ฟอร์มเปล่า)
- 2026-10-10 08:38 · ขั้น 1 → done · form_spec_check ERROR 0 · 10 ช่อง · 18 แถว · ลายเซ็น 3

## ขั้น 2 — gate AI-DEFAULT (unattended-policy)
- G1 ไม่เปลี่ยนค่า/ไม่ส่งต่อ — ทะเบียนความเสี่ยงเก็บในเอกสารนี้เท่านั้น
- G2 dynamic 2 ขั้นตามช่องลงชื่อ: ผู้ตรวจสอบ (ผู้จัดการฝ่ายพัฒนาธุรกิจ) → role-line-manager · ผู้อนุมัติ/รับทราบ (รองกรรมการผู้จัดการ/กรรมการผู้จัดการ) → role-gm (ไม่มี role ตรงใน master → แจ้งรายงาน) · ไม่มีวงเงิน
- G3 เกณฑ์/ช่วงระดับ/ประเภท อ่านจาก RiskMatrix config · คะแนน = โอกาส×ผลกระทบ · ตัด 7 จากคะแนนคงเหลือ · คงเหลือ>ก่อนควบคุม = เตือน
- G4 ไม่จำกัด (PDF ≥18 แถว) · G5 1:1 · G6 แถวล่างต่อขั้น ข้อความในระบบ · G7 กลับร่าง · G8 เจ้าของ/ผู้อนุมัติหลังส่ง/admin · G9 ออกเลขบันทึกครั้งแรก รหัส RSK · G10 แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock พร้อมเริ่มทำ · 16 มติ · AI-DEFAULT 11 · VALID 5
- 2026-10-10 08:39 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · 16 มติ · AI-DEFAULT 11

## ขั้น 3 — declaration ร่าง
- doa_tool: init → BLOCK G5 (decisions on_reject: draft) → แก้ decisions.yaml เป็น back_to_draft → lock ใหม่ + tag → PASS · เติมคำตัดสินต่อขั้น (ตรวจสอบแล้ว/ส่งกลับแก้ไข · อนุมัติ / รับทราบ/ส่งกลับแก้ไข) AI-DEFAULT · validate --print-config PASS (G8/G9)
- ntf: rsk_cancelled + rsk_very_high_approved (คะแนน ≥17 → in-app+email) · ตัด over_limit (review) · BLOCK 0
- doccfg RSK (ไม่ชน registry · J001 ใช้ PJI) PASS · mdoc WARN (G04 taxonomy รออนุมัติ · G09 doa pending) BLOCK 0

## ขั้น 4 — แบบพิมพ์ Replica (R9 ตารางกรอบ · R10 2 หน้า)
- 2 หน้า: หน้า 1 หัว+ข้อมูล+เกณฑ์+ทะเบียน 14 แถว · หน้า 2 ทะเบียนต่อ+สรุประดับ+ลงชื่อ+ประวัติ · ฟอนต์ 8pt · thead ซ้ำ · หน้า N/2
- parity IDENTICAL 5/5 · ไม่มี {{}} หลง · missing keys 0
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py เรียก render_pdf → ทำเฉพาะ render_doc + build_html ได้ out/*.html)
- verify-only: Chromium บน cloud container render 5 สถานะ = 2 หน้าทุกสถานะ · ภาพ _states_sheet(.png/_p2.png) ดูแล้ว (ไม่ล้น · ลายเซ็นครบตาม signs) · PDF ไม่ส่งเข้า DevPack
- compare_original (container) approved vs ต้นฉบับ region 0:0.6 = 0.226 WARN — อธิบายใน print-spec §7 (ต้นฉบับ Excel ย่อ 1 หน้า vs ระบบ 2 หน้า 8pt)
- 2026-10-10 08:46 · ขั้น 4 → done · parity 5/5 · 2 หน้าทุกสถานะ (verify container) · compare 0.226 WARN อธิบายแล้ว · NO-BROWSER ไม่มี PDF
- 2026-10-10 08:46 · ขั้น 3 → done · doa PASS · ntf PASS · doccfg RSK PASS · mdoc WARN(BLOCK 0)

## ขั้น 5 — HTML Q-form (html-generator v9.4)
- ฐาน: archetype Q-form จาก DevPack ตัวอย่าง F-FIN-ACL (generic ลอกตรง) + ปรับ domain ตาม FORM_SPEC 1:1 · เทียบ GOLDEN_SKELETON + U1–U28 ก่อน build
- คำตัดสินเปลี่ยนเป็น ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ · อนุมัติ / รับทราบ/ไม่อนุมัติ (เดิม "ส่งกลับแก้ไข" ชนกับปุ่มแก้ไขใน e2e S5) → แก้ print_config + RSK.doa.yaml + data ใหม่ · parity 5/5 · doa validate PASS · doccfg PASS
- ทะเบียนความเสี่ยง 9 ช่อง/แถว → ตาราง (Rule #107 >4 ช่อง) ใช้ความกว้างเต็ม drawer · การ์ดสรุปเป็นแถบบนตาราง (ไม่ใช่การ์ดข้างขวา — ตารางกว้างไม่พอ)
- audit.sh FAIL 0 · WARN 3 (skeleton เดิม: ss-caret/empty-icon ไม่มี w- · .uc-email · font-size px) · prune_css ตัด 3.6 KB → audit ซ้ำ FAIL 0
- [NO-BROWSER] ข้าม e2e_standard.py บนเครื่อง user — verify บน cloud container (Chromium): 21/21 ผ่าน (reports/e2e_report.json) · render-check.py ข้าม
- meta cube-archetype=Q-form ✓ · window.__QA__ ✓
- U1 ✓ (ไม่มี stat cards · badge ใน sub) U2 ✓ U3 ✓ U4 ✓ U5 ✓ kebab U6 ✓ page-size 25 U7 ✓ U8 ✓ U9 ✓ U10 ✓ U11 ✓ U12 ✓ U13 ✓ U14 ✓ wizard 1290 U15 ✓ U16 n/a (ไม่มีลบ) U17 ✓ คน=icon วงกลม U18 ✓ U19 ✓ U20 n/a (ชุดเดียว) U21 ~ (font-size skeleton เดิม) U22 ✓ U23 ✓ U24 ✓ search-select U25 ✓ backdrop onmousedown U26–U28 n/a (ไม่มีหน้าตั้งค่า)
- 2026-10-10 08:59 · ขั้น 5 → done · audit FAIL 0 · e2e 21/21 (container) · U1–U28 ✓
- 2026-10-10 08:59 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-002.md (+.docx) Prebrief Mode · Quality Gate C1–C20 → APPROVED (C16 WARN ไม่มี registry ตรง — feature ใหม่)
- FRD_F-TMP-002_Pack 00–07 + INDEX + declarations/ · frd_lint รอบ 1: BLOCK 0 · WARN 1 (N3 จับ "15" ใน DEC-15/OQ-05 = false positive → ปรับถ้อยคำ 05) · รอบ 2: BLOCK 0 · WARN 0 · PASS 15
- frd_ref ใส่ตาม lint: doccfg FN-03/FN-05 · ntf FN-07/FN-09 · doccfg --final PASS (registry ไม่ชน · RSK) · ntf --final PASS · doa PASS · mdoc WARN (G04 taxonomy · G09 doa pending) BLOCK 0
- 2026-10-10 09:05 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · declaration --final PASS

## ขั้น 8 — UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-002.md (AS-BUILT) จาก inventory · brief_check PASS · FAIL 0 · WARN 0
- testcases-F-TMP-002.md 30 เคส / 65 step · tc_lint รอบ 1 ERROR 2 (step simulate ไม่ขึ้นต้น verb) → แก้ → ERROR 0
- [NO-BROWSER] ข้าม verify_anchors.py บนเครื่อง user — verify บน cloud container: รอบ 1 MISSING 2 (หัว modal ที่ประกอบจากโค้ด) → เปลี่ยน anchor → DOM 88 · SOURCE 23 · MISSING 0 (reports/anchors.json)
- HTML แก้ microcopy: หัว modal อนุมัติ "ยืนยัน {คำ}?" · toast ขั้นกลาง "ส่งต่อขั้นถัดไปแล้ว ·" (เดิมได้ "ตรวจสอบแล้วแล้ว") → audit FAIL 0 · e2e 21/21 (container)
- cases.json (Lite) 24 เคส · QA_AUDIT drop ledger 6 · lite_audit หายเงียบ 0 · stamp แล้ว · testcase-F-TMP-002.html build (ไม่มีภาพ — [NO-BROWSER] ข้าม capture.py)
- 2026-10-10 09:11 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 · anchors MISSING 0 (container) · lite_audit หายเงียบ 0
- ขั้น 9: K2 BLOCK — orig/content.html (ผลแตกข้อความจาก to_image) ถูกนับเป็น prototype ซ้ำ → ย้ายไป orig/out/content.html (สแกนข้าม out/)

## ขั้น 9 — ตรวจรวม + แพ็ก
- manifest_scan 48 artifact · consistency_check READY · BLOCK 0 · WARN 1 (K9 compare 0.226 — อธิบายใน print-spec §7)
- dm.sh pack J002 → _pack/F-TMP-002_DevPack.zip · [NO-BROWSER] ไม่มี PDF แบบพิมพ์ในชุด → ส่งแบบมีเงื่อนไข (ต้องรัน render_states/e2e/verify_anchors/capture บนเครื่องที่มี browser)
- 2026-10-10 09:13 · ขั้น 9 → done · consistency READY · BLOCK 0 · zip _pack/F-TMP-002_DevPack.zip
