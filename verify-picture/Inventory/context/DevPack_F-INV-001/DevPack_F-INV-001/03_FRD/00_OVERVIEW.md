# 00_OVERVIEW — F-INV-001 Stock by Location (สต็อกตามตำแหน่ง)

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Open Questions + Coverage Manifest
> **Generator:** frd-generator-v6.1 (HTML-first, Design Authority Edition, Reverse Mode)

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-INV |
| **Feature Name** | Stock by Location (สต็อกตามตำแหน่ง) |
| **Feature Code** | F-INV-001 |
| **Module** | Inventory / Warehouse |
| **Variant** | **FULL** (9 files + INDEX) — see §0.1.1 for the applied decision rule |
| **Status** | DRAFT — awaiting decision on G-01 (costing/valuation scope creep) and OQ-INV-01..05 |
| **FRD Version** | 1.0 (2026-08-10) |
| **Generator** | frd-generator-v6.1 |
| **Source ("BRD" substitute)** | `PREBRIEF_F-INV_Stock-by-Location.md` (101 lines) + `FUNCTION_CHECKLIST_F-INV_Stock-by-Location.md` — see §0.1.2 |
| **Source HTML** | `StockByLocation.html` (3,124 lines, gated — see §0.1.3) |
| **Author** | AI (frd-generator-v6.1), lane run |
| **Reviewers** | Strike / พี่เบิร์ด / ทีมขาย / Policy (named OQ owners — see §0.8) |

### §0.1.0 Sync Read Substitution (logged per skill instruction)

**Sync Read substitution: the calling instruction explicitly directs using `html-generator-v8`
(installed at `.agents/skills/html-generator-v8/`) in place of the skill's own default reference to
`html-generator-v6`, because v8 supersedes v6/v7 and is what actually produced/QC'd this HTML.**

Concretely, the Design Authority Sync Read was performed against:
- `html-generator-v8/knowledge/iron-rules.md` (966 lines, read in full — Rules #1-49 base set +
  Group 18 Rule #94/#94.1 Master Combobox/Cascade Clear + Group 19 Rules #95-#97 Overlay Portal /
  List Full-Height / Responsive Desktop-Base)
- `html-generator-v8/knowledge/ci-tokens.md` (CUBE Warm Light token set — Charcoal/Red/Orange)
- `html-generator-v8/knowledge/microcopy.md` (central microcopy standard — button labels, toasts,
  modal confirm copy, empty states, status pill vocabulary, format rules)

Per R2/v6.1, no CI hex value, iron-rule count, or shell pixel dimension is hardcoded anywhere in
this pack outside of direct quotes from the Sync Read source or verbatim values copied from the
gated HTML itself (e.g. drawer `920px`, adjustment modal `min(1440px, 100vw − 48px)`).

### §0.1.1 Pack Variant Decision (applied honestly against the precedent's rule — not defaulted to FULL)

No Brief `F-INV_CODE.md` §3.4 Generator Hints exists, so the variant is decided by the BRD-fallback
rule, applying the same decision rule used in `DevPack_F-CUST-001/03_FRD/00_OVERVIEW.md §0.1.1`:

```
pages    = 5 route-level surfaces (Gate #/stock · List-by-SKU #/stock/{ctx}/sku ·
           List-by-Location #/stock/{wh}/loc · Break/Pack #/stock/{wh}/bp ·
           Audit Log #/stock/{wh}/log) + 5 drawer modes (product 3-tab · balance 3-tab ·
           location · break/pack · adjustment-log) + 3 modal types (Manual Adjustment wide ·
           Export · Break/Pack create)
states   = Balance status: 4 explicit values (available / damaged / blocked / quarantine —
           `statusLabel()` L1125) · Location status: ≥4 distinct values actually branched in code
           (active / full / blocked / frozen, plus `adjLineError()` L2602 also guards
           inactive/maintenance/decommissioned) · Break/Pack order status: 2 (locked / done)
approval = No real approval/DOA workflow is implemented — OB-8/FN-18 write directly with no
           maker-checker gate. PREBRIEF §6 OQ-INV-01 explicitly flags this as an open question
           ("ควรมี DOA threshold ไหม") rather than a built approval chain — so `approval = No`
           as currently built (see §0.8 OQ-INV-01 for the pending decision)
money    = No formal money/valuation obligation is IN SCOPE per PREBRIEF §1 ("ไม่ทำ: costing
           engine VD-PDM-07") — a valuation display exists in the HTML but is explicitly a
           carried scope-creep gap (§0.1.4 / G-01), not a specified requirement, so it is not
           counted toward this decision

Decision rule: IF pages ≤ 2 AND states ≤ 2 AND NOT approval → LEAN
               ELIF states ≥ 4 OR (approval AND money) OR Engine Management → FULL
               ELSE → STANDARD

Evaluation:  pages=5 route surfaces + 5 drawer modes + 3 modal types (fails LEAN's ≤2 outright)
             · states: balance status alone = 4 → **states ≥ 4 satisfies the FULL branch
             independently**, without even needing location status or BP status
             · Engine Management: 3 independent CUBIC-Engine candidates are declared in
             `03_LOGIC.md §3.2` (unit-conversion engine, adjustment-ceiling validation engine,
             append-only audit-log engine) → **a second independent hit on the FULL branch**
             · approval AND money = FALSE (neither condition holds as specified) — this arm does
             NOT trigger, and is recorded here so the decision is not silently over-claimed
→ Variant = FULL (9 files + INDEX), triggered independently by (states ≥ 4) AND (Engine
  Management), NOT by (approval ∧ money)
```

