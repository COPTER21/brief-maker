# QC — UX HTML Checker Report

**File:** `01_HTML/StockByLocation.html` (3,113 → 3,127 lines after fix)
**Feature:** F-INV-001 Stock by Location — Reverse Mode (HTML = as-built ground truth)
**Authoritative rules:** html-generator-**v8** iron-rules / ci-tokens / microcopy (v6 superseded)
**Date:** 2026-08-10

## Verdict: **PASS with WARNINGS**

All hard BLOCK-level violations found in Phase 1 were fixed surgically and re-verified. Remaining findings are stylistic/typography drift (WARN) that pre-date this QC pass, are low-risk, and would require a broad rewrite to fully normalize — flagged instead of mass-edited to avoid destabilizing a business-validated Reverse Mode file.

---

## Initial counts (before fix)
- **BLOCK: 3** — legacy 540px drawer (Rule #11), missing custom scrollbar block (Rule #49/ci-tokens, mandatory every file), wrong font stack + unused Inter Google Fonts import (Rule #2)
- **WARN: ~10** categories from self_audit.py (see below) — none are BREAKING iron rules, all pre-existing stylistic drift
- **NOT-CHECKED: 1** — real browser rendering (no Chromium/Playwright in this environment)

## Fixes applied (verified by re-running static_scan.py + self_audit.py)

| # | Rule | Location | Before → After |
|---|---|---|---|
| 1 | #11 Drawer Width Standard (BREAKING — 540px legacy banned) | line 445 `.drawer{...}` | `width: 540px` → `width: 920px` (v2 standard, used by product/location/BP/adj-log view drawers) |
| 2 | #49 Scrollbar (ci-tokens, mandatory in every file) | after `.drawer-backdrop`... actually inserted after RESET block, ~line 27-40 | Was using browser default scrollbar (`webkit_scrollbar:false` in scan) — added the standard thin/rounded scrollbar CSS block + `scrollbar-gutter: stable` on `html`/`.drawer-body`/`.modal-body`, dark-surface override scoped to `.sidebar` only (not `.drawer`, which is white — avoided an invisible-white-scrollbar-on-white-bg mistake caught during the fix) |
| 3 | #2 Font Stack (ห้าม font-family อื่น) | `<head>` font links + 7 `font-family` declarations | Removed unused `Inter` Google Fonts `<link>` (was loaded but never referenced); fixed reversed stack order `'Noto Sans Thai', 'Satoshi', ...` → canonical `'Satoshi', 'Noto Sans Thai', system-ui, sans-serif` on `body` + 6 heading/title selectors that were missing Satoshi entirely |

Confirmed post-fix via `static_scan.py`: `px_watchlist.540px: 0`, `920px: 1`; `webkit_scrollbar: true, scrollbar_width_px: 5`; `font_families: ["'Satoshi', 'Noto Sans Thai', system-ui, sans-serif", ...]`; Inter link gone. Esc chain (`escape_handler: true`), hashchange routing (`#/stock`, `#/stock/`), backdrop and `drawer_translate` were already correct and untouched.

## Business-logic surfaces reviewed (heuristic pass)

- **2-code model (OB-2):** confirmed only `code` + `old_code` used (`fourCodeChips()` line ~2560); no `code_item`/`code_sku` remnants found.
- **Service exclusion (OB-3):** `isStockable(p) { return p && p.type !== 'SV'; }` (line 818) correctly guards product picker in Manual Adjustment (`adjLineHTML` filters `Object.values(PRODUCTS).filter(isStockable)`).
- **3-value stock status (OB-7):** `ขาดสต็อก` / `ต้องเติม` / `ปกติ` pills present and mutually exclusive in list view.
- **RBAC (OB-12):** `canAdjust()` gate with toast `"ไม่มีสิทธิ์ปรับสต็อก (Warehouse Staff / Finance เท่านั้น)"` at `openAdjust()` entry (line 2566), tagged `// BACKEND: Policy Center RBAC`.
- **#95 Overlay Portal + Esc chain (OB-9):** `.dd-panel.is-portal` implementation moves dropdowns to `#dd-portal` at document end on open; keydown listener closes dropdown first (`Escape` + `.dd-panel.is-open` check) before the second listener closes modal/drawer — correct two-stage Esc chain.
- **Allocated ceiling guard (OB-11):** `adjLineError()` blocks reduce beyond `on_hand - allocated` with message `"ลดได้สูงสุด X ... ห้ามแตะยอดจอง"`.
- **New-balance-in-empty-location flow (OB-8/S-05b):** `adjLineInfo()`/`adjLineHTML()` correctly detect `isNew` (no existing RAW row) and render "รายการใหม่ในตำแหน่งนี้ · ปัจจุบัน 0 → n".
- **Manual Adjustment as wide modal, not drawer (Rule #14 tension):** the editor uses `.modal.is-adj` (`width: min(1440px, calc(100vw - 48px))`), not a drawer slide-in. This is technically a Rule #14 deviation (multi-line create should be drawer/B2 pattern), **but it is an explicitly documented business decision** — PREBRIEF OB-8 states "line editor grid (v8 B2) modal กว้าง ~1392px" sourced from มติ 2026-08-09. Treated as an accepted Reverse Mode override, not re-architected. Flagged here for visibility only.

## Remaining WARN (not fixed — see rationale)

From `self_audit.py` (independent counter, re-run after fixes):
- **hex_off (20 values)** — badge palette for 10 location types + 4 stock-substatuses (pick-face/reserve/hold/damaged/bulk/staging/pack/receiving-dock/transit/virtual, available/blocked/damaged/quarantine) uses hex pairs beyond the 5 pairs whitelisted in ci-tokens' "Pill Background Variants" table. This is a genuine business need (PREBRIEF §4 LOCATIONS.type has 7-10 distinct types that must stay visually distinguishable) that the current CI token set doesn't cover. **Recommend:** formalize an extended secondary-badge palette in `ci-tokens.md` rather than collapsing 14 categories into 5 approved colors (which would destroy the distinction OB-4/S-03 depends on). Not remapped in this pass — risk of visual regression outweighs a mechanical fix.
- **font_off / font_count (11 off-scale sizes, 18 total vs limit 8)** and **spacing_off (122)** — the file uses many hand-tuned px values (9.5–15.5px fonts, non-8pt-grid gaps like 7/11/13/14/17/18/19px) instead of the fixed `--fs-*`/`--sp-*` tokens from ci-tokens v3.13. This is broad, pre-existing drift across ~120+ declarations; normalizing all of it is a typography pass, not a surgical fix, and risks shifting the layout of a working, business-signed-off screen. Left as WARN for a dedicated follow-up pass.
- **flex_noalign (8), inline_layout (63), z_adhoc (9)** — minor: missing `align-items` on a few flex rules, inline layout styles on dynamic rows, and literal (not var-based) z-index numbers. The z-index values themselves (19/20/30/50/51/60/61/500) match ci-tokens' documented shell/sidebar/drawer/modal/portal stack exactly — this is a false-positive from the generic script (checks for `var(--z-*)` usage, which this ci-tokens version doesn't define as vars). No action needed.
- **missing_ids (`ddp-`, `ddw-`)** — false positive: these are dynamic id prefixes concatenated with an index at runtime (`'ddp' + i`), not literal ids; the regex flags the string-literal fragment before concatenation. No real missing element.
- **stopprop_blanket (1 over threshold)**, **tbody_font_fat (font-size 15 in a table cell)**, **long_banners (1 match)** — reviewed individually: the "15px" is a deliberately emphasized quantity number in the break/pack move table (design intent, not density bloat); the flagged "banner" (`bp-note`, line ~2972: "เมื่อสร้าง: ของต้นทางถูกจอง...") is a genuine action-consequence warning tied to creating a break/pack order, which Rule #33.3 explicitly exempts from the no-hint-banner rule. Neither requires a fix.
- **preflight stamp missing** — not stamped, correctly, since self_audit still reports non-zero counts above; per instructions a PREFLIGHT stamp should only be added once self_audit is fully clean, which is out of scope for this surgical pass.

## NOT-CHECKED

- **RENDER: UNAVAILABLE** — no Chromium/Playwright available in this environment (`python3 -c "import playwright"` fails, no `chromium`/`google-chrome` binary found). No screenshots were captured; none of the requested shot filenames (`main list`, `product drawer tabs`, `location drawer`, `manual adjustment modal`, `break/pack view`, `audit log view`, `Esc-chain`) exist. Do not treat any filename as produced — this pass is source-code/static-analysis only.

## Files
- Fixed: `/Users/chinchin/2b-projects/stike/output/11-inventory/DevPack_F-INV-001/01_HTML/StockByLocation.html`
- This report: `/Users/chinchin/2b-projects/stike/output/11-inventory/DevPack_F-INV-001/01_HTML/_UX_CHECK_REPORT.md`
