# RUN_LOG — F-TMP-004 FM-IVM-02 แบบฟอร์มตารางติดตามงานและแผนฐาน (REQ-TMP-004)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: to_image.py (LibreOffice → PDF → pypdfium2) ได้ page-1.png + content.html · ถ้อยคำยึด openpyxl/content.html · ตำแหน่ง/เส้นยึดภาพ
- FORM_SPEC: 19 ช่อง · แถวซ้ำ 2 (หมุดหมาย 8 แถว · รายการติดตามงาน 18 แถว) · ตัวเลือก 2 (สถานะ 5 ค่าจาก data validation H13:H20 / G24:G41) · สูตร 1 (ความคลาดเคลื่อน = วันที่ปรับปรุง − วันที่ตามแผนฐาน ตรง I13:I20) · ลายเซ็น 3 · anomalies 6 · form_spec_check ERROR 0
- ช่องเพิ่ม 1 ช่อง: F01 ชื่อโครงการ / ธุรกรรม — กระดาษไม่มีช่องระบุโครงการ (anomaly) · ยกเว้น G5 แบบ AI-DEFAULT รอลูกค้ายืนยัน
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC · impact_summary.py รับ REQ-TMP-004 ได้ (regex สกิลแก้แล้ว)
- ไฟล์ลูกค้าเป็นฟอร์มเปล่า ไม่มีข้อมูลตัวอย่าง/ข้อมูลส่วนบุคคล
- 2026-10-11 00:29 · ขั้น 1 → done · FORM_SPEC 19 ช่อง ERROR 0 · PREBRIEF v2

## ขั้น 2 — มติ AI (unattended · ตาม 4_knowledge/governance/unattended-policy.md)
- G1: ตารางติดตามงาน/แผนฐาน ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อ · ชื่อโครงการกรอกเอง (FM-IVM-01 ยังไม่ลิงก์)
- G2: dynamic 2 ขั้นตามช่องลงชื่อ: ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน → role-line-manager) · ผู้อนุมัติ/รับทราบ (รอง กก.ผจก./กก.ผจก. → role-gm) · ไม่มีวงเงิน · ⚠ role บนกระดาษไม่มีใน doa-roles-contract
- G3: สูตร 1 (ความคลาดเคลื่อน วัน) คำนวณอัตโนมัติ · ร้อยละ 0–100 บล็อก · แล้วเสร็จ<100 เตือน · ช้ากว่าแผนเตือน · ≥1 แถวต่อตารางก่อนส่ง
- G4: ไม่จำกัดแถว · PDF ขั้นต่ำ 8 / 18 แถว · G5: 1:1 + ช่องเพิ่ม ชื่อโครงการ / ธุรกรรม (กระดาษไม่มีช่องระบุโครงการ) · G6: แถวล่างต่อขั้น ข้อความในระบบ
- G7: ไม่อนุมัติ → กลับร่างเลขเดิม · ยกเลิก owner+admin ร่าง/รออนุมัติ เหตุผลบังคับ · G8: เจ้าของ/ผู้อนุมัติหลังส่ง/admin ฝ่ายเห็นทั้งหมด
- G9: เอกสารภายใน ออกเลขตอนบันทึกครั้งแรก · รหัส IVMB (IVM + B = ฟอร์มลำดับ 02 ตามแบบแผนชุดนี้)
- G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock = พร้อมเริ่มทำ · 18 มติ (AI-DEFAULT 12 · VALID 6)
- 2026-10-11 00:30 · ขั้น 2 → done · DECISIONS.lock พร้อม · 18 มติ AI-DEFAULT 12
- 2026-10-11 00:30 · ขั้น 3 → done · DOA PASS (2 ขั้น dynamic) · NTF PASS (2 event) · doccfg/mdoc หลังขั้น 4

## ขั้น 3–4 — หมายเหตุ
- DOA: doa_tool init เขียน on_reject: draft → แก้เป็น back_to_draft (ตรง DEC-09) · เติมคำตัดสินขั้น 2 (อนุมัติ/ไม่อนุมัติ) · validate PASS (+print_config PASS) · mock → IVMB.doa.mock.js
- ⚠ role บนกระดาษไม่มีใน doa-roles-contract: "ผู้จัดการฝ่ายบริหารการลงทุน" (ใช้ role-line-manager) · "รองกรรมการผู้จัดการ/กรรมการผู้จัดการ" (ใช้ role-gm) · module investment ไม่อยู่ใน Module Registry
- NTF: ตัด ivmb_over_limit_approved (เกณฑ์เตือนแสดงขณะกรอก) · เพิ่ม ivmb_baseline_approved (แจ้งผู้รับผิดชอบหมุดหมาย/งาน) · PASS
- DOCCFG IVMB PASS (--registry ไม่ชน IVMA/IVMJ) · MDOC WARN (G04 taxonomy รออนุมัติ · G09 doa pending) · function_code F01 ค่าชั่วคราว
- แบบพิมพ์: R9 ตารางกรอบ 10 คอลัมน์ · 26 แถวซ้ำ (8+18) > ~20 → ออกแบบ 2 หน้าตาม R10 (ตัดหน้าก่อน "รายการติดตามงาน" · หัวย่อหน้า 2 · thead ซ้ำ · มีต่อหน้าถัดไป · หน้า 1/2, 2/2) · ฟอนต์ 8pt
- data 5 สถานะ (draft · approved · rejected · long-12milestones-18tasks · approved-doa6steps) ข้อมูลสมมติทั้งหมด · parity IDENTICAL 5/5 · render_doc --strict + build_html ไม่มี {{}} หลง
- [NO-BROWSER] ข้าม render_states.py (เรียก render_pdf.py) — ยังไม่ได้ PDF/จำนวนหน้า/_states_sheet.png
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ PDF สถานะ approved)
- 2026-10-11 00:33 · ขั้น 4 → done · Replica 2 หน้า R10 · parity 5/5 · NO-BROWSER: ยังไม่ render PDF/compare

