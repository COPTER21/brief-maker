# S1.8 Coverage Map before HTML · F-WH-QHOLD

| Scenario | Route/action entry | Required actual behavior/evidence | Boundary |
|---|---|---|---|
| S-01 | `#/holds` → **เพิ่มการกัก** drawer → named DOA slot picker | pendingHeld30, ATP60, status requested, no approval yet | stock and DOA mock |
| S-02 | `#/pending` → DEMO external approval event E1 | activeHeld30, pending0, ATP60; replay stable | demo harness only, real DOA TODO |
| S-03 | `#/pending` → DEMO reject event | pendingHeld0, ATP90; history rejected | demo harness only |
| S-04 | `#/holds` release12 → `#/pending` DEMO approve | request ATP60; approved held18/ATP72 | mock decision |
| S-05 | `#/pending` DEMO reject release | held30/ATP60; reservation cleared | mock decision |
| S-06 | release20 then15 same slice/version | second blocked, releasable10; no over-release | local guard; server atomicity spec |
| S-07 | hold drawer invalid quantities | inline error and no request; valid90→ATP0 | UoM precision `[ASSUMED]` |
| S-08 | release31/0 reject, 30 approve/replay | no ATP premature; final ATP90 once | mock decision |
| S-09 | DOA policy slots/picker | avatar+name+position/department; missing/ineligible block | policy/people mock, no hardcoded role |
| S-10 | stock slice drawer availability check | qty61 denied, qty60 contract-valid, no sale/transfer | no transaction |

## Navigation and UI locks
Tabs **รายการกัก**, **รออนุมัติ**, **ประวัติ** directly under page-head, actions upper right, canonical `.toolbar>.search-box`, master combobox, no hint/banner, no wizard. Pending/history rows are meaningful, not placeholder text. Every demo approval/rejection/simulation control has `data-demo` and orange DEMO badge; FRD/UI Brief include **Demo-only elements**. Filters search source/lot/location/status; list counts and ATP derive from stock slice/request state. No movement edit/delete control.

## Declaration and cross-lane hook map
`doa`: request carries required slots and selected person snapshots; decision event external mock. `ntf`: business hold/release result declaration only, no DOA auto-event duplicate. `csq`: consequence producer draft, no tube calculation. GRN QC W3-LITE source lookup/ref mock; no GRN posting. Source Item/UoM missing explicit FEATURE_LIST row is logged as gap; use existing picker soft ref and `[ASSUMED]` precision. Every declaration must have brief at S5; no actual engine registration or downstream acceptance test.

## Gate expectations
S3a v9 UX audit; S3b concrete arithmetic and DOM handler evidence for all WF-FN01–10/S01–10; S3c actual render attempt or WARN. S6.5 R2 must trace every FN/S/BR/DECL/LOCK to FRD and TC; unmet block rule is BLOCK, fix within cap. No fake success from comments or rule text alone.
