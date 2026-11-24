# F-TMP-005 DevPack — รายงานความคืบหน้าโครงการ (REQ-TMP-005)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 20 ข้อ (AI-DEFAULT 15) · พร้อมเริ่มทำ
- test case AI 61 เคส
- e2e_standard 21/21
- frd_lint BLOCK 0
- anchor ที่ไม่พบบนจอ 0
- เทียบต้นฉบับ WARN 0.485

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K9 — เทียบต้นฉบับ WARN 0.485

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
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 20 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 21 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (15 ข้อ) · Strike · ก่อน UAT
- OQ-03 · role admin ฝ่ายพัฒนาโครงการ ไม่อยู่ใน DOA master · role-line-manager เป็น relative role · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · ไม่มี module Project ใน FEATURE_REGISTRY · MDOC enum · พี่เบิร์ด · ก่อน register
- OQ-05 · ถ้อยคำคำอธิบาย ☐ ล่าช้า หรือมีปัญหา ซ้ำประโยค ☐ มีความเสี่ยง · ลูกค้า · –
- OQ-06 · รายงานของโครงการที่แผนถูกยกเลิก/ปิด · ลูกค้า · –
- OQ-07 · ข้อความยาวกับแบบพิมพ์ 2 หน้า · ลูกค้า · –
- OQ-08 · เขียนสถานะกิจกรรมกลับ PJP (Phase 2) · ลูกค้า · –
- OQ-09 · รหัส feature/REQ จริง · taxonomy function_code · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · รหัสโครงการ เลือกได้เฉพาะแ
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ผลการดำเนินงานในรอบรายงาน: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 9 แถวตามกระดาษ
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: KPI โครงการ (แผน vs ผลจริง): ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 8 แถวตามกระดาษ
- DEC-07 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ปัญหา อุปสรรค และความเสี่ยง: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 11 แถวตามกระดาษ
- DEC-08 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: แผนงานในรอบถัดไป: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 10 แถวตามกระดาษ
- DEC-09 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ประเด็นที่ต้องการการตัดสินใจจากผู้บริหาร: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 11 แถ
- DEC-10 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ) · รวม/แยก: owner_due: เก็บ owne
- DEC-11 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-12 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-13 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-14 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส PPR
- DEC-15 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `9711e9c5` | prototype |
| `02_BRD/BRD_F-TMP-005.docx` | `5ecd1dec` | brd_docx |
| `02_BRD/BRD_F-TMP-005.md` | `72bba647` | brd |
| `03_FRD/FRD_F-TMP-005_Pack/00_OVERVIEW.md` | `65543fb2` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/01_UI.md` | `88ea3fe1` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/02_API.md` | `ef6d24db` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/03_LOGIC.md` | `4c85c713` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/04_DB.md` | `aaeae9a1` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/05_RULES.md` | `6cbd1723` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/06_TESTS.md` | `14f0046c` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/07_LOCKED_DECISIONS.md` | `846c9e9e` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/INDEX.md` | `15f1d7a3` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/_SECTION_N.md` | `af6796dd` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/DOA_BRIEF_F-TMP-005.md` | `2ce053bf` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/DOCCFG_BRIEF_F-TMP-005.md` | `02441d38` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/MDOC_BRIEF_PPR.md` | `c3410c01` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/NTF_BRIEF_F-TMP-005.md` | `5b952a28` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/PPR.doa.yaml` | `d4bde69d` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/PPR.doccfg.yaml` | `c4595b0c` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/PPR.mdoc.yaml` | `0fd87aa3` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/PPR.ntf.yaml` | `fba97a98` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-005.md` | `ec6df7c1` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `c8f6e682` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `482a82ed` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-005.md` | `2ce053bf` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-005.md` | `02441d38` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_PPR.md` | `c3410c01` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-005.md` | `5b952a28` | ntf_brief |
| `05_Governance/PPR.doa.yaml` | `d4bde69d` | doa_yaml |
| `05_Governance/PPR.doccfg.yaml` | `c4595b0c` | doccfg_yaml |
| `05_Governance/PPR.mdoc.yaml` | `0fd87aa3` | mdoc_yaml |
| `05_Governance/PPR.ntf.yaml` | `fba97a98` | ntf_yaml |
| `05_Governance/decisions.yaml` | `d808e064` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-005.md` | `34c2ac66` | qa_audit |
| `06_Test/cases.json` | `39920dbc` | cases_json |
| `06_Test/testcase-F-TMP-005.html` | `72d61527` | testcases_uat |
| `06_Test/testcases-F-TMP-005.md` | `c32aaf65` | testcases_ai |
| `07_Print/_states_sheet.png` | `8f8aee82` | print_image_states_sheet |
| `07_Print/approved-doa6steps.data.json` | `9e53a1cc` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `92a120af` | print_data_approved_data |
| `07_Print/compare.json` | `ed57d57e` | report_compare |
| `07_Print/compare_side.png` | `e766a2c2` | print_image_compare_side |
| `07_Print/draft.data.json` | `5ed9b2fc` | print_data_draft_data |
| `07_Print/form.tpl.html` | `0815130c` | print_template |
| `07_Print/long-12rows.data.json` | `86512aa0` | print_data_long_12rows_data |
| `07_Print/pending.data.json` | `5adb745b` | print_data_pending_data |
| `07_Print/print_config.json` | `6778e93b` | print_config |
| `07_Print/profile.json` | `cc07c6f2` | print_profile |
| `07_Print/rejected.data.json` | `9719ab04` | print_data_rejected_data |
| `07_Print/รายงานความคืบหน้าโครงการ_approved-doa6steps.pdf` | `87fa7140` | print_pdf_approved_doa6steps |
| `07_Print/รายงานความคืบหน้าโครงการ_approved.pdf` | `48447dd2` | print_pdf_approved |
| `07_Print/รายงานความคืบหน้าโครงการ_draft.pdf` | `939696d3` | print_pdf_draft |
| `07_Print/รายงานความคืบหน้าโครงการ_long-12rows.pdf` | `f0237484` | print_pdf_long_12rows |
| `07_Print/รายงานความคืบหน้าโครงการ_pending.pdf` | `a296a229` | print_pdf_pending |
| `07_Print/รายงานความคืบหน้าโครงการ_print-spec.md` | `10418986` | print_spec |
| `07_Print/รายงานความคืบหน้าโครงการ_rejected.pdf` | `78f04afa` | print_pdf_rejected |
| `07_Print/รายงานความคืบหน้าโครงการ_template.html` | `44bb09b9` | print_extra_template |
| `08_Reference/01_list.png` | `4146bb5c` | original_01_list |
| `08_Reference/02_create.png` | `c92aae57` | original_02_create |
| `08_Reference/03_review.png` | `d3dddb21` | original_03_review |
| `08_Reference/04_submit.png` | `1fa2c7f4` | original_04_submit |
| `08_Reference/05_sign.png` | `a7b7f693` | original_05_sign |
| `08_Reference/06_pdf.png` | `36202955` | original_06_pdf |
| `08_Reference/07_view.png` | `f25b1376` | original_07_view |
| `08_Reference/2. FM-PDM-02 แบบฟอร์มรายงานความคืบหน้าโครงการ.docx` | `825059ed` | original_2_fm_pdm_02 |
| `08_Reference/FORM_SPEC.check.json` | `5ee776f3` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `5ece120a` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-005.html` | `a7b94bdf` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-005_v2.md` | `5bda2fec` | prebrief |
| `08_Reference/RUN_LOG.md` | `d5cd2fcd` | run_log |
| `08_Reference/SAMPLE.pdf` | `11693508` | original_sample |
| `08_Reference/page-1.png` | `d92621c2` | original_page_1 |
| `08_Reference/page-2.png` | `732c6870` | original_page_2 |
| `08_Reference/page-3.png` | `923ed96c` | original_page_3 |
| `08_Reference/page-4.png` | `778c7766` | original_page_4 |
| `08_Reference/reports/_SECTION_N.md` | `af6796dd` | report_frd_lint |
| `08_Reference/reports/anchors.json` | `4575252d` | report_anchors |
| `08_Reference/reports/e2e_report.json` | `7063f419` | report_e2e |
