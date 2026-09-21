# 07_LOCKED_DECISIONS — F084 Stocktake

## §7.0 Scope Lock

LOCK-ST-01..05 imported verbatim from BRD §3.4 and enforced by Overview §0.11. No conflicts found

## §7.1 Locked Decisions

- LD-01: final variance uses recount submission when present; first count remains evidence
- LD-02: threshold comparison is strict `>`; equality does not trigger recount
- LD-03: approval basis is absolute value, not net signed total
- LD-04: F082 owns inventory adjustment/posting; F084 sends draft only
- LD-05: rejected and closed release only the lock owned by the round
- LD-06: production identity never comes from the DEMO persona selector

## §7.2 Convention Deviations

- Status `recount` is a waiting/active mixed phase in prototype; backend distinguishes sheet assignment/status internally but presents one UI label “รอนับซ้ำ”
- `round_code` is a readable key, not a regulated document number; no DOCCFG declaration

## §7.3 Deferred

DOA `role-*` mapping, final F082 adapter schema and cross-feature lock query are deferred to owners in OQ-ST-01..04 without changing the locked business behavior
