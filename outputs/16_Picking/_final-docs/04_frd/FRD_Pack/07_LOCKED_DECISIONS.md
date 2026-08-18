# 07_LOCKED_DECISIONS — F-WH-PICK Picking

## §7.0 Scope Lock — IMMUTABLE

| LOCK | Decision | Status |
|---|---|---|
| 01 | Wave S5 | aligned |
| 02 | User entry is create Pick | aligned |
| 03 | Warehouse/Location from real master; prototype mock | aligned |
| 04 | one location one lot | aligned |
| 05 | ERP/PREBRIEF allocation standard | aligned |
| 06 | ERP-standard exception paths | aligned |
| 07 | Picking permission model | aligned |
| 08 | assignee list shows everyone initially | aligned |
| 09 | assigned picker can operate their work | aligned |
| 10 | pickup still Packing→DN; DN adjusts later | aligned |
| 11 | SO-only Pick queue/source | aligned |
| 12 | remove download-like replenishment icon from row action | aligned |

No scope drift found.

## §7.1 Engineering decisions

- LD-01 optimistic concurrency and Idempotency-Key are conservative defaults pending implementation review
- LD-02 allocation algorithm is pure `pick-allocation-engine` candidate; registration waits for Architect/OQ-03
- LD-03 Inventory/Sales/Packing are accessed through contracts; Picking never writes another module table directly
- LD-04 ENG-NOTIFY owns channel/preferences/templates; feature emits only declared events
- LD-05 custom state actions use POST action endpoints for semantic clarity

## §7.2 Deferred decisions

OQ-01..06 in `00_OVERVIEW`; none expands scope automatically. No convention deviation beyond semantic POST actions.
