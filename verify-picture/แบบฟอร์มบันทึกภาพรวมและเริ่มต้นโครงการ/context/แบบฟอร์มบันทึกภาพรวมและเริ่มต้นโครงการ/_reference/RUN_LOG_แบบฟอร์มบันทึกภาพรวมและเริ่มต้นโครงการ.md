# RUN_LOG — F-TMP-001 FM-BDM-01 แบบฟอร์มบันทึกภาพรวมและเริ่มต้นโครงการ (REQ-TMP-001)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · อ่านฟอร์ม + PREBRIEF v2
- ภาพ: to_image.py (LibreOffice → PDF → pypdfium2) → orig/SAMPLE.pdf + page-1.png (ฟอนต์ไทยไม่มีใน LibreOffice → ภาพเห็นกล่องแทนอักษร · ถ้อยคำยึด content.html/openpyxl · ตำแหน่ง/เส้นยึดภาพ)
- ท้ายกระดาษ (footer xlsx): Doc. No. : FM-BDM-01 · Rev.00 : 01/07/2569 · data validation สถานะกิจกรรม = ยังไม่เริ่ม/กำลังดำเนินการ/รอตรวจทาน/แล้วเสร็จ/พักงาน
- FORM_SPEC 28 ช่อง (กรอก 23 · ระบบใส่ 5) · แถวซ้ำ 2 (แผนงาน 6 แถว · ประวัติการแก้ไข 1 แถว) · ลายเซ็น 3 · ข้อมูลขัดกัน 3 → form_spec_check ERROR 0
- ไม่มี PREBRIEF CMS → prebrief_v2 (module BDM — ยังไม่มีใน FEATURE_REGISTRY → เสนอใน _BATCH_REPORT)
- แก้บั๊ก impact_summary.py: regex หัว PREBRIEF รับ REQ-[\d-]+ เท่านั้น → REQ-[\w-]+ (รองรับ REQ-TMP-001) — ไม่กระทบด่าน
- PDPA: ฟอร์มเปล่า ไม่มีข้อมูลส่วนบุคคลจริง
- 2026-10-10 08:38 · ขั้น 1 → done · form_spec_check ERROR 0 · 28 ช่อง

## ขั้น 2 · gate (unattended · AI-DEFAULT)
- G1 ไม่เปลี่ยนค่า/ไม่ส่งต่อ (เอกสารบันทึกเริ่มโครงการ) · G2 dynamic 2 ขั้นตามช่องผู้อนุมัติบนกระดาษ: ผู้ตรวจสอบ=role-line-manager (ผู้จัดการฝ่ายพัฒนาธุรกิจ ไม่มี role ใน master) → ผู้อนุมัติ/รับทราบ=role-gm (รองกรรมการผู้จัดการ/กรรมการผู้จัดการ ใกล้สุดใน master — รอยืนยัน) · ไม่มีวงเงิน
- G3 ไม่มีค่าคงที่ · กฎวันที่ 2 ข้อ · G4 ไม่จำกัด (PDF ≥6/≥1) · G5 1:1 แยก 2 แถวรวมค่า · G6 แถวต่อขั้น DOA · G7 กลับร่าง · G8 เจ้าของ/ผู้อนุมัติหลังส่ง/admin · G9 first_save รหัส PJI · G10 แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- DECISIONS.lock พร้อมเริ่มทำ · 15 มติ (AI-DEFAULT 12 · VALID 3)
- 2026-10-10 08:39 · ขั้น 2 → done · พร้อมเริ่มทำ · AI-DEFAULT 12

## ขั้น 3 · declaration ร่าง
- แก้ decisions.yaml G7 `on_reject: draft` → `back_to_draft` (ค่าที่ doa_tool รับ) → lock ใหม่ + tag (AI-DEFAULT 12 เท่าเดิม)
- doa: PJI.doa.yaml dynamic 2 ขั้น (role-line-manager → role-gm) ไม่มีวงเงิน · validate/brief PASS (INFO: role-line-manager relative role)
- ntf: ตัด pji_over_limit_approved (ไม่มีเกณฑ์ตัวเลข) · เพิ่ม pji_owner_assigned (อนุมัติแล้วแจ้งผู้รับผิดชอบหลัก/กิจกรรม) · validate/brief PASS
- doccfg + mdoc ทำหลังขั้น 4 (ใช้ print_config)
- 2026-10-10 08:39 · ขั้น 3 → done · doa PASS · ntf PASS · doccfg/mdoc หลังขั้น 4

