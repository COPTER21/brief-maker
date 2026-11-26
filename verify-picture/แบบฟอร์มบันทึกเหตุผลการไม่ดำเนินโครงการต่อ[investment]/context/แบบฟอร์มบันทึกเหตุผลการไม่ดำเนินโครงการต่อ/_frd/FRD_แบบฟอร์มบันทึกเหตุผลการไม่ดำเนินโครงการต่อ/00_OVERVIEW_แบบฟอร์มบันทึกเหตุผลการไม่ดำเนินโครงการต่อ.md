# 00_OVERVIEW — F-TMP-002 แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ (Project Discontinuation Record · IVMJ)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-002 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (pages=3, states=4, approval=Y, money=N) |
| Source | BRD-IVM-IVMJ-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-002_v2 · FORM_SPEC FM-IVM-10 · DECISIONS.lock (15 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0 · self_audit PASS · e2e 21/21) |
| Module / Area | ฝ่ายบริหารการลงทุน (Investment) · Core Cube (Operation) |
| Status | Ready for Dev (หลัง OQ-03/04/06 ปิด) |
| Date | 2026-10-11 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-11 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · ตารางเหตุผล 8 คอลัมน์ · ข้อสรุป 6 ช่อง · DOA 2 ขั้น · ส่งกลับ→กลับร่าง · ผู้อนุมัติขั้นสุดท้ายยืนยัน/เปลี่ยนผล · ยกเลิก · แนบไฟล์ · PDF FM-IVM-10 Replica 2 หน้า · เลข IVMJ · CSV
### Out of Scope
ทะเบียนโครงการ / FM-IVM-01 (ชื่อโครงการกรอกเอง) · FM-IVM-11 ปิดงานอัตโนมัติ · เปลี่ยนสถานะโครงการในระบบอื่น (DEC-01/02) · ทำซ้ำเป็นฟีเจอร์ทางการ (DEC-11)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ | Maker | owner |
| ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน) | Checker | role-line-manager |
| ผู้อนุมัติ / รับทราบ (รองกรรมการผู้จัดการ / กรรมการผู้จัดการ) | Approver | role-gm |
| admin ฝ่ายบริหารการลงทุน | Monitor · admin view | (ยังไม่มี role id — OQ-04) |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · F-ORG-001 (OrgUnit · อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type IVMJ · status · print_config · revisions) · Organization (header/logo)
### Downstream
ENG-NOTIFY (ivmj_cancelled · ivmj_result_recorded) · ENG-DOC-STORE (approved_final) · ทะเบียนโครงการ/FM-IVM-11 (ประกาศ event `ivmj.approved` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
ตาม CUBE Core (API REST · PostgreSQL RLS · PDF render server-side จาก template logic-less เดียวกับ prototype)

## §0.7 Open Questions
OQ-01 ตัวชี้วัด · OQ-02 ใบเซ็นยืนยัน DEC (AI-DEFAULT) · OQ-03 role/module ใน DOA master · OQ-04 admin role id · OQ-05 ทะเบียนโครงการ · OQ-06 รหัส IVMJ/feature id/taxonomy (รายละเอียด BRD §13)

## §0.8 Coverage Manifest
| FORM_SPEC | ที่ |
|---|---|
| F01–F05 ข้อมูลโครงการ | 04 §4.2 · 01 P-02 การ์ด ① |
| F06–F13 ตารางเหตุผล | 04 ivm_discontinuation_reason · 01 P-02 การ์ด ② |
| F14–F19 ข้อสรุป | 04 §4.2 · 01 P-02 การ์ด ③ |
| S1–S3 ลายเซ็น | 03 FN-08 sign_rows · 05 BR-11 |
| control FM-IVM-10 Rev.00 | print_config · DOCCFG |
| anomalies 4 | DEC-12..15 → 05 |
