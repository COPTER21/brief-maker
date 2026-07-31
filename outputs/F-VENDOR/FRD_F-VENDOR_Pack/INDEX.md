# INDEX — FRD F-VENDOR ทะเบียนคู่ค้า

> **Variant:** FULL  
> **Status:** IN-REVIEW · v1.1 HTML↔FRD sync · 2026-07-31  
> **Entry point:** เอกสารสำหรับส่งต่อ AI Coding Agent โดยไม่มี codebase ปัจจุบัน

---

## Pack Contents

| File | Read when you need |
|---|---|
| `00_OVERVIEW.md` | scope, source precedence, roles, dependencies, open questions, BRD coverage |
| `01_UI.md` | route, drawer/modal surfaces, action visibility, journeys |
| `02_API.md` | endpoint contracts, headers, payloads, cross-module contracts |
| `03_LOGIC.md` | functions, CUBIC candidates, API↔logic trace |
| `04_DB.md` | tables, fields, classification, constraints, retention |
| `05_RULES.md` | business/state/permission/validation/error rules |
| `06_TESTS.md` | acceptance criteria, test inventory, DoD, cross-module tests |
| `07_LOCKED_DECISIONS.md` | user confirmations, final decisions, historical drift |

## Source Baseline

| Source | Authority |
|---|---|
| User confirmations 2026-07-31 | approval and scope |
| `outputs/F-VENDOR/vendor.html` | UI source of truth |
| `CUBE_4.0_AI_CONTEXT_PACK.md` + `Central Plan/` | global rules/dependencies |
| `BRD_vendor_master.md` v1.1 | approved business intent |
| other Vendor context files | historical/reference only |

## Quick Start by Role

- FE: `01_UI.md` → `02_API.md` → approved HTML; then use future `UI_BRIEF_vendor.md`
- BE: `02_API.md` → `03_LOGIC.md` → `05_RULES.md` → `04_DB.md`
- DBA/Security: `04_DB.md` → `05_RULES.md §5.7` → `07_LOCKED_DECISIONS.md`
- QA: `06_TESTS.md` → `05_RULES.md` → approved HTML
- PM/BA: `00_OVERVIEW.md` → `07_LOCKED_DECISIONS.md`
- Architect: `03_LOGIC.md §3.2/§3.4` → `02_API.md §2.10`

## UI → API

| UI surface | Main actions | API |
|---|---|---|
| UI-01 Vendor list | list/filter/detail | API-01, API-03 |
| UI-02 Create/Edit | refs/create/update/submit KYC | API-02..API-06, API-17/18 |
| UI-03 View tabs | detail/eligibility/Price List | API-03, API-19, API-20 |
| UI-04 KYC | pass/fail/sanctions block | API-07 |
| UI-05 Approval | submit/approve/reject | API-08, API-09 |
| UI-06 Status actions | block/unblock/deactivate/blacklist | API-10..API-13 |
| Bank actions | submit/verify/deactivate | API-14..API-16 |

## API → Logic

| API range | Functions | Engines/External |
|---|---|---|
| API-01/03 | FN-01 | Policy field policy |
| API-02 | FN-02 | reference services |
| API-04 | FN-03/FN-05 | ENG-02 |
| API-05 | FN-04/FN-05 | ENG-02 |
| API-06 | FN-06/FN-05 | — |
| API-07 | FN-07 | sanctions evidence adapter |
| API-08 | FN-08 | Policy Center |
| API-09 | FN-09 | — |
| API-10..13 | FN-10/FN-15 | ENG-01 |
| API-14/15 | FN-11/FN-15 | ENG-01 after decision |
| API-16 | FN-12/FN-15 | ENG-01 |
| API-17/18 | FN-13/FN-14 | scanner/storage |
| API-19 | FN-15 | ENG-01 |
| API-20 | FN-16 | F-VENDOR-PRICE-LIST |

## API → DB

| API range | Main reads | Main writes |
|---|---|---|
| API-01..03 | vendor aggregate/ref stores | sensitive view audit when applicable |
| API-04/05 | all vendor aggregate tables | vendor/contacts/addresses/banks + audit |
| API-06 | vendor | vendor + audit |
| API-07 | vendor/attachments | KYC review + vendor + audit |
| API-08/09 | vendor/approval | approval steps + vendor + audit |
| API-10..13 | vendor | vendor + audit |
| API-14..16 | bank/vendor | bank + audit |
| API-17/18 | attachments | attachment metadata + audit |
| API-19 | vendor/banks | — |
| API-20 | vendor + downstream | — |

## R8 Verification

| Check | Result |
|---|---|
| Mutation APIs with function trace | 15/15 ✅ |
| Declared functions traced | 16/16 ✅ |
| Declared engines traced | 2/2 ✅ |
| Business thresholds hidden in API | none ✅ |
| UI calls engine directly | none ✅ |

## Cross-Module Map

```text
F-VENDOR
  ├─ E-002 → F-VENDOR-PRICE-LIST
  │           vendor_id + status
  ├─ E-007 → F-PO
  │           vendor_id + status + default_payment_term
  └─ Payment/PV
              active + KYC + verified-bank eligibility

Policy Center ──resolve chain──> F-VENDOR approval snapshot
Sanctions provider ──evidence──> F-VENDOR KYC review
```

## Pack Statistics

| Metric | Count |
|---|---:|
| UI surfaces | 7 |
| APIs | 20 |
| Scope-local functions | 16 |
| CUBIC engine candidates | 2 |
| DB tables | 8 |
| Business rules | 30 |
| BRD edge cases | 13 |
| Activated probe/default cases | 6 |
| Acceptance criteria | 20 |
| Test inventory | 28 |
| Cross-module tests | 6 |
| Locked decisions | 12 |
| Open questions | 6 |

## Coverage and Lock Pointers

- BRD Coverage Manifest: `00_OVERVIEW.md §0.12`
- Scope Lock: `07_LOCKED_DECISIONS.md §7.0`
- Historical drift resolution: `07_LOCKED_DECISIONS.md §7.2`
- Microcopy anchors: `06_TESTS.md §6.9`
- Cross-module contracts: `02_API.md §2.10`
- Cross-module tests: `06_TESTS.md §6.8`

## Implementation Handoff Order

1. Confirm OQ-01..OQ-04 and OQ-06 before production implementation
2. establish schema/RLS/classification and audit/outbox
3. implement pure engines and unit tests
4. implement functions/state transitions
5. implement APIs with idempotency/concurrency
6. build UI against approved HTML + future UI Brief
7. run AC/XT/security tests and drift checks
