# F-FIN-ACL DevPack — ใบเคลียร์เงินทดรองจ่าย (REQ-2569-0000)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 0
- มติ 15 ข้อ (AI-DEFAULT 9) · พร้อมเริ่มทำ
- test case AI 60 เคส
- e2e_standard 21/21
- frd_lint BLOCK 0
- anchor ที่ไม่พบบนจอ 0
- เทียบต้นฉบับ PASS 0.66

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
| `06_Test` | test case AI + UAT ฉบับคน + QA audit | 5 |
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 20 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 16 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT · Strike · ก่อน UAT
- OQ-03 · role id ตรง master DOA · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · ExpensePolicy.advance_clear_due_day · Company.bank_accounts มีหรือยัง · พี่เบิร์ด · ก่อน dev
- OQ-05 · FM-FIN-01 + กันเคลียร์ซ้ำ · Strike · –
- OQ-06 · รหัส ACL ชนไหม · taxonomy function_code · Strike · ก่อน register
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 3 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "ภายในวันที่ 5 ของเดือนถัดไป" → ExpensePolicy.advance_cl
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายละเอียดค่าใช้จ่าย: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 10 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ) · แก้ป้าย 'ผ่าย/แผนก' → 'ฝ่าย/แ
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, role-finance-offi
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส ACL
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `b1485d21` | prototype |
| `02_BRD/BRD_F-FIN-ACL.docx` | `6f763884` | brd_docx |
| `02_BRD/BRD_F-FIN-ACL.md` | `b9b01270` | brd |
| `03_FRD/FRD_F-FIN-ACL_Pack/00_OVERVIEW.md` | `b76108c3` | frd_pack |
| `03_FRD/FRD_F-FIN-ACL_Pack/01_UI.md` | `3a967066` | frd_pack |
| `03_FRD/FRD_F-FIN-ACL_Pack/02_API.md` | `39e4063c` | frd_pack |
| `03_FRD/FRD_F-FIN-ACL_Pack/03_LOGIC.md` | `4fce5b14` | frd_pack |
| `03_FRD/FRD_F-FIN-ACL_Pack/04_DB.md` | `9323ccf0` | frd_pack |
| `03_FRD/FRD_F-FIN-ACL_Pack/05_RULES.md` | `3809904a` | frd_pack |
| `03_FRD/FRD_F-FIN-ACL_Pack/06_TESTS.md` | `7a3a440b` | frd_pack |
| `03_FRD/FRD_F-FIN-ACL_Pack/07_LOCKED_DECISIONS.md` | `fcbc2aa8` | frd_pack |
| `03_FRD/FRD_F-FIN-ACL_Pack/INDEX.md` | `fd221c70` | frd_pack |
| `03_FRD/FRD_F-FIN-ACL_Pack/_SECTION_N.md` | `caad042e` | frd_pack |
| `03_FRD/FRD_F-FIN-ACL_Pack/declarations/ACL.doa.yaml` | `5ae1e700` | frd_pack |
| `03_FRD/FRD_F-FIN-ACL_Pack/declarations/ACL.doccfg.yaml` | `f1b6d3e0` | frd_pack |
| `03_FRD/FRD_F-FIN-ACL_Pack/declarations/ACL.mdoc.yaml` | `4995d0b4` | frd_pack |
| `03_FRD/FRD_F-FIN-ACL_Pack/declarations/ACL.ntf.yaml` | `2d3c535b` | frd_pack |
| `03_FRD/FRD_F-FIN-ACL_Pack/declarations/DOA_BRIEF_F-FIN-ACL.md` | `21e3a70c` | frd_pack |
| `03_FRD/FRD_F-FIN-ACL_Pack/declarations/DOCCFG_BRIEF_F-FIN-ACL.md` | `57d1d902` | frd_pack |
| `03_FRD/FRD_F-FIN-ACL_Pack/declarations/MDOC_BRIEF_ACL.md` | `e64c8a02` | frd_pack |
| `03_FRD/FRD_F-FIN-ACL_Pack/declarations/NTF_BRIEF_F-FIN-ACL.md` | `f2521b61` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-FIN-ACL.md` | `540830fd` | ui_brief |
| `05_Governance/ACL.doa.yaml` | `5ae1e700` | doa_yaml |
| `05_Governance/ACL.doccfg.yaml` | `f1b6d3e0` | doccfg_yaml |
| `05_Governance/ACL.mdoc.yaml` | `4995d0b4` | mdoc_yaml |
| `05_Governance/ACL.ntf.yaml` | `2d3c535b` | ntf_yaml |
| `05_Governance/DECISIONS.lock.json` | `4425f1d5` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `007c401a` | decisions_md |
| `05_Governance/DOA_BRIEF_F-FIN-ACL.md` | `21e3a70c` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-FIN-ACL.md` | `57d1d902` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_ACL.md` | `e64c8a02` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-FIN-ACL.md` | `f2521b61` | ntf_brief |
| `05_Governance/decisions.yaml` | `d0ab447d` | decisions_yaml |
| `06_Test/QA_AUDIT_F-FIN-ACL.md` | `c4f77c10` | qa_audit |
| `06_Test/cases.json` | `023b8063` | cases_json |
| `06_Test/shot-spec.json` | `3a7c9706` | shot_spec |
| `06_Test/testcase-F-FIN-ACL.html` | `1a35dfba` | testcases_uat |
| `06_Test/testcases-F-FIN-ACL.md` | `a4f14ee8` | testcases_ai |
| `07_Print/ACL_approved-6steps.pdf` | `56d84f8a` | print_pdf_acl_approved_6steps |
| `07_Print/ACL_approved.pdf` | `96972874` | print_pdf_acl_approved |
| `07_Print/ACL_draft.pdf` | `a4318a52` | print_pdf_acl_draft |
| `07_Print/ACL_long-14rows-overspent.pdf` | `c1087a06` | print_pdf_acl_long_14rows_overspent |
| `07_Print/ACL_print-spec.md` | `7d77a1f5` | print_spec |
| `07_Print/ACL_rejected.pdf` | `76ebc79b` | print_pdf_acl_rejected |
| `07_Print/ACL_states_sheet.png` | `438e4280` | print_image_acl_states_sheet |
| `07_Print/ACL_template.html` | `18fbe148` | print_extra_acl_template |
| `07_Print/approved-6steps.data.json` | `e49a0efc` | print_data_approved_6steps_data |
| `07_Print/approved.data.json` | `daef2595` | print_data_approved_data |
| `07_Print/base_form_patch.css` | `de4a0c55` | print_extra_base_form_patch |
| `07_Print/compare.json` | `649bbbe1` | report_compare |
| `07_Print/compare_overlay.png` | `609b5f9c` | print_image_compare_overlay |
| `07_Print/compare_side.png` | `7b4c830b` | print_image_compare_side |
| `07_Print/draft.data.json` | `a8b954c9` | print_data_draft_data |
| `07_Print/form.tpl.html` | `99f4b403` | print_template |
| `07_Print/long-14rows-overspent.data.json` | `3b41e29a` | print_data_long_14rows_overspent_data |
| `07_Print/print_config.json` | `2f295707` | print_config |
| `07_Print/profile.json` | `ce670887` | print_profile |
| `07_Print/rejected.data.json` | `7c0b4b88` | print_data_rejected_data |
| `08_Reference/FM-FIN-02.xlsx` | `36b85e86` | original_fm_fin_02 |
| `08_Reference/FORM_SPEC.check.json` | `ac44b9a3` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `05779237` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-2569-0000.html` | `8fa2a6d2` | impact_summary |
| `08_Reference/PREBRIEF_REQ-2569-0000_v2.md` | `ad0465bd` | prebrief |
| `08_Reference/RUN_LOG.md` | `81d950f3` | run_log |
| `08_Reference/img-000.jpg` | `8d1c2ab7` | original_img_000 |
| `08_Reference/img-001.png` | `efc057cc` | original_img_001 |
| `08_Reference/logo_flat.png` | `3abaa0d8` | original_logo_flat |
| `08_Reference/page-1.png` | `03d84828` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `caad042e` | report_frd_lint |
| `08_Reference/reports/anchors.json` | `6f2515b2` | report_anchors |
| `08_Reference/reports/e2e_report.json` | `d601b988` | report_e2e |
| `08_Reference/shot_list.png` | `372845fb` | original_shot_list |
| `08_Reference/shot_uat.png` | `ee4c2028` | original_shot_uat |
| `08_Reference/shot_wizard.png` | `c491c562` | original_shot_wizard |
