# 00_OVERVIEW — F-PG GL Posting Group

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Open Questions
> **Mode:** HTML-first Mode A (Recognize & Validate) + Lane Mode (no-ask, one-shot)

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-PG (F-0.19, Finance Foundation) — legacy code F-GL-POSTING-001 |
| **Feature Name** | GL Posting Group — Specific Posting Groups + General Posting Setup |
| **Feature Code** | BRD-FIN-019 |
| **Module** | Finance / GL Foundation |
| **Variant** | **STANDARD** (7 files) — see §0.1.1 for reasoning |
| **Status** | DRAFT (this FRD generation) |
| **FRD Version** | 1.0 (2026-08-10) |
| **Generator** | frd-generator-v6 (skill v6.1, HTML-first), Sync Read → html-generator-v7 knowledge (v6 not installed in this project — v7 is the highest installed version) |
| **Source Brief** | N/A — no `F-PG_CODE.md` Brief exists for this lane (BRD generated Fresh Mode from PREBRIEF + HTML, not from a Brief). Variant decided via **Variant Fallback from BRD** (see §0.1.1). |
| **Source BRD** | `BRD_F-PG_GL-Posting-Group.md` v1.0 — status: ✅ APPROVED (2026-08-10) |
| **Source HTML** | `f-postgrp.html` — passed UX gate + Coverage gate (round 3, 11/11 BLOCK fixed, GAP-01/02/03 fixed — see HTML PREFLIGHT comment) |
| **Author** | frd-generator-v6 (AI-generated FRD, BA review pending) |
| **Reviewers** | BA (Strike), Finance Lead, Tech Lead |

### §0.1.1 Variant Decision (Variant Fallback — no Brief §3.4 available)

No Brief Generator Hints exist for this feature (WF-01 lane ran Fresh/Reverse Mode: PREBRIEF → HTML → BRD → FRD, skipping the Brief stage entirely). Applying the skill's **Variant Fallback** formula against BRD facts:

| Input | Value | Source |
|---|---|---|
| pages | **7** (P-01..P-07) | BRD §14.6 Screen Inventory |
| states | **3** (ร่าง / ใช้งาน / ไม่ใช้งาน — all-directional, BR-06) | BRD §8.1 State Diagram |
| approval | **No** (OB-5 — no DOA, no Approver in any §5 step) | BRD §5, §16.1 |
| money/calc rules | Rules exist (R01/R02 account-type validation) but are **validation constants**, not calculation engines | BRD §9.1 |
| §9.5 Engine Management | **None** — BRD §13 Phase 4 explicitly states "ไม่มีในรอบนี้" (GL resolve engine is out-of-scope, BR-08) | BRD §13, §9.5 |

Formula:
- `pages ≤ 2 AND states ≤ 2 AND NOT approval` → LEAN — **fails** (pages=7)
- `states ≥ 4 OR (approval AND money) OR §9.5 has Engine Management` → FULL — **fails** (states=3, no approval, no engine mgmt)
- else → **STANDARD**

**Decision: STANDARD (7 files: 00/01/02/03/04/05/06 — no 07_LOCKED_DECISIONS, no INDEX)**

**Judgment note (per task instruction to weigh STANDARD vs FULL explicitly):** This feature has real complexity signals that could tempt an upgrade to FULL — 2 parallel entities (dual-tab), IR-PG-01 partial-lock (a genuinely two-part rule), 8 FIXED business rules (BR-01..08) + 1 DYNAMIC (R09) + 1 WARNING gap, and ~20 API endpoints once CRUD+bulk+import/export are enumerated per tab. However, none of the hard FULL triggers fire: only **3** independent states (not ≥4), **zero** approval steps, **zero** calculation engines beyond one integration engine (COA resolver, §3.2), and total business rules (~10) stay well under the ">15 rules" FULL upgrade signal in `pack-variants.md`. The high API count is a symptom of **entity duplication** (tab1 and tab2 each need CRUD+status+bulk-delete+import+export = 9 endpoints × 2), not of business complexity — it does not by itself justify FULL. **Verdict: STANDARD stands**, logged here per Lane Mode transparency requirement.

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-08-10 | frd-generator-v6 (AI, Lane Mode no-ask) | Initial FRD generation from BRD v1.0 APPROVED + HTML v8 (f-postgrp.html, post round-3 coverage-gate fixes). Resolves OQ-PG-02 (COA sync contract) inline per BRD §15 instruction. Supersedes stale FRD pack v5.1 referenced in BRD OQ-PG-05. |

