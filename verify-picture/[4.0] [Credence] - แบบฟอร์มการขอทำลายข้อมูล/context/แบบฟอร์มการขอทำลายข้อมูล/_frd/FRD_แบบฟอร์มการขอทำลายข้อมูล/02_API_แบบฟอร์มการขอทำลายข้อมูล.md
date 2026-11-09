# 02_API — F-TMP-003 (HTTP layer · logic อยู่ 03)

| API | Method · Path | ใคร | เรียก FN | Error |
|---|---|---|---|---|
| API-01 | GET /data-destruction-requests?tab&status&data_type&q&page&size | ทุก role | FN-10 listVisible | — |
| API-02 | GET /data-destruction-requests/{id} | canSee | FN-10 | 404 NOT_FOUND (ไม่มีสิทธิ์เห็น = ไม่พบ) |
| API-03 | POST /data-destruction-requests | ผู้ร้องขอ | FN-01 validate → FN-02 issueNumber | 422 VALIDATION · 409 DOC_TYPE_INACTIVE |
| API-04 | PUT /data-destruction-requests/{id} | เจ้าของ · status=draft | FN-01 | 403 NOT_OWNER · 409 NOT_DRAFT · 409 STALE |
| API-05 | GET /doa/resolve?feature_id=F-TMP-003&employee_id= | ผู้ร้องขอ | (DOA กลาง) | — |
| API-06 | POST /data-destruction-requests/{id}/submit `{assignees[]}` | เจ้าของ | FN-03 resolveAndSubmit | 422 ASSIGNEE_REQUIRED · 422 SELF_APPROVE · 409 STALE |
| API-07 | POST /data-destruction-requests/{id}/decide `{decision:approve|reject, note}` | ผู้พิจารณาขั้นปัจจุบัน | FN-04 decideStep / FN-05 returnToDraft | 403 NOT_CURRENT_APPROVER · 422 REASON_REQUIRED |
| API-08 | POST /data-destruction-requests/{id}/destroyed `{note}` | role-it-officer · status=approved | FN-07 markDestroyed | 403 NOT_IT_OFFICER · 409 NOT_APPROVED |
| API-09 | POST /data-destruction-requests/{id}/cancel `{reason}` | เจ้าของ / role-it-officer · draft/pending | FN-06 cancelRequest | 403 · 409 · 422 REASON_REQUIRED |
| API-10 | GET /data-destruction-requests/{id}/pdf | canSee | FN-08 docPrintData + render | — |
| API-11 | GET /data-destruction-requests/export.csv | ตามสิทธิ์รายการ | FN-10 | — |
| API-12 | POST /data-destruction-requests/{id}/attachments | เจ้าของ · draft | Document Center (file_policy) | 413 · 415 |

ENG-NOTIFY event ที่ API ทำให้เกิด (ยิงจาก 03): drits_cancelled (API-09 จาก pending) · drits_ready_for_it (API-07 อนุมัติขั้นสุดท้าย) · drits_destroyed (API-08) · DOA engine ยิง doa_pending/doa_result เอง
Integration event `drits.destroyed` = ประกาศไว้ **ไม่ยิงรอบนี้** (DEC-02)
