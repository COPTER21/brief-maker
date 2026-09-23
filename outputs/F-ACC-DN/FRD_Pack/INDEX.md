# INDEX — FRD F-ACC-DN ใบลดหนี้ผู้ขาย (Debit Note)

> **Variant:** FULL (9 files + INDEX) · **Audience:** All roles (entry point)
> **Purpose:** Cross-reference + Function Trace + R8 verification + Quick Nav
> Source of truth = `outputs/F-ACC-DN/F-ACC-DN_debit-note.html` (HTML-first) · Mirror ของ F-ACC-CN re-domain AR→AP

---

## 📂 Pack Contents

| # | File | Audience | Purpose |
|---|---|---|---|
| 00 | OVERVIEW.md | All | Meta + Scope + Coverage Manifest (24 FN) |
| 01 | UI.md | FE + html-generator-v9 | Layout Decision Log + 4 pages + journey |
| 02 | API.md | BE (HTTP) | 17 API + Cross-Module Contract |
| 03 | LOGIC.md | BE (logic) | 17 Functions + 2 Engines + Trace |
| 04 | DB.md | DBA/BE | 5 tables + 1 view + classification |
| 05 | RULES.md | BE + QA | 17 BR + state machine + edge + errors + security |
| 06 | TESTS.md | QA | AC (24 FN) + TC + XT + DoD |
| 07 | LOCKED_DECISIONS.md | All | Scope Lock §7.0 (10) + 8 LD |
| — | INDEX.md | All | this file |

---

## 🔍 Quick Nav
- **FE dev** → 01_UI (route/pattern/microcopy) → 02_API (data shape)
- **BE dev** → 02_API §2.2 → 03_LOGIC §3.3 (which FN/ENG) → 04_DB → 05_RULES
- **DBA** → 04_DB §4.2/§4.6
- **QA** → 06_TESTS §6.1 AC + 05_RULES §5.5 edge + §6.4 DoD
- **PM** → 00_OVERVIEW §0.8 OQ + 00 §0.12 Coverage
- **Architect** → 03_LOGIC §3.2 (ENG dn-totals/ap-open-item DRAFT) + 07 §7.1 LD (LD-07 dnRoom · LD-08 vendorCn)

---

## 🔗 Cross-Reference

### Page → API
| Page | Action | Calls |
|---|---|---|
| P-01 list | filter/sort/search | API-01 |
| P-01 list | CSV | API-10 |
| P-01 list | vendor-credit card/modal | API-17 |
| P-01 list | row click | API-02 → P-04 |
| P-02 create s1 | invoice picker (dnRoom>0) | API-11 |
| P-02 create s2 | RTV picker | API-12 |
| P-02 create | save draft | API-03 |
| P-03 edit | save | API-04 |
| P-02/P-04 | submit (slot picker) | API-05 |
| P-04 | approve | API-06 |
| P-04 | reject | API-07 |
| P-04 / row | cancel | API-08 |
| P-04 | send / resend | API-09 |
| P-04 ref tab | บันทึก vendorCn | API-16 |
| P-04 pdf tab | PDF | API-13 |
| P-04 | ออกเอกสารแก้ไข | API-14 |

### API → Logic (§3.3)
ดู 03_LOGIC §3.3 (authoritative). สรุป: ทุก mutation → ≥1 FN.

### API → DB (side effects)
| API | Reads | Writes |
|---|---|---|
| API-01/02/17 | T_debit_note(_line) · V_vendor_credit_ledger | — |
| API-03/04 | ap_invoice(APINV), reason_master | T_debit_note,_line,_attachment,_audit |
| API-05 | T_debit_note | T_debit_note(status/chain), _audit |
| API-06 | T_debit_note, ap_open_item | T_debit_note(status/code/apply_to_ap/vendor_credit), ap_open_item(dn_applied), _audit + JE (ext) |
| API-07 | T_debit_note | T_debit_note(status/history), _audit |
| API-08 | T_debit_note | T_debit_note(cancelled/cancel_info), _audit |
| API-09 | T_debit_note | T_debit_note(sent), _audit |
| API-16 | T_debit_note | T_debit_note(vendor_cn/date/input_vat_*), _audit + input_vat_line (ext) |

### Engine ↔ Feature
| Engine | Used by | Status |
|---|---|---|
| dn-totals-engine | F-ACC-DN (this) · AP Invoice/CN kernel (candidate) | DRAFT |
| ap-open-item-resolver | F-ACC-DN · AP family | DRAFT |
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
| POST vendor-cn (16) | 1 | 1 | ✅ |

**No orphan Function/Engine:** FN-01..17 + ENG dn-totals + ap-open-item ทุกตัว trace ใน §3.3. ✅

---

## 📊 Pack Statistics
| Metric | Count |
|---|---|
| Pages | 4 (+overlay modals incl. vendorCn) |
| APIs | 17 |
| Functions | 17 |
| Engines | 2 feature-owned (+5 external) |
| DB Tables | 5 (+1 view V_vendor_credit_ledger) |
| Business Rules | 17 (BR-01..17) |
| FN coverage | 24/24 |
| Edge Cases | 7 confirmed + 5 probe |
| Error codes | 22 |
| Scope Locks | 10 |
| Locked Decisions | 8 |
| Declarations | doa + ntf + csq + doccfg + pdfdoc |

---

## Coverage Manifest Pointer
- BRD requirement → ที่อยู่: `00_OVERVIEW §0.12` (FN 24/24 · BR 17/17 · Edge 7/7 · Story 10/10)
- Scope Lock: `07_LOCKED §7.0` (10 LOCK, no drift)

## 🔄 Mirror Delta vs F-ACC-CN (สำหรับ reviewer)
| จุด | CN (AR) | DN (AP) |
|---|---|---|
| Domain | ลูกค้า / ใบแจ้งหนี้ AR | ผู้ขาย / ใบตั้งหนี้ AP |
| VAT | ภาษีขาย (output) | **ภาษีซื้อ (input)** — negative |
| Prefix | CN-YYYY-NNNN | **DN-YYYY-NNNN** |
| Return doc | Sales Return (SR) | **RTV** (คืนสินค้าจากผู้ขาย) |
| เพดาน | outstanding (จ่ายครบออกไม่ได้) | **dnRoom ไม่หัก paid** (จ่ายครบยังออกได้ → vendorCredit) |
| VAT reversal | ทันทีเมื่อ approve | **gated by vendorCn** (ม.82/10) |
| FN added | — | **FN-20 (vendor credit) · FN-21 (vendorCn input VAT)** |
| JE | Dr รายได้/ภาษีขาย · Cr ลูกหนี้ | **Dr เจ้าหนี้ · Cr รับคืน/ส่วนลด · Cr ภาษีซื้อ** |
