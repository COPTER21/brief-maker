# F-TMP-001 DevPack — แบบประเมินความพึงพอใจลูกค้า (REQ-TMP-001)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 13 ข้อ (AI-DEFAULT 10) · พร้อมเริ่มทำ
- test case AI 52 เคส
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
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 11 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 9 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (ไม่มีสายพิจารณา · สิทธิ์ยกเลิก · ผจก.ขายเห็นทุกใบ) · ทีม BA · ก่อน UAT
- OQ-03 · รหัสชั่วคราว F-TMP-001 / REQ-TMP-001 → เลขจริง · function_code taxonomy · ทีม BA · ก่อน register
- OQ-04 · ผู้ประเมิน = ผู้บันทึกในระบบ หรือให้ร้านค้าตอบเอง · ลูกค้า · ก่อน UAT
- OQ-05 · ชื่อบริษัทที่ถูกต้อง (จำกัด / จำกัด (มหาชน)) — ระบบอ่าน Organization · ลูกค้า · –
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่มีการอนุมัติ
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ชื่อบริษัทในหัวเรื่องและข้
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-09 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส CSE
- DEC-10 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `9eab0670` | prototype |
| `02_BRD/BRD_F-TMP-001.docx` | `3b9d403b` | brd_docx |
| `02_BRD/BRD_F-TMP-001.md` | `6214e020` | brd |
| `03_FRD/FRD_F-TMP-001_Pack/00_OVERVIEW.md` | `f81f21e0` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/01_UI.md` | `a139d8ca` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/02_API.md` | `0ff4531e` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/03_LOGIC.md` | `1ed8d470` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/04_DB.md` | `4c4288d8` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/05_RULES.md` | `a2f15573` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/06_TESTS.md` | `d6934d68` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/07_LOCKED_DECISIONS.md` | `0d55f112` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/INDEX.md` | `1c6437d1` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/_SECTION_N.md` | `13f0b6f5` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/CSE.doccfg.yaml` | `727fd3b3` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/CSE.mdoc.yaml` | `9f086521` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/CSE.ntf.yaml` | `52cfca87` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/DOCCFG_BRIEF_F-TMP-001.md` | `ed2ef63d` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/MDOC_BRIEF_CSE.md` | `6902682a` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/NTF_BRIEF_F-TMP-001.md` | `7a9e94fb` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-001.md` | `b45fc0a4` | ui_brief |
| `05_Governance/CSE.doccfg.yaml` | `727fd3b3` | doccfg_yaml |
| `05_Governance/CSE.mdoc.yaml` | `9f086521` | mdoc_yaml |
| `05_Governance/CSE.ntf.yaml` | `52cfca87` | ntf_yaml |
| `05_Governance/DECISIONS.lock.json` | `521cae01` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `f154f326` | decisions_md |
| `05_Governance/DOCCFG_BRIEF_F-TMP-001.md` | `ed2ef63d` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_CSE.md` | `6902682a` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-001.md` | `7a9e94fb` | ntf_brief |
| `05_Governance/decisions.yaml` | `76e6b700` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-001.md` | `27292759` | qa_audit |
| `06_Test/cases.json` | `f7061edf` | cases_json |
| `06_Test/testcase-F-TMP-001.html` | `3e094cf2` | testcases_uat |
| `06_Test/testcases-F-TMP-001.md` | `71688d55` | testcases_ai |
| `07_Print/CSE_print-spec.md` | `31ae5d25` | print_spec |
| `07_Print/CSE_template.html` | `5b38405c` | print_extra_cse_template |
| `07_Print/alt-choices-low.data.json` | `d11fb6a5` | print_data_alt_choices_low_data |
| `07_Print/blank-print.data.json` | `e996835b` | print_data_blank_print_data |
| `07_Print/draft.data.json` | `a95c9277` | print_data_draft_data |
| `07_Print/form.tpl.html` | `cb592ed5` | print_template |
| `07_Print/long-suggestion.data.json` | `d4822429` | print_data_long_suggestion_data |
| `07_Print/print_config.json` | `5f35c97d` | print_config |
| `07_Print/profile.json` | `83731434` | print_profile |
| `07_Print/render_data.py` | `035c826e` | print_extra_render_data |
| `07_Print/submitted.data.json` | `44f07ec1` | print_data_submitted_data |
| `08_Reference/FORM_SPEC.check.json` | `6dccd1aa` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `e7707d52` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-001.html` | `092cf50c` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-001_v2.md` | `42e173f7` | prebrief |
| `08_Reference/RUN_LOG.md` | `3bddac25` | run_log |
| `08_Reference/SAMPLE.pdf` | `4da52d0e` | original_sample |
| `08_Reference/page-1.png` | `1d8e310f` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `13f0b6f5` | report_frd_lint |
| `08_Reference/แบบประเมินความพึงพอใจลูกค้า.docx` | `724f2d08` | original_ |
