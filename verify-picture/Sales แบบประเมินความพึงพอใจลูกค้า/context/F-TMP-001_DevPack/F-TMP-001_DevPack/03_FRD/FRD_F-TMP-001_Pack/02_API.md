# 02_API — F-TMP-001
> base `/api/v1/customer-satisfactions` · tenant จาก token (RLS) · ทุก write มี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/customer-satisfactions?q&status&business_type&page&size&sort` | รายการตามสิทธิ์ | FN-08 |
| API-02 | GET `/customer-satisfactions/{id}` | รายละเอียด + audit | FN-08 |
| API-03 | POST `/customer-satisfactions` | สร้างร่าง + ออกเลข | FN-01, FN-02 |
| API-04 | PUT `/customer-satisfactions/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01 |
| API-05 | POST `/customer-satisfactions/{id}/submit` | ส่ง (resolve DOA → 0 ขั้น = submitted) | FN-01, FN-03, FN-05 |
| API-06 | POST `/customer-satisfactions/{id}/cancel` `{reason}` | ยกเลิก | FN-04 |
| API-07 | GET `/customer-satisfactions/{id}/pdf` | PDF FM-SAL-06 | FN-06 |
| API-08 | GET `/customer-satisfactions/export.csv` | CSV ตามตัวกรอง | FN-07 |
| API-09 | POST/DELETE `/customer-satisfactions/{id}/attachments` | ไฟล์ (Document Center) | FN-09 |
| API-10 | GET `/customers?q` (Sales › Customer · อ่าน) | ตัวช่วยเลือกชื่อร้าน | — (API ของ feature เจ้าของ) |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ store:{customer_id|null, name}, business_type|null, relationship_years|null, rating:{quality..overall: 1–5|null}, suggestion, attachment_ids[] }` → 422 VR-01 (store.name ว่าง) · ค่า enum/คะแนนนอกช่วง → 422 `INVALID_VALUE`
- API-05: 409 `NOT_DRAFT` · 422 `INCOMPLETE` (VR-02..04 พร้อมรายการช่อง) · 403 `NOT_OWNER`
- API-06: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/role-mgr-sales) · 409 `NOT_CANCELLABLE` (cancelled) · 422 `REASON_REQUIRED`
- API-02/07 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- API-03 เมื่อ doc_type CSE ปิดใช้ → 409 `DOC_TYPE_INACTIVE`

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 `STALE` · audit ทุก write (append-only) · RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API ของ feature)
