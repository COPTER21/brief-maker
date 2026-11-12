# 04_DB — F-TMP-005

## §4.1 Table Overview
| Table | ใช้ |
|---|---|
| `pr_po_outstanding_review` | header (1 รายงาน) |
| `pr_po_outstanding_review_item` | รายการ PR/PO ค้าง (แถวซ้ำ) |
| `pr_po_outstanding_review_audit` | ประวัติ append-only |
| (Document Center) `attachment` | ไฟล์แนบ (ref_type='PPO') |

## §4.2 Per-Table
### pr_po_outstanding_review
| column | type | null | หมายเหตุ / ช่องบนกระดาษ | Class |
|---|---|---|---|---|
| id | uuid PK | N | | Internal |
| tenant_id | uuid | N | RLS | Internal |
| doc_no | varchar(30) unique/tenant | N | เลขที่ (ENG-DOC-NUM · footer) | Internal |
| status | enum(draft,pending,returned,approved,cancelled) | N | | Internal |
| report_date | date | N | วันที่รายงาน : | Internal |
| org_unit_id | uuid | N | หน่วยงาน : (soft-ref F-ORG-001) | Internal |
| org_unit_name_snapshot | varchar(200) | N | หน่วยงาน : | Internal |
| preparer_id | uuid | N | soft-ref F-EMP-001 | Internal |
| preparer_name_snapshot | varchar(200) | N | ผู้จัดทำรายงาน : / ลงชื่อ ผู้จัดทำ (PII) | Confidential·PII |
| position_snapshot · dept_snapshot | varchar(200) | Y | ตำแหน่ง : | Internal |
| header_snapshot | jsonb | Y | Organization (ชื่อบริษัท · โลโก้) ณ ออกเลข | Internal |
| items_count · no_po_count | int | N | สรุปต่อรายงาน (FN-04) | Internal |
| approval_required | bool | N | จาก DOA | Internal |
| doa_ref | varchar(50) | Y | doa_entry_ref | Internal |
| approval_chain | jsonb | Y | snapshot ตอนส่ง [{step, role_id, label, words, assignee, status, at, note}] | Internal |
| approver_role / approved_by / approved_at | varchar / uuid / timestamptz | Y | ลงชื่อ ผู้มีอำนาจอนุมัติ | Internal |
| submitted_at | timestamptz | Y | ลงชื่อ ผู้จัดทำ (ส่งในระบบ) | Internal |
| returned_by / returned_at / returned_reason | uuid / timestamptz / text | Y | DEC-08 | Internal |
| cancel_reason | text | Y | | Internal |
| version | int | N | optimistic lock | Internal |
| created_by/at · updated_by/at | | N | | Internal |
### pr_po_outstanding_review_item
| column | type | หมายเหตุ (ช่องบนกระดาษ) |
|---|---|---|
| id · review_id FK | | |
| seq | smallint N | ลำดับ |
| pr_no | varchar(50) Y | เลขที่ PR (soft ref · F072 ยังไม่มี) |
| po_no | varchar(50) Y | เลขที่ PO (soft ref · F078 ยังไม่มี) |
| order_date | date Y | วันที่สั่งซื้อ (บังคับเมื่อมี po_no) |
| receive_date | date Y | วันที่รับ สินค้า/บริการ (≥ order_date) |
| vendor_name | varchar(200) Y | ผู้ผลิต ผู้จัดจำหน่าย (บังคับเมื่อมี po_no) |
| description | text N | รายละเอียด |
| order_qty | numeric(18,3) N | จำนวนสั่งซื้อ (> 0) |
| uom_code · uom_name_snapshot | varchar N | หน่วย (uom_master) |
| request_org_unit_id · request_org_unit_name_snapshot | uuid · varchar N | ฝ่าย/แผนก ขอซื้อสินค้า/บริการ |
| outstanding_reason | text N | สาเหตุคงค้าง |
| current_status | text N | สถานะปัจจุบัน |
| corrective_action | text N | แนวทางการแก้ไข |
| check (pr_no is not null or po_no is not null) | | DEC-14 |
| check (receive_date is null or order_date is null or receive_date >= order_date) | | DEC-13 |
### pr_po_outstanding_review_audit
id · review_id · action · actor_id · note · at (append-only · ไม่มี update/delete)

## §4.3 ER
pr_po_outstanding_review 1—N pr_po_outstanding_review_item · 1—N pr_po_outstanding_review_audit · 1—N attachment(ref) · item N—1 uom_master (soft) · item N—1 OrgUnit (soft)

## §4.5 Field Dictionary (FE)
`report_date` · `org_unit` · `preparer.name` · `preparer.position` · `items[].seq` · `items[].pr_no` · `items[].po_no` · `items[].order_date` · `items[].receive_date` · `items[].vendor_name` · `items[].description` · `items[].order_qty` · `items[].uom` · `items[].request_dept` · `items[].outstanding_reason` · `items[].current_status` · `items[].corrective_action`

## §4.6 Data Classification
Default Internal · PII overlay: preparer_name_snapshot · ข้อมูลตัวอย่าง prototype = ชื่อสมมติ · เลข PR-TEST/PO-TEST · ผู้ขายสมมติ

## §4.7 Retention
ตามนโยบายเอกสารจัดซื้อ (ยืนยันกับ Policy Center) · ไม่ hard delete
