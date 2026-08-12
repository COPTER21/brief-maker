# 00_OVERVIEW — F-BOM-001 สูตรการผลิต (Bill of Materials)

> **FRD version:** 6.1 · **Pack variant:** STANDARD (7 files)  
> **Status:** AI-DRAFT — generated from BRD + as-built HTML; open decisions remain in §0.10  
> **Source order:** Scope Lock > BRD business intent > observed HTML behavior  
> **HTML sync:** `html-generator-v8` fallback (highest installed version); source HTML is `outputs/05_BOM/01_HTML/f-bom.html`

---

## §0.1 Purpose

กำหนด contract สำหรับทะเบียนสูตรการผลิตแบบ single-level: หลาย version ต่อสินค้าผลผลิต, สูตรหลักหนึ่งสูตรต่อ FG, ส่วนประกอบพร้อม UoM/scrap, cost rollup, status lifecycle, bulk action และ audit trail เพื่อให้ Backend, Frontend, DBA และ QA สร้างระบบจริงตรงกับ prototype โดยไม่เพิ่ม approval, routing, import/export หรือ multi-level BOM.

## §0.2 Pack Map

| File | Layer | ผู้ใช้หลัก |
|---|---|---|
| `00_OVERVIEW.md` | scope, route, trace, coverage | ทุกทีม |
| `01_UI.md` | page/action/state contract | FE, QA |
| `02_API.md` | HTTP contract | BE, FE, QA |
| `03_LOGIC.md` | functions/engine/transactions | BE, Architect |
| `04_DB.md` | schema/index/classification | DBA, BE, Security |
| `05_RULES.md` | rules/state/errors/security | BE, QA |
| `06_TESTS.md` | acceptance/regression/XT | QA, Dev |

## §0.3 Inputs and Authority

| Priority | Artifact | Use |
|---:|---|---|
| 1 | Scope Lock in `BRD_F-BOM-001.md` §3.4 | boundary and prohibitions |
| 2 | `outputs/05_BOM/03_BRD/BRD_F-BOM-001.md` | business intent, rules, downstream map |
| 3 | `outputs/05_BOM/01_HTML/f-bom.html` | routes, visible behavior, microcopy |
| 4 | `outputs/05_BOM/01_HTML/_PREBRIEF.md` | original feature constraints |
| 5 | `Related context/Item Master/FRD/02_API.md`, F-UOM context | upstream field contracts |

Quality evidence: `outputs/05_BOM/02_QC/_UX_CHECK_REPORT.md`, `outputs/05_BOM/02_QC/_COVERAGE_REPORT.md`, and `outputs/05_BOM/02_QC/e2e_bom.py`. The earlier coverage report is stale for FN-09; actual HTML contains clickable sibling-version navigation.

## §0.4 Pack Variant Decision

STANDARD is selected because the feature has 4 route states, 3 lifecycle statuses, no approval flow, and one deterministic calculation engine. The seven API surfaces are cohesive around one master-data aggregate and do not add a second workflow domain.

## §0.5 Actors and Permission Summary

| Actor | Read | Create/Edit | Status/Default | Bulk delete | View cost |
|---|:---:|:---:|:---:|:---:|:---:|
| Planner | ✓ | ✓ | ✓ | ✓ | by D-CLASS permission |
| Production | active BOM only | — | — | — | — |
| Costing | ✓ | — | — | — | ✓ |
| Auditor | ✓ | — | — | — | masked unless separately granted |

Authorization is re-evaluated on every API request. UI visibility is not an authorization boundary.

## §0.6 Route and Page Inventory

| Page | Route | Pattern observed | Purpose |
|---|---|---|---|
| P-01 | `#/bom` | Pattern A list + stats/filter/table/bulk | browse, filter, sort, select, bulk action |
| P-02 | `#/bom/create` | Pattern B form + 2-step wizard + line editor | create draft or active BOM |
| P-03 | `#/bom/edit/:id` | Pattern B form + 2-step wizard + line editor | amend existing BOM |
| P-04 | `#/bom/view/:id` | Pattern C detail + tabs | overview, components, history, sibling versions |

Supporting overlay: Pattern D confirmation modal for bulk delete. Dropdowns render through the observed overlay portal behavior. Layout/component rules follow the synced `html-generator-v8`; this FRD does not duplicate CI token values or hardcode rule counts.

## §0.7 System Context

```text
Item Master ─┐
             ├─> F-BOM-001 ─> Production / MO (active BOM + immutable snapshot)
UoM Master ──┘          └───> Costing (Confidential rollup)
Policy D-CLASS ──────────────> cost masking/access audit
Audit service <────────────── every BOM mutation
```

No inventory posting, GL posting, approval, notification, print/PDF, or document running-number contract is introduced.

## §0.8 Data Classification Summary

Highest classification is **Confidential** because `standard_cost`, `line_cost`, and `total_cost` expose product cost. BOM structure and master identifiers are Internal; actor identifiers and audit diffs are Confidential. Full field-level classification and enforcement are in `04_DB.md` §4.6 and `05_RULES.md` §5.7.

