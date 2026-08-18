# 00_OVERVIEW — F-WH-PICK Picking

| Field | Value |
|---|---|
| Variant | FULL (3 pages, 7 states, cross-module transactions, allocation engine) |
| BRD | `../BRD_F-WH-PICK_Picking.md` — APPROVED |
| HTML | `../f-wh-picking.html` — UX/Coverage/E2E passed |
| Module | Warehouse Outbound / S5 |
| Highest classification | Confidential |

## §0.1 Purpose

เปลี่ยน SO ที่พร้อมส่งเป็นใบหยิบที่ล็อกตำแหน่ง/ล็อตจริง ให้ผู้หยิบบันทึกครบหรือขาด และส่งผลต่อ Inventory, Sales, Packing และ ENG-NOTIFY อย่างตรวจสอบย้อนหลังได้

## §0.2 Scope

In: SO queue, create/wave, allocate, assign, pick, short, relocate, hold, cancel, close-short, Packing handoff, A4, audit.

Out: source trigger นอก SO, SO warehouse reservation, real replenishment/cycle count, Pack/DN logic, RF gun, multi-picker zone picking.

## §0.3 Roles

| Role | Scope |
|---|---|
| `wh_lead` | ทุกใบ; create/assign/cancel/all pick actions |
| `picker` | ใบที่ตนได้รับมอบหมาย; pick/relocate/hold/close-short/to-pack |
| `viewer` | read-only |

## §0.4 Dependencies / Value Stream

`Sales Order → Picking → Packing → Delivery Note`; reads Item, Location, Inventory balance, Employee/IAM; writes through Inventory/Sales/Packing/ENG-NOTIFY contracts only.

## §0.5 Security domains

Authentication/authorization, transaction integrity, audit logging, employee operational data, multi-tenant isolation, idempotency and concurrency.

## §0.6 AI defaults from probing

- `[AI-DEFAULT]` optimistic lock via version/If-Match
- `[AI-DEFAULT]` Idempotency-Key on every mutation
- `[AI-DEFAULT]` downstream/notification failure does not corrupt committed Pick state
- `[AI-DEFAULT]` stale/inactive master is revalidated at mutation time

## §0.7 Data classification

Confidential: assignee/workload, Pick operational detail. Internal: quantities, lot/location, audit and event refs. Public: none.

## §0.8 Open Questions

OQ-01 waveMax/workload setting owner; OQ-02 picker override/close-short permission; OQ-03 allocation engine registration/owner; OQ-04 override reason; OQ-05 Packing intake contract; OQ-06 current F-NOTIFY catalog.

## §0.11 Scope Lock

LOCK-01..12 imported verbatim in `07_LOCKED_DECISIONS.md §7.0`; no drift found.

## §0.12 Coverage Manifest

| BRD ref | Requirement | Pack evidence |
|---|---|---|
| US-01 / FN-01..09 | queue/create/allocation | `01_UI` P-01/P-02; API-01/03; FN-03/04; BR-01..07; AT-01..09 |
| US-02 / FN-10..11 | assignment/permission | P-02/P-03; API-04; FN-05; BR-08; AT-10..11 |
| US-03 / FN-12..13 | start/pick movement | P-03; API-05/06; FN-06/07; BR-06/09; AT-12..13 |
| US-04 / FN-14..18 | short/relocate/refresh | P-03 overlays; API-07..10; FN-08..11; BR-07/09..12; AT-14..18 |
| US-05 / FN-19..23 | finish/pack/hold/cancel | P-03; API-11..15; FN-12..16; BR-13..15; AT-19..23 |
| US-06 / FN-90..94 | list/tabs/A4/Esc/audit | P-01/P-03; API-01/02/16; BR-16; AT-90..94 |
| LOCK-11 / FN-24 | SO-only negative | API source enum + BR-17 + AT-24 |
| EC-01..07 | confirmed edges | `05_RULES §5.5`; `06_TESTS` EC/XT cases |
| EC-08..12 | conservative defaults | `05_RULES §5.5 [AI-DEFAULT]`; `06_TESTS` CC/ID/XT/NTF |

Verdict: every BRD story/rule/edge has an implementation and test anchor.
