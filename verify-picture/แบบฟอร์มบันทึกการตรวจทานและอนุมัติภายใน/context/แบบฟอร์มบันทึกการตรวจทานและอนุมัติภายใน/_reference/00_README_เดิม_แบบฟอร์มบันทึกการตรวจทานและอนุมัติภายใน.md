# F-TMP-006 DevPack — แบบฟอร์มบันทึกการตรวจทานและอนุมัติภายใน (REQ-TMP-006)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 18 ข้อ (AI-DEFAULT 12) · พร้อมเริ่มทำ
- test case AI 32 เคส
- e2e_standard 21/21
- frd_lint BLOCK 0
- anchor ที่ไม่พบบนจอ 0
- เทียบต้นฉบับ WARN 0.367

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K9 — เทียบต้นฉบับ WARN 0.367

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
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 13 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 15 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (12 ข้อ) · Strike · ก่อน UAT
- OQ-03 · role กรรมการผู้จัดการ/ผู้มีอำนาจตามตารางอำนาจอนุมัติ ไม่มีใน DOA master (ใช้ role-gm ชั่วคราว) · ผู้ตรวจสอบ "รองกรรมการผู้จัดการ" ขั้นเดียวกับผู้จัดการฝ่ายหรือแยก · Strike + พี่เบิร์ด · ก่อน wire
- OQ-04 · ReviewApprovalConfig มีหรือยัง / เจ้าของ · พี่เบิร์ด · ก่อน dev
- OQ-05 · ผูกกับโครงการ / FM-BDM-05 ไหม · ลูกค้า · –
- OQ-06 · ผลการตรวจทาน ข้อความอิสระหรือรายการตัวเลือก · ลูกค้า · –
- OQ-07 · รหัส IRV ชนไหม · taxonomy function_code · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "สถานะ: เปิด / กำลังดำเนินการ / ปิด" → ReviewApprovalCon
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: บันทึกการตรวจทาน: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 10 แถวตามกระดาษ
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: บันทึกการอนุมัติภายใน: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 3 แถวตามกระดาษ
- DEC-07 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-08 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-09 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-10 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-11 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส IRV
- DEC-12 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `ca0c892a` | prototype |
| `02_BRD/BRD_F-TMP-006.docx` | `272f524e` | brd_docx |
| `02_BRD/BRD_F-TMP-006.md` | `12d13821` | brd |
| `03_FRD/FRD_F-TMP-006_Pack/00_OVERVIEW.md` | `4b686b8d` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/01_UI.md` | `8d43a42d` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/02_API.md` | `34a41b87` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/03_LOGIC.md` | `af2c0a33` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/04_DB.md` | `54afc844` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/05_RULES.md` | `8eb8e61d` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/06_TESTS.md` | `32efee35` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/07_LOCKED_DECISIONS.md` | `721ae82d` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/INDEX.md` | `b09daaf5` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/_SECTION_N.md` | `16290f42` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/DOA_BRIEF_F-TMP-006.md` | `8d196b0d` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/DOCCFG_BRIEF_F-TMP-006.md` | `388a4706` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/IRV.doa.yaml` | `a16847ed` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/IRV.doccfg.yaml` | `d28e43fd` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/IRV.mdoc.yaml` | `77ed2d2a` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/IRV.ntf.yaml` | `6f2b3f16` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/MDOC_BRIEF_IRV.md` | `93c35e0d` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/declarations/NTF_BRIEF_F-TMP-006.md` | `c437dd36` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-006.md` | `2a91387b` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `612be3c0` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `6ef41f68` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-006.md` | `8d196b0d` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-006.md` | `388a4706` | doccfg_brief |
| `05_Governance/IRV.doa.yaml` | `a16847ed` | doa_yaml |
| `05_Governance/IRV.doccfg.yaml` | `d28e43fd` | doccfg_yaml |
| `05_Governance/IRV.mdoc.yaml` | `77ed2d2a` | mdoc_yaml |
| `05_Governance/IRV.ntf.yaml` | `6f2b3f16` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_IRV.md` | `93c35e0d` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-006.md` | `c437dd36` | ntf_brief |
| `05_Governance/decisions.yaml` | `648c9441` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-006.md` | `8d138850` | qa_audit |
| `06_Test/cases.json` | `a4383484` | cases_json |
| `06_Test/testcase-F-TMP-006.html` | `d7749c24` | testcases_uat |
| `06_Test/testcases-F-TMP-006.md` | `1c0a0ef9` | testcases_ai |
| `07_Print/FM-BDM-06_template.html` | `8402ead5` | print_extra_fm_bdm_06_template |
| `07_Print/IRV_print-spec.md` | `c14cef3e` | print_spec |
| `07_Print/approved-doa6steps.data.json` | `25e1908b` | print_data_approved_doa6steps_data |
| `07_Print/approved.data.json` | `6534ef00` | print_data_approved_data |
| `07_Print/compare.json` | `5ab32773` | report_compare |
| `07_Print/compare_overlay.png` | `a3e07187` | print_image_compare_overlay |
| `07_Print/compare_side.png` | `e01579be` | print_image_compare_side |
| `07_Print/draft.data.json` | `9a62e29b` | print_data_draft_data |
| `07_Print/form.tpl.html` | `8664b693` | print_template |
| `07_Print/long-24rows.data.json` | `ada3babf` | print_data_long_24rows_data |
| `07_Print/print_config.json` | `80da3772` | print_config |
| `07_Print/profile.json` | `ba81bae8` | print_profile |
| `07_Print/rejected.data.json` | `53c5edc8` | print_data_rejected_data |
| `08_Reference/6. FM-BDM-06 แบบฟอร์มบันทึกการตรวจทานและอนุมัติภายใน.xlsx` | `928bd957` | original_6_fm_bdm_06 |
| `08_Reference/FORM_SPEC.check.json` | `c6352df0` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `97b74e98` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-006.html` | `dae7ce00` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-006_v2.md` | `1eff7f99` | prebrief |
| `08_Reference/RUN_LOG.md` | `d34c1f45` | run_log |
| `08_Reference/SAMPLE.pdf` | `d1c1348e` | original_sample |
| `08_Reference/page-1.png` | `e130c5fa` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `16290f42` | report_frd_lint |
| `08_Reference/reports/anchors.json` | `58d0eba4` | report_anchors |
| `08_Reference/reports/e2e_report.json` | `1db788a8` | report_e2e |
| `08_Reference/shot_list.png` | `ec2b2b28` | original_shot_list |
| `08_Reference/shot_pdf.png` | `15e30deb` | original_shot_pdf |
| `08_Reference/shot_view.png` | `ce44be15` | original_shot_view |
| `08_Reference/shot_wizard.png` | `1212fcc8` | original_shot_wizard |
