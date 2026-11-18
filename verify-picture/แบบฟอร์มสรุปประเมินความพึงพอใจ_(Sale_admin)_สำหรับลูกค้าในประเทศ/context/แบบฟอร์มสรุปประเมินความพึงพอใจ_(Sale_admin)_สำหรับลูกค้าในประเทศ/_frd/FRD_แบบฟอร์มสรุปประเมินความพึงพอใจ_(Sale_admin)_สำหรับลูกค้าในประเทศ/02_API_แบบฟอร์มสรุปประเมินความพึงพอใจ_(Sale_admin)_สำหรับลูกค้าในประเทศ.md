# 02_API — F-TMP-005
> base `/api/v1/sds-summaries` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/sds-summaries?q&status&period&mine_to_act&page&page_size&sort` | รายการตามสิทธิ์ | FN-09 |
| API-02 | GET `/sds-summaries/{id}` | รายละเอียด + columns + chain + audit | FN-09 |
| API-03 | POST `/sds-summaries` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-03 |
| API-04 | PUT `/sds-summaries/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/sds-summaries/eligible-surveys?period` | ลูกค้าที่มีแบบประเมิน SDA บันทึกผลแล้วในเดือน (ใบล่าสุด + count) | FN-02 |
| API-06 | POST `/sds-summaries/{id}/submit` `{assignees[]}` (+ GET `/doa-preview`) | resolve + ส่ง · snapshot chain | FN-04 |
| API-07 | POST `/sds-summaries/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-05, FN-06 |
| API-08 | POST `/sds-summaries/{id}/cancel` `{reason}` | ยกเลิก | FN-06 |
| API-09 | GET `/sds-summaries/{id}/pdf` | PDF FM-SAL-21 (2 หน้า) | FN-07 |
| API-10 | GET `/sds-summaries/export.csv` | CSV ตามตัวกรอง (1 แถว = 1 ลูกค้า) | FN-09 |
| API-11 | POST/DELETE `/sds-summaries/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ period_month:'YYYY-MM', columns:[{customer_id, sda_id}], conclusion, suggestion, attachment_ids[] }` · server ดึง customer_name / sda_doc_no / survey_date / score_q1..q5 จาก SDA เอง (ไม่รับคะแนนจาก FE) → 422 ตาม VR-01..05
- API-05: อ่าน F-TMP-004 SDA สถานะ recorded ตาม period_month · ต่อ customer คืนใบล่าสุด + จำนวนใบ · ป้ายหัวข้อ/ระดับจาก SalesConfig.sda_topics / sda_scale (config)
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04) · 422 `SOURCE_SURVEY_CANCELLED` (มีคอลัมน์ที่ SDA ถูกยกเลิก) · 422 `CONCLUSION_REQUIRED`
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject) · approve ขั้นสุดท้าย + มีช่องระดับต่ำ → event `sds_low_score_approved`
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/ผู้จัดการฝ่ายขาย) · 409 `NOT_CANCELLABLE` (approved/cancelled) · ยกเลิกจาก pending → event `sds_cancelled`
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- ทุก write: 409 `STALE_VERSION` · 409 `DOC_TYPE_INACTIVE` (F-DOCCFG ปิดใช้)

## §2.3 ฟิลด์อนุมัติ (DOA contract — ใน response API-02 และตาราง header)
| field | ความหมาย |
|---|---|
| approval_required | bool จาก DOA entry |
| doa_ref | doa_entry_ref ที่ resolve ตอนส่ง |
| approval_status | = status |
| approval_chain | jsonb snapshot ขั้น/ผู้พิจารณา/ผล ตอนส่ง (append-only) |
| approver_role | role ขั้นปัจจุบัน (ค่าเริ่ม role-ceo) |
| approved_by · approved_at | ผู้รับทราบและอนุมัติขั้นสุดท้าย |
> `TODO: DOA engine` — FE/BE ใช้ hook `DOA-ENGINE-HOOK` (resolve จาก DOA กลาง) · ห้าม hardcode จำนวนขั้น/role

## §2.4 Events (ประกาศ · ENG-NOTIFY)
| event | เมื่อ | หมายเหตุ |
|---|---|---|
| sds_cancelled | pending → cancelled | ผู้อนุมัติขั้นปัจจุบัน (NTF_BRIEF) |
| sds_low_score_approved | → approved และมีช่องระดับ ≤ 2 (ตาม SalesConfig.sda_scale) | owner + role-mgr-sales |
| sds.approved | → approved | **ประกาศเท่านั้น ไม่ยิงรอบนี้** (DEC-02) |
