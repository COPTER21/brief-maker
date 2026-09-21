# PREBRIEF — F-WH-STOCKTAKE · Stocktake

Source W4-LITE §2–3 and GOLDEN_RULES #1–12. Scope lock ST-01 large inventory round console, not Q; ST-02 scope freeze + timestamp snapshot; ST-03 blind count/recount/DOA; ST-04 Stock Adjustment mock [ASSUMED contract], no direct balance edit. Owner Warehouse BA.

## 1 · Obligations

| ID | Contract | Destination |
|---|---|---|
| O1 | Warehouse/Location/Item soft pickers | §4/FN01–02 |
| O2 | Scope-specific freeze OQ-ST-01 | §3/BR01/FN03 |
| O3 | Timestamped immutable snapshot | §4/BR02/FN04 |
| O4 | Count sheet/assignee, blind OQ-ST-02 | §3–4/BR03/FN05–07 |
| O5 | Threshold config/effective date recount | §5/BR04/FN08–09 |
| O6 | DOA actual person slot and append-only | §5/BR05/FN10 |
| O7 | W3-LITE adjustment mock, no local mutation | §6/BR06/FN11 |
| O8 | Cycle Count W4-FULL boundary | §6/FN12 |

## 2 · Scenarios D1–D6

D1 quantities: S01 equal, S02 shortage, S03 surplus, S04 blank/negative invalid. D2 states: S05 draft→frozen→assigned→counting→recount/approval→closed, S06 rejection/reopen with event. D3 controls: S07 threshold exceeded requires second independent count, S08 below threshold proceeds summary. D4 refs: S09 invalid warehouse/location/item or overlapping freeze blocks. D5 downstream: S10 approved variance sends mock Stock Adjustment only; S11 close releases selected scope freeze. D6 ERP standard: S12 movement attempt within scope blocked during freeze, outside scope permitted; S13 delayed approval still uses captured snapshot [AI-DRAFT][STD].

| S | Kind | Required evidence | BR | State/action | FN |
|---|---|---|---|---|---|
| S01 | Happy | snapshot/count equal | BR02–03 | count→review | 04–07 |
| S02,S03 | Alt | signed variance qty | BR04 | count→review/recount | 08–09 |
| S04 | Exception | blank/negative | BR03 | stay counting | 07 |
| S05 | Happy | scope,time,assignee,DOA | BR01–05 | full cycle | 01–10 |
| S06 | Alt | approver/reason/audit | BR05 | approval→rejected | 10 |
| S07 | Exception | threshold config/count2 | BR04 | recount required | 08–09 |
| S08 | Alt | variance under threshold | BR04 | review→approval | 08 |
| S09 | Exception | invalid ref/overlap | BR01 | stay draft | 01–03 |
| S10,S11 | Happy | adjustment mock/freeze release | BR06 | approved→closed | 11 |
| S12,S13 | Edge | movement scope/snapshot timestamp | BR01–02 | frozen/approval | 03–04 |

## 3 · Journey/status

Supervisor creates a round with warehouse/zone/all and effective date; freeze only selected scope [ASSUMED OQ-ST-01], atomically snapshot on-hand per item/location at freeze time. Assign count sheets to named counters. Counter sees location/item/UoM and own count input but **not system balance or variance** [ASSUMED OQ-ST-02]. Supervisor with permission can reveal snapshot balance; compare after counter submits. If abs(variance) exceeds configured threshold, assign second independent recount; no approval before completed recount. DOA resolves named person slot; approval emits adjustment request to W3-LITE mock and releases scope freeze on close. Rejection records reason and correction event, never overwrites count/movement. No direct stock mutation.

## 4 · Data dictionary

| Entity | Fields (type, required, source) |
|---|---|
| Round | id (string auto), name (text required), warehouse/location scope (search picker required), scope type enum all/zone/location (required), freeze_at (datetime auto), snapshot_at (datetime auto), status (enum auto), threshold_policy_ref/effective_date (config), created_by/time (auto), assignees (person picker), doa_chain_ref (engine) |
| Snapshot line | round id, item/location/UoM (master soft-ref snapshot), system_qty (decimal immutable, supervisor only), captured_at, version/movement watermark (auto) |
| Count sheet/line | sheet id, round/item/location, counter person, count_round 1/2, counted_qty decimal≥0 or blank pending, submitted_at, evidence/comment, immutable prior result, due date (config) |
| Variance | snapshot qty−accepted count (computed, supervisor view), threshold/exceeded flag, recount outcome, review reason, approval event, adjustment mock ref/status, audit fields |

## 5 · Rules

- BR01 [ASSUMED OQ-ST-01] freeze movement only selected scope. No overlap with another active freeze; outside scope remains operable. Movement control lives in central inventory engine, console displays mock block hook.
- BR02 snapshot inventory balance atomically at freeze time and preserve timestamp/version; no recompute using later on-hand value.
- BR03 [ASSUMED OQ-ST-02] blind count by default, counter cannot see system_qty or variance; supervisor permission gates reveal. Zero count valid; blank pending; negative rejected. Count submission append-only.
- BR04 threshold from config+effective_date, compare abs variance; if exceeded, second independent count required. [AI-DRAFT] equality threshold does not trigger recount; owner Warehouse BA.
- BR05 DOA resolved approver person avatar/name/position, maker≠approver; reason on reject; append-only decisions.
- BR06 approved final variance forwards soft-link [ASSUMED contract] to Stock Adjustment W3-LITE; status reflects queued/ack/error mock. Stocktake itself never updates inventory on-hand. Close releases freeze after handoff acknowledgment [AI-DRAFT].

## 6 · Boundaries and OQ

Stocktake is large selected-scope count round, distinct from Cycle Count + ABC W4-FULL recurring targeted rotation. No Lot/Barcode/Cycle feature built here. Item/Warehouse master, inventory balance, Stock Adjustment are picker/hook/mock. OQ-ST-01 Warehouse+Inventory engine owner; OQ-ST-02 Warehouse supervisor+Policy owner. Threshold/effective date owner Inventory config. [ASSUMED contract] W3-LITE adjustment payload owner Warehouse integration. No hard delete or direct movement mutation. Declarations detect doa+csq, exactly chip 2/2.

## 7 · Coverage

O1–O8 map to §§3–6 and FN; S01–S13 each have BR, transition/action and FN. Confidence 90% with explicit assumptions and owners. No internal graph edges by pack design; external hooks checked separately.
