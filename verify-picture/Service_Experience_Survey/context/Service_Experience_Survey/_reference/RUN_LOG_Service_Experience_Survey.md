# RUN_LOG — F-TMP-006 FM-SAL-22 แบบประเมินความพึงพอใจ Sales Admin (ต่างประเทศ) (REQ-TMP-006)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพฟอร์ม: to_image.py ใช้ LibreOffice → PDF → pypdfium2 ได้ page-1.png (หน้าพิมพ์จริงจาก Word 1 หน้า ไม่ใช่ภาพจาก HTML) · ถ้อยคำยึด content.html + word/document.xml · ตำแหน่ง/เส้นยึดภาพ
- content.html ใช้แล้วย้ายไป orig/out/content.html (กัน scanner นับเป็น prototype ซ้ำ)
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC (--cls FRM --module SALES)
- FORM_SPEC: 14 ช่อง (ระบบ 1 = Company Name จาก Customer master · กรอก 13) · คะแนน 1–5 จำนวน 10 ข้อ ใน 3 กลุ่ม (Communication & Responsiveness 3 · Documentation & Execution 5 · Professionalism 2) · Additional Feedback 1 ช่อง · ลายเซ็น 0 · Doc No.FM-SAL-22 Rev.00 : 01/07/2569 (footer ขวา) · form_spec_check ERROR 0 WARN 0
- ฟอร์มเป็นภาษาอังกฤษล้วน หัวฟอร์มไม่มีชื่อไทย → title = "Service Experience Survey" (ตามหัวฟอร์มจริง) · ชื่อในคิวไม่เพี้ยน → ไม่ rename
- ข้อมูลส่วนบุคคล: ต้นฉบับว่างเปล่า · Contact Person = pdpa:true → ตัวอย่างใช้ชื่อสมมติเท่านั้น · "Credence Public Company Limited" = ชื่อบริษัทผู้ออกฟอร์ม (Organization) ไม่ใช่ข้อมูลตัวอย่างลูกค้า
- 2026-10-10 17:46 · ขั้น 1 → done · FORM_SPEC 14 ช่อง ERROR 0 · title จากหัวฟอร์ม (อังกฤษล้วน)

## ขั้น 2 · gate (unattended — AI-DEFAULT ทุกหมวด)
- G1: ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อ — แบบบันทึกผลประเมิน (ผลไปสรุปที่ใบสรุปฯ ต่างประเทศภายหลัง ไม่ wire รอบนี้)
- G2: กระดาษไม่มีช่องลงชื่อผู้อนุมัติ (0) → ไม่มีการอนุมัติ (doa.required=false) ตามนโยบาย "ค่าเริ่ม = จำนวนช่องลงชื่อบนกระดาษ"
- G3: ไม่มีสูตร/ค่าคงที่ · กฎ: ข้อละ 1 คะแนน (1–5) ครบ 10 ข้อจึงบันทึกผลได้ · Month ค่าเริ่ม = เดือนปัจจุบัน · ไม่มีช่องวันที่ → ใช้เวลาระบบ
- G4: ไม่มีรายการซ้ำ (หัวข้อคงที่ 10 ข้อ 3 กลุ่ม)
- G5: 1:1 ไม่เพิ่มช่อง · ป้ายภาษาอังกฤษตามกระดาษ · ไม่มีคำสะกดผิดต้องแก้
- G6: ไม่มีลายเซ็น → ไม่เพิ่มช่องลงชื่อ
- G7: ไม่มีอนุมัติ · ยกเลิกได้ เจ้าของ + admin role · ร่าง/บันทึกผลแล้ว · เหตุผลบังคับ
- G8: เจ้าของ + admin ฝ่ายขาย (role-mgr-sales มีใน doa-roles-contract) เห็นทั้งหมด
- G9: ออกเลขตอนบันทึกครั้งแรก · รหัส SEA (ไม่ชน ACL/CSG/CSM/OTN/SDA · เว้น SDS/SES ให้ FM-SAL-21/23)
- G10: แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗
- 2026-10-10 17:46 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · AI-DEFAULT 10/14

