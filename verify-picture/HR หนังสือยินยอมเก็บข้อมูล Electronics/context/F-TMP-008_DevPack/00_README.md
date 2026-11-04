# F-TMP-008 DevPack — หนังสือยินยอมในการเก็บรวบรวม ใช้ และเปิดเผยข้อมูลส่วนบุคคล (REQ-TMP-008)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 15 ข้อ (AI-DEFAULT 10) · พร้อมเริ่มทำ
- test case AI 27 เคส
- ไม่มี report e2e_standard (html-generator v9.2 #111)
- frd_lint BLOCK 0
- anchor ที่ไม่พบบนจอ 0

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
| `02_BRD` | BRD | 1 |
| `03_FRD` | FRD Pack | 9 |
| `04_UI_Brief` | UI Brief AS-BUILT | 1 |
| `05_Governance` | มติ (DECISIONS) + ใบประกาศ DOCCFG / DOA / MDOC / NTF | 11 |
| `06_Test` | test case AI + UAT ฉบับคน + QA audit | 4 |
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 10 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 11 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่มีการอนุมัติ
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "บริษัท ครีเดนซ์ จำกัด (มหาชน)" → Organization.legal_nam
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง  · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ)
- DEC-08 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-09 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส PDC
- DEC-10 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `145da600` | prototype |
| `02_BRD/BRD_F-TMP-008.md` | `43742eda` | brd |
| `03_FRD/FRD_F-TMP-008_Pack/00_OVERVIEW.md` | `f4da489e` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/01_UI.md` | `b0af5d4e` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/02_API.md` | `4fa6097b` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/03_LOGIC.md` | `471e7d81` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/04_DB.md` | `9f504156` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/05_RULES.md` | `5feb01b8` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/06_TESTS.md` | `23c80eea` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/07_LOCKED_DECISIONS.md` | `71543a7e` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/INDEX.md` | `6a7236b4` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-008.md` | `202ced21` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `de4879c6` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `77ac7577` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-008.md` | `e5ca3c47` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-008.md` | `a1045d35` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_PDC.md` | `79d06a8f` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-008.md` | `c0579084` | ntf_brief |
| `05_Governance/PDC.doa.yaml` | `439963c4` | doa_yaml |
| `05_Governance/PDC.doccfg.yaml` | `f4bfc367` | doccfg_yaml |
| `05_Governance/PDC.mdoc.yaml` | `6000b8c5` | mdoc_yaml |
| `05_Governance/PDC.ntf.yaml` | `62aa9010` | ntf_yaml |
| `05_Governance/decisions.yaml` | `93106f9e` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-008.md` | `91a0b767` | qa_audit |
| `06_Test/cases.json` | `8a15a8ac` | cases_json |
| `06_Test/testcase-F-TMP-008.html` | `4fca09b9` | testcases_uat |
| `06_Test/testcases-F-TMP-008.md` | `5ed4ce9d` | testcases_ai |
| `07_Print/PDC_print-spec.md` | `e641cbeb` | print_spec |
| `07_Print/PDC_template.html` | `aba791a6` | print_extra_pdc_template |
| `07_Print/approved-doa6steps.data.json` | `cbec670e` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `11a824b2` | print_data_approved_data |
| `07_Print/draft.data.json` | `026230cc` | print_data_draft_data |
| `07_Print/form.tpl.html` | `f56b7b57` | print_template |
| `07_Print/long-withdrawn.data.json` | `d44a8ec3` | print_data_long_withdrawn_data |
| `07_Print/print_config.json` | `444de105` | print_config |
| `07_Print/profile.json` | `48190d1a` | print_profile |
| `07_Print/rejected.data.json` | `f7e3ec04` | print_data_rejected_data |
| `08_Reference/FORM_SPEC.check.json` | `9a2552a4` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `e22847b2` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-008.html` | `7cca80ed` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-008_v2.md` | `ddb0dcb5` | prebrief |
| `08_Reference/RUN_LOG.md` | `47e63058` | run_log |
| `08_Reference/SAMPLE.pdf` | `c7fd24cc` | original_sample |
| `08_Reference/page-1.png` | `2b6fb843` | original_page_1 |
| `08_Reference/page-2.png` | `0358f56e` | original_page_2 |
| `08_Reference/reports/_SECTION_N.md` | `4aab9009` | report_frd_lint |
| `08_Reference/reports/anchors.json` | `8edd08ff` | report_anchors |
| `08_Reference/หนังสือยินยอม PDPA กรณีสมัครงาน.docx` | `ffa8a9d6` | original_pdpa |
