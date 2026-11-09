# 02_API — F-TMP-006
> base `/api/v1/server-room-access` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/server-room-access?q&status&cert&owner&page&size&sort` | รายการตามสิทธิ์ (cert = pend/ok) | FN-09 |
| API-02 | GET `/server-room-access/{id}` | รายละเอียด + entries + chain + audit | FN-09 |
| API-03 | POST `/server-room-access` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-03 |
| API-04 | PUT `/server-room-access/{id}` | แก้ร่าง (เจ้าของ · draft) — เพิ่ม/แก้/ลบแถวที่ยังไม่รับรอง · บันทึกเวลาออก | FN-01, FN-02 |
| API-05 | POST `/server-room-access/{id}/submit` | ส่งปิดรอบ (draft → submitted) | FN-04 |
| API-06 | POST `/server-room-access/{id}/entries/{entryId}/certify` | รับรองรายแถว | FN-10 |
| API-07 | POST `/server-room-access/{id}/cancel` `{reason}` | ยกเลิก | FN-06 |
| API-08 | GET `/server-room-access/{id}/pdf` | PDF FM-ITS-09 | FN-07 |
| API-09 | GET `/server-room-access/export.csv` | CSV ตามตัวกรอง | FN-09 |
| API-10 | POST/DELETE `/server-room-access/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ entries:[{ id?, visitor_emp_id?, visitor_name, visitor_department, in_date, in_time, out_date?, out_time?, purpose }], attachment_ids[] }` · `visitor_signed_by/at` server ใส่เอง (ผู้เรียก API ตอนสร้างแถว) · `certified_by/at` แก้ผ่าน API นี้ไม่ได้ (FE ส่งมาจะถูกละ) · แถวที่รับรองแล้วแก้/ลบไม่ได้ → 409 `ENTRY_CERTIFIED` · 422 ตาม VR-01..04
- response แถวมี `issues[]` (คำนวณฝั่ง server — overstay) สำหรับไฮไลต์
- API-05: 409 `NOT_DRAFT` · 403 `NOT_OWNER` · 422 `ENTRIES_OPEN` (ยังไม่บันทึกออก) · 422 `ENTRIES_NOT_CERTIFIED`
- API-06: 403 `NOT_IT_OFFICER` · 403 `SELF_CERTIFY` (ผู้รับรอง = ผู้เข้า) · 409 `ENTRY_OPEN` · 409 `ALREADY_CERTIFIED` · 409 `NOT_DRAFT`
- API-07: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin role) · 409 `NOT_CANCELLABLE` (cancelled) · 422 `REASON_REQUIRED`
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | sral_certify_pending · sral_overstay · sral_submitted · sral_cancelled | {ref: sral_id, vars} | ✓ |
| ระบบประตู/บัตรผ่าน | — | — | ไม่มี (DEC-02) |
| ENG-DOC-STORE | store(pdf,'SRAL',id,…) | | ไม่เก็บค่าเริ่ม (snapshot flags ✗ — ปรับที่ F-DOCCFG) |
