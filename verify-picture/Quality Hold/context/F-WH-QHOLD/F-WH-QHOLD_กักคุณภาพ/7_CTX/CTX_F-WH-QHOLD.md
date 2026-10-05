# Developer Context Pack · F-WH-QHOLD กักคุณภาพ
Source: FRD 00–08, BRD, frozen HTML SHA, 45-case TC. AI 100% no-vibe; dev may start now on server-owned contracts. Local HTML is prototype/domain fixture, not live Warehouse/DOA integration.

## Build order
1. Inventory-sourced slice read and tenant/warehouse RLS; onHand/reservedSales read-only. 2. QHold projection/version and decimal/UoM capacity validation. 3. External DOA effective policy lookup, required actual-person slots and maker/approver SoD. 4. Atomic request reservation/event/outbox/idempotency. 5. Signed DOA decision adapter with sourceEventId/version guard. 6. ATP/transfer availability read-only contract. 7. History/audit, NC/CSQ declarations after owner confirmation. 8. UI hookup and 45-case QA.

## Invariants
Pending hold provisionally blocks ATP `[ASSUMED]`; active held plus pending held excluded while onHand and movements remain unchanged. Pending release reserves held and never frees ATP until approved. Repeated request/event returns prior result or conflict; no double ATP rise. Append-only history. No sale/transfer, GRN/RTV, NC delivery, CSQ registration/stamp, JE or stock adjustment implementation in this feature.

## Contract entry points
FRD API-01 slices, API-02 DOA policy, API-03 requests, API-04 adapter-only decisions, API-05 pending, API-06 events, API-07 availability. Error catalog in FRD 05_RULES. DB `qh_slice_projection`, `qh_request`, `qh_event`, `qh_outbox` in 04_DB. Selected person snapshots Restricted PII; strip names from NC/CSQ envelope. Demo-only policy/decision controls tagged `data-demo` and DEMO badge; replace with real adapters, not client authorization.

## Tests and handoff gates
13/13 isolated domain assertions; 45 detailed cases, 14 backend/mock-only. Frozen HTML v9 audit FAIL0/WARN2. No browser rendering, responsive click/print, production security/concurrency or external integration was executed. Those are required implementation checks. Capture failure was PIL/system and Playwright/bundled absence. Verify exact QA file `กักคุณภาพ HTML Testcase.html` and use case ledger; no test beyond mock payload/ack/projection/unchanged stock for external services.

## Decisions pending owners
OQ-QH-01 held onHand/no ATP — Warehouse Product Owner + Inventory; OQ-QH-02 pending hold timing — Warehouse Product Owner; OQ-QH-03 pending release reservation — Warehouse Product Owner; OQ-QH-04 DOA slots/event/idempotency — DOA owner; OQ-QH-05 UoM precision and references — Inventory/Item; OQ-QH-06 GRN/NC/CSQ payload/catalog — respective owners; OQ-QH-07 SoD/effective policy — DOA/Security. Defaults already used and tagged `[ASSUMED]`; owner decisions can be scheduled without blocking developer kickoff.
