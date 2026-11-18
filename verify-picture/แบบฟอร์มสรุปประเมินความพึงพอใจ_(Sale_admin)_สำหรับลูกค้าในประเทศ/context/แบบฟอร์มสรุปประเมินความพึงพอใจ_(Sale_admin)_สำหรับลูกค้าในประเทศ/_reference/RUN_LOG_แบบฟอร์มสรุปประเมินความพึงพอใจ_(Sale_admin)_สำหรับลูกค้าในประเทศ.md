# RUN_LOG — F-TMP-005 FM-SAL-21 สรุปแบบประเมินความพึงพอใจ (ในประเทศ) (REQ-TMP-005)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · อ่านฟอร์ม (หมายเหตุ)
- ภาพหน้า: to_image.py ใช้ LibreOffice → PDF → pypdfium2 ได้ page-1.png (หน้าพิมพ์จาก Word 1 หน้า แนวนอน ไม่ใช่ภาพ HTML) · ฟอนต์ไทยไม่มีในเครื่อง → ตัวไทยเป็นกล่อง · ถ้อยคำยึด content.html · ตำแหน่ง/เส้นยึดภาพ
- content.html ใช้แล้วย้ายไป orig/out/content.html · สคริปต์ช่วย + ไฟล์ชั่วคราวอยู่ orig/out/ (ลบไม่ได้)
- form.title จากหัวฟอร์ม: "แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าในประเทศ" · ชื่อในคิวไม่เพี้ยน → ไม่ rename
- โครงฟอร์ม: เมทริกซ์ หัวข้อ 5 ข้อ (แถว · ตรง q1–q5 ของ FM-SAL-20 SDA) × ลูกค้า 6 คอลัมน์ · แถวว่างใต้ชื่อลูกค้า 1 แถว (ไม่มีป้าย) · สรุปผลการประเมิน + ข้อเสนอแนะ (เส้นประ 4 บรรทัด) · ลงชื่อ 2 ช่อง: ผู้สรุปผลการประเมิน (Sales Administrative Manager) · ผู้รับทราบและอนุมัติ (Managing Director) · Doc No.FM-SAL-21 Rev.00 : 01/07/2569
- FORM_SPEC 10 ช่อง (ระบบ 7 · กรอก 3) · form_spec_check ERROR 0 · ไม่มี PREBRIEF CMS → PREBRIEF v2 (--cls FRM --module SALES)
- ข้อมูลส่วนบุคคล: หัวคอลัมน์มีชื่อลูกค้าจริง (นิติบุคคล + บุคคลธรรมดา) และชื่อผู้ลงนามจริง 2 คน → pdpa · ห้ามใช้เป็นข้อมูลตัวอย่าง (ใช้ชื่อสมมติทั้งหมด)
- 2026-10-10 17:46 · ขั้น 1 → done · FORM_SPEC 10 ช่อง ERROR 0 · title จากหัวฟอร์ม · PREBRIEF v2

