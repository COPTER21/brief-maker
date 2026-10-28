# F-TMP-005 DevPack — แบบฟอร์มสำรวจสมรรถนะ (REQ-TMP-005)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 0
- มติ 12 ข้อ (AI-DEFAULT 12) · พร้อมเริ่มทำ
- test case AI 30 เคส
- e2e_standard None/0
- frd_lint BLOCK 0
- anchor ที่ไม่พบบนจอ 0

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
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 12 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-line-manager · วงเง
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "1 ต้องพัฒนา (ยังไม่สามารถปฏิบัติได้ตามมาตรฐาน)" → Compe
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สมรรถนะหลัก (Core Competency): ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 5 แถวตามกระดาษ
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สมรรถนะเฉพาะสายงาน (Functional Competency): ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 6 แ
- DEC-07 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-08 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-09 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-10 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-11 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส CMP
- DEC-12 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `f8251e15` | prototype |
| `02_BRD/BRD_F-TMP-005.md` | `963154a0` | brd |
| `03_FRD/FRD_F-TMP-005_Pack/00_OVERVIEW.md` | `e0865b75` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/01_UI.md` | `add8498a` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/02_API.md` | `48b77b9f` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/03_LOGIC.md` | `7f1f261c` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/04_DB.md` | `2775d13b` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/05_RULES.md` | `5962c352` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/06_TESTS.md` | `349939a5` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/07_LOCKED_DECISIONS.md` | `eb418e69` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-005.md` | `2d8dbd8c` | ui_brief |
| `05_Governance/CMP.doa.yaml` | `fa5e211f` | doa_yaml |
| `05_Governance/CMP.doccfg.yaml` | `985ead61` | doccfg_yaml |
| `05_Governance/CMP.mdoc.yaml` | `e3dcba24` | mdoc_yaml |
| `05_Governance/CMP.ntf.yaml` | `5a9a77a1` | ntf_yaml |
| `05_Governance/DECISIONS.lock.json` | `ce7d8bd8` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `73c7a52f` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-005.md` | `4db6ae03` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-005.md` | `5cbae429` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_CMP.md` | `821a0dd7` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-005.md` | `14537652` | ntf_brief |
| `05_Governance/decisions.yaml` | `849f9869` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-005.md` | `48c39d5c` | qa_audit |
| `06_Test/cases.json` | `f16cd082` | cases_json |
| `06_Test/testcases-F-TMP-005.md` | `8c3139c0` | testcases_ai |
| `07_Print/CMP_print-spec.md` | `15504472` | print_spec |
| `07_Print/CMP_template.html` | `956170db` | print_extra_cmp_template |
| `07_Print/approved-doa6steps.data.json` | `9d5464d5` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `6d03e063` | print_data_approved_data |
| `07_Print/draft.data.json` | `06c7f6f8` | print_data_draft_data |
| `07_Print/form.tpl.html` | `a832205d` | print_template |
| `07_Print/long-12rows.data.json` | `58a6d833` | print_data_long_12rows_data |
| `07_Print/print_config.json` | `18d54e67` | print_config |
| `07_Print/profile.json` | `d44e7a93` | print_profile |
| `07_Print/rejected.data.json` | `d0623d8a` | print_data_rejected_data |
| `08_Reference/FORM_SPEC.check.json` | `5446b154` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `ac00b88d` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-005.html` | `11bdb456` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-005_v2.md` | `a57ef0ea` | prebrief |
| `08_Reference/RUN_LOG.md` | `dd12e661` | run_log |
| `08_Reference/SAMPLE.pdf` | `4760103c` | original_sample |
| `08_Reference/page-1.png` | `e1a7c105` | original_page_1 |
| `08_Reference/page-2.png` | `c3e096d4` | original_page_2 |
| `08_Reference/reports/_SECTION_N.md` | `c565f153` | report_frd_lint |
| `08_Reference/reports/anchors.json` | `26e3f25b` | report_anchors |
| `08_Reference/reports/e2e_report.json` | `82ca6e24` | report_e2e |
| `08_Reference/ฟอร์มสำรวจสมรรถนะ.docx` | `5f8830ec` | original_ |
