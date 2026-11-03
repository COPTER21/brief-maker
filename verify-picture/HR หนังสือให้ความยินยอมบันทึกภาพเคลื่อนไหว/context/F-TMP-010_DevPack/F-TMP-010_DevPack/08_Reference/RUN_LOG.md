# RUN_LOG — F-TMP-010 หนังสือให้ความยินยอมในการบันทึกและเผยแพร่ภาพถ่าย หรือภาพเคลื่อนไหว (REQ-TMP-010)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)
> โหมด: unattended · NO-BROWSER

## ขั้น 1 · อ่านฟอร์ม + PREBRIEF v2 (2026-10-07)
- `to_image.py` แปลง .docx → LibreOffice → PDF → `page-1.png` / `page-2.png` (2 หน้า) + `content.html` — ภาพเป็นหน้ากระดาษจริงจาก PDF ใช้เทียบโครงเส้น/ตำแหน่งได้ (ฟอนต์ไทยในภาพเป็นกล่อง ตาม E2)
- หัวฟอร์มจริง = "หนังสือให้ความยินยอมในการบันทึกและเผยแพร่ภาพถ่าย หรือภาพเคลื่อนไหว" → `dm.sh rename J010` แล้ว (ชื่อไฟล์เดิมสั้นกว่า ไม่ตรงหัวฟอร์ม — anomaly A7)
- Doc No. **FM-HRM-51** · Rev. 00 : 01/07/2569 · A4 แนวตั้ง 2 หน้า · โลโก้ Credence กลางหัวกระดาษทั้ง 2 หน้า
- FORM_SPEC: **17 ช่อง** (กรอก 13 · คำนวณ 2 · ระบบใส่ 2) · ตัวเลือก 3 (ข้อ 1–3 · ยินยอม/ถอนความยินยอม) · ลายเซ็น 2 (ผู้ให้ความยินยอม · ผู้ปกครองของผู้เยาว์) · ค่าคงที่ 4 · ข้อมูลขัดกัน 7
- `form_spec_check.py` → **ERROR 0** · gate ที่ต้องถาม G1 G3 G5 G6 G8 G9 G10 (ไม่มีช่องผู้อนุมัติบนกระดาษ → ไม่ขึ้น G2/G7)
- ถ้อยคำทางกฎหมายคัดตรงตัวจาก `orig/content.src.txt` ทุกย่อหน้า (ห้ามเรียบเรียง) · คำสะกดผิด/ไม่สม่ำเสมอคงไว้แล้วบันทึกเป็น anomaly
- [BUG-WORKAROUND P1] `impact_summary.py` regex ไม่รับ `REQ-TMP-010` → ทำสำเนาเป็น REQ-2569-0010 รัน แล้ว sed แทนกลับ
- [BUG-WORKAROUND M1] ย้าย `orig/content.html` → `orig/content.src.txt` กัน manifest_scan K2 นับซ้ำกับ feature.html
- PDPA: 11 ช่องติด `pdpa: true` (ชื่อ · อายุ · เลขบัตรประชาชน ของผู้ให้ความยินยอม/ผู้ปกครอง/ผู้เยาว์) · ต้นฉบับเป็นฟอร์มเปล่า ไม่มีข้อมูลบุคคลจริง → prototype ใช้ชื่อสมมติทั้งหมด + โลโก้ placeholder
- 2026-10-07 16:40 · ขั้น 1 → done

