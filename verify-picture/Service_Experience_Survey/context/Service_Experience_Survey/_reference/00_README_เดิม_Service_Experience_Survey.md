# F-TMP-006 DevPack — Service Experience Survey (REQ-TMP-006)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 14 ข้อ (AI-DEFAULT 10) · พร้อมเริ่มทำ
- test case AI 30 เคส
- e2e_standard 21/21
- frd_lint BLOCK 0
- เทียบต้นฉบับ WARN 0.378

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K9 — เทียบต้นฉบับ WARN 0.378

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
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 13 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 13 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่มีการอนุมัติ
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ทุกข้อเลือกคะแนนได้ 1 ค่า 
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นตามตำแหน่งกระดาษ  · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ)
- DEC-08 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติ none · admin role เห็นทั้งหมด
- DEC-09 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส SEA
- DEC-10 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `7d6ed66d` | prototype |
| `02_BRD/BRD_F-TMP-006.docx` | `3bbb49b7` | brd_docx |
| `02_BRD/BRD_F-TMP-006.md` | `061310a3` | brd |
| `03_FRD/FRD_F-TMP-006_Pack/00_OVERVIEW.md` | `4117f992` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/01_UI.md` | `9d3e654f` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/02_API.md` | `e3c52332` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/03_LOGIC.md` | `fda31126` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/04_DB.md` | `f476342f` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/05_RULES.md` | `572c7b2a` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/06_TESTS.md` | `9259a2e5` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/07_LOCKED_DECISIONS.md` | `4f8b0a67` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/INDEX.md` | `6d939c53` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/_SECTION_N.md` | `09aa6c54` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/DOCCFG_BRIEF_F-TMP-006.md` | `0b32beda` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/MDOC_BRIEF_SEA.md` | `2567fd2d` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/NTF_BRIEF_F-TMP-006.md` | `6b9a79ff` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/SEA.doccfg.yaml` | `96c9c142` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/SEA.mdoc.yaml` | `3cc790ae` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/SEA.ntf.yaml` | `ea1cdfcb` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-006.md` | `9b1f863e` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `ecd797b7` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `a228c0ab` | decisions_md |
| `05_Governance/DOCCFG_BRIEF_F-TMP-006.md` | `0b32beda` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_SEA.md` | `2567fd2d` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-006.md` | `6b9a79ff` | ntf_brief |
| `05_Governance/SEA.doccfg.yaml` | `96c9c142` | doccfg_yaml |
| `05_Governance/SEA.mdoc.yaml` | `3cc790ae` | mdoc_yaml |
| `05_Governance/SEA.ntf.yaml` | `ea1cdfcb` | ntf_yaml |
| `05_Governance/decisions.yaml` | `046630fc` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-006.md` | `0aebaea7` | qa_audit |
| `06_Test/cases.json` | `8e19379b` | cases_json |
| `06_Test/testcase-F-TMP-006.html` | `95706da8` | testcases_uat |
| `06_Test/testcases-F-TMP-006.md` | `54a794a0` | testcases_ai |
| `07_Print/SEA_print-spec.md` | `c5b6d7f2` | print_spec |
| `07_Print/Service_Experience_Survey_template.html` | `eba49470` | print_extra_service_experience_survey_template |
| `07_Print/_states_sheet.png` | `72c5cd85` | print_image_states_sheet |
| `07_Print/cancelled.data.json` | `725da7bc` | print_data_cancelled_data |
| `07_Print/compare.json` | `3210612c` | report_compare |
| `07_Print/compare_side.png` | `8487fc08` | print_image_compare_side |
| `07_Print/draft.data.json` | `10562ef3` | print_data_draft_data |
| `07_Print/form.tpl.html` | `f93e89fb` | print_template |
| `07_Print/long-comments.data.json` | `c3390c0e` | print_data_long_comments_data |
| `07_Print/low-score.data.json` | `cfd3ca30` | print_data_low_score_data |
| `07_Print/print_config.json` | `d676c6e6` | print_config |
| `07_Print/profile.json` | `ce68728e` | print_profile |
| `07_Print/recorded.data.json` | `a10aa24a` | print_data_recorded_data |
| `08_Reference/22. FM-SAL-22 แบบประเมินความพึงพอใจ Sales Admin (ต่างประเทศ).docx` | `78b32749` | original_22_fm_sal_22_sales_admin |
| `08_Reference/FORM_SPEC.check.json` | `69bf2436` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `e6ead9d0` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-006.html` | `ecc7f2d2` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-006_v2.md` | `9510f631` | prebrief |
| `08_Reference/RUN_LOG.md` | `3a032fd8` | run_log |
| `08_Reference/SAMPLE.pdf` | `5d382997` | original_sample |
| `08_Reference/page-1.png` | `359289d5` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `09aa6c54` | report_frd_lint |
| `08_Reference/reports/e2e_container_ref.json` | `ac6dc196` | report_e2e |
| `08_Reference/shot_list.png` | `06e742e7` | original_shot_list |
| `08_Reference/shot_pdf.png` | `49067fca` | original_shot_pdf |
| `08_Reference/shot_wizard.png` | `5829a3fe` | original_shot_wizard |
