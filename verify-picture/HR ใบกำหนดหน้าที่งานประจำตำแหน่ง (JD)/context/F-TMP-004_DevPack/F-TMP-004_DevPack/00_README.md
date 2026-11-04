# F-TMP-004 DevPack — ใบกำหนดหน้าที่งานประจำตำแหน่ง (JD) (REQ-TMP-004)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 17 ข้อ (AI-DEFAULT 12) · พร้อมเริ่มทำ
- test case AI 54 เคส
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
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 15 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ลูกค้ายืนยัน DEC AI-DEFAULT 12 ข้อ (ใบลงนาม) ก่อน UAT
- OQ-02 · ผู้อนุมัติค่าเริ่ม role-line-manager (ยังไม่อยู่ใน DOA master 14 role) หรือ role-mgr-hr
- OQ-03 · ตัวชี้วัด
- OQ-04 · function_code Taxonomy ของ JD (F01 ชั่วคราว)
- OQ-05 · รหัส feature จริง + เลข REQ จริง · Position master มีชื่ออังกฤษหรือไม่
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-line-manager · วงเง
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ชื่อตำแหน่ง (ไทย) / แผนก /
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ผู้บังคับบัญชาโดยตรง(หัวหน้า): ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 3 แถวตามกระดาษ
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ผู้ใต้บังคับบัญชาโดยตรง(ลูกน้อง): ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 3 แถวตามกระดา
- DEC-07 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-08 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-09 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-10 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-11 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส JD
- DEC-12 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `9ea79413` | prototype |
| `02_BRD/BRD_F-TMP-004.docx` | `71d4ee29` | brd_docx |
| `02_BRD/BRD_F-TMP-004.md` | `55d4d8de` | brd |
| `03_FRD/FRD_F-TMP-004_Pack/00_OVERVIEW.md` | `9482fa8e` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/01_UI.md` | `167a9e25` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/02_API.md` | `69c9e197` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/03_LOGIC.md` | `4881c215` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/04_DB.md` | `f8985e11` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/05_RULES.md` | `ce9641a6` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/06_TESTS.md` | `0cdd9c17` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/07_LOCKED_DECISIONS.md` | `23bef386` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/INDEX.md` | `30b46cab` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/_SECTION_N.md` | `b836078b` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/DOA_BRIEF_F-TMP-004.md` | `79469773` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/DOCCFG_BRIEF_F-TMP-004.md` | `7bcd16c1` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/JD.doa.yaml` | `3bfab380` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/JD.doccfg.yaml` | `cc5863c4` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/JD.mdoc.yaml` | `fadf4877` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/JD.ntf.yaml` | `c34dcf3a` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/MDOC_BRIEF_JD.md` | `948542a6` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/NTF_BRIEF_F-TMP-004.md` | `715bf951` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-004.md` | `1871a0c8` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `9d7ab4b7` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `bed5a0d6` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-004.md` | `79469773` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-004.md` | `7bcd16c1` | doccfg_brief |
| `05_Governance/JD.doa.yaml` | `3bfab380` | doa_yaml |
| `05_Governance/JD.doccfg.yaml` | `cc5863c4` | doccfg_yaml |
| `05_Governance/JD.mdoc.yaml` | `fadf4877` | mdoc_yaml |
| `05_Governance/JD.ntf.yaml` | `c34dcf3a` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_JD.md` | `948542a6` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-004.md` | `715bf951` | ntf_brief |
| `05_Governance/decisions.yaml` | `a9983cf3` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-004.md` | `aa9dc9a7` | qa_audit |
| `06_Test/cases.json` | `00145f9d` | cases_json |
| `06_Test/testcase-F-TMP-004.html` | `23cf57a6` | testcases_uat |
| `06_Test/testcases-F-TMP-004.md` | `d9a0b2f1` | testcases_ai |
| `07_Print/JD_print-spec.md` | `c2b76578` | print_spec |
| `07_Print/JD_states_sheet.png` | `0a6cf55f` | print_image_jd_states_sheet |
| `07_Print/JD_template.html` | `e822fff3` | print_extra_jd_template |
| `07_Print/approved-doa6steps.data.json` | `65c30fac` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `16582fea` | print_data_approved_data |
| `07_Print/draft.data.json` | `ea8935df` | print_data_draft_data |
| `07_Print/form.tpl.html` | `2aea1c8b` | print_template |
| `07_Print/long-12rows.data.json` | `58bf50d2` | print_data_long_12rows_data |
| `07_Print/print_config.json` | `d4e9902e` | print_config |
| `07_Print/profile.json` | `a5b12152` | print_profile |
| `07_Print/rejected.data.json` | `dc79be75` | print_data_rejected_data |
| `08_Reference/FORM_SPEC.check.json` | `20c4042a` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `e2fcb651` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-004.html` | `49d5ef04` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-004_v2.md` | `8ce1c986` | prebrief |
| `08_Reference/RUN_LOG.md` | `f7719eb3` | run_log |
| `08_Reference/SAMPLE.pdf` | `f1f27522` | original_sample |
| `08_Reference/page-1.png` | `a8328bbe` | original_page_1 |
| `08_Reference/page-2.png` | `ed2ec1e2` | original_page_2 |
| `08_Reference/reports/_SECTION_N.md` | `b836078b` | report_frd_lint |
| `08_Reference/shot_detail_sandbox.png` | `d75cf636` | original_shot_detail_sandbox |
| `08_Reference/shot_list_sandbox.png` | `de31adbe` | original_shot_list_sandbox |
| `08_Reference/shot_pdf_sandbox.png` | `74fe7adb` | original_shot_pdf_sandbox |
| `08_Reference/shot_sign_sandbox.png` | `ec6a43f8` | original_shot_sign_sandbox |
| `08_Reference/shot_wiz_sandbox.png` | `74fad2ab` | original_shot_wiz_sandbox |
| `08_Reference/ใบกำหนดหน้าที่งานประจำตำแหน่ง (JD).docx` | `8d64eef9` | original_jd |
