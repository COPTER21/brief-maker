# S1.8 planned coverage · F-WH-ROP

| Contract | Route | Control/handler target | Boundary |
|---|---|---|---|
| FN-01/S-01/06/08 | `#/policies` | canonical `.toolbar>.search-box`, sortable policy table, real stats | config list |
| FN-02/S-01/02/07 | `#/policies` drawer | Item/Warehouse searchable pickers, min/max/safety/effectiveDate, inline validation | versioned config |
| FN-03/S-06/07/08 | `#/suggestions` | effective policy exact pair/date lookup | no invented policy |
| FN-04/05/S-03/04/05/09 | `#/suggestions` | available snapshot, trigger boundary and computed qty | read-only inventory/QHold |
| FN-06/S-12 | `#/suggestions` | NC candidate/rule ref soft link | NC evaluation/delivery external |
| FN-07/S-10/11 | `#/suggestions` | PR mock payload/ack, replay/unavailable | no procurement implementation |
| FN-08/S-13 | `#/history` | immutable policy/suggestion/mock event list | append-only |

No Pattern Q, PR/PO creation, stock mutation, hardcoded NC threshold/recipient/channel or fabricated KPI. S3 must test handlers, not count rule text as implementation. Declarations `ntf,csq` require scoped briefs and FRD/TC trace.
