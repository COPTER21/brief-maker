# FRD Pack Index — F-WH-STKTRF

| File | Audience | Content |
|---|---|---|
| 00_OVERVIEW.md | all | scope, actors, dependencies, classification, coverage |
| 01_UI.md | FE/QA | routes, surfaces, states, overlays, accessibility |
| 02_API.md | BE/integration | HTTP and cross-module contracts |
| 03_LOGIC.md | BE | functions, invariants, concurrency |
| 04_DB.md | BE/DBA/security | entities, constraints, classification |
| 05_RULES.md | BE/QA/BA | business rules, validation, edges, errors |
| 06_TESTS.md | QA | acceptance, negative, permission, integration tests |
| 07_LOCKED_DECISIONS.md | all | immutable decisions and OQs |

## Trace quick map

UI → API → logic is documented in 01_UI §1.6, 02_API §2.1 and 03_LOGIC §3.3. API-01..15 map one-to-one to FN-01..15; external engines are called only from logic functions. Database writes map to the seven entity groups in 04_DB.

## Phase 3.5 verification

- A Pack completeness: PASS — FULL, 8 numbered files + INDEX.
- B/C API and R8 logic trace: PASS — every mutation has a function; no orphan function.
- D API↔DB: PASS.
- E UI↔API: PASS.
- F/G engine purity and placement: PASS — no new engine; HTTP layer is thin.
- H Security: PASS — P2 and SoD enforced.
- I Conventions: PASS — snake_case fields, camelCase functions, uppercase error codes.
- J Classification: PASS — all entity groups classified; no Public default; no Restricted field.
- K Coverage manifest: PASS — S-01..10, BR-01..33, V-01..21 and E-01..21 mapped.
- L Scope lock/value stream: PASS — LK-1..11 imported; contracts and tests included.
- M HTML alignment: PASS — 4 routes/10 surfaces match; visible negative/mutation copy anchored to HTML/BRD.

**Verdict: APPROVED.**

