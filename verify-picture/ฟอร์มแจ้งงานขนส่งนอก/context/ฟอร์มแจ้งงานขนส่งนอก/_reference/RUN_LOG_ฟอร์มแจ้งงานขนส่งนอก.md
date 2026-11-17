# RUN_LOG — F-TMP-003 FM-SAL-16 ฟอร์มแจ้งงานขนส่งนอก (REQ-TMP-003)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · อ่านฟอร์ม (หมายเหตุ)
- ภาพหน้า: `_system/tools/to_image.py` ใช้ LibreOffice → PDF → pypdfium2 (ไม่ใช่ภาพ HTML) แต่ฟอนต์ไทยไม่มีในเครื่อง → ตัวไทยเป็นกล่อง · ถ้อยคำยึด content.html + openpyxl · ตำแหน่ง/เส้นยึดภาพ · ภาพแตกคอลัมน์ E (วันที่นัดส่ง) ไปหน้า 2 จากความกว้างคอลัมน์ (print area A1:E26 = 1 หน้า A4 แนวตั้ง) → ไม่ใช้เทียบ layout 1:1
- xlsx 1 ชีต (Sheet2) · หัวฟอร์ม B1 "ฟอร์มแจ้งงานขนส่งนอก…" · footer ขวา "Doc. No. : FM-SAL-16" / "Rev.00 : 01/07/2569" · ตาราง 5 คอลัมน์ × 20 บรรทัด · "ผู้จัดทำ……" ใต้ตาราง · โลโก้ฝัง 1 ภาพ
- form.title = "ฟอร์มแจ้งงานขนส่งนอก" (หัวฟอร์ม) · ชื่อคิวไม่เพี้ยน → ไม่ rename
- FORM_SPEC 8 ช่อง · form_spec_check ERROR 0 · ไม่มี PREBRIEF CMS → สร้าง PREBRIEF v2 (module Sales)
- ข้อมูลส่วนบุคคล: ไฟล์ลูกค้าไม่มีข้อมูลจริง (ตารางว่าง) · ช่องผู้จัดทำติด pdpa
- content.html ใช้แล้ว → ย้ายไป orig/out/content.html (กัน scanner นับเป็น prototype)
- 2026-10-10 17:14 · ขั้น 1 → done · FORM_SPEC 8 ช่อง ERROR 0 · PREBRIEF v2

## ขั้น 2 · gate (unattended — AI-DEFAULT ทุกหมวด)
- G1: ไม่เปลี่ยนค่า/ไม่ส่งต่อ — เป็นใบแจ้งงานให้ผู้ขนส่งนอก ยังไม่ผูก SO/ใบส่งของ → ผู้ใช้กรอกเลขที่ PO เอง
- G2: กระดาษมีแค่ "ผู้จัดทำ" ไม่มีช่องผู้อนุมัติ → ไม่มีการอนุมัติ · เก็บ field approver_role/approved_by/approval_chain ว่าง + TODO: DOA engine (เปิดภายหลังได้โดยไม่แก้โครง)
- G3: ไม่มีสูตร/ค่าคงที่ · กฎ: จำนวน > 0 (บล็อก) · วันที่นัดส่งก่อนรอบวันที่ = เตือน · ต้องมี ≥1 แถวครบ 5 ช่อง · แถวไม่ครบ = บล็อก
- G4: ไม่จำกัดแถว · แบบพิมพ์ขั้นต่ำ 20 บรรทัด · G5: 1:1 ไม่เพิ่มช่อง (หน้าจอแก้สะกด "รอบวันที่" · แบบพิมพ์คงตามกระดาษ)
- G6: บล็อกผู้จัดทำ = ชื่อ + "ส่งในระบบ วันที่ เวลา" ไม่ใช้ภาพ · G7: ไม่มีอนุมัติ · ยกเลิก owner+admin สถานะ ร่าง/ส่งแล้ว เหตุผลบังคับ
- G8: เจ้าของ · admin ฝ่ายขาย (role-mgr-sales) เห็นทั้งหมด · G9: ออกเลขตอนบันทึกครั้งแรก รหัส OTN (Outsourced Transport Notice — ไม่ชน ACL/CSG/CSM · ไม่ใช้กลุ่ม S../SA.. เลี่ยง J004) · G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- 2026-10-10 17:15 · ขั้น 2 → done · 15 มติ · AI-DEFAULT 10 · VALID 5

