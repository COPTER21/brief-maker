# CTX — F-WH-STKTRF: Stock Transfer

> **derived from:** FRD F-WH-STKTRF v1.0 · **generated:** 2026-09-17
> **module:** Warehouse · **status:** active
> ⚠ Derived artifact — source of truth is `FRD_Pack/`; regenerate when the FRD changes.

---

## 1. Summary

Stock Transfer controls movements between bins and warehouses. Same-warehouse transfers post one direct movement; cross-warehouse transfers post source→transit then transit→destination and close only after destination receipt. The feature supports approval, partial receipt, shortage write-off approval, return, cancellation before movement, and append-only reversal. It never edits/deletes committed movement and does not post a real JE in this release.

## 2. Data Contract

### Entities

| Entity | PK | Cross-feature fields | Notes |
|---|---|---|---|
| `stock_transfer` | `id` | `code`, `status`, `mode`, warehouse/transit refs+snapshots, `creator_id`, totals, `shipped_by/at`, `reversal_of_id`, `accounting_status`, `version` | Code nullable until submit; reversal self-link unique |
| `stock_transfer_line` | `id` | `transfer_id`, item/UOM/bin refs+snapshots, requested/shipped/received/written_off/returned qty, `unit_cost_snapshot` | Quantity invariant applies |
| `stock_transfer_approval` | `id` | `transfer_id`, `approval_type`, `step_no`, `assignee_id`, `status`, actor/time, `doa_policy_snapshot` | Frozen approval snapshot |
| `stock_transfer_receipt` | `id` | `transfer_id`, `receipt_no`, receiver/time, destination bin, qty | Multiple receipts allowed |
| `stock_transfer_attachment` | `id` | `transfer_id`, purpose, storage key, file metadata, uploader/time | Evidence/document authorization required |
| `inventory_movement` | `id` | transfer/line refs, movement type, source/destination, qty/cost, reversal link, posting status | Append-only |
| `stock_transfer_audit` | `id` | transfer, event/from/to state, actor snapshot, reason, time, correlation | Append-only |

### States

| Field | Values | Owner |
|---|---|---|
| `status` | `draft`, `pending_approval`, `approved`, `moved`, `in_transit`, `partial`, `closed`, `closed_diff`, `returned`, `cancelled`, `reversed` | F-WH-STKTRF |
| approval status | `pending`, `approved`, `rejected`, `cancelled` | DOA snapshot/action contract |
| accounting status | `pending_posting` in this release | future W5 |

### Relationships and invariant

- Transfer 1—N lines, approvals, receipts, attachments, audit and movement links.
- Transfer 0—1 reversal transfer through `reversal_of_id`.
- Item, UOM, warehouse and bin are soft references with immutable display snapshots.
- Per line: shipped = received + written off + returned + in transit.

## 3. API Surface

| Method | Endpoint | Purpose | Key input |
|---|---|---|---|
| GET | `/api/v1/stock-transfers` | list/filter/page/KPI | search, state, warehouse, creator, reason, date |
| POST | `/api/v1/stock-transfers` | create/duplicate draft | header, lines, attachments |
| GET | `/api/v1/stock-transfers/{id}` | detail and allowed actions | actor context |
| PATCH | `/api/v1/stock-transfers/{id}` | edit draft | version, patch |
| POST | `/{id}/submit` | number document and freeze DOA | real-person approver selections |
| POST | `/{id}/approval-actions` | approve/reject current slot | action, reason/note |
| POST | `/{id}/ship` | direct move or source→transit | version, actor |
| POST | `/{id}/receipts` | full/partial receipt | per-line qty/bin/discrepancy |
| POST | `/{id}/return-to-source` | return remaining transit | reason |
| POST | `/{id}/shortage-requests` | create write-off approval request | qty, reason, evidence, approvers |
| POST | `/{id}/shortage-actions` | act on shortage chain | action, note |
| POST | `/{id}/cancel` | cancel before movement | reason |
| POST | `/{id}/reversals` | create approval-pending reversal | reason, approvers |
| GET | `/{id}/document` | retrieve document metadata/snapshot | document id |
| POST | `/{id}/attachments` | upload attachment/evidence | file, purpose |

