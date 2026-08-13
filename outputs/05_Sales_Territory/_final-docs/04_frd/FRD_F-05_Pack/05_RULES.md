# 05_RULES — F-05 Sales Territory

> Audience: BE + QA  
> Declarative source for business rules, validation, edges, errors and data/security enforcement.

---

## §5.1 Business Rules

| ID | Statement | Class/source | Enforced/Tested by |
|---|---|---|---|
| BR-ST-01 | Route is the primary Territory unit. | FIXED · PREBRIEF OB1 | schema · AC-01/03 |
| BR-ST-02 | One Route holds at most one salesperson reference. | FIXED · OB2 | schema · AC-13 |
| BR-ST-03 | Salesperson is optional soft reference; F-05 cannot create a person or require a live provider. | FIXED · OB3/PMBA | FN-03 · XT-01 |
| BR-ST-04 | `route_code` is tenant-unique, 2–12, uppercase `A-Z 0-9 - _`. | FIXED · OB8 | DB/FN-03 · AC-04 |
| BR-ST-05 | `route_code` is immutable after create. | FIXED · OB8 | API-04/FN-03/05 · AC-06 |
| BR-ST-06 | Province is optional; blank never increments province KPI. | FIXED · OB5/approved UI | query/read model · AC-04 |
| BR-ST-07 | Province uses a versioned offline 77-province dataset. | FIXED · OB5/11 | FN-03/asset · AC-11 |
| BR-ST-08 | Region values follow approved HTML; central/online values remain valid. | FIXED · approved UI | FN-03 · AC-04 |
| BR-ST-09 | No hard delete; only archive/restore. | FIXED · OB7 | no DELETE API · AC-07/08 |
| BR-ST-10 | Create/edit/archive/restore append immutable audit evidence. | FIXED · OB7 | FN-08/DB · AC-03/05/07/08 |
| BR-ST-11 | Customer/coverage/sales/workload are read-only future-derived and never current mutation inputs. | FIXED · OB6 | API §2.5 · AC-10/XT |
| BR-ST-12 | Master edits/archive do not mutate historical consumer snapshots. | FIXED · OB9 | snapshot boundary · XT-05 |
| BR-ST-13 | Archived Route is unavailable for new future transactions when consumers exist. | FIXED · OB7/9 | future contract only · XT-02–05 |
| BR-ST-14 | No approval/DOA workflow. | FIXED · OB10 | API/state · AC-14 |
| BR-ST-15 | Area/province overlap is allowed only as `[AI-DEFAULT]` pending OQ-09; no enforcement implemented. | WARNING | OQ-09 · AC-15 |
| BR-ST-16 | Green coverage starts at 25% only in prototype `[AI-DEFAULT]`; not a production rule. | WARNING | OQ-04 · AC-10 |
| BR-ST-17 | Capacity/workload formula is prototype `[AI-DEFAULT]`; no production Engine/API persistence. | DYNAMIC candidate | OQ-06 · AC-10 |
| BR-ST-18 | Route Type list/config owner unresolved `[AI-DEFAULT]`; use approved HTML values only for prototype compatibility. | CONFIGURABLE candidate | OQ-07 · AC-04 |
| BR-ST-19 | Map state changes only for valid interactive target/coordinates inside visible frame. | FIXED · PMBA feedback | FE guard · AC-12 |
| BR-ST-20 | External font/map/provider failure cannot break core master flow. | FIXED · offline constraint | UI states · AC-10/11 |

## §5.2 State Machine

```text
create(valid) → active ──archive──> archived
                  ^                  |
                  └────restore───────┘
```

| From | To | Action | Role | Conditions |
|---|---|---|---|---|
| none | active | create | sales_admin/system_admin | valid + unique code |
| active | archived | archive | sales_admin/system_admin | current version; no hard delete |
| archived | active | restore | sales_admin/system_admin | current version + unique code `[AI-DEFAULT]` |

No Draft/Submitted/Approved state exists.

## §5.3 Permission Matrix

| Role | View | Create | Edit | Archive | Restore | Workload/Map |
|---|---|---|---|---|---|---|
| sales_admin | all | yes | yes | yes | yes | yes |
| system_admin | all | yes | yes | yes | yes | yes |
| sales_manager | `[AI-DEFAULT]` hold until OQ-02 | no | no | no | no | hold |
| salesperson | `[AI-DEFAULT]` hold until OQ-02 | no | no | no | no | hold |

Backend denial is authoritative even if a prototype action is visible.

## §5.4 Validation

| Field/action | Rule | Error |
|---|---|---|
| `route_code` create | required + regex + unique | `BR_ROUTE_CODE_INVALID`, `ERR_ROUTE_CODE_CONFLICT` |
| `route_code` edit | cannot mutate | `BR_ROUTE_CODE_IMMUTABLE` |
| `route_name` | required, nonblank | `BR_REQUIRED_FIELD` |
| `route_type` | required and accepted config/value | `BR_ROUTE_TYPE_INVALID` |
| `region` | required and approved value | `BR_REGION_INVALID` |
| `province_code` | null or local dataset member | `BR_PROVINCE_INVALID` |
| `salesperson_ref` | nullable opaque string; no current existence call | `BR_SALESPERSON_REF_INVALID` only for structural format |
| `universe` | null/blank or integer ≥0 | `BR_UNIVERSE_INVALID` |
| archive/restore | state + version + permission | state/409/403 errors below |

