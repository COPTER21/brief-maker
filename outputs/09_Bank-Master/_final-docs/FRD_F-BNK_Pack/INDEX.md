# INDEX — FRD F-BNK Bank Master (ธนาคาร / บัญชีบริษัท)

> **Variant:** FULL · **Generator:** frd-generator-v6.1 (Lane Mode) · **Source of truth:** `01_HTML/BankMaster.html`

---

## 📂 Pack Contents
| # | File | Audience | Purpose |
|---|---|---|---|
| 00 | OVERVIEW.md | All | Meta + Scope + Roles + Scope-Lock ptr + **Coverage Manifest** + Probe Log |
| 01 | UI.md | FE dev | Layout Decision Log + Pages (routes) + Journey + **Section M** |
| 02 | API.md | BE dev (HTTP) | 16 API contracts + Cross-Module Contract |
| 03 | LOGIC.md | BE dev (logic) | 12 Functions + 2 Engines + R8 Trace |
| 04 | DB.md | DBA / BE | 3 tables + Classification (R10) |
| 05 | RULES.md | BE + QA | 12 BR + State Machine + 17 Edge Cases + Errors + D-CLASS |
| 06 | TESTS.md | QA | 18 AC + Cross-Module + **P0 permission/negative set** + verbatim microcopy |
| 07 | LOCKED_DECISIONS.md | All | **Scope Lock §7.0 (immutable)** + 5 LDs |

---

## 🔍 Quick Nav by Question
- **FE dev, where do I start?** → 01_UI §1.0 Layout Decision Log + §1.2 per-page (routes + actions → API IDs).
- **BE dev, new endpoint?** → 02_API §2.2 → 03_LOGIC §3.3 (which Functions/Engines) → 04_DB (tables) → 05_RULES (validation).
- **How is the account number protected?** → 05_RULES BR-BNK-09 + §5.7 D-CLASS → 04_DB §4.6 → 02_API-05 → 03_LOGIC FN-05 + ENG-BNK-01 → 06_TESTS TC-07/08/09/16 (P0).
- **W1 custom-bank delete rule?** → 05_RULES BR-BNK-08 → 03_LOGIC FN-10 → 02_API-13 → 06_TESTS AC-12/13.
- **Cross-module (PV/RV/Recon/Payroll)?** → 02_API §2.X + API-16 → 06_TESTS §6.9 XT-01..04.
- **PM, open risks?** → 00_OVERVIEW §0.8 OQ-BNK-01..06 · 07_LOCKED §7.5.

---

## 🔗 Cross-Reference Tables

### Page → API
| Page | Action | Calls |
|---|---|---|
| P-01 list | company switch / filter | API-01 |
| P-01 list | reveal | **API-05** |
| P-01 list | row → view | API-03 |
| P-01 list | create | API-02 |
| P-03 create/edit | save | API-02 / API-04 |
| P-04 view | deactivate/activate/archive | API-06/07/08 |
| P-04 view | set default | API-09 |
| P-02 banks | list / view | API-10 / API-15 |
| P-05 bank form | create/edit | API-11 / API-12 |
| P-02 banks | delete custom | **API-13** |
| M-03 (mock) → real | pickable | API-16 |

### API → Logic (from 03_LOGIC §3.3)
| API | Functions | Engines |
|---|---|---|
| API-02 POST /bank-accounts | FN-01, FN-03, FN-06, FN-12 | ENG-BNK-01 |
| API-04 PUT /bank-accounts/:id | FN-02, FN-03, FN-12 | ENG-BNK-01 |
| API-05 POST …/reveal | FN-05, FN-12 | **ENG-BNK-01** |
| API-06/07/08 lifecycle | FN-07, FN-06, FN-12 | — |
| API-09 set-default | FN-06, FN-12 | — |
| API-11 POST /banks | FN-08, FN-12 | **ENG-BNK-02** |
| API-12 PUT /banks/:id | FN-09, FN-12 | ENG-BNK-02 |
| API-13 DELETE /banks/:id | FN-10, FN-12 | — |
| API-16 pickable | FN-11 | ENG-BNK-01 |

### API → DB
| API | Reads | Writes |
|---|---|---|
| API-01/03/16 | T_company_bank_account | — |
| API-02 | T_bank, T_company, T_chart_of_account | T_company_bank_account, T_bank_audit_log, T_bank.used_count |
| API-04 | T_company_bank_account | T_company_bank_account, T_bank_audit_log |
| API-05 | T_company_bank_account (decrypt) | T_bank_audit_log (revealed) |
| API-06/07/08/09 | T_company_bank_account | T_company_bank_account, T_bank_audit_log |
| API-11/12 | T_bank | T_bank, T_bank_audit_log |
| API-13 | T_bank | T_bank (delete), T_bank_audit_log |

### Engine ↔ Feature
| Engine | Used by | Status |
|---|---|---|
| ENG-BNK-01 sensitive-field-masker | F-BNK (this) + PV/Payroll (planned) | DRAFT |
| ENG-BNK-02 swift-bic-validator | F-BNK (this) + any bank-entry feature | DRAFT |

---

## 🚨 R8 Verification Matrix
| API (mutation) | Functions | Engines | ✅ |
|---|---|---|---|
| POST /bank-accounts | 3 | 1 | ✅ |
| PUT /bank-accounts/:id | 2 | 1 | ✅ |
| POST …/reveal | 1 | 1 | ✅ |
| POST …/deactivate·activate·archive | 2 | 0 | ✅ |
| POST …/set-default | 1 | 0 | ✅ |
| POST /banks | 1 | 1 | ✅ |
| PUT /banks/:id | 1 | 1 | ✅ |
| DELETE /banks/:id | 1 | 0 | ✅ |

| Function/Engine | Traced? |
|---|---|
| FN-01..12 | ✅ all in §3.3 |
| ENG-BNK-01 | ✅ (API-05 direct + FN-01/02/04/11) |
| ENG-BNK-02 | ✅ (API-11/12) |

No orphans. No hidden logic in 02_API.

---

## 📊 Pack Statistics
| Metric | Count |
|---|---|
| Pages (surfaces) | 9 (1 route · 2 tabs · 4 drawers · 3 modals) |
| APIs | 16 |
| Functions | 12 |
| Engines | 2 (DRAFT) |
| DB Tables | 3 (+2 existing) |
| Business Rules | 12 |
| Edge Cases | 17 |
| Error codes | 20 |
| Locked Decisions | 6 (+7 Scope Locks) |
| Open Questions | 6 (5 [AI-DEFAULT] open · OQ-BNK-05 RESOLVED 2026-08-06 → LD-06) |

---

## Coverage Manifest Pointer ⭐
- `00_OVERVIEW §0.12` — every BRD Story/Rule/Edge → home in pack (9/9 · 12/12 · 15/15).
- Scope Lock: `07_LOCKED §7.0` (LOCK-01..07, immutable).
- Section M (HTML alignment): `01_UI §1.9`.
