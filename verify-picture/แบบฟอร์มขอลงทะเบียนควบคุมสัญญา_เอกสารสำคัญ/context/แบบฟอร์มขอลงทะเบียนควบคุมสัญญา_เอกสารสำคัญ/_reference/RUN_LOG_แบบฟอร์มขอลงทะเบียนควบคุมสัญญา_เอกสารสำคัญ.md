# RUN_LOG — F-TMP-009 FM-AGM-01 แบบฟอร์มลงทะเบียนควบคุมสัญญา (REQ-TMP-009)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพหน้า: `to_image.py` ใช้ LibreOffice → PDF → pypdfium2 (ได้ SAMPLE.pdf จริง 1 หน้า) · แต่เครื่องไม่มีฟอนต์ไทย → ภาพเป็นกล่อง □ → ถ้อยคำยึด content.html + document.xml/footer1.xml ของ docx · ตำแหน่ง/เส้นยึดภาพ (ไม่ใช้เทียบ layout 1:1)
- Doc. No. FM-AGM-01 · Rev.00 : 01/07/2569 อยู่ใน footer ของ docx · โลโก้บริษัทลูกค้า (Credence) ที่หัวกระดาษ → ระบบใช้โลโก้ Organization
- ฟอร์มเปล่า ไม่มีข้อมูลตัวอย่าง/ข้อมูลส่วนบุคคล · ชื่อคู่สัญญา ติด pdpa
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC (--req REQ-TMP-009 --module AGM)
- FEATURE_REGISTRY (4_knowledge/project_docs) ไม่มี module/feature บริหารสัญญา → feature ใหม่ (เสนอใน _BATCH_REPORT)
- content.html ย้ายไป orig/out/ แล้ว (กัน scanner นับเป็น prototype)
- 2026-10-10 18:56 · ขั้น 1 → done

## ขั้น 2 · เหตุผลรายหมวด (unattended — AI-DEFAULT ทุกหมวด)
- G1: ฟอร์มเป็นทะเบียนคุมสัญญา ไม่เปลี่ยนค่าระบบอื่น ไม่ส่งต่อ (post_to [])
- G2: กระดาษมีผู้ลงนาม 2 จุดหลังผู้ขอ → dynamic 2 ขั้น: role-line-manager (หัวหน้า/ผู้จัดการ) → role-compliance (แทน "ผู้เชี่ยวชาญด้านบริหารสัญญา" ชั่วคราว ไม่มี role ตรงใน DOA master → OQ) · ไม่มีวงเงิน
- G3: ไม่มีสูตร/ค่าคงที่ · เพิ่ม validation วันที่สิ้นสุด ≥ เริ่มต้น และสาเหตุบังคับเมื่อเลือกแก้ไข
- G4: ไม่มีแถวซ้ำ
- G5: 1:1 · ช่อง 4 เก็บ 2 ค่าแสดงบรรทัดเดียว
- G6: แถวล่าง 1 ช่องต่อขั้น DOA · ข้อความ "พิจารณาในระบบ"
- G7: ไม่อนุมัติ → กลับร่างเลขเดิม · ยกเลิกได้ เจ้าของ + admin (ร่าง/รออนุมัติ) เหตุผลบังคับ
- G8: เจ้าของ · ผู้อนุมัติหลังส่ง · admin ฝ่ายบริหารสัญญาเห็นทั้งหมด
- G9: เลขที่ออกตอนบันทึกครั้งแรก · รหัส CTR (ไม่ชน registry) · เลขทะเบียนควบคุม (F07) ออกเมื่อผู้ดูแลสัญญารับลงทะเบียน
- G10: แนบไฟล์ ✓ (สำเนาสัญญา) · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗
- 2026-10-10 18:57 · ขั้น 2 → done
- ขั้น 3: แก้ decisions G7 on_reject draft→back_to_draft (doa_tool BLOCK G5) แล้วล็อกใหม่ + tag
- 2026-10-10 18:58 · ขั้น 3 → done

## ขั้น 4 · แบบพิมพ์
- Replica เส้นประ R1–R8 + B6 sign_rows + กล่องผู้ดูแลสัญญา · 5 สถานะ (draft · approved · rejected · long-text · approved-doa6steps) · parity IDENTICAL 5/5 · ไม่มี {{}} หลง · ไม่มี key ขาด
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py ส่วน PDF/นับหน้า/_states_sheet.png) — ทำ render_doc + build_html แทน ได้ HTML ทุกสถานะใน print/out/
- [NO-BROWSER] ข้าม compare_original.py (ไม่มี approved.pdf)
- ต้นฉบับ 1 หน้า · ออกแบบ 1 หน้า (--max-pages 1) · ประเมินความสูงเนื้อหา ~230mm — ต้องยืนยันจำนวนหน้าบนเครื่องที่มี browser
- doccfg CTR (registry ไม่ชน) PASS · mdoc WARN (taxonomy_def_id ว่าง · doa pending — อธิบายได้) · doa validate --print-config PASS · ntf PASS
- OQ: เลข "ทะเบียนควบคุมเลขที่" ใช้ sequence แยกจากเลข CTR หรือไม่ (ยังไม่ประกาศ doc_type แยก)
- 2026-10-10 19:00 · ขั้น 4 → done

