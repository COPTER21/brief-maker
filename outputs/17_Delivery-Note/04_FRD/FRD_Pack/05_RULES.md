# 05_RULES — F-WH-DN Delivery Note

## §5.1 Business rules

| ID | Rule |
|---|---|
| BR-DN-01 | queue contains packed and unbound Packing only |
| BR-DN-02 | reference combine key is source_type + customer + ship_to |
| BR-DN-03 | confirm creates draft without GI |
| BR-DN-04 | ready requires recipient/contact/assignee/date/carrier and transport-dependent fields |
| BR-DN-05 | over-capacity own vehicle warns; does not block |
| BR-DN-06 | 3PL dispatch requires tracking number |
| BR-DN-07 | tracking is forward-only; delivered is produced by POD |
| BR-DN-08 | reference dispatch creates atomic Goods Issue |
| BR-DN-09 | POD requires receiver; rejected line requires reason; photo cap comes from config |
| BR-DN-10 | result derives from total rejected: zero/full/between |
| BR-DN-11 | rejected quantity produces return movement and source counter adjustment |
| BR-DN-12 | first failed attempt is 1; max attempts comes from config |
| BR-DN-13 | return/cancel after GI reverses GI before restoring pack/source |
| BR-DN-14 | Sales sync is allowed only for sales_order source |
| BR-DN-15 | Stock Transfer displays origin→destination and never writes SO |
| BR-DN-16 | non-draft reference is read-only except explicit ready edit |
| BR-DN-17 | audit is append-only |
| BR-DN-18 | manual mode must not call Pack/Inventory/Sales/Transfer/AR automation |
| BR-DN-19 | every manual state change requires reason |
| BR-DN-20 | assignee is active company Employee only; manual entry is limited to driver/vehicle |
| BR-DN-21 | document number/snapshot rules belong to F-DOCCFG engines |
| BR-DN-22 | channel/preferences belong to ENG-NOTIFY |

## §5.2 State transitions

| Mode | From | Action | To | Guard/effect |
|---|---|---|---|---|
| reference | — | confirm packs | draft | valid combine; bind; no GI |
| reference | draft | ready | ready | BR-DN-04 |
| reference | ready | dispatch | in_transit | BR-DN-06/08 |
| reference | in_transit | track | in_transit | forward only |
| reference | in_transit | failed | failed | append attempt starting 1 |
| reference | failed | reschedule/return | ready/returned | preserve attempts / reverse+release |
| reference | in_transit | POD | delivered/partial/returned | result/stock/source sync |
| reference | draft/ready/in_transit/failed | cancel | cancelled | reason; conditional reverse |
| manual | any allowed | manual transition | any allowed | reason; audit only |

## §5.3 Permissions

Backend rechecks role, tenant and assignment for every mutation. `wh_lead` owns create/manage/destructive actions. Driver/picker is limited to configured assigned-record operations. Viewer is read-only. Manual transition permission remains OQ-02 and defaults conservatively to `wh_lead`.

## §5.4 Validations

- Reference create: at least one pack; all combine keys equal; none already bound; quantity/weight snapshot consistent
- Assignee: active Employee in same company; reject free text/manual object
- Manual driver: first name, last name and valid phone; manual vehicle: nonblank normalized plate
- Ready/dispatch: state/version and carrier-dependent required fields; 3PL tracking nonblank
- POD: receiver nonblank; 0≤rejected≤sent; rejected reason required; media count within config
- Return/cancel/manual transition: nonblank reason; server derives attempt/time/actor
- Manual mode: reject GI/source refs/automatic integration flags

## §5.5 Edge cases

| EC | Resolution |
|---|---|
| EC-01 mixed combine key | disable incompatible selection and reject API confirm |
| EC-02 refreshed deep route | prototype resolves list/no drawer; production may reload by ID but must avoid stale overlay |
| EC-03 first failed attempt | server writes attempt_no=1 |
| EC-04 return all | reason + reverse GI + pack queue restore |
| EC-05 cancel pre/post GI | no reverse before GI; mandatory successful reverse after GI |
| EC-06 Stock Transfer | show WH-01→WH-02; XT-04 only; XT-03 forbidden |
| EC-07 manual blank reason | reject without state/audit change |
| EC-08 invalid manual transport | inline validation; do not create temporary candidate |
| EC-09 A4 long data | wrap/page safely; preserve totals/signatures |
| EC-10 `[AI-DEFAULT]` concurrent write | version mismatch →409 and reload prompt |
| EC-11 `[AI-DEFAULT]` duplicate retry | same key/body returns prior result; different body →409 |
| EC-12 `[AI-DEFAULT]` inactive master | block new transition; retain historical snapshot |
| EC-13 `[AI-DEFAULT]` downstream/NTF failure | business transaction/outbox atomic; retry safely |
| EC-14 `[AI-DEFAULT]` partial GI/reverse | forbidden; rollback entire transition |

## §5.6 Error catalog

| Code | HTTP | Cause |
|---|---:|---|
| ERR_VALIDATION_FAILED | 400 | invalid shape/format |
| ERR_FORBIDDEN / ERR_NOT_ASSIGNED | 403 | role/scope |
| ERR_DN_NOT_FOUND | 404 | missing DN |
| ERR_STALE_DATA / ERR_IDEMPOTENCY_CONFLICT | 409 | concurrency/retry |
| BR_DN_COMBINE_MISMATCH | 422 | source/customer/ship-to differs |
| BR_DN_PACK_UNAVAILABLE | 422 | not packed/already bound |
| BR_DN_EMPLOYEE_REQUIRED | 422 | assignee not Employee |
| BR_DN_TRANSPORT_REQUIRED | 422 | missing driver/vehicle/tracking |
| BR_DN_REASON_REQUIRED | 422 | missing reason |
| BR_DN_POD_INVALID | 422 | receiver/qty/reason/media invalid |
| BR_DN_TRANSITION_INVALID | 422 | state/mode guard |
| BR_DN_MANUAL_AUTOMATION_FORBIDDEN | 422 | integration requested for Manual DN |
| ERR_DOWNSTREAM_UNAVAILABLE | 503 | shared/downstream service unavailable |

## §5.7 Security / D-CLASS

Tenant RLS, role/assignment recheck, audit all mutations and confidential reads/exports, transactional idempotent outbox, encrypted contact/POD references and masked PII outside operational need. Logs use IDs/hashes rather than full address/phone/media. No Restricted field identified.

