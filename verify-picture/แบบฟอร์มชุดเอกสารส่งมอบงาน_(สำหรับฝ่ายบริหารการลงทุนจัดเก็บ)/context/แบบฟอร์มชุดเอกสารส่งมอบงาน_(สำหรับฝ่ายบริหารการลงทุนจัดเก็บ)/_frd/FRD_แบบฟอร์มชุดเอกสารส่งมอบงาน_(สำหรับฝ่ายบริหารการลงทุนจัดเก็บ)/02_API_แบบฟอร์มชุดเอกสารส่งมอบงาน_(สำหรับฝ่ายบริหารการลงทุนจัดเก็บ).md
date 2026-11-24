# 02_API — F-TMP-008
> base `/api/v1/handover-records` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/handover-records?q&status&result&dept&mine_to_act&page&size&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/handover-records/{id}` | รายละเอียด + items + chain + audit | FN-10 |
| API-03 | POST `/handover-records` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-03 |
| API-04 | PUT `/handover-records/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/handover-records/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-04 |
| API-06 | POST `/handover-records/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-04 |
| API-07 | POST `/handover-records/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-05, FN-06 |
| API-08 | POST `/handover-records/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-09 | GET `/handover-records/{id}/pdf` | PDF FM-BDM-08 (2 หน้า) | FN-08 |
| API-10 | GET `/handover-records/export.csv` | CSV ตามตัวกรอง | FN-10 |
| API-11 | POST/DELETE `/handover-records/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ handover:{project_name, sender, receiver, received_date, received_time, package_version, result}, items:[{doc_name, doc_code_rev, received, completeness, issue, fix_owner, due_date}], followup:{open_issues, pending_docs, followup_date, remark}, attachment_ids[] }` · 422 ตาม VR-01..08
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- response มี `open_items` (จำนวนแถวไม่ผ่าน — คำนวณฝั่ง server FN-02)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | hoi_cancelled · hoi_acknowledged_open_items | {ref: handover_record_id, vars} | ✓ |
| ENG-DOC-STORE | store(pdf,'HOI',id,'approved_final') | | ✓ |
| ระบบอื่น | — | | ไม่ส่งต่อ (DEC-02) |
