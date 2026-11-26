# RUN_LOG — F-TMP-003 FM-IVM-11 แบบฟอร์มบันทึกการปิดงานและห้องข้อมูล (REQ-TMP-003)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: to_image.py (LibreOffice → PDF → pypdfium2) ได้ page-1.png + content.html · ฟอนต์ไทยในภาพ render เป็นกล่อง → ถ้อยคำยึด content.html + openpyxl · ตำแหน่ง/เส้นยึดภาพ
- FORM_SPEC: 14 ช่อง · แถวซ้ำ 2 (รายการตรวจสอบ 8 รายการคงที่ · บทเรียน 10 แถว) · ตัวเลือก 1 (สถานะ 4 ค่า จาก data validation D21:D28) · ค่าคงที่ 1 (8 รายการตรวจสอบ → config) · ลายเซ็น 3 · anomalies 5 · form_spec_check ERROR 0
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC (--module investment --req REQ-TMP-003)
- ไฟล์ลูกค้าไม่มีข้อมูลตัวอย่าง/ข้อมูลส่วนบุคคล (ฟอร์มเปล่า)
- 2026-10-11 00:29 · ขั้น 1 → done · FORM_SPEC 14 ช่อง ERROR 0 · PREBRIEF v2

## ขั้น 2 — มติ AI (unattended · ตาม 4_knowledge/governance/unattended-policy.md)
- G1: บันทึกการปิดงาน ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อ · การปรับ/ยกเลิกสิทธิห้องข้อมูลทำนอกระบบ บันทึกผลเป็นสถานะรายการ · ชื่อโครงการกรอกเอง (FM-IVM-01 ยังไม่ลิงก์)
- G2: dynamic 2 ขั้นตามช่องลงชื่อ: ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน → role-line-manager) · ผู้อนุมัติ/รับทราบ (รองกรรมการผู้จัดการ/กรรมการผู้จัดการ → role-gm) · ไม่มีวงเงิน · ⚠ ไม่มี role ผู้จัดการฝ่ายบริหารการลงทุน / รองกรรมการผู้จัดการ ใน doa-roles-contract
- G3: 8 รายการตรวจสอบพิมพ์ตายตัว → config ivmk.checklist_items · กติกาตรวจ 5 ข้อจาก anomalies (ทุกรายการ แล้วเสร็จ/ไม่เกี่ยวข้อง ก่อนส่ง · แล้วเสร็จ → ผู้รับผิดชอบ+วันที่ · ไม่เกี่ยวข้อง → หมายเหตุ · วันที่ ≤ วันปิดงาน · ข้อ 8 → บทเรียน ≥1)
- G4: รายการตรวจสอบคงที่ 8 แถว · บทเรียนไม่จำกัด · PDF ≥ 8/10 แถว · G5: 1:1 · G6: แถวล่างต่อขั้น ข้อความในระบบ
- G7: ไม่อนุมัติ → กลับร่างเลขเดิม · ยกเลิก owner+admin ร่าง/รออนุมัติ เหตุผลบังคับ · G8: เจ้าของ/ผู้อนุมัติหลังส่ง/admin ฝ่ายเห็นทั้งหมด
- G9: เอกสารภายใน ออกเลขตอนบันทึกครั้งแรก · รหัส IVMK (IVM + K=ลำดับที่ 11 ของ FM-IVM-11 · ไม่อยู่ใน registry)
- G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock = พร้อมเริ่มทำ · 17 มติ (AI-DEFAULT 12 · VALID 5)
- 2026-10-11 00:29 · ขั้น 2 → done · DECISIONS.lock พร้อม · 17 มติ AI-DEFAULT 12
- 2026-10-11 00:30 · ขั้น 3 → done · DOA PASS (2 ขั้น dynamic) · NTF PASS (3 event) · doccfg/mdoc หลังขั้น 4

