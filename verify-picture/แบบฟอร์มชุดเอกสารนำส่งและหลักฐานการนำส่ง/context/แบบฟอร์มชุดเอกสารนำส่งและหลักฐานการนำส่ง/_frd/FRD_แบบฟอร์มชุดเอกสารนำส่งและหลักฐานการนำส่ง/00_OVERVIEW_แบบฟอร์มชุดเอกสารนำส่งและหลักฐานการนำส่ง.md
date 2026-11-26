# 00_OVERVIEW — F-TMP-009 แบบฟอร์มชุดเอกสารนำส่งและหลักฐานการนำส่ง (Document Dispatch Package and Delivery Evidence Form · IVMG)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-009 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (pages=4, states=5, approval=Y, money=N) |
| Source | BRD-IVM-IVMG-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-009_v2 · FORM_SPEC FM-IVM-07 · DECISIONS.lock (21 DEC · AI-DEFAULT 12) · feature.html (html-generator-v9.4 · audit FAIL 0 · self_audit PASS · smoke 64/64 · NO-BROWSER) |
| Module / Area | ฝ่ายบริหารการลงทุน (Investment) · Core Cube (Operation) |
| Status | Ready for Dev (หลัง OQ-03/04/06/08 ปิด) |
| Date | 2026-10-11 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-11 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · ข้อมูลการนำส่ง 7 ช่อง (ผู้จัดทำ/ผู้ตรวจทาน/ผู้อนุมัติ ระบบใส่) · รายการตรวจสอบชุดเอกสาร 6 คอลัมน์ (ลำดับระบบรัน) · ขาดเอกสาร/มีข้อจำกัด ต้องมีหมายเหตุ · DOA 2 ขั้น · ส่งกลับ→กลับร่าง · ยกเลิก · หลังอนุมัติ: บันทึกหลักฐานการนำส่งเอกสาร 10 คอลัมน์ + ปิดการนำส่ง · แนบไฟล์ (ใบ + หลักฐานต่อแถว) · PDF FM-IVM-07 Replica 2 หน้า · เลข IVMG · CSV
### Out of Scope
ส่งเอกสารออกจากระบบเอง (DEC-01) · ทะเบียนโครงการ / FM-IVM-01 (OQ-05) · ดึงรายการจาก FM-IVM-04/06 (OQ-07) · เชื่อม FM-IVM-08 (OQ-08) · บังคับช่องทางตามระดับความลับ (OQ-09) · เปลี่ยนสถานะในระบบอื่น (DEC-01/02) · ช่องเพิ่มนอกกระดาษ (DEC-07) · ทำซ้ำ (DEC-12 ✗)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ (ผู้ประสานงานบริหารการลงทุน / ผู้รับผิดชอบที่ได้รับมอบหมาย) | Maker | owner |
| ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน) | Checker | role-line-manager |
| ผู้อนุมัติ / รับทราบ (รองกรรมการผู้จัดการ / กรรมการผู้จัดการ / ผู้มีอำนาจตามตารางอำนาจอนุมัติ) | Approver | role-gm |
| admin ฝ่ายบริหารการลงทุน | Monitor · admin view · บันทึกหลักฐานแทน | (ยังไม่มี role id — OQ-04) |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · F-ORG-001 (OrgUnit · อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type IVMG · status · print_config · revisions) · Organization (header/logo)
### Downstream
ENG-NOTIFY (ivmg_cancelled · ivmg_delivery_failed · ivmg_dispatch_closed) · ENG-DOC-STORE (approved_final) · ทะเบียนโครงการ / ห้องข้อมูล / FM-IVM-08 (ประกาศ event `ivmg.approved` · `ivmg.closed` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
ตาม CUBE Core (API REST · PostgreSQL RLS · PDF render server-side จาก template logic-less เดียวกับ prototype)

## §0.7 Open Questions
OQ-01 ตัวชี้วัด · OQ-02 ใบเซ็นยืนยัน DEC (AI-DEFAULT) · OQ-03 role/module ใน DOA master (ผู้จัดการฝ่ายบริหารการลงทุน · รอง กก.ผจก./กก.ผจก.) · OQ-04 admin role id · OQ-05 ทะเบียนโครงการ · OQ-06 รหัส IVMG/feature id/taxonomy · OQ-07 ดึงรายการจาก FM-IVM-04/06 · OQ-08 ความสัมพันธ์กับ FM-IVM-08 · OQ-09 ช่องทางตามระดับความลับ · OQ-10 ยกเลิกหลังอนุมัติ (รายละเอียด BRD §13)

## §0.8 Coverage Manifest
| FORM_SPEC | ที่ |
|---|---|
| F01–F04 ข้อมูลการนำส่ง (กรอก) | 04 ivm_dispatch · 01 P-02 การ์ด ① |
| F05–F07 ผู้จัดทำ / ผู้ตรวจทาน / ผู้อนุมัติ (ระบบ) | 04 ivm_dispatch (maker snapshot · approval_chain) · 03 FN-09 |
| F08–F13 รายการตรวจสอบชุดเอกสาร | 04 ivm_dispatch_doc · 01 P-02 การ์ด ② |
| F14–F23 หลักฐานการนำส่งเอกสาร | 04 ivm_dispatch_delivery · 01 P-04 |
| choices doc_status · confidentiality · channel · receipt_status | 05 BR-10 · 04 enum |
| S1–S3 ลายเซ็น | 03 FN-09 sign_rows · 05 BR-15 |
| control FM-IVM-07 Rev.00 | print_config · DOCCFG |
| anomalies 9 | DEC-13..21 → 05 |
