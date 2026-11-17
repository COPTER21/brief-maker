# 00_OVERVIEW — F-TMP-001 แบบสำรวจความพึงพอใจลูกค้า สำหรับลูกค้า General Trade (Customer Satisfaction Survey — GT)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-001 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2 · โหมดไม่เฝ้า) |
| Variant | **STANDARD** (pages=3, states=3, approval=N, money=N) |
| Source | BRD-SAL-CSG-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-001_v2 · FORM_SPEC FM-SAL-10 · DECISIONS.lock (13 DEC · AI-DEFAULT) · feature.html (html-generator-v9.4 · Q-form · audit FAIL 0) |
| Module / Area | Sales · Core Cube (ช่องทาง General Trade) |
| Status | Ready for Dev (หลัง OQ-02/04/06 ปิด) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (unattended) |

## §0.3 Scope
### In Scope
รายการ (segmented tabs สถานะ · ค้นหา · กรองเดือน/ผู้บันทึก · CSV) · สร้าง/แก้ร่าง wizard 3 ขั้น · ดู 4 แท็บ · ให้คะแนน 16 ข้อ (5–1) · ข้อเสนอแนะ 2 ส่วน · บันทึกผล (ไม่มีขั้นพิจารณา) · ยกเลิก · แนบไฟล์ · PDF FM-SAL-10 Replica · เลขที่ CSG
### Out of Scope
FM-SAL-11 แบบสรุปหัวข้อการประเมิน (J002) · ลูกค้ากรอกเองผ่านลิงก์ · ส่งต่อระบบอื่น (DEC-02) · ทำซ้ำ (DEC-10) · สายพิจารณา/DOA (DEC-03)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| พนักงานขาย GT (ผู้บันทึก) | Maker | owner |
| ผู้จัดการฝ่ายขาย | Reviewer (รับแจ้ง) · admin view · ยกเลิกได้ | role-mgr-sales |

## §0.5 Dependencies
### Upstream
Customer master (Sales · `customerId` — อ่านชื่อ/รหัส/เบอร์ · flag ช่องทาง GT) · Employee (HR · ผู้บันทึก) · F-DOCCFG/F003 (doc_type CSG · status · print_config) · Organization (header_snapshot: ชื่อบริษัท · โลโก้) · Document Center (ไฟล์แนบ)
### Downstream
ENG-NOTIFY (csg_low_score_recorded · csg_cancelled) · FM-SAL-11 แบบสรุปหัวข้อการประเมิน (อ่านผ่าน API-01 — **ไม่ wire รอบนี้** DEC-02) · Report area

## §0.6 Open Questions
OQ-01 ตัวชี้วัด · OQ-02 ใบเซ็นยืนยัน DEC-01..10 (AI-DEFAULT) · OQ-03 เกณฑ์คะแนนต่ำ ≤ 2 · OQ-04 flag GT ใน Customer master · OQ-05 กันตอบซ้ำต่อเดือน · OQ-06 รหัส CSG / function_code / รหัส feature จริง · OQ-07 รูปแบบ Q-form "DOA 0 ขั้น" (ดู BRD §13)

## §0.7 Coverage Manifest
| FORM_SPEC | FRD |
|---|---|
| F01 ประจำเดือน | 04 `period_month` · 01 P-02 |
| F02 วันที่ | 04 `survey_date` · 01 P-02 |
| F03 ชื่อบริษัท | 04 `customer_id` + `customer_name_snapshot` (system · Customer master) |
| F04 ฝ่าย/แผนก | 04 `contact_dept` |
| F05 เบอร์โทร.ติดต่อ | 04 `contact_phone` (PDPA) |
| F06–F21 หัวข้อการประเมิน 16 ข้อ (choices q1_1…q3_8) | 04 `customer_survey_gt_score.q_key` · 01 P-02 rate-row |
| F22 ข้อเสนอแนะด้านเจ้าหน้าที่ฯ | 04 `comment_staff` |
| F23 ข้อเสนอแนะอื่นๆ ฯ | 04 `comment_other` |
| control Doc.No.FM-SAL-10 Rev.00 | print_config (DOCCFG) |
ครบ 23/23 ช่อง ✓
