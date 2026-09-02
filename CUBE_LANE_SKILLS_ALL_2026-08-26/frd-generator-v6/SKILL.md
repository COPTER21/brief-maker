---
name: frd-generator-v6
description: >
  สร้าง FRD มาตรฐาน 2BSimple v6 — Pack Mode แยกไฟล์ตาม layer (UI/API/LOGIC/DB/Rules/Tests)
  ตาม CUBIC 3-layer + Logic Placement Matrix + R8 traceability + R10 Data Classification
  ★ v6.1 HTML-first: รับ HTML (ผ่าน ux/coverage gate) เป็น input ร่วม — Phase 1.5 เปลี่ยนจาก
  "ตัดสิน layout" เป็น "สกัด+ตรวจ+บันทึก pattern จากหน้าจอจริง" + Sync Read → html-generator-v9
  (CI/iron rules/microcopy ห้าม hardcode) + Lane Mode (no-ask probing) + Phase 3.5 Section M
  ตรวจ HTML alignment ★ Scope Lock R11 · Value Stream R12 · Coverage Manifest R13
  ใช้เมื่อ user พูดถึง "สร้าง FRD", "เขียน FRD", "frd-generator", "FRD v6", "FRD pack",
  "FRD จาก BRD", "frd-generator-v6", "SOW3.3"
  Input: BRD v2.2 APPROVED + HTML จาก html-generator-v9 (แนะนำ) + Security Bible
  Output: FRD_F-XX_Pack/ 6-9 ไฟล์ (LEAN/STANDARD/FULL) · Chain: BRD → FRD → TC
  Version pin: cube-master-knowledge/knowledge/04_skills/workflow-master-wf01-06.md
---

> **Sync Read (2026-08-25):** ทุกที่ที่อ้าง `html-generator-v9` = html-generator **เวอร์ชันสูงสุดที่ติดตั้ง**
> (`GEN=$(ls -d /mnt/skills/user/html-generator-v* | sort -V | tail -1)`) — ณ วันนี้คือ v9 (Pattern Q/P · B2 v2 · Iron Rules #1–#103)
> ห้าม hardcode CI/จำนวนกฎ/px จาก generator เก่า · FRD = frd-generator-v6 · BRD = brd-generator-full

# FRD Generator v6.1 — Design Authority Edition (HTML-first)

**ตำแหน่งใน workflow:** WF-01 · SOP3 · SOW3.3 (Actor: BA) — เอกสารหัวใจหลักของการพัฒนา
**DoD:** 1) FRD Pack ครบตาม variant  2) Phase 3.5 ผ่านทุก section (A-M)  3) Layout Decision Log ครบทุกหน้า  4) Coverage Manifest ไม่มี requirement หล่น  5) (เมื่อมี HTML) ทุกหน้า/route ตรง HTML เป๊ะ

> **Changelog v6.1 (2026-07-25) — HTML-first:**
> - ⭐ Sync Read ย้าย → **html-generator-v9** (v4 ไม่มีในเครื่องแล้ว) + fallback หา v* สูงสุด
> - ⭐ **ห้าม hardcode CI/จำนวน iron rules/spec ตัวเลข** — ทุกอย่างยึด v6 ปัจจุบันผ่าน Sync Read (CI ปัจจุบัน = Warm Light)
> - ⭐ Phase 1.5 dual mode: มี HTML → **Recognize & Validate** (สกัด pattern จากจอจริง) / ไม่มี → ตัดสินเองแบบเดิม
> - ⭐ Lane Mode (no-ask): Phase 2.5 probing ตอบเองจาก BRD/NODE_BRIEF + tag `AI-DEFAULT` — ห้ามถาม
> - ⭐ Phase 3.5 Section M: HTML Alignment check
> - ⭐ 01_UI ทุกหน้ามี route จริง · 06_TESTS ยึดข้อความจริงบนจอก่อน microcopy กลาง

> **Changelog v6.0 (2026-07-06) — Design Authority Edition** *(การอ้าง v4 ด้านล่างเป็นบริบท ณ ตอนนั้น — ปัจจุบัน superseded โดย v6.1 ให้ยึด html-generator-v9)*:
> - ⭐ **FRD = Design Authority** — Phase 1.5 ใหม่: รับ Screen Inventory หยาบ + UI Signals จาก BRD v2.1 §14.6 → ตัดสิน pattern A-M ของ html-generator-v9 เอง + Layout Decision Log ใน 01_UI §1.0 (บทบาทย้ายมาจาก BRD ตั้งแต่ 2026-07-06)
> - ⭐ **Sync Read → html-generator-v9** — pattern A-M ความหมายใหม่, Drawer v2 920/680, Sidebar 232px, shell-bar ขาว, Placement Contract #46, Stepper #47, microcopy กลาง
> - ⭐ **Scope Lock Inheritance (R11)** — LOCK-XX จาก BRD §3.4 → 07_LOCKED_DECISIONS §7.0 (immutable) + drift check ชั้นที่ 3
> - ⭐ **Value Stream Propagation (R12)** — BRD §12.1 Downstream Impact → 02_API cross-module contract + 03_LOGIC integration + 06_TESTS cross-module cases
> - ⭐ **Coverage Manifest (R13)** — ตาราง BRD §7/§9/§10 → ไฟล์+section ใน pack — กัน requirement หล่นระหว่าง BRD→FRD (Phase 3.5 Section K)
> - ⭐ **Variant fallback จาก BRD** — ไม่มี Brief §3.4 ก็ตัดสิน LEAN/STANDARD/FULL จาก BRD เองได้ (ไม่ถาม user)
> - ⭐ **06_TESTS microcopy-aware** — expected text อ้าง microcopy กลาง (toast/ปุ่ม) ของ html-generator-v9
> - 🔗 Chain sync: BRD v2.1 (upstream) / html-generator-v9 + ai-testcase-md-generator + qa-friendly-html-generator (downstream)
> - ✅ Preserved: 3-layer, Logic Placement Matrix, R8 traceability, R10 Data Classification, Phase 2.5/3.5, no manual gates

> **Changelog v5.1 (2026-05-22):**
> - ⭐ **Data Classification 4-level** — Public / Internal / Confidential / Restricted บังคับทุก column ใน 04_DB §4.2
> - ⭐ **PII flag overlay** — แยกจาก classification (field สามารถมีทั้ง classification + pii_flag)
> - ⭐ **Iron Rule R10** — Data Classification mandatory + verify ใน Phase 3.5
> - ⭐ **04_DB §4.6 ขยาย** — 4-level definition + enforcement mapping (DB/API/UI/Audit) + Policy Center linkage
> - ⭐ **00_OVERVIEW §0.7.1 ใหม่** — Data Classification summary (highest level ที่ feature แตะ)
> - ⭐ **05_RULES §5.7 D-CLASS** — Enforcement summary per feature
> - 🔗 **Policy Center wire** — Restricted fields → Restricted Resources registry; Classification override → Data Classification module (Policy Center)
>
> **Changelog v5.0 (2026-05-18):**
> - 🎯 **03_LOGIC.md = mandatory ทุก variant** — แก้ปัญหา v4 ที่ logic ธรรมดาไปกองใน 02_API
> - 🎯 **03_LOGIC = Functions + Engines** — Functions (logic ทั่วไป, scope-local) + Engines (reusable/CUBIC)
> - 🎯 **Logic Placement Decision Matrix** — ตาราง 8 รูปแบบ ระบุชัดว่า function แบบไหนไปที่ไหน
> - 🎯 **Iron Rule R8** — ทุก mutation API ต้อง trace ไปที่ Function/Engine ใน 03_LOGIC (Phase 3.5 verify)
> - 🎯 **LEAN ไม่ merge** — เลิก `02_API_DB.md` รวม → แยก 02_API + 04_DB ตามเดิม (consistency กับ STANDARD/FULL)
> - 🎯 **LEAN ได้ 03_LOGIC แล้ว** — function ธรรมดามีที่อยู่ ไม่ต้องแอบใน API
> - ✅ **Preserved from v4:** Auto-detect (no manual gates), Security Bible §0.1, Adaptive variant, Phase 2.5 probing, Phase 3.5 mechanical verification
> - 🔄 **File count changed:** v4 (4/6/9) → v5 (6/7/9)

