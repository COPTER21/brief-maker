# CSQ_BRIEF · F-WH-ROP · จุดสั่งซื้อซ้ำ

> Draft for `csq` chip, `[ASSUMED contract]`: central CSQ contract/catalog unavailable. This is not registered with ENG-CSQ and the local HTML emits nothing. Owner: CSQ Engine owner.

| Provisional event | Trigger | Tube | Condition | FRD source |
|---|---|---|---|---|
| `master.changed` (reuse candidate) | successful FN-02 policy-version commit + append event | master-policy DC `[DEFAULT — รอยืนยัน]` | changed policy only; no invalid save, recompute, mock PR or NC candidate | 03_LOGIC FN-02, 04_DB `rop_policy_version`/`rop_event`, 05_RULES BR-CSQ-01–05 |

Envelope fields: tenant_id, policy_ref, item_code, warehouse_ref, version, effective_date, idempotency_key, correlation_id. Every field must come from policy/event DB; no Restricted actor name is sent raw. Event ID/profile/tube must be confirmed against central catalog before registration. If CSQ owner classifies a reorder-policy change as no 7C effect, retire this provisional event instead of emitting a false consequence. ROP computes no EC/AC/FC value and stores no tube stamps. OC belongs to Operation Process, document-level DC to DOA, SC reserved false. A reversal is a new policy version/event with `reversal_of`, never update/delete historical event. Central engine owns evaluation; this feature only proposes producer facts. Tests in W4 may verify payload shape and no duplicate local event, not engine registration or 7C outcome.

Open questions: CSQ owner confirms central contract, event ID and master-policy DC classification; Warehouse Product Owner confirms whether effective policy change merits declaration. No deployment registration before answers.