---

## §0.3 Scope

### In Scope
- **Tab 1 — Specific Posting Groups** (`GL_Posting_Group`): CRUD, 3 independent statuses (ร่าง/ใช้งาน/ไม่ใช้งาน), bulk status-change + bulk delete (skips `used>0`), CSV import (merge-only) + export, per `kind` (เจ้าหนี้/สินค้าคงคลัง/ธนาคาร/ลูกหนี้)
- **Tab 2 — General Posting Setup** (`GL_Posting_Setup`): CRUD, same status/bulk/import/export pattern, matrix `bus_group × prod_group → 3 accounts`
- Validation per R01-R07 (COA leaf+postable+active+type-match, unique code/combination, kind locked after create, clear account fields on kind-change pre-submit)
- **IR-PG-01** partial lock: `used>0` locks **only** `code` (tab1) / `bus+prod` combination (tab2) — name/account/status remain editable always
- **R05** kind lock: `kind` is read-only in edit mode **unconditionally** — independent of `used`
- COA dropdown integration — **this FRD resolves OQ-PG-02** by specifying the real API contract (§2.5 of `02_API.md`) replacing the current 16-account hardcoded mock
- CSV import/export, merge-only, per-tab, 3-step (pick → preview → done)
- Contract served to Item Master (F-PDM): `GET /gl/posting-groups?type=product`, `GET /gl/vat-groups` (declared in `02_API.md` §2.6 — see gap notes for OQ-PG-04/OQ-PG-01)

### Out of Scope (BRD §3.2 / FN-40 — carried forward, do not re-introduce)
- **Import Replace/merge-overwrite mode** — banned by 2026-08-09 lane decision (LOCK-03). Import is **merge-only, add-only**, permanently. No mode selector exists or should exist.
- **Kind change after create** — `kind` locked forever post-create (R05/LOCK-02), regardless of `used`.
- **Single-row delete** — no per-row delete button exists or should exist; only bulk-delete (which auto-skips `used>0`).
- **VAT Posting Setup (tab 3)** — not built. Blocked on **OQ-PG-01**.
- **Business/Product Group management UI** — not built. Blocked on **OQ-PG-04**.
- **Real GL posting** — this feature is a mapping/translation layer ONLY (**BR-08/LOCK-05**). The GL/Journal Engine resolves and posts at document-time; that engine is entirely out of this FRD's scope.
- **Approval chain / DOA** — none. 4 DOA placeholder fields exist on both entities and are always `null` (OB-5/LOCK-04).
- **hint-i / field-help / ph-sub** — cut per lane decision (OB-7); no tooltip help affordances in this feature's forms.

### Out of Scope (Phase 2.5 Lane-Mode conservative defaults — flagged, not user-confirmed)
- DI-01..04, CA-01, CA-07, ST-02, ST-04, PM-03/04, FU-01/02 — all remain **☐ unconfirmed** in BRD §10.2. Lane Mode applied conservative defaults for the subset that is safe to default (see `05_RULES.md` §5.5, all tagged `[AI-DEFAULT]`) and logged the rest as Open Questions below (§0.8) for BA confirmation at SOW3.7 — **not silently decided**.

---

## §0.4 Roles & Responsibilities (COSO)

> BRD §5 confirms **no Approver in any workflow step** (OB-5 — DOA placeholder null ×4, no NOTIF emit). SoD (Maker≠Approver) passes vacuously since there is no Approver to conflict with Maker.

