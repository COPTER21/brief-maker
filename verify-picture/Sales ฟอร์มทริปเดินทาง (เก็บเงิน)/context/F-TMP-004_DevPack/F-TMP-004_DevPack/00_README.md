# F-TMP-004 DevPack — ใบเดินทาง เขตการขาย General Trade (เก็บเงิน) (REQ-TMP-004)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 16 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 33 เคส
- e2e_standard 21/21
- frd_lint BLOCK 0
- เทียบต้นฉบับ WARN 0.362

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K9 — เทียบต้นฉบับ WARN 0.362

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
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 13 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 15 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ยอดรวมทุกคอลัมน์รวมทุกแถวข
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการวันทำงาน: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 31 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส TRV
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `e6d49a00` | prototype |
| `02_BRD/BRD_F-TMP-004.md` | `6caa3383` | brd |
| `03_FRD/FRD_F-TMP-004_Pack/00_OVERVIEW.md` | `90648471` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/01_UI.md` | `d418f6df` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/02_API.md` | `eb88eb2e` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/03_LOGIC.md` | `b5486512` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/04_DB.md` | `45539195` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/05_RULES.md` | `375d1229` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/06_TESTS.md` | `23340541` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/07_LOCKED_DECISIONS.md` | `0ea8d557` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-004.md` | `84ba1180` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `a5efafd7` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `214a0549` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-004.md` | `079260f7` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-004.md` | `49bff405` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_TRV.md` | `42adc091` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-004.md` | `45d6f6cf` | ntf_brief |
| `05_Governance/TRV.doa.yaml` | `c0eeaea4` | doa_yaml |
| `05_Governance/TRV.doccfg.yaml` | `c645141e` | doccfg_yaml |
| `05_Governance/TRV.mdoc.yaml` | `4c6c27a7` | mdoc_yaml |
| `05_Governance/TRV.ntf.yaml` | `c7d515db` | ntf_yaml |
| `05_Governance/decisions.yaml` | `07b0f248` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-004.md` | `cd1c34d6` | qa_audit |
| `06_Test/cases.json` | `850fa44b` | cases_json |
| `06_Test/testcases-F-TMP-004.md` | `a28e8aa1` | testcases_ai |
| `07_Print/TRV_print-spec.md` | `9aa65674` | print_spec |
| `07_Print/TRV_template.html` | `e9cdb6cb` | print_extra_trv_template |
| `07_Print/_states_sheet.png` | `1e56f28d` | print_image_states_sheet |
| `07_Print/approved-doa6steps.data.json` | `411c8a9d` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `b78b32cf` | print_data_approved_data |
| `07_Print/compare.json` | `5ea0732b` | report_compare |
| `07_Print/compare_side.png` | `0d78f70c` | print_image_compare_side |
| `07_Print/draft.data.json` | `986b28aa` | print_data_draft_data |
| `07_Print/form.tpl.html` | `c3da83d5` | print_template |
| `07_Print/long-full31.data.json` | `77123ae0` | print_data_long_full31_data |
| `07_Print/print_config.json` | `ce5d0f7d` | print_config |
| `07_Print/profile.json` | `b1acc3f5` | print_profile |
| `07_Print/rejected.data.json` | `fd73ff0e` | print_data_rejected_data |
| `08_Reference/FORM_SPEC.check.json` | `a522af77` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `e6cadc3b` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-004.html` | `457df8c1` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-004_v2.md` | `c6eb8eff` | prebrief |
| `08_Reference/RUN_LOG.md` | `3a5fa916` | run_log |
| `08_Reference/SAMPLE.pdf` | `3759dfc9` | original_sample |
| `08_Reference/approved-doa6steps.pdf` | `5a315963` | original_approved_doa6steps |
| `08_Reference/approved.pdf` | `3e48ba13` | original_approved |
| `08_Reference/draft.pdf` | `9d161af7` | original_draft |
| `08_Reference/long-full31.pdf` | `a3e24486` | original_long_full31 |
| `08_Reference/page-1.png` | `f48271a0` | original_page_1 |
| `08_Reference/rejected.pdf` | `b4590778` | original_rejected |
| `08_Reference/reports/_SECTION_N.md` | `671e97ea` | report_frd_lint |
| `08_Reference/reports/e2e_report.json` | `c66526aa` | report_e2e |
| `08_Reference/ฟอร์มทริปเดินทาง (เก็บเงิน).xlsx` | `4a4d72fc` | original_ |
