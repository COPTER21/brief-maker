# RUN_LOG — F-TMP-003 ฟอร์มขอลายเซ็น electronics (REQ-TMP-003)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)

## ขั้น 1 · อ่านฟอร์ม + PREBRIEF v2 (2026-10-07)
- ภาพฟอร์ม: `_system/tools/to_image.py` → LibreOffice → PDF → pypdfium2 (2 หน้า) ได้ `SAMPLE.pdf` + `page-1.png` `page-2.png` + `content.html`
  - เป็นหน้ากระดาษจริงจาก LibreOffice (ไม่ใช่ HTML snapshot) → เทียบ layout ได้
  - ฟอนต์ไทยในภาพ render เป็นกล่อง → ถ้อยคำทั้งหมดยึดจาก `orig/content.src.txt` + XML ของ .docx (ตรวจ `w:p` ทีละย่อหน้า) · ภาพใช้ดูตำแหน่ง/เส้น/ช่องติ๊ก
- checkbox ในต้นฉบับเป็นอักขระ Wingdings (U+F0A8 / U+F0A1) ไม่ใช่ content control → นับได้ครบ 11 ช่องติ๊ก (กรณี 3 · เหตุผลกรณี 2 สามข้อ · ประเภทเปลี่ยนกรณี 3 สามข้อ · เจ้าหน้าที่ 2)
- ชื่อเอกสาร: ชื่อไฟล์ "ฟอร์มขอลายเซ็น electronics" ไม่ตรงหัวฟอร์ม → `dm.sh rename J003 "คำขอมีและใช้ลายเซ็นดิจิทัล (Digital Signature)"`
- เลขฟอร์มจาก footer: **FM-HRM-23 · Rev. 00 : 01/07/2569**
- `form_spec_check.py` → **ERROR 0** · 19 ช่อง (ระบบ 8 · กรอก 10 · ระบบใส่ 1) · ตัวเลือก 4 กลุ่ม · ลายเซ็น 2 · anomalies 6 · gate ที่ต้องถาม G1 G2 G5 G6 G7 G8 G9 G10
- `prebrief_v2.py --req REQ-TMP-003 --module HR` → PREBRIEF_REQ-TMP-003_v2.md (ไม่มี PREBRIEF จาก CMS)
- `impact_summary.py` **บั๊กที่รู้แล้ว**: regex `REQ-[\d-]+` ไม่รับ `REQ-TMP-003` → รันบนสำเนาที่แทนเป็น `REQ-9903-0003` แล้ว sed กลับเป็น REQ-TMP-003 ใน output ทั้ง .html/.json
- `orig/content.html` → เปลี่ยนชื่อเป็น `orig/content.src.txt` (กัน `manifest_scan.py` นับเป็น prototype ซ้ำ → K2 BLOCK)
- PDPA: ต้นฉบับเป็นฟอร์มเปล่า ไม่มีข้อมูลบุคคลจริง · ช่องชื่อ/อีเมล/โทร/ตัวอย่างลายมือชื่อ ติด `pdpa: true` ทั้งหมด → prototype/แบบพิมพ์ใช้ชื่อสมมติเท่านั้น
- 2026-10-07 13:28 · ขั้น 1 → done

## ขั้น 2 · gate 10 หมวด → DECISIONS.lock (โหมดไม่เฝ้า · AI ตอบเอง)
ตอบตาม `unattended-policy.md` ทุกหมวด → `decisions_lock.py` = **พร้อมเริ่มทำ** · `dm.sh tag` → **AI-DEFAULT 11 มติ** (DEC-01..11) + VALID 6 มติ (DEC-12..17 จาก anomalies)
- G1 `config_changes: []` `post_to: []` — ใบนี้เป็นคำขอใบรับรอง CA · การออก/เพิกถอนใบรับรองทำนอกระบบโดยเจ้าหน้าที่ · การแก้ชื่อ-นามสกุลในทะเบียนพนักงานเป็นงานของ F-EMP-001 ไม่ใช่ผลอัตโนมัติของใบนี้
- G2 dynamic · ค่าเริ่ม 1 ขั้น ตามช่องลงชื่อผู้อนุมัติบนกระดาษ 1 จุด ("เจ้าหน้าที่") · ไม่มีวงเงิน
  - **role บนกระดาษคือ "เจ้าหน้าที่" (ผู้ดูแลลายเซ็นดิจิทัล) ซึ่งยังไม่มีใน `doa-roles-contract.md`** → ใช้ `role-mgr-hr` (ผู้จัดการฝ่ายบุคคล · module hr) เป็นค่าเริ่มที่ DOA กลางรู้จัก และเสนอเพิ่ม `role-hr-officer` ใน DOA กลาง (ใส่ใน _BATCH_REPORT)
