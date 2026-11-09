# 02_API — F-TMP-004 (HTTP layer · logic อยู่ 03)

| API | Method · Path | ใคร | เรียก FN | Error |
|---|---|---|---|---|
| API-01 | GET /repair-requests?tab&status&device_type&q&page&size | ทุก role | FN-13 listVisible | — |
| API-02 | GET /repair-requests/{id} | canSee | FN-13 | 404 NOT_FOUND (ไม่มีสิทธิ์เห็น = ไม่พบ) |
| API-03 | POST /repair-requests | ผู้แจ้งซ่อม | FN-01 validate → FN-02 issueNumber | 422 VALIDATION · 409 DOC_TYPE_INACTIVE |
| API-04 | PUT /repair-requests/{id} | เจ้าของ · status=draft | FN-01 | 403 NOT_OWNER · 409 NOT_DRAFT · 409 STALE |
| API-05 | POST /repair-requests/{id}/report | เจ้าของ · draft | FN-03 report | 409 NOT_DRAFT · 409 STALE |
| API-06 | POST /repair-requests/{id}/receive | role-it-officer · reported | FN-04 receive | 403 NOT_IT_OFFICER · 409 NOT_REPORTED |
| API-07 | PUT /repair-requests/{id}/inspection `{repair_date, check_result, claim_*}` | role-it-officer · inspecting | FN-05 saveInspection | 422 VALIDATION · 409 NOT_INSPECTING |
| API-08 | GET /doa/resolve?feature_id=F-TMP-004&employee_id= | role-it-officer | (DOA กลาง) | — |
| API-09 | POST /repair-requests/{id}/submit `{assignees[]}` | role-it-officer · inspecting | FN-06 resolveAndSubmit | 422 ASSIGNEE_REQUIRED · 422 SELF_APPROVE · 422 INSPECTION_INCOMPLETE · 409 STALE |
| API-10 | POST /repair-requests/{id}/decide `{decision:approve|reject, note}` | ผู้พิจารณาขั้นปัจจุบัน | FN-07 decideStep / FN-08 returnToInspecting | 403 NOT_CURRENT_APPROVER · 422 REASON_REQUIRED |
| API-11 | POST /repair-requests/{id}/repair `{repair_result, repair_note}` | role-it-officer · approved | FN-09 recordRepair | 403 NOT_IT_OFFICER · 409 NOT_APPROVED · 422 NOTE_REQUIRED |
| API-12 | POST /repair-requests/{id}/acknowledge | เจ้าของ · repaired | FN-10 acknowledge | 403 NOT_OWNER · 409 NOT_REPAIRED |
| API-13 | POST /repair-requests/{id}/cancel `{reason}` | เจ้าของ / role-it-officer · draft/reported/inspecting/pending | FN-11 cancelRequest | 403 · 409 · 422 REASON_REQUIRED |
| API-14 | GET /repair-requests/{id}/pdf · GET /repair-requests/export.csv | canSee / ตามสิทธิ์รายการ | FN-12 docPrintData + render · FN-13 | — |
| API-15 | POST /repair-requests/{id}/attachments | เจ้าของ · draft | Document Center (file_policy) | 413 · 415 |

ENG-NOTIFY event ที่ API ทำให้เกิด (ยิงจาก 03): crr_reported (API-05) · crr_received (API-06) · crr_cancelled (API-13 จาก pending) · crr_repaired (API-11) · DOA engine ยิง doa_pending/doa_result เอง
Integration event `crr.closed` = ประกาศไว้ **ไม่ยิงรอบนี้** (DEC-02)
