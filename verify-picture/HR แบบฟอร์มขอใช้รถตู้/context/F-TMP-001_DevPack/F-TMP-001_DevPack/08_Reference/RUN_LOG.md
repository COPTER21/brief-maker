# RUN_LOG — F-TMP-001 HR แบบฟอร์มขอใช้รถตู้ (REQ-TMP-001)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)

## ขั้น 1 · อ่านฟอร์ม + PREBRIEF v2
- โหมด NO-BROWSER (CUBE_NO_BROWSER=1) — ข้ามคำสั่งที่ต้องเปิด browser ทุกขั้น และบันทึกไว้ทุกครั้ง
- ภาพฟอร์ม: `_system/tools/to_image.py` (LibreOffice → PDF → pypdfium2) ได้ `SAMPLE.pdf` + `page-1.png` `page-2.png` (2 หน้า · หน้า 2 = ส่วนล้นของบล็อกลงชื่อผู้อนุมัติ) + `content.html`
  - ภาพมาจาก PDF จริงของ LibreOffice → ใช้เทียบ layout/เส้น/ตำแหน่งได้ แต่ **ฟอนต์ไทยในเครื่องไม่มี → ตัวอักษรไทยในภาพเป็นกล่องว่าง** → ถ้อยคำทั้งหมดยึด `content.html` (ข้อความจริงจาก .docx)
- ชื่อไฟล์ไม่เพี้ยน และหัวฟอร์มอ่านได้ว่า "แบบฟอร์มขอใช้รถตู้" → ไม่ต้อง rename (ชื่องาน "HR แบบฟอร์มขอใช้รถตู้" ครอบคลุม module HR + ชื่อหัวฟอร์ม)
- FORM_SPEC.json: 22 ช่อง (ระบบ 5 · กรอก 15 · คำนวณ 1 · ระบบใส่ 1) · แถวซ้ำ 1 กลุ่ม (รายชื่อผู้เดินทาง 5 แถว) · ตัวเลือก 1 กลุ่ม (ลักษณะการเดินทาง 3 ตัวเลือก) · สูตร 1 · ค่าคงที่ 0 · ลายเซ็น 3 · ข้อมูลขัดกัน 3
- control: Doc No. FM-HRM-22 · Rev. 00 : 01/07/2569 · ไม่มีเลขที่รันบนกระดาษ
- **PDPA**: ต้นฉบับพิมพ์ชื่อบุคคลจริงไว้ใต้ช่องลงชื่อผู้จัดการฝ่ายทรัพยากรบุคคล → บันทึกเป็น anomaly · ห้ามใช้เป็นข้อมูลตัวอย่างใน prototype/แบบพิมพ์ (ใช้ชื่อสมมติ)
- form_spec_check: ERROR 0 · WARN 0 → ผ่านด่าน
- PREBRIEF v2 สร้างจาก FORM_SPEC (ไม่มี PREBRIEF จาก CMS) → coverage 22/22 "ครบ"
- [หมายเหตุเครื่องมือ] `impact_summary.py` อ่านเลขคำขอด้วย regex `REQ-[\d-]+` จึงไม่รับรหัสชั่วคราว `REQ-TMP-001` → รันด้วยสำเนาหัวเรื่องชั่วคราว แล้วแทนเลขกลับเป็น REQ-TMP-001 ในไฟล์ผลลัพธ์ (เนื้อหาเหมือนเดิมทุกประการ) → `IMPACT_SUMMARY_REQ-TMP-001.html/.json`
- 2026-10-07 12:14 · ขั้น 1 → done

