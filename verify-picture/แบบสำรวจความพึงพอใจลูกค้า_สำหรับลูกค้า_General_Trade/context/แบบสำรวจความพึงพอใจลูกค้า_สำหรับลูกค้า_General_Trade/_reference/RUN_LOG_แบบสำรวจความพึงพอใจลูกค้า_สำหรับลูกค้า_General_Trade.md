# RUN_LOG — F-TMP-001 FM-SAL-10 แบบสำรวจความพึงพอใจลูกค้า สำหรับลูกค้า General Trade (REQ-TMP-001)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพฟอร์ม: to_image.py ใช้ LibreOffice → PDF → pypdfium2 ได้ page-1/2.png (หน้าพิมพ์จริงจาก Excel) · ภาพไม่มีฟอนต์ไทย (กล่องสี่เหลี่ยม) → ถ้อยคำยึด content.html/openpyxl · ตำแหน่ง/เส้นยึดภาพ · page-2 = คอลัมน์คะแนน "1" ที่หลุดหน้า (ไม่ใช่เนื้อหาใหม่)
- xlsx 1 ชีต (FM-SAL-10) = 1 ฟอร์ม · ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC
- FORM_SPEC: 23 ช่อง (ระบบ 1 = ชื่อบริษัทจาก Customer master · กรอก 22) · ตัวเลือกคะแนน 5–1 จำนวน 16 ข้อ (3 ด้าน: 4+4+8) · ข้อเสนอแนะ 2 ช่อง · ลายเซ็น 0 · Doc.No.FM-SAL-10 Rev.00: 01/07/2569 (footer) · form_spec_check ERROR 0
- ข้อมูลส่วนบุคคล: ตัวอย่างไม่มีชื่อ/เบอร์จริง (มีแค่วันที่ 31/3/69) · เบอร์โทร.ติดต่อ ติด pdpa
- แก้สกิลใน workspace: impact_summary.py regex รับรหัสคำขอชั่วคราว `REQ-TMP-001` (เดิมรับแค่ตัวเลข) — ไม่กระทบด่าน
- 2026-10-10 13:19 · ขั้น 1 → done · FORM_SPEC 23 ช่อง ERROR 0 · title จากหัวฟอร์ม

## ขั้น 2 · gate (unattended — AI-DEFAULT ทุกหมวด)
- G1: ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อ — เป็นแบบบันทึกผลสำรวจ (ผลไปสรุปที่ FM-SAL-11 ภายหลัง ไม่ wire รอบนี้)
- G2: กระดาษไม่มีช่องลงชื่อผู้อนุมัติ (0) → ไม่มีการอนุมัติ (doa.required=false) ตามนโยบาย "ค่าเริ่ม = จำนวนช่องลงชื่อบนกระดาษ"
- G3: ไม่มีสูตร/ค่าคงที่ · กฎ: คะแนนข้อละ 1 ค่า ครบ 16 ข้อจึงบันทึกผลได้ · ประจำเดือนค่าเริ่มจากวันที่ วันที่นอกเดือน = เตือน
- G4: ไม่มีรายการซ้ำ (หัวข้อคงที่ 16 ข้อ)
- G5: 1:1 ไม่เพิ่มช่อง · แก้ "ไว้่" → "ไว้"
- G6: ไม่มีลายเซ็น → ไม่เพิ่มช่องลงชื่อ
- G7: ไม่มีอนุมัติ · ยกเลิกได้ เจ้าของ + admin role · ร่าง/บันทึกผลแล้ว · เหตุผลบังคับ
- G8: เจ้าของ + admin ฝ่ายขาย (role-mgr-sales) เห็นทั้งหมด
- G9: ออกเลขตอนบันทึกครั้งแรก · รหัส CSG (ย่อจากชื่อเอกสาร · เลี่ยงชนกับ J002 FM-SAL-11)
- G10: แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗
- 2026-10-10 13:20 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · AI-DEFAULT ทุกหมวด