**Log:** `Variant = FULL (fallback from PREBRIEF: pages=5 route surfaces + 5 drawer modes + 3
modal types, states≥4 [balance status alone = 4], approval=No, money=No as scoped [valuation
present in HTML is an unscoped carried gap, see G-01], multi-engine=Yes [3 engines]). The FULL
branch is satisfied twice independently — states≥4 and Engine Management — and NOT by
approval∧money, which is the honest evaluation the calling instruction asked to see rather than a
default assumption.`

**Additional reasoning beyond the mechanical rule:** this feature carries a genuine multi-line
document-style editor (Manual Adjustment, OB-8) with per-line live validation against two
different ceilings (allocated-quantity ceiling, location/master availability), an append-only
audit trail with its own dedicated view + drawer (OB-11/S-12), and a two-phase locking sub-workflow
(Break/Pack, S-11) that mutates `allocated` as a side effect of order creation. Any one of these
alone would likely justify STANDARD; together, with the states≥4 and multi-engine hits already
independently satisfying FULL, STANDARD would under-document the interactions (in particular the
`LOCKED_LOCS` cross-cutting guard that both `adjLineError()` (L2601) and Break/Pack's own lock
(L2343-2344) depend on).

### §0.1.2 Input Substitution Note

This feature has **no traditional `BRD_F-XX.md`**. In its place, `PREBRIEF_F-INV_Stock-by-Location.md`
serves as the business source of truth (§0 Obligations OB-1..12, §1 Scope, §2 Scenarios S-01..S-12
incl. S-05b/S-08b, §3 pointer to Function Checklist, §4 Data per scenario, §5 Coverage Matrix,
§6 Open Questions OQ-INV-01..05, §7 Precedents), paired with
`FUNCTION_CHECKLIST_F-INV_Stock-by-Location.md` (FN-01..23, FN-30, FN-40 — numbered with
intentional gaps per the checklist's own declaration).

This FRD treats each PREBRIEF section as its BRD counterpart per the skill's Conflict Resolution
table (§2 Scenarios ↔ BRD §7/§10, §4 Data ↔ BRD §6, §5 Coverage Matrix ↔ BRD §9/§10 cross-check,
§6 OQ ↔ BRD Open Questions).

**Source PREBRIEF status: NOT human-approved in the traditional BRD sense.** Its header states it
is the source of truth "สกัดจาก ENC pack (base) + มติ 2026-08-09 ทั้งชุด" with "[AI-DRAFT]" tags
where the AI reasoned independently. §6 carries 5 open questions with named human owners (Strike,
พี่เบิร์ด, ทีมขาย, Chin) who have **not** signed off. This FRD is generated against the pinned
defaults implied by the already-built and already-QC'd HTML, and inherits their provisional
status — it does **not** claim BRD-style APPROVED status.

### §0.1.3 HTML Gate Status

`StockByLocation.html` passed both quality gates before this FRD run, with one carried flag:

- **UX/CI gate** (`_UX_CHECK_REPORT.md`): 🟢 **PASS with WARNINGS** — 3 BLOCK-level findings from
  Phase 1 (legacy 540px drawer, missing scrollbar block, wrong font stack) were fixed surgically
  and re-verified (`static_scan.py` confirms `540px: 0`, `920px: 1`, scrollbar present, Satoshi/Noto
  Sans Thai stack correct). Remaining WARNs are pre-existing stylistic drift (extended badge palette
  for 10 location types + 4 stock sub-statuses, hand-tuned font/spacing values) — none BREAKING,
  none block this FRD. One explicitly accepted deviation: **Manual Adjustment renders as a
  `.modal.is-adj` 1440px-wide modal, not a drawer** — this is a Rule #14 tension (multi-line create
  should normally be drawer/B2 pattern) but is treated as an accepted Reverse Mode override per
  PREBRIEF OB-8 ("มติ 2026-08-09"), not re-architected. See `07_LOCKED_DECISIONS.md` LD-01.
- **Coverage gate** (`_COVERAGE_REPORT.md`, round 1): 🟡 **WARN** — OB 12/12 ✓ · Scenario 12/12
  (+S-05b/S-08b) ✓ · FN 25/26 ✓ (FN-40 build/test gate out of this checker's scope, not a business
  gap) · **Scope Guard 4/5 clean, 1/5 = G-01 scope creep** (see §0.1.4 below). Verdict downgraded
  from PASS to WARN specifically because of G-01, which this FRD must not silently resolve.

