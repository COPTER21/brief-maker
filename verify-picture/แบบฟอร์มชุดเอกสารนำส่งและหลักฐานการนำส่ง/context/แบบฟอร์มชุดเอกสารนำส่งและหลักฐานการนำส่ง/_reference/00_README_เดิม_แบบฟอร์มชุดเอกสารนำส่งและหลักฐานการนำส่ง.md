# F-TMP-009 DevPack — แบบฟอร์มชุดเอกสารนำส่งและหลักฐานการนำส่ง (REQ-TMP-009)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 21 ข้อ (AI-DEFAULT 12) · พร้อมเริ่มทำ
- test case AI 45 เคส
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
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 11 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 9 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ลำดับแถวทั้งสองตาราง ระบบร
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการตรวจสอบชุดเอกสาร: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 10 แถวตามกระดาษ
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: หลักฐานการนำส่งเอกสาร: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 15 แถวตามกระดาษ
- DEC-07 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-08 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-09 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-10 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-11 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส IVMG
- DEC-12 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `1acbf891` | prototype |
| `02_BRD/BRD_F-TMP-009.docx` | `5b714d18` | brd_docx |
| `02_BRD/BRD_F-TMP-009.md` | `d2711a66` | brd |
| `03_FRD/FRD_F-TMP-009_Pack/00_OVERVIEW.md` | `687510ea` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/01_UI.md` | `12f79b73` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/02_API.md` | `400ed122` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/03_LOGIC.md` | `38c1cda0` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/04_DB.md` | `5e6c92c2` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/05_RULES.md` | `cf68df9f` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/06_TESTS.md` | `0ec28ba3` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/07_LOCKED_DECISIONS.md` | `01b61f51` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/INDEX.md` | `85b8cc4a` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/_SECTION_N.md` | `67f13526` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/declarations/DOA_BRIEF_F-TMP-009.md` | `0c559a78` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/declarations/DOCCFG_BRIEF_F-TMP-009.md` | `e4969ff5` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/declarations/IVMG.doa.yaml` | `0b84556a` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/declarations/IVMG.doccfg.yaml` | `b793bf1c` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/declarations/IVMG.mdoc.yaml` | `969fb561` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/declarations/IVMG.ntf.yaml` | `328711d9` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/declarations/MDOC_BRIEF_IVMG.md` | `8330ef58` | frd_pack |
| `03_FRD/FRD_F-TMP-009_Pack/declarations/NTF_BRIEF_F-TMP-009.md` | `5b972d91` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-009.md` | `1512d3f8` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `ed548f80` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `8228bd97` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-009.md` | `0c559a78` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-009.md` | `e4969ff5` | doccfg_brief |
| `05_Governance/IVMG.doa.yaml` | `0b84556a` | doa_yaml |
| `05_Governance/IVMG.doccfg.yaml` | `b793bf1c` | doccfg_yaml |
| `05_Governance/IVMG.mdoc.yaml` | `969fb561` | mdoc_yaml |
| `05_Governance/IVMG.ntf.yaml` | `328711d9` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_IVMG.md` | `8330ef58` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-009.md` | `5b972d91` | ntf_brief |
| `05_Governance/decisions.yaml` | `e75f2c39` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-009.md` | `2e67ab11` | qa_audit |
| `06_Test/cases.json` | `359a0cc9` | cases_json |
| `06_Test/testcase-F-TMP-009.html` | `5cc8b3d1` | testcases_uat |
| `06_Test/testcases-F-TMP-009.md` | `7f205841` | testcases_ai |
| `07_Print/R3.data.json` | `078f4d89` | print_data_r3_data |
| `07_Print/approved-doa6steps.data.json` | `52f26f6f` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `9ad014aa` | print_data_approved_data |
| `07_Print/draft.data.json` | `d217e755` | print_data_draft_data |
| `07_Print/form.tpl.html` | `faf78427` | print_template |
| `07_Print/long-16rows.data.json` | `317a3c20` | print_data_long_16rows_data |
| `07_Print/print_config.json` | `0be977fa` | print_config |
| `07_Print/profile.json` | `387dcafa` | print_profile |
| `07_Print/rejected.data.json` | `4b118928` | print_data_rejected_data |
| `07_Print/แบบฟอร์มชุดเอกสารนำส่งและหลักฐานการนำส่ง_print-spec.md` | `d5873038` | print_spec |
| `07_Print/แบบฟอร์มชุดเอกสารนำส่งและหลักฐานการนำส่ง_template.html` | `90b70931` | print_extra_template |
| `08_Reference/7. FM-IVM-07 แบบฟอร์มชุดเอกสารนำส่งและหลักฐานการนำส่ง.xlsx` | `2a1c71a6` | original_7_fm_ivm_07 |
| `08_Reference/FORM_SPEC.check.json` | `5b1dd309` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `80849250` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-009.html` | `a585595a` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-009_v2.md` | `c3a5c9b8` | prebrief |
| `08_Reference/RUN_LOG.md` | `383ff081` | run_log |
| `08_Reference/SAMPLE.pdf` | `637f0cf6` | original_sample |
| `08_Reference/page-1.png` | `a95fc970` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `67f13526` | report_frd_lint |
