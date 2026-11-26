# 00_OVERVIEW — F-TMP-010 แบบฟอร์มบันทึกการอนุมัตินำส่ง (Pre-submission Approval Record · IVMH)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-010 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (pages=3, states=4, approval=Y, money=N) |
| Source | BRD-IVM-IVMH-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-010_v2 · FORM_SPEC FM-IVM-08 · DECISIONS.lock (18 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0 · self_audit PASS · smoke 58/58 · NO-BROWSER) |
| Module / Area | ฝ่ายบริหารการลงทุน (Investment) · Core Cube (Operation) |
| Status | Ready for Dev (หลัง OQ-03/04/06/09 ปิด) |
| Date | 2026-10-11 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-11 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · รายละเอียดการขออนุมัติ 6 ช่อง · ระดับอำนาจอนุมัติ → สาย 2/3 ขั้น · ตารางผลการพิจารณา (ระบบเติมจากการกด) · ผลการพิจารณา 5 ค่า + กติกา · ให้แก้ไข/ไม่อนุมัติ→กลับร่าง · ยกเลิก · แนบไฟล์ · PDF FM-IVM-08 Replica 2 หน้า · เลข IVMH · CSV
### Out of Scope
ทะเบียนโครงการ / FM-IVM-01 (OQ-05) · ผูกชุดเอกสารนำส่ง FM-IVM-07 (OQ-07) · ติดตามเงื่อนไขหลังอนุมัติ (OQ-08) · เปลี่ยนสถานะในระบบอื่น (DEC-01/02) · ช่องเพิ่มนอกกระดาษ (DEC-06) · ทำซ้ำ (DEC-11 ✗)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ (ผู้ประสานงานบริหารการลงทุน) | Maker | owner |
| ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน) | Checker | role-line-manager |
| ผู้อนุมัติ / รับทราบ (รองกรรมการผู้จัดการ) | Approver | role-gm |
| ผู้อนุมัติ (กรรมการผู้จัดการ / ผู้มีอำนาจ) — เฉพาะระดับกรรมการผู้จัดการ | Approver | role-gm |
| admin ฝ่ายบริหารการลงทุน | Monitor · admin view | (ยังไม่มี role id — OQ-04) |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · F-ORG-001 (OrgUnit · อ่าน) · F-DLG-001 DOA (resolve ตามระดับอำนาจอนุมัติ) · F-DOCCFG/F003 (doc_type IVMH · status · print_config · revisions) · Organization (header/logo)
### Downstream
ENG-NOTIFY (ivmh_cancelled · ivmh_conditional_approved) · ENG-DOC-STORE (approved_final) · ชุดเอกสารนำส่ง / ทะเบียนโครงการ (ประกาศ event `ivmh.approved` — **ไม่ยิงรอบนี้** DEC-02)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
ตาม CUBE Core (API REST · PostgreSQL RLS · PDF render server-side จาก template logic-less เดียวกับ prototype)

## §0.7 Open Questions
OQ-01 ตัวชี้วัด · OQ-02 ใบเซ็นยืนยัน DEC (AI-DEFAULT) · OQ-03 role/module ใน DOA master · OQ-04 admin role id · OQ-05 ทะเบียนโครงการ · OQ-06 รหัส IVMH/feature id/taxonomy · OQ-07 ผูก FM-IVM-07 · OQ-08 ติดตามเงื่อนไขหลังอนุมัติ · OQ-09 DOA engine รองรับ 5 ผลการพิจารณา + resolve ตามระดับ · OQ-10 ไม่อนุมัติจบใบหรือกลับร่าง (รายละเอียด BRD §13)

## §0.8 Coverage Manifest
| FORM_SPEC | ที่ |
|---|---|
| F01–F06 รายละเอียดการขออนุมัติ | 04 ivm_submission_approval · 01 P-02 การ์ด ①②③ |
| F07–F13 ผลการพิจารณา | 04 approval_chain (jsonb) · 01 P-02 การ์ด ④ (อ่านอย่างเดียว) · P-03 · 03 FN-06/09 |
| choices authority_level · review_decision | 05 BR-01/06 · 04 enum |
| S1–S3 ลายเซ็น | 03 FN-09 sign_rows · 05 BR-13 |
| control FM-IVM-08 Rev.00 | print_config · DOCCFG |
| anomalies 7 | DEC-12..18 → 05 |
