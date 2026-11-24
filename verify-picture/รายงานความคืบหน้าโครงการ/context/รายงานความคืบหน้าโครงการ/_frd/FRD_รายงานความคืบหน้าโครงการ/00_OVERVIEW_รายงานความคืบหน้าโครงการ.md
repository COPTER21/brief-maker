# 00_OVERVIEW — F-TMP-005 รายงานความคืบหน้าโครงการ (Project Progress Report)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-005 v1.0 · frd-generator-v6 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (pages=3, states=4, approval=Y, money=Y) |
| Source | BRD-PDM-PPR-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-005_v2 · FORM_SPEC FM-PDM-02 (35 ช่อง) · DECISIONS.lock (20 DEC · AI-DEFAULT 15) · feature.html (html-generator-v9.4 · audit FAIL 0 · self_audit PASS · e2e 21/21 + flow 20/20) · print/form.tpl.html (thai-doc v2.2 Replica 2 หน้า) |
| Module / Area | ยังไม่มี module Project (OQ-04) · DOA module = budget · MDOC = เอกสารทั่วไป · Core Cube |
| Status | Ready for Dev (หลัง OQ-03/04/09 ปิด) |
| Date | 2026-10-11 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-11 | สร้างจาก doc-master-pipeline ขั้น 7 (unattended) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น · การ์ด ①–⑦) · ดู 4 แท็บ · ข้อมูลโครงการ (lookup PJP อนุมัติแล้ว) + ข้อ 1–6 ครบ 35 ช่อง · เติมค่าเริ่มจากแผนโครงการ · แจ้งผู้จัดการโครงการ · PM ส่ง → DOA dynamic (ค่าเริ่ม 2 ขั้น) · ไม่อนุมัติ→ร่าง · ยกเลิก · แนบไฟล์ · CSV · PDF FM-PDM-02 2 หน้า · เลข PPR
### Out of Scope
เขียนกลับแผนโครงการ / ส่งต่อระบบอื่น (DEC-01/02) · dashboard รวมทุกโครงการ · เตือนครบรอบ · ทำซ้ำ · ประกาศ

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำรายงาน (Prepared by) | Maker | owner (requester_id) |
| ผู้จัดการโครงการ (Project Manager) | Maker · Submitter | project_plan.project_manager_id (relative ต่อโครงการ — ไม่ใช่ role DOA) |
| ผู้ตรวจสอบ (Reviewed by) | Checker | role-line-manager (relative · ผังองค์กรของผู้ส่ง) |
| ผู้อนุมัติ (Approved by) | Approver | role-gm |
| admin ฝ่ายพัฒนาโครงการ | Monitor | role ใหม่ — ยังไม่อยู่ใน DOA master (OQ-03) |

## §0.5 Dependencies
### Upstream
F-TMP-004 แผนโครงการ (อ่าน PJP อนุมัติแล้ว: code · name · project_manager · start/end · total_approved · actions · goals.kpi) · HR · Employee · Organization (Company header/logo) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type PPR · status · print_config)
### Downstream
ENG-NOTIFY (ppr_cancelled · ppr_draft_for_pm · ppr_urgent_decision) · ENG-DOC-STORE (approved_final) · F-TMP-004 (ประกาศ event `ppr.approved` — **ไม่ยิงรอบนี้** DEC-02)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/project-progress` (feature.html = source of truth) · BE: REST `/api/v1/progress-reports` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less · 2 หน้า) + data contract (03 FN-08)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: เนื้อหารายงาน/งบ · Confidential(PII): ชื่อผู้จัดทำ/PM/ผู้รับผิดชอบ snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (15 ข้อ) | Strike | ก่อน UAT |
| OQ-03 | role admin ฝ่ายพัฒนาโครงการ ไม่อยู่ใน DOA master · role-line-manager เป็น relative role | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | ไม่มี module Project ใน FEATURE_REGISTRY · MDOC enum | พี่เบิร์ด | ก่อน register |
| OQ-05 | ถ้อยคำคำอธิบาย ☐ ล่าช้า หรือมีปัญหา ซ้ำประโยค ☐ มีความเสี่ยง | ลูกค้า | – |
| OQ-06 | รายงานของโครงการที่แผนถูกยกเลิก/ปิด | ลูกค้า | – |
| OQ-07 | ข้อความยาวกับแบบพิมพ์ 2 หน้า | ลูกค้า | – |
| OQ-08 | เขียนสถานะกิจกรรมกลับ PJP (Phase 2) | ลูกค้า | – |
| OQ-09 | รหัส feature/REQ จริง · taxonomy function_code | Strike | ก่อน register |

## §0.9 Glossary
PJP = แผนโครงการ (FM-PDM-01 · F-TMP-004) · PPR = รายงานความคืบหน้าโครงการ (FM-PDM-02) · PM = ผู้จัดการโครงการ · รอบการรายงาน = period_from–period_to

## §0.10 Coverage Manifest
| FORM_SPEC | ที่อยู่ |
|---|---|
| F01–F05 ข้อมูลโครงการ + รอบ + วันที่ | 01 P-02 ① · 04 progress_report |
| F06–F07 ☐ สถานะ + คำอธิบาย | 01 P-02 ② · 04 overall_status · status_note |
| F08–F13 ผลการดำเนินงาน | 01 ③ · 04 progress_report_performance |
| F14–F19 ระยะเวลา/งบ แผน-ผล-สถานะ | 01 ④ · 04 schedule_* · budget_* |
| F20–F23 KPI | 01 ④ · 04 progress_report_kpi |
| F24–F28 ปัญหา/ความเสี่ยง | 01 ⑤ · 04 progress_report_issue |
| F29–F31 แผนรอบถัดไป | 01 ⑥ · 04 progress_report_next |
| F32–F35 ประเด็นตัดสินใจ | 01 ⑦ · 04 progress_report_decision |
| S1–S4 ลงชื่อ | 05 BR-12 · 03 FN-08 sign_rows |
