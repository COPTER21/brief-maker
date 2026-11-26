# F-TMP-003 DevPack — แบบฟอร์มบันทึกการปิดงานและห้องข้อมูล (REQ-TMP-003)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 17 ข้อ (AI-DEFAULT 12) · พร้อมเริ่มทำ
- test case AI 48 เคส
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
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "รายการตรวจสอบ 8 รายการ (ข้อความพิมพ์ตายตัว)" → config: 
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการตรวจสอบการปิดงานและห้องข้อมูล: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 8 แถวตามกร
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: บทเรียนที่ได้รับและการติดตามผล: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 10 แถวตามกระดาษ
- DEC-07 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-08 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-09 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-10 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-11 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส IVMK
- DEC-12 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `8fe0fdca` | prototype |
| `02_BRD/BRD_F-TMP-003.docx` | `443e1874` | brd_docx |
| `02_BRD/BRD_F-TMP-003.md` | `fb40e3f5` | brd |
| `03_FRD/FRD_F-TMP-003_Pack/00_OVERVIEW.md` | `2ac84c9e` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/01_UI.md` | `eccb84c3` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/02_API.md` | `a4e2e949` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/03_LOGIC.md` | `f6cc4df1` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/04_DB.md` | `7278d353` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/05_RULES.md` | `45876a75` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/06_TESTS.md` | `4fe3a82f` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/07_LOCKED_DECISIONS.md` | `dbeba1f6` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/INDEX.md` | `e1367e86` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/_SECTION_N.md` | `fab8f716` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/DOA_BRIEF_F-TMP-003.md` | `a566f2f2` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/DOCCFG_BRIEF_F-TMP-003.md` | `cdf40618` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/IVMK.doa.yaml` | `55f48d65` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/IVMK.doccfg.yaml` | `e6c59656` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/IVMK.mdoc.yaml` | `b65ac45d` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/IVMK.ntf.yaml` | `700ddde9` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/MDOC_BRIEF_IVMK.md` | `84036df1` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/NTF_BRIEF_F-TMP-003.md` | `29ad4173` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-003.md` | `ac6a6711` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `c5bb1b8c` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `0615fc53` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-003.md` | `a566f2f2` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-003.md` | `cdf40618` | doccfg_brief |
| `05_Governance/IVMK.doa.yaml` | `55f48d65` | doa_yaml |
| `05_Governance/IVMK.doccfg.yaml` | `e6c59656` | doccfg_yaml |
| `05_Governance/IVMK.mdoc.yaml` | `b65ac45d` | mdoc_yaml |
| `05_Governance/IVMK.ntf.yaml` | `700ddde9` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_IVMK.md` | `84036df1` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-003.md` | `29ad4173` | ntf_brief |
| `05_Governance/decisions.yaml` | `fdeb2b54` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-003.md` | `15c70f88` | qa_audit |
| `06_Test/cases.json` | `beb478e3` | cases_json |
| `06_Test/testcase-F-TMP-003.html` | `30e57cc7` | testcases_uat |
| `06_Test/testcases-F-TMP-003.md` | `8e904105` | testcases_ai |
| `07_Print/approved-doa6steps.data.json` | `60530bb7` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `9c7cfe05` | print_data_approved_data |
| `07_Print/draft.data.json` | `32ad369b` | print_data_draft_data |
| `07_Print/form.tpl.html` | `e7f58b62` | print_template |
| `07_Print/long-14lessons.data.json` | `01b1fc8c` | print_data_long_14lessons_data |
| `07_Print/print_config.json` | `1736a41e` | print_config |
| `07_Print/profile.json` | `b56d2eb0` | print_profile |
| `07_Print/rejected.data.json` | `9df86e85` | print_data_rejected_data |
| `07_Print/แบบฟอร์มบันทึกการปิดงานและห้องข้อมูล_print-spec.md` | `a5753984` | print_spec |
| `07_Print/แบบฟอร์มบันทึกการปิดงานและห้องข้อมูล_template.html` | `5705d7a3` | print_extra_template |
| `08_Reference/11. FM-IVM-11 แบบฟอร์มบันทึกการปิดงานและห้องข้อมูล.xlsx` | `3a1be460` | original_11_fm_ivm_11 |
| `08_Reference/FORM_SPEC.check.json` | `85ebdde5` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `b6fa8457` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-003.html` | `75afeeb3` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-003_v2.md` | `dfc3cdbe` | prebrief |
| `08_Reference/RUN_LOG.md` | `cec71203` | run_log |
| `08_Reference/SAMPLE.pdf` | `2770bb6a` | original_sample |
| `08_Reference/page-1.png` | `e792a7c3` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `fab8f716` | report_frd_lint |
