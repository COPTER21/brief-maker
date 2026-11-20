# F-TMP-001 DevPack — แบบฟอร์มบันทึกภาพรวมและเริ่มต้นโครงการ (REQ-TMP-001)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 15 ข้อ (AI-DEFAULT 12) · พร้อมเริ่มทำ
- test case AI 36 เคส
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
| `02_BRD` | BRD | 2 |
| `03_FRD` | FRD Pack | 18 |
| `04_UI_Brief` | UI Brief AS-BUILT | 1 |
| `05_Governance` | มติ (DECISIONS) + ใบประกาศ DOCCFG / DOA / MDOC / NTF | 11 |
| `06_Test` | test case AI + UAT ฉบับคน + QA audit | 4 |
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 10 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 11 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT 12 ข้อ · Strike · ก่อน UAT
- OQ-03 · role ผู้ตรวจสอบ (ผู้จัดการฝ่ายพัฒนาธุรกิจ) · ผู้อนุมัติ/รับทราบ (รองกรรมการผู้จัดการ/กรรมการผู้จัดการ) ไม่มีใน DOA master · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · ตัวเลือกระดับความสำคัญ (สูง/กลาง/ต่ำ = AI-DEFAULT) · ลูกค้า · ก่อน dev
- OQ-05 · module Business Development · รหัส feature จริง · taxonomy function_code (MDOC ใช้ F01 ชั่วคราว) · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · วันที่เป้าหมาย ≥ วันที่เริ
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: แผนงานเบื้องต้น: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 6 แถวตามกระดาษ
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ประวัติการแก้ไข: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 1 แถวตามกระดาษ
- DEC-07 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ) · รวม/แยก: วันที่เริ่มต้น / วัน
- DEC-08 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-09 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-10 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-11 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส PJI
- DEC-12 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `b63e8390` | prototype |
| `02_BRD/BRD_F-TMP-001.docx` | `ebc24f83` | brd_docx |
| `02_BRD/BRD_F-TMP-001.md` | `4838ef63` | brd |
| `03_FRD/FRD_F-TMP-001_Pack/00_OVERVIEW.md` | `b2342cea` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/01_UI.md` | `07d6cc21` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/02_API.md` | `0e2abb25` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/03_LOGIC.md` | `cbd5817c` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/04_DB.md` | `75521d12` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/05_RULES.md` | `8d83bde8` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/06_TESTS.md` | `b3c1d67d` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/07_LOCKED_DECISIONS.md` | `204c4348` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/INDEX.md` | `35e407ab` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/_SECTION_N.md` | `0476e231` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/DOA_BRIEF_F-TMP-001.md` | `e48f555c` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/DOCCFG_BRIEF_F-TMP-001.md` | `5d8d64b7` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/MDOC_BRIEF_PJI.md` | `cfa5e961` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/NTF_BRIEF_F-TMP-001.md` | `c8139957` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/PJI.doa.yaml` | `3e39c1a9` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/PJI.doccfg.yaml` | `bc5c233c` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/PJI.mdoc.yaml` | `3cfcbf48` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/PJI.ntf.yaml` | `95b5cce4` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-001.md` | `7326f216` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `9969ec8a` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `947eb4c8` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-001.md` | `e48f555c` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-001.md` | `5d8d64b7` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_PJI.md` | `cfa5e961` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-001.md` | `c8139957` | ntf_brief |
| `05_Governance/PJI.doa.yaml` | `3e39c1a9` | doa_yaml |
| `05_Governance/PJI.doccfg.yaml` | `bc5c233c` | doccfg_yaml |
| `05_Governance/PJI.mdoc.yaml` | `3cfcbf48` | mdoc_yaml |
| `05_Governance/PJI.ntf.yaml` | `95b5cce4` | ntf_yaml |
| `05_Governance/decisions.yaml` | `bf402724` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-001.md` | `af04c26e` | qa_audit |
| `06_Test/cases.json` | `7ee92ddd` | cases_json |
| `06_Test/testcase-F-TMP-001.html` | `e2e386c8` | testcases_uat |
| `06_Test/testcases-F-TMP-001.md` | `19de1c8d` | testcases_ai |
| `07_Print/FM-BDM-01_template.html` | `789978a2` | print_extra_fm_bdm_01_template |
| `07_Print/PJI_print-spec.md` | `f5655093` | print_spec |
| `07_Print/approved-doa6steps.data.json` | `c542a66b` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `4b40ac1a` | print_data_approved_data |
| `07_Print/draft.data.json` | `3ddcd25c` | print_data_draft_data |
| `07_Print/form.tpl.html` | `f1a8cd95` | print_template |
| `07_Print/long-14rows.data.json` | `7c1bb073` | print_data_long_14rows_data |
| `07_Print/print_config.json` | `07f27412` | print_config |
| `07_Print/profile.json` | `e453c9b7` | print_profile |
| `07_Print/rejected.data.json` | `e91069e2` | print_data_rejected_data |
| `08_Reference/1. FM-BDM-01 แบบฟอร์มบันทึกภาพรวมและเริ่มต้นโครงการ.xlsx` | `d1b3719b` | original_1_fm_bdm_01 |
| `08_Reference/FORM_SPEC.check.json` | `5acc6f2f` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `a213b970` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-001.html` | `fbadfd62` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-001_v2.md` | `9d58c529` | prebrief |
| `08_Reference/RUN_LOG.md` | `6e77b7a8` | run_log |
| `08_Reference/SAMPLE.pdf` | `f115d5c8` | original_sample |
| `08_Reference/logo.png` | `524e41e9` | original_logo |
| `08_Reference/page-1.png` | `e2d82e55` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `0476e231` | report_frd_lint |
| `08_Reference/reports/anchors.json` | `941c0df4` | report_anchors |
