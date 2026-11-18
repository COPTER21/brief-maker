# F-TMP-005 DevPack — แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าในประเทศ (REQ-TMP-005)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 16 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 45 เคส
- e2e_standard 21/21
- frd_lint BLOCK 0
- เทียบต้นฉบับ WARN 0.247

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K9 — เทียบต้นฉบับ WARN 0.247

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
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 10 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (ประจำเดือน · แถวใต้ชื่อ · ≤ 12 ราย · 1 ขั้น · กลับร่าง) · Strike · ก่อน UAT
- OQ-03 · role "Managing Director" ไม่มีใน DOA master (ใช้ role-ceo) · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · SalesConfig.sda_topics/sda_scale ใน Sales Configuration (ร่วม F-TMP-004) · พี่เบิร์ด · ก่อน dev
- OQ-05 · แบบพิมพ์แนวตั้ง 2 หน้า 12 คอลัมน์ แทนต้นฉบับแนวนอน 1 หน้า 6 คอลัมน์ · ลูกค้า · ก่อน UAT
- OQ-06 · กันสร้างซ้ำเดือน / ลูกค้า > 12 ราย · ลูกค้า · –
- OQ-07 · F-TMP-005 / SDS / function_code ชั่วคราว · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-ceo · วงเงิน: ไม่มี
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "1. ความรวดเร็วในการตอบคำถาม … 5. คุณภาพสินค้า" → SalesC
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลูกค้าที่ประเมิน (คอลัมน์): สูงสุด 12 แถว · PDF อย่างน้อย 6 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · เพิ่ม: ประจำเดือน
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส SDS
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `9e0d967a` | prototype |
| `02_BRD/BRD_F-TMP-005.docx` | `70d68f07` | brd_docx |
| `02_BRD/BRD_F-TMP-005.md` | `2ede17d4` | brd |
| `03_FRD/FRD_F-TMP-005_Pack/00_OVERVIEW.md` | `d902ed30` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/01_UI.md` | `cc51dc03` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/02_API.md` | `d7a53fbf` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/03_LOGIC.md` | `af1f1c92` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/04_DB.md` | `be03d521` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/05_RULES.md` | `c90d0a7d` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/06_TESTS.md` | `29a25823` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/07_LOCKED_DECISIONS.md` | `f5b4a5ab` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/INDEX.md` | `88599730` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/_SECTION_N.md` | `18f5e6fb` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/DOA_BRIEF_F-TMP-005.md` | `6e296c8a` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/DOCCFG_BRIEF_F-TMP-005.md` | `9ae1cf2e` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/MDOC_BRIEF_SDS.md` | `158d2be1` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/NTF_BRIEF_F-TMP-005.md` | `38a8fc60` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/SDS.doa.yaml` | `0ec82973` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/SDS.doccfg.yaml` | `48e0f59f` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/SDS.mdoc.yaml` | `e281752d` | frd_pack |
| `03_FRD/FRD_F-TMP-005_Pack/declarations/SDS.ntf.yaml` | `c4905192` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-005.md` | `e967840f` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `7c81b518` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `b2b6cdff` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-005.md` | `6e296c8a` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-005.md` | `9ae1cf2e` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_SDS.md` | `158d2be1` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-005.md` | `38a8fc60` | ntf_brief |
| `05_Governance/SDS.doa.yaml` | `0ec82973` | doa_yaml |
| `05_Governance/SDS.doccfg.yaml` | `48e0f59f` | doccfg_yaml |
| `05_Governance/SDS.mdoc.yaml` | `e281752d` | mdoc_yaml |
| `05_Governance/SDS.ntf.yaml` | `c4905192` | ntf_yaml |
| `05_Governance/decisions.yaml` | `fa7cf4b5` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-005.md` | `f83d4a8b` | qa_audit |
| `06_Test/cases.json` | `9f1992f0` | cases_json |
| `06_Test/testcase-F-TMP-005.html` | `1918c11d` | testcases_uat |
| `06_Test/testcases-F-TMP-005.md` | `80471876` | testcases_ai |
| `07_Print/FM-SAL-21_print-spec.md` | `e10f5313` | print_spec |
| `07_Print/FM-SAL-21_template.html` | `5cff012d` | print_extra_fm_sal_21_template |
| `07_Print/approved-doa6steps.data.json` | `7f2fa2d2` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `2999de52` | print_data_approved_data |
| `07_Print/compare.json` | `a242710d` | report_compare |
| `07_Print/compare_side.png` | `8719ef87` | print_image_compare_side |
| `07_Print/draft.data.json` | `92b41d84` | print_data_draft_data |
| `07_Print/form.tpl.html` | `3cb44826` | print_template |
| `07_Print/long-12customers.data.json` | `a52c750f` | print_data_long_12customers_data |
| `07_Print/print_config.json` | `c73a6c10` | print_config |
| `07_Print/profile.json` | `d258eb60` | print_profile |
| `07_Print/rejected.data.json` | `a2dbef48` | print_data_rejected_data |
| `07_Print/render_data.py` | `da13bf1a` | print_extra_render_data |
| `08_Reference/21. FM-SAL-21 สรุปแบบประเมินความพึงพอใจ (ในประเทศ).docx` | `5c5dcf50` | original_21_fm_sal_21 |
| `08_Reference/FORM_SPEC.check.json` | `fe8b5e81` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `3847ca20` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-005.html` | `115aa753` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-005_v2.md` | `88edca28` | prebrief |
| `08_Reference/RUN_LOG.md` | `1a69753d` | run_log |
| `08_Reference/SAMPLE.pdf` | `1f108086` | original_sample |
| `08_Reference/page-1.png` | `9cabbc24` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `18f5e6fb` | report_frd_lint |
| `08_Reference/reports/e2e_container_ref.json` | `ac980a99` | report_e2e |
