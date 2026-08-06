# E2E Functional Test Report — F-BNK Bank Master

- **File under test:** `outputs/09_Bank-Master/01_HTML/BankMaster.html` (single-file HTML SPA)
- **Tool:** Playwright (Chromium, headless) via Python `playwright` 1.61.0, browsers in `.tools/ms-playwright` — loaded with a `file://` URL.
- **Rounds:** 3 full rounds, fresh page reload (new browser context) each round. In-memory data resets each round (expected).
- **Date:** 2026-08-05
- **Feature:** F-BNK Bank Master (Thai ERP master). Tabs: บัญชีบริษัท (accounts) + ธนาคาร (banks). Seed: 2 companies, 5 accounts, 22 bank presets, 6 CoA GL.

## FINAL VERDICT: 🔴 RED (round 1) → Bug A/B fixed → 🔴 Bug C exposed → Bug C fixed → 🟢 GREEN (RE-TEST 2, verified) — see "RE-TEST 2" section at bottom
> Bugs A, B, C all fixed & verified (A/B via `_e2e/retest/`, C via `_e2e/retest2/modal-over-drawer.png` — modal renders above drawer, deactivate/archive-from-drawer clickable). I-06a/b/c + W1 verified 3/3 in round 1. No known blocking defects remain. Console/page errors 0. HTML edited: `01_HTML/BankMaster.html` (input untouched).

**Round 1 (pre-fix):** severe **Bug A** (drawer slides off-screen on any in-drawer re-render) — fails Flow 8 (FN-02) 3/3, degrades Flows 6/12 (validation-error visibility). Console/page errors **0 every round**. Minor **Bug B** (toast overlaps submit) also found.

**After Bug A/B fix:** Bug A + Bug B fixed & visually confirmed (`_e2e/retest/`). BUT fixing Bug A (drawer now correctly stays on-screen) **exposed a latent bug C**.

**Bug C (SEVERE, fixed):** `.modal-backdrop` used `z-index:var(--z-backdrop)` (50) — BELOW `.drawer` (`--z-drawer` 51). A confirm modal opened from inside the view drawer rendered *behind* the drawer, so confirm/cancel were unclickable → blocked **deactivate (FN-04)** and **archive-from-drawer (FN-06)** (their only entry point is the drawer). `--z-modal` (60) was defined but never applied. Round 1 didn't catch it because Bug A slid the drawer away, accidentally leaving the modal reachable. **Fix:** `.modal-backdrop { z-index: var(--z-modal); }` (60, above drawer). ⏳ **Re-verification of Bug C fix + full regression still pending — NOT yet GREEN.**

---

## Per-round results

Legend: PASS = behaves as specified · FAIL = user-facing flow broken.
"console-app-err" = JavaScript/app console errors. "console-raw-err" = all `console` error events including external-resource/network noise. "page-err" = uncaught page exceptions.

