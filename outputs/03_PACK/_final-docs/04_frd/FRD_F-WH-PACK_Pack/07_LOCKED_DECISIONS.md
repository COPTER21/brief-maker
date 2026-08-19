# 07_LOCKED_DECISIONS — F-WH-PACK Packing

## §7.0 Scope Lock

| ID | Decision | Source | Status |
|---|---|---|---|
| LOCK-PACK-01 | root HTML is unchanged source of UI behavior | user/PM/BA 2026-08-19 | locked |
| LOCK-PACK-02 | Picking final contract wins for edge in | Picking final FRD | locked |
| LOCK-PACK-03 | no DN artifact; no invented contract | user | locked |
| LOCK-PACK-04 | NTF only; no DOA/DOCCFG declaration | user | locked |
| LOCK-PACK-05 | UX gate waived, not passed | user + UX report | locked |

## §7.1 Decisions

### LD-01 — One active carton

Use a DB-enforced partial unique invariant plus service validation. This prevents race-driven double active cartons.

### LD-02 — Idempotent unit is Pick source SO

Unique `(tenant,pick,source_type,source_ref)`; wave returns multiple stable pack refs. This aligns Picking final contract.

### LD-03 — Optimistic command concurrency

Pack/box versions and atomic transactions; stale writer receives 409. Allocation additionally locks/reconciles the source line.

### LD-04 — Print snapshots are versioned

Close creates immutable label version; reopen invalidates it; reprint is separately audited. PACKSLIP and BOXLABEL sizes are fixed by print specs.

### LD-05 — Notification through outbox/ENG-NOTIFY

Packing declares business events only. Recipients/channels/preferences are not hardcoded.

### LD-06 — DN adapter remains disabled

Only port shell/test seam is allowed until OQ-DN-01 becomes a locked external contract. Packing does not directly claim SO/Inventory posting ownership.

### LD-07 — Transfer is future adapter

HTML mock demonstrates intent; current confirmed Picking source is SO. No production Transfer path before OQ-XT-01.

## §7.2 Convention Deviations

- Actual enterprise feature ID is `F-WH-PACK`, so scope-local IDs use that prefix instead of illustrative `F-XX`.
- Custom action POST endpoints are intentional state commands, not generic PATCH.

## §7.3 Deferred

OQ owners/deadlines are authoritative in BRD §15. Library/framework selection, binary storage provider and queue implementation are Tech Lead decisions that must preserve contracts.
