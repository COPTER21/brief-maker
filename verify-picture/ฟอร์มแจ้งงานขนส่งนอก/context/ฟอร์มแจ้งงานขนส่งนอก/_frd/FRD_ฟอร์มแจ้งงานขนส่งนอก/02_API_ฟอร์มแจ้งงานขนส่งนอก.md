# 02_API — F-TMP-003
> base `/api/v1/outsourced-transport-notices` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/outsourced-transport-notices?q&status&carrier&preparer&page&size&sort` | รายการตามสิทธิ์ + count ต่อสถานะ (tabs) · q ค้นเลขที่/ผู้ขนส่ง/เลขที่PO/ปลายทาง | FN-08 |
| API-02 | GET `/outsourced-transport-notices/{id}` | รายละเอียด + lines + audit | FN-08 |
| API-03 | POST `/outsourced-transport-notices` | สร้างร่าง + ออกเลข | FN-01, FN-02 |
| API-04 | PUT `/outsourced-transport-notices/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01 |
| API-05 | POST `/outsourced-transport-notices/{id}/submit` | ส่งแจ้งงาน | FN-03, FN-04, FN-06 |
| API-06 | POST `/outsourced-transport-notices/{id}/cancel` `{reason}` | ยกเลิก | FN-05, FN-06 |
| API-07 | GET `/outsourced-transport-notices/{id}/pdf` | PDF FM-SAL-16 | FN-07 |
| API-08 | GET `/outsourced-transport-notices/export.csv` | CSV ตามตัวกรอง (1 แถวต่อรายการ) | FN-08 |
| API-09 | POST/DELETE `/outsourced-transport-notices/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ carrier_id, round_date, lines:[{ origin, destination, po_no, qty, delivery_date }], attachment_ids[] }` — ร่าง: lines ไม่ครบได้ · ไม่มี carrier_id/round_date → 422 (VR-01/02) · qty ไม่ใช่จำนวนเต็ม > 0 (เมื่อกรอก) → 422 `QTY_INVALID` · แถวว่างทั้งแถวถูกตัดทิ้ง
- API-05: 409 `NOT_DRAFT` · 422 `LINES_INCOMPLETE {rows:[n]}` (BR-01/02) · 422 `NO_LINES` · 403 `NOT_OWNER` · response มี `warnings:[{code:'DELIVERY_BEFORE_ROUND', rows:[n]}]` (BR-04 ไม่บล็อก)
- API-06: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/role-mgr-sales) · 409 `ALREADY_CANCELLED` · 422 `REASON_REQUIRED`
- API-03: 409 `DOC_TYPE_INACTIVE` (F-DOCCFG ปิดใช้ OTN)
- ทุก GET ใบที่ไม่มีสิทธิ์เห็น → 404 `NOT_FOUND` (ไม่บอกว่ามีใบอยู่)
- 409 `STALE_VERSION` เมื่อ If-Match ไม่ตรง

## §2.3 Events (ENG-NOTIFY · NTF_BRIEF_F-TMP-003)
- `otn_submitted` — API-05 สำเร็จ → role-mgr-sales
- `otn_early_delivery_date` — API-05 สำเร็จและมีแถว delivery_date < round_date → role-mgr-sales
- `otn_cancelled` — API-06 สำเร็จโดยผู้ที่ไม่ใช่เจ้าของ → เจ้าของ
- ไม่มี doa_* (ไม่มี DOA — DEC-03) · ไม่ยิง event ไประบบอื่น (DEC-02)
