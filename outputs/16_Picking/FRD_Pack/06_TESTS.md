# 06_TESTS — F-WH-PICK Picking

## §6.1 Acceptance inventory

| ID | Acceptance | Trace |
|---|---|---|
| AT-01 | eligible SO appears; payment/hold gates disable selection | FN-01..03, BR-01/02 |
| AT-02 | remaining accounts for picked/open Pick; SO drill shows breakdown | FN-04 |
| AT-03 | one/multi SO same WH creates Pick; mixed/max/open blocked | FN-05, BR-03 |
| AT-04 | allocation proves FEFO/FIFO, type rank, route and split | FN-06, ENG-01 |
| AT-05 | save atomically increments location allocation and runs Pick number contract | FN-07 |
| AT-06 | relocate releases old, allocates new and audits | FN-08 |
| AT-07 | no balance creates actionable short line | FN-09 |
| AT-08 | assignee search/keyboard/selected state/workload all render | FN-10 |
| AT-09 | role and own-assignment actions enforced UI+API | FN-11 |
| AT-10 | start changes assigned→in_progress | FN-12 |
| AT-11 | scan+quantity complete creates movement and updates SO | FN-13 |
| AT-12 | partial short requires reason, releases and backorders | FN-14 |
| AT-13 | partial relocate commits first part and reallocates remaining | FN-15 |
| AT-14 | refresh latest balance hard-allocates or shows exact no-stock warning | FN-16 |
| AT-15 | manual location applies same hard eligibility | FN-17 |
| AT-16 | Inventory replenishment mechanism exists internally but row icon is absent | FN-18, LOCK-12 |
| AT-17 | terminal lines + picked qty finish Pick | FN-19 |
| AT-18 | send Packing returns one ref per SO and is idempotent | FN-20 |
| AT-19 | close-short updates all remaining/backorder with reason | FN-21 |
| AT-20 | hold keeps allocation and resume works | FN-22 |
| AT-21 | cancel pre-start releases all; started cancel blocked | FN-23 |
| AT-22 | non-SO source rejected and absent from queue/UI | FN-24, LOCK-11 |
| AT-23 | list/tabs/A4/Esc/audit behavior matches HTML | FN-90..94 |

## §6.2 Negative/edge cases

| TC | Expected |
|---|---|
| TC-CC-01 | two mutations with same version: first wins, second 409 |
| TC-ID-01 | same idempotency/body returns same result, no duplicate allocation/movement/event |
| TC-PERM-01 | viewer/picker-other record gets 403 even with direct API |
| TC-LOC-01 | HOLD/STAGING/PACK/blocked/frozen/inactive/manual candidate rejected |
| TC-QTY-01 | over/negative/short-without-reason rejected |
| TC-STATE-01 | cancel after start and Packing before picked rejected |
| TC-MASTER-01 | deactivated master blocks new allocation, history snapshot remains |
| TC-PDF-01 | long Thai item/address wraps and font renders |

## §6.3 Test data

Use prototype seed equivalents: WH-01/WH-02, lot and non-lot items, short stock, SO gate/hold/pickup/service/open pick, roles wh_lead/picker/viewer. Do not assert mock counts as production truth.

## §6.4 Cross-module tests

| XT | Scenario | Expected |
|---|---|---|
| XT-01 | create/cancel Pick | Inventory allocation increments then releases once; SO queue returns |
| XT-02 | record full/short | Inventory movement and SO picked/reserved/backorder agree |
| XT-03 | finish/send Packing | one Packing intake per SO; retry does not duplicate |
| XT-04 | assign/short/done/short-close | declared ENG-NOTIFY event accepted with Pick ref |
| XT-05 | NTF unavailable | Pick transaction commits; event stays queued |
| XT-06 | Packing unavailable | status remains picked; retry safe |

## §6.5 UI microcopy checks

Verify verbatim from HTML: “เลือกผู้หยิบ”, “มอบหมายแล้ว”, “กรุณาระบุเหตุผล”, “หยิบครบ — พร้อมส่งต่อ Packing”, “ยกเลิกแล้ว”, and the no-stock/relocate messages recorded in `01_UI §1.5`.

## §6.6 DoD

- all P0/P1 acceptance + negative + XT pass
- all mutation unit/integration tests cover function, engine and transaction boundaries
- no open Critical/High security issue; RLS/role/ownership verified
- migration, rollback/forward plan, monitoring, alerting and outbox verified in staging
- allocation engine deterministic test includes FEFO, FIFO, split, rank, route, no-stock

## §6.7 Trace coverage

All functions FN-01..17 and ENG-01 are exercised by AT-01..23 or XT-01..06; all BR-PICK-01..17 have at least one positive or negative assertion.
