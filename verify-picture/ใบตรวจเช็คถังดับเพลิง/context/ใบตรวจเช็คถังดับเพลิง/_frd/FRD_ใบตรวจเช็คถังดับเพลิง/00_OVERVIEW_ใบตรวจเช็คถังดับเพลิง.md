# 00_OVERVIEW — F-TMP-001 ใบตรวจเช็คถังดับเพลิง (Fire Extinguisher Inspection Card)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-001 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2 · unattended) |
| Variant | **STANDARD** (fallback from BRD: pages=3, states=2, approval=N, money=N, repeat=Y) |
| Source | BRD-WHS-FEC-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-001_v2 · FORM_SPEC FM-WHS-03 · DECISIONS.lock (13 DEC) · feature.html (html-generator-v9 · audit FAIL 0 · self_audit PASS · jsdom smoke 27/27) |
| Module / Area | Inventory / Warehouse · Core Cube (แผนกคลังสินค้า) |
| Status | Ready for Dev (หลัง OQ-03/04 ปิด) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ · สร้างใบตรวจ (wizard 3 ขั้น) · ดู 3 แท็บ · บันทึกผลตรวจรายครั้ง · แก้แถววันเดียวกัน · ยกเลิกใบ · แจ้งผิดปกติ · แนบไฟล์ · CSV · PDF FM-WHS-03 Replica · เลขที่ FEC
### Out of Scope
ขั้นพิจารณา/ลงนาม (DEC-03 · DEC-07) · งานซ่อม/ผู้จำหน่าย · ทะเบียนถัง · รอบตรวจ/เตือนเลยรอบ · ทำซ้ำ (DEC-02 · DEC-10)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| เจ้าหน้าที่คลังสินค้า (ผู้ตรวจ) | Maker | owner / warehouse_staff |
| ผู้จัดการคลังสินค้า | Checker (รับแจ้ง) + Admin | role-mgr-wh |
| พนักงานนอกแผนก | Maker (จำกัดเฉพาะใบของตน) | owner |

## §0.5 Dependencies
F-EMP-001 (ผู้ตรวจ) · Warehouse Location master (ยังไม่มีรหัส — OQ-04) · F-DOCCFG + ENG-DOC-NUM · ENG-NOTIFY · Document Center · Organization (header_snapshot)

## §0.6 Open Questions
OQ-01 ตัวชี้วัด · OQ-02 ใบเซ็นยืนยัน DEC · OQ-03 archetype ไม่มี DOA · OQ-04 Warehouse Location master + รหัส feature · OQ-05 งานซ่อม Phase 2 · OQ-06 function_code (รายละเอียด BRD §13)

## §0.7 Data Classification
สูงสุด = Confidential (ชื่อผู้ตรวจ · PII) · ที่เหลือ Internal

## §0.8 Coverage Manifest (BRD → FRD)
| BRD | ไปที่ |
|---|---|
| §6 S-01..08 | 06 §6.1 AC-01..10 |
| §8 BR-01..12 · VR-01..06 | 05 §5.1 · §5.4 |
| §9 EC-01..08 | 05 §5.5 · 06 |
| §2.4 DEC-01..13 | 07 §7.0 |
| §10 Value stream | 02 §2.4 · 03 FN-07 |
ไม่มี requirement หล่น ✓
