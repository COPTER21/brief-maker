# F-TMP-002 DevPack — แบบฟอร์มยืมสินทรัพย์ (REQ-TMP-002)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 13 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 65 เคส · UAT เก็บ 53 เคส
- e2e_standard 32/32
- frd_lint BLOCK 0

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K4 — microcopy ใน FRD 06 ที่ไม่พบใน prototype 2/14: ['ทะเบียนสินทรัพย์ซ้ำกับรายการที่ n', 'เลยกำหนดคืน n']

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
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 10 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (11 ข้อ) · Strike · ก่อน UAT
- OQ-03 · role admin ฝ่ายบริหารสินทรัพย์ / ผู้ให้ยืม = role-mgr-acc ตรง master DOA ไหม · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · Asset Master field (code/name/category) · พี่เบิร์ด · ก่อน dev
- OQ-05 · ตรวจยืมซ้อน + อัปเดตสถานะทะเบียน · ลูกค้า · –
- OQ-06 · รหัส feature/REQ จริง · taxonomy function_code · module enum F185 ไม่มี Asset · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-mgr-acc · วงเงิน: ไ
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · จำนวนที่ให้ยืม ≤ จำนวนที่ย
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการสินทรัพย์ที่ยืม: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 11 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส ALN
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `2371a765` | prototype |
| `02_BRD/BRD_F-TMP-002.docx` | `e1fa50e5` | brd_docx |
| `02_BRD/BRD_F-TMP-002.md` | `fce0889e` | brd |
| `03_FRD/FRD_F-TMP-002_Pack/00_OVERVIEW.md` | `77fe1618` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/01_UI.md` | `80ae0793` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/02_API.md` | `bb810969` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/03_LOGIC.md` | `7ecad8cc` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/04_DB.md` | `2f9271c6` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/05_RULES.md` | `a18ab070` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/06_TESTS.md` | `58c1badf` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/07_LOCKED_DECISIONS.md` | `c6d29d9d` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/INDEX.md` | `70b70d87` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/_SECTION_N.md` | `1d8ae7cd` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/ALN.doa.yaml` | `4f269f1a` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/ALN.doccfg.yaml` | `ea5defc0` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/ALN.mdoc.yaml` | `3353c4ec` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/ALN.ntf.yaml` | `f1dd5837` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/DOA_BRIEF_F-TMP-002.md` | `3bd50c08` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/DOCCFG_BRIEF_F-TMP-002.md` | `abc1451c` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/MDOC_BRIEF_ALN.md` | `20a43035` | frd_pack |
| `03_FRD/FRD_F-TMP-002_Pack/declarations/NTF_BRIEF_F-TMP-002.md` | `c6f8c939` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-002.md` | `f249e7af` | ui_brief |
| `05_Governance/ALN.doa.yaml` | `4f269f1a` | doa_yaml |
| `05_Governance/ALN.doccfg.yaml` | `ea5defc0` | doccfg_yaml |
| `05_Governance/ALN.mdoc.yaml` | `3353c4ec` | mdoc_yaml |
| `05_Governance/ALN.ntf.yaml` | `f1dd5837` | ntf_yaml |
| `05_Governance/DECISIONS.lock.json` | `8f23d1aa` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `eb8f7b03` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-002.md` | `3bd50c08` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-002.md` | `abc1451c` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_ALN.md` | `20a43035` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-002.md` | `c6f8c939` | ntf_brief |
| `05_Governance/decisions.yaml` | `cc01002b` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-002.md` | `8d5d4a4c` | qa_audit |
| `06_Test/cases.json` | `0fb8c68a` | cases_json |
| `06_Test/testcase-F-TMP-002.html` | `d3db3a2b` | testcases_uat |
| `06_Test/testcases-F-TMP-002.md` | `16aa44bc` | testcases_ai |
| `07_Print/approved-doa6steps.data.json` | `952e19a5` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `7b7df6aa` | print_data_approved_data |
| `07_Print/draft.data.json` | `673c5837` | print_data_draft_data |
| `07_Print/form.tpl.html` | `14992faa` | print_template |
| `07_Print/long-14rows.data.json` | `1b510fac` | print_data_long_14rows_data |
| `07_Print/print_config.json` | `808e8d03` | print_config |
| `07_Print/profile.json` | `7a150b7b` | print_profile |
| `07_Print/rejected.data.json` | `9d14aea9` | print_data_rejected_data |
| `07_Print/returned.data.json` | `b57ce8b8` | print_data_returned_data |
| `07_Print/แบบฟอร์มยืมสินทรัพย์_print-spec.md` | `0bf7bb1f` | print_spec |
| `07_Print/แบบฟอร์มยืมสินทรัพย์_template.html` | `e7529f64` | print_extra_template |
| `08_Reference/4. FM-ASM-04 แบบฟอร์มยืมสินทรัพย์.xlsx` | `d1a17390` | original_4_fm_asm_04 |
| `08_Reference/FORM_SPEC.check.json` | `6780dba9` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `ec6822e3` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-002.html` | `145aca8e` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-002_v2.md` | `d0c60215` | prebrief |
| `08_Reference/RUN_LOG.md` | `d1ac7d68` | run_log |
| `08_Reference/SAMPLE.pdf` | `68b84ce6` | original_sample |
| `08_Reference/page-1.png` | `1fd07f17` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `1d8ae7cd` | report_frd_lint |
| `08_Reference/reports/e2e_jsdom_report.json` | `cb2a40b6` | report_e2e |