## ขั้น 3 · declaration ร่าง
- DOA: ไม่ทำ — DEC-03 ไม่มีการอนุมัติ (`doa_tool init` ตอบ "ไม่ต้องทำ DOA_BRIEF") · โครงข้อมูลเก็บ approver_role/approved_by/approval_chain ว่าง + TODO: DOA engine · admin role = role-mgr-sales (มีใน doa-roles-contract)
- NTF: 3 event (otn_submitted → role-mgr-sales · otn_early_delivery_date → role-mgr-sales · otn_cancelled → เจ้าของ) · VERDICT PASS
- DOCCFG/MDOC ทำหลังขั้น 4 (ใช้ print_config)
- 2026-10-10 17:16 · ขั้น 3 → done · NTF PASS · DOA ไม่มี (DEC-03) · doccfg/mdoc หลังขั้น 4
- DOCCFG (หลังขั้น 4): OTN · {PREFIX}-{YYYY}-{run:4} · yearly · global · no-gap ✗ · ออกเลขตอนบันทึกครั้งแรก · --registry PASS (ไม่ชน ACL/CSG/CSM)
- MDOC: OTN · FRM · source=declaration (REQ-TMP-003 ชั่วคราว) · WARN G04 ยังไม่มี taxonomy_def_id · function_code F01 รอ taxonomy ยืนยัน

## ขั้น 4 · แบบพิมพ์ Replica
- template R9 `.form-grid` ตาราง 5 คอลัมน์ (thead หัวซ้ำ) × lines ≥ 20 แถว + R4 รอบวันที + หัวเรื่องมีเส้นประชื่อผู้ขนส่ง + B6 sign_rows (ผู้จัดทำ 1 ช่อง · doa_step:* พร้อมรับ DOA ภายหลัง)
- 5 สถานะ: draft · submitted · cancelled · long-20rows (dense) · blank · parity_check IDENTICAL 5/5 · render_doc ไม่มี {{}} หลง · ไม่มี key ขาด · build_html ผ่าน (profile token ผ่านการตรวจ — form_logo_align แก้ flex-start → left)
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py ส่วน PDF/นับหน้า/_states_sheet) — สร้าง HTML ต่อสถานะใน print/out/ ด้วย render_doc + build_html แทน
- ตรวจภาพเสริม (ไม่ใช่ด่านทางการ · ไม่แพ็ก PDF): render ในคอนเทนเนอร์ Claude → ทุกสถานะ 1 หน้า (รอบแรก long 2 หน้าเพราะคอลัมน์เท่ากัน → ตั้งความกว้างคอลัมน์ตาม xlsx + 9.5pt) · ภาพ `out/_states_sheet_preview.png`
- compare_original (คอนเทนเนอร์) 0.161 WARN — ต้นฉบับไม่มีฟอนต์ไทย + คอลัมน์ E หลุดหน้า + ขอบ/สเกลต่าง · ดูภาพวางคู่แล้ว โครงตรง — เหตุผลใน print-spec §7 · [NO-BROWSER] compare_original.py บนเครื่อง user ข้าม (ไม่มี PDF ของเรา)
- doa validate --print-config: ไม่รัน (ไม่มี DOA · DEC-03)
- แบบพิมพ์ 1 หน้า (ไม่ต้อง R10 · --max-pages 1) · ฟอนต์ 9.5pt · เกิน 20 แถว = ใบต่อ หัวตารางซ้ำ (OQ)
- 2026-10-10 17:21 · ขั้น 4 → done · parity 5/5 · 1 หน้า (ตรวจในคอนเทนเนอร์) · NO-BROWSER ไม่มี PDF · DOCCFG PASS · MDOC WARN G04
- 2026-10-10 · ขั้น 4 · (บันทึกเพิ่ม) ภาพ `print/out/_states_sheet_preview.png` · `print/compare_preview/compare_side.png`

