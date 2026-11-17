# 02_API — F-TMP-001
> base `/api/v1/fire-ext-cards` · tenant จาก token (RLS) · ทุก write มี `If-Match: version` + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/fire-ext-cards?q&status&last_result&zone&page&size&sort` | รายการตามสิทธิ์ | FN-08 |
| API-02 | GET `/fire-ext-cards/{id}` | รายละเอียด + checks + audit | FN-08 |
| API-03 | POST `/fire-ext-cards` | สร้างใบ + ออกเลข (+ แถวแรก) | FN-01, FN-02, FN-03, FN-07 |
| API-04 | POST `/fire-ext-cards/{id}/checks` | บันทึกผลตรวจ | FN-02, FN-04, FN-07 |
| API-05 | PUT `/fire-ext-cards/{id}/checks/{check_id}` | แก้แถว (ผู้บันทึก · วันเดียวกัน) | FN-02, FN-05, FN-07 |
| API-06 | POST `/fire-ext-cards/{id}/cancel` `{reason}` | ยกเลิกใบ | FN-06, FN-07 |
| API-07 | GET `/fire-ext-cards/{id}/pdf` | PDF FM-WHS-03 | FN-09 |
| API-08 | GET `/fire-ext-cards/export.csv` | CSV ตามตัวกรอง | FN-08 |
| API-09 | POST/DELETE `/fire-ext-cards/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03 body: `{ location_id, first_check?: { check_date, gauge, seal_pin, hose, body }, attachment_ids[] }` → 422 `LOCATION_REQUIRED` · 409 `LOCATION_HAS_ACTIVE_CARD` · 409 `DOC_TYPE_INACTIVE`
- API-04/05 body: `{ check_date, gauge, seal_pin, hose, body }` (enum normal|abnormal) → 422 `MARKS_INCOMPLETE` · 422 `DATE_IN_FUTURE` · 409 `DATE_DUPLICATE` · 409 `CARD_CANCELLED`
- API-05: 403 `NOT_RECORDER` · 403 `EDIT_WINDOW_CLOSED`
- API-06: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/role-mgr-wh) · 422 `REASON_REQUIRED` · 409 `NOT_CANCELLABLE`
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND`

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 Events / Cross-module (ENG-NOTIFY · ประกาศใน NTF_BRIEF)
- `fec_abnormal_found` → role-mgr-wh (บังคับ · in-app+email) — ยิงจาก FN-07 เมื่อแถวที่บันทึก/แก้มี x
- `fec_cancelled` → role-mgr-wh (in-app · ปิดได้) — ยิงจาก FN-07 เมื่อ active→cancelled
- Asset/Maintenance (งานซ่อม): ไม่ส่งต่อรอบนี้ (DEC-02)
