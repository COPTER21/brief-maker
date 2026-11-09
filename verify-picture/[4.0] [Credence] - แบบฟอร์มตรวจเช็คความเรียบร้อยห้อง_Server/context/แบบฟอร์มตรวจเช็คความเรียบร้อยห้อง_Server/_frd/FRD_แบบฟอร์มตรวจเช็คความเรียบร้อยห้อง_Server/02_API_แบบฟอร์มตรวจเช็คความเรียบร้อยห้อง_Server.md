# 02_API — F-TMP-002
> base `/api/v1/server-room-checks` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/server-room-checks?q&status&result&owner&page&size&sort` | รายการตามสิทธิ์ (result = abn/ok) | FN-09 |
| API-02 | GET `/server-room-checks/{id}` | รายละเอียด + rows + chain + audit | FN-09 |
| API-03 | POST `/server-room-checks` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-03 |
| API-04 | PUT `/server-room-checks/{id}` | แก้ร่าง (เจ้าของ · draft) — เพิ่ม/แก้/ลบแถว | FN-01, FN-02 |
| API-05 | POST `/server-room-checks/{id}/submit` | ส่งปิดรอบ (draft → submitted) | FN-04 |
| API-07 | POST `/server-room-checks/{id}/cancel` `{reason}` | ยกเลิก | FN-06 |
| API-08 | GET `/server-room-checks/{id}/pdf` | PDF FM-ITS-10 | FN-07 |
| API-09 | GET `/server-room-checks/export.csv` | CSV ตามตัวกรอง | FN-09 |
| API-10 | POST/DELETE `/server-room-checks/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ rows:[{ id?, check_date, access_log, extinguisher_pressure, temperature_c, humidity_rh, aircon, cctv, mdb, pdu, remark }], attachment_ids[] }` · `checked_by` server ใส่เอง (ผู้เรียก API สำหรับแถวใหม่/แถวที่แก้) — FE ส่งมาจะถูกละ · 422 ตาม VR-01..03
- response แถวมี `issues[]` (คำนวณฝั่ง server จาก criteria_snapshot) สำหรับไฮไลต์
- API-05: 409 `NOT_DRAFT` · 403 `NOT_OWNER`
- (ไม่มี API-06 — ไม่มีขั้นพิจารณา DEC-03 · ถ้าเพิ่มผู้ตรวจทาน = enhancement)
- API-07: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin role) · 409 `NOT_CANCELLABLE` (cancelled) · 422 `REASON_REQUIRED`
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | src_abnormal_found · src_submitted · src_cancelled | {ref: src_id, vars} | ✓ |
| IT Support › Ticket | `src.abnormal_found` {src_id, check_date, issues[]} | | ประกาศ ไม่ยิง (DEC-02) |
| ENG-DOC-STORE | store(pdf,'SRC',id,…) | | ไม่เก็บค่าเริ่ม (snapshot flags ✗ — ปรับที่ F-DOCCFG) |