## ขั้น 5 — HTML Q-form
- ฐาน: references/form-archetype/_SOURCE_form-request-reference.html (เปลือก/CSS/BASE-KIT) + app script ใหม่ของ IVMB (_build/app1–5.js · build_feature.py) + be-datepicker (Rule #114) · DOC_TPL = print/form.tpl.html · tpl_render.js วางตรง
- เทียบ GOLDEN_SKELETON v9.4 + U1–U28 ก่อน build: ไม่มี stat cards (ตัวเลขเป็น badge ใน ph-sub) · kebab ⋮ · คน = วงกลม icon · pagination 25 + page-size · backdrop onmousedown · drawer header lean (sub = ความคืบหน้าเฉลี่ย/ช้ากว่าแผน) · ไม่มี page tabs (ชุดเดียว)
- แถวซ้ำ 10 คอลัมน์ → ตารางกรอก (Rule #107 > 4 ช่อง) · วันที่ = bedateHTML ต่อช่อง · สถานะ = select 5 ค่า · ความคลาดเคลื่อนคำนวณสด · ปรับปรุงล่าสุดระบบใส่
- U1✓ U2✓ U3✓ U4✓ U5✓ U6✓ U7✓ U8✓ U9✓ U10✓ U11✓ U12✓ U13✓ U14✓(wizard wide 3 ขั้น) U15✓ U16 n/a(ไม่มีลบ ใช้ยกเลิก) U17✓ U18✓ U19✓ U20 n/a(ชุดเดียว) U21✓ U22✓ U23✓ U24✓ U25✓ U26–U28 n/a(ไม่มีหน้าตั้งค่า)
- audit.sh FAIL 0 · WARN 3 (เท่ากับ canonical: Rule #21 ใน BASE-KIT · .uc-email ใน kit · token font-size) · self_audit PASS (แก้ hint ยาว 3 + missing id 1 แล้ว) · prune_css ตัด 74 rule แล้ว audit/self_audit ซ้ำผ่าน · node --check ผ่าน
- smoke test แบบไม่มี browser (node + DOM stub · _build/smoke.js): 36/36 — สิทธิ์ G8 · validate (ร้อยละ 0–100 บล็อก · แล้วเสร็จ<100 เตือน) · ออกเลข · ส่ง/ส่งกลับเป็นร่างเลขเดิม/ส่งใหม่/อนุมัติ 2 ขั้น · ยกเลิก · PDF เติมแถว 8/18 · DOA 6 ขั้น = 7 ช่องลงนาม · DOC.active=false
- parity PDF ใน prototype: data จาก docPrintData(R1) → render_doc.py (Python) = tplRender (JS) IDENTICAL
- [NO-BROWSER] ข้าม e2e_standard.py · [NO-BROWSER] ข้าม render-check.py
- 2026-10-11 00:39 · ขั้น 5 → done · audit FAIL0 · self_audit PASS · smoke 36/36 · NO-BROWSER ข้าม e2e
- 2026-10-11 00:39 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-004.md (+ .docx md_to_docx) · brd-generator-full v2.3 Prebrief Mode · Quality Gate C1–C20 → APPROVED · §2.4 = DECISIONS.lock 18 DEC · OQ-01..07
- FRD_F-TMP-004_Pack 00–07 + INDEX (Input Mode 0 · FULL) · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 12
- declaration --final: DOCCFG IVMB PASS (--registry · frd_ref FN-04/FN-06) · NTF PASS (frd_ref FN-06/08/10) · DOA PASS (+print_config) · MDOC WARN (G04 taxonomy รอ · G09 doa pending) → สำเนาใน FRD_Pack/declarations
- หมายเหตุ: ผู้รับผิดชอบในแถว = ข้อความ (FORM_SPEC F04/F13 type text) → รัน form_spec_check · prebrief_v2 · decisions_lock · tag ใหม่หลังแก้ (ผลเท่าเดิม 18 มติ AI-DEFAULT 12)
- 2026-10-11 00:44 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK0 WARN0 · decl final PASS

## ขั้น 8 — UI Brief → test case → UAT
- UI_BRIEF_F-TMP-004.md (AS-BUILT จาก inventory · _build/build_uibrief.py) · brief_check PASS · FAIL 0 · WARN 0
- seed ปรับ (R3/R9 เหลือ 1 หมุดหมาย ให้มีตาราง "ตามแผน" ไว้ทดสอบตัวกรอง) → rebuild feature.html + prune + audit FAIL 0 + self_audit PASS + smoke 36/36 + parity PDF IDENTICAL ซ้ำ
- testcases-F-TMP-004.md 39 เคส / 178 step · tc_lint ERROR 0 · cases.json (Lite 34 เคส) + QA_AUDIT drop ledger 5 · lite_audit หายเงียบ 0 (--stamp) · testcase-F-TMP-004.html (build.py · shots ว่าง)
- [NO-BROWSER] ข้าม verify_anchors.py · [NO-BROWSER] ข้าม capture.py (เอกสาร UAT build แบบไม่มีภาพ)
- 2026-10-11 00:49 · ขั้น 8 → done · brief_check PASS · tc_lint 0 · lite_audit 0 · NO-BROWSER: ข้าม verify_anchors/capture
