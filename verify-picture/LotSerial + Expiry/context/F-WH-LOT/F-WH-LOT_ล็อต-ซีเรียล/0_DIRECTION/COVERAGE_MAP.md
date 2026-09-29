# Coverage map · F-WH-LOT (frozen HTML)

| Scenario | Actual route/selector | Handler/observable outcome | Boundary |
|---|---|---|---|
| S-01 | `#/records` → `#drawer #f1/#f0/#f3` | `lotChooseItem`, `validate`, `saveRecord`; new identity | local demonstration, API-02 production |
| S-02 | `#drawer #f3/#e3` | expiry-required field error, no row | local demonstration |
| S-03 | `#drawer #f3` hidden for non-expiry item | accepted identity with null expiry | local demonstration |
| S-04 | `#drawer #f2/#e2` | same-item duplicate serial error | local check; server atomic uniqueness remains API-02 |
| S-05 | `#/settings #lotItemPick/#lotTracking/#lotExpiryFlag` | `lotSaveSetting`; selected item policy changes, movement fixture unchanged | API-03 production/versioning |
| S-06 | `#/settings #lotRecommendation` | `eligibleLots`, `lotRecommend`; FEFO ordered table, held/expired excluded | API-04 read-only; upstream availability mock |
| S-07 | `#/settings #lotRecommendation` | non-expiry receipt order | API-04 read-only |
| S-08 | `#/history #traceLot/#movementDetail` | `lotTrace`, `lotShowMovement`; exact refs per selected lot | W3-LITE read mock |
| S-09 | `#/history .empty` | no movement yields explicit empty state | W3-LITE read mock |
| S-10 | `#drawer #saveBtn` | local replay toast; production Idempotency-Key contract | API-02 production |

No GRN/Transfer posting, reservation, notification delivery or CSQ 7C evaluation in HTML. S3 pure-domain behavior 8/8 is isolated Node evidence; browser visual/interactions are NOT-CHECKED. See `_GATES/_COVERAGE_REPORT.md` for round-2 FN/BR/TC matrix.
