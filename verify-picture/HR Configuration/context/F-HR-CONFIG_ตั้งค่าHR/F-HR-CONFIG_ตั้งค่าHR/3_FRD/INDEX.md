# INDEX — FRD F-HR-CONFIG · HR Configuration (ตั้งค่าHR)

> **Variant:** FULL · **Audience:** ทุก role (จุดเริ่มต้นของการนำทาง)
> **Purpose:** Cross-reference + Trace matrices + Quick Nav

---

## 📂 Pack Contents

| # | File | Audience | Size hint |
|---|---|---|---|
| 00 | `00_OVERVIEW.md` | All + **ทีมของอีก 18 feature HR** | Meta + Scope + **สัญญาข้าม feature §0.13–§0.15** + Coverage Manifest |
| 01 | `01_UI.md` | FE dev | Layout Decision Log + 10 หน้า/ส่วน (7 routes) |
| 02 | `02_API.md` | BE dev (HTTP) | 17 API + Cross-Module Contract |
| 03 | `03_LOGIC.md` | BE dev (logic) | 20 Functions + 2 Engines + 2 Candidates + Trace |
| 04 | `04_DB.md` | DBA / BE | 16 tables + Classification |
| 05 | `05_RULES.md` | BE + QA | BR-01…21 + BR-CSQ-01…05 + VR-01…30 + Edge + Errors |
| 06 | `06_TESTS.md` | QA | AT-01…38 + TC inventory + DoD + Cross-module |
| 07 | `07_LOCKED_DECISIONS.md` | All | Scope Lock (IMMUTABLE) + LD-01…08 |
| — | `UI_BRIEF_ตั้งค่าHR.md` | FE + designer | (S7) สรุปหน้าจอจริง + Drift Log |

> **ไม่มี `PRINT_SPEC.md` โดยเจตนา** — ไม่มีท่อ `pdfdoc` (ดู `00_OVERVIEW §0.10`)

---

## 🔍 Quick Nav by Question

**"ผมทำ feature HR ตัวอื่น — ต้องต่อกับตัวนี้ยังไง?"**
→ `00_OVERVIEW §0.13` (Published Config Surface + endpoint + กติกา C-1…C-6)
→ `00_OVERVIEW §0.14` (Effective-Dated Contract P-1…P-9)
→ `00_OVERVIEW §0.15` (Soft-Reference Read Model)
→ `02_API §2.X` (Cross-Module Contract — endpoint + event)

**"ผม FE dev — เริ่มอ่านที่ไหน?"** → `01_UI §1.0` (Layout Decision Log) → `§1.2` (แต่ละหน้า + action → API) → `02_API §2.2` (response schema)

**"ผม BE dev — สร้าง endpoint — เริ่มที่ไหน?"** → `02_API §2.2` → `03_LOGIC §3.3` (เรียก Function/Engine ตัวไหน) → `04_DB` → `05_RULES`

**"ผม DBA — schema มีอะไร?"** → `04_DB §4.1` → `§4.2` (per-table + classification) → `§4.3` (ER) → `§4.4` (migration)

**"ผม QA — test อะไรบ้าง?"** → `06_TESTS §6.1` (AT) → `§6.2` (TC inventory) → `05_RULES §5.5` (edge) → `§6.10` (ข้อความจริงบนจอ) → `§6.4` (DoD)

**"ผม PM — อะไรยังไม่ปิด?"** → `00_OVERVIEW §0.8` (OQ-01…OQ-20 · ข้อที่ blocking) → `07_LOCKED §7.3`

**"ผม Architect — engine ตัวไหนเป็น CUBIC candidate?"** → `03_LOGIC §3.2` (DRAFT 2 ตัว) → `§3.4` (candidate 2 ตัว) → `07_LOCKED §7.1 LD-03` + `§7.4` (tradeoffs)

**"ทำไมถึงไม่มี approval / ไม่มี retro?"** → `07_LOCKED §7.1 LD-04` · `§7.4 AT-02` · `05_RULES §5.9` (NS-01, NS-02)

---

