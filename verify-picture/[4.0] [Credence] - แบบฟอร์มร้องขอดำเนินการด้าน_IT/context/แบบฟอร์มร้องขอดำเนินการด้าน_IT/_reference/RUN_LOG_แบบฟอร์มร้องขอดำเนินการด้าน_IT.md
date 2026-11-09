# RUN_LOG — F-TMP-001 FM-ITS-01 แบบฟอร์มขอรับบริการด้านเทคโนโลยีสารสนเทศ (REQ-TMP-001)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพฟอร์ม: to_image.py → LibreOffice → PDF → pypdfium2 (หน้ากระดาษจริงจาก print area ของ Excel · A4 portrait scale 85%) · เครื่องไม่มีฟอนต์ไทย → ตัวอักษรไทยในภาพเป็นกล่อง ใช้ภาพยึดตำแหน่ง/เส้น ถ้อยคำยึด content.html + sharedStrings + drawing1.xml (textbox ตัวเลือก)
- ☐ ประเภทงาน 6 ข้อ อ่านจาก Excel form control + textbox ใน drawing1.xml (ไม่อยู่ในเซลล์)
- หัวฟอร์มจริง "แบบฟอร์มร้องขอดำเนินการด้าน IT (IT Request Form)" ≠ ชื่อไฟล์ "แบบฟอร์มขอรับบริการด้านเทคโนโลยีสารสนเทศ" → form.title ยึดหัวฟอร์ม (ชื่อในคิวไม่เพี้ยน จึงไม่ rename)
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC
- แก้บั๊กสกิล impact_summary.py: regex รหัส REQ รับเฉพาะตัวเลข (REQ-[\d-]+) → อ่าน REQ-TMP-001 ไม่ได้ → เปลี่ยนเป็น REQ-[\w-]+ (ไม่กระทบด่าน)
- form_spec_check: ERROR 0 · 11 ช่อง · ลายเซ็น 3 · ข้อมูลส่วนบุคคล: ฟอร์มเปล่า ไม่มีข้อมูลตัวอย่างจริง
- 2026-10-10 07:53 · ขั้น 1 → done · FORM_SPEC 11 ช่อง ERROR 0 · PREBRIEF v2 · impact summary

## ขั้น 2 · gate (unattended — AI-DEFAULT 11 มติ + VALID 4)
- G1: ฟอร์มไม่ระบุการเปลี่ยนค่า/ส่งต่อ → config_changes [] · post_to [] (IT Support/Ticket ยังเป็น (—) ใน registry)
- G2: ช่องผู้อนุมัติบนกระดาษ 1 ช่อง "ตรวจสอบโดย" → dynamic 1 ขั้น role-line-manager · ไม่มีวงเงิน
- G3: ไม่มีสูตร/ค่าคงที่ · กติกาตรวจ = เตือน (วันที่ส่งมอบ ≥ วันที่ขอ) + อื่นๆ ต้องระบุ + เลือกประเภทงาน ≥1
- G4: ไม่มีรายการซ้ำบนกระดาษ (DEC-05 แสดง "None แถว" = ไม่เกี่ยว)
- G5: 1:1 · แก้สะกด ตําแหน่ง→ตำแหน่ง
- G6: แถวล่าง: ผู้ร้องขอ · ช่องต่อขั้น DOA (ตรวจสอบโดย) · ดำเนินการโดย (เจ้าหน้าที่ IT ผู้ปิดงาน — ไม่ใช่ขั้น DOA) · ข้อความในระบบ ไม่ใช้ภาพ
- G7: ไม่อนุมัติ → กลับร่างเลขเดิม · ยกเลิก owner+admin ใน draft/pending · เหตุผลบังคับ
- G8: เจ้าของ · ผู้อนุมัติหลังส่ง · admin role ฝ่าย IT เห็นทั้งหมด
- G9: ออกเลขตอนบันทึกครั้งแรก · รหัส ITRS (prefix "ITRS." พิมพ์บนกระดาษ — ไม่มี [CODE] ในชื่อไฟล์)
- G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- decisions_lock: พร้อมเริ่มทำ (exit 0) · dm.sh tag → AI-DEFAULT 11
- 2026-10-10 07:54 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · AI-DEFAULT 11

## ขั้น 3 · declaration ร่าง
- doa: init module=it (dept `it` ใน contract · ไม่มี module IT ใน registry 9 ตัว) · doa_type itrs · 1 ขั้น role-line-manager (ตรวจสอบโดย) → validate BLOCK G5 "on_reject ต้องเป็น back_to_draft|end" เพราะ init เขียน `draft` (บั๊ก init) → แก้ yaml เป็น back_to_draft → PASS
- ntf: เติม itrs_ready_for_it (approved → คิว IT · role-it-officer) · itrs_completed (IT ดำเนินการแล้ว → แจ้งผู้ขอ) · ตัด over_limit_approved (ไม่มีเกณฑ์วงเงิน) → PASS
- role-it-officer (เจ้าหน้าที่ IT ผู้ดำเนินการ / admin role ฝ่าย IT) ไม่มีใน doa-roles-contract → แจ้งใน _BATCH_REPORT
- doccfg + mdoc ทำหลังขั้น 4
- 2026-10-10 07:54 · ขั้น 3 → done · doa PASS · ntf PASS · doccfg/mdoc หลังขั้น 4

