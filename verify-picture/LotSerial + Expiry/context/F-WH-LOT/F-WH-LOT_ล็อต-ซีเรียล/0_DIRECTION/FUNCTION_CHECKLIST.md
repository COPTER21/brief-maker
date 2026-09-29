# Function checklist · F-WH-LOT

Contract: W4A row Lot/Serial + Expiry, PREBRIEF S-01..S-10, BRD, frozen HTML and FRD. The FN IDs below match FRD `03_LOGIC.md` exactly. WF is evidenced by frozen prototype/static plus isolated domain tests; DEV and browser QA remain open.

| FN | Capability / observable outcome | Scenario | Rule | UI / mock evidence | WF | DEV | QA |
|---|---|---|---|---|---|---|---|
| FN-01 | Search/filter/sort lot identities and data-derived counts; pagination is production API-only | S-01,S-08 | BR-08 | `#/records` → `renderTableOnly`, `stats` | ✓ | [ ] | [ ] |
| FN-02 | Create lot/serial identity; item policy drives conditional expiry/serial validation and duplicate guard | S-01,S-02,S-03,S-04,S-10 | BR-01,BR-02,BR-03 | drawer → `validate`, `saveRecord`; isolated domain tests | ✓ | [ ] | [ ] |
| FN-03 | Save per-item tracking/expiry policy with append-only config audit | S-05 | BR-01,BR-08 | `#/settings` → `lotSaveSetting`; isolated domain tests | ✓ | [ ] | [ ] |
| FN-04 | Recommend eligible FEFO/FIFO lots by item/warehouse without stock mutation | S-06,S-07 | BR-04,BR-05,BR-06 | `#/settings` → `eligibleLots`, `lotRecommend`; isolated domain tests | ✓ | [ ] | [ ] |
| FN-05 | Trace selected lot through distinct immutable movement refs and source mock | S-08,S-09 | BR-07,BR-08 | `#/history` → `lotTrace`, `lotShowMovement`; isolated domain tests | ✓ | [ ] | [ ] |
| FN-06 | Open NC expiry rules as soft link; notification delivery remains external | S-06 | BR-09 | `#/settings` → `lotOpenNC` mock toast; production destination contract in FRD | ✓ | [ ] | [ ] |
| FN-07 | Append audit event on successful identity or config mutation only | S-01,S-05,S-10 | BR-08 | `state.history.unshift` in `saveRecord`/`lotSaveSetting`; isolated domain tests | ✓ | [ ] | [ ] |
| FN-08 | Read immutable audit history | S-05,S-08 | BR-08 | production API-06 only; prototype history tab shows movement, not config audit | N/A-UI | [ ] | [ ] |

No transaction posting, stock reservation, NC delivery, or CSQ stamp is within this feature's HTML scope. `[ASSUMED]` contract owners are recorded in HANDOFF.
