# 02_API — F-AGM-010 Cane Check-In

> REST `/api/agm/checkins` + `/api/cane-bookings/*` (sync) · headers: X-Idempotency-Key, X-Trace-Id · R8: mutation → Function

## §2.1 Endpoints
| API | Method | Path | Purpose |
|---|---|---|---|
| API-01 | GET | /checkins?tab=&status=&entryType=&q=&date= | list (pending/checked-in) + stats |
| API-02 | GET | /checkins/:id | detail |
| API-03 | GET | /cane-bookings/:cbm | lookup CBM (CBM check-in) — "ไม่พบรหัส CBM นี้" ถ้าไม่มี |
| API-04 | GET | /quotas/search?q= | ค้นโควต้าสมาชิก — "ไม่พบโควต้านี้" |
| **API-C1** | POST | /checkins/cbm | เช็คอิน CBM (weighToken req + sync) |
| **API-C2** | POST | /checkins/member | เช็คอินสมาชิก (NBM doc + payment bill) |
| **API-C3** | POST | /checkins/central | เช็คอินโควต้ากลาง (NBM doc + payment bill) |
| **API-SYNC** | POST | /cane-bookings/:cbm/status-transitions ⭐ | {event:CHECK_IN, to_status:"รอผลการเท", checkin_id, coin_no, farmer_quota_no, checkin_datetime} · X-Idempotency-Key=checkin_id |
| API-RETRY | POST | (API-SYNC ซ้ำ) | retry sync (idempotent) |
| **API-V** | POST | /checkins/:id/void | ยกเลิก (reason optional) |
| API-05 | GET | /checkins/export | export CSV |

## §2.X Contracts ⭐
- **API-C1 (CBM):** weighToken required ("กรุณาใส่เลขเหรียญชั่ง") · CBM code valid (API-03) · หลังสร้าง check-in → call **API-SYNC** (BR-03/04)
- **API-SYNC:** POST status-transitions · idempotent (X-Idempotency-Key=checkin_id) · success 200 {cbm_code, old_status, new_status:"รอผลการเท", version} → syncPending=false · fail (non-2xx) → throw → syncPending=true + syncError → retry (same key = no dup)
- **API-C2/C3 (Member/Central):** ข้อมูลครบ (plate/driver/phone/type/weigh) "กรุณากรอกข้อมูลให้ครบถ้วน" · payment bill งวด1+2 "กรุณาเลือกประเภทการชำระเงินให้ครบถ้วน" · gen NBM doc · ไม่มี sync (non-CBM)
- **API-V:** reason optional · emit void audit (+ reversal event ไป Booking — OQ-04)
- **entryType → doc:** จองคิว=CBM-#### · ไม่จองคิว/กลาง=NBM-#### (BR-05)

## §2.2 ตัวอย่าง
```
POST /api/cane-bookings/CBM-2568-0000004/status-transitions
X-Idempotency-Key: CHKIN-5
{ "event":"CHECK_IN","to_status":"รอผลการเท","source":"cane_checkin",
  "checkin_id":"CHKIN-5","coin_no":"022","farmer_quota_no":"Q12348","checkin_datetime":"..." }
→ 200 { "cbm_code":"CBM-2568-0000004","old_status":"อยู่ระหว่างจัดส่ง","new_status":"รอผลการเท","version":12 }
```
Events: `checkin.created` · `checkin.synced|sync_failed` · `checkin.voided` · (→ CBM `cbm.checkin` = booking รอผลการเท)

## §2.3 Errors → 05_RULES §5.6
VALIDATION_FAILED · NOT_FOUND(CBM/quota) · SYNC_FAILED(retryable) · CONFLICT(409 dup idempotency = no-op) · CONFLICT_UPDATE_STALE(409 version)
