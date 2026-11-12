# RUN_LOG — F-TMP-005 FM-PUR-03 PR-PO Outstanding (REQ-TMP-005)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพฟอร์ม: `to_image.py` → LibreOffice → PDF → pypdfium2 (2 หน้า = 2 ชีต) · ฟอนต์ไทยในภาพเป็นกล่อง → ถ้อยคำยึด xlsx (openpyxl) · ตำแหน่ง/เส้นยึดภาพ · ใช้เสร็จเปลี่ยนชื่อ orig/content.html → orig/content_text.htm (กัน K2)
- ไฟล์มี 2 ชีตเนื้อหาเดียวกัน: ชีต 1 แนวนอน FM-PUR-003 Rev.02 16/6/2026 (ต้นแบบ) · ชีต 2 แนวตั้ง footer FM-PUR-03 REV.00 01/07/2569 → anomaly
- archetype = report (รายงานติดตาม/สอบทาน PR-PO ค้าง · ตารางรายการ 8 แถว + ผู้จัดทำ + ผู้มีอำนาจอนุมัติ)
- PR (F072) / PO (F078) / Supplier ยังไม่มีในระบบ (FEATURE_REGISTRY "—") → เลขที่ PR/PO · ผู้ผลิต กรอกเอง (G1 policy) · หน่วย = UOM Master · ฝ่าย/แผนก = ผังองค์กร
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC (--module PUR)
- form.title = "แบบฟอร์มรายงานผลการสอบทานคำขอซื้อและใบสั่งซื้อค้างนาน (PR/PO Outstanding)" (หัวฟอร์ม A1) · ชื่อในคิวไม่เพี้ยน → ไม่ rename
- form_spec_check: ERROR 0 · WARN 0 · 17 ช่อง · แถวซ้ำ 1 กลุ่ม (8 แถว) · ลายเซ็น 2 · anomalies 5
- 2026-10-10 05:39 · ขั้น 1 → done · FORM_SPEC 17 ช่อง ERROR 0 · PREBRIEF v2 สร้างจากฟอร์ม

## ขั้น 2 · gate (unattended — AI-DEFAULT 11 มติ + VALID 5)
- G1 รายงานสอบทาน ไม่เปลี่ยนค่า/ไม่ปิด PR-PO/ไม่ส่งต่อ (PR F072 · PO F078 ยังไม่มี → กรอกเลขอ้างอิงเอง) · G2 ช่อง "ผู้มีอำนาจอนุมัติ" 1 จุดไม่ระบุตำแหน่ง → role-mgr-pur (ผู้จัดการ module purchase · มีใน contract) · G3 ไม่มีค่าคงที่/สูตร · กฎ PR หรือ PO ≥1 · มี PO → วันที่สั่งซื้อ+ผู้ผลิตบังคับ · วันที่รับ ≥ วันที่สั่งซื้อ · เกณฑ์ "ค้างนาน" ไม่แต่ง (OQ)
- G4 ไม่จำกัดแถว · PDF ขั้นต่ำ 8 · G5 1:1 ต้นแบบชีต 1 Rev.02 · G6 แถวล่างต่อขั้น · G7 กลับร่าง · G8 admin = role-mgr-pur · G9 PPO ออกเลขตอนบันทึกครั้งแรก · G10 แนบ ✓ CSV ✓ ทำซ้ำ ✗
- 2026-10-10 05:40 · ขั้น 2 → done · 16 มติ (AI-DEFAULT 11 · VALID 5) พร้อมเริ่มทำ

## ขั้น 3 · declaration ร่าง
- doa: init เขียน on_reject: draft → แก้เป็น back_to_draft (ความหมายเดิมตาม G7) → PASS · 1 ขั้น role-mgr-pur ป้าย "ผู้มีอำนาจอนุมัติ" (role มีใน doa-roles-contract.md — `--roles` รับไฟล์ .md ไม่ได้ จึงตรวจด้วย grep)
- ntf: เก็บ ppo_cancelled · ตัด ppo_over_limit_approved (ไม่มีเกณฑ์ตัวเลข/วงเงิน) → PASS
- doccfg + mdoc ทำหลังขั้น 4 (ต้องใช้ print_config)
- 2026-10-10 05:40 · ขั้น 3 → done · doa PASS · ntf PASS (doccfg/mdoc หลังขั้น 4)

