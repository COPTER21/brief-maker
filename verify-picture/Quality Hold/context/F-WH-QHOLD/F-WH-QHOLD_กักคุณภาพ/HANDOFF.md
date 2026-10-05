# DEVPACK HANDOFF · F-WH-QHOLD กักคุณภาพ
**W4B FULL · AI 100% no-vibe · 2026-09-14 · developer can start now.** This is an AI-reviewed specification and local HTML prototype, not a claim that real DOA, Inventory, GRN, NC or CSQ integrations run. Start with `3_FRD/INDEX.md`, then `7_CTX/CTX_F-WH-QHOLD.md`; BRD business intent in `2_BRD`, frozen HTML in `1_HTML`, 45-case TC and exact Thai QA HTML in `4_TC`, draft DOA/NTF/CSQ producer contracts in `5_DECLARATIONS`, UI brief in `6_UI_BRIEF`, direction and gate evidence in `0_DIRECTION`.

## Required behavior
Hold request30 against onHand100/reserved10 produces pendingHeld30/ATP60; external approval converts to activeHeld30/ATP60, rejection restores ATP90. Pending release12 leaves ATP60 and reserves releasable to18; approval activeHeld18/ATP72, rejection retains held30/ATP60. OnHand and movement ledger unchanged. DOA person slots come from effective policy, display actual named eligible people and persist person snapshots; UI DEMO decision controls are not production authorization. Append-only events and atomic replay/version guards prevent double effect. Sale/transfer availability check is contract only.

## Gate evidence / limits
FULL17 stages; S3a v9 static FAIL0/WARN2, isolated domain assertions13/13, FRD A–M13/13, 45 test cases with 44 source-ledger entries and 14 system/mock-only cases. Exact QA file `กักคุณภาพ HTML Testcase.html` built 1:1. Browser render/click/print not checked because capture dependencies absent; S3c/S6b/S6.5 WARN. No production permission, DB concurrency, real DOA/GRN/NC/CSQ/transfer result tested. Dev must validate these with owning teams and integration harness. HTML SHA recorded in `0_DIRECTION/_GATES/HTML_FREEZE_SHA256.txt`; any HTML edit requires S3a–c and html-to-frd-sync.

## ASSUMED / OQ owners
| OQ | Default | Owner |
|---|---|---|
| OQ-QH-01 | held remains onHand, excluded ATP | Warehouse Product Owner + Inventory owner |
| OQ-QH-02 | pending hold quarantines immediately | Warehouse Product Owner |
| OQ-QH-03 | pending release reserves held, no early ATP increase | Warehouse Product Owner |
| OQ-QH-04 | DOA slots/eligible named people/event keys mock contract | DOA owner |
| OQ-QH-05 | EA integer demo precision, real UoM/stock reference | Item/Inventory owner |
| OQ-QH-06 | GRN QC source, NC/NTF and CSQ event/catalog mock | GRN, Notification/NC, CSQ owners |
| OQ-QH-07 | maker/approver SoD/effective policy | DOA/Security owner |

## DIVERGENCE / dependencies
W4 held-not-ATP default is followed; pending timing is source-unspecified and tagged `[ASSUMED]`. GRN/RTV W3-LITE and DOA/NC/CSQ are soft refs/contracts; no downstream implementation here. No JE/Stock Adjustment behavior added. Owner-reviewed declarations may change event IDs/profile; no local delivery or 7C stamp. Developer may build QHold server now using FRD contracts, with these OQs in backlog rather than waiting for a human design handoff.
