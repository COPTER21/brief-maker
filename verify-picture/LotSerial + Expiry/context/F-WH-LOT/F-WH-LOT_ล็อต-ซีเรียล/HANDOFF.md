# Dev handoff · F-WH-LOT · ล็อต-ซีเรียล

**AI 100% · no-vibe · dev เริ่มได้เลยจากแพ็กนี้.** Use BRD for business intent, FRD 00–08 for production behavior, frozen HTML + UI Brief for local UI, and TC/QA HTML for acceptance. Implement server contracts as specified, with the explicit owners below before external integration. `7_CTX` is for dependent feature briefs, not an implementation substitute for FRD.

## Pack inventory and gate verdict
| Folder | Artifact |
|---|---|
| 0_DIRECTION | RIF/PREBRIEF/FUNCTION_CHECKLIST/scope/coverage + frozen hash and gate evidence |
| 1_HTML | v9 single-file `F-WH-LOT.html`; no postfreeze edit |
| 2_BRD | BRD Markdown and DOCX (pandoc unavailable; python-docx fallback, structure checked) |
| 3_FRD | 9-file FRD with 14/14 Phase3.5 structural verification |
| 4_TC | 59-case manual TC, 59-case QA HTML, cases JSON and coverage ledger |
| 5_DECLARATIONS | CSQ brief JSON/MD and NTF divergence record |
| 6_UI_BRIEF | As-built UI map with 13 sections and FRD pairing |
| 7_CTX | Derived technical context card |

Lane: S3a WARN (v9 audit FAIL0/WARN2 and static heuristic false positives); S3b PASS 8/8 isolated pure-domain assertions; S3c WARN because Playwright browser launch failed twice, **no visual/browser interaction pass**. S6b WARN because QA builder has 0 screenshots. S6.5 WARN for visual gap, FN-08 API-only audit read and NC notification chip divergence. The pack is development-ready with these open verification items, not production-release approved. `0_DIRECTION/_GATES` has exact evidence and attempts.

## Fixed business rules
Per-item tracking `none|lot|serial` and expiry policy drive create validation; no item-name regex. Expiry-enabled item picking recommendation is FEFO; non-expiry is receipt order. Exclude expired, fully-held and zero-available candidates; `available=max(0,onHand-held)`. Recommendation does not reserve or adjust stock. Lot movement/identity audit is append-only; no delete/edit of movement history. `Avg` valuation is separate from lot picking order. (FRD BR-01..09)

## [ASSUMED] / OQ and owner
| Decision | Default used in pack | Owner before release |
|---|---|---|
| Serial identity quantity | one unit per serial; unique within tenant+item | Warehouse Product Owner |
| FEFO ties | expiry date → receipt date → stable lot code; non-expiry receipt date → lot code | Warehouse Product Owner |
| Availability snapshot | `max(0,onHand-held)` with no reservation; expiry compare at current date | Warehouse Product Owner + Inventory owner |
| Policy version/effective date | future effective policy version, no rewrite of old identity/movement | Warehouse Product Owner |
| API paths/response and W3-LITE movement envelope | proposed endpoints and soft-reference payload in FRD | API owner + W3-LITE owner |
| CSQ `master.changed` envelope | [ASSUMED contract] because owner skill references missing csq-contract resource | CSQ owner/registry |
| NC near-expiry notification | threshold/channels/recipients external; W4 chip `csq` vs detected `ntf` DIVERGENCE | NC owner + registry owner |
| Retention/actor-ID classification | central security policy; actor ID flagged PII | Security owner |
| Visible config audit | API-06 specified, prototype has local event collection but no config audit UI | Warehouse Product Owner + UI owner |

## Mock/TODO boundaries
- W3-LITE GRN/Transfer movement reader returns immutable exact-lot source refs or unavailable/empty. This pack does **not** receive, transfer, reverse, or post inventory.
- Picking consumes ranked API-04 candidates; it owns reservation/issue. This feature does not make those calls.
- NC/ENG-NOTIFY and CSQ own notification delivery and 7C respectively; TC asserts only candidate/envelope shape under mock harness, never external delivery/stamp.
- No JE connection in this feature. Count variance and valuation are separate features, not implemented here.

## Required verification before production release
UI QA opens desktop and narrow viewport, checks drawer/menu/toolbar/tab rendering and executes browser-facing TC; attach screenshots to QA artifact. Integration QA executes the 15 `system/mock` cases with controlled API/mocks for role, tenant, idempotency, movement source and event envelope. Owners above resolve ASSUMED contracts and divergence; update FRD/CTX and rerun impacted gates if decisions alter the frozen UI.
