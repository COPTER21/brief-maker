# RUN_LOG — F-TMP-002 บันทึกภายใน (REQ-TMP-002)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)

## ขั้น 1 · อ่านฟอร์ม + PREBRIEF v2 (2026-10-07)
- ต้นฉบับ `orig/บันทึกภายใน.doc` → `to_image.py` แปลงได้ด้วย **LibreOffice → PDF → pypdfium2** (ไม่ใช่เส้นทาง HTML) → ได้ `orig/SAMPLE.pdf` + `orig/page-1.png` ซึ่งเป็นหน้ากระดาษจริง ใช้เทียบ layout ได้
- ถ้อยคำยึดจาก text layer ของ SAMPLE.pdf (พิกัดจริง) · ตำแหน่ง/เส้นยึดจาก page-1.png (ภาพแสดงอักษรไทยเป็นกล่องเพราะฟอนต์ในเครื่องเรนเดอร์ไม่ได้ — ไม่กระทบถ้อยคำ เพราะอ่านจาก text layer)
- ชื่อบนหัวฟอร์ม = "บันทึกภายใน" ตรงกับชื่องาน → **ไม่ต้อง rename**
- Doc No. บนกระดาษ FM-HRM-54 · Rev.00 : 01/07/2569 · โลโก้ Credence (ครีเดนซ์)
- โครงกระดาษ: กล่องหัว (เส้นทึบคู่) = ชื่อเอกสาร + 5 บรรทัด (วันที่ · เรียน · จาก · เรื่อง · เลขที่) → พื้นที่เนื้อหาว่างกลางหน้า → กล่องล่าง (เส้นทึบ) = ข้อคิดเห็นฝ่ายกฎหมาย + ลงชื่อ + ฝ่ายกฎหมาย + วันที่
- FORM_SPEC: 8 ช่อง (ระบบ 1 · กรอก 4 · ระบบใส่ 3) · ลายเซ็น 1 (ฝ่ายกฎหมาย) · แถวซ้ำ 0 · ตัวเลือก 0 · สูตร 0 · ค่าคงที่ 0 · anomalies 4
- `form_spec_check.py` → **ERROR 0** · gate ที่ต้องถาม G1 G2 G5 G6 G7 G8 G9 G10
- ไฟล์ตัวอย่างเป็นแบบฟอร์มเปล่า → ไม่มีข้อมูลส่วนบุคคล (pdpa_fields = 0) · prototype ใช้ข้อมูลสมมติล้วน
- `prebrief_v2.py` → `PREBRIEF_REQ-TMP-002_v2.md` (ไม่มี PREBRIEF จาก CMS) · ประเภทงาน = แบบ 2 ดึงข้อมูลเดิม
- **ข้ามรันไม่ได้:** `impact_summary.py` อ่าน PREBRIEF ไม่ผ่าน — regex ในสกิลบังคับ `REQ-[\d-]+` (ตัวเลขล้วน) แต่รอบนี้ใช้รหัสชั่วคราว `REQ-TMP-002` ที่มีตัวอักษร → ไม่สร้าง IMPACT_SUMMARY (ไม่ใช่ไฟล์บังคับของ K1) · เสนอแก้ regex ในรายงาน
- 2026-10-07 12:14 · ขั้น 1 → done

