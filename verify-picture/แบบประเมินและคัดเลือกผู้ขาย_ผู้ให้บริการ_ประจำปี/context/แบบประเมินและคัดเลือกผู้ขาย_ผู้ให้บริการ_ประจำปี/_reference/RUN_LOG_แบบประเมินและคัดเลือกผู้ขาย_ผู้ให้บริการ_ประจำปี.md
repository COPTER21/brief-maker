# RUN_LOG — F-TMP-004 FM-PUR-01 แบบประเมินและคัดเลือกผู้ขายผู้ให้บริการ ประจำปี (REQ-TMP-004)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ไฟล์ต้นฉบับนามสกุล .xlsx แต่จริงเป็น Excel 97-2003 (OLE/.xls) → `to_image.py` (openpyxl) อ่านไม่ได้ ("File contains no valid workbook part") · ทดแทน: คัดสำเนาเป็น .xls นอก workspace → LibreOffice → PDF → pdftoppm → `orig/page-1.png` (หน้ากระดาษจริง A4 1 หน้า · ฟอนต์ไทยเป็นกล่อง) + ถ้อยคำ/ตารางจาก xlrd → `orig/content_text.htm` (ตั้งชื่อ .htm ตั้งแต่แรก กัน K2) · header/footer: DOC.No. : FM-PUR-01 / REV.00 : 01/07/2569
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC (--module PUR)
- form.title = "แบบประเมินและคัดเลือกผู้ขาย/ผู้ให้บริการ ประจำปี" (จากหัวฟอร์ม) · ชื่อในคิวไม่เพี้ยน (แค่ไม่มี "/") → ไม่ rename
- form_spec_check: ERROR 0 · 16 ช่อง · แถวซ้ำ 1 (หัวข้อประเมิน 4 ข้อ) · ตัวเลือก 5 · สูตร 3 · ลายเซ็น 3 · anomalies 6 (คะแนนเฉลี่ย=คะแนนเต็ม · สรุปผลต้องคำนวณ · <6 ต้องผู้บริหารพิจารณาแต่ไม่มีช่อง · สเกลคะแนน · สะกดผิด · ไฟล์ .xls)
- ไม่มีข้อมูลส่วนบุคคล/ชื่อผู้ขายจริงในไฟล์ (ฟอร์มเปล่า)
- 2026-10-10 05:03 · ขั้น 1 → done · FORM_SPEC 16 ช่อง ERROR 0 · PREBRIEF v2 สร้างจากฟอร์ม

## ขั้น 2 · gate (unattended — AI-DEFAULT 11 มติ + VALID 6)
- G1 ใบประเมินผู้ขายประจำปี ไม่เปลี่ยนค่า/ไม่ส่งต่อ (Supplier/Vendor master ยังไม่มี → กรอกชื่อ/รหัสผู้ขายเอง)
- G2 กระดาษมีช่องพิจารณา 2 จุด → dynamic 2 ขั้น: ผู้จัดทำ (แผนกจัดซื้อ) = role-pur-officer (**ไม่อยู่ใน DOA contract → แจ้ง report**) · ผู้จัดการแผนกจัดซื้อ = role-mgr-pur · ผลไม่ผ่าน (<6) → DOA กลางเพิ่มขั้นผู้บริหาร (role-gm) แบบมีเงื่อนไข — TODO: DOA engine
- G3 หัวข้อ/คะแนนเต็ม/เกณฑ์ผ่าน/มาตรฐาน อ่านจาก VendorEvaluationConfig (เสนอเป็น config ของ feature นี้) · คะแนนเกินคะแนนเต็ม = บล็อก (ขัดแย้งทางตรรกะ) · คะแนนรวม/สรุปผล คำนวณล้วน
- G4 หัวข้อจาก config · G5 1:1 คงคำ "คะแนนเฉลี่ย" + แก้สะกด 5 คำ · G6 แถวล่างต่อขั้น · G7 กลับร่าง · G8 admin = role-mgr-pur · G9 VEV ออกเลขตอนบันทึกครั้งแรก · G10 แนบ ✓ CSV ✓
- 2026-10-10 05:03 · ขั้น 2 → done · 17 มติ (AI-DEFAULT 11 · VALID 6) พร้อมเริ่มทำ

