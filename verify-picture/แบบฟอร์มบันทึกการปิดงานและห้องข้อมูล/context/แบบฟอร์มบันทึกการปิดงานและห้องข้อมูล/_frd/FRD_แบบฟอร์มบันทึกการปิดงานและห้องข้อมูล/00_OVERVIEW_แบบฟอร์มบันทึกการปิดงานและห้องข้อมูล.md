# 00_OVERVIEW — F-TMP-003 แบบฟอร์มบันทึกการปิดงานและห้องข้อมูล (Transaction Closing & Data Room Record · IVMK)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-003 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (pages=3, states=4, approval=Y, money=N) |
| Source | BRD-IVM-IVMK-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-003_v2 · FORM_SPEC FM-IVM-11 · DECISIONS.lock (17 DEC · AI-DEFAULT 12) · feature.html (html-generator-v9.4 · audit FAIL 0 · self_audit PASS · e2e ยังไม่รัน [NO-BROWSER]) |
| Module / Area | ฝ่ายบริหารการลงทุน (Investment) · Core Cube (Operation) |
| Status | Ready for Dev (หลัง OQ-03/04/06 ปิด · e2e รอบเต็มบนเครื่องที่มี browser) |
| Date | 2026-10-11 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-11 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · สรุปการปิดงาน 5 ช่อง · รายการตรวจสอบ 8 ข้อจาก config (สถานะ 4 ค่า) · บทเรียน 4 คอลัมน์ · DOA 2 ขั้น · ส่งกลับ→กลับร่าง · ยกเลิก · แนบไฟล์ · PDF FM-IVM-11 Replica 2 หน้า · เลข IVMK · CSV
### Out of Scope
ปรับสิทธิ/ทำลายข้อมูลจริงในห้องข้อมูล (ทำนอกระบบ) · ทะเบียนโครงการ / FM-IVM-01 / FM-IVM-03 / FM-IVM-04 (กรอกเอง) · เปลี่ยนสถานะโครงการในระบบอื่น (DEC-01/02) · ทำซ้ำเป็นฟีเจอร์ทางการ (DEC-12) · หน้าตั้งค่ารายการตรวจสอบ (OQ-07)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ | Maker | owner |
| ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน) | Checker | role-line-manager |
| ผู้อนุมัติ / รับทราบ (รองกรรมการผู้จัดการ / กรรมการผู้จัดการ) | Approver | role-gm |
| admin ฝ่ายบริหารการลงทุน | Monitor · admin view | (ยังไม่มี role id — OQ-04) |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · F-ORG-001 (OrgUnit · อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type IVMK · status · print_config · revisions) · config ivmk.checklist_items (รายการตรวจสอบตั้งต้น · มีเวอร์ชัน) · Organization (header/logo)
### Downstream
ENG-NOTIFY (ivmk_cancelled · ivmk_closed_handover · ivmk_lesson_assigned) · ENG-DOC-STORE (approved_final) · ทะเบียนโครงการ/ห้องข้อมูล (ประกาศ event `ivmk.approved` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
ตาม CUBE Core (API REST · PostgreSQL RLS · PDF render server-side จาก template logic-less เดียวกับ prototype)

## §0.7 Open Questions
OQ-01 ตัวชี้วัด · OQ-02 ใบเซ็นยืนยัน DEC (AI-DEFAULT) · OQ-03 role/module ใน DOA master · OQ-04 admin role id · OQ-05 ทะเบียนโครงการ/ห้องข้อมูล · OQ-06 รหัส IVMK/feature id/taxonomy · OQ-07 ผู้ดูแล config รายการตรวจสอบ (รายละเอียด BRD §13)

## §0.8 Coverage Manifest
| FORM_SPEC | ที่ |
|---|---|
| F01–F05 สรุปการปิดงาน | 04 §4.2 ivm_closing · 01 P-02 การ์ด ① |
| F06–F10 รายการตรวจสอบ (K01 → config) | 04 ivm_closing_check · 01 P-02 การ์ด ② · 03 FN-01/FN-03 |
| F11–F14 บทเรียน | 04 ivm_closing_lesson · 01 P-02 การ์ด ③ |
| S1–S3 ลายเซ็น | 03 FN-08 sign_rows · 05 BR-11 |
| control FM-IVM-11 Rev.00 | print_config · DOCCFG |
| anomalies 5 | DEC-13..17 → 05 BR-02..05 · BR-14 |
