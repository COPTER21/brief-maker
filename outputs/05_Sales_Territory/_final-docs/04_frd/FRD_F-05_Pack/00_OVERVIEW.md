# 00_OVERVIEW — F-05 Sales Territory

> Audience: PM, BA, FE, BE, QA, DBA  
> Source order: approved scope lock → BRD business intent → approved HTML for actual UI/route → PREBRIEF/CHECKLIST/Central Plan baseline.

---

## §0.1 Document Control

| Field | Value |
|---|---|
| Feature ID | `F-05` / `F-SALES-TERRITORY` |
| Feature Name | Sales Territory (ผังเขตขาย) |
| Module | Sales · Field Operations |
| Variant | **STANDARD** |
| Status | **APPROVED WITH WARNINGS — implementation values marked `[AI-DEFAULT]` remain unapproved** |
| FRD Version | 1.0 · 2026-08-13 |
| Generator | frd-generator-v6.1 · HTML-first · Lane Mode |
| Source BRD | `../../03_brd/BRD_Sales_Territory.md` · 28/28 review checks · critical 0 |
| Source HTML | `../../01_prototype/sales-territory.html` · approved UI source of truth |
| Business baseline | PREBRIEF + CHECKLIST + Central Plan v2 |
| Companion declarations | Not run: DOA/DOCCFG/NTF are outside the user-approved skill list and not required by scope |

**Sync Read log:** `html-generator-v8` is the highest/current installed HTML generator and supersedes the v6 fallback named by this FRD skill. Observed patterns and HTML fidelity were checked against v8; no CI values, iron-rule count or shell dimensions are pinned in this pack.

### Variant decision

Fallback inputs: pages=1 route, states=2 (`active`, `archived`), approval=No, money=No. This initially qualifies for LEAN. It is upgraded to **STANDARD** because BRD has 20 rules, multiple mutation paths and confirmed/AI edge cases that require an auditable `05_RULES.md`. It is not FULL: no multi-step approval, no financial algorithm, no complex state machine and no reusable engine.

## §0.2 Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-13 | Initial HTML-first STANDARD pack |

## §0.3 Scope

### In scope

- Standalone Route master: list/search/status filter/create/view/edit/archive/restore.
- One hash route `#/sales-territory` with three tabs and drawers/modal exactly as approved HTML.
- Immutable unique route code, required name/type/region, optional province/salesperson soft-ref/universe.
- Active/Archived lifecycle, no hard delete, append-only audit evidence.
- Offline local Thailand map; pointer outside visible map frame produces no map state change.
- Workload/coverage/map mock/read-only states are visibly non-production until providers exist.
- Future-safe snapshot DTO and hook declarations only; no current runtime dependency on future modules.

### Out of scope

- Implementing Sales Team/Salesperson, Customer Master, Sales Order, Sales Target or Visit Operation.
- Calling endpoints or emitting integration events that imply those five modules currently exist.
- DOA/approval, hard delete, multi-owner Route, GPS/full route-line/production choropleth, overlap enforcement.
- Audit Trail UI until OQ-08 closes; audit storage remains required.
- Production monitoring/dashboard screens; §17/§18 BRD items are operational requirements, not extra HTML pages.

## §0.4 Roles and COSO

| Role | Current release authority | COSO touchpoint |
|---|---|---|
| `sales_admin` | view/create/edit/archive/restore | Maker |
| `system_admin` | view/create/edit/archive/restore | Maker / control operator |
| `sales_manager` | **not granted until OQ-02 closes** | `[AI-DEFAULT]` candidate viewer only |
| `salesperson` | **not granted until OQ-02 closes** | `[AI-DEFAULT]` candidate own-scope viewer only |
| System | validation, authorization, audit, state transition | Checker/System control |
| Approver | N/A | Feature has no approval/DOA |

Mutation permission is rechecked server-side at request time `[AI-DEFAULT]` (OQ-17).

## §0.5 Dependencies

### Current hard dependencies

- Authentication/authorization platform.
- Persistence and append-only audit facility.
- Versioned local geo asset for 77 provinces.

### Future-only contracts — unavailable now

| Future module | Intended direction | Release behavior |
|---|---|---|
| Sales Team/Salesperson | soft reference into Route | mock/blank; no network call |
| Customer Master | customer assignment/coverage | labelled mock/unavailable |
| Sales Order | order/sales metrics + snapshot consumer | labelled mock/unavailable |
| Sales Target | target by territory | disabled hook |
| Visit Operation | route/visit context | disabled hook |

## §0.6 Architecture boundary

`UI → /api/v1/sales-territories → scope-local Functions → DB + audit`

- HTTP transport stays in `02_API.md`.
- Business orchestration stays in `03_LOGIC.md`.
- Declarative constraints/errors stay in `05_RULES.md`.
- No reusable CUBIC Engine is justified in this release.
- Concrete framework, hosting and tenant mechanism are platform decisions; tenant isolation is `[AI-DEFAULT]` pending OQ-FRD-01.

## §0.7 Security Context

