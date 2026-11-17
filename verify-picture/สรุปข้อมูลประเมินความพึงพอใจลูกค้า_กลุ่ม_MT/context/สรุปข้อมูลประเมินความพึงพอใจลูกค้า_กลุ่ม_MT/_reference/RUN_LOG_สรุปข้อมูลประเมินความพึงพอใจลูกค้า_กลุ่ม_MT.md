# RUN_LOG — F-TMP-008 FM-SAL-07 แบบฟอร์มรายงานสรุปข้อมูล แบบประเมิณความพึงพอใจของลูกค้า MT (REQ-TMP-008)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · อ่านฟอร์ม (หมายเหตุ)
- ภาพหน้า: `_system/tools/to_image.py` (LibreOffice → PDF → pypdfium2) ฟอนต์ไทยไม่มีในเครื่อง → ตัวไทยในภาพเป็นกล่อง · ถ้อยคำยึด content.html + openpyxl · ตำแหน่ง/เส้น/สียึดภาพ (ภาพไม่ใช่หน้ากระดาษพิมพ์จริง — ห้ามใช้เทียบ layout 1:1)
- xlsx 1 ชีต "สรุปการประเมิณครั้งที่1" · print area A1:R37 A4 แนวนอน fit 1 หน้า · footer Doc.No.FM-SAL-07 Rev.00: 01/07/2569
- form.title = "สรุปข้อมูลประเมินความพึงพอใจลูกค้า กลุ่ม MT" (หัวฟอร์ม A1 แก้คำสะกด ประเมิณ→ประเมิน · ลุกค้า→ลูกค้า ตาม G5) · ชื่อคิวไม่เพี้ยน → ไม่ rename
- โครง: ตาราง 9 หัวข้อ × 15 ช่องทาง MT (คะแนน 1–5) · แถวรวม · แถว % (=รวม/45) · สถานะสี เขียว/เหลือง/แดง · มาตรฐาน 95% · ภาพรวมโดยสรุป 3 กลุ่ม · ข้อเสนอแนะ 4 บรรทัด · ผู้สรุป + วันที่ 2 ช่อง · **ไม่มีช่องผู้อนุมัติ**
- FORM_SPEC 20 ช่อง · form_spec_check ERROR 0 · ไม่มี PREBRIEF CMS → สร้าง PREBRIEF v2
- ข้อมูลส่วนบุคคล: B35 มีชื่อจริงพนักงาน (ผู้สรุป) → pdpa · ไม่ใช้เป็นตัวอย่าง · ชื่อช่องทาง = ชื่อบริษัทคู่ค้า (หัวคอลัมน์ของฟอร์ม ไม่ใช่บุคคล)
- content.html ย้ายไป orig/out/ (กัน scanner นับเป็น prototype)
- 2026-10-10 18:26 · ขั้น 1 → done · FORM_SPEC 20 ช่อง ERROR 0 · PREBRIEF v2

## ขั้น 2 · gate (unattended — AI-DEFAULT ทุกหมวด)
- G1: ไม่เปลี่ยนค่า/ไม่ส่งต่อ — เป็นรายงานสรุปผลประเมิน · คะแนนจากแบบประเมินลูกค้า MT ยังไม่ผูก → ผู้ใช้กรอกคะแนนเอง
- G2: **ไม่มีการอนุมัติ** — กระดาษไม่มีช่องลงชื่อผู้อนุมัติ (มีแค่ผู้สรุปการประเมิณ Sales Manager) ตามนโยบาย "ค่าเริ่ม = จำนวนช่องลงชื่อผู้อนุมัติบนกระดาษ" = 0 · ผู้จัดทำ role-mgr-sales · ไม่ทำ DOA_BRIEF (doa_tool: ห้ามยัด DOA เข้า feature ที่ไม่มีอนุมัติ) · field DOA วางนิยามใน FRD 02/03
- G3: ค่าคงที่ (95% · 80% · คะแนนเต็ม 5 · หัวข้อ 9 ข้อ · ช่องทาง 15 · ป้าย/สี · ข้อความแนะนำ) อ่านจาก SalesConfig · % = รวม/คะแนนเต็ม ตามสูตรต้นฉบับ · เพิ่มสูตรรวมต่อช่องทางที่ขาด · สถานะ/สี/รายชื่อกลุ่มคำนวณแทนการพิมพ์มือ
- G4: หัวข้อ/ช่องทางคงที่ตาม config (snapshot ในใบ) · ข้อเสนอแนะไม่จำกัด PDF ขั้นต่ำ 4 บรรทัด
- G5: 1:1 แก้คำสะกด · G6: บล็อกผู้สรุป ข้อความ "ยืนยันสรุปในระบบ" ไม่ใช้ภาพ · G7: ไม่มีอนุมัติ · ยกเลิก owner+admin ร่าง/สรุปแล้ว เหตุผลบังคับ · แก้หลังสรุปไม่ได้
- G8: เจ้าของ · Sales admin เห็นทั้งหมด · G9: ออกเลขตอนบันทึกครั้งแรก รหัส MTS (registry ไม่ชน · SES กันให้ J007) · G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- 2026-10-10 18:27 · ขั้น 2 → done · 20 มติ · AI-DEFAULT ทุกหมวด ยกเว้น VALID

