# F-TMP-009 DevPack — แบบฟอร์มขอลงทะเบียนควบคุมสัญญา/เอกสารสำคัญ (REQ-TMP-009)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 14 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 41 เคส
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
| `03_FRD` | FRD Pack | 18 |
| `04_UI_Brief` | UI Brief AS-BUILT | 1 |
| `05_Governance` | มติ (DECISIONS) + ใบประกาศ DOCCFG / DOA / MDOC / NTF | 11 |
| `06_Test` | test case AI + UAT ฉบับคน + QA audit | 4 |
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 10 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 9 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · วันที่สิ้นสุดสัญญาต้องไม่ก
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ) · รวม/แยก: วันที่เริ่มต้นและสิ้
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส CTR
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `cfd62b85` | prototype |
| `02_BRD/BRD_F-TMP-009.docx` | `8978aa55` | brd_docx |
| `02_BRD/BRD_F-TMP-009.md` | `7efdd8ad` | brd |
| `03_FRD/FRD_F-TMP-009_Pack/00_OVERVIEW.md` | `c2105dab` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/01_UI.md` | `c1be3e5d` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/02_API.md` | `db63e539` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/03_LOGIC.md` | `5883ed32` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/04_DB.md` | `417bc16b` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/05_RULES.md` | `60e3d7ef` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/06_TESTS.md` | `c70fb82a` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/07_LOCKED_DECISIONS.md` | `e4647879` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/INDEX.md` | `a9cbdb28` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/_SECTION_N.md` | `4d30036a` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/declarations/CTR.doa.yaml` | `2b17774f` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/declarations/CTR.doccfg.yaml` | `33a34bc3` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/declarations/CTR.mdoc.yaml` | `15bf41a6` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/declarations/CTR.ntf.yaml` | `c76bd9c9` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/declarations/DOA_BRIEF_F-TMP-009.md` | `ea792d5a` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/declarations/DOCCFG_BRIEF_F-TMP-009.md` | `758a6902` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/declarations/MDOC_BRIEF_CTR.md` | `205a43bc` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/declarations/NTF_BRIEF_F-TMP-009.md` | `07f7bab1` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-009.md` | `f81270f5` | ui_brief |
| `05_Governance/CTR.doa.yaml` | `2b17774f` | doa_yaml |
| `05_Governance/CTR.doccfg.yaml` | `33a34bc3` | doccfg_yaml |
| `05_Governance/CTR.mdoc.yaml` | `15bf41a6` | mdoc_yaml |
| `05_Governance/CTR.ntf.yaml` | `c76bd9c9` | ntf_yaml |
| `05_Governance/DECISIONS.lock.json` | `3abd7e5d` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `6300e6f9` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-009.md` | `ea792d5a` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-009.md` | `758a6902` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_CTR.md` | `205a43bc` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-009.md` | `07f7bab1` | ntf_brief |
| `05_Governance/decisions.yaml` | `6403b9c7` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-009.md` | `aa2c78f1` | qa_audit |
| `06_Test/cases.json` | `73d64f3e` | cases_json |
| `06_Test/testcase-F-TMP-009.html` | `cc3db0bf` | testcases_uat |
| `06_Test/testcases-F-TMP-009.md` | `d7e536fe` | testcases_ai |
| `07_Print/CTR_print-spec.md` | `b8375909` | print_spec |
| `07_Print/CTR_template.html` | `02649be0` | print_extra_ctr_template |
| `07_Print/approved-doa6steps.data.json` | `477c6caa` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `89dd199c` | print_data_approved_data |
| `07_Print/draft.data.json` | `3ab9ef57` | print_data_draft_data |
| `07_Print/form.tpl.html` | `47d66f41` | print_template |
| `07_Print/long-text.data.json` | `1f742d7c` | print_data_long_text_data |
| `07_Print/print_config.json` | `d679c66a` | print_config |
| `07_Print/profile.json` | `f9532fb7` | print_profile |
| `07_Print/rejected.data.json` | `01e0434d` | print_data_rejected_data |
| `08_Reference/1. FM-AGM-01 แบบฟอร์มลงทะเบียนควบคุมสัญญา.docx` | `13634e55` | original_1_fm_agm_01 |
| `08_Reference/FORM_SPEC.check.json` | `dfa943bc` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `b94d13e8` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-009.html` | `2fb9f4a7` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-009_v2.md` | `070f0be5` | prebrief |
| `08_Reference/RUN_LOG.md` | `c2e17bf3` | run_log |
| `08_Reference/SAMPLE.pdf` | `2a09df2f` | original_sample |
| `08_Reference/page-1.png` | `b61df172` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `4d30036a` | report_frd_lint |
