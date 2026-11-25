# 00_OVERVIEW — F-TMP-007 แบบฟอร์มรายการคำขอเอกสารและข้อมูล (Document and Information Request List · IVME)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-007 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (pages=3, states=4, approval=Y, money=N) |
| Source | BRD-IVM-IVME-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-007_v2 · FORM_SPEC FM-IVM-05 · DECISIONS.lock (18 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0 · self_audit PASS · jsdom 42/42 · NO-BROWSER) |
| Module / Area | ฝ่ายบริหารการลงทุน (Investment) · Core Cube (Operation) |
| Status | Ready for Dev (หลัง OQ-03/04/06/08 ปิด) |
| Date | 2026-10-11 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-11 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · ชื่อโครงการ / ธุรกรรม · รายการคำขอเอกสารและข้อมูล 10 คอลัมน์ (ไม่จำกัดแถว · ใบใหม่ตั้งต้น 1 แถว) · รหัสคำขอระบบรัน (prefix จาก config) · กติกาสถานะ↔วันที่ · ลำดับวันที่ · เหตุผลการปิดแถว · ลิงก์ path/URL · ป้ายเกินกำหนด · สรุปรายการคำขอ · หมายเหตุการใช้งาน (อ่านจาก config) · DOA 2 ขั้น · ส่งกลับ→กลับร่าง · ยกเลิก · แนบไฟล์ · PDF FM-IVM-05 Replica 2 หน้า · เลข IVME · CSV
### Out of Scope
ส่งคำขอจริงถึงผู้ถูกขอข้อมูล (ติดตามนอกระบบ · DEC-01/02) · ตรวจไฟล์จริงในห้องข้อมูล · ทะเบียนโครงการ / FM-IVM-01 (ชื่อโครงการกรอกเอง) · อัปเดตสถานะการรับมอบหลังอนุมัติ (OQ-07) · ส่งต่อ FM-IVM-04/06 · ทำซ้ำ (DEC-11 ไม่มี)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ | Maker | owner |
| ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน) | Checker | role-line-manager |
| ผู้อนุมัติ / รับทราบ (รองกรรมการผู้จัดการ / กรรมการผู้จัดการ) | Approver | role-gm |
| admin ฝ่ายบริหารการลงทุน | Monitor · admin view | (ยังไม่มี role id — OQ-04) |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · F-ORG-001 (OrgUnit · อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type IVME · status · print_config · revisions) · Organization (header/logo) · config DocRequestPolicy (code_prefix · usage_note · เจ้าของ OQ-08) · master list ivme.request_status
### Downstream
ENG-NOTIFY (ivme_cancelled · ivme_request_list_approved) · ENG-DOC-STORE (approved_final) · FM-IVM-04/06 (ประกาศ event `ivme.approved` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
ตาม CUBE Core (API REST · PostgreSQL RLS · PDF render server-side จาก template logic-less เดียวกับ prototype)

## §0.7 Open Questions
OQ-01 ตัวชี้วัด · OQ-02 ใบเซ็นยืนยัน DEC (AI-DEFAULT · รวมช่องเพิ่มชื่อโครงการ) · OQ-03 role/module ใน DOA master · OQ-04 admin role id · OQ-05 ทะเบียนโครงการ · OQ-06 รหัส IVME/feature id/taxonomy · OQ-07 อัปเดตสถานะการรับมอบหลังอนุมัติ · OQ-08 เจ้าของ config DocRequestPolicy (รายละเอียด BRD §13)

## §0.8 Coverage Manifest
| FORM_SPEC | ที่ |
|---|---|
| F01 ชื่อโครงการ / ธุรกรรม (ช่องเพิ่ม) | 04 §4.2 project_name · 01 P-02 ขั้น 1 การ์ด ① |
| F02 รหัสคำขอ (auto) | 04 ivm_doc_request_item.request_code · 03 FN-02 · 05 BR-01 |
| F03–F11 รายการคำขอเอกสารและข้อมูล | 04 ivm_doc_request_item · 01 P-02 ขั้น 1 การ์ด ② |
| choices request_status (6) | 05 BR-10 · 04 enum |
| constants รูปแบบรหัสคำขอ · หมายเหตุการใช้งาน | 04 usage_note_snapshot · 03 FN-12 · 01 P-02 ขั้น 1 การ์ด ③ · 05 BR-01/02 |
| S1–S3 ลายเซ็น | 03 FN-09 sign_rows · 05 BR-16 |
| control FM-IVM-05 Rev.00 | print_config · DOCCFG |
| anomalies 7 | DEC-12..18 → 05 |
