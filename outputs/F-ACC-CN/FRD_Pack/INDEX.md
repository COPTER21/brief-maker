# INDEX — FRD F-ACC-CN ใบลดหนี้ลูกค้า (Credit Note)

> **Variant:** FULL (9 files + INDEX) · **Audience:** All roles (entry point)
> **Purpose:** Cross-reference + Function Trace + R8 verification + Quick Nav
> Source of truth = `outputs/F-ACC-CN/F-ACC-CN_credit-note.html` (HTML-first)

---

## 📂 Pack Contents

| # | File | Audience | Purpose |
|---|---|---|---|
| 00 | OVERVIEW.md | All | Meta + Scope + Coverage Manifest (22 FN) |
| 01 | UI.md | FE + html-generator-v9 | Layout Decision Log + 4 pages + journey |
| 02 | API.md | BE (HTTP) | 15 API + Cross-Module Contract |
| 03 | LOGIC.md | BE (logic) | 15 Functions + 2 Engines + Trace |
| 04 | DB.md | DBA/BE | 5 tables + classification |
| 05 | RULES.md | BE + QA | 15 BR + state machine + edge + errors + security |
| 06 | TESTS.md | QA | AC (22 FN) + TC + XT + DoD |
| 07 | LOCKED_DECISIONS.md | All | Scope Lock §7.0 (10) + 6 LD |
| — | INDEX.md | All | this file |

---

## 🔍 Quick Nav
- **FE dev** → 01_UI (route/pattern/microcopy) → 02_API (data shape)
- **BE dev** → 02_API §2.2 → 03_LOGIC §3.3 (which FN/ENG) → 04_DB → 05_RULES
- **DBA** → 04_DB §4.2/§4.6
- **QA** → 06_TESTS §6.1 AC + 05_RULES §5.5 edge + §6.4 DoD
- **PM** → 00_OVERVIEW §0.8 OQ + 00 §0.12 Coverage
- **Architect** → 03_LOGIC §3.2 (ENG cn-totals/ar-open-item DRAFT) + 07 §7.1 LD

---

## 🔗 Cross-Reference

### Page → API
| Page | Action | Calls |
|---|---|---|
| P-01 list | filter/sort/search | API-01 |
| P-01 list | CSV | API-10 |
| P-01 list | row click | API-02 → P-04 |
| P-02 create s1 | invoice picker | API-11 |
| P-02 create s2 | SR picker (RET) | API-12 |
| P-02 create | save draft | API-03 |
| P-03 edit | save | API-04 |
| P-02/P-04 | submit (slot picker) | API-05 |
| P-04 | approve | API-06 |
| P-04 | reject | API-07 |
| P-04 / row | cancel | API-08 |
| P-04 | send / resend | API-09 |
| P-04 pdf tab | PDF | API-13 |
| P-04 | ออกเอกสารแก้ไข | API-14 |

### API → Logic (§3.3)
ดู 03_LOGIC §3.3 (authoritative). สรุป: ทุก mutation → ≥1 FN.

### API → DB (side effects)
| API | Reads | Writes |
|---|---|---|
| API-01/02 | T_credit_note(_line) | — |
| API-03/04 | ar_invoice(F094), reason_master | T_credit_note,_line,_attachment,_audit |
| API-05 | T_credit_note | T_credit_note(status/chain), _audit |
| API-06 | T_credit_note, ar_open_item | T_credit_note(status/code/approved), ar_open_item(cn_applied), _audit + JE/VAT (ext) |
| API-07 | T_credit_note | T_credit_note(status/history), _audit |
| API-08 | T_credit_note | T_credit_note(cancelled/cancel_info), _audit |
| API-09 | T_credit_note | T_credit_note(sent), _audit |

### Engine ↔ Feature
| Engine | Used by | Status |
|---|---|---|
| cn-totals-engine | F-ACC-CN (this) · AR Invoice/DN (candidate) | DRAFT |
| ar-open-item-resolver | F-ACC-CN · AR family | DRAFT |
| ENG-DOA / ENG-DOC-NUM / ENG-DOC-STORE / ENG-NOTIFY / ENG-CSQ | external (declare-only) | EXISTING |

---

## 🚨 R8 Verification Matrix (Phase 3.5 Section C)

**ทุก mutation API มี ≥1 Function/Engine:**
| API (mutation) | FN | ENG | ✅ |
|---|:--:|:--:|:--:|
| POST create (03) | 3 | 2 | ✅ |
| PUT update (04) | 3 | 2 | ✅ |
| POST submit (05) | 1 | 1 | ✅ |
| POST approve (06) | 2 | 3 | ✅ |
| POST reject (07) | 1 | 0 | ✅ |
| POST cancel (08) | 1 | 1 | ✅ |
| POST send (09) | 1 | 2 | ✅ |
| POST revise-doc (14) | 1 | 0 | ✅ |

**No orphan Function/Engine:** FN-01..15 + ENG cn-totals + ar-open-item ทุกตัว trace ใน §3.3. ✅

---

## 📊 Pack Statistics
| Metric | Count |
|---|---|
| Pages | 4 (+overlay modals) |
| APIs | 15 |
| Functions | 15 |
| Engines | 2 feature-owned (+5 external) |
| DB Tables | 5 |
| Business Rules | 15 (BR-01..15) |
| FN coverage | 22/22 |
| Edge Cases | 6 confirmed + 4 probe |
| Error codes | 21 |
| Scope Locks | 10 |
| Locked Decisions | 6 |
| Declarations | doa + ntf + csq + doccfg + pdfdoc |

---

## Coverage Manifest Pointer
- BRD requirement → ที่อยู่: `00_OVERVIEW §0.12` (FN 22/22 · BR 15/15 · Edge 6/6)
- Scope Lock: `07_LOCKED §7.0` (10 LOCK, no drift)
