# 02_API — F-FIN-ACL
> base `/api/v1/advance-clearings` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/advance-clearings?q&status&result&dept&mine_to_act&page&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/advance-clearings/{id}` | รายละเอียด + chain + audit | FN-10 |
| API-03 | POST `/advance-clearings` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-03 |
| API-04 | PUT `/advance-clearings/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/advance-clearings/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-04 |
| API-06 | POST `/advance-clearings/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-04 |
| API-07 | POST `/advance-clearings/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-05, FN-06 |
| API-08 | POST `/advance-clearings/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-09 | GET `/advance-clearings/{id}/pdf` | PDF FM-FIN-02 | FN-08 |
| API-10 | GET `/advance-clearings/export.csv` | CSV ตามตัวกรอง | FN-10 |
| API-11 | POST/DELETE `/advance-clearings/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ advance_ref, advance_amount, lines:[{description, amount}], attachment_ids[] }` · amount เป็น string ทศนิยม 2 → 422 ตาม VR-01..03
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject) · 422 `REFUND_SLIP_REQUIRED` (ขั้น role-finance-officer · refund>0 · ไม่มีไฟล์ประเภทสลิป)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/การเงิน) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | acl_cancelled · acl_overspent_approved · acl_refund_due | {ref: acl_id, vars} | ✓ |
| ENG-DOC-STORE | store(pdf,'ACL',id,'approved_final') | | ✓ |
| AP/GL | `acl.approved` {acl_id, advance_ref, total_expense, refund_amount} | | ประกาศ ไม่ยิง (DEC-02) |
