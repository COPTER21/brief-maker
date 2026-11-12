# RUN_LOG — F-TMP-006 FM-PUR-04 แบบฟอร์มเปิดเผยผลประโยชน์ทับซ้อนประจำปี 2569 (REQ-TMP-006)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ต้นฉบับ .docx → `to_image.py` (LibreOffice → PDF → pypdfium2) ได้ `orig/page-1.png` (A4 1 หน้า · ฟอนต์ไทยเป็นกล่อง) + `orig/SAMPLE.pdf` + content.html → เปลี่ยนชื่อเป็น `orig/content_text.htm` (กัน K2) · ถ้อยคำยึด content_text.htm/document.xml · ข้อความ "ฝ่ายกฎหมาย"/"วันที่" ในกรอบผู้บังคับบัญชาอยู่ใน textbox ที่ภาพตัดหาย
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC (--module PUR)
- form.title = "แบบฟอร์มเปิดเผยผลประโยชน์ทับซ้อนของแผนกจัดซื้อ ประจำปี" (หัวฟอร์ม · ตัดปี 2569 ออกเพราะปีเป็นค่าตัวแปรรอบปี F01) · ชื่อในคิวไม่เพี้ยน → ไม่ rename
- form_spec_check: ERROR 0 · 10 ช่อง · ตัวเลือก 1 (ไม่มี/มี) · ค่าคงที่ 2 (ปี · ถ้อยคำรับรอง) · ลายเซ็น 2 · anomalies 7 (ปี hardcode · "ฝ่ายกฎหมาย" ใต้กรอบผู้บังคับบัญชา · ติ๊กได้ 2 ช่อง · มีแต่ไม่กรอก · ข้อมูลลับ · แจ้งเปลี่ยนแปลงระหว่างปี · textbox)
- ฟอร์มเปล่า ไม่มีข้อมูลส่วนบุคคลจริง · ข้อมูลที่จะกรอกเป็นข้อมูลลับ (ความสัมพันธ์ครอบครัว/ธุรกิจ) → pdpa true ทุกช่องบุคคล · ตัวอย่างใช้ชื่อสมมติ
- 2026-10-10 05:40 · ขั้น 1 → done · FORM_SPEC 10 ช่อง ERROR 0 · PREBRIEF v2 สร้างจากฟอร์ม

## ขั้น 2 · gate (unattended — AI-DEFAULT 11 มติ + VALID 7)
- G1 ใบรับรอง/บันทึกเท่านั้น ไม่เปลี่ยนค่า ไม่ส่งต่อ (ทะเบียน COI/Vendor master ยังไม่มี · ผล "มี" ไม่บล็อกผู้ขายอัตโนมัติ)
- G2 กระดาษมีช่องผู้พิจารณา 1 ช่อง ไม่มี ☐ คำตัดสิน → dynamic 1 ขั้น role-line-manager (relative role · อยู่ในตาราง "ใช้จริงแต่ยังไม่อยู่ใน master") คำตัดสิน รับทราบ/ส่งกลับแก้ไข · คำ "ฝ่ายกฎหมาย" ใต้ช่องลงชื่อขัดหัวกรอบ → ไม่เพิ่มขั้นเอง เสนอ OQ (เพิ่ม role-compliance ที่ DOA กลาง) — TODO: DOA engine
- G3 ปี = ตัวแปรรอบปี (CoiDisclosureConfig.current_year) ไม่ hardcode 2569 · ถ้อยคำรับรองจาก config + snapshot · เลือก ไม่มี/มี 1 ตัว (บล็อก) · มี → รายละเอียดบังคับ · ติ๊กยืนยันความจริง (บล็อก) · ส่งซ้ำในปี = เตือน + ใบใหม่อ้างใบเดิม
- G4 ไม่มีแถวซ้ำ · G5 1:1 ไม่มีคำสะกดผิดชัดเจน · G6 ช่องในกรอบต่อขั้น · G7 ส่งกลับแก้ไข → ร่างเลขเดิม · G8 ข้อมูลลับ: admin = role-compliance (ไม่ใช่ role-mgr-pur) · CSV ไม่มีช่องรายละเอียด · G9 COI ออกเลขตอนบันทึกครั้งแรก · G10 แนบ ✓ CSV ✓
- 2026-10-10 05:41 · ขั้น 2 → done · 18 มติ (AI-DEFAULT 11 · VALID 7) พร้อมเริ่มทำ

