# 02_API — F-TMP-005 (HTTP layer · logic อยู่ 03)

| API | Method · Path | ใคร | เรียก FN | Error |
|---|---|---|---|---|
| API-01 | GET /change-requests?tab&status&change_type&q&page&size | ทุก role | FN-09 listVisible | — |
| API-02 | GET /change-requests/{id} | canSee | FN-09 | 404 NOT_FOUND (ไม่มีสิทธิ์เห็น = ไม่พบ) |
| API-03 | POST /change-requests | ผู้ขอ | FN-01 validate → FN-02 issueNumber | 422 VALIDATION · 409 DOC_TYPE_INACTIVE |
| API-04 | PUT /change-requests/{id} | เจ้าของ · status=draft | FN-01 | 403 NOT_OWNER · 409 NOT_DRAFT · 409 STALE |
| API-05 | GET /doa/resolve?feature_id=F-TMP-005&employee_id= | ผู้ขอ | (DOA กลาง) | — |
| API-06 | POST /change-requests/{id}/submit `{assignees[]}` | เจ้าของ | FN-03 resolveAndSubmit | 422 ASSIGNEE_REQUIRED · 422 SELF_APPROVE · 409 STALE |
| API-07 | POST /change-requests/{id}/decide `{decision:approve|reject, note}` | ผู้พิจารณาขั้นปัจจุบัน | FN-04 decideStep / FN-05 returnToDraft | 403 NOT_CURRENT_APPROVER · 422 REASON_REQUIRED |
| API-08 | POST /change-requests/{id}/cancel `{reason}` | เจ้าของ / role-it-officer · draft/pending | FN-06 cancelRequest | 403 · 409 · 422 REASON_REQUIRED |
| API-09 | GET /change-requests/{id}/pdf | canSee | FN-07 docPrintData + render | — |
| API-10 | GET /change-requests/export.csv | ตามสิทธิ์รายการ | FN-09 | — |
| API-11 | POST /change-requests/{id}/attachments | เจ้าของ · draft | Document Center (file_policy) | 413 · 415 |

ENG-NOTIFY event ที่ API ทำให้เกิด (ยิงจาก 03): itcr_cancelled (API-08 จาก pending) · itcr_approved_for_it (API-07 อนุมัติขั้นสุดท้าย) · DOA engine ยิง doa_pending/doa_result เอง
Integration event `itcr.approved` = ประกาศไว้ **ไม่ยิงรอบนี้** (DEC-02)
