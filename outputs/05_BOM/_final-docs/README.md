# F-BOM-001 สูตรการผลิต — Dev Handoff Pack

> WF-01 Steps 1–10 complete · 2026-08-12  
> Prototype source of truth: `01_prototype/f-bom.html`  
> Production business/security contract: `04_frd/FRD_F-BOM_Pack/`

## เริ่มอ่าน

1. เปิด `08_tldr/FEATURE_TLDR_F-BOM-001.html` เพื่อเข้าใจฟีเจอร์ใน 2 นาที
2. เปิด `01_prototype/f-bom.html` เพื่อทดลองหน้าจอจริง
3. อ่าน `03_brd/BRD_F-BOM-001.md` สำหรับ business scope และ open questions
4. พัฒนาตาม `04_frd/FRD_F-BOM_Pack/` ทั้ง 7 ไฟล์
5. ใช้ `05_ui-brief/UI_BRIEF_F-BOM.md` คู่ prototype สำหรับ UI as-built และ Drift Log
6. ทดสอบด้วย `06_testcases/testcases-F-BOM.md` (AI/technical) และ `07_uat/testcase-F-BOM.html` (ผู้ใช้ Lite)

## เนื้อหา

| Folder | Artifact | Audience |
|---|---|---|
| `00_context/` | PREBRIEF + Function Checklist | BA/PM/Dev |
| `01_prototype/` | self-contained functional HTML prototype | ทุกทีม |
| `02_qc/` | UX, coverage round 1/2, E2E script | QA/Lead |
| `03_brd/` | BRD Markdown/DOCX + AI review | BA/PM |
| `04_frd/` | STANDARD FRD Pack 7 files | Dev/QA/DBA/Security |
| `05_ui-brief/` | extraction-based UI handoff | Frontend/QA |
| `06_testcases/` | 44 AI test cases | QA automation/agent |
| `07_uat/` | 23-case Lite UAT with 13 screenshots | End user/UAT |
| `08_tldr/` | one-page plain-language summary | ทุกทีม |

## Quality status

- Prototype E2E: **26/26 passed** (re-run during final verification)
- BRD AI gate: **28/28**
- FRD pack: 7/7 files; APIs 7; functions 9; engine 1; R8 trace complete
- Coverage round 2: substantive **PASS** — Function Checklist 24/24, BR 15/15, VR 8/8, confirmed EC 10/10, downstream edges 4/4
- Coverage verdict remains **WARN** only because `workflow_graph.json` / `NODE_BRIEF F-BOM` was not found
- UI Brief verification: 4/4 routes, 6/6 overlay categories, explicit 5-item drift log
- AI test suite: 44 cases; manifest 8/8; XT 8/8; Scope Lock covered
- UAT capture: **OK 13 · SKIP/FAIL 0**; smoke: 23 cases, 5 groups, 47 steps, no page errors
- TL;DR checker: **PASS**

## Production decisions that override the mock

- A non-active formula cannot be the default. The prototype seed/save path still allows `draft + is_default=true`; enforce FRD BR-02 and database constraints.
- Cost values are Confidential. The prototype displays them unconditionally; production must default-deny/mask according to D-CLASS.
- Unknown IDs need a visible not-found state in production; the prototype silently returns to the list.
- Loading, request error, stale-edit and permission states are FRD requirements but have no as-built visual design yet.

## Open items before production freeze

| ID | Item |
|---|---|
| OQ-BOM-01 | confirm amend/delete behavior when an MO already references the formula and immutable MO snapshot ownership |
| OQ-BOM-04 | confirm zero/null cost, scrap 100%, and deactivated Item/UoM policy |
| OQ-BOM-06 | confirm whether `eff_from` is a real business field or prototype residual |
| OQ-BOM-07 | formal `scope_lock_ref` — ไม่พบข้อมูลในบทสนทนา |
| OQ-BOM-08 | confirm production load profile/performance targets |
| Governance | `workflow_graph.json` / `NODE_BRIEF F-BOM` — ไม่พบข้อมูลในบทสนทนาและไม่พบใน workspace |

No approval/DOA, document configuration, notification declaration, CSV import/export, print/PDF transaction document, inventory posting, or GL posting belongs to this feature.

