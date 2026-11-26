# 02_API — F-TMP-009
> base `/api/v1/ivm-dispatches` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/ivm-dispatches?q&status&confidentiality&mine_to_act&page&size&sort` | รายการตามสิทธิ์ | FN-12 |
| API-02 | GET `/ivm-dispatches/{id}` | รายละเอียด + docs + deliveries + chain + audit | FN-12 |
| API-03 | POST `/ivm-dispatches` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-04 |
| API-04 | PUT `/ivm-dispatches/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/ivm-dispatches/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-05 |
| API-06 | POST `/ivm-dispatches/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-05 |
| API-07 | POST `/ivm-dispatches/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-06, FN-07 |
| API-08 | POST `/ivm-dispatches/{id}/cancel` `{reason}` | ยกเลิก | FN-08 |
| API-09 | GET `/ivm-dispatches/{id}/pdf` | PDF FM-IVM-07 | FN-09 |
| API-10 | GET `/ivm-dispatches/export.csv` | CSV ตามตัวกรอง | FN-12 |
| API-11 | POST/DELETE `/ivm-dispatches/{id}/attachments` | ไฟล์ (Document Center) ระดับใบ + หลักฐานต่อแถว | FN-03 |
| API-12 | PUT `/ivm-dispatches/{id}/deliveries` `{deliveries:[…]}` | บันทึกหลักฐานการนำส่ง (หลังอนุมัติ) | FN-10, FN-11 |
| API-13 | POST `/ivm-dispatches/{id}/close` | ปิดการนำส่ง | FN-13, FN-11 |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ project_name, purpose, recipient, dispatch_date, docs:[{doc_name, version, status, confidentiality, remark}], attachment_ids[] }` → 422 ตาม VR-01..04 · `seq` สร้างฝั่ง server ตามลำดับ (ส่งมาจะถูกละ) · response มี `warnings[]` (DOCS_MISSING + count) ไม่บล็อก
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/closed/cancelled)
- API-12 body: `{ deliveries:[{id?, sent_at, sender, receiver, receiver_org, channel, docs_sent, evidence, evidence_file_id, remark, receipt_status}] }` (แทนทั้งชุด · audit before/after) → 409 `NOT_APPROVED` (status ≠ approved) · 403 `NOT_OWNER` · 422 ตาม VR-05..09 · response `warnings[]` (SENT_BEFORE_DISPATCH_DATE + rows)
- API-13: 409 `NOT_APPROVED` · 422 `NO_RECEIVED` · 422 `PENDING_CONFIRMATION` (+count) · 403 `NOT_OWNER`
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- Events (FN-11): `ivmg_cancelled` · `ivmg_delivery_failed` · `ivmg_dispatch_closed` ผ่าน ENG-NOTIFY · `ivmg.approved` / `ivmg.closed` ประกาศไว้ไม่ยิง (DEC-02)

## §2.3 Common
Idempotency-Key ทุก POST/PUT · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)