- G3 ไม่มีสูตร/ค่าคงที่บนกระดาษ → ใช้ค่ามาตรฐาน (DEC-04 ไม่มีผลจริงกับใบนี้)
- G4 ไม่มีแถวซ้ำ → DEC-05 ออกมาเป็น "min_rows None" ตามบั๊กที่ทราบของ `decisions_lock.py` (ปล่อยได้ · ไม่มี repeat group จริง)
- G5 1:1 · 19 ช่อง ไม่เพิ่ม/รวม/แยก
- G6 แถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อแทนการอนุมัติ · ช่อง "ตัวอย่างลายมือชื่อ/ลายมือเขียนชื่อ" เป็น**ข้อมูลของคำขอ** (เว้นกรอบว่างบนแบบพิมพ์ให้เขียนด้วยมือ + แนบไฟล์ได้ตาม G10) ไม่ใช่ลายเซ็นอนุมัติ
- G7 ไม่อนุมัติ → กลับเป็นร่างเลขเดิม · ยกเลิกได้ owner + admin_role สถานะ draft/pending · ต้องมีเหตุผล
- G8 เจ้าของ · ผู้อนุมัติหลังส่ง · admin role ของฝ่ายบุคคลเห็นทั้งหมด
- G9 ออกเลขตอนบันทึกครั้งแรก (เอกสารภายใน ไม่ใช่เอกสารการเงิน no-gap) · **รหัส DSR** (ไม่ชนกับ ACL · MEM · VAN)
- G10 แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗
- `impact_summary.py --decisions` → **พร้อมเริ่มทำ** (ใช้วิธีเลี่ยงบั๊ก REQ-TMP เหมือนขั้น 1)
- 2026-10-07 13:29 · ขั้น 2 → done

## ขั้น 3 · ร่าง declaration (doa · ntf)
- `doa_tool.py init` รอบแรก on_reject = `draft` → `brief --roles` ให้ **BLOCK G5 "on_reject ต้องเป็น back_to_draft หรือ end"**
  - แก้ `decisions.yaml` G7 เป็น `on_reject: back_to_draft` → lock ใหม่ → `dm.sh tag` ใหม่ → init/brief ใหม่ → **VERDICT PASS** (แก้รอบเดียว)
  - `roles.txt` สร้างจาก `4_knowledge/governance/doa-roles-contract.md` ส่งให้ `--roles` → role-mgr-hr อยู่ใน master ไม่มี BLOCK
  - INFO G8: ยังไม่ให้ `--print-config` (ตรวจ sign_boxes ตอนขั้น 4/7)
- `ntf_tool.py suggest` ได้ 2 event · ตัด DOA events 3 ตัวอัตโนมัติ
  - ตัด `dsr_over_limit_approved` (review: true) ออก — เอกสารไม่มีค่าคงที่/สูตร/วงเงิน จึงไม่มี "เกินเกณฑ์"
  - เติม `dsr_name_change_requested` — กรณีที่ 3 (เปลี่ยนชื่อ-นามสกุล) ต้องแจ้งผู้ดูแลทะเบียนพนักงาน (F-EMP-001) ให้แก้เอง เพราะ DEC-01/02 ไม่ให้ระบบเปลี่ยนค่าข้ามระบบอัตโนมัติ
  - `ntf_tool.py brief` → **VERDICT PASS**
- doccfg + mdoc รอ `print_config.json` จากขั้น 4 (ตามคำสั่งของ step)
- 2026-10-07 13:31 · ขั้น 3 → done

