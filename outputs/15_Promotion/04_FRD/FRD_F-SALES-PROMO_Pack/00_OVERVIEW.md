# 00_OVERVIEW — F-SALES-PROMO Promotion

## §0.1 Document Control

| Field | Value |
|---|---|
| Feature | F-SALES-PROMO · Promotion |
| Module | Sales |
| FRD version | 1.0 · 2026-08-18 |
| Status | READY FOR DEVELOPMENT |
| Inputs | BRD_F-SALES-PROMO_Promotion.md + Promotion.html |
| Pack variant | FULL |
| Variant evidence | 5 UI surfaces, 8+ states, sequential approval, monetary engine |
| HTML gate | PM/BA approved; UX/Coverage/E2E gate passed |

## §0.2 Purpose

เก็บและควบคุมข้อเสนอชั่วคราวสำหรับลูกค้ากลุ่มกว้าง จากการสร้าง/อนุมัติไปจนถึงการประเมินใน Quotation/Sales Order และการนับ usage จาก Invoice โดยใช้ Item/Master/DOA/GL contracts กลาง

## §0.3 Scope

### In

- CRUD แบบไม่ hard-deleteสำหรับ draft, 4 rule types, 3 scope types, coupon/priority/exclusive/TA/budget/quota
- overlap acknowledgement, DOA sequential no-amount approval, lifecycle actions, simulator, audit, export
- reusable calculation candidate `promo-engine`
- downstream contracts for QT/SO, Invoice, GL and Inventory

### Out

- customer-specific promotion, loyalty, mixed promotion type, multiline discount, ATP decision, Campaign integration
- feature-local DOA configuration, Document Configuration declaration, Notification declaration

## §0.4 Actors

| Actor | Permissions |
|---|---|
| `sales_marketing_officer` | view/create/edit draft/submit/copy/cancel/simulate/export |
| `role-mgr-sales` | above + current-step approve/reject + pause/resume/end |
| `role-mgr-bu` | current-step approve/reject |
| `system` | eligibility, calculation, scheduled state, usage, audit |

## §0.5 Architecture Boundary

```text
Promotion UI → Promotion API → scope-local functions → promo-engine
                                      ↓
       Promotion DB + DOA adapter + master adapters + audit

Price Resolver → TA engine → promo-engine → QT/SO snapshot
Invoice usage event → Promotion usage + GL reference
Free goods output → SO/Inventory ATP and stock movement
```

## §0.6 Dependencies

| Dependency | Direction | Contract |
|---|---|---|
| Sales Price List | in | price-resolver result |
| Trade Agreement | in | price after TA + `promo_allowed` |
| Customer/Group/Channel | in | scope match; default/doc channel |
| Item Master | in | product/category/uom/factor/list price |
| GL Posting Group | in | valid posting account ref |
| DOA + Employee | in/out | resolve slots, candidates, snapshot, My Approval |
| Quotation/Sales Order | out | evaluate and freeze applied result |
| Invoice | in/out | idempotent usage + GL trace |
| Inventory | out | free item/qty; ATP remains downstream |

## §0.7 Security & Data Classification

### §0.7.1 Highest classification

**Confidential** — customer reference, employee/assignee identity, budget/discount usage, approval history. ไม่มี Restricted fields ใน feature นี้; customer/employee details beyond display snapshot remain owned by master features.

| Domain | Enforcement |
|---|---|
| AuthN/AuthZ | IAM token + permission middleware every API |
| SoD | submitter cannot be approver/candidate |
| Tenant isolation | `X-Tenant-Id` mandatory and part of every unique/index key |
| Audit | append-only mutation/state/calculation reference |
| Concurrency | ETag/`If-Match`; 409 on stale update |
| Idempotency | mutation and usage event keys |

## §0.8 Lifecycle Summary

`draft → pending_approval → scheduled → active ⇄ paused → ended`, with `rejected→draft`, `budget_exhausted`, `cancelled`, `ended_early` branches. Full matrix: `05_RULES.md` §5.3.

## §0.9 Technical Assumptions `[AI-DEFAULT]`

- Optimistic concurrency using integer `version`
- Idempotency-Key required for every POST mutation
- Money stored as decimal(19,4), rounded to currency scale only at public result boundaries
- Pagination cursor/limit; default limit 20, max 100
- In-flight DOA chain is immutable after submit

## §0.10 Manual Follow-ups