## ขั้น 3 · declaration ร่าง
- DOA: ไม่ทำ — doa_tool init ตอบ "ไม่มีการอนุมัติ (doa.required=false) — ไม่ต้องทำ DOA_BRIEF" (DEC-03) · field approver_role/approved_by/approval_chain = null + `TODO: DOA engine` นิยามใน FRD 02/03
- NTF: mts_low_channel (final และมีช่องทาง < 80%) → role-mgr-bu + Sales admin · mts_cancelled (admin ยกเลิกใบ final) → owner · ตัด mts_over_limit_approved (ไม่มี approved) · brief PASS
- DOCCFG/MDOC ทำหลังขั้น 4 (ต้องใช้ print_config)
- 2026-10-10 18:27 · ขั้น 3 → done · ntf PASS · doa ไม่มี (DEC-03) · doccfg/mdoc ทำในขั้น 4

## ขั้น 4 · แบบพิมพ์ + doccfg/mdoc
- แบบพิมพ์ Replica R9 ตารางกรอบ + R10 **2 หน้า** (หน้า 1 ตารางคะแนน 2 ช่วง ช่วงละ 8 ช่องทาง + มาตรฐาน/คำอธิบายผล · หน้า 2 ภาพรวมโดยสรุป + ข้อเสนอแนะ + บล็อกผู้สรุป + วันที่) · ฟอนต์ 8.5pt (≥ 8pt)
- ต้นฉบับ A4 แนวนอน แต่ build_html (base.css) รองรับ A4 แนวตั้งเท่านั้น และห้ามแก้สคริปต์/ห้าม style ใน body → ออกแบบแนวตั้ง แบ่งตาราง (บันทึกใน print-spec §7)
- 5 สถานะ: draft · final · final-allpass · cancelled · long-12recs (ไม่มี ไม่อนุมัติ / DOA 6 ขั้น เพราะไม่มีอนุมัติ DEC-03)
- parity_check IDENTICAL 5/5 · render_doc --strict 5/5 ไม่มี {{}} หลง · build_html 5 สถานะ + FM-SAL-07_template.html
- [NO-BROWSER] ข้าม render_pdf.py (ส่วน PDF/นับหน้า/ภาพของ render_states.py) — ประเมินความสูง: หน้า 1 ≈ 220mm · หน้า 2 ≤ 200mm (พื้นที่ 269mm) → คาด 2 หน้าทุกสถานะ ต้องยืนยันบนเครื่องที่มี browser
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ final.pdf) · ไม่มี _states_sheet.png
- DOCCFG: MTS · brief --registry PASS (ไม่ชน) · MDOC: brief WARN (G04 ยังไม่มี taxonomy_def_id) · doa: none · DOA validate ข้าม (ไม่มี X.doa.yaml — DEC-03)
- ไฟล์ body ชั่วคราวอยู่ใน print/out/_body
- 2026-10-10 18:31 · ขั้น 4 → done · R10 2 หน้า · parity 5/5 · [NO-BROWSER] ไม่ render PDF/compare

