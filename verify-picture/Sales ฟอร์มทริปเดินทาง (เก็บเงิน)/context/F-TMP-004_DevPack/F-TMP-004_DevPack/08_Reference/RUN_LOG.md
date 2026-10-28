# RUN_LOG — F-TMP-004 ฟอร์มทริปเดินทาง (เก็บเงิน) (REQ-TMP-004)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)

## ขั้น 1 · อ่านฟอร์ม + PREBRIEF v2 (2026-10-07)
- โหมดรอบนี้: **NO-BROWSER** — ข้ามสคริปต์ที่ต้องเปิด browser ทุกตัว บันทึกเป็น `[NO-BROWSER] ข้าม <สคริปต์>`
- ต้นฉบับ .xlsx 1 ชีท (`ทริปเดือน เก็บเงิน sales`) · ใช้ `_system/tools/to_image.py` แทน `extract_assets.py` → ได้ `orig/SAMPLE.pdf` + `orig/page-1.png` + `orig/content.html`
  - วิธีแปลง: LibreOffice → PDF → pypdfium2 (หน้ากระดาษจริง 1 หน้า A4 แนวนอน) → เทียบ layout ได้
  - ภาพ render ไม่มีฟอนต์ไทยใน LibreOffice (ตัวอักษรไทยเป็นกล่องว่าง) → **ถ้อยคำยึด `orig/content.src.txt` + cell dump จาก openpyxl · ตำแหน่ง/เส้น/สัดส่วนคอลัมน์ยึด page-1.png**
  - ย้าย `orig/content.html` → `orig/content.src.txt` แล้ว (กัน manifest_scan นับเป็น prototype ซ้ำ — บั๊กที่รู้แล้ว)
- ชื่อเอกสาร: หัวฟอร์มระบุ "ใบเดินทาง : เขตการขาย General Trade" ซึ่งเฉพาะเจาะจงกว่าชื่องาน → `dm.sh rename J004 "ใบเดินทาง เขตการขาย General Trade (เก็บเงิน)"` (คง "(เก็บเงิน)" จากชื่อชีทต้นฉบับ)
- FORM_SPEC: 38 ช่อง (ระบบ 2 · กรอก 22 · คำนวณ 13 · ระบบใส่ 1) · แถวซ้ำ 1 กลุ่ม 31 แถว · ตัวเลือก 0 · สูตร 13 · ค่าคงที่ 0 · ลายเซ็น 3 · ข้อมูลขัดกัน 5
- `form_spec_check.py` → **ERROR 0** · gate ที่ต้องถาม G1–G10
- ข้อมูลส่วนบุคคล: ต้นฉบับเป็นฟอร์มเปล่า ไม่มีข้อมูลจริงกรอกไว้ → ไม่มี sample ที่ติด pdpa ไหลเข้า prototype (ช่อง "ผู้รับผิดชอบเขต" ติด `pdpa: true` ไว้ตามชนิดข้อมูล)
- ข้อมูลขัดกันที่พบในต้นฉบับ (เข้าเป็น validation rule):
  1. สูตรรวมยอด 8/13 ช่องครอบช่วงไม่ครบ 31 แถว (I9:I33 · J9:J37 · K9:K31 · L9:L32 · M9:M33 · O9:O30 · Q9:Q33 · S9:S33) → ยอดรวมต่ำกว่าจริง
  2. แถวที่ 31 คอลัมน์ "จังหวัดที่ปฎิบัติงาน" มีสูตรค้าง `=D39` (อ้างช่อง "เริ่มต้นตลาด")
  3. หัวคอลัมน์ "จำนวน" ไม่ระบุหน่วย → ตั้งค่าเริ่ม "จำนวนร้านที่เข้าเยี่ยม" รอลูกค้ายืนยัน
  4. กระดาษสะกด "Accual" (ควรเป็น "Actual") · 5. กระดาษสะกด "ปฎิบัติงาน" (ควรเป็น "ปฏิบัติงาน") → คงถ้อยคำตามกระดาษในแบบพิมพ์ เสนอแก้ในรายงาน
- PREBRIEF จาก CMS: ไม่มี → สร้าง `PREBRIEF_REQ-TMP-004_v2.md` จาก FORM_SPEC (`--cls FRM --module sales`)
- `impact_summary.py`: regex `REQ-[\d-]+` ไม่รับ `REQ-TMP-004` → รันผ่านสำเนาที่แทนเป็น `REQ-2569-0004` ใน `_tmp_impact/` แล้วแทนกลับเป็น `REQ-TMP-004` ในไฟล์ผลลัพธ์ · ลบโฟลเดอร์ชั่วคราวแล้ว
- 2026-10-07 13:27 · ขั้น 1 → done

