# F-TMP-001 DevPack — แบบฟอร์มใบแจ้งซ่อมสินทรัพย์ (REQ-TMP-001)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 16 ข้อ (AI-DEFAULT 12) · พร้อมเริ่มทำ
- test case AI 50 เคส
- e2e_standard 21/21
- anchor ที่ไม่พบบนจอ 0
- เทียบต้นฉบับ WARN 0.139

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K9 — เทียบต้นฉบับ WARN 0.139

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
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 18 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 14 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (12 ข้อ) · Strike · ก่อน UAT
- OQ-03 · ผู้ตรวจสอบ = ผู้บังคับบัญชา (role-line-manager) หรือเจ้าหน้าที่สินทรัพย์/ช่าง (ต้องเพิ่ม role) · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · Asset Master / Maintenance Schedule (Phase 2) · Strike · –
- OQ-05 · รหัส feature จริงแทน F-TMP-001 · function_code taxonomy · Strike · ก่อน register
- OQ-06 · Rev. ของแบบฟอร์ม · ลูกค้า · –
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ต้องมีรายการแจ้งซ่อมอย่างน
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการทรัพย์สินที่แจ้งซ่อม: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 10 แถวตามกระดาษ
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ประวัติการซ่อม: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 6 แถวตามกระดาษ
- DEC-07 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-08 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-09 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-10 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-11 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส RPR
- DEC-12 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `958d79c8` | prototype |
| `02_BRD/BRD_F-TMP-001.docx` | `d82943b3` | brd_docx |
| `02_BRD/BRD_F-TMP-001.md` | `eb9897a0` | brd |
| `03_FRD/FRD_F-TMP-001_Pack/00_OVERVIEW.md` | `43aa29b7` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/01_UI.md` | `91a97413` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/02_API.md` | `62d9d3ea` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/03_LOGIC.md` | `235f5181` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/04_DB.md` | `6fc76fcb` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/05_RULES.md` | `178c0af7` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/06_TESTS.md` | `0546ba14` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/07_LOCKED_DECISIONS.md` | `5a118be4` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/INDEX.md` | `b2f6fe42` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/_SECTION_N.md` | `33bbbc8d` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/DOA_BRIEF_F-TMP-001.md` | `7346e141` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/DOCCFG_BRIEF_F-TMP-001.md` | `2eace5d2` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/MDOC_BRIEF_RPR.md` | `efc31abe` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/NTF_BRIEF_F-TMP-001.md` | `dfca80dd` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/RPR.doa.yaml` | `34fbb5ca` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/RPR.doccfg.yaml` | `665b9ba9` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/RPR.mdoc.yaml` | `69e4ef07` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/RPR.ntf.yaml` | `22cd365d` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-001.md` | `1bb4d4ba` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `6a897ba7` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `d6c4d857` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-001.md` | `7346e141` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-001.md` | `2eace5d2` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_RPR.md` | `efc31abe` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-001.md` | `dfca80dd` | ntf_brief |
| `05_Governance/RPR.doa.yaml` | `34fbb5ca` | doa_yaml |
| `05_Governance/RPR.doccfg.yaml` | `665b9ba9` | doccfg_yaml |
| `05_Governance/RPR.mdoc.yaml` | `69e4ef07` | mdoc_yaml |
| `05_Governance/RPR.ntf.yaml` | `22cd365d` | ntf_yaml |
| `05_Governance/decisions.yaml` | `80a0a555` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-001.md` | `d4e8d1d3` | qa_audit |
| `06_Test/cases.json` | `42c4be72` | cases_json |
| `06_Test/testcase-F-TMP-001.html` | `f62ec937` | testcases_uat |
| `06_Test/testcases-F-TMP-001.md` | `c5a21001` | testcases_ai |
| `07_Print/FM-ASM-03_print-spec.md` | `7e70d871` | print_spec |
| `07_Print/FM-ASM-03_template.html` | `228f955c` | print_extra_fm_asm_03_template |
| `07_Print/RPR_approved-doa6steps.pdf` | `47daf893` | print_pdf_rpr_approved_doa6steps |
| `07_Print/RPR_approved.pdf` | `7ae1632b` | print_pdf_rpr_approved |
| `07_Print/RPR_draft.pdf` | `25350380` | print_pdf_rpr_draft |
| `07_Print/RPR_long-14rows.pdf` | `0f804c03` | print_pdf_rpr_long_14rows |
| `07_Print/RPR_rejected.pdf` | `7c16373a` | print_pdf_rpr_rejected |
| `07_Print/RPR_states_sheet.png` | `17da9e6b` | print_image_rpr_states_sheet |
| `07_Print/approved-doa6steps.data.json` | `e960d56c` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `c79677e0` | print_data_approved_data |
| `07_Print/compare.json` | `e6c8a281` | report_compare |
| `07_Print/compare_side.png` | `dbd16092` | print_image_compare_side |
| `07_Print/draft.data.json` | `27ccff4a` | print_data_draft_data |
| `07_Print/form.tpl.html` | `03bc7f8b` | print_template |
| `07_Print/long-14rows.data.json` | `7cd43982` | print_data_long_14rows_data |
| `07_Print/print_config.json` | `07aa990f` | print_config |
| `07_Print/profile.json` | `a72006c6` | print_profile |
| `07_Print/rejected.data.json` | `e872d1a3` | print_data_rejected_data |
| `08_Reference/3. FM-ASM-03 แบบฟอร์มใบแจ้งซ่อมสินทรัพย์.xlsx` | `b7714607` | original_3_fm_asm_03 |
| `08_Reference/FORM_SPEC.check.json` | `18719b67` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `417ef949` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-001.html` | `2399a6e0` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-001_v2.md` | `21558135` | prebrief |
| `08_Reference/RUN_LOG.md` | `90add351` | run_log |
| `08_Reference/SAMPLE.pdf` | `b9c62ba5` | original_sample |
| `08_Reference/page-1.png` | `e34c7364` | original_page_1 |
| `08_Reference/reports/anchors.json` | `e4c40f7a` | report_anchors |
| `08_Reference/reports/e2e_report.json` | `b4387378` | report_e2e |
| `08_Reference/shot_list.png` | `8d603863` | original_shot_list |
| `08_Reference/shot_sign.png` | `c4e1f05e` | original_shot_sign |
| `08_Reference/shot_view.png` | `2cd26658` | original_shot_view |
| `08_Reference/shot_wizard.png` | `a429ab17` | original_shot_wizard |
