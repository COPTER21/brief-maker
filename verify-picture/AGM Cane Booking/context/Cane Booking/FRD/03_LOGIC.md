# 03_LOGIC — F-AGM-007 Cane Booking Management

> R8: mutation API → ≥1 Function · no HTTP ใน function · state machine centralized

## §3.1 Functions
| FN | Name | Purpose | Invoked by |
|---|---|---|---|
| FN-01 | `createBooking` | สร้าง + snapshot farmer/debt + waiting_for_verify | API-02 |
| FN-05 | `buildBookingListQuery` | list + filter 3-axis + **deriveDisplay** + phase_flags | API-01 |
| FN-06 | `computeCombinedProgress` ⭐ | คำนวณ 10-step combined + derived (รอส่งอนุมัติตัด/อยู่ระหว่างจัดส่ง/รอผลการเท) | API-04, FN-05 |
| FN-A | `approvalAction` | approve/reject/cancel (reason) + Gate + audit + event | API-A1/A2/A3 |
| FN-B | `cutTransportAction` | send-approval/approve/finish/dispatch-start · **no-skip guard** + Gate(A=verified) + audit | API-B1..B4 |
| FN-E | `ingestSystemEvent` ⭐ | check-in/receiving-completed/payment-completed · **non-manual** · idempotent(event_id) · set closed_at/awaiting_payment/completed | API-E1/E2/E3 |
| FN-V | `voidBooking` | manual void (reason) revert 1 ขั้น + clear tracking · block เมื่อ completed | API-V |
| FN-P | `generateDoc` ⭐ | ใบสั่งตัด/ใบส่งอ้อย idempotent + doc number + QR · gate ตามสถานะ | API-P1/P2/Pbulk |
| FN-10 | `recordBookingHistory` | append-only audit + event emit | ทุก FN |
| FN-11 | `guardTransition` ⭐ | ตรวจ no-skip + Gate + system-controlled + optimistic + idempotency | FN-A/B/E/V |
| FN-12 | `resolveDebt` | อ่าน Debt Mgt outstanding + snapshot | FN-01, API-D |

## §3.2 Engines
- **ENG-EXT-SRC** `booking-source-connector` [read] — Quota/Crop/Season snapshot · Debt Mgt
- **ENG-EVT** `event-ingest` [NEW] ⭐ — รับ system event (check-in/receiving/payment) idempotent · used FN-E
- **ENG-PDF** `doc-generator` — ใบสั่งตัด/ใบส่งอ้อย A4 + QR · idempotent · used FN-P

## §3.3 API ↔ Logic Trace (R8)
| API | Functions |
|---|---|
| API-01 | FN-05,06 |
| API-02 | FN-01,12,10 |
| API-04 | FN-06 |
| API-A1/A2/A3 | FN-A,11,10 |
| API-B1..B4 | FN-B,11,10 |
| API-E1/E2/E3 | FN-E,11,10 (ENG-EVT) |
| API-V | FN-V,11,10 |
| API-P1/P2/Pbulk | FN-P (ENG-PDF) |
| API-D | FN-12 |
> ทุก mutation มี FN + FN-11 guard + FN-10 audit ✅ · system events non-manual ✅

## §3.5 Locked Decisions
- LOCK-01/02: FN-B/FN-11 no-skip + Gate + ไม่มี dispatched (ปิดด้วย closed_at ผ่าน FN-E)
- LOCK-04: FN-06 derived states
- LOCK-05: FN-E only (system) สำหรับ รอผลการเท/รอทำจ่าย/เสร็จสิ้น
- LOCK-08: FN-11 idempotent+optimistic+reason
- LOCK-10: FN-P print gate + QR
- LOCK-11: FN-V/FN-A block เมื่อ completed
