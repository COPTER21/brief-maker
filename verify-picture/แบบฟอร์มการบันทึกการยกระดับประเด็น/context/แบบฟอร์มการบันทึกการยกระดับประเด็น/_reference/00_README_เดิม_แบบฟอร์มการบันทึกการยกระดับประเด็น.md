# F-TMP-011 DevPack — แบบฟอร์มการบันทึกการยกระดับประเด็น (REQ-TMP-011)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 18 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
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
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · รหัสการยกระดับ (ESC-001…) 
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: บันทึกการยกระดับประเด็น: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 20 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · เพิ่ม: ชื่อโครงการ / ธุรกรรม (F01 · กระดาษไม่มีช่องระบุโครงก
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส IVMI
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `4e441122` | prototype |
| `02_BRD/BRD_F-TMP-011.docx` | `ea0a52a7` | brd_docx |
| `02_BRD/BRD_F-TMP-011.md` | `9b2d7a47` | brd |
| `03_FRD/FRD_F-TMP-011_Pack/00_OVERVIEW.md` | `f3de521c` | frd_pack |
| `03_FRD/FRD_F-TMP-011_Pack/01_UI.md` | `c67945ef` | frd_pack |
| `03_FRD/FRD_F-TMP-011_Pack/02_API.md` | `b4cea7b5` | frd_pack |
| `03_FRD/FRD_F-TMP-011_Pack/03_LOGIC.md` | `df827d75` | frd_pack |
| `03_FRD/FRD_F-TMP-011_Pack/04_DB.md` | `6e7e417e` | frd_pack |
| `03_FRD/FRD_F-TMP-011_Pack/05_RULES.md` | `773be7fb` | frd_pack |
| `03_FRD/FRD_F-TMP-011_Pack/06_TESTS.md` | `c3ec849c` | frd_pack |
| `03_FRD/FRD_F-TMP-011_Pack/07_LOCKED_DECISIONS.md` | `77feaf3a` | frd_pack |
| `03_FRD/FRD_F-TMP-011_Pack/INDEX.md` | `05361f5c` | frd_pack |
| `03_FRD/FRD_F-TMP-011_Pack/_SECTION_N.md` | `186d9a7f` | frd_pack |
| `03_FRD/FRD_F-TMP-011_Pack/declarations/DOA_BRIEF_F-TMP-011.md` | `cd9245dc` | frd_pack |
| `03_FRD/FRD_F-TMP-011_Pack/declarations/DOCCFG_BRIEF_F-TMP-011.md` | `bd72f70d` | frd_pack |
| `03_FRD/FRD_F-TMP-011_Pack/declarations/IVMI.doa.yaml` | `0a6c2359` | frd_pack |
| `03_FRD/FRD_F-TMP-011_Pack/declarations/IVMI.doccfg.yaml` | `69a927e6` | frd_pack |
| `03_FRD/FRD_F-TMP-011_Pack/declarations/IVMI.mdoc.yaml` | `d8695ee7` | frd_pack |
| `03_FRD/FRD_F-TMP-011_Pack/declarations/IVMI.ntf.yaml` | `a23b1af5` | frd_pack |
| `03_FRD/FRD_F-TMP-011_Pack/declarations/MDOC_BRIEF_IVMI.md` | `67e5f3ac` | frd_pack |
| `03_FRD/FRD_F-TMP-011_Pack/declarations/NTF_BRIEF_F-TMP-011.md` | `3a412d34` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-011.md` | `e477251e` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `6561e5c4` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `0c0c813a` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-011.md` | `cd9245dc` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-011.md` | `bd72f70d` | doccfg_brief |
| `05_Governance/IVMI.doa.yaml` | `0a6c2359` | doa_yaml |
| `05_Governance/IVMI.doccfg.yaml` | `69a927e6` | doccfg_yaml |
| `05_Governance/IVMI.mdoc.yaml` | `d8695ee7` | mdoc_yaml |
| `05_Governance/IVMI.ntf.yaml` | `a23b1af5` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_IVMI.md` | `67e5f3ac` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-011.md` | `3a412d34` | ntf_brief |
| `05_Governance/decisions.yaml` | `16fff9cf` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-011.md` | `6ddb1b1e` | qa_audit |
| `06_Test/cases.json` | `f25989ae` | cases_json |
| `06_Test/testcase-F-TMP-011.html` | `d0927d62` | testcases_uat |
| `06_Test/testcases-F-TMP-011.md` | `57530e2f` | testcases_ai |
| `07_Print/R1.data.json` | `004db09e` | print_data_r1_data |
| `07_Print/approved-doa6steps.data.json` | `ef5399e5` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `b85b2c46` | print_data_approved_data |
| `07_Print/draft.data.json` | `bb92a118` | print_data_draft_data |
| `07_Print/form.tpl.html` | `a6b1d353` | print_template |
| `07_Print/long-24escalations.data.json` | `768e2107` | print_data_long_24escalations_data |
| `07_Print/print_config.json` | `414c4b1e` | print_config |
| `07_Print/profile.json` | `ac4f03ec` | print_profile |
| `07_Print/rejected.data.json` | `ba71906c` | print_data_rejected_data |
| `07_Print/แบบฟอร์มการบันทึกการยกระดับประเด็น_print-spec.md` | `42968eb0` | print_spec |
| `07_Print/แบบฟอร์มการบันทึกการยกระดับประเด็น_template.html` | `9319e87b` | print_extra_template |
| `08_Reference/9. FM-IVM-09 แบบฟอร์มการบันทึกการยกระดับประเด็น.xlsx` | `95292da9` | original_9_fm_ivm_09 |
| `08_Reference/FORM_SPEC.check.json` | `50cca49d` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `6fdadfd4` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-011.html` | `e8244bc7` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-011_v2.md` | `43b31182` | prebrief |
| `08_Reference/RUN_LOG.md` | `f516aecd` | run_log |
| `08_Reference/SAMPLE.pdf` | `0cee5db8` | original_sample |
| `08_Reference/page-1.png` | `95de4d5f` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `186d9a7f` | report_frd_lint |
