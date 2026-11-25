# RUN_LOG — F-TMP-006 FM-IVM-04 แบบฟอร์มห้องข้อมูล มาตรฐานชื่อไฟล์ และทะเบียนควบคุมเอกสาร (REQ-TMP-006)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: to_image.py (LibreOffice → PDF → pypdfium2) ได้ page-1.png + content.html · ถ้อยคำยึด openpyxl/content.html · ตำแหน่ง/เส้นยึดภาพ
- FORM_SPEC: 37 ช่อง · แถวซ้ำ 4 (โฟลเดอร์ 8 · ทะเบียนเอกสาร 5 · การเปลี่ยนแปลง 5 · สิทธิการเข้าถึง 5) · ตัวเลือก 5 (จาก data validation D13:D20/E44:E48 · F31:F35 · I37:I41 · J44:J48) · สูตร 0 · ค่าคงที่ 6 (มาตรฐานชื่อไฟล์ 5 + โฟลเดอร์มาตรฐาน 8) · ลายเซ็น 3 · anomalies 8 · form_spec_check ERROR 0 WARN 0
- ช่องเพิ่ม 1 ช่อง: F01 ชื่อโครงการ / ธุรกรรม — กระดาษไม่มีช่องระบุโครงการ (anomaly) · ยกเว้น G5 แบบ AI-DEFAULT รอลูกค้ายืนยัน
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC (--req REQ-TMP-006) · รอบแรกลืม --req ได้ REQ-XXXX → ย้ายไฟล์ impact เป็น _tmp/*.bak
- ไฟล์ลูกค้าเป็นฟอร์มเปล่า ไม่มีข้อมูลตัวอย่าง/ข้อมูลส่วนบุคคล (ชื่อโฟลเดอร์ 8 แถว = ค่ามาตรฐาน ไม่ใช่ข้อมูลบุคคล)
- 2026-10-11 00:58 · ขั้น 1 → done · FORM_SPEC 37 ช่อง ERROR 0 · PREBRIEF v2

## ขั้น 2 — มติ AI (unattended · ตาม 4_knowledge/governance/unattended-policy.md)
- G1: ทะเบียนห้องข้อมูล/ควบคุมเอกสาร ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อ · ไม่สร้างสิทธิจริงในไดรฟ์ (เป็นทะเบียน) · ชื่อโครงการกรอกเอง (FM-IVM-01 ยังไม่ลิงก์)
- G2: dynamic 2 ขั้นตามช่องลงชื่อ: ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน → role-line-manager) · ผู้อนุมัติ/รับทราบ (รอง กก.ผจก./กก.ผจก. → role-gm) · ไม่มีวงเงิน · ⚠ role บนกระดาษไม่มีใน doa-roles-contract
- G3: มาตรฐานชื่อไฟล์ + โฟลเดอร์มาตรฐาน 8 แถว อ่านจาก config · รันรหัส D-/CH-/ลำดับ · ฉบับ Vnn/Final บล็อก · สิทธิ/การเปลี่ยนแปลง กฎวันที่ บล็อก · ไม่ตรงมาตรฐานเตือน
- G4: ไม่จำกัดแถว · PDF ขั้นต่ำ 8/5/5/5 · G5: 1:1 + ช่องเพิ่ม ชื่อโครงการ / ธุรกรรม · G6: แถวล่างต่อขั้น ข้อความในระบบ
- G7: ไม่อนุมัติ → กลับร่างเลขเดิม · ยกเลิก owner+admin ร่าง/รออนุมัติ เหตุผลบังคับ · G8: เจ้าของ/ผู้อนุมัติหลังส่ง/admin ฝ่ายเห็นทั้งหมด
- G9: เอกสารภายใน ออกเลขตอนบันทึกครั้งแรก · รหัส IVMD (IVM + D = ฟอร์มลำดับ 04 ตามแบบแผนชุดนี้)
- G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock = พร้อมเริ่มทำ · 22 มติ (AI-DEFAULT 14 · VALID 8)
- 2026-10-11 00:58 · ขั้น 2 → done · DECISIONS.lock พร้อม · 22 มติ AI-DEFAULT 14

## ขั้น 3 — หมายเหตุ
- DOA: doa_tool init เขียน on_reject: draft (validate BLOCK G5) → แก้เป็น back_to_draft (ตรง DEC-11) · เติมคำตัดสินขั้น 2 (อนุมัติ/ไม่อนุมัติ) · role_notes · TODO: DOA engine · validate PASS · mock → IVMD.doa.mock.js
- ⚠ role บนกระดาษไม่มีใน doa-roles-contract: "ผู้จัดการฝ่ายบริหารการลงทุน" (ใช้ role-line-manager) · "รองกรรมการผู้จัดการ/กรรมการผู้จัดการ" (ใช้ role-gm) · module investment ไม่อยู่ใน Module Registry
- NTF: ตัด ivmd_over_limit_approved (เกณฑ์เตือนแสดงขณะกรอก) · เพิ่ม ivmd_register_approved (แจ้งผู้จัดทำ + admin role ให้ไปตั้งสิทธิในไดรฟ์จริง) · PASS
- 2026-10-11 00:59 · ขั้น 3 → done · DOA PASS (2 ขั้น dynamic) · NTF PASS (2 event) · doccfg/mdoc หลังขั้น 4

## ขั้น 3–4 — หมายเหตุ
- DOCCFG IVMD PASS (--registry ไม่ชน ACL/IVMA/IVMJ/IVMK/IVMB) · MDOC WARN (G04 taxonomy รออนุมัติ · G09 doa pending) · function_code F01 ค่าชั่วคราว · DOA validate --print-config PASS
- แบบพิมพ์: R9 ตารางกรอบ 10 คอลัมน์ · 23 แถวซ้ำ (8+5+5+5) + มาตรฐานชื่อไฟล์ > ~20 → ออกแบบ 2 หน้าตาม R10 (ตัดหน้าก่อนตารางการเปลี่ยนแปลง CH- · หัว "(ต่อ)" · หัวย่อหน้า 2 · thead ซ้ำ · มีต่อหน้าถัดไป · หน้า 1/2, 2/2) · ฟอนต์ 8pt
- data 5 สถานะ (draft · approved · rejected · long-10folders-8docs-7changes-8access · approved-doa6steps) ข้อมูลสมมติทั้งหมด · parity IDENTICAL 5/5 · render_doc --strict + build_html ไม่มี {{}} หลง · print-spec + template.html (fonts ฝัง)
- [NO-BROWSER] ข้าม render_states.py (เรียก render_pdf.py) — ยังไม่ได้ PDF/จำนวนหน้า/_states_sheet.png
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ PDF สถานะ approved)
- 2026-10-11 01:02 · ขั้น 4 → done · Replica 2 หน้า R10 · parity 5/5 · NO-BROWSER: ยังไม่ render PDF/compare

## ขั้น 5 — HTML Q-form
- ฐาน: references/form-archetype/_SOURCE_form-request-reference.html (เปลือก/CSS/BASE-KIT) + app script ใหม่ของ IVMD (_build/app1–5.js · build_feature.py) + be-datepicker (Rule #114) · DOC_TPL = print/form.tpl.html · tpl_render.js วางตรง
- เทียบ GOLDEN_SKELETON v9.4 + U1–U28 ก่อน build: ไม่มี stat cards (ตัวเลขเป็น badge ใน ph-sub) · kebab ⋮ · คน = วงกลม icon · pagination 25 + page-size · backdrop onmousedown · drawer header lean (sub = โฟลเดอร์/เอกสาร/สิทธิใช้งาน 1 บรรทัด) · ไม่มี page tabs (ชุดเดียว)
- wizard 4 ขั้น (ห้องข้อมูลและมาตรฐานชื่อไฟล์ › ทะเบียนเอกสาร (+การเปลี่ยนแปลง) › สิทธิการเข้าถึงและเอกสารแนบ › ตรวจสอบและยืนยัน) · แถวซ้ำ 4 กลุ่ม → ตารางกรอก (Rule #107) · ใบใหม่ตั้งต้น 8 โฟลเดอร์มาตรฐาน · มาตรฐานชื่อไฟล์อ่านอย่างเดียว · ชื่อไฟล์ตามมาตรฐานแสดงสดใต้ชื่อเอกสาร
- U1✓ U2✓ U3✓ U4✓ U5✓ U6✓ U7✓ U8✓ U9✓ U10✓ U11✓ U12✓ U13✓ U14✓(wizard wide 4 ขั้น) U15✓ U16 n/a(ไม่มีลบ ใช้ยกเลิก) U17✓ U18✓ U19✓ U20 n/a(ชุดเดียว) U21✓ U22✓ U23✓ U24✓ U25✓ U26–U28 n/a(ไม่มีหน้าตั้งค่า)
- บั๊กใบก่อน (modal อนุมัติ/ส่งกลับพังตอนกำลังปิดหลังตัดสิน): render() วาด modal เฉพาะ state.modal.open · renderModal คืน '' เมื่อใบไม่มีขั้นรอพิจารณา · confirm* กันไม่มี curStep · open* เช็กสิทธิ — ทดสอบด้วย timer จริง (jsdom) + คิว timer (stub)
- audit.sh FAIL 0 · WARN 4 (Rule #21 ใน BASE-KIT · .uc-email ใน kit · token font-size ใน kit · #100F step เอกสารแนบ — G10 attachments=true คงไว้) · self_audit PASS (แก้ hint ยาว 3) · prune_css ตัด 75 rule แล้ว audit/self_audit ซ้ำผ่าน · node --check ผ่าน
- smoke stub (_build/smoke.js · timer แบบคิว): 46/46 · jsdom ทั้งไฟล์ (_build/jsdom_smoke.js · timer จริง): 26/26 ไม่มี error — สิทธิ์ G8 · validate (ฉบับ Vnn/Final · นำไปใช้แล้วต้องมีวันที่มีผล · วันที่ยกเลิกสิทธิ) · เตือน (ไม่ใช่ Final · วันที่มีผลก่อนวันที่) · ออกเลข IVMD · ส่ง/ส่งกลับเป็นร่างเลขเดิม/ส่งใหม่/อนุมัติ 2 ขั้น · ยกเลิก · ทำซ้ำ · PDF เติมแถว 8/5/5/5 · DOA 6 ขั้น = 7 ช่องลงนาม · DOC.active=false
- parity PDF ใน prototype: data จาก docPrintData(R1) → render_doc.py (Python) = tplRender (JS) IDENTICAL
- [NO-BROWSER] ข้าม e2e_standard.py · [NO-BROWSER] ข้าม render-check.py
- 2026-10-11 01:13 · ขั้น 5 → done · audit FAIL0 · self_audit PASS · smoke 46/46 · jsdom 26/26 · NO-BROWSER ข้าม e2e
- 2026-10-11 01:13 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-006.md (+ .docx md_to_docx) · brd-generator-full v2.3 Prebrief Mode · Quality Gate C1–C20 → APPROVED · §2.4 = DECISIONS.lock 22 DEC · OQ-01..08
- FRD_F-TMP-006_Pack 00–07 + INDEX (Input Mode 0 · FULL · API 12 · FN 12 · BR 20 · VR 12 · AC 16) · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 15 (N3 ค่าคงที่ไม่ hardcode)
- declaration --final: DOCCFG IVMD PASS (--registry · frd_ref FN-04/FN-06) · NTF PASS (frd_ref FN-06/08/10) · DOA PASS (+print_config · frd_ref FN-05/06/07) · MDOC WARN (G04 taxonomy รอ · G09 doa pending) → สำเนาใน FRD_Pack/declarations
- 2026-10-11 01:19 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK0 WARN0 · decl final PASS

## ขั้น 8 — UI Brief → test case → UAT
- UI_BRIEF_F-TMP-006.md (AS-BUILT จาก inventory · _build/build_uibrief.py) · brief_check PASS · FAIL 0 · WARN 0
- testcases-F-TMP-006.md 43 เคส / 253 step · tc_lint ERROR 0 · cases.json (Lite 38 เคส) + QA_AUDIT drop ledger 5 · lite_audit หายเงียบ 0 (--stamp) · testcase-F-TMP-006.html (build.py · shots ว่าง)
- เคสครอบจุดบั๊กใบก่อน (modal ปิดหลังตัดสิน): TC-A01 · TC-A02 · TC-R01
- [NO-BROWSER] ข้าม verify_anchors.py · [NO-BROWSER] ข้าม capture.py (เอกสาร UAT build แบบไม่มีภาพ)
- 2026-10-11 01:23 · ขั้น 8 → done · brief_check PASS · tc_lint 0 · lite_audit 0 · NO-BROWSER: ข้าม verify_anchors/capture
