# RUN_LOG — F-TMP-003 แบบฟอร์มขออนุญาตเข้าพื้นที่สำนักงาน (REQ-TMP-003)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพฟอร์ม: to_image.py วิธี LibreOffice → PDF → pypdfium2 (1 หน้า) = หน้ากระดาษจริงจาก docx → ถ้อยคำยึด content.html · ตำแหน่ง/เส้นยึดภาพ (ภาพอ่านได้ชัด)
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC ล้วน
- form_spec_check: ERROR 0 · WARN 0 · 14 ช่อง (ระบบ 4 · กรอก 8 · ระบบใส่ 2) · ตัวเลือก 1 (อนุมัติ/ไม่อนุมัติ) · ลายเซ็น 3 (ผู้มาติดต่อ=other · พนักงานผู้รับการติดต่อ=requester · ผู้บังคับบัญชาต้นสังกัด=approver) · ค่าคงที่ 1 (ชื่อบริษัท → Company.name_th) · ข้อมูลขัดกัน 4
- ฟอร์มว่าง ไม่มีข้อมูลส่วนบุคคลตัวอย่าง · ชื่อเอกสารไม่เพี้ยน (ไม่ต้อง rename) · หัวฟอร์ม "แบบฟอร์มขออนุญาตเข้าพื้นที่สำนักงาน" FM-HRM-05 Rev. 00 : 01/07/2569
- ผู้ขอในระบบ = พนักงานผู้รับการติดต่อ (host) บันทึกข้อมูลผู้มาติดต่อแทน · ผู้มาติดต่อเป็นบุคคลภายนอก ลงนามด้วยมือบนแบบพิมพ์
- feature ที่ใกล้: ไม่มีใน FEATURE_REGISTRY (HR / Policy Center·Security Control ใกล้สุด) → ใช้ F-TMP-003 ชั่วคราว · เสนอ feature ใหม่ "Visitor Access Request" ใน _BATCH_REPORT
- 2026-10-08 13:17 · ขั้น 1 → done · FORM_SPEC ERROR 0 · PREBRIEF v2 จาก FORM_SPEC

## ขั้น 2 · gate (unattended — AI-DEFAULT)
- G1: ไม่เปลี่ยน config/ไม่ส่งต่อ — บันทึกขออนุญาตเข้าพื้นที่ ไม่ต่อระบบบัตรผ่าน/ประตูรอบนี้
- G2: กระดาษมีช่องผู้อนุมัติ 1 จุด (ผู้บังคับบัญชาต้นสังกัด) → DOA dynamic 1 ขั้น role-line-manager · ไม่มีวงเงิน (role-line-manager ยังไม่อยู่ใน DOA master → แจ้งในรายงาน)
- G3: ชื่อบริษัท 2 จุดอ่านจาก Company.name_th · ไม่อนุมัติต้องมีความเห็น (บล็อก) · วันที่ลงนามก่อนวันเข้าพื้นที่ = เตือน · G4: ไม่มีรายการซ้ำ (lock สร้าง DEC-05 ให้เสมอ — ไม่มีผล) · G5: 1:1
- G6: ช่องลงนามผู้มาติดต่อ (บุคคลภายนอก) คงไว้บนแบบพิมพ์ให้เซ็นมือ · ช่องพนักงาน/ผู้บังคับบัญชาเป็นข้อความ "ส่งในระบบ/พิจารณาในระบบ"
- G7: ไม่อนุมัติ → กลับร่าง · ยกเลิก เจ้าของ+admin ที่ร่าง/รออนุมัติ เหตุผลบังคับ · G8: เจ้าของ · ผู้อนุมัติหลังส่ง · role-mgr-hr เห็นทั้งหมด · G9: VAR ออกเลขบันทึกครั้งแรก · G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock พร้อมเริ่มทำ (15 มติ · AI-DEFAULT 11 · VALID 4) · dm.sh tag แล้ว
- 2026-10-08 13:18 · ขั้น 2 → done · 15 มติ · AI-DEFAULT 11

