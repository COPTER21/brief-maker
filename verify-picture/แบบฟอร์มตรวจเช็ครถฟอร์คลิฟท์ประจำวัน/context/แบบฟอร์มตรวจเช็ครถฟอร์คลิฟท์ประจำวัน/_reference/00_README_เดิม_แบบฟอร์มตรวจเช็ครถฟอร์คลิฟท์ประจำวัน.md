# F-TMP-002 DevPack — แบบฟอร์มตรวจเช็ครถฟอร์คลิฟท์ประจำวัน (REQ-TMP-002)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 2
- มติ 17 ข้อ (AI-DEFAULT 13) · พร้อมเริ่มทำ
- test case AI 64 เคส
- ไม่มี report e2e_standard (html-generator v9.2 #111)
- frd_lint BLOCK 0

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K3 — run_log: ไฟล์ถูกแก้หลังลงทะเบียน — รัน manifest_scan ใหม่
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
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT · Strike · ก่อน UAT
- OQ-03 · ช่องหมายเลข/ทะเบียนรถ (DEC-17) · ลูกค้า · Phase 2
- OQ-04 · ForkliftChecklistConfig อยู่ที่ไหน (feature ใหม่) · พี่เบิร์ด · ก่อน dev
- OQ-05 · role-supervisor แบบ relative (ผังองค์กร) · Strike + พี่เบิร์ด · ก่อน wire
- OQ-06 · ปุ่มทำซ้ำของ archetype ขัด DEC-13 · Strike · –
- OQ-07 · function_code taxonomy · รหัส feature จริง · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-supervisor · วงเงิน
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "รายการตรวจสอบทั่วไป 15 รายการ (สภาพตัวรถโดยรวม … ตรวจสอ
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการตรวจสอบทั่วไป: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 15 แถวตามกระดาษ
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการตรวจสอบเฉพาะรถฟอร์คลิฟท์น้ำมัน: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 8 แถวตามก
- DEC-07 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการตรวจสอบเฉพาะรถฟอร์คลิฟท์ไฟฟ้า: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 6 แถวตามกร
- DEC-08 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-09 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-10 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-11 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-12 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส FLI
- DEC-13 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `b9cf1639` | prototype |
| `02_BRD/BRD_F-TMP-002.docx` | `6ac2f6c2` | brd_docx |
| `02_BRD/BRD_F-TMP-002.md` | `6082b4c2` | brd |
| `03_FRD/FRD_F-TMP-002_Pack/00_OVERVIEW.md` | `0d1227bc` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/01_UI.md` | `5779f023` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/02_API.md` | `4b5f0649` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/03_LOGIC.md` | `c0c32b9f` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/04_DB.md` | `b2901c60` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/05_RULES.md` | `fc23141f` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/06_TESTS.md` | `9110b39a` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/07_LOCKED_DECISIONS.md` | `9d880247` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/INDEX.md` | `882afae5` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/_SECTION_N.md` | `dbd56061` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/DOA_BRIEF_F-TMP-002.md` | `99a7db76` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/DOCCFG_BRIEF_F-TMP-002.md` | `a6657f5c` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/FLI.doa.yaml` | `4a781250` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/FLI.doccfg.yaml` | `4f50c463` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/FLI.mdoc.yaml` | `1947ffb6` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/FLI.ntf.yaml` | `b77abe0c` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/MDOC_BRIEF_FLI.md` | `11b7e3ba` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/NTF_BRIEF_F-TMP-002.md` | `e935252f` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-002.md` | `cda1c6ed` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `9db66731` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `bf94ca42` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-002.md` | `99a7db76` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-002.md` | `a6657f5c` | doccfg_brief |
| `05_Governance/FLI.doa.yaml` | `4a781250` | doa_yaml |
| `05_Governance/FLI.doccfg.yaml` | `4f50c463` | doccfg_yaml |
| `05_Governance/FLI.mdoc.yaml` | `1947ffb6` | mdoc_yaml |
| `05_Governance/FLI.ntf.yaml` | `b77abe0c` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_FLI.md` | `11b7e3ba` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-002.md` | `e935252f` | ntf_brief |
| `05_Governance/decisions.yaml` | `1a020ce3` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-002.md` | `f4358802` | qa_audit |
| `06_Test/cases.json` | `23290586` | cases_json |
| `06_Test/testcase-F-TMP-002.html` | `20402f2f` | testcases_uat |
| `06_Test/testcases-F-TMP-002.md` | `16bf9475` | testcases_ai |
| `07_Print/FLI_print-spec.md` | `99a849ba` | print_spec |
| `07_Print/FM-WHS-04_template.html` | `831519f2` | print_extra_fm_whs_04_template |
| `07_Print/approved-doa6steps.data.json` | `aef18435` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `9224f318` | print_data_approved_data |
| `07_Print/draft.data.json` | `98d26f1a` | print_data_draft_data |
| `07_Print/form.tpl.html` | `3570ae18` | print_template |
| `07_Print/long-20items.data.json` | `4a9edd99` | print_data_long_20items_data |
| `07_Print/print_config.json` | `a4ef3dd1` | print_config |
| `07_Print/profile.json` | `869ba7f1` | print_profile |
| `07_Print/rejected.data.json` | `e3bc10e5` | print_data_rejected_data |
| `08_Reference/4. FM-WHS-04 แบบฟอร์มตรวจเช็ครถฟอร์คลิฟท.xlsx` | `5956601e` | original_4_fm_whs_04 |
| `08_Reference/FORM_SPEC.check.json` | `7ec30d1b` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `3ee083e1` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-002.html` | `106b21be` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-002_v2.md` | `1a09205c` | prebrief |
| `08_Reference/RUN_LOG.md` | `f239929e` | run_log |
| `08_Reference/SAMPLE.pdf` | `67a8f670` | original_sample |
| `08_Reference/page-1.png` | `08eb86ad` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `dbd56061` | report_frd_lint |