## ขั้น 2 · gate 10 หมวด (โหมดไม่เฝ้า — AI ตอบเองตาม unattended-policy.md)
- G1 `config_changes: []` · `post_to: []` — เอกสารบันทึกคำขอ+อนุมัติอย่างเดียว ยังไม่มี feature ทะเบียนรถ/ตารางใช้รถให้ส่งต่อ
- G2 dynamic · ค่าเริ่ม 2 ขั้นตามช่องลงชื่อผู้อนุมัติบนกระดาษ: `role-line-manager` (ผู้บังคับบัญชา) → `role-mgr-hr` (ผู้จัดการฝ่ายทรัพยากรบุคคล) · ไม่มีวงเงิน
  - `role-line-manager` อยู่ในหมวด "ใช้งานจริงแต่ยังไม่อยู่ใน master" ของ doa-roles-contract.md (relative role จาก F-ORG-001) → แจ้งใน _BATCH_REPORT
  - คำตัดสินผูก role: ผู้บังคับบัญชา = อนุมัติ/ไม่อนุมัติ · ผู้จัดการฝ่ายทรัพยากรบุคคล = เห็นควร/ไม่เห็นควร (ตามคำบนกระดาษ)
- G3 ไม่มีค่าคงที่บนกระดาษ · คำนวณจำนวนวันอัตโนมัติ (ต้นฉบับให้กรอกเอง = สูตรที่ผิด → แก้) · เกินเกณฑ์ = เตือน · ขัดแย้งทางตรรกะ = บล็อก
- G4 รายชื่อผู้เดินทางไม่จำกัดแถว · PDF อย่างน้อย 5 แถวตามกระดาษ
- G5 1:1 ไม่เพิ่มช่อง
- G6 แถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ
- G7 ไม่อนุมัติ = กลับเป็นร่างเลขเดิม · ยกเลิกได้ เจ้าของ + admin role · สถานะ ร่าง/รออนุมัติ · เหตุผลบังคับ
- G8 เจ้าของ · ผู้อนุมัติหลังส่ง · admin role (HR) เห็นทั้งหมด
- G9 ออกเลขตอนบันทึกครั้งแรก (เอกสารภายใน ไม่ต้อง no-gap) · รหัส `VAN` (ย่อจาก "ขอใช้รถตู้" · ไม่ชนกับ registry ที่มีแค่ ACL)
- G10 แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗
- decisions_lock: 14 มติ · สถานะ "พร้อมเริ่มทำ" (exit 0) → ผ่านด่าน
- tag-ai-default: 11 มติเป็น AI-DEFAULT (G1–G10) · 3 มติ VALID จาก FORM_SPEC.anomalies
- 2026-10-07 12:19 · ขั้น 2 → done

## ขั้น 3 · ร่าง declaration (doa · ntf) — doccfg/mdoc รอ print_config จากขั้น 4
- `doa_tool.py init` → `VAN.doa.yaml`: dynamic · 1 set (ไม่มีวงเงิน) · 2 ขั้น sequential
  - ขั้น 1 `role-line-manager` (ผู้บังคับบัญชา) · ขั้น 2 `role-mgr-hr` (ผู้จัดการฝ่ายทรัพยากรบุคคล) คำตัดสิน เห็นควร/ไม่เห็นควร (ตามคำบนกระดาษ)
  - on_reject back_to_draft (DEC-08) · defaults_unconfirmed: true (AI-DEFAULT)
- `doa_tool.py brief` → VERDICT **PASS** (BLOCK 0) → `DOA_BRIEF_F-TMP-001.md`
- `ntf_tool.py suggest` เสนอ 2 event → ตัดสินแล้ว:
  - เก็บ `van_cancelled` (ยกเลิกระหว่างรออนุมัติ — DOA engine ไม่ยิง)
  - ตัด `van_over_limit_approved` — ฟอร์มไม่มีวงเงิน/เกณฑ์ตัวเลข (constants = 0) กฎใน DEC-04 เป็นกฎตรรกะที่บล็อกตั้งแต่กรอก
  - ไม่เพิ่ม event แจ้งผู้เดินทางตอนอนุมัติ — ขัด DEC-11 (G10 ประกาศ ✗) → เสนอให้ลูกค้าตัดสินรอบหน้า
  - ตัด doa_pending / doa_result / doa_escalate (DOA engine เจ้าของ)
- `ntf_tool.py brief` → VERDICT **PASS** (BLOCK 0) → `NTF_BRIEF_F-TMP-001.md`

