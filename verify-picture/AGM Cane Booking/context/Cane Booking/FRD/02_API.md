# 02_API — F-AGM-007 Cane Booking Management

> REST · `/api/cbm/*` (alias `/api/etcd/*` deprecate) · headers: X-Idempotency-Key, If-Match(row_version), X-Trace-Id · R8: mutation → Function

## §2.1 Endpoints
| API | Method | Path | Purpose |
|---|---|---|---|
| API-01 | GET | /cbm/bookings | list search/filter/sort/page (+ derived phase display, phase_flags) |
| API-02 | POST | /cbm/bookings | สร้าง (waiting_for_verify) |
| API-04 | GET | /cbm/bookings/:id | detail + timeline |
| API-05 | PUT | /cbm/bookings/:id | แก้ไข (ก่อนส่งทำจ่าย) |
| **API-A1** | POST | /:id/approve | approval: waiting_for_verify → verified |
| **API-A2** | POST | /:id/reject | → rejected (reason บังคับ) |
| **API-A3** | POST | /:id/cancel | → cancelled (reason บังคับ) |
| **API-B1** | POST | /:id/cut/send-approval | verified&cut=null → awaiting_cut_approval |
| **API-B2** | POST | /:id/cut/approve | awaiting_cut_approval → awaiting_cutting |
| **API-B3** | POST | /:id/cut/finish | awaiting_cutting → awaiting_dispatch (payload cutting_summary?) |
| **API-B4** | POST | /:id/dispatch/start | awaiting_dispatch → dispatching (dispatch_started_at) |
| **API-E1** | POST | /cbm/events/check-in | (system) → checkin_id → "รอผลการเท" |
| **API-E2** | POST | /cbm/events/receiving-completed | (system) → ปิดแกน B (closed_at) + payment=awaiting_payment |
| **API-E3** | POST | /cbm/events/payment-completed | (system) → payment=completed (lock) |
| API-V | POST | /:id/void | manual void (reason) revert 1 ขั้น |
| API-P1 | GET | /:id/print/cutting-order | PDF ใบสั่งตัด (≥awaiting_cutting) |
| API-P2 | GET | /:id/print/delivery-note | PDF ใบส่งอ้อย (≥awaiting_dispatch) |
| API-Pbulk | POST | /cbm/bookings/print/bulk | {type, ids[]} → ZIP (202 job) |
| API-D | GET | /debt/debtors?quota_id= | outstanding (แสดงตอนสร้าง) |
| API-15 | GET | /cbm/bookings/export | export CSV (แสดง "-" ตามจอ) |
| API-12 | GET | /:id/history | audit + events |

## §2.X State/Event Contract ⭐ (→ BRD §4)
- **Manual actions (A1..A3, B1..B4, V):** idempotent (X-Idempotency-Key) + optimistic (If-Match row_version) + reason(reverse/reject/cancel) + emit event + audit · ผิดลำดับ → 400 ILLEGAL_STATE_TRANSITION
- **System events (E1..E3):** idempotent (event_id) · **non-manual guard**: PATCH/manual → awaiting_payment/completed/รอผลการเท = 400 ILLEGAL_STATE_TRANSITION · ซ้ำ → 409/200 no-op
  - E2 receiving: ถ้าสร้างคำขอจ่ายไม่สำเร็จ → คง dispatching + 202 + retry (banner)
- **Print (P1/P2/Pbulk):** idempotent generator · เลขเอกสารรันแยกจาก booking · ฝัง QR `/:id/view`

## §2.2 ตัวอย่าง
```
POST /api/cbm/bookings/CBM-2568-000012/dispatch/start
{ "vehicle_plate":"xx-1234","lane":"D3","dispatch_start_at":"2025-11-11T16:00:00+07:00" }
→ 200 { "id":"CBM-2568-000012","cut_transport_status":"dispatching","dispatch_started_at":"...","row_version":8 }
```
Events emitted: `cbm.approval.verified|rejected|cancelled` · `cbm.cut.approval.requested|approved` · `cbm.cut.finished` · `cbm.dispatch.started` · `cbm.checkin` · `cbm.dispatch.closed`(receiving) · `cbm.payment.completed`

## §2.3 Errors → 05_RULES §5.6
VALIDATION_FAILED · FORBIDDEN · CONFLICT_UPDATE_STALE(409) · ILLEGAL_STATE_TRANSITION(400) · CONFLICT(409 dup event)
