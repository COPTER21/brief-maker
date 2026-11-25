# 02_API — F-TMP-007
> base `/api/v1/ivm-doc-requests` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/ivm-doc-requests?q&status&overdue&mine_to_act&page&size&sort` | รายการตามสิทธิ์ | FN-11 |
| API-02 | GET `/ivm-doc-requests/{id}` | รายละเอียด + items + summary + chain + audit | FN-11 |
| API-03 | POST `/ivm-doc-requests` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-04 |
| API-04 | PUT `/ivm-doc-requests/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/ivm-doc-requests/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-05 |
| API-06 | POST `/ivm-doc-requests/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-05 |
| API-07 | POST `/ivm-doc-requests/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-06, FN-07 |
| API-08 | POST `/ivm-doc-requests/{id}/cancel` `{reason}` | ยกเลิก | FN-08 |
| API-09 | GET `/ivm-doc-requests/{id}/pdf` | PDF FM-IVM-05 | FN-09 |
| API-10 | GET `/ivm-doc-requests/export.csv` | CSV ตามตัวกรอง (1 แถวต่อคำขอ) | FN-11 |
| API-11 | POST/DELETE `/ivm-doc-requests/{id}/attachments` | ไฟล์ (Document Center) | FN-03 |
| API-12 | GET `/ivm-doc-requests/defaults` | prefix รหัสคำขอ + หมายเหตุการใช้งาน (config) สำหรับใบใหม่ | FN-12 |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ project_name, items:[{request_code?, item, requestee, owner, request_date, due_date, status, received_date, remark, doc_link}], attachment_ids[] }` → 422 ตาม VR-01..09 · `request_code` ของแถวใหม่ (ไม่ส่งมา) ออกฝั่ง server = prefix + (max+1) · แถวเดิมคงรหัส · `usage_note_snapshot` ตั้งตอนออกเลข (ส่งมาจะถูกละ) · response มี `summary{total, received, partial, pending, closed, overdue}` + `warnings[]` (OVERDUE · CREDENTIAL_WORD) ไม่บล็อก
- API-06: 409 `NOT_DRAFT` · 422 `NO_ITEMS` (VR-10) · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- Events (FN-10): `ivme_cancelled` · `ivme_request_list_approved` ผ่าน ENG-NOTIFY · `ivme.approved` ประกาศไว้ไม่ยิง (DEC-02)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS · `doc_link` ต้องเป็น URL/path (422 LINK_FORMAT) · คำว่า password/รหัสผ่าน ใน doc_link/remark → warning CREDENTIAL_WORD (ไม่เก็บค่า credential ใน log)

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)
