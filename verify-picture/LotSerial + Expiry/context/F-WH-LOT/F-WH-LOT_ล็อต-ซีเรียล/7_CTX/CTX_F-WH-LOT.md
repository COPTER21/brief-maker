# CTX — F-WH-LOT: Lot/Serial + Expiry

> derived from: FRD F-WH-LOT v1, files 00–08 · generated: 2026-09-14 · module: Warehouse · status: proposed implementation
> Derived reference for cross-feature planning. FRD remains source of truth for implementation; regenerate CTX after any FRD revision. Browser acceptance remains open.

## 1. Summary
Warehouse operators record lot/serial identities under an effective per-item tracking and expiry policy. Other features can read ranked eligible lots and exact-lot movement refs. FEFO applies only to expiry-enabled items; otherwise the recommendation uses receipt order. The feature does not reserve, issue, receive or mutate on-hand inventory. Source transactions and notification/CSQ outcomes remain external contracts. (FRD 00_OVERVIEW, 03_LOGIC)

## 2. Data contract
### Owned entities
| Entity | Key | Cross-feature fields | Ownership/invariant |
|---|---|---|---|
| `T_item_tracking_policy` | tenant_id + item_code + version | tracking_mode, expiry_enabled, effective_date | versioned; no expiry when mode=none |
| `T_lot_identity` | tenant_id + lot_id | item_code, lot_code, serial_code?, expiry_date?, warehouse_ref? | soft Item/Warehouse refs; unique tenant+item+nonnull serial |
| `T_lot_audit` | tenant_id + event_id | subject_ref, action, before_json?, after_json?, idempotency_key, created_by/date | append-only; unique tenant+idempotency key |

All owned rows include authenticated actor and server timestamps. `before_json`/`after_json` and idempotency key are Confidential; actor ID is PII flagged. Retention and actor classification are central security decisions. (FRD 04_DB §§4.1–4.6)

### Read models and relationships
- W3-LITE movement adapter: `movement_id,tenant_id,lot_id,item_code,kind,qty,at,source_ref{type,id},from_ref,to_ref,previous_movement_id`; read-only, append-only upstream, mock until contract is ready. No owned movement table. (FRD 02_API API-X1; 04_DB §4.1)
- Availability adapter: on-hand and held snapshot by item/warehouse/lot; QHold is retained on-hand but not available. This feature computes eligible candidates and does not write balances. (FRD 03_LOGIC FN-04; 05_RULES BR-04)
- Item and Warehouse references are soft snapshots, no hard FK into master storage. (FRD 04_DB §§4.1,4.5)

### Enums and derived state
| Field | Complete values | Owner |
|---|---|---|
| tracking_mode | `none`, `lot`, `serial` | this feature's versioned policy |
| display status | `พร้อมใช้`, `กักอยู่`, `หมดอายุ` | derived from upstream availability/date; never freely edited |
| movement kind | W3-LITE contract, not enumerated here | W3-LITE |
(FRD 04_DB §4.4)

## 3. API surface
All paths are **proposed [ASSUMED]** until API owner confirms. Tenant auth, permission, correlation ID, UPPER_SNAKE error envelope required; mutating operations take `Idempotency-Key`. (FRD 02_API)

| ID | Method/path | Main request | Main response |
|---|---|---|---|
| API-01 | GET `/api/warehouse/lot-identities` | item_code?, warehouse_ref?, query?, status?, sort?, page? | rows + count |
| API-02 | POST `/api/warehouse/lot-identities` | item_code, lot_code, serial_code?, expiry_date?, key | 201 lot_id/status |
| API-03 | PUT `/api/warehouse/items/{item_code}/tracking-policy` | tracking_mode, expiry_enabled, effective_date, expected_version, key | policy version |
| API-04 | GET `/api/warehouse/lot-recommendations` | item_code, warehouse_ref, at_date, required_qty? | ranked candidates + available_qty; no reservation id |
| API-05 | GET `/api/warehouse/lots/{lot_id}/movements` | direction?, page? | immutable refs + predecessor/successor |
| API-06 | GET `/api/warehouse/lots/{lot_id}/events` | page? | append-only audit rows |

API-X1 W3-LITE movement reader, API-X2 NC rules link/candidate envelope, API-X3 Picking recommendation consumer and API-X4 CSQ master.changed producer are mock/TODO interfaces. Errors and replay behavior remain in FRD 02_API; no live downstream outcome is evidenced by the prototype.

### Events
| Event | Trigger | Key payload / status |
|---|---|---|
| `master.changed` | successful item policy change | CSQ brief envelope; registration/evaluation external [ASSUMED contract] |
| expiry candidate to NC | NC rule evaluation boundary | tenant_id,item_code,lot_id,expiry_date,ref_id,idempotency_key; NC owns threshold/recipients/channel; `ntf` chip divergence unresolved |
(FRD 02_API API-X2/X4, 03_LOGIC §3.4, 5_DECLARATIONS)

## 4. Cross-boundary rules
| Rule | Contract for consumers |
|---|---|
| BR-04 | eligible quantity is `max(0,on_hand-held)` and must be positive; expiry-enabled item requires unexpired date |
| BR-05 | expiry-enabled item uses FEFO by expiry; non-expiry item uses receipt order; stable tie-break `[ASSUMED]` |
| BR-06 | recommendation is read-only; Picking owns reserve/issue |
| BR-07 | GRN/Transfer movement refs are W3-LITE read-only mocks until upstream contract; never fabricate source or mutate history |
| BR-08 | identity/config audit and movement ledger are append-only; no hard delete |
| BR-09 | near-expiry threshold and delivery belong to NC; no local channel selection |
(FRD 05_RULES)

## 5. Integration
- **Depends on:** Item and Warehouse master soft references; W3-LITE GRN/Transfer movement read mock; upstream availability/QHold snapshot; NC rule view; central User Access. (FRD 02_API/04_DB)
- **Depended by:** Picking can consume API-04 candidate list, but retains all reservation/issue responsibility. SCAN and CYCLE depend on lot identity/trace contracts in W4. (FRD 02_API API-X3; W4 graph)
- **Declarations:** DOA no approval here; CSQ brief for proposed `master.changed` [ASSUMED contract], no 7C result; NTF detect/chip DIVERGENCE pending registry owner; DOCCFG not applicable to console/master. (FRD 00_OVERVIEW, 5_DECLARATIONS)
- **Engine hooks:** NC/ENG-NOTIFY and CSQ external; no new shared engine. `rankEligibleLots` is scope-local pure logic. (FRD 03_LOGIC §3.2)
- **Owners before integration:** Warehouse Product Owner for serial qty, FEFO ties, expiry/availability/effective policy; W3-LITE for source payload; NC/registry for notification divergence; CSQ owner for contract registration; API owner for paths. (FRD 02_API/03_LOGIC; HANDOFF)

*Trace: §1 ← FRD 00_OVERVIEW/03_LOGIC; §2 ← FRD 04_DB; §3 ← FRD 02_API; §4 ← FRD 05_RULES; §5 ← FRD 02_API/03_LOGIC and declarations. This card is a reference, not a replacement for the FRD Pack.*
