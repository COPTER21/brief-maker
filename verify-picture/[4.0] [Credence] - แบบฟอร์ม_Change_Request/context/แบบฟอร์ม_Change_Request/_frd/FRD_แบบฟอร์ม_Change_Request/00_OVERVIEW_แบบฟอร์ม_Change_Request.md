# 00_OVERVIEW — F-TMP-005 แบบฟอร์ม Change Request (Change Request Form)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-005 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) · รหัส feature ชั่วคราว |
| Variant | **FULL** (fallback from BRD: pages=3, states=4, approval=Y, money=N → states ≥ 4) |
| Source | BRD-TMP-005 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-005_v2 · FORM_SPEC FM-ITS-07 · DECISIONS.lock (17 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0) |
| Module / Area | IT Support · Core Cube |
| Status | Ready for Dev (หลัง OQ-02/03 ปิด) · ทุกมติ [AI-DEFAULT] รอลูกค้ายืนยันในใบลงนาม |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ (แท็บ ทั้งหมด/รอฉันพิจารณา/คำขอของฉัน · กรอง · CSV) · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · DOA dynamic (ค่าเริ่ม 2 ขั้น ตรวจสอบโดย → อนุมัติโดย) · ไม่อนุมัติ→กลับร่าง · ยกเลิก · แจ้งเจ้าหน้าที่ IT เมื่ออนุมัติครบ · แนบไฟล์ · PDF FM-ITS-07 Replica · เลข ITCR
### Out of Scope
บันทึกผลการดำเนินการ/ปิดงาน (OQ-04) · ปฏิทินการเปลี่ยนแปลง · CMDB · ทำซ้ำ · ประกาศ (DEC-02 · DEC-11)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้ขอ ("ผู้ขอซื้อ" บนกระดาษ) | Maker | owner |
| ตรวจสอบโดย (ผู้บังคับบัญชา) | Checker · DOA ขั้น 1 | role-line-manager (relative) |
| อนุมัติโดย (ผู้จัดการฝ่าย IT) | Approver · DOA ขั้น 2 | role-mgr-it — **ยังไม่อยู่ใน DOA contract (OQ-03)** |
| เจ้าหน้าที่ IT (admin view · ผู้รับแจ้ง) | — | role-it-officer — **ยังไม่อยู่ใน DOA contract (OQ-03)** |

## §0.5 Dependencies
### Upstream
HR · Employee (ชื่อ/ตำแหน่ง · อ่าน) · ผังองค์กร (ผู้บังคับบัญชา) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type ITCR · status · print_config) · Organization (header_snapshot · โลโก้)
### Downstream
ENG-NOTIFY (itcr_cancelled · itcr_approved_for_it) · ENG-DOC-STORE (approved_final) · ทะเบียนการเปลี่ยนแปลง/CMDB (ประกาศ event `itcr.approved` — **ไม่ยิงรอบนี้** DEC-02)

## §0.6 Pack
00_OVERVIEW · 01_UI · 02_API · 03_LOGIC · 04_DB · 05_RULES · 06_TESTS · 07_LOCKED_DECISIONS · INDEX · declarations/ (DOA · DOCCFG · NTF · MDOC ฉบับจริง)

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม (FORM_SPEC 11 ช่อง + ☐ 5) | ทุกช่อง | 01 §1.3 · 04 §4.1 |
| ลายเซ็น 3 จุด | ผู้ขอซื้อ · ตรวจสอบโดย/อนุมัติโดย (ต่อขั้น DOA) | 03 FN-07 · 01 §1.5 |
| BRD S-01..S-11 | ทุก story | 01 · 03 · 06 |
| BRD BR-01..11 · VR-01..11 · EC-01..11 | ทุกข้อ | 05 |
| DEC-01..17 | ทุกข้อ | 07 §7.0 |

## §0.13 Open Questions (จาก BRD §13)
OQ-01 ตัวชี้วัด · OQ-02 ใบลงนามยืนยัน DEC AI-DEFAULT · OQ-03 role-mgr-it / role-it-officer นอก DOA contract · OQ-04 บันทึกผลการดำเนินการ · OQ-05 ป้าย "ผู้ขอซื้อ" / ตัวตน "ตรวจสอบโดย" · OQ-06 รหัส feature จริง + function_code
