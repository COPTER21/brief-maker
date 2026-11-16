# RUN_LOG — F-TMP-003 FM-WHS-09 สรุปผลการเคลียร์สินค้า Slow Move (REQ-TMP-003)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพฟอร์ม: `to_image.py` แปลงผ่าน LibreOffice → PDF → pypdfium2 (หน้ากระดาษจริง A4 แนวนอน scale 78%) แต่เครื่องไม่มีฟอนต์ไทย → ตัวอักษรไทยในภาพเป็นกล่อง · ถ้อยคำยึด xlsx (openpyxl) / content.html · ตำแหน่ง/เส้นยึดภาพ · ใช้เสร็จเปลี่ยนชื่อ orig/content.html → orig/content_text.htm (กัน K2)
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC (module WHS)
- form.title = "สรุปผลการเคลียร์สินค้า Slow move" (หัวฟอร์ม A3 ตัด "ประจำเดือน …" ซึ่งเป็นช่อง F03) · ชื่อในคิวไม่เพี้ยน → ไม่ rename
- แถว 4 ของไฟล์ = หัวตารางร่างเดิมไม่มีเส้น ("]efy" · วันผลิต ×2) ไม่ปรากฏเป็นตารางในภาพ → ยึดหัวแถว 5 · บันทึกเป็น anomaly
- form_spec_check: ERROR 0 · 12 ช่อง · แถวซ้ำ 1 กลุ่ม (23 แถว) · ลายเซ็น 2 (ผู้จัดทำ · ผู้อนุมัติ) · anomalies 4
- รหัสสินค้า/รายละเอียด อ่านจาก Product Master (F-PRODUCT-MASTER-001 · T_product) อ่านอย่างเดียว
- 2026-10-10 05:01 · ขั้น 1 → done · FORM_SPEC 12 ช่อง ERROR 0 · PREBRIEF v2 สร้างจากฟอร์ม

## ขั้น 2 · gate (unattended — AI-DEFAULT 11 มติ + VALID 4)
- G1 ใบสรุปผลประจำเดือน ไม่เปลี่ยนค่า/ไม่ตัดสต็อก/ไม่ส่งต่อ (Inventory/Stock Adjustment ยังไม่มี) · G2 ช่อง "ผู้อนุมัติ" 1 จุดไม่ระบุตำแหน่ง → role-mgr-wh (ผู้จัดการ module inventory · มีใน contract) · G3 แนวทางการเคลียร์จาก config + กฎวันที่/จำนวน
- G4 ไม่จำกัดแถว · PDF ขั้นต่ำ 23 · G5 1:1 ไม่ใช้หัวร่างแถว 4 · G6 แถวล่างต่อขั้น · G7 กลับร่าง · G8 admin = role-mgr-wh · G9 SMC ออกเลขตอนบันทึกครั้งแรก · G10 แนบ ✓ CSV ✓
- 2026-10-10 05:02 · ขั้น 2 → done · 15 มติ (AI-DEFAULT 11 · VALID 4) พร้อมเริ่มทำ

## ขั้น 3 · declaration ร่าง
- doa: init เขียน on_reject: draft → แก้เป็น back_to_draft (ความหมายเดิมตาม DEC-08 · validate รับเฉพาะ back_to_draft|end) → PASS · 1 ขั้น role-mgr-wh ป้าย "ผู้อนุมัติ"
- ntf: เก็บ smc_cancelled · ตัด smc_over_limit_approved (ไม่มีเกณฑ์ตัวเลข/วงเงิน) → PASS
- doccfg + mdoc ทำหลังขั้น 4 (ต้องใช้ print_config)
- 2026-10-10 05:02 · ขั้น 3 → done · doa PASS · ntf PASS (doccfg/mdoc หลังขั้น 4)