## 🔗 Cross-Reference Tables

### Page → API

| Page | route | Actions | Calls |
|---|---|---|---|
| P-01 | `#/hr-config` | redirect | — |
| P-02…P-07 | `#/hr-config/{leave,ot,holiday,period,appraisal,company}` | list / filter / as-of | API-01 |
| P-02…P-07 | เดียวกัน | กดแถว | API-02 |
| P-02…P-07 | เดียวกัน | + สร้างค่าใหม่ | API-03 → API-06 |
| P-02…P-07 | เดียวกัน | แก้ไข | API-04 → API-05 → API-06 |
| P-02…P-07 | เดียวกัน | ยกเลิกเวอร์ชันรอมีผล | API-07 |
| P-02…P-07 | เดียวกัน | ปิดใช้ / เปิดใช้กลับ | API-11 → API-09 · API-10 |
| P-05 | `#/hr-config/period` | สร้างงวดทั้งปี / ปิดงวด / เปิดงวด | API-14 · API-15 · API-16 |
| P-09 | (drawer) | tab ประวัติ / ใครใช้ค่านี้ | API-12 · API-11 |
| — | (ไม่มี UI) | ปลายทางอ่านค่า | **API-13** · API-17 |

### API → Logic

| API | Functions | Engines |
|---|---|---|
| API-01, API-02, API-17 | FN-01 | — |
| API-03 | FN-02, FN-04, FN-05, FN-17 | — |
| API-04 | FN-03, FN-05, FN-17 | — |
| API-05 | FN-04, FN-05, FN-17 | — |
| API-06 | FN-06, FN-05, FN-20, FN-19, FN-17, FN-16 | — |
| API-07 | FN-07, FN-19, FN-17, FN-16 | — |
| API-08 | FN-08, FN-17 | — |
| API-09 | FN-09, FN-12, FN-17, FN-16 | — |
| API-10 | FN-10, FN-05, FN-20, FN-06, FN-17, FN-16 | — |
| API-11 | FN-12 | — |
| API-12 | FN-11 | — |
| **API-13** | — | **ENG-HRCFG-01** |
| API-14 | FN-13, FN-17 | **ENG-HRCFG-02** |
| API-15 | FN-14, FN-17, FN-16 | — |
| API-16 | FN-15, FN-17 | — |

### API → DB

| API | Reads | Writes |
|---|---|---|
| API-01, API-02 | `T_hr_config_item`, `_version`, payload, `_item_company` | — |
| API-03 | `T_hr_config_item` (dup check) | `T_hr_config_item`, `_item_company`, `_version`, payload, **Audit** |
| API-04, API-05 | `_version`, payload | `_version`, payload, **Audit** |
| **API-06** | `_version`, **`T_hr_pay_period` (FOR SHARE)**, `T_hr_legal_minimum`, `T_hr_config_param` | `_version` (status + window), **Audit**, **CSQ event** |
| API-07 | `_version` | `_version`, **Audit**, **CSQ event** |
| API-08 | `_version` | `_version`, **Audit** |
| API-09 | `T_hr_config_usage` | `T_hr_config_item`, `_version`, **Audit**, **CSQ event** |
| API-10 | `T_hr_pay_period` | `T_hr_config_item`, `_version`, payload, **Audit**, **CSQ event** |
| API-11 | `T_hr_config_usage` | — |
| API-12 | `_version`, payload | — |
| **API-13** | `_item`, `_version`, `_item_company`, payload | `T_hr_config_usage.last_seen_at` (async, best-effort) |
| API-14 | `T_hr_period_rule`, `T_hr_pay_period` | `T_hr_pay_period`, **Audit** |
| API-15, API-16 | `T_hr_pay_period` | `T_hr_pay_period`, **Audit**, (API-15) **CSQ event** |
| API-17 | `T_hr_pay_period` | — |
| **ไม่มี** | — | **ไม่มี DELETE ที่ใดเลย** (BR-07) |

### Engine ↔ Feature

