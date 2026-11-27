# 00_OVERVIEW — F-TMP-011 แบบฟอร์มการบันทึกการยกระดับประเด็น (Issue Escalation Log · IVMI)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-011 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (pages=3, states=4, approval=Y, money=N) |
| Source | BRD-IVM-IVMI-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-011_v2 · FORM_SPEC FM-IVM-09 · DECISIONS.lock (18 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0 · self_audit PASS · smoke 56/56 · NO-BROWSER) |
| Module / Area | ฝ่ายบริหารการลงทุน (Investment) · Core Cube (Operation) |
| Status | Ready for Dev (หลัง OQ-03/04/06 ปิด) |
| Date | 2026-10-11 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-11 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · ชื่อโครงการ / ธุรกรรม · บันทึกการยกระดับประเด็น 10 คอลัมน์ · รหัส ESC- ระบบรัน · หมายเหตุบังคับเมื่อมีข้อสั่งการแล้ว/ยกเลิก · เตือนประเด็นเลยกำหนด · DOA 2 ขั้น · ส่งกลับ→กลับร่าง · ยกเลิก · แนบไฟล์ · PDF FM-IVM-09 Replica 2 หน้า · เลข IVMI · CSV
### Out of Scope
ทะเบียนโครงการ / FM-IVM-01 (ชื่อโครงการกรอกเอง) · ดึงประเด็นจาก FM-IVM-03 อัตโนมัติ (OQ-07) · อัปเดตผลการพิจารณาหลังอนุมัติ (OQ-08) · แจ้งเตือนกำหนดส่งรายวัน · เปลี่ยนสถานะในระบบอื่น (DEC-01/02) · ทำซ้ำ (DEC-11 ✗)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ | Maker | owner |
| ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน) | Checker | role-line-manager |
| ผู้อนุมัติ / รับทราบ (รองกรรมการผู้จัดการ / กรรมการผู้จัดการ / ผู้มีอำนาจ) | Approver | role-gm |
| admin ฝ่ายบริหารการลงทุน | Monitor · admin view | (ยังไม่มี role id — OQ-04) |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · F-ORG-001 (OrgUnit · อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type IVMI · status · print_config · revisions) · Organization (header/logo)
### Downstream
ENG-NOTIFY (ivmi_cancelled · ivmi_log_approved) · ENG-DOC-STORE (approved_final) · รายการประเด็นคงค้าง FM-IVM-03 (ประกาศ event `ivmi.approved` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
ตาม CUBE Core (API REST · PostgreSQL RLS · PDF render server-side จาก template logic-less เดียวกับ prototype)

## §0.7 Open Questions
OQ-01 ตัวชี้วัด · OQ-02 ใบเซ็นยืนยัน DEC (AI-DEFAULT · รวมช่องเพิ่มชื่อโครงการ) · OQ-03 role/module ใน DOA master · OQ-04 admin role id · OQ-05 ทะเบียนโครงการ · OQ-06 รหัส IVMI/feature id/taxonomy · OQ-07 ดึงประเด็นจาก FM-IVM-03 · OQ-08 อัปเดตผลการพิจารณาหลังอนุมัติ (รายละเอียด BRD §13)

## §0.8 Coverage Manifest
| FORM_SPEC | ที่ |
|---|---|
| F01 ชื่อโครงการ / ธุรกรรม (ช่องเพิ่ม) | 04 §4.2 project_name · 01 P-02 การ์ด ① |
| F02–F11 บันทึกการยกระดับประเด็น | 04 ivm_escalation_item · 01 P-02 การ์ด ② |
| choices esc_status | 05 BR-05 · 04 enum |
| S1–S3 ลายเซ็น | 03 FN-09 sign_rows · 05 BR-11 |
| control FM-IVM-09 Rev.00 | print_config · DOCCFG |
| anomalies 7 | DEC-12..18 → 05 |