## ขั้น 3 · declaration ร่าง
- DOA: ไม่ทำ — DEC-03 ไม่มีการอนุมัติ (`doa_tool init` ตอบ "ไม่ต้องทำ DOA_BRIEF") · role ที่ใช้ (role-mgr-sales) มีใน doa-roles-contract
- NTF: 2 event (sea_low_score_recorded → role-mgr-sales · sea_cancelled → เจ้าของ) · ตัด DOA events · VERDICT PASS
- DOCCFG (หลังขั้น 4): SEA · {PREFIX}-{YYYY}-{run:4} · yearly · global · no-gap ✗ · ออกเลขตอนบันทึกครั้งแรก · module SAL · --registry PASS (ไม่ชน ACL/CSG/CSM/OTN/SDA)
- MDOC: SEA · FRM · source=declaration · WARN G04 ยังไม่มี taxonomy_def_id · function_code F01 รอ taxonomy ยืนยัน

## ขั้น 4 · แบบพิมพ์ Replica
- template R1/R2/R4 + R9 `.form-grid` 3 ตาราง (หัวกลุ่ม | 1 2 3 4 5) วนจาก `groups[]` · ไม่มี sign_rows (ไม่มีลายเซ็น/DOA) · footer ภาษาอังกฤษตามภาษาฟอร์ม
- 5 สถานะ: draft · recorded · low-score · long-comments (dense) · cancelled · parity_check IDENTICAL 5/5 · ไม่มี {{}} หลง · ไม่มี key ขาด · build_html ผ่าน
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py เรียก render_pdf → สร้าง HTML ต่อสถานะด้วย render_doc + build_html แทน ใน print/out/)
- ตรวจภาพเสริม (ไม่ใช่ด่านทางการ · ไม่แพ็ก PDF): render ในคอนเทนเนอร์ Claude → 5/5 สถานะ = 1 หน้า · compare รอบ 1 = 0.378 WARN · รอบ 2 (เพิ่มระยะ) = 0.305 + ล้น 2 หน้า → กลับค่ารอบ 1 · เหตุผลใน print-spec §7
- [NO-BROWSER] compare_original.py บนเครื่อง user ข้าม (ไม่มี PDF) — ต้องรันซ้ำบนเครื่องที่มี browser
- doa validate --print-config: ไม่รัน (ไม่มี DOA)
- แบบพิมพ์ 1 หน้า (ไม่ต้อง R10) · ฟอนต์ 10.5pt · template HTML: print/Service_Experience_Survey_template.html
- 2026-10-10 17:51 · ขั้น 3 → done · NTF PASS · DOCCFG PASS · MDOC WARN G04 · DOA ไม่มี (DEC-03)
- 2026-10-10 17:51 · ขั้น 4 → done · parity 5/5 · 1 หน้า (ตรวจในคอนเทนเนอร์) · NO-BROWSER ไม่มี PDF