| Engine | Used by | Status |
|---|---|---|
| **ENG-HRCFG-01** `hr-config-resolve` | F-HR-CONFIG (this) + **8 consumer** (Leave · OT/Shift · Shift&Roster · Attendance · Payroll · Performance · Welfare · Salary Structure) | **DRAFT** (register Phase 2 · LD-03) |
| **ENG-HRCFG-02** `hr-period-generator` | F-HR-CONFIG (this) + Payroll · Attendance (คาดการณ์) | **DRAFT** (register Phase 2 · LD-03) |
| `hr-policy-retro-engine` | — | **CANDIDATE** (gated by OQ-04) |
| `hr-eligibility-rule-engine` | — | **CANDIDATE** (gated by OQ-02) |
| ENG-CSQ 7C | F-HR-CONFIG (SecC · 6 event) | **EXISTING** ✅ (เรียกใช้) |
| Policy Center — Audit Trail · Roles & Permissions | F-HR-CONFIG | **EXISTING** ✅ (เรียกใช้) |
| DOA Engine | — (ไม่ใช้รอบนี้) | **EXISTING** ✅ |

---

## 🚨 R8 Verification Matrix

**กติกา 1: ทุก mutation API ต้องมี ≥1 Function/Engine**

| API (mutation) | Functions | Engines | ✅ |
|---|---|:---:|:---:|
| POST /items (API-03) | 4 | 0 | ✅ |
| POST /items/:id/versions (API-04) | 3 | 0 | ✅ |
| PUT /versions/:id (API-05) | 3 | 0 | ✅ |
| POST /versions/:id/publish (API-06) | 6 | 0 | ✅ |
| POST /versions/:id/cancel (API-07) | 4 | 0 | ✅ |
| POST /versions/:id/discard (API-08) | 2 | 0 | ✅ |
| POST /items/:id/deactivate (API-09) | 4 | 0 | ✅ |
| POST /items/:id/reactivate (API-10) | 6 | 0 | ✅ |
| POST /periods/generate (API-14) | 2 | 1 | ✅ |
| POST /periods/:id/close (API-15) | 3 | 0 | ✅ |
| POST /periods/:id/reopen (API-16) | 2 | 0 | ✅ |

**กติกา 2: ไม่มี orphan Function/Engine**

| Function/Engine | Traced ที่ §3.3? |
|---|---|
| FN-01 | ✅ API-01, 02, 17 |
| FN-02 | ✅ API-03 |
| FN-03 | ✅ API-04 |
| FN-04 | ✅ API-03, 05 |
| FN-05 | ✅ API-03, 04, 05, 06, 10 |
| FN-06 | ✅ API-06, API-10, scheduler |
| FN-07 | ✅ API-07 |
| FN-08 | ✅ API-08 |
| FN-09 | ✅ API-09 |
| FN-10 | ✅ API-10 |
| FN-11 | ✅ API-12 |
| FN-12 | ✅ API-11, FN-09 |
| FN-13 | ✅ API-14 |
| FN-14 | ✅ API-15 |
| FN-15 | ✅ API-16 |
| FN-16 | ✅ FN-06, 07, 09, 10, 14 |
| FN-17 | ✅ ทุก mutation function |
| FN-18 | ✅ (nested) FN-05 |
| FN-19 | ✅ FN-06, FN-07 |
| FN-20 | ✅ FN-06, FN-10 |
| **ENG-HRCFG-01** | ✅ API-13 |
| **ENG-HRCFG-02** | ✅ API-14 (ผ่าน FN-13) |
| `hr-policy-retro-engine` | **N/A — ยังไม่สร้าง** (candidate · §3.4 · gated by OQ-04) |
| `hr-eligibility-rule-engine` | **N/A — ยังไม่สร้าง** (candidate · §3.4 · gated by OQ-02) |

**ผล: ไม่มี orphan · mutation API ครบทุกแถว ✅**

---

## 🧾 Declaration Matrix (CSQ)

