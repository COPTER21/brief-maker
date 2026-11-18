# 02_API — F-TMP-006
> base `/api/v1/sales-admin-evals-ovs` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/sales-admin-evals-ovs?q&status&month&recorder&page&size&sort` | รายการตามสิทธิ์ + count ต่อสถานะ (tabs) | FN-08 |
| API-02 | GET `/sales-admin-evals-ovs/{id}` | รายละเอียด + scores + audit | FN-08 |
| API-03 | POST `/sales-admin-evals-ovs` | สร้างร่าง + ออกเลข | FN-01, FN-02 |
| API-04 | PUT `/sales-admin-evals-ovs/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01 |
| API-05 | POST `/sales-admin-evals-ovs/{id}/record` | บันทึกผล (ครบ 10 ข้อ) | FN-03, FN-04, FN-06 |
| API-06 | POST `/sales-admin-evals-ovs/{id}/cancel` `{reason}` | ยกเลิก | FN-05, FN-06 |
| API-07 | GET `/sales-admin-evals-ovs/{id}/pdf` | PDF FM-SAL-22 (ภาษาอังกฤษ) | FN-07 |
| API-08 | GET `/sales-admin-evals-ovs/export.csv` | CSV ตามตัวกรอง | FN-08 |
| API-09 | POST/DELETE `/sales-admin-evals-ovs/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ period_month, customer_id, contact_person, scores:{ q1..q10: 1–5 }, comment, attachment_ids[] }` — scores บางส่วนได้ (ร่าง) · ค่าไม่อยู่ใน 1–5 → 422 `SCORE_OUT_OF_RANGE` · ไม่มี period_month/customer_id/contact_person → 422 (VR-01..03) · ไม่มี field วันที่ (DEC-12 — วันที่บันทึก = `created_at`)
- API-05: 409 `NOT_DRAFT` · 422 `SCORES_INCOMPLETE {missing:[q_key]}` (BR-02) · 403 `NOT_OWNER`
- API-06: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/role-mgr-sales) · 409 `ALREADY_CANCELLED` · 422 `REASON_REQUIRED`
- API-03: 409 `DOC_TYPE_INACTIVE` (F-DOCCFG ปิดใช้ SEA)
- ทุก GET ใบที่ไม่มีสิทธิ์เห็น → 404 `NOT_FOUND`
- 409 `STALE_VERSION` เมื่อ If-Match ไม่ตรง
- response มี field DOA มาตรฐาน `approver_role` · `approved_by` · `approval_chain` (ว่าง/[] — DEC-03 ไม่มีการอนุมัติ · `TODO: DOA engine` เติมเมื่อ DOA กลางมี entry)
- `contact_person` = ข้อมูลส่วนบุคคล → ส่งเฉพาะผู้มีสิทธิ์เห็นใบ · ไม่ log ลง access log

## §2.3 Events (ENG-NOTIFY · NTF_BRIEF_F-TMP-006)
- `sea_low_score_recorded` — API-05 สำเร็จและมีข้อ ≤ เกณฑ์ (ค่าเริ่ม 2) → role-mgr-sales
- `sea_cancelled` — API-06 สำเร็จโดยผู้ที่ไม่ใช่เจ้าของ → เจ้าของ
- ไม่มี doa_* (DEC-03) · ไม่ยิง event ไประบบอื่น (DEC-02)
