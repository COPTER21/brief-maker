# 05 RULES · F-WH-ROP

| Rule | Requirement | Test |
|---|---|---|
| BR-ROP-01 | exact Item×Warehouse effective version, append-only | AT-01,02 |
| BR-ROP-02 | `0≤safety≤min≤max`, lead≥0, pack≥1, ADU window allowed | AT-03..07 |
| BR-ROP-03 | ATP from F009 as-is; no reserved/hold subtraction | AT-08 |
| BR-ROP-04 | `ROP=max(min,safety+ADU×lead)`; trigger only ATP<ROP | AT-09..12 |
| BR-ROP-05 | `raw=max(0,max+safety−ATP−onOrder)`; ceil by pack | AT-13..15 |
| BR-ROP-06 | three visible statuses and explicit no-policy/snapshot states | AT-16..18 |
| BR-ROP-07 | daily 06:00 + affected movement + manual use same evaluator | AT-19..21 |
| BR-ROP-08 | NTF event replay-safe; central config owns delivery | AT-22,23 |
| BR-ROP-09 | one F072 Draft per warehouse/run; multiple lines; vendor does not split | AT-24..26 |
| BR-ROP-10 | Draft only, `submitted=false`, human submit to DOA | AT-27 |
| BR-ROP-11 | history append-only and human-readable | AT-28 |
| BR-CSQ-01 | only successful sensitive policy commit emits `master.changed` | AT-29 |
| BR-CSQ-02 | profile candidate CSQ-ROP-01, SecC, unique per pair+version | AT-29 |
| BR-CSQ-03 | invalid/no-effect save emits no CSQ | AT-30 |
| BR-CSQ-04 | threshold detection is NTF, not CSQ | AT-31 |
| BR-CSQ-05 | PR lifecycle belongs to F072 with origin refs | AT-32 |

## Prohibitions

No hold query, no stock write, no PR submit, no PO creation, no vendor split, no local notification channel, no 7C result card, no hardcoded approval chain, no mutation of history.
