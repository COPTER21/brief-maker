# 00_OVERVIEW — F-WH-PACK Packing

## §0.1 Document Control

| Field | Value |
|---|---|
| Feature | F-WH-PACK — Packing |
| Module | Warehouse Outbound |
| Variant | FULL (มี state machine 5 states, 10+ mutations, cross-module integration) |
| Status | IN-REVIEW — guarded OQs |
| FRD Version | 1.0 · 2026-08-19 |
| Generator | frd-generator-v6 |
| Source | BRD v1.0 + approved HTML + PREBRIEF/checklist + Picking final contract |
| UX Gate | WAIVED-BLOCK; HTML unchanged |

## §0.2 Revision

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-19 | Initial HTML-first pack |

## §0.3 Scope

In: Packing intake/queue, carton allocation, scan/undo/weight, close/reopen/finish/cancel, printing, permission, audit, notification and DN adapter boundary.

Out: Picking execution, Transfer contract, DN implementation, inventory posting, route planning, serial scan, photos, freight charge, DOA/DOCCFG declarations.

## §0.4 COSO Roles

| Role | Responsibility |
|---|---|
| Maker: `picker`/`packer` | start/pack/close/finish own job subject to IAM decision |
| Checker: `wh_lead` | reopen, exception review, operational verification |
| Approver | N/A — no approval workflow |
| Owner | Warehouse Operations |
| System | invariants, snapshots, audit, outbox, print and integrations |

## §0.5 Dependencies

| Direction | Dependency | Contract |
|---|---|---|
| upstream | Picking | `POST /api/v1/picks/:id/send-to-packing`; `picked→to_pack`; `{pick,pack_refs[]}` |
| upstream/read | SO, Item, Inventory, Location, IAM | snapshot/read models; exact service endpoints implementation-owned |
| downstream | Print | PACKSLIP A4, BOXLABEL 150×100 |
| downstream | ENG-NOTIFY | NTF declaration after FRD |
| downstream | Delivery Note | adapter disabled until OQ-DN-01 resolved |

## §0.6 Architecture

UI → `/api/v1/packing-*` HTTP layer → scope-local Functions → pure carton calculation engine / print engine → PostgreSQL. Mutations use transaction + outbox + append-only audit.

## §0.7 Security/Data

- Multi-tenant: YES; tenant and warehouse isolation mandatory
- Confidential/PII: ship-to/contact and employee identity snapshots
- Financial: NO
- Audit: YES, every mutation and state transition

## §0.8 Open Questions

OQ-01..10, OQ-XT-01, OQ-DN-01 from BRD §15. None may be filled by implementation guess. OQ-DN-01 and OQ-XT-01 block only their integrations, not core Packing.

## §0.9 Glossary

| Term | Meaning |
|---|---|
| job | idempotent intake unit for one Pick source SO |
| pack | document/lifecycle instance for one job |
| active carton | sole open carton accepting allocation |
| label version | immutable print snapshot; reopen invalidates previous version |

## §0.10 Navigation

`01_UI` screens · `02_API` HTTP · `03_LOGIC` functions/engines · `04_DB` schema · `05_RULES` authority · `06_TESTS` acceptance · `07_LOCKED_DECISIONS` immutable choices · `INDEX` quick map.

## §0.12 Coverage Manifest

| BRD Ref | Pack coverage |
|---|---|
| US-01 intake | UI P-01 · API-01/03 · FN-01 · BR-PACK-01/03 · AT-01/02 |
| US-02 carton open | P-02 · API-05 · FN-03 · BR-PACK-04/06 · AT-04 |
| US-03 allocation | P-02 · API-06/07 · FN-04 · ENG-01 · BR-PACK-05/07 · AT-05/06 |
| US-04 carton close | P-02 · API-08 · FN-05 · BR-PACK-08 · AT-07/08 |
| US-05 finish | P-02 · API-10 · FN-07 · BR-PACK-09 · AT-09/10 |
| US-06 reopen | P-02 · API-09/11 · FN-06/08 · BR-PACK-10 · AT-11 |
| US-07 cancel | P-02 · API-12 · FN-09 · BR-PACK-12 · AT-12 |
| US-08 DN | P-02 · API-13 · FN-10 · BR-PACK-11 · XT-03 |
| BR-13 print | P-03 · API-14/15 · ENG-02 · AT-13/14 |
| BR-15 audit | P-04 · API-16 · FN-11 · AT-15 |
| BR-16 notify | outbox · NTF brief · XT-04 |

Stories 8/8 · Rules 16/16 · confirmed edges 10/10; unresolved contracts routed to OQs.