## ขั้น 5 · HTML Q-form (html-generator v9.4)
- ฐาน: feature.html ของ J004 (FM-SAL-20 · ผ่าน audit/e2e แล้ว · มาจาก canonical Q-form + Group 25) → เปลี่ยนเฉพาะส่วนโดเมนด้วยสคริปต์ (orig/out/_scratch/transform.py): ช่อง 1:1 FM-SAL-22 (Month · Company Name · Contact Person · 3 กลุ่ม 10 ข้อ × คะแนน 1–5 · Additional Feedback) · ไม่มีช่องวันที่ (วันที่บันทึก = ระบบ) · SEA_TPL = print/form.tpl.html · PDF_CSS token = profile.json · ข้อมูลสมมติทั้งหมด (ลูกค้า/ผู้ติดต่อสมมติ) · เทียบ GOLDEN_SKELETON + U1–U28 ก่อน build (โครงเดียวกับ J004)
- ⚠️ ข้อขัดแย้งเครื่องมือ (เหมือน J001/J004): Q-form (#108) บังคับ DOA slot-row แต่ DEC-03 = ไม่มีการอนุมัติ → "สาย DOA 0 ขั้น" (MOCK_DOA_RESOLVED.steps=[] · DOA-ENGINE-HOOK · TODO: DOA engine) · ไม่มี DOA_BRIEF
- audit.sh FAIL 0 · WARN 3 (เท่ากับฐาน canonical: #21 lucide · #40 .uc-email · token font-size) · prune_css ตัด 1 rule → audit ซ้ำ FAIL 0 · meta cube-archetype=Q-form + window.__QA__ · node --check ผ่าน
- [NO-BROWSER] ข้าม e2e_standard.py บนเครื่อง user · ตรวจเสริมในคอนเทนเนอร์ Claude = 21/21 ผ่าน → reports/e2e_container_ref.json (ไม่ใช่ report ทางการ) · smoke สร้าง→บันทึกผล SEA-2569-0015 ผ่าน · ไม่มี pageerror · screenshot reports/shot_list/wizard/pdf.png (Lucide CDN ถูกบล็อกในคอนเทนเนอร์ ไอคอนไม่ขึ้น)
- [NO-BROWSER] ข้าม render-check.py · capture.py
- U1–U28: U1✓ U2✓ U3✓ U4✓ U5✓ U6✓ U7✓ U8✓ U9✓ U10✓ U11✓ U12✓ U13✓(0 ขั้น) U14✓(Wizard 3 ขั้น) U15✓ U16–(ไม่มีลบ — ยกเลิก+เหตุผล) U17✓ U18✓ U19✓ U20✓ U21✓ U22✓ U23✓ U24✓ U25✓(onmousedown) U26–U28 –(ไม่มีหน้าตั้งค่า)
- แบบพิมพ์: เลขตัวอย่างเปลี่ยนเป็น SEA-2569-xxxx ให้ตรง prototype → parity IDENTICAL 5/5 ซ้ำ · render คอนเทนเนอร์ 5/5 = 1 หน้า · compare 0.378 WARN
- 2026-10-10 17:56 · ขั้น 5 → done · audit FAIL 0 · e2e ข้าม (NO-BROWSER) · คอนเทนเนอร์ 21/21
- 2026-10-10 17:56 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-006.md/.docx (brd-generator-full v2.3 Prebrief Mode · Lane · md_to_docx ผ่าน) · Quality Gate C1–C20 → APPROVED (C16 WARN: รหัส feature ชั่วคราว) · อ้าง DEC-01..14 ครบ · โครงจาก J004 แต่เนื้อหา/ช่อง/ถ้อยคำเขียนใหม่ตาม FM-SAL-22
- FRD_F-TMP-006_Pack (frd-generator-v6.2 Input Mode 0 · STANDARD) · field DOA (approver_role / approved_by / approval_chain + TODO: DOA engine) วางใน 02_API §2.2 + 03 FN-03 — ไม่ใส่ใน 04/05 (กัน K7 นับเป็นมีอนุมัติ ตามบทเรียน J004)
- frd_lint รอบ 1: BLOCK 0 · WARN 1 (N2 หาคีย์ q2/q5/q6/q7 ไม่เจอ) → เพิ่ม 01 §1.4 Field Map → รอบ 2 BLOCK 0 · WARN 0 · PASS 9
- declaration --final: DOCCFG PASS (registry ไม่ชน · frd_ref FN-02) · NTF PASS (frd_ref FN-05/06) · MDOC WARN G04 (taxonomy_def_id ว่าง) · ไม่มี DOA (DEC-03) · คัดลง FRD_Pack/declarations/
- 2026-10-10 18:00 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · DOCCFG/NTF final PASS · MDOC WARN G04

## ขั้น 8 · UI Brief → test case AI → UAT
- extract_anchors → reports/inventory.json · UI_BRIEF_F-TMP-006.md (§0–§13 · โครงจาก J004 + §4/§5/§7 เขียนใหม่ตามฟอร์มนี้ · §9 microcopy สร้างใหม่จาก inventory + ถ้อยคำอังกฤษตามกระดาษ) · brief_check รอบ 1 FAIL B5 (`#sumSec1/#sumSec3` id dynamic) → แก้ถ้อยคำ → รอบ 2 PASS FAIL 0 · WARN 0
- testcases-F-TMP-006.md 30 เคส / 89 step (ปรับ TC-C01..C04 · V01/V02 ใหม่ตามช่อง Month/Company/Contact · K01 · D01/D02 แบบพิมพ์อังกฤษ) · tc_lint ERROR 0
- [NO-BROWSER] ข้าม verify_anchors.py (anchor ข้อความตรวจด้วย brief_check + smoke ในคอนเทนเนอร์แทน)
- cases.json (Lite 27 เคส · drop 3: TC-K02 ENG-NOTIFY · TC-E01/E02 simulate) · lite_audit หายเงียบ 0 · --stamp แล้ว
- [NO-BROWSER] ข้าม capture.py → UAT testcase-F-TMP-006.html build ด้วย shots ว่าง (ต้อง capture รอบเต็มบนเครื่องที่มี browser)
- 2026-10-10 18:03 · ขั้น 8 → done · brief_check PASS · tc_lint 30 เคส ERROR 0 · lite_audit 0 · verify_anchors/capture ข้าม (NO-BROWSER)
