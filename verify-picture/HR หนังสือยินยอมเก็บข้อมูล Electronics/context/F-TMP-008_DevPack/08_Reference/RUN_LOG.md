# RUN_LOG — F-TMP-008 หนังสือยินยอม PDPA กรณีสมัครงาน (REQ-TMP-008)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · อ่านฟอร์ม + PREBRIEF v2 (2026-10-07)
- `to_image.py` แปลง .docx → LibreOffice → PDF → `page-1.png` / `page-2.png` (2 หน้า) + `content.html` — **ภาพเป็นหน้ากระดาษจริงจาก PDF** (ไม่ใช่ HTML snapshot) ใช้เทียบ layout ได้
- หัวฟอร์มจริง = "หนังสือยินยอมในการเก็บรวบรวม ใช้ และเปิดเผยข้อมูลส่วนบุคคล" → `dm.sh rename J008` แล้ว (ชื่อเดิม "หนังสือยินยอม PDPA กรณีสมัครงาน" เป็นชื่อไฟล์ ไม่ใช่หัวฟอร์ม)
- Doc No. FM-HRM-31 · Rev. 00 : 01/07/2569 · A4 แนวตั้ง 2 หน้า · โลโก้ Credence
- FORM_SPEC: 3 ช่อง (กรอก 1 · คำนวณ 1 · ระบบใส่ 1) · ตัวเลือก 8 (ตารางความยินยอม ข้อ 1-8 · ยินยอม/ไม่ยินยอม) · ลายเซ็น 1 (เจ้าของข้อมูล) · ค่าคงที่ 4 · ข้อมูลขัดกัน 5
- `form_spec_check.py` → **ERROR 0** · gate ที่ต้องถาม G1 G3 G5 G6 G8 G9 G10 (ไม่มีช่องผู้อนุมัติบนกระดาษ → ไม่ขึ้น G2/G7)
- ถ้อยคำทางกฎหมายคัดตรงตัวจาก `orig/content.src.txt` ทุกย่อหน้า (ห้ามเรียบเรียง) · ตำแหน่ง/เส้นตารางยึด page-N.png
- [BUG-WORKAROUND] `impact_summary.py` regex `REQ-[\d-]+` ไม่รับ `REQ-TMP-008` → ทำสำเนาเป็น REQ-2569-0008 รัน แล้ว sed แทนกลับ
- [BUG-WORKAROUND] ย้าย `orig/content.html` → `orig/content.src.txt` กัน manifest_scan K2 นับซ้ำกับ feature.html
- PDPA: ชื่อเจ้าของข้อมูล + ชื่อตัวบรรจง ติด `pdpa: true` · ต้นฉบับเป็นฟอร์มเปล่า ไม่มีข้อมูลบุคคลจริง → prototype ใช้ชื่อสมมติทั้งหมด
- 2026-10-07 15:33 · ขั้น 1 → done

