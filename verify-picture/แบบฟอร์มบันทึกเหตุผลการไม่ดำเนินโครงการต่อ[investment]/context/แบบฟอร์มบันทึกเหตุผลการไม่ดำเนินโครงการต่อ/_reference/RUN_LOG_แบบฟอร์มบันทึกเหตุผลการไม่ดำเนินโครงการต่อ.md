# RUN_LOG — F-TMP-002 FM-IVM-10แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ (REQ-TMP-002)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: to_image.py (LibreOffice → PDF → pypdfium2) ได้ page-1.png + content.html · ฟอนต์ไทยในภาพ render เป็นกล่อง → ถ้อยคำยึด content.html + openpyxl · ตำแหน่ง/เส้นยึดภาพ
- FORM_SPEC: 19 ช่อง · แถวซ้ำ 1 (เหตุผล 8 แถว ตาม data validation B20:B27) · ตัวเลือก 2 (ใช่/ไม่ใช่ · ผลการพิจารณา 4 ค่า จาก data validation D32) · ลายเซ็น 3 · anomalies 4 · form_spec_check ERROR 0
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC
- impact_summary.py regex รับเฉพาะ REQ-ตัวเลข → รันสำเนาที่แก้ regex เป็น [\w-]+ (ไม่แก้สกิล) สำหรับ REQ-TMP-002
- ไฟล์ลูกค้าไม่มีข้อมูลตัวอย่าง/ข้อมูลส่วนบุคคล (ฟอร์มเปล่า)
- 2026-10-10 23:49 · ขั้น 1 → done · FORM_SPEC 19 ช่อง ERROR 0 · PREBRIEF v2

## ขั้น 2 — มติ AI (unattended · ตาม 4_knowledge/governance/unattended-policy.md)
- G1: ฟอร์มบันทึกเหตุผล/ปิดโครงการ ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อ · ชื่อโครงการกรอกเอง (FM-IVM-01 ยังไม่ลิงก์)
- G2: dynamic 2 ขั้นตามช่องลงชื่อ: ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน → role-line-manager) · ผู้อนุมัติ/รับทราบ (รองกรรมการผู้จัดการ/กรรมการผู้จัดการ → role-gm) · ไม่มีวงเงิน · ⚠ ไม่มี role ผู้จัดการฝ่ายบริหารการลงทุน / รองกรรมการผู้จัดการ ใน doa-roles-contract
- G3: ไม่มีสูตร/ค่าคงที่ · เพิ่มกติกาตรวจ 3 ข้อจาก anomalies (≥1 เหตุผล "ใช่" + รายละเอียด · มีเงื่อนไข → ข้อสั่งการบังคับ)
- G4: ไม่จำกัดแถว · PDF ≥ 8 แถว · G5: 1:1 · G6: แถวล่างต่อขั้น ข้อความในระบบ
- G7: ไม่อนุมัติ → กลับร่างเลขเดิม · ยกเลิก owner+admin ร่าง/รออนุมัติ เหตุผลบังคับ · G8: เจ้าของ/ผู้อนุมัติหลังส่ง/admin ฝ่ายเห็นทั้งหมด
- G9: เอกสารภายใน ออกเลขตอนบันทึกครั้งแรก · รหัส IVMJ (IVM + J=ลำดับที่ 10 ของ FM-IVM-10 · กันชนกับฟอร์ม IVM อื่นที่ทำพร้อมกัน · ไม่อยู่ใน registry)
- G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock = พร้อมเริ่มทำ · 15 มติ (AI-DEFAULT 11 · VALID 4)
- 2026-10-10 23:49 · ขั้น 2 → done · DECISIONS.lock พร้อม · 15 มติ AI-DEFAULT 11
- 2026-10-10 23:50 · ขั้น 3 → done · DOA PASS (2 ขั้น dynamic) · NTF PASS (2 event) · doccfg/mdoc หลังขั้น 4

