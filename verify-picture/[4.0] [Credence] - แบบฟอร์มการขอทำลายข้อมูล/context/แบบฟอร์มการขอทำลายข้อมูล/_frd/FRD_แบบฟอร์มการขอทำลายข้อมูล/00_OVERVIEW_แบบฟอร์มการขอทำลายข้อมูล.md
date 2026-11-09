# 00_OVERVIEW — F-TMP-003 แบบฟอร์มการขอทำลายข้อมูล (Data Destruction Request Form)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-003 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) · รหัส feature ชั่วคราว |
| Variant | **FULL** (fallback from BRD: pages=3, states=5, approval=Y, money=N → states ≥ 4) |
| Source | BRD-TMP-003 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-003_v2 · FORM_SPEC FM-ITS-02 · DECISIONS.lock (17 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0) |
| Module / Area | IT Support · Core Cube |
| Status | Ready for Dev (หลัง OQ-02/03 ปิด) · ทุกมติ [AI-DEFAULT] รอลูกค้ายืนยันในใบลงนาม |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ (แท็บ ทั้งหมด/รอฉันพิจารณา/คำขอของฉัน · กรอง · CSV) · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · DOA dynamic (ค่าเริ่ม 2 ขั้น ตรวจสอบ → อนุมัติ) · ไม่อนุมัติ→กลับร่าง · ยกเลิก · บันทึกการทำลายแล้ว (เจ้าหน้าที่ IT) · แนบไฟล์ · PDF FM-ITS-02 Replica · เลข DRITS
### Out of Scope
ลบ/ทำลายข้อมูลในระบบปลายทางอัตโนมัติ · retention schedule · ทะเบียนชุดข้อมูล · ทำซ้ำ · ประกาศ (DEC-02 · DEC-11)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้ร้องขอ (พนักงาน) | Maker | owner |
| ตรวจสอบ (ผู้บังคับบัญชา) | Checker · DOA ขั้น 1 | role-line-manager (relative) |
| อนุมัติ (ผู้จัดการฝ่าย IT) | Approver · DOA ขั้น 2 | role-mgr-it — **ยังไม่อยู่ใน DOA contract (OQ-03)** |
| เจ้าหน้าที่ IT (ผู้ทำลายข้อมูล · admin view) | Executor | role-it-officer — **ยังไม่อยู่ใน DOA contract (OQ-03)** |

## §0.5 Dependencies
### Upstream
HR · Employee (ชื่อ/ตำแหน่ง · อ่าน) · ผังองค์กร (ผู้บังคับบัญชา) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type DRITS · status · print_config) · Organization (header_snapshot · โลโก้)
### Downstream
ENG-NOTIFY (drits_cancelled · drits_ready_for_it · drits_destroyed) · ENG-DOC-STORE (approved_final) · ทะเบียนข้อมูล/retention (ประกาศ event `drits.destroyed` — **ไม่ยิงรอบนี้** DEC-02)

## §0.6 Pack
00_OVERVIEW · 01_UI · 02_API · 03_LOGIC · 04_DB · 05_RULES · 06_TESTS · 07_LOCKED_DECISIONS · INDEX · declarations/ (DOA · DOCCFG · NTF · MDOC ฉบับจริง)

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม (FORM_SPEC 10 ช่อง + ☐ 10/4/4) | ทุกช่อง | 01 §1.3 · 04 §4.1 |
| ลายเซ็น 4 จุด | ผู้ร้องขอ · ตรวจสอบ/อนุมัติ (ต่อขั้น DOA) · เจ้าหน้าที่ IT | 03 FN-08 · 01 §1.5 |
| BRD S-01..S-13 | ทุก story | 01 · 03 · 06 |
| BRD BR-01..13 · VR-01..11 · EC-01..11 | ทุกข้อ | 05 |
| DEC-01..17 | ทุกข้อ | 07 §7.0 |
