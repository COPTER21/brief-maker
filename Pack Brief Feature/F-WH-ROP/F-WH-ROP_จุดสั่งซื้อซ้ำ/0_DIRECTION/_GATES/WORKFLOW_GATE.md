# S3b — ROP workflow/coverage gate

Verdict: PASS for authored workflow logic and isolated domain assertions; browser interaction is pending S3c/S6b. `DOMAIN_TEST.json` records 17/17 passing assertions against `_lane_tools/rop_inject.js` in a VM. It does not assert DOM rendering or a production API.

| Scenario | Actual route and handler | Evidence / limit |
|---|---|---|
| S-01 | `#/records` policy drawer → `ropSaveFromDrawer` → `ropSavePolicy` | version/event append; exact pair tested |
| S-02 | drawer → `ropValidate` | bounds reject negative/inversion; no append on error |
| S-03 | `#/history` → `ropEvaluatePair` | ITEM-103 WH-01 available=min=10, qty20 |
| S-04 | `#/history` → `ropEvaluatePair` | ITEM-104 WH-01 available9, qty21 |
| S-05 | `#/history` → `ropEvaluatePair` | ITEM-101 WH-02 available35>min25, qty0; PR disabled |
| S-06 | policy/evaluation exact Item×Warehouse | WH-01 and WH-02 policy refs differ |
| S-07 | `ropSavePolicy`, `ropPolicyActive` | future version not active before date; old version retained |
| S-08 | check pair drawer → `ropEvaluatePair` | ITEM-116 no policy, explicit `NO_POLICY` |
| S-09 | `ropEvaluatePair` | ITEM-101 WH-01 onHand20, held12, available8, qty22 |
| S-10 | suggestion drawer → `ropPreparePR` | mock PR payload/ack with pair, qty, version, key; no actual PR |
| S-11 | `ropPreparePR` | replay same key and unavailable retry path tested |
| S-12 | suggestion drawer → `ropNcCandidate` | external NC rule ref candidate; above-min candidate valid; no delivery claim |
| S-13 | `#/settings` event list/detail | saves/PR/NC append events; no edit/delete history controls; UI inspection only |

UI contracts: v9 shell; tabs directly below page-head; canonical filter block copied; Item/Warehouse master search menus; action buttons only in page-head/drawer; no hint/banner; policy and history are read-only where required. Policy history `policy.saved` detail shows historical version/effective date. Business rule BR-04 trigger uses configured min and available snapshot, while NC owns its own notification rule/threshold. PR and NC remain mock boundaries.