## ขั้น 4 · แบบพิมพ์ Replica (print/)
- `form.tpl.html` แบบเส้นประ (R1–R7) + B6 `sign_rows` v2.1 + B7 · ถ้อยคำคัดตรงจาก `orig/content.html` ทุกบรรทัด
- `profile.json` ปรับ 5 token (title 13pt · logo 14mm · row_gap 7px · indent 10mm · fill_m 28mm)
- `print_config.json`: VAN · FM-HRM-22 · min_rows 5 · sign_boxes `requester` + `doa_step:*` · `decision_words.by_role.role-mgr-hr = เห็นควร/ไม่เห็นควร` · max_per_row 4
- `make_data.py` → data 5 สถานะ (ชื่อสมมติทั้งหมด · ไม่มีข้อมูลส่วนบุคคลจากไฟล์ลูกค้า)
  - draft · approved · rejected (เลือก "เฉพาะขาไป" → บล็อกขากลับว่าง) · long-12rows-3signs · approved-doa6steps (7 ช่อง 2 แถว 4+3)
- **parity_check: ✅ IDENTICAL 5/5** ไม่มีคำเตือน → ผ่านด่าน
- ตรวจ body ทุกสถานะ: ไม่มี `{{…}}` หลง · ไม่มี key หายจาก data → ผ่านด่าน
- `build_html.py` → `print/VAN_template.html` + `print/out/<state>.html` ครบ 5 สถานะ
- **[NO-BROWSER] ข้าม render_pdf.py** (ยืนยันแล้ว: pyshim หา Edge/Chrome/Chromium ไม่เจอ) → **ข้าม render_states.py** (PDF · `_states_sheet.png` · จำนวนหน้า) และ **ข้าม compare_original.py**
  - ด่าน "ทุกสถานะ 1 หน้า" และ "compare PASS/WARN" ยังไม่ได้ตรวจ → บันทึกใน `print/out/_states.json` + `VAN_print-spec.md` §7–§8 · ต้องรันรอบเต็มบนเครื่องที่มี browser
- declaration ที่เหลือ (ต้องใช้ print_config):
  - `doccfg_tool.py init + brief --registry doccfg_registry_codes.txt` → **PASS** (BLOCK 0) · รหัส VAN ไม่ชนกับ registry (มีแค่ ACL) → `DOCCFG_BRIEF_F-TMP-001.md`
  - `mdoc_tool.py validate/brief` → **WARN** (BLOCK 0): G04 ยังไม่มี taxonomy_def_id (เสนอ definition ใหม่) · G09 doa = pending
    - `function_code: F31` เป็น **[AI-DEFAULT รอยืนยัน]** — ไม่มี Taxonomy Master v1 ในชุดความรู้ของ workspace → แจ้งใน _BATCH_REPORT
    - `source: declaration` (ไม่ใช่ request) เพราะ REQ-TMP-001 ไม่ตรงรูปแบบ REQ-YYYY-NNNN ที่ G10 ต้องการ
  - `doa_tool.py validate --print-config` → **PASS** · INFO G1 `role-line-manager` เป็น relative role ต้องยืนยันกับ DOA กลาง
- 2026-10-07 12:28 · ขั้น 3 → done
- 2026-10-07 12:28 · ขั้น 4 → done

## ขั้น 5 · HTML Q-form (feature.html)
- สร้างจาก archetype canonical `references/form-archetype/_SOURCE_form-request-reference.html` (Pattern Q2 · v9.2)
  - ส่วน generic (BASE-KIT CSS · shell · search-select · formatters · render preservation) ลอกตรง
  - ส่วน domain เขียนใหม่ทั้งก้อนตาม FORM_SPEC + DECISIONS.lock → `_build/van_domain.js` + `_build/assemble_van.py` (ประกอบซ้ำได้)
- ช่องตาม FORM_SPEC 1:1 (DEC-06) · wizard 3 ขั้น (ข้อมูลหลัก · เอกสารแนบ · ตรวจสอบและยืนยัน — DEC-11 แนบไฟล์ ✓)
  - การ์ด ① ใช้รถตู้เมื่อไหร่ เพื่ออะไร (ช่วงวันที่ + จำนวนวันคำนวณสด) ② ใช้รถเที่ยวไหน (3 ตัวเลือก + บล็อกขาไป/ขากลับ enable ตามตัวเลือก) ③ ใครเดินทางบ้าง (แถวซ้ำไม่จำกัด)