## ขั้น 2 · Gate 10 หมวด → DECISIONS.lock (2026-10-07)
- ตอบเองตาม `unattended-policy.md` — เหตุผลรายหมวด:
  - G1 ไม่เปลี่ยน config / ไม่ส่งต่อระบบอื่น — หนังสือยินยอมเป็นหลักฐาน ไม่ไปตั้งค่าใด (การบังคับใช้ผลความยินยอมกับงานสื่อ/การตลาดเป็นงานรอบถัดไป)
  - G2 `required: false` — กระดาษมีลายเซ็น 2 จุดคือ "ผู้ให้ความยินยอม" และ "ผู้ปกครองของผู้เยาว์" ทั้งคู่เป็นผู้ให้ความยินยอม ไม่ใช่ผู้อนุมัติ → ไม่มีสาย DOA (ตามสูตร "ค่าเริ่ม = จำนวนช่องผู้อนุมัติบนกระดาษ")
  - G3 เกณฑ์ผู้เยาว์ · ชื่อ/ที่อยู่/อีเมลบริษัท อ่านจาก config · ข้อ 1-3 บังคับเลือก 1 ใน 2 · ใบที่ยืนยันแล้ว immutable
  - G4 ไม่มี repeat group → [BUG-KNOWN O1] `decisions_lock.py` ยังออก DEC-05 (G4) ให้ โดย min_rows = None — ปล่อยได้ ไม่มีผลกับด่าน
  - G5 1:1 ไม่เพิ่มช่อง (รวมถึงไม่เพิ่ม "วันที่" ใต้ลายเซ็นผู้ปกครองที่กระดาษไม่มี — DEC-14)
  - G6 ลายเซ็นแถวล่าง ไม่ใช้ภาพลายมือชื่อ
  - G7 ไม่มีการอนุมัติ → `on_reject: back_to_draft` ประกาศไว้เฉย ๆ · ยกเลิกได้เฉพาะ ร่าง/รอยืนยัน · หลังยืนยันใช้ "ถอนความยินยอม"
  - G8 เจ้าของเห็นของตัวเอง · admin role (HR) เห็นทั้งหมด — เลขบัตรประชาชน + ข้อมูลผู้เยาว์ต้องจำกัดผู้เห็น
  - G9 ออกเลขตอนบันทึกครั้งแรก · รหัส **IMC** (ตรวจแล้วไม่ชนทะเบียน ACL MEM VAN TRV DSR CMP LOA TWP PDC)
  - G10 แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ (ความยินยอมทำซ้ำไม่ได้) · ประกาศ ✗
- `decisions_lock.py` → **พร้อมเริ่มทำ (exit 0)** · 17 มติ · `dm.sh tag J010` → **AI-DEFAULT 10 · VALID 7** (DEC-11..17 จาก anomalies)
- [BUG-WORKAROUND P1] impact_summary ฉบับยืนยัน ใช้วิธีสำเนา REQ-2569-0010 แล้วแทนกลับเหมือนขั้น 1
- 2026-10-07 16:41 · ขั้น 2 → done

## ขั้น 3 · ร่าง declaration (2026-10-07)
- **DOA**: `doa_tool.py init` ไม่ออกใบให้ (DECISIONS G2 = ไม่มีผู้อนุมัติ · exit 1 by design) แต่ feature เข้าเกณฑ์ Trigger Rule ของสกิล (ออก PDF + มีช่องลายเซ็น + schema มี `approval_chain`)
  → เขียน `IMC.doa.yaml` เองตาม §Interview (กันบั๊ก M5 ที่ขั้น 9): `approval_required: false` · `matrix[0].steps: []` · `mode: dynamic` · `on_reject: back_to_draft` (D1) · `platform: hr_platform` (D2)
  → `doa_tool.py brief` → **VERDICT PASS**
- **NTF**: suggest ได้ event ตั้งต้นที่ไม่เข้าเคส (`imc_cancelled` ส่งหา current_step_approver · `imc_over_limit_approved`) → แทนด้วย event ธุรกิจจริง 4 ตัว
  `imc_consent_recorded` (in-app · ปิดได้) · `imc_consent_withdrawn` (in-app+email · **ปิดไม่ได้** DEC-15) · `imc_minor_consent_recorded` (in-app · DEC-04) · `imc_cancelled` (in-app · DEC-07)
  ตัด doa_* ทั้งหมด (ไม่มีสายอนุมัติ) → `ntf_tool.py brief` → **VERDICT PASS · BLOCK 0**
- role ที่ใช้: `role-mgr-hr` · `role-compliance` — มีใน `doa-roles-contract.md` ทั้งคู่
- doccfg + mdoc เลื่อนไปทำหลังขั้น 4 (ต้องใช้ print_config.json)
- 2026-10-07 16:42 · ขั้น 3 → done

