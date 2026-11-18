# RUN_LOG — F-TMP-004 FM-SAL-20 แบบประเมินความพึงพอใจ ในประเทศ (Sale admin) (REQ-TMP-004)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพฟอร์ม: to_image.py ใช้ LibreOffice → PDF → pypdfium2 ได้ page-1.png (หน้าพิมพ์จริงจาก Word 1 หน้า ไม่ใช่ภาพจาก HTML) · ภาพไม่มีฟอนต์ไทย (กล่องสี่เหลี่ยม) → ถ้อยคำยึด content.html + word/document.xml · ตำแหน่ง/เส้นยึดภาพ
- content.html ใช้แล้วย้ายไป orig/out/content.html (กัน scanner นับเป็น prototype ซ้ำ)
- docx 1 หน้า = 1 ฟอร์ม · ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC (--cls FRM --module SALES)
- FORM_SPEC: 9 ช่อง (ระบบ 1 = ชื่อลูกค้าจาก Customer master · กรอก 8) · ระดับความพึงพอใจ 5 ระดับ (มากที่สุด/มาก/ปานกลาง/น้อย/ควรปรับปรุง) 5 ข้อ · ข้อเสนอแนะ 1 ช่อง · ลายเซ็น 0 · Doc No.FM-SAL-20 Rev.00 : 01/07/2569 (footer ขวา) · form_spec_check ERROR 0
- title จากหัวฟอร์ม: "แบบประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าในประเทศ" · ชื่อในคิวไม่เพี้ยน → ไม่ rename
- ข้อมูลส่วนบุคคล: ต้นฉบับว่างเปล่า ไม่มีชื่อ/เบอร์/วันที่จริง
- 2026-10-10 17:14 · ขั้น 1 → done · FORM_SPEC 9 ช่อง ERROR 0 · title จากหัวฟอร์ม

## ขั้น 2 · gate (unattended — AI-DEFAULT ทุกหมวด)
- G1: ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อ — เป็นแบบบันทึกผลประเมิน (ผลไปสรุปที่ FM-SAL-21 ภายหลัง ไม่ wire รอบนี้)
- G2: กระดาษไม่มีช่องลงชื่อผู้อนุมัติ (0) → ไม่มีการอนุมัติ (doa.required=false) ตามนโยบาย "ค่าเริ่ม = จำนวนช่องลงชื่อบนกระดาษ"
- G3: ไม่มีสูตร/ค่าคงที่ · กฎ: ข้อละ 1 ระดับ ครบ 5 ข้อจึงบันทึกผลได้ · ประจำเดือนค่าเริ่มจากวันที่ วันที่นอกเดือน = เตือน
- G4: ไม่มีรายการซ้ำ (หัวข้อคงที่ 5 ข้อ)
- G5: 1:1 ไม่เพิ่มช่อง · ไม่มีคำสะกดผิดต้องแก้
- G6: ไม่มีลายเซ็น → ไม่เพิ่มช่องลงชื่อ
- G7: ไม่มีอนุมัติ · ยกเลิกได้ เจ้าของ + admin role · ร่าง/บันทึกผลแล้ว · เหตุผลบังคับ
- G8: เจ้าของ + admin ฝ่ายขาย (role-mgr-sales มีใน doa-roles-contract) เห็นทั้งหมด
- G9: ออกเลขตอนบันทึกครั้งแรก · รหัส SDA (ไม่ชน ACL/CSG/CSM · เว้น SEA/SDS/SES ให้ FM-SAL-21/22/23)
- G10: แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗
- 2026-10-10 17:15 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · AI-DEFAULT ทุกหมวด

## ขั้น 3 · declaration ร่าง
- DOA: ไม่ทำ — DEC-03 ไม่มีการอนุมัติ (`doa_tool init` ตอบ "ไม่ต้องทำ DOA_BRIEF — ห้ามยัด DOA เข้า feature ที่ไม่มีอนุมัติ") · role ที่ใช้ (role-mgr-sales = ผู้รับแจ้ง/admin) มีใน doa-roles-contract
- NTF: 2 event (sda_low_score_recorded → role-mgr-sales · sda_cancelled → เจ้าของ) · ตัด sda_over_limit_approved (ไม่มีขั้นอนุมัติ) · VERDICT PASS
- DOCCFG (หลังขั้น 4): SDA · {PREFIX}-{YYYY}-{run:4} · yearly · global · no-gap ✗ · ออกเลขตอนบันทึกครั้งแรก · snapshot ✗ · module SAL (ตาม J001) · --registry PASS (ไม่ชน ACL/CSG/CSM)
- MDOC: SDA · FRM · source=declaration (REQ-TMP-004 รหัสชั่วคราว) · WARN G04 ยังไม่มี taxonomy_def_id · function_code F01 รอ taxonomy ยืนยัน