## ขั้น 4 · แบบพิมพ์ Replica (R9 ตารางกรอบ + R10 2 หน้า)
- ต้นฉบับ A4 แนวนอน 1 หน้า (scale 78%) แต่ engine thai-doc ล็อก A4 แนวตั้ง (base.css ห้ามแก้) → จัดตาราง 27 คอลัมน์ฐานตามสัดส่วนเดิม · ถ้อยคำ/ลำดับคอลัมน์ 1:1
- ออกแบบ 2 หน้าตาม R10: แถวจริง 23 (> ~20) + บล็อกลงชื่อ DOA N ขั้น · หน้า 1 = หัว + ตาราง 23 แถวเท่ากระดาษ + "มีต่อหน้าถัดไป" · หน้า 2 = ใบต่อ (หัวย่อ + หัวตารางซ้ำ + แถว 24+ ขั้นต่ำ 5 สูงสุด 30) + ลงชื่อทั้งก้อน · ฟอนต์ 8.5pt · "หน้า n/2"
- parity_check: IDENTICAL 5/5 (draft · approved · rejected · long-45items · approved-doa6steps 4+3)
- [NO-BROWSER] ข้าม render_pdf.py (ใน render_states.py) — render body + build_html เองครบ 5 สถานะ (ไม่มี {{}} หลง · missing key 0 · โครง 2 หน้าทุกสถานะ)
- ตรวจภาพเพิ่ม: render out/<state>.html ชุดเดียวกันด้วย Chromium ใน container ของ agent → ทุกสถานะ 2 หน้า ไม่ล้น · ปรับคอลัมน์ 2 รอบ (รายละเอียดตัดบรรทัด · "ลำดับ" ถูกตัดตอน dense) → out/_states_sheet.png (คัดกลับเครื่องให้คนดู)
- [NO-BROWSER] ข้าม compare_original.py (ไม่มี approved.pdf บนเครื่อง) · คาด WARN เพราะเปลี่ยนแนวกระดาษ — บันทึกใน print-spec §7
- ไฟล์ค้างลบไม่ได้ (workspace ห้ามลบ): print/out/_<state>.body.html (ไฟล์ชั่วคราว) · reports/_unused_long40.bak (ว่าง · data ชุดแรกก่อนปรับ)
- doccfg SMC PASS (registry ไม่ชน · J004 ใช้ VEV) · mdoc WARN (G04 ไม่มี taxonomy_def_id · G09 doa pending · function_code F01 ชั่วคราว) · source=declaration เพราะ REQ-TMP-003 ไม่ใช่รูปแบบ REQ-YYYY-NNNN
- doa validate --print-config PASS
- 2026-10-10 05:08 · ขั้น 4 → done · 2 หน้า R10 · parity 5/5 · [NO-BROWSER] ไม่มี PDF/compare (ภาพตรวจจาก Chromium container) · doccfg PASS · mdoc WARN
- แก้ถ้อยคำกฎ G3 (DEC-04): ห้ามวันอนาคตเฉพาะ วันที่ติดตาม/วันที่เคลียร์ (วันหมดอายุเป็นอนาคตได้) → lock ใหม่ + tag (ระหว่างขั้น 5 · ความหมายเดิม แก้คำกำกวม)

