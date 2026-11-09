# F-TMP-004 DevPack — แบบฟอร์มใบแจ้งซ่อมอุปกรณ์คอมพิวเตอร์ (REQ-TMP-004)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 18 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 58 เคส
- ไม่มี report e2e_standard (html-generator v9.2 #111)
- frd_lint BLOCK 0

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
| `03_FRD` | FRD Pack | 17 |
| `04_UI_Brief` | UI Brief AS-BUILT | 1 |
| `05_Governance` | มติ (DECISIONS) + ใบประกาศ DOCCFG / DOA / MDOC / NTF | 11 |
| `06_Test` | test case AI + UAT ฉบับคน + QA audit | 4 |
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 10 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 9 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-line-manager · วงเง
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · วันที่ต้องการส่งมอบ ต้องไม
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส CRR
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `a36b3797` | prototype |
| `02_BRD/BRD_F-TMP-004.docx` | `58815535` | brd_docx |
| `02_BRD/BRD_F-TMP-004.md` | `c8568700` | brd |
| `03_FRD/FRD_F-TMP-004_Pack/00_OVERVIEW.md` | `d0d37f82` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/01_UI.md` | `2c26a56e` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/02_API.md` | `bb760575` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/03_LOGIC.md` | `101fa11f` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/04_DB.md` | `c06efc60` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/05_RULES.md` | `bbb59bb3` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/06_TESTS.md` | `3e119efa` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/07_LOCKED_DECISIONS.md` | `2a38dc85` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/INDEX.md` | `1572a4ed` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/CRR.doa.yaml` | `4ad18775` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/CRR.doccfg.yaml` | `8f7f0934` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/CRR.mdoc.yaml` | `a29cdace` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/CRR.ntf.yaml` | `13777698` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/DOA_BRIEF_F-TMP-004.md` | `342efdb1` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/DOCCFG_BRIEF_F-TMP-004.md` | `3bf55163` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/MDOC_BRIEF_CRR.md` | `86a0c9c3` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/NTF_BRIEF_F-TMP-004.md` | `a6e90821` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-004.md` | `a32954da` | ui_brief |
| `05_Governance/CRR.doa.yaml` | `4ad18775` | doa_yaml |
| `05_Governance/CRR.doccfg.yaml` | `8f7f0934` | doccfg_yaml |
| `05_Governance/CRR.mdoc.yaml` | `a29cdace` | mdoc_yaml |
| `05_Governance/CRR.ntf.yaml` | `13777698` | ntf_yaml |
| `05_Governance/DECISIONS.lock.json` | `3c132eac` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `0a9178f6` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-004.md` | `342efdb1` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-004.md` | `3bf55163` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_CRR.md` | `86a0c9c3` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-004.md` | `a6e90821` | ntf_brief |
| `05_Governance/decisions.yaml` | `17c75450` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-004.md` | `6800881b` | qa_audit |
| `06_Test/cases.json` | `c39b3c21` | cases_json |
| `06_Test/testcase-F-TMP-004.html` | `e55501f9` | testcases_uat |
| `06_Test/testcases-F-TMP-004.md` | `9b4768e0` | testcases_ai |
| `07_Print/CRR_print-spec.md` | `03f516ac` | print_spec |
| `07_Print/approved-doa6steps.data.json` | `d987ffea` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `9e0755b9` | print_data_approved_data |
| `07_Print/draft.data.json` | `6248b11f` | print_data_draft_data |
| `07_Print/form.tpl.html` | `e331c6e1` | print_template |
| `07_Print/long-text.data.json` | `4ac126f5` | print_data_long_text_data |
| `07_Print/print_config.json` | `5997fc46` | print_config |
| `07_Print/profile.json` | `ecca1ff8` | print_profile |
| `07_Print/rejected.data.json` | `1d07c0b7` | print_data_rejected_data |
| `07_Print/แบบฟอร์มใบแจ้งซ่อมอุปกรณ์คอมพิวเตอร์_template.html` | `9e333092` | print_extra_template |
| `08_Reference/6. FM-ITS-06 แบบฟอร์มใบแจ้งซ่อมอุปกรณ์คอมพิวเตอร์.xlsx` | `66bc0458` | original_6_fm_its_06 |
| `08_Reference/FORM_SPEC.check.json` | `155ea707` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `e9ae039f` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-004.html` | `7fe99dbb` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-004_v2.md` | `81bf9e4d` | prebrief |
| `08_Reference/RUN_LOG.md` | `8df3e933` | run_log |
| `08_Reference/SAMPLE.pdf` | `fdf2072d` | original_sample |
| `08_Reference/page-1.png` | `ab4cb794` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `43d5d736` | report_frd_lint |
