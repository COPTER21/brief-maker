# F-TMP-002 DevPack — หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade (REQ-TMP-002)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 20 ข้อ (AI-DEFAULT 14) · พร้อมเริ่มทำ
- test case AI 64 เคส
- ไม่มี report e2e_standard (html-generator v9.2 #111)

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
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 11 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 8 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (สูตร % · 1 ขั้น · กลับร่าง) · Strike · ก่อน UAT
- OQ-03 · role "ผู้อำนวยการสายงานการขาย" ไม่มีใน DOA master (ใช้ role-mgr-bu) · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · SalesConfig.csat_* ใน Sales Configuration · พี่เบิร์ด · ก่อน dev
- OQ-05 · ผูกแบบสำรวจ FM-SAL-10 · Strike · –
- OQ-06 · กันสร้างซ้ำเดือน/หน่วยงาน · ลูกค้า · –
- OQ-07 · F-TMP-002 / CSM / function_code ชั่วคราว · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-mgr-bu · วงเงิน: ไม
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "ตั้งแต่ 3 ครั้งขึ้นไป / เดือน" → SalesConfig.csat_min_o
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ด้านคุณภาพสินค้า/บริการ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 4 แถวตามกระดาษ
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ด้านการส่งมอบสินค้า: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 4 แถวตามกระดาษ
- DEC-07 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ด้านเจ้าหน้าที่ผู้ให้บริการ/พนักงานขาย: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 8 แถวตา
- DEC-08 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: โดยมีรายชื่อดังนี้: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 14 แถวตามกระดาษ
- DEC-09 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-10 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-11 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-12 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-13 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส CSM
- DEC-14 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `7cf21d28` | prototype |
| `02_BRD/BRD_F-TMP-002.docx` | `131c4cdf` | brd_docx |
| `02_BRD/BRD_F-TMP-002.md` | `38533a0a` | brd |
| `03_FRD/FRD_F-TMP-002_Pack/00_OVERVIEW.md` | `b71197cf` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/01_UI.md` | `8ef1a042` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/02_API.md` | `a416e086` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/03_LOGIC.md` | `a765f1f7` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/04_DB.md` | `e0738ee4` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/05_RULES.md` | `08f24d5a` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/06_TESTS.md` | `2579ab2d` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/07_LOCKED_DECISIONS.md` | `269081eb` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/INDEX.md` | `a97550b8` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/_SECTION_N.md` | `1419408f` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/CSM.doa.yaml` | `75dd4f40` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/CSM.doccfg.yaml` | `1b618e72` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/CSM.mdoc.yaml` | `f4d6dc9d` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/CSM.ntf.yaml` | `6db96e9d` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/DOA_BRIEF_F-TMP-002.md` | `eb94a472` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/DOCCFG_BRIEF_F-TMP-002.md` | `c7c1f5bc` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/MDOC_BRIEF_CSM.md` | `43ddbbe9` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/NTF_BRIEF_F-TMP-002.md` | `8a641b15` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-002.md` | `e04841af` | ui_brief |
| `05_Governance/CSM.doa.yaml` | `75dd4f40` | doa_yaml |
| `05_Governance/CSM.doccfg.yaml` | `1b618e72` | doccfg_yaml |
| `05_Governance/CSM.mdoc.yaml` | `f4d6dc9d` | mdoc_yaml |
| `05_Governance/CSM.ntf.yaml` | `6db96e9d` | ntf_yaml |
| `05_Governance/DECISIONS.lock.json` | `057e0f60` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `cb66f2f0` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-002.md` | `eb94a472` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-002.md` | `c7c1f5bc` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_CSM.md` | `43ddbbe9` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-002.md` | `8a641b15` | ntf_brief |
| `05_Governance/decisions.yaml` | `5cb7839c` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-002.md` | `a1d0bb4f` | qa_audit |
| `06_Test/cases.json` | `22c01dff` | cases_json |
| `06_Test/testcase-F-TMP-002.html` | `d441c764` | testcases_uat |
| `06_Test/testcases-F-TMP-002.md` | `1ac8fb24` | testcases_ai |
| `07_Print/FM-SAL-11_print-spec.md` | `ab6dcafc` | print_spec |
| `07_Print/FM-SAL-11_template.html` | `6cc2be2c` | print_extra_fm_sal_11_template |
| `07_Print/approved-doa6steps.data.json` | `94e93e5c` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `a14d977c` | print_data_approved_data |
| `07_Print/draft.data.json` | `2cdf3d24` | print_data_draft_data |
| `07_Print/form.tpl.html` | `04eeb7a5` | print_template |
| `07_Print/long-22customers.data.json` | `61e33bdc` | print_data_long_22customers_data |
| `07_Print/print_config.json` | `6b166def` | print_config |
| `07_Print/profile.json` | `44bbc7f2` | print_profile |
| `07_Print/rejected.data.json` | `16c7b290` | print_data_rejected_data |
| `07_Print/render_data.py` | `1bae6e75` | print_extra_render_data |
| `08_Reference/11. FM-SAL-11 แบบสรุปหัวข้อการประเมินความพึงพอใจ สำหรับ General Trade.xlsx` | `79106d5d` | original_11_fm_sal_11_general_trade |
| `08_Reference/FORM_SPEC.check.json` | `12f4135d` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `ebb1948f` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-002.html` | `e0b0663a` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-002_v2.md` | `1cdc67a3` | prebrief |
| `08_Reference/RUN_LOG.md` | `25c84105` | run_log |
| `08_Reference/SAMPLE.pdf` | `71f205ba` | original_sample |
| `08_Reference/page-1.png` | `bfd8986b` | original_page_1 |
