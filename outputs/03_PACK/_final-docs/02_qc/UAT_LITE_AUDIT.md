# UAT Lite Audit — F-WH-PACK

- AI MD baseline: 40 cases / 101 steps
- Kept for human UAT: 19 cases / 43 steps
- Mode: Lite; retained IDs unchanged

## Drop ledger

- TC-Q02, Q04, Q05 — idempotency/wave contract/Transfer gate ต้องใช้ fixture หรือเป็น contract-level
- TC-P03 — covered by TC-P02 second step
- TC-P06 — UOM permutation; AI/API test retained
- TC-P08 — numeric boundary repetition; AI test retained
- TC-P10..P14 — special flags/master snapshot/weight failure/override mostly seed or backend dependent; core visible weight covered in pack flow
- TC-L04, L05, L07 — lead/DN contract and shipped lock require unavailable downstream/seed; AI test retained
- TC-D03 — immutable audit/version validation is system-oriented; user-facing print covered by D01/D02
- TC-U01 — lead breadth/export is administrative regression; core permissions covered by U02/U03
- TC-X01..X05 — simulate/concurrency/outage/cross-module cases; not suitable for end-user manual run

## Merge notes

- Q03 merged search, reset and warehouse filter into 3 human-readable steps.
- P04 merged valid custom name/tare entry and submit into one step; blank validation remains separate.
- P05 keeps baseline capture before delta comparison.
- L06 keeps blank-reason validation and successful cancel in one acceptance case.
- U04 merges keyboard/Esc/responsive checks while preserving each visible checkpoint.

No case was silently removed; AI coverage remains in `testcase_qa/testcases-F-WH-PACK.md`.