## ขั้น 4 · แบบพิมพ์ Replica (โหมด NO-BROWSER)
- `print/form.tpl.html` (logic-less) · `profile.json` (8 token ต่างจาก default-replica · โลโก้ชิดขวาตามต้นฉบับ) · `print_config.json` (doc_type DSR · sign_boxes `doa_step:*` · decision_words.by_role role-mgr-hr = ดำเนินการได้/ไม่สามารถดำเนินการได้)
- data 5 สถานะ (`make_data.py`): draft (กรณี 1 · รออนุมัติ) · approved (กรณี 3 เปลี่ยนทั้งชื่อและนามสกุล · ครบทุกช่อง) · rejected (กรณี 2 ลืมรหัสผ่าน · มีเหตุผลไม่ดำเนินการ) · long-3signs (ข้อความยาว + 3 ขั้น) · approved-doa6steps (6 ขั้น → 7 ช่อง 2 แถว 4+3)
- ช่องลงชื่อสร้างจาก `sign_rows.py` ทุกสถานะ (ไม่ fix จำนวน) → 2 / 2 / 2 / 4 / 4+3
- **บล็อกลงชื่อย้ายลงแถวล่าง (B6) ตามหลัก form-replica ข้อ 3** → ช่องติ๊ก "ดำเนินการได้ / ไม่สามารถดำเนินการได้" ของเจ้าหน้าที่อยู่ในกล่องลงชื่อ (decision ผูก role) · ในเนื้อฟอร์มคงหัวข้อ "สำหรับเจ้าหน้าที่" + บรรทัด "เนื่องจาก ……" ไว้ ไม่พิมพ์คำซ้ำ
- `parity_check.py` → **IDENTICAL ทั้ง 5 ไฟล์**
- `render_doc.py --strict` ทั้ง 5 สถานะ ผ่าน (ไม่มี key ขาด) → `build_html.py --mode replica` ได้ HTML ต่อสถานะใน `print/out/` + `DSR_template.html` · ตรวจแล้วไม่มี `{{…}}` หลงเหลือ
- `[NO-BROWSER] ข้าม render_states.py` (PDF + `_states_sheet.png` ต่อสถานะ) · `[NO-BROWSER] ข้าม render_pdf.py` · `[NO-BROWSER] ข้าม compare_original.py` (เทียบภาพกับ `orig/SAMPLE.pdf`)
  → **ต้องรันรอบเต็มบนเครื่องที่มี browser** เพื่อได้ PDF ทุกสถานะ · `_states_sheet.png` · `compare/compare_side.png` และยืนยัน "ทุกสถานะ 1 หน้า"
- 2026-10-07 13:37 · ขั้น 4 → done

## ขั้น 5 · HTML Q-form (Pattern Q2) + gate
- `feature.html` สร้างจาก archetype Q-form — ลอกโครงกลางจาก DevPack ที่ผ่านแล้วในกองนี้ (J001 · `_SOURCE_form-request-reference.html` ชุดเดียวกัน) แล้วเปลี่ยนเฉพาะส่วน domain
  - list 9 คอลัมน์ (เลขที่ · วันที่ขอ · ผู้ยื่นคำขอ · สังกัดหน่วยงาน · กรณี · รายละเอียดกรณี · สถานะ · ลายเซ็น · ⋮) · ตัวกรอง สถานะ/กรณี/ฝ่าย
  - wizard 3 ขั้น (ข้อมูลหลักคำขอ · เอกสารแนบ · ตรวจสอบและยืนยัน) · กรณี 3 ทางเป็น track-card · ตัวเลือกย่อยเป็น chip · ช่องชื่อเดิม/ชื่อใหม่เปิดเฉพาะกรณี 3 และบังคับเฉพาะส่วนที่เลือกเปลี่ยน (DEC-13/DEC-14)
  - view tabs: รายละเอียด › PDF Preview › ลายเซ็น/อนุมัติ › ประวัติ · เอกสารแนบเป็น section ในแท็บรายละเอียด
  - DOA: `MOCK_DOA_RESOLVED` 1 ขั้น dynamic + slot picker ตอนส่ง · `DECISION_WORDS` ผูก role (ดำเนินการได้ / ไม่สามารถดำเนินการได้)
  - PDF Preview ใช้ `DSR_TPL` = `print/form.tpl.html` ตรงตัว (ตรวจแล้ว **TPL IDENTICAL** กับไฟล์บนดิสก์) + `docPrintData()` ตาม data contract
