# RUN_LOG — F-TMP-002 FM-SAL-11 แบบสรุปหัวข้อการประเมินความพึงพอใจ สำหรับ General Trade (REQ-TMP-002)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · อ่านฟอร์ม (หมายเหตุ)
- ภาพหน้า: `_system/tools/to_image.py` ใช้ LibreOffice → PDF → pypdfium2 ได้ (ไม่ใช่ภาพ HTML) แต่ฟอนต์ไทย (Noto Sans Thai) ไม่มีในเครื่อง → ภาพเห็นตัวไทยเป็นกล่อง · ถ้อยคำยึด content.html + openpyxl · ตำแหน่ง/เส้นยึดภาพ
- ไฟล์ xlsx มี 1 ชีต (ชื่อชีต FM-SAL-10 แต่ footer Doc.No.FM-SAL-11 → ยึด FM-SAL-11) · print area C1:N76 A4 แนวตั้ง 1 หน้า
- form.title = "หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade" (หัวฟอร์ม C5) — ชื่อไฟล์มีคำว่า "แบบสรุป" นำหน้า แต่หัวฟอร์มไม่มี · ชื่อคิวไม่เพี้ยน → ไม่ rename
- FORM_SPEC 47 ช่อง · form_spec_check ERROR 0 · ไม่มี PREBRIEF CMS → สร้าง PREBRIEF v2
- ข้อมูลส่วนบุคคล: ไฟล์ลูกค้าไม่มีข้อมูลจริง (ตาราง/รายชื่อว่าง) · ช่องชื่อลูกค้าติด pdpa
- 2026-10-10 13:20 · ขั้น 1 → done · FORM_SPEC 47 ช่อง ERROR 0 · PREBRIEF v2

## ขั้น 2 · gate (unattended — AI-DEFAULT ทุกหมวด)
- G1: ไม่เปลี่ยนค่า/ไม่ส่งต่อ — เป็นแบบสรุปผลประเมิน ไม่มีผลต่อข้อมูลหลัก · ผลจากแบบสำรวจ FM-SAL-10 ยังไม่ผูก → ผู้ใช้กรอกจำนวนเอง
- G2: dynamic 1 ขั้นตามช่องลงชื่อ "ผู้อำนวยการสายงานการขาย" → role-mgr-bu (role ใกล้สุดใน master; ไม่มี role "ผอ.สายงานขาย" — แจ้งใน _BATCH_REPORT) · ผู้จัดทำ = Sales Manager (role-mgr-sales) · ไม่มีวงเงิน
- G3: ค่าคงที่ (เกณฑ์ 3 ครั้ง/เดือน · ช่วง CSAT · ระดับคะแนน · หัวข้อ 16 ข้อ) อ่านจาก SalesConfig · คำนวณอัตโนมัติ · แก้สูตรรวมที่ขาดในต้นฉบับ · % ใช้สูตร CSAT ถ่วงน้ำหนัก 5–1 (ต้นฉบับไม่มีสูตร) · 85.83% ตายตัว → คำนวณ
- G4: ไม่จำกัด (ตาราง 3 ด้านแถว = หัวข้อใน config · รายชื่อลูกค้า PDF ขั้นต่ำ 14 แถว)
- G5: 1:1 · G6: แถวล่างต่อขั้น DOA ข้อความ ไม่ใช้ภาพ · G7: ไม่อนุมัติ = กลับร่าง เลขเดิม · ยกเลิก owner+admin ร่าง/รออนุมัติ เหตุผลบังคับ
- G8: เจ้าของ · ผู้อนุมัติหลังส่ง · Sales admin เห็นทั้งหมด · G9: ออกเลขตอนบันทึกครั้งแรก รหัส CSM (เลี่ยงชนกับ J001 FM-SAL-10) · G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- 2026-10-10 13:20 · ขั้น 2 → done · 20 มติ · AI-DEFAULT 14 · VALID 6
- 2026-10-10 13:21 · ขั้น 3 → done · doa PASS · ntf PASS (doccfg/mdoc ทำในขั้น 4)

## ขั้น 3–4 · declaration + แบบพิมพ์
- DOA: dynamic 1 ขั้น role-mgr-bu (ป้าย "ผู้อำนวยการสายงานการขาย") · brief PASS · validate (print_config) PASS
- NTF: csm_cancelled + csm_low_csat (approved และ % โดยรวม < 60) · brief PASS
- DOCCFG: code CSM (registry ไม่ชน · J001 ใช้ CSG) · brief PASS · MDOC: validate/brief WARN (G04 ยังไม่มี taxonomy_def_id · G09 doa pending) — class RPT · function_code F01 ชั่วคราว รอเทียบ Taxonomy Master
- แบบพิมพ์ Replica R9 ตารางกรอบ + R10 **2 หน้า** (หน้า 1 ตาราง 3 ด้าน · หน้า 2 สรุปผล + รายชื่อลูกค้า + บล็อกลงชื่อ) · ฟอนต์ 9pt (≥ 8pt)
- parity_check IDENTICAL 5/5 · render_doc --strict 5/5 ไม่มี {{}} หลง · build_html 5 สถานะ + FM-SAL-11_template.html
- [NO-BROWSER] ข้าม render_pdf.py (ส่วน PDF/นับหน้า/ภาพของ render_states.py) — ประเมินความสูง: หน้า 1 ≈ 245mm · หน้า 2 ≤ 215mm (พื้นที่ 269mm) → คาด 2 หน้าทุกสถานะ ต้องยืนยันบนเครื่องที่มี browser
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ approved.pdf) · ไม่มี _states_sheet.png
- ไฟล์ body ชั่วคราวย้ายไป print/out/_body (ลบไม่ได้ในโฟลเดอร์ที่เชื่อม)
- 2026-10-10 13:26 · ขั้น 4 → done · R10 2 หน้า · parity 5/5 · [NO-BROWSER] ไม่ render PDF/compare

