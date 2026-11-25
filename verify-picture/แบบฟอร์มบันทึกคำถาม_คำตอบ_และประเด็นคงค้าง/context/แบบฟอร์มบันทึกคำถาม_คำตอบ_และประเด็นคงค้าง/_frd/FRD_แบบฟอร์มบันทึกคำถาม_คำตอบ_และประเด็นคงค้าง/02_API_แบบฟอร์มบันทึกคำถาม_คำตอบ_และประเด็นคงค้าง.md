# 02_API — F-TMP-005
> base `/api/v1/ivm-qa-logs` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/ivm-qa-logs?q&status&late&mine_to_act&page&size&sort` | รายการตามสิทธิ์ | FN-11 |
| API-02 | GET `/ivm-qa-logs/{id}` | รายละเอียด + questions + issues + chain + audit | FN-11 |
| API-03 | POST `/ivm-qa-logs` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-04 |
| API-04 | PUT `/ivm-qa-logs/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/ivm-qa-logs/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-05 |
| API-06 | POST `/ivm-qa-logs/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-05 |
| API-07 | POST `/ivm-qa-logs/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-06, FN-07 |
| API-08 | POST `/ivm-qa-logs/{id}/cancel` `{reason}` | ยกเลิก | FN-08 |
| API-09 | GET `/ivm-qa-logs/{id}/pdf` | PDF FM-IVM-03 | FN-09 |
| API-10 | GET `/ivm-qa-logs/export.csv` | CSV ตามตัวกรอง | FN-11 |
| API-11 | POST/DELETE `/ivm-qa-logs/{id}/attachments` | ไฟล์ (Document Center) | FN-03 |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ project_name, questions:[{asked_date, question, asker, responder, answer, evidence, status, due_date, remark}], issues:[{opened_date, issue, category, owner, priority, due_date, status, escalate, remark}], attachment_ids[] }` → 422 ตาม VR-01..08 · `q_no` / `oi_no` สร้างฝั่ง server ตามลำดับ (ส่งมาจะถูกละ) · response มี `warnings[]` (OVERDUE_QUESTION · OVERDUE_ISSUE) ไม่บล็อก
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- Events (FN-10): `ivmc_cancelled` · `ivmc_log_approved` · `ivmc_escalation_flagged` ผ่าน ENG-NOTIFY · `ivmc.approved` ประกาศไว้ไม่ยิง (DEC-02)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)
