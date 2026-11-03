# F-TMP-010 DevPack — หนังสือให้ความยินยอมในการบันทึกและเผยแพร่ภาพถ่าย หรือภาพเคลื่อนไหว (REQ-TMP-010)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 17 ข้อ (AI-DEFAULT 10) · พร้อมเริ่มทำ
- test case AI 32 เคส
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
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "อายุต่ำกว่า 20 ปี" → PdpaPolicy.minor_age_threshold, "บ
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-09 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส IMC
- DEC-10 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `9ccdfe4d` | prototype |
| `02_BRD/BRD_F-TMP-010.md` | `4aa0d28b` | brd |
| `03_FRD/FRD_F-TMP-010_Pack/00_OVERVIEW.md` | `6de4cd2d` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/01_UI.md` | `332486d8` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/02_API.md` | `341b6f6f` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/03_LOGIC.md` | `e9a0b9a7` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/04_DB.md` | `f54c97e3` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/05_RULES.md` | `d112a5be` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/06_TESTS.md` | `ba4cfae0` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/07_LOCKED_DECISIONS.md` | `bb382ef8` | frd_pack |
| `03_FRD/FRD_F-TMP-010_Pack/INDEX.md` | `ff5d4b00` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-010.md` | `8e889b69` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `fe6a4f75` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `468893c5` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-010.md` | `5d725a54` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-010.md` | `b68ec781` | doccfg_brief |
| `05_Governance/IMC.doa.yaml` | `a6072a8f` | doa_yaml |
| `05_Governance/IMC.doccfg.yaml` | `66d6fd43` | doccfg_yaml |
| `05_Governance/IMC.mdoc.yaml` | `e2c6f094` | mdoc_yaml |
| `05_Governance/IMC.ntf.yaml` | `83f04c62` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_IMC.md` | `270e644e` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-010.md` | `d998965c` | ntf_brief |
| `05_Governance/decisions.yaml` | `c5814721` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-010.md` | `7223211a` | qa_audit |
| `06_Test/cases.json` | `636705f8` | cases_json |
| `06_Test/testcase-F-TMP-010.html` | `67db733c` | testcases_uat |
| `06_Test/testcases-F-TMP-010.md` | `e2c8aeab` | testcases_ai |
| `07_Print/IMC_print-spec.md` | `e41f1859` | print_spec |
| `07_Print/IMC_template.html` | `fccc21d6` | print_extra_imc_template |
| `07_Print/approved-doa6steps.data.json` | `b1dda784` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `2f49db7c` | print_data_approved_data |
| `07_Print/draft.data.json` | `c044ce74` | print_data_draft_data |
| `07_Print/form.tpl.html` | `c4b31487` | print_template |
| `07_Print/long-withdrawn.data.json` | `876060b7` | print_data_long_withdrawn_data |
| `07_Print/print_config.json` | `37225a2d` | print_config |
| `07_Print/profile.json` | `b049b253` | print_profile |
| `07_Print/rejected.data.json` | `924d2698` | print_data_rejected_data |
| `08_Reference/FORM_SPEC.check.json` | `4b4eabd3` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `9306b98e` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-010.html` | `cc15e776` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-010_v2.md` | `7d744935` | prebrief |
| `08_Reference/RUN_LOG.md` | `a8902620` | run_log |
| `08_Reference/SAMPLE.pdf` | `944a3d39` | original_sample |
| `08_Reference/page-1.png` | `cf72250f` | original_page_1 |
| `08_Reference/page-2.png` | `e7ef6ed4` | original_page_2 |
| `08_Reference/reports/_SECTION_N.md` | `a6f3608a` | report_frd_lint |
| `08_Reference/reports/anchors.json` | `034a7514` | report_anchors |
| `08_Reference/หนังสือให้ความยินยอมบันทึกภาพเคลื่อนไหว.docx` | `0a35c04c` | original_ |