## ขั้น 2 · Gate 10 หมวด → DECISIONS.lock (2026-10-07)
- ตอบเองตาม `unattended-policy.md` — เหตุผลรายหมวด:
  - G1 ไม่เปลี่ยน config / ไม่ส่งต่อระบบอื่น — หนังสือยินยอมเป็นหลักฐาน ไม่ไปตั้งค่าใด (การบังคับใช้ผลความยินยอมกับ module อื่นเป็นงานรอบถัดไป)
  - G2 `required: false` — กระดาษมีช่องลงชื่อจุดเดียวคือ "เจ้าของข้อมูลส่วนบุคคล" ไม่มีช่องผู้อนุมัติ → ไม่มีสาย DOA (ตามสูตร "ค่าเริ่ม = จำนวนช่องผู้อนุมัติบนกระดาษ")
  - G3 ถ้อยคำกฎหมาย + ชื่อบริษัท + ลิงก์นโยบาย อ่านจาก config · ข้อ 1-8 บังคับเลือก 1 ใน 2 · ใบที่ยืนยันแล้ว immutable
  - G4 ไม่มี repeat group (ตาราง 8 ข้อเป็นรายการตายตัวจากฉบับของหนังสือ) — DEC-05 ที่ script ออกให้เป็นค่าว่าง ปล่อยได้ (บั๊กรู้แล้ว)
  - G5 1:1 ไม่เพิ่มช่อง · G6 ลายเซ็นแถวล่าง 1 ช่อง (เจ้าของข้อมูล) ไม่ใช้ภาพ
  - G7 ไม่มีการอนุมัติ → ไม่ออก DEC G7 · ยกเลิกได้เฉพาะสถานะร่าง หลังยืนยันใช้ "ถอนความยินยอม"
  - G8 เจ้าของเห็นของตัวเอง · ผู้ดูแล HR เห็นทั้งหมด (ข้อมูลอ่อนไหว ม.26 ต้องจำกัดผู้เห็น — DEC-15)
  - G9 ออกเลขตอนบันทึกครั้งแรก · รหัส **PDC** (ไม่ชนทะเบียน ACL MEM VAN TRV DSR CMP LOA)
  - G10 แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ (ความยินยอมทำซ้ำไม่ได้) · ประกาศ ✗
- `decisions_lock.py` → **พร้อมเริ่มทำ (exit 0)** · 15 มติ · `dm.sh tag J008` → AI-DEFAULT 10 · VALID 5 (DEC-11..15 จาก anomalies)
- 2026-10-07 15:34 · ขั้น 2 → done

## ขั้น 3 · ร่าง declaration (2026-10-07)
- **DOA: ไม่ทำ** — `doa_tool.py init` ออก "DEC: ไม่มีการอนุมัติ (doa.required=false) — ห้ามยัด DOA เข้า feature ที่ไม่มีอนุมัติ" (exit 1 by design) → ไม่มี DOA_BRIEF · ด่าน doa BLOCK 0 ผ่านโดยปริยาย
  - schema ยังคงประกาศ field `approver_role / approved_by / approval_chain` ว่างไว้ + marker `DOA-ENGINE-HOOK` ตามกติกา (ห้าม hardcode rule) เผื่อลูกค้าขอให้มีผู้รับรอง
- **NTF**: suggest ได้ event ตั้งต้นที่ไม่เข้าเคส (over_limit จาก G3) → แทนด้วย event ธุรกิจจริง 3 ตัว
  `pdc_consent_recorded` (in-app · ปิดได้) · `pdc_consent_withdrawn` (in-app+email · **ปิดไม่ได้** DEC-14) · `pdc_sensitive_refused` (in-app · DEC-15)
  ตัด doa_* ทั้งหมด (ไม่มีสายอนุมัติ) → `ntf_tool.py brief` **VERDICT PASS · BLOCK 0**
- doccfg + mdoc เลื่อนไปทำหลังขั้น 4 (ต้องใช้ print_config.json)
- 2026-10-07 15:36 · ขั้น 3 → done

