# FRD · F-WH-QHOLD · กักคุณภาพ
2026-09-14 · AI-approved specification; production integration unverified. Sources: BRD §§1–18, RIF, PREBRIEF S-01–10, LOCK-01–08, frozen HTML SHA. Owner Warehouse Product Owner.

## Objective and boundary
Identify Item/Warehouse/location/lot stock slice; request partial hold/release with configured DOA persons; keep onHand and movement ledger immutable while ATP/transfer projection excludes quarantine. GRN QC source, DOA policy/decision, NC delivery, CSQ stamps and sale/transfer execution are external mock/TODO. No wizard. HTML tabs: รายการกัก, รออนุมัติ, ประวัติ.

## Status of evidence
Local JavaScript domain assertions 13/13 and v9 static audit FAIL0. Browser rendering and production server contract are NOT-CHECKED. `data-demo` approval buttons only simulate an incoming DOA event; local named-person catalog is fixture, not actual policy authority. Data fields classified in 04_DB. OQs in 07_LOCKED.
