# UAT Lite Audit — F-WH-STKTRF

- Source MD: 53 cases.
- Retained for end users: 16 cases.
- Retained IDs: TC-A01, A02, A03, A04, A05, A06, A08, A09, V05, V13, V16, P03, L02, L04, L05, L06 (16 cases).
- Steps were translated to plain Thai and merged only where navigation was atomic; all visible decision points remain.

## Drop ledger

- TC-V01..V04, V06..V12, V14..V15, V17..V21: repetitive validation variants; representative high-risk validations retained.
- TC-P01, P02, P04..P06: require identity/config switching not exposed in final prototype; covered by AI tests.
- TC-L01, L03: list permutations/empty data depend on seed; retained indirectly through L02/L04.
- TC-C01..C05: concurrency/injection cases are system/AI tests.
- TC-X01..X06: integration collector/simulation required; system/AI tests.
- TC-A07: cancellation is covered by lifecycle and PM/BA review; Lite set prioritizes receive/reversal exceptions.

Expected values were rewritten to avoid prototype seed counts and to refer to actual configured document/item/master data.
