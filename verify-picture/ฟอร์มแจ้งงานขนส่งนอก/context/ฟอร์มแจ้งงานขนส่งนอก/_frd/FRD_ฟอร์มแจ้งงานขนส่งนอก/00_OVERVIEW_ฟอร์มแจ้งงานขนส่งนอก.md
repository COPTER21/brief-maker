# 00_OVERVIEW — F-TMP-003 ฟอร์มแจ้งงานขนส่งนอก (Outsourced Transport Job Notice)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-003 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2 · โหมดไม่เฝ้า) |
| Variant | **STANDARD** (pages=3, states=3, approval=N, money=N) |
| Source | BRD-SAL-OTN-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-003_v2 · FORM_SPEC FM-SAL-16 · DECISIONS.lock (15 DEC · AI-DEFAULT) · feature.html (html-generator-v9.4 · Q-form · audit FAIL 0) |
| Module / Area | Sales · Core Cube (Sales Admin) |
| Status | Ready for Dev (หลัง OQ-02/04/07 ปิด) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (unattended) |

## §0.3 Scope
### In Scope
รายการ (segmented tabs สถานะ · ค้นหาเลขที่/ผู้ขนส่ง/เลขที่PO/ปลายทาง · กรองผู้ขนส่ง/ผู้จัดทำ · CSV) · สร้าง/แก้ร่าง wizard 3 ขั้น · ดู 4 แท็บ · ตารางรายการงานขนส่งไม่จำกัดแถว · ส่งแจ้งงาน (ไม่มีขั้นพิจารณา) · ยกเลิก · แนบไฟล์ · PDF FM-SAL-16 Replica · เลขที่ OTN
### Out of Scope
ดึงรายการจาก SO/ใบส่งของ · ส่งใบแจ้งงานถึงผู้ขนส่งในระบบ/อีเมล · ผู้ขนส่งตอบรับงาน · ค่าขนส่ง · ส่งต่อระบบอื่น (DEC-02) · ทำซ้ำ (DEC-10) · สายพิจารณา/DOA (DEC-03 — โครง approver_role/approved_by/approval_chain เตรียมไว้ · TODO: DOA engine)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| Sales Admin (ผู้จัดทำ) | Maker | owner |
| ผู้จัดการฝ่ายขาย | Reviewer (รับแจ้ง) · admin view · ยกเลิกได้ | role-mgr-sales |

## §0.5 Dependencies
### Upstream
Vendor master (ผู้ขนส่ง ประเภทขนส่ง — อ่านชื่อ/รหัส) · Employee (HR · ผู้จัดทำ) · F-DOCCFG/F003 (doc_type OTN · status · print_config) · Organization (header_snapshot: ชื่อบริษัท · โลโก้) · Document Center (ไฟล์แนบ)
### Downstream
ENG-NOTIFY (otn_submitted · otn_early_delivery_date · otn_cancelled) · Sales Order/ใบส่งของ (อ้างเลขที่PO เป็นข้อความ — **ไม่ wire รอบนี้** DEC-02) · Report area

## §0.6 Open Questions
OQ-01 ตัวชี้วัด · OQ-02 ใบเซ็นยืนยัน DEC-01..10 (AI-DEFAULT) + ความหมายเส้นประต่อหัวฟอร์ม · OQ-03 เตือน/บล็อกวันที่นัดส่ง + แจ้งคลัง/ผู้ขนส่ง · OQ-04 Vendor ประเภทขนส่ง · OQ-05 เกิน 20 แถว/หน่วยจำนวน/คำ "รอบวันที" · OQ-06 ผูก PO กับ SO / กันซ้ำ · OQ-07 รหัส OTN / function_code / รหัส feature จริง / snapshot PDF (ดู BRD §13)

## §0.7 Coverage Manifest
| FORM_SPEC | FRD |
|---|---|
| F01 ฟอร์มแจ้งงานขนส่งนอก…… (`carrier_name`) | 04 `carrier_id` + `carrier_name_snapshot` (system · Vendor master) · 01 P-02 การ์ด ① |
| F02 รอบวันที (`round_date`) | 04 `round_date` · 01 P-02 การ์ด ① |
| F03 ต้นทาง (`lines[].origin`) | 04 `outsourced_transport_notice_line.origin` · 01 P-02 ตาราง |
| F04 ปลายทาง (`lines[].destination`) | 04 `destination` |
| F05 เลขที่PO (`lines[].po_no`) | 04 `po_no` |
| F06 จำนวน (`lines[].qty`) | 04 `qty` |
| F07 วันที่นัดส่ง (`lines[].delivery_date`) | 04 `delivery_date` |
| F08 ผู้จัดทำ (`prepared_by`) | 04 `prepared_by` + `submitted_at` (system · Employee · PDPA) |
| repeat lines (min_rows 20) | 04 line table · print_config.min_rows 20 |
| signature S1 ผู้จัดทำ | print sign_rows (requester) · 03 FN-07 |
| control Doc. No. : FM-SAL-16 Rev.00 : 01/07/2569 | print_config (DOCCFG) |
ครบ 8/8 ช่อง ✓
