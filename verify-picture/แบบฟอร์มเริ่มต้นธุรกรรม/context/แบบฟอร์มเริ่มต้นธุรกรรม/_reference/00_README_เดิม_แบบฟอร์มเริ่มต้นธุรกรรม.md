# F-TMP-001 DevPack — แบบฟอร์มเริ่มต้นธุรกรรม (REQ-TMP-001)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 14 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 29 เคส
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
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT · Strike · ก่อน UAT
- OQ-03 · role ผู้ตรวจสอบ/ผู้อนุมัติ + admin_role ไม่มีตรงใน DOA roles master · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · module บริหารการลงทุน + feature id จริง (ใช้ F-TMP-001 / finance ชั่วคราว) · พี่เบิร์ด · ก่อน dev
- OQ-05 · ประเภทธุรกรรม/แหล่งที่มา เป็น master ไหม · ลูกค้า · –
- OQ-06 · รหัส IVMA ชนไหม · taxonomy function_code · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ประวัติการแก้ไข: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 2 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส IVMA
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `f1017897` | prototype |
| `02_BRD/BRD_F-TMP-001.docx` | `c63ea90e` | brd_docx |
| `02_BRD/BRD_F-TMP-001.md` | `c34ad405` | brd |
| `03_FRD/FRD_F-TMP-001_Pack/00_OVERVIEW.md` | `b3d6aa0a` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/01_UI.md` | `a58dd41c` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/02_API.md` | `748a8bdd` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/03_LOGIC.md` | `1661fc1e` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/04_DB.md` | `30b0634f` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/05_RULES.md` | `19d5473b` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/06_TESTS.md` | `2d43c3bc` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/07_LOCKED_DECISIONS.md` | `d507a59f` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/INDEX.md` | `1f5b702c` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/_SECTION_N.md` | `21192d80` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/DOA_BRIEF_F-TMP-001.md` | `e998b442` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/DOCCFG_BRIEF_F-TMP-001.md` | `78b72777` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/IVMA.doa.yaml` | `a547e145` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/IVMA.doccfg.yaml` | `4bd52d1c` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/IVMA.mdoc.yaml` | `894139d1` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/IVMA.ntf.yaml` | `5cf3506e` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/MDOC_BRIEF_IVMA.md` | `74531254` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/NTF_BRIEF_F-TMP-001.md` | `846f185e` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-001.md` | `152c59e6` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `0c8680bd` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `b758bc6f` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-001.md` | `e998b442` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-001.md` | `78b72777` | doccfg_brief |
| `05_Governance/IVMA.doa.yaml` | `a547e145` | doa_yaml |
| `05_Governance/IVMA.doccfg.yaml` | `4bd52d1c` | doccfg_yaml |
| `05_Governance/IVMA.mdoc.yaml` | `894139d1` | mdoc_yaml |
| `05_Governance/IVMA.ntf.yaml` | `5cf3506e` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_IVMA.md` | `74531254` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-001.md` | `846f185e` | ntf_brief |
| `05_Governance/decisions.yaml` | `a52b4e19` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-001.md` | `33f8bd68` | qa_audit |
| `06_Test/cases.json` | `43b3d486` | cases_json |
| `06_Test/testcase-F-TMP-001.html` | `3cc29fd6` | testcases_uat |
| `06_Test/testcases-F-TMP-001.md` | `7f2ae4c7` | testcases_ai |
| `07_Print/approved-doa6steps.data.json` | `7b30f69b` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `05e2f3a0` | print_data_approved_data |
| `07_Print/draft.data.json` | `8f154094` | print_data_draft_data |
| `07_Print/form.tpl.html` | `90260f9d` | print_template |
| `07_Print/long-12revisions.data.json` | `1edfb767` | print_data_long_12revisions_data |
| `07_Print/print_config.json` | `81d31702` | print_config |
| `07_Print/profile.json` | `a0ea94b0` | print_profile |
| `07_Print/rejected.data.json` | `213ae39d` | print_data_rejected_data |
| `07_Print/แบบฟอร์มเริ่มต้นธุรกรรม_print-spec.md` | `0d407f20` | print_spec |
| `07_Print/แบบฟอร์มเริ่มต้นธุรกรรม_template.html` | `6b5829de` | print_extra_template |
| `08_Reference/1. FM-IVM-01 แบบฟอร์มเริ่มต้นธุรกรรม.xlsx` | `f6c5ab5a` | original_1_fm_ivm_01 |
| `08_Reference/FORM_SPEC.check.json` | `cfd846a3` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `d0b57eeb` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-001.html` | `062eb9fb` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-001_v2.md` | `4b354b3f` | prebrief |
| `08_Reference/RUN_LOG.md` | `288b48d8` | run_log |
| `08_Reference/SAMPLE.pdf` | `7fd5a0bc` | original_sample |
| `08_Reference/page-1.png` | `777bb40d` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `21192d80` | report_frd_lint |
