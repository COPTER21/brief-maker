# F-TMP-004 DevPack — แบบฟอร์มแผนโครงการ (REQ-TMP-004)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 2
- มติ 18 ข้อ (AI-DEFAULT 14) · พร้อมเริ่มทำ
- test case AI 61 เคส
- e2e_standard 21/21
- frd_lint BLOCK 0
- anchor ที่ไม่พบบนจอ 0
- เทียบต้นฉบับ WARN 0.303

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K3 — run_log: ไฟล์ถูกแก้หลังลงทะเบียน — รัน manifest_scan ใหม่
- WARN K9 — เทียบต้นฉบับ WARN 0.303

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
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 20 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (14 ข้อ) · Strike · ก่อน UAT
- OQ-03 · role admin ฝ่ายพัฒนาโครงการ ไม่อยู่ใน DOA master · role-line-manager เป็น relative role · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · ไม่มี module Project ใน FEATURE_REGISTRY · MDOC enum · พี่เบิร์ด · ก่อน register
- OQ-05 · ข้อความยาวในส่วนที่ 2–3 กับแบบพิมพ์ 2 หน้า · ลูกค้า · –
- OQ-06 · รหัส feature/REQ จริง · taxonomy function_code · Strike · ก่อน register
- OQ-07 · ผู้รับผิดชอบหลัก (ไม่ใช่ผู้จัดทำ) ควรเห็นใบไหม · ลูกค้า · –
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ระยะเวลาดำเนินการ = วันที่
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: เป้าหมายและ KPI: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 3 แถวตามกระดาษ
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: แผนการดำเนินงาน (กิจกรรม): ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 10 แถวตามกระดาษ
- DEC-07 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการงบประมาณ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 6 แถวตามกระดาษ
- DEC-08 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ความเสี่ยง: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 5 แถวตามกระดาษ
- DEC-09 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-10 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-11 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-12 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-13 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส PJP
- DEC-14 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `0583e300` | prototype |
| `02_BRD/BRD_F-TMP-004.docx` | `b7f66dc3` | brd_docx |
| `02_BRD/BRD_F-TMP-004.md` | `798f22db` | brd |
| `03_FRD/FRD_F-TMP-004_Pack/00_OVERVIEW.md` | `fe5d3311` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/01_UI.md` | `6d28b43d` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/02_API.md` | `4dddfd00` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/03_LOGIC.md` | `26985bed` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/04_DB.md` | `57cbfb7c` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/05_RULES.md` | `e3f1c1c9` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/06_TESTS.md` | `b70bc971` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/07_LOCKED_DECISIONS.md` | `d608aa47` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/INDEX.md` | `a48677f6` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/_SECTION_N.md` | `b525bffc` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/DOA_BRIEF_F-TMP-004.md` | `d1da44a0` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/DOCCFG_BRIEF_F-TMP-004.md` | `84dccd0b` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/MDOC_BRIEF_PJP.md` | `81cd1a7a` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/NTF_BRIEF_F-TMP-004.md` | `74ce96f4` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/PJP.doa.yaml` | `563caacb` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/PJP.doccfg.yaml` | `843e9bac` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/PJP.mdoc.yaml` | `1a2a0dfa` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/PJP.ntf.yaml` | `6279d48a` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-004.md` | `636d646a` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `d988f98f` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `d3b95a9b` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-004.md` | `d1da44a0` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-004.md` | `84dccd0b` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_PJP.md` | `81cd1a7a` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-004.md` | `74ce96f4` | ntf_brief |
| `05_Governance/PJP.doa.yaml` | `563caacb` | doa_yaml |
| `05_Governance/PJP.doccfg.yaml` | `843e9bac` | doccfg_yaml |
| `05_Governance/PJP.mdoc.yaml` | `1a2a0dfa` | mdoc_yaml |
| `05_Governance/PJP.ntf.yaml` | `6279d48a` | ntf_yaml |
| `05_Governance/decisions.yaml` | `0a5f6b83` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-004.md` | `09f119ba` | qa_audit |
| `06_Test/cases.json` | `b21c7fe4` | cases_json |
| `06_Test/testcase-F-TMP-004.html` | `85b07eec` | testcases_uat |
| `06_Test/testcases-F-TMP-004.md` | `3ac346aa` | testcases_ai |
| `07_Print/_states_sheet.png` | `6e23a1e2` | print_image_states_sheet |
| `07_Print/approved-doa6steps.data.json` | `9e95286d` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `0547b11f` | print_data_approved_data |
| `07_Print/compare.json` | `69543c0c` | report_compare |
| `07_Print/compare_side.png` | `6217b6cd` | print_image_compare_side |
| `07_Print/draft.data.json` | `73364070` | print_data_draft_data |
| `07_Print/form.tpl.html` | `e8da3c74` | print_template |
| `07_Print/long-12rows.data.json` | `e361d0dd` | print_data_long_12rows_data |
| `07_Print/pending.data.json` | `07c59551` | print_data_pending_data |
| `07_Print/print_config.json` | `a7203939` | print_config |
| `07_Print/profile.json` | `34d8b378` | print_profile |
| `07_Print/rejected.data.json` | `7a18a51d` | print_data_rejected_data |
| `07_Print/แบบฟอร์มแผนโครงการ_approved-doa6steps.pdf` | `635cdd8c` | print_pdf_approved_doa6steps |
| `07_Print/แบบฟอร์มแผนโครงการ_approved.pdf` | `80775943` | print_pdf_approved |
| `07_Print/แบบฟอร์มแผนโครงการ_draft.pdf` | `95382e37` | print_pdf_draft |
| `07_Print/แบบฟอร์มแผนโครงการ_long-12rows.pdf` | `b73486d8` | print_pdf_long_12rows |
| `07_Print/แบบฟอร์มแผนโครงการ_pending.pdf` | `18588b64` | print_pdf_pending |
| `07_Print/แบบฟอร์มแผนโครงการ_print-spec.md` | `a3798c3c` | print_spec |
| `07_Print/แบบฟอร์มแผนโครงการ_rejected.pdf` | `f4ebad9f` | print_pdf_rejected |
| `07_Print/แบบฟอร์มแผนโครงการ_template.html` | `3849b2cd` | print_extra_template |
| `08_Reference/01_list.png` | `f3256d27` | original_01_list |
| `08_Reference/02_create.png` | `bc330c03` | original_02_create |
| `08_Reference/03_review.png` | `033f9a3c` | original_03_review |
| `08_Reference/04_approve.png` | `9b9c6e93` | original_04_approve |
| `08_Reference/05_pdf.png` | `2ed86782` | original_05_pdf |
| `08_Reference/06_sign.png` | `05ffb2db` | original_06_sign |
| `08_Reference/07_view.png` | `06607e86` | original_07_view |
| `08_Reference/1. FM-PDM -01 แบบฟอร์มแผนโครงการ (PROJECT PLAN FORM).xlsx` | `9ef97535` | original_1_fm_pdm_01_project_plan_form |
| `08_Reference/FORM_SPEC.check.json` | `e35af326` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `fa97f812` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-004.html` | `82354339` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-004_v2.md` | `7749d6a6` | prebrief |
| `08_Reference/RUN_LOG.md` | `02d3c493` | run_log |
| `08_Reference/SAMPLE.pdf` | `886fbc29` | original_sample |
| `08_Reference/page-1.png` | `a2ba1e24` | original_page_1 |
| `08_Reference/page-2.png` | `44b2b4a7` | original_page_2 |
| `08_Reference/page-3.png` | `14ba102e` | original_page_3 |
| `08_Reference/reports/_SECTION_N.md` | `b525bffc` | report_frd_lint |
| `08_Reference/reports/anchors.json` | `4184d03a` | report_anchors |
| `08_Reference/reports/e2e_report.json` | `0ab7a309` | report_e2e |
