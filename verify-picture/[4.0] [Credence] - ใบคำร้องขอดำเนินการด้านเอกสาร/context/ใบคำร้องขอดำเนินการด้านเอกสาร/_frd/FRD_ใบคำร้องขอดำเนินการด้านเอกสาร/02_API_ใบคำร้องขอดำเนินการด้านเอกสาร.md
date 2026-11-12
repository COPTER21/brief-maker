# 02_API — F-TMP-007 (HTTP layer · logic อยู่ 03)

| API | Method · Path | ใคร | เรียก FN | Error |
|---|---|---|---|---|
| API-01 | GET /dars?tab&status&purpose&q&page&size | ทุก role | FN-10 listVisible | — |
| API-02 | GET /dars/{id} | canSee | FN-10 | 404 NOT_FOUND (ไม่มีสิทธิ์เห็น = ไม่พบ) |
| API-03 | POST /dars | ผู้จัดทำ | FN-01 validate → FN-02 issueNumber | 422 VALIDATION · 409 DOC_TYPE_INACTIVE |
| API-04 | PUT /dars/{id} | เจ้าของ · status=draft | FN-01 | 403 NOT_OWNER · 409 NOT_DRAFT · 409 STALE |
| API-05 | GET /doa/resolve?feature_id=F-TMP-007&employee_id= | ผู้จัดทำ | (DOA กลาง) | — |
| API-06 | POST /dars/{id}/submit `{assignees[]}` | เจ้าของ | FN-03 resolveAndSubmit | 422 ASSIGNEE_REQUIRED · 422 SELF_APPROVE · 409 STALE |
| API-07 | POST /dars/{id}/decide `{decision:approve|reject, note}` | ผู้พิจารณาขั้นปัจจุบัน | FN-04 decideStep / FN-05 returnToDraft | 403 NOT_CURRENT_APPROVER · 422 REASON_REQUIRED |
| API-08 | POST /dars/{id}/cancel `{reason}` | เจ้าของ / role-doc-controller · draft/pending | FN-06 cancelDar | 403 · 409 · 422 REASON_REQUIRED |
| API-09 | POST /dars/{id}/receive `{receiver_id}` | role-doc-controller · approved | FN-08 recordReceipt | 403 NOT_ADMIN · 409 NOT_APPROVED · 422 RECEIVER_REQUIRED |
| API-10 | GET /dars/{id}/pdf | canSee | FN-07 docPrintData + render | — |
| API-11 | GET /dars/export.csv | ตามสิทธิ์รายการ | FN-10 | — |
| API-12 | POST /dars/{id}/attachments | เจ้าของ · draft | Document Center (file_policy) | 413 · 415 |

ENG-NOTIFY event ที่ API ทำให้เกิด (ยิงจาก 03): dar_cancelled (API-08 จาก pending) · dar_distributed (API-07 อนุมัติขั้นสุดท้าย) · dar_received (API-09) · DOA engine ยิง doa_pending/doa_result เอง
Integration event `dar.approved` = ประกาศไว้ **ไม่ยิงรอบนี้** (DEC-02)
