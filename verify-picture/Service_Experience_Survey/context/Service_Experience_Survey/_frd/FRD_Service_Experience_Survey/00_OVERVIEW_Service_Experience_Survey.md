# 00_OVERVIEW — F-TMP-006 Service Experience Survey (แบบประเมินความพึงพอใจ Sales Admin — ลูกค้าต่างประเทศ)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-006 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2 · โหมดไม่เฝ้า) |
| Variant | **STANDARD** (pages=3, states=3, approval=N, money=N) |
| Source | BRD-SAL-SEA-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-006_v2 · FORM_SPEC FM-SAL-22 · DECISIONS.lock (14 DEC · AI-DEFAULT 10) · feature.html (html-generator-v9.4 · Q-form · audit FAIL 0) |
| Module / Area | Sales · Core Cube (Sales Admin · ลูกค้าต่างประเทศ) |
| Status | Ready for Dev (หลัง OQ-02/04/07 ปิด) |
| Date | 2026-10-11 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-11 | สร้างจาก doc-master-pipeline ขั้น 7 (unattended) |

## §0.3 Scope
### In Scope
รายการ (segmented tabs สถานะ · ค้นหา · กรองเดือน/ผู้บันทึก · CSV) · สร้าง/แก้ร่าง wizard 3 ขั้น · ดู 4 แท็บ · คะแนน 1–5 จำนวน 10 ข้อ ใน 3 กลุ่ม (Communication & Responsiveness 3 · Documentation & Execution 5 · Professionalism 2) · Contact Person · Additional Feedback · บันทึกผล (ไม่มีขั้นพิจารณา) · ยกเลิก · แนบไฟล์ · PDF FM-SAL-22 Replica (ภาษาอังกฤษ) · เลขที่ SEA
### Out of Scope
ใบสรุปผลการประเมินต่างประเทศ (FM-SAL-23) · ใบในประเทศ FM-SAL-20/21 · ลูกค้ากรอกเองผ่านลิงก์ · ส่งต่อระบบอื่น (DEC-02) · ทำซ้ำ (DEC-10) · สายพิจารณา/DOA (DEC-03) · แบบพิมพ์สองภาษา (OQ-08)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| เจ้าหน้าที่ Sales Admin ต่างประเทศ (ผู้บันทึก) | Maker | owner |
| ผู้จัดการฝ่ายขาย | Reviewer (รับแจ้ง) · admin view · ยกเลิกได้ | role-mgr-sales |

## §0.5 Dependencies
### Upstream
Customer master (Sales · `customerId` — อ่านชื่อ/รหัส/ประเทศ · flag ต่างประเทศ) · Employee (HR · ผู้บันทึก) · F-DOCCFG/F003 (doc_type SEA · status · print_config) · Organization (header_snapshot: ชื่อบริษัทภาษาอังกฤษ · โลโก้) · Document Center (ไฟล์แนบ) · DOA กลาง (ไม่มี entry — TODO: DOA engine)
### Downstream
ENG-NOTIFY (sea_low_score_recorded · sea_cancelled) · ใบสรุปผลการประเมินต่างประเทศ FM-SAL-23 (อ่านผ่าน API-01 — **ไม่ wire รอบนี้** DEC-02) · Report area

## §0.6 Open Questions
OQ-01 ตัวชี้วัด · OQ-02 ใบเซ็นยืนยัน DEC-01..10 (AI-DEFAULT) · OQ-03 เกณฑ์คะแนนต่ำ ≤ 2 · OQ-04 flag ต่างประเทศใน Customer master · OQ-05 Contact Person เลือกจากรายชื่อผู้ติดต่อใน Customer master หรือพิมพ์เอง · OQ-06 กันตอบซ้ำต่อเดือน · OQ-07 รหัส SEA / function_code / รหัส feature จริง (ดู BRD §13) · OQ-08 ภาษาแบบพิมพ์ (อังกฤษล้วน / สองภาษา) และรูปแบบเลขปี (ค.ศ./พ.ศ.)

## §0.7 Coverage Manifest
| FORM_SPEC | FRD |
|---|---|
| F01 Month | 04 `period_month` · 01 P-02 |
| F02 Company Name | 04 `customer_id` + `customer_name_snapshot` (system · Customer master) |
| F03 Contact Person | 04 `contact_person` (PDPA · Confidential) · 01 P-02 |
| F04–F13 คะแนน 10 ข้อ 3 กลุ่ม (choices q1…q10 · 1–5) | 04 `sales_admin_eval_ovs_score.q_key` · 01 P-02 rate-row |
| F14 Additional Feedback | 04 `comment` |
| control Doc No.FM-SAL-22 Rev.00 | print_config (DOCCFG) |
ครบ 14/14 ช่อง ✓
