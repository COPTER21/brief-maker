# Coverage Report · F-WH-ROP (รอบ 2: FRD + Test Cases)

- วันที่: 2026-09-18
- Contract: Cube Feature List F085, PREBRIEF, Scope Lock, Function Checklist, PM/BA decisions
- Artifacts: `F-WH-ROP.html`, `BRD_F-WH-ROP.md`, `FRD_Pack/`, `testcases-F-WH-ROP.md`
- Checklist: FN 8 · rules 16 · integration/scope paths 10 · exceptions 8

## Verdict: 🟢 PASS

สรุป: ครบ 34/34 · gap block 0 · gap warn 0 · NOT-CHECKED 0

## Coverage Matrix

| Item | Type | HTML | FRD | TC | Evidence |
|---|---|---:|---:|---:|---|
| F009 → F085 ATP final | edge in | ✓ | ✓ | ✓ | `ropSnapshot/ropEvaluatePair` · 02_API Cross-module · BR-ROP-03 · TC-006,015 |
| F009 ADU/On-Order/asOf | edge in | ✓ | ✓ | ✓ | suggestion drawer · 02_API/03_LOGIC FN-04 · TC-006,016 |
| F085 → ENG-NOTIFY | edge out | ✓ | ✓ | ✓ | `ropNcCandidate` · API-05/FN-06 · TC-010,024 |
| F085 → F072 Draft | edge out | ✓ | ✓ | ✓ | `ropPreparePR` · API-06/FN-07 · TC-011,018,024 |
| F072 owns PR lifecycle | boundary | ✓ | ✓ | ✓ | HTML CSQ/contract comment · 02_API · BR-CSQ-05 · TC-019,021 |
| Item×Warehouse policy | rule | ✓ | ✓ | ✓ | policy drawer · BR-ROP-01 · TC-003,005 |
| bounds validation | block rule | ✓ | ✓ | ✓ | field-level errors · BR-ROP-02 · TC-004 |
| active version by date | rule | ✓ | ✓ | ✓ | `ropPolicyActive` · FN-03 · TC-005,023 |
| no hold subtraction | block rule | ✓ | ✓ | ✓ | F009 label/logic · BR-ROP-03 · TC-006,015 |
| ROP formula | block rule | ✓ | ✓ | ✓ | drawer reason · BR-ROP-04 · TC-006..008 |
| qty formula/rounding | block rule | ✓ | ✓ | ✓ | raw/pack/qty fields · BR-ROP-05 · TC-006,016 |
| three statuses | rule | ✓ | ✓ | ✓ | pills/KPI · BR-ROP-06 · TC-007 |
| no-policy state | exception | ✓ | ✓ | ✓ | `#ropCheckResult .check-card` · AT-17 · TC-009 |
| no-snapshot state | exception | ✓ | ✓ | ✓ | `SNAPSHOT_UNAVAILABLE` contract · AT-18 · TC-017 |
| schedule 06:00 | trigger | ✓ anchor | ✓ | ✓ | HTML TRIGGER comment + last-auto text · FN-05 · TC-012 |
| movement trigger | trigger | ✓ anchor | ✓ | ✓ | HTML TRIGGER comment · FN-05 · TC-012 |
| manual trigger | trigger | ✓ | ✓ | ✓ | **รันตรวจตอนนี้** · FN-05 · TC-012 |
| evaluation replay | block rule | ✓ | ✓ | ✓ | idempotency logic · BR-ROP-07/10 · TC-012 |
| NTF replay | block rule | ✓ | ✓ | ✓ | toast + event key · BR-ROP-08 · TC-010 |
| grouped Draft per warehouse | block rule | ✓ | ✓ | ✓ | PR toast/ack · BR-ROP-09 · TC-011,018 |
| vendor does not split | scope guard | ✓ | ✓ | ✓ | optional picker/vendor_suggests · BR-ROP-09 · TC-011 |
| Draft only/no auto-submit | scope guard | ✓ | ✓ | ✓ | `submitted:false` · BR-ROP-10 · TC-011 |
| human-readable history | rule | ✓ | ✓ | ✓ | `ropEventLabel/Detail` · BR-ROP-11 · TC-013 |
| append-only history | block rule | ✓ | ✓ | ✓ | no edit/delete · FN-08 · TC-005,013 |
| CSQ `master.changed` | declaration | ✓ anchor | ✓ | ✓ | ENG-CSQ comment · BR-CSQ-01,02 · TC-020 |
| CSQ invalid/no-effect exclusion | declaration | N/A-UI | ✓ | ✓ | FN-02/BR-CSQ-03 · TC-021 |
| threshold is NTF not CSQ | declaration | ✓ anchor | ✓ | ✓ | HTML comment · BR-CSQ-04 · TC-010,021 |
| PR event excluded from F085 CSQ | declaration | ✓ anchor | ✓ | ✓ | HTML comment · BR-CSQ-05 · TC-019,021 |
| permission isolation | backend rule | N/A-UI | ✓ | ✓ | 00 Overview/04 DB · TC-022 |
| optimistic conflict | backend rule | N/A-UI | ✓ | ✓ | API-02/FN-02 · TC-023 |
| dependency failure/retry | exception | ✓ error target | ✓ | ✓ | `#ropActionResult` · API-05/06 · TC-024 |
| no PO creation | scope guard | ✓ | ✓ | ✓ | no handler/API; locked decision · TC-011 |
| no Quality Hold query | scope guard | ✓ | ✓ | ✓ | HTML/FRD prohibition · TC-015 |
| no printable document/DOCCFG | scope guard | ✓ | ✓ | ✓ | no print route; LOCK-10 · TC-001 |

## Diff from Round 1

- Closed declaration drift: removed `rop.threshold_breached` and `rop.pr_draft_created` from F085 CSQ; retained threshold under NTF and PR lifecycle under F072.
- BRD/FRD/Test Case replaced obsolete mock/equality/min-only rules with approved Draft and Safety-driven formula.
- New backend-only coverage: permission, version conflict, CSQ exclusions and dependency retry.

## Gaps

ไม่มี coverage gap. Registry questions in CSQ brief are deployment coordination and are tracked in `PROPOSALS_outbound.md`; they do not represent missing FRD/TC coverage.
