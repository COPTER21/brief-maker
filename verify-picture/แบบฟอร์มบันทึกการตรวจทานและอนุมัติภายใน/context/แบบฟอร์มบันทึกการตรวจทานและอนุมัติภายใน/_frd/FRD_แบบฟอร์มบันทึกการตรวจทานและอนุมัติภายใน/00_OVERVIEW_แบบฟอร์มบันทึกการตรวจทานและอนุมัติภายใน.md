# 00_OVERVIEW — F-TMP-006 แบบฟอร์มบันทึกการตรวจทานและอนุมัติภายใน (Internal Review & Approval Record)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-006 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2 · โหมดไม่เฝ้า) |
| Variant | **FULL** (pages=3, states=4, approval=Y, repeat=Y ×2) |
| Source | BRD-TMP-006-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-006_v2 · FORM_SPEC FM-BDM-06 · DECISIONS.lock (18 DEC · AI-DEFAULT 12) · feature.html (html-generator-v9.4 · audit FAIL 0 · e2e 21/21) |
| Module / Area | Business Development (ฝ่ายพัฒนาธุรกิจ) |
| Status | Ready for Dev (หลัง OQ-03/04 ปิด · ลูกค้ายืนยัน AI-DEFAULT ก่อน UAT) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (unattended) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · บันทึกการตรวจทานไม่จำกัดแถว · บันทึกการอนุมัติภายใน (เติมจาก DOA + เพิ่มนอกระบบ) · สถานะสุดท้าย (สถานะการอนุมัติ · วันที่มีผล · หมายเหตุ) · DOA 2 ขั้น · ไม่ผ่าน→กลับร่าง · ยกเลิก · แนบไฟล์ · PDF FM-BDM-06 Replica 2 หน้า · เลข IRV · CSV · แจ้งเตือนข้อแก้ไขค้างหลังอนุมัติ
### Out of Scope
ผูกโครงการ/FM-BDM-05 (OQ-05) · หน้าตั้งค่า ReviewApprovalConfig · ทำซ้ำ · ประกาศ · dashboard ติดตามข้ามใบ · ส่งต่อระบบอื่น (DEC-02)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ | Maker | owner |
| ผู้ตรวจสอบ (ผู้จัดการฝ่ายพัฒนาธุรกิจ / รองกรรมการผู้จัดการ) | Checker | role-line-manager |
| ผู้อนุมัติ / รับทราบ (กรรมการผู้จัดการ / ผู้มีอำนาจตามตารางอำนาจอนุมัติ) | Approver | role-gm (ชั่วคราว · OQ-03) |
| admin ฝ่ายพัฒนาธุรกิจ | Monitor · เห็นทั้งหมด · ยกเลิกได้ | admin_role |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน · รายชื่อให้เลือก) · F-ORG-001 (OrgUnit · อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type IRV · status · print_config · form_revisions) · ReviewApprovalConfig (review_statuses · final_statuses · final_needs_effective) · Company Master (logo/header)
### Downstream
ENG-NOTIFY (irv_cancelled · irv_approved_open_items) · ENG-DOC-STORE (approved_final) · Report area (อ่าน · Phase 2)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/internal-review` (อ้าง feature.html เป็น source of truth) · BE: REST `/api/v1/internal-reviews` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less · 2 หน้า) + data contract (03 FN-08)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: เอกสาร/บันทึกการตรวจทาน · Confidential(PII): ชื่อผู้จัดทำ/ผู้ตรวจทาน/ผู้พิจารณา snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (12 ข้อ) | Strike | ก่อน UAT |
| OQ-03 | role กรรมการผู้จัดการ/ผู้มีอำนาจตามตารางอำนาจอนุมัติ ไม่มีใน DOA master (ใช้ role-gm ชั่วคราว) · ผู้ตรวจสอบ "รองกรรมการผู้จัดการ" ขั้นเดียวกับผู้จัดการฝ่ายหรือแยก | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | ReviewApprovalConfig มีหรือยัง / เจ้าของ | พี่เบิร์ด | ก่อน dev |
| OQ-05 | ผูกกับโครงการ / FM-BDM-05 ไหม | ลูกค้า | – |
| OQ-06 | ผลการตรวจทาน ข้อความอิสระหรือรายการตัวเลือก | ลูกค้า | – |
| OQ-07 | รหัส IRV ชนไหม · taxonomy function_code | Strike | ก่อน register |

## §0.9 Glossary
สถานะเอกสาร (workflow) = ร่าง/รออนุมัติ/อนุมัติแล้ว/ยกเลิก · สถานะการอนุมัติ (บนกระดาษ) = ผลสุดท้ายที่ผู้จัดทำบันทึก · ข้อแก้ไขค้าง = แถวตรวจทานสถานะ เปิด/กำลังดำเนินการ

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED (DEC) · INDEX · declarations/

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม F01–F08 (บันทึกการตรวจทาน) | seq · item · reviewer · review_date · result · comment · fix_owner · status | 01 §1.2 P-02 · 04 §4.2 · 03 FN-01/FN-08 |
| ช่องในฟอร์ม F09–F14 (บันทึกการอนุมัติภายใน) | seq · approver_name · position · decision · decided_date · evidence | 01 §1.2 P-02 · 04 §4.2 · 03 FN-05/06/08 |
| ช่องในฟอร์ม F15–F17 (สถานะสุดท้าย) | approval_status · effective_date · remark | 01 §1.2 · 04 §4.2 · 03 FN-01/02 |
| ค่าคงที่บนกระดาษ 2 ชุด | สถานะข้อแก้ไข · สถานะการอนุมัติ | ReviewApprovalConfig · 05 BR-01 |
| ลายเซ็น S1–S3 | ผู้จัดทำ + DOA 2 ขั้น | 03 FN-04/05/08 · 05 BR-11 |
| BRD S-01..S-10 | stories | 06 AC-01..AC-14 |
| BRD BR-01..13 · VR-01..06 · EC-01..09 | rules | 05 §5.1 / §5.4 / §5.5 |
| DEC-01..18 | มติ | 07 §7.0 |
| declaration | DOA · NTF · DOCCFG · MDOC | declarations/ · 03 FN-03/05/07/09 |
| หน้าจอ HTML | P-01 · P-02 · P-03 · M-01..05 | 01 §1.1 |
ไม่มี requirement หล่น
