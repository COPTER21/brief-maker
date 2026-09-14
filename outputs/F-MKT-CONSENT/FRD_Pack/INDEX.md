# INDEX — FRD F-MKT-CONSENT ความยินยอม PDPA (FULL)

> **Variant:** FULL (9 files + INDEX) · **Audience:** All roles (entry point)
> **FRD v1.1 (2026-09-14)** — sync BA-gate round: FIX-01 (answered=terminal · re-answer block · evidence immutable) · FIX-02 (role check ใน mutation) · FIX-03 (send version snapshot) · FIX-04 (double-submit `_busy`) · FIX-05 (sub-status guards) · FIX-06 (contract anchors F136/F031/F157) · FIX-07/08 (demo-only + pill). + OQ-CNS-01/02/03.

---

## 📂 Pack Contents
| # | File | Audience | Content |
|---|---|---|---|
| 00 | OVERVIEW.md | All | Meta + Scope + Roles + Coverage Manifest + OQ |
| 01 | UI.md | FE | Layout Decision Log + 5 pages + drawers/modals + Journey |
| 02 | API.md | BE (HTTP) | 20 API contracts + Cross-Module + resolve locked contract |
| 03 | LOGIC.md | BE (logic) | 21 Functions + 2 Engines + Trace + Request state machine |
| 04 | DB.md | DBA / BE | 9 tables (+answered_at, +vers snapshot) + Classification |
| 05 | RULES.md | BE + QA | 26 BR + CSQ + State + Permission + 14 Edge + Errors + Security |
| 06 | TESTS.md | QA | 25 AT + 10 FN-40 negatives + Cross-Module + DoD |
| 07 | LOCKED_DECISIONS.md | All | Scope Lock (13) + 8 LD |

---

## 🔍 Quick Nav
- **FE dev** → 01_UI (§1.0 Decision Log, §1.2 per-page actions→API)
- **BE dev** → 02_API §2.2 + 03_LOGIC §3.3 (which FN/ENG) + 04_DB + 05_RULES
- **DBA** → 04_DB §4.2 (RLS/indexes) + §4.6 Classification
- **QA** → 06_TESTS §6.1 (AT) + §6.2 (FN-40) + 05_RULES §5.5 (edge)
- **PM/risk** → 00 §0.8 (OQ) + 07 §7.0 (Scope Lock)
- **Architect** → 03 §3.2 (Engines DRAFT) + §3.4 (CSQ/F143 deps)

---

## 🔗 Cross-Reference

### Page → API
| Page | Action | Calls |
|---|---|---|
| P-01 Registry | row click / filter / stat | API-15 / API-14 / API-18 |
| P-02 Requests | create / send / link / doc | API-07 / API-09 / API-10 / API-11 |
| P-03 Purposes | create / version / close | API-02 / API-04 / API-05 |
| P-04 Resolve | ตรวจสิทธิ์ | API-20 |
| P-05 Recipient | load / answer | API-12 / API-13 |
| (drawer) consent | withdraw / renew | API-17 / API-19 |

### API → Logic (ดู 03_LOGIC §3.3 — authoritative)
| API | Functions | Engines |
|---|---|---|
| API-02 POST purposes | FN-01 | — |
| API-04 POST versions | FN-02, FN-17 | — |
| API-07 POST requests | FN-05 | — |
| API-13 POST answer | FN-09, FN-10, FN-11 | — |
| API-17 POST withdraw | FN-13, FN-19 | — |
| API-19 POST renew | FN-14, FN-05, FN-19 | — |
| API-20 POST resolve | FN-20 | ENG-01, ENG-02 |
| API-14/15/16/18 GET | FN-11/12/18 | ENG-02 |

### API → DB
| API | Reads | Writes |
|---|---|---|
| API-02 | T_consent_purpose | T_consent_purpose, T_consent_policy_version, T_audit_log |
| API-13 | T_consent_request(+purpose), T_consent_policy_version | T_consent, T_consent_evidence, T_consent_history, T_consent_csq_outbox |
| API-17 | T_consent | T_consent, T_consent_history, T_consent_csq_outbox |
| API-20 | T_consent, T_consent_purpose | — (read-only) |

### Engine ↔ Feature
| Engine | Used by | Status |
|---|---|---|
| ENG-01 consent-resolution-engine | F-MKT-CONSENT (this) + F143 (planned) | DRAFT |
| ENG-02 consent-status-evaluator | F-MKT-CONSENT (this) + ENG-01 | DRAFT |

---

## 🚨 R8 Verification Matrix (Phase 3.5 Section C anchor)

**ทุก mutation API มี ≥1 Function/Engine:**
| API (mutation) | FN | ENG | ✅ |
|---|---|---|---|
| POST purposes (02) | 1 | 0 | ✅ |
| POST versions (04) | 2 | 0 | ✅ |
| POST close (05) | 1 | 0 | ✅ |
| POST requests (07) | 1 | 0 | ✅ |
| POST send (09) | 1 | 0 | ✅ |
| POST link-export (10) | 1 | 0 | ✅ |
| POST answer (13) | 3 | 0 | ✅ |
| POST withdraw (17) | 2 | 0 | ✅ |
| POST renew (19) | 3 | 0 | ✅ |
| POST resolve (20) | 1 | 2 | ✅ |

**No orphan:** FN-01..20 + ENG-01/02 traced ✅ (ดู 03 §3.3)

---

## 📊 Pack Statistics
| Metric | Count |
|---|---|
| Pages / surfaces | 5 (4 tab + recipient) |
| Drawers/Modals | 11 |
| APIs | 20 |
| Functions | 21 (+FN-21 snapshotVers) |
| Engines | 2 |
| DB Tables | 9 (+audit shared) |
| Business Rules | 26 + 5 CSQ (BR-23..26 = BA-gate fixes) |
| FN positive | 20 · FN-40 negatives | 10 |
| Edge Cases | 14 (+EC-12/13/14) |
| Error codes | 14 (+BR_REQUEST_CLOSED, BR_NOT_GRANTED) |
| Locked Decisions | 8 · Scope Locks | 13 |
| CSQ events | 7 (declare-only) |
| Open Questions | 11 (+OQ-CNS-01/02/03) |
| Acceptance Tests | 25 (AT-21..25 = FIX-01..05) |

---

## 🎯 Coverage Manifest Pointer
- ทุก BRD requirement → 00_OVERVIEW §0.12 (Stories 20/20 · Rules 22+CSQ · Edges 5/5) — Phase 3.5 Section K ✅
- Scope Lock: 07_LOCKED §7.0 (N/A standalone · 13 locks inherited)

## Chain ถัดไป (WF-01)
- **step 7 companion:** `csq-declaration` → `CSQ_BRIEF_F-MKT-CONSENT.md` (**ผู้ใช้สั่ง/parent — ไม่ auto**)
- **step 8:** html-ui-brief · **step 9:** ai-testcase-md-generator (อ่าน 05+06+02+03) · **step 10:** qc-coverage R2