## §5.5 Confirmed Edge Cases

| ID | Scenario | Required handling | Test |
|---|---|---|---|
| EC-01 | duplicate/invalid code or missing required | reject; preserve drawer values; field/generic validation | AC-04 |
| EC-02 | province blank | save valid Route; province KPI unchanged | AC-04 |
| EC-03 | salesperson provider absent | save nullable/fixture soft ref without outbound call | XT-01 |
| EC-04 | future salesperson inactive/deleted | behavior unresolved; do not block silently `[AI-DEFAULT]` | OQ-03/XT-01 |
| EC-05 | linked customer count available in future | archive warning may show count; current absence does not block | XT-02 |
| EC-06 | universe/coverage source absent | show blank/mock/unavailable; no fake production value | AC-10 |
| EC-07 | archive/restore | state change + immutable audit; no deletion | AC-07/08 |
| EC-08 | pointer outside map frame/side list | zero map hover/tooltip/selection/state mutation | AC-12 |
| EC-09 | master edited/archived | historical snapshot remains byte/value stable | XT-05 |
| EC-10 | any future provider absent | core master CRUD/state remains available | XT-01–05 |

## §5.5.1 Lane Probe Defaults — Not Business-Approved

| Probe | Default | Error/Test |
|---|---|---|
| PR-2 stale data | `If-Match` + version; first committed write wins `[AI-DEFAULT]` | `ERR_STALE_DATA`, AC-16 |
| PR-3 permission mid-flight | reauthorize on every mutation `[AI-DEFAULT]` | `ERR_PERMISSION_REVOKED`, AC-17 |
| PR-4 network failure | retry only with same idempotency key `[AI-DEFAULT]` | AC-18 |
| PR-7 double submit | same key/body returns cached result; different body 409; TTL proposed 24h `[AI-DEFAULT]` | `ERR_IDEMPOTENCY_CONFLICT`, AC-18 |
| restore conflict | block restore `[AI-DEFAULT]` | `ERR_RESTORE_CODE_CONFLICT`, AC-19 |
| local asset corrupt | contained error, core structure available `[AI-DEFAULT]` | AC-11 |

## §5.6 Error Catalog

| Code | HTTP | Cause |
|---|---:|---|
| `ERR_INVALID_QUERY` | 400 | invalid list filters/pagination |
| `ERR_NOT_AUTHENTICATED` | 401 | missing/invalid authentication |
| `ERR_INSUFFICIENT_ROLE` | 403 | role lacks action |
| `ERR_PERMISSION_REVOKED` | 403 | role changed before mutation `[AI-DEFAULT]` |
| `ERR_ROUTE_NOT_FOUND` | 404 | Route missing/out of scope |
| `ERR_ROUTE_CODE_CONFLICT` | 409 | unique code conflict |
| `ERR_STALE_DATA` | 409 | optimistic version mismatch `[AI-DEFAULT]` |
| `ERR_IDEMPOTENCY_CONFLICT` | 409 | same key/different body `[AI-DEFAULT]` |
| `ERR_RESTORE_CODE_CONFLICT` | 409 | restore would violate code uniqueness `[AI-DEFAULT]` |
| `BR_ROUTE_CODE_INVALID` | 422 | format/length invalid |
| `BR_ROUTE_CODE_IMMUTABLE` | 422 | edit attempts code mutation |
| `BR_REQUIRED_FIELD` | 422 | name/type/region missing |
| `BR_ROUTE_TYPE_INVALID` | 422 | value not in approved config |
| `BR_REGION_INVALID` | 422 | unsupported region |
| `BR_PROVINCE_INVALID` | 422 | non-null province not in local dataset |
| `BR_UNIVERSE_INVALID` | 422 | negative/non-integer universe |
| `BR_INVALID_STATE_TRANSITION` | 422 | archive/restore from wrong state |
| `ERR_AUDIT_WRITE_FAILED` | 500 | atomic audit append failed; mutation rolls back |

User-facing messages use approved HTML text where it exists. New API conflict copy is not invented here; UI should map i18n keys only after BA copy approval.

## §5.7 Security and D-CLASS

### Applied controls

- Authenticate all access; least privilege role/scope authorization.
- Reauthorize mutation `[AI-DEFAULT]`.
- Tenant isolation `[AI-DEFAULT]` pending architecture contract.
- Server validation and DB constraints; client validation is convenience only.
- Append-only mutation audit; rollback if success audit cannot write.
- Avoid PII in operational logs; actor/salesperson references are Confidential.
- Geo asset must be local, versioned and integrity checked.

### Data classification enforcement

| Layer | Internal | Confidential |
|---|---|---|
| DB | tenant isolation `[AI-DEFAULT]` | column/role access |
| API | authenticated | scope/role check; minimum response |
| UI | normal | do not expose unauthorized salesperson/actor detail |
| Audit | mutation | access/mutation per platform policy; immutable |
| Export | platform internal policy | exclude/mask without authorization |

No Restricted field and no Public default. Full dictionary: `04_DB.md §4.2/§4.5/§4.6`.

## §5.8 Operational Requirements

- Proposed p95 ≤2s and save ≥99% are `[AI-DEFAULT]` OQ-21, not hard business rules.
- Critical integrity targets remain zero: accepted invalid/duplicate, hard delete, historical snapshot mutation.
- Monitor validation rejects, permission denial, audit failure, geo asset failure and future provider absence without treating mock metrics as production.

