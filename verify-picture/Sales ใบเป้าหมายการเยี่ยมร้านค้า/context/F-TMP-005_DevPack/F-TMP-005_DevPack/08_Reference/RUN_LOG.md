# RUN_LOG — F-TMP-005 ใบเป้าหมายการเยี่ยมร้านค้า (REQ-TMP-005)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพฟอร์ม: to_image.py วิธี LibreOffice → PDF → pypdfium2 (1 หน้า · A4 แนวนอน) = หน้ากระดาษจริงจาก xlsx · ถ้อยคำยึด content.html + อ่านเซลล์ด้วย openpyxl (sheet เดียว "FM-SAL-09" · print area B1:P44) · Doc No./Rev. อ่านจาก footer ขวา
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC ล้วน (--module Sales)
- form_spec_check: ERROR 0 · WARN 0 · 17 ช่อง · แถวซ้ำ 1 (วันทำงาน 1–31) · สูตร 2 (จำนวนลูกค้า = นับร้าน · แถวรวม) · ลายเซ็น 3 (ผู้นำเสนอ · ผู้อนุมัติ × 2) · ข้อมูลขัดกัน 7
- ฟอร์มว่าง ไม่มีข้อมูลส่วนบุคคล/ชื่อร้านตัวอย่าง · ชื่อเอกสารไม่เพี้ยน (ไม่ต้อง rename) · หัวฟอร์ม "ใบเป้าหมายการเยี่ยมร้านค้า : เขตการขาย General Trade" FM-SAL-09 Rev.00:01/07/2569
- feature ที่ใกล้: Sales · Visit Operation ⟂ (H @sales) + Sales Territory ⟂ + Customer (FEATURE_REGISTRY ยังไม่มีรหัส) → ใช้ F-TMP-005 ชั่วคราว
- 2026-10-08 13:54 · ขั้น 1 → done · FORM_SPEC ERROR 0 · PREBRIEF v2 จาก FORM_SPEC

## ขั้น 2 · gate (unattended — AI-DEFAULT)
- G1: ไม่เปลี่ยน config/ไม่ส่งต่อ — แผนเยี่ยมเก็บในเอกสารนี้ ไม่แก้ Customer/Sales Territory ไม่สร้าง Visit อัตโนมัติ
- G2: ช่อง "ผู้อนุมัติ" 2 ช่อง ไม่ระบุตำแหน่ง → dynamic 2 ขั้น role-line-manager (relative role — ไม่อยู่ใน DOA master 14 role → แจ้งในรายงาน) → role-mgr-sales (ผู้จัดการค่าเริ่มของ module sales) · ไม่มีวงเงิน
- G3: จำนวนลูกค้า = นับร้าน · แถวรวม · วันที่อยู่ในรอบ/ไม่ซ้ำ · ร้าน >7 เตือน · ร้านซ้ำในวันเดียว บล็อก · เขต+รอบเดียวกันอนุมัติได้ใบเดียว (ใบเดิม → ถูกแทนที่)
- G4: สูงสุด 31 แถว (วันทำงาน 1–31) PDF ≥31 · G5: 1:1 (คอลัมน์ว่างใต้ "วันทำงาน" ไม่ทำเป็นช่อง) · G6: แถวล่างต่อขั้น DOA · G7: ไม่อนุมัติ → กลับร่าง · ยกเลิก เจ้าของ+admin ร่าง/รออนุมัติ ระบุเหตุผล
- G8: เจ้าของ · ผู้อนุมัติหลังส่ง · role-mgr-sales ทั้งหมด · TO/CC เห็นใบอนุมัติแล้วที่ตนถูกระบุ · G9: SVT ออกเลขบันทึกครั้งแรก · G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock พร้อมเริ่มทำ (18 มติ · AI-DEFAULT 11 · VALID 7) · dm.sh tag แล้ว
- 2026-10-08 13:54 · ขั้น 2 → done · 18 มติ · AI-DEFAULT 11

## ขั้น 3 · declaration ร่าง
- doa: init → on_reject: draft (บั๊กสกิลที่รู้แล้ว) → แก้ yaml เป็น back_to_draft → validate PASS · 2 ขั้น role-line-manager → role-mgr-sales (INFO G1 relative role — ยืนยันกับ DOA กลาง) · validate --print-config PASS
- ntf: svt_cancelled · svt_plan_published (→ TO/CC เมื่ออนุมัติขั้นสุดท้าย) · svt_superseded · ตัด svt_over_limit_approved (เตือนร้าน >7 แสดงตอนกรอกพอ) · validate/brief PASS
- doccfg (หลังขั้น 4): SVT · {PREFIX}-{YYYY}-{run:4} · first_save · snapshot approved_final · --registry ไม่ชน · VERDICT PASS
- mdoc: SVT · FRM · function_code F01 ชั่วคราว · source=declaration (REQ-TMP-005 ไม่ใช่รูปแบบ REQ-YYYY-NNNN) · VERDICT WARN (G04 taxonomy_def_id ว่าง · G09 doa pending)

