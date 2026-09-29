# _COVERAGE_REPORT · F-WH-LOT · round 2

Verdict: **WARN**. Business FN/S/BR scope has FRD and TC trace; frozen HTML carries identified prototype behavior except FN-08 (production API-only). Browser visual interaction NOT-CHECKED. NC expiry notification has chip/detect DIVERGENCE, owned by NC/registry; no local delivery is claimed. These limitations are explicit handoff items, not silent passes.

## Evidence matrix

| Item | HTML / UI evidence | FRD evidence | TC evidence |
|---|---|---|---|
| FN-01 | #/records `.toolbar`, `renderTableOnly`, `stats` | 01_UI P-01; 03_LOGIC FN-01 | TC-001,TC-002,TC-004,TC-005,TC-006,TC-008,TC-009,TC-010,TC-023 |
| FN-02 | drawer `validate`/`saveRecord` | 01_UI P-04; 03_LOGIC FN-02; 05_RULES BR-01..03 | TC-011,TC-012,TC-013,TC-014,TC-015,TC-016,TC-019 |
| FN-03 | #/settings `lotSaveSetting` | 01_UI P-03; 03_LOGIC FN-03 | TC-026,TC-027,TC-028,TC-029,TC-030,TC-031,TC-032 |
| FN-04 | #/settings `lotRecommend`/`eligibleLots` | 01_UI P-03; 03_LOGIC FN-04; 05_RULES BR-04..06 | TC-034,TC-035,TC-036,TC-037,TC-038,TC-040,TC-041,TC-042 |
| FN-05 | #/history `lotTrace`/`lotShowMovement` | 01_UI P-02; 03_LOGIC FN-05 | TC-007,TC-043,TC-044,TC-045,TC-046,TC-047 |
| FN-06 | #/settings `lotOpenNC` (mock toast) | 02_API API-X2; 03_LOGIC FN-06 | TC-033,TC-052 |
| FN-07 | `state.history.unshift` on successful create/config; no mutation of movement | 03_LOGIC FN-07; 04_DB T_lot_audit | TC-001,TC-016,TC-031,TC-032,TC-048,TC-053,TC-055 |
| FN-08 | N/A-UI: config audit read is production API-only; movement tab is not config audit | 02_API API-06; 03_LOGIC FN-08 | TC-026,TC-027,TC-028,TC-029,TC-030,TC-031,TC-032 |
| S-01 | drawer item policy → valid create | 02_API API-02; 05_RULES BR-01 | TC-011,TC-012,TC-013,TC-014,TC-015,TC-016,TC-019 |
| S-02 | drawer expiry field error | 02_API API-02; 05_RULES BR-02 | TC-011,TC-012,TC-013,TC-014,TC-015,TC-016,TC-019 |
| S-03 | drawer non-expiry null date | 02_API API-02; 05_RULES BR-02 | TC-017 |
| S-04 | drawer duplicate serial error | 02_API API-02; 05_RULES BR-03 | TC-018,TC-020,TC-021,TC-022 |
| S-05 | #/settings per-item save | 02_API API-03; 05_RULES BR-01 | TC-026,TC-027,TC-028,TC-029,TC-030,TC-031,TC-032 |
| S-06 | #/settings FEFO ranked candidates | 02_API API-04; 05_RULES BR-04/05 | TC-034,TC-035,TC-036,TC-037,TC-038,TC-040,TC-041,TC-042 |
| S-07 | #/settings non-expiry receipt order | 02_API API-04; 05_RULES BR-05 | TC-039 |
| S-08 | #/history distinct movement refs | 02_API API-05; 05_RULES BR-07 | TC-007,TC-043,TC-044,TC-045,TC-046,TC-047 |
| S-09 | #/history empty selected-lot trace | 02_API API-05; 05_RULES BR-07 | TC-007,TC-043,TC-044,TC-045,TC-046,TC-047 |
| S-10 | drawer local replay toast (nonserial fixture) | 02_API API-02; 05_RULES BR-08 | TC-025,TC-058 |
| BR-01 | #/records `.toolbar`, `renderTableOnly`, `stats` | 05_RULES BR-01; 08_COVERAGE_MANIFEST BR-01 | TC-013,TC-018,TC-019,TC-027,TC-028,TC-054,TC-057,TC-059 |
| BR-02 | drawer `validate`/`saveRecord` | 05_RULES BR-02; 08_COVERAGE_MANIFEST BR-02 | TC-015,TC-017,TC-029 |
| BR-03 | #/settings `lotSaveSetting` | 05_RULES BR-03; 08_COVERAGE_MANIFEST BR-03 | TC-021,TC-022 |
| BR-04 | #/settings `lotRecommend`/`eligibleLots` | 05_RULES BR-04; 08_COVERAGE_MANIFEST BR-04 | TC-005,TC-035,TC-036,TC-037,TC-038,TC-042 |
| BR-05 | #/history `lotTrace`/`lotShowMovement` | 05_RULES BR-05; 08_COVERAGE_MANIFEST BR-05 | TC-034,TC-039,TC-040 |
| BR-06 | #/settings `lotOpenNC` (mock toast) | 05_RULES BR-06; 08_COVERAGE_MANIFEST BR-06 | TC-041,TC-051 |
| BR-07 | `state.history.unshift` on successful create/config; no mutation of movement | 05_RULES BR-07; 08_COVERAGE_MANIFEST BR-07 | TC-043,TC-044,TC-045,TC-048,TC-049,TC-056 |
| BR-08 | N/A-UI: config audit read is production API-only; movement tab is not config audit | 05_RULES BR-08; 08_COVERAGE_MANIFEST BR-08 | TC-001,TC-016,TC-031,TC-032,TC-048,TC-053,TC-055 |
| BR-09 | N/A-UI: config audit read is production API-only; movement tab is not config audit | 05_RULES BR-09; 08_COVERAGE_MANIFEST BR-09 | TC-033,TC-052 |
| DECL-DOA | N/A: no approval transition | 00_OVERVIEW §0.12; no DOA declaration | N/A |
| DECL-NTF | DIVERGENCE: near-expiry NC delivery belongs external NC; no local declaration or send | 02_API API-X2; 05_RULES BR-09; 5_DECLARATIONS DIVERGENCE | TC mock TC-033,TC-052 |
| DECL-CSQ | N/A-UI: CSQ brief for master.changed; no 7C stamp claimed | 5_DECLARATIONS CSQ_BRIEF; 03_LOGIC §3.4 | TC mock TC-053 |
| DECL-DOCCFG | N/A: console/master no numbered transaction | 00_OVERVIEW §0.12 | N/A |
| XT-W3 | Selected-lot distinct GRN/Transfer mock refs only | 02_API API-05; 03_LOGIC §3.4 | TC mock TC-043,TC-049,TC-050 |
| XT-PICK | Recommendation payload only, no reservation/issue | 02_API API-04; 03_LOGIC §3.4 | TC mock TC-051 |

