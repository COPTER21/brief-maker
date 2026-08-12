# 05_RULES — F-LOCATION-MASTER-001 Warehouse & Bin

## §5.1 Business Rules

| ID | Declarative rule | Enforced by | Error |
|---|---|---|---|
| BR-LOC-01 | hierarchy is Warehouse › Zone › Area › Rack › Location | DB/FN-01/ENG-HIER-PATH | `BR_HIERARCHY_INVALID` |
| BR-LOC-02 | Location parent is Rack XOR Area; direct Area requires `allows_direct` | DB/FN-14 | `BR_AREA_DIRECT_NOT_ALLOWED` |
| BR-LOC-03 | code is unique within its parent | unique index/FN-14 | `BR_LOCATION_CODE_DUPLICATE` |
| BR-LOC-04 | 10 initial Location types are config-backed and schema-extensible | type config/FN-13 | `BR_LOCATION_TYPE_INVALID` |
| BR-LOC-05 | each Location has exactly one `storage_uom` | DB/FN-13 | `BR_STORAGE_UOM_REQUIRED` |
| BR-LOC-06 | `storage_uom` cannot change while `hasStock=true` | FN-15/FN-20 | `BR_STORAGE_UOM_LOCKED_HAS_STOCK` |
| BR-LOC-07 | blocked/frozen requires reason | DB/FN-16 | `BR_STATUS_REASON_REQUIRED` |
| BR-LOC-08 | `full` is derived and cannot be set manually | FN-16/FN-25 | `BR_FULL_DERIVED_ONLY` |
| BR-LOC-09 | decommission requires `hasStock=false` | FN-21 | `BR_DECOMMISSION_HAS_STOCK` |
| BR-LOC-10 | `[AI-DEFAULT]` delete parent with any child is blocked pending OQ-LOC-04 | FN-12 | `BR_PARENT_HAS_CHILDREN` |
| BR-LOC-11 | generation is all-or-nothing | FN-18/DB transaction | `BR_BULK_TEMPLATE_INVALID` |
| BR-LOC-12 | Branch picker active-only; saved inactive Branch resolves; no cascade | FN-22 | `BR_BRANCH_INVALID` |
| BR-LOC-13 | Geo cascade/postcode uses external Geo contract only | FN-24 | `ERR_DEPENDENCY_UNAVAILABLE` |
| BR-LOC-14 | every mutation appends immutable audit in same transaction | FN-23 | `ERR_AUDIT_WRITE_FAILED` |
| BR-LOC-15 | `[AI-DEFAULT]` re-parent blocked when node has children/Location has stock pending OQ-LOC-05 | update functions | `BR_REPARENT_NOT_ALLOWED` |
| BR-LOC-16 | current UI allows UOM mutation for `canManage` + no stock; final policy pending OQ-LOC-06 | API auth/FN-15/20 | `ERR_INSUFFICIENT_ROLE` |
| BR-LOC-17 | no type-driven default is enforced until OQ-LOC-03 resolves | FN-13 | — |

## §5.2 Location State Machine

```text
create → active ↔ inactive
           ├──────↔ blocked (reason required)
           ├──────↔ frozen  (reason required)
           └─ Inventory capacity → full → previous operational state
active/inactive ── no stock ──> decommissioned (terminal V1)
```

| From | To | Actor | Guard |
|---|---|---|---|
| create | active | `canManage` | valid fields/parent/unique |
| active/inactive/blocked/frozen | active/inactive | `canManage` | version + permission |
| active/inactive | blocked/frozen | `canManage` | non-empty reason |
| operational | full/previous | trusted integration | Inventory capacity signal |
| active/inactive | decommissioned | `canManage` | `hasStock=false` |

Manual transition to `full` or from `decommissioned` is forbidden. Whether blocked/frozen may decommission is not specified; V1 limits action to active/inactive as BRD table states.

## §5.3 Permission Matrix

| Capability | Read | Parent CRUD | Location CRUD | Status | Bulk | Derived full |
|---|---:|---:|---:|---:|---:|---:|
| authenticated user | ✅ | — | — | — | — | — |
| `canManage` | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| trusted Inventory integration | storage contract | — | — | — | — | ✅ |

Permission is re-evaluated on each mutation; no DOA/approver role.

## §5.4 Field Validation

| Field/action | Rule | UI text source | Code |
|---|---|---|---|
| code/name | required | `กรุณากรอกรหัส`, `กรุณากรอกชื่อ` | `ERR_VALIDATION_FAILED` |
| Warehouse branch | required + resolvable | `กรุณาเลือกสาขาสังกัด` | `BR_BRANCH_INVALID` |
| controlled temperature | min/max required; min ≤ max | `กรุณากรอกช่วงอุณหภูมิ` | `BR_TEMPERATURE_RANGE_INVALID` |
| parent | exactly one; exists same tenant | `กรุณาเลือก Rack` / `กรุณาเลือก Area` | `BR_LOCATION_PARENT_INVALID` |
| direct Area | `allows_direct=true` | `Area นี้ไม่อนุญาตวางตำแหน่งตรง — เพิ่ม Rack ก่อน` | `BR_AREA_DIRECT_NOT_ALLOWED` |
| Location code | required + sibling unique | `กรุณากรอกรหัสตำแหน่ง`, `รหัสซ้ำภายใน parent เดียวกัน` | duplicate code above |
| capacity | > 0 | `ความจุต้องมากกว่า 0` | `BR_CAPACITY_INVALID` |
| blocked/frozen reason | trim length > 0 | `กรอกเหตุผลก่อน` | `BR_STATUS_REASON_REQUIRED` |
| generation dimensions/count | positive; patterns valid; output unique | `template ไม่ถูกต้อง` | `BR_BULK_TEMPLATE_INVALID` |

