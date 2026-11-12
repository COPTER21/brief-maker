# F-TMP-007 DevPack — ใบคำร้องขอดำเนินการด้านเอกสาร (REQ-TMP-007)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 16 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 69 เคส · UAT เก็บ 58 เคส
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
| `03_FRD` | FRD Pack | 17 |
| `04_UI_Brief` | UI Brief AS-BUILT | 1 |
| `05_Governance` | มติ (DECISIONS) + ใบประกาศ DOCCFG / DOA / MDOC / NTF | 11 |
| `06_Test` | test case AI + UAT ฉบับคน + QA audit | 4 |
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 12 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 14 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 4 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ผู้ใช้กรอกเอง · เกินเกณฑ์ = เตือน · วัตถุประสงค์ เลือก 1 ข้อ (บล็อก) · ISSUE เลื
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการเอกสารที่ต้องดำเนินการจัดทำ/ทบทวนเพิ่มเติม: ไม่จำกัดจำนวนแถว · PDF อย่างน้
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส DAR
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `7f8081e4` | prototype |
| `02_BRD/BRD_F-TMP-007.docx` | `e5184ab5` | brd_docx |
| `02_BRD/BRD_F-TMP-007.md` | `5a3b082e` | brd |
| `03_FRD/FRD_F-TMP-007_Pack/00_OVERVIEW.md` | `f1812df7` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/01_UI.md` | `2c3f75e8` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/02_API.md` | `5c6da22b` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/03_LOGIC.md` | `313eb656` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/04_DB.md` | `3182ee88` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/05_RULES.md` | `ff885d35` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/06_TESTS.md` | `7cb185fd` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/07_LOCKED_DECISIONS.md` | `a8bc7c80` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/INDEX.md` | `4bc7db13` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/DAR.doa.yaml` | `a8686b96` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/DAR.doccfg.yaml` | `8c9014a4` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/DAR.mdoc.yaml` | `859b9568` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/DAR.ntf.yaml` | `e14dae80` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/DOA_BRIEF_F-TMP-007.md` | `37b80260` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/DOCCFG_BRIEF_F-TMP-007.md` | `fc8e4a89` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/MDOC_BRIEF_DAR.md` | `5f860258` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/declarations/NTF_BRIEF_F-TMP-007.md` | `2da106c2` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-007.md` | `ac639de4` | ui_brief |
| `05_Governance/DAR.doa.yaml` | `a8686b96` | doa_yaml |
| `05_Governance/DAR.doccfg.yaml` | `8c9014a4` | doccfg_yaml |
| `05_Governance/DAR.mdoc.yaml` | `859b9568` | mdoc_yaml |
| `05_Governance/DAR.ntf.yaml` | `e14dae80` | ntf_yaml |
| `05_Governance/DECISIONS.lock.json` | `14e7036a` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `bdabfd13` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-007.md` | `37b80260` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-007.md` | `fc8e4a89` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_DAR.md` | `5f860258` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-007.md` | `2da106c2` | ntf_brief |
| `05_Governance/decisions.yaml` | `8122c0e7` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-007.md` | `79cc0c39` | qa_audit |
| `06_Test/cases.json` | `b0906ca5` | cases_json |
| `06_Test/testcase-F-TMP-007.html` | `6708dbd9` | testcases_uat |
| `06_Test/testcases-F-TMP-007.md` | `5f5675ec` | testcases_ai |
| `07_Print/DAR_data-contract.md` | `0b1f2082` | print_data_contract |
| `07_Print/DAR_print-spec.md` | `ed7a3115` | print_spec |
| `07_Print/DAR_template.html` | `c02f7849` | print_extra_dar_template |
| `07_Print/_states_sheet.png` | `4cbf6993` | print_image_states_sheet |
| `07_Print/approved-doa6steps.data.json` | `771d9550` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `290588fe` | print_data_approved_data |
| `07_Print/draft.data.json` | `582a26a6` | print_data_draft_data |
| `07_Print/form.tpl.html` | `6a78c6ab` | print_template |
| `07_Print/long.data.json` | `2b885f6d` | print_data_long_data |
| `07_Print/print_config.json` | `4c2a3472` | print_config |
| `07_Print/profile.json` | `c9cb5805` | print_profile |
| `07_Print/rejected.data.json` | `c52dfb7b` | print_data_rejected_data |
| `08_Reference/3. FM-CCC-03 ใบคำร้องขอดำเนินการด้านเอกสาร  Document Action Request (DAR Form ).xlsx` | `c0202801` | original_3_fm_ccc_03_document_action_request_dar_ |
| `08_Reference/FORM_SPEC.check.json` | `32be04cf` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `27f0bb4a` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-007.html` | `b1a7ca3b` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-007_v2.md` | `9266fc90` | prebrief |
| `08_Reference/RUN_LOG.md` | `b5b47d83` | run_log |
| `08_Reference/RUN_STATE.json` | `2e9fee56` | original_run_state |
| `08_Reference/SAMPLE.pdf` | `bfbbd5fc` | original_sample |
| `08_Reference/page-1.png` | `41fc9ec3` | original_page_1 |
| `08_Reference/page-2.png` | `c6c61f50` | original_page_2 |
| `08_Reference/reports/_SECTION_N.md` | `956a4a0f` | report_frd_lint |
| `08_Reference/reports/audit.txt` | `67f9b2f5` | report_audit |
| `08_Reference/reports/precheck_outside.txt` | `7f602646` | report_precheck_outside |
| `08_Reference/reports/ui_brief_check.md` | `39907d3b` | report_ui_brief_check |