## ขั้น 3 · declaration ร่าง
- doa: init → BLOCK G5 "on_reject ต้องเป็น back_to_draft หรือ end" (init เขียน `draft` จาก decisions → ไม่ตรงกับ validator) → แก้ yaml เป็น back_to_draft ตาม DEC-08 → VERDICT PASS · 1 ขั้น role-line-manager (INFO G1 relative role ยืนยันกับ DOA กลาง) · mock → VAR.doa.mock.js
- ntf: suggest ได้ var_over_limit_approved (review) → ตัด (ไม่มีเกณฑ์ตัวเลข) · เพิ่ม var_cancelled (ยกเลิกระหว่างรอ → ผู้อนุมัติขั้นปัจจุบัน + ผู้สร้าง) · ผลอนุมัติมาจาก doa_result · VERDICT PASS
- doccfg (หลังขั้น 4): VAR · ออกเลขบันทึกครั้งแรก · --registry ไม่ชน (ACL CSE EXI) · VERDICT PASS
- mdoc: VAR · FRM · F01 ชั่วคราว · source=declaration · doa=pending · VERDICT WARN (G04 taxonomy_def_id ว่าง · G09 doa pending)

## ขั้น 4 · แบบพิมพ์ Replica
- form.tpl.html สร้างจาก print/make_print.py (ถ้อยคำตาม content.html) · R2/R3/R4 เส้นประ · กรอบเจ้าหน้าที่ใช้ form-grid 1 ช่อง · R6 ☐ อนุมัติ/ไม่อนุมัติ · B6 sign_rows (ผู้ขอ + ขั้น DOA) + B7
- data 5 สถานะ (สมมติทั้งหมด): draft · approved · rejected · long-3steps · approved-doa6steps (7 ช่อง 4+3 dense)
- parity_check: IDENTICAL 5/5 · ไม่มี {{}} หลง · missing keys 0 · build_html ทุกสถานะ → print/out/*.html + VAR_template.html
- [NO-BROWSER] ข้าม render_pdf.py (ใน render_states.py — ลองแล้ว playwright launch ไม่ได้) → ไม่มี PDF/_states_sheet.png/จำนวนหน้า
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ PDF จาก browser)
- doa validate --print-config: PASS · print-spec + data-contract เขียนแล้ว
- 2026-10-08 13:21 · ขั้น 4 → done · parity 5/5 · [NO-BROWSER] ไม่มี PDF/compare
- 2026-10-08 13:21 · ขั้น 3 → done · doa PASS · ntf PASS · doccfg PASS · mdoc WARN G04/G09

## ขั้น 5 · HTML Q-form
- ฐาน: html-generator-v9 Q-form (_SOURCE + form-archetype) ผ่านโครงที่ใช้แล้วใน J002 (v9.4) → html/build_feature.py ประกอบ app_var.js + var_page.css + be-datepicker + print/form.tpl.html + tpl_render.js · เปิด GOLDEN_SKELETON + U1–U28 เทียบก่อน build
- U1 ✓ no-scorecard (badge ใน sub) · U2 ✓ · U3 ✓ · U4 ✓ · U5 ✓ kebab ⋮ · U6 ✓ page-size 25 + pager · U7 ✓ CSV ที่ head · U8 ✓ 920/1290 · U9 ✓ เหตุผลบังคับ (ไม่อนุมัติ/ยกเลิก) · U10 ✓ · U11 ✓ · U12 ✓ · U13 ✓ block §6.1 · U14 ✓ Q2 wizard 1290 (2 ส่วน + แนบไฟล์ · Rule #100F) · U15 ✓ · U16 n/a (ไม่มีลบ — ยกเลิกแทน) · U17 ✓ person icon วงกลม (รวมผู้มาติดต่อ) · U18 ✓ · U19 ✓ header sub = ผู้มาติดต่อ · วันที่ · U20 n/a (ชุดข้อมูลเดียว) · U21 ✓ · U22 ✓ · U23 ✓ empty-sub · U24 ✓ combobox พนักงาน (portal) · U25 ✓ backdrop onmousedown · U26–U28 n/a
- audit.sh: FAIL 0 · WARN 3 (มาจาก base-kit เดิม) · self_audit: รอบแรก FAIL (font 11.5 · hint > 60 ตัวอักษร 2 จุด) → แก้ → PASS · prune_css ตัด 78 rule แล้วรัน audit/self_audit ซ้ำ ผ่าน · node --check ผ่าน
- [NO-BROWSER] ข้าม e2e_standard.py · [NO-BROWSER] ข้าม render-check.py
- หมายเหตุ: smoke test ด้วย jsdom บนเครื่อง (_system/work/_scratch_J003/smoke.js) 28/29 ผ่าน — ข้อเดียวที่ไม่ผ่านคือเกณฑ์ในสคริปต์ทดสอบเอง (คาด ≥5 แถว ข้อมูลจริง E01 เห็น 4 ใบถูกต้อง) · ครอบ: สิทธิ์ G8 · validation · DEC-08/14/15 · DOA N ขั้น · API ล้ม · PDF — ไม่ใช่ด่านทางการ ต้องรัน e2e_standard บนเครื่องที่มี browser
- DOA: MOCK_DOA_RESOLVED 1 ขั้น role-line-manager → resolve จาก host · ไม่อนุมัติ = กลับร่างเลขเดิม (lastReject แสดง banner + ☑ ไม่อนุมัติใน PDF) · ผู้รับการติดต่อที่ไม่มีผู้บังคับบัญชา = บล็อก
- 2026-10-08 13:31 · ขั้น 5 → done · audit FAIL 0 · self_audit PASS · [NO-BROWSER] e2e ข้าม
- 2026-10-08 13:31 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-003.md/.docx (Prebrief + Lane Mode) · AI Review C1–C20 → APPROVED (C16 WARN ไม่มี registry — feature ชั่วคราว) · OQ 7 ข้อ
- FRD_F-TMP-003_Pack 00–07 + INDEX · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 11
- declaration --final: doccfg PASS (--registry ไม่ชน · numbering.frd_ref 03_LOGIC FN-03 · snapshot FN-05) · ntf PASS (var_cancelled frd_ref FN-06/FN-08) · doa PASS (--print-config) · mdoc WARN (G04 taxonomy_def_id ว่าง — OQ-06 · G09 doa pending)
- สำเนา declaration --final วางใน FRD_F-TMP-003_Pack/declarations/ (เหมือน J002)
- 2026-10-08 13:36 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 · doccfg/ntf --final PASS

## ขั้น 8 · UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-003.md (html/ui_brief_gen.py จาก inventory + อ่านโค้ดจริง) · brief_check: PASS · FAIL 0 · WARN 0 (B1–B8)
- testcases-F-TMP-003.md: 47 เคส / 82 step (html/tc_cases.py + tc_gen.py) · tc_lint ERROR 0 · Coverage Ledger + Audit (AC 14/14 · BR 12/12 · VR 8/8 · EC 10/11 ข้าม 1 มีเหตุผล · DEC 15/15)
- [NO-BROWSER] ข้าม verify_anchors.py
- cases.json (Lite 41 เคส · drop ledger 6) · lite_audit: หายเงียบ 0 · ประทับ meta.source แล้ว
- [NO-BROWSER] ข้าม capture.py — ไม่มีภาพประกอบ step (shots_empty.json) · build.py → testcase-F-TMP-003.html (41 เคส · 11 หมวด)
- 2026-10-08 13:42 · ขั้น 8 → done · brief_check PASS · tc_lint 0 · lite_audit หายเงียบ 0 · [NO-BROWSER] verify_anchors/capture ข้าม

## ขั้น 9 · ตรวจรวม + แพ็ก
- เปลี่ยนชื่อ orig/content.html → content.extract.htm (กัน K2 นับเป็น prototype ซ้ำ — เหมือน J002) · ไฟล์ช่วยทำงาน (smoke.js, literal dir ที่สร้างพลาด) อยู่ใน _system/work/_scratch_J003
- consistency_check: READY · BLOCK 0 · WARN 1 (K9 ไม่มี report e2e_standard — [NO-BROWSER]) · PASS 8
- [NO-BROWSER] ไม่มี _states_sheet.png / screenshot หน้าจอหลักใน DevPack (ไม่มี browser บนเครื่อง และไม่คัดไฟล์ไป render นอกเครื่อง) → ต้องรันรอบเต็มบนเครื่องที่มี browser
- dm.sh pack J003 → _pack/F-TMP-003_DevPack.zip (55 ไฟล์ · READY)
- 2026-10-08 13:42 · ขั้น 9 → done · consistency READY BLOCK 0 · zip _pack/F-TMP-003_DevPack.zip
