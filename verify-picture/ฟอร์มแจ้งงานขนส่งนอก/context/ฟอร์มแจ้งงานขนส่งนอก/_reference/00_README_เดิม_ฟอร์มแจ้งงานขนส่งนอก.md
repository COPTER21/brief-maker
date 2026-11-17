# F-TMP-003 DevPack — ฟอร์มแจ้งงานขนส่งนอก (REQ-TMP-003)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 15 ข้อ (AI-DEFAULT 10) · พร้อมเริ่มทำ
- test case AI 32 เคส
- e2e_standard 21/21
- frd_lint BLOCK 0
- เทียบต้นฉบับ WARN 0.161

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K9 — เทียบต้นฉบับ WARN 0.161

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
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 13 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 18 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่มีการอนุมัติ
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · จำนวน ต้องมากกว่า 0 (บล็อก
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายการงานขนส่ง: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 20 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง  · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ)
- DEC-08 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติ none · admin role เห็นทั้งหมด
- DEC-09 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส OTN
- DEC-10 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `920d37fc` | prototype |
| `02_BRD/BRD_F-TMP-003.docx` | `96293e51` | brd_docx |
| `02_BRD/BRD_F-TMP-003.md` | `8fb1bd5f` | brd |
| `03_FRD/FRD_F-TMP-003_Pack/00_OVERVIEW.md` | `647f1994` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/01_UI.md` | `ff091ba1` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/02_API.md` | `7caeae6e` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/03_LOGIC.md` | `21e76837` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/04_DB.md` | `0d4c241d` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/05_RULES.md` | `9fb40a4c` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/06_TESTS.md` | `ded1ef55` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/07_LOCKED_DECISIONS.md` | `5d5701ef` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/INDEX.md` | `49fc1019` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/_SECTION_N.md` | `1124cddb` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/DOCCFG_BRIEF_F-TMP-003.md` | `73a35542` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/MDOC_BRIEF_OTN.md` | `4e32b030` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/NTF_BRIEF_F-TMP-003.md` | `5261419f` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/OTN.doccfg.yaml` | `358daad7` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/OTN.mdoc.yaml` | `7c4fe19c` | frd_pack |
| `03_FRD/FRD_F-TMP-003_Pack/declarations/OTN.ntf.yaml` | `0bb474d1` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-003.md` | `77a5e816` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `77554d26` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `1337e44f` | decisions_md |
| `05_Governance/DOCCFG_BRIEF_F-TMP-003.md` | `73a35542` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_OTN.md` | `4e32b030` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-003.md` | `5261419f` | ntf_brief |
| `05_Governance/OTN.doccfg.yaml` | `358daad7` | doccfg_yaml |
| `05_Governance/OTN.mdoc.yaml` | `7c4fe19c` | mdoc_yaml |
| `05_Governance/OTN.ntf.yaml` | `0bb474d1` | ntf_yaml |
| `05_Governance/decisions.yaml` | `d917ca32` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-003.md` | `fb174f40` | qa_audit |
| `06_Test/cases.json` | `b2d4d30d` | cases_json |
| `06_Test/testcase-F-TMP-003.html` | `0a666c7d` | testcases_uat |
| `06_Test/testcases-F-TMP-003.md` | `fc649cb0` | testcases_ai |
| `07_Print/FM-SAL-16_print-spec.md` | `36956afe` | print_spec |
| `07_Print/FM-SAL-16_template.html` | `c41c9c84` | print_extra_fm_sal_16_template |
| `07_Print/blank.data.json` | `f1010eb6` | print_data_blank_data |
| `07_Print/cancelled.data.json` | `6fa819ff` | print_data_cancelled_data |
| `07_Print/compare.json` | `1687099a` | report_compare |
| `07_Print/compare_side.png` | `4e4b6f91` | print_image_compare_side |
| `07_Print/draft.data.json` | `b210bd8c` | print_data_draft_data |
| `07_Print/form.tpl.html` | `674a9cab` | print_template |
| `07_Print/long-20rows.data.json` | `aa2908b8` | print_data_long_20rows_data |
| `07_Print/print_config.json` | `9128e3c1` | print_config |
| `07_Print/profile.json` | `ae1d60b3` | print_profile |
| `07_Print/render_data.py` | `4b32cba2` | print_extra_render_data |
| `07_Print/submitted.data.json` | `850bc80f` | print_data_submitted_data |
| `08_Reference/16. FM-SAL-16 ฟอร์มแจ้งงานขนส่งนอก.xlsx` | `d7c977be` | original_16_fm_sal_16 |
| `08_Reference/FORM_SPEC.check.json` | `667ad453` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `8ada6519` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-003.html` | `ffc2c036` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-003_v2.md` | `49bb9e5e` | prebrief |
| `08_Reference/RUN_LOG.md` | `b996d08e` | run_log |
| `08_Reference/SAMPLE.pdf` | `69c00e11` | original_sample |
| `08_Reference/page-1.png` | `4c5bdbc0` | original_page_1 |
| `08_Reference/page-2.png` | `c71e44db` | original_page_2 |
| `08_Reference/reports/_SECTION_N.md` | `1124cddb` | report_frd_lint |
| `08_Reference/reports/e2e_container_ref.json` | `7549ef45` | report_e2e |
| `08_Reference/shot_list.png` | `1bdc3fa1` | original_shot_list |
| `08_Reference/shot_submit_modal.png` | `d80e3688` | original_shot_submit_modal |
| `08_Reference/shot_view_detail.png` | `e6a61587` | original_shot_view_detail |
| `08_Reference/shot_view_pdf.png` | `37aacdef` | original_shot_view_pdf |
| `08_Reference/shot_view_sign.png` | `935b1aa7` | original_shot_view_sign |
| `08_Reference/shot_wiz1_filled.png` | `2823a613` | original_shot_wiz1_filled |
| `08_Reference/shot_wiz3_review.png` | `2d6cc965` | original_shot_wiz3_review |
