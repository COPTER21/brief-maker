# S6.5 Coverage R2 · F-WH-ROP

**Verdict: WARN** — all source checklist/scenarios/BR/XT/LOCK are represented in frozen HTML handlers, FRD and TC ledger; actual browser render and external PR/NC/CSQ contracts remain not checked. No business BLOCK gap was found. This is coverage, not test execution.

| Item | HTML source evidence | FRD evidence | TC evidence | Result |
|---|---|---|---|---|
| WF-FN-01 list/filter/count | `#/records` `ropRows`+`fillFilters`+`renderTableOnly` | 08_COVERAGE_MANIFEST WF-FN-01 / 01_UI | TC-018, TC-048, TC-049, TC-050 | covered |
| WF-FN-02 versioned policy | `#/records` `ropOpenPolicy`+`ropSaveFromDrawer`+`ropSavePolicy` | 03_LOGIC FN-01/02; 05_RULES R-02/03 | TC-001, TC-003, TC-010, TC-039 | covered |
| WF-FN-03 active pair/date | `ropPolicyActive` | 03_LOGIC FN-03; 05_RULES R-01 | TC-008, TC-010, TC-033 | covered |
| WF-FN-04 availability/formula | `ropSnapshot`+`ropEvaluatePair` | 03_LOGIC FN-04/05; 05_RULES R-04/05 | TC-005, TC-006, TC-007, TC-009 | covered |
| WF-FN-05 suggestions/missing | `#/history` `ropSuggestions`+`ropCheckPair` | 01_UI / 05_RULES R-01/04 | TC-005, TC-007, TC-033 | covered |
| WF-FN-06 NC candidate | `ropNcCandidate`+`ropSendNC` | 02_API API-05; 03_LOGIC FN-07; NTF brief | TC-015, TC-044, TC-046 | covered |
| WF-FN-07 PR mock | `ropPreparePR`+`ropSendPR` | 02_API API-04; 03_LOGIC FN-06 | TC-012, TC-013, TC-014, TC-041 | covered |
| WF-FN-08 event history | `#/settings` `ropEvents`+`openView` | 02_API API-06; 03_LOGIC FN-08 | TC-011, TC-040, TC-047 | covered |
| S-01 policy drawer save | PREBRIEF route/handlers in WORKFLOW_GATE | 08_COVERAGE_MANIFEST row; 05_RULES | TC-001, TC-036 | covered |
| S-02 ropValidate error | PREBRIEF route/handlers in WORKFLOW_GATE | 08_COVERAGE_MANIFEST row; 05_RULES | TC-003, TC-004 | covered |
| S-03 ITEM-103 equality qty20 | PREBRIEF route/handlers in WORKFLOW_GATE | 08_COVERAGE_MANIFEST row; 05_RULES | TC-005 | covered |
| S-04 ITEM-104 below qty21 | PREBRIEF route/handlers in WORKFLOW_GATE | 08_COVERAGE_MANIFEST row; 05_RULES | TC-006 | covered |
| S-05 ITEM-101 WH-02 above qty0 | PREBRIEF route/handlers in WORKFLOW_GATE | 08_COVERAGE_MANIFEST row; 05_RULES | TC-007, TC-031 | covered |
| S-06 exact warehouse policy | PREBRIEF route/handlers in WORKFLOW_GATE | 08_COVERAGE_MANIFEST row; 05_RULES | TC-008 | covered |
| S-07 future active version | PREBRIEF route/handlers in WORKFLOW_GATE | 08_COVERAGE_MANIFEST row; 05_RULES | TC-010, TC-032 | covered |
| S-08 ITEM-116 NO_POLICY | PREBRIEF route/handlers in WORKFLOW_GATE | 08_COVERAGE_MANIFEST row; 05_RULES | TC-018, TC-033 | covered |
| S-09 onHand20 held12 available8 | PREBRIEF route/handlers in WORKFLOW_GATE | 08_COVERAGE_MANIFEST row; 05_RULES | TC-009 | covered |
| S-10 PR mock payload | PREBRIEF route/handlers in WORKFLOW_GATE | 08_COVERAGE_MANIFEST row; 05_RULES | TC-012 | covered |
| S-11 PR replay/unavailable | PREBRIEF route/handlers in WORKFLOW_GATE | 08_COVERAGE_MANIFEST row; 05_RULES | TC-013, TC-014 | covered |
| S-12 NC candidate envelope | PREBRIEF route/handlers in WORKFLOW_GATE | 08_COVERAGE_MANIFEST row; 05_RULES | TC-015 | covered |
| S-13 append-only event detail | PREBRIEF route/handlers in WORKFLOW_GATE | 08_COVERAGE_MANIFEST row; 05_RULES | TC-011, TC-040 | covered |
| BR-01 | 03_LOGIC demo analogue / UI entry where applicable | 05_RULES R-01 | TC-001, TC-008, TC-010, TC-032, TC-036, TC-037, TC-039 | covered |
| BR-02 | 03_LOGIC demo analogue / UI entry where applicable | 05_RULES R-02 | TC-001 | covered |
| BR-03 | 03_LOGIC demo analogue / UI entry where applicable | 05_RULES R-03 | TC-002, TC-003 | covered |
| BR-04 | 03_LOGIC demo analogue / UI entry where applicable | 05_RULES R-04 | TC-005, TC-006, TC-007, TC-028, TC-031, TC-032 | covered |
| BR-05 | 03_LOGIC demo analogue / UI entry where applicable | 05_RULES R-05 | TC-009, TC-017, TC-029, TC-030 | covered |
| BR-06 | 03_LOGIC demo analogue / UI entry where applicable | 05_RULES R-06 | TC-015, TC-044, TC-045, TC-046, TC-060 | covered |
| BR-07 | 03_LOGIC demo analogue / UI entry where applicable | 05_RULES R-07 | TC-012, TC-041, TC-042 | covered |
| BR-08 | 03_LOGIC demo analogue / UI entry where applicable | 05_RULES R-08 | TC-011, TC-013, TC-016, TC-039, TC-040, TC-043, TC-047 | covered |
| DECL-NTF | `ropNcCandidate` local envelope, no delivery | 02_API cross-module + 05_RULES; NTF Markdown/JSON draft | TC-015/044/046/060 | WARN catalog unavailable, contract owner needed |
| DECL-CSQ | no local engine emit; FN-02 policy event source | 02_API cross-module + 05_RULES; CSQ Markdown/JSON draft | TC-059 sys only | WARN central contract unavailable |
| DECL-DOA | N/A; no ROP approval UI | BRD §4/15 owner OQ, not a declared chip | TC-055–058 backend permission separate | N/A |
| DECL-DOCCFG | N/A; policy refs/version not document numbering | 07_LOCKED scope | no document-number case | N/A |
| SURFACE-list | `#/records` canonical filter + `ropRows` | 01_UI | TC-018/048–050 | covered |
| SURFACE-drawer | `ropOpenPolicy`, `ropOpenCheck`, `openView` | 01_UI | TC-001/033/040 | covered |
| SURFACE-error/empty | `ropValidate`, `ropCheckPair`, `renderTableOnly` | 05_RULES | TC-019–025/033/050 | covered |
| SURFACE-mock | `ropSendPR`, `ropSendNC` | 02_API/03_LOGIC/06_TESTS | TC-012–016/041–047 | covered to mock only |
| SURFACE-visual | official renderer unavailable twice | 01_UI states NOT-CHECKED | no executed screenshot | WARN |

## R2 numerical checks
- Workflow capabilities: 8/8 mapped to actual authored handler, FRD section and TC IDs.
- PREBRIEF scenarios: 13/13; BRD rules: 8/8; 05_RULES R-01–08: 8/8; XT: 5/5; LOCK: 6/6.
- TC source: 60/60 IDs in Markdown and QA mirror; 82/82 ledger items map to cases; 20 cases are system/mock-only and have `sys:true`.
- Declaration chips: NTF and CSQ briefs present; both drafts await central catalog/contract owner and are not registered. No DOA/DOCCFG chip or signal for ROP.
- R1 to R2: S3 gate source behavior remained frozen after calendar-date correction. S5 manifest gained explicit workflow-to-logic mapping and S6a ledger gained matching WF-FN traces; no HTML edit after final freeze.
- Exclusions respected: actual W2-PUR-LITE PR creation, NC delivery, CSQ registration/stamp and stock/movement mutation have no success claim or business implementation.

## Remaining validation work
1. Browser desktop/table/drawer visual and real click-flow; Playwright absent in environment.
2. Production server access, concurrency, decimal/UoM and snapshot freshness; local VM does not prove these.
3. NC/CSQ/Procurement owner contract and event catalog confirmation; mocks only.
