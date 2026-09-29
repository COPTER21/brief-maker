# S3b coverage R1 · F-WH-LOT · round 2
Verdict: PASS for local business scope; external integrations remain mock/TODO as authorized.

| Obligation | HTML route / selector and function | Evidence |
|---|---|---|
| Item tracking none/lot/serial/expiry | `#/settings` `#lotItemPick`, `#lotTracking`, `#lotExpiryFlag`; `lotSaveSetting()` | Per-item config changed in local model; other item unchanged in domain test 6 |
| Conditional expiry and serial uniqueness | drawer `#f1/#f2/#f3`; `validate()` | Domain tests 1–2, 8 |
| FEFO for expiry item; FIFO non-expiry | `#/settings` `#lotRecommendation`; `eligibleLots()` | Domain tests 3–4; excluded expired/held, ordered eligible lots |
| Movement trace forward/back | `#/history` `#traceLot` and `#movementDetail`; `lotTrace()`/`lotShowMovement()` | Domain test 5: selected lots have distinct refs; predecessor/successor is shown |
| GRN/Transfer external mock | selected movement `from/to`, no mutation of source | No GRN/Transfer operation in HTML; movement fixtures read-only |
| Expiry through NC | `#/settings` “เปิดกฎแจ้งเตือน” → `lotOpenNC()` | Hook only; NC threshold and delivery external. `ntf` chip divergence logged. |
| Append-only | `lotMovements` read-only; `state.history.unshift()` for local master/config | Domain tests 6–7 preserve movement dataset |

`DOMAIN_TEST.json`: 8/8 pure-domain assertions passed. Browser interaction/render NOT-CHECKED in S3c; this report does not claim visual execution. No graph contradiction or scope expansion found.