---

## 🎯 Document Chain

```
WF-01 v2 (HTML-first lane — ปัจจุบัน):
RIF v2.1 → html-generator-v9 → [ux gate + coverage gate ผ่าน] → brd-generator-full v2.2
    ↓ BRD v2.2 (§3.4 LOCK · §12.1 Value Stream · §14.6 Screen Inventory สกัดจาก HTML — มี route จริง)
    ↓ + HTML ตัวจริง (เข้าคู่กัน)
frd-generator-v6 ⭐ (this skill — SOW3.3, Design Authority)
    ↓ FRD_F-XX_Pack/ (6-9 files, 01_UI §1.0 = Layout Decision Log)
    └──→ ai-testcase-md-generator + qa-friendly-html-generator (TC) → output-checker M3 → html-ui-brief → DevPack
    Post-lane: vibe HTML → html-to-frd-sync เสมอ

(สาย Bible: module-decomposer-erp → Brief พร้อม §3.4 Generator Hints — ยังใช้ได้ เป็น input เสริม)
(doc-only mode: ไม่มี HTML ก็รันได้ — Phase 1.5 ตัดสิน layout เอง + ระบุใน pack ว่า "layout = FRD-decided รอ HTML")
```

---

## 📥 Input

### Required (2 files)

| # | File | Read for |
|---|---|---|
| 1 | `BRD_F-XX.md` (BRD v2.2 APPROVED — v2.1 ก็รับได้) | **All 18 sections** — primary spec source (รวม §3.4 Scope Lock, §12.1 Value Stream, §14.6 Screen Inventory) |
| 2 | `<feature>.html` (**Recommended — เคสหลัก WF-01 v2**) | หน้าจอ/route/pattern/ข้อความจริง — Phase 1.5 สกัด, 01_UI ผูก route, 06_TESTS ยึดข้อความจอ ⚠️ ต้องผ่าน ux+coverage gate แล้วเท่านั้น |
| 3 | `F-XX_CODE.md` (Brief — **optional**) | §3.4 Generator Hints (ถ้ามี = ชนะเรื่อง variant) — งาน WF-01 ปกติไม่มี Brief ก็รันได้ |

### Lane Mode v2 inputs (feature-lane-runner v2 · S5 · 2026-08-25)
| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `01_PREBRIEF.md` + `01_FUNCTION_CHECKLIST.md` | ledger: **Coverage Manifest §0.12 ต้องมีคอลัมน์ FN-XX** (ทุก FN → ไฟล์/section) · 03_LOGIC ทุก function อ้าง FN · 05_RULES อ้าง BR-XX |
| `03_DOA_BRIEF.md` `03_NTF_BRIEF.md` `03_CSQ_BRIEF.md` `03_DOCCFG_BRIEF.md` `03_PDFDOC/print-spec.md` | Sync Read บังคับ — event/slot/doc_type ใน FRD ⊆ brief · เพิ่มจาก HTML → append ใน brief เดิม · ไม่มี brief แต่ FRD ต้องใช้ = BLOCK |
| `10_<feature>.html` (v9) | Phase 1.5 สกัด pattern — ใช้ชุด **A–Q + B2 v2** ของ html-generator-v9 (Pattern Q: list · wizard 5 steps · view tabs detail/[domain]/pdf/sign/history) |
| `00_LANE_BRIEF.md` | LOCK/มติ id · `[ASSUMED]` list → §7.0 Locked + §OQ |

### Auto-Read (no user action)

| # | File | Read for |
|---|---|---|
| 3 | `/mnt/user-data/uploads/Security_Spec_Bible.md` หรือ skill knowledge | §0.1 Domain Triggers → identify security domains relevant |
| 4 | `/mnt/skills/user/html-generator-v9/SKILL.md` + `knowledge/iron-rules.md` + `knowledge/ci-tokens.md` + `knowledge/microcopy.md` | Layout Library (Pattern A-N) + Iron Rules + CI + microcopy (Sync Read — authoritative) — ถ้า v6 ไม่มี ให้หา `html-generator-v*` เวอร์ชันสูงสุดที่ติดตั้ง แล้ว log ว่าใช้ตัวไหน |
| 5 | `knowledge/conventions.md` | Cross-feature naming + format conventions |
| 6 | `references/cubic-schema-templates.md` | API + Engine entity format |
| 7 | `references/logic-placement-matrix.md` ⭐ NEW | Function vs Engine vs API-internal vs Rule decision |

### Document Chain Check

| สถานการณ์ | Action |
|---|---|
| ขาด BRD APPROVED | STOP — "ต้องมี BRD ที่ผ่าน brd-generator-full status = APPROVED" |
| ขาด Brief | ✅ ปกติ (WF-01) — ใช้ Variant Fallback จาก BRD (ดู Pack Variant Selection) |
| BRD มี §14.6 Screen Inventory (v2.1) | ✅ input มาตรฐาน — เข้า Phase 1.5 Design Authority |
| BRD มี §14.6 Layout Deviation Log (legacy ก่อน 2026-07) | ✅ รับได้ — ใช้ Layout ID เดิมเป็น starting point แล้ว re-validate กับ html-generator-v9 ปัจจุบัน |
| BRD ไม่มี §14.6 เลย | ⚠️ WARN — สร้าง Screen Inventory เองจาก BRD §5 Journey + §6 (log ว่า inferred) ไม่ STOP |
| BRD ไม่มี §3.4 Scope Lock | ⚠️ WARN — งานอาจ standalone; 07_LOCKED §7.0 ระบุ "N/A" |
| BRD status = NEEDS REVISION | STOP — "แก้ BRD ให้ APPROVED ก่อน" |
| มี HTML แนบ (ผ่าน gate) | ✅ เคสหลัก — Phase 1.5 เข้าโหมด Recognize & Validate |
| มี HTML แต่ไม่ยืนยันว่าผ่าน gate | ⚠️ WARN — ใช้ได้แต่ log "HTML unverified" (lane ปกติผ่านมาแล้วเสมอ) |

### Conflict Resolution

| ประเภทข้อมูล | Priority | เหตุผล |
|---|---|---|
| **Pack Variant decision** | Brief §3.4 (ถ้ามี) → fallback BRD-based rules | Generator Hints ชนะเมื่อมี |
| **Layout Template / Pattern (มี HTML)** | **HTML ที่ผ่าน gate = de facto — FRD สกัด+ตรวจ+บันทึก** ⭐ v6.1 | จอจริงผ่าน iron rules มาแล้ว — FRD ห้ามเขียน spec สวนจอ; ถ้า pattern บนจอขัด standard v6 (ไม่ควรเกิด) → flag `⚠️ HTML-STANDARD CONFLICT` ห้ามแก้เงียบ |
| **Layout Template / Pattern (ไม่มี HTML)** | **FRD Phase 1.5 ตัดสินเอง (Design Authority)** | BRD ให้แค่ประเภทหยาบ + signals |
| **Pages list + routes** | BRD v2.2 §14.6 (สกัดจาก HTML — มี route) → ตรวจกับ HTML ตัวจริงอีกชั้น | ห้ามแต่งหน้าเพิ่ม/ตัดหน้า |
| **Scope Lock (LOCK-XX)** | **BRD §3.4 — immutable ห้าม override** ⭐ | สัญญากับลูกค้า |
| **Cross-module contract** | BRD §12.1 Value Stream | Downstream Impact Map |
| **Field design** | BRD §6 | refined ผ่าน enricher |
| **Workflow + COSO** | BRD §5 | Philosophy embedded |
| **Business Rules** | BRD §9 | + ERP enrichment from Brief §6 |
| **Edge Cases** | BRD §10 | refined ผ่าน enricher |
| **Logic placement** | `logic-placement-matrix.md` ⭐ | NEW — single source of truth |
| **Security domains** | Security Bible §0.1 trigger from Brief features | from v4 |
| **SLA/KPI** | BRD §17 | — |

