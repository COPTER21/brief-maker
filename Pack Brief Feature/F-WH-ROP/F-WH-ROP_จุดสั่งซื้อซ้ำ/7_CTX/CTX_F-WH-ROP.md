# CTX — F-WH-ROP: จุดสั่งซื้อซ้ำ

> **derived from:** FRD F-WH-ROP v1.0 · **generated:** 2026-09-14 · **module:** Warehouse · **status:** AI-specified / external contracts pending. Derived reference only; FRD is source of truth and implementation input. Regenerate if FRD changes.

## 1. Summary
Maintains effective-dated reorder policy per exact Item×Warehouse, reads Inventory/QHold availability and derives suggested replenishment quantity. It sends NC candidate facts to a mock rule boundary and prepares PR mock payload/ack when a positive suggestion exists. It does not create PR, deliver notification or change stock/movement. User access, persistence and downstream adapters are proposed production contracts, not implemented in local HTML. (FRD 00_OVERVIEW, 03_LOGIC FN01–08)

## 2. Data Contract
### Entities
| Entity | Key | Shared fields | Source/ownership |
|---|---|---|---|
| `rop_policy_version` | `policy_ref` | tenant_id, item_code, warehouse_ref, version, min_qty, max_qty, safety_qty, effective_date, nc_rule_ref | ROP version store; old rows immutable |
| `rop_event` | `event_ref` | tenant_id, kind, policy_ref, item_code, warehouse_ref, at, correlation_id | ROP append-only audit/outbox |
| `rop_mock_request` | `request_ref` | tenant_id, kind PR/NC, idempotency_key, request_hash, policy_ref, snapshot_ref, ack_json, status | ROP mock ledger only |
| `AvailabilitySnapshot` | `snapshot_ref` | item, warehouse, onHand, held, asOf | upstream Inventory/QHold read model; no ROP write |
| Item / Warehouse | existing code/ref | identity, scope, name | external master soft refs |

### States/enums
| Domain | Values | Owner |
|---|---|---|
| Policy temporal state | future, effective, superseded | ROP by effective date/version |
| Suggestion status | below, equal, above threshold | ROP FN-05 derived |
| Mock request kind | PR, NC | ROP local mock ledger |
| Mock PR outcome | new, acknowledged, retryable unavailable, replay | ROP adapter, no Procurement transaction |
| NC candidate outcome | new, submitted to mock, replay | ROP adapter, no delivery |
| Event kind in demo | `policy.saved`, `suggestion.evaluated`, `pr.mock`, `nc.candidate` | append-only producer events |

### Relationships, constraints and audit
One Item×Warehouse pair has many policy versions; one latest effective version as of date is selected. A policy may reference an NC rule but does not own it. A policy and stock snapshot produce a derived suggestion. Mock requests and events reference policy/version and snapshot; upstream stock remains unchanged. Unique tenant/pair/version and tenant/kind/idempotency key; quantity order `0≤safety≤min≤max` `[ASSUMED]`. All writes carry actor/correlation/time; actor is Restricted/PII, thresholds and stock Confidential. Refer FRD 04_DB §4.2/4.6.

## 3. API Surface (proposed, not live)
| ID | Method/path | Purpose | Key input/output |
|---|---|---|---|
| API-01 | GET `/v1/rop/policies` | scoped policy read | itemCode, warehouseRef, asOf → policy versions |
| API-02 | POST `/v1/rop/policies` | append version | pair, min/max/safety, effectiveDate, ncRuleRef, expectedVersion → policy/version/event |
| API-03 | GET `/v1/rop/suggestions` | derive current advice | pair, asOf → policyVersion, snapshotRef, onHand, held, available, triggered, suggestedQty |
| API-04 | POST `/v1/rop/pr-preparations` | prepare PR mock only | policyRef, snapshotRef, suggestedQty, key → mockRef/ack/replay |
| API-05 | POST `/v1/rop/nc-candidates` | submit NC candidate mock | policyRef, snapshotRef, ruleRef, key → envelope/replay |
| API-06 | GET `/v1/rop/events` | immutable event read | scoped pair/cursor → events |
| API-07 | GET `/v1/rop/options` | scoped master lookup | kind item/warehouse, q → code/name options |