## ขั้น 2 · Gate 10 หมวด → DECISIONS.lock (2026-10-07 · unattended)
- ตอบเองทั้ง 10 หมวดตาม `4_knowledge/governance/unattended-policy.md` → `decisions.yaml` → `decisions_lock.py` → **"พร้อมเริ่มทำ" (exit 0)** → `dm.sh tag J004` ติด AI-DEFAULT 11 มติ (DEC-12..16 เป็น VALID จาก FORM_SPEC ไม่ติดป้าย)
- เหตุผลรายหมวด:
  - G1 — ใบเดินทางเป็นแผน/ผลการออกตลาดของพนักงานขาย ไม่มีช่องใดสั่งแก้ค่าตั้งต้น และไม่มีเอกสารปลายทางระบุบนกระดาษ → `config_changes: []` · `post_to: []`
  - G2 — กระดาษมีช่องลงชื่อ 3 ช่อง: "ผู้นำเสนอ" (ผู้ขอ) + "ผู้อนุมัติ" 2 ช่อง → dynamic 2 ขั้น `role-line-manager` → `role-mgr-sales` (ผู้จัดการ module sales ตาม doa-roles-contract §3) · ไม่มีช่วงวงเงินบนกระดาษ → `amount: none`
  - G3 — ไม่มีค่าคงที่พิมพ์ตายตัว · มีสูตรรวมยอด 13 ช่อง → คำนวณอัตโนมัติ ผู้ใช้แก้ไม่ได้ · แก้สูตรที่ครอบช่วงไม่ครบในต้นฉบับ · Accual > แผน = เตือน ไม่บล็อก
  - G4 — กระดาษ 31 แถว (1 เดือน) → ไม่จำกัดจำนวนแถว · PDF ขั้นต่ำ 31 แถว
  - G5 — 1:1 ไม่เพิ่มช่อง · คงคำสะกดบนกระดาษ ("Accual" · "ปฎิบัติงาน") เพื่อ parity แล้วเสนอแก้ในรายงาน
  - G6 — แถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ
  - G7 — ไม่อนุมัติ = กลับเป็นร่างเลขเดิม · ยกเลิกได้โดยเจ้าของ + admin role เฉพาะสถานะ draft/pending · ต้องมีเหตุผล
  - G8 — เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role ของหน่วยงานเจ้าของเห็นทั้งหมด
  - G9 — ไม่ใช่เอกสารการเงินที่ต้อง no-gap → ออกเลขตอนบันทึกครั้งแรก · รหัส **TRV** (ใบเดินทาง/Travel · ไม่ชนกับ ACL · MEM · VAN ใน registry)
  - G10 — แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗
- `impact_summary.py` ฉบับยืนยัน: ใช้วิธีเลี่ยงบั๊ก regex เดิม (สำเนา REQ-2569-0004 → แทนกลับ)
- 2026-10-07 13:29 · ขั้น 2 → done

## ขั้น 3 · ร่าง declaration (doa · ntf) (2026-10-07)
- `doa_tool.py init --code TRV --module sales` → `TRV.doa.yaml` · 1 set · 2 ขั้น (role-line-manager → role-mgr-sales) · mode dynamic · on_reject back_to_draft · `brief` → **VERDICT PASS** (BLOCK 0)
  - `amount: none` ตาม DEC-03 แม้เอกสารมีช่องจำนวนเงิน — กระดาษไม่มีช่วงวงเงิน และใบนี้เป็นแผน/ผลการออกตลาด ไม่ใช่ใบขออนุมัติใช้เงิน (ยกให้ลูกค้ายืนยันในใบเซ็น)
  - `role-line-manager` ยังไม่อยู่ใน Roles Master 14 ตัวของ doa-roles-contract (อยู่ในกลุ่ม "ใช้จริงแต่ยังไม่อยู่ใน master") → แจ้งใน _BATCH_REPORT
- `ntf_tool.py suggest` ได้ 2 event · ตัด `trv_over_limit_approved` (review: true · ผู้รับเป็น TODO-role) เหลือ `trv_cancelled` → `brief` → **VERDICT PASS** (BLOCK 0)
- doccfg + mdoc รอ `print_config.json` จากขั้น 4
- 2026-10-07 13:30 · ขั้น 3 → done

