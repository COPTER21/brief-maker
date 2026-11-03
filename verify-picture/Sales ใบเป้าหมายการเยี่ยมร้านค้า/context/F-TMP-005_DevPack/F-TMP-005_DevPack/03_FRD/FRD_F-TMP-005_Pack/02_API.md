# 02_API — F-TMP-005

## §2.1 API Overview
| API | Method · Path | ใช้ | FN |
|---|---|---|---|
| API-01 | GET `/visit-targets?q&status&territory&page&size&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/visit-targets/{id}` | รายละเอียด + days + stores + audit | FN-10 |
| API-03 | GET `/visit-targets/prefill?territory_id&sales_cycle` | ผู้รับผิดชอบเขต/ตำแหน่ง · TO ค่าเริ่ม · ร้านในเขต · ใบใช้งานเดิมของเขต+รอบ | FN-01 |
| API-04 | POST `/visit-targets` | สร้างร่าง + ออกเลข SVT | FN-02, FN-03 |
| API-05 | PUT `/visit-targets/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-02 |
| API-06 | GET `/visit-targets/{id}/doa-preview` | resolve ขั้นค่าเริ่ม (approver_role ต่อขั้น) | FN-04 |
| API-07 | POST `/visit-targets/{id}/submit` `{assignees[]}` | ส่งอนุมัติ · snapshot approval_chain | FN-04 |
| API-08 | POST `/visit-targets/{id}/decide` `{decision: approve\|reject, note}` | อนุมัติ/ไม่อนุมัติ ขั้นปัจจุบัน | FN-05, FN-06 |
| API-09 | POST `/visit-targets/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-10 | GET `/visit-targets/{id}/pdf` | PDF FM-SAL-09 (A4 แนวนอน) | FN-08 |
| API-11 | GET `/visit-targets/export.csv` | CSV ตามตัวกรองและสิทธิ์ (1 แถวต่อวันทำงาน) | FN-10 |
| API-12 | POST/DELETE `/visit-targets/{id}/attachments` | ไฟล์ (Document Center · ref_type=SVT) | — |

## §2.2 Contract สำคัญ
- API-04/05 body: `{territory_id, sales_cycle:"YYYY-MM", to_recipient, cc_recipients[], days[{visit_date, market_start, market_end, lodging_province?, stores[customerId]}]}` · `customer_count` และ total_customer_count server คำนวณ (ไม่รับจาก client) · territory_owner/ตำแหน่ง server snapshot
- 422 `VALIDATION` {field, code} ตาม 05 §5.4 · 409 `DOC_TYPE_INACTIVE` · 409 `STALE_VERSION` · 404 ใบไม่มีสิทธิ์ (ไม่บอกว่ามีอยู่)
- API-07: status → pending · DOA engine ยิง doa_pending
- API-08 approve ขั้นสุดท้าย: status → approved · ใบเดิมเขต+รอบเดียวกัน → superseded + emit **svt_superseded** · emit **svt_plan_published** (TO + CC) · reject: status → draft (BR-DOA-03) · 403 NOT_CURRENT_APPROVER
- API-09: emit **svt_cancelled** เมื่อยกเลิกจาก pending

## §2.3 Common
- Header `X-Tenant` · optimistic lock `version` · วันที่ ISO · ข้อความ error ภาษาไทยตาม 06 §6.10

## §2.4 API → Logic Trace
| API | FN |
|---|---|
| 01, 02, 11 | FN-10 |
| 03 | FN-01 |
| 04 | FN-02, FN-03 |
| 05 | FN-02 |
| 06, 07 | FN-04 |
| 08 | FN-05 / FN-06 (+FN-09) |
| 09 | FN-07 (+FN-09) |
| 10 | FN-08 |

## §2.X Cross-Module Contract
| Module | ใช้ | ทิศ |
|---|---|---|
| Sales Territory ⟂ | GET territory (code, name, owner_employee_id) read | in |
| Customer | GET customers?territory_id (customerId, name) read | in |
| Employee / Position | ชื่อ · ตำแหน่ง · ผู้บังคับบัญชาตรง (resolve role-line-manager) | in |
| F-DOCCFG | status ของ doc_type SVT · ENG-DOC-NUM.next | in |
| DOA กลาง | /doa/resolve?feature_id=F-TMP-005 (ค่าเริ่ม 2 ขั้น) | in |
| Document Center | attachments ref_type=SVT | out |
| ENG-NOTIFY | svt_cancelled · svt_plan_published · svt_superseded | out |