## ขั้น 2 · gate (unattended — AI-DEFAULT ทุกหมวด)
- G1: ไม่เปลี่ยนค่า/ไม่ส่งต่อ — ใบสรุปอ่านผลจากแบบประเมิน SDA (FM-SAL-20) ที่บันทึกผลแล้วแบบอ่านอย่างเดียว
- G2: dynamic 1 ขั้นตามช่องลงชื่อ "ผู้รับทราบและอนุมัติ · Managing Director" → role-ceo (ไม่มี role "Managing Director" ใน doa-roles-contract — ใช้ role ใกล้สุดชั่วคราว จดใน OQ) · ผู้สรุป = Sales Administrative Manager → role-mgr-sales · ไม่มีวงเงิน
- G3: หัวข้อ 5 ข้อ + สเกล 5 ระดับ อ่านจาก SalesConfig (ชุดเดียวกับ SDA) · ค่าคะแนนดึงจาก SDA บันทึกผลแล้ว อ่านอย่างเดียว · ระดับต่ำ = เตือน ไม่บล็อก · ลูกค้าซ้ำ = บล็อก (DEC-12)
- G4: คอลัมน์ลูกค้าสูงสุด 12/ใบ (เบี่ยงจากนโยบาย "ไม่จำกัด" — เหตุผล: ตารางเป็นคอลัมน์ แบบพิมพ์ขยายไม่จำกัดไม่ได้ → ออกแบบ 2 ชุด × 6 คอลัมน์ ตามความกว้างกระดาษ · 2 หน้าคงที่ R10) · เกิน 12 ทำใบเพิ่ม → จดใน OQ
- G5: 1:1 + เพิ่ม "ประจำเดือน" (ใบสรุปต้องมีงวด) · G6: แถวล่าง ผู้สรุป + 1 ช่องต่อขั้น DOA ข้อความ ไม่ใช้ภาพ
- G7: ไม่อนุมัติ = กลับร่าง เลขเดิม · ยกเลิก owner+admin ร่าง/รออนุมัติ เหตุผลบังคับ · G8: เจ้าของ · ผู้อนุมัติหลังส่ง · role-mgr-sales เห็นทั้งหมด
- G9: ออกเลขตอนบันทึกครั้งแรก รหัส SDS (ไม่ชน ACL/CSG/CSM/OTN/SDA · เว้น SEA/SES ให้ FM-SAL-22/23) · G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock พร้อมเริ่มทำ · 16 มติ · AI-DEFAULT 11 · VALID 5
- 2026-10-10 17:47 · ขั้น 2 → done · 16 มติ · AI-DEFAULT 11 · VALID 5
- 2026-10-10 17:48 · ขั้น 3 → done · doa PASS (role-ceo 1 ขั้น) · ntf PASS 2 event (doccfg/mdoc ทำในขั้น 4)

