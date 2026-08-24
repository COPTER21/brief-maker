# 07_LOCKED_DECISIONS — F-WH-DN Delivery Note

## §7.0 Imported Scope Lock

| LOCK | Immutable decision |
|---|---|
| LOCK-01 | work only under `outputs/17_Delivery-Note`; source pack untouched |
| LOCK-02 | preserve seed UI unless a necessary correction is identified |
| LOCK-03 | reference combine requires same source type, customer and ship-to |
| LOCK-04 | Stock Transfer is real in-scope and never syncs Sales Order |
| LOCK-05 | Manual create is separate from Reference create |
| LOCK-06 | Manual DN can move to all statuses only with a reason every time |
| LOCK-07 | Manual DN has no automatic GI/source sync |
| LOCK-08 | assignee is company Employee only and has no manual entry |
| LOCK-09 | manual driver needs first/last/phone; manual vehicle needs plate |
| LOCK-10 | Reference dispatch is the Goods Issue trigger |
| LOCK-11 | return/cancel after GI reverses before restoring queue/source |
| LOCK-12 | failed attempt numbering begins at 1 |

## §7.1 Architecture decisions

| LD | Decision |
|---|---|
| LD-01 | FULL pack due to multi-state and multi-module transactional flow |
| LD-02 | Reference and Manual use separate mutation functions and guards |
| LD-03 | cross-module writes use contracts/outbox, never foreign-table writes |
| LD-04 | optimistic concurrency and idempotency are conservative AI defaults pending BA/architect confirmation |
| LD-05 | document number/snapshot and notification policies remain centrally configured |

## §7.2 Functions cut / deviations

No HTML-standard conflict or scope drift found. Real 3PL, route optimization, mobile e-POD, automatic freight/Credit Note and master maintenance are excluded, not silently specified.

