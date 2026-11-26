# 00_OVERVIEW — F-TMP-008 แบบฟอร์มชุดเอกสารส่งมอบงาน (Handover Document Package Form · IVMF)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-008 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (pages=3, states=4, approval=Y, money=N) |
| Source | BRD-IVM-IVMF-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-008_v2 · FORM_SPEC FM-IVM-06 · DECISIONS.lock (18 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0 · self_audit PASS · smoke 53/53 · NO-BROWSER) |
| Module / Area | ฝ่ายบริหารการลงทุน (Investment) · Core Cube (Operation) |
| Status | Ready for Dev (หลัง OQ-03/04/06 ปิด) |
| Date | 2026-10-11 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-11 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · ข้อมูลการรับมอบ 6 ช่อง · ผลการตรวจรับเอกสาร 8 คอลัมน์ (ลำดับระบบรัน) · ประเด็นค้างและข้อตกลงการติดตาม 4 ช่อง · ผูกได้รับแล้ว↔ความครบถ้วน · ผลการรับมอบสอดคล้องตาราง + คำแนะนำ (เตือน) · DOA 2 ขั้น · ส่งกลับ→กลับร่าง · ยกเลิก · แนบไฟล์ · PDF FM-IVM-06 Replica 2 หน้า · เลข IVMF · CSV
### Out of Scope
ทะเบียนโครงการ / FM-IVM-01 (ชื่อโครงการกรอกเอง · OQ-05) · ดึงรายการเอกสารจาก FM-IVM-05 / FM-IVM-04 (OQ-07) · ปิดรายการค้างส่งหลังอนุมัติ (OQ-08) · เปลี่ยนสถานะในระบบอื่น (DEC-01/02) · ช่องเพิ่มนอกกระดาษ (DEC-06) · ทำซ้ำ (DEC-11 ✗)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ (ฝ่ายบริหารการลงทุน) | Maker | owner |
| ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน) | Checker | role-line-manager |
| ผู้อนุมัติ / รับทราบ (ฝ่ายพัฒนาธุรกิจรับทราบผลการรับมอบ) | Approver (รับทราบ) | role-mgr-bu |
| admin ฝ่ายบริหารการลงทุน | Monitor · admin view | (ยังไม่มี role id — OQ-04) |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · F-ORG-001 (OrgUnit · อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type IVMF · status · print_config · revisions) · Organization (header/logo)
### Downstream
ENG-NOTIFY (ivmf_cancelled · ivmf_handover_followup) · ENG-DOC-STORE (approved_final) · ทะเบียนโครงการ / ห้องข้อมูล (ประกาศ event `ivmf.approved` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
ตาม CUBE Core (API REST · PostgreSQL RLS · PDF render server-side จาก template logic-less เดียวกับ prototype)

## §0.7 Open Questions
OQ-01 ตัวชี้วัด · OQ-02 ใบเซ็นยืนยัน DEC (AI-DEFAULT) · OQ-03 role/module ใน DOA master (ผู้จัดการฝ่ายบริหารการลงทุน · ฝ่ายพัฒนาธุรกิจรับทราบ) · OQ-04 admin role id · OQ-05 ทะเบียนโครงการ · OQ-06 รหัส IVMF/feature id/taxonomy · OQ-07 ดึงรายการเอกสารจาก FM-IVM-05 · OQ-08 ปิดรายการค้างส่งหลังอนุมัติ (รายละเอียด BRD §13)

## §0.8 Coverage Manifest
| FORM_SPEC | ที่ |
|---|---|
| F01–F06 ข้อมูลการรับมอบ | 04 ivm_handover · 01 P-02 การ์ด ① |
| F07–F14 ผลการตรวจรับเอกสาร | 04 ivm_handover_item · 01 P-02 การ์ด ② |
| F15–F18 ประเด็นค้างและข้อตกลงการติดตาม | 04 ivm_handover · 01 P-02 การ์ด ③ |
| choices handover_result · received · completeness | 05 BR-08 · 04 enum |
| S1–S3 ลายเซ็น | 03 FN-09 sign_rows · 05 BR-14 |
| control FM-IVM-06 Rev.00 | print_config · DOCCFG |
| anomalies 7 | DEC-12..18 → 05 |