## ขั้น 3 · declaration ร่าง
- doa: init เขียน on_reject: draft → validate BLOCK G5 (รับ back_to_draft|end) → แก้เป็น back_to_draft (ความหมายเดิม DEC-08) · label ขั้น = "ผู้บังคับบัญชา" + decision รับทราบ/ส่งกลับแก้ไข · notes OQ ฝ่ายกฎหมาย (role-compliance) — TODO: DOA engine · validate PASS (INFO role-line-manager relative role) · mock → COI.doa.mock.js
- ntf: ตัด coi_over_limit_approved (ไม่มีเกณฑ์/วงเงิน) · เติม coi_conflict_declared (ส่งใบที่ตอบ มี → role-compliance · in-app เท่านั้น ข้อความไม่มีรายละเอียดลับ) · coi_cancelled
- doccfg + mdoc ทำหลังขั้น 4 (ต้องใช้ print_config)
- 2026-10-10 05:42 · ขั้น 3 → done · doa PASS (1 ขั้น role-line-manager) · ntf PASS (doccfg/mdoc หลังขั้น 4)

## ขั้น 4 · แบบพิมพ์ Replica (R4–R8 เส้นประ · 1 หน้า)
- ต้นฉบับ 1 หน้า เส้นประ ไม่มีแถวซ้ำยาว → ออกแบบ 1 หน้า (ไม่ใช้ R10) · ฟอนต์ 10pt (หัว 14pt) · dense เมื่อรายละเอียด > 5 บรรทัด หรือ DOA > 4 ขั้น
- หัวเรื่องบรรทัด 2 = "ประจำปี {{doc.year}}" (ตัวแปรรอบปี) · ลงชื่อกลางหน้า + ช่องลงชื่อในกรอบ → แถวลงชื่อล่าง B6 (sign_rows: ผู้เปิดเผย + 1 ช่อง/ขั้น · คำตัดสิน by_role รับทราบ/ส่งกลับแก้ไข) · กรอบข้อคิดเห็นแสดงข้อคิดเห็นรายขั้น · footer มี "เอกสารลับ" + "แทนฉบับ …"
- data 5 สถานะ (ชื่อสมมติทั้งหมด): draft · approved (ไม่มี) · rejected (ส่งกลับแก้ไข) · long-12lines (รายละเอียด 12 บรรทัด + 3 ช่อง + แทนฉบับเดิม) · approved-doa6steps (4+3)
- parity_check: IDENTICAL 5/5
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py — playwright launch fail) → render_doc.py --strict + build_html.py ครบ 5 สถานะ (ไม่มี {{}} หลง · missing key 0) · ไม่มี PDF / _states_sheet.png · **จำนวนหน้ายังไม่ได้วัด** (ประมาณการ ≤ 1 หน้าทุกสถานะ) → ต้องรัน `--max-pages 1` รอบเต็ม
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ approved.pdf)
- ไฟล์ค้าง `print/out/_approved-doa6steps.body.html` จากรอบ render_states ที่ fail (ถูกเขียนทับด้วยรอบ render_doc แล้ว)
- print-spec `COI_print-spec.md` + `COI_data-contract.md` · template `FM-PUR-04_template.html`
- doccfg COI PASS (registry ACL/FEC/FLI/SMC/VEV ไม่ชน · J005 ใช้ PPO) · mdoc WARN (G04 taxonomy_def_id ว่าง · G09 doa pending · function_code F01 ชั่วคราว) · source=declaration (REQ-TMP-006 ไม่ใช่รูปแบบ REQ-YYYY-NNNN)
- doa validate --print-config: PASS (INFO role-line-manager relative role)
- 2026-10-10 05:44 · ขั้น 4 → done · 1 หน้า · parity 5/5 · [NO-BROWSER] ไม่มี PDF/compare/วัดหน้า · doccfg PASS · mdoc WARN

