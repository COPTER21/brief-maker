# F-TMP-008 DevPack — แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายบริหารการลงทุนจัดเก็บ) (REQ-TMP-008)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 17 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 30 เคส
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
- OQ-03 · ไม่มี role ผู้จัดการฝ่ายพัฒนาธุรกิจ ใน DOA master (ใช้ role-mgr-bu ชั่วคราว) · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · HandoverConfig มีหรือยัง / ใช้ร่วมกับ FM-BDM-07 · พี่เบิร์ด · ก่อน dev
- OQ-05 · ผูกกับ FM-BDM-07 / โครงการ ไหม · ลูกค้า · –
- OQ-06 · กำหนดการติดตาม เป็นวันที่หรือข้อความ · ลูกค้า · –
- OQ-07 · รหัส HOI ชนไหม (HOB สงวน FM-BDM-07) · taxonomy function_code · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "ผลการรับมอบ: รับมอบครบถ้วน / รับมอบแบบมีเงื่อนไข / ยังไ
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ผลการตรวจรับเอกสาร: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 12 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส HOI
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `720a26ee` | prototype |
| `02_BRD/BRD_F-TMP-008.docx` | `3678e372` | brd_docx |
| `02_BRD/BRD_F-TMP-008.md` | `9b70be5f` | brd |
| `03_FRD/FRD_F-TMP-008_Pack/00_OVERVIEW.md` | `fcef7361` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/01_UI.md` | `32c0cd7d` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/02_API.md` | `491cb6db` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/03_LOGIC.md` | `f5bb612a` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/04_DB.md` | `76d9df06` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/05_RULES.md` | `629d3907` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/06_TESTS.md` | `ee1e4417` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/07_LOCKED_DECISIONS.md` | `1fa2ecbd` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/INDEX.md` | `55e33da8` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/_SECTION_N.md` | `1dfcba60` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/DOA_BRIEF_F-TMP-008.md` | `41f74467` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/DOCCFG_BRIEF_F-TMP-008.md` | `fb1c8638` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/HOI.doa.yaml` | `e1ecbbbf` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/HOI.doccfg.yaml` | `e96d3b93` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/HOI.mdoc.yaml` | `68e3fbcb` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/HOI.ntf.yaml` | `238eb476` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/MDOC_BRIEF_HOI.md` | `32d76dd5` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/NTF_BRIEF_F-TMP-008.md` | `d24c5379` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-008.md` | `03768ea8` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `c1e87d25` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `39b29a97` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-008.md` | `41f74467` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-008.md` | `fb1c8638` | doccfg_brief |
| `05_Governance/HOI.doa.yaml` | `e1ecbbbf` | doa_yaml |
| `05_Governance/HOI.doccfg.yaml` | `e96d3b93` | doccfg_yaml |
| `05_Governance/HOI.mdoc.yaml` | `68e3fbcb` | mdoc_yaml |
| `05_Governance/HOI.ntf.yaml` | `238eb476` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_HOI.md` | `32d76dd5` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-008.md` | `d24c5379` | ntf_brief |
| `05_Governance/decisions.yaml` | `f6b71db0` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-008.md` | `c19c106b` | qa_audit |
| `06_Test/cases.json` | `a03cd89e` | cases_json |
| `06_Test/testcase-F-TMP-008.html` | `fae8dc9c` | testcases_uat |
| `06_Test/testcases-F-TMP-008.md` | `925f7fe6` | testcases_ai |
| `07_Print/FM-BDM-08_template.html` | `4209ff0d` | print_extra_fm_bdm_08_template |
| `07_Print/HOI_print-spec.md` | `6d061c7e` | print_spec |
| `07_Print/approved-doa6steps.data.json` | `dc44df42` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `a4eef267` | print_data_approved_data |
| `07_Print/draft.data.json` | `d54a4d5d` | print_data_draft_data |
| `07_Print/form.tpl.html` | `1686eec3` | print_template |
| `07_Print/long-24rows.data.json` | `5a5f1a43` | print_data_long_24rows_data |
| `07_Print/print_config.json` | `8307bf0d` | print_config |
| `07_Print/profile.json` | `e177ea02` | print_profile |
| `07_Print/rejected.data.json` | `c0392359` | print_data_rejected_data |
| `08_Reference/8. FM-BDM-08 แบบฟอร์มชุดเอกสารส่งมอบงาน  (สำหรับฝ่ายบริหารการลงทุนจัดเก็บ).xlsx` | `8d941938` | original_8_fm_bdm_08 |
| `08_Reference/FORM_SPEC.check.json` | `732e32ad` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `6351ccff` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-008.html` | `504179f4` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-008_v2.md` | `58eccb0b` | prebrief |
| `08_Reference/RUN_LOG.md` | `0a316150` | run_log |
| `08_Reference/SAMPLE.pdf` | `a28d9452` | original_sample |
| `08_Reference/page-1.png` | `ba08c73d` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `1dfcba60` | report_frd_lint |