- Create actual central entry using `DOA_BRIEF_F-SALES-PROMO.md`
- Architect assigns global engine id for `promo-engine`; use `F-SALES-PROMO-ENG-01` until registered
- Campaign integration remains excluded

## §0.11 Scope Locks

| Lock | Requirement |
|---|---|
| LOCK-PROMO-01 | AS-BUILT UI = approved Promotion.html |
| LOCK-PROMO-02 | no customer-specific promotion |
| LOCK-PROMO-03 | Item Master source of truth; other references soft/snapshot |
| LOCK-PROMO-04 | DOA no amount, sequential, config-driven, SoD |
| LOCK-PROMO-05 | ATP/free-goods shortage decision belongs to SO |
| LOCK-PROMO-06 | usage originates from Invoice and counts promotion occurrences |
| LOCK-PROMO-07 | Campaign future only |

## §0.12 Coverage Manifest

### Stories

| BRD | Requirement | Pack location |
|---|---|---|
| US-01 | create draft | 01_UI P-03 · API-02 · FN-02 · AT-01 |
| US-02 | author one of four rules | 01_UI P-03 · API-02/03 · FN-01 · AT-02..05 |
| US-03 | submit to DOA | 01_UI P-05 · API-04 · FN-04 · AT-06 |
| US-04 | approve/reject | 01_UI P-02/P-05 · API-05/06 · FN-05 · AT-07/08 |
| US-05 | simulate cart | 01_UI P-04 · API-13 · ENG-01 · AT-09..14 |
| US-06 | pause/resume/end | 01_UI P-02/P-05 · API-08..10 · FN-07 · AT-15 |
| US-07 | usage/budget/account | 01_UI P-02 · API-14 · FN-08 · AT-16/XT-03 |

### Business Rules

| BRD | Pack location |
|---|---|
| BR-01 | 05 BR-PROMO-01 · ENG-01 · AT-09 |
| BR-02 | 05 BR-PROMO-02 · ENG-01 · AT-10 |
| BR-03 | 05 BR-PROMO-03 · ENG-01 · AT-09/14 |
| BR-04 | 05 BR-PROMO-04 · ENG-01 · AT-11/XT-04 |
| BR-05 | 05 BR-PROMO-05 · ENG-01 · AT-12/13 |
| BR-06 | 05 BR-PROMO-06 · ENG-01 · AT-14 |
| BR-07 | 05 BR-PROMO-07 · FN-03/04 · AT-06 |
| BR-08 | 05 BR-PROMO-08 · AT-06 |
| BR-09 | 05 BR-PROMO-09 · ENG-01 · AT-16 |
| BR-10 | 05 BR-PROMO-10 · FN-08 · AT-16 |
| BR-11 | 05 BR-PROMO-11 · FN-02/06 · AT-17 |
| BR-12 | 05 BR-PROMO-12 · FN-07 · AT-15 |
| BR-13 | 05 BR-PROMO-13 · ENG-01 · XT-04 |
| BR-14 | 05 BR-PROMO-14 · ENG-01 · XT-03 |
| BR-15 | 05 BR-PROMO-15 · FN-01 · AT-05/10 |
| BR-16 | 05 BR-PROMO-16 · AT-18 |
| BR-17 | 05 BR-PROMO-17 · FN-09 · AT-19 |
| BR-DOA-01..07 | 05 §5.5 · FN-04/05 · AT-06..08/20 |

### Confirmed and AI-default edges

| Edge | Pack location |
|---|---|
| EC-01..04 | 05 §5.6 · AT-02..08 |
| EC-05..09 | 05 §5.6 · AT-10..16 · XT-04 |
| EC-10..12 | 05 §5.6 · AT-17/19 · XT-01..03 |
| EC-AI-01 | 05 `[AI-DEFAULT]` · AT-21 |
| EC-AI-02 | 05 `[AI-DEFAULT]` · AT-22 |
| EC-AI-03 | 05 `[AI-DEFAULT]` · AT-20 |
| EC-AI-04 | 05 `[AI-DEFAULT]` · AT-23 |
| EC-AI-05 | 05 `[AI-DEFAULT]` · AT-24 |

## §0.13 FRD Verification Summary

- FULL files: 9/9 + INDEX ✅
- Mutation API → Function/Engine trace: 14/14 ✅
- DB links and data classification: complete ✅
- Scope lock/value-stream contracts: complete ✅
- HTML surfaces/routes: 5/5 on `#/promotions` ✅
- Verdict: PASS
