# 00_OVERVIEW — F-TMP-007 แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายพัฒนาธุรกิจจัดเก็บ) (Handover Package · BD copy)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-007 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2 · โหมดไม่เฝ้า) |
| Variant | **FULL** (pages=3, states=4, approval=Y, repeat=Y ×1) |
| Source | BRD-TMP-007-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-007_v2 · FORM_SPEC FM-BDM-07 · DECISIONS.lock (16 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0 · e2e 21/21 verify) |
| Module / Area | Business Development (ฝ่ายพัฒนาธุรกิจ) |
| Status | Ready for Dev (หลัง OQ-03/04 ปิด · ลูกค้ายืนยัน AI-DEFAULT ก่อน UAT) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (unattended) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · ข้อมูลการส่งมอบ (ชื่อโครงการ · ผู้ส่งมอบ · ผู้รับมอบ · วันที่ส่งมอบ · ฉบับชุดเอกสาร · สถานะข้อมูล) · รายการเอกสารในชุดส่งมอบไม่จำกัดแถว · สมมติฐาน ประเด็นค้าง และข้อจำกัด · DOA 2 ขั้น (ขั้นรับทราบ = ผู้รับมอบ) · ไม่ผ่าน→กลับร่าง · ยกเลิก · แนบไฟล์ · PDF FM-BDM-07 Replica 2 หน้า · เลข HOB · CSV · แจ้งเตือนเอกสารขาดหลังรับมอบ
### Out of Scope
ดึงรายการเอกสารจากเอกสาร BDM อัตโนมัติ (OQ-05) · สร้างฉบับ FM-BDM-08 อัตโนมัติ (DEC-02) · หน้าตั้งค่า HandoverPackageConfig · ทำซ้ำ · ประกาศ

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ | Maker | owner |
| ผู้ตรวจสอบ (ผู้จัดการฝ่ายพัฒนาธุรกิจ) | Checker | role-line-manager |
| ผู้อนุมัติ / รับทราบ (ฝ่ายบริหารการลงทุนเป็นผู้รับมอบ) | Approver | role-mgr-bu (ชั่วคราว · OQ-03) |
| admin ฝ่ายพัฒนาธุรกิจ | Monitor · เห็นทั้งหมด · ยกเลิกได้ | admin_role |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน · รายชื่อให้เลือก ผู้ส่งมอบ/ผู้รับมอบ/ผู้รับผิดชอบ) · F-ORG-001 (OrgUnit · อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type HOB · status · print_config · form_revisions) · HandoverPackageConfig (data_statuses · doc_statuses · complete_data · limited_data · gap_doc) · Company Master (logo/header)
### Downstream
ENG-NOTIFY (hob_cancelled · hob_received_with_gaps) · ENG-DOC-STORE (approved_final) · Report area (อ่าน · Phase 2)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/handover-package-bd` (อ้าง feature.html เป็น source of truth) · BE: REST `/api/v1/handover-packages-bd` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less · 2 หน้า) + data contract (03 FN-08)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: ชุดเอกสาร/รายการเอกสาร · Confidential(PII): ชื่อผู้จัดทำ/ผู้ส่งมอบ/ผู้รับมอบ/ผู้รับผิดชอบ snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (11 ข้อ) | Strike | ก่อน UAT |
| OQ-03 | role ฝ่ายบริหารการลงทุน (ผู้รับมอบ) ไม่มีใน DOA master (ใช้ role-mgr-bu ชั่วคราว) | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | HandoverPackageConfig มีหรือยัง / เจ้าของ / ใช้ร่วม FM-BDM-08 | พี่เบิร์ด | ก่อน dev |
| OQ-05 | ดึงรายการเอกสารจากเอกสาร BDM ในระบบอัตโนมัติไหม | ลูกค้า | – |
| OQ-06 | FM-BDM-07 กับ FM-BDM-08 เป็นเอกสารเดียว 2 มุมมองหรือ 2 เอกสาร | ลูกค้า + Strike | – |
| OQ-07 | รหัส HOB ชนไหม · taxonomy function_code | Strike | ก่อน register |

## §0.9 Glossary
สถานะเอกสาร (workflow) = ร่าง/รออนุมัติ/อนุมัติแล้ว/ยกเลิก · สถานะข้อมูล (บนกระดาษ) = ความครบของชุดที่ผู้จัดทำประเมิน · เอกสารขาด/มีข้อจำกัด = แถวรายการสถานะ ∈ gap_doc

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED (DEC) · INDEX · declarations/

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม F01–F06 (ข้อมูลการส่งมอบ) | project_name · sender · receiver · handover_date · package_version · data_status | 01 §1.2 P-02 · 04 §4.2 · 03 FN-01/FN-08 |
| ช่องในฟอร์ม F07–F14 (รายการเอกสารในชุดส่งมอบ) | seq · doc_name · doc_ref · doc_date · owner · status · location · remark | 01 §1.2 P-02 · 04 §4.2 · 03 FN-01/02/08 |
| ช่องในฟอร์ม F15–F18 (สมมติฐาน ประเด็นค้าง และข้อจำกัด) | assumptions · open_issues · data_limits · bd_support | 01 §1.2 · 04 §4.2 · 03 FN-01 |
| ค่าคงที่บนกระดาษ 2 ชุด | สถานะข้อมูล · สถานะเอกสาร | HandoverPackageConfig · 05 BR-01 |
| ลายเซ็น S1–S3 | ผู้จัดทำ + DOA 2 ขั้น | 03 FN-04/05/08 · 05 BR-11 |
| BRD S-01..S-09 | stories | 06 AC-01..AC-13 |
| BRD BR-01..13 · VR-01..07 · EC-01..09 | rules | 05 §5.1 / §5.4 / §5.5 |
| DEC-01..16 | มติ | 07 §7.0 |
| declaration | DOA · NTF · DOCCFG · MDOC | declarations/ · 03 FN-03/05/07/09 |
| หน้าจอ HTML | P-01 · P-02 · P-03 · M-01..05 | 01 §1.1 |
ไม่มี requirement หล่น