## ขั้น 4 · แบบพิมพ์ Replica + doccfg/mdoc (2026-10-07)
- โหมด Replica · บล็อก **R9 ตารางกรอบ** (ต้นฉบับเป็นตาราง Excel เส้นทึบ 19 คอลัมน์ × 31 แถว) + B6 sign_rows + B7 footer
- ไฟล์: `print/form.tpl.html` · `print/profile.json` · `print/print_config.json` · `print/make_data.py` · data 5 สถานะ · `print/TRV_template.html` · `print/TRV_print-spec.md` · `print/TRV_data-contract.md`
- 5 สถานะ: ร่าง 5 แถว · อนุมัติแล้ว 20 แถว · ไม่อนุมัติ 12 แถว · ยาว 36 แถว (dense) · **DOA 6 ขั้น → 7 ช่อง 2 แถว (4+3)** ✔ ตรงกติกา v2.1
- ด่าน: `parity_check.py` → **IDENTICAL 5/5** · `render_doc.py --strict` ทุกสถานะ → ไม่มี `{{}}` หลง (0) · `build_html.py` ผ่านทุกไฟล์
- `[NO-BROWSER] ข้าม render_states.py` (ไม่ได้ `_states_sheet.png` · ยังไม่ยืนยันจำนวนหน้า)
- `[NO-BROWSER] ข้าม compare_original.py` (ไม่ได้ `compare_side.png` / score เทียบต้นฉบับ)
- `[NO-BROWSER] ข้าม render_pdf.py` (ไม่มี PDF ในชุดส่งมอบ)
- **ความต่างจากกระดาษที่ต้องให้คนเคาะ** (บันทึกใน print-spec §7)
  1. ต้นฉบับ **A4 แนวนอน** แต่ base.css ล็อก `@page size:A4 portrait` และห้ามแก้ base.css รายเอกสาร → ทำเป็นแนวตั้ง + ย่อขนาดผ่าน profile (form_fs 5.6pt · row_h 5.2mm)
  2. สัดส่วนความกว้างคอลัมน์ไม่ตรงต้นฉบับ — โหมด Replica ห้าม style ใน body และมีคลาสความกว้างแค่ g-25/g-50/g-75 → ใช้ 19 คอลัมน์เท่ากัน
- `doccfg_tool.py init` + `brief --registry 4_knowledge/governance/doccfg_registry_codes.txt` → **VERDICT PASS** · code **TRV** ไม่ชน (ACL · MEM · VAN)
- `mdoc_tool.py brief --doccfg` → **VERDICT WARN** (G04 ยังไม่มี taxonomy_def_id · G09 doa = pending) — WARN มาตรฐานของงานรอบนี้ ไม่บล็อก
- `doa_tool.py validate --print-config` → **VERDICT PASS** (INFO G1 `role-line-manager` เป็น relative role ต้องยืนยันกับ DOA กลาง)
- 2026-10-07 13:38 · ขั้น 4 → done