Per Phase 1.5 **Mode A (Recognize & Validate)**, this FRD treats the gated HTML as de facto layout
ground truth — `01_UI.md §1.0` extracts observed patterns with real function names and line numbers
rather than deciding new ones.

### §0.1.4 Known Deviations Carried From Gate Reports (do not silently drop)

| Gate finding | What it means for this FRD | Where it lands |
|---|---|---|
| **G-01** (Coverage — Scope Guard) | A costing/valuation feature exists in the HTML (`canValuation()` L801, `canValExport()` L803, "ดูมูลค่า/ซ่อนมูลค่า" toggle L2047-2050, `.val-box` showing ต้นทุน/หน่วย + มูลค่าคงเหลือ = `on_hand × cost` at L2135-2144, "รวมมูลค่า" export toggle L1360-1374) that is **NOT in PREBRIEF scope** and directly contradicts PREBRIEF §1's explicit line "ไม่ทำ: ... costing engine (VD-PDM-07)". The HTML even cites a non-existent source: `// FRD §0.3 + BR-D02` (L790) — no such FRD section or business rule exists anywhere in this pack's inputs. | **Treated as an out-of-scope leftover / carried gap — pending decision.** NOT specified as an in-scope feature anywhere in this pack (`02_API.md`, `03_LOGIC.md`, `04_DB.md` explicitly exclude it). Recorded as **OQ-INV-06** (new, §0.8) and as **LD-02** in `07_LOCKED_DECISIONS.md` — the FRD does not invent a resolution either way (does not spec it as approved, does not spec its removal as mandatory) |
| **Manual Adjustment = wide modal (1440px), not drawer** | Rule #14 tension, explicitly accepted per OB-8 ("มติ 2026-08-09") | `07_LOCKED_DECISIONS.md` LD-01 · `01_UI.md §1.0` P-05 |
| **Extended badge palette (10 location types + 4 stock sub-statuses) beyond ci-tokens' 5 whitelisted pill pairs** | Genuine business need (PREBRIEF §4 LOCATIONS.type) — not remapped by the UX checker to avoid destroying visual distinction | Noted here only; `01_UI.md §1.4` records the palette as observed, not re-specified |
| **`FN-40` build/test gate** | Out of business-coverage scope per the checker's own division of labor — not re-verified in this FRD | Noted here only |
| **No real DOA/approval engine on high-value adjustments** | OQ-INV-01 (carried, unresolved) | §0.8 |

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-08-10 | frd-generator-v6.1 (AI, lane run) | Initial FRD generation from PREBRIEF + FUNCTION_CHECKLIST + gated HTML (Mode A) |

---

## §0.3 Scope

### In Scope (PREBRIEF §1 "ทำ")
- Stock-on-hand screen at (product × location) granularity within **1 warehouse at a time**
  (warehouse-gate-first routing, OB-1) — 4 views: by-product (aggregate) / by-location /
  break-pack / adjustment history
- Product drawer (3 tabs: overview / storage locations / movement) + balance drawer (view-only,
  same 3-tab shape) + location drawer ("what's in this location")
- **Manual Adjustment**: multi-line editor with live per-line validation, including creating a
  **new balance** in a previously-empty location (OB-8, S-05/S-05b)
- **Break/Pack**: create a break/pack order that locks source+destination locations, assign an
  owner, complete it (moves real stock) or cancel it (releases the lock) (S-11)
- **Append-only ADJ audit log** — view, search/filter, drill into any past adjustment (OB-11, S-12)
- **Low-stock monitoring** against `min_stock` from Item Master (OB-6, S-08) and **negative-stock
  display** for over-allocation reconciliation (S-08b, EC-07 by design)

### Out of Scope (PREBRIEF §1 "ไม่ทำ" — verbatim)
- **GRN / Putaway / RTV** — sidebar stub entries only, no route handler (`data-feature="grn"` etc.
  at L672-683 confirmed inert)
- **Multi-UOM bucket display per UoM** (VD-PDM-05 cut) — `bucketsFor()`/`UOMCONV` exist but are
  used only to compute "quantity in the location's own unit" (OB-4, in-scope), never to show a
  per-UoM breakdown in the list
- **Costing engine (VD-PDM-07)** — **see G-01 above: present in HTML as an unresolved leftover,
  not specified as an in-scope requirement anywhere in this pack**
- **Allocation/reservation authoring UI** — `allocated` is read-only everywhere in this feature;
  it is written only by the Sales system (upstream) and by this feature's own Break/Pack lock
  mechanism (a documented, in-scope side effect — see `05_RULES.md` BR-11)
- **Full location-transfer flow** — `MOVE_LABEL.transfer` exists only as a timeline label; there is
  no "move stock between locations" form beyond Break/Pack

---

## §0.4 Roles & Responsibilities

Source: HTML `ROLE_META` (L793-799) — 5 roles, corroborated by `canAdjust()` (L1032),
`canExport()`/`canValuation()`/`canValExport()` (L801-804).

