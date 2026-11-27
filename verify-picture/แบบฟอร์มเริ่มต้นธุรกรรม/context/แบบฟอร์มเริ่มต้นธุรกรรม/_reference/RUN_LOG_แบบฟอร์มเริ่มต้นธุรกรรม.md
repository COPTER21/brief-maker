# RUN_LOG — F-TMP-001 FM-IVM-01 แบบฟอร์มเริ่มต้นธุรกรรม (REQ-TMP-001)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · อ่านฟอร์ม (หมายเหตุ)
- ภาพฟอร์ม: `_system/tools/to_image.py` → LibreOffice → PDF → page-1.png (หน้ากระดาษจริง 1 หน้า A4 ตั้ง แต่ฟอนต์ไทยในภาพไม่แสดง → ถ้อยคำยึด content.html + openpyxl · ตำแหน่ง/เส้นยึดภาพ)
- FORM_SPEC: 18 ช่อง (ระบบ 1 · กรอก 13 · ระบบใส่ 4) · แถวซ้ำ 1 (ประวัติการแก้ไข) · ลายเซ็น 3 (ผู้จัดทำ/ผู้ตรวจสอบ/ผู้อนุมัติ-รับทราบ) · ERROR 0
- form.title = "แบบฟอร์มเริ่มต้นธุรกรรม" (หัวฟอร์ม C1) · Doc No. FM-IVM-01 Rev.00 : 01/07/2569 (footer) · ชื่อชีต INV-FM-01 ขัดกับ footer → ยึด footer
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC · ไม่มีข้อมูลส่วนบุคคลในไฟล์ (ฟอร์มเปล่า)
- แก้บั๊กสคริปต์: `impact_summary.py` regex REQ รับแค่ตัวเลข → อ่าน REQ-TMP-xxx ไม่ได้ → แก้เป็น `REQ-[A-Z\d-]+` (ไม่กระทบ REQ ตัวเลข)
- ไม่มี module ลงทุนใน FEATURE_REGISTRY → เสนอ module ใหม่ "บริหารการลงทุน (IVM)" ใน _BATCH_REPORT · DOA ใช้ module `finance` ชั่วคราว
- 2026-10-10 23:49 · ขั้น 1 → done

## ขั้น 2 · gate (unattended — AI-DEFAULT ทุกหมวด ตาม unattended-policy)
- G1 ไม่เปลี่ยนค่า/ไม่ส่งต่อ — ฟอร์มเป็นบันทึกเริ่มต้นธุรกรรม ไม่มีคำสั่งให้ปรับข้อมูลระบบอื่น
- G2 dynamic 2 ขั้นตามช่องลงชื่อบนกระดาษ: ผู้ตรวจสอบ (ผจก.ฝ่ายบริหารการลงทุน) → role-line-manager · ผู้อนุมัติ/รับทราบ (รอง กก.ผจก./กก.ผจก.) → role-gm (ใกล้สุดใน contract) · ไม่มีวงเงิน
- G3 ไม่มีสูตร/ค่าคงที่ · G4 ประวัติการแก้ไขไม่จำกัด PDF ขั้นต่ำ 2 แถว · G5 1:1 (แถวป้ายว่างไม่ทำเป็นช่อง)
- G6 1 ช่อง/ขั้น DOA ข้อความ "พิจารณาในระบบ" · G7 ไม่อนุมัติกลับร่างเลขเดิม ยกเลิกได้เจ้าของ+admin เหตุผลบังคับ
- G8 เจ้าของ/ผู้อนุมัติหลังส่ง/admin ฝ่ายเห็นทั้งหมด · G9 ออกเลขตอนบันทึกครั้งแรก รหัส IVMA (FM-IVM-01 → 01=A กันชนกับ FM-IVM อื่น) · G10 แนบไฟล์ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- decisions_lock: 14 มติ "พร้อมเริ่มทำ" · tag → AI-DEFAULT 11 มติ
- 2026-10-10 23:49 · ขั้น 2 → done
- ขั้น 3: doa IVMA (finance ชั่วคราว · 2 ขั้น role-line-manager → role-gm) PASS · ntf 2 event (ivma_cancelled · ivma_responsible_assigned) PASS · แก้ on_reject draft→back_to_draft ตาม doa_tool แล้วล็อกใหม่

