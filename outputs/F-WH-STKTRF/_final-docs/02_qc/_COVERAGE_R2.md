# Coverage Report — F-WH-STKTRF (Round 2: FRD + AI Test Cases)

- Date: 2026-09-17 · node: `F083 Stock Transfer` · wave W3 · Q-document
- Contract: confirmed feature pack, round-1 report, function checklist (61 FN), BRD scope locks
- Artifacts: `F-WH-STKTRF.html`, `FRD_Pack/`, `testcases-F-WH-STKTRF.md`, declaration briefs

## Verdict: 🟢 PASS

Summary: **FN QA 61/61 · stories 10/10 · rules 34/34 · validations 21/21 · confirmed edges 21/21 · errors 11/11 · XT 6/6 · locks 11/11 · BLOCK 0 · WARN 0**

## Coverage matrix

| Item | Type | HTML | FRD | TC | Evidence |
|---|---|:---:|:---:|:---:|---|
| Warehouse/location input | edge in | ✓ | ✓ | ✓ | pickers/guards · 02_API API-02/04 · TC-V04/V08/P06 |
| Inventory movement/transit | edge out | ✓ | ✓ | ✓ | ship/receive tabs · API-07/08 · FN-07/08 · TC-A01..03/X04 |
| Cost/accounting handoff | edge out | ✓ | ✓ | ✓ | `รอลงบัญชี` · 02_API §2.3 · TC-X06 |
| DOA approval | engine | ✓ | ✓ | ✓ | real-person modals · API-05/06/10/11 · TC-A04/A08/X02 |
| DOCCFG number/snapshot | engine | ✓ | ✓ | ✓ | draft/submit/PDF · API-05/13/14 · TC-A09/X01 |
| Notification | engine | ✓ | ✓ | ✓ | HTML NTF anchors · 02_API §2.3 · TC-X03 |
| Same/cross mode and transit | block rules BR-02/03/05 | ✓ | ✓ | ✓ | 05_RULES §5.1 · TC-A01/A02/V04 |
| Quantity/location validity | block BR-01/04/06..11 | ✓ | ✓ | ✓ | 05_RULES §5.1/5.2 · TC-V05..10/P06 |
| Approval/rejection | block BR-12/13 | ✓ | ✓ | ✓ | 05_RULES + DOA brief · TC-A08/P05 |
| Receive SoD/invariant | block BR-14..17 | ✓ | ✓ | ✓ | API-08/FN-08 · TC-A03/P02/P03/V13 |
| Shortage/return | exception BR-18/19 | ✓ | ✓ | ✓ | API-09..11/FN-09..11 · TC-A04/A05/V15..17 |
| Final balance recheck | block BR-20 | ✓ | ✓ | ✓ | FN-07 algorithm · TC-C01 |
| Cancel/edit guards | block BR-21..23 | ✓ | ✓ | ✓ | state matrix · TC-A07/V19/P01 |
| Pending JE | lock BR-24 | ✓ | ✓ | ✓ | cross-module contract · TC-X06 |
| Append-only reversal | lock BR-25/26 | ✓ | ✓ | ✓ | 04_DB invariant · TC-A06/C05/X05 |
| Central config/audit/scope | BR-27..33 | ✓ | ✓ | ✓ | 05_RULES §5.1/5.6 · TC-X03..06/L06 |
| Confirmed exceptions E-01..08 | path | ✓ | ✓ | ✓ | 05_RULES §5.3 · TC-V04..10/L05/P06 |
| Confirmed exceptions E-09..15 | path | ✓ | ✓ | ✓ | 05_RULES §5.3 · TC-C01/A03..05/V13/V19/X03 |
| Confirmed exceptions E-16..21 | path | ✓ | ✓ | ✓ | 05_RULES §5.3 · TC-V20/X04/P02/P03/C02/L03 |
| Scope locks LK-1..11 | lock | ✓ | ✓ | ✓ | 07_LOCKED §7.0 · Ledger LOCK rows · TC-A/L/P/X groups |

## Error and state coverage

All eleven FRD error codes map to explicit test cases. All eleven lifecycle states appear in lifecycle/list cases. Concurrency/idempotency defaults are labeled `[AI-DEFAULT]` in both FRD and TC. No test authorizes an excluded capability.

## Scope guard

Stock adjustment, cycle count, location-master mutation, real JE posting, hard delete, manual transit selection, Lot/Serial and carrier/tracking remain absent as capabilities. Negative verification exists where the UI must guide or hide them.

## Diff from round 1

- Closed downstream documentation gap: API/logic/database contracts now exist in FRD.
- Closed QA gap: 53 AI cases trace the round-1 UI hooks and confirmed exception paths.
- QA column in `_coverage_wf_ticks.md` updated to **61/61 checked**; DEV remains unchecked for the implementation team.
- New gaps: none.

