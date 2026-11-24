# 00_OVERVIEW — F-TMP-004 แบบฟอร์มแผนโครงการ (Project Plan)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-004 v1.0 · frd-generator-v6 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (pages=3, states=4, approval=Y, money=Y) |
| Source | BRD-PDM-PJP-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-004_v2 · FORM_SPEC FM-PDM-01 (37 ช่อง) · DECISIONS.lock (18 DEC · AI-DEFAULT 14) · feature.html (html-generator-v9.4 · audit FAIL 0 · self_audit PASS · e2e 21/21 + flow 17/17 บน Chromium ใน container) |
| Module / Area | ยังไม่มี module Project (OQ-04) · DOA module = budget · MDOC = เอกสารทั่วไป · Core Cube |
| Status | Ready for Dev (หลัง OQ-03/04/06 ปิด) |
| Date | 2026-10-11 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-11 | สร้างจาก doc-master-pipeline ขั้น 7 (unattended) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น · การ์ด ①–⑧) · ดู 4 แท็บ · ส่วนที่ 1–8 ครบ 37 ช่อง · ระยะเวลา/ยอดรวมคำนวณ · DOA dynamic (ค่าเริ่ม 2 ขั้น ผู้ตรวจสอบ → ผู้อนุมัติ) · งบที่ได้รับอนุมัติ (ผู้อนุมัติขั้นสุดท้าย) · ไม่อนุมัติ→กลับร่าง · ยกเลิก · อัปเดตสถานะกิจกรรมหลังอนุมัติ · แนบไฟล์ · PDF FM-PDM-01 Replica 2 หน้า · รหัสโครงการ PJP · CSV
### Out of Scope
ส่งงบเข้า Budget module / ใบขอใช้งบ (DEC-01/02) · รายงานความคืบหน้า (FM-PDM-02 แยก) · ทำซ้ำ · ประกาศ · Gantt

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ (Prepared by) | Maker | owner |
| ผู้ตรวจสอบ (Reviewed by) | Checker | role-line-manager (relative · ผังองค์กร) |
| ผู้อนุมัติ (Approved by) | Approver | role-gm |
| ผู้รับผิดชอบหลัก (Project Manager) | Operator (อัปเดตสถานะกิจกรรม) | project_manager_id |
| admin ฝ่ายพัฒนาโครงการ | Monitor | role ใหม่ — ยังไม่อยู่ใน DOA master (OQ-03) |

## §0.5 Dependencies
### Upstream
HR · Employee (ผู้จัดทำ/ผู้รับผิดชอบ · อ่าน) · Organization (Department · Company header/logo) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type PJP · status · print_config)
### Downstream
ENG-NOTIFY (pjp_cancelled · pjp_budget_adjusted · pjp_activity_delayed) · ENG-DOC-STORE (approved_final) · Budget (ประกาศ event `pjp.approved` — **ไม่ยิงรอบนี้** DEC-02) · รายงานความคืบหน้าโครงการ FM-PDM-02 (อ้างรหัส PJP)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/project-plan` (feature.html = source of truth) · BE: REST `/api/v1/project-plans` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less · 2 หน้า) + data contract (03 FN-08)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: เนื้อหาแผน/งบประมาณ · Confidential(PII): ชื่อผู้จัดทำ/ผู้รับผิดชอบ snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (14 ข้อ) | Strike | ก่อน UAT |
| OQ-03 | role admin ฝ่ายพัฒนาโครงการ ไม่อยู่ใน DOA master · role-line-manager เป็น relative role | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | ไม่มี module Project ใน FEATURE_REGISTRY · MDOC enum | พี่เบิร์ด | ก่อน register |
| OQ-05 | ข้อความยาวในส่วนที่ 2–3 กับแบบพิมพ์ 2 หน้า | ลูกค้า | – |
| OQ-06 | รหัส feature/REQ จริง · taxonomy function_code | Strike | ก่อน register |
| OQ-07 | ผู้รับผิดชอบหลัก (ไม่ใช่ผู้จัดทำ) ควรเห็นใบไหม | ลูกค้า | – |

## §0.9 Glossary
รหัสโครงการ = เลขที่เอกสาร PJP · งบที่ได้รับอนุมัติ = ยอดที่ผู้อนุมัติขั้นสุดท้ายกำหนดต่อรายการ · สถานะกิจกรรม = Not Started / In Progress / Completed / Delayed (ค่าตามต้นฉบับ)

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED (DEC) · INDEX · declarations/

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม F01–F40 (37 ช่อง · FORM_SPEC) | ส่วนที่ 1 (7) · 2 (3) · 3 (2) · 4 goals (4) · 5 actions (7) · 6 budget (4 + รวม 2) · 7 risks (5) · 8 (3) | 01 §1.2 · 04 §4.2 · 03 FN-01/FN-08 |
| ลายเซ็น S1–S3 | ผู้จัดทำ · ผู้ตรวจสอบ (DOA ขั้น 1) · ผู้อนุมัติ (DOA ขั้น 2) | 03 FN-04/05/08 · 04 approval_chain |
| สูตร 4 | duration_days ×2 · total_requested · total_approved | 03 FN-02 |
| BRD S-01..S-16 | stories | 06 AC-01..AC-18 |
| BRD BR-01..14 · VR-01..09 · EC-01..10 | rules | 05 §5.1 / §5.4 / §5.5 |
| DEC-01..18 | มติ | 07 §7.0 |
| declaration | DOA · NTF · DOCCFG · MDOC | declarations/ · 03 FN-03/04/05/06/09 |
| หน้าจอ HTML | P-01 · P-02 · P-03 · M-01..06 | 01 §1.1 |
ไม่มี requirement หล่น