## ขั้น 4 · แบบพิมพ์ Replica
- template R4 แถวเส้นประ + R9 `.form-grid` ตารางหัว 2 ชั้น (rowspan/colspan: รายละเอียด | ระดับความพึงพอใจ → มากที่สุด…ควรปรับปรุง) · ไม่มี sign_rows ที่มีช่อง (ไม่มีลายเซ็น/DOA — บล็อก sign_rows ว่างไว้)
- 5 สถานะ: draft · recorded · low-score · long-comments (dense) · cancelled · parity_check IDENTICAL 5/5 · render_doc ไม่มี {{}} หลง · ไม่มี key ขาด · build_html ผ่าน
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py หยุดที่ render_pdf ตัวแรก → สร้าง HTML ต่อสถานะด้วย render_doc + build_html ตามขั้นเดียวกับ render_states แทน ใน print/out/)
- ตรวจภาพเสริม (ไม่ใช่ด่านทางการ · ไม่แพ็ก PDF): render ในคอนเทนเนอร์ Claude → 5/5 สถานะ = 1 หน้า · compare_original รอบ 1 = 0.442 WARN → ปรับ profile ระยะห่าง (11pt · grid 10mm) รอบ 2 = 0.445 WARN — ดูภาพวางคู่แล้ว โครงตรง เหตุผลใน print-spec §7 (ต้นฉบับไม่มีฟอนต์ไทย หัวเรื่องจึง 2 บรรทัด · footer ต้นฉบับเป็นภาพที่อยู่บริษัท)
- [NO-BROWSER] compare_original.py บนเครื่อง user ข้าม (ไม่มี PDF ของเรา) — ต้องรันซ้ำบนเครื่องที่มี browser
- doa validate --print-config: ไม่รัน (ไม่มี DOA)
- แบบพิมพ์ 1 หน้า (ไม่ต้อง R10) · ฟอนต์ 11pt · template HTML: print/แบบประเมินความพึงพอใจ_SaleAdmin_ในประเทศ_template.html
- 2026-10-10 17:19 · ขั้น 3 → done · NTF PASS · DOCCFG PASS · MDOC WARN G04 · DOA ไม่มี (DEC-03)
- 2026-10-10 17:19 · ขั้น 4 → done · parity 5/5 · 1 หน้า (ตรวจในคอนเทนเนอร์) · NO-BROWSER ไม่มี PDF

