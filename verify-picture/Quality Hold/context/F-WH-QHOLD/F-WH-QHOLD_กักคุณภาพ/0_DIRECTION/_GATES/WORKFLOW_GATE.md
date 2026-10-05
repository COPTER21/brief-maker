# S3b QHold workflow coverage gate

**Verdict:** PASS for business/domain routes with N/A-UI on concurrent two-writer race, requiring backend harness; browser clicks not claimed. `_lane/DOMAIN_TEST.json` has 13/13 isolated VM assertions for all ten numerical scenarios and three source/idempotency controls. Source is `_lane_tools/qhold_inject.js` injected into v9 shell; all handlers below actually mutate local quarantine projection or display calculated rows, not prose-only placeholders.

| Workflow capability | Actual route / handler | Evidence/limit |
|---|---|---|
| WF-FN-01 list/stats | `#/records`, `qhRows`, `qhStats`, canonical `renderTableOnly` | 18 slices, onHand/held/ATP computed from model |
| WF-FN-02 slice/origin refs | `qhOpenForm`, `qhSlicePicker`, `qhChooseSlice`, `qhSubmitForm` | picker snapshots, GRN QC source required, later-issue reason |
| WF-FN-03 DOA people | `qhPolicyFor`, `qhPersonPicker`, `qhChoosePerson`, `qhValidSlots` | two required config slots; actual named eligible people with initials/position/department; mock policy DEMO |
| WF-FN-04 hold request | `qhRequest('hold')`, `qhHoldable`, `qhATP` | S01/07 pendingHeld, no onHand write |
| WF-FN-05 hold decision | `#/history`, `qhShowRequest`, `qhSimDecision`, `qhDecide` | S02/03 DEMO external event; replay guard |
| WF-FN-06 release request | `qhOpenForm('release')`, `qhRequest`, `qhReleasable` | S04/05/06/08 reserve held, ATP unchanged pending |
| WF-FN-07 release decision | `qhDecide`, `qhShowRequest` | approved decrements activeHeld once; rejected clears reservation only |
| WF-FN-08 concurrency/idempotency | `qhRequest` expectedSliceVersion/key and `qhDecide` sourceEventId/version | S06 pure logic tested; simultaneous UI actors N/A-UI/backend harness |
| WF-FN-09 history | `#/settings`, `qhEvents`, `qhShowEvent` | append-only event view, source refs, no edit/delete |
| WF-FN-10 outbound contract | slice drawer `qhCheckOutbound`→`qhCanOutbound` | S10 availability check only; no sale/transfer |

| Scenario | Result from isolated domain assertion | UI entry |
|---|---|---|
| S01 | ATP90→60, pendingHeld30, onHand100 | records add hold drawer |
| S02 | approved held30 ATP60; E1 replay one event | pending DEMO decision |
| S03 | reject restores ATP90 | pending DEMO decision |
| S04 | release12 requested ATP60; approved held18 ATP72 | records release drawer→pending DEMO |
| S05 | reject release held30 ATP60 | pending DEMO |
| S06 | stale/over-limit second release rejected, approve20 ATP80 | source function; concurrent UI N/A-UI |
| S07 | invalid 91/0/negative/NaN/precision rejected; pending90 ATP0 | hold drawer + pure test |
| S08 | release31/0 reject, release30→ATP90 once | release drawer→pending DEMO |
| S09 | missing/ineligible slots reject, selected person snapshots kept | DOA slot picker + pure test |
| S10 | outbound61 denies, 60 contract-valid, stock unchanged | slice drawer check, pure test |

Scope guard: no generic `domainAction` hardcoded manager hierarchy in generated QHold branch; no GRN/transfer/sale posting, stock balance or movement mutation. `qhMovements` remains a fixed upstream mock trace; request/decision events are separate append-only data. Demo-only decisions and people policy are labeled; production DOA must send its own decision event. Browser visual/actual keyboard/selector path remains S3c WARN until renderer exists.
