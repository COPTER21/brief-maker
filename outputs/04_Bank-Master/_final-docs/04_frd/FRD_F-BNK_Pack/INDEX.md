# INDEX — FRD F-BNK Bank Master (บัญชีธนาคาร)

> **Variant:** FULL (9 files + INDEX) · **Audience:** All roles (entry point)
> **Purpose:** Cross-reference + Function Trace + Quick Nav
> **Source of Truth:** HTML `01_HTML/f-bank.html` (gate-passed: UX 🟢 · Coverage PASS · E2E R1 21/21 + R2 15/15, 0 console errors) · BRD APPROVED · Conflict Priority: LOCK (Strike 2026-08-11) > BRD > HTML

---

## 📂 Pack Contents

| # | File | Audience | Content |
|---|---|---|---|
| 00 | OVERVIEW.md | All | Meta + Scope + Roles + Dependencies + OQ + **Coverage Manifest §0.12** |
| 01 | UI.md | FE dev | **Layout Decision Log §1.0** + Pages P-01..06 + Journey |
| 02 | API.md | BE (HTTP) | 11 APIs + **GL Cross-Module Contract §2.6 (3 drifts)** + §2.7 (Receipt/PV/GL serve) |
| 03 | LOGIC.md | BE (logic) | 14 Functions (FN-01..14 incl. FN-13b) + **no engine (§3.2 empty)** + Trace §3.3 |
| 04 | DB.md | DBA / BE | 1 Table (T_bank_account, 25 cols) + Data Classification (Confidential: account_no/promptpay) |
| 05 | RULES.md | BE + QA | BR-01..10 + validations + Edge Cases + Errors + Security |
| 06 | TESTS.md | QA | AT-01..21 + DoD + Cross-Module (XT) + Microcopy verbatim |
| 07 | LOCKED_DECISIONS.md | All | **Scope Lock §7.0 (OQ-BNK-01..04 + GL Contract)** + LD-B-01..07 |
| — | INDEX.md | All | This file |

---

## 🔍 Quick Nav by Question

- **FE dev เริ่มที่ไหน?** → 01_UI §1.0 (Layout Decision Log) → §1.2 (page actions + API)
- **BE dev สร้าง endpoint?** → 02_API §2.2 → 03_LOGIC §3.3 (Functions) → 04_DB → 05_RULES
- **GL integration?** → 02_API §2.6 (consume F-PG-API-01 `?kind=bank&status=active` + 3 drifts) + 03_LOGIC FN-14
- **DBA?** → 04_DB (T_bank_account + 2 partial-unique ★ index + account_no dash-strip unique + RLS)
- **QA?** → 06_TESTS §6.1 (AT) + 05_RULES §5.5 (Edges) + §6.10 (microcopy verbatim)
- **PM — OQ/risk?** → 00_OVERVIEW §0.8 (OQ-BNK-01..04 CLOSED + 06/07/08/CC-01 open; blocking: OQ-BNK-06, OQ-BNK-07)
- **Security — masking?** → 04_DB §4.6 (Confidential account_no/promptpay) + 05_RULES §5.7 D11 (OQ-BNK-08)

---

## 🔗 Cross-Reference Tables

### Page → API (from 01_UI §1.2)
| Page | Actions | Calls |
|---|---|---|
| P-01 List | row click / filter / stat / bulk-status / export / import | API-03 / API-01 / API-01 / API-06 / API-10 / (P-05) |
| P-02 Create | save · GL picker | API-02 · F-PG-API-01 |
| P-03 Edit | save (IR-BNK-01) · GL picker | API-04 · F-PG-API-01 |
| P-04 View | change status | API-05 |
| P-05 Import | preview / commit | API-08 / API-09 |
| P-06 Bulk delete | confirm | API-07 |
| (downstream Receipt/PV) | picker | API-11 |

### API → Logic (from 03_LOGIC §3.3)
| API | Functions | Engines |
|---|---|---|
| API-01 GET /bank-accounts | FN-04, FN-10 | — |
| API-02 POST /bank-accounts | FN-01, FN-03, FN-08, FN-09 | — |
| API-03 GET /:id | FN-10 | — |
| API-04 PUT /:id | FN-02, FN-03, FN-08 | — |
| API-05 POST /:id/status | FN-05 | — |
| API-06 POST /bulk-status | FN-06 | — |
| API-07 POST /bulk-delete | FN-07 | — |
| API-08 POST /import/preview | FN-11 | — |
| API-09 POST /import/commit | FN-12 | — |
| API-10 GET /export | FN-13 | — |
| API-11 GET /active | FN-13b | — |
| (form picker GL) | FN-14 | — |

