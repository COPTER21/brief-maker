# RUN_LOG — F-TMP-007 FM-SAL-23 สรุปแบบประเมินความพึงพอใจ (ต่างประเทศ) (REQ-TMP-007)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · อ่านฟอร์ม (หมายเหตุ)
- ภาพหน้า: to_image.py ใช้ LibreOffice → PDF → pypdfium2 ได้ page-1.png (หน้าพิมพ์จาก Word 1 หน้า แนวนอน ไม่ใช่ภาพ HTML) · ฟอนต์ไทยไม่มีในเครื่อง → ตัวไทยเป็นกล่อง · ถ้อยคำยึด content.html · ตำแหน่ง/เส้นยึดภาพ
- content.html ใช้แล้วย้ายไป orig/out/content.html
- form.title จากหัวฟอร์ม: "แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าต่างประเทศ" · ชื่อในคิวไม่เพี้ยน → ไม่ rename
- โครงฟอร์ม: เมทริกซ์ หัวข้อ 10 ข้อใน 3 กลุ่ม (3+5+2 · ตรง q1–q10 ของ FM-SAL-22 SEA ที่เป็นอังกฤษ) × ลูกค้า 4 คอลัมน์ · แถวป้ายรวม "ระดับความพึงพอใจ" ใต้ชื่อลูกค้า · สรุปผลการประเมิน + ข้อเสนอแนะ (เส้นประ 4 บรรทัด) · ลงชื่อ 2 ช่อง: ผู้สรุปผลการประเมิน (Sales Administrative Manager · ซ้าย) · ผู้รับทราบและอนุมัติ (Managing Director · ขวา) · Doc No.FM-SAL-23 Rev.00 : 01/07/2569
- FORM_SPEC 14 ช่อง (ระบบ 11 · กรอก 3) · form_spec_check ERROR 0 · ไม่มี PREBRIEF CMS → PREBRIEF v2 (--cls FRM --module SALES)
- ข้อมูลส่วนบุคคล: หัวคอลัมน์มีชื่อลูกค้าจริง 4 ราย + ชื่อผู้ลงนามจริง 2 คน → ห้ามใช้เป็นข้อมูลตัวอย่าง (ใช้ชื่อสมมติทั้งหมด)
- 2026-10-10 18:24 · ขั้น 1 → done · FORM_SPEC 14 ช่อง ERROR 0 · title จากหัวฟอร์ม · PREBRIEF v2

## ขั้น 2 · gate (unattended — AI-DEFAULT ทุกหมวด)
- G1: ไม่เปลี่ยนค่า/ไม่ส่งต่อ — ใบสรุปอ่านผลจากแบบประเมิน SEA (FM-SAL-22) ที่บันทึกผลแล้วแบบอ่านอย่างเดียว
- G2: dynamic 1 ขั้นตามช่องลงชื่อ "ผู้รับทราบและอนุมัติ · Managing Director" → role-ceo (ไม่มี role "Managing Director" ใน doa-roles-contract — role ใกล้สุดชั่วคราว จดใน OQ · แนวเดียวกับ J005) · ผู้สรุป = Sales Administrative Manager → role-mgr-sales · ไม่มีวงเงิน
- G3: หัวข้อ 10 ข้อ 3 กลุ่ม + สเกล 1–5 อ่านจาก SalesConfig (ชุดเดียวกับ SEA) · ค่าคะแนนดึงจาก SEA บันทึกผลแล้ว อ่านอย่างเดียว พิมพ์เป็นตัวเลข · คะแนน 1–2 = เตือน ไม่บล็อก · ลูกค้าซ้ำ = บล็อก
- G4: คอลัมน์ลูกค้าสูงสุด 8/ใบ (เบี่ยงจากนโยบาย "ไม่จำกัด" — ตารางเป็นคอลัมน์ ขยายไม่จำกัดไม่ได้ → 2 ชุด × 4 คอลัมน์ตามกระดาษ · 2 หน้าคงที่ R10) · เกิน 8 ทำใบเพิ่ม → จดใน OQ
- G5: 1:1 + เพิ่ม "ประจำเดือน" (ใบสรุปต้องมีงวด) · G6: แถวล่าง ผู้สรุป + 1 ช่องต่อขั้น DOA ข้อความ ไม่ใช้ภาพ
- G7: ไม่อนุมัติ = กลับร่าง เลขเดิม · ยกเลิก owner+admin ร่าง/รออนุมัติ เหตุผลบังคับ · G8: เจ้าของ · ผู้อนุมัติหลังส่ง · role-mgr-sales เห็นทั้งหมด
- G9: ออกเลขตอนบันทึกครั้งแรก รหัส SES (ไม่ชน ACL/CSG/CSM/OTN/SDA/SDS/SEA · ไม่ใช้กลุ่ม MT.. ที่กันให้ J008) · G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock พร้อมเริ่มทำ · 15 มติ · AI-DEFAULT 11 · VALID 4
- 2026-10-10 18:24 · ขั้น 2 → done · 15 มติ · AI-DEFAULT 11 · VALID 4

