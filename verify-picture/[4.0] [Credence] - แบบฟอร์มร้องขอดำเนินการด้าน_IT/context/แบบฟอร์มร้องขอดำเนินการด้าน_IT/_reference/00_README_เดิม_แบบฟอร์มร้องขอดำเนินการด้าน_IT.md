# F-TMP-001 DevPack — แบบฟอร์มร้องขอดำเนินการด้าน IT (REQ-TMP-001)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 15 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 64 เคส
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
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-line-manager · วงเง
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · วันที่ต้องการส่งมอบ ต้องไม
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส ITRS
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `6b8e9bc9` | prototype |
| `02_BRD/BRD_F-TMP-001.docx` | `e3916b6a` | brd_docx |
| `02_BRD/BRD_F-TMP-001.md` | `999fa166` | brd |
| `03_FRD/FRD_F-TMP-001_Pack/00_OVERVIEW.md` | `80256dc0` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/01_UI.md` | `86e94e28` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/02_API.md` | `e9950e73` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/03_LOGIC.md` | `f9c01b65` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/04_DB.md` | `edff6764` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/05_RULES.md` | `2c00e622` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/06_TESTS.md` | `ce150fa2` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/07_LOCKED_DECISIONS.md` | `80949202` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/INDEX.md` | `2f51edb1` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/_SECTION_N.md` | `9a10a1de` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/DOA_BRIEF_F-TMP-001.md` | `096f92d2` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/DOCCFG_BRIEF_F-TMP-001.md` | `63db2673` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/ITRS.doa.yaml` | `0e0414be` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/ITRS.doccfg.yaml` | `25cd8d47` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/ITRS.mdoc.yaml` | `0cdc4547` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/ITRS.ntf.yaml` | `258e3012` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/MDOC_BRIEF_ITRS.md` | `c919eb83` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/NTF_BRIEF_F-TMP-001.md` | `bdd185bf` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-001.md` | `f324e018` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `8555d9f7` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `1b2f2bfd` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-001.md` | `096f92d2` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-001.md` | `63db2673` | doccfg_brief |
| `05_Governance/ITRS.doa.yaml` | `0e0414be` | doa_yaml |
| `05_Governance/ITRS.doccfg.yaml` | `25cd8d47` | doccfg_yaml |
| `05_Governance/ITRS.mdoc.yaml` | `0cdc4547` | mdoc_yaml |
| `05_Governance/ITRS.ntf.yaml` | `258e3012` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_ITRS.md` | `c919eb83` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-001.md` | `bdd185bf` | ntf_brief |
| `05_Governance/decisions.yaml` | `a208eeab` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-001.md` | `286e3542` | qa_audit |
| `06_Test/cases.json` | `51da403f` | cases_json |
| `06_Test/testcase-F-TMP-001.html` | `aad5e3d3` | testcases_uat |
| `06_Test/testcases-F-TMP-001.md` | `5edb795d` | testcases_ai |
| `07_Print/ITRS_print-spec.md` | `d3ead028` | print_spec |
| `07_Print/ITRS_template.html` | `95deba41` | print_extra_itrs_template |
| `07_Print/approved-doa6steps.data.json` | `48a9fd6b` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `2a7a8d20` | print_data_approved_data |
| `07_Print/draft.data.json` | `a9b32a18` | print_data_draft_data |
| `07_Print/form.tpl.html` | `03d16f92` | print_template |
| `07_Print/long-text.data.json` | `1079f57b` | print_data_long_text_data |
| `07_Print/print_config.json` | `d85969be` | print_config |
| `07_Print/profile.json` | `7d007449` | print_profile |
| `07_Print/rejected.data.json` | `0e88bb12` | print_data_rejected_data |
| `08_Reference/1. FM-ITS-01 แบบฟอร์มขอรับบริการด้านเทคโนโลยีสารสนเทศ.xlsx` | `1daa5b62` | original_1_fm_its_01 |
| `08_Reference/FORM_SPEC.check.json` | `fea0d4bb` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `a5681320` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-001.html` | `b5a26b38` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-001_v2.md` | `eafe00a6` | prebrief |
| `08_Reference/RUN_LOG.md` | `bd2e5516` | run_log |
| `08_Reference/SAMPLE.pdf` | `56c56376` | original_sample |
| `08_Reference/page-1.png` | `5a59868a` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `9a10a1de` | report_frd_lint |
