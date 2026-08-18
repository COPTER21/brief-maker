# 06_TESTS — F-SALES-PROMO Promotion

## §6.1 Acceptance Test Inventory

| ID | Scenario | Expected visible/system result | Trace |
|---|---|---|---|
| AT-01 | create valid draft | row/detail status “ร่าง”; audit create | US-01,FN-01/02 |
| AT-02 | LINE_DISC valid + pct>100 invalid | valid saves; invalid blocks | BR-03,VR-04,FN-04/08 |
| AT-03 | FREE_GOODS authoring | buy/get/UOM/qty/repeat persists | BR-04,FN-05 |
| AT-04 | THRESHOLD unordered/duplicate | block invalid; sorted valid tiers persist | BR-05,FN-06/08 |
| AT-05 | BUNDLE/coupon validation | duplicate items/high price/bad coupon block | BR-05/15,FN-07/08 |
| AT-06 | submit with overlap | no ack blocked; ack+slots sends; old record unchanged | BR-07/08,DOA,FN-09/10/15/16 |
| AT-07 | sequential approve | only current assignee acts; next step then active/scheduled | DOA,FN-11/12 |
| AT-08 | reject without/with reason | blank blocked; valid returns draft + history | DOA,FN-13 |
| AT-09 | LINE discount after TA | exact line discount + GL; promoAllowed false line skipped | BR-01/03/14,FN-18/24 |
| AT-10 | coupon/scope/date eligibility | correct coupon case-insensitive applies; missing/wrong skips | BR-02/15,FN-22 |
| AT-11 | free goods repeat | aggregated base qty creates zero-price free row | BR-04/13,FN-19 |
| AT-12 | threshold | highest reached tier after line discount; “ขาดอีก” when below | BR-05,FN-20 |
| AT-13 | bundle | min complete set count and correct savings | BR-05,FN-21 |
| AT-14 | ordering/exclusive | ascending priority; applied exclusive stops later | BR-06,FN-23 |
| AT-15 | pause/resume/end/cancel | only valid states; required reasons; irreversible end | BR-12,FN-28..30 |
| AT-16 | budget/quota usage | over-budget occurrence skipped; usage/exhaustion correct | BR-09/10,FN-26/27/31 |
| AT-17 | edit approved vs copy | edit blocked; copy draft clears coupon/start/usage/approval | BR-11,FN-17 |
| AT-18 | customer-specific scope | option/API rejected; direct user belongs to TA | BR-16,FN-03 |
| AT-19 | audit | every mutation/state/usage adds append-only event | BR-17,FN-94 |
| AT-20 | DOA policy version changes | frozen pending chain unchanged | EC-AI-03,FN-10 |
| AT-21 | concurrent draft save | stale version returns 409 and preserves latest | EC-AI-01 |
| AT-22 | double submit/approve/usage | one transition/count only | EC-AI-02,EC-12,FN-93 |
| AT-23 | permission/auth | 401/403 and no data change | EC-AI-04,FN-14 |
| AT-24 | decimal/boundary | no negative net; stable rounding | EC-AI-05,BR-03..05 |

## §6.2 UI/Search Tests

- FN-90: all seven tabs, search by code/name/coupon, type/scope filters, sort, empty state
- FN-91: four detail tabs, rule hero and six-fact grid
- FN-92: CSV rows exactly match current filter and permission
- FN-95: Esc chain combobox→modal→drawer; portal scroll/select works
- FN-96: approval candidate/timeline shows avatar + position + name
- responsive: 1024 and 1440 widths have no table/input overlap

## §6.3 Validation Boundary Matrix

| Field | Invalid | Boundary valid |
|---|---|---|
| priority | 0,1000,decimal | 1,999 |
| percentage | 0,100.01 | >0,100 |
| date | from before authoring, until<from | from=today, until=from |
| coupon | 2 chars, 21 chars, space, duplicate case variant | 3/20 chars A-Z0-9-_ |
| tier | zero/duplicate/descending min | one tier min>0; ascending |
| bundle | one/duplicate item, price≥list | two unique; 0<price<list |
| quantity | 0/negative | minimum 1/base conversion |

## §6.4 Permission / SoD Tests

- submitter excluded from every slot candidate list and approval endpoint
- wrong step assignee sees no buttons; direct call returns 403
- Sales Manager can lifecycle-manage but cannot bypass current DOA step
- BU Head has only assigned decision access, not create/edit/manage
- Invoice service cannot access human UI mutations; human cannot post usage events

## §6.5 State Tests

Every edge in `05_RULES.md` §5.3 has one positive case. For every state, attempt at least one forbidden transition and expect `BR_PROMO_INVALID_TRANSITION` with no audit of successful transition.

## §6.6 Engine Golden Data

- PM-011: LINE_DISC 10% BEV, min base qty 12
- PM-012: buy 10 cases get 1 case, wholesale, repeat, per-customer quota
- PM-013: threshold 20k→3%, 50k→5%, online/marketplace
- PM-014: bundle 189, retail/LINE, exclusive
- PM-015: `WELCOME100`, online, one per customer, total 1000
- PM-009 paused; PM-005 ended; verify both skipped with reason

## §6.7 Non-Functional DoD

- p95 list/evaluate ≤2s at designed load; no duplicate mutation under retry
- all tenant queries isolated; all inputs schema/sanitization checked
- audit transaction atomic with mutation
- no plain sensitive payload/coupon leaked to app log
- deterministic engine: same input/version returns byte-equivalent monetary result/order

## §6.8 Microcopy Anchors

Use Promotion.html verbatim. Required spot checks:

- “สร้างโปรโมชัน”
- “ทดสอบตะกร้า”
- “กรุณากรอกข้อมูลให้ครบถ้วน”
- “เลือกผู้อนุมัติให้ครบทุกขั้น”
- “ต้องยืนยันการทับซ้อนก่อนส่ง”
- “ไม่ใช่ผู้มีสิทธิ์ในขั้นปัจจุบัน”
- “ไม่อนุมัติ — ตีกลับเป็นร่าง”
- “ปิดโปรโมชันก่อนกำหนด”

## §6.9 Cross-Module Tests (XT)

| XT | Setup / action | Expected |
|---|---|---|
| XT-01 Price List + TA | resolved unit + promo_allowed inputs | Promotion uses supplied price only; no re-pricing |
| XT-02 QT/SO | call evaluate after TA then freeze result | applied/skipped/free rows and GL refs persist in document snapshot |
| XT-03 Invoice/GL/usage | post invoice with applied promotion; retry same event | GL ref trace correct; usage increment once |
| XT-04 Inventory ATP | free item output exceeds stock | promo-engine output unchanged; SO handles warning/block/partial per its contract |
| XT-05 DOA/Employee | config returns sequential slots/candidates | submitter removed; chosen people frozen; My Approval hook receives current item |
| XT-06 Master references | deactivate item/channel/group after submit | historical detail readable; new authoring cannot select inactive record |

## §6.10 Scope Lock Verification

- No test creates customer-specific promotion
- No test expects feature to decide ATP shortage
- No amount-tier approval test exists; DOA is no-amount sequential
- Campaign test is excluded and listed in coverage ledger as future

## §6.11 Verification Result

Acceptance 24/24 specified · UI FN 36/36 covered including FN-90..96 · XT 6/6 · Locks 7/7 · negative rendered cases included for validation/permission/state.
