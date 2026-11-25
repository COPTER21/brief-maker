# 02_API — F-TMP-006
> base `/api/v1/ivm-data-rooms` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/ivm-data-rooms?q&status&open_docs&mine_to_act&page&size&sort` | รายการตามสิทธิ์ | FN-11 |
| API-02 | GET `/ivm-data-rooms/{id}` | รายละเอียด + folders + documents + changes + access + chain + audit | FN-11 |
| API-03 | POST `/ivm-data-rooms` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-04 |
| API-04 | PUT `/ivm-data-rooms/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/ivm-data-rooms/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-05 |
| API-06 | POST `/ivm-data-rooms/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-05 |
| API-07 | POST `/ivm-data-rooms/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-06, FN-07 |
| API-08 | POST `/ivm-data-rooms/{id}/cancel` `{reason}` | ยกเลิก | FN-08 |
| API-09 | GET `/ivm-data-rooms/{id}/pdf` | PDF FM-IVM-04 | FN-09 |
| API-10 | GET `/ivm-data-rooms/export.csv` | CSV ตามตัวกรอง | FN-11 |
| API-11 | POST/DELETE `/ivm-data-rooms/{id}/attachments` | ไฟล์ (Document Center) | FN-03 |
| API-12 | GET `/ivm-data-rooms/defaults` | มาตรฐานการตั้งชื่อไฟล์ + โฟลเดอร์มาตรฐาน (config) สำหรับใบใหม่ | FN-12 |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ project_name, folders:[{folder_name, owner, access_level, required_docs, remark}], documents:[{doc_name, owner, version, version_date, doc_status, location, reviewer, approver, remark}], changes:[{change_date, doc_ref, detail, reason, impact, approver, effective_date, status, remark}], access:[{user_name, org_unit, role, access_level, scope, granted_date, revoked_date, approver, status}], attachment_ids[] }` → 422 ตาม VR-01..10 · `folder_no` / `doc_code` / `change_code` / `seq` / `std_file_name` คำนวณฝั่ง server (ส่งมาจะถูกละ) · `naming_snapshot` ตั้งตอนออกเลข (ส่งมาจะถูกละ) · response มี `warnings[]` (NOT_FINAL_VERSION · EFFECTIVE_BEFORE_DATE) ไม่บล็อก
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- Events (FN-10): `ivmd_cancelled` · `ivmd_register_approved` ผ่าน ENG-NOTIFY · `ivmd.approved` ประกาศไว้ไม่ยิง (DEC-02)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS · `location` ห้ามมีรหัสผ่าน/token (ตรวจ pattern `password=|token=` → 422 CREDENTIAL_IN_LINK)

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)
