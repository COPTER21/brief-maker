# 00_OVERVIEW — F-TMP-004 แบบฟอร์มตารางติดตามงานและแผนฐาน (Deal Tracker and Baseline Plan · IVMB)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-004 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (pages=3, states=4, approval=Y, money=N) |
| Source | BRD-IVM-IVMB-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-004_v2 · FORM_SPEC FM-IVM-02 · DECISIONS.lock (18 DEC · AI-DEFAULT 12) · feature.html (html-generator-v9.4 · audit FAIL 0 · self_audit PASS · smoke 36/36 · NO-BROWSER) |
| Module / Area | ฝ่ายบริหารการลงทุน (Investment) · Core Cube (Operation) |
| Status | Ready for Dev (หลัง OQ-03/04/06 ปิด) |
| Date | 2026-10-11 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-11 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · ชื่อโครงการ / ธุรกรรม · แผนฐานและหมุดหมายสำคัญ 10 คอลัมน์ · รายการติดตามงาน 10 คอลัมน์ · ความคลาดเคลื่อน (วัน) คำนวณอัตโนมัติ · DOA 2 ขั้น · ส่งกลับ→กลับร่าง · ยกเลิก · แนบไฟล์ · PDF FM-IVM-02 Replica 2 หน้า · เลข IVMB · CSV
### Out of Scope
ทะเบียนโครงการ / FM-IVM-01 (ชื่อโครงการกรอกเอง) · อัปเดตความคืบหน้าหลังอนุมัติ (OQ-07) · แจ้งเตือนกำหนดส่งรายวัน · เปลี่ยนสถานะในระบบอื่น (DEC-01/02) · ทำซ้ำเป็นฟีเจอร์ทางการ (DEC-12)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ | Maker | owner |
| ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน) | Checker | role-line-manager |
| ผู้อนุมัติ / รับทราบ (รองกรรมการผู้จัดการ / กรรมการผู้จัดการ) | Approver | role-gm |
| admin ฝ่ายบริหารการลงทุน | Monitor · admin view | (ยังไม่มี role id — OQ-04) |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · F-ORG-001 (OrgUnit · อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type IVMB · status · print_config · revisions) · Organization (header/logo)
### Downstream
ENG-NOTIFY (ivmb_cancelled · ivmb_baseline_approved) · ENG-DOC-STORE (approved_final) · ทะเบียนโครงการ/FM-IVM-11 (ประกาศ event `ivmb.approved` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
ตาม CUBE Core (API REST · PostgreSQL RLS · PDF render server-side จาก template logic-less เดียวกับ prototype)

## §0.7 Open Questions
OQ-01 ตัวชี้วัด · OQ-02 ใบเซ็นยืนยัน DEC (AI-DEFAULT · รวมช่องเพิ่มชื่อโครงการ) · OQ-03 role/module ใน DOA master · OQ-04 admin role id · OQ-05 ทะเบียนโครงการ · OQ-06 รหัส IVMB/feature id/taxonomy · OQ-07 อัปเดตความคืบหน้าหลังอนุมัติ (รายละเอียด BRD §13)

## §0.8 Coverage Manifest
| FORM_SPEC | ที่ |
|---|---|
| F01 ชื่อโครงการ / ธุรกรรม (ช่องเพิ่ม) | 04 §4.2 project_name · 01 P-02 การ์ด ① |
| F02–F10 แผนฐานและหมุดหมายสำคัญ | 04 ivm_deal_tracker_milestone · 01 P-02 การ์ด ② |
| F11–F19 รายการติดตามงาน | 04 ivm_deal_tracker_task · 01 P-02 การ์ด ③ |
| formula F09 ความคลาดเคลื่อน | 03 FN-02 · 05 BR-01/02 |
| S1–S3 ลายเซ็น | 03 FN-09 sign_rows · 05 BR-12 |
| control FM-IVM-02 Rev.00 | print_config · DOCCFG |
| anomalies 6 | DEC-13..18 → 05 |