- DOA dynamic (DEC-03): `MOCK_DOA_RESOLVED` 2 ขั้น + `resolveDoa()` + marker `DOA-ENGINE-HOOK` · modal ส่ง = 1 slot ต่อขั้น · ไม่ fix จำนวนขั้น/ชื่อคน
- คำตัดสินผูก role (DEC-07): `DECISION_WORDS.by_role['role-mgr-hr'] = เห็นควร/ไม่เห็นควร` ใช้ทั้งปุ่ม · timeline · แบบพิมพ์
- ไม่อนุมัติ = กลับเป็นร่างเลขเดิม (DEC-08) · การมองเห็นตาม DEC-09 · ส่งออก CSV ✓ ทำซ้ำ ✗ ประกาศ ✗ (DEC-11)
- PDF Preview ฝัง `print/form.tpl.html` เป็น `VAN_TPL` (ตรวจแล้วตรงกับไฟล์ต้นฉบับทุกไบต์) + `tplRender` + `tplSignRows`
- **Rule #114**: เปลี่ยนช่องวันที่จาก `type="date"` เป็น `bedateHTML()` (ตัวเลือกวัน พ.ศ. กลาง) + CSS ของ block
  - หมายเหตุ: archetype canonical ของสกิลยังใช้ `type="date"` อยู่ (audit baseline ของมันคือ FAIL=1) — ไฟล์นี้แก้แล้ว
- **ด่าน**: `audit.sh` → **FAIL=0** · WARN=3 (ทั้งหมดมาจาก BASE-KIT เท่ากับ baseline) · `prune_css.py` ตัด 41 rule (ลด 3.7 KB) แล้วรัน audit ซ้ำ FAIL=0
- **[NO-BROWSER] ข้าม `e2e_standard.py`** และ **ข้าม `render-check.py`** → บันทึกใน `reports/e2e_report.json` (status SKIPPED)
  - ทดแทนด้วย `reports/nodom_smoke.js` (node + stub DOM): docPrintData + tplRender ทุก record 12 ใบ → ไม่มี `{{}}` หลง ไม่มี `undefined`
  - DOA 6 ขั้น → ช่องลงชื่อ 7 ช่อง 2 แถว (4+3) · dense = true · คำตัดสิน "เห็นควร" ขึ้นเฉพาะ role-mgr-hr
  - กฎการมองเห็น: owner เห็น 4 · ผู้อนุมัติเห็น 3 · admin (ผจก.HR) เห็น 12 · ร่างของคนอื่นรั่วถึงผู้อนุมัติ = 0
- ข้อมูลตัวอย่างทั้งหมดเป็นชื่อสมมติ + โลโก้ placeholder (ไม่ใช้โลโก้/ชื่อจริงจากไฟล์ลูกค้า — DEC-12)
- 2026-10-07 12:45 · ขั้น 5 → done
- 2026-10-07 12:45 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 6 · ดู HTML + PDF (ข้ามตามโหมดไม่เฝ้า)
- `mark 6 skip --note "unattended — ให้คนดูจาก _BATCH_REPORT"`
- ภาพที่ควรมีให้คนเปิดดูภายหลัง: `print/out/_states_sheet.png` **ยังไม่มี** ([NO-BROWSER]) → ต้องรัน render_states บนเครั้องที่มี browser · แทนด้วย `print/out/*.html` ทั้ง 5 สถานะ + `feature.html` ที่เปิดดูได้ตรง ๆ

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- `BRD_F-TMP-001.md` (brd-generator-full · Prebrief Mode · New Feature)
  - §3.4 Scope Lock = DECISIONS.lock (LOCK-01…LOCK-14) · §12.1 Downstream Impact Map · §15 Open Questions 7 ข้อ · §16 Security preset P2 · §17 SLA/KPI/Threshold/Throughput
  - **AI Review: ✅ APPROVED 28/28** (C01–C23 + PE01–PE05) → ผ่านด่าน
