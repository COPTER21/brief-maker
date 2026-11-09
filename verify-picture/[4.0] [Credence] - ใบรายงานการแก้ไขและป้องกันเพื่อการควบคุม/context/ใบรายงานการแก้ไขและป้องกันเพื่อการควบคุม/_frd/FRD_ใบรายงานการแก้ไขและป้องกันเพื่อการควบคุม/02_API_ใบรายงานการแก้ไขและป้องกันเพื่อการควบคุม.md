# 02_API — F-TMP-008
| ID | Method · Path | ใช้ทำ | FN | Error |
|---|---|---|---|---|
| API-01 | GET /car?tab&status&dept&q&page&size | รายการตามสิทธิ์ | FN-14 | — |
| API-02 | GET /car/{id} | รายละเอียด | FN-14 | 404 NOT_FOUND |
| API-03 | POST /car | บันทึกร่างครั้งแรก (ออกเลข) | FN-01 → FN-02 → FN-03 | 400 VALIDATION · 409 DOC_TYPE_INACTIVE |
| API-04 | PUT /car/{id} | แก้ร่าง (ช่วงการจัดทำ) | FN-01 → FN-03 | 403 NOT_OWNER · 409 STALE |
| API-05 | POST /car/{id}/submit-review | ส่งตรวจสอบ (ผู้ตรวจสอบ + assignees DOA) | FN-04 → FN-13 (car_submitted_for_review) | 400 SUBMIT_INCOMPLETE · 403 NOT_OWNER |
| API-06 | PUT /car/{id}/review | บันทึกช่วงการตรวจสอบ + ข้อ 10 | FN-05 | 403 NOT_REVIEWER · 409 STALE |
| API-07 | POST /car/{id}/review-signs/{point} | ลงนามตรวจสอบ | FN-06 | 403 NOT_SIGNER · 403 SOD_SELF |
| API-08 | POST /car/{id}/return | ตีกลับเป็นร่าง (เหตุผล) | FN-07 → FN-13 (car_review_returned) | 403 NOT_REVIEWER |
| API-09 | POST /car/{id}/send-approval | ส่งอนุมัติ | FN-08 | 400 REVIEW_SIGNS_INCOMPLETE |
| API-10 | POST /car/{id}/decide {approve|reject, note} | อนุมัติ/ไม่อนุมัติขั้นปัจจุบัน | FN-09 / FN-10 | 403 NOT_CURRENT_APPROVER · 400 REASON_REQUIRED |
| API-11 | POST /car/{id}/cancel {reason} | ยกเลิก | FN-11 → FN-13 (car_cancelled) | 403 NOT_OWNER · 400 REASON_REQUIRED |
| API-12 | GET /car/{id}/pdf | PDF (template + data contract) | FN-12 | — |
| API-13 | POST /car/{id}/attachments | แนบไฟล์ (Document Center) | — | 413 · 415 |
| API-14 | GET /car/export.csv | ส่งออก CSV ตามตัวกรอง | FN-14 | — |
- DOA hook: GET /doa/resolve?feature_id=F-TMP-008 · callback ผล → FN-09/10 (`TODO: DOA engine`)