## ขั้น 3–4 — หมายเหตุ
- DOA: doa_tool init เขียน on_reject: draft → แก้เป็น back_to_draft (ตรง G7) · เติมคำตัดสินขั้น 2 (อนุมัติ/ไม่อนุมัติ) · role_notes · validate PASS (+print_config PASS)
- ⚠ role บนกระดาษไม่มีใน doa-roles-contract: "ผู้จัดการฝ่ายบริหารการลงทุน" (ใช้ role-line-manager) · "รองกรรมการผู้จัดการ/กรรมการผู้จัดการ" (ใช้ role-gm) · module investment ไม่อยู่ใน Module Registry
- NTF: ตัด ivmk_over_limit_approved (ไม่มีเกณฑ์วงเงิน) · เพิ่ม ivmk_closed_handover (แจ้งผู้รับผิดชอบหลังปิดงาน + ผู้รับผิดชอบรายการ) · ivmk_lesson_assigned (แจ้งผู้รับผิดชอบบทเรียน) · PASS
- DOCCFG IVMK PASS (--registry) · MDOC WARN (G04 taxonomy รออนุมัติ · G09 doa pending) · function_code F01 = ค่าชั่วคราว
- แบบพิมพ์: R9 ตารางกรอบ · ออกแบบ 2 หน้าตาม R10 ตั้งแต่แรก (สรุป 5 ช่อง + ตรวจสอบ 8 แถว + บทเรียน 10 แถว + ลงชื่อ + ประวัติ เกิน A4 ที่ ≥8pt) · ตัดหน้าก่อน "บทเรียนที่ได้รับและการติดตามผล" · หัวย่อหน้า 2 · thead ซ้ำ · มีต่อหน้าถัดไป · หน้า 1/2, 2/2 · ฟอนต์ 8.5pt
- data 5 สถานะ (draft · approved · rejected · long-14lessons · approved-doa6steps) · parity IDENTICAL 5/5 · ไม่มี {{}} หลง (render_doc --strict + build_html ทุกสถานะ)
- [NO-BROWSER] ข้าม render_states.py / render_pdf.py → ไม่มี PDF / _states_sheet.png · ยังไม่ได้ยืนยันว่าทุกสถานะ 2 หน้าเท่ากัน → ต้องรันรอบเต็มบนเครื่องที่มี browser
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ PDF ที่ render) — บันทึกใน print-spec §7
- 2026-10-11 00:32 · ขั้น 4 → done · Replica 2 หน้า R10 · parity 5/5 · [NO-BROWSER] ไม่มี PDF/compare · DOCCFG IVMK PASS · MDOC WARN(G04,G09)

