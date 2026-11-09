# RUN_LOG — F-TMP-004 FM-ITS-06 แบบฟอร์มใบแจ้งซ่อมอุปกรณ์คอมพิวเตอร์ (REQ-TMP-004)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพฟอร์ม: to_image.py → LibreOffice → PDF → pypdfium2 (หน้ากระดาษจริงจาก print area A1:F46 · A4 portrait) · ตัวไทยในภาพอ่านได้ · ถ้อยคำยึด content.html + openpyxl + drawing1.xml (textbox ☐ ประเภท) + vmlDrawing (☐ 11 ช่อง)
- หัวฟอร์มจริง "แบบฟอร์มใบแจ้งซ่อมอุปกรณ์คอมพิวเตอร์" = ชื่อไฟล์ → form.title ตรง ไม่ต้อง rename
- 2 ส่วน: ส่วนที่ 1 ผู้แจ้งซ่อม (7 ช่อง + ☐ประเภท 4) · ส่วนที่ 2 เจ้าหน้าที่ IT (วันที่ซ่อม + ☐ผลตรวจเช็ค 5 + ชุด ระยะเวลา/ร้านค้า/วันที่ส่งเคลม ใต้ 3 ตัวเลือก → จดเป็น 4 ช่องใช้ร่วม) · ผลการซ่อม ☐2 + บรรทัด 2 · ลายเซ็น 6 จุด (ผู้แจ้งซ่อม · ผู้รับแจ้ง · ผู้ดำเนินการ · อนุมัติโดย · ผู้ดำเนินการ · ผู้แจ้งซ่อม) ทุกจุดมี (วัน/เดือน/ปี)
- แก้สะกด (G5): ตําแหน่ง→ตำแหน่ง · ส่งเครม→ส่งเคลม · สั้งซื้อ→สั่งซื้อ · anomaly: ตัวเลือกสั่งซื้อใช้คำ "ร้านค้าที่ส่งเคลม" → คงคำ + OQ ลูกค้า
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC · impact_summary (regex REQ-[\w-]+ ใช้ได้แล้ว)
- form_spec_check: ERROR 0 · WARN 0 · 17 ช่อง · ลายเซ็น 6 · ข้อมูลส่วนบุคคล: ฟอร์มเปล่า ไม่มีข้อมูลจริง (โลโก้ลูกค้าในภาพ ไม่ใช้ — ระบบใช้โลโก้ Organization)
- 2026-10-10 08:32 · ขั้น 1 → done · FORM_SPEC 17 ช่อง ERROR 0 · PREBRIEF v2 · impact summary

## ขั้น 2 · gate (unattended — AI-DEFAULT 11 มติ + VALID 7)
- G1: ฟอร์มไม่ระบุการเปลี่ยนค่า/ส่งต่อ → config_changes [] · post_to [] (ทะเบียนทรัพย์สิน/ใบขอซื้อไม่ผูก · รหัสทรัพย์สินผู้ใช้กรอกเอง)
- G2: ช่องผู้อนุมัติบนกระดาษ 1 ช่อง "อนุมัติโดย" (ส่วนที่ 2) → dynamic 1 ขั้น role-line-manager (ผู้บังคับบัญชาของเจ้าหน้าที่ IT ผู้ส่งอนุมัติ) · ไม่มีวงเงิน
- G3: ไม่มีสูตร/ค่าคงที่ · กติกาตรวจ = เตือน (วันที่ส่งมอบ ≥ วันที่แจ้ง · ถึง ≥ ระยะเวลา) + อื่นๆ ต้องระบุ + ชุดเคลมบังคับเมื่อเลือกส่งบริษัท/สั่งซื้อ + ซ่อมไม่ได้ต้องระบุ
- G4: ไม่มีรายการซ้ำ
- G5: 1:1 · แก้สะกด ตำแหน่ง · ส่งเคลม · สั่งซื้อ
- G6: แถวลงชื่อตามกระดาษ 3 แถว · อนุมัติโดย = ช่องต่อขั้น DOA · อื่น ๆ (ผู้แจ้งซ่อม/ผู้รับแจ้ง/ผู้ดำเนินการ) = ชื่อผู้กดจากระบบ · ข้อความในระบบ ไม่ใช้ภาพ
- G7: ไม่อนุมัติ → กลับร่าง (ส่วนที่ 2 ให้ IT แก้) เลขเดิม · ยกเลิก owner+admin ใน draft/pending · เหตุผลบังคับ
- G8: เจ้าของ · ผู้อนุมัติหลังส่ง · admin role ฝ่าย IT เห็นทั้งหมด
- G9: ออกเลขตอนบันทึกครั้งแรก · รหัส CRR (Computer Repair Request) — ITRS/SRC ใช้แล้ว
- G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- decisions_lock: พร้อมเริ่มทำ (exit 0) · dm.sh tag → AI-DEFAULT 11
- 2026-10-10 08:32 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · AI-DEFAULT 11

