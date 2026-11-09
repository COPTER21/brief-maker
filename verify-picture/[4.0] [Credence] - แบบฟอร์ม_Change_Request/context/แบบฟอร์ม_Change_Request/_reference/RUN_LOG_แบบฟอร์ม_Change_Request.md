# RUN_LOG — F-TMP-005 FM-ITS-07 แบบฟอร์ม Change Request Form (REQ-TMP-005)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพฟอร์ม: to_image.py → LibreOffice → PDF → pypdfium2 (print area A1:F25 · A4 portrait scale 88%) · ตัวไทยในภาพเป็นกล่อง (ไม่มีฟอนต์ไทยในเครื่องแปลง) → ภาพยึดตำแหน่ง/เส้น · ถ้อยคำยึด content.html + drawing1.xml (หัว Change Request Form) + vmlDrawing (☐ 5 ช่อง) + footer
- หัวฟอร์มพิมพ์อังกฤษล้วน "Change Request Form" → form.title = "แบบฟอร์ม Change Request" (ชื่อในคิวไม่เพี้ยน → ไม่ rename)
- ช่อง 11: วันที่ · ตำแหน่ง · ชื่อ-นามสกุล · วันที่ต้องการส่งมอบ · สถานที่ส่งมอบ · เรื่องที่ต้องการ · ☐ประเภท 5 (+อื่นๆ ระบุ) · รายละเอียด · วัตถุประสงค์ · ระบบที่ได้รับผลกระทบ · แผนการดำเนินการ (คำอธิบายสีเทาใต้หัวข้อ = hint)
- ลายเซ็น 3: ผู้ขอซื้อ (anomaly — คำไม่ตรงเอกสาร คงคำ + OQ) · ตรวจสอบโดย · อนุมัติโดย · ไม่มีช่องเลขที่บนกระดาษ (running_no_on_paper false)
- แก้สะกด (G5): ตําแหน่ง→ตำแหน่ง
- ไม่มี PREBRIEF จาก CMS → PREBRIEF v2 จาก FORM_SPEC (--req REQ-TMP-005 --module "IT Support") · impact_summary
- form_spec_check: ERROR 0 · 11 ช่อง · ตัวเลือก 1 · ลายเซ็น 3 · ข้อมูลส่วนบุคคล: ฟอร์มเปล่า ไม่มีข้อมูลจริง (ชื่อผู้สร้างใน docProps ไม่ใช้)
- orig/content.html → orig/out/content.html (กันชน artifact prototype · บทเรียน J001/J002)
- 2026-10-10 09:09 · ขั้น 1 → done · FORM_SPEC 11 ช่อง ERROR 0 · PREBRIEF v2 · impact summary

## ขั้น 2 · gate (unattended — AI-DEFAULT 11 มติ + VALID 6)
- G1: ฟอร์มไม่ระบุการเปลี่ยนค่า/ส่งต่อ → config_changes [] · post_to [] (การเปลี่ยนแปลงจริงทำนอกระบบโดยฝ่าย IT)
- G2: ช่องผู้อนุมัติบนกระดาษ 2 ช่อง (ตรวจสอบโดย · อนุมัติโดย) → dynamic 2 ขั้น role-line-manager → role-mgr-it · ไม่มีวงเงิน · role-mgr-it ไม่มีใน doa-roles-contract (เหมือน J003) → แจ้ง _BATCH_REPORT
- G3: ไม่มีสูตร/ค่าคงที่ · ส่งมอบ ≥ วันที่ขอ (เตือน) · ประเภท ≥1 เลือกหลายข้อได้ (บล็อก) · อื่นๆ ต้องระบุ (บล็อก)
- G4: ไม่มีรายการซ้ำ
- G5: 1:1 · แก้สะกด ตำแหน่ง · ป้าย ผู้ขอซื้อ คงคำ + OQ
- G6: แถวล่าง ผู้ขอซื้อ + ช่องต่อขั้น DOA (ตรวจสอบโดย · อนุมัติโดย) · ข้อความในระบบ ไม่ใช้ภาพ
- G7: ไม่อนุมัติ → กลับร่างเลขเดิม · ยกเลิก owner+admin ใน draft/pending · เหตุผลบังคับ
- G8: เจ้าของ · ผู้อนุมัติหลังส่ง · admin role ฝ่าย IT (role-it-officer) เห็นทั้งหมด
- G9: ออกเลขตอนบันทึกครั้งแรก · รหัส ITCR (IT Change Request — ACL/ITRS/SRC/DRITS/CRR ใช้แล้ว)
- G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- decisions_lock: พร้อมเริ่มทำ (exit 0) · dm.sh tag → AI-DEFAULT 11
- 2026-10-10 09:09 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · AI-DEFAULT 11