## ขั้น 3 · declaration ร่าง
- doa: init เขียน on_reject: draft แต่ validate รับเฉพาะ back_to_draft|end → แก้เป็น back_to_draft (ความหมายเดิมตาม DEC-08) · เติม `conditional_steps` (ผลไม่ผ่าน → + role-gm "ผู้บริหาร") สถานะ proposed — TODO: DOA engine (DEC-14) · validate WARN: role-pur-officer ไม่อยู่ใน contract (แจ้ง report)
- ntf: เติม vev_evaluation_failed (DEC-13/14 · หมายเหตุใต้สรุปผล) → PASS
- doccfg + mdoc ทำหลังขั้น 4 (ต้องใช้ print_config)
- 2026-10-10 05:04 · ขั้น 3 → done · doa WARN (role-pur-officer นอก contract) · ntf PASS (doccfg/mdoc หลังขั้น 4)

## ขั้น 4 · แบบพิมพ์ Replica (R9 ตารางกรอบ + R10 2 หน้า)
- ออกแบบ 2 หน้าตาม R10: ต้นฉบับ 1 หน้าเต็มหน้าแล้ว — DOA 6 ขั้น (7 ช่อง 2 แถว) / หัวข้อจาก config 12 ข้อ เกิน A4 ที่ฟอนต์ ≥ 8pt (8.5pt) · ตัดหน้าก่อน "ระบบการบริหารงานที่ได้รับรองมาตรฐานต่างๆ" · หน้า 2 = มาตรฐาน + สรุปผล + หมายเหตุ + ความคิดเห็น + ลงชื่อทั้งก้อน · thead ซ้ำ · "หน้า n/2"
- parity_check: IDENTICAL 5/5 (draft · approved · rejected · long-12criteria · approved-doa6steps 4+3)
- [NO-BROWSER] ข้าม render_pdf.py (ใน render_states.py — playwright launch fail) → render_doc.py --strict + build_html.py เองครบ 5 สถานะ (ไม่มี {{}} หลง · missing key 0 · โครง 2 หน้าทุกสถานะ) · ไม่มี PDF / _states_sheet.png
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ approved.pdf)
- ไฟล์ค้าง `print/out/_approved-doa6steps.body.html` จากรอบ render_states ที่ fail (ถูกเขียนทับด้วยรอบ render_doc แล้ว)
- doccfg VEV PASS (registry ไม่ชน: ACL/FEC/FLI · J003 ใช้ SMC) · mdoc WARN (taxonomy_def_id ว่าง · doa pending · function_code F01 ชั่วคราว) · source=declaration เพราะ REQ-TMP-004 ไม่ใช่รูปแบบ REQ-YYYY-NNNN
- doa validate --print-config: WARN (role-pur-officer นอก contract) · BLOCK 0
- 2026-10-10 05:08 · ขั้น 4 → done · 2 หน้า R10 · parity 5/5 · [NO-BROWSER] ไม่มี PDF/compare · doccfg PASS · mdoc WARN

