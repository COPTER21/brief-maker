# 00_OVERVIEW — F-TMP-001 แบบฟอร์มบันทึกภาพรวมและเริ่มต้นโครงการ (Project Overview & Initiation)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-001 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (pages=3, states=4, approval=Y, money=N) |
| Source | BRD-BDM-PJI-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-001_v2 · FORM_SPEC FM-BDM-01 · DECISIONS.lock (15 DEC) · feature.html (html-generator-v9.4 · audit FAIL 0 · [NO-BROWSER] e2e ยังไม่รัน — jsdom smoke ผ่าน) |
| Module / Area | Business Development · Core Cube (module ใหม่ — OQ-05) |
| Status | Ready for Dev (หลัง OQ-03/04/05 ปิด) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ + segmented ทั้งหมด/รอฉันพิจารณา · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · แผนงานเบื้องต้น · DOA dynamic ค่าเริ่ม 2 ขั้น · ไม่อนุมัติ→กลับร่าง · ยกเลิก · แนบไฟล์ · ประวัติการแก้ไข · PDF FM-BDM-01 Replica 2 หน้า · เลข PJI · CSV
### Out of Scope
ติดตามความคืบหน้ากิจกรรมหลังอนุมัติ · เชื่อมงบประมาณ/บริหารโครงการ · ทำซ้ำ · ประกาศ (DEC-01/02/12)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ | Maker | owner |
| ผู้ตรวจสอบ | Checker | role-line-manager |
| ผู้อนุมัติ / รับทราบ | Approver | role-gm (OQ-03) |
| admin ฝ่ายพัฒนาธุรกิจ | Monitor · เห็นทั้งหมด | admin_role |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · F-ORG-001 (OrgUnit · ผู้บังคับบัญชา) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type PJI · status · print_config) · Organization (header/logo)
### Downstream
ENG-NOTIFY (pji_cancelled · pji_owner_assigned) · ENG-DOC-STORE (approved_final) · Report area (อ่าน) — ไม่ส่งต่อระบบอื่น (DEC-02)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/project-initiation` (feature.html = source of truth) · BE: REST `/api/v1/project-initiations` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less) + data contract (03 FN-08)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: เนื้อหาโครงการ/แผนงาน · Confidential(PII): ชื่อผู้จัดทำ/ผู้รับผิดชอบ snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT 12 ข้อ | Strike | ก่อน UAT |
| OQ-03 | role ผู้ตรวจสอบ (ผู้จัดการฝ่ายพัฒนาธุรกิจ) · ผู้อนุมัติ/รับทราบ (รองกรรมการผู้จัดการ/กรรมการผู้จัดการ) ไม่มีใน DOA master | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | ตัวเลือกระดับความสำคัญ (สูง/กลาง/ต่ำ = AI-DEFAULT) | ลูกค้า | ก่อน dev |
| OQ-05 | module Business Development · รหัส feature จริง · taxonomy function_code (MDOC ใช้ F01 ชั่วคราว) | Strike | ก่อน register |

## §0.9 Glossary
หมุดหมาย = milestone ของแผนงาน · ผู้สนับสนุน = บุคคล/หน่วยงานที่ช่วย (ข้อความอิสระ) · ฉบับ = เวอร์ชันเอกสารที่อนุมัติแล้ว