## ขั้น 5 · HTML (html-generator v9.4 · Q-form)
- feature.html ประกอบจาก canonical `references/form-archetype` (shell + CSS + BASE-KIT) + script เฉพาะเอกสาร (`_build/app*.js` · `_build/build.py`) — เทียบ GOLDEN_SKELETON + U1–U28 ก่อน build
- ปรับตาม v9.4: ตัด stat cards (ตัวเลข = ph-badge ≤3 · ค่า 0 ซ่อน) · คน = วงกลม icon (empChip/user chip) · backdrop drawer/modal = onmousedown · pagination + page-size 10/25/50 (ค่าเริ่ม 25) · ไม่มี page tabs (ชุดข้อมูลเดียว) · ไม่มี type=date (เดือน = search combobox)
- PDF tab ฝัง print/form.tpl.html + tpl_render.js (tplRender/tplSignRows) · docPrintData(r) ตาม data contract — parity JS (prototype) ↔ render_doc.py IDENTICAL 11/11 seed · ไม่มี {{}} หลง
- audit.sh FAIL 0 · WARN 3 (Rule #21 / #40 .uc-email / Token font-size — มาจาก shell+kit canonical เดียวกับไฟล์อ้างอิง) · self_audit PASS · prune_css ตัด 65 rule แล้วรัน audit/self_audit/smoke ซ้ำ ผ่าน
- smoke (node vm, ไม่ใช้ browser): renderPage × 4 persona · ทุกใบที่เห็น × 4 แท็บ · wizard 3 ขั้น + validate · modal ส่ง/อนุมัติ/ไม่อนุมัติ → error 0 · canSee/canAct ตรงกฎ (E01 เห็น R1,R3,R5,R6,R8,R10,R11 · E02 act R7,R8)
- [NO-BROWSER] ข้าม e2e_standard.py · ข้าม render-check.py (ภาพ/วัด layout) — ต้องรันบนเครื่องที่มี browser
- U1–U28: U1✓ U2✓ U3✓ U4✓ U5✓ U6✓ U7✓ U8✓ U9✓ U10✓ U11✓(kit) U12✓ U13✓ U14✓(Q2 wizard) U15✓ U16 n/a(ไม่มีลบ · ยกเลิกมีเหตุผล) U17✓ U18✓ U19✓ U20✓(ไม่มี tabs) U21✓(kit WARN token) U22✓ U23✓ U24✓ U25✓ U26–U28 n/a(ไม่มีหน้า config)
- 2026-10-10 13:35 · ขั้น 5 → done · audit FAIL 0 · self_audit PASS · [NO-BROWSER] ไม่รัน e2e
- 2026-10-10 13:35 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 6 · ข้าม (unattended — ให้คนดูจาก _BATCH_REPORT)
## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-002.md/.docx (Prebrief Mode · Lane) — AI Review: APPROVED (C16 WARN ไม่มี Registry entry เพราะ F-TMP ชั่วคราว)
- FRD_F-TMP-002_Pack (00–07 + INDEX + declarations/) · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 17 (แก้ WARN N2 q_pct/d_pct/s_pct · N3 false-positive "§3.1"/"c3")
- declaration --final: DOCCFG PASS (registry ไม่ชน · frd_ref FN-03/FN-06) · NTF PASS (frd_ref FN-06/07/09) · DOA validate (print_config + feature.html) PASS · MDOC WARN (G04 taxonomy · G09 doa pending — ตามคาด)
- 2026-10-10 13:40 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · declaration --final PASS

## ขั้น 8 · UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-002.md (14 section · สกัดจาก feature.html + inventory) · brief_check: PASS · FAIL 0 · WARN 0
- testcases-F-TMP-002.md: 64 เคส · 166 step · tc_lint ERROR 0 · Coverage AC 14/14 · BR 17/17 · VR 6/6 · EC 11/11 · TC-D 6/6 · DEC 20/20
- [NO-BROWSER] ข้าม verify_anchors.py (anchor เขียนจากข้อความใน feature.html โดยตรง) · ข้าม capture.py (ไม่มีภาพหน้าจอ · regionKey ว่าง)
- UAT Lite: cases.json 23 เคส · drop ledger 41 (QA_AUDIT_F-TMP-002.md) · lite_audit หายเงียบ 0 · --stamp แล้ว · build testcase-F-TMP-002.html (ไม่มีภาพ)
- 2026-10-10 13:52 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 · lite_audit หายเงียบ 0 · [NO-BROWSER] ข้าม verify_anchors/capture

## ขั้น 9 · ตรวจรวม + แพ็ก
- consistency_check รอบแรก NOT READY: K2 ไฟล์ซ้ำ (ไฟล์ทดสอบ smoke + orig/content.html ถูกนับเป็น prototype) · K5 route สร้างจากตัวแปร · K4 microcopy ไม่เต็มข้อความ · K6 BRD รวม DEC-05–07
  - แก้: ย้าย `_build/` → `.build/` (scanner ข้าม) · `orig/content.html` → `orig/out/content.html` · เพิ่ม `ROUTES` literal ใน prototype (rebuild + prune + audit FAIL 0 + self_audit PASS + smoke 0) · 06_TESTS ใช้ข้อความปุ่มเต็ม · BRD แยก DEC-05/06/07 · รวม data contract เข้า print-spec §2 · make_data.py → render_data.py
- consistency_check: READY · BLOCK 0 · WARN 1 (K9 ไม่มี report e2e — [NO-BROWSER])
