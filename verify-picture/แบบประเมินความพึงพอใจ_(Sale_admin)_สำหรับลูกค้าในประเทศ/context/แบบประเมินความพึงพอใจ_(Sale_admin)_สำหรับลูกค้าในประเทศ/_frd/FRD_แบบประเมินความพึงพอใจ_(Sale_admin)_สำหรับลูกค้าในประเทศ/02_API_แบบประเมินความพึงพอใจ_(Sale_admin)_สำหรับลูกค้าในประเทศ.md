# 02_API — F-TMP-004
> base `/api/v1/sale-admin-evals-dom` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/sale-admin-evals-dom?q&status&month&recorder&page&size&sort` | รายการตามสิทธิ์ + count ต่อสถานะ (tabs) | FN-08 |
| API-02 | GET `/sale-admin-evals-dom/{id}` | รายละเอียด + scores + audit | FN-08 |
| API-03 | POST `/sale-admin-evals-dom` | สร้างร่าง + ออกเลข | FN-01, FN-02 |
| API-04 | PUT `/sale-admin-evals-dom/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01 |
| API-05 | POST `/sale-admin-evals-dom/{id}/record` | บันทึกผล (ครบ 5 ข้อ) | FN-03, FN-04, FN-06 |
| API-06 | POST `/sale-admin-evals-dom/{id}/cancel` `{reason}` | ยกเลิก | FN-05, FN-06 |
| API-07 | GET `/sale-admin-evals-dom/{id}/pdf` | PDF FM-SAL-20 | FN-07 |
| API-08 | GET `/sale-admin-evals-dom/export.csv` | CSV ตามตัวกรอง | FN-08 |
| API-09 | POST/DELETE `/sale-admin-evals-dom/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ customer_id, survey_date, period_month, scores:{ q1..q5: 1–5 }, comment, attachment_ids[] }` — scores บางส่วนได้ (ร่าง) · ค่าไม่อยู่ใน 1–5 → 422 `SCORE_OUT_OF_RANGE` · ไม่มี customer_id/survey_date/period_month → 422 (VR-01..03)
- API-05: 409 `NOT_DRAFT` · 422 `SCORES_INCOMPLETE {missing:[q_key]}` (BR-02) · 403 `NOT_OWNER`
- API-06: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/role-mgr-sales) · 409 `ALREADY_CANCELLED` · 422 `REASON_REQUIRED`
- API-03: 409 `DOC_TYPE_INACTIVE` (F-DOCCFG ปิดใช้ SDA)
- ทุก GET ใบที่ไม่มีสิทธิ์เห็น → 404 `NOT_FOUND`
- 409 `STALE_VERSION` เมื่อ If-Match ไม่ตรง
- response มี `approver_role` · `approved_by` · `approval_chain` (ว่าง — DEC-03 · TODO: DOA engine)

## §2.3 Events (ENG-NOTIFY · NTF_BRIEF_F-TMP-004)
- `sda_low_score_recorded` — API-05 สำเร็จและมีข้อ ≤ เกณฑ์ (ค่าเริ่ม 2 = น้อย/ควรปรับปรุง) → role-mgr-sales
- `sda_cancelled` — API-06 สำเร็จโดยผู้ที่ไม่ใช่เจ้าของ → เจ้าของ
- ไม่มี doa_* (ไม่มี DOA — DEC-03) · ไม่ยิง event ไประบบอื่น (DEC-02)
