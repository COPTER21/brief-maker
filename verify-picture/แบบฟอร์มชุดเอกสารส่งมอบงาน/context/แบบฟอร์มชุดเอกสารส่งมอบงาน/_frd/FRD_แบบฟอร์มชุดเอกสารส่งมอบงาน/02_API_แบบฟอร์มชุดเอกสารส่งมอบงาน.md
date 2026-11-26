# 02_API — F-TMP-008
> base `/api/v1/ivm-handovers` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/ivm-handovers?q&status&result&mine_to_act&page&size&sort` | รายการตามสิทธิ์ | FN-11 |
| API-02 | GET `/ivm-handovers/{id}` | รายละเอียด + items + chain + audit | FN-11 |
| API-03 | POST `/ivm-handovers` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-04 |
| API-04 | PUT `/ivm-handovers/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/ivm-handovers/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-05 |
| API-06 | POST `/ivm-handovers/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-05 |
| API-07 | POST `/ivm-handovers/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-06, FN-07 |
| API-08 | POST `/ivm-handovers/{id}/cancel` `{reason}` | ยกเลิก | FN-08 |
| API-09 | GET `/ivm-handovers/{id}/pdf` | PDF FM-IVM-06 | FN-09 |
| API-10 | GET `/ivm-handovers/export.csv` | CSV ตามตัวกรอง | FN-11 |
| API-11 | POST/DELETE `/ivm-handovers/{id}/attachments` | ไฟล์ (Document Center) | FN-03 |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ project_name, sender_name, receiver_name, handover_at, package_version, handover_result, items:[{doc_name, doc_ref, received, completeness, issue, fix_owner, due_date}], open_issues, pending_docs, followup_schedule, ivm_remark, attachment_ids[] }` → 422 ตาม VR-01..10 · `seq` สร้างฝั่ง server ตามลำดับ (ส่งมาจะถูกละ) · received = no → server ตั้ง completeness = incomplete · response มี `warnings[]` (RESULT_NOT_SUGGESTED + suggested_result) ไม่บล็อก
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- Events (FN-10): `ivmf_cancelled` · `ivmf_handover_followup` ผ่าน ENG-NOTIFY · `ivmf.approved` ประกาศไว้ไม่ยิง (DEC-02)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)
