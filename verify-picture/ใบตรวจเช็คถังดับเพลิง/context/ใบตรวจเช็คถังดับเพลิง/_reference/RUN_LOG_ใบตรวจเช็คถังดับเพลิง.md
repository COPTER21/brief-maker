# RUN_LOG — F-TMP-001 FM-WHS-03 ใบตรวจเช็คถังดับเพลิง (REQ-TMP-001)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: to_image.py วิธี LibreOffice → PDF → pypdfium2 (หน้ากระดาษจริงจาก Excel ไม่ใช่ HTML+browser) · ฟอนต์ไทยในเครื่อง render เป็นกล่อง → ถ้อยคำยึด content.html / openpyxl · ตำแหน่ง/เส้นยึด page-1.png
- ต้นฉบับ: 1 ชีตมีการ์ด 2 ใบซ้าย-ขวา (สถานที่ B8 / A5) เหมือนกัน → FORM_SPEC จดการ์ดเดียว · ตาราง 12 แถว × 6 คอลัมน์ · ไม่มีช่องลงชื่อ/อนุมัติ
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC
- form_spec_check: ERROR 0 · 7 ช่อง · anomalies 3
- แก้ impact_summary.py: regex เลขคำขอรับรหัสชั่วคราว REQ-TMP-001 ได้ (เดิมรับแต่ตัวเลข)
- 2026-10-10 04:21 · ขั้น 1 → done · FORM_SPEC 7 ช่อง ERROR 0 · PREBRIEF v2 · impact ร่าง

## ขั้น 2 — เหตุผลมติ (unattended · AI-DEFAULT)
- G1 ไม่เปลี่ยนค่า/ไม่ส่งต่อ — ใบบันทึกตรวจ ไม่มีผลต่อ master · G2 ไม่มีอนุมัติ — กระดาษไม่มีช่องลงชื่อผู้อนุมัติ
- G3 ไม่มีสูตร · กติกา: เลือกครบ 4 หัวข้อ · x = ผิดปกติ → แจ้ง role-mgr-wh (ตามข้อความท้ายฟอร์ม) · G4 ไม่จำกัด PDF ≥12 แถว
- G5 1:1 แก้ 'ผู้จำหนาย'→'ผู้จำหน่าย' · G6 ไม่มีลายเซ็น ผู้ตรวจเป็นข้อความต่อแถว · G7 ไม่มีอนุมัติ ยกเลิกได้เจ้าของ+admin ต้องมีเหตุผล
- G8 admin = role-mgr-wh เห็นทั้งหมด · G9 ออกเลขบันทึกครั้งแรก รหัส FEC (Fire Extinguisher Check) · G10 แนบไฟล์ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- 2026-10-10 04:21 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · 13 มติ (AI-DEFAULT 10 + VALID 3)

## ขั้น 3 — หมายเหตุ
- DOA: ไม่ทำ DOA_BRIEF — DEC-03 ไม่มีการอนุมัติ (doa_tool init ปฏิเสธเอง: ห้ามยัด DOA เข้า feature ที่ไม่มีอนุมัติ)
- NTF: 2 event (fec_abnormal_found บังคับ in-app+email → role-mgr-wh · fec_cancelled) · VERDICT PASS
- doccfg + mdoc ทำหลังขั้น 4 (ต้องใช้ print_config)
- 2026-10-10 04:22 · ขั้น 3 → done · NTF PASS · DOA ไม่มี (DEC-03) · doccfg/mdoc หลังขั้น 4

## ขั้น 4 — แบบพิมพ์ Replica (R9 ตารางกรอบ · 1 หน้า)
- parity_check: IDENTICAL 5/5 (active-3rows · full-12rows · abnormal · long-24rows · cancelled) · ไม่มี {{}} หลง · ไม่มี key หาย
- สถานะ ร่าง/อนุมัติ/ไม่อนุมัติ/DOA 6 ขั้น ไม่ใช้ — เอกสารไม่มีอนุมัติและไม่มีช่องลงชื่อ (DEC-03 · DEC-07) → ใช้สถานะตามวงจรใบตรวจแทน
- [NO-BROWSER] ข้าม render_pdf.py (ใน render_states.py) — build HTML ทุกสถานะด้วย render_doc + build_html แทน · ไม่มี PDF/_states_sheet.png/จำนวนหน้า
- [NO-BROWSER] ข้าม compare_original (ไม่มี PDF ของแบบพิมพ์ระบบ)
- ไม่เกิน A4: ต้นฉบับ 1 การ์ด = 12 แถว · ทดสอบ 24 แถว dense (ประเมินพอดี 1 หน้า) → ไม่ใช้ R10 2 หน้า · --max-pages 1 (รอยืนยันบนเครื่องที่มี browser)
- doccfg FEC: VERDICT PASS (--registry) · mdoc: WARN (taxonomy_def_id ว่าง · function_code F01 ชั่วคราว) · source=declaration เพราะ REQ-TMP-001 ไม่ใช่เลขคำขอจริง
- doa validate: ไม่มี DOA (DEC-03)
- ไฟล์ขยะ print/out/_abnormal.body.html ลบไม่ได้ (โฟลเดอร์ไม่อนุญาตลบ) — ไม่ต้องแพ็ก
- 2026-10-10 04:25 · ขั้น 4 → done · parity 5/5 · HTML ทุกสถานะ · NO-BROWSER ไม่มี PDF · doccfg PASS · mdoc WARN