- `FRD_F-TMP-001_Pack/` 8 ไฟล์ (00_OVERVIEW · 01_UI · 02_API · 03_LOGIC FN-01…FN-12 · 04_DB · 05_RULES · 06_TESTS 53 เคส · 07_LOCKED_DECISIONS)
- **`frd_lint.py` Section N: BLOCK 0 · WARN 0 · PASS 11** → ผ่านด่าน (`reports/_SECTION_N.md`)
  - N1 DEC ครบ 14 ข้อใน 07 · N2 ทุกช่องมีคีย์ใน 04/01 · N4 เคสปฏิเสธสิทธิ์ 9 จุด + เคส "ผู้อนุมัติไม่เห็นร่างของคนอื่น"
  - N5 header_snapshot + จุดออกเลข FN-04 · N6 approval_chain + doa_ref · N7 event van_cancelled ถูกอ้าง · N8 ไม่อ้างสกิลเวอร์ชันที่ไม่ได้ติดตั้ง
- ใส่ `frd_ref` ตามที่ lint พิมพ์ แล้วออก declaration ฉบับจริง:
  - `doccfg_tool.py brief --final --registry doccfg_registry_codes.txt` → **PASS** (BLOCK 0)
  - `ntf_tool.py brief --final` → **PASS** (BLOCK 0)
- หมายเหตุ: ไม่มีแบบ "ฉบับจริง (--final)" สำหรับ doa/mdoc ในสกิลเวอร์ชันนี้ — ใช้ผล validate/brief ของขั้น 3–4 (doa PASS · mdoc WARN ไม่มี BLOCK)
- 2026-10-07 13:02 · ขั้น 7 → done

## ขั้น 8 · UI Brief → test case AI → UAT
- `extract_anchors.py` → `reports/inventory.json` (route 5 · toast 12 · overlay 33 · z-index 12 · ปุ่ม 20 · microcopy 257 · function 197 · marker 7 · archetype Q-form · __QA__ มี)
- `UI_BRIEF_F-TMP-001.md` ครบ §0–§13 (AS-BUILT)
  - **`brief_check.py`: PASS · FAIL 0 · WARN 0** → ผ่านด่าน (`reports/brief_check.md`)
  - B1 route ครบ 5 · B2 toast คงที่ครบ 12 · B5 anchor ที่อ้างมีจริงทั้งหมด (fn 31 · class 24 · id 19) · B6 CSS vars 47/47 · B7 microcopy 58/60 · B8 §0–§13 ครบ
- `testcases-F-TMP-001.md` (ai-testcase-md-generator) 32 เคส · 167 step · กลุ่ม CRT 11 · DOA 10 · PERM 4 · PDF 4 · LIST 3
  - **`tc_lint.py`: ERROR 0** → ผ่านด่าน (`reports/tc_counts.json`)
- `cases.json` (qa-friendly · Lite) เก็บ 30 เคส · `QA_AUDIT_F-TMP-001.md` drop ledger 2 เคส (TC-DOA-02 ต้องใช้เครื่องมือนักพัฒนา · TC-PERM-02 ต้องรู้รหัสภายในเอกสาร)
  - **`lite_audit.py --stamp`: หายเงียบ 0** → ผ่านด่าน · ประทับ md5 ของ MD ต้นทางลง `cases.json` แล้ว
- **[NO-BROWSER] ข้าม `verify_anchors.py`** (ต้องใช้ browser เทียบ anchor กับหน้าจอจริง) → ทดแทนด้วย brief_check B5 ที่ตรวจ anchor กับไฟล์ HTML แบบ static
- **[NO-BROWSER] ข้าม `capture.py`** → ยังไม่มีภาพประกอบ และยังไม่ได้ build เอกสาร UAT เป็น HTML (`build.py`) — บันทึกไว้ใน QA_AUDIT
- 2026-10-07 13:17 · ขั้น 8 → done
