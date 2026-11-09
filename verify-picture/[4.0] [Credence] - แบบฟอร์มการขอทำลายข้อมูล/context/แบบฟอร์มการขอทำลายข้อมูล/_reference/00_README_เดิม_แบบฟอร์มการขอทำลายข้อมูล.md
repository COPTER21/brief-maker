# F-TMP-003 DevPack — แบบฟอร์มการขอทำลายข้อมูล (REQ-TMP-003)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 17 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
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
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ช่วงเวลาของข้อมูล ถึง ต้อง
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส DRITS
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `2d453429` | prototype |
| `02_BRD/BRD_F-TMP-003.docx` | `81306426` | brd_docx |
| `02_BRD/BRD_F-TMP-003.md` | `7590b210` | brd |
| `03_FRD/FRD_F-TMP-003_Pack/00_OVERVIEW.md` | `23f012bf` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/01_UI.md` | `6120cc5f` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/02_API.md` | `cb4cf15d` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/03_LOGIC.md` | `71b5a67a` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/04_DB.md` | `79f7ad6b` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/05_RULES.md` | `cf71555c` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/06_TESTS.md` | `c7987d6e` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/07_LOCKED_DECISIONS.md` | `259c29b6` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/INDEX.md` | `02883589` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/_SECTION_N.md` | `94614096` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/DOA_BRIEF_F-TMP-003.md` | `4dd4ed19` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/DOCCFG_BRIEF_F-TMP-003.md` | `8344e69c` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/DRITS.doa.yaml` | `e3542545` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/DRITS.doccfg.yaml` | `509d1928` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/DRITS.mdoc.yaml` | `3d28dccb` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/DRITS.ntf.yaml` | `02c576d4` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/MDOC_BRIEF_DRITS.md` | `18d7ed3d` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/NTF_BRIEF_F-TMP-003.md` | `c141a171` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-003.md` | `5faf6277` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `e8962b2e` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `ad471c9d` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-003.md` | `4dd4ed19` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-003.md` | `8344e69c` | doccfg_brief |
| `05_Governance/DRITS.doa.yaml` | `e3542545` | doa_yaml |
| `05_Governance/DRITS.doccfg.yaml` | `509d1928` | doccfg_yaml |
| `05_Governance/DRITS.mdoc.yaml` | `3d28dccb` | mdoc_yaml |
| `05_Governance/DRITS.ntf.yaml` | `02c576d4` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_DRITS.md` | `18d7ed3d` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-003.md` | `c141a171` | ntf_brief |
| `05_Governance/decisions.yaml` | `06b1ebd5` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-003.md` | `78ccf9cf` | qa_audit |
| `06_Test/cases.json` | `dee5bcaf` | cases_json |
| `06_Test/testcase-F-TMP-003.html` | `16dbbbae` | testcases_uat |
| `06_Test/testcases-F-TMP-003.md` | `0bf07a09` | testcases_ai |
| `07_Print/DRITS_print-spec.md` | `2936efd1` | print_spec |
| `07_Print/DRITS_template.html` | `d8671eb6` | print_extra_drits_template |
| `07_Print/approved-doa6steps.data.json` | `6aac6ab2` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `ef2f6d7a` | print_data_approved_data |
| `07_Print/draft.data.json` | `de650fa8` | print_data_draft_data |
| `07_Print/form.tpl.html` | `1619827f` | print_template |
| `07_Print/long-text.data.json` | `4a811d8a` | print_data_long_text_data |
| `07_Print/print_config.json` | `cf140229` | print_config |
| `07_Print/profile.json` | `abf00393` | print_profile |
| `07_Print/rejected.data.json` | `7034a33c` | print_data_rejected_data |
| `08_Reference/2. FM-ITS-02 แบบฟอร์มการขอทำลายข้อมูลเอกสารประจำปี.xlsx` | `bbe0879d` | original_2_fm_its_02 |
| `08_Reference/FORM_SPEC.check.json` | `2d7d7fbb` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `7c3b8ffc` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-003.html` | `1b99e89e` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-003_v2.md` | `bc2a5f3b` | prebrief |
| `08_Reference/RUN_LOG.md` | `d1b1334e` | run_log |
| `08_Reference/SAMPLE.pdf` | `cfb6bca5` | original_sample |
| `08_Reference/page-1.png` | `d8419bfa` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `94614096` | report_frd_lint |
