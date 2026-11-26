# F-TMP-004 DevPack — แบบฟอร์มตารางติดตามงานและแผนฐาน (REQ-TMP-004)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 18 ข้อ (AI-DEFAULT 12) · พร้อมเริ่มทำ
- test case AI 39 เคส
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
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 11 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 9 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ความคลาดเคลื่อน (วัน) = วั
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: แผนฐานและหมุดหมายสำคัญ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 8 แถวตามกระดาษ
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการติดตามงาน: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 18 แถวตามกระดาษ
- DEC-07 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · เพิ่ม: ชื่อโครงการ / ธุรกรรม (F01 · กระดาษไม่มีช่องระบุโครงก
- DEC-08 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-09 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-10 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-11 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส IVMB
- DEC-12 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `185acf3b` | prototype |
| `02_BRD/BRD_F-TMP-004.docx` | `ffe2e9a5` | brd_docx |
| `02_BRD/BRD_F-TMP-004.md` | `453dec41` | brd |
| `03_FRD/FRD_F-TMP-004_Pack/00_OVERVIEW.md` | `47049fe8` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/01_UI.md` | `be556ea5` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/02_API.md` | `595e776b` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/03_LOGIC.md` | `dd3a562e` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/04_DB.md` | `c8592806` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/05_RULES.md` | `0f26de6c` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/06_TESTS.md` | `d1849a8d` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/07_LOCKED_DECISIONS.md` | `f783172f` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/INDEX.md` | `f2c8ae61` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/_SECTION_N.md` | `3ab3cd30` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/DOA_BRIEF_F-TMP-004.md` | `adc261c9` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/DOCCFG_BRIEF_F-TMP-004.md` | `5ec946f2` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/IVMB.doa.yaml` | `1d6d35ce` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/IVMB.doccfg.yaml` | `a997ab82` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/IVMB.mdoc.yaml` | `5dcbed0d` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/IVMB.ntf.yaml` | `c0dcb971` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/MDOC_BRIEF_IVMB.md` | `5538790d` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/NTF_BRIEF_F-TMP-004.md` | `db89eeb0` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-004.md` | `fea99941` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `81cf356f` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `5a943c8b` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-004.md` | `adc261c9` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-004.md` | `5ec946f2` | doccfg_brief |
| `05_Governance/IVMB.doa.yaml` | `1d6d35ce` | doa_yaml |
| `05_Governance/IVMB.doccfg.yaml` | `a997ab82` | doccfg_yaml |
| `05_Governance/IVMB.mdoc.yaml` | `5dcbed0d` | mdoc_yaml |
| `05_Governance/IVMB.ntf.yaml` | `c0dcb971` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_IVMB.md` | `5538790d` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-004.md` | `db89eeb0` | ntf_brief |
| `05_Governance/decisions.yaml` | `6a6d1881` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-004.md` | `fe2223ec` | qa_audit |
| `06_Test/cases.json` | `915407b7` | cases_json |
| `06_Test/testcase-F-TMP-004.html` | `01b4fd1d` | testcases_uat |
| `06_Test/testcases-F-TMP-004.md` | `3742c5b4` | testcases_ai |
| `07_Print/R1.data.json` | `20704198` | print_data_r1_data |
| `07_Print/approved-doa6steps.data.json` | `cf8887eb` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `60fd15de` | print_data_approved_data |
| `07_Print/draft.data.json` | `4f4a91e3` | print_data_draft_data |
| `07_Print/form.tpl.html` | `c0ede71c` | print_template |
| `07_Print/long-12milestones-18tasks.data.json` | `b18eab6b` | print_data_long_12milestones_18tasks_data |
| `07_Print/print_config.json` | `a0c0c1cd` | print_config |
| `07_Print/profile.json` | `3bf1047c` | print_profile |
| `07_Print/rejected.data.json` | `bc94a880` | print_data_rejected_data |
| `07_Print/แบบฟอร์มตารางติดตามงานและแผนฐาน_print-spec.md` | `1fb81eab` | print_spec |
| `07_Print/แบบฟอร์มตารางติดตามงานและแผนฐาน_template.html` | `9c519ce9` | print_extra_template |
| `08_Reference/2. FM-IVM-02 แบบฟอร์มตารางติดตามงานและแผนฐาน.xlsx` | `7f38ac57` | original_2_fm_ivm_02 |
| `08_Reference/FORM_SPEC.check.json` | `017ba924` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `4ea00635` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-004.html` | `fa80b6f8` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-004_v2.md` | `eff3b6a2` | prebrief |
| `08_Reference/RUN_LOG.md` | `c582e069` | run_log |
| `08_Reference/SAMPLE.pdf` | `3faeceec` | original_sample |
| `08_Reference/page-1.png` | `0aa122b7` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `3ab3cd30` | report_frd_lint |
