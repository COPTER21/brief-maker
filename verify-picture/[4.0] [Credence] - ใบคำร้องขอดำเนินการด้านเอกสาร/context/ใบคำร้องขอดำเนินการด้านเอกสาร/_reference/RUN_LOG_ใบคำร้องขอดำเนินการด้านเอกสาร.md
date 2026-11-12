# RUN_LOG — F-TMP-007 FM-CCC-03 ใบคำร้องขอดำเนินการด้านเอกสาร Document Action Request (DAR Form ) (REQ-TMP-007)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: to_image.py → LibreOffice → PDF → pypdfium2 · print area A1:DM32 กว้าง → แตกเป็น page-1/page-2 (กระดาษจริง A4 แนวนอน 1 หน้า) · ถ้อยคำยึด openpyxl/content.html (เปลี่ยนชื่อเป็น orig/content_extract.txt กัน K2 นับเป็น prototype) · ตำแหน่ง/เส้นยึดภาพ
- หัวกระดาษ (K1:CU1) = "ใบคำร้องขอดำเนินการด้านเอกสาร / Document Action Request (DAR Form )" → form.title = ใบคำร้องขอดำเนินการด้านเอกสาร · ชื่อในคิวไม่เพี้ยน → ไม่ต้อง rename
- 17 ช่อง · ตัวเลือก 5 กลุ่ม (วัตถุประสงค์ 4 · ISSUE 4 · ที่มา 4 · แจกจ่าย 27 หน่วยงาน · วิธีรับ 2) · แถวซ้ำ 1 (เอกสารเกี่ยวข้อง 14 แถว) · ลายเซ็น 6 (ผู้จัดทำ + 4 ขั้นพิจารณา + ลงนามรับเอกสารควบคุม) · DAR.No. บนกระดาษ · ไม่มีข้อมูลตัวอย่าง/ข้อมูลส่วนบุคคลในไฟล์
- anomalies 5: หน่วยงานแจกจ่ายชุด V–AA ซ้ำชุด P–U · อื่นๆ ไม่มีช่องระบุ · ISSUE 4 ตัวเลือก · วันที่บังคับใช้ · รูปแบบ E-Mail
- form_spec_check: ERROR 0 · ไม่มี PREBRIEF CMS → PREBRIEF v2 จาก FORM_SPEC (--req REQ-TMP-007 --module CCC)
- 2026-10-10 09:37 · ขั้น 1 → done · FORM_SPEC 17 ช่อง · 14 แถว · ลายเซ็น 6 · ERROR 0

## ขั้น 2 — เหตุผลรายหมวด (unattended · AI-DEFAULT ทั้งหมด)
- G1: ฟอร์มไม่ได้เขียนว่าเปลี่ยนค่า/ส่งต่อ → config_changes [] · post_to [] · การขึ้นทะเบียน/แก้เอกสารควบคุมจริงอยู่นอกระบบนี้ (เสนอเชื่อม Policy Center · Policy Document เป็นงานต่อยอดใน _BATCH_REPORT)
- G2: ช่องพิจารณาบนกระดาษ 4 ช่อง → dynamic 4 ขั้น: role-line-manager (ผู้ตรวจสอบ) · role-mgr-bu (ผู้อนุมัติ) · role-doc-controller (ผู้ควบคุมเอกสาร — ไม่มีใน contract) · role-mgr-ocs (ผู้จัดการฝ่ายสำนักเลขานุการบริษัท — ไม่มีใน contract) · ไม่มีวงเงิน · กระดาษอ้าง "ตารางผู้มีอำนาจอนุมัติด้านเอกสาร" → ตั้งที่ DOA กลาง
- G3: ไม่มีสูตร/ค่าคงที่ · กติกาตรวจ 7 ข้อ (ตัวเลือกบังคับ · เดิม/ใหม่ตามวัตถุประสงค์ · อื่นๆ ต้องระบุ · แจกจ่าย ≥1 · E-mail รูปแบบ · วันบังคับใช้ก่อนวันเขียน = เตือน · แถวเอกสารเกี่ยวข้องต้องครบคู่)
- G4: กระดาษ 14 แถว → ไม่จำกัด · PDF ขั้นต่ำ 14
- G5: 1:1 ไม่เพิ่มช่อง · หน่วยงานแจกจ่าย 27 ช่องตามกระดาษ (ชุดซ้ำ V–AA ติด (2) → OQ)
- G6: แถวล่าง ผู้จัดทำ + 1 ช่องต่อขั้น DOA · "ลงนามรับเอกสารควบคุม" = ข้อความระบบเมื่อผู้รับกดรับหลังอนุมัติ · ไม่ใช้ภาพ
- G7: ไม่อนุมัติ → กลับร่างเลขเดิม · ยกเลิก: เจ้าของ + admin role · ร่าง/รออนุมัติ · เหตุผลบังคับ
- G8: เจ้าของ · ผู้พิจารณาหลังส่ง · admin role (Document Control Center / CCC) เห็นทั้งหมด
- G9: ออกเลขบันทึกครั้งแรก · รหัส DAR (พิมพ์บนกระดาษ DAR.No.) — ไม่ชน registry (ACL ITRS SRC DRITS CRR ITCR SRAL) และไม่ชน J008 (CAR)
- G10: แนบ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗
- decisions_lock: 16 มติ พร้อมเริ่มทำ (exit 0) · tag-ai-default → 11 มติ AI-DEFAULT
- 2026-10-10 09:37 · ขั้น 2 → done · 16 มติ · AI-DEFAULT 11 · DOA 4 ขั้น · code DAR

