# 00_OVERVIEW — F-TMP-007 ใบคำร้องขอดำเนินการด้านเอกสาร (Document Action Request · DAR Form)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-007 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) · รหัส feature ชั่วคราว |
| Variant | **FULL** (fallback from BRD: pages=3, states=5, approval=Y, money=N → states ≥ 4) |
| Source | BRD-TMP-007 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-007_v2 · FORM_SPEC FM-CCC-03 · DECISIONS.lock (16 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0) · print/ (thai-doc v2.2 R9+R10) |
| Module / Area | Policy Center · Document Control (CCC) · Core Cube |
| Status | Ready for Dev (หลัง OQ-02/03 ปิด) · ทุกมติ [AI-DEFAULT] รอลูกค้ายืนยันในใบลงนาม |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ (แท็บ ทั้งหมด/รอฉันดำเนินการ/ใบ DAR ของฉัน · กรอง · CSV) · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · DOA dynamic (ค่าเริ่ม 4 ขั้น ผู้ตรวจสอบ → ผู้อนุมัติ → ผู้ควบคุมเอกสาร → ผู้จัดการฝ่ายสำนักเลขานุการบริษัท) · ไม่อนุมัติ→กลับร่าง · ยกเลิก · แจ้งหน่วยงานแจกจ่ายเมื่ออนุมัติครบ · ลงนามรับเอกสารควบคุม · เอกสารเกี่ยวข้องไม่จำกัดแถว · แนบไฟล์ · PDF FM-CCC-03 Replica 2 หน้า · เลข DAR
### Out of Scope
ขึ้นทะเบียน/แก้ทะเบียนเอกสารควบคุมจริง (OQ-06 · DEC-01/02) · ทำซ้ำ · ประกาศ (DEC-11)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ (ผู้เขียนใบ DAR) | Maker | owner |
| ผู้ตรวจสอบ (ผู้บังคับบัญชา) | Checker · DOA ขั้น 1 | role-line-manager (relative) |
| ผู้อนุมัติ (ผู้บริหารสายงาน) | Approver · DOA ขั้น 2 | role-mgr-bu |
| ผู้ควบคุมเอกสาร (Document Control Center · admin role) | Approver · DOA ขั้น 3 · admin view · บันทึกลงนามรับ | role-doc-controller — **ยังไม่อยู่ใน DOA contract (OQ-03)** |
| ผู้จัดการฝ่ายสำนักเลขานุการบริษัท | Approver · DOA ขั้น 4 | role-mgr-ocs — **ยังไม่อยู่ใน DOA contract (OQ-03)** |

## §0.5 Dependencies
### Upstream
HR · Employee (ผู้เขียน/ฝ่าย/แผนก · อ่าน) · ผังองค์กร (ผู้บังคับบัญชา) · Organization (หน่วยงานแจกจ่าย · header_snapshot · โลโก้) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type DAR · status · print_config)
### Downstream
ENG-NOTIFY (dar_cancelled · dar_distributed · dar_received) · ENG-DOC-STORE (approved_final) · ทะเบียนเอกสารควบคุม Policy Center (ประกาศ event `dar.approved` — **ไม่ยิงรอบนี้** DEC-02)

## §0.6 Pack
00_OVERVIEW · 01_UI · 02_API · 03_LOGIC · 04_DB · 05_RULES · 06_TESTS · 07_LOCKED_DECISIONS · INDEX · declarations/ (DOA · DOCCFG · NTF · MDOC ฉบับจริง)

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม (FORM_SPEC 17 ช่อง + ตัวเลือก 5 กลุ่ม) | ทุกช่อง | 01 §1.3 · 04 §4.1–4.3 |
| แถวซ้ำ เอกสารที่ต้องจัดทำ/ทบทวน (14 บนกระดาษ) | ไม่จำกัด · PDF ≥14 | 01 §1.3 · 04 §4.2 · 03 FN-07 |
| ลายเซ็น 6 จุด | ผู้จัดทำ · 4 ขั้นพิจารณา (ต่อขั้น DOA) · ลงนามรับเอกสารควบคุม (ข้อความระบบ) | 03 FN-07/FN-08 · 01 §1.5 |
| BRD S-01..S-16 | ทุก story | 01 · 03 · 06 |
| BRD BR-01..17 · VR-01..13 · EC-01..17 | ทุกข้อ | 05 |
| DEC-01..16 | ทุกข้อ | 07 §7.0 |

## §0.13 Open Questions (จาก BRD §13)
OQ-01 ตัวชี้วัด · OQ-02 ใบลงนามยืนยัน DEC AI-DEFAULT · OQ-03 role-doc-controller / role-mgr-ocs นอก DOA contract · OQ-04 หน่วยงานแจกจ่ายชุดซ้ำ · OQ-05 ผู้รับกดลงนามรับเอง · OQ-06 เชื่อมทะเบียนเอกสารควบคุม · OQ-07 รหัส feature จริง + function_code