- Authentication: required for all APIs.
- Authorization: least privilege; mutations only `sales_admin`/`system_admin` until OQ-02.
- Audit: every mutation with actor/time/result/before/after; append-only.
- PII: `salesperson_ref` and actor IDs are Confidential + PII overlay.
- No financial fields.
- Security domains applied: authentication/session, authorization/admin actions, PII protection, audit logging, tenant isolation `[AI-DEFAULT]`, local asset integrity.

### §0.7.1 Data Classification Summary

Highest level: **Confidential**. No Restricted field is defined, so Restricted Resources registration is not required by this schema. Default for unspecified fields is Internal; Public is never inferred.

## §0.8 Open Questions / Defaults

BRD OQ-01–OQ-21 are propagated below; defaults are not approvals.

| ID | Question/default | Blocking point | Owner |
|---|---|---|---|
| OQ-01 | future Salesperson source/identifier | integration design | PM/BA |
| OQ-02 | Manager/Salesperson permissions | role/API freeze | PM/BA/Security |
| OQ-03 | inactive/deleted future Salesperson behavior | integration design | PM/BA |
| OQ-04 | coverage green threshold 25% `[AI-DEFAULT]` | workload production rule | PM/BA |
| OQ-05 | `universe` editable/imported/derived contract | data/API freeze | PM/BA |
| OQ-06 | capacity/workload formula owner/source | workload production rule | PM/BA |
| OQ-07 | Route Type values/config owner | config/schema freeze | PM/BA |
| OQ-08 | Audit Trail UI vs backend evidence | UI scope freeze | PM/BA |
| OQ-09 | overlap allowed confirmation | business-rule freeze | PM/BA |
| OQ-10 | full choropleth/route line/GPS remains out of scope | roadmap | PM/BA |
| OQ-11 | province with multiple regions map color | map production | PM/BA |
| OQ-12 | local 77-province geo dataset owner/version | build/map production | Tech Lead |
| OQ-13 | map KPI/legend when future data absent | UAT | PM/BA |
| OQ-14 | `R-BK-01` fixture vs production seed | migration/seed | PM/BA |
| OQ-15 | audit retention `[AI-DEFAULT: central policy]` | production policy | Security/Compliance |
| OQ-16 | concurrency `[AI-DEFAULT: optimistic lock]` | API design | Tech Lead |
| OQ-17 | reauthorize on mutation `[AI-DEFAULT: yes]` | API/security design | Security |
| OQ-18 | timeout/fallback for future providers | future integration | Tech Lead |
| OQ-19 | local geo asset failure behavior `[AI-DEFAULT: contained error]` | UAT | PM/BA/Tech Lead |
| OQ-20 | restore code conflict `[AI-DEFAULT: block]` | API/state freeze | PM/BA |
| OQ-21 | M04/M05/performance profile approval | NFR freeze | PM/BA/Tech Lead |
| OQ-FRD-01 | canonical tenant context/RLS contract `[AI-DEFAULT: tenant_id + platform context]` | schema freeze | Architect |
| OQ-FRD-02 | idempotency result retention `[AI-DEFAULT: 24h]` | API implementation | Tech Lead |

### Lane Mode probes applied

- PR-2 stale data → `[AI-DEFAULT]` optimistic locking with `If-Match`/version, tied to OQ-16.
- PR-3 permission mid-flight → `[AI-DEFAULT]` recheck on every mutation, tied to OQ-17.
- PR-4 network failure + PR-7 double submit → `[AI-DEFAULT]` idempotency key on mutations; retention OQ-FRD-02.
- PR-5/PR-6/PR-8/PR-9 not triggered: no bulk, draft wizard, cancellation compensation, finance/inventory counter.

## §0.9 Glossary

| Term | Definition |
|---|---|
| Route | Primary business unit of Sales Territory |
| Universe | Optional target/store universe value; business source unresolved |
| Soft reference | Identifier stored without current hard FK/runtime dependency |
| Snapshot DTO | Immutable territory dimensions copied into a future transaction |
| Fixture | Prototype-only data, not production seed |

## §0.10 Pack Navigation

| File | Purpose |
|---|---|
| `00_OVERVIEW.md` | scope, warnings, locks, coverage |
| `01_UI.md` | one-route UI extraction and API mapping |
| `02_API.md` | current HTTP contracts + future non-runtime declarations |
| `03_LOGIC.md` | functions and R8 trace |
| `04_DB.md` | tables, dictionary, classification |
| `05_RULES.md` | BR-01–20, validation, edge/error/security |
| `06_TESTS.md` | AC, tests, cross-module safeguards, Phase 3.5 report |

## §0.11 Scope Lock

Scope Lock Ref: PREBRIEF/CHECKLIST + approved HTML GATE + PM/BA decisions on 2026-08-13; no separate signed RIF.