## ขั้น 3–4 · declaration + แบบพิมพ์
- DOA: dynamic 1 ขั้น role-ceo (ป้าย "ผู้รับทราบและอนุมัติ · Managing Director") · brief PASS · validate (print_config) PASS · role-ceo = role ใกล้สุดชั่วคราว (ไม่มี MD ใน contract)
- NTF: sds_cancelled + sds_low_score_approved (อนุมัติแล้วมีช่องระดับ น้อย/ควรปรับปรุง → เจ้าของ + role-mgr-sales) · ตัด sds_over_limit_approved (ไม่มีวงเงิน/เกณฑ์ตัวเลข) · brief PASS
- DOCCFG: SDS · {PREFIX}-{YYYY}-{run:4} · yearly · global · ออกเลขตอนบันทึกครั้งแรก · snapshot approved_final · --registry PASS (ไม่ชน ACL/CSG/CSM/OTN/SDA)
- MDOC: SDS · class RPT · function_code F01 ชั่วคราว · WARN G04 (ยังไม่มี taxonomy_def_id) · G09 (doa pending) — ตามคาด
- แบบพิมพ์ Replica R9 ตารางกรอบ + R10 **2 หน้า**: หน้า 1 = หัว + ประจำเดือน + ตาราง 2 ชุด × 6 คอลัมน์ (หัวตารางซ้ำ) · หน้า 2 = สรุปผล + ข้อเสนอแนะ + บล็อกลงชื่อ · ฟอนต์ 9pt
- ต้นฉบับแนวนอน แต่ engine thai-doc ล็อก A4 portrait (base.css `@page size:A4 portrait`) → ออกแบบแนวตั้ง แบ่งคอลัมน์ลูกค้า (บันทึกใน print-spec §7)
- parity_check IDENTICAL 5/5 · render_doc ไม่มี {{}} หลง · ไม่มี key ขาด · build_html 5 สถานะ (print/out/*.html) + FM-SAL-21_template.html
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py ส่วน PDF) บนเครื่อง user → สร้าง HTML ต่อสถานะด้วย render_doc + build_html แทน
- ตรวจเสริมในคอนเทนเนอร์ Claude (playwright chromium · ไม่ใช่ด่านทางการ · ไม่แพ็ก PDF): 5/5 สถานะ = 2 หน้า · _states_sheet.png ดูแล้ว · compare_original = WARN 0.247 (แนวนอน vs แนวตั้ง — เหตุผลใน print-spec §7) · compare_side.png ดูแล้ว โครงตารางตรง
- [NO-BROWSER] ข้าม compare_original.py บนเครื่อง user (ไม่มี approved.pdf) — ต้องรันซ้ำบนเครื่องที่มี browser
- 2026-10-10 17:52 · ขั้น 4 → done · R10 2 หน้า · parity 5/5 · คอนเทนเนอร์ 5/5 = 2 หน้า · DOCCFG PASS · MDOC WARN G04/G09

## ขั้น 5 · HTML (html-generator v9.4 · Q-form)
- feature.html ประกอบจาก canonical `references/form-archetype/_SOURCE_form-request-reference.html` (shell + CSS + BASE-KIT) + script เฉพาะเอกสาร (`.build/app1–5.js` · `.build/build.py` · แนวเดียวกับ J002 ที่ผ่านแล้ว) — เทียบ GOLDEN_SKELETON + U1–U28 ก่อน build
- โดเมน: ประจำเดือน (เพิ่ม · DEC-06) · ดึงแบบประเมิน SDA ที่บันทึกผลแล้วของเดือน (อ่านอย่างเดียว · ≤ 12 ราย · ลูกค้าซ้ำ = บล็อก · หลายใบใช้ใบล่าสุด · SDA ถูกยกเลิกหลังดึง = เตือน+บล็อกส่ง) · ตารางเมทริกซ์หัวข้อ × ลูกค้า (ระดับต่ำไฮไลต์) · สรุปผล (บังคับตอนส่ง · ≤ 1,000) · ข้อเสนอแนะ · DOA 1 ขั้น role-ceo คำตัดสิน "รับทราบและอนุมัติ" · ข้อมูลสมมติทั้งหมด
- PDF tab ฝัง print/form.tpl.html + tpl_render.js · docPrintData(r) ตาม print-spec §2 — parity JS ↔ render_doc.py IDENTICAL 11/11 seed
- audit.sh FAIL 0 · WARN 3 (Rule #21 / #40 .uc-email / Token font-size — มาจาก shell+kit canonical เดียวกับไฟล์อ้างอิง) · self_audit PASS (รอบแรก FAIL hex_off 2 สี → เปลี่ยนเป็น color-mix จาก token) · prune_css ตัด 89 rule แล้ว audit/self_audit ซ้ำผ่าน · node --check ผ่าน · มี meta cube-archetype=Q-form + window.__QA__
- [NO-BROWSER] ข้าม e2e_standard.py · render-check.py บนเครื่อง user · ตรวจเสริมในคอนเทนเนอร์ Claude (Lucide CDN ถูกบล็อก ไอคอนไม่ขึ้น): e2e_standard 21/21 ผ่าน → reports/e2e_container_ref.json (ไม่ใช่ report ทางการ) + flow สร้าง→ดึง 12 ราย→ส่ง→อนุมัติ→PDF ไม่มี pageerror
- U1–U28: U1✓ U2✓ U3✓ U4✓ U5✓ U6✓(10/25/50 + pager) U7✓ U8✓(1290 wizard/920 view) U9✓ U10✓(ไฮไลต์ระดับต่ำ = color-mix จาก --c-warning) U11✓ U12✓ U13✓ U14✓(Q2 wizard 3 ขั้น) U15✓ U16 n/a(ไม่มีลบ · ยกเลิกมีเหตุผล) U17✓ U18✓ U19✓(sub 2 fact) U20✓(ไม่มี page tabs) U21✓(kit WARN token) U22✓ U23✓ U24✓ U25✓ U26–U28 n/a(ไม่มีหน้า config)
- 2026-10-10 18:05 · ขั้น 5 → done · audit FAIL 0 · self_audit PASS · [NO-BROWSER] e2e ข้าม · คอนเทนเนอร์ 21/21
- 2026-10-10 18:05 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-005.md/.docx (brd-generator-full v2.3 Prebrief Mode · Lane · md_to_docx ผ่าน) · AI Review C1–C23 → APPROVED (C16 WARN: รหัส feature ชั่วคราว) · DEC-01..16 อยู่ใน §2.4 แยกรายข้อ
- FRD_F-TMP-005_Pack (frd-generator-v6.2 Input Mode 0 · FULL) 00–07 + INDEX · ฟิลด์ DOA (approval_chain/approver_role/approved_by + TODO: DOA engine) อยู่ใน 02 §2.3 และ 04_DB (เอกสารนี้มีการอนุมัติจริง + มี DOA_BRIEF → K7 ไม่ควร BLOCK)
- frd_lint: รอบแรก WARN N3 (บรรทัด BR-15 ถูกนับเป็นค่าคงที่ hardcode — false positive) → เติม "อ่านจาก config" · รอบสอง BLOCK 0 · WARN 0 · PASS 13 → reports/_SECTION_N.md
- declaration --final: DOCCFG PASS (registry ไม่ชน · frd_ref FN-03/FN-05 · decision_words by_role role-ceo) · NTF PASS (frd_ref FN-05/06/08) · DOA validate (print_config + feature.html) PASS · MDOC WARN (G04 taxonomy · G09 doa pending — ตามคาด) · คัดลง FRD_Pack/declarations/
- 2026-10-10 18:09 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · declaration --final PASS · MDOC WARN G04/G09

## ขั้น 8 · UI Brief → test case AI → UAT
- ก่อนเริ่ม: ปรับ feature.html ให้ "ถัดไป" ขั้น 1 ไม่บังคับสรุปผล (บังคับตอนบันทึกและส่งอนุมัติ — ตรง AC-01/AC-05) → rebuild · audit FAIL 0 · self_audit PASS · คอนเทนเนอร์ e2e 21/21 + เดินตาม test case 49 จุดผ่าน (หลังแก้สคริปต์ตรวจ S02/D03 ให้ตรงขั้นตอน)
- extract_anchors → reports/inventory.json · UI_BRIEF_F-TMP-005.md (§0–§13 · .build/make_brief.py) · brief_check PASS FAIL 0 · WARN 0 → reports/brief_check.md
- testcases-F-TMP-005.md 45 เคส / 132 step · tc_lint ERROR 0 · Coverage AC 14/14 · BR 15/15 · VR 7/7 · EC 11/12 (EC-01 ข้ามพร้อมเหตุผล) · TC-D 6/6 · DEC 16/16 · ค่าคาดหวังตรวจกับ prototype ในคอนเทนเนอร์แล้ว
- [NO-BROWSER] ข้าม verify_anchors.py (anchor เขียนจากข้อความใน feature.html โดยตรง · ตรวจด้วย brief_check + เดินเคสในคอนเทนเนอร์แทน)
- UAT Lite: cases.json 38 เคส · drop ledger 7 (QA_AUDIT_F-TMP-005.md) · lite_audit หายเงียบ 0 · --stamp แล้ว
- [NO-BROWSER] ข้าม capture.py → build testcase-F-TMP-005.html ด้วย shots ว่าง (ไม่มีภาพหน้าจอในเอกสารคน)
- 2026-10-10 18:21 · ขั้น 8 → done · brief_check PASS · tc_lint 45 เคส ERROR 0 · lite_audit หายเงียบ 0 · verify_anchors/capture ข้าม (NO-BROWSER)

## ขั้น 9 · ตรวจรวม + แพ็ก
- manifest_scan 43 artifact · ซ้ำ 0 · unmapped 5 (RUN_STATE · IMPACT json · รายงานย่อย)
- consistency_check รอบ 1: READY · WARN K4 ("ระดับต่ำ n ช่อง" ใน 06 §6.3 ไม่ใช่ข้อความตรงตัว) → แก้ถ้อยคำ · K7 PASS (มี DOA_BRIEF จริง — เอกสารนี้มีการอนุมัติ)
- WARN คงเหลือ: K9 compare 0.247 (ต้นฉบับแนวนอน vs แบบพิมพ์แนวตั้ง — เหตุผลใน print-spec §7) · K9 e2e = report จากคอนเทนเนอร์ (reports/e2e_container_ref.json 21/21) ไม่ใช่เครื่อง user
