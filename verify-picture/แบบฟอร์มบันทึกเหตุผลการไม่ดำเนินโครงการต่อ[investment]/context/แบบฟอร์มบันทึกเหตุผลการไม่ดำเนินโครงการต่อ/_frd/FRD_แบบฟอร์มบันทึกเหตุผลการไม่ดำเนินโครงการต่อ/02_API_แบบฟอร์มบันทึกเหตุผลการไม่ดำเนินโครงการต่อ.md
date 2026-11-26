# 02_API — F-TMP-002
> base `/api/v1/ivm-discontinuations` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/ivm-discontinuations?q&status&result&mine_to_act&page&size&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/ivm-discontinuations/{id}` | รายละเอียด + reasons + chain + audit | FN-10 |
| API-03 | POST `/ivm-discontinuations` | สร้างร่าง + ออกเลข | FN-01, FN-03 |
| API-04 | PUT `/ivm-discontinuations/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01 |
| API-05 | GET `/ivm-discontinuations/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-04 |
| API-06 | POST `/ivm-discontinuations/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-04 |
| API-07 | POST `/ivm-discontinuations/{id}/decide` `{decision: approve\|reject, note, result?, instruction?}` | ตัดสินขั้นปัจจุบัน | FN-05, FN-06 |
| API-08 | POST `/ivm-discontinuations/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-09 | GET `/ivm-discontinuations/{id}/pdf` | PDF FM-IVM-10 | FN-08 |
| API-10 | GET `/ivm-discontinuations/export.csv` | CSV ตามตัวกรอง | FN-10 |
| API-11 | POST/DELETE `/ivm-discontinuations/{id}/attachments` | ไฟล์ (Document Center) | FN-02 |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ project_name, owner_employee_id, proposed_date, stopped_at_step, reasons:[{reason, selected:'yes'|'no', detail, evidence_ref, impact, reconsider_condition, owner, remark}], summary:{reason, supporting_docs, result, instruction, archive_plan, follow_up}, attachment_ids[] }` → 422 ตาม VR-01..06
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject) · 422 `INSTRUCTION_REQUIRED` (ขั้นสุดท้าย result=continue_conditional ไม่มี instruction) · `result` รับเฉพาะขั้นสุดท้าย (อื่น → 422 `RESULT_NOT_ALLOWED`)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- Events (FN-09): `ivmj_cancelled` · `ivmj_result_recorded` ผ่าน ENG-NOTIFY · `ivmj.approved` ประกาศไว้ไม่ยิง (DEC-02)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)
