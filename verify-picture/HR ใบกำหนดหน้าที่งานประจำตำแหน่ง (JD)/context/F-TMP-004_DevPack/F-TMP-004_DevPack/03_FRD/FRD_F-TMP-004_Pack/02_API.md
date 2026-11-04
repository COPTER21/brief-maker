# 02_API — F-TMP-004

## §2.1 API Overview
| API | Method · Path | ใช้ | FN |
|---|---|---|---|
| API-01 | GET `/job-descriptions?q&status&division&page&size&sort` | รายการตามสิทธิ์ | FN-12 |
| API-02 | GET `/job-descriptions/{id}` | รายละเอียด + superiors + subordinates + audit | FN-12 |
| API-03 | GET `/job-descriptions/prefill?position_id` | ตำแหน่ง/แผนก/ฝ่าย/รายงานต่อ + ฉบับใช้งานเดิม | FN-01 |
| API-04 | POST `/job-descriptions` | สร้างร่าง + ออกเลข JD | FN-02, FN-03 |
| API-05 | PUT `/job-descriptions/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-02 |
| API-06 | GET `/job-descriptions/{id}/doa-preview` | resolve ขั้นค่าเริ่ม (approver_role ต่อขั้น) | FN-04 |
| API-07 | POST `/job-descriptions/{id}/submit` `{assignees[]}` | ส่งอนุมัติ · snapshot approval_chain | FN-04 |
| API-08 | POST `/job-descriptions/{id}/decide` `{decision: approve\|reject, note}` | อนุมัติ/ไม่อนุมัติ ขั้นปัจจุบัน | FN-05, FN-06 |
| API-09 | POST `/job-descriptions/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-10 | GET `/job-descriptions/{id}/pdf` | PDF FM-HRM-32 | FN-08 |
| API-11 | GET `/job-descriptions/export.csv` | CSV ตามตัวกรองและสิทธิ์ | FN-12 |
| API-12 | POST/DELETE `/job-descriptions/{id}/attachments` | ไฟล์ (Document Center · ref_type=JD) | — |
| API-13 | PUT `/job-descriptions/{id}/incumbent` `{employee_id}` | HR ระบุ/เปลี่ยนผู้ดำรงตำแหน่ง (approved) | FN-10 |
| API-14 | POST `/job-descriptions/{id}/acknowledge` | ผู้ดำรงตำแหน่งรับทราบ | FN-11 |

## §2.2 Contract สำคัญ
- API-04/05 body: `{position_id, position_name_en, reports_to, job_purpose, key_responsibilities, job_specification, kpi, other_qualifications, superiors[{position, headcount}], subordinates[{position, headcount}], acknowledged_by?}` · `subordinate_summary` server คำนวณ (ไม่รับจาก client)
- 422 `VALIDATION` {field, code} ตาม 05 §5.4 · 409 `DOC_TYPE_INACTIVE` · 409 `STALE_VERSION` · 404 ใบไม่มีสิทธิ์ (ไม่บอกว่ามีอยู่)
- API-07: status → pending · DOA engine ยิง doa_pending
- API-08 approve ขั้นสุดท้าย: status → approved · ฉบับเดิม → superseded + emit **jd_superseded** · emit **jd_ack_requested** ถ้ามี acknowledged_by · reject: status → draft (BR-DOA-03) · 403 NOT_CURRENT_APPROVER
- API-09: emit **jd_cancelled** เมื่อยกเลิกจาก pending
- API-13: emit **jd_ack_requested** · API-14: emit **jd_acknowledged** · 403 NOT_INCUMBENT

## §2.3 Common
- Header `X-Tenant` · optimistic lock `version` · วันที่ ISO · ข้อความ error ภาษาไทยตาม 06 §6.10

## §2.4 API → Logic Trace
| API | FN |
|---|---|
| 01, 02, 11 | FN-12 |
| 03 | FN-01 |
| 04 | FN-02, FN-03 |
| 05 | FN-02 |
| 06, 07 | FN-04 |
| 08 | FN-05 / FN-06 (+FN-09) |
| 09 | FN-07 (+FN-09) |
| 10 | FN-08 |
| 13 | FN-10 (+FN-09) |
| 14 | FN-11 (+FN-09) |

## §2.X Cross-Module Contract
| Module | ใช้ | ทิศ |
|---|---|---|
| Organization · Position & Tier | GET position (name_th, org_unit, reports_to) read | in |
| OrgUnit / Employee | แผนก · ฝ่าย · ผู้บังคับบัญชาตรง (resolve role-line-manager) | in |
| F-DOCCFG | status ของ doc_type JD · ENG-DOC-NUM.next | in |
| DOA กลาง | /doa/resolve?feature_id=F-TMP-004 (ค่าเริ่ม 1 ขั้น) | in |
| Document Center | attachments ref_type=JD | out |
| ENG-NOTIFY | jd_cancelled · jd_ack_requested · jd_acknowledged · jd_superseded | out |