> **🚨 Iron Rule (v6.1):** อำนาจ layout อยู่ที่ FRD — แต่รูปแบบใช้อำนาจต่างตาม input:
> ไม่มี HTML → ตัดสินเอง · มี HTML (ผ่าน gate) → สกัด+ตรวจ+บันทึก — **ห้ามเขียน spec ที่สวนกับจอจริง**
> FRD ห้ามขัด iron rules / CI ของ html-generator-v9 — ขัดเมื่อไหร่ standard ชนะ + log deviation
> **ห้าม hardcode ใน FRD:** ชื่อสี/hex, จำนวน iron rules, ขนาด px ของ shell — ทั้งหมดยึด Sync Read v6 ปัจจุบัน
> (บทเรียน: v6.0 hardcode "Navy + 48 rules" ไว้ พอ v6 เปลี่ยนเป็น Warm Light + 49 rules → spec โกหก dev ทันที)

---

## 📤 Output — Adaptive Pack (v5)

### Pack Variant Selection (auto from Brief §3.4)

```
IF Brief §3.4 Generator Hints มี → ใช้ตามนั้น (authoritative):
  IF complexity == Low AND has-entity == No → LEAN (6 files)
  ELIF complexity == Critical OR has-state == Yes OR multi-engine → FULL (9 + INDEX)
  ELSE → STANDARD (7 files)

ELSE (ไม่มี Brief — งาน WF-01 ปกติ) → Variant Fallback จาก BRD เอง ⭐ v6:
  pages   = จำนวนหน้าใน §14.6 Screen Inventory
  states  = จำนวน state ใน §8 State Diagram
  approval= §5 มี approval step (COSO Approver ≠ System)?
  money   = §9 มี rule เชิงเงิน/คำนวณซับซ้อน?
  Decision:
    IF pages ≤ 2 AND states ≤ 2 AND NOT approval → LEAN
    ELIF states ≥ 4 OR approval AND money OR §9.5 มี Engine Management → FULL
    ELSE → STANDARD
  Log ใน 00_OVERVIEW: "Variant = X (fallback from BRD: pages=N, states=N, approval=Y/N)"
  ★ ไม่ถาม user — one-shot
```

### Variant Structures (v5 — 03_LOGIC mandatory)

#### 📋 LEAN Pack (6 files) — Simple features
```
FRD_F-XX_Pack/
├── 00_OVERVIEW.md         Document Control + Scope + Roles
├── 01_UI.md               Pages + Components + simple Journey
├── 02_API.md              APIs (HTTP layer, thin)
├── 03_LOGIC.md ⭐ NEW     Functions (scope-local) — Engines section empty/omitted
├── 04_DB.md               Tables + Fields
└── 06_TESTS.md            Acceptance + DoD
```
**ใหม่ v5:** LEAN มี 03_LOGIC แล้ว — function `createXxx`, `updateXxx`, `formatXxx` มีที่อยู่ชัดเจน
Examples: Dashboard with create-record action, simple search with filters, view-edit page

#### 📋 STANDARD Pack (7 files) — Medium features
```
FRD_F-XX_Pack/
├── 00_OVERVIEW.md
├── 01_UI.md
├── 02_API.md              APIs (HTTP layer only)
├── 03_LOGIC.md ⭐         Functions + Engines (≤ 2 engines OK ที่นี่)
├── 04_DB.md               DB tables
├── 05_RULES.md            Business Rules + Edge Cases
└── 06_TESTS.md
```
Examples: CRUD with simple workflow, list+detail+edit pattern, basic approval

#### 📋 FULL Pack (9 files + INDEX) — Complex features
```
FRD_F-XX_Pack/
├── 00_OVERVIEW.md         Document Control + Scope + Dependencies
├── 01_UI.md               Pages + Components + Journey + Layout IDs
├── 02_API.md              API contracts (CUBIC API schema)
├── 03_LOGIC.md ⭐         Functions + Engines (CUBIC Engine schema, 3+ engines)
├── 04_DB.md               Tables + Fields + Relationships + Indexes
├── 05_RULES.md            Business Rules + Validation + Edge Cases + Errors
├── 06_TESTS.md            Acceptance + DoD + WebSocket events
├── 07_LOCKED_DECISIONS.md LD-NN + Convention deviations
└── INDEX.md               Cross-reference + Function Trace + Quick Nav
```
Examples: Payroll, multi-step approval workflow, complex calculation feature

---

## 🆕 03_LOGIC.md Structure (v5 NEW)

ทุก variant ต้องมี — ขนาดต่างกันตามจำนวน logic

### Template

```markdown
# 03_LOGIC — F-XX [Feature Name]

> Audience: BE dev (business logic layer)
> Scope: All non-HTTP logic — pure functions, state transitions, calculations, validations, integrations

---

## §3.1 Functions (Scope-Local)

> Logic ที่ใช้ใน feature นี้เท่านั้น ไม่ register CUBIC
> Format: lightweight — name + purpose + input/output + invoked-by

### F-XX-FN-01: createPayrollRecord
- **Purpose:** สร้าง payroll record ใหม่จาก employee + period
- **Input:** `{ employeeId, periodId, baseSalary }`
- **Output:** `PayrollRecord | ValidationError[]`
- **Invoked by:** `F-XX-API-02 POST /payrolls`
- **Calls:** F-XX-FN-03 (validate), ENG-005 (calculate)
- **Side effects:** INSERT T_payroll, audit log
- **Iron rule check:** ✅ no HTTP terms

### F-XX-FN-02: ...

---

## §3.2 Engines (Reusable / CUBIC-Registered)

> ใช้ข้าม feature 2+ ตัว หรือ logic เชิงคำนวณซับซ้อน → register CUBIC Registry
> Format: CUBIC Engine Entity schema

### ENG-005: payroll-calculation-engine (NEW)
- **id:** (assigned at registration)
- **code:** `payroll-calculation-engine`
- **name:** Payroll Calculation Engine
- **category:** financial-calculation
- **input schema:** `{ baseSalary, deductions[], bonuses[], taxRules }`
- **output schema:** `{ gross, netPay, breakdown[] }`
- **logic outline:**
  1. Sum bonuses → grossAdjustments
  2. Apply tax rules sequentially (FIFO)
  3. Subtract deductions
  4. Return breakdown
- **Used by features:** F-04 (Payroll), F-XX (planned)
- **Iron rule check:** ✅ pure, no HTTP, reusable

### ENG-006: ...

---

## §3.3 API ↔ Logic Trace Table (Phase 3.5 Anchor)

| API | Calls Functions | Calls Engines |
|---|---|---|
| F-XX-API-01 GET /payrolls | F-XX-FN-04 (filter) | — |
| F-XX-API-02 POST /payrolls | F-XX-FN-01, F-XX-FN-03 | ENG-005 |
| F-XX-API-03 PUT /payrolls/:id | F-XX-FN-05 | ENG-005 |

> **Iron Rule R8 check:** ทุก mutation API ต้องมี ≥ 1 Function/Engine ใน column นี้
```

