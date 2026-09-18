# NTF_BRIEF · F-WH-ROP · จุดสั่งซื้อซ้ำ

> Draft producer contract for `ntf` chip. F-NOTIFY event catalog is absent from this workspace, so event ID, template and recipient policy are `[ASSUMED contract]` for Notification owner review; no ENG-NOTIFY/NC live emit or delivery is claimed.

| Event candidate | Trigger (FRD) | Recipient owner | Template candidate | Channel | User preference |
|---|---|---|---|---|---|
| `rop.reorder_candidate` `[ASSUMED]` | FN-07 after valid policy/snapshot and external `ncRuleRef`; API-05 envelope ack only | NC rule owner resolves recipient by configured rule | **{item_code} / {warehouse_ref}** พร้อมใช้ {available} · นโยบาย {policy_ref} | determined by NC central config, not ROP | determined by NC central config |

Payload: tenant_id, item_code, warehouse_ref, policy_ref, policy_version, rule_ref, on_hand, held, available, snapshot_as_of, idempotency_key. The ROP min merely determines PR suggestion; it does not determine whether NC alerts. NC may evaluate above-min candidates against a different rule. Do not hardcode threshold, email/LINE, recipient, quiet hours or template in ROP code. No DOA `doa_pending/result/escalate` event is declared. Trigger on candidate submission only, never on list read, validation failure or replay. Notification owner must check central catalog for an existing low-stock event and reuse it if semantically identical before wiring; the catalog was unavailable in this lane.

Dev wiring: replace mock API-05 only after owner-reviewed NC contract. The current HTML tests validate envelope/replay and unchanged stock only, never delivery. OQ owner: Notification/NC owner; channel/template/recipient/event ID and threshold semantics.
