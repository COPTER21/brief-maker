# RUN_LOG — F-NEW ใบเคลียร์เงินทดรองจ่าย (REQ-NEW)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · อ่านฟอร์ม (2026-10-06)
- ต้นฉบับ: FM-FIN-02.xlsx (Credence) → soffice → PDF → page-1.png · logo 1 รูป
- FORM_SPEC: 14 ช่อง · แถวซ้ำ 1 (10 แถว) · สูตร 4 · ค่าคงที่ 2 · ลายเซ็น 4 · anomalies 4 → form_spec_check ERROR 0
- REQ/F-code ยังไม่มี → ใช้ REQ-2569-0000 / F-NEW ชั่วคราว (impact_summary ต้องการรูปแบบ REQ-ตัวเลข)
- ⚠️ check-skills: doccfg/doa/mdoc/ntf declaration เป็นรุ่นเก่า (ไม่มี *_tool.py) → ขั้น 3 ทำแบบมือ ไม่มีด่านอัตโนมัติ
- feature ใบเบิกเงินทดรองจ่าย (FM-FIN-01) ยังไม่มีใน FEATURE_REGISTRY → ถามใน gate
- 2026-10-06 07:41 · ขั้น 1 → done · FORM_SPEC 14 ช่อง · ERROR 0

## ขั้น 2 · gate (2026-10-06)
- user: "ประเมินตาม standard แล้วทำต่อได้เลย" → AI ตัดสินทุกหมวด · G2–G10 ติด AI-DEFAULT (ยืนยันในใบเซ็น)
- G1: ไม่เปลี่ยน config · ไม่ post ต่อ · FM-FIN-01 ไม่อยู่ในระบบ → F06/F11 ผู้ใช้กรอก
- รหัสชั่วคราว: REQ-2569-0000 · F-FIN-ACL · code ACL
- DECISIONS.lock 15 มติ → พร้อมเริ่มทำ
- 2026-10-06 07:44 · ขั้น 2 → done · 15 DEC · AI-DEFAULT 11

## ขั้น 3–4 · declaration ร่าง + แบบพิมพ์ (2026-10-06)
- DOA/NTF/DOCCFG ร่างแบบมือ (ไม่มี *_tool.py) — ไม่มีด่าน BLOCK อัตโนมัติ · MDOC mdoc_tool brief = WARN (taxonomy ว่าง · doa pending · function_code F01 รอยืนยัน)
- แบบพิมพ์: ฟอร์มเป็นตารางกรอบ → thai-doc v2 ไม่มี block → เพิ่ม R9 `.form-grid` ใน replica.css สำเนา (/home/claude/td) — เสนอเข้าสกิล v2.1
- parity IDENTICAL 4/4 · ทุกสถานะ 1 หน้า · ไม่มี {{}} · compare 0:0.72 = 0.66 PASS · ดู _states_sheet + compare_side แล้ว
- 2026-10-06 07:48 · ขั้น 3 → done · ร่างมือ DOA/NTF/DOCCFG · MDOC WARN
- 2026-10-06 07:48 · ขั้น 4 → done · parity 4/4 · compare 0.66

## ขั้น 5 · HTML Q-form (2026-10-06)
- ฐาน: references/form-archetype (_SOURCE ผ่าน e2e 21/21 ในเครื่องนี้) → แทน domain ACL ทั้งชุด
- แก้ระหว่างทาง: คำตัดสินขั้น 2 "ส่งกลับแก้ไข" ชนตัวตรวจปุ่ม "แก้ไข" (e2e S5) → เปลี่ยนเป็น "รับเคลียร์ / ไม่รับเคลียร์" ทั้ง HTML + print_config + data + DOA_BRIEF (render แบบพิมพ์ใหม่ parity 4/4)
- แก้ pageerror: modal approve/reject render ระหว่าง fade หลังสายรีเซ็ต → guard
- ด่าน: audit FAIL 0 (WARN 3 = เท่า baseline อ้างอิง) · e2e_standard 21/21 · prune_css −4.9 KB แล้วรันซ้ำผ่าน · e2e_domain 13/13 (สร้าง→ส่ง→อนุมัติเรียงขั้น→บล็อกสลิป→ไม่รับเคลียร์กลับร่าง→PDF parity HTML=Python)
- 2026-10-06 08:05 · ขั้น 5 → done · audit 0 · e2e 21/21 · domain 13/13
- 2026-10-06 08:05 · ขั้น 6 → doing
- 2026-10-06 08:13 · ขั้น 6 → done · user ok ไม่แก้

