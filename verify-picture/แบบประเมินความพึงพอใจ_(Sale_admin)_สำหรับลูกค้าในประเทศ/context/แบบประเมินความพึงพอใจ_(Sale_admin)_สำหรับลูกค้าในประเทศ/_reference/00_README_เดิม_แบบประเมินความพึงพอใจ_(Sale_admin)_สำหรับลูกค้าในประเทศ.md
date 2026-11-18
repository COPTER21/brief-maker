# F-TMP-004 DevPack — แบบประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าในประเทศ (REQ-TMP-004)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 13 ข้อ (AI-DEFAULT 10) · พร้อมเริ่มทำ
- test case AI 30 เคส
- e2e_standard 21/21
- frd_lint BLOCK 0
- เทียบต้นฉบับ WARN 0.445

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K9 — เทียบต้นฉบับ WARN 0.445

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
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ทุกข้อเลือกระดับความพึงพอใ
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นตามตำแหน่งกระดาษ  · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ)
- DEC-08 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติ none · admin role เห็นทั้งหมด
- DEC-09 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส SDA
- DEC-10 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `4da7b2cc` | prototype |
| `02_BRD/BRD_F-TMP-004.docx` | `71a6905a` | brd_docx |
| `02_BRD/BRD_F-TMP-004.md` | `18f72a12` | brd |
| `03_FRD/FRD_F-TMP-004_Pack/00_OVERVIEW.md` | `8e16df59` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/01_UI.md` | `23f46cde` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/02_API.md` | `18b2044e` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/03_LOGIC.md` | `d83eb86f` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/04_DB.md` | `7ff15fa8` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/05_RULES.md` | `625ba7a1` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/06_TESTS.md` | `9b968472` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/07_LOCKED_DECISIONS.md` | `e3d87bff` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/INDEX.md` | `e871fead` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/_SECTION_N.md` | `b001b6ba` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/DOCCFG_BRIEF_F-TMP-004.md` | `d71d19e3` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/MDOC_BRIEF_SDA.md` | `2e50d5e5` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/NTF_BRIEF_F-TMP-004.md` | `a524754d` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/SDA.doccfg.yaml` | `5e70b28d` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/SDA.mdoc.yaml` | `fd047131` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/SDA.ntf.yaml` | `5409dcd7` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-004.md` | `a182b69a` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `03128d23` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `287f36da` | decisions_md |
| `05_Governance/DOCCFG_BRIEF_F-TMP-004.md` | `d71d19e3` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_SDA.md` | `2e50d5e5` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-004.md` | `a524754d` | ntf_brief |
| `05_Governance/SDA.doccfg.yaml` | `5e70b28d` | doccfg_yaml |
| `05_Governance/SDA.mdoc.yaml` | `fd047131` | mdoc_yaml |
| `05_Governance/SDA.ntf.yaml` | `5409dcd7` | ntf_yaml |
| `05_Governance/decisions.yaml` | `e95c77c5` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-004.md` | `f739167a` | qa_audit |
| `06_Test/cases.json` | `15586b1e` | cases_json |
| `06_Test/testcase-F-TMP-004.html` | `d06a9135` | testcases_uat |
| `06_Test/testcases-F-TMP-004.md` | `5ecb3121` | testcases_ai |
| `07_Print/SDA_print-spec.md` | `e8770284` | print_spec |
| `07_Print/_states_sheet.png` | `c2235b0b` | print_image_states_sheet |
| `07_Print/cancelled.data.json` | `a4c8f4fd` | print_data_cancelled_data |
| `07_Print/compare.json` | `36e8d769` | report_compare |
| `07_Print/compare_side.png` | `ffbcf9dc` | print_image_compare_side |
| `07_Print/draft.data.json` | `db6159b8` | print_data_draft_data |
| `07_Print/form.tpl.html` | `a5becbca` | print_template |
| `07_Print/long-comments.data.json` | `1bc7b309` | print_data_long_comments_data |
| `07_Print/low-score.data.json` | `e12eb4c7` | print_data_low_score_data |
| `07_Print/print_config.json` | `6a72fd6a` | print_config |
| `07_Print/profile.json` | `d678b27c` | print_profile |
| `07_Print/recorded.data.json` | `9b4d4832` | print_data_recorded_data |
| `07_Print/แบบประเมินความพึงพอใจ_SaleAdmin_ในประเทศ_template.html` | `933fd54b` | print_extra_saleadmin_template |
| `08_Reference/20. FM-SAL-20 แบบประเมินความพึงพอใจ ในประเทศ (Sale admin).docx` | `6946edbf` | original_20_fm_sal_20_sale_admin |
| `08_Reference/FORM_SPEC.check.json` | `c7cf237f` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `38d5e211` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-004.html` | `2b715c58` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-004_v2.md` | `78912ac2` | prebrief |
| `08_Reference/RUN_LOG.md` | `9aec45fa` | run_log |
| `08_Reference/SAMPLE.pdf` | `1eaab3a1` | original_sample |
| `08_Reference/page-1.png` | `f13384e0` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `b001b6ba` | report_frd_lint |
| `08_Reference/reports/e2e_container_ref.json` | `1e1fb1e8` | report_e2e |
| `08_Reference/shot_list.png` | `9e610a21` | original_shot_list |
| `08_Reference/shot_pdf.png` | `db513d50` | original_shot_pdf |
| `08_Reference/shot_wizard.png` | `1e1bd11a` | original_shot_wizard |
