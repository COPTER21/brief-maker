# F-TMP-007 DevPack — แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายพัฒนาธุรกิจจัดเก็บ) (REQ-TMP-007)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 16 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
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
- OQ-03 · role ฝ่ายบริหารการลงทุน (ผู้รับมอบ) ไม่มีใน DOA master (ใช้ role-mgr-bu ชั่วคราว) · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · HandoverPackageConfig มีหรือยัง / เจ้าของ / ใช้ร่วม FM-BDM-08 · พี่เบิร์ด · ก่อน dev
- OQ-05 · ดึงรายการเอกสารจากเอกสาร BDM ในระบบอัตโนมัติไหม · ลูกค้า · –
- OQ-06 · FM-BDM-07 กับ FM-BDM-08 เป็นเอกสารเดียว 2 มุมมองหรือ 2 เอกสาร · ลูกค้า + Strike · –
- OQ-07 · รหัส HOB ชนไหม · taxonomy function_code · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "สถานะข้อมูล: สมบูรณ์ / มีข้อจำกัด / รอข้อมูลเพิ่มเติม" 
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการเอกสารในชุดส่งมอบ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 12 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส HOB
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `88321264` | prototype |
| `02_BRD/BRD_F-TMP-007.docx` | `41455158` | brd_docx |
| `02_BRD/BRD_F-TMP-007.md` | `3bd309f0` | brd |
| `03_FRD/FRD_F-TMP-007_Pack/00_OVERVIEW.md` | `b51b0289` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/01_UI.md` | `f21c9bad` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/02_API.md` | `ec98768f` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/03_LOGIC.md` | `0a6ec448` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/04_DB.md` | `cd22dbce` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/05_RULES.md` | `92782260` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/06_TESTS.md` | `6a02a2e4` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/07_LOCKED_DECISIONS.md` | `3ae5d7ad` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/INDEX.md` | `b7c5472b` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/_SECTION_N.md` | `76790c3e` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/DOA_BRIEF_F-TMP-007.md` | `29814b8c` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/DOCCFG_BRIEF_F-TMP-007.md` | `2e06eaa1` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/HOB.doa.yaml` | `b0239aaf` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/HOB.doccfg.yaml` | `e3b25a90` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/HOB.mdoc.yaml` | `42ac0efa` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/HOB.ntf.yaml` | `d560f6e2` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/MDOC_BRIEF_HOB.md` | `9f14f197` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/NTF_BRIEF_F-TMP-007.md` | `3f57e459` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-007.md` | `55d54cd2` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `3eba01d6` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `edaf9ebb` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-007.md` | `29814b8c` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-007.md` | `2e06eaa1` | doccfg_brief |
| `05_Governance/HOB.doa.yaml` | `b0239aaf` | doa_yaml |
| `05_Governance/HOB.doccfg.yaml` | `e3b25a90` | doccfg_yaml |
| `05_Governance/HOB.mdoc.yaml` | `42ac0efa` | mdoc_yaml |
| `05_Governance/HOB.ntf.yaml` | `d560f6e2` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_HOB.md` | `9f14f197` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-007.md` | `3f57e459` | ntf_brief |
| `05_Governance/decisions.yaml` | `445ca13e` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-007.md` | `862bfdb7` | qa_audit |
| `06_Test/cases.json` | `a3cdab13` | cases_json |
| `06_Test/testcase-F-TMP-007.html` | `f5c8be1b` | testcases_uat |
| `06_Test/testcases-F-TMP-007.md` | `cfd93771` | testcases_ai |
| `07_Print/FM-BDM-07_template.html` | `80c28b9e` | print_extra_fm_bdm_07_template |
| `07_Print/HOB_print-spec.md` | `4644fb52` | print_spec |
| `07_Print/approved-doa6steps.data.json` | `882df7df` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `549309ea` | print_data_approved_data |
| `07_Print/draft.data.json` | `ab70c812` | print_data_draft_data |
| `07_Print/form.tpl.html` | `f5135ca1` | print_template |
| `07_Print/long-24rows.data.json` | `e5a6ff9b` | print_data_long_24rows_data |
| `07_Print/print_config.json` | `b75f9a68` | print_config |
| `07_Print/profile.json` | `6db304f5` | print_profile |
| `07_Print/rejected.data.json` | `cd34a047` | print_data_rejected_data |
| `08_Reference/7. FM-BDM-07 แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายพัฒนาธุรกิจจัดเก็บ).xlsx` | `a392ffbe` | original_7_fm_bdm_07 |
| `08_Reference/FORM_SPEC.check.json` | `9fa23080` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `d00d4af6` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-007.html` | `bb9ab67c` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-007_v2.md` | `6dbd1756` | prebrief |
| `08_Reference/RUN_LOG.md` | `b6f8188c` | run_log |
| `08_Reference/SAMPLE.pdf` | `9b22b86e` | original_sample |
| `08_Reference/page-1.png` | `399ba3de` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `76790c3e` | report_frd_lint |
