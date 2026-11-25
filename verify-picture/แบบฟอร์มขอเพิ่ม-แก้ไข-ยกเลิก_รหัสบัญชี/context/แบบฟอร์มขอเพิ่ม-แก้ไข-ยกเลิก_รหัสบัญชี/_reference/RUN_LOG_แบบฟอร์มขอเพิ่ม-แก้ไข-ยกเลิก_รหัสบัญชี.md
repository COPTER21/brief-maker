# RUN_LOG — F-TMP-003 FM-ACC-01 แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี (REQ-TMP-003)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพหน้าจาก to_image.py (LibreOffice → PDF) — เครื่องไม่มีฟอนต์ไทย ตัวอักษรเป็นกล่อง และล้นเป็น 2 หน้า · ถ้อยคำยึด content.html · ตำแหน่ง/กรอบยึดภาพ · ห้ามใช้ภาพนี้เทียบ layout แบบพิมพ์ 1:1 (ต้นฉบับ Word = 1 หน้า A4)
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC · form_spec_check ERROR 0 · 13 ช่อง · ลายเซ็น 4 · ข้อมูลขัดกัน 3
- ฟอร์มว่าง ไม่มีข้อมูลส่วนบุคคล
- 2026-10-11 00:28 · ขั้น 1 → done · FORM_SPEC 13 ช่อง ERROR 0 · PREBRIEF v2

## ขั้น 2 · gate (unattended — AI-DEFAULT 11 มติ + VALID 3)
- G1 ไม่เปลี่ยนค่า/ไม่ส่งต่อ: COA ใน FEATURE_REGISTRY ยังเป็น (—) → ระบบไม่แก้ผังบัญชีเอง · ช่อง "ผู้บันทึกเข้าระบบ" = ขั้นหลังอนุมัติ เจ้าหน้าที่บัญชี (admin role) กด "บันทึกเข้าระบบแล้ว" ลงชื่อ+วันที่ (ไม่ใช่ขั้น DOA)
- G2 dynamic 2 ขั้นตามกระดาษ: ผู้ตรวจสอบ = role-line-manager · ผู้อนุมัติ = role-mgr-acc · ไม่มีวงเงิน
- G3 ไม่มีสูตร · กฎ 1 ใบ 1 ประเภท · G4 ไม่จำกัดแถว (PDF ≥4) · G5 1:1 + แก้คำ "วัตถุประสงค์ในการยกเลิก" · G6 แถวล่างต่อขั้น · G7 ไม่อนุมัติกลับร่าง · G8 มาตรฐาน · G9 ออกเลขตอนบันทึกครั้งแรก รหัส ACR (ย่อ Account Code Request · ไม่ชน ACL/RPR/ALN) · G10 แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- 2026-10-11 00:29 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · 14 มติ (AI-DEFAULT 11)

## ขั้น 3 · declaration ร่าง
- DOA: ACR.doa.yaml dynamic 2 ขั้น (role-line-manager → role-mgr-acc) · init เขียน on_reject: draft แต่ validate ต้องการ back_to_draft → แก้ yaml (ไม่แก้สคริปต์) · PASS · INFO role-line-manager เป็น relative role ยังไม่อยู่ใน master
- NTF: ตัด over_limit (ไม่มีวงเงิน) · เพิ่ม acr_ready_to_record (→ approved แจ้ง admin role ฝ่ายบัญชี) · acr_recorded · PASS
- DOCCFG: ACR (ไม่ชน ACL/RPR/ALN ใน registry) · PASS · MDOC: source=declaration ชั่วคราว (REQ-TMP-003 ไม่ตรงรูปแบบ REQ-YYYY-NNNN) · function_code F01 + taxonomy_def_id ว่าง → WARN รออนุมัติ G04

## ขั้น 4 · แบบพิมพ์ Replica
- parity IDENTICAL 6/6 · [NO-BROWSER] render_states.py / compare_original.py รันแทนบน Chromium ใน container แล้วคัดผลกลับ (print/out · print/compare)
- 6 สถานะ 1 หน้าทุกไฟล์ (--max-pages 1) · กรณีสุดขั้ว 12 แถว + DOA 6 ขั้น = 2 หน้า (บล็อกลงชื่อขึ้นหน้า 2 ทั้งก้อน) — เก็บ data ไว้ .build ไม่อยู่ในชุดบังคับ
- compare 0.132 WARN — อธิบายได้: ภาพต้นฉบับไม่มีฟอนต์ไทย/ล้น 2 หน้า + ย้ายลายเซ็นเป็นแถวล่าง (ดู print-spec §7) · ดูภาพวางคู่แล้ว
- doa validate --print-config PASS
- 2026-10-11 00:34 · ขั้น 3 → done · doa/ntf/doccfg PASS · mdoc WARN(G04)
- 2026-10-11 00:34 · ขั้น 4 → done · 6 สถานะ 1 หน้า · parity 6/6 · compare WARN อธิบายได้

