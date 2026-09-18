# 08_COVERAGE_MANIFEST · F-WH-ROP

| Source | FRD destination | TC route / assertion |
|---|---|---|
| US-01, S-01, BR-01/BR-02 | 01_UI records; 02_API API-02; 03_LOGIC FN-01/02/03; 05_RULES R-01/02 | policy save/version/effective cases |
| US-02, S-02, BR-03 | 02_API API-02 errors; 03_LOGIC FN-01; 05_RULES R-03 | blank/negative/nonfinite/date cases |
| US-03, S-03, BR-04 | 03_LOGIC FN-05; 05_RULES R-04 | equality qty20 |
| US-04, S-04, BR-04 | 03_LOGIC FN-05 | below qty21 |
| US-05, S-05, BR-04/06 | 03_LOGIC FN-05/07 | above qty0, no PR, NC candidate separate |
| S-06, BR-01 | 03_LOGIC FN-03 | WH isolation |
| S-07, BR-01/BR-02/08 | 03_LOGIC FN-02/03/08; 04_DB | future/current version and event |
| S-08 | 02_API NO_POLICY; 05_RULES R-01 | missing pair explicit |
| US-06, S-09, BR-05 | 03_LOGIC FN-04/05; 05_RULES R-05 | onHand20 held12 available8 |
| US-07, S-10/S-11, BR-07/08 | 02_API API-04; 03_LOGIC FN-06 | PR mock payload/replay/unavailable |
| S-12, BR-06/08 | 02_API API-05; 03_LOGIC FN-07 | NC envelope/replay only |
| US-08, S-13, BR-08 | 01_UI settings; 02_API API-06; 03_LOGIC FN-08 | append-only detail/no edit |
| All §10 edges | 05_RULES error matrix; 06_TESTS AT/XT | negative/error/permission and cross-module mock |
| LOCK-01–06, OQ-ROP-01–07 | 07_LOCKED; 00_OVERVIEW; HANDOFF | lock/hash/assumption review |

A–M mechanical gate checks and unresolved visual warning are recorded in `_lane/FRD_GATE_A_M.md`; no local browser or backend integration is claimed.

## Workflow capability registry vs FRD function registry
`0_DIRECTION/FUNCTION_CHECKLIST.md` FN-01–08 are workflow coverage IDs (`WF-FN-*` below); 03_LOGIC FN-01–09 are implementation function IDs with their own meanings. They are deliberately distinct and never used interchangeably.

| WF capability | HTML handler evidence | FRD functions/rules | TC |
|---|---|---|---|
| WF-FN-01 list/filter/stats | `ropRows`, `fillFilters`, `renderTableOnly`, `stats` | FN-09, R-01 | TC-018/048/049/050 |
| WF-FN-02 versioned policy | `ropOpenPolicy`, `ropSaveFromDrawer`, `ropSavePolicy` | FN-01/02, R-02/03 | TC-001/003/010/039 |
| WF-FN-03 active pair/date | `ropPolicyActive` | FN-03, R-01 | TC-008/010/033 |
| WF-FN-04 availability/formula | `ropEvaluatePair`, `ropSnapshot` | FN-04/05, R-04/05 | TC-005/006/007/009 |
| WF-FN-05 suggestions/empty | `ropSuggestions`, `ropCheckPair` | FN-05, R-01/04 | TC-005/007/033 |
| WF-FN-06 NC candidate | `ropNcCandidate`, `ropSendNC` | FN-07, R-06 | TC-015/044/046 |
| WF-FN-07 PR mock | `ropPreparePR`, `ropSendPR` | FN-06, R-07/08 | TC-012/013/014/041 |
| WF-FN-08 event history | `ropEvents`, `ropRows`, `openView` | FN-02/06/07/08, R-08 | TC-011/040/047 |
