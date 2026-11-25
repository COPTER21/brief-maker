# 02_API — F-TMP-003
> base `/api/v1/account-code-requests` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/account-code-requests?q&status&type&mine_to_act&to_record&page&page_size&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/account-code-requests/{id}` | รายละเอียด + chain + recorded + audit | FN-10 |
| API-03 | POST `/account-code-requests` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-03 |
| API-04 | PUT `/account-code-requests/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/account-code-requests/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-04 |
| API-06 | POST `/account-code-requests/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-04 |
| API-07 | POST `/account-code-requests/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-05, FN-06 |
| API-08 | POST `/account-code-requests/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-09 | POST `/account-code-requests/{id}/record` `{recorded_at}` | บันทึกเข้าระบบแล้ว | FN-11 |
| API-10 | GET `/account-code-requests/{id}/pdf` | PDF FM-ACC-01 | FN-08 |
| API-11 | GET `/account-code-requests/export.csv` | CSV ตามตัวกรอง | FN-10 |
| API-12 | POST/DELETE `/account-code-requests/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ request_type, add:{lines:[{account_name}], purpose}, edit:{account_code, change_to, purpose}, cancel:{account_code, account_name, purpose}, attachment_ids[] }` → server เก็บเฉพาะส่วนของ request_type (อื่นล้าง) · 422 ตาม VR-01..06 (`TYPE_REQUIRED` · `ADD_LINES_REQUIRED` · `DUPLICATE_ACCOUNT_NAME` · `PURPOSE_REQUIRED` · `EDIT_INCOMPLETE` · `CANCEL_INCOMPLETE`)
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject · DEC-14)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/recorded/cancelled)
- API-09: 409 `NOT_APPROVED` · 403 `NOT_RECORDER` (ไม่ใช่ admin ฝ่ายบัญชี) · 422 `RECORDED_AT_INVALID` (> วันนี้ หรือ < วันที่อนุมัติ)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | acr_cancelled · acr_ready_to_record · acr_recorded | {ref: acr_id, vars} | ✓ |
| ENG-DOC-STORE | store(pdf,'ACR',id,'approved_final') | | ✓ |
| COA | `acr.approved` {acr_id, request_type, account_code, account_names[], change_to} | | ประกาศ ไม่ยิง (DEC-02) |
