# DevPack handoff · F-WH-ROP จุดสั่งซื้อซ้ำ

**AI 100% · no-vibe · FULL lane · 2026-09-14.** Dev can start from this self-contained pack: `0_DIRECTION` intent/lock/gates, `1_HTML` frozen local console, `2_BRD` business contract (.md/.docx), `3_FRD` implementation contract, `4_TC` 60 AI/QA cases, `5_DECLARATIONS` NTF/CSQ draft briefs, `6_UI_BRIEF` source-anchored UI map, `7_CTX` cross-feature reference. The FRD, not CTX or prototype, is implementation authority. BRD `APPROVED` is AI review, not stakeholder sign-off.

## Implement first
Exact tenant Item×Warehouse policy version + effective date; server-side bounds/reference/expectedVersion; Inventory/QHold read snapshot and availability formula; positive PR mock adapter and NC candidate adapter with durable idempotency; append-only event/outbox; scoped access and audit. Preserve three routes and frozen UI behavior. Do not create actual W2-PUR-LITE PR, deliver NC notification, register CSQ, mutate stock/movement, or implement W3-LITE GRN/PO/RTV or W5-FULL JE in this feature. NC owns its own threshold/channel/recipients, independent of ROP min. Production API and DB in FRD are proposed contracts; local HTML uses fixtures only.

## Decisions required from owners
| ID | Default used in this pack | Owner / release action |
|---|---|---|
| OQ-ROP-01 | `0≤safety≤min≤max`, trigger `available≤min`, replenish to max `[ASSUMED]` | Warehouse Product Owner confirms formula and equality rule |
| OQ-ROP-02 | QHold excluded available/ATP while retained onHand `[ASSUMED]` W4 §3 | Inventory/QHold owner confirms snapshot contract |
| OQ-ROP-03 | effective at tenant-local day start, UTC transport `[ASSUMED]` | Warehouse Product Owner confirms timezone/effective semantics |
| OQ-ROP-04 | missing/stale snapshot blocks positive advice; freshness SLA unknown `[ASSUMED]` | Inventory owner defines SLA/error contract |
| OQ-ROP-05 | Maker≠Approver if policy approval configured; no demo approval `[ASSUMED]` | DOA/Security owner decides slot/role matrix |
| OQ-ROP-06 | PR/NC mock envelope/ack/idempotency; 24h retention default `[ASSUMED contract]` | W2-PUR-LITE Procurement and NC owners approve contracts |
| OQ-ROP-07 | held>onHand clamps available0 and raises data-quality issue `[ASSUMED]` | Inventory owner confirms escalation |
| DECL-NTF | `rop.reorder_candidate` is provisional; catalog unavailable | Notification/NC owner reuses existing event or approves ID, template, recipients and channel |
| DECL-CSQ | `master.changed` master-policy DC is provisional; catalog unavailable | CSQ owner confirms event/tube or retires declaration; no registration now |

## Evidence and material WARN
Final HTML SHA-256 is in `0_DIRECTION/_GATES/HTML_FREEZE_SHA256.txt`. S3 v9 audit FAIL=0/WARN=2 (canonical icon class/token lint); isolated Node domain assertions 18/18; BRD C01–C23/PE gate, FRD A–M verifier 13/13; R2 coverage 82/82 ledger items and 60/60 QA mirror IDs. Calendar-date patch occurred after first S3 freeze; S3a–c were rerun and `HTML_DRIFT_SYNC.md` records that no FRD existed yet. Browser renderer and capture each failed twice because Playwright was unavailable (system capture also lacked PIL), so desktop/mobile visuals, real click sequence, screenshots and PDF preview were **NOT-CHECKED**. Twenty cases marked `sys:true` need backend/mock harness. Production auth, persistence, NC/CSQ catalog, actual downstream integration and performance remain untested. These warnings do not assert business behavior beyond the mock contract.

## Pack manifest
`0_DIRECTION`: LANE_BRIEF, RIF_v2, _SCOPE_LOCK, PREBRIEF, FUNCTION_CHECKLIST, COVERAGE_MAP, `_GATES` copied evidence. `1_HTML`: F-WH-ROP.html. `2_BRD`: BRD_F-WH-ROP.md/docx. `3_FRD`: 00–08 + INDEX. `4_TC`: testcases-F-WH-ROP.md, cases.json, case_ledger.json, exact Thai QA HTML and empty image map. `5_DECLARATIONS`: NTF/CSQ Markdown+JSON. `6_UI_BRIEF`: UI_BRIEF_F-WH-ROP.md. `7_CTX`: CTX_F-WH-ROP.md. Zip includes this HANDOFF.
