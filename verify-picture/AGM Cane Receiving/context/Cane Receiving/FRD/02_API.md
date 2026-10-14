# 02_API — F-AGM-011 Cane Receiving

> REST `/api/cane-receivings` + `/ext/factory/dump` (external) · headers: X-Idempotency-Key, If-Match(etag), X-Trace-Id · R8: mutation → Function

## §2.1 Endpoints
| API | Method | Path | Purpose |
|---|---|---|---|
| API-01 | GET | /cane-receivings?tab=&status=&caneType=&entryType=&q=&date= | list (draft/issued/void) + stats |
| API-02 | GET | /cane-receivings/:id | detail (+ dump result) |
| **API-DUMP** | GET | /ext/factory/dump?checkin_datetime=&weigh_coin=&quota_id= ⭐ | (external) dump v2 → caneType/timeIn/out/gross/tare/net · status SUCCESS/NOT_FOUND/DUPLICATE/ERROR |
| **API-C1** | POST | /cane-receivings | ออกใบรับอ้อย (idempotent) + side effects |
| **API-SYNC** | POST | /cane-receivings/sync-all ⭐ | {date_from,date_to,filters} → bulk dump+create → SyncAllResponse |
| **API-V** | POST | /cane-receivings/:id/void | ยกเลิก (reason≥5) + rollback |
| API-PDF | GET | /cane-receivings/:id/pdf | PDF A4 + QR |
| API-03 | GET | /cane-receivings/export | export CSV |
| API-CBM | PATCH | /cane-bookings/:cbm/status | (side effect) awaiting_payment / awaiting_dump_result |
| API-COIN | POST | /weigh-coin/free | (side effect) ปลดเลขเหรียญชั่ง |

## §2.X Contracts ⭐
- **API-DUMP (v2):** query `checkin_datetime + weigh_coin + quota_id?` (เปลี่ยนจาก date+coin) · response ไม่มี CCS · ถ้าโรงงานไม่ส่ง net → BE คำนวณ net = gross − tare · status≠SUCCESS → error banner (NOT_FOUND/DUPLICATE/ERROR)
- **API-C1 (issue):** idempotent (X-Idempotency-Key) · payload มี cane_type_code/cane_type_name/weigh_in_time/weigh_out_time/gross/tare/net · **side effects (atomic-ish):** status Issued + CRN + **PATCH CBM → awaiting_payment** + **POST /weigh-coin/free** + gen PDF A4+QR · เก็บ dump_result snapshot (jsonb, audit)
- **API-SYNC (Sync All):** X-Idempotency-Key + lock (ไม่รันซ้อน) · **บังคับ date_from/date_to** · select Draft (checked_in & receiving_id NULL) → ต่อ record: API-DUMP → SUCCESS = API-C1 + side effects · fail = เก็บ error · response {summary{total,success,failed}, failed_items[{checkin_id,weigh_coin,member_no,farmer_name,error_code,error_message}]}
- **API-V (void):** reason≥5 · block ถ้า paymentStatus=ชำระเงินแล้ว · rollback CBM → awaiting_dump_result · keep dump snapshot (audit)

## §2.2 ตัวอย่าง
```
POST /api/cane-receivings/sync-all   (X-Idempotency-Key: <uuid>)
{ "date_from":"2025-01-10","date_to":"2025-01-10","filters":{"area_code":null,"extension_code":null} }
→ 200 { "summary":{"total":120,"success":100,"failed":20},
        "failed_items":[{"checkin_id":"CHK-2025-00001","weigh_coin":"WC-000111","member_no":"M0001",
                         "error_code":"NOT_FOUND","error_message":"ไม่พบข้อมูลผลการเทในระบบโรงงาน"}] }
```
Events: `receiving.issued` (→ cbm.awaiting_payment + coin.freed) · `receiving.voided` (→ cbm.awaiting_dump_result) · `receiving.synced_all`

## §2.3 Errors → 05_RULES §5.6
VALIDATION_FAILED · DUMP_NOT_FOUND/DUPLICATE/ERROR · CONFLICT(409 dup idempotency = no-op) · CONFLICT_UPDATE_STALE(409 etag) · VOID_BLOCKED_PAID · SYNC_ALL_DATE_REQUIRED