## ขั้น 2 · gate 10 หมวด → DECISIONS.lock (โหมดไม่เฝ้า)
- ตอบเองตาม `4_knowledge/governance/unattended-policy.md` ทุกหมวด → `decisions_lock.py` = **พร้อมเริ่มทำ (exit 0)** · 15 มติ · `tag-ai-default` ติด AI-DEFAULT 11 ข้อ (DEC-01..11) · DEC-12..15 = VALID จาก FORM_SPEC.anomalies
- เหตุผลรายหมวด:
  - G1 ฟอร์มไม่เขียนว่าอนุมัติแล้วเปลี่ยนค่าหรือส่งต่อระบบใด → `config_changes: []` · `post_to: []`
  - G2 กระดาษมีช่องลงชื่อผู้พิจารณา 1 จุดคือ "ฝ่ายกฎหมาย" → dynamic 1 ขั้น · ไม่มีช่วงวงเงินบนกระดาษ → `amount: none`
  - G3 กระดาษไม่มีสูตรและไม่มีตัวเลขพิมพ์ตายตัว → ใช้ค่าเสนอทั้งชุด (ไม่มีผลจริงกับเอกสารนี้)
  - G4 ไม่มี repeat group บนกระดาษ → `max_rows: null`
  - G5 1:1 ไม่เพิ่มช่อง (ไม่เพิ่มหมายเหตุ) · G6 แถวล่าง 1 ช่องต่อขั้น DOA ไม่ใช้ภาพลายมือชื่อ
  - G7 กลับเป็นร่างเลขเดิม · ยกเลิกได้เฉพาะ draft/pending · ต้องมีเหตุผล
  - G8 เจ้าของ · ผู้อนุมัติหลังส่ง · admin role เห็นทั้งหมด
  - G9 เอกสารภายใน ไม่ใช่เอกสารการเงิน no-gap → ออกเลขตอนบันทึกครั้งแรก · ชื่อไฟล์ไม่มี `[CODE]` → ย่อ 3 ตัวจากชื่อเอกสาร = **MEM** (ไม่ชนกับ registry ที่มีแค่ ACL)
  - G10 แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗
- **ข้อสังเกตเครื่องมือ:** `decisions_lock.py` ออก DEC-05 (G4) ให้เสมอแม้ไม่มี repeat group → ข้อความ "PDF อย่างน้อย None แถว" เป็น placeholder ไม่มีผลกับเอกสารนี้
- **role mapping ที่ต้องให้ลูกค้ายืนยัน:** "ฝ่ายกฎหมาย" บนกระดาษไม่มี role ตรงใน `doa-roles-contract.md` (ไม่มี `role-legal`) → map เป็น `role-compliance` (เจ้าหน้าที่กำกับดูแล · M4) ซึ่งเป็น role ที่ใกล้ที่สุดในรายการ 14 role · เสนอขอเพิ่ม `role-legal` ที่ DOA กลางในรายงาน
- 2026-10-07 12:16 · ขั้น 2 → done

## ขั้น 3 · ร่าง declaration (doa · ntf)
- `doa_tool.py init` → `MEM.doa.yaml` · 1 set · 1 ขั้น (role-compliance · ป้าย "ฝ่ายกฎหมาย" ดึงจาก FORM_SPEC.signatures) · mode dynamic · on_reject back_to_draft · ติด DEFAULT (AI-DEFAULT)
- `doa_tool.py brief` → **VERDICT PASS (BLOCK 0)** → DOA_BRIEF_F-TMP-002.md (ร่าง)
- `ntf_tool.py suggest` → 2 event ตั้งต้น · ตัด DOA events 3 (doa_pending/doa_result/doa_escalate)
  - **ตัดสิน event ที่ติด `review: true`:** ตัด `mem_over_limit_approved` ออก — ฟอร์มนี้ไม่มีสูตร ไม่มีค่าคงที่ ไม่มีเกณฑ์ (formulas 0 · constants 0 · calc.rules []) จึงไม่มีเงื่อนไข "เกินเกณฑ์" ให้ยิง
  - ไม่เพิ่ม event แจ้งผู้รับตามช่อง "เรียน" เพราะเป็นข้อความอิสระ ไม่ผูก user ในระบบ + G10 announce = ✗
  - เหลือ `mem_cancelled` 1 event
- `ntf_tool.py brief` → **VERDICT PASS (BLOCK 0)** → NTF_BRIEF_F-TMP-002.md (ร่าง)
- doccfg + mdoc รอ `print_config.json` จากขั้น 4

