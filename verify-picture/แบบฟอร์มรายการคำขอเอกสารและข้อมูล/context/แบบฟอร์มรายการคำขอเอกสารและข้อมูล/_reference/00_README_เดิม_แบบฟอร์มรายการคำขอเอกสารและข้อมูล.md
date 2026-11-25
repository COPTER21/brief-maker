# F-TMP-007 DevPack — แบบฟอร์มรายการคำขอเอกสารและข้อมูล (REQ-TMP-007)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 18 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
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
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 10 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 9 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "DR-001 … DR-020" → DocRequestPolicy.code_prefix, "ให้ผู
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการคำขอเอกสารและข้อมูล: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 20 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · เพิ่ม: ชื่อโครงการ / ธุรกรรม (F01 · กระดาษไม่มีช่องระบุโครงก
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส IVME
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `cad23fc0` | prototype |
| `02_BRD/BRD_F-TMP-007.docx` | `ed778ea8` | brd_docx |
| `02_BRD/BRD_F-TMP-007.md` | `2f3964fd` | brd |
| `03_FRD/FRD_F-TMP-007_Pack/00_OVERVIEW.md` | `738d4892` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/01_UI.md` | `ec5f5b61` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/02_API.md` | `192d9368` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/03_LOGIC.md` | `6b97cc3a` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/04_DB.md` | `58e726f5` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/05_RULES.md` | `96c37cb2` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/06_TESTS.md` | `7c1f236c` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/07_LOCKED_DECISIONS.md` | `342a902c` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/INDEX.md` | `3f8c04f1` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/_SECTION_N.md` | `fc428b2b` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/DOA_BRIEF_F-TMP-007.md` | `9f5fcd60` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/DOCCFG_BRIEF_F-TMP-007.md` | `51b572c1` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/IVME.doa.yaml` | `6b3bb26d` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/IVME.doccfg.yaml` | `323b54b0` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/IVME.mdoc.yaml` | `ff9f5056` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/IVME.ntf.yaml` | `99c3933a` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/MDOC_BRIEF_IVME.md` | `afc81e9e` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/NTF_BRIEF_F-TMP-007.md` | `c157d992` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-007.md` | `ba520887` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `41dc3b73` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `69dfcdb8` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-007.md` | `9f5fcd60` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-007.md` | `51b572c1` | doccfg_brief |
| `05_Governance/IVME.doa.yaml` | `6b3bb26d` | doa_yaml |
| `05_Governance/IVME.doccfg.yaml` | `323b54b0` | doccfg_yaml |
| `05_Governance/IVME.mdoc.yaml` | `ff9f5056` | mdoc_yaml |
| `05_Governance/IVME.ntf.yaml` | `99c3933a` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_IVME.md` | `afc81e9e` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-007.md` | `c157d992` | ntf_brief |
| `05_Governance/decisions.yaml` | `1bf2850c` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-007.md` | `a8a6b736` | qa_audit |
| `06_Test/cases.json` | `55dc2c6e` | cases_json |
| `06_Test/testcase-F-TMP-007.html` | `bb079b87` | testcases_uat |
| `06_Test/testcases-F-TMP-007.md` | `f7ffc77c` | testcases_ai |
| `07_Print/approved-doa6steps.data.json` | `17c8b25d` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `f7fa985a` | print_data_approved_data |
| `07_Print/draft.data.json` | `1a8e1b24` | print_data_draft_data |
| `07_Print/form.tpl.html` | `04bb6cae` | print_template |
| `07_Print/long-28requests.data.json` | `95ca3cc0` | print_data_long_28requests_data |
| `07_Print/print_config.json` | `37f74cb5` | print_config |
| `07_Print/profile.json` | `2a19c88e` | print_profile |
| `07_Print/rejected.data.json` | `aad18a0b` | print_data_rejected_data |
| `07_Print/แบบฟอร์มรายการคำขอเอกสารและข้อมูล_print-spec.md` | `d462787a` | print_spec |
| `07_Print/แบบฟอร์มรายการคำขอเอกสารและข้อมูล_template.html` | `ce77ba50` | print_extra_template |
| `08_Reference/5. FM-IVM-05 แบบฟอร์มรายการคำขอเอกสารและข้อมูล.xlsx` | `d6a8428c` | original_5_fm_ivm_05 |
| `08_Reference/FORM_SPEC.check.json` | `7f8cf5c2` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `20ae3c4a` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-007.html` | `be9c8584` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-007_v2.md` | `676bba6e` | prebrief |
| `08_Reference/RUN_LOG.md` | `fe96c0e5` | run_log |
| `08_Reference/SAMPLE.pdf` | `d502e9fd` | original_sample |
| `08_Reference/page-1.png` | `b493bd09` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `fc428b2b` | report_frd_lint |
