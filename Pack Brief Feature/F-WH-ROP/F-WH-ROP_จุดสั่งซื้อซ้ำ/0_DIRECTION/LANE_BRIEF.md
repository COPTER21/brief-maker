# LANE_BRIEF · F-WH-ROP · Reorder Point

> W4A FULL · 2026-09-14 · AI 100% no-vibe · Warehouse console/master

## Intent
Maintain min/max/safety stock **per Item×Warehouse** with version/effective date; compare an authorized inventory availability snapshot against the configured reorder policy, show replenishment suggestions and history, and expose a soft-link mock suggestion to PR. Notification of threshold crossing is governed by NC rules; no hardcoded notification threshold, recipient or channel. This feature never creates a live PR, PO, GRN or stock movement. Source W4 §2 and W4A checklist.

## Output and ownership
Policy maintainer saves a valid Item×Warehouse policy. Operator sees data-derived below/equal/above threshold status, suggested quantity and explanation. A `recommend PR` action prepares `{item,warehouse,qty,policyVersion,sourceRef,idempotencyKey}` for the PR soft-link mock, records mock acknowledgement and append-only event, without procurement execution. NC event candidate carries policy/rule refs and is sent only to NC mock; NC owns evaluation/delivery. Item/Warehouse/Inventory are read-only soft refs.

## Scope lock
`LOCK-W4-ROP`: console/master tabs directly below page-head; no Pattern Q wizard, no procurement transaction, no stock adjustment. Canonical toolbar filter on lists, no hint/banner; no persona switcher unless DEMO-marked. Thresholds in effective configuration (min/max/safety); NC notification rule in central NC configuration. Declaration chips `ntf,csq`; their briefs must be present and constrained to envelope/owner, not live delivery or 7C claim.

## Assumptions and owners
`[ASSUMED]` valid inequality `0≤safety≤min≤max`, trigger `available≤min`, suggested qty `max(0,max-available)`, no PR recommendation when quantity zero; owner Warehouse Product Owner. Snapshot `available` excludes QHold ATP but may remain on-hand, owner Inventory/QHold. PR payload/ack, NC envelope/threshold and CSQ event are `[ASSUMED contract]` owned by Purchase/NC/CSQ respectively. Conflict and replay are server authoritative.
