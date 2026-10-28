# F-TMP-003 DevPack — แบบฟอร์มขออนุญาตเข้าพื้นที่สำนักงาน (REQ-TMP-003)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 15 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 47 เคส
- ไม่มี report e2e_standard (html-generator v9.2 #111)

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
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 8 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ลูกค้ายืนยัน DEC AI-DEFAULT 11 ข้อ (ใบลงนาม) ก่อน UAT
- OQ-02 · host ไม่มีผู้บังคับบัญชา → ใครพิจารณา · role-line-manager ยังไม่อยู่ใน DOA master (14 role)
- OQ-03 · ตัวชี้วัด
- OQ-04 · ใบที่อนุมัติแล้วยกเลิกได้หรือไม่
- OQ-05 · ส่งต่อจุดรับแขก/ระบบแลกบัตร (รอบถัดไป)
- OQ-06 · function_code Taxonomy ของ VAR (F01 ชั่วคราว) · รหัส feature/REQ จริง
- OQ-07 · ถ้อยคำยินยอม PDPA บนแบบฟอร์ม
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-line-manager · วงเง
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "บริษัท ครีเดนซ์ จำกัด (มหาชน) / บริษัท ครีเดนซ์ จำกัด" 
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส VAR
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `724c1943` | prototype |
| `02_BRD/BRD_F-TMP-003.docx` | `10d1d847` | brd_docx |
| `02_BRD/BRD_F-TMP-003.md` | `713d81ff` | brd |
| `03_FRD/FRD_F-TMP-003_Pack/00_OVERVIEW.md` | `1fd8dbe3` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/01_UI.md` | `040e0a85` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/02_API.md` | `e5984c42` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/03_LOGIC.md` | `99985af8` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/04_DB.md` | `041b2653` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/05_RULES.md` | `94c659b2` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/06_TESTS.md` | `b059cbe0` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/07_LOCKED_DECISIONS.md` | `4a8c05cd` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/INDEX.md` | `c750d186` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/_SECTION_N.md` | `42c650dd` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/DOA_BRIEF_F-TMP-003.md` | `bb593754` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/DOCCFG_BRIEF_F-TMP-003.md` | `a1b6caf3` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/MDOC_BRIEF_VAR.md` | `a6f41a72` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/NTF_BRIEF_F-TMP-003.md` | `72e5e686` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/VAR.doa.yaml` | `19a1ff8b` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/VAR.doccfg.yaml` | `82cdd273` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/VAR.mdoc.yaml` | `66c988be` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/VAR.ntf.yaml` | `fe46042e` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-003.md` | `40272383` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `e3ff150c` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `3fbe75f1` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-003.md` | `bb593754` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-003.md` | `a1b6caf3` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_VAR.md` | `a6f41a72` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-003.md` | `72e5e686` | ntf_brief |
| `05_Governance/VAR.doa.yaml` | `19a1ff8b` | doa_yaml |
| `05_Governance/VAR.doccfg.yaml` | `82cdd273` | doccfg_yaml |
| `05_Governance/VAR.mdoc.yaml` | `66c988be` | mdoc_yaml |
| `05_Governance/VAR.ntf.yaml` | `fe46042e` | ntf_yaml |
| `05_Governance/decisions.yaml` | `5d394bba` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-003.md` | `31596fa5` | qa_audit |
| `06_Test/cases.json` | `94cf5650` | cases_json |
| `06_Test/testcase-F-TMP-003.html` | `95b28fd5` | testcases_uat |
| `06_Test/testcases-F-TMP-003.md` | `248792e5` | testcases_ai |
| `07_Print/VAR_print-spec.md` | `807a0d5b` | print_spec |
| `07_Print/VAR_template.html` | `b9e0de0e` | print_extra_var_template |
| `07_Print/approved-doa6steps.data.json` | `18075933` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `89dd0a16` | print_data_approved_data |
| `07_Print/draft.data.json` | `eb5a59d5` | print_data_draft_data |
| `07_Print/form.tpl.html` | `b272bdb3` | print_template |
| `07_Print/long-3steps.data.json` | `cd85797d` | print_data_long_3steps_data |
| `07_Print/print_config.json` | `5a97a375` | print_config |
| `07_Print/profile.json` | `9caadaa2` | print_profile |
| `07_Print/rejected.data.json` | `adf3e8b0` | print_data_rejected_data |
| `08_Reference/FORM_SPEC.check.json` | `77acbf84` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `d7715260` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-003.html` | `8eb54f1f` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-003_v2.md` | `f4a225a5` | prebrief |
| `08_Reference/RUN_LOG.md` | `601641f5` | run_log |
| `08_Reference/SAMPLE.pdf` | `acbf5853` | original_sample |
| `08_Reference/page-1.png` | `1256f0bd` | original_page_1 |
| `08_Reference/แบบฟอร์มขออนุญาตเข้าพื้นที่สำนักงาน.docx` | `d2ac4f36` | original_ |
