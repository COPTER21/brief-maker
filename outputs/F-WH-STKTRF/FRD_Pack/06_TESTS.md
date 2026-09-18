# 06_TESTS — F-WH-STKTRF

## 6.1 Acceptance flow tests

| ID | Scenario | Expected |
|---|---|---|
| AT-01 | Same warehouse, approve, `ย้ายสินค้า` | one direct movement; status moved; no receive action |
| AT-02 | Different warehouses, approve | transit location shown read-only; shipment required before receipt |
| AT-03 | Confirm `ส่งออกจากต้นทาง` | CUBE modal; one source→transit movement; status in_transit |
| AT-04 | Receive all remaining | transit→destination movement; remaining zero; closed |
| AT-05 | Receive part and choose wait | only actual quantity moves; remaining shown; status partial |
| AT-06 | Request shortage then approve sequentially | no write-off before last slot; final write-off closes/keeps partial by remaining |
| AT-07 | Destination returns remaining | transit→original source movement; returned; not shortage |
| AT-08 | Cancel pre-movement; reverse completed document | cancel posts no movement; reversal starts pending approval and original changes only after completion |
| AT-09 | Submit with DOA slots | every slot shows real person; missing slot blocks submit |
| AT-10 | Transit tabs/KPI | in-transit and my-receive queues reflect committed state |

## 6.2 Validation tests

VT-01..VT-21 execute each BRD V-01..V-21 once with invalid input/state and once at its valid boundary. Expected message is the exact Thai text in BRD §9.2/HTML. FN-40 rendered negative must remain visible and actionable.

## 6.3 Edge tests

EC-01..EC-21 execute each confirmed BRD edge case. Required concurrency cases: two shipments against one bin, two receipts on one document, double-click mutation within busy window, repeated idempotency key, stale `If-Match`, and repeat reversal.

## 6.4 Permission tests

- Source officer cannot ship unless assigned supervisor permission.
- Shipper cannot receive the same cross-warehouse document.
- Non-destination actor sees disabled receive with a visible reason.
- Shipper cannot approve shortage write-off.
- Non-current DOA assignee cannot act.
- Read-only accounting/audit cannot mutate.

## 6.5 Data/invariant tests

After every movement assert the quantity invariant, append-only row count, two-way reversal links, snapshot survival after master retirement, unique code allocation only on submit, and no actual JE posting.

## 6.6 UI fidelity spot checks

Routes match HTML; wide tables scroll horizontally; line-editor columns align; upload control accepts file selection; modal cancel causes no mutation; Esc follows the overlay chain; disabled tooltip is visible; shipment does not call native browser confirm.

## 6.7 API/logic tests

Each API-01..15 calls FN-01..15. Mutation errors use the catalog; transaction rollback leaves neither partial movement nor partial state. Attachment access is signed and permission-scoped.

## 6.8 Definition of done

All BRD stories/rules/validations/confirmed edges pass; zero console errors; all 61 FN hooks remain covered; approval/document/notification declaration keys resolve in integration environment.

## 6.9 Cross-module tests

1. DOCCFG allocates one `TRF-YYYY-NNNN` on first submit and stores document snapshots.
2. DOA returns real-person slots and owns its pending/result notifications.
3. Business events reach ENG-NOTIFY exactly once with central channel preference.
4. Inventory ledger posts atomically and exposes transit stock to reporting.
5. Cancellation before movement emits no stock entry; return/reversal creates compensating entries.
6. W5 adapter remains uncalled; UI/audit show `รอลงบัญชี`.

