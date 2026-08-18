# Coverage Report — F-SALES-PROMO (รอบ 2: FRD + Test Cases)

- Date: 2026-08-18
- Contract: PREBRIEF_F-SALES-PROMO + FUNCTION_CHECKLIST + Central Plan promotion edges
- Artifacts: Promotion.html, BRD, FRD_Pack, DOA brief, testcases-F-SALES-PROMO.md
- Contract inventory: obligations 13 · rule groups 18 · functional items 36 · XT 6 · locks 7

## Verdict: 🟢 PASS

FRD และ Test Cases ครอบ in-scope contract 100%; block gap 0, warn gap 0, not-checked 0. รายการ manual wiring/engine registration เป็น delivery follow-up ที่มี spec/test contract แล้ว ไม่ใช่ coverage gap.

## Coverage Matrix — Obligations / Edges

| Item | Type | HTML | FRD | TC | Evidence |
|---|---|:---:|:---:|:---:|---|
| OB-1 Price List+TA base | edge in | ✓ | ✓ | ✓ | simulator post-price copy · 02 §2.4 · TC-X01/S01/S10 |
| OB-2 Group/Channel/Customer | edge in | ✓ | ✓ | ✓ | scope/simulator controls · 00 §0.6 · TC-L04/S03 |
| OB-3 Item Master | edge in | ✓ | ✓ | ✓ | product/UOM picker · 04 snapshots · TC-X06 |
| OB-4 GL Posting Group | edge in/out | ✓ | ✓ | ✓ | GL form/detail · 02 API-13/14 · TC-S01/X03 |
| OB-5 DOA/Employee | gov edge | ✓ | ✓ | ✓ | submit modal/timeline · DOA brief · TC-A01..A05/P01/X05 |
| OB-6 QT/SO calcPromo | edge out | ✓ simulator hook | ✓ | ✓ | ENG-01/API-13 · TC-X02 |
| OB-7 Invoice/GL/Inventory | edge out | ✓ detail copy | ✓ | ✓ | API-14/XT · TC-X03/X04 |
| OB-8 notification events | async | ✓ copy only | ✓ contract/deferred declaration | ✓ source behavior | 02 §2.5; DOA events owner; declaration intentionally skipped |
| OB-9 PM numbering | config edge | ✓ mock code | ✓ deferred wiring | ✓ format visible | 04 unique code; TC-C01 |
| OB-10 no customer-specific | scope guard | ✓ | ✓ | ✓ | 07 LOCK-02 · TC-P04 |
| OB-11 overlap warn+ack/no replace | exception | ✓ | ✓ | ✓ | confirmSubmit/overlaps · BR-07/08 · TC-A01/A02 |
| OB-12 approved UI layout | UI lock | ✓ | ✓ | ✓ | 01 UI five surfaces · TC-L01/L08 |
| OB-13 BA HTML+PREBRIEF process | provenance | ✓ | ✓ | ✓ | 00 §0.1/0.12 · Meta sources |

## Coverage Matrix — Business Rules

| Rule | FRD | TC | Evidence |
|---|:---:|:---:|---|
| BR-01 | ✓ | ✓ | 05 BR-PROMO-01 · TC-S01/X01 |
| BR-02 | ✓ | ✓ | 05 BR-PROMO-02 · TC-S02..S04/S11 |
| BR-03 | ✓ | ✓ | 05 BR-PROMO-03 · TC-C03/C04/S01/S10 |
| BR-04 | ✓ | ✓ | 05 BR-PROMO-04 · TC-C05/S05/X04 |
| BR-05 | ✓ | ✓ | 05 BR-PROMO-05 · TC-C06..08/S06..08 |
| BR-06 | ✓ | ✓ | 05 BR-PROMO-06 · TC-S09 |
| BR-07 | ✓ | ✓ | 05 BR-PROMO-07 · TC-A01/A02 |
| BR-08 | ✓ | ✓ | 05 BR-PROMO-08 · TC-A02 |
| BR-09 | ✓ | ✓ | 05 BR-PROMO-09 · TC-S11/X03 |
| BR-10 | ✓ | ✓ | 05 BR-PROMO-10 · TC-S12/X03 |
| BR-11 | ✓ | ✓ | 05 BR-PROMO-11 · TC-C11/C12 |
| BR-12 | ✓ | ✓ | 05 BR-PROMO-12/§5.3 · TC-A06..A09 |
| BR-13 | ✓ | ✓ | 05 BR-PROMO-13 · TC-S05/X04 |
| BR-14 | ✓ | ✓ | 05 BR-PROMO-14 · TC-S01/X03 |
| BR-15 | ✓ | ✓ | 05 BR-PROMO-15 · TC-C09/C10/S02 |
| BR-16 | ✓ | ✓ | 05 BR-PROMO-16 · TC-P04 |
| BR-17 | ✓ | ✓ | 05 BR-PROMO-17 · TC-A10/X03 |
| BR-DOA-01..07 | ✓ | ✓ | 05 §5.5 + DOA brief · TC-A01..A05/P01..P03/X05 |

