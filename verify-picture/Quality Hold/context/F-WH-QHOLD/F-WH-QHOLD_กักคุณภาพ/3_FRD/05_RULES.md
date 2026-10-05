# Rules, validation and external injection
| BR | Rule | Error / owner |
|---|---|---|
| BR-01 | require identified slice, origin/reason; GRN QC requires mock GRN source; later issue source nullable | BAD_SLICE, REASON_REQUIRED, SOURCE_REQUIRED · GRN owner |
| BR-02 | configured DOA required slots with eligible actual people; revalidate on submit and decision | POLICY_UNAVAILABLE, SLOT_REQUIRED, PERSON_INELIGIBLE · DOA owner |
| BR-03 | held/pending held remains onHand but excluded ATP/transfer | CAPACITY_EXCEEDED · Inventory owner |
| BR-04 | request/decision event append-only, movement untouched | IMMUTABLE_EVENT · Warehouse owner |
| BR-05 | finite positive qty/UoM precision and ≤holdable/releasable; no clamp | INVALID_QTY, QTY_PRECISION, HOLD_EXCEEDS_FREE, RELEASE_EXCEEDS_HELD · Item/Inventory owner |
| BR-06 | pending hold blocks immediately `[ASSUMED]`, pending release reserves held and never frees ATP | CAPACITY_EXCEEDED · Warehouse Product Owner |
| BR-07 | version/sourceEventId/idempotency atomic, replay returns original, conflicting body/decision denied | VERSION_CONFLICT, IDEMPOTENCY_CONFLICT, EVENT_CONFLICT, INVALID_TRANSITION · DOA owner |
| BR-08 | DOA, GRN, NC, CSQ and sale/transfer are external mock/TODO | MOCK_UNAVAILABLE · respective owners |

DOA producer sends request context action/slice/qty/reason/origin/source and selected personRef snapshots; actual approval only through DOA decision adapter. No hardcoded hierarchy or local approval policy. NTF declaration emits business `inventory.quarantine_changed` candidate after approved hold/release; DOA's own pending/result/escalate alerts remain central and must not be duplicated. NC selects recipients/channel/template, no local delivery. CSQ candidate follows approved material availability change; central 7C only, no stamp here. W3-LITE GRN QC ref is soft mock, no receiving processing. Sale/transfer only asks API-07, no posting.