- **ไม่มีช่องวันที่ของเบราว์เซอร์** (Rule #114) — เอกสารนี้ไม่มีช่องวันที่ให้ผู้ใช้กรอก (วันที่เป็น auto) จึงไม่ต้องใช้ `bedateHTML()` ในฟอร์ม แต่ยังเก็บ kit ไว้ใน BASE-KIT
- ด่าน: `audit.sh` → **FAIL = 0 · WARN = 3** (WARN ทั้งหมดเป็นของ BASE-KIT กลาง: `data-lucide` ใน helper กลางไม่มี class w-N · `.uc-email` ใน kit · hardcoded font-size ใน shell CSS — เหมือน DevPack ใบก่อนในกองนี้)
- `prune_css.py` → ตัด rule ที่ไม่ใช้ 10 ข้อ (−1.0 KB) แล้ว audit ซ้ำยัง FAIL = 0 · ตรวจไวยากรณ์ JS ด้วย `node --check` ผ่าน
- `[NO-BROWSER] ข้าม e2e_standard.py` · `[NO-BROWSER] ข้าม render-check.py` → `window.__QA__` ใส่ครบตาม Rule #111 แล้ว ต้องรัน e2e รอบเต็มบนเครื่องที่มี browser ก่อน UAT
- 2026-10-07 13:57 · ขั้น 5 → done
- 2026-10-07 13:57 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- `BRD_F-TMP-003.md` (Prebrief Mode · DEC = Scope Lock ชั่วคราว §3.4) → **APPROVED** (§19) ติดเงื่อนไข: ลูกค้ายืนยันมติ AI-DEFAULT 11 ข้อ + ปิด OQ-01…OQ-05
- `FRD_F-TMP-003_Pack/` 8 ไฟล์ (00_OVERVIEW · 01_UI · 02_API · 03_LOGIC · 04_DB · 05_RULES · 06_TESTS · 07_LOCKED_DECISIONS)
- `frd_lint.py` → **BLOCK 0 · WARN 0 · PASS 12** (N1 DEC ครบ 17 · N2 ช่องครบ · N3 ไม่มีค่าคงที่ · N4 เคสปฏิเสธสิทธิ์ 11 จุด + เคสร่างไม่รั่ว · N5 ENG-DOC-NUM ที่ FN-04 + header_snapshot · N6 approval_chain/doa_ref · N7 event ครบ · N8 ไม่อ้างเวอร์ชันที่ไม่ได้ติดตั้ง)
- ใส่ `frd_ref` ตามที่ lint เสนอ → `doccfg_tool.py brief --final --registry` = **PASS** (รหัส DSR ไม่ชน ACL/MEM/VAN) · `ntf_tool.py brief --final` = **PASS**
- `mdoc_tool.py` = WARN 2 ข้อตามคาด (taxonomy_def_id ว่าง · doa pending) — ไม่ใช่ BLOCK
- 2026-10-07 14:07 · ขั้น 7 → done

## ขั้น 8 · UI Brief → test case AI → UAT
- `extract_anchors.py` → `reports/inventory.json` (vars 47 · route 5 · overlay 33 · toast 11 · ปุ่ม 19 · function 186 · archetype Q-form · `__QA__` ครบ)
- `UI_BRIEF_F-TMP-003.md` (§0–§13) → `brief_check.py` = **PASS · FAIL 0 · WARN 0** (B1 route ครบ · B2 toast คงที่ครบ 11 · B5 anchor มีจริงทั้งหมด · B6 CSS vars 47/47)
- `testcases-F-TMP-003.md` 22 เคส · 97 step (CRT 8 · DOA 6 · PERM 3 · PDF 3 · LIST 2) → `tc_lint.py` = **ERROR 0**
- `cases.json` (เอกสารแบบทดสอบสำหรับคน) 20 เคส + `QA_AUDIT_F-TMP-003.md` → `lite_audit.py --stamp` = **หายเงียบ 0** · drop ledger 2 เคส (TC-PERM-02 ต้องรู้ URL ภายใน · TC-PDF-03 ต้องใช้เครื่องมือนักพัฒนา)
- `[NO-BROWSER] ข้าม verify_anchors.py` (ตรวจ anchor กับหน้าจอจริง) · `[NO-BROWSER] ข้าม capture.py` (ถ่ายภาพประกอบ) → ยังไม่ build UAT HTML เพราะรอภาพ
- 2026-10-07 14:18 · ขั้น 8 → done

## ขั้น 9 · ตรวจรวม + แพ็ก DevPack
- `manifest_scan.py` → 38 artifact · ซ้ำ 0 (ย้าย `orig/content.html` → `content.src.txt` ตั้งแต่ขั้น 1 จึงไม่ชนกับ `feature.html`)
- `consistency_check.py` รอบแรก: **READY · BLOCK 0 · WARN 3** → แก้ 2 WARN แล้วรันซ้ำ
  - K4 microcopy: เขียน "ดำเนินการได้/ไม่สามารถดำเนินการได้" ติดกันด้วย `/` ใน 06_TESTS → แยกเป็นสองข้อความ
  - K6: เติมตาราง DEC-01…DEC-17 ใน BRD §3.4 (เดิม BRD อ้างมติไม่ครบ 7 ข้อ)
- `consistency_check.py` รอบสอง: **READY · BLOCK 0 · WARN 1 · PASS 9** — WARN เดียวที่เหลือคือ `[NO-BROWSER] ไม่มี report e2e_standard` ตามที่คาดไว้
