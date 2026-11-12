# F-TMP-006 DevPack — แบบฟอร์มเปิดเผยผลประโยชน์ทับซ้อนของแผนกจัดซื้อ ประจำปี (REQ-TMP-006)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 18 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
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
| `03_FRD` | FRD Pack | 18 |
| `04_UI_Brief` | UI Brief AS-BUILT | 1 |
| `05_Governance` | มติ (DECISIONS) + ใบประกาศ DOCCFG / DOA / MDOC / NTF | 11 |
| `06_Test` | test case AI + UAT ฉบับคน + QA audit | 4 |
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 10 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 9 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT · Strike · ก่อน UAT
- OQ-03 · "ฝ่ายกฎหมาย" ใต้ช่องลงชื่อ: ต้องลงนามเป็นขั้น 2 ไหม · = role-compliance ไหม · ลูกค้า + พี่เบิร์ด · ก่อน wire
- OQ-04 · ทะเบียน COI กลาง + เตือนตอนจัดซื้อกับผู้ขายที่เกี่ยวข้อง · ลูกค้า + พี่เบิร์ด · Phase 2
- OQ-05 · ใช้กับแผนกอื่น · เปิดรอบ/ติดตามผู้ยังไม่ยื่น · ลูกค้า · –
- OQ-06 · CoiDisclosureConfig อยู่ที่ไหน (Purchase Configuration / Policy Center) · พี่เบิร์ด · ก่อน dev
- OQ-07 · แยกรายละเอียดเป็นช่อง · ลูกค้า · –
- OQ-08 · function_code taxonomy · รหัส feature จริง · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-line-manager · วงเง
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "ประจำปี 2569" → CoiDisclosureConfig.current_year (ตัวแป
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส COI
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `824941ce` | prototype |
| `02_BRD/BRD_F-TMP-006.docx` | `18ff97a6` | brd_docx |
| `02_BRD/BRD_F-TMP-006.md` | `16c73308` | brd |
| `03_FRD/FRD_F-TMP-006_Pack/00_OVERVIEW.md` | `2e01b011` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/01_UI.md` | `3145b1b4` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/02_API.md` | `639f1f80` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/03_LOGIC.md` | `f4a14400` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/04_DB.md` | `379266fe` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/05_RULES.md` | `20e431f2` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/06_TESTS.md` | `c4c273ab` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/07_LOCKED_DECISIONS.md` | `f771a1c3` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/INDEX.md` | `4fffa598` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/_SECTION_N.md` | `4ec625b2` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/COI.doa.yaml` | `81733b16` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/COI.doccfg.yaml` | `6dee80a7` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/COI.mdoc.yaml` | `e9b120cc` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/COI.ntf.yaml` | `e8c7c5c7` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/DOA_BRIEF_F-TMP-006.md` | `ba7d5831` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/DOCCFG_BRIEF_F-TMP-006.md` | `edd21a0a` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/MDOC_BRIEF_COI.md` | `a666ac7a` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/NTF_BRIEF_F-TMP-006.md` | `89be4553` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-006.md` | `3cdf037e` | ui_brief |
| `05_Governance/COI.doa.yaml` | `81733b16` | doa_yaml |
| `05_Governance/COI.doccfg.yaml` | `6dee80a7` | doccfg_yaml |
| `05_Governance/COI.mdoc.yaml` | `e9b120cc` | mdoc_yaml |
| `05_Governance/COI.ntf.yaml` | `e8c7c5c7` | ntf_yaml |
| `05_Governance/DECISIONS.lock.json` | `9a2acc22` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `af4402a9` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-006.md` | `ba7d5831` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-006.md` | `edd21a0a` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_COI.md` | `a666ac7a` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-006.md` | `89be4553` | ntf_brief |
| `05_Governance/decisions.yaml` | `09f2e248` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-006.md` | `0ac290f9` | qa_audit |
| `06_Test/cases.json` | `29b0da99` | cases_json |
| `06_Test/testcase-F-TMP-006.html` | `64296b38` | testcases_uat |
| `06_Test/testcases-F-TMP-006.md` | `92951a8a` | testcases_ai |
| `07_Print/COI_print-spec.md` | `70de4681` | print_spec |
| `07_Print/FM-PUR-04_template.html` | `0eb0616e` | print_extra_fm_pur_04_template |
| `07_Print/approved-doa6steps.data.json` | `66e2b3dd` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `76d3538d` | print_data_approved_data |
| `07_Print/draft.data.json` | `76013a2d` | print_data_draft_data |
| `07_Print/form.tpl.html` | `b62e8806` | print_template |
| `07_Print/long-12lines.data.json` | `c20bc22e` | print_data_long_12lines_data |
| `07_Print/print_config.json` | `f2e085b5` | print_config |
| `07_Print/profile.json` | `2f04bd02` | print_profile |
| `07_Print/rejected.data.json` | `f51586ec` | print_data_rejected_data |
| `08_Reference/4. FM-PUR-04 แบบฟอร์มเปิดเผยผลประโยชน์ทับซ้อนประจำปี 2569.docx` | `089b564a` | original_4_fm_pur_04_2569 |
| `08_Reference/FORM_SPEC.check.json` | `36747a93` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `ec92be8d` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-006.html` | `364073ae` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-006_v2.md` | `afdb9d1e` | prebrief |
| `08_Reference/RUN_LOG.md` | `d1d8309e` | run_log |
| `08_Reference/SAMPLE.pdf` | `8f8d6da8` | original_sample |
| `08_Reference/page-1.png` | `8474e292` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `4ec625b2` | report_frd_lint |