## ขั้น 5 · HTML Q-form (feature.html) (2026-10-07)
- สร้างจาก archetype canonical `references/form-archetype/_SOURCE_form-request-reference.html` (Pattern Q2 · v9.2)
  - ส่วน generic (BASE-KIT CSS · shell · search-select · formatters · render preservation) ลอกตรง
  - ส่วน domain เขียนใหม่ทั้งก้อนตาม FORM_SPEC + DECISIONS.lock → `_build/trv_domain.js` + `_build/assemble_trv.py` (ประกอบซ้ำได้)
  - `<meta name="cube-archetype" content="Q-form">` ติดมากับ archetype (Rule #112)
- ช่องตาม FORM_SPEC 1:1 (DEC-06) · wizard 3 ขั้น (ข้อมูลหลักใบเดินทาง · เอกสารแนบ · ตรวจสอบและยืนยัน — DEC-11 แนบไฟล์ ✓)
  - การ์ด ① ใบนี้ของเขตไหน รอบไหน (TO · CC · เขต · รอบการขาย — ผู้รับผิดชอบเขต/ตำแหน่งดึงจากระบบ ไม่ใช่ช่องกรอก)
  - การ์ด ② วันทำงานของรอบนี้ = **ตาราง 19 คอลัมน์ตามกระดาษ** (Rule #107: แถวซ้ำ > 4 ช่อง → ตาราง ไม่ใช่การ์ด) + แถวรวมยอดอัปเดตสดแบบ soft
- ยอดรวม 13 ช่องเป็น computed ล้วน ผู้ใช้แก้ไม่ได้ และรวมทุกแถวเสมอ (DEC-04 · DEC-12) · เตือนเมื่อ Accual > แผน (ไม่บล็อก)
- DOA dynamic (DEC-03): `MOCK_DOA_RESOLVED` 2 ขั้น + `resolveDoa()` + DOA-ENGINE-HOOK · modal ส่ง = 1 slot ต่อขั้น · ไม่ fix จำนวนขั้น/ชื่อคน
- ไม่อนุมัติ = **กลับเป็นร่างเลขเดิม** (DEC-08) → สถานะ draft + ป้าย "ส่งกลับแก้ไข" + แบนเนอร์เหตุผล · chain resolve ใหม่ตอนส่งรอบถัดไป (BR-DOA-02)
- ยกเลิกเฉพาะสถานะ ร่าง/รออนุมัติ โดยเจ้าของ + admin role (DEC-08) · การมองเห็นตาม DEC-09 (ร่างของคนอื่นไม่รั่วถึงผู้อนุมัติ)
- DEC-11: **ไม่มีปุ่ม "ทำซ้ำ"** ทั้งใน ⋮ และหัวลิ้นชัก (ต่างจาก archetype canonical) · ส่งออก CSV ✓ · ประกาศ ✗
- PDF Preview ฝัง `print/form.tpl.html` เป็น `TRV_TPL` (ฉีดจากไฟล์เดียวกับฝั่ง server) + `tplRender` + `tplSignRows` (ผลการแบ่งแถวเท่ากับ `sign_rows.py`)
- **Rule #114**: ช่องวันที่ทุกช่องใช้ `bedateHTML()` (ตัวเลือกวัน พ.ศ. กลาง) + CSS ของ block — ไม่มี `input type="date"` ในไฟล์
- **ด่าน**: `audit.sh` → **FAIL=0** · WARN=3 (BASE-KIT ทั้งหมด = baseline เดียวกับ archetype) · `prune_css.py` ตัด 60 rule (ลด 5.5 KB) แล้วรัน audit ซ้ำ FAIL=0
- **[NO-BROWSER] ข้าม `e2e_standard.py`** · **[NO-BROWSER] ข้าม `render-check.py`** → `reports/e2e_report.json` status = SKIPPED
  - ทดแทนด้วย `reports/nodom_smoke.js` (node + stub DOM) → **ALL CHECKS OK**
    - docPrintData + tplRender ทุก record 11 ใบ → ไม่มี `{{}}` หลง ไม่มี `undefined` · แบบพิมพ์เติมบรรทัดว่างครบ 31 ทุกใบ
    - ยอดรวมครบทุกแถว (18 แถว × 13 คอลัมน์) · DOA 6 ขั้น → ช่องลงชื่อ 7 ช่อง 2 แถว (4+3) · dense = true
    - การมองเห็น: owner เห็น 5 · ผู้อนุมัติเห็น 6 · admin (ผจก.ฝ่ายขาย) เห็น 11 · ร่างของคนอื่นรั่วถึงผู้อนุมัติ = 0
    - ใบที่ถูกส่งกลับแก้ไข = ร่างเลขเดิม (DEC-08) · ไม่มีปุ่มทำซ้ำ (DEC-11) · ไม่มี `type="date"` (#114)
- ข้อมูลตัวอย่างทั้งหมดเป็นชื่อ/บริษัท/เขตสมมติ + โลโก้ placeholder (ไม่ใช้ข้อมูลจากไฟล์ลูกค้า)
- 2026-10-07 13:52 · ขั้น 5 → done
- 2026-10-07 13:52 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 6 · ดู HTML + PDF (ข้ามตามโหมดไม่เฝ้า)
- `mark J004 6 skip --note "unattended — ให้คนดูจาก _BATCH_REPORT"`
- ภาพที่ควรมีให้คนเปิดดูภายหลัง: `print/out/_states_sheet.png` **ยังไม่มี** ([NO-BROWSER]) → ต้องรัน `render_states.py` บนเครื่องที่มี browser
  - แทนด้วย `print/out/*.html` ครบ 5 สถานะ (เปิดดูในเบราว์เซอร์ได้ตรง ๆ) + `feature.html`

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง (2026-10-07)
- `BRD_F-TMP-004.md` (Prebrief Mode — PREBRIEF v2 + DECISIONS.lock แทน RIF · DEC = Scope Lock ชั่วคราวใน §3.4) → **AI Review = APPROVED (มีเงื่อนไข)**
  - เงื่อนไข: ต้องได้คำตอบ Open Questions Q1–Q8 + รันรอบเต็มที่มี browser ก่อน UAT
- `FRD_F-TMP-004_Pack/` ครบ 8 ไฟล์ (00_OVERVIEW · 01_UI · 02_API · 03_LOGIC · 04_DB · 05_RULES · 06_TESTS · 07_LOCKED_DECISIONS)
  - 07 §7.0 = DECISIONS.lock ครบ 16 มติ · 05 §5 ผูกมติ VALID (DEC-12…16) เป็นกฎตรวจ
- **ด่าน** `frd_lint.py` → **BLOCK 0 · WARN 0 · PASS 11** (`reports/_SECTION_N.md`)
  - N1 DEC ครบ 16 · N2 ทุกช่องมีคีย์ใน 04/01 · N4 เคสปฏิเสธสิทธิ์ 9 จุด + เคส "ผู้อนุมัติไม่เห็นร่างของคนอื่น"
  - N5 ไม่อ้าง F185 API-23 · มี header_snapshot · จุดออกเลข FN-04 · N6 approval_chain + doa_ref · N7 event trv_cancelled ถูกอ้าง
- declaration ฉบับจริง (ใส่ frd_ref ตามที่ lint พิมพ์):
  - `doccfg_tool.py brief --final --registry` → **PASS** (numbering.frd_ref = 03_LOGIC FN-04 · snapshot = FN-11)
  - `ntf_tool.py brief --final` → **PASS** (trv_cancelled.frd_ref = 03_LOGIC FN-09)
  - `doa_tool.py` + `mdoc_tool.py` คงผลจากขั้น 3/4 (PASS · WARN มาตรฐาน 2 ข้อ)
- 2026-10-07 14:04 · ขั้น 7 → done

## ขั้น 8 · UI Brief → test case AI → UAT (2026-10-07)
- `extract_anchors.py` → `reports/inventory.json` (vars 47 · z-index 22 · routes 5 · overlay 33 · toast 10 · ปุ่ม 20 · microcopy 233 · function 188 · marker 7 · archetype Q-form · `__QA__` ✓)
- `UI_BRIEF_F-TMP-004.md` (AS-BUILT · §0–§13) — ส่วนบรรยายเขียนเอง + รายการ verbatim (token · z-index · toast · microcopy · function · marker) ประกอบด้วย `_build/make_ui_brief.py` จาก inventory
  - **ด่าน** `brief_check.py` → **PASS · FAIL 0 · WARN 0** (B1 route 5 · B2 toast 10 · B3 overlay ครบ · B4 z-index 12 ค่า · B5 anchor มีจริงทั้งหมด · B6 CSS vars 47/47 · B7 microcopy 60/60 · B8 ครบ 14 section)
  - แก้ 1 รอบ: ตอนแรก B5 FAIL เพราะ brief อ้าง `dupRec` (ฟังก์ชันที่ตัดออกตาม DEC-11) และ `#toast-root` (ของจริงคือ `#toast`) → แก้ข้อความแล้วผ่าน
- `testcases-F-TMP-004.md` — **33 เคส · 137 step** (CRT 11 · DOA 10 · PERM 4 · PDF 5 · LIST 3) + Coverage Ledger + Coverage Audit + Result Report
  - **ด่าน** `tc_lint.py` → **ERROR 0** (`reports/tc_counts.json`)
- `cases.json` (เอกสารแบบทดสอบสำหรับคน) — 32 เคส · ตัด `TC-PERM-02` (ต้องรู้รหัสภายในของเอกสาร) บันทึกใน Drop Ledger ของ `QA_AUDIT_F-TMP-004.md`
  - **ด่าน** `lite_audit.py --stamp` → **หายเงียบ 0 · คิดเคสใหม่ 0** · ประทับ `meta.source` แล้ว
- **[NO-BROWSER] ข้าม `verify_anchors.py`** (ต้องเปิดไฟล์ในเบราว์เซอร์เพื่อยืนยัน anchor บนจอจริง) → ไม่มี `reports/anchors.json`
- **[NO-BROWSER] ข้าม `capture.py`** และ build เอกสาร UAT HTML (`build.py`) → ยังไม่มีภาพประกอบ · ทุก step ตั้ง `regionKey` รอไว้แล้ว
- 2026-10-07 14:14 · ขั้น 8 → done
