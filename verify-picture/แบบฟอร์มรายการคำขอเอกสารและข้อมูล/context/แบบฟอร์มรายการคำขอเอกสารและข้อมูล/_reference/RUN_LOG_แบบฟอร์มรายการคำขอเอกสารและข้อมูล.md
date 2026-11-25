# RUN_LOG — F-TMP-007 FM-IVM-05 แบบฟอร์มรายการคำขอเอกสารและข้อมูล (REQ-TMP-007)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: to_image.py (LibreOffice → PDF → pypdfium2) ได้ page-1.png + content.html · ถ้อยคำยึด openpyxl/content.html · ตำแหน่ง/เส้นยึดภาพ
- FORM_SPEC: 11 ช่อง · แถวซ้ำ 1 (รายการคำขอ 20 แถว DR-001…DR-020) · ตัวเลือก 1 (สถานะ 6 ค่า จาก data validation G13:G32) · สูตร 0 · ค่าคงที่ 2 · ลายเซ็น 3 · anomalies 7 · form_spec_check ERROR 0 WARN 0
- ช่องเพิ่ม 1 ช่อง: F01 ชื่อโครงการ / ธุรกรรม — กระดาษไม่มีช่องระบุโครงการ (anomaly) · ยกเว้น G5 แบบ AI-DEFAULT รอลูกค้ายืนยัน (แนวเดียวกับ FM-IVM-04)
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC (--req REQ-TMP-007) · impact_summary ฉบับร่าง
- ไฟล์ลูกค้าเป็นฟอร์มเปล่า ไม่มีข้อมูลตัวอย่าง/ข้อมูลส่วนบุคคล
- ชื่อในคิวมี FM-IVM-05 นำหน้า → dm.sh rename เป็นชื่อจากหัวฟอร์ม
- 2026-10-11 01:27 · ขั้น 1 → done · FORM_SPEC 11 ช่อง ERROR 0 · PREBRIEF v2

## ขั้น 2 — มติ AI (unattended · ตาม 4_knowledge/governance/unattended-policy.md)
- G1: ทะเบียนคำขอเอกสาร/ข้อมูล ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อ · ไม่ส่งคำขอจริงไปผู้ถูกขอข้อมูล (ทะเบียนติดตาม) · ชื่อโครงการกรอกเอง (FM-IVM-01 ยังไม่ลิงก์)
- G2: dynamic 2 ขั้นตามช่องลงชื่อ: ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน → role-line-manager) · ผู้อนุมัติ/รับทราบ (รอง กก.ผจก./กก.ผจก. → role-gm) · ไม่มีวงเงิน · ⚠ role บนกระดาษไม่มีใน doa-roles-contract
- G3: รหัส DR-nnn + หมายเหตุการใช้งาน อ่านจาก config · สถานะ↔วันที่ (ขอแล้ว+ต้องมีวันที่ขอ · ได้รับครบ+ต้องมีวันที่ได้รับ) บล็อก · ลำดับวันที่บล็อก · ไม่เกี่ยวข้อง/ยกเลิก ต้องมีหมายเหตุ · เกินกำหนดเตือน · ลิงก์มีรหัสผ่านเตือน
- G4: ไม่จำกัดแถว · PDF ขั้นต่ำ 20 แถว · G5: 1:1 + ช่องเพิ่ม ชื่อโครงการ / ธุรกรรม · G6: แถวล่างต่อขั้น ข้อความในระบบ
- G7: ไม่อนุมัติ → กลับร่างเลขเดิม · ยกเลิก owner+admin ร่าง/รออนุมัติ เหตุผลบังคับ · G8: เจ้าของ/ผู้อนุมัติหลังส่ง/admin ฝ่ายเห็นทั้งหมด
- G9: เอกสารภายใน ออกเลขตอนบันทึกครั้งแรก · รหัส IVME (IVM + E = ฟอร์มลำดับ 05 ตามแบบแผนชุดนี้)
- G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock = พร้อมเริ่มทำ · 18 มติ (AI-DEFAULT 11 · VALID 7)
- 2026-10-11 01:27 · ขั้น 2 → done · DECISIONS.lock พร้อม · 18 มติ AI-DEFAULT 11