## ขั้น 3 · declaration ร่าง
- DOA: dynamic 1 ขั้น role-ceo (ป้าย "ผู้รับทราบและอนุมัติ · Managing Director") · brief PASS · role-ceo = role ใกล้สุดชั่วคราว (ไม่มี MD ใน contract) → OQ
- NTF: ses_cancelled + ses_low_score_approved (อนุมัติแล้วมีช่องคะแนน 1–2 → เจ้าของ + role-mgr-sales) · ตัด ses_over_limit_approved (ไม่มีวงเงิน/เกณฑ์ตัวเลข) · brief PASS
- doccfg/mdoc ทำในขั้น 4 (ต้องใช้ print_config)
- 2026-10-10 18:25 · ขั้น 3 → done · doa PASS (role-ceo 1 ขั้น) · ntf PASS 2 event (doccfg/mdoc ทำในขั้น 4)

## ขั้น 4 · แบบพิมพ์ + doccfg/mdoc
- DOCCFG: SES · ออกเลขตอนบันทึกครั้งแรก · snapshot approved_final · brief --registry PASS (ไม่ชน ACL/CSG/CSM/OTN/SDA/SDS/SEA)
- MDOC: SES · class RPT · function_code F01 ชั่วคราว · WARN G04 (ยังไม่มี taxonomy_def_id) · G09 (doa pending) — ตามคาด
- DOA validate (print_config) PASS
- แบบพิมพ์ Replica R9 ตารางกรอบ + R10 **2 หน้า**: หน้า 1 = หัว + ประจำเดือน + ตาราง 2 ชุด × 4 คอลัมน์ (หัวตารางซ้ำ · แถวกลุ่ม 3 + หัวข้อ 10) · หน้า 2 = สรุปผล + ข้อเสนอแนะ + บล็อกลงชื่อ · ฟอนต์ 9pt · row 6mm
- ต้นฉบับแนวนอน แต่ engine thai-doc ล็อก A4 portrait → ออกแบบแนวตั้ง แบ่งคอลัมน์ลูกค้า (print-spec §7)
- parity_check IDENTICAL 5/5 · render_doc ไม่มี {{}} หลง · ไม่มี key ขาด · build_html 5 สถานะ (print/out/*.html) + FM-SAL-23_template.html
- [NO-BROWSER] ข้าม render_pdf.py (ส่วน PDF ของ render_states.py) บนเครื่อง user → สร้าง HTML ต่อสถานะด้วย render_doc + build_html แทน
- ตรวจเสริมในคอนเทนเนอร์ Claude (playwright chromium · ไม่ใช่ด่านทางการ · ไม่แพ็ก PDF): 5/5 สถานะ = 2 หน้า (out/_states_container.json) · _states_sheet.png ดูแล้ว · compare_original WARN 0.361 (แนวนอน vs แนวตั้ง — print-spec §7) · compare_side.png ดูแล้ว โครงตารางตรง
- [NO-BROWSER] ข้าม compare_original.py บนเครื่อง user (ไม่มี approved.pdf) — ต้องรันซ้ำบนเครื่องที่มี browser
- 2026-10-10 18:29 · ขั้น 4 → done · R10 2 หน้า · parity 5/5 · คอนเทนเนอร์ 5/5 = 2 หน้า · DOCCFG PASS · MDOC WARN G04/G09

## ขั้น 5 · HTML (html-generator v9.4 · Q-form)
- feature.html ประกอบจาก canonical `references/form-archetype/_SOURCE_form-request-reference.html` (shell + CSS + BASE-KIT) + script เฉพาะเอกสาร (`.build/app1–5.js` · `.build/build.py` — ต่อยอดจากโครงของ J005 FM-SAL-21 ที่ผ่านทุกด่าน แล้วปรับโดเมนเป็น SEA/SES) — เทียบ GOLDEN_SKELETON + U1–U28 ก่อน build
- โดเมน: ประจำเดือน (เพิ่ม · DEC-06/12) · ดึงแบบประเมิน SEA ที่บันทึกผลแล้วของเดือน (อ่านอย่างเดียว · ≤ 8 ราย · ลูกค้าซ้ำ = บล็อก DEC-14 · หลายใบใช้ใบล่าสุด · SEA ถูกยกเลิกหลังดึง = เตือน+บล็อกส่ง) · ตารางเมทริกซ์ แถวกลุ่ม 3 + หัวข้อ 10 × ลูกค้า (คะแนนตัวเลข 1–5 · คะแนน 1–2 ไฮไลต์) · สรุปผล (บังคับตอนส่ง · ≤ 1,000) · ข้อเสนอแนะ · DOA 1 ขั้น role-ceo คำตัดสิน "รับทราบและอนุมัติ" · ข้อมูลสมมติทั้งหมด
- PDF tab ฝัง print/form.tpl.html + tpl_render.js · docPrintData(r) ตาม print-spec §2 — parity JS ↔ render_doc.py IDENTICAL 11/11 seed (.build/print_parity_js.json)
- audit.sh FAIL 0 · WARN 3 (Rule #21 / #40 .uc-email / Token font-size — มาจาก shell+kit canonical) · self_audit PASS · prune_css ตัด 89 rule แล้ว audit/self_audit ซ้ำผ่าน · node --check ผ่าน · มี meta cube-archetype=Q-form + window.__QA__
- [NO-BROWSER] ข้าม e2e_standard.py · render-check.py บนเครื่อง user · ตรวจเสริมในคอนเทนเนอร์ Claude (ไฟล์หลัง prune): e2e_standard 21/21 → reports/e2e_container_ref.json (ไม่ใช่ report ทางการ) + flow สร้าง→ดึง 8 ราย→ส่ง→อนุมัติ→PDF ไม่มี pageerror · ภาพ reports/shot_view/shot_wizard/shot_pdf.png
- U1–U28: U1✓ U2✓ U3✓ U4✓ U5✓ U6✓(pager + page-size) U7✓ U8✓ U9✓ U10✓(ไฮไลต์คะแนนต่ำ = token) U11✓ U12✓ U13✓ U14✓(Q2 wizard 3 ขั้น) U15✓ U16 n/a(ไม่มีลบ · ยกเลิกมีเหตุผล) U17✓ U18✓ U19✓ U20✓(ไม่มี page tabs) U21✓(kit WARN token) U22✓ U23✓ U24✓ U25✓ U26–U28 n/a(ไม่มีหน้า config)
- 2026-10-10 18:34 · ขั้น 5 → done · audit FAIL 0 · self_audit PASS · [NO-BROWSER] e2e ข้าม · คอนเทนเนอร์ 21/21
- 2026-10-10 18:34 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-007.md/.docx (brd-generator-full v2.3 Prebrief Mode · Lane · md_to_docx ผ่าน · โครงต่อยอดจาก BRD J005 แล้วปรับโดเมน SEA/SES ทั้งฉบับ) · AI Review C1–C23 → APPROVED (C16 WARN: รหัส feature ชั่วคราว) · DEC-01..15 อยู่ใน §2.4 แยกรายข้อ
- FRD_F-TMP-007_Pack (frd-generator-v6.2 Input Mode 0 · FULL) 00–07 + INDEX · 07 §7.0 สร้างจาก DECISIONS.lock.json ตรงตัว · ฟิลด์ DOA (approval_chain/approver_role/approved_by + TODO: DOA engine) อยู่ใน 02 §2.3 และ 04_DB (เอกสารนี้มีการอนุมัติจริง + มี DOA_BRIEF → K7 ไม่ควร BLOCK)
- ข้อมูลทดสอบ 06 §6.3 ตรวจกับ prototype ในคอนเทนเนอร์: ก.ย. 69 มี SEA บันทึกผลแล้ว 12 ราย → ดึง 8 เหลือ 4 · C03 2 ใบ · C09 ถูกยกเลิก
- frd_lint: BLOCK 0 · WARN 0 · PASS 13 → reports/_SECTION_N.md
- declaration --final: DOCCFG PASS (registry ไม่ชน · frd_ref FN-03/FN-05 · module SAL ตาม J005) · NTF PASS (frd_ref FN-05/06/08) · DOA validate (print_config + feature.html) PASS · MDOC WARN (G04 taxonomy · G09 doa pending — ตามคาด) · คัดลง FRD_Pack/declarations/
- 2026-10-10 18:38 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · declaration --final PASS · MDOC WARN G04/G09

## ขั้น 8 · UI Brief → test case AI → UAT
- extract_anchors → reports/inventory.json · UI_BRIEF_F-TMP-007.md (§0–§13 · .build/make_brief.py) · brief_check PASS FAIL 0 · WARN 0 → reports/brief_check.md
- testcases-F-TMP-007.md 45 เคส / 132 step · tc_lint ERROR 0 · Coverage AC 14/14 · BR 15/15 · VR 7/7 · EC 11/12 (EC-01 ข้ามพร้อมเหตุผล) · TC-D 6/6 · DEC 15/15 · ค่าคาดหวังหลัก (จำนวนแถว/badge/toast ดึง 8 เหลือ 4 · ส.ค. เหลือ 6 · ล้าง 8 ราย · คะแนนต่ำ 4 ช่อง · เลข SEA ของลูกค้า 01/03 · ช่องคะแนน 1–2 = 6) ตรวจกับ prototype ในคอนเทนเนอร์แล้ว
- [NO-BROWSER] ข้าม verify_anchors.py (anchor เขียนจากข้อความใน feature.html โดยตรง · ตรวจด้วย brief_check + ค่าจาก prototype ในคอนเทนเนอร์แทน)
- UAT Lite: cases.json 38 เคส · drop ledger 7 (QA_AUDIT_F-TMP-007.md) · lite_audit หายเงียบ 0 · --stamp แล้ว
- [NO-BROWSER] ข้าม capture.py → build testcase-F-TMP-007.html ด้วย shots ว่าง (ไม่มีภาพหน้าจอในเอกสารคน)
- 2026-10-10 18:40 · ขั้น 8 → done · brief_check PASS · tc_lint 45 เคส ERROR 0 · lite_audit หายเงียบ 0 · verify_anchors/capture ข้าม (NO-BROWSER)
