# F-TMP-008 DevPack — สรุปข้อมูลประเมินความพึงพอใจลูกค้า กลุ่ม MT (REQ-TMP-008)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 20 ข้อ (AI-DEFAULT 12) · พร้อมเริ่มทำ
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
| `07_Print` | แบบพิมพ์: template · data contract · PDF ทุกสถานะ · print-spec · print_config | 11 |
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 9 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- OQ-01 · ตัวชี้วัด · ลูกค้า · –
- OQ-02 · ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (ไม่มีผู้อนุมัติ · เกณฑ์ 95/80 · ถ้อยคำป้ายเหลือง/แดง) · Strike · ก่อน UAT
- OQ-03 · ต้องการผู้รับรองรายงานหรือไม่ (ถ้าต้องการ → DOA กลาง role-mgr-bu) · ลูกค้า + พี่เบิร์ด · –
- OQ-04 · SalesConfig.mt_* ใน Sales Configuration · ผูกช่องทางกับ Customer master · พี่เบิร์ด · ก่อน dev
- OQ-05 · ผูกแบบประเมินลูกค้า MT · Strike · –
- OQ-06 · แบบพิมพ์แนวตั้ง 2 หน้า (ต้นฉบับแนวนอน) · ลูกค้า · ก่อน UAT
- OQ-07 · F-TMP-008 / MTS / function_code ชั่วคราว · Strike · ก่อน register
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่มีการอนุมัติ
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "มาตรฐานที่กำหนด 95%" → SalesConfig.mt_csat_standard_pct
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: หัวข้อประเมิน: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 9 แถวตามกระดาษ
- DEC-06 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องทาง (คอลัมน์): ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 15 แถวตามกระดาษ
- DEC-07 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ข้อเสนอแนะ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 4 แถวตามกระดาษ
- DEC-08 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-09 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง  · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ)
- DEC-10 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติ none · admin role เห็นทั้งหมด
- DEC-11 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส MTS
- DEC-12 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `2e2f6fdd` | prototype |
| `02_BRD/BRD_F-TMP-008.docx` | `2ae36137` | brd_docx |
| `02_BRD/BRD_F-TMP-008.md` | `46764af7` | brd |
| `03_FRD/FRD_F-TMP-008_Pack/00_OVERVIEW.md` | `6ab72a34` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/01_UI.md` | `4ae1a003` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/02_API.md` | `8df062e7` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/03_LOGIC.md` | `830f7b21` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/04_DB.md` | `3c10ddff` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/05_RULES.md` | `1d4285ec` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/06_TESTS.md` | `7a52305e` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/07_LOCKED_DECISIONS.md` | `d89f3c31` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/INDEX.md` | `c28a47d8` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/_SECTION_N.md` | `bacb30ae` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/DOCCFG_BRIEF_F-TMP-008.md` | `e6f8179d` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/MDOC_BRIEF_MTS.md` | `cf5f5bb6` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/MTS.doccfg.yaml` | `963e3bc5` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/MTS.mdoc.yaml` | `c8813b67` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/MTS.ntf.yaml` | `e8a6272c` | frd_pack |
| `03_FRD/FRD_F-TMP-008_Pack/declarations/NTF_BRIEF_F-TMP-008.md` | `202047e5` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-008.md` | `89a4df46` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `d4c4241a` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `aa2704da` | decisions_md |
| `05_Governance/DOCCFG_BRIEF_F-TMP-008.md` | `e6f8179d` | doccfg_brief |
| `05_Governance/MDOC_BRIEF_MTS.md` | `cf5f5bb6` | mdoc_brief |
| `05_Governance/MTS.doccfg.yaml` | `963e3bc5` | doccfg_yaml |
| `05_Governance/MTS.mdoc.yaml` | `c8813b67` | mdoc_yaml |
| `05_Governance/MTS.ntf.yaml` | `e8a6272c` | ntf_yaml |
| `05_Governance/NTF_BRIEF_F-TMP-008.md` | `202047e5` | ntf_brief |
| `05_Governance/decisions.yaml` | `d804d81e` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-008.md` | `6379dade` | qa_audit |
| `06_Test/cases.json` | `18535785` | cases_json |
| `06_Test/testcase-F-TMP-008.html` | `ff5f6f3e` | testcases_uat |
| `06_Test/testcases-F-TMP-008.md` | `78c9bee6` | testcases_ai |
| `07_Print/FM-SAL-07_print-spec.md` | `07b98dbd` | print_spec |
| `07_Print/FM-SAL-07_template.html` | `91fa2172` | print_extra_fm_sal_07_template |
| `07_Print/cancelled.data.json` | `0819baa4` | print_data_cancelled_data |
| `07_Print/draft.data.json` | `13277651` | print_data_draft_data |
| `07_Print/final-allpass.data.json` | `19391b40` | print_data_final_allpass_data |
| `07_Print/final.data.json` | `7c69a4fd` | print_data_final_data |
| `07_Print/form.tpl.html` | `ac71c879` | print_template |
| `07_Print/long-12recs.data.json` | `23867ca2` | print_data_long_12recs_data |
| `07_Print/print_config.json` | `7b3fa797` | print_config |
| `07_Print/profile.json` | `d1fc7368` | print_profile |
| `07_Print/render_data.py` | `6a4bf1fe` | print_extra_render_data |
| `08_Reference/7. FM-SAL-07 แบบฟอร์มรายงานสรุปข้อมูล แบบประเมิณความพึงพอใจของลูกค้า MT.xlsx` | `5b3dd35e` | original_7_fm_sal_07_mt |
| `08_Reference/FORM_SPEC.check.json` | `39da3a8a` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `9a28a851` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-008.html` | `2528fa31` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-008_v2.md` | `ed377274` | prebrief |
| `08_Reference/RUN_LOG.md` | `995d3689` | run_log |
| `08_Reference/SAMPLE.pdf` | `ddb08232` | original_sample |
| `08_Reference/page-1.png` | `81cee38f` | original_page_1 |
| `08_Reference/reports/_SECTION_N.md` | `bacb30ae` | report_frd_lint |