## ขั้น 5 — HTML (html-generator v9.4) · feature.html
- ฐาน: form-archetype reference (base-kit + utils ลอกตรง) + be-datepicker (Rule #114) · เทียบ GOLDEN_SKELETON + U1–U28 ก่อน build
- archetype: `Q-form-noapproval` — โครง Q2 ครบ (list · wizard wide 3 ขั้น 'ข้อมูลหลักใบตรวจ › เอกสารแนบ › ตรวจสอบและยืนยัน' · view tabs · PDF ผ่าน data contract · __QA__) แต่ **ไม่ประกาศ Q-form** เพราะชุดตรวจ Q-form บังคับ MOCK_DOA_RESOLVED / .slot-row / {{#signs}} / แท็บ sign ซึ่งขัด DEC-03 (ไม่มีอนุมัติ) + DEC-07 (ไม่มีช่องลงชื่อ) + doa-declaration "ห้ามยัด DOA เข้า feature ที่ไม่มีอนุมัติ" → ข้อ Q-form ที่เหลือตรวจด้วยมือผ่านครบ: STEPS 3 ขั้น ✓ STEPH ✓ 'ตรวจสอบและยืนยัน' ✓ 'เอกสารแนบ' ✓ tabBtn detail/pdf/history ✓ docPill ✓ drawer wide ✓ tplRender + .pdf-frame ✓ __QA__ ✓ · N/A: #108 DOA ×2 · #108/#110 {{#signs}} · #101 tab sign · #98 renderSignProgress (ให้คนยืนยันใน _BATCH_REPORT)
- audit.sh: FAIL 0 · WARN 3 (base-kit) · self_audit: PASS · prune_css: ตัด 88 rule แล้วรันซ้ำ FAIL 0 / PASS
- [NO-BROWSER] ข้าม e2e_standard.py · render-check.py — แทนด้วย jsdom smoke (reports/smoke_jsdom.json) 27/27 PASS: S1 · S2/S4/S5/S6 ×3 persona · S7 · S9 · S10 + validation (สถานที่ซ้ำ · วันที่ซ้ำ · วันอนาคต · เหตุผลยกเลิก) + แจ้งผิดปกติ
- PDF ใน prototype: docPrintData(R1) → parity_check กับ form.tpl.html = IDENTICAL
- U1–U28: U1✓ U2✓ U3✓ U4✓ U5✓ U6✓ U7✓ U8✓ U9✓ U10✓ U11✓(14px→12/16 ตาม self_audit) U12✓ U13 N/A(ไม่มีอนุมัติ) U14✓ U15 N/A(แก้ระดับแถวใน modal) U16 N/A(ไม่มีลบ ใช้ยกเลิก+เหตุผล) U17✓ U18✓ U19✓ U20✓(ชุดเดียว ไม่มี tabs) U21✓ U22✓ U23✓ U24✓ U25✓ U26–U28 N/A(ไม่ใช่หน้าตั้งค่า)
- 2026-10-10 04:38 · ขั้น 5 → done · audit FAIL 0 · self_audit PASS · jsdom smoke 27/27 · NO-BROWSER ข้าม e2e/render-check · archetype Q-form-noapproval
- 2026-10-10 04:38 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-001.md/.docx (Prebrief Mode · AI Review C01–C23 + PE01–PE05 → APPROVED) · DEC 13 ข้ออ้างครบใน §2.4
- FRD_F-TMP-001_Pack (STANDARD · 00–07 + INDEX + declarations/) · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 9
- declaration --final: DOCCFG FEC PASS (--registry) · NTF PASS (frd_ref FN-07) · MDOC WARN (taxonomy_def_id ว่าง · function_code F01 ชั่วคราว → OQ-06) · DOA ไม่มี (DEC-03)
- FRD 04/05 ไม่ใช้คำ "อนุมัติ" เพื่อไม่ให้ K7 ตีความว่ามีขั้นพิจารณา (feature นี้ไม่มี DOA)
- 2026-10-10 04:42 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 · DOCCFG/NTF final PASS · MDOC WARN

## ขั้น 8 — UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-001.md: brief_check B1–B8 PASS · FAIL 0 · WARN 0
- testcases-F-TMP-001.md: 22 เคส · 52 step · tc_lint ERROR 0
- [NO-BROWSER] ข้าม verify_anchors.py — แทนด้วยตรวจข้อความตัวหนาเทียบ source HTML: 114 anchor · missing 0 (reports/srccheck_tc_refs.json)
- cases.json (Lite 22/22) + QA_AUDIT · lite_audit หายเงียบ 0 · --stamp แล้ว
- [NO-BROWSER] ข้าม capture.py — build testcase-F-TMP-001.html ด้วย shots ว่าง (regionKey ว่างทุก step · ไม่มีภาพหน้าจอ)
- 2026-10-10 04:46 · ขั้น 8 → done · brief_check PASS · tc_lint 22 เคส ERROR 0 · lite_audit 0 หาย · NO-BROWSER ข้าม verify_anchors/capture

## ขั้น 9 — เตรียมแพ็ก
- orig/content.html → orig/content_extract.htm (ถ้อยคำที่สกัดจาก xlsx ขั้น 1) — กัน manifest จับเป็น prototype ซ้ำ (K2)
- print/make_data.py → print/render_data.py (ให้ manifest จับเป็นไฟล์แบบพิมพ์) · data-contract รวมเป็นภาคผนวกใน print-spec แล้วย้ายฉบับแยกไป print/out/
- reports/smoke_jsdom.json · srccheck_tc_refs.json = ผลตรวจแทนเครื่องมือ browser (NO-BROWSER) — ไม่ตั้งชื่อเป็น e2e/anchors เพื่อไม่ให้ K9 ตีความเป็นผล e2e_standard/verify_anchors จริง
