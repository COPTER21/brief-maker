# Workspace-local CUBE skills

- The six CUBE skills are project-scoped through `.agents/skills`, which points to
  `CUBE_Skills_Bundle_6_2026-07-30/skills`.
- Do not install or copy these skills into the user/global Codex skills directory.
- For every Python command used by these skills, use `.tools/python.cmd`. This
  wrapper selects `.venv`, UTF-8 mode, and the workspace-local Playwright cache.
- For Playwright installation or diagnostics, use `.tools/playwright.cmd`.
- On Windows, run shell-based skill checks with `.tools/bash.cmd`; do not use
  the WSL `bash` shim.
- Do not run `pip install` outside `.venv`, and do not install Playwright browsers
  outside `.tools/ms-playwright`.
