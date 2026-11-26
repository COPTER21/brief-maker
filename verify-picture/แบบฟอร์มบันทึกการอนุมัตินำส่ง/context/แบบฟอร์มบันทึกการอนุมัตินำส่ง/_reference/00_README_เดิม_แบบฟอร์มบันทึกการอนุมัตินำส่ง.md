# F-TMP-010 DevPack — แบบฟอร์มบันทึกการอนุมัตินำส่ง (REQ-TMP-010)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 18 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 42 เคส
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
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 3 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ระดับอำนาจอนุมัติ เลือกจาก
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ผลการพิจารณา: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 3 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส IVMH
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `576e2591` | prototype |
| `02_BRD/BRD_F-TMP-010.docx` | `deb72d17` | brd_docx |
| `02_BRD/BRD_F-TMP-010.md` | `21bfc896` | brd |
| `03_FRD/FRD_F-TMP-010_Pack/00_OVERVIEW.md` | `ba3ca645` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/01_UI.md` | `5957836f` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/02_API.md` | `9661e0fe` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/03_LOGIC.md` | `9848d09e` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/04_DB.md` | `5763f3d0` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/05_RULES.md` | `5f50e9a3` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/06_TESTS.md` | `b73afb9a` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/07_LOCKED_DECISIONS.md` | `d459e185` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/INDEX.md` | `2d91dcef` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/_SECTION_N.md` | `63a9d73a` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/declarations/DOA_BRIEF_F-TMP-010.md` | `ba8866e9` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/declarations/DOCCFG_BRIEF_F-TMP-010.md` | `031ffdee` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/declarations/IVMH.doa.yaml` | `bcadde70` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/declarations/IVMH.doccfg.yaml` | `2faf56b4` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/declarations/IVMH.mdoc.yaml` | `181466d0` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/declarations/IVMH.ntf.yaml` | `0b23f3da` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/declarations/MDOC_BRIEF_IVMH.md` | `406a49ad` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/declarations/NTF_BRIEF_F-TMP-010.md` | `acafee94` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-010.md` | `f74a5332` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `1058364f` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `54713e1d` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-010.md` | `ba8866e9` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-010.md` | `031ffdee` | doccfg_brief |
| `05_Governance/IVMH.doa.yaml` | `bcadde70` | doa_yaml |
| `05_Governance/IVMH.doccfg.yaml` | `2faf56b4` | doccfg_yaml |
| `05_Governance/IVMH.mdoc.yaml` | `181466d0` | mdoc_yaml |
| `05_Governance/IVMH.ntf.yaml` | `0b23f3da` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_IVMH.md` | `406a49ad` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-010.md` | `acafee94` | ntf_brief |
| `05_Governance/decisions.yaml` | `6540202a` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-010.md` | `d38630d7` | qa_audit |
| `06_Test/cases.json` | `3ea8d231` | cases_json |
| `06_Test/testcase-F-TMP-010.html` | `24cac5b0` | testcases_uat |
| `06_Test/testcases-F-TMP-010.md` | `fc23c073` | testcases_ai |
| `07_Print/R1.data.json` | `16205810` | print_data_r1_data |
| `07_Print/approved-doa6steps.data.json` | `6dae5e3b` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `bc374d66` | print_data_approved_data |
| `07_Print/draft.data.json` | `05a27998` | print_data_draft_data |
| `07_Print/form.tpl.html` | `852edb37` | print_template |
| `07_Print/long-text.data.json` | `babaee49` | print_data_long_text_data |
| `07_Print/print_config.json` | `77407b31` | print_config |
| `07_Print/profile.json` | `5ed9036a` | print_profile |
| `07_Print/rejected.data.json` | `439bd09a` | print_data_rejected_data |
| `07_Print/แบบฟอร์มบันทึกการอนุมัตินำส่ง_print-spec.md` | `295ebe52` | print_spec |
| `07_Print/แบบฟอร์มบันทึกการอนุมัตินำส่ง_template.html` | `73b6b099` | print_extra_template |
| `08_Reference/8. FM-IVM-08 แบบฟอร์มบันทึกการอนุมัตินำส่ง.xlsx` | `fd4cd087` | original_8_fm_ivm_08 |
| `08_Reference/FORM_SPEC.check.json` | `3ae28e3c` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `2ecd42d7` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-010.html` | `3ade2450` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-010_v2.md` | `9b64c71b` | prebrief |
| `08_Reference/RUN_LOG.md` | `308c1d7f` | run_log |
| `08_Reference/SAMPLE.pdf` | `abc5c59c` | original_sample |
| `08_Reference/page-1.png` | `2755f572` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `63a9d73a` | report_frd_lint |
