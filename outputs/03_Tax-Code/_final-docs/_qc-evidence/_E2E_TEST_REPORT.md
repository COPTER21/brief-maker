# E2E Test Report · Tax Code (F-TAX)

> Executed real SPA logic in **jsdom v25** (headless — Chrome extension declined). Instrumented a COPY of `f-taxcode.html`; original untouched.
> Run: 2026-08-10 11:02:31 · Rounds: 2 · Engine: node v24.18.0

## Verdict: 🟢 PASS

- **Round 1:** 21/21 passed · JS errors: 0
- **Round 2:** 21/21 passed · JS errors: 0

Total: **42/42** assertions passed across both rounds.

## Results per round

| TC | Trace | What it verifies | R1 | R2 |
|---|---|---|:--:|:--:|
| HOOK | - | instrumentation hook exposes app internals | ✅ | ✅ |
| TC-01 | FN-21/22 | List renders 10 records (page 8) + stats total10/active8/inactive1/draft1 | ✅ | ✅ |
| TC-02 | FN-01/02/03·S-01 | Create (blank code→auto VAT01, rate 7, active) | ✅ | ✅ |
| TC-03 | FN-03·S-01 | Create decimal rate 0.75 (WHT auto WHT01) | ✅ | ✅ |
| TC-04 | FN-05·S-02·BR-03 | Exempt → rate=0 & locked; switch back → unlocked | ✅ | ✅ |
| TC-05 | FN-06·S-03 | Edit used=0 (VAT10): code/rate/type all editable | ✅ | ✅ |
| TC-06 | FN-07·S-04·BR-04 | IR-TAX-01: used>0 locks code/rate/type + lock tag shown | ✅ | ✅ |
| TC-07 | FN-08·BR-04 | IR-TAX-01 guard: save keeps rate/code even if forced; name updates | ✅ | ✅ |
| TC-08 | FN-14·BR-01 | Duplicate code (vat7 vs VAT7) blocked + field error | ✅ | ✅ |
| TC-09 | FN-15·BR-02 | Rate invalid (>100 / <0 / empty) blocked | ✅ | ✅ |
| TC-10 | FN-09·S-05·BR-06 | Status changes freely draft⇄active⇄inactive (no approval) | ✅ | ✅ |
| TC-11 | FN-10·S-05 | Bulk set status (2 rows → inactive) | ✅ | ✅ |
| TC-12 | FN-12/13·S-06·BR-05 | Bulk delete removes used=0, skips used>0 | ✅ | ✅ |
| TC-13 | FN-17·S-08·BR-08/03/01/02 | Import validation: valid + 6 error codes | ✅ | ✅ |
| TC-14 | FN-18·S-08·BR-08 | Import confirms 3 valid / skips 2; blank status→draft | ✅ | ✅ |
| TC-15 | FN-16/20·S-09 | Export CSV + template download run cleanly | ✅ | ✅ |
| TC-16 | FN-21/22 | Filter status=draft + numeric sort by rate ascending | ✅ | ✅ |
| TC-17 | FN-24·OB-7 | Esc chain: 1st Esc closes menu, keeps drawer open | ✅ | ✅ |
| TC-19 | FN-16·S-08 | Import: no preview until a file is chosen (empty→stay pick, file→preview+filename) | ✅ | ✅ |
| TC-20 | FN-05·BR-03 | Exempt shows lock tag "ยกเว้นภาษี=อัตรา 0"; cleared on switch back | ✅ | ✅ |
| TC-18 | stability | Zero JS runtime/console errors during round | ✅ | ✅ |

## Detail (Round 1)

- **HOOK** ✅ — instrumentation hook exposes app internals
  - `window.__app ready`
- **TC-01** ✅ — List renders 10 records (page 8) + stats total10/active8/inactive1/draft1
  - `records=10 pageRows=8 stats=[10,8,1,1]`
- **TC-02** ✅ — Create (blank code→auto VAT01, rate 7, active)
  - `count 10->11 new=VAT01/7/active`
- **TC-03** ✅ — Create decimal rate 0.75 (WHT auto WHT01)
  - `new=WHT01/0.75`
- **TC-04** ✅ — Exempt → rate=0 & locked; switch back → unlocked
  - `exempt(val=0,disabled=true) backUnlocked=true`
- **TC-05** ✅ — Edit used=0 (VAT10): code/rate/type all editable
  - `code.dis=false rate.dis=false type.dis=false`
- **TC-06** ✅ — IR-TAX-01: used>0 locks code/rate/type + lock tag shown
  - `code.dis=true rate.dis=true type.dis=true lockTag=true`
- **TC-07** ✅ — IR-TAX-01 guard: save keeps rate/code even if forced; name updates
  - `name='VAT7 ชื่อใหม่' rate 7->7 code VAT7->VAT7`
- **TC-08** ✅ — Duplicate code (vat7 vs VAT7) blocked + field error
  - `count stable=true has-err=true`
- **TC-09** ✅ — Rate invalid (>100 / <0 / empty) blocked
  - `150:blocked -1:blocked empty:blocked`
- **TC-10** ✅ — Status changes freely draft⇄active⇄inactive (no approval)
  - `draft->active->inactive->draft`
- **TC-11** ✅ — Bulk set status (2 rows → inactive)
  - `T-004=inactive T-005=inactive`
- **TC-12** ✅ — Bulk delete removes used=0, skips used>0
  - `T-001(used214) kept=true T-010(used0) removed=true count 12->11`
- **TC-13** ✅ — Import validation: valid + 6 error codes
  - `valid:OK valid-blank-status:OK REQUIRED:OK BAD_TYPE:OK RATE_INVALID:OK EXEMPT_RATE:OK BAD_STATUS:OK CODE_DUPLICATE:OK`
- **TC-14** ✅ — Import confirms 3 valid / skips 2; blank status→draft
  - `imported=3 ok=3 err=2 VAT9.status=draft`
- **TC-15** ✅ — Export CSV + template download run cleanly
  - `no exception`
- **TC-16** ✅ — Filter status=draft + numeric sort by rate ascending
  - `draftFilter=true ratesAsc=true rates=[0,0,0.75,0.75,1,2,3,5,5,7,7,9,10,15]`
- **TC-17** ✅ — Esc chain: 1st Esc closes menu, keeps drawer open
  - `menuClosed=true drawerStillOpen=true`
- **TC-19** ✅ — Import: no preview until a file is chosen (empty→stay pick, file→preview+filename)
  - `pickStart=true emptyStays=true chosen->preview=true fn=taxcodes.csv`
- **TC-20** ✅ — Exempt shows lock tag "ยกเว้นภาษี=อัตรา 0"; cleared on switch back
  - `tagShown=true cleared=true`
- **TC-18** ✅ — Zero JS runtime/console errors during round
  - `clean`

---
_Note: Visual render gate (pixel layout) still needs a real browser pass before dev handoff — this harness verifies behavior/logic/state, not rendered pixels._
