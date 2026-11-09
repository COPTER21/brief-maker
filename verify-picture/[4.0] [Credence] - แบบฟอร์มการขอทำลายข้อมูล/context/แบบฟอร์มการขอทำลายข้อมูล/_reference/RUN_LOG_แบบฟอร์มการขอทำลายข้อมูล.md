# RUN_LOG — F-TMP-003 FM-ITS-02 แบบฟอร์มการขอทำลายข้อมูลเอกสารประจำปี (REQ-TMP-003)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพฟอร์ม: to_image.py → LibreOffice → PDF → pypdfium2 (หน้ากระดาษจริงจาก print area · A4 portrait scale 84%) · ภาพยึดตำแหน่ง/เส้น · ถ้อยคำยึด content.html + sharedStrings + drawing1.xml (☐ + textbox ตัวเลือกอยู่นอกเซลล์)
- หัวฟอร์มจริง "แบบฟอร์มการขอทำลายข้อมูล" ≠ ชื่อไฟล์ "…ข้อมูลเอกสารประจำปี" → form.title ยึดหัวฟอร์ม (ชื่อในคิวไม่เพี้ยน → ไม่ rename)
- ☐ 17 ตัวใน Excel: ประเภทข้อมูล 10 · เหตุผล 4 · วิธีการ 3 (ตัวเลือก "เข้ารหัสและทำลายข้อมูลอย่างปลอดภัย" ไม่มี ☐ → anomaly · แสดงครบ 4)
- ลงชื่อ 4 ช่อง: ผู้ร้องขอ · ตรวจสอบ · เจ้าหน้าที่ IT · อนุมัติ (สะกดผิด อนุมัมติ) · footer Doc. No. FM-ITS-02 Rev.00 : 01/07/2569 · prefix เลขที่ DRITS.
- ไม่มี PREBRIEF จาก CMS → PREBRIEF v2 จาก FORM_SPEC (--req REQ-TMP-003) · รอบแรกลืม --req ได้ REQ-XXXX → ย้ายไฟล์ผิดไป .scratch/old
- form_spec_check: ERROR 0 · 10 ช่อง · ตัวเลือก 3 · ลายเซ็น 4 · ข้อมูลส่วนบุคคล: ฟอร์มเปล่า ไม่มีข้อมูลตัวอย่างจริง
- 2026-10-10 08:31 · ขั้น 1 → done · FORM_SPEC 10 ช่อง ERROR 0 · PREBRIEF v2 · impact summary

## ขั้น 2 · gate (unattended — AI-DEFAULT 11 มติ + VALID 6)
- G1: ฟอร์มไม่ระบุการเปลี่ยนค่า/ส่งต่อ → config_changes [] · post_to [] (การทำลายจริงทำนอกระบบ · ระบบเก็บผล)
- G2: ช่องผู้อนุมัติบนกระดาษ 2 ช่อง (ตรวจสอบ · อนุมัติ) → dynamic 2 ขั้น role-line-manager → role-mgr-it (ผู้จัดการฝ่าย IT = role ตามหน้าที่ ฟอร์มของฝ่าย IT) · ไม่มีวงเงิน · role-mgr-it ไม่มีใน doa-roles-contract → แจ้ง _BATCH_REPORT
- G3: ไม่มีสูตร/ค่าคงที่ · ถึง ≥ จาก (บังคับ) · ถึง ≤ วันที่ขอ (เตือน) · อื่นๆ ต้องระบุ · เลือก ≥1 ต่อกลุ่ม
- G4: ไม่มีรายการซ้ำ
- G5: 1:1 · แก้สะกด ตําแหน่ง→ตำแหน่ง · อนุมัมติ→อนุมัติ · ☐ ครบหน้า เข้ารหัสฯ
- G6: แถวล่าง 4 ช่องตามกระดาษ: ผู้ร้องขอ · ตรวจสอบ (DOA 1) · เจ้าหน้าที่ IT (ผู้ดำเนินการทำลาย — ลงเมื่อบันทึกผลทำลาย ไม่ใช่ขั้น DOA) · อนุมัติ (DOA 2) · ข้อความในระบบ ไม่ใช้ภาพ
- G7: ไม่อนุมัติ → กลับร่างเลขเดิม · ยกเลิก owner+admin ใน draft/pending · เหตุผลบังคับ
- G8: เจ้าของ · ผู้อนุมัติหลังส่ง · admin role ฝ่าย IT เห็นทั้งหมด
- G9: ออกเลขตอนบันทึกครั้งแรก · รหัส DRITS (prefix "DRITS." บนกระดาษ)
- G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- decisions_lock: พร้อมเริ่มทำ (exit 0) · dm.sh tag → AI-DEFAULT 11
- 2026-10-10 08:31 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · AI-DEFAULT 11

