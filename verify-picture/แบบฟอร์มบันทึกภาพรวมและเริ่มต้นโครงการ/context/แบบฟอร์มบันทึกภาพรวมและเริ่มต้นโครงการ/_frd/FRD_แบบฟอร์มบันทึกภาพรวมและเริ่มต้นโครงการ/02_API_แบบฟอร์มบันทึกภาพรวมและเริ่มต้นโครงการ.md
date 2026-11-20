# 02_API — F-TMP-001

## §2.1 API Overview
| API | Method · Path | ใช้ |
|---|---|---|
| API-01 | GET /api/v1/project-initiations?q&status&priority&project_status&mine_to_act&page | รายการที่เห็นได้ |
| API-02 | GET /api/v1/project-initiations/{id} | รายละเอียด (404 ถ้าไม่มีสิทธิ์) |
| API-03 | POST /api/v1/project-initiations | สร้างร่าง + ออกเลข PJI |
| API-04 | PUT /api/v1/project-initiations/{id} | แก้ร่าง (owner · draft · version) |
| API-05 | GET /api/v1/project-initiations/{id}/doa-preview | resolve สาย DOA ค่าเริ่ม |
| API-06 | POST /api/v1/project-initiations/{id}/submit | ส่ง {assignees[]} |
| API-07 | POST /api/v1/project-initiations/{id}/decision | {action: approve/reject, note/reason} |
| API-08 | POST /api/v1/project-initiations/{id}/cancel | {reason} |
| API-09 | GET /api/v1/project-initiations/{id}/pdf | PDF จาก template |
| API-10 | GET /api/v1/project-initiations/export.csv | CSV ตามตัวกรอง |
| API-11 | POST /api/v1/project-initiations/{id}/attachments | แนบไฟล์ (Document Center) |

## §2.2 Contract สำคัญ
- API-03/04 body: `{name, origin, type_opportunity, owner_id, supporters, start_date, target_date, priority, project_status, problem, objective, analysis_scope, deliverables, assumptions, constraints, plan[{activity, owner_id, supporter, start_date, due_date, status, remark}], revision_detail, version}`
- API-07 approve ครบขั้นสุดท้าย → ระบบยิง `pji_owner_assigned` (FN-09) · cancel ระหว่าง pending → `pji_cancelled`
- Errors: 400 VALIDATION (VR-01..05) · 403 NOT_OWNER / NOT_CURRENT_APPROVER · 404 NOT_FOUND · 409 VERSION_CONFLICT / DOC_TYPE_INACTIVE · 422 INVALID_STATE

## §2.3 Common
Auth JWT · tenant จาก token · ทุก write มี `version` (optimistic lock) · เวลา ISO 8601

## §2.4 API → Logic Trace
| API | FN |
|---|---|
| 01,02,10 | FN-10 |
| 03 | FN-01, FN-02, FN-03 |
| 04 | FN-01, FN-02 |
| 05,06 | FN-04 |
| 07 | FN-05 (+FN-08, FN-09) / FN-06 |
| 08 | FN-07 (+FN-09) |
| 09 | FN-08 |
| 11 | FN-02 |

## §2.X Cross-Module Contract
DOA resolve (F-DLG-001) · ENG-DOC-NUM/STORE (F-DOCCFG) · ENG-NOTIFY (F-NOTIFY) · Employee (F-EMP-001) — อ่านอย่างเดียว