## ขั้น 5 · HTML Q-form
- feature.html จาก reference form-archetype + golden skeleton v9.4 (โครงจาก J002 .build ปรับ domain) · ฝัง print/form.tpl.html + tpl_render + PDF_CSS · DOA mock 2 ขั้น (role-line-manager → role-mgr-acc) + DECISION_WORDS.by_role · ขั้นหลังอนุมัติ "บันทึกเข้าระบบแล้ว" (admin ฝ่ายบัญชี)
- audit.sh FAIL 0 · WARN 3 (มาจาก kit กลาง: lucide comment · .uc-email · font-size px ใน shell) · self_audit PASS (แก้ naked_hint 1 · missing_id 1) · prune_css ตัด 58 rule แล้วรันซ้ำผ่าน
- [NO-BROWSER] e2e_standard.py รันแทนบน Chromium ใน container → 21/21 ผ่าน (reports/e2e_report.json) · flow เพิ่ม 15/15 (สร้าง→ส่ง→ตรวจสอบ→อนุมัติ→บันทึกเข้าระบบ · ไม่อนุมัติ→กลับร่าง · ชื่อซ้ำ/ช่องว่าง = บล็อก) reports/flow_check_report.json · render-check.py รันใน container (reports/screens/) — ไอคอน lucide ไม่ขึ้นใน container เพราะไม่มี network
- U1 ✓ ไม่มี stat card · U2 ✓ · U3 ✓ · U4 ✓ · U5 ✓ kebab ⋮ · U6 ✓ pager+page size · U7 ✓ CSV ที่ ph · U8 ✓ · U9 ✓ เหตุผลบังคับ · U10 ✓ · U11 ✓ kit · U12 ✓ · U13 ✓ · U14 ✓ wizard 3 ขั้น · U15 ✓ แก้ไขปิด view ก่อน · U16 n/a (ไม่มีลบ ใช้ยกเลิก) · U17 ✓ คน=icon วงกลม · U18 ✓ ellipsis · U19 ✓ header sub 1 fact (ประเภทคำขอ) · U20 ✓ · U21 ✓ · U22 ✓ · U23 ✓ · U24 ✓ search combobox · U25 ✓ backdrop onmousedown · U26–U28 n/a
- 2026-10-11 00:44 · ขั้น 5 → done · audit FAIL 0 · self_audit PASS · e2e 21/21 (Chromium ใน container)
- 2026-10-11 00:44 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-003 (.md+.docx) APPROVED (Prebrief Mode · Lane) · FRD pack 00–07+INDEX · frd_lint BLOCK 0 WARN 0 PASS 13 · doccfg --final PASS (--registry · ACR ไม่ชน) · ntf --final PASS · doa validate --html PASS · mdoc WARN (taxonomy รออนุมัติ G04 · doa pending · source=declaration เพราะ REQ ชั่วคราว)
- 2026-10-11 00:49 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 · declaration --final PASS

## ขั้น 8 · UI Brief → test case → UAT
- UI_BRIEF_F-TMP-003 · brief_check PASS (FAIL 0 WARN 0) · testcases-F-TMP-003.md 62 เคส/133 step · tc_lint ERROR 0 · cases.json Lite 48 เคส · drop ledger 14 · lite_audit หายเงียบ 0 (stamp)
- [NO-BROWSER] verify_anchors.py รันแทนบน Chromium ใน container → MISSING 0 (หัวข้อ modal ที่ประกอบตอนรัน 4 จุดเปลี่ยนเป็นข้อความไม่ตัวหนา + หมายเหตุ) · reports/anchors.json
- [NO-BROWSER] capture.py รันแทนใน container → OK 11 · SKIP/FAIL 0 · build testcase-F-TMP-003.html (48 เคส · 11 ภาพ)
- 2026-10-11 00:59 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 (62 เคส) · anchors MISSING 0 · lite_audit หายเงียบ 0

## ขั้น 9 · แพ็ก
- ย้าย orig/content.html → orig/content.extract.htm (กันชนชื่อ prototype) · reports/e2e_flow_report.json → reports/flow_check_report.json (กัน K2 ซ้ำกับ e2e_report) · data-contract รวมเข้า print-spec §A
- manifest_scan (ซ้ำ 0 · unmapped 10 = RUN_STATE/รายงานประกอบ/inventory อธิบายได้) · consistency READY (BLOCK 0 · WARN 1 K9 compare 0.132 = ภาพต้นฉบับไม่มีฟอนต์ไทย) · dm.sh pack → _pack/F-TMP-003_DevPack.zip 73 ไฟล์ · ไม่ได้รัน finish (ตัวคุมทำ)
- [NO-BROWSER] สคริปต์ browser ทั้งหมด (render_states · compare_original · e2e_standard · render-check · verify_anchors · capture) รันแทนบน Chromium ใน container — ผลจริง ไม่ได้ข้าม
- 2026-10-11 00:59 · ขั้น 9 → done · READY · BLOCK 0 · zip 73 ไฟล์
