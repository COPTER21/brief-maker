# NTF_BRIEF · F-WH-QHOLD · กักคุณภาพ
Draft `ntf` producer candidate `[ASSUMED contract]`; central catalog unavailable, no NC delivery. Owner Notification/NC owner. Do not duplicate DOA `doa_pending`, `doa_result` or escalation notifications.

| Candidate | Trigger | Facts | Channel/recipient |
|---|---|---|---|
| `inventory.quarantine_changed` | exactly once after **approved** hold/release commits projection/event | tenant,warehouse,slice,lot,request,kind,qty,held_before,held_after,ATP_after,source_ref,event_key,at | central NC rule only |

No candidate on requested/rejected/replay/read/validation failure. No personally named approver in payload. NC chooses recipient/template/channel/quiet hours, and should reuse an equivalent catalog event if present. No local sending; mock contract test verifies event envelope and idempotency only. Owner must confirm event ID, whether rejected decisions need a separate business alert, and SLA before wiring.
