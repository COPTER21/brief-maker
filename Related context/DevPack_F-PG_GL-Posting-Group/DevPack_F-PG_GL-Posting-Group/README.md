# DevPack — F-PG GL Posting Group (กลุ่มการบันทึกบัญชีแยกประเภท)

WF-01 HTML-first lane · Reverse Mode · ปิด 2026-08-10

## Folder structure

```
DevPack_F-PG_GL-Posting-Group/
├── 01_HTML/    HTML prototype + UI brief + QC gate reports + reference screenshots
├── 02_BRD/     PREBRIEF + Function Checklist + generated BRD
├── 03_FRD/     FRD Pack (STANDARD variant, 7 files, flattened — no wrapper folder)
└── 04_QA/      AI test cases (MD) + QA-friendly UAT HTML
```

## Contents

| File | จาก skill | สถานะ |
|---|---|---|
| `01_HTML/f-postgrp.html` | html-generator-v7 | ✅ PASS UX gate (iter. 3) + Coverage gate (iter. 2) |
| `01_HTML/HTML_UI_BRIEF_F-PG.md` | handoff (FRD 01_UI + HTML) | FE dev quick-start — routing, CI tokens, pages/patterns, lock-rule guard map, microcopy anchors, FN-40 checklist, known gaps |
| `01_HTML/_UX_CHECK_REPORT.md` | qc-ux-html-checker | ✅ PASS (8 non-blocking WARN) |
| `01_HTML/_COVERAGE_REPORT.md` | qc-coverage-checker | ✅ PASS |
| `01_HTML/_shots/` | qa-friendly-html-generator (capture) | 33 reference screenshots (list/create/edit/import/bulk-delete states) — referenced by `HTML_UI_BRIEF_F-PG.md` §8 |
| `02_BRD/PREBRIEF_F-PG_GL-Posting-Group.md` | input (PREBRIEF) | Reverse Mode source brief |
| `02_BRD/FUNCTION_CHECKLIST_F-PG_GL-Posting-Group.md` | input | FN-01..23, FN-40, FN-90 |
| `02_BRD/BRD_F-PG_GL-Posting-Group.md` | brd-generator-full | ✅ APPROVED (28/28) |
| `03_FRD/00_OVERVIEW.md` … `06_TESTS.md` (7 files) | frd-generator-v6 | ✅ STANDARD variant, no BLOCK |
| `04_QA/testcases-f-pg-gl-posting-group.md` | ai-testcase-md-generator | 80 cases, Manifest cross-check 26/26 ✅ |
| `04_QA/testcase-f-pg-gl-posting-group.html` | qa-friendly-html-generator | 80/80 cases 1:1, screenshots embedded |

## Open items for dev/PM before/at handoff

| ID | Status | Note |
|---|---|---|
| OQ-PG-01 | ✅ Decided 2026-08-10 (Option B — VAT Posting Setup tab 3) | **Build deferred to Phase 2** — not in this pack |
| OQ-PG-02 | ✅ Resolved | Real COA sync API contract in `03_FRD/02_API.md` §2.5 |
| OQ-PG-03 | 🟡 Open — due before dev handoff | `used` field real sync to journal count; confirm before go-live (affects IR-PG-01 lock) |
| OQ-PG-04 | ✅ Decided 2026-08-10 (use Item Master's 6-value set) | **Build deferred to Phase 2** — not in this pack |
| OQ-BRD-06 | 🟡 Open | Finance/Compliance to confirm Security Preset P4 (vs default P3) |

## Scope note

Tab 1 (Specific Posting Groups) + Tab 2 (General Posting Setup, as-built DOMESTIC/FOREIGN × GOODS/SERVICE axis) only. VAT Posting Setup (tab 3) and the Item-Master-aligned product axis are decided but **not built** — see Phase 2 in `02_BRD/BRD_F-PG_GL-Posting-Group.md` §13.