## ขั้น 4 · แบบพิมพ์ Replica (R9 ตารางกรอบ · 1 หน้า)
- form.tpl.html R9 + sign_rows (ผู้ร้องขอ + ขั้น DOA + ดำเนินการโดย) · profile.json · print_config.json · make_data.py → 5 สถานะ (draft · approved · rejected · long-text · approved-doa6steps 8 ช่อง 4+4)
- parity_check: IDENTICAL 5/5 · ไม่มี {{}} หลง · ไม่มี key ขาด · build_html ทุกสถานะ → print/out/*.html + ITRS_template.html
- [NO-BROWSER] ข้าม render_pdf.py (ภายใน render_states.py) — render body + build_html ทีละสถานะแทน ได้ HTML ไม่มี PDF/PNG/_states_sheet.png
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ approved.pdf)
- ตรวจภาพเบื้องต้นนอกเครื่องงาน (stage HTML ไป Chromium ใน container ของ agent · ไม่เก็บไฟล์กลับ): ทุกสถานะ 1 หน้า A4 · ลายเซ็นไม่ตัด · ฟอนต์ไม่ต่ำกว่า 8pt → ไม่เข้า R10 · ไม่ใช่ผลด่านทางการ ต้องรัน render_states --max-pages 1 บนเครื่องที่มี browser
- แก้หลังดูภาพ: ช่อง "ITRS." แสดงเลขที่เต็ม (เดิมพิมพ์ "ITRS. ITRS-2569-…" ซ้ำ) → บันทึกใน print-spec §7
- doccfg: ITRS · registry ไม่ชน (มีแค่ ACL) → PASS · mdoc: WARN G04 (ยังไม่มี taxonomy_def_id) + G09 (doa pending) — อธิบายได้ · source=declaration เพราะ REQ ชั่วคราวไม่ผ่านรูปแบบ REQ-YYYY-NNNN · module "เอกสารทั่วไป" (enum ไม่มี IT) · function_code F01 ชั่วคราว
- doa validate --print-config: PASS
- ไฟล์ค้าง print/out/_approved-doa6steps.body.html (ลบไม่ได้ — เครื่องปิดการลบ) เป็นไฟล์ชั่วคราว ไม่ใช่ผลงาน
- 2026-10-10 07:58 · ขั้น 4 → done · parity 5/5 IDENTICAL · HTML ทุกสถานะ · [NO-BROWSER] ไม่มี PDF/compare · doccfg PASS · mdoc WARN อธิบายได้
- 2026-10-10 07:58 · ขั้น 3 → done · doa PASS · ntf PASS · doccfg PASS · mdoc WARN(G04,G09)

## ขั้น 5 · HTML Q-form (html-generator v9.4)
- build: .build/build_feature.py ประกอบจาก canonical references/form-archetype (shell + BASE-KIT) + be-datepicker block + tpl_render.js (verbatim) + app ของ ITRS (build/a1–a11.js) + extra.css (Group 25) · PDF tab ฝัง print/form.tpl.html + docPrintData()
- เปิด GOLDEN_SKELETON.html + U1–U28 เทียบก่อน build: U1 ✓ (ไม่มี stat cards · badge ใน sub) · U2 ✓ · U3 ✓ · U4 ✓ · U5 ✓ kebab ⋮ · U6 ✓ page-size 10/25/50 + x–y จาก N + pager · U7 ✓ CSV ที่ head · U8 ✓ 920/1290 · U9 ✓ เหตุผลบังคับ · U10 ✓ · U11 ✓ · U12 ✓ · U13 ✓ summary+timeline+emp-chip · U14 ✓ Q-form wizard 3 ขั้น (#120 ยกเว้น Q/Q2) · U15 ✓ แก้ไข = wizard เดิม+prefill เฉพาะร่าง · U16 – (ไม่มีลบ: ยกเลิกเอกสาร = soft + เหตุผล) · U17 ✓ คน = วงกลม icon (เลิก initials ทั้ง user chip) · U18 ✓ nowrap+ellipsis · U19 ✓ header sub 1 fact (วันที่ส่งมอบ) · U20 ✓ seg tabs ทั้งหมด/รอฉันพิจารณา/คำขอของฉัน (ไม่ซ้ำแกนสถานะ) · U21 ✓ · U22 ✓ chips ≤3 ค่า 0 ซ่อน · U23 ✓ empty state · U24 ✓ search-select portal · U25 ✓ backdrop onmousedown (drawer+modal) · U26–U28 – (ไม่มีหน้าตั้งค่า)
- audit.sh: FAIL 0 · WARN 3 (มาจาก BASE-KIT ของ canonical: comment lucide · .uc-email CSS · font-size px ใน shell) · prune_css ตัด 76 rule → audit ซ้ำ FAIL 0
- [NO-BROWSER] ข้าม e2e_standard.py · ข้าม render-check.py บนเครื่องงาน
- ตรวจเบื้องต้นนอกเครื่องงาน (stage feature.html ไป Chromium ใน container ของ agent · lucide stub · ไม่เก็บไฟล์กลับ): e2e_standard 21/21 ก่อนและหลัง prune · ไม่มี pageerror — ไม่ใช่ผลด่านทางการ ต้องรันซ้ำบนเครื่องที่มี browser
- ช่องตามกระดาษ 1:1 (#106): ชื่อ-นามสกุล/ตำแหน่ง/วันที่/เลขที่ = ระบบใส่ (การ์ดสรุป) · กรอก: เรื่องที่ต้องการ · ประเภทงาน ☐6 (+อื่นๆ) · วันที่ต้องการส่งมอบ (bedateHTML) · สถานที่ส่งมอบ · รายละเอียด · เหตุผล · Spec · ไม่มีช่องเพิ่ม (หมายเหตุดำเนินการของ IT อยู่ใน modal/ประวัติ ไม่อยู่บนแบบพิมพ์)
- สถานะ: ร่าง → รออนุมัติ → รอดำเนินการ (อนุมัติแล้ว) → ดำเนินการแล้ว · ไม่อนุมัติ = กลับร่างเลขเดิม + แบนเนอร์เหตุผล · ยกเลิก (ร่าง/รออนุมัติ · เจ้าของ+admin IT)
- 2026-10-10 08:10 · ขั้น 5 → done · audit FAIL 0 · U1–U28 ✓ · [NO-BROWSER] e2e/render-check ข้าม (pre-check นอกเครื่อง 21/21)
- 2026-10-10 08:10 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-001.md/.docx (brd-generator-full v2.3 Prebrief Mode · Lane) — AI Review C01–C23 + PE01–PE05 → **APPROVED** (C16 ไม่มีรหัสใน registry = ยอมรับใน Prebrief Mode · ตัวชี้วัดไม่มีใน input → OQ-01)
- FRD_F-TMP-001_Pack (frd-generator-v6.2 Input Mode 0 · FULL variant: states=5) 00–07 + INDEX + declarations/
- frd_lint Section N: BLOCK 0 · WARN 0 · PASS 13
- declaration --final: doccfg PASS (registry ไม่ชน · frd_ref FN-02/FN-04) · ntf PASS (frd_ref FN-06/04/07) · doa PASS (--print-config) · mdoc WARN G04 (ไม่มี taxonomy_def_id) + G09 (doa pending) — อธิบายได้
- 2026-10-10 08:15 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 · declaration final PASS (mdoc WARN G04/G09)

## ขั้น 8 · UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-001.md (§0–§13 · CSS vars/microcopy สกัดจาก inventory) · brief_check: PASS · FAIL 0 · WARN 0
- testcases-F-TMP-001.md: 64 เคส / 192 step (L12 C5 V10 F3 D4 A4 T3 K3 P6 R5 E6 X3) · tc_lint ERROR 0 · Coverage Audit + Ledger (DEC 15/15 · XT 4/4)
- [NO-BROWSER] ข้าม verify_anchors.py บนเครื่องงาน · ตรวจเบื้องต้นนอกเครื่องงาน (Chromium ใน container ของ agent): DOM 315 · SOURCE 85 · PATTERN 3 · DATA 10 · MISSING 0 — ไม่ใช่ผลด่านทางการ
- UAT (qa-friendly v3.1 Lite): cases.json 54 เคส · drop ledger 10 (คำสั่งหลังบ้าน/จำลอง/แจ้งเตือนจริง) · lite_audit หายเงียบ 0 + stamp md5 · build testcase-F-TMP-001.html
- [NO-BROWSER] ข้าม capture.py → ไม่มีภาพหน้าจอ (regionKey ว่างทุก step · shots_b64.json = {})
- 2026-10-10 08:22 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 (64 เคส) · lite_audit หายเงียบ 0 · [NO-BROWSER] verify_anchors/capture ข้าม

## ขั้น 9 · ตรวจรวม + แพ็ก
- ย้ายไฟล์ช่วย build ไป .build/ (ซ่อนจาก manifest) · orig/content.html → orig/out/ (กันชน artifact prototype)
- manifest_scan: 39 artifact · ซ้ำ 0 · จับคู่ไม่ได้ 8 (ไฟล์ช่วย: IMPACT json · RUN_STATE · shots_b64 ว่าง · make_data.py · reports/inventory·ui_brief_check·tc_counts) — อธิบายได้
- consistency_check: READY · BLOCK 0 · WARN 1 (K9 ไม่มี report e2e — [NO-BROWSER])
- dm.sh pack (โหมด NO-BROWSER = แพ็กแบบมีเงื่อนไข)
