# F-TMP-006 DevPack — รายงานการเข้า-ออก ห้อง server (REQ-TMP-006)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 14 ข้อ (AI-DEFAULT 10) · พร้อมเริ่มทำ
- test case AI 51 เคส
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
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (โดยเฉพาะ ไม่มีขออนุมัติก่อนเข้า · ผู้รับรอง ≠ ผู้เข้า) · Strike · ก่อน UAT
- OQ-03 · role-it-officer · admin role ฝ่าย IT — role id ใน RBAC/DOA contract · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · ServerRoomAccessConfig อยู่ที่ไหน · พี่เบิร์ด · ก่อน dev
- OQ-05 · บุคคลภายนอกต้องเก็บข้อมูลเพิ่มไหม (เลขบัตร — PDPA) · ลูกค้า · –
- OQ-06 · หลายห้อง server ต่อบริษัทไหม · ลูกค้า · –
- OQ-07 · function_code taxonomy SRAL · รหัส feature จริง · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่มีการอนุมัติ
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ผู้ใช้กรอกเอง · เกินเกณฑ์ = เตือน · วันเวลาออก ก่อนวันเวลาเข้า → บล็อก (ขัดแย้งท
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการเข้า-ออกห้อง server: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 21 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นตามตำแหน่งกระดาษ  · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ)
- DEC-08 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติ none · admin role เห็นทั้งหมด
- DEC-09 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส SRAL
- DEC-10 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `ec3a7556` | prototype |
| `02_BRD/BRD_F-TMP-006.docx` | `ed3bb14f` | brd_docx |
| `02_BRD/BRD_F-TMP-006.md` | `a33ecc69` | brd |
| `03_FRD/FRD_F-TMP-006_Pack/00_OVERVIEW.md` | `4903bf20` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/01_UI.md` | `93e5c88c` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/02_API.md` | `38fd771d` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/03_LOGIC.md` | `c86e91ff` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/04_DB.md` | `b78eabef` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/05_RULES.md` | `ce3d12b1` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/06_TESTS.md` | `e837db87` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/07_LOCKED_DECISIONS.md` | `9b9fa42a` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/INDEX.md` | `0bc85491` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/_SECTION_N.md` | `2886c37b` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/DOCCFG_BRIEF_F-TMP-006.md` | `4997ae10` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/MDOC_BRIEF_SRAL.md` | `4c4ea9b9` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/NTF_BRIEF_F-TMP-006.md` | `7c2fecce` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/SRAL.doccfg.yaml` | `14ddab0c` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/SRAL.mdoc.yaml` | `f73b7a6a` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/SRAL.ntf.yaml` | `f522874f` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-006.md` | `244893db` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `a32bfa80` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `f6e54864` | decisions_md |
| `05_Governance/DOCCFG_BRIEF_F-TMP-006.md` | `4997ae10` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_SRAL.md` | `4c4ea9b9` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-006.md` | `7c2fecce` | ntf_brief |
| `05_Governance/SRAL.doccfg.yaml` | `14ddab0c` | doccfg_yaml |
| `05_Governance/SRAL.mdoc.yaml` | `f73b7a6a` | mdoc_yaml |
| `05_Governance/SRAL.ntf.yaml` | `f522874f` | ntf_yaml |
| `05_Governance/decisions.yaml` | `1cbf16b0` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-006.md` | `daa4b997` | qa_audit |
| `06_Test/cases.json` | `fde5c579` | cases_json |
| `06_Test/testcase-F-TMP-006.html` | `2df7d370` | testcases_uat |
| `06_Test/testcases-F-TMP-006.md` | `f23c46a2` | testcases_ai |
| `07_Print/SRAL_print-spec.md` | `0124e195` | print_spec |
| `07_Print/cancelled.data.json` | `d08e69fa` | print_data_cancelled_data |
| `07_Print/draft.data.json` | `a23cbc7f` | print_data_draft_data |
| `07_Print/form.tpl.html` | `7a77792a` | print_template |
| `07_Print/long-24rows.data.json` | `71bba175` | print_data_long_24rows_data |
| `07_Print/pending-cert.data.json` | `e38490ac` | print_data_pending_cert_data |
| `07_Print/print_config.json` | `b2ae7e94` | print_config |
| `07_Print/profile.json` | `fb113c01` | print_profile |
| `07_Print/submitted.data.json` | `2108b77f` | print_data_submitted_data |
| `07_Print/รายงานการเข้า-ออก_ห้อง_server_template.html` | `febb15ff` | print_extra_server_template |
| `08_Reference/9. FM-ITS-09 แบบฟอร์มรายงานการเข้า-ออก ห้อง server.xlsx` | `430646f5` | original_9_fm_its_09_server |
| `08_Reference/FORM_SPEC.check.json` | `63b48269` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `69429a74` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-006.html` | `21213302` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-006_v2.md` | `4e59ed90` | prebrief |
| `08_Reference/RUN_LOG.md` | `3d37296d` | run_log |
| `08_Reference/SAMPLE.pdf` | `bb5e6faf` | original_sample |
| `08_Reference/page-1.png` | `b1417dea` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `2886c37b` | report_frd_lint |