| Role | เห็นอะไร | ทำอะไรได้ | HTML evidence |
|---|---|---|---|
| **Inventory Viewer** (`inventory_viewer`) | ทุกคลัง (no scope lock) | อ่านอย่างเดียว — ไม่มีปุ่มปรับสต็อก/export/valuation | `ROLE_META.inventory_viewer.scope = null`; excluded from `canAdjust`/`canExport`/`canValuation` |
| **Warehouse Staff** (`warehouse_staff`) | **เฉพาะคลังของตัวเอง** (`scope: 'WH-01'`, row-level lock — `roleScope()` L804 forces `whCtx`) | ปรับสต็อก (`canAdjust` ✓) · แตก/แพ็ค · ไม่เห็น export/valuation | `roleScope()` used at L1160, L1222, L1281 to force warehouse context |
| **Procurement** (`procurement`) | ทุกคลัง | อ่านอย่างเดียว — เหมือน Inventory Viewer (ไม่มีสิทธิ์ปรับ/export/valuation ตาม flags ปัจจุบัน) | not in `canAdjust`/`canExport`/`canValuation` lists |
| **Finance** (`finance`) — **default demo role** | ทุกคลัง | ปรับสต็อก (`canAdjust` ✓) · export (`canExport` ✓) · **ดูมูลค่า + export รวมมูลค่า** (`canValuation`/`canValExport` ✓ — this is the G-01 surface) | `CURRENT_ROLE = 'finance'` (L800) |
| **Auditor** (`auditor`) | ทุกคลัง | ไม่ปรับสต็อก · export ✓ · ดูมูลค่า ✓ (export-รวมมูลค่า ✗ — เฉพาะ finance) | `canValExport()` L803 explicitly `=== 'finance'` only |

> **RBAC boundary (OB-12, S-10):** `canAdjust()` (L1032) gates every adjustment entry point —
> product drawer header (L1932), balance drawer header (L2041), list page header (L1524), audit
> log page header (L2762) — via **conditional render**, not merely `disabled`. A non-permitted role
> never sees the button. Attempting the action anyway (e.g. scripted call) is also blocked at the
> function entry (`openAdjust()` L2578 toast: "ไม่มีสิทธิ์ปรับสต็อก (Warehouse Staff / Finance
> เท่านั้น)").
>
> **Row-level scoping note:** `warehouse_staff` is the only role with a forced single-warehouse
> scope — it skips the warehouse-selection gate entirely and cannot call `changeWh()` (L1346 no-ops
> when `roleScope()` is truthy). `02_API.md §2.3` requires this be enforced server-side
> independently of the client-side gate.

---

## §0.5 Dependencies

### Upstream (this feature reads — config/data reads, no cascade)

| Dependency | Type | Used for |
|---|---|---|
| **Item Master** (Product Master) | Config read (soft-ref) | `code`/`old_code`/`type`/`typeLabel`/`uom`/`cost`/`status`/`min_stock` — this feature JOINs product_master, owns only `stock_balances` (comment at L807-809) |
| **Location Hierarchy** | Config read (soft-ref) | Warehouse → Zone → Area → Rack → Location tree (`locContext()` L952) + `loc_status`/`type`/`cap_uom`/`cap_val` |
| **Sales system** | Runtime read (`allocated`) | `allocated` on every balance is populated by Sales reservations — this feature never writes it except via its own Break/Pack lock side effect (BR-11) |
| **GRN (Goods Receipt)** | Runtime read (`in_transit`, `received`) | `in_transit` quantity and FIFO `received` timestamp are populated by GRN, displayed read-only here |
| **User Management / Policy & Security** | Runtime read | Role-based capability flags (§0.4) — mocked via `ROLE_META`/`setRole()` in the prototype, must be real Policy Center in production (OB-12) |

### Downstream (features that consume this feature's data)

| Consumer | What it uses | Production status |
|---|---|---|
| **Accounting** | ADJ log → mūlkā adjustment value (PREBRIEF §1 "เส้นออก") | 🔴 not produced — future; **not built in this pack** because valuation is the unresolved G-01 gap |
| **Purchase** | Low-stock signal → replenishment request | 🔴 not produced — **OQ-INV-05** (unresolved: notification vs. auto-PR vs. report-only) |

### External / Shared Foundation

| Service | Purpose |
|---|---|
| Audit Trail (Shared Foundation) | `ADJLOG.unshift()` (L2727) is append-only — no `splice`/delete found anywhere on `ADJLOG` in the file |
| Policy Center | Real RBAC enforcement for `canAdjust()` — mocked via `ROLE_META` in the prototype (OB-12) |

---

## §0.6 Stack & Architecture

| Layer | Technology (as observed in gated HTML / CUBE ERP standard) |
|---|---|
| Frontend | Single-file vanilla JS SPA (`state` object + `render()`), CUBE Warm Light CI per Sync Read |
| API | To be implemented per `02_API.md` (REST, CUBE convention) |
| Database | PostgreSQL (RLS multi-tenant + multi-warehouse row scoping, CUBE ERP standard) |
| Engine layer | 3 CUBIC Engine candidates — see `03_LOGIC.md §3.2` |
| Auth | JWT + role-based (5 roles, warehouse row-scoping for `warehouse_staff`) |

