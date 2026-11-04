# F-TMP-002 DevPack — แบบสอบถามบุคลากรที่พ้นจากงาน (Exit Interview) (REQ-TMP-002)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 17 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 58 เคส
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
| `03_FRD` | FRD Pack | 16 |
| `04_UI_Brief` | UI Brief AS-BUILT | 1 |
| `05_Governance` | มติ (DECISIONS) + ใบประกาศ DOCCFG / DOA / MDOC / NTF | 9 |
| `06_Test` | test case AI + UAT ฉบับคน + QA audit | 4 |
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 10 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 14 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ลูกค้ายืนยัน DEC AI-DEFAULT 11 ข้อ (ใบลงนาม) ก่อน UAT
- OQ-02 · ต้องการขั้น "HR รับทราบ" ที่ DOA กลางหรือไม่
- OQ-03 · ตัวชี้วัด
- OQ-04 · function_code Taxonomy ของ EXI (F01 ชั่วคราว)
- OQ-05 · รหัส feature จริง + เลข REQ จริง
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่มีการอนุมัติ
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · อายุตัว = ปีเต็มจาก Employ
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ปัจจัยที่เลือก + หมายเลขลำดับความสำคัญ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 1 แถวตา
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สิ่งที่ควรปรับปรุง: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 5 แถวตามกระดาษ
- DEC-07 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-08 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติ none · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส EXI
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `766e64a0` | prototype |
| `02_BRD/BRD_F-TMP-002.docx` | `18680eee` | brd_docx |
| `02_BRD/BRD_F-TMP-002.md` | `e07b7c9f` | brd |
| `03_FRD/FRD_F-TMP-002_Pack/00_OVERVIEW.md` | `55e5d3c0` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/01_UI.md` | `b471bcfc` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/02_API.md` | `25ac8602` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/03_LOGIC.md` | `fed2d4e4` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/04_DB.md` | `e0ac09d3` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/05_RULES.md` | `596a9a48` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/06_TESTS.md` | `18ee425d` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/07_LOCKED_DECISIONS.md` | `f61f6111` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/INDEX.md` | `fd32b321` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/_SECTION_N.md` | `000ceaef` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/DOCCFG_BRIEF_F-TMP-002.md` | `a2dcfc76` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/EXI.doccfg.yaml` | `8b039d42` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/EXI.mdoc.yaml` | `01ecd00d` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/EXI.ntf.yaml` | `0526a284` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/MDOC_BRIEF_EXI.md` | `b3d8e1f4` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/NTF_BRIEF_F-TMP-002.md` | `a44a5f38` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-002.md` | `bdf09eab` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `7ba357b3` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `614c1f9f` | decisions_md |
| `05_Governance/DOCCFG_BRIEF_F-TMP-002.md` | `a2dcfc76` | doccfg_brief |
| `05_Governance/EXI.doccfg.yaml` | `8b039d42` | doccfg_yaml |
| `05_Governance/EXI.mdoc.yaml` | `01ecd00d` | mdoc_yaml |
| `05_Governance/EXI.ntf.yaml` | `0526a284` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_EXI.md` | `b3d8e1f4` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-002.md` | `a44a5f38` | ntf_brief |
| `05_Governance/decisions.yaml` | `aa0c38b2` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-002.md` | `9418117b` | qa_audit |
| `06_Test/cases.json` | `ef8976f0` | cases_json |
| `06_Test/testcase-F-TMP-002.html` | `165bb5ac` | testcases_uat |
| `06_Test/testcases-F-TMP-002.md` | `d380ac7d` | testcases_ai |
| `07_Print/EXI_print-spec.md` | `6f13d4e1` | print_spec |
| `07_Print/EXI_states_sheet.png` | `7c5f9528` | print_image_exi_states_sheet |
| `07_Print/EXI_template.html` | `b0876b3a` | print_extra_exi_template |
| `07_Print/contract-end.data.json` | `43298d02` | print_data_contract_end_data |
| `07_Print/draft.data.json` | `3d516e98` | print_data_draft_data |
| `07_Print/form.tpl.html` | `2c6b72ec` | print_template |
| `07_Print/long-12rows-allreasons.data.json` | `36c0e917` | print_data_long_12rows_allreasons_data |
| `07_Print/print_config.json` | `ea6f4cdf` | print_config |
| `07_Print/profile.json` | `98df687b` | print_profile |
| `07_Print/submitted.data.json` | `b1c23802` | print_data_submitted_data |
| `08_Reference/FORM_SPEC.check.json` | `5296f4a3` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `aa6f71a5` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-002.html` | `2574495f` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-002_v2.md` | `286c3480` | prebrief |
| `08_Reference/RUN_LOG.md` | `3fd75317` | run_log |
| `08_Reference/SAMPLE.pdf` | `b92dc74b` | original_sample |
| `08_Reference/page-1.png` | `e9836689` | original_page_1 |
| `08_Reference/page-2.png` | `7a117377` | original_page_2 |
| `08_Reference/page-3.png` | `08de473e` | original_page_3 |
| `08_Reference/reports/_SECTION_N.md` | `000ceaef` | report_frd_lint |
| `08_Reference/shot_list_sandbox.png` | `2a098e40` | original_shot_list_sandbox |
| `08_Reference/shot_view_pdf_sandbox.png` | `f8064e75` | original_shot_view_pdf_sandbox |
| `08_Reference/shot_wizard_sandbox.png` | `45b0fdf6` | original_shot_wizard_sandbox |
| `08_Reference/แบบฟอร์ม Exit Interview.docx` | `bed21687` | original_exit_interview |