### LEAN variant — Functions only
```markdown
## §3.1 Functions (Scope-Local)
[3-5 functions]

## §3.2 Engines
> ไม่มี engine ใน LEAN feature นี้
> (ถ้ามี logic ที่ reusable ในอนาคต → upgrade เป็น STANDARD/FULL)

## §3.3 API ↔ Logic Trace Table
[mandatory แม้ LEAN]
```

---

## 🎯 Logic Placement Decision Matrix (v5 CORE)

> **ใช้ matrix นี้ทุกครั้งที่ตัดสินใจ "logic ตัวนี้ไปที่ไหน"**

| # | Logic Pattern | ที่อยู่ | เหตุผล |
|---|---|---|---|
| 1 | HTTP routing, request parsing, response shaping | **02_API.md** (internal) | HTTP layer ไม่ใช่ business logic |
| 2 | Field-level validation < 5 lines (`required`, `format`) | **02_API.md** (Request Validation block) | trivial, no reuse |
| 3 | **Function สร้าง/อัปเดต record ธรรมดา** (createX, updateX) | **03_LOGIC.md §3.1 Functions** ⭐ | scope-local, ไม่ reuse แต่ไม่ใช่ HTTP |
| 4 | Format / transform helper (formatCurrency, parseDate) | **03_LOGIC.md §3.1 Functions** | scope-local utility |
| 5 | Validation รวมศูนย์ ใช้ข้าม API หลายตัวใน feature เดียว | **03_LOGIC.md §3.1 Functions** | reuse within feature |
| 6 | Pure calculation (no HTTP, no DB I/O direct) | **03_LOGIC.md §3.2 Engines** | testable, often reusable |
| 7 | Reusable ข้าม feature 2+ ตัว | **03_LOGIC.md §3.2 Engines** | CUBIC register candidate |
| 8 | External integration (3rd party API, payment gateway) | **03_LOGIC.md §3.2 Engines** (wrap by API) | hide complexity |
| 9 | State transition rule (status A → B allowed when X) | **05_RULES.md** + **03_LOGIC.md §3.1** trigger | rule declarative, trigger procedural |
| 10 | Business rule constant / threshold (max_amount, OT_rate) | **05_RULES.md** | declarative, easy to audit |

### Tie-breakers
- **Function vs Engine:** ถ้าตอบ "ใช่" ≥ 2 ใน 3 ข้อนี้ → Engine ไม่ใช่ Function:
  1. Pure (no I/O direct)?
  2. Reusable 2+ features?
  3. Logic > 20 lines / มี algorithm ชัด?
- **API-internal vs Function:** ถ้า logic > 5 lines หรือถูกเรียก 2+ ที่ → Function

> **อ้างอิงเต็ม:** `references/logic-placement-matrix.md`

---

## 🎯 Decision Rules (Master)

### Pack Variant
| Brief §3.4 says (ถ้าไม่มี Brief → ใช้ Variant Fallback จาก BRD — ดู Pack Variant Selection) | → Variant |
|---|---|
| complexity=Low + has-entity=No | LEAN |
| complexity=Medium + has-entity=Yes + ≤ 3 APIs | STANDARD |
| complexity=Critical OR has-state OR multi-engine (3+) | FULL |

### ID Strategy (Hybrid)
- **Scope-local IDs:** `F-XX-API-01`, `F-XX-FN-01`, `F-XX-ENG-01` หรือ `ENG-NNN` (global candidate)
- **Readable label:** "Create Payroll Record", "Payroll Calculation Engine"
- **Note in 07_LOCKED:** "Global Engine IDs to be assigned at CUBIC Registry registration"

### Phase Preserve from v4.0
| Phase | v5 Status |
|---|---|
| Phase 0 Auto-detect | ✅ KEEP |
| Phase 1 Sync Read | ✅ KEEP + read logic-placement-matrix |
| Phase 2.5 Edge Case Probing | ✅ KEEP |
| Phase 3.5 Mechanical Verification | ✅ KEEP + R8 check |
| Phase 4 Deliver | ✅ KEEP |

---

## 📐 Workflow

### Phase 0 — Auto-Detect (No Manual Gates)

**Skill ทำเอง — ไม่ถาม user:**

1. Read BRD ทั้งฉบับ — §3.4 Scope Lock, §12.1 Value Stream, §14.6 Screen Inventory + UI Signals
2. Read Brief §3.4 Generator Hints (ถ้ามี)
3. Decide Pack Variant — Brief ก่อน, ไม่มีก็ fallback จาก BRD (ดูตารางบน) — **ไม่ถาม user**
4. Decide ERP vs General — จาก BRD; ไม่ระบุ → default ERP (บริบท CUBE) + log assumption

**ONE-SHOT: ไม่มีคำถามกลางทาง** — ทุกความไม่ชัดตัดด้วย default + log ใน 00_OVERVIEW Open Questions

---

### Phase 1 — Read + Plan

**1.1 Sync Read (Sequential, mandatory):**

```
1. view {brd_path}/BRD_F-XX.md                         (primary)
2. view {brief_path}/F-XX_CODE.md                       (ถ้ามี)
3. view /mnt/skills/user/html-generator-v9/SKILL.md     (Design Authority Sync Read ⭐)
   + view /mnt/skills/user/html-generator-v9/knowledge/iron-rules.md
   + view /mnt/skills/user/html-generator-v9/knowledge/ci-tokens.md
   (ถ้า v6 ไม่มี → หา html-generator-v* เวอร์ชันสูงสุด + log)
   → extract: pattern list A-M + ความหมาย, Placement Cheat Sheet (#46), Stepper (#47),
     Landing variants (#48), Drawer v2 920/.standard 680, Sidebar 232px + shell-bar ขาว 52px,
     microcopy กลาง (knowledge/microcopy.md ของ v4 — สำหรับ 06_TESTS expected text)
4. view knowledge/conventions.md
5. view references/logic-placement-matrix.md
6. view references/cubic-schema-templates.md (if FULL — has Engines)
```
> **ห้าม hardcode pattern ใน skill นี้** — ความหมาย A-N อ่านสดจาก html-generator-v9 ทุก session
> (v4 อัพเรื่อย ๆ — Sync Read คือกลไกกัน FRD สั่งของเก่า)

**1.2 Security Bible Application:** (เหมือน v4)

