# F-TMP-005 DevPack — ใบเป้าหมายการเยี่ยมร้านค้า (REQ-TMP-005)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 18 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 41 เคส
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
- OQ-01 · ลูกค้ายืนยัน DEC AI-DEFAULT 11 ข้อ (ใบลงนาม) ก่อน UAT
- OQ-02 · ผู้อนุมัติขั้น 1 = role-line-manager (ยังไม่อยู่ใน DOA master 14 role) หรือ role-supervisor · ขั้น 2 = role-mgr-sales
- OQ-03 · ตัวชี้วัด
- OQ-04 · function_code Taxonomy ของ SVT (F01 ชั่วคราว)
- OQ-05 · รหัส feature จริง + เลข REQ จริง · "รอบการขาย" = เดือนปฏิทินหรือไม่
- OQ-06 · คอลัมน์ย่อยว่างใต้ "วันทำงาน" ใช้ทำอะไร
- OQ-07 · แบบพิมพ์ A4 แนวนอน — thai-doc v2.1 ยังไม่มี token orientation
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ผู้รับผิดชอบเขต = ผู้สร้าง
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: แผนเยี่ยมรายวัน (วันทำงาน 1–31): สูงสุด 31 แถว · PDF อย่างน้อย 31 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส SVT
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `e17bc259` | prototype |
| `02_BRD/BRD_F-TMP-005.docx` | `76f73629` | brd_docx |
| `02_BRD/BRD_F-TMP-005.md` | `d91a2a15` | brd |
| `03_FRD/FRD_F-TMP-005_Pack/00_OVERVIEW.md` | `79f2af84` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/01_UI.md` | `72493d87` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/02_API.md` | `65cbbc21` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/03_LOGIC.md` | `7b905405` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/04_DB.md` | `174a6bf7` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/05_RULES.md` | `35490bd1` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/06_TESTS.md` | `94655dcc` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/07_LOCKED_DECISIONS.md` | `be3241ce` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/INDEX.md` | `7a977b84` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/_SECTION_N.md` | `2c0a00fe` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/DOA_BRIEF_F-TMP-005.md` | `f58eb769` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/DOCCFG_BRIEF_F-TMP-005.md` | `3edc99c2` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/MDOC_BRIEF_SVT.md` | `a9ae415e` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/NTF_BRIEF_F-TMP-005.md` | `498c311c` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/SVT.doa.yaml` | `1639561c` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/SVT.doccfg.yaml` | `6ee1e120` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/SVT.mdoc.yaml` | `c590c482` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/SVT.ntf.yaml` | `36000ba3` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-005.md` | `0da6b1da` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `3afe64fe` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `bba2b1fb` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-005.md` | `f58eb769` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-005.md` | `3edc99c2` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_SVT.md` | `a9ae415e` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-005.md` | `498c311c` | ntf_brief |
| `05_Governance/SVT.doa.yaml` | `1639561c` | doa_yaml |
| `05_Governance/SVT.doccfg.yaml` | `6ee1e120` | doccfg_yaml |
| `05_Governance/SVT.mdoc.yaml` | `c590c482` | mdoc_yaml |
| `05_Governance/SVT.ntf.yaml` | `36000ba3` | ntf_yaml |
| `05_Governance/decisions.yaml` | `b07a9d02` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-005.md` | `f71d9a90` | qa_audit |
| `06_Test/cases.json` | `c5ff58e1` | cases_json |
| `06_Test/testcase-F-TMP-005.html` | `6dfc5d7b` | testcases_uat |
| `06_Test/testcases-F-TMP-005.md` | `6ae4ea22` | testcases_ai |
| `07_Print/SVT_print-spec.md` | `ca6019bf` | print_spec |
| `07_Print/SVT_template.html` | `02e6e868` | print_extra_svt_template |
| `07_Print/approved-doa6steps.data.json` | `0e3923b8` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `52eb1323` | print_data_approved_data |
| `07_Print/draft.data.json` | `7d6edf97` | print_data_draft_data |
| `07_Print/form.tpl.html` | `b8534df8` | print_template |
| `07_Print/long-31rows.data.json` | `a48bae27` | print_data_long_31rows_data |
| `07_Print/print_config.json` | `003c4f7a` | print_config |
| `07_Print/profile.json` | `e135e7df` | print_profile |
| `07_Print/rejected.data.json` | `dc34f235` | print_data_rejected_data |
| `08_Reference/FORM_SPEC.check.json` | `0be73356` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `1ba6a3b2` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-005.html` | `4452b678` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-005_v2.md` | `0b106f71` | prebrief |
| `08_Reference/RUN_LOG.md` | `a560b1b6` | run_log |
| `08_Reference/SAMPLE.pdf` | `e2f7ec28` | original_sample |
| `08_Reference/page-1.png` | `ca817c46` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `2c0a00fe` | report_frd_lint |
| `08_Reference/ใบเป้าหมายการเยี่ยมร้านค้า.xlsx` | `5cde8bf7` | original_ |