## §0.9 Requirements Trace Summary

| BRD story | UI | API | Logic | Rules | Tests |
|---|---|---|---|---|---|
| S-01 create | P-01/P-02 | API-02 | FN-03/FN-05/ENG-01 | BR-01..07 | AC-01, AC-02 |
| S-02 default | P-02/P-03 | API-02/API-04 | FN-08 | BR-02 | AC-03 |
| S-03 sibling versions | P-04 | API-03 | FN-02 | BR-01 | AC-04 |
| S-04 amend used BOM | P-03 | API-04 | FN-04 | BR-12 | AC-05 |
| S-05 validation | P-02/P-03 | API-02/API-04 | FN-05 | VR-01..08 | AC-06 |
| S-06 component/UoM reset | P-02/P-03 | upstream lookup | FN-05 | BR-06 | AC-07 |
| S-07 lifecycle | P-01/P-04 | API-05 | FN-06/FN-08 | BR-08/10 | AC-08 |
| S-08 guarded bulk delete | P-01 | API-06 | FN-07 | BR-11 | AC-09 |

## §0.10 Open Decisions and Provisional Defaults

| ID | Decision | Current implementation contract |
|---|---|---|
| OQ-BOM-01 | edit/delete when `used>0`; immutable MO snapshot | `[AI-DEFAULT]` allow edit, block delete, MO keeps immutable snapshot |
| OQ-BOM-03 | Item field mapping | use discovered `cover_url`, `name_th`, `standard_cost`, `base_uom`; validate active/type server-side |
| OQ-BOM-04 | zero/null cost, scrap 100%, deactivated master | `[AI-DEFAULT]` zero/null cost allowed and displayed as zero; 100% allowed; existing BOM remains readable |
| OQ-BOM-06 | `eff_from` scope | preserve optional field because it is visible in HTML; no status automation |
| OQ-BOM-07 | formal `scope_lock_ref` | ไม่พบข้อมูลในบทสนทนา |
| OQ-BOM-08 | performance load profile | `[AI-DEFAULT]` targets in `06_TESTS.md` §6.6 |
| DRIFT-02 | draft + default in HTML save path/seed | backend invariant wins: any non-active save clears `is_default` |

## §0.11 Scope Lock (R11)

**Locked in**

- single-level BOM only; parent is active FG; component is active RM/PM/TR
- multiple case-insensitive versions per FG, exactly zero or one active default
- statuses `draft`, `active`, `inactive`; transitions allowed in every direction without approval
- structured line editor, Item/UoM validation, decimal cost rollup
- list/detail/create/edit, sibling-version navigation, bulk status and guarded bulk delete
- Item Master, UoM Master, D-CLASS, audit, MO snapshot and Costing contracts

**Locked out**

- multi-level explosion, routing/work center/machine, by-product/co-product
- approval/DOA, notification hooks, CSV import/export, print/PDF
- inventory/GL posting, automatic effective-date status transition
- editable standard cost or BOM-side master maintenance

**Forbidden implementation shortcuts**

- do not trust UI validation, `used`, role, cost visibility, or default state from request payload
- do not use binary floating point for quantity/scrap/cost
- do not physically delete an audit log or a BOM referenced by MO
- do not hardcode Item/UoM display names as referential keys

## §0.12 Coverage Manifest (R13)

| Source requirement | FRD evidence | Test evidence | Status |
|---|---|---|:---:|
| S-01..S-08 | `01_UI.md`, `02_API.md`, `03_LOGIC.md` | AC-01..AC-09 | ✓ |
| BR-01..BR-15 | `05_RULES.md` §5.1 | TC-BR-01..15 | ✓ |
| VR-01..VR-08 | `05_RULES.md` §5.4 | TC-VR-01..08 | ✓ |
| EC-01..EC-10 | `05_RULES.md` §5.5 | TC-EC-01..10 | ✓ |
| MO downstream | `02_API.md` §2.X, `03_LOGIC.md` FN-09 | XT-01..XT-03 | ✓ |
| Costing downstream | `02_API.md` §2.X, ENG-01 | XT-04..XT-05 | ✓ |
| Confidential cost | `04_DB.md` §4.6, `05_RULES.md` §5.7 | TC-SEC-01..04 | ✓ |
| Scope Lock | §0.11 + every layer out-of-scope note | TC-SCOPE-01..04 | ✓ |
| `[AI-DEFAULT]` decisions | §0.10 + `05_RULES.md` §5.9 | TC-AID-01..06 | ✓ |

## §0.13 Definition of Ready for Development

- All seven files exist and identifiers cross-reference without orphan API/function/engine.
- Open decisions in §0.10 are accepted as provisional defaults or closed by owner.
- Round-2 coverage report has no missing BRD story/rule/confirmed edge.
- Any future HTML change must rerun `outputs/05_BOM/02_QC/e2e_bom.py` and update the drift ledger.
