# RUN_LOG — F-TMP-006 FM-ITS-09 แบบฟอร์มรายงานการเข้า-ออก ห้อง server (REQ-TMP-006)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 — หมายเหตุ
- ภาพฟอร์ม: to_image.py → LibreOffice → PDF → pypdfium2 (หน้ากระดาษจริง A4 แนวนอน) · เครื่องไม่มีฟอนต์ไทย ภาพเห็นตัวไทยเป็นกล่อง → ถ้อยคำยึด content.html + openpyxl · ตำแหน่ง/เส้นยึดภาพ · content.html เปลี่ยนชื่อเป็น orig/content_extract.txt (กัน K2 นับเป็น prototype ซ้ำ)
- หัวกระดาษ (A1:I1 merge) = "รายงานการเข้า-ออก ห้อง server" → form.title · โลโก้ฝังในชีตมุมซ้ายบน · Doc No./Rev. footer ขวา (FM-ITS-09 · Rev.00 : 01/07/2569)
- ตาราง 9 คอลัมน์ · แถวว่าง 21 แถว · ไม่มีช่องลงชื่อท้ายใบ · ลายเซ็นผู้เข้า / ลายเซ็นผู้รับรอง เป็นคอลัมน์ต่อแถว (who=other — รับรองรายแถว ไม่ใช่อนุมัติเอกสาร) · ไม่มีข้อมูลตัวอย่าง/ข้อมูลส่วนบุคคลในไฟล์
- form_spec_check: ERROR 0 · ไม่มี PREBRIEF CMS → PREBRIEF v2 จาก FORM_SPEC (--req REQ-TMP-006 --module IT) · ชื่อในคิวไม่เพี้ยน → ไม่ต้อง rename
- ไฟล์ IMPACT_SUMMARY_REQ-XXXX-XXXX.* (รันแรกลืม --req) ย้ายไป .scratch/
- 2026-10-10 09:09 · ขั้น 1 → done · FORM_SPEC 9 ช่อง · 21 แถว · ERROR 0

## ขั้น 2 — เหตุผลรายหมวด (unattended · AI-DEFAULT ทั้งหมด)
- G1: ทะเบียนเข้า-ออกห้อง server เป็นบันทึกอย่างเดียว ไม่เปลี่ยนค่า/ไม่ส่งต่อ (ไม่เชื่อมระบบประตู/บัตร — เสนอเป็นงานต่อยอดใน _BATCH_REPORT)
- G2: กระดาษไม่มีช่องลงชื่อผู้อนุมัติท้ายใบ → จำนวนขั้น = 0 → ไม่ทำ DOA · "ลายเซ็นผู้รับรอง" ต่อแถว = การรับรองรายแถวโดยเจ้าหน้าที่ IT ผู้ดูแลห้อง (สิทธิ์ role-it-officer — ไม่มีใน doa-roles-contract) · ลูกค้ายืนยันว่าต้องขออนุมัติก่อนเข้าห้องไหม
- G3: ไม่มีสูตร/ค่าคงที่ · เวลาออกก่อนเข้า = บล็อก · อยู่นานเกิน 12 ชม. (config) / แถวค้างซ้อน = เตือน · ส่งปิดรอบต้องครบเวลาออก + ผู้รับรอง · ผู้รับรอง ≠ ผู้เข้า (SoD)
- G4: กระดาษ 21 แถว → ไม่จำกัดแถว · PDF ขั้นต่ำ 21 แถว
- G5: 1:1 ตามกระดาษ 9 คอลัมน์ ไม่เพิ่มช่อง · ตัดช่องว่างท้าย "เหตุผลการเข้าใช้"
- G6: ลายเซ็นเป็นข้อความระบบต่อแถว ("ลงชื่อในระบบ" / "รับรองในระบบ" + ชื่อ + วันเวลา) ไม่ใช้ภาพ
- G7: ไม่มีอนุมัติ → ร่าง(เปิดรอบ) → ส่งแล้ว(ปิดรอบ) · ยกเลิกได้โดยเจ้าของ + admin role · ต้องมีเหตุผล
- G8: เจ้าของ · admin role ของหน่วยงาน IT เห็นทั้งหมด
- G9: ออกเลขเมื่อบันทึกครั้งแรก · รหัส SRAL (Server Room Access Log) — ไม่ชน registry (ACL ITRS SRC DRITS CRR) และไม่ชน J005 (ITCR)
- G10: แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗
- decisions_lock: 14 มติ พร้อมเริ่มทำ (exit 0) · tag-ai-default → 10 มติ AI-DEFAULT
- 2026-10-10 09:09 · ขั้น 2 → done · 14 มติ · AI-DEFAULT 10 · ไม่มี DOA · code SRAL

