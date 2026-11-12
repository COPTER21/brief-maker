# F-TMP-005 DevPack — แบบฟอร์มรายงานผลการสอบทานคำขอซื้อและใบสั่งซื้อค้างนาน (PR/PO Outstanding) (REQ-TMP-005)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 16 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 64 เคส
- ไม่มี report e2e_standard (html-generator v9.2 #111)
- frd_lint BLOCK 0
- anchor ที่ไม่พบบนจอ 0

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K9 — ไม่มี report e2e_standard (html-generator v9.2 #111)

## อ่านอะไรก่อน
| คุณคือ | อ่านตามลำดับ |
|---|---|
| ทุกคน | 03_FRD/…/00_OVERVIEW.md → 07_LOCKED_DECISIONS.md → 05_Governance (มติ) → เปิด 01_Prototype |
| FE | 01_Prototype → 04_UI_Brief → FRD 01_UI |
| BE | FRD 02_API → 03_LOGIC → 04_DB → 05_RULES → 05_Governance → 07_Print |
| QA | 06_Test (UAT ฉบับคน · test case AI) → FRD 06_TESTS |
| PM / Owner | 02_BRD · FRD 00_OVERVIEW (คำถามค้าง) · 08_Reference/IMPACT_SUMMARY |

## โฟลเดอร์
| โฟลเดอร์ | มีอะไร | ไฟล์ |
|---|---|---|
| `01_Prototype` | หน้าจอจริง (source of truth ของ UI) | 1 |
| `02_BRD` | BRD | 2 |
| `03_FRD` | FRD Pack | 18 |
| `04_UI_Brief` | UI Brief AS-BUILT | 1 |
| `05_Governance` | มติ (DECISIONS) + ใบประกาศ DOCCFG / DOA / MDOC / NTF | 11 |
| `06_Test` | test case AI + UAT ฉบับคน + QA audit | 4 |
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 12 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 14 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT · Strike · ก่อน UAT
- OQ-03 · อายุค้าง/มูลค่า/งวด + เกณฑ์ค้างนาน (PurchaseConfig) (DEC-15) · ลูกค้า + พี่เบิร์ด · Phase 2
- OQ-04 · เมื่อ PR/PO/Supplier ขึ้นระบบ → search-select + ดึงรายการค้าง · พี่เบิร์ด · –
- OQ-05 · role-mgr-pur resolve ตามหน่วยงานผู้จัดทำ (relative) · admin ระดับฝ่าย · Strike + พี่เบิร์ด · ก่อน wire
- OQ-06 · รหัสฟอร์ม/Rev ที่ถูกต้อง (FM-PUR-003 vs FM-PUR-03 · Rev.02 vs Rev.00) (DEC-12) · ลูกค้า · ก่อน UAT
- OQ-07 · "วันที่รับ" = กำหนดรับ หรือรับจริง (DEC-13) · ลูกค้า · –
- OQ-08 · รายการ > 24 แถว / ข้อความยาว → แบบพิมพ์เพิ่มหน้า? · Strike · –
- OQ-09 · function_code taxonomy · รหัส feature จริง · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-mgr-pur · วงเงิน: ไ
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "(ไม่มีตัวเลข/ตัวเลือกพิมพ์ตายตัว) เกณฑ์ 'ค้างนาน' ไม่ได
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการคำขอซื้อ/ใบสั่งซื้อค้างนาน: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 8 แถวตามกระดา
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส PPO
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `b388f00d` | prototype |
| `02_BRD/BRD_F-TMP-005.docx` | `c783bf07` | brd_docx |
| `02_BRD/BRD_F-TMP-005.md` | `74010513` | brd |
| `03_FRD/FRD_F-TMP-005_Pack/00_OVERVIEW.md` | `8ec5fbc9` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/01_UI.md` | `5b46688d` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/02_API.md` | `2c5d20c8` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/03_LOGIC.md` | `a516a75e` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/04_DB.md` | `a69d1444` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/05_RULES.md` | `3a6999f7` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/06_TESTS.md` | `c7079711` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/07_LOCKED_DECISIONS.md` | `450f1698` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/INDEX.md` | `eebb80bf` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/_SECTION_N.md` | `10293a35` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/DOA_BRIEF_F-TMP-005.md` | `f375a0e9` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/DOCCFG_BRIEF_F-TMP-005.md` | `718c7c18` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/MDOC_BRIEF_PPO.md` | `0af6e840` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/NTF_BRIEF_F-TMP-005.md` | `41457e81` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/PPO.doa.yaml` | `78d3c35e` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/PPO.doccfg.yaml` | `7d9b0997` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/PPO.mdoc.yaml` | `067be579` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/PPO.ntf.yaml` | `a04d8b18` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-005.md` | `7abbd022` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `41ea4124` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `669cad3a` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-005.md` | `f375a0e9` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-005.md` | `718c7c18` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_PPO.md` | `0af6e840` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-005.md` | `41457e81` | ntf_brief |
| `05_Governance/PPO.doa.yaml` | `78d3c35e` | doa_yaml |
| `05_Governance/PPO.doccfg.yaml` | `7d9b0997` | doccfg_yaml |
| `05_Governance/PPO.mdoc.yaml` | `067be579` | mdoc_yaml |
| `05_Governance/PPO.ntf.yaml` | `a04d8b18` | ntf_yaml |
| `05_Governance/decisions.yaml` | `58a8b681` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-005.md` | `08d58b8b` | qa_audit |
| `06_Test/cases.json` | `c1b54bc4` | cases_json |
| `06_Test/testcase-F-TMP-005.html` | `a22aa39e` | testcases_uat |
| `06_Test/testcases-F-TMP-005.md` | `3b56d54f` | testcases_ai |
| `07_Print/FM-PUR-03_template.html` | `f1ef55fd` | print_extra_fm_pur_03_template |
| `07_Print/PPO_print-spec.md` | `fd1ed763` | print_spec |
| `07_Print/_states_sheet.png` | `6d6e257d` | print_image_states_sheet |
| `07_Print/approved-doa6steps.data.json` | `2abc8f01` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `cde26f02` | print_data_approved_data |
| `07_Print/draft.data.json` | `ab1a08c2` | print_data_draft_data |
| `07_Print/form.tpl.html` | `f3c9053e` | print_template |
| `07_Print/long-24items.data.json` | `51432032` | print_data_long_24items_data |
| `07_Print/print_config.json` | `f9983c85` | print_config |
| `07_Print/profile.json` | `c79ac3e4` | print_profile |
| `07_Print/rejected.data.json` | `26704225` | print_data_rejected_data |
| `07_Print/render_nobrowser.py` | `08187683` | print_extra_render_nobrowser |
| `08_Reference/3. FM-PUR-03 PR-PO_Outstanding.xlsx` | `6c8e6bcb` | original_3_fm_pur_03_pr_po_outstanding |
| `08_Reference/FORM_SPEC.check.json` | `4d7afabd` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `e777c970` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-005.html` | `69303ccd` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-005_v2.md` | `a0e43538` | prebrief |
| `08_Reference/RUN_LOG.md` | `e6be76eb` | run_log |
| `08_Reference/SAMPLE.pdf` | `c380677c` | original_sample |
| `08_Reference/page-1.png` | `788ccc2b` | original_page_1 |
| `08_Reference/page-2.png` | `ca87d906` | original_page_2 |
| `08_Reference/reports/_SECTION_N.md` | `10293a35` | report_frd_lint |
| `08_Reference/reports/anchors.json` | `a0d727b7` | report_anchors |
| `08_Reference/screen_create.png` | `cd09f60b` | original_screen_create |
| `08_Reference/screen_list.png` | `71f2fcef` | original_screen_list |
| `08_Reference/screen_view.png` | `e5ebb397` | original_screen_view |
