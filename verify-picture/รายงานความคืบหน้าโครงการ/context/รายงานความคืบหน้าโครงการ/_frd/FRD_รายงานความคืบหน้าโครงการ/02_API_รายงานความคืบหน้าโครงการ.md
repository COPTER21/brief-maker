# 02_API — F-TMP-005
> base `/api/v1/progress-reports` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/progress-reports?q&status&overall&project&mine_to_act&mine_to_submit&page&page_size&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/progress-reports/{id}` | รายละเอียด + ตารางลูก + chain + audit + warnings | FN-10 |
| API-03 | POST `/progress-reports` | สร้างร่าง + ออกเลข PPR | FN-01, FN-02, FN-03 |
| API-04 | PUT `/progress-reports/{id}` | แก้ร่าง (ผู้จัดทำ/PM · draft) | FN-01, FN-02 |
| API-05 | GET `/progress-reports/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) จาก PM | FN-04 |
| API-06 | POST `/progress-reports/{id}/submit` `{assignees[]}` | PM ส่ง · snapshot chain | FN-04 (+FN-09) |
| API-07 | POST `/progress-reports/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-05, FN-06 |
| API-08 | POST `/progress-reports/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-09 | POST `/progress-reports/{id}/notify-pm` | ผู้จัดทำแจ้งผู้จัดการโครงการ | FN-11 |
| API-10 | GET `/progress-reports/{id}/pdf` | PDF FM-PDM-02 (2 หน้า) | FN-08 |
| API-11 | GET `/progress-reports/export.csv` | CSV 1 แถวต่อกิจกรรมตามตัวกรอง | FN-10 |
| API-12 | POST/DELETE `/progress-reports/{id}/attachments` | ไฟล์ (Document Center) | — |
| API-13 | GET `/project-plans?status=approved&q` · GET `/project-plans/{id}` (F-TMP-004 · อ่าน) | lookup + ค่าเริ่ม | FN-02 (feature เจ้าของ) |
| API-14 | GET `/employees?q` (อ่าน) | combobox ผู้รับผิดชอบ | — (feature เจ้าของ) |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ project_plan_id, period_from, period_to, report_date, overall_status, status_note, schedule_plan, schedule_actual, schedule_status, budget_plan, budget_actual, budget_status, performance:[{activity, plan, actual, pct, remarks}], kpis:[{metric, plan, actual, status}], issues:[{description, impact, resolution, owner_id, due_date}], next_plan:[{description, owner_id, due_date}], decisions_needed:[{topic, options, recommendation, impact}] }` → 201 `{id, doc_no, version, warnings[]}` · 422 `VALIDATION` {field errors VR-01..07} · 409 `DOC_TYPE_INACTIVE` · 422 `PROJECT_NOT_APPROVED`
- API-06: 409 `NOT_DRAFT` · 403 `NOT_PROJECT_MANAGER` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04) · 409 `PROJECT_NOT_ACTIVE` (OQ-06)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE`
- API-09: 409 `NOT_DRAFT` · 403 `NOT_OWNER` · ผู้เรียกเป็น PM เอง = 422 `IS_PROJECT_MANAGER`
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | ppr_cancelled · ppr_draft_for_pm · ppr_urgent_decision | {ref: report_id, vars} | ✓ |
| ENG-DOC-STORE | store(pdf,'PPR',id,'approved_final') | | ✓ |
| F-TMP-004 | `ppr.approved` {report_id, project_plan_id, performance[]} | | ประกาศ ไม่ยิง (DEC-02 · OQ-08) |
