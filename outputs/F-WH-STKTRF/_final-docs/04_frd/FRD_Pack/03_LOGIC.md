# 03_LOGIC — F-WH-STKTRF

## 3.1 Scope-local functions

| ID/code | Purpose | Input → output | Side effects |
|---|---|---|---|
| FN-01 `queryTransfers` | filter/sort/page list and KPI | query, actor → page | none |
| FN-02 `createTransferDraft` | create/duplicate editable draft | command → transfer | insert header/lines/audit |
| FN-03 `getTransferDetail` | build tabs and allowed actions | id, actor → detail | none |
| FN-04 `updateTransferDraft` | update draft only | id, version, patch → transfer | update draft/audit |
| FN-05 `submitTransfer` | validate, number, freeze approval chain | id, approvers → pending transfer | doc number, approval/audit |
| FN-06 `actOnTransferApproval` | sequential approve/reject | action → state | approval/audit/notify |
| FN-07 `executeShipment` | direct move or source→transit | id, actor → movement result | append movement/state/audit |
| FN-08 `receiveTransfer` | receive committed remaining only | rows, actor → receipt result | append receipt/movement/state |
| FN-09 `returnTransferToSource` | return remaining transit quantity | reason → returned state | append reverse-route movement |
| FN-10 `requestShortageWriteOff` | stage write-off and chain | qty, reason, files, approvers → pending | approval/attachment/audit |
| FN-11 `actOnShortageApproval` | advance chain; final write-off only | action → state | final movement/state/audit |
| FN-12 `cancelTransfer` | cancel pre-movement | reason → cancelled | state/audit |
| FN-13 `createTransferReversal` | create approval-pending opposite transfer | original, reason, approvers → reversal | insert transfer/lines/approval |
| FN-14 `getTransferDocument` | resolve stored/rendered print snapshot | id → document | optional store snapshot |
| FN-15 `attachTransferFile` | validate and store metadata | file, purpose → attachment | file/metadata/audit |

## 3.2 Engines

No new reusable CUBIC engine. Reuse external `ENG-DOC-NUM`, `ENG-DOC-STORE`, DOA, ENG-NOTIFY and the inventory-ledger posting contract. Mode derivation and remaining-quantity calculation stay scope-local because they are bound to TRF lifecycle.

## 3.3 API ↔ logic trace

API-01..15 call FN-01..15 respectively. Every mutation API-02,04..13,15 has exactly one transaction coordinator function above; that function may call external engines but the HTTP layer contains no business logic.

## 3.4 Core algorithms

`deriveMode`: source warehouse equals destination → internal; otherwise inter-warehouse and resolve one configured transit bin. `remaining = shipped - received - written_off - returned`; never trust browser totals. `postMovement` locks inventory rows, rechecks balance, appends immutable ledger rows, increments aggregate version, then commits state/audit atomically. Reversal replays completed original movement legs in reverse order/direction and links both documents.

## 3.5 Concurrency defaults

`[AI-DEFAULT]` optimistic versioning for documents, row lock during stock posting, unique idempotency key per actor/action/document, and unique `(reversal_of_id)` prevent duplicate reversal. A second concurrent receipt receives 409 and must reload actual remaining.

