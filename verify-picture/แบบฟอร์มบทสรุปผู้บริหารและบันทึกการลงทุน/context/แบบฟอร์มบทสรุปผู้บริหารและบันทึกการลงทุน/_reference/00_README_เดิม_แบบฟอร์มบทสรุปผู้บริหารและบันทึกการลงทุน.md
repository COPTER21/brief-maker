# F-TMP-005 DevPack — แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน (REQ-TMP-005)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 16 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 31 เคส
- e2e_standard 21/21
- frd_lint BLOCK 0
- anchor ที่ไม่พบบนจอ 0
- เทียบต้นฉบับ WARN 0.408

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K9 — เทียบต้นฉบับ WARN 0.408

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
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 11 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (11 ข้อ) + เงื่อนไขค้าง = เตือนไม่บล็อก · Strike · ก่อน UAT
- OQ-03 · role กรรมการผู้จัดการ/ผู้มีอำนาจตามตาราง ไม่มีใน DOA master (ใช้ role-gm ชั่วคราว) · ผู้ตรวจสอบ "รองกรรมการผู้จัดการ" ไม่มี role · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · InvestmentMemo config มีหรือยัง / เจ้าของ · พี่เบิร์ด · ก่อน dev
- OQ-05 · ผูกกับโครงการ FM-BDM-01 / ผลคัดกรอง FM-BDM-03 / ส่งต่อ FM-BDM-06 ไหม · ลูกค้า · –
- OQ-06 · ตารางอำนาจอนุมัติตามวงเงิน (ตั้งที่ DOA กลาง) · ลูกค้า · ก่อน wire
- OQ-07 · เงื่อนไขเกิน 20 แถว → PDF หน้า 3 ได้ไหม · ลูกค้า · –
- OQ-08 · รหัส IVM ชนไหม · taxonomy function_code · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "ยังไม่เริ่ม · กำลังดำเนินการ · แล้วเสร็จ · พักงาน" → In
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: เอกสารและเงื่อนไขประกอบ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 6 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส IVM
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `4fab2275` | prototype |
| `02_BRD/BRD_F-TMP-005.docx` | `28020447` | brd_docx |
| `02_BRD/BRD_F-TMP-005.md` | `891c529f` | brd |
| `03_FRD/FRD_F-TMP-005_Pack/00_OVERVIEW.md` | `2eb97104` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/01_UI.md` | `2af40700` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/02_API.md` | `06c7bcd5` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/03_LOGIC.md` | `2e14234d` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/04_DB.md` | `273e15aa` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/05_RULES.md` | `53f1cf6f` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/06_TESTS.md` | `93fcb48d` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/07_LOCKED_DECISIONS.md` | `12d895df` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/INDEX.md` | `db4c9d0f` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/_SECTION_N.md` | `b8f53c54` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/DOA_BRIEF_F-TMP-005.md` | `3956c353` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/DOCCFG_BRIEF_F-TMP-005.md` | `f15f2701` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/IVM.doa.yaml` | `448b905a` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/IVM.doccfg.yaml` | `37fa5abb` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/IVM.mdoc.yaml` | `f8617b62` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/IVM.ntf.yaml` | `c951b79a` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/MDOC_BRIEF_IVM.md` | `1a539bd7` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/NTF_BRIEF_F-TMP-005.md` | `224fd9c9` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-005.md` | `ff251337` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `96b7ebc2` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `f0e92ddd` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-005.md` | `3956c353` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-005.md` | `f15f2701` | doccfg_brief |
| `05_Governance/IVM.doa.yaml` | `448b905a` | doa_yaml |
| `05_Governance/IVM.doccfg.yaml` | `37fa5abb` | doccfg_yaml |
| `05_Governance/IVM.mdoc.yaml` | `f8617b62` | mdoc_yaml |
| `05_Governance/IVM.ntf.yaml` | `c951b79a` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_IVM.md` | `1a539bd7` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-005.md` | `224fd9c9` | ntf_brief |
| `05_Governance/decisions.yaml` | `dad2ba5a` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-005.md` | `a7c6f531` | qa_audit |
| `06_Test/cases.json` | `b2c48652` | cases_json |
| `06_Test/testcase-F-TMP-005.html` | `2ba6149c` | testcases_uat |
| `06_Test/testcases-F-TMP-005.md` | `3311ec46` | testcases_ai |
| `07_Print/FM-BDM-05_template.html` | `d16ac44a` | print_extra_fm_bdm_05_template |
| `07_Print/IVM_print-spec.md` | `f3ac34fd` | print_spec |
| `07_Print/approved-doa6steps.data.json` | `8fcae442` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `5f78fd32` | print_data_approved_data |
| `07_Print/compare.json` | `fe37fd5b` | report_compare |
| `07_Print/compare_overlay.png` | `cc440016` | print_image_compare_overlay |
| `07_Print/compare_side.png` | `a6dbcb3b` | print_image_compare_side |
| `07_Print/draft.data.json` | `bd32ec43` | print_data_draft_data |
| `07_Print/form.tpl.html` | `738eb768` | print_template |
| `07_Print/long-12conditions.data.json` | `b5e0c202` | print_data_long_12conditions_data |
| `07_Print/print_config.json` | `643aacd5` | print_config |
| `07_Print/profile.json` | `1b4c37fb` | print_profile |
| `07_Print/rejected.data.json` | `2db5742c` | print_data_rejected_data |
| `08_Reference/5. FM-BDM-05 แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน.xlsx` | `3ff3dd7b` | original_5_fm_bdm_05 |
| `08_Reference/FORM_SPEC.check.json` | `6a508d6f` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `715e90d7` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-005.html` | `40b10132` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-005_v2.md` | `ed31dfc3` | prebrief |
| `08_Reference/RUN_LOG.md` | `e5c49c1f` | run_log |
| `08_Reference/SAMPLE.pdf` | `bdf87118` | original_sample |
| `08_Reference/page-1.png` | `9999cbe5` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `b8f53c54` | report_frd_lint |
| `08_Reference/reports/anchors.json` | `04049058` | report_anchors |
| `08_Reference/reports/e2e_report.json` | `1db788a8` | report_e2e |
