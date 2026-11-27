# 00_OVERVIEW — F-TMP-001 แบบฟอร์มเริ่มต้นธุรกรรม (Transaction Initiation Form)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-001 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (pages=3, states=4, approval=Y, money=N) |
| Source | BRD-TMP-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-001_v2 · FORM_SPEC FM-IVM-01 · DECISIONS.lock (14 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0 · self_audit PASS · smoke 29/29 · e2e ยังไม่รัน — NO-BROWSER) |
| Module / Area | บริหารการลงทุน (เสนอ module ใหม่ · OQ-04) · Core Cube |
| Status | Ready for Dev (หลัง OQ-03/04 ปิด) |
| Date | 2026-10-11 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-11 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · ข้อมูลธุรกรรม 8 ช่อง + ขอบเขตงาน 5 ช่อง · ผู้รับผิดชอบจากพนักงาน · DOA 2 ขั้นค่าเริ่ม (dynamic) · ส่งกลับ/ไม่อนุมัติ→กลับร่าง · ยกเลิก · ประวัติการแก้ไขอัตโนมัติ · แนบไฟล์ · PDF FM-IVM-01 Replica 2 หน้า · เลข IVMA · CSV
### Out of Scope
FM-IVM-02..11 · ทะเบียนธุรกรรมกลาง · ส่งต่อระบบอื่น (DEC-02) · ทำซ้ำเป็นชุด · ประกาศ

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ | Maker | owner |
| ผู้ตรวจสอบ | Checker | role-line-manager |
| ผู้อนุมัติ / รับทราบ | Approver | role-gm |
| admin ฝ่ายบริหารการลงทุน | view all · ยกเลิกได้ | admin_role (ยังไม่มีใน DOA contract — OQ-03) |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน/เลือกผู้รับผิดชอบ) · F-ORG-001 (OrgUnit · ผัง) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type IVMA · status · print_config) · Company Master (header/logo)
### Downstream
ENG-NOTIFY (ivma_cancelled · ivma_responsible_assigned) · ENG-DOC-STORE (approved_final) · FM-IVM-02..11 (ประกาศ event `ivma.approved` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/ivm-init` (feature.html เป็น source of truth) · BE: REST `/api/v1/transaction-initiations` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less) + data contract (03 FN-08)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: ข้อมูลธุรกรรม/ขอบเขต · Confidential(PII): ชื่อผู้จัดทำ/ผู้รับผิดชอบ snapshot · บุคคลภายนอกที่เกี่ยวข้อง

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT | Strike | ก่อน UAT |
| OQ-03 | role ผู้ตรวจสอบ/ผู้อนุมัติ + admin_role ไม่มีตรงใน DOA roles master | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | module บริหารการลงทุน + feature id จริง (ใช้ F-TMP-001 / finance ชั่วคราว) | พี่เบิร์ด | ก่อน dev |
| OQ-05 | ประเภทธุรกรรม/แหล่งที่มา เป็น master ไหม | ลูกค้า | – |
| OQ-06 | รหัส IVMA ชนไหม · taxonomy function_code | Strike | ก่อน register |

## §0.9 Glossary
ธุรกรรม = โครงการลงทุน/ร่วมทุน/ซื้อกิจการ/จัดหาเงินทุน ที่ฝ่ายบริหารการลงทุนดูแล · ผู้รับผิดชอบ = ผู้ได้รับมอบหมายดำเนินธุรกรรม · ฉบับ = เวอร์ชันของแบบฟอร์มหลังแก้ไขตามที่ส่งกลับ

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED (DEC) · INDEX · declarations/

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม F01–F18 (FORM_SPEC) | txn.* 8 · scope.* 5 · revisions[] 5 | 01 §1.2 P-02 · 04 §4.2 · 03 FN-01/FN-08 |
| BRD S-01..S-10 | stories | 06 AC-01..AC-13 |
| BRD BR-01..10 · VR-01..06 · EC-01..09 | rules | 05 §5.1 / §5.4 / §5.5 |
| DEC-01..14 | มติ | 07 §7.0 |
| declaration | DOA · NTF · DOCCFG · MDOC | declarations/ · 03 FN-03/04/05/07/09 |
| หน้าจอ HTML | P-01 · P-02 · P-03 · M-01..05 | 01 §1.1 |
ไม่มี requirement หล่น
