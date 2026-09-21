# 00_OVERVIEW — F084 Stocktake

| Field | Value |
|---|---|
| Feature | F084 · F-WH-STOCKTAKE · ตรวจนับใหญ่ |
| Module | Warehouse |
| Variant | FULL (8 states + approval + financial variance) |
| Status | APPROVED |
| Version | 1.0 · 2026-09-20 |
| Source | `BRD_F-WH-STOCKTAKE.md` + HTML ที่ผ่าน E2E 20/20 |

## §0.2 Scope

In: รอบนับ, scoped freeze/snapshot, assigned blind count, threshold recount, variance review, DOA sequential approval, F082 draft handoff, append-only history. Out: PDF/เลขรัน, Cycle Count/ABC, barcode implementation, master implementation, direct on-hand mutation, DOA setup UI

## §0.3 Roles

| Role | หน้าที่ |
|---|---|
| counter | กรอก/ส่งผลเฉพาะ sheet ที่มอบหมาย |
| recount_counter | กรอก/ส่งครั้ง 2 และต้องคนละคน |
| supervisor | สร้าง/freeze/assign/review/submit DOA/handoff |
| current_approver | approve/reject เฉพาะ step ปัจจุบัน |
| auditor | อ่าน event ตามสิทธิ์ |

## §0.4 Dependencies

- Upstream: Warehouse/Location F008, Inventory F009, Item, Roles F020, DOA F019
- Downstream: Stock Adjustment F082, Inventory movement engine
- Optional input hook: Barcode F089

## §0.5 Security and Classification

Multi-tenant: yes in production. Highest classification: **Confidential** (`system_qty`, `unit_cost`, `variance_value`, selected people). Audit required for every mutation. Counter responses must exclude system balance and variance

## §0.6 Open Questions

| ID | Question | Owner |
|---|---|---|
| OQ-ST-01 | lock registry/query contract ข้าม movement features | Inventory owner |
| OQ-ST-02 | permission จริงของ reveal/approval | Policy owner |
| OQ-ST-03 | DOA tier และ `role-*` mapping | Warehouse BA + DOA admin |
| OQ-ST-04 | F082 payload/ack final | F082 owner |

## §0.7 `[AI-DEFAULT]` Probes

- PR-1 approval concurrency: optimistic lock; first commit wins, second 409
- PR-3 permission mid-flight: re-check role/person on every mutation
- PR-4/PR-7: idempotency key for freeze, submit, decision and handoff; cache same result 24h
- PR-9: scope lock transaction and snapshot use one atomic boundary

## §0.11 Scope Lock

| LOCK | FRD enforcement |
|---|---|
| LOCK-ST-01 | ไม่มี document/PDF/number API หรือ page |
| LOCK-ST-02 | API-03 + FN-03/FN-04 + DB snapshot/lock |
| LOCK-ST-03 | API response projection + UI permission matrix |
| LOCK-ST-04 | BR-ST-04/06/07/08 + approval APIs |
| LOCK-ST-05 | ไม่มี inventory update; only F082 contract + append-only tables |

## §0.12 Coverage Manifest

| BRD Ref | Requirement | อยู่ที่ |
|---|---|---|
| S-01 | สร้างรอบ | UI P-01/O-01 · API-02 · FN-02 · AT-01/02 |
| S-02 | freeze snapshot | UI P-02 · API-03 · FN-03/04 · AT-03/04 |
| S-03 | assign blind sheet | UI P-02 · API-04 · FN-05 · AT-05/06 |
| S-04 | submit count | UI P-02 · API-05 · FN-06 · AT-07/08 |
| S-05 | independent recount | UI P-02/P-03 · API-04/05 · FN-07 · AT-09/10 |
| S-06 | variance review | UI P-03 · API-06 · FN-08/ENG-01 · AT-11 |
| S-07 | DOA approval | UI P-03 · API-07/08 · FN-09/10 · AT-12..16 |
| S-08 | F082 handoff | UI P-03/P-04 · API-09 · FN-11/ENG-02 · XT-01/02 |
| BR-ST-01..10 | กฎธุรกิจ | `05_RULES.md` §5.1 · `06_TESTS.md` |
| Edge cases | overlap/invalid/permission/concurrency/idempotency | `05_RULES.md` §5.5 · `06_TESTS.md` |

สรุป: Stories 8/8 · Rules 10/10 · confirmed edges 10/10

## §0.13 Demo-only elements

`[data-demo="persona-switch"]` และ badge `DEMO` เป็น review harness เพื่อสลับ P1–P5 เท่านั้น Production ต้องใช้ session identity/authorization และไม่ render ส่วนนี้
