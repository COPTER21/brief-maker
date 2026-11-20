# 02_API — F-TMP-006
> base `/api/v1/internal-reviews` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/internal-reviews?q&status&final_status&dept&mine_to_act&page&size&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/internal-reviews/{id}` | รายละเอียด + reviews + approvals + chain + audit | FN-10 |
| API-03 | POST `/internal-reviews` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-03 |
| API-04 | PUT `/internal-reviews/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/internal-reviews/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-04 |
| API-06 | POST `/internal-reviews/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-04 |
| API-07 | POST `/internal-reviews/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-05, FN-06 |
| API-08 | POST `/internal-reviews/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-09 | GET `/internal-reviews/{id}/pdf` | PDF FM-BDM-06 (2 หน้า) | FN-08 |
| API-10 | GET `/internal-reviews/export.csv` | CSV ตามตัวกรอง | FN-10 |
| API-11 | POST/DELETE `/internal-reviews/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ reviews:[{item, reviewer, review_date, result, comment, fix_owner, status}], approvals:[{approver_name, position, decision, decided_date, evidence}] (เฉพาะ source=manual), final:{approval_status, effective_date, remark}, attachment_ids[] }` · แถว source=doa ไม่รับจาก FE (server เก็บเอง FN-05/06) · 422 ตาม VR-01..04
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- response มี `open_items` (จำนวนแถวสถานะ ≠ closed_status) · `warnings[]` (complete_with_open · closed_without_owner) — เตือน ไม่บล็อก

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | irv_cancelled · irv_approved_open_items | {ref: internal_review_id, vars} | ✓ |
| ENG-DOC-STORE | store(pdf,'IRV',id,'approved_final') | | ✓ |
| ระบบอื่น | — | | ไม่ส่งต่อ (DEC-02) |