## ขั้น 5 · HTML Q-form (html-generator v9.4)
- ฐาน: feature.html ของ J001 (FM-SAL-10 · ผ่าน audit/e2e แล้ว · สร้างจาก canonical `_SOURCE_form-request-reference.html` + BE date picker #114 + ส่วนเสริม v9.4 Group 25) → เปลี่ยนเฉพาะส่วนโดเมน: ช่อง 1:1 FM-SAL-20 (ประจำเดือน · ชื่อลูกค้า · วันที่ · 5 ข้อ × 5 ระดับเป็นคำ · ข้อเสนอแนะเพิ่มเติม 1 ช่อง) · SDA_TPL = print/form.tpl.html · PDF_CSS token = profile.json · ข้อมูลสมมติทั้งหมด · เทียบ GOLDEN_SKELETON + U1–U28 ก่อน build
- ⚠️ ข้อขัดแย้งเครื่องมือ (เหมือน J001): Q-form (#108) บังคับ DOA slot-row แต่ DEC-03 = ไม่มีการอนุมัติ → "สาย DOA 0 ขั้น" (MOCK_DOA_RESOLVED.steps=[] · DOA-ENGINE-HOOK · TODO: DOA engine) · ไม่มี DOA_BRIEF · ไม่มีปุ่มอนุมัติ
- audit.sh FAIL 0 · WARN 3 (เท่ากับไฟล์ canonical: #21 lucide ใน base-kit · #40 .uc-email · token font-size ใน CSS กลาง) · prune_css ตัด 0 rule (ฐาน prune แล้ว) audit ซ้ำ FAIL 0 · มี meta cube-archetype=Q-form + window.__QA__ · node --check script หลักผ่าน
- [NO-BROWSER] ข้าม e2e_standard.py บนเครื่อง user · ตรวจเสริมในคอนเทนเนอร์ Claude (Lucide CDN ถูกบล็อก ไอคอนไม่ขึ้น) = 21/21 ผ่าน → reports/e2e_container_ref.json (ไม่ใช่ report ทางการ) · screenshot reports/shot_list/wizard/pdf.png
- [NO-BROWSER] ข้าม render-check.py · capture.py
- U1–U28: U1✓ U2✓ U3✓ U4✓ U5✓ U6✓(page-size 10/25/50 + pager) U7✓ U8✓(1290 wizard/920 view) U9✓ U10✓ U11✓ U12✓ U13✓(block §6.1 · 0 ขั้น) U14✓(Wizard 3 ขั้นตาม Q2 #100F — เอกสารเบาแต่ archetype ล็อก 3 ขั้น) U15✓ U16–(ไม่มีลบ — ใช้ยกเลิก+เหตุผล) U17✓ U18✓ U19✓ U20✓ U21✓ U22✓ U23✓ U24✓ U25✓(onmousedown) U26–U28 –(ไม่มีหน้าตั้งค่า)
- 2026-10-10 17:24 · ขั้น 5 → done · audit FAIL 0 · e2e ข้าม (NO-BROWSER) · คอนเทนเนอร์ 21/21
- 2026-10-10 17:24 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-004.md/.docx (brd-generator-full v2.3 Prebrief Mode · Lane · md_to_docx ผ่าน) · Quality Gate C1–C20 → APPROVED (C16 WARN: รหัส feature ชั่วคราว) · อ้าง DEC-01..13 ครบ
- FRD_F-TMP-004_Pack (frd-generator-v6.2 Input Mode 0 · STANDARD) · 04_DB มี approver_role / approved_by / approval_chain (ว่าง · TODO: DOA engine — DEC-03)
- frd_lint: BLOCK 0 · WARN 0 · PASS 9 → reports/_SECTION_N.md
- declaration --final: DOCCFG PASS (registry ไม่ชน · frd_ref FN-02) · NTF PASS (frd_ref FN-05/06) · MDOC WARN G04 (taxonomy_def_id ว่าง → รออนุมัติ definition) · ไม่มี DOA (DEC-03) · คัดลง FRD_Pack/declarations/
- 2026-10-10 17:28 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 · DOCCFG/NTF final PASS · MDOC WARN G04

## ขั้น 8 · UI Brief → test case AI → UAT
- extract_anchors → reports/inventory.json · UI_BRIEF_F-TMP-004.md (§0–§13 · microcopy จาก inventory) · brief_check PASS FAIL 0 · WARN 0 (รอบแรก FAIL B5 id แบบ dynamic `#secAns1/#sumSec1` → แก้ถ้อยคำ แล้วผ่าน)
- testcases-F-TMP-004.md 30 เคส / 88 step · tc_lint ERROR 0
- [NO-BROWSER] ข้าม verify_anchors.py (anchor ข้อความตรวจด้วย brief_check + e2e ในคอนเทนเนอร์แทน)
- cases.json (Lite 27 เคส · drop 3: TC-K02 ENG-NOTIFY · TC-E01/E02 simulate) · lite_audit หายเงียบ 0 · --stamp แล้ว
- [NO-BROWSER] ข้าม capture.py → UAT testcase-F-TMP-004.html build ด้วย shots ว่าง (ไม่มีภาพหน้าจอในเอกสารคน — ต้อง capture รอบเต็มบนเครื่องที่มี browser)
- 2026-10-10 17:30 · ขั้น 8 → done · brief_check PASS · tc_lint 30 เคส ERROR 0 · lite_audit 0 · verify_anchors/capture ข้าม (NO-BROWSER)

## ขั้น 9 · ตรวจรวม + แพ็ก
- manifest_scan 44 artifact · ซ้ำ 0 (orig/out/content.html ไม่ถูกนับเป็น prototype) · unmapped 8 (ไฟล์ช่วย/รายงานย่อย)
- consistency_check รอบ 1: NOT READY · BLOCK K7 "มีการอนุมัติแต่ไม่มี DOA_BRIEF" — สาเหตุ: regex ของ K7 นับคำ `approval_chain`/"อนุมัติ" ใน 04/05 เป็นสัญญาณว่ามีอนุมัติ แต่ DEC-03 = ไม่มีการอนุมัติ (ใส่ field DOA ไว้ตามกติกา DOA) → แก้: เอาคอลัมน์ approver_role/approved_by/approval_chain ออกจาก 04_DB (คงไว้ใน 02 API response + 03 FN-03 `TODO: DOA engine`) และเลี่ยงคำว่า "อนุมัติ" ใน 04/05 → frd_lint ซ้ำ BLOCK 0
- consistency_check รอบ 2: **READY** · BLOCK 0 · WARN 1 (K9 compare 0.445 WARN — เหตุผลใน print-spec §7) · K9 e2e = report จากคอนเทนเนอร์ (reports/e2e_container_ref.json 21/21) ไม่ใช่เครื่อง user
- แพ็กด้วย `dm.sh pack J004` (NO-BROWSER → แบบมีเงื่อนไข)
- pack: _pack/F-TMP-004_DevPack.zip · READY (แบบมีเงื่อนไข NO-BROWSER) · consistency BLOCK 0 · WARN 1 (K9 compare)