## ขั้น 5 · HTML Q-form (html-generator v9.4)
- ฐาน: kit กลาง + shell จาก feature ที่ผ่านด่านแล้ว (J004 · BASE-KIT ไม่แก้) เทียบ GOLDEN_SKELETON/U1–U28 · page CSS + app JS ของ COI เขียนใหม่ทั้งชุด (`_build/page.css` · `app1–3.js` · `build.py`) · ฝัง form.tpl.html + tpl_render.js + PDF_CSS (base+replica+profile ไม่รวม @font-face)
- โดเมน: wizard 3 ขั้น (Q2 #100F) · ขั้น 1 = ① ข้าพเจ้า/ตำแหน่ง/ปี จากระบบ + ถ้อยคำรับรองจาก COI_CONFIG ② ไม่มี/มี (track-card เลือก 1) + รายละเอียด (เฉพาะ มี · ≥10 ตัวอักษร) ③ ถ้อยคำท้าย + ติ๊กยืนยัน · การ์ดสรุปขวา (ผู้บังคับบัญชา · ปี · แทนฉบับ) · เตือนมีใบปีนี้แล้ว → ใบใหม่อ้างใบเดิม · เมนู "แจ้งเปลี่ยนแปลง" จากใบที่รับทราบแล้ว
- DOA: MOCK_DOA_RESOLVED 1 ขั้น role-line-manager (รับทราบ/ส่งกลับแก้ไข) · slot picker · ผู้ส่งไม่อยู่ในรายชื่อ — TODO: DOA engine · ข้อคิดเห็นของผู้บังคับบัญชา = note ในขั้น → พิมพ์ในกรอบ
- สิทธิ์ (เอกสารลับ): admin = role-compliance (E07) · ผู้จัดการฝ่ายจัดซื้อเห็นเฉพาะใบที่ตนพิจารณา · CSV ไม่มีรายละเอียด · PDF genPdf ตรวจ canSee
- audit.sh: FAIL 0 · WARN 3 (มาจาก BASE-KIT เดิม: #21 icon ใน kit · #40 .uc-email · font-size px ใน kit) · prune_css ตัด 0 · audit ซ้ำ FAIL 0
- [NO-BROWSER] ข้าม e2e_standard.py (pyshim: ไม่พบ browser) · ข้าม render-check.py → ทดแทนด้วย smoke test jsdom (reports/smoke_jsdom.js → smoke_jsdom_report.txt) 39/39 PASS: สิทธิ์ G8 4 persona (owner/ผู้บังคับบัญชา/ผจก.จัดซื้อ/compliance) · ทุก tab ทุกใบไม่มี error · PDF 1 หน้าไม่มี {{}} · ปีตัวแปร (2568/2569) · validation (ไม่เลือก · ไม่ยืนยัน · มีแต่รายละเอียดสั้น · ไม่มี → ล้างรายละเอียด) · ส่ง → แจ้ง coi_conflict_declared · ส่งกลับแก้ไข → ร่างเลขเดิม → แก้ → รับทราบ → ใบเดิมถูกแทนที่ · DOA push 2 ขั้น (ฝ่ายกฎหมาย) · CSV ไม่มีรายละเอียด · ยกเลิก · S.sim · DOC.active
- U1–U28: U1✓ no-scorecard (นับใน ph-count) · U2✓ · U3✓ · U4✓ · U5✓ kebab ⋮ · U6✓ pager 25 · U7✓ CSV ที่ head · U8✓ 920/1290 · U9✓ เหตุผลบังคับ · U10✓ pill · U11✓ · U12✓ lucide mono · U13✓ block ลายเซ็นกลาง · U14✓ Q2 wizard 3 ขั้น (#100F) · U15✓ edit = wizard เดียวกัน · U16 n/a (ไม่มีลบ ใช้ยกเลิก+เหตุผล) · U17✓ person icon · U18✓ 1 cell 1 บรรทัด · U19✓ header sub 2 fact (ชื่อ · ปี) · U20✓ segmented (ทั้งหมด/รอฉันพิจารณา) · U21✓ (page CSS ใช้ --fs-*) · U22✓ · U23✓ empty panel (ยังไม่มีข้อคิดเห็น) · U24✓ search-select · U25✓ backdrop onmousedown · U26–U28 n/a (CoiDisclosureConfig เสนอเป็นหน้า config ใน report)
- 2026-10-10 05:54 · ขั้น 5 → done · audit FAIL 0 · [NO-BROWSER] e2e ข้าม → jsdom smoke 39/39 · U1–U28 ✓
- 2026-10-10 05:54 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-006.md (+ .docx md_to_docx) · Prebrief Mode · AI Review C01–C23/PE01–05 → APPROVED (C22 ตัวชี้วัด → OQ-01 ตามกติกา ห้ามแต่งตัวเลข) · Data Classification Confidential
- FRD_F-TMP-006_Pack 00–07 + INDEX · 07 §7.0 คัดตาราง DEC จาก DECISIONS.lock (18) · frd_lint Section N: รอบแรก WARN 1 (N2 reviewer_comment หาไม่เจอใน 04) → เติมคีย์ใน 04 approval_chain[].comment → BLOCK 0 · WARN 0 · PASS 14
- declaration --final: DOCCFG PASS (registry ACL/FEC/FLI/SMC/VEV ไม่ชน · COI · frd_ref FN-03/FN-06) · NTF PASS (frd_ref FN-05/08/10) · DOA PASS (INFO role-line-manager relative role · frd_ref) · MDOC WARN (G04 taxonomy_def_id ว่าง · G09 doa pending · function_code F01 ชั่วคราว) → คัดลง FRD_F-TMP-006_Pack/declarations/
- 2026-10-10 06:01 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · declaration --final BLOCK 0 (mdoc WARN)

## ขั้น 8 · UI Brief → test case AI → UAT
- html-ui-brief: extract_anchors (vars 47 · z 21 · routes 5 · toast 11) → UI_BRIEF_F-TMP-006.md (สร้างด้วย _build/make_ui_brief.py จาก inventory + อ่านโค้ด) · brief_check PASS (FAIL 0 · WARN 0 · anchor fn 71/class 29/id 25 มีจริง)
- ai-testcase-md-generator: testcases-F-TMP-006.md 50 เคส / 89 step · tc_lint ERROR 0 (รอบแรก ERROR 1: TC-XT04 step ไม่ขึ้นต้น verb → แก้) · Ledger (AC 15/15 · BR 20/20 + BR-DOA-05 ไม่ใช้ · VR 6/6 · EC 9/12 (EC-07 แก้ DOA กลาง · EC-10 config เปลี่ยน · EC-12 PDF ยาวดูที่ print/long-12lines) · error 13/13 · permission 15/15 · XT 4/4 · DEC 18/18)
- [NO-BROWSER] ข้าม verify_anchors.py (playwright) — anchor ตรวจด้วย jsdom smoke + อ่านโค้ด
- qa-friendly: cases.json Lite 43 เคส · lite_audit หายเงียบ 0 (drop ledger 7) --stamp · [NO-BROWSER] ข้าม capture.py → shots_b64.json ว่าง ({}) · build testcase-F-TMP-006.html
- 2026-10-10 06:06 · ขั้น 8 → done · brief_check PASS · tc_lint ERROR 0 (50 เคส) · lite_audit หายเงียบ 0 · [NO-BROWSER] verify_anchors/capture ข้าม