## ขั้น 5 · HTML (html-generator v9.4 · Q-form)
- feature.html ประกอบจาก canonical `references/form-archetype` (shell + CSS + BASE-KIT) + `templates/blocks/be-datepicker` + script เฉพาะเอกสาร (`.build/app1–5.js` · `.build/build.py`) — เทียบ GOLDEN_SKELETON + U1–U28 ก่อน build (ใช้โครงเดียวกับ J002 ที่ผ่านด่าน)
- wizard 4 ขั้น (คะแนนรายช่องทาง › ภาพรวมและข้อเสนอแนะ › เอกสารแนบ › ตรวจสอบและยืนยัน) · ตารางคะแนน 9×15 พิมพ์แล้วรวม/%/สถานะอัปเดตสด · วันที่ใช้ bedateHTML (Rule #114)
- ไม่มีอนุมัติ (DEC-03): ปุ่ม "ยืนยันสรุป" แทนส่งอนุมัติ · audit Q-form บังคับ MOCK_DOA_RESOLVED / slot-row / renderSignProgress (กติกาสคริปต์คิดว่าทุก Q-form มีอนุมัติ) → ใส่ DOA hook 0 ขั้น (steps []) + slot ผู้สรุป 1 ช่อง + คอลัมน์ลายเซ็น 0/1–1/1 — ไม่ได้เพิ่มขั้นอนุมัติจริง
- audit.sh FAIL 0 · WARN 4 (Rule #21 / #40 .uc-email / Token font-size — มาจาก shell+kit canonical · #109 canSee ไม่มีคำ draft เพราะไม่มีผู้อนุมัติ → เห็นเฉพาะเจ้าของ + admin) · self_audit PASS · prune_css ตัด 87 rule แล้วรัน audit/self_audit/smoke ซ้ำ ผ่าน
- smoke (node vm, ไม่ใช้ browser): renderPage × 4 persona · ทุกใบที่เห็น × 4 แท็บ · wizard 4 ขั้น + validate (ว่าง/คะแนน 7/บางส่วน/ลำดับวันที่/ไม่มีข้อเสนอแนะ) · modal ยืนยันสรุป/ยกเลิก/ทิ้ง → error 0 · E01 เห็น R1,R3,R4,R6,R8,R9 · E03 เห็น R2,R5,R7 · E05 เห็นทั้งหมด · E02 ไม่เห็น
- parity JS (docPrintData + tplRender) ↔ render_doc.py IDENTICAL 9/9 seed · ไม่มี {{}} หลง
- [NO-BROWSER] ข้าม e2e_standard.py · ข้าม render-check.py — ต้องรันบนเครื่องที่มี browser
- U1–U28: U1✓ U2✓ U3✓ U4✓ U5✓ U6✓ U7✓ U8✓ U9✓ U10✓ U11✓(kit) U12✓ U13✓(ผู้สรุป 1 ช่อง) U14✓(wizard) U15✓ U16 n/a(ไม่มีลบ · ยกเลิกมีเหตุผล) U17✓ U18✓ U19✓ U20✓(ไม่มี tabs) U21✓(kit WARN token) U22✓ U23✓ U24✓ U25✓ U26–U28 n/a(ไม่มีหน้า config)
- 2026-10-10 18:38 · ขั้น 5 → done · audit FAIL 0 · self_audit PASS · [NO-BROWSER] ไม่รัน e2e
- 2026-10-10 18:38 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 6 · ข้าม (unattended — ให้คนดูจาก _BATCH_REPORT)

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-008.md/.docx (Prebrief Mode · Lane) — AI Review: APPROVED (C16 WARN ไม่มี Registry entry เพราะ F-TMP ชั่วคราว)
- FRD_F-TMP-008_Pack (00–07 + INDEX + declarations/) · ไม่มีอนุมัติ → นิยาม field DOA (approval_required=false · approver_role/approved_by/approval_chain/doa_ref = null · TODO: DOA engine) ไว้ใน 02 §2.3 + 03 FN-03 · 04/05 ไม่ใช้คำ approval_chain/อนุมัติ (กัน K7 false-positive)
- frd_lint Section N: BLOCK 0 · WARN 0 · PASS 15 (แก้ WARN N3 "× 100" ใน BR-03 → "แสดงเป็นร้อยละ")
- declaration --final: DOCCFG PASS (registry ไม่ชน · frd_ref FN-03 · snapshot approved_final = ฉบับยืนยันสรุป FN-04) · NTF PASS (frd_ref FN-04/05/08) · MDOC WARN (G04 taxonomy_def_id — ตามคาด) · DOA ไม่มี (DEC-03)
- 2026-10-10 18:44 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 WARN 0 · declaration --final PASS

## ขั้น 8 · UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-008.md (§0–§13 · สกัดจาก feature.html + inventory) · brief_check: PASS · FAIL 0 · WARN 0
- testcases-F-TMP-008.md: 51 เคส · 177 step · tc_lint ERROR 0 · Coverage AC 13/13 · BR 15/15 · VR 6/6 · EC 11/11 · TC-D 6/6 · DEC 20/20
- [NO-BROWSER] ข้าม verify_anchors.py (anchor เขียนจากข้อความใน feature.html โดยตรง) · ข้าม capture.py (ไม่มีภาพหน้าจอ · regionKey ว่าง)
- UAT Lite: cases.json 19 เคส · drop ledger 32 (QA_AUDIT_F-TMP-008.md) · lite_audit หายเงียบ 0 · --stamp แล้ว · build testcase-F-TMP-008.html (ไม่มีภาพ)
- 2026-10-10 18:53 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 · lite_audit หายเงียบ 0 · [NO-BROWSER] ข้าม verify_anchors/capture
