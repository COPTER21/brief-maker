# 02_API — F-TMP-002

## §2.1 API Overview
| API | Method · Path | ใช้ | FN |
|---|---|---|---|
| API-01 | GET `/exit-interviews?q&status&sep_type&division&page&size&sort` | รายการตามสิทธิ์ (ความลับ) | FN-10 |
| API-02 | GET `/exit-interviews/{id}` | รายละเอียด + reasons + improvements + audit | FN-10 |
| API-03 | GET `/exit-interviews/prefill?employee_id` | ข้อมูลบุคลากรจาก Employee + ค่าคำนวณ | FN-01 |
| API-04 | POST `/exit-interviews` | สร้างร่าง + ออกเลข EXI | FN-02, FN-03 |
| API-05 | PUT `/exit-interviews/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-02 |
| API-06 | GET `/exit-interviews/{id}/doa-preview` | resolve ขั้นค่าเริ่ม (ค่าเริ่ม 0) | FN-04 |
| API-07 | POST `/exit-interviews/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-04 |
| API-08 | POST `/exit-interviews/{id}/decide` `{decision: acknowledge\|return, note}` | สำรอง — ไม่ใช้รอบนี้ (DEC-03 · OQ-02) | FN-05 |
| API-09 | POST `/exit-interviews/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-10 | GET `/exit-interviews/{id}/pdf` | PDF FM-HRM-06 | FN-08 |
| API-11 | GET `/exit-interviews/export.csv` | CSV ตามตัวกรองและสิทธิ์ | FN-10 |
| API-12 | POST/DELETE `/exit-interviews/{id}/attachments` | ไฟล์ (Document Center · ref_type=EXI) | — |

## §2.2 Contract สำคัญ
- API-04/05 body: `{employee_id, sep_type, resign_date?, contract_end_reason?, contract_end_other?, age_years, service_years, service_months, calc_manual, probation_status, education_degree, education_major, employment_type, ratings{q01..q26: 1..5}, exit_reasons[{reason, rank}], exit_reasons_other_text?, improvements[{item, reason}], other_comments}`
- 422 `VALIDATION` {field, code} ตาม 05 §5.4 · 409 `DOC_TYPE_INACTIVE` · 409 `STALE_VERSION` · 404 ใบไม่มีสิทธิ์ (ไม่บอกว่ามีอยู่)
- API-07: 0 ขั้น → status=submitted ทันที + emit **exi_submitted** · มีขั้น → pending
- API-09: emit **exi_cancelled** เมื่อยกเลิกจาก submitted/pending

## §2.3 Common
- Header `X-Tenant` · optimistic lock `version` · วันที่ ISO · ข้อความ error ภาษาไทยตาม 06 §6.10

## §2.4 API → Logic Trace
| API | FN |
|---|---|
| 01, 02, 11 | FN-10 |
| 03 | FN-01 |
| 04 | FN-02, FN-03 |
| 05 | FN-02 |
| 06, 07 | FN-04 (+FN-09) |
| 08 | FN-05 / FN-06 |
| 09 | FN-07 (+FN-09) |
| 10 | FN-08 |

## §2.X Cross-Module Contract
| Module | ใช้ | ทิศ |
|---|---|---|
| F-EMP-001 | GET employee profile (read) | in |
| F-ORG-001 | OrgUnit / Position name (read) | in |
| F-DOCCFG | status ของ doc_type EXI · ENG-DOC-NUM.next | in |
| Document Center | attachments ref_type=EXI | out |
| ENG-NOTIFY | exi_submitted · exi_cancelled | out |
| DOA กลาง | /doa/resolve?feature_id=F-TMP-002 (ค่าเริ่ม 0 ขั้น) | in |
