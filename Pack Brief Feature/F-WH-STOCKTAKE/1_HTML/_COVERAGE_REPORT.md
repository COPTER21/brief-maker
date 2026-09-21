# S3b coverage — Stocktake

Verdict **WARN** pending browser state flow, no missing contract element in static UI. Generic graph validator V2 calls both nodes orphan because W4-LITE graph deliberately has no internal edges; external dependencies and CONTEXT_PACK are actual scope. DIVERGENCE-GRAPH-01 owner pack maintainer, graph unchanged.

| Obligation/FN/scenario | Route / UI handler evidence | Verdict |
|---|---|---|
| FN01–02, S05/S09 | `#/create` Warehouse/Location searchable `combo` picker; `#/sheets` Item/Location snapshot list | ✓ mock soft refs |
| FN03–04, S12/S13 | `freezeRound` blocks overlapping selected scope, captures `freezeAt`, immutable snapshot and scoped log; no global freeze | ✓ [ASSUMED] |
| FN05–07, S01/S04 | `#/sheets` `openAssign`, real person picker, `recordCount`, zero accepted/blank and negative rejected; counter hides snapshot | ✓ |
| FN08–09, S02/S03/S07/S08 | `inventoryConfig.varianceThreshold/effectiveDate`, `submitCount` requires independent recount above threshold | ✓ mock |
| FN10, S06 | `#/variance` `openDoa`, `.slot-row` actual person, approve/reject reason and `audit` | ✓ |
| FN11, S10/S11 | `handoff` produces W3-LITE mock ref and scope-release event, no Item qty mutation | ✓ [ASSUMED contract] |
| FN12 | PREBRIEF §6/BRD boundary; no Cycle Count route or logic in HTML | ✓ boundary |
| S01–S13 | Paths above; no source-less or positive stock mutation | ✓ static |

Declarations doa+csq 2/2 match FEATURE_LIST_ALL chip; no NTF/DOCCFG/PDFDOC invented. #104 tabs and #105 DEMO harness visible; #106 list toolbar uses authoritative block. WARN: freeze engine and Adjustment acknowledgment are mock integration contracts; runtime browser scenarios in S3c determine final gate.