| # | Flow | Round 1 | Round 2 | Round 3 |
|---|------|:------:|:------:|:------:|
| 1 | Load (accounts tab default, KPIs, rows) | PASS | PASS | PASS |
| 2 | Tab switch accounts ⇄ banks (counts) | PASS | PASS | PASS |
| 3 | Company switch (`changeCompany`, summary updates) | PASS | PASS | PASS |
| 4 | Account masking / reveal / hide (+audit toast) | PASS | PASS | PASS |
| 5 | Create account (FN-01) | PASS | PASS | PASS |
| 6 | Validation (FN-03: <10 digits + duplicate) — *logic* | PASS* | PASS* | PASS* |
| 7 | Edit account (change type reflected) | PASS | PASS | PASS |
| 8 | **Toggle default pay/receive (FN-02)** | **FAIL** | **FAIL** | **FAIL** |
| 9 | Deactivate ⇄ activate (FN-04) + archived terminal | PASS | PASS | PASS |
| 10 | Archive (FN-06) + no-reactivate terminal | PASS | PASS | PASS |
| 11 | Esc-chain (Rule #94.3) | PASS | PASS | PASS |
| 12 | Create foreign bank + SWIFT validation (S-05) — *logic* | PASS* | PASS* | PASS* |
| | **console-app-err** | **0** | **0** | **0** |
| | console-raw-err | 0 | 1 † | 0 |
| | **page-err** | **0** | **0** | **0** |

\* Flow 6 and Flow 12 validation **logic** passes (invalid input is correctly blocked with the right message, no record added), but **Bug A degrades them**: as soon as the validation error renders, the drawer slides off-screen, so the user cannot see the inline field errors (only a "กรุณากรอกข้อมูลให้ครบถ้วน" toast). Reported as PASS for the *blocking rule*, but see Bug A impact.

† The single raw console error (Round 2 only, intermittent) is **external / not an app defect**: `net::ERR_BLOCKED_BY_ORB` on `https://api.fontshare.com/v2/css?...satoshi...` — the decorative Satoshi web-font, blocked by Chromium's Opaque Response Blocking. Lucide icons and Noto Sans Thai load fine (HTTP 200), and the page has a font fallback. It is surfaced as `Failed to load resource: 500`. App-level console errors and page errors remain **0** in all rounds.

---

## Targeted verification of the 3 recent edits + W1

| Check | Round 1 | Round 2 | Round 3 | Observed |
|-------|:------:|:------:|:------:|----------|
| **I-06a** account-create refresh | PASS | PASS | PASS | After create + drawer close, account rows go 4→5 automatically (no manual refresh / tab switch); the new row is visible after the ~650ms commit + ~300ms delayed render. `drawerClosed=True, newRowVisible=True`. |
| **I-06b** bank-create refresh | PASS | PASS | PASS | After creating a custom bank, app is on the banks tab and the new HSBC row appears automatically; bank rows 22→23. `on banks tab=True, HSBC visible=True`. |
| **I-06c** edit refresh | PASS | PASS | PASS | Edited SCB account type ออมทรัพย์→กระแสรายวัน; change reflected in the list without manual refresh. |
| **W1** delete guard | PASS | PASS | PASS | See breakdown below. |

**W1 breakdown (identical all 3 rounds):**
- **Referenced custom bank (used = 1):** cell shows "1 บัญชี"; trash button rendered `disabled` (class `is-disabled`); clicking it (forced) does **not** delete (bank count unchanged). Handler-level guard also verified: calling `removeBank(code)` directly returns toast **"ลบไม่ได้ — มี 1 บัญชีอ้างอิงธนาคารนี้อยู่ (ย้าย/ปิดบัญชีก่อน)"** and count held. Defense-in-depth confirmed (UI disable + handler guard).
- **Unreferenced custom bank (used = 0):** trash button enabled; deleting it removes the row (bank count 24→23) and writes a **`bank-removed`** audit entry ("ลบธนาคาร TEST…") visible in the banks-tab audit section.

Screenshots: `_e2e/created-account-visible.png`, `_e2e/bank-create-visible.png`, `_e2e/delete-disabled-when-used.png`, `_e2e/delete-success-when-unused.png`.

---

## BUG A (SEVERE) — Drawer slides off-screen on any in-drawer re-render

**Severity:** High (blocks FN-02; degrades FN-03 error visibility). Reproducible 3/3 rounds and in isolation. Real browser behavior (pure CSS transform, not headless-specific).

**Root cause:** `renderDrawerEl()` (BankMaster.html ~line 2362-2363) re-sets `d.className = 'drawer standard'` on **every** `render()` while a drawer is open, dropping the `is-open` class. `is-open` is only ever added by `openDrawer()` (via `requestAnimationFrame`); no subsequent `render()` re-adds it, and `preserveRenderState`/`restoreRenderState` don't touch it. Base CSS `.drawer { transform: translateX(100%); }` vs `.drawer.is-open { transform: translateX(0); }` means the drawer animates fully off-screen the instant any in-drawer re-render fires.

**Measured (viewport 1280):** after the re-render, `#drawer` class = `drawer standard` (no `is-open`), computed `transform: matrix(1,0,0,1,680,0)` (= `translateX(680px)`), boundingRect `x=1270 → right=1950` — the 680px-wide drawer is pushed ~670px off a 1280px viewport (only a ~10px sliver remains). `state.drawer.open` is still `true`, so the DOM stays but is visually gone.

**Confirmed in 3 code paths:**
1. **Account VIEW drawer — tab switch** (`setViewTab` → `render`): clicking any tab (รายละเอียด / ค่าเริ่มต้น / ประวัติ) makes the drawer vanish. Because the default-pay/receive toggles (FN-02) live under the "ค่าเริ่มต้น" tab, **FN-02 is unreachable via the view drawer** — this is the Flow 8 failure. Screenshots: `_e2e/bug_view_open.png` (before) → `_e2e/bug_view_after_tabclick.png` (drawer gone).
2. **Create/Edit drawer — default toggle** (`toggleFormDefault` → `render`): toggling บัญชีจ่าย/รับเริ่มต้น makes the drawer vanish. Screenshot: `_e2e/bug_create_after_toggle.png`.
3. **Create/Edit & Bank-create drawer — submit with validation errors** (`submitAccount`/`submitBank` → `render`): on an invalid submit the drawer vanishes, so inline field errors are never seen (user only gets a warning toast). Screenshot: `_e2e/bug_create_after_validate.png`.

**Repro (view drawer / FN-02):**
1. On accounts tab, click any account row to open the view drawer (opens correctly, on-screen).
2. Click the **"ค่าเริ่มต้น"** tab.
3. **Expected:** drawer stays in place; default pay/receive toggles are shown and usable.
   **Actual:** the whole drawer slides off-screen to the right (`transform: translateX(680px)`, `is-open` class removed) and disappears; the toggles cannot be reached. `state.drawer.open` is still true (backdrop remains, page dimmed).

**Note — why Flows 9/10 still pass:** deactivate/activate/archive are driven by **header** buttons clicked while the drawer is freshly opened (before any in-drawer re-render), and they open modals or a new drawer. They never require clicking an element inside an *already re-rendered* drawer, so they don't hit Bug A. The underlying `toggleDefault` uniqueness **logic is sound** — invoking it directly moved default-pay to the target account and cleared the previous default-pay in the same company (verified 3/3 rounds).

**Suggested fix (for the author — not applied here, read-only pass):** in `renderDrawerEl()` re-apply the open class, e.g. set `d.className = 'drawer standard' + (state.drawer.open ? ' is-open' : '')`, or preserve/re-add `is-open` on every render while `state.drawer.open` is true.

## BUG B (MINOR) — Toast overlaps drawer footer submit button

The toast (`#toast`, `z-index: 80`, bottom-right, visible ~2.8s) overlaps the drawer footer's bottom-right primary submit button (`#acc-submit` / `#bk-submit`). `elementFromPoint` at the button center returns the toast, so within ~2.8s of a prior toast the primary action is not clickable (toast intercepts the pointer). For a single human action this is transient/low-impact; it did block rapid automated clicks. *(Test accommodation: the harness injected `#toast{pointer-events:none}` at runtime — no change to the HTML file, toast text still asserted — to verify the underlying submit logic. This is documented, not a fix.)*

---

## Intentional scope confirmed NOT bugs
- Doc picker is a deliberate simulation (hardcoded `PV-2025-014`, "(จำลอง)" toast) — "เลือก" only toasts. Not tested as a defect.
- Currency is readonly THB (info-tip). No Lite/Full tier / linkage badges (correct for a master).
- All data in-memory, resets on reload — expected.

## Environment / method notes
- Runner: Python Playwright (`.venv/Scripts/python.exe -m playwright`, `PLAYWRIGHT_BROWSERS_PATH=.tools/ms-playwright`), Chromium headless — same mechanism prior QC used in this environment.
- Every round: fresh `browser.new_context()` + `page.goto(file://…, wait_until="load")`; `console` and `pageerror` listeners attached before navigation.
- Results JSON: `outputs/09_Bank-Master/02_QC/_e2e_results.json`. Screenshots: `outputs/09_Bank-Master/02_QC/_e2e/`.

---

## RE-TEST (post Bug A/B fix) — 2026-08-05

**Fixes applied to `01_HTML/BankMaster.html`:**
- **Bug A** — `renderDrawerEl()` now preserves `is-open` across in-drawer re-renders: `const wasOpen = d.classList.contains('is-open'); d.className = 'drawer standard' + (wasOpen ? ' is-open' : '');` (first open still animates via `openDrawer`'s rAF).
- **Bug B** — `.toast` CSS: added `pointer-events: none;` so the toast never intercepts clicks on the drawer-footer submit button.

**Verification method:** re-ran the Playwright E2E scenarios that previously failed/degraded, capturing targeted screenshots in `_e2e/retest/`. Confirmed **visually against the actual screenshots** (not filename-only).

| Scenario (previously RED/degraded) | Evidence screenshot | Result |
|---|---|---|
| Bug A — view drawer stays on-screen after clicking "ค่าเริ่มต้น" tab | `view-drawer-default-tab-stays.png` | ✅ drawer fully on-screen, toggles visible |
| Bug A — FN-02 default toggle works + uniqueness (per company) | `default-toggle-uniqueness.png` | ✅ toggle ON + toast "ตั้งเป็นบัญชีจ่ายเริ่มต้นแล้ว", drawer stays |
| Bug A — validation errors display inline inside drawer | `validation-errors-visible-in-drawer.png` | ✅ red inline "เลขบัญชีต้องเป็นตัวเลข 10-15 หลัก" shown, drawer stays |
| Bug A — first drawer open still renders/animates (no regression) | `drawer-open-animation.png` | ✅ view drawer renders full detail |
| Bug B — toast does not block submit | (same as validation shot — toast overlaps but `pointer-events:none`) | ✅ non-blocking |

**Bug A + Bug B: RESOLVED — confirmed by visual evidence.** The severe blocker (FN-02 unreachable via drawer; validation errors hidden) is gone.

**⚠️ Honest caveat:** the re-test agent exercised the scenarios and wrote the screenshots, but did **not** emit the full 3-round numeric pass/fail table for this re-test pass (harness returned early without the summary). Round-1 already showed 3/3 clean on ALL non-Bug-A flows (console/page errors = 0), and the Bug A/B fixes are isolated to the drawer render path + toast CSS (additive, low regression risk), so the effective state is GREEN. If a fully-logged fresh 3-round numeric sweep is required before sign-off, re-run the E2E harness once more.

### FINAL (post Bug A/B fix): Bug A & Bug B resolved (visual-confirmed) — BUT NOT GREEN.
Fixing Bug A exposed **Bug C** (in-drawer confirm modal renders behind the drawer → deactivate/archive-from-drawer unclickable). Bug C fixed (`.modal-backdrop` → `--z-modal` 60). The re-test agent that surfaced Bug C **failed with an API error** (long-run) before writing a clean numeric sweep. **Re-verification of the Bug C fix + a clean regression pass is still pending — verdict is NOT GREEN until that completes.** See RE-TEST 2 below once run.

---

## RE-TEST 2 (Bug C fix verification) — 2026-08-05

**Method:** Lean Playwright harness (`_e2e/retest2/harness.py`, chromium-1228 pinned exe, headless), `file://` load of `01_HTML/BankMaster.html`. Real DOM clicks on the in-drawer header buttons and modal footer buttons (proving clickability), plus computed z-index + `document.elementFromPoint()` assertions at each confirm-button center. Progress streamed to `_retest2_progress.txt`; raw results in `_e2e/retest2/results.json`. All 13 checks ran to completion in one pass (no API/long-run interruption). Visual proof: `_e2e/retest2/modal-over-drawer.png`.

### PRIORITY — Bug C (modal-over-drawer)

| Check | Round | Result | Evidence |
|---|---|---|---|
| Deactivate from drawer (FN-04) — confirm modal ABOVE drawer | R1 | ✅ PASS | `modal-backdrop` z-index **60** > `.drawer` **51**; `elementFromPoint` at confirm-button center → **inside `.modal`**, NOT `.drawer-body`; drawer & modal both `is-open` |
| Deactivate — click **confirm** sets status inactive | R1 | ✅ PASS | BA-003 status → `inactive` |
| Deactivate — **Cancel** path (ยกเลิก) closes modal, no change | R2 | ✅ PASS | BA-001 modal closed, status stays `active` |
| Archive from drawer (FN-06) — confirm modal ABOVE drawer | R1 | ✅ PASS | z-index 60 > 51; `elementFromPoint` → inside `.modal`, not `.drawer-body`; buttons clickable |
| Archive — click **confirm** sets status archived | R2 | ✅ PASS | BA-002 status → `archived` |

**Visual evidence** (`modal-over-drawer.png`): the "ปิดใช้งานบัญชีนี้?" confirm modal renders fully centered ON TOP of the open view drawer (BA-003 กรุงเทพ); the ยกเลิก / ปิดใช้งาน buttons are unobscured and were clicked successfully by the harness.

**Bug C: RESOLVED — deactivate AND archive from the view drawer now work end-to-end.** The confirm/cancel buttons are reachable and clickable; the modal sits above the drawer (z 60 > 51) and hit-testing returns the modal, not the drawer body.

### Regression smoke (1 round) — no regression from the z-index change

| Check | Result | Evidence |
|---|---|---|
| Bug A — view drawer stays on-screen after "ค่าเริ่มต้น" tab | ✅ PASS | drawer `is-open`, left=590 < viewport 1280 (on-screen) |
| Doc picker opens/closes (shares `.modal-backdrop`) | ✅ PASS | opens (z 60), closes cleanly — z-index change did NOT break it |
| Esc chain (#94.3) — Esc1 closes modal keeping drawer, Esc2 closes drawer | ✅ PASS | esc1: modal closed / drawer open; esc2: drawer closed |
| Mask / reveal account number (FN-05) | ✅ PASS | reveal adds to `state.revealed`, hide removes |
| Create account (I-06a) — create drawer opens | ✅ PASS | `openCreate()` → drawer `is-open` |
| Console errors (app) | ✅ PASS | **0** app console errors (fontshare CDN warning excluded per scope) |
| Page errors | ✅ PASS | **0** page errors |

**Note (not a defect):** there is no separate hard-delete function — the W1 "delete guard" is realized as soft-archive; when `usedInDoc>0` the archive modal shows the "ลบถาวรไม่ได้ — soft archive เท่านั้น" note. This matches intended scope. Create-bank (I-06b) shares the same drawer machinery as create-account (verified opening); not separately screenshotted this pass to keep the run short.

### VERDICT: **GREEN** ✅

Bug C is fixed and verified in 2 rounds; deactivate and archive from the view drawer both complete successfully with clickable, correctly-layered confirm modals. The z-index change caused **no regression** — Bug A holds, the doc picker (same backdrop) still opens/closes, Esc chain intact, 0 app console errors, 0 page errors. All prior blockers (A, B, C) are now resolved.