## Gate findings and follow-up

- **WARN / browser:** S3c render failed with Playwright launch; no desktop/mobile visual acceptance. The 8 pure-domain assertions and static code trace are isolated evidence only. Owner: UI QA before release.
- **WARN / declaration divergence:** W4 chip has csq; near-expiry can trigger NC notification signal. NC owns threshold/channel/delivery, registry owner resolves chip mapping. No `ntf` file added silently and no delivery assertion in TC.
- **N/A-UI:** FN-08 audit read is production API only, while prototype exposes movement trace and stores local create/config events without config-audit list. Owner: Warehouse Product Owner decides whether audit list is needed in production UI; server must retain API-06.
- **Mock contracts:** GRN/Transfer W3-LITE, Picking and NC/CSQ are payload/reference boundaries. TC system/mock cases require a harness; no downstream posting or 7C result is tested.

## Round 1 → round 2

S3 business gaps in the initial generic HTML (per-item config, FEFO, distinct trace, conditional fields) were repaired before freeze and isolated domain tests passed 8/8. Round 2 adds exact FRD/TC trace and exposes FN-08 API-only limitation and notification DIVERGENCE. No HTML change after freeze.

R15 construction: 59 AI manual cases = 59 QA JSON cases; official QA builder reported 59 cases. QA HTML has 0 screenshot regions (WARN).
