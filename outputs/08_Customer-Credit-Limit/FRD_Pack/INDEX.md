# FRD Pack Index — F-CUST-CL-001

- `00_OVERVIEW.md`: scope, dependencies, OQs, manifest
- `01_UI.md`: approved HTML-aligned UI behavior
- `02_API.md`: HTTP contracts and cross-module contracts
- `03_LOGIC.md`: functions, engines, API trace
- `04_DB.md`: ownership schema and classification
- `05_RULES.md`: validations, states, DOA rules
- `06_TESTS.md`: acceptance and cross-module tests
- `07_LOCKED_DECISIONS.md`: immutable decisions

## Verification report
Variant FULL: 9 files + index complete. All mutations trace to functions; all entities reference storage; UI actions map to APIs; DOA injection and scope locks are present; classifications are declared; manifest covers BRD stories/rules/edges. HTML alignment: 4 surfaces match the approved prototype anchors. **Verdict: PASS.**
