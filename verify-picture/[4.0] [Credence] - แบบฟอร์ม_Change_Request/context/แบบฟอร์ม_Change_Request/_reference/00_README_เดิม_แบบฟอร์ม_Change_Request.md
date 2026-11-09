# F-TMP-005 DevPack — แบบฟอร์ม Change Request (REQ-TMP-005)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 17 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 61 เคส
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
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 9 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · วันที่ต้องการส่งมอบ ต้องไม
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส ITCR
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `8d9fb84b` | prototype |
| `02_BRD/BRD_F-TMP-005.docx` | `52e7ac9b` | brd_docx |
| `02_BRD/BRD_F-TMP-005.md` | `c60971ff` | brd |
| `03_FRD/FRD_F-TMP-005_Pack/00_OVERVIEW.md` | `77813cd8` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/01_UI.md` | `c753b4bf` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/02_API.md` | `76abb8b2` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/03_LOGIC.md` | `674a48b6` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/04_DB.md` | `93e92f52` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/05_RULES.md` | `fdbc98c5` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/06_TESTS.md` | `3e4e327a` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/07_LOCKED_DECISIONS.md` | `206e7b30` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/INDEX.md` | `4f006584` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/DOA_BRIEF_F-TMP-005.md` | `12028ac1` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/DOCCFG_BRIEF_F-TMP-005.md` | `565c4101` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/ITCR.doa.yaml` | `2a065e46` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/ITCR.doccfg.yaml` | `64b24c46` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/ITCR.mdoc.yaml` | `fd0167eb` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/ITCR.ntf.yaml` | `c59c8a65` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/MDOC_BRIEF_ITCR.md` | `a0c7cf53` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/NTF_BRIEF_F-TMP-005.md` | `1aca05ab` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-005.md` | `05d264a6` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `2cccf1e9` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `9c1e0125` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-005.md` | `12028ac1` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-005.md` | `565c4101` | doccfg_brief |
| `05_Governance/ITCR.doa.yaml` | `2a065e46` | doa_yaml |
| `05_Governance/ITCR.doccfg.yaml` | `64b24c46` | doccfg_yaml |
| `05_Governance/ITCR.mdoc.yaml` | `fd0167eb` | mdoc_yaml |
| `05_Governance/ITCR.ntf.yaml` | `c59c8a65` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_ITCR.md` | `a0c7cf53` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-005.md` | `1aca05ab` | ntf_brief |
| `05_Governance/decisions.yaml` | `6a260676` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-005.md` | `66291d4b` | qa_audit |
| `06_Test/cases.json` | `f2db0a64` | cases_json |
| `06_Test/testcase-F-TMP-005.html` | `bcd650fb` | testcases_uat |
| `06_Test/testcases-F-TMP-005.md` | `f561e6c3` | testcases_ai |
| `07_Print/ITCR_print-spec.md` | `6663bb92` | print_spec |
| `07_Print/ITCR_template.html` | `9bbdff08` | print_extra_itcr_template |
| `07_Print/approved-doa6steps.data.json` | `94b9878d` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `32991ff9` | print_data_approved_data |
| `07_Print/draft.data.json` | `e595c2d7` | print_data_draft_data |
| `07_Print/form.tpl.html` | `0cb7c7d9` | print_template |
| `07_Print/long-text.data.json` | `b0bcc69f` | print_data_long_text_data |
| `07_Print/print_config.json` | `75505634` | print_config |
| `07_Print/profile.json` | `2cc74c31` | print_profile |
| `07_Print/rejected.data.json` | `0da0f8e8` | print_data_rejected_data |
| `08_Reference/7. FM-ITS-07 แบบฟอร์ม Change Request Form.xlsx` | `7211dc9e` | original_7_fm_its_07_change_request_form |
| `08_Reference/FORM_SPEC.check.json` | `dd5a4cec` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `90de7fe7` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-005.html` | `10e69207` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-005_v2.md` | `6a04d4e7` | prebrief |
| `08_Reference/RUN_LOG.md` | `4cdd81f9` | run_log |
| `08_Reference/SAMPLE.pdf` | `49c9fd49` | original_sample |
| `08_Reference/page-1.png` | `b6741d00` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `a6b98bf8` | report_frd_lint |
