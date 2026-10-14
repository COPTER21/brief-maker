# 03_LOGIC — F-AGM-010 Cane Check-In

> R8: mutation API → ≥1 Function · sync/idempotency centralized · no HTTP ใน function

## §3.1 Functions
| FN | Name | Purpose | Invoked by |
|---|---|---|---|
| FN-01 | `buildCheckInListQuery` | list (tab pending/checked-in) + filter + stats | API-01 |
| FN-02 | `lookupCbm` | หา CBM booking (dispatching) — not found error | API-03 |
| FN-03 | `searchMemberQuota` | ค้นโควต้าสมาชิก | API-04 |
| FN-C1 | `checkInCbm` ⭐ | validate weighToken + สร้าง check-in + **call syncBooking** | API-C1 |
| FN-C2 | `checkInMember` | validate ข้อมูล+payment bill + gen NBM doc | API-C2 |
| FN-C3 | `checkInCentral` | validate ข้อมูล+payment bill (no quota) + NBM doc | API-C3 |
| FN-SYNC | `syncBookingStatus` ⭐ | POST status-transitions {event:CHECK_IN, to_status:รอผลการเท} · idempotent(checkin_id) · set syncPending/error | API-SYNC/RETRY |
| FN-RETRY | `retrySync` | เรียก FN-SYNC ซ้ำด้วย checkin_id เดิม (no dup) | API-RETRY |
| FN-V | `voidCheckIn` | ยกเลิก (reason optional) + audit + reversal event | API-V |
| FN-10 | `recordCheckInAudit` | append audit | ทุก FN |
| FN-11 | `guardIdempotency` ⭐ | X-Idempotency-Key (checkin_id) กัน sync ซ้ำ | FN-SYNC |

## §3.2 Engines
- **ENG-BOOKING** `booking-sync-connector` ⭐ — POST /cane-bookings/:cbm/status-transitions (event CHECK_IN → รอผลการเท) · idempotent · retry-safe
- **ENG-SCALE** `weigh-token-source` [read] — เลขเหรียญชั่งจากเครื่องชั่ง (OQ-01)
- **ENG-EXT-Q** `quota-member-connector` [read] — Quota/Member (สมาชิก)
- **ENG-DOC** `checkin-doc-generator` — NBM doc number (Member/Central)

## §3.3 API ↔ Logic Trace (R8)
| API | Functions |
|---|---|
| API-01/02 | FN-01 |
| API-03/04 | FN-02/03 |
| API-C1 | FN-C1,SYNC,11,10 |
| API-C2/C3 | FN-C2/C3,10 |
| API-SYNC/RETRY | FN-SYNC,11,10 (ENG-BOOKING) |
| API-V | FN-V,10 |
> ทุก mutation มี FN + FN-10 audit · CBM check-in → FN-SYNC idempotent ✅

## §3.5 Locked Decisions
- LOCK-02: FN-C1/C2/C3 3 methods
- LOCK-03: FN-C1/C2/C3 weighToken required
- LOCK-04: FN-SYNC event CHECK_IN → รอผลการเท (ENG-BOOKING)
- LOCK-05: FN-RETRY idempotent (checkin_id)
- LOCK-06: doc prefix CBM/NBM by entryType
- LOCK-07: FN-C2/C3 payment bill 2 งวด
- LOCK-08: FN-V void + reason