## ขั้น 3 — หมายเหตุ
- DOA: doa_tool init เขียน on_reject: draft → แก้เป็น back_to_draft (ตรง DEC-08) · เติมคำตัดสินขั้น 2 (อนุมัติ/ไม่อนุมัติ) · role_notes · TODO: DOA engine · validate PASS · mock → IVME.doa.mock.js
- ⚠ role บนกระดาษไม่มีใน doa-roles-contract: "ผู้จัดการฝ่ายบริหารการลงทุน" (ใช้ role-line-manager) · "รองกรรมการผู้จัดการ/กรรมการผู้จัดการ" (ใช้ role-gm) · module investment ไม่อยู่ใน Module Registry
- NTF: ตัด ivme_over_limit_approved (เกณฑ์เตือนแสดงขณะกรอก) · เพิ่ม ivme_request_list_approved (แจ้งผู้จัดทำ + admin role ให้เริ่มส่งคำขอนอกระบบ) · PASS
- 2026-10-11 01:28 · ขั้น 3 → done · DOA PASS (2 ขั้น dynamic) · NTF PASS (2 event) · doccfg/mdoc หลังขั้น 4

## ขั้น 4 — แบบพิมพ์ Replica
- R9 ตารางกรอบ 10 คอลัมน์ · รายการคำขอขั้นต่ำ 20 แถว (ต้นฉบับ DR-001…DR-020) > A4 พร้อมบล็อกลงชื่อ → ออกแบบ 2 หน้าตาม R10 (ตัดหน้าก่อน "การตรวจทาน / อนุมัติ" · หัว "(ต่อ)" + เลขที่ · thead ซ้ำ · มีต่อหน้าถัดไป · หน้า 1/2, 2/2) · ฟอนต์ 8pt (ไม่ต่ำกว่า)
- data 5 สถานะ (draft · approved · rejected · long-28requests · approved-doa6steps) ข้อมูลสมมติทั้งหมด · parity IDENTICAL 5/5 · render_doc ไม่มี {{}} หลง · ไม่มี key ขาด · DOA 6 ขั้น = 7 ช่อง (4+3)
- doa validate --print-config PASS · DOCCFG IVME init + brief --registry PASS (ไม่ชน IVMA/IVMB/IVMC/IVMD/IVMJ/IVMK) · MDOC WARN (G04 taxonomy รออนุมัติ · G09 doa pending · function_code F01 ค่าชั่วคราว)
- [NO-BROWSER] ข้าม render_states.py (เรียก render_pdf.py) — ยังไม่ได้ PDF/จำนวนหน้า/_states_sheet.png
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ PDF สถานะ approved)
- 2026-10-11 07:34 · ขั้น 4 → done · Replica 2 หน้า R10 · parity 5/5 · DOCCFG PASS · NO-BROWSER: ยังไม่ render PDF/compare