## ขั้น 5 · HTML Q-form
- ฐาน: references/form-archetype/_SOURCE_form-request-reference.html (shell/CSS/generic) + JS feature เขียนใหม่ตามโดเมน · เทียบ GOLDEN_SKELETON + U1–U28 ก่อน build
- audit.sh FAIL 0 · WARN 3 (ติดมาจาก reference: Rule #21 ใน comment/helper กลาง · .uc-email CSS ไม่ได้ใช้ · font-size px ของ shell) · self_audit PASS (แก้ spacing 14→16 · z → var(--z-popover) · ข้อความ #114) · prune_css ตัด 65 rule แล้วรันซ้ำผ่าน
- [NO-BROWSER] ข้าม e2e_standard.py และ render-check.py — ทดแทนด้วย smoke test jsdom (node) ไล่ flow: list/visibility · 4 tabs · สร้าง→ส่ง→อนุมัติ E02→รับทราบ E05→ลงทะเบียน→รับต้นฉบับ · ส่งกลับเป็นร่าง · ยกเลิก · แก้ไขร่าง · ทำซ้ำ · DOA 6 ขั้น (7 ช่อง 2 แถว dense) · page-size · DOC.active=false → JS error 0 (บั๊กที่เจอ: renderModal หลังปิด modal อ่าน curStep ว่าง → แก้แล้ว)
- U1–U28: U1✓ U2✓ U3✓ U4✓ U5✓(ellipsis-vertical) U6✓(page-size 10/25/50 default 25) U7✓ U8✓ U9✓ U10✓ U11✓(ระยะจาก reference) U12✓ U13✓ U14✓(Q-form wizard 1290) U15✓(แก้ไขจาก view ปิด view ก่อน) U16–(ไม่มีลบ · ใช้ยกเลิกพร้อมเหตุผล) U17✓(วงกลม #111 + icon user) U18✓ U19✓(sub = ประเภท · ระยะสัญญา) U20–(ชุดข้อมูลเดียว ไม่มี tabs) U21✓(ตาม reference) U22✓(chips ≤3 ซ่อนค่า 0) U23✓ U24✓ U25✓(onmousedown) U26–U28 –(ไม่มีหน้าตั้งค่า)
- 2026-10-10 19:12 · ขั้น 5 → done
- 2026-10-10 19:12 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-009.md/.docx (Prebrief Mode · APPROVED · C16 WARN module ใหม่ไม่อยู่ใน FEATURE_REGISTRY)
- FRD_F-TMP-009_Pack 00–07 + INDEX · frd_lint Section N: BLOCK 0 · WARN 0 · PASS 13
- doccfg --final --registry PASS (CTR ไม่ชน) · ntf --final PASS · doa brief --print-config PASS · mdoc WARN (taxonomy_def_id ว่าง · doa pending → อธิบายได้)
- มีการอนุมัติจริง (2 ขั้น) → ทำ DOA_BRIEF ตามปกติ (ไม่ใช่สาย 0 ขั้น)
- ตัดปุ่ม "ทำซ้ำ" ออกจาก prototype ให้ตรง DEC-11 (ทำซ้ำ ✗)
- 2026-10-10 19:17 · ขั้น 7 → done

## ขั้น 8 · UI Brief → test case AI → UAT
- UI_BRIEF_F-TMP-009.md: brief_check PASS (FAIL 0 · WARN 0 · B1–B8)
- testcases-F-TMP-009.md: 41 เคส / 100 step · tc_lint ERROR 0 · Ledger: AC 14/14 · BR 15/15 · VR 9/9 · EC 5/8 (ข้าม 3 มีเหตุผล) · DEC 12/14 (DEC-05 N/A · DEC-13 OQ-04)
- [NO-BROWSER] ข้าม verify_anchors.py — anchor เขียนจากโค้ดจริง + ไล่ flow ด้วย smoke jsdom
- cases.json (Lite 25 เคส) + QA_AUDIT (drop ledger 16) · lite_audit หายเงียบ 0 · --stamp แล้ว
- [NO-BROWSER] ข้าม capture.py → build testcase-F-TMP-009.html ด้วย shots ว่าง (ไม่มีภาพประกอบ — build เตือน regionKey ไม่มีภาพ)
- 2026-10-10 19:25 · ขั้น 8 → done

## ขั้น 9 · แพ็ก
- manifest_scan (unmapped 8 = ไฟล์ทำงาน/รายงานกลาง อธิบายได้) · consistency_check READY · BLOCK 0 · WARN 1 (K9 ไม่มี e2e_standard report — [NO-BROWSER]) · แก้ K4 (microcopy ใน 06) แล้ว
- `bash _system/dm.sh pack J009` → _pack/F-TMP-009_DevPack.zip
