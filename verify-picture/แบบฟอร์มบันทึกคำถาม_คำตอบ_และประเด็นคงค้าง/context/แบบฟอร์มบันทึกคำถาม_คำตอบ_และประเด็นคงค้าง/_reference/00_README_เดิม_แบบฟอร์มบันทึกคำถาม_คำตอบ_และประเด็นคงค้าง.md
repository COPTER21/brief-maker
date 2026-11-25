# F-TMP-005 DevPack — แบบฟอร์มบันทึกคำถาม คำตอบ และประเด็นคงค้าง (REQ-TMP-005)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 19 ข้อ (AI-DEFAULT 12) · พร้อมเริ่มทำ
- test case AI 40 เคส
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
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · เลขที่คำถาม (Q-001…) และรห
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: บันทึกคำถามและคำตอบ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 14 แถวตามกระดาษ
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการประเด็นคงค้าง: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 14 แถวตามกระดาษ
- DEC-07 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · เพิ่ม: ชื่อโครงการ / ธุรกรรม (F01 · กระดาษไม่มีช่องระบุโครงก
- DEC-08 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-09 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-10 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-11 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส IVMC
- DEC-12 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `11c1be76` | prototype |
| `02_BRD/BRD_F-TMP-005.docx` | `55f47f88` | brd_docx |
| `02_BRD/BRD_F-TMP-005.md` | `a5198953` | brd |
| `03_FRD/FRD_F-TMP-005_Pack/00_OVERVIEW.md` | `e4af2682` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/01_UI.md` | `b4720708` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/02_API.md` | `d52d7540` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/03_LOGIC.md` | `2fad3dea` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/04_DB.md` | `2f24127d` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/05_RULES.md` | `b561b2e7` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/06_TESTS.md` | `03c9b4f2` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/07_LOCKED_DECISIONS.md` | `dfe4e841` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/INDEX.md` | `51357821` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/_SECTION_N.md` | `b68336df` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/DOA_BRIEF_F-TMP-005.md` | `5ed55b8e` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/DOCCFG_BRIEF_F-TMP-005.md` | `44c939cc` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/IVMC.doa.yaml` | `810b1f00` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/IVMC.doccfg.yaml` | `f3d38977` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/IVMC.mdoc.yaml` | `93e28207` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/IVMC.ntf.yaml` | `90bb374b` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/MDOC_BRIEF_IVMC.md` | `a5c93876` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/NTF_BRIEF_F-TMP-005.md` | `9f8f34d9` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-005.md` | `4f40ec3c` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `5f8fc09f` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `3f4bb44b` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-005.md` | `5ed55b8e` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-005.md` | `44c939cc` | doccfg_brief |
| `05_Governance/IVMC.doa.yaml` | `810b1f00` | doa_yaml |
| `05_Governance/IVMC.doccfg.yaml` | `f3d38977` | doccfg_yaml |
| `05_Governance/IVMC.mdoc.yaml` | `93e28207` | mdoc_yaml |
| `05_Governance/IVMC.ntf.yaml` | `90bb374b` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_IVMC.md` | `a5c93876` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-005.md` | `9f8f34d9` | ntf_brief |
| `05_Governance/decisions.yaml` | `547cadcb` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-005.md` | `12c53ad8` | qa_audit |
| `06_Test/cases.json` | `943be187` | cases_json |
| `06_Test/testcase-F-TMP-005.html` | `8fc0bc67` | testcases_uat |
| `06_Test/testcases-F-TMP-005.md` | `e6ca61d7` | testcases_ai |
| `07_Print/R1.data.json` | `59a4a768` | print_data_r1_data |
| `07_Print/approved-doa6steps.data.json` | `134bb241` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `db7cd028` | print_data_approved_data |
| `07_Print/draft.data.json` | `914eb381` | print_data_draft_data |
| `07_Print/form.tpl.html` | `1ae8ae2e` | print_template |
| `07_Print/long-18questions-16issues.data.json` | `5e664223` | print_data_long_18questions_16issues_data |
| `07_Print/print_config.json` | `f6ce614a` | print_config |
| `07_Print/profile.json` | `d31f2ea6` | print_profile |
| `07_Print/rejected.data.json` | `46fc04d3` | print_data_rejected_data |
| `07_Print/แบบฟอร์มบันทึกคำถาม คำตอบ และประเด็นคงค้าง_print-spec.md` | `6bdcccb4` | print_spec |
| `07_Print/แบบฟอร์มบันทึกคำถาม คำตอบ และประเด็นคงค้าง_template.html` | `2d7f46eb` | print_extra_template |
| `08_Reference/3. FM-IVM-03 แบบฟอร์มบันทึกคำถาม คำตอบ และประเด็นคงค้าง.xlsx` | `3d57abb2` | original_3_fm_ivm_03 |
| `08_Reference/FORM_SPEC.check.json` | `adc3c354` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `98698f3e` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-005.html` | `84ca743c` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-005_v2.md` | `5eea9f28` | prebrief |
| `08_Reference/RUN_LOG.md` | `cd5038d8` | run_log |
| `08_Reference/SAMPLE.pdf` | `13cd0c77` | original_sample |
| `08_Reference/page-1.png` | `7914621f` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `b68336df` | report_frd_lint |