All endpoints require server tenant+warehouse scoping. API-02 requires maintainer write permission and expectedVersion; API-04/05 require durable idempotency in production. Proposed error vocabulary: ACCESS_DENIED, BAD_REFERENCE, REQUIRED, POLICY_BOUNDS, BAD_EFFECTIVE_DATE, VERSION_CONFLICT, NO_POLICY, SNAPSHOT_UNAVAILABLE, SNAPSHOT_STALE, NO_POSITIVE_SUGGESTION, MOCK_UNAVAILABLE, IDEMPOTENCY_CONFLICT, NC_RULE_MISSING. (FRD 02_API and 05_RULES)

### Declared events, draft only
`master.changed` after policy version commit is a provisional CSQ producer candidate, not emitted/registered in local HTML; master-policy DC classification requires CSQ owner confirmation. `rop.reorder_candidate` is a provisional NTF/NC producer candidate with external ruleRef and availability facts, not notification delivery. Their IDs are `[ASSUMED contract]` because central catalogs are absent; no DOA auto-event is redeclared. (FRD 02_API Cross-module, 05_RULES; declaration briefs)

## 4. Shared rules for dependent features
| Rule | Contract | Affected boundary |
|---|---|---|
| BR-01/02 | exact Item×Warehouse effective version; future policy inactive until effective date | Item/Warehouse consumers and Inventory snapshot readers |
| BR-04 | ROP PR trigger uses available≤configured min, qty to configured max `[ASSUMED]` | Procurement candidate consumer; not NC threshold |
| BR-05 | held retained onHand but excluded from available/ATP | QHold, Inventory, Scan, Cycle consumers |
| BR-06 | NC receives candidate facts/ruleRef and owns threshold/channel/recipient/delivery | Notification Center; no ROP alert decision |
| BR-07 | PR request is soft-link mock context/ack only | W2-PUR-LITE Procurement; no PR created here |
| BR-08 | version/event append-only and mock request idempotent | Audit and downstream replay |

Missing or stale upstream snapshot must not be treated as zero; positive advice blocks pending owner freshness SLA `[ASSUMED]`. Numeric precision/UoM and tenant-local effective-day semantics remain owner defaults in BRD §15. This card is a reference, not a guarantee of production readiness.

## 5. Integration
- **Depends on:** Item and Warehouse master soft references; Inventory/QHold onHand/held/asOf read snapshot; NC rule reference; W2-PUR-LITE PR mock. No W3-LITE GRN/PO/RTV or W5-FULL JE implementation is part of ROP.
- **Depended by:** Procurement may later consume positive PR candidate payload; NC may evaluate reorder candidate; CSQ may register policy-change profile after owner review. Consumers must treat all current acknowledgements as mock only.
- **Declarations:** DOA none in ROP; NTF draft `rop.reorder_candidate`; CSQ draft `master.changed`; DOCCFG none. Both drafts have unresolved central contract/event catalog.
- **Engine hooks:** no live ENG-NOTIFY, ENG-CSQ, PR engine, stock or movement emitter. Future adapters use FRD 02_API contracts and owner-reviewed declarations.
- **OQ owners:** Warehouse Product Owner (formula/effective date), Inventory/QHold owner (availability/freshness), DOA/Security owner (approval/roles), Procurement owner (PR contract), NC owner (candidate/rule), CSQ owner (profile/tube). (BRD §15, FRD 07_LOCKED)

*trace: §1 ← FRD 00_OVERVIEW/03_LOGIC · §2 ← FRD 04_DB/03_LOGIC · §3 ← FRD 02_API + 05_RULES · §4 ← FRD 05_RULES · §5 ← FRD 02_API/07_LOCKED + declaration briefs.*