**1.3 Mental Map — Enhanced:**
- Pages count + layouts (from BRD §14.6)
- APIs needed (HTTP layer)
- **Functions needed (apply Logic Placement Matrix items #3-5)** ⭐ NEW
- **Engines needed (apply Logic Placement Matrix items #6-8)** ⭐ NEW
- DB tables (from BRD §6)
- Cross-file dependencies

---

### Phase 1.5 — Design Authority: Layout Decision ⭐ v6.1 (dual mode)

**Input:** BRD §14.6 Screen Inventory + UI Signals + §5 Journey **+ HTML ตัวจริง (ถ้ามี)**
**Output:** Layout Decision Log → เขียนลง **01_UI §1.0** (ทุกหน้า ทุก decision มีเหตุผล)

**Mode A — มี HTML (เคสหลัก WF-01 v2): Recognize & Validate**
1. ไล่ทุก route ใน HTML → ระบุว่าแต่ละหน้าใช้ pattern อะไร (เทียบ Layout Library v6 จาก Sync Read)
2. ตรวจ: pattern ที่จอใช้ compliant กับ v6 มั้ย (ปกติผ่าน — เพราะผ่าน ux gate มาแล้ว)
3. บันทึกลง Decision Log: `Pattern (observed)` + evidence (route + selector หลัก)
4. **ห้าม**ตัดสิน pattern ใหม่ที่ต่างจากจอ — เจอจุดที่คิดว่าควรเป็น pattern อื่น → Open Question ไม่ใช่แก้ spec
5. หน้าใน HTML ที่ BRD ไม่มี หรือกลับกัน → `⚠️ HTML-BRD DRIFT` (ไม่ควรเกิด — BRD v2.2 สกัดจาก HTML เดียวกัน ถ้าเกิด = มีอะไรผิดต้นน้ำ)

**Mode B — ไม่มี HTML (doc-only): ตัดสินเองแบบเดิม** ใช้ตาราง map ด้านล่าง + ระบุใน 00_OVERVIEW ว่า "layout = FRD-decided (no HTML) — รอ HTML ยืนยัน"

**1.5.1 Map ประเภทหยาบ → Pattern (Mode B — ตารางนี้คือ default, ความหมายจริงยึด v6 ปัจจุบันจาก Sync Read):**

| ประเภทหยาบจาก BRD | Pattern v6 | หมายเหตุ |
|---|---|---|
| หน้ารายการ | A (list-view) | >8 cols → drawer ตาม Rule #40 |
| ฟอร์มสร้าง/แก้ไข (ขั้นเดียว) | B (create/edit drawer v2 920px) | .standard 680 ถ้า ≤6 fields |
| ฟอร์มสร้าง (หลายขั้น) | B + Stepper #47 (2-5 steps, สุดท้าย "ตรวจสอบและยืนยัน") | |
| หน้ารายละเอียด (generic) | C (view drawer tabbed) | |
| หน้ารายละเอียด + **Doc/Transaction signal** (approver+พิมพ์+ลายเซ็น) | **G+H+I ครบชุด** | ห้ามใช้ C generic |
| หน้ายืนยัน | D (modal 440px) | |
| dashboard | J (J1 KPI / J2 Chart / J3 Mixed) | |
| รายงาน (ดู+พิมพ์) | K (+print CSS) | |
| card grid / kanban / timeline | L | ต้องมี toggle กลับ list |
| หน้าแรก / landing | M (M1/M2/M3 เท่านั้น) | |
| shell หลายโมดูล / sidebar 3 ระดับ | N (sidebar-nav-shell + icon rail) | v6 ใหม่ — ยึด spec จาก Sync Read |

**1.5.2 กติกาตัดสิน:**
- **CI Lock:** palette/tokens = **ตามที่ html-generator-v9 ประกาศใน Sync Read เท่านั้น** (ปัจจุบัน Warm Light — แต่ห้ามจำค่า ให้อ่านสด) — BRD/RIF ขอสีนอก token → ปฏิเสธ + Open Question
- **Iron Rules ของ v6 ชนะเสมอ** (จำนวน/เนื้อหายึด `knowledge/iron-rules.md` ปัจจุบัน) — function ที่ standard ไม่รองรับ → ตัด + log "Functions Cut" (flow หลักต้องครบ)
- **NON-STANDARD signal จาก BRD** → เคารพ + ระบุใน Layout Decision Log ว่า "NON-STANDARD (stakeholder approved per OQ-XX)" — ถ้ายังไม่มี approval → ใช้ standard ไปก่อน + OQ
- **ERP Shell:** ทุกหน้า ERP ระบุ Sidebar Active + Breadcrumb — spec ขนาด/สี ยึด Pattern N + shell spec ของ v6 (Sync Read — ห้าม hardcode px)

**1.5.3 Layout Decision Log (ลง 01_UI §1.0):**

| Page | route | BRD บอก (หยาบ) | Pattern (observed จาก HTML / decided ถ้า doc-only) | เหตุผล/evidence | Deviation/Functions Cut |
|---|---|---|---|---|---|
| P-01 | `#/pr-list` | หน้ารายการ | A (observed) | table หลัก + drawer filter | — |
| P-03 | `#/pr/:id` | รายละเอียด + Doc signal | G+H+I (observed) | approver+PDF+ลายเซ็นบนจอจริง | — |

---

### Phase 2 — Write Pack Files

**Order:** 00 → 01 → 04 → 02 → **03 (LOGIC)** → 05 → 06 → 07 → INDEX

(ลำดับใหม่: เขียน 02_API เสร็จแล้วเขียน 03_LOGIC ทันที เพื่อ trace API → Logic ครบ)

**Per-file:** อ่าน template ที่ตรงกัน + fill ตาม BRD + Brief + Matrix

**v6.1 additions ระหว่างเขียน:**
- **01_UI:** ทุกหน้าใน §1.0 + Pages ต้องมี `route` จริง (จาก HTML — dev ผูก hash routing ตรงนี้) · doc-only → "route: TBD"

- **07_LOCKED §7.0:** import LOCK-XX จาก BRD §3.4 ทั้งชุด (immutable) — spec ใดขัด LOCK → LOCK ชนะ + log
- **02_API:** เพิ่ม section Cross-Module Contract จาก BRD §12.1 (endpoint/event ที่ downstream ต้องใช้ เช่น PR approved → budget commit event)
- **03_LOGIC:** integration กับ downstream (จาก §12.1) เป็น Function/Engine ตาม matrix #8
- **06_TESTS:** (1) expected text: **มี HTML → ยึดข้อความจริงบนจอ (verbatim) เป็นอันดับแรก** แล้วค่อย fallback microcopy กลาง v6 (`html-generator-v9/knowledge/microcopy.md`) — ห้ามเดาคำเอง (2) Cross-Module Test Cases (§6.9) จาก §12.1 ("ยกเลิก PR → budget release จริง")
- **00_OVERVIEW §0.12 Coverage Manifest ⭐:** ตาราง requirement ทุกข้อจาก BRD →ที่อยู่ใน pack:
  | BRD Ref | Requirement | อยู่ที่ (file §) |
  |---|---|---|
  | §7 S-01 | สร้าง QT | 01_UI P-02 + 02_API-02 + 03_FN-01 + 06_TESTS AT-01 |
  | §9 R-04 | ส่วนลด ≤30% | 05_RULES BR-04 + 06 AT-07 |
  | §10 E-03 | tier=null | 05_RULES EC-03 |
  ทุก story/rule/edge จาก BRD ต้องมีแถว — ไม่มีที่ลง = ใส่ Open Question ห้ามหายเงียบ

```
view templates/00_overview.template.md
view templates/01_ui.template.md
view templates/04_db.template.md
view templates/02_api.template.md
view templates/03_logic.template.md ⭐ NEW (Functions + Engines + Trace Table)
view templates/05_rules.template.md
view templates/06_tests.template.md
view templates/07_locked_decisions.template.md (STANDARD/FULL)
view templates/INDEX.template.md (FULL only)
```

---

### Phase 2.5 — Edge Case Probing (v6.1 — dual mode)

Trigger Matrix + PR-1..PR-9 ตาม `references/edge-case-probes.md`

**Interactive mode:** ถาม user ตาม probe (เหมือนเดิม)
**Lane Mode (รันใต้ feature-lane-runner / user สั่ง one-shot):** **ห้ามถาม** — ตอบ probe เองตามลำดับ:
1. หาคำตอบใน BRD §10 Edge Cases / §9 Rules
2. หาใน NODE_BRIEF + GOLDEN_RULES ของ node (ถ้าแนบมา)
3. ไม่เจอ → ใช้ **conservative default** ของ probe นั้น (เช่น PR-1 → optimistic lock 409, PR-7 → idempotency key required)
   + tag rule นั้นใน 05_RULES ว่า `[AI-DEFAULT]` + เพิ่ม Open Question ให้ BA confirm ตอน review
4. log ทุก probe ที่ใช้ default ลง 00_OVERVIEW

> เหตุผล: default เชิง conservative ทำให้ dev ได้ spec ที่ปลอดภัยเสมอ (ล็อกไว้ก่อน ดีกว่าปล่อย race)
> และ `[AI-DEFAULT]` ทำให้คนตามเก็บได้ทีหลังโดยไม่ต้องขุดว่า AI ตัดสินใจแทนตรงไหน

Apply answers → 02_API / 03_LOGIC / 05_RULES / 07_LOCKED_DECISIONS

---

### Phase 3.5 — Mechanical Verification (Enhanced with R8)

**Write report ใน chat:**

```markdown
## 🔍 Phase 3.5 Verification Report — FRD F-XX

### A. Pack Completeness
- [ ] Variant decision match Brief §3.4 ✅/❌
- [ ] All expected files generated ([6/7/9] files) ✅/❌
- [ ] 03_LOGIC.md exists (mandatory all variants) ✅/❌ ⭐ NEW
- [ ] INDEX.md (if FULL) cross-references all files ✅/❌

### B. Function/API Coverage
From 02_API.md — mutation APIs:
- [API-01] [name] → Contract complete ✅/❌

### C. R8 Logic Traceability ⭐ NEW
From 03_LOGIC §3.3 Trace Table:
- [ ] ทุก mutation API มี ≥ 1 Function/Engine in trace ✅/❌
- [ ] ทุก Function listed in §3.1 ถูก trace อย่างน้อย 1 API ✅/❌
- [ ] Engine ที่ listed in §3.2 ถูก trace ผ่าน Function หรือ direct API ✅/❌
- [ ] ไม่มี orphan Function/Engine (ไม่ถูกใช้) ✅/❌

### D. API ↔ DB Linkage
- [API-01] reads/writes table: [T_xxx] → exists in 04_DB.md ✅/❌

### E. UI ↔ API Cross-reference
- P-01 action "Submit" → calls [API-01] → exists in 02_API.md ✅/❌

### F. Engine Iron Rules (CUBIC 3-layer) — apply to 03_LOGIC §3.2
- [ ] No Engine references HTTP terms (req/res/header) ✅/❌
- [ ] All Engine input/output = pure objects ✅/❌
- [ ] Feature doesn't bypass API to call Engine ✅/❌

### G. Logic Placement Compliance ⭐ NEW
- [ ] ไม่มี "createX/updateX function" แอบใน 02_API (ต้องอยู่ใน 03_LOGIC §3.1) ✅/❌
- [ ] ไม่มี "pure calculation" แอบใน 02_API (ต้องอยู่ใน 03_LOGIC §3.2) ✅/❌
- [ ] ทุก logic ที่ matrix #3-8 อยู่ใน 03_LOGIC จริง ✅/❌

### H. Security Bible Application
- [ ] All Bible triggers identified → relevant domains applied ✅/❌

### I. Convention Compliance
- API path format ✅/❌
- field_key = snake_case ✅/❌
- Function code = camelCase ✅/❌ ⭐ NEW
- Engine code = kebab-case ✅/❌
- Error code = UPPER_SNAKE ✅/❌

### J. Data Classification (R10 — v5.1) ⭐ NEW
- [ ] ทุก column ใน 04_DB §4.2 มี `Classification` (Public/Internal/Confidential/Restricted) ✅/❌
- [ ] ทุก column ใน 04_DB §4.2 มี `PII` flag ✅/❌
- [ ] 04_DB §4.5 Field Dictionary มี `Classification` column ✅/❌
- [ ] 04_DB §4.6 ครบ 6 subsections (.1-.6) ✅/❌
- [ ] 00_OVERVIEW §0.7.1 ระบุ highest level ที่ feature แตะ ✅/❌
- [ ] 05_RULES §5.7 มี subsection D-CLASS ✅/❌
- [ ] ไม่มี default = Public (ตรวจหา Public ที่ไม่ใช่ field public-facing จริง) ✅/❌
- [ ] Restricted fields → flag ใน 00_OVERVIEW Open Questions (wire Restricted Resources) ✅/❌

### K. Coverage Manifest (R13 — v6) ⭐
- [ ] ทุก Story ใน BRD §7 มีแถวใน 00_OVERVIEW §0.12 ✅/❌
- [ ] ทุก Rule ใน BRD §9 มีแถว (ชี้ 05_RULES + test) ✅/❌
- [ ] ทุก Edge ใน BRD §10 (☑ confirmed) มีแถว ✅/❌
- [ ] ไม่มีแถวที่ "อยู่ที่" ว่าง — ของที่ไม่มีที่ลง อยู่ใน Open Questions ✅/❌

### L. Scope Lock + Value Stream (R11/R12 — v6) ⭐
- [ ] Scope Lock imported ครบตาม BRD §3.4 (FULL: 07 §7.0 / อื่น: 00 §0.11) หรือ "N/A — standalone" ✅/❌
- [ ] ไม่มี spec ใดใน pack ขัด LOCK ✅/❌
- [ ] 02_API มี Cross-Module Contract ครบตาม BRD §12.1 downstream ✅/❌
- [ ] 06_TESTS มี cross-module case อย่างน้อย 1 ต่อ downstream ที่มี data ไหล ✅/❌

### M. HTML Alignment (v6.1 — เมื่อมี HTML) ⭐
- [ ] จำนวนหน้าใน 01_UI = จำนวนหน้าใน HTML เป๊ะ (ไม่มี invented/missing page)
- [ ] ทุก route ใน 01_UI มีจริงใน HTML
- [ ] ทุก Pattern (observed) ใน Decision Log ตรงกับที่จอใช้จริง (spot-check ≥3 หน้า พร้อม evidence)
- [ ] 06_TESTS expected text ที่อ้างจอ — ตรง verbatim (spot-check ≥5 ข้อความ)
- [ ] doc-only mode → mark section นี้ "N/A — no HTML" (ห้ามติ๊กผ่านเฉย ๆ)

### Verdict
✅ All checks passed → deliver Pack
❌ Found issues at [section] → fix before deliver
```

---

### Phase 4 — Deliver + Next Steps

1. Save files ที่ `/mnt/user-data/outputs/FRD_F-XX_Pack/`
2. Present ผ่าน `present_files`
3. Show next steps:

```
FRD Pack พร้อมแล้ว — Chain ถัดไป (WF-01 SOP3):

🎨 HTML มีอยู่แล้วในเลน (HTML-first) — ถ้าต้อง regen/patch ใช้ html-generator-v9 (อ่าน 01_UI.md — Layout Decision Log §1.0 คือคำสั่ง)
📋 SOW3.5 Testcase → ai-testcase-md-generator + qa-friendly-html-generator (อ่าน 05+06+02+03)
📦 SOW3.6 Final Pack → uba-taxonomy-register + output-checker + dev-brief-generator
📦 Dev Handover:
   - 01_UI.md  → FE dev
   - 02_API.md → BE dev (HTTP layer)
   - 03_LOGIC.md ⭐ → BE dev (business logic — Functions + Engines)
   - 04_DB.md → DBA / BE dev
   - 05_RULES.md → BE dev + QA
   - 06_TESTS.md → QA
   - 07_LOCKED_DECISIONS.md → all
```

---

## 🚨 Critical Rules (v5 — R8 NEW)

### R1: ห้ามเดาข้อมูล
ถ้า BRD ไม่มี → ใส่ใน 00_OVERVIEW Open Questions

### R2: Design Authority ที่นี่ (v6.1 — dual mode)
- อำนาจ layout อยู่ที่ Phase 1.5 — มี HTML: สกัด+ตรวจ+บันทึก (ห้ามสวนจอ) / ไม่มี: ตัดสินเอง
- ทุกหน้า ต้องมีแถวใน 01_UI §1.0 Layout Decision Log (route + pattern + เหตุผล + deviation)
- ห้ามขัด iron rules / CI ของ html-generator-v9 (Sync Read) — standard ชนะ + log Functions Cut
- **ห้าม hardcode สี/จำนวน rules/px** — ยึด Sync Read เสมอ

### R3: CUBIC Schema Compliance
02_API.md ตาม CUBIC API Entity / 03_LOGIC.md §3.2 ตาม CUBIC Engine Entity

### R4: ID Convention
- Scope-local: `F-XX-API-01`, `F-XX-FN-01`, `ENG-NNN`
- Field key: snake_case
- **Function code: camelCase (createPayrollRecord)** ⭐ NEW
- Engine code: kebab-case (payroll-calculation-engine)
- Error code: UPPER_SNAKE_CASE
- Status: snake_case past tense

### R5: Pack Variant Discipline
ห้ามผสม variants — เลือก 1 variant ต่อ FRD

### R6: Security Bible Mandatory
Apply §0.1 Domain Triggers ทุกครั้ง

### R7: Mechanical Verification Mandatory
Phase 3.5 รันทุก FRD ก่อน deliver

### R8: Logic Traceability (NEW v5) ⭐
- ทุก mutation API ต้อง trace ไปที่ ≥ 1 Function/Engine ใน 03_LOGIC §3.3
- ห้ามมี orphan Function/Engine (declared แต่ไม่ถูกเรียก)
- ห้ามมี "hidden logic" ใน 02_API ที่ matrix บอกว่าควรอยู่ 03_LOGIC
- Verify ใน Phase 3.5 Section C + G

### R9: 03_LOGIC Mandatory (NEW v5) ⭐
- ทุก variant ต้องมี 03_LOGIC.md
- LEAN ที่มีแค่ read action → 03_LOGIC ขั้นต่ำ 1 Function (เช่น `buildDashboardQuery`)
- ถ้า feature ไม่มี logic จริง ๆ (pure display ดึง field ตรง) → flag ใน 00_OVERVIEW ว่า "no custom logic" + 03_LOGIC mark "N/A — pure display feature"

### R10: Data Classification Mandatory (NEW v5.1) ⭐
- ทุก column ใน 04_DB §4.2 ต้องมี `Classification` column (Public / Internal / Confidential / Restricted)
- ทุก field ใน 04_DB §4.5 Field Dictionary ต้องมี `Classification`
- Default = Internal ถ้าไม่ระบุ (ห้าม default Public)
- 04_DB §4.6 ต้องครอบคลุม 4-level definition + enforcement mapping
- 00_OVERVIEW §0.7.1 ต้องสรุประดับสูงสุดที่ feature แตะ
- 05_RULES §5.7 ต้องมี subsection D-CLASS อธิบาย enforcement
- Field ที่ classification = Restricted → ต้องระบุใน 00_OVERVIEW Open Questions ว่า wire กับ Restricted Resources registry หรือยัง
- Verify ใน Phase 3.5

### R11: Scope Lock Inheritance (NEW v6) ⭐
- LOCK-XX จาก BRD §3.4 → FULL: 07_LOCKED §7.0 / LEAN·STANDARD: 00_OVERVIEW §0.11 — ครบทุกข้อ, immutable ตลอด pack
- spec ขัด LOCK → LOCK ชนะ + รายงาน; scope ใหม่เกิน LOCK ที่โผล่ระหว่างเขียน FRD → Open Question (drift ชั้นที่ 3)

### R12: Value Stream Propagation (NEW v6) ⭐
- BRD §12.1 Downstream Impact ทุกแถวที่มี data ไหล → ต้องมี (a) contract ใน 02_API หรือ event, (b) logic ใน 03_LOGIC ถ้ามีการแปลง, (c) test ใน 06_TESTS §6.9 + contract ใน 02_API §2.X
- ยกเลิก/แก้กลางทาง (คอลัมน์สุดท้ายของ Impact Map) → ต้องมี edge case + test

### R13: Coverage Manifest Mandatory (NEW v6) ⭐
- 00_OVERVIEW §0.12 ครบทุก story/rule/edge จาก BRD — Phase 3.5 Section K ตรวจ
- requirement ที่ไม่มีที่ลง = Open Question ห้ามหายเงียบ

### R14: HTML Fidelity (NEW v6.1) ⭐
- เมื่อมี HTML: FRD ต้อง 1:1 กับจอจริง — หน้า/route/pattern/ข้อความ expected ห้ามต่างจาก HTML
- อยากเปลี่ยนอะไรบนจอ → Open Question / ส่งเข้า html-to-frd-sync — **ห้ามแก้ผ่าน FRD เงียบ ๆ**
- Phase 3.5 Section M ตรวจ · เหตุผล: FRD ที่ขัด prototype = บัคที่ dev สร้างตามคำสั่งเอกสาร

---

## 📋 Output Validation Checklist (v5)

### Pack Structure
- [ ] Variant ตรงกับ Brief §3.4 (LEAN 6 / STANDARD 7 / FULL 9+INDEX)
- [ ] **03_LOGIC.md exists ทุก variant** ⭐
- [ ] ไฟล์ที่ variant กำหนดสร้างครบ
- [ ] INDEX.md (FULL only) มี cross-reference + Function Trace

### Per-File Quality
- [ ] 00_OVERVIEW: Document Control + Scope + Roles + Dependencies + Open Questions
- [ ] 01_UI: §1.0 Layout Decision Log ครบทุกหน้า + Pages + Components + Journey
- [ ] 02_API: ทุก endpoint Contract Block ครบ (HTTP layer only)
- [ ] **03_LOGIC §3.1:** ทุก Function มี Purpose + Input + Output + Invoked-by + Side effects ⭐
- [ ] **03_LOGIC §3.2:** ทุก Engine มี CUBIC Entity ครบ (FULL/STANDARD with engines) ⭐
- [ ] **03_LOGIC §3.3:** Trace table ครบทุก mutation API ⭐
- [ ] 04_DB: Tables + Field Dictionary + Relationships + Indexes
- [ ] 05_RULES: Business Rules + Validation + Edge Cases + Error Catalog
- [ ] 06_TESTS: Acceptance per FR + DoD
- [ ] 07_LOCKED_DECISIONS (STANDARD/FULL): LD-NN + Convention deviations

### Cross-References (Phase 3.5)
- [ ] UI actions → API exists
- [ ] **API → Function/Engine exists in 03_LOGIC §3.3** ⭐
- [ ] API → DB table exists
- [ ] No orphan Function/Engine
- [ ] All triggered Security domains documented

### Logic Placement (Matrix Compliance) ⭐ NEW
- [ ] CRUD function ใน 03_LOGIC §3.1 (ไม่ใช่ 02_API)
- [ ] Pure calculation ใน 03_LOGIC §3.2
- [ ] HTTP-only logic ใน 02_API
- [ ] Declarative rules ใน 05_RULES

### Data Classification (R10 — v5.1) ⭐ NEW
- [ ] 04_DB §4.2 ทุก column มี `Classification` (Public/Internal/Confidential/Restricted)
- [ ] 04_DB §4.2 ทุก column มี `PII` flag (Yes/—)
- [ ] 04_DB §4.5 Field Dictionary มี `Classification` column
- [ ] 04_DB §4.6 อธิบาย 4-level + enforcement mapping
- [ ] 00_OVERVIEW §0.7.1 สรุประดับสูงสุดที่ feature แตะ
- [ ] 05_RULES §5.7 มี subsection D-CLASS
- [ ] ไม่มี default = Public โดยลืม (default = Internal เท่านั้น)
- [ ] Restricted fields flag ใน 00_OVERVIEW Open Questions (wire กับ Restricted Resources)

### v6.1 Additions ⭐
- [ ] (มี HTML) 01_UI ทุกหน้ามี route จริง + Pattern (observed) + Phase 3.5 M ผ่าน
- [ ] Lane Mode: probe ที่ใช้ default ติด `[AI-DEFAULT]` ครบ + log ใน 00_OVERVIEW

### v6 Additions ⭐
- [ ] 00_OVERVIEW §0.12 Coverage Manifest ครบ (ทุก BRD §7/§9/§10 มีแถว)
- [ ] Scope Lock imported ครบ (07 §7.0 หรือ 00 §0.11 ตาม variant) / "N/A — standalone"
- [ ] 02_API Cross-Module Contract ตาม BRD §12.1
- [ ] 06_TESTS ยึดข้อความจริงบนจอ (มี HTML) / microcopy กลาง v6 (doc-only) + มี cross-module cases

### Standards Compliance
- [ ] CUBIC schema: API (02) + Engine (03 §3.2)
- [ ] Iron Rules: Feature→API→Function/Engine (R8 enforced)
- [ ] Engine = pure (no HTTP terms)
- [ ] ID Conventions (camelCase Function, kebab-case Engine)

---

## 📚 Reference Files

| File | Purpose |
|---|---|
| `references/pack-variants.md` | Variant selection decision tree + examples |
| `references/logic-placement-matrix.md` ⭐ NEW | Function vs Engine vs API-internal decision (10 patterns) |
| `references/cubic-schema-templates.md` | API Entity + Engine Entity field-by-field |
| `references/edge-case-probes.md` | PR-1 to PR-9 probing patterns |
| `templates/00_overview.template.md` | Document Control + Scope |
| `templates/01_ui.template.md` | Pages + Components + Journey |
| `templates/02_api.template.md` | CUBIC API Entity (HTTP layer only) |
| `templates/03_logic.template.md` ⭐ NEW | Functions + Engines + Trace Table |
| `templates/04_db.template.md` | Tables + Fields + Relationships |
| `templates/05_rules.template.md` | Rules + Validation + Edge Cases + Errors |
| `templates/06_tests.template.md` | Acceptance + DoD |
| `templates/07_locked_decisions.template.md` | LDs + Convention deviations |
| `templates/INDEX.template.md` | Cross-reference + Function Trace + Quick nav |
| `knowledge/conventions.md` | Cross-feature naming + format rules |
| `examples/frd_v6_lean_walkthrough.md` | F-01 Customer Quick-Add LEAN variant (6 files, no engine) |
| `examples/frd_v6_standard_walkthrough.md` ⭐ NEW | F-02 Product Catalog STANDARD variant (7 files, 1 engine) |
| `examples/frd_v6_full_walkthrough.md` | F-04 Payroll FULL variant (9 + INDEX, 3+ engines) |

---

## 🆚 Comparison: v5.1 → v6.0

| Dimension | v5.1 | v6.0 |
|---|---|---|
| Design Authority | BRD (§14.6 Layout ID) — FRD copy | **FRD Phase 1.5 ตัดสินเอง** ⭐ |
| BRD input | §14.6 Layout Deviation Log (STOP ถ้าไม่มี) | §14.6 Screen Inventory หยาบ (legacy ก็รับได้) |
| Sync Read | html-generator-v9 (ตายแล้ว) | **html-generator-v9 (A-M, Drawer v2, #46-48, microcopy)** |
| Variant без Brief | ถาม user | **fallback จาก BRD — ไม่ถาม** |
| Scope Lock | ❌ | **R11 → 07_LOCKED §7.0** |
| Value Stream | ❌ | **R12 → API/LOGIC/TESTS** |
| Coverage Manifest | ❌ | **R13 + Phase 3.5 K** |
| Test expected text | เดาคำเอง | **microcopy กลาง v4** |

**v6.0 → v6.1 (2026-07-25):** Sync Read → **v6** · HTML-first (Phase 1.5 Recognize & Validate + R14 HTML Fidelity + Phase 3.5 M) · Lane Mode probing (no-ask, `[AI-DEFAULT]`) · ห้าม hardcode CI/rules/px

## 🆚 Comparison: v4.0 → v5.0

| Dimension | v4.0 | v5.0 |
|---|---|---|
| File count | 4 / 6 / 9 | **6 / 7 / 9** |
| 03_LOGIC.md | Only FULL (as 03_ENGINE) | **All variants** ⭐ |
| LEAN structure | 02_API_DB merged | **02_API + 04_DB separate** ⭐ |
| Logic placement | Implicit (engine ≤ 2 merged into 02_API) | **Explicit Matrix (10 patterns)** ⭐ |
| Function vs Engine | Engine only concept | **Function (scope-local) + Engine (reusable)** ⭐ |
| Logic traceability | UI→API verified, API→Logic implicit | **R8: API→Function/Engine trace table mandatory** ⭐ |
| Orphan logic detection | ❌ | **✅ Phase 3.5 Section C** ⭐ |
| Hidden logic in API | ❌ tolerated | **✅ Phase 3.5 Section G blocks** ⭐ |
| CRUD function ที่อยู่ | 02_API "Engine Logic" section | **03_LOGIC §3.1 Functions** ⭐ |
| Manual gates | 0 | 0 (preserved) |
| Security Bible | ✅ §0.1 | ✅ §0.1 (preserved) |
| Phase 2.5/3.5 | ✅ | ✅ + R8 check + Matrix check |

---

## 🎓 Quick Start

```
User: "สร้าง FRD จาก Brief + BRD นี้"
       + แนบ F-04_CB-PAYROLL.md + BRD_F-04.md

Skill:
  Phase 0: Auto-detect
    - Read Brief §3.4 → complexity=Critical, has-state=Yes
    - Decision: FULL variant (9 files + INDEX)

  Phase 1: Read + Plan
    - Sync Read 6 files (including logic-placement-matrix.md)
    - Apply Security Bible §0.1 (financial + PII + admin)
    - Mental map:
      • 7 pages, 8 APIs
      • Functions: ~12 (createX, updateX, formatX, validateX)
      • Engines: 3 (payroll-calc, tax-rule-applier, deduction-validator)
      • 4 tables

  Phase 2: Write Pack (order with 03_LOGIC after 02_API)
    - 00 → 01 → 04 → 02 → 03_LOGIC → 05 → 06 → 07 → INDEX

  Phase 2.5: Edge Case Probing — PR-1, PR-7, PR-9 active

  Phase 3.5: Mechanical Verification
    - Section C: R8 — API → Function/Engine trace check ✅
    - Section G: Logic Placement compliance ✅

  Phase 4: Deliver — present 10 files

Example LEAN:
User: "สร้าง FRD สำหรับ Customer Quick-Add"
  Phase 0: complexity=Low, has-entity=Yes → LEAN (6 files)
  Phase 2 generates:
    - 03_LOGIC §3.1: createCustomerRecord, validateCustomerData (2 functions)
    - 03_LOGIC §3.2: (empty — "no reusable engines")
    - 03_LOGIC §3.3: API-01 POST /customers → createCustomerRecord ✅
```

**Key v5 win:** function `createCustomerRecord` มีที่อยู่ชัด ไม่ต้องแอบใน 02_API
