# 00_OVERVIEW — F-TMP-004 แบบฟอร์มใบแจ้งซ่อมอุปกรณ์คอมพิวเตอร์

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-004 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) · รหัส feature ชั่วคราว |
| Variant | **FULL** (fallback from BRD: pages=3, states=8, approval=Y, money=N → states ≥ 4) |
| Source | BRD-TMP-004 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-004_v2 · FORM_SPEC FM-ITS-06 · DECISIONS.lock (18 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0) |
| Module / Area | IT Support · Core Cube |
| Status | Ready for Dev (หลัง OQ-02/03/04 ปิด) · ทุกมติ [AI-DEFAULT] รอลูกค้ายืนยันในใบลงนาม |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ (แท็บ ทั้งหมด/งานที่ต้องทำ/ใบแจ้งซ่อมของฉัน · กรอง · CSV) · สร้าง/แก้ร่าง ส่วนที่ 1 (3 ขั้น) · ส่งแจ้งซ่อม · รับแจ้ง · บันทึกผลตรวจเช็ค (ส่วนที่ 2) · DOA dynamic (ค่าเริ่ม 1 ขั้น "อนุมัติโดย") · ไม่อนุมัติ→กลับร่างผลตรวจเช็ค · บันทึกผลการซ่อม · รับทราบผล→ปิดงาน · ยกเลิก · แนบไฟล์ · PDF FM-ITS-06 Replica 2 หน้า · เลข CRR
### Out of Scope
ผูกทะเบียนทรัพย์สิน · สร้าง PR จากตัวเลือกสั่งซื้อ · ติดตามร้านเคลมภายนอก · มอบหมายรายคน/SLA · ทำซ้ำ · ประกาศ (DEC-02 · DEC-11)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้แจ้งซ่อม (พนักงาน) | Maker | owner |
| เจ้าหน้าที่ IT (ผู้รับแจ้ง · ผู้ดำเนินการ · admin view) | Executor / Maker ของส่วนที่ 2 | role-it-officer — **ยังไม่อยู่ใน DOA contract (OQ-03)** |
| อนุมัติโดย (ผู้บังคับบัญชาของผู้ส่งอนุมัติ) | Approver | role-line-manager (relative) |

## §0.5 Dependencies
### Upstream
HR · Employee (ชื่อ/ตำแหน่ง · อ่าน) · ผังองค์กร (ผู้บังคับบัญชา) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type CRR · status · print_config) · Organization (header_snapshot · โลโก้)
### Downstream
ENG-NOTIFY (crr_reported · crr_received · crr_cancelled · crr_repaired) · ENG-DOC-STORE (approved_final) · ทะเบียนทรัพย์สิน / PR (ประกาศ event `crr.closed` — **ไม่ยิงรอบนี้** DEC-02)

## §0.6 Pack
00_OVERVIEW · 01_UI · 02_API · 03_LOGIC · 04_DB · 05_RULES · 06_TESTS · 07_LOCKED_DECISIONS · INDEX · declarations/ (DOA · DOCCFG · NTF · MDOC ฉบับจริง)

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม (FORM_SPEC 17 ช่อง + ☐ 4/5/2) | ทุกช่อง | 01 §1.3/§1.5 · 04 §4.1 |
| ลายเซ็น 6 จุด | ผู้แจ้งซ่อม · ผู้รับแจ้ง · ผู้ดำเนินการ + อนุมัติโดย (ต่อขั้น DOA) · ผู้ดำเนินการ · ผู้แจ้งซ่อม | 03 FN-12 · 01 §1.6 |
| BRD S-01..S-14 | ทุก story | 01 · 03 · 06 |
| BRD BR-01..14 · VR-01..13 · EC-01..14 | ทุกข้อ | 05 |
| DEC-01..18 | ทุกข้อ | 07 §7.0 |