## ขั้น 3 · declaration ร่าง
- doa: init module=it · doa_type crr · 1 ขั้น role-line-manager (อนุมัติโดย) · init เขียน on_reject: draft → แก้เป็น back_to_draft (บทเรียน J001) · action ส่งอนุมัติจาก `inspecting` (ร่างผลตรวจเช็คส่วนที่ 2 = draft ของขั้นอนุมัติ — กระดาษวางช่อง อนุมัติโดย ในส่วนของ IT) · ไม่อนุมัติ → กลับ inspecting เลขเดิม → validate PASS · brief PASS
- ntf: crr_reported (→ role-it-officer) · crr_received · crr_cancelled · crr_repaired · ตัด over_limit (ไม่มีเกณฑ์ตัวเลข) → PASS
- role-it-officer (เจ้าหน้าที่ IT ผู้รับแจ้ง/ผู้ดำเนินการ · admin role ฝ่าย IT) ไม่มีใน doa-roles-contract → แจ้งใน _BATCH_REPORT
- doccfg + mdoc ทำหลังขั้น 4
- 2026-10-10 08:33 · ขั้น 3 → done · doa PASS · ntf PASS · doccfg/mdoc หลังขั้น 4

## ขั้น 4 · แบบพิมพ์ Replica (R9 ตารางกรอบ · 2 หน้า R10)
- form.tpl.html R9 · หน้า 1 = หัว + ส่วนที่ 1 + ลงชื่อ ผู้แจ้งซ่อม/ผู้รับแจ้ง · หน้า 2 = หัวย่อ (thead เลขที่เอกสาร/วันที่ ซ้ำ) + ส่วนที่ 2 + sign_rows (ผู้ดำเนินการ + ขั้น DOA) + ผลการซ่อม + ลงชื่อ ผู้ดำเนินการ/ผู้แจ้งซ่อม · cont-note "มีต่อหน้าถัดไป" · page-no หน้า X/2 · ฟอนต์ 9.6pt
- เหตุผล R10: รอบแรกออกแบบ 1 หน้า → ตรวจ Chromium นอกเครื่องงาน ล้นเป็น 2 หน้าทุกสถานะ (3 หน้าเมื่อ DOA 6 ขั้น/ข้อความยาว) · สัญญาณ R10 "ส่วนกรอกหลายหมวด + สายอนุมัติ ≥4 ขั้น" → ตัดหน้าตั้งใจก่อนส่วนที่ 2
- data 5 สถานะ (make_data.py · ข้อมูลสมมติ): draft · approved · rejected · long-text · approved-doa6steps (7 ช่อง 4+3)
- parity_check: IDENTICAL 5/5 · render_doc --strict ไม่มี key ขาด · ไม่มี {{}} หลง · build_html ทุกสถานะ → print/out/*.html + แบบฟอร์มใบแจ้งซ่อมอุปกรณ์คอมพิวเตอร์_template.html
- [NO-BROWSER] ข้าม render_pdf.py (ภายใน render_states.py) — render_doc + build_html ทีละสถานะแทน ได้ HTML ไม่มี PDF/PNG/_states_sheet.png
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ approved.pdf)
- ตรวจภาพเบื้องต้นนอกเครื่องงาน (stage HTML ไป Chromium ใน container ของ agent · ไม่เก็บไฟล์กลับ): 5/5 สถานะ = 2 หน้า · บล็อกลงชื่อไม่ตัด · ไม่ใช่ผลด่านทางการ ต้องรัน render_states --max-pages 2 บนเครื่องที่มี browser
- doccfg: CRR · --registry (ACL/ITRS/SRC) ไม่ชน → PASS · mdoc: WARN G04 (ไม่มี taxonomy_def_id) + G09 (doa pending) — อธิบายได้ · source=declaration · function_code F01 ชั่วคราว
- doa validate --print-config: PASS (sign_boxes doa_step:*)
- 2026-10-10 08:38 · ขั้น 4 → done · 2 หน้า R10 · parity 5/5 IDENTICAL · [NO-BROWSER] ไม่มี PDF/compare · doccfg PASS · mdoc WARN(G04,G09)

## ขั้น 5 · HTML Q-form (html-generator v9.4)
- build: .scratch/build_feature.py ประกอบจาก canonical references/form-archetype (shell + BASE-KIT) + be-datepicker + tpl_render.js (verbatim) + app CRR (.scratch/build/c1a–c8.js) + extra.css (Group 25) · PDF tab ฝัง print/form.tpl.html + docPrintData()
- เปิด GOLDEN_SKELETON.html + ui-standard-list-drawer.md U1–U28 เทียบก่อน build
- flow ตามลายเซ็น 6 จุดบนกระดาษ: ร่าง → (ส่งแจ้งซ่อม) รอรับแจ้ง → (IT รับแจ้ง) ตรวจเช็ค → (IT บันทึกผลตรวจเช็ค + ส่งอนุมัติ · DOA N ขั้น เลือกผู้พิจารณาต่อขั้น) รออนุมัติ → รอผลซ่อม → (IT บันทึกผลการซ่อม) รอผู้แจ้งรับทราบ → (ผู้แจ้งรับทราบ) ปิดงาน · ไม่อนุมัติ = กลับ ตรวจเช็ค เลขเดิม + แบนเนอร์เหตุผล · ยกเลิก (ร่าง/รอรับแจ้ง/ตรวจเช็ค/รออนุมัติ · เจ้าของ+admin IT · เหตุผลบังคับ)
- audit.sh: FAIL 0 · WARN 3 (มาจาก BASE-KIT กลาง: comment lucide · .uc-email · font-size px ใน shell) → reports/audit.txt · prune_css ตัด 78 rule → audit ซ้ำ FAIL 0
- [NO-BROWSER] ข้าม e2e_standard.py · ข้าม render-check.py บนเครื่องงาน
- ทดแทน: smoke test jsdom (node · ไม่ใช่ browser จริง · ไม่ใช่ด่านทางการ) 54/54 · JS error 0 → reports/smoke_jsdom.txt (สิทธิ์ G8 · wizard/validation · flow ครบ 7 สถานะ · ไม่อนุมัติกลับตรวจเช็ค · DOA 2 ขั้น dynamic · BR-DOA-04 · ยกเลิกต้องมีเหตุผล · backdrop mousedown · sim stale)
- ตรวจเบื้องต้นนอกเครื่องงาน (stage feature.html ไป Chromium ใน container ของ agent · lucide stub · ไม่เก็บไฟล์กลับ): e2e_standard 21/21 (รอบแรก 19/21 → แก้: สายผู้พิจารณาว่างจนกว่าจะส่งอนุมัติ · ผู้พิจารณาไม่เห็นใบหลังตีกลับ) — ไม่ใช่ผลด่านทางการ ต้องรันซ้ำบนเครื่องที่มี browser
- __QA__.openSubmit: e2e มาตรฐานเปิด modal ส่งอนุมัติจากใบร่าง แต่ flow นี้ส่งอนุมัติจาก ตรวจเช็ค → hook เปิด modal แบบ preview (นับช่องผู้พิจารณา) · ยืนยันส่งจากใบที่ไม่ใช่ ตรวจเช็ค = ไม่เปลี่ยนสถานะ
- parity แบบพิมพ์ใน prototype: printData จาก JS → render_doc.py IDENTICAL 6/6 (รวม DOA 2 ขั้น) · key ของ printData = key ของ make_data.py ตรงกัน
- U1–U28: U1✓ U2✓ U3✓ U4✓ U5✓ kebab ⋮ U6✓ U7✓ U8✓ 920/1290 U9✓ U10✓ U11✓(kit) U12✓ U13✓ summary+timeline 6 จุดลงชื่อ+emp-chip U14✓ wizard 3 ขั้น U15✓ แก้ไข = wizard เดิม เฉพาะร่าง U16 n/a (ไม่มีลบ — ยกเลิกเอกสาร soft + เหตุผล) U17✓ U18✓ U19✓ header sub 1 fact (รายการ) U20✓ seg tabs ทั้งหมด/งานที่ต้องทำ/ใบแจ้งซ่อมของฉัน U21✓(kit) U22✓ U23✓ U24✓ search-select portal U25✓ backdrop onmousedown U26–U28 n/a (ไม่มีหน้าตั้งค่า)
- 2026-10-10 08:55 · ขั้น 5 → done · audit FAIL 0 · [NO-BROWSER] e2e/render-check ข้าม → jsdom smoke 54/54 · pre-check e2e นอกเครื่อง 21/21
- 2026-10-10 08:55 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 6 — ข้าม (unattended)
- ให้คนดูจาก _BATCH_REPORT · [NO-BROWSER] ยังไม่มี _states_sheet.png / screenshot หน้าจอหลัก (ต้อง render บนเครื่องที่มี browser)

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-004.md/.docx (brd-generator-full v2.3 Prebrief Mode · Lane · md_to_docx.py) — AI Review C01–C23 + PE01–PE05 → **APPROVED** (C16 ไม่มีรหัสใน registry = ยอมรับใน Prebrief Mode · ตัวชี้วัดไม่มีใน input → OQ-01)
- FRD_F-TMP-004_Pack (frd-generator-v6.2 Input Mode 0 · FULL variant: states=8) 00–07 + INDEX + declarations/ · FRD บรรยายสายอนุมัติตรง DEC-03/08 (1 ขั้น role-line-manager ของผู้ส่ง · ไม่อนุมัติ → inspecting) — บทเรียน K2/K7 จาก J002
- frd_lint Section N: BLOCK 0 · WARN 0 · PASS 14 → reports/_SECTION_N.md
- declaration --final: doccfg PASS (--registry · CRR ไม่ชน ACL/ITRS/SRC · frd_ref FN-02/FN-07) · ntf PASS (frd_ref FN-03/04/11/09) · doa PASS (--print-config) · mdoc WARN G04 (ไม่มี taxonomy_def_id) + G09 (doa pending) — อธิบายได้
- OQ ใหม่: OQ-04 คำ "ส่งเคลม" ใต้ตัวเลือกสั่งซื้อ (DEC-15) · OQ-06 อนุมัติก่อนซ่อมทุกกรณีหรือเฉพาะส่งเคลม/สั่งซื้อ
- 2026-10-10 09:00 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 · declaration final PASS (mdoc WARN G04/G09)

## ขั้น 8 · UI Brief → test case AI → UAT
- extract_anchors → reports/inventory.json · UI_BRIEF_F-TMP-004.md (§0–§13 · CSS vars/microcopy สกัดจาก inventory) → brief_check: PASS · FAIL 0 · WARN 0 → reports/ui_brief_check.md
- testcases-F-TMP-004.md: 58 เคส / 291 step (L7 C7 V2 F2 R2 I5 A4 M3 X3 P6 D5 E5 K4 XT3) · tc_lint ERROR 0 · Coverage Ledger อัตโนมัติ: AT 22/22 · BR 16/16 · VR 13/13 · EC 10/14 (ที่เหลือทดสอบที่แบบพิมพ์/API) · DN 7/8 · DEC 18/18 · XT 3/3
- [NO-BROWSER] ข้าม verify_anchors.py · ข้าม capture.py (เอกสารคนไม่มีภาพหน้าจอ)
- UAT (qa-friendly Lite): cases.json 44 เคส · drop ledger 14 (จำลองหลังบ้าน/เชิงเทคนิค/ยุบ) · lite_audit หายเงียบ 0 + stamp · build.py → testcase-F-TMP-004.html (ไม่มีภาพ)
- 2026-10-10 09:05 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 (58 เคส) · lite_audit หายเงียบ 0 · [NO-BROWSER] verify_anchors/capture ข้าม

## ขั้น 9 · ตรวจรวม + แพ็ก
- orig/content.html → orig/out/ (กันชน artifact prototype · บทเรียน J001/J002 K2) · สคริปต์ประกอบ/สร้างเอกสารอยู่ .scratch/ (manifest_scan ข้ามโฟลเดอร์ขึ้นต้นจุด)
- manifest_scan: 39 artifact · ซ้ำ 0 · จับคู่ไม่ได้ 8 (RUN_STATE · IMPACT json · make_data.py · reports/audit·ui_brief_check·smoke_jsdom·tc_counts·inventory) — อธิบายได้
- consistency_check: READY · BLOCK 0 · WARN 1 (K9 ไม่มี report e2e — [NO-BROWSER]) · K2/K7 ผ่านรอบแรก
- dm.sh pack (โหมด NO-BROWSER = แพ็กแบบมีเงื่อนไข) · รอบแรก WARN K3 (RUN_LOG แก้หลัง scan) → scan ใหม่แล้วแพ็กซ้ำ
