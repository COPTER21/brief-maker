# RUN_LOG — F-TMP-001 FM-ASM-03 แบบฟอร์มใบแจ้งซ่อมสินทรัพย์ (REQ-TMP-001)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพฟอร์ม: `to_image.py` (LibreOffice → PDF → page-1.png) · ฟอนต์ไทยในภาพเป็นกล่อง (เครื่องไม่มีฟอนต์ Noto Sans Thai) → ถ้อยคำยึด content.html + sharedStrings · ตำแหน่ง/เส้นยึดภาพ
- ชื่อเอกสารอยู่ใน text box หัวกระดาษ: "แบบฟอร์มใบแจ้งซ่อมสินทรัพย์" · footer ขวา "Doc. No. : FM-ASM-03" · ไม่มี Rev.
- FORM_SPEC 14 ช่อง · แถวซ้ำ 2 (รายการ 10 แถว · ประวัติซ่อม 6 แถว) · ลายเซ็น 4 · form_spec_check ERROR 0 · ไม่มี PREBRIEF CMS → สร้าง PREBRIEF v2
- ไม่มีข้อมูลส่วนบุคคลในต้นฉบับ (ฟอร์มเปล่า)
- แก้ impact_summary.py: regex REQ รองรับรหัสชั่วคราว (`REQ-[\w-]+` แทน `REQ-[\d-]+`) — REQ-TMP-001 อ่านไม่ได้
- 2026-10-10 23:49 · ขั้น 1 → done · FORM_SPEC ERROR 0 · 14 ช่อง · PREBRIEF v2

## ขั้น 2 · gate (unattended · AI-DEFAULT)
- G1 ไม่เปลี่ยน config ไม่ส่งต่อ — ใบแจ้งซ่อมเป็นเอกสารภายใน · Asset Master/Maintenance Schedule ยังไม่มีในระบบ
- G2 dynamic 2 ขั้นตามช่องลงชื่อ: ผู้ตรวจสอบ = role-line-manager · ผู้อนุมัติ = role-mgr-acc (ผู้จัดการ module asset ตาม doa-roles-contract §3) · ไม่มีวงเงิน
- G3 ไม่มีสูตร/ค่าคงที่ · กฎตรวจ 4 ข้อ (≥1 แถว · จำนวน>0 · ทะเบียนสินทรัพย์กรอกเอง · ประวัติซ่อมผู้ตรวจสอบกรอก)
- G4 ไม่จำกัดแถว (PDF ขั้นต่ำ 10/6 แถว) · G5 1:1 · G6 แถวล่างต่อขั้น DOA ไม่ใช้ภาพ · G7 ไม่อนุมัติ → กลับร่าง เหตุผลบังคับ
- G8 เจ้าของ/ผู้อนุมัติหลังส่ง/admin ฝ่ายบริหารสินทรัพย์ · G9 ออกเลขตอนบันทึกแรก รหัส RPR (ASM ชนกับเอกสารแผนกเดียวกัน) · G10 แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- decisions_lock: 16 มติ · พร้อมเริ่มทำ · tag-ai-default → 12 มติ AI-DEFAULT (ที่เหลือ VALID จากข้อมูลตัวอย่าง)
- 2026-10-10 23:49 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · 16 มติ · AI-DEFAULT 12
- ขั้น 3: DOA_BRIEF PASS (แก้ on_reject → back_to_draft 1 รอบ) · NTF_BRIEF PASS 2 event (rpr_cancelled · rpr_ready_for_repair) · doccfg/mdoc ทำหลังแบบพิมพ์
- 2026-10-10 23:50 · ขั้น 3 → done · doa PASS · ntf PASS · doccfg/mdoc หลังขั้น 4

