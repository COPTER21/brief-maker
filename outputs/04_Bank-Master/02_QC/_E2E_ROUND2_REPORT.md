# Bank Master — E2E ROUND 2 (Adversarial / Edge / Latent-Bug Hunt)

- **Target:** `outputs/04_Bank-Master/01_HTML/f-bank.html` (opened via `file://`)
- **Tool:** Real Playwright (Chromium, headless), Python 3.13, `PYTHONIOENCODING=utf-8`
- **Date:** 2026-08-11
- **Test script:** `scratchpad/r2_e2e.py` (drives the actual browser — clicks, types, scrolls, reloads)
- **Screenshots:** `_e2e_r2_shots/` (16 PNGs, one+ per matrix item)
- **Raw machine results:** `_e2e_r2_shots/_raw_results.json`

## VERDICT: **PASS — 15/15 passed · 0 console errors**

No bugs found. Every latent base-kit trap, negative path, business-rule edge, and robustness cycle held. Total console/page errors across the entire session: **0**.

---

## Matrix results

### Latent base-kit bugs (historically missed — hammered)

| # | Item | Result | Evidence |
|---|------|--------|----------|
| 1 | Drawer re-render no-jump (IR #29) | **PASS** | Edit KBANK-01 at 560px viewport → `.dw-body` overflow = 325px. Scrolled to 200px, then toggled checkbox + changed status dropdown + flipped ★def-receive. scrollTop stayed **200 → 200**. Root cause it holds: drawer inputs do not trigger `renderList()`/re-render, so there is nothing to reset the scroll. |
| 2 | Focus / input preservation | **PASS** | Typed `โฟกัสเทสต์` (name) + `สาขาทดสอบ` (branch), then clicked the use-pay checkbox. Both values retained verbatim; nothing wiped (no re-render on toggle). |
| 3 | In-drawer overlay z-index | **PASS** | Opened status menu inside VIEW drawer. `elementFromPoint(menu-center)` resolves to a `.pm-item` inside `#statusMenu` — menu paints **above** drawer body, not behind. |
| 4 | Overlay clip (Rule #95) | **PASS** | Status menu bottom (150px) ≤ drawer bottom (900px); not clipped by any overflow ancestor. GL picker is a native `<select>` (browser-rendered popup — structurally unclippable). |

### Negative / validation paths

| # | Item | Result | Evidence |
|---|------|--------|----------|
| 5 | Empty required fields | **PASS** | Cleared name + acct-no, clicked save → `#fld-acct-name` and `#fld-acct-no` get `has-err`, drawer stays open, record count 8→8. Visible validation, no silent no-op, no crash. |
| 6 | Duplicate code | **PASS** | Entered `KBANK-01` → `#fld-code` `has-err`, message `รหัส KBANK-01 ถูกใช้แล้ว`, count 8→8. Uniqueness enforced (case-insensitive). |
| 7 | Invalid account number | **PASS** | Entered `ABCXYZ` → digit-strip yields 0 digits → fails 10–12 rule → `#fld-acct-no` `has-err`, no crash, count 8→8. |
| 8 | Double-submit (IR #44) | **PASS** | Valid form, clicked save; the immediate second real click **timed out (blocked)** because `#saveBtn` gets `is-disabled` (`pointer-events:none`) synchronously. Exactly **1** record created. |

### Business-rule edges

| # | Item | Result | Evidence |
|---|------|--------|----------|
| 9 | IR-BNK-01 lock (used>0) | **PASS** | Edit KBANK-01 (used=620): `#in-bank` and `#in-acct-no` both `disabled` at the DOM. Force-cleared `disabled` + changed values via JS + saved → record still `bank=KBANK`, `account_no=012-3-45678-9`. Save-guard (`if(!locked){data.bank=…;data.account_no=…}`) means forced values do **not** persist. |
| 10 | Delete used-guard | **PASS** | Select KBANK-01 (used=620) only → bulk-delete confirm button `disabled`. Select KTB-01 (used=0) + KBANK-01 → confirm → KTB-01 removed, KBANK-01 kept, count 9→8. |
| 11 | GL picker draft hide/keep + rebind | **PASS** | Fresh create: options = `["", "KBANK"]` — SCB(draft) hidden. Edit SCB-01: `SCB — …(ร่าง)` present and selected (retained to prevent binding loss). Rebound to KBANK, saved → `posting_group='KBANK'` (old SCB binding cleanly replaced, no orphan). |
| 12 | Zero-row empty state | **PASS** | Filtered to `search=ZZZ_NO_MATCH_QUERY` → `.empty` block with icon + title (`ไม่พบบัญชีธนาคารที่ตรงกับตัวกรอง`) + desc + `ล้างตัวกรอง` action button; no table rows, no blank/broken table. |

### Robustness

| # | Item | Result | Evidence |
|---|------|--------|----------|
| 13 | Rapid open/close (drawer+modal) | **PASS** | 6 drawer open/Esc + 4 import-modal open/Esc cycles. End state: drawer/backdrop/modal all `is-open=false`, single `#drawer` node (no duplication), `body overflow='visible'`. Note: app never applies a body scroll-lock, so no scroll-lock leak is possible by design. |
| 14 | Reload mid-state (F5) | **PASS** | Applied filter + opened create drawer, then reloaded. Returns clean list (8 rows), drawer closed, **0** new console errors. Hash routing (`render()` on load/hashchange) is reload-safe. |
| 15 | Console-error sweep | **PASS** | **0** console errors / pageerrors across the entire adversarial session. |

---

## Design observations (not bugs)

- **No per-row or in-view Delete control.** Deletion is only reachable via bulk-select → `ลบ`. The matrix's "delete-from-view" overlay does not exist; item 3/4 were validated against the in-view **status menu** (the only in-drawer overlay) plus the native GL `<select>`. This is an intentional design choice (used>0 guard steers users to status-change instead of delete).
- **GL Posting Group picker is a native `<select>`**, not a custom JS dropdown — so Rule #95 overlay-clipping cannot occur there.
- **Body is never scroll-locked** while drawer/modal are open (background can scroll behind the overlay). Not a leak; simply no lock is applied. Minor UX note only.
- **Double-submit protection is `pointer-events:none`**, effective against real pointer input. A purely programmatic `.click()` (which bypasses pointer-events) would re-enter `saveBank` during the 500ms window; there is no in-flight boolean guard. Not reachable by a human user; noted for completeness (WARN-informational, not a defect).

## Console error total: **0**
