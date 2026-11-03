# F-TMP-002 DevPack — บันทึกภายใน (REQ-TMP-002)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 15 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 37 เคส
- ไม่มี report e2e_standard (html-generator v9.2 #111)
- frd_lint BLOCK 0
- anchor ที่ไม่พบบนจอ 0

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
| `02_BRD` | BRD | 1 |
| `03_FRD` | FRD Pack | 9 |
| `04_UI_Brief` | UI Brief AS-BUILT | 1 |
| `05_Governance` | มติ (DECISIONS) + ใบประกาศ DOCCFG / DOA / MDOC / NTF | 11 |
| `06_Test` | test case AI + UAT ฉบับคน + QA audit | 3 |
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 10 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 9 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-compliance · วงเงิน
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส MEM
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `b8fefa13` | prototype |
| `02_BRD/BRD_F-TMP-002.md` | `13a85066` | brd |
| `03_FRD/FRD_F-TMP-002_Pack/00_OVERVIEW.md` | `4f22270f` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/01_UI.md` | `70ff0381` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/02_API.md` | `07c0a79e` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/03_LOGIC.md` | `c01767a2` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/04_DB.md` | `f64a41b1` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/05_RULES.md` | `a285b0eb` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/06_TESTS.md` | `edc293c3` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/07_LOCKED_DECISIONS.md` | `84e4f307` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/INDEX.md` | `b1b70549` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-002.md` | `937b7506` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `80ade1a5` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `d2bd7bbd` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-002.md` | `be3d9568` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-002.md` | `a3121709` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_MEM.md` | `27251041` | mdoc_brief |
| `05_Governance/MEM.doa.yaml` | `54512f2e` | doa_yaml |
| `05_Governance/MEM.doccfg.yaml` | `aad3e495` | doccfg_yaml |
| `05_Governance/MEM.mdoc.yaml` | `8d4f92f1` | mdoc_yaml |
| `05_Governance/MEM.ntf.yaml` | `8af03f8f` | ntf_yaml |
| `05_Governance/NTF_BRIEF_F-TMP-002.md` | `e59d66ef` | ntf_brief |
| `05_Governance/decisions.yaml` | `0925eaee` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-002.md` | `20da2c86` | qa_audit |
| `06_Test/cases.json` | `4227edd4` | cases_json |
| `06_Test/testcases-F-TMP-002.md` | `11df7eed` | testcases_ai |
| `07_Print/MEM_print-spec.md` | `0f6b0b11` | print_spec |
| `07_Print/MEM_template.html` | `42f74f22` | print_extra_mem_template |
| `07_Print/approved.data.json` | `e81ca400` | print_data_approved_data |
| `07_Print/doa-6steps.data.json` | `14b5a4eb` | print_data_doa_6steps_data |
| `07_Print/draft.data.json` | `3eba756b` | print_data_draft_data |
| `07_Print/form.tpl.html` | `78cade6e` | print_template |
| `07_Print/long-12rows-3signs.data.json` | `24733f8b` | print_data_long_12rows_3signs_data |
| `07_Print/print_config.json` | `7b754c8e` | print_config |
| `07_Print/profile.json` | `29b12296` | print_profile |
| `07_Print/rejected.data.json` | `be0cf24e` | print_data_rejected_data |
| `08_Reference/FORM_SPEC.check.json` | `c4697b7b` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `7483b1a3` | form_spec |
| `08_Reference/PREBRIEF_REQ-TMP-002_v2.md` | `b6744523` | prebrief |
| `08_Reference/RUN_LOG.md` | `2782f5a4` | run_log |
| `08_Reference/SAMPLE.pdf` | `be841436` | original_sample |
| `08_Reference/page-1.png` | `bec2d61d` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `db657c6c` | report_frd_lint |
| `08_Reference/reports/anchors.json` | `3e0d1eb5` | report_anchors |
| `08_Reference/บันทึกภายใน.doc` | `7b4287d9` | original_ |