## ขั้น 5 — HTML Q-form
- ฐาน: references/form-archetype/_SOURCE_form-request-reference.html (เปลือก/CSS/BASE-KIT) + app script ของ IVMK (_build/app1–5.js · build_feature.py — โครงเดียวกับ J002 IVMJ) + be-datepicker (Rule #114) · DOC_TPL = print/form.tpl.html · tpl_render.js วางตรง
- domain: สรุปการปิดงาน 5 ช่อง · รายการตรวจสอบ 8 การ์ด (ถ้อยคำล็อกจาก CHECKLIST_CFG = config ivmk.checklist_items · สถานะ 4 ค่า seg-control · แล้วเสร็จ → ผู้รับผิดชอบ+วันที่ · ไม่เกี่ยวข้อง → หมายเหตุ) · บทเรียนการ์ดต่อแถว · กติกาส่ง (submitGaps) บล็อกทั้งใน wizard และ openSubmit จาก view · ร่างบันทึกได้ทุกสถานะ
- เทียบ GOLDEN_SKELETON v9.4 + U1–U28 ก่อน build: U1✓(ไม่มี stat cards · badge ใน ph-sub) U2✓ U3✓ U4✓ U5✓(kebab ⋮) U6✓(pagination 25 + page-size) U7✓ U8✓ U9✓ U10✓ U11✓ U12✓ U13✓ U14✓(wizard wide 3 ขั้น) U15✓ U16 n/a(ไม่มีลบ ใช้ยกเลิก) U17✓(คน = วงกลม icon) U18✓ U19✓(header sub = วันที่ปิดงาน 1 fact) U20 n/a(ชุดเดียว) U21✓ U22✓ U23✓ U24✓ U25✓(backdrop onmousedown) U26–U28 n/a(ไม่มีหน้าตั้งค่า)
- audit.sh FAIL 0 · WARN 3 (เท่ากับ canonical: Rule #21 ใน BASE-KIT · .uc-email ใน kit · token font-size) · self_audit PASS (แก้ naked_hints 2 → ย่อ hint ≤60 ตัวอักษร) · prune_css ตัด 62 rule แล้ว audit/self_audit ซ้ำผ่าน · มี meta cube-archetype=Q-form + window.__QA__
- [NO-BROWSER] ข้าม e2e_standard.py · render-check.py (ไม่มี browser บนเครื่องผู้ใช้ · ไม่ใช้ browser ใน cloud ตามกติกาชุดนี้)
- ทดสอบเสริม (ไม่ใช่ browser — jsdom บน node ในเครื่อง ติดตั้งนอก workspace): smoke ตามโครง S2/S4/S5/S7/S8/S9 + กติกา G3 + อนุมัติครบ 2 ขั้น/ส่งกลับ/ยกเลิก/ทำซ้ำ/CSV = 22/22 ผ่าน ไม่มี pageerror · พบและแก้ 1 จุด: renderModal ตอน modal approve/reject กำลังปิดหลังตัดสิน (curStep ว่าง) → guard return ''
- 2026-10-11 00:42 · ขั้น 5 → done · audit FAIL0 · self_audit PASS · [NO-BROWSER] ข้าม e2e/render-check · jsdom smoke 22/22
- 2026-10-11 00:42 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-003.md (+ .docx md_to_docx) · brd-generator-full v2.3 Prebrief Mode · Quality Gate C1–C20 → APPROVED (C16 WARN: module investment ไม่อยู่ใน Registry → OQ-03) · §2.4 = DECISIONS.lock 17 DEC · OQ-01..07
- FRD_F-TMP-003_Pack 00–07 + INDEX (Input Mode 0 · FULL · API 12 · FN 10 · AC 14 · deny 7) · frd_lint Section N รอบแรก WARN 1 (N3 "ข้อ 8" ดูเหมือน hardcode ค่าคงที่) → เปลี่ยนเป็นอ้างชื่อรายการ "บันทึกบทเรียนที่ได้รับ" ทั้ง FRD/BRD และข้อความบนจอ (rebuild feature.html + prune + audit FAIL 0 + self_audit PASS + jsdom smoke 22/22) → BLOCK 0 · WARN 0 · PASS 14
- declaration --final: DOCCFG IVMK PASS (--registry · frd_ref FN-03/FN-05) · NTF PASS (3 event · frd_ref FN-05/07/09) · DOA PASS (+print_config +html) · MDOC WARN (G04 taxonomy รอ · G09 doa pending) → สำเนาใน FRD_Pack/declarations
- 2026-10-11 00:48 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK0 WARN0 · decl final PASS (MDOC WARN G04/G09)

## ขั้น 8 — UI Brief → test case → UAT
- UI_BRIEF_F-TMP-003.md (AS-BUILT จาก inventory · _build/build_uibrief.py) · brief_check PASS · FAIL 0 · WARN 0
- testcases-F-TMP-003.md 48 เคส / 207 step · tc_lint ERROR 0 · Ledger AC-01..14 / BR / VR / EC / TC-D / DEC ครบ (ปิด BR-06/14/15 + TC-D04 ที่ขาดรอบแรก) · cases.json (Lite 42 เคส) + QA_AUDIT drop ledger 6 · lite_audit หายเงียบ 0 (--stamp) · testcase-F-TMP-003.html (build.py · shots ว่าง)
- [NO-BROWSER] ข้าม verify_anchors.py / capture.py · ตรวจ anchor แบบ static (ไม่ใช่ browser): 140 anchor · ตรงตัวใน feature.html 99 · ที่เหลือ 41 = ข้อความประกอบ/ตัวเลขที่สร้างตอนรัน (เลขที่ · จำนวน · ข้อความต่อด้วย ·) ตรวจด้วยตาแล้วมีต้นทางในโค้ด · ต้องรัน verify_anchors.py บนเครื่องที่มี browser
- เอกสารคนไม่มีภาพประกอบ (capture.py ข้าม)
- 2026-10-11 00:54 · ขั้น 8 → done · brief_check PASS · tc_lint 0 · lite_audit 0 · [NO-BROWSER] ข้าม verify_anchors/capture