## ขั้น 4 · แบบพิมพ์ Replica (FM-HRM-54)
- โหมด Replica · template `print/form.tpl.html` ใช้ **R9 ตารางกรอบ (`form-grid`) เซลล์เดียว** 2 กล่อง (กรอบหัวกระดาษ · กรอบข้อคิดเห็นฝ่ายกฎหมาย) เพราะต้นฉบับเป็นกรอบเส้นทึบ — ภายในกล่องใช้ R4 `form-row` ปกติ จึงไม่มีเส้นตารางภายในที่กระดาษไม่มี
- ป้ายหัวบรรทัด (วันที่/เรียน/จาก/เรื่อง/เลขที่) ใช้ `.form-num` + profile `form_num_w: 18mm` ให้ `:` ตรงแนวเหมือนต้นฉบับ · ค่าที่กรอกใช้ `.g-v` (ไม่มีเส้นประ) ตรงกับกระดาษที่ไม่มีเส้นใต้ในกรอบหัว
- บรรทัดข้อคิดเห็นฝ่ายกฎหมายใช้ `.fill fill--left` (เส้นประ) ตรงกับกระดาษ · เติมบรรทัดว่างจนครบ min_rows = 2
- `sign_rows` จาก `sign_rows.py` · **ตัดช่องผู้ขอออกตาม DEC-14** (กระดาษไม่มีช่องลงชื่อผู้จัดทำ) → ช่อง = จำนวนขั้น DOA ล้วน
- data 5 สถานะ: draft · approved · rejected · long-12rows-3signs (14 ย่อหน้า + 3 ช่อง · dense) · doa-6steps (**6 ช่อง 2 แถว 3+3** · dense)
  - ฟอร์มนี้ไม่มี repeat group → สถานะ "ยาว" ใช้จำนวนย่อหน้าเนื้อหาแทนจำนวนแถวรายการ (บันทึกไว้ใน print-spec §8)
- ด่าน: `parity_check.py` → **IDENTICAL 5/5 ไม่มีคำเตือน** · render ทุกสถานะด้วย `render_doc.py --strict` + `build_html.py` → **ไม่มี `{{}}` หลงเหลือ 0/5** · profile token ผ่านการตรวจของ `build_html.py`
- `[NO-BROWSER] ข้าม render_states.py / render_pdf.py` → ไม่มี PDF · ไม่มี `_states_sheet.png` · **ยืนยัน "ทุกสถานะ 1 หน้า" ไม่ได้**
- `[NO-BROWSER] ข้าม compare_original.py` → ไม่มีคะแนนเทียบต้นฉบับ · ไม่มี `compare_side.png` (บันทึกเหตุผลใน print-spec §7 แล้ว)
- ข้อมูลตัวอย่างเป็นข้อมูลสมมติทั้งหมด · โลโก้ใช้ placeholder ไม่ใช่โลโก้ลูกค้า (ต้นฉบับเป็นฟอร์มเปล่าอยู่แล้ว ไม่มีข้อมูลส่วนบุคคล)
- `print_config.json` → `doccfg_tool.py init` → `brief --registry doccfg_registry_codes.txt` → **VERDICT PASS** (รหัส MEM ไม่ชนกับ ACL)
- `mdoc_tool.py validate/brief --doccfg` → **VERDICT WARN (BLOCK 0)** — WARN G04 ยังไม่มี taxonomy_def_id · WARN G09 doa = pending (ปกติของงานที่ยังไม่ wire)
  - **ต้องให้คนยืนยัน:** `class_code: INT` และ `function_code: F01` เลือกเองเพราะ Taxonomy Master v1 ไม่มีในโฟลเดอร์นี้ (register-contract บอกแค่ช่วง F01–F48 ไม่มีคำอธิบาย) → ใส่ไว้ในรายงาน
- `doa_tool.py validate --print-config` → **VERDICT PASS** (G8 `doa_step:*` ครบ · G9 ไม่มีคำตัดสินผูกลำดับขั้น)
- 2026-10-07 12:26 · ขั้น 3 → done
- 2026-10-07 12:26 · ขั้น 4 → done

