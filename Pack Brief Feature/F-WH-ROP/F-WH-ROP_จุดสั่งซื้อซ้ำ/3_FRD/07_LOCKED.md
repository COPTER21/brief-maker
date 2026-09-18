# 07_LOCKED · F-WH-ROP

## 7.0 Immutable scope inheritance
LOCK-01 console/master only; LOCK-02 exact configurable Item×Warehouse thresholds/effective version; LOCK-03 NC external rule and PR soft-link mock; LOCK-04 QHold excluded available, stock read-only; LOCK-05 no cross-lane transaction completion; LOCK-06 HTML freeze after S3, change requires S3a–S3c and html-to-frd-sync. Source `0_DIRECTION/_SCOPE_LOCK.md`. No lock overridden.

## Decisions and assumptions
LD-01 current HTML routes `#/records`, `#/history`, `#/settings`; no wizard. LD-02 ROP PR boundary uses policy min, NC candidate independent of ROP trigger. LD-03 append-only policy/event, immutable source stock. LD-04 tenant-local effective date and decimal precision require owner validation. `[ASSUMED]` OQ-ROP-01–07 with owners are in BRD §15 and HANDOFF; no default is stakeholder signoff. Dev must not implement W3 PR or NC delivery in ROP. If HTML changes, compare frozen hash and rerun sync/gates.
