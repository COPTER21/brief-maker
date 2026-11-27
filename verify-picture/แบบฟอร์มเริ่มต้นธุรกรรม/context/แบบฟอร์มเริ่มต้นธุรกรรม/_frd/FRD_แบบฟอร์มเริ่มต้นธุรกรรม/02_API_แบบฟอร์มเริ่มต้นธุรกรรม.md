# 02_API — F-TMP-001
> base `/api/v1/transaction-initiations` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/transaction-initiations?q&status&returned&dept&mine_to_act&page&size&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/transaction-initiations/{id}` | รายละเอียด + chain + revisions + audit | FN-10 |
| API-03 | POST `/transaction-initiations` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-03 |
| API-04 | PUT `/transaction-initiations/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/transaction-initiations/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-04 |
| API-06 | POST `/transaction-initiations/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain · ฉบับใหม่ถ้าถูกส่งกลับ | FN-04 |
| API-07 | POST `/transaction-initiations/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-05, FN-06 |
| API-08 | POST `/transaction-initiations/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-09 | GET `/transaction-initiations/{id}/pdf` | PDF FM-IVM-01 | FN-08 |
| API-10 | GET `/transaction-initiations/export.csv` | CSV ตามตัวกรอง | FN-10 |
| API-11 | POST/DELETE `/transaction-initiations/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ txn:{name, owner, source, type, start_date, responsible_id, internal_units, external_parties}, scope:{objective, work_scope, deliverables, data_received, open_issues}, attachment_ids[] }` → 422 ตาม VR-01..04
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- API-03 เมื่อ doc_type ปิดใช้ → 409 `DOC_TYPE_INACTIVE`

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | ivma_cancelled · ivma_responsible_assigned | {ref: ivma_id, vars} | ✓ |
| ENG-DOC-STORE | store(pdf,'IVMA',id,'approved_final') | | ✓ |
| FM-IVM-02..11 | `ivma.approved` {ivma_id, doc_no, txn_name, responsible_id, start_date} | | ประกาศ ไม่ยิง (DEC-02) |
