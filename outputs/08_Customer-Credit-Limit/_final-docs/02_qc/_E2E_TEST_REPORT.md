# E2E Test Report — Customer Credit Limit

- Date: 2026-08-14
- Target: `../01_HTML/f-credit-limit.html`
- Runner: Playwright / Chromium
- Result: **PASS — 2/2 rounds**

## Round 1 — Credit control actions

1. Opened the list and verified 8 customer profiles.
2. Opened customer `CUST-2026-0033` and verified the View Drawer.
3. Recorded a credit review and verified success feedback.
4. Verified Hold requires a reason, then held the profile and verified feedback.
5. Unheld the same profile with a reason and verified feedback.
6. Pressed Esc and verified the drawer closed.

## Round 2 — Search and DOA approval flow

1. Typed a customer code character-by-character, verified the search box retained focus and verified one result; verified empty state and reset filter.
2. Opened Change Credit Limit; verified submit is disabled before valid input and when the requested limit equals the current limit.
3. Entered a DOA-supported amount and mandatory reason; verified `บันทึกคำขอ` enabled.
4. Verified the saved request is `รอส่งอนุมัติ`, sent it explicitly, then verified it changes to `รออนุมัติ` before approving each displayed DOA step until completion.
5. Verified no pending request remained and the History tab showed the completed approval event.

## Evidence

- `e2e_credit_limit.py` — repeatable test script.
- `_e2e_shots/r1_01_list.png`
- `_e2e_shots/r1_02_hold.png`
- `_e2e_shots/r2_01_pending.png`
- `_e2e_shots/r2_02_approved_history.png`

## Boundary

This validates the single-file Credit Limit prototype and its mock data/DOA behavior. Real My Profile, Sales Order, AR Invoice and Notification integrations remain deferred because their feature implementations do not yet exist.
