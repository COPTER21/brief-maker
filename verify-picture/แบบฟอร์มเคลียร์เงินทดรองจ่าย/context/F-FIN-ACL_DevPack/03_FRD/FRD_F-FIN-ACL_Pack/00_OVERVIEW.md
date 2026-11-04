# 00_OVERVIEW — F-FIN-ACL ใบเคลียร์เงินทดรองจ่าย (Advance Clearing)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-FIN-ACL v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (fallback from BRD: pages=3, states=4, approval=Y, money=Y) |
| Source | BRD-FIN-ACL-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-2569-0000_v2 · FORM_SPEC FM-FIN-02 · DECISIONS.lock (15 DEC) · feature.html (html-generator-v9.2 · audit FAIL 0 · e2e 21/21 · domain 13/13) |
| Module / Area | Finance · Core Cube (Operation) |
| Status | Ready for Dev (หลัง OQ-03/04 ปิด) |
| Date | 2026-10-06 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-06 | สร้างจาก doc-master-pipeline ขั้น 7 |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · คำนวณ รวม/เหลือคืน/TOTAL/ตัวอักษร · DOA 3 ขั้น · ไม่อนุมัติ→กลับร่าง · ยกเลิก · แนบไฟล์ · PDF FM-FIN-02 Replica · เลข ACL · CSV
### Out of Scope
FM-FIN-01 ใบเบิก · post AP/GL · จ่าย/รับเงินจริง · ทำซ้ำ · เตือนเลยกำหนด · กันเคลียร์ซ้ำต่อใบเบิก (DEC-02 · OQ-05)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้ขอเคลียร์ (พนักงาน) | Maker | owner |
| ผู้อนุมัติ/ตรวจสอบ | Checker | role-line-manager |
| ผู้รับเคลียร์เงิน | Checker/Custodian · admin view | role-finance-officer |
| ผู้จัดการฝ่ายการเงิน | Approver | role-finance-manager |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · F-ORG-001 (OrgUnit · อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type ACL · status · print_config) · ExpensePolicy (advance_clear_due_day) · Company Master (bank_accounts · logo/header)
### Downstream
ENG-NOTIFY (acl_cancelled · acl_overspent_approved · acl_refund_due) · ENG-DOC-STORE (approved_final) · AP/GL (ประกาศ event `acl.approved` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/advance-clearing` (อ้าง feature.html เป็น source of truth) · BE: REST `/api/v1/advance-clearings` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less) + data contract (03 FN-08)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: เอกสาร/ยอด · Confidential(PII): ชื่อผู้ขอ snapshot · Internal: บัญชีธนาคารบริษัท (อ่านจาก config)

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT | Strike | ก่อน UAT |
| OQ-03 | role id ตรง master DOA | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | ExpensePolicy.advance_clear_due_day · Company.bank_accounts มีหรือยัง | พี่เบิร์ด | ก่อน dev |
| OQ-05 | FM-FIN-01 + กันเคลียร์ซ้ำ | Strike | – |
| OQ-06 | รหัส ACL ชนไหม · taxonomy function_code | Strike | ก่อน register |

## §0.9 Glossary
เงินทดรองจ่าย = เงินที่บริษัทจ่ายล่วงหน้าให้พนักงานไปใช้ · เคลียร์ = แจ้งค่าใช้จ่ายจริงและคืนส่วนต่าง · เหลือส่งคืน (ติดลบ = ใช้เกิน)

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED (DEC) · INDEX · declarations/

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม F01–F14 (FORM_SPEC) | เลขที่ · วันที่ · ชื่อ · ตำแหน่ง · ฝ่าย · advance_ref · lines(seq/description/amount) · total_expense · advance_amount · refund_amount · total_amount · total_amount_text | 01 §1.2 P-02 · 04 §4.2 · 03 FN-02/FN-08 |
| BRD S-01..S-09 | stories | 06 AC-01..AC-12 |
| BRD BR-01..11 · VR-01..05 · EC-01..08 | rules | 05 §5.1 / §5.4 / §5.5 |
| DEC-01..15 | มติ | 07 §7.0 |
| declaration | DOA · NTF · DOCCFG · MDOC | declarations/ · 03 FN-03/05/06/07/09 |
| หน้าจอ HTML | P-01 · P-02 · P-03 · M-01..05 | 01 §1.1 |
ไม่มี requirement หล่น
