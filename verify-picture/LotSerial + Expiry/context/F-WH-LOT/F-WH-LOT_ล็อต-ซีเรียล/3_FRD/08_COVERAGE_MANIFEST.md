# 08_COVERAGE_MANIFEST — F-WH-LOT

Same complete BRD→UI/API/Logic/Rules/Tests ledger as 00_OVERVIEW §0.12 for quick review.

| BRD ID | Requirement | 01_UI | 02_API | 03_LOGIC | 05_RULES | 06_TESTS |
|---|---|---|---|---|---|---|
| S-01 | Per-item policy isolation | P-03 | API-03 | FN-03 | BR-01 | AT-01 |
| S-02 | Expiry-enabled create rejection | P-04 | API-02 | FN-02 | BR-02 | AT-02 |
| S-03 | Non-expiry null date create | P-04 | API-02 | FN-02 | BR-03 | AT-03 |
| S-04 | Same-item duplicate serial | P-04 | API-02 | FN-02 | BR-04 | AT-04 |
| S-05 | FEFO candidate order/exclusion | P-03 | API-04 | FN-04 | BR-05 | AT-05 |
| S-06 | Non-expiry receipt order | P-03 | API-04 | FN-04 | BR-06 | AT-06 |
| S-07 | Selected-lot trace | P-02 | API-05 | FN-05 | BR-07 | AT-07 |
| S-08 | Browse list | P-01 | API-01 | FN-01 | BR-08 | AT-08 |
| S-09 | NC soft hook | P-03 | API-X2 | FN-06 | BR-09 | AT-09 |
| S-10 | Retry save | P-04 | API-02 | FN-02 | BR-09 | AT-10 |
| BR-01 | Tracking none/lot/serial per item; expiry requires active tracking | P-01..04 | API-01..05 | §3.1 | BR-01 | AT-01 |
| BR-02 | Expiry required iff selected item policy enables it | P-01..04 | API-01..05 | §3.1 | BR-02 | AT-02,AT-03 |
| BR-03 | Serial unique tenant+item; serial qty=1 [ASSUMED] | P-01..04 | API-01..05 | §3.1 | BR-03 | AT-04 |
| BR-04 | Eligible=max(0,on_hand-held)>0 and unexpired if expiry enabled [ASSUMED] | P-01..04 | API-01..05 | §3.1 | BR-04 | AT-05 |
| BR-05 | Expiry item FEFO; non-expiry received_at ASC; stable tie-break [ASSUMED] | P-01..04 | API-01..05 | §3.1 | BR-05 | AT-05,AT-06 |
| BR-06 | Recommendation cannot reserve or mutate stock | P-01..04 | API-01..05 | §3.1 | BR-06 | AT-05,AT-06 |
| BR-07 | GRN/Transfer refs read-only mock until W3-LITE | P-01..04 | API-01..05 | §3.1 | BR-07 | XT-01 |
| BR-08 | Config/identity audit and movement ledger append-only | P-01..04 | API-01..05 | §3.1 | BR-08 | AT-01,AT-07 |
| BR-09 | Near-expiry threshold and delivery owned by NC rules | P-01..04 | API-01..05 | §3.1 | BR-09 | XT-02 |
| EC-01 | zero/held/expired | P-03 | API-04 | FN-04 | BR-04 | AT-05 |
| EC-02 | missing movement source | P-02 | API-05 | FN-05 | BR-07 | AT-07,XT-01 |
| EC-03 | concurrent duplicate serial | P-04 | API-02 | FN-02 | BR-03 | AT-04 |