| Lock | Immutable decision |
|---|---|
| LOCK-01 | Route code unique, 2–12, `A-Z 0-9 - _`, immutable after create |
| LOCK-02 | Province optional; blank never increments province KPI |
| LOCK-03 | Active/Archived with archive/restore; no hard delete |
| LOCK-04 | No approval/DOA |
| LOCK-05 | Five future modules remain hook/mock only; no hard dependency |
| LOCK-06 | Historical consumers must use snapshot; master edits do not rewrite history |
| LOCK-07 | Exactly one route `#/sales-territory`; tabs/drawers/modal are surfaces, not invented routes |
| LOCK-08 | Map responds only to valid target/coordinates inside visible frame |
| LOCK-09 | Structure list uses document/outer-page scrolling as approved |
| LOCK-10 | `R-BK-01` is visible prototype fixture; production seed awaits OQ-14 |

**Convention deviation:** lifecycle value `active` is preserved verbatim from the approved HTML/BRD even though the general convention prefers past-tense state keys; `archived` already conforms. Renaming `active` in FRD would violate HTML fidelity and Scope Lock.

## §0.12 Coverage Manifest

### Stories 9/9

| BRD Ref | Requirement | Pack anchors |
|---|---|---|
| US-01 | Create Route | `01_UI` S-04 · API-03 · FN-04 · AC-03/04 |
| US-02 | View detail | `01_UI` S-06 · API-02 · FN-02 · AC-02 |
| US-03 | Edit Route | `01_UI` S-05 · API-04 · FN-05 · AC-05/06 |
| US-04 | Archive | `01_UI` S-07 · API-05 · FN-06 · AC-07 |
| US-05 | Restore | `01_UI` S-01 action · API-06 · FN-07 · AC-08 |
| US-06 | Search/filter/reset | `01_UI` S-01 · API-01 · FN-01 · AC-01/09 |
| US-07 | Workload | `01_UI` S-02 mock/read-only · AC-10 |
| US-08 | Map | `01_UI` S-03 · AC-11/12 |
| US-09 | Safe future hooks | `01_UI` S-06 · `02_API` §2.5 · XT-01–05 |

### Rules 20/20

| BRD Ref | Requirement | Pack anchors |
|---|---|---|
| BR-01 | Route primary unit | `04_DB` Route · BR-ST-01 · AC-01/03 |
| BR-02 | one salesperson per Route | `04_DB` · BR-ST-02 · AC-13 |
| BR-03 | salesperson soft ref only | `02_API` §2.5 · BR-ST-03 · XT-01 |
| BR-04 | code format/unique | API-03 · FN-03/04 · BR-ST-04 · AC-04 |
| BR-05 | code immutable | API-04 · FN-03/05 · BR-ST-05 · AC-06 |
| BR-06 | optional province / blank KPI | `01_UI` S-04 · BR-ST-06 · AC-04 |
| BR-07 | 77 provinces offline | `01_UI` S-03 · BR-ST-07 · AC-11 |
| BR-08 | approved region values | `04_DB` · BR-ST-08 · AC-04 |
| BR-09 | archive/restore, no hard delete | API-05/06 · BR-ST-09 · AC-07/08 |
| BR-10 | append-only audit | FN-08 · audit table · BR-ST-10 · AC-03/05/07/08 |
| BR-11 | future-derived read-only | `02_API` §2.5 · BR-ST-11 · AC-10 |
| BR-12 | historical snapshot immutable | `03_LOGIC` §3.5 · BR-ST-12 · XT-05 |
| BR-13 | archived excluded from new future records | `02_API` §2.5 · BR-ST-13 · XT-02–05 |
| BR-14 | no DOA/approval | state/API absence · BR-ST-14 · AC-14 |
| BR-15 | overlap baseline default | BR-ST-15 · OQ-09 · AC-15 |
| BR-16 | prototype coverage threshold | BR-ST-16 · OQ-04 · AC-10 |
| BR-17 | prototype workload formula | BR-ST-17 · OQ-06 · AC-10 |
| BR-18 | Route Types unresolved | BR-ST-18 · OQ-07 · AC-04 |
| BR-19 | map boundary | `01_UI` S-03 · BR-ST-19 · AC-12 |
| BR-20 | offline/core resilience | `01_UI` states · BR-ST-20 · AC-10/11 |

### Confirmed edges 9/9

| BRD edge | Pack anchors |
|---|---|
| duplicate/invalid code or missing required | BR-ST-04/05 · EC-01 · AC-04 |
| province blank | BR-ST-06 · EC-02 · AC-04 |
| salesperson source unavailable | EC-03 · XT-01 |
| future salesperson inactive/deleted | EC-04 · OQ-03 · XT-01 |
| linked-customer warning when data exists | EC-05 · XT-02 |
| universe/coverage blank when unavailable | EC-06 · AC-10 |
| archive/restore with audit | EC-07 · AC-07/08 |
| pointer outside map frame | EC-08 · AC-12 |
| downstream snapshot immutable | EC-09 · XT-05 |

EC-10 is an additional fixed resilience consolidation from BR-ST-20, not a substitute for a BRD edge.

Summary: Stories 9/9 · Rules 20/20 · confirmed edges 9/9 · missing anchors 0.