## ขั้น 4 · แบบพิมพ์ Replica (R9 ตารางกรอบ + R10 2 หน้า)
- ต้นฉบับ A4 แนวนอน (ชีต 1 Rev.02) แต่ engine thai-doc ล็อก A4 แนวตั้ง → ตาราง 37 คอลัมน์ฐานตามสัดส่วนเดิม · ถ้อยคำ/ลำดับคอลัมน์ 1:1
- ออกแบบ 2 หน้าตาม R10: หน้า 1 = หัว + 4 บรรทัด + ตาราง 12 แถว (ขั้นต่ำ 8 = กระดาษ) + "มีต่อหน้าถัดไป" · หน้า 2 = ใบต่อ (หัวย่อ + หัวตารางซ้ำ + แถว 13–24 ขั้นต่ำ 5) + ลงชื่อทั้งก้อน · ฟอนต์ 8pt · "หน้า n/2"
- รอบแรก 18+20 แถว → ภาพ Chromium ล้น 3–4 หน้า (ข้อความคอลัมน์แคบตัด 3 บรรทัด · วันที่ล้นช่อง) → ปรับ 12+12 + ขยายคอลัมน์วันที่ 2→3 → ทุกสถานะ 2 หน้า
- parity_check: IDENTICAL 5/5 (draft · approved · rejected · long-24items · approved-doa6steps 4+3)
- [NO-BROWSER] ข้าม render_pdf.py (ใน render_states.py) — render body + build_html เอง (_build/render_nobrowser.py) ครบ 5 สถานะ (ไม่มี {{}} หลง · missing key 0 · โครง 2 หน้าทุกสถานะ)
- ตรวจภาพเพิ่ม: Chromium ใน container ของ agent → out/_states_sheet.png (คัดกลับเครื่อง)
- [NO-BROWSER] ข้าม compare_original.py (ไม่มี approved.pdf บนเครื่อง) · คาด WARN เพราะเปลี่ยนแนวกระดาษ — บันทึกใน print-spec §7
- ไฟล์ค้างลบไม่ได้: ย้าย data/html ชุด long-38items (รอบแรก) ไป _build/trash/ · print/out/_<state>.body.html (ไฟล์ชั่วคราว)
- doccfg PPO PASS (registry ไม่ชน: ACL FEC FLI SMC VEV · J006 ใช้ COI) · mdoc WARN (G04 ไม่มี taxonomy_def_id · G09 doa pending) · source=declaration (REQ-TMP ไม่ใช่ REQ-YYYY-NNNN)
- doa validate --print-config PASS
- 2026-10-10 05:45 · ขั้น 4 → done · 2 หน้า R10 · parity 5/5 · [NO-BROWSER] ไม่มี PDF/compare (ภาพตรวจจาก Chromium container) · doccfg PASS · mdoc WARN