| Role | Person/Team | Responsibilities |
|---|---|---|
| **Maker** | Finance Lead | Create/edit/status-change/bulk-delete/import records in both tabs |
| **Checker** | — (none) | N/A — no checker step defined in BRD §5 |
| **Approver** | — (none, OB-5) | N/A — no sign-off step; system commits Maker's action immediately |
| **Owner / Watcher** | Auditor / Compliance | View + export only (read-only, no create/edit/delete) |
| **System** | Backend | Validation (R01-R07), audit log (S01-07), COA resolve (ENG-PG-01) |
| **Future consumer (not built)** | Vendor/Customer/Item/Bank Master maintainer | Will select posting group/setup at master-create time once those masters exist |

---

## §0.5 Dependencies

### Upstream (this feature depends on)
| Dependency | Type | Source |
|---|---|---|
| Chart of Accounts (COA) | API (leaf+postable+active accounts, filtered by type) | F-COA-001 — **resolved this pass, see 02_API.md §2.5 (OQ-PG-02)** |

### Downstream (features that depend on this)
| Consumer | What it uses |
|---|---|
| Item Master (F-PDM) | `GET /gl/posting-groups?type=product` + `GET /gl/vat-groups` — declared contract, see 02_API.md §2.6. **Gap:** prod-group value set mismatch — decided 2026-08-10 (OQ-PG-04, use Item's 6-value set), data-sync build scheduled Phase 2 |
| Vendor / Customer / Bank Master (not built yet) | Will soft-reference `GL_Posting_Group.code` at master-create time (future edge, declared but not implemented) |
| GL / Journal Engine (out of scope, BR-08) | Resolves `(vendor/customer→code)` and `(bus×prod→combination)` into journal lines at document-posting time — cross-module contract declared in 02_API.md §2.7, **not implemented in this feature** |

### External
| Service | Purpose |
|---|---|
| F-COA-001 (Chart of Accounts) | Source of truth for all account dropdowns — see §2.5 |

---

## §0.6 Stack & Architecture

| Layer | Technology |
|---|---|
| Frontend | Vanilla JS SPA (single HTML file, component-state routing — see 01_UI §1.0 Section M notes) |
| API | REST, `/api/v1/gl/...` |
| Database | Relational (PostgreSQL assumed per CUBE ERP convention) |
| Auth | Role-based (Finance Lead / Auditor) |

---

## §0.7 Multi-Tenant & Security Context

- [x] Multi-tenant feature: assumed YES (CUBE ERP standard RLS pattern) — BRD does not explicitly discuss tenancy; carried as convention default, not contradicted by BRD.
- [ ] PII data involved: **NO** (BRD §16.2 — ISO/IEC 27701 not applicable, no PII fields)
- [x] Financial data: **YES** — control-account mapping; BRD selected **Security Preset P4 (Financial/Payment, 16 controls)** overriding the module-type default of P3 (see BRD §16.1)
- [x] Audit log required: **YES** — S01-07 Immutable Master Data Log (Must)

**Security Bible domains applied:** D2 (Auth/Session), D5 (Financial — audit mandatory on every account/status/code change), D9 (Audit Logging), D15 (Admin Actions), D17 (Multi-Tenant Isolation) — see `05_RULES.md` §5.7

### §0.7.1 Data Classification Summary

- [ ] Has Restricted fields — **none**
- [ ] Has Confidential fields — **none**
- [x] **Internal only (default)** — all fields (account codes, group codes, status) classified **Internal**; none are PII or salary-like data. See `04_DB.md` §4.6.

---

## §0.8 Open Questions

| ID | Question | Blocking? | Owner | Status carried from BRD §15 |
|---|---|---|---|---|
| **OQ-PG-01** | Tax mapping gap: field-on-Tax-master (A) vs tab-3 "VAT Posting Setup" (B, recommended) vs status-quo (C) | NO — decided, build deferred | Strike (product owner) | **✅ DECIDED 2026-08-10 — Option B** (tab 3 "VAT Posting Setup"). This is a **decision-only** closure — BRD §13 now schedules the build as **Phase 2** of the delivery plan, not in this FRD/HTML. Tab-3 VAT Posting Setup remains fully out of scope of this FRD Pack; the next lane pass will produce its own HTML (new ux/coverage gate cycle) + FRD delta before dev implements it. |
| **OQ-PG-02** | COA dropdown hardcode (16 accounts) → must sync from F-COA-001, filtered leaf+postable+active+type (R02) | YES — blocks production go-live (mock accounts are placeholder) | FRD/Dev team | **✅ RESOLVED IN THIS PASS** — real API contract written in `02_API.md` §2.5 (`ENG-PG-01 coa-account-resolver` consuming `GET /api/v1/coa/accounts`). See also `03_LOGIC.md` §3.2. |
| **OQ-PG-03** | `used` mock counter → must become real journal-post count; must reconfirm IR-PG-01 semantics against real `used` | YES — launch blocker per BRD §16.4 R-05 | Strike | Target: "ก่อน dev handoff" (before dev handoff) — **still open**, target date not yet reached, no action needed from this FRD beyond flagging (see `05_RULES.md` BR-05 note). |
| **OQ-PG-04** | `bus_group`/`prod_group` value set (`DOMESTIC/FOREIGN × GOODS/SERVICE`) does not match Item Master's 6-value product-group set (`FINISHED/RAWMAT/PACKAGING/SERVICE/TRADE/EXPENSE`) | NO — decided, build deferred | Strike (product owner) | **✅ DECIDED 2026-08-10 — use Item Master's 6-value set as the `prod_group` axis** + build an Admin Panel for R09 (lookup value management). This is a **decision-only** closure — BRD §13 now schedules the build as **Phase 2**, not in this FRD/HTML. This FRD Pack still documents the *current as-built* GOODS/SERVICE value set (§0.9 Glossary + `04_DB.md`) and keeps the Item Master contract endpoint (`02_API.md` §2.6) as **contract-declared but data-not-synced** until the Phase 2 lane pass ships the new axis. |
| **OQ-PG-05** | FRD pack v5.1 was stale | NO — action item, not a decision | BA | **✅ RESOLVED** — this document is the regenerated pack. |
| OQ-BRD-06 | Security Preset P4 vs P3 confirmation | NO | Finance Lead / Compliance | Still open per BRD — inherited, not this FRD's concern to resolve, carried forward for visibility. |
| **OQ-FRD-07 (new, this pass)** | DI-01..04 / CA-01 / CA-07 / ST-02 / ST-04 / PM-03/PM-04 / FU-01/FU-02 (BRD §10.2, all ☐ unconfirmed) | NO (defaults applied, safe-side) | BA (SOW3.7) | Lane Mode applied conservative `[AI-DEFAULT]` handling per probe — see `05_RULES.md` §5.5. BA must tick ☑/☐ at SOW3.7; none of these block this FRD's delivery. |

> Resolved questions (OQ-PG-02, OQ-PG-05) are reflected directly in the relevant pack files rather than moved to a 07_LOCKED_DECISIONS file, since this is a STANDARD-variant pack (no 07 file — see `references/pack-variants.md`).

---

## §0.9 Glossary

| Term | Definition |
|---|---|
| GL | General Ledger |
| Posting Group | (Tab 1) mapping of an entity `kind` (เจ้าหนี้/สินค้าคงคลัง/ธนาคาร/ลูกหนี้) → control account(s) |
| Posting Setup | (Tab 2) mapping of `bus_group × prod_group` → sales/purchase/COGS accounts |
| `kind` | One of 4 values: `vendor` (เจ้าหนี้), `inventory` (สินค้าคงคลัง), `bank` (ธนาคาร), `customer` (ลูกหนี้) — as-built field values from HTML (BRD uses Thai labels for the same 4) |
| `bus_group` (as-built) | `DOMESTIC` \| `FOREIGN` — **as-built value set**, does not map to any external master yet |
| `prod_group` (as-built) | `GOODS` \| `SERVICE` — **as-built value set**, gap vs Item's 6-value set (OQ-PG-04) |
| `used` | Count of journal lines already posted through this mapping (currently **mock**, static — OQ-PG-03). Drives IR-PG-01 partial lock. |
| IR-PG-01 | Partial-lock rule: `used>0` locks **only** `code` (tab1) / `bus+prod` (tab2). Confirmed 2026-08-09 (มติ) — **not** AI-inferred. |
| R05 | Separate rule: `kind` is **always** locked in edit mode, independent of `used`. Do not conflate with IR-PG-01. |
| Soft-reference | Storing `code`/`combination` as a plain value (no DB-level FK) so downstream masters/documents can reference it without breaking when it's edited |
| DOA | Delegation of Authority — not used in this feature; 4 placeholder fields always `null` |

---

## §0.10 Pack Navigation

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW.md | All | This file — meta + scope + Coverage Manifest |
| 01_UI.md | FE dev | Pages + Layout Decision Log + Journey (HTML-first, Recognize & Validate) |
| 02_API.md | BE dev (HTTP) | API contracts — 20 endpoints served + 1 consumed (COA) + Cross-Module Contract (GL engine) |
| 03_LOGIC.md | BE dev (logic) | Functions (17) + 1 Engine (`coa-account-resolver`, resolves OQ-PG-02) + Trace Table |
| 04_DB.md | DBA / BE | 2 tables: `T_gl_posting_group`, `T_gl_posting_setup` |
| 05_RULES.md | BE + QA | BR-01..08 + R09 (DYNAMIC) + Tax gap (WARNING) + IR-PG-01/R05 kept separate + Edge Cases |
| 06_TESTS.md | QA | Acceptance criteria + DoD + microcopy-anchored expected text |

---

## §0.11 Scope Lock (STANDARD variant)

> **Scope Lock Ref:** N/A — no formal sign-off document for this lane; BRD §3.4 records these as pseudo-scope-lock via PREBRIEF §0 Obligations + มติ 2026-08-09. Imported verbatim below — **immutable**, no spec in this pack may override these.

| LOCK-ID | Statement | Source |
|---|---|---|
| LOCK-01 | IR-PG-01 partial lock: `used>0` locks ONLY `code`(tab1)/`combination`(tab2) — name/account/status always editable | BRD §3.4, PREBRIEF §0 OB-8, มติ 2026-08-09 |
| LOCK-02 | `kind` always locked after create (R05) — independent of `used` | BRD §3.4, FRD pack legacy R05, PREBRIEF OB-1 |
| LOCK-03 | Import = merge-only, add-only. **No** Replace/merge-overwrite mode, ever | BRD §3.4, มติ 2026-08-09, PREBRIEF §2 S-10① |
| LOCK-04 | 3 statuses, free bidirectional transitions, both tabs, no approval | BRD §3.4, PREBRIEF OB-6 + OB-5 |
| LOCK-05 | This feature does not post to GL itself — GL/Journal Engine posts | BRD §3.4, PREBRIEF §0.2/§4 BR-08 |

**Scope Drift check:** None found — BRD §3.4 confirms `_COVERAGE_REPORT.md` (Iteration 2) shows HTML covers 34/34 contract items, 0 gap-block, 0 gap-warn, 0 scope-creep. This FRD's API/DB/Rules design was cross-checked against the HTML as-built (§1.0 Section M) and introduces no new scope beyond BRD §3.1/§3.2.

---

## §0.12 Coverage Manifest (BRD → Pack, no requirement dropped)

| BRD Ref | Requirement (short) | Located at |
|---|---|---|
| §7 S-01 | Create Specific Posting Group | 01_UI P-02 · 02_API-02 · 03_LOGIC FN-01/FN-03 · 06_TESTS AC-01 |
| §7 S-02 | Create General Posting Setup | 01_UI P-03 · 02_API-11 · 03_LOGIC FN-07/FN-09 · 06_TESTS AC-04 |
| §7 S-03 | Edit record with `used=0` | 01_UI P-04/P-05 · 02_API-04/13 · 03_LOGIC FN-02/FN-08 · 06_TESTS AC-06 |
| §7 S-04 | Edit record with `used>0` (IR-PG-01) | 01_UI P-04/P-05 · 02_API-04/13 · 05_RULES BR-05(IR-PG-01) · 06_TESTS AC-07/AC-08 |
| §7 S-05 | Validation errors | 02_API-02/11 · 05_RULES §5.4 · 06_TESTS AC-02/AC-05 |
| §7 S-06 | Free status change | 01_UI P-04/P-05 · 02_API-05/14 · 03_LOGIC FN-05/FN-11 · 05_RULES BR-06 · 06_TESTS AC-09 |
| §7 S-07 | Bulk delete (skip used>0) | 01_UI P-01/P-07 · 02_API-06/15 · 03_LOGIC FN-06/FN-12 · 05_RULES BR-04(R06) · 06_TESTS AC-10 |
| §7 S-08 | Import CSV merge-only | 01_UI P-06 · 02_API-07/08/16/17 · 03_LOGIC FN-13/FN-14 · 05_RULES BR-07 · 06_TESTS AC-11..14 |
| §7 S-09 | Export CSV | 01_UI P-01 · 02_API-09/18 · 03_LOGIC FN-15 · 06_TESTS AC-15 |
| §9 BR-01/R01/R02 | COA leaf+postable+active+type-match | 02_API §2.5 · 03_LOGIC ENG-PG-01/FN-03/FN-09 · 05_RULES BR-01 · 06_TESTS AC-01/AC-02/AC-16 |
| §9 BR-02/R03,R04 | Unique code / combination | 05_RULES BR-02 · 06_TESTS AC-02/AC-05 |
| §9 BR-03/R05 | Kind locked always | 05_RULES BR-03 · 06_TESTS AC-17 |
| §9 BR-03/R07 | Clear accounts on kind change pre-submit | 03_LOGIC FN-03 note · 05_RULES BR-03 · 06_TESTS AC-18 |
| §9 BR-04/R06 | No delete when used>0, bulk skip | 05_RULES BR-04 · 06_TESTS AC-10 |
| §9 BR-05/IR-PG-01 | Partial lock code/combination only | 05_RULES BR-05 · 06_TESTS AC-07/AC-08 |
| §9 BR-06 | 3 free statuses, no approval | 05_RULES BR-06 · 06_TESTS AC-09 |
| §9 BR-07 | Merge-only import, blank status=draft | 05_RULES BR-07 · 06_TESTS AC-11/AC-13 |
| §9 BR-08 | No GL posting (mapping layer only) | 00_OVERVIEW §0.11 LOCK-05 · 02_API §2.7 · 05_RULES BR-08 |
| §9 R09 | bus/prod value set — DYNAMIC | 04_DB §4.1 note · 05_RULES §5.1 R09 · 00_OVERVIEW OQ-PG-04 |
| §9 Tax mapping gap | WARNING — no tab 3 | 05_RULES §5.1 (Tax gap) · 00_OVERVIEW OQ-PG-01 |
| §10.1 E01-E10 | BA-confirmed edge cases | 05_RULES §5.5 EC-01..10 |
| §10.2 DI/CA/ST/PM/FU | AI-pattern edge cases (unconfirmed) | 05_RULES §5.5 (tagged `[AI-DEFAULT]` where defaulted) · 00_OVERVIEW OQ-FRD-07 |
| §12.1 Upstream (COA) | COA leaf+postable+active sync | 02_API §2.5 (resolves OQ-PG-02) |
| §12.1 Downstream (Item Master) | 2 GET endpoints contract | 02_API §2.6 |
| §12.1 Downstream (GL/Journal Engine) | resolve+post at doc-time | 02_API §2.7 (Cross-Module Contract, not implemented here) |
| §12.1 Downstream (Tax Code gap) | no mapping | 00_OVERVIEW OQ-PG-01 |
| §14.6 P-01..P-07 | Screen Inventory | 01_UI §1.0/§1.1 |
| §16 Security Preset P4 | 16 controls | 05_RULES §5.7 |

**Summary:** Stories 9/9 ✅ · Rules 10/10 ✅ · Edges 10 confirmed / 14 AI-pattern (flagged) ✅ · Cross-module rows 4/4 ✅ · No requirement without a landing spot.
