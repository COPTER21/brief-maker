# F-TMP-001 DevPack — แบบสำรวจความพึงพอใจลูกค้า สำหรับลูกค้า General Trade (REQ-TMP-001)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 13 ข้อ (AI-DEFAULT 10) · พร้อมเริ่มทำ
- test case AI 30 เคส
- e2e_standard 21/21
- frd_lint BLOCK 0
- เทียบต้นฉบับ WARN 0.595

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K9 — เทียบต้นฉบับ WARN 0.595

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
| `03_FRD` | FRD Pack | 16 |
| `04_UI_Brief` | UI Brief AS-BUILT | 1 |
| `05_Governance` | มติ (DECISIONS) + ใบประกาศ DOCCFG / DOA / MDOC / NTF | 9 |
| `06_Test` | test case AI + UAT ฉบับคน + QA audit | 4 |
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 13 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 14 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่มีการอนุมัติ
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ทุกข้อคะแนนเลือกได้ 1 ค่า 
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นตามตำแหน่งกระดาษ  · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ)
- DEC-08 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติ none · admin role เห็นทั้งหมด
- DEC-09 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส CSG
- DEC-10 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `80bc0cd6` | prototype |
| `02_BRD/BRD_F-TMP-001.docx` | `ec6cdcbf` | brd_docx |
| `02_BRD/BRD_F-TMP-001.md` | `e8c4adc3` | brd |
| `03_FRD/FRD_F-TMP-001_Pack/00_OVERVIEW.md` | `c869852e` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/01_UI.md` | `1140987d` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/02_API.md` | `f24fd316` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/03_LOGIC.md` | `6f9d1ba2` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/04_DB.md` | `8f81ef57` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/05_RULES.md` | `aa6d9dd2` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/06_TESTS.md` | `dd85aa26` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/07_LOCKED_DECISIONS.md` | `897fe2b6` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/INDEX.md` | `366304c8` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/_SECTION_N.md` | `debe980a` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/CSG.doccfg.yaml` | `d7b97ee0` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/CSG.mdoc.yaml` | `37424555` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/CSG.ntf.yaml` | `5e0d5496` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/DOCCFG_BRIEF_F-TMP-001.md` | `54bf2ec2` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/MDOC_BRIEF_CSG.md` | `ff2eb0cb` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/NTF_BRIEF_F-TMP-001.md` | `67c75f4b` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-001.md` | `ae13feb9` | ui_brief |
| `05_Governance/CSG.doccfg.yaml` | `d7b97ee0` | doccfg_yaml |
| `05_Governance/CSG.mdoc.yaml` | `37424555` | mdoc_yaml |
| `05_Governance/CSG.ntf.yaml` | `5e0d5496` | ntf_yaml |
| `05_Governance/DECISIONS.lock.json` | `dc9b9b9c` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `fb5ab3d7` | decisions_md |
| `05_Governance/DOCCFG_BRIEF_F-TMP-001.md` | `54bf2ec2` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_CSG.md` | `ff2eb0cb` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-001.md` | `67c75f4b` | ntf_brief |
| `05_Governance/decisions.yaml` | `a9f30123` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-001.md` | `1e0945f2` | qa_audit |
| `06_Test/cases.json` | `d5e700f8` | cases_json |
| `06_Test/testcase-F-TMP-001.html` | `aca2d4a0` | testcases_uat |
| `06_Test/testcases-F-TMP-001.md` | `2b26355b` | testcases_ai |
| `07_Print/CSG_print-spec.md` | `adabc36c` | print_spec |
| `07_Print/_states_sheet.png` | `76bd1314` | print_image_states_sheet |
| `07_Print/cancelled.data.json` | `d8b23c22` | print_data_cancelled_data |
| `07_Print/compare.json` | `5f69a6cd` | report_compare |
| `07_Print/compare_side.png` | `8f5f6c75` | print_image_compare_side |
| `07_Print/draft.data.json` | `ed22b6c1` | print_data_draft_data |
| `07_Print/form.tpl.html` | `a4fc9436` | print_template |
| `07_Print/long-comments.data.json` | `9f07ab71` | print_data_long_comments_data |
| `07_Print/low-score.data.json` | `af902ea3` | print_data_low_score_data |
| `07_Print/print_config.json` | `349d016e` | print_config |
| `07_Print/profile.json` | `3bbb98d5` | print_profile |
| `07_Print/recorded.data.json` | `266d0018` | print_data_recorded_data |
| `07_Print/แบบสำรวจความพึงพอใจลูกค้า_GT_template.html` | `7b20f84a` | print_extra_gt_template |
| `08_Reference/10. FM-SAL-10 แบบสำรวจความพึงพอใจลูกค้า สำหรับลูกค้า General Trade.xlsx` | `4281cbdc` | original_10_fm_sal_10_general_trade |
| `08_Reference/FORM_SPEC.check.json` | `35c967bb` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `75358ffb` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-001.html` | `7070789b` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-001_v2.md` | `2d82cc81` | prebrief |
| `08_Reference/RUN_LOG.md` | `d2a101e9` | run_log |
| `08_Reference/SAMPLE.pdf` | `15d48773` | original_sample |
| `08_Reference/page-1.png` | `4a219422` | original_page_1 |
| `08_Reference/page-2.png` | `9bbf04ef` | original_page_2 |
| `08_Reference/reports/_SECTION_N.md` | `debe980a` | report_frd_lint |
| `08_Reference/reports/e2e_container_ref.json` | `ac6dc196` | report_e2e |
| `08_Reference/shot_list.png` | `576f7ddd` | original_shot_list |
| `08_Reference/shot_pdf.png` | `15935230` | original_shot_pdf |
| `08_Reference/shot_wizard.png` | `35c3dbc4` | original_shot_wizard |