All mutations use `Idempotency-Key` and `If-Match`; stale/invalid transitions return 409.

### Events emitted

The notification declaration registers the `transfer_*` names below. FRD 02_API currently uses shorter `trf.*` contract names for six matching events; the mapping is explicit here so consumers do not treat them as separate business events.

| Declared event | FRD 02_API name | Trigger | Payload keys |
|---|---|---|---|
| `transfer_shipped` | `trf.shipped` | approved→in_transit | transfer, code, warehouses, shipped totals |
| `transfer_moved_intra` | `[not documented]` | approved→moved | transfer, warehouse, line count |
| `transfer_partially_received` | `trf.partial` | in_transit→partial | shipped, received, remaining |
| `transfer_received` | `trf.received` | in_transit/partial→closed | destination and receipt totals |
| `transfer_shortage_written_off` | `trf.shortage` | final shortage approval posts write-off | shortage qty/value/reason |
| `transfer_returned_to_source` | `trf.returned` | remaining stock returned | source bins and reason |
| `transfer_in_transit_aging` | `[not documented]` | central aging rule fires | remaining and aging days |
| `transfer_reversed` | `trf.reversed` | reversal completes | original and reversal refs |
| `transfer_cancelled` | `[not documented]` | pre-movement cancellation | actor and reason |

DOA owns `doa_pending`, `doa_result`, and `doa_escalate`; this feature must not duplicate them.

## 4. Shared Rules

| Rule | Contract | Impact |
|---|---|---|
| LK-3 | Cross-warehouse stock always passes through configured transit; shipment is not receipt | Inventory/reporting/location consumers |
| LK-4 | Destination confirmation closes the cross-warehouse transfer | Warehouse receiving and reporting |
| LK-5 | DOA slots resolve to real people; no hardcoded feature chain | DOA/My Approval |
| LK-6 | Number and snapshot only through document engines | F-DOCCFG/document consumers |
| LK-8 | Movement is append-only; corrections are compensating reversal rows | Inventory/audit/accounting |
| LK-9 | Location model is inherited from Putaway; this feature cannot redefine it | Location Master/Putaway |
| BR-14 | Shipper and receiver differ; receiver belongs to destination warehouse | IAM/warehouse authorization |
| BR-18 | Shortage write-off requires reason, evidence, full second approval chain, and shipper exclusion | DOA/audit/accounting |
| BR-24 | Real JE posting is disabled; movement exposes `pending_posting` only | W5 accounting |
| BR-27 | Aging thresholds/channels are central configuration, not feature code | ENG-NOTIFY/NC rules |
| BR-28 | Retired master data must not break old documents because snapshots persist | Master-data owners |

## 5. Integration

- **Depends on:** Location Master/Putaway location contract; inventory ledger; DOA; F-DOCCFG; ENG-NOTIFY.
- **Depended by:** inventory/transit reporting, audit, and future W5 accounting consume transfer/movement state.
- **Declarations:** DOA—transfer and shortage actions; NTF—nine business events; DOCCFG—`TRF`, annual Gregorian pattern, global default, final snapshot. CSQ is referenced by source contract but was not generated in this selected declaration run.
- **Engine hooks:** `ENG-DOC-NUM.next`, `ENG-DOC-STORE.store`, DOA resolve/action, `ENG-NOTIFY.emit`, inventory-ledger append.
- **Future hook:** JE posting only after an approved W5 contract.

---

*trace: §2 ← FRD 04_DB · §3 ← FRD 02_API + NTF brief · §4 ← FRD 05_RULES/07_LOCKED · §5 ← FRD/BRD/declaration briefs*
