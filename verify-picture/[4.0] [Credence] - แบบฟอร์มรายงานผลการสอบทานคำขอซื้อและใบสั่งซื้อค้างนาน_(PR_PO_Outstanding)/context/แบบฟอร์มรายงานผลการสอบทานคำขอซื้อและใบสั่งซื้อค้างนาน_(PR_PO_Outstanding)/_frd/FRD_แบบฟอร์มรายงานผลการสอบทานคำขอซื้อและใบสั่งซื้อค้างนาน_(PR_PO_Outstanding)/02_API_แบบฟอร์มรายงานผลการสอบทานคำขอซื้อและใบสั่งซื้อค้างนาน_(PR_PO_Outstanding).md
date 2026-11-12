# 02_API — F-TMP-005
> base `/api/v1/pr-po-outstanding-reviews` · tenant จาก token (RLS) · ทุก write มี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/pr-po-outstanding-reviews?q&status&month&mine_to_act&page&sort` | รายการตามสิทธิ์ | FN-11 |
| API-02 | GET `/pr-po-outstanding-reviews/{id}` | รายละเอียด + รายการ + chain + audit | FN-11 |
| API-03 | POST `/pr-po-outstanding-reviews` | สร้างร่าง + ออกเลข + snapshot ผู้จัดทำ/หน่วยงาน/หน่วย | FN-01, FN-02, FN-03 |
| API-04 | PUT `/pr-po-outstanding-reviews/{id}` | แก้ไข (เจ้าของ · draft/returned) | FN-01, FN-02, FN-04 |
| API-05 | GET `/pr-po-outstanding-reviews/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-05 |
| API-06 | POST `/pr-po-outstanding-reviews/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-05 |
| API-07 | POST `/pr-po-outstanding-reviews/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-06, FN-07 |
| API-08 | POST `/pr-po-outstanding-reviews/{id}/cancel` `{reason}` | ยกเลิก | FN-08 |
| API-09 | GET `/pr-po-outstanding-reviews/{id}/pdf` | PDF FM-PUR-03 (2 หน้า) | FN-09 |
| API-10 | GET `/pr-po-outstanding-reviews/export.csv` | CSV ระดับรายการตามตัวกรอง | FN-11 |
| API-11 | POST/DELETE `/pr-po-outstanding-reviews/{id}/attachments` | ไฟล์ (Document Center) | — |
| API-12 | GET `/org-units?active=true&q` (F-ORG-001) | หน่วยงาน · ฝ่าย/แผนกขอซื้อ — อ่านอย่างเดียว | FN-02 |
| API-13 | GET `/uoms?active=true` (F-PRODUCT-MASTER-001 · uom_master) | หน่วยนับ — อ่านอย่างเดียว | FN-02 |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ report_date:'YYYY-MM-DD', org_unit_id, items:[{seq, pr_no, po_no, order_date, receive_date, vendor_name, description, order_qty, uom_code, request_org_unit_id, outstanding_reason, current_status, corrective_action}], attachment_ids[] }` → 422 ตาม VR-01..10 (`REPORT_DATE_REQUIRED` · `FUTURE_DATE` · `ORG_UNIT_REQUIRED` · `NO_ITEM` · `PR_OR_PO_REQUIRED` · `ORDER_DATE_REQUIRED` · `ORDER_AFTER_REPORT` · `RECEIVE_BEFORE_ORDER` · `VENDOR_REQUIRED` · `DESCRIPTION_REQUIRED` · `QTY_NOT_POSITIVE` · `UOM_REQUIRED` · `UOM_INACTIVE` · `DEPT_REQUIRED` · `REASON_TEXT_REQUIRED` · `STATUS_TEXT_REQUIRED` · `ACTION_TEXT_REQUIRED`) · response มี `warnings[]` (`DUPLICATE_PR_NO` · `DUPLICATE_PO_NO` · `PRINT_ROWS_EXCEEDED`) ไม่บล็อก
- API-04: 409 `NOT_EDITABLE` (ไม่ใช่ draft/returned) · 403 `NOT_OWNER`
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin role-mgr-pur) · 409 `NOT_CANCELLABLE` (approved/cancelled) · 422 `REASON_REQUIRED`
- API-02 ของรายงานที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | ppo_cancelled | {ref: review_id, vars} | ✓ |
| ENG-DOC-STORE | store(pdf,'PPO',id,'approved_final') | | ✓ |
| PR (F072) / PO (F078) | `ppo.approved` {review_id, items[{pr_no, po_no, corrective_action}]} | | ประกาศ ไม่ยิง (DEC-02 · ยังไม่มีในระบบ) |
