# F-TMP-008 DevPack — ใบรายงานการแก้ไขและป้องกันเพื่อการควบคุม (REQ-TMP-008)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 35 ข้อ (AI-DEFAULT 28) · พร้อมเริ่มทำ
- test case AI 60 เคส
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
| `03_FRD` | FRD Pack | 17 |
| `04_UI_Brief` | UI Brief AS-BUILT | 1 |
| `05_Governance` | มติ (DECISIONS) + ใบประกาศ DOCCFG / DOA / MDOC / NTF | 11 |
| `06_Test` | test case AI + UAT ฉบับคน + QA audit | 4 |
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 10 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 10 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 4 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "(วิเคราะห์สาเหตุและเริ่มดำเนินการภายใน 30 นาที)" → CarC
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: 3. อาการของปัญหา (+6.3 ประสิทธิผล): ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 5 แถวตามกระ
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ผู้เข้าร่วมประชุม: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 8 แถวตามกระดาษ
- DEC-07 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สาเหตุระดับ 1 ( ทำไม 1) — การจัดทำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 7 แถวตามกระ
- DEC-08 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สาเหตุระดับ 2 ( ทำไม 2 ) — การจัดทำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 7 แถวตามกร
- DEC-09 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สาเหตุระดับ 1 ( ทำไม 1) — การตรวจสอบ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 7 แถวตามก
- DEC-10 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สาเหตุระดับ 2 ( ทำไม 2 ) — การตรวจสอบ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 7 แถวตาม
- DEC-11 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สาเหตุระดับ 3 ( ทำไม 3 ) — การจัดทำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 7 แถวตามกร
- DEC-12 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สาเหตุรากเหง้า — การจัดทำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 7 แถวตามกระดาษ
- DEC-13 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สาเหตุระดับ 3 ( ทำไม 3 ) — การตรวจสอบ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 7 แถวตาม
- DEC-14 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สาเหตุรากเหง้า — การตรวจสอบ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 7 แถวตามกระดาษ
- DEC-15 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: 5. คิดค้นมาตรการแก้ปัญหาและวางแผนปฏิบัติการ ( D ) — การจัดทำ: ไม่จำกัดจำนวนแถว ·
- DEC-16 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: 5. คิดค้นมาตรการแก้ปัญหาและวางแผนปฏิบัติการ ( D ) — การตรวจสอบ: ไม่จำกัดจำนวนแถว
- DEC-17 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: 5.2 การแก้ไขปัญหา / 6.2 ผลการแก้ไขปัญหา — การจัดทำ: ไม่จำกัดจำนวนแถว · PDF อย่าง
- DEC-18 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: 7.สร้างระบบการป้องกัน ( A ) — การจัดทำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 7 แถวตา
- DEC-19 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: 5.2 การแก้ไขปัญหา / 6.2 ผลการแก้ไขปัญหา — การตรวจสอบ: ไม่จำกัดจำนวนแถว · PDF อย่
- DEC-20 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: 7.สร้างระบบการป้องกัน ( A ) — การตรวจสอบ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 7 แถว
- DEC-21 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: 8. เอกสารที่ต้องแก้ไข หลังจากการแก้ไขและป้องกัน: ไม่จำกัดจำนวนแถว · PDF อย่างน้อ
- DEC-22 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: 10.การตรวจสอบ 3 Doc หลังการแก้ไขป้องกัน: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 3 แถวต
- DEC-23 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-24 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นตามตำแหน่งกระดาษ 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบ
- DEC-25 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-26 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-27 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส CAR
- DEC-28 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `adda4a84` | prototype |
| `02_BRD/BRD_F-TMP-008.docx` | `ba1022bc` | brd_docx |
| `02_BRD/BRD_F-TMP-008.md` | `d4ad3a8b` | brd |
| `03_FRD/FRD_F-TMP-008_Pack/00_OVERVIEW.md` | `1cc86f94` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/01_UI.md` | `ee1688b1` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/02_API.md` | `e3a3f45f` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/03_LOGIC.md` | `d8db15de` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/04_DB.md` | `b17a64f4` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/05_RULES.md` | `3ac56fc5` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/06_TESTS.md` | `60bfe34a` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/07_LOCKED_DECISIONS.md` | `314138eb` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/INDEX.md` | `8f3d5106` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/CAR.doa.yaml` | `256b85fe` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/CAR.doccfg.yaml` | `8773e0bb` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/CAR.mdoc.yaml` | `1c009d3d` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/CAR.ntf.yaml` | `86cfc3ac` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/DOA_BRIEF_F-TMP-008.md` | `d5b72da9` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/DOCCFG_BRIEF_F-TMP-008.md` | `e232c0af` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/MDOC_BRIEF_CAR.md` | `252842ff` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/NTF_BRIEF_F-TMP-008.md` | `88b76c93` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-008.md` | `5956c041` | ui_brief |
| `05_Governance/CAR.doa.yaml` | `256b85fe` | doa_yaml |
| `05_Governance/CAR.doccfg.yaml` | `8773e0bb` | doccfg_yaml |
| `05_Governance/CAR.mdoc.yaml` | `1c009d3d` | mdoc_yaml |
| `05_Governance/CAR.ntf.yaml` | `86cfc3ac` | ntf_yaml |
| `05_Governance/DECISIONS.lock.json` | `39fc06bf` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `700031af` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-008.md` | `d5b72da9` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-008.md` | `e232c0af` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_CAR.md` | `252842ff` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-008.md` | `88b76c93` | ntf_brief |
| `05_Governance/decisions.yaml` | `c3139782` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-008.md` | `f28ea92a` | qa_audit |
| `06_Test/cases.json` | `02d883d2` | cases_json |
| `06_Test/testcase-F-TMP-008.html` | `95f56edd` | testcases_uat |
| `06_Test/testcases-F-TMP-008.md` | `7c5a9f78` | testcases_ai |
| `07_Print/CAR_print-spec.md` | `8eae4ed0` | print_spec |
| `07_Print/CAR_template.html` | `eeb09fb0` | print_extra_car_template |
| `07_Print/approved-doa6steps.data.json` | `4179147b` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `bdcd7af4` | print_data_approved_data |
| `07_Print/draft.data.json` | `df140dc0` | print_data_draft_data |
| `07_Print/form.tpl.html` | `294cb2ab` | print_template |
| `07_Print/long-text.data.json` | `075ae4e6` | print_data_long_text_data |
| `07_Print/print_config.json` | `609410e4` | print_config |
| `07_Print/profile.json` | `461911b0` | print_profile |
| `07_Print/rejected.data.json` | `626fe1c5` | print_data_rejected_data |
| `08_Reference/4. FM-CCC-04 ใบรายงานการแก้ไขและป้องกันเพื่อการควบคุม Corrective Action Request (CAR).xlsx` | `f9293361` | original_4_fm_ccc_04_corrective_action_request_ca |
| `08_Reference/FORM_SPEC.check.json` | `f4409a82` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `6a48a583` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-008.html` | `d8f9f99b` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-008_v2.md` | `ef8c7089` | prebrief |
| `08_Reference/RUN_LOG.md` | `02e79bc0` | run_log |
| `08_Reference/SAMPLE.pdf` | `36ae7d0f` | original_sample |
| `08_Reference/page-1.png` | `2b1ad265` | original_page_1 |
| `08_Reference/page-2.png` | `8246c698` | original_page_2 |
| `08_Reference/reports/_SECTION_N.md` | `613214b5` | report_frd_lint |