## ขั้น 3 · declaration ร่าง
- doa: init module=it (dept `it` ใน contract · ไม่มี module IT ใน registry) · doa_type drits · 2 ขั้น role-line-manager (ตรวจสอบ) → role-mgr-it (อนุมัติ) · init เขียน on_reject: draft → แก้เป็น back_to_draft (บทเรียน J001) · validate WARN G1 (role-mgr-it ไม่อยู่ใน contract) · BLOCK 0
- ntf: drits_cancelled · drits_ready_for_it (approved → คิว IT · role-it-officer) · drits_destroyed (IT บันทึกการทำลาย → แจ้งผู้ขอ) · ตัด over_limit_approved (ไม่มีเกณฑ์วงเงิน) → PASS
- role-mgr-it (อนุมัติ) + role-it-officer (เจ้าหน้าที่ IT / admin role ฝ่าย IT) ไม่มีใน doa-roles-contract → แจ้งใน _BATCH_REPORT
- doccfg + mdoc ทำหลังขั้น 4
- 2026-10-10 08:32 · ขั้น 3 → done · doa WARN (role-mgr-it นอก contract) BLOCK 0 · ntf PASS · doccfg/mdoc หลังขั้น 4

## ขั้น 4 · แบบพิมพ์ Replica (R9 ตารางกรอบ · 1 หน้า)
- form.tpl.html R9 (หัวช่องพื้นเทา th) + sign_rows (ผู้ร้องขอ + ขั้น DOA + เจ้าหน้าที่ IT ท้ายสุด) · profile.json · print_config.json · make_data.py → 5 สถานะ (draft · approved · rejected · long-text · approved-doa6steps 8 ช่อง 4+4) · ข้อมูลสมมติทั้งหมด
- parity_check: IDENTICAL 5/5 · ไม่มี {{}} หลง · ไม่มี key ขาด · build_html ทุกสถานะ → print/out/*.html + DRITS_template.html (.scratch/render_nobrowser.py)
- [NO-BROWSER] ข้าม render_pdf.py (ภายใน render_states.py) — render body + build_html ทีละสถานะแทน ได้ HTML ไม่มี PDF/PNG/_states_sheet.png
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ approved.pdf)
- ตรวจภาพเบื้องต้นนอกเครื่องงาน (stage long-text + doa6steps ไป Chromium ใน container ของ agent · ไม่เก็บไฟล์กลับ): 1 หน้า A4 · ลายเซ็นไม่ตัด · ฟอนต์ ≥ 8pt → ไม่เข้า R10 · ไม่ใช่ผลด่านทางการ ต้องรัน render_states --max-pages 1 บนเครื่องที่มี browser
- ลำดับช่องลงชื่อต่างกระดาษ: กระดาษ ผู้ร้องขอ·ตรวจสอบ·เจ้าหน้าที่ IT·อนุมัติ → ระบบ ผู้ร้องขอ·[DOA ตรวจสอบ·อนุมัติ]·เจ้าหน้าที่ IT (IT ลงเมื่อทำลายเสร็จหลังอนุมัติ · ขั้น DOA ต้องต่อเนื่อง) → print-spec §7
- doccfg: DRITS · registry ไม่ชน (ACL/ITRS/SRC) → PASS · mdoc: WARN G04 (ยังไม่มี taxonomy_def_id) + G09 (doa pending) — อธิบายได้ · module "เอกสารทั่วไป" · function_code F01 ชั่วคราว
- doa validate --print-config: WARN (role-mgr-it นอก contract) · BLOCK 0
- 2026-10-10 08:35 · ขั้น 4 → done · parity 5/5 IDENTICAL · HTML ทุกสถานะ · [NO-BROWSER] ไม่มี PDF/compare · doccfg PASS · mdoc WARN อธิบายได้

## ขั้น 5 · HTML Q-form (html-generator v9.4)
- build: .build/build_feature.py ประกอบจาก canonical references/form-archetype (shell + BASE-KIT) + be-datepicker + tpl_render.js (verbatim) + app ของ DRITS (.build/app.js = โครง Q-form เดียวกับ F-TMP-001 + patch_*.py แก้ domain) + extra.css (Group 25) · PDF tab ฝัง print/form.tpl.html + docPrintData() (data contract = make_data.py)
- เปิด GOLDEN_SKELETON + U1–U28 เทียบก่อน build: U1 ✓ (ไม่มี stat cards · badge ใน sub) · U2 ✓ · U3 ✓ · U4 ✓ · U5 ✓ kebab ⋮ · U6 ✓ page-size 10/25/50 + x–y จาก N + pager · U7 ✓ CSV ที่ head · U8 ✓ 920/1290 · U9 ✓ เหตุผลบังคับ · U10 ✓ · U11 ✓ · U12 ✓ · U13 ✓ summary+timeline+emp-chip · U14 ✓ Q-form wizard 3 ขั้น · U15 ✓ แก้ไข = wizard เดิม+prefill เฉพาะร่าง · U16 – (ไม่มีลบ: ยกเลิก = soft + เหตุผล) · U17 ✓ คน = วงกลม icon · U18 ✓ nowrap+ellipsis · U19 ✓ header sub 1 fact (ช่วงข้อมูล) · U20 ✓ seg tabs ทั้งหมด/รอฉันพิจารณา/คำขอของฉัน · U21 ✓ · U22 ✓ chips ≤3 ค่า 0 ซ่อน · U23 ✓ empty state · U24 ✓ search-select portal · U25 ✓ backdrop onmousedown (drawer+modal) · U26–U28 – (ไม่มีหน้าตั้งค่า)
- audit.sh: FAIL 0 · WARN 3 (มาจาก BASE-KIT ของ canonical: comment lucide · .uc-email CSS · font-size px ใน shell) · prune_css ตัด 77 rule → audit ซ้ำ FAIL 0 · มี meta cube-archetype + window.__QA__
- prune_css ตัด .jt-grid.cols-5/.cols-2 รอบแรก (class ประกอบจาก template literal) → เปลี่ยนเป็นชื่อ class ตรงตัว แล้ว build/prune ใหม่
- [NO-BROWSER] ข้าม e2e_standard.py · ข้าม render-check.py บนเครื่องงาน
- ตรวจเบื้องต้นนอกเครื่องงาน (stage feature.html ไป Chromium ใน container ของ agent · lucide stub · ไม่เก็บไฟล์กลับ): e2e_standard 21/21 หลัง prune · flow สร้าง→ส่ง 2 ขั้น→อนุมัติ E02→อนุมัติ E10→บันทึกการทำลาย E08 ไม่มี pageerror · validate ถึง<จาก บล็อก — ไม่ใช่ผลด่านทางการ ต้องรันซ้ำบนเครื่องที่มี browser
- ช่องตามกระดาษ 1:1 (#106): ชื่อ-นามสกุล/ตำแหน่ง/วันที่/เลขที่ = ระบบใส่ (การ์ดสรุป) · กรอก: รายละเอียดของข้อมูล · โปรแกรม · ประเภทข้อมูล ☐10 · ช่วงเวลา จาก/ถึง (bedateHTML) · เหตุผล ☐4 (+อื่นๆ ระบุ) · วิธีการ ☐4 (+อื่นๆ ระบุ) · ไม่มีช่องเพิ่ม
- สถานะ: ร่าง → รออนุมัติ (ขั้น 1 ตรวจสอบ → ขั้น 2 อนุมัติ) → รอทำลายข้อมูล (อนุมัติแล้ว) → ทำลายแล้ว (เจ้าหน้าที่ IT) · ไม่อนุมัติ = กลับร่างเลขเดิม + แบนเนอร์เหตุผล · ยกเลิก (ร่าง/รออนุมัติ · เจ้าของ+admin IT)
- หมายเหตุ: ในแท็บ PDF ของ container (ไม่มี Google Fonts) แถว ☐ ประเภทข้อมูลตัดบรรทัดเพราะฟอนต์สำรอง · แบบพิมพ์จริงฝัง Sarabun (out/*.html) ไม่ตัด
- 2026-10-10 08:44 · ขั้น 5 → done · audit FAIL 0 · U1–U28 ✓ · [NO-BROWSER] e2e/render-check ข้าม (pre-check นอกเครื่อง 21/21)
- 2026-10-10 08:44 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-003.md/.docx (brd-generator-full v2.3 Prebrief Mode · Lane) — AI Review C01–C23 + PE01–PE05 → **APPROVED** (C16 ไม่มีรหัสใน registry = ยอมรับใน Prebrief Mode · ตัวชี้วัดไม่มีใน input → OQ-01)
- FRD_F-TMP-003_Pack (frd-generator-v6.2 Input Mode 0 · FULL variant: states=5) 00–07 + INDEX + declarations/ · 07 §7.0 = แถว DEC จาก DECISIONS.lock.md ตรงตัว (17)
- FRD บรรยายสาย DOA ตรงมติ DEC-03 (2 ขั้น ตรวจสอบ → อนุมัติ) · เจ้าหน้าที่ IT = executor ไม่ใช่ขั้น DOA (บทเรียน K2/K7 จาก J001/J002)
- frd_lint Section N: BLOCK 0 · WARN 0 · PASS 13
- declaration --final: doccfg PASS (registry ไม่ชน · frd_ref FN-02/FN-04) · ntf PASS (frd_ref FN-06/04/07) · doa WARN (role-mgr-it นอก contract · --print-config) BLOCK 0 · mdoc WARN G04 + G09 — อธิบายได้
- 2026-10-10 08:48 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 · declaration final BLOCK 0 (doa WARN role-mgr-it · mdoc WARN G04/G09)

## ขั้น 8 · UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-003.md (§0–§13 · CSS vars/z-index/microcopy สกัดจาก reports/inventory.json ด้วย .build/gen_ui_brief.py) · brief_check: PASS · FAIL 0 · WARN 0 (รอบแรก B5 FAIL: อ้าง id ที่ประกอบจาก template literal → เขียนใหม่ไม่อ้าง id ตรง)
- testcases-F-TMP-003.md: 64 เคส / 228 step (L12 C5 V10 F3 D4 A4 T3 K3 P6 R5 E6 X3) · tc_lint ERROR 0 · Coverage Ledger + Audit (S 13/13 · DEC 17/17 · XT 4/4 · ข้าม BR-15/EC-06/EC-07 พร้อมเหตุผล)
- [NO-BROWSER] ข้าม verify_anchors.py บนเครื่องงาน · ตรวจเบื้องต้นนอกเครื่องงาน (Chromium ใน container ของ agent · lucide stub): DOM 292 · SOURCE 61 · PATTERN 5 · DATA 44 · MISSING 0 — ไม่ใช่ผลด่านทางการ
- UAT (qa-friendly v3.1 Lite): cases.json 53 เคส · drop ledger 11 (คำสั่งหลังบ้าน/จำลอง/แจ้งเตือนจริง/ต้อง render PDF) · lite_audit หายเงียบ 0 + stamp md5 · build testcase-F-TMP-003.html
- [NO-BROWSER] ข้าม capture.py → ไม่มีภาพหน้าจอ (regionKey ว่างทุก step · shots_b64.json = {})
- 2026-10-10 08:55 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 (64 เคส) · lite_audit หายเงียบ 0 · [NO-BROWSER] verify_anchors/capture ข้าม
