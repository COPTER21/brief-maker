# INDEX — F-PO-001 ใบสั่งซื้อ (Purchase Order) — FRD v5 FULL Pack

> Cross-reference + Function Trace + Quick Navigation
> Generator: frd-generator-v5 (v5.1) · Variant: FULL · 2026-06-08

---

## Quick Navigation
| File | Content |
|---|---|
| 00_OVERVIEW | Doc control, scope, roles (COSO), dependencies, data-class summary, open questions |
| 01_UI | 3 pages + Layout IDs + wizard 5 steps + view tabs + UI↔API map |
| 02_API | 13 endpoints + contracts (HTTP layer) |
| 03_LOGIC | 9 Functions + 3 Engines + API↔Logic trace |
| 04_DB | 4 tables + classification (4-level) + relationships/indexes |
| 05_RULES | R01–R20 + VR01–VR08 + state machine + edge cases + errors + D-CLASS |
| 06_TESTS | AC per FR-01..07 + DoD + test data |
| 07_LOCKED_DECISIONS | LD-01..12 + conventions + layout |

## Function Trace (R8 — every mutation API → Function/Engine)
| API | Functions | Engines |
|---|---|---|
| API-03 create | FN-01, FN-03, FN-05 | po-amount |
| API-04 update | FN-02, FN-05 | po-amount |
| API-05 submit | FN-05, FN-06 | doa-resolver |
| API-06 approve | FN-06, FN-07 | doa-resolver |
| API-07/08 reject/return | FN-06 | — |
| API-09 cancel | FN-06 | — |
| API-10 pdf | FN-08 | po-amount, baht-text |
| API-13 attach | — (storage) | — |
✅ No orphan function/engine · ✅ No hidden logic in API

## Cross-Reference Matrix
| Concept | Defined | Referenced |
|---|---|---|
| Vendor logic (CP lock / PR select) | 03 FN-04 | 01 §1.3, 05 R04/R05, 07 LD-01/02 |
| Amount calc (VAT/discount/WHT) | 03 ENG po-amount | 02 API-03/04/10, 05 §5.3, 06 FR-03 |
| DoA resolve + SoD | 03 ENG doa-resolver, FN-06 | 02 API-05/06, 05 R12/R13, 06 FR-04 |
| State machine | 03 FN-06, 05 §5.4 | 01 §1.4 actions, 04 status_doc |
| Data classification | 04 §4.6 | 00 §0.7.1, 05 §5.7 |
| PO PDF variants | 03 FN-08 | 01 §1.4 PDF tab, 07 LD-11, PO_print-spec.md |

## Status / Verification
- Variant: FULL (9 files + INDEX) ✅ ตรง has-state+approval+3 engines
- R8 logic traceability ✅ · R9 03_LOGIC present ✅ · R10 data classification ทุก column ✅
- Layout authority: BRD §14.6 (html-generator-v3 v3.9) — no override ✅
- Security: P2 (14 controls) + User Access ENC + DOA ENC ✅
- Open questions (non-blocking): Q1 SLA, Q2 WHT table, Q3 cancel+GRN

## Downstream
→ html-generator-v3 (ใช้ 01_UI + Layout IDs) — prototype มีแล้ว (purchase-order.html)
→ frd-qa-generator-v2 (ใช้ 05_RULES + 06_TESTS + 02_API + 03_LOGIC)
