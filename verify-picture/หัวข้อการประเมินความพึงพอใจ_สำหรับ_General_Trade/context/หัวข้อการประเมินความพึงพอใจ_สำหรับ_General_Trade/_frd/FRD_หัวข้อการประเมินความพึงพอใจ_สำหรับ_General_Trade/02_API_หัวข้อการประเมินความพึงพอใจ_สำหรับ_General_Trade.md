# 02_API — F-TMP-002
> base `/api/v1/csat-summaries` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/csat-summaries?q&status&period&mine_to_act&page&page_size&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/csat-summaries/{id}` | รายละเอียด + lines + customers + chain + audit | FN-10 |
| API-03 | POST `/csat-summaries` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-03 |
| API-04 | PUT `/csat-summaries/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/csat-summaries/eligible-customers?period` | ลูกค้าในหน่วยงานที่สั่งซื้อถึงเกณฑ์ + order_count | FN-04 |
| API-06 | POST `/csat-summaries/{id}/submit` `{assignees[]}` (+ GET `/doa-preview`) | resolve + ส่ง · snapshot chain | FN-05 |
| API-07 | POST `/csat-summaries/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-06, FN-07 |
| API-08 | POST `/csat-summaries/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-09 | GET `/csat-summaries/{id}/pdf` | PDF FM-SAL-11 (2 หน้า) | FN-08 |
| API-10 | GET `/csat-summaries/export.csv` | CSV ตามตัวกรอง | FN-10 |
| API-11 | POST/DELETE `/csat-summaries/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ period_month:'YYYY-MM', lines:[{section_key, topic_id, c5, c4, c3, c2, c1}], customers:[{customer_id}], attachment_ids[] }` · ค่า c* เป็นจำนวนเต็ม ≥ 0 → 422 ตาม VR-01..04 · server ไม่รับ topic_text/total/pct จาก FE (คำนวณเอง)
- API-05: อ่าน Customer + COUNT Sale Order ในเดือน · เกณฑ์จาก SalesConfig.csat_min_orders_per_month (config)
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject) · approve ขั้นสุดท้าย + % โดยรวมต่ำกว่าช่วงกลาง → event `csm_low_csat`
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/Sales admin) · 409 `NOT_CANCELLABLE` (approved/cancelled) · ยกเลิกจาก pending → event `csm_cancelled`
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- ทุก write: 409 `STALE_VERSION` · 409 `DOC_TYPE_INACTIVE` (F-DOCCFG ปิดใช้)

## §2.3 Events (ประกาศ · ENG-NOTIFY)
| event | เมื่อ | หมายเหตุ |
|---|---|---|
| csm_cancelled | pending → cancelled | ผู้อนุมัติขั้นปัจจุบัน (NTF_BRIEF) |
| csm_low_csat | → approved และ overall_pct < SalesConfig.csat_bands[mid].min | owner + role-mgr-sales |
| csm.approved | → approved | **ประกาศเท่านั้น ไม่ยิงรอบนี้** (DEC-02) |
