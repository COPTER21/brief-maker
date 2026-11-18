# 02_API — F-TMP-009
> base `/api/ctr` · auth = session · ทุก response ใบที่ไม่มีสิทธิ์เห็น = 404 NOT_FOUND (ไม่บอกว่ามีใบ)

| API | Method · Path | ใช้ | FN | Error |
|---|---|---|---|---|
| API-01 | GET /api/ctr?q&status&type&unit&page&size&sort | รายการที่เห็นได้ + counts (mine_to_act · to_register) | FN-11 | — |
| API-02 | GET /api/ctr/{id} | รายละเอียด + approval_chain + audit | FN-11 | 404 NOT_FOUND |
| API-03 | POST /api/ctr | บันทึกครั้งแรก (ร่าง) → ออกเลข CTR | FN-01 FN-02 FN-03 | 422 VALIDATION · 409 DOC_TYPE_INACTIVE |
| API-04 | PUT /api/ctr/{id} | แก้ร่างของตน | FN-01 FN-02 | 403 NOT_OWNER · 409 NOT_DRAFT · 409 STALE |
| API-05 | POST /api/ctr/{id}/submit {assignees[]} | ส่งพิจารณา (resolve + freeze สาย) | FN-04 | 422 ASSIGNEE_REQUIRED · 422 SELF_APPROVAL · 409 NOT_DRAFT |
| API-06 | POST /api/ctr/{id}/approve {note?} | อนุมัติ/รับทราบ ขั้นปัจจุบัน | FN-05 FN-10 | 403 NOT_CURRENT_APPROVER · 409 STALE |
| API-07 | POST /api/ctr/{id}/reject {reason} | ไม่อนุมัติ/ส่งกลับแก้ไข → ร่าง | FN-06 | 403 NOT_CURRENT_APPROVER · 422 REASON_REQUIRED |
| API-08 | POST /api/ctr/{id}/cancel {reason} | ยกเลิก (ร่าง/รอพิจารณา) | FN-07 FN-10 | 403 · 409 INVALID_STATE · 422 REASON_REQUIRED |
| API-09 | POST /api/ctr/{id}/register | ลงทะเบียนควบคุม (ออกเลขทะเบียน) | FN-08 FN-10 | 403 NOT_CUSTODIAN · 409 INVALID_STATE |
| API-10 | POST /api/ctr/{id}/receive {received_date} | บันทึกรับต้นฉบับ/คู่ฉบับ | FN-08 FN-10 | 403 · 409 INVALID_STATE · 422 DATE_IN_FUTURE |
| API-11 | GET /api/ctr/{id}/pdf | PDF FM-AGM-01 Replica | FN-09 | 404 |
| API-12 | GET /api/ctr/export.csv?(ตัวกรองเดียวกับ API-01) | CSV ตามตัวกรอง | FN-11 | — |
| API-13 | POST /api/ctr/{id}/attachments | แนบไฟล์ (Document Center · ref_type='CTR') | — (Document Center) | 413 · 415 |

## §2.1 Events (ENG-NOTIFY — ประกาศใน NTF_BRIEF)
ctr_registered (API-09) · ctr_original_received (API-10) · ctr_cancelled (API-08 เมื่อเดิม pending) — doa_pending/doa_result/doa_escalate เป็นของ DOA engine