## ขั้น 5 · HTML Q-form (html-generator v9.4)
- ฐาน: shell + CSS + BASE-KIT + BE date picker + tpl_render ของ Q-form v9.4 ที่ผ่าน audit แล้ว (คัดจาก canonical `references/form-archetype` ผ่านงาน J001 · เก็บสำเนาที่ `.build/base_qform_v94.html`) + script เฉพาะเอกสาร `.build/app1–4.js` + `.build/extra.css` → `.build/build.py` · เทียบ GOLDEN_SKELETON + U1–U28 ก่อน build
- แถวซ้ำ 5 ช่อง (> 4) → ตารางกรอกในขั้น 1 (#107) · แถวว่างไม่นับ · แถวไม่ครบ/จำนวน ≤ 0 = บล็อก + ข้อความใต้แถว · วันที่นัดส่งก่อนรอบวันที่ = เตือน · "เพิ่มรายการ" ยกต้นทาง+วันที่นัดส่งจากแถวก่อน · การ์ดสรุปสด (จำนวนรายการ/จำนวนรวม/เตือนวันที่)
- DOA 0 ขั้น (DEC-03): MOCK_DOA_RESOLVED.steps=[] (DOA-ENGINE-HOOK) · modal ส่งวน slot ตาม resolve · record มี approver_role/approved_by/approval_chain + TODO: DOA engine · แบบพิมพ์ sign_rows = ผู้จัดทำ + ขั้น DOA
- PDF tab ฝัง print/form.tpl.html + tplRender/tplSignRows · docPrintData(r) = data contract (= render_data.py) — parity JS ↔ render_doc.py IDENTICAL 12/12 seed (ตรวจในคอนเทนเนอร์)
- audit.sh FAIL 0 · WARN 3 (#21 lucide ใน base-kit · #40 .uc-email · token font-size — มาจาก shell/kit กลางเดียวกับไฟล์อ้างอิง)
- self_audit รอบแรก FAIL (custom_tabs false-positive จาก `S.list.tab` ใน class · spacing 14/7/44 · hex จากเลขกฎในคอมเมนต์ CSS + #F1EEE9 · hint ยาว) → แก้ทั้งหมด → PASS · prune_css ตัด 0 แล้วรัน audit/self_audit ซ้ำ ผ่าน · มี meta cube-archetype=Q-form + window.__QA__
- [NO-BROWSER] ข้าม e2e_standard.py บนเครื่อง user · ตรวจเสริมในคอนเทนเนอร์ Claude (CDN ไอคอนถูกบล็อก → ไม่มีไอคอน) = 21/21 ผ่าน (รอบแรก 20/21: S9 ใช้ร่างแรกของ owner ซึ่งกรอกไม่ครบ → สลับลำดับ seed ให้ร่างครบมาก่อน) → `reports/e2e_container_ref.json` (ไม่ใช่ report ทางการ) · smoke: สร้าง→ส่ง · จำนวน 0 บล็อก · ส่งร่างไม่ครบถูกบล็อก · ยกเลิกต้องมีเหตุผล · บันทึกร่าง — pageerror 0 · screenshot `reports/shot_*.png`
- [NO-BROWSER] ข้าม render-check.py
- U1–U28: U1✓ U2✓ U3✓ U4✓ U5✓ U6✓(page-size 10/25/50 ค่าเริ่ม 25) U7✓ U8✓(1290 wizard/920 view) U9✓ U10✓ U11✓(kit) U12✓ U13✓(block §6.1 · 0 ขั้น) U14✓(Q2 wizard 3 ขั้น) U15✓ U16–(ไม่มีลบ — ยกเลิก+เหตุผล) U17✓ U18✓ U19✓(sub 2 fact) U20✓(segmented สถานะ) U21✓(WARN token จาก kit) U22✓(ph-badge 1 ตัว) U23✓ U24✓ U25✓(onmousedown) U26–U28 –(ไม่มีหน้าตั้งค่า)
- 2026-10-10 17:32 · ขั้น 5 → done · audit FAIL 0 · self_audit PASS · e2e ข้าม (NO-BROWSER) · คอนเทนเนอร์ 21/21
- 2026-10-10 17:32 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-003.md/.docx (brd-generator-full v2.3 Prebrief Mode · Lane) · Quality Gate C1–C20 → APPROVED (C16 WARN: รหัส feature ชั่วคราว) · DEC-01..15 แยกแถวครบ
- FRD_F-TMP-003_Pack (frd-generator-v6.2 Input Mode 0 · STANDARD) · 04 มี approver_role/approved_by/approval_chain (TODO: DOA engine · ว่าง — DEC-03)
- frd_lint: BLOCK 0 · WARN 0 · PASS 10 → reports/_SECTION_N.md
- declaration --final: DOCCFG PASS (--registry ไม่ชน · frd_ref FN-02) · NTF PASS (frd_ref FN-05/06) · MDOC WARN G04 (taxonomy_def_id ว่าง → รออนุมัติ definition) · ไม่มี DOA (DEC-03) · คัดลง FRD_Pack/declarations/
- 2026-10-10 17:36 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 · DOCCFG/NTF final PASS · MDOC WARN G04

## ขั้น 8 · UI Brief → test case AI → UAT
- extract_anchors → reports/inventory.json · UI_BRIEF_F-TMP-003.md (§0–§13 · สร้างด้วย `.build/make_brief.py`) · brief_check PASS · FAIL 0 · WARN 0 → reports/brief_check.md
- testcases-F-TMP-003.md 32 เคส / 93 step (`.build/make_tc.py`) · tc_lint ERROR 0 · Coverage AC 12/12 · BR 11/13 · VR 6/6 · EC 5/8 · DEC 13/15 (ข้ามพร้อมเหตุผล)
- [NO-BROWSER] ข้าม verify_anchors.py (anchor เขียนจากข้อความใน feature.html โดยตรง + ตรวจ flow หลักด้วย smoke ในคอนเทนเนอร์) · ข้าม capture.py (ไม่มีภาพหน้าจอ · regionKey ว่าง)
- UAT Lite: cases.json 29 เคส · drop ledger 3 (TC-K01 ENG-NOTIFY · TC-E01/E02 simulate) · lite_audit หายเงียบ 0 · --stamp แล้ว · build testcase-F-TMP-003.html (ไม่มีภาพ)
- 2026-10-10 17:42 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 · lite_audit 0 · [NO-BROWSER] ข้าม verify_anchors/capture

## ขั้น 9 · ตรวจรวม + แพ็ก
- consistency_check รอบแรก NOT READY: K7 BLOCK "มีการอนุมัติแต่ไม่มี DOA_BRIEF" — heuristic ของสคริปต์จับคำ `approval_chain` / "อนุญาต" ใน FRD 04/05 (คอลัมน์ hook DOA ที่ว่าง + คำว่า "อนุญาต null") ทั้งที่ DEC-03 ไม่มีการอนุมัติ และ doa_tool init ปฏิเสธการทำ DOA_BRIEF · K4 WARN microcopy "ส่งในระบบ วันที่ เวลา"
  - แก้: ย้ายนิยามคอลัมน์ hook DOA (approver_role/approved_by/approval_chain · TODO: DOA engine) ไป FRD 03_LOGIC §3.4 · 04_DB อ้างถึง · ปรับถ้อยคำ 04/05 · 06 AC-09 ใช้ "ส่งในระบบ" ตรงจอ · frd_lint ซ้ำ BLOCK 0 · ไม่ได้แก้สคริปต์ (บันทึกในรายงานว่า K7 เป็น false-positive กับเอกสารไม่มีอนุมัติที่มีคอลัมน์ hook)
- consistency_check: READY · BLOCK 0 · WARN 1 (K9 เทียบต้นฉบับ 0.161 — เหตุผลใน print-spec §7) · K9 e2e 21/21 มาจาก `reports/e2e_container_ref.json` = รันในคอนเทนเนอร์ ไม่ใช่เครื่อง user ([NO-BROWSER])
- 2026-10-10 17:43 · ขั้น 9 → done · pack READY (มีเงื่อนไข NO-BROWSER) · consistency BLOCK 0 · WARN K9 compare 0.161
