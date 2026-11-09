# RUN_LOG — F-TMP-002 FM-ITS-10 แบบฟอร์มตรวจเช็คความเรียบร้อยห้อง Server (REQ-TMP-002)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: to_image.py → LibreOffice → PDF → pypdfium2 (หน้ากระดาษจริงจาก Excel print setup · A4 แนวนอน) · ฟอนต์ไทยในเครื่องไม่มี ภาพจึงเห็นตัวไทยเป็นกล่อง → ถ้อยคำยึด content.html + openpyxl · ตำแหน่ง/เส้นยึดภาพ
- โลโก้อยู่ใน page header (&G) · Doc No./Rev. อยู่ footer ขวา (FM-ITS-10 · Rev.00 : 01/07/2569)
- ตาราง 11 คอลัมน์ · แถวว่าง 30 แถว · ไม่มีช่องลงชื่อท้ายใบ (มีคอลัมน์ ผู้ตรวจสอบ ต่อแถว) · ไม่มีข้อมูลตัวอย่าง/ข้อมูลส่วนบุคคลในไฟล์
- form_spec_check: ERROR 0 · WARN 0 · ไม่มี PREBRIEF CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC
- 2026-10-10 07:53 · ขั้น 1 → done

## ขั้น 2 — เหตุผลรายหมวด (unattended · AI-DEFAULT ทั้งหมด)
- G1: ใบตรวจเช็คเป็นบันทึกประจำวันอย่างเดียว ไม่เปลี่ยนค่า/ไม่ส่งต่อ (ไม่เปิด IT Ticket อัตโนมัติเมื่อพบไม่ปกติ — เสนอเป็นงานต่อยอดใน _BATCH_REPORT)
- G2: กระดาษไม่มีช่องลงชื่อผู้อนุมัติ → ตามนโยบาย (จำนวนขั้น = ช่องผู้อนุมัติบนกระดาษ = 0) → ไม่มีการอนุมัติ · ไม่ทำ DOA (doa_tool: ห้ามยัด DOA เข้า feature ที่ไม่มีอนุมัติ) · ลูกค้าต้องยืนยันว่าต้องมีหัวหน้า IT ตรวจทานรายเดือนไหม
- G3: เกณฑ์ 18-27°C / 40-55 %RH บนหัวตาราง → อ่านจาก config · ไม่มีสูตร · นอกเกณฑ์/ไม่ปกติ/ไม่มีทะเบียน = เตือน ไม่บล็อก
- G4: 30 แถวบนกระดาษ (≈1 เดือน) → ไม่จำกัดแถว · PDF ขั้นต่ำ 30 แถว
- G5: 1:1 ตามกระดาษ 11 คอลัมน์ ไม่เพิ่มช่อง
- G6: ไม่มีช่องลงชื่อท้ายใบ → ชื่อผู้ตรวจสอบเป็นข้อความจากระบบในคอลัมน์ต่อแถว ไม่ใช้ภาพ
- G7: ไม่มีอนุมัติ → สถานะ ร่าง → ส่งแล้ว(ปิดรอบ) · ยกเลิกได้โดยเจ้าของ + admin role · ต้องมีเหตุผล
- G8: เจ้าของ · admin role ของหน่วยงาน IT เห็นทั้งหมด
- G9: ออกเลขเมื่อบันทึกครั้งแรก (เอกสารภายใน ไม่ใช่การเงิน) · รหัส SRC (Server Room Check)
- G10: แนบไฟล์ ✓ (รูปเกจ/จุดผิดปกติ) · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗
- 2026-10-10 07:54 · ขั้น 2 → done

## ขั้น 3 — declaration (ร่าง)
- DOA: ไม่ทำ — DEC-03 ไม่มีการอนุมัติ (doa_tool init ปฏิเสธเอง "ห้ามยัด DOA เข้า feature ที่ไม่มีอนุมัติ")
- NTF: 3 event (src_abnormal_found · src_submitted · src_cancelled) → brief PASS · ไม่มี doa_* events
- DOCCFG: code SRC (Server Room Check) — ไม่ชน registry (ACL) และไม่ชน J001 (ITRS) → brief PASS (--registry)
- MDOC: class REC · function_code F01 ชั่วคราว (ไม่มีตาราง Taxonomy ใน workspace) · source=declaration เพราะ REQ ยังเป็นเลขชั่วคราว → WARN G04 (taxonomy_def_id ว่าง) อธิบายได้

