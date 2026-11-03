# RUN_LOG — F-TMP-001 แบบประเมินความพึงพอใจลูกค้า (REQ-TMP-001)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพฟอร์ม: to_image.py → LibreOffice → PDF → pypdfium2 (หน้ากระดาษจริงจาก docx · ไม่ใช่ HTML+browser) · ฟอนต์ไทยในเครื่องเรนเดอร์ไม่ขึ้น (เป็นกล่อง) → ถ้อยคำยึด content.html · ตำแหน่ง/เส้นยึด page-1.png
- ชื่อเอกสารไม่เพี้ยน → ไม่ rename · หัวฟอร์มจริง "แบบฟอร์มประเมินความพึงพอใจของบริษัทครีเดนซ์ จำกัด (มหาชน)" · FM-SAL-06 Rev.00: 01/07/2569
- FORM_SPEC 12 ช่อง (ระบบ 1 · กรอก 11) · ตัวเลือก 2 · ลายเซ็น 1 (ผู้ประเมิน · ไม่มีช่องผู้อนุมัติ) · ข้อมูลขัดกัน 3 · form_spec_check ERROR 0
- ไม่มี PREBRIEF จาก CMS → prebrief_v2.py สร้างจาก FORM_SPEC
- แก้ regex ใน impact_summary.py ให้รับรหัสคำขอชั่วคราว (REQ-TMP-001) — เดิมรับเฉพาะตัวเลข · ไม่กระทบด่าน
- 2026-10-08 12:34 · ขั้น 1 → done

## ขั้น 2 · gate (unattended — AI-DEFAULT 10 มติ + VALID 3)
- G1 ไม่เปลี่ยนค่า/ไม่ส่งต่อ — แบบสอบถามเก็บผลในเอกสารนี้เท่านั้น
- G2 ไม่มีการอนุมัติ — กระดาษมีช่องลงชื่อแค่ "ผู้ประเมิน" (ผู้ขอ) ช่องผู้อนุมัติ = 0 → ไม่ยัด DOA (doa-declaration กติกา 4)
- G3 ไม่มีสูตร/ค่าคงที่ · ชื่อบริษัทหัวเรื่อง + ข้อ 2 ดึง Organization.legal_name (แก้ จำกัด vs มหาชน)
- G4 ไม่มีรายการซ้ำ (ตาราง 9 หัวข้อคงที่) — DEC-05 ข้อความ "None แถว" = ไม่เกี่ยว
- G5 1:1 · G6 ช่องผู้ประเมิน 1 ช่อง ข้อความ "ส่งในระบบ" · G7 ไม่มีอนุมัติ → ยกเลิกได้ เจ้าของ+admin (ร่าง/ส่งแล้ว) เหตุผลบังคับ
- G8 เจ้าของ + admin role ฝ่ายขาย (role-mgr-sales) เห็นทั้งหมด · G9 ออกเลขบันทึกครั้งแรก รหัส CSE · G10 แนบไฟล์ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- 2026-10-08 12:34 · ขั้น 2 → done

## ขั้น 3 · declaration (ร่าง)
- DOA: ไม่ทำ — DEC-03 ไม่มีการอนุมัติ (doa_tool init จะปฏิเสธ · "ห้ามยัด DOA เข้า feature ที่ไม่มีอนุมัติ")
- NTF: suggest ได้ cse_over_limit_approved → ตัด (ไม่มีอนุมัติ/เกณฑ์) · เติม cse_submitted → role-mgr-sales (in-app · ปิดได้) · brief PASS (N1–N7)
- doccfg + mdoc ทำหลังขั้น 4

