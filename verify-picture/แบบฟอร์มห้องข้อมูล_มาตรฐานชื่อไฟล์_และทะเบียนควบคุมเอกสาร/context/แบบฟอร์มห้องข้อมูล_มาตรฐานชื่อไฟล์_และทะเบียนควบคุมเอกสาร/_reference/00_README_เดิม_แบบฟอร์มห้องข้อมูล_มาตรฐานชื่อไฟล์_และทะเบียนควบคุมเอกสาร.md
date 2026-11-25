# F-TMP-006 DevPack — แบบฟอร์มห้องข้อมูล มาตรฐานชื่อไฟล์ และทะเบียนควบคุมเอกสาร (REQ-TMP-006)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 22 ข้อ (AI-DEFAULT 14) · พร้อมเริ่มทำ
- test case AI 43 เคส
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
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "วันที่_ชื่อเอกสาร_ฉบับ_สถานะ" → FileNamingPolicy.patter
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: โครงสร้างโฟลเดอร์ห้องข้อมูล: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 8 แถวตามกระดาษ
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ทะเบียนสถานะเอกสารและประวัติฉบับ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 5 แถวตามกระดา
- DEC-07 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: การเปลี่ยนแปลงเอกสาร: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 5 แถวตามกระดาษ
- DEC-08 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: บันทึกสิทธิการเข้าถึงข้อมูล: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 5 แถวตามกระดาษ
- DEC-09 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · เพิ่ม: ชื่อโครงการ / ธุรกรรม (F01 · กระดาษไม่มีช่องระบุโครงก
- DEC-10 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-11 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-12 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-13 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส IVMD
- DEC-14 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `137ac5c1` | prototype |
| `02_BRD/BRD_F-TMP-006.docx` | `cca5a329` | brd_docx |
| `02_BRD/BRD_F-TMP-006.md` | `01d134b6` | brd |
| `03_FRD/FRD_F-TMP-006_Pack/00_OVERVIEW.md` | `eac32a5f` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/01_UI.md` | `ceb78bad` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/02_API.md` | `57af07ae` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/03_LOGIC.md` | `15d7598f` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/04_DB.md` | `f40dc99f` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/05_RULES.md` | `0f9d5e3d` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/06_TESTS.md` | `ba2cb7af` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/07_LOCKED_DECISIONS.md` | `68daa9a6` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/INDEX.md` | `79d4fcaf` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/_SECTION_N.md` | `c5f28727` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/DOA_BRIEF_F-TMP-006.md` | `2ca6cd68` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/DOCCFG_BRIEF_F-TMP-006.md` | `32315786` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/IVMD.doa.yaml` | `306cdee0` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/IVMD.doccfg.yaml` | `f71b36f7` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/IVMD.mdoc.yaml` | `b96187de` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/IVMD.ntf.yaml` | `63138cfc` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/MDOC_BRIEF_IVMD.md` | `ecc2960f` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/NTF_BRIEF_F-TMP-006.md` | `0b9d3c3c` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-006.md` | `b68b99a9` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `909b95f2` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `ec3bf4f7` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-006.md` | `2ca6cd68` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-006.md` | `32315786` | doccfg_brief |
| `05_Governance/IVMD.doa.yaml` | `306cdee0` | doa_yaml |
| `05_Governance/IVMD.doccfg.yaml` | `f71b36f7` | doccfg_yaml |
| `05_Governance/IVMD.mdoc.yaml` | `b96187de` | mdoc_yaml |
| `05_Governance/IVMD.ntf.yaml` | `63138cfc` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_IVMD.md` | `ecc2960f` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-006.md` | `0b9d3c3c` | ntf_brief |
| `05_Governance/decisions.yaml` | `31235253` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-006.md` | `0c3f1a64` | qa_audit |
| `06_Test/cases.json` | `9877d697` | cases_json |
| `06_Test/testcase-F-TMP-006.html` | `fb49c43c` | testcases_uat |
| `06_Test/testcases-F-TMP-006.md` | `74a10a7c` | testcases_ai |
| `07_Print/R1.data.json` | `716a2317` | print_data_r1_data |
| `07_Print/approved-doa6steps.data.json` | `20a82f37` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `4bbec396` | print_data_approved_data |
| `07_Print/draft.data.json` | `4a858075` | print_data_draft_data |
| `07_Print/form.tpl.html` | `d4de7239` | print_template |
| `07_Print/long-10folders-8docs-7changes-8access.data.json` | `613e97ac` | print_data_long_10folders_8docs_7changes_8access_da |
| `07_Print/print_config.json` | `a1c30fbd` | print_config |
| `07_Print/profile.json` | `31c51880` | print_profile |
| `07_Print/rejected.data.json` | `caffe32b` | print_data_rejected_data |
| `07_Print/แบบฟอร์มห้องข้อมูล มาตรฐานชื่อไฟล์ และทะเบียนควบคุมเอกสาร_print-spec.md` | `88bcb6c6` | print_spec |
| `07_Print/แบบฟอร์มห้องข้อมูล มาตรฐานชื่อไฟล์ และทะเบียนควบคุมเอกสาร_template.html` | `94967043` | print_extra_template |
| `08_Reference/4. FM-IVM-04 แบบฟอร์มห้องข้อมูล มาตรฐานชื่อไฟล์ และทะเบียนควบคุมเอกสาร.xlsx` | `60d74ad1` | original_4_fm_ivm_04 |
| `08_Reference/FORM_SPEC.check.json` | `812447ff` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `664813ca` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-006.html` | `7d0ec4f1` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-006_v2.md` | `8076a931` | prebrief |
| `08_Reference/RUN_LOG.md` | `9f3edfb0` | run_log |
| `08_Reference/SAMPLE.pdf` | `28754c38` | original_sample |
| `08_Reference/page-1.png` | `05c3f8de` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `c5f28727` | report_frd_lint |
