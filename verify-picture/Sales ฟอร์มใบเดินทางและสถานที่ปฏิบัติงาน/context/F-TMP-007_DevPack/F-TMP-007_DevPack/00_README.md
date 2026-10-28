# F-TMP-007 DevPack — ใบเดินทางและสถานที่ปฎิบัติงาน  สำหรับ General Trade (REQ-TMP-007)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 17 ข้อ (AI-DEFAULT 12) · พร้อมเริ่มทำ
- test case AI 38 เคส
- ไม่มี report e2e_standard (html-generator v9.2 #111)
- frd_lint BLOCK 0
- anchor ที่ไม่พบบนจอ 0

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
| `02_BRD` | BRD | 1 |
| `03_FRD` | FRD Pack | 8 |
| `04_UI_Brief` | UI Brief AS-BUILT | 1 |
| `05_Governance` | มติ (DECISIONS) + ใบประกาศ DOCCFG / DOA / MDOC / NTF | 11 |
| `06_Test` | test case AI + UAT ฉบับคน + QA audit | 3 |
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 10 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 12 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-line-manager · วงเง
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ยอดรวมทุกคอลัมน์รวมทุกแถวข
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการวันทำงาน: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 27 แถวตามกระดาษ
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: เอกสารที่แนบ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 3 แถวตามกระดาษ
- DEC-07 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-08 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-09 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-10 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-11 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส TWP
- DEC-12 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `114f887d` | prototype |
| `02_BRD/BRD_F-TMP-007.md` | `a3f86835` | brd |
| `03_FRD/FRD_F-TMP-007_Pack/00_OVERVIEW.md` | `ae1d752f` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/01_UI.md` | `b407e383` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/02_API.md` | `36a36a34` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/03_LOGIC.md` | `916cc7eb` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/04_DB.md` | `52a3fcc1` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/05_RULES.md` | `48091f60` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/06_TESTS.md` | `0c2d3cec` | frd_pack |
| `03_FRD/FRD_F-TMP-007_Pack/07_LOCKED_DECISIONS.md` | `1f58bea6` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-007.md` | `5c2bc91f` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `1616590e` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `01b69161` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-007.md` | `21595b1c` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-007.md` | `c39271cc` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_TWP.md` | `ab59416a` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-007.md` | `e20a491b` | ntf_brief |
| `05_Governance/TWP.doa.yaml` | `45078683` | doa_yaml |
| `05_Governance/TWP.doccfg.yaml` | `31ec9c57` | doccfg_yaml |
| `05_Governance/TWP.mdoc.yaml` | `ac4af308` | mdoc_yaml |
| `05_Governance/TWP.ntf.yaml` | `b441a8e9` | ntf_yaml |
| `05_Governance/decisions.yaml` | `35ad07c8` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-007.md` | `d3993a09` | qa_audit |
| `06_Test/cases.json` | `1b5bd254` | cases_json |
| `06_Test/testcases-F-TMP-007.md` | `577fb078` | testcases_ai |
| `07_Print/TWP_print-spec.md` | `578e8e68` | print_spec |
| `07_Print/TWP_template.html` | `d4102a4c` | print_extra_twp_template |
| `07_Print/approved-doa6steps.data.json` | `7d3e1fe8` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `4198686b` | print_data_approved_data |
| `07_Print/draft.data.json` | `26e5a4c4` | print_data_draft_data |
| `07_Print/form.tpl.html` | `b60fce1c` | print_template |
| `07_Print/long-34rows.data.json` | `686b833f` | print_data_long_34rows_data |
| `07_Print/print_config.json` | `60708a0c` | print_config |
| `07_Print/profile.json` | `f14bb415` | print_profile |
| `07_Print/rejected.data.json` | `7acefecc` | print_data_rejected_data |
| `08_Reference/FORM_SPEC.check.json` | `71377f48` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `ec1699de` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-007.html` | `9416267a` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-007_v2.md` | `acc75114` | prebrief |
| `08_Reference/RUN_LOG.md` | `b42b5c06` | run_log |
| `08_Reference/SAMPLE.pdf` | `8f1c57cd` | original_sample |
| `08_Reference/_crop_hdr.png` | `54c79fe3` | original_crop_hdr |
| `08_Reference/_crop_hdr2.png` | `a36aca41` | original_crop_hdr2 |
| `08_Reference/page-1.png` | `86d89c79` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `ff4a4ad4` | report_frd_lint |
| `08_Reference/reports/anchors.json` | `12d75e68` | report_anchors |
| `08_Reference/ฟอร์มใบเดินทางและสถานที่ปฏิบัติงาน.xlsx` | `8c1299c1` | original_ |
