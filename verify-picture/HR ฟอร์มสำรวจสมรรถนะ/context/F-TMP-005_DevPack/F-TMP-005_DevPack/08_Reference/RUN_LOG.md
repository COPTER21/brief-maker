# RUN_LOG — F-TMP-005 ฟอร์มสำรวจสมรรถนะ (REQ-TMP-005)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)

## ขั้น 1 · อ่านฟอร์ม + PREBRIEF v2 (2026-10-07)
- โหมด **NO-BROWSER** (dm.sh check: ไม่มี Edge/Chrome/Chromium) → ข้ามคำสั่งที่ต้องใช้ browser ทุกขั้น
- ภาพฟอร์ม: ใช้ `_system/tools/to_image.py` (LibreOffice → PDF → pypdfium2) ได้ `page-1.png` `page-2.png` + `content.html` = **หน้ากระดาษจริง** (ผ่าน soffice ไม่ใช่ HTML→browser) → เทียบ layout ได้
- ภาพ render ด้วย fallback font (สระไทยเป็นกล่อง) → **ถ้อยคำยึด `orig/content.src.txt`** · ตำแหน่ง/เส้น/ตาราง/โลโก้/Doc No. ยึดภาพ
- ชื่อจริงจากหัวฟอร์ม = "แบบฟอร์มสำรวจสมรรถนะ" (ชื่อไฟล์เดิม "ฟอร์มสำรวจสมรรถนะ") → `dm.sh rename J005`
- control: Doc No. **FM-HRM-40** · REV.00 : 01/07/2569 · โลโก้ Credence (ใช้โลโก้ Organization แทน)
- FORM_SPEC: 14 ช่อง (ระบบ 3 · กรอก 11) · แถวซ้ำ 2 กลุ่ม (core 5 แถว · func 6 แถว) · ตัวเลือก 3 · ค่าคงที่ 4 (ตารางระดับ 1–4) · ลายเซ็น 2 · สูตร 0 · anomalies 0
- `form_spec_check.py` → **ERROR 0** (exit 0) · gate ที่ต้องถาม G1–G10
- [บั๊ก #1] `impact_summary.py` regex `REQ-[\d-]+` ไม่รับ `REQ-TMP-005` → รันบนสำเนาที่แทนเป็น `REQ-2569-0005` แล้ว sed กลับเป็น `REQ-TMP-005` ใน IMPACT_SUMMARY_*.{html,json}
- [บั๊ก #2 ป้องกันล่วงหน้า] `mv orig/content.html orig/content.src.txt` กัน `manifest_scan.py` นับเป็น prototype ซ้ำ (K2 BLOCK)
- ไม่มี PREBRIEF จาก CMS → สร้าง PREBRIEF v2 จาก FORM_SPEC ตรง ๆ (`--req REQ-TMP-005 --cls FRM --module HR`)
- PDPA: ฟอร์มเปล่า ไม่มีข้อมูลตัวอย่างจริง · ช่อง ชื่อ–สกุล ติด `pdpa: true` → ใช้ชื่อสมมติใน prototype/แบบพิมพ์
- 2026-10-07 14:26 · ขั้น 1 → done

## ขั้น 2 · gate 10 หมวด → DECISIONS.lock (โหมดไม่เฝ้า · AI ตอบเอง)
- G1 — ฟอร์มสำรวจสมรรถนะเป็น "บันทึกผลประเมิน" ไม่มีถ้อยคำบนกระดาษที่สั่งเปลี่ยนค่าใด → `config_changes: []` · `post_to: []`
- G2 — ช่องลงชื่อผู้อนุมัติบนกระดาษ 1 จุด (ผู้ประเมิน) → dynamic · ค่าเริ่ม 1 ขั้น `role-line-manager` · ไม่มีวงเงิน
- G3 — ตารางระดับ 1–4 เป็นค่าคงที่บนกระดาษ → อ่านจาก `CompetencyLevelConfig` ห้าม hardcode · ไม่มีสูตรบนกระดาษ
- G4 — core 5 แถว / func 6 แถว = ขั้นต่ำบนกระดาษ · ไม่จำกัดจำนวนแถวในระบบ
- G5 — 1:1 ไม่เพิ่มช่อง · G6 — แถวล่าง 1 ช่องต่อขั้น DOA + ช่องผู้รับประเมิน ไม่ใช้ภาพลายเซ็น
- G7 — ไม่อนุมัติ = กลับร่างเลขเดิม (`on_reject: back_to_draft` ตามบั๊ก #5 — เขียน `draft` จะ BLOCK G5 ขั้น 3) · ยกเลิกที่ draft/pending ต้องมีเหตุผล
- G8 — เจ้าของ · ผู้อนุมัติหลังส่ง · admin role (HR) เห็นทั้งหมด
- G9 — ไม่ใช่เอกสารการเงิน no-gap → ออกเลขตอนบันทึกครั้งแรก · รหัส **CMP** (ไม่ชน ACL/MEM/VAN/TRV/DSR ในทะเบียน)
- G10 — แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗
- `decisions_lock.py` → 12 มติ · **พร้อมเริ่มทำ (exit 0)** → `dm.sh tag J005` ติด **AI-DEFAULT 12/12**
- [บั๊ก #7 ยืนยัน] DEC-05/DEC-06 ออกมาเป็น G4 ตามจำนวน repeat group (ที่นี่มีจริง 2 กลุ่ม — ไม่ใช่ false positive)
- 2026-10-07 14:27 · ขั้น 2 → done

## ขั้น 3 · ร่าง declaration (doa · ntf)
- `doa_tool.py init` → `CMP.doa.yaml` · 1 set · 1 ขั้น (`role-line-manager` ป้าย "ผู้ประเมิน") · mode dynamic · `on_reject: back_to_draft` (บั๊ก #5) · amount none
- แก้ `platform: core → hr_platform` ตาม doa-roles-contract §3 (hr → hr_platform)
- `doa_tool.py validate` → **VERDICT PASS · BLOCK 0** · INFO 2: `role-line-manager` เป็น relative role (ยืนยันกับ DOA กลางก่อน wire) · ยังไม่ให้ --print-config (ตรวจ sign_boxes ขั้น 4)
- `ntf_tool.py suggest` → 2 event · ตัด DOA events 3 ตัว · **ตัดสิน review แล้ว**: ลบ `cmp_over_limit_approved` (ฟอร์มไม่มีสูตร/เกณฑ์ตัวเลข — FORM_SPEC.formulas = 0) เหลือ `cmp_cancelled`
- `ntf_tool.py validate/brief` → **VERDICT PASS · BLOCK 0**
- doccfg + mdoc ยังไม่ทำ (ต้องใช้ print_config จากขั้น 4)
- 2026-10-07 14:28 · ขั้น 3 → done

## ขั้น 4 · แบบพิมพ์ Replica (FM-HRM-40)
- โหมด **Replica** · block map: R1 โลโก้ · R2 ชื่อเอกสาร · form-section ×4 · R4 บรรทัดเส้นประ (ข้อมูลทั่วไป) · **R9 ตารางกรอบ ×3** (ระดับ 1–4 · Core · Functional) · R8 form-box ×3 · R6 form-check (แนวทางการพัฒนา) · B6 sign_rows · B7 footer
- profile `credence-fm-hrm-40`: form_fs 9pt · form_title_fs 15pt · form_logo_h 13mm · form_title_gap 10px · form_grid_gap 4px · form_row_gap 6px
- data 5 สถานะ (`make_data.py` · ชื่อสมมติ + โลโก้ placeholder ตาม PDPA): draft · approved · rejected · long-12rows · approved-doa6steps (7 ช่อง → 4+3)
- **ด่าน: `parity_check.py` → IDENTICAL 5/5** · `render_doc.py` ทุกสถานะ → **ไม่มี `{{}}` หลง**
- `build_html.py --mode replica --profile` → `CMP_template.html` + `out/<state>.html` ครบ 5 สถานะ (เปิดดูได้ด้วยมือ)
- [NO-BROWSER] ข้าม `render_states.py` · `render_pdf.py` · `compare_original.py` → **ยังไม่มี PDF · `_states_sheet.png` · `compare_side.png` · ยังไม่ได้ยืนยันจำนวนหน้า/การตัดหน้า** (บันทึกไว้ใน print-spec §6/§7/§8)
- `doa_tool.py validate --print-config` → **PASS** (G8/G9 ช่องลงชื่อ dynamic ตรงกับ `sign_boxes: doa_step:*` + `decision_words.by_role`)
- `doccfg_tool.py init/brief --registry doccfg_registry_codes.txt` → **VERDICT PASS** · code `CMP` ไม่ชน ACL/MEM/VAN/TRV/DSR
- `mdoc_tool.py validate/brief --doccfg` → **VERDICT WARN · BLOCK 0** (G04 ยังไม่มี taxonomy_def_id · G09 doa = pending — ปกติของแบบใหม่)
- print-spec + data-contract เขียนครบ (`print/CMP_print-spec.md` · `print/CMP_data-contract.md`)
- 2026-10-07 14:34 · ขั้น 4 → done

## ขั้น 5 · HTML Q-form (feature.html)
- ประกอบจาก archetype Pattern Q2 (v9.2) ผ่าน `feature.html` ของ J001 ที่ผ่าน audit แล้ว — `_build/assemble.py` + `_build/domain.js` (ประกอบซ้ำได้)
  - generic (BASE-KIT CSS · shell · search-select · formatters · render preservation · bedateHTML) ลอกตรง · domain เขียนใหม่ทั้งก้อนตาม FORM_SPEC + DECISIONS.lock
  - `<meta name="cube-archetype" content="Q-form">` ติดมากับ archetype (Rule #112)
- ช่องตาม FORM_SPEC 1:1 (DEC-07) · wizard 3 ขั้น (ข้อมูลและผลประเมิน · เอกสารแนบ · ตรวจสอบและยืนยัน)
  - การ์ด ① วันที่ประเมิน (bedateHTML · ชื่อ–สกุล/ตำแหน่ง/แผนก ดึงจากระบบ ไม่ใช่ช่องกรอก) + legend ระดับ 1–4
  - การ์ด ② สมรรถนะหลัก · การ์ด ③ สมรรถนะเฉพาะสายงาน = **การ์ดต่อแถว** (Rule #107: แถวซ้ำ ≤4 ช่อง → การ์ด) + ปุ่มระดับ 1–4 (เลือกได้ค่าเดียว กดซ้ำเพื่อยกเลิก)
  - การ์ด ④ สรุปผลและแผนพัฒนา — จุดแข็ง / ควรพัฒนา / แนวทางการพัฒนา (chip เลือกหลายข้อ) / รายละเอียดเพิ่มเติม
- ตารางระดับ 1–4 อ่านจาก `LEVEL_CONFIG` (mock ของ `CompetencyLevelConfig.levels[]`) — ไม่ hardcode ในแบบพิมพ์ (DEC-04)
- DOA dynamic (DEC-03): `MOCK_DOA_RESOLVED` 1 ขั้น (`role-line-manager` ป้าย "ผู้ประเมิน") + `resolveDoa()` + DOA-ENGINE-HOOK · modal ส่ง = 1 slot ต่อขั้น · ไม่ fix จำนวนขั้น
- ส่งกลับแก้ไข = **กลับเป็นร่างเลขเดิม** (DEC-09) · ยกเลิกเฉพาะ ร่าง/รออนุมัติ โดยเจ้าของ + admin role · การมองเห็นตาม DEC-10
- DEC-12: **ไม่มีคำสั่ง "ทำซ้ำ"** ทั้งใน ⋮ และหัวลิ้นชัก · ส่งออก CSV ✓ · แนบไฟล์ ✓ · ประกาศ ✗
- PDF Preview ฝัง `print/form.tpl.html` เป็น `CMP_TPL` (ไฟล์เดียวกับฝั่ง server) + `tplRender` + `tplSignRows` (ผลการแบ่งแถวเท่ากับ `sign_rows.py`)
- **Rule #114**: ช่องวันที่ใช้ `bedateHTML()` — ไม่มี `input type="date"` ในไฟล์
- **ด่าน**: `audit.sh` → **FAIL=0** · WARN=3 (BASE-KIT baseline เดียวกับ archetype) · `prune_css.py` ตัด 37 rule (ลด 3.2 KB) แล้ว audit ซ้ำ **FAIL=0**
- **[NO-BROWSER] ข้าม `e2e_standard.py`** · **[NO-BROWSER] ข้าม `render-check.py`** → `reports/e2e_report.json` status = SKIPPED
  - ทดแทนด้วย `reports/nodom_smoke.js` (node + stub DOM) → **ALL CHECKS OK** (log: `reports/nodom_smoke.log`)
    - docPrintData + tplRender ทุก record 12 ใบ → ไม่มี `{{}}` หลง ไม่มี `undefined` · เติมแถวว่างครบ core 5 / func 6 ทุกใบ
    - ระดับ 1–4 ติ๊กช่องเดียวต่อแถวที่มีชื่อ · แถวว่างไม่ติ๊ก · ตารางระดับมาจาก config · ถ้อยคำบนกระดาษครบ
    - DOA 6 ขั้น → ช่องลงชื่อ 7 ช่อง 2 แถว (4+3) · dense = true
    - การมองเห็น: owner เห็น 4 · ผู้พิจารณาเห็น 3 · admin (ผจก.ฝ่ายบุคคล) เห็น 12 · ร่างของคนอื่นรั่วถึงผู้พิจารณา = 0
- ข้อมูลตัวอย่างทั้งหมดเป็นชื่อ/บริษัท/สมรรถนะสมมติ + โลโก้ placeholder (ไม่ใช้ข้อมูลจากไฟล์ลูกค้า)
- 2026-10-07 14:56 · ขั้น 5 → done
- 2026-10-07 14:56 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 6 · ดู HTML + PDF (ข้ามตามโหมดไม่เฝ้า)
- `mark J005 6 skip --note "unattended — ให้คนดูจาก _BATCH_REPORT"`
- ภาพที่ควรมีให้คนเปิดดูภายหลัง: `print/out/_states_sheet.png` **ยังไม่มี** ([NO-BROWSER]) → ต้องรัน `render_states.py` บนเครื่องที่มี browser
  - แทนด้วย `print/out/*.html` ครบ 5 สถานะ (เปิดดูในเบราว์เซอร์ได้ตรง ๆ) + `feature.html`

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- `BRD_F-TMP-005.md` — Lane Mode (PREBRIEF v2 + DECISIONS.lock แทน RIF · DEC = Scope Lock ชั่วคราวใน §3.4) · มี Dev Requirements Summary + Quality gate + ประเด็นที่ต้องให้ลูกค้าเคาะ
- `FRD_F-TMP-005_Pack/` ครบ 8 ไฟล์ (00–07) · 07 §7.0 = DECISIONS.lock ครบ 12 DEC ติดป้าย `[AI-DEFAULT]`
- **ด่าน `frd_lint.py` Section N → BLOCK 0 · WARN 4 · PASS 11**
  - N1 DEC ครบ 12 · N2 ทุกช่องมีคีย์ใน 04/01 · N4 เคสปฏิเสธสิทธิ์ 8 จุด + เคส "ผู้อนุมัติไม่เห็นร่างของคนอื่น"
  - N5 ไม่อ้าง F185 API-23 · มี header_snapshot · จุดออกเลข FN-01 · N6 approval_chain + doa_ref · N7 event cmp_cancelled ถูกอ้าง · N8 ผ่าน
  - **WARN N3 ×4 = false positive** — regex ตัดเหลือเลข 1/2/3/4 แล้วไปชนตัวเลขธรรมดาในประโยค ("3.0 State machine" · "ระดับ 1–4" · "2 รายการ") ไม่ใช่การ hardcode คำอธิบายระดับจริง (คำอธิบายอ่านจาก `CompetencyLevelConfig` ทุกจุด)
- declaration ฉบับจริง (ใส่ frd_ref แล้ว): doccfg `numbering.frd_ref = 03_LOGIC FN-01` · `snapshot_points[].frd_ref = 03_LOGIC FN-07` · ntf `cmp_cancelled.frd_ref = 03_LOGIC FN-06`
  - `doccfg_tool brief --final --registry` → **PASS** · `ntf_tool brief --final` → **PASS** · `doa_tool brief --print-config` → **PASS** · `mdoc_tool brief` → WARN (BLOCK 0 · taxonomy_def_id + doa pending ตามปกติของแบบใหม่)
- 2026-10-07 15:05 · ขั้น 7 → done

## ขั้น 8 · UI Brief → test case AI → UAT
- `extract_anchors.py` → `reports/inventory.json` (vars 47 · z-index 22 · routes 5 · overlay 33 · toast 12 · ปุ่ม 20 · microcopy 267 · function 191 · marker 7 · archetype Q-form · `__QA__` true)
- `UI_BRIEF_F-TMP-005.md` (AS-BUILT) ประกอบจาก `_build/ui_brief_head.md` + inventory (`_build/make_ui_brief.py`)
  - **ด่าน `brief_check.py` → PASS · FAIL 0 · WARN 0** (B1 route 5/5 · B2 toast คงที่ 12/12 · B3 overlay ครบ · B4 z-index 12 ค่า · B5 anchor มีจริงทั้งหมด · B6 CSS vars 47/47 · B7 microcopy 60/60 · B8 ครบ §0–§13)
- `testcases-F-TMP-005.md` **30 เคส · 128 step** (CRT 10 · DOA 8 · PERM 4 · PDF 4 · LIST 4) + Coverage Ledger + Coverage Audit + Result schema
  - **ด่าน `tc_lint.py` → ERROR 0**
  - **ด่าน `verify_anchors.py` → MISSING 0** (DOM 0 · SOURCE 46 · DATA 46) — สคริปต์ตรวจพบว่าไม่มี browser แล้ว fallback เป็นโหมด source เอง · [NO-BROWSER] ส่วน DOM ยังไม่ได้ไล่
- `cases.json` (เอกสารแบบทดสอบสำหรับคน) **27 เคส** จาก `_build/make_cases.py` · ตัด 3 เคสลง drop ledger ของ `QA_AUDIT_F-TMP-005.md`
  - **ด่าน `lite_audit.py` → หายเงียบ 0 · ERROR 0** (ประทับ `meta.source` แล้ว)
- ยังไม่ได้ gen ไฟล์ UAT HTML จาก cases.json ([NO-BROWSER]) — ทำต่อได้ด้วย qa-friendly-html-generator บนเครื่องที่มี browser
- 2026-10-07 15:14 · ขั้น 8 → done