## ขั้น 3–4 — หมายเหตุ
- DOA: doa_tool init เขียน on_reject: draft แต่ validate รับแค่ back_to_draft/end → แก้ yaml เป็น back_to_draft (ตรง DEC-08) · เติมคำตัดสินขั้น 2 · validate PASS (+print_config PASS)
- ⚠ role บนกระดาษไม่มีใน doa-roles-contract: "ผู้จัดการฝ่ายบริหารการลงทุน" (ใช้ role-line-manager) · "รองกรรมการผู้จัดการ/กรรมการผู้จัดการ" (ใช้ role-gm) · module investment ไม่อยู่ใน Module Registry
- NTF: ตัด ivmj_over_limit_approved (ไม่มีเกณฑ์วงเงิน) · เพิ่ม ivmj_result_recorded · PASS
- DOCCFG IVMJ PASS (--registry) · MDOC WARN (G04 taxonomy รออนุมัติ · G09 doa pending) · source=declaration เพราะ REQ-TMP-002 ไม่ตรงรูปแบบ REQ-YYYY-NNNN · function_code F01 = ค่าชั่วคราว
- แบบพิมพ์: R9 ตารางกรอบ · ร่างแรก 1 หน้าล้นเป็น 2 หน้า (ตารางลงชื่อ+ประวัติล้น) → ออกแบบ 2 หน้าตาม R10 (ตัดหน้าก่อน "ข้อสรุป…" · หัวย่อหน้า 2 · มีต่อหน้าถัดไป · หน้า 1/2, 2/2) · ฟอนต์ 8.5pt
- parity IDENTICAL 5/5 · ไม่มี {{}} หลง
- [NO-BROWSER] ข้าม render_pdf.py / render_states.py บนเครื่องผู้ใช้ (playwright launch ล้ม) → build HTML ทุกสถานะด้วย render_doc.py + build_html.py · ตรวจจำนวนหน้าด้วย Chromium ใน cloud container จาก HTML ชุดเดียวกัน: ทุกสถานะ 2 หน้า · นำ PDF + _states_sheet.png กลับมาไว้ print/out
- compare_original (approved.pdf vs SAMPLE.pdf): 0.554 WARN — อธิบายใน print-spec §7 (แบ่ง 2 หน้า · ต้นฉบับ render ฟอนต์ไทยเป็นกล่อง)
- 2026-10-10 23:58 · ขั้น 3 → done · DOA PASS · NTF PASS · DOCCFG IVMJ PASS · MDOC WARN(G04,G09)
- 2026-10-10 23:58 · ขั้น 4 → done · Replica 2 หน้า R10 · parity 5/5 · compare 0.554 WARN อธิบายแล้ว

