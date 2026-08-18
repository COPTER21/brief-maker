# UAT Lite Audit — F-WH-PICK

- Source MD: 32 cases / 77 steps
- Kept: 16 cases / 34 user-facing steps (TC IDs preserved)
- Dropped: 16 cases because they require backend injection, duplicate a visible acceptance, or add no value to manual UAT

## Drop ledger

- TC-Q02 — payment-release mock is environment-specific; queue blocking retained in TC-Q01
- TC-Q04 — open-Pick arithmetic requires controlled seed; AI/API suite covers it
- TC-Q05 — service-line exclusion is data setup heavy; covered in automated suite
- TC-C04/C05/C07 — FIFO permutation, wizard relocation and stale master covered by allocation/automated tests
- TC-A03 — direct forbidden API is backend-only; visible read-only behavior kept in TC-A04
- TC-P01 — merged into TC-A02 start flow
- TC-P05/P06/P07/P08 — refresh/inbound/internal Inventory mechanism; visible removed icon retained in TC-C06
- TC-X03/X04/X05 — downstream outage, concurrency and idempotency require simulation
- TC-U01 — Esc technical sequence covered by automated E2E; manual document keeps higher-value flows

## Merge notes

- Queue gate variants merged into TC-Q01
- Start/progress merged into TC-A02
- Removed replenishment icon check merged into TC-C06

Mock/dynamic guard: no expected count/identifier is tied to prototype seed; running numbers and master-derived values are described as matching their configured source.
