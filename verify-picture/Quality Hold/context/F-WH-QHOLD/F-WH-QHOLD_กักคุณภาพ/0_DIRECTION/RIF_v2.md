# RIF v2 · F-WH-QHOLD · Quality Hold

**Type:** New Feature · **business owner:** Warehouse Product Owner · **confidence:** high for W4 §2 hold/release/ATP and declaration chips; medium for pending-hold timing, release reservation and DOA contract `[ASSUMED]`. Status: AI intake, not human approval.

## Business need and observable result
Warehouse must isolate a stock slice from promise/transfer while QC or an issue is reviewed, then release only through configured approval. A hold request or release request must show requested/approved/rejected state and the responsible person selection. onHand remains unchanged; ATP/transferable change according to quarantine projection only. Every state decision is auditable and idempotent.

## In scope
Select existing Item/Warehouse/location/lot soft refs and reason, source GRN QC mock or later issue; request partial/full hold; request partial/full release; DOA real-person slot picker from external policy response; mock external approval/rejection; pending-hold/pending-release reservation; computed ATP; read-only history; search/filter/sort. Declarations `doa,ntf,csq`.

## Out of scope
Create/approve GRN F079, actual sale/transfer, actual stock balance write, movement edit/delete, hardcoded approval chain, NC delivery, CSQ consequence stamp, document number/PDF, Pattern Q. No status label may imply a mock external workflow completed.

## Rules and source
| ID | Intent | Source/status |
|---|---|---|
| BR-01 | identified slice holds qty with lot/location flag | W4 §2; F088 CHECKLIST |
| BR-02 | hold/release via DOA slot people, no role ID chain | Golden Rule 3, W4 §2 |
| BR-03 | hold onHand but excluded ATP and transfer | W4 OQ-QH-01 `[ASSUMED]` |
| BR-04 | append-only quarantine events and no stock/movement mutation | Golden Rule 4 |
| BR-05 | partial hold/release and no release>held | `[ASSUMED]` Warehouse Product Owner |
| BR-06 | requested hold provisionally blocks ATP; requested release does not free ATP | `[ASSUMED]` Warehouse Product Owner |
| BR-07 | NC/NTF and CSQ declaration producer only | W4 §2 and chips |
| BR-08 | GRN QC and DOA decision are mocks, no downstream completion | W4 §2/5 |

## OQ/defaults/owners
OQ-QH-01 retained onHand/not ATP `[ASSUMED]`, Warehouse Product Owner + Inventory owner. OQ-QH-02 pending hold immediately quarantines `[ASSUMED]`, Warehouse Product Owner. OQ-QH-03 release reservation/pending timing `[ASSUMED]`, Warehouse Product Owner. OQ-QH-04 DOA policy response slot IDs, eligible people, decision event/idempotency `[ASSUMED contract]`, DOA owner. OQ-QH-05 exact onHand/reservedSales/held UoM precision and negative/overlap handling `[ASSUMED]`, Inventory owner. OQ-QH-06 GRN source and NC/CSQ event IDs `[ASSUMED contract]`, respective owners. No wait for owner response in this lane; HANDOFF must carry these.