## ขั้น 3 · declaration ร่าง
- DOA: ไม่ทำ — DEC-03 ไม่มีการอนุมัติ (`doa_tool init` ตอบ "ไม่ต้องทำ DOA_BRIEF — ห้ามยัด DOA เข้า feature ที่ไม่มีอนุมัติ") · ไม่มี role ต้องเทียบ doa-roles-contract (ใช้ role-mgr-sales เป็นผู้รับแจ้ง/owner เท่านั้น)
- NTF: 2 event (csg_low_score_recorded → role-mgr-sales · csg_cancelled → เจ้าของ) · VERDICT PASS
- DOCCFG (หลังขั้น 4): CSG · {PREFIX}-{YYYY}-{run:4} · yearly · global · no-gap ✗ · ออกเลขตอนบันทึกครั้งแรก · snapshot ✗ · --registry PASS
- MDOC: CSG · FRM · source=declaration (REQ-TMP-001 เป็นรหัสชั่วคราว ไม่ผ่านรูปแบบ REQ-YYYY-NNNN → G10 BLOCK ถ้าใช้ source=request) · WARN G04 ยังไม่มี taxonomy_def_id · function_code F01 รอ taxonomy ยืนยัน

## ขั้น 4 · แบบพิมพ์ Replica
- template R4 แถวเส้นประ + R9 `.form-grid` 3 ตารางคะแนน (thead 5 4 3 2 1) · ไม่มี sign_rows (ไม่มีลายเซ็น/DOA)
- 5 สถานะ: draft · recorded · low-score · long-comments (dense) · cancelled · parity_check IDENTICAL 5/5 · render_doc ไม่มี {{}} หลง · ไม่มี key ขาด · build_html ผ่าน (profile token ผ่านการตรวจ)
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py เรียก render_pdf → ไม่ได้ PDF/_states_sheet.png บนเครื่อง user) — สร้าง HTML ต่อสถานะใน print/out/ แทน
- ตรวจภาพเสริม (ไม่ใช่ด่านทางการ · ไม่แพ็ก PDF): render ในคอนเทนเนอร์ Claude → draft/recorded/long-comments = 1 หน้าทุกไฟล์ · compare_original 0.595 WARN (ต้นฉบับไม่มีฟอนต์ไทย · คอลัมน์ 1 หลุดหน้า) ดูภาพวางคู่แล้ว โครงตรง — เหตุผลใน print-spec §7
- [NO-BROWSER] compare_original.py บนเครื่อง user ข้าม (ไม่มี PDF ของเรา) — ต้องรันซ้ำบนเครื่องที่มี browser
- doa validate --print-config: ไม่รัน (ไม่มี DOA)
- แบบพิมพ์ 1 หน้า (ไม่ต้อง R10) · ฟอนต์ 9pt
- 2026-10-10 13:24 · ขั้น 3 → done · NTF PASS · DOCCFG PASS · MDOC WARN G04 · DOA ไม่มี (DEC-03)
- 2026-10-10 13:24 · ขั้น 4 → done · parity 5/5 · 1 หน้า (ตรวจในคอนเทนเนอร์) · NO-BROWSER ไม่มี PDF

