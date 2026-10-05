# UI Brief · F-WH-CYCLE นับตามรอบ
2026-09-14 · authored HTML shell/overlay, BRD §14, FRD 01_UI. Frozen SHA in gate evidence. Visual browser run NOT-CHECKED.

## 1. Intent
Set ABC policy, assign periodic blind counts, review/recount and send only reviewed nonzero variance to mock Stock Adjustment. No local stock/movement edit.
## 2. IA
ERP Warehouse shell, three tabs immediately under page-head: จัดชั้น ABC `#/records`, แผนนับและงานนับ `#/history`, ตรวจทานและประวัติ `#/settings`. Upper-right actions only; canonical `.toolbar>.search-box` on list. No hint/banner/wizard.
## 3. ABC list
Columns Item, value, frequency, score, actual share, class, status; descending score and stable code tie. Default score is monetary value, thresholds70/20/10; optional weighted score distinct and named. Show indivisible-item overshoot honestly and zero-total C. Data-derived stats/foot counts. Row click shows score/share/class details.
## 4. Policy drawer
Basis, effective ISO date, A/B/C percentages, frequency window and A/B/C cadence months. Validate sum100, nonnegative percentages, positive window/cadence and real date. Save appends version; current ABC resolves policy effective at tenant business asOf, so a future policy does not reclassify today. Plan drawer records วันที่สร้างแผน and resolves its effective policy; old plan snapshots unchanged. Cancel no change. Config is effective, not hardcoded threshold logic.
## 5. Plan list/drawer
Rows id, item, lot/location, due, assigned person, class, status. Create drawer searchable Item picker, Warehouse, named counter, last accepted review date. Capture Item/UoM/expected/policy snapshots; due Jan31→Feb28/Apr30/Jul31 by class. Counter list never shows expected.
## 6. Count drawer
Assigned counter sees item/lot/location/UoM and blank counted field. Blank rejected, zero accepted. Recount opens new blank field; old attempt remains immutable reviewer audit. No expected/value/variance in counter drawer/list/export. Prototype fixture keeps expected in memory and is not a production security boundary.
## 7. Reviewer
After submitted, reviewer sees expected/count/base delta and latest attempt. Accept requires reason; request recount opens new attempt. Before review no mock dispatch. Old attempt cannot be accepted after recount. Zero delta closes without StockAdj. Nonzero reviewed shows `ส่งผลต่าง (mock)` and only an ack/ref, not actual adjustment.
## 8. History
Append-only policy/plan/count/review/mock events with time/actor/source. Search/filter and footer based on visible data. No edit/delete. Actor refs Restricted, scoped production access.
## 9. States/microcopy
Assigned/รอนับ→submitted/รอตรวจ→recount_requested/นับใหม่ or reviewed/ตรวจแล้ว→adjustment_requested/ส่งผลต่างแล้ว. Toast reflects request/ack, never says stock adjusted. Inline errors keep drawer open. Distinct loading/empty/unavailable responses required in production.
## 10. Design system
v9 CUBE Warm Light with red action/orange demo, shared table/drawer/filter; 1280/1024 and narrow viewport scroll/popup behavior need real visual inspection. Table headings single datum per column, no fabricated totals.
## 11. Demo-only elements
`data-demo="persona-switch"` orange DEMO role selector exposes counter/reviewer local views. It is separate from real user identity and is not production authorization. QA marks it harness. Production API must derive actor permission server-side and deny `?view=reviewer`/alternate export or value endpoint bypass for a counter.
## 12. Accessibility/error
Input labels, keyboard searchable Item picker, focus after drawer, invalid count/threshold message adjacent. Keyboard, screen reader, Thai text rhythm, export, print and responsive interactions NOT-CHECKED because Playwright absent. Visual QA before release.
## 13. Developer handoff
FRD 00–08, CTX and 47-case TC are source. Move ABC snapshot/assignment, blind projection, review/version and W3 mock outbox server-side. Preserve 13/13 local arithmetic behavior. `[ASSUMED]` optional weighted mode/90-day window/zero/tie/month-end and OQ-ST-02 blind rule owner Warehouse Product Owner. No live W3 or CSQ claim.
