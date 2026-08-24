# UAT Lite Drop Ledger — F-WH-DN

Source: `testcases-F-WH-DN.md` 50 cases. UAT Lite keeps 18 user-observable cases and drops 32 cases with reasons below. Kept IDs remain unchanged.

## Kept

TC-Q01, Q04, Q07, A01, A04, A06, L01, L02, L06, L10, L11, L12, L13, T02, M03, M05, U02, U04.

## Dropped

- TC-Q02,Q03,Q05,Q06,Q08 — duplicate list/create permutations or direct-route guards; core create/guard remains covered.
- TC-A02,A03,A05,A07,A08,A09 — duplicate lookup/validation permutations; Employee-only and both manual transport validations remain.
- TC-L03,L04,L05,L07,L08,L09,L14,L15 — detailed 3PL/tracking/POD/backorder permutations; primary lifecycle, failed, full POD and destructive paths remain for end users.
- TC-T01,T03,T04 — Transfer display/dispatch/reversal permutations; core real Transfer create/no-SO case remains.
- TC-M01,M02,M04,M06,M07 — Manual open/required/reason/isolation/terminal permutations; create and multi-status history cases cover the user workflow.
- TC-U01,U03 — read-only and print are already visible within retained lifecycle/POD cases; removed to keep Lite document short.
- TC-X01,X02,X03 — service simulation, concurrency, idempotency, outbox and failure injection cannot be performed by an end user.

Audit: MD 50 cases → UAT Lite 18 kept / 32 dropped. No new case was invented; retained IDs and business assertions come from the MD source.
