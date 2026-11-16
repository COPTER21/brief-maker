# F-TMP-004 DevPack — แบบประเมินและคัดเลือกผู้ขาย/ผู้ให้บริการ ประจำปี (REQ-TMP-004)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 17 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 62 เคส
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
| `03_FRD` | FRD Pack | 18 |
| `04_UI_Brief` | UI Brief AS-BUILT | 1 |
| `05_Governance` | มติ (DECISIONS) + ใบประกาศ DOCCFG / DOA / MDOC / NTF | 11 |
| `06_Test` | test case AI + UAT ฉบับคน + QA audit | 4 |
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 10 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 8 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT · Strike · ก่อน UAT
- OQ-03 · Vendor master + อัปเดตสถานะ AVL ตามผล · ลูกค้า + พี่เบิร์ด · Phase 2
- OQ-04 · VendorEvaluationConfig อยู่ที่ไหน (Purchase Configuration?) · พี่เบิร์ด · ก่อน dev
- OQ-05 · role-pur-officer นอก DOA master · DOA เงื่อนไขตามผล (ไม่ใช่วงเงิน) · ผู้บริหาร = role-gm หรือ role-proc-dir · Strike + พี่เบิร์ด · ก่อน wire
- OQ-06 · หัวคอลัมน์ "คะแนนเฉลี่ย" → "คะแนนเต็ม"? · ฝ่าย/แผนกจัดซื้อ · ลูกค้า · –
- OQ-07 · ปุ่มทำซ้ำของ archetype ขัด DEC-11 · Strike · –
- OQ-08 · function_code taxonomy · รหัส feature จริง · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-pur-officer, role-m
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "หัวข้อการประเมิน 4 ข้อ + เกณฑ์ย่อย (3-5 วันทำการ · 0.5-
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: หัวข้อการประเมิน (Performance Item): ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 4 แถวตามกร
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส VEV
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `2b2a8922` | prototype |
| `02_BRD/BRD_F-TMP-004.docx` | `03f932bb` | brd_docx |
| `02_BRD/BRD_F-TMP-004.md` | `417cd576` | brd |
| `03_FRD/FRD_F-TMP-004_Pack/00_OVERVIEW.md` | `0b7f4654` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/01_UI.md` | `256cd3a5` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/02_API.md` | `34eb5fc6` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/03_LOGIC.md` | `6a6d9ac1` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/04_DB.md` | `f8ccfcd5` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/05_RULES.md` | `4dd0af90` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/06_TESTS.md` | `15fbaf26` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/07_LOCKED_DECISIONS.md` | `ddc9dacc` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/INDEX.md` | `8429cd58` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/_SECTION_N.md` | `471b3bad` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/DOA_BRIEF_F-TMP-004.md` | `c785a098` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/DOCCFG_BRIEF_F-TMP-004.md` | `f86f0230` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/MDOC_BRIEF_VEV.md` | `b571c9f7` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/NTF_BRIEF_F-TMP-004.md` | `c7971940` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/VEV.doa.yaml` | `638bcccc` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/VEV.doccfg.yaml` | `3858dae9` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/VEV.mdoc.yaml` | `115ed734` | frd_pack |
| `03_FRD/FRD_F-TMP-004_Pack/declarations/VEV.ntf.yaml` | `076ce798` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-004.md` | `f19cb4c5` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `54f518de` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `2973fc62` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-004.md` | `c785a098` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-004.md` | `f86f0230` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_VEV.md` | `b571c9f7` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-004.md` | `c7971940` | ntf_brief |
| `05_Governance/VEV.doa.yaml` | `638bcccc` | doa_yaml |
| `05_Governance/VEV.doccfg.yaml` | `3858dae9` | doccfg_yaml |
| `05_Governance/VEV.mdoc.yaml` | `115ed734` | mdoc_yaml |
| `05_Governance/VEV.ntf.yaml` | `076ce798` | ntf_yaml |
| `05_Governance/decisions.yaml` | `1e38bc9c` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-004.md` | `aca54289` | qa_audit |
| `06_Test/cases.json` | `f8ed7ec6` | cases_json |
| `06_Test/testcase-F-TMP-004.html` | `211f9b3d` | testcases_uat |
| `06_Test/testcases-F-TMP-004.md` | `d00ea816` | testcases_ai |
| `07_Print/FM-PUR-01_template.html` | `41339ced` | print_extra_fm_pur_01_template |
| `07_Print/VEV_print-spec.md` | `2e0475be` | print_spec |
| `07_Print/approved-doa6steps.data.json` | `bd83ab05` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `64211d05` | print_data_approved_data |
| `07_Print/draft.data.json` | `8fe4bd7e` | print_data_draft_data |
| `07_Print/form.tpl.html` | `09b9759d` | print_template |
| `07_Print/long-12criteria.data.json` | `5e33aa1d` | print_data_long_12criteria_data |
| `07_Print/print_config.json` | `583e5ef0` | print_config |
| `07_Print/profile.json` | `e0f72103` | print_profile |
| `07_Print/rejected.data.json` | `d89b3ea4` | print_data_rejected_data |
| `08_Reference/1. FM-PUR-01 แบบประเมินและคัดเลือกผู้ขายผู้ให้บริการ ประจำปี.xlsx` | `d4344d6d` | original_1_fm_pur_01 |
| `08_Reference/FORM_SPEC.check.json` | `873be71e` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `347a80e6` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-004.html` | `bd70ed06` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-004_v2.md` | `31412966` | prebrief |
| `08_Reference/RUN_LOG.md` | `cb192148` | run_log |
| `08_Reference/page-1.png` | `8b0758b0` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `471b3bad` | report_frd_lint |
