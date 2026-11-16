# 02_API — F-TMP-003
> base `/api/v1/slow-move-clearances` · tenant จาก token (RLS) · ทุก write มี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/slow-move-clearances?q&status&month&mine_to_act&page&sort` | รายการตามสิทธิ์ | FN-11 |
| API-02 | GET `/slow-move-clearances/{id}` | รายละเอียด + รายการ + chain + audit | FN-11 |
| API-03 | POST `/slow-move-clearances` | สร้างร่าง + ออกเลข + snapshot สินค้า/แนวทาง | FN-01, FN-02, FN-03 |
| API-04 | PUT `/slow-move-clearances/{id}` | แก้ไข (เจ้าของ · draft/returned) | FN-01, FN-02, FN-04 |
| API-05 | GET `/slow-move-clearances/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-05 |
| API-06 | POST `/slow-move-clearances/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-05 |
| API-07 | POST `/slow-move-clearances/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-06, FN-07 |
| API-08 | POST `/slow-move-clearances/{id}/cancel` `{reason}` | ยกเลิก | FN-08 |
| API-09 | GET `/slow-move-clearances/{id}/pdf` | PDF FM-WHS-09 (2 หน้า) | FN-09 |
| API-10 | GET `/slow-move-clearances/export.csv` | CSV ตามตัวกรอง | FN-11 |
| API-11 | POST/DELETE `/slow-move-clearances/{id}/attachments` | ไฟล์ (Document Center) | — |
| API-12 | GET `/slow-move-config/clearance-methods` | แนวทางการเคลียร์ปัจจุบัน — อ่านอย่างเดียว | FN-02 |
| API-13 | GET `/products?active=true&q` (F-PRODUCT-MASTER-001) | ค้นหาสินค้า (รหัส · ชื่อ · หน่วย) — อ่านอย่างเดียว | FN-02 |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ clearance_month:'YYYY-MM', items:[{seq, product_code, follow_up_date, clearance_method_code, clearance_method_note, cleared_date, cleared_qty, expiry_date, remark}], attachment_ids[] }` → 422 ตาม VR-01..06 (`MONTH_INVALID` · `NO_ITEM` · `PRODUCT_REQUIRED` · `PRODUCT_INACTIVE` · `FOLLOW_UP_REQUIRED` · `FUTURE_DATE` · `METHOD_REQUIRED` · `METHOD_NOTE_REQUIRED` · `CLEARED_PAIR_REQUIRED` · `QTY_NOT_POSITIVE` · `CLEARED_BEFORE_FOLLOW_UP`) · response มี `warnings[]` (`EXPIRED_AT_FOLLOW_UP` · `DUPLICATE_PRODUCT`) ไม่บล็อก
- API-04: 409 `NOT_EDITABLE` (ไม่ใช่ draft/returned) · 403 `NOT_OWNER`
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin role-mgr-wh) · 409 `NOT_CANCELLABLE` (approved/cancelled) · 422 `REASON_REQUIRED`
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | smc_cancelled | {ref: clearance_id, vars} | ✓ |
| ENG-DOC-STORE | store(pdf,'SMC',id,'approved_final') | | ✓ |
| Stock Adjustment / Transfer / Purchase Return | `smc.approved` {clearance_id, items[{product_code, clearance_method_code, cleared_qty, cleared_date}]} | | ประกาศ ไม่ยิง (DEC-02) |