## ขั้น 5 · HTML Q-form + gate
- archetype **Q-form (Pattern Q2)** — ประกาศ `<meta name="cube-archetype" content="Q-form">` · ขึ้นจาก canonical `references/form-archetype/_SOURCE_form-request-reference.html` (BASE-KIT + shell + utils เดิมทั้งก้อน) แล้วเขียนส่วน domain ใหม่ทั้งหมดให้ตรง FORM_SPEC/DECISIONS ของเอกสารนี้
- ตัดของ OSW ที่ไม่มีในฟอร์มนี้ออก: แถวซ้ำ (tripCard/setLine/addLine) · ตัวเลือก track-card · สูตรเบี้ยเลี้ยง · ปุ่ม "ทำซ้ำ" (G10 copy = ✗) · ช่อง `type="date"` (ฟอร์มนี้ไม่มีช่องวันที่ให้ผู้ใช้กรอก → ไม่ชน Rule #114)
- wizard 3 ขั้นล็อก: ข้อมูลหลักบันทึก › เอกสารแนบ › ตรวจสอบและยืนยัน · ขั้น 1 = `.wz-split` (การ์ด ① ส่งถึงใคร เรื่องอะไร · ② เนื้อหาบันทึก) + การ์ดสรุปสด (จาก/วันที่/เลขที่ ดึงจากระบบ)
- view tabs ตาม #101: รายละเอียด › PDF Preview › ลายเซ็น/อนุมัติ › ประวัติ · PDF ใช้ `MEM_TPL` = `print/form.tpl.html` ฝังตรง ๆ + `tplRender` + `docPrintData()`
- DOA dynamic: `MOCK_DOA_RESOLVED` 1 ขั้น (role-compliance) · modal ส่ง = 1 slot ต่อขั้น · `__QA__.doa.push/pop` ปรับจำนวนขั้นได้ → ช่องลายเซ็นใน PDF เพิ่มตาม ไม่ fix
- **ข้อคิดเห็นฝ่ายกฎหมาย (F07)** ไม่ใช่ช่องของผู้จัดทำ — กรอกใน modal อนุมัติ/ไม่อนุมัติของผู้พิจารณา แล้วไปขึ้นในกรอบบนแบบพิมพ์
- DEC-08 (ไม่อนุมัติ = กลับเป็นร่างเลขเดิม) ทำเป็นปุ่ม "แก้แล้วส่งใหม่" (`reopenDraft`) — เลขที่เดิม ไม่ออกเลขใหม่
- ด่าน:
  - `audit.sh` → **FAIL = 0** (WARN 3 ข้อ ตกทอดจาก BASE-KIT ของสกิล: Rule #21 ไอคอนในโค้ด helper · Rule #40 `.uc-email` · hardcoded font-size ใน sidebar — เหมือนไฟล์ canonical)
  - `prune_css.py` → ตัด rule 70 · ลด 6.4 KB → รัน `audit.sh` ซ้ำ **FAIL = 0** เท่าเดิม
  - มี `<meta cube-archetype>` ✓ · `window.__QA__` ✓ · ตรวจ syntax JS ด้วย `node --check` ผ่าน
  - **ตรวจเพิ่มแทน e2e:** รัน `tplRender` ที่ฝังใน prototype เทียบกับ `render_doc.py` ฝั่ง server ครบทั้ง 5 สถานะ → **IDENTICAL 5/5** (ยืนยันว่า PDF ใน prototype กับ PDF ฝั่งระบบจริงออกมาเหมือนกัน)
- `[NO-BROWSER] ข้าม e2e_standard.py` — ด่าน e2e (21 เคส) ยังไม่ได้รัน ต้องรันบนเครื่องที่มี browser ก่อน UAT
- `[NO-BROWSER] ข้าม render-check.py` — ยังไม่ได้ตรวจ visual (Thai rhythm · empty state · sticky · ปุ่ม)
- 2026-10-07 12:45 · ขั้น 5 → done
- 2026-10-07 12:45 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- `BRD_F-TMP-002.md` (Prebrief Mode · DEC = Scope Lock §3.4) — §2.1 ตัวชี้วัด 3 ตัว (2 ตัวระบุว่าต้องเก็บ baseline ก่อน launch) · §6 Data Entity ครบ 8 ช่อง · §9 BR 13 ข้อ + Edge Case 8 · §14.6 Screen Inventory สกัดจาก prototype จริง · §18 Quality Gate C01–C23 → **Status: APPROVED**
- `FRD_F-TMP-002_Pack` **FULL (9 ไฟล์ + INDEX)** — fallback จาก BRD: pages 4 · states 5 · approval Yes
  - 03_LOGIC: MEM-FN-01…FN-10 · จุดออกเลข ENG-DOC-NUM ที่ FN-01 · เก็บสำเนา ENG-DOC-STORE ที่ FN-09 · `mem_cancelled` ที่ FN-06
  - 05_RULES: VR-01…VR-04 ผูกกับ DEC-12…DEC-15 ตรงตัว
  - 07_LOCKED_DECISIONS: DEC-01…DEC-15 ครบ + ตาราง "ใช้ที่ไหนใน FRD นี้" + convention deviations 4 ข้อ
- ด่าน `frd_lint.py` (Section N) → **BLOCK 0 · WARN 0 · PASS 11** → `reports/_SECTION_N.md`
- ใส่ `frd_ref` ตามที่ lint พิมพ์ (`03_LOGIC MEM-FN-01` / `MEM-FN-09` / `MEM-FN-06`) แล้วออก declaration ฉบับจริง:
  - `doccfg_tool.py brief --final --registry doccfg_registry_codes.txt` → **PASS** (รหัส MEM ไม่ชน)
  - `ntf_tool.py brief --final` → **PASS**
  - `doa_tool.py brief --print-config` → **PASS**
  - `mdoc_tool.py brief --doccfg` → **WARN (BLOCK 0)** — taxonomy_def_id ว่าง · doa = pending
  - ไม่เหลือป้าย "ร่าง — ยืนยันหลัง FRD" ในใบประกาศใด
- 2026-10-07 12:56 · ขั้น 7 → done

## ขั้น 8 · UI Brief → test case AI → UAT
- `extract_anchors.py` → `reports/inventory.json` (CSS var 47 · z-index 21 · route 5 · overlay 33 · toast 12 · ปุ่ม 20 · function 158 · archetype Q-form · `__QA__` ✓)
- `UI_BRIEF_F-TMP-002.md` ครบ §0–§13 · `brief_check.py` → **PASS · FAIL 0 · WARN 0** (B1 route 5/5 · B2 toast คงที่ 12/12 · B5 anchor มีจริงทั้งหมด (fn 58 · class 88 · id 22) · B6 CSS var 47/47 = 100% · B7 microcopy 75%)
- `testcases-F-TMP-002.md` **37 เคส · 157 step** (C 5 · S 4 · A 2 · R 3 · X 2 · P 6 · E 5 · D 5 · L 5) + Coverage Ledger + Coverage Audit + Result schema
  - `tc_lint.py` → **ERROR 0** (แก้ 3 step ที่ไม่ขึ้นต้น verb tag แล้ว)
  - `verify_anchors.py` รันได้แบบ **source-only** (ไม่มี browser) → MISSING 1 และติดธง ⚠ แล้ว ⇒ "anchor ไม่พบที่ไม่ได้ติดธง = 0" ผ่าน · `[NO-BROWSER] verify_anchors.py โหมด DOM ข้าม` (ยังไม่ได้ยืนยัน anchor จากหน้าจอจริง)
- เอกสาร UAT ฝั่งคน: `cases.json` โหมด **Lite 28 เคส** (id เดิมจาก MD) + `QA_AUDIT_F-TMP-002.md` drop ledger 9 เคส พร้อมเหตุผทุกข้อ
  - `lite_audit.py --stamp` → **หายเงียบ 0 · ERROR 0** · ประทับ md5 ต้นทางลง `cases.json` แล้ว
  - `regionKey` ว่างทุกขั้น เพราะถ่ายภาพไม่ได้ · `[NO-BROWSER] ข้าม capture.py` และ `[NO-BROWSER] ข้าม build.py` → **ยังไม่มี `testcase-F-TMP-002.html` ให้ผู้ทดสอบ**
- 2026-10-07 13:14 · ขั้น 8 → done