---

## §0.7 Multi-Tenant & Security Context

- [x] **Multi-tenant feature: YES** (CUBE ERP standard) — RLS on `tenant_id` assumed, not directly
      observable in a single-tenant prototype
- [x] **Multi-warehouse row scoping: YES** — `warehouse_staff` role is scoped to one warehouse
      server-side, not merely hidden client-side (§0.4)
- [ ] **PII data involved: NO** — this feature holds no personal data; `PEOPLE`/`assignee` on
      Break/Pack orders is internal employee-directory data, not customer/individual PII
- [x] **Financial data: CONDITIONAL** — `cost`/valuation exists in the HTML (G-01) but is **out of
      scope** per PREBRIEF; this pack does not specify it as a financial-data surface to build.
      If G-01 is resolved "in favor of keeping it," it must re-enter this pack through a proper
      Security Bible pass at that time (flagged in §0.8 OQ-INV-06)
- [x] **Audit log required: YES** — append-only ADJ log, every create/edit path (BR-10)

**Security Bible domains applied:** **D9** (Audit Logging — append-only ADJ log), **D15** (Admin
Actions — Manual Adjustment + Break/Pack require a mandatory reason/assignment), **D17**
(Multi-Tenant/Multi-Warehouse Isolation — `warehouse_staff` row scoping). **D5** (Financial) is
**deliberately NOT applied** in this pass because the valuation surface that would trigger it is
the unresolved G-01 gap, not an in-scope requirement — see `05_RULES.md §5.7`.

### §0.7.1 Data Classification Summary (R10)

**Highest classification level this feature specifies as in-scope: `Internal`.**

- [ ] Has Restricted fields — **NO** (no PII, no national-ID-class data)
- [x] **Has Confidential fields — CONDITIONAL, currently N/A**: `PRODUCTS.cost` and the derived
      `on_hand × cost` valuation exist in the HTML and **would** be Confidential if specified —
      but since G-01 leaves this un-specified, `04_DB.md §4.2` marks the `cost`-adjacent surface
      **N/A pending G-01 resolution** rather than assigning it a classification for a feature that
      isn't formally in scope
- [x] **Internal (default)** — stock quantities, location codes/hierarchy, product codes, ADJ log
      contents (reason, actor, before/after quantities), Break/Pack order data
- [ ] Public-facing data — **NO**

**Linkage:** No Restricted fields exist in the specified (in-scope) surface of this feature, so no
Restricted Resources registry wiring is required for what this pack actually specifies. **If**
G-01's valuation surface is later ratified as in-scope, `cost`/valuation must be re-classified
Confidential and routed through a Security Bible D5 review before it re-enters any pack — this is
the substance of **OQ-INV-06**.

---

## §0.8 Open Questions

> **PREBRIEF's own register is OQ-INV-01..05, reproduced below verbatim in meaning and unmodified
> in numbering — none has been resolved by this FRD pass.** OQ-INV-06 is **new**, raised by this
> FRD directly from the Coverage gate's G-01 finding.

| ID | Question | PREBRIEF's own [AI-DRAFT] lean | Blocking? | Owner |
|---|---|---|---|---|
| **OQ-INV-01** | Manual Adjustment มูลค่าสูงต้องมีอนุมัติ (DOA) ไหม? ตอนนี้บันทึกตรงไม่มีสายอนุมัติ | ควรมี threshold — ประกาศผ่าน DOA กลาง (วงเงิน = มูลค่าปรับ) | NO (feature is usable without it; risk is control-gap on large adjustments) | **Strike** |
| **OQ-INV-02** | `min_stock` เป็น per-item (รวมทุกคลัง) หรือ per-item-per-warehouse? ปัจจุบันเทียบ avail ของคลังที่เปิดอยู่กับ threshold ก้อนเดียว | standard = per warehouse/location group | NO | **Strike + พี่เบิร์ด** |
| **OQ-INV-03** | หน่วยของตำแหน่ง (1-loc-1-uom) เปลี่ยนได้เมื่อไหร่ — เฉพาะตอน loc ว่างสนิท? ใครมีสิทธิ์? (กระทบ Location Hierarchy master) | ไม่ระบุ default — genuinely open | NO | **Strike** |
| **OQ-INV-04** | สต็อกติดลบ (จองเกิน, EC-07): ใครเป็นเจ้าภาพ reconcile + ระบบขายควรถูก block จองเกิน avail ตั้งแต่ต้นทางไหม | ไม่ระบุ default — genuinely open, cross-feature with Sales | **YES for go-live** (negative stock currently just displays, with no owner assigned) | **Strike + ทีมขาย** |
| **OQ-INV-05** | Low stock → ต่อ action อะไร: แจ้งเตือน (F-NT) / สร้าง PR อัตโนมัติ / รายงานเฉย ๆ | ไม่ระบุ default — genuinely open | NO | **Strike** |
| **OQ-INV-06** (new, from Coverage G-01) | Costing/valuation display (`canValuation`, `.val-box`, "รวมมูลค่า" export) exists in the HTML but directly contradicts PREBRIEF §1's "ไม่ทำ: costing engine". Keep it (needs a real OB/S/FN + Security Bible D5 pass) or strip it from the HTML before dev handoff? | **No default taken by this FRD** — per the calling instruction, this must not be silently resolved either way | **YES — must close before dev sign-off**, because leaving the HTML as-is ships an unspecified, un-reviewed financial-data surface | **Strike** (business decision) + **Architect/Security** (if kept) |

