# BRD Drift Report v1.1 — F-WH-STKTRF

## Metadata

- BRD base: `Pack Brief Feature/F-WH-STKTRF_Stock Transfer/2_BRD/BRD_F-WH-STKTRF.md` v1.0
- HTML source: `outputs/F-WH-STKTRF/F-WH-STKTRF.html`
- Review date: 2026-09-17
- Gate evidence: UX/Coverage/E2E reports in the feature output folder; PM/BA manual review passed

## Summary

| Severity | Count | Result |
|---|---:|---|
| Critical | 0 | No decision gate required |
| Business | 0 | Existing BRD contract preserved |
| Hidden logic | 4 | Existing BRD rules are now enforced in the prototype |
| UX | 6 | Carry forward to FRD/UI Brief |

## Hidden logic alignment

| Ref | HTML revision | BRD contract retained |
|---|---|---|
| HL-01 | Receive action accepts only in-transit/partial documents and clamps quantity to actual remaining balance | Receive guard, invariant, and partial receipt rules in Sections 5, 8, 9, 10 |
| HL-02 | Reversal creates a new approval-pending document; no prefilled receipt/movement; original becomes reversed only after completion | Append-only reversal and approval rules in Sections 5, 8, 9 |
| HL-03 | Shortage remains partial until its approval chain finishes; write-off occurs only at final approval | Shortage handling and SoD rules in Sections 5, 8, 9, 16 |
| HL-04 | Shipment and reason actions use a short busy lock to prevent duplicate execution | Concurrent-action protection in Sections 9 and 10 |

## UX drift

- Disabled receive/return actions expose the reason through a custom tooltip.
- Shipment confirmation uses an in-product CUBE modal instead of a browser dialog.
- Landing filters were realigned; creator moved into the searchable filter set.
- Landing table shows creator and transfer reason columns.
- Wizard line-item columns were aligned.
- Attachments use file upload; wide tables scroll horizontally without clipping columns.

These are presentation/interaction refinements. They do not add a new role, field type, status, scope item, security preset, or rule-management level.

## Section impact

| BRD section | Treatment |
|---|---|
| Section 1 | Updated metadata and changelog only |
| Sections 2–18 | Preserved from v1.0 |

## Revision checks

- CR01: PASS — changelog identifies version, date, source, and drift summary.
- CR02: PASS — no critical drift exists.
- CR03: PASS — business sections remain unchanged.
- CR04: PASS — no flexibility tag changed; migration plan is not applicable.
- CR05: PASS — COSO, SoD, P2 security controls, SLA, KPI, and monitoring remain valid.

## Verdict

**APPROVED — 0 critical drift, 0 business drift.**

