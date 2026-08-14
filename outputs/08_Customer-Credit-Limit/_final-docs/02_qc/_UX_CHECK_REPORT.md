# UX Check Report — Customer Credit Limit

- Date: 2026-08-14 · Iteration: 4
- Generator: html-generator-v8
- Artifact: `../01_HTML/f-credit-limit.html`
- Render evidence: `_ux_shots_iteration2/route_credit-limits.png`

## Verdict: PASS

| BLOCK | WARN | INFO | NOT-CHECKED |
|---:|---:|---:|---:|
| 0 | 0 | 3 | 0 |

## Fixed since iteration 1

- UX-01: normalized all checked spacing, type scale, flex/grid alignment, inline layout and z-index values. `self_audit.py` now reports zero findings in every category.
- UX-02: consolidated the conflicting tab/advice selectors and replaced remaining ad-hoc component styles with the existing component classes.
- UX-03/UX-06: added explicit Lucide size utilities and type tokens. `audit.sh` result is `FAIL=0 · WARN=0`.
- UX-07: separated filter and table into inset panels, preserving breathing room around the list workspace.
- UX-08: preserved search focus and caret position across filter re-rendering.
- UX-09: realigned the DOA approval timeline to a 24px dot and a shared vertical centerline.
- UX-10: aligned `refreshChgFoot()` with the drawer validation rule so the submit button stays disabled unless the request is changed, reasoned and DOA-resolvable.
- UX-11: split request lifecycle into `รอส่งอนุมัติ` → explicit `ส่งอนุมัติ` → `รออนุมัติ`; approval actions are unavailable until the request is sent.
- UX-12: the DOA timeline now shows a role icon, approver name and position from the mocked DOA resolve payload.

## Verification evidence

- Static scan: approved CI colors and font stack; hash routing, Esc handler, 680px drawer, 440px confirmation modal and 5px scrollbar detected.
- Mechanical audit: `spacing_off=0`, `font_off=0`, `flex_noalign=0`, `grid_nogap=0`, `inline_layout=0`, `z_adhoc=0`.
- Render: list screen and primary action overlay rendered without overflow or stacking regression.

## Scope of this pass

This is a prototype UX gate. Live My Profile, Sales Order, AR Invoice and Notification integrations remain intentionally deferred and are tracked by the coverage report; they are not UX failures.