> Resolved questions → move to `07_LOCKED_DECISIONS.md` as LD-NN.
> **Count: 6 open questions (5 inherited verbatim from PREBRIEF §6 + 1 new).**

### §0.8.1 Phase 2.5 Edge-Case Probing Log (Lane Mode — no-ask)

Per the skill's Lane Mode, no question was put to the user. Each probe was resolved in order:
(1) PREBRIEF, (2) gated HTML, (3) conservative default tagged `[AI-DEFAULT]`.

| Probe | Triggered by | Resolution | Source | `[AI-DEFAULT]`? |
|---|---|---|---|---|
| **PR-1** Concurrency | two staff adjusting the same balance simultaneously | Server must re-read `on_hand`/`allocated` at write time; second concurrent write against a stale snapshot loses on version mismatch → 409 | Conservative default (HTML has no client-side concurrency guard at all — mock is single-user) | ✅ `[AI-DEFAULT]` → `05_RULES.md` EC-INV-01 |
| **PR-2** Stale data | list/drawer view held open while another user adjusts | Not addressed by PREBRIEF or HTML (no `If-Match`/version anywhere) | Conservative default | ✅ `[AI-DEFAULT]` → `05_RULES.md` EC-INV-02 |
| **PR-3** Permission mid-flight | role switch while a drawer/modal is open (demo `setRole()` shows this can literally happen) | Re-check `canAdjust()`/warehouse scope server-side at mutation time, not just at initial render | HTML's own `setRole()` (L1385) already resets pagination + navigates away, corroborating that client state cannot be trusted after a role change | ✅ `[AI-DEFAULT]` → `05_RULES.md` EC-INV-03 |
| **PR-7** Idempotency | double-submit on `submitAdjust()`/`submitBPOrder()` | `Idempotency-Key` required on both mutation endpoints, 24h cache | Conservative default (client only has an implicit single-flight via modal-close, not a real guard) | ✅ `[AI-DEFAULT]` → `05_RULES.md` EC-INV-04 |
| **PR-9** Race condition | `(pid, loc_id)` uniqueness invariant (PREBRIEF §4 RAW) | Application-level uniqueness check (`submitAdjust()` L2700-2701 dedupes within one submitted batch) is insufficient under concurrent submits from two users — a DB unique constraint is the authority | Conservative default | ✅ `[AI-DEFAULT]` → `04_DB.md §4.2` unique constraint |
| **PR-8** Compensation | Break/Pack: `submitBPOrder()` writes `allocated` (lock) + creates the order in what must be one transaction | **Answered by the HTML itself** — `submitBPOrder()` (L2338-2344) sets `allocated` and pushes the order together; a partial failure would strand a locked location with no matching order | Corroborated, not defaulted | ❌ no default needed |
| **PR-5** Bulk/atomic | Manual Adjustment is inherently multi-line/bulk | **Answered by PREBRIEF (OB-8/S-05)** — one ADJ document, multiple lines, all-or-nothing (any line error blocks the whole submit, per `adjLineError()` gating in `submitAdjust()` L2702-2705) | PREBRIEF S-07 | ❌ no default needed |

**`[AI-DEFAULT]` tag count: 4** (EC-INV-01..04 in `05_RULES.md §5.5`), consolidated for BA
confirmation alongside OQ-INV-01..06.

---

## §0.9 Glossary

| Term | Definition |
|---|---|
| **2-code model** | Every product carries exactly `code` (รหัสกลาง) + `old_code` (รหัสเก่า, nullable) — `code_item`/`code_sku` are explicitly cut (OB-2) |
| **Available (พร้อมใช้)** | `on_hand − allocated`, computed per balance row (`avail()` L1059) or aggregated per product (`skuAgg()` L1221) |
| **1 location = 1 UoM** | Every location stores exactly one unit of measure at a time (business rule, not a UI restriction) — `locUomIdx()` (L1088) picks the largest unit for bulk/reserve/pack/dock/transit locations and the smallest (base) unit for pick-face/others |
| **Base unit (หน่วยฐาน)** | The smallest UoM in a product's conversion chain — `on_hand`/`allocated` in `RAW` are **always** stored in base units; the UI displays the location's own unit with the base-unit equivalent shown alongside when `factor > 1` (`qtyCell()` L1068) |
| **Break** | Convert a larger UoM at a source location into smaller UoM(s) at destination location(s) (e.g. 1 พาเลท → 10 แพ็ค) |
| **Pack** | The inverse of Break — combine smaller units into a larger unit |
| **ADJ document** | One Manual Adjustment submission = one `ADJLOG` entry (`ADJ-YYYY-NNNN`), which may contain multiple lines across different products/locations |
| **New balance (รายการใหม่)** | A Manual Adjustment line where `(pid, loc_id)` has no existing `RAW` row — submitting it creates one (OB-8/S-05b) |
| **Allocated ceiling** | The business rule that a reduce-adjustment can never take `on_hand` below `allocated` — allocated quantity is untouchable by Manual Adjustment (OB-11) |
| **Service item (SV)** | A product `type` that must never carry a stock balance, never appear in any picker/list/export on this screen (OB-3) — enforced by `isStockable()` (L830) |
| **G-01** | This FRD's internal shorthand for the unresolved costing/valuation scope-creep gap (§0.1.4, §0.8 OQ-INV-06) |