## Coverage Matrix — Function Checklist

| FN | FRD evidence | TC evidence | Status |
|---|---|---|:---:|
| FN-01 | 01 P-03, 02 API-02 | TC-C01/C02 | ✓ |
| FN-02 | 04 header fields | TC-C01/C04/C09 | ✓ |
| FN-03 | 05 scope rules | TC-L04/P04 | ✓ |
| FN-04 | ENG-01 LINE | TC-C03/C04/S01 | ✓ |
| FN-05 | ENG-01 FREE | TC-C05/S05 | ✓ |
| FN-06 | ENG-01 THRESHOLD | TC-C06/C07/S06/S07 | ✓ |
| FN-07 | ENG-01 BUNDLE | TC-C08/S08 | ✓ |
| FN-08 | 05 §5.4 | TC-C02/C04/C07..C10 | ✓ |
| FN-09 | FN-04/API-04 | TC-A01/A02 | ✓ |
| FN-10 | approval snapshot | TC-A02/X05 | ✓ |
| FN-11 | FN-05/API-05 | TC-A03/A04 | ✓ |
| FN-12 | lifecycle final decision | TC-A04 | ✓ |
| FN-13 | reject contract | TC-A05 | ✓ |
| FN-14 | SoD contract | TC-P01/P02 | ✓ |
| FN-15 | FN-03 overlap | TC-A01 | ✓ |
| FN-16 | ack persistence | TC-A02 | ✓ |
| FN-17 | FN-06 copy | TC-C12 | ✓ |
| FN-18 | ENG-01 LINE result | TC-S01 | ✓ |
| FN-19 | ENG-01 FREE result | TC-S05/X04 | ✓ |
| FN-20 | ENG-01 threshold | TC-S06/S07 | ✓ |
| FN-21 | ENG-01 bundle | TC-S08 | ✓ |
| FN-22 | coupon eligibility | TC-S02 | ✓ |
| FN-23 | ordering/exclusive | TC-S09 | ✓ |
| FN-24 | promoAllowed | TC-S10 | ✓ |
| FN-25 | detail usage/account tab | TC-X03/X04 | ✓ |
| FN-26 | usage aggregates | TC-X03/S12 | ✓ |
| FN-27 | exhaustion rule | TC-S11/S12 | ✓ |
| FN-28 | lifecycle pause/resume | TC-A06/A07 | ✓ |
| FN-29 | end early | TC-A08 | ✓ |
| FN-30 | cancel state/reason | TC-A09 + state matrix | ✓ |
| FN-31 | per-customer quota | TC-S12 | ✓ |
| FN-90 | 01 P-01 | TC-L01..L06 | ✓ |
| FN-91 | 01 P-02 | TC-L01/A10 | ✓ |
| FN-92 | API-15 | TC-L07 | ✓ |
| FN-93 | idempotency/busy | TC-N02 | ✓ |
| FN-94 | FN-09 audit | TC-A10/X03 | ✓ |
| FN-95 | 01 §1.7 | TC-L08 | ✓ |
| FN-96 | DOA UI contract | TC-A01..A04 | ✓ |

## Cross-Module / Locks

| Item | FRD | TC | Result |
|---|:---:|:---:|:---:|
| XT-01..XT-06 | 02 §2.4 + 06 §6.9 | TC-X01..TC-X06 | ✓ 6/6 |
| LOCK-PROMO-01..07 | 07 §7.0 | TC-L01/L08/P04/X03..X06 | ✓ 7/7 |
| N/A-UI backend controls | 03/04/05 | TC-N01..N03/P03 | ✓ |

## Gaps

ไม่มี block/warn gap.

## Scope Creep Check

- ไม่มี customer-specific, loyalty, mixed-type, Campaign, ATP decision ใน feature artifacts
- persona switch remains explicitly demo-only; not production authorization
- `[AI-DEFAULT]` reliability controls are labeled in FRD and tests; they do not change approved business scope

## Diff from Round 1

- Closed downstream-spec gap: FRD now defines API/logic/DB/test contracts behind all HTML hooks
- Added explicit coverage for XT-01..06, LOCK-01..07, concurrency/idempotency and DOA freeze
- No new HTML drift introduced

## Checker Self-Gate

- Every ✓ points to FRD section and/or TC id ✅
- No criteria invented outside PREBRIEF/checklist/approved engineering safeguards ✅
- NOT-CHECKED = 0 ✅
- Verdict policy applied: no missing block rule/edge ✅

Final verdict: **PASS — ready for UAT generation and dev handoff.**
