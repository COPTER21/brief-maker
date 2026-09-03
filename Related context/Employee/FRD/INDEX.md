# INDEX — FRD F-EMP-001 Employee Master (FULL Pack)

> Cross-reference + Function Trace + Quick Navigation
> Generator: frd-generator-v5 (v5.1) · Variant: FULL (9 files + INDEX) · Status: APPROVED

---

## 📁 Pack Files
| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW.md | All | Document Control + Scope + Roles + Dependencies + Open Questions |
| 01_UI.md | FE | 6 Pages + Components + Layout IDs + Journey |
| 02_API.md | BE | 11 API contracts (HTTP layer) |
| 03_LOGIC.md | BE | 15 Functions + 5 Engines + Trace Table |
| 04_DB.md | DBA/BE | 6 tables + Field Dictionary + Classification (R10) |
| 05_RULES.md | BE/QA | Rules + Validation + Edge Cases + Errors + State Machine + D-CLASS |
| 06_TESTS.md | QA | 12 AC + Coverage Map + DoD |
| 07_LOCKED_DECISIONS.md | All | LD-01..10 + deviations + Pre-DOA |
| INDEX.md | All | this file |

## 🔗 Page → API
| Page | APIs |
|---|---|
| P-01 List | API-01, API-09 |
| P-02 Profile | API-02, API-11 |
| P-03 Create | API-03, API-10 |
| P-04 Edit | API-04, API-10 |
| P-05 Delete | API-05, API-11 |
| P-06 Import | API-08 |

## 🔗 API → Function/Engine (R8 summary)
ดู 03_LOGIC §3.3 — ทุก mutation API trace ครบ, ไม่มี orphan ✅

## 🔗 API → Table
| API | Tables |
|---|---|
| 01/02/09 | T_employee (+5 sub, read) |
| 03 | T_employee + 5 sub (INSERT) |
| 04 | T_employee + sub (UPDATE) |
| 05 | T_employee (soft-delete) |
| 06/07 | T_employee (lifecycle/status) |
| 08 | T_employee + sub (bulk) |
| 10 | M_address (read) |
| 11 | T_user (read) |

## 🧩 Engines (CUBIC candidates)
ENG-01 thai-national-id-validator · ENG-02 address-cascade-resolver · ENG-03 supervisor-cycle-detector · ENG-04 pii-masking-engine · ENG-05 employee-status-machine

## 🔐 Classification highest = **Restricted** (national_id/sso/tax/bank/grade/salary) · Preset P6

## ➡️ Downstream Chain
- 🎨 html-generator-v3 → ใช้ 01_UI.md (prototype employee-management.html มีแล้ว ✅)
- 📋 frd-qa-generator-v2 → ใช้ 02_API + 03_LOGIC + 05_RULES + 06_TESTS
- 🏷️ uba-taxonomy-register → assign Smart Code + global ENG IDs
