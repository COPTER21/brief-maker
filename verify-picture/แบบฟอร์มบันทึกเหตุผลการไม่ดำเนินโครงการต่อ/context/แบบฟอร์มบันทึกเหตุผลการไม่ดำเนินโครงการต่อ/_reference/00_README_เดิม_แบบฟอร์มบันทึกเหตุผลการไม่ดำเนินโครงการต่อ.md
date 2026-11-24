# F-TMP-004 DevPack — แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ (REQ-TMP-004)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 16 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 30 เคส
- e2e_standard 21/21
- anchor ที่ไม่พบบนจอ 0
- เทียบต้นฉบับ WARN 0.467

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K9 — เทียบต้นฉบับ WARN 0.467

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
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 13 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 10 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (11 ข้อ) + ค่าเริ่ม "ไม่ใช่" ของช่องเลือก · Strike · ก่อน UAT
- OQ-03 · role รองกรรมการผู้จัดการ/กรรมการผู้จัดการ/ผู้มีอำนาจตามตาราง ไม่มีใน DOA master (ใช้ role-gm ชั่วคราว) · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · ProjectClosure config มีหรือยัง / เจ้าของ · พี่เบิร์ด · ก่อน dev
- OQ-05 · ผูกกับโครงการ FM-BDM-01 / ผลคัดกรอง FM-BDM-03 และปิดโครงการต้นทางไหม · ลูกค้า · –
- OQ-06 · รหัส PCL ชนไหม · taxonomy function_code · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "ไม่สอดคล้องกับกลยุทธ์ · ตลาดไม่น่าสนใจ · ผลตอบแทนไม่เพี
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: เหตุผลการไม่ดำเนินโครงการต่อ: สูงสุด 8 แถว · PDF อย่างน้อย 8 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส PCL
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `a3d218b4` | prototype |
| `02_BRD/BRD_F-TMP-004.docx` | `758b3b2f` | brd_docx |
| `02_BRD/BRD_F-TMP-004.md` | `c62f103d` | brd |
| `03_FRD/FRD_F-TMP-004_Pack/00_OVERVIEW.md` | `0b6c033d` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/01_UI.md` | `2b895ab9` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/02_API.md` | `a2493bd1` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/03_LOGIC.md` | `ae915eae` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/04_DB.md` | `c8b353e4` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/05_RULES.md` | `c8015531` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/06_TESTS.md` | `9f7e1a44` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/07_LOCKED_DECISIONS.md` | `83072629` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/INDEX.md` | `87bf8d4c` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/_SECTION_N.md` | `ab653a33` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/DOA_BRIEF_F-TMP-004.md` | `282826ab` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/DOCCFG_BRIEF_F-TMP-004.md` | `a5d148f3` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/MDOC_BRIEF_PCL.md` | `39d2005c` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/NTF_BRIEF_F-TMP-004.md` | `a80df05b` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/PCL.doa.yaml` | `e66be927` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/PCL.doccfg.yaml` | `0983a725` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/PCL.mdoc.yaml` | `d0e60186` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/PCL.ntf.yaml` | `ac042cdc` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-004.md` | `aa523830` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `9ded388c` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `be5c8e62` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-004.md` | `282826ab` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-004.md` | `a5d148f3` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_PCL.md` | `39d2005c` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-004.md` | `a80df05b` | ntf_brief |
| `05_Governance/PCL.doa.yaml` | `e66be927` | doa_yaml |
| `05_Governance/PCL.doccfg.yaml` | `0983a725` | doccfg_yaml |
| `05_Governance/PCL.mdoc.yaml` | `d0e60186` | mdoc_yaml |
| `05_Governance/PCL.ntf.yaml` | `ac042cdc` | ntf_yaml |
| `05_Governance/decisions.yaml` | `2a9c13d7` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-004.md` | `25d50d59` | qa_audit |
| `06_Test/cases.json` | `ff8f7f06` | cases_json |
| `06_Test/testcase-F-TMP-004.html` | `29f22638` | testcases_uat |
| `06_Test/testcases-F-TMP-004.md` | `da353745` | testcases_ai |
| `07_Print/FM-BDM-04_template.html` | `52d93dc8` | print_extra_fm_bdm_04_template |
| `07_Print/PCL_print-spec.md` | `b984dfd8` | print_spec |
| `07_Print/approved-doa6steps.data.json` | `1a47c194` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `bc96a3d4` | print_data_approved_data |
| `07_Print/compare.json` | `be675f45` | report_compare |
| `07_Print/compare_overlay.png` | `af432fe5` | print_image_compare_overlay |
| `07_Print/compare_side.png` | `f2e8cc38` | print_image_compare_side |
| `07_Print/draft.data.json` | `d2b92863` | print_data_draft_data |
| `07_Print/form.tpl.html` | `0e69ba7d` | print_template |
| `07_Print/long-8reasons.data.json` | `723f3a66` | print_data_long_8reasons_data |
| `07_Print/print_config.json` | `53371252` | print_config |
| `07_Print/profile.json` | `962e97f5` | print_profile |
| `07_Print/rejected.data.json` | `2088e2d6` | print_data_rejected_data |
| `08_Reference/4. FM-BDM-04 แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ.xlsx` | `a898b881` | original_4_fm_bdm_04 |
| `08_Reference/FORM_SPEC.check.json` | `a51d45d4` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `68ac56ab` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-004.html` | `b9e70fab` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-004_v2.md` | `7d33f165` | prebrief |
| `08_Reference/RUN_LOG.md` | `5b82a99e` | run_log |
| `08_Reference/SAMPLE.pdf` | `ef2c6a84` | original_sample |
| `08_Reference/page-1.png` | `b5fe9ecf` | original_page_1 |
| `08_Reference/reports/anchors.json` | `6fd29cdd` | report_anchors |
| `08_Reference/reports/e2e_report.json` | `1db788a8` | report_e2e |