## ขั้น 4 · แบบพิมพ์ Replica
- form.tpl.html สร้างจาก print/make_print.py (ถ้อยคำตาม content.html/เซลล์ xlsx) · R1 โลโก้ซ้าย + R2 ชื่อบริษัท/ชื่อเอกสาร · R9 ตารางหัว (TO/CC/ผู้รับผิดชอบเขต/ตำแหน่ง/เขต/รอบการขาย) · R9 ตาราง 31 แถว 15 คอลัมน์ (ร้าน 7 ช่อง) + แถวรวม · B6 sign_rows (ผู้นำเสนอ + DOA N ขั้น) · B7
- data 5 สถานะ (สมมติทั้งหมด): draft · approved · rejected · long-31rows (บางวัน 12 ร้าน → ช่องที่ 7 ต่อชื่อ) · approved-doa6steps (7 ช่อง 4+3)
- parity_check: IDENTICAL 5/5 · render_doc --strict ไม่มี {{}} หลง · build_html ทุกสถานะ → print/out/*.html + SVT_template.html · body กลางอยู่ _system/work/_scratch_J005
- ข้อจำกัดสกิล: ต้นฉบับ A4 แนวนอน แต่ thai-doc v2.1 base.css ล็อก @page A4 portrait และ profile ไม่มี token orientation → prototype พิมพ์แนวตั้ง · print_config.paper = A4-landscape ให้ server · บันทึกใน print-spec §7 + รายงาน
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py ต้อง launch browser) — ใช้ render_doc.py + build_html.py แทน
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ PDF จาก browser) · ไม่มี _states_sheet.png (ไม่ได้ render นอกเครื่อง)
- 2026-10-08 13:57 · ขั้น 4 → done · parity 5/5 · [NO-BROWSER] ไม่มี PDF/compare · พิมพ์แนวตั้ง (สกิลไม่รองรับ landscape)
- 2026-10-08 13:57 · ขั้น 3 → done · DOA PASS 2 ขั้น · ntf PASS · doccfg PASS · mdoc WARN G04/G09

## ขั้น 5 · HTML Q-form
- ฐาน: html-generator-v9 references/form-archetype/_SOURCE (Q2) + เทียบ GOLDEN_SKELETON + U1–U28 → ประกอบด้วย html/build_feature.py (app_svt.js + svt_page.css + be-datepicker + print/form.tpl.html + tpl_render.js) · โครงเดียวกับ J004 (ผ่าน v9.4)
- domain: ส่วนหัว (เขตจาก Sales Territory ที่ตนรับผิดชอบ → ผู้รับผิดชอบเขต/ตำแหน่ง · รอบการขาย · TO ค่าเริ่ม = ผู้อนุมัติขั้นแรก · CC หลายคน) · แผนรายวัน (การ์ดต่อวัน ≤31: วันที่ พ.ศ. จำกัดในรอบ · เริ่มต้นตลาด = สิ้นสุดตลาด · ที่พัก (จังหวัด) · ร้านค้า multi-pick จาก Customer ในเขต · จำนวนลูกค้านับสด) · บล็อก: วันที่นอกรอบ/ซ้ำ · ช่องว่าง · ร้าน 0 · ร้านซ้ำในวัน · เตือน: ร้าน >7 · อนุมัติขั้นสุดท้าย → แจ้ง TO/CC + ใบเดิมเขต/รอบเดียวกัน → ถูกแทนที่
- U1 ✓ no-scorecard (badge ใน sub) · U2 ✓ · U3 ✓ · U4 ✓ · U5 ✓ kebab ⋮ · U6 ✓ page-size 25 + pager · U7 ✓ CSV ที่ head · U8 ✓ 920/1290 · U9 ✓ เหตุผลบังคับ · U10 ✓ · U11 ✓ · U12 ✓ · U13 ✓ block §6.1 · U14 ✓ Q2 wizard 1290 · U15 ✓ edit = ฟอร์มเดียว ปิด view ก่อน · U16 n/a (ไม่มีลบ — ยกเลิกแทน) · U17 ✓ person icon วงกลม · U18 ✓ (รายชื่อร้าน ellipsis + title) · U19 ✓ header sub = เขต · รอบ · U20 n/a ชุดข้อมูลเดียว · U21 ✓ · U22 ✓ badge ≤3 ค่า 0 ซ่อน · U23 ✓ empty-sub · U24 ✓ combobox portal (เขต/รอบ/TO/CC/ร้าน/จังหวัด) · U25 ✓ backdrop onmousedown · U26–U28 n/a
- audit.sh: FAIL 0 · WARN 3 (มาจาก base-kit เดิม — เหมือน J004) · self_audit: รอบแรก FAIL (flex_noalign .st-chips · naked_hints 1 · missing_ids 'day-') → แก้ align-items + ย่อ hint + querySelector → PASS · prune_css ตัด 65 rule แล้วรัน audit/self_audit ซ้ำ ผ่าน
- ตรวจเพิ่มบนเครื่อง (node · ไม่ใช้ browser · ไม่ใช่ผลด่านทางการ): node --check script หลัก OK · smoke test ฟังก์ชัน: docPrintData → 31 แถว · tplRender ไม่มี {{ หลง · validate (ซ้ำวันที่ → บล็อก · ฟอร์มว่าง → บล็อก) · สิทธิ์ CC เห็นเฉพาะใบอนุมัติ/ถูกแทนที่ · E02 อนุมัติขั้น 1 · E04 ขั้น 2 + เห็นทั้งหมด
- [NO-BROWSER] ข้าม e2e_standard.py · [NO-BROWSER] ข้าม render-check.py · ไม่มี screenshot หน้าจอ (ไม่ render นอกเครื่อง)
- DOA: MOCK_DOA_RESOLVED 2 ขั้น role-line-manager → role-mgr-sales (DOA-ENGINE-HOOK + TODO: DOA engine) · รองรับ N ขั้น (__QA__.doa.push) · field approver_role/approved_by/approval_chain อยู่ใน FRD
- 2026-10-08 14:07 · ขั้น 5 → done · audit FAIL 0 · self_audit PASS · [NO-BROWSER] e2e ข้าม
- 2026-10-08 14:07 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-005.md/.docx (Prebrief + Lane Mode · md_to_docx.py) · AI Review C1–C20 + PE02 SoD → APPROVED (C16 WARN ไม่มี registry — feature ชั่วคราว)
- FRD_F-TMP-005_Pack 00–07 + INDEX + declarations/ · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 13
- declaration --final: doccfg PASS (--registry ไม่ชน · numbering.frd_ref 03_LOGIC FN-03 · snapshot FN-05) · ntf PASS (frd_ref FN-07/09) · doa PASS (--print-config) · mdoc WARN (G04 taxonomy_def_id ว่าง — OQ-04 · G09 doa pending รอ wire)
- OQ เพิ่ม: OQ-06 คอลัมน์ว่างใต้ "วันทำงาน" · OQ-07 แบบพิมพ์ A4 แนวนอน (thai-doc ไม่มี orientation)
- 2026-10-08 14:12 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 · doccfg/ntf --final PASS

## ขั้น 8 · UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-005.md (html/ui_brief_gen.py จาก inventory + อ่านโค้ดจริง) · brief_check: รอบแรก FAIL B5 (อ้าง pickDayN / #dcnt-N ที่สร้างแบบ dynamic) → แก้ brief อ้าง setDayDate() / .day-cnt → PASS · FAIL 0 · WARN 0 (B1–B8)
- testcases-F-TMP-005.md: 41 เคส / 75 step · tc_lint ERROR 0 · Coverage Ledger + Audit (AC 14/14 · BR 15/15 · VR 10/10 · EC 9/10 ข้าม 1 มีเหตุผล · DEC 18/18)
- [NO-BROWSER] ข้าม verify_anchors.py — anchor เขียนจากข้อความคงที่ใน app_svt.js (ไม่ได้ตรวจด้วย browser)
- cases.json (Lite 37 เคส · drop ledger 4) · lite_audit: หายเงียบ 0 · ประทับ meta.source แล้ว
- [NO-BROWSER] ข้าม capture.py — ไม่มีภาพประกอบ step (regionKey = "") · build.py → testcase-F-TMP-005.html (37 เคส · 11 หมวด)
- 2026-10-08 14:17 · ขั้น 8 → done · brief_check PASS · tc_lint 0 · lite_audit หายเงียบ 0 · [NO-BROWSER] verify_anchors/capture ข้าม