## ขั้น 3 — declaration (ร่าง)
- doa: init module=policy (Document Control อยู่ใต้ governance · ผู้จัดการค่าเริ่ม role-compliance) · doa_type dar · 4 ขั้น: role-line-manager (ผู้ตรวจสอบ) → role-mgr-bu (ผู้อนุมัติ) → role-doc-controller (ผู้ควบคุมเอกสาร) → role-mgr-ocs (ผู้จัดการฝ่ายสำนักเลขานุการบริษัท) · init เขียน on_reject: draft → แก้เป็น back_to_draft · validate WARN G1 (role-doc-controller · role-mgr-ocs นอก contract) · BLOCK 0
- ntf: dar_cancelled (→ ผู้พิจารณาขั้นปัจจุบัน) · dar_distributed (approved → หน่วยงานที่แจกจ่าย + อีเมลที่ระบุ · บังคับ) · dar_received (ลงนามรับ → เจ้าของ + ผู้ควบคุมเอกสาร) · ตัด over_limit (ไม่มีเกณฑ์ตัวเลข)
- doccfg + mdoc ทำหลังขั้น 4
- 2026-10-10 09:38 · ขั้น 3 → done · doa WARN (role-doc-controller · role-mgr-ocs นอก contract) BLOCK 0 · ntf PASS · doccfg/mdoc หลังขั้น 4

## ขั้น 4 — แบบพิมพ์ Replica (ทำต่อจาก agent ก่อน)
- ใช้ form.tpl.html / make_data.py ที่ agent ก่อนร่างไว้ (R9 ตารางกรอบ + R10 2 หน้า · ตัดหน้าก่อนส่วนแจกจ่าย · บล็อกลงชื่อทั้งก้อนหน้า 2 · หัวตารางซ้ำ · "หน้า 1/2")
- แก้ profile: form_logo_align flex-start → left (build_html ไม่รับ)
- สถานะ long ล้นเป็น 3 หน้า (แถวแก้ไข 10 + เอกสารเกี่ยวข้อง 14 บนหน้า 1) → เพิ่ม print_config.page1_row_budget = 22 (แถวแก้ไข + แถวเอกสารเกี่ยวข้องบนหน้า 1) ส่วนเกินไปตารางต่อหน้า 2 → ทุกสถานะ 2 หน้า
- parity_check: IDENTICAL 5/5 · ไม่มี {{}} หลง · ฟอนต์ 8.5pt
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py เรียกภายใน — แทนด้วย .scratch/render_states_nobrowser.py: render_doc + build_html ทางการ + weasyprint พรีวิวนับหน้า · ไม่ใช่ด่านทางการ) → 5 สถานะ = 2 หน้าเท่ากัน · out/_states_sheet.png (พรีวิว weasyprint)
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ approved.pdf จาก Chromium) — คาด WARN เพราะเปลี่ยน A4 แนวนอน → แนวตั้ง 2 หน้า · เหตุผลอยู่ใน DAR_print-spec.md §7
- build_html → print/DAR_template.html · DAR_print-spec.md · DAR_data-contract.md
- doccfg init (module CCC · code DAR) → brief --registry PASS · mdoc brief WARN (G04 taxonomy_def_id ว่าง · G09 doa pending) · doa validate --print-config WARN (role-doc-controller · role-mgr-ocs นอก contract) BLOCK 0
- 2026-10-10 12:14 · ขั้น 4 → done · R10 2 หน้า ทุกสถานะ (พรีวิว weasyprint) · parity 5/5 · [NO-BROWSER] ข้าม render_pdf/compare_original · doccfg PASS · mdoc WARN · doa WARN BLOCK 0

