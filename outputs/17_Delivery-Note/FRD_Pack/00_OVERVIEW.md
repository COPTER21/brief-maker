# 00_OVERVIEW — F-WH-DN Delivery Note

| Field | Value |
|---|---|
| Variant | FULL (3 routes, 8 states, multiple transactional integrations) |
| BRD | `../BRD_F-WH-DN_DeliveryNote.md` — APPROVED |
| HTML | `../f-wh-delivery-note.html` — UX/Coverage/E2E passed |
| Module | Warehouse Outbound / S5 |
| Highest classification | Confidential |

## §0.1 Purpose

สร้างและติดตามใบส่งของจาก Packing หรือแบบ Manual ตั้งแต่เตรียมข้อมูล ออกรถ ผลส่ง ตีกลับ และยกเลิก พร้อมควบคุม stock/source sync ตามชนิดต้นทาง

## §0.2 Scope

In: SO/Stock Transfer reference, combine guard, delivery assignment, own/3PL/pickup/manual transport, dispatch/GI, tracking, failed attempts, POD, partial/backorder decision, return/cancel/reverse, Manual DN, A4, audit.

Out: real 3PL API, route optimization, multi-vehicle split, mobile e-POD/GPS, automatic freight calculation/Credit Note, master maintenance.

## §0.3 Roles

| Role | Scope |
|---|---|
| `wh_lead` | all records and management actions |
| `picker/driver` | dispatch/tracking/fail/POD on assigned records per IAM |
| `viewer/sales` | read/print only |

## §0.4 Dependencies / Value Stream

`SO/Transfer → Picking → Packing → Delivery Note → Inventory + source status + AR`; also reads Employee/Fleet/Carrier and calls Document/Notification engines.

## §0.5 Security domains

Authorization, tenant isolation, transaction integrity, PII minimization, audit, concurrency, idempotency, outbox and external snapshot control.

## §0.6 AI defaults from probing

- `[AI-DEFAULT]` optimistic lock by version/If-Match
- `[AI-DEFAULT]` Idempotency-Key on all mutations
- `[AI-DEFAULT]` all-or-nothing GI/reversal/source sync
- `[AI-DEFAULT]` revalidate active master at mutation while keeping snapshots
- `[AI-DEFAULT]` downstream/notification failure uses transactional outbox and safe retry

## §0.7.1 Data classification

Confidential: customer/ship-to/contact, driver name/phone, assignment and POD/audit. Internal: quantities, warehouse, source references, statuses and integration refs. Public: none. Restricted: none identified.

## §0.8 Open Questions

OQ-01 max attempts/photo config; OQ-02 mutation permissions; OQ-03 manual transport governance; OQ-04 Stock Transfer contract; OQ-05 RTN/QC; OQ-06 AR/Credit Note; OQ-07 catalog collisions; OQ-08 performance targets.

## §0.11 Scope Lock

LOCK-01..12 are imported verbatim in `07_LOCKED_DECISIONS.md §7.0`; no conflict found.

## §0.12 Coverage Manifest

| BRD ref | Requirement | Pack evidence |
|---|---|---|
| US-01 / BR-01..03 | queue, combine, reference create | `01_UI` P-01; API-01/03; FN-01/03; AT-01..04 |
| US-02 / BR-04..06,20 | assignment and transport | P-01/P-02; API-04/05; FN-04/05; AT-05..10 |
| US-03 / BR-07..08 | ready/dispatch/GI | P-02; API-06/07; FN-06/07; ENG-DN-01; AT-11..13 |
| US-04 / BR-09..12 | tracking, failed, POD | P-02 overlays; API-08..10; FN-08..10; AT-14..20 |
| US-05 / BR-13..14 | partial/return/cancel/SO | API-11..14; FN-11..14; AT-21..27 |
| US-06 / BR-15 | Stock Transfer | P-01/P-02; XT-03; AT-28..30 |
| US-07 / BR-18..19 | Manual DN/status isolation | API-15/16; FN-15/16; AT-31..35 |
| US-08 / BR-16..17,21..22 | read-only, A4, audit/shared services | API-02/17; P-02 tabs; AT-36..40 |
| EC-01..09 | confirmed edge cases | `05_RULES §5.5`; `06_TESTS §6.7` |
| EC-10..14 | conservative engineering defaults | `05_RULES §5.5 [AI-DEFAULT]`; `06_TESTS §6.8` |

Verdict: all BRD stories, rules and confirmed edges have implementation and test anchors.