## ขั้น 3 · declaration ร่าง
- doa: init module=it · doa_type itcr · 2 ขั้น role-line-manager (ตรวจสอบโดย) → role-mgr-it (อนุมัติโดย) · init เขียน on_reject: draft → แก้เป็น back_to_draft (บทเรียน J001) · validate WARN G1 (role-mgr-it นอก contract) · BLOCK 0
- ntf: itcr_cancelled (→ ผู้อนุมัติขั้นปัจจุบัน) · itcr_approved_for_it (approved → role-it-officer) · ตัด over_limit (ไม่มีเกณฑ์ตัวเลข) → PASS
- role-mgr-it + role-it-officer ไม่มีใน doa-roles-contract (ชื่อเดียวกับ J003/J004) → แจ้ง _BATCH_REPORT
- doccfg + mdoc ทำหลังขั้น 4
- 2026-10-10 09:09 · ขั้น 3 → done · doa WARN (role-mgr-it นอก contract) BLOCK 0 · ntf PASS · doccfg/mdoc หลังขั้น 4

## ขั้น 4 · แบบพิมพ์ Replica (R9 ตารางกรอบ · 1 หน้า)
- form.tpl.html R9 (หัวช่องซ้ายพื้นเทา th) + sign_rows (ผู้ขอซื้อ + ขั้น DOA) · profile.json · print_config.json · make_data.py → 5 สถานะ (draft · approved · rejected · long-text · approved-doa6steps 7 ช่อง 4+3) · ข้อมูลสมมติทั้งหมด
- parity_check: IDENTICAL 5/5 · ไม่มี {{}} หลง · ไม่มี key ขาด · build_html ทุกสถานะ → print/out/*.html + ITCR_template.html (.scratch/render_nobrowser.py)
- [NO-BROWSER] ข้าม render_pdf.py (ภายใน render_states.py) — render body + build_html ทีละสถานะแทน ได้ HTML ไม่มี PDF/PNG/_states_sheet.png
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ approved.pdf)
- ตรวจภาพเบื้องต้นนอกเครื่องงาน (stage HTML 5 สถานะไป Chromium ใน container ของ agent · ไม่เก็บไฟล์กลับ): 5/5 = 1 หน้า A4 · บล็อกลงชื่อไม่ตัด · ฟอนต์ ≥ 8pt → ไม่เข้า R10 · ไม่ใช่ผลด่านทางการ ต้องรัน render_states --max-pages 1 บนเครื่องที่มี browser
- ปรับ anomaly เลขที่: แสดงที่ footer (ไม่ใช่หัว) → form_spec_check + decisions_lock + tag ใหม่ (DEC-17 ข้อความเปลี่ยน · AI-DEFAULT 11 เท่าเดิม)
- doccfg: ITCR · --registry (ACL/ITRS/SRC/DRITS/CRR) ไม่ชน → PASS · mdoc: WARN G04 (ไม่มี taxonomy_def_id) + G09 (doa pending) — อธิบายได้ · function_code F01 ชั่วคราว
- doa validate --print-config: WARN (role-mgr-it นอก contract) · BLOCK 0
- 2026-10-10 09:12 · ขั้น 4 → done · 1 หน้า · parity 5/5 IDENTICAL · [NO-BROWSER] ไม่มี PDF/compare · doccfg PASS · mdoc WARN(G04,G09)

## ขั้น 5 · HTML Q-form (html-generator v9.4)
- build: .build/build_feature.py ประกอบจาก canonical references/form-archetype (shell + BASE-KIT) + be-datepicker + tpl_render.js (verbatim) + app ITCR (.build/patch_app.py: โครง Q-form ของ F-TMP-001 ซึ่งหัวฟอร์ม Excel ชุดเดียวกัน + p_head/p_view/p_print/p_wiz.js) + extra.css (Group 25) · PDF tab ฝัง print/form.tpl.html + docPrintData() · โลโก้ตัวอย่างจาก xl/media ของต้นฉบับ (ระบบจริงอ่าน Organization)
- เปิด GOLDEN_SKELETON.html + ui-standard-list-drawer.md U1–U28 เทียบก่อน build
- ช่องตามกระดาษ 1:1 (#106): ชื่อ-นามสกุล/ตำแหน่ง/วันที่ = ระบบใส่ (การ์ดสรุป) · กรอก: เรื่องที่ต้องการ · ☐ประเภท 5 (+อื่นๆ) · วันที่ต้องการส่งมอบ (bedateHTML) · สถานที่ส่งมอบ · รายละเอียด · วัตถุประสงค์ · ระบบที่ได้รับผลกระทบ · แผนการดำเนินการ (คำอธิบายเทาบนกระดาษ = field-help) · ไม่มีช่องเพิ่ม
- flow: ร่าง → รออนุมัติ (ขั้น 1 ตรวจสอบโดย role-line-manager → ขั้น 2 อนุมัติโดย role-mgr-it · dynamic เลือกผู้พิจารณาต่อขั้น) → อนุมัติแล้ว (แจ้ง IT itcr_approved_for_it) · ไม่อนุมัติ (ขั้นใดก็ได้) = กลับร่างเลขเดิม + แบนเนอร์เหตุผล · ยกเลิก (ร่าง/รออนุมัติ · เจ้าของ+admin IT · เหตุผลบังคับ) · ไม่มีขั้น "ดำเนินการแล้ว" (กระดาษไม่มีช่องลงชื่อผู้ดำเนินการ)
- audit.sh: FAIL 0 · WARN 3 (มาจาก BASE-KIT กลาง: comment lucide · .uc-email · font-size px ใน shell) → reports/audit.txt · prune_css ตัด 76 rule → audit ซ้ำ FAIL 0 · มี meta cube-archetype + window.__QA__
- [NO-BROWSER] ข้าม e2e_standard.py · ข้าม render-check.py บนเครื่องงาน
- ตรวจเบื้องต้นนอกเครื่องงาน (stage feature.html ไป Chromium ใน container ของ agent · lucide stub · ไม่เก็บไฟล์กลับ): e2e_standard 21/21 ก่อนและหลัง prune · flow test 16/16 (อนุมัติ 2 ขั้นเรียงลำดับ · ไม่อนุมัติขั้น 2 กลับร่างเลขเดิม + ผู้พิจารณาไม่เห็นร่าง · อื่นๆ/ประเภท ≥1 บล็อก · ส่งมอบก่อนวันที่ขอ = เตือน · ออกเลข ITCR ตอนบันทึกร่าง · admin ยกเลิก) · ไม่มี pageerror — ไม่ใช่ผลด่านทางการ ต้องรันซ้ำบนเครื่องที่มี browser
- parity แบบพิมพ์ใน prototype: printData จาก JS (R6 อนุมัติ 2 ขั้น · ร่างใหม่) → render_doc.py IDENTICAL 2/2 · key ของ printData = key ของ make_data.py
- U1–U28: U1✓ (ไม่มี stat cards · badge ใน sub) U2✓ U3✓ U4✓ U5✓ kebab ⋮ U6✓ page-size+x–y จาก N+pager U7✓ CSV ที่ head U8✓ 920/1290 U9✓ เหตุผลบังคับ U10✓ U11✓(kit) U12✓ U13✓ summary+timeline+emp-chip U14✓ wizard 3 ขั้น U15✓ แก้ไข = wizard เดิม เฉพาะร่าง U16 – (ไม่มีลบ: ยกเลิก = soft + เหตุผล) U17✓ คน = วงกลม icon U18✓ U19✓ header sub 1 fact (วันที่ส่งมอบ) U20✓ seg tabs ทั้งหมด/รอฉันพิจารณา/คำขอของฉัน U21✓(kit) U22✓ U23✓ U24✓ search-select portal U25✓ backdrop onmousedown U26–U28 – (ไม่มีหน้าตั้งค่า)
- 2026-10-10 09:20 · ขั้น 5 → done · audit FAIL 0 · U1–U28 ✓ · [NO-BROWSER] e2e/render-check ข้าม (pre-check นอกเครื่อง 21/21 · flow 16/16)
- 2026-10-10 09:21 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 6 — ข้าม (unattended)
- ให้คนดูจาก _BATCH_REPORT · [NO-BROWSER] ยังไม่มี _states_sheet.png / screenshot หน้าจอหลัก (ต้อง render บนเครื่องที่มี browser)

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-005.md/.docx (brd-generator-full v2.3 Prebrief Mode · Lane · md_to_docx.py) — AI Review C01–C23 + PE01–PE05 → **APPROVED** (C16 ไม่มีรหัสใน registry = ยอมรับใน Prebrief Mode · ตัวชี้วัดไม่มีใน input → OQ-01)
- FRD_F-TMP-005_Pack (frd-generator-v6.2 Input Mode 0 · FULL variant: states=4 + approval) 00–07 + INDEX + declarations/ · 07 §7.0 = แถว DEC จาก DECISIONS.lock.md ตรงตัว (17)
- FRD บรรยายสาย DOA ตรงมติ DEC-03 (2 ขั้น ตรวจสอบโดย role-line-manager → อนุมัติโดย role-mgr-it · ไม่อนุมัติขั้นใดก็ได้ → draft เลขเดิม DEC-08) · ไม่มีขั้นผู้ดำเนินการ (บทเรียน K2/K7)
- frd_lint Section N: BLOCK 0 · WARN 0 · PASS 12 → reports/_SECTION_N.md
- declaration --final: doccfg PASS (--registry · ITCR ไม่ชน · frd_ref FN-02/FN-04) · ntf PASS (frd_ref FN-06/FN-04) · doa WARN (role-mgr-it นอก contract · --print-config) BLOCK 0 · mdoc WARN G04 (ไม่มี taxonomy_def_id) + G09 (doa pending) — อธิบายได้
- OQ ใหม่: OQ-04 บันทึกผลดำเนินการ/ปิดงาน · OQ-05 ป้าย ผู้ขอซื้อ / ตัวตน ตรวจสอบโดย
- 2026-10-10 09:24 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 · declaration final BLOCK 0 (doa WARN role-mgr-it · mdoc WARN G04/G09)

## ขั้น 8 · UI Brief → test case AI → UAT
- extract_anchors → reports/inventory.json · UI_BRIEF_F-TMP-005.md (§0–§13 · CSS vars/z-index/microcopy สกัดจาก inventory ด้วย .build/gen_ui_brief.py) → brief_check: PASS · FAIL 0 · WARN 0 → reports/ui_brief_check.md
- testcases-F-TMP-005.md: 61 เคส / 140 step (L11 C5 V7 F3 D5 A5 K4 P7 R6 E5 X3) · tc_lint ERROR 0 · Coverage Ledger + Audit (S 11/11 · VR 11/11 · DEC 17/17 · XT 3/3 · ข้าม BR-13/EC-04/EC-07 พร้อมเหตุผล)
- [NO-BROWSER] ข้าม verify_anchors.py บนเครื่องงาน · ตรวจเบื้องต้นนอกเครื่องงาน (Chromium ใน container ของ agent · lucide stub): DOM 224 · SOURCE 59 · PATTERN 6 · DATA 15 · MISSING 0 — ไม่ใช่ผลด่านทางการ
- UAT (qa-friendly v3.1 Lite): cases.json 51 เคส · drop ledger 10 (คำสั่งหลังบ้าน/จำลอง/แจ้งเตือนจริง/ตั้งค่าเอกสาร) · lite_audit หายเงียบ 0 + stamp md5 · build testcase-F-TMP-005.html · เคสที่เริ่มจากใบเฉพาะ ระบุเลขที่ใน "ก่อนเริ่ม"
- [NO-BROWSER] ข้าม capture.py → ไม่มีภาพหน้าจอ (regionKey ว่างทุก step · shots_b64.json = {})
- 2026-10-10 09:33 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 (61 เคส) · lite_audit หายเงียบ 0 · [NO-BROWSER] verify_anchors/capture ข้าม

## ขั้น 9 · ตรวจรวม + แพ็ก
- ไฟล์ช่วย build อยู่ .build/ + .scratch/ (ซ่อนจาก manifest) · orig/content.html → orig/out/ (กันชน artifact prototype)
- manifest_scan: 39 artifact · ซ้ำ 0 · จับคู่ไม่ได้ 8 (ไฟล์ช่วย: RUN_STATE · IMPACT json · shots_b64 ว่าง · make_data.py · reports/audit·ui_brief_check·tc_counts·inventory) — อธิบายได้
- consistency_check: READY · BLOCK 0 · WARN 1 (K9 ไม่มี report e2e — [NO-BROWSER]) · K2/K7 ผ่านรอบแรก
- dm.sh pack (โหมด NO-BROWSER = แพ็กแบบมีเงื่อนไข)
