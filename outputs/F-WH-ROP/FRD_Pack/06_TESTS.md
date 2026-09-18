# 06 TESTS · F-WH-ROP

| AT | Scenario | Expected visual/contract result |
|---|---|---|
| AT-01 | save valid pair | new version; other warehouse unchanged |
| AT-02 | future/current versions | correct active version by date |
| AT-03 | safety>min | error below Safety; no event |
| AT-04 | min>max | error below Min; no event |
| AT-05 | negative/blank/nonfinite | field errors; drawer stays open |
| AT-06 | lead<0 or pack<1 | field error; no save |
| AT-07 | unknown master | require picker selection |
| AT-08 | F009 ATP already excludes hold | evaluator uses exact ATP |
| AT-09 | ATP=ROP | not triggered |
| AT-10 | ATP just below ROP | triggered |
| AT-11 | safety change | ROP and trigger outcome change |
| AT-12 | ADU=0 | ROP falls back to max(Min,Safety) |
| AT-13 | 30+5−8−0 | raw 27 |
| AT-14 | raw27 pack12 | suggested 36 |
| AT-15 | On-Order covers target | qty 0 and no Draft line |
| AT-16 | within 20% above ROP | Near status |
| AT-17 | no policy | separated card and prefilled add action |
| AT-18 | missing snapshot | unavailable, no side effects |
| AT-19 | schedule 06:00 | catalog run anchor |
| AT-20 | movement event | only affected pair evaluated |
| AT-21 | rerun same key | same result; event count unchanged |
| AT-22 | notify triggered | user sees success toast; NTF envelope complete |
| AT-23 | notify replay/failure | already-sent toast or retryable error, no duplicate |
| AT-24 | two low items same warehouse | one Draft with two lines |
| AT-25 | two warehouses | two Drafts |
| AT-26 | preferred vendors differ | still one Draft; suggestions only |
| AT-27 | F072 acknowledgment | visible Draft number, status waiting review, submitted=false |
| AT-28 | history | Thai labels; no internal event/ref column; no edit/delete |
| AT-29 | sensitive config commit | one `master.changed` SecC envelope |
| AT-30 | invalid or note-only change | no CSQ event |
| AT-31 | threshold breach | NTF only; no CSQ |
| AT-32 | PR created | F072 event owns lifecycle and carries origin refs |

Permission tests must verify unauthorized tenant/warehouse returns 403 without existence leakage. Contract tests must verify 409 replay and 424 dependency behavior. UI E2E covers FN-01..08 and all visible negative states.