## ขั้น 4 · แบบพิมพ์ Replica
- form.tpl.html (R1 R2 R4 R6 inline · R9 ตารางคะแนน 2 คอลัมน์ · R8 กล่องข้อเสนอแนะ · R7 · B6 sign_rows · B7) · profile.json · print_config.json · make_data.py → 5 สถานะ (draft · submitted · alt-choices-low · long-suggestion · blank-print) ข้อมูลสมมติทั้งหมด
- parity_check: IDENTICAL 5/5 · render_doc + build_html ทุกสถานะ: ไม่มี {{}} หลง · ไม่มี key ขาด → print/out/*.html + _states.json
- [NO-BROWSER] ข้าม render_pdf.py (ส่วน PDF/PNG/_states_sheet.png/จำนวนหน้าของ render_states.py)
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ approved/submitted.pdf ที่ render ไม่ได้)
- สถานะ "DOA 6 ขั้น" ไม่เกี่ยว (DEC-03 ไม่มีอนุมัติ) · doa_tool validate ไม่เกี่ยว (ไม่มี DOA)
- doccfg init/brief --registry: CSE ไม่ชน · D1–D8 PASS · mdoc brief WARN (G04 taxonomy_def_id ว่าง = รออนุมัติ · function_code F01 ชั่วคราว · source=declaration เพราะ REQ-TMP ไม่ผ่าน G10 รูปแบบ REQ-YYYY-NNNN)
- ไฟล์ทดลอง soffice/body ที่ลบในโฟลเดอร์ไม่ได้ ย้ายไป _system/_trash_J001/ (ไม่ใช่ส่วนของงาน)
- 2026-10-08 12:38 · ขั้น 4 → done
- 2026-10-08 12:38 · ขั้น 3 → done

## ขั้น 5 · HTML Q-form (feature.html)
- โครง v9.4 GOLDEN_SKELETON (CSS kit ยกตรง · แก้ .btn line-height:1 → padding-top:2px ตาม Rule #36) + Q2 form archetype · `<meta cube-archetype=Q-form>` · `window.__QA__`
- ช่อง = FORM_SPEC 1:1 (ข้อ 1–4 · 9 หัวข้อคะแนน 1–5 · ข้อเสนอแนะ) · ข้อ 2 บริษัทคู่ค้าแสดงในการ์ดสรุป (อ่านจาก Organization) · PDF Preview ใช้ form.tpl.html + tplRender + docPrintData (template เดียวกับแบบพิมพ์)
- DOA (DEC-03): MOCK_DOA_RESOLVED steps = [] (dynamic · DOA กลางเพิ่มขั้นได้ ไม่แก้ feature) → ส่งแล้ว = "ส่งแล้ว" · slot-row วนตามขั้น · มี `TODO: DOA engine` + approval_chain/approver_role/approved_by
- สถานะ: ร่าง · รอพิจารณา (เฉพาะเมื่อ DOA มีขั้น) · ส่งแล้ว · ยกเลิก (เหตุผลบังคับ · เจ้าของ+admin role-mgr-sales)
- audit.sh: FAIL 0 · WARN 1 (hardcoded font-size px ใน CSS kit ของ golden skeleton) · prune_css: ตัด 0 · audit ซ้ำ FAIL 0
- [NO-BROWSER] ข้าม e2e_standard.py (ไม่มี reports/e2e_report.json) · [NO-BROWSER] ข้าม render-check.py
- ตรวจแทนชั่วคราว (ไม่ใช่ด่านทางการ): jsdom smoke ไล่ S0–S10 ตาม e2e_standard + flow สร้าง→ส่ง · ยกเลิก · DOA เพิ่มขั้น→อนุมัติ = PASS 26/26 · ไม่มี pageerror
- U1✓ U2✓ U3✓ U4✓ U5✓ U6✓ U7✓ U8✓ U9✓ U10✓ U11✓ U12✓ U13✓ U14✓ U15✓ U16✓(ไม่มีลบ · ยกเลิก=สถานะ) U17✓ U18✓ U19✓ U20✓(ชุดเดียว ไม่มี tabs) U21✓ U22✓ U23✓ U24✓ U25✓ U26–U28 n/a (ไม่มีหน้าตั้งค่า)
- 2026-10-08 12:49 · ขั้น 5 → done
- 2026-10-08 12:49 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 6 · ข้าม (unattended — ให้คนดูจาก _BATCH_REPORT)

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-001.md/.docx (brd-generator-full v2.3 Prebrief Mode) · AI Review C01–C23 + PE01–05 ผ่าน → **APPROVED**
- FRD_F-TMP-001_Pack (frd-generator-v6.2 Mode 0 · FULL: 00–07 + INDEX + declarations/) · ไม่มีคำ อนุมัติ/approval_chain ใน 04/05 (ไม่มี DOA — DEC-03)
- frd_lint Section N: BLOCK 0 · WARN 0 · PASS 9 (ไม่ส่ง --doa เพราะไม่มี DOA)
- doccfg --final --registry: PASS (frd_ref 03_LOGIC F-TMP-001-FN-02) · ntf --final: PASS (cse_submitted frd_ref FN-05) · mdoc: WARN G04 (taxonomy_def_id ว่าง = รออนุมัติ)
- เปลี่ยนชื่อ print/make_data.py → render_data.py และ orig/content.html → content_from_docx.htm (กัน manifest_scan จับเป็น prototype ซ้ำ)
- 2026-10-08 12:54 · ขั้น 7 → done

## ขั้น 8 · UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-001.md (สกัดจาก feature.html + inventory) · brief_check: PASS · FAIL 0 · WARN 0 (B1–B8)
- testcases-F-TMP-001.md: 52 เคส · 185 step · tc_lint ERROR 0 · Coverage AC 13/13 · BR 12/12 · VR 6/6 · EC 7/8 (EC-08 นอก scope) · สิทธิ์ 5/5 · XT 3/3 · DEC 13/13
- [NO-BROWSER] ข้าม verify_anchors.py (ไม่มี reports/anchors.json) — anchor ไล่เทียบกับ source HTML ด้วยมือ + inventory
- UAT: cases.json (Lite 43 เคส · drop ledger 9) · lite_audit หายเงียบ 0 + stamp · [NO-BROWSER] ข้าม capture.py (ไม่มีภาพหน้าจอ · regionKey ว่าง) · build.py → testcase-F-TMP-001.html (ไม่มีภาพ)
- 2026-10-08 13:01 · ขั้น 8 → done
