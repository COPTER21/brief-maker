# F-TMP-002 DevPack — แบบฟอร์มประเมินความเสี่ยง (REQ-TMP-002)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 16 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 30 เคส
- e2e_standard 21/21
- frd_lint BLOCK 0
- anchor ที่ไม่พบบนจอ 0
- เทียบต้นฉบับ WARN 0.226

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K9 — เทียบต้นฉบับ WARN 0.226

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
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 15 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (11 ข้อ) · Strike · ก่อน UAT
- OQ-03 · role รองกรรมการผู้จัดการ/กรรมการผู้จัดการ ไม่มีใน DOA master (ใช้ role-gm ชั่วคราว) · "ตามความเหมาะสม" · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · RiskMatrix config มีหรือยัง / เจ้าของ · พี่เบิร์ด · ก่อน dev
- OQ-05 · ผูกกับโครงการ FM-BDM-01 ไหม · ลูกค้า · –
- OQ-06 · รหัส RSK ชนไหม · taxonomy function_code · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "คะแนน 1–5 โอกาสเกิด/ผลกระทบ (ต่ำมาก…สูงมาก + คำอธิบาย)"
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ทะเบียนความเสี่ยง: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 18 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส RSK
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `8314ebf6` | prototype |
| `02_BRD/BRD_F-TMP-002.docx` | `bfb1ba8d` | brd_docx |
| `02_BRD/BRD_F-TMP-002.md` | `d648f31c` | brd |
| `03_FRD/FRD_F-TMP-002_Pack/00_OVERVIEW.md` | `b1613b91` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/01_UI.md` | `12733d93` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/02_API.md` | `930aa9f0` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/03_LOGIC.md` | `237b869c` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/04_DB.md` | `248deaaa` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/05_RULES.md` | `6039f898` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/06_TESTS.md` | `ac236111` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/07_LOCKED_DECISIONS.md` | `3c8fda84` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/INDEX.md` | `62d77713` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/_SECTION_N.md` | `abb1294c` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/DOA_BRIEF_F-TMP-002.md` | `187f2468` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/DOCCFG_BRIEF_F-TMP-002.md` | `2412ea4a` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/MDOC_BRIEF_RSK.md` | `68222921` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/NTF_BRIEF_F-TMP-002.md` | `2fdd7a63` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/RSK.doa.yaml` | `0781c755` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/RSK.doccfg.yaml` | `b383639e` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/RSK.mdoc.yaml` | `e080b78d` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/RSK.ntf.yaml` | `d40b2edb` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-002.md` | `e8ede7e6` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `06e24ecb` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `8abef079` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-002.md` | `187f2468` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-002.md` | `2412ea4a` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_RSK.md` | `68222921` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-002.md` | `2fdd7a63` | ntf_brief |
| `05_Governance/RSK.doa.yaml` | `0781c755` | doa_yaml |
| `05_Governance/RSK.doccfg.yaml` | `b383639e` | doccfg_yaml |
| `05_Governance/RSK.mdoc.yaml` | `e080b78d` | mdoc_yaml |
| `05_Governance/RSK.ntf.yaml` | `d40b2edb` | ntf_yaml |
| `05_Governance/decisions.yaml` | `5ddf475d` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-002.md` | `05d21d8d` | qa_audit |
| `06_Test/cases.json` | `3394374f` | cases_json |
| `06_Test/testcase-F-TMP-002.html` | `29211ef6` | testcases_uat |
| `06_Test/testcases-F-TMP-002.md` | `5c6a048d` | testcases_ai |
| `07_Print/FM-BDM-02_template.html` | `c4a802ff` | print_extra_fm_bdm_02_template |
| `07_Print/RSK_print-spec.md` | `61d4b7b9` | print_spec |
| `07_Print/approved-doa6steps.data.json` | `a4722c1c` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `7e3f50d2` | print_data_approved_data |
| `07_Print/compare.json` | `b12f033a` | report_compare |
| `07_Print/compare_overlay.png` | `cc87cf10` | print_image_compare_overlay |
| `07_Print/compare_side.png` | `5696fb87` | print_image_compare_side |
| `07_Print/draft.data.json` | `5c25be62` | print_data_draft_data |
| `07_Print/form.tpl.html` | `66657204` | print_template |
| `07_Print/long-24rows.data.json` | `c801465e` | print_data_long_24rows_data |
| `07_Print/print_config.json` | `3fb10b98` | print_config |
| `07_Print/profile.json` | `45569d6c` | print_profile |
| `07_Print/rejected.data.json` | `27f96957` | print_data_rejected_data |
| `08_Reference/2. FM-BDM-02 แบบฟอร์มประเมินความเสี่ยง.xlsx` | `513afb94` | original_2_fm_bdm_02 |
| `08_Reference/FORM_SPEC.check.json` | `38fa9f7f` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `45fc90ca` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-002.html` | `b3809816` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-002_v2.md` | `dd42f33f` | prebrief |
| `08_Reference/RUN_LOG.md` | `8504bb7c` | run_log |
| `08_Reference/SAMPLE.pdf` | `a1429499` | original_sample |
| `08_Reference/page-1.png` | `9dc605aa` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `abb1294c` | report_frd_lint |
| `08_Reference/reports/anchors.json` | `af73b4f6` | report_anchors |
| `08_Reference/reports/e2e_report.json` | `1db788a8` | report_e2e |
| `08_Reference/shot_list.png` | `16a0a665` | original_shot_list |
| `08_Reference/shot_pdf.png` | `a462f204` | original_shot_pdf |
| `08_Reference/shot_view.png` | `fe22f3ec` | original_shot_view |
| `08_Reference/shot_wizard.png` | `99af9c6c` | original_shot_wizard |