## ขั้น 4 · แบบพิมพ์ Replica
- template R4 (หัวเส้นประ) + R9 ตารางกรอบ 2 ตาราง (16 คอลัมน์เท่ากัน ใช้ colspan ตามสัดส่วนต้นฉบับ) + B6 sign_rows ในตารางกรอบ
- parity_check IDENTICAL 5/5 · render_doc --strict + build_html ครบ 5 สถานะ ไม่มี `{{}}` หลง · FM-ASM-03_template.html
- [NO-BROWSER] ข้าม render_states.py / render_pdf.py บนเครื่อง user — ทดแทนด้วยการ render HTML ชุดเดียวกัน (out/*.html) ผ่าน render_pdf.py ของสกิลบน Chromium ใน cloud container → PDF 5 สถานะ **1 หน้าทุกสถานะ** (max-pages 1) · _states_sheet.png ดูแล้ว (ไม่ล้น · ลายเซ็น 3 ช่อง / 7 ช่อง 4+3 ครบ)
- compare_original.py (container): WARN score 0.139 region 0:0.75 — เหตุผล: ภาพต้นฉบับมาจาก Excel scale 56% + ฟอนต์ไทยเป็นกล่อง (เครื่องไม่มี Noto Sans Thai) และเนื้อหาต้นฉบับกว้าง/สูงต่างสเกล → line match ต่ำ · ดู compare_side.png แล้ว ลำดับบล็อก/คอลัมน์/ถ้อยคำตรงต้นฉบับครบ · ความต่างตั้งใจ: ชื่อเอกสารกลางใต้โลโก้ · แถวลงชื่อล่างเป็นตารางกรอบต่อขั้น DOA + คำตัดสิน
- print_config: sign_boxes requester + doa_step:* · decision_words.by_role role-line-manager = ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ
- doccfg RPR PASS (registry ไม่ชน) · mdoc WARN (G04 taxonomy ว่าง · G09 doa pending) — source เปลี่ยนเป็น declaration เพราะ REQ-TMP-001 ไม่ใช่รูปแบบ REQ-YYYY-NNNN · doa validate + print_config PASS
- 2026-10-10 23:56 · ขั้น 4 → done · parity 5/5 · 1 หน้าทุกสถานะ (Chromium container) · compare WARN 0.14 อธิบายแล้ว · doccfg PASS · mdoc WARN · doa PASS

## ขั้น 5 · HTML Q-form (html-generator v9.4)
- ประกอบจาก canonical `_SOURCE_form-request-reference.html` (BASE-KIT ไม่แก้) + page CSS/app JS ของเอกสารนี้ (`build/build_feature.py`) · PDF tab = print/form.tpl.html + tplRender/tplSignRows + docPrintData
- audit.sh FAIL 0 · WARN 3 (มาจาก BASE-KIT: lucide w/h ใน kit · .uc-email · font-size ใน kit) · prune_css ตัด 25 rule แล้วรันซ้ำ FAIL 0
- [NO-BROWSER] ข้าม e2e_standard.py / render-check.py บนเครื่อง user — ทดแทนด้วย e2e_standard.py ของสกิลบน Chromium ใน cloud container: **21/21 ผ่าน** (ทั้งก่อนและหลัง prune) · reports/e2e_report.json · screenshot reports/shot_*.png
- U1–U28: U1 ✓ no-scorecard · U2 ✓ · U3 ✓ · U4 ✓ · U5 ✓ kebab ⋮ · U6 ✓ pager ทุกหน้า (25) · U7 ✓ CSV ที่ page head · U8 ✓ 920/wide 1290 · U9 ✓ เหตุผลบังคับ · U10 ✓ · U11 ✓ · U12 ✓ lucide mono · U13 ✓ timeline+emp-chip+progress · U14 ✓ Q-form wizard 3 ขั้น · U15 ✓ แก้ไข = wizard เดิม + prefill ปิด view ก่อน · U16 – (ไม่มีลบ — ใช้ยกเลิกเอกสาร DEC-09) · U17 ✓ คน = วงกลม icon · U18 ✓ 1 cell 1 บรรทัด · U19 ✓ header sub 1 fact · U20 ✓ seg tabs ทั้งหมด/รอฉันพิจารณา · U21 ✓ · U22 ✓ chip นับเดียว · U23 ✓ sub-table ว่างมีแผง · U24 ✓ combobox portal · U25 ✓ backdrop onmousedown · U26–U28 – (ไม่มีหน้าตั้งค่า)
- domain: รายการ 6 ช่อง = ตารางกรอก (#107) · ทะเบียนสินทรัพย์ = กรอกเอง (Asset Master ยังไม่มี) · ประวัติการซ่อม = ผู้ตรวจสอบ (ขั้นแรกของสาย) กรอกใน modal ตรวจสอบ ใช้ bedateHTML (#114) · ไม่อนุมัติ = กลับเป็นร่าง "ตีกลับแก้ไข" (DEC-09) · ไม่มีปุ่มทำซ้ำ (DEC-12)
- 2026-10-11 00:11 · ขั้น 5 → done · audit FAIL 0 · e2e 21/21 (Chromium container) · U1–U28 ✓
- 2026-10-11 00:11 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-001.md/.docx (brd-generator-full v2.3 Prebrief Mode · Lane) — AI Review C01–C23 + PE01–05 → **APPROVED** (C16 ไม่มี feature ใน FEATURE_REGISTRY = WARN ตาม v2.3 → OQ-05)
- FRD_F-TMP-001_Pack FULL (00–07 + INDEX) · Input Mode 0 · frd_lint Section N: **BLOCK 0 · WARN 0 · PASS 12**
- declaration --final: DOCCFG PASS (registry ไม่ชน · frd_ref FN-03/FN-05) · NTF PASS (frd_ref FN-05/07/09) · DOA PASS · MDOC WARN (G04 taxonomy ว่าง · G09 doa pending — ตามปิดก่อนเปิดใช้)
- 2026-10-11 00:16 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · declaration --final PASS

## ขั้น 8 · UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-001.md (html-ui-brief v1.1) · extract_anchors → brief_check: **PASS · FAIL 0 · WARN 0** (B1–B8)
- testcases-F-TMP-001.md (ai-testcase-md-generator v1.3 · Mode 0): 50 เคส / 150 step · tc_lint **ERROR 0**
- [NO-BROWSER] ข้าม verify_anchors.py บนเครื่อง user — ทดแทนด้วย Chromium ใน cloud container: DOM 177 · SOURCE 54 · PATTERN 3 · DATA 28 · **MISSING 0** (แก้หัว modal ที่ประกอบจาก template 3 จุด แล้วรันซ้ำ)
- testcase-F-TMP-001.html (qa-friendly v3.1 Lite): เก็บ 43 / drop ledger 7 (ระบบจำลอง/หลังบ้าน) · lite_audit **หายเงียบ 0** + stamp
- [NO-BROWSER] ข้าม capture.py — เอกสาร UAT ไม่มีภาพหน้าจอ (regionKey ว่างทุก step) · ภาพหน้าจอหลักอยู่ที่ reports/shot_*.png
- 2026-10-11 00:25 · ขั้น 8 → done · brief_check PASS · tc_lint 0 · anchors MISSING 0 · lite_audit 0
- ขั้น 9: K2 ไฟล์ซ้ำ → เปลี่ยนชื่อ build/UI_BRIEF…src.md → build/uibrief_source.md.txt · orig/content.html → orig/content_extract.html.txt (ไม่ใช่ฉบับส่งมอบ)
- ขั้น 9: consistency_check **READY · BLOCK 0 · WARN 0 · PASS 10** → dm.sh pack
- ขั้น 9: คัด PDF 5 สถานะ + _states_sheet + compare_side จาก print/out → print/ ให้ manifest_scan เก็บเข้า 07_Print · rescan หลังแก้ RUN_LOG (K3)