## ขั้น 4 · แบบพิมพ์ Replica
- R9 ตารางกรอบ · ออกแบบ 2 หน้าตาม R10 (ข้อความยาว 6 ช่อง + DOA dynamic + ประวัติแก้ไขไม่จำกัด → 1 หน้าต้องบีบ < 8pt) · ตัดหน้าก่อน "การตรวจทาน / อนุมัติ" · หัวตารางซ้ำ · "หน้า 1/2"
- data 5 สถานะ (draft · approved · rejected · long-12revisions · approved-doa6steps) ข้อมูลสมมติทั้งหมด · parity IDENTICAL 5/5 · render_doc --strict + build_html ไม่มี {{}} หลง
- [NO-BROWSER] ข้าม render_states.py (เรียก render_pdf.py) — ยังไม่ได้ PDF/จำนวนหน้า/_states_sheet.png
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ PDF สถานะ approved)
- doccfg IVMA (registry ไม่ชน) PASS · mdoc WARN (taxonomy_def_id ว่าง · doa pending · function_code F01 ชั่วคราว) · doa validate --print-config PASS
- 2026-10-10 23:53 · ขั้น 3 → done
- 2026-10-10 23:53 · ขั้น 4 → done · NO-BROWSER: ยังไม่ render PDF/compare

## ขั้น 5 · HTML Q-form
- โครง shell/CSS/helper จาก form-archetype reference (html-generator-v9) + app ใหม่ทั้งหมดของ IVMA (ข้อมูลสมมติ) + be-datepicker (#114) + form.tpl.html ฝังเป็น IVMA_TPL (parity JS↔Python IDENTICAL)
- เทียบ GOLDEN_SKELETON v9.4: ตัด stat cards → badge ใน sub · kebab ⋮ · คน = วงกลมรูปคน SVG (.emp-av) · drawer header lean (sub = วันที่เริ่มโครงการ) · backdrop onmousedown (drawer + modal) · ไม่มี page tabs (ชุดข้อมูลเดียว)
- U1–U28: U1✓ U2✓ U3✓ U4✓ U5✓ U6✓(page-size 25/50/100) U7✓ U8✓ U9✓ U10✓ U11✓ U12✓ U13✓ U14✓(wizard 3 ขั้น Q2) U15✓ U16 n/a(ไม่มีลบ — ยกเลิกเอกสารแทน) U17✓ U18✓ U19✓ U20✓(ไม่มี tabs) U21✓ U22✓ U23✓ U24✓ U25✓ U26–U28 n/a(ไม่มีหน้าตั้งค่า)
- audit.sh FAIL 0 (WARN 3 เดียวกับ reference: w-/h- class · .uc-email · font-size px) · self_audit PASS · prune_css ตัด 78 rule · node --check ผ่าน
- smoke test แบบไม่มี browser (node + DOM stub): 29/29 — สิทธิ์ G8 · flow ส่ง/ส่งกลับเป็นร่างเลขเดิม/ส่งใหม่=ฉบับ 01/อนุมัติ 2 ขั้น · DOA 6 ขั้น = 7 แถวลงนาม · DOC.active=false
- [NO-BROWSER] ข้าม e2e_standard.py · [NO-BROWSER] ข้าม render-check.py
- 2026-10-11 00:03 · ขั้น 5 → done · audit FAIL0 · self_audit PASS · NO-BROWSER ข้าม e2e
- 2026-10-11 00:03 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-001.md/.docx (Prebrief Mode · Lane) — AI Review C01–C23 + PE01–PE05 ผ่าน → APPROVED · ตัวชี้วัด = OQ-01 (ไม่แต่งตัวเลข)
- FRD_F-TMP-001_Pack (00–07 + INDEX + declarations/) · 07 = DECISIONS.lock 14 DEC
- frd_lint: BLOCK 0 · WARN 0 · PASS 12 · ใส่ frd_ref ตามที่ lint พิมพ์
- declaration --final: doccfg IVMA PASS (registry ไม่ชน) · ntf PASS · doa PASS · mdoc WARN (taxonomy_def_id ว่าง · doa pending) — อธิบายได้ ไม่ BLOCK
- 2026-10-11 00:08 · ขั้น 7 → done

## ขั้น 8 · UI Brief → test case → UAT
- UI_BRIEF_F-TMP-001.md (AS-BUILT §0–§13 · สกัดจาก inventory) · brief_check FAIL 0 · WARN 0
- testcases-F-TMP-001.md 29 เคส / 68 step · tc_lint ERROR 0
- [NO-BROWSER] ข้าม verify_anchors.py · [NO-BROWSER] ข้าม capture.py (เอกสาร UAT build แบบไม่มีภาพ)
- cases.json (Lite 29 เคส · drop 0) · lite_audit หายเงียบ 0 + stamp · testcase-F-TMP-001.html (build ไม่มีภาพ)
- 2026-10-11 00:11 · ขั้น 8 → done · NO-BROWSER: ข้าม verify_anchors/capture