## ขั้น 4 · แบบพิมพ์ Replica + doccfg/mdoc (2026-10-07)
- โหมด **Replica** (ลูกค้าส่งไฟล์มา) · `print/form.tpl.html` ใช้ R1 โลโก้ · R2 ชื่อเอกสาร · R4 บรรทัดกรอก · R7 ย่อหน้ากฎหมาย · **R9 ตารางกรอบ** (ตารางความยินยอม 8 ข้อ) · B6 sign_rows · B7 footer
- ถ้อยคำกฎหมาย 4 ย่อหน้าอยู่ใน template ตรงตัวตามกระดาษ (ห้ามเรียบเรียง) · ชื่อบริษัท/ลิงก์นโยบายเป็น `{{company.legal_name}}` / `{{policy.*}}` อ่านจาก Organization (DEC-04)
- `profile.json`: form_fs 9pt · form_title_fs 12pt · form_logo_h 13mm · form_para_gap 10px/7px · form_grid_gap 10px · form_indent 10mm
- data 5 สถานะ (`make_data.py`): draft · approved (ยินยอมทุกข้อ) · rejected (ไม่ยินยอมข้ออ่อนไหวบางข้อ) · long-withdrawn (ยาว + บล็อกถอนความยินยอม + dense) · approved-doa6steps (chain 6 ขั้น → 7 ช่อง 2 แถว)
- **ชื่อบุคคลในตัวอย่างเป็นชื่อสมมติทั้งหมด** (ต้นฉบับเป็นฟอร์มเปล่า ไม่มีข้อมูลบุคคลจริง) · โลโก้เป็น placeholder SVG ไม่ใช่โลโก้ลูกค้า
- `parity_check.py` → **✅ IDENTICAL 5/5** ไม่มีคำเตือน
- [NO-BROWSER] ข้าม `render_states.py` · `compare_original.py` · `render_pdf.py` → แทนด้วย `render_doc.py --strict` + `build_html.py` (ได้ HTML ครบ 5 สถานะ + `PDC_template.html`) และ **stub DOM smoke test** `print/check_states.js` (node) → **PASS ทุกสถานะ**
  ตรวจ: ไม่มี `{{}}` หลง · ตาราง 8 แถว · ช่องติ๊ก 16 ช่อง · ร่างยังไม่ติ๊ก / ใบที่ยืนยันติ๊กครบ 8 · ช่องลงชื่อ 1 (ปกติ) / 7 (chain 6 ขั้น) · ถ้อยคำกฎหมายครบ 4 ย่อหน้า · footer Doc No. + CUBE NATIVE
  **ค้าง:** PDF · จำนวนหน้า · `_states_sheet.png` · `compare_side.png` → ต้องรันรอบเต็มบนเครื่องที่มี browser (บันทึกใน print-spec §6/§7/§8)
- ความต่างจากกระดาษที่ตั้งใจ 5 ข้อ บันทึกใน `print/PDC_print-spec.md` §7 (ข้อสำคัญ: คอลัมน์เลขลำดับรวมกับคอลัมน์ "ข้อมูลส่วนบุคคล" เพราะ `.form-grid` เป็น table-layout:fixed และมีเฉพาะ g-25/50/75)
- `doccfg_tool.py init` + `brief --registry` → **VERDICT PASS** · รหัส **PDC** ไม่ชนทะเบียน · แก้ `snapshot.approved_final = true` + snapshot_points (เก็บสำเนา PDF เป็นหลักฐานความยินยอมตอนยืนยัน — บังคับตาม PDPA)
- `mdoc_tool.py brief --doccfg` → **VERDICT WARN** (G04 ยังไม่มี taxonomy_def_id — เข้าคิว definition ใหม่) · **BLOCK 0** · `doa: none`
  ⚠ `function_code: F01` เลือกตามรูปแบบเท่านั้น — Taxonomy Master (F-90) ไม่มีในโฟลเดอร์นี้ ต้องให้คนยืนยัน
- `doa_tool.py validate` ไม่ได้รัน — ไม่มี `.doa.yaml` (ไม่มีสายอนุมัติ)
- 2026-10-07 15:45 · ขั้น 4 → done