## ขั้น 4 · แบบพิมพ์ Replica (R9 ตารางกรอบ · 2 หน้า R10)
- ต้นฉบับพิมพ์ 1 หน้าที่ scale 46% → ที่ ≥8pt เกิน A4 → ออกแบบ 2 หน้า (ตัดก่อนแผนงานเบื้องต้น · หัวตารางซ้ำ · "มีต่อหน้าถัดไป" · "หน้า 1/2") ฟอนต์ 9pt
- data 5 สถานะ (draft · approved · rejected · long-14rows · approved-doa6steps 7 ช่อง 4+3) · ข้อมูลสมมติทั้งหมด
- parity_check IDENTICAL 5/5 · render_doc ไม่มี {{}} · missing key 0 · build_html PASS ทุกสถานะ (out/*.html)
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py ขั้น PDF/ภาพ/นับหน้า · _states_sheet.png) — ทำ HTML แทน · ต้องรัน `render_states.py --max-pages 2` บนเครื่องที่มี browser
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ approved.pdf) — ภาพต้นฉบับ orig/page-1.png ดูแล้ว
- print_config.json (PJI · pages 2 · sign_boxes doa_step:* · decision_words.by_role) · print-spec PJI_print-spec.md
- doccfg init/brief --registry PASS (PJI ไม่ชน) · mdoc brief WARN (G04 taxonomy ว่าง · G09 doa pending) — source=declaration เพราะ REQ-TMP-001 ไม่ใช่เลข F186 · doa validate --print-config PASS
- 2026-10-10 08:43 · ขั้น 4 → done · parity 5/5 · 2 หน้า R10 · [NO-BROWSER] ไม่ได้ PDF

## ขั้น 5 · HTML Q-form (html-generator v9.4)
- ฐาน: DevPack ตัวอย่าง F-FIN-ACL (ผ่าน audit FAIL 0) — คง CSS/shell/framework · เขียน domain script ใหม่ทั้งหมดตาม FORM_SPEC (build/a1–a8.js + assemble.py)
- เทียบ GOLDEN_SKELETON + U1–U28 แล้วแก้จากฐาน ACL: ตัด stat cards → ph-badge (U1) · segmented ทั้งหมด/รอฉันพิจารณา (U20) · คน = วงกลมไอคอน ไม่มี initials (U17) · backdrop onmousedown + target check (U25) · header sub = ชื่อโครงการ + เป้าหมาย (U19) · วันที่ใช้ bedateHTML (Rule #114)
- U1✓ U2✓ U3✓ U4✓ U5✓ U6✓ U7✓ U8✓ U9✓ U10✓ U11✓ U12✓ U13✓ U14✓(Wizard 1290) U15✓ U16 n/a(ไม่มีลบ · ยกเลิกมีเหตุผล) U17✓ U18✓ U19✓ U20✓ U21~(WARN token font-size จากฐาน) U22✓ U23✓ U24✓ U25✓ U26–U28 n/a (ไม่มีหน้า config)
- audit.sh FAIL 0 · WARN 3 (เท่าฐาน ACL: lucide class ใน helper · .uc-email · hardcoded font-size) · prune_css ตัด 2.0 KB แล้ว audit ซ้ำ FAIL 0
- [NO-BROWSER] ข้าม e2e_standard.py · ข้าม render-check.py — ทดแทนชั่วคราวด้วย jsdom smoke (reports/smoke_jsdom.json): เปิด view ทุกใบ×4 แท็บ · validation ช่องบังคับ/วันที่เป้าหมาย/วันครบกำหนด บล็อก · สร้าง→ส่ง→ตรวจสอบ(E02)→อนุมัติ(E10) = approved + ประวัติการแก้ไข 1 ฉบับ · ส่งกลับแก้ไข → ร่าง · owner ไม่เห็นร่างคนอื่น / admin เห็น · PDF 2 หน้าไม่มี {{}} · DOC.active=false ปุ่มสร้าง disabled · JS error 0
- parity: docPrintData(prototype) → parity_check IDENTICAL 2/2 · key set ตรงกับ print/*.data.json
- 2026-10-10 08:54 · ขั้น 5 → done · audit FAIL 0 · [NO-BROWSER] e2e ข้าม (jsdom smoke ผ่าน)
- 2026-10-10 08:54 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-001.md/.docx (APPROVED · Prebrief Mode) · FRD_F-TMP-001_Pack 00–07 + INDEX + declarations/
- frd_lint: BLOCK 0 · WARN 0 · PASS 12 (reports/_SECTION_N.md)
- ใส่ frd_ref: doccfg numbering FN-03 · snapshot FN-05 · ntf pji_cancelled FN-07/09 · pji_owner_assigned FN-05/09
- doccfg brief --final --registry PASS (PJI ไม่ชน) · ntf brief --final PASS · doa brief --print-config PASS · mdoc WARN (taxonomy ว่าง · doa pending)
- 2026-10-10 08:58 · ขั้น 7 → done · frd_lint BLOCK 0 · declaration --final PASS

## ขั้น 8 · UI Brief → test case → UAT
- แก้ toast อนุมัติขั้นกลาง → 'บันทึกผล "<คำตัดสิน>" แล้ว · เลขที่' (เดิมซ้ำคำ "แล้วแล้ว") → assemble + prune ใหม่ · audit FAIL 0 · jsdom smoke ผ่าน
- UI_BRIEF_F-TMP-001.md (AS-BUILT จาก extract_anchors) · brief_check FAIL 0 WARN 0 (B1–B8 PASS)
- testcases-F-TMP-001.md 36 เคส · 83 step · tc_lint ERROR 0 · cases.json + QA_AUDIT · lite_audit หายเงียบ 0 (stamp แล้ว)
- testcase-F-TMP-001.html build แบบไม่มีภาพ (shots ว่าง)
- [NO-BROWSER] ข้าม verify_anchors.py · ข้าม capture.py — ทดแทน: anchor ตัวหนา 86 จุด ตรวจ static 77 + runtime jsdom 9 = ไม่พบ 0 (reports/anchors_static.json · anchors_runtime.json)
- 2026-10-10 09:04 · ขั้น 8 → done · brief_check 0 · tc_lint 0 · lite_audit 0 · [NO-BROWSER] verify_anchors/capture ข้าม
