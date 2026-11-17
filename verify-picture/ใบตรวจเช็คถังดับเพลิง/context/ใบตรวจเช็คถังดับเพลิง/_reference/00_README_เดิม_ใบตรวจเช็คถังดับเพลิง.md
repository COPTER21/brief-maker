# F-TMP-001 DevPack — ใบตรวจเช็คถังดับเพลิง (REQ-TMP-001)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 13 ข้อ (AI-DEFAULT 10) · พร้อมเริ่มทำ
- test case AI 22 เคส
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
| `03_FRD` | FRD Pack | 16 |
| `04_UI_Brief` | UI Brief AS-BUILT | 1 |
| `05_Governance` | มติ (DECISIONS) + ใบประกาศ DOCCFG / DOA / MDOC / NTF | 9 |
| `06_Test` | test case AI + UAT ฉบับคน + QA audit | 4 |
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 11 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 10 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่มีการอนุมัติ
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ทุกแถวต้องเลือกครบ 4 หัวข้
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการตรวจ (ต่อครั้ง): ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 12 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นตามตำแหน่งกระดาษ  · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ)
- DEC-08 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติ none · admin role เห็นทั้งหมด
- DEC-09 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส FEC
- DEC-10 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `036fefbd` | prototype |
| `02_BRD/BRD_F-TMP-001.docx` | `711439c7` | brd_docx |
| `02_BRD/BRD_F-TMP-001.md` | `762f1671` | brd |
| `03_FRD/FRD_F-TMP-001_Pack/00_OVERVIEW.md` | `7fd28d6a` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/01_UI.md` | `4fa42c45` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/02_API.md` | `ea87f4a1` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/03_LOGIC.md` | `cc63bdfb` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/04_DB.md` | `2fe3cfb0` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/05_RULES.md` | `48d568a0` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/06_TESTS.md` | `6bf7b09e` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/07_LOCKED_DECISIONS.md` | `749d8399` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/INDEX.md` | `7e51a277` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/_SECTION_N.md` | `d844a339` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/DOCCFG_BRIEF_F-TMP-001.md` | `3f52fd82` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/FEC.doccfg.yaml` | `e2478faa` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/FEC.mdoc.yaml` | `3153c40a` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/FEC.ntf.yaml` | `3c064abb` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/MDOC_BRIEF_FEC.md` | `472c995b` | frd_pack |
| `03_FRD/FRD_F-TMP-001_Pack/declarations/NTF_BRIEF_F-TMP-001.md` | `cf3377ef` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-001.md` | `6fb33872` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `5bddeb01` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `4e89dc7e` | decisions_md |
| `05_Governance/DOCCFG_BRIEF_F-TMP-001.md` | `3f52fd82` | doccfg_brief |
| `05_Governance/FEC.doccfg.yaml` | `e2478faa` | doccfg_yaml |
| `05_Governance/FEC.mdoc.yaml` | `3153c40a` | mdoc_yaml |
| `05_Governance/FEC.ntf.yaml` | `3c064abb` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_FEC.md` | `472c995b` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-001.md` | `cf3377ef` | ntf_brief |
| `05_Governance/decisions.yaml` | `7e170a86` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-001.md` | `6a4d4512` | qa_audit |
| `06_Test/cases.json` | `e5c558ae` | cases_json |
| `06_Test/testcase-F-TMP-001.html` | `fe4abe4c` | testcases_uat |
| `06_Test/testcases-F-TMP-001.md` | `d7156127` | testcases_ai |
| `07_Print/abnormal.data.json` | `aeed3b59` | print_data_abnormal_data |
| `07_Print/active-3rows.data.json` | `f9035d69` | print_data_active_3rows_data |
| `07_Print/cancelled.data.json` | `82835711` | print_data_cancelled_data |
| `07_Print/form.tpl.html` | `deba4d5a` | print_template |
| `07_Print/full-12rows.data.json` | `650681c1` | print_data_full_12rows_data |
| `07_Print/long-24rows.data.json` | `8455f2c6` | print_data_long_24rows_data |
| `07_Print/print_config.json` | `de887b86` | print_config |
| `07_Print/profile.json` | `0e5a2f1f` | print_profile |
| `07_Print/render_data.py` | `fb90fc52` | print_extra_render_data |
| `07_Print/ใบตรวจเช็คถังดับเพลิง_print-spec.md` | `56afb28d` | print_spec |
| `07_Print/ใบตรวจเช็คถังดับเพลิง_template.html` | `0503a819` | print_extra_template |
| `08_Reference/3. FM-WHS-03 ใบตรวจเช็คถังดับเพลิง.xlsx` | `d453063b` | original_3_fm_whs_03 |
| `08_Reference/FORM_SPEC.check.json` | `de150272` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `23159bfb` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-001.html` | `a8425e94` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-001_v2.md` | `1e457d99` | prebrief |
| `08_Reference/RUN_LOG.md` | `d2d7a412` | run_log |
| `08_Reference/SAMPLE.pdf` | `256ac9fa` | original_sample |
| `08_Reference/page-1.png` | `4e87ecd7` | original_page_1 |
| `08_Reference/page-2.png` | `5339fae6` | original_page_2 |
| `08_Reference/reports/_SECTION_N.md` | `d844a339` | report_frd_lint |
