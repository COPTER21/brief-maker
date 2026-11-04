# F-TMP-001 DevPack — แบบฟอร์มขอใช้รถตู้ (REQ-TMP-001)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 14 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 32 เคส
- e2e_standard None/0
- frd_lint BLOCK 0

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K4 — microcopy ใน FRD 06 ที่ไม่พบใน prototype 3/20: ['อนุมัติ/ไม่อนุมัติ', 'เห็นควร/ไม่เห็นควร', 'ใส่สถานที่และเวลาขากลับให้ครบ']

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
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 11 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · จำนวนวัน = (ถึงวันที่ − วั
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายชื่อผู้เดินทาง: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 5 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส VAN
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `ab9d1917` | prototype |
| `02_BRD/BRD_F-TMP-001.md` | `6c4f38df` | brd |
| `03_FRD/FRD_F-TMP-001_Pack/00_OVERVIEW.md` | `50c2cb1c` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/01_UI.md` | `58a38cd2` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/02_API.md` | `fbffcf2a` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/03_LOGIC.md` | `544b3027` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/04_DB.md` | `615bba5d` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/05_RULES.md` | `d5e77e53` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/06_TESTS.md` | `c701481c` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/07_LOCKED_DECISIONS.md` | `03936227` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-001.md` | `f40832d8` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `1f80044e` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `617b72c2` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-001.md` | `698d2fe8` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-001.md` | `ca7fff14` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_VAN.md` | `5929a3a9` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-001.md` | `8731fea9` | ntf_brief |
| `05_Governance/VAN.doa.yaml` | `3e66b29e` | doa_yaml |
| `05_Governance/VAN.doccfg.yaml` | `3b40c382` | doccfg_yaml |
| `05_Governance/VAN.mdoc.yaml` | `62bb0fc2` | mdoc_yaml |
| `05_Governance/VAN.ntf.yaml` | `70962662` | ntf_yaml |
| `05_Governance/decisions.yaml` | `338e0cdd` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-001.md` | `d0376659` | qa_audit |
| `06_Test/cases.json` | `4c14ac48` | cases_json |
| `06_Test/testcases-F-TMP-001.md` | `2f32faad` | testcases_ai |
| `07_Print/VAN_print-spec.md` | `e48b4e39` | print_spec |
| `07_Print/VAN_template.html` | `94de7f08` | print_extra_van_template |
| `07_Print/approved-doa6steps.data.json` | `9434fb65` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `d7dc14e7` | print_data_approved_data |
| `07_Print/draft.data.json` | `811e85bd` | print_data_draft_data |
| `07_Print/form.tpl.html` | `dfd6af52` | print_template |
| `07_Print/long-12rows-3signs.data.json` | `7731d4f6` | print_data_long_12rows_3signs_data |
| `07_Print/print_config.json` | `1affad71` | print_config |
| `07_Print/profile.json` | `7147cc9d` | print_profile |
| `07_Print/rejected.data.json` | `0b65ba8f` | print_data_rejected_data |
| `08_Reference/FORM_SPEC.check.json` | `f47e0129` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `ff94ff7d` | form_spec |
| `08_Reference/HR แบบฟอร์มขอใช้รถตู้.docx` | `e94d6b82` | original_hr |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-001.html` | `b66992af` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-001_v2.md` | `c4af7b64` | prebrief |
| `08_Reference/RUN_LOG.md` | `a952ae80` | run_log |
| `08_Reference/SAMPLE.pdf` | `383965ca` | original_sample |
| `08_Reference/page-1.png` | `699d49ec` | original_page_1 |
| `08_Reference/page-2.png` | `6569c6ca` | original_page_2 |
| `08_Reference/reports/_SECTION_N.md` | `be5dd06a` | report_frd_lint |
| `08_Reference/reports/e2e_report.json` | `1b9ddbda` | report_e2e |