| # | event_id | ท่อ | Trigger (FRD) | ประกาศไว้ที่ |
|---|---|---|---|---|
| E1 | `hrconfig.published` | SecC | `03_LOGIC FN-06` · `API-06` | `CSQ_BRIEF §2` |
| E2 | `hrconfig.effective` | SecC | `03_LOGIC FN-06` (scheduler/lazy) | เดียวกัน |
| E3 | `hrconfig.cancelled` | SecC | `03_LOGIC FN-07` · `API-07` | เดียวกัน |
| E4 | `hrconfig.deactivated` | SecC | `03_LOGIC FN-09` · `API-09` | เดียวกัน |
| E5 | `hrconfig.reactivated` | SecC | `03_LOGIC FN-10` · `API-10` | เดียวกัน |
| E6 | `hrconfig.period_closed` | SecC `[DEFAULT — OQ-18]` | `03_LOGIC FN-14` · `API-15` | เดียวกัน |
| — | **ไม่มี event อื่น** | — | — | **event ⊆ CSQ_BRIEF เป๊ะ 6/6** ✅ |
| — | ท่อ **OC / DC-เอกสาร / SC** | **ห้ามประกาศ** | — | reject 422 · BR-CSQ-01 |
| — | ท่อ **EC / AC / FC** | ไม่ประกาศ | — | ที่นี่เก็บ "อัตรา" ไม่ใช่ธุรกรรม — ปลายทางประกาศเอง |
| — | **DOA / NTF / DOCCFG / PDFDOC** | **not needed** | — | `5_DECLARATIONS/NOT_NEEDED.md` |

---

## 📊 Pack Statistics

| Metric | Count |
|---|---|
| Pages / ส่วน (routes จริง) | **10 (7 routes + drawer×2 + modal)** |
| APIs | **17** (mutation 11 · read 6 · **DELETE 0**) |
| Functions | **20** |
| Engines (จะ register) | **2** (+ candidate 2) |
| DB Tables | **16** |
| Business Rules | **21 (BR) + 5 (BR-CSQ)** |
| Validation Rules | **30 (VR)** |
| Edge Cases | **15 ยืนยันแล้ว + 18 จาก probing** |
| Error codes | **41** |
| Acceptance Criteria | **38 (AT)** |
| Cross-module test cases | **10 (XT)** |
| Locked Decisions | **8 (LD)** + Scope Lock 8 รายการ |
| Open Questions | **20 (OQ)** — blocking 6 |
| CSQ events | **6 (SecC เท่านั้น)** |
| FN coverage | **53/53** (in scope 42 · ไม่รองรับ 11) |
| Scenario coverage | **35/35** (in scope 24 · ไม่รองรับ 11) |

---

## 🎯 Reading Order Recommendation

**คนอ่านครั้งแรก (ทุก role):** `00_OVERVIEW §0.3` → `§0.13–§0.15` → `01_UI §1.3` Journey → เจาะไฟล์ตาม role

**Dev เข้าใหม่:** `00_OVERVIEW` → `INDEX` (ไฟล์นี้) → `01_UI` (FE) หรือ `02_API` + `03_LOGIC` (BE) หรือ `04_DB` (DBA) → `05_RULES` → `06_TESTS`

**Architect review:** `03_LOGIC §3.2` + `§3.4` (engines/candidates) → `04_DB §4.3` + `§4.8` → `07_LOCKED §7.1` + `§7.4` → matrix ในไฟล์นี้

**ทีมของ feature HR ตัวอื่น:** `00_OVERVIEW §0.13` → `§0.14` → `§0.15` → `02_API §2.X` → **จบ** (ไม่ต้องอ่านไฟล์อื่น)

---

## Coverage Manifest Pointer
- **ทุก BRD requirement → ที่อยู่ใน pack:** `00_OVERVIEW §0.12` (Stories 37 · Rules 21 · VR 30 · Edges 15+17 · FN 53 · Scenario 35) — Phase 3.5 Section K verify
- **Scope Lock:** `07_LOCKED §7.0` (IMMUTABLE)
- **Functions Cut ("ไม่รองรับ" 14 รายการ):** `05_RULES §5.9` (ตรงกับ BRD §14.6.3)
