# F-TMP-003 DevPack — แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี (REQ-TMP-003)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 14 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 62 เคส
- e2e_standard 21/21
- frd_lint BLOCK 0
- anchor ที่ไม่พบบนจอ 0
- เทียบต้นฉบับ WARN 0.132

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K9 — เทียบต้นฉบับ WARN 0.132

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
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 21 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 22 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (11 ข้อ) · Strike · ก่อน UAT
- OQ-03 · role admin ฝ่ายบัญชี (ผู้บันทึกเข้าระบบ) + role-line-manager ยังไม่อยู่ใน DOA master · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · COA field (code/name) · ตรวจรหัสมีจริง/ซ้ำ · เลือกจาก COA · พี่เบิร์ด · ก่อน dev
- OQ-05 · SoD ผู้บันทึกเข้าระบบ ≠ ผู้อนุมัติ ไหม · ลูกค้า · –
- OQ-06 · รหัส feature/REQ จริง · taxonomy function_code · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · 1 ใบ = 1 ประเภทคำขอ (เพิ่ม
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ชื่อบัญชีที่ต้องการขอเพิ่ม: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 4 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส ACR
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `ed80420a` | prototype |
| `02_BRD/BRD_F-TMP-003.docx` | `4841de17` | brd_docx |
| `02_BRD/BRD_F-TMP-003.md` | `89eaa5b0` | brd |
| `03_FRD/FRD_F-TMP-003_Pack/00_OVERVIEW.md` | `022e77e5` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/01_UI.md` | `8d24f15e` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/02_API.md` | `78fb07f8` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/03_LOGIC.md` | `783e063b` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/04_DB.md` | `69e5c4fe` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/05_RULES.md` | `af3eac90` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/06_TESTS.md` | `9558c651` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/07_LOCKED_DECISIONS.md` | `b196d42d` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/INDEX.md` | `70924f36` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/_SECTION_N.md` | `44726aa4` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/ACR.doa.yaml` | `f3c3cd6e` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/ACR.doccfg.yaml` | `ce60f77d` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/ACR.mdoc.yaml` | `a78ac4a9` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/ACR.ntf.yaml` | `26786ad2` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/DOA_BRIEF_F-TMP-003.md` | `d7ccda34` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/DOCCFG_BRIEF_F-TMP-003.md` | `b54f63b3` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/MDOC_BRIEF_ACR.md` | `b9037f61` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/NTF_BRIEF_F-TMP-003.md` | `872a96cb` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-003.md` | `254e09a9` | ui_brief |
| `05_Governance/ACR.doa.yaml` | `f3c3cd6e` | doa_yaml |
| `05_Governance/ACR.doccfg.yaml` | `ce60f77d` | doccfg_yaml |
| `05_Governance/ACR.mdoc.yaml` | `a78ac4a9` | mdoc_yaml |
| `05_Governance/ACR.ntf.yaml` | `26786ad2` | ntf_yaml |
| `05_Governance/DECISIONS.lock.json` | `c5c814b7` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `7a7139aa` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-003.md` | `d7ccda34` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-003.md` | `b54f63b3` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_ACR.md` | `b9037f61` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-003.md` | `872a96cb` | ntf_brief |
| `05_Governance/decisions.yaml` | `d59d50ca` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-003.md` | `ec166f4c` | qa_audit |
| `06_Test/cases.json` | `09eea836` | cases_json |
| `06_Test/testcase-F-TMP-003.html` | `cce0e036` | testcases_uat |
| `06_Test/testcases-F-TMP-003.md` | `2d5acf0a` | testcases_ai |
| `07_Print/ACR_approved-doa6steps.pdf` | `396b19cf` | print_pdf_acr_approved_doa6steps |
| `07_Print/ACR_approved.pdf` | `41f2b1a5` | print_pdf_acr_approved |
| `07_Print/ACR_draft.pdf` | `0dcfeadd` | print_pdf_acr_draft |
| `07_Print/ACR_edit-pending.pdf` | `5566f218` | print_pdf_acr_edit_pending |
| `07_Print/ACR_long-12rows.pdf` | `55666e29` | print_pdf_acr_long_12rows |
| `07_Print/ACR_rejected.pdf` | `e1d64c30` | print_pdf_acr_rejected |
| `07_Print/ACR_states_sheet.png` | `f038578c` | print_image_acr_states_sheet |
| `07_Print/approved-doa6steps.data.json` | `1718ac20` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `72621335` | print_data_approved_data |
| `07_Print/compare.json` | `54ebe5d1` | report_compare |
| `07_Print/compare_overlay.png` | `76c44b9e` | print_image_compare_overlay |
| `07_Print/compare_side.png` | `3241d56e` | print_image_compare_side |
| `07_Print/draft.data.json` | `282ed992` | print_data_draft_data |
| `07_Print/edit-pending.data.json` | `99742377` | print_data_edit_pending_data |
| `07_Print/form.tpl.html` | `6a6e6a92` | print_template |
| `07_Print/long-12rows.data.json` | `1d5bbd21` | print_data_long_12rows_data |
| `07_Print/print_config.json` | `16564911` | print_config |
| `07_Print/profile.json` | `6a961d49` | print_profile |
| `07_Print/rejected.data.json` | `083925ea` | print_data_rejected_data |
| `07_Print/แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี_print-spec.md` | `05f41e3e` | print_spec |
| `07_Print/แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี_template.html` | `dbf0ce2f` | print_extra_template |
| `08_Reference/1. FM-ACC-01 แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี.docx` | `d03e3943` | original_1_fm_acc_01 |
| `08_Reference/FORM_SPEC.check.json` | `abfe9bec` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `d0e29ee1` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-003.html` | `538a5f56` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-003_v2.md` | `49c2096b` | prebrief |
| `08_Reference/RUN_LOG.md` | `695c853a` | run_log |
| `08_Reference/SAMPLE.pdf` | `70923bb4` | original_sample |
| `08_Reference/page-1.png` | `26da0f98` | original_page_1 |
| `08_Reference/page-2.png` | `dd83b0a9` | original_page_2 |
| `08_Reference/reports/_SECTION_N.md` | `44726aa4` | report_frd_lint |
| `08_Reference/reports/anchors.json` | `6668a40b` | report_anchors |
| `08_Reference/reports/e2e_report.json` | `44774fb3` | report_e2e |
| `08_Reference/shot_approve.png` | `d77119f9` | original_shot_approve |
| `08_Reference/shot_list.png` | `1e077c15` | original_shot_list |
| `08_Reference/shot_pdf.png` | `1f665e0d` | original_shot_pdf |
| `08_Reference/shot_record.png` | `78950635` | original_shot_record |
| `08_Reference/shot_sign.png` | `2b80d8aa` | original_shot_sign |
| `08_Reference/shot_submit.png` | `f8e2e79e` | original_shot_submit |
| `08_Reference/shot_wiz2.png` | `93da02ea` | original_shot_wiz2 |
| `08_Reference/shot_wiz3.png` | `2a8a757e` | original_shot_wiz3 |
| `08_Reference/shot_wiz_edit.png` | `c16d96c8` | original_shot_wiz_edit |
| `08_Reference/shot_wiz_empty.png` | `9fbe06a2` | original_shot_wiz_empty |