## ขั้น 5 · HTML Q-form + gate (2026-10-07)
- Pattern **Q2 (Q-form)** — `<meta name="cube-archetype" content="Q-form">` · ต่อยอดจาก `_SOURCE_form-request-reference.html` (BASE-KIT v6.4 + CSS) แล้วเขียนโซน domain ใหม่ทั้งหมดสำหรับ PDC (`build/domain_a..f.js` + `build/assemble.py`)
- Surface 1 list: เลขที่ · วันที่ให้ความยินยอม · เจ้าของข้อมูล · ฝ่าย · ยินยอม n/8 · ข้อมูลอ่อนไหว · สถานะ · ลายเซ็น · ⋮ (แก้ไข[ร่าง] · พิมพ์ · ถอนความยินยอม · ยกเลิก)
- Surface 2 wizard 3 ขั้น: `ข้อมูลหลักหนังสือยินยอม` › `เอกสารแนบ` › `ตรวจสอบและยืนยัน` · 8 ข้อเป็นการ์ดละข้อ + `.track-card` ยินยอม/ไม่ยินยอม (Rule #107) · การ์ดสรุปสดด้านขวา
- Surface 3 view tabs: รายละเอียด › PDF Preview › ลายเซ็น / อนุมัติ › ประวัติ (Rule #101 ครบ)
- Surface 4: `MOCK_DOA_RESOLVED.steps = []` (DEC-03 ไม่มีผู้อนุมัติบนกระดาษ) แต่ **ไม่ fix สาย** — `Q.doa.push()` เพิ่มขั้นที่ DOA กลางแล้วฟีเจอร์รับได้ทันที (ทดสอบแล้ว S23/S24) · PDF ฝัง `print/form.tpl.html` + `tplRender` + `tplSignRows` (ช่องลายเซ็นวนจากข้อมูล)
- ของเพิ่มตามมติ: **ถอนความยินยอมรายข้อ** (DEC-14) ผูกกับใบเดิม เก็บวันที่/ผู้บันทึก/เหตุผล · ใบที่ยืนยันแล้ว immutable (DEC-04) · บังคับเลือกครบ 8 ข้อ (DEC-13) · ป้ายข้อมูลอ่อนไหว ม.26 (DEC-15)
- ด่าน: `audit.sh` → **FAIL 0 · WARN 3** (WARN ทั้ง 3 มาจาก BASE-KIT เดิม: data-lucide ใน helper กลาง · `.uc-email` · font-size ของ sidebar)
- `self_audit.py` → **PASS** (รอบแรก FAIL `naked_hints = 7` → ย้ายถ้อยคำกฎหมายยาวออกจาก class `hint/help` ไปใช้ `.tl-body` และย่อข้อความช่วยให้ ≤60 ตัวอักษร)
- `prune_css.py` → ตัด 35 rule (−3.2 KB) แล้วรัน audit + self_audit + e2e ซ้ำ ผ่านทั้งหมด
- [NO-BROWSER] ข้าม `e2e_standard.py` · `render-check.py` → แทนด้วย **stub DOM smoke test** `build/e2e_stub.js` (node + `build/stub_dom.js` จำลอง DOM/BASE-KIT helper แล้ว eval โซน domain จาก feature.html) → **PASS 39/39** (`reports/e2e_stub_report.txt`)
  ครอบ: route · tabs · seed ครบทุกสถานะ · การมองเห็น (ร่างคนอื่นไม่รั่ว · HR เห็นหมด) · แก้ไขเฉพาะร่างตัวเอง · บังคับเลือกครบ 8 ข้อ · PDF ไม่มี {{}} + 8 แถว + 16 ช่องติ๊ก + ถ้อยคำกฎหมายตรงตัว · DOA dynamic เพิ่ม/ถอดขั้น · ยืนยัน → immutable · ถอนความยินยอม + เหตุผลบังคับ · ปิดใช้แบบเอกสาร · API ล้ม
  **ค้าง:** ภาพหน้าจอจริง + viewport/visual check ต้องรันบนเครื่องที่มี browser (`e2e_standard.py` · `render-check.py` · `capture.py`)
- 2026-10-07 16:02 · ขั้น 5 → done
- 2026-10-07 16:02 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง (2026-10-07)
- `BRD_F-TMP-008.md` (Prebrief Mode · STANDARD) — §2.4 Scope Lock = DECISIONS.lock (DEC-01..15) · §13 Open Questions OQ-01..OQ-08 · §14 Security (ม.26 = Restricted) · สถานะ **APPROVED (AI-DEFAULT)**
- `FRD_F-TMP-008_Pack/` 9 ไฟล์ (INDEX · 00..07) — 03_LOGIC FN-01..FN-10 · 04_DB 4 ตาราง (+attachment) พร้อม `header_snapshot` · `approval_chain` · `doa_ref` · Data Classification Restricted ที่ `pdpa_consent_line.choice`
- `frd_lint.py` (Section N) → **BLOCK 0 · WARN 1 · PASS 12** (`reports/_SECTION_N.md`)
  - WARN N3 เป็น false positive: regex จับเลข "8" จากคำว่า **R8** ในบรรทัด "ทุก mutation API มี FN ปลายทางครบ (R8)" ไม่ใช่การ hardcode จำนวนข้อความยินยอม (03/05 เลี่ยงเลขจำนวนข้อโดยอ้าง "ทุกข้อในรายการของฉบับ" แทน)
- declaration ฉบับจริง: `doccfg_tool.py brief --final --registry` → **PASS** (`numbering.frd_ref = 03_LOGIC F-TMP-008-FN-03` · `snapshot_points[0].frd_ref = …FN-08`) · `ntf_tool.py brief --final` → **PASS** (frd_ref ครบ 3 event) · `mdoc_tool.py brief` → **WARN** (G04 taxonomy_def_id ว่าง · BLOCK 0)
- ไม่มี DOA_BRIEF (DEC-03) — บันทึกเป็น CD-02 ใน 07 §7.2
- ยังไม่ได้ทำ `.docx` ของ BRD (ไม่มีขั้นตอน/สคริปต์ในโฟลเดอร์นี้) — ส่งเป็น .md
- 2026-10-07 16:14 · ขั้น 7 → done

## ขั้น 8 · UI Brief → test case AI → UAT (2026-10-07)
- `extract_anchors.py` → `reports/inventory.json` (css var 47 · z-index 21 · overlay 33 · toast 12 · ปุ่ม 25 · microcopy 230 · function 174 · archetype Q-form · `__QA__` true)
- `UI_BRIEF_F-TMP-008.md` (§0–§13) → `brief_check.py` **PASS · FAIL 0 · WARN 0** (B1–B8 ผ่านหมด · CSS vars 47/47 · microcopy 59/60 · anchor ที่อ้างมีจริงทุกตัว)
- `testcases-F-TMP-008.md` (AI agent) → `tc_lint.py` **27 เคส · 87 step · ERROR 0** (`reports/tc_counts.json`)
  - รอบแรก ERROR 1 "Meta บอก 26 เคส แต่มี 27" → แก้ Meta + ตาราง Coverage ให้ตรง
- `verify_anchors.py` รันได้ในโหมด **source อย่างเดียว** (ไม่มี browser) → **MISSING 0** (`reports/anchors.json`)
  - รอบแรก MISSING 1 (`Doc No. FM-HRM-31` ไม่มีเป็นข้อความต่อเนื่องในโค้ด เพราะ template ใช้ `Doc No. {{doc.form_code}}`) → แก้ anchor เป็น `FM-HRM-31`
- `cases.json` (แบบทดสอบฉบับผู้ใช้ 24 เคส · 7 กลุ่ม) + `QA_AUDIT_F-TMP-008.md` (drop ledger 3 เคสที่ต้องสั่งผ่าน console/master: TC-S03 · TC-K01 · TC-E01)
- `lite_audit.py --stamp` → **หายเงียบ 0** · ประทับ meta.source แล้ว
- `build.py` → `testcase-F-TMP-008.html` (1,240 KB · 24 เคส · 7 กลุ่ม)
- [NO-BROWSER] ข้าม `capture.py` → ไม่มีภาพประกอบ (`regions 0`) · `shots_b64.json` ว่าง · ต้องรัน capture บนเครื่องที่มี browser ถ้าต้องการภาพในแบบทดสอบ
- 2026-10-07 16:27 · ขั้น 8 → done