## ขั้น 5 · HTML Q-form (html-generator v9.4)
- ฐาน: โครง Q-form ที่ผ่านด่านแล้วในงานเดียวกัน (J003 · BASE-KIT + BE Date Picker Rule 114 · ไม่แก้ BASE-KIT) เทียบ GOLDEN_SKELETON + U1–U28 · เปลี่ยน domain ทั้งหมดด้วย _build/patch_feature.py + new_*.js · ฝัง form.tpl.html (PPO_TPL) + tpl_render.js + PDF_CSS (base+replica+profile ใหม่)
- archetype Q-form (report) · แถวรายการ 12 ช่อง > 4 → ตารางกรอก (Rule #107) เลื่อนแนวนอน · หน่วย = search-select UOM Master · ฝ่าย/แผนก + หน่วยงาน = search-select ผังองค์กร · วันที่ทุกช่อง bedate พ.ศ. · PR/PO/ผู้ผลิต = ข้อความ (ยังไม่มี feature)
- ตัด "ทำซ้ำ" ออก (DEC-11 extras.copy = false) — เมนู ⋮ = แก้ไข[ร่าง] · พิมพ์ · ยกเลิก
- audit.sh: FAIL 0 · WARN 3 (จาก BASE-KIT เดิม: #21 · #40 .uc-email · font-size px ใน kit) · prune_css ตัด 1 rule แล้ว audit ซ้ำ FAIL 0
- [NO-BROWSER] ข้าม e2e_standard.py · ข้าม render-check.py → smoke test jsdom (reports/smoke_jsdom.js) 47/47 PASS: สิทธิ์เห็น owner/approver/admin · ทุก tab ทุกใบ ไม่มี error · PDF 2 หน้าไม่มี {{}} (12+5 / ร่าง 8+5 / ยาว 24 = 12+12 dense / เกิน 24 ตัดที่ 24) · validation (≥1 แถว · PR หรือ PO · มี PO → วันที่สั่งซื้อ+ผู้ผลิต · วันที่สั่งซื้ออนาคต/หลังวันที่รายงาน · วันที่รับก่อนวันที่สั่งซื้อ · จำนวน > 0 · ช่องบังคับ) · PO ซ้ำ = เตือน · ส่ง → ไม่อนุมัติ → แก้ → ส่งใหม่ → อนุมัติ · DOA 2 ขั้นเรียงขั้น · ยกเลิก · DOC.active · S.sim · CSV · ไม่มีทำซ้ำ
- ตรวจภาพเพิ่ม (Chromium ใน container ของ agent · ไม่มีไอคอนเพราะ offline · pageerror 0): wizard · view · PDF Preview แสดงถูก · แก้ eyebrow หัว drawer ที่ซ้ำ (DOC_NAME มี "(PR/PO Outstanding)" อยู่แล้ว) → ใช้ชื่อสั้น
- U1–U28: U1✓ no-scorecard · U2✓ · U3✓ · U4✓ · U5✓ kebab ⋮ · U6✓ pager 25 · U7✓ CSV ที่ head · U8✓ 920/wide · U9✓ เหตุผลบังคับ · U10✓ pill · U11✓ · U12✓ lucide mono · U13✓ block ลายเซ็นกลาง · U14✓ Q2 wizard 3 ขั้น · U15✓ edit = wizard เดียวกัน · U16 n/a (ไม่มีลบเอกสาร ใช้ยกเลิก+เหตุผล · ลบแถวในตาราง) · U17✓ person icon · U18✓ · U19✓ header sub 2 fact · U20✓ segmented (ทั้งหมด/รอฉันอนุมัติ) · U21✓ · U22✓ · U23✓ empty panel ทุกตาราง · U24✓ search-select · U25✓ backdrop onmousedown · U26–U28 n/a (ไม่มีหน้า config)
- 2026-10-10 05:53 · ขั้น 5 → done · audit FAIL 0 · [NO-BROWSER] e2e ข้าม → jsdom smoke 47/47 · U1–U28 ✓
- 2026-10-10 05:53 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-005.md (+ .docx md_to_docx) · Prebrief Mode · AI Review C01–C23/PE01–05 → APPROVED (C22 ตัวชี้วัด → OQ-01 ตามกติกา ห้ามแต่งตัวเลข) · OQ 9 ข้อ
- FRD_F-TMP-005_Pack 00–07 + INDEX · 07 §7.0 สร้างจาก DECISIONS.lock.json ตรงตัว · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 11
- declaration --final: DOCCFG PASS (registry ไม่ชน · PPO) · NTF PASS · DOA PASS (print_config) · MDOC WARN (G04 taxonomy_def_id ว่าง · G09 doa pending · function_code F01 ชั่วคราว) → คัดลง FRD_F-TMP-005_Pack/declarations/
- 2026-10-10 05:58 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · declaration --final PASS (mdoc WARN)
- แก้ข้อความหลงจากโครงเดิมใน feature.html (ระหว่างขั้น 8): ผลลัพธ์แท็บลายเซ็น "ปิดใบสรุปประจำเดือน (ไม่ตัดสต็อก)" → "ปิดรายงานสอบทาน (ไม่ปิด/ยกเลิก PR-PO)" · แถบรอ "ผู้อนุมัติใบนี้" → "ผู้มีอำนาจอนุมัติรายงานนี้" · เตือนเกินแถว PDF Preview → audit FAIL 0 · smoke 47/47 ซ้ำ

## ขั้น 8 · UI Brief → test case AI → UAT
- html-ui-brief: extract_anchors (vars 46 · z 26 · routes 0 (hash ผ่าน go/RT) · toast 11) → UI_BRIEF_F-TMP-005.md (_build/make_brief.py) · brief_check PASS (FAIL 0 · WARN 0)
- ai-testcase-md-generator: testcases-F-TMP-005.md 64 เคส / 123 step · tc_lint ERROR 0 · Ledger (AC 15/15 · BR 19/20 · VR 12/12 · EC 10/11 · error 23/23 · permission 14/14 · XT 4/4 · DEC 16/16)
- verify_anchors.py: เครื่อง workspace ไม่มี browser → รันด้วย Chromium ใน container ของ agent (ไอคอน offline) · รอบแรก MISSING 3 (หัว modal ที่ประกอบสด + ☑ ใน iframe PDF) → ปรับถ้อยคำ → DOM 184 · SOURCE 49 · PATTERN 11 · DATA 84 · MISSING 0 (reports/anchors.json)
- qa-friendly: cases.json Lite 51 เคส / 71 step · lite_audit หายเงียบ 0 (drop ledger 13) --stamp · [NO-BROWSER] ข้าม capture.py → shots_b64.json ว่าง {} · build testcase-F-TMP-005.html
- 2026-10-10 06:13 · ขั้น 8 → done · brief_check PASS · tc_lint ERROR 0 (64 เคส) · verify_anchors MISSING 0 (Chromium container) · lite_audit หายเงียบ 0 · [NO-BROWSER] capture ข้าม
