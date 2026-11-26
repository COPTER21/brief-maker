# F-TMP-002 DevPack — แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ (REQ-TMP-002)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 15 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 40 เคส
- e2e_standard 21/21
- frd_lint BLOCK 0
- anchor ที่ไม่พบบนจอ 0
- เทียบต้นฉบับ WARN 0.554

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K9 — เทียบต้นฉบับ WARN 0.554

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
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 19 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 16 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ต้องมีเหตุผลอย่างน้อย 1 แถ
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: เหตุผลการไม่ดำเนินโครงการต่อ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 8 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส IVMJ
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `a06e92d9` | prototype |
| `02_BRD/BRD_F-TMP-002.docx` | `e889fc4d` | brd_docx |
| `02_BRD/BRD_F-TMP-002.md` | `f4962186` | brd |
| `03_FRD/FRD_F-TMP-002_Pack/00_OVERVIEW.md` | `814e5e67` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/01_UI.md` | `9e9b707c` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/02_API.md` | `d8514fdd` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/03_LOGIC.md` | `fd5b1862` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/04_DB.md` | `d503bdf3` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/05_RULES.md` | `0cf26b33` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/06_TESTS.md` | `594ced40` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/07_LOCKED_DECISIONS.md` | `2ebccb18` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/INDEX.md` | `50856a88` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/_SECTION_N.md` | `301e1f9b` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/DOA_BRIEF_F-TMP-002.md` | `cbf2a521` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/DOCCFG_BRIEF_F-TMP-002.md` | `d17fe60e` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/IVMJ.doa.yaml` | `334c75dd` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/IVMJ.doccfg.yaml` | `e9577550` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/IVMJ.mdoc.yaml` | `675b4880` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/IVMJ.ntf.yaml` | `f6055ef8` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/MDOC_BRIEF_IVMJ.md` | `eaa5a975` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/NTF_BRIEF_F-TMP-002.md` | `c17a03a6` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-002.md` | `5440d50b` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `aaa74642` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `9a87aa82` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-002.md` | `cbf2a521` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-002.md` | `d17fe60e` | doccfg_brief |
| `05_Governance/IVMJ.doa.yaml` | `334c75dd` | doa_yaml |
| `05_Governance/IVMJ.doccfg.yaml` | `e9577550` | doccfg_yaml |
| `05_Governance/IVMJ.mdoc.yaml` | `675b4880` | mdoc_yaml |
| `05_Governance/IVMJ.ntf.yaml` | `f6055ef8` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_IVMJ.md` | `eaa5a975` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-002.md` | `c17a03a6` | ntf_brief |
| `05_Governance/decisions.yaml` | `996b2685` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-002.md` | `7f9e28bc` | qa_audit |
| `06_Test/cases.json` | `d47adf8c` | cases_json |
| `06_Test/testcase-F-TMP-002.html` | `6ce933a8` | testcases_uat |
| `06_Test/testcases-F-TMP-002.md` | `ba4110ff` | testcases_ai |
| `07_Print/IVMJ_approved-doa6steps.pdf` | `38375a58` | print_pdf_ivmj_approved_doa6steps |
| `07_Print/IVMJ_approved.pdf` | `9fa73f4f` | print_pdf_ivmj_approved |
| `07_Print/IVMJ_draft.pdf` | `e558b0cc` | print_pdf_ivmj_draft |
| `07_Print/IVMJ_long-12rows-conditional.pdf` | `cd97cbc8` | print_pdf_ivmj_long_12rows_conditional |
| `07_Print/IVMJ_rejected.pdf` | `7dec25a3` | print_pdf_ivmj_rejected |
| `07_Print/IVMJ_states_sheet.png` | `8f1573cd` | print_image_ivmj_states_sheet |
| `07_Print/approved-doa6steps.data.json` | `ef56a313` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `0ab750b4` | print_data_approved_data |
| `07_Print/compare.json` | `b3c7ead2` | report_compare |
| `07_Print/compare_overlay.png` | `67e4306a` | print_image_compare_overlay |
| `07_Print/compare_side.png` | `e5b591c5` | print_image_compare_side |
| `07_Print/draft.data.json` | `177531e7` | print_data_draft_data |
| `07_Print/form.tpl.html` | `b41bf4b2` | print_template |
| `07_Print/long-12rows-conditional.data.json` | `3b1868cc` | print_data_long_12rows_conditional_data |
| `07_Print/print_config.json` | `df43c7a9` | print_config |
| `07_Print/profile.json` | `f4499d86` | print_profile |
| `07_Print/rejected.data.json` | `1ea980ab` | print_data_rejected_data |
| `07_Print/แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ_print-spec.md` | `2e43cc55` | print_spec |
| `07_Print/แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ_template.html` | `a2f908cc` | print_extra_template |
| `08_Reference/10. FM-IVM-10แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ.xlsx` | `0b794de1` | original_10_fm_ivm_10 |
| `08_Reference/FORM_SPEC.check.json` | `9b9cd3a2` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `667bc912` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-002.html` | `46088627` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-002_v2.md` | `54e67220` | prebrief |
| `08_Reference/RUN_LOG.md` | `3917a480` | run_log |
| `08_Reference/SAMPLE.pdf` | `bfb6b4d1` | original_sample |
| `08_Reference/page-1.png` | `977f7883` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `301e1f9b` | report_frd_lint |
| `08_Reference/reports/anchors.json` | `21b9a45e` | report_anchors |
| `08_Reference/reports/e2e_report.json` | `2e2e5eee` | report_e2e |
| `08_Reference/screen_list.png` | `94021d67` | original_screen_list |
| `08_Reference/screen_pdf.png` | `0f97b208` | original_screen_pdf |
| `08_Reference/screen_sign.png` | `33284465` | original_screen_sign |
| `08_Reference/screen_view.png` | `8d0ba136` | original_screen_view |
| `08_Reference/screen_wiz.png` | `7e162a83` | original_screen_wiz |
