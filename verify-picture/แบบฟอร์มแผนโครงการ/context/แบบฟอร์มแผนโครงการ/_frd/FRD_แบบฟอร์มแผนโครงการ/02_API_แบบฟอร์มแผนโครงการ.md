# 02_API — F-TMP-004
> base `/api/v1/project-plans` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/project-plans?q&status&owner_dept&mine_to_act&delayed&page&page_size&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/project-plans/{id}` | รายละเอียด + goals/actions/budget/risks + chain + audit | FN-10 |
| API-03 | POST `/project-plans` | สร้างร่าง + ออกรหัสโครงการ | FN-01, FN-02, FN-03 |
| API-04 | PUT `/project-plans/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/project-plans/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-04 |
| API-06 | POST `/project-plans/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-04 |
| API-07 | POST `/project-plans/{id}/decide` `{decision: approve\|reject, approved_budget[]?, note}` | ตัดสินขั้นปัจจุบัน (approved_budget เฉพาะขั้นสุดท้าย) | FN-05, FN-06 |
| API-08 | POST `/project-plans/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-09 | PATCH `/project-plans/{id}/actions/status` `{items:[{action_id, status}]}` | อัปเดตสถานะกิจกรรม (approved) | FN-11 |
| API-10 | GET `/project-plans/{id}/pdf` | PDF FM-PDM-01 (2 หน้า) | FN-08 |
| API-11 | GET `/project-plans/export.csv` | CSV 1 แถวต่อกิจกรรมตามตัวกรอง | FN-10 |
| API-12 | POST/DELETE `/project-plans/{id}/attachments` | ไฟล์ (Document Center) | — |
| API-13 | GET `/employees?q` · GET `/org-units` (อ่าน) | combobox ผู้รับผิดชอบ/หน่วยงาน | — (feature เจ้าของ) |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ project_name, owner_dept_id, project_manager_id, start_date, end_date, background, problem_opportunity, justification, objective_primary, objective_secondary, goals:[{quantitative, qualitative, kpi, method}], actions:[{activity, responsible_id, start_date, end_date, status}], budget:[{item, requested, remark}], risks:[{risk, impact, severity, mitigation, owner_id}], benefit_financial, benefit_operational, benefit_strategic, attachment_ids[] }` → 422 ตาม VR-01..06 (`FIELD_REQUIRED` · `END_BEFORE_START` · `GROUP_MIN_ROWS` · `ROW_INCOMPLETE` · `AMOUNT_INVALID`) · ไม่มี duration/total ใน body (คำนวณฝั่ง server)
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject) · 422 `APPROVED_BUDGET_INVALID` (approve ขั้นสุดท้าย · ค่า < 0) · approved_budget ถูกส่งในขั้นที่ไม่ใช่ขั้นสุดท้าย = ไม่สนใจ
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-09: 409 `NOT_APPROVED` · 403 `NOT_PLAN_OWNER` (ไม่ใช่ผู้จัดทำ/ผู้รับผิดชอบหลัก) · 422 `STATUS_INVALID` (นอก 4 ค่า)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | pjp_cancelled · pjp_budget_adjusted · pjp_activity_delayed | {ref: plan_id, vars} | ✓ |
| ENG-DOC-STORE | store(pdf,'PJP',id,'approved_final') | | ✓ |
| Budget | `pjp.approved` {plan_id, doc_no, owner_dept, budget[item, approved]} | | ประกาศ ไม่ยิง (DEC-02) |