## ขั้น 4 — แบบพิมพ์ Replica
- R9 ตารางกรอบ 11 คอลัมน์ · ต้นฉบับ A4 แนวนอน → engine รองรับแนวตั้งเท่านั้น → ออกแบบ 2 หน้า (R10): 16 แถว/หน้า · หัวตารางซ้ำ · "มีต่อหน้าถัดไป" · "หน้า X/2" · ฟอนต์ 8pt
- data 5 สถานะ: draft · submitted · abnormal · long-31rows · cancelled (ไม่อนุมัติ/DOA 6 ขั้น ไม่ใช้ — ไม่มี DOA)
- parity_check: IDENTICAL 5/5 · ไม่มี {{}} หลง · key ขาด 0 · build_html ทุกสถานะ OK (out/*.html)
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py เรียก render_pdf → สร้าง HTML ต่อสถานะด้วย render_doc + build_html แทน) · ข้าม compare_original.py (ต้องใช้ PDF จาก render_pdf) → ยังไม่มี _states_sheet.png / compare_side.png
- ภาพต้นฉบับ page-1.png มาจาก LibreOffice (หน้ากระดาษจริง) แต่ตัวไทยเป็นกล่องเพราะเครื่องไม่มีฟอนต์ไทย
- 2026-10-10 07:58 · ขั้น 3 → done · no DOA (DEC-03) · NTF PASS · DOCCFG SRC PASS · MDOC WARN G04
- 2026-10-10 07:58 · ขั้น 4 → done · 2 หน้า R10 · parity 5/5 · NO-BROWSER ไม่มี PDF/compare

## ขั้น 5 — HTML Q-form (html-generator v9.4)
- feature.html ประกอบจาก base-kit/shell ของ DevPack ตัวอย่าง F-FIN-ACL (ผ่านทุกด่าน) + page CSS/JS ของ SRC (สคริปต์ `_scratch/build_feature.py`) · แบบพิมพ์ฝัง form.tpl.html + tplRender (= tpl_render.js)
- เปิด GOLDEN_SKELETON.html + ui-standard-list-drawer.md U1–U28 เทียบก่อน build
- audit.sh: FAIL 0 · WARN 3 (มาจาก base-kit กลาง: lucide class ใน comment/kit · .uc-email · font-size px ใน kit) → reports/audit.txt
- prune_css.py: ตัด 2 rule → audit FAIL 0 ซ้ำ
- [NO-BROWSER] ข้าม e2e_standard.py · render-check.py → ทดแทนด้วย smoke test jsdom (ไม่ใช่ browser จริง) 33/33 ผ่าน · JS error 0 → reports/smoke_jsdom.txt (สิทธิ์ G8 · wizard/validation · ส่งปิดรอบ 0 ขั้น · ยกเลิกต้องมีเหตุผล · DOA N ขั้น dynamic · backdrop mousedown · tabs)
- parity แบบพิมพ์ใน prototype: printData จาก JS → render_doc.py IDENTICAL 3/3 (รวมกรณีเพิ่มขั้น DOA แล้วช่องลงชื่องอก)
- U1–U28: U1✓ U2✓ U3✓ U4✓ U5✓ U6✓ U7✓ U8✓ U9✓ U10✓ U11✓(kit) U12✓ U13✓(ไม่มีขั้น → summary+timeline+ผู้ตรวจสอบรายวัน) U14✓(wizard 1290 · ตารางกรอก) U15✓ U16 n/a(ไม่มีลบ ใช้ยกเลิก) U17✓ U18✓ U19✓ U20✓(tabs สถานะ · ไม่มี dropdown สถานะซ้ำ) U21✓(kit) U22✓ U23✓ U24✓ U25✓ U26–U28 n/a(ไม่มีหน้าตั้งค่า)
- 2026-10-10 08:10 · ขั้น 5 → done · audit FAIL 0 · NO-BROWSER: e2e ข้าม → jsdom smoke 33/33
- 2026-10-10 08:10 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 6 — ข้าม (unattended)
- ให้คนดูจาก _BATCH_REPORT · [NO-BROWSER] ยังไม่มี _states_sheet.png / screenshot หน้าจอหลัก (ต้อง render บนเครื่องที่มี browser)

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-002.md/.docx (brd-generator-full v2.3 Prebrief Mode · Lane) — AI Review C01–C23 + PE01–PE05 ผ่าน → APPROVED (C22 ตัวชี้วัด → OQ-01 · PE02 SoD ใช้ detective control เพราะไม่มีขั้นอนุมัติ)
- FRD_F-TMP-002_Pack (frd-generator-v6 Input Mode 0 · STANDARD) 00–07 + INDEX + declarations/
- frd_lint: BLOCK 0 · WARN 0 · PASS 12 → reports/_SECTION_N.md
- doccfg --final --registry: PASS (SRC ไม่ชน) · ntf --final: PASS · mdoc: WARN G04 (taxonomy_def_id ว่าง — OQ-07)
- DOA: ไม่มี DOA_BRIEF (DEC-03 ไม่มีการอนุมัติ) · admin role ฝ่าย IT ไม่อยู่ใน doa-roles-contract → OQ-03 (ไม่ใช้กับ DOA เพราะ 0 ขั้น แต่ใช้กับสิทธิ์มองเห็น/ยกเลิก)
- 2026-10-10 08:15 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 · doccfg/ntf --final PASS

## ขั้น 8 — UI Brief → test case AI → UAT
- extract_anchors → reports/inventory.json · UI_BRIEF_F-TMP-002.md (§0–§13) → brief_check: PASS · FAIL 0 · WARN 0
- testcases-F-TMP-002.md: 53 เคส / 241 step → tc_lint ERROR 0 (reports/tc_counts.json)
- [NO-BROWSER] ข้าม verify_anchors.py · ข้าม capture.py (เอกสารคนไม่มีภาพหน้าจอ)
- cases.json (Lite 39 เคส) + QA_AUDIT (drop ledger 14) → lite_audit: หายเงียบ 0 · ประทับ meta.source · build.py → testcase-F-TMP-002.html (ไม่มีภาพ)
- 2026-10-10 08:23 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 · lite_audit หายเงียบ 0 · NO-BROWSER: verify_anchors/capture ข้าม

## ขั้น 9 — ตรวจรวม + แพ็ก
- consistency_check รอบแรก NOT READY: K2 orig/content.html ถูกนับเป็น prototype ซ้ำ → เปลี่ยนชื่อเป็น orig/content_extract.txt · K7 "มีการอนุมัติแต่ไม่มี DOA_BRIEF" — FRD 04/05 ยังบรรยายเส้นทางผู้ตรวจทานแบบ dynamic (approval_chain · pending · decide) ขัด DEC-03 → แก้รอบที่ 1: ตัดเส้นทางนั้นออกจาก FRD (04 ไม่มี field DOA · 05 BR-13 · 02 ไม่มี API-06 · 03 FN-05 สงวน) + BRD v1.1 + testcases ตัด TC-A01/A02/D06 (50 เคส) + UI brief Drift D-03 (โครง DOA ของ archetype dormant ใน prototype) · ไม่ทำ DOA_BRIEF เพราะ doa_tool ห้ามยัด DOA เข้า feature ที่ไม่มีอนุมัติ
- frd_lint ซ้ำ: BLOCK 0 · tc_lint ERROR 0 · lite_audit หายเงียบ 0 · brief_check FAIL 0
- consistency_check รอบสอง: READY · BLOCK 0 · WARN 1 (K9 ไม่มี e2e report — NO-BROWSER)
- ไฟล์ทำงานของ agent (สคริปต์ประกอบ/สร้างเอกสาร) ย้ายไป .scratch/ (manifest_scan ข้ามโฟลเดอร์ขึ้นต้นจุด · ลบไฟล์ไม่ได้ในโฟลเดอร์นี้)
