# 02_API — F-TMP-007
> base `/api/v1/handover-packages-bd` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/handover-packages-bd?q&status&data_status&dept&mine_to_act&page&size&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/handover-packages-bd/{id}` | รายละเอียด + items + chain + audit | FN-10 |
| API-03 | POST `/handover-packages-bd` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-03 |
| API-04 | PUT `/handover-packages-bd/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/handover-packages-bd/{id}/doa-preview` | resolve สายค่าเริ่ม (slot · ขั้นรับทราบ = ผู้รับมอบ) | FN-04 |
| API-06 | POST `/handover-packages-bd/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-04 |
| API-07 | POST `/handover-packages-bd/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-05, FN-06 |
| API-08 | POST `/handover-packages-bd/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-09 | GET `/handover-packages-bd/{id}/pdf` | PDF FM-BDM-07 (2 หน้า) | FN-08 |
| API-10 | GET `/handover-packages-bd/export.csv` | CSV ตามตัวกรอง | FN-10 |
| API-11 | POST/DELETE `/handover-packages-bd/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ handover:{project_name, sender_id, receiver_id, handover_date, package_version, data_status}, items:[{doc_name, doc_ref, doc_date, owner_name, status, location, remark}], notes:{assumptions, open_issues, data_limits, bd_support}, attachment_ids[] }` · 422 ตาม VR-01..05
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- response มี `gap_items` (จำนวนแถวสถานะ ∈ gap_doc) · `warnings[]` (complete_with_gap · doc_after_handover) — เตือน ไม่บล็อก

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | hob_cancelled · hob_received_with_gaps | {ref: handover_package_id, vars} | ✓ |
| ENG-DOC-STORE | store(pdf,'HOB',id,'approved_final') | | ✓ |
| ระบบอื่น / FM-BDM-08 | — | | ไม่ส่งต่อ (DEC-02) |
