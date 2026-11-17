# 02_API — F-TMP-008
> base `/api/v1/mt-csat-summaries` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/mt-csat-summaries?q&status&year&page&page_size&sort` | รายการตามสิทธิ์ | FN-09 |
| API-02 | GET `/mt-csat-summaries/{id}` | รายละเอียด + scores + recommendations + audit | FN-09 |
| API-03 | POST `/mt-csat-summaries` | สร้างร่าง + ออกเลข + snapshot config | FN-01, FN-02, FN-03 |
| API-04 | PUT `/mt-csat-summaries/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | POST `/mt-csat-summaries/{id}/finalize` | ยืนยันสรุป (draft → final) | FN-04 |
| API-06 | POST `/mt-csat-summaries/{id}/cancel` `{reason}` | ยกเลิก | FN-05 |
| API-07 | GET `/mt-csat-summaries/{id}/pdf` | PDF FM-SAL-07 (2 หน้า) | FN-07 |
| API-08 | GET `/mt-csat-summaries/export.csv` | CSV ตามตัวกรอง | FN-09 |
| API-09 | POST/DELETE `/mt-csat-summaries/{id}/attachments` | ไฟล์ (Document Center) | FN-06 |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ round_no:int, assessment_date:'YYYY-MM-DD', summary_date:'YYYY-MM-DD', scores:[{criterion_id, channel_id, score|null}], notes:{pass_note, below_note, far_note}, recommendations:[text], attachment_ids[] }` · score เป็นจำนวนเต็ม 1..max_score ของหัวข้อ หรือ null → 422 ตาม VR-01..03 · server ไม่รับ total/pct/status/รายชื่อกลุ่มจาก FE (คำนวณเอง FN-02)
- API-03/04 response: `warnings:[{code:'DUP_ROUND'}]` เมื่อครั้งที่ซ้ำในปีเดียวกัน (ไม่บล็อก · DEC-20)
- API-05: 403 `NOT_OWNER` · 409 `NOT_DRAFT` · 422 `INCOMPLETE_CHANNEL` (ช่องทางกรอกไม่ครบ) · 422 `NO_CHANNEL` · 422 `RECOMMENDATION_REQUIRED` · สำเร็จ + มีช่องทางสถานะ far → event `mts_low_channel`
- API-06: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/Sales admin) · 409 `NOT_CANCELLABLE` (cancelled แล้ว) · 422 `REASON_REQUIRED` · admin ยกเลิกใบ final ของคนอื่น → event `mts_cancelled`
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- ทุก write: 409 `STALE_VERSION` · 409 `DOC_TYPE_INACTIVE` (F-DOCCFG ปิดใช้)

## §2.3 Field DOA (มาตรฐานกลาง — เอกสารนี้ไม่มีขั้นอนุมัติ · DEC-03)
| field | ค่า | หมายเหตุ |
|---|---|---|
| approval_required | `false` | ตั้งตอนสร้าง |
| approver_role | `null` | TODO: DOA engine — ถ้าลูกค้าเพิ่มผู้รับรอง (OQ-03) ให้ resolve จาก DOA กลาง ห้าม hardcode role |
| approved_by | `null` | TODO: DOA engine |
| approval_chain | `null` | TODO: DOA engine (jsonb snapshot ตอนส่ง · append-only เมื่อเปิดใช้) |
| doa_ref | `null` | doa_entry_ref เมื่อเปิดใช้ |
คืนใน API-02 ทุกครั้ง (คีย์คงที่ เพื่อให้หน้าจอ/รายงานกลางอ่านได้เหมือนเอกสารอื่น)

## §2.4 Events (ประกาศ · ENG-NOTIFY)
| event | เมื่อ | หมายเหตุ |
|---|---|---|
| mts_low_channel | draft → final และมีช่องทาง % ต่ำกว่าเกณฑ์ต่ำใน config | role-mgr-bu + Sales admin (NTF_BRIEF) |
| mts_cancelled | final → cancelled โดย Sales admin (ไม่ใช่เจ้าของ) | owner |
| mts.finalized | → final | **ประกาศเท่านั้น ไม่ยิงรอบนี้** (DEC-02) |
