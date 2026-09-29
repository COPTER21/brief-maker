# TC ledger gate · F-WH-LOT

Verdict: PASS (document construction; browser execution NOT-CHECKED).

- AI manual TC and QA JSON share 59 unique IDs and one shared authored case source; MD is category-ordered, JSON is creation-ordered.
- Rule/error/permission/cross-lane ledger: 46/46 mapped to specific case IDs.
- 15 cases are marked system/mock, requiring controlled backend/mock harness; none asserts live downstream posting or delivery.
- TC-005 status filter: canonical select options are populated by fillFilters() from LOT state rows, which include กักอยู่; static code trace, not browser evidence.
- Browser render/interaction remains NOT-CHECKED due runner render tool failures; domain pure-function checks are separate.
