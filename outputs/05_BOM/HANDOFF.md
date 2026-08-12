# HANDOFF — F-BOM-001 Bill of Materials · WF-01 COMPLETE

## Current status

- Steps 1–10 complete on 2026-08-12.
- Prototype source of truth: `outputs/05_BOM/01_HTML/f-bom.html`.
- Consolidated pack: `outputs/05_BOM/_final-docs/`.
- Start here: `outputs/05_BOM/_final-docs/README.md`.

## Delivered

| Step | Artifact |
|---:|---|
| 1–4 | `01_HTML/f-bom.html`, `02_QC/` reports and E2E |
| 5 | `03_BRD/BRD_F-BOM-001.md`, `.docx`, `_AI_REVIEW_REPORT.md` |
| 6 | `04_FRD/FRD_F-BOM_Pack/` (STANDARD, 7 files) + `_COVERAGE_REPORT_ROUND2.md` |
| 7 | `05_UI_BRIEF/UI_BRIEF_F-BOM.md` |
| 8 | `06_TESTCASES/testcases-F-BOM.md` (44 cases) |
| 9 | `07_UAT/testcase-F-BOM.html` (Lite 23 cases, 13 screenshots) |
| 10 | `08_TLDR/FEATURE_TLDR_F-BOM-001.html` |

## Verified results

- `rtk .tools/python.cmd outputs/05_BOM/02_QC/e2e_bom.py` → `E2E ROUND: 26/26 passed`.
- UAT capture → `CAPTURE VERIFY (R18): OK 13 · SKIP/FAIL 0`.
- UAT browser smoke → 23 cases, 5 groups, 47 result rows; image modal/localStorage/print preview work; `page_errors: []`.
- TL;DR check → `✅ PASS — ไม่มีศัพท์ระบบหลุด / placeholder ครบ / self-contained`.
- BRD DOCX is a valid Office archive and BRD AI review is 28/28.

## Known drift / do not copy blindly

1. HTML can produce or seed `draft + is_default=true`; production must enforce active-only default.
2. HTML shows raw cost to everyone; production must mask Confidential cost by permission.
3. Unknown IDs silently return to list; FRD requires visible not-found behavior.
4. HTML lacks production loading/error/stale/permission states.

## Still open

- OQ-BOM-01, OQ-BOM-04, OQ-BOM-06, OQ-BOM-08: see `_final-docs/README.md` and FRD `00_OVERVIEW.md` §0.10.
- Formal `scope_lock_ref`: ไม่พบข้อมูลในบทสนทนา.
- `workflow_graph.json` / `NODE_BRIEF F-BOM`: ไม่พบข้อมูลในบทสนทนาและไม่พบใน workspace; round-2 coverage is therefore `WARN` for governance, while available-contract coverage passes.

## Verbatim references

Production invariant that overrides the current mock:

`if target is not active, is_default=false`

