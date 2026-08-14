# Workspace-local CUBE skills

- The 13 CUBE skills and the `kickoff` orchestrator are project-scoped through
  `.agents/skills`.
- Do not install or copy these skills into the user/global Codex skills directory.
- For every Python command used by these skills, use `.tools/python.cmd`. This
  wrapper selects `.venv`, UTF-8 mode, and the workspace-local Playwright cache.
- For Playwright installation or diagnostics, use `.tools/playwright.cmd`.
- On Windows, run shell-based skill checks with `.tools/bash.cmd`; do not use
  the WSL `bash` shim.
- Do not run `pip install` outside `.venv`, and do not install Playwright browsers
  outside `.tools/ms-playwright`.

# Codex feature workflow

Read the real paths from `.agents/workflow.paths.md`. In workflow rules, refer to
roles such as `CENTRAL_PLAN`, `BRIEF_ROOT`, and `OUTPUT_ROOT`; do not duplicate
their concrete business paths here.

Use Codex-provided memory/context when available, but verify that any referenced
workspace file still exists. Do not create or hardcode a Claude Code memory path.

## Entry point and approval gates

- Start with `$kickoff <feature>` or an equivalent request that triggers the
  repo-local `kickoff` skill.
- Stop at exactly three normal approval gates: after kickoff discovery and the
  neutral declaration choice, after step 5 with a one-line declaration recap,
  and after step 12 before commit.
- After kickoff approval, run steps 1 through 5 continuously. After the user
  reviews the HTML and fresh checks, run steps 6 through 12 continuously.
- Stop immediately on a `BLOCK` verdict, unresolved source conflict, material
  PREBRIEF gap, required edit to another feature, or a heavy test that still
  fails after one fix-and-rerun cycle.

## Twelve steps

1. Build or revise HTML with `html-generator-v8`; treat seed HTML as input, run
   its prescribed self-audit/static checks, and do not trust embedded pass claims.
2. Use `thai-doc-pdf-generator` for printable A4 output. This is the only
   skippable step and only when the feature has no printable document.
3. Run `qc-ux-html-checker` and produce `_UX_CHECK_REPORT.md`.
4. Run `qc-coverage-checker` round 1 against the confirmed feature brief,
   global contracts, and locked referenced features; update the `WF` column.
5. Run one feature E2E suite using shared `uikit.py`. Cover every `FN` and test
   every `FN-40` as a rendered negative case. Report `FN covered/total` and
   tests passed/total.
6. Generate BRD with `brd-generator-full` from PREBRIEF, checklist, and HTML.
7. Generate the FRD pack with `frd-generator-v6`.
   Immediately afterward, run only the declaration skills selected by the user
   at kickoff (as refined at the step-5 gate).
8. Generate the UI brief with `html-ui-brief`, then verify it using the shared
   `ui-brief-check.py --verify`.
9. Generate AI test cases with `ai-testcase-md-generator`; update the `QA` column.
10. Run `qc-coverage-checker` round 2 against FRD and test cases.
11. Generate end-user UAT with `qa-friendly-html-generator`; put the final UAT
    HTML at the feature folder root and keep only cases/evidence specs under `_qa`.
11.5. Generate `feature-tldr-html` last.
12. Close with `PROPOSALS_outbound.md`, unresolved OQs, applicable entries in
    `PENDING_REGISTRY`, and `declaration รอบนี้: ...` or `declaration รอบนี้: ไม่มี`;
    report full paths of user-facing files and wait for an explicit commit instruction.

## Declaration choice

- At kickoff, always present this neutral list in this exact order without a
  recommendation or evidence-based hint: `doccfg-declaration` (running document
  number), `doa-declaration` (approval chain), `ntf-declaration` (notification
  event), `none`, or `?` to decide at the step-5 gate.
- Let the user select zero through three declaration skills. The selection is
  authorization to run those skills after step 7; do not ask again then.
- At the step-5 gate, recap the selection in one line and allow changes. Ask the
  full question again only when the earlier answer was `?`.
- No selection means no declaration run and no repeated reminder during the
  remaining steps.
- Do not infer, recommend, or pre-check which declaration applies. Do not let a
  declaration skill invent a target code, approval chain, or notification event;
  missing business decisions become OQs for the BA/user.

## Integrity and precedence

- If HTML changes after step 5, rerun steps 3, 4, and 5 before continuing.
- Precedence: `html-generator-v8` for UI/BASE-KIT/CI; locked artifacts for
  cross-feature contracts; `CENTRAL_PLAN` for global contracts/waves/edges;
  PREBRIEF for this feature's business intent; checklist and seed HTML for FN
  inventory, not final appearance.
- Do not edit files under `.agents/skills` while executing a feature.
- Do not write a replacement UI checker. Reuse `uikit.py`; feature E2E files
  should contain only the feature-specific navigation and assertions.
- Do not use `wait_for_timeout`; use `ready()`, `settle()`, `after()`, or
  `hush()` from `uikit.py`.
- If a user-visible UI defect escapes the checker, fix the feature and extend
  shared `uikit.py`, then prove the new check fails against the broken version
  before restoring the fix.
- Before fixing any checker finding, verify it is real. Register BASE-KIT or CI
  issues in `PENDING_REGISTRY` instead of silently changing shared conventions.
- Never commit or propose a branch unless the user explicitly asks.

## Artifact placement

- Keep single-file deliverables at the feature root: HTML, BRD, UI brief, AI
  test cases, feature TLDR, proposals, check reports, and final UAT HTML.
- Keep multi-file internals in `FRD_Pack/`, `_e2e/`, and `_qa/`.
- Closing reports must include full paths to every file the user should open.