## ขั้น 6 · user review (2026-10-06) — ok ไม่แก้

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง (2026-10-06)
- BRD-FIN-ACL-001 Prebrief Mode (md + docx) · APPROVED (Lane)
- FRD FULL (pages 3 · states 4 · approval · money) 9 ไฟล์ + INDEX · frd_lint Section N: BLOCK 0 · WARN 1 (N3 false positive — เลข 5 ในหัวข้อ §5.x)
- declaration --final ทำมือ: ใส่ frd_ref FN-03/FN-05/FN-07/FN-09 · MDOC route แก้เป็น #/advance-clearing (WARN: taxonomy ว่าง · doa pending)
- 2026-10-06 08:17 · ขั้น 7 → done · BRD ✓ · FRD FULL · lint BLOCK 0

## ขั้น 8 · UI Brief → TC → UAT (2026-10-06)
- UI_BRIEF brief_check: FAIL 0 · WARN 0 (B1–B8 PASS · vars 47/47 · microcopy 98%)
- testcases-F-FIN-ACL.md: 59 เคส / 396 step · tc_lint ERROR 0 · verify_anchors MISSING 0 (DOM 425)
- UAT Lite: 43 เคส / 94 step · capture OK 29/29 · lite_audit หายเงียบ 0 (drop ledger 16) · build 4.1 MB · เปิดไม่มี pageerror
- 2026-10-06 08:28 · ขั้น 8 → done · brief 0 · tc 59 · uat 43

## ขั้น 9 · ตรวจรวม + แพ็ก (2026-10-06)
- manifest_scan 55 artifact · ซ้ำ 0 · consistency READY (BLOCK 0 · WARN 0 · PASS 12) — แก้ K6: BRD แยก DEC-12..15 รายข้อ
- เพิ่มเข้า 07_Print: PDF 4 สถานะ + states sheet + base_form_patch.css (= R9 .form-grid · เสนอเข้า thai-doc v2.1)
- 2026-10-06 08:28 · ขั้น 9 → done · READY 12/12

## แก้หลังส่ง v1.1 (2026-10-06) — ช่องลงชื่อ PDF dynamic ตาม DOA (user แจ้ง)
- เดิม: วนจาก signs[] แล้ว (จำนวนตาม chain) แต่แถวเดียว → 6 ขั้นช่องเบียด · คำตัดสินผูกลำดับขั้น · print_config fix doa_step:1/2
- ใหม่: sign_rows[].signs[] แถวละ ≤4 เฉลี่ย (7→4+3) · dense เมื่อขั้น >4 · `.signs-block` ไม่ตัดข้ามหน้า · คำตัดสินผูก role (print_config.decision_words.by_role) · ลบ doa_step:N fix
- ด่าน: parity 5/5 (+approved-6steps) · ทุกสถานะ 1 หน้า (สุดขั้ว 14 แถว+6 ขั้น = 2 หน้า บล็อกลงชื่อทั้งก้อนหน้า 2) · compare 0.66 · audit FAIL 0 · e2e 21/21 · domain 18/18 (D10 1/3/6 ขั้น) · frd_lint BLOCK 0 · brief_check 0 · tc 60 (TC-D06) · anchors MISSING 0 · UAT 44 เคส
- เอกสารที่แก้: form.tpl.html · base_form_patch.css · print_config · ACL_print-spec · feature.html · BRD v1.1 (BR-12) · FRD 01/03/05/06/07/INDEX · DOA_BRIEF §5.1 · UI_BRIEF · testcases · cases/QA_AUDIT