## ขั้น 5 — HTML Q-form
- ฐาน: references/form-archetype/_SOURCE_form-request-reference.html (เปลือก/CSS/BASE-KIT) + app script ใหม่ของ IVMJ (_build/app1–5.js · build_feature.py) + be-datepicker (Rule #114) · DOC_TPL = print/form.tpl.html · tpl_render.js วางตรง
- เทียบ GOLDEN_SKELETON v9.4 + U1–U28 ก่อน build → ปรับจาก canonical v9.2: ตัด stat cards (U1 → badge ใน ph-sub) · คน = วงกลม icon (U17) · pagination 25 + page-size (U6) · backdrop onmousedown (U25) · kebab ⋮ (U5) · header lean sub 1 fact (U19) · date = bedateHTML
- U1✓ U2✓ U3✓ U4✓ U5✓ U6✓ U7✓ U8✓ U9✓ U10✓ U11✓ U12✓ U13✓ U14✓(wizard wide 3 ขั้น) U15✓ U16 n/a(ไม่มีลบ ใช้ยกเลิก) U17✓ U18✓ U19✓ U20 n/a(ชุดเดียว ไม่มี page tabs) U21✓ U22✓ U23✓ U24✓ U25✓ U26–U28 n/a(ไม่มีหน้าตั้งค่า)
- audit.sh FAIL 0 · WARN 3 (เท่ากับ canonical: Rule #21 ใน BASE-KIT · .uc-email ใน kit · token font-size) · self_audit PASS · prune_css ตัด 46 rule แล้ว audit/self_audit ซ้ำผ่าน
- e2e: คำตัดสิน role-line-manager เดิม "ส่งกลับแก้ไข" ชนกับตัวตรวจปุ่ม "แก้ไข" (S5) → เปลี่ยนเป็น "ตรวจสอบแล้ว / ส่งกลับ" ทั้ง FORM_SPEC · DOA · print_config แล้วรัน form_spec_check · prebrief_v2 · doa/doccfg/mdoc brief · data/parity ใหม่
- [NO-BROWSER] ข้าม e2e_standard.py / render-check.py บนเครื่องผู้ใช้ → รัน e2e_standard.py ชุดเดียวกันกับ feature.html ฉบับเดียวกันใน Chromium ของ cloud container: 21/21 ผ่าน (ก่อนและหลัง prune) · reports/e2e_report.json + screenshot reports/screen_*.png (ไอคอน lucide ไม่ขึ้นในภาพเพราะ CDN ถูกบล็อกใน container)
- [NO-BROWSER] ข้าม render-check.py (visual) — ให้คนดู screenshot ใน _BATCH_REPORT
- 2026-10-11 00:12 · ขั้น 5 → done · audit FAIL0 · self_audit PASS · e2e 21/21 (cloud Chromium)
- 2026-10-11 00:12 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-002.md (+ .docx md_to_docx) · brd-generator-full v2.3 Prebrief Mode · Quality Gate C1–C20 → APPROVED · §2.4 = DECISIONS.lock 15 DEC · OQ-01..06
- FRD_F-TMP-002_Pack 00–07 + INDEX (Input Mode 0 · FULL) · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 12
- declaration --final: DOCCFG IVMJ PASS (--registry · frd_ref FN-03/FN-05) · NTF PASS (frd_ref FN-05/07/09) · DOA PASS (+print_config) · MDOC WARN (G04 taxonomy รอ · G09 doa pending) → สำเนาใน FRD_Pack/declarations
- 2026-10-11 00:17 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK0 WARN0 · decl final PASS

## ขั้น 8 — UI Brief → test case → UAT
- UI_BRIEF_F-TMP-002.md (AS-BUILT จาก inventory · _build/build_uibrief.py) · brief_check PASS · FAIL 0 · WARN 0
- testcases-F-TMP-002.md 40 เคส / 175 step · tc_lint ERROR 0 · cases.json (Lite 35 เคส) + QA_AUDIT drop ledger 5 · lite_audit หายเงียบ 0 (--stamp) · testcase-F-TMP-002.html (build.py · shots ว่าง)
- anchor: toast อนุมัติเดิม "{คำ}แล้ว" อ่านเป็น "ตรวจสอบแล้วแล้ว" → แก้เป็น "บันทึกผล {คำ} · เลขที่" แล้ว rebuild feature.html + prune + audit FAIL 0 + self_audit PASS + e2e 21/21 ซ้ำ
- [NO-BROWSER] ข้าม verify_anchors.py / capture.py บนเครื่องผู้ใช้ → รัน verify_anchors.py ใน Chromium ของ cloud container: DOM 154 · SOURCE 70 · PATTERN 6 · DATA 21 · MISSING 0 (reports/anchors.json) · capture.py ข้าม (เอกสารคนไม่มีภาพประกอบ)
- แบบพิมพ์: render PDF ใหม่ทุกสถานะหลังเปลี่ยนคำตัดสิน (Chromium cloud) — ทุกสถานะ 2 หน้า · _states_sheet.png ใหม่ · compare ใหม่ด้านล่าง
- compare_original (ใหม่) 0.554 WARN — เหตุผลเดิม (print-spec §7)
- 2026-10-11 00:26 · ขั้น 8 → done · brief_check PASS · tc_lint 0 · anchors MISSING 0 (cloud) · lite_audit 0
- ขั้น 9: K2 ไฟล์ซ้ำ prototype → เปลี่ยนชื่อ _build/feature.preprune.html → .bak และ orig/content.html (ถ้อยคำจาก to_image) → content.html.txt (ไม่ลบ)
- ขั้น 9: คัด PDF ทุกสถานะ + _states_sheet.png จาก print/out → print/IVMJ_* ให้ manifest_scan เก็บเข้า 07_Print