## ขั้น 3 — declaration (ร่าง)
- DOA: ไม่ทำ — DEC-03 ไม่มีการอนุมัติ (doa_tool init ปฏิเสธเอง "ห้ามยัด DOA เข้า feature ที่ไม่มีอนุมัติ") · ผู้รับรองรายแถว = สิทธิ์ role-it-officer (ไม่ใช่ DOA)
- NTF: 4 event (sral_certify_pending · sral_overstay · sral_submitted · sral_cancelled) → brief PASS · ตัด sral_over_limit_approved จาก suggest (ไม่มีอนุมัติ) · ไม่มี doa_* events
- DOCCFG: code SRAL (Server Room Access Log) — ไม่ชน registry (ACL ITRS SRC DRITS CRR) และไม่ชน J005 (ITCR) → brief PASS (--registry)
- MDOC: class REC · function_code F01 ชั่วคราว · source=declaration (REQ เลขชั่วคราว) → WARN G04 (taxonomy_def_id ว่าง) อธิบายได้

## ขั้น 4 — แบบพิมพ์ Replica
- R9 ตารางกรอบ 9 คอลัมน์ · ต้นฉบับ A4 แนวนอน 21 แถว → engine รองรับแนวตั้งเท่านั้น + แถวจริง > ~20 + ช่องลายเซ็นเป็นข้อความ 2 บรรทัด → ออกแบบ 2 หน้า (R10): 12 แถว/หน้า · หัวตารางซ้ำ · "มีต่อหน้าถัดไป" · "หน้า X/2" · ฟอนต์ 8pt
- data 5 สถานะ: draft · submitted · pending-cert · long-24rows · cancelled (ไม่อนุมัติ/DOA 6 ขั้น ไม่ใช้ — ไม่มี DOA) · ทุกสถานะ 12+12 แถว = 2 หน้าเท่ากัน
- parity_check: IDENTICAL 5/5 · render_doc --strict ไม่มี key ขาด · ไม่มี {{}} หลง · build_html ทุกสถานะ OK (out/*.html) · SRAL_print-spec.md
- [NO-BROWSER] ข้าม render_pdf.py (render_states.py เรียก render_pdf → สร้าง HTML ต่อสถานะด้วย render_doc + build_html แทน) · ข้าม compare_original.py (ต้องใช้ PDF) → ยังไม่มี _states_sheet.png / compare_side.png
- 2026-10-10 09:12 · ขั้น 3 → done · no DOA (DEC-03) · NTF PASS · DOCCFG SRAL PASS · MDOC WARN G04
- 2026-10-10 09:12 · ขั้น 4 → done · 2 หน้า R10 · parity 5/5 · NO-BROWSER ไม่มี PDF/compare

## ขั้น 5 — HTML Q-form (html-generator v9.4)
- feature.html ประกอบจาก base-kit/shell ของ DevPack ตัวอย่าง F-FIN-ACL (ผ่านทุกด่าน) + page CSS/JS ของ SRAL (`.scratch/build_feature.py` · app_part1–5) · แบบพิมพ์ฝัง form.tpl.html + tplRender (= tpl_render.js)
- เปิด GOLDEN_SKELETON.html + ui-standard-list-drawer.md U1–U28 เทียบก่อน build
- โครง: list (seg tabs · filter สถานะรับรอง/ผู้บันทึก · kebab ⋮ · pagination) · wizard 1290 (ตารางกรอก 9 คอลัมน์ · ชื่อพนักงานเลือกจาก datalist เติมฝ่ายให้ · บุคคลภายนอกพิมพ์เอง · เวลา HH:MM) · view drawer (รายละเอียด · PDF Preview · ลายเซ็น / รับรอง · ประวัติ) · modal รับรองรายแถว / ส่งปิดรอบ (บล็อกถ้ายังไม่ออก/ไม่รับรอง) / ยกเลิก (เหตุผลบังคับ)
- audit.sh: FAIL 0 · WARN 3 (มาจาก base-kit กลาง: lucide class ใน comment/kit · .uc-email · font-size px ใน kit) → reports/audit.txt · รอบแรก FAIL Rule #98 (ไม่มี renderSignProgress) → เพิ่มกลับ → FAIL 0
- prune_css.py: ตัด 3 rule → audit FAIL 0 ซ้ำ
- [NO-BROWSER] ข้าม e2e_standard.py · render-check.py → ทดแทนด้วย smoke test jsdom (ไม่ใช่ browser จริง · ไม่ใช่ด่านทางการ) 46/46 ผ่าน · JS error 0 → reports/smoke_jsdom.txt (สิทธิ์ G8 · SoD ผู้รับรอง ≠ ผู้เข้า · non-IT รับรองไม่ได้ · แถวยังไม่ออกรับรองไม่ได้ · ปิดรอบบล็อกถ้าไม่ครบ · ออกก่อนเข้าบล็อก · ยกเลิกต้องมีเหตุผล · DOA dynamic · backdrop mousedown · tabs)
- parity แบบพิมพ์ใน prototype: printData จาก JS → render_doc.py --strict + parity_check IDENTICAL 2/2
- U1–U28: U1✓ U2✓ U3✓ U4✓ U5✓ U6✓ U7✓ U8✓ U9✓ U10✓ U11✓(kit) U12✓ U13✓(ไม่มีขั้น → summary+timeline+ลายเซ็นต่อแถว) U14✓(wizard 1290 · ตารางกรอก) U15✓ U16 n/a(ไม่มีลบ ใช้ยกเลิก) U17✓ U18✓ U19✓ U20✓(tabs สถานะ) U21✓(kit) U22✓ U23✓ U24✓ U25✓ U26–U28 n/a(ไม่มีหน้าตั้งค่า)
- 2026-10-10 09:20 · ขั้น 5 → done · audit FAIL 0 · NO-BROWSER: e2e ข้าม → jsdom smoke 46/46
- 2026-10-10 09:20 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 6 — ข้าม (unattended)
- ให้คนดูจาก _BATCH_REPORT · [NO-BROWSER] ยังไม่มี _states_sheet.png / screenshot หน้าจอหลัก (ต้อง render บนเครื่องที่มี browser)

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-006.md/.docx (brd-generator-full v2.3 Prebrief Mode · Lane · md_to_docx) — AI Review C01–C23 + PE01–PE05 ผ่าน → APPROVED (C22 ตัวชี้วัด → OQ-01 · PE02 SoD ผู้รับรอง ≠ ผู้เข้า preventive + ระดับเอกสาร detective)
- FRD_F-TMP-006_Pack (frd-generator-v6 Input Mode 0 · STANDARD) 00–07 + INDEX + declarations/ · 07 §7.0 สร้างจาก DECISIONS.lock.json ตรงตัว · 04/05 ไม่มีถ้อยคำสายพิจารณา (กัน K7 ตามบทเรียน J002)
- frd_lint: BLOCK 0 · WARN 0 · PASS 11 → reports/_SECTION_N.md
- doccfg --final --registry: PASS (SRAL ไม่ชน) · ntf --final: PASS · mdoc: WARN G04 (taxonomy_def_id ว่าง — OQ-07)
- DOA: ไม่มี DOA_BRIEF (DEC-03) · role-it-officer (ผู้รับรองรายแถว) + admin role ฝ่าย IT ไม่อยู่ใน doa-roles-contract → OQ-03 (ไม่ใช้กับ DOA เพราะ 0 ขั้น แต่ใช้กับสิทธิ์รับรอง/มองเห็น/ยกเลิก)
- 2026-10-10 09:24 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 · doccfg/ntf --final PASS

## ขั้น 8 — UI Brief → test case AI → UAT
- extract_anchors → reports/inventory.json · UI_BRIEF_F-TMP-006.md (§0–§13) → brief_check: PASS · FAIL 0 · WARN 0 (reports/brief_check.md)
- testcases-F-TMP-006.md: 51 เคส / 232 step → tc_lint ERROR 0 (reports/tc_counts.json) · รอบแรก ERROR 2 (step "RUN console" ไม่ขึ้นต้น verb) → แก้เป็น TYPE → console
- [NO-BROWSER] ข้าม verify_anchors.py · ข้าม capture.py (เอกสารคนไม่มีภาพหน้าจอ)
- cases.json (Lite 42 เคส · 9 กลุ่ม) + QA_AUDIT (drop ledger 9) → lite_audit: หายเงียบ 0 · ประทับ meta.source · build.py → testcase-F-TMP-006.html (ไม่มีภาพ)
- 2026-10-10 09:30 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 · lite_audit หายเงียบ 0 · NO-BROWSER: verify_anchors/capture ข้าม
