# F-TMP-002 DevPack — แบบฟอร์มตรวจเช็คความเรียบร้อยห้อง Server (REQ-TMP-002)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 13 ข้อ (AI-DEFAULT 10) · พร้อมเริ่มทำ
- test case AI 50 เคส
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
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 10 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 9 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (โดยเฉพาะ ไม่มีผู้ตรวจทาน) · Strike · ก่อน UAT
- OQ-03 · admin role ฝ่าย IT — role id ใน RBAC/DOA · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · ServerRoomCheckConfig อยู่ที่ไหน · พี่เบิร์ด · ก่อน dev
- OQ-05 · รูปแบบความดันถังดับเพลิง · ลูกค้า · –
- OQ-06 · หลายห้อง Server ต่อบริษัทไหม · ลูกค้า · –
- OQ-07 · function_code taxonomy SRC · รหัส feature จริง · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่มีการอนุมัติ
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "18-27°C" → ServerRoomCheckConfig.temp_min_c / temp_max_
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการตรวจเช็คประจำวัน: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 30 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นตามตำแหน่งกระดาษ  · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ)
- DEC-08 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติ none · admin role เห็นทั้งหมด
- DEC-09 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส SRC
- DEC-10 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `e275c55e` | prototype |
| `02_BRD/BRD_F-TMP-002.docx` | `0055724d` | brd_docx |
| `02_BRD/BRD_F-TMP-002.md` | `f0ac1fc2` | brd |
| `03_FRD/FRD_F-TMP-002_Pack/00_OVERVIEW.md` | `d85b8c0e` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/01_UI.md` | `1f6b2e8d` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/02_API.md` | `d62dee52` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/03_LOGIC.md` | `af3035de` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/04_DB.md` | `29b84bc9` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/05_RULES.md` | `258caf73` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/06_TESTS.md` | `2fbe1dfa` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/07_LOCKED_DECISIONS.md` | `a959b10b` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/INDEX.md` | `16aa6875` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/_SECTION_N.md` | `3a4eec78` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/DOCCFG_BRIEF_F-TMP-002.md` | `eb8d9367` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/MDOC_BRIEF_SRC.md` | `4acf451a` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/NTF_BRIEF_F-TMP-002.md` | `7036c453` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/SRC.doccfg.yaml` | `05935ba7` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/SRC.mdoc.yaml` | `d0eb54ff` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/SRC.ntf.yaml` | `7f69fdca` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-002.md` | `e0dca9fd` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `89270f50` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `e36be76e` | decisions_md |
| `05_Governance/DOCCFG_BRIEF_F-TMP-002.md` | `eb8d9367` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_SRC.md` | `4acf451a` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-002.md` | `7036c453` | ntf_brief |
| `05_Governance/SRC.doccfg.yaml` | `05935ba7` | doccfg_yaml |
| `05_Governance/SRC.mdoc.yaml` | `d0eb54ff` | mdoc_yaml |
| `05_Governance/SRC.ntf.yaml` | `7f69fdca` | ntf_yaml |
| `05_Governance/decisions.yaml` | `1bff287e` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-002.md` | `e2c2501a` | qa_audit |
| `06_Test/cases.json` | `fc0e08c3` | cases_json |
| `06_Test/testcase-F-TMP-002.html` | `7805bd48` | testcases_uat |
| `06_Test/testcases-F-TMP-002.md` | `e3d2575b` | testcases_ai |
| `07_Print/SRC_print-spec.md` | `a179da98` | print_spec |
| `07_Print/abnormal.data.json` | `253bdbf2` | print_data_abnormal_data |
| `07_Print/cancelled.data.json` | `c18a5277` | print_data_cancelled_data |
| `07_Print/draft.data.json` | `59d16363` | print_data_draft_data |
| `07_Print/form.tpl.html` | `db37e5b2` | print_template |
| `07_Print/long-31rows.data.json` | `e7b8a9e8` | print_data_long_31rows_data |
| `07_Print/print_config.json` | `e53d4613` | print_config |
| `07_Print/profile.json` | `aff9ca28` | print_profile |
| `07_Print/submitted.data.json` | `59d5a372` | print_data_submitted_data |
| `07_Print/แบบฟอร์มตรวจเช็คความเรียบร้อยห้อง_Server_template.html` | `231ca68a` | print_extra_server_template |
| `08_Reference/10. FM-ITS-10 แบบฟอร์มตรวจเช็คความเรียบร้อยห้อง Server.xlsx` | `c5604365` | original_10_fm_its_10_server |
| `08_Reference/FORM_SPEC.check.json` | `34374599` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `3a46f888` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-002.html` | `9dc47ba2` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-002_v2.md` | `7935ea9d` | prebrief |
| `08_Reference/RUN_LOG.md` | `bcdffc9b` | run_log |
| `08_Reference/SAMPLE.pdf` | `e9dbc6c8` | original_sample |
| `08_Reference/page-1.png` | `8a67c309` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `3a4eec78` | report_frd_lint |