### API → DB (from 02_API side effects)
| API | Reads | Writes |
|---|---|---|
| API-01/03/11 | T_bank_account | — (read; +read-access-log Confidential) |
| API-02 | (dup check) | T_bank_account, T_audit_log |
| API-04 | T_bank_account (used check → IR lock) | T_bank_account (guard bank/account_no), T_audit_log |
| API-05/06 | T_bank_account | status (+ ★ drop non-active), T_audit_log |
| API-07 | T_bank_account (used check) | DELETE (used=0), T_audit_log |
| API-08 | T_bank_account (dedup) | — (preview only) |
| API-09 | (dup check) | INSERT (merge-only), T_audit_log |

### External Contract (consume / serve)
| Direction | Endpoint | Owner | Note |
|---|---|---|---|
| **Consume** | `GET /gl/posting-groups?kind=bank&status=active` (F-PG-API-01) | F-PG | generic API-01, no dedicated endpoint · 3 drifts (§2.6) |
| **Serve** | `GET /bank-accounts/active?side=` (API-11) | F-BNK | Receipt/PV picker (ยังไม่ทำ) |
| **Serve (read)** | resolve posting_group → account_1 | external GL engine | at post time (§2.7) |

---

## 🚨 R8 Verification Matrix

**Rule:** ทุก mutation API มี ≥ 1 Function/Engine
| API (mutation) | Functions | Engines | ✅/❌ |
|---|---|---|---|
| POST /bank-accounts | 4 (FN-01/03/08/09) | 0 | ✅ |
| PUT /:id | 3 (FN-02/03/08) | 0 | ✅ |
| POST /:id/status | 1 (FN-05) | 0 | ✅ |
| POST /bulk-status | 1 (FN-06) | 0 | ✅ |
| POST /bulk-delete | 1 (FN-07) | 0 | ✅ |
| POST /import/commit | 1 (FN-12) | 0 | ✅ |

**Rule:** No orphan Function/Engine
| Function | Traced in §3.3? |
|---|---|
| FN-01 createBankAccount | ✅ (API-02) |
| FN-02 updateBankAccount (IR guard) | ✅ (API-04) |
| FN-03 validateBankAccount | ✅ (API-02, 04, +11 import) |
| FN-04 buildBankListQuery | ✅ (API-01) |
| FN-05 setBankStatus (★ drop) | ✅ (API-05) |
| FN-06 bulkSetBankStatus | ✅ (API-06) |
| FN-07 bulkDeleteBankAccounts | ✅ (API-07) |
| FN-08 enforceDefaultPerSide | ✅ (API-02, 04) |
| FN-09 generateBankCode | ✅ (API-02) |
| FN-10 maskAccountNo/normalize | ✅ (API-01, 03; FN-03) |
| FN-11 previewImportRows | ✅ (API-08) |
| FN-12 commitImportRows | ✅ (API-09) |
| FN-13 exportBankRegistry | ✅ (API-10) |
| FN-13b getActiveAccountsForPicker | ✅ (API-11) |
| FN-14 buildBankPostingGroupOptions | ✅ (form picker + save) |
| Engines | ไม่มี (LD-B-06 — registry-only) |

**Result:** R8 PASS — no orphan, ทุก mutation traced ✅ · engines = 0 (feature ไม่มี engine ของตัวเอง)

---

## 📊 Pack Statistics

| Metric | Count |
|---|---|
| Pages | 6 (P-01..06) |
| APIs (owned) | 11 (+ 1 consumed external F-PG-API-01) |
| Functions | 14 (FN-01..14 incl. FN-13b) |
| Engines | 0 (external GL engine only — §2.7/§3.4) |
| DB Tables | 1 (T_bank_account, 25 cols) |
| Business Rules | 10 (BR-01..10) |
| Field Validations | 8 form + 9 import (incl. IN_FILE_DUPLICATE) |
| Edge Cases | 11 (EC-01..11) |
| Error codes | 19 |
| Locked Decisions | 7 (LD-B-01..07) + 7 Scope Locks |
| Banks (config seed) | 9 · Account types 3 |
| Open Questions | 6 open (2 blocking: OQ-BNK-06, OQ-BNK-07) + OQ-BNK-01..04 CLOSED |

---

## Coverage Manifest Pointer ⭐
- **00_OVERVIEW §0.12** — Stories 8/8 · Rules 10/10 · Edges (13 confirmed + 10 probe) — ไม่มี requirement หล่น (unresolved → OQ, ไม่หายเงียบ)
- **Scope Lock:** 07_LOCKED §7.0 (7 locks — OQ-BNK-01..04 + GL Contract + VD-PDM + Governance, drift=none)
- **GL contract verified 3 จุด (DEV ห้ามลอก mock):** D-1 `?kind=bank` (NOT `?type=`) · D-2 active-only คืน KBANK เท่านั้น · D-3 generic F-PG-API-01 (no dedicated endpoint) — 02_API §2.6

---

## 🎯 Reading Order
1. 00_OVERVIEW (scope + coverage) → 2. 01_UI §1.3 Journey → 3. drill per role (FE:01 / BE:02+03 / DBA:04 / QA:05+06) → 4. 07_LOCKED (constraints, GL contract).
