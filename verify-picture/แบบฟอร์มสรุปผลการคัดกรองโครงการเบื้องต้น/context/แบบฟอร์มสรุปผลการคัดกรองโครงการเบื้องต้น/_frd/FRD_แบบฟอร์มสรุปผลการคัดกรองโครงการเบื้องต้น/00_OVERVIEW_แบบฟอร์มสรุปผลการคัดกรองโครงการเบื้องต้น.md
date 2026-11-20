# 00_OVERVIEW — F-TMP-003 แบบฟอร์มสรุปผลการคัดกรองโครงการเบื้องต้น (Preliminary Project Screening)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-003 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2 · โหมดไม่เฝ้า) |
| Variant | **FULL** (pages=3, states=4, approval=Y, repeat=Y) |
| Source | BRD-TMP-003-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-003_v2 · FORM_SPEC FM-BDM-03 · DECISIONS.lock (17 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0 · e2e 21/21) |
| Module / Area | Business Development (ฝ่ายพัฒนาธุรกิจ) |
| Status | Ready for Dev (หลัง OQ-03/04 ปิด · ลูกค้ายืนยัน AI-DEFAULT ก่อน UAT) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (unattended) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · การประเมิน 8 เกณฑ์ (น้ำหนักจาก config) · คะแนนถ่วงน้ำหนัก/คะแนนรวม/ผลเสนอ คำนวณ · ข้อสรุปการคัดกรอง 6 หัวข้อ · DOA 2 ขั้น · ไม่ผ่าน→กลับร่าง · ยกเลิก · แนบไฟล์ · PDF FM-BDM-03 Replica 2 หน้า · เลข SCR · CSV · แจ้งเตือนผลไม่ดำเนินการต่อ
### Out of Scope
ผูกโครงการ FM-BDM-01 (OQ-05) · สร้าง FM-BDM-04 อัตโนมัติ (OQ-07 · DEC-02) · หน้าตั้งค่า ScreeningCriteria · ทำซ้ำ · ประกาศ · ส่งต่อระบบอื่น (DEC-02)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ | Maker | owner |
| ผู้ตรวจสอบ (ผู้จัดการฝ่ายพัฒนาธุรกิจ) | Checker | role-line-manager |
| ผู้อนุมัติ / รับทราบ (รองกรรมการผู้จัดการ / ผู้มีอำนาจตามตารางอำนาจอนุมัติ) | Approver | role-gm (ชั่วคราว · OQ-03) |
| admin ฝ่ายพัฒนาธุรกิจ | Monitor · เห็นทั้งหมด · ยกเลิกได้ | admin_role |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · F-ORG-001 (OrgUnit · อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type SCR · status · print_config · form_revisions) · ScreeningCriteria config (items · score_max · recommend_bands) · Company Master (logo/header)
### Downstream
ENG-NOTIFY (scr_cancelled · scr_not_proceed_approved) · ENG-DOC-STORE (approved_final) · FM-BDM-04 (ผู้ใช้ทำเอง · ไม่ส่งต่ออัตโนมัติ)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/project-screening` (อ้าง feature.html เป็น source of truth) · BE: REST `/api/v1/project-screenings` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less · 2 หน้า) + data contract (03 FN-08)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: เอกสาร/ผลคัดกรอง · Confidential(PII): ชื่อผู้จัดทำ/ผู้พิจารณา snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (11 ข้อ) | Strike | ก่อน UAT |
| OQ-03 | role รองกรรมการผู้จัดการ / ผู้มีอำนาจตามตารางอำนาจอนุมัติ ไม่มีใน DOA master (ใช้ role-gm ชั่วคราว) | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | ScreeningCriteria config มีหรือยัง / เจ้าของ | พี่เบิร์ด | ก่อน dev |
| OQ-05 | ผูกกับโครงการ FM-BDM-01 ไหม | ลูกค้า | – |
| OQ-06 | รหัส SCR ชนไหม · taxonomy function_code | Strike | ก่อน register |
| OQ-07 | ผลไม่ดำเนินการต่อ → สร้าง FM-BDM-04 อัตโนมัติไหม | ลูกค้า | – |

## §0.9 Glossary
คะแนนถ่วงน้ำหนัก = น้ำหนัก (%) × คะแนน ÷ คะแนนเต็ม (5) · คะแนนรวมถ่วงน้ำหนัก = ผลรวม 8 เกณฑ์ (เต็ม 100) · ผลเสนอจากคะแนน = ช่วงตาม recommend_bands · ผลการพิจารณา = ที่ผู้จัดทำเลือก (อาจต่างจากผลเสนอได้พร้อมเหตุผล)

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED (DEC) · INDEX · declarations/

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม F01–F14 (FORM_SPEC) | criterion · weight · score · weighted_score · rationale · risk_condition · total_score · recommendation · strengths · concerns · info_needed · decision · conditions · next_steps | 01 §1.2 P-02 · 04 §4.2 · 03 FN-02/FN-08 |
| ค่าคงที่บนกระดาษ 3 ชุด | เกณฑ์+น้ำหนัก · เกณฑ์ผลเสนอ · สเกลคะแนน | ScreeningCriteria config · 03 FN-02/08 · 05 BR-03/04 |
| ลายเซ็น S1–S3 | ผู้จัดทำ + DOA 2 ขั้น | 03 FN-04/05/08 · 05 BR-12 |
| BRD S-01..S-10 | stories | 06 AC-01..AC-14 |
| BRD BR-01..13 · VR-01..05 · EC-01..09 | rules | 05 §5.1 / §5.4 / §5.5 |
| DEC-01..17 | มติ | 07 §7.0 |
| declaration | DOA · NTF · DOCCFG · MDOC | declarations/ · 03 FN-03/05/07/09 |
| หน้าจอ HTML | P-01 · P-02 · P-03 · M-01..05 | 01 §1.1 |
ไม่มี requirement หล่น