## ขั้น 5 · HTML Q-form (html-generator v9.4)
- ฐาน: kit กลาง (file-skeleton BASE-KIT + BE Date Picker Rule 114 · ไม่แก้ BASE-KIT) + form-archetype page CSS + page CSS ของ SMC · โครง/แพตเทิร์นเทียบ GOLDEN_SKELETON + U1–U28 และงานผ่านด่านก่อนหน้า (J002) · ฝัง form.tpl.html + tpl_render.js + PDF_CSS (base+replica+profile)
- แถวรายการ 9 ช่อง > 4 → ตารางกรอก (Rule #107) · รหัสสินค้า = search-select จาก Product Master · วันที่ทุกช่อง = bedate พ.ศ. (ไม่มี type=date) · แนวทางการเคลียร์จาก SlowMoveConfig + ระบุเพิ่มเติม
- audit.sh: FAIL 0 · WARN 3 (จาก BASE-KIT เดิม: #21 icon ใน kit · #40 .uc-email · font-size px ใน kit) · prune_css ตัด 58 rule แล้ว audit ซ้ำ FAIL 0
- [NO-BROWSER] ข้าม e2e_standard.py · ข้าม render-check.py → ทดแทนด้วย smoke test jsdom (reports/smoke_jsdom.js) 44/44 PASS: สิทธิ์เห็น (owner/approver/admin) · ทุก tab ทุกใบ ไม่มี error · PDF 2 หน้าไม่มี {{}} (23+5 / ยาว 40 = 23+17 dense) · validation (≥1 รายการ · วันที่ติดตาม/แนวทางบังคับ · วันอนาคต · วันที่เคลียร์ก่อนวันที่ติดตาม · วันที่+จำนวนคู่กัน · จำนวน>0 · "อื่น ๆ" ต้องระบุ) · เตือนหมดอายุ/สินค้าซ้ำ · ส่ง → ไม่อนุมัติ → แก้ → ส่งใหม่ → อนุมัติ · DOA 2 ขั้นเรียงขั้น · ยกเลิก · DOC.active · S.sim · CSV · ไม่มี JS error
- ตรวจภาพเพิ่ม (Chromium ใน container ของ agent · ไม่มีไอคอนเพราะ offline): list · wizard · view แสดงถูก · ตารางกรอกเลื่อนแนวนอนได้ในจอ 1440 (ตั้งใจ — คงคอลัมน์ 1:1)
- U1–U28: U1✓ no-scorecard (นับใน ph-count) · U2✓ · U3✓ · U4✓ · U5✓ kebab ⋮ · U6✓ pager 25 · U7✓ CSV ที่ head · U8✓ 920/1290 · U9✓ เหตุผลบังคับ · U10✓ pill · U11✓ · U12✓ lucide mono · U13✓ block ลายเซ็นกลาง · U14✓ Q2 wizard 3 ขั้น · U15✓ edit = wizard เดียวกัน · U16 n/a (ไม่มีลบเอกสาร ใช้ยกเลิก+เหตุผล · ลบแถวในตารางกรอก) · U17✓ person icon · U18✓ · U19✓ header sub 2 fact · U20✓ segmented (ทั้งหมด/รอฉันอนุมัติ) · U21✓ (page CSS ใช้ --fs-*) · U22✓ · U23✓ empty panel ทุกตาราง · U24✓ search-select · U25✓ backdrop onmousedown · U26–U28 n/a (ไม่มีหน้า config — SlowMoveConfig เสนอเป็น feature ใหม่)
- 2026-10-10 05:19 · ขั้น 5 → done · audit FAIL 0 · [NO-BROWSER] e2e ข้าม → jsdom smoke 44/44 · U1–U28 ✓
- 2026-10-10 05:19 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-003.md (+ .docx md_to_docx) · Prebrief Mode · AI Review C01–C23/PE01–05 → APPROVED (C22 ตัวชี้วัด → OQ-01 ตามกติกา ห้ามแต่งตัวเลข) · OQ 8 ข้อ
- FRD_F-TMP-003_Pack 00–07 + INDEX · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 11
- declaration --final: DOCCFG PASS (registry ไม่ชน · SMC) · NTF PASS · DOA PASS (print_config) · MDOC WARN (G04 taxonomy_def_id ว่าง · G09 doa pending · function_code F01 ชั่วคราว) → คัดลง FRD_F-TMP-003_Pack/declarations/
- 2026-10-10 05:24 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · declaration --final PASS (mdoc WARN)

## ขั้น 8 · UI Brief → test case AI → UAT
- html-ui-brief: extract_anchors (vars 46 · z 26 · routes 0 (hash ผ่าน go/RT) · toast 11) → UI_BRIEF_F-TMP-003.md · brief_check PASS (FAIL 0 · WARN 0) — รอบแรก B5 FAIL (#bd-* id สร้างแบบ dynamic) แก้เป็นอ้าง key แล้วผ่าน
- ai-testcase-md-generator: testcases-F-TMP-003.md 60 เคส / 129 step · tc_lint ERROR 0 · Ledger ครบ (AC 15/15 · BR 18/19 · VR 8/8 · EC 8/10 · error 23/23 · permission 14/14 · XT 4/4 · DEC 15/15)
- [NO-BROWSER] ข้าม verify_anchors.py (playwright) — anchor ตรวจด้วย jsdom smoke + สคริปต์เทียบข้อความตัวหนากับ feature.html (ที่ไม่ตรงตัว = ข้อความประกอบ dynamic ตรวจด้วยโค้ดแล้ว)
- qa-friendly: cases.json Lite 47 เคส / 82 step · lite_audit หายเงียบ 0 (drop ledger 13) --stamp · [NO-BROWSER] ข้าม capture.py → shots_b64.json ว่าง {} · build testcase-F-TMP-003.html
- 2026-10-10 05:36 · ขั้น 8 → done · brief_check PASS · tc_lint ERROR 0 (60 เคส) · lite_audit หายเงียบ 0 · [NO-BROWSER] verify_anchors/capture ข้าม
