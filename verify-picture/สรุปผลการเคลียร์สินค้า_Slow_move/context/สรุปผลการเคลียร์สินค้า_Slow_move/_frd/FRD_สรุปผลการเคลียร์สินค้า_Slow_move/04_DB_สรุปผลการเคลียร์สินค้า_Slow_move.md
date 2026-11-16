# 04_DB — F-TMP-003

## §4.1 Table Overview
| Table | ใช้ |
|---|---|
| `slow_move_clearance` | header (1 ใบ/เดือน) |
| `slow_move_clearance_item` | รายการสินค้า (แถวซ้ำ) |
| `slow_move_clearance_audit` | ประวัติ append-only |
| `slow_move_config_method` | แนวทางการเคลียร์ (config ของ feature · OQ-04) |
| (Document Center) `attachment` | ไฟล์แนบ (ref_type='SMC') |

## §4.2 Per-Table
### slow_move_clearance
| column | type | null | หมายเหตุ / ช่องบนกระดาษ | Class |
|---|---|---|---|---|
| id | uuid PK | N | | Internal |
| tenant_id | uuid | N | RLS | Internal |
| doc_no | varchar(30) unique/tenant | N | เลขที่ (ENG-DOC-NUM · footer) | Internal |
| status | enum(draft,pending,returned,approved,cancelled) | N | | Internal |
| clearance_month | char(7) 'YYYY-MM' | N | ประจำเดือน | Internal |
| preparer_id | uuid | N | soft-ref F-EMP-001 | Internal |
| preparer_name_snapshot | varchar(200) | N | ลงชื่อ ผู้จัดทำ (PII) | Confidential·PII |
| position_snapshot · dept_snapshot | varchar(200) | Y | | Internal |
| header_snapshot | jsonb | Y | Organization (ชื่อบริษัท · ที่อยู่ · โลโก้) ณ ออกเลข | Internal |
| items_count · cleared_count · expired_count | int | N | สรุปต่อใบ (FN-04) | Internal |
| approval_required | bool | N | จาก DOA | Internal |
| doa_ref | varchar(50) | Y | doa_entry_ref | Internal |
| approval_chain | jsonb | Y | snapshot ตอนส่ง [{step, role_id, label, words, assignee, status, at, note}] | Internal |
| approver_role / approved_by / approved_at | varchar / uuid / timestamptz | Y | ลงชื่อ ผู้อนุมัติ | Internal |
| returned_by / returned_at / returned_reason | uuid / timestamptz / text | Y | DEC-08 | Internal |
| cancel_reason | text | Y | | Internal |
| version | int | N | optimistic lock | Internal |
| created_by/at · updated_by/at | | N | | Internal |
### slow_move_clearance_item
| column | type | หมายเหตุ (ช่องบนกระดาษ) |
|---|---|---|
| id · clearance_id FK | | |
| seq | smallint N | ลำดับ |
| product_code | varchar(50) N | รหัสสินค้า (soft-ref T_product.product_code) |
| product_name_snapshot · uom_snapshot | varchar | รายละเอียด (snapshot) |
| follow_up_date | date N | วันที่ติดตาม |
| clearance_method_code · clearance_method_label · clearance_method_note | varchar · varchar · text | แนวทางการเคลียร์ |
| cleared_date | date Y | วันที่ (ผลการเคลียร์) |
| cleared_qty | numeric(18,3) Y | จำนวน (> 0 · คู่กับ cleared_date) |
| expiry_date | date Y | วันหมดอายุ |
| remark | text Y | หมายเหตุ |
| check (cleared_date is null) = (cleared_qty is null) | | DEC-13 |
### slow_move_clearance_audit
id · clearance_id · action · actor_id · note · at (append-only · ไม่มี update/delete)
### slow_move_config_method
id · tenant_id · code · label · need_note · seq · active · effective_from (ค่าเริ่มเสนอ 6 แนวทาง — รอลูกค้ายืนยัน)

## §4.3 ER
slow_move_clearance 1—N slow_move_clearance_item · 1—N slow_move_clearance_audit · 1—N attachment(ref) · item N—1 T_product (soft)

## §4.5 Field Dictionary (FE)
`clearance_month` · `items[].seq` · `items[].product_code` · `items[].product_name` · `items[].follow_up_date` · `items[].clearance_method` · `items[].cleared_date` · `items[].cleared_qty` · `items[].expiry_date` · `items[].remark`

## §4.6 Data Classification
Default Internal · PII overlay: preparer_name_snapshot · ข้อมูลตัวอย่าง prototype = ชื่อ/สินค้าสมมติ

## §4.7 Retention
ตามนโยบายเอกสารคลังสินค้า (ยืนยันกับ Policy Center) · ไม่ hard delete
