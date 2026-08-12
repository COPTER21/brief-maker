# 07_LOCKED_DECISIONS — F-LOCATION-MASTER-001 Warehouse & Bin

## §7.0 Scope Lock — IMMUTABLE

| LOCK-ID | Locked decision | Source | FRD status |
|---|---|---|---|
| LOCK-LOC-01 | Company only via `branch_id` → `T_branch`; no `company_id`; children inherit via Warehouse | HANDOFF Locked Scope #1 | ✅ API/DB/rules aligned |
| LOCK-LOC-02 | no F-INV build-out, Geo schema, GRN/Putaway/RTV/Pick-Pack-Ship; Inventory edge only `storage_uom` lock + `hasStock` | HANDOFF #2 | ✅ contract seam only |
| LOCK-LOC-03 | no DOA; RBAC capability is `canManage` | HANDOFF #3 | ✅ |
| LOCK-LOC-04 | CI = CUBE Warm Light v8 | HANDOFF #4 | ✅ UI points to Sync Read |
| LOCK-LOC-05 | inferred assumptions marked `[AI-DEFAULT]` | HANDOFF #5 | ✅ |
| LOCK-LOC-06 | `warehouse-bin.html` is source of truth for UI microcopy; do not invent | HANDOFF #6 | ✅ exact text anchored |

Scope Lock Ref: `outputs/06_Warehouse-Bin/HANDOFF.md`; signed form/date: ไม่พบข้อมูลในบทสนทนา.

Drift found: three prototype mock handler gaps are recorded in `00_OVERVIEW §0.9`; FRD does not redefine visible UI.

## §7.1 Locked Decisions

### LD-LOC-01: Five-level hierarchy with direct Area exception

- Decision: Warehouse › Zone › Area › Rack › Location; Location parent is Rack XOR an Area with `allows_direct=true`
- Implications: XOR DB constraint, typed parent validation, deterministic path engine
- Reversibility: HARD after stock references exist

### LD-LOC-02: Soft Branch reference

- Decision: store only `branch_id`; active-only picker; resolve saved inactive reference; no cross-module cascade
- Rationale: follows Company BR-09/EC-10 and preserves historical Warehouse
- Reversibility: MEDIUM

### LD-LOC-03: One storage UOM per Location with Inventory guard

- Decision: exactly one `storage_uom`; mutation/decommission checks Inventory `hasStock`
- Rationale: storage contract consistency without implementing F-INV
- Reversibility: HARD if changed to multi-UOM

### LD-LOC-04: Derived `full`

- Decision: only trusted Inventory capacity signal sets `full`; user cannot set it manually; prior state is restored when cleared
- Reversibility: MEDIUM

### LD-LOC-05: Atomic generation

- Decision: `ENG-LOC-GEN` returns a pure plan and FN-18 commits every Rack/Location/audit in one transaction
- Reversibility: EASY contractually, but partial mode would require new UX

### LD-LOC-06: WORM audit in mutation transaction

- Decision: every mutation and derived status change appends immutable audit; audit failure rolls back business write
- Reversibility: HARD/compliance-sensitive

### LD-LOC-07: FULL FRD variant

- Decision: FULL because lifecycle has six states, cross-module guards, bulk transaction and two engine candidates
- Implications: dedicated `07_LOCKED_DECISIONS.md` and `INDEX.md`

## §7.2 Convention Deviations

### CD-LOC-01: Generic typed node read/delete routes

- Convention default: separate resource route per entity
- Deviation: GET/DELETE `/location-nodes/{node_type}/{id}` for common hierarchy operations
- Reason: one UI renderer and identical parent guard/audit orchestration; create/update remain typed routes
- Guard: whitelist node types; never construct table identifiers from raw input

### CD-LOC-02: Action route for decommission

- Deviation: POST `/locations/{id}/decommission` instead of generic status PATCH
- Reason: stock precondition, terminal semantics and explicit audit differ from ordinary status change

## §7.3 Pending Decisions

OQ-LOC-01..08 remain pending as listed in `00_OVERVIEW §0.8`. Until closed, safe defaults apply only where marked `[AI-DEFAULT]`; owners must not treat them as signed business decisions.

## §7.4 Architecture Tradeoffs

| ID | Tradeoff | Accepted position |
|---|---|---|
| AT-01 | normalized five tables vs polymorphic single node table | normalized tables for constraints/readability |
| AT-02 | synchronous stock guard vs cached/event state | synchronous/fail-closed decision window `[AI-DEFAULT]` pending OQ-LOC-08 |
| AT-03 | hard delete vs historical continuity | parent delete guarded; Location decommissioned |
| AT-04 | config-backed types vs hard enum | config-backed seed; behavior defaults deferred |

## §7.5 Decisions Deferred to Implementation Review

| Item | Owner | Deadline/status |
|---|---|---|
| exact Geo contract | Strike + พี่เบิร์ด | before Dev handoff; pending |
| hierarchy NON-STANDARD approval | Chin | before Dev handoff; pending |
| type defaults/re-parent/delete/UOM permission | Strike | before Phase 1; pending |
| engine global IDs | Architect | before Dev handoff; pending |
| Inventory stock/capacity transport | Inventory + Architect | before guarded API implementation; owner name ไม่พบข้อมูลในบทสนทนา |
| batch maximum and audit retention | Product/Platform owner | ไม่พบข้อมูลในบทสนทนา |

## §7.6 References

- BRD: `outputs/06_Warehouse-Bin/03_BRD/BRD_Warehouse_Bin.md`
- UI: `outputs/06_Warehouse-Bin/warehouse-bin.html`
- Company reference: `outputs/01_Company/04_FRD/FRD_F-ORG-001_Pack/`
- rules/tests: `05_RULES.md`, `06_TESTS.md`
