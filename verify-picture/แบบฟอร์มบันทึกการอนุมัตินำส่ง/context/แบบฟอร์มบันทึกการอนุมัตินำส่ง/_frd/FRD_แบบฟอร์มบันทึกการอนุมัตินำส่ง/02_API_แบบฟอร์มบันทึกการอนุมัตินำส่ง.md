# 02_API — F-TMP-010
> base `/api/v1/ivm-submission-approvals` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/ivm-submission-approvals?q&status&authority_level&mine_to_act&page&size&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/ivm-submission-approvals/{id}` | รายละเอียด + chain + audit | FN-10 |
| API-03 | POST `/ivm-submission-approvals` | สร้างร่าง + ออกเลข | FN-01, FN-03 |
| API-04 | PUT `/ivm-submission-approvals/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01 |
| API-05 | GET `/ivm-submission-approvals/{id}/doa-preview?authority_level` | resolve สายค่าเริ่ม (slot) | FN-04 |
| API-06 | POST `/ivm-submission-approvals/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-04 |
| API-07 | POST `/ivm-submission-approvals/{id}/decide` `{decision: approve\|approve_cond\|ack\|revise\|reject, instruction}` | พิจารณาขั้นปัจจุบัน | FN-05, FN-06 |
| API-08 | POST `/ivm-submission-approvals/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-09 | GET `/ivm-submission-approvals/{id}/pdf` | PDF FM-IVM-08 | FN-08 |
| API-10 | GET `/ivm-submission-approvals/export.csv` | CSV ตามตัวกรอง | FN-10 |
| API-11 | POST/DELETE `/ivm-submission-approvals/{id}/attachments` | ไฟล์ (Document Center) | FN-02 |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ project_name, subject, supporting_docs, authority_level, ivm_proposal, proposed_conditions, attachment_ids[] }` → 422 ตาม VR-01/02 · ตารางผลการพิจารณาไม่รับจาก client (ระบบเติม)
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `INSTRUCTION_REQUIRED` (approve_cond/revise/reject) · 422 `ACK_NOT_ALLOWED` (ack ขั้น 1/ขั้นสุดท้าย)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- Events (FN-09): `ivmh_cancelled` · `ivmh_conditional_approved` ผ่าน ENG-NOTIFY · `ivmh.approved` ประกาศไว้ไม่ยิง (DEC-02)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)
