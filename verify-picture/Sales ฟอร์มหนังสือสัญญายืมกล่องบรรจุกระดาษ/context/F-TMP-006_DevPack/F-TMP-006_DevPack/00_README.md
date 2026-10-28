# F-TMP-006 DevPack — หนังสือสัญญายืม (กล่องบรรจุกระดาษ) (REQ-TMP-006)

> ชุดส่ง dev = **01_Prototype (หน้าจอจริง) + 03_FRD (ระบบ) + 04_UI_Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ · ประกอบจาก FEATURE_MANIFEST.json (devpack-assembler)

**สถานะ:** ✅ READY — consistency BLOCK 0 · WARN 1
- มติ 16 ข้อ (AI-DEFAULT 11) · พร้อมเริ่มทำ
- test case AI 32 เคส
- e2e_standard None/0
- frd_lint BLOCK 0

**ข้อที่ยังไม่ผ่าน / ต้องรู้:**
- WARN K3 — run_log: ไฟล์ถูกแก้หลังลงทะเบียน — รัน manifest_scan ใหม่

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
| `08_Reference` | PREBRIEF · FORM_SPEC · สรุปผลกระทบ · ต้นฉบับลูกค้า · report | 11 |

## เรื่องค้าง (ต้องปิดก่อน dev / deploy)
- DEC-01 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: อนุมัติแล้วไม่เปลี่ยนค่าในระบบ
- DEC-02 (G1) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง)
- DEC-03 (G2) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-mgr-sales · วงเงิน:
- DEC-04 (G3) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ค่าคงที่อ่านจาก config: "ร้อยละ 10 (สิบ) ของจำนวนที่ติดตั้งทั้งหมดต่อปี" → Sales
- DEC-05 (G4) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: รายละเอียดกล่องที่สนับสนุน: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 1 แถวตามกระดาษ
- DEC-06 (G5) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ)
- DEC-07 (G6) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณา
- DEC-08 (G7) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ 
- DEC-09 (G8) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด
- DEC-10 (G9) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ออกเลขเมื่อบันทึกครั้งแรก · รหัส LOA
- DEC-11 (G10) ใช้ค่าเสนอ — ยืนยันกับลูกค้า: ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV

## md5
| ไฟล์ | md5 | artifact |
|---|---|---|
| `01_Prototype/feature.html` | `eb35383d` | prototype |
| `02_BRD/BRD_F-TMP-006.md` | `351ead31` | brd |
| `03_FRD/FRD_F-TMP-006_Pack/00_OVERVIEW.md` | `63e4108b` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/01_UI.md` | `fa383504` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/02_API.md` | `9c44d7b4` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/03_LOGIC.md` | `65c0936c` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/04_DB.md` | `165f3bb6` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/05_RULES.md` | `76dba3d1` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/06_TESTS.md` | `d233514b` | frd_pack |
| `03_FRD/FRD_F-TMP-006_Pack/07_LOCKED_DECISIONS.md` | `dd9c51f8` | frd_pack |
| `04_UI_Brief/UI_BRIEF_F-TMP-006.md` | `3ae17082` | ui_brief |
| `05_Governance/DECISIONS.lock.json` | `f96e7e06` | decisions_lock |
| `05_Governance/DECISIONS.lock.md` | `d3888a04` | decisions_md |
| `05_Governance/DOA_BRIEF_F-TMP-006.md` | `42c23a7c` | doa_brief |
| `05_Governance/DOCCFG_BRIEF_F-TMP-006.md` | `63b2083b` | doccfg_brief |
| `05_Governance/LOA.doa.yaml` | `43ac6c3a` | doa_yaml |
| `05_Governance/LOA.doccfg.yaml` | `e78eb53a` | doccfg_yaml |
| `05_Governance/LOA.mdoc.yaml` | `225a0a97` | mdoc_yaml |
| `05_Governance/LOA.ntf.yaml` | `4620bbd3` | ntf_yaml |
| `05_Governance/MDOC_BRIEF_LOA.md` | `c635b386` | mdoc_brief |
| `05_Governance/NTF_BRIEF_F-TMP-006.md` | `9820c5f8` | ntf_brief |
| `05_Governance/decisions.yaml` | `f4354fbe` | decisions_yaml |
| `06_Test/QA_AUDIT_F-TMP-006.md` | `6ee82dad` | qa_audit |
| `06_Test/cases.json` | `f5d2632b` | cases_json |
| `06_Test/testcases-F-TMP-006.md` | `8cac2093` | testcases_ai |
| `07_Print/LOA_print-spec.md` | `650ed168` | print_spec |
| `07_Print/LOA_template.html` | `7e6cbe18` | print_extra_loa_template |
| `07_Print/approved.data.json` | `18e3bfdb` | print_data_approved_data |
| `07_Print/doa-6steps.data.json` | `8706c4d7` | print_data_doa_6steps_data |
| `07_Print/draft.data.json` | `756e09b5` | print_data_draft_data |
| `07_Print/form.tpl.html` | `051e25a3` | print_template |
| `07_Print/long-13rows-4signs.data.json` | `fea1627c` | print_data_long_13rows_4signs_data |
| `07_Print/print_config.json` | `261eb307` | print_config |
| `07_Print/profile.json` | `e2ac3183` | print_profile |
| `07_Print/rejected.data.json` | `67e73a4b` | print_data_rejected_data |
| `08_Reference/FORM_SPEC.check.json` | `a50ccfa1` | form_spec_check |
| `08_Reference/FORM_SPEC.json` | `66cfb7a6` | form_spec |
| `08_Reference/IMPACT_SUMMARY_REQ-TMP-006.html` | `8f6e8117` | impact_summary |
| `08_Reference/PREBRIEF_REQ-TMP-006_v2.md` | `43c5832e` | prebrief |
| `08_Reference/RUN_LOG.md` | `99258a39` | run_log |
| `08_Reference/SAMPLE.pdf` | `849791e7` | original_sample |
| `08_Reference/page-1.png` | `910dd8b7` | original_page_1 |
| `08_Reference/page-2.png` | `ae11eda3` | original_page_2 |
| `08_Reference/reports/_SECTION_N.md` | `b94cedc6` | report_frd_lint |
| `08_Reference/reports/e2e_report.json` | `63d2c46d` | report_e2e |
| `08_Reference/ฟอร์มหนังสือสัญญายืมกล่องบรรจุกระดาษ.doc` | `106eac16` | original_ |
