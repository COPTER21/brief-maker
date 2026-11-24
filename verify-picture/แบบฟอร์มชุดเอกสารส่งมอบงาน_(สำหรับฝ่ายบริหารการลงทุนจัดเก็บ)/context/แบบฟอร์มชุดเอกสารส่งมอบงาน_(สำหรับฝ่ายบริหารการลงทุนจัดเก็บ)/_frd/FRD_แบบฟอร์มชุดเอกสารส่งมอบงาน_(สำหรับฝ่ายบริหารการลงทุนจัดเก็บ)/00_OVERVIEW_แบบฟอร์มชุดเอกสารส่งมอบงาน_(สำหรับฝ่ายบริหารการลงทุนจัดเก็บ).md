# 00_OVERVIEW — F-TMP-008 แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายบริหารการลงทุนจัดเก็บ) (Handover Package Record — Investment Management)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-008 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2 · โหมดไม่เฝ้า) |
| Variant | **FULL** (pages=3, states=4, approval=Y, repeat=Y ×1) |
| Source | BRD-TMP-008-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-008_v2 · FORM_SPEC FM-BDM-08 · DECISIONS.lock (17 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0 · e2e 21/21) |
| Module / Area | Business Development (ผู้ใช้หลัก ฝ่ายบริหารการลงทุน · ฝ่ายพัฒนาธุรกิจรับทราบ) |
| Status | Ready for Dev (หลัง OQ-03/04 ปิด · ลูกค้ายืนยัน AI-DEFAULT ก่อน UAT) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (unattended) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · ข้อมูลการรับมอบ 6 ช่อง · ผลการตรวจรับเอกสารไม่จำกัดแถว · ประเด็นค้างและข้อตกลงการติดตาม · DOA 2 ขั้น (ตรวจสอบ → ฝ่ายพัฒนาธุรกิจรับทราบ) · ไม่ผ่าน→กลับร่าง · ยกเลิก · แนบไฟล์ · PDF FM-BDM-08 Replica 2 หน้า · เลข HOI · CSV · แจ้งเตือนเอกสารค้างส่งหลังรับทราบ
### Out of Scope
ผูกคู่ FM-BDM-07 / โครงการ (OQ-05) · หน้าตั้งค่า HandoverConfig · ทำซ้ำ · ประกาศ · dashboard ติดตามข้ามใบ · ส่งต่อระบบอื่น (DEC-02)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ (ฝ่ายบริหารการลงทุน) | Maker | owner |
| ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน) | Checker | role-line-manager |
| ผู้อนุมัติ / รับทราบ (ฝ่ายพัฒนาธุรกิจรับทราบผลการรับมอบ) | Approver | role-mgr-bu (ชั่วคราว · OQ-03) |
| admin ฝ่ายบริหารการลงทุน | Monitor · เห็นทั้งหมด · ยกเลิกได้ | admin_role |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน · รายชื่อให้เลือก) · F-ORG-001 (OrgUnit · อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type HOI · status · print_config · form_revisions) · HandoverConfig (handover_results · received_options · completeness_options) · Company Master (logo/header)
### Downstream
ENG-NOTIFY (hoi_cancelled · hoi_acknowledged_open_items) · ENG-DOC-STORE (approved_final) · Report area (อ่าน · Phase 2)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/handover-investment` (อ้าง feature.html เป็น source of truth) · BE: REST `/api/v1/handover-records` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less · 2 หน้า) + data contract (03 FN-08)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: เอกสาร/ผลการตรวจรับ · Confidential(PII): ชื่อผู้จัดทำ/ผู้ส่งมอบ/ผู้รับมอบ/ผู้รับผิดชอบ/ผู้พิจารณา snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (11 ข้อ) | Strike | ก่อน UAT |
| OQ-03 | ไม่มี role ผู้จัดการฝ่ายพัฒนาธุรกิจ ใน DOA master (ใช้ role-mgr-bu ชั่วคราว) | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | HandoverConfig มีหรือยัง / ใช้ร่วมกับ FM-BDM-07 | พี่เบิร์ด | ก่อน dev |
| OQ-05 | ผูกกับ FM-BDM-07 / โครงการ ไหม | ลูกค้า | – |
| OQ-06 | กำหนดการติดตาม เป็นวันที่หรือข้อความ | ลูกค้า | – |
| OQ-07 | รหัส HOI ชนไหม (HOB สงวน FM-BDM-07) · taxonomy function_code | Strike | ก่อน register |

## §0.9 Glossary
สถานะเอกสาร (workflow) = ร่าง/รออนุมัติ/รับทราบแล้ว/ยกเลิก · ผลการรับมอบ (บนกระดาษ) = ผลที่ผู้จัดทำบันทึก · แถวไม่ผ่าน = ได้รับแล้ว ≠ ได้รับ หรือ ความครบถ้วน ≠ ครบถ้วน · ค้างส่ง = จำนวนแถวไม่ผ่าน

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED (DEC) · INDEX · declarations/

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม F01–F06 (ข้อมูลการรับมอบ) | project_name · sender · receiver · received_at · package_version · result | 01 §1.2 P-02 · 04 §4.2 · 03 FN-01/FN-08 |
| ช่องในฟอร์ม F07–F14 (ผลการตรวจรับเอกสาร) | seq · doc_name · doc_code_rev · received · completeness · issue · fix_owner · due_date | 01 §1.2 P-02 · 04 §4.2 · 03 FN-01/02/08 |
| ช่องในฟอร์ม F15–F18 (ประเด็นค้าง) | open_issues · pending_docs · followup_date · remark | 01 §1.2 · 04 §4.2 · 03 FN-01 |
| ค่าคงที่บนกระดาษ 3 ชุด | ผลการรับมอบ · ได้รับแล้ว · ความครบถ้วน | HandoverConfig · 05 BR-01 |
| ลายเซ็น S1–S3 | ผู้จัดทำ + DOA 2 ขั้น | 03 FN-04/05/08 · 05 BR-11 |
| BRD S-01..S-10 | stories | 06 AC-01..AC-14 |
| BRD BR-01..13 · VR-01..10 · EC-01..09 | rules | 05 §5.1 / §5.4 / §5.5 |
| DEC-01..17 | มติ | 07 §7.0 |
| declaration | DOA · NTF · DOCCFG · MDOC | declarations/ · 03 FN-03/05/07/09 |
| หน้าจอ HTML | P-01 · P-02 · P-03 · M-01..05 | 01 §1.1 |
ไม่มี requirement หล่น
