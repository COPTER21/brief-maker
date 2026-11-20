# F-TMP-003 DevPack — แบบฟอร์มสรุปผลการคัดกรองโครงการเบื้องต้น (REQ-TMP-003)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 17 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 31 เคส
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
| `03_FRD` | FRD Pack | 18 |
| `04_UI_Brief` | UI Brief AS-BUILT | 1 |
| `05_Governance` | มติ (DECISIONS) + ใบประกาศ DOCCFG / DOA / MDOC / NTF | 11 |
| `06_Test` | test case AI + UAT ฉบับคน + QA audit | 4 |
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 10 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 9 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (11 ข้อ) · Strike · ก่อน UAT
- OQ-03 · role รองกรรมการผู้จัดการ / ผู้มีอำนาจตามตารางอำนาจอนุมัติ ไม่มีใน DOA master (ใช้ role-gm ชั่วคราว) · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · ScreeningCriteria config มีหรือยัง / เจ้าของ · พี่เบิร์ด · ก่อน dev
- OQ-05 · ผูกกับโครงการ FM-BDM-01 ไหม · ลูกค้า · –
- OQ-06 · รหัส SCR ชนไหม · taxonomy function_code · Strike · ก่อน register
- OQ-07 · ผลไม่ดำเนินการต่อ → สร้าง FM-BDM-04 อัตโนมัติไหม · ลูกค้า · –
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "8 เกณฑ์ประเมิน + น้ำหนัก 15/15/15/20/10/10/10/5" → Scre
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: เกณฑ์ประเมิน: สูงสุด 8 แถว · PDF อย่างน้อย 8 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส SCR
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `b3612d7d` | prototype |
| `02_BRD/BRD_F-TMP-003.docx` | `5e9bedb9` | brd_docx |
| `02_BRD/BRD_F-TMP-003.md` | `34ead952` | brd |
| `03_FRD/FRD_F-TMP-003_Pack/00_OVERVIEW.md` | `d5bdefa3` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/01_UI.md` | `3d5dd446` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/02_API.md` | `9865fb16` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/03_LOGIC.md` | `d7526370` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/04_DB.md` | `cfe59df0` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/05_RULES.md` | `964bb7a3` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/06_TESTS.md` | `e2b6a2dc` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/07_LOCKED_DECISIONS.md` | `bb44e45c` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/INDEX.md` | `7c4ed16d` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/_SECTION_N.md` | `b1acbd46` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/DOA_BRIEF_F-TMP-003.md` | `62d244ad` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/DOCCFG_BRIEF_F-TMP-003.md` | `e4a5d833` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/MDOC_BRIEF_SCR.md` | `564be494` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/NTF_BRIEF_F-TMP-003.md` | `df012188` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/SCR.doa.yaml` | `ecfff421` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/SCR.doccfg.yaml` | `7875b77c` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/SCR.mdoc.yaml` | `09f13a2e` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/SCR.ntf.yaml` | `dd1b634e` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-003.md` | `c617b531` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `a957843d` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `2d4c08a2` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-003.md` | `62d244ad` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-003.md` | `e4a5d833` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_SCR.md` | `564be494` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-003.md` | `df012188` | ntf_brief |
| `05_Governance/SCR.doa.yaml` | `ecfff421` | doa_yaml |
| `05_Governance/SCR.doccfg.yaml` | `7875b77c` | doccfg_yaml |
| `05_Governance/SCR.mdoc.yaml` | `09f13a2e` | mdoc_yaml |
| `05_Governance/SCR.ntf.yaml` | `dd1b634e` | ntf_yaml |
| `05_Governance/decisions.yaml` | `2437ded7` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-003.md` | `b7532702` | qa_audit |
| `06_Test/cases.json` | `74ba3f25` | cases_json |
| `06_Test/testcase-F-TMP-003.html` | `2a9d7fbf` | testcases_uat |
| `06_Test/testcases-F-TMP-003.md` | `ba88b4e3` | testcases_ai |
| `07_Print/FM-BDM-03_template.html` | `62b3cd27` | print_extra_fm_bdm_03_template |
| `07_Print/SCR_print-spec.md` | `ee9bae0c` | print_spec |
| `07_Print/approved-doa6steps.data.json` | `8a5c8a79` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `1efa24dc` | print_data_approved_data |
| `07_Print/draft.data.json` | `0c63a620` | print_data_draft_data |
| `07_Print/form.tpl.html` | `8df4e123` | print_template |
| `07_Print/long-text.data.json` | `2751750a` | print_data_long_text_data |
| `07_Print/print_config.json` | `e15315ce` | print_config |
| `07_Print/profile.json` | `491dab40` | print_profile |
| `07_Print/rejected.data.json` | `b4f39434` | print_data_rejected_data |
| `08_Reference/3. FM-BDM-03 แบบฟอร์มสรุปผลการคัดกรองโครงการเบื้องต้น.xlsx` | `b9aa4ba1` | original_3_fm_bdm_03 |
| `08_Reference/FORM_SPEC.check.json` | `380c04b0` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `39c565d4` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-003.html` | `5b26e725` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-003_v2.md` | `5f0e4fd2` | prebrief |
| `08_Reference/RUN_LOG.md` | `6b18ab37` | run_log |
| `08_Reference/SAMPLE.pdf` | `ebf3f4fa` | original_sample |
| `08_Reference/page-1.png` | `51c12f93` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `b1acbd46` | report_frd_lint |