---

## §0.10 Pack Navigation

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW.md | All | This file — meta + scope + variant reasoning + 6 OQs + Coverage Manifest |
| 01_UI.md | FE dev | Layout Decision Log (Mode A, observed) + Pages + Journey |
| 02_API.md | BE dev (HTTP) | API contracts + Cross-Module Contract |
| 03_LOGIC.md | BE dev (logic) | Functions + 3 Engines + API↔Logic Trace Table |
| 04_DB.md | DBA / BE | Tables + Field Dictionary + Data Classification |
| 05_RULES.md | BE + QA | BR-01..11 + Edge Cases + Error Catalog + D-CLASS |
| 06_TESTS.md | QA | Acceptance Criteria + verbatim microcopy from the gated HTML |
| 07_LOCKED_DECISIONS.md | All | LD-01 (Adjustment modal deviation) · LD-02 (G-01 non-resolution) |
| INDEX.md | All | Cross-reference + Function Trace + Quick Nav |

---

## §0.11 Scope Lock (pointer)

> PREBRIEF has no §3.4-style formal Scope Lock section (no other feature's open question is being
> resolved here). **§7.0 in `07_LOCKED_DECISIONS.md` records this as "N/A — standalone"** — the
> only locked items in this pack are LD-01 (accepted modal-not-drawer deviation) and LD-02 (explicit
> non-resolution of G-01), both of which are design/process decisions, not cross-feature contract
> locks.

---

## §0.12 Coverage Manifest (R13 — PREBRIEF → Pack, no requirement left unlanded)

> Source: `PREBRIEF_F-INV_Stock-by-Location.md` §0 Obligations (OB-1..12) · §2 Scenarios
> (S-01..S-12 + S-05b/S-08b) · `FUNCTION_CHECKLIST` (FN-01..23, FN-30, FN-40) · §6 OQ register
> (OQ-INV-01..05). Rule: every row must name a landing place. Anything without one becomes an
> Open Question.

### §0.12.1 Obligations (OB-1..OB-12) — 12/12

| OB | Requirement (ย่อ) | อยู่ที่ใน Pack |
|---|---|---|
| OB-1 | ENC HTML = superset, rebrand Warm Light/CUBE 4.0 | `01_UI` §1.0 CI note (Sync Read v8 — not hardcoded) |
| OB-2 | 2-code model (code + old_code) | `04_DB` §4.2 `PRODUCTS`/`T_product` fields · `03_LOGIC` FN-05 `fourCodeChips` · `05_RULES` BR-01 · `06_TESTS` AC-01 |
| OB-3 | Service exclusion (SV) | `03_LOGIC` FN-03 `isStockable` · `05_RULES` BR-02 · `06_TESTS` AC-05/AC-06 |
| OB-4 | 1 location 1 uom + base ledger | `03_LOGIC` **ENG-INV-01 unit-conversion-engine** + FN-06 `rowUnit`/FN-08 `locUomIdx` · `05_RULES` BR-03 · `06_TESTS` AC-02 |
| OB-5 | List "ตามสินค้า" = 1 แถว/สินค้า | `01_UI` P-02 · `03_LOGIC` FN-04 `skuAgg` · `05_RULES` BR-04 · `06_TESTS` AC-01 |
| OB-6 | Low stock จาก `min_stock` (Item Master) | `02_API` §2.X cross-module (Item Master) · `03_LOGIC` FN-09 · `05_RULES` BR-05 · `06_TESTS` AC-07 |
| OB-7 | สถานะ list 3 ค่า (ปกติ/ต้องเติม/ขาดสต็อก) | `01_UI` P-02 · `03_LOGIC` FN-04 (embedded classify) · `05_RULES` BR-06 · `06_TESTS` AC-01/AC-07/AC-08 |
| OB-8 | Adjust สร้าง balance ใหม่ + line editor grid v8 B2 | `01_UI` P-05 (LD-01 modal deviation) · `03_LOGIC` FN-13..17 · `05_RULES` BR-07 · `06_TESTS` AC-09/AC-10 |
| OB-9 | #95 Overlay Portal + Esc chain | `01_UI` §1.0 component note · `03_LOGIC` FN-20 `ddTog`/`ddCloseAll` · `06_TESTS` AC-15 |
| OB-10 | #67.1 Hint opt-in (no teaching hints) | `01_UI` §1.0 note (verified absent) |
| OB-11 | Allocated untouchable + append-only ADJ log | `03_LOGIC` **ENG-INV-02 adjustment-ceiling-engine** + FN-15 `adjLineError` + **ENG-INV-03 audit-log-engine** · `04_DB` `T_stock_adjustment_log` append-only · `05_RULES` BR-08/BR-09 · `06_TESTS` AC-11/AC-12 |
| OB-12 | RBAC (warehouse_staff + finance only) | `00_OVERVIEW` §0.4 · `02_API` §2.3 · `03_LOGIC` FN-19 `canAdjust` · `05_RULES` BR-10 · `06_TESTS` AC-13 |