## ขั้น 5 · HTML Q-form (html-generator v9.4)
- ฐาน: kit กลาง + shell จาก feature ที่ผ่านด่านแล้ว (J002 · BASE-KIT ไม่แก้) เทียบ GOLDEN_SKELETON/U1–U28 · page CSS + app JS ของ VEV เขียนใหม่ทั้งชุด · ฝัง form.tpl.html + tpl_render.js + PDF_CSS (base+replica+profile ไม่รวม @font-face)
- โดเมน: wizard 3 ขั้น · ขั้น 1 = ① ผู้ขาย (ชื่อ/รหัส · ☐สินค้า ☐บริการ เลือกได้ทั้งคู่ + ระบุ · เลขอ้างอิง · เครดิต) ② ให้คะแนน 4 หัวข้อจาก VEV_CONFIG (0..คะแนนเต็ม ทศนิยม 1) + บรรทัดคำนวณสด (soft update) ③ มาตรฐาน 8 ตัวเลือก (+อื่นๆ ระบุ) ④ ความคิดเห็น · การ์ดสรุปขวา (สายอนุมัติตามผล · เตือนผู้ขายซ้ำในปี)
- DOA: MOCK_DOA_RESOLVED 2 ขั้น (role-pur-officer เห็นด้วย/ไม่เห็นด้วย → role-mgr-pur อนุมัติ/ไม่อนุมัติ) + MOCK_DOA_CONDITIONAL (ไม่ผ่าน → + role-gm) — TODO: DOA engine · slot picker ต่อขั้น · ผู้ส่งไม่อยู่ในรายชื่อ
- audit.sh: FAIL 0 · WARN 3 (มาจาก BASE-KIT เดิม: #21 icon ใน kit · #40 .uc-email · font-size px ใน kit) · prune_css ตัด 3 rule แล้ว audit ซ้ำ FAIL 0
- [NO-BROWSER] ข้าม e2e_standard.py · ข้าม render-check.py → ทดแทนด้วย smoke test jsdom (reports/smoke_jsdom.js → smoke_jsdom_report.txt) 38/38 PASS: สิทธิ์ G8 (owner/ผู้พิจารณา/admin) · ทุก tab ทุกใบ 4 persona ไม่มี error · PDF 2 หน้าไม่มี {{}} · ☑ ไม่ผ่าน + ช่องผู้บริหาร · validation (ชื่อ/รหัส · ประเภท+ระบุ · คะแนนเกิน/ทศนิยม/ไม่ใช่ตัวเลข · อื่นๆ) · เตือนซ้ำ · ไม่ผ่าน → 3 ขั้น + แจ้ง vev_evaluation_failed · ไม่เห็นด้วย → กลับร่างเลขเดิม → แก้ → ผ่าน 2 ขั้น → อนุมัติ · DOA push 3 ขั้น · ร่างไม่ครบส่งไม่ได้ · ยกเลิก · S.sim · DOC.active · CSV
- U1–U28: U1✓ no-scorecard (นับใน ph-count) · U2✓ · U3✓ · U4✓ · U5✓ kebab ⋮ · U6✓ pager 25 · U7✓ CSV ที่ head · U8✓ 920/1290 · U9✓ เหตุผลบังคับ · U10✓ pill · U11✓ · U12✓ lucide mono · U13✓ block ลายเซ็นกลาง · U14✓ Q2 wizard 3 ขั้น · U15✓ edit = wizard เดียวกัน · U16 n/a (ไม่มีลบ ใช้ยกเลิก+เหตุผล) · U17✓ person icon · U18✓ ชื่อผู้ขาย ellipsis 1 บรรทัด · U19✓ header sub 2 fact · U20✓ segmented (ทั้งหมด/รอฉันพิจารณา) ไม่ซ้ำแกน filter · U21✓ (page CSS ใช้ --fs-*) · U22✓ · U23✓ empty panel (มาตรฐานไม่ระบุ) · U24✓ search-select · U25✓ backdrop onmousedown · U26–U28 n/a (VendorEvaluationConfig เสนอเป็นหน้า config ใน report)
- 2026-10-10 05:19 · ขั้น 5 → done · audit FAIL 0 · [NO-BROWSER] e2e ข้าม → jsdom smoke 38/38 · U1–U28 ✓
- 2026-10-10 05:19 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-004.md (+ .docx md_to_docx) · Prebrief Mode · AI Review C01–C23/PE01–05 → APPROVED (C22 ตัวชี้วัด → OQ-01 ตามกติกา ห้ามแต่งตัวเลข)
- FRD_F-TMP-004_Pack 00–07 + INDEX · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 15
- declaration --final: DOCCFG PASS (registry ACL/FEC/FLI ไม่ชน · VEV) · NTF PASS · DOA WARN (role-pur-officer นอก contract · เติม §9 ขั้นตามเงื่อนไขผลประเมิน TODO: DOA engine) · MDOC WARN (G04 taxonomy_def_id ว่าง · G09 doa pending · function_code F01 ชั่วคราว) → คัดลง FRD_F-TMP-004_Pack/declarations/
- 2026-10-10 05:25 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · declaration --final BLOCK 0 (doa/mdoc WARN)

## ขั้น 8 · UI Brief → test case AI → UAT
- html-ui-brief: extract_anchors (vars 47 · z 21 · routes 5 · toast 12) → UI_BRIEF_F-TMP-004.md · brief_check PASS (FAIL 0 · WARN 0) · หมายเหตุ: route เดิมประกอบจากค่าคงที่ ROOT → extract ได้ 0 → แก้เป็น string literal แล้ว rebuild (audit FAIL 0 · smoke 38/38 ซ้ำ)
- ai-testcase-md-generator: testcases-F-TMP-004.md 62 เคส / 147 step · tc_lint ERROR 0 · Ledger (AC 15/15 · BR 19/19 + BR-DOA-05 ไม่ใช้ · VR 10/10 · EC 10/12 (EC-07 แก้ DOA กลาง · EC-10 config เปลี่ยน — ไม่มีหน้าจอ) · error 20/20 · permission 14/14 · XT 4/4 · DEC 17/17)
- [NO-BROWSER] ข้าม verify_anchors.py (playwright) — anchor ตรวจด้วย jsdom smoke + อ่านโค้ด
- qa-friendly: cases.json Lite 51 เคส · lite_audit หายเงียบ 0 (drop ledger 11) --stamp · [NO-BROWSER] ข้าม capture.py → shots_b64.json ว่าง ({}) · build testcase-F-TMP-004.html
- 2026-10-10 05:31 · ขั้น 8 → done · brief_check PASS · tc_lint ERROR 0 (62 เคส) · lite_audit หายเงียบ 0 · [NO-BROWSER] verify_anchors/capture ข้าม