## ขั้น 5 — HTML Q-form
- ฐาน: references/form-archetype/_SOURCE_form-request-reference.html (เปลือก/CSS/BASE-KIT) + app script ใหม่ของ IVME (_build/app1–5.js · build_feature.py) + be-datepicker (Rule #114) · DOC_TPL = print/form.tpl.html · tpl_render.js วางตรง
- เทียบ GOLDEN_SKELETON v9.4 + U1–U28 ก่อน build: ไม่มี stat cards (ตัวเลขเป็น badge ใน ph-sub) · kebab ⋮ · คน = วงกลม icon · pagination 25 + page-size · backdrop onmousedown · drawer header lean (sub = คำขอ n รายการ · ได้รับครบ n) · ไม่มี page tabs (ชุดเดียว)
- wizard 3 ขั้น #100F (รายการคำขอเอกสารและข้อมูล › เอกสารแนบ › ตรวจสอบและยืนยัน) · แถวซ้ำ 10 คอลัมน์ → ตารางกรอก (Rule #107) · ใบใหม่ตั้งต้น 1 แถว DR-001 · รหัสคำขอรันต่อ ไม่รันใหม่เมื่อลบแถว · หมายเหตุการใช้งานอ่านอย่างเดียวจาก DocRequestPolicy · ไม่มีปุ่มทำซ้ำ (DEC-11 / G10)
- กติกา DEC-14/15/16/17 บล็อกในแถว (สถานะ↔วันที่ · ลำดับวันที่ · หมายเหตุเมื่อปิดรายการ · ลิงก์ path/URL) · เตือน: เกินกำหนด · คำว่ารหัสผ่าน · ส่งได้เมื่อมีคำขอ ≥1 (DEC-04)
- U1✓ U2✓ U3✓ U4✓ U5✓ U6✓ U7✓ U8✓ U9✓ U10✓ U11✓ U12✓ U13✓ U14✓(wizard wide 3 ขั้น) U15✓ U16 n/a(ไม่มีลบ ใช้ยกเลิก) U17✓ U18✓ U19✓ U20 n/a(ชุดเดียว) U21✓ U22✓ U23✓ U24✓ U25✓ U26–U28 n/a(ไม่มีหน้าตั้งค่า)
- บั๊กใบก่อน (modal อนุมัติ/ส่งกลับพังตอนกำลังปิด): render() วาด modal เฉพาะ state.modal.open · renderModal คืน '' เมื่อไม่มีขั้นรอพิจารณา · confirm* guard S.md/curStep/canCancel · open* เช็กสิทธิ — ทดสอบ jsdom timer จริง
- audit.sh FAIL 0 · WARN 3 (Rule #21 ใน BASE-KIT · .uc-email ใน kit · token font-size ใน kit) · self_audit PASS (แก้ hint ยาว 1) · prune_css ตัด 69 rule แล้ว audit/self_audit ซ้ำผ่าน · node --check ผ่าน
- jsdom ทั้งไฟล์ (_build/jsdom_smoke.js · timer จริง): 42/42 ไม่มี error — สิทธิ์ G8 · กติกาบล็อก 7 เคส · เตือน 2 เคส · ออกเลข IVME · ส่ง/ตรวจสอบแล้ว/อนุมัติ 2 ขั้น · ส่งกลับเป็นร่างเลขเดิม · ส่งไม่มีคำขอ = บล็อก · ยกเลิก · PDF เติมแถวถึง DR-020 · DOA 6 ขั้น = 7 ช่อง (4+3) · DOC.active=false · CSV
- parity PDF ใน prototype: docPrintData(R1/R2/R6/R11) → render_doc.py (Python) = tplRender (JS) IDENTICAL 4/4
- [NO-BROWSER] ข้าม e2e_standard.py · [NO-BROWSER] ข้าม render-check.py
- 2026-10-11 07:44 · ขั้น 5 → done · audit FAIL0 · self_audit PASS · jsdom 42/42 · NO-BROWSER ข้าม e2e
- 2026-10-11 07:44 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-007.md (+ .docx md_to_docx) · brd-generator-full v2.3 Prebrief Mode · Quality Gate C1–C20 → APPROVED · §2.4 = DECISIONS.lock 18 DEC · OQ-01..08
- FRD_F-TMP-007_Pack 00–07 + INDEX (Input Mode 0 · FULL · API 12 · FN 12 · BR 20 · VR 12 · EC 17 · AC 16) · 07 §7.0 คัดจาก DECISIONS.lock.md ตรงตัว · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 13 (N3 DR-001 … DR-020 ไม่ hardcode)
- declaration --final: DOCCFG IVME PASS (--registry · frd_ref FN-04/FN-06) · NTF PASS (frd_ref FN-06/08/10) · DOA PASS (+print_config · frd_ref FN-05/06/07) · MDOC WARN (G04 taxonomy รอ · G09 doa pending) → สำเนาใน FRD_Pack/declarations
- 2026-10-11 07:49 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK0 WARN0 · decl final PASS

## ขั้น 8 — UI Brief → test case → UAT
- UI_BRIEF_F-TMP-007.md (AS-BUILT จาก inventory · _build/build_uibrief.py) · brief_check PASS · FAIL 0 · WARN 0
- testcases-F-TMP-007.md 43 เคส / 215 step · tc_lint ERROR 0 · cases.json (Lite 39 เคส) + QA_AUDIT drop ledger 4 · lite_audit หายเงียบ 0 (--stamp) · testcase-F-TMP-007.html (build.py · shots ว่าง)
- ค่าที่เคสอ้าง (จำนวนแถว · ตัวกรองเกินกำหนด · CSV 32 คำขอ · สรุป R1 · คิวผู้พิจารณา) ตรวจกับ prototype ด้วย jsdom (_tmp/claims.js) ตรงทุกค่า
- เคสครอบจุดบั๊กใบก่อน (modal ปิดหลังตัดสิน): TC-A01 · TC-A02 · TC-R01
- [NO-BROWSER] ข้าม verify_anchors.py · [NO-BROWSER] ข้าม capture.py (เอกสาร UAT build แบบไม่มีภาพ)
- 2026-10-11 07:54 · ขั้น 8 → done · brief_check PASS · tc_lint 0 · lite_audit 0 · NO-BROWSER: ข้าม verify_anchors/capture