### §0.12.2 Scenarios (S-01..S-12, incl. S-05b/S-08b) — 14/14

| S | ชื่อ | อยู่ที่ใน Pack |
|---|---|---|
| S-01 | เปิดจอครั้งแรก | `01_UI` P-02 · `02_API` API-01 · `03_LOGIC` FN-01/FN-04 · `06_TESTS` AC-01 |
| S-02 | product drawer 3 tabs | `01_UI` P-02 drawer-product · `02_API` API-02 · `03_LOGIC` FN-06/FN-07/FN-10 · `06_TESTS` AC-02 |
| S-03 | by-location + loc drawer | `01_UI` P-03 · `02_API` API-05 · `03_LOGIC` FN-11/FN-12 · `06_TESTS` AC-03 |
| S-04 | ค้นหา + กรอง | `01_UI` P-02 filter bar · `03_LOGIC` FN-01/FN-22 · `06_TESTS` AC-04 |
| S-05 | ปรับเพิ่ม/ลด multi-line | `01_UI` P-05 · `02_API` API-08 · `03_LOGIC` FN-13..18 · `05_RULES` BR-07 · `06_TESTS` AC-09 |
| S-05b | เพิ่มเข้าตำแหน่งว่าง | `01_UI` P-05 · `03_LOGIC` FN-17 · `05_RULES` BR-07 · `06_TESTS` AC-10 |
| S-06 | ลดชนเพดานจอง (blocked) | `03_LOGIC` FN-15 `adjLineError` · `05_RULES` BR-08 · `06_TESTS` AC-11 |
| S-07 | ตำแหน่ง/มาสเตอร์ไม่พร้อม (blocked) | `03_LOGIC` FN-15 · `05_RULES` BR-08 · `06_TESTS` AC-11b |
| S-08 | Low stock | `01_UI` P-02 stat + badge · `03_LOGIC` FN-09 · `05_RULES` BR-05 · `06_TESTS` AC-07 |
| S-08b | ขาดสต็อก (ติดลบ, EC-07) | `01_UI` P-02 badge · `05_RULES` BR-06/EC-INV-05 · `06_TESTS` AC-08 |
| S-09 | สินค้าบริการไม่โผล่ | `03_LOGIC` FN-03 `isStockable` (all call sites) · `06_TESTS` AC-05/AC-06 |
| S-10 | สิทธิ์ | `00_OVERVIEW` §0.4 · `03_LOGIC` FN-19 `canAdjust` · `06_TESTS` AC-13 |
| S-11 | Break/Pack | `01_UI` P-04 · `02_API` API-09..11 · `03_LOGIC` FN-23..26 · `05_RULES` BR-11 · `06_TESTS` AC-14 |
| S-12 | Audit log | `01_UI` P-06 · `02_API` API-12 · `03_LOGIC` FN-18 (write) + FN-27 (read/filter) · `05_RULES` BR-09 · `06_TESTS` AC-12 |

### §0.12.3 Function Checklist (FN-01..23, FN-30, FN-40) — 25/26 landed, 1 out of business scope

All 25 business-facing items map to `03_LOGIC.md §3.1` Functions and/or `01_UI.md §1.2` page
actions — the full FN → FRD-ID cross-reference is in `INDEX.md` Function Trace. FN-40 (build/test
gate: `node --check`, audit navy=0, Playwright 60+, md5) is infrastructure/CI, not a business
function — noted here as **N/A to this FRD** per the same division of labor the coverage checker
itself applied.

### §0.12.4 Open Questions (OQ-INV-01..05) — 5/5 carried

All five are reproduced in **§0.8 above**, unresolved and un-renumbered, each retaining its
PREBRIEF owner. One more (OQ-INV-06) was added by this pass for G-01.

### §0.12.5 Manifest Summary

**OB 12/12 ✅ · S 14/14 ✅ · FN 25/26 landed (1 N/A — infra gate) ✅ · OQ 5/5 carried ✅**

**Requirements with no landing place: 0.** Nothing was silently dropped. One new Open Question
(OQ-INV-06) was raised for a *specification conflict discovered in the ground-truth artifact
itself* (G-01) — it is tracked rather than silently resolved in either direction, per the calling
instruction's explicit requirement.
