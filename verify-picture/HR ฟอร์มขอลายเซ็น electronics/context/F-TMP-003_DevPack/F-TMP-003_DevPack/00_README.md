# F-TMP-003 DevPack — คำขอมีและใช้ลายเซ็นดิจิทัล (Digital Signature) (REQ-TMP-003)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 2
- มติ 17 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 22 เคส
- ไม่มี report e2e_standard (html-generator v9.2 #111)
- frd_lint BLOCK 0

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K3 — run_log: ไฟล์ถูกแก้หลังลงทะเบียน — รัน manifest_scan ใหม่
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
| `02_BRD` | BRD | 1 |
| `03_FRD` | FRD Pack | 8 |
| `04_UI_Brief` | UI Brief AS-BUILT | 1 |
| `05_Governance` | มติ (DECISIONS) + ใบประกาศ DOCCFG / DOA / MDOC / NTF | 11 |
| `06_Test` | test case AI + UAT ฉบับคน + QA audit | 3 |
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 10 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 10 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-mgr-hr · วงเงิน: ไม
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส DSR
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `e850dc94` | prototype |
| `02_BRD/BRD_F-TMP-003.md` | `1b8a6820` | brd |
| `03_FRD/FRD_F-TMP-003_Pack/00_OVERVIEW.md` | `afbca923` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/01_UI.md` | `e07b2c61` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/02_API.md` | `e97c8e0c` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/03_LOGIC.md` | `cfaa7fb7` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/04_DB.md` | `d0412f0d` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/05_RULES.md` | `39eb6d8a` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/06_TESTS.md` | `e68c01df` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/07_LOCKED_DECISIONS.md` | `5515de64` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-003.md` | `adc69707` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `31ce19c8` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `a704b530` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-003.md` | `16c3b833` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-003.md` | `93106d61` | doccfg_brief |
| `05_Governance/DSR.doa.yaml` | `f0711e96` | doa_yaml |
| `05_Governance/DSR.doccfg.yaml` | `1ca00527` | doccfg_yaml |
| `05_Governance/DSR.mdoc.yaml` | `56a54192` | mdoc_yaml |
| `05_Governance/DSR.ntf.yaml` | `cbac33f9` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_DSR.md` | `f5cfc35e` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-003.md` | `b8cb2750` | ntf_brief |
| `05_Governance/decisions.yaml` | `9ecfbd02` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-003.md` | `ee3b2272` | qa_audit |
| `06_Test/cases.json` | `3a66659f` | cases_json |
| `06_Test/testcases-F-TMP-003.md` | `e6530f2f` | testcases_ai |
| `07_Print/DSR_print-spec.md` | `d3ca1814` | print_spec |
| `07_Print/DSR_template.html` | `5f46b5b7` | print_extra_dsr_template |
| `07_Print/approved-doa6steps.data.json` | `4e12ba38` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `bee89c50` | print_data_approved_data |
| `07_Print/draft.data.json` | `47c1ab32` | print_data_draft_data |
| `07_Print/form.tpl.html` | `4317d184` | print_template |
| `07_Print/long-3signs.data.json` | `a8671281` | print_data_long_3signs_data |
| `07_Print/print_config.json` | `bde9fda0` | print_config |
| `07_Print/profile.json` | `dd43cb50` | print_profile |
| `07_Print/rejected.data.json` | `ab4c1400` | print_data_rejected_data |
| `08_Reference/FORM_SPEC.check.json` | `4a59889d` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `3c46194c` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-003.html` | `f6265ef1` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-003_v2.md` | `9e045dac` | prebrief |
| `08_Reference/RUN_LOG.md` | `7fc7cf44` | run_log |
| `08_Reference/SAMPLE.pdf` | `ff5cf379` | original_sample |
| `08_Reference/page-1.png` | `79b5c3f5` | original_page_1 |
| `08_Reference/page-2.png` | `d531bea4` | original_page_2 |
| `08_Reference/reports/_SECTION_N.md` | `5ae082da` | report_frd_lint |
| `08_Reference/ฟอร์มขอลายเซ็น electronics.docx` | `8fcdfc39` | original_electronics |