## ขั้น 5 · HTML Q-form (html-generator v9.4)
- build: .build/build_feature.py ประกอบจาก canonical references/form-archetype (shell + BASE-KIT) + be-datepicker + tpl_render.js (verbatim) + app DAR (.build/patch_app.py: โครง Q-form ของ J005 ITCR + p_head/p_view/p_print/p_wiz/p_act.js) + extra.css (Group 25 + DAR) · PDF tab ฝัง print/form.tpl.html + docPrintData() · โลโก้ = placeholder (ไม่ใช้โลโก้ลูกค้า · ระบบจริงอ่าน Organization)
- เปิด GOLDEN_SKELETON.html + ui-standard-list-drawer.md U1–U28 เทียบก่อน build (โครงจาก J005 ที่เทียบแล้ว)
- ช่องตามกระดาษ 1:1 (#106): ถึง/วันที่เขียน/ผู้เขียน/ฝ่าย/แผนก/DAR.No. = ระบบใส่ (การ์ดสรุป) · กรอก: วัตถุประสงค์ ◉4 · ISSUE ◉4 · Document No. · Revision · ชื่อเอกสาร · วันบังคับใช้ (bedateHTML) · ขั้นตอนใน PL/WI · ที่มา ◉4 + รายละเอียด · เดิม/ใหม่ · เอกสารเกี่ยวข้อง (แถวไม่จำกัด) · แจกจ่าย ☐27 · หมายเหตุ · วิธีรับ ☐2 · E-Mail · ไม่มีช่องเพิ่ม
- flow: ร่าง → รออนุมัติ (4 ขั้นเรียง · dynamic เลือกผู้พิจารณาต่อขั้น) → อนุมัติแล้ว·รอลงนามรับ (dar_distributed) → ลงนามรับแล้ว (Document Control Center บันทึกผู้รับ · dar_received · ไม่ใช่ขั้น DOA) · ไม่อนุมัติ = กลับร่างเลขเดิม + แบนเนอร์เหตุผล · ยกเลิก (ร่าง/รออนุมัติ · เจ้าของ+admin · เหตุผลบังคับ)
- ตีความ (unattended): "ลงนามรับ" ให้ admin role (Document Control Center) บันทึกแทนผู้รับ เพื่อคง G8 (ผู้รับในหน่วยงานแจกจ่ายไม่เห็นใบ) → OQ ให้ลูกค้ายืนยัน
- audit.sh: FAIL 0 · WARN 3 (มาจาก BASE-KIT กลาง: comment lucide · .uc-email · font-size px ใน shell) → reports/audit.txt · prune_css ตัด 77 rule → audit ซ้ำ FAIL 0 · มี meta cube-archetype + window.__QA__
- [NO-BROWSER] ข้าม e2e_standard.py · ข้าม render-check.py บนเครื่องงาน
- ตรวจเบื้องต้นนอกเครื่องงาน (Chromium ใน container ของ agent · ไม่ใช่ด่านทางการ): e2e_standard 21/21 · flow 27/27 · parity printData JS → render_doc IDENTICAL 3/3 → reports/precheck_outside.txt
- U1–U28: U1✓ U2✓ U3✓ U4✓ U5✓ U6✓ U7✓ U8✓ U9✓ U10✓ U11✓(kit) U12✓ U13✓(summary+timeline+emp-chip+ขั้นลงนามรับ) U14✓(wizard 1290 3 ขั้น) U15✓ U16 n/a(ไม่มีลบ ใช้ยกเลิก) U17✓ U18✓ U19✓(sub = Document No. · ชื่อเอกสาร) U20✓(ทั้งหมด/รอฉันดำเนินการ/ใบ DAR ของฉัน) U21✓ U22✓ U23✓(empty state + empty-mini ตารางย่อย) U24✓ U25✓ U26–U28 n/a(ไม่มีหน้าตั้งค่า)
- 2026-10-10 12:24 · ขั้น 5 → done · audit FAIL 0 · U1–U28 ✓ · [NO-BROWSER] e2e/render-check ข้าม (pre-check นอกเครื่อง e2e 21/21 · flow 27/27 · parity 3/3)
- 2026-10-10 12:24 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-007.md/.docx (brd-generator-full v2.3 Prebrief Mode · Lane · md_to_docx.py) — AI Review C01–C23 + PE01–PE05 → **APPROVED** (C16 ไม่มีรหัสใน registry = ยอมรับใน Prebrief Mode · ตัวชี้วัดไม่มีใน input → OQ-01)
- FRD_F-TMP-007_Pack (frd-generator-v6.2 Input Mode 0 · FULL variant: states=5 + approval) 00–07 + INDEX + declarations/ · 07 §7.0 = แถว DEC จาก DECISIONS.lock.md ตรงตัว (16)
- FRD บรรยายสาย DOA ตรงมติ DEC-03 (4 ขั้น role-line-manager ผู้ตรวจสอบ → role-mgr-bu ผู้อนุมัติ → role-doc-controller ผู้ควบคุมเอกสาร → role-mgr-ocs ผู้จัดการฝ่ายสำนักเลขานุการบริษัท · ไม่อนุมัติขั้นใดก็ได้ → draft เลขเดิม DEC-08) · ลงนามรับ = ไม่ใช่ขั้น DOA (บทเรียน K2/K7)
- frd_lint Section N: BLOCK 0 · WARN 0 · PASS 13 → reports/_SECTION_N.md
- declaration --final: doccfg PASS (--registry · DAR ไม่ชน · frd_ref FN-02/FN-04 · print_config.pages 2) · ntf PASS (frd_ref FN-06/FN-04/FN-08) · doa brief WARN (role-doc-controller · role-mgr-ocs นอก contract · --print-config --html) BLOCK 0 · mdoc WARN G04 (ไม่มี taxonomy_def_id) + G09 (doa pending) — อธิบายได้
- OQ ใหม่: OQ-04 หน่วยงานแจกจ่ายชุดซ้ำ · OQ-05 ผู้รับกดลงนามรับเอง · OQ-06 เชื่อมทะเบียนเอกสารควบคุม · OQ-07 รหัส feature จริง
- 2026-10-10 12:30 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · declaration final BLOCK 0 (doa WARN role-doc-controller/role-mgr-ocs · mdoc WARN G04/G09)

## ขั้น 8 · UI Brief → test case AI → UAT
- extract_anchors → reports/inventory.json · UI_BRIEF_F-TMP-007.md (§0–§13 · CSS vars/z-index/microcopy สกัดจาก inventory ด้วย .build/gen_ui_brief.py) → brief_check: PASS · FAIL 0 · WARN 0 → reports/ui_brief_check.md (รอบแรก FAIL B5 anchor `#f-emails` สร้างจาก template → เปลี่ยนเป็นอ้าง `fld('emails')`)
- testcases-F-TMP-007.md: 69 เคส / 238 step (L12 C8 V8 F3 D4 A5 K4 G3 P7 R6 E5 X4) · tc_lint ERROR 0 · Coverage Ledger + Audit (S 16/16 · BR 18/18 · VR 13/13 · EC 16/17 · DEC 16/16 · XT 4/4 · ข้าม EC-12 พร้อมเหตุผล)
- [NO-BROWSER] ข้าม verify_anchors.py บนเครื่องงาน · ตรวจเบื้องต้นนอกเครื่องงาน (Chromium ใน container ของ agent): DOM 371 · SOURCE 83 · PATTERN 8 · DATA 218 · MISSING 0 (รอบแรก MISSING 2 ข้อความแบนเนอร์ dynamic → ปรับ anchor) — ไม่ใช่ผลด่านทางการ
- UAT (qa-friendly v3.1 Lite): cases.json 58 เคส · drop ledger 11 (คำสั่งหลังบ้าน/จำลอง/แจ้งเตือนจริง/ตั้งค่าเอกสาร) · lite_audit หายเงียบ 0 + stamp md5 · build testcase-F-TMP-007.html · manifest testcases_ai / testcases_uat
- [NO-BROWSER] ข้าม capture.py → ไม่มีภาพหน้าจอ (regionKey ว่างทุก step · shots_b64.json = {})
- 2026-10-10 12:38 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 (69 เคส) · lite_audit หายเงียบ 0 · [NO-BROWSER] verify_anchors/capture ข้าม (pre-check นอกเครื่อง MISSING 0)

## ขั้น 9 · ตรวจรวม + แพ็ก
- manifest_scan (40 artifact · ซ้ำ 0) + เพิ่มเข้า manifest: print/out/_states_sheet.png (พรีวิว weasyprint — ไม่ใช่ PDF ทางการ) · DAR_data-contract.md · RUN_STATE.json · reports (precheck_outside · ui_brief_check · audit)
- consistency_check: **READY** · BLOCK 0 · WARN 1 (K9 ไม่มี report e2e_standard — [NO-BROWSER]) · PASS 9
- `dm.sh pack J007` → _pack/F-TMP-007_DevPack.zip (แพ็กแบบมีเงื่อนไข NO-BROWSER: ยังไม่มี PDF ทางการ/e2e/ภาพ UAT — ต้องรันรอบเต็มบนเครื่องที่มี browser)
- ไม่รัน finish/report (ตัวคุมทำ) · รหัส DAR ยังไม่จดลง registry (finish จดให้)
- 2026-10-10 12:39 · ขั้น 9 → done · consistency READY (BLOCK 0 · WARN K9 NO-BROWSER) · pack F-TMP-007_DevPack.zip (มีเงื่อนไข NO-BROWSER)
