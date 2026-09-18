# 07_LOCKED_DECISIONS — F-INV-001 Stock by Location

> Audience: All roles

---

## §7.0 Scope Lock (R11)

**N/A — standalone.** PREBRIEF has no §3.4-style Scope Lock section, and this feature does not
resolve any other feature's open question. There is no cross-feature contract to lock here.

The two items below are **local design/process decisions**, not Scope Locks in the R11 sense —
recorded here because both are "do not silently re-decide this" items, which is the same spirit
even though the mechanism differs.

---

## §7.1 Locked Decisions (LD-NN)

### LD-01 — Manual Adjustment renders as a wide modal (1440px), not a drawer
**Decision:** The Manual Adjustment editor (P-05) is implemented as `.modal.is-adj`, a centered
modal `min(1440px, calc(100vw - 48px))` wide, rather than the drawer pattern (920px standard /
1290px `.wide` for B2 line editors) that Iron Rule #14 would otherwise require for a multi-line
create form.

**Source of the decision:** PREBRIEF OB-8 states this explicitly: "Adjust สร้าง balance ใหม่ได้
(เพิ่มสินค้าเข้าตำแหน่งว่าง) + line editor grid (v8 B2) modal กว้าง ~1392px + summary bar", citing
"มติ 2026-08-09" (a dated business decision, not an AI inference).

**Independent corroboration:** `_UX_CHECK_REPORT.md` reviewed this exact tension against Rule #14
and explicitly chose **not** to re-architect it, treating it as "an accepted Reverse Mode
override," flagged for visibility rather than silently normalized or silently flagged as a defect.

**Status:** LOCKED. Do not "fix" this to a drawer in a future HTML regeneration pass without a new
explicit business decision overriding OB-8. `01_UI.md §1.0` records this as an accepted deviation,
not an unresolved one.

**Consequence for dev:** the FE build must implement this as a modal component sized per the
observed CSS, not per the standard drawer component library defaults.

---

### LD-02 — G-01 (costing/valuation scope creep) is explicitly NOT resolved by this FRD
**Decision:** The costing/valuation surface found in the HTML (`canValuation()`, `canValExport()`,
".val-box" showing "ต้นทุน/หน่วย" + "มูลค่าคงเหลือ", "รวมมูลค่า" export toggle) is:
- **NOT specified as an in-scope requirement** in `01_UI.md`, `02_API.md`, `03_LOGIC.md`, or
  `04_DB.md` of this pack — none of those files define an endpoint, function, engine, or DB
  classification for it
- **NOT specified for removal** either — this FRD does not instruct that the HTML be stripped of
  this feature

**Why this FRD stops here rather than picking a side:** the calling instruction for this FRD run
was explicit that this must be handled as "an out-of-scope leftover / carried gap — pending
decision," consistent with treating it as unresolved rather than inventing a resolution. Choosing
either direction (spec it as real, or mandate its removal) would be inventing a business decision
that belongs to Strike (per PREBRIEF's own scope-out line: "ไม่ทำ: ... costing engine VD-PDM-07"),
not to this FRD pass.

**What happens next:** tracked as **OQ-INV-06** in `00_OVERVIEW.md §0.8`. Whichever way it
resolves:
- **If kept:** requires a new OB/Scenario/FN triplet added to a PREBRIEF revision, a Security
  Bible D5 (Financial) review, a `04_DB.md §4.6` Confidential classification for `cost`, and new
  `02_API.md`/`03_LOGIC.md` contracts — none of which exist yet in this pack
- **If removed:** requires the HTML to be patched to strip `canValuation`/`canValExport`/the
  `.val-box` block/the `inclVal` export toggle before dev handoff, and this pack requires no
  changes (it already omits the feature)

**Status:** LOCKED as *unresolved-and-tracked* — this framing itself must not be silently
discarded in a future pass; a future FRD revision must either supersede this LD explicitly (citing
the resolution) or continue to carry it forward.

---

## §7.2 Convention Deviations (non-blocking, observed)

| # | Observed deviation | Iron Rule tension | Disposition |
|---|---|---|---|
| 1 | Row-action column retains an eye icon (`<i data-lucide="eye">`) even though row-click already opens the same view | Rule #41 (no eye icon when row-click = view) | Pre-existing, non-BLOCK per UX gate; not re-specified as a fix in this FRD — carried as observation only (`01_UI.md §1.2` P-02) |
| 2 | Extended badge palette (10 location types + 4 stock sub-statuses) beyond ci-tokens' 5 whitelisted pill pairs | ci-tokens "Pill Background Variants" table | Accepted — genuine business need per OB-4/S-03 (distinguishing 10 location types); UX checker explicitly recommended formalizing an extended palette in ci-tokens rather than collapsing categories |
| 3 | Hand-tuned font/spacing values (11 off-scale font sizes, 122 spacing declarations) vs. fixed `--fs-*`/`--sp-*` tokens | ci-tokens v3.13 fixed type scale/spacing | Pre-existing, broad drift — WARN only, not BLOCK; UX checker left it for a dedicated follow-up typography pass rather than a surgical fix that risks layout regression on a business-signed-off screen |
