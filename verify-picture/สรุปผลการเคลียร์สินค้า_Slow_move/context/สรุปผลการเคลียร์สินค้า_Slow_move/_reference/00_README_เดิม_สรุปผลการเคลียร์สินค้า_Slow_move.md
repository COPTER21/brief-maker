# F-TMP-003 DevPack — สรุปผลการเคลียร์สินค้า Slow move (REQ-TMP-003)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 15 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 60 เคส
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
- OQ-03 · ช่องคลัง/คงเหลือ/หน่วย/วันผลิต (DEC-12/15) · ลูกค้า · Phase 2
- OQ-04 · SlowMoveConfig อยู่ที่ไหน (feature ใหม่) · พี่เบิร์ด · ก่อน dev
- OQ-05 · role-mgr-wh resolve ตามหน่วยงานผู้จัดทำ (relative) · Strike + พี่เบิร์ด · ก่อน wire
- OQ-06 · ปุ่มทำซ้ำของ archetype ขัด DEC-11 · Strike · –
- OQ-07 · function_code taxonomy · รหัส feature จริง · Strike · ก่อน register
- OQ-08 · แถวเกิน 53 ต่อใบ → แบบพิมพ์เพิ่มหน้า? · Strike · –
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-mgr-wh · วงเงิน: ไม
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "แนวทางการเคลียร์ (ช่องข้อความ ไม่มีตัวเลือกพิมพ์บนกระดา
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการสินค้า Slow move: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 23 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส SMC
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `6f7c127e` | prototype |
| `02_BRD/BRD_F-TMP-003.docx` | `990cbffe` | brd_docx |
| `02_BRD/BRD_F-TMP-003.md` | `f6ac33f9` | brd |
| `03_FRD/FRD_F-TMP-003_Pack/00_OVERVIEW.md` | `c14a4233` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/01_UI.md` | `e2ff39d6` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/02_API.md` | `dd532bf8` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/03_LOGIC.md` | `9ed86ed2` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/04_DB.md` | `aa555962` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/05_RULES.md` | `e3479fdf` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/06_TESTS.md` | `f45e1914` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/07_LOCKED_DECISIONS.md` | `def3a1e7` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/INDEX.md` | `d7e252e8` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/_SECTION_N.md` | `f05cb862` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/DOA_BRIEF_F-TMP-003.md` | `1450bcf7` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/DOCCFG_BRIEF_F-TMP-003.md` | `78db1cd3` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/MDOC_BRIEF_SMC.md` | `f4dcbd01` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/NTF_BRIEF_F-TMP-003.md` | `8f29b7a6` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/SMC.doa.yaml` | `35e092dc` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/SMC.doccfg.yaml` | `9e1d77a5` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/SMC.mdoc.yaml` | `c7852043` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/SMC.ntf.yaml` | `faf051a2` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-003.md` | `7d7d8f9b` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `cbb9dfa8` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `b6fd6840` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-003.md` | `1450bcf7` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-003.md` | `78db1cd3` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_SMC.md` | `f4dcbd01` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-003.md` | `8f29b7a6` | ntf_brief |
| `05_Governance/SMC.doa.yaml` | `35e092dc` | doa_yaml |
| `05_Governance/SMC.doccfg.yaml` | `9e1d77a5` | doccfg_yaml |
| `05_Governance/SMC.mdoc.yaml` | `c7852043` | mdoc_yaml |
| `05_Governance/SMC.ntf.yaml` | `faf051a2` | ntf_yaml |
| `05_Governance/decisions.yaml` | `c89f557d` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-003.md` | `2aa55bd3` | qa_audit |
| `06_Test/cases.json` | `906568cd` | cases_json |
| `06_Test/testcase-F-TMP-003.html` | `ccf91e34` | testcases_uat |
| `06_Test/testcases-F-TMP-003.md` | `49e1115c` | testcases_ai |
| `07_Print/FM-WHS-09_template.html` | `ad2a8bcf` | print_extra_fm_whs_09_template |
| `07_Print/SMC_print-spec.md` | `9e5f82a5` | print_spec |
| `07_Print/approved-doa6steps.data.json` | `0cad9fe9` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `f19ff10b` | print_data_approved_data |
| `07_Print/draft.data.json` | `fdb8e4ec` | print_data_draft_data |
| `07_Print/form.tpl.html` | `1075822d` | print_template |
| `07_Print/long-45items.data.json` | `fedeaaf3` | print_data_long_45items_data |
| `07_Print/print_config.json` | `15e45dfa` | print_config |
| `07_Print/profile.json` | `8386a993` | print_profile |
| `07_Print/rejected.data.json` | `f26b56c5` | print_data_rejected_data |
| `08_Reference/9. FM-WHS-09 สรุปผลการเคลียร์สินค้า Slow Move.xlsx` | `11a1e288` | original_9_fm_whs_09_slow_move |
| `08_Reference/FORM_SPEC.check.json` | `b9970580` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `1b887283` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-003.html` | `1a93bdc8` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-003_v2.md` | `0a5c5ad9` | prebrief |
| `08_Reference/RUN_LOG.md` | `b681d982` | run_log |
| `08_Reference/SAMPLE.pdf` | `f0e88a15` | original_sample |
| `08_Reference/page-1.png` | `9493af3f` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `f05cb862` | report_frd_lint |
