# 02_API — F-TMP-003
> base `/api/hr/visitor-access` · tenant จาก token · สิทธิ์ตาม 05 §5.3 (ไม่มีสิทธิ์ = 404) · optimistic lock ด้วย `version`

## §2.1 Endpoints
| API | Method · Path | ใช้ทำ | FN |
|---|---|---|---|
| API-01 | GET `/` ?q&status&division&page&size&sort | รายการที่เห็นได้ (page-size ค่าเริ่ม 25) | FN-09 |
| API-02 | GET `/{id}` | รายละเอียด + approval_chain + audit + attachments | FN-09 |
| API-03 | GET `/prefill?host_employee_id=` | ดึง host.full_name/division/line_manager | FN-01 |
| API-04 | POST `/` | บันทึกร่าง (ออกเลข VAR ครั้งแรก) | FN-02, FN-03 |
| API-05 | PUT `/{id}` | แก้ร่าง (เฉพาะ owner · status=draft) | FN-02 |
| API-06 | GET `/doa/resolve?feature_id=F-TMP-003&host_employee_id=` | resolve steps + assignee ค่าเริ่ม (DOA กลาง) | FN-04 |
| API-07 | POST `/{id}/submit` {assignees[]} | ส่งขออนุมัติ (snapshot approval_chain) | FN-02, FN-04 |
| API-08 | POST `/{id}/decide` {decision: approve\|reject, note} | อนุมัติ / ไม่อนุมัติ (กลับร่าง) — DOA callback | FN-05 |
| API-09 | POST `/{id}/cancel` {reason} | ยกเลิก | FN-06 |
| API-10 | GET `/{id}/pdf` | PDF แบบพิมพ์ FM-HRM-05 | FN-07 |
| API-11 | GET `/export.csv` | CSV ตามสิทธิ์ (ไม่มีโทรศัพท์) | FN-09 |
| API-12 | POST/DELETE `/{id}/attachments` | แนบไฟล์ → Document Center (ref_type='VAR') | FN-02 |

## §2.2 Contract (หลัก)
- request body (API-04/05): `{ visit:{request_date, purpose}, visitor:{title, full_name, phone, company, sign_date}, host_employee_id, attachments[] }`
- response: `{ id, doc_no, status, version, host:{full_name, division, line_manager}, approval_chain[], header_snapshot, ... }`
- error: 400 VALIDATION {field, code} · 404 · 409 DOC_TYPE_INACTIVE · 409 STALE_VERSION · 409 HOST_NO_MANAGER · 403 SELF_APPROVAL
## §2.3 DOA / Notify
- API-06/07/08 เป็นตามมาตรฐาน DOA กลาง (approver_role / approved_by / approval_chain) — `TODO: DOA engine` wire ตาม DOA_BRIEF_F-TMP-003 (wire_status pending)
- API-09 emit `var_cancelled` (FN-08) เมื่อยกเลิกจาก pending · doa_pending/doa_result ยิงโดย DOA engine
## §2.4 API ↔ FN
ทุก API ผูก FN (คอลัมน์ FN ใน §2.1) ✓
