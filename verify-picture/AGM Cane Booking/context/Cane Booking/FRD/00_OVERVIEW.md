# 00_OVERVIEW — F-AGM-007 Cane Booking Management

> Pack STANDARD (7 ไฟล์) · Refactor+Enhancement Synthesis v1.1→v1.7 · constraint mode (invariants.md 🔒)

## §0.1 Feature
| Field | Value |
|---|---|
| ID | F-AGM-007 · Cane Booking Management (CBM) — เดิม ETCD |
| Module | AGM · WKN |
| Cross-module/Events | read Quota/Crop/Season · Debt Mgt · รับ event Receiving/Payment/Check-In (system-controlled) |
| Route | `#/bookings` (list) · `#/bookings/:booking_id` (detail+timeline) · `#/bookings/:id/view` (read-only QR) |
| CI | CUBE Warm Light |

## §0.11 Scope Lock (BRD §3.4)
LOCK-01..11 — สรุป: 3-axis no-skip · ไม่มี dispatched · combined 10-step timeline + derived · system-controlled locks · phase "-" + filter · verified="อนุมัติรอบจองแล้ว" · idempotent+optimistic+reason · debt% · print 2 PDFs + bulk · completed lock

## §0.12 Coverage Manifest
| Story | Layer | Test |
|---|---|---|
| US-01 create | 01_UI OV-01 · API-02 · FN-01 | AC-01..05 |
| US-02 approve/reject/cancel | 01_UI OV-03 · API-A1..A3 · FN-A | AC-06..09 |
| US-03 cut/dispatch flow | 01_UI Detail actions · API-B1..B4 · FN-B | AC-10..15 |
| US-04 system events | 01_UI sim buttons · API-E1..E3 · FN-E | AC-16..19 |
| US-05 list 3-axis+derived | P-01 · API-01 · FN-05 | AC-20..24 |
| US-06 detail timeline | P-02 · API-04 · FN-06 | AC-25..27 |
| US-07 print docs | API-P1/P2/Pbulk · FN-P | AC-28..31 |
| US-08 debt % | OV-01/detail · API-D · FN-01 | AC-32 |
| US-09 void/lock | API-V · FN-V | AC-33..34 |
| US-10 search/export | P-01 · API-01/15 · FN-05 | AC-35..36 |
> Coverage 10/10 · FN + API state actions + events ✅

## §0.13 Variant = STANDARD (7 files)

## §0.14 Cross-Module Summary
CBM อ่าน Quota/Crop/Season + Debt · **รับ event** จาก Receiving/Payment/Check-In (non-manual) · ในต้นแบบจำลอง event ด้วยปุ่ม "จำลอง event ระบบ"