## ขั้น 4 · แบบพิมพ์ Replica + doccfg/mdoc (2026-10-07)
- โหมด **Replica** · `print/form.tpl.html` ใช้ R1 โลโก้ · R2 ชื่อเอกสาร · R3 form-date (เขียนที่ / วันที่ ชิดขวา) · R4 บรรทัดกรอก · R6 form-check (ยินยอม/ถอนความยินยอม ต่อข้อ) · R7 ย่อหน้ากฎหมาย · B6 sign_rows · B7 footer
- ถ้อยคำกฎหมายทุกย่อหน้าอยู่ใน template ตรงตัวตามกระดาษ (คงคำสะกดที่ไม่สม่ำเสมอ: บูท/บูธ · "เป็นผู้ปกครองของ ข้าพเจ้า" · "ข้อมูลส่วนของบุคคล") · ชื่อ/ที่อยู่/อีเมลบริษัท + เกณฑ์ผู้เยาว์เป็น `{{company.*}}` / `{{policy.minor_age}}` อ่านจาก config (DEC-04)
- `profile.json`: form_fs 9pt · form_title_fs 12pt · form_logo_h 13mm · form_para_gap 9px/6px · form_row_gap 7px · form_indent 10mm · form_date_w 52mm
- data 5 สถานะ (`make_data.py`): draft · approved (ยินยอมครบ 3 ข้อ) · rejected (ถอนความยินยอมข้อ 3) · long-withdrawn (ผู้เยาว์ + ผู้ปกครอง + ถอนทั้งฉบับ + dense) · approved-doa6steps (chain 6 ขั้น → 8 ช่อง 2 แถว 4+4)
- **ช่องลงชื่อ = ผู้ให้ความยินยอม + ผู้ปกครอง (ช่องคงที่ตามกระดาษ) + 1 ช่องต่อขั้น DOA** — ไม่ fix จำนวน (`sign_boxes` มี `guardian` เพิ่มจาก template มาตรฐาน)
- **ชื่อบุคคลในตัวอย่างเป็นชื่อสมมติทั้งหมด · เลขบัตรประชาชนเป็น `0 0000 00000 00 0`** (ต้นฉบับเป็นฟอร์มเปล่า ไม่มีข้อมูลบุคคลจริง) · โลโก้เป็น placeholder SVG ไม่ใช่โลโก้ลูกค้า
- `parity_check.py` → **✅ IDENTICAL 5/5** ไม่มีคำเตือน · `render_doc.py --strict` ผ่านทั้ง 5 · ไม่มี `{{}}` หลง
- [NO-BROWSER] ข้าม `render_states.py` · `render_pdf.py` · `compare_original.py` → แทนด้วย `render_doc.py --strict` + `build_html.py` (HTML ครบ 5 สถานะ + `IMC_template.html`) และ **stub DOM smoke test** `print/check_states.js` (node) → **PASS 100 · FAIL 0**
  **ค้าง:** PDF · จำนวนหน้า · `_states_sheet.png` · `compare_side.png` → ต้องรันรอบเต็มบนเครื่องที่มี browser (บันทึกใน print-spec §6)
- ความต่างจากกระดาษที่ตั้งใจ 6 ข้อ บันทึกใน `print/IMC_print-spec.md` §7 (ข้อสำคัญ: ย้ายบล็อกลงชื่อ 2 จุดมารวมแถวล่าง · เพิ่มบรรทัดวันที่ใต้ลายเซ็นผู้ปกครองที่กระดาษไม่มี)
- `doccfg_tool.py init` + `brief --registry` → **VERDICT PASS** · รหัส **IMC** ไม่ชนทะเบียน · แก้ `snapshot.approved_final = true` + snapshot_points (เก็บสำเนา PDF เป็นหลักฐานความยินยอมตอนยืนยัน — บังคับตาม PDPA)
- `mdoc_tool.py brief --doccfg` → **VERDICT WARN** (G04 ยังไม่มี taxonomy_def_id — บั๊กรู้แล้ว D3) · **BLOCK 0** · `doa: none`
  ⚠ `function_code: F01` เลือกตามรูปแบบเท่านั้น — Taxonomy Master (F-90) ไม่มีในโฟลเดอร์นี้ ต้องให้คนยืนยัน
- `doa_tool.py validate --print-config` → **VERDICT PASS**
- 2026-10-07 16:50 · ขั้น 4 → done