## ขั้น 5 · HTML Q-form (html-generator v9.4)
- ฐาน: canonical `references/form-archetype/_SOURCE_form-request-reference.html` (shell + CSS + base-kit) + BE date picker (#114) + ส่วนเสริม v9.4 Group 25 · เทียบ GOLDEN_SKELETON + U1–U28 ก่อน build
- ⚠️ ข้อขัดแย้งเครื่องมือ: Q-form (#108) บังคับ DOA mock/slot-row/{{#signs}} แต่ DEC-03 = ไม่มีการอนุมัติ → ทำแบบ "สาย DOA 0 ขั้น": MOCK_DOA_RESOLVED.steps=[] (DOA-ENGINE-HOOK) · modal บันทึกผลวนแถวผู้พิจารณาตาม resolve (=0) · แบบพิมพ์มี sign_rows วนตามสาย (=0 ช่อง ไม่แสดงอะไร) · ไม่มี DOA_BRIEF · ไม่มีปุ่มอนุมัติ — ให้คนยืนยันใน _BATCH_REPORT
- แบบพิมพ์เพิ่มบล็อก sign_rows (ว่าง) → parity_check ซ้ำ IDENTICAL 5/5
- audit.sh FAIL 0 · WARN 3 (เท่ากับไฟล์ canonical: #21 lucide ใน base-kit · #40 .uc-email ใน CSS กลาง · token font-size ใน CSS กลาง) · prune_css ตัด 73 rule แล้ว audit ซ้ำ FAIL 0 · มี meta cube-archetype=Q-form + window.__QA__
- [NO-BROWSER] ข้าม e2e_standard.py บนเครื่อง user · ตรวจเสริมในคอนเทนเนอร์ Claude (icon library stub เพราะ CDN ถูกบล็อก) = 21/21 ผ่าน ทั้งก่อน/หลัง prune → reports/e2e_container_ref.json (ไม่ใช่ report ทางการ) · screenshot reports/shot_*.png
- [NO-BROWSER] ข้าม render-check.py · capture.py
- U1–U28: U1✓ U2✓ U3✓ U4✓ U5✓ U6✓(page-size 10/25/50 + pager) U7✓ U8✓(1290 wizard/920 view) U9✓ U10✓ U11✓ U12✓ U13✓(block §6.1 · 0 ขั้น) U14✓(Wizard 3 ขั้นตาม Q2) U15✓(edit = wizard เดิม · ปิด view ก่อน) U16–(ไม่มีลบ — ใช้ยกเลิก+เหตุผล) U17✓ U18✓ U19✓(sub 2 fact) U20✓(segmented สถานะ ไม่ซ้ำ filter) U21✓ U22✓ U23✓ U24✓ U25✓(onmousedown) U26–U28 –(ไม่มีหน้าตั้งค่า)
- 2026-10-10 13:41 · ขั้น 5 → done · audit FAIL 0 · e2e ข้าม (NO-BROWSER) · คอนเทนเนอร์ 21/21
- 2026-10-10 13:41 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-001.md/.docx (brd-generator-full v2.3 Prebrief Mode · Lane) · Quality Gate C1–C20 → APPROVED (C16 WARN: รหัส feature ชั่วคราว) · อ้าง DEC-01..13 ครบ
- FRD_F-TMP-001_Pack (frd-generator-v6.2 Input Mode 0 · STANDARD) · 04/05 ไม่มีคำ/คอลัมน์สายพิจารณา (DEC-03)
- frd_lint: BLOCK 0 · WARN 0 · PASS 9 → reports/_SECTION_N.md
- declaration --final: DOCCFG PASS (registry ไม่ชน · frd_ref FN-02) · NTF PASS (frd_ref FN-05/06) · MDOC WARN G04 (taxonomy_def_id ว่าง → รออนุมัติ definition) · ไม่มี DOA (DEC-03) · คัดลง FRD_Pack/declarations/
- 2026-10-10 13:46 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 · DOCCFG/NTF final PASS · MDOC WARN G04

## ขั้น 8 · UI Brief → test case AI → UAT
- extract_anchors → reports/inventory.json · UI_BRIEF_F-TMP-001.md (14 section) · brief_check PASS FAIL 0 · WARN 0
- testcases-F-TMP-001.md 30 เคส / 88 step · tc_lint ERROR 0
- [NO-BROWSER] ข้าม verify_anchors.py (anchor ข้อความตรวจด้วย brief_check + e2e ในคอนเทนเนอร์แทน)
- cases.json (Lite 27 เคส · drop 3: TC-K02 ENG-NOTIFY · TC-E01/E02 simulate) · lite_audit หายเงียบ 0 · --stamp แล้ว
- [NO-BROWSER] ข้าม capture.py → UAT testcase-F-TMP-001.html build ด้วย shots ว่าง (ไม่มีภาพหน้าจอในเอกสารคน — ต้อง capture รอบเต็มบนเครื่องที่มี browser)
- 2026-10-10 13:50 · ขั้น 8 → done · brief_check PASS · tc_lint 30 เคส ERROR 0 · lite_audit 0 · verify_anchors/capture ข้าม (NO-BROWSER)

## ขั้น 9 · ตรวจรวม + แพ็ก
- manifest_scan 45 artifact · ซ้ำ 0 (orig/content.html → content_extract.html.txt กันนับเป็น prototype ซ้ำ) · unmapped 9 (ไฟล์ช่วย/รายงานย่อย)
- consistency_check: **READY** · BLOCK 0 · WARN 1 (K9 compare 0.595 WARN — เหตุผลใน print-spec §7) · K9 e2e = report จากคอนเทนเนอร์ (reports/e2e_container_ref.json 21/21) ไม่ใช่เครื่อง user
- แพ็กด้วย `dm.sh pack J001` (NO-BROWSER → แบบมีเงื่อนไข)
- pack: _pack/F-TMP-001_DevPack.zip · 60 ไฟล์ · READY (แบบมีเงื่อนไข NO-BROWSER)
- 2026-10-10 13:51 · ขั้น 9 → done · consistency READY · BLOCK 0 · F-TMP-001_DevPack.zip (NO-BROWSER มีเงื่อนไข)
