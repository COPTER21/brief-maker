# RUN_LOG — J006 · หนังสือสัญญายืม (กล่องบรรจุกระดาษ) · F-TMP-006 · REQ-TMP-006

โหมด: unattended · NO-BROWSER

## ขั้น 1 · อ่านฟอร์ม + PREBRIEF v2
- ต้นฉบับ `.doc` (Word 97) → `_system/tools/to_image.py` ใช้เส้นทาง **LibreOffice → PDF → pypdfium2** ได้ `orig/SAMPLE.pdf` + `page-1.png` `page-2.png` (2 หน้า)
  - เป็นหน้ากระดาษจริงจาก LibreOffice (ไม่ใช่เส้นทาง HTML+browser) → ใช้เทียบ layout ได้
  - ภาพ PNG แสดงอักษรไทยเป็นกล่องว่าง (ฟอนต์ไทยไม่ครบใน renderer) → **ถ้อยคำยึดจาก text layer ของ SAMPLE.pdf** (pypdfium2 get_text_range) · ตำแหน่ง/เส้น/กรอบยึดจาก PNG
- ไม่มี `orig/content.html` (ไม่ได้ใช้เส้นทาง HTML) → ไม่ต้องย้ายเป็น content.src.txt (เลี่ยงบั๊ก manifest_scan นับ prototype ซ้ำได้เอง)
- โครงเอกสาร: 2 หน้า = ชุด **ต้นฉบับ** (หน้า 1) + **สำเนา** (หน้า 2) เนื้อความเดียวกัน · หัวกระดาษ Doc. No. : FM-SAL-14 · Rev.00 : 01/07/2569
- ชื่อจริงจากหัวฟอร์ม = "หนังสือสัญญายืม" (ชื่อไฟล์เดิมเป็น "ฟอร์มหนังสือสัญญายืมกล่องบรรจุกระดาษ") → `dm.sh rename J006 "หนังสือสัญญายืม (กล่องบรรจุกระดาษ)"` ก่อนขั้น 2
- เอกสารเป็น **หนังสือสัญญา** — เนื้อสัญญาเป็นข้อความคงที่ (blocks kind=para) 5 ย่อหน้า · ช่องเติมมีเพียง 10 ช่อง
- FORM_SPEC: 10 ช่อง (ระบบ 4 · กรอก 3 · ระบบใส่ 3) · แถวซ้ำ 1 · ตัวเลือก 1 (ต้นฉบับ/สำเนา) · ค่าคงที่ 2 · ลายเซ็น 2 (ผู้รับมอบ · ผู้ส่งมอบ) · anomalies 5
- `form_spec_check.py` → **ERROR 0** (รอบแรก ERROR 2: F08/F09 ไม่อยู่ใน block → ใส่ `fields` ให้ block kind=sign แล้วผ่าน)
- gate ที่ต้องถาม: G1–G10 ครบ
- PDPA: ชื่อ/ที่อยู่ลูกค้า + ชื่อผู้ลงนาม ติด `pdpa: true` · ต้นฉบับไม่มีข้อมูลตัวอย่างจริงกรอกไว้ (เป็นฟอร์มเปล่า) → ไม่มีข้อมูลส่วนบุคคลไหลลง prototype
- **บั๊กที่เจอซ้ำ (#1)**: `impact_summary.py` regex `REQ-[\d-]+` ไม่รับ `REQ-TMP-006` → ทำสำเนาแทนเป็น `REQ-2569-0006` รัน แล้ว sed แทนกลับในไฟล์ผลลัพธ์ทั้ง .html/.json
- 2026-10-07 14:28 · ขั้น 1 → done

## ขั้น 2 · gate 10 หมวด → DECISIONS.lock (โหมดไม่เฝ้า — AI ตอบเอง)
เหตุผลรายหมวด (ตาม `unattended-policy.md` + signals ใน FORM_SPEC.check.json):
- **G1** หนังสือสัญญายืมกล่องให้ลูกค้าใช้ฟรี กล่องยังเป็นทรัพย์สินบริษัท → ไม่แก้ค่าตั้งต้น ไม่ตัดสต๊อก ไม่ลงบัญชี · `config_changes: []` `post_to: []`
- **G2** ช่องลงชื่อฝั่งบริษัทบนกระดาษมี 1 ช่อง ("ผู้ส่งมอบ") → ค่าเริ่ม 1 ขั้น · module = sales → `role-mgr-sales` (ตาม Module Registry ใน doa-roles-contract §3) · ฝั่ง "ผู้รับมอบ" เป็นคู่สัญญาภายนอก ไม่นับเป็นขั้น DOA · dynamic · ไม่มีวงเงิน
- **G3** ไม่มีสูตร · ค่าคงที่ 2 ตัวในเนื้อสัญญา (ร้อยละ 10 ต่อปี · ชื่อบริษัท) ต้องอ่านจาก config ห้าม hardcode
- **G4** กระดาษมีบรรทัดรายละเอียดกล่อง 1 บรรทัด → ไม่จำกัดแถว · PDF ขั้นต่ำ 1 แถว
- **G5** 1:1 — เนื้อสัญญาเป็นถ้อยคำผูกพันทางกฎหมาย ห้ามเพิ่ม/แก้ช่องหรือถ้อยคำ
- **G6** แถวล่าง 1 ช่องต่อขั้น DOA + ช่องคู่สัญญาฝั่งลูกค้าเป็นช่องเซ็นบนกระดาษ (ไม่ใช่ขั้นในระบบ) · ไม่ใช้ภาพลายมือชื่อ
- **G7** กลับเป็นร่างเลขเดิม (`on_reject: back_to_draft` — ค่าที่ doa_tool รับ, บั๊ก #5) · ยกเลิกโดย owner + admin_role สถานะ draft/pending · ต้องมีเหตุผล
- **G8** เจ้าของ · ผู้อนุมัติหลังส่ง · admin role ของฝ่ายขายเห็นทั้งหมด
- **G9** ไม่ใช่เอกสารการเงิน no-gap → ออกเลขตอนบันทึกครั้งแรก · รหัส **LOA** (Loan Agreement — ไม่ชนกับ ACL/MEM/VAN/TRV/DSR ใน registry)
- **G10** แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗
- DEC-12..16 = VALID จาก anomalies 5 ข้อของต้นฉบับ (เลขข้อสำเนาไหลต่อ · หัวเรื่องสำเนาตกหน้า 1 · เส้นประแทรกกลางประโยค · กรอบว่างหัวกระดาษ · ไม่มีช่องวันครบกำหนดคืน)
- DEC-05 (G4) ออกแม้บนกระดาษมีแถวเดียว — ตามบั๊ก #7 ปล่อยได้
- `decisions_lock.py` → **พร้อมเริ่มทำ (exit 0)** · `dm.sh tag J006` → 11 มติเปลี่ยนเป็น AI-DEFAULT
- 2026-10-07 14:29 · ขั้น 2 → done

## ขั้น 3 · ร่าง declaration (doa · ntf) — doccfg/mdoc ทำหลังขั้น 4
- `doa_tool.py init` → `LOA.doa.yaml` · doa_type `loa` · scope `document_sign` · mode dynamic · 1 set 1 ขั้น (`role-mgr-sales`) · `on_reject: back_to_draft` (บั๊ก #5 — ค่าที่ tool รับ) · `wire_status: pending`
  - `validate` **PASS** (INFO G8: ยังไม่ให้ --print-config → ตรวจ sign_boxes ตอนขั้น 4)
  - `brief` → `DOA_BRIEF_F-TMP-006.md` **PASS** · `mock` → `_doa_mock.js` (MOCK_DOA_RESOLVED + DECISION_WORDS + marker DOA-ENGINE-HOOK) ใช้ฝัง HTML ขั้น 5
  - role `role-mgr-sales` อยู่ใน Roles Master (DOA v23) → ไม่มี WARN · ไม่ต้อง map role ใหม่
- `ntf_tool.py suggest` ได้ 2 event (ตัด doa_pending/doa_result/doa_escalate อัตโนมัติ ตาม N2)
  - ตัดสิน event ที่ `review: true`: **ตัด `loa_over_limit_approved` ออก** — เอกสารไม่มีช่องคำนวณและไม่มีเกณฑ์วงเงินที่ระบบตรวจรายใบ (เพดานร้อยละ 10 ต่อปีเป็นถ้อยคำในสัญญา ไม่ใช่ค่าตรวจ · DEC-04)
  - เติม event ธุรกิจของเอกสาร: **`loa_signed_copy_attached`** — แนบไฟล์หนังสือที่ลงนามครบสองฝ่ายกลับเข้าเอกสาร (หลักฐานผูกพันจริงของสัญญา · ใช้ G10 แนบไฟล์)
  - `validate` **PASS** · `brief` → `NTF_BRIEF_F-TMP-006.md` **PASS**
- 2026-10-07 14:30 · ขั้น 3 → done

## ขั้น 4 · แบบพิมพ์ Replica (thai-doc-pdf-generator v2.1)
- โหมด **Replica** · บล็อก R1 (logo) · R3 (วันที่/ชุด/เลขที่) · R2 (ชื่อเรื่อง) · R4 (บรรทัดกรอก) · R5 (รายละเอียดกล่อง) · R7/`form-section` (เนื้อสัญญา) · **B6 sign_rows** · B7 footer
- `form.tpl.html` + `profile.json` (11 token) + `print_config.json` (`doc_type LOA` · `sign_boxes: requester + doa_step:*` · `decision_words.by_role[role-mgr-sales] = ลงนาม/ไม่ลงนาม` · `copies: ต้นฉบับ+สำเนา`)
- data 5 สถานะ สร้างด้วย `sign_rows.py` (`build_signs` + `chunk_signs`) ผ่าน `print/_make_data.py` — **ห้าม fix จำนวนช่อง**
  - draft (2 ช่อง) · approved (2) · rejected (2 · ชุดสำเนา · ช่องเติมในเนื้อสัญญาเว้นว่าง) · long 13 แถว + 3 ขั้น (4 ช่อง · dense) · **DOA 6 ขั้น → 7 ช่อง 2 แถว (4+3) · dense**
- ด่าน: `parity_check.py` → **IDENTICAL 5/5 ไม่มีคำเตือน** · `render_doc.py` ทุกสถานะ → **ไม่มี `{{}}` หลง** · `build_html.py` → `LOA_template.html` + `out/<state>.html` 5 ไฟล์
- `[NO-BROWSER] ข้าม render_states.py` (ไม่ได้ `_states_sheet.png` และ PDF) · `[NO-BROWSER] ข้าม compare_original.py` (ไม่ได้ compare score / compare_side.png)
  - **แทนด้วย node smoke test** `print/out/_smoke.js` (ใช้ `tpl_render.js` ตัวเดียวกับ prototype): ไม่มี `{{}}` ค้าง · เลขข้อ 1./2. ทุกชุด ไม่มี 3./4. (DEC-12) · ช่องลงชื่อ = 1 + ขั้น DOA · ทุกแถว ≤4 ช่อง · ร้อยละ+ชื่อบริษัทมาจาก data ไม่ hardcode → **SMOKE PASS**
  - ค้างให้คนดู: จำนวนหน้าจริง · ภาพวางคู่กับต้นฉบับ → ต้องรันรอบเต็มบนเครื่องที่มี browser ก่อน UAT
- ต้นฉบับแนวตั้งอยู่แล้ว → ไม่ติดข้อจำกัด `@page A4 portrait` ของ base.css
- ความต่างจากกระดาษ 10 ข้อ (D1–D10) บันทึกใน `print/LOA_print-spec.md` §7 · ที่ต้องให้ลูกค้าเคาะ: D4 (ตำแหน่งวันที่) · D6 (เพิ่มช่อง ☐ ลงนาม / ☐ ไม่ลงนาม) · D9 (กรอบว่างหัวกระดาษ)
- `LOA_data-contract.md` ครบทุก key
- **doccfg**: `doccfg_tool.py init` (ใส่ `--print-config`) → `LOA.doccfg.yaml` · ปรับ `snapshot.sent_external = true` (หนังสือสัญญาส่งให้คู่สัญญาภายนอกลงนาม) → `validate --registry` **PASS** · `brief --registry` **PASS** → รหัส **LOA** ไม่ชนกับ ACL/MEM/VAN/TRV/DSR
- **mdoc**: `LOA.mdoc.yaml` · class `AGR` (หนังสือสัญญา) · `prints` 2 รายการ (ต้นฉบับ · สำเนา) = เอกสารชุดใช้เลขที่เดียว · `validate` **WARN** (G01 ไม่ได้ให้รายการ F-DOCCFG · G04 ยังไม่มี taxonomy_def_id · G09 doa = pending — ทั้งสามเป็น WARN ที่ตามปิดทีหลัง ไม่ใช่ BLOCK) → `brief --doccfg` ออก `MDOC_BRIEF_LOA.md`
  - **ต้องให้คนเคาะ**: `function_code` ใช้ F31 ตามใบก่อนหน้าในกองนี้ แต่ workspace ไม่มีตาราง F01–F48 ให้ตรวจว่า AGR ควรเป็นรหัสไหน
- `doa_tool.py validate --print-config` → **PASS** (G8/G9 ช่องลงชื่อ dynamic ผ่าน)
- 2026-10-07 14:40 · ขั้น 4 → done

## ขั้น 5 · HTML Q-form + gate
- ประกอบจาก archetype canonical `html-generator-v9/references/form-archetype/_SOURCE_form-request-reference.html` ด้วย `_build/assemble_loa.py` (วิธีเดียวกับ J001–J004)
  - prefix = base-kit + CSS + body + generic utils ของ archetype · domain = `_build/loa_domain.js` (745 บรรทัด เขียนใหม่ทั้งก้อน)
  - `LOA_TPL` = `print/form.tpl.html` ไฟล์เดียวกับฝั่ง server (parity IDENTICAL) · `CO_LOGO` = โลโก้ placeholder (ห้ามใช้โลโก้ลูกค้า)
  - **บั๊ก #4 (PDF_CSS ซ้ำ)**: ไม่เจอ เพราะคัด `const PDF_CSS` บรรทัดเดียวจาก archetype แล้วตัด domain เดิมทั้งก้อนก่อนต่อ domain ใหม่ → `grep -c 'const PDF_CSS'` = 1
  - **บั๊ก #3 (Rule #114 input ชนิด date)**: ใช้ `bedateHTML()` จาก `templates/blocks/be-datepicker` สำหรับช่อง "วันที่ของหนังสือ" → `grep -c 'type="date"'` = 0
  - ล้างคอมเมนต์หัว domain เดิมของ archetype ที่ค้างอยู่ → ไม่มีร่องรอยเอกสารเดิมในไฟล์ (grep = 0)
- หน้าจอ: list (ค้นหา/กรองสถานะ/กรองลูกค้า/กรองฝ่าย · 3 stat card · ส่งออก CSV) · wizard 3 ขั้น · ลิ้นชัก 4 แท็บ (รายละเอียด · PDF Preview · ลายเซ็น · ประวัติ)
  - PDF Preview มีปุ่มสลับชุด **ต้นฉบับ / สำเนา** (print_config.copies) · ปุ่มพิมพ์ออกทั้ง 2 ชุดในครั้งเดียว
  - เนื้อสัญญา 2 ข้อแสดงเป็นข้อความคงที่ (แก้รายฉบับไม่ได้) · ร้อยละอ่านจาก `POLICY.freeReplacePct` (mock ของ SalesPolicy)
  - DEC-11 ไม่มีปุ่มสร้างใบใหม่จากใบเดิม ทั้งในเมนู ⋮ และหัวลิ้นชัก
- ด่าน: `audit.sh` → **FAIL = 0** · WARN 3 (สืบทอดจาก base-kit ของ archetype เอง) · มี `<meta cube-archetype="Q-form">` + `window.__QA__`
- `[NO-BROWSER] ข้าม e2e_standard.py` · `[NO-BROWSER] ข้าม render-check.py` · ไม่รัน `prune_css.py` (ไม่ใช่ด่าน · เลี่ยงแตะ base-kit v6.4 ที่ห้ามแก้)
  - **แทนด้วย node stub-DOM smoke test** `_build/_smoke_html.js` — โหลดบล็อก JS จริงจาก feature.html ใน vm พร้อม stub DOM แล้วตรวจ 11 ข้อ (S1–S11) → **PASS ทั้งหมด** · ผลเก็บใน `reports/e2e_report.json`
  - ค้างให้คนดู: flow เต็มบนหน้าจอ · visual · PDF parity ในหน้าจอ → ต้องรันรอบเต็มบนเครื่องที่มี browser ก่อน UAT
- 2026-10-07 15:00 · ขั้น 5 → done
- 2026-10-07 15:00 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- `BRD_F-TMP-006.md` 19 หัวข้อ (Lane Mode — ใช้ PREBRIEF v2 + DECISIONS.lock แทน RIF · DEC = Scope Lock ชั่วคราวใน §3.3)
  - §15 Open Questions 9 ข้อ (Q1–Q9) · §19 AI Review → **APPROVED (มีเงื่อนไข)**
  - พบของที่ยังไม่มีในระบบ: ค่าตั้งค่า **`SalesPolicy.box_free_replace_pct`** (เพดานเปลี่ยนกล่องฟรีต่อปี) — ต้องสร้างก่อนเปิดใช้ · ลงใน §12 Dependencies และ §17 Operations
- `FRD_F-TMP-006_Pack/` ครบ 8 ไฟล์ (00 Overview · 01 UI · 02 API · 03 LOGIC FN-01…FN-12 · 04 DB · 05 RULES · 06 TESTS T-01…T-56 · 07 LOCKED_DECISIONS)
- `frd_lint.py` รอบแรก **BLOCK 1** (N6: ไม่พบคำว่า `approval_chain` ใน 04_DB เพราะตั้งชื่อตารางเป็น `box_loan_agreement_chain`) → แก้หัวข้อให้มีคำว่า `approval_chain` → รอบสอง **BLOCK 0 · WARN 1 · PASS 12**
- **บั๊กเครื่องมือใหม่ (#8)**: `frd_lint.py` N3 ตรวจค่าคงที่โดยดึง "เฉพาะตัวเลข" จากข้อความบนกระดาษ — ค่าคงที่ "ร้อยละ 10 (สิบ)…" เหลือเลข `10` แล้ว regex `(?<![\d.,])10(?![\d])` ไปจับคำว่า **DEC-10** และ **FN-10** ใน 03/05 เป็น hardcode (false positive)
  - ตรวจแล้วค่าจริงไม่ได้ hardcode: template อ่านจาก `{{policy.free_replace_pct}}` · logic อ่านจาก `SalesPolicy.box_free_replace_pct` · บรรทัดที่ถูกจับไม่มีค่าคงที่อยู่เลย
  - เป็น WARN ไม่ใช่ BLOCK → ด่านผ่าน · เลี่ยงไม่ได้ตราบที่ยังมี DEC/FN เลข 10 (จะเจอซ้ำกับทุกเอกสารที่ค่าคงที่ลงท้ายด้วยเลขที่ชนกับเลข DEC/FN)
- declaration ฉบับจริง (`--final` · ใส่ frd_ref ตามที่ lint พิมพ์):
  - `doccfg_tool.py brief --final --registry` → **PASS** (`numbering.frd_ref = 03_LOGIC FN-04` · `snapshot_points[].frd_ref = 03_LOGIC FN-07, FN-11`)
  - `ntf_tool.py brief --final` → **PASS** (`loa_cancelled` = FN-09 · `loa_signed_copy_attached` = FN-12)
  - `doa_tool.py brief --print-config` → **PASS** · `mdoc_tool.py brief --doccfg` → **WARN** (G01/G04/G09 ตามมาตรฐาน ตามปิดทีหลัง)
- 2026-10-07 15:13 · ขั้น 7 → done

## ขั้น 8 · UI Brief → test case AI → UAT
- `extract_anchors.py` → `reports/inventory.json` (vars 47 · z-index 22 · routes 5 · overlay 33 · toast 11 · ปุ่ม 20 · microcopy 228 · function 180 · marker 7 · archetype Q-form · __QA__ true)
- `UI_BRIEF_F-TMP-006.md` (AS-BUILT) ประกอบจาก `_build/ui_brief_head.md` (เขียนมือ §0–§13) + รายการ verbatim จาก inventory
  - ด่าน `brief_check.py` → **PASS · FAIL 0 · WARN 0** (B1 route 5/5 · B2 toast 11/11 · B3 overlay ครบ · B4 z-index 12 ค่า · B5 anchor มีจริงทั้งหมด · B6 CSS vars 47/47 · B7 microcopy 60/60 · B8 ครบ §0–§13)
  - ระวังบั๊ก #6: ใน §11 ไม่เขียนชื่อฟังก์ชันที่จงใจตัดออก — ใช้คำว่า "เมนู ⋮ มีแค่ แก้ไข · พิมพ์ · ยกเลิกเอกสาร" แทน
- `testcases-F-TMP-006.md` — **32 เคส · 102 step** (CRT 10 · DOA 8 · PERM 5 · PDF 6 · LIST 3) + Coverage Ledger + Coverage Audit + Result Report
  - `tc_lint.py` รอบแรก **ERROR 1** (Meta บอก 26 เคส แต่เครื่องมือนับได้ 32 — นับจากหัวข้อ `### TC-…` ทั้งหมด) → แก้ Meta เป็น 32 → รอบสอง **ERROR 0**
  - `[NO-BROWSER] ข้าม verify_anchors.py` (ต้องเปิด DOM ด้วย browser เพื่อเก็บข้อความจริง) → anchor ตัวหนาทุกตัวเขียนจาก `UI_BRIEF` ที่ผ่าน B5 แล้ว (anchor ทุกตัวมีจริงใน feature.html) · ต้องรัน verify_anchors รอบเต็มก่อน UAT
- `cases.json` (เอกสารแบบทดสอบสำหรับคน) แปลงจาก MD ด้วย `_build/make_cases.py` — **31 เคส** (ตัด TC-PERM-02 ที่ต้องรู้ route ภายใน)
- `QA_AUDIT_F-TMP-006.md` + `lite_audit.py --stamp` → **MD 32 เคส → เก็บ 31 · drop ledger 1 · หายเงียบ 0**
- 2026-10-07 15:22 · ขั้น 8 → done

## ขั้น 9 · ตรวจรวม + แพ็ก DevPack
- `manifest_scan.py` → 39 artifact · ซ้ำ 0 (ไม่มี `orig/content.html` เพราะใช้เส้นทาง LibreOffice → PDF ตั้งแต่ขั้น 1 จึงไม่เจอบั๊ก #2 ที่นับ prototype ซ้ำ)
- `consistency_check.py` รอบแรก **READY · BLOCK 0 · WARN 1** (K6: BRD ไม่อ้าง DEC-03 · DEC-06 · DEC-07 · DEC-09 · DEC-10 · DEC-13)
  → เติมตารางผูกมติกับหัวข้อ BRD ใน §3.3 → รอบสอง **READY · BLOCK 0 · WARN 0 · PASS 10**
  - K4 microcopy FRD 06 ↔ prototype ตรง 19 ข้อความ · K5 route ตรง · K6 FRD 07 อ้างมติครบ 16 · K7 declaration ฉบับจริงครบ · K8 testcases 32 เคสตรงกับเอกสารคนและ QA_AUDIT · K9 frd_lint BLOCK 0