## ขั้น 5 · HTML Q-form + gate (2026-10-07)
- Pattern **Q2 (Q-form)** — `<meta name="cube-archetype" content="Q-form">` · ต่อยอดจาก `_SOURCE_form-request-reference.html` (BASE-KIT v6.4 + CSS) แล้วเขียนโซน domain ใหม่ทั้งหมดสำหรับ IMC (`build/domain_a..f.js` + `build/assemble.py`)
- Surface 1 list: เลขที่ · วันที่ให้ความยินยอม · ผู้ให้ความยินยอม · บูธกิจกรรม · ยินยอม n/3 · ช่วงอายุ (ผู้เยาว์/บรรลุนิติภาวะ) · สถานะ · ลายเซ็น · ⋮ (แก้ไข[ร่าง] · พิมพ์ · ถอนความยินยอม · ยกเลิก)
- Surface 2 wizard 3 ขั้น: `ข้อมูลผู้ให้ความยินยอม` › `เอกสารแนบ` › `ตรวจสอบและยืนยัน` · การ์ด 5 ก้อน (หัวหนังสือ · ผู้ให้ความยินยอม · บูธกิจกรรม · ความยินยอม 3 ข้อแบบ `.track-card` · ส่วนผู้เยาว์ที่เปิดอัตโนมัติเมื่ออายุต่ำกว่าเกณฑ์ใน config) + การ์ดสรุปสดด้านขวา
- Surface 3 view tabs: รายละเอียด › PDF Preview › ลายเซ็น / อนุมัติ › ประวัติ (Rule #101 ครบ)
- Surface 4: `MOCK_DOA_RESOLVED.steps = []` (DEC-03 ไม่มีผู้อนุมัติบนกระดาษ) แต่ **ไม่ fix สาย** — `Q.doa.push()` เพิ่มขั้นที่ DOA กลางแล้วฟีเจอร์รับได้ทันที (ทดสอบแล้ว S32/S33/S35) · PDF ฝัง `print/form.tpl.html` + `tplRender` + `tplSignRows`
- ของเพิ่มตามมติ: **ถอนความยินยอมรายข้อ** (DEC-15/DEC-16) ผูกกับใบเดิม เก็บวันที่/ผู้บันทึก/เหตุผล · ใบที่ยืนยันแล้ว immutable (DEC-04) · บังคับเลือกครบ 3 ข้อ (DEC-13) · เกณฑ์ผู้เยาว์อ่านจาก `MINOR_AGE` (config) ห้าม hardcode rule
- ด่าน: `audit.sh` → **FAIL 0 · WARN 3** (WARN ทั้ง 3 มาจาก BASE-KIT เดิม: data-lucide ใน helper กลาง · `.uc-email` · font-size ของ sidebar)
- `self_audit.py` → **PASS** (รอบแรก FAIL `missing_ids = ['f-']` เพราะ `getElementById('f-' + path)` เป็น id ที่ประกอบตอนรัน → เปลี่ยนเป็น `data-fld` + `querySelector`)
- `prune_css.py` → ตัด 36 rule (−3.3 KB) แล้วรัน audit + self_audit + e2e ซ้ำ ผ่านทั้งหมด (ไม่เหลือไฟล์ `*.prepruned.html`)
- [NO-BROWSER] ข้าม `e2e_standard.py` · `render-check.py` → แทนด้วย **stub DOM smoke test** `build/e2e_stub.js` (node + `build/stub_dom.js`) → **PASS 50/50** (`reports/e2e_stub_report.txt`)
  ครอบ: route · tabs · seed ครบทุกสถานะ · การมองเห็น (ร่างคนอื่นไม่รั่ว · HR เห็นหมด) · แก้ไขเฉพาะร่างตัวเอง · ตรวจช่องตามกระดาษครบ (ชื่อ/เลขบัตร/ช่วงวันที่) · กฎผู้เยาว์ต้องมีผู้ปกครอง · PDF ไม่มี {{}} + 3 ชุดตัวเลือก + 6 ช่องติ๊ก + 2 ช่องลงชื่อ + ถ้อยคำกฎหมายตรงตัว (รวมคำสะกดที่ไม่สม่ำเสมอของต้นฉบับ) · DOA dynamic เพิ่ม/ถอดขั้น (ช่องลงชื่อเพิ่มตาม) · ยืนยัน → immutable · ถอนความยินยอมรายข้อ + เหตุผลบังคับ · ปิดใช้แบบเอกสาร · API ล้ม
  **ค้าง:** ภาพหน้าจอจริง + viewport/visual check ต้องรันบนเครื่องที่มี browser (`e2e_standard.py` · `render-check.py` · `capture.py`)
- 2026-10-07 17:06 · ขั้น 5 → done
- 2026-10-07 17:06 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง (2026-10-07)
- `BRD_F-TMP-010.md` (Prebrief Mode · STANDARD) — §2.4 Scope Lock = DECISIONS.lock (DEC-01..17 ผูกครบทุกข้อพร้อมคอลัมน์ "ใช้ที่ไหนใน BRD นี้" กันบั๊ก M4) · §13 Open Questions OQ-01..OQ-08 · §14 Security (เลขบัตรประชาชน + choice = Restricted) · สถานะ **APPROVED (AI-DEFAULT)**
- `FRD_F-TMP-010_Pack/` 9 ไฟล์ (INDEX · 00..07) — 03_LOGIC FN-01..FN-12 · 04_DB 4 ตาราง (+Document Center) พร้อม `header_snapshot` · `approval_chain` · `doa_ref` + `TODO: DOA engine`
- `frd_lint.py` (Section N) → **BLOCK 0 · WARN 0 · PASS 16** (`reports/_SECTION_N.md`) — ผ่านรอบแรก
  - N3 ผ่านเพราะเลี่ยงเขียนเลขเกณฑ์ผู้เยาว์ตรง ๆ ใน 03/05 (อ้าง `PdpaPolicy.minor_age_threshold` แทน ตามบทเรียน F1)
- declaration ฉบับจริง: `doccfg_tool.py brief --final --registry` → **PASS** (`numbering.frd_ref = 03_LOGIC F-TMP-010-FN-03` · `snapshot_points[0].frd_ref = …FN-06`) · `ntf_tool.py brief --final` → **PASS** (frd_ref ครบ 4 event) · `mdoc_tool.py brief` → **WARN** (G04 taxonomy_def_id ว่าง · BLOCK 0) · `doa_tool.py brief --print-config --html` → **PASS** (marker DOA-ENGINE-HOOK มีใน HTML · sign_boxes ครบ)
- ยังไม่ได้ทำ `.docx` ของ BRD (ไม่มีขั้นตอน/สคริปต์ในโฟลเดอร์นี้) — ส่งเป็น .md
- 2026-10-07 17:20 · ขั้น 7 → done

## ขั้น 8 · UI Brief → test case AI → UAT (2026-10-07)
- `extract_anchors.py` → `reports/inventory.json` (css var 47 · z-index 21 · overlay 33 · toast 12 · ปุ่ม 26 · microcopy 284 · function 187 · archetype Q-form · `__QA__` true)
- `UI_BRIEF_F-TMP-010.md` (§0–§13 + §9.1) → `brief_check.py` **PASS · FAIL 0 · WARN 0** (B1–B8 ผ่านหมด · CSS vars 47/47 · microcopy 45/60)
  - รอบแรก WARN B7 (27/60 = 45%) → เติม §9.1 microcopy เพิ่มเติม (ป้ายช่อง · placeholder · สถานะ · เดือนไทย) ให้ถึง 75%
- `testcases-F-TMP-010.md` (AI agent) → `tc_lint.py` **32 เคส · 136 step · ERROR 0** (`reports/tc_counts.json`) — เขียน Meta หลังนับเคสเสร็จตามบทเรียน F4
- `verify_anchors.py` รันได้ในโหมด **source อย่างเดียว** (ไม่มี browser) → **MISSING 0** (`reports/anchors.json` · SOURCE 220 · PATTERN 1 · DATA 1)
- `cases.json` (แบบทดสอบฉบับผู้ใช้ 29 เคส · 9 กลุ่ม · สร้างด้วย `build/make_cases.py`) + `QA_AUDIT_F-TMP-010.md` (drop ledger 3 เคสที่ต้องสั่งผ่าน console: TC-S03 · TC-K01 · TC-E01)
- `lite_audit.py --stamp` → **หายเงียบ 0** · ประทับ meta.source แล้ว
- `build.py` → `testcase-F-TMP-010.html` (1,254 KB · 29 เคส · 9 กลุ่ม)
- [NO-BROWSER] ข้าม `capture.py` → ไม่มีภาพประกอบ (`regions 0`) · `reports/shots_b64.json` ว่าง · ต้องรัน capture บนเครื่องที่มี browser ถ้าต้องการภาพในแบบทดสอบ
- 2026-10-07 17:37 · ขั้น 8 → done

## ขั้น 9 · ตรวจรวม + แพ็ก DevPack (2026-10-07)
- `manifest_scan.py` → ซ้ำ 0 ตั้งแต่รอบแรก (ย้าย `orig/content.html` → `content.src.txt` ตั้งแต่ขั้น 1 ตามบทเรียน M1 · `prune_css.py` ไม่ทิ้งไฟล์ `*.prepruned.html` ไว้จึงไม่ติด M2)
- `consistency_check.py` รอบแรก → **READY · BLOCK 0 · WARN 1 · PASS 10**
  - K7 ผ่านตั้งแต่รอบแรกเพราะเขียน `IMC.doa.yaml` เองตั้งแต่ขั้น 3 (กันบั๊ก M5 ที่ J008 เจอ)
  - WARN เดียว = K9 "ไม่มี report e2e_standard" → เป็นผลของโหมด NO-BROWSER (มี `reports/e2e_stub_report.txt` แทน) ต้องรัน `e2e_standard.py` บนเครื่องที่มี browser ก่อนส่งลูกค้า
- ลำดับที่ใช้: `mark 9 done` → `manifest_scan` → `pack` → `finish` (ตามบทเรียน S1)
- 2026-10-07 17:37 · ขั้น 9 → done
