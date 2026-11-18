# 00_OVERVIEW — F-TMP-004 แบบประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าในประเทศ (Sale Admin Satisfaction — Domestic)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-004 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2 · โหมดไม่เฝ้า) |
| Variant | **STANDARD** (pages=3, states=3, approval=N, money=N) |
| Source | BRD-SAL-SDA-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-004_v2 · FORM_SPEC FM-SAL-20 · DECISIONS.lock (13 DEC · AI-DEFAULT) · feature.html (html-generator-v9.4 · Q-form · audit FAIL 0) |
| Module / Area | Sales · Core Cube (Sale admin · ลูกค้าในประเทศ) |
| Status | Ready for Dev (หลัง OQ-02/04/07 ปิด) |
| Date | 2026-10-11 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-11 | สร้างจาก doc-master-pipeline ขั้น 7 (unattended) |

## §0.3 Scope
### In Scope
รายการ (segmented tabs สถานะ · ค้นหา · กรองเดือน/ผู้บันทึก · CSV) · สร้าง/แก้ร่าง wizard 3 ขั้น · ดู 4 แท็บ · ระดับความพึงพอใจ 5 ข้อ (มากที่สุด…ควรปรับปรุง = 5–1) · ข้อเสนอแนะเพิ่มเติม · บันทึกผล (ไม่มีขั้นพิจารณา) · ยกเลิก · แนบไฟล์ · PDF FM-SAL-20 Replica · เลขที่ SDA
### Out of Scope
FM-SAL-21 สรุปผลการประเมินในประเทศ · FM-SAL-22/23 ต่างประเทศ · ลูกค้ากรอกเองผ่านลิงก์ · ส่งต่อระบบอื่น (DEC-02) · ทำซ้ำ (DEC-10) · สายพิจารณา/DOA (DEC-03)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| เจ้าหน้าที่ Sale admin (ผู้บันทึก) | Maker | owner |
| ผู้จัดการฝ่ายขาย | Reviewer (รับแจ้ง) · admin view · ยกเลิกได้ | role-mgr-sales |

## §0.5 Dependencies
### Upstream
Customer master (Sales · `customerId` — อ่านชื่อ/รหัส · flag ในประเทศ) · Employee (HR · ผู้บันทึก) · F-DOCCFG/F003 (doc_type SDA · status · print_config) · Organization (header_snapshot: ชื่อบริษัท · โลโก้) · Document Center (ไฟล์แนบ) · DOA กลาง (ไม่มี entry — TODO: DOA engine)
### Downstream
ENG-NOTIFY (sda_low_score_recorded · sda_cancelled) · FM-SAL-21 สรุปผลการประเมินในประเทศ (อ่านผ่าน API-01 — **ไม่ wire รอบนี้** DEC-02) · Report area

## §0.6 Open Questions
OQ-01 ตัวชี้วัด · OQ-02 ใบเซ็นยืนยัน DEC-01..10 (AI-DEFAULT) · OQ-03 เกณฑ์ระดับต่ำ ≤ 2 · OQ-04 flag ในประเทศใน Customer master · OQ-05 ตัวเลือก "ไม่เคยพบปัญหา" ข้อ 3–4 · OQ-06 กันตอบซ้ำต่อเดือน · OQ-07 รหัส SDA / function_code / รหัส feature จริง (ดู BRD §13)

## §0.7 Coverage Manifest
| FORM_SPEC | FRD |
|---|---|
| F01 ประจำเดือน | 04 `period_month` · 01 P-02 |
| F02 ชื่อลูกค้า | 04 `customer_id` + `customer_name_snapshot` (system · Customer master) |
| F03 วันที่ | 04 `survey_date` · 01 P-02 |
| F04–F08 รายละเอียด 5 ข้อ (choices q1…q5 · ระดับ มากที่สุด/มาก/ปานกลาง/น้อย/ควรปรับปรุง) | 04 `sale_admin_eval_dom_score.q_key` · 01 P-02 rate-row |
| F09 ข้อเสนอแนะเพิ่มเติม | 04 `comment` |
| control Doc No.FM-SAL-20 Rev.00 | print_config (DOCCFG) |
ครบ 9/9 ช่อง ✓