## §5.5 Edge Cases / Activated Probes

| EC | Scenario | Resolution | Test |
|---|---|---|---|
| EC-01 | two editors save same version | first wins; second `ERR_STALE_DATA` | TC-CC-01 |
| EC-02 | permission removed while drawer open | commit recheck rejects `ERR_PERMISSION_REVOKED` | TC-PR-01 |
| EC-03 | response lost after successful create/bulk | replay same idempotency key returns original result | TC-NF-01 |
| EC-04 | batch contains one duplicate/invalid code | rollback entire generation | TC-BULK-01 |
| EC-05 | bulk UOM selection mixes stock/no-stock | update no-stock, skip stocked, return counts; write failure rolls back allowed subset | TC-UOM-01 |
| EC-06 | Inventory provider unavailable | fail closed; no UOM/decommission mutation | TC-INV-01 |
| EC-07 | Branch becomes inactive after save | existing ref displays; picker prevents new selection | XT-01 |
| EC-08 | capacity makes full then frees | derived full then restore recorded prior state | TC-STATE-02 |
| EC-09 | parent delete races with child create | DB constraint/transaction blocks delete | TC-DEL-01 |
| EC-10 | hierarchy has cycle/orphan corrupted data | engine rejects graph and emits anomaly; no cross-tenant nodes | TC-HIER-02 |
| EC-11 | double-click submit | frontend busy + backend idempotency; one record/audit | TC-ID-01 |
| EC-12 | HTML mock gap on edit/decommission/bulk | production persistence/audit/full batch verified | TC-DRIFT-01..03 |

## §5.6 Error Catalog

| Code | HTTP | Message key / cause |
|---|---:|---|
| `ERR_VALIDATION_FAILED` | 400 | `error.validation.failed` |
| `ERR_NOT_AUTHENTICATED` | 401 | `error.auth.unauth` |
| `ERR_INSUFFICIENT_ROLE` | 403 | `error.auth.role` |
| `ERR_PERMISSION_REVOKED` | 403 | `error.auth.revoked` |
| `ERR_NOT_FOUND` | 404 | `error.notfound` |
| `ERR_STALE_DATA` | 409 | `error.concurrency.stale` |
| `ERR_DUPLICATE_IDEMPOTENCY_KEY` | 409 | same key, different body |
| `ERR_DEPENDENCY_UNAVAILABLE` | 503 | Company/Geo/Inventory unavailable |
| `ERR_AUDIT_WRITE_FAILED` | 500 | audit append failed; business write rolls back |
| `BR_HIERARCHY_INVALID` | 422 | invalid level/parent graph |
| `BR_LOCATION_PARENT_INVALID` | 422 | parent XOR/existence failed |
| `BR_AREA_DIRECT_NOT_ALLOWED` | 422 | direct Area disallowed |
| `BR_LOCATION_CODE_DUPLICATE` | 409 | duplicate sibling code |
| `BR_LOCATION_TYPE_INVALID` | 422 | inactive/unknown type |
| `BR_STORAGE_UOM_REQUIRED` | 422 | missing UOM |
| `BR_STORAGE_UOM_LOCKED_HAS_STOCK` | 422 | stocked Location UOM lock |
| `BR_STATUS_REASON_REQUIRED` | 422 | blocked/frozen reason missing |
| `BR_FULL_DERIVED_ONLY` | 422 | manual full attempt |
| `BR_DECOMMISSION_HAS_STOCK` | 422 | stock guard |
| `BR_PARENT_HAS_CHILDREN` | 409 | delete guard |
| `BR_BULK_TEMPLATE_INVALID` | 422 | invalid generation plan |
| `BR_BRANCH_INVALID` | 422 | Branch missing/not selectable |
| `BR_REPARENT_NOT_ALLOWED` | 422 | current safe default |
| `BR_TEMPERATURE_RANGE_INVALID` | 422 | controlled range invalid |
| `BR_CAPACITY_INVALID` | 422 | capacity ≤ 0 |

UI displays exact HTML microcopy for known validation conditions in `01_UI §1.5`; new backend/system errors resolve through i18n keys, not hardcoded invented screen text.

## §5.7 Security Controls

- D2 authenticated sessions via platform; no credential handling in feature
- D9 all mutations append WORM audit, including rejected guarded attempts where platform policy requires `[AI-DEFAULT]`
- D15 admin/master actions record actor, before/after, reason, correlation and result
- D17 `tenant_id` RLS plus same-tenant parent validation
- data classification is Internal; no PII fields; secrets are never logged
- API authorizes by `canManage`; hiding controls is not authorization

## §5.8 Compliance

Specific statutory retention duration or regulatory report: ไม่พบข้อมูลในบทสนทนา. Platform audit/data-retention policy applies pending owner confirmation.
