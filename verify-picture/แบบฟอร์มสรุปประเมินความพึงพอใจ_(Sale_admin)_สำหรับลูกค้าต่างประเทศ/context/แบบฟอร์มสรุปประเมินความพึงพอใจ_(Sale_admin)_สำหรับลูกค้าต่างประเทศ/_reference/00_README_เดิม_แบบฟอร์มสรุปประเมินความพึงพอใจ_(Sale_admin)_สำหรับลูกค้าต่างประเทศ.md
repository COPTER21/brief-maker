# F-TMP-007 DevPack — แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าต่างประเทศ (REQ-TMP-007)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 15 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 45 เคส
- e2e_standard 21/21
- frd_lint BLOCK 0
- เทียบต้นฉบับ WARN 0.361

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K9 — เทียบต้นฉบับ WARN 0.361

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
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 13 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 13 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (ประจำเดือน · ≤ 8 ราย · 1 ขั้น · กลับร่าง) · Strike · ก่อน UAT
- OQ-03 · role "Managing Director" ไม่มีใน DOA master (ใช้ role-ceo) · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · SalesConfig.sea_topics/sea_topic_groups/sea_scale ใน Sales Configuration (ร่วม F-TMP-006) · พี่เบิร์ด · ก่อน dev
- OQ-05 · แบบพิมพ์แนวตั้ง 2 หน้า 8 คอลัมน์ แทนต้นฉบับแนวนอน 1 หน้า 4 คอลัมน์ · ลูกค้า · ก่อน UAT
- OQ-06 · กันสร้างซ้ำเดือน / ลูกค้า > 8 ราย · ลูกค้า · –
- OQ-07 · F-TMP-007 / SES / function_code ชั่วคราว · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-ceo · วงเงิน: ไม่มี
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "ความชัดเจนในการสื่อสาร … ความพึงพอใจในบริการ (10 ข้อ · 
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลูกค้าที่ประเมิน (คอลัมน์): สูงสุด 8 แถว · PDF อย่างน้อย 8 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · เพิ่ม: ประจำเดือน
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส SES
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `111de052` | prototype |
| `02_BRD/BRD_F-TMP-007.docx` | `46002e83` | brd_docx |
| `02_BRD/BRD_F-TMP-007.md` | `252d9644` | brd |
| `03_FRD/FRD_F-TMP-007_Pack/00_OVERVIEW.md` | `92d0fa03` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/01_UI.md` | `84a86724` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/02_API.md` | `8d318efb` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/03_LOGIC.md` | `3ce74bbe` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/04_DB.md` | `b930c609` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/05_RULES.md` | `3f83223d` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/06_TESTS.md` | `0bd6a985` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/07_LOCKED_DECISIONS.md` | `d83c245b` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/INDEX.md` | `71308eb8` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/_SECTION_N.md` | `1baba3e0` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/DOA_BRIEF_F-TMP-007.md` | `d21555c3` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/DOCCFG_BRIEF_F-TMP-007.md` | `562e8538` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/MDOC_BRIEF_SES.md` | `c0501dea` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/NTF_BRIEF_F-TMP-007.md` | `73817555` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/SES.doa.yaml` | `a901bc8a` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/SES.doccfg.yaml` | `b889d5d4` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/SES.mdoc.yaml` | `f58e2006` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/SES.ntf.yaml` | `0a21b8ee` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-007.md` | `1c0dc8a6` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `d60e375e` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `97ae5d6d` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-007.md` | `d21555c3` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-007.md` | `562e8538` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_SES.md` | `c0501dea` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-007.md` | `73817555` | ntf_brief |
| `05_Governance/SES.doa.yaml` | `a901bc8a` | doa_yaml |
| `05_Governance/SES.doccfg.yaml` | `b889d5d4` | doccfg_yaml |
| `05_Governance/SES.mdoc.yaml` | `f58e2006` | mdoc_yaml |
| `05_Governance/SES.ntf.yaml` | `0a21b8ee` | ntf_yaml |
| `05_Governance/decisions.yaml` | `3e2689e2` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-007.md` | `ab8e3988` | qa_audit |
| `06_Test/cases.json` | `09b1bfa1` | cases_json |
| `06_Test/testcase-F-TMP-007.html` | `5ead7fbd` | testcases_uat |
| `06_Test/testcases-F-TMP-007.md` | `5e78e9e2` | testcases_ai |
| `07_Print/FM-SAL-23_print-spec.md` | `a31f58fe` | print_spec |
| `07_Print/FM-SAL-23_template.html` | `9596dc2b` | print_extra_fm_sal_23_template |
| `07_Print/approved-doa6steps.data.json` | `a9d446a1` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `753184f3` | print_data_approved_data |
| `07_Print/compare.json` | `3c395bf2` | report_compare |
| `07_Print/compare_side.png` | `cf8c633c` | print_image_compare_side |
| `07_Print/draft.data.json` | `5e2a2de7` | print_data_draft_data |
| `07_Print/form.tpl.html` | `5436f8fb` | print_template |
| `07_Print/long-8customers.data.json` | `3a32b515` | print_data_long_8customers_data |
| `07_Print/print_config.json` | `490b9f11` | print_config |
| `07_Print/profile.json` | `3623e266` | print_profile |
| `07_Print/rejected.data.json` | `bee54a29` | print_data_rejected_data |
| `07_Print/render_data.py` | `2ee07c47` | print_extra_render_data |
| `08_Reference/23. FM-SAL-23 สรุปแบบประเมินความพึงพอใจ  (ต่างประเทศ).docx` | `1d2de4da` | original_23_fm_sal_23 |
| `08_Reference/FORM_SPEC.check.json` | `b2be3679` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `2dd9a4d9` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-007.html` | `cae78df9` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-007_v2.md` | `69681e7c` | prebrief |
| `08_Reference/RUN_LOG.md` | `f9cff495` | run_log |
| `08_Reference/SAMPLE.pdf` | `2a999347` | original_sample |
| `08_Reference/page-1.png` | `d96d51a3` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `1baba3e0` | report_frd_lint |
| `08_Reference/reports/e2e_container_ref.json` | `ac980a99` | report_e2e |
| `08_Reference/shot_pdf.png` | `8b814c7d` | original_shot_pdf |
| `08_Reference/shot_view.png` | `d053377d` | original_shot_view |
| `08_Reference/shot_wizard.png` | `80a0fa68` | original_shot_wizard |
